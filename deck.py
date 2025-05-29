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

    @staticmethod
    def get_markdowns_card_infos(mcards):
        card_markdown_template = "## {name}\n### Fortune Telling\n{fortune_telling}\n### Keywords\n{keywords}\n### Meaning\n{meanings}"
    
        markdown_list = []
        cards_name = []
        for card, orientation in mcards:
            name = card.name
            name += "" if orientation else " (Reversed)"
            fortune_telling = '\n'.join(card.fortune_telling)
            keywords = '\n'.join(card.keywords)
            meanings = '\n'.join(card.meanings_light) if orientation else '\n'.join(card.meanings_shadow)
            
            # Generate the markdown for the current card using the template
            card_markdown = card_markdown_template.format(
                name=name ,
                fortune_telling=fortune_telling,
                keywords=keywords,
                meanings=meanings
            )
            
            markdown_list.append(card_markdown.strip())
            cards_name.append(name)
            
        return "\n\n".join(markdown_list), cards_name

    def __repr__(self):
        return f"Deck with {len(self.cards)} cards"

    def __getitem__(self, i):
        return self.cards[i]