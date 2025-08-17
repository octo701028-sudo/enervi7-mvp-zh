import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
import tempfile
import datetime
import os

# -------------------------------------------------
# 標籤：七階能量表
# -------------------------------------------------
LABELS = [
    "Level 0 覺知啟動",
    "Level 1 情緒穩定",
    "Level 2 行動啟動",
    "Level 3 共振合作",
    "Level 4 創造顯化",
    "Level 5 靈性統合",
    "Level 6 全頻創造",
]

# 範例組合
PRESETS = {
    "—": [50] * 7,
    "均衡（60）": [60] * 7,
    "Level 0~2 偏低": [40, 45, 45, 55, 55, 60, 60],
    "Level 2 行動高": [50, 50, 85, 60, 65, 55, 50],
    "Level 4 創造高": [45, 55, 60, 65, 60, 55, 85],
    "Level 6 全頻高": [55, 60, 65, 70, 70, 80, 90],
}

# 微行動建議
MICRO = {
    "Level 0 覺知啟動": "建立『覺察日誌』，三次深呼吸，寫下當下的情緒與念頭。",
    "Level 1 情緒穩定": "做 2 分鐘緩慢吐氣或身體掃描，讓情緒波動降一格。",
    "Level 2 行動啟動": "小步快跑：5–10 分鐘完成一件可見的小任務。",
    "Level 3 共振合作": "主動聯繫 1 位夥伴，交換資源或約一次對話。",
    "Level 4 創造顯化": "定義『下一個可見成果』，做->收回饋->再調整。",
    "Level 5 靈性統合": "花 10 分鐘盤點全局，整合 1 個跨領域連結。",
    "Level 6 全頻創造": "設定一個共創/倍增行動，讓成果可被複製與傳遞。",
}

# -------------------------------------------------
# Streamlit 主介面
# -------------------------------------------------
st.set_page_config(page_title="七階能量表", layout="centered")

st.title("🔮 七階能量表")
st.write("調整每一階的能量值（0–100），觀察整體狀態並獲取微行動建議。")

# 左側：範例組合
preset = st.sidebar.selectbox("快速套用範例", list(PRESETS.keys()))
values = PRESETS[preset].copy()

# 左側：自訂滑桿
st.sidebar.header("自訂能量值")
for i, label in enumerate(LABELS):
    values[i] = st.sidebar.slider(label, 0, 100, values[i], 1)

# -------------------------------------------------
# 繪製雷達圖
# -------------------------------------------------
angles = np.linspace(0, 2 * np.pi, len(LABELS), endpoint=False).tolist()
values_circular = values + values[:1]
angles_circular = angles + angles[:1]

fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
ax.plot(angles_circular, values_circular, "o-", linewidth=2)
ax.fill(angles_circular, values_circular, alpha=0.25)
ax.set_thetagrids(np.degrees(angles), LABELS, fontsize=12)
ax.set_ylim(0, 100)
ax.set_title("七階能量雷達圖", size=16, pad=20)

st.pyplot(fig)

# -------------------------------------------------
# 微行動建議
# -------------------------------------------------
st.header("✨ 微行動建議")

tips = []
for label, val in zip(LABELS, values):
    if val < 50:
        tips.append(f"【{label}】較低 → {MICRO[label]}")
    elif val > 80:
        tips.append(f"【{label}】能量充沛 → 嘗試擴散或分享此能量。")

if not tips:
    st.success("目前能量均衡，持續保持就好 🌈")
else:
    for t in tips:
        st.write("- " + t)

# -------------------------------------------------
# 下載 PDF 報告
# -------------------------------------------------
def create_pdf(values, tips, fig_path):
    tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(tmpfile.name, pagesize=A4)
    styles = getSampleStyleSheet()
    flow = []

    flow.append(Paragraph("🔮 七階能量表 報告", styles["Title"]))
    flow.append(Paragraph(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), styles["Normal"]))
    flow.append(Spacer(1, 12))

    # 數據
    for label, val in zip(LABELS, values):
        flow.append(Paragraph(f"{label}: {val}", styles["Normal"]))
    flow.append(Spacer(1, 12))

    # 插入雷達圖
    flow.append(Image(fig_path, width=400, height=400))
    flow.append(Spacer(1, 12))

    # 建議
    flow.append(Paragraph("✨ 微行動建議", styles["Heading2"]))
    if tips:
        for t in tips:
            flow.append(Paragraph("- " + t, styles["Normal"]))
    else:
        flow.append(Paragraph("目前能量均衡，持續保持就好 🌈", styles["Normal"]))

    doc.build(flow)
    return tmpfile.name

# 將雷達圖暫存為 PNG
tmp_img = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
fig.savefig(tmp_img.name)

if st.button("📥 下載 PDF 報告"):
    pdf_path = create_pdf(values, tips, tmp_img.name)
    with open(pdf_path, "rb") as f:
        st.download_button("下載完成報告", f, file_name="energy_report.pdf")