from util import prepare_data
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from random import choice


class Bot:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.classifier = SVC(kernel='linear', probability=True)

    def load_data(self, file_path):
        self.patterns, self.tags, self.responses = prepare_data(file_path)

    def train(self):
        X = self.vectorizer.fit_transform(self.patterns)
        y = self.tags
        self.classifier.fit(X, y)

    def get_response(self, user_input):
        user_input_vectorized = self.vectorizer.transform([user_input])
        predicted_tag = self.classifier.predict(user_input_vectorized)[0]
        
        return choice(self.responses.get(predicted_tag, ["Sorry, I don't understand that."]))


if __name__ == "__main__":
    bot = Bot()
    bot.load_data('training_data.json')
    bot.train()

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        response = bot.get_response(user_input)
        print(f"Bot: {response}")
       