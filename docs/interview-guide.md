# Discovery Interview Guide

**Goal:** Learn how infra and ML platform teams decide between APIs, rented GPUs, and owned hardware, and which costs they track. Answers feed the open questions in `prd.md`.

**Who to recruit (5–8 people):** ML engineers, ML platform or infra leads, and engineering managers running LLMs in production. Good sources are LinkedIn, CSUEB alumni, and Bay Area ML meetups. Aim for at least 2 people who have self-hosted a model.

**Format:** 25 minutes, recorded with permission. Ask about past behavior, not opinions about the future.

## Script

**Context (3 min)**
1. What LLM workloads does your team run in production today?
2. Who decides how they're served, and who pays the bill?

**Last decision (10 min)**
3. Tell me about the last time you chose between an API and hosting a model yourselves. What happened?
4. What numbers did you look at? Where did they come from?
5. What surprised you after launch, in cost, reliability, or effort?
6. Roughly what share of your GPU time is doing useful work? How do you know?

**Hidden costs (6 min)**
7. What costs didn't show up on the GPU or API bill?
8. How much engineering time goes into keeping self-hosted models running?

**Tool reaction (5 min):** Share the dashboard.
9. Walk me through what you'd do first. What's confusing?
10. What input is missing that would change your answer?
11. Would you use this for a real decision? What would stop you?

**Close (1 min)**
12. Who else should I talk to?

## Synthesis template

Fill in one row per interview. Look for patterns that show up in 3 or more interviews.

| # | Role / company size | Current setup | Last decision and why | Utilization (known?) | Hidden costs named | Tool reaction | Top quote |
|---|---|---|---|---|---|---|---|
| 1 | | | | | | | |

## After interviews, add to README

- 3–5 patterns, each with a count (e.g., "4 of 6 didn't know their utilization")
- 2–3 short quotes, anonymized
- What changed in the product or the v2 priority list because of it

Only include this section once you've done the interviews. Don't publish hypothetical findings.
