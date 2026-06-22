"""
Standard benchmark tasks used to evaluate each agent during evolution.

These tasks are chosen because they exercise the full range of each agent's skills
and expose all 5 scoring dimensions. Keep them stable across generations
so scores are comparable.
"""

BENCHMARK_TASKS: dict[str, str] = {
    "amara": (
        "Create a LinkedIn post about why African hospitals are still on paper records "
        "and how OPES EMR solves this. Include English and French versions. "
        "The post must have a hook that stops the scroll, specific stats or pain points "
        "relevant to Cameroon, mention of OPES EMR with pricing context, and a CTA to book a demo."
    ),
    "chisom": (
        "A hospital director in Yaoundé asks: 'We currently use paper records and Excel. "
        "Your OPES EMR costs how much? And what happens if our internet goes down?' "
        "Respond as CHISOM in both English and French. Be specific about the OPES EMR "
        "on-premise model, offline capability, and perpetual licensing price."
    ),
    "kofi": (
        "Build a complete Facebook ad campaign to get 20 demo bookings from private clinic "
        "owners in Douala this month. Include: campaign objective, audience targeting, "
        "3 ad variants (hook + body + CTA each), budget recommendation in FCFA, "
        "and a lead magnet offer. Apply the Grand Slam Offer framework."
    ),
    "zara": (
        "Write a 1,200-word SEO blog post: 'Comment choisir un logiciel de gestion "
        "hospitalière au Cameroun' (How to choose a hospital management system in Cameroon). "
        "Target keyword: 'logiciel gestion hôpital Cameroun'. Include OPES HIS product mention, "
        "meta description, and 3 internal link suggestions."
    ),
    "emeka": (
        "Research and list 10 qualified hospital leads in Douala, Cameroon. "
        "For each: name, type (private/public/clinic/NGO), size estimate, "
        "relevant contact title, and Tier (A/B/C) based on procurement likelihood. "
        "Then write a day-0 cold email to a Tier-A lead for OPES Hospital HIS."
    ),
    "fatima": (
        "A new client, Dr. Mireille Ndongo at Clinique Sainte-Marie in Yaoundé, "
        "just purchased OPES EMR (perpetual licence). Create her 30-day onboarding sequence: "
        "Day 0, 3, 7, 14, 30. Each touchpoint: channel (WhatsApp or email), "
        "message in English + French, and the specific goal of that message."
    ),
    "atlas": (
        "Produce a competitor analysis of OpenMRS vs OPES Health Systems for the "
        "Cameroonian market. Cover: product features, deployment model, pricing, "
        "geographic presence, FHIR compliance, offline capability, and African language support. "
        "End with 5 specific OPES competitive advantages to use in sales."
    ),
    "nova": (
        "Design the complete KPI framework for all 8 OPES AI employees. "
        "For each agent (AMARA, CHISOM, KOFI, ZARA, EMEKA, FATIMA, ATLAS, NOVA): "
        "3 primary KPIs, target benchmark, measurement frequency, and data source. "
        "Format as a CEO dashboard specification ready to implement."
    ),
}
