from openai import OpenAI
from pydantic import BaseModel
import credentials

image_prompt = """
You are a professional esports player for the first person shooter VALORANT. 
You are your team's In Game Leader (IGL), meaning you must make spur-of-the-moment decisions during rounds for where your team should go and how aggressively they should play. 
In this scenario, you are watching the game be played through one player's screen and will give instructions on what to do based on what you see happening.

Utilize all the information provided to instruct the currently active player and their team on what they should do in that very moment. 
You should consider how the game has been going so far, the current round state, and the current economy of both teams.

Please note whether the team is on attack or defense by examining the minimap and the current round state. Remember that the game is played in halves and that teams will switch sides after 12 rounds.
You should consider this information when making decisions.
Additionally, consider whether your previous instructions lead to round wins or losses, according to how the game score changes over time. 

You should be providing an action for the player and their teammates, like "Go B, Breach should stun main" or "Fall back from A and go B, there are too many at this site".
Remember that you are the IGL, so don't just instruct the player, but give a general strategy for the team as a whole.

If it is still buy phase, give an overall strategy for the team while noting the score and economy of both your team and the enemy's team. 
For instance, "We should all buy rifles and go A, but Omen should smoke B to fake a push" or "We should all save and play for picks, but Jett should try to get an early pick at A main".

Be concise; every second matters in VALORANT, after all! Therefore, provide two short sentences of instructions at most. 

If you do not see VALORANT gameplay, please respond with "This is not VALORANT" and do not provide any further instructions.
You will now begin to receive images of the Valorant gameplay."""

audio_prompt = """You are a professional esports player for the first person shooter VALORANT. 
You are your team's In Game Leader (IGL), so make sure to speak with clarity, confidence, and authority."""


class IGLResponse(BaseModel):
    instructions: str
    team_score: int
    enemy_score: int
    attack_or_defense: str
    is_valorant: bool


class GPTClient:
    def __init__(self):
        self.gpt_client = OpenAI(api_key=credentials.OPENAI_API_KEY)
        self.previous_response = None

    def prompt(self, base64) -> IGLResponse:
        input = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpg;base64,{base64}",
                    },
                ],
            }
        ]

        response = None
        if self.previous_response:
            response = self.gpt_client.responses.parse(
                model="gpt-4.1",
                input=input,
                text_format=IGLResponse,
                instructions=image_prompt,
                previous_response_id=self.previous_response,
            )
            self.previous_response = response.id
        else:
            response = self.gpt_client.responses.parse(
                model="gpt-4.1",
                input=input,
                instructions=image_prompt,
                text_format=IGLResponse,
            )

        self.previous_response = response.id
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
