import tkinter as tk

# Cores
BG_YELLOW = "#fff176"      # fundo da janela (amarelo claro)
DARK_YELLOW = "#b58900"    # amarelo escuro = bit 1
BLACK = "#000000"          # preto = bit 0
BORDER = "#ffffff"         # cor do rebordo

# Dimensões
WINDOW_W = 800
WINDOW_H = 600
RECT_W = 180
RECT_H = 100
NUM_RECTS = 8


class BinaryRect:
    def __init__(self, canvas, x1, y1, x2, y2, bit=1):
        """
        canvas: tkinter Canvas
        coords: x1,y1,x2,y2 (esquerda, topo, direita, fundo)
        bit: 1 (amarelo escuro) ou 0 (preto)
        """
        self.canvas = canvas
        self.coords = (x1, y1, x2, y2)
        self.bit = 1 if bit else 0
        self.item_id = None
        self.draw()

    def draw(self):
        x1, y1, x2, y2 = self.coords
        fill = DARK_YELLOW if self.bit == 1 else BLACK
        if self.item_id is None:
            self.item_id = self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=fill,
                outline=BORDER,
                width=1
            )
        else:
            self.canvas.coords(self.item_id, x1, y1, x2, y2)
            self.canvas.itemconfig(self.item_id, fill=fill)

    def toggle(self):
        self.bit = 0 if self.bit == 1 else 1
        self.draw()

    def contains_point(self, x, y):
        x1, y1, x2, y2 = self.coords
        return x1 <= x <= x2 and y1 <= y <= y2


def create_stacked_rects(canvas, n, base_w, base_h):
    """
    Cria n rectângulos empilhados de baixo para cima e direita para esquerda.
    Cada rect sobrepõe 2/3 do anterior.
    """
    shift_x = base_w / 3
    shift_y = base_h / 3

    margin = 40
    start_right = WINDOW_W - margin
    start_bottom = WINDOW_H - margin

    rects = []

    # desenhar de baixo para cima (rect 0 no fundo, rect n-1 no topo)
    for i in range(n):
        x2 = start_right - (i * shift_x)
        y2 = start_bottom - (i * shift_y)
        x1 = x2 - base_w
        y1 = y2 - base_h
        rect = BinaryRect(canvas, x1, y1, x2, y2, bit=1)
        rects.append(rect)
    return rects


class App:
    def __init__(self, root):
        self.root = root
        root.title("fotonic lab")
        root.resizable(False, False)

        self.canvas = tk.Canvas(
            root,
            width=WINDOW_W,
            height=WINDOW_H,
            bd=0,
            highlightthickness=0,
            bg=BG_YELLOW
        )
        self.canvas.pack()

        # criar rectângulos
        self.rects = create_stacked_rects(self.canvas, NUM_RECTS, RECT_W, RECT_H)

        # clicar verifica do topo para baixo
        self.canvas.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        x, y = event.x, event.y
        for rect in reversed(self.rects):  # topo -> fundo
            if rect.contains_point(x, y):
                rect.toggle()
                break


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry(f"{WINDOW_W}x{WINDOW_H}")
    app = App(root)
    root.mainloop()
