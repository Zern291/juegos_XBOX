import requests

TOKEN = "8174192090:AAEqGlNr2MVAIih0kvFYu43eK7PHeONyF5o"

def get_chat_id():
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    response = requests.get(url)
    data = response.json()
    print(data)

if __name__ == "__main__":
    get_chat_id()
