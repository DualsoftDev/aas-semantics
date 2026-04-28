"""
Sequence 엔티티별 예제 다이어그램 SVG 모음.
generate.py 가 viewer.html 생성 시 사용.
"""

# 공통 SVG 헤더 (defs + 스타일)
_DEFS = """
<defs>
  <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
    <path d="M0,0 L10,5 L0,10 Z" fill="#0969da"/>
  </marker>
  <marker id="arrow-orange" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
    <path d="M0,0 L10,5 L0,10 Z" fill="#bc4c00"/>
  </marker>
  <style>
    .box      { fill:#fff; stroke:#0969da; stroke-width:2; }
    .box-act  { fill:#dafbe1; stroke:#1a7f37; stroke-width:2; }
    .box-dev  { fill:#fff8c5; stroke:#9a6700; stroke-width:2; }
    .box-call { fill:#ddf4ff; stroke:#0969da; stroke-width:2; }
    .box-tok  { fill:#fdd; stroke:#cf222e; stroke-width:2; }
    .lbl      { font:13px ui-sans-serif,system-ui,sans-serif; fill:#1f2328; }
    .lbl-bold { font:bold 14px ui-sans-serif,system-ui,sans-serif; fill:#1f2328; }
    .meta     { font:11px ui-sans-serif,system-ui,sans-serif; fill:#656d76; }
    .state    { fill:#0969da; }
    .state-r  { fill:#1a7f37; }
    .state-g  { fill:#bc4c00; }
    .state-f  { fill:#0969da; }
    .state-h  { fill:#656d76; }
    .arrow    { stroke:#0969da; stroke-width:2; fill:none; marker-end:url(#arrow); }
    .arrow-o  { stroke:#bc4c00; stroke-width:2; fill:none; marker-end:url(#arrow-orange); }
  </style>
</defs>
"""


def _svg(viewbox: str, body: str) -> str:
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}">{_DEFS}{body}</svg>'


DIAGRAMS = {

    # ── PROJECT ────────────────────────────────────────────────────────────
    "entity/Project/1/0": _svg("0 0 640 360", """
      <rect class="box" x="20" y="20" width="600" height="320" rx="8"/>
      <text class="lbl-bold" x="40" y="48">Project "MyFactory"</text>
      <text class="meta"     x="40" y="68">Author · Version · DateTime · TokenSpecs</text>

      <text class="meta"     x="40" y="100">Active Systems</text>
      <rect class="box-act"  x="40"  y="110" width="170" height="60" rx="6"/>
      <text class="lbl"      x="55"  y="135">DsSystem "Cell-A"</text>
      <text class="meta"     x="55"  y="155">flows + devices</text>
      <rect class="box-act"  x="230" y="110" width="170" height="60" rx="6"/>
      <text class="lbl"      x="245" y="135">DsSystem "Cell-B"</text>
      <text class="meta"     x="245" y="155">flows + devices</text>

      <text class="meta"     x="40" y="210">Passive Systems (Devices)</text>
      <rect class="box-dev"  x="40"  y="220" width="120" height="50" rx="6"/>
      <text class="lbl"      x="60"  y="250">Cylinder</text>
      <rect class="box-dev"  x="180" y="220" width="120" height="50" rx="6"/>
      <text class="lbl"      x="215" y="250">Robot</text>
      <rect class="box-dev"  x="320" y="220" width="120" height="50" rx="6"/>
      <text class="lbl"      x="345" y="250">Sensor</text>
    """),

    # ── SYSTEM (active) ────────────────────────────────────────────────────
    "entity/System/1/0": _svg("0 0 640 320", """
      <rect class="box-act" x="20" y="20" width="600" height="280" rx="8"/>
      <text class="lbl-bold" x="40" y="48">DsSystem "Cell-A" (active)</text>

      <text class="meta" x="40" y="80">Flow "MainFlow"</text>
      <rect class="box" x="60"  y="90" width="100" height="50" rx="6"/><text class="lbl" x="92" y="120">W1</text>
      <rect class="box" x="200" y="90" width="100" height="50" rx="6"/><text class="lbl" x="232" y="120">W2</text>
      <rect class="box" x="340" y="90" width="100" height="50" rx="6"/><text class="lbl" x="372" y="120">W3</text>
      <line class="arrow" x1="160" y1="115" x2="200" y2="115"/>
      <line class="arrow" x1="300" y1="115" x2="340" y2="115"/>

      <text class="meta" x="40" y="190">Used Devices</text>
      <rect class="box-dev" x="60"  y="200" width="120" height="50" rx="6"/><text class="lbl" x="80"  y="230">Cylinder1</text>
      <rect class="box-dev" x="200" y="200" width="120" height="50" rx="6"/><text class="lbl" x="230" y="230">Robot1</text>
      <rect class="box-dev" x="340" y="200" width="120" height="50" rx="6"/><text class="lbl" x="372" y="230">Sensor1</text>
    """),

    # ── DEVICE (passive) ───────────────────────────────────────────────────
    "entity/Device/1/0": _svg("0 0 480 280", """
      <rect class="box-dev" x="40" y="20" width="400" height="240" rx="8"/>
      <text class="lbl-bold" x="60" y="50">Device "Cylinder1" (passive)</text>
      <text class="meta" x="60" y="70">SystemType: Cylinder_2</text>

      <text class="meta" x="60" y="100">Exposed APIs (ApiDef)</text>
      <rect class="box" x="60"  y="115" width="110" height="40" rx="6"/><text class="lbl" x="92"  y="140">ADV</text>
      <rect class="box" x="190" y="115" width="110" height="40" rx="6"/><text class="lbl" x="222" y="140">RET</text>
      <rect class="box" x="320" y="115" width="110" height="40" rx="6"/><text class="lbl" x="343" y="140">DETECT</text>

      <text class="meta" x="60" y="190">Tags</text>
      <text class="lbl"  x="60" y="215">LS_Adv1, LS_Ret1, SOL_Adv, SOL_Ret …</text>
    """),

    # ── FLOW ───────────────────────────────────────────────────────────────
    "entity/Flow/1/0": _svg("0 0 640 200", """
      <rect class="box-act" x="20" y="20" width="600" height="160" rx="8"/>
      <text class="lbl-bold" x="40" y="50">Flow "MainFlow"</text>

      <rect class="box" x="60"  y="90" width="90" height="50" rx="6"/><text class="lbl" x="90"  y="120">W1 Pickup</text>
      <rect class="box" x="200" y="90" width="90" height="50" rx="6"/><text class="lbl" x="225" y="120">W2 Process</text>
      <rect class="box" x="340" y="90" width="90" height="50" rx="6"/><text class="lbl" x="365" y="120">W3 Place</text>
      <rect class="box" x="480" y="90" width="90" height="50" rx="6"/><text class="lbl" x="505" y="120">W4 Reset</text>
      <line class="arrow" x1="150" y1="115" x2="200" y2="115"/>
      <line class="arrow" x1="290" y1="115" x2="340" y2="115"/>
      <line class="arrow" x1="430" y1="115" x2="480" y2="115"/>
    """),

    # ── WORK (state machine) ───────────────────────────────────────────────
    "entity/Work/1/0": _svg("0 0 640 280", """
      <rect class="box" x="20" y="20" width="600" height="240" rx="8"/>
      <text class="lbl-bold" x="40" y="48">Work "Pickup" — State Machine</text>
      <text class="meta" x="40" y="68">R(eady) → G(oing) → F(inish) → H(oming) → R …</text>

      <circle cx="120" cy="160" r="34" class="state-r"/><text class="lbl" x="113" y="166" fill="#fff">R</text>
      <circle cx="260" cy="160" r="34" class="state-g"/><text class="lbl" x="253" y="166" fill="#fff">G</text>
      <circle cx="400" cy="160" r="34" class="state-f"/><text class="lbl" x="393" y="166" fill="#fff">F</text>
      <circle cx="540" cy="160" r="34" class="state-h"/><text class="lbl" x="533" y="166" fill="#fff">H</text>

      <line class="arrow" x1="155" y1="160" x2="225" y2="160"/>
      <line class="arrow" x1="295" y1="160" x2="365" y2="160"/>
      <line class="arrow" x1="435" y1="160" x2="505" y2="160"/>
      <path class="arrow" d="M540,194 Q540,240 120,210 L120,194"/>

      <text class="meta" x="100" y="220">Ready</text>
      <text class="meta" x="240" y="220">Going</text>
      <text class="meta" x="380" y="220">Finish</text>
      <text class="meta" x="520" y="220">Homing</text>
    """),

    # ── CALL ───────────────────────────────────────────────────────────────
    "entity/Call/1/0": _svg("0 0 640 280", """
      <rect class="box" x="20" y="20" width="600" height="240" rx="8"/>
      <text class="lbl-bold" x="40" y="48">Work "Pickup"</text>
      <text class="meta" x="40" y="68">Calls (sequential within a work)</text>

      <rect class="box-call" x="40"  y="100" width="160" height="60" rx="6"/>
      <text class="lbl"  x="60" y="125">Call_1</text>
      <text class="meta" x="60" y="145">→ Robot.MOVE_TO_A</text>

      <rect class="box-call" x="240" y="100" width="160" height="60" rx="6"/>
      <text class="lbl"  x="260" y="125">Call_2</text>
      <text class="meta" x="260" y="145">→ Gripper.GRAB</text>

      <rect class="box-call" x="440" y="100" width="160" height="60" rx="6"/>
      <text class="lbl"  x="460" y="125">Call_3</text>
      <text class="meta" x="460" y="145">→ Robot.RETURN</text>

      <line class="arrow" x1="200" y1="130" x2="240" y2="130"/>
      <line class="arrow" x1="400" y1="130" x2="440" y2="130"/>

      <text class="meta" x="40" y="200">Each Call references an ApiDef + binds runtime values.</text>
    """),

    # ── ApiDef ────────────────────────────────────────────────────────────
    "entity/ApiDef/1/0": _svg("0 0 600 240", """
      <rect class="box-dev" x="20" y="20" width="560" height="200" rx="8"/>
      <text class="lbl-bold" x="40" y="48">ApiDef "MOVE_TO_A" (exposed by Robot)</text>

      <rect class="box" x="80"  y="90" width="180" height="50" rx="6"/>
      <text class="lbl" x="100" y="115">Input</text>
      <text class="meta" x="100" y="132">InTag: M_Trigger (BOOL)</text>

      <rect class="box" x="340" y="90" width="180" height="50" rx="6"/>
      <text class="lbl" x="360" y="115">Output</text>
      <text class="meta" x="360" y="132">OutTag: M_Done (BOOL)</text>

      <line class="arrow" x1="260" y1="115" x2="340" y2="115"/>

      <text class="meta" x="40" y="180">ApiDef = signature only (caller binds via ApiCall at runtime)</text>
    """),

    # ── ApiCall ───────────────────────────────────────────────────────────
    "entity/ApiCall/1/0": _svg("0 0 640 260", """
      <rect class="box-call" x="20" y="20" width="600" height="220" rx="8"/>
      <text class="lbl-bold" x="40" y="50">ApiCall — runtime binding of Call ↔ ApiDef</text>

      <rect class="box-call" x="40"  y="80" width="170" height="50" rx="6"/>
      <text class="lbl" x="60" y="105">Caller (Call)</text>
      <text class="meta" x="60" y="122">Work_Pickup.Call_1</text>

      <rect class="box-dev" x="430" y="80" width="170" height="50" rx="6"/>
      <text class="lbl" x="450" y="105">Callee (ApiDef)</text>
      <text class="meta" x="450" y="122">Robot.MOVE_TO_A</text>

      <line class="arrow" x1="210" y1="105" x2="430" y2="105"/>
      <text class="meta" x="245" y="98">binding</text>

      <rect class="box" x="40"  y="160" width="560" height="60" rx="6"/>
      <text class="lbl"  x="60" y="185">In: M001 (M_Trigger)</text>
      <text class="lbl"  x="320" y="185">Out: M002 (M_Done)</text>
      <text class="meta" x="60" y="208">실제 PLC 태그가 ApiDef 의 InTag/OutTag 자리에 매핑됨.</text>
    """),

    # ── TokenSpec ─────────────────────────────────────────────────────────
    "entity/TokenSpec/1/0": _svg("0 0 640 280", """
      <rect class="box-tok" x="20" y="20" width="600" height="100" rx="8"/>
      <text class="lbl-bold" x="40" y="48">TokenSpec "RecipeA"</text>
      <text class="meta" x="40" y="70">Id=1 · Label="Steel Door" · Source=W_Start</text>
      <text class="meta" x="40" y="92">Fields: thickness=2mm, color=red</text>

      <text class="meta" x="40" y="155">Token flow at runtime:</text>
      <circle cx="80" cy="200" r="20" class="state-r"/><text class="lbl" x="71" y="205" fill="#fff">#1</text>
      <line class="arrow" x1="105" y1="200" x2="155" y2="200"/>
      <rect class="box" x="155" y="180" width="80" height="40" rx="6"/><text class="lbl" x="180" y="205">W_Start</text>
      <line class="arrow" x1="240" y1="200" x2="290" y2="200"/>
      <rect class="box" x="290" y="180" width="80" height="40" rx="6"/><text class="lbl" x="318" y="205">W2</text>
      <line class="arrow" x1="375" y1="200" x2="425" y2="200"/>
      <rect class="box" x="425" y="180" width="80" height="40" rx="6"/><text class="lbl" x="453" y="205">W3</text>
      <line class="arrow" x1="510" y1="200" x2="560" y2="200"/>
      <text class="lbl" x="565" y="205">Done</text>
    """),

    # ── ArrowWork ─────────────────────────────────────────────────────────
    "entity/ArrowWork/1/0": _svg("0 0 600 220", """
      <rect class="box-act" x="20" y="20" width="560" height="180" rx="8"/>
      <text class="lbl-bold" x="40" y="50">ArrowWork — Work 간 전이 / 리셋 규칙</text>

      <rect class="box" x="80"  y="100" width="120" height="60" rx="6"/>
      <text class="lbl" x="120" y="135">W1 (source)</text>

      <rect class="box" x="380" y="100" width="120" height="60" rx="6"/>
      <text class="lbl" x="420" y="135">W2 (target)</text>

      <line class="arrow-o" x1="200" y1="130" x2="380" y2="130"/>
      <text class="lbl" x="240" y="120">Reset / Sequence</text>
      <text class="meta" x="220" y="155">예: W2 가 R 진입하면 W1 H→R 트리거</text>
    """),

    # ── ArrowCall ─────────────────────────────────────────────────────────
    "entity/ArrowCall/1/0": _svg("0 0 600 220", """
      <rect class="box" x="20" y="20" width="560" height="180" rx="8"/>
      <text class="lbl-bold" x="40" y="50">Work "Pickup" — ArrowCall (Call 간 순서)</text>

      <rect class="box-call" x="60"  y="100" width="130" height="60" rx="6"/>
      <text class="lbl" x="85" y="135">Call_A</text>

      <rect class="box-call" x="240" y="100" width="130" height="60" rx="6"/>
      <text class="lbl" x="265" y="135">Call_B</text>

      <rect class="box-call" x="420" y="100" width="130" height="60" rx="6"/>
      <text class="lbl" x="445" y="135">Call_C</text>

      <line class="arrow" x1="190" y1="130" x2="240" y2="130"/>
      <line class="arrow" x1="370" y1="130" x2="420" y2="130"/>

      <text class="meta" x="40" y="195">Work 내부 Call 들의 직렬 실행 순서를 지정.</text>
    """),
}


def get(path: str):
    """Path → SVG, no diagram defined → None."""
    return DIAGRAMS.get(path)
