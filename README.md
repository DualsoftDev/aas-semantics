# DualSoft AAS Semantics

DualSoft ds2 / Sequence Model 가 발급하는 AAS (Asset Administration Shell) **ConceptDescription (CD)** 카탈로그.

전체 29개 CD — Entities (11) · Submodels (9) · Simulation (9).

## URL 규칙

각 CD 는 **자기 폴더** 안에 `cd.json` (AAS) + `index.html` (사람용 viewer) 로 호스팅됩니다.

| 용도 | URL 예시 (`entity/ApiCall/1/0` 기준) |
|---|---|
| **IRI / semanticId** (식별자, AAS 안에서 참조) | https://dualsoftdev.github.io/aas-semantics/entity/ApiCall/1/0 |
| **브라우저 viewer** (사람이 클릭) | 같은 URL — 자동으로 `index.html` 서빙 (다이어그램 + 다국어 정의) |
| **JSON fetch** (도구) | https://dualsoftdev.github.io/aas-semantics/entity/ApiCall/1/0/cd.json |
| **Raw fetch** (도구, 다른 경로) | https://raw.githubusercontent.com/DualsoftDev/aas-semantics/main/entity/ApiCall/1/0/cd.json |
| **GitHub UI 소스 보기** | https://github.com/DualsoftDev/aas-semantics/tree/main/entity/ApiCall/1/0 |

→ **IRI 자체가 클릭 가능한 사람용 viewer 페이지**. AAS Package Explorer 등 도구에서 semanticId 클릭 시 브라우저로 viewer 가 떠서 즉시 이해 가능 (self-describing).

전체 카탈로그: [index.html](https://dualsoftdev.github.io/aas-semantics/) (사람용) · [`index.json`](index.json) (도구용).

## 카탈로그 구조

| 그룹 | 경로 | 개수 | 용도 |
|---|---|---|---|
| **Entities** | [`entity/`](entity/) | 11 | ds2 핵심 엔티티 (Project · System · Device · Flow · Work · Call · ApiDef · ApiCall · TokenSpec · ArrowWork · ArrowCall) |
| **Submodels** | [`sm/`](sm/) | 9 | 서브모델 자체 (SequenceModel + 8개 도메인: Simulation · Control · Monitoring · Logging · Maintenance · Hmi · Quality · CostAnalysis) |
| **Simulation** | [`sim/`](sim/) | 9 | 시뮬레이션 결과 박제 (Result · Meta + 7 KPI: CycleTime · Throughput · Capacity · Constraints · ResourceUtilization · OEE · PerToken) |

## CD 형식

각 `cd.json` 은 AAS V3 ConceptDescription + IEC 61360 EmbeddedDataSpecification 을 따릅니다:

```json
{
  "modelType": "ConceptDescription",
  "id": "https://dualsoftdev.github.io/aas-semantics/sim/Kpi/OEE/1/0",
  "idShort": "OEEkpi",
  "displayName": [
    { "language": "en", "text": "OEE KPI" },
    { "language": "de", "text": "OEE-KPI" },
    { "language": "ko", "text": "OEE 지표" }
  ],
  "description": [
    { "language": "en", "text": "Overall Equipment Effectiveness = Availability × Performance × Quality." },
    { "language": "de", "text": "..." },
    { "language": "ko", "text": "종합설비효율 = 가동률 × 성능률 × 양품률." }
  ],
  "embeddedDataSpecifications": [{
    "dataSpecification": {
      "type": "ExternalReference",
      "keys": [{
        "type": "GlobalReference",
        "value": "https://admin-shell.io/aas/3/0/DataSpecificationIec61360"
      }]
    },
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

## Entity Viewer 다이어그램

엔티티별 viewer (`index.html`) 에 SVG 다이어그램 + 다국어 정의 (한/영/독) 포함:

| Entity | 다이어그램 |
|---|---|
| [Project](https://dualsoftdev.github.io/aas-semantics/entity/Project/1/0) | Project → ActiveSystems + Devices 트리 |
| [System](https://dualsoftdev.github.io/aas-semantics/entity/System/1/0) | 활성 System = Flow + Devices |
| [Device](https://dualsoftdev.github.io/aas-semantics/entity/Device/1/0) | 패시브 Device = APIs 노출 |
| [Flow](https://dualsoftdev.github.io/aas-semantics/entity/Flow/1/0) | W1 → W2 → W3 시퀀스 |
| [Work](https://dualsoftdev.github.io/aas-semantics/entity/Work/1/0) | R/G/F/H 상태머신 |
| [Call](https://dualsoftdev.github.io/aas-semantics/entity/Call/1/0) | Work 내 Call 들 + 디바이스 API 참조 |
| [ApiDef](https://dualsoftdev.github.io/aas-semantics/entity/ApiDef/1/0) | Input → Output 시그니처 |
| [ApiCall](https://dualsoftdev.github.io/aas-semantics/entity/ApiCall/1/0) | Caller(Call) ↔ Callee(ApiDef) 바인딩 |
| [TokenSpec](https://dualsoftdev.github.io/aas-semantics/entity/TokenSpec/1/0) | 토큰이 Work 들을 흐르는 모습 |
| [ArrowWork](https://dualsoftdev.github.io/aas-semantics/entity/ArrowWork/1/0) | W1 ━[Reset]━→ W2 |
| [ArrowCall](https://dualsoftdev.github.io/aas-semantics/entity/ArrowCall/1/0) | Work 내 Call 간 순서 |

## 재생성 / 유지보수

CD 메타데이터는 [`cds.yaml`](cds.yaml) 에 단일 진실 원천. 모든 JSON / HTML 파일은 다음으로 일괄 재생성:

```sh
python3 generate.py
```

호스팅 위치를 바꾸고 싶으면 `--base-url` 옵션 (또는 `cds.yaml` 의 `baseUrl` 한 줄 수정):

```sh
python3 generate.py --base-url https://semantics.dualsoft.com
```

엔티티 다이어그램은 [`diagrams.py`](diagrams.py) 의 `DIAGRAMS` dict 에서 SVG 로 정의됩니다.

### ds2 코드와의 동기화

CD IRI 베이스는 ds2 측 `AasxSemantics.fs` 의 `CdBaseUrl` 와 일치해야 합니다.

```fsharp
// ds2/Solutions/Convert/Ds2.Aasx/AasxSemantics.fs
let [<Literal>] CdBaseUrl = "https://dualsoftdev.github.io/aas-semantics"
```

CD 항목 추가 시:
1. `cds.yaml` 에 새 entry 추가
2. (옵션) `diagrams.py` 에 SVG 추가
3. `python3 generate.py` 실행
4. ds2 측 [`AasxSemantics.fs`](https://github.com/DualsoftDev/ds2/blob/master/Solutions/Convert/Ds2.Aasx/AasxSemantics.fs) 와 [`Concepts/Catalog.fs`](https://github.com/DualsoftDev/ds2/blob/master/Solutions/Convert/Ds2.Aasx/Concepts/Catalog.fs) 에도 동일하게 추가

## License

Public domain — 산업 표준화 목적의 공개 사양.
