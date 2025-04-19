from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

# Simple scripted chatbot responses simulating therapist and friend tones
therapist_responses = {
    "hello": "Hello, how are you feeling today?",
    "sad": "I'm sorry to hear that you're feeling sad. Would you like to talk about it?",
    "anxious": "Anxiety can be tough. Let's try some deep breathing exercises together.",
    "help": "I'm here to listen. Please tell me more about what's troubling you.",
    "default": "I understand. Can you please elaborate more on that?"
}

friend_responses = {
    "hello": "Hey! I'm here for you. What's up?",
    "sad": "I'm sorry you're feeling down. Want to chat about it?",
    "anxious": "Take a deep breath, buddy. We got this!",
    "help": "I'm here to support you. Tell me what's on your mind.",
    "default": "I'm listening. Go on."
}
# Define response dictionaries
therapist_responses = {
    "stress": "Can you tell me more about what's causing stress?",
    "anxiety": "Have you tried deep breathing exercises?",
    "default": "Let's explore some ways to manage these feelings."
}

friend_responses = {
    "happy": "That's great to hear! What's making you happy?",
    "sad": "I'm here for you. Want to talk about it?",
    "default": "Tell me more, I'm listening!"
}

# Function to return chatbot response
def get_chatbot_response(message, mode):
    message = message.lower()  # Normalize input

    if mode == "therapist":
        for key in therapist_responses:
            if key in message:
                return therapist_responses[key]
        return therapist_responses["default"]

    elif mode == "friend":
        for key in friend_responses:
            if key in message:
                return friend_responses[key]
        return friend_responses["default"]

    else:
        return "I'm not sure how to respond. Try selecting 'therapist' or 'friend' mode."

# Example usage
user_message = "I'm feeling anxious today."
print(get_chatbot_response(user_message, "therapist"))
  # Define response dictionaries
therapist_responses = {
    "stress": "Can you tell me more about what's causing stress?",
    "anxiety": "Have you tried deep breathing exercises?",
    "default": "Let's explore some ways to manage these feelings."
}

friend_responses = {
    "happy": "That's great to hear! What's making you happy?",
    "sad": "I'm here for you. Want to talk about it?",
    "default": "Tell me more, I'm listening!"
}

# Function to return chatbot response
def get_chatbot_response(message, mode):
    message = message.lower()  # Normalize input
    
    if mode == "therapist":
        for key in therapist_responses:
            if key in message:
                return therapist_responses[key]
        return therapist_responses["default"]

    elif mode == "friend":
        for key in friend_responses:
            if key in message:
                return friend_responses[key]
        return friend_responses["default"]

    else:
        return  "I'm not sure how to respond. Try selecting 'therapist' or 'friend' mode." 


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get("message", "")
    mode = data.get("mode", "therapist")
    response = get_chatbot_response(message, mode)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
###front end
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Emotional Support Chatbot</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" />
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet" />
    <style>
        body {
            font-family: 'Roboto', sans-serif;
        }
    </style>
</head>
<body class="bg-gray-50 min-h-screen flex flex-col">
    <header class="bg-blue-600 text-white p-4 text-center text-2xl font-semibold">
        Emotional Support Chatbot
    </header>

    <main class="flex-grow container mx-auto p-4 max-w-4xl">
        <section class="mb-8">
            <h2 class="text-xl font-bold mb-4">Chatbot</h2>
            <div class="border rounded-lg p-4 bg-white shadow-md flex flex-col h-96">
                <div id="chat-window" class="flex-grow overflow-y-auto mb-4 space-y-3">
                    <!-- Chat messages will appear here -->
                </div>
                <div class="flex space-x-2">
                    <select id="mode-select" class="border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400">
                        <option value="therapist">Therapist</option>
                        <option value="friend">Friend</option>
                    </select>
                    <input id="user-input" type="text" placeholder="Type your message..." class="flex-grow border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400" />
                    <button id="send-btn" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition">Send</button>
                </div>
            </div>
        </section>

        <section class="mb-8">
            <h2 class="text-xl font-bold mb-4">Exercises to Deal with Emotions</h2>
            <ul class="list-disc list-inside space-y-2 bg-white p-4 rounded shadow-md">
                <li>Practice deep breathing: Inhale slowly for 4 seconds, hold for 7 seconds, and exhale for 8 seconds.</li>
                <li>Write down your feelings in a journal daily.</li>
                <li>Take a short walk outside to clear your mind.</li>
                <li>Try progressive muscle relaxation to reduce tension.</li>
                <li>Practice mindfulness meditation for 5-10 minutes.</li>
            </ul>
        </section>

        <section>
            <h2 class="text-xl font-bold mb-4">Helpline Numbers</h2>
            <ul class="list-disc list-inside space-y-2 bg-white p-4 rounded shadow-md">
                <li>National Suicide Prevention Lifeline: 1-800-273-8255</li>
                <li>Crisis Text Line: Text HOME to 741741</li>
                <li>Substance Abuse and Mental Health Services Administration (SAMHSA): 1-800-662-HELP (4357)</li>
                <li>National Domestic Violence Hotline: 1-800-799-7233</li>
                <li>Veterans Crisis Line: 1-800-273-8255 (Press 1)</li>
            </ul>
        </section>
    </main>

    <footer class="bg-blue-600 text-white p-4 text-center">
        &copy; 2024 Emotional Support Project
    </footer>

    <script src="main.js"></script>
</body>
</html>
###jss
document.addEventListener("DOMContentLoaded", () => {
    const chatWindow = document.getElementById("chat-window");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");
    const modeSelect = document.getElementById("mode-select");

    function appendMessage(sender, message) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("p-2", "rounded", "max-w-xs", "break-words");
        if (sender === "user") {
            messageDiv.classList.add("bg-blue-600", "text-white", "self-end");
        } else {
            messageDiv.classList.add("bg-gray-200", "text-gray-900", "self-start");
        }
        messageDiv.textContent = message;
        chatWindow.appendChild(messageDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        appendMessage("user", message);
        userInput.value = "";
        userInput.disabled = true;
        sendBtn.disabled = true;

        try {
            const response = await fetch("http://127.0.0.1:5000/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    message: message,
                    mode: modeSelect.value,
                }),
            });
            const data = await response.json();
            appendMessage("bot", data.response);
        } catch (error) {
            appendMessage("bot", "Sorry, there was an error connecting to the server.");
        } finally {
            userInput.disabled = false;
            sendBtn.disabled = false;
            userInput.focus();
        }
    }

    sendBtn.addEventListener("click", sendMessage);
    userInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            sendMessage();
        }
    });
});
