"""Aggregate scoring module. Combines all category scores into final grade."""
from .mobile import score_mobile
from .design import score_design
from .seo import score_seo
from .accessibility import score_accessibility
from .performance import score_performance


def get_grade(score: int, max_score: int) -> str:
    pct = (score / max_score) * 100 if max_score > 0 else 0
    if pct >= 90:
        return 'A'
    elif pct >= 75:
        return 'B'
    elif pct >= 60:
        return 'C'
    elif pct >= 40:
        return 'D'
    else:
        return 'F'


def get_grade_emoji(grade: str) -> str:
    return {'A': '🟢', 'B': '🟡', 'C': '🟠', 'D': '🔴', 'F': '💀'}.get(grade, '❓')


def score_website(html: str, css: str = "", page_size_kb: float = 0, screenshot_path: str = None) -> dict:
    """Run all scoring modules and return aggregate results."""
    mobile = score_mobile(html, css)
    design = score_design(html, css, screenshot_path)
    seo = score_seo(html)
    a11y = score_accessibility(html)
    perf = score_performance(html, page_size_kb)

    categories = {
        'Mobile Responsiveness': mobile,
        'Design Quality': design,
        'SEO': seo,
        'Accessibility': a11y,
        'Performance': perf,
    }

    total_score = sum(c['score'] for c in categories.values())
    total_max = sum(c['max'] for c in categories.values())
    grade = get_grade(total_score, total_max)
    emoji = get_grade_emoji(grade)

    return {
        'total_score': total_score,
        'total_max': total_max,
        'percentage': round((total_score / total_max) * 100, 1) if total_max > 0 else 0,
        'grade': grade,
        'emoji': emoji,
        'categories': categories,
        'prospect_priority': 'HIGH' if grade in ('D', 'F') else 'MEDIUM' if grade == 'C' else 'LOW',
    }
