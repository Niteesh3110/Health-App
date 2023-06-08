#IMPORTS
import os
from dotenv import load_dotenv, find_dotenv
from flask import Flask, request, jsonify, render_template
import openai as op

#API KEY GOES HERE

load_dotenv(find_dotenv())

op.api_key = os.getenv('openAI')

#Initilizing flask app 
app = Flask(__name__)

#messages is giving AI the information
messages = [{
	'role': 'system',
	'content': 'You are an AI specialised in health. Do not answer irrelevant questions'
}]

#This is where the app access json data coming from openai API
@app.route('/api/chat', methods=['POST'])
def chat():
	condition = request.json['condition']
	severity = request.json['severity']
	user_input = request.json['user_input']

	#Here the app is taking values from the html form and giving it to the AI
	messages.append({
		'role': 'user',
		'content': f"My Health Condition is {condition} and my health severity scale is {severity} {user_input}",
		})

	#Accessing the data here
	chat = op.ChatCompletion.create(
			model="gpt-3.5-turbo",
			messages=messages
		)
	reply = chat.choices[0].message.content
	messages.append({
		'role': 'assistant',
		'content': reply
		})

	return jsonify(reply)

#Routing and rendering is done here
@app.route('/')
def index():
	return render_template('index.html')

if __name__ == '__main__':
	app.run()
