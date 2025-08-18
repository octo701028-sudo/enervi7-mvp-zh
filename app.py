import streamlit as st
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.font_manager import FontProperties
import numpy as np
import os, glob, io

# ============= 字型自動偵測（避免中文變口口） =============
FONT_DIR = "fonts"
PREFERRED = [
    "NotoSansTC-VariableFont_wght.ttf",
    "NotoSansTC-Regular.ttf",
    "NotoSansTC-Medium.ttf",
    "NotoSansTC-Bold.ttf",
    "NotoSansTC-Light.ttf",
    "NotoSansTC-ExtraLight.ttf",
]

def find_tc_font():
    for name in PREFERRED:
        p = os.path.join(FONT_DIR, name)
        if os.path.exists(p): return p
    matches = glob.glob(os.path.join(FONT_DIR, "NotoSansTC*.ttf"))
    return matches[0] if matches else None

tc_font_path = find_tc_font()
if tc_font_path:
    try:
        mpl.font_manager.fontManager.addfont(tc_font_path)
    except Exception:
        pass
    fp = FontProperties(fname=tc_font_path)
    mpl.rcParams["font.family"] = fp.get_name()
    mpl.rcParams["axes.unicode_minus"] = False
else:
    st.warning("⚠️ 找不到中文字型，請把任一 `NotoSansTC*.ttf` 放到 `fonts/` 資料夾。")

# ============= 七階定義（名稱、關鍵字、行動特徵、突破關鍵） =============
LEVELS = [
    {
        "name": "Level 0 覺知啟動",
        "kw": "清明、觀察",
        "feature": "開始注意自己的情緒與行動模式",
        "break": "建立「覺察日誌」",
    },
    {
        "name": "Level 1 情緒穩定",
        "kw": "平衡、包容",
        "feature": "減少情緒波動，情緒不干擾判斷",
        "break": "呼吸與釋放練習",
    },
    {
        "name": "Level 2 行動啟動",
        "kw": "決心、推進",
        "feature": "從構想到行動的時間縮短",
        "break": "小步快跑法則",
    },
    {
        "name": "Level 3 關係互動",
        "kw": "連結、信任",
        "feature": "主動尋求合作與資源",
        "break": "開啟互助專案",
    },
    {
        "name": "Level 4 表達流動",
        "kw": "豐盛、主權",
        "feature": "把想法落地為具體成果",
        "break": "行動＋回饋循環",
    },
    {
        "name": "Level 5 直覺開展",
        "kw": "洞察、整合",
        "feature": "看見全局、跨領域連結",
        "break": "內外合一策略",
    },
    {
        "name": "Level 6 靈性覺醒",
        "kw": "無限、共創",
        "feature": "能量可自由轉換為財富／成果",
        "break": "成果倍增法",
    },
]

def suggest_line(score: int, breakthrough: str) -> str:
    if score < 40:
        return f"起步建議：先做「{breakthrough}」，每天 5–10 分鐘建立慣性。"
    elif score < 70:
        return f"優化建議：持續「{breakthrough}」，再加入每週一次回顧調整。"
    else:
        return f"加速建議：把「{breakthrough}」制度化，擴大到團隊／夥伴共作。"

# ============= 介面 =============
st.title("✨ 七階能量圖")
st.markdown("輸入或調整每一階的能量值（0–100），即時生成雷達圖，並可下載 PNG / PDF。")

chart_title = st.text_input("圖表標題（可自訂）", "我的能量狀態")

scores = []
for L in LEVELS:
    v = st.slider(L["name"], 0, 100, 50)
    scores.append(v)

# ============= 雷達圖 =============
labels = [L["name"] for L in LEVELS]
angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
vals = scores + scores[:1]
angs = angles + angles[:1]

fig, ax = plt.subplots(figsize=(6.5, 6.5), subplot_kw=dict(polar=True))
ax.plot(angs, vals, "o-", linewidth=2, label="能量值")
ax.fill(angs, vals, alpha=0.25)
ax.set_xticks(angles)
ax.set_xticklabels(labels, fontproperties=(FontProperties(fname=tc_font_path) if tc_font_path else None))
ax.set_yticks([20, 40, 60, 80, 100])
ax.set_ylim(0, 100)
plt.title(chart_title, size=16, fontproperties=(FontProperties(fname=tc_font_path) if tc_font_path else None))
st.pyplot(fig)

# ============= 下載按鈕 =============
buf_png = io.BytesIO()
fig.savefig(buf_png, format="png", bbox_inches="tight")
st.download_button("⬇️ 下載 PNG", data=buf_png.getvalue(), file_name="energy_chart.png", mime="image/png")

buf_pdf = io.BytesIO()
fig.savefig(buf_pdf, format="pdf", bbox_inches="tight")
st.download_button("⬇️ 下載 PDF", data=buf_pdf.getvalue(), file_name="energy_chart.pdf", mime="application/pdf")

# ============= 圖下方：七階關鍵字／行動建議 =============
st.markdown("## ✨ 微行動建議")
for i, L in enumerate(LEVELS):
    s = scores[i]
    with st.expander(f"{L['name']}｜分數：{s}"):
        st.markdown(f"**情緒關鍵詞**：{L['kw']}")
        st.markdown(f"**行動特徵**：{L['feature']}")
        st.markdown(f"**突破關鍵**：{L['break']}")
        st.info(suggest_line(s, L["break"]))