---
title: "I Built an AI That Finds Bad Local Business Websites (And Pitches Them Redesigns)"
published: false
description: "How I used Hermes Agent to build an autonomous web quality scanner that prospects, scores, and generates pitch reports for local businesses — replacing hours of manual work with a single command."
tags: hermesagentchallenge, devchallenge, agents, python, webdev
---

# I Built an AI That Finds Bad Local Business Websites (And Pitches Them Redesigns)

Your dentist's website loads 58 JavaScript files before showing a single image. The local steakhouse has 122 elements that break on mobile. The auto body shop uses 25 different font families on one page.

I know this because I built an AI agent that finds these problems automatically — and then writes the pitch email to fix them.

## The Problem

I run a web design agency. My best clients are local businesses with terrible websites. But finding them meant manually visiting hundreds of sites, screenshotting the ugly ones, writing up reports, and crafting personalized pitches. It was mind-numbing work that ate hours every week.

So I taught my AI agent to do it.

## What I Built

**Hermes Local Business Web Scanner** — a tool built on [Hermes Agent](https://hermes-agent.nousresearch.com/) that takes a city and industry, then autonomously:

1. **Discovers** local businesses via web search
2. **Scores** their websites across 5 categories (mobile, design, SEO, accessibility, performance)
3. **Ranks** them worst-first (best prospects at the top)
4. **Generates** visual pitch reports with specific issues
5. **Writes** personalized pitch email drafts

One command. Full prospecting pipeline. Done.

## Demo: Tupelo, MS

I ran it against businesses across different industries. Every single one had real problems costing them customers.

### 🔴 Blue Canoe — Dive Bar — Grade: D (57%)

Tupelo's beloved live music venue. Great vibe, rough website.

The agent found 58 scripts blocking render, no meta description (invisible on Google), no H1 heading, and 8 fixed-width elements that break mobile completely. Their site is a local institution that nobody can find on search.

### 🔴 Tom's Automotive — Auto Repair — Grade: D (59%)

Family-owned shop. Clean 49KB site but zero calls-to-action. No "Book Now." No "Get a Quote." Visitors show up and don't know what to do. Plus 13 touch targets too small to tap on a phone.

### 🔴 Auto Spa of Tupelo — Auto Body — Grade: D (58%)

Collision and paint shop. Their page is 984KB with 25 font families. Twenty-five. Mobile is completely broken with 223 fixed-width elements. It's the kind of site that makes you think the business is closing — when they're actually thriving.

### 🟠 Woody's Tupelo Steakhouse — Restaurant — Grade: C (61%)

A 30-year Tupelo institution. Their site has 122 fixed-width elements, 110 tiny touch targets, 4 H1 tags, and zero semantic HTML. It's all divs all the way down.

### The Pattern

These aren't unusual. This is what local business websites look like everywhere. The scanner found measurable, specific problems in seconds per site. A human would need 15-20 minutes each to catch the same issues. Multiply that by a hundred prospects and you're talking days of work.

## How It Works

The scanner uses Hermes Agent's full agentic pipeline — not just a script:

**Discovery** — `web_search` finds businesses, `web_extract` pulls their info. The agent builds a candidate list.

**Visual Analysis** — `browser` opens each site, takes screenshots, and `browser_vision` assesses visual quality. It resizes the viewport to check mobile.

**Technical Scoring** — `execute_code` runs a Python engine analyzing 5 categories (mobile, design, SEO, accessibility, performance). Each scores 0-20. Total: 0-100 with letter grades.

**Report Generation** — `write_file` creates HTML pitch reports with score breakdowns, issue lists, and personalized pitch emails.

**Prioritization** — Worst scores rank highest. A bar with 58 blocking scripts is a better lead than a steakhouse with a viewport tag.

The key insight: a pure Python script can score websites. But an *agent* decides which targets to pursue, handles failures gracefully, adapts its approach, and generates contextual output. That's the difference.

## The Code

~1,500 lines across 5 scoring modules:

```
scorer/
├── mobile.py         # Viewport, media queries, fixed-width, touch targets
├── design.py         # Contrast, typography, CTAs, whitespace
├── seo.py            # Title, meta, headings, alt text
├── accessibility.py  # Semantic HTML, ARIA, form labels, links
├── performance.py    # Size, blocking, requests, image formats
└── aggregate.py      # Combines scores, assigns grades
```

The [Hermes skill](~/.hermes/skills/biz-web-scanner/SKILL.md) teaches the agent the full workflow. Once loaded:

> "Scan auto repair shops in Tupelo, MS and generate pitch reports"

...and Hermes handles discovery, scoring, screenshots, and pitch generation.

**GitHub:** [github.com/scastile/hermes-biz-scanner](https://github.com/scastile/hermes-biz-scanner)

## What Actually Surprised Me

**The problems are everywhere.** I didn't cherry-pick these businesses. I ran the scanner against the first results that loaded. Every single one had serious, fixable issues.

**Specificity sells.** "Your website has problems" gets ignored. "Your site loads 58 JavaScript files, has no meta description, and breaks on mobile" gets responses. The agent generates the specific version automatically.

**Local businesses are underserved.** Most can't tell good design from bad. They know their site "doesn't feel right" but can't articulate why. Show them 223 fixed-width elements and suddenly it makes sense.

**This is a real business.** Not a demo, not a toy. This is how I find clients. The scanner does the prospecting, I do the selling.

## Try It

```bash
git clone https://github.com/scastile/hermes-biz-scanner.git
cd hermes-biz-scanner
python main.py score https://example.com --name "Example" --city "City" --industry "Restaurant"
open output/Example-report.html
```

Or with Hermes Agent:

> "Scan 5 businesses in my area and rank them by website quality"

---

*Submission for the [Hermes Agent Challenge](https://dev.to/challenges/hermes-agent-2026-05-15). If you run a local business and want a free website audit, drop your URL in the comments.*
