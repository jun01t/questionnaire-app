"""問診票生成のロジック"""

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from typing import List, Dict, Optional
import os
from .prompts import (
    QUESTION_GENERATION_PROMPT,
    QUESTIONNAIRE_COMPLETION_PROMPT,
    QUESTIONNAIRE_SYSTEM_PROMPT
)


class QuestionnaireAgent:
    """問診票生成エージェント"""
    
    def __init__(self, model_name: str = "gpt-4o-mini", temperature: float = 0.7):
        """
        問診票エージェントを初期化
        
        Args:
            model_name: 使用するLLMモデル名
            temperature: 生成のランダム性（0.0-2.0）
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY環境変数が設定されていません")
        
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            api_key=api_key
        )
        self.memory = ConversationBufferMemory(
            return_messages=True,
            memory_key="chat_history"
        )
        self.conversation_history: List[Dict[str, str]] = []
        self.is_complete = False
        
    def get_next_question(self) -> str:
        """
        次の質問を生成
        
        Returns:
            次の質問文
        """
        if self.is_complete:
            return "問診票が完成しました。他に質問はありません。"
        
        # 会話履歴を文字列に変換
        history_text = self._format_conversation_history()
        
        # 現在の問診票の状態を取得
        current_questionnaire = self._get_current_questionnaire_summary()
        
        # 質問生成プロンプトを作成
        prompt = ChatPromptTemplate.from_messages([
            ("system", QUESTIONNAIRE_SYSTEM_PROMPT),
            ("human", QUESTION_GENERATION_PROMPT.format(
                conversation_history=history_text,
                current_questionnaire=current_questionnaire
            ))
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({})
        
        return response.content.strip()
    
    def add_answer(self, answer: str) -> None:
        """
        患者の回答を追加
        
        Args:
            answer: 患者の回答
        """
        if self.is_complete:
            return
        
        # 最後の質問を取得（なければ空文字）
        last_question = ""
        if self.conversation_history:
            last_question = self.conversation_history[-1].get("question", "")
        
        # 会話履歴に追加
        self.conversation_history.append({
            "question": last_question,
            "answer": answer
        })
        
        self.memory.chat_memory.add_user_message(f"質問: {last_question}")
        self.memory.chat_memory.add_ai_message(f"回答: {answer}")
    
    def generate_complete_questionnaire(self) -> str:
        """
        完成した問診票を生成
        
        Returns:
            完成した問診票のテキスト
        """
        history_text = self._format_conversation_history()
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", QUESTIONNAIRE_SYSTEM_PROMPT),
            ("human", QUESTIONNAIRE_COMPLETION_PROMPT.format(
                conversation_history=history_text
            ))
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({})
        
        self.is_complete = True
        return response.content.strip()
    
    def _format_conversation_history(self) -> str:
        """会話履歴を文字列形式に変換"""
        if not self.conversation_history:
            return "まだ会話が始まっていません。"
        
        history_parts = []
        for i, conv in enumerate(self.conversation_history, 1):
            if conv.get("question"):
                history_parts.append(f"質問{i}: {conv['question']}")
            if conv.get("answer"):
                history_parts.append(f"回答{i}: {conv['answer']}")
        
        return "\n".join(history_parts)
    
    def _get_current_questionnaire_summary(self) -> str:
        """現在の問診票の状態を要約"""
        if not self.conversation_history:
            return "問診票はまだ開始されていません。"
        
        summary_parts = []
        for conv in self.conversation_history:
            if conv.get("answer"):
                summary_parts.append(conv['answer'])
        
        return "\n".join(summary_parts) if summary_parts else "まだ情報がありません。"
    
    def reset(self) -> None:
        """問診票をリセット"""
        self.conversation_history = []
        self.memory.clear()
        self.is_complete = False

