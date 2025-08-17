
# Enervi 7 Radar — MVP

一個最小可行版本（MVP），輸入 7 個分數（0–100）即時產生雷達圖，並可下載 PNG。

## 線上部署（免費永久網址）
使用 **Streamlit Community Cloud**。

1. 建立 GitHub 帳號並登入
2. 建立新 Repository（例如：`enervi7-mvp`）
3. 上傳這三個檔案：`app.py`、`requirements.txt`、`README.md`
4. 前往 https://streamlit.io/cloud → **New app**
5. 選取你的 repo（branch 選 `main`，app file 選 `app.py`）→ **Deploy**
6. 等待部署完成，你會得到固定網址：
   ```
   https://<你的專案>-<你的帳號>.streamlit.app
   ```
> 免費版提醒：長時間無人使用會休眠，再次開啟時會自動喚醒。

## 本地執行
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 說明
- 7 個分數順序：Root, Sacral, Solar, Heart, Throat, Third Eye, Crown
- 分數範圍：0–100（程式會自動夾住）
- 一鍵下載高解析 PNG
