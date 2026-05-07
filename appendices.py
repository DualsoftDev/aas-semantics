"""
appendices.py — 학습 가이드 페이지 (CD 가 아닌 부록).

CD 카탈로그 외부의 학습/참고 페이지를 정의. generate.py 가 docs/<slug>/index.html 로
배포한다. 각 부록은 entity/sm/sim CD 의 appendixLinks 에서 상호 참조됨.

부록 1차 (수직 슬라이스): Duality 8 Cases — ds-language.html (HelpDS) 에서 lifting.
"""

import html


def _esc(s: str) -> str:
    return html.escape(s) if s else ""


# ══════════════════════════════════════════════════════════════════════════════
# Duality 8 Cases — 출처: HelpDS/ds-language.html (Korean primary, English bilingual)
DUALITY_CASES = [
    {
        "num": 1,
        "ko": "System ⊕ Device — 동적 역할 전환",
        "en": "System ⊕ Device — Dynamic Role Switching",
        "summary": "DS 시스템은 호출 방향에 따라 'System(능동)' 또는 'Device(수동)' 역할을 동적으로 수행한다.",
        "table": [
            ("상황 1", "A.ApiCall → B.ApiDef", "A=System, B=Device"),
            ("상황 2", "B.ApiCall → A.ApiDef", "B=System, A=Device"),
        ],
        "example": "컨베이어(A) → 로봇팔(B) 제품 전달 요청 = A=System / B=Device.\n로봇팔(B) → 컨베이어(A) 픽업완료 알림 = B=System / A=Device.",
        "linkCds": [("entity/System/1/0", "System"), ("entity/Device/1/0", "Device"),
                    ("entity/ApiDef/1/0", "ApiDef"), ("entity/ApiCall/1/0", "ApiCall")],
    },
    {
        "num": 2,
        "ko": "Instance ⊕ Reference — 디지털 트윈 구조",
        "en": "Instance ⊕ Reference — Digital Twin Structure",
        "summary": "Instance 는 new 로 생성된 실 시스템, Reference 는 기존 시스템을 참조하는 읽기 전용 별칭.",
        "table": [
            ("정의 방식", "new 로 생성된 시스템", "기존 시스템 참조"),
            ("실행 가능성", "✅ Active 설정 시 가능", "❌ 항상 Passive (읽기 전용)"),
            ("값 변경", "✅ 가능", "❌ 불가능"),
        ],
        "example": "동일 Cylinder 디바이스를 두 번 사용할 때:\n- Cylinder1 = Instance (실체)\n- Cylinder1_Mirror = Reference (Cylinder1.Id 참조)\n→ Mirror 는 정의 변경 불가, 표시·시뮬에만 사용.",
        "linkCds": [("entity/Work/1/0", "Work"), ("entity/Call/1/0", "Call")],
    },
    {
        "num": 3,
        "ko": "Arrow 인과 연결과 Bit 이중성",
        "en": "Causal Arrows ⊕ Bit Duality",
        "summary": "흐름의 최소 단위는 Bit. Bit 는 Arrow 인과 연결 속에서 원인이자 결과의 이중성을 가진다.",
        "table": [
            ("Work(Bit)", "시스템 루트의 Bit 그룹", "외부 ApiDef 에 의해 트리거"),
            ("Call(Bit)", "Work 내부 Bit 그룹", "ApiCall 포함"),
        ],
        "example": "ApiDef → Work → Call → ApiCall → ApiDef → … (cyclic causal chain)",
        "linkCds": [("entity/Work/1/0", "Work"), ("entity/Call/1/0", "Call"),
                    ("entity/ArrowWork/1/0", "ArrowWork"), ("entity/ArrowCall/1/0", "ArrowCall")],
    },
    {
        "num": 4,
        "ko": "Tag = Write ⊕ Read — 데이터 전달",
        "en": "Tag = Write ⊕ Read — Data Transfer",
        "summary": "Tag 는 시스템 간 1:1 Pair 연결. Write 측·Read 측이 짝을 이뤄 물리 전송을 표현.",
        "table": [
            ("기본 구조", "Active → Write Tag → [bus] → Read Tag → Passive", "Pair 1:1"),
            ("Shared Memory", "공유 변수처럼 다수 접근", "허용"),
            ("DB 매핑", "간접 경로로 다수 접근", "허용"),
        ],
        "example": "Active System → Write Tag M_Trigger(M001) → [PLC bus] → Read Tag M_Trigger(M001) → Passive Cylinder.\n→ Cylinder 측은 Read 만 가능 (1:1 페어).",
        "linkCds": [("entity/ApiCall/1/0", "ApiCall")],
    },
    {
        "num": 5,
        "ko": "WorkBit = R ⊕ G ⊕ F ⊕ H — FSM 상태",
        "en": "WorkBit = R ⊕ G ⊕ F ⊕ H — FSM States",
        "summary": "Work 의 4개 상태 — 단일 비트(WorkBit) 와 외부 신호 조건에 따라 전이.",
        "table": [
            ("Ready (R)", "Homing 완료 → 진입", "Start 신호 → 종료", "외부 제어"),
            ("Going (G)", "Start 신호 → 진입", "내부 작업 완료 → 종료", "내부 제어"),
            ("Finish (F)", "Going 완료 → 진입", "Reset 신호 → 종료", "외부 제어"),
            ("Homing (H)", "Reset 신호 → 진입", "초기화 완료 → 종료", "내부 제어"),
        ],
        "example": "Ready → [Start↑] → Going → [완료] → Finish → [Reset] → Homing → [초기화 완료] → Ready …",
        "linkCds": [("entity/Work/1/0", "Work"), ("entity/ArrowWork/1/0", "ArrowWork"),
                    ("sm/SequenceMonitoring/1/0", "SeqMonSm")],
    },
    {
        "num": 6,
        "ko": "φ(θ) = Phase ⊕ State Inference",
        "en": "φ(θ) = Phase ⊕ State Inference",
        "summary": "Work 의 센서·상태 조건을 위상값 φ(θ) 로 수치화. Binary / Exponential 두 인코딩.",
        "table": [
            ("Binary", "φ(θ) = (1/2ⁿ) × Σ(2^(i-1) × Vᵢ × Cᵢ,θ) × 2π", "센서 i 별 비트 가중치"),
            ("Exponential", "φ(θ) = (1/eⁿ) × Σ(e^(i-1) × Vᵢ × Cᵢ,θ) × 2π", "고지수 센서에 더 큰 가중"),
        ],
        "example": "디지털 트윈 동기화: 실설비 φ vs 가상설비 φ 비교 → 차이가 임계 초과 시 desync 알람.\n알람 탐지: φ 의 급변 또는 역진행 발생 시 이상 징후 분류.",
        "linkCds": [("sim/Kpi/OEE/1/0", "OEEkpi"), ("sm/SequenceMonitoring/1/0", "SeqMonSm")],
    },
    {
        "num": 7,
        "ko": "Tag = SemanticLink ⊕ PhysicalBinding",
        "en": "Tag = SemanticLink ⊕ PhysicalBinding",
        "summary": "Tag 는 의미론적 연결과 물리적 바인딩의 이중 역할.",
        "table": [
            ("SemanticLink", "동작의 의미 이름", "StartCommand, RobotArmReady"),
            ("PhysicalBinding", "실제 하드웨어 주소", "X100, Y102, DB100.DBX0.2, %IX0.0"),
        ],
        "example": '{ "tagName": "StartSignal", "semantic": "Start", "binding": "X100", "type": "Digital" }',
        "linkCds": [("entity/ApiCall/1/0", "ApiCall")],
    },
    {
        "num": 8,
        "ko": "Arrow = Start ⊕ Reset — 인과 신호",
        "en": "Arrow = Start ⊕ Reset — Causal Signals",
        "summary": "Arrow 는 Start (라이징 엣지) 와 Reset (하이 레벨) 두 의미를 동시에 가진다.",
        "table": [
            ("Start", "라이징 엣지", "이전 Work 의 Finish", "다음 Work 트리거"),
            ("Reset", "하이 레벨", "현재 Work 의 Going", "현재 Work 초기화"),
        ],
        "example": "컨베이어 완료 (Finish↑) ⟹ 로봇팔 시작 (Start 신호)\n로봇팔 실행 (Going■) ⟹ 초기화 조건 활성 (Reset 신호)",
        "timing_table": [
            # rows: label + [(class, value), ...]
            ("Work A", [("r","R"), ("g","G"), ("g","G"), ("f","F"), ("f","F"), ("f","F"), ("f","F")]),
            ("Work B", [("r","R"), ("r","R"), ("r","R"), ("g","G"), ("g","G"), ("f","F"), ("h","H")]),
            ("Start",  [("","0"), ("","0"), ("","0"), ("sig1","1↑"), ("","0"), ("","0"), ("","0")]),
            ("Reset",  [("","0"), ("","0"), ("","0"), ("sig1","1"), ("sig1","1"), ("","0"), ("","0")]),
        ],
        "timing_header": ["t0","t1","t2","t3","t4","t5","t6"],
        "linkCds": [("entity/ArrowWork/1/0", "ArrowWork"), ("entity/Work/1/0", "Work")],
    },
]


# ══════════════════════════════════════════════════════════════════════════════
APPENDICES = {
    "duality": {
        "title": "Duality 8 Cases — ds2 의 이중성 원리",
        "subtitle": "DualSoft DS Language 의 8 가지 이중성 (Cases 1–8)",
        "intro": (
            "DS 시스템은 <strong>하나의 구성 요소가 맥락에 따라 역할과 의미가 달라지는 설계 구조</strong>를 채택한다. "
            "구조적 이중성 (Cases 1–4) 과 실행적 이중성 (Cases 5–8) 두 축으로 분류되며, 모든 ds2 엔티티 (Work / Call / "
            "Arrow / Tag) 의 의미론적 기반이 된다. 본 페이지는 HelpDS/ds-language.html 의 정식 정의를 lifting 한 "
            "참조 문서이며, 각 Case 는 등장하는 ConceptDescription 으로 직접 링크된다."
        ),
        "cases": DUALITY_CASES,
        "summary_struct": [
            ("1", "System ⊕ Device", "호출 방향에 따라 능동/수동", "컨베이어 ↔ 로봇"),
            ("2", "Instance ⊕ Reference", "실행 실체와 참조 대상 구분", "디지털 트윈"),
            ("3", "원인(Bit) ⊕ 결과(Bit)", "흐름 속에서 원인이자 결과", "신호 체인"),
            ("4", "ReadTag ⊕ WriteTag", "맥락에 따른 읽기/쓰기 해석", "데이터 전송"),
        ],
        "summary_exec": [
            ("5", "WorkBit = R⊕G⊕F⊕H", "FSM 기반 상태 흐름", "상태 머신"),
            ("6", "φ(θ) 위상 표현", "센서 조합 기반 위치 수치화", "동기화"),
            ("7", "Tag = Semantic ⊕ Binding", "의미 이름과 물리 주소 연결", "I/O 매핑"),
            ("8", "Arrow = Start ⊕ Reset", "인과 신호 역할 분리", "제어 흐름"),
        ],
    },
}


# ══════════════════════════════════════════════════════════════════════════════
APPENDIX_HEAD = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>{title} — DualSoft AAS Semantics</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
           max-width: 1080px; margin: 2rem auto; padding: 0 1rem; color: #1f2328; line-height: 1.55; }}
    h1 {{ color: #0969da; margin: 0 0 4px 0; font-size: 1.8rem; }}
    h2 {{ color: #1f2328; font-size: 1.25rem; margin-top: 2.4rem; border-bottom: 1px solid #d0d7de; padding-bottom: 4px; }}
    h3 {{ color: #1f2328; font-size: 1.05rem; margin-top: 1.6rem; }}
    .subtitle {{ color: #656d76; font-size: 1.05rem; margin-bottom: 1.4rem; }}
    .links a {{ color: #0969da; text-decoration: none; margin-right: 1rem; font-size: 0.9rem; }}
    .links a:hover {{ text-decoration: underline; }}
    .case-card {{ background: #f6f8fa; border: 1px solid #d0d7de; border-radius: 10px; padding: 16px 20px; margin: 16px 0; }}
    .case-num {{ display: inline-block; background: linear-gradient(135deg, #0969da, #54aeff); color:#fff; font-weight: 700; padding: 3px 12px; border-radius: 14px; font-size: 0.78rem; margin-right: 8px; }}
    .case-title {{ font-size: 1.05rem; font-weight: 700; color: #0550ae; }}
    .case-en {{ color: #656d76; font-size: 0.85rem; margin-left: 6px; font-weight: 400; }}
    .case-summary {{ color: #1f2328; margin: 8px 0 12px 0; font-size: 0.95rem; }}
    .case-table {{ width: 100%; border-collapse: collapse; margin: 8px 0; font-size: 0.86rem; }}
    .case-table th, .case-table td {{ padding: 6px 10px; border: 1px solid #d0d7de; text-align: left; vertical-align: top; }}
    .case-table th {{ background: #fff; color: #656d76; font-size: 0.74rem; text-transform: uppercase; letter-spacing: 0.5px; }}
    .case-example {{ background: #fff; border-left: 3px solid #1a7f37; border-radius: 4px; padding: 10px 14px; margin-top: 10px; font-size: 0.88rem; white-space: pre-line; }}
    .case-link-row {{ margin-top: 12px; display: flex; flex-wrap: wrap; gap: 6px; }}
    .case-link {{ background: #ddf4ff; color: #0969da; border: 1px solid #54aeff; padding: 3px 10px; border-radius: 12px; font-size: 0.78rem; text-decoration: none; }}
    .case-link:hover {{ background: #b7e4ff; }}
    .summary-table {{ width: 100%; border-collapse: collapse; font-size: 0.88rem; margin: 10px 0; }}
    .summary-table th, .summary-table td {{ padding: 8px 12px; border: 1px solid #d0d7de; }}
    .summary-table th {{ background: #f6f8fa; color: #656d76; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.5px; }}
    .summary-table td:first-child {{ font-weight: 700; color: #0550ae; text-align: center; }}
    .timing-strip {{ background: #fff; border: 1px solid #d0d7de; border-radius: 6px; padding: 10px; margin: 10px 0; overflow-x: auto; }}
    .timing-strip table {{ border-collapse: collapse; font-size: 0.78rem; }}
    .timing-strip td {{ padding: 4px 10px; text-align: center; border: 1px solid #d0d7de; min-width: 36px; font-family: ui-monospace, Consolas, monospace; }}
    .timing-strip th {{ padding: 4px 10px; background: #f6f8fa; text-align: center; font-weight: 600; font-size: 0.72rem; color: #656d76; text-transform: uppercase; }}
    .timing-strip td.r {{ background: #dafbe1; color: #1a7f37; font-weight: 600; }}
    .timing-strip td.g {{ background: #ffd8b5; color: #bc4c00; font-weight: 600; }}
    .timing-strip td.f {{ background: #ddf4ff; color: #0969da; font-weight: 600; }}
    .timing-strip td.h {{ background: #eaeef2; color: #656d76; font-weight: 600; }}
    .timing-strip td.sig1 {{ background: #ffeaea; color: #cf222e; font-weight: 700; }}
    .timing-strip td.row-label {{ background: #f6f8fa; font-weight: 600; color: #1f2328; text-align: left; padding-left: 12px; padding-right: 14px; }}
    code {{ background: #eef1f4; padding: 1px 6px; border-radius: 3px; font-size: 0.86em; font-family: ui-monospace, Consolas, monospace; }}
    .footer {{ margin-top: 3rem; padding-top: 1rem; border-top: 1px solid #d0d7de; color: #656d76; font-size: 0.85rem; }}
    .intro-box {{ background: linear-gradient(135deg, #ddf4ff, #fff); border: 1px solid #54aeff; border-radius: 10px; padding: 14px 18px; margin: 12px 0; font-size: 0.96rem; line-height: 1.7; }}
  </style>
</head>
<body>
"""


def _render_case(case) -> str:
    parts = [f'<div class="case-card" id="case-{case["num"]}">']
    parts.append(
        f'<div><span class="case-num">Case {case["num"]}</span>'
        f'<span class="case-title">{_esc(case["ko"])}</span>'
        f'<span class="case-en">— {_esc(case["en"])}</span></div>'
    )
    parts.append(f'<div class="case-summary">{_esc(case["summary"])}</div>')

    # table
    if case.get("table"):
        ncols = len(case["table"][0])
        body = "".join(
            "<tr>" + "".join(f"<td>{_esc(c)}</td>" for c in row) + "</tr>"
            for row in case["table"]
        )
        parts.append(f'<table class="case-table"><tbody>{body}</tbody></table>')

    # timing table (case 8)
    if case.get("timing_table") and case.get("timing_header"):
        head_html = "<tr><th></th>" + "".join(f"<th>{_esc(h)}</th>" for h in case["timing_header"]) + "</tr>"
        body_rows = []
        for label, cells in case["timing_table"]:
            cells_html = "".join(f'<td class="{cls}">{_esc(val)}</td>' for cls, val in cells)
            body_rows.append(f'<tr><td class="row-label">{_esc(label)}</td>{cells_html}</tr>')
        parts.append(
            '<div class="timing-strip"><table>'
            f'<thead>{head_html}</thead>'
            f'<tbody>{"".join(body_rows)}</tbody>'
            '</table></div>'
        )

    # example
    if case.get("example"):
        parts.append(f'<div class="case-example">{_esc(case["example"])}</div>')

    # CD links
    if case.get("linkCds"):
        chips = "".join(
            f'<a class="case-link" href="../../{_esc(path)}/">→ {_esc(name)}</a>'
            for path, name in case["linkCds"]
        )
        parts.append(f'<div class="case-link-row">{chips}</div>')

    parts.append('</div>')
    return "".join(parts)


def _render_summary_table(rows, headers) -> str:
    head = "<tr>" + "".join(f"<th>{_esc(h)}</th>" for h in headers) + "</tr>"
    body = "".join(
        "<tr>" + "".join(f"<td>{_esc(c)}</td>" for c in r) + "</tr>"
        for r in rows
    )
    return f'<table class="summary-table"><thead>{head}</thead><tbody>{body}</tbody></table>'


def render_appendix(slug: str, app: dict, root_rel: str) -> str:
    title = app["title"]
    parts = [APPENDIX_HEAD.format(title=_esc(title))]
    parts.append(f'<div class="links" style="margin-bottom: 1rem;"><a href="{root_rel}">← Catalog</a></div>')
    parts.append(f'<h1>{_esc(title)}</h1>')
    if app.get("subtitle"):
        parts.append(f'<div class="subtitle">{_esc(app["subtitle"])}</div>')
    if app.get("intro"):
        parts.append(f'<div class="intro-box">{app["intro"]}</div>')

    if slug == "duality":
        # Summary tables (구조적 / 실행적)
        parts.append('<h2>이중성 분류 (요약)</h2>')
        parts.append('<h3>🏗️ 구조적 이중성 (Cases 1–4)</h3>')
        parts.append(_render_summary_table(app["summary_struct"], ["Case", "구성 요소", "설명", "예시"]))
        parts.append('<h3>⚡ 실행적 이중성 (Cases 5–8)</h3>')
        parts.append(_render_summary_table(app["summary_exec"], ["Case", "구성 요소", "설명", "활용"]))

        parts.append('<h2>상세 Cases</h2>')
        for case in app["cases"]:
            parts.append(_render_case(case))

    parts.append(
        '<div class="footer">'
        '학습 가이드 (부록) — 출처: <a href="https://github.com/DualsoftDev/HelpDS/blob/master/HelpDS/ds-language.html" target="_blank">HelpDS/ds-language.html</a>. '
        f'Part of <a href="{root_rel}">DualSoft AAS Semantics catalog</a>.'
        '</div>'
        '</body></html>'
    )
    return "".join(parts)
