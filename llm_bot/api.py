import frappe

from typing import Optional

from langchain_openai import ChatOpenAI
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import RedisChatMessageHistory


@frappe.whitelist()
def get_chatbot_response(session_id: str, prompt_message: str) -> str:
    llm_type = get_llm_type_from_settings()
    if llm_type == 'MistralAI':
        mistral_api_key = frappe.conf.get("mistral_api_key")
        if not mistral_api_key:
            frappe.throw("Please set `mistral_api_key` in site config")
        # print(mistral_api_key)
        llm = ChatMistralAI(mistral_api_key=mistral_api_key, model="mistral-large-latest", temperature=0)
    else:
        return f"{llm_type} is not supported yet."
    ### RedisChatMessageHistory
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "你是一个AI助手，你的名字是'小Yo'，你的生日是2024年2月29日。在帮助用户解决问题时，请一步步思考。在回答问题时，如果用户提供的信息不完整，请有礼貌地向用户提问，并提供提问的理由，以获得解决问题所需的必要信息。回复时，请务必不要说类似'让我们一步步思考'类似的话，请尽量以人类口吻自然的回答或提问。"),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}"),
        ]
    )
    chain = prompt | llm
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
    ### no RedisChatMessageHistory
    # messages = [
    #     SystemMessage(
    #         content="你是一个AI助手。让我们一步步思考。"
    #     ),
    #     HumanMessage(
    #         content=prompt_message
    #     ),
    # ]
    # response = llm.invoke(messages)
    print(session_id, '[user]', prompt_message)
    print(session_id, '[bot]', response.content)
    return response.content



def get_llm_type_from_settings():
    return (
        frappe.db.get_single_value("LLM Bot Settings", "llm_type") or "MistralAI"
    )
