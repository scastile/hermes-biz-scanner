"""Pitch email generator. Creates personalized pitch emails based on scoring results."""
from datetime import date


PITCH_TEMPLATE = """Subject: {business_name} — Your Website Is Costing You Patients

Hi there,

I was searching for a {industry} in {city} and found {business_name}. First impression? Your services look great — but your website doesn't show it.

I ran a quick analysis of {url} and found some issues that are likely costing you new patients:

{top_issues}

These aren't just cosmetic problems. They directly impact how many people:
- Find you on Google (SEO)
- Stay on your site instead of bouncing (mobile experience)
- Trust you enough to book an appointment (design quality)

I'm [Your Name] from PaperLab Studio. I build modern, fast, mobile-first websites for local businesses like yours. Here's what I'd fix:

{redesign_bullets}

**What this gets you:**
- More phone calls from new patients finding you on Google
- A site that looks great on phones (where 60%+ of your visitors are)
- Faster loading = lower bounce rates
- A professional first impression that matches the quality of your work

I put together a quick mockup showing what a redesigned {business_name} site could look like. Want to see it?

Happy to hop on a 15-minute call to walk through it. No pressure — if it's not a fit, no hard feelings.

Best,
[Your Name]
PaperLab Studio
{contact_email}
{contact_phone}

P.S. — Your competitors' websites are looking pretty sharp these days. Time to level up.
"""


def generate_pitch(business_name: str, url: str, city: str, industry: str,
                   score_result: dict, contact_email: str = "", contact_phone: str = "") -> str:
    """Generate a pitch email from scoring results."""
    cats = score_result['categories']

    # Collect top issues (all failures across categories)
    issues = []
    for cat_name, cat_data in cats.items():
        for detail in cat_data['details']:
            if detail.startswith('✗'):
                issues.append(f"  • {detail}")

    top_issues = '\n'.join(issues[:5]) if issues else "  • General design and usability concerns"

    # Generate redesign bullets based on low-scoring categories
    bullets = []
    for cat_name, cat_data in cats.items():
        pct = (cat_data['score'] / cat_data['max']) * 100
        if pct < 60:
            if 'Mobile' in cat_name:
                bullets.append(f"  • Rebuild mobile experience — currently {pct:.0f}/100")
            elif 'Design' in cat_name:
                bullets.append(f"  • Modernize visual design — currently {pct:.0f}/100")
            elif 'SEO' in cat_name:
                bullets.append(f"  • Fix SEO fundamentals — currently {pct:.0f}/100")
            elif 'Accessibility' in cat_name:
                bullets.append(f"  • Improve accessibility — currently {pct:.0f}/100")
            elif 'Performance' in cat_name:
                bullets.append(f"  • Speed optimization — currently {pct:.0f}/100")

    redesign_bullets = '\n'.join(bullets) if bullets else "  • Complete visual refresh and mobile optimization"

    return PITCH_TEMPLATE.format(
        business_name=business_name,
        url=url,
        city=city,
        industry=industry,
        top_issues=top_issues,
        redesign_bullets=redesign_bullets,
        contact_email=contact_email or "[your email]",
        contact_phone=contact_phone or "[your phone]",
    )
