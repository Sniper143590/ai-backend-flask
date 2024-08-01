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

print(OPENAI_API_KEY)

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

def get_response(query, llm, promptContext, chatSession):
    model = ChatOpenAI(openai_api_key=os.getenv(OPENAI_API_KEY), model=llm)
    print(llm)
    prepend = "Please format the response in HTML tags which wrapped with div without any code symbol like ``` so that I can directly add it in div tag with following additional rules: 1. the text inside of h tag should be bold 2. Insert <br/> instead of '\n\n' and below of h2 tag to display the and in the way that OpenAI's ChatGPT does."
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

    results = wrapped_chain.invoke(query, config={"configurable": {"session_id": chatSession}})
    # for result in results:
    #     yield result
    # result = model.invoke(messages)
    return parser.invoke(results)

def get_response1(query, llm, promptContext, chatSession):
    try:
        model = ChatOpenAI(openai_api_key=os.getenv(OPENAI_API_KEY), model=llm)
        print(llm)
        prepend = "Please format the response in markdown text."
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
        response_text = "" 
        results = wrapped_chain.invoke(query, config={"configurable": {"session_id": chatSession}})
        # for result in results:  # Use async for to iterate over the generator
        #     # print(result)
        #     yield result
        #     response_text += result 
        return results
        # result = model.invoke(messages)
        # return parser.invoke(results)
    except Exception as e:
        print(str(e))
        return 'Backend Error'
     

def preprompt_generate(response, presetButtonPrompt):
    limit = ' Each query must be between 20 and 30 characters and a simple and short sentence'
    prompt = f'Q: Give me 6 different related queries with {response} based on following instruction: {presetButtonPrompt}.{limit} A:'
    response = openai.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": "You are a helpful related topic generator. Only provide 6 topics at once."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content