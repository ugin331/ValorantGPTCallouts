from openai import OpenAI
import credentials

prompt = """You are a professional esports player for the first person shooter VALORANT. You are your team's In Game Leader (IGL), meaning you must make spur-of-the-moment decisions during rounds for where your team should go, how aggressively they should play, etc. In this scenario, I will send you screengrabs of rounds of VALORANT currently being played.
Utilize all the information provided to instruct the currently active player and their team on what they should do in that very moment. This should be an action for the player and their teammates, like "Go B, Breach should stun main" or "Fall back from A and go B, there are too many at this site".
If it is still buy phase, give an overall strategy for the team.
Be concise; every second matters in VALORANT, after all! Therefore, provide two sentences of instructions at most. The current round state will follow this message."""


class GPTClient:
    def __init__(self):
        self.gpt_client = OpenAI(api_key=credentials.OPENAI_API_KEY)

    def prompt(self, base64):
        message = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpg;base64,{base64}",
                        },
                    },
                ],
            }
        ]

        response = self.gpt_client.chat.completions.create(
            model="gpt-4.1",
            messages=message,
            max_completion_tokens=150,
        )
        # print(response)

        response_msg = response.choices[0].message.content
        return response_msg

    def audio_prompt(self, text):
        with self.gpt_client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice="coral",
            input=text,
            instructions="You are a professional esports player for the first person shooter VALORANT. You are your team's In Game Leader (IGL), so make sure to speak with clarity, confidence, and authority.",
            speed=3,
        ) as response:
            response.stream_to_file("audio.wav")
