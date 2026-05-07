"""
Sequence 엔티티별 예제 다이어그램 SVG 모음.
generate.py 가 viewer.html 생성 시 사용.

entity/* CD 11개는 통합 overview 다이어그램(overview_diagram.build_overview)을 사용한다.
각 엔티티 CD 페이지마다 해당 엔티티가 빨간색 + glow 로 강조되는 동일한 다이어그램.
sm/* 와 sim/* 는 별도 도식 (SubmodelElement Tree, KPI 산식 등) 사용.
"""

from overview_diagram import build_overview as _build_overview

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

    "entity/Project/1/0": _build_overview("Project"),

    "entity/System/1/0": _build_overview("System"),

    "entity/Device/1/0": _build_overview("Device"),

    "entity/Flow/1/0": _build_overview("Flow"),

    "entity/Work/1/0": _build_overview("Work"),

    "entity/Call/1/0": _build_overview("Call"),

    "entity/ApiDef/1/0": _build_overview("ApiDef"),

    "entity/ApiCall/1/0": _build_overview("ApiCall"),

    "entity/TokenSpec/1/0": _build_overview("TokenSpec"),

    "entity/ArrowWork/1/0": _build_overview("ArrowWork"),

    # ── SequenceMonitoring SMC tree ───────────────────────────────────────
    "sm/SequenceMonitoring/1/0": _svg("0 0 760 460", """
      <rect class="box" x="20" y="20" width="720" height="420" rx="8"/>
      <text class="lbl-bold" x="40" y="48">SeqMonSm — SubmodelElement Tree</text>
      <text class="meta" x="40" y="68">IDTA 02026-1-0 · semanticId: .../sm/SequenceMonitoring/1/0</text>

      <rect class="box-act" x="40" y="90" width="220" height="44" rx="6"/>
      <text class="lbl" x="60" y="118">📊 SystemSnapshot (SMC)</text>

      <rect class="box-act" x="280" y="90" width="220" height="44" rx="6"/>
      <text class="lbl" x="300" y="118">📋 OperationalEvents (SML)</text>

      <rect class="box-act" x="520" y="90" width="200" height="44" rx="6"/>
      <text class="lbl" x="540" y="118">📈 PerformanceMetrics (SMC)</text>

      <rect class="box-call" x="60" y="150" width="180" height="34" rx="5"/>
      <text class="meta" x="80" y="172">WorkStates: Map&lt;Guid, NodeState&gt;</text>

      <rect class="box-call" x="60" y="190" width="180" height="34" rx="5"/>
      <text class="meta" x="80" y="212">CallStates: Map&lt;Guid, NodeState&gt;</text>

      <rect class="box-call" x="60" y="230" width="180" height="34" rx="5"/>
      <text class="meta" x="80" y="252">WorkProgress: Map&lt;Guid, float&gt;</text>

      <rect class="box-call" x="60" y="270" width="180" height="34" rx="5"/>
      <text class="meta" x="80" y="292">DeviceStates: Map&lt;Name, bool&gt;</text>

      <rect class="box-call" x="60" y="310" width="180" height="34" rx="5"/>
      <text class="meta" x="80" y="332">Statistics: ProductionStats</text>

      <rect class="box-call" x="300" y="150" width="180" height="34" rx="5"/>
      <text class="meta" x="320" y="172">StateChanged · ProgressUpdated</text>
      <rect class="box-call" x="300" y="190" width="180" height="34" rx="5"/>
      <text class="meta" x="320" y="212">CycleStarted · CycleCompleted</text>
      <rect class="box-call" x="300" y="230" width="180" height="34" rx="5"/>
      <text class="meta" x="320" y="252">SystemStarted · SystemStopped</text>
      <rect class="box-call" x="300" y="270" width="180" height="34" rx="5"/>
      <text class="meta" x="320" y="292">IOValueChanged · TcUpdated</text>
      <rect class="box-call" x="300" y="310" width="180" height="34" rx="5"/>
      <text class="meta" x="320" y="332">Flow/WorkMtWtUpdated</text>
      <rect class="box-call" x="300" y="350" width="180" height="34" rx="5"/>
      <text class="meta" x="320" y="372">AlarmOccurred</text>

      <rect class="box-call" x="540" y="150" width="180" height="34" rx="5"/>
      <text class="meta" x="560" y="172">MT (Moving Time, ms)</text>
      <rect class="box-call" x="540" y="190" width="180" height="34" rx="5"/>
      <text class="meta" x="560" y="212">WT (Wait Time, ms)</text>
      <rect class="box-call" x="540" y="230" width="180" height="34" rx="5"/>
      <text class="meta" x="560" y="252">TC = MT + WT (Total Cycle)</text>
      <rect class="box-call" x="540" y="270" width="180" height="34" rx="5"/>
      <text class="meta" x="560" y="292">CT (Cycle Time, per Work)</text>
      <rect class="box-call" x="540" y="310" width="180" height="34" rx="5"/>
      <text class="meta" x="560" y="332">→ sim/Kpi/* CD 박제</text>

      <text class="meta" x="40" y="410">★ 모든 이벤트는 PostgreSQL signal_event/work/flow 테이블에 기록되어 sim/Kpi/* 산출에 사용됨.</text>
    """),

    # ── sim/Kpi/OEE — formula visual ──────────────────────────────────────
    "sim/Kpi/OEE/1/0": _svg("0 0 720 360", """
      <rect class="box" x="20" y="20" width="680" height="320" rx="8"/>
      <text class="lbl-bold" x="40" y="50">OEE = Availability × Performance × Quality</text>
      <text class="meta" x="40" y="72">ISO 22400-2:2014 · 종합설비효율 (Overall Equipment Effectiveness)</text>

      <rect class="box-act" x="60"  y="110" width="170" height="80" rx="8"/>
      <text class="lbl-bold" x="100" y="140" fill="#1a7f37">Availability</text>
      <text class="meta" x="80" y="160">실제 가동 ÷ 계획 가동</text>
      <text class="lbl" x="115" y="180" fill="#1a7f37">0.92</text>

      <text class="lbl-bold" x="245" y="160">×</text>

      <rect class="box-act" x="270" y="110" width="170" height="80" rx="8"/>
      <text class="lbl-bold" x="305" y="140" fill="#bc4c00">Performance</text>
      <text class="meta" x="290" y="160">목표 CT ÷ 실제 CT</text>
      <text class="lbl" x="320" y="180" fill="#bc4c00">0.85</text>

      <text class="lbl-bold" x="455" y="160">×</text>

      <rect class="box-act" x="480" y="110" width="170" height="80" rx="8"/>
      <text class="lbl-bold" x="525" y="140" fill="#0969da">Quality</text>
      <text class="meta" x="500" y="160">양품 ÷ 총생산</text>
      <text class="lbl" x="530" y="180" fill="#0969da">0.98</text>

      <line class="arrow" x1="360" y1="200" x2="360" y2="240"/>

      <rect class="box-tok" x="200" y="250" width="320" height="60" rx="8"/>
      <text class="lbl-bold" x="240" y="280" fill="#cf222e" style="font-size:18px">OEE = 0.7676 (76.76%)</text>
      <text class="meta" x="260" y="300">월드클래스 기준: ≥ 85%</text>
    """),

    "entity/ArrowCall/1/0": _build_overview("ArrowCall"),
}


def get(path: str):
    """Path → SVG, no diagram defined → None."""
    return DIAGRAMS.get(path)
