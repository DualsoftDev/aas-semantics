"""
ds2 엔티티 별 SDK 수준 상세 정보 — F# 타입 정의 + 필드 테이블 + 관계 + 예제.
generate.py 가 viewer (index.html) 에 임베드.

원본: https://github.com/DualsoftDev/ds2/blob/master/Solutions/Core/Ds2.Core/Entities.fs
"""

DS2_REPO = "https://github.com/DualsoftDev/ds2/blob/master"
ENTITIES_FS = f"{DS2_REPO}/Solutions/Core/Ds2.Core/Entities.fs"
ENUM_FS     = f"{DS2_REPO}/Solutions/Core/Ds2.Core/Enum.fs"
ABSTRACT_FS = f"{DS2_REPO}/Solutions/Core/Ds2.Core/AbstractClass.fs"
TOKEN_FS    = f"{DS2_REPO}/Solutions/Core/Ds2.Core/TokenTypes.fs"
MODEL_FS    = f"{DS2_REPO}/Solutions/Core/Ds2.Core/ModelClass.fs"


# 공통 부모 클래스 — 모든 엔티티가 상속.
DS_ENTITY_FIELDS = [
    ("Id",   "Guid",   "Guid.NewGuid()", "Guid", "전역 고유 식별자 (자동 생성)"),
    ("Name", "string", "(생성자 인자)",     "Name", "엔티티 이름"),
]

DS_CHILD_FIELDS = [
    ("ParentId", "Guid", "(생성자 인자)", "ParentId", "부모 엔티티 Id 참조"),
]


# ══════════════════════════════════════════════════════════════════════════════
ENTITY_DETAILS = {

    # ── PROJECT ────────────────────────────────────────────────────────────
    "entity/Project/1/0": {
        "fsharpType": """type Project [<JsonConstructor>] internal (name) =
    inherit DsEntity(name)

    member val ActiveSystemIds       = ResizeArray<Guid>() with get, set
    member val PassiveSystemIds      = ResizeArray<Guid>() with get, set

    member val Nameplate             : Nameplate option             = None
    member val HandoverDocumentation : HandoverDocumentation option = None
    member val TechnicalData         : TechnicalData option         = None
    member val SimulationResult      : SimulationScenario option    = None

    member val TokenSpecs = ResizeArray<TokenSpec>()
    member val Author     : string         = ""
    member val DateTime   : DateTimeOffset = DateTimeOffset.Now
    member val Version    : string         = "1.0.0" """,
        "inherits": [("DsEntity", ABSTRACT_FS)],
        "fields": DS_ENTITY_FIELDS + [
            ("ActiveSystemIds",       "ResizeArray<Guid>",          "[]",                 "ActiveSystemIds (Skip)",  "활성 (능동) 시스템 Id 리스트"),
            ("PassiveSystemIds",      "ResizeArray<Guid>",          "[]",                 "PassiveSystemIds (Skip)", "패시브 (디바이스) 시스템 Id 리스트"),
            ("Nameplate",             "Nameplate option",           "None",               "Nameplate (Skip)",        "별도 SM (IDTA 02006) 으로 직렬화"),
            ("HandoverDocumentation", "HandoverDocumentation option", "None",             "HandoverDocumentation (Skip)", "별도 SM (IDTA 02004) 으로 직렬화"),
            ("TechnicalData",         "TechnicalData option",       "None",               "TechnicalData (Skip)",    "별도 SM (IDTA 02003) 으로 직렬화 — 시뮬 결과는 포함하지 않음"),
            ("SimulationResult",      "SimulationScenario option",  "None",               "SimulationResult (Skip)", "SequenceSimulation/SystemProperties/SimulationResult 로 직렬화되는 시뮬 KPI 박제"),
            ("TokenSpecs",            "ResizeArray<TokenSpec>",     "[]",                 "TokenSpecs",              "토큰 유형 카탈로그"),
            ("Author",                "string",                     "\"\"",               "Author",                  "프로젝트 작성자"),
            ("DateTime",              "DateTimeOffset",             "DateTimeOffset.Now", "DateTime",                "마지막 수정 시각"),
            ("Version",               "string",                     "\"1.0.0\"",          "Version",                 "프로젝트 버전 (semver)"),
        ],
        "relationships": [
            ("Project.ActiveSystemIds[*]",  "→ DsSystem (active)", "entity/System/1/0"),
            ("Project.PassiveSystemIds[*]", "→ DsSystem (passive/device)", "entity/Device/1/0"),
            ("Project.TokenSpecs[*]",       "→ TokenSpec",         "entity/TokenSpec/1/0"),
        ],
        "exampleFsharp": """let project = Project("MyFactory")
project.Author  <- "ahn@dualsoft.com"
project.Version <- "1.2.0"
project.ActiveSystemIds.Add(cellA.Id)
project.PassiveSystemIds.Add(cylinder.Id)""",
        "aasMapping": "Project.* 필드는 SequenceModel 서브모델 안의 'Project' SubmodelElementCollection 에 매핑. Nameplate / HandoverDocumentation / TechnicalData 는 IDTA 표준 서브모델로 분리되고, SimulationResult 는 SequenceSimulation/SystemProperties/SimulationResult SMC 로 emit.",
        "sourceFiles": [(ENTITIES_FS, "Entities.fs (Project)")],
    },

    # ── SYSTEM (active) ────────────────────────────────────────────────────
    "entity/System/1/0": {
        "fsharpType": """type DsSystem [<JsonConstructor>] internal (name) =
    inherit DsEntity(name)

    member val Properties = ResizeArray<SystemSubmodelProperty>() with get, set
    member val IRI        : string option = None with get, set
    member val SystemType : string option = None with get, set""",
        "inherits": [("DsEntity", ABSTRACT_FS)],
        "fields": DS_ENTITY_FIELDS + [
            ("Properties", "ResizeArray<SystemSubmodelProperty>", "[]", "(submodel-specific)", "도메인별 시스템 속성 (Simulation/Control/Monitoring/...)"),
            ("IRI",        "string option", "None",        "IRI",        "전역 식별 IRI (선택, 패시브 디바이스 식별용)"),
            ("SystemType", "string option", "None",        "SystemType", "디바이스 카탈로그 타입 (예: Cylinder_2, RobotWeldGrip)"),
        ],
        "relationships": [
            ("DsSystem ← Project.ActiveSystemIds",  "← Project",         "entity/Project/1/0"),
            ("DsSystem → Flow[*]",                  "1 시스템 = 다수 Flow", "entity/Flow/1/0"),
        ],
        "exampleFsharp": """let cellA = DsSystem("Cell-A")
cellA.SystemType <- Some "AssemblyCell"
project.ActiveSystemIds.Add(cellA.Id)""",
        "aasMapping": "Active 시스템은 SequenceModel/Project/ActiveSystems SML 안에 SMC 로 매핑. 같은 타입(DsSystem)이지만 Project 의 ActiveSystemIds vs PassiveSystemIds 멤버십으로 능동/패시브 구분.",
        "sourceFiles": [(ENTITIES_FS, "Entities.fs (DsSystem)")],
    },

    # ── DEVICE (passive) ───────────────────────────────────────────────────
    "entity/Device/1/0": {
        "fsharpType": """// Device 는 별도 타입이 아닌 DsSystem (passive 역할).
// Project.PassiveSystemIds 에 등록된 DsSystem 인스턴스.

type DsSystem [<JsonConstructor>] internal (name) =
    inherit DsEntity(name)
    member val IRI        : string option = None    // 디바이스 식별 IRI
    member val SystemType : string option = None    // 카탈로그 타입 (Cylinder_2 등)""",
        "inherits": [("DsEntity", ABSTRACT_FS)],
        "fields": DS_ENTITY_FIELDS + [
            ("IRI",        "string option", "None", "IRI",        "디바이스 IRI — 외부 카탈로그 / OPC UA 서버 매핑"),
            ("SystemType", "string option", "None", "SystemType", "카탈로그 타입 키 — 시뮬/제어 코드젠의 분기 판단용"),
        ],
        "relationships": [
            ("Device ← Project.PassiveSystemIds", "← Project",     "entity/Project/1/0"),
            ("Device → ApiDef[*]",                "디바이스가 노출", "entity/ApiDef/1/0"),
        ],
        "exampleFsharp": """let cylinder1 = DsSystem("Cylinder1")
cylinder1.SystemType <- Some "Cylinder_2"
cylinder1.IRI <- Some "https://factory.example.com/devices/cyl-1"
project.PassiveSystemIds.Add(cylinder1.Id)""",
        "aasMapping": "Passive 디바이스는 SequenceModel/Project/DeviceReferences SML 또는 분리 저장 모드에서 별도 AASX 파일로 export.",
        "sourceFiles": [(ENTITIES_FS, "Entities.fs (DsSystem 재사용)")],
    },

    # ── FLOW ───────────────────────────────────────────────────────────────
    "entity/Flow/1/0": {
        "fsharpType": """type Flow [<JsonConstructor>] internal (name, parentId) =
    inherit DsChild(name, parentId)

    member val Properties = ResizeArray<FlowSubmodelProperty>() with get, set""",
        "inherits": [("DsEntity", ABSTRACT_FS), ("DsChild", ABSTRACT_FS)],
        "fields": DS_ENTITY_FIELDS + DS_CHILD_FIELDS + [
            ("Properties", "ResizeArray<FlowSubmodelProperty>", "[]", "(submodel-specific)", "도메인별 Flow 속성"),
        ],
        "relationships": [
            ("Flow.ParentId", "→ DsSystem (active)", "entity/System/1/0"),
            ("Flow → Work[*]", "1 Flow = 다수 Work (DsChild.ParentId)", "entity/Work/1/0"),
            ("ArrowWork.ParentId", "Flow 가 아니라 DsSystem 을 참조", "entity/ArrowWork/1/0"),
        ],
        "exampleFsharp": """let mainFlow = Flow("MainFlow", cellA.Id)
// Work 들이 mainFlow.Id 를 ParentId 로 등록""",
        "aasMapping": "Flow 는 SequenceModel 안의 System SMC 하위 Flows SML 안 SMC 로 매핑.",
        "sourceFiles": [(ENTITIES_FS, "Entities.fs (Flow)")],
    },

    # ── WORK ───────────────────────────────────────────────────────────────
    "entity/Work/1/0": {
        "fsharpType": """type Work [<JsonConstructor>] internal (flowPrefix: string, localName: string, parentId: Guid) =
    inherit DsChild("", parentId)

    member val Properties  = ResizeArray<WorkSubmodelProperty>()
    member val FlowPrefix  : string  = flowPrefix
    member val LocalName   : string  = localName
    member val ReferenceOf : Guid option   = None     // 다른 Work 참조 (ref 노드)
    member val Status4     : Status4       = Ready    // 런타임 상태 (R/G/F/H)
    member val Position    : Xywh option   = None     // 캔버스 좌표
    member val TokenRole   : TokenRole     = None     // None / Source / Ignore / Sink
    member val Duration    : TimeSpan option = None   // 시뮬 사이클 타임

    // Name = "{FlowPrefix}.{LocalName}" 자동 합성""",
        "inherits": [("DsEntity", ABSTRACT_FS), ("DsChild", ABSTRACT_FS)],
        "fields": DS_ENTITY_FIELDS + DS_CHILD_FIELDS + [
            ("FlowPrefix",  "string",         "(인자)",        "FlowPrefix (Skip)",  "Flow 접두어 — Name 의 앞부분"),
            ("LocalName",   "string",         "(인자)",        "LocalName (Skip)",   "Work 로컬명 — Name 의 뒷부분"),
            ("ReferenceOf", "Guid option",    "None",         "ReferenceOf",        "원본 Work Id (참조 노드일 때)"),
            ("Status4",     "Status4 enum",   "Ready",        "Status",             "런타임 상태: Ready=0 · Going=1 · Finish=2 · Homing=3"),
            ("Position",    "Xywh option",    "None",         "Position",           "캔버스 좌표 (X,Y,W,H)"),
            ("TokenRole",   "TokenRole flags","None",         "TokenRole",          "토큰 역할: None / Source(시드) / Ignore / Sink"),
            ("Duration",    "TimeSpan option","None",         "Duration",           "설계 사이클 타임 (시뮬용)"),
        ],
        "relationships": [
            ("Work.ParentId", "→ Flow", "entity/Flow/1/0"),
            ("Work → Call[*]", "1 Work = 다수 Call (DsChild.ParentId)", "entity/Call/1/0"),
            ("Work ↔ ArrowWork", "Work 간 전이 (Source/Target)", "entity/ArrowWork/1/0"),
            ("Work.ReferenceOf", "참조 Work (다른 Work 의 미러)", "entity/Work/1/0"),
        ],
        "stateMachine": [
            ("Ready (R)",  "초기/대기 — 토큰 도착하면 Going 으로 전이"),
            ("Going (G)",  "진행 중 — Calls 실행 중. 완료 시 Finish 로 전이"),
            ("Finish (F)", "완료 — 토큰 다음 Work 로 이동, 다음 사이클 위해 Homing 으로 전이"),
            ("Homing (H)", "복귀 중 — 리셋 조건 충족 시 Ready 로 복귀"),
        ],
        "exampleFsharp": """let pickup = Work("MainFlow", "Pickup", mainFlow.Id)
pickup.Duration  <- Some (TimeSpan.FromSeconds 12.5)
pickup.TokenRole <- TokenRole.Source     // 토큰 시드 지점
// Name = "MainFlow.Pickup" 자동 생성""",
        "aasMapping": "Work 는 SequenceModel/.../Flows/<flow>/Works SML 안 SMC. Status4 는 시뮬/모니터링 시 런타임 상태.",
        "sourceFiles": [(ENTITIES_FS, "Entities.fs (Work)"), (ENUM_FS, "Enum.fs (Status4 / TokenRole)")],
    },

    # ── CALL ───────────────────────────────────────────────────────────────
    "entity/Call/1/0": {
        "fsharpType": """type Call [<JsonConstructor>] internal (devicesAlias: string, apiName: string, parentId: Guid) =
    inherit DsChild("", parentId)

    member val Properties     = ResizeArray<CallSubmodelProperty>()
    member val Status4        : Status4    = Ready
    member val Position       : Xywh option = None
    member val ApiCalls       = ResizeArray<ApiCall>()         // 런타임 바인딩
    member val CallConditions = ResizeArray<CallCondition>()
    member val ReferenceOf    : Guid option = None

    member val DevicesAlias = devicesAlias    // Name 의 앞부분
    member val ApiName      = apiName         // Name 의 뒷부분
    // Name = "{DevicesAlias}.{ApiName}" 자동 합성""",
        "inherits": [("DsEntity", ABSTRACT_FS), ("DsChild", ABSTRACT_FS)],
        "fields": DS_ENTITY_FIELDS + DS_CHILD_FIELDS + [
            ("DevicesAlias",   "string",                          "(인자)",  "DevicesAlias (Skip)", "디바이스 별칭 — Name 의 앞부분"),
            ("ApiName",        "string",                          "(인자)",  "ApiName (Skip)",      "호출하는 API 명 — Name 의 뒷부분"),
            ("Status4",        "Status4 enum",                    "Ready",  "Status",              "런타임 상태 (R/G/F/H)"),
            ("Position",       "Xywh option",                     "None",   "Position",            "캔버스 좌표"),
            ("ApiCalls",       "ResizeArray<ApiCall>",            "[]",     "ApiCalls (Skip)",     "런타임 바인딩 (Tag 매핑) — 별도 처리"),
            ("CallConditions", "ResizeArray<CallCondition>",      "[]",     "CallConditions",      "조건부 호출 (AutoAux/ComAux/SkipUnmatch)"),
            ("ReferenceOf",    "Guid option",                     "None",   "ReferenceOf",         "원본 Call Id (참조)"),
        ],
        "relationships": [
            ("Call.ParentId",  "→ Work", "entity/Work/1/0"),
            ("Call.ApiName",   "→ ApiDef.Name (디바이스가 노출)", "entity/ApiDef/1/0"),
            ("Call.ApiCalls",  "→ ApiCall (런타임 Tag 바인딩)", "entity/ApiCall/1/0"),
            ("Call ↔ ArrowCall", "Call 간 순서 (Source/Target)", "entity/ArrowCall/1/0"),
        ],
        "exampleFsharp": """let moveCall = Call("Robot1", "MOVE_TO_A", pickup.Id)
// Name = "Robot1.MOVE_TO_A" 자동 생성

// CallCondition 추가 (AutoAux 자동 보조)
let cond = CallCondition()
cond.Type  <- Some CallConditionType.AutoAux
moveCall.CallConditions.Add(cond)""",
        "aasMapping": "Call 은 Work SMC 하위 Calls SML 안 SMC. ApiCalls 컬렉션은 [<AasxField(Skip)>] 로 별도 ApiCalls SML 컨테이너에 분리 저장됨.",
        "sourceFiles": [(ENTITIES_FS, "Entities.fs (Call)"), (ENUM_FS, "Enum.fs (CallConditionType)")],
    },

    # ── APIDEF ────────────────────────────────────────────────────────────
    "entity/ApiDef/1/0": {
        "fsharpType": """and ApiDef [<JsonConstructor>] internal (name, parentId) =
    inherit DsChild(name, parentId)

    member val ApiDefActionType : ApiDefActionType = Normal
    member val TxGuid : Guid option = None    // 송신 IOTag 참조
    member val RxGuid : Guid option = None    // 수신 IOTag 참조

// ApiDefActionType DU:
//   Normal  | Push | Pulse | Time of int (ms)""",
        "inherits": [("DsEntity", ABSTRACT_FS), ("DsChild", ABSTRACT_FS)],
        "fields": DS_ENTITY_FIELDS + DS_CHILD_FIELDS + [
            ("ApiDefActionType", "ApiDefActionType DU", "Normal", "ApiDefActionType", "동작 유형: Normal · Push · Pulse · Time(ms)"),
            ("TxGuid",           "Guid option",         "None",   "TxGuid",           "송신 IOTag Id (디바이스 → 호출자 응답)"),
            ("RxGuid",           "Guid option",         "None",   "RxGuid",           "수신 IOTag Id (호출자 → 디바이스 트리거)"),
        ],
        "relationships": [
            ("ApiDef.ParentId", "→ DsSystem (Device 가 노출)", "entity/Device/1/0"),
            ("ApiDef ← Call.ApiName", "← Call (이름 매칭)", "entity/Call/1/0"),
            ("ApiDef ← ApiCall.ApiDefId", "← ApiCall (Id 참조)", "entity/ApiCall/1/0"),
        ],
        "exampleFsharp": """let moveApi = ApiDef("MOVE_TO_A", robot1.Id)
moveApi.ApiDefActionType <- ApiDefActionType.Pulse
// IOTag 등록 후 TxGuid / RxGuid 연결""",
        "aasMapping": "ApiDef 는 디바이스 SMC 하위 ApiDefs SML 안 SMC.",
        "sourceFiles": [(ENTITIES_FS, "Entities.fs (ApiDef)"), (ENUM_FS, "Enum.fs (ApiDefActionType)")],
    },

    # ── APICALL ───────────────────────────────────────────────────────────
    "entity/ApiCall/1/0": {
        "fsharpType": """and ApiCall [<JsonConstructor>] internal (name) =
    inherit DsEntity(name)

    member val InTag        : IOTag option = None    // 호출 트리거 태그
    member val OutTag       : IOTag option = None    // 응답 태그
    member val ApiDefId     : Guid option  = None    // 바인딩된 ApiDef
    member val InputSpec    : ValueSpec    = UndefinedValue
    member val OutputSpec   : ValueSpec    = UndefinedValue
    member val OriginFlowId : Guid option  = None    // 호출하는 Flow Id""",
        "inherits": [("DsEntity", ABSTRACT_FS)],
        "fields": DS_ENTITY_FIELDS + [
            ("InTag",        "IOTag option",  "None",            "InTag",        "호출 트리거 태그 (호출자 → 디바이스)"),
            ("OutTag",       "IOTag option",  "None",            "OutTag",       "응답 태그 (디바이스 → 호출자)"),
            ("ApiDefId",     "Guid option",   "None",            "ApiDefId",     "바인딩된 ApiDef Id"),
            ("InputSpec",    "ValueSpec DU",  "UndefinedValue",  "InputSpec",    "입력 값 스펙 (상수/태그 참조/표현식)"),
            ("OutputSpec",   "ValueSpec DU",  "UndefinedValue",  "OutputSpec",   "출력 값 스펙"),
            ("OriginFlowId", "Guid option",   "None",            "OriginFlowId", "호출자 Flow Id (역참조)"),
        ],
        "relationships": [
            ("ApiCall ← Call.ApiCalls",   "← Call (소비자)",        "entity/Call/1/0"),
            ("ApiCall.ApiDefId",          "→ ApiDef (시그니처 정의)", "entity/ApiDef/1/0"),
            ("ApiCall.OriginFlowId",      "→ Flow (호출 컨텍스트)",   "entity/Flow/1/0"),
        ],
        "exampleFsharp": """let apiCall = ApiCall("MOVE_TO_A_call_1")
apiCall.ApiDefId     <- Some moveApi.Id
apiCall.OriginFlowId <- Some mainFlow.Id

let inTag = IOTag("M_Trigger", "M001", "이동 시작 신호")
inTag.DataType <- IOTagDataType.BOOL
apiCall.InTag <- Some inTag

let outTag = IOTag("M_Done", "M002", "이동 완료 신호")
outTag.DataType <- IOTagDataType.BOOL
apiCall.OutTag <- Some outTag

moveCall.ApiCalls.Add(apiCall)""",
        "aasMapping": "ApiCall 은 별도 ApiCalls SML 안 SMC 로 저장 (Call.ApiCalls 는 Skip 마킹). ApiDefId 로 후처리 시 ApiDef 와 결합.",
        "sourceFiles": [(ENTITIES_FS, "Entities.fs (ApiCall)"), (MODEL_FS, "ModelClass.fs (IOTag)")],
    },

    # ── TOKENSPEC ─────────────────────────────────────────────────────────
    "entity/TokenSpec/1/0": {
        "fsharpType": """// F# record (참조 타입). DsEntity 비상속.
type TokenSpec = {
    Id: int
    Label: string
    Fields: Map<string, string>
    WorkId: System.Guid option   // 시드 Source Work
}""",
        "inherits": [],
        "fields": [
            ("Id",     "int",                  "(필수)",     "Id",     "토큰 번호 (Project 내 고유)"),
            ("Label",  "string",               "(필수)",     "Label",  "사람용 표시명 (예: 'Steel Door')"),
            ("Fields", "Map<string, string>",  "Map.empty",  "Fields", "추가 필드 (레시피/제품 데이터)"),
            ("WorkId", "Guid option",          "None",       "WorkId", "시드 시작 Work Id"),
        ],
        "relationships": [
            ("TokenSpec ← Project.TokenSpecs", "← Project",       "entity/Project/1/0"),
            ("TokenSpec.WorkId",               "→ Work (시드 지점)", "entity/Work/1/0"),
        ],
        "exampleFsharp": """let recipeA = {
    Id     = 1
    Label  = "Steel Door"
    Fields = Map.ofList [ "thickness", "2mm"; "color", "red" ]
    WorkId = Some pickup.Id
}
project.TokenSpecs.Add(recipeA)""",
        "aasMapping": "TokenSpec 은 SequenceModel/Project/TokenSpecs SML 안 SMC 로 export.",
        "sourceFiles": [(TOKEN_FS, "TokenTypes.fs")],
    },

    # ── ARROW WORK ────────────────────────────────────────────────────────
    "entity/ArrowWork/1/0": {
        "fsharpType": """type ArrowBetweenWorks [<JsonConstructor>] internal (parentId, sourceId, targetId, arrowType) =
    inherit DsArrow(parentId, sourceId, targetId, arrowType)

// DsArrow:
type DsArrow(parentId, sourceId, targetId, arrowType) =
    inherit DsChild("", parentId)
    member val SourceId  = sourceId
    member val TargetId  = targetId
    member val ArrowType : ArrowType = arrowType""",
        "inherits": [("DsEntity", ABSTRACT_FS), ("DsChild", ABSTRACT_FS), ("DsArrow", ABSTRACT_FS)],
        "fields": DS_ENTITY_FIELDS + DS_CHILD_FIELDS + [
            ("SourceId",  "Guid",      "(인자)", "Source", "출발 Work Id"),
            ("TargetId",  "Guid",      "(인자)", "Target", "도착 Work Id"),
            ("ArrowType", "ArrowType", "(인자)", "Type",   "전이 의미: Unspecified=0 · Start=1 · Reset=2 · StartReset=3 · ResetReset=4 · Group=5"),
        ],
        "relationships": [
            ("ArrowWork.ParentId", "→ DsSystem (Flow 가 아님)", "entity/System/1/0"),
            ("ArrowWork.SourceId / TargetId", "→ Work", "entity/Work/1/0"),
        ],
        "stateMachine": [
            ("Start (=1)",       "Source 완료(F) 시 Target 시작(R→G)"),
            ("Reset (=2)",       "Source 시작(R→G) 시 Target 리셋(F→H 강제)"),
            ("StartReset (=3)",  "Source 완료 → Target 시작 + Target 시작 → Source 리셋"),
            ("ResetReset (=4)",  "Source 시작 → Target 리셋 + Target 시작 → Source 리셋"),
            ("Group (=5)",       "그룹 연결 (논리 묶음, 실행 의미 없음)"),
        ],
        "exampleFsharp": """let arrow = ArrowBetweenWorks(
    parentId  = cellA.Id,
    sourceId  = w1.Id,
    targetId  = w2.Id,
    arrowType = ArrowType.StartReset)""",
        "aasMapping": "ArrowWork 는 System SMC 하위 Arrows SML 안 SMC 로 export. parentId 는 System.id 이며, 같은 System 안 다른 Flow 의 Work 도 연결 가능.",
        "sourceFiles": [(ENTITIES_FS, "Entities.fs (ArrowBetweenWorks)"), (ABSTRACT_FS, "AbstractClass.fs (DsArrow)"), (ENUM_FS, "Enum.fs (ArrowType)")],
    },

    # ── ARROW CALL ────────────────────────────────────────────────────────
    "entity/ArrowCall/1/0": {
        "fsharpType": """type ArrowBetweenCalls [<JsonConstructor>] internal (parentId, sourceId, targetId, arrowType) =
    inherit DsArrow(parentId, sourceId, targetId, arrowType)

// DsArrow 상속 — ArrowBetweenWorks 와 같은 구조, parentId 가 Work Id 인 점만 다름""",
        "inherits": [("DsEntity", ABSTRACT_FS), ("DsChild", ABSTRACT_FS), ("DsArrow", ABSTRACT_FS)],
        "fields": DS_ENTITY_FIELDS + DS_CHILD_FIELDS + [
            ("SourceId",  "Guid",      "(인자)", "Source", "출발 Call Id"),
            ("TargetId",  "Guid",      "(인자)", "Target", "도착 Call Id"),
            ("ArrowType", "ArrowType", "(인자)", "Type",   "Call 간 전이 의미 (대부분 Start)"),
        ],
        "relationships": [
            ("ArrowCall.ParentId", "→ Work (Call 들의 부모)", "entity/Work/1/0"),
            ("ArrowCall.SourceId / TargetId", "→ Call", "entity/Call/1/0"),
        ],
        "exampleFsharp": """let callArrow = ArrowBetweenCalls(
    parentId  = pickup.Id,
    sourceId  = call1.Id,
    targetId  = call2.Id,
    arrowType = ArrowType.Start)""",
        "aasMapping": "ArrowCall 은 Work SMC 하위 Arrows SML 안 SMC 로 export.",
        "sourceFiles": [(ENTITIES_FS, "Entities.fs (ArrowBetweenCalls)"), (ABSTRACT_FS, "AbstractClass.fs (DsArrow)")],
    },
}


# ══════════════════════════════════════════════════════════════════════════════
# Phase 0/1 풍부화 (수직 슬라이스): Work + SequenceMonitoring + OEE
# ──────────────────────────────────────────────────────────────────────────────
# 출처:
#   - 시나리오 / Call 시퀀스: HelpDS/samples/{automotive,semiconductor,pharma,electronics,logistics}
#   - PLC 5벤더 태그: HelpDS/aasPages 자료 + ds-vs-plc.html
#   - 8 Duality Cases: HelpDS/ds-language.html
#   - IDTA 02026 / OEE 산식: HelpDS/submodelTemplate/SequenceMonitoring.html, ISO 22400-2:2014


# ── entity/Work/1/0 — 시나리오 + ds2.json + PLC 등가 + 표준 + 부록 링크 ────────
ENTITY_DETAILS["entity/Work/1/0"].update({

    "scenarios": [
        {
            "domain": "🚗 Automotive · Body Press",
            "system": "PressLine — 현대로보틱스 차체프레스",
            "meta": "Cycle ~8s · 120 parts/h",
            "body": (
                "차체 프레스 라인의 6-Work 시퀀스 중 <strong>W2 1차프레스</strong> Work. "
                "Going(G) 단계에서 Drawing 동작 (1.5s) 을 수행하고, Finish(F) 시 W3 2차프레스로 토큰 전이."
            ),
            "calls": [
                {"name": "슬라이드하강 (Slide Down)", "duration": "1.0s"},
                {"name": "드로잉 (Drawing)", "duration": "1.5s"},
                {"name": "슬라이드상승 (Slide Up)", "duration": "1.0s"},
            ],
            "timing": "",  # rendered separately if needed
        },
        {
            "domain": "🔬 Semiconductor · CVD/PVD",
            "system": "Centura 5200 — AMAT 박막증착",
            "meta": "Throughput 60 wph · 350°C / 2.5 mTorr",
            "body": (
                "웨이퍼 박막증착 6-Work 라인의 <strong>W4 플라즈마생성</strong> Work. "
                "RF 파워 1500W 인가 → 플라즈마 안정화까지 1.5s 소요. Duration 필드로 시뮬용 사이클타임 박제."
            ),
            "calls": [
                {"name": "플라즈마발생 (Plasma Ignition)", "duration": "1.5s"},
                {"name": "RF파워조절 (RF Power Control)", "duration": "1.2s"},
                {"name": "플라즈마안정화 (Plasma Stabilization)", "duration": "1.1s"},
            ],
        },
        {
            "domain": "💊 Pharma · Tableting",
            "system": "고속 타정 라인",
            "meta": "Cycle ~6s · GMP 등급",
            "body": "정제 제조 6-Work 중 <strong>W3 타정</strong>. Punch 정렬 → 압축력 제어 → 배출 직렬 진행.",
            "calls": [
                {"name": "펀치정렬 (Punch Alignment)", "duration": "0.6s"},
                {"name": "압축력제어 (Compression)", "duration": "0.7s"},
                {"name": "배출 (Ejection)", "duration": "0.5s"},
            ],
        },
    ],

    "ds2JsonSnippet": {
        "title": "동일 시나리오의 ds2.json 표현",
        "description": "Work 는 GUID 키 딕셔너리 항목. parentId 는 Flow.id, status4=0(Ready), duration 은 시뮬용 사이클타임.",
        "json": """{
  "works": {
    "88888888-8888-8888-8888-888888888888": {
      "id":         "88888888-8888-8888-8888-888888888888",
      "parentId":   "44444444-4444-4444-4444-444444444444",
      "name":       "PressLine.W2_1차프레스",
      "flowPrefix": "PressLine",
      "localName":  "W2_1차프레스",
      "status4":    0,
      "tokenRole":  0,
      "duration":   "00:00:03.5000000",
      "position":   { "x": 240, "y": 200, "w": 120, "h": 40 },
      "properties": []
    }
  }
}""",
    },

    "industryStandards": [
        {"name": "IEC 61131-3", "scope": "Sequential Function Chart 매핑 기반", "url": "https://webstore.iec.ch/publication/4552"},
        {"name": "ISA-95 (IEC 62264)", "scope": "Operational Activity Model 호환", "url": "https://www.isa.org/standards-and-publications/isa-standards/isa-standards-committees/isa95"},
        {"name": "IDTA 02024-1-0", "scope": "SequenceControl 표준 SubmodelElement", "url": "https://industrialdigitaltwin.org/en/content-hub/submodels"},
    ],

    "relatedCds": [
        ("entity/Flow/1/0", "Flow", "Work 의 부모 — 순차 흐름의 컨테이너"),
        ("entity/Call/1/0", "Call", "Work 안의 디바이스 API 호출"),
        ("entity/ArrowWork/1/0", "ArrowWork", "Work 간 전이 / 리셋 규칙"),
        ("sm/SequenceMonitoring/1/0", "SeqMonSm", "Work 의 R/G/F/H 런타임 상태를 추적"),
        ("sim/Kpi/CycleTime/1/0", "CTkpi", "Work 별 사이클타임 박제 KPI"),
    ],

    "appendixLinks": [
        ("duality", "Duality 8 Cases — 이중성 원리", "Work = Bit 그룹 (Case 3) + R⊕G⊕F⊕H FSM (Case 5)"),
    ],
})


# ── sm/SequenceMonitoring/1/0 — IDTA 02026 SubmodelElement Tree ────────────
ENTITY_DETAILS["sm/SequenceMonitoring/1/0"] = {
    "fsharpType": """// ds2 측 SequenceMonitoringSubmodel — Work/Call 의 R/G/F/H 런타임 상태,
// 진행률, 디바이스 IO 값, MT/WT/TC 시간 메트릭, 생산 사이클 이벤트를 수집.

type SystemSnapshot = {
    Timestamp     : DateTime
    SystemName    : string
    WorkStates    : Map<Guid, NodeState>          // R/G/F/H
    CallStates    : Map<Guid, NodeState>
    WorkProgress  : Map<Guid, float>              // 0.0 ~ 1.0
    DeviceStates  : Map<string, bool>             // IO 값
    Statistics    : ProductionStatistics
}

type ProductionStatistics = {
    TotalWorks       : int
    CompletedWorks   : int
    TotalCalls       : int
    CompletedCalls   : int
    ElapsedTime      : float    // seconds
    AverageProgress  : float    // 0.0 ~ 1.0
}""",

    "smcProperties": [
        {"idShort": "MonitoringConfiguration", "semanticId": "https://admin-shell.io/IDTA/02026/1/0/MonitoringConfiguration",
         "valueType": "SubmodelElementCollection", "multiplicity": "1", "description": "샘플링 주기 / 보존 정책 / 활성 메트릭 설정"},
        {"idShort": "SystemSnapshot", "semanticId": "https://admin-shell.io/IDTA/02026/1/0/SystemSnapshot",
         "valueType": "SubmodelElementCollection", "multiplicity": "1", "description": "최신 상태 스냅샷"},
        {"idShort": "WorkStates", "semanticId": "https://admin-shell.io/IDTA/02026/1/0/WorkStates",
         "valueType": "Map<Guid,NodeState>", "multiplicity": "0..*", "description": "Work 별 R/G/F/H 현재 상태"},
        {"idShort": "CallStates", "semanticId": "https://admin-shell.io/IDTA/02026/1/0/CallStates",
         "valueType": "Map<Guid,NodeState>", "multiplicity": "0..*", "description": "Call 별 R/G/F/H 현재 상태"},
        {"idShort": "WorkProgress", "semanticId": "https://admin-shell.io/IDTA/02026/1/0/WorkProgress",
         "valueType": "Map<Guid,double>", "multiplicity": "0..*", "description": "Work 진행률 (0.0~1.0)"},
        {"idShort": "DeviceStates", "semanticId": "https://admin-shell.io/IDTA/02026/1/0/DeviceStates",
         "valueType": "Map<string,bool>", "multiplicity": "0..*", "description": "IO 태그 현재 값 (sensor/actuator)"},
        {"idShort": "OperationalEvents", "semanticId": "https://admin-shell.io/IDTA/02026/1/0/OperationalEvents",
         "valueType": "SubmodelElementList", "multiplicity": "0..*", "description": "운영 이벤트 시퀀스 (10 종)"},
        {"idShort": "PerformanceMetrics", "semanticId": "https://admin-shell.io/IDTA/02026/1/0/PerformanceMetrics",
         "valueType": "SubmodelElementCollection", "multiplicity": "1", "description": "MT/WT/TC + KPI 집계"},
        {"idShort": "MT_ms", "semanticId": "https://admin-shell.io/IDTA/02026/1/0/MT",
         "valueType": "Property:long", "multiplicity": "0..*", "description": "Moving Time — 실제 동작 시간 (ms)"},
        {"idShort": "WT_ms", "semanticId": "https://admin-shell.io/IDTA/02026/1/0/WT",
         "valueType": "Property:long", "multiplicity": "0..*", "description": "Wait Time — 대기 시간 (ms)"},
        {"idShort": "TC_ms", "semanticId": "https://admin-shell.io/IDTA/02026/1/0/TC",
         "valueType": "Property:long", "multiplicity": "0..*", "description": "Total Cycle = MT + WT (ms)"},
        {"idShort": "StateChangeHistory", "semanticId": "https://admin-shell.io/IDTA/02026/1/0/StateChangeHistory",
         "valueType": "SubmodelElementList", "multiplicity": "0..*", "description": "상태 전이 로그 (감사 추적용)"},
    ],

    "operationalEvents": [
        {"name": "StateChanged",
         "params": "(nodeType, nodeId, oldState, newState, ts, deviceName)",
         "useCase": "Work/Call 의 R→G→F→H 전이 감지. PostgreSQL: work_state, call 테이블."},
        {"name": "ProgressUpdated",
         "params": "(nodeType, nodeId, progress 0.0~1.0, ts, deviceName)",
         "useCase": "Work 진행률 갱신. PostgreSQL: signal_event.progress_rate."},
        {"name": "ProductionCycleStarted",
         "params": "(cycleNum, startTime, flowName)",
         "useCase": "Takt Time 측정 시작점. 한 cycle = Source Work R→F."},
        {"name": "ProductionCycleCompleted",
         "params": "(cycleNum, success, duration, completedWorks, yield)",
         "useCase": "사이클 완료 시 양품률·소요시간 박제."},
        {"name": "SystemStarted",
         "params": "(systemName, startTime, operatorId)",
         "useCase": "설비 가동 시작. 가동률(Availability) 분자 측정 시작."},
        {"name": "SystemStopped",
         "params": "(systemName, stopTime, totalCycles, reason)",
         "useCase": "정지 사유 기록 (정상/비상/고장)."},
        {"name": "IOValueChanged",
         "params": "(signal, ioType I/O, value, ts, deviceName)",
         "useCase": "센서/액추에이터 값 변화. PLC 태그(%IX/%QX) → DS Tag 매핑."},
        {"name": "TcUpdated",
         "params": "(signal, tcMs, ts)",
         "useCase": "실제 사이클타임 측정값. PostgreSQL: signal_event.tc."},
        {"name": "FlowMtWtUpdated",
         "params": "(flowName, mtMs, wtMs, ts)",
         "useCase": "Flow 단위 MT/WT 갱신 → flow.mt, flow.wt 테이블."},
        {"name": "WorkMtWtUpdated",
         "params": "(workGuid, workName, mtMs, wtMs, ts)",
         "useCase": "Work 단위 MT/WT 갱신 → work.mt, work.wt 테이블."},
        {"name": "AlarmOccurred",
         "params": "(alarmCode, severity, message, deviceName, ts)",
         "useCase": "알람 (설비 이상 / 품질 / 안전) 박제."},
    ],

    "submodelExample": {
        "title": "예제: 차체프레스 라인 1 cycle 모니터링 스냅샷",
        "description": "한 시점의 SystemSnapshot SMC 의 직렬화 — 6-Work 라인이 W2(Going) 진행 중일 때.",
        "json": """{
  "modelType": "Submodel",
  "idShort": "SequenceMonitoringSubmodel",
  "kind": "Instance",
  "semanticId": {
    "type": "ExternalReference",
    "keys": [{"type":"GlobalReference","value":"https://dualsoftdev.github.io/aas-semantics/sm/SequenceMonitoring/1/0"}]
  },
  "submodelElements": [
    {
      "idShort": "SystemSnapshot",
      "modelType": "SubmodelElementCollection",
      "value": [
        { "idShort": "Timestamp",  "modelType":"Property", "valueType":"xs:dateTime", "value":"2026-05-07T09:30:14Z" },
        { "idShort": "SystemName", "modelType":"Property", "valueType":"xs:string",   "value":"PressLine" },
        {
          "idShort": "WorkStates", "modelType":"SubmodelElementList",
          "value":[
            {"idShort":"W1_소재투입","modelType":"Property","valueType":"xs:string","value":"Finish"},
            {"idShort":"W2_1차프레스","modelType":"Property","valueType":"xs:string","value":"Going"},
            {"idShort":"W3_2차프레스","modelType":"Property","valueType":"xs:string","value":"Ready"},
            {"idShort":"W4_트림",    "modelType":"Property","valueType":"xs:string","value":"Ready"},
            {"idShort":"W5_검사",    "modelType":"Property","valueType":"xs:string","value":"Ready"},
            {"idShort":"W6_배출",    "modelType":"Property","valueType":"xs:string","value":"Homing"}
          ]
        },
        { "idShort":"AverageProgress","modelType":"Property","valueType":"xs:double","value":0.42 }
      ]
    },
    {
      "idShort": "OperationalEvents",
      "modelType": "SubmodelElementList",
      "value": [
        {"idShort":"e1","modelType":"SubmodelElementCollection","value":[
          {"idShort":"name","modelType":"Property","valueType":"xs:string","value":"StateChanged"},
          {"idShort":"workName","modelType":"Property","valueType":"xs:string","value":"PressLine.W2_1차프레스"},
          {"idShort":"old","modelType":"Property","valueType":"xs:string","value":"Ready"},
          {"idShort":"new","modelType":"Property","valueType":"xs:string","value":"Going"},
          {"idShort":"ts","modelType":"Property","valueType":"xs:dateTime","value":"2026-05-07T09:30:14.120Z"}
        ]}
      ]
    }
  ]
}""",
    },

    "relationships": [
        ("SeqMonSm.WorkStates[*]",  "→ Work (R/G/F/H 추적 대상)", "entity/Work/1/0"),
        ("SeqMonSm.CallStates[*]",  "→ Call",                       "entity/Call/1/0"),
        ("SeqMonSm.DeviceStates[*]", "→ Device IO 태그",             "entity/Device/1/0"),
        ("SeqMonSm → sim/Kpi/*",    "박제 데이터로 KPI 산출",        "sim/Kpi/OEE/1/0"),
    ],

    "industryStandards": [
        {"name": "IDTA 02026-1-0", "scope": "SequenceMonitoring 표준 (Draft)",
         "url": "https://industrialdigitaltwin.org/en/content-hub/submodels"},
        {"name": "ISO 22400-2:2014", "scope": "MES KPI 정의 (가동률, OEE 등)",
         "url": "https://www.iso.org/standard/56847.html"},
        {"name": "ISA-95 (IEC 62264)", "scope": "Level 3 Operations Management"},
        {"name": "OPC UA Part 8", "scope": "DataAccess (실시간 IO 값 송수신)"},
    ],

    "relatedCds": [
        ("sm/SequenceModel/1/0",      "SeqModelSm",  "모니터링 대상 시퀀스 모델"),
        ("sm/SequenceLogging/1/0",    "SeqLogSm",    "장기 보존 로깅 (모니터링 vs 로깅 분리)"),
        ("sm/SequenceMaintenance/1/0","SeqMaintSm",  "정비 (MTBF/MTTR 산출 기반)"),
        ("sim/Kpi/OEE/1/0",           "OEEkpi",      "Availability × Performance × Quality"),
        ("sim/Kpi/CycleTime/1/0",     "CTkpi",       "Work TC 박제 KPI"),
        ("entity/Work/1/0",           "Work",         "추적 대상 — R/G/F/H FSM"),
    ],

    "appendixLinks": [
        ("duality", "Duality 8 Cases", "Case 5: WorkBit = R⊕G⊕F⊕H FSM 의미 — 모니터링 대상"),
    ],

    "aasMapping": (
        "SeqMonSm 은 한 AAS 안에 1 개 인스턴스. 실시간 메트릭은 PerformanceMetrics SMC 에 누적, "
        "장기 보존이 필요한 부분은 SequenceLogging 으로 분리 저장. SimulationResult 박제 시 "
        "관련 KPI 는 sim/Kpi/* CD 의 semanticId 로 인용."
    ),

    "sourceFiles": [
        ("https://github.com/DualsoftDev/ds2/blob/master/Solutions/Convert/Ds2.Aasx/Concepts/Catalog.fs", "Catalog.fs (CD 카탈로그)"),
        ("https://github.com/DualsoftDev/ds2/blob/master/Solutions/Runtime/Ev2.Runtime.Sim", "Ev2.Runtime.Sim (이벤트 발행자)"),
    ],
}


# ── sim/Kpi/OEE/1/0 — Overall Equipment Effectiveness ─────────────────────
ENTITY_DETAILS["sim/Kpi/OEE/1/0"] = {
    "fsharpType": """// Ds2.Core/SequenceSubmodels/01_Simulation.fs
type KpiOeeItem() =
    member val ResourceName              = "" with get, set
    member val CalculationDate           = DateTime.MinValue with get, set
    member val CalculationPeriod_s       = 0.0 with get, set
    member val Availability              = 0.0 with get, set
    member val Performance               = 0.0 with get, set
    member val Quality                   = 0.0 with get, set
    member val OEE                       = 0.0 with get, set
    member val PlannedOperatingTime_s    = 0.0 with get, set
    member val ActualOperatingTime_s     = 0.0 with get, set
    member val PlannedProductionQty      = 0 with get, set
    member val ActualProductionQty       = 0 with get, set
    member val GoodProductQty            = 0 with get, set
    member val DefectQty                 = 0 with get, set
    member val TimeLoss_pct              = 0.0 with get, set
    member val SpeedLoss_pct             = 0.0 with get, set
    member val QualityLoss_pct           = 0.0 with get, set
    member val TargetOEE                 = 0.0 with get, set
    member val OeeGap                    = 0.0 with get, set
    member val OeeClass                  = "" with get, set""",

    "kpiFormula": {
        "expr": "OEE = Availability × Performance × Quality",
        "source": "ISO 22400-2:2014 (Manufacturing operations management — KPIs Part 2)",
        "components": [
            {"symbol": "Availability (가동률)",
             "formula": "Run Time ÷ Planned Production Time",
             "description": "정지·고장 시간 제외한 실제 가동 비율"},
            {"symbol": "Performance (성능률)",
             "formula": "(Ideal CT × Total Units) ÷ Run Time",
             "description": "이상 사이클타임 대비 실제 처리속도"},
            {"symbol": "Quality (양품률)",
             "formula": "Good Units ÷ Total Units",
             "description": "재작업/폐기 제외 양품 비율"},
        ],
        "example": {
            "scenario": "PressLine 1 시프트 (8h) — 도금 라인 평일 야간 운영",
            "inputs": [
                "PlannedTimeMs = 28,800,000 (8h)",
                "RunTimeMs = 26,496,000 (3분 공구교체 + 휴식 제외)",
                "IdealCtMs = 4,300 / ActualCtMs avg = 5,058",
                "GoodUnits = 4,725 / TotalUnits = 4,821",
            ],
            "calc": "Availability=0.92 · Performance=0.85 · Quality=0.98",
            "result": "OEE = 0.92 × 0.85 × 0.98 = 0.7676 (76.76%)",
        },
    },

    "submodelExample": {
        "title": "sim/Kpi/OEE 박제 위치 — SequenceSimulation/SystemProperties/SimulationResult/KPI_OEE",
        "description": "Promaker 가 시뮬 또는 실가동 데이터를 박제할 때 ds2 export 가 생성하는 OEE 그룹 형태.",
        "json": """{
  "idShort": "KPI_OEE",
  "modelType": "SubmodelElementList",
  "semanticId": {
    "type": "ExternalReference",
    "keys": [{"type":"GlobalReference","value":"https://dualsoftdev.github.io/aas-semantics/sim/Kpi/OEE/1/0"}]
  },
  "value": [
    { "idShort":"OeeItem", "modelType":"SubmodelElementCollection", "value":[
      { "idShort":"ResourceName",           "modelType":"Property","valueType":"xs:string","value":"PressLine" },
      { "idShort":"CalculationDate",        "modelType":"Property","valueType":"xs:dateTime","value":"2026-05-07T09:30:14Z" },
      { "idShort":"CalculationPeriod_s",    "modelType":"Property","valueType":"xs:double","value":28800 },
      { "idShort":"Availability",           "modelType":"Property","valueType":"xs:double","value":0.92 },
      { "idShort":"Performance",            "modelType":"Property","valueType":"xs:double","value":0.85 },
      { "idShort":"Quality",                "modelType":"Property","valueType":"xs:double","value":0.98 },
      { "idShort":"OEE",                    "modelType":"Property","valueType":"xs:double","value":0.7676 },
      { "idShort":"PlannedOperatingTime_s", "modelType":"Property","valueType":"xs:double","value":28800 },
      { "idShort":"ActualOperatingTime_s",  "modelType":"Property","valueType":"xs:double","value":26496 },
      { "idShort":"GoodProductQty",         "modelType":"Property","valueType":"xs:int",   "value":4725 },
      { "idShort":"DefectQty",              "modelType":"Property","valueType":"xs:int",   "value":96 }
    ]}
  ]
}""",
    },

    "relationships": [
        ("KPI_OEE ⊂ SimulationResult", "← SequenceSimulation/SystemProperties 하위", "sim/Result/1/0"),
        ("OEEkpi ← sm/SequenceMonitoring", "← 모니터링 데이터로 산출",        "sm/SequenceMonitoring/1/0"),
        ("Performance ← Cycle Time",   "→ 이상/실제 CT 비교",                "sim/Kpi/CycleTime/1/0"),
    ],

    "industryStandards": [
        {"name": "ISO 22400-2:2014", "scope": "OEE 정의 단일 진실 원천",
         "url": "https://www.iso.org/standard/56847.html"},
        {"name": "VDMA 66412-1", "scope": "OEE 산업 가이드라인"},
        {"name": "ISA-95 (IEC 62264)", "scope": "MES KPI 모델"},
        {"name": "World Class OEE", "scope": "벤치마크 ≥ 85% (이산제조)"},
    ],

    "relatedCds": [
        ("sim/Result/1/0",                "SimResult",  "OEE 가 박제되는 컨테이너"),
        ("sim/Kpi/CycleTime/1/0",         "CTkpi",      "Performance 분자 (Ideal CT) / 분모 (Actual CT)"),
        ("sim/Kpi/Throughput/1/0",        "TPkpi",      "Capacity 와 함께 처리 능력 표현"),
        ("sim/Kpi/ResourceUtilization/1/0","RUkpi",     "Availability 의 보조 지표"),
        ("sm/SequenceMonitoring/1/0",     "SeqMonSm",   "OEE 산출의 원천 데이터"),
        ("sm/SequenceQuality/1/0",        "SeqQualSm",  "Quality 분자 (양품 수) 원천"),
    ],

    "appendixLinks": [
        ("duality", "Duality 8 Cases", "Case 6 (φ(θ) 위상) 으로 디지털 트윈 ↔ 실설비 동기화 판단"),
    ],

    "aasMapping": (
        "OEEkpi CD 는 SequenceSimulation/SystemProperties/SimulationResult/KPI_OEE 에 semanticId 로 붙는다. "
        "ds2 v2026 이전엔 TechnicalData(IDTA 02003) 안에 있었으나 표준 SM 분리 정책에 따라 이전됨."
    ),

    "sourceFiles": [
        ("https://github.com/DualsoftDev/ds2/blob/master/Solutions/Convert/Ds2.Aasx/Concepts/Catalog.fs",
         "Catalog.fs (simulationConceptDescriptionInfos)"),
    ],
}


def get(path: str):
    return ENTITY_DETAILS.get(path)
