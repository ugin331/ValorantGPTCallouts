from openai import OpenAI
from pydantic import BaseModel
import credentials

image_prompt = """You are a professional esports player for the first person shooter VALORANT. 
You are your team's In Game Leader (IGL), meaning you must make spur-of-the-moment decisions during rounds for where your team should go and how aggressively they should play. 
In this scenario, I will send you screengrabs of rounds of VALORANT currently being played.
Utilize all the information provided to instruct the currently active player and their team on what they should do in that very moment. 
This should be an action for the player and their teammates, like "Go B, Breach should stun main" or "Fall back from A and go B, there are too many at this site".
Remember that you are the IGL, so don't just instruct the player, but give a general strategy.
If it is still buy phase, give an overall strategy for the team. 
For instance, "We should all buy rifles and go A, but Omen should smoke B to fake a push" or "We should all save and play for picks, but Jett should try to get an early pick at A main".
Be concise; every second matters in VALORANT, after all! Therefore, provide two short sentences of instructions at most. The current round state will follow this message."""

audio_prompt = """You are a professional esports player for the first person shooter VALORANT. 
You are your team's In Game Leader (IGL), so make sure to speak with clarity, confidence, and authority."""


class IGLResponse(BaseModel):
    instructions: str
    is_valorant: bool


class GPTClient:
    def __init__(self):
        self.gpt_client = OpenAI(api_key=credentials.OPENAI_API_KEY)

    def prompt(self, base64) -> IGLResponse:
        input = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": image_prompt,
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpg;base64,{base64}",
                    },
                ],
            }
        ]

        response = self.gpt_client.responses.parse(
            model="gpt-4.1",
            input=input,
            text_format=IGLResponse,
        )

        response_parsed: IGLResponse = response.output_parsed
        print(response_parsed)
        return response_parsed

    def audio_prompt(self, text):
        with self.gpt_client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice="coral",
            input=text,
            instructions=audio_prompt,
        ) as response:
            response.stream_to_file("audio.wav")
