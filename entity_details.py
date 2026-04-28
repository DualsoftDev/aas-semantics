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
            ("TechnicalData",         "TechnicalData option",       "None",               "TechnicalData (Skip)",    "별도 SM (IDTA 02003) 으로 직렬화"),
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
        "aasMapping": "Project.* 필드는 SequenceModel 서브모델 안의 'Project' SubmodelElementCollection 에 매핑. Nameplate / HandoverDocumentation / TechnicalData 는 별도 서브모델로 분리.",
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
            ("Flow → ArrowWork[*]", "Work 간 전이 컨테이너", "entity/ArrowWork/1/0"),
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
            ("ArrowWork.ParentId", "→ DsSystem (Flow 의 부모) — 또는 Flow ID 형태로도 사용", "entity/System/1/0"),
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
    parentId  = mainFlow.Id,
    sourceId  = w1.Id,
    targetId  = w2.Id,
    arrowType = ArrowType.StartReset)""",
        "aasMapping": "ArrowWork 는 Flow SMC 하위 Arrows SML 안 SMC 로 export.",
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


def get(path: str):
    return ENTITY_DETAILS.get(path)
