import base64
from io import BytesIO
from PIL import Image

def bitmap_to_PIL(bmpinfo, bmpstr):
    im = Image.frombuffer('RGB', 
                          (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                          bmpstr, 'raw', 'BGRX', 0, 1)
    im_small = im.resize((bmpinfo['bmWidth'] // 2, bmpinfo['bmHeight'] // 2), Image.LANCZOS)
    return im_small

def sct_to_PIL(cap):
    im = Image.frombytes('RGB', cap.size, cap.rgb)
    im_small = im.resize((cap.width // 2, cap.height // 2), Image.LANCZOS)
    return im_small

def save_PIL_to_disk(image):
    image.save('./test.jpg', format='JPEG', quality=50, optimize=True)

def b64_encode(image):
    buffer = BytesIO()
    image.save(buffer, format='JPEG', quality=50, optimize=True)
    buffer.seek(0)
    b64_str = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    return b64_str