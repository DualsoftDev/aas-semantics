# DualSoft AAS Semantics

DualSoft ds2 / Sequence Model 가 발급하는 AAS (Asset Administration Shell) **ConceptDescription (CD)** 카탈로그.

전체 29개 CD — Entities (11) · Submodels (9) · Simulation (9).

## 🎯 카탈로그 범위 — ds2 자체 CD 만

본 리포는 **ds2 가 자체 발급하는 CD** 만 호스팅합니다. AAS 표준 SM (Nameplate / HandoverDocumentation / TechnicalData 등) 의 CD 는 **IDTA 가 published `.aasx` 템플릿** 으로 직접 제공하므로 이 리포에 없습니다.

| 카테고리 | 출처 | 위치 |
|---|---|---|
| **ds2 도메인 CD** (entity / sm / sim 29개) | ✅ 본 리포 | `entity/`, `sm/`, `sim/` |
| **IDTA 표준 SM CD** (Nameplate v3.0.1, HD v2.0, TD v2.0 등) | ❌ 본 리포에 없음 | [admin-shell-io/submodel-templates](https://github.com/admin-shell-io/submodel-templates) |

ds2 v2026 이후 export 흐름:
```
ds2 사용자 데이터 ──┐
                   ├─→ AAS Submodel emit
IDTA 표준 .aasx ───┘    (템플릿이 구조/CD/언어슬롯 정의, ds2 가 값 주입)
```
- ds2 의 **자체** SM (`SequenceModel`, `SequenceSimulation` 등 9 종) → **본 리포의 sm/* CD** 사용
- ds2 가 emit 하는 **IDTA 표준 SM** (`Nameplate`, `HandoverDocumentation`, `TechnicalData`) → **IDTA 의 published 템플릿** 사용 (본 리포 비관여)

따라서 **IDTA 가 v3.0.2 등 새 버전 publish → ds2 의 임베디드 .aasx 만 교체** (본 리포 갱신 불필요).
**ds2 의 자체 도메인 CD 변경 → 본 리포 + ds2 `Catalog.fs` 양쪽 동기화 필요**.

---

## 🤖 AI 가 AAS 모델을 만들 때 (필독)

> **AI 는 절대 `.aasx` 를 직접 생성하지 말 것.** 산출물은 항상 **`*.ds2.json` 한 파일**.
>
> 사용자가 그 ds2.json 을 **Promaker** 로 열어서(`File → Open`) 검토 후 **`Save As → AASX`** 로 패키징한다.
>
> 자세한 스키마·예시·검증 체크리스트:
> - 📘 [`AI_GUIDE_DS2_JSON.md`](AI_GUIDE_DS2_JSON.md) — 가이드 (반드시 먼저 읽을 것)
> - 📄 [`SAMPLE.ds2.json`](SAMPLE.ds2.json) — 최소 동작 샘플 (1 Active System × 1 Flow × 2 Work × 1 Arrow + 1 Passive Device)

---

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
| **Submodels** | [`sm/`](sm/) | 9 | ds2 자체 서브모델 (SequenceModel + 8 도메인). IDTA 표준 SM 은 본 리포 비관여 |
| **Simulation** | [`sim/`](sim/) | 9 | 시뮬결과 박제 (Result · Meta + 7 KPI). **SequenceSimulation/SystemProperties/SimulationResult SMC 하위에서 참조됨** |

> **참고**: `SimulationResult` 박제는 ds2 v2026 이전에 TechnicalData (IDTA 02003) 안에 있었으나,
> AAS 표준 SM 분리 정책에 따라 **SequenceSimulation 서브모델의 `SystemProperties/SimulationResult`** 로 이동했습니다.

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

ds2 의 AASX export 인프라 (v2026):
| 파일 | 역할 |
|---|---|
| `AasxSemantics.fs` | `CdBaseUrl` + 모든 ds2 자체 SemanticId 상수 |
| `Concepts/Catalog.fs` | ds2 자체 발급 CD 의 `ConceptDescriptionInfo` (entity 11 + sm 9 + sim 9) — 본 리포 `cds.yaml` 의 진실 원천 미러 |
| `Concepts/Builder.fs` | 임베디드 SequenceModel.aasx 로드 + 본 리포 CD 와 통합 |
| `Concepts/TemplateLoader.fs` | IDTA 표준 .aasx 템플릿 (Nameplate/HD/TD) 임베디드 로드 + 사용자 폴더 .aasx 스캔 |
| `Concepts/TemplateScaffold.fs` | 템플릿 SM 의 path 기반 값 주입 (사용자 데이터만, 구조는 무수정) |
| `Concepts/Templates/*.aasx` | IDTA published 템플릿 (Nameplate v3.0.1 / HD v2.0 / TD v2.0) — 새 버전 publish 시 파일만 교체 |

**ds2 자체 도메인 CD 항목 추가 시** (본 리포 관할):
1. `cds.yaml` 에 새 entry 추가
2. (옵션) `diagrams.py` 에 SVG 추가
3. `python3 generate.py` 실행
4. ds2 측 [`AasxSemantics.fs`](https://github.com/DualsoftDev/ds2/blob/master/Solutions/Convert/Ds2.Aasx/AasxSemantics.fs) 와 [`Concepts/Catalog.fs`](https://github.com/DualsoftDev/ds2/blob/master/Solutions/Convert/Ds2.Aasx/Concepts/Catalog.fs) 에도 동일하게 추가

**IDTA 표준 SM 새 버전 publish 시** (본 리포 비관여):
- ds2 측 `Concepts/Templates/*.aasx` 만 [admin-shell-io/submodel-templates](https://github.com/admin-shell-io/submodel-templates) 에서 다운로드 받아 교체
- 본 리포는 변경 없음

**사용자 정의 SM 첨부** (Promaker 사용자 워크플로우):
- 사용자가 임의 .aasx 를 `%APPDATA%\Dualsoft\Promaker\AasxUserTemplates\` 에 떨궈두면 export 시 자동 첨부
- ds2 자체 표준 SM 과 idShort 충돌 시 사용자 SM 이 override (Promaker UI 가 안내)

## License

Public domain — 산업 표준화 목적의 공개 사양.
