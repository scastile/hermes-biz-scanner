"""Templates for report generation."""

PROSPECT_LIST_TEMPLATE = """# 🎯 Local Business Web Prospect List

**Generated:** {date}  
**Total Prospects:** {count}  
**Ranked by:** Worst score first (best prospects at top)

| # | Business | URL | Location | Score | Grade | Priority |
|---|----------|-----|----------|-------|-------|----------|
{rows}

---

### Priority Legend
- 🔴 **HIGH** — Grade D or F. These businesses desperately need a redesign. Lead with these.
- 🟟 **MEDIUM** — Grade C. Decent but significant room for improvement.
- 🟢 **LOW** — Grade A or B. Already decent. Harder sell but could be upsold on specific improvements.

### Next Steps
1. Start with HIGH priority prospects
2. Generate individual pitch reports for top 5
3. Customize pitch emails with specific issues
4. Send and track responses
"""
