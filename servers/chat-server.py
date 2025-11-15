# Example chat server
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import torch
from transformers import pipeline, AutoTokenizer
import os


app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

modelsPath = {
    "Llama-3.2-3B-Instruct": "D:/Web/Llama-3.2-3B-Instruct",
}

pipe = None
tokenizer = None
current_model = None
device = "cuda" if torch.cuda.is_available() else "cpu"


def load_model(model_name: str) -> tuple[bool, str]:
    """
    Load model

    Args:
        model_name (str): Model name

    Returns:
        bool: True if model loaded successfully, False otherwise
    """
    global current_model, pipe, tokenizer
    if device == "cuda":
        torch.cuda.empty_cache()

    try:
        tokenizer = AutoTokenizer.from_pretrained(modelsPath[model_name])
        pipe = pipeline(
            "text-generation",
            model=modelsPath[model_name],
            tokenizer=tokenizer,
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            device_map="auto",
        )
        current_model = model_name
    except Exception as e:
        return False, f"Failed to load {model_name}: {str(e)}"

    return True, f"{model_name} loaded successfully"


@app.route("/api/load-model", methods=["POST"])
def load_model_endpoint() -> Response:
    data = request.json
    model_name = data.get("model")

    if model_name not in modelsPath:
        return jsonify({"success": False, "message": f"Unkown {model_name}"})

    if not os.path.exists(modelsPath[model_name]):
        return jsonify({"success": False, "message": f"{model_name} doesn't exist"})

    ret, res = load_model(model_name)
    return jsonify({"success": ret, "message": res})


def generate_response(prompt: str, config: dict) -> str:
    """
    Generate response from the model

    Args:
        prompt (str): Prompt
        config (dict): Configuration

    Returns:
        str: Response
    """
    global pipe, tokenizer
    if pipe is None:
        return ""

    outputs = pipe(
        prompt,
        max_new_tokens=int(config["maxTokens"]),
        temperature=float(config["temperature"]),
        top_p=float(config["topP"]),
        do_sample=True,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.pad_token_id,
        bos_token_id=tokenizer.bos_token_id,
    )

    response = outputs[0]["generated_text"][-1]["content"]
    return response


@app.route("/api/generate", methods=["POST"])
def generate_endpoint() -> Response:
    data = request.json
    prompt = data.get("prompt")
    config = data.get("config", {})

    if not current_model:
        return jsonify({"success": False, "message": "No model loaded"})

    if not prompt:
        return jsonify({"success": False, "message": "Prompt is required"})

    try:
        response = generate_response(prompt, config)
        return jsonify(
            {"success": True, "message": "Generate done", "response": response}
        )
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


def unload_model() -> bool:
    """
    Unload the current model

    Returns:
        bool: True if model unloaded successfully, False otherwise
    """
    global pipe, current_model

    try:
        del pipe
        if device == "cuda":
            torch.cuda.empty_cache()

        pipe = None
        current_model = None
    except Exception as e:
        return False

    return True


@app.route("/api/unload-model", methods=["POST"])
def unload_model_endpoint() -> Response:
    """
    Unload the current model

    Returns:
        Response: Response
    """
    if pipe is None:
        return jsonify({"success": False, "message": "No model loaded"})

    if unload_model():
        return jsonify({"success": True, "message": "Model unloaded successfully"})
    else:
        return jsonify({"success": False, "message": "Failed to unload model"})


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
