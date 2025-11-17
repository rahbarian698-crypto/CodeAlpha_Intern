def chatbot():
    # Welcome banner
    print("=====================================")
    print(" 🤖  WELCOME TO PYTHON CHATBOT   🤖")
    print("======================================")
    print(" Type 'bye' anytime to exit.")
    print()

    # Big dictionary of replies
    responses = {
        "hello": "Hi there!",
        "hi": "Hello!",
        "hey": "Hey! How can I help?",
        "how are you": "I'm doing great, thanks!",
        "what is your name": "I am your Python Chatbot.",
        "who made you": "I was created by Muhammad!",
        "thanks": "You're welcome!",
        "thank you": "Happy to help!",
        "bye": "Goodbye! Take care.",
        "goodbye": "See you soon!",
        "what can you do": "I can chat with you and reply to simple messages!",
        "who are you": "I'm a simple Python chatbot.",
        "help": "Sure! Tell me what you need help with.",
        "what's up": "Just chatting here!",
        "how old are you": "I don't have an age, I'm just code!",
        "what is python": "Python is a programming language.",
        "tell me a joke": "Why do programmers hate nature? Too many bugs!",
        "open google": "I can't open Google, but you can!",
        "what is your favorite color": "I like all colors equally.",
        "i am sad": "I'm sorry to hear that. I hope things get better soon.",
        "i am happy": "That's great! Keep smiling!",
        "where do you live": "I live inside your Python file.",
        "who is muhammad": "A legend!",
        "good morning": "Good morning! Have a great day!",
        "good night": "Good night! Sleep well!",
        "how is the weather": "I can't check weather, but I hope it’s nice!",
        "are you real": "I’m real inside the computer.",
        "do you like me": "Of course! You're awesome!",
        "what are you doing": "Just waiting for your message!",
        "ok": "Alright!",
        "yes": "Great!",
        "no": "Okay, no problem!"
    }

    # Chat loop
    while True:
        user_input = input("You: ").lower()

        if user_input in responses:
            print("Bot:", responses[user_input])
            if user_input == "bye":
                break
        else:
            print("Bot: Sorry, I don't understand that.")


chatbot()