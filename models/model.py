# anything in this model will be displayed in the attribute frame

class State:
    def __init__(self):
        pass


class Card:
    def __init__(self):
        self.type = None

    def choice(self):
        # types of card: birthday, thank you, Christmas,
        #                valentine, blank (add your own text)
        pass


class Overlay:
    def __init__(self, img_path, x=0, y=0, scale=1.0):
        self.img_path = img_path
        self.x = x
        self.y = y
        self.scale = scale


class Eyes(Overlay):
    pass


class Nose(Overlay):
    pass


class Lips(Overlay):
    pass


class Accessory(Overlay):
    pass
