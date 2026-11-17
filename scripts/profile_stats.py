import os
import json
import urllib.request
import datetime

USERNAME = os.getenv("GITHUB_REPOSITORY_OWNER", "vaishnosingh")
TOKEN = os.getenv("GITHUB_TOKEN", "")
ASSETS_DIR = "assets"

os.makedirs(ASSETS_DIR, exist_ok=True)


def fetch_github_stats():
    headers = {"User-Agent": "VaishnoSingh-Profile-Engine"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"

    stats = {
        "public_repos": 0,
        "followers": 0,
        "stars": 0,
        "forks": 0,
        "total_commits": 0,
        "languages": {"Backend / APIs": 42, "Python / FastAPI": 28, "Java / Spring": 18, "IoT / ESP32 C++": 12},
    }

    try:
        req = urllib.request.Request(f"https://api.github.com/users/{USERNAME}", headers=headers)
        with urllib.request.urlopen(req, timeout=10) as res:
            user_data = json.loads(res.read().decode())
            stats["public_repos"] = user_data.get("public_repos", 0)
            stats["followers"] = user_data.get("followers", 0)

        req_repos = urllib.request.Request(
            f"https://api.github.com/users/{USERNAME}/repos?per_page=100&type=owner", headers=headers
        )
        with urllib.request.urlopen(req_repos, timeout=10) as res:
            repos = json.loads(res.read().decode())
            lang_bytes = {}
            for r in repos:
                stats["stars"] += r.get("stargazers_count", 0)
                stats["forks"] += r.get("forks_count", 0)
                lang = r.get("language")
                if lang:
                    lang_bytes[lang] = lang_bytes.get(lang, 0) + r.get("size", 1)

            if lang_bytes:
                total_size = sum(lang_bytes.values()) or 1
                top_langs = sorted(lang_bytes.items(), key=lambda x: x[1], reverse=True)[:5]
                stats["languages"] = {k: max(5, round((v / total_size) * 100)) for k, v in top_langs}
    except Exception as e:
        print(f"Using fallback telemetry: {e}")

    return stats


def write_svg(filename, content):
    with open(os.path.join(ASSETS_DIR, filename), "w", encoding="utf-8") as f:
        f.write(content.strip())


def build_section_header(filename, tag, title, subtitle):
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 70" width="100%">
  <defs>
    <linearGradient id="hGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#06b6d4" stop-opacity="0.25"/>
      <stop offset="40%" stop-color="#6366f1" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#090d16" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="lineGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#06b6d4"/>
      <stop offset="50%" stop-color="#6366f1"/>
      <stop offset="100%" stop-color="#090d16" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect width="900" height="70" rx="10" fill="#090d16"/>
  <rect x="1" y="1" width="898" height="68" rx="9" fill="url(#hGrad)" stroke="#1e293b" stroke-width="1"/>
  <rect x="0" y="12" width="4" height="46" rx="2" fill="#06b6d4"/>
  <text x="24" y="28" fill="#06b6d4" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="700" letter-spacing="2">[{tag}]</text>
  <text x="24" y="52" fill="#f8fafc" font-family="'Inter', -apple-system, sans-serif" font-size="20" font-weight="800" letter-spacing="0.5">{title}</text>
  <text x="875" y="46" text-anchor="end" fill="#64748b" font-family="'JetBrains Mono', monospace" font-size="11">{subtitle}</text>
  <rect x="24" y="64" width="850" height="1.5" fill="url(#lineGrad)"/>
</svg>"""
    write_svg(filename, svg)


def build_hero():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 280" width="100%">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#060911"/>
      <stop offset="50%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#090d16"/>
    </linearGradient>
    <linearGradient id="accent" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#06b6d4"/>
      <stop offset="50%" stop-color="#38bdf8"/>
      <stop offset="100%" stop-color="#818cf8"/>
    </linearGradient>
    <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">
      <path d="M 32 0 L 0 0 0 32" fill="none" stroke="#1e293b" stroke-width="0.6" stroke-dasharray="2,2"/>
    </pattern>
    <style>
      .pulse { animation: pulse 3s infinite ease-in-out; }
      .scan { animation: scan 6s infinite linear; }
      @keyframes pulse { 0%, 100% { opacity: 0.35; } 50% { opacity: 0.95; } }
      @keyframes scan { 0% { transform: translateY(-280px); } 100% { transform: translateY(280px); } }
    </style>
  </defs>

  <rect width="900" height="280" rx="16" fill="url(#bg)" stroke="#1e293b" stroke-width="1.5"/>
  <rect width="900" height="280" rx="16" fill="url(#grid)" opacity="0.45"/>

  <!-- Glowing Ambient Orbs -->
  <circle cx="780" cy="70" r="110" fill="#06b6d4" opacity="0.08" class="pulse"/>
  <circle cx="140" cy="220" r="130" fill="#6366f1" opacity="0.08" class="pulse"/>

  <!-- Top Telemetry Bar -->
  <rect x="28" y="22" width="844" height="30" rx="6" fill="#090d16" opacity="0.8" stroke="#1e293b" stroke-width="1"/>
  <circle cx="46" cy="37" r="5" fill="#ef4444"/>
  <circle cx="64" cy="37" r="5" fill="#f59e0b"/>
  <circle cx="82" cy="37" r="5" fill="#10b981"/>
  <text x="105" y="41" fill="#64748b" font-family="'JetBrains Mono', monospace" font-size="11">root@vaishnosingh-cluster:~# systemctl status architecture.service</text>
  <circle cx="850" cy="37" r="4" fill="#10b981" class="pulse"/>
  <text x="838" y="41" text-anchor="end" fill="#10b981" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="700">ONLINE</text>

  <!-- Main Identity -->
  <text x="45" y="102" fill="#06b6d4" font-family="'JetBrains Mono', monospace" font-size="13" font-weight="600" letter-spacing="3">// SYSTEM ARCHITECT &amp; BACKEND ENGINEER</text>
  <text x="45" y="156" fill="#ffffff" font-family="'Inter', -apple-system, sans-serif" font-size="46" font-weight="900" letter-spacing="1">VAISHNO K SINGH</text>
  <rect x="45" y="172" width="440" height="3" rx="1.5" fill="url(#accent)"/>

  <text x="45" y="206" fill="#94a3b8" font-family="'Inter', -apple-system, sans-serif" font-size="15">
    Engineering fault-tolerant distributed backends, low-latency APIs, and intelligent ESP32 edge IoT systems.
  </text>

  <!-- Bottom HUD Pills -->
  <g transform="translate(45, 226)">
    <rect width="195" height="30" rx="6" fill="#0f172a" stroke="#06b6d4" stroke-width="1"/>
    <text x="97" y="19" text-anchor="middle" fill="#38bdf8" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="600">⚡ HIGH-CONCURRENCY APIs</text>
  </g>
  <g transform="translate(252, 226)">
    <rect width="195" height="30" rx="6" fill="#0f172a" stroke="#6366f1" stroke-width="1"/>
    <text x="97" y="19" text-anchor="middle" fill="#818cf8" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="600">☁️ CLOUD MICROSERVICES</text>
  </g>
  <g transform="translate(459, 226)">
    <rect width="195" height="30" rx="6" fill="#0f172a" stroke="#10b981" stroke-width="1"/>
    <text x="97" y="19" text-anchor="middle" fill="#34d399" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="600">🔌 EDGE IoT &amp; HARDWARE</text>
  </g>
</svg>"""
    write_svg("hero.svg", svg)


def build_about():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 250" width="100%">
  <rect width="900" height="250" rx="14" fill="#090d16" stroke="#1e293b" stroke-width="1.5"/>
  
  <!-- Left Column: YAML Terminal -->
  <rect x="20" y="20" width="480" height="210" rx="10" fill="#0d131f" stroke="#1e293b" stroke-width="1"/>
  <text x="38" y="46" fill="#64748b" font-family="'JetBrains Mono', monospace" font-size="11"># /etc/vaishno/telemetry.yaml</text>

  <text x="38" y="74" fill="#38bdf8" font-family="'JetBrains Mono', monospace" font-size="12.5" font-weight="700">engineer:</text>
  <text x="54" y="96" fill="#94a3b8" font-family="'JetBrains Mono', monospace" font-size="12">role: <tspan fill="#a7f3d0">"Backend Software Developer"</tspan></text>
  <text x="54" y="116" fill="#94a3b8" font-family="'JetBrains Mono', monospace" font-size="12">base: <tspan fill="#a7f3d0">"New Delhi, India"</tspan></text>

  <text x="38" y="146" fill="#38bdf8" font-family="'JetBrains Mono', monospace" font-size="12.5" font-weight="700">core_domains:</text>
  <text x="54" y="168" fill="#cbd5e1" font-family="'JetBrains Mono', monospace" font-size="12">- Distributed Systems &amp; Event-Driven Pipelines</text>
  <text x="54" y="188" fill="#cbd5e1" font-family="'JetBrains Mono', monospace" font-size="12">- Database Indexing, Caching &amp; Query Tuning</text>
  <text x="54" y="208" fill="#cbd5e1" font-family="'JetBrains Mono', monospace" font-size="12">- Smart Home &amp; Edge Sensor Automation (ESP32)</text>

  <!-- Right Column: Engineering Architecture Pillars -->
  <g transform="translate(520, 20)">
    <rect width="360" height="62" rx="10" fill="#0d131f" stroke="#1e293b" stroke-width="1"/>
    <rect x="0" y="14" width="4" height="34" rx="2" fill="#06b6d4"/>
    <text x="20" y="28" fill="#f8fafc" font-family="'Inter', sans-serif" font-size="13.5" font-weight="700">01 // Low-Latency Backend Design</text>
    <text x="20" y="47" fill="#64748b" font-family="'Inter', sans-serif" font-size="11.5">Clean REST/gRPC contracts, async workers &amp; Redis caching</text>
  </g>

  <g transform="translate(520, 94)">
    <rect width="360" height="62" rx="10" fill="#0d131f" stroke="#1e293b" stroke-width="1"/>
    <rect x="0" y="14" width="4" height="34" rx="2" fill="#6366f1"/>
    <text x="20" y="28" fill="#f8fafc" font-family="'Inter', sans-serif" font-size="13.5" font-weight="700">02 // Resilient Data Infrastructure</text>
    <text x="20" y="47" fill="#64748b" font-family="'Inter', sans-serif" font-size="11.5">PostgreSQL, MongoDB, Kafka streams &amp; containerized CI/CD</text>
  </g>

  <g transform="translate(520, 168)">
    <rect width="360" height="62" rx="10" fill="#0d131f" stroke="#1e293b" stroke-width="1"/>
    <rect x="0" y="14" width="4" height="34" rx="2" fill="#10b981"/>
    <text x="20" y="28" fill="#f8fafc" font-family="'Inter', sans-serif" font-size="13.5" font-weight="700">03 // Full-Spectrum Hardware Integration</text>
    <text x="20" y="47" fill="#64748b" font-family="'Inter', sans-serif" font-size="11.5">Bridging physical relays, power monitors &amp; cloud dashboards</text>
  </g>
</svg>"""
    write_svg("about.svg", svg)


def build_orbit():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 300" width="100%">
  <defs>
    <style>
      .orbit-cw { transform-origin: 230px 150px; animation: spinCW 28s linear infinite; }
      .orbit-ccw { transform-origin: 230px 150px; animation: spinCCW 20s linear infinite; }
      @keyframes spinCW { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
      @keyframes spinCCW { from { transform: rotate(360deg); } to { transform: rotate(0deg); } }
    </style>
  </defs>
  <rect width="900" height="300" rx="14" fill="#090d16" stroke="#1e293b" stroke-width="1.5"/>

  <!-- Left Animated Orbital Core -->
  <circle cx="230" cy="150" r="115" fill="none" stroke="#1e293b" stroke-width="1.5" stroke-dasharray="6,6"/>
  <circle cx="230" cy="150" r="72" fill="none" stroke="#1e293b" stroke-width="1.5"/>
  
  <!-- Core Node -->
  <circle cx="230" cy="150" r="34" fill="#0f172a" stroke="#06b6d4" stroke-width="2"/>
  <text x="230" y="147" text-anchor="middle" fill="#06b6d4" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="700">CORE</text>
  <text x="230" y="161" text-anchor="middle" fill="#f8fafc" font-family="'JetBrains Mono', monospace" font-size="9">ENGINE</text>

  <!-- Outer Orbiting Nodes -->
  <g class="orbit-cw">
    <circle cx="230" cy="35" r="18" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5"/>
    <text x="230" y="39" text-anchor="middle" fill="#38bdf8" font-family="monospace" font-size="9" font-weight="700">API</text>
    <circle cx="345" cy="150" r="18" fill="#0f172a" stroke="#818cf8" stroke-width="1.5"/>
    <text x="345" y="154" text-anchor="middle" fill="#818cf8" font-family="monospace" font-size="9" font-weight="700">SQL</text>
    <circle cx="230" cy="265" r="18" fill="#0f172a" stroke="#34d399" stroke-width="1.5"/>
    <text x="230" y="269" text-anchor="middle" fill="#34d399" font-family="monospace" font-size="9" font-weight="700">IoT</text>
    <circle cx="115" cy="150" r="18" fill="#0f172a" stroke="#f472b6" stroke-width="1.5"/>
    <text x="115" y="154" text-anchor="middle" fill="#f472b6" font-family="monospace" font-size="9" font-weight="700">K8S</text>
  </g>

  <!-- Inner Orbiting Nodes -->
  <g class="orbit-ccw">
    <circle cx="281" cy="99" r="13" fill="#0f172a" stroke="#f59e0b" stroke-width="1.5"/>
    <circle cx="179" cy="201" r="13" fill="#0f172a" stroke="#06b6d4" stroke-width="1.5"/>
  </g>

  <!-- Right Matrix Stack Cards -->
  <g transform="translate(420, 24)">
    <rect width="450" height="56" rx="8" fill="#0d131f" stroke="#1e293b"/>
    <text x="18" y="24" fill="#06b6d4" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="700">LANGUAGES &amp; RUNTIMES</text>
    <text x="18" y="44" fill="#e2e8f0" font-family="'Inter', sans-serif" font-size="13" font-weight="600">Java • Python • TypeScript • JavaScript (Node.js) • C/C++ • SQL</text>
  </g>

  <g transform="translate(420, 92)">
    <rect width="450" height="56" rx="8" fill="#0d131f" stroke="#1e293b"/>
    <text x="18" y="24" fill="#818cf8" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="700">FRAMEWORKS &amp; SERVICES</text>
    <text x="18" y="44" fill="#e2e8f0" font-family="'Inter', sans-serif" font-size="13" font-weight="600">Spring Boot • FastAPI • Express.js • REST • GraphQL • Microservices</text>
  </g>

  <g transform="translate(420, 160)">
    <rect width="450" height="56" rx="8" fill="#0d131f" stroke="#1e293b"/>
    <text x="18" y="24" fill="#34d399" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="700">DATA STORES, MESSAGING &amp; INFRA</text>
    <text x="18" y="44" fill="#e2e8f0" font-family="'Inter', sans-serif" font-size="13" font-weight="600">PostgreSQL • MongoDB • Redis • Kafka • Docker • AWS • Linux</text>
  </g>

  <g transform="translate(420, 228)">
    <rect width="450" height="50" rx="8" fill="#0d131f" stroke="#1e293b"/>
    <text x="18" y="21" fill="#f59e0b" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="700">EDGE HARDWARE &amp; AUTOMATION</text>
    <text x="18" y="39" fill="#e2e8f0" font-family="'Inter', sans-serif" font-size="13" font-weight="600">ESP32 / ESP8266 • MQTT • PZEM Power Telemetry • Smart Relays</text>
  </g>
</svg>"""
    write_svg("orbit.svg", svg)


def build_stats(stats):
    now_str = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    langs = list(stats["languages"].items())[:4]

    bars_svg = ""
    colors = ["#06b6d4", "#6366f1", "#10b981", "#f59e0b"]
    for idx, (lang, pct) in enumerate(langs):
        y = 75 + idx * 42
        bar_w = int((pct / 100.0) * 360)
        color = colors[idx % len(colors)]
        bars_svg += f"""
        <text x="480" y="{y}" fill="#e2e8f0" font-family="'JetBrains Mono', monospace" font-size="12">{lang}</text>
        <text x="860" y="{y}" text-anchor="end" fill="{color}" font-family="'JetBrains Mono', monospace" font-size="12" font-weight="700">{pct}%</text>
        <rect x="480" y="{y+8}" width="380" height="8" rx="4" fill="#1e293b"/>
        <rect x="480" y="{y+8}" width="{bar_w}" height="8" rx="4" fill="{color}"/>
        """

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 250" width="100%">
  <rect width="900" height="250" rx="14" fill="#090d16" stroke="#1e293b" stroke-width="1.5"/>

  <!-- Left 2x2 Metric Grid -->
  <g transform="translate(24, 24)">
    <rect width="205" height="92" rx="10" fill="#0d131f" stroke="#1e293b"/>
    <text x="20" y="32" fill="#64748b" font-family="'JetBrains Mono', monospace" font-size="11">PUBLIC REPOSITORIES</text>
    <text x="20" y="72" fill="#06b6d4" font-family="'Inter', sans-serif" font-size="34" font-weight="800">{stats["public_repos"]}</text>
  </g>

  <g transform="translate(245, 24)">
    <rect width="205" height="92" rx="10" fill="#0d131f" stroke="#1e293b"/>
    <text x="20" y="32" fill="#64748b" font-family="'JetBrains Mono', monospace" font-size="11">TOTAL STARS EARNED</text>
    <text x="20" y="72" fill="#818cf8" font-family="'Inter', sans-serif" font-size="34" font-weight="800">{stats["stars"]}</text>
  </g>

  <g transform="translate(24, 132)">
    <rect width="205" height="92" rx="10" fill="#0d131f" stroke="#1e293b"/>
    <text x="20" y="32" fill="#64748b" font-family="'JetBrains Mono', monospace" font-size="11">NETWORK FOLLOWERS</text>
    <text x="20" y="72" fill="#10b981" font-family="'Inter', sans-serif" font-size="34" font-weight="800">{stats["followers"]}</text>
  </g>

  <g transform="translate(245, 132)">
    <rect width="205" height="92" rx="10" fill="#0d131f" stroke="#1e293b"/>
    <text x="20" y="32" fill="#64748b" font-family="'JetBrains Mono', monospace" font-size="11">REPOSITORY FORKS</text>
    <text x="20" y="72" fill="#f59e0b" font-family="'Inter', sans-serif" font-size="34" font-weight="800">{stats["forks"]}</text>
  </g>

  <!-- Right Language Telemetry Bars -->
  <text x="480" y="42" fill="#94a3b8" font-family="'JetBrains Mono', monospace" font-size="12" font-weight="700">CODEBASE DISTRIBUTION // LIVE TELEMETRY</text>
  {bars_svg}
  <text x="860" y="236" text-anchor="end" fill="#475569" font-family="'JetBrains Mono', monospace" font-size="10">Last Synced: {now_str}</text>
</svg>"""
    write_svg("stats.svg", svg)


def build_skyline():
    bars = ""
    heights = [28, 45, 62, 38, 80, 95, 52, 70, 110, 88, 64, 92, 120, 74, 58, 104, 86, 115, 72, 96, 68, 84, 108, 60, 90, 118, 76, 64]
    for i, h in enumerate(heights):
        x = 38 + i * 30
        y = 148 - h
        color = "#06b6d4" if h > 90 else ("#6366f1" if h > 65 else "#1e293b")
        bars += f'<rect x="{x}" y="{y}" width="18" height="{h}" rx="4" fill="{color}" opacity="0.88"/>'

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 180" width="100%">
  <rect width="900" height="180" rx="14" fill="#090d16" stroke="#1e293b" stroke-width="1.5"/>
  <text x="38" y="30" fill="#64748b" font-family="'JetBrains Mono', monospace" font-size="11" letter-spacing="1.5">3D ISOMETRIC COMMIT VELOCITY SKYLINE // PULSED ACTIVITY</text>
  {bars}
  <line x1="30" y1="148" x2="870" y2="148" stroke="#06b6d4" stroke-width="1.5" opacity="0.5"/>
</svg>"""
    write_svg("skyline.svg", svg)


def build_footer():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 90" width="100%">
  <defs>
    <linearGradient id="fGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#06b6d4" stop-opacity="0.15"/>
      <stop offset="50%" stop-color="#6366f1" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#06b6d4" stop-opacity="0.15"/>
    </linearGradient>
  </defs>
  <rect width="900" height="90" rx="12" fill="#090d16" stroke="#1e293b" stroke-width="1"/>
  <rect x="20" y="18" width="860" height="54" rx="8" fill="url(#fGrad)"/>
  <text x="450" y="44" text-anchor="middle" fill="#f8fafc" font-family="'JetBrains Mono', monospace" font-size="13" font-weight="700" letter-spacing="1">DESIGNED &amp; AUTOMATED BY VAISHNO K SINGH</text>
  <text x="450" y="62" text-anchor="middle" fill="#38bdf8" font-family="'JetBrains Mono', monospace" font-size="10">⚡ Powered by Self-Updating Python SVG Generators &amp; GitHub Actions</text>
</svg>"""
    write_svg("footer.svg", svg)


if __name__ == "__main__":
    data = fetch_github_stats()
    build_hero()
    build_section_header("h-about.svg", "01 // IDENTITY", "SYSTEM TELEMETRY & ARCHITECTURE FOCUS", "whoami.yaml")
    build_about()
    build_section_header("h-stack.svg", "02 // ARSENAL", "TECH ORBIT & CORE ENGINEERING STACK", "runtime-matrix")
    build_orbit()
    build_section_header("h-stats.svg", "03 // METRICS", "LIVE GITHUB TELEMETRY & VELOCITY", "auto-synced")
    build_stats(data)
    build_skyline()
    build_section_header("h-connect.svg", "04 // NETWORK", "TRANSMISSION CHANNELS & SOCIAL NODES", "ping vaishnosingh")
    build_footer()
    print("Successfully generated all 10 custom SVG assets.")
