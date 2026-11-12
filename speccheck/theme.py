"""The page design: colors, logo, drawings, and static page sections."""

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap');
:root{--ink:#14212e;--muted:#566575;--line:#dfe5ea;--navy:#102a3f;--navy-muted:#b6c6d2;--accent:#0b6e76}
html,body,.stApp{background:#fff;color:var(--ink);font-family:"IBM Plex Sans",-apple-system,"Segoe UI",sans-serif}
header[data-testid="stHeader"],[data-testid="stToolbar"],[data-testid="stDecoration"],[data-testid="stStatusWidget"]{display:none!important}
[data-testid="stMainBlockContainer"]{padding:0!important;max-width:none!important}
[data-testid="stMainBlockContainer"]>[data-testid="stVerticalBlock"],[data-testid="stMainBlockContainer"]>div>[data-testid="stVerticalBlock"]{gap:0!important}
.st-key-band-demo,.st-key-band-match,.st-key-band-gap,.st-key-band-table,.st-key-band-products,.st-key-band-spec{padding:44px max(20px,calc((100% - 1040px)/2))!important}
.st-key-band-demo{background:#e7f0fb}.st-key-band-match{background:#e2f5e9}.st-key-band-gap{background:#fce8e5}
.st-key-band-table{background:#e0f3f1}.st-key-band-products{background:#eeeafb}.st-key-band-spec{background:#fcf1da}
h1,h2,h3,p{font-family:"IBM Plex Sans",-apple-system,"Segoe UI",sans-serif}
.sc-h2{font-size:1.3rem;font-weight:600;color:var(--ink);margin:0;line-height:1.3}
.sc-label{display:inline-block;background:#fff;font-size:.8rem;font-weight:600;padding:3px 11px;border-radius:999px;color:var(--muted);margin-bottom:4px}
.sc-wrap{max-width:1080px;margin:0 auto;padding-inline:20px}
.sc-band{background:var(--navy);color:#f2f7fa}
.sc-nav{display:flex;justify-content:space-between;align-items:center;gap:12px;padding-block:18px}
.sc-brand{display:flex;align-items:center;gap:10px;font-weight:600;font-size:1.05rem}
.sc-brand svg{width:30px;height:30px;flex:none}
.sc-tag{font-size:.86rem;color:var(--navy-muted);text-align:right}.sc-tag b{color:#f2f7fa;font-weight:600}
.sc-hero{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr);gap:44px;align-items:center;padding-block:40px 60px}
.sc-hero>*{min-width:0}
.sc-hero h1{color:#f2f7fa;font-size:clamp(2rem,5vw,3rem);line-height:1.12;font-weight:600;margin:0 0 14px;padding:0}
.sc-lede{font-size:1.1rem;color:var(--navy-muted);max-width:60ch;margin:0}
.sc-visual{display:grid;gap:14px;min-width:0}.sc-visual svg{width:100%;height:auto;display:block}
.sc-preview{background:#fff;color:var(--ink);border-radius:10px;padding:16px;display:grid;gap:8px;box-shadow:0 18px 40px rgba(0,0,0,.28)}
.sc-preview small{font-size:.8rem;font-weight:600;color:var(--muted)}
.sc-prow{display:flex;justify-content:space-between;gap:10px;align-items:center;padding-top:8px;border-top:1px solid #e6ebef;font-size:.9rem}
.sc-chip{display:inline-block;padding:1px 9px;border-radius:999px;font-weight:600;font-size:.8rem;white-space:nowrap}
.PASS{background:#dff3e6;color:#17603a}.FAIL{background:#fbe3e0;color:#96231a}.REVIEW{background:#fcefd0;color:#7a4c0b}
.sc-sec{padding-block:44px}
.st-key-band-path{padding:44px max(20px,calc((100% - 1040px)/2))!important;background:#eaeef2}
.st-key-band-path button{min-height:86px;font-weight:600}
.sc-cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin-top:18px}
.sc-card{border-radius:10px;padding:20px;min-width:0}.sc-card svg{width:100%;max-width:210px;height:auto;display:block;margin-bottom:8px}
.sc-card b{display:block;color:var(--ink);font-size:1.05rem;font-weight:600}.sc-card p{color:var(--ink);font-size:.94rem;margin:4px 0 0}
.c-blue{background:#e7f0fb;color:#1d5fa8}.c-teal{background:#e0f3f1;color:#0b6e76}.c-amber{background:#fcf1da;color:#8a5a0c}
.sc-panel{background:#fff;border:1px solid var(--line);border-radius:8px;padding:22px}
.sc-verdict{display:flex;flex-wrap:wrap;gap:10px 14px;align-items:center;justify-content:space-between}
.sc-kicker{font-size:.82rem;font-weight:600;color:var(--muted)}
.sc-verdict h2{font-size:1.3rem;font-weight:600;margin:0;padding:0;color:var(--ink);line-height:1.3}
.sc-counts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));border-top:1px solid var(--line);padding-top:14px;margin-top:14px}
.sc-counts div{padding-inline:16px;border-left:1px solid var(--line);min-width:0}.sc-counts div:first-child{padding-left:0;border-left:0}
.sc-counts b{display:block;font:500 1.6rem/1.2 "IBM Plex Mono",Consolas,monospace}.sc-counts span{font-size:.84rem;color:var(--muted)}
.sc-small{font-size:.86rem;color:var(--muted);margin:12px 0 0}
.sc-scroll{overflow-x:auto;background:#fff;border:1px solid var(--line);border-radius:8px;margin-top:6px}
.sc-scroll table{border-collapse:collapse;width:100%;min-width:720px;font-size:.9rem;color:var(--ink)}
.sc-scroll.small table{min-width:520px}
.sc-scroll th{font-size:.8rem;font-weight:600;text-align:left;color:var(--muted);background:#eaeef2;white-space:nowrap;border:0}
.sc-scroll th,.sc-scroll td{padding:10px 14px;border:0;border-bottom:1px solid var(--line);vertical-align:top}
.sc-scroll tr:last-child td{border-bottom:0}
.sc-scroll td:nth-child(4){white-space:nowrap}
.sc-num{font-family:"IBM Plex Mono",Consolas,monospace;font-size:.84rem}.sc-quote{color:var(--muted)}
.sc-foot{background:var(--navy);color:var(--navy-muted);padding-block:22px;font-size:.86rem}
.stButton button[kind="primary"]{background:var(--accent);border-color:var(--accent);color:#fff}
.sc-spec{white-space:pre-wrap;overflow-wrap:anywhere;font:400 .85rem/1.55 "IBM Plex Mono",Consolas,monospace;margin:0}
@media (max-width:780px){.sc-hero{grid-template-columns:1fr;gap:26px;padding-block:24px 36px}.sc-cards{grid-template-columns:1fr}.sc-counts div{padding-inline:10px}}

.st-key-band-demo,.st-key-band-match,.st-key-band-gap,.st-key-band-table,.st-key-band-products,.st-key-band-spec,.st-key-band-path{background:#fff!important;border-top:1px solid var(--line)}
.sc-label{background:none;color:var(--accent);padding:0;border-radius:0;font-size:.74rem;letter-spacing:.08em;text-transform:uppercase}
.sc-card,.c-blue,.c-teal,.c-amber{background:#f6f8fa;border:1px solid var(--line);color:var(--accent)}
.sc-card svg{max-width:110px!important}
.sc-preview{box-shadow:0 8px 24px rgba(0,0,0,.18)}
.sc-type{background:#e4f1f2;border:1px solid var(--accent);border-radius:8px;padding:18px 20px;margin:14px 0}
.sc-type-kicker{color:var(--accent);text-transform:uppercase;letter-spacing:.06em;font-size:.76rem;font-weight:600}
.sc-type b{display:block;font-size:1.2rem;color:var(--ink);margin-top:4px}
.sc-type p{font-size:1.05rem;line-height:1.55;margin:6px 0 0;max-width:70ch;color:var(--ink)}
.sc-scroll td{vertical-align:middle}
.sc-row-FAIL{background:#fdf1ef}.sc-row-REVIEW{background:#fef8e8}
.sc-name{font-weight:600}.sc-tag{font-size:.78rem;color:var(--muted);margin-top:2px}
.sc-note{font-size:.8rem;color:#8a5a0c;margin-top:4px}
.sc-quote{font-style:italic}
.sc-mine td{font-weight:600;background:#e4f1f2}
.sc-scroll td .sc-tag,.sc-scroll td .sc-name{text-align:left;display:block}
.sc-trends{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-top:10px}
.sc-trend,.sc-trend div{text-align:left!important}
.sc-trend{align-content:start;border:1px solid var(--line);border-radius:8px;padding:12px;background:#fff;min-width:0;display:grid;gap:6px}
@media (max-width:900px){.sc-trends{grid-template-columns:repeat(2,minmax(0,1fr))}}
.sc-docwrap{background:#eaeef2;border-radius:6px;padding:24px 16px}
.sc-docpage{background:#fff;color:#202124;max-width:720px;margin:0 auto;padding:56px 64px;box-shadow:0 1px 3px rgba(60,64,67,.3),0 4px 8px rgba(60,64,67,.15);font-family:Arial,"Helvetica Neue",Helvetica,sans-serif;font-size:11pt;line-height:1.5}
.sc-docpage h1{font-family:Arial,sans-serif;font-size:20pt;font-weight:400;margin:0 0 6px;padding:0;line-height:1.25;color:#202124}
.sc-docpage h2{font-family:Arial,sans-serif;font-size:13pt;font-weight:700;margin:18px 0 4px;padding:0;color:#202124}
.sc-docpage p{margin:0 0 8px;font-family:Arial,sans-serif;color:#202124}
.sc-docpage .sc-docnote{font-style:italic;color:#5f6368;margin-bottom:14px}
@media (max-width:600px){.sc-docpage{padding:28px 20px}}
.sc-split{display:grid;gap:8px;border:1px solid var(--line);border-radius:8px;padding:16px 18px;background:#fff;margin:10px 0}
.sc-split-row{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(0,2fr) 7rem 3.2rem;gap:12px;align-items:center;font-size:.9rem;text-align:left}
.sc-split-bar{height:8px;background:#eaeef2;border-radius:4px;overflow:hidden}
.sc-split-bar span{display:block;height:100%;border-radius:4px}
.sc-split-num{text-align:right;font-variant-numeric:tabular-nums}
</style>
"""

LOGO = ('<svg viewBox="0 0 32 32" fill="none" aria-hidden="true"><rect width="32" height="32" rx="8" fill="#5fd0cd"/>'
        '<path d="M9 6h10l5 5v15H9z" fill="#08242a"/><path d="M19 6v5h5" stroke="#5fd0cd" stroke-width="1.6" stroke-linejoin="round"/>'
        '<path d="M12.5 18l2.8 2.8 5.2-6" stroke="#5fd0cd" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def _cabinet(x: int) -> str:
    return (f'<g transform="translate({x} 20)"><rect width="88" height="128" rx="3" fill="#1b3f5a" stroke="#5b7f98" stroke-width="2"/>'
            '<rect x="10" y="10" width="68" height="40" rx="2" fill="#163349" stroke="#5b7f98"/>'
            '<circle cx="24" cy="30" r="5" fill="#5fd0cd"/><circle cx="42" cy="30" r="5" fill="#f3cd83"/>'
            '<rect x="54" y="22" width="16" height="16" rx="2" fill="#2d5a78"/>'
            '<rect x="10" y="58" width="68" height="60" rx="2" fill="#163349" stroke="#5b7f98"/>'
            '<path d="M18 72h52M18 84h52M18 96h52" stroke="#5b7f98" stroke-width="2"/></g>')


LINEUP = ('<svg viewBox="0 0 400 160" role="img" aria-label="Illustration of a switchgear lineup">'
          + "".join(_cabinet(x) for x in (12, 106, 200, 294))
          + '<path d="M12 46H382" stroke="#5fd0cd" stroke-width="3" opacity=".7"/><path d="M0 150H400" stroke="#5b7488" stroke-width="2"/></svg>')

_ART = 'viewBox="0 0 200 110" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"'
_DOC = (f'<svg {_ART}><path d="M58 8h58l22 22v72H58z" fill="#fff"/><path d="M116 8v22h22"/>'
        '<rect x="70" y="40" width="56" height="12" rx="2" fill="currentColor" opacity=".22" stroke="none"/>'
        '<path d="M72 46h52M72 64h52M72 80h34"/><circle cx="136" cy="74" r="17" fill="#fff"/><path d="M148 86l14 14M128 74h16"/></svg>')
_GEAR = (f'<svg {_ART}><g fill="#fff"><rect x="28" y="14" width="44" height="86" rx="3"/><rect x="78" y="14" width="44" height="86" rx="3"/>'
         '<rect x="128" y="14" width="44" height="86" rx="3"/></g><path d="M36 36h28M86 36h28M136 36h28M36 50h28M86 50h28M136 50h28"/>'
         '<path d="M40 76l6 6 14-14M90 76l6 6 14-14M142 68l16 16M158 68l-16 16"/></svg>')
_FLAG = (f'<svg {_ART}><rect x="36" y="10" width="128" height="90" rx="5" fill="#fff"/><path d="M36 30h128"/>'
         '<path d="M52 46h66M52 64h66M52 82h66"/><path d="M134 40v18M134 41h15l-4 5 4 5h-15" fill="currentColor"/><path d="M134 70l5 5 10-10"/></svg>')

HEADER = f"""
<header class="sc-band"><div class="sc-wrap">
<div class="sc-nav"><div class="sc-brand">{LOGO}SpecCheck AI</div><div class="sc-tag"><b>By Brian Oh</b></div></div>
<div class="sc-hero"><div><h1>Spec review for power equipment</h1>
<p class="sc-lede">Upload a customer spec. SpecCheck AI checks it against a product catalog and shows what passes, what fails, and what an engineer should review.</p></div>
<div class="sc-visual"><div class="sc-preview"><small>Sample result</small>
<div class="sc-prow"><span>Current: 3000 A</span><span class="sc-chip PASS">Pass</span></div>
<div class="sc-prow"><span>Infrared windows</span><span class="sc-chip FAIL">Fail</span></div>
<div class="sc-prow"><span>Witnessed factory test</span><span class="sc-chip REVIEW">Review</span></div></div></div></div>
</div></header>
<section class="sc-sec"><div class="sc-wrap"><div class="sc-h2">How it works</div><div class="sc-cards">
<div class="sc-card c-blue">{_DOC}<b>1. Find the requirements</b><p>Claude lists each requirement and the line it came from.</p></div>
<div class="sc-card c-teal">{_GEAR}<b>2. Check the catalog</b><p>Each requirement is checked against every product and marked pass, fail, or review.</p></div>
<div class="sc-card c-amber">{_FLAG}<b>3. Review the results</b><p>See the best match, what's missing, and what an engineer should check.</p></div>
</div></div></section>
"""

FOOTER = ('<footer class="sc-foot"><div class="sc-wrap">All specs and products here are made up. '
          'An engineer should review every result before it goes to a customer.</div></footer>')
