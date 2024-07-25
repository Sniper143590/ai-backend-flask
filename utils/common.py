from database.firebase import db
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
import openai 

load_dotenv()
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
parser = StrOutputParser()
openai.api_key = OPENAI_API_KEY

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

def get_response(query, llm, promptContext):
    model = ChatOpenAI(openai_api_key=os.getenv(OPENAI_API_KEY), model=llm)
    print(llm)
    prepend = "Please format the response in HTML tags so that I can display the response in the way that OpenAI's ChatGPT does."
    promptContext = prepend + promptContext
    messages = [
        SystemMessage(content=promptContext),
        HumanMessage(content=query),
    ]
    system_message_prompt = SystemMessagePromptTemplate.from_template(promptContext)

    human_message_prompt = HumanMessagePromptTemplate.from_template(query)

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, MessagesPlaceholder(variable_name="chat_history"), human_message_prompt]
    )
    chain = chat_prompt | ChatOpenAI(openai_api_key=os.getenv(OPENAI_API_KEY), model=llm) | StrOutputParser()

    wrapped_chain = RunnableWithMessageHistory(chain, get_session_history)

    result = wrapped_chain.invoke(query, config={"configurable": {"session_id": "abc123"}})
    print("result>>>", result)
    return result
    # result = model.invoke(messages)
    # return parser.invoke(result)

def preprompt_generate(query, presetButtonPrompt):
    limit = ' Each query must be between 30 and 40 characters'
    prompt = f'Q: Give me 6 different related queries with {query} based on following instruction: {presetButtonPrompt}.{limit} A:'
    response = openai.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": "You are a helpful related topic generator. Only provide 6 topics at once."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content