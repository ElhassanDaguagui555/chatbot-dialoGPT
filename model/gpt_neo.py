import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

class EnhancedChatbot:
    def __init__(self):
        model_name = "microsoft/DialoGPT-medium"  # Modèle pré-entraîné
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.chat_history_ids = None  # Historique des conversations
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)  # Déplacer le modèle sur GPU si disponible

    def generate_response(self, user_message):
        try:
            # Encode le message utilisateur
            input_ids = self.tokenizer.encode(user_message + self.tokenizer.eos_token, return_tensors="pt").to(self.device)

            # Ajouter l'historique de la conversation
            if self.chat_history_ids is not None:
                input_ids = torch.cat([self.chat_history_ids, input_ids], dim=-1)

            # Générer une réponse avec des paramètres ajustés
            self.chat_history_ids = self.model.generate(
                input_ids,
                max_length=1000,
                pad_token_id=self.tokenizer.eos_token_id,
                temperature=0.6,  # Contrôler la créativité (plus bas = réponses plus cohérentes)
                top_k=40,         # Considérer uniquement les 40 mots les plus probables
                top_p=0.85,       # Probabilité cumulative pour limiter les réponses incohérentes
                repetition_penalty=1.2,  # Réduire les répétitions
                no_repeat_ngram_size=2  # Éviter les répétitions de bigrammes
            )

            # Décoder la réponse générée
            response = self.tokenizer.decode(self.chat_history_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)

            # Nettoyer la réponse pour éviter les répétitions
            response = response.strip()

            # Ajouter des réponses conditionnelles pour des questions fréquentes
            response = self._customize_response(user_message, response)

            return response

        except Exception as e:
            return f"Une erreur s'est produite lors de la génération de la réponse : {str(e)}"

    def _customize_response(self, user_message, response):
        """
        Ajouter des réponses personnalisées pour des questions spécifiques.
        """
        lower_message = user_message.lower()

        if "your name" in lower_message or "who are you" in lower_message:
            return "I'm an enhanced version of DialoGPT!"
        if "how old are you" in lower_message:
            return "I don't have an age, I'm an AI trained by OpenAI."
        if "hello" in lower_message or "hi" in lower_message:
            return "Hello! How can I assist you today?"
        if "bye" in lower_message or "goodbye" in lower_message:
            return "Goodbye! Have a great day!"

        # Si aucune réponse conditionnelle ne correspond, retourner la réponse générée
        return response

# Fonction pour tester le chatbot
if __name__ == "__main__":
    chatbot = EnhancedChatbot()
    print("Chatbot prêt ! Tapez 'exit' pour quitter.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Chatbot: Goodbye!")
            break
        response = chatbot.generate_response(user_input)
        print(f"Chatbot: {response}")
