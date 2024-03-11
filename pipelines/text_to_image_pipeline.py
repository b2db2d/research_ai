from diffusers import StableDiffusionPipeline
from omegaconf import OmegaConf
from typing import Any, Callable, Dict, List, Optional, Union
from PIL import Image

class Text2ImagePipeline(object):
    '''
        Generalized pipeline for Text to Image tasks.
        
        Prompt is modified with prefix and trigger-words defined in the config file.
        Then, images are generated using the modified prompt.
    '''
    def __init__(self, config:str) -> None:
        self.cfg = OmegaConf.load(config)
        self.device = self.cfg.device
        self.pipe = StableDiffusionPipeline.from_single_file(self.cfg.base_model_path)
        self.pipe.load_lora_weights(self.cfg.lora_path)
        self.pipe.to(self.device)
        
        self.positive_prefix = self.cfg.positive_prompt_prefix.split(',')
        self.lora_trigger_word = self.cfg.lora_trigger_word.split(',')
        
        self.width = self.cfg.width
        self.height = self.cfg.height
        self.num_inference_steps = self.cfg.num_inference_steps
        self.guidance_scale = self.cfg.guidance_scale
        
    def assemble_prompts(self, prompt:str) -> str:
        '''
            Modifies prompts based on the contents of the config file.
        '''
        full_prompt = ""
        for prefix in self.positive_prefix:
            full_prompt += f"{prefix}, "
        
        for trigger_word in self.lora_trigger_word:
            full_prompt += f"{trigger_word}, "
        full_prompt += prompt
        return full_prompt
    
    def __call__(self, prompt:str, path:str="test.png") -> Image:
        '''
            Diffusion model inference using prompt.
        '''
        prompt = self.assemble_prompts(prompt)
        image = self.pipe(prompt, width=self.width, height=self.height,
                          num_inference_steps=self.num_inference_steps, guidance_scale=self.guidance_scale).images[0]
        if path is not None:
            image.save(path)
        return image, prompt

if __name__ == "__main__":   
    config_path = 'config/animal_variation.yaml'
    p = Text2ImagePipeline(config_path)
    p("a furry green dragonite smiling.")