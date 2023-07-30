from flask import Flask, render_template, request
import openai
import requests
import json

app = Flask(__name__)

openai.api_key = "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"

def query_vectara(customer_id, corpus_id, query, endpoint, api_key, auth_token):
    url = f"https://{endpoint}/v1/query"
    headers = {
        "x-api-key": api_key,
        "customer-id": str(customer_id),
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    
    query_data = {
        "query": [
            {
                "query": query,
                "numResults": 10,
                "corpusKey": [
                    {
                        "customerId": customer_id,
                        "corpusId": corpus_id
                    }
                ]
            }
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=query_data)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        return [f"Request to Vectara failed: {err}"]
    
    results = response.json()
    text_list = []
    try:
        for result in results['responseSet'][0]['response']:
            text_list.append(result['text'])
    except KeyError:
        return [f"Unexpected response structure from Vectara."]
    
    return text_list
    url = f"https://{endpoint}/v1/query"
    headers = {
        "x-api-key": api_key,
        "customer-id": str(customer_id),
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }

    query_data = {
        "query": [
            {
                "query": query,
                "numResults": 10,
                "corpusKey": [
                    {
                        "customerId": customer_id,
                        "corpusId": corpus_id
                    }
                ]
            }
        ]
    }
    
    response = requests.post(url, headers=headers, json=query_data)
    
    if response.status_code == 200:
        results = response.json()
        text_list = []
        for result in results['responseSet'][0]['response']:
            text_list.append(result['text'])
        return text_list
    else:
        return [f"Request failed with status code {response.status_code}"]

def sendQus(com, additional_info):
    prompt = ("This bot is a customer service agent for a company called Five Seasons which is a company that specialized in optical and selling glasses. The company has different branches. In the reply the bot should be welcoming but not greeting the costumer using the Islamic greets unless the costumer use it. The bot will receive the customer's complaint in text form, analyze it, and respond with an apologetic and friendly tone in the Saudi Najdi dialect. Please provide a solution to the customer's issue with detailed steps based on the information the customer has provided in the following complaint. Make sure the reply is in the Saudi Najdi dialect and use emojis when necessary. Also, make sure the reply is consistent with the Saudi culture and sounds like Saudis. If needed provide like a to-do-list to the costumer. Also please depends first on the information provided to CHatgpt through Vectara API:\n\n"
                "Complaint: {}\n\nsummarize and add this Additional info: {}\n\nSuggested reply in the Saudi Najdi dialect. This reply should be very concise and to the poin. Be welcoming but do not greet with the Islamic greet if the costumer did not greet you with that:".format(com, additional_info))

    message_pairs = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": com}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_pairs,
    )
    bot_message = response['choices'][0]['message']['content'].strip()
    return bot_message

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        complaint = request.form['complaint']

        customer_id = 4199489844
        corpus_id = 4
        endpoint = "h.serving.vectara.io"
        api_key = "zqt_-k8hNDnFUtiFs9cJRkFAYyiLrLyn_UNlQRTWdQ"
        auth_token = "your_auth_token"
        
        vectara_data = query_vectara(customer_id, corpus_id, complaint, endpoint, api_key, auth_token)
        response = sendQus(complaint, vectara_data)
        return render_template('index.html', response=response, complaint=complaint)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
