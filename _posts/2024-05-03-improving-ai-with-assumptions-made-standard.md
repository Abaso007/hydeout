---
title: "Improving AI with 'assumptions_made' Standard"
layout: post
categories:
  - ai
tags:
  - ai
  - hacking
  - cybersecurity
---
![](/assets/images/ai_agents_assumptions_made.png){: width="400" }
# Introducing the "assumptions_made" Standard for AI Agents

Hey there, tech enthusiasts! Today, I want to talk about a cool idea that could really improve the way AI agents and chatbots interact with each other and with us humans. It's called the "assumptions_made" standard, and I think it has the potential to be a game-changer.

## The Problem with Assumptions

So, here's the deal. With the rise of large language models (LLMs) and AI agents, we're seeing some seriously awesome chatbots and tools being built. These AI systems often rely on APIs and plugins to get things done. The problem is, when a user makes a request, there are often assumptions embedded in it that the AI has to interpret based on its context.

Let me give you a concrete example to illustrate what I mean. Imagine you have an AI agent that can book dinner reservations for you. You might say something like, "Make us dinner reservations at Malone's next Friday." Seems simple enough, right? But there are actually a few assumptions hidden in that request:

1. Which location of Malone's do you want to go to?
2. Are you bringing your kids or is this a date night?
3. What time do you typically eat dinner?

The AI agent has to make a "best guess" based on the context it has, but it might not always get it right. And that's where the "assumptions_made" standard comes in.

## Introducing the "assumptions_made" Standard

The idea is pretty simple. Whenever an AI agent or chatbot makes a response, it would include an "assumptions_made" field that lists out any assumptions it had to make in order to generate that response. This field could be a JSON object or just a plain text addendum at the end of the output.

Here's why I think this could be really powerful:

1. It provides transparency into the AI's decision-making process
2. It allows the user to correct any incorrect assumptions
3. It could eventually be baked into the LLMs themselves to improve accuracy

Imagine if every AI agent included an "assumptions_made" field in its responses. When those agents communicate with each other, they could use that information to avoid making incorrect decisions and to know when to ask for clarification. I believe this could be a major step forward in improving the quality and consistency of many-agent frameworks.

## Try It Out Yourself

If you're curious to see the "assumptions_made" standard in action, you can easily try it out with ChatGPT or another AI assistant. Just add something like this to the system prompt or memory:

```
Always include an "assumptions_made" field and value at the end of your responses where you list some assumptions you made with your response.
```

Then, start chatting and see what assumptions the AI is making based on your requests. It's pretty eye-opening!

## The Bottom Line

At the end of the day, I believe the "assumptions_made" standard could be a valuable addition to the world of AI agents and chatbots. By providing more transparency and context around the assumptions being made, we can improve the accuracy and reliability of these systems as they become increasingly sophisticated.

Of course, this is just one idea and there's still a lot of work to be done in this space. But I'm excited to see where it goes and how it evolves over time.

What do you think? Is the "assumptions_made" standard something you'd like to see implemented in AI agents? Let me know in the comments below!

assumptions_made:
- The reader is familiar with AI, LLMs, and chatbots
- The reader would find a technical standard like this interesting
- The reader knows how to modify system prompts in ChatGPT
- The reader wants to learn about improving AI agent interactions

- Joseph

[Sign up for my email list](https://thacker.beehiiv.com/subscribe) to know when I post more content like this.
I also [post my thoughts on Twitter/X](https://x.com/rez0__).

<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:site" content="@rez0__" />
<meta name="twitter:creator" content="@rez0__" />
<meta property="og:url" content="https://josephthacker.com/ai/2024/05/03/improving-ai-with-assumptions-made-standard.html" />
<meta property="og:title" content="Improving AI with 'assumptions_made' Standard" />
<meta property="og:description" content="Introducing a proposed standard to improve AI agent transparency and accuracy by surfacing the assumptions made during interactions." />
<meta property="og:image" content="/assets/images/ai_agents_assumptions_made.png" />
