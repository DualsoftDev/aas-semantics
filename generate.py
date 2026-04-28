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


def _render_relationships(rels) -> str:
    if not rels: return ""
    items = "".join(
        f'<li><code>{_esc(label)}</code> {_esc(arrow)} <a href="../../../../{target}/">{_esc(target)}</a></li>'
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


def _render_detail_sections(detail) -> str:
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

    if detail.get("relationships"):
        parts.append('<h2>관계 / Relationships</h2>')
        parts.append('<div class="card">' + _render_relationships(detail["relationships"]) + '</div>')

    if detail.get("exampleFsharp"):
        parts.append('<h2>예제 (F#) / Example</h2>')
        parts.append(f'<pre><code>{_esc(detail["exampleFsharp"])}</code></pre>')

    if detail.get("aasMapping"):
        parts.append('<h2>AAS 매핑 / AAS Mapping</h2>')
        parts.append(f'<div class="card">{_esc(detail["aasMapping"])}</div>')

    if detail.get("sourceFiles"):
        parts.append('<h2>원본 코드 / Source files</h2>')
        parts.append('<div class="card">' + _render_source_files(detail["sourceFiles"]) + '</div>')

    return "\n".join(parts)


def build_html(cd: dict, full_id: str) -> str:
    """index.html (사람용 viewer) 생성."""
    svg = _diagrams.get(cd["path"])
    diagram_section = (
        f'<h2>다이어그램 / Diagram</h2>\n  <div class="diagram">{svg}</div>'
        if svg else ""
    )

    detail = _details.get(cd["path"])
    detail_sections = _render_detail_sections(detail)

    depth = len(cd["path"].split("/"))
    root_rel = "../" * depth

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
    return 0


if __name__ == "__main__":
    sys.exit(main())
