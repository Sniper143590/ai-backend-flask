from flask import Blueprint, request, jsonify, current_app, Response, stream_with_context
from utils.common import get_response, get_response1, preprompt_generate
import asyncio
llm_blueprint = Blueprint('llm_blueprint', __name__)

@llm_blueprint.route('/query', methods=['POST'])
def query():
    try:
        data = request.get_json()
        query = data['query']
        llm = data['llm']
        promptContext = data['promptContext']
        lastThreeConversations = data['lastThreeConversations']
        presetButtonPrompt = data['presetButtonPrompt']
        chatSession = data['chatSession']
        print("History ---- >>", lastThreeConversations)
        response = get_response(query, llm, promptContext, chatSession)
        preprompts = preprompt_generate(response, presetButtonPrompt )
        preprompts = preprompts.replace('1. ', '').replace('2. ', '').replace('3. ', '').replace('4. ', '').replace('5. ', '').replace('6. ', '').replace('. ', '.').replace('"','')
        preprompts = preprompts.split('\n')
        print(preprompts)
        return jsonify({"message": response, "preprompts":preprompts}), 201
    except Exception as e:
        print(e)
        return jsonify({"messsage": "Backend Error"}), 500
        
@llm_blueprint.route('/query1', methods=['POST'])
def query1():
    try:
        data = request.get_json()
        query = data['query']
        llm = data['llm']
        promptContext = data['promptContext']
        lastThreeConversations = data['lastThreeConversations']
        presetButtonPrompt = data['presetButtonPrompt']
        chatSession = data['chatSession']
        print("History ---- >>", lastThreeConversations)
        response = get_response1(query, llm, promptContext, chatSession)
        print(response)
        preprompts = preprompt_generate(response, presetButtonPrompt )
        preprompts = preprompts.replace('1. ', '').replace('2. ', '').replace('3. ', '').replace('4. ', '').replace('5. ', '').replace('6. ', '').replace('. ', '.').replace('"','')
        preprompts = preprompts.split('\n')
        print(response)
        return jsonify({"message": response, "preprompts":preprompts}), 201
    except Exception as e:
        print(e)
        return jsonify({"messsage":"Backend Error"}), 500

@llm_blueprint.route('/refresh-preset-prompts', methods=['POST'])
def refresh_preset_prompts():
    try:
        data = request.get_json()
        query = data['query']
        presetButtonPrompt = data['presetButtonPrompt']
        preprompts = preprompt_generate(query, presetButtonPrompt)
        print(preprompts)
        preprompts = preprompts.replace('1. ', '').replace('2. ', '').replace('3. ', '').replace('4. ', '').replace('5. ', '').replace('6. ', '').replace('. ', '.').replace('"','')
        preprompts = preprompts.split('\n')
        print(preprompts)
        return jsonify({'preprompts':preprompts}), 201
    except Exception as e:
        print(e)
        return jsonify({'preprompts':[]}), 500
# @llm_blueprint.route('/create', methods=['POST'])
# def create_document():
#     data = request.get_json()
#     db.collection('users').add(data)
#     return jsonify({"message": "Document successfully created"}), 201

# @llm_blueprint.route('/read/<string:id>', methods=['GET'])
# def read_document(id):
#     doc_ref = db.collection('users').document(id)
#     doc = doc_ref.get()
#     if doc.exists:
#         return jsonify(doc.to_dict()), 200  
#     else:
#         return jsonify({"error": "No such document!"}), 404

# @llm_blueprint.route('/update/<string:id>', methods=['PUT'])
# def update_document(id):
#     data = request.get_json()
#     db.collection('users').document(id).set(data)
#     return jsonify({"message": "Document successfully updated"}), 200

# @llm_blueprint.route('/delete/<string:id>', methods=['DELETE'])
# def delete_document(id):
#     db.collection('users').document(id).delete()
#     return jsonify({"message": "Document successfully deleted"}), 200