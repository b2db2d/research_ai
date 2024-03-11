import requests
import base64
from PIL import Image
import io

res = requests.post('http://localhost:5000/generate_single_view', json={"prompt":"Studying for exam."})
encoded_image = res.json()['image']
prompt = res.json()['prompt']
img = base64.b64decode(encoded_image)
img = Image.open(io.BytesIO(img))
img.save('testing_receive.png')

print(prompt)