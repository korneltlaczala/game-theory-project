import customtkinter as ctk

from solver import SubtractionGame

class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Subtraction and All-But Games")
        self.geometry("1200x800")
        self.resizable(False, False)
        self.game = SubtractionGame()

        self.generate_widgets()

    def run(self):
        self.mainloop()

    def generate_widgets(self):
        self.generate_move_buttons()

    def generate_move_buttons(self):
        self.bottom_frame = ctk.CTkFrame(self)
        self.bottom_frame.pack(side="bottom", fill="x")
        rows = 2
        cols = 20

        label = ctk.CTkLabel(self.bottom_frame, text="Valid moves:", font=("Helvetica", 20, "bold"))
        label.grid(row=0, column=0, columnspan=cols, sticky="w", padx=5, pady=5)

        for i in range(1,rows*cols+1):
            button = MoveButton(master=self.bottom_frame, text=str(i), move=i, game=self.game, height=50)
            button.grid(row=(i-1)//cols+1, column=(i-1)%cols, sticky="ew", padx=5, pady=5)
            self.bottom_frame.columnconfigure((i-1)%cols, weight=1)
            button.configure(command=button.switch_state)

class MoveButton(ctk.CTkButton):

    def __init__(self, master, text, move, game,  **kwargs):
        super().__init__(master, text=text, **kwargs)
        self.state = 0
        self.move = move
        self.game = game

    def switch_state(self):
        if self.state == 0:
            self.configure(fg_color="#3B8ED0", border_color="white", border_width=2)
            self.state = 1
            self.game.add_move(self.move)
            print("siema")
            self.game.update()
        else:
            self.configure(fg_color="#1F6AA5", border_color="white", border_width=0)
            self.state = 0
            self.game.remove_move(self.move)
            self.game.update()

if __name__ == "__main__":
    app = App()
    app.run()