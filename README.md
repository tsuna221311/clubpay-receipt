# 部活精算AI システム

レシート画像をアップロードするだけで、AIが自動的に品目・金額・日付を抽出し、Googleスプレッドシートに記録するシステムです。

## 🎯 機能

- 📸 レシート画像のアップロード
- 🤖 Google Gemini APIによる自動データ抽出
- 📊 Google Sheetsへの自動保存
- 🎨 モダンで使いやすいUI（Tailwind CSS）

## 🔧 必要な準備

### 1. Google Generative AI APIキーの取得

1. [Google AI Studio](https://aistudio.google.com/apikey) にアクセス
2. 「API key を作成」をクリック
3. 生成されたAPIキーをコピー

### 2. Google Sheetsの準備

1. [Google Sheets](https://sheets.google.com) で新しいスプレッドシートを作成
2. スプレッドシートURLから以下の形式のIDを取得：
   ```
   https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit
   ```
3. 最初の行にヘッダーを作成（例：日付、品目、金額）

### 3. Google Sheets認証ファイルの準備

1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. 新しいプロジェクトを作成
3. Google Sheets APIを有効化
4. サービスアカウントを作成
5. `credentials.json` をダウンロード
6. プロジェクトの `backend/` フォルダに配置

## 📦 インストール

### 1. 依存ライブラリのインストール

```bash
cd backend
pip install -r requirements.txt
```

### 2. 環境変数の設定

`.env` ファイルを開いて、取得したAPIキーを設定：

```env
GENAI_API_KEY=your_api_key_here
```

### 3. main.py の設定

`backend/main.py` の設定部分を編集：

```python
# --- 設定 ---
GENAI_API_KEY = "your_api_key_here"
SHEET_ID = "your_sheet_id_here"
```

## 🚀 使い方

### サーバーの起動

```bash
cd backend
python main.py
```

ブラウザで `http://127.0.0.1:8000` にアクセス

### レシートの登録

1. 「クリックまたはドラッグ&ドロップ」エリアにレシート画像をアップロード
2. AIが自動的に以下を抽出：
   - 📝 品目名
   - 💰 金額
   - 📅 日付
3. スプレッドシートに自動保存

## 📋 プロジェクト構成

```
club-pay/
├── backend/
│   ├── main.py              # メインアプリケーション
│   ├── requirements.txt      # 依存ライブラリ
│   └── credentials.json      # Google認証ファイル
├── .env                      # 環境変数設定
└── README.md                 # このファイル
```

## 🛠️ 技術スタック

- **フレームワーク**: FastAPI
- **AI/ML**: Google Generative AI (Gemini 1.5 Flash)
- **スプレッドシート連携**: gspread
- **画像処理**: PIL
- **フロントエンド**: HTML/CSS (Tailwind CSS)

## ⚠️ 注意事項

- `credentials.json` と `.env` ファイルはGitにコミットしないでください（`.gitignore` に追加済み）
- APIキーは絶対に公開しないでください
- Google Cloud の無料枠を超えないようご注意ください

## 🐛 トラブルシューティング

### APIキーが無効と言われる場合
- APIキーが正しくコピーされているか確認
- `.env` ファイルが正しく保存されているか確認
- main.py の `GENAI_API_KEY` が `""` になっていないか確認

### スプレッドシートに保存されない場合
- `credentials.json` が `backend/` フォルダにあるか確認
- `SHEET_ID` が正しいか確認
- サービスアカウントにシートの編集権限があるか確認

### 画像が解析できない場合
- 対応形式：JPEG、PNG
- 画像が見やすいレシートか確認
- インターネット接続を確認

## 📝 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 👨‍💻 サポート

問題が発生した場合は、上記のトラブルシューティングをご確認ください。
