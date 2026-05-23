---
name: biz-web-scanner
description: "Scan and score local business websites for design quality, SEO, accessibility, performance, and mobile responsiveness. Generates pitch reports and email drafts. Uses parallel subagents for concurrent scoring. Use when the user wants to analyze business websites, find poor-performing local business sites, generate pitch reports, or score URLs."
metadata:
  hermes:
    tags: [scanner, prospecting, web-design, local-business, scoring, multi-agent]
    related-skills: [polymarket-weather-bot]
---

# Biz Web Scanner Skill

Scan local business websites, score their quality, and generate pitch reports. Uses **parallel subagents** via `delegate_task` to score multiple businesses concurrently.

## When to Use

- User wants to score one or more business websites
- User wants to find local businesses with bad websites (prospecting)
- User wants to generate pitch reports
- User says "scan", "score", "pitch report", "business website", "prospect"
- User wants to scan multiple businesses at once (triggers parallel mode)

## Scoring Engine

Installed at `/opt/hermes-biz-scanner/`. 5 categories, 0-100 scale:

| Category | Max | Criteria |
|----------|-----|----------|
| Mobile Responsiveness | 20 | Viewport, media queries, fixed-width, touch targets |
| Design Quality | 20 | Contrast, typography, CTAs, whitespace |
| SEO | 20 | Title, meta description, heading hierarchy, alt text |
| Accessibility | 20 | Semantic HTML, ARIA, form labels, link quality |
| Performance | 20 | Page size, render-blocking, requests, image formats |

Grades: A (90+), B (75-89), C (60-74), D (40-59), F (<40)

## Single Business Workflow

For scoring a single URL directly:

1. `web_extract` the HTML
2. `browser` for screenshots
3. `execute_code` to run the scoring engine
4. `write_file` to generate report + pitch email

```python
import sys; sys.path.insert(0, '/opt/hermes-biz-scanner')
from scorer.aggregate import score_website
result = score_website(html, css, page_size_kb)
# result = {total_score, total_max, percentage, grade, emoji, categories, prospect_priority}
```

## Parallel Multi-Agent Workflow (Multiple Businesses)

**This is the recommended approach for 2+ businesses.** Instead of scoring sequentially, spawn N concurrent subagents:

### Step 1: Discovery (Main Agent)
Use `web_search` to find businesses:
```
"Find [count] [industry] in [city] with websites"
```

### Step 2: Spawn Parallel Subagents (Main Agent)
Use `delegate_task` to spawn one subagent per business. Each subagent gets:

**Goal:** Score one business website and generate a pitch report.

**Context provided to each subagent:**
- Business name, URL, city, industry
- Instructions to: fetch HTML, run scoring engine, generate report, save outputs
- Output path: `/opt/hermes-biz-scanner/output/`

**Constraints:** Each subagent only uses: `web_extract`, `browser`, `execute_code`, `write_file`

### Step 3: Collect Results (Main Agent)
When all subagents complete, collect their results:
- Read `*-data.json` files from output directory
- Rank by score (worst first = best prospects)
- Generate prospect list with `generate_prospect_list()`

### Example Prompt for Main Agent

> Scan 4 restaurants in Tupelo, MS. Use parallel subagents to score each one concurrently. Generate a prospect list ranked by worst score.

The main agent should:
1. Discover 4 restaurants via web_search
2. Spawn 4 subagents via delegate_task (one per restaurant)
3. Wait for all subagents to complete
4. Aggregate results into a prospect list

## Output Artifacts

Per business:
- `{name}-report.html` — Visual pitch report
- `{name}-pitch.txt` — Pitch email draft
- `{name}-data.json` — Raw scoring data

Batch scan:
- `prospect-list.md` — Ranked table of all businesses

## Priority Grades

- **HIGH** (D/F): Best prospects — desperate need for redesign
- **MEDIUM** (C): Decent but significant room for improvement
- **LOW** (A/B): Already decent, harder sell

## Tips

- Parallel scanning is ~3-4x faster than sequential for 4+ businesses
- Each subagent has isolated context — one failure doesn't affect others
- For best results, limit to 4-6 concurrent subagents (API rate limits)
- Cross-reference web_search results for business info (phone, reviews)
- Tailor pitch emails based on specific issues found
