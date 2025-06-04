import os
from PIL import Image

class Card:
    def __init__(self, name, number, arcana, img, fortune_telling, keywords, meanings_light, meanings_shadow):
        self.name = name
        self.number = number
        self.arcana = arcana
        self.img = img
        self.fortune_telling = fortune_telling
        self.keywords = keywords
        self.meanings_light = meanings_light
        self.meanings_shadow = meanings_shadow

    @classmethod
    def create_card(cls, row, base_img_path):
        img_path = os.path.join(base_img_path, 'cards', row['img'])
        
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"Image not found: {img_path}")
    
        card = cls(
            name=row['name'],
            number=row['number'],
            arcana=row['arcana'],
            img=Image.open(img_path),  
            fortune_telling=row['fortune_telling'],
            keywords=row['keywords'],
            meanings_light=row['meanings.light'],
            meanings_shadow=row['meanings.shadow']
        )
        return card

    def __repr__(self):
        return f"Card(name={self.name}, number={self.number}, arcana={self.arcana})"