import os
import getpass
from flask import Flask, request, jsonify, make_response
from dotenv import load_dotenv
from api.llm import llm_blueprint
from langchain_core.output_parsers import StrOutputParser
from flask_cors import CORS

parser = StrOutputParser()
app = Flask(__name__)

app.register_blueprint(llm_blueprint, url_prefix='/api')


from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
load_dotenv()
CORS(app)

@app.route("/")
def index():
    model = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4")
    messages = [
        SystemMessage(content="You are a helpful assistant"),
        HumanMessage(content="hi!"),
    ]

    result = model.invoke(messages)
    # db.drop_all()
    # del_all_records()
    
    # print('Deleted')
    return parser.invoke(result)

if __name__ == '__main__':
    app.run(debug=True)