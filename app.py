# app.py — Enervi 7 Radar 彩色能量環 + 等級解讀（白底）
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Enervi 7 Radar — 彩色能量環", page_icon="✨", layout="centered")
st.title("Enervi 7 Radar — MVP")
st.caption("輸入 7 個分數（0–100），即時生成白底彩色能量環雷達圖，並附等級解讀。")

# 7 軸
LABELS = ["Root", "Sacral", "Solar", "Heart", "Throat", "Third Eye", "Crown"]

# 快速範例
PRESETS = {
    "—": [50]*7,
    "均衡（60）": [60]*7,
    "Grounded（Root 高）": [80, 60, 60, 55, 55, 50, 50],
    "Open Heart（Heart 高）": [45, 55, 60, 85, 60, 55, 55],
    "Visionary（上三輪高）": [45, 50, 55, 60, 65, 85, 80],
    "Willpower（Solar/Throat 高）": [55, 50, 85, 60, 70, 55, 50],
}

# 七階能量色（由內而外的同心圓）
LEVELS = [
    {"name": "Level 0  覺知啟動", "color": "#FFFFFF", "kw": "清明、觀察", "act": "注意自己的情緒與行動模式", "key": "建立『覺察日誌』"},
    {"name": "Level 1  情緒穩定", "color": "#3CB371", "kw": "平衡、包容", "act": "減少情緒波動，不讓情緒干擾判斷", "key": "呼吸與釋放練習"},
    {"name": "Level 2  行動啟動", "color": "#FFD700", "kw": "決心、推進", "act": "從構想到行動的時間縮短", "key": "小步快跑法則"},
    {"name": "Level 3  共振合作", "color": "#1E90FF", "kw": "連結、信任", "act": "主動尋求合作與資源", "key": "開啟互助專案"},
    {"name": "Level 4  創造顯化", "color": "#DAA520", "kw": "豐盛、主權", "act": "把想法落地為具體成果", "key": "行動＋回饋循環"},
    {"name": "Level 5  靈性統合", "color": "#800080", "kw": "洞察、整合", "act": "看見全局、跨領域連結", "key": "內外合一策略"},
    {"name": "Level 6  全頻創造", "color": "#9B30FF", "kw": "無限、共創", "act": "能量可自由轉換為財富/成果", "key": "成果倍增法"},
]
# 讓最外圈再加一圈金色光暈（依你的表格：紫金混合）
OUTER_GLOW = "#FFD700"

# 文字輸入
title = st.text_input("圖表標題", "Enervi 7 Energy Geometry — Demo")
preset = st.selectbox("快速套用範例", list(PRESETS.keys()))
preset_vals = PRESETS[preset]

# 分數輸入
scores = []
for i, lab in enumerate(LABELS):
    default = int(preset_vals[i])
    scores.append(st.slider(lab, 0, 100, default, 1))
scores = np.array(scores, dtype=float)

def draw_colorrings_radar(title_text, labels, vals):
    # 收尾相接
    cats = labels + [labels[0]]
    values = np.append(vals, vals[0])

    # 極座標
    angles = np.linspace(0, 2*np.pi, len(cats), endpoint=True)
    fig = plt.figure(figsize=(7, 7))
    ax = plt.subplot(111, polar=True)

    # 白底
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    # 角度與刻度
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=12, color="black")
    ax.set_rlabel_position(0)
    ax.set_yticks([25, 50, 75, 100])
    ax.set_yticklabels(["25", "50", "75", "100"], fontsize=9, color="gray")
    ax.set_ylim(0, 100)

    # 灰點線（格線）
    ax.grid(color="#DDDDDD", linestyle="--", linewidth=0.6, alpha=0.7)

    # 外框
    for spine in ax.spines.values():
        spine.set_color("black")
        spine.set_linewidth(1.2)

    # ---- 由內而外畫七層彩色能量環（同心圓）----
    # 用 7 等分半徑：0–100 -> 每層約 100/7
    bands = np.linspace(0, 100, 8)  # 8 個點、7 個區段
    for i in range(7):
        r0, r1 = bands[i], bands[i+1]
        # 顏色：對應 LEVELS[i]
        col = LEVELS[i]["color"]
        ax.fill_between(angles, r0, r1, color=col, alpha=0.15, zorder=0)
    # 最外一層金色光暈
    ax.fill_between(angles, 95, 100, color=OUTER_GLOW, alpha=0.10, zorder=0)

    # ---- 使用者的七邊形（海軍藍實線＋半透明填滿）----
    ax.plot(angles, values, linewidth=2.6, color="navy", zorder=5)
    ax.fill(angles, values, color="navy", alpha=0.18, zorder=4)
    ax.scatter(angles[:-1], vals, s=18, color="navy", zorder=6)

    ax.set_title(title_text, fontsize=18, pad=20, color="black")
    st.pyplot(fig)
    return fig

fig = draw_colorrings_radar(title, LABELS, scores)

# 下載圖
import io
buf = io.BytesIO()
fig.savefig(buf, format="png", dpi=240, bbox_inches="tight")
st.download_button("⬇️ 下載 PNG", data=buf.getvalue(), file_name="enervi7_radar.png", mime="image/png")

# ===== 等級解讀（依平均分數落點區間）=====
st.subheader("🔮 七階能量解讀")
avg = float(np.mean(scores))

# 0–100 均分 7 區：你可自行微調門檻
bins = np.linspace(0, 100, 8)             # 0,14.3,28.6,...,100
level_idx = int(np.digitize([avg], bins, right=True)[0])
level_idx = min(max(level_idx, 0), 6)
L = LEVELS[level_idx]

st.write(f"**平均分數**：{avg:.1f}")
st.write(f"**當下層級**：{L['name']}")
st.write(f"**情緒關鍵詞**：{L['kw']}")
st.write(f"**行動特徵**：{L['act']}")
st.write(f"**突破關鍵**：{L['key']}")

# 補充：哪一軸最高/最低，給一個微行動提示
max_i, min_i = int(np.argmax(scores)), int(np.argmin(scores))
hi, lo = LABELS[max_i], LABELS[min_i]
st.markdown("---")
st.write(f"今日最亮：**{hi}**　需要照顧：**{lo}**")
MICRO = {
    "Root": "赤足接地 3–5 分鐘，做 3 次深呼吸。",
    "Sacral": "安排一個 5 分鐘的愉悅時刻，讓身體說話。",
    "Solar": "在 5–10 分鐘內完成一件可見的小任務。",
    "Heart": "寫 3 件感恩，或向一位人發送關懷訊息。",
    "Throat": "說一句真實的話，或寫 3 句誠實日記。",
    "Third Eye": "靜坐 3–5 分鐘，觀想當日最佳畫面。",
    "Crown": "把注意放在頭頂上方 10 公分，停留 1 分鐘。",
}
st.write(f"針對 **{lo}** 的微行動建議：{MICRO.get(lo, '給自己一點時間與空間')}")

st.caption("色帶、關鍵詞與行動說明來自你提供的七階能量表；區間分界可依你的系統再微調。")