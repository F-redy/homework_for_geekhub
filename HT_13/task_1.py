# 1. Напишіть програму, де клас «геометричні фігури» (Figure) містить властивість color
# з початковим значенням white і метод для зміни кольору фігури,
# а його підкласи «овал» (Oval) і «квадрат» (Square) містять методи __init__ для завдання початкових розмірів
# об'єктів при їх створенні.

class Figure:
    def __init__(self):
        self.color = 'white'

    def change_color(self, new_color):
        if new_color and isinstance(new_color, str):
            self.color = new_color


class Oval(Figure):
    def __init__(self, horizontal_radius, vertical_radius):
        super().__init__()
        self.horizontal_radius = horizontal_radius
        self.vertical_radius = vertical_radius


class Square(Figure):
    def __init__(self, side_length):
        super().__init__()
        self.side_length = side_length


if __name__ == "__main__":
    oval = Oval(5, 10)
    print(f"Oval color: {oval.color}")
    oval.change_color('blue')
    print(f"Oval color after change: {oval.color}\n")

    square = Square(7)
    print(f"Square color: {square.color}")
    square.change_color('red')
    print(f"Square color after change: {square.color}")
