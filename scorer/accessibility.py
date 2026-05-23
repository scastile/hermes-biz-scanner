"""Accessibility scoring module. 0-20 points."""
import re
from html.parser import HTMLParser


class A11yParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.semantic_tags = 0
        self.total_tags = 0
        self.aria_count = 0
        self.form_count = 0
        self.input_with_label = 0
        self.input_without_label = 0
        self.link_count = 0
        self.empty_links = 0
        self.in_label = False
        self.label_for = {}
        self.input_ids = set()
        self.labels = {}

    def handle_starttag(self, tag, attrs):
        self.total_tags += 1
        attrs_dict = dict(attrs)

        # Semantic HTML
        semantic = {'header', 'nav', 'main', 'article', 'section', 'aside', 'footer', 'figure', 'figcaption'}
        if tag in semantic:
            self.semantic_tags += 1

        # ARIA attributes
        for attr in attrs:
            if attr[0].startswith('aria-'):
                self.aria_count += 1

        # Forms
        if tag == 'form':
            self.form_count += 1
        if tag == 'label':
            self.in_label = True
            if 'for' in attrs_dict:
                self.label_for[attrs_dict['for']] = True
        if tag in ('input', 'textarea', 'select'):
            input_id = attrs_dict.get('id', '')
            if input_id:
                self.input_ids.add(input_id)
            if input_id and input_id in self.label_for:
                self.input_with_label += 1
            else:
                # Check for aria-label or aria-labelledby
                if attrs_dict.get('aria-label') or attrs_dict.get('aria-labelledby'):
                    self.input_with_label += 1
                else:
                    self.input_without_label += 1

        # Links
        if tag == 'a':
            self.link_count += 1
            href = attrs_dict.get('href', '')
            if not href or href == '#' or href == 'javascript:void(0)':
                self.empty_links += 1

    def handle_endtag(self, tag):
        if tag == 'label':
            self.in_label = False


def score_accessibility(html: str) -> dict:
    """Score accessibility. Returns {score, max, details}."""
    details = []
    score = 0
    max_score = 20

    parser = A11yParser()
    try:
        parser.feed(html)
    except Exception:
        pass

    # Semantic HTML (5 points)
    if parser.total_tags == 0:
        details.append("✗ No HTML to analyze (-5)")
    elif parser.semantic_tags >= 5:
        score += 5
        details.append(f"✓ {parser.semantic_tags} semantic elements — good HTML structure (+5)")
    elif parser.semantic_tags >= 2:
        score += 3
        details.append(f"~ {parser.semantic_tags} semantic elements — could use more (+3)")
    else:
        details.append(f"✗ Only {parser.semantic_tags} semantic elements — div soup (-5)")

    # ARIA attributes (5 points)
    if parser.aria_count >= 5:
        score += 5
        details.append(f"✓ {parser.aria_count} ARIA attributes — good accessibility markup (+5)")
    elif parser.aria_count >= 2:
        score += 3
        details.append(f"~ {parser.aria_count} ARIA attributes — minimal a11y markup (+3)")
    elif parser.aria_count == 0:
        details.append("✗ No ARIA attributes — screen reader unfriendly (-5)")
    else:
        score += 1
        details.append(f"~ Only {parser.aria_count} ARIA attributes (+1)")

    # Form labels (5 points)
    total_inputs = parser.input_with_label + parser.input_without_label
    if total_inputs == 0:
        score += 5
        details.append("✓ No form inputs to check (+5)")
    elif parser.input_without_label == 0:
        score += 5
        details.append(f"✓ All {total_inputs} form inputs have labels (+5)")
    elif parser.input_with_label >= total_inputs * 0.5:
        score += 3
        details.append(f"~ {parser.input_with_label}/{total_inputs} inputs labeled (+3)")
    else:
        details.append(f"✗ {parser.input_without_label}/{total_inputs} inputs missing labels — screen reader issue (-5)")

    # Link quality (5 points)
    if parser.link_count == 0:
        score += 3
        details.append("~ No links found — unusual for a business site (+3)")
    elif parser.empty_links == 0:
        score += 5
        details.append(f"✓ All {parser.link_count} links have valid hrefs (+5)")
    elif parser.empty_links <= 2:
        score += 3
        details.append(f"~ {parser.empty_links} empty/placeholder links (+3)")
    else:
        details.append(f"✗ {parser.empty_links} empty links — poor navigation (-5)")

    return {"score": score, "max": max_score, "details": details}
