#!/usr/bin/env python3
"""
generate.py — cds.yaml 의 매니페스트로부터 AAS V3 ConceptDescription JSON 파일 + index.json 생성.

사용법:
    python3 generate.py
    python3 generate.py --base-url https://dualsoftdev.github.io/aas-semantics

GitHub Pages 활성화 후 dereferenceable 한 URL 로 옮길 때 --base-url 옵션으로 일괄 재생성.
"""
import argparse
import json
import os
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML 필요: pip install pyyaml")


IEC61360_DATA_SPEC_REF = "https://admin-shell.io/aas/3/0/DataSpecificationIec61360"


def lang_strings(items):
    """[(lang, text), ...] → AAS LangString list"""
    return [{"language": lang, "text": text} for lang, text in items if text]


def build_cd(cd: dict, base_url: str) -> dict:
    full_id = base_url.rstrip("/") + "/" + cd["path"]

    display = lang_strings([
        ("en", cd.get("en")),
        ("de", cd.get("de")),
        ("ko", cd.get("ko")),
    ])
    description = lang_strings([
        ("en", cd.get("defEn")),
        ("de", cd.get("defDe")),
        ("ko", cd.get("defKo")),
    ])

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
                "keys": [{
                    "type": "GlobalReference",
                    "value": IEC61360_DATA_SPEC_REF,
                }],
            },
            "dataSpecificationContent": spec_content,
        }],
    }


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate AAS CD JSON files from cds.yaml")
    parser.add_argument("--manifest", default="cds.yaml", help="path to cds.yaml")
    parser.add_argument("--out", default=".", help="output root directory")
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

    index = {
        "baseUrl": base_url,
        "count": len(cds),
        "items": [],
    }

    for cd in cds:
        full_id = base_url.rstrip("/") + "/" + cd["path"]
        cd_obj = build_cd(cd, base_url)
        out_path = out_root / (cd["path"] + ".json")
        write_json(out_path, cd_obj)
        index["items"].append({
            "id": full_id,
            "idShort": cd["idShort"],
            "path": cd["path"] + ".json",
            "displayName": {
                "en": cd.get("en"),
                "de": cd.get("de"),
                "ko": cd.get("ko"),
            },
        })
        print(f"  ✓ {cd['path']}.json")

    write_json(out_root / "index.json", index)
    print(f"\n총 {len(cds)}개 CD + index.json 생성 완료 → {out_root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
