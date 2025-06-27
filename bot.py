from util import prepare_data
from random import choice
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

class ChatBot:
    def __init__(self, file_path):
        self.patterns, self.tags, self.responses = prepare_data(file_path)
        self.vectorizer = TfidfVectorizer()
        self.classifier = LogisticRegression(random_state=0, max_iter=10000)

        self.X = self.vectorizer.fit_transform(self.patterns)
        self.Y = self.tags

        self.classifier.fit(self.X, self.Y)


    def get_response(self, input_text):
        processed_input = self.vectorizer.transform([input_text])
        predicted_tag = self.classifier.predict(processed_input)[0]
        response = self.responses.get(predicted_tag, ["Sorry, I don't understand that."])

        return choice(response)


if __name__ == "__main__":
    file_path = 'intents.json'
    bot = ChatBot(file_path)
    
    user_input = "Hello! How are you?"
    print(bot.get_response(user_input))