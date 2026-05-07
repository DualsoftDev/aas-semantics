# AI 용 가이드 — `*.ds2.json` 만 생성하라 (AASX 직접 생성 금지)

> ⚠️ **이 문서를 본 AI 가 가장 먼저 지켜야 할 규칙**
>
> 1. **AASX 파일을 직접 만들지 말라.** `.aasx` 는 OPC zip 패키지 (이미지·thumbnail·복수 Submodel·signed metadata) 라서 LLM 이 텍스트로 만들면 깨진다.
> 2. **출력 결과물은 항상 `*.ds2.json` 한 파일.**
> 3. 사용자가 그 파일을 **Promaker** 에 열어서 (File → Open) 검토한 뒤, GUI 의 *Save As → AASX* 메뉴로 자동 패키징한다.
> 4. ds2 ↔ AASX 변환은 사용자 도구가 책임진다. AI 는 절대 변환을 시도하지 말라.
> 5. **AAS 표준/시뮬레이션 메타 필드는 생성하지 말라.** `nameplate`, `handoverDocumentation`, `technicalData`, `simulationResult` 는 Promaker/AASX export 가 템플릿 또는 시뮬레이션 결과에서 채운다.

---

## 워크플로

```
┌─────────────────┐    파일 1개      ┌──────────────────┐    GUI 메뉴       ┌────────┐
│ 생성형 AI (LLM) │ ───────────────▶ │ Promaker (편집기) │ ────────────────▶ │ *.aasx │
│  ds2.json 작성  │  *.ds2.json      │  열어서 검증·편집 │  Save As → AASX  │ (배포용)│
└─────────────────┘                  └──────────────────┘                   └────────┘
```

---

## ds2.json 최상위 스키마 (DsStore — **모든 키 camelCase**)

```json
{
  "projects":   { "<guid>": { /* Project   */ } },
  "systems":    { "<guid>": { /* DsSystem  */ } },
  "flows":      { "<guid>": { /* Flow      */ } },
  "works":      { "<guid>": { /* Work      */ } },
  "calls":      { "<guid>": { /* Call      */ } },
  "apiDefs":    { "<guid>": { /* ApiDef    */ } },
  "arrowWorks": { "<guid>": { /* ArrowBetweenWorks */ } },
  "arrowCalls": { "<guid>": { /* ArrowBetweenCalls */ } }
}
```

규칙:
- 모든 컬렉션은 GUID 키 딕셔너리. 키와 값의 `id` 는 같은 GUID.
- `apiCalls` 는 별도 최상위 컬렉션이 **아니다** — 각 Call 안에 `apiCalls: [...]` 배열로 인라인.
- GUID 형식: `"11111111-1111-1111-1111-111111111111"` (8-4-4-4-12).
- 빈 컬렉션도 명시적으로 `{}` 또는 `[]` 로 포함 (생략 금지).

### 부모-자식 ID 체인

```
project
  ├── activeSystemIds  → System.id  (Active = 시퀀스 시스템)
  └── passiveSystemIds → System.id  (Passive = 디바이스/장치)

System.id  ──parent──→ Flow.parentId
Flow.id    ──parent──→ Work.parentId
Work.id    ──parent──→ Call.parentId
System.id  ──parent──→ ApiDef.parentId        (Passive 시스템이 노출하는 API)

ArrowBetweenWorks.parentId = System.id        ⚠️ 주의: Flow 가 아니라 SYSTEM.
  ├── sourceId = Work.id
  └── targetId = Work.id

ArrowBetweenCalls.parentId = Work.id
  ├── sourceId = Call.id
  └── targetId = Call.id

Call.apiCalls[].apiDefId      → ApiDef.id     (어떤 API 를 호출하는지)
Call.apiCalls[].originFlowId  → Flow.id       (이 ApiCall 이 속한 Active Flow)
```

---

## 엔티티별 필드

### project
```json
{
  "id":               "<guid>",
  "name":             "MyProject",
  "author":           "",
  "version":          "1.0.0",
  "dateTime":         "2026-04-29T00:00:00+09:00",
  "activeSystemIds":  ["<guid>"],
  "passiveSystemIds": ["<guid>", "<guid>"],
  "tokenSpecs":       []
}
```
> ❌ `nameplate`, `handoverDocumentation`, `technicalData`, `simulationResult` 는 생성하지 말 것 — AASX 표준 Submodel 또는 SequenceSimulation 박제 영역이다.

### system (Active 시퀀스 또는 Passive 디바이스)
```json
{
  "id":         "<guid>",
  "name":       "S1",
  "systemType": "Unit",
  "properties": []
}
```
- `systemType` 권장 값:
  - **Active 시스템**: `"Unit"` 또는 설비 타입명. 생략하면 구버전 호환 마이그레이션에서 기본 디바이스 타입이 들어갈 수 있으므로 명시 권장.
  - **Passive 디바이스**: `"Unit"`, `"Cylinder_1".."Cylinder_10"`, `"RobotWeldGrip"`, `"Part"` 등.

### flow
```json
{
  "id":         "<guid>",
  "name":       "F1",
  "parentId":   "<system.id>",
  "properties": []
}
```

### work (Flow 안의 작업 노드)
```json
{
  "id":         "<guid>",
  "parentId":   "<flow.id>",
  "name":       "F1.W1",
  "flowPrefix": "F1",
  "localName":  "W1",
  "status4":    0,
  "tokenRole":  0,
  "duration":   "00:00:00.5000000",
  "position":   { "x": 100, "y": 200, "w": 120, "h": 40 },
  "properties": []
}
```
- `name` = `"<flowPrefix>.<localName>"` (실제 직렬화 시 자동 합성되나 명시해도 무방).
- `position` 필드명: `x`, `y`, `w`, `h` (✅) — `Width`/`Height` (❌) 가 아님.
- `status4`: 0=Ready 1=Going 2=Finish 3=Homing.
- `tokenRole`: Flags — 0=None, 1=Source, 2=Ignore, 4=Sink, 조합 가능 (예: 5 = Source+Sink).
- `duration`: `"hh:mm:ss"` 또는 `"hh:mm:ss.fff0000"` TimeSpan.

### call (Work 안에서 디바이스 API 호출)
```json
{
  "id":             "<guid>",
  "parentId":       "<work.id>",
  "name":           "Cyl1.ADV",
  "devicesAlias":   "Cyl1",
  "apiName":        "ADV",
  "status4":        0,
  "position":       { "x": 100, "y": 240, "w": 120, "h": 40 },
  "apiCalls":       [ /* 인라인 ApiCall — 아래 참고 */ ],
  "callConditions": [],
  "properties":     []
}
```
- `name` = `"<devicesAlias>.<apiName>"`.

### apiCall (Call.apiCalls 안에 인라인)
```json
{
  "id":           "<guid>",
  "name":         "Cyl1.ADV",
  "apiDefId":     "<apiDef.id>",
  "originFlowId": "<flow.id>",
  "inputSpec":    { "Case": "UndefinedValue" },
  "outputSpec":   { "Case": "UndefinedValue" }
}
```
- `originFlowId` 는 이 ApiCall 이 호출되는 **Active Flow** 의 id (그 Call → Work → Flow chain).
- `inputSpec`/`outputSpec` 은 F# DU. 보통 `{"Case":"UndefinedValue"}` 그대로.

### apiDef (Passive 디바이스가 노출하는 API)
```json
{
  "id":               "<guid>",
  "name":             "ADV",
  "parentId":         "<passive system.id>",
  "apiDefActionType": { "Case": "Normal" },
  "txGuid":           "<work.id>",
  "rxGuid":           "<work.id>"
}
```
- `apiDefActionType`: `{"Case":"Normal"}` | `{"Case":"Push"}` | `{"Case":"Pulse"}` | `{"Case":"Time","Fields":[1000]}`.
- `txGuid`/`rxGuid` 는 보통 동일한 Passive 시스템 안의 Work id (그 API 동작이 매핑되는 Work).

### arrowBetweenWorks ⚠️ parentId 는 **System.id** (Flow 아님)
```json
{
  "id":        "<guid>",
  "parentId":  "<system.id>",
  "sourceId":  "<work.id>",
  "targetId":  "<work.id>",
  "arrowType": 1,
  "name":      ""
}
```
- 같은 System 안에서 Work 간 흐름을 표현. 다른 Flow 의 Work 도 연결 가능.
- `arrowType`: 0=Unspecified 1=Start 2=Reset **3=StartReset 4=ResetReset** 5=Group.

### arrowBetweenCalls (parentId = Work.id)
```json
{
  "id":        "<guid>",
  "parentId":  "<work.id>",
  "sourceId":  "<call.id>",
  "targetId":  "<call.id>",
  "arrowType": 1,
  "name":      ""
}
```

---

## Enum 정수값

| Enum                | 0           | 1     | 2      | 3          | 4          | 5     |
| ------------------- | ----------- | ----- | ------ | ---------- | ---------- | ----- |
| `status4`           | Ready       | Going | Finish | Homing     |            |       |
| `arrowType`         | Unspecified | Start | Reset  | StartReset | ResetReset | Group |
| `tokenRole` (Flags) | None=0      | Source=1 | Ignore=2 |        | Sink=4     |       |

DU 류는 문자열 `Case` 키 사용:
- `apiDefActionType`: `{"Case":"Normal"}` 등
- `inputSpec`/`outputSpec`: `{"Case":"UndefinedValue"}` 등

---

## 자주 쓰는 패턴

### Pattern 1 — Active 시퀀스 + Passive 디바이스 1대 호출
```
Project
└─ Active System "S1"
    └─ Flow "F1"
        ├─ Work "F1.Start"  (tokenRole=0, position 좌상단)
        │   └─ Call "Cyl1.ADV"   (apiDefId → Cyl1.ADV ApiDef)
        └─ Work "F1.End"    (position 우측)
            └─ Call "Cyl1.RET"
└─ Passive System "Cyl1" (systemType: "Unit")
    ├─ Flow "Cyl1_Flow"
    │   ├─ Work "Cyl1_Flow.ADV"  (duration="00:00:00.5")
    │   └─ Work "Cyl1_Flow.RET"  (duration="00:00:00.5")
    ├─ ApiDef "ADV" (parentId = Cyl1.id, txGuid/rxGuid = Cyl1_Flow.ADV.id)
    └─ ApiDef "RET" (parentId = Cyl1.id, txGuid/rxGuid = Cyl1_Flow.RET.id)
ArrowWorks:
  parentId=S1.id   F1.Start → F1.End      arrowType=1 (Start)
  parentId=Cyl1.id Cyl1_Flow.ADV → RET    arrowType=4 (ResetReset, ADV/RET 짝)
ArrowCalls:
  (없음 — Work 마다 Call 1 개씩이라)
```

### Pattern 2 — 한 Flow 안에 Work A → Work B 순차 진행
```
ArrowWorks: parentId=S1.id, sourceId=A.id, targetId=B.id, arrowType=1
```

### Pattern 3 — Work 안에 Call 두 개 순차 (Call C1 → C2)
```
ArrowCalls: parentId=Work.id, sourceId=C1.id, targetId=C2.id, arrowType=1
```

### Pattern 4 — 두 Flow 가 같은 Active System 안에서 cross-flow 연결
```
Active System S1 안에 Flow F1, F2.
ArrowWorks: parentId=S1.id, sourceId=F1.W1, targetId=F2.W1, arrowType=3 (StartReset)
```

---

## 검증 체크리스트 (출력 후 자가 점검)

- [ ] 모든 키가 **camelCase** (`projects`, 아니라 `Projects` ❌).
- [ ] 모든 `project.activeSystemIds`/`passiveSystemIds` 가 `systems` 의 id 와 매칭.
- [ ] 모든 `flow.parentId` = `system.id`.
- [ ] 모든 `work.parentId` = `flow.id`.
- [ ] 모든 `call.parentId` = `work.id`.
- [ ] 모든 `apiDef.parentId` = Passive `system.id`.
- [ ] 모든 `arrowWorks[].parentId` = **`system.id`** (⚠️ Flow 아님).
- [ ] 모든 `arrowCalls[].parentId` = `work.id`.
- [ ] 모든 `arrowWorks[].sourceId/targetId` = `work.id`.
- [ ] 모든 `arrowCalls[].sourceId/targetId` = `call.id`.
- [ ] 모든 `call.apiCalls[].apiDefId` = `apiDef.id`.
- [ ] 모든 `call.apiCalls[].originFlowId` = Active `flow.id`.
- [ ] 컬렉션 키와 값의 `id` 동일.
- [ ] `position`: `x`, `y`, `w`, `h` (소문자 단일 글자).
- [ ] `nameplate`/`handoverDocumentation`/`technicalData`/`simulationResult` 필드 **없음**.

---

## 흔한 실수

| ❌ 잘못된 것                                | ✅ 올바른 것                              |
| ------------------------------------------- | ----------------------------------------- |
| `.aasx` 파일 직접 생성                      | `*.ds2.json` 만 생성                      |
| PascalCase 키 (`"Projects"`, `"Systems"`)   | camelCase 키 (`"projects"`, `"systems"`)  |
| `position: { Width:120, Height:40 }`         | `position: { x:.., y:.., w:120, h:40 }`   |
| `arrowWorks.parentId = flow.id`             | `arrowWorks.parentId = system.id`         |
| `apiCalls` 를 별도 최상위 컬렉션으로        | 각 Call 안에 `apiCalls:[...]` 인라인       |
| `technicalData`/`simulationResult` 채워서 출력 | 해당 필드 자체 출력하지 않음              |
| `apiDefActionType: "Normal"` (문자열)       | `apiDefActionType: { "Case": "Normal" }` |
| `inputSpec: null`                           | `inputSpec: { "Case": "UndefinedValue" }` |
| `duration: 500` 또는 `"500ms"`              | `duration: "00:00:00.5000000"`            |

---

## 미니멀 예시 — 1 Active + 1 Passive + Call/Arrow 짝

[`SAMPLE.ds2.json`](SAMPLE.ds2.json) — 그대로 복제하여 GUID 만 새로 발급한 뒤 확장하는 것이 안전.

---

## LLM system prompt 한 줄 요약

> *Your output for any DS2/sequence-control modeling request must be a single `*.ds2.json` file conforming to the DsStore schema in `AI_GUIDE_DS2_JSON.md`. Use **camelCase keys**. ArrowBetweenWorks `parentId` is the **System** id (not Flow). **DO NOT produce `.aasx`** and **DO NOT include `nameplate`, `handoverDocumentation`, `technicalData`, or `simulationResult`** — the user opens the JSON in Promaker which packages AASX and fills standard/simulation data.*
