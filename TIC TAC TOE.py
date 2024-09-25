import tkinter as tk
from tkinter import messagebox, ttk
import random
import pygame

class TicTacToeGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe Multijugador")
        self.master.geometry("450x700")
        self.master.configure(bg="#1A1A2E")

        # Inicializar pygame para el manejo de audio
        pygame.mixer.init()

        self.buttons = []
        self.state = [' '] * 9
        self.game_over = False
        self.current_player = 'X'
        self.game_mode = tk.StringVar(value="Jugador vs IA")
        self.difficulty = tk.StringVar(value="Medio")
        
        # Paleta de colores vibrantes para X y O
        self.x_colors = ["#FF6B6B", "#FF8E72", "#FF5E78", "#FF9671", "#FFA45B", "#FFCC80"]
        self.o_colors = ["#4ECDC4", "#45B7D1", "#33658A", "#5AB9EA", "#5680E9", "#84CEEB"]
        
        # Cargar sonidos
        self.click_sound = pygame.mixer.Sound("recursos/clic.wav")
        self.win_sound = pygame.mixer.Sound("recursos/aplausos.mp3")
        self.lose_sound = pygame.mixer.Sound("recursos/perder.mp3")
        self.draw_sound = pygame.mixer.Sound("recursos/perder1.mp3")

        # Cargar y reproducir música de fondo
        pygame.mixer.music.load("recursos/fondo1.1.wav")
        pygame.mixer.music.play(-1)  # El -1 hace que la música se repita indefinidamente

        self.create_title()
        self.create_game_mode_selector()
        self.create_difficulty_selector()
        self.create_board()
        self.create_reset_button()
        self.create_status_label()
        self.create_music_controls()

        self.start_new_game()

    def create_title(self):
        title_frame = tk.Frame(self.master, bg="#1A1A2E")
        title_frame.pack(pady=20)

        title_chars = list("TIC TAC TOE")
        self.title_labels = []
        
        for char in title_chars:
            label = tk.Label(title_frame, text=char, font=("Helvetica", 28, "bold"), bg="#1A1A2E")
            label.pack(side=tk.LEFT, padx=2)
            self.title_labels.append(label)
        
        self.animate_title()

    def animate_title(self):
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#F9ED69", "#F08A5D"]
        for i, label in enumerate(self.title_labels):
            color = random.choice(colors)
            self.master.after(i * 100, lambda l=label, c=color: l.config(fg=c))
        self.master.after(1500, self.animate_title)

    def create_game_mode_selector(self):
        mode_frame = tk.Frame(self.master, bg="#1A1A2E")
        mode_frame.pack(pady=10)

        tk.Label(mode_frame, text="Modo de juego:", font=("Helvetica", 14), bg="#1A1A2E", fg="white").pack(side=tk.LEFT, padx=5)
        mode_combo = ttk.Combobox(mode_frame, textvariable=self.game_mode, values=["Jugador vs IA", "Jugador vs Jugador"], state="readonly", font=("Helvetica", 12))
        mode_combo.pack(side=tk.LEFT)
        mode_combo.bind("<<ComboboxSelected>>", lambda _: self.reset_game())

    def create_difficulty_selector(self):
        diff_frame = tk.Frame(self.master, bg="#1A1A2E")
        diff_frame.pack(pady=10)

        tk.Label(diff_frame, text="Dificultad IA:", font=("Helvetica", 14), bg="#1A1A2E", fg="white").pack(side=tk.LEFT, padx=5)
        diff_combo = ttk.Combobox(diff_frame, textvariable=self.difficulty, values=["Fácil", "Medio", "Difícil"], state="readonly", font=("Helvetica", 12))
        diff_combo.pack(side=tk.LEFT)
        diff_combo.bind("<<ComboboxSelected>>", lambda _: self.reset_game())

    def create_board(self):
        self.board_frame = tk.Frame(self.master, bg="#1A1A2E")
        self.board_frame.pack(pady=20)

        for i in range(3):
            for j in range(3):
                button = tk.Button(self.board_frame, text="", font=("Helvetica", 40, "bold"), width=3, height=1,
                                   command=lambda row=i, col=j: self.on_click(row, col),
                                   bg="#16213E", fg="white", activebackground="#0F3460")
                button.grid(row=i, column=j, padx=5, pady=5)
                self.buttons.append(button)

    def create_reset_button(self):
        self.reset_button = tk.Button(self.master, text="Nuevo Juego", font=("Helvetica", 14, "bold"),
                                      command=self.reset_game, bg="#E94560", fg="white",
                                      activebackground="#B83B5E")
        self.reset_button.pack(pady=20)

    def create_status_label(self):
        self.status_label = tk.Label(self.master, text="", font=("Helvetica", 14), bg="#1A1A2E", fg="#4ECDC4")
        self.status_label.pack(pady=10)

    def create_music_controls(self):
        music_frame = tk.Frame(self.master, bg="#1A1A2E")
        music_frame.pack(pady=10)

        self.music_var = tk.BooleanVar(value=True)
        self.music_checkbox = tk.Checkbutton(music_frame, text="Música", variable=self.music_var,
                                             command=self.toggle_music, bg="#1A1A2E", fg="white",
                                             selectcolor="#1A1A2E", activebackground="#1A1A2E")
        self.music_checkbox.pack(side=tk.LEFT, padx=10)

        self.volume_scale = tk.Scale(music_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                                     command=self.set_volume, bg="#1A1A2E", fg="white",
                                     troughcolor="#0F3460", activebackground="#E94560")
        self.volume_scale.set(50)  # Volumen inicial al 50%
        self.volume_scale.pack(side=tk.LEFT, padx=10)

    def toggle_music(self):
        if self.music_var.get():
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()

    def set_volume(self, val):
        volume = float(val) / 100
        pygame.mixer.music.set_volume(volume)

    def start_new_game(self):
        self.state = [' '] * 9
        self.game_over = False
        self.current_player = 'X'
        for button in self.buttons:
            button.config(text="", state="normal", bg="#16213E")
        
        if self.game_mode.get() == "Jugador vs IA":
            self.start_player = random.choice(['user', 'machine'])
            if self.start_player == 'machine':
                self.status_label.config(text="La IA comienza primero.")
                self.master.after(1000, self.machine_move)
            else:
                self.status_label.config(text="Tú comienzas. Haz clic en una casilla.")
        else:
            self.status_label.config(text="Jugador X comienza. Haz clic en una casilla.")

    def on_click(self, row, col):
        index = 3 * row + col
        if self.state[index] == ' ' and not self.game_over:
            self.click_sound.play()
            self.animate_move(index, self.current_player)
            if self.check_winner():
                return
            
            if self.game_mode.get() == "Jugador vs IA" and self.current_player == 'X':
                self.master.after(500, self.machine_move)
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                self.status_label.config(text=f"Turno del Jugador {self.current_player}")

    def animate_move(self, index, player):
        self.state[index] = player
        button = self.buttons[index]
        
        colors = random.sample(self.x_colors if player == 'X' else self.o_colors, 3)
        
        def change_color(color_index=0):
            if color_index < len(colors):
                button.config(text=player, fg=colors[color_index], state="disabled")
                self.master.after(100, lambda: change_color(color_index + 1))
            else:
                button.config(fg=colors[-1])

        change_color()

    def machine_move(self):
        if ' ' in self.state and not self.game_over:
            if self.difficulty.get() == "Fácil":
                move = self.get_easy_move()
            elif self.difficulty.get() == "Medio":
                move = self.get_medium_move()
            else:
                move = self.get_best_move(self.state)
            
            self.click_sound.play()
            self.animate_move(move, 'O')
            if not self.check_winner():
                self.current_player = 'X'
                self.status_label.config(text="Tu turno. Haz clic en una casilla.")

    def get_easy_move(self):
        return random.choice([i for i, v in enumerate(self.state) if v == ' '])

    def get_medium_move(self):
        if random.random() < 0.7:
            return self.get_best_move(self.state)
        else:
            return self.get_easy_move()

    def check_winner(self):
        winner = self.get_winner(self.state)
        if winner:
            self.highlight_winning_line()
            self.master.after(1000, lambda: self.show_winner_message(winner))
            return True
        elif ' ' not in self.state:
            self.master.after(500, lambda: self.show_draw_message())
            self.game_over = True
            return True
        return False

    def highlight_winning_line(self):
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        for a, b, c in winning_combinations:
            if self.state[a] == self.state[b] == self.state[c] != ' ':
                highlight_color = "#F9ED69"  # Color amarillo brillante para la línea ganadora
                for index in (a, b, c):
                    self.buttons[index].config(bg=highlight_color)
                break

    def show_winner_message(self, winner):
        if self.game_mode.get() == "Jugador vs IA":
            if winner == 'X':
                self.win_sound.play()
                messagebox.showinfo("Fin del Juego", "¡Has ganado!")
            else:
                self.lose_sound.play()
                messagebox.showinfo("Fin del Juego", "La IA ha ganado.")
        else:
            self.win_sound.play()
            messagebox.showinfo("Fin del Juego", f"¡El Jugador {winner} ha ganado!")
        self.game_over = True

    def show_draw_message(self):
        self.draw_sound.play()
        messagebox.showinfo("Fin del Juego", "¡Empate!")
        self.game_over = True

    def reset_game(self):
        self.start_new_game()

    @staticmethod
    def get_winner(state):
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        for a, b, c in winning_combinations:
            if state[a] == state[b] == state[c] and state[a] != ' ':
                return state[a]
        return None

    def minimax(self, state, depth, is_maximizing):
        winner = self.get_winner(state)
        if winner == 'X':
            return -1
        elif winner == 'O':
            return 1
        elif ' ' not in state:
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for i in range(9):
                if state[i] == ' ':
                    state[i] = 'O'
                    score = self.minimax(state, depth + 1, False)
                    state[i] = ' '
                    best_score = max(best_score, score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if state[i] == ' ':
                    state[i] = 'X'
                    score = self.minimax(state, depth + 1, True)
                    state[i] = ' '
                    best_score = min(best_score, score)
            return best_score

    def get_best_move(self, state):
        best_score = float('-inf')
        best_move = None
        for i in range(9):
            if state[i] == ' ':
                state[i] = 'O'
                score = self.minimax(state, 0, False)
                state[i] = ' '
                if score > best_score:
                    best_score = score
                    best_move = i
        return best_move

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeGUI(root)
    root.mainloop()