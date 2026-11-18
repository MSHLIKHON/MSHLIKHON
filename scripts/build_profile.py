#!/usr/bin/env python3
"""Render Likhon's original profile artwork. Python standard library only."""
import argparse
import collections
import datetime as dt
import html
import json
import math
import os
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
BG = '#0c1118'
PANEL = '#111923'
LINE = '#283643'
WHITE = '#f0f2e9'
MUTED = '#a4b2c1'
MINT = '#b8ff75'
BLUE = '#8baeff'
MONO = "'SFMono-Regular',Consolas,'Liberation Mono',monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif"


def esc(value):
    return html.escape(str(value), quote=True)


def text(x, y, value, size=18, color=WHITE, weight=400, mono=False, extra=''):
    return (f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" '
            f'font-weight="{weight}" font-family="{MONO if mono else SANS}" {extra}>{esc(value)}</text>')


def rect(x, y, w, h, fill=PANEL, radius=12, stroke=LINE, extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" {extra}/>'


def path(d, color=LINE, width=1, extra=''):
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" {extra}/>'


def circle(x, y, r, fill=MINT, extra=''):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" {extra}/>'


def svg(w, h, title, content, description=''):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">{esc(title)}</title><desc id="desc">{esc(description or title)}</desc>
<defs>
 <linearGradient id="wash" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#162332"/><stop offset="1" stop-color="{BG}"/></linearGradient>
 <radialGradient id="halo"><stop stop-color="{MINT}" stop-opacity=".13"/><stop offset="1" stop-color="{MINT}" stop-opacity="0"/></radialGradient>
 <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#8398af" stroke-opacity=".055"/></pattern>
</defs>
<style>
 .pulse{{animation:pulse 3s ease-in-out infinite}} .flow{{stroke-dasharray:5 13;animation:flow 6s linear infinite}}
 .float{{animation:float 7s ease-in-out infinite}} .scan{{animation:scan 9s linear infinite}}
 .trace{{stroke-dasharray:180 700;animation:trace 16s linear infinite}}
 @keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.3}}}}
 @keyframes flow{{to{{stroke-dashoffset:-180}}}}
 @keyframes float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-7px)}}}}
 @keyframes scan{{0%{{transform:translateX(0);opacity:0}}10%,80%{{opacity:.6}}100%{{transform:translateX(1050px);opacity:0}}}}
 @keyframes trace{{to{{stroke-dashoffset:-880}}}}
 @media(prefers-reduced-motion:reduce){{.pulse,.flow,.float,.scan,.trace{{animation:none}}}}
</style>
{rect(.5,.5,w-1,h-1,BG,18)}
{content}
</svg>'''


def header(cfg):
    s = rect(1,1,1198,438,'url(#wash)',18,'none')
    s += rect(1,1,1198,438,'url(#grid)',18,'none')
    s += circle(976,212,250,'url(#halo)')
    s += rect(34,32,43,32,MINT,7,'none') + text(43,54,'ML',18,BG,800,True)
    s += text(92,54,'MSHLIKHON / PERSONAL SYSTEM',14,MUTED,500,True,extra='letter-spacing="1"')
    s += circle(1010,48,4,MINT,'class="pulse"') + text(1024,53,'DHAKA · BD',14,MUTED,500,True)
    s += text(40,111,'PEOPLE FIRST. SYSTEMS WITH PURPOSE.',14,MINT,600,True,extra='letter-spacing="2"')
    s += text(34,225,cfg['short_name'],120,WHITE,800,extra='letter-spacing="-7"')
    s += text(42,270,cfg['name'],23,MUTED,500)
    s += text(42,318,'Curiosity into code.',29,WHITE,600)
    s += text(42,355,'Code into something useful.',29,WHITE,600)
    s += path('M42 386 H1158',LINE)
    for x, label in [(42,'SOFTWARE ENGINEERING'),(360,'NETWORKS & INFORMATION SYSTEMS'),(850,'TECH FOR SOCIAL IMPACT')]:
        s += text(x,416,label,13,MUTED,500,True)
    # The personal monogram is a connected system: ideas, engineering, community.
    s += '<g class="float">'
    s += path('M895 122 L1065 186 L1001 322 L831 258 Z',LINE,1.5)
    s += path('M895 122 L1001 322 M831 258 L1065 186',LINE)
    s += '<ellipse cx="948" cy="221" rx="140" ry="91" transform="rotate(-24 948 221)" fill="none" stroke="#435665"/>'
    s += '<ellipse cx="948" cy="221" rx="140" ry="91" transform="rotate(-24 948 221)" fill="none" stroke="#b8ff75" class="flow"/>'
    s += rect(901,175,94,94,BG,22,'#8baeff')
    s += text(918,235,'ML',38,WHITE,700,True)
    for x,y,n,label in [(895,122,'01','LEARN'),(1065,186,'02','BUILD'),(1001,322,'03','CONNECT'),(831,258,'04','IMPACT')]:
        s += circle(x,y,18,BG,f'stroke="{MINT}"')+text(x,y+5,n,12,MINT,500,True,'text-anchor="middle"')
        s += text(x,y-29,label,11,MUTED,500,True,'text-anchor="middle"')
    s += '</g>'
    return svg(1200,440,'Likhon — People first. Systems with purpose.',s,
               cfg['name']+' · CSE at UIU. Software engineering, networking and technology for social impact.')


def about(cfg):
    s = text(32,44,'01 / THE PERSON BEHIND THE CODE',14,MINT,500,True)
    s += text(32,95,'I build to make things easier for people.',34,WHITE,650)
    for y,line in [(139,'CSE undergraduate at United International University, Dhaka.'),
                   (170,'Majoring in Software Engineering; interested in networks,'),
                   (201,'databases, information systems and practical web applications.')]:
        s += text(34,y,line,21,MUTED)
    s += text(34,251,'LEARN DELIBERATELY. BUILD THOUGHTFULLY. KEEP IMPROVING.',13,MINT,500,True)
    s += path('M828 80 V255',LINE)
    s += text(861,103,'CURRENT CHAPTER',12,MUTED,500,True)
    s += text(861,139,'Software Engineering',23,WHITE,600)
    s += text(861,182,'Expected graduation',15,MUTED)
    s += text(861,212,cfg['graduation'],24,BLUE,600)
    s += circle(868,249,4,MINT,'class="pulse"') + text(881,255,'Open to entry-level opportunities',14,MINT)
    return svg(1200,286,'About Likhon',s)


def projects(cfg):
    result={}
    for p in cfg['projects']:
        a=p['accent']
        s=path('M22 1 H578',a,2)
        s+=text(28,37,p['category'],12,MUTED,500,True)
        s+=text(28,96,p['name'],33,WHITE,650,extra='letter-spacing="-.8"')
        s+=text(28,126,p['tag'],11,a,600,True,extra='letter-spacing="1"')
        for i,line in enumerate(p['description']):s+=text(28,174+i*27,line,17,MUTED)
        s+=path('M28 228 H552',LINE)
        s+=text(28,258,p['stack'],13,a,500,True)
        s+=text(550,38,'↗',24,a,500,extra='text-anchor="end"')
        # Four distinct, original glyphs reference the actual problem domain.
        if p['motif']=='compass':
            s+=circle(522,100,30,'none',f'stroke="{LINE}"')
            s+=path('M508 116 L531 79 L527 105 Z',a,2)
            s+=circle(522,100,3,a,'class="pulse"')
        elif p['motif']=='bridge':
            s+=path('M491 119 V82 M549 119 V82 M486 104 Q520 59 554 104 M486 114 H554',a,1.8)
            for x in [501,511,529,539]:s+=path(f'M{x} 92 V113',LINE)
        elif p['motif']=='steps':
            for j in range(4):s+=rect(492+j*16,117-j*13,10,10,a,2,'none',f'opacity="{.3+j*.2}"')
            s+=path('M491 134 H554',LINE)
        else:
            for i,j in [(1,0),(2,1),(0,2),(1,2),(2,2)]:s+=rect(493+j*17,76+i*17,12,12,a,2,'none')
        result['project-'+p['repo']+'.svg']=svg(580,284,p['name'],s,' '.join(p['description'])+' '+p['stack'])
    return result


def stack():
    s=text(32,43,'02 / WORKING TOOLBOX',14,MINT,500,True)
    columns=[(32,'CODE & APPLICATIONS',['C · Python · Java','HTML · PHP · MySQL']),
             (435,'NETWORKS & DATA',['Cisco Packet Tracer','IP addressing · SQL · ER diagrams']),
             (838,'TOOLS & COLLABORATION',['Git · GitHub · VS Code','Figma · Teamwork'])]
    for x,label,lines in columns:
        s+=path(f'M{x} 71 H{x+330}',LINE)
        s+=text(x,105,label,13,BLUE,500,True)
        for i,line in enumerate(lines):s+=text(x,146+i*32,line,18,WHITE)
    s+=path('M32 210 H1168',LINE)
    s+=circle(39,240,4,MINT,'class="pulse"')
    s+=text(53,246,'LEARNING',12,MINT,500,True)
    s+=text(167,246,'Software design  /  Networking fundamentals  /  Web security',17,MUTED)
    return svg(1200,275,'Skills and current learning',s)


def community():
    s=text(32,43,'03 / BEYOND THE KEYBOARD',14,MINT,500,True)
    s+=text(32,96,'Good systems start with understanding people.',32,WHITE,650)
    s+=text(32,135,'Community work informs how I think, collaborate and build.',20,MUTED)
    columns=[(32,'01','UIU Social Services Club','Deputy Logistics · 2024–2026'),
             (435,'02','UIU App Forum','General Member · 2023–Present'),
             (838,'03','Social Welfare Initiative','Founder & Volunteer · 2020–Present')]
    for x,n,name,role in columns:
        s+=path(f'M{x} 169 H{x+330}',LINE)
        s+=text(x,202,n,12,MINT,600,True)
        s+=text(x,235,name,21,WHITE,600)
        s+=text(x,266,role,14,MUTED)
    return svg(1200,298,'Leadership and community',s)


def public_data(cfg, refresh=False):
    target=ROOT/'data/github.json'
    if refresh:
        token=os.environ.get('GITHUB_TOKEN')
        if not token:raise RuntimeError('GITHUB_TOKEN is required for --refresh')
        query='''query($login: String!) { user(login: $login) {
          login name bio url followers { totalCount }
          repositories(first: 50, ownerAffiliations: OWNER, privacy: PUBLIC,
            orderBy: {field: UPDATED_AT, direction: DESC}) {
            totalCount nodes { name url description isFork stargazerCount
              primaryLanguage { name }
              languages(first: 8, orderBy: {field: SIZE, direction: DESC}) {
                edges { size node { name color } } } } }
          contributionsCollection { contributionCalendar { totalContributions
            weeks { contributionDays { date contributionCount color } } } }
        } }'''
        body=json.dumps({'query':query,'variables':{'login':cfg['username']}}).encode()
        req=urllib.request.Request('https://api.github.com/graphql',data=body,
            headers={'Authorization':'Bearer '+token,'Content-Type':'application/json',
                     'User-Agent':'MSHLIKHON-profile'})
        with urllib.request.urlopen(req,timeout=30) as response:result=json.load(response)
        if result.get('errors'):raise RuntimeError(str(result['errors']))
        data=result['data']['user']
        if not data:raise RuntimeError('GitHub user was not found')
        target.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    return json.loads(target.read_text())


def contribution_art(data):
    cal=data['contributionsCollection']['contributionCalendar']
    weeks=cal['weeks']
    days=[d for w in weeks for d in w['contributionDays']]
    max_count=max([d['contributionCount'] for d in days]+[1])
    active=sum(d['contributionCount']>0 for d in days)
    repos=data['repositories']
    languages=collections.Counter()
    for r in repos['nodes']:
        if r['isFork']:continue
        for edge in r['languages']['edges']:languages[edge['node']['name']]+=edge['size']
    s=text(32,44,'04 / THE WORK, OVER TIME',14,MINT,500,True)
    metrics=[(32,f"{cal['totalContributions']:,}",'CONTRIBUTIONS'),
             (332,str(active),'ACTIVE DAYS'),(632,str(repos['totalCount']),'PUBLIC REPOSITORIES')]
    for x,val,label in metrics:s+=text(x,99,val,40,WHITE,650)+text(x,126,label,11,MUTED,500,True)
    s+=text(1168,89,'REAL DATA.',17,MINT,600,True,'text-anchor="end"')
    s+=text(1168,115,'STEADY PROGRESS.',14,MUTED,500,True,'text-anchor="end"')
    s+=path('M32 150 H1168',LINE)
    colors=['#1b2830','#355141','#507d4d','#83b55f',MINT]
    start=dt.date.fromisoformat(days[0]['date']);end=dt.date.fromisoformat(days[-1]['date'])
    pitch=20; x0=(1200-len(weeks)*pitch)/2
    last_month=None
    for wi,w in enumerate(weeks):
        for d in w['contributionDays']:
            date=dt.date.fromisoformat(d['date']); dow=(date.weekday()+1)%7
            x=x0+wi*pitch;y=197+dow*20;c=d['contributionCount']
            level=0 if c==0 else min(4,1+int(3*math.log1p(c)/math.log1p(max_count)))
            s+=f'<g><title>{d["date"]}: {c} contributions</title>'+rect(round(x,1),y,15,15,colors[level],3,'none')+'</g>'
        first=dt.date.fromisoformat(w['contributionDays'][0]['date'])
        if first.month!=last_month and wi<len(weeks)-2:
            s+=text(round(x0+wi*pitch,1),182,first.strftime('%b'),11,MUTED,400,True)
            last_month=first.month
    s+=text(32,371,f'{start:%d %b %Y} — {end:%d %b %Y}',12,MUTED,400,True)
    s+=text(850,371,'LESS',10,MUTED,400,True)
    for i,c in enumerate(colors):s+=rect(897+i*21,359,14,14,c,3,'none')
    s+=text(1010,371,'MORE',10,MUTED,400,True)
    s+=text(32,413,'PUBLIC REPOSITORY LANGUAGE MIX',11,BLUE,500,True)
    mix='   /   '.join(k for k,_ in languages.most_common(5)) or 'No language data yet'
    s+=text(32,444,mix,17,WHITE,500)
    s+=text(1168,444,'SOURCE / GITHUB API',10,MUTED,500,True,'text-anchor="end"')
    result={'activity.svg':svg(1200,470,'GitHub contributions and public repository language mix',s,
             f"{cal['totalContributions']} contributions across {active} active days; {repos['totalCount']} public repositories. {mix}")}
    # Original isometric skyline: one pillar per day; actual counts set pillar height.
    skyline=text(32,42,'CONTRIBUTION TERRAIN / ONE PILLAR, ONE DAY',12,MUTED,500,True)
    for wi,w in enumerate(weeks):
        for d in w['contributionDays']:
            dow=(dt.date.fromisoformat(d['date']).weekday()+1)%7;c=d['contributionCount']
            x=100+wi*17+dow*15
            height=3 if c==0 else 8+48*math.log1p(c)/math.log1p(max_count)
            y=134+dow*11-wi*.40-height
            top='#263b38' if not c else MINT
            skyline+=f'<path d="M{x} {y} l14 6 v{height:.1f} l-14 -6 Z" fill="{("#162825" if not c else "#477347")}"/>'
            skyline+=f'<path d="M{x+14} {y+6} l10 -6 v{height:.1f} l-10 6 Z" fill="{("#101e23" if not c else "#274b3a")}"/>'
            skyline+=f'<path d="M{x} {y} l10 -6 l14 6 l-10 6 Z" fill="{top}"/>'
    skyline+=path('M40 229 H1160',LINE)
    skyline+=path('M40 229 H1160',MINT,2,'class="trace"')
    skyline+=text(32,264,'SMALL CONTRIBUTIONS. COMPOUNDING OVER TIME.',12,MINT,500,True)
    result['terrain.svg']=svg(1200,288,'Isometric contribution terrain',skyline,
          'An original isometric rendering of the same GitHub calendar. Higher pillars represent more contributions.')
    return result


def contact_art(label, detail, color=MINT):
    s=circle(29,33,4,color)+text(47,39,label,17,WHITE,600)+text(330,39,'↗',22,color,500)
    return svg(360,68,label,s,detail)


def footer():
    s=path('M32 1 H1168',LINE)
    s+=text(32,57,'MAKE IT USEFUL.',30,WHITE,700,extra='letter-spacing="-.8"')
    s+=text(32,91,'Then make it better.',20,MUTED)
    s+=text(1168,57,'MD SHYED HASAN LIKHON',13,MINT,500,True,'text-anchor="end"')
    s+=text(1168,86,'DHAKA, BANGLADESH / OPEN TO COLLABORATE',11,MUTED,500,True,'text-anchor="end"')
    return svg(1200,126,'Make it useful. Then make it better. — Likhon',s)


def readme(cfg):
    u=cfg['username']; p=cfg['projects']
    img=lambda f,alt,w='100%':f'<img src="assets/{f}" width="{w}" alt="{esc(alt)}" />'
    lines=['<!-- Generated from profile.json by scripts/build_profile.py. -->',
           img('hero.svg',cfg['name']+' — People first. Systems with purpose.'),'',
           '<p align="center">',
           f'<a href="{cfg["portfolio"]}">Portfolio</a> &nbsp; / &nbsp; '
           f'<a href="{cfg["linkedin"]}">LinkedIn</a> &nbsp; / &nbsp; '
           f'<a href="mailto:{cfg["email"]}">Email</a> &nbsp; / &nbsp; '
           f'<a href="https://github.com/{u}?tab=repositories">Repositories</a>',
           '</p>','',img('about.svg','CSE undergraduate at UIU, majoring in Software Engineering. Expected graduation Summer 2027. Open to entry-level opportunities.'),'',
           '### Selected work','',
           'Practical tools, community systems and experiments I learn from.','']
    for i in range(0,len(p),2):
        lines+=['<p align="center">']
        for project in p[i:i+2]:
            alt=project['name']+' — '+' '.join(project['description'])+' '+project['stack']
            lines+=[f'<a href="https://github.com/{u}/{project["repo"]}">'+img('project-'+project['repo']+'.svg',alt,'49%')+'</a>']
        lines+=['</p>','']
    lines += [f'**Also built:** [Personal portfolio]({cfg["portfolio"]}) · '
              f'[Medical portfolio](https://github.com/{u}/dr-pritom-medical-portfolio). '
              '**Team coursework:** [Mayor’s Rise](https://github.com/ashad-abir/Mayor-s-Rise), a collaborative Java OOP project.','',
              img('stack.svg','C, Python, Java, HTML, PHP, MySQL; Cisco Packet Tracer, SQL, Git, GitHub, VS Code and Figma.'),'',
              img('community.svg','Deputy Logistics, UIU Social Services Club, 2024–2026. Member, UIU App Forum, 2023–Present. Founder and volunteer, Personal Social Welfare Initiative, 2020–Present.'),'',
              '<details>','<summary>More about my community work and continuing learning</summary>','',
              '- **National Children’s Task Force, school branch** — General Secretary, August 2017–February 2018; children’s rights and welfare initiatives.',
              '- **Personal Social Welfare Initiative** — Relief and community support.',
              '- **Continuing learning** — Grameenphone Academy skill development courses and professional workshops. [Certificates](https://drive.google.com/drive/folders/1-tNXgIcSrWGG24EfCFrsKpNAvmtIfNsZ?usp=share_link).','',
              '</details>','',img('activity.svg','Live GitHub contributions, active days, public repository count and language mix; refreshed daily.'),'',
              '<details>','<summary>Explore my contribution terrain</summary>','',img('terrain.svg','Isometric rendering of my actual daily GitHub contributions.'),'','</details>','',
              '<p align="center">',
              f'<a href="{cfg["portfolio"]}">'+img('contact-portfolio.svg','Explore my portfolio','32%')+'</a>',
              f'<a href="{cfg["linkedin"]}">'+img('contact-linkedin.svg','Connect on LinkedIn','32%')+'</a>',
              f'<a href="mailto:{cfg["email"]}">'+img('contact-email.svg','Start a conversation','32%')+'</a>',
              '</p>','',img('closing.svg','Make it useful. Then make it better. — MD Shyed Hasan Likhon'),'']
    return '\n'.join(lines)


def build(refresh=False):
    cfg=json.loads((ROOT/'profile.json').read_text())
    data=public_data(cfg,refresh)
    assets={'hero.svg':header(cfg),'about.svg':about(cfg),'stack.svg':stack(),
            'community.svg':community(),'closing.svg':footer(),
            'contact-portfolio.svg':contact_art('Explore portfolio',cfg['portfolio']),
            'contact-linkedin.svg':contact_art('Connect on LinkedIn',cfg['linkedin'],BLUE),
            'contact-email.svg':contact_art('Start a conversation','mailto:'+cfg['email'])}
    assets.update(projects(cfg));assets.update(contribution_art(data))
    (ROOT/'assets').mkdir(exist_ok=True)
    for name,content in assets.items():(ROOT/'assets'/name).write_text(content+'\n')
    (ROOT/'README.md').write_text(readme(cfg))
    print(f'Built {len(assets)} original SVG assets and README for {cfg["username"]}.')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--refresh',action='store_true',help='Fetch current public GitHub data')
    build(parser.parse_args().refresh)
