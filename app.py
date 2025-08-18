# app.py — Enervi7（Streamlit 最終版；已移除 JSON 區塊）
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Enervi7 量測", layout="wide")

# ============ 一、題目文字 ============
Q_TEXTS = {
    "Q1": "Q1 覺察：我能清楚覺察自己此刻的情緒、念頭與身體感受。",
    "Q2": "Q2 釋放：當我察覺壓力或情緒時，我能有效地鬆開與代謝。",
    "Q3": "Q3 信任：我對生活與未來持有信任與安全感，能允許事情順勢發生。",
    "Q4": "Q4 行動：我能把想法拆解成最小可行步驟，並付諸行動。",
    "Q5": "Q5 流動：我能維持專注與節奏，接受回饋並快速微調。",
    "Q6": "Q6 共鳴：我與他人／世界連結感良好，能創造正向回饋與影響。",
    "Q7": "Q7 整合：我能總結經驗並固化成結構與習慣，持續複製成果。"
}
T_TEXTS = {
    "T1": "T1 覺察→釋放：當我看見情緒或議題時，我能順利進入釋放與鬆綁。",
    "T2": "T2 釋放→信任：在放下之後，我能自然進入信任與允許的狀態。",
    "T3": "T3 信任→行動：從內在信任轉為具體行動的過程對我來說是順暢的。",
    "T4": "T4 行動→流動：從單次行動進入穩定節奏與回饋迭代是順暢的。",
    "T5": "T5 流動→共鳴：把成果對外分享並獲得回饋與擴散是順暢的。",
    "T6": "T6 共鳴→整合：將被驗證的做法整理成 SOP／習慣是順暢的。",
    "T7": "T7 整合→新覺察：結束一輪後回到清明覺察開啟下一輪是順暢的。"
}

# ============ 二、七階/轉換文字資源 ============
STAGE_META = {
    "S1": {"name": "S1 覺察 Awareness",
           "keywords": ["覺知當下", "辨識情緒", "看見模式", "誠實面對"],
           "actions": ["寫三句『此刻我真實的感受是…』",
                       "3 分鐘腹式呼吸（4-4-6）並記錄身體感受",
                       "列出 1 個反覆出現的念頭，標記：是事實還是解讀？"]},
    "S2": {"name": "S2 釋放 Release",
           "keywords": ["鬆綁負荷", "情緒代謝", "放下執著", "完成回收"],
           "actions": ["做一次『寫了就撕/燒』釋放書寫（2–3 段）",
                       "身體掃描，對緊繃部位做 60 秒放鬆",
                       "將一件拖延小事今天完成並打勾"]},
    "S3": {"name": "S3 信任 Trust",
           "keywords": ["允許發生", "對齊意圖", "資源感", "安全感"],
           "actions": ["用『我允許…』造句 3 句（對應今日焦點）",
                       "回顧 1 次被支持的證據，寫下為何可複製",
                       "今天主動請求一次幫助（小範圍即可）"]},
    "S4": {"name": "S4 行動 Action",
           "keywords": ["最小步驟", "可驗證", "節奏", "執行力"],
           "actions": ["把目標拆成 10 分鐘可完成的一步，現在就做",
                       "設定今日 3 件 MIT",
                       "完成後『公開回報』給可信任對象"]},
    "S5": {"name": "S5 流動 Flow",
           "keywords": ["專注", "回饋循環", "韌性", "迭代"],
           "actions": ["把卡點→調整 1 個微策略（A/B 嘗試）",
                       "25 分鐘番茄鐘全程專注",
                       "記錄 1 個有效回饋，明天沿用"]},
    "S6": {"name": "S6 共鳴 Resonance",
           "keywords": ["連結", "價值感", "貢獻", "擴散"],
           "actions": ["分享一個小成果或洞見到社群／朋友",
                       "邀請 1 人給具體回饋（3 句具體描述）",
                       "主動建立一個合作可能（發出一則邀請）"]},
    "S7": {"name": "S7 整合 Integration",
           "keywords": ["總結經驗", "固化習慣", "結構化", "長期化"],
           "actions": ["用 5 句話摘要本週 3 件學到＋1 改進",
                       "把有效步驟寫成 Checklist 並固定到行程",
                       "為下個週期設定一個可衡量指標（KPI）"]},
}
TRANSITION_META = {
    "T1": {"label": "S1→S2 臨界（覺察→釋放）",
           "actions": ["把『我觀察到…』改寫成『我願意放下…』×3",
                       "情緒書寫→身體放鬆收尾（頸肩／腹部）"]},
    "T2": {"label": "S2→S3 臨界（釋放→信任）",
           "actions": ["列出 3 個現有資源（人／物／技能）",
                       "寫 1 段：若一切對我有利，今天我允許什麼？"]},
    "T3": {"label": "S3→S4 臨界（信任→行動）",
           "actions": ["產出『最小可行步驟』並在 10 分鐘內啟動",
                       "預約 1 個『行動時段』，行前只做準備清單"]},
    "T4": {"label": "S4→S5 臨界（行動→流動）",
           "actions": ["把今日行動回饋記錄並做 1 次微調",
                       "建立 25 分鐘專注儀式，結束回顧 2 分鐘"]},
    "T5": {"label": "S5→S6 臨界（流動→共鳴）",
           "actions": ["公開分享 1 個進展／案例，索取具體回饋",
                       "辨識最被共鳴的價值，明天主打該元素"]},
    "T6": {"label": "S6→S7 臨界（共鳴→整合）",
           "actions": ["把有效做法寫成 SOP／Checklist",
                       "選一個可持續節奏（週／月）放進行事曆"]},
    "T7": {"label": "S7→S1 臨界（整合→新覺察）",
           "actions": ["本週回顧 3 句＋下一輪新意圖 1 句",
                       "挑選 1 個欲精進的指標，設置觀測方式"]},
}

# ============ 三、核心計分 ============
def compute_enervi7_scores(answers, penalty=False, tau=4.0, delta=0.3):
    Q = [float(answers.get(f"Q{i}", 0)) for i in range(1, 8)]
    T = [float(answers.get(f"T{i}", 0)) for i in range(1, 8)]
    wQ, wPrev, wNext = 0.60, 0.20, 0.20

    stages_raw = []
    for i in range(7):
        prev_t = T[(i - 1) % 7]
        next_t = T[i]
        val = wQ * Q[i] + wPrev * prev_t + wNext * next_t
        if penalty:
            if prev_t < tau: val -= delta
            if next_t < tau: val -= delta
            val = max(0.0, val)
        stages_raw.append(val)

    stages = [round(v * 10, 1) for v in stages_raw]   # 0..100
    transitions = [round(t * 10, 1) for t in T]       # 0..100

    stages_dict = {f"S{i+1}": stages[i] for i in range(7)}
    transitions_dict = {f"T{i+1}": transitions[i] for i in range(7)}
    dominant_idx = max(range(7), key=lambda i: stages[i])
    bottleneck_sorted = sorted(range(7), key=lambda i: transitions[i])[:2]

    return {
        "stages": stages_dict,
        "transitions": transitions_dict,
        "dominant_stage": f"S{dominant_idx+1}",
        "bottleneck_transitions": [f"T{i+1}" for i in bottleneck_sorted]
    }

# ============ 四、UI：表單（一鍵提交、立即出圖） ============
st.title("Enervi7 量測（Streamlit 版）")
st.caption("填寫 14 題（0–10）。按「開始測驗」後立即顯示雷達圖、分數與瓶頸摘要。下方恆常顯示七階關鍵字／行動建議。")

with st.form("enervi7_form", clear_on_submit=False):
    st.subheader("七階題 Q1–Q7")
    Q_vals = {}
    for i in range(1, 8):
        key = f"Q{i}"
        Q_vals[key] = st.slider(Q_TEXTS[key], min_value=0, max_value=10, value=5, step=1)

    st.subheader("七個轉換 T1–T7")
    T_vals = {}
    for i in range(1, 8):
        key = f"T{i}"
        T_vals[key] = st.slider(T_TEXTS[key], min_value=0, max_value=10, value=5, step=1)

    st.divider()
    c1, c2, c3 = st.columns([1,1,2])
    with c1:
        use_penalty = st.checkbox("加強卡關顯示（低轉換會小幅拉低相鄰階段）",
                                  value=st.session_state.get("use_penalty", False))
    with c2:
        tau = st.number_input("門檻 τ（0..10）", 0.0, 10.0, float(st.session_state.get("tau", 4.0)), 0.1)
    with c3:
        delta = st.number_input("強度 δ（0..2）", 0.0, 2.0, float(st.session_state.get("delta", 0.3)), 0.1)

    submitted = st.form_submit_button("開始測驗", use_container_width=True)

# 記住參數
st.session_state["use_penalty"] = use_penalty
st.session_state["tau"] = tau
st.session_state["delta"] = delta

# 計算（每次提交覆寫結果）
if submitted:
    payload = {**Q_vals, **T_vals}
    st.session_state["result"] = compute_enervi7_scores(
        payload, penalty=use_penalty, tau=tau, delta=delta
    )

# ============ 五、結果顯示 ============
if "result" in st.session_state:
    result = st.session_state["result"]

    # 雷達圖
    st.subheader("雷達圖")
    labels = [STAGE_META[f"S{i+1}"]["name"] for i in range(7)]
    vals = [result["stages"][f"S{i+1}"] for i in range(7)]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=vals + [vals[0]], theta=labels + [labels[0]],
        fill="toself", name="Enervi7"
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False, margin=dict(t=10, r=10, b=10, l=10), height=440
    )
    st.plotly_chart(fig, use_container_width=True)

    # 七階/轉換分數表
    cL, cR = st.columns(2)
    with cL:
        st.markdown("### 七階分數（0–100）")
        for i in range(1, 8):
            v = result["stages"][f"S{i}"]
            level = "低" if v < 40 else ("中" if v < 70 else "高")
            st.write(f"**{STAGE_META[f'S{i}']['name']}**：{v}（{level}）")
    with cR:
        st.markdown("### 轉換分數（0–100）")
        for i in range(1, 8):
            v = result["transitions"][f"T{i}"]
            level = "低" if v < 40 else ("中" if v < 70 else "高")
            st.write(f"**{TRANSITION_META[f'T{i}']['label']}**：{v}（{level}）")

    # 摘要
    s_dom = result["dominant_stage"]
    b1, b2 = result["bottleneck_transitions"]
    st.info(
        f"主導階段：**{STAGE_META[s_dom]['name']}**｜"
        f"瓶頸：**{TRANSITION_META[b1]['label']}**；次瓶頸：**{TRANSITION_META[b2]['label']}**"
    )

# ============ 六、七階關鍵字＋行動建議（恆常顯示） ============
st.markdown("---")
st.header("七階關鍵字＋行動建議")
cols = st.columns(3)
for idx, sid in enumerate(["S1","S2","S3","S4","S5","S6","S7"]):
    with cols[idx % 3]:
        meta = STAGE_META[sid]
        st.subheader(meta["name"])
        st.caption("關鍵字")
        st.write("、".join(meta["keywords"]))
        st.caption("行動建議")
        for act in meta["actions"]:
            st.write("•", act)

# ============ 七、瓶頸轉換建議（說明） ============
with st.expander("瓶頸轉換的解卡建議（說明）"):
    st.write("測驗後系統會自動找出分數最低的兩個轉換（T1–T7），並顯示對應的行動。")
    for tid, meta in TRANSITION_META.items():
        st.write(f"**{meta['label']}**")
        for act in meta["actions"]:
            st.write("•", act)