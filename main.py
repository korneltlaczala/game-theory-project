import customtkinter as ctk

from solver import SubtractionGame

class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Subtraction and All-But Games")
        self.geometry("1600x800")
        self.resizable(False, False)
        self.game = SubtractionGame()
        self.result_display_length = 45

        self.generate_widgets()

    def run(self):
        self.mainloop()

    def generate_widgets(self):
        self.generate_move_buttons()
        self.generate_result_frame()

    def generate_move_buttons(self):
        self.left_frame = ctk.CTkFrame(self)
        self.left_frame.pack(side="left", fill="y")
        rows = 20
        cols = 2

        label = ctk.CTkLabel(self.left_frame, text="Valid moves:", font=("Helvetica", 14, "bold"))
        label.grid(row=0, column=0, columnspan=cols, sticky="w", padx=5, pady=5)

        for i in range(1, rows * cols + 1):
            button = MoveButton(master=self.left_frame, text=str(i), move=i, game=self.game, width = 50, height = 50)
            button.grid(row=(i-1)//cols + 1, column=(i-1) % cols, sticky="ew", padx=5, pady=5)
            self.left_frame.rowconfigure((i-1)//cols + 1, weight=1)
            self.left_frame.columnconfigure((i-1) % cols, weight=1)
            button.configure(command=button.switch_state)

    def generate_result_frame(self):
        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.pack(side="bottom", fill="both", expand=True)
        self.right_frame.rowconfigure(0, weight=1)

    def generate_result_display(self):
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        colors = ["#e2786f", "#8fbf8f"]  # mild dark red and darker green
        # add period length and first period index labels

        label_frame = ctk.CTkFrame(self.right_frame, fg_color=self.right_frame.cget("fg_color"))
        label_frame.pack(fill="x", padx=10, pady=10, side="bottom")

        index_frame = ctk.CTkFrame(label_frame, fg_color=label_frame.cget("fg_color"))
        index_frame.grid(row=1, column=0, columnspan=self.result_display_length, sticky="ew")

        for i in range(self.result_display_length):
            index_label = ctk.CTkLabel(index_frame, text=str(i), text_color="light gray", width=25, height=25)
            index_label.grid(row=0, column=i, padx=3, sticky="ew")

        values_frame = ctk.CTkFrame(label_frame)
        values_frame.grid(row=2, column=0, columnspan=self.result_display_length, sticky="ew")

        for i, value in enumerate(self.game.result[:self.result_display_length]):
            color_index = 0 if value == 0 else 1
            color = colors[color_index]
            label = ctk.CTkLabel(values_frame, text=str(value), fg_color=color, text_color="black", width=25, height=25)
            label.grid(row=0, column=i, padx=3, sticky="ew")

            # highlight period start in a separate row
            if self.game.is_periodic and i == self.game.first_period_start:
                highlight_label = ctk.CTkLabel(label_frame, text="", fg_color="#FFD700", height=5)  # Gold color for period start
                highlight_label.grid(row=3, column=i, columnspan=self.game.period_length, padx=3, sticky="ew")

class MoveButton(ctk.CTkButton):
    def __init__(self, master, text, move, game, **kwargs):
        super().__init__(master, text=text, **kwargs)
        self.state = 0
        self.move = move
        self.game = game

    def switch_state(self):
        if self.state == 0:
            self.configure(fg_color="#3B8ED0", border_color="white", border_width=2)
            self.state = 1
            self.game.add_move(self.move)
            self.game.update()
        else:
            self.configure(fg_color="#1F6AA5", border_color="white", border_width=0)
            self.state = 0
            self.game.remove_move(self.move)
            self.game.update()

        self.master.master.generate_result_display()

if __name__ == "__main__":
    app = App()
    app.run()