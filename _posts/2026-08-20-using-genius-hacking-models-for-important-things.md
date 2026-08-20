---
title: "Using Genius Hacking Models for Important Things: Cheating to Get the NetHack 5.0 High Score"
layout: post
date: 2026-08-20 00:00:00 -0400
description: "How I used GPT-5.6 Daybreak Blue to find an on-demand NetHack 5.0 crash, duplicate items, farm krakens, and get the high score on NAO."
image: /assets/images/nethack-kraken-farm.png
categories:
  - hacking
tags:
  - ai
  - hacking
  - cybersecurity
---
![](/assets/images/nethack-kraken-farm.png){: width="600" }
This is how I used GPT-5.6 Daybreak Blue to find a buffer overflow, crash the game in order to dupe items, and get the high score on the NetHack 5.0 leaderboard.

I love NetHack. It's such an awesome game. And I love hacking/bug hunting. So when I met Demo (aka [turb0](https://x.com/7urb01)), who is an epic bug bounty hunter and has ascended NetHack (and variants) around 300 times, I asked him a million questions.

My favorite thing he told me about was how he'd do a "hacked run" nearly every year at [Junethack](https://junethack.net/), the annual NetHack tournament. He would show off the bugs he found during the previous year and use them to break the game in some way.

I wanted to do that too! But I'm not nearly as good at deep white-box vulns as he is. Luckily, top AI models finally are. So I set GPT-5.6 Daybreak Blue on the hunt. Within a few hours, it found an **ideal crash**. It could be induced at any time rather than only during specific actions.

![GPT-5.6 Daybreak Blue reporting the NetHack crash recovery exploit chain](/assets/images/nethack-daybreak-finds-crash-recovery.png){: width="700" }
*Daybreak Blue coming back with: "Yes, this is real."*

### The crash

NetHack 5 had an integer-truncation bug in [`resize_tty()`](https://github.com/k21971/NAO-5.x/blob/3aa4ab31751d3886436d94b585a96704892fd477/win/tty/wintty.c#L392-L411): terminal widths above 32,767 wrapped negative, leading to an undersized allocation and out-of-bounds write. Resizing to 65,529 columns and back reliably crashed the game.

That was unusually powerful because it gave players an on-demand crash at any exact moment. During a level transition, NetHack saved the departing level before updating its global checkpoint. We dropped an item, descended, paused at `--More--`, and triggered the crash. Recovery then combined the new level file, containing the dropped item, with the old global state, where it was still in inventory. The result was a duplicate, including charged wands of wishing and unique artifacts.

Crazily enough, Demo had hypothesized an issue here in the past.

![Demo asking whether terminal width and height could reach dangerous sinks in NetHack](/assets/images/nethack-demo-terminal-size-hypothesis.png){: width="600" }
*Demo was asking exactly the right question a year earlier.*

### The live chain

I reproduced the complete chain on live NAO. You can see where they fixed it [here](https://github.com/k21971/dgamelaunch/commit/1a6653f0c3ba8e44e297f4e394952603ab45d734), followed by a [fix for a bypass in the original patch](https://github.com/k21971/dgamelaunch/commit/9e055c3108f69e34a87ad57e06c555bcd635446e). I was credited on the main page.

Shoutout to dtype, the dev who fixed it.

![NAO crediting rez0 for the overflow report](/assets/images/nethack-nao-credit.png){: width="700" }
*Thanks, NAO!*

[NAO](https://www.alt.org/nethack/) (nethack.alt.org) is the major server where most people play. The other main one is [Hardfought](https://www.hardfought.org/nethack/), but NAO is the vanilla server. All the wishes, deaths, and ascensions there get posted in [IRC](https://www.alt.org/nethack/irc.php).

Duping wishes and making tons of wishes is naturally very noisy. Other players were annoyed and started tagging devs. The devs got to fixing it before I used the best and easiest way to rack up an insane score: duping dilithium crystals.

![NetHack players noticing rez0bot's wish spam in IRC](/assets/images/nethack-players-catching-on-wish-spam.png){: width="700" }
*Other players starting to notice: "I don't understand how all of that is possible."*

They patched it, and I didn't have enough wishes to wish for tons of dilithium crystals, but I had lots of scrolls and wishes. So I wished for magic markers and wrote cursed scrolls of genocide so that I could later reverse genocide (summon) lots of krakens. Krakens give the most experience, so I could farm them for experience instead.

![603 cursed scrolls of genocide in the NetHack inventory](/assets/images/nethack-603-cursed-scrolls-of-genocide.png){: width="362" }
*A completely normal number of cursed scrolls of genocide.*

Krakens are the red semicolons.

![A NetHack level packed with summoned krakens](/assets/images/nethack-kraken-farm.png){: width="750" }
*Every red semicolon is a kraken.*

### The high score

Anyways, I eventually got the [high score](https://www.alt.org/nethack/top-5.0.php).

![rez0bot at the top of the NetHack 5.0 leaderboard](/assets/images/nethack-5.0-high-score-leaderboard.png){: width="750" }
*29,926,212 points. Number one on NAO's NetHack 5.0 leaderboard.*

![Rodney announcing rez0bot as number one on the NetHack 5.0 leaderboard](/assets/images/nethack-rodney-high-score-announcement.png){: width="600" }
*Rodney announcing the result in IRC.*

The full [dumplog is here](https://www.alt.org/nethack/userdata/r/rez0bot/dumplog/1786710983.nh500.txt).

This is the kind of important work genius hacking models were made for :P Also, the nethack server NAO is awesome and they let hacked runs like this live on in infamy on the leaderboard. Thanks to Demo for the inspiration, and to the NAO devs (mostly dtype) for being so cool about everything.

\- Joseph

[Sign up for my email list](https://thacker.beehiiv.com/subscribe) to know when I post more content like this.

I also [post my thoughts on Twitter/X](https://x.com/rez0__).

<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:site" content="@rez0__" />
<meta name="twitter:creator" content="@rez0__" />
<meta property="og:url" content="https://josephthacker.com/hacking/2026/08/20/using-genius-hacking-models-for-important-things.html" />
<meta property="og:title" content="Using Genius Hacking Models for Important Things: Cheating to Get the NetHack 5.0 High Score" />
<meta property="og:description" content="How I used GPT-5.6 Daybreak Blue to find an on-demand NetHack 5.0 crash, duplicate items, farm krakens, and get the high score on NAO." />
<meta property="og:image" content="https://josephthacker.com/assets/images/nethack-kraken-farm.png" />
