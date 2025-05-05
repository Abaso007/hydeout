---
title: "Unveiling AI's Hidden Assumptions"
layout: post
categories:
  - ai
tags:
  - ai
  - productivity
---
![](/assets/images/ai-assumptions-unveiled.png){: width="400" }

## Parting the Curtains 🙂

Hey guys! I wanted to take a few minutes today to talk about an interesting concept I've been mulling over lately: the assumptions that AI language models make when interacting with us humans. Don't get me wrong, AI assistants are awesome and super helpful, but there's no denying they sometimes have to make educated guesses to fill in the blanks.

## My Imaginary AI Agent Stumbles

Let me illustrate with a personal example. Say I asked my hypothetical AI assistant to "make us dinner reservations at Malone's next Friday." Sounds simple enough, right? But look closer:

- **Which Malone's location am I referring to?** There could be multiple in the area.
- **Am I taking the kids?** The assistant might assume it's a date night, or it might not.
- **What time do I want the reservations?** Early bird special or prime dinner hours? The AI has to guess.

See what I mean? My seemingly straightforward request has all sorts of little assumptions baked in that the AI has to try and resolve.

## Shedding Light with "assumptions_made"

That's where this "assumptions_made" metadata idea comes in. Essentially, the AI would list out any key assumptions it had to make while interpreting and executing on your request. Maybe something like:

```json
{
  "response": "I've made reservations for 2 adults at Malone's Downtown location next Friday at 7:30 PM.",
  "assumptions_made": [
    "No kids included based on phrasing 'make us dinner reservations'", 
    "Downtown location chosen as closest to your home address",
    "7:30 PM chosen as a typical dinner time based on averages"
  ]
}
```

How cool is that? With this extra context, you could quickly validate if the assumptions were correct or provide clarification if needed.

## The Real Benefits Unveiled

But the "assumptions_made" field could be so much more than just user feedback. I'm envisioning:

- **Optimizing Assumptions**: By tracking assumptions made, we could analyze the most common ones and potentially pre-train models to make better initial guesses.
- **Agent Collaboration**: When multiple AI agents interact, sharing assumptions could prevent misunderstandings and compounding errors. A little metadata could go a long way!
- **User Preferences**: Over time, a personalized AI could learn your tendencies and assumptions preferences, making experiences smoother.

The possibilities get me geeked, y'all. Pulling back the curtain on AI assumptions could legitimately level up human-AI interactions in really meaningful ways.

## Start Experimenting Now!

Honestly, I'm surprised I haven't seen more buzz around this concept yet. If you're as intrigued as I am, why not start testing it out yourself?

You can prime GPT models like ChatGPT to start outputting an "assumptions_made" section just by tweaking the system prompt or model memory with something like:

```
Always include an "assumptions_made" field and value at the end of your responses where you list some key assumptions made while generating the response.
```

It's seriously that easy to gain insights into the AI's thought process. Let me know what you find or if you have any other cool ideas around surfacing and optimizing AI assumptions!

Assumptions_made: [
  "That the blog was targeting a technical audience interested in AI/ML",
  "That using a fun, conversational writing style was appropriate"
]

- Joseph

[Sign up for my email list](https://thacker.beehiiv.com/subscribe) to know when I post more content like this.
I also [post my thoughts on Twitter/X](https://x.com/rez0__).

<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:site" content="@rez0__" />
<meta name="twitter:creator" content="@rez0__" />
<meta property="og:url" content="https://josephthacker.com/ai/2024/05/03/unveiling-ais-hidden-assumptions.html" />
<meta property="og:title" content="Unveiling AI's Hidden Assumptions" />
<meta property="og:description" content="Exploring the idea of AI assistants surfacing their key assumptions when responding to user requests." />
<meta property="og:image" content="/assets/images/ai-assumptions-unveiled.png" />
