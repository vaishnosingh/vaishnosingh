#!/usr/bin/env python3
"""Builds assets/skyline.svg (3D contribution skyline) and assets/stats.svg from live GitHub data.
Usage: GH_LOGIN=you GH_TOKEN=... python scripts/profile_stats.py      (--placeholder renders empty versions)"""
import os, sys, json, html, random, urllib.request
LOGIN=os.environ.get("GH_LOGIN","vaishnosingh"); TOKEN=os.environ.get("GH_TOKEN","")
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","assets")
SANS="'Segoe UI','Helvetica Neue',Arial,sans-serif"; SERIF="'Iowan Old Style','Palatino Linotype','Book Antiqua',Georgia,serif"
INK,INK2,MARI,RANI,PEA,VIO,IVO,MUT="#07051A","#160F3F","#FFB400","#E8348A","#1FC6B4","#8B5CF6","#F7EEDC","#A79FC9"
esc=lambda s:html.escape(str(s),quote=False)
QUERY="""query($login:String!){user(login:$login){followers{totalCount}
repositories(ownerAffiliations:OWNER,isFork:false,first:100,orderBy:{field:PUSHED_AT,direction:DESC}){nodes{stargazerCount languages(first:8,orderBy:{field:SIZE,direction:DESC}){edges{size node{name color}}}}}
contributionsCollection{totalCommitContributions totalIssueContributions totalPullRequestContributions
contributionCalendar{totalContributions weeks{contributionDays{contributionCount weekday}}}}}}"""

def fetch():
    req=urllib.request.Request("https://api.github.com/graphql",data=json.dumps({"query":QUERY,"variables":{"login":LOGIN}}).encode(),
        headers={"Authorization":"bearer "+TOKEN,"Content-Type":"application/json","User-Agent":"profile-stats"})
    d=json.load(urllib.request.urlopen(req,timeout=30))
    if d.get("errors"): sys.exit(json.dumps(d["errors"]))
    return d["data"]["user"]

def digest(u):
    cc=u["contributionsCollection"];cal=cc["contributionCalendar"]
    days=[(wi,d["weekday"],d["contributionCount"]) for wi,w in enumerate(cal["weeks"]) for d in w["contributionDays"]]
    seq=[c for _,_,c in days];longest=run=0
    for c in seq: run=run+1 if c>0 else 0;longest=max(longest,run)
    rev=seq[::-1];i=1 if rev and rev[0]==0 else 0;cur=0
    while i<len(rev) and rev[i]>0: cur+=1;i+=1
    langs={}
    for r in u["repositories"]["nodes"]:
        for e in r["languages"]["edges"]:
            n=e["node"];l=langs.setdefault(n["name"],[0,n["color"] or "#8B8B8B"]);l[0]+=e["size"]
    return dict(days=days,total=cal["totalContributions"],cur=cur,longest=longest,commits=cc["totalCommitContributions"],prs=cc["totalPullRequestContributions"],
        issues=cc["totalIssueContributions"],stars=sum(r["stargazerCount"] for r in u["repositories"]["nodes"]),followers=u["followers"]["totalCount"],langs=langs)

def shade(h,f): return "#%02x%02x%02x"%tuple(int(int(h[i:i+2],16)*f) for i in (1,3,5))
def stars(seed):
    r=random.Random(seed);o="".join(f'<circle cx="{r.uniform(0,1000):.0f}" cy="{r.uniform(0,H_MAX):.0f}" r="{r.uniform(.5,1.5):.1f}" fill="#fff" fill-opacity="{r.uniform(.2,.8):.2f}"/>' for _ in range(90))
    return f'<g style="animation:dr 140s linear infinite"><g id="sf">{o}</g><use xlink:href="#sf" x="-1000"/></g>'
H_MAX=460
CSS=f"""@keyframes dr{{to{{transform:translateX(1000px)}}}}@keyframes rise{{from{{transform:scaleY(0)}}}}@keyframes fade{{from{{opacity:0;transform:translateY(14px)}}}}
.rise{{animation:rise .9s cubic-bezier(.2,.8,.2,1) both}}.tile{{animation:fade .8s cubic-bezier(.2,.8,.2,1) both}}
.num{{font:700 34px {SERIF};fill:{IVO}}}.lab{{font:13px {SANS};fill:{MUT}}}.ttl{{font:700 26px {SERIF};fill:{IVO}}}.sub{{font:14px {SANS};fill:{MUT}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}"""
def wrap(W,H,aria,body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{esc(aria)}"><title>{esc(aria)}</title>'
      f'<defs><style>{CSS}</style><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{INK}"/><stop offset="1" stop-color="{INK2}"/></linearGradient>'
      f'<linearGradient id="bd" x1="0" x2="1"><stop offset="0" stop-color="{MARI}"/><stop offset=".6" stop-color="{RANI}"/><stop offset="1" stop-color="{PEA}"/></linearGradient>'
      f'<radialGradient id="gw"><stop offset="0" stop-color="{RANI}" stop-opacity=".35"/><stop offset="1" stop-color="{RANI}" stop-opacity="0"/></radialGradient>'
      f'<clipPath id="c"><rect width="{W}" height="{H}" rx="24"/></clipPath></defs><g clip-path="url(#c)"><rect width="{W}" height="{H}" fill="url(#bg)"/>{stars(W+H)}{body}</g>'
      f'<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="24" fill="none" stroke="url(#bd)" stroke-opacity=".5" stroke-width="1.5"/></svg>')

LV=[("#2A2060",),(PEA,),(VIO,),(RANI,),(MARI,)]
def skyline(D):
    W,H=1000,470;ux,uy,vx,vy=15,2.8,7.5,-9;ox,oy=76,292
    P=lambda w,d:(ox+w*ux+d*vx,oy+w*uy+d*vy)
    pt=lambda p:f"{p[0]:.1f},{p[1]:.1f}"
    days=D["days"] if D else [(w,d,0) for w in range(53) for d in range(7)]
    m=max([c for _,_,c in days]+[1]);out=""
    plate=lambda a,b,dy=0:[P(a,b),P(53.4,b),P(53.4,7.4),P(a,7.4)]
    c=[P(-.4,-.4),P(53.4,-.4),P(53.4,7.4),P(-.4,7.4)];t=10
    out+=f'<polygon points="{pt(c[3])} {pt(c[2])} {pt((c[2][0],c[2][1]+t))} {pt((c[3][0],c[3][1]+t))}" fill="#0C0830"/>'
    out+=f'<polygon points="{pt(c[0])} {pt(c[3])} {pt((c[3][0],c[3][1]+t))} {pt((c[0][0],c[0][1]+t))}" fill="#0E0A38"/>'
    out+=f'<polygon points="{pt(c[1])} {pt(c[2])} {pt((c[2][0],c[2][1]+t))} {pt((c[1][0],c[1][1]+t))}" fill="#090626"/>'
    out+=f'<polygon points="{" ".join(pt(p) for p in c)}" fill="#1A1250" stroke="#3B2A8C"/>'
    for w,d,n in sorted(days,key=lambda x:(-x[1],x[0])):
        lv=0 if n==0 else min(4,max(1,-(-n*4//m)));col=LV[lv][0];h=2 if n==0 else 6+(n/m)**.7*125
        a,b,cc,dd=P(w+.12,d+.12),P(w+.88,d+.12),P(w+.88,d+.88),P(w+.12,d+.88);up=lambda p:(p[0],p[1]-h)
        g=(f'<polygon points="{pt(up(a))} {pt(up(b))} {pt(up(cc))} {pt(up(dd))}" fill="{shade(col,1.0) if n else col}"/>'
           f'<polygon points="{pt(a)} {pt(b)} {pt(up(b))} {pt(up(a))}" fill="{shade(col,.72)}"/>'
           f'<polygon points="{pt(b)} {pt(cc)} {pt(up(cc))} {pt(up(b))}" fill="{shade(col,.5)}"/>')
        if n:
            bx,by=P(w+.5,d+.5);out+=f'<g class="rise" style="transform-origin:{bx:.1f}px {by:.1f}px;animation-delay:{w*.03:.2f}s">{g}</g>'
        else: out+=g
    tot=f'{D["total"]:,}' if D else "—"
    head=f'<ellipse cx="500" cy="420" rx="520" ry="90" fill="url(#gw)"/><text class="ttl" x="40" y="54">Contribution skyline</text><text class="sub" x="40" y="78">{tot} contributions in the last year</text>'
    return wrap(W,H,"3D contribution skyline for the last year",head+out)

def stats(D):
    W,H=1000,350
    f=lambda k:f'{D[k]:,}' if D else "—"
    T=[("Contributions, 1 year","total",MARI),("Commits","commits",RANI),("Pull requests","prs",PEA),("Issues","issues",VIO),
       ("Current streak","cur",MARI),("Longest streak, 1 year","longest",RANI),("Stars earned","stars",PEA),("Followers","followers",VIO)]
    out=""
    for i,(lab,k,col) in enumerate(T):
        x=20+(i%4)*246;y=26+(i//4)*104
        out+=(f'<g transform="translate({x} {y})"><g class="tile" style="animation-delay:{i*.08:.2f}s"><rect x="6" y="6" width="222" height="88" rx="14" fill="#04030F" fill-opacity=".7"/>'
              f'<rect width="222" height="88" rx="14" fill="#150F3A" stroke="#3A2A8A"/><rect x="0" y="22" width="4" height="30" rx="2" fill="{col}"/>'
              f'<text class="num" x="22" y="54">{f(k)}</text><text class="lab" x="22" y="76">{esc(lab)}</text></g></g>')
    out+=f'<text class="ttl" x="40" y="258" style="font-size:20px">Top languages</text>'
    L=sorted(D["langs"].items(),key=lambda kv:-kv[1][0])[:6] if D else []
    tot=sum(v[0] for _,v in L) or 1;x=40
    if L:
        for n,(s,col) in L:
            w=944*s/tot-3;out+=f'<rect x="{x:.1f}" y="270" width="{max(w,2):.1f}" height="12" rx="6" fill="{col}"/>';x+=w+3
        for i,(n,(s,col)) in enumerate(L):
            lx=40+(i%3)*316;ly=312+(i//3)*24
            out+=f'<circle cx="{lx+6}" cy="{ly-4}" r="5" fill="{col}"/><text class="lab" x="{lx+20}" y="{ly}" style="fill:{IVO}">{esc(n)} <tspan style="fill:{MUT}">{100*s/tot:.1f}%</tspan></text>'
    else: out+=f'<rect x="40" y="270" width="944" height="12" rx="6" fill="#2A2060"/><text class="lab" x="40" y="312">Waiting for the first workflow run</text>'
    return wrap(W,H,"GitHub stats",out)

if __name__=="__main__":
    D=None if "--placeholder" in sys.argv else digest(fetch())
    os.makedirs(OUT,exist_ok=True)
    open(os.path.join(OUT,"skyline.svg"),"w",encoding="utf-8").write(skyline(D));open(os.path.join(OUT,"stats.svg"),"w",encoding="utf-8").write(stats(D))
    print("wrote assets/skyline.svg and assets/stats.svg")
