import random
import tkinter as tk
from tkinter import messagebox
import time


class MazeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Maze Game: You're Your Own Enemy!")
        self.canvas = tk.Canvas(master, width=800, height=520, bg="white")
        self.canvas.pack()

        self.cell_size = 40
        self.rows = 13
        self.cols = 20

        self.maze = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 2],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

        self.player_pos = [1, 1]
        self.shadow_pos = [6, 1]  
        self.move_count = 0
        self.timer_start = None

        self.draw_maze()

        self.master.bind("<Up>", lambda event: self.move_player(0, -1))
        self.master.bind("<Down>", lambda event: self.move_player(0, 1))
        self.master.bind("<Left>", lambda event: self.move_player(-1, 0))
        self.master.bind("<Right>", lambda event: self.move_player(1, 0))

        self.check_initial_position()

    def draw_maze(self):
        self.canvas.delete("all")
        for row in range(self.rows):
            for col in range(self.cols):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                if self.maze[row][col] == 1:  # Wall
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="black")
                elif self.maze[row][col] == 2:  # Victory
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="green")

        px, py = self.player_pos
        self.canvas.create_oval(
            px * self.cell_size + 5,
            py * self.cell_size + 5,
            px * self.cell_size + self.cell_size - 5,
            py * self.cell_size + self.cell_size - 5,
            fill="blue",
        )

        sx, sy = self.shadow_pos
        self.canvas.create_oval(
            sx * self.cell_size + 5,
            sy * self.cell_size + 5,
            sx * self.cell_size + self.cell_size - 5,
            sy * self.cell_size + self.cell_size - 5,
            fill="light blue",
        )

    def move_player(self, dx, dy):
        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy

        if self.maze[new_y][new_x] != 1:
            self.player_pos = [new_x, new_y]
            self.move_count += 1

            self.timer_start = None

            if self.maze[new_y][new_x] == 2:
                self.win_game("You win!")
                return

            numbers = [0,1,2,3]
            if self.shadow_pos:
                if self.shadow_pos[0] < self.player_pos[0]:
                    self.shadow_pos[0] += random.choice(numbers)
                elif self.shadow_pos[0] > self.player_pos[0]:
                    self.shadow_pos[0] -= random.choice(numbers)

                if self.shadow_pos[1] < self.player_pos[1]:
                    self.shadow_pos[1] += random.choice(numbers)
                elif self.shadow_pos[1] > self.player_pos[1]:
                    self.shadow_pos[1] -= random.choice(numbers)

            if self.shadow_pos == self.player_pos:
                self.lose_game("You lost, You're your own enemy!")
                return

            self.draw_maze()

    def check_initial_position(self):
        """Check if the player is staying in the initial position."""
        if self.player_pos == [1, 1]:
            if self.timer_start is None:
                self.timer_start = time.time()
            elif time.time() - self.timer_start >= 10:
                self.win_game("You win, can't hurt yourself if you do nothing!")
                return

        self.master.after(1000, self.check_initial_position)

    def win_game(self, message):
        """Handle winning the game."""
        messagebox.showinfo("Victory!", message)
        self.master.quit()

    def lose_game(self, message):
        """Handle losing the game."""
        messagebox.showerror("Game Over!", message)
        self.master.quit()

root = tk.Tk()
game = MazeGame(root)
root.mainloop()

# I hate my life