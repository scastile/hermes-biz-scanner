"""Mobile responsiveness scoring module. 0-20 points."""
import re
from html.parser import HTMLParser


class ViewportParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.has_viewport = False
        self.media_queries = 0
        self.inline_styles = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'meta' and attrs_dict.get('name') == 'viewport':
            self.has_viewport = True


def score_mobile(html: str, css: str = "", headers: dict = None) -> dict:
    """Score mobile responsiveness. Returns {score, max, details}."""
    details = []
    score = 0
    max_score = 20

    parser = ViewportParser()
    try:
        parser.feed(html)
    except Exception:
        pass

    # Viewport meta tag (5 points)
    if parser.has_viewport:
        score += 5
        details.append("✓ Viewport meta tag present (+5)")
    else:
        details.append("✗ No viewport meta tag — site won't scale on mobile (-5)")

    # Media queries in CSS (5 points)
    if css:
        mq_count = len(re.findall(r'@media', css))
        if mq_count >= 3:
            score += 5
            details.append(f"✓ {mq_count} media queries found (+5)")
        elif mq_count >= 1:
            score += 3
            details.append(f"~ Only {mq_count} media queries — minimal responsive CSS (+3)")
        else:
            details.append("✗ No media queries — no responsive CSS rules (-5)")
    else:
        details.append("✗ No CSS available to check media queries (-5)")

    # Fixed-width elements (5 points deduction check)
    fixed_width = re.findall(r'width:\s*(\d{3,})px', css or '')
    if not fixed_width:
        score += 5
        details.append("✓ No fixed-width elements detected (+5)")
    elif len(fixed_width) <= 3:
        score += 2
        details.append(f"~ {len(fixed_width)} fixed-width elements found (+2)")
    else:
        details.append(f"✗ {len(fixed_width)} fixed-width elements — likely overflows on mobile (-5)")

    # Touch-friendly tap targets (5 points)
    small_taps = re.findall(r'(?:width|height):\s*(\d{1,2})px', css or '')
    small_count = sum(1 for s in small_taps if int(s) < 44)
    if small_count == 0:
        score += 5
        details.append("✓ Touch targets appear adequately sized (+5)")
    elif small_count <= 5:
        score += 2
        details.append(f"~ {small_count} potentially small touch targets (+2)")
    else:
        details.append(f"✗ {small_count} small touch targets — hard to tap on mobile (-5)")

    return {"score": score, "max": max_score, "details": details}
