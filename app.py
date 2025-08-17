# -*- coding: utf-8 -*-
import io
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib import rcParams

# ========== 字型：放在 repo 的 fonts/ 資料夾 ==========
FONT_PATH = "fonts/NotoSansTC-VariableFont_wght.ttf"
try:
    _font = fm.FontProperties(fname=FONT_PATH)
    rcParams["font.sans-serif"] = [_font.get_name()]
    rcParams["font.family"] = "sans-serif"
    rcParams["axes.unicode_minus"] = False
except Exception:
    st.warning("⚠️ 找不到中文字型，請確認 fonts/ 內有 NotoSansTC-VariableFont_wght.ttf")
    _font = None

# ========== 頁面設定 ==========
st.set_page_config(page_title="七階能量圖", page_icon="✨", layout="centered")

st.title("✨ 七階能量圖")
st.caption("輸入或調整每一階的能量值（0–100），即時生成雷達圖，並可下載 PNG。")

# 標籤
LEVEL_LABELS = [
    "Level 0 覺知啟動",
    "Level 1 情緒穩定",
    "Level 2 行動啟動",
    "Level 3 共振合作",
    "Level 4 創造顯化",
    "Level 5 靈性統合",
    "Level 6 全頻創造",
]

# 快速範例
EXAMPLES = {
    "—": None,
    "均衡狀態（全 60）": [60]*7,
    "行動啟動（70 / 其餘 50）": [50, 50, 70, 50, 50, 50, 50],
    "創造顯化（75 / 其餘 55）": [55, 55, 55, 55, 75, 55, 55],
    "靈性統合（80 / 其餘 60）": [60, 60, 60, 60, 60, 80, 60],
}

col1, col2 = st.columns([2,1], vertical_alignment="center")
with col1:
    chart_title = st.text_input("圖表標題（可自訂）", value="我的能量狀態")
with col2:
    preset = st.selectbox("快速套用範例", list(EXAMPLES.keys()))
    if EXAMPLES[preset]:
        st.session_state["levels"] = EXAMPLES[preset]

# 輸入
default_vals = st.session_state.get("levels", [50]*7)
sliders = []
for i, label in enumerate(LEVEL_LABELS):
    val = st.slider(label, 0, 100, int(default_vals[i]))
    sliders.append(val)
st.session_state["levels"] = sliders[:]

# 畫雷達圖（白底）
def draw_radar(values, labels, title=""):
    n = len(labels)
    values = values + values[:1]
    angles = np.linspace(0, 2*np.pi, n, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6.5, 6.5), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.grid(color="#DDDDDD", linewidth=0.8)
    ax.spines["polar"].set_color("#999999")
    ax.spines["polar"].set_linewidth(1.0)

    ax.set_ylim(0, 100)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(["20", "40", "60", "80", "100"], fontsize=10, fontproperties=_font)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=11, fontproperties=_font)

    ax.plot(angles, values, color="#203A8F", linewidth=2.2, marker="o", markersize=5)
    ax.fill(angles, values, color="#203A8F", alpha=0.18)

    if title:
        ax.set_title(title, fontsize=16, pad=18, fontproperties=_font)

    plt.tight_layout()
    return fig

fig = draw_radar(sliders, LEVEL_LABELS, title=chart_title)
st.pyplot(fig, clear_figure=False)

# ====== 指標與提示 ======
arr = np.array(sliders, dtype=float)
avg = float(np.mean(arr))
mx = int(np.max(arr))
top_idx = [i for i, v in enumerate(sliders) if v == mx]
top_labels = [LEVEL_LABELS[i] for i in top_idx]

m1, m2 = st.columns(2)
with m1:
    st.metric("平均能量", f"{avg:.1f}")
with m2:
    st.metric("最高能量值", f"{mx}")

st.success("最高能量階：**{}**（{}）".format("、".join(top_labels), mx))

# 微行動建議（對最高能量階給 1 句可執行行動）
SUGGESTIONS = {
    "Level 0 覺知啟動": "建立「覺察日誌」，每天寫 3 句觀察與體感。",
    "Level 1 情緒穩定": "做 3 分鐘方塊呼吸，並為當下情緒命名一次。",
    "Level 2 行動啟動": "今天完成 1 個 10 分鐘的小步快跑任務。",
    "Level 3 共振合作": "主動向 1 位夥伴提出具體協作請求。",
    "Level 4 創造顯化": "把概念寫成 1 頁行動方案或原型草圖。",
    "Level 5 靈性統合": "安排 15 分鐘靜心，回顧『內外一致』的下一步。",
    "Level 6 全頻創造": "為成果加上 1 個放大機制（自動化/流程化/授權）。",
}

st.subheader("✨ 微行動建議")
for lbl in top_labels:
    st.write(f"• **{lbl}**：{SUGGESTIONS.get(lbl, '持續穩定輸入與輸出，保持覺察。')}")

# 下載 PNG
buf = io.BytesIO()
fig.savefig(buf, format="png", dpi=200, bbox_inches="tight", facecolor="white")
st.download_button("⬇️ 下載我的能量圖", data=buf.getvalue(),
                   file_name="七階能量圖.png", mime="image/png")