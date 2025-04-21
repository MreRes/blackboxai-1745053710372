from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Load a free Indonesian language model for text generation or classification
# You can change the model to any suitable open-source model available on Hugging Face
model_name = "indobenchmark/indobert-base-p1"
nlp = pipeline("text-classification", model=model_name)

@app.route('/api/ai', methods=['POST'])
def ai_response():
    data = request.json
    text = data.get('text', '')
    if not text:
        return jsonify({"error": "No input text provided"}), 400

    try:
        result = nlp(text)
        # Process the result to generate a meaningful response
        # For simplicity, return the label with highest score
        label = result[0]['label']
        score = result[0]['score']
        response_text = f"Label: {label}, Confidence: {score:.2f}"
        return jsonify({"response": response_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
