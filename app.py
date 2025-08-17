import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Enervi 7 Radar — MVP", page_icon="✨", layout="centered")
st.title("Enervi 7 Radar — MVP")
st.caption("輸入 7 個分數（0–100），即時生成雷達圖，並可下載 PNG。")

# ===== 參數與預設 =====
labels = ["Root", "Sacral", "Solar", "Heart", "Throat", "Third Eye", "Crown"]

# 快速套用範例：你可依需求再增/改
PRESETS = {
    "—": [50, 50, 50, 50, 50, 50, 50],
    "Balanced（均衡）": [60, 60, 60, 60, 60, 60, 60],
    "Grounded（紮根強）": [80, 55, 60, 60, 55, 50, 50],      # Root 高
    "Open Heart（心中心開）": [45, 55, 60, 85, 60, 55, 55],  # Heart 高
    "Visionary（願景清晰）": [45, 50, 55, 60, 65, 85, 80],    # Third Eye/Crown 高
    "Willpower（行動與意志）": [55, 50, 85, 60, 65, 55, 50],  # Solar/Throat 高
}

# 顯示標題輸入
title = st.text_input("圖表標題", "Enervi 7 Energy Geometry")

# 範例下拉
preset_name = st.selectbox("快速套用範例", list(PRESETS.keys()))
preset_values = PRESETS[preset_name]

# ===== 數值輸入 =====
scores = []
for i, lab in enumerate(labels):
    default = int(preset_values[i]) if preset_values else 50
    val = st.slider(lab, 0, 100, default, 1)
    scores.append(val)

scores = np.array(scores, dtype=float)

# ===== 雷達圖繪製 =====
def draw_radar(title_text: str, cats: list[str], vals: np.ndarray):
    # 封閉曲線用：頭尾補一點
    categories = cats + [cats[0]]
    values = np.append(vals, vals[0])

    angles = np.linspace(0, 2*np.pi, len(categories), endpoint=True)

    fig = plt.figure(figsize=(6, 6))
    ax = plt.subplot(111, polar=True)
    ax.set_theta_offset(np.pi / 2)   # 讓第一軸在上方
    ax.set_theta_direction(-1)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(cats, fontsize=11)

    ax.set_rlabel_position(0)
    ax.set_yticks([25, 50, 75, 100])
    ax.set_yticklabels(["25", "50", "75", "100"], fontsize=9)
    ax.set_ylim(0, 100)

    # 底色淡圈（不指定顏色，讓使用者主題決定）
    ax.plot(angles, values, linewidth=2)
    ax.fill(angles, values, alpha=0.15)

    ax.set_title(title_text, fontsize=16, pad=20)
    st.pyplot(fig)
    return fig

fig = draw_radar(title, labels, scores)

# 下載圖檔
import io
buf = io.BytesIO()
fig.savefig(buf, format="png", dpi=200, bbox_inches="tight")
st.download_button("⬇️ 下載 PNG", data=buf.getvalue(), file_name="enervi7_radar.png", mime="image/png")

# ===== 詩意能量解讀 =====
st.subheader("🔮 能量解讀（MVP）")

def interpret(labels, vals):
    tips = []
    arr = np.array(vals, dtype=float)

    # 找最高/最低
    hi_idx = int(np.argmax(arr))
    lo_idx = int(np.argmin(arr))
    hi = labels[hi_idx]; lo = labels[lo_idx]

    # 基本敘述
    tips.append(f"今天最亮的面向是 **{hi}**，值得善用它帶來的順流。")
    tips.append(f"目前較需要照顧的是 **{lo}**，可以安排一個溫柔的小行動。")

    # 區域性建議（你可自由調整）
    guide = {
        "Root": "做 3 次深呼吸＋赤足接地 5 分鐘。",
        "Sacral": "安排一個小小的愉悅時刻，讓身體說話。",
        "Solar": "完成一件具體的小目標（2–10 分鐘可完成）。",
        "Heart": "寫下 3 件感恩，或向一位朋友送出關懷訊息。",
        "Throat": "說一句真實的話，或寫 3 句誠實日記。",
        "Third Eye": "靜心 5 分鐘，讓圖像/直覺浮現。",
        "Crown": "把注意力放在頭頂上方 10 公分，感受被支持。",
    }
    tips.append(f"針對 **{lo}** 的微行動建議：{guide.get(lo, '給自己一點時間與空間。')}")

    # 均衡度
    spread = arr.max() - arr.min()
    if spread <= 15:
        tips.append("整體相當 **均衡**，可以嘗試提升某一軸，探索更多可能性。")
    elif spread <= 35:
        tips.append("目前呈現 **自然起伏**，順著能量做事，會更省力。")
    else:
        tips.append("差距較大，建議今天選一個弱項做 **2–5 分鐘** 小練習即可。")

    # 主題性辨識（示例）
    if arr[labels.index("Heart")] >= 75:
        tips.append("♥ 心能量旺盛：適合連結、分享、與人合作。")
    if arr[labels.index("Root")] < 45 and arr[labels.index("Third Eye")] >= 70:
        tips.append("👣 先紮根再遠望：在願景之前，把身體安頓好。")

    return tips

for line in interpret(labels, scores):
    st.write("• " + line)

st.caption("提示僅供參考，請以你的直覺與身體感受為主。")