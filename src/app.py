"""Streamlitアプリケーション - 問診票アプリ"""

import streamlit as st
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from questionnaire import QuestionnaireAgent

# 環境変数を読み込む
load_dotenv()

# ページ設定
st.set_page_config(
    page_title="医療問診票アプリ",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .question-box {
        background-color: #f0f2f6;
        color: #1a1a1a;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #1f77b4;
    }
    .answer-box {
        background-color: #e8f4f8;
        color: #1a1a1a;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #2ecc71;
    }
    .questionnaire-box {
        background-color: #fff;
        color: #1a1a1a;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 2px solid #1f77b4;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

def init_session_state():
    """セッション状態を初期化"""
    if 'agent' not in st.session_state:
        try:
            st.session_state.agent = QuestionnaireAgent()
            st.session_state.questions_asked = []
            st.session_state.current_question = ""
            st.session_state.answers = []
            st.session_state.questionnaire_complete = False
            st.session_state.final_questionnaire = ""
        except ValueError as e:
            st.error(f"エラー: {str(e)}")
            st.info("📝 サイドバーでOpenAI APIキーを設定してください。")
            st.session_state.agent = None

def check_api_key():
    """APIキーの確認"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        api_key = st.sidebar.text_input(
            "OpenAI API Key",
            type="password",
            help="OpenAI APIキーを入力してください"
        )
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
            st.session_state.agent = None  # 再初期化を促す
            st.rerun()
        return False
    return True

def main():
    """メインアプリケーション"""
    
    # ヘッダー
    st.markdown('<div class="main-header">🏥 医療問診票アプリ</div>', unsafe_allow_html=True)
    
    # APIキーの確認
    if not check_api_key():
        st.stop()
    
    # セッション状態の初期化
    init_session_state()
    
    if st.session_state.agent is None:
        return
    
    # サイドバー
    with st.sidebar:
        st.header("📋 設定")
        
        if st.button("🔄 問診票をリセット", use_container_width=True):
            st.session_state.agent.reset()
            st.session_state.questions_asked = []
            st.session_state.current_question = ""
            st.session_state.answers = []
            st.session_state.questionnaire_complete = False
            st.session_state.final_questionnaire = ""
            st.rerun()
        
        st.divider()
        st.header("📊 問診の進行状況")
        st.info(f"質問数: {len(st.session_state.questions_asked)}")
        st.info(f"回答数: {len(st.session_state.answers)}")
        
        if st.session_state.questionnaire_complete:
            st.success("✅ 問診票完成")
        else:
            st.info("🔄 進行中")
    
    # メインコンテンツ
    if not st.session_state.questionnaire_complete:
        # 問診が未完了の場合
        
        # 初回質問の取得
        if not st.session_state.current_question:
            with st.spinner("初期化中..."):
                try:
                    question = st.session_state.agent.get_next_question()
                    st.session_state.current_question = question
                    st.session_state.questions_asked.append(question)
                except Exception as e:
                    st.error(f"エラーが発生しました: {str(e)}")
                    st.info("APIキーが正しいか確認してください。")
                    st.stop()
        
        # 現在の質問を表示
        if st.session_state.current_question:
            st.markdown(f'<div class="question-box"><strong>📌 質問 {len(st.session_state.questions_asked)}</strong><br>{st.session_state.current_question}</div>', unsafe_allow_html=True)
        
        # 回答入力フォーム
        with st.form("answer_form", clear_on_submit=True):
            answer = st.text_area(
                "あなたの回答を入力してください:",
                height=150,
                placeholder="回答をここに入力してください..."
            )
            col1, col2 = st.columns([1, 5])
            with col1:
                submit_button = st.form_submit_button("送信", use_container_width=True)
            with col2:
                complete_button = st.form_submit_button("問診票を完成させる", use_container_width=True)
        
        # 送信ボタンが押された場合
        if submit_button and answer:
            st.session_state.agent.add_answer(answer)
            st.session_state.answers.append(answer)
            
            # 次の質問を取得
            with st.spinner("次の質問を生成中..."):
                try:
                    next_question = st.session_state.agent.get_next_question()
                    if next_question and "完成" not in next_question:
                        st.session_state.current_question = next_question
                        st.session_state.questions_asked.append(next_question)
                    else:
                        # 自動的に完成させる
                        complete_button = True
                except Exception as e:
                    st.error(f"エラーが発生しました: {str(e)}")
        
        # 問診票を完成させるボタンが押された場合
        if complete_button:
            with st.spinner("問診票を生成中..."):
                try:
                    final_questionnaire = st.session_state.agent.generate_complete_questionnaire()
                    st.session_state.final_questionnaire = final_questionnaire
                    st.session_state.questionnaire_complete = True
                    st.rerun()
                except Exception as e:
                    st.error(f"エラーが発生しました: {str(e)}")
        
        # これまでの会話履歴を表示
        if st.session_state.answers:
            st.divider()
            st.header("📝 これまでの会話")
            for i, (q, a) in enumerate(zip(st.session_state.questions_asked[:-1], st.session_state.answers), 1):
                st.markdown(f'<div class="question-box"><strong>質問 {i}:</strong> {q}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="answer-box"><strong>回答 {i}:</strong> {a}</div>', unsafe_allow_html=True)
    
    else:
        # 問診票が完成した場合
        st.success("✅ 問診票が完成しました！")
        
        st.markdown('<div class="questionnaire-box">', unsafe_allow_html=True)
        st.markdown(st.session_state.final_questionnaire)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # ダウンロードボタン
        st.download_button(
            label="📥 問診票をダウンロード",
            data=st.session_state.final_questionnaire,
            file_name=f"questionnaire_{len(st.session_state.answers)}_answers.txt",
            mime="text/plain"
        )
        
        # 会話履歴も表示
        with st.expander("📝 会話履歴を表示"):
            for i, (q, a) in enumerate(zip(st.session_state.questions_asked, st.session_state.answers + [""]), 1):
                st.markdown(f'**質問 {i}:** {q}')
                if i <= len(st.session_state.answers):
                    st.markdown(f'**回答 {i}:** {st.session_state.answers[i-1]}')
                st.divider()

if __name__ == "__main__":
    main()

