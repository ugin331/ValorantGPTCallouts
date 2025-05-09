from src.image import *
from src.gpt import GPTClient
import time
import src.bot

# so testing on mac works
try:
    from src.screen import ScreenshotClient
except ImportError:
    from src.screen_mac import ScreenshotClient

client = ScreenshotClient()
gpt = GPTClient()
time.sleep(5)
cap = client.mss_capture()
im = sct_to_PIL(cap)
save_PIL_to_disk(im)
base64 = b64_encode(im)

# print(base64)

response = gpt.prompt(base64)
print(response)
gpt.audio_prompt(response)

client.cleanup()
