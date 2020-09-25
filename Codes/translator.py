from googletrans import Translator


class Translate:
    def __init__(self):
        self.translator = Translator()

    def translateToPersian(self, engWord):
        return self.translator.translate(engWord, dest='fa').text

    def translateToEng(self, perWord):
        return self.translator.translate(perWord, dest='en').text
