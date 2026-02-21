import pygame
import sys

# Constants
WIDTH, HEIGHT = 640, 640
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
BEIGE = (245, 222, 179)
GREY = (128, 128, 128)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

class Piece:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, col, color):
        self.row = row       
        self.col = col
        self.color = color
        self.king = False

    def make_king(self):
        self.king = True

    def draw(self, win, highlight=False):
        radius = SQUARE_SIZE//2 - self.PADDING
        x = self.col * SQUARE_SIZE + SQUARE_SIZE//2
        y = self.row * SQUARE_SIZE + SQUARE_SIZE//2
        if highlight:
            pygame.draw.circle(win, BLUE, (x, y), radius + self.OUTLINE + 4, 4)
        pygame.draw.circle(win, GREY, (x, y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (x, y), radius)
        if self.king:
            pygame.draw.circle(win, RED, (x, y), radius//2, 2)

    def move(self, row, col):
        self.row = row
        self.col = col

class Board:
    def __init__(self):
        self.board = []
        self.selected_piece = None
        self.create_board()

    def draw_squares(self, win):
        win.fill(BEIGE)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, BROWN, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if row < 3 and (row + col) % 2 == 1:
                    self.board[row].append(Piece(row, col, WHITE))
                elif row > 4 and (row + col) % 2 == 1:
                    self.board[row].append(Piece(row, col, BLACK))
                else:
                    self.board[row].append(0)

    def draw(self, win, selected=None):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    if selected is not None and piece == selected:
                        piece.draw(win, highlight=True)
                    else:
                        piece.draw(win)

    def get_piece(self, row, col):
        return self.board[row][col]

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = 0, piece
        piece.move(row, col)
        if (piece.color == WHITE and row == ROWS - 1) or (piece.color == BLACK and row == 0):
            piece.make_king()

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))
        if piece.color == BLACK or piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                if last:
                    break
            elif current.color == color:
                break
            else:
                last = [current]
            left -= 1
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last
                if last:
                    break
            elif current.color == color:
                break
            else:
                last = [current]
            right += 1
        return moves

    def count_pieces(self):
        white, black = 0, 0
        for row in self.board:
            for piece in row:
                if piece != 0:
                    if piece.color == WHITE:
                        white += 1
                    else:
                        black += 1
        return white, black

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def draw_winner(win, text):
    font = pygame.font.SysFont('arial', 60, True)
    text_surface = font.render(text, True, RED)
    rect = text_surface.get_rect(center=(WIDTH//2, HEIGHT//2))
    win.blit(text_surface, rect)
    pygame.display.update()
    pygame.time.delay(3000)

def main():
    run = True
    clock = pygame.time.Clock()
    board = Board()
    turn = WHITE
    selected = None
    valid_moves = {}
    winner = None
    must_continue = False  # For multiple jumps

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN and winner is None:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                piece = board.get_piece(row, col)
                if selected:
                    if (row, col) in valid_moves:
                        board.move(selected, row, col)
                        skipped = valid_moves[(row, col)]
                        if skipped:
                            board.remove(skipped)
                        # Check for multiple jumps
                        if skipped:
                            selected = board.get_piece(row, col)
                            new_moves = board.get_valid_moves(selected)
                            # Only allow further jumps if there are moves with skipped pieces
                            jump_moves = {move: skips for move, skips in new_moves.items() if skips}
                            if jump_moves:
                                valid_moves = jump_moves
                                must_continue = True
                                continue
                        selected = None
                        valid_moves = {}
                        turn = BLACK if turn == WHITE else WHITE
                        must_continue = False
                    else:
                        if not must_continue:
                            selected = None
                            valid_moves = {}
                if piece != 0 and piece.color == turn and not must_continue:
                    selected = piece
                    valid_moves = board.get_valid_moves(piece)

        board.draw(WIN, selected)
        if selected:
            for move in valid_moves:
                row, col = move
                pygame.draw.circle(WIN, RED, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

        white_count, black_count = board.count_pieces()
        if winner is None:
            if white_count == 0:
                winner = 'Black won'
            elif black_count == 0:
                winner = 'White won'
            if winner:
                draw_winner(WIN, winner)

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()