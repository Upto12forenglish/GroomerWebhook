from flask import Flask, request
import requests

# Replace 'YOUR_BOT_API_TOKEN' with your Telegram Bot API token
bot_token = '5859254130:AAG97x57CY4iMFyUz9Lsp0_4wnOAhwL_HgE'

def reply_to_user(message_text, chat_id):
    # Check grammar using the Groomer API
    api_url = "https://upto12forenglish-groomer.hf.space/fullcorrection"
    api_key = "bCD34EfGhIjKlMno"
    input_text = message_text

    # Define the query parameters
    params = {
        "api_key": api_key,
        "input_text": input_text,
    }

    try:
        response = requests.get(api_url, params=params)

        if response.status_code == 200:
            data = response.json()
            print("Correction:", data["correction"])
            print("Mistakes:", data["mistakes"])
        else:
            print("Request failed with status code:", response.status_code)

    except Exception as e:
        print("An error occurred:", e)


    # URL for sending a message using the Telegram Bot API
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'

    # Parameters for the POST request
    params = {
        'chat_id': chat_id,
        'text': data["correction"],
    }

    try:
        response = requests.post(url, data=params)
        data = response.json()
        if data['ok']:
            print(f'Message sent to {chat_id}: {message_text}')
        else:
            print(f'Failed to send the message. Telegram API response: {data}')
    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')
    return '', 200

##########################

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def receive_updates():
    data = request.get_json()
    print("Received Update:")
    print(data)
    chat_id = data['message']['chat']['id']
    message_text = data['message']['text']
    print("Chat id: ", chat_id)
    print("message: ", message_text)

    reply_to_user(message_text, chat_id)
    return {"status": "Update received"}

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0', port=8080)
