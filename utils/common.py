from database.firebase import db
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
import openai 

load_dotenv()
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
parser = StrOutputParser()
openai.api_key = OPENAI_API_KEY

def get_response(query, llm, promptContext):
    model = ChatOpenAI(openai_api_key=os.getenv(OPENAI_API_KEY), model=llm)
    print(llm)
    messages = [
        SystemMessage(content=promptContext),
        HumanMessage(content=query),
    ]

    result = model.invoke(messages)
    return parser.invoke(result)

def preprompt_generate(query):
    limit = ' Each query must be between 50 and 80 characters'
    prompt = f'Q: Give me 3 different related queries with {query}.{limit} A:'
    response = openai.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": "You are a helpful related topic generator. Only provide 3 topics at once."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content