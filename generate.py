#!/usr/bin/env python3
"""
generate.py — cds.yaml 에서 AAS V3 ConceptDescription JSON + viewer index.html 일괄 생성.

사용법:
    python3 generate.py
    python3 generate.py --base-url https://dualsoftdev.github.io/aas-semantics

각 CD 는 자기 폴더 안에 다음을 가진다:
    <path>/cd.json       ← AAS ConceptDescription
    <path>/index.html    ← 사람용 viewer (다이어그램 + 다국어 정의)
"""
import argparse
import html
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML 필요: pip install pyyaml")

import diagrams as _diagrams
import entity_details as _details
try:
    import detail_diagrams as _detail_diagrams
except ImportError:
    _detail_diagrams = None
try:
    import appendices as _appendices
except ImportError:
    _appendices = None


IEC61360_DATA_SPEC_REF = "https://admin-shell.io/aas/3/0/DataSpecificationIec61360"


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>{title} — AAS ConceptDescription</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
           max-width: 1080px; margin: 2rem auto; padding: 0 1rem; color: #1f2328; line-height: 1.55; }}
    h1 {{ color: #0969da; margin: 0 0 4px 0; font-size: 1.7rem; }}
    h2 {{ color: #1f2328; font-size: 1.15rem; margin-top: 2.2rem; border-bottom: 1px solid #d0d7de; padding-bottom: 4px; }}
    .subtitle {{ color: #656d76; font-size: 0.95rem; margin-bottom: 1.5rem; }}
    .card {{ background: #f6f8fa; border: 1px solid #d0d7de; border-radius: 8px; padding: 12px 16px; margin: 12px 0; }}
    .iri {{ font-family: ui-monospace, "SF Mono", Consolas, monospace; word-break: break-all;
           background: #fff; padding: 6px 10px; border-radius: 4px; border: 1px solid #d0d7de;
           font-size: 0.85rem; display: inline-block; margin-top: 4px; }}
    .lang-block {{ margin: 8px 0; padding: 8px 12px; border-left: 3px solid #0969da; background: #fff; }}
    .lang-block .label {{ font-weight: 600; color: #0969da; font-size: 0.78rem; margin-bottom: 4px; letter-spacing: 0.5px; }}
    .diagram {{ background: #fff; border: 1px solid #d0d7de; border-radius: 8px; padding: 1rem; text-align: center; margin: 1rem 0; }}
    .diagram svg {{ max-width: 100%; height: auto; }}
    .links a {{ color: #0969da; text-decoration: none; margin-right: 1rem; font-size: 0.9rem; }}
    .links a:hover {{ text-decoration: underline; }}
    .footer {{ margin-top: 3rem; padding-top: 1rem; border-top: 1px solid #d0d7de; color: #656d76; font-size: 0.85rem; }}
    code {{ background: #eef1f4; padding: 2px 6px; border-radius: 3px; font-size: 0.88em; font-family: ui-monospace, "SF Mono", Consolas, monospace; }}
    pre {{ background: #0d1117; color: #e6edf3; padding: 14px 16px; border-radius: 8px; overflow-x: auto;
          font-family: ui-monospace, "SF Mono", Consolas, monospace; font-size: 0.85rem; line-height: 1.5;
          border: 1px solid #30363d; }}
    pre code {{ background: transparent; color: inherit; padding: 0; }}
    table.fields {{ width: 100%; border-collapse: collapse; margin: 8px 0; font-size: 0.88rem; }}
    table.fields th, table.fields td {{ text-align: left; padding: 6px 10px; border-bottom: 1px solid #d0d7de; vertical-align: top; }}
    table.fields th {{ background: #f6f8fa; color: #656d76; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600; }}
    table.fields td.fname {{ font-family: ui-monospace, "SF Mono", Consolas, monospace; font-weight: 600; color: #0550ae; white-space: nowrap; }}
    table.fields td.ftype {{ font-family: ui-monospace, "SF Mono", Consolas, monospace; color: #0a3069; font-size: 0.82rem; }}
    table.fields td.fdef {{ font-family: ui-monospace, "SF Mono", Consolas, monospace; color: #6f42c1; font-size: 0.82rem; }}
    .relations li {{ margin: 6px 0; }}
    .pill {{ display: inline-block; padding: 1px 8px; border-radius: 12px; font-size: 0.72rem; font-weight: 600;
            background: #ddf4ff; color: #0969da; margin-left: 6px; vertical-align: middle; }}
    .pill-state {{ background: #fff8c5; color: #9a6700; }}
    /* === Phase 0 enrichment: scenarios / vendors / IDTA / events / KPI / standards / related / appendix === */
    .scenario-card {{ background: #fff; border: 1px solid #d0d7de; border-radius: 8px; padding: 14px 16px; margin: 12px 0; }}
    .scenario-header {{ display: flex; flex-wrap: wrap; align-items: center; gap: 10px; margin-bottom: 8px; }}
    .scenario-domain {{ display: inline-block; padding: 2px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 600; background: #ddf4ff; color: #0969da; }}
    .scenario-system {{ font-weight: 600; color: #1f2328; }}
    .scenario-meta {{ color: #656d76; font-size: 0.85rem; }}
    .scenario-body {{ font-size: 0.9rem; color: #1f2328; line-height: 1.55; }}
    .call-strip {{ display: flex; gap: 6px; margin-top: 8px; flex-wrap: wrap; }}
    .call-chip {{ background: #f6f8fa; border: 1px solid #d0d7de; border-radius: 6px; padding: 4px 10px; font-size: 0.8rem; }}
    .call-chip .call-dur {{ color: #656d76; font-size: 0.75rem; margin-left: 6px; }}
    .vendor-list {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 10px; }}
    .vendor-card {{ background: #fff; border: 1px solid #d0d7de; border-radius: 6px; padding: 10px 12px; }}
    .vendor-card .v-name {{ font-weight: 600; color: #0550ae; font-size: 0.85rem; margin-bottom: 6px; }}
    .vendor-card code {{ display: block; margin: 2px 0; font-size: 0.78rem; background: #eef1f4; padding: 2px 6px; border-radius: 3px; }}
    .iota-table {{ width: 100%; border-collapse: collapse; font-size: 0.82rem; margin: 8px 0; }}
    .iota-table th, .iota-table td {{ padding: 6px 8px; border: 1px solid #d0d7de; text-align: left; vertical-align: top; }}
    .iota-table th {{ background: #f6f8fa; color: #656d76; font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.4px; }}
    .iota-table td.idShort {{ font-family: ui-monospace, Consolas, monospace; color: #0550ae; font-weight: 600; white-space: nowrap; }}
    .iota-table td.semId {{ font-family: ui-monospace, Consolas, monospace; color: #6f42c1; font-size: 0.7rem; word-break: break-all; }}
    .iota-table td.vt {{ font-family: ui-monospace, Consolas, monospace; color: #0a3069; font-size: 0.78rem; }}
    .iota-table td.mult {{ text-align: center; font-family: ui-monospace, Consolas, monospace; color: #1a7f37; font-size: 0.78rem; }}
    .event-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 10px; margin: 10px 0; }}
    .event-card {{ background: #f6f8fa; border-left: 3px solid #0969da; border-radius: 4px; padding: 10px 12px; }}
    .event-card .ev-name {{ font-weight: 600; color: #0550ae; font-size: 0.85rem; }}
    .event-card .ev-params {{ color: #656d76; font-size: 0.78rem; margin-top: 4px; font-family: ui-monospace, Consolas, monospace; }}
    .event-card .ev-use {{ color: #1f2328; font-size: 0.8rem; margin-top: 6px; }}
    .kpi-formula {{ background: #fff; border: 2px solid #0969da; border-radius: 8px; padding: 14px 18px; margin: 10px 0; text-align: center; }}
    .kpi-formula .expr {{ font-family: 'Cambria Math', Georgia, serif; font-size: 1.15rem; color: #0550ae; font-weight: 600; }}
    .kpi-formula .source {{ color: #656d76; font-size: 0.78rem; margin-top: 6px; }}
    .kpi-components {{ margin-top: 12px; display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 8px; text-align: left; }}
    .kpi-comp-card {{ background: #f6f8fa; border-radius: 6px; padding: 8px 10px; font-size: 0.82rem; }}
    .kpi-comp-card .sym {{ font-weight: 600; color: #0550ae; }}
    .kpi-comp-card .formula {{ font-family: ui-monospace, Consolas, monospace; color: #6f42c1; font-size: 0.78rem; margin-top: 2px; }}
    .kpi-example {{ background: #dafbe1; border-left: 4px solid #1a7f37; border-radius: 4px; padding: 10px 14px; margin-top: 10px; font-size: 0.88rem; }}
    .kpi-example .calc {{ font-family: 'Cambria Math', Georgia, serif; font-size: 1rem; color: #1f2328; margin: 6px 0; }}
    .kpi-example .result {{ font-weight: 700; color: #1a7f37; font-size: 1.1rem; }}
    .standards-row {{ display: flex; flex-wrap: wrap; gap: 6px; margin: 8px 0; }}
    .std-badge {{ background: #fff8c5; color: #9a6700; border: 1px solid #d4a72c; padding: 3px 10px; border-radius: 12px; font-size: 0.78rem; font-weight: 600; }}
    .std-badge a {{ color: inherit; text-decoration: none; }}
    .std-badge .scope {{ font-weight: 400; color: #6e5500; }}
    .related-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 8px; margin: 8px 0; }}
    .related-card {{ background: #fff; border: 1px solid #d0d7de; border-radius: 6px; padding: 8px 12px; transition: border-color 0.15s; }}
    .related-card:hover {{ border-color: #0969da; }}
    .related-card a {{ display: block; text-decoration: none; }}
    .related-card .r-name {{ font-weight: 600; color: #0550ae; font-size: 0.88rem; }}
    .related-card .r-desc {{ color: #656d76; font-size: 0.78rem; margin-top: 3px; }}
    .appendix-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 10px; }}
    .appendix-card {{ background: linear-gradient(135deg, #ddf4ff, #fff); border: 1px solid #0969da; border-radius: 8px; padding: 10px 14px; }}
    .appendix-card a {{ text-decoration: none; color: #0550ae; font-weight: 600; }}
    .appendix-card .a-desc {{ color: #1f2328; font-size: 0.82rem; margin-top: 4px; font-weight: 400; }}
    .timing-strip {{ background: #fff; border: 1px solid #d0d7de; border-radius: 6px; padding: 10px; margin: 10px 0; overflow-x: auto; }}
    .timing-strip table {{ border-collapse: collapse; font-size: 0.78rem; }}
    .timing-strip td {{ padding: 4px 10px; text-align: center; border: 1px solid #d0d7de; min-width: 36px; font-family: ui-monospace, Consolas, monospace; }}
    .timing-strip th {{ padding: 4px 10px; background: #f6f8fa; text-align: center; font-weight: 600; font-size: 0.72rem; color: #656d76; text-transform: uppercase; }}
    .timing-strip td.r {{ background: #dafbe1; color: #1a7f37; font-weight: 600; }}
    .timing-strip td.g {{ background: #ffd8b5; color: #bc4c00; font-weight: 600; }}
    .timing-strip td.f {{ background: #ddf4ff; color: #0969da; font-weight: 600; }}
    .timing-strip td.h {{ background: #eaeef2; color: #656d76; font-weight: 600; }}
    .timing-strip td.sig1 {{ background: #ffeaea; color: #cf222e; font-weight: 700; }}
    .timing-strip td.row-label {{ background: #f6f8fa; font-weight: 600; color: #1f2328; text-align: left; padding-left: 12px; padding-right: 14px; }}
    .section-sub {{ color: #656d76; font-size: 0.95rem; margin: 14px 0 6px 0; font-weight: 600; }}
  </style>
</head>
<body>
  <div class="links" style="margin-bottom: 1rem;">
    <a href="{root_rel}">← Catalog</a>
  </div>

  <h1>{idShort} <span class="pill">{group}</span></h1>
  <div class="subtitle"><strong>{nameEn}</strong> · {nameKo} · {nameDe}</div>

  <div class="card">
    <div><strong>IRI (semanticId)</strong></div>
    <div class="iri">{iri}</div>
    <div class="links" style="margin-top: 10px;">
      <a href="cd.json">📄 cd.json (raw)</a>
      <a href="https://github.com/DualsoftDev/aas-semantics/tree/main/{path}" target="_blank">📂 GitHub source</a>
    </div>
  </div>

  <h2>설명 / Description / Beschreibung</h2>
  <div class="card">
    <div class="lang-block">
      <div class="label">한국어</div>
      <div>{defKo}</div>
    </div>
    <div class="lang-block">
      <div class="label">English</div>
      <div>{defEn}</div>
    </div>
    <div class="lang-block">
      <div class="label">Deutsch</div>
      <div>{defDe}</div>
    </div>
  </div>

  {diagram_section}

  {detail_sections}

  <h2>AAS ConceptDescription 메타</h2>
  <div class="card">
    <div>idShort: <code>{idShort}</code></div>
    {dataType_line}
    {unit_line}
    {source_line}
  </div>

  <div class="footer">
    Part of <a href="{root_rel}">DualSoft AAS Semantics catalog</a> ·
    <a href="https://github.com/DualsoftDev/aas-semantics" target="_blank">aas-semantics repo</a> ·
    <a href="https://github.com/DualsoftDev/ds2" target="_blank">ds2 repo</a>
  </div>
</body>
</html>
"""


def _esc(s: str) -> str:
    return html.escape(s) if s else ""


def lang_strings(items):
    return [{"language": lang, "text": text} for lang, text in items if text]


def build_cd(cd: dict, base_url: str) -> dict:
    full_id = base_url.rstrip("/") + "/" + cd["path"]
    display = lang_strings([("en", cd.get("en")), ("de", cd.get("de")), ("ko", cd.get("ko"))])
    description = lang_strings([("en", cd.get("defEn")), ("de", cd.get("defDe")), ("ko", cd.get("defKo"))])

    spec_content = {
        "modelType": "DataSpecificationIec61360",
        "preferredName": display,
        "shortName": [{"language": "EN", "text": cd["idShort"]}],
        "definition": description,
    }
    if cd.get("dataType"):
        spec_content["dataType"] = cd["dataType"]
    if cd.get("unit"):
        spec_content["unit"] = cd["unit"]
    if cd.get("sourceOfDefinition"):
        spec_content["sourceOfDefinition"] = cd["sourceOfDefinition"]

    return {
        "modelType": "ConceptDescription",
        "id": full_id,
        "idShort": cd["idShort"],
        "displayName": display,
        "description": description,
        "embeddedDataSpecifications": [{
            "dataSpecification": {
                "type": "ExternalReference",
                "keys": [{"type": "GlobalReference", "value": IEC61360_DATA_SPEC_REF}],
            },
            "dataSpecificationContent": spec_content,
        }],
    }


def _group_for(path: str) -> str:
    if path.startswith("entity/"): return "Entity"
    if path.startswith("sm/"):     return "Submodel"
    if path.startswith("sim/"):    return "Simulation"
    return ""


def _render_inheritance(inherits) -> str:
    if not inherits: return ""
    chain = " ← ".join(f'<a href="{href}" target="_blank">{name}</a>' for name, href in inherits)
    return f'<div class="card"><strong>상속 체인 / Inheritance:</strong> {chain}</div>'


def _render_fields_table(fields) -> str:
    if not fields: return ""
    rows = []
    for name, ftype, fdef, aas, desc in fields:
        rows.append(
            f'<tr><td class="fname">{_esc(name)}</td>'
            f'<td class="ftype">{_esc(ftype)}</td>'
            f'<td class="fdef">{_esc(fdef)}</td>'
            f'<td><code>{_esc(aas)}</code></td>'
            f'<td>{_esc(desc)}</td></tr>'
        )
    return (
        '<table class="fields">'
        '<thead><tr><th>Field</th><th>Type</th><th>Default</th><th>AAS field</th><th>Description</th></tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table>'
    )


def _render_relationships(rels, root_rel: str = "../../../../") -> str:
    if not rels: return ""
    items = "".join(
        f'<li><code>{_esc(label)}</code> {_esc(arrow)} <a href="{root_rel}{target}/">{_esc(target)}</a></li>'
        for label, arrow, target in rels
    )
    return f'<ul class="relations">{items}</ul>'


def _render_state_table(rows) -> str:
    if not rows: return ""
    body = "".join(
        f'<tr><td class="fname"><span class="pill pill-state">{_esc(name)}</span></td><td>{_esc(desc)}</td></tr>'
        for name, desc in rows
    )
    return (
        '<table class="fields">'
        '<thead><tr><th>State / Type</th><th>Meaning</th></tr></thead>'
        f'<tbody>{body}</tbody></table>'
    )


def _render_source_files(srcs) -> str:
    if not srcs: return ""
    items = "".join(
        f'<li><a href="{href}" target="_blank">{_esc(label)}</a></li>'
        for href, label in srcs
    )
    return f'<ul>{items}</ul>'


def _render_scenarios(scenarios) -> str:
    """현실 도메인 시나리오 카드 (자동차/반도체/제철/제약/물류 등)."""
    if not scenarios: return ""
    cards = []
    for sc in scenarios:
        domain = sc.get("domain", "")
        system = sc.get("system", "")
        meta = sc.get("meta", "")
        body = sc.get("body", "")
        calls = sc.get("calls", [])
        timing = sc.get("timing", "")  # raw HTML (e.g., a timing strip)

        call_chips = "".join(
            f'<div class="call-chip">{_esc(c.get("name",""))}'
            + (f'<span class="call-dur">· {_esc(c["duration"])}</span>' if c.get("duration") else "")
            + '</div>'
            for c in calls
        )
        call_section = f'<div class="call-strip">{call_chips}</div>' if call_chips else ""

        cards.append(
            f'<div class="scenario-card">'
            f'<div class="scenario-header">'
            f'<span class="scenario-domain">{_esc(domain)}</span>'
            f'<span class="scenario-system">{_esc(system)}</span>'
            + (f'<span class="scenario-meta">· {_esc(meta)}</span>' if meta else "")
            + '</div>'
            f'<div class="scenario-body">{body}</div>'  # body is allowed to contain inline HTML
            f'{call_section}'
            f'{timing}'
            '</div>'
        )
    return "".join(cards)


def _render_timing_strip(rows, header) -> str:
    """t0..t6 타이밍 표 (Work A/B + Start/Reset 신호)."""
    if not rows: return ""
    head = "<tr><th></th>" + "".join(f"<th>{_esc(h)}</th>" for h in header) + "</tr>"
    body_rows = []
    for label, cells in rows:
        cells_html = "".join(f'<td class="{cls}">{_esc(val)}</td>' for cls, val in cells)
        body_rows.append(f'<tr><td class="row-label">{_esc(label)}</td>{cells_html}</tr>')
    return (
        '<div class="timing-strip"><table>'
        f'<thead>{head}</thead>'
        f'<tbody>{"".join(body_rows)}</tbody>'
        '</table></div>'
    )


def _render_ds2_snippet(snip) -> str:
    if not snip: return ""
    desc = f'<div class="desc">{_esc(snip.get("description",""))}</div>' if snip.get("description") else ""
    title = f'<h3 class="section-sub">{_esc(snip.get("title",""))}</h3>' if snip.get("title") else ""
    json_text = snip.get("json", "")
    return f'<div class="ds2-snippet">{title}{desc}<pre><code>{_esc(json_text)}</code></pre></div>'


def _render_plc_equivalent(plc) -> str:
    """PLC 5종 벤더 동일 동작 표기."""
    if not plc: return ""
    scenario = plc.get("scenario", "")
    behavior = plc.get("behavior", "")
    vendors = plc.get("vendors", [])
    if not vendors: return ""
    cards = []
    for v in vendors:
        lines = [f'<div class="v-name">{_esc(v.get("name",""))}</div>']
        for label in ("input", "output", "code"):
            if v.get(label):
                pretty = {"input": "Input", "output": "Output", "code": "Code"}[label]
                lines.append(f'<code><b>{pretty}:</b> {_esc(v[label])}</code>')
        cards.append(f'<div class="vendor-card">{"".join(lines)}</div>')
    return (
        (f'<div class="scenario-meta">시나리오: <strong>{_esc(scenario)}</strong></div>' if scenario else "")
        + (f'<p>{_esc(behavior)}</p>' if behavior else "")
        + f'<div class="vendor-list">{"".join(cards)}</div>'
    )


def _render_iota_property_table(rows) -> str:
    """IDTA SubmodelElement Property 표."""
    if not rows: return ""
    body = "".join(
        f'<tr>'
        f'<td class="idShort">{_esc(r.get("idShort",""))}</td>'
        f'<td class="semId">{_esc(r.get("semanticId",""))}</td>'
        f'<td class="vt">{_esc(r.get("valueType",""))}</td>'
        f'<td class="mult">{_esc(r.get("multiplicity",""))}</td>'
        f'<td>{_esc(r.get("description",""))}</td>'
        '</tr>'
        for r in rows
    )
    return (
        '<table class="iota-table">'
        '<thead><tr>'
        '<th>idShort</th><th>semanticId</th><th>valueType</th><th>multiplicity</th><th>설명 / description</th>'
        '</tr></thead>'
        f'<tbody>{body}</tbody></table>'
    )


def _render_operational_events(events) -> str:
    """SequenceMonitoring 의 OperationalEvent 카드."""
    if not events: return ""
    cards = "".join(
        f'<div class="event-card">'
        f'<div class="ev-name">{_esc(e.get("name",""))}</div>'
        + (f'<div class="ev-params">{_esc(e["params"])}</div>' if e.get("params") else "")
        + (f'<div class="ev-use">{_esc(e["useCase"])}</div>' if e.get("useCase") else "")
        + '</div>'
        for e in events
    )
    return f'<div class="event-grid">{cards}</div>'


def _render_kpi_formula(kpi) -> str:
    """sim/* KPI 산식 + 컴포넌트 분해 + 계산 예시."""
    if not kpi: return ""
    parts = ['<div class="kpi-formula">']
    if kpi.get("expr"):
        parts.append(f'<div class="expr">{_esc(kpi["expr"])}</div>')
    if kpi.get("source"):
        parts.append(f'<div class="source">출처: {_esc(kpi["source"])}</div>')
    if kpi.get("components"):
        comps = "".join(
            f'<div class="kpi-comp-card">'
            f'<div class="sym">{_esc(c.get("symbol",""))}</div>'
            + (f'<div class="formula">{_esc(c["formula"])}</div>' if c.get("formula") else "")
            + (f'<div>{_esc(c.get("description",""))}</div>' if c.get("description") else "")
            + '</div>'
            for c in kpi["components"]
        )
        parts.append(f'<div class="kpi-components">{comps}</div>')
    parts.append('</div>')
    if kpi.get("example"):
        ex = kpi["example"]
        ex_parts = ['<div class="kpi-example">']
        if ex.get("scenario"):
            ex_parts.append(f'<div><strong>예제:</strong> {_esc(ex["scenario"])}</div>')
        if ex.get("inputs"):
            ips = "; ".join(_esc(i) for i in ex["inputs"])
            ex_parts.append(f'<div>입력: {ips}</div>')
        if ex.get("calc"):
            ex_parts.append(f'<div class="calc">{_esc(ex["calc"])}</div>')
        if ex.get("result"):
            ex_parts.append(f'<div class="result">→ {_esc(ex["result"])}</div>')
        ex_parts.append('</div>')
        parts.append("".join(ex_parts))
    return "".join(parts)


def _render_industry_standards(stds) -> str:
    if not stds: return ""
    badges = []
    for s in stds:
        name = _esc(s.get("name",""))
        scope = s.get("scope","")
        url = s.get("url")
        inner = f'{name}' + (f'<span class="scope"> · {_esc(scope)}</span>' if scope else "")
        if url:
            inner = f'<a href="{_esc(url)}" target="_blank">{inner}</a>'
        badges.append(f'<span class="std-badge">{inner}</span>')
    return f'<div class="standards-row">{"".join(badges)}</div>'


def _render_related_cds(rels, root_rel: str) -> str:
    if not rels: return ""
    cards = "".join(
        f'<div class="related-card"><a href="{root_rel}{_esc(path)}/">'
        f'<div class="r-name">{_esc(name)}</div>'
        f'<div class="r-desc">{_esc(desc)}</div>'
        '</a></div>'
        for path, name, desc in rels
    )
    return f'<div class="related-grid">{cards}</div>'


def _render_appendix_links(links, root_rel: str) -> str:
    if not links: return ""
    cards = "".join(
        f'<div class="appendix-card">'
        f'<a href="{root_rel}docs/{_esc(slug)}/">📚 {_esc(name)}</a>'
        f'<div class="a-desc">{_esc(desc)}</div>'
        '</div>'
        for slug, name, desc in links
    )
    return f'<div class="appendix-grid">{cards}</div>'


def _render_detail_sections(detail, root_rel: str = "../../../../") -> str:
    if not detail: return ""
    parts = []

    if detail.get("inherits"):
        parts.append(_render_inheritance(detail["inherits"]))

    if detail.get("fsharpType"):
        parts.append('<h2>F# 타입 정의 / Type Definition</h2>')
        parts.append(f'<pre><code>{_esc(detail["fsharpType"])}</code></pre>')

    if detail.get("fields"):
        parts.append('<h2>필드 / Fields</h2>')
        parts.append(_render_fields_table(detail["fields"]))

    if detail.get("stateMachine"):
        parts.append('<h2>상태 / 의미 / States &amp; Semantics</h2>')
        parts.append(_render_state_table(detail["stateMachine"]))

    if detail.get("scenarios"):
        parts.append('<h2>현실 시나리오 / Real-world Scenarios</h2>')
        parts.append('<p style="color:#656d76;font-size:0.9rem;margin:6px 0 4px 0;">실제 도메인(자동차·반도체·제철·제약·물류 등)에서 이 CD 가 등장하는 예시.</p>')
        parts.append(_render_scenarios(detail["scenarios"]))

    if detail.get("ds2JsonSnippet"):
        parts.append('<h2>ds2.json 스니펫 / Sample JSON</h2>')
        parts.append(_render_ds2_snippet(detail["ds2JsonSnippet"]))

    if detail.get("plcEquivalent"):
        parts.append('<h2>PLC 동등 표기 / PLC Vendor Equivalents</h2>')
        parts.append(_render_plc_equivalent(detail["plcEquivalent"]))

    if detail.get("smcProperties"):
        parts.append('<h2>IDTA SubmodelElement Property Table</h2>')
        parts.append(_render_iota_property_table(detail["smcProperties"]))

    if detail.get("operationalEvents"):
        parts.append('<h2>운영 이벤트 / Operational Events</h2>')
        parts.append(_render_operational_events(detail["operationalEvents"]))

    if detail.get("submodelExample"):
        parts.append('<h2>Submodel 예제 / Submodel Example (JSON)</h2>')
        parts.append(_render_ds2_snippet(detail["submodelExample"]))

    if detail.get("kpiFormula"):
        parts.append('<h2>KPI 산식 / Formula</h2>')
        parts.append(_render_kpi_formula(detail["kpiFormula"]))

    if detail.get("relationships"):
        parts.append('<h2>관계 / Relationships</h2>')
        parts.append('<div class="card">' + _render_relationships(detail["relationships"], root_rel) + '</div>')

    if detail.get("exampleFsharp"):
        parts.append('<h2>예제 (F#) / Example</h2>')
        parts.append(f'<pre><code>{_esc(detail["exampleFsharp"])}</code></pre>')

    if detail.get("aasMapping"):
        parts.append('<h2>AAS 매핑 / AAS Mapping</h2>')
        parts.append(f'<div class="card">{_esc(detail["aasMapping"])}</div>')

    if detail.get("industryStandards"):
        parts.append('<h2>산업 표준 / Industry Standards</h2>')
        parts.append(_render_industry_standards(detail["industryStandards"]))

    if detail.get("relatedCds"):
        parts.append('<h2>관련 CD / Related ConceptDescriptions</h2>')
        parts.append(_render_related_cds(detail["relatedCds"], root_rel))

    if detail.get("appendixLinks"):
        parts.append('<h2>학습 가이드 / Appendix Pages</h2>')
        parts.append(_render_appendix_links(detail["appendixLinks"], root_rel))

    if detail.get("sourceFiles"):
        parts.append('<h2>원본 코드 / Source files</h2>')
        parts.append('<div class="card">' + _render_source_files(detail["sourceFiles"]) + '</div>')

    return "\n".join(parts)


def build_html(cd: dict, full_id: str) -> str:
    """index.html (사람용 viewer) 생성."""
    svg = _diagrams.get(cd["path"])
    detail_svg = _detail_diagrams.get_detail(cd["path"]) if _detail_diagrams else None

    diagram_parts = []
    if svg:
        # entity/* 는 통합 overview 사용 → "전체 구조" 라벨, 그 외엔 단일 다이어그램
        if cd["path"].startswith("entity/") and detail_svg:
            diagram_parts.append('<h2>다이어그램 / Diagram</h2>')
            diagram_parts.append(
                '<h3 style="margin:12px 0 4px 0; color:#0550ae; font-size:1rem;">'
                '전체 구조 / Overview — 이 엔티티가 DS 안에서 위치</h3>'
            )
            diagram_parts.append(f'<div class="diagram">{svg}</div>')
            diagram_parts.append(
                '<h3 style="margin:18px 0 4px 0; color:#0550ae; font-size:1rem;">'
                '엔티티 상세 / Entity Detail — 내부 구조 · 동작</h3>'
            )
            diagram_parts.append(f'<div class="diagram">{detail_svg}</div>')
        else:
            diagram_parts.append('<h2>다이어그램 / Diagram</h2>')
            diagram_parts.append(f'<div class="diagram">{svg}</div>')
    diagram_section = "\n  ".join(diagram_parts)

    detail = _details.get(cd["path"])
    depth = len(cd["path"].split("/"))
    root_rel = "../" * depth
    detail_sections = _render_detail_sections(detail, root_rel)

    dataType_line = f'<div>dataType: <code>{_esc(cd.get("dataType",""))}</code></div>' if cd.get("dataType") else ""
    unit_line     = f'<div>unit: <code>{_esc(cd.get("unit",""))}</code></div>' if cd.get("unit") else ""
    source_line   = f'<div>source: <code>{_esc(cd.get("sourceOfDefinition",""))}</code></div>' if cd.get("sourceOfDefinition") else ""

    return HTML_TEMPLATE.format(
        title=_esc(cd["idShort"]),
        idShort=_esc(cd["idShort"]),
        group=_group_for(cd["path"]),
        nameEn=_esc(cd.get("en", "")),
        nameDe=_esc(cd.get("de", "")),
        nameKo=_esc(cd.get("ko", "")),
        defEn=_esc(cd.get("defEn", "")),
        defDe=_esc(cd.get("defDe", "")),
        defKo=_esc(cd.get("defKo", "")),
        iri=_esc(full_id),
        path=cd["path"],
        root_rel=root_rel,
        diagram_section=diagram_section,
        detail_sections=detail_sections,
        dataType_line=dataType_line,
        unit_line=unit_line,
        source_line=source_line,
    )


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
        if not content.endswith("\n"):
            f.write("\n")


def write_json(path: Path, data: dict) -> None:
    write_text(path, json.dumps(data, ensure_ascii=False, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate AAS CD JSON + viewer HTML files from cds.yaml")
    parser.add_argument("--manifest", default="cds.yaml")
    parser.add_argument("--out", default=".")
    parser.add_argument("--base-url", default=None,
                        help="override baseUrl in manifest (use Pages URL after enabling)")
    args = parser.parse_args()

    here = Path(__file__).resolve().parent
    manifest_path = here / args.manifest
    out_root = (here / args.out).resolve()

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = yaml.safe_load(f)

    base_url = args.base_url or manifest["baseUrl"]
    cds = manifest.get("cds", [])
    if not cds:
        sys.exit("manifest 의 cds 가 비어있습니다.")

    index = {"baseUrl": base_url, "count": len(cds), "items": []}

    for cd in cds:
        full_id = base_url.rstrip("/") + "/" + cd["path"]
        cd_obj = build_cd(cd, base_url)
        cd_dir = out_root / cd["path"]
        write_json(cd_dir / "cd.json", cd_obj)
        write_text(cd_dir / "index.html", build_html(cd, full_id))

        index["items"].append({
            "id": full_id,
            "idShort": cd["idShort"],
            "path": cd["path"] + "/cd.json",
            "viewer": cd["path"] + "/",
            "displayName": {"en": cd.get("en"), "de": cd.get("de"), "ko": cd.get("ko")},
        })
        print(f"  ✓ {cd['path']}/  (cd.json + index.html)")

    write_json(out_root / "index.json", index)
    print(f"\n총 {len(cds)}개 CD 폴더 + index.json 생성 완료 → {out_root}")

    # ── Appendix pages (학습 가이드: Duality 8 Cases 등) ────────────────────
    if _appendices is not None and hasattr(_appendices, "APPENDICES"):
        for slug, app in _appendices.APPENDICES.items():
            depth = 2  # docs/<slug>/index.html  → root_rel "../../"
            root_rel = "../" * depth
            html_str = _appendices.render_appendix(slug, app, root_rel)
            write_text(out_root / "docs" / slug / "index.html", html_str)
            print(f"  ✓ docs/{slug}/  (appendix)")
        print(f"\n부록 {len(_appendices.APPENDICES)} 개 생성 완료 → {out_root / 'docs'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
