# Generate six skill pages from the tune-skill template, verbatim CSS/JS.
import re, os, sys

SRC = open('tune-skill/index.html', encoding='utf-8').read()

def sub(pattern, new, page, flags=re.S):
    out, n = re.subn(pattern, lambda m: new, page, count=1, flags=flags)
    if n != 1:
        raise SystemExit(f"anchor not found: {pattern[:60]}")
    return out

def span(pattern, prefix, body, suffix, page):
    out, n = re.subn(pattern, lambda m: prefix + body + suffix, page, count=1, flags=re.S)
    if n != 1:
        raise SystemExit(f"span anchor not found: {pattern[:60]}")
    return out

def build(c):
    n = c["name"]
    p = SRC.replace('tune-skill', n)
    p = sub(r'<title>.*?</title>', f'<title>{c["title"]}</title>', p)
    p = sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{c["desc"]}">', p)
    p = sub(r'<meta property="og:title" content=".*?">', f'<meta property="og:title" content="{c["title"]}">', p)
    p = sub(r'<meta property="og:description" content=".*?">', f'<meta property="og:description" content="{c["ogdesc"]}">', p)
    p = sub(r'"name": "[^"]*",\n  "alternateName": "[^"]*",', f'"name": "{n}",\n  "alternateName": "{n}",', p)
    p = sub(r'"description": "An open agent skill that fine-tunes a SKILL\.md that already exists: triggering description, sibling overlap, stale names and counts, broken handoffs\.",', f'"description": "{c["desc"]}",', p)
    p = sub(r'<h1 class="hero-h">.*?</h1>', f'<h1 class="hero-h">{c["h1"]}</h1>', p)
    p = sub(r'<p class="hero-sub">.*?</p>', f'<p class="hero-sub">{c["hsub"]}</p>', p)
    p = sub(r'<div class="stats">.*?</div>', f'<div class="stats">{c["stats"]}</div>', p)
    p = sub(r'<div class="manuscript">.*?</aside>', f'<div class="manuscript">{c["ms"]}</div>\n        </div>\n      </aside>', p)
    p = sub(r'<h2>Copy one line\. Tune the skill you already have\.</h2>', f'<h2>{c["install_h2"]}</h2>', p)
    p = sub(r'<p class="cmd-note" id="cmd-note">.*?</p>', f'<p class="cmd-note" id="cmd-note">{c["cmd_note"]}</p>', p)
    p = span(r'<section id="commands">.*?</section>', '<section id="commands">\n  <div class="wrap">', c["audit"], '\n  </div>\n</section>', p)
    p = span(r'<section id="principles">.*?</section>', '<section id="principles">\n  <div class="wrap">', c["principles"], '\n  </div>\n</section>', p)
    p = sub(r'<div class="foot-cta">.*?<footer>', f'<div class="foot-cta">{c["cta"]}</div>\n\n<footer>', p)
    p = span(r'<footer>\s*<div class="wrap">.*?</div>', '<footer>\n  <div class="wrap">', c["footer"], '</div>', p)
    p = sub(r'<a href="#commands">The audit</a>', f'<a href="#commands">{c["nav_mid"]}</a>', p)
    # install commands JS + noscript list
    p = sub(r'<ul>\s*<li><span class="mono">npx skills add.*?</ul>', c["noscript"], p, )
    p = sub(r'var cmds=\{.*?\n  \};', c["cmds_js"], p)
    n2 = c["name"]
    os.makedirs(n2, exist_ok=True)
    open(f'{n2}/index.html', 'w', encoding='utf-8', newline='\n').write(p)
    print(n2, len(p))

def cats(items):
    out = '<div class="cmd-cats">'
    for title, span, desc, lis, wide in items:
        cls = 'cat wide' if wide else 'cat'
        out += f'\n      <div class="{cls}">\n        <h3>{title} <span>{span}</span></h3>\n        <p class="cat-desc">{desc}</p>\n        <ul>' + ''.join(f'<li>{x}</li>' for x in lis) + '</ul>\n      </div>'
    return out + '\n    </div>'

def pr(items):
    out = '<div class="principles">'
    for h, t in items:
        out += f'\n      <div class="pr">\n        <h3>{h}</h3>\n        <p>{t}</p>\n      </div>'
    return out + '\n    </div>'

def install_js(n, extra_note):
    return f'''var cmds={{
    one:{{say:false,note:'The install line from the repo README. <b>SKILL.md</b> sits at the repo root, so the archive arrives whole. {extra_note}',text:'npx skills add arm-pz/{n} --skill {n}'}},
    agent:{{say:true,note:'Paste this to your agent. It reads the repo, installs itself, and reports where it put things.',text:'Install the {n} skill from github.com/arm-pz/{n} into this project\\u2019s skills directory, then confirm it loads.'}},
    claude:{{say:false,note:'Manual install into <b>.claude/skills/</b>. The clone folder is the skill folder.',text:'git clone https://github.com/arm-pz/{n} && mkdir -p .claude/skills && cp -r {n} .claude/skills/'}},
    cursor:{{say:false,note:'Manual install into <b>.cursor/skills/</b>.',text:'git clone https://github.com/arm-pz/{n} && mkdir -p .cursor/skills && cp -r {n} .cursor/skills/'}},
    codex:{{say:false,note:'Manual install into <b>.agents/skills/</b>.',text:'git clone https://github.com/arm-pz/{n} && mkdir -p .agents/skills && cp -r {n} .agents/skills/'}},
    qoder:{{say:false,note:'Manual install into <b>.qoder/skills/</b>, or <b>~/.qoder/skills/</b> to make it available in every project. Start a new session afterwards.',text:'git clone https://github.com/arm-pz/{n} && mkdir -p .qoder/skills && cp -r {n} .qoder/skills/'}},
    other:{{say:false,note:'The skill is markdown. Copy the <b>{n}</b> folder wherever your agent loads skills from. Replace <b>your-agent</b> in the command with your agent\\'s folder.',text:'git clone https://github.com/arm-pz/{n} && cp -r {n} your-agent/skills/'}}
  }};'''

def nos(n, bullet4):
    b4 = f'\n          <li>{bullet4}</li>' if bullet4 else ''
    return f'''<ul>
          <li><span class="mono">npx skills add arm-pz/{n} --skill {n}</span> is the line in the README. It installs the skill folder into your agent's skills directory.</li>
          <li><span class="mono">git clone https://github.com/arm-pz/{n}</span> produces a <span class="mono">{n}/</span> folder with <span class="mono">SKILL.md</span> at its root, so copy that folder whole into <span class="mono">.claude/skills/</span>, <span class="mono">.cursor/skills/</span>, <span class="mono">.agents/skills/</span>, <span class="mono">.qoder/skills/</span>, or wherever your agent loads skills from: <span class="mono">cp -r {n} .claude/skills/</span>.</li>
          <li>Or paste to your agent: "Install the {n} skill from github.com/arm-pz/{n} into this project's skills directory, then confirm it loads."</li>{b4}
        </ul>'''
