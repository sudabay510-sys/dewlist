from helpers import L, LM, opt, env_names

Q = [
    {"id": "age", "type": "choice", "prompt": "First, how old are you?", "help": "Dewlist is for adults.",
     "options": [opt("18_24", "18–24"), opt("25_34", "25–34"), opt("35_49", "35–49"), opt("50", "50+"), opt("under", "Under 18")]},
    {"id": "concern", "type": "choice", "prompt": "Is any of this happening right now?", "help": "Safety check — these need a professional, not a routine.",
     "options": [opt("none", "None of these"), opt("rash", "A painful, spreading, or bleeding rash or sore"), opt("mole", "A mole or spot that’s changing"), opt("severe", "Severe acne, swelling, or a reaction to a product")]},
    {"id": "goal", "type": "choice", "prompt": "What would you like your routine to focus on?", "help": "Cosmetic goals only.",
     "options": [opt("simple", "Just a simple, consistent routine"), opt("sun", "Better daily sun protection habits"), opt("hydration", "Skin that feels less dry or tight"), opt("shine", "Skin that feels less oily"), opt("texture", "Smoother-feeling skin")]},
    {"id": "feel", "type": "choice", "prompt": "By midday, how does your skin usually feel?",
     "options": [opt("tight", "Tight or dry"), opt("comfy", "Comfortable"), opt("shiny", "Shiny in the T-zone"), opt("oily", "Oily all over"), opt("unsure", "Hard to say")]},
    {"id": "sensitive", "type": "choice", "prompt": "Do new products often sting or irritate?",
     "options": [opt("often", "Often"), opt("sometimes", "Sometimes"), opt("rarely", "Rarely")]},
    {"id": "minutes", "type": "choice", "prompt": "How long do you want to spend, morning + night?",
     "options": [opt("2", "2 minutes or less"), opt("5", "About 5 minutes"), opt("10", "10+ minutes — I enjoy it")]},
    {"id": "climate", "type": "choice", "prompt": "What’s your climate like right now?",
     "options": [opt("dry", "Dry / cold"), opt("humid", "Hot / humid"), opt("mild", "Mild"), opt("indoor", "Lots of AC or heating indoors")]},
    {"id": "sun", "type": "choice", "prompt": "How often do you wear sunscreen?",
     "options": [opt("daily", "Daily"), opt("sometimes", "Sometimes"), opt("rarely", "Rarely or never")]},
    {"id": "fragrance", "type": "choice", "prompt": "Fragrance in products?",
     "options": [opt("free", "Prefer fragrance-free"), opt("ok", "Don’t mind"), opt("love", "Love scented products")]},
    {"id": "current", "type": "choice", "prompt": "What’s in your routine today?",
     "options": [opt("nothing", "Nothing consistent"), opt("basic", "Cleanser + moisturizer"), opt("many", "Lots of products, no real order"), opt("rx", "I use a prescription from a doctor")]},
]


def plan(a):
    flagged = a.get("concern") not in (None, "none")
    minor = a.get("age") == "under"
    sens = a.get("sensitive") in ("often", "sometimes") or a.get("fragrance") == "free"
    minutes = a.get("minutes", "5")
    am = ["Rinse or gentle cleanser", "Moisturizer suited to how your skin feels", "Broad-spectrum sunscreen (SPF 30+ is a common recommendation from dermatology groups)"]
    pm = ["Gentle cleanser (remove sunscreen/makeup)", "Moisturizer"]
    if minutes == "10":
        pm.insert(1, "Optional: one ‘extra’ step you already tolerate — add only one new product at a time")
    pre = []
    if flagged:
        pre.append("Please see a dermatologist or doctor about what you described before changing your routine. A plan can’t assess skin conditions.")
    if minor:
        pre.append("Dewlist is designed for adults. Please talk with a parent/guardian and a doctor or dermatologist about your skin.")
    if a.get("current") == "rx":
        pre.append("Keep following your prescriber’s instructions. Ask them before adding anything new.")
    return {
        "title": "Your Dewlist routine — " + ("check in with a professional first" if (flagged or minor) else f"{'gentle, ' if sens else ''}{L(Q[5]['options'], minutes).lower()}"),
        "summary": f"Cosmetic focus: {L(Q[2]['options'], a.get('goal')).lower()}. Skin feel: {L(Q[3]['options'], a.get('feel')).lower()}. Climate: {L(Q[6]['options'], a.get('climate')).lower()}. This is general skincare-habit education — not a diagnosis, treatment, or medical advice.",
        "preview_sections": ([{"title": "Before you start", "bullets": pre}] if pre else []) + [
            {"title": "Morning order (unlocked)", "bullets": am},
            {"title": "Evening order (unlocked)", "bullets": pm},
            {"title": "Patch-test habit", "body": "Try any new product on a small area (like inside the forearm or behind the ear) for several days first." + (" With easily irritated skin, go slower and choose fragrance-free." if sens else "") + " Stop and talk to a dermatologist if irritation happens."},
        ],
        "locked_sections": [
            {"title": "4-week habit tracker", "teaser": "Daily check-boxes and a ‘how does it feel’ note — no before/after promises."},
            {"title": "Ingredient label explainer", "teaser": "How to read an INCI list — education, not product prescriptions."},
            {"title": "Seasonal routine swaps", "teaser": "General ideas for dry winters and humid summers."},
            {"title": "Questions to bring to your dermatologist", "teaser": "A short list to make an appointment easier."},
        ],
    }


BRAND = {
    "name": "Dewlist", "slug": "dewlist", "port": 5112,
    "tagline": "A simple AM/PM skincare habit plan — general education, not medical advice.",
    "eyebrow": "Skincare habits · education only",
    "hero_title": "A simple routine you’ll actually keep.",
    "hero_lede": "Answer 10 questions about how your skin feels, your time, and your preferences. Dewlist gives you a calm AM/PM order, a patch-test habit, and sunscreen reminders.",
    "cta_primary": "Build my routine", "cta_short": "Start quiz",
    "cta_band_title": "Fewer products. Clear order. Kind to your skin.",
    "cta_band_text": "General education to help you build habits — and know when to see a dermatologist.",
    "honesty_line": "General education only. Not a diagnosis or treatment. No skin-results promises.",
    "safety_title": "Health note",
    "safety_note": "Dewlist doesn’t diagnose or treat skin conditions. For acne that hurts or scars, rashes, changing moles, or reactions, see a board-certified dermatologist or your doctor.",
    "audience_line": "Adults who feel lost in the product aisle and want a simple, consistent routine — with clear limits.",
    "personas": [
        {"title": "Routine beginner", "text": "You own a cleanser. Maybe. You want to start simple."},
        {"title": "Product collector", "text": "A shelf full of bottles and no idea what order they go in."},
        {"title": "Sensitive-skin cautious", "text": "You want gentle, slow, patch-tested steps."},
    ],
    "journey": [
        {"stage": "Overwhelm", "pain": "Too many products and opinions.", "fix": "A short AM/PM order matched to your time."},
        {"stage": "Try", "pain": "New products sting or break you out.", "fix": "One-at-a-time patch-test habit."},
        {"stage": "Stick with it", "pain": "Routines fade after a week.", "fix": "A 4-week habit tracker."},
        {"stage": "Know when to ask", "pain": "Unsure if something needs a doctor.", "fix": "Clear ‘see a dermatologist’ pointers."},
    ],
    "how_steps": [
        {"title": "Answer 10 questions", "text": "Skin feel, time, climate, and a safety check."},
        {"title": "See your routine", "text": "AM/PM order and patch-test habit unlocked."},
        {"title": "Start your plan", "text": "Enter your email, then complete checkout on Gumroad."},
    ],
    "features": [
        {"title": "AM/PM order", "text": "Steps in a sensible sequence for your time."},
        {"title": "Patch-test habit", "text": "Introduce one product at a time."},
        {"title": "Sunscreen habit", "text": "Daily reminders built in."},
        {"title": "Seasonal education", "text": "Subscription: routine swap ideas as weather changes."},
    ],
    "sample_peek": ["Gentle cleanse → moisturize → SPF", "One new product at a time", "Patch test before full use", "When to see a dermatologist"],
    "trust_points": [
        {"title": "No diagnosis", "text": "We don’t identify or treat conditions."},
        {"title": "No product kickbacks", "text": "We don’t sell or push specific brands."},
        {"title": "Safety screen", "text": "Concerning symptoms → professional, not a routine."},
    ],
    "faq": [
        {"q": "Can Dewlist treat my acne or eczema?", "a": "No. Dewlist is general habit education. Please see a dermatologist for any skin condition."},
        {"q": "Do you recommend specific products?", "a": "No. We describe product types and how to introduce them, not brands."},
        {"q": "How does billing work?", "a": "Choose Monthly or Quarterly, save your email, then complete payment on Gumroad. Renews automatically. Cancel anytime from your Gumroad library."},
        {"q": "I use a prescription. Can I use this?", "a": "Follow your prescriber first and ask them before adding anything new."},
    ],
    "pricing": [
        {"id": "monthly", "name": "Monthly", "price": "$12", "period": "/ month",
         "intro": "$12", "renewal": "$12 / month", "renewal_note": "Renews automatically. Cancel anytime from your Gumroad library.",
         "includes": ["AM/PM routine", "Patch-test guide", "Habit tracker"]},
        {"id": "quarterly", "name": "Quarterly", "price": "$29", "period": "every 3 months",
         "intro": "$29", "renewal": "$29 every 3 months", "renewal_note": "Renews automatically. Cancel anytime from your Gumroad library.", "featured": True,
         "includes": ["Everything in Monthly", "Ingredient label explainer", "Seasonal routine swaps"]},
    ],
    "checkout_url": "https://solvfix.gumroad.com/l/ozmyi",
    "disclaimer_short": "General skincare education only. Not medical advice, diagnosis, or treatment. See a dermatologist for skin concerns. No results guarantees.",
    "disclaimer_long": "Dewlist provides general, non-medical skincare-habit education for adults. It does not diagnose, treat, cure, or prevent any disease or skin condition, does not evaluate symptoms, and is not a substitute for advice from a board-certified dermatologist or other licensed clinician. Statements have not been evaluated by the FDA. Stop using any product that irritates your skin and seek professional care. Dewlist does not sell or recommend specific products. Payments are processed by Gumroad, not on this site.",
    "font_url": "https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap",
    "fonts": ("DM Serif Display", "Plus Jakarta Sans"),
    "questions": Q, "generate_plan": plan,
    "voice": "Gentle, clear, science-respecting. Like a friend who reads labels — and tells you when to see a doctor.",
    "palette": {"Background (blush)": "#FBF5F3", "Alt": "#F4E8E4", "Card": "#FFFFFF", "Ink": "#2B2326", "Muted": "#6E5F63", "Accent (rosewood)": "#A8506A", "Accent hover": "#8C3F56", "Highlight (dew)": "#BFE3DC"},
    "logo_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none"><rect width="64" height="64" rx="32" fill="#A8506A"/><path d="M32 14c7 9 12 15.5 12 22a12 12 0 0 1-24 0c0-6.5 5-13 12-22z" fill="#FBF5F3"/><path d="M27 37a5 5 0 0 0 5 5" stroke="#BFE3DC" stroke-width="3" stroke-linecap="round"/></svg>',
    "css_vars": """
  --bg:#FBF5F3;--bg-alt:#F4E8E4;--card:#FFFFFF;--ink:#2B2326;--muted:#6E5F63;--line:#EBDCD7;
  --accent:#A8506A;--accent-2:#8C3F56;--on-accent:#FFFFFF;--hi:#BFE3DC;--radius:24px;
  --font-display:'DM Serif Display', Georgia, serif;--font-body:'Plus Jakarta Sans', system-ui, sans-serif;
  --shadow-card:0 24px 50px rgba(168,80,106,.10);--shadow-btn:0 10px 24px rgba(168,80,106,.25);
  --cta-band-bg:#BFE3DC;--cta-band-ink:#1F3330;--cta-band-btn:#A8506A;--cta-band-btn-ink:#FFFFFF;--tracking:-0.01em;
""",
    "personality": "background:radial-gradient(700px 400px at 80% 0%, #F7D6DE 0%, transparent 60%), radial-gradient(600px 300px at 0% 90%, #DDF1EC 0%, transparent 60%), var(--bg);",
    "extra_css": ".btn{border-radius:999px}h1{font-weight:400}.dot{background:var(--hi);outline:2px solid var(--accent)}",
    "dos": ["Say ‘general education’ and ‘see a dermatologist’ plainly.", "Describe product types, never specific brands or prescription ingredients."],
    "donts": ["Diagnose, name, or claim to treat conditions (acne, eczema, rosacea, etc.).", "Show before/after photos or promise visible results."],
}
BRAND.update(env_names("dewlist"))
