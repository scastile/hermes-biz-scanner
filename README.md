# Hermes Local Business Web Scanner

An autonomous web quality scanner built on [Hermes Agent](https://hermes-agent.nousresearch.com/) that finds local businesses with bad websites, scores them, and generates pitch reports.

## Why

I run a small web design agency. Prospecting used to mean manually visiting hundreds of local business websites, screenshotting the ugly ones, and writing pitch emails. Now my AI agent does it in minutes.

## What It Does

1. **Discovers** local businesses in any city/industry
2. **Scores** websites across 5 categories (mobile, design, SEO, accessibility, performance)
3. **Ranks** by worst score first (best prospects at top)
4. **Generates** visual pitch reports with specific issues
5. **Writes** personalized pitch email drafts

## Quick Start

```bash
# Score a single website
python main.py score https://example.com --name "Example" --city "City" --industry "Industry"

# Output
open output/Example-report.html   # Visual pitch report
open output/Example-pitch.txt     # Pitch email draft
```

## Scoring Categories

| Category | Max | What It Checks |
|----------|-----|----------------|
| Mobile Responsiveness | 20 | Viewport, media queries, fixed-width, touch targets |
| Design Quality | 20 | Contrast, typography, CTAs, whitespace |
| SEO | 20 | Title, meta description, headings, alt text |
| Accessibility | 20 | Semantic HTML, ARIA, form labels, links |
| Performance | 20 | Page size, blocking resources, requests, image formats |

## Grade Scale

| Grade | % | Priority |
|-------|---|----------|
| A | 90-100 | LOW |
| B | 75-89 | LOW |
| C | 60-74 | MEDIUM |
| D | 40-59 | HIGH |
| F | 0-39 | HIGH |

## With Hermes Agent

Load the skill and say:

> "Scan dentists in Corinth, MS and generate pitch reports"

The agent handles discovery, scoring, and report generation autonomously.

## License

MIT
