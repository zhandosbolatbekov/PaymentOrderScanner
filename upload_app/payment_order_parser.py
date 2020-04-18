import re
from json import JSONEncoder


class ScannedWordData:
    def __init__(self, text, min_x, min_y, max_x, max_y):
        self.text = text
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y

    def __str__(self):
        return (self.text + ': (' + str(self.min_x) + ', ' + str(self.min_y) + ') -> (' + str(self.max_x) + ', ' + str(
            self.max_y) + ')')


class PaymentOrderParser:
    class ParsedData:
        recipient_iin = None
        recipient_iban = None
        beneficiary_code = None
        knp = None
        product_names = None
        total_amount = None

    class ParsedDataEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__

    def parse(self, words: [ScannedWordData]) -> ParsedData:
        parsed = self.ParsedData()
        parsed.recipient_iin = self.parse_iin(words)
        parsed.recipient_iban = self.parse_iban(words)
        parsed.beneficiary_code = self.parse_kbe(words)
        return parsed

    def parse_iin(self, words):
        for word in words:
            if len(word.text) == 12 and word.text.isdecimal():
                return word.text
        return None

    def parse_iban(self, words):
        for word in words:
            if len(word.text) == 20 and re.search('^KZ[A-Z0-9]{18}$', word.text).group(0) is not None:
                return word.text
        return None

    def parse_kbe(self, words):
        title_word = None
        for word in words:
            if title_word is not None:
                if len(word.text) == 2 and word.text.isdecimal() and self.have_intersection_on_x(word, title_word):
                    return word.text
            elif word.text.lower() == 'кбе':
                title_word = word
        return None

    @staticmethod
    def have_intersection_on_x(lhs: ScannedWordData, rhs: ScannedWordData) -> bool:
        return min(lhs.max_x, rhs.max_x) - max(lhs.min_x, rhs.min_x) > 0

    @staticmethod
    def have_intersection_on_y(self, lhs: ScannedWordData, rhs: ScannedWordData) -> bool:
        return min(lhs.max_y, rhs.max_y) - max(lhs.min_y, rhs.min_y) > 0
