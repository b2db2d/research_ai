### Summary

This repository contains Text to 3D model generation pipeline.


### Installation

```
pip install -r requirements.txt
```

Download models from, https://drive.google.com/drive/folders/1I5xhnLmaWlR2CDEG-ehAz3zyNoHzzZzi?usp=drive_link, and place safetensors within ***sd1_5***, ***sd1_5_lora*** under ***models/sd1_5***, ***models/sd1_5_lora*** directories, respectively.

### How to use

***app.py*** runs flask api server, and sample usage is written under ***client.py***.

### TODO
- [ ] Open up width/height variable in generating single view pipeline
- [ ] Batch Processing / Multiple Single View Output
- [ ] Fine-tuning MVDream
- [ ] Training Nerf / Gaussian Splatting on large dataset, with augmentation