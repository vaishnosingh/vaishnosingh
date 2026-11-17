#!/usr/bin/env python3
"""
Generates assets/skyline.svg (3D contribution skyline) and assets/stats.svg from live GitHub data.
Usage: GH_LOGIN=you GH_TOKEN=... python scripts/profile_stats.py
"""
import os, sys, json, html, urllib.request

LOGIN = os.environ.get("GH_LOGIN", "vaishnosingh")
TOKEN = os.environ.get("GH_TOKEN", "")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Inter', Roboto, sans-serif"
MONO = "'JetBrains Mono', 'SFMono-Regular', Menlo, Monaco, Consolas, monospace"

# Sleek 3D Slate & Electric Accent Palette
C_CANVAS = "#0B0F19"
C_PANEL = "#0F172A"
C_PANEL_ALT = "#131C31"
C_BORDER = "#1E293B"
C_BORDER_LIGHT = "rgba(255, 255, 255, 0.12)"
C_TEXT_WHITE = "#F8FAFC"
C_TEXT_MUTED = "#94A3B8"
C_TEXT_DIM = "#64748B"

# Accents
C_CYAN = "#06B6D4"
C_INDIGO = "#6366F1"
C_EMERALD = "#10B981"
C_AMBER = "#F59E0B"
C_SKY = "#38BDF8"

esc = lambda s: html.escape(str(s), quote=False)

def shade(h, f):
    h = h.lstrip('#')
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(int(h[i:i+2], 16) * f))) for i in (0, 2, 4))

QUERY = """query($login:String!){
  user(login:$login){
    followers{totalCount}
    repositories(ownerAffiliations:OWNER,isFork:false,first:100,orderBy:{field:PUSHED_AT,direction:DESC}){
      nodes{
        stargazerCount
        languages(first:8,orderBy:{field:SIZE,direction:DESC}){
          edges{size node{name color}}
        }
      }
    }
    contributionsCollection{
      totalCommitContributions
      totalIssueContributions
      totalPullRequestContributions
      contributionCalendar{
        totalContributions
        weeks{contributionDays{contributionCount weekday}}
      }
    }
  }
}"""

def fetch():
    if not TOKEN:
        return None
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
        headers={
            "Authorization": f"bearer {TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": "profile-stats"
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.load(resp)
            if data.get("errors"):
                print("GraphQL Errors:", data["errors"], file=sys.stderr)
                return None
            return data["data"]["user"]
    except Exception as e:
        print(f"Fetch error: {e}", file=sys.stderr)
        return None

def digest(u):
    if not u:
        return None
    cc = u["contributionsCollection"]
    cal = cc["contributionCalendar"]
    days = [(wi, d["weekday"], d["contributionCount"]) for wi, w in enumerate(cal["weeks"]) for d in w["contributionDays"]]
    seq = [c for _, _, c in days]
    longest = run = 0
    for c in seq:
        run = run + 1 if c > 0 else 0
        longest = max(longest, run)
    rev = seq[::-1]
    i = 1 if rev and rev[0] == 0 else 0
    cur = 0
    while i < len(rev) and rev[i] > 0:
        cur += 1
        i += 1
    langs = {}
    for r in u["repositories"]["nodes"]:
        for e in r["languages"]["edges"]:
            n = e["node"]
            l = langs.setdefault(n["name"], [0, n["color"] or "#64748B"])
            l[0] += e["size"]
    return {
        "days": days,
        "total": cal["totalContributions"],
        "cur": cur,
        "longest": longest,
        "commits": cc["totalCommitContributions"],
        "prs": cc["totalPullRequestContributions"],
        "issues": cc["totalIssueContributions"],
        "stars": sum(r["stargazerCount"] for r in u["repositories"]["nodes"]),
        "followers": u["followers"]["totalCount"],
        "langs": langs
    }

def wrap_svg(W, H, title, content):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{esc(title)}">
  <title>{esc(title)}</title>
  <defs>
    <linearGradient id="cardBg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0E1322"/>
      <stop offset="100%" stop-color="#080B12"/>
    </linearGradient>
    <linearGradient id="topBevel" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#38BDF8" stop-opacity="0.5"/>
      <stop offset="30%" stop-color="#818CF8" stop-opacity="0.3"/>
      <stop offset="70%" stop-color="#6366F1" stop-opacity="0.1"/>
      <stop offset="100%" stop-color="#06B6D4" stop-opacity="0.4"/>
    </linearGradient>
    <linearGradient id="gridGlow" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1E293B" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#0F172A" stop-opacity="0.4"/>
    </linearGradient>
    <radialGradient id="ambientLight" cx="50%" cy="0%" r="70%">
      <stop offset="0%" stop-color="#1E293B" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="#080B12" stop-opacity="0"/>
    </radialGradient>
    <filter id="tileDropShadow" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000000" flood-opacity="0.4"/>
    </filter>
  </defs>

  <!-- Outer Card Frame -->
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="18" fill="url(#cardBg)" stroke="{C_BORDER}" stroke-width="1"/>
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="17" fill="url(#ambientLight)"/>
  <!-- 3D Specular Top Rim -->
  <path d="M 18,1 L {W-18},1" stroke="url(#topBevel)" stroke-width="1.5" stroke-linecap="round"/>

  {content}
</svg>"""

LV_COLORS = ["#172033", "#0284C7", "#06B6D4", "#6366F1", "#A855F7"]

def skyline(D):
    W, H = 1000, 470
    # Isometric grid projection vectors
    ux, uy = 15.2, 2.7
    vx, vy = 7.4, -9.0
    ox, oy = 76, 296

    P = lambda w, d: (ox + w * ux + d * vx, oy + w * uy + d * vy)
    pt = lambda p: f"{p[0]:.1f},{p[1]:.1f}"

    days = D["days"] if D else [(w, d, 0) for w in range(53) for d in range(7)]
    m = max([c for _, _, c in days] + [1])

    # 3D Base Plate
    t = 12
    c = [P(-0.5, -0.5), P(53.5, -0.5), P(53.5, 7.5), P(-0.5, 7.5)]
    plate = ""
    # Side walls of the 3D base plate
    plate += f'<polygon points="{pt(c[3])} {pt(c[2])} {pt((c[2][0], c[2][1]+t))} {pt((c[3][0], c[3][1]+t))}" fill="#0A0F1D" stroke="#1E293B" stroke-width="0.5"/>'
    plate += f'<polygon points="{pt(c[0])} {pt(c[3])} {pt((c[3][0], c[3][1]+t))} {pt((c[0][0], c[0][1]+t))}" fill="#0F172A" stroke="#1E293B" stroke-width="0.5"/>'
    plate += f'<polygon points="{pt(c[1])} {pt(c[2])} {pt((c[2][0], c[2][1]+t))} {pt((c[1][0], c[1][1]+t))}" fill="#080C17" stroke="#1E293B" stroke-width="0.5"/>'
    # Top surface of the 3D base plate
    plate += f'<polygon points="{" ".join(pt(p) for p in c)}" fill="#11192C" stroke="#1E293B" stroke-width="1"/>'

    # Draw isometric grid accent lines
    grid_lines = ""
    for w_step in range(0, 54, 8):
        p1 = P(w_step, -0.5)
        p2 = P(w_step, 7.5)
        grid_lines += f'<line x1="{p1[0]:.1f}" y1="{p1[1]:.1f}" x2="{p2[0]:.1f}" y2="{p2[1]:.1f}" stroke="rgba(255,255,255,0.03)" stroke-width="1"/>'

    # Render columns sorted back-to-front for proper isometric overlap
    bars = ""
    for w, d, n in sorted(days, key=lambda x: (-x[1], x[0])):
        if n == 0:
            lv = 0
            col = LV_COLORS[0]
            h = 2.5
        else:
            lv = min(4, max(1, 1 + int((n / m) * 3.99)))
            col = LV_COLORS[lv]
            h = 6 + (n / m)**0.72 * 125

        a, b, cc, dd = P(w + 0.12, d + 0.12), P(w + 0.88, d + 0.12), P(w + 0.88, d + 0.88), P(w + 0.12, d + 0.88)
        up = lambda p: (p[0], p[1] - h)

        # 3D block faces: Top, Front, Right
        top_face = f'<polygon points="{pt(up(a))} {pt(up(b))} {pt(up(cc))} {pt(up(dd))}" fill="{col}"/>'
        front_face = f'<polygon points="{pt(a)} {pt(b)} {pt(up(b))} {pt(up(a))}" fill="{shade(col, 0.72)}"/>'
        side_face = f'<polygon points="{pt(b)} {pt(cc)} {pt(up(cc))} {pt(up(b))}" fill="{shade(col, 0.50)}"/>'

        bars += top_face + front_face + side_face

    tot = f'{D["total"]:,}' if D else "—"

    # Header & Meta elements
    header = f"""
  <!-- Header Info -->
  <g transform="translate(36, 32)">
    <rect x="0" y="0" width="168" height="24" rx="12" fill="#1E293B" fill-opacity="0.6" stroke="#334155" stroke-width="0.8"/>
    <circle cx="12" cy="12" r="4" fill="#10B981"/>
    <text x="24" y="16" font-family="{MONO}" font-size="10" font-weight="600" fill="#E2E8F0" letter-spacing="0.5">3D CONTRIBUTION GRID</text>
    
    <text x="0" y="54" font-family="{SANS}" font-size="24" font-weight="800" fill="{C_TEXT_WHITE}" letter-spacing="-0.5">Annual Engineering Activity</text>
    <text x="0" y="76" font-family="{SANS}" font-size="13" font-weight="400" fill="{C_TEXT_MUTED}"><tspan font-weight="600" fill="{C_CYAN}">{tot}</tspan> verified contributions across git repositories in the last year</text>
  </g>

  <!-- Legend -->
  <g transform="translate(730, 44)">
    <text x="0" y="14" font-family="{SANS}" font-size="11" fill="{C_TEXT_DIM}" font-weight="500">Less</text>
    <rect x="32" y="4" width="12" height="12" rx="3" fill="{LV_COLORS[0]}" stroke="#334155" stroke-width="0.5"/>
    <rect x="50" y="4" width="12" height="12" rx="3" fill="{LV_COLORS[1]}"/>
    <rect x="68" y="4" width="12" height="12" rx="3" fill="{LV_COLORS[2]}"/>
    <rect x="86" y="4" width="12" height="12" rx="3" fill="{LV_COLORS[3]}"/>
    <rect x="104" y="4" width="12" height="12" rx="3" fill="{LV_COLORS[4]}"/>
    <text x="124" y="14" font-family="{SANS}" font-size="11" fill="{C_TEXT_DIM}" font-weight="500">More</text>
  </g>
"""
    content = header + f'<g>{plate}{grid_lines}{bars}</g>'
    return wrap_svg(W, H, "3D Contribution Skyline", content)

def stats(D):
    W, H = 1000, 360
    f = lambda k: f'{D[k]:,}' if D else "—"

    # 8 Key Performance Indicators
    metrics = [
        ("TOTAL CONTRIBUTIONS", "total", C_CYAN),
        ("COMMITS PUSHED", "commits", C_INDIGO),
        ("PULL REQUESTS", "prs", C_EMERALD),
        ("ISSUES RESOLVED", "issues", C_SKY),
        ("ACTIVE STREAK", "cur", C_CYAN),
        ("LONGEST STREAK", "longest", C_INDIGO),
        ("STARS EARNED", "stars", C_AMBER),
        ("COMMUNITY FOLLOWERS", "followers", C_EMERALD)
    ]

    tiles = ""
    for i, (label, key, col) in enumerate(metrics):
        col_idx = i % 4
        row_idx = i // 4
        x = 36 + col_idx * 236
        y = 34 + row_idx * 102

        unit = " days" if "STREAK" in label and D and D[key] > 0 else ""
        val = f(key) + unit

        tiles += f"""
    <!-- Stat Tile {i+1} -->
    <g transform="translate({x}, {y})" filter="url(#tileDropShadow)">
      <rect width="220" height="88" rx="12" fill="#111827" stroke="#1F2937" stroke-width="1"/>
      <rect x="1" y="1" width="218" height="1" rx="0.5" fill="rgba(255,255,255,0.08)"/>
      <rect x="0" y="24" width="3.5" height="40" rx="1.75" fill="{col}"/>
      <text x="18" y="48" font-family="{SANS}" font-size="28" font-weight="800" fill="{C_TEXT_WHITE}" letter-spacing="-0.5">{val}</text>
      <text x="18" y="70" font-family="{MONO}" font-size="10.5" font-weight="600" fill="{C_TEXT_MUTED}" letter-spacing="0.5">{label}</text>
    </g>"""

    # Languages Bar Section
    lang_section = f"""
  <g transform="translate(36, 256)">
    <text x="0" y="14" font-family="{MONO}" font-size="11" font-weight="600" fill="{C_TEXT_MUTED}" letter-spacing="1">CORE CODEBASE LANGUAGES</text>
"""

    langs = sorted(D["langs"].items(), key=lambda kv: -kv[1][0])[:6] if D else []
    total_size = sum(v[0] for _, v in langs) or 1

    bar_width = 928
    bar_height = 10
    bar_elements = ""
    legend_elements = ""

    if langs:
        cur_x = 0
        for name, (size, color) in langs:
            segment_w = (size / total_size) * bar_width
            if segment_w < 3:
                segment_w = 3
            bar_elements += f'<rect x="{cur_x:.1f}" y="26" width="{segment_w:.1f}" height="{bar_height}" rx="3" fill="{color}"/>'
            cur_x += segment_w + 2

        for i, (name, (size, color)) in enumerate(langs):
            pct = (size / total_size) * 100
            leg_x = (i % 3) * 310
            leg_y = 56 + (i // 3) * 22
            legend_elements += f"""
      <circle cx="{leg_x + 5}" cy="{leg_y - 4}" r="4.5" fill="{color}"/>
      <text x="{leg_x + 16}" y="{leg_y}" font-family="{SANS}" font-size="12" font-weight="500" fill="{C_TEXT_WHITE}">{esc(name)} <tspan font-family="{MONO}" font-size="11" fill="{C_TEXT_DIM}">{pct:.1f}%</tspan></text>"""
    else:
        bar_elements = f'<rect x="0" y="26" width="{bar_width}" height="{bar_height}" rx="5" fill="#1E293B"/>'
        legend_elements = f'<text x="0" y="56" font-family="{SANS}" font-size="12" fill="{C_TEXT_MUTED}">Analyzing repository code distribution...</text>'

    lang_section += bar_elements + legend_elements + "\n  </g>"

    content = f"""
  <g>
    {tiles}
    {lang_section}
  </g>
"""
    return wrap_svg(W, H, "Developer Metrics & Performance", content)

if __name__ == "__main__":
    data_user = fetch()
    D = digest(data_user)
    os.makedirs(OUT, exist_ok=True)
    
    sky_svg = skyline(D)
    stats_svg = stats(D)
    
    with open(os.path.join(OUT, "skyline.svg"), "w", encoding="utf-8") as f:
        f.write(sky_svg)
    with open(os.path.join(OUT, "stats.svg"), "w", encoding="utf-8") as f:
        f.write(stats_svg)
        
    print("Successfully generated assets/skyline.svg and assets/stats.svg")
