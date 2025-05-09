from image import *
from screen import ScreenshotClient
from gpt import GPTClient
import time

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

client.cleanup()