# app.py — Enervi 7 Radar (ZH) 完整版（含關鍵字/行動建議）

import io
import math
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd  # ← 新增：用表格呈現

# ---------- 參數 ----------
TITLE = "✨ 七階能量圖"
FONT_PATH_DEFAULT = "fonts/NotoSansTC-VariableFont_wght.ttf"  # 請放在 fonts/ 內
LEVEL_LABELS = [
    "Level 0 覺知啟動",
    "Level 1 情緒穩定",
    "Level 2 行動啟動",
    "Level 3 共振合作",
    "Level 4 創造成果",
    "Level 5 靈性統合",
    "Level 6 全頻創造",
]
PLOT_COLOR = "#2E64FE"
FILL_ALPHA = 0.25

# 七階對照：情緒關鍵詞 / 行動特徵 / 突破關鍵（對應你給的圖片內容）
LEVEL_META = [
    {"階段": LEVEL_LABELS[0], "情緒關鍵詞": "清明、觀察", "行動特徵": "開始注意自己的情緒與行動模式", "突破關鍵": "建立「覺察日誌」"},
    {"階段": LEVEL_LABELS[1], "情緒關鍵詞": "平衡、包容", "行動特徵": "減少情緒波動、情緒不干擾判斷", "突破關鍵": "呼吸與釋放練習"},
    {"階段": LEVEL_LABELS[2], "情緒關鍵詞": "決心、推進", "行動特徵": "從構想到行動的時間縮短", "突破關鍵": "小步快跑法則"},
    {"階段": LEVEL_LABELS[3], "情緒關鍵詞": "連結、信任", "行動特徵": "主動尋求合作與資源", "突破關鍵": "開啟互助專案"},
    {"階段": LEVEL_LABELS[4], "情緒關鍵詞": "豐盛、主權", "行動特徵": "把想法落地為具體成果", "突破關鍵": "行動＋回饋循環"},
    {"階段": LEVEL_LABELS[5], "情緒關鍵詞": "洞察、整合", "行動特徵": "看見全局、跨領域連結", "突破關鍵": "內外合一策略"},
    {"階段": LEVEL_LABELS[6], "情緒關鍵詞": "無限、共創", "行動特徵": "能量可自由轉換為財富／成果", "突破關鍵": "成果倍增法"},
]

# ---------- 字體載入 ----------
font_prop = None
font_ok = False
try:
    font_prop = fm.FontProperties(fname=FONT_PATH_DEFAULT)
    _ = font_prop.get_name()
    font_ok = True
except Exception:
    st.warning(f"找不到中文字型，請確認 **{FONT_PATH_DEFAULT}** 是否存在。")
plt.rcParams["axes.unicode_minus"] = False
if font_ok:
    plt.rcParams["font.family"] = font_prop.get_name()

# ---------- UI ----------
st.set_page_config(page_title="Enervi 7 Radar — ZH", page_icon="🌟", layout="centered")
st.title(TITLE)
st.caption("輸入或調整每一階的能量值（0–100），即時生成雷達圖，並可下載 PNG / PDF。")

chart_title = st.text_input("圖表標題（可自訂）", value="我的能量狀態")

presets = {
    "—": [50, 50, 50, 50, 50, 50, 50],
    "成長模式": [40, 55, 65, 60, 58, 52, 48],
    "高動能": [55, 60, 85, 70, 62, 50, 45],
    "靜心整合": [60, 70, 45, 55, 65, 75, 80],
}
preset_name = st.selectbox("快速套用範例", list(presets.keys()))
values = presets[preset_name].copy()

for i, label in enumerate(LEVEL_LABELS):
    values[i] = st.slider(label, 0, 100, int(values[i]), 1)

# ---------- 畫雷達圖 ----------
def radar_chart(vals, labels, title):
    N = len(vals)
    angles = [n / float(N) * 2 * math.pi for n in range(N)]
    angles += angles[:1]
    vals = vals + vals[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.set_theta_offset(math.pi / 2)
    ax.set_theta_direction(-1)

    ax.set_xticks(angles[:-1])
    if font_ok:
        ax.set_xticklabels(labels, fontproperties=font_prop)
        ax.set_title(title, fontproperties=font_prop, fontsize=18, pad=14)
    else:
        ax.set_xticklabels(labels)
        ax.set_title(title, fontsize=18, pad=14)

    ax.set_rlabel_position(0)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(["20", "40", "60", "80", "100"])

    ax.plot(angles, vals, color=PLOT_COLOR, linewidth=2)
    ax.fill(angles, vals, color=PLOT_COLOR, alpha=FILL_ALPHA)

    fig.tight_layout()
    return fig

fig = radar_chart(values, LEVEL_LABELS, chart_title)
st.pyplot(fig, use_container_width=True)

# ---------- 匯出：PNG ----------
png_buf = io.BytesIO()
fig.savefig(png_buf, format="png", dpi=300, bbox_inches="tight")
png_buf.seek(0)
st.download_button("⬇️ 下載 PNG 圖檔", png_buf, file_name="enervi7_radar.png", mime="image/png")

# ---------- 匯出：PDF（ImageReader 解法） ----------
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.utils import ImageReader

    pdf_buf = io.BytesIO()
    c = canvas.Canvas(pdf_buf, pagesize=A4)

    png_buf_for_pdf = io.BytesIO(png_buf.getvalue())
    img = ImageReader(png_buf_for_pdf)

    page_w, page_h = A4
    margin = 36
    img_w = page_w - margin * 2
    img_h = img_w
    x = margin
    y = page_h - margin - img_h

    c.setTitle("Enervi 7 Radar — ZH")
    c.drawString(margin, page_h - margin + 6, "Enervi 7 Radar — ZH")
    c.drawImage(img, x, y, width=img_w, height=img_h, preserveAspectRatio=True, mask='auto')
    c.showPage()
    c.save()
    pdf_buf.seek(0)

    st.download_button("⬇️ 下載 PDF 報表", pdf_buf, file_name="enervi7_radar.pdf", mime="application/pdf")
except Exception:
    st.info("若需要下載 PDF，請在 `requirements.txt` 中加入：`reportlab`。")

# ---------- 七階關鍵字／行動建議 ----------
st.markdown("### 🔎 七階關鍵字／行動建議")
# 表格
df = pd.DataFrame(LEVEL_META)
st.dataframe(df, use_container_width=True, hide_index=True)

# 聚焦建議：找出 1–2 個最低分
vals_np = np.array(values)
rank_idx = np.argsort(vals_np)  # 由低到高
focus_idxs = rank_idx[:2] if len(values) >= 2 else rank_idx[:1]

st.markdown("### ✨ 本週聚焦微行動建議")
for idx in focus_idxs:
    row = LEVEL_META[idx]
    score = values[idx]
    st.markdown(
        f"- **{row['階段']}**（目前 {score}）｜情緒關鍵詞：*{row['情緒關鍵詞']}* → **突破關鍵：{row['突破關鍵']}**  \n"
        f"  小提醒：{row['行動特徵']}。"
    )

# ---------- 說明 ----------
with st.expander("ℹ️ 使用說明 / 疑難排解"):
    st.markdown(
        """
**若中文變框框或亂碼：**
1. 在 repo 建立 `fonts/` 資料夾  
2. 把 `NotoSansTC-VariableFont_wght.ttf` 放進 `fonts/`  
3. 重新部署即可

**想改顏色或字體大小：**  
在檔頭的 `PLOT_COLOR` / `FILL_ALPHA` 與 `radar_chart()` 內 `fontsize` 自行調整。

**表格內容客製：**  
修改 `LEVEL_META` 裡各階段的「情緒關鍵詞／行動特徵／突破關鍵」即可。
"""
    )