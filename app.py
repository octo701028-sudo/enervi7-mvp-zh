
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

LABELS = ["Root", "Sacral", "Solar", "Heart", "Throat", "Third Eye", "Crown"]

def radar(values, title="Enervi 7 Energy Geometry"):
    vals = [max(0, min(100, float(v))) for v in values]
    N = len(vals)
    angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
    vals += vals[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(7,7), subplot_kw=dict(polar=True))
    ax.plot(angles, vals, marker="o", linewidth=2)
    ax.fill(angles, vals, alpha=0.15)
    ax.set_thetagrids(np.degrees(np.array(angles[:-1])), LABELS)
    ax.set_ylim(0, 100)
    ax.set_rticks([25,50,75,100])
    ax.set_title(title, fontweight="bold")
    fig.text(0.02, 0.02, "Enervi 7  •  Energy • Vivid • Integration", fontsize=9, alpha=0.7)
    fig.tight_layout(pad=2.0)
    return fig

st.set_page_config(page_title="Enervi 7 — MVP", page_icon="✨", layout="centered")

st.title("Enervi 7 Radar — MVP")
st.caption("輸入 7 個分數（0–100），即時生成雷達圖，並可下載 PNG。")

col1, col2 = st.columns(2)
with col1:
    title = st.text_input("圖表標題", "Enervi 7 Energy Geometry")
with col2:
    preset = st.selectbox("快速套用範例", ["—", "Demo(60,50,70,55,40,75,60)"])

scores = {}
for i, label in enumerate(LABELS):
    default = [60,50,70,55,40,75,60][i] if preset.startswith("Demo") else 50
    scores[label] = st.slider(label, 0, 100, value=default, step=1)

vals = [scores[l] for l in LABELS]
fig = radar(vals, title=title)
st.pyplot(fig)

import io
buf = io.BytesIO()
fig.savefig(buf, format="png", dpi=200, bbox_inches="tight")
st.download_button("下載 PNG", data=buf.getvalue(), file_name="enervi7_chart.png", mime="image/png")

st.markdown("---")
st.markdown("**如何使用**：調整分數 ➜ 下方按鈕下載圖片。")
