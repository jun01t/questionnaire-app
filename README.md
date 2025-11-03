# 🏥 医療問診票アプリ

LangChainを使用した対話型の医療問診票生成アプリケーションです。AIが適切な質問を順番に提示し、患者の回答を基に問診票を自動生成します。

## ✨ 機能

- 🤖 AIによる適切な質問の自動生成
- 💬 対話形式での問診票作成
- 📋 構造化された問診票の自動生成
- 💾 問診票のダウンロード機能
- 📱 レスポンシブなUIデザイン

## 🚀 セットアップ

### 1. 必要な環境

- Python 3.8以上
- OpenAI APIキー

### 2. 依存パッケージのインストール

```bash
cd questionnaire-app
pip install -r requirements.txt
```

### 3. 環境変数の設定

`.env.example`を`.env`にコピーして、OpenAI APIキーを設定してください：

```bash
cp .env.example .env
```

`.env`ファイルを開いて、取得したOpenAI APIキーを設定：

```
OPENAI_API_KEY=sk-your-api-key-here
```

### 4. アプリケーションの起動

プロジェクトルートディレクトリ（`questionnaire-app/`）から以下を実行：

```bash
streamlit run src/app.py
```

ブラウザで `http://localhost:8501` にアクセスしてください。

**注意**: 初回起動時にサイドバーでOpenAI APIキーを入力することもできます（`.env`ファイルに設定していない場合）。

## 📦 プロジェクト構造

```
questionnaire-app/
├── src/
│   ├── __init__.py
│   ├── app.py              # Streamlitメインアプリケーション
│   ├── questionnaire.py    # 問診票生成ロジック
│   └── prompts.py          # プロンプトテンプレート
├── requirements.txt        # 依存パッケージ
├── .env.example           # 環境変数テンプレート
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

## ⚠️ 注意事項

- このアプリケーションは教育・研究目的のものです
- 実際の医療診断には使用しないでください
- OpenAI APIキーは安全に管理してください
- APIの使用には料金が発生する場合があります

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

