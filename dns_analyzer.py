import dns.resolver
import asyncio
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import logging
from .base_analyzer import BaseAnalyzer
from tenacity import retry, stop_after_attempt, wait_exponential
import whois
import tldextract
import socket
import aiodns

logger = logging.getLogger(__name__)

class DNSAnalyzer(BaseAnalyzer):
    def __init__(self):
        self.resolver = dns.resolver.Resolver()
        self.resolver.timeout = 2
        self.resolver.lifetime = 4
        
        # Essential DNS records to check
        self.record_types = {
            'A': {'weight': 1.0, 'required': True},
            'AAAA': {'weight': 0.5, 'required': False},
            'MX': {'weight': 0.8, 'required': True},
            'NS': {'weight': 1.0, 'required': True},
            'TXT': {'weight': 0.8, 'required': True},
            'SOA': {'weight': 0.8, 'required': True},
            'DMARC': {'weight': 0.8, 'required': False},
            'SPF': {'weight': 0.8, 'required': False}
        }
        
        # Known reliable nameservers
        self.reliable_nameservers = {
            'cloudflare': ['cloudflare.com', 'cloudflare-dns.com'],
            'google': ['google.com', 'googledns.com'],
            'amazon': ['aws.com', 'awsdns'],
            'microsoft': ['microsoft.com', 'azure-dns'],
            'godaddy': ['godaddy.com', 'domaincontrol.com'],
        }

    async def analyze(self, domain: str, html_content: str = None) -> Dict:
        """Enhanced DNS analysis with comprehensive checks."""
        analysis_start_time = datetime.utcnow()
        
        try:
            results = {
                "timestamp": analysis_start_time.isoformat(),
                "domain": domain,
                "records": {},
                "security_score": 10.0,
                "risk_level": "SECURE",
                "issues": [],
                "warnings": [],
                "recommendations": []
            }

            # Run all DNS checks concurrently
            tasks = [
                self._check_basic_records(domain),
                self._check_email_security(domain),
                self._check_nameservers(domain),
                self._check_dnssec(domain),
                self._check_reverse_dns(domain)
            ]
            
            checks = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            basic_records, email_security, nameserver_info, dnssec_info, reverse_dns = checks
            
            # Update results with all findings
            results.update({
                "records": basic_records.get("records", {}),
                "email_security": email_security,
                "nameservers": nameserver_info,
                "dnssec": dnssec_info,
                "reverse_dns": reverse_dns
            })
            
            # Calculate security score
            score_factors = self._calculate_security_score(results)
            results["security_score"] = score_factors["score"]
            results["risk_level"] = self._get_risk_level(score_factors["score"])
            results["issues"].extend(score_factors["issues"])
            results["warnings"].extend(score_factors["warnings"])
            
            # Generate recommendations
            results["recommendations"] = self._generate_recommendations(results)
            
            return results

        except Exception as e:
            logger.error(f"DNS analysis error for {domain}: {str(e)}")
            return self._create_error_response(domain, str(e), analysis_start_time)

    async def _check_basic_records(self, domain: str) -> Dict:
        """Check basic DNS records (A, AAAA, MX, NS, TXT, SOA)."""
        records = {}
        issues = []
        
        for record_type in ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA']:
            try:
                answers = await self._dns_lookup_with_timeout(domain, record_type)
                if answers:
                    records[record_type] = [str(rdata) for rdata in answers]
                elif self.record_types[record_type]['required']:
                    issues.append(f"Missing required {record_type} record")
            except Exception as e:
                logger.warning(f"Error checking {record_type} records: {str(e)}")
                
        return {"records": records, "issues": issues}

    async def _check_email_security(self, domain: str) -> Dict:
        """Check email security records (SPF, DMARC, DKIM)."""
        results = {
            "spf": {"found": False, "valid": False, "record": None},
            "dmarc": {"found": False, "valid": False, "record": None},
            "dkim_selectors": []
        }
        
        # Check SPF
        try:
            txt_records = await self._dns_lookup_with_timeout(domain, 'TXT')
            for record in txt_records:
                if str(record).startswith('"v=spf1'):
                    results["spf"] = {
                        "found": True,
                        "valid": self._validate_spf(str(record)),
                        "record": str(record)
                    }
        except Exception:
            pass

        # Check DMARC
        try:
            dmarc_records = await self._dns_lookup_with_timeout(f"_dmarc.{domain}", 'TXT')
            for record in dmarc_records:
                if str(record).startswith('"v=DMARC1'):
                    results["dmarc"] = {
                        "found": True,
                        "valid": self._validate_dmarc(str(record)),
                        "record": str(record)
                    }
        except Exception:
            pass

        # Check common DKIM selectors
        common_selectors = ['default', 'google', 'k1', 'selector1', 'selector2']
        for selector in common_selectors:
            try:
                dkim_records = await self._dns_lookup_with_timeout(f"{selector}._domainkey.{domain}", 'TXT')
                if dkim_records:
                    results["dkim_selectors"].append(selector)
            except Exception:
                continue

        return results

    async def _check_nameservers(self, domain: str) -> Dict:
        """Check nameserver configuration and reliability."""
        try:
            ns_records = await self._dns_lookup_with_timeout(domain, 'NS')
            nameservers = [str(ns) for ns in ns_records]
            
            results = {
                "nameservers": nameservers,
                "count": len(nameservers),
                "reliable_provider": False,
                "geographically_distributed": False
            }
            
            # Check if using reliable provider
            for provider, domains in self.reliable_nameservers.items():
                if any(any(domain in ns.lower() for domain in domains) for ns in nameservers):
                    results["reliable_provider"] = True
                    results["provider"] = provider
                    break
            
            # Check geographical distribution
            if len(nameservers) >= 2:
                results["geographically_distributed"] = True
            
            return results
            
        except Exception as e:
            logger.error(f"Error checking nameservers: {str(e)}")
            return {"nameservers": [], "count": 0, "reliable_provider": False}

    async def _check_dnssec(self, domain: str) -> Dict:
        """Check DNSSEC configuration."""
        try:
            # Check for DNSSEC records
            dnskey_records = await self._dns_lookup_with_timeout(domain, 'DNSKEY')
            ds_records = await self._dns_lookup_with_timeout(domain, 'DS')
            
            return {
                "enabled": bool(dnskey_records and ds_records),
                "valid": bool(dnskey_records and ds_records),
                "algorithms": [str(record.algorithm) for record in dnskey_records] if dnskey_records else []
            }
        except Exception:
            return {"enabled": False, "valid": False, "algorithms": []}

    async def _check_reverse_dns(self, domain: str) -> Dict:
        """Check reverse DNS configuration."""
        try:
            # Get A records
            a_records = await self._dns_lookup_with_timeout(domain, 'A')
            if not a_records:
                return {"configured": False, "matches": False}
            
            # Check reverse DNS for first IP
            ip = str(a_records[0])
            try:
                reverse_name = await asyncio.to_thread(socket.gethostbyaddr, ip)
                return {
                    "configured": True,
                    "matches": domain in reverse_name[0],
                    "reverse_name": reverse_name[0]
                }
            except socket.herror:
                return {"configured": False, "matches": False}
                
        except Exception:
            return {"configured": False, "matches": False}

    def _validate_spf(self, record: str) -> bool:
        """Validate SPF record format and content."""
        record = record.strip('"')
        if not record.startswith('v=spf1'):
            return False
            
        # Check for common issues
        if record.count('all') > 1:
            return False
        if not any(m in record for m in ['~all', '-all', '?all', '+all']):
            return False
            
        return True

    def _validate_dmarc(self, record: str) -> bool:
        """Validate DMARC record format and content."""
        record = record.strip('"')
        if not record.startswith('v=DMARC1'):
            return False
            
        # Check for required tags
        required_tags = ['p=']
        return all(tag in record for tag in required_tags)

    def _calculate_security_score(self, results: Dict) -> Dict:
        """Calculate security score with detailed factors."""
        score = 10.0
        issues = []
        warnings = []
        
        # Check basic records
        for record_type, config in self.record_types.items():
            if config['required'] and record_type not in results.get('records', {}):
                score -= config['weight']
                issues.append(f"Missing {record_type} record")
        
        # Check email security
        email_security = results.get('email_security', {})
        if not email_security.get('spf', {}).get('valid'):
            score -= 1.0
            warnings.append("Invalid or missing SPF record")
        if not email_security.get('dmarc', {}).get('valid'):
            score -= 1.0
            warnings.append("Invalid or missing DMARC record")
        if not email_security.get('dkim_selectors'):
            score -= 0.5
            warnings.append("No DKIM selectors found")
        
        # Check nameservers
        ns_info = results.get('nameservers', {})
        if ns_info.get('count', 0) < 2:
            score -= 1.0
            issues.append("Insufficient number of nameservers")
        if not ns_info.get('reliable_provider'):
            score -= 0.5
            warnings.append("Not using a major DNS provider")
        
        # Check DNSSEC
        if not results.get('dnssec', {}).get('enabled'):
            score -= 1.0
            warnings.append("DNSSEC not enabled")
        
        # Check reverse DNS
        if not results.get('reverse_dns', {}).get('matches'):
            score -= 0.5
            warnings.append("Reverse DNS not properly configured")
        
        return {
            "score": max(0.0, min(10.0, score)),
            "issues": issues,
            "warnings": warnings
        }

    def _generate_recommendations(self, results: Dict) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []
        
        # Add recommendations based on issues
        if results.get("issues"):
            for issue in results["issues"]:
                if "Missing" in issue:
                    recommendations.append(f"Configure {issue.split()[-2]} record")
                elif "Insufficient" in issue:
                    recommendations.append("Add additional nameservers for redundancy")
        
        # Add recommendations based on warnings
        if results.get("warnings"):
            for warning in results["warnings"]:
                if "SPF" in warning:
                    recommendations.append("Configure SPF record with appropriate policy")
                elif "DMARC" in warning:
                    recommendations.append("Configure DMARC record with appropriate policy")
                elif "DKIM" in warning:
                    recommendations.append("Configure DKIM for email authentication")
                elif "DNSSEC" in warning:
                    recommendations.append("Enable DNSSEC for additional security")
                elif "DNS provider" in warning:
                    recommendations.append("Consider using a major DNS provider for better reliability")
        
        return recommendations[:5]  # Return top 5 recommendations

    def _create_error_response(self, domain: str, error: str, start_time: datetime) -> Dict:
        """Create standardized error response."""
        return {
            "timestamp": start_time.isoformat(),
            "domain": domain,
            "security_score": 0.0,
            "risk_level": "ERROR",
            "error": error,
            "records": {},
            "issues": ["DNS analysis failed"],
            "warnings": [],
            "recommendations": [
                "Verify domain name is correct",
                "Check domain's DNS configuration",
                "Ensure domain is properly registered"
            ]
        }

    def _get_risk_level(self, score: float) -> str:
        """Determine risk level based on security score."""
        if score >= 9.0:
            return "SECURE"
        elif score >= 7.0:
            return "LOW"
        elif score >= 5.0:
            return "MEDIUM"
        elif score >= 3.0:
            return "HIGH"
        else:
            return "CRITICAL"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def _dns_lookup_with_timeout(self, domain: str, record_type: str) -> List:
        """Perform DNS lookup with retry logic and timeout."""
        try:
            if record_type == 'DMARC':
                domain = f"_dmarc.{domain}"
                record_type = 'TXT'
            elif record_type == 'SPF':
                record_type = 'TXT'

            resolver = aiodns.DNSResolver()
            resolver.nameservers = ['8.8.8.8', '1.1.1.1']  # Use reliable DNS servers
            
            try:
                result = await resolver.query(domain, record_type)
                return result if isinstance(result, list) else [result]
            except aiodns.error.DNSError as e:
                if 'DNS server returned answer with no data' in str(e):
                    return []
                raise

        except Exception as e:
            logger.warning(f"DNS lookup failed for {domain} ({record_type}): {str(e)}")
            return [] 