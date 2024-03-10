import requests
import base64
from PIL import Image
import io

res = requests.post('http://localhost:5000/generate_single_view', json={"prompt":"A black otter."})
encoded_image = res.json()['image']
img = base64.b64decode(encoded_image)
img = Image.open(io.BytesIO(img))
img.save('testing_receive.png')