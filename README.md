# DualSoft AAS Semantics

DualSoft ds2 / Sequence Model 가 발급하는 AAS (Asset Administration Shell) **ConceptDescription (CD)** 카탈로그.

## URL 규칙

각 CD 는 **자기 폴더 안 `cd.json`** 으로 호스팅됩니다 — 향후 examples / viewer 등 같은 폴더에 확장 가능.

| 용도 | URL |
|---|---|
| **IRI / semanticId** (식별자) | `https://github.com/DualsoftDev/aas-semantics/blob/main/entity/ApiCall/1/0` |
| **GitHub UI 폴더 보기** | https://github.com/DualsoftDev/aas-semantics/tree/main/entity/ApiCall/1/0 |
| **Fetch URL** (도구가 JSON 가져올 때) | `https://dualsoftdev.github.io/aas-semantics/entity/ApiCall/1/0/cd.json` |
| **Raw fetch** | `https://raw.githubusercontent.com/DualsoftDev/aas-semantics/main/entity/ApiCall/1/0/cd.json` |

전체 카탈로그는 [`index.json`](index.json) 의 `items[].id` (IRI) + `path` (`<base>/cd.json`) 참조.

## 카탈로그 구조

| 그룹 | 경로 | 개수 | 용도 |
|---|---|---|---|
| **Entities** | [`entity/`](entity/) | 11 | ds2 핵심 엔티티 (Project / System / Flow / Work / Call / ApiDef / ApiCall / TokenSpec / Arrow) |
| **Submodels** | [`sm/`](sm/) | 9 | 서브모델 자체 (SequenceModel + 8개 도메인) |
| **Simulation** | [`sim/`](sim/) | 9 | 시뮬레이션 결과 (Meta + Result + 7 KPI) |

전체 목록은 [`index.json`](index.json) 참조.

## CD 형식

각 JSON 파일은 AAS V3 ConceptDescription + IEC 61360 EmbeddedDataSpecification 을 따릅니다:

```json
{
  "modelType": "ConceptDescription",
  "id": "https://github.com/DualsoftDev/aas-semantics/blob/main/sim/Kpi/OEE/1/0",
  "idShort": "OEEkpi",
  "displayName": [
    { "language": "en", "text": "OEE KPI" },
    { "language": "de", "text": "OEE-KPI" },
    { "language": "ko", "text": "OEE 지표" }
  ],
  "description": [
    { "language": "en", "text": "..." },
    { "language": "de", "text": "..." },
    { "language": "ko", "text": "..." }
  ],
  "embeddedDataSpecifications": [{
    "dataSpecification": { "type": "ExternalReference",
      "keys": [{ "type": "GlobalReference",
                 "value": "https://admin-shell.io/aas/3/0/DataSpecificationIec61360" }] },
    "dataSpecificationContent": {
      "modelType": "DataSpecificationIec61360",
      "preferredName": [...],
      "shortName":     [...],
      "definition":    [...],
      "unit":          "ratio (0..1)",
      "dataType":      "REAL_MEASURE",
      "sourceOfDefinition": "ISO 22400-2:2014"
    }
  }]
}
```

## 재생성

CD 메타데이터는 [`cds.yaml`](cds.yaml) 에 단일 진실 원천으로 보관됩니다. 모든 JSON 파일은 `python generate.py` 로 일괄 재생성 가능:

```sh
python3 generate.py
```

ds2 코드의 [`AasxSemantics.fs`](https://github.com/DualsoftDev/ds2/blob/master/Solutions/Convert/Ds2.Aasx/AasxSemantics.fs) 의 `CdBaseUrl` 과 [`Concepts/Catalog.fs`](https://github.com/DualsoftDev/ds2/blob/master/Solutions/Convert/Ds2.Aasx/Concepts/Catalog.fs) 의 항목들과 일치하게 유지하세요.

## License

Public domain — 산업 표준화 목적의 공개 사양.
