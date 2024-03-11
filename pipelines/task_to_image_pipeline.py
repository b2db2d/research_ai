from PIL import Image
from pipelines.text_to_image_pipeline import Text2ImagePipeline
import requests
import json
import base64

class Task2ImagePipeline(Text2ImagePipeline):
    def __init__(self, config: str) -> None:
        super().__init__(config)
        self.base_url = "http://127.0.0.1:8000"
        self.template_image_path = self.cfg.vlm_template_image_path
        self.vlm_model = self.cfg.vlm_model
        self.vlm_max_tokens = self.cfg.vlm_max_tokens
        self.vlm_temperature = self.cfg.vlm_temperature
        self.vlm_top_p = self.cfg.vlm_top_p
        self.vlm_use_stream = self.cfg.vlm_use_stream
        self.vlm_task_to_prompt_template = self.cfg.vlm_task_to_prompt_template
    
    def get_text_from_task(self, task_description:str):
        if self.template_image_path is not None:
            img_url = f"data:image/png;base64,{self.encode_image(self.template_image_path)}"
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text", "text": f"{self.vlm_task_to_prompt_template} '{task_description}'.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": img_url
                        },
                    },
                ],
            }
        ]

        post_data = {
            "model": self.vlm_model,
            "messages": messages,
            "stream": self.vlm_use_stream,
            "max_tokens": self.vlm_max_tokens,
            "temperature": self.vlm_temperature,
            "top_p": self.vlm_top_p
        }

        response = requests.post(f"{self.base_url}/v1/chat/completions", json=post_data, stream=self.vlm_use_stream)
        if response.status_code == 200:
            if self.vlm_use_stream:
                for line in response.iter_lines():
                    if line:
                        decoded_line = line.decode('utf-8')[6:]
                        try:
                            response_json = json.loads(decoded_line)
                            content = response_json.get("choices", [{}])[0].get("delta", {}).get("content", "")
                            return content
                        except:
                            print("Special Token:", decoded_line)
            else:
                decoded_line = response.json()
                content = decoded_line.get("choices", [{}])[0].get("message", "").get("content", "")
                return content
        else:
            print("Error:", response.status_code)
            return None

    def encode_image(self, image_path):
        """
        Encodes an image file into a base64 string.
        Args:
            image_path (str): The path to the image file.

        This function opens the specified image file, reads its content, and encodes it into a base64 string.
        The base64 encoding is used to send images over HTTP as text.
        """

        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def __call__(self, task_description: str, path: str = "test.png") -> Image:
        prompt = self.get_text_from_task(task_description)
        return super().__call__(prompt, path)