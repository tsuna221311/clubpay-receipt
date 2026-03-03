import os
import json
import io
import google.generativeai as genai
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import PIL.Image
import gspread
from google.oauth2.service_account import Credentials

# --- 設定 ---
# TODO: 以下の値を自分のものに変更してください
# Google Generative AI APIキーを取得: https://aistudio.google.com/apikey
GENAI_API_KEY = ""
# Google Sheets IDを指定: スプレッドシートURLから取得
SHEET_ID = ""

genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

app = FastAPI(title="部活精算AI PRO")

# スプレッドシート保存
def save_to_sheet(item, amount, date):
    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID).sheet1
        sheet.append_row([date, item, amount])
        return True
    except:
        return False

# --- フロントエンドUI (HTML) ---
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>部活精算AI - TOKIUM Style</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        .drop-zone { border: 2px dashed #cbd5e1; transition: all 0.3s; }
        .drop-zone.active { border-color: #3b82f6; background: #eff6ff; }
        .loading { display: none; }
    </style>
</head>
<body class="bg-slate-50 min-h-screen font-sans">
    <nav class="bg-blue-600 text-white p-4 shadow-lg">
        <div class="container mx-auto flex items-center">
            <i class="fas fa-file-invoice-dollar mr-3 text-2xl"></i>
            <h1 class="text-xl font-bold">部活精算AI システム</h1>
        </div>
    </nav>

    <main class="container mx-auto px-4 py-8 max-w-2xl">
        <div class="bg-white rounded-2xl shadow-sm p-8 border border-slate-200">
            <h2 class="text-2xl font-bold text-slate-800 mb-6 text-center">レシートをアップロード</h2>

            <div id="dropZone" class="drop-zone rounded-xl p-10 text-center cursor-pointer mb-6">
                <i class="fas fa-cloud-upload-alt text-4xl text-blue-500 mb-4"></i>
                <p class="text-slate-600 font-medium">クリックまたはドラッグ＆ドロップ</p>
                <input type="file" id="fileInput" class="hidden" accept="image/*">
            </div>

            <div id="loading" class="loading text-center py-4">
                <i class="fas fa-spinner fa-spin text-blue-500 text-3xl mb-2"></i>
                <p class="text-slate-500 text-sm">AIがレシートを解析して帳簿をつけています...</p>
            </div>

            <div id="result" class="hidden space-y-4">
                <div class="bg-green-50 border border-green-200 rounded-lg p-4">
                    <p class="text-green-700 font-bold text-center"><i class="fas fa-check-circle mr-2"></i>スプレッドシートに保存しました！</p>
                </div>
                <div class="grid grid-cols-2 gap-4 text-sm bg-slate-50 p-4 rounded-lg">
                    <div class="text-slate-500">品目</div><div id="res-item" class="font-bold text-right text-slate-800">-</div>
                    <div class="text-slate-500">金額</div><div id="res-amount" class="font-bold text-right text-slate-800">-</div>
                    <div class="text-slate-500">日付</div><div id="res-date" class="font-bold text-right text-slate-800">-</div>
                </div>
                <button onclick="location.reload()" class="w-full bg-slate-800 text-white py-2 rounded-lg hover:bg-slate-700 transition">続けて登録する</button>
            </div>
        </div>
    </main>

    <script>
        const dropZone = document.getElementById('dropZone');
        const fileInput = document.getElementById('fileInput');

        dropZone.onclick = () => fileInput.click();

        fileInput.onchange = (e) => handleUpload(e.target.files[0]);

        async function handleUpload(file) {
            if (!file) return;

            dropZone.classList.add('hidden');
            document.getElementById('loading').classList.remove('hidden');

            const formData = new FormData();
            formData.append('file', file);

            try {
                const response = await fetch('/analyze', { method: 'POST', body: formData });
                const data = await response.json();

                document.getElementById('loading').classList.add('hidden');
                document.getElementById('result').classList.remove('hidden');
                document.getElementById('res-item').innerText = data.item;
                document.getElementById('res-amount').innerText = "¥" + data.amount.toLocaleString();
                document.getElementById('res-date').innerText = data.date;
            } catch (error) {
                alert('解析に失敗しました。');
                location.reload();
            }
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def get_ui():
    return HTML_CONTENT

@app.post("/analyze")
async def analyze_receipt(file: UploadFile = File(...)):
    img_data = await file.read()
    img = PIL.Image.open(io.BytesIO(img_data))
    prompt = "レシートから品目(日本語)、合計金額(数値)、日付(YYYY-MM-DD)を抜き出しJSON形式で返せ。{'item':'品名','amount':100, 'date':'2024-01-01'}"
    response = model.generate_content([prompt, img])
    result = json.loads(response.text.replace('```json', '').replace('```', '').strip())

    save_to_sheet(result['item'], result['amount'], result['date'])
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
