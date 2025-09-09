import random
import tkinter as tk
from tkinter import messagebox

# The main game logic class for Minesweeper.
# It manages the game board, mine placement, and game state.
class Minesweeper:
    def __init__(self, rows, cols, num_mines):
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.visible_board = [[' ' for _ in range(cols)] for _ in range(rows)]
        self.game_over = False
        self.win = False
        self._place_mines()
        self._calculate_numbers()

    def _place_mines(self):
        """Randomly places a specified number of mines on the board."""
        mines_placed = 0
        while mines_placed < self.num_mines:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            if self.board[r][c] != 'M':
                self.board[r][c] = 'M'
                mines_placed += 1

    def _get_neighbors(self, r, c):
        """Returns a list of valid neighboring coordinates for a given cell."""
        neighbors = []
        for i in range(r - 1, r + 2):
            for j in range(c - 1, c + 2):
                if 0 <= i < self.rows and 0 <= j < self.cols and (i, j) != (r, c):
                    neighbors.append((i, j))
        return neighbors

    def _calculate_numbers(self):
        """Calculates and assigns the number of adjacent mines for each non-mine cell."""
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == 'M':
                    continue
                count = 0
                for nr, nc in self._get_neighbors(r, c):
                    if self.board[nr][nc] == 'M':
                        count += 1
                self.board[r][c] = count

    def reveal(self, r, c):
        """Recursively reveals cells, stopping at cells with adjacent mines."""
        if self.game_over or self.visible_board[r][c] != ' ':
            return
        
        if self.board[r][c] == 'M':
            self.game_over = True
            self.visible_board[r][c] = 'M'
            return
        
        self.visible_board[r][c] = str(self.board[r][c])
        
        if self.board[r][c] == 0:
            for nr, nc in self._get_neighbors(r, c):
                if self.visible_board[nr][nc] == ' ':
                    self.reveal(nr, nc)
        
        self.check_win()

    def flag(self, r, c):
        """Toggles a flag on a cell."""
        if self.game_over or self.visible_board[r][c] not in (' ', 'F'):
            return
        
        if self.visible_board[r][c] == ' ':
            self.visible_board[r][c] = 'F'
        elif self.visible_board[r][c] == 'F':
            self.visible_board[r][c] = ' '
            
    def check_win(self):
        """Checks if the player has won the game."""
        hidden_cells = 0
        for r in range(self.rows):
            for c in range(self.cols):
                if self.visible_board[r][c] == ' ':
                    hidden_cells += 1
        
        if hidden_cells == self.num_mines:
            self.win = True
            self.game_over = True

    def __str__(self):
        """A string representation of the board for debugging."""
        return '\n'.join([' '.join(row) for row in self.visible_board])

# ---
# The graphical user interface (GUI) class using tkinter.
# It creates the visual game board and handles user interactions.
class MinesweeperGUI:
    def __init__(self, rows, cols, num_mines):
        self.game = Minesweeper(rows, cols, num_mines)
        self.window = tk.Tk()
        self.window.title("Minesweeper")
        self.buttons = [[None for _ in range(cols)] for _ in range(rows)]
        self._create_widgets()
        self.window.mainloop()

    def _create_widgets(self):
        """Creates the grid of buttons for the game board."""
        for r in range(self.game.rows):
            for c in range(self.game.cols):
                button = tk.Button(
                    self.window,
                    width=4,
                    height=2,
                    command=lambda r=r, c=c: self._on_click_left(r, c)
                )
                button.grid(row=r, column=c)
                button.bind('<Button-3>', lambda event, r=r, c=c: self._on_click_right(event, r, c))
                self.buttons[r][c] = button
    
    def _update_board(self):
        """Updates the visual appearance of the board based on the game state."""
        for r in range(self.game.rows):
            for c in range(self.game.cols):
                cell_value = self.game.visible_board[r][c]
                button = self.buttons[r][c]
                
                if cell_value == ' ':
                    button.config(text='', relief=tk.RAISED, state=tk.NORMAL)
                elif cell_value == 'F':
                    button.config(text='🚩', relief=tk.RAISED, state=tk.NORMAL)
                else:
                    button.config(text=cell_value, relief=tk.SUNKEN, state=tk.DISABLED)
                    if cell_value == '0':
                        button.config(text='')
                    elif cell_value == 'M':
                        button.config(text='💣')
                    else:
                        colors = {
                            '1': 'blue', '2': 'green', '3': 'red', '4': 'purple', 
                            '5': 'maroon', '6': 'turquoise', '7': 'black', '8': 'gray'
                        }
                        button.config(fg=colors.get(cell_value, 'black'))

    def _on_click_left(self, r, c):
        """Handles a left mouse click to reveal a cell."""
        self.game.reveal(r, c)
        self._update_board()
        self._check_game_status()

    def _on_click_right(self, event, r, c):
        """Handles a right mouse click to flag a cell."""
        self.game.flag(r, c)
        self._update_board()
        
    def _check_game_status(self):
        """Displays a message box when the game ends (win or lose)."""
        if self.game.game_over:
            if self.game.win:
                messagebox.showinfo("Minesweeper", "Congratulations, you won! 🎉")
            else:
                # Reveal all mines on game over
                for r in range(self.game.rows):
                    for c in range(self.game.cols):
                        if self.game.board[r][c] == 'M':
                            self.buttons[r][c].config(text='💣', relief=tk.SUNKEN)
                messagebox.showinfo("Minesweeper", "Game Over! You hit a mine. 💥")
            self.window.quit()

if __name__ == "__main__":
    MinesweeperGUI(10, 10, 15)
