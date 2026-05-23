---
title: "I Built an AI That Finds Bad Local Business Websites (And Pitches Them Redesigns)"
published: false
description: "How I used Hermes Agent to build an autonomous web quality scanner that prospects, scores, and generates pitch reports for local businesses — replacing hours of manual work with a single command."
tags: hermesagentchallenge, devchallenge, agents, python, webdev
---

# I Built an AI That Finds Bad Local Business Websites (And Pitches Them Redesigns)

I run a small web design agency. Finding clients used to mean manually visiting hundreds of local business websites, screenshotting the ugly ones, writing up reports, and crafting personalized pitch emails. It sucked.

Then I taught my AI agent to do it.

## What I Built

**Hermes Local Business Web Scanner** — an autonomous tool built on [Hermes Agent](https://hermes-agent.nousresearch.com/) that:

1. **Discovers** local businesses in any city/industry
2. **Scores** their websites across 5 categories (mobile, design, SEO, accessibility, performance)
3. **Ranks** them by worst score first (best prospects at the top)
4. **Generates** visual pitch reports with specific issues highlighted
5. **Writes** personalized pitch email drafts ready to send

The whole pipeline runs autonomously. Give it a city and industry, and it comes back with a prioritized prospect list and everything you need to start selling.

## Demo: Tupelo, MS

I ran it against local businesses across different industries in Tupelo, MS. Here's what it found:

### 🔴 Blue Canoe — Grade: D (57%)

Tupelo's beloved dive bar with live music and 100+ beers. Great vibe, rough website.

**Issues found:**
- 8 fixed-width elements breaking mobile layout
- 8 touch targets too small to tap on phones
- No meta description — invisible in search results
- No H1 tag — no clear page heading
- 58 scripts and 66 total requests killing performance
- Zero modern image formats (all JPEG/PNG)

### 🔴 Tom's Automotive — Grade: D (59%)

Family-owned auto repair shop. Clean 49KB site, but no clear calls-to-action — visitors won't know what to do.

**Issues found:**
- 10 fixed-width elements breaking mobile
- 13 touch targets too small for mobile
- No clear CTAs — no "Book Now", no "Get a Quote" buttons
- Only 1 of 6 images has alt text
- 11 scripts and 5 stylesheets blocking render

### 🔴 Auto Spa of Tupelo — Grade: D (58%)

Auto body and painting shop. Massive 984KB page with 25 font families — typographic chaos.

**Issues found:**
- 223 fixed-width elements — mobile is completely broken
- 168 touch targets too small to tap
- 25 font families — no consistent visual identity
- 22 scripts, no external stylesheets (all inline)
- Only 13 of 22 images have alt text

### 🟠 Woody's Tupelo Steakhouse — Grade: C (61%)

A Tupelo institution for 30 years. Charcoal-grilled steaks, southern hospitality, and a website that's seen better days.

**Issues found:**
- 122 fixed-width elements — mobile is a disaster
- 110 touch targets too small for mobile
- 8 font families — typographic chaos
- 4 H1 tags when there should be only one
- Only 2 of 12 images have alt text
- Zero semantic HTML elements — it's all divs

### The Pattern

Every single one of these businesses has real problems that cost them customers. The scanner found them in seconds. A human would need 15-20 minutes per site to catch the same issues.

## How It Works: The Hermes Agentic Pipeline

This is where it gets interesting. The scanner doesn't just run a script — it uses Hermes Agent's full agentic capabilities:

### Step 1: Discovery (`web_search` + `web_extract`)

```
"Find auto repair shops in Tupelo, MS with websites"
```

Hermes searches, extracts business names, URLs, phone numbers, and reviews. It builds a candidate list automatically.

### Step 2: Visual Analysis (`browser` + `browser_vision`)

For each candidate, Hermes:
- Opens the site in a headless browser
- Takes full-page screenshots
- Uses vision AI to assess visual design quality
- Checks for mobile responsiveness by resizing the viewport

### Step 3: Technical Scoring (`execute_code`)

Hermes runs a Python scoring engine that analyzes:
- **Mobile**: Viewport meta, media queries, fixed-width elements, touch target sizes
- **Design**: Color contrast, font consistency, CTA presence, whitespace
- **SEO**: Title tags, meta descriptions, heading hierarchy, image alt text
- **Accessibility**: Semantic HTML, ARIA attributes, form labels, link quality
- **Performance**: Page size, render-blocking resources, HTTP requests, image formats

Each category scores 0-20. Total: 0-100 with letter grades.

### Step 4: Report Generation (`write_file`)

For each business, Hermes generates:
- **HTML pitch report** — Visual score breakdown with progress bars, issue lists, and redesign recommendations
- **Pitch email draft** — Personalized to the specific issues found
- **JSON data** — Raw scores for further processing

### Step 5: Prioritization

Prospects are ranked worst-first. A bar scoring 57% (Grade D) with 58 blocking scripts and no meta description is a better lead than a steakhouse scoring 61% (Grade C) who at least has a viewport tag.

## The Code

The scoring engine is ~1,500 lines of Python across 5 modules:

```
scorer/
├── mobile.py         # Viewport, media queries, fixed-width, touch targets
├── design.py         # Contrast, typography, CTAs, whitespace
├── seo.py            # Title, meta, headings, alt text
├── accessibility.py  # Semantic HTML, ARIA, form labels, links
├── performance.py    # Size, blocking, requests, image formats
└── aggregate.py      # Combines all scores, assigns grades
```

The Hermes skill (`~/.hermes/skills/biz-web-scanner/SKILL.md`) teaches the agent the full workflow — from discovery to pitch. Once loaded, you just say:

> "Scan auto repair shops in Tupelo, MS and generate pitch reports"

...and Hermes handles the rest.

**GitHub repo:** [github.com/scastile/hermes-biz-scanner](https://github.com/scastile/hermes-biz-scanner)

## What I Learned

**1. Agentic > Scripted**

A pure Python script can score websites. But an *agent* can decide which businesses to target, handle failures gracefully (SSL errors, timeouts, redirects), adapt its approach based on what it finds, and generate contextual output. The difference is night and day.

**2. Skills are force multipliers**

By encoding the workflow as a Hermes skill, I can reuse it across sessions without re-explaining. The agent remembers the scoring criteria, the report format, the pitch template. Next time I say "scan restaurants in Memphis," it just works.

**3. The boring stuff is what wins**

Every other submission is building RAG pipelines and chat interfaces. I built a tool that finds bad websites and sells redesigns. It's not sexy, but it's *useful* — and it puts food on the table.

**4. Local business prospecting is a goldmine**

There are millions of small businesses with terrible websites. Most can't tell good design from bad. If you can show them specific, measurable problems (223 fixed-width elements! 25 font families! 58 blocking scripts!), they get it immediately.

## Try It Yourself

```bash
# Clone the repo
git clone https://github.com/scastile/hermes-biz-scanner.git
cd hermes-biz-scanner

# Score a single website
python main.py score https://example.com --name "Example Business" --city "Your City" --industry "Restaurant"

# Check the output
open output/Example_Business-report.html
```

Or if you have Hermes Agent installed, just load the skill and say:

> "Scan 5 businesses in my area and rank them by website quality"

The agent will discover, score, and generate pitch reports automatically.

---

*This is a submission for the [Hermes Agent Challenge](https://dev.to/challenges/hermes-agent-2026-05-15). If you found this useful, I'd appreciate a reaction — and if you know a business with a terrible website, send them my way.*
