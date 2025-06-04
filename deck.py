import random

class Deck:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_cards(self, count):
        if len(self.cards) >= count:
            drawn_cards = random.sample(self.cards, count)

            multiple_cards = []
            for card in drawn_cards:
                orientation = random.choice([0, 1])
                multiple_cards.append((card, orientation))
                
            return multiple_cards
        return None

    def __repr__(self):
        return f"Deck with {len(self.cards)} cards"

    def __getitem__(self, i):
        return self.cards[i]