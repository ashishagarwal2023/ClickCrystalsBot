import requests
import json
from uuid import uuid4

class TokenRateLimitedError(Exception):
    def __init__(self, message="The token is rate limited. Try again later."):
        self.message = message
        super().__init__(self.message)

class Bot:
    def __init__(self, access_token: str):
        self.session = requests.Session()
        self.session.headers["user-agent"] = "node"
        self.access_token = access_token
        self.conversation_id = None

    def token(self, access_token: str):
        self.access_token = access_token
        self.conversation_id = None
    
    def reset(self):
        self.conversation_id = None

    def prompt(self, prompt_text: str) -> str:
        body = {
            "action": "next",
            "conversation_mode": {"kind": "primary_assistant"},
            "force_paragen": False,
            "force_rate_limit": False,
            "history_and_training_disabled": True,
            "messages": [{
                "metadata": {},
                "author": {"role": "user"},
                "content": {"content_type": "text", "parts": [prompt_text]}
            }],
            "model": "text-davinci-002-render-sha",
            "parent_message_id": str(uuid4()),
            "timezone_offset_min": -330
        }

        if self.conversation_id is not None:
            try:
                body["conversation_id"] = self.conversation_id
            except:
                raise TokenRateLimitedError("The token is rate limited. Try again later.")

        response = self.session.post(
            url="https://chat.openai.com/backend-api/conversation",
            headers={
                "accept": "text/event-stream",
                "accept-language": "en-US",
                "authorization": f"Bearer {self.access_token}",
                "content-type": "application/json",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "Referer": "https://chat.openai.com",
                "Referrer-Policy": "strict-origin-when-cross-origin"
            },
            data=json.dumps(body)
        )

        data = {}
        for chunk in response.text.split("\n"):
            if chunk.startswith("data: {\"message\":"):
                try:
                    data = json.loads(chunk[6:])
                except json.JSONDecodeError:
                    raise Exception("Couldn't parse assistant's answer into a valid JSON. Might be a bug.")

        try:
            if data.get("conversation_id", "") != None:
                self.conversation_id = data["conversation_id"]
        except:
            raise TokenRateLimitedError("The token is rate limited. Try again later.")
            
        if data["message"]["status"] != "finished_successfully":
            raise Exception("The bot's message was not finished successfully, might be a error.")

        if data["message"]["content"]["content_type"] != "text":
            raise Exception("The response did not gave the bot's response as text, most likely due to a bug.")

        message_parts = data["message"]["content"]["parts"]
        return "".join(message_parts)