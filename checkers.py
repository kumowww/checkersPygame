import pygame
import pygame.gfxdraw
import sys

WIDTH, HEIGHT = 640, 640
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
BROWN = (139, 69, 19)
BEIGE = (245, 222, 179)
GREY = (100, 100, 100)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def draw_smooth_circle(surface, color, center, radius):
    x, y = center
    pygame.gfxdraw.aacircle(surface, x, y, radius, color)
    pygame.gfxdraw.filled_circle(surface, x, y, radius, color)

def find_captures(state, r, c, color, is_king, current_skipped, current_path, captures):
    found_capture = False
    dirs = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    
    if is_king:
        for dr, dc in dirs:
            step = 1
            hit_pos = None
            while True:
                nr, nc = r + dr*step, c + dc*step
                if not (0 <= nr < 8 and 0 <= nc < 8):
                    break
                
                if state[nr][nc] is not None:
                    if state[nr][nc][0] == color:
                        break
                    if (nr, nc) in current_skipped:
                        break
                    if hit_pos is not None:
                        break
                    hit_pos = (nr, nc)
                else:
                    if hit_pos is not None:
                        found_capture = True
                        new_skipped = current_skipped + [hit_pos]
                        new_path = current_path + [(nr, nc)]
                        
                        temp_orig = state[r][c]
                        state[r][c] = None
                        state[nr][nc] = (color, True)
                        
                        find_captures(state, nr, nc, color, True, new_skipped, new_path, captures)
                        
                        state[r][c] = temp_orig
                        state[nr][nc] = None
                step += 1
    else:
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            nnr, nnc = r + 2*dr, c + 2*dc
            
            if 0 <= nnr < 8 and 0 <= nnc < 8:
                if state[nr][nc] is not None and state[nr][nc][0] != color and (nr, nc) not in current_skipped:
                    if state[nnr][nnc] is None:
                        found_capture = True
                        new_skipped = current_skipped + [(nr, nc)]
                        new_path = current_path + [(nnr, nnc)]
                        
                        promotes = False
                        if color == WHITE and nnr == 7: promotes = True
                        if color == BLACK and nnr == 0: promotes = True
                        new_is_king = is_king or promotes
                        
                        temp_orig = state[r][c]
                        state[r][c] = None
                        state[nnr][nnc] = (color, new_is_king)
                        
                        find_captures(state, nnr, nnc, color, new_is_king, new_skipped, new_path, captures)
                        
                        state[r][c] = temp_orig
                        state[nnr][nnc] = None
                        
    if not found_capture and current_skipped:
        captures.append({'dest': (r, c), 'skipped': current_skipped, 'path': current_path})

def get_piece_moves(state, r, c):
    color, is_king = state[r][c]
    captures = []
    find_captures(state, r, c, color, is_king, [], [], captures)
    
    if captures:
        max_c = max(len(cap['skipped']) for cap in captures)
        return [cap for cap in captures if len(cap['skipped']) == max_c]
        
    moves = []
    if is_king:
        dirs = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in dirs:
            step = 1
            while True:
                nr, nc = r + dr*step, c + dc*step
                if 0 <= nr < 8 and 0 <= nc < 8 and state[nr][nc] is None:
                    moves.append({'dest': (nr, nc), 'skipped': [], 'path': [(nr, nc)]})
                    step += 1
                else:
                    break
    else:
        dir_r = 1 if color == WHITE else -1
        dirs = [(dir_r, -1), (dir_r, 1)]
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 8 and 0 <= nc < 8 and state[nr][nc] is None:
                moves.append({'dest': (nr, nc), 'skipped': [], 'path': [(nr, nc)]})
                
    return moves

def get_moves_for_player(state, player_color):
    moves = {}
    max_skipped = 0
    
    for r in range(ROWS):
        for c in range(COLS):
            if state[r][c] and state[r][c][0] == player_color:
                piece_moves = get_piece_moves(state, r, c)
                if piece_moves:
                    moves[(r, c)] = piece_moves
                    for m in piece_moves:
                        if len(m['skipped']) > max_skipped:
                            max_skipped = len(m['skipped'])
                            
    filtered_moves = {}
    for start_pos, p_moves in moves.items():
        valid_p_moves = [m for m in p_moves if len(m['skipped']) == max_skipped]
        if valid_p_moves:
            filtered_moves[start_pos] = valid_p_moves
            
    return filtered_moves

class Game:
    def __init__(self):
        self.state = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.turn = WHITE
        self.selected = None
        self.valid_moves = {}
        self.winner = None
        self._init_board()
        
    def _init_board(self):
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 1:
                    if row < 3:
                        self.state[row][col] = (WHITE, False)
                    elif row > 4:
                        self.state[row][col] = (BLACK, False)

    def draw(self, win):
        win.fill(BEIGE)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, BROWN, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                
        if self.selected:
            r, c = self.selected
            x = c * SQUARE_SIZE + SQUARE_SIZE // 2
            y = r * SQUARE_SIZE + SQUARE_SIZE // 2
            draw_smooth_circle(win, BLUE, (x, y), SQUARE_SIZE // 2 - 5)
            
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.state[row][col]
                if piece:
                    color, is_king = piece
                    x = col * SQUARE_SIZE + SQUARE_SIZE // 2
                    y = row * SQUARE_SIZE + SQUARE_SIZE // 2
                    
                    draw_smooth_circle(win, GREY, (x, y), SQUARE_SIZE // 2 - 10)
                    draw_smooth_circle(win, color, (x, y), SQUARE_SIZE // 2 - 12)
                    
                    if is_king:
                        draw_smooth_circle(win, GOLD, (x, y), SQUARE_SIZE // 4)
                        draw_smooth_circle(win, color, (x, y), SQUARE_SIZE // 4 - 2)

        if self.selected and self.selected in self.valid_moves:
            for move in self.valid_moves[self.selected]:
                r, c = move['dest']
                x = c * SQUARE_SIZE + SQUARE_SIZE // 2
                y = r * SQUARE_SIZE + SQUARE_SIZE // 2
                draw_smooth_circle(win, RED, (x, y), 10)

    def apply_move(self, start_pos, move):
        sr, sc = start_pos
        dr, dc = move['dest']
        color, is_king = self.state[sr][sc]
        
        for r, c in move['path']:
            if color == WHITE and r == 7:
                is_king = True
            elif color == BLACK and r == 0:
                is_king = True
                
        self.state[dr][dc] = (color, is_king)
        self.state[sr][sc] = None
        
        for rr, cc in move['skipped']:
            self.state[rr][cc] = None
            
        self.turn = BLACK if self.turn == WHITE else WHITE
        self.selected = None
        self.valid_moves = get_moves_for_player(self.state, self.turn)
        self.check_winner()

    def check_winner(self):
        w_count = sum(1 for r in range(ROWS) for c in range(COLS) if self.state[r][c] and self.state[r][c][0] == WHITE)
        b_count = sum(1 for r in range(ROWS) for c in range(COLS) if self.state[r][c] and self.state[r][c][0] == BLACK)
        
        if w_count == 0:
            self.winner = 'Black won'
        elif b_count == 0:
            self.winner = 'White won'
        elif not self.valid_moves:
            self.winner = 'Black won' if self.turn == WHITE else 'White won'

def draw_winner(win, text):
    font = pygame.font.SysFont('arial', 60, True)
    text_surface = font.render(text, True, RED)
    rect = text_surface.get_rect(center=(WIDTH//2, HEIGHT//2))
    win.blit(text_surface, rect)

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game()
    game.valid_moves = get_moves_for_player(game.state, game.turn)
    
    while run:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            if event.type == pygame.MOUSEBUTTONDOWN and not game.winner:
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE
                
                if game.selected:
                    move_chosen = None
                    for move in game.valid_moves.get(game.selected, []):
                        if move['dest'] == (row, col):
                            move_chosen = move
                            break
                            
                    if move_chosen:
                        game.apply_move(game.selected, move_chosen)
                    else:
                        if game.state[row][col] and game.state[row][col][0] == game.turn and (row, col) in game.valid_moves:
                            game.selected = (row, col)
                        else:
                            game.selected = None
                else:
                    if game.state[row][col] and game.state[row][col][0] == game.turn and (row, col) in game.valid_moves:
                        game.selected = (row, col)
                        
        game.draw(WIN)
        
        if game.winner:
            draw_winner(WIN, game.winner)
            
        pygame.display.update()
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()