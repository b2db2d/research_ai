from PIL import Image
from flask import Flask, request, json, jsonify, abort, send_file
from pipelines.text_to_image_pipeline import Text2ImagePipeline
from io import StringIO, BytesIO
import base64

app = Flask(__name__)
config_path = 'config/animal_variation.yaml'
pipe = Text2ImagePipeline(config_path)

@app.route('/generate_single_view', methods=["POST"])
def generate_single_view():
    if request.method == 'POST':
        data = request.get_json()
        prompt = data["prompt"]
        image = pipe(prompt, path=None)

        buffer = BytesIO()
        image.save(buffer, 'png')
        buffer.seek(0)        
        
        data = buffer.read()
        data = base64.b64encode(data).decode()

        return jsonify({'image': data})
        
if __name__ == "__main__":
    app.run()