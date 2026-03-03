部活精算AIシステム

レシート画像をアップロードするだけで、AIが自動的に品目・金額・日付を抽出し、Googleスプレッドシートに記録するシステムです。

主な機能
自動データ抽出: アップロードされたレシート画像から、Gemini APIが内容を解析します。

スプレッドシート連携: 解析した「日付・品目・金額」をGoogleスプレッドシートへ即座に保存します。

直感的なインターフェース: Tailwind CSSを採用した、シンプルで実用的なUIを提供します。

導入手順
1. 各種キーとシートの準備
Gemini APIキーの取得: Google AI StudioからAPIキーを発行します。

スプレッドシートの作成: Google Sheetsで新規シートを作成し、URLから SHEET_ID を取得します。

形式: https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit

Google Sheets APIの設定: Google Cloud Consoleでプロジェクトを作成し、サービスアカウントの credentials.json を取得して backend/ フォルダへ配置してください。

2. 環境構築
プロジェクトをクローン後、以下の手順で設定を行います。

Bash
# 依存ライブラリのインストール
cd backend
pip install -r requirements.txt
.env ファイルを作成し、APIキーを記述します。

コード スニペット
GENAI_API_KEY=your_api_key_here
使用方法
サーバーの起動:

Bash
python main.py
ブラウザでのアクセス: http://127.0.0.1:8000 を開きます。

レシートの登録: 画像をアップロードすると、自動的にスプレッドシートへデータが転記されます。

プロジェクト構成

club-pay/
├── backend/

│   ├── main.py           # メインアプリケーション

│   ├── requirements.txt  # 依存ライブラリ一覧

│   └── credentials.json  # Google認証ファイル

├── .env                  # 環境変数設定

└── README.md             # 本ドキュメント

技術スタック
Backend: FastAPI

AI: Google Gemini 1.5 Flash

Integration: gspread (Google Sheets API)

Frontend: HTML / CSS (Tailwind CSS)

注意事項
セキュリティ: credentials.json や .env は機密情報を含むため、Gitなどの公開環境にコミットしないでください。

権限設定: 作成したサービスアカウントのメールアドレスに対し、対象スプレッドシートの編集権限を付与する必要があります。

トラブルシューティング
システムが正常に動作しない場合は、以下の点を確認してください。

credentials.json が適切なディレクトリに配置されているか。

サービスアカウントにスプレッドシートの共有権限が与えられているか。

APIキーの有効期限や制限設定に問題がないか。
