import os
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# =============================
# 字型設定（根目錄）
# =============================
FONT_FILE = "NotoSansTC-VariableFont_wght.ttf"
HAS_FONT = os.path.exists(FONT_FILE)

# Matplotlib 字型
try:
    if HAS_FONT:
        font_manager.fontManager.addfont(FONT_FILE)
        plt.rcParams["font.family"] = "Noto Sans TC"
        plt.rcParams["font.sans-serif"] = ["Noto Sans TC", "NotoSansTC", "Arial Unicode MS"]
        plt.rcParams["axes.unicode_minus"] = False
    else:
        st.warning(f"⚠️ 找不到中文字型，請確認專案根目錄有 {FONT_FILE}")
except Exception as e:
    st.warning(f"⚠️ 字型套用失敗：{e}")

# ReportLab 字型
try:
    PDF_FONT_NAME = "NotoSansTC"
    if HAS_FONT:
        pdfmetrics.registerFont(TTFont(PDF_FONT_NAME, FONT_FILE))
    else:
        PDF_FONT_NAME = "Helvetica"
except Exception as e:
    PDF_FONT_NAME = "Helvetica"
    st.warning(f"⚠️ PDF 字型註冊失敗：{e}")


# =============================
# Streamlit App
# =============================

st.title("✨ 七階能量圖")

st.write("輸入或調整每一階的能量值（0–100），即時生成雷達圖，並可下載 PNG/PDF。")

# 自訂圖表標題
chart_title = st.text_input("圖表標題（可自訂）", "我的能量狀態")

# 能量層級
levels = [
    "Level 0 覺知啟動",
    "Level 1 情緒穩定",
    "Level 2 行動啟動",
    "Level 3 表達流動",
    "Level 4 心輪敞開",
    "Level 5 直覺啟示",
    "Level 6 靈性合一"
]

values = []
for level in levels:
    val = st.slider(level, 0, 100, 50)
    values.append(val)

# 關閉雷達圖要回到起點
values += values[:1]

# =============================
# 畫雷達圖
# =============================
angles = np.linspace(0, 2 * np.pi, len(levels), endpoint=False).tolist()
angles += angles[:1]

fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(levels, fontsize=12)

ax.plot(angles, values, linewidth=2, linestyle="solid")
ax.fill(angles, values, alpha=0.3)

ax.set_title(chart_title, size=16, pad=20)

st.pyplot(fig)


# =============================
# 下載 PNG
# =============================
buf = BytesIO()
fig.savefig(buf, format="png", bbox_inches="tight")
st.download_button(
    label="📥 下載 PNG",
    data=buf.getvalue(),
    file_name="energy_chart.png",
    mime="image/png"
)


# =============================
# 下載 PDF
# =============================
pdf_buf = BytesIO()
c = canvas.Canvas(pdf_buf, pagesize=A4)

width, height = A4
c.setFont(PDF_FONT_NAME, 16)
c.drawString(50, height - 50, chart_title)

c.setFont(PDF_FONT_NAME, 12)
y = height - 100
for i, (lvl, val) in enumerate(zip(levels, values[:-1])):
    c.drawString(50, y - i*20, f"{lvl}: {val}")

# 插入圖片
img_buf = BytesIO()
fig.savefig(img_buf, format="png", bbox_inches="tight")
c.drawImage(BytesIO(img_buf.getvalue()), 50, 200, width=500, preserveAspectRatio=True, mask='auto')

c.save()

st.download_button(
    label="📥 下載 PDF",
    data=pdf_buf.getvalue(),
    file_name="energy_chart.pdf",
    mime="application/pdf"
)