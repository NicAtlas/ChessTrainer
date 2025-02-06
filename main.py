import pygame
import chess
from puzzle_mode import PuzzleSystem
from opening_trainer import OpeningTrainer
from chess_engine import ChessEngine
import random

class ChessTrainer:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()  # Initialize sound system
        self.screen_size = 800
        # Make window wider to accommodate side panel
        self.screen = pygame.display.set_mode((self.screen_size + 400, self.screen_size))
        pygame.display.set_caption("Chess Trainer")
        
        # Initialize fonts
        self.title_font = pygame.font.Font(None, 64)
        self.menu_font = pygame.font.Font(None, 36)
        
        self.board = chess.Board()
        self.square_size = self.screen_size // 8
        self.selected_piece = None
        self.dragging = False
        self.dragged_piece = None
        self.dragged_pos = None
        self.legal_moves = set()  # Store legal moves for the selected piece
        
        self.puzzle_system = PuzzleSystem()
        self.opening_trainer = OpeningTrainer()
        self.chess_engine = None  # Will be initialized when difficulty is chosen
        
        # Game states: 'menu', 'puzzle', 'opening', 'bot', 'difficulty_select', 'opening_select', 'puzzle_select', 'theme_select'
        self.current_state = 'menu'
        self.selected_difficulty = None
        
        self.waiting_for_computer = False
        self.computer_move_delay = 500  # 500ms delay for computer moves
        self.last_move_time = 0
        
        # Add color themes
        self.color_themes = {
            'Classic': {
                'light_square': (240, 217, 181),
                'dark_square': (181, 136, 99),
                'legal_move': (130, 151, 105, 150),
                'selected': (186, 202, 43, 150),
                'background': (181, 136, 99),
                'button': (101, 67, 33),
                'text': (240, 217, 181),
                'sidebar': (240, 217, 181)
            },
            'Midnight': {
                'light_square': (108, 117, 125),
                'dark_square': (58, 59, 60),
                'legal_move': (169, 27, 13, 150),
                'selected': (200, 40, 20, 150),
                'background': (40, 40, 40),
                'button': (20, 20, 20),
                'text': (200, 200, 200),
                'sidebar': (80, 80, 80)
            },
            'Forest': {
                'light_square': (173, 189, 143),
                'dark_square': (87, 116, 71),
                'legal_move': (155, 103, 60, 150),
                'selected': (184, 139, 74, 150),
                'background': (76, 99, 60),
                'button': (56, 79, 40),
                'text': (238, 238, 210),
                'sidebar': (173, 189, 143)
            },
            'Ocean': {
                'light_square': (164, 214, 233),
                'dark_square': (100, 149, 237),
                'legal_move': (255, 140, 0, 150),
                'selected': (255, 165, 0, 150),
                'background': (25, 25, 112),
                'button': (0, 0, 139),
                'text': (240, 248, 255),
                'sidebar': (176, 224, 230)
            }
        }
        self.current_theme = 'Classic'
        self.colors = self.color_themes[self.current_theme]
        
        # Add text rendering for opening descriptions
        self.description_font = pygame.font.Font(None, 24)
        self.error_message = None
        self.error_time = 0
        self.error_duration = 2000  # Show error messages for 2 seconds
        
        # Add button for return to menu
        self.return_button_rect = pygame.Rect(20, 20, 150, 40)
        
        self.board_flipped = False  # Track board orientation
        
        # Add promotion dialog properties
        self.promotion_dialog = None
        self.promotion_move = None
        self.promotion_buttons = {}
        self.promotion_pieces = ['q', 'r', 'b', 'n']  # Queen, Rook, Bishop, Knight
        
        self.puzzle_completed = False
        self.next_random_puzzle_button_rect = pygame.Rect(self.screen_size + 50, self.screen_size - 120, 300, 40)
        
        # Add flip board button
        self.flip_button_rect = pygame.Rect(self.screen_size + 100, self.screen_size - 180, 200, 40)
        
        # Add game end state
        self.game_end_message = None
        self.game_end_time = 0
        self.game_end_duration = 5000  # Show end game message for 5 seconds
        
        self.hint_button_rect = pygame.Rect(self.screen_size + 100, self.screen_size - 240, 200, 40)
        self.colors['hint'] = (255, 223, 0, 150)  # Yellow with transparency
        
        self.load_assets()
        
    def load_assets(self):
        # Load piece images
        self.pieces = {}
        piece_names = {
            'p': 'pawn',
            'n': 'knight',
            'b': 'bishop',
            'r': 'rook',
            'q': 'queen',
            'k': 'king'
        }
        
        for piece_symbol, piece_name in piece_names.items():
            # Load white pieces
            img_path = f'pieces/white_{piece_name}.png'
            self.pieces[f'w{piece_symbol}'] = pygame.image.load(img_path)
            self.pieces[f'w{piece_symbol}'] = pygame.transform.scale(
                self.pieces[f'w{piece_symbol}'], 
                (self.square_size, self.square_size)
            )
            
            # Load black pieces
            img_path = f'pieces/black_{piece_name}.png'
            self.pieces[f'b{piece_symbol}'] = pygame.image.load(img_path)
            self.pieces[f'b{piece_symbol}'] = pygame.transform.scale(
                self.pieces[f'b{piece_symbol}'], 
                (self.square_size, self.square_size)
            )
        
        # Load sound effects
        self.sounds = {
            'move': pygame.mixer.Sound('sounds/Move.ogg'),
            'capture': pygame.mixer.Sound('sounds/Capture.ogg'),
            'check': pygame.mixer.Sound('sounds/Check.ogg')
        }

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                # Adjust coordinates if board is flipped
                actual_row = row if not self.board_flipped else 7 - row
                actual_col = col if not self.board_flipped else 7 - col
                
                color = self.colors['light_square'] if (row + col) % 2 == 0 else self.colors['dark_square']
                pygame.draw.rect(
                    self.screen, 
                    color, 
                    (actual_col * self.square_size, actual_row * self.square_size, 
                     self.square_size, self.square_size)
                )
        
        # Highlight legal moves
        if self.selected_piece is not None:
            # Highlight selected square
            file = chess.square_file(self.selected_piece)
            rank = chess.square_rank(self.selected_piece)
            if self.board_flipped:
                file = 7 - file
                rank = 7 - rank
            s = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
            pygame.draw.rect(s, self.colors['selected'], s.get_rect())
            self.screen.blit(s, (file * self.square_size, (7-rank) * self.square_size))
            
            # Highlight legal moves
            for move in self.legal_moves:
                file = chess.square_file(move.to_square)
                rank = chess.square_rank(move.to_square)
                if self.board_flipped:
                    file = 7 - file
                    rank = 7 - rank
                s = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
                pygame.draw.rect(s, self.colors['legal_move'], s.get_rect())
                self.screen.blit(s, (file * self.square_size, (7-rank) * self.square_size))

        # Draw hint square if exists
        if self.current_state == 'puzzle' and self.puzzle_system.hint_square is not None:
            file = chess.square_file(self.puzzle_system.hint_square)
            rank = chess.square_rank(self.puzzle_system.hint_square)
            if self.board_flipped:
                file = 7 - file
                rank = 7 - rank
            s = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
            pygame.draw.rect(s, self.colors['hint'], s.get_rect())
            self.screen.blit(s, (file * self.square_size, (7-rank) * self.square_size))

    def draw_pieces(self):
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece is not None and square != self.selected_piece:
                file = chess.square_file(square)
                rank = chess.square_rank(square)
                if self.board_flipped:
                    file = 7 - file
                    rank = 7 - rank
                x = file * self.square_size
                y = (7 - rank) * self.square_size
                piece_symbol = piece.symbol().lower()
                color = 'w' if piece.color else 'b'
                self.screen.blit(self.pieces[f'{color}{piece_symbol}'], (x, y))
        
        # Draw dragged piece last
        if self.dragging and self.selected_piece is not None:
            piece = self.board.piece_at(self.selected_piece)
            if piece and self.dragged_pos:
                piece_symbol = piece.symbol().lower()
                color = 'w' if piece.color else 'b'
                x, y = self.dragged_pos
                x -= self.square_size // 2
                y -= self.square_size // 2
                self.screen.blit(self.pieces[f'{color}{piece_symbol}'], (x, y))

    def play_sound(self, sound_type):
        """Play a sound effect"""
        if sound_type in self.sounds:
            self.sounds[sound_type].play()

    def draw_menu(self):
        self.screen.fill(self.colors['background'])
        
        # Draw title
        title = self.title_font.render("Welcome to Chess Trainer", True, self.colors['text'])
        title_rect = title.get_rect(center=(self.screen_size//2, 100))
        self.screen.blit(title, title_rect)
        
        # Menu options
        options = [
            ("Learn an Opening", "opening_select"),
            ("Play Puzzles", "puzzle_select"),
            ("Play vs Bot", "difficulty_select"),
            ("Change Theme", "theme_select")  # Add theme option
        ]
        
        for i, (text, state) in enumerate(options):
            button = self.menu_font.render(text, True, self.colors['text'])
            button_rect = button.get_rect(center=(self.screen_size//2, 250 + i*100))
            
            # Draw button background
            pygame.draw.rect(self.screen, self.colors['button'], 
                           button_rect.inflate(20, 10))
            self.screen.blit(button, button_rect)
            
            # Store button rect for click detection
            setattr(self, f"{state}_rect", button_rect)

    def draw_difficulty_select(self):
        self.screen.fill((181, 136, 99))
        title = self.title_font.render("Select Bot Difficulty", True, (240, 217, 181))
        title_rect = title.get_rect(center=(self.screen_size//2, 100))
        self.screen.blit(title, title_rect)
        
        difficulties = [
            ("Easy", 2),
            ("Medium", 3),
            ("Hard", 4)
        ]
        
        for i, (text, depth) in enumerate(difficulties):
            button = self.menu_font.render(text, True, (240, 217, 181))
            button_rect = button.get_rect(center=(self.screen_size//2, 250 + i*100))
            pygame.draw.rect(self.screen, (101, 67, 33), button_rect.inflate(20, 10))
            self.screen.blit(button, button_rect)
            setattr(self, f"difficulty_{depth}_rect", button_rect)

    def draw_puzzle_select(self):
        self.screen.fill((181, 136, 99))
        title = self.title_font.render("Select Puzzle Difficulty", True, (240, 217, 181))
        title_rect = title.get_rect(center=(self.screen_size//2, 100))
        self.screen.blit(title, title_rect)
        
        difficulties = [
            ("Beginner (<1200)", (0, 1200)),
            ("Intermediate (1200-1800)", (1200, 1800)),
            ("Advanced (1800-2400)", (1800, 2400)),
            ("Expert (>2400)", (2400, 3000))
        ]
        
        for i, (text, rating_range) in enumerate(difficulties):
            button = self.menu_font.render(text, True, (240, 217, 181))
            button_rect = button.get_rect(center=(self.screen_size//2, 250 + i*80))
            pygame.draw.rect(self.screen, (101, 67, 33), button_rect.inflate(20, 10))
            self.screen.blit(button, button_rect)
            setattr(self, f"puzzle_range_{rating_range[0]}_{rating_range[1]}_rect", button_rect)

    def handle_menu_click(self, pos):
        if hasattr(self, 'opening_select_rect') and self.opening_select_rect.collidepoint(pos):
            self.current_state = 'opening_select'
        elif hasattr(self, 'puzzle_select_rect') and self.puzzle_select_rect.collidepoint(pos):
            self.current_state = 'puzzle_select'
        elif hasattr(self, 'difficulty_select_rect') and self.difficulty_select_rect.collidepoint(pos):
            self.current_state = 'difficulty_select'
        elif hasattr(self, 'theme_select_rect') and self.theme_select_rect.collidepoint(pos):
            self.current_state = 'theme_select'

    def handle_difficulty_click(self, pos):
        for depth in [2, 3, 4]:
            rect_name = f'difficulty_{depth}_rect'
            if hasattr(self, rect_name) and getattr(self, rect_name).collidepoint(pos):
                self.chess_engine = ChessEngine(depth)
                self.current_state = 'bot'
                self.board.reset()
                self.board_flipped = False  # Player is always White
                return

    def handle_puzzle_click(self, pos):
        ranges = [(0, 1200), (1200, 1800), (1800, 2400), (2400, 3000)]
        for min_rating, max_rating in ranges:
            rect_name = f'puzzle_range_{min_rating}_{max_rating}_rect'
            if hasattr(self, rect_name) and getattr(self, rect_name).collidepoint(pos):
                # Load puzzle and set up initial position
                self.puzzle_system.load_puzzle((min_rating, max_rating))
                self.current_state = 'puzzle'
                self.board = self.puzzle_system.get_current_board()
                
                # Always flip board so player's pieces are at bottom
                self.board_flipped = self.board.turn
                
                # Set up the first move to be animated
                self.waiting_for_computer = True
                self.last_move_time = pygame.time.get_ticks()
                return

    def handle_opening_click(self, pos):
        """Handle clicks in opening trainer mode"""
        # Check if return to menu button was clicked
        if self.return_button_rect.collidepoint(pos):
            self.current_state = 'menu'
            self.board.reset()
            return
        
        # Check if we're selecting an opening from the menu
        if self.current_state == 'opening_select':
            for opening_key in self.opening_trainer.openings:
                rect_name = f"opening_{opening_key}_rect"
                if hasattr(self.opening_trainer, rect_name):
                    rect = getattr(self.opening_trainer, rect_name)
                    if rect.collidepoint(pos):
                        self.opening_trainer.start_opening(opening_key)
                        self.current_state = 'opening'
                        self.board.reset()
                        return

    def draw_game_sidebar(self):
        """Draw the common sidebar for all game modes"""
        # Create a side panel for text
        panel_rect = pygame.Rect(self.screen_size, 0, 400, self.screen_size)  # 400px wide panel
        pygame.draw.rect(self.screen, (240, 217, 181), panel_rect)  # Light background for panel
        
        # Update return button position to be in the side panel
        self.return_button_rect = pygame.Rect(self.screen_size + 100, self.screen_size - 60, 200, 40)
        pygame.draw.rect(self.screen, (101, 67, 33), self.return_button_rect)
        return_text = self.menu_font.render("Return to Menu", True, (240, 217, 181))
        return_rect = return_text.get_rect(center=self.return_button_rect.center)
        self.screen.blit(return_text, return_rect)
        
        # Draw flip board button
        pygame.draw.rect(self.screen, (101, 67, 33), self.flip_button_rect)
        flip_text = self.menu_font.render("Flip Board", True, (240, 217, 181))
        flip_rect = flip_text.get_rect(center=self.flip_button_rect.center)
        self.screen.blit(flip_text, flip_rect)

    def draw_puzzle_info(self):
        """Draw puzzle information in sidebar"""
        self.draw_game_sidebar()
        
        if self.puzzle_system.get_completion_message():
            # Draw congratulations message
            congrats_text = self.menu_font.render(
                self.puzzle_system.get_completion_message(), 
                True, (0, 100, 0)
            )
            self.screen.blit(congrats_text, (self.screen_size + 20, 20))
            
            # Draw puzzle rating info
            rating_text = self.description_font.render(
                f"Puzzle Rating: {self.puzzle_system.current_puzzle['rating']}", 
                True, (0, 0, 0)
            )
            self.screen.blit(rating_text, (self.screen_size + 20, 60))
            
            # Draw wider next random puzzle button
            pygame.draw.rect(self.screen, (101, 67, 33), self.next_random_puzzle_button_rect)
            next_text = self.menu_font.render("Next Random Puzzle", True, (240, 217, 181))
            next_rect = next_text.get_rect(center=self.next_random_puzzle_button_rect.center)
            self.screen.blit(next_text, next_rect)
        
        elif self.puzzle_system.current_puzzle:
            # Draw puzzle rating
            rating_text = self.menu_font.render(
                f"Puzzle Rating: {self.puzzle_system.current_puzzle['rating']}", 
                True, (0, 0, 0)
            )
            self.screen.blit(rating_text, (self.screen_size + 20, 20))
            
            # Draw puzzle themes
            themes_text = self.menu_font.render("Themes:", True, (0, 0, 0))
            self.screen.blit(themes_text, (self.screen_size + 20, 60))
            
            y_offset = 90
            for theme in self.puzzle_system.current_puzzle['themes']:
                theme_text = self.description_font.render(f"• {theme}", True, (0, 0, 0))
                self.screen.blit(theme_text, (self.screen_size + 40, y_offset))
                y_offset += 25

            # Draw hint button if puzzle is not completed
            pygame.draw.rect(self.screen, (101, 67, 33), self.hint_button_rect)
            hint_text = self.menu_font.render("Show Hint", True, (240, 217, 181))
            hint_rect = hint_text.get_rect(center=self.hint_button_rect.center)
            self.screen.blit(hint_text, hint_rect)

    def draw_bot_info(self):
        """Draw bot game information in sidebar"""
        self.draw_game_sidebar()
        
        # Draw difficulty level
        if self.selected_difficulty:
            difficulty_text = self.menu_font.render(f"Bot Difficulty: {self.selected_difficulty}", 
                                                  True, (0, 0, 0))
            self.screen.blit(difficulty_text, (self.screen_size + 20, 20))
        
        # Draw turn indicator
        turn_text = self.menu_font.render("Your turn" if self.board.turn else "Bot's turn", 
                                        True, (0, 0, 0))
        self.screen.blit(turn_text, (self.screen_size + 20, 60))
        
        # Draw game end message if exists
        if self.game_end_message:
            current_time = pygame.time.get_ticks()
            if current_time - self.game_end_time < self.game_end_duration:
                message_color = (0, 150, 0) if "won" in self.game_end_message.lower() else (150, 0, 0)
                end_text = self.menu_font.render(self.game_end_message, True, message_color)
                self.screen.blit(end_text, (self.screen_size + 20, 100))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if self.current_state in ['opening', 'puzzle', 'bot']:
                    if event.pos[0] >= self.screen_size:  # Click is in side panel
                        if self.return_button_rect.collidepoint(event.pos):
                            self.current_state = 'menu'
                            self.board.reset()
                            self.puzzle_system.clear_completion()
                            return
                        elif self.flip_button_rect.collidepoint(event.pos):
                            self.board_flipped = not self.board_flipped
                            return
                        elif (self.current_state == 'puzzle' and 
                              self.puzzle_system.get_completion_message() and 
                              self.next_random_puzzle_button_rect.collidepoint(event.pos)):
                            # Load a completely random puzzle
                            self.puzzle_system.load_random_puzzle()
                            self.board = self.puzzle_system.get_current_board()
                            # Always flip board so player's pieces are at bottom
                            self.board_flipped = self.board.turn
                            self.waiting_for_computer = True
                            self.last_move_time = pygame.time.get_ticks()
                            self.puzzle_system.clear_completion()
                            return
                        elif (self.current_state == 'puzzle' and 
                              not self.puzzle_system.get_completion_message() and 
                              self.hint_button_rect.collidepoint(event.pos)):
                            self.puzzle_system.hint_square = self.puzzle_system.get_hint()
                            return
                        return  # Ignore other clicks in side panel
                
                # Only allow moves if puzzle is not completed
                if self.current_state == 'puzzle' and self.puzzle_system.get_completion_message():
                    return
                
                # Handle promotion dialog if active
                if self.promotion_dialog:
                    if self.handle_promotion_click(event.pos):
                        return
                
                # Handle regular board and menu clicks
                if self.current_state == 'menu':
                    self.handle_menu_click(event.pos)
                elif self.current_state == 'difficulty_select':
                    self.handle_difficulty_click(event.pos)
                elif self.current_state == 'puzzle_select':
                    self.handle_puzzle_click(event.pos)
                elif self.current_state == 'opening_select':
                    self.handle_opening_click(event.pos)
                elif self.current_state == 'theme_select':
                    self.handle_theme_click(event.pos)
                elif not self.waiting_for_computer:
                    # Only handle board clicks if they're within the board area
                    if event.pos[0] < self.screen_size:
                        # Only allow moves when it's player's turn (White)
                        if self.current_state == 'bot' and not self.board.turn:
                            return  # Don't allow moves when it's Black's turn
                        
                        file = event.pos[0] // self.square_size
                        rank = 7 - (event.pos[1] // self.square_size)
                        if self.board_flipped:
                            file = 7 - file
                            rank = 7 - rank
                        square = chess.square(file, rank)
                        
                        if self.board.piece_at(square):
                            self.selected_piece = square
                            self.dragging = True
                            self.dragged_pos = event.pos
                            self.legal_moves = {move for move in self.board.legal_moves 
                                              if move.from_square == square}

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.selected_piece is not None:
                # Only handle piece drops on the board area
                if event.pos[0] < self.screen_size:
                    file = event.pos[0] // self.square_size
                    rank = 7 - (event.pos[1] // self.square_size)
                    if self.board_flipped:
                        file = 7 - file
                        rank = 7 - rank
                    target_square = chess.square(file, rank)
                    
                    # Create move, adding queen promotion if it's a promotion move
                    move = chess.Move(self.selected_piece, target_square)
                    if self.is_promotion_move(move):
                        move = chess.Move(self.selected_piece, target_square, promotion=chess.QUEEN)
                    
                    if move in self.board.legal_moves:
                        # Handle move based on game state
                        if self.current_state == 'puzzle':
                            if self.puzzle_system.verify_move(move):
                                # Correct puzzle move
                                sound_type = 'capture' if self.board.piece_at(target_square) else 'move'
                                self.board.push(move)
                                self.play_sound(sound_type)
                                if self.board.is_check():
                                    self.play_sound('check')
                                
                                # Check for puzzle completion after player's move
                                if self.puzzle_system.is_puzzle_complete():
                                    self.puzzle_system.complete_puzzle()
                                    self.play_sound('check')
                                    return
                                
                                # Get computer's response if puzzle not complete
                                self.waiting_for_computer = True
                                self.last_move_time = pygame.time.get_ticks()
                        elif self.current_state == 'bot':
                            # Only handle player's moves (White)
                            if self.board.turn:  # White's turn
                                sound_type = 'capture' if self.board.piece_at(target_square) else 'move'
                                self.board.push(move)
                                self.play_sound(sound_type)
                                if self.board.is_check():
                                    self.play_sound('check')
                                self.check_game_end()
                        
                                # Prepare for bot's response
                                self.waiting_for_computer = True
                                self.last_move_time = pygame.time.get_ticks()
                        elif self.current_state == 'opening':
                            if not self.opening_trainer.is_opening_complete():
                                if self.opening_trainer.verify_move(move):
                                    # Correct opening move
                                    sound_type = 'capture' if self.board.piece_at(target_square) else 'move'
                                    self.board.push(move)
                                    self.play_sound(sound_type)
                                    if self.board.is_check():
                                        self.play_sound('check')
                                    
                                    # Make computer's response move if exists and opening not complete
                                    response = self.opening_trainer.get_next_move()
                                    if response and not self.opening_trainer.is_opening_complete():
                                        self.waiting_for_computer = True
                                        self.last_move_time = pygame.time.get_ticks()
                                else:
                                    # Wrong opening move
                                    self.error_message = "Incorrect move for this opening line"
                                    self.error_time = pygame.time.get_ticks()
                
                self.selected_piece = None
                self.dragging = False
                self.dragged_pos = None
                self.legal_moves = set()

                # Clear hint when making a move
                self.puzzle_system.clear_hint()

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.dragged_pos = event.pos

    def handle_computer_move(self):
        """Handle computer's move in puzzle or bot mode"""
        current_time = pygame.time.get_ticks()
        if self.waiting_for_computer and current_time - self.last_move_time >= self.computer_move_delay:
            if self.current_state == 'puzzle':
                if self.puzzle_system.current_move_index == 0:
                    first_move = self.puzzle_system.make_first_move()
                    if first_move:
                        sound_type = 'capture' if self.board.piece_at(first_move.to_square) else 'move'
                        self.play_sound(sound_type)
                        if self.board.is_check():
                            self.play_sound('check')
                else:
                    computer_move = self.puzzle_system.get_computer_response()
                    if computer_move:
                        sound_type = 'capture' if self.board.piece_at(computer_move.to_square) else 'move'
                        self.play_sound(sound_type)
                        if self.board.is_check():
                            self.play_sound('check')
            self.waiting_for_computer = False

    def draw_opening_info(self):
        """Draw opening description and error messages"""
        # Use common sidebar
        self.draw_game_sidebar()
        
        # Draw opening name and description in side panel
        if self.opening_trainer.current_opening:
            name = self.opening_trainer.current_opening['name']
            name_text = self.menu_font.render(name, True, (0, 0, 0))
            self.screen.blit(name_text, (self.screen_size + 20, 20))
            
            if self.opening_trainer.is_opening_complete():
                # Show full opening description when complete
                description = self.opening_trainer.get_current_opening_info()
                if description:
                    # Split description into multiple lines
                    y_offset = 60
                    # Wrap text to fit panel width
                    words = description.strip().split()
                    line = []
                    for word in words:
                        line.append(word)
                        text = ' '.join(line)
                        text_surface = self.description_font.render(text, True, (0, 0, 0))
                        if text_surface.get_width() > 360:  # Leave some margin
                            line.pop()
                            text = ' '.join(line)
                            text_surface = self.description_font.render(text, True, (0, 0, 0))
                            self.screen.blit(text_surface, (self.screen_size + 20, y_offset))
                            y_offset += 30
                            line = [word]
                    if line:
                        text = ' '.join(line)
                        text_surface = self.description_font.render(text, True, (0, 0, 0))
                        self.screen.blit(text_surface, (self.screen_size + 20, y_offset))
            elif self.board.move_stack:
                # Show move description during play
                last_move = self.board.peek()
                description = self.opening_trainer.get_move_description(last_move)
                if description:
                    desc_text = self.description_font.render(description, True, (0, 0, 0))
                    self.screen.blit(desc_text, (self.screen_size + 20, 60))
        
        # Draw error message if exists
        if self.error_message:
            current_time = pygame.time.get_ticks()
            if current_time - self.error_time < self.error_duration:
                error_text = self.description_font.render(self.error_message, True, (255, 0, 0))
                error_rect = error_text.get_rect(center=(self.screen_size//2, self.screen_size - 50))
                self.screen.blit(error_text, error_rect)
            else:
                self.error_message = None

    def draw_promotion_dialog(self):
        """Draw the promotion selection dialog"""
        if not self.promotion_dialog:
            return
        
        # Draw semi-transparent background
        s = pygame.Surface((self.screen_size, self.screen_size))
        s.set_alpha(128)
        s.fill((0, 0, 0))
        self.screen.blit(s, (0, 0))
        
        # Draw dialog box
        dialog_width = 400
        dialog_height = 120
        dialog_x = (self.screen_size - dialog_width) // 2
        dialog_y = (self.screen_size - dialog_height) // 2
        
        pygame.draw.rect(self.screen, (240, 217, 181), 
                        (dialog_x, dialog_y, dialog_width, dialog_height))
        pygame.draw.rect(self.screen, (101, 67, 33), 
                        (dialog_x, dialog_y, dialog_width, dialog_height), 2)
        
        # Draw piece options
        piece_size = 60
        spacing = 20
        total_width = (piece_size + spacing) * len(self.promotion_pieces)
        start_x = dialog_x + (dialog_width - total_width) // 2
        
        self.promotion_buttons.clear()
        color = 'w' if self.board.turn else 'b'
        
        for i, piece in enumerate(self.promotion_pieces):
            x = start_x + i * (piece_size + spacing)
            y = dialog_y + (dialog_height - piece_size) // 2
            
            # Draw piece button
            button_rect = pygame.Rect(x, y, piece_size, piece_size)
            pygame.draw.rect(self.screen, (181, 136, 99), button_rect)
            
            # Draw piece image
            piece_img = self.pieces[f'{color}{piece}']
            self.screen.blit(piece_img, button_rect)
            
            # Store button rect for click detection
            self.promotion_buttons[piece] = button_rect

    def handle_promotion_click(self, pos):
        """Handle clicks in the promotion dialog"""
        for piece, rect in self.promotion_buttons.items():
            if rect.collidepoint(pos):
                # Create the promotion move
                move = chess.Move(
                    self.promotion_move.from_square,
                    self.promotion_move.to_square,
                    promotion=chess.Piece.from_symbol(piece).piece_type
                )
                
                # Make the move
                self.board.push(move)
                sound_type = 'capture' if self.board.piece_at(move.to_square) else 'move'
                self.play_sound(sound_type)
                if self.board.is_check():
                    self.play_sound('check')
                
                # Clear promotion state
                self.promotion_dialog = None
                self.promotion_move = None
                
                # Handle computer response if needed
                if self.current_state in ['puzzle', 'bot', 'opening']:
                    self.waiting_for_computer = True
                    self.last_move_time = pygame.time.get_ticks()
                
                return True
        return False

    def is_promotion_move(self, move):
        """Check if a move would result in pawn promotion"""
        piece = self.board.piece_at(move.from_square)
        if piece and piece.piece_type == chess.PAWN:
            rank = chess.square_rank(move.to_square)
            return (piece.color and rank == 7) or (not piece.color and rank == 0)
        return False

    def get_rating_range(self, rating):
        """Get the rating range for a given rating"""
        if rating < 1200:
            return (0, 1200)
        elif rating < 1800:
            return (1200, 1800)
        elif rating < 2400:
            return (1800, 2400)
        else:
            return (2400, 3000)

    def check_game_end(self):
        """Check if the game has ended and set appropriate message"""
        if self.board.is_checkmate():
            if self.board.turn:  # Black won (bot)
                self.game_end_message = "The bot crushed you! Better luck next time!"
            else:  # White won (player)
                self.game_end_message = "Congratulations! You defeated the bot!"
            self.game_end_time = pygame.time.get_ticks()
        elif self.board.is_stalemate() or self.board.is_insufficient_material():
            self.game_end_message = "Game drawn! Not bad!"
            self.game_end_time = pygame.time.get_ticks()

    def draw_theme_select(self):
        """Draw theme selection menu"""
        self.screen.fill(self.colors['background'])
        title = self.title_font.render("Select Theme", True, self.colors['text'])
        title_rect = title.get_rect(center=(self.screen_size//2, 100))
        self.screen.blit(title, title_rect)
        
        # Draw theme options
        for i, theme_name in enumerate(self.color_themes.keys()):
            button = self.menu_font.render(theme_name, True, self.color_themes[theme_name]['text'])
            button_rect = button.get_rect(center=(self.screen_size//2, 250 + i*80))
            
            # Draw button using theme's own colors
            pygame.draw.rect(self.screen, self.color_themes[theme_name]['button'], 
                           button_rect.inflate(20, 10))
            self.screen.blit(button, button_rect)
            
            # Store button rect for click detection
            setattr(self, f"theme_{theme_name.lower()}_rect", button_rect)
        
        # Draw back button
        back_button = self.menu_font.render("Back", True, self.colors['text'])
        self.back_button_rect = back_button.get_rect(center=(self.screen_size//2, 550))
        pygame.draw.rect(self.screen, self.colors['button'], 
                        self.back_button_rect.inflate(20, 10))
        self.screen.blit(back_button, self.back_button_rect)

    def handle_theme_click(self, pos):
        """Handle clicks in theme selection menu"""
        # Check theme buttons
        for theme_name in self.color_themes.keys():
            rect_name = f"theme_{theme_name.lower()}_rect"
            if hasattr(self, rect_name) and getattr(self, rect_name).collidepoint(pos):
                self.current_theme = theme_name
                self.colors = self.color_themes[theme_name]
                self.current_state = 'menu'
                return
        
        # Check back button
        if hasattr(self, 'back_button_rect') and self.back_button_rect.collidepoint(pos):
            self.current_state = 'menu'

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.handle_event(event)
            
            # Handle computer moves
            if self.waiting_for_computer:
                self.handle_computer_move()
            
            self.screen.fill((255, 255, 255))
            
            if self.current_state == 'menu':
                self.draw_menu()
            elif self.current_state == 'difficulty_select':
                self.draw_difficulty_select()
            elif self.current_state == 'puzzle_select':
                self.draw_puzzle_select()
            elif self.current_state == 'opening_select':
                self.opening_trainer.draw_opening_select(self.screen, self.menu_font)
            elif self.current_state == 'theme_select':
                self.draw_theme_select()
            else:
                self.draw_board()
                self.draw_pieces()
                if self.current_state == 'opening':
                    self.draw_opening_info()
                elif self.current_state == 'puzzle':
                    self.draw_puzzle_info()
                elif self.current_state == 'bot':
                    self.draw_bot_info()
                if self.promotion_dialog:
                    self.draw_promotion_dialog()
            
            pygame.display.flip()
        
        pygame.quit()

if __name__ == "__main__":
    trainer = ChessTrainer()
    trainer.run()
