"""Design quality scoring module. 0-20 points."""
import re
from html.parser import HTMLParser


def score_design(html: str, css: str = "", screenshot_path: str = None) -> dict:
    """Score design quality. Returns {score, max, details}."""
    details = []
    score = 0
    max_score = 20

    # Color contrast — check for inline style color/bgcolor combos (5 points)
    color_pairs = re.findall(
        r'color:\s*(#[0-9a-fA-F]{3,6}|rgb[a]?\([^)]+\))[^}]*background(?:-color)?:\s*(#[0-9a-fA-F]{3,6}|rgb[a]?\([^)]+\))',
        css or ''
    )
    # Also check the reverse order
    bg_color_pairs = re.findall(
        r'background(?:-color)?:\s*(#[0-9a-fA-F]{3,6}|rgb[a]?\([^)]+\))[^}]*color:\s*(#[0-9a-fA-F]{3,6}|rgb[a]?\([^)]+\))',
        css or ''
    )
    total_pairs = len(color_pairs) + len(bg_color_pairs)

    # Check for very low-contrast combos (light gray on white, etc.)
    low_contrast = 0
    light_colors = {'#fff', '#ffffff', '#f5f5f5', '#fafafa', '#eee', '#eeeeee', '#ddd', '#dddddd'}
    for pair in color_pairs + bg_color_pairs:
        if isinstance(pair, tuple):
            c1, c2 = pair[0].lower(), pair[1].lower()
        else:
            continue
        if c1 in light_colors and c2 in light_colors:
            low_contrast += 1

    if total_pairs > 0 and low_contrast == 0:
        score += 5
        details.append("✓ Color contrast appears adequate (+5)")
    elif low_contrast <= 2:
        score += 3
        details.append(f"~ {low_contrast} potential low-contrast color pairs (+3)")
    else:
        details.append(f"✗ {low_contrast} low-contrast color pairs — readability issues (-5)")

    # Typography consistency (5 points)
    font_families = re.findall(r'font-family:\s*([^;]+)', css or '')
    unique_fonts = set(f.strip().strip("'\"") for f in font_families if f.strip())
    if len(unique_fonts) <= 3 and len(unique_fonts) >= 1:
        score += 5
        details.append(f"✓ {len(unique_fonts)} font families — consistent typography (+5)")
    elif len(unique_fonts) <= 5:
        score += 3
        details.append(f"~ {len(unique_fonts)} font families — somewhat inconsistent (+3)")
    elif len(unique_fonts) > 5:
        details.append(f"✗ {len(unique_fonts)} font families — typographic chaos (-5)")
    else:
        details.append("✗ No font-family declarations found (-5)")

    # CTA visibility (5 points) — look for buttons, prominent links
    cta_patterns = [
        r'class="[^"]*(?:btn|button|cta|action|primary|submit)[^"]*"',
        r'<button[\s>]',
        r'class="[^"]*(?:book|schedule|contact|call|order|buy|sign)[^"]*"',
    ]
    cta_count = sum(len(re.findall(p, html, re.I)) for p in cta_patterns)
    if cta_count >= 3:
        score += 5
        details.append(f"✓ {cta_count} CTAs detected — good call-to-action presence (+5)")
    elif cta_count >= 1:
        score += 3
        details.append(f"~ Only {cta_count} CTAs — could be more prominent (+3)")
    else:
        details.append("✗ No clear CTAs found — visitors won't know what to do (-5)")

    # Whitespace and layout (5 points) — check for padding/margin usage
    padding_count = len(re.findall(r'padding:', css or ''))
    margin_count = len(re.findall(r'margin:', css or ''))
    total_spacing = padding_count + margin_count
    if total_spacing >= 20:
        score += 5
        details.append(f"✓ {total_spacing} spacing declarations — good whitespace (+5)")
    elif total_spacing >= 10:
        score += 3
        details.append(f"~ {total_spacing} spacing declarations — adequate whitespace (+3)")
    elif total_spacing >= 5:
        score += 1
        details.append(f"~ Only {total_spacing} spacing declarations — cramped layout (+1)")
    else:
        details.append("✗ Minimal spacing — layout feels cramped and unprofessional (-5)")

    return {"score": score, "max": max_score, "details": details}
