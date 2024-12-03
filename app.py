from flask import Flask, render_template, request, jsonify
from model.gpt_neo import EnhancedChatbot

app = Flask(__name__)
chatbot = EnhancedChatbot()

@app.route("/")
def home():
    return render_template("index.html")  # Page d'accueil du chatbot

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"response": "Je n'ai pas compris votre question. Veuillez réessayer."})
    
    response = chatbot.generate_response(user_message)
    return jsonify({"response": response})

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)

