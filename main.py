#!/usr/bin/env python3
"""Hermes Local Business Web Scanner — CLI entry point.

Scores local business websites for design quality, SEO, accessibility,
performance, and mobile responsiveness. Generates pitch reports.

Usage:
    python main.py score <url> [--city CITY] [--industry INDUSTRY] [--name NAME]
    python main.py batch <city> <industry> [--count 5]
    python main.py demo
"""
import argparse
import json
import os
import sys
import time
from datetime import datetime
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scorer.aggregate import score_website
from pitch.generator import generate_pitch
from report.reporter import generate_prospect_list, generate_pitch_report


def fetch_url(url: str, timeout: int = 15) -> tuple:
    """Fetch URL, return (html, headers, page_size_kb)."""
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    req = Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    try:
        resp = urlopen(req, timeout=timeout)
        html = resp.read().decode('utf-8', errors='replace')
        headers = dict(resp.headers)
        size_kb = len(html.encode()) / 1024
        return html, headers, size_kb
    except (URLError, HTTPError, OSError) as e:
        print(f"  ⚠ Failed to fetch {url}: {e}")
        return "", {}, 0


def extract_css(html: str) -> str:
    """Extract inline and linked CSS from HTML."""
    import re
    css_parts = []

    # Inline styles
    inline = re.findall(r'<style[^>]*>(.*?)</style>', html, re.DOTALL)
    css_parts.extend(inline)

    # Inline style attributes
    style_attrs = re.findall(r'style="([^"]+)"', html)
    css_parts.extend(style_attrs)

    return '\n'.join(css_parts)


def score_single(url: str, name: str = "", city: str = "", industry: str = "",
                 output_dir: str = "output") -> dict:
    """Score a single website and generate reports."""
    print(f"\n{'='*60}")
    print(f"🔍 Scoring: {name or url}")
    print(f"{'='*60}")

    html, headers, size_kb = fetch_url(url)
    if not html:
        return None

    css = extract_css(html)

    print(f"  📄 Page size: {size_kb:.0f}KB")
    print(f"  🎨 CSS rules extracted: {len(css)} chars")

    result = score_website(html, css, size_kb)

    # Print results
    sr = result
    print(f"\n  {sr['emoji']} Grade: {sr['grade']} ({sr['total_score']}/{sr['total_max']}, {sr['percentage']}%)")
    print(f"  🎯 Prospect Priority: {sr['prospect_priority']}")
    print()

    for cat_name, cat_data in sr['categories'].items():
        pct = (cat_data['score'] / cat_data['max']) * 100
        emoji = '✅' if pct >= 75 else '⚠️' if pct >= 50 else '❌'
        print(f"  {emoji} {cat_name}: {cat_data['score']}/{cat_data['max']} ({pct:.0f}%)")
        for detail in cat_data['details']:
            print(f"      {detail}")
        print()

    # Generate reports
    os.makedirs(output_dir, exist_ok=True)
    safe_name = (name or url).replace(' ', '_').replace('/', '_')

    # Pitch report (HTML)
    report_html = generate_pitch_report(
        business_name=name or url,
        url=url,
        city=city or "Unknown",
        industry=industry or "Business",
        score_result=result,
    )
    report_path = os.path.join(output_dir, f"{safe_name}-report.html")
    with open(report_path, 'w') as f:
        f.write(report_html)
    print(f"  📊 Report saved: {report_path}")

    # Pitch email
    pitch = generate_pitch(
        business_name=name or url,
        url=url,
        city=city or "your city",
        industry=industry or "business",
        score_result=result,
    )
    pitch_path = os.path.join(output_dir, f"{safe_name}-pitch.txt")
    with open(pitch_path, 'w') as f:
        f.write(pitch)
    print(f"  📧 Pitch saved: {pitch_path}")

    # JSON data
    json_path = os.path.join(output_dir, f"{safe_name}-data.json")
    with open(json_path, 'w') as f:
        json.dump(result, f, indent=2, default=str)
    print(f"  💾 Data saved: {json_path}")

    return {
        'name': name or url,
        'url': url,
        'city': city,
        'industry': industry,
        'score_result': result,
    }


def run_demo(output_dir: str = "output"):
    """Run demo scan against 5 sample businesses."""
    print("🎯 Hermes Local Business Web Scanner — Demo Mode")
    print("=" * 60)

    # Demo targets — mix of likely poor websites
    targets = [
        {
            'name': 'Example Dental Office',
            'url': 'https://www.example.com',  # Placeholder — will be replaced
            'city': 'Corinth, MS',
            'industry': 'Dentist',
        },
        {
            'name': 'Example Restaurant',
            'url': 'https://www.example.com',
            'city': 'Corinth, MS',
            'industry': 'Restaurant',
        },
    ]

    print("\n⚠️  Demo mode: Replace target URLs with real local business websites")
    print("   Edit the targets list in main.py or use: python main.py score <url>\n")

    prospects = []
    for t in targets:
        result = score_single(
            url=t['url'],
            name=t['name'],
            city=t['city'],
            industry=t['industry'],
            output_dir=output_dir,
        )
        if result:
            prospects.append(result)
        time.sleep(1)  # Be polite

    if prospects:
        # Generate prospect list
        list_md = generate_prospect_list(prospects)
        list_path = os.path.join(output_dir, "prospect-list.md")
        with open(list_path, 'w') as f:
            f.write(list_md)
        print(f"\n📋 Prospect list saved: {list_path}")

    print(f"\n✅ Demo complete. Check {output_dir}/ for all artifacts.")


def main():
    parser = argparse.ArgumentParser(description='Hermes Local Business Web Scanner')
    subparsers = parser.add_subparsers(dest='command')

    # Score command
    score_parser = subparsers.add_parser('score', help='Score a single website')
    score_parser.add_argument('url', help='Website URL')
    score_parser.add_argument('--name', default='', help='Business name')
    score_parser.add_argument('--city', default='', help='City')
    score_parser.add_argument('--industry', default='', help='Industry')
    score_parser.add_argument('--output', default='output', help='Output directory')

    # Batch command
    batch_parser = subparsers.add_parser('batch', help='Score multiple businesses')
    batch_parser.add_argument('city', help='City to search')
    batch_parser.add_argument('industry', help='Industry to search')
    batch_parser.add_argument('--count', type=int, default=5, help='Number of businesses')
    batch_parser.add_argument('--output', default='output', help='Output directory')

    # Demo command
    demo_parser = subparsers.add_parser('demo', help='Run demo scan')
    demo_parser.add_argument('--output', default='output', help='Output directory')

    args = parser.parse_args()

    if args.command == 'score':
        score_single(args.url, args.name, args.city, args.industry, args.output)
    elif args.command == 'batch':
        print("Batch mode requires Hermes Agent integration for discovery.")
        print("Use: python main.py score <url> for individual scoring.")
    elif args.command == 'demo':
        run_demo(args.output)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
