try:
    from flask import Flask, render_template, request, jsonify
    import requests
except:
    import os
    os.system("pip install flask")
    os.system("pip install requests")
    from flask import Flask, render_template, request
    import requests

try:
    from gpt import TokenRateLimitedError, Bot
except:
    raise Exception("No GPT module found. It is required to use this bot.")

app = Flask(__name__, static_url_path='/static')
access_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJnc3RhZHZvY2F0ZXByYXNoYW50QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlfSwiaHR0cHM6Ly9hcGkub3BlbmFpLmNvbS9hdXRoIjp7InBvaWQiOiJvcmctTzJyS2RaM2YwSHVCZnIxTWRndDdmdFJYIiwidXNlcl9pZCI6InVzZXItRE5kUENMR2RvSWlyb1B2b1Q1WGZ4OFViIn0sImlzcyI6Imh0dHBzOi8vYXV0aDAub3BlbmFpLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwNjA4ODUxODk2MTg3NjI1ODc0NiIsImF1ZCI6WyJodHRwczovL2FwaS5vcGVuYWkuY29tL3YxIiwiaHR0cHM6Ly9vcGVuYWkub3BlbmFpLmF1dGgwYXBwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE3MDkzOTg2MTcsImV4cCI6MTcxMDI2MjYxNywiYXpwIjoiVGRKSWNiZTE2V29USHROOTVueXl3aDVFNHlPbzZJdEciLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIG1vZGVsLnJlYWQgbW9kZWwucmVxdWVzdCBvcmdhbml6YXRpb24ucmVhZCBvcmdhbml6YXRpb24ud3JpdGUgb2ZmbGluZV9hY2Nlc3MifQ.ulHceJbCeEwd5zn2u30Xjz1EJiNn8lRBM1PW-BV6p_LAULKdLt_d7FSJdjc9V3w-0B2zaq0a-N4Ebj1lQiv48FJ1vM8SWOYN3Tgg_DYhasRgwYiwMCRgFT5xje0z0eJVZBYpYhOk4YEDSw1ylMyFgITcmTON1bLMkco__7Im6DuAP2Da_PgUJXyhlDTDMSQ5loGz5DiZ2mKIz_eKPerwN4LMTfgMPW-BqFNp0uK-ZKrdpn40Y1MKUqszGkk18mbzfLbw5Sgpo893HusymUAj_FukeeN1LYSSgc9nIUeSIg6aMigdlb6xqF25N8db40cOkW5zCCvQGUlEK469OQwXIA"
bot = Bot(access_token)
print("Bot is ready")

url = "https://raw.githubusercontent.com/ashishagarwal2023/ClickCrystalsXYZ/35eb057ad0b0aa1ca5f8d3d1d3618bcfaaf2dd0b/msg.md"
print("Fetching transcript")
response = requests.get(url)
if response.status_code == 200:
    print("Transcript fetched, prompting it...")
    print(response.text)
    bot.prompt(response.text)
else:
    print("Failed to fetch the URL:", response.status_code)

# main page chat
@app.route('/')
def home():
    return render_template('index.html')

# the get resp
@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input']
    bot_response = bot.prompt(user_input)
    return str(bot_response)

@app.route('/new_chat', methods=['POST'])
def new_chat():
    bot.reset()
    return jsonify({'message': 'Chat session reset successfully'})

if __name__ == '__main__':
    app.run()