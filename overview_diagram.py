"""
DS Overview Diagram — Active ⇄ Passive · Tag-Pair Signal Flow
─────────────────────────────────────────────────────────────────
모든 entity CD 페이지에서 공통으로 사용되는 통합 다이어그램.
build_overview(highlight=<EntityName>) 호출 시 해당 엔티티가
빨간색 + glow 효과로 강조됨 (다른 부분은 기본 시안/황금톤).

지원 highlight 값:
  Project · System · Device · Flow · Work · Call · ApiCall · ApiDef ·
  TokenSpec · ArrowWork · ArrowCall · None (강조 없음)

표현 요소:
  · Project       — 외곽 dashed 컨테이너 (전체 캔버스)
  · System        — Active DsSystem 3D 박스 (cyan)
  · Device        — Passive DsSystem 2개 (Cylinder + Motor, amber)
  · Flow          — Active 안 cyan 사각형
  · Work          — Work★ + Passive Work × 2 (cyan dashed)
  · Call          — Call₁ + Passive Call × 2 (white/cyan)
  · ApiCall       — ApiCall ellipse × 3
  · ApiDef        — chevron flag × 4 (Active 좌 2, Passive 좌 1×2)
  · TokenSpec     — 좌상단 recipe card
  · ArrowWork     — 녹색 화살표 (Work★ → Work₂)
  · ArrowCall     — 주황 화살표 (Call₁ → Call₂)
  · TAG (보조)    — 좌하단 wireframe pyramid (entity 아님)
  · Tag-Pair Bus  — Active → Passive 시안 dashed bus × 2
"""

# ─── 색상 상수 ─────────────────────────────────────────────────────
HL_FILL_OPAQUE = "#cf222e"
HL_FILL_TRANS  = "rgba(207,34,46,0.92)"
HL_STROKE      = "#ff8585"
HL_FILTER      = 'filter="url(#overview-glow)"'
HL_TEXT        = "#fff"


def build_overview(highlight: str = None) -> str:
    """Build the unified DS overview SVG with the given entity highlighted."""
    hl = highlight or ""

    def is_hl(*names):
        return hl in names

    def star(name):
        return " ★" if is_hl(name) else ""

    # ── Project boundary ─────────────────────────────────────────
    if is_hl("Project"):
        proj = ('stroke="#ff8585" stroke-width="3" '
                'filter="url(#overview-glow)" opacity="1"')
        proj_label = ('fill="#ff8585" font-size="16" font-weight="700"')
    else:
        proj = ('stroke="#3d6fb5" stroke-width="0.8" '
                'stroke-dasharray="8 5" opacity="0.5"')
        proj_label = ('fill="#9bcaff" font-size="11" font-style="italic" opacity="0.6"')

    # ── TokenSpec card ───────────────────────────────────────────
    if is_hl("TokenSpec"):
        ts_box = (f'fill="{HL_FILL_TRANS}" stroke="{HL_STROKE}" '
                  f'stroke-width="2.5" filter="url(#overview-glow)"')
        ts_label = HL_TEXT
        ts_sub = "#ffd0d0"
    else:
        ts_box = ('fill="rgba(252,211,77,0.08)" stroke="#fcd34d" stroke-width="1.4"')
        ts_label = "#fef3c7"
        ts_sub = "#fcd34d"

    # ── Active System (cyan box) ─────────────────────────────────
    if is_hl("System"):
        sys_top    = (f'fill="rgba(207,34,46,0.55)" stroke="{HL_STROKE}" '
                      f'stroke-width="3" filter="url(#overview-glow)"')
        sys_right  = (f'fill="rgba(207,34,46,0.40)" stroke="{HL_STROKE}" stroke-width="3"')
        sys_front  = (f'fill="rgba(207,34,46,0.25)" stroke="{HL_STROKE}" stroke-width="3"')
        sys_label  = HL_STROKE
    else:
        sys_top    = 'fill="url(#ov-ds-top-1)" stroke="#54aeff" stroke-width="1.6"'
        sys_right  = 'fill="url(#ov-ds-right-1)" stroke="#54aeff" stroke-width="1.6"'
        sys_front  = 'fill="url(#ov-ds-front-1)" stroke="#54aeff" stroke-width="2"'
        sys_label  = "#dbeefe"

    # ── Device (Passive boxes — both Cylinder & Motor) ──────────
    if is_hl("Device"):
        dev_top   = (f'fill="rgba(207,34,46,0.45)" stroke="{HL_STROKE}" '
                     f'stroke-width="3" filter="url(#overview-glow)"')
        dev_right = (f'fill="rgba(207,34,46,0.35)" stroke="{HL_STROKE}" stroke-width="3"')
        dev_front = (f'fill="rgba(207,34,46,0.22)" stroke="{HL_STROKE}" stroke-width="3"')
        dev_label = HL_STROKE
    else:
        dev_top   = 'fill="url(#ov-ds-top-passive)" stroke="#fcd34d" stroke-width="1.4"'
        dev_right = 'fill="url(#ov-ds-right-passive)" stroke="#fcd34d" stroke-width="1.4"'
        dev_front = 'fill="url(#ov-ds-front-passive)" stroke="#fcd34d" stroke-width="1.8"'
        dev_label = "#fef3c7"

    # ── Flow (Active 안 사각형) ──────────────────────────────────
    if is_hl("Flow"):
        flow_attrs = (f'fill="rgba(207,34,46,0.30)" stroke="{HL_STROKE}" '
                      f'stroke-width="3" filter="url(#overview-glow)"')
        flow_label_color = HL_STROKE
    else:
        flow_attrs = 'fill="rgba(30,60,140,0.18)" stroke="#54aeff" stroke-width="1.5"'
        flow_label_color = "#9bcaff"

    # ── Work (Work★ in Active + Passive Works × 2) ───────────────
    if is_hl("Work"):
        work_attrs = (f'fill="{HL_FILL_TRANS}" stroke="{HL_STROKE}" '
                      f'stroke-width="3" filter="url(#overview-glow)"')
        work_label_color = HL_TEXT
        # Passive abstract Work outline
        pwork_attrs = (f'fill="rgba(207,34,46,0.20)" stroke="{HL_STROKE}" '
                       f'stroke-width="2" stroke-dasharray="4 3" filter="url(#overview-glow)"')
        pwork_label = HL_STROKE
    else:
        work_attrs = ('fill="rgba(60,120,200,0.18)" stroke="#9bcaff" stroke-width="1.8"')
        work_label_color = "#dbeefe"
        pwork_attrs = ('fill="rgba(125,211,252,0.04)" stroke="#7dd3fc" '
                       'stroke-width="1.2" stroke-dasharray="4 3"')
        pwork_label = "#7dd3fc"

    # ── Call (Call₁ in Active + Passive Calls × 2) ───────────────
    if is_hl("Call"):
        call_attrs = (f'fill="{HL_FILL_TRANS}" stroke="{HL_STROKE}" '
                      f'stroke-width="3" filter="url(#overview-glow)"')
        call_label_color = HL_TEXT
        pcall_attrs = (f'fill="rgba(207,34,46,0.30)" stroke="{HL_STROKE}" '
                       f'stroke-width="2.5" filter="url(#overview-glow)"')
        pcall_label = HL_STROKE
    else:
        call_attrs = ('fill="rgba(255,255,255,0.16)" stroke="#fff" stroke-width="1.5"')
        call_label_color = "#dbeefe"
        pcall_attrs = ('fill="rgba(125,211,252,0.10)" stroke="#7dd3fc" stroke-width="1.2"')
        pcall_label = "#7dd3fc"

    # ── ApiCall (in Active + Passive × 2) ────────────────────────
    if is_hl("ApiCall"):
        apicall_attrs = (f'fill="{HL_FILL_OPAQUE}" stroke="{HL_STROKE}" '
                         f'stroke-width="2.5" filter="url(#overview-glow)"')
        apicall_label_color = HL_TEXT
    else:
        apicall_attrs = 'fill="rgba(255,255,255,0.22)" stroke="#fff" stroke-width="1.2"'
        apicall_label_color = "#dbeefe"
    if is_hl("ApiCall"):
        papicall_attrs = (f'fill="rgba(207,34,46,0.45)" stroke="{HL_STROKE}" '
                          f'stroke-width="2" filter="url(#overview-glow)"')
        papicall_label = HL_TEXT
    else:
        papicall_attrs = ('fill="rgba(125,211,252,0.18)" stroke="#7dd3fc" stroke-width="1"')
        papicall_label = "#7dd3fc"

    # ── ApiDef (4 chevrons total) ────────────────────────────────
    if is_hl("ApiDef"):
        apidef_active = (f'fill="{HL_FILL_OPAQUE}" stroke="{HL_STROKE}" '
                         f'stroke-width="2.5" filter="url(#overview-glow)"')
        apidef_passive = (f'fill="{HL_FILL_OPAQUE}" stroke="{HL_STROKE}" '
                          f'stroke-width="2.5" filter="url(#overview-glow)"')
        apidef_label_active = HL_TEXT
        apidef_label_passive = HL_TEXT
    else:
        apidef_active = 'fill="url(#ov-apidef-grad-1)" stroke="#54aeff" stroke-width="1.5"'
        apidef_passive = 'fill="url(#ov-apidef-grad-passive)" stroke="#fcd34d" stroke-width="1.5"'
        apidef_label_active = "#dbeefe"
        apidef_label_passive = "#fef3c7"

    # ── ArrowWork (Work★ → Work₂ + bottom legend) ────────────────
    # 강조 시: 흰 outline 라인 + 빨간 코어 라인 + 흰 외곽 빨간 마커
    # filter 는 라인에 적용하지 않음 (Gaussian blur 가 화살표를 흐릿하게 만듦).
    # 강조 효과는 halo / callout 으로 별도 표현.
    if is_hl("ArrowWork"):
        arrowwork_attrs = f'stroke="{HL_STROKE}" stroke-width="3" stroke-linecap="round"'
        arrowwork_marker = "url(#ov-arr-red)"
        arrowwork_label_color = HL_STROKE
        # 가는 빨간 라인이 빨간/파란 배경에서 잘 보이게 흰 outline (선폭 6) 깔기
        arrowwork_outline_in = ('<line x1="565" y1="438" x2="585" y2="438" '
                                'stroke="#ffffff" stroke-width="6" stroke-linecap="round"/>')
        arrowwork_outline_legend = ('<line x1="240" y1="600" x2="350" y2="600" '
                                    'stroke="#ffffff" stroke-width="5.5" stroke-linecap="round"/>')
    else:
        arrowwork_attrs = 'stroke="#3cd58a" stroke-width="2.5"'
        arrowwork_marker = "url(#ov-arr-green)"
        arrowwork_label_color = "#3cd58a"
        arrowwork_outline_in = ""
        arrowwork_outline_legend = ""

    # ── ArrowCall (Call₁ → Call₂ + bottom legend) ────────────────
    if is_hl("ArrowCall"):
        arrowcall_attrs = f'stroke="{HL_STROKE}" stroke-width="3" stroke-linecap="round"'
        arrowcall_marker = "url(#ov-arr-red)"
        arrowcall_label_color = HL_STROKE
        # Work★ 빨간 배경 위 빨간 화살표 → 가시성 0. 흰 outline 필수.
        arrowcall_outline_in = ('<line x1="388" y1="465" x2="415" y2="465" '
                                'stroke="#ffffff" stroke-width="6" stroke-linecap="round"/>')
        arrowcall_outline_legend = ('<line x1="450" y1="600" x2="560" y2="600" '
                                    'stroke="#ffffff" stroke-width="5.5" stroke-linecap="round"/>')
    else:
        arrowcall_attrs = 'stroke="#ffd17a" stroke-width="2.5"'
        arrowcall_marker = "url(#ov-arr-orange)"
        arrowcall_label_color = "#ffa454"
        arrowcall_outline_in = ""
        arrowcall_outline_legend = ""

    # ── 강조 보조 요소 (halo + callout) — 작은 엔티티 가시성 강화 ─────────
    extras = []

    if is_hl("ArrowWork"):
        # in-context arrow (565-585, 438) — 매우 작음. Halo + 라벨 추가.
        extras.append('''
  <circle cx="575" cy="438" r="32" fill="none" stroke="#ff8585" stroke-width="2.5"
          stroke-dasharray="5 3" filter="url(#overview-glow)"/>
  <rect x="518" y="382" width="116" height="24" rx="12" fill="#cf222e"
        stroke="#ff8585" stroke-width="1.5" filter="url(#overview-glow)"/>
  <text x="576" y="399" text-anchor="middle" fill="#fff" font-size="11" font-weight="700">★ ArrowWork</text>
  <line x1="576" y1="406" x2="576" y2="412" stroke="#ff8585" stroke-width="2"/>''')

    if is_hl("ArrowCall"):
        # in-context CallArrow (388-415, 465) inside Work★ — Halo + 라벨 (Work★ 아래 빈 공간)
        extras.append('''
  <ellipse cx="402" cy="465" rx="32" ry="20" fill="none" stroke="#ff8585" stroke-width="2.5"
           stroke-dasharray="4 3" filter="url(#overview-glow)"/>
  <rect x="345" y="540" width="115" height="24" rx="12" fill="#cf222e"
        stroke="#ff8585" stroke-width="1.5" filter="url(#overview-glow)"/>
  <text x="402" y="557" text-anchor="middle" fill="#fff" font-size="11" font-weight="700">★ ArrowCall</text>
  <path d="M 402 488 Q 402 510 402 540" fill="none" stroke="#ff8585" stroke-width="1.5" stroke-dasharray="3 2" opacity="0.8"/>''')

    if is_hl("ApiCall"):
        # ApiCall ellipses are SMALL (rx=32 ry=13 in Active, rx=22-26 ry=8 in Passives) — add halo + callout
        extras.append('''
  <!-- Halo around Active ApiCall (small ellipse hidden in Work★) -->
  <ellipse cx="330" cy="471" rx="42" ry="22" fill="none" stroke="#ffffff" stroke-width="2.2"
           stroke-dasharray="4 3" filter="url(#overview-glow)" opacity="0.95"/>
  <!-- Halos around Passive 1 + 2 ApiCalls -->
  <ellipse cx="1156" cy="306" rx="32" ry="14" fill="none" stroke="#ff8585" stroke-width="2"
           stroke-dasharray="4 3" filter="url(#overview-glow)"/>
  <ellipse cx="1188" cy="476" rx="36" ry="14" fill="none" stroke="#ff8585" stroke-width="2"
           stroke-dasharray="4 3" filter="url(#overview-glow)"/>
  <!-- Callout below Active -->
  <rect x="200" y="540" width="100" height="24" rx="12" fill="#cf222e"
        stroke="#ff8585" stroke-width="1.5" filter="url(#overview-glow)"/>
  <text x="250" y="557" text-anchor="middle" fill="#fff" font-size="11" font-weight="700">★ ApiCall</text>
  <line x1="250" y1="540" x2="306" y2="488" stroke="#ff8585" stroke-width="1.5" stroke-dasharray="3 2" opacity="0.8"/>''')

    if is_hl("Call"):
        # Call ellipses — already prominent but add callout for clarity
        extras.append('''
  <rect x="200" y="540" width="100" height="24" rx="12" fill="#cf222e"
        stroke="#ff8585" stroke-width="1.5" filter="url(#overview-glow)"/>
  <text x="250" y="557" text-anchor="middle" fill="#fff" font-size="11" font-weight="700">★ Call</text>
  <line x1="270" y1="540" x2="290" y2="492" stroke="#ff8585" stroke-width="1.5" stroke-dasharray="3 2" opacity="0.8"/>''')

    if is_hl("ApiDef"):
        # 4 ApiDef chevrons — already red. Add callout.
        extras.append('''
  <rect x="36" y="406" width="100" height="24" rx="12" fill="#cf222e"
        stroke="#ff8585" stroke-width="1.5" filter="url(#overview-glow)"/>
  <text x="86" y="423" text-anchor="middle" fill="#fff" font-size="11" font-weight="700">★ ApiDef</text>''')

    if is_hl("TokenSpec"):
        # Card already glows. Add larger halo + ★ banner
        extras.append('''
  <rect x="32" y="44" width="138" height="62" rx="6" fill="none" stroke="#ff8585"
        stroke-width="2.5" stroke-dasharray="5 3" filter="url(#overview-glow)"/>''')

    if is_hl("Flow"):
        extras.append('''
  <rect x="200" y="540" width="100" height="24" rx="12" fill="#cf222e"
        stroke="#ff8585" stroke-width="1.5" filter="url(#overview-glow)"/>
  <text x="250" y="557" text-anchor="middle" fill="#fff" font-size="11" font-weight="700">★ Flow</text>''')

    if is_hl("Work"):
        # Work★ already has glow + ★. Add a small badge banner outside Active for clarity
        extras.append('''
  <rect x="200" y="540" width="100" height="24" rx="12" fill="#cf222e"
        stroke="#ff8585" stroke-width="1.5" filter="url(#overview-glow)"/>
  <text x="250" y="557" text-anchor="middle" fill="#fff" font-size="11" font-weight="700">★ Work</text>''')

    if is_hl("System"):
        extras.append('''
  <rect x="200" y="540" width="140" height="24" rx="12" fill="#cf222e"
        stroke="#ff8585" stroke-width="1.5" filter="url(#overview-glow)"/>
  <text x="270" y="557" text-anchor="middle" fill="#fff" font-size="11" font-weight="700">★ System (Active)</text>''')

    if is_hl("Device"):
        extras.append('''
  <rect x="940" y="540" width="170" height="24" rx="12" fill="#cf222e"
        stroke="#ff8585" stroke-width="1.5" filter="url(#overview-glow)"/>
  <text x="1025" y="557" text-anchor="middle" fill="#fff" font-size="11" font-weight="700">★ Device (Passive ×2)</text>''')

    if is_hl("Project"):
        extras.append('''
  <rect x="630" y="540" width="120" height="24" rx="12" fill="#cf222e"
        stroke="#ff8585" stroke-width="1.5" filter="url(#overview-glow)"/>
  <text x="690" y="557" text-anchor="middle" fill="#fff" font-size="11" font-weight="700">★ Project</text>''')

    extras_block = "\n".join(extras)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1400 660">
<defs>
  <linearGradient id="ov-ds-top-1" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="rgba(48,90,165,0.55)"/>
    <stop offset="1" stop-color="rgba(28,64,128,0.45)"/>
  </linearGradient>
  <linearGradient id="ov-ds-right-1" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="rgba(20,52,115,0.45)"/>
    <stop offset="1" stop-color="rgba(8,28,75,0.55)"/>
  </linearGradient>
  <linearGradient id="ov-ds-front-1" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="rgba(15,40,90,0.22)"/>
    <stop offset="1" stop-color="rgba(8,25,60,0.40)"/>
  </linearGradient>
  <linearGradient id="ov-ds-top-passive" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="rgba(120,90,40,0.45)"/>
    <stop offset="1" stop-color="rgba(80,60,28,0.40)"/>
  </linearGradient>
  <linearGradient id="ov-ds-right-passive" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="rgba(70,55,25,0.40)"/>
    <stop offset="1" stop-color="rgba(45,35,18,0.50)"/>
  </linearGradient>
  <linearGradient id="ov-ds-front-passive" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="rgba(50,40,20,0.20)"/>
    <stop offset="1" stop-color="rgba(30,24,12,0.34)"/>
  </linearGradient>
  <linearGradient id="ov-apidef-grad-1" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="rgba(40,80,150,0.92)"/>
    <stop offset="1" stop-color="rgba(20,52,115,0.92)"/>
  </linearGradient>
  <linearGradient id="ov-apidef-grad-passive" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="rgba(150,110,40,0.92)"/>
    <stop offset="1" stop-color="rgba(115,80,25,0.92)"/>
  </linearGradient>
  <linearGradient id="ov-tag-front-1" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="rgba(48,95,180,0.7)"/>
    <stop offset="1" stop-color="rgba(20,52,115,0.7)"/>
  </linearGradient>
  <linearGradient id="ov-tag-right-1" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="rgba(28,64,128,0.65)"/>
    <stop offset="1" stop-color="rgba(10,30,80,0.65)"/>
  </linearGradient>
  <filter id="overview-glow" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="6" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <marker id="ov-arr-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
    <path d="M0,0 L10,5 L0,10 z" fill="#3cd58a"/>
  </marker>
  <marker id="ov-arr-orange" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
    <path d="M0,0 L10,5 L0,10 z" fill="#ffa454"/>
  </marker>
  <marker id="ov-arr-red" viewBox="-1 -1 12 12" refX="10" refY="5" markerWidth="8" markerHeight="8" orient="auto">
    <path d="M0,0 L10,5 L0,10 z" fill="#ff8585" stroke="#ffffff" stroke-width="1.2" stroke-linejoin="round"/>
  </marker>
</defs>

<!-- Background -->
<rect width="1400" height="660" fill="#061026"/>

<!-- Project boundary (faint dashed by default) -->
<rect x="15" y="15" width="1370" height="565" fill="none" {proj} rx="6"/>
<text x="32" y="38" {proj_label}>Project{star("Project")}</text>

<!-- TokenSpec card (top-left, faint when not highlighted) -->
<g>
  <rect x="40" y="50" width="125" height="50" {ts_box} rx="3"/>
  <polygon points="153,50 165,50 165,62 153,50" fill="rgba(252,211,77,0.20)" stroke="#fcd34d" stroke-width="0.8"/>
</g>
<text x="50" y="70" fill="{ts_label}" font-size="12" font-weight="700">TokenSpec{star("TokenSpec")}</text>
<text x="50" y="88" fill="{ts_sub}" font-size="9" font-style="italic">Recipe · #1</text>

<!-- ════════════ ACTIVE DsSystem 3D Wireframe ════════════ -->
<line x1="220" y1="160" x2="220" y2="480" stroke="#3d6fb5" stroke-width="1" stroke-dasharray="3 4" opacity="0.55"/>
<line x1="220" y1="480" x2="740" y2="480" stroke="#3d6fb5" stroke-width="1" stroke-dasharray="3 4" opacity="0.55"/>
<line x1="220" y1="480" x2="160" y2="530" stroke="#3d6fb5" stroke-width="1" stroke-dasharray="3 4" opacity="0.55"/>
<polygon points="160,210 680,210 740,160 220,160" {sys_top}/>
<polygon points="680,210 680,530 740,480 740,160" {sys_right}/>
<rect x="160" y="210" width="520" height="320" {sys_front}/>

<!-- Active Physical Backdrop (production line) -->
<g opacity="0.45" stroke="#7dd3fc" fill="none">
  <rect x="180" y="232" width="80" height="100" stroke-width="1.5"/>
  <rect x="172" y="226" width="96" height="10" stroke-width="1.4"/>
  <rect x="200" y="276" width="40" height="22" stroke-width="1.3"/>
  <line x1="220" y1="236" x2="220" y2="276" stroke-width="1"/>
  <rect x="178" y="328" width="84" height="10" stroke-width="1.4"/>
  <line x1="195" y1="232" x2="195" y2="328" stroke-width="0.7"/>
  <line x1="245" y1="232" x2="245" y2="328" stroke-width="0.7"/>
  <rect x="556" y="298" width="80" height="34" stroke-width="1.5"/>
  <line x1="596" y1="298" x2="596" y2="262" stroke-width="2"/>
  <line x1="596" y1="262" x2="635" y2="232" stroke-width="2"/>
  <line x1="635" y1="232" x2="628" y2="216" stroke-width="1.7"/>
  <circle cx="596" cy="298" r="8" stroke-width="1.4"/>
  <circle cx="596" cy="262" r="6" stroke-width="1.2"/>
  <circle cx="635" cy="232" r="6" stroke-width="1.2"/>
  <rect x="618" y="208" width="22" height="12" stroke-width="1.2"/>
  <rect x="358" y="282" width="98" height="50" stroke-width="1.5"/>
  <rect x="370" y="290" width="74" height="34" stroke-width="1"/>
  <rect x="386" y="270" width="42" height="14" stroke-width="1.1"/>
  <line x1="407" y1="270" x2="407" y2="282" stroke-width="0.9"/>
</g>
<g opacity="0.55" stroke="#7dd3fc" fill="none">
  <rect x="180" y="510" width="490" height="16" stroke-width="1.5"/>
  <line x1="180" y1="514" x2="670" y2="514" stroke-width="0.7"/>
  <line x1="180" y1="522" x2="670" y2="522" stroke-width="0.7"/>
  <circle cx="200" cy="518" r="6" stroke-width="1"/>
  <circle cx="240" cy="518" r="6" stroke-width="1"/>
  <circle cx="280" cy="518" r="6" stroke-width="1"/>
  <circle cx="320" cy="518" r="6" stroke-width="1"/>
  <circle cx="360" cy="518" r="6" stroke-width="1"/>
  <circle cx="400" cy="518" r="6" stroke-width="1"/>
  <circle cx="440" cy="518" r="6" stroke-width="1"/>
  <circle cx="480" cy="518" r="6" stroke-width="1"/>
  <circle cx="520" cy="518" r="6" stroke-width="1"/>
  <circle cx="560" cy="518" r="6" stroke-width="1"/>
  <circle cx="600" cy="518" r="6" stroke-width="1"/>
  <circle cx="640" cy="518" r="6" stroke-width="1"/>
</g>

<!-- DsSystem big label -->
<text x="370" y="288" fill="{sys_label}" font-size="40" font-weight="700"
      font-family="'Segoe UI', Inter, system-ui, sans-serif" letter-spacing="-1" opacity="0.92">DsSystem{star("System")}</text>

<!-- Active LEFT ApiDefs -->
<polygon points="186,162 186,222 116,222 86,192 116,162" {apidef_active} opacity="0.75"/>
<line x1="60" y1="222" x2="86" y2="192" stroke="#54aeff" stroke-width="1" opacity="0.5"/>
<polygon points="170,192 170,252 90,252 60,222 90,192" {apidef_active}/>
<text x="100" y="228" fill="{apidef_label_active}" font-size="14" font-weight="600">ApiDef{star("ApiDef")}</text>
<polygon points="170,332 170,392 90,392 60,362 90,332" {apidef_active}/>
<text x="100" y="368" fill="{apidef_label_active}" font-size="14" font-weight="600">ApiDef</text>

<!-- TAG pyramid (semantic, lower-left) -->
<line x1="90" y1="475" x2="75" y2="540" stroke="#3d6fb5" stroke-width="1" stroke-dasharray="3 3" opacity="0.6"/>
<line x1="75" y1="540" x2="135" y2="540" stroke="#3d6fb5" stroke-width="1" stroke-dasharray="3 3" opacity="0.6"/>
<line x1="75" y1="540" x2="50" y2="560" stroke="#3d6fb5" stroke-width="1" stroke-dasharray="3 3" opacity="0.6"/>
<polygon points="90,475 110,560 135,540" fill="url(#ov-tag-right-1)" stroke="#54aeff" stroke-width="1.3"/>
<polygon points="90,475 50,560 110,560" fill="url(#ov-tag-front-1)" stroke="#54aeff" stroke-width="1.5"/>
<text x="58" y="585" fill="#dbeefe" font-size="13" font-weight="600">TAG</text>
<path d="M 92 475 Q 70 360 92 252" fill="none" stroke="#54aeff" stroke-width="1.2"
      stroke-dasharray="3 3" opacity="0.7"/>

<!-- Inside Active: Flow ⊃ Work★ ⊃ Call ⊃ ApiCall -->
<rect x="210" y="345" width="450" height="160" {flow_attrs} rx="4"/>
<text x="226" y="367" fill="{flow_label_color}" font-size="18" font-weight="700">Flow{star("Flow")}</text>

<rect x="232" y="378" width="330" height="122" {work_attrs} rx="4"/>
<text x="335" y="408" fill="{work_label_color}" font-size="20" font-weight="700">Work{star("Work")}</text>

<ellipse cx="315" cy="465" rx="68" ry="28" {call_attrs}/>
<text x="298" y="447" fill="{call_label_color}" font-size="13" font-weight="700">Call{star("Call")}</text>

<ellipse cx="330" cy="471" rx="32" ry="13" {apicall_attrs}/>
<text x="310" y="475" fill="{apicall_label_color}" font-size="10" font-weight="600">ApiCall{star("ApiCall")}</text>

<!-- CallArrow (Call₁ → Call₂) -->
{arrowcall_outline_in}
<line x1="388" y1="465" x2="415" y2="465" {arrowcall_attrs} marker-end="{arrowcall_marker}"/>

<!-- Call₂ (sibling, dimmed unless ArrowCall is highlighted) -->
<ellipse cx="475" cy="465" rx="50" ry="22" fill="rgba(255,255,255,0.06)"
         stroke="#fff" stroke-width="1.2" stroke-dasharray="3 3" opacity="0.7"/>
<text x="461" y="469" fill="rgba(255,255,255,0.7)" font-size="11" font-style="italic">Call₂</text>

<!-- WorkArrow (Work★ → Work₂) -->
{arrowwork_outline_in}
<line x1="565" y1="438" x2="585" y2="438" {arrowwork_attrs} marker-end="{arrowwork_marker}"/>

<!-- Work₂ (sibling, dimmed) -->
<rect x="588" y="395" width="68" height="100" fill="rgba(255,255,255,0.04)"
      stroke="#3d6fb5" stroke-width="1.5" stroke-dasharray="3 3" rx="4" opacity="0.75"/>
<text x="603" y="450" fill="#9bcaff" font-size="12" font-style="italic">Work₂</text>

<!-- Bus 1 → Passive 1 (Cylinder) -->
<polygon points="680,275 680,305 720,290" fill="url(#ov-tag-front-1)" stroke="#7dd3fc" stroke-width="1.5"/>
<text x="680" y="268" fill="#7dd3fc" font-size="11" font-weight="700">Write</text>
<line x1="722" y1="290" x2="813" y2="290" stroke="#7dd3fc" stroke-width="3" stroke-dasharray="8 4"/>
<polygon points="815,275 815,305 845,290" fill="url(#ov-tag-front-1)" stroke="#7dd3fc" stroke-width="1.5"/>
<text x="817" y="268" fill="#7dd3fc" font-size="11" font-weight="700">Read</text>

<!-- Bus 2 → Passive 2 (Motor) -->
<path d="M 362 471 Q 470 540 680 460" fill="none" stroke="#54aeff"
      stroke-width="1.2" stroke-dasharray="2 3" opacity="0.7"/>
<polygon points="680,445 680,475 720,460" fill="url(#ov-tag-front-1)" stroke="#7dd3fc" stroke-width="1.5"/>
<text x="680" y="438" fill="#7dd3fc" font-size="11" font-weight="700">Write</text>
<line x1="722" y1="460" x2="813" y2="460" stroke="#7dd3fc" stroke-width="3" stroke-dasharray="8 4"/>
<polygon points="815,445 815,475 845,460" fill="url(#ov-tag-front-1)" stroke="#7dd3fc" stroke-width="1.5"/>
<text x="817" y="438" fill="#7dd3fc" font-size="11" font-weight="700">Read</text>

<!-- ════════════ PASSIVE 1: Cylinder ════════════ -->
<line x1="990" y1="180" x2="990" y2="320" stroke="#7a5d2c" stroke-width="1" stroke-dasharray="3 4" opacity="0.55"/>
<line x1="990" y1="320" x2="1340" y2="320" stroke="#7a5d2c" stroke-width="1" stroke-dasharray="3 4" opacity="0.55"/>
<line x1="990" y1="320" x2="940" y2="355" stroke="#7a5d2c" stroke-width="1" stroke-dasharray="3 4" opacity="0.55"/>
<polygon points="940,215 1290,215 1340,180 990,180" {dev_top}/>
<polygon points="1290,215 1290,355 1340,320 1340,180" {dev_right}/>
<rect x="940" y="215" width="350" height="140" {dev_front}/>

<!-- Passive 1 Physical: Cylinder -->
<g opacity="0.55" stroke="#fcd34d" fill="none">
  <rect x="1015" y="278" width="170" height="42" fill="rgba(252,211,77,0.04)" stroke-width="1.5" rx="3"/>
  <rect x="1009" y="276" width="9" height="46" stroke-width="1"/>
  <rect x="1182" y="276" width="9" height="46" stroke-width="1"/>
  <rect x="1191" y="293" width="48" height="12" fill="rgba(252,211,77,0.08)" stroke-width="1.2"/>
  <rect x="1236" y="289" width="9" height="20" fill="rgba(252,211,77,0.12)" stroke-width="1.2"/>
  <circle cx="1042" cy="273" r="3.5" stroke-width="1"/>
  <circle cx="1158" cy="273" r="3.5" stroke-width="1"/>
  <line x1="1042" y1="269" x2="1042" y2="278" stroke-width="0.8"/>
  <line x1="1158" y1="269" x2="1158" y2="278" stroke-width="0.8"/>
  <line x1="1015" y1="328" x2="1185" y2="328" stroke-width="0.8"/>
  <line x1="1030" y1="320" x2="1030" y2="335" stroke-width="0.8"/>
  <line x1="1170" y1="320" x2="1170" y2="335" stroke-width="0.8"/>
  <line x1="1100" y1="278" x2="1100" y2="320" stroke-width="0.8" stroke-dasharray="3 2"/>
</g>

<text x="970" y="240" fill="{dev_label}" font-size="20" font-weight="700"
      font-family="'Segoe UI', Inter, system-ui, sans-serif" opacity="0.85">DsSystem{star("Device")}</text>

<rect x="1005" y="258" width="240" height="82" {pwork_attrs} rx="3"/>
<text x="1009" y="271" fill="{pwork_label}" font-size="11" font-weight="700">Work</text>

<ellipse cx="1140" cy="302" rx="45" ry="16" {pcall_attrs}/>
<text x="1126" y="295" fill="{pcall_label}" font-size="11" font-weight="700">Call</text>

<ellipse cx="1156" cy="306" rx="22" ry="8" {papicall_attrs}/>
<text x="1140" y="309" fill="{papicall_label}" font-size="9" font-weight="600">ApiCall</text>

<polygon points="940,275 940,305 880,305 855,290 880,275" {apidef_passive}/>
<text x="884" y="295" fill="{apidef_label_passive}" font-size="11" font-weight="600">ApiDef</text>

<!-- Passive 1 outgoing Tag chain (모두 viewBox 안에) -->
<polygon points="1290,300 1290,316 1308,308" fill="url(#ov-tag-front-1)" stroke="#7dd3fc" stroke-width="1"/>
<line x1="1310" y1="308" x2="1352" y2="308" stroke="#7dd3fc" stroke-width="2" stroke-dasharray="5 3"/>
<polygon points="1366,302 1366,314 1354,314 1352,308 1354,302" fill="rgba(115,80,25,0.6)" stroke="#fcd34d" stroke-width="1"/>
<text x="1310" y="334" fill="#9bcaff" font-size="9" font-style="italic">→ DsSystem</text>

<!-- ════════════ PASSIVE 2: Motor ════════════ -->
<line x1="990" y1="350" x2="990" y2="495" stroke="#7a5d2c" stroke-width="1" stroke-dasharray="3 4" opacity="0.55"/>
<line x1="990" y1="495" x2="1340" y2="495" stroke="#7a5d2c" stroke-width="1" stroke-dasharray="3 4" opacity="0.55"/>
<line x1="990" y1="495" x2="940" y2="530" stroke="#7a5d2c" stroke-width="1" stroke-dasharray="3 4" opacity="0.55"/>
<polygon points="940,385 1290,385 1340,350 990,350" {dev_top}/>
<polygon points="1290,385 1290,530 1340,495 1340,350" {dev_right}/>
<rect x="940" y="385" width="350" height="145" {dev_front}/>

<!-- Passive 2 Physical: Motor -->
<g opacity="0.55" stroke="#fcd34d" fill="none">
  <rect x="1015" y="438" width="125" height="68" fill="rgba(252,211,77,0.04)" stroke-width="1.5" rx="4"/>
  <line x1="1030" y1="448" x2="1030" y2="496" stroke-width="0.8"/>
  <line x1="1045" y1="448" x2="1045" y2="496" stroke-width="0.8"/>
  <line x1="1060" y1="448" x2="1060" y2="496" stroke-width="0.8"/>
  <line x1="1075" y1="448" x2="1075" y2="496" stroke-width="0.8"/>
  <line x1="1090" y1="448" x2="1090" y2="496" stroke-width="0.8"/>
  <line x1="1105" y1="448" x2="1105" y2="496" stroke-width="0.8"/>
  <line x1="1120" y1="448" x2="1120" y2="496" stroke-width="0.8"/>
  <rect x="1055" y="425" width="38" height="14" fill="rgba(252,211,77,0.08)" stroke-width="1"/>
  <rect x="1140" y="448" width="18" height="48" fill="rgba(252,211,77,0.08)" stroke-width="1.3"/>
  <rect x="1158" y="466" width="44" height="12" fill="rgba(252,211,77,0.08)" stroke-width="1.2"/>
  <rect x="1200" y="461" width="11" height="22" fill="rgba(252,211,77,0.12)" stroke-width="1.2"/>
  <rect x="1212" y="468" width="38" height="8" fill="rgba(252,211,77,0.08)" stroke-width="1"/>
  <rect x="1020" y="506" width="22" height="9" fill="none" stroke-width="1"/>
  <rect x="1115" y="506" width="22" height="9" fill="none" stroke-width="1"/>
</g>

<text x="970" y="412" fill="{dev_label}" font-size="20" font-weight="700"
      font-family="'Segoe UI', Inter, system-ui, sans-serif" opacity="0.85">DsSystem</text>

<rect x="1005" y="425" width="240" height="98" {pwork_attrs} rx="3"/>
<text x="1009" y="438" fill="{pwork_label}" font-size="11" font-weight="700">Work</text>

<ellipse cx="1175" cy="472" rx="50" ry="16" {pcall_attrs}/>
<text x="1158" y="466" fill="{pcall_label}" font-size="11" font-weight="700">Call</text>

<ellipse cx="1188" cy="476" rx="26" ry="8" {papicall_attrs}/>
<text x="1170" y="479" fill="{papicall_label}" font-size="9" font-weight="600">ApiCall</text>

<polygon points="940,445 940,475 880,475 855,460 880,445" {apidef_passive}/>
<text x="884" y="465" fill="{apidef_label_passive}" font-size="11" font-weight="600">ApiDef</text>

<!-- Passive 2 outgoing Tag chain (모두 viewBox 안에) -->
<polygon points="1290,470 1290,486 1308,478" fill="url(#ov-tag-front-1)" stroke="#7dd3fc" stroke-width="1"/>
<line x1="1310" y1="478" x2="1352" y2="478" stroke="#7dd3fc" stroke-width="2" stroke-dasharray="5 3"/>
<polygon points="1366,472 1366,484 1354,484 1352,478 1354,472" fill="rgba(115,80,25,0.6)" stroke="#fcd34d" stroke-width="1"/>
<text x="1310" y="504" fill="#9bcaff" font-size="9" font-style="italic">→ DsSystem</text>

<!-- ════════════ Bottom legend ════════════ -->
{arrowwork_outline_legend}
<line x1="240" y1="600" x2="350" y2="600" {arrowwork_attrs} marker-end="{arrowwork_marker}"/>
<text x="246" y="620" fill="{arrowwork_label_color}" font-size="13" font-weight="700">ArrowWork{star("ArrowWork")}</text>

{arrowcall_outline_legend}
<line x1="450" y1="600" x2="560" y2="600" {arrowcall_attrs} marker-end="{arrowcall_marker}"/>
<text x="450" y="620" fill="{arrowcall_label_color}" font-size="13" font-weight="700">ArrowCall{star("ArrowCall")}</text>

<line x1="700" y1="600" x2="810" y2="600" stroke="#7dd3fc" stroke-width="3" stroke-dasharray="8 4"/>
<text x="700" y="620" fill="#7dd3fc" font-size="13" font-weight="700">Tag-Pair Bus</text>

<!-- ════════════ Highlight enhancements (halo + callouts) ════════════ -->
{extras_block}
</svg>'''


# Quick test
if __name__ == "__main__":
    for name in ("Project", "System", "Device", "Flow", "Work", "Call",
                 "ApiCall", "ApiDef", "TokenSpec", "ArrowWork", "ArrowCall"):
        svg = build_overview(name)
        import xml.etree.ElementTree as ET
        ET.fromstring(svg)
        print(f"  ✓ build_overview({name!r}) — {len(svg)} bytes, valid XML")
