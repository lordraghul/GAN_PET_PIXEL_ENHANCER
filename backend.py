# backend.py
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
import tensorflow as tf
import numpy as np
import io
from PIL import Image
import os
from model import resolve_single
from utils import load_image
from model.srgan import generator

app = FastAPI()

# Config GPU
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
    except RuntimeError as e:
        print(e)
else:
    print("⚠ Aucun GPU détecté — fallback sur CPU")

# Dossier des poids
WEIGHTS_DIR = 'weights/srgan'
weights_file = lambda filename: os.path.join(WEIGHTS_DIR, filename)

# Chargement des modèles une seule fois
print("🔧 Chargement des modèles SRGAN...")
pre_generator = generator()
gan_generator = generator()
pre_generator.load_weights(weights_file('pre_generator.weights.h5'))
gan_generator.load_weights(weights_file('gan_generator.weights.h5'))
print("✅ Modèles chargés.")

def process_srgan(image_bytes):
    # Charger image basse résolution
    lr = load_image(io.BytesIO(image_bytes))

    # Résolution via les deux modèles
    pre_sr = resolve_single(pre_generator, lr)
    gan_sr = resolve_single(gan_generator, lr)

    # Convertir en image PIL (pour export)
    gan_img = Image.fromarray((gan_sr * 255).astype(np.uint8))
    buf = io.BytesIO()
    gan_img.save(buf, format="PNG")
    buf.seek(0)
    return buf

@app.post("/superres")
async def superres(file: UploadFile = File(...)):
    image_bytes = await file.read()
    result_buffer =_
