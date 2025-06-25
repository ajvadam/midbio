from flask import Flask, request, jsonify
from gradio_client import Client

app = Flask(__name__)
client = Client("finegrain/finegrain-object-cutter")


@app.route("/cut", methods=["POST"])
def cut():
    try:
        data = request.get_json()
        base64_code = data.get("name")
        prompt = data.get("prompt", "chair")  # default prompt

        if not base64_code:
            return jsonify({"error": "Missing base64 input"}), 400

        # Format base64 into a data URI
        image_data = f"data:image/png;base64,{base64_code}"

        result = client.predict(img={ 'url' : image_data},
                                prompt=prompt,
                                api_name="/process_prompt")

        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
