import chess
import pygame

class OpeningTrainer:
    def __init__(self):
        self.openings = self.load_openings()
        self.current_opening = None
        self.current_position = None
        self.progress = {}
        
    def load_openings(self):
        """Load opening database"""
        return {
            'ruy_lopez': {
                'name': 'Ruy Lopez',
                'moves': ['e2e4', 'e7e5', 'g1f3', 'b8c6', 'f1b5'],
                'descriptions': {
                    'e2e4': 'Controls the center with the king pawn',
                    'g1f3': 'Develops the kingside knight and attacks e5',
                    'f1b5': 'The Ruy Lopez move, pinning the knight'
                }
            },
            'sicilian_defense': {
                'name': 'Sicilian Defense',
                'moves': ['e2e4', 'c7c5'],
                'descriptions': {
                    'e2e4': 'Controls the center with the king pawn',
                    'c7c5': 'The Sicilian Defense, fighting for the d4 square'
                }
            },
            'queens_gambit': {
                'name': "Queen's Gambit",
                'moves': ['d2d4', 'd7d5', 'c2c4'],
                'descriptions': {
                    'd2d4': 'Controls the center with the queen pawn',
                    'c2c4': 'The gambit pawn, offering it for better development'
                }
            },
            'kings_indian': {
                'name': "King's Indian Defense",
                'moves': ['d2d4', 'g8f6', 'c2c4', 'g7g6'],
                'descriptions': {
                    'd2d4': 'Controls the center with the queen pawn',
                    'g8f6': 'Develops the kingside knight',
                    'g7g6': 'Prepares to fianchetto the bishop'
                }
            },
            'french_defense': {
                'name': "French Defense",
                'moves': ['e2e4', 'e7e6'],
                'descriptions': {
                    'e2e4': 'Controls the center with the king pawn',
                    'e7e6': 'The French Defense, preparing to challenge the center'
                }
            },
            'caro_kann': {
                'name': "Caro-Kann Defense",
                'moves': ['e2e4', 'c7c6'],
                'descriptions': {
                    'e2e4': 'Controls the center with the king pawn',
                    'c7c6': 'The Caro-Kann, preparing to support d5'
                }
            },
            'italian_game': {
                'name': "Italian Game",
                'moves': ['e2e4', 'e7e5', 'g1f3', 'b8c6', 'f1c4'],
                'descriptions': {
                    'e2e4': 'Controls the center with the king pawn',
                    'g1f3': 'Develops the kingside knight and attacks e5',
                    'f1c4': 'The Italian Game, developing the bishop to attack f7'
                }
            },
            'london_system': {
                'name': "London System",
                'moves': ['d2d4', 'd7d5', 'c1f4'],
                'descriptions': {
                    'd2d4': 'Controls the center with the queen pawn',
                    'c1f4': 'The London System setup, developing the light bishop'
                }
            }
        }
    
    def start_opening(self, opening_name):
        """Start practicing a specific opening"""
        if opening_name in self.openings:
            self.current_opening = self.openings[opening_name]
            self.current_position = chess.Board()
            return True
        return False
    
    def verify_move(self, move):
        """Verify if the move follows the opening line"""
        if not self.current_opening:
            return False
            
        current_move_index = len(self.current_position.move_stack)
        if current_move_index >= len(self.current_opening['moves']):
            return False
            
        expected_move = self.current_opening['moves'][current_move_index]
        return move.uci() == expected_move
    
    def get_move_description(self, move):
        """Get the description for a specific move"""
        if not self.current_opening:
            return ""
            
        return self.current_opening['descriptions'].get(move.uci(), "")
    
    def track_progress(self, opening_name, success):
        """Track opening practice progress"""
        if opening_name not in self.progress:
            self.progress[opening_name] = {
                'attempts': 0,
                'successes': 0
            }
        
        self.progress[opening_name]['attempts'] += 1
        if success:
            self.progress[opening_name]['successes'] += 1
    
    def get_completion_rate(self, opening_name):
        """Get completion rate for an opening"""
        if opening_name not in self.progress:
            return 0
            
        stats = self.progress[opening_name]
        if stats['attempts'] == 0:
            return 0
            
        return stats['successes'] / stats['attempts']

    def draw_opening_select(self, screen, font):
        """Draw opening selection menu"""
        screen.fill((181, 136, 99))
        title = pygame.font.Font(None, 64).render("Select an Opening", True, (240, 217, 181))
        title_rect = title.get_rect(center=(screen.get_width()//2, 100))
        screen.blit(title, title_rect)
        
        row = 0
        col = 0
        button_width = 300
        button_height = 60
        padding = 20
        
        for opening_key, opening_data in self.openings.items():
            button = font.render(opening_data['name'], True, (240, 217, 181))
            button_rect = button.get_rect(
                center=(200 + col*(button_width + padding),
                       200 + row*(button_height + padding))
            )
            pygame.draw.rect(screen, (101, 67, 33), button_rect.inflate(20, 10))
            screen.blit(button, button_rect)
            
            # Store button rect for click detection
            setattr(self, f"opening_{opening_key}_rect", button_rect)
            
            col += 1
            if col > 1:
                col = 0
                row += 1

    def get_next_move(self):
        """Get the next move in the opening line"""
        if not self.current_opening:
            return None
        
        current_move_index = len(self.current_position.move_stack)
        if current_move_index >= len(self.current_opening['moves']):
            return None
        
        next_move = chess.Move.from_uci(self.current_opening['moves'][current_move_index])
        self.current_position.push(next_move)
        return next_move

    def get_opening_info(self, opening_name):
        """Get detailed information about an opening"""
        opening_descriptions = {
            'ruy_lopez': """
            You've completed the main line of the Ruy Lopez opening!

            The Ruy Lopez is one of the oldest and most classic chess openings. Named after Spanish priest Ruy López de Segura 
            from the 16th century, it begins with 1.e4 e5 2.Nf3 Nc6 3.Bb5. The opening aims to attack Black's e5 pawn and 
            create pressure on Black's position. It remains one of the most popular openings at all levels of chess.
            """,
            'sicilian_defense': """
            You've completed the main line of the Sicilian Defense!

            The Sicilian Defense is the most popular response to White's 1.e4. By playing 1...c5, Black immediately fights 
            for the center and creates an imbalanced position. It's known for leading to sharp, tactical play and is favored 
            by players who like to play for a win with Black. Many World Champions have relied on the Sicilian Defense.
            """,
            'queens_gambit': """
            You've completed the main line of the Queen's Gambit!

            The Queen's Gambit (1.d4 d5 2.c4) is one of the oldest known chess openings. White offers a pawn to gain control 
            of the center. Despite its name, it's not a true gambit as Black cannot safely keep the pawn. The Queen's Gambit 
            is considered one of the most reliable openings for White and was featured in the popular Netflix series.
            """,
            'kings_indian': """
            You've completed the main line of the King's Indian Defense!

            The King's Indian Defense is a hypermodern opening where Black allows White to build a broad pawn center with d4 
            and c4, then challenges it with piece pressure. It's known for leading to complex positions with opposite-side 
            attacks. Many aggressive players, including Garry Kasparov, have used it successfully at the highest levels.
            """,
            'french_defense': """
            You've completed the main line of the French Defense!

            The French Defense (1.e4 e6) is a solid choice for Black that leads to closed, strategic positions. Black aims to 
            challenge White's center with ...d5 and often develops a strong pawn chain. The opening was named after a 1834 
            correspondence match between Paris and London, and is known for its solid but somewhat cramped positions.
            """,
            'caro_kann': """
            You've completed the main line of the Caro-Kann Defense!

            The Caro-Kann Defense (1.e4 c6) is a solid opening for Black, named after Horatio Caro and Marcus Kann. It's 
            similar to the French Defense but avoids the blocked bishop problem. Black aims to support ...d5 with the c-pawn 
            first. It's known for being one of the most solid and positionally sound defenses to 1.e4.
            """,
            'italian_game': """
            You've completed the main line of the Italian Game!

            The Italian Game (1.e4 e5 2.Nf3 Nc6 3.Bc4) is one of the oldest recorded chess openings. White develops naturally 
            and aims the bishop at Black's weak f7 square. It leads to open games with many tactical possibilities. The opening 
            was popular during the romantic era of chess and has recently seen a revival at the highest levels.
            """,
            'london_system': """
            You've completed the main line of the London System!

            The London System is a popular opening system for White where pieces are developed to standard squares regardless 
            of Black's setup. It's characterized by an early Bf4 and is considered very reliable and low-risk. Popular among 
            club players and recently adopted by top players, it's known for being a solid, systematic opening choice.
            """
        }
        return opening_descriptions.get(opening_name, "No detailed description available.")

    def is_opening_complete(self):
        """Check if all moves in the opening line have been played"""
        if not self.current_opening:
            return False
        return len(self.current_position.move_stack) >= len(self.current_opening['moves'])

    def get_current_opening_info(self):
        """Get info for the current opening"""
        if not self.current_opening:
            return None
        return self.get_opening_info(
            next(key for key, value in self.openings.items() 
                 if value == self.current_opening)
        )
