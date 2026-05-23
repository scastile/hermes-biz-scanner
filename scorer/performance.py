"""Performance signals scoring module. 0-20 points."""
import re
from html.parser import HTMLParser


class PerfParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.script_count = 0
        self.css_count = 0
        self.image_count = 0
        self.iframe_count = 0
        self.inline_style_count = 0
        self.total_tags = 0
        self.lazy_images = 0
        self.modern_images = 0  # webp, avif

    def handle_starttag(self, tag, attrs):
        self.total_tags += 1
        attrs_dict = dict(attrs)

        if tag == 'script':
            src = attrs_dict.get('src', '')
            if src:
                self.script_count += 1
            if attrs_dict.get('src', '').endswith('.js'):
                self.script_count += 1
        elif tag == 'link':
            if attrs_dict.get('rel') == 'stylesheet':
                self.css_count += 1
        elif tag == 'img':
            self.image_count += 1
            src = attrs_dict.get('src', '')
            if src.endswith('.webp') or src.endswith('.avif'):
                self.modern_images += 1
            if attrs_dict.get('loading') == 'lazy':
                self.lazy_images += 1
        elif tag == 'iframe':
            self.iframe_count += 1
        elif tag == 'style':
            self.inline_style_count += 1


def score_performance(html: str, page_size_kb: float = 0, load_time_ms: float = 0) -> dict:
    """Score performance signals. Returns {score, max, details}."""
    details = []
    score = 0
    max_score = 20

    parser = PerfParser()
    try:
        parser.feed(html)
    except Exception:
        pass

    # Page size (5 points)
    if page_size_kb > 0:
        if page_size_kb < 1000:
            score += 5
            details.append(f"✓ Page size {page_size_kb:.0f}KB — fast loading (+5)")
        elif page_size_kb < 3000:
            score += 3
            details.append(f"~ Page size {page_size_kb:.0f}KB — acceptable (+3)")
        else:
            details.append(f"✗ Page size {page_size_kb:.0f}KB — too heavy, slow loading (-5)")
    else:
        # Estimate from HTML length
        html_kb = len(html.encode()) / 1024
        if html_kb < 200:
            score += 5
            details.append(f"✓ HTML size {html_kb:.0f}KB — lightweight (+5)")
        elif html_kb < 500:
            score += 3
            details.append(f"~ HTML size {html_kb:.0f}KB — moderate (+3)")
        else:
            details.append(f"✗ HTML size {html_kb:.0f}KB — heavy (-5)")

    # Render-blocking resources (5 points)
    blocking = parser.script_count + parser.css_count
    if blocking <= 5:
        score += 5
        details.append(f"✓ {parser.script_count} scripts, {parser.css_count} stylesheets — minimal blocking (+5)")
    elif blocking <= 10:
        score += 3
        details.append(f"~ {parser.script_count} scripts, {parser.css_count} stylesheets — moderate (+3)")
    else:
        details.append(f"✗ {parser.script_count} scripts, {parser.css_count} stylesheets — too many blocking resources (-5)")

    # HTTP requests estimate (5 points)
    total_requests = parser.script_count + parser.css_count + parser.image_count + parser.iframe_count
    if total_requests <= 20:
        score += 5
        details.append(f"✓ ~{total_requests} estimated requests — efficient (+5)")
    elif total_requests <= 40:
        score += 3
        details.append(f"~ ~{total_requests} estimated requests — acceptable (+3)")
    else:
        details.append(f"✗ ~{total_requests} estimated requests — too many (-5)")

    # Modern image formats (5 points)
    if parser.image_count == 0:
        score += 3
        details.append("~ No images found (+3)")
    elif parser.modern_images == parser.image_count and parser.image_count > 0:
        score += 5
        details.append(f"✓ All {parser.image_count} images use modern formats (WebP/AVIF) (+5)")
    elif parser.modern_images > 0:
        score += 3
        details.append(f"~ {parser.modern_images}/{parser.image_count} images use modern formats (+3)")
    else:
        details.append(f"✗ No modern image formats — all JPEG/PNG (-5)")

    return {"score": score, "max": max_score, "details": details}
