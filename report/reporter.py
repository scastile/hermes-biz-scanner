"""Report generator. Assembles scoring results into markdown and HTML reports."""
import os
from datetime import datetime


def _load_template(filename):
    """Load a template file from the templates directory."""
    template_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'report', 'templates')
    with open(os.path.join(template_dir, filename), 'r') as f:
        return f.read()


def generate_prospect_list(prospects: list) -> str:
    """Generate a ranked prospect list from multiple scoring results.
    
    prospects: list of {name, url, city, industry, score_result}
    Returns: markdown string
    """
    sorted_prospects = sorted(prospects, key=lambda p: p['score_result']['percentage'])

    rows = []
    for i, p in enumerate(sorted_prospects, 1):
        sr = p['score_result']
        priority = sr['prospect_priority']
        emoji = sr['emoji']
        rows.append(
            f"| {i} | {p['name']} | [{p['url']}]({p['url']}) | "
            f"{p['city']} | {sr['total_score']}/{sr['total_max']} ({sr['percentage']}%) | "
            f"{emoji} {sr['grade']} | {priority} |"
        )

    template = _load_template('prospect_list.md')
    return template.format(
        date=datetime.now().strftime('%Y-%m-%d %H:%M'),
        count=len(prospects),
        rows='\n'.join(rows),
    )


def generate_pitch_report(business_name: str, url: str, city: str, industry: str,
                          score_result: dict, screenshot_paths: dict = None) -> str:
    """Generate a detailed pitch report for a single business.
    
    Returns: HTML string
    """
    sr = score_result
    cats = sr['categories']

    # Build category breakdown
    cat_rows = []
    for cat_name, cat_data in cats.items():
        pct = (cat_data['score'] / cat_data['max']) * 100
        bar_width = int(pct)
        color = '#15be53' if pct >= 75 else '#f59e0b' if pct >= 50 else '#ef4444'
        details = '<br>'.join(cat_data['details'])
        cat_rows.append(f"""
        <tr>
          <td><strong>{cat_name}</strong></td>
          <td>{cat_data['score']}/{cat_data['max']}</td>
          <td>
            <div style="background:#e5e7eb;border-radius:4px;height:20px;width:100%;">
              <div style="background:{color};border-radius:4px;height:20px;width:{bar_width}%;"></div>
            </div>
            <small>{pct:.0f}%</small>
          </td>
          <td style="font-size:0.85em;">{details}</td>
        </tr>""")

    # Build issues list
    all_issues = []
    for cat_name, cat_data in cats.items():
        for detail in cat_data['details']:
            if detail.startswith('✗'):
                all_issues.append(f"<li><strong>{cat_name}:</strong> {detail[2:]}</li>")

    # Build strengths list
    all_strengths = []
    for cat_name, cat_data in cats.items():
        for detail in cat_data['details']:
            if detail.startswith('✓'):
                all_strengths.append(f"<li><strong>{cat_name}:</strong> {detail[2:]}</li>")

    # Screenshots
    screenshots_html = ""
    if screenshot_paths:
        for label, path in screenshot_paths.items():
            screenshots_html += f'<div style="margin:10px 0;"><strong>{label}</strong><br><img src="{path}" style="max-width:100%;border:1px solid #ddd;border-radius:8px;"></div>'

    template = _load_template('pitch_report.html')
    # Use string replacement instead of .format() to avoid CSS brace conflicts
    priority_lower = sr['prospect_priority'].lower()
    replacements = {
        '{business_name}': business_name,
        '{url}': url,
        '{city}': city,
        '{industry}': industry,
        '{date}': datetime.now().strftime('%Y-%m-%d %H:%M'),
        '{emoji}': sr['emoji'],
        '{grade}': sr['grade'],
        '{score}': str(sr['total_score']),
        '{max_score}': str(sr['total_max']),
        '{percentage}': str(sr['percentage']),
        '{priority}': sr['prospect_priority'],
        '{priority.lower()}': f'priority-{priority_lower}',
        '{category_rows}': '\n'.join(cat_rows),
        '{issues}': '\n'.join(all_issues) if all_issues else '<li>No critical issues found</li>',
        '{strengths}': '\n'.join(all_strengths) if all_strengths else '<li>No notable strengths</li>',
        '{screenshots}': screenshots_html,
    }
    result = template
    for key, val in replacements.items():
        result = result.replace(key, val)
    return result
