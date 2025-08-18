# app.py
# Enervi7 – 14題計分 → 七軸雷達圖（單檔 Flask 版）
# 直接執行：python app.py

from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)

# ========================
#  一、階段/轉換的顯示與建議
# ========================

STAGE_META = {
    "S1": {
        "name": "S1 覺察 Awareness",
        "keywords": ["覺知當下", "辨識情緒", "看見模式", "誠實面對"],
        "actions": [
            "寫三句『此刻我真實的感受是…』",
            "做 3 分鐘腹式呼吸（4-4-6）並記錄身體感受",
            "列出1個反覆出現的念頭，標記：是事實還是解讀？"
        ]
    },
    "S2": {
        "name": "S2 釋放 Release",
        "keywords": ["鬆綁負荷", "情緒代謝", "放下執著", "完成回收"],
        "actions": [
            "做一次『寫了就撕/燒』的釋放書寫（2-3段）",
            "身體掃描，對緊繃部位做 60 秒放鬆",
            "將一件拖延小事今天完成並打勾"
        ]
    },
    "S3": {
        "name": "S3 信任 Trust",
        "keywords": ["允許發生", "對齊意圖", "資源感", "安全感"],
        "actions": [
            "用『我允許…』造句 3 句（對應今日焦點）",
            "回顧過往 1 次被支持的證據，寫下為何可複製",
            "今天主動請求一次幫助（小範圍即可）"
        ]
    },
    "S4": {
        "name": "S4 行動 Action",
        "keywords": ["最小步驟", "可驗證", "節奏", "執行力"],
        "actions": [
            "將目標拆成 10 分鐘可完成的一步，現在就做",
            "設定今日 3 件 MIT（Most Important Tasks）",
            "完成後『公開回報』給一位可信任的人"
        ]
    },
    "S5": {
        "name": "S5 流動 Flow",
        "keywords": ["專注", "回饋循環", "韌性", "迭代"],
        "actions": [
            "把今天的卡點→調整 1 個微策略（嘗試 A/B）",
            "為單一任務設定 25 分鐘番茄鐘並全程專注",
            "記錄 1 個有效回饋，明天沿用"
        ]
    },
    "S6": {
        "name": "S6 共鳴 Resonance",
        "keywords": ["連結", "價值感", "貢獻", "擴散"],
        "actions": [
            "分享一個小成果或洞見到社群/朋友",
            "邀請 1 人給具體回饋（3 句具體描述）",
            "主動建立一個合作可能（發出一則邀請）"
        ]
    },
    "S7": {
        "name": "S7 整合 Integration",
        "keywords": ["總結經驗", "固化習慣", "結構化", "長期化"],
        "actions": [
            "用 5 句話摘要本週學到的 3 件事＋1 改進",
            "將有效步驟寫成 Checklist 並固定到行程",
            "為下個週期設定一個可衡量指標（KPI）"
        ]
    }
}

TRANSITION_META = {
    "T1": {"label": "S1→S2 臨界點（從覺察到釋放）",
           "actions": ["把『我觀察到…』改寫成『我願意放下…』句型 3 句",
                       "做一次情緒書寫並以身體放鬆收尾（頸肩/腹部）"]},
    "T2": {"label": "S2→S3 臨界點（從釋放到信任）",
           "actions": ["列出 3 個現有資源（人/物/技能）",
                       "寫 1 段：若一切對我有利，今天我可以允許什麼？"]},
    "T3": {"label": "S3→S4 臨界點（從信任到行動）",
           "actions": ["產出『最小可行步驟』並在 10 分鐘內啟動",
                       "預約 1 個『行動時段』，行前只做準備清單"]},
    "T4": {"label": "S4→S5 臨界點（從行動到流動）",
           "actions": ["把今日行動的回饋紀錄下來並做 1 次微調",
                       "建立 1 個 25 分鐘專注儀式，結束回顧 2 分鐘"]},
    "T5": {"label": "S5→S6 臨界點（從流動到共鳴）",
           "actions": ["公開分享 1 個進展/案例，索取 1 次具體回饋",
                       "辨識最被共鳴的價值，明天主打該元素"]},
    "T6": {"label": "S6→S7 臨界點（從共鳴到整合）",
           "actions": ["把有效做法寫成 SOP/Checklist",
                       "選一個可持續的節奏（週/月）放進行事曆"]},
    "T7": {"label": "S7→S1 臨界點（從整合回覺察/新週期）",
           "actions": ["本週回顧 3 句＋下一輪新意圖 1 句",
                       "挑選 1 個欲精進的指標，設置觀測方式"]}
}

# ========================
#  二、核心計分邏輯
# ========================

def compute_enervi7_scores(answers, penalty=False, tau=4.0, delta=0.3):
    """
    answers: dict, keys 'Q1'..'Q7', 'T1'..'T7', values 0..10
    penalty: 是否啟用轉換懲罰項（使卡關能反映到相鄰階段）
    tau:     懲罰門檻（0..10）
    delta:   懲罰強度（0..10 尺度）
    return:  結果字典
    """
    Q = [float(answers.get(f"Q{i}", 0)) for i in range(1, 8)]
    T = [float(answers.get(f"T{i}", 0)) for i in range(1, 8)]

    wQ, wPrev, wNext = 0.60, 0.20, 0.20

    stages_raw = []
    for i in range(7):
        prev_t = T[(i - 1) % 7]  # Ti-1
        next_t = T[i]            # Ti
        val = wQ * Q[i] + wPrev * prev_t + wNext * next_t

        if penalty:
            if prev_t < tau:
                val -= delta
            if next_t < tau:
                val -= delta
            val = max(0.0, val)

        stages_raw.append(val)

    # 0..100
    stages = [round(v * 10, 1) for v in stages_raw]
    transitions = [round(t * 10, 1) for t in T]

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

# ========================
#  三、頁面模板（單檔版）
# ========================

PAGE = """
<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Enervi7 測量</title>
  <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans TC", "Helvetica Neue", Arial, "PingFang TC", "Microsoft JhengHei", sans-serif; margin: 24px; }
    .wrap { max-width: 1080px; margin: 0 auto; }
    h1 { margin-bottom: 8px; }
    .card { border: 1px solid #e5e7eb; border-radius: 12px; padding: 16px; margin-bottom: 16px; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; }
    label { display:block; font-size: 13px; color:#374151; margin-bottom: 4px;}
    input[type="number"] { width: 100%; padding: 8px; border:1px solid #d1d5db; border-radius:8px; }
    .btn { background:#111827; color:#fff; padding:10px 16px; border-radius:10px; border:none; cursor:pointer; }
    .btn:disabled { opacity:.5; cursor:not-allowed; }
    table { width:100%; border-collapse: collapse; }
    th, td { padding:8px 10px; border-bottom:1px solid #e5e7eb; text-align: left; }
    .pill { display:inline-block; padding:2px 8px; border-radius:999px; font-size:12px; border:1px solid #e5e7eb; margin-right:6px;}
    .low { background:#fee2e2; }
    .mid { background:#fef9c3; }
    .high{ background:#dcfce7; }
    .hint { color:#6b7280; font-size:13px; }
    .klist { margin:6px 0 0 16px; }
  </style>
</head>
<body>
  <div class="wrap">
    <h1>Enervi7 量測（14題 → 七軸雷達）</h1>
    <p class="hint">請輸入 0–10 分（可小數）。預設 5。可勾選「加強卡關顯示」讓低轉換拉低相鄰階段分數。</p>

    <form method="post" action="/analyze" class="card">
      <h3>七階題（Q1–Q7）</h3>
      <div class="grid">
        {% for i in range(1,8) %}
        <div>
          <label for="Q{{i}}">Q{{i}}</label>
          <input type="number" step="0.1" min="0" max="10" name="Q{{i}}" id="Q{{i}}" value="{{defaults['Q'+str(i)]}}">
        </div>
        {% endfor %}
      </div>

      <h3 style="margin-top:16px;">七個轉換（T1–T7）</h3>
      <div class="grid">
        {% for i in range(1,8) %}
        <div>
          <label for="T{{i}}">T{{i}}</label>
          <input type="number" step="0.1" min="0" max="10" name="T{{i}}" id="T{{i}}" value="{{defaults['T'+str(i)]}}">
        </div>
        {% endfor %}
      </div>

      <div style="margin-top:12px;">
        <label><input type="checkbox" name="penalty" {% if defaults['penalty'] %}checked{% endif %}> 加強卡關顯示（轉換懲罰）</label>
      </div>

      <button class="btn" type="submit" style="margin-top:12px;">計算</button>
    </form>

    {% if result %}
    <div class="card">
      <h3>雷達圖</h3>
      <div id="radar" style="height:460px;"></div>
    </div>

    <div class="card">
      <h3>結果摘要</h3>
      <p>
        <span class="pill">主導階段：<b>{{ stage_meta[result['dominant_stage']]['name'] }}</b></span>
        <span class="pill">瓶頸轉換：<b>{{ transition_meta[result['bottleneck_transitions'][0]]['label'] }}</b></span>
        <span class="pill">次瓶頸：<b>{{ transition_meta[result['bottleneck_transitions'][1]]['label'] }}</b></span>
      </p>
      <div class="grid">
        <div>
          <h4>七階分數（0–100）</h4>
          <table>
            <thead><tr><th>階段</th><th>分數</th><th>等級</th></tr></thead>
            <tbody>
            {% for k,v in result['stages'].items() %}
              {% set level = 'low' if v<40 else ('mid' if v<70 else 'high') %}
              <tr><td>{{ stage_meta[k]['name'] }}</td><td>{{ v }}</td>
                <td><span class="pill {{level}}">{{ '低' if level=='low' else ('中' if level=='mid' else '高') }}</span></td>
              </tr>
            {% endfor %}
            </tbody>
          </table>
        </div>
        <div>
          <h4>轉換分數（0–100）</h4>
          <table>
            <thead><tr><th>轉換</th><th>分數</th><th>等級</th></tr></thead>
            <tbody>
            {% for k,v in result['transitions'].items() %}
              {% set level = 'low' if v<40 else ('mid' if v<70 else 'high') %}
              <tr><td>{{ transition_meta[k]['label'] }}</td><td>{{ v }}</td>
                <td><span class="pill {{level}}">{{ '低' if level=='low' else ('中' if level=='mid' else '高') }}</span></td>
              </tr>
            {% endfor %}
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div class="card">
      <h3>關鍵字＋行動建議</h3>
      <div class="grid">
        {% for sid, s in stage_meta.items() %}
        <div>
          <h4 style="margin:0 0 6px 0;">{{ s['name'] }}</h4>
          <div class="hint">關鍵字</div>
          <ul class="klist">
            {% for kw in s['keywords'] %}<li>• {{ kw }}</li>{% endfor %}
          </ul>
          <div class="hint" style="margin-top:6px;">行動建議</div>
          <ul class="klist">
            {% for act in s['actions'] %}<li>• {{ act }}</li>{% endfor %}
          </ul>
        </div>
        {% endfor %}
      </div>
    </div>

    <div class="card">
      <h3>瓶頸轉換的解卡建議</h3>
      <div class="grid">
        {% for tid in result['bottleneck_transitions'] %}
        <div>
          <h4 style="margin:0 0 6px 0;">{{ transition_meta[tid]['label'] }}</h4>
          <ul class="klist">
            {% for act in transition_meta[tid]['actions'] %}<li>• {{ act }}</li>{% endfor %}
          </ul>
        </div>
        {% endfor %}
      </div>
    </div>
    {% endif %}

    <div class="card">
      <h3>JSON API</h3>
      <p class="hint">POST <code>/api/compute</code>，Body（JSON）鍵名 <code>Q1..Q7</code>、<code>T1..T7</code>、選填 <code>penalty</code>（bool）。回傳包含 <code>stages</code>、<code>transitions</code>、<code>dominant_stage</code>、<code>bottleneck_transitions</code>。</p>
      <pre>{
  "Q1":5,"Q2":5,"Q3":5,"Q4":5,"Q5":5,"Q6":5,"Q7":5,
  "T1":5,"T2":5,"T3":5,"T4":5,"T5":5,"T6":5,"T7":5,
  "penalty": false
}</pre>
    </div>
  </div>

  {% if result %}
  <script>
    (function(){
      // 雷達資料
      const labels = ["S1 覺察","S2 釋放","S3 信任","S4 行動","S5 流動","S6 共鳴","S7 整合"];
      const vals = [
        {{ result['stages']['S1'] }},
        {{ result['stages']['S2'] }},
        {{ result['stages']['S3'] }},
        {{ result['stages']['S4'] }},
        {{ result['stages']['S5'] }},
        {{ result['stages']['S6'] }},
        {{ result['stages']['S7'] }}
      ];
      // Radar 要首尾相接
      const valsClosed = vals.concat([vals[0]]);
      const labelsClosed = labels.concat([labels[0]]);

      const data = [{
        type: 'scatterpolar',
        r: valsClosed,
        theta: labelsClosed,
        fill: 'toself',
        name: 'Enervi7'
      }];

      const layout = {
        polar: {
          radialaxis: { visible: true, range: [0, 100] }
        },
        margin: { t: 20, r: 20, b: 20, l: 20 },
        showlegend: false
      };

      Plotly.newPlot('radar', data, layout, {displayModeBar:false});
    })();
  </script>
  {% endif %}
</body>
</html>
"""

# ========================
#  四、路由
# ========================

@app.route("/", methods=["GET"])
def index():
    defaults = {**{f"Q{i}": 5 for i in range(1,8)},
                **{f"T{i}": 5 for i in range(1,8)},
                "penalty": False}
    return render_template_string(
        PAGE,
        defaults=defaults,
        result=None,
        stage_meta=STAGE_META,
        transition_meta=TRANSITION_META
    )

@app.route("/analyze", methods=["POST"])
def analyze():
    # 讀表單
    payload = {}
    for i in range(1,8):
        payload[f"Q{i}"] = float(request.form.get(f"Q{i}", 0) or 0)
        payload[f"T{i}"] = float(request.form.get(f"T{i}", 0) or 0)
    use_penalty = True if request.form.get("penalty") == "on" else False

    result = compute_enervi7_scores(payload, penalty=use_penalty)

    # 將使用者輸入回填到表單
    defaults = {**{f"Q{i}": payload[f"Q{i}"] for i in range(1,8)},
                **{f"T{i}": payload[f"T{i}"] for i in range(1,8)},
                "penalty": use_penalty}

    return render_template_string(
        PAGE,
        defaults=defaults,
        result=result,
        stage_meta=STAGE_META,
        transition_meta=TRANSITION_META
    )

@app.route("/api/compute", methods=["POST"])
def api_compute():
    data = request.get_json(force=True, silent=True) or {}
    use_penalty = bool(data.get("penalty", False))
    result = compute_enervi7_scores(data, penalty=use_penalty)
    return jsonify(result)

# ========================
#  五、啟動
# ========================

if __name__ == "__main__":
    app.run(debug=True)