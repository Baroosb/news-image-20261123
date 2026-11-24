#!/usr/bin/env python3
"""news-image-20261123 v4 — "The World in One Day", Monday 23 Nov 2026.

v4 is a full visual overhaul of v3. Content started as v3's 35
stories; a post-build fact audit (AUDIT.md) then failed 10 items as
Sunday-dated or misnumbered, and those slots were rebuilt from the
verified Monday replacements in REPLACEMENTS.md (lead 1 reframed as
Monday's announcement; cards 4, 8, 12, 13 and ALSO 17, 18, 20
replaced; card 10 re-sourced to PA's Monday report; Sensex corrected
to -1,484 in ALSO 19 and the stat strip).
The dense newspaper grid is gone; v4 is a premium editorial poster:

- deep ink-navy masthead carrying the kicker, the giant Playfair date,
  the red-lead strap (cream italic) and the UTC ticker in one band;
- a calm cream stat strip with big navy numerals;
- lead panels and cards on light cream with generous whitespace;
- simple flat duotone scenes (big geometric shapes, no clip-art
  detail) in navy / teal / sand / rust / ochre;
- the world map restyled to a muted-teal ocean with sand land;
- the ALSO digest set in two airy columns, region-grouped, at one
  uniform size with real leading (long items wrap, never shrink).

Renders entry-v4.png (1024x1024) plus entry-v4-300.png with PIL.
Every text block goes through a fit helper that registers a check;
the build fails loudly if any block had to be ellipsized.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry-v4.png")
OUT300 = os.path.join(HERE, "entry-v4-300.png")

FONTS = os.path.join(HERE, "fonts")
DEJA = "/usr/share/fonts/truetype/dejavu"


def _vf(name, size, axes):
    """Load a variable font from fonts/ pinned to the given axis values."""
    fnt = ImageFont.truetype(os.path.join(FONTS, name), size)
    fnt.set_variation_by_axes(axes)
    return fnt


def pf900(s):
    """Playfair Display Black — masthead date, stat figures, card figures."""
    return _vf("PlayfairDisplay-VF.ttf", s, [900])


def pf700(s):
    """Playfair Display Bold — lead and card headlines."""
    return _vf("PlayfairDisplay-VF.ttf", s, [700])


def pf_i700(s):
    """Playfair Display Bold Italic — the strap."""
    return _vf("PlayfairDisplay-Italic-VF.ttf", s, [700])


def ar500(s):
    """Archivo Medium — card micro-lines."""
    return ImageFont.truetype(os.path.join(FONTS, "Archivo-500.ttf"), s)


def ar700(s):
    """Archivo Bold — band, pills, chips, headers, map labels."""
    return ImageFont.truetype(os.path.join(FONTS, "Archivo-700.ttf"), s)


def bc600(s):
    """Barlow Condensed SemiBold — kickers, stat captions, region bar."""
    return ImageFont.truetype(
        os.path.join(FONTS, "BarlowCondensed-600.ttf"), s)


def in400(s):
    """Inter Regular (full charset, carries the rupee sign) — body text."""
    return _vf("Inter-VF.ttf", s, [14, 400])


def dsans(s):
    """DejaVu Sans — pictogram glyphs only (the one slot the new faces
    cannot cover: crossed swords, heavy cross, scales)."""
    return ImageFont.truetype(os.path.join(DEJA, "DejaVuSans.ttf"), s)


# ---------------------------------------------------------------- palette
NAVY = (20, 35, 46)        # deep ink navy — masthead, figures
NAVY_TX = (22, 30, 36)     # body ink on cream
CREAM = (243, 234, 216)    # warm cream paper
CREAM_LT = (250, 245, 232)  # panel fill
RUST = (179, 64, 42)       # rust red accent
OCHRE = (217, 164, 65)     # ochre accent
MID = (96, 88, 74)
HAIR = (204, 193, 168)
WHITE = (250, 248, 242)
TEAL_OC = (172, 198, 190)  # muted teal — map ocean, scene seas
SAND = (228, 214, 175)     # map land
SAND_D = (214, 198, 164)   # scene land / blocks

REGION_COLORS = {
    "Europe": (70, 100, 140),
    "Asia": (34, 110, 104),
    "Africa": (198, 118, 38),
    "Americas": (96, 122, 52),
    "Middle East": (138, 28, 19),
    "Global": (51, 72, 79),
    "Oceania": (112, 72, 112),
}

TIER_COLORS = {
    "CONFIRMED": (96, 122, 52),
    "OFFICIAL": (70, 100, 140),
    "REPORTED": (178, 102, 30),
    "CLAIM": (138, 28, 19),
}

# ---------------------------------------------------------------- stories
# Page numbering: leads are 1-3 (Benghazi, Trump/Iran, Kyiv toll), cards
# 4-15, ALSO ON 16-35. Fields: n, region, place, field, tier, headline,
# body (leads/cards), figure (cards), source, pin (lon, lat).
# Text as audited: fixed slots follow AUDIT.md / REPLACEMENTS.md.
STORIES = [
    dict(n=1, region="Africa", place="BENGHAZI, LIBYA", field="CONFLICT",
         tier="REPORTED",
         headline="Zelensky: Ukraine sank Russian corvette off Libya "
                  "with seven naval drones",
         body=("Zelensky announced on Monday that seven naval drones "
               "from a mothership sank the Russian corvette Merkury "
               "off Libya \u2014 a first. The SBU released details the "
               "same day; satellite imagery showed the ship "
               "rolled over. Libya condemned the attack; Moscow "
               "responded."),
         source="CNN / AP",
         pin=(20.1, 32.1)),
    dict(n=2, region="Middle East", place="WASHINGTON / TEHRAN",
         field="POLITICS", tier="REPORTED",
         headline="Trump sets New Year deadline for an Iran deal",
         body=("President Trump demanded a \u201cpermanent\u201d deal by "
               "New Year and threatened US strikes, as reports said Iran "
               "was preparing a tanker convoy from Kharg Island to "
               "challenge the US naval blockade."),
         source="NDTV, agency inputs",
         pin=(50.3, 29.2)),
    dict(n=3, region="Europe", place="DYMER, UKRAINE", field="CONFLICT",
         tier="REPORTED",
         headline="Kyiv-region strike toll reaches at least nine",
         body=("Rescuers searched the rubble of a five-storey block in "
               "Dymer, north of Kyiv, collapsed by a Russian drone; "
               "by Monday the toll had reached at least nine "
               "dead, a child pulled out alive."),
         source="The Guardian",
         pin=(30.4, 50.7)),
    dict(n=4, region="Middle East", place="SYRIA", field="SECURITY",
         tier="REPORTED", figure="15 ALLIES",
         headline="US discussing military training for Syrian forces",
         body=("The US is discussing training Syrian soldiers in "
               "demining and ordnance disposal \u2014 a first US "
               "training mission with Syria's military since former "
               "rebels took power in Damascus in 2024 \u2014 with "
               "personnel from ~15 allies and a possible March start."),
         source="Reuters",
         pin=(38.0, 35.0)),
    dict(n=5, region="Global", place="WORLD MARKETS", field="ENERGY",
         tier="REPORTED", figure="<$92",
         headline="Oil slips below $92 as selloff outweighs Iran fears",
         body=("Brent fell under $92 as the AI-led equity selloff hit "
               "commodities; Hormuz attacks limited the losses."),
         source="Reuters",
         pin=(56.5, 26.5)),
    dict(n=6, region="Europe", place="WARSAW", field="SECURITY",
         tier="CLAIM", figure="2 PLOTS",
         headline="Poland: Russia twice tried to kill rapper Kyivstoner",
         body=("Polish authorities said Russian agents twice tried to "
               "kill the Ukrainian-American rapper in August."),
         source="Al Jazeera",
         pin=(21.0, 52.2)),
    dict(n=7, region="Europe", place="ROSTOV, RUSSIA", field="CONFLICT",
         tier="REPORTED", figure="200 KM",
         headline="Ukrainian drones set Novoshakhtinsk refinery ablaze",
         body=("A large drone attack early Monday left the oil plant "
               "burning, 200 km from Ukrainian-held territory."),
         source="Kyiv Independent",
         pin=(39.9, 47.8)),
    dict(n=8, region="Europe", place="KYIV", field="CONFLICT",
         tier="REPORTED", figure="NEW STRIKES",
         headline="Zelenskiy says intelligence shows Russia planning "
                  "new strikes on Ukraine",
         body=("In his Monday nightly address, Zelenskiy said "
               "Ukrainian intelligence shows Russia preparing new "
               "strikes, and urged the US and other partners to heed "
               "the warning because air-defence supplies depend on "
               "their decisions."),
         source="Reuters",
         pin=(30.5, 50.4)),
    dict(n=9, region="Europe", place="LONDON", field="POLITICS",
         tier="OFFICIAL", figure="UTILITIES",
         headline="UK to argue for more public control of utilities",
         body=("The Labour government sets out its case for greater "
               "public control of energy and water on Monday."),
         source="Reuters",
         pin=(-3.5, 53.5)),
    dict(n=10, region="Europe", place="LONDON", field="POLITICS",
         tier="REPORTED", figure="£17BN",
         headline="Burnham denies EU deal is a ‘prelude’ to rejoining",
         body=("Presenting his EU agreement to MPs on Monday, Burnham "
               "said it is “not a prelude” to rejoining and "
               "that rejoining without a referendum would be "
               "“unthinkable”. The Treasury puts the gain at "
               "up to £17bn a year (0.5% of GDP); the Partnerships "
               "Bill faces a Commons vote before Christmas, and SPS "
               "checks end 1 Mar 2028."),
         source="PA Media",
         pin=(0.8, 51.2)),
    dict(n=11, region="Europe", place="BRATISLAVA", field="POLITICS",
         tier="OFFICIAL", figure="5 LEADERS",
         headline="Visegr\u00e1d Four and Austria meet at Bratislava Castle",
         body=("Fico, Babi\u0161, Tusk and Hungary's PM joined Austria's "
               "chancellor on competitiveness, energy and the EU budget."),
         source="Czech Govt / TASR",
         pin=(17.1, 48.1)),
    dict(n=12, region="Europe", place="LONDON", field="SPORT",
         tier="CONFIRMED", figure="4-0",
         headline="Brentford rout 10-man Everton 4-0 in Monday night "
                  "Premier League",
         body=("Keane Lewis-Potter scored two goals in three minutes "
               "midway through the first half to set Brentford on its "
               "way to a comfortable 4-0 Premier League win over "
               "10-man Everton on Monday night."),
         source="AP",
         pin=(-0.3, 51.5)),
    dict(n=13, region="Africa", place="BUNIA, DR CONGO", field="HEALTH",
         tier="REPORTED", figure=">1,000",
         headline="‘Fields of graves’: Ebola deaths in Congo "
                  "far exceed official counts",
         body=("A Reuters analysis of cemetery satellite imagery, "
               "published Monday, found more than 1,000 excess deaths "
               "in Bunia by early November against an official Ebola "
               "toll of 707; at Nyamurongo cemetery, burials rose from "
               "2.4 a day before the outbreak to over 9 a day."),
         source="Reuters",
         pin=(29.5, 1.6)),
    dict(n=14, region="Americas", place="NEW YORK", field="MARKETS",
         tier="REPORTED", figure="+4.7%",
         headline="S&P 500's best day since April 2025 as Nvidia soars 31%",
         body=("Wall Street's best day since April 2025: the S&P 500 "
               "surged 4.7% as Nvidia jumped 31%, its best day since "
               "2003, rebounding from the AI-led selloff."),
         source="Reuters",
         pin=(-74.0, 40.7)),
    dict(n=15, region="Asia", place="BANGKOK", field="LAW",
         tier="CONFIRMED", figure="3 YEARS",
         headline="Thai court cuts MP Rukchanok's sentence to three years",
         body=("The appeal court halved the People's Party MP's "
               "l\u00e8se-majest\u00e9 sentence from six years."),
         source="Khaosod English",
         pin=(100.5, 13.8)),
]

ALSO = [
    dict(n=16, region="Asia", place="TOYOHASHI, JAPAN", tier="OFFICIAL",
         line="Japan confirms season's 3rd bird flu case; ~80,000 hens to be culled in Aichi",
         source="Jiji Press", pin=(137.8, 35.2)),
    dict(n=17, region="Asia", place="SHANGHAI", tier="REPORTED",
         line="China stocks V-rebound: Shanghai +0.15% at 3,538.95 (low 3,476.65), ChiNext +3.08%; turnover ¥1.55tn",
         source="Yonhap Infomax", pin=(121.5, 31.2)),
    dict(n=18, region="Asia", place="AHMEDABAD", tier="REPORTED",
         line="Adani Airport Holdings to sell up to 1.55% to 360 One for up to ₹27.9bn ($300.37M)",
         source="Reuters", pin=(72.6, 23.0)),
    dict(n=19, region="Asia", place="MUMBAI", tier="REPORTED",
         line="Sensex plunges 1,484 points as the global AI selloff hits Indian markets",
         source="Hindu BusinessLine", pin=(72.9, 19.1)),
    dict(n=20, region="Asia", place="TAIPEI", tier="REPORTED",
         line="Taiwan TAIEX swings 1,666 points to close +2.16% (36,811.89); short-sale curbs debut, stabilization fund steps in",
         source="TVBS / BigGo", pin=(121.0, 23.5)),
    dict(n=21, region="Asia", place="HYDERABAD", tier="REPORTED",
         line="Hyderabad approves AI traffic management plan covering 429 signals",
         source="Daily AI Brief", pin=(78.5, 17.4)),
    dict(n=22, region="Asia", place="NEW DELHI", tier="REPORTED",
         line="Nepal PM Balen Shah holds first bilateral talks with Modi in New Delhi",
         source="Hindustan Times", pin=(77.2, 28.6)),
    dict(n=23, region="Americas", place="VIRGINIA, USA", tier="REPORTED",
         line="Trump hosts 3rd meme coin gala as the $TRUMP token sinks below $1 (peak ~$75)",
         source="Reuters", pin=(-77.8, 38.9)),
    dict(n=24, region="Americas", place="WASHINGTON", tier="REPORTED",
         line="Senate panel investigates Vance's ties to a prized Venezuelan oil contract",
         source="Reuters", pin=(-77.0, 38.9)),
    dict(n=25, region="Americas", place="ALBERTA, CANADA", tier="OFFICIAL",
         line="Alberta unveils bill letting the province fund and build gas pipelines itself",
         source="Reuters", pin=(-113.5, 53.5)),
    dict(n=26, region="Americas", place="TORONTO", tier="REPORTED",
         line="Canadian dollar falls for a 10th straight session, to a 19-month low",
         source="Reuters", pin=(-79.4, 43.7)),
    dict(n=27, region="Americas", place="S\u00e3o Paulo, BRAZIL",
         tier="REPORTED",
         line="Braskem agrees a $4.9 billion restructuring plan with its creditors",
         source="Reuters", pin=(-46.6, -23.5)),
    dict(n=28, region="Americas", place="SANTA CLARA, USA",
         tier="REPORTED",
         line="Nvidia board reinstates Jensen Huang as CEO, 11 days after he resigned",
         source="Reuters", pin=(-122.0, 37.4)),
    dict(n=29, region="Americas", place="SINGAPORE", tier="REPORTED",
         line="US set to blacklist Singapore chip firm Megaspeed, tied to Nvidia scandal",
         source="Reuters", pin=(103.6, 2.8)),
    dict(n=30, region="Oceania", place="MELBOURNE", tier="CONFIRMED",
         line="Australian music icon Ian \u2018Molly\u2019 Meldrum dies aged 83; tributes pour in",
         source="ABC News", pin=(145.0, -37.8)),
    dict(n=31, region="Oceania", place="CANBERRA", tier="REPORTED",
         line="Newspoll slump for Albanese as Angus Taylor leads as preferred PM",
         source="The New Daily", pin=(149.1, -35.3)),
    dict(n=32, region="Oceania", place="CANBERRA", tier="REPORTED",
         line="Greens optimistic of a deal on the digital duty of care bill this week",
         source="ABC News", pin=(146.0, -33.5)),
    dict(n=33, region="Oceania", place="WELLINGTON", tier="CONFIRMED",
         line="Cricket: NZ hold India to a draw \u2014 NZ 239-5 (Mitchell 49 not out), India 720-9 declared",
         source="AAP", pin=(174.2, -41.2)),
    dict(n=34, region="Global", place="NEW YORK", tier="REPORTED",
         line="Asia markets brace for more AI-led selling as US futures bounce",
         source="Reuters", pin=(-74.0, 40.7)),
    dict(n=35, region="Global", place="THE HAGUE", tier="OFFICIAL",
         line="Chemical weapons watchdog OPCW faces budget crisis over unpaid US dues",
         source="Reuters", pin=(4.5, 52.1)),
]

ALL_STORIES = STORIES + ALSO

STATS = [
    ("9", "DEAD IN KYIV-REGION STRIKES"),
    ("<$92", "BRENT CRUDE, DOWN MONDAY"),
    ("80,000", "HENS TO BE CULLED, AICHI"),
    ("-1,484", "SENSEX POINTS, MONDAY TRADE"),
    ("NVIDIA +31%", "BEST DAY SINCE 2003 \u00b7 WALL ST BEST SINCE APR 2025"),
    ("720/9", "INDIA DECLARED, WELLINGTON"),
]

TIMELINE = [
    ("02:00 UTC", "BANGKOK \u2014 appeal court cuts MP Rukchanok's sentence to 3 years"),
    ("18:30 UTC", "MELBOURNE \u2014 Molly Meldrum dies, 05:30 Mon AEDT"),
]

DATE_CHECK = (
    "Left out as other days' news: RSF strikes on Khartoum (Sun 22 Nov) \u00b7 "
    "COP31 ends without a pact, Antalya (Sun 22 Nov) \u00b7 S. Korea minister "
    "resigns (Sun 22 Nov) \u00b7 \u2018Chapo Isidro\u2019 captured, Sinaloa "
    "(Fri 20 Nov) \u00b7 Anthropic IPO (Wed 18 Nov)"
)

# region counts computed from the data, never typed by hand
REGION_ORDER = ["Europe", "Middle East", "Africa", "Asia", "Americas",
                "Oceania", "Global"]
REGION_COUNTS = {r: sum(1 for s in ALL_STORIES if s["region"] == r)
                 for r in REGION_ORDER}
N_STORIES = len(ALL_STORIES)
N_REGIONS = sum(1 for v in REGION_COUNTS.values() if v > 0)

# ------------------------------------------------------------ fit checks
CHECKS = []
ELLIPSIZED = []


def _register(label, needed, box):
    CHECKS.append((label, needed, box))


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=fnt) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def ellipsize(draw, text, fnt, max_w):
    while text and draw.textlength(text + "\u2026", font=fnt) > max_w:
        text = text[:-1]
    return text + "\u2026"


def fit_box(draw, label, text, make_font, start, min_size, max_w, box_h,
            leading=1.16):
    """Largest font whose wrapped block fits box_h; registers a check."""
    size = start
    while size > min_size:
        fnt = make_font(size)
        lines = wrap(draw, text, fnt, max_w)
        h = (len(lines) - 1) * leading * size + size
        if h <= box_h:
            _register(label, h, box_h)
            return fnt, lines, size
        size -= 1
    fnt = make_font(min_size)
    lines = wrap(draw, text, fnt, max_w)
    max_lines = max(1, int((box_h - min_size) / (leading * min_size)) + 1)
    if len(lines) > max_lines:
        tail = " ".join(lines[max_lines - 1:])
        lines = lines[:max_lines - 1] + [ellipsize(draw, tail, fnt, max_w)]
        ELLIPSIZED.append(label)
    h = (len(lines) - 1) * leading * min_size + min_size
    _register(label, h, box_h)
    return fnt, lines, min_size


def fit_oneline(draw, label, text, make_font, start, min_size, max_w,
                step=1):
    size = start
    while size > min_size and \
            draw.textlength(text, font=make_font(size)) > max_w:
        size -= step
    fnt = make_font(size)
    if draw.textlength(text, font=fnt) > max_w:
        text = ellipsize(draw, text, fnt, max_w)
        ELLIPSIZED.append(label)
    _register(label, draw.textlength(text, font=fnt), max_w)
    return fnt, text


def tracked_width(draw, text, fnt, tracking):
    return sum(draw.textlength(c, font=fnt) for c in text) + \
        tracking * max(0, len(text) - 1)


def draw_tracked(draw, x, y, text, fnt, tracking, fill):
    cx = x
    for c in text:
        draw.text((cx, y), c, font=fnt, fill=fill)
        cx += draw.textlength(c, font=fnt) + tracking
    return cx


def fit_tracked(draw, label, text, make_font, start, min_size, tracking,
                max_w):
    size = start
    while size > min_size and \
            tracked_width(draw, text, make_font(size), tracking) > max_w:
        size -= 1
    fnt = make_font(size)
    if tracked_width(draw, text, fnt, tracking) > max_w:
        ELLIPSIZED.append(label)
    _register(label, tracked_width(draw, text, fnt, tracking), max_w)
    return fnt


def report_checks():
    bad = [(l, n, b) for (l, n, b) in CHECKS if n > b + 0.5]
    for l, n, b in CHECKS:
        print(f"  fit {'ok  ' if n <= b + 0.5 else 'FAIL'} {l}: "
              f"{n:.0f} <= {b:.0f}")
    print(f"fit check: {len(CHECKS) - len(bad)}/{len(CHECKS)} blocks fit; "
          f"ellipsized: {len(ELLIPSIZED)} {ELLIPSIZED}")
    if bad or ELLIPSIZED:
        raise SystemExit("FIT CHECK FAILED")


def text_block(draw, x, y, lines, fnt, size, leading=1.16, fill=NAVY_TX):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += size * leading
    return y


def pill(draw, x, y, tier, size=11):
    fnt = ar700(size)
    w_ = draw.textlength(tier, font=fnt) + 12
    draw.rectangle([x, y, x + w_, y + size + 7], fill=TIER_COLORS[tier])
    draw.text((x + 6, y + 3), tier, font=fnt, fill=WHITE)
    return w_

# ------------------------------------------------------------ lead scenes
# Simple flat duotone geometry: big silhouettes, no fiddly detail.
def scene_benghazi(d, x, y, w_, h):
    """Teal sea, sand coast, one navy corvette, rust fire, two drones."""
    d.rectangle([x, y, x + w_, y + h], fill=TEAL_OC)
    coast = [(0.00, 0.60), (0.20, 0.52), (0.38, 0.36), (0.52, 0.32),
             (0.66, 0.42), (0.82, 0.50), (1.00, 0.54),
             (1.00, 1.00), (0.00, 1.00)]
    d.polygon([(x + u * w_, y + v * h) for u, v in coast], fill=SAND)
    d.line([(x + u * w_, y + v * h) for u, v in coast[:7]],
           fill=(150, 128, 84), width=2)
    # corvette: one big navy silhouette straddling the coast bulge
    bx, by = x + 0.50 * w_, y + 0.16 * h
    d.polygon([(bx - 46, by + 14), (bx + 50, by + 14), (bx + 38, by + 26),
               (bx - 34, by + 26)], fill=NAVY)
    d.rectangle([bx - 20, by + 2, bx + 18, by + 14], fill=NAVY)
    d.rectangle([bx + 2, by - 10, bx + 9, by + 2], fill=NAVY)
    # fire: two rust/ochre discs on the base
    for dx, r, col in [(-58, 13, RUST), (-50, 8, OCHRE),
                       (34, 9, RUST), (38, 5, OCHRE)]:
        d.ellipse([bx + dx - r, by + 24 - r, bx + dx + r, by + 24 + r],
                  fill=col)
    # two sea drones: plain wedges with dashed wakes
    for (ux, vy) in [(0.13, 0.16), (0.26, 0.07)]:
        dx_, dy_ = x + ux * w_, y + vy * h
        for k in range(4):
            sx = dx_ + k * 12
            d.line([sx, dy_ + 11, sx + 6, dy_ + 11], fill=WHITE, width=2)
        d.polygon([(dx_ + 44, dy_ + 6), (dx_ + 66, dy_ + 11),
                   (dx_ + 44, dy_ + 16)], fill=NAVY)
    f = ar700(11)
    d.text((bx - 32, by + 34), "BENGHAZI", font=f, fill=NAVY_TX)
    d.text((x + 10, y + 7), "MEDITERRANEAN SEA", font=in400(10),
           fill=(70, 96, 90))
    d.text((x + w_ - 52, y + h - 19), "LIBYA", font=ar700(12),
           fill=NAVY_TX)


def scene_iran(d, x, y, w_, h):
    """Teal gulf, sand shores, three navy tankers, rust blockade, clock."""
    d.rectangle([x, y, x + w_, y + h], fill=TEAL_OC)
    d.polygon([(x, y + h), (x, y + 0.52 * h), (x + 0.30 * w_, y + 0.60 * h),
               (x + 0.42 * w_, y + h)], fill=SAND)
    d.polygon([(x + 0.52 * w_, y), (x + w_, y), (x + w_, y + 0.40 * h),
               (x + 0.66 * w_, y + 0.34 * h), (x + 0.55 * w_, y + 0.16 * h)],
              fill=SAND)
    # Kharg Island: one sand ellipse
    kx, ky = x + 0.47 * w_, y + 0.42 * h
    d.ellipse([kx - 14, ky - 8, kx + 14, ky + 8], fill=(198, 172, 112))
    d.text((kx - 25, ky - 26), "KHARG I.", font=ar700(10), fill=NAVY_TX)
    # tanker convoy: three navy hulls heading south-east
    for (ux, vy) in [(0.50, 0.52), (0.58, 0.62), (0.66, 0.72)]:
        tx, ty = x + ux * w_, y + vy * h
        d.polygon([(tx - 18, ty), (tx + 20, ty), (tx + 14, ty + 8),
                   (tx - 12, ty + 8)], fill=NAVY)
        d.rectangle([tx - 8, ty - 6, tx + 6, ty], fill=NAVY)
    # blockade: rust dashes + one slate warship
    for k in range(7):
        sx = x + (0.70 + k * 0.04) * w_
        d.line([sx, y + 0.86 * h, sx + 12, y + 0.86 * h], fill=RUST,
               width=3)
    wx, wy = x + 0.80 * w_, y + 0.90 * h
    d.polygon([(wx - 20, wy), (wx + 22, wy), (wx + 15, wy + 7),
               (wx - 13, wy + 7)], fill=(51, 72, 79))
    d.text((x + 8, y + 7), "PERSIAN GULF", font=in400(10),
           fill=(70, 96, 90))
    d.text((x + w_ - 52, y + 9), "IRAN", font=ar700(12), fill=NAVY_TX)
    # deadline clock badge, bottom-left, clear of every label
    cx, cy, r = x + 28, y + h - 28, 15
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=CREAM_LT,
              outline=RUST, width=3)
    d.line([cx, cy, cx, cy - 9], fill=RUST, width=3)
    d.line([cx, cy, cx + 7, cy + 3], fill=RUST, width=3)
    d.text((cx + r + 5, cy - 13), "NEW YEAR", font=ar700(10), fill=RUST)
    d.text((cx + r + 5, cy + 2), "DEADLINE", font=ar700(10), fill=RUST)


def scene_kyiv(d, x, y, w_, h):
    """Navy night, one sand block with a collapsed corner, floodlight."""
    d.rectangle([x, y, x + w_, y + h], fill=(30, 44, 56))
    for bx, bw, bh in [(0.02, 0.15, 0.52), (0.82, 0.16, 0.58)]:
        d.rectangle([x + bx * w_, y + h - bh * h, x + (bx + bw) * w_,
                     y + h], fill=(44, 60, 72))
    # main block
    bx0, by0, bx1, by1 = x + 0.30 * w_, y + 0.14 * h, x + 0.68 * w_, y + h
    d.rectangle([bx0, by0, bx1, by1], fill=SAND_D)
    # collapsed corner (single jagged bite)
    d.polygon([(bx1 - 50, by0), (bx1, by0), (bx1, by0 + 58),
               (bx1 - 18, by0 + 46), (bx1 - 38, by0 + 64),
               (bx1 - 28, by0 + 30)], fill=(30, 44, 56))
    d.polygon([(bx1 - 50, by0 + 7), (bx1 - 6, by0 + 3), (bx1 - 13, by0 + 50),
               (bx1 - 32, by0 + 56)], fill=(110, 96, 78))
    # window grid: ochre lit, slate dark
    for r_ in range(3):
        for c_ in range(4):
            wx = bx0 + 11 + c_ * 23
            wy = by0 + 9 + r_ * 17
            if wx > bx1 - 56 and r_ < 2:
                continue
            lit = (r_ * 4 + c_) % 3 == 0
            d.rectangle([wx, wy, wx + 11, wy + 11],
                        fill=OCHRE if lit else (70, 86, 98))
    # rubble pile + floodlight beam + three rescuer silhouettes
    d.polygon([(bx0 - 14, y + h), (bx1 + 26, y + h), (bx1 - 28, y + h - 22),
               (bx0 + 28, y + h - 15)], fill=(150, 138, 112))
    lx = x + 0.15 * w_
    d.line([lx, y + h, lx + 5, y + h - 46], fill=NAVY, width=3)
    d.polygon([(lx + 5, y + h - 46), (bx0 + 60, y + h - 26),
               (bx0 + 36, y + h - 6)], fill=(232, 214, 150))
    for fx in (0.44, 0.55, 0.63):
        px = x + fx * w_
        d.ellipse([px - 4, y + h - 30, px + 4, y + h - 22], fill=NAVY)
        d.line([px, y + h - 22, px, y + h - 10], fill=NAVY, width=3)
    lf = in400(10)
    ltxt = "DYMER, NORTH OF KYIV"
    d.text((x + w_ - d.textlength(ltxt, font=lf) - 10, y + 7), ltxt,
           font=lf, fill=(200, 208, 220))


SCENES = {1: scene_benghazi, 2: scene_iran, 3: scene_kyiv}

# ------------------------------------------------------------ world map
# Simplified coastline polygons as (lon, lat) vertices, drawn with a
# linear projection — recognisable continents, honest simplification.
# (Same coastline data as build3.py.)
CONTINENTS = [
    # North America
    [(-168, 66), (-158, 71), (-140, 70), (-125, 71), (-110, 68),
     (-95, 69), (-85, 66), (-82, 62), (-78, 62), (-85, 55), (-90, 51),
     (-95, 49), (-89, 48), (-84, 46), (-76, 44), (-70, 42), (-74, 39),
     (-76, 35), (-80, 32), (-81, 26), (-84, 30), (-89, 30), (-94, 29),
     (-97, 26), (-97, 22), (-94, 18), (-90, 21), (-87, 21), (-86, 16),
     (-83, 9), (-78, 8), (-77, 4), (-80, 9), (-84, 15), (-88, 21),
     (-91, 19), (-97, 16), (-105, 20), (-110, 23), (-114, 29),
     (-117, 33), (-122, 37), (-124, 46), (-130, 55), (-145, 60),
     (-155, 58), (-162, 61)],
    # South America
    [(-77, 4), (-72, 11), (-64, 10), (-52, 5), (-50, 0), (-44, -3),
     (-35, -8), (-39, -13), (-41, -22), (-48, -27), (-53, -33),
     (-58, -38), (-65, -41), (-65, -45), (-67, -50), (-68, -54),
     (-71, -54), (-73, -46), (-73, -37), (-71, -30), (-70, -20),
     (-75, -15), (-79, -8), (-81, -4), (-80, 1)],
    # Africa
    [(-6, 35), (0, 36), (10, 37), (11, 34), (20, 32), (30, 31),
     (32, 30), (35, 28), (38, 22), (40, 15), (43, 12), (48, 11),
     (51, 10), (45, 2), (41, -4), (40, -12), (38, -20), (35, -26),
     (31, -29), (26, -33), (20, -35), (17, -32), (14, -26), (12, -15),
     (13, -8), (9, -2), (9, 4), (4, 6), (-3, 5), (-8, 5), (-13, 8),
     (-17, 12), (-17, 16), (-16, 21), (-13, 28), (-9, 31)],
    # Eurasia
    [(-9, 43), (-2, 44), (-1, 46), (-5, 48), (0, 49), (2, 51), (5, 53),
     (8, 55), (8, 57), (18, 56), (21, 55), (24, 58), (28, 60), (30, 62),
     (28, 66), (32, 70), (45, 68), (60, 69), (75, 72), (90, 72),
     (105, 77), (120, 73), (140, 72), (158, 70), (170, 67), (178, 66),
     (178, 62), (162, 60), (158, 52), (150, 45), (142, 42), (140, 38),
     (135, 35), (129, 33), (122, 31), (120, 26), (114, 23), (108, 18),
     (106, 9), (103, 5), (100, 8), (98, 13), (95, 16), (92, 16),
     (89, 22), (86, 20), (80, 15), (77, 8), (73, 16), (68, 22),
     (66, 25), (61, 25), (57, 26), (52, 28), (50, 29), (49, 30),
     (54, 26), (59, 22), (55, 17), (52, 15), (45, 12), (43, 12),
     (40, 15), (38, 21), (35, 28), (34, 31), (36, 36), (30, 36),
     (27, 37), (23, 36), (22, 38), (19, 40), (15, 38), (12, 44),
     (8, 44), (3, 42), (0, 40), (-2, 37), (-6, 36), (-9, 37),
     (-9, 43)],
    # Indonesia / Papua (simplified)
    [(95, 5), (100, 0), (105, -5), (110, -7), (115, -8), (120, -9),
     (125, -9), (131, -3), (138, -2), (144, -4), (147, -7), (143, -8),
     (136, -5), (130, -4), (124, -10), (117, -10), (110, -10),
     (104, -6), (98, 2)],
    # Australia
    [(114, -22), (114, -30), (115, -34), (118, -35), (124, -33),
     (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
     (145, -38), (147, -38), (150, -37), (153, -31), (153, -27),
     (151, -24), (149, -20), (146, -19), (143, -15), (142, -11),
     (142, -14), (140, -18), (136, -15), (135, -12), (132, -11),
     (130, -12), (126, -14), (122, -17), (118, -20)],
    # Britain
    [(-5, 50), (-3, 53), (-5, 55), (-3, 57), (-1, 57), (0, 54),
     (1, 52), (1, 51), (-2, 50)],
    # Japan (Honshu simplified)
    [(130, 31), (133, 34), (137, 35), (140, 36), (141, 40), (141, 44),
     (140, 42), (139, 38), (136, 35), (132, 33), (130, 32)],
    # New Zealand
    [(167, -46), (170, -44), (173, -42), (174, -41), (176, -38),
     (175, -37), (173, -39), (171, -42), (168, -47)],
    # Madagascar
    [(44, -16), (47, -14), (50, -16), (49, -20), (47, -24), (45, -25),
     (44, -21), (43, -18)],
]


def project(lon, lat, box):
    x0, y0, x1, y1 = box
    px = x0 + (lon + 180) / 360.0 * (x1 - x0)
    py = y0 + (78 - lat) / 140.0 * (y1 - y0)
    return px, py


def draw_map(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=TEAL_OC)
    for poly in CONTINENTS:
        pts = [project(lon, lat, box) for lon, lat in poly]
        d.polygon(pts, fill=SAND, outline=(150, 138, 105))
    for label, lon, lat in [("EUROPE", -2, 63), ("AFRICA", 16, -10),
                            ("ASIA", 88, 46), ("AMERICAS", -100, 44),
                            ("OCEANIA", 150, -27)]:
        px, py = project(lon, lat, box)
        f = ar700(9)
        d.text((px - d.textlength(label, font=f) / 2, py), label,
               font=f, fill=(90, 84, 70))
    # pins with fan-out offsets for clusters: story -> (dx, dy).
    # Offsets are solved so every pin centre lands INSIDE its story's
    # coastline polygon (not in the ocean) and cluster pins stay
    # separated enough for their numbers to read.
    fan = {1: (-5, 5), 2: (-6, -6), 3: (25, -11), 4: (24, -11),
           5: (-4, 6), 6: (14, -4), 7: (37, 8), 8: (9, 22),
           9: (2, 0), 10: (11, 4), 11: (18, 8), 12: (-9, 13),
           13: (0, 0), 14: (-35, 0), 15: (15, -8), 16: (0, -1),
           17: (11, -16), 18: (0, -29), 19: (0, 0), 20: (2, -7),
           21: (12, -5), 22: (2, -8), 23: (-13, 6), 24: (2, 0),
           25: (-2, -2), 26: (-15, -7), 27: (-6, 2), 28: (9, 4),
           29: (0, -3), 30: (-1, 0), 31: (-26, -10), 32: (-5, -13),
           33: (-1, -2), 34: (-43, 16), 35: (22, -2)}
    for s in ALL_STORIES:
        px, py = project(s["pin"][0], s["pin"][1], box)
        dx, dy = fan.get(s["n"], (0, 0))
        cx, cy = px + dx, py + dy
        if dx or dy:
            d.line([px, py, cx, cy], fill=MID, width=1)
        col = REGION_COLORS[s["region"]]
        r = 8.5
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col, outline=NAVY)
        f = ar700(10)
        t = str(s["n"])
        d.text((cx - d.textlength(t, font=f) / 2, cy - 6), t, font=f,
               fill=WHITE)
    d.rectangle(box, outline=NAVY, width=2)

# ------------------------------------------------------------ the page
W = H = 1024
MX = 28
CW = W - 2 * MX


def render():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # ---- navy masthead: kicker, giant date, strap, UTC ticker
    d.rectangle([0, 0, W, 180], fill=NAVY)
    d.line([MX, 10, W - MX, 10], fill=OCHRE, width=2)
    kf = fit_tracked(d, "kicker", "THE WORLD IN ONE DAY", ar700, 13, 10,
                     2, 300)
    draw_tracked(d, MX, 18, "THE WORLD IN ONE DAY", kf, 2, OCHRE)
    right = (f"{N_STORIES} STORIES \u00b7 {N_REGIONS} REGIONS \u00b7 "
             f"EVERY ONE DATED MONDAY 23 NOVEMBER 2026")
    f, t = fit_oneline(d, "masthead right", right, ar700, 11, 8, 640)
    d.text((W - MX - d.textlength(t, font=f), 19), t, font=f, fill=CREAM)
    f, t = fit_oneline(d, "date", "MONDAY 23 NOVEMBER 2026", pf900,
                       84, 40, CW)
    d.text((MX - 2, 36), t, font=f, fill=CREAM)
    d.line([MX, 118, W - MX, 118], fill=(90, 104, 114), width=1)
    strap = ("Kyiv says sea drones sank Russian corvette off Libya \u2022 "
             "Trump sets New Year deadline for Iran \u2022 "
             "Kyiv-region strike toll reaches at least nine")
    f, lines, sz = fit_box(d, "strap", strap, pf_i700, 20, 13, CW, 36,
                           leading=1.05)
    text_block(d, MX, 125, lines, f, sz, leading=1.05, fill=CREAM)
    # UTC ticker inside the masthead (Melbourne text already fixed)
    f = ar700(11)
    d.text((MX, 165), "THE DAY IN UTC", font=f, fill=OCHRE)
    tx = MX + 112
    for when, what in TIMELINE:
        f1 = ar700(12)
        d.text((tx, 164), when, font=f1, fill=OCHRE)
        tx += d.textlength(when, font=f1) + 8
        f2, t2 = fit_oneline(d, f"timeline {when}", what, in400, 12, 8,
                             MX + CW - tx - 6)
        d.text((tx, 164), t2, font=f2, fill=CREAM)
        tx += d.textlength(t2, font=f2) + 26
    d.line([0, 178, W, 178], fill=OCHRE, width=3)

    # ---- stat strip on cream: big navy numerals
    sx = MX
    colw = CW / len(STATS)
    for i, (num, cap) in enumerate(STATS):
        f, t = fit_oneline(d, f"stat {i}", num, pf900, 36, 16, colw - 12)
        d.text((sx + 2, 190), t, font=f, fill=NAVY)
        f2, lines, sz2 = fit_box(d, f"stat cap {i}", cap, bc600, 10, 7,
                                 colw - 12, 24, leading=1.1)
        text_block(d, sx + 2, 230, lines, f2, sz2, leading=1.1, fill=MID)
        if i:
            d.line([sx, 192, sx, 254], fill=HAIR, width=1)
        sx += colw
    d.line([MX, 256, W - MX, 256], fill=NAVY, width=2)

    # ---- region bar
    bx = MX
    total = sum(REGION_COUNTS.values())
    for r in REGION_ORDER:
        n = REGION_COUNTS[r]
        if not n:
            continue
        seg = CW * n / total
        d.rectangle([bx, 262, bx + seg, 284], fill=REGION_COLORS[r])
        label = f"{r.upper()} {n}"
        f = bc600(11 if seg > 92 else 9)
        if seg <= 52:
            f = bc600(8)
        tw = d.textlength(label, font=f)
        if tw <= seg - 4:
            d.text((bx + (seg - tw) / 2, 267 if seg > 52 else 269),
                   label, font=f, fill=WHITE)
        bx += seg
    _register("region bar", CW, CW)

    # ---- 3 lead panels
    ly = 290
    lh = 200
    gap = 12
    pw = (CW - 2 * gap) / 3
    for i, s in enumerate(STORIES[:3]):
        x = MX + i * (pw + gap)
        d.rectangle([x, ly, x + pw, ly + lh], fill=CREAM_LT,
                    outline=HAIR, width=1)
        SCENES[s["n"]](d, x + 6, ly + 6, pw - 12, 58)
        ky = ly + 72
        d.rectangle([x + 10, ky, x + 32, ky + 18],
                    fill=REGION_COLORS[s["region"]])
        nf = ar700(12)
        d.text((x + 21 - d.textlength(str(s["n"]), font=nf) / 2, ky + 2),
               str(s["n"]), font=nf, fill=WHITE)
        pillw = d.textlength(s["tier"], font=ar700(11)) + 12
        kick = f"{s['place']} \u00b7 {s['field']}"
        f, t = fit_oneline(d, f"lead kick {s['n']}", kick, bc600, 11, 8,
                           pw - 48 - pillw)
        d.text((x + 38, ky + 3), t, font=f, fill=MID)
        pill(d, x + pw - 10 - pillw, ky, s["tier"])
        hy = ky + 26
        f, lines, hsz = fit_box(d, f"lead head {s['n']}", s["headline"],
                                pf700, 22, 14, pw - 20, 46, leading=1.06)
        text_block(d, x + 10, hy, lines, f, hsz, leading=1.06)
        head_h = (len(lines) - 1) * 1.06 * hsz + hsz
        by = hy + head_h + 6
        body = s["body"] + f" ({s['source']})"
        f, lines, bsz = fit_box(d, f"lead body {s['n']}", body, in400,
                                12, 9, pw - 20, ly + lh - by - 8,
                                leading=1.18)
        text_block(d, x + 10, by, lines, f, bsz, leading=1.18)

    # ---- card grid: stories 4-15, 4 cols x 3 rows
    cy0 = 498
    ch = 47
    cgap = 5
    cw4 = (CW - 3 * cgap) // 4
    cards = STORIES[3:]
    for idx, s in enumerate(cards):
        cx = MX + (idx % 4) * (cw4 + cgap)
        cyy = cy0 + (idx // 4) * (ch + cgap)
        col = REGION_COLORS[s["region"]]
        d.rectangle([cx, cyy, cx + cw4, cyy + ch], fill=CREAM_LT,
                    outline=HAIR, width=1)
        d.rectangle([cx, cyy, cx + 34, cyy + ch], fill=col)
        nf = ar700(14)
        d.text((cx + 17 - d.textlength(str(s["n"]), font=nf) / 2,
                cyy + 5), str(s["n"]), font=nf, fill=WHITE)
        glyph = {"CONFLICT": "\u2694", "ENERGY": "\u25cf",
                 "SECURITY": "\u25c6", "POLITICS": "\u00a7",
                 "SPORT": "\u2605", "HEALTH": "\u271a",
                 "MARKETS": "\u25b2",
                 "LAW": "\u2696"}.get(s["field"], "\u25aa")
        gf = dsans(13)
        d.text((cx + 17 - d.textlength(glyph, font=gf) / 2, cyy + 29),
               glyph, font=gf, fill=WHITE)
        f, t = fit_oneline(d, f"card fig {s['n']}", s["figure"], pf900,
                           14, 10, cw4 - 48)
        d.text((cx + 42, cyy + 2), t, font=f, fill=col)
        f, lines, hsz = fit_box(d, f"card head {s['n']}", s["headline"],
                                pf700, 10, 8, cw4 - 48, 17, leading=1.08)
        text_block(d, cx + 42, cyy + 18, lines, f, hsz, leading=1.08)
        micro = f"{s['tier']} \u00b7 {s['source']}"
        f, t = fit_oneline(d, f"card micro {s['n']}", micro, ar500, 9, 6,
                           cw4 - 48)
        d.text((cx + 42, cyy + ch - 10), t, font=f, fill=MID)
    cards_bottom = cy0 + 3 * ch + 2 * cgap

    # ---- bottom zone: map (left) + DATE CHECK / legend (right)
    hz = cards_bottom + 10
    f = ar700(12)
    d.text((MX, hz), "WHERE IT HAPPENED \u2014 PINS MATCH STORY NUMBERS",
           font=f, fill=NAVY)
    map_box = (MX, hz + 20, 540, hz + 140)
    draw_map(d, map_box)
    d.text((MX + 6, hz + 126), "Scenes are drawn illustrations, "
           "not photographs", font=in400(8), fill=(70, 96, 90))
    rx = 556
    rw = W - MX - rx
    d.rectangle([rx, hz - 4, W - MX, hz + 86], outline=RUST, width=2)
    d.text((rx + 12, hz + 4), "DATE CHECK \u2014 LEFT OUT ON PURPOSE",
           font=f, fill=RUST)
    f, lines, dsz = fit_box(d, "date check", DATE_CHECK, in400, 11, 8,
                            rw - 24, 56, leading=1.16)
    text_block(d, rx + 12, hz + 24, lines, f, dsz, leading=1.16)
    legend = ("HOW SURE: CONFIRMED = 2+ outlets or the official record "
              "\u00b7 OFFICIAL = authorities' own statement \u00b7 "
              "REPORTED = one source's account \u00b7 CLAIM = one side's "
              "claim, labelled")
    f, lines, lsz = fit_box(d, "legend", legend, in400, 10, 8, rw, 36,
                            leading=1.16)
    text_block(d, rx, hz + 94, lines, f, lsz, leading=1.16)
    honest = ("Full day \u2014 compiled Tuesday, after Monday 23 November "
              "ended in every time zone")
    f, t = fit_oneline(d, "honesty", honest, in400, 9, 6, rw)
    d.text((rx, hz + 142), t, font=f, fill=MID)

    # ---- ALSO ON: two columns, grouped by region, real leading.
    # One uniform pitch for both columns, solved against a fixed
    # bottom limit so the digest ends with a real bottom margin.
    az = hz + 156
    also_title = (f"ALSO ON MONDAY 23 NOVEMBER \u2014 {len(ALSO)} MORE "
                  f"STORIES, GROUPED BY REGION")
    f2, t2 = fit_oneline(d, "also title", also_title, ar700, 12, 9, 700)
    d.text((MX, az), t2, font=f2, fill=NAVY)
    d.line([MX, az + 18, MX + 92, az + 18], fill=OCHRE, width=3)
    by_n = {s["n"]: s for s in ALSO}
    blocks_a = [("ASIA", "Asia", list(range(16, 23))),
                ("AMERICAS", "Americas", list(range(23, 27)))]
    blocks_b = [("AMERICAS (CONT.)", "Americas", list(range(27, 30))),
                ("OCEANIA", "Oceania", list(range(30, 34))),
                ("GLOBAL", "Global", list(range(34, 36)))]
    list_top = az + 28
    list_bottom = 1016
    head_h = 14
    # ONE uniform size for every ALSO item — the size 18 of the 20
    # already fit at. Items too long for one line at this size (17
    # and 20) wrap onto a second line instead of shrinking, so no
    # item on the page renders smaller than its neighbours.
    ALSO_SIZE = 10

    def _also_lines(s, col_w):
        line = f"{s['line']} ({s['source']})"
        return wrap(d, line, in400(ALSO_SIZE), col_w - 26)

    def _pitch(blocks, col_w):
        fixed = head_h * len(blocks)
        n_lines = sum(len(_also_lines(by_n[n], col_w))
                      for _, _, nums in blocks for n in nums)
        return (list_bottom - list_top - fixed) / max(1, n_lines)

    pitch = min(_pitch(blocks_a, 468), _pitch(blocks_b, 472))

    def draw_also_column(x0, col_w, blocks, tag):
        ay = float(list_top)
        fnt = in400(ALSO_SIZE)
        for label, region, nums in blocks:
            hf = ar700(10)
            d.rectangle([x0, ay + 2, x0 + 8, ay + 10],
                        fill=REGION_COLORS[region])
            d.text((x0 + 13, ay + 1), label, font=hf,
                   fill=REGION_COLORS[region])
            ay += head_h
            for n in nums:
                s = by_n[n]
                col = REGION_COLORS[s["region"]]
                d.rectangle([x0, ay, x0 + 20, ay + 12], fill=col)
                nf = ar700(9)
                d.text((x0 + 10 - d.textlength(str(n), font=nf) / 2,
                        ay + 1), str(n), font=nf, fill=WHITE)
                lines = _also_lines(s, col_w)
                widest = max(d.textlength(ln, font=fnt) for ln in lines)
                _register(f"also {n}", widest, col_w - 26)
                for j, ln in enumerate(lines):
                    d.text((x0 + 26, ay + 1 + j * pitch), ln, font=fnt,
                           fill=NAVY_TX)
                ay += pitch * len(lines)
        _register(f"also list {tag}", ay, list_bottom)
        return ay

    draw_also_column(MX, 468, blocks_a, "A")
    draw_also_column(524, 472, blocks_b, "B")

    img.save(OUT)
    img.resize((300, 300), Image.LANCZOS).save(OUT300)
    return img


if __name__ == "__main__":
    render()
    report_checks()
    size = os.path.getsize(OUT)
    with Image.open(OUT) as im:
        dims = im.size
    print(f"entry-v4.png: {dims[0]}x{dims[1]}, {size} bytes "
          f"({size / 1048576:.3f} MiB)")
    assert dims == (1024, 1024), dims
    assert size <= 1048576, size
    print(f"stories on page: {N_STORIES}; regions: "
          + ", ".join(f"{r} {REGION_COUNTS[r]}" for r in REGION_ORDER
                      if REGION_COUNTS[r]))
