import chromadb
from chromadb.utils import embedding_functions
import uuid

class BasicRAG:
    def __init__(self, collection_name="my_collection"):
        self.client = chromadb.Client()
        self.ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        self.collection = self.client.create_collection(name=collection_name, embedding_function=self.ef)

    def add_data(self, texts, metadatas=None):
        """
        Add data to the vector store.
        
        :param texts: List of text chunks to add
        :param metadatas: List of metadata dicts corresponding to each text chunk (optional)
        """
        ids = [str(uuid.uuid4()) for _ in texts]
        self.collection.add(
            documents=texts,
            metadatas=metadatas if metadatas else [{}] * len(texts),
            ids=ids
        )
        print(f"Added {len(texts)} documents to the collection.")

    def lookup(self, query, n_results=5):
        """
        Look up the closest chunks for a given query.
        
        :param query: The query text
        :param n_results: Number of results to retrieve
        :return: List of retrieved documents and their metadata
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        retrieved_docs = []
        for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
            retrieved_docs.append({
                'document': doc,
                'metadata': metadata
            })
        
        return retrieved_docs

# Example usage
if __name__ == "__main__":
    rag = BasicRAG()
    
    # Adding data
    texts = [
        "The quick brown fox jumps over the lazy dog.",
        "Python is a high-level programming language.",
        "Machine learning is a subset of artificial intelligence.",
        "Natural language processing deals with the interaction between computers and humans using natural language.",
    ]
    metadatas = [
        {"source": "common phrase"},
        {"source": "programming"},
        {"source": "AI"},
        {"source": "NLP"},
    ]
    rag.add_data(texts, metadatas)
    
    # Looking up
    query = "What is Python programming?"
    results = rag.lookup(query, n_results=2)
    
    print(f"Query: {query}")
    print("Results:")
    for i, result in enumerate(results, 1):
        print(f"{i}. Document: {result['document']}")
        print(f"   Metadata: {result['metadata']}")
        print()