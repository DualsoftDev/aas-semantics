"""
Entity 별 상세 다이어그램 (전문가급) — overview 다이어그램 아래 표시.
UML 컨벤션 + 정보 밀도 높은 기술 도식.

각 엔티티의 핵심 측면:
  · Project       — Submodel 트리 + ID 체계 + 메타데이터
  · System        — Active 시스템 아키텍처 (Flow ⊕ Devices ⊕ APIs)
  · Device        — API 시그니처 + IO Tag 매핑 표
  · Flow          — Work 토큰 흐름 (Source → Sink 다이어그램)
  · Work          — R/G/F/H 상태머신 (UML state diagram)
  · Call          — Call 실행 + Condition + ApiCalls
  · ApiDef        — Function signature + ActionType 4종 + Tx/Rx
  · ApiCall       — Caller↔Callee 런타임 바인딩 + PLC 태그
  · TokenSpec     — 토큰 정의 + Multi-token Flow lanes
  · ArrowWork     — 5종 ArrowType 비교 (Start/Reset/StartReset/ResetReset/Group)
  · ArrowCall     — Call 직렬/병렬 실행 패턴
"""

# 공통 SVG 헤더 — 라이트톤, 전문가 도식
_DEFS = """
<defs>
  <!-- State machine gradients -->
  <radialGradient id="grad-r" cx="0.35" cy="0.35" r="0.7">
    <stop offset="0" stop-color="#3fb950"/>
    <stop offset="1" stop-color="#116329"/>
  </radialGradient>
  <radialGradient id="grad-g" cx="0.35" cy="0.35" r="0.7">
    <stop offset="0" stop-color="#fb8500"/>
    <stop offset="1" stop-color="#a04100"/>
  </radialGradient>
  <radialGradient id="grad-f" cx="0.35" cy="0.35" r="0.7">
    <stop offset="0" stop-color="#54aeff"/>
    <stop offset="1" stop-color="#0550ae"/>
  </radialGradient>
  <radialGradient id="grad-h" cx="0.35" cy="0.35" r="0.7">
    <stop offset="0" stop-color="#a4adb8"/>
    <stop offset="1" stop-color="#4f5660"/>
  </radialGradient>

  <!-- Card gradients -->
  <linearGradient id="card-blue" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#ddf4ff"/>
    <stop offset="1" stop-color="#b6e3ff"/>
  </linearGradient>
  <linearGradient id="card-green" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#dafbe1"/>
    <stop offset="1" stop-color="#aceebb"/>
  </linearGradient>
  <linearGradient id="card-amber" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#fff8c5"/>
    <stop offset="1" stop-color="#f7e07a"/>
  </linearGradient>
  <linearGradient id="card-purple" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#fbefff"/>
    <stop offset="1" stop-color="#ecd5ff"/>
  </linearGradient>
  <linearGradient id="card-red" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#ffebe9"/>
    <stop offset="1" stop-color="#ffcecb"/>
  </linearGradient>

  <!-- Drop shadow -->
  <filter id="dshadow" x="-10%" y="-10%" width="120%" height="120%">
    <feDropShadow dx="0" dy="2" stdDeviation="2.5" flood-color="rgba(15,30,60,0.18)"/>
  </filter>
  <filter id="dshadow-strong" x="-10%" y="-10%" width="120%" height="120%">
    <feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="rgba(15,30,60,0.25)"/>
  </filter>

  <!-- Arrow markers -->
  <marker id="m-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
    <path d="M0,0 L10,5 L0,10 z" fill="#0969da"/>
  </marker>
  <marker id="m-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
    <path d="M0,0 L10,5 L0,10 z" fill="#1a7f37"/>
  </marker>
  <marker id="m-orange" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
    <path d="M0,0 L10,5 L0,10 z" fill="#bc4c00"/>
  </marker>
  <marker id="m-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
    <path d="M0,0 L10,5 L0,10 z" fill="#cf222e"/>
  </marker>
  <marker id="m-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
    <path d="M0,0 L10,5 L0,10 z" fill="#7c3aed"/>
  </marker>
  <marker id="m-gray" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
    <path d="M0,0 L10,5 L0,10 z" fill="#656d76"/>
  </marker>

  <!-- Common text styles -->
  <style>
    .d-title    { font: 700 18px Inter, 'Segoe UI', system-ui, sans-serif; fill: #0550ae; }
    .d-subtitle { font: italic 12px Inter, 'Segoe UI', system-ui, sans-serif; fill: #656d76; }
    .d-section  { font: 700 13px Inter, 'Segoe UI', system-ui, sans-serif; fill: #1f2328; }
    .d-label    { font: 600 13px Inter, 'Segoe UI', system-ui, sans-serif; fill: #1f2328; }
    .d-text     { font: 12px Inter, 'Segoe UI', system-ui, sans-serif; fill: #1f2328; }
    .d-meta     { font: 11px Inter, 'Segoe UI', system-ui, sans-serif; fill: #656d76; }
    .d-tiny     { font: 10px Inter, 'Segoe UI', system-ui, sans-serif; fill: #656d76; }
    .d-mono     { font: 11px ui-monospace, 'SF Mono', Consolas, monospace; fill: #6f42c1; }
    .d-mono-key { font: 600 11px ui-monospace, 'SF Mono', Consolas, monospace; fill: #0550ae; }
    .d-state-name { font: 700 32px Inter, system-ui, sans-serif; fill: #fff; text-anchor: middle; }
    .d-state-sub  { font: 600 10px Inter, system-ui, sans-serif; fill: rgba(255,255,255,0.95); text-anchor: middle; }
    .d-cond     { font: 600 11px Inter, system-ui, sans-serif; fill: #1f2328; text-anchor: middle; }
  </style>
</defs>
"""


def _svg(viewbox: str, body: str) -> str:
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}">{_DEFS}{body}</svg>'


# ══════════════════════════════════════════════════════════════════════════════
# PROJECT — Submodel/Entity Tree
# ══════════════════════════════════════════════════════════════════════════════
_PROJECT = _svg("0 0 960 460", """
  <rect width="960" height="460" fill="#fdfdff"/>
  <text x="36" y="38" class="d-title">📦 Project — DS 모델 루트 컨테이너</text>
  <text x="36" y="58" class="d-subtitle">DsEntity 루트 · 모든 시스템·디바이스·토큰 사양을 보유</text>

  <!-- Project root card -->
  <rect x="36" y="80" width="270" height="350" rx="8" fill="url(#card-purple)" stroke="#7c3aed" stroke-width="2" filter="url(#dshadow)"/>
  <text x="52" y="106" class="d-section" fill="#7c3aed">Project (root)</text>

  <!-- Metadata section -->
  <rect x="48" y="118" width="246" height="92" rx="4" fill="#fff" stroke="#d0d7de"/>
  <text x="58" y="135" class="d-meta" font-weight="700">METADATA</text>
  <text x="58" y="153" class="d-text"><tspan class="d-mono-key">name</tspan>: "MyFactory"</text>
  <text x="58" y="170" class="d-text"><tspan class="d-mono-key">author</tspan>: "ahn@dualsoft.com"</text>
  <text x="58" y="187" class="d-text"><tspan class="d-mono-key">version</tspan>: "1.2.0"</text>
  <text x="58" y="204" class="d-text"><tspan class="d-mono-key">dateTime</tspan>: 2026-04-29T00:00</text>

  <!-- ID lists -->
  <rect x="48" y="220" width="246" height="64" rx="4" fill="#fff" stroke="#d0d7de"/>
  <text x="58" y="237" class="d-meta" font-weight="700">ENTITY ID 컬렉션</text>
  <text x="58" y="255" class="d-text"><tspan class="d-mono-key">activeSystemIds</tspan>[*] → DsSystem</text>
  <text x="58" y="272" class="d-text"><tspan class="d-mono-key">passiveSystemIds</tspan>[*] → Device</text>

  <!-- TokenSpecs -->
  <rect x="48" y="294" width="246" height="60" rx="4" fill="#ffeaea" stroke="#cf222e"/>
  <text x="58" y="312" class="d-meta" font-weight="700" fill="#cf222e">tokenSpecs[*]</text>
  <text x="58" y="330" class="d-text">#1 RecipeA "Steel Door"</text>
  <text x="58" y="347" class="d-text">#2 RecipeB "Aluminum Panel"</text>

  <!-- IDTA std submodels (skip flag) -->
  <rect x="48" y="364" width="246" height="56" rx="4" fill="#f6f8fa" stroke="#d0d7de" stroke-dasharray="3 2"/>
  <text x="58" y="381" class="d-meta" font-weight="700">IDTA 표준 SM (별도 SM 으로 직렬화)</text>
  <text x="58" y="397" class="d-tiny">Nameplate · HandoverDocumentation</text>
  <text x="58" y="412" class="d-tiny">TechnicalData (시뮬결과는 SeqSim 으로 이전)</text>

  <!-- Active Systems -->
  <line x1="306" y1="180" x2="386" y2="140" stroke="#1a7f37" stroke-width="2" marker-end="url(#m-green)"/>
  <text x="320" y="156" class="d-tiny">activeSystemIds</text>
  <rect x="386" y="92" width="248" height="120" rx="6" fill="url(#card-green)" stroke="#1a7f37" stroke-width="2" filter="url(#dshadow)"/>
  <text x="404" y="114" class="d-section" fill="#1a7f37">⚙ Active Systems</text>
  <text x="404" y="134" class="d-meta">제어 흐름을 주도 — Flow 보유</text>
  <rect x="404" y="144" width="100" height="28" rx="4" fill="#fff" stroke="#1a7f37"/>
  <text x="416" y="163" class="d-label" fill="#1a7f37">Cell-A</text>
  <rect x="514" y="144" width="100" height="28" rx="4" fill="#fff" stroke="#1a7f37"/>
  <text x="526" y="163" class="d-label" fill="#1a7f37">Cell-B</text>
  <text x="404" y="195" class="d-mono">DsSystem (Active role)</text>

  <!-- Passive Systems -->
  <line x1="306" y1="220" x2="386" y2="240" stroke="#9a6700" stroke-width="2" marker-end="url(#m-orange)"/>
  <text x="316" y="232" class="d-tiny">passiveSystemIds</text>
  <rect x="386" y="234" width="248" height="120" rx="6" fill="url(#card-amber)" stroke="#9a6700" stroke-width="2" filter="url(#dshadow)"/>
  <text x="404" y="256" class="d-section" fill="#9a6700">🔧 Passive Devices</text>
  <text x="404" y="276" class="d-meta">Active 가 호출 — APIs 노출</text>
  <rect x="404" y="284" width="68" height="24" rx="4" fill="#fff" stroke="#9a6700"/>
  <text x="412" y="301" class="d-text" fill="#9a6700">Cylinder1</text>
  <rect x="478" y="284" width="68" height="24" rx="4" fill="#fff" stroke="#9a6700"/>
  <text x="492" y="301" class="d-text" fill="#9a6700">Robot1</text>
  <rect x="552" y="284" width="76" height="24" rx="4" fill="#fff" stroke="#9a6700"/>
  <text x="568" y="301" class="d-text" fill="#9a6700">Sensor1</text>
  <text x="404" y="335" class="d-mono">DsSystem (Passive role)</text>

  <!-- AAS Output -->
  <rect x="660" y="92" width="270" height="262" rx="6" fill="url(#card-blue)" stroke="#0969da" stroke-width="2" filter="url(#dshadow)"/>
  <text x="678" y="114" class="d-section" fill="#0550ae">📂 AAS Export</text>
  <text x="678" y="132" class="d-meta">Promaker → AASX 패키징</text>
  <line x1="678" y1="142" x2="912" y2="142" stroke="#0969da" stroke-width="0.5" stroke-dasharray="3 2"/>

  <text x="678" y="160" class="d-mono-key">SequenceModel</text>
  <text x="678" y="174" class="d-tiny">→ Project · Systems · Flows · Works · Calls</text>

  <text x="678" y="194" class="d-mono-key">SequenceSimulation</text>
  <text x="678" y="208" class="d-tiny">→ SystemProperties/SimulationResult + KPIs</text>

  <text x="678" y="228" class="d-mono-key">SequenceMonitoring · Logging</text>
  <text x="678" y="242" class="d-tiny">→ Runtime state · Events</text>

  <text x="678" y="262" class="d-mono-key">SequenceMaintenance · HMI · Quality · Cost</text>
  <text x="678" y="276" class="d-tiny">→ 도메인 별 전용 SM</text>

  <line x1="678" y1="288" x2="912" y2="288" stroke="#0969da" stroke-width="0.5" stroke-dasharray="3 2"/>
  <text x="678" y="306" class="d-mono-key" fill="#7c3aed">IDTA 표준 SM (외부 템플릿)</text>
  <text x="678" y="320" class="d-tiny">Nameplate · HD · TechnicalData</text>
  <text x="678" y="338" class="d-tiny" font-style="italic">★ ds2 v2026: 시뮬결과는 SeqSim 으로 이동</text>

  <!-- Footer -->
  <text x="36" y="450" class="d-tiny">★ ID 체인: Project.activeSystemIds[i] → DsSystem.id (referential integrity)</text>
""")


# ══════════════════════════════════════════════════════════════════════════════
# SYSTEM — Active System Architecture
# ══════════════════════════════════════════════════════════════════════════════
_SYSTEM = _svg("0 0 960 480", """
  <rect width="960" height="480" fill="#fdfdff"/>
  <text x="36" y="38" class="d-title">⚙ DsSystem (Active) — 제어 시스템 아키텍처</text>
  <text x="36" y="58" class="d-subtitle">Active = activeSystemIds 등록 · Flow 보유 · 다른 시스템의 ApiDef 호출</text>

  <!-- Outer Active System box -->
  <rect x="36" y="80" width="888" height="320" rx="10" fill="url(#card-green)" stroke="#1a7f37" stroke-width="2.5" filter="url(#dshadow)"/>
  <text x="60" y="110" class="d-section" fill="#1a7f37" font-size="16">DsSystem "Cell-A"</text>
  <text x="60" y="130" class="d-mono">id · name · systemType="AssemblyCell" · IRI · properties[*]</text>

  <!-- Flow container -->
  <rect x="60" y="148" width="540" height="128" rx="6" fill="#fff" stroke="#0969da" stroke-width="2"/>
  <text x="76" y="170" class="d-section" fill="#0550ae">Flow "MainFlow"</text>
  <text x="76" y="186" class="d-tiny">parentId = Cell-A.id · 직렬 Work 시퀀스</text>

  <!-- Works in flow -->
  <g>
    <rect x="80"  y="198" width="100" height="62" rx="4" fill="url(#card-blue)" stroke="#0969da"/>
    <text x="96" y="218" class="d-label" fill="#0550ae">W₁ Pickup</text>
    <text x="96" y="236" class="d-tiny">Source · 12.5s</text>
    <circle cx="92" cy="248" r="4" fill="#cf222e"/>
    <text x="100" y="252" class="d-tiny" fill="#cf222e">token</text>

    <rect x="200" y="198" width="100" height="62" rx="4" fill="url(#card-blue)" stroke="#0969da"/>
    <text x="216" y="218" class="d-label" fill="#0550ae">W₂ Process</text>
    <text x="216" y="236" class="d-tiny">duration: 8.0s</text>

    <rect x="320" y="198" width="100" height="62" rx="4" fill="url(#card-blue)" stroke="#0969da"/>
    <text x="336" y="218" class="d-label" fill="#0550ae">W₃ Place</text>
    <text x="336" y="236" class="d-tiny">duration: 6.0s</text>

    <rect x="440" y="198" width="140" height="62" rx="4" fill="url(#card-blue)" stroke="#0969da"/>
    <text x="456" y="218" class="d-label" fill="#0550ae">W₄ Reset (Sink)</text>
    <text x="456" y="236" class="d-tiny">tokenRole: Sink</text>

    <line x1="180" y1="229" x2="200" y2="229" stroke="#1a7f37" stroke-width="2" marker-end="url(#m-green)"/>
    <line x1="300" y1="229" x2="320" y2="229" stroke="#1a7f37" stroke-width="2" marker-end="url(#m-green)"/>
    <line x1="420" y1="229" x2="440" y2="229" stroke="#1a7f37" stroke-width="2" marker-end="url(#m-green)"/>
  </g>

  <!-- Devices used (right side) -->
  <rect x="620" y="148" width="304" height="232" rx="6" fill="url(#card-amber)" stroke="#9a6700" stroke-width="2"/>
  <text x="638" y="170" class="d-section" fill="#9a6700">참조 Devices (passiveSystemIds)</text>
  <text x="638" y="186" class="d-tiny">호출되는 외부 시스템 — Calls 가 ApiDef 호출</text>

  <rect x="638" y="200" width="270" height="34" rx="4" fill="#fff" stroke="#9a6700"/>
  <text x="650" y="222" class="d-text" fill="#9a6700"><tspan font-weight="700">Cylinder1</tspan> · ADV/RET/DETECT/HOME</text>

  <rect x="638" y="240" width="270" height="34" rx="4" fill="#fff" stroke="#9a6700"/>
  <text x="650" y="262" class="d-text" fill="#9a6700"><tspan font-weight="700">Robot1</tspan> · MOVE_TO_*/GRAB/RELEASE</text>

  <rect x="638" y="280" width="270" height="34" rx="4" fill="#fff" stroke="#9a6700"/>
  <text x="650" y="302" class="d-text" fill="#9a6700"><tspan font-weight="700">Sensor1</tspan> · READ/CALIBRATE</text>

  <rect x="638" y="320" width="270" height="34" rx="4" fill="#fff" stroke="#9a6700"/>
  <text x="650" y="342" class="d-text" fill="#9a6700"><tspan font-weight="700">Conveyor1</tspan> · START/STOP/SPEED</text>

  <!-- Connection arrow (Calls in MainFlow → Devices) - 보라 점선 = ApiCall binding (라벨은 footer 에서 설명) -->
  <path d="M 580 229 Q 605 230 638 230" stroke="#7c3aed" stroke-width="1.5" stroke-dasharray="4 3" fill="none" marker-end="url(#m-purple)"/>

  <!-- Properties -->
  <rect x="60" y="290" width="540" height="86" rx="6" fill="#fff" stroke="#d0d7de"/>
  <text x="76" y="310" class="d-section">SystemSubmodelProperty[*] (도메인별)</text>
  <rect x="76" y="320" width="116" height="48" rx="3" fill="#f6f8fa" stroke="#d0d7de"/>
  <text x="86" y="338" class="d-mono-key">Sim</text>
  <text x="86" y="354" class="d-tiny">cycleTime · OEE</text>
  <rect x="200" y="320" width="116" height="48" rx="3" fill="#f6f8fa" stroke="#d0d7de"/>
  <text x="210" y="338" class="d-mono-key">Ctrl</text>
  <text x="210" y="354" class="d-tiny">FBTagMap · IO config</text>
  <rect x="324" y="320" width="116" height="48" rx="3" fill="#f6f8fa" stroke="#d0d7de"/>
  <text x="334" y="338" class="d-mono-key">Mon</text>
  <text x="334" y="354" class="d-tiny">alarms · trends</text>
  <rect x="448" y="320" width="140" height="48" rx="3" fill="#f6f8fa" stroke="#d0d7de"/>
  <text x="458" y="338" class="d-mono-key">Maint · HMI · Qual</text>
  <text x="458" y="354" class="d-tiny">domain-specific</text>

  <!-- Bottom note -->
  <text x="36" y="405" class="d-meta"><tspan fill="#7c3aed" font-style="italic">보라 점선 화살표</tspan> = ApiCall binding (Active 의 Call/ApiCall 이 Passive 의 ApiDef 호출)</text>
  <text x="36" y="425" class="d-section">★ Active vs Passive 결정자: Project.activeSystemIds vs passiveSystemIds 등록 여부</text>
  <text x="36" y="445" class="d-meta">동일 DsSystem 타입. 같은 시스템도 호출 방향에 따라 동적 역할 전환 가능 (Duality Case 1)</text>
  <text x="36" y="465" class="d-meta">F# type: <tspan class="d-mono">type DsSystem [&lt;JsonConstructor&gt;] internal (name) = inherit DsEntity(name)</tspan></text>
""")


# ══════════════════════════════════════════════════════════════════════════════
# DEVICE — API Contract + I/O Tag mapping
# ══════════════════════════════════════════════════════════════════════════════
_DEVICE = _svg("0 0 960 500", """
  <rect width="960" height="500" fill="#fdfdff"/>
  <text x="36" y="38" class="d-title">🔧 Device (Passive DsSystem) — API 계약 + I/O Tag 매핑</text>
  <text x="36" y="58" class="d-subtitle">Active 가 호출하는 시스템 — ApiDefs 노출 + IOTags 로 PLC 주소 바인딩</text>

  <!-- Device header -->
  <rect x="36" y="80" width="888" height="60" rx="6" fill="url(#card-amber)" stroke="#9a6700" stroke-width="2" filter="url(#dshadow)"/>
  <text x="60" y="106" class="d-section" fill="#9a6700" font-size="16">Device "Cylinder1" (passive)</text>
  <text x="60" y="125" class="d-mono">SystemType="Cylinder_2" · IRI="https://factory.example.com/devices/cyl-1" · Make: Festo</text>

  <!-- Section: Exposed APIs -->
  <text x="36" y="172" class="d-section">노출 APIs (apiDefs[*]) — 외부 시스템이 호출 가능한 메서드</text>
  <line x1="36" y1="180" x2="924" y2="180" stroke="#d0d7de"/>

  <g transform="translate(36, 192)">
    <!-- ADV -->
    <rect x="0" y="0" width="210" height="86" rx="6" fill="#fff" stroke="#9a6700" stroke-width="1.5" filter="url(#dshadow)"/>
    <polygon points="0,12 -16,30 0,48 0,12" fill="url(#card-amber)" stroke="#9a6700" stroke-width="1.5"/>
    <text x="14" y="22" class="d-label" fill="#9a6700">ADV</text>
    <text x="14" y="40" class="d-tiny">Advance / 전진</text>
    <text x="14" y="58" class="d-mono">action: <tspan fill="#0550ae">Pulse</tspan></text>
    <text x="14" y="74" class="d-mono">timeout: 2000ms</text>

    <!-- RET -->
    <rect x="226" y="0" width="210" height="86" rx="6" fill="#fff" stroke="#9a6700" stroke-width="1.5" filter="url(#dshadow)"/>
    <polygon points="226,12 210,30 226,48 226,12" fill="url(#card-amber)" stroke="#9a6700" stroke-width="1.5"/>
    <text x="240" y="22" class="d-label" fill="#9a6700">RET</text>
    <text x="240" y="40" class="d-tiny">Retract / 후진</text>
    <text x="240" y="58" class="d-mono">action: <tspan fill="#0550ae">Pulse</tspan></text>
    <text x="240" y="74" class="d-mono">timeout: 2000ms</text>

    <!-- DETECT -->
    <rect x="452" y="0" width="210" height="86" rx="6" fill="#fff" stroke="#9a6700" stroke-width="1.5" filter="url(#dshadow)"/>
    <polygon points="452,12 436,30 452,48 452,12" fill="url(#card-amber)" stroke="#9a6700" stroke-width="1.5"/>
    <text x="466" y="22" class="d-label" fill="#9a6700">DETECT</text>
    <text x="466" y="40" class="d-tiny">Sense object / 감지</text>
    <text x="466" y="58" class="d-mono">action: <tspan fill="#0550ae">Normal</tspan></text>
    <text x="466" y="74" class="d-mono">→ BOOL result</text>

    <!-- HOME -->
    <rect x="678" y="0" width="210" height="86" rx="6" fill="#fff" stroke="#9a6700" stroke-width="1.5" filter="url(#dshadow)"/>
    <polygon points="678,12 662,30 678,48 678,12" fill="url(#card-amber)" stroke="#9a6700" stroke-width="1.5"/>
    <text x="692" y="22" class="d-label" fill="#9a6700">HOME</text>
    <text x="692" y="40" class="d-tiny">Reset to home / 원점</text>
    <text x="692" y="58" class="d-mono">action: <tspan fill="#0550ae">Time(3000)</tspan></text>
    <text x="692" y="74" class="d-mono">3s 후 자동 완료</text>
  </g>

  <!-- Section: I/O Tag Table -->
  <text x="36" y="316" class="d-section">I/O Tags — Semantic ⊕ PhysicalBinding (Duality Case 7)</text>
  <line x1="36" y1="324" x2="924" y2="324" stroke="#d0d7de"/>

  <!-- Table header -->
  <rect x="36" y="334" width="888" height="28" rx="4" fill="#f6f8fa" stroke="#d0d7de"/>
  <text x="50" y="352" class="d-meta" font-weight="700">SEMANTIC NAME</text>
  <text x="200" y="352" class="d-meta" font-weight="700">DIRECTION</text>
  <text x="320" y="352" class="d-meta" font-weight="700">PLC ADDRESS</text>
  <text x="500" y="352" class="d-meta" font-weight="700">DATA TYPE</text>
  <text x="610" y="352" class="d-meta" font-weight="700">USED BY API</text>
  <text x="780" y="352" class="d-meta" font-weight="700">ROLE</text>

  <!-- Rows -->
  <g font-family="ui-monospace, Consolas, monospace" font-size="11">
    <rect x="36" y="362" width="888" height="24" fill="#fff" stroke="#d0d7de" stroke-width="0.5"/>
    <text x="50" y="378" fill="#0550ae" font-weight="600">LS_Adv1</text>
    <text x="200" y="378" fill="#1a7f37">Input ▶</text>
    <text x="320" y="378" fill="#1f2328">%IX0.0</text>
    <text x="500" y="378" fill="#cf222e">BOOL</text>
    <text x="610" y="378" fill="#0550ae">ADV</text>
    <text x="780" y="378" fill="#656d76">limit switch (전진완)</text>

    <rect x="36" y="386" width="888" height="24" fill="#f6f8fa" stroke="#d0d7de" stroke-width="0.5"/>
    <text x="50" y="402" fill="#0550ae" font-weight="600">LS_Ret1</text>
    <text x="200" y="402" fill="#1a7f37">Input ▶</text>
    <text x="320" y="402" fill="#1f2328">%IX0.1</text>
    <text x="500" y="402" fill="#cf222e">BOOL</text>
    <text x="610" y="402" fill="#0550ae">RET</text>
    <text x="780" y="402" fill="#656d76">limit switch (후진완)</text>

    <rect x="36" y="410" width="888" height="24" fill="#fff" stroke="#d0d7de" stroke-width="0.5"/>
    <text x="50" y="426" fill="#0550ae" font-weight="600">SOL_Adv</text>
    <text x="200" y="426" fill="#bc4c00">Output ◀</text>
    <text x="320" y="426" fill="#1f2328">%QX0.0</text>
    <text x="500" y="426" fill="#cf222e">BOOL</text>
    <text x="610" y="426" fill="#0550ae">ADV</text>
    <text x="780" y="426" fill="#656d76">solenoid trigger</text>

    <rect x="36" y="434" width="888" height="24" fill="#f6f8fa" stroke="#d0d7de" stroke-width="0.5"/>
    <text x="50" y="450" fill="#0550ae" font-weight="600">SOL_Ret</text>
    <text x="200" y="450" fill="#bc4c00">Output ◀</text>
    <text x="320" y="450" fill="#1f2328">%QX0.1</text>
    <text x="500" y="450" fill="#cf222e">BOOL</text>
    <text x="610" y="450" fill="#0550ae">RET</text>
    <text x="780" y="450" fill="#656d76">solenoid trigger</text>
  </g>

  <text x="36" y="490" class="d-tiny">★ ApiDefActionType: Normal · Push · Pulse · Time(ms) — 디바이스 동작 타입에 따라 Tx/Rx 시그널 패턴 결정</text>
""")


# ══════════════════════════════════════════════════════════════════════════════
# FLOW — Sequential Work flow with token visualization
# ══════════════════════════════════════════════════════════════════════════════
_FLOW = _svg("0 0 960 480", """
  <rect width="960" height="480" fill="#fdfdff"/>
  <text x="36" y="38" class="d-title">🌊 Flow — Work 의 컨테이너 (흐름은 ArrowWork 가 결정)</text>
  <text x="36" y="58" class="d-subtitle">Flow 자체에는 흐름 정보 없음 · Work 의 parentId 그룹일 뿐 · ArrowBetweenWorks 는 System 소속</text>

  <!-- DsSystem outer container (Arrow 의 parent) -->
  <rect x="36" y="80" width="888" height="220" rx="10" fill="url(#card-green)" stroke="#1a7f37" stroke-width="2" filter="url(#dshadow)"/>
  <text x="60" y="106" class="d-section" fill="#1a7f37" font-size="15">DsSystem "Cell-A"</text>
  <text x="60" y="124" class="d-tiny" fill="#1a7f37">★ ArrowBetweenWorks 의 진짜 parent — 모든 Work 간 전이 규칙은 여기에 등록됨</text>

  <!-- Flow inner — 단순 컨테이너만 -->
  <rect x="60" y="140" width="840" height="148" rx="8" fill="#fff" stroke="#0969da" stroke-width="2"/>
  <text x="80" y="162" class="d-label" fill="#0550ae">Flow "MainFlow" — Work 컨테이너 (parentId 그룹)</text>
  <text x="80" y="180" class="d-mono">id · name · parentId(=Cell-A.id) · properties[*]</text>

  <!-- 4 Works inside Flow (no arrows between — Flow 가 전이 결정 안 함) -->
  <rect x="84" y="200" width="184" height="76" rx="6" fill="url(#card-blue)" stroke="#0969da" stroke-width="2"/>
  <text x="98" y="222" class="d-label" fill="#0550ae">W₁ Pickup</text>
  <text x="98" y="240" class="d-tiny">parentId = Flow.id</text>
  <rect x="98" y="248" width="50" height="18" rx="9" fill="#dafbe1" stroke="#1a7f37"/>
  <text x="106" y="261" font-size="9" fill="#116329" font-weight="700">Source</text>

  <rect x="280" y="200" width="184" height="76" rx="6" fill="url(#card-blue)" stroke="#0969da" stroke-width="2"/>
  <text x="294" y="222" class="d-label" fill="#0550ae">W₂ Process</text>
  <text x="294" y="240" class="d-tiny">parentId = Flow.id</text>
  <text x="294" y="262" class="d-tiny">duration: 8.0s</text>

  <rect x="476" y="200" width="184" height="76" rx="6" fill="url(#card-blue)" stroke="#0969da" stroke-width="2"/>
  <text x="490" y="222" class="d-label" fill="#0550ae">W₃ Place</text>
  <text x="490" y="240" class="d-tiny">parentId = Flow.id</text>
  <text x="490" y="262" class="d-tiny">duration: 6.0s</text>

  <rect x="672" y="200" width="208" height="76" rx="6" fill="url(#card-blue)" stroke="#0969da" stroke-width="2"/>
  <text x="688" y="222" class="d-label" fill="#0550ae">W₄ Reset</text>
  <text x="688" y="240" class="d-tiny">parentId = Flow.id</text>
  <rect x="688" y="248" width="40" height="18" rx="9" fill="#ffeaea" stroke="#cf222e"/>
  <text x="697" y="261" font-size="9" fill="#cf222e" font-weight="700">Sink</text>

  <!-- ArrowBetweenWorks panel — System 소속 -->
  <rect x="36" y="320" width="888" height="116" rx="10" fill="url(#card-amber)" stroke="#9a6700" stroke-width="2" filter="url(#dshadow)"/>
  <text x="60" y="346" class="d-section" fill="#9a6700" font-size="15">ArrowBetweenWorks[*] — DsSystem 소속 (⚠ Flow.id 가 아니라 System.id)</text>
  <text x="60" y="364" class="d-tiny" fill="#9a6700">전이 / 리셋 / 그룹 규칙은 모두 여기서 정의 — Flow 는 단순 Work 그룹</text>

  <g font-family="ui-monospace, Consolas, monospace" font-size="11" fill="#1f2328">
    <text x="60" y="386"><tspan fill="#9a6700">#1</tspan>  parentId=<tspan fill="#0550ae">Cell-A.id</tspan>  source=<tspan fill="#0550ae">W₁.id</tspan>  target=<tspan fill="#0550ae">W₂.id</tspan>  type=<tspan fill="#cf222e">Start(=1)</tspan></text>
    <text x="60" y="404"><tspan fill="#9a6700">#2</tspan>  parentId=<tspan fill="#0550ae">Cell-A.id</tspan>  source=<tspan fill="#0550ae">W₂.id</tspan>  target=<tspan fill="#0550ae">W₃.id</tspan>  type=<tspan fill="#cf222e">Start(=1)</tspan></text>
    <text x="60" y="422"><tspan fill="#9a6700">#3</tspan>  parentId=<tspan fill="#0550ae">Cell-A.id</tspan>  source=<tspan fill="#0550ae">W₃.id</tspan>  target=<tspan fill="#0550ae">W₄.id</tspan>  type=<tspan fill="#cf222e">Start(=1)</tspan></text>
  </g>

  <!-- Bottom note -->
  <text x="36" y="460" class="d-tiny">★ 핵심 규칙: Work.parentId = Flow.id (그룹) · ArrowBetweenWorks.parentId = System.id (전이 규칙). 같은 System 안 다른 Flow 의 Work 도 ArrowWork 로 연결 가능.</text>
""")


# ══════════════════════════════════════════════════════════════════════════════
# WORK — UML state diagram (R/G/F/H)
# ══════════════════════════════════════════════════════════════════════════════
_WORK = _svg("0 0 1000 540", """
  <rect width="1000" height="540" fill="#fdfdff"/>
  <text x="36" y="38" class="d-title">⚡ Work — Status4 R/G/F/H 상태머신</text>
  <text x="36" y="58" class="d-subtitle">UML state diagram · 외부 신호(Start↑/Reset) ⊕ 내부 완료 조건으로 전이</text>

  <!-- Initial state marker (UML convention) -->
  <circle cx="74" cy="240" r="10" fill="#1f2328"/>
  <line x1="86" y1="240" x2="138" y2="240" stroke="#1f2328" stroke-width="2" marker-end="url(#m-gray)"/>
  <text x="74" y="270" class="d-tiny" text-anchor="middle">[init]</text>

  <!-- States -->
  <g>
    <!-- R Ready -->
    <circle cx="200" cy="240" r="58" fill="url(#grad-r)" filter="url(#dshadow-strong)"/>
    <text x="200" y="252" class="d-state-name">R</text>
    <text x="200" y="278" class="d-state-sub">Ready · 0</text>
    <rect x="130" y="320" width="140" height="76" rx="6" fill="#fff" stroke="#1a7f37" stroke-width="1.5"/>
    <text x="200" y="340" class="d-section" text-anchor="middle" fill="#116329">Ready</text>
    <text x="200" y="358" class="d-text" text-anchor="middle">실행 준비 / 대기</text>
    <text x="200" y="376" class="d-tiny" text-anchor="middle">토큰 도착 대기</text>
    <text x="200" y="390" class="d-tiny" text-anchor="middle">do: nothing</text>

    <!-- G Going -->
    <circle cx="430" cy="240" r="58" fill="url(#grad-g)" filter="url(#dshadow-strong)"/>
    <text x="430" y="252" class="d-state-name">G</text>
    <text x="430" y="278" class="d-state-sub">Going · 1</text>
    <rect x="360" y="320" width="140" height="76" rx="6" fill="#fff" stroke="#bc4c00" stroke-width="1.5"/>
    <text x="430" y="340" class="d-section" text-anchor="middle" fill="#a04100">Going</text>
    <text x="430" y="358" class="d-text" text-anchor="middle">실행 중 / 진행</text>
    <text x="430" y="376" class="d-tiny" text-anchor="middle">do: Calls 직렬 실행</text>
    <text x="430" y="390" class="d-tiny" text-anchor="middle">duration 카운트</text>

    <!-- F Finish -->
    <circle cx="660" cy="240" r="58" fill="url(#grad-f)" filter="url(#dshadow-strong)"/>
    <text x="660" y="252" class="d-state-name">F</text>
    <text x="660" y="278" class="d-state-sub">Finish · 2</text>
    <rect x="590" y="320" width="140" height="76" rx="6" fill="#fff" stroke="#0969da" stroke-width="1.5"/>
    <text x="660" y="340" class="d-section" text-anchor="middle" fill="#0550ae">Finish</text>
    <text x="660" y="358" class="d-text" text-anchor="middle">완료 / 다음으로</text>
    <text x="660" y="376" class="d-tiny" text-anchor="middle">do: 토큰 → next Work</text>
    <text x="660" y="390" class="d-tiny" text-anchor="middle">Reset 신호 대기</text>

    <!-- H Homing -->
    <circle cx="890" cy="240" r="58" fill="url(#grad-h)" filter="url(#dshadow-strong)"/>
    <text x="890" y="252" class="d-state-name">H</text>
    <text x="890" y="278" class="d-state-sub">Homing · 3</text>
    <rect x="820" y="320" width="140" height="76" rx="6" fill="#fff" stroke="#656d76" stroke-width="1.5"/>
    <text x="890" y="340" class="d-section" text-anchor="middle" fill="#4f5660">Homing</text>
    <text x="890" y="358" class="d-text" text-anchor="middle">초기화 / 복귀</text>
    <text x="890" y="376" class="d-tiny" text-anchor="middle">do: 디바이스 원점</text>
    <text x="890" y="390" class="d-tiny" text-anchor="middle">완료 시 R 으로</text>
  </g>

  <!-- Transitions with conditions -->
  <g>
    <!-- R → G -->
    <line x1="258" y1="240" x2="372" y2="240" stroke="#1a7f37" stroke-width="2.5" marker-end="url(#m-blue)"/>
    <rect x="280" y="218" width="70" height="22" rx="11" fill="#fff" stroke="#1a7f37" stroke-width="1.2"/>
    <text x="315" y="234" class="d-cond" fill="#1a7f37">Start ↑</text>

    <!-- G → F -->
    <line x1="488" y1="240" x2="602" y2="240" stroke="#bc4c00" stroke-width="2.5" marker-end="url(#m-blue)"/>
    <rect x="510" y="218" width="78" height="22" rx="11" fill="#fff" stroke="#bc4c00" stroke-width="1.2"/>
    <text x="549" y="234" class="d-cond" fill="#bc4c00">Calls 완료</text>

    <!-- F → H -->
    <line x1="718" y1="240" x2="832" y2="240" stroke="#0969da" stroke-width="2.5" marker-end="url(#m-blue)"/>
    <rect x="740" y="218" width="70" height="22" rx="11" fill="#fff" stroke="#0969da" stroke-width="1.2"/>
    <text x="775" y="234" class="d-cond" fill="#0969da">Reset</text>

    <!-- H → R (cycle back) -->
    <path d="M 890 298 Q 890 460 200 460 Q 200 320 200 298" fill="none" stroke="#656d76" stroke-width="2" stroke-dasharray="6 4" marker-end="url(#m-blue)"/>
    <rect x="490" y="450" width="160" height="22" rx="11" fill="#fff" stroke="#656d76" stroke-width="1.2"/>
    <text x="570" y="466" class="d-cond" fill="#656d76">Homing 완료 (cyclic)</text>
  </g>

  <!-- Status4 enum legend -->
  <rect x="36" y="490" width="928" height="40" rx="6" fill="#f6f8fa" stroke="#d0d7de"/>
  <text x="50" y="510" class="d-section">Status4 enum (Enum.fs):</text>
  <circle cx="225" cy="506" r="6" fill="#1a7f37"/>
  <text x="237" y="510" class="d-text">Ready = 0</text>
  <circle cx="335" cy="506" r="6" fill="#bc4c00"/>
  <text x="347" y="510" class="d-text">Going = 1</text>
  <circle cx="445" cy="506" r="6" fill="#0969da"/>
  <text x="457" y="510" class="d-text">Finish = 2</text>
  <circle cx="558" cy="506" r="6" fill="#656d76"/>
  <text x="570" y="510" class="d-text">Homing = 3</text>
  <text x="685" y="510" class="d-tiny" font-style="italic">★ tokenRole=Source 는 즉시 R→G; Sink 는 F 후 토큰 소멸</text>
""")


# ══════════════════════════════════════════════════════════════════════════════
# CALL — Call execution + Conditions + ApiCalls
# ══════════════════════════════════════════════════════════════════════════════
_CALL = _svg("0 0 960 460", """
  <rect width="960" height="460" fill="#fdfdff"/>
  <text x="36" y="38" class="d-title">📞 Call — Work 안 디바이스 API 호출 단위</text>
  <text x="36" y="58" class="d-subtitle">name = "{DevicesAlias}.{ApiName}" · CallConditions ⊕ ApiCalls 실행</text>

  <!-- Parent Work container -->
  <rect x="36" y="80" width="888" height="232" rx="10" fill="url(#card-blue)" stroke="#0969da" stroke-width="2.5" filter="url(#dshadow)"/>
  <text x="60" y="108" class="d-section" fill="#0550ae" font-size="15">Work "Pickup" (parent)</text>
  <text x="60" y="126" class="d-mono">parentId = MainFlow.id · Status4 = Going (Calls 실행 중)</text>

  <!-- Call cards -->
  <g>
    <!-- Call_1 -->
    <rect x="60" y="140" width="252" height="160" rx="8" fill="#fff" stroke="#0969da" stroke-width="1.8" filter="url(#dshadow)"/>
    <rect x="60" y="140" width="252" height="32" rx="8" fill="#0969da"/>
    <text x="76" y="161" class="d-label" fill="#fff">Call_1: Robot1.MOVE_TO_A</text>
    <text x="76" y="190" class="d-mono-key">DevicesAlias:</text>
    <text x="170" y="190" class="d-mono">"Robot1"</text>
    <text x="76" y="208" class="d-mono-key">ApiName:</text>
    <text x="170" y="208" class="d-mono">"MOVE_TO_A"</text>
    <text x="76" y="226" class="d-mono-key">Status4:</text>
    <text x="170" y="226" class="d-mono" fill="#bc4c00">Going</text>
    <line x1="76" y1="236" x2="296" y2="236" stroke="#d0d7de"/>
    <text x="76" y="254" class="d-meta" font-weight="700">CallConditions</text>
    <text x="76" y="270" class="d-tiny">· AutoAux (자동 보조)</text>
    <text x="76" y="284" class="d-tiny">· SkipUnmatch=false</text>

    <!-- Call_2 -->
    <rect x="338" y="140" width="252" height="160" rx="8" fill="#fff" stroke="#0969da" stroke-width="1.8" filter="url(#dshadow)"/>
    <rect x="338" y="140" width="252" height="32" rx="8" fill="#0969da"/>
    <text x="354" y="161" class="d-label" fill="#fff">Call_2: Gripper1.GRAB</text>
    <text x="354" y="190" class="d-mono-key">DevicesAlias:</text>
    <text x="448" y="190" class="d-mono">"Gripper1"</text>
    <text x="354" y="208" class="d-mono-key">ApiName:</text>
    <text x="448" y="208" class="d-mono">"GRAB"</text>
    <text x="354" y="226" class="d-mono-key">Status4:</text>
    <text x="448" y="226" class="d-mono" fill="#1a7f37">Ready</text>
    <line x1="354" y1="236" x2="574" y2="236" stroke="#d0d7de"/>
    <text x="354" y="254" class="d-meta" font-weight="700">CallConditions</text>
    <text x="354" y="270" class="d-tiny">· ComAux (공통 보조)</text>
    <text x="354" y="284" class="d-tiny">· timeout: 1500ms</text>

    <!-- Call_3 -->
    <rect x="616" y="140" width="252" height="160" rx="8" fill="#fff" stroke="#0969da" stroke-width="1.8" filter="url(#dshadow)"/>
    <rect x="616" y="140" width="252" height="32" rx="8" fill="#0969da"/>
    <text x="632" y="161" class="d-label" fill="#fff">Call_3: Robot1.LIFT</text>
    <text x="632" y="190" class="d-mono-key">DevicesAlias:</text>
    <text x="726" y="190" class="d-mono">"Robot1"</text>
    <text x="632" y="208" class="d-mono-key">ApiName:</text>
    <text x="726" y="208" class="d-mono">"LIFT"</text>
    <text x="632" y="226" class="d-mono-key">Status4:</text>
    <text x="726" y="226" class="d-mono" fill="#1a7f37">Ready</text>
    <line x1="632" y1="236" x2="852" y2="236" stroke="#d0d7de"/>
    <text x="632" y="254" class="d-meta" font-weight="700">apiCalls[*]</text>
    <text x="632" y="270" class="d-tiny">→ apiDefId: ...</text>
    <text x="632" y="284" class="d-tiny">→ originFlowId: MainFlow.id</text>

    <!-- ArrowCall transitions (orange arrows + "Start" label above; full label in subtitle) -->
    <line x1="314" y1="220" x2="336" y2="220" stroke="#bc4c00" stroke-width="2.5" marker-end="url(#m-orange)"/>
    <text x="325" y="212" font-size="8" font-weight="700" fill="#bc4c00" text-anchor="middle">Start</text>
    <line x1="592" y1="220" x2="614" y2="220" stroke="#bc4c00" stroke-width="2.5" marker-end="url(#m-orange)"/>
    <text x="603" y="212" font-size="8" font-weight="700" fill="#bc4c00" text-anchor="middle">Start</text>
  </g>

  <!-- Bottom note for ArrowCall context -->
  <text x="76" y="318" class="d-tiny" fill="#bc4c00">★ Call 사이의 화살표 = ArrowBetweenCalls (arrowType=Start)</text>

  <!-- Inheritance note -->
  <rect x="36" y="324" width="430" height="116" rx="6" fill="#f6f8fa" stroke="#d0d7de"/>
  <text x="50" y="344" class="d-section">F# 타입 / 상속</text>
  <text x="50" y="362" class="d-mono">Call.inherits(DsChild)</text>
  <text x="50" y="378" class="d-mono">DsChild.inherits(DsEntity)</text>
  <text x="50" y="394" class="d-tiny">parentId : Guid → Work.id</text>
  <text x="50" y="408" class="d-tiny">apiCalls : ResizeArray&lt;ApiCall&gt; (Skip 마킹 → 별도 SML)</text>
  <text x="50" y="424" class="d-tiny">callConditions : ResizeArray&lt;CallCondition&gt;</text>

  <!-- CallConditionType enum -->
  <rect x="486" y="324" width="438" height="116" rx="6" fill="#f6f8fa" stroke="#d0d7de"/>
  <text x="500" y="344" class="d-section">CallConditionType enum</text>
  <text x="500" y="362" class="d-text">· <tspan class="d-mono">AutoAux</tspan> — 자동 보조 (다음 Call 자동 트리거)</text>
  <text x="500" y="378" class="d-text">· <tspan class="d-mono">ComAux</tspan> — 공통 보조 (예: 안전 체크)</text>
  <text x="500" y="394" class="d-text">· <tspan class="d-mono">SkipUnmatch</tspan> — 조건 불일치 시 스킵</text>
  <text x="500" y="410" class="d-text">· <tspan class="d-mono">Custom</tspan> — 사용자 정의 expression</text>
  <text x="500" y="430" class="d-tiny" font-style="italic">★ 조건이 모두 충족되어야 ApiCall 실행</text>
""")


# ══════════════════════════════════════════════════════════════════════════════
# APIDEF — Method signature + ActionType variants
# ══════════════════════════════════════════════════════════════════════════════
_APIDEF = _svg("0 0 960 480", """
  <rect width="960" height="480" fill="#fdfdff"/>
  <text x="36" y="38" class="d-title">📥 ApiDef — 디바이스 노출 API 시그니처</text>
  <text x="36" y="58" class="d-subtitle">parentId = Device.id · Tx/Rx IOTag 매핑 · ActionType 4종</text>

  <!-- ApiDef header card -->
  <rect x="36" y="80" width="888" height="60" rx="6" fill="url(#card-amber)" stroke="#9a6700" stroke-width="2" filter="url(#dshadow)"/>
  <text x="60" y="106" class="d-section" fill="#9a6700" font-size="15">ApiDef "MOVE_TO_A"</text>
  <text x="60" y="125" class="d-mono">parentId=Robot1.id · ApiDefActionType=Pulse · TxGuid=&lt;OutTag.id&gt; · RxGuid=&lt;InTag.id&gt;</text>

  <!-- Method signature visualization -->
  <text x="36" y="172" class="d-section">메서드 시그니처 (function signature)</text>
  <line x1="36" y1="180" x2="924" y2="180" stroke="#d0d7de"/>

  <!-- Input box -->
  <rect x="60" y="200" width="280" height="120" rx="8" fill="url(#card-green)" stroke="#1a7f37" stroke-width="2" filter="url(#dshadow)"/>
  <text x="76" y="224" class="d-section" fill="#116329">▶ Input (RxGuid)</text>
  <text x="76" y="246" class="d-mono">InTag = M_Trigger</text>
  <text x="76" y="266" class="d-mono">DataType = BOOL</text>
  <text x="76" y="286" class="d-mono">PLC: %M001</text>
  <text x="76" y="306" class="d-tiny">호출자 → 디바이스 (수신 IOTag)</text>

  <!-- Arrow -->
  <line x1="350" y1="260" x2="610" y2="260" stroke="#0969da" stroke-width="3" marker-end="url(#m-blue)"/>
  <rect x="430" y="240" width="100" height="40" rx="6" fill="#fff" stroke="#0969da" stroke-width="1.5"/>
  <text x="480" y="258" class="d-cond" fill="#0550ae">Pulse</text>
  <text x="480" y="272" class="d-tiny" text-anchor="middle">300ms</text>

  <!-- Output box -->
  <rect x="620" y="200" width="280" height="120" rx="8" fill="url(#card-blue)" stroke="#0969da" stroke-width="2" filter="url(#dshadow)"/>
  <text x="636" y="224" class="d-section" fill="#0550ae">◀ Output (TxGuid)</text>
  <text x="636" y="246" class="d-mono">OutTag = M_Done</text>
  <text x="636" y="266" class="d-mono">DataType = BOOL</text>
  <text x="636" y="286" class="d-mono">PLC: %M002</text>
  <text x="636" y="306" class="d-tiny">디바이스 → 호출자 (송신 IOTag)</text>

  <!-- ActionType variants -->
  <text x="36" y="356" class="d-section">ApiDefActionType DU (4종) — 디바이스 동작 패턴</text>
  <line x1="36" y1="364" x2="924" y2="364" stroke="#d0d7de"/>

  <g>
    <!-- Normal -->
    <rect x="60" y="378" width="200" height="80" rx="6" fill="#fff" stroke="#0969da" stroke-width="1.5" filter="url(#dshadow)"/>
    <text x="76" y="398" class="d-label" fill="#0550ae">Normal</text>
    <text x="76" y="416" class="d-tiny">즉시 실행 · Tx 1 → Rx 1</text>
    <text x="76" y="432" class="d-tiny">예: 센서 READ</text>
    <line x1="80" y1="446" x2="100" y2="446" stroke="#0969da" stroke-width="1"/>
    <line x1="100" y1="446" x2="100" y2="438" stroke="#0969da" stroke-width="1"/>
    <line x1="100" y1="438" x2="160" y2="438" stroke="#0969da" stroke-width="1"/>
    <line x1="160" y1="438" x2="160" y2="446" stroke="#0969da" stroke-width="1"/>
    <line x1="160" y1="446" x2="240" y2="446" stroke="#0969da" stroke-width="1"/>

    <!-- Push -->
    <rect x="276" y="378" width="200" height="80" rx="6" fill="#fff" stroke="#0969da" stroke-width="1.5" filter="url(#dshadow)"/>
    <text x="292" y="398" class="d-label" fill="#0550ae">Push</text>
    <text x="292" y="416" class="d-tiny">Tx 펄스 → Rx 응답 대기</text>
    <text x="292" y="432" class="d-tiny">예: ADV/RET (실린더)</text>
    <line x1="296" y1="446" x2="316" y2="446" stroke="#0969da" stroke-width="1"/>
    <line x1="316" y1="446" x2="316" y2="438" stroke="#0969da" stroke-width="1"/>
    <line x1="316" y1="438" x2="324" y2="438" stroke="#0969da" stroke-width="1"/>
    <line x1="324" y1="438" x2="324" y2="446" stroke="#0969da" stroke-width="1"/>
    <line x1="324" y1="446" x2="380" y2="446" stroke="#0969da" stroke-width="1"/>
    <line x1="380" y1="446" x2="380" y2="438" stroke="#1a7f37" stroke-width="1.5"/>
    <line x1="380" y1="438" x2="456" y2="438" stroke="#1a7f37" stroke-width="1.5"/>

    <!-- Pulse -->
    <rect x="492" y="378" width="200" height="80" rx="6" fill="#fff" stroke="#0969da" stroke-width="1.5" filter="url(#dshadow)"/>
    <text x="508" y="398" class="d-label" fill="#0550ae">Pulse</text>
    <text x="508" y="416" class="d-tiny">짧은 트리거 펄스</text>
    <text x="508" y="432" class="d-tiny">예: 솔레노이드 트리거</text>
    <line x1="512" y1="446" x2="540" y2="446" stroke="#0969da" stroke-width="1"/>
    <line x1="540" y1="446" x2="540" y2="438" stroke="#0969da" stroke-width="1"/>
    <line x1="540" y1="438" x2="548" y2="438" stroke="#0969da" stroke-width="1"/>
    <line x1="548" y1="438" x2="548" y2="446" stroke="#0969da" stroke-width="1"/>
    <line x1="548" y1="446" x2="600" y2="446" stroke="#0969da" stroke-width="1"/>
    <line x1="600" y1="446" x2="600" y2="438" stroke="#0969da" stroke-width="1"/>
    <line x1="600" y1="438" x2="608" y2="438" stroke="#0969da" stroke-width="1"/>
    <line x1="608" y1="438" x2="608" y2="446" stroke="#0969da" stroke-width="1"/>
    <line x1="608" y1="446" x2="672" y2="446" stroke="#0969da" stroke-width="1"/>

    <!-- Time -->
    <rect x="708" y="378" width="200" height="80" rx="6" fill="#fff" stroke="#0969da" stroke-width="1.5" filter="url(#dshadow)"/>
    <text x="724" y="398" class="d-label" fill="#0550ae">Time(ms)</text>
    <text x="724" y="416" class="d-tiny">시간 기반 자동 완료</text>
    <text x="724" y="432" class="d-tiny">예: HOMING (3000ms)</text>
    <line x1="728" y1="450" x2="752" y2="450" stroke="#0969da" stroke-width="1"/>
    <line x1="752" y1="450" x2="752" y2="442" stroke="#0969da" stroke-width="1"/>
    <line x1="752" y1="442" x2="850" y2="442" stroke="#0969da" stroke-width="1"/>
    <line x1="850" y1="442" x2="850" y2="450" stroke="#0969da" stroke-width="1"/>
    <line x1="850" y1="450" x2="888" y2="450" stroke="#0969da" stroke-width="1"/>
  </g>
""")


# ══════════════════════════════════════════════════════════════════════════════
# APICALL — Runtime binding diagram
# ══════════════════════════════════════════════════════════════════════════════
_APICALL = _svg("0 0 960 500", """
  <rect width="960" height="500" fill="#fdfdff"/>
  <text x="36" y="38" class="d-title">🔗 ApiCall — Call ↔ ApiDef 런타임 바인딩</text>
  <text x="36" y="58" class="d-subtitle">apiDefId · originFlowId · InTag/OutTag(IOTag) + ValueSpec(DU)</text>

  <!-- Caller-Callee binding -->
  <g>
    <!-- Caller -->
    <rect x="36" y="80" width="280" height="120" rx="8" fill="url(#card-blue)" stroke="#0969da" stroke-width="2" filter="url(#dshadow)"/>
    <text x="56" y="104" class="d-section" fill="#0550ae">Caller (Call)</text>
    <text x="56" y="124" class="d-mono">Pickup.Call_1</text>
    <text x="56" y="142" class="d-tiny">parent: Work "Pickup"</text>
    <text x="56" y="158" class="d-tiny">name: "Robot1.MOVE_TO_A"</text>
    <text x="56" y="174" class="d-tiny">apiCalls[0]: <tspan font-weight="700">this ApiCall</tspan></text>
    <text x="56" y="190" class="d-tiny">callConditions: [AutoAux]</text>

    <!-- Binding arrow -->
    <line x1="316" y1="140" x2="644" y2="140" stroke="#7c3aed" stroke-width="2" marker-end="url(#m-purple)" stroke-dasharray="5 3"/>
    <rect x="394" y="120" width="170" height="42" rx="6" fill="#fff" stroke="#7c3aed" stroke-width="1.5" filter="url(#dshadow)"/>
    <text x="479" y="138" class="d-cond" fill="#7c3aed">apiDefId binding</text>
    <text x="479" y="154" class="d-tiny" text-anchor="middle">Guid 매칭</text>

    <!-- Callee -->
    <rect x="644" y="80" width="280" height="120" rx="8" fill="url(#card-amber)" stroke="#9a6700" stroke-width="2" filter="url(#dshadow)"/>
    <text x="664" y="104" class="d-section" fill="#9a6700">Callee (ApiDef)</text>
    <text x="664" y="124" class="d-mono">Robot1.MOVE_TO_A</text>
    <text x="664" y="142" class="d-tiny">parent: Robot1 (Device)</text>
    <text x="664" y="158" class="d-tiny">ActionType: Pulse</text>
    <text x="664" y="174" class="d-tiny">TxGuid → M_Done</text>
    <text x="664" y="190" class="d-tiny">RxGuid → M_Trigger</text>
  </g>

  <!-- Tag bindings -->
  <text x="36" y="232" class="d-section">PLC Tag Bindings — physical address pair</text>
  <line x1="36" y1="240" x2="924" y2="240" stroke="#d0d7de"/>

  <!-- InTag -->
  <rect x="36" y="256" width="430" height="140" rx="8" fill="#fff" stroke="#1a7f37" stroke-width="2" filter="url(#dshadow)"/>
  <rect x="36" y="256" width="430" height="32" rx="8" fill="#1a7f37"/>
  <text x="56" y="278" class="d-label" fill="#fff">InTag (RxGuid 측 — 호출자 → 디바이스)</text>
  <text x="56" y="306" class="d-mono-key">name:</text>
  <text x="130" y="306" class="d-mono">"M_Trigger"</text>
  <text x="56" y="324" class="d-mono-key">DataType:</text>
  <text x="130" y="324" class="d-mono" fill="#cf222e">BOOL</text>
  <text x="56" y="342" class="d-mono-key">PLC Address:</text>
  <text x="160" y="342" class="d-mono" fill="#1f2328">%M001</text>
  <text x="56" y="360" class="d-mono-key">inputSpec:</text>
  <text x="140" y="360" class="d-mono" fill="#7c3aed">{ Case: "Constant", Fields: [true] }</text>
  <text x="56" y="382" class="d-tiny">★ Active 시스템이 WRITE → Passive 시스템이 READ (1:1 페어)</text>

  <!-- OutTag -->
  <rect x="494" y="256" width="430" height="140" rx="8" fill="#fff" stroke="#bc4c00" stroke-width="2" filter="url(#dshadow)"/>
  <rect x="494" y="256" width="430" height="32" rx="8" fill="#bc4c00"/>
  <text x="514" y="278" class="d-label" fill="#fff">OutTag (TxGuid 측 — 디바이스 → 호출자)</text>
  <text x="514" y="306" class="d-mono-key">name:</text>
  <text x="588" y="306" class="d-mono">"M_Done"</text>
  <text x="514" y="324" class="d-mono-key">DataType:</text>
  <text x="588" y="324" class="d-mono" fill="#cf222e">BOOL</text>
  <text x="514" y="342" class="d-mono-key">PLC Address:</text>
  <text x="618" y="342" class="d-mono" fill="#1f2328">%M002</text>
  <text x="514" y="360" class="d-mono-key">outputSpec:</text>
  <text x="612" y="360" class="d-mono" fill="#7c3aed">{ Case: "UndefinedValue" }</text>
  <text x="514" y="382" class="d-tiny">★ 디바이스가 WRITE → Active 시스템이 READ (응답 신호)</text>

  <!-- F# example -->
  <rect x="36" y="412" width="888" height="76" rx="6" fill="#0d1117" stroke="#30363d"/>
  <text x="50" y="432" class="d-mono" fill="#79c0ff">let </text>
  <text x="86" y="432" class="d-mono" fill="#ffa657">apiCall</text>
  <text x="142" y="432" class="d-mono" fill="#79c0ff"> = </text>
  <text x="166" y="432" class="d-mono" fill="#7ee787">ApiCall</text>
  <text x="220" y="432" class="d-mono" fill="#e6edf3">("MOVE_TO_A_call_1")</text>
  <text x="50" y="450" class="d-mono" fill="#ffa657">apiCall.ApiDefId</text>
  <text x="190" y="450" class="d-mono" fill="#79c0ff"> &lt;- </text>
  <text x="222" y="450" class="d-mono" fill="#79c0ff">Some </text>
  <text x="262" y="450" class="d-mono" fill="#ffa657">moveApi.Id</text>
  <text x="350" y="450" class="d-mono" fill="#8b949e"> // bind to ApiDef</text>
  <text x="50" y="468" class="d-mono" fill="#ffa657">apiCall.OriginFlowId</text>
  <text x="220" y="468" class="d-mono" fill="#79c0ff"> &lt;- </text>
  <text x="252" y="468" class="d-mono" fill="#79c0ff">Some </text>
  <text x="292" y="468" class="d-mono" fill="#ffa657">mainFlow.Id</text>
  <text x="392" y="468" class="d-mono" fill="#8b949e"> // 호출 컨텍스트 추적</text>
""")


# ══════════════════════════════════════════════════════════════════════════════
# TOKENSPEC — Multi-token flow lanes
# ══════════════════════════════════════════════════════════════════════════════
_TOKENSPEC = _svg("0 0 960 460", """
  <rect width="960" height="460" fill="#fdfdff"/>
  <text x="36" y="38" class="d-title">🎫 TokenSpec — 토큰 사양 + 다중 토큰 흐름</text>
  <text x="36" y="58" class="d-subtitle">제품/레시피 정의 · Project.tokenSpecs[] · Source Work 에서 토큰 발생</text>

  <!-- Two TokenSpec definitions -->
  <g>
    <!-- RecipeA -->
    <rect x="36" y="80" width="430" height="106" rx="8" fill="url(#card-red)" stroke="#cf222e" stroke-width="2" filter="url(#dshadow)"/>
    <circle cx="60" cy="106" r="12" fill="#cf222e"/>
    <text x="56" y="111" font-size="11" font-weight="700" fill="#fff">#1</text>
    <text x="80" y="110" class="d-section" fill="#cf222e">RecipeA · "Steel Door"</text>
    <text x="56" y="138" class="d-mono-key">Id:</text>
    <text x="100" y="138" class="d-mono">1</text>
    <text x="160" y="138" class="d-mono-key">WorkId:</text>
    <text x="220" y="138" class="d-mono">W_Start.id</text>
    <text x="56" y="156" class="d-mono-key">Fields:</text>
    <text x="118" y="156" class="d-mono" fill="#7c3aed">thickness=2mm · color=red · weight=8.5kg</text>
    <text x="56" y="174" class="d-tiny">Source: W_Start (tokenRole=Source)</text>

    <!-- RecipeB -->
    <rect x="494" y="80" width="430" height="106" rx="8" fill="url(#card-purple)" stroke="#7c3aed" stroke-width="2" filter="url(#dshadow)"/>
    <circle cx="518" cy="106" r="12" fill="#7c3aed"/>
    <text x="514" y="111" font-size="11" font-weight="700" fill="#fff">#2</text>
    <text x="538" y="110" class="d-section" fill="#7c3aed">RecipeB · "Aluminum Panel"</text>
    <text x="514" y="138" class="d-mono-key">Id:</text>
    <text x="558" y="138" class="d-mono">2</text>
    <text x="618" y="138" class="d-mono-key">WorkId:</text>
    <text x="678" y="138" class="d-mono">W_Start.id</text>
    <text x="514" y="156" class="d-mono-key">Fields:</text>
    <text x="576" y="156" class="d-mono" fill="#7c3aed">thickness=1mm · color=silver · weight=3.2kg</text>
    <text x="514" y="174" class="d-tiny">Source: W_Start (혼류 시 같은 시스템)</text>
  </g>

  <!-- Multi-token flow lanes -->
  <text x="36" y="216" class="d-section">런타임: 두 토큰이 같은 Flow 안에서 동시 흐름 (혼류)</text>
  <line x1="36" y1="224" x2="924" y2="224" stroke="#d0d7de"/>

  <!-- Lane 1 (RecipeA) -->
  <g>
    <text x="50" y="262" class="d-meta" font-weight="700" fill="#cf222e">Lane #1</text>
    <text x="50" y="280" class="d-tiny" fill="#cf222e">RecipeA</text>

    <circle cx="124" cy="270" r="14" fill="#cf222e" filter="url(#dshadow)"/>
    <text x="120" y="274" font-size="10" font-weight="700" fill="#fff">#1</text>

    <line x1="138" y1="270" x2="170" y2="270" stroke="#cf222e" stroke-width="2" marker-end="url(#m-red)"/>

    <rect x="170" y="252" width="120" height="36" rx="4" fill="#fff" stroke="#0969da" stroke-width="1.5"/>
    <text x="206" y="276" class="d-label" fill="#0550ae" text-anchor="middle">W_Start</text>

    <line x1="290" y1="270" x2="320" y2="270" stroke="#cf222e" stroke-width="2" marker-end="url(#m-red)"/>

    <rect x="320" y="252" width="120" height="36" rx="4" fill="#fff" stroke="#0969da" stroke-width="1.5"/>
    <text x="356" y="276" class="d-label" fill="#0550ae" text-anchor="middle">W_Press</text>

    <line x1="440" y1="270" x2="470" y2="270" stroke="#cf222e" stroke-width="2" marker-end="url(#m-red)"/>

    <rect x="470" y="252" width="120" height="36" rx="4" fill="#fff" stroke="#0969da" stroke-width="1.5"/>
    <text x="516" y="276" class="d-label" fill="#0550ae" text-anchor="middle">W_Inspect</text>

    <line x1="590" y1="270" x2="620" y2="270" stroke="#cf222e" stroke-width="2" marker-end="url(#m-red)"/>

    <rect x="620" y="252" width="120" height="36" rx="4" fill="#fff" stroke="#0969da" stroke-width="1.5"/>
    <text x="668" y="276" class="d-label" fill="#0550ae" text-anchor="middle">W_Pack</text>

    <line x1="740" y1="270" x2="772" y2="270" stroke="#cf222e" stroke-width="2" marker-end="url(#m-red)"/>

    <rect x="772" y="252" width="100" height="36" rx="4" fill="#dafbe1" stroke="#1a7f37" stroke-width="1.5"/>
    <text x="804" y="276" class="d-label" fill="#116329" text-anchor="middle">Sink</text>
  </g>

  <!-- Lane 2 (RecipeB) -->
  <g>
    <text x="50" y="334" class="d-meta" font-weight="700" fill="#7c3aed">Lane #2</text>
    <text x="50" y="352" class="d-tiny" fill="#7c3aed">RecipeB</text>

    <circle cx="124" cy="342" r="14" fill="#7c3aed" filter="url(#dshadow)"/>
    <text x="120" y="346" font-size="10" font-weight="700" fill="#fff">#2</text>

    <line x1="138" y1="342" x2="170" y2="342" stroke="#7c3aed" stroke-width="2" marker-end="url(#m-purple)"/>

    <rect x="170" y="324" width="120" height="36" rx="4" fill="#fff" stroke="#0969da" stroke-width="1.5"/>
    <text x="206" y="348" class="d-label" fill="#0550ae" text-anchor="middle">W_Start</text>

    <line x1="290" y1="342" x2="320" y2="342" stroke="#7c3aed" stroke-width="2" marker-end="url(#m-purple)"/>

    <rect x="320" y="324" width="120" height="36" rx="4" fill="#fff" stroke="#0969da" stroke-width="1.5"/>
    <text x="356" y="348" class="d-label" fill="#0550ae" text-anchor="middle">W_Bend</text>

    <line x1="440" y1="342" x2="470" y2="342" stroke="#7c3aed" stroke-width="2" marker-end="url(#m-purple)"/>

    <rect x="470" y="324" width="120" height="36" rx="4" fill="#fff" stroke="#0969da" stroke-width="1.5"/>
    <text x="516" y="348" class="d-label" fill="#0550ae" text-anchor="middle">W_Inspect</text>

    <line x1="590" y1="342" x2="620" y2="342" stroke="#7c3aed" stroke-width="2" marker-end="url(#m-purple)"/>

    <rect x="620" y="324" width="120" height="36" rx="4" fill="#fff" stroke="#0969da" stroke-width="1.5"/>
    <text x="668" y="348" class="d-label" fill="#0550ae" text-anchor="middle">W_Pack</text>

    <line x1="740" y1="342" x2="772" y2="342" stroke="#7c3aed" stroke-width="2" marker-end="url(#m-purple)"/>

    <rect x="772" y="324" width="100" height="36" rx="4" fill="#dafbe1" stroke="#1a7f37" stroke-width="1.5"/>
    <text x="804" y="348" class="d-label" fill="#116329" text-anchor="middle">Sink</text>
  </g>

  <!-- KPI per token note -->
  <rect x="36" y="384" width="888" height="56" rx="6" fill="#f6f8fa" stroke="#d0d7de"/>
  <text x="50" y="402" class="d-section">Per-Token KPI (sim/Kpi/PerToken)</text>
  <text x="50" y="420" class="d-meta">혼류 환경에서 토큰 유형(origin/spec) 별로 분리 집계 — RecipeA: avg CT 28s, RecipeB: avg CT 18s, 병목 식별 가능</text>
  <text x="50" y="436" class="d-tiny">★ Work.tokenRole = Source(1) · Sink(4) · Ignore(2) · None(0) — Flags 조합 가능 (Source+Sink = 5)</text>
""")


# ══════════════════════════════════════════════════════════════════════════════
# ARROWWORK — 5 ArrowType variations
# ══════════════════════════════════════════════════════════════════════════════
_ARROWWORK = _svg("0 0 960 580", """
  <rect width="960" height="580" fill="#fdfdff"/>
  <text x="36" y="38" class="d-title">↪ ArrowBetweenWorks — Work 간 전이 / 리셋 규칙</text>
  <text x="36" y="58" class="d-subtitle">parentId = DsSystem.id (⚠ Flow 아님) · ArrowType enum 5종</text>

  <!-- Header -->
  <rect x="36" y="80" width="888" height="36" rx="4" fill="#f6f8fa" stroke="#d0d7de"/>
  <text x="50" y="102" class="d-meta" font-weight="700">ArrowType</text>
  <text x="180" y="102" class="d-meta" font-weight="700">시그널</text>
  <text x="306" y="102" class="d-meta" font-weight="700">동작</text>
  <text x="640" y="102" class="d-meta" font-weight="700">실제 사용 예</text>

  <!-- Row 1: Start (=1) -->
  <g>
    <rect x="36" y="120" width="888" height="78" rx="4" fill="#fff" stroke="#1a7f37" stroke-width="1.5"/>
    <text x="50" y="142" class="d-label" fill="#1a7f37">Start (=1)</text>
    <text x="50" y="160" class="d-tiny">기본 순차 전이</text>

    <text x="180" y="146" class="d-mono" fill="#1a7f37">Source.F → Target.R→G</text>
    <text x="180" y="164" class="d-mono" fill="#1a7f37">라이징 엣지 트리거</text>

    <rect x="306" y="138" width="60" height="46" rx="4" fill="url(#card-blue)" stroke="#0969da"/>
    <text x="336" y="166" class="d-text" fill="#0550ae" text-anchor="middle">W₁</text>
    <!-- Arrow + Start↑ label above (no rect, arrow visible) -->
    <line x1="370" y1="161" x2="436" y2="161" stroke="#1a7f37" stroke-width="2.5" marker-end="url(#m-green)"/>
    <text x="403" y="153" font-size="10" font-weight="700" fill="#1a7f37" text-anchor="middle">Start ↑</text>
    <rect x="440" y="138" width="60" height="46" rx="4" fill="url(#card-blue)" stroke="#0969da"/>
    <text x="470" y="166" class="d-text" fill="#0550ae" text-anchor="middle">W₂</text>

    <text x="640" y="146" class="d-text">W_Pickup → W_Process</text>
    <text x="640" y="164" class="d-tiny">완료 후 다음 단계 시작</text>
  </g>

  <!-- Row 2: Reset (=2) -->
  <g>
    <rect x="36" y="202" width="888" height="78" rx="4" fill="#fff" stroke="#bc4c00" stroke-width="1.5"/>
    <text x="50" y="224" class="d-label" fill="#bc4c00">Reset (=2)</text>
    <text x="50" y="242" class="d-tiny">강제 초기화</text>

    <text x="180" y="228" class="d-mono" fill="#bc4c00">Source.G → Target.F→H</text>
    <text x="180" y="246" class="d-mono" fill="#bc4c00">하이 레벨 트리거</text>

    <rect x="306" y="220" width="60" height="46" rx="4" fill="url(#card-blue)" stroke="#0969da"/>
    <text x="336" y="248" class="d-text" fill="#0550ae" text-anchor="middle">W₁</text>
    <!-- Arrow + Reset label above (no rect, arrow visible) -->
    <line x1="370" y1="243" x2="436" y2="243" stroke="#bc4c00" stroke-width="2.5" marker-end="url(#m-orange)"/>
    <text x="403" y="235" font-size="10" font-weight="700" fill="#bc4c00" text-anchor="middle">Reset</text>
    <rect x="440" y="220" width="60" height="46" rx="4" fill="url(#card-blue)" stroke="#0969da"/>
    <text x="470" y="248" class="d-text" fill="#0550ae" text-anchor="middle">W₂</text>

    <text x="640" y="228" class="d-text">상위 Work 시작 → 하위 강제 종료</text>
    <text x="640" y="246" class="d-tiny">에러 핸들링 / 리셋 로직</text>
  </g>

  <!-- Row 3: StartReset (=3) -->
  <g>
    <rect x="36" y="284" width="888" height="78" rx="4" fill="#fff" stroke="#7c3aed" stroke-width="1.5"/>
    <text x="50" y="306" class="d-label" fill="#7c3aed">StartReset (=3)</text>
    <text x="50" y="324" class="d-tiny">양방향 합성</text>

    <text x="180" y="310" class="d-mono" fill="#7c3aed">Start + Reset 조합</text>
    <text x="180" y="328" class="d-mono" fill="#7c3aed">동시 양방향</text>

    <rect x="306" y="302" width="60" height="46" rx="4" fill="url(#card-blue)" stroke="#0969da"/>
    <text x="336" y="330" class="d-text" fill="#0550ae" text-anchor="middle">W₁</text>
    <path d="M 368 320 L 438 320" stroke="#1a7f37" stroke-width="2" marker-end="url(#m-green)"/>
    <path d="M 438 340 L 368 340" stroke="#bc4c00" stroke-width="2" marker-end="url(#m-orange)"/>
    <rect x="440" y="302" width="60" height="46" rx="4" fill="url(#card-blue)" stroke="#0969da"/>
    <text x="470" y="330" class="d-text" fill="#0550ae" text-anchor="middle">W₂</text>

    <text x="640" y="310" class="d-text">상호 독립 전이 + 리셋</text>
    <text x="640" y="328" class="d-tiny">cross-flow 동기화</text>
  </g>

  <!-- Row 4: ResetReset (=4) -->
  <g>
    <rect x="36" y="366" width="888" height="78" rx="4" fill="#fff" stroke="#cf222e" stroke-width="1.5"/>
    <text x="50" y="388" class="d-label" fill="#cf222e">ResetReset (=4)</text>
    <text x="50" y="406" class="d-tiny">상호 리셋 (짝)</text>

    <text x="180" y="392" class="d-mono" fill="#cf222e">A.G → B.H 와 B.G → A.H</text>
    <text x="180" y="410" class="d-mono" fill="#cf222e">배타적 활성</text>

    <rect x="306" y="384" width="60" height="46" rx="4" fill="url(#card-blue)" stroke="#0969da"/>
    <text x="336" y="412" class="d-text" fill="#0550ae" text-anchor="middle">ADV</text>
    <path d="M 368 402 L 438 402" stroke="#cf222e" stroke-width="2" marker-end="url(#m-red)"/>
    <path d="M 438 422 L 368 422" stroke="#cf222e" stroke-width="2" marker-end="url(#m-red)"/>
    <rect x="440" y="384" width="60" height="46" rx="4" fill="url(#card-blue)" stroke="#0969da"/>
    <text x="470" y="412" class="d-text" fill="#0550ae" text-anchor="middle">RET</text>

    <text x="640" y="392" class="d-text">ADV ↔ RET (실린더 짝)</text>
    <text x="640" y="410" class="d-tiny">하나가 진행 중이면 다른 하나는 H</text>
  </g>

  <!-- Row 5: Group (=5) -->
  <g>
    <rect x="36" y="448" width="888" height="78" rx="4" fill="#fff" stroke="#656d76" stroke-width="1.5" stroke-dasharray="4 3"/>
    <text x="50" y="470" class="d-label" fill="#656d76">Group (=5)</text>
    <text x="50" y="488" class="d-tiny">논리 묶음 (실행 의미 없음)</text>

    <text x="180" y="474" class="d-mono" fill="#656d76">시각적 그룹화만</text>
    <text x="180" y="492" class="d-mono" fill="#656d76">런타임 효과 X</text>

    <rect x="306" y="466" width="60" height="46" rx="4" fill="url(#card-blue)" stroke="#0969da"/>
    <text x="336" y="494" class="d-text" fill="#0550ae" text-anchor="middle">W₁</text>
    <line x1="368" y1="489" x2="438" y2="489" stroke="#656d76" stroke-width="1.5" stroke-dasharray="3 2"/>
    <rect x="440" y="466" width="60" height="46" rx="4" fill="url(#card-blue)" stroke="#0969da"/>
    <text x="470" y="494" class="d-text" fill="#0550ae" text-anchor="middle">W₂</text>

    <text x="640" y="474" class="d-text">UI 캔버스에서 보조 그룹</text>
    <text x="640" y="492" class="d-tiny">F# Group 으로 카테고리 관리</text>
  </g>

  <!-- Footer -->
  <text x="36" y="556" class="d-tiny">★ <tspan font-weight="700">parentId 주의</tspan>: ArrowBetweenWorks.parentId = DsSystem.id (Flow 가 아님) — 같은 시스템 안 다른 Flow 의 Work 도 연결 가능</text>
""")


# ══════════════════════════════════════════════════════════════════════════════
# ARROWCALL — Sequential / Parallel Call execution
# ══════════════════════════════════════════════════════════════════════════════
_ARROWCALL = _svg("0 0 960 440", """
  <rect width="960" height="440" fill="#fdfdff"/>
  <text x="36" y="38" class="d-title">↩ ArrowBetweenCalls — Work 안 Call 실행 순서</text>
  <text x="36" y="58" class="d-subtitle">parentId = Work.id · DsArrow 상속 · arrowType 으로 직렬/병렬 결정</text>

  <!-- Sequential pattern -->
  <text x="36" y="92" class="d-section">패턴 1: 직렬 실행 (arrowType=Start)</text>
  <line x1="36" y1="100" x2="924" y2="100" stroke="#d0d7de"/>

  <rect x="36" y="112" width="888" height="100" rx="8" fill="url(#card-blue)" stroke="#0969da" stroke-width="1.5"/>
  <text x="56" y="134" class="d-label" fill="#0550ae">Work "Pickup" — Calls 직렬</text>
  <text x="56" y="152" class="d-tiny">Call_A.F → Call_B.G → ... 순차 진행</text>

  <g transform="translate(60, 165)">
    <rect x="0" y="0" width="160" height="38" rx="6" fill="#fff" stroke="#0969da"/>
    <text x="80" y="24" class="d-text" fill="#0550ae" text-anchor="middle">Call_A: Robot.MOVE</text>
    <!-- Arrow + Start label (above arrow, no rect to keep arrow visible) -->
    <line x1="162" y1="19" x2="204" y2="19" stroke="#bc4c00" stroke-width="2.5" marker-end="url(#m-orange)"/>
    <text x="183" y="11" font-size="9" font-weight="700" fill="#bc4c00" text-anchor="middle">Start</text>
    <rect x="208" y="0" width="160" height="38" rx="6" fill="#fff" stroke="#0969da"/>
    <text x="288" y="24" class="d-text" fill="#0550ae" text-anchor="middle">Call_B: Gripper.GRAB</text>
    <line x1="370" y1="19" x2="412" y2="19" stroke="#bc4c00" stroke-width="2.5" marker-end="url(#m-orange)"/>
    <text x="391" y="11" font-size="9" font-weight="700" fill="#bc4c00" text-anchor="middle">Start</text>
    <rect x="416" y="0" width="160" height="38" rx="6" fill="#fff" stroke="#0969da"/>
    <text x="496" y="24" class="d-text" fill="#0550ae" text-anchor="middle">Call_C: Robot.LIFT</text>
    <line x1="578" y1="19" x2="620" y2="19" stroke="#bc4c00" stroke-width="2.5" marker-end="url(#m-orange)"/>
    <text x="599" y="11" font-size="9" font-weight="700" fill="#bc4c00" text-anchor="middle">Start</text>
    <rect x="624" y="0" width="160" height="38" rx="6" fill="#fff" stroke="#0969da"/>
    <text x="704" y="24" class="d-text" fill="#0550ae" text-anchor="middle">Call_D: Robot.RETURN</text>
  </g>

  <!-- Parallel pattern -->
  <text x="36" y="248" class="d-section">패턴 2: 병렬 실행 (ArrowCall 생략 — fork 시작점에서 동시 활성)</text>
  <line x1="36" y1="256" x2="924" y2="256" stroke="#d0d7de"/>

  <rect x="36" y="268" width="888" height="148" rx="8" fill="url(#card-green)" stroke="#1a7f37" stroke-width="1.5"/>
  <text x="56" y="290" class="d-label" fill="#116329">Work "ParallelOps" — fork-join 병렬</text>

  <g transform="translate(60, 308)">
    <!-- Source call -->
    <rect x="0" y="14" width="120" height="32" rx="6" fill="#fff" stroke="#0969da"/>
    <text x="60" y="34" class="d-text" fill="#0550ae" text-anchor="middle">Call_Init</text>

    <!-- Fork lines -->
    <line x1="120" y1="20" x2="200" y2="0" stroke="#1a7f37" stroke-width="2" marker-end="url(#m-green)"/>
    <line x1="120" y1="30" x2="200" y2="30" stroke="#1a7f37" stroke-width="2" marker-end="url(#m-green)"/>
    <line x1="120" y1="40" x2="200" y2="60" stroke="#1a7f37" stroke-width="2" marker-end="url(#m-green)"/>

    <!-- Parallel calls -->
    <rect x="200" y="-12" width="160" height="28" rx="6" fill="#fff" stroke="#0969da"/>
    <text x="280" y="6" class="d-text" fill="#0550ae" text-anchor="middle">Call_X (parallel)</text>

    <rect x="200" y="20" width="160" height="28" rx="6" fill="#fff" stroke="#0969da"/>
    <text x="280" y="38" class="d-text" fill="#0550ae" text-anchor="middle">Call_Y (parallel)</text>

    <rect x="200" y="52" width="160" height="28" rx="6" fill="#fff" stroke="#0969da"/>
    <text x="280" y="70" class="d-text" fill="#0550ae" text-anchor="middle">Call_Z (parallel)</text>

    <!-- Join lines -->
    <line x1="360" y1="0" x2="440" y2="20" stroke="#1a7f37" stroke-width="2" marker-end="url(#m-green)"/>
    <line x1="360" y1="34" x2="440" y2="30" stroke="#1a7f37" stroke-width="2" marker-end="url(#m-green)"/>
    <line x1="360" y1="64" x2="440" y2="40" stroke="#1a7f37" stroke-width="2" marker-end="url(#m-green)"/>

    <!-- Final call -->
    <rect x="440" y="14" width="120" height="32" rx="6" fill="#fff" stroke="#0969da"/>
    <text x="500" y="34" class="d-text" fill="#0550ae" text-anchor="middle">Call_Done</text>
  </g>

  <!-- Note placed BELOW container body (outside translate group) -->
  <text x="60" y="430" class="d-tiny" fill="#1a7f37">★ X·Y·Z 사이에 ArrowCall 없음 → Init 완료 시 동시 시작 (fork-join semantics)</text>
""")


# ══════════════════════════════════════════════════════════════════════════════
# DETAIL_DIAGRAMS dict
# ══════════════════════════════════════════════════════════════════════════════
DETAIL_DIAGRAMS = {
    "entity/Project/1/0":   _PROJECT,
    "entity/System/1/0":    _SYSTEM,
    "entity/Device/1/0":    _DEVICE,
    "entity/Flow/1/0":      _FLOW,
    "entity/Work/1/0":      _WORK,
    "entity/Call/1/0":      _CALL,
    "entity/ApiDef/1/0":    _APIDEF,
    "entity/ApiCall/1/0":   _APICALL,
    "entity/TokenSpec/1/0": _TOKENSPEC,
    "entity/ArrowWork/1/0": _ARROWWORK,
    "entity/ArrowCall/1/0": _ARROWCALL,
}


def get_detail(path: str):
    """Path → 상세 SVG, 없으면 None."""
    return DETAIL_DIAGRAMS.get(path)
