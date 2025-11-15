# Example draw server
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import sys
from transformers import CLIPTokenizer
from PIL import Image
import torch
import json
import io
import base64
import gc

path = ""  #  path to sd folder
sys.path.append(path)
try:
    from sd import pipeline  # type: ignore
    from sd.model_loader import preload_models_from_standard_weights  # type: ignore
except ImportError as e:
    print(f"Error importing sd module: {e}")
    sys.exit(0)


app = Flask(__name__)
CORS(app)


device = "cuda" if torch.cuda.is_available() else "cpu"
model_file = f"{path}/data/v1-5-pruned-emaonly.ckpt"
models = {}


@app.route("/api/load-models", methods=["POST"])
def load_model_endpoint() -> Response:
    global models
    try:
        if device == "cuda":
            torch.cuda.empty_cache()

        models = preload_models_from_standard_weights(model_file, "cpu")
        return jsonify({"success": True, "message": "Models loaded successfully"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


@app.route("/api/generate", methods=["POST"])
def generate_endpoint() -> Response:
    global models

    if not models:
        return jsonify({"success": False, "message": "No model loaded"})

    prompt = request.form.get("prompt")
    uncond_prompt = request.form.get("uncond_prompt")
    config = request.form.get("config", {})
    image = request.files.get("image", None)

    config = json.loads(config) if config else {}
    input_image = Image.open(image.stream) if image else None

    try:
        tokenizer = CLIPTokenizer(
            f"{path}/data/vocab.json", merges_file=f"{path}/data/merges.txt"
        )
        output = pipeline.generate(
            prompt=prompt,
            uncond_prompt=uncond_prompt,
            input_image=input_image,
            strength=float(config["strength"]),
            do_cfg=config["do_cfg"],
            cfg_scale=float(config["cfg_scale"]),
            sampler_name=config["sampler"],
            n_inference_steps=int(config["steps"]),
            seed=int(config["seed"]),
            models=models,
            device=device,
            idle_device="cpu",
            tokenizer=tokenizer,
        )

        output = Image.fromarray(output)

        # Save image to buffer
        buffer = io.BytesIO()
        output.save(buffer, format="PNG")
        buffer.seek(0)
        img_str = base64.b64encode(buffer.getvalue()).decode()

        # Release GPU memory
        if device == "cuda":
            torch.cuda.empty_cache()

        del models
        del tokenizer
        del output
        gc.collect()

        models = {}

        return jsonify(
            {"success": True, "message": "generate successfully", "image": img_str}
        )
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


if __name__ == "__main__":
    app.run(host="localhost", port=5001, debug=True)
