# 🏥 医療問診票アプリ

LangChainを使用した対話型の医療問診票生成アプリケーションです。AIが適切な質問を順番に提示し、患者の回答を基に問診票を自動生成します。

## ✨ 機能

- 🤖 AIによる適切な質問の自動生成
- 💬 対話形式での問診票作成
- 📋 構造化された問診票の自動生成
- 💾 問診票のダウンロード機能
- 📱 レスポンシブなUIデザイン

## 🚀 セットアップ

### 方法1: ローカル環境で起動

#### 1. 必要な環境

- Python 3.8以上
- OpenAI APIキー

#### 2. 依存パッケージのインストール

```bash
# 仮想環境を作成（推奨）
python -m venv venv

# 仮想環境を有効化
# macOS/Linuxの場合:
source venv/bin/activate
# Windowsの場合:
# venv\Scripts\activate

# 依存パッケージをインストール
pip install -r requirements.txt
```

#### 3. 環境変数の設定

`.env`ファイルを作成して、OpenAI APIキーを設定してください：

```bash
echo "OPENAI_API_KEY=sk-your-api-key-here" > .env
```

または、テキストエディタで`.env`ファイルを作成し、以下のように設定してください：

```env
OPENAI_API_KEY=sk-your-api-key-here
```

#### 4. アプリケーションの起動

プロジェクトルートディレクトリから以下を実行：

```bash
streamlit run src/app.py
```

ブラウザで `http://localhost:8501` にアクセスしてください。

**注意**: 初回起動時にサイドバーでOpenAI APIキーを入力することもできます（`.env`ファイルに設定していない場合）。

---

### 方法2: Docker Composeで起動

Dockerがインストールされている場合、Docker Composeを使用すると環境構築が簡単で一貫性があります。

#### 1. 前提条件

- Docker Desktop（またはDocker Engine + Docker Compose）
- OpenAI APIキー

#### 2. 環境変数の設定

`.env`ファイルを作成して、OpenAI APIキーを設定してください：

```bash
# .envファイルを作成
echo "OPENAI_API_KEY=sk-your-api-key-here" > .env
```

または、テキストエディタで`.env`ファイルを作成し、以下のように設定してください：

```env
OPENAI_API_KEY=sk-your-api-key-here
```

#### 3. Docker Composeで起動

```bash
# イメージをビルドして起動
docker compose up --build

# バックグラウンドで起動する場合
docker compose up -d --build
```

ブラウザで `http://localhost:8501` にアクセスしてください。

#### 4. 停止

```bash
# コンテナを停止
docker compose down

# コンテナとボリュームを削除する場合
docker compose down -v
```

## 📦 プロジェクト構造

```text
questionnaire-app/
├── src/
│   ├── __init__.py
│   ├── app.py              # Streamlitメインアプリケーション
│   ├── questionnaire.py    # 問診票生成ロジック
│   └── prompts.py          # プロンプトテンプレート
├── requirements.txt        # 依存パッケージ
├── Dockerfile             # Dockerイメージ定義
├── docker-compose.yml     # Docker Compose設定
├── .dockerignore          # Docker無視ファイル
├── .env                   # 環境変数（自分で作成）
└── README.md              # このファイル
```

## 🎯 使い方

1. アプリケーションを起動すると、最初の質問が表示されます
2. 質問に対して回答を入力し、「送信」ボタンをクリック
3. AIが次の適切な質問を自動生成します
4. 必要な情報が揃ったら、「問診票を完成させる」ボタンをクリック
5. 完成した問診票が表示され、ダウンロード可能になります

## 🛠️ 技術スタック

- **LangChain**: LLMアプリケーション構築フレームワーク
- **LangChain OpenAI**: OpenAIモデルとの統合
- **Streamlit**: Webアプリケーションフレームワーク
- **OpenAI API**: GPT-4o-miniモデルを使用

## 📝 カスタマイズ

### モデルの変更

`src/questionnaire.py`の`QuestionnaireAgent`クラスの初期化時にモデルを変更できます：

```python
agent = QuestionnaireAgent(model_name="gpt-4", temperature=0.7)
```

### プロンプトのカスタマイズ

`src/prompts.py`でプロンプトテンプレートを編集することで、問診票の形式や質問の内容をカスタマイズできます。

## 🐳 Docker関連のトラブルシューティング

### コンテナの再ビルド

コードを変更した場合は、イメージを再ビルドしてください：

```bash
docker compose up --build
```

### ログの確認

```bash
# コンテナのログを確認
docker compose logs -f

# 最後の100行を確認
docker compose logs --tail=100
```

### コンテナ内でのデバッグ

```bash
# 実行中のコンテナに入る
docker compose exec questionnaire-app bash

# コンテナを再起動
docker compose restart
```

## 🔧 エラー対処

### Error 429: Quota Exceeded（クォータ超過）

以下のようなエラーが表示された場合：

```text
Error code: 429 - insufficient_quota
```

**原因**: OpenAI APIの使用制限に達しました。

#### 直接OpenAI APIを呼び出している場合

**対処方法**:

1. OpenAIのアカウントページでクレジット残高を確認
   - [OpenAI 請求設定ページ](https://platform.openai.com/account/billing)
2. クレジットカードを登録する
3. 使用量の上限を引き上げる
4. 新しいAPIキーを取得する

#### 外部サービス経由の場合

LangChain、Vercel AI SDK、n8nなどの外部サービス経由でOpenAI APIを呼び出している場合、以下の可能性があります：

- **原因**: 外部サービス側のバックエンドAPIキーが上限超過
- **対処方法**:
  1. 使用している外部サービスの設定を確認
  2. そのサービスの料金プランや使用制限を確認
  3. `.env`または設定ファイル内の`OPENAI_API_KEY`が有効か確認
  4. 別のAPIキーに差し替えてテストしてみる
  5. サービス提供者に問い合わせる

### APIキーが無効な場合

APIキーが正しくない場合は、サイドバーから新しいキーを入力してください。
また、`.env`ファイルに正しいキーが設定されているか確認してください。

```bash
# .envファイルの内容を確認（注意: 内容が表示されます）
cat .env
```

## ⚠️ 注意事項

- このアプリケーションは教育・研究目的のものです
- 実際の医療診断には使用しないでください
- OpenAI APIキーは安全に管理してください
- APIの使用には料金が発生する場合があります
- `.env`ファイルは`.gitignore`に含めることを推奨します

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。
