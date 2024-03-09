import frappe

from typing import Optional

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import RedisChatMessageHistory


@frappe.whitelist()
def get_chatbot_response(session_id: str, prompt_message: str) -> str:
		# Throw if no key in site_config
		# Maybe extract and cache this (site cache)
		opeai_api_key = frappe.conf.get("openai_api_key")
		openai_model = get_model_from_settings()
		if not opeai_api_key:
				frappe.throw("Please set `openai_api_key` in site config")
		prompt = ChatPromptTemplate.from_messages(
		    [
    		    ("system", "You're an assistant。"),
        		MessagesPlaceholder(variable_name="history"),
        		("human", "{question}"),
    		]
		)
		chain = prompt | ChatOpenAI(model_name=openai_model, temperature=0, openai_api_key=opeai_api_key)
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
		response = chain_with_history.invoke({"question": "Hi! I'm bob"}, config=config)
		return response




# from langchain_openai import OpenAI
# from langchain.prompts import PromptTemplate
# from langchain.memory import ConversationBufferMemory
# from langchain_community.chat_message_histories import RedisChatMessageHistory
# from langchain.chains import ConversationChain


# # Note: Copied the default template and added extra instructions for code output
# prompt_template = PromptTemplate(
# 	input_variables=["history", "input"],
# 	output_parser=None,
# 	partial_variables={},
# 	template="""
# 	The following is a friendly conversation between a human and an AI.
# 	The AI is talkative and provides lots of specific details from its context. The AI's name is llmBot and it's birth date it 24th April, 2023.
# 	If the AI does not know the answer to a question, it truthfully says it does not know. 
# 	Any programming code should be output in a github flavored markdown code block mentioning the programming language.
	
	
# 	Current conversation:
# 	{history}
# 	Human: {input}
# 	AI:""",
# 	template_format="f-string",
# 	validate_template=True,
# )


# @frappe.whitelist()
# def get_chatbot_response(session_id: str, prompt_message: str) -> str:
# 	# Throw if no key in site_config
# 	# Maybe extract and cache this (site cache)
# 	opeai_api_key = frappe.conf.get("openai_api_key")
# 	openai_model = get_model_from_settings()

# 	if not opeai_api_key:
# 		frappe.throw("Please set `openai_api_key` in site config")

# 	llm = OpenAI(model_name=openai_model, temperature=0, openai_api_key=opeai_api_key)
	# message_history = RedisChatMessageHistory(
	# 	session_id=session_id,
	# 	url=frappe.conf.get("redis_cache") or "redis://localhost:6379/0",
	# )
# 	memory = ConversationBufferMemory(memory_key="history", chat_memory=message_history)
# 	conversation_chain = ConversationChain(llm=llm, memory=memory, prompt=prompt_template)

# 	response = conversation_chain.invoke(prompt_message)
# 	return response


def get_model_from_settings():
	return (
		frappe.db.get_single_value("LLM Bot Settings", "openai_model") or "gpt-3.5-turbo"
	)
