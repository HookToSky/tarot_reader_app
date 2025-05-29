import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk 
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
import pandas as pd
import os

from card import Card
from deck import Deck


def load_tarot_data(base_path="./data", json_file='tarot-images.json'):
    json_path = os.path.join(base_path, json_file)

    data = pd.read_json(json_path)
    normalized_data = pd.json_normalize(data['cards'])
    normalized_data = normalized_data[['name', 'number', 'arcana', 'img', 'fortune_telling',
                                    'keywords', 'meanings.light','meanings.shadow']].copy()
    
    return normalized_data

tarot_images_path = './data/'
normalized_data = load_tarot_data(tarot_images_path)
# Draw each card on the canvas
card_width = 100
card_height = 150
spacing = 20
start_x = 50

class TarotApp:
    def __init__(self, root):
        self.root = root
        self.llm = ChatOllama(model="mistral")
        self.root.title("Tarot Reader")
        self.root.geometry("900x600")
        self.template = "What are the key ideas of {topic}?"
        self.prompt = PromptTemplate(template=self.template, input_variables=["topic"])
        self.llm_chain = self.prompt | self.llm
        self.cards = normalized_data
        self.deck = Deck()
        self.load_cards_into_deck()
        self.card_images = []

        title = ttk.Label(root, text="Three-Card Tarot Reading", font=("Helvetica", 18))
        title.pack(pady=10)

        prompt_frame = ttk.Frame(root)
        prompt_frame.pack(pady=10)
        ttk.Label(prompt_frame, text="Ask your question:").pack(side="left")
        self.prompt_entry = ttk.Entry(prompt_frame, width=50)
        self.prompt_entry.pack(side="left", padx=10)

        submit_button = ttk.Button(prompt_frame, text="Submit", command=self.handle_prompt)
        submit_button.pack()


        self.canvas = tk.Canvas(self.root, width=800, height=400, bg="white")
        self.canvas.pack(pady=20)

        # Add a frame for user interaction
        self.prompt_frame = tk.Frame(self.root)
        self.prompt_frame.pack(pady=10)

        # Add buttons for interaction
        self.shuffle_button = ttk.Button(self.prompt_frame, text="Shuffle Deck", command=self.shuffle_deck)
        self.shuffle_button.grid(row=0, column=0, padx=10)

        self.draw_button = ttk.Button(self.prompt_frame, text="Draw Card", command=self.draw_one_card)
        self.draw_button.grid(row=0, column=1, padx=10)

        # Track drawn cards
        self.drawn_cards = []
        self.max_cards = 3  # Limit the number of cards to draw

    def load_cards_into_deck(self):
        """Load cards from the normalized data into the Deck."""
        for _, row in self.cards.iterrows():
            card = Card(
                name=row['name'],
                number=row['number'],
                arcana=row['arcana'],
                img=row['img'],
                fortune_telling=row['fortune_telling'],
                keywords=row['keywords'],
                meanings_light=row['meanings.light'],
                meanings_shadow=row['meanings.shadow']
            )
            self.deck.add_card(card)

    def shuffle_deck(self):
        """Shuffle the deck."""
        self.deck.shuffle()
        self.canvas.delete("all")  # Clear the canvas
        self.canvas.create_text(400, 200, text="Deck shuffled!", font=("Arial", 16), fill="green")
        self.drawn_cards = []  # Reset drawn cards

    def draw_one_card(self):
        """Draw one card from the deck and display it on the canvas."""
        if len(self.drawn_cards) < self.max_cards:
            card = self.deck.draw_cards(1)  # Draw one card
            if card:
                self.drawn_cards.append(card[0])  # Add the card to the drawn list
                self.display_card(card[0], len(self.drawn_cards) - 1)
        else:
            self.canvas.create_text(400, 350, text="Maximum cards drawn!", font=("Arial", 12), fill="red")

    def display_card(self, card_tuple, position):
        """Display a single card on the canvas."""
        card, orientation = card_tuple
        card_width = 100
        card_height = 150
        spacing = 20
        start_x = 50

        x1 = start_x + position * (card_width + spacing)
        y1 = 100

        # Load the card image
        try:
            img_path = card.img  # Path to the card image
            img = Image.open(img_path)
            img = img.resize((card_width, card_height), Image.ANTIALIAS)  # Resize the image
            tk_img = ImageTk.PhotoImage(img)

            # Store the image reference to prevent garbage collection
            self.card_images.append(tk_img)

            # Display the image on the canvas
            self.canvas.create_image(x1, y1, anchor=tk.NW, image=tk_img)

        except Exception as e:
            # If the image fails to load, display a placeholder rectangle
            self.canvas.create_rectangle(x1, y1, x1 + card_width, y1 + card_height, fill="lightblue", outline="black")
            self.canvas.create_text(x1 + card_width // 2, y1 + 20, text="Image\nNot Found", font=("Arial", 10), fill="black")

        # Add card name and orientation below the image
        card_name = card.name + (" (Reversed)" if orientation == 0 else "")
        self.canvas.create_text(x1 + card_width // 2, y1 + card_height + 10, text=card_name, font=("Arial", 10), fill="black")


    def handle_prompt(self):
        question = self.prompt_entry.get()
        chosen_cards = self.drawn_cards()

        response = f"You asked: \"{question}\"\n\n"
        answer = self.llm_chain.invoke({"input": question, "cards": chosen_cards})
        response += answer["output"]

if __name__ == "__main__":
    root = tk.Tk()
    app = TarotApp(root)
    root.mainloop()