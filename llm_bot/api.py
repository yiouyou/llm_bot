import frappe

from typing import Optional

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_openai import ChatOpenAI
from langchain_mistralai import ChatMistralAI


@frappe.whitelist()
def get_chatbot_response(session_id: str, prompt_message: str) -> str:
    mistral_api_key = frappe.conf.get("mistral_api_key")
    if not mistral_api_key:
        frappe.throw("Please set `mistral_api_key` in site config")
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "你是一个AI助手。让我们一步步思考。"),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}"),
        ]
    )
    chain = prompt | ChatMistralAI(model_name=mistral_api_key, model="mistral-large-latest", temperature=0)
    chain_with_history = RunnableWithMessageHistory(
        chain,
        lambda session_id: RedisChatMessageHistory(
            session_id=session_id,
            url=frappe.conf.get("redis_cache") or "redis://localhost:6379/0",
        ),
        input_messages_key="question",
        history_messages_key="history",
    )
    config = {"configurable": {"session_id": session_id}}
    response = chain_with_history.invoke({"question": prompt_message}, config=config)
    return response.content


def get_openai_model_from_settings():
  return (
    frappe.db.get_single_value("LLM Bot Settings", "openai_model") or "gpt-3.5-turbo"
  )
