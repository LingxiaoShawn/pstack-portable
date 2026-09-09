#!/usr/bin/env python3
"""Render a grounded brief as a dependency-free, scrollable HTML presentation."""
import argparse
import html
import json
from pathlib import Path
from urllib.parse import urlparse


def text(value, field):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a nonempty string")
    return html.escape(value)


def strings(value, field):
    if not isinstance(value, list) or not value:
        raise ValueError(f"{field} must be a nonempty list")
    return [text(item, field) for item in value]


def render(data):
    if not isinstance(data, dict):
        raise ValueError("brief must be a JSON object")
    title = text(data.get("title"), "title")
    summary = text(data.get("summary"), "summary")
    problem = text(data.get("problem"), "problem")
    language = data.get("language", "en")
    if language not in {"en", "zh"}:
        raise ValueError("language must be en or zh")
    labels = (["问题", "结构", "一个例子", "验证与依据", "之前", "之后", "仍不确定", "上一页", "下一页", "显示全部"]
              if language == "zh" else
              ["The problem", "The structure", "One example", "Checks and sources", "Before", "After", "Uncertainties", "Previous", "Next", "Show all"])
    before = strings(data.get("before"), "before")
    after = strings(data.get("after"), "after")
    example = strings(data.get("example"), "example")
    verification = strings(data.get("verification"), "verification")
    uncertainties = strings(data["uncertainties"], "uncertainties") if data.get("uncertainties") else []
    sources = data.get("sources")
    if not isinstance(sources, list) or not sources:
        raise ValueError("sources must contain at least one inspected file or URL")
    source_html = []
    for source in sources:
        if not isinstance(source, dict):
            raise ValueError("each source must be an object")
        label = text(source.get("label"), "source label")
        location = text(source.get("location"), "source location")
        raw = source["location"]
        parsed = urlparse(raw)
        if parsed.scheme in {"https", "http"} and parsed.netloc:
            source_html.append(f'<li><a href="{location}" rel="noreferrer">{label}</a></li>')
        else:
            source_html.append(f'<li>{label}<code>{location}</code></li>')

    def items(values):
        return "<ul>" + "".join(f"<li>{v}</li>" for v in values) + "</ul>"

    sections = [
        f'<h1>{title}</h1><p class="summary">{summary}</p>',
        f'<h2>{labels[0]}</h2><p>{problem}</p>',
        f'<h2>{labels[1]}</h2><div class="comparison"><article><h3>{labels[4]}</h3>{items(before)}</article><article><h3>{labels[5]}</h3>{items(after)}</article></div>',
        f'<h2>{labels[2]}</h2><ol class="example">'+"".join(f"<li>{x}</li>" for x in example)+"</ol>",
        f'<h2>{labels[3]}</h2>{items(verification)}'+(f'<h3>{labels[6]}</h3>{items(uncertainties)}' if uncertainties else "")+'<ul class="sources">'+"".join(source_html)+"</ul>",
    ]
    body = "\n".join(f'<section class="slide" id="slide-{i+1}" aria-label="{i+1} / 5">{section}</section>' for i, section in enumerate(sections))
    css = """
*{box-sizing:border-box}body{margin:0;background:#f6f4ef;color:#162e35;font:clamp(20px,2.2vw,30px)/1.55 system-ui,sans-serif}
main{max-width:1200px;margin:auto;padding:40px 32px 110px}.slide{padding:34px 0;min-height:65vh;overflow-wrap:anywhere}
h1{font-size:clamp(40px,6vw,72px);line-height:1.12;max-width:18ch;margin:25px 0}h2{font-size:clamp(32px,4vw,50px);line-height:1.2}
h3{font-size:1em;color:#1c605f}.summary{font-size:1.25em;max-width:40ch}p,li{max-width:66ch}li{margin:.55em 0}
.comparison{display:grid;grid-template-columns:1fr 1fr;gap:24px}article{background:white;border:1px solid #c7d3d0;border-radius:20px;padding:20px 28px}
.sources{font-size:18px;border-top:1px solid #bdc9c6;padding-top:20px}code{display:block;font:16px/1.5 ui-monospace,monospace;white-space:pre-wrap;color:#374d53}
a{color:#125f71}nav{position:fixed;bottom:0;width:100%;background:#f6f4efed;border-top:1px solid #bdc9c6;padding:14px;display:none;justify-content:center;gap:12px;align-items:center}
button{font:16px system-ui;padding:10px 16px;border:1px solid #607d7b;border-radius:8px;background:white;color:#162e35;cursor:pointer}button:disabled{opacity:.45}
.js nav{display:flex}.js:not(.show-all) .slide:not(.active){display:none}
@media(max-width:700px){.comparison{grid-template-columns:1fr}main{padding:16px 20px 110px}nav{gap:6px}button{padding:10px}}
@media print{nav{display:none!important}.slide{display:block!important;break-before:page;min-height:0}main{padding:0}.sources{font-size:14px}}
"""
    js = """
const slides=[...document.querySelectorAll('.slide')];let index=0;
const previous=document.getElementById('previous'),next=document.getElementById('next'),counter=document.getElementById('counter'),all=document.getElementById('all');
function show(n){index=Math.max(0,Math.min(slides.length-1,n));slides.forEach((s,i)=>s.classList.toggle('active',i===index));previous.disabled=index===0;next.disabled=index===slides.length-1;counter.textContent=(index+1)+' / '+slides.length;window.scrollTo(0,0)}
previous.addEventListener('click',()=>show(index-1));next.addEventListener('click',()=>show(index+1));
all.addEventListener('click',()=>{const on=document.documentElement.classList.toggle('show-all');all.setAttribute('aria-pressed',String(on))});
document.addEventListener('keydown',e=>{if(e.target.closest('button,a,input,textarea,select')||e.altKey||e.ctrlKey||e.metaKey)return;if(e.key==='ArrowRight'){e.preventDefault();show(index+1)}if(e.key==='ArrowLeft'){e.preventDefault();show(index-1)}});
show(0);document.documentElement.classList.add('js');
"""
    return f'<!doctype html><html lang="{language}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>{css}</style></head><body><main>{body}</main><nav aria-label="Slides"><button id="previous">{labels[7]}</button><span id="counter" aria-live="polite">1 / 5</span><button id="next">{labels[8]}</button><button id="all" aria-pressed="false">{labels[9]}</button></nav><script>{js}</script></body></html>'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    result = render(json.loads(args.input.read_text()))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(result)
    print(args.output.resolve())


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError) as exc:
        raise SystemExit(str(exc))
