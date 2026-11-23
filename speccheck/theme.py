"""The page design: colors, logo, drawings, and static page sections."""

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600;700&family=Inter:wght@300;400;500;600&family=Inter+Tight:wght@300;400;500&family=Instrument+Serif&display=swap');
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
.st-key-band-path button{min-height:44px;font-weight:600}
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
.sc-docpage{background:#fff;color:#1a1a1a;max-width:720px;margin:0 auto;padding:56px 72px 48px;box-shadow:0 1px 3px rgba(60,64,67,.3),0 4px 8px rgba(60,64,67,.15);font-family:"Courier New",Courier,monospace;font-size:10pt;line-height:1.45}
.sc-docpage h1{font-family:"Courier New",Courier,monospace;font-size:12pt;font-weight:700;text-align:center;text-transform:uppercase;letter-spacing:.02em;margin:0 0 4px;padding:0;line-height:1.5;color:#1a1a1a}
.sc-docpage h2{font-family:"Courier New",Courier,monospace;font-size:11pt;font-weight:700;margin:20px 0 6px;padding:0;color:#1a1a1a}
.sc-docpage h3{font-family:"Courier New",Courier,monospace;font-size:11pt;font-weight:700;margin:10px 0 4px;padding:0;color:#1a1a1a}
.sc-docpage h4{font-family:"Courier New",Courier,monospace;font-size:11pt;font-weight:700;text-align:center;margin:24px 0 0;padding:0;color:#1a1a1a}
.sc-docpage p{margin:0 0 6px;font-family:"Courier New",Courier,monospace;color:#1a1a1a}
.sc-docpage p.sc-item{padding-left:52px;text-indent:-22px}
.sc-docpage .sc-note{margin:8px 0 8px 42%;font-size:9pt;line-height:1.3}
.sc-docpage .sc-l1{padding-left:28px;text-indent:-18px}.sc-docpage .sc-l2{padding-left:56px;text-indent:-18px}.sc-docpage .sc-l3{padding-left:84px;text-indent:-18px}.sc-docpage .sc-l4{padding-left:112px;text-indent:-22px}
.sc-docpage .sc-ref{display:grid;grid-template-columns:150px 1fr;gap:8px;padding-left:28px}.sc-docpage .sc-ref span:first-child{overflow:hidden;white-space:nowrap}.sc-docpage .sc-ref span:first-child::after{content:" ........................................"}
.sc-docpage .sc-pg{display:flex;justify-content:center;border-top:1px dashed #bbb;margin:22px 0 14px;padding-top:6px;font-size:9pt;color:#666}
.sc-docpage .sc-docnote{font-style:italic;color:#555;text-align:center;font-size:9.5pt;margin-bottom:10px}
html:root body .sc-docpage,html:root body .sc-docpage h1,html:root body .sc-docpage h2,html:root body .sc-docpage h3,html:root body .sc-docpage h4,html:root body .sc-docpage p{font-family:"Courier New",Courier,monospace!important;letter-spacing:0}
@media (max-width:600px){.sc-docpage{padding:28px 20px}}
.sc-split{display:grid;gap:8px;border:1px solid var(--line);border-radius:8px;padding:16px 18px;background:#fff;margin:10px 0}
.sc-split-row{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(0,2fr) 7rem 3.2rem;gap:12px;align-items:center;font-size:.9rem;text-align:left}
.sc-split-bar{height:8px;background:#eaeef2;border-radius:4px;overflow:hidden}
.sc-split-bar span{display:block;height:100%;border-radius:4px}
.sc-split-num{text-align:right;font-variant-numeric:tabular-nums}

/* Plain tool layout: system fonts, flat panels, no hero. */
html,body,.stApp,h1,h2,h3,p,.sc-h2{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif!important}
.stApp{background:#f6f8fa}
.sc-top{border-bottom:1px solid var(--line);background:#fff}
.sc-top-in{display:flex;justify-content:space-between;align-items:center;padding-block:12px}
.sc-brand{display:flex;align-items:center;gap:8px;font-weight:600;color:var(--ink)}
.sc-brand svg{width:22px;height:22px}
.sc-by{font-size:.88rem;color:var(--muted)}
.sc-intro{padding-block:18px 4px;color:var(--ink);max-width:1080px}
.sc-label{display:none!important}
.st-key-band-demo,.st-key-band-match,.st-key-band-gap,.st-key-band-table,.st-key-band-products,.st-key-band-spec,.st-key-band-path{background:#f6f8fa!important;border-top:0!important;padding-top:14px!important;padding-bottom:14px!important}
.sc-h2{font-size:1.05rem!important;font-weight:600}
.sc-panel,.sc-type,.sc-scroll,.sc-split,.sc-trend,.sc-docwrap{border-radius:4px!important;box-shadow:none}
.sc-type{background:#fff!important;border:1px solid var(--line)!important}
.sc-type-kicker{text-transform:none!important;letter-spacing:0!important;color:var(--muted)!important;font-weight:500!important}
.sc-chip{border-radius:3px}
.stButton button,.stDownloadButton button{border-radius:4px}
.sc-foot{background:#f6f8fa!important;color:var(--muted)!important;border-top:1px solid var(--line)}
.sc-hx{background:linear-gradient(180deg,#fff,#f6f8fa);border-bottom:1px solid var(--line)}
.sc-hx-in{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:40px;align-items:center;padding-block:36px 40px}
.sc-hx-in>*{min-width:0}
.sc-hx-tag{margin:0 0 10px;font-size:.85rem;font-weight:600;color:var(--accent)}
.sc-hx h1{margin:0;padding:0;font-size:clamp(1.7rem,3.6vw,2.4rem);line-height:1.15;font-weight:650;color:var(--ink)}
.sc-hx-lede{margin:12px 0 0;font-size:1.05rem;color:var(--muted);max-width:52ch}
.sc-hx-visual{position:relative;padding-bottom:28px}
.sc-hx-card{position:absolute;right:0;bottom:0;width:min(270px,70%);background:#fff;border:1px solid var(--line);border-radius:8px;padding:12px 14px;box-shadow:0 10px 28px rgba(20,33,46,.14);display:grid;gap:6px}
.sc-hx-head{font-size:.78rem;font-weight:600;color:var(--muted)}
.sc-hx-row{display:flex;justify-content:space-between;align-items:center;gap:10px;font-size:.85rem;padding-top:6px;border-top:1px solid var(--line)}
@media (max-width:820px){.sc-hx-in{grid-template-columns:1fr;gap:20px}.sc-hx-card{position:static;width:auto;margin-top:12px}.sc-hx-visual{padding-bottom:0}}
.sc-hx{background:radial-gradient(1200px 500px at 85% 20%,rgba(95,208,205,.18),transparent 60%),linear-gradient(135deg,#0d4b55 0%,#102a3f 70%)!important;border-bottom:0;position:relative;overflow:hidden}
.sc-hx::before{content:"";position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.05) 1px,transparent 1px);background-size:32px 32px;pointer-events:none}
.sc-hx-in{position:relative}
.sc-hx-tag{color:#7fe0dc!important}
.sc-hx h1{color:#fff!important}
.sc-hx-lede{color:#c3d3dc!important}
.sc-hx-visual{padding-bottom:0}
.sc-hx-card{bottom:-10px;right:auto;left:-24px;width:min(250px,60%);box-shadow:0 16px 40px rgba(0,0,0,.35)}
.iso-art{width:100%;height:auto;display:block;max-height:340px}
.i-front{fill:#e8eef2}.i-side{fill:#b9c6cf}.i-top{fill:#f6f9fb}.i-door{fill:#dfe7ec;stroke:#a9b8c2;stroke-width:1}
.i-window{fill:#2b3b47;stroke:#8fa1ad}.i-led-g{fill:#34c27a}.i-led-r{fill:#e5534b}.i-led-a{fill:#f2b33d}
.i-plate{fill:#c9d4db}.i-vent{stroke:#a9b8c2;stroke-width:2}.i-handle{stroke:#6b7c88;stroke-width:3;stroke-linecap:round}
.i-shadow{fill:#000;opacity:.28}.i-tray{fill:#9fb0bb}.i-tray-f{fill:#7d8f9b}.i-cable{stroke:#1d2b35;stroke-width:3.5;stroke-linecap:round}
.sketch{width:100%;height:auto;display:block}
.s-ln{fill:none;stroke:#e9f4f6;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}
.s-thin{fill:none;stroke:#cfe6ea;stroke-width:1;stroke-linecap:round;opacity:.85}
.s-dim{fill:none;stroke:#7fe0dc;stroke-width:1;stroke-linecap:round}
.s-dot{fill:none;stroke:#e9f4f6;stroke-width:1.2}
.sketch text{font-family:ui-monospace,SFMono-Regular,Consolas,monospace;fill:#e9f4f6}
.sketch .lbl{font-size:11px}.sketch .dimt{font-size:10px;fill:#7fe0dc}.sketch .num{font-size:10px;opacity:.7}
.sketch .tb{font-size:9px;letter-spacing:.04em}.sketch .tbs{font-size:8px;opacity:.7}
.st-key-band-path{background:#eef3f8!important}.st-key-band-demo{background:#eef7f6!important}
.st-key-band-match{background:#eef8f1!important}.st-key-band-gap{background:#fbf0ee!important}
.st-key-band-table{background:#f3f1f9!important}.st-key-band-products{background:#fbf6ec!important}.st-key-band-spec{background:#f1f3f5!important}
.st-key-band-path,.st-key-band-demo,.st-key-band-match,.st-key-band-gap,.st-key-band-table,.st-key-band-products,.st-key-band-spec{padding-top:22px!important;padding-bottom:22px!important}
.sc-desc{margin:4px 0 12px;color:#5b6670;font-size:.92rem;max-width:62ch}

/* Plain tool look: text status labels, one summary line, square corners */
.sc-chip{background:none!important;padding:0!important;border-radius:0!important;font:600 .78rem "IBM Plex Mono",Consolas,monospace!important;text-transform:uppercase}
.sc-chip.PASS{color:#1d7a46!important}.sc-chip.FAIL{color:#b3261e!important}.sc-chip.REVIEW{color:#9a6200!important}
.sc-panel{border:0!important;background:none!important;padding:0!important;border-radius:0!important}
.sc-panel h2{font-size:1.35rem;font-weight:600;margin:0}
.sc-tally{font:400 .88rem "IBM Plex Mono",Consolas,monospace;color:#5d6b77;margin:4px 0 0}
.sc-tally b{font-weight:500;color:#1b2630}.sc-tally b.bad{color:#b3261e}
.st-key-band-about{background:#fff!important;padding-top:22px!important;padding-bottom:22px!important}
.sc-about{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:28px;margin-top:10px}
.sc-about p{margin:0;max-width:46ch}
.sc-steps{margin:0;padding-left:20px;display:grid;gap:6px}
.sc-steps li::marker{font-family:"IBM Plex Mono",Consolas,monospace;color:#0b6e76}
@media (max-width:760px){.sc-about{grid-template-columns:1fr;gap:12px}}
button,[data-testid="stBaseButton-secondary"],[data-testid="stBaseButton-primary"]{border-radius:3px!important}

/* Small section sketches */
.sc-h2{display:flex!important;align-items:center;gap:10px}
.fig{width:120px;height:46px;margin-left:auto;flex:none;color:#0b6e76}
.f-ln{fill:none;stroke:currentColor;stroke-width:1.4;stroke-linecap:round;stroke-linejoin:round}
.f-thin{fill:none;stroke:currentColor;stroke-width:1;stroke-linecap:round;opacity:.65}
.f-tag{font:8px "IBM Plex Mono",Consolas,monospace;fill:#5d6b77;letter-spacing:.06em}
.sc-res-row{display:flex;gap:16px;align-items:flex-start}.sc-res-row>.sc-panel{flex:1;min-width:0}
.st-key-band-about{padding:22px max(20px,calc((100% - 1040px)/2))!important}
@media (max-width:600px){.fig{width:84px;height:32px}}
.st-key-band-questions{background:#f0f4f1!important;padding:22px max(20px,calc((100% - 1040px)/2))!important}
.sc-qcols{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:28px;margin-top:6px}
.sc-qcols h3{font-size:.95rem;font-weight:600;margin:0 0 6px}
.sc-qcols h4{font:600 .7rem "IBM Plex Mono",Consolas,monospace;text-transform:uppercase;letter-spacing:.07em;color:#5d6b77;margin:10px 0 4px}
.sc-facts{font:400 .85rem "IBM Plex Mono",Consolas,monospace;color:#5d6b77;margin:0 0 8px}
.st-key-band-table [data-testid="stHorizontalBlock"]{background:#fff;border:1px solid #d9dfe4;padding:10px 12px;gap:16px}
.st-key-band-table [data-testid="stButtonGroup"]{justify-content:flex-end}.sc-facts b{font-family:"IBM Plex Sans",sans-serif;font-weight:500;color:#1b2630}
.sc-chip{font:600 .8rem "IBM Plex Sans",sans-serif!important;text-transform:none!important;display:inline-flex;align-items:center;gap:6px}
.sc-chip::before{content:"";width:8px;height:8px;border-radius:50%;background:currentColor}
.sc-table th,table th{text-transform:none!important;letter-spacing:0!important;font-family:"IBM Plex Sans",sans-serif!important}
.sc-tally{font-family:"IBM Plex Sans",sans-serif!important}
.f-tag{display:none}
.sc-summary{display:grid;gap:6px;margin:4px 0 10px;font-size:.9rem;color:#5d6b77}.sc-summary b{color:#1b2630}
.sc-bar{display:flex;height:6px;border-radius:3px;overflow:hidden;background:#e5e9ec;gap:2px}
.sc-bar-PASS{background:#1d7a46}.sc-bar-REVIEW{background:#d9a21b}.sc-bar-FAIL{background:#b3261e}
.sc-matrix tr.sc-grp td{background:#f3f5f7;font-weight:600;font-size:.84rem;color:#1b2630;padding:7px 12px;border-top:1px solid #d9dfe4}
.sc-matrix tr.sc-grp td span{float:right;font-weight:400;color:#5d6b77}
.sc-num{color:#8a96a0;font-variant-numeric:tabular-nums;width:2rem}
.sc-pref{margin-left:8px;font-size:.72rem;font-weight:500;color:#0b6e76;border:1px solid #9cc9cc;border-radius:3px;padding:0 5px;vertical-align:1px}
.sc-ref{color:#5d6b77;font-size:.85rem}.sc-sec{display:block;color:#1b2630;font-size:.78rem}
.sc-ref .sc-quote{font-style:normal}
.sc-why{font-size:.78rem;color:#5d6b77;margin-top:3px;max-width:22ch;line-height:1.35}
.sc-row-FAIL .sc-why{color:#b3261e}.sc-row-REVIEW .sc-why{color:#7a4c0b}
.st-key-band-compare{background:#f2f6fa!important;padding:22px max(20px,calc((100% - 1040px)/2))!important}
.sc-cmp{border-collapse:separate;border-spacing:0;font-size:.84rem;width:max-content;min-width:100%}
.sc-cmp th,.sc-cmp td{padding:7px 10px;border-bottom:1px solid #d9dfe4;text-align:left;vertical-align:top;background:#fff}
.sc-cmp thead th{min-width:120px;max-width:170px;white-space:normal;border-bottom:1px solid #b9c3cb}
.sc-cmp tbody th{position:sticky;left:0;z-index:1;font-weight:500;white-space:nowrap}
.sc-cmp td.need{color:#5d6b77;white-space:nowrap}
.sc-cmp .best{background:#eef6f6}.sc-cmp td.c-FAIL{background:#fdf1ef}
.sc-cmp-name{font-weight:600;line-height:1.3}.sc-cmp-sum{font-size:.74rem;margin-top:3px}
.sc-cmp-sum.ok{color:#1d7a46}.sc-cmp-sum.warn{color:#9a6200}.sc-cmp-sum.bad{color:#b3261e}
.sc-cmp-tag{display:inline-block;margin-top:4px;font-size:.68rem;font-weight:600;color:#fff;background:#0b6e76;border-radius:3px;padding:0 5px}
.sc-mk{display:inline-block;width:1.1rem;font-weight:700}.sc-mk.PASS{color:#1d7a46}.sc-mk.FAIL{color:#b3261e}.sc-mk.REVIEW{color:#9a6200}
.sc-legend{display:flex;flex-wrap:wrap;gap:4px 8px;align-items:center;font-size:.84rem;color:#5d6b77}
.sc-legend .sc-chip{margin-left:8px}.sc-legend .sc-chip:first-child{margin-left:0}
.sc-na{color:#8a96a0;font-size:.8rem;font-style:italic}
.sc-matrix tr.sc-row-REVIEW td{background:#fff!important}.sc-matrix tr.sc-row-REVIEW td:first-child{box-shadow:inset 3px 0 0 #d9a21b}
.sc-matrix tr.sc-row-FAIL td:first-child{box-shadow:inset 3px 0 0 #b3261e}
.sc-ci-name{font-weight:500}.sc-ci-need{font-size:.78rem;color:#5d6b77;font-weight:400}
.sc-cmp-maker{font-size:.72rem;color:#5d6b77;font-weight:500;text-transform:uppercase;letter-spacing:.04em}
.sc-cmp td.c-REVIEW{background:#fff}.sc-cmp td.c-REVIEW.best{background:#eef6f6}
.sc-cmp tbody th{min-width:150px;white-space:normal}
.sc-cmp th.mine,.sc-cmp td.mine{background:#fff8e6!important;border-left:2px solid #d9a21b;border-right:2px solid #d9a21b;font-weight:500}
.sc-res-row{display:grid!important;grid-template-columns:minmax(0,1fr) 200px;gap:24px}
.sc-verdict{font-weight:600;font-size:.92rem;margin:2px 0 6px}.sc-verdict.ok{color:#1d7a46}.sc-verdict.warn{color:#9a6200}.sc-verdict.bad{color:#b3261e}
.sc-closest{font-size:.88rem;margin:0 0 4px}
.sc-score{border-left:1px solid #d9dfe4;padding-left:20px;display:grid;align-content:center;gap:6px}
.sc-score-lbl{font-size:.75rem;color:#5d6b77}.sc-score-num{color:#5d6b77}.sc-score-num b{font-size:2.2rem;font-weight:600;color:#1b2630;line-height:1}
.sc-score-det{display:flex;gap:12px;font-size:.8rem;color:#5d6b77}.sc-score-det .bad{color:#b3261e;font-weight:600}.sc-score-det .warn{color:#9a6200;font-weight:600}
@media (max-width:700px){.sc-res-row{grid-template-columns:1fr}.sc-score{border-left:0;border-top:1px solid #d9dfe4;padding:12px 0 0}}
.st-key-band-table,.st-key-band-products,.st-key-band-compare,.st-key-band-demo,.st-key-band-path,.st-key-band-about{background:#fff!important}
.st-key-band-questions,.st-key-band-spec{background:#f7f8f9!important;border-top:1px solid #b9c3cb!important}
.st-key-band-demo{border-left:4px solid #1f5f9e!important}.st-key-band-table{border-left:4px solid #2b4a6f!important}
.st-key-band-compare{border-left:4px solid #2f6f6a!important}.st-key-band-products{border-left:4px solid #a0522d!important}
.st-key-band-questions{border-top:2px solid #5f6b2e!important}.st-key-band-spec{border-top:2px solid #6b7280!important}
.st-key-band-demo .sc-h2{color:#1f5f9e}.st-key-band-table .sc-h2{color:#2b4a6f}.st-key-band-compare .sc-h2{color:#2f6f6a}
.st-key-band-products .sc-h2{color:#a0522d}.st-key-band-questions .sc-h2{color:#5f6b2e}.st-key-band-spec .sc-h2{color:#6b7280}
.sc-ic{display:inline-grid;place-items:center;width:28px;height:28px;border-radius:6px;flex:none}.sc-ic svg{width:16px;height:16px}
.sc-anchor{display:block;position:relative;top:-12px}
.sc-jump{position:fixed;right:16px;bottom:16px;z-index:1000}
.sc-jump>summary{list-style:none;cursor:pointer;background:#1b2630;color:#fff;font-size:.84rem;font-weight:500;padding:8px 14px;border-radius:2px;box-shadow:0 2px 6px rgba(0,0,0,.2)}
.sc-jump>summary::-webkit-details-marker{display:none}
.sc-jump nav{position:absolute;right:0;bottom:calc(100% + 6px);background:#fff;border:1px solid #b9c3cb;box-shadow:0 4px 14px rgba(0,0,0,.15);min-width:190px;padding:4px 0;display:grid}
.sc-jump nav a{color:#1b2630!important;text-decoration:none!important;padding:6px 14px;font-size:.88rem}
.sc-jump nav a:hover{background:#e3f0f1}
.sc-qspec li::marker{color:#9a6200!important}
.sc-qcols ol{margin:0;padding-left:22px;display:grid;gap:8px}
.sc-qcols li::marker{font-family:"IBM Plex Mono",Consolas,monospace;color:#0b6e76}
@media (max-width:760px){.sc-qcols{grid-template-columns:1fr}}
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

def _hx_cabinet(x: int) -> str:
    return (f'<g transform="translate({x} 24)"><rect width="92" height="150" rx="3" fill="#fff" stroke="#dfe5ea" stroke-width="2"/>'
            '<rect x="10" y="12" width="72" height="46" rx="2" fill="#f6f8fa" stroke="#dfe5ea"/>'
            '<circle cx="26" cy="35" r="5" fill="#2fa36b"/><circle cx="44" cy="35" r="5" fill="#e0a526"/>'
            '<rect x="58" y="27" width="16" height="16" rx="2" fill="#e4f1f2" stroke="#0b6e76"/>'
            '<rect x="10" y="66" width="72" height="72" rx="2" fill="#f6f8fa" stroke="#dfe5ea"/>'
            '<path d="M20 84h52M20 98h52M20 112h52" stroke="#dfe5ea" stroke-width="2"/>'
            '<circle cx="72" cy="128" r="3" fill="#566575"/></g>')


HERO_ART = '<svg class="sketch" viewBox="0 0 658 324" role="img" aria-label="Sketch of a 13.8 kV switchgear front view with dimensions and labels"><rect x="55.5" y="43.3" width="380.0" height="22.0" fill="#d98a4e" fill-opacity="0.55" transform="rotate(-0.09 54.0 40.0)"/><rect x="63.1" y="72.3" width="92.0" height="200.0" fill="#7fb3d5" fill-opacity="0.18" transform="rotate(0.46 60.0 70.0)"/><rect x="80.4" y="95.8" width="56.0" height="30.0" fill="#5cc3c0" fill-opacity="0.45" transform="rotate(-0.58 78.0 94.0)"/><rect x="70.6" y="176.8" width="76.0" height="86.0" fill="#a7b4bf" fill-opacity="0.22" transform="rotate(0.49 68.0 174.0)"/><rect x="153.7" y="72.7" width="92.0" height="200.0" fill="#7fb3d5" fill-opacity="0.18" transform="rotate(-0.15 152.0 70.0)"/><rect x="172.5" y="95.8" width="56.0" height="30.0" fill="#5cc3c0" fill-opacity="0.45" transform="rotate(-0.26 170.0 94.0)"/><rect x="162.5" y="177.4" width="76.0" height="86.0" fill="#a7b4bf" fill-opacity="0.22" transform="rotate(-0.47 160.0 174.0)"/><rect x="246.5" y="73.1" width="92.0" height="200.0" fill="#7fb3d5" fill-opacity="0.18" transform="rotate(0.56 244.0 70.0)"/><rect x="263.9" y="95.8" width="56.0" height="30.0" fill="#5cc3c0" fill-opacity="0.45" transform="rotate(0.53 262.0 94.0)"/><rect x="255.5" y="176.5" width="76.0" height="86.0" fill="#a7b4bf" fill-opacity="0.22" transform="rotate(-0.54 252.0 174.0)"/><rect x="339.4" y="72.3" width="92.0" height="200.0" fill="#7fb3d5" fill-opacity="0.18" transform="rotate(0.49 336.0 70.0)"/><rect x="356.7" y="97.1" width="56.0" height="30.0" fill="#5cc3c0" fill-opacity="0.45" transform="rotate(-0.41 354.0 94.0)"/><rect x="347.1" y="175.9" width="76.0" height="86.0" fill="#a7b4bf" fill-opacity="0.22" transform="rotate(-0.11 344.0 174.0)"/><rect x="457.2" y="267.2" width="190.0" height="20.0" fill="#f2cf6b" fill-opacity="0.55" transform="rotate(-0.38 454.0 264.0)"/><path class="s-thin" d="M117.3 39.2 L117.8 50.9 L117.3 62.5 M180.7 39.4 L180.5 50.9 L180.7 62.3 M244.0 39.5 L244.0 51.2 L244.0 62.9 M307.3 39.3 L307.0 51.1 L307.3 63.0 M370.7 39.3 L371.0 50.9 L370.7 62.5 M67.1 80.0 L105.8 80.1 L144.4 80.0 M144.0 79.9 L144.2 123.0 L144.0 166.2 M144.0 166.0 L105.9 165.6 L67.9 166.0 M68.0 166.1 L67.9 122.9 L68.0 79.7 M77.2 94.0 L105.8 93.6 L134.5 94.0 M134.0 93.7 L134.5 108.9 L134.0 124.2 M134.5 124.0 L106.0 123.5 L77.5 124.0 M78.0 124.7 L77.7 109.2 L78.0 93.6 M67.5 174.0 L105.9 174.5 L144.3 174.0 M144.0 173.2 L144.3 217.0 L144.0 260.7 M144.4 260.0 L106.2 259.8 L68.0 260.0 M68.0 260.4 L68.5 216.7 L68.0 173.0 M79.8 214.0 L106.0 214.4 L132.2 214.0 M79.2 222.0 L105.9 222.2 L132.7 222.0 M79.1 230.0 L105.9 230.3 L132.8 230.0 M79.7 238.0 L106.3 238.4 L133.0 238.0 M160.0 80.0 L198.1 80.1 L236.2 80.0 M236.0 79.5 L236.4 123.1 L236.0 166.8 M236.2 166.0 L197.7 165.7 L159.2 166.0 M160.0 166.4 L160.0 123.0 L160.0 79.5 M169.5 94.0 L198.0 94.4 L226.5 94.0 M226.0 93.7 L225.7 109.3 L226.0 124.9 M226.1 124.0 L198.0 123.8 L169.9 124.0 M170.0 124.9 L170.2 109.1 L170.0 93.3 M159.1 174.0 L197.7 174.0 L236.2 174.0 M236.0 173.2 L236.0 216.8 L236.0 260.4 M236.2 260.0 L197.7 260.1 L159.3 260.0 M160.0 260.3 L159.6 216.9 L160.0 173.5 M171.2 214.0 L197.7 214.3 L224.1 214.0 M171.7 222.0 L198.1 221.8 L224.4 222.0 M171.9 230.0 L198.2 229.6 L224.6 230.0 M171.3 238.0 L197.7 238.3 L224.1 238.0 M251.3 80.0 L289.8 79.6 L328.4 80.0 M328.0 79.3 L328.4 122.7 L328.0 166.2 M328.9 166.0 L290.3 166.0 L251.7 166.0 M252.0 166.4 L252.5 122.7 L252.0 79.0 M261.8 94.0 L290.0 93.9 L318.3 94.0 M318.0 93.5 L318.5 109.0 L318.0 124.5 M318.1 124.0 L290.0 124.3 L262.0 124.0 M262.0 124.5 L262.2 108.9 L262.0 93.3 M251.6 174.0 L290.3 174.1 L329.0 174.0 M328.0 173.2 L327.8 216.9 L328.0 260.6 M328.1 260.0 L289.8 259.7 L251.5 260.0 M252.0 260.9 L251.7 217.1 L252.0 173.3 M263.9 214.0 L290.0 214.1 L316.1 214.0 M263.4 222.0 L289.9 222.2 L316.5 222.0 M263.5 230.0 L290.1 229.8 L316.7 230.0 M263.9 238.0 L290.3 238.5 L316.7 238.0 M343.2 80.0 L382.0 80.4 L420.9 80.0 M420.0 80.0 L420.0 123.2 L420.0 166.5 M420.1 166.0 L381.9 165.7 L343.7 166.0 M344.0 166.1 L344.4 122.7 L344.0 79.3 M353.6 94.0 L382.3 93.9 L411.0 94.0 M410.0 94.0 L410.2 109.4 L410.0 124.8 M410.2 124.0 L381.9 123.5 L353.5 124.0 M354.0 124.8 L354.4 108.9 L354.0 93.1 M343.3 174.0 L382.0 174.1 L420.7 174.0 M420.0 174.0 L420.0 217.0 L420.0 260.1 M420.3 260.0 L381.7 260.2 L343.0 260.0 M344.0 260.4 L343.7 217.1 L344.0 173.8 M355.5 214.0 L382.2 213.6 L408.9 214.0 M355.8 222.0 L382.1 221.8 L408.3 222.0 M355.4 230.0 L382.1 230.0 L408.7 230.0 M355.6 238.0 L381.8 237.6 L408.1 238.0 M40.7 271.5 L35.1 276.0 L29.5 280.5 M68.0 271.5 L62.8 276.2 L57.8 280.6 M96.1 271.8 L91.0 276.5 L85.5 280.4 M124.4 271.6 L119.0 276.3 L113.7 280.1 M152.2 271.7 L146.5 276.1 L141.3 280.4 M180.2 271.8 L174.8 276.5 L169.2 280.4 M208.4 271.6 L202.9 275.5 L197.7 280.2 M236.2 272.0 L230.8 276.4 L225.7 280.3 M264.6 271.5 L258.8 276.0 L253.6 280.1 M292.6 271.9 L287.4 275.8 L281.8 280.5 M320.4 271.9 L315.0 275.7 L309.8 280.3 M348.1 271.8 L343.2 276.5 L337.8 280.6 M376.0 271.8 L370.5 275.8 L365.3 280.6 M404.7 271.8 L399.1 276.6 L393.9 280.6 M453.1 264.0 L501.0 264.3 L549.0 263.6 L596.9 264.1 L644.9 264.0 M644.0 263.6 L644.2 292.9 L644.0 322.2 M644.7 322.0 L597.0 322.3 L549.3 322.3 L501.7 322.0 L454.0 322.0 M454.0 322.1 L454.1 292.8 L454.0 263.4 M453.8 284.0 L501.5 284.5 L549.1 284.1 L596.8 283.9 L644.4 284.0 M574.0 283.0 L573.8 302.6 L574.0 322.2"/><path class="s-ln" d="M53.2 40.0 L95.7 39.8 L138.2 40.0 L180.7 39.9 L223.2 39.3 L265.7 40.6 L308.1 39.5 L350.6 40.8 L393.1 39.8 L435.6 40.0 M434.0 39.9 L434.6 51.3 L434.0 62.7 M434.8 62.0 L392.4 62.2 L350.1 62.8 L307.7 62.5 L265.3 62.1 L223.0 61.8 L180.6 62.4 L138.3 61.6 L95.9 61.9 L53.5 62.0 M54.0 64.2 L54.9 51.7 L54.0 39.3 M59.9 70.0 L106.1 70.7 L152.3 70.0 M152.0 68.9 L151.4 109.5 L152.4 150.2 L152.3 190.9 L151.2 231.5 L152.0 272.2 M152.4 270.0 L105.9 270.4 L59.4 270.0 M60.0 271.0 L60.8 230.6 L60.0 190.1 L60.3 149.6 L60.7 109.1 L60.0 68.6 M136.0 199.6 L135.3 210.0 L136.0 220.4 M151.6 70.0 L199.0 70.1 L246.5 70.0 M244.0 70.0 L244.0 110.3 L244.1 150.6 L243.4 191.0 L244.4 231.3 L244.0 271.6 M244.6 270.0 L198.0 269.3 L151.4 270.0 M152.0 271.1 L151.9 230.5 L152.0 189.8 L152.0 149.1 L151.9 108.4 L152.0 67.7 M228.0 197.9 L228.1 210.0 L228.0 222.2 M242.6 70.0 L289.6 69.5 L336.7 70.0 M336.0 69.6 L336.3 109.8 L335.5 150.0 L336.0 190.1 L336.3 230.3 L336.0 270.5 M336.6 270.0 L289.4 270.0 L242.2 270.0 M244.0 270.3 L244.0 230.0 L243.8 189.7 L244.3 149.5 L243.7 109.2 L244.0 68.9 M320.0 199.0 L319.5 210.4 L320.0 221.7 M334.4 70.0 L381.4 69.6 L428.4 70.0 M428.0 70.0 L427.7 110.1 L427.7 150.3 L428.0 190.4 L428.1 230.5 L428.0 270.7 M430.2 270.0 L381.9 270.1 L333.6 270.0 M336.0 272.4 L335.5 231.8 L335.5 191.2 L335.4 150.6 L336.8 109.9 L336.0 69.3 M412.0 198.4 L412.4 209.5 L412.0 220.5 M35.0 270.0 L76.9 269.1 L118.9 270.4 L160.8 270.0 L202.8 269.1 L244.7 270.8 L286.6 270.6 L328.6 269.5 L370.5 269.4 L412.4 270.3 L454.4 270.0"/><path class="s-dim" d="M59.3 304.0 L100.3 303.5 L141.3 303.9 L182.3 303.6 L223.4 303.7 L264.4 304.3 L305.4 303.9 L346.4 304.0 L387.4 304.4 L428.4 304.0 M60.0 297.6 L60.1 303.8 L60.0 310.0 M428.0 298.0 L427.6 304.0 L428.0 310.1 M59.3 304.3 L64.0 302.7 L68.3 300.9 M59.8 303.7 L64.2 305.7 L68.3 307.1 M428.9 304.2 L423.9 302.6 L419.1 301.0 M428.9 303.7 L424.3 305.4 L419.6 307.1 M30.0 69.8 L29.7 110.0 L29.9 150.2 L30.2 190.4 L29.7 230.6 L30.0 270.7 M23.8 70.0 L30.0 70.1 L36.2 70.0 M23.7 270.0 L30.3 269.6 L36.9 270.0 M30.0 69.5 L28.6 74.0 L26.8 78.4 M29.8 69.4 L31.4 73.9 L33.3 78.8 M30.3 270.3 L28.8 266.1 L26.8 261.7 M29.9 270.2 L31.6 265.6 L33.1 261.2 M381.6 110.0 L420.1 110.2 L458.5 110.0 M423.0 51.0 L440.7 51.4 L458.5 51.0 M382.0 230.0 L420.0 230.1 L458.1 230.0"/><circle class="s-dot" cx="81.8" cy="140.0" r="3.6"/><circle class="s-dot" cx="93.9" cy="140.0" r="3.6"/><circle class="s-dot" cx="106.0" cy="140.0" r="3.6"/><circle class="s-dot" cx="173.9" cy="140.0" r="3.6"/><circle class="s-dot" cx="185.8" cy="140.0" r="3.6"/><circle class="s-dot" cx="197.8" cy="140.0" r="3.6"/><circle class="s-dot" cx="266.1" cy="140.0" r="3.6"/><circle class="s-dot" cx="278.2" cy="140.0" r="3.6"/><circle class="s-dot" cx="289.7" cy="140.0" r="3.6"/><circle class="s-dot" cx="358.0" cy="140.0" r="3.6"/><circle class="s-dot" cx="370.2" cy="140.0" r="3.6"/><circle class="s-dot" cx="381.7" cy="140.0" r="3.6"/><circle class="s-dot" cx="382.2" cy="110.0" r="2.2"/><circle class="s-dot" cx="423.8" cy="51.0" r="2.2"/><circle class="s-dot" cx="382.1" cy="230.0" r="2.2"/><text class="num" x="106.0" y="284.0" text-anchor="middle">1</text><text class="num" x="198.0" y="284.0" text-anchor="middle">2</text><text class="num" x="290.0" y="284.0" text-anchor="middle">3</text><text class="num" x="382.0" y="284.0" text-anchor="middle">4</text><text class="dimt" x="244.0" y="298.0" text-anchor="middle">144 in.</text><text class="dimt" x="24.0" y="170.0" text-anchor="middle" transform="rotate(-90 24.0 170.0)">95 in.</text><text class="lbl" x="464.0" y="114.0" text-anchor="start">Main breaker, 3000 A</text><text class="lbl" x="464.0" y="55.0" text-anchor="start">Copper bus, 40 kA</text><text class="lbl" x="464.0" y="234.0" text-anchor="start">NEMA 1 enclosure</text><text class="tb" x="462.0" y="278.0" text-anchor="start">13.8 kV SWITCHGEAR · FRONT VIEW</text><text class="tb" x="462.0" y="300.0" text-anchor="start">SPECCHECK</text><text class="tbs" x="462.0" y="314.0" text-anchor="start">NOT TO SCALE</text><text class="tb" x="582.0" y="300.0" text-anchor="start">DWG SC-101</text><text class="tbs" x="582.0" y="314.0" text-anchor="start">REV A</text></svg>'

HEADER = f"""
<header class="sc-top" id="top"><div class="sc-wrap sc-top-in"><div class="sc-brand">{LOGO}<span>SpecCheck AI</span></div><span class="sc-by">Brian Oh</span></div></header>
<section class="sc-hx"><div class="sc-wrap sc-hx-in">
<div class="sc-hx-copy">
<p class="sc-kicker-serif">Spec review for power equipment</p>
<h1>Check a customer spec in minutes</h1>
<p class="sc-hx-lede">SpecCheck reads a power-equipment spec and checks every item against real products, so you see which one fits and what is missing.</p>
<p class="sc-cta"><a class="sc-cta-main" href="#sec-samples" target="_self">Try a sample spec</a></p>
<p class="sc-cta-note"><span>Pass, fail, or review for every item</span></p></div>
<div class="sc-hx-visual">{HERO_ART}</div>
<ol class="sc-hsteps"><li><b>Step 1: Upload the spec</b>Drop in the customer's PDF, plus any addenda.</li><li><b>Step 2: Pull out the requirements</b>Claude lists every rating and option, with the spec's exact wording.</li><li><b>Step 3: Check the products</b>Each requirement is compared to the catalog: pass, fail, or needs a look.</li><li><b>Step 4: See the results</b>Best fit, what's missing, and what to ask the customer.</li></ol>
</div></section>
"""


# Simple line icons (Lucide, ISC license) shown next to section titles.
ICON_PATHS = {
    "live": "<path d=\"M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4\"/><polyline points=\"17 8 12 3 7 8\"/><line x1=\"12\" x2=\"12\" y1=\"3\" y2=\"15\"/>",
    "check": "<rect width=\"8\" height=\"4\" x=\"8\" y=\"2\" rx=\"1\"/><path d=\"M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2\"/><path d=\"m9 14 2 2 4-4\"/>",
    "compare": "<rect width=\"18\" height=\"18\" x=\"3\" y=\"3\" rx=\"2\"/><path d=\"M9 3v18\"/><path d=\"M15 3v18\"/>",
    "cost": "<polyline points=\"22 7 13.5 15.5 8.5 10.5 2 17\"/><polyline points=\"16 7 22 7 22 13\"/>",
    "questions": "<path d=\"M7.9 20A9 9 0 1 0 4 16.1L2 22Z\"/><path d=\"M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3\"/><path d=\"M12 17h.01\"/>",
    "spec": "<path d=\"M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z\"/><path d=\"M14 2v4a2 2 0 0 0 2 2h4\"/><path d=\"M16 13H8\"/><path d=\"M16 17H8\"/><path d=\"M10 9H8\"/>"
}


def icon(name: str, color: str) -> str:
    return (f'<span class="sc-ic" style="color:{color};background:{color}22" aria-hidden="true">'
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round">{ICON_PATHS[name]}</svg></span>')


# ---- Look matched to the website: graph-paper background, white section cards,
# ---- numbered colored headers with line drawings, colored tabs, tables, and charts.
import json as _json
from pathlib import Path as _Path

SECTION_ART = _json.loads((_Path(__file__).parent / "section_art.json").read_text(encoding="utf-8"))
SECTION_COLOR = {"live": "#1f5f9e", "check": "#2b4a6f", "compare": "#2f6f6a", "cost": "#a0522d",
                 "questions": "#5f6b2e", "spec": "#6b7280"}


def section_head(name: str, title: str, number: int) -> str:
    """Numbered section title in the section's color, with its drawing on the right."""
    art = SECTION_ART[name].replace("<svg ", '<svg aria-hidden="true" ', 1)
    return (f'<div class="sc-h2 sc-sh" style="--sc:{SECTION_COLOR[name]}">'
            f'<span class="sc-shn">{number:02d}</span><span class="sc-sht">{title}</span>{art}</div>')


_CARDS = ".st-key-band-table,.st-key-band-compare,.st-key-band-products,.st-key-band-spec,.st-key-band-questions"

CSS += """<style>
/* Page: light blue-gray graph paper */
.stApp,[data-testid="stAppViewContainer"],[data-testid="stMain"]{background-color:#e8edf0!important;
 background-image:linear-gradient(rgba(42,93,143,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(42,93,143,.06) 1px,transparent 1px)!important;
 background-size:24px 24px!important;background-attachment:fixed!important}
.st-key-band-about,.st-key-band-demo,.st-key-band-path{background:transparent!important;border:0!important}

/* Sections become white cards with a colored top rule */
""" + _CARDS + """{background:#fff!important;border:1px solid #d6dde3!important;border-top:3px solid var(--sc)!important;
 border-radius:6px!important;box-shadow:0 1px 3px rgba(20,40,60,.08)!important;
 margin:14px max(16px,calc((100% - 1240px)/2))!important;width:auto!important;padding:0 20px 20px!important;overflow:hidden}
.st-key-band-table{--sc:#2b4a6f}.st-key-band-compare{--sc:#2f6f6a}.st-key-band-products{--sc:#a0522d}
.st-key-band-questions{--sc:#5f6b2e}.st-key-band-spec{--sc:#6b7280}
""" + ",".join(s + " .sc-label" for s in _CARDS.split(",")) + """{display:none!important}
.st-key-band-match,.st-key-band-gap{margin:14px max(16px,calc((100% - 1240px)/2))!important;width:auto!important;
 border-radius:6px!important;border:1px solid #cfe3d6!important;border-left:4px solid #2f8a57!important;padding:18px 20px!important;box-shadow:0 1px 3px rgba(20,40,60,.08)}
.st-key-band-gap{border-color:#efd3cf!important;border-left-color:#b3261e!important}

.sc-matrix .sc-sec{padding-block:0!important}
/* Keep the header flush with the card top: anchors take no space, labels are hidden in cards */
""" + _CARDS + """{position:relative}
""" + ",".join(c + ' [data-testid="stElementContainer"]:has(.sc-anchor)' for c in _CARDS.split(",")) + """{position:absolute!important;height:0!important;margin:0!important}
""" + ",".join(c + ' [data-testid="stElementContainer"]:has(.sc-label)' for c in _CARDS.split(",")) + """{display:none!important}

/* Numbered header bar with a drawing */
.sc-sh{display:flex!important;align-items:center;gap:12px;margin:0 -20px 14px!important;padding:10px 20px!important;
 background:color-mix(in srgb,var(--sc) 6%,#fff);border-bottom:1px solid color-mix(in srgb,var(--sc) 22%,#d9dfe4);
 color:var(--sc)!important;font-size:1.05rem!important;font-weight:600;min-height:58px}
.sc-shn{font:600 .78rem "IBM Plex Mono",Consolas,monospace;color:var(--sc);padding-right:12px;border-right:1px solid color-mix(in srgb,var(--sc) 35%,#d9dfe4)}
.sc-sh .sec-art{width:150px;height:auto;margin-left:auto;margin-block:-8px;flex:none;color:var(--sc);opacity:.8}
@media (max-width:640px){.sc-sh .sec-art{width:96px}}

/* Sample tabs: one muted color per equipment type */
.st-key-sample button{--c:#2a5d8f;border-color:color-mix(in srgb,var(--c) 40%,#d9dfe4)!important;
 background:color-mix(in srgb,var(--c) 5%,#fff)!important;color:color-mix(in srgb,var(--c) 70%,#1b2630)!important;
 box-shadow:inset 0 -2px 0 color-mix(in srgb,var(--c) 55%,transparent)}
.st-key-sample button:nth-of-type(2){--c:#9a6418}
.st-key-sample button:nth-of-type(3),.st-key-sample button:nth-of-type(4),.st-key-sample button:nth-of-type(5){--c:#5d4f8c}
.st-key-sample button:nth-of-type(6){--c:#2f6f6a}.st-key-sample button:nth-of-type(7){--c:#3f7344}.st-key-sample button:nth-of-type(8){--c:#8a3b52}
.st-key-sample button:hover{border-color:var(--c)!important}
.st-key-sample button[aria-checked="true"],.st-key-sample button[aria-pressed="true"]{background:var(--c)!important;border-color:var(--c)!important;color:#fff!important;box-shadow:none}
.st-key-sample button[aria-checked="true"] *,.st-key-sample button[aria-pressed="true"] *{color:#fff!important}

/* Requirement table: colored group bands and result pills */
.sc-matrix tr.sc-grp{--g:#2a5d8f}
.sc-matrix tr.sc-grp[data-g="Construction"]{--g:#9a6418}.sc-matrix tr.sc-grp[data-g="Standards"]{--g:#5d4f8c}
.sc-matrix tr.sc-grp[data-g="Site and size"]{--g:#2f6f6a}.sc-matrix tr.sc-grp[data-g="Delivery and price"]{--g:#3f7344}
.sc-matrix tr.sc-grp[data-g="Other"]{--g:#6b7280}
.sc-matrix tr.sc-grp td{background:color-mix(in srgb,var(--g) 10%,#fff)!important;color:var(--g)!important;box-shadow:inset 4px 0 0 var(--g)}
.sc-matrix tr.sc-grp td span{color:color-mix(in srgb,var(--g) 70%,#5d6b77)!important}
.sc-chip{padding:2px 9px 2px 7px!important;border-radius:999px!important}
.sc-chip.PASS{background:#1d7a4621!important}.sc-chip.REVIEW{background:#9a620026!important}.sc-chip.FAIL{background:#b3261e21!important}

/* Compare table: tinted cells */
.sc-cmp td.c-PASS{background:#f1f8f4}.sc-cmp td.c-REVIEW{background:#fbf6ec}
.sc-cmp td.best{box-shadow:inset 2px 0 0 #0b6e76,inset -2px 0 0 #0b6e76}

/* Price charts: one color per material */
.sc-trend{--m:#2f6f6a;box-shadow:inset 3px 0 0 var(--m)}
.sc-trend[data-m="Copper"]{--m:#b5652b}.sc-trend[data-m="Aluminum"]{--m:#5b7c99}.sc-trend[data-m="Lead"]{--m:#5e6470}
.sc-trend[data-m="Nickel"]{--m:#4f7f5a}.sc-trend[data-m="Steel"]{--m:#46566b}.sc-trend[data-m="Electrical steel"]{--m:#6d5a8f}
.sc-trend[data-m="Transformer oil"]{--m:#a07a1f}.sc-trend[data-m="Brent crude oil"]{--m:#3b3b3b}
.sc-trend > .sc-tag:first-child{color:var(--m)!important}
.sc-trend svg polyline{stroke:var(--m)!important}.sc-trend svg polygon{fill:var(--m)!important;opacity:.14}
.sc-trend svg circle[r="4"]{fill:var(--m)!important}

/* Question cards: colored headers per audience */
.sc-qcols>div{border:1px solid #d9dfe4;border-radius:6px;overflow:hidden;background:#fff}
.sc-qcols>div:first-child{--qc:#1f5f9e}.sc-qcols>div:last-child{--qc:#2f6f6a}
.sc-qcols h3{margin:0 0 4px!important;padding:10px 14px;background:color-mix(in srgb,var(--qc) 10%,#fff);color:var(--qc)!important;
 box-shadow:inset 4px 0 0 var(--qc);border-bottom:1px solid #d9dfe4}
.sc-qcols h4{margin:10px 14px 4px!important;color:var(--qc)!important}
.sc-qcols h4:nth-of-type(2){color:#9a6418!important}
.sc-qcols ol{margin:0 14px 10px 14px!important}
.sc-qcols li::marker{color:var(--qc)!important;font-weight:600}.sc-qcols .sc-qspec li::marker{color:#9a6418!important}
</style>"""


# ---- Bright studio look (matches the website): warm cream page, pastel hero glow, thin headline,
# ---- white cards, soft pastel step cards, dark text everywhere for easy reading.
CSS += """<style>
html,body,.stApp,[data-testid="stAppViewContainer"],[data-testid="stMain"]{background:#faf7f2!important;background-image:none!important;color:#1f2328!important;font-family:"Inter",-apple-system,"Segoe UI",sans-serif!important}
.stApp p,.stApp li,.stApp label,.stApp button,.stApp input,.stApp select,.stApp td,.stApp th{font-family:"Inter",-apple-system,"Segoe UI",sans-serif}


.sc-top{background:transparent!important;border-bottom:0!important;position:relative;z-index:2;margin-bottom:-70px}
.sc-brand,.sc-by{background:rgba(255,255,255,.75);border:1px solid rgba(31,35,40,.08);border-radius:999px;box-shadow:0 2px 10px rgba(31,35,40,.06);backdrop-filter:blur(12px)}
.sc-brand{padding:8px 20px 8px 10px;display:flex;align-items:center;gap:10px}
.sc-brand span,.sc-by{font:600 .8rem "Inter",sans-serif!important;text-transform:uppercase;letter-spacing:.04em;color:#1f2328!important}
.sc-by{padding:12px 22px}


.sc-hx{background:radial-gradient(110% 85% at 75% 0%,#ffd9c4 0%,#ffe9d6 22%,#f3ecff 52%,#e8f3ff 78%,#faf7f2 100%)!important;border-bottom:0!important}
.sc-hx::before{display:none!important}
.sc-hx-in{display:flex!important;flex-direction:column;align-items:center;text-align:center;gap:18px!important;padding-block:110px 56px!important}
.sc-hx-copy{display:flex;flex-direction:column;align-items:center;gap:14px}
.sc-kicker-serif{margin:0;font:400 1.2rem "Instrument Serif",Georgia,serif;color:#4a4440}
.sc-hx h1{font-family:"Inter Tight","Inter",sans-serif!important;font-weight:300!important;font-size:clamp(2.4rem,6vw,4.6rem)!important;line-height:1.04!important;letter-spacing:-.045em!important;color:#1f2328!important;max-width:15ch;margin:0!important}
.sc-hx-lede{color:#4d5157!important;max-width:48ch;margin:0!important}
.sc-cta{margin:12px 0 0}
.sc-cta-main{display:inline-block;background:#1f2328;color:#fff!important;text-decoration:none!important;font:500 .82rem "Inter",sans-serif;text-transform:uppercase;letter-spacing:.03em;padding:20px 28px;border-radius:4px}
.sc-cta-main:hover{background:#3a3f47}
.sc-cta-note{display:flex;gap:8px 26px;justify-content:center;flex-wrap:wrap;margin:0;font-size:.86rem;color:#4d5157}
.sc-cta-note span::before{content:"✓";color:#1c7c49;margin-right:6px}
.sc-hx-visual{width:min(760px,100%);background:rgba(255,255,255,.65);border:1px solid rgba(31,35,40,.08);border-radius:12px;padding:26px 24px 18px!important;margin-top:28px;box-shadow:0 24px 60px rgba(120,90,60,.14)}
.sc-hx-visual svg{width:100%;height:auto}
.sc-hsteps{list-style:none;padding:0;margin:40px 0 0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;width:100%;text-align:left}
.sc-hsteps li{border-radius:10px;padding:22px 20px 26px;min-height:140px;border:1px solid rgba(31,35,40,.06);color:#4d5157;font-size:.9rem;box-shadow:0 6px 18px rgba(31,35,40,.05)}
.sc-hsteps li b{display:block;font:500 1.08rem/1.25 "Inter Tight","Inter",sans-serif;color:#1f2328;margin-bottom:8px}
.sc-hsteps li:nth-child(1){background:linear-gradient(165deg,#dbeeff,#f2f8ff)}
.sc-hsteps li:nth-child(2){background:linear-gradient(165deg,#e9e2ff,#f6f2ff)}
.sc-hsteps li:nth-child(3){background:linear-gradient(165deg,#ffe8c7,#fff5e6)}
.sc-hsteps li:nth-child(4){background:linear-gradient(165deg,#d9f2e1,#f0faf3)}
@media (max-width:860px){.sc-hsteps{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:520px){.sc-hsteps{grid-template-columns:1fr}.sc-hsteps li{min-height:0}.sc-hx-in{padding-top:90px!important}}


.st-key-band-about{display:none!important}
.sc-hx-visual .s-ln{stroke:#2f3740!important}.sc-hx-visual .s-thin{stroke:#56606b!important}.sc-hx-visual .s-dim{stroke:#0b6e76!important}
.sc-hx-visual .s-dot{fill:#2f3740!important;stroke:#2f3740!important}.sc-hx-visual text{fill:#2f3740!important}.sc-hx-visual text.dimt{fill:#0b6e76!important}
.sc-hx-visual svg rect[fill]{fill-opacity:.55}
.sc-cta-note span{margin:0 12px}
.sc-hx-visual{background:transparent!important;border:0!important;box-shadow:none!important}
@media (min-width:1100px){.sc-hx{margin-left:-64px!important;padding-left:64px!important}}
.sc-rail{position:fixed;left:14px;top:50%;transform:translateY(-50%);z-index:40;display:flex;flex-direction:column;gap:2px;padding:8px;background:rgba(255,255,255,.9);border:1px solid #ebe5db;border-radius:16px;box-shadow:0 8px 24px rgba(31,35,40,.08);backdrop-filter:blur(10px)}
.sc-rail a{position:relative;display:grid;place-items:center;width:40px;height:40px;border-radius:10px;color:#5d6168;text-decoration:none}
.sc-rail a svg{width:20px;height:20px}
.sc-rail a:hover{background:#f3eee6;color:#1f2328}
.sc-rail a.on{background:#1f2328;color:#fff}
.sc-rail a span{position:absolute;left:50px;top:50%;transform:translateY(-50%);white-space:nowrap;background:#1f2328;color:#fff;font:500 .78rem "Inter",sans-serif;padding:6px 10px;border-radius:8px;opacity:0;pointer-events:none;transition:opacity .12s}
.sc-rail a:hover span,.sc-rail a:focus-visible span{opacity:1}
@media (max-width:1099px){.sc-rail{display:none!important}}
@media (min-width:1100px){[data-testid="stMain"]{padding-left:64px!important}.sc-jump{display:none!important}}
.sc-rail{background:linear-gradient(180deg,rgba(255,255,255,.95),rgba(250,244,236,.95))!important}
.sc-rail a:nth-of-type(1){--rc:#6b7280}
.sc-rail a:nth-of-type(2){--rc:#3d6fb6}
.sc-rail a:nth-of-type(3){--rc:#4a7bd0}
.sc-rail a:nth-of-type(4){--rc:#2f9a5f}
.sc-rail a:nth-of-type(5){--rc:#7a5cc2}
.sc-rail a:nth-of-type(6){--rc:#2f8f86}
.sc-rail a:nth-of-type(7){--rc:#c0703a}
.sc-rail a:nth-of-type(8){--rc:#8a8f2e}
.sc-rail a:nth-of-type(9){--rc:#b4577a}
.sc-rail a{color:var(--rc)!important;background:color-mix(in srgb,var(--rc) 10%,#fff)!important;margin:2px 0}
.sc-rail a:hover{background:color-mix(in srgb,var(--rc) 20%,#fff)!important;color:var(--rc)!important}
.sc-rail a.on{background:var(--rc)!important;color:#fff!important;box-shadow:0 4px 12px color-mix(in srgb,var(--rc) 35%,transparent)}
.sc-rail a span{background:var(--rc)!important}
.sc-matrix{border-collapse:collapse!important;border:1px solid #d9d1c4!important}
.sc-matrix th,.sc-matrix td{border:1px solid #e3dcd0!important}
.sc-matrix thead th{border-bottom:2px solid #d4ccbf!important}
.sc-matrix tr.sc-grp td{border-left:1px solid #e3dcd0!important}
.sc-cmp{border-collapse:collapse!important}
.sc-cmp th,.sc-cmp td{border:1px solid #e3dcd0!important}
.stApp [data-testid="stButtonGroup"] button[aria-checked="true"]{background:#1f2328!important;border-color:#1f2328!important;color:#fff!important}
.stApp [data-testid="stButtonGroup"] button[aria-checked="true"] p,.stApp [data-testid="stButtonGroup"] button[aria-checked="true"] span{color:#fff!important}


""" + _CARDS + """{background:#fff!important;border:1px solid #ebe5db!important;border-top:1px solid #ebe5db!important;border-radius:10px!important;box-shadow:0 8px 24px rgba(31,35,40,.05)!important}
.sc-sh{background:transparent!important;border-bottom:0!important;color:#1f2328!important;font:300 2rem/1.15 "Inter Tight","Inter",sans-serif!important;letter-spacing:-.035em;padding:26px 20px 6px!important;min-height:0}
.sc-shn{display:none!important}
.sc-sh .sec-art{opacity:.7}
.st-key-band-match,.st-key-band-gap{background:linear-gradient(160deg,#e3f5e9,#f4fbf6)!important;border:1px solid #cbe8d5!important;border-left:1px solid #cbe8d5!important;border-radius:10px!important}
.st-key-band-gap{background:linear-gradient(160deg,#fde6e3,#fff4f2)!important;border-color:#f3cfca!important}
.st-key-band-demo .sc-h2,.st-key-band-demo .sc-h2 span{font-family:"Inter Tight","Inter",sans-serif!important;font-weight:400!important;color:#1f2328!important}


.stApp [data-testid="stBaseButton-primary"],.stApp [data-testid="stDownloadButton"] button{background:#1f2328!important;border-color:#1f2328!important;color:#fff!important;border-radius:4px!important;text-transform:uppercase;font-size:.8rem!important;letter-spacing:.03em}
.st-key-sample button{border-radius:999px!important;box-shadow:none!important}
.sc-matrix thead th,.sc-cmp thead th{background:#f5f0e8!important}
.sc-jump>summary,.sc-jump summary{background:rgba(31,35,40,.88)!important;color:#fff!important;border-radius:999px!important}
</style>"""

# Streamlit treats a blank line as the end of an HTML block, so keep the styles free of blank lines.
CSS = "\n".join(line for line in CSS.splitlines() if line.strip())
