$(document).ready(function () {
    $("#send-btn").click(function () {
        const userInput = $("#user-input").val().trim();
        if (!userInput) return;

        // Afficher le message utilisateur
        $("#messages").append(`<div><strong>Vous:</strong> ${userInput}</div>`);

        // Envoyer la requête au serveur Flask
        $.ajax({
            url: "/chat",
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify({ message: userInput }),
            success: function (response) {
                // Afficher la réponse du chatbot
                $("#messages").append(`<div><strong>Chatbot:</strong> ${response.response}</div>`);
                $("main").scrollTop($("main")[0].scrollHeight); // Auto-scroll
            },
            error: function () {
                $("#messages").append(`<div><strong>Chatbot:</strong> Une erreur est survenue. Réessayez.</div>`);
            },
        });

        // Effacer le champ d'entrée utilisateur
        $("#user-input").val("");
    });
});
