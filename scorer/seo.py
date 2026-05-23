"""SEO basics scoring module. 0-20 points."""
import re
from html.parser import HTMLParser


class SEOParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.meta_description = ""
        self.h1_count = 0
        self.h2_count = 0
        self.h3_count = 0
        self.img_count = 0
        self.img_with_alt = 0
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'title':
            self.in_title = True
        elif tag == 'h1':
            self.h1_count += 1
        elif tag == 'h2':
            self.h2_count += 1
        elif tag == 'h3':
            self.h3_count += 1
        elif tag == 'img':
            self.img_count += 1
            if attrs_dict.get('alt', '').strip():
                self.img_with_alt += 1
        elif tag == 'meta':
            if attrs_dict.get('name', '').lower() == 'description':
                self.meta_description = attrs_dict.get('content', '')

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


def score_seo(html: str) -> dict:
    """Score SEO basics. Returns {score, max, details}."""
    details = []
    score = 0
    max_score = 20

    parser = SEOParser()
    try:
        parser.feed(html)
    except Exception:
        pass

    # Title tag (5 points)
    title_len = len(parser.title.strip())
    if 30 <= title_len <= 60:
        score += 5
        details.append(f"✓ Title tag optimal length ({title_len} chars): \"{parser.title.strip()[:50]}\" (+5)")
    elif 10 <= title_len < 30 or 60 < title_len <= 80:
        score += 3
        details.append(f"~ Title tag acceptable ({title_len} chars): \"{parser.title.strip()[:50]}\" (+3)")
    elif title_len > 0:
        score += 1
        details.append(f"~ Title tag poor length ({title_len} chars) (+1)")
    else:
        details.append("✗ No title tag — critical SEO issue (-5)")

    # Meta description (5 points)
    desc_len = len(parser.meta_description.strip())
    if 120 <= desc_len <= 160:
        score += 5
        details.append(f"✓ Meta description optimal ({desc_len} chars) (+5)")
    elif 50 <= desc_len < 120 or 160 < desc_len <= 200:
        score += 3
        details.append(f"~ Meta description acceptable ({desc_len} chars) (+3)")
    elif desc_len > 0:
        score += 1
        details.append(f"~ Meta description too short/long ({desc_len} chars) (+1)")
    else:
        details.append("✗ No meta description — missing search snippet (-5)")

    # Heading hierarchy (5 points)
    if parser.h1_count == 1:
        score += 5
        details.append(f"✓ Exactly 1 H1 tag — proper hierarchy (+5)")
    elif parser.h1_count == 0:
        score += 1
        details.append("✗ No H1 tag — missing main heading (-4)")
    else:
        score += 2
        details.append(f"~ {parser.h1_count} H1 tags — should only have one (+2)")

    # Bonus for having h2s
    if parser.h2_count >= 2:
        score = min(score + 0, max_score)  # Already counted above
    elif parser.h2_count == 0 and parser.h1_count > 0:
        details.append("  Note: No H2 subheadings — flat content structure")

    # Image alt text (5 points)
    if parser.img_count == 0:
        score += 5
        details.append("✓ No images to check (+5)")
    elif parser.img_with_alt == parser.img_count:
        score += 5
        details.append(f"✓ All {parser.img_count} images have alt text (+5)")
    elif parser.img_with_alt >= parser.img_count * 0.5:
        score += 3
        details.append(f"~ {parser.img_with_alt}/{parser.img_count} images have alt text (+3)")
    else:
        details.append(f"✗ Only {parser.img_with_alt}/{parser.img_count} images have alt text — accessibility + SEO issue (-5)")

    return {"score": score, "max": max_score, "details": details}
