import chess
import random

CHESS_PUZZLES = [
    {
        "fen": "r6k/pp2r2p/4Rp1Q/3p4/8/1N1P2R1/PqP2bPP/7K b - - 0 24",
        "moves": ["f2g3", "e6e7", "b2b1", "b3c1", "b1c1", "h6c1"],
        "rating": 1925,
        "themes": ["crushing", "hangingPiece", "long", "middlegame"]
    },
    {
        "fen": "5rk1/1p3ppp/pq3b2/8/8/1P1Q1N2/P4PPP/3R2K1 w - - 2 27",
        "moves": ["d3d6", "f8d8", "d6d8", "f6d8"],
        "rating": 1547,
        "themes": ["advantage", "endgame", "short"]
    },
    {
        "fen": "8/4R3/1p2P3/p4r2/P6p/1P3Pk1/4K3/8 w - - 1 64",
        "moves": ["e7f7", "f5e5", "e2f1", "e5e6"],
        "rating": 1266,
        "themes": ["advantage", "endgame", "rookEndgame", "short"]
    },
    {
        "fen": "r2qr1k1/b1p2ppp/pp4n1/P1P1p3/4P1n1/B2P2Pb/3NBP1P/RN1QR1K1 b - - 1 16",
        "moves": ["b6c5", "e2g4", "h3g4", "d1g4"],
        "rating": 1093,
        "themes": ["advantage", "middlegame", "short"]
    },
    {
        "fen": "r4r2/1p3pkp/p5p1/3R1N1Q/3P4/8/P1q2P2/3R2K1 b - - 3 25",
        "moves": ["g6f5", "d5c5", "c2e4", "h5g5", "g7h8", "g5f6"],
        "rating": 2793,
        "themes": ["crushing", "endgame", "long"]
    },
    {
        "fen": "7r/6k1/2b1pp2/8/P1N3p1/5nP1/4RP2/Q4K2 w - - 2 38",
        "moves": ["e2e6", "h8h1", "f1e2", "h1a1"],
        "rating": 1497,
        "themes": ["advantage", "endgame", "short", "skewer"]
    },
    {
        "fen": "5r1k/pp4pp/5p2/1BbQp1r1/6K1/7P/1PP3P1/3R3R w - - 2 26",
        "moves": ["g4h4", "c5f2", "g2g3", "f2g3"],
        "rating": 1018,
        "themes": ["mate", "mateIn2", "middlegame", "short"]
    },
    {
        "fen": "2r3k1/p1q2pp1/Q3p2p/b1Np4/2nP1P2/4P1P1/5K1P/2B1N3 b - - 3 33",
        "moves": ["c7b6", "a6c8", "g8h7", "c8b7"],
        "rating": 2175,
        "themes": ["advantage", "hangingPiece", "middlegame", "short"]
    },
    {
        "fen": "6k1/1p3pp1/1p5p/2r1p3/2n5/r3PN2/2RnNPPP/2R3K1 b - - 1 32",
        "moves": ["f7f6", "f3d2", "c4d2", "c2d2", "c5c1", "e2c1"],
        "rating": 1827,
        "themes": ["advantage", "long", "middlegame"]
    },
    {
        "fen": "1rb2rk1/q5P1/4p2p/3p3p/3P1P2/2P5/2QK3P/3R2R1 b - - 0 29",
        "moves": ["f8f7", "c2h7", "g8h7", "g7g8q"],
        "rating": 1049,
        "themes": ["advancedPawn", "attraction", "mate", "mateIn2", "middlegame", "promotion", "short"]
    },
    {
        "fen": "6nr/pp3p1p/k1p5/8/1QN5/2P1P3/4KPqP/8 b - - 5 26",
        "moves": ["b7b5", "b4a5", "a6b7", "c4d6", "b7b8", "a5d8"],
        "rating": 1257,
        "themes": ["endgame", "long", "mate", "mateIn3"]
    },
    {
        "fen": "r3k2r/pb1p1ppp/1b4q1/1Q2P3/8/2NP1Pn1/PP4PP/R1B2R1K w kq - 1 17",
        "moves": ["h2g3", "g6h5"],
        "rating": 1302,
        "themes": ["mate", "mateIn1", "middlegame", "oneMove"]
    },
    {
        "fen": "8/4R1k1/p5pp/3B4/5q2/8/5P1P/6K1 b - - 5 40",
        "moves": ["g7f6", "e7f7", "f6e5", "f7f4"],
        "rating": 1127,
        "themes": ["advantage", "endgame", "master", "masterVsMaster", "short", "skewer", "superGM"]
    },
    {
        "fen": "r3kb1r/pppqpn1p/5p2/3p1bpQ/2PP4/4P1B1/PP3PPP/RN2KB1R w KQkq - 1 11",
        "moves": ["b1c3", "f5g4", "h5g4", "d7g4"],
        "rating": 1678,
        "themes": ["advantage", "opening", "short", "trappedPiece"]
    },
    {
        "fen": "r5k1/pp4pp/4p1q1/4p3/3n4/P5P1/1PP2Q1P/2KR1R2 w - - 4 24",
        "moves": ["f2e3", "g6c2"],
        "rating": 927,
        "themes": ["endgame", "mate", "mateIn1", "oneMove", "queensideAttack"]
    },
    {
        "fen": "r1b2rk1/p4ppp/2p5/6q1/2p3P1/3P1Q1P/PPP5/1K2RR2 b - - 0 17",
        "moves": ["c4d3", "f3f7", "f8f7", "e1e8", "f7f8", "f1f8"],
        "rating": 1369,
        "themes": ["kingsideAttack", "long", "mate", "mateIn3", "middlegame", "sacrifice"]
    },
    {
        "fen": "r7/7R/P3k3/4p2p/3b2p1/3K4/8/5R2 b - - 7 55",
        "moves": ["a8a6", "h7h6", "e6d5", "h6a6"],
        "rating": 969,
        "themes": ["crushing", "endgame", "short", "skewer"]
    },
    {
        "fen": "8/n7/P7/3k4/PK6/7P/5PP1/8 w - - 0 53",
        "moves": ["b4a5", "d5c5", "f2f3", "a7c6"],
        "rating": 1660,
        "themes": ["endgame", "knightEndgame", "mate", "mateIn2", "short"]
    },
    {
        "fen": "5r1k/2p3Rp/3p4/p2Pn3/1p2B3/1P6/PKP2r1P/6R1 b - - 1 28",
        "moves": ["f2e2", "g7h7"],
        "rating": 1096,
        "themes": ["endgame", "master", "mate", "mateIn1", "oneMove"]
    },
    {
        "fen": "8/2p1b3/q1Pp2k1/3Pp3/4Pr2/1Q3PK1/3N2P1/7R w - - 1 47",
        "moves": ["h1e1", "e7h4", "g3h2", "h4e1"],
        "rating": 1228,
        "themes": ["crushing", "endgame", "short", "skewer"]
    },
    {
        "fen": "3r1rk1/1Q3ppp/1q2pb2/8/1P1N4/4P1P1/3B1PBP/R5K1 b - - 0 23",
        "moves": ["b6b7", "g2b7", "f6d4", "e3d4"],
        "rating": 1059,
        "themes": ["advantage", "middlegame", "short"]
    },
    {
        "fen": "1k5r/n2r2pp/5p2/ppN5/5P2/8/2R3PP/1R4K1 b - - 3 28",
        "moves": ["d7c7", "c5a6", "b8b7", "a6c7"],
        "rating": 1359,
        "themes": ["crushing", "endgame", "fork", "short"]
    },
    {
        "fen": "6k1/pp3rpp/4Nb2/4p3/1B1r4/6PK/PP5P/2R5 b - - 0 28",
        "moves": ["d4b4", "c1c8", "f6d8", "c8d8", "f7f8", "d8f8"],
        "rating": 886,
        "themes": ["endgame", "long", "mate", "mateIn3"]
    },
    {
        "fen": "6rk/1pp1R1p1/6Bp/2b4P/8/pP3PK1/P1P5/8 w - - 5 32",
        "moves": ["e7c7", "c5d6", "f3f4", "d6c7"],
        "rating": 871,
        "themes": ["crushing", "endgame", "fork", "short"]
    },
    {
        "fen": "2r3k1/1p1q1ppp/4p3/Q7/3P4/P1B5/1Pr2PPP/R5K1 b - - 0 22",
        "moves": ["d7d4", "c3d4", "c2c1", "a5e1"],
        "rating": 1828,
        "themes": ["advantage", "endgame", "hangingPiece", "short"]
    },
    {
        "fen": "8/7p/4K3/6p1/2k3P1/8/5P2/8 b - - 0 43",
        "moves": ["c4d4", "e6f5", "h7h6", "f5g6", "d4e4", "g6h6"],
        "rating": 1478,
        "themes": ["crushing", "endgame", "long", "master", "pawnEndgame"]
    },
    {
        "fen": "8/3r1ppp/4p3/k3P3/pR2R2P/2P5/2Kr1PP1/8 w - - 4 31",
        "moves": ["c2c1", "d2d1", "c1b2", "d7d2", "b2a3", "d1a1"],
        "rating": 930,
        "themes": ["endgame", "exposedKing", "long", "mate", "mateIn3", "rookEndgame"]
    },
    {
        "fen": "2k3r1/pp5p/4p3/2p2p2/2P5/P4P1q/1PQ1RR1b/7K w - - 0 32",
        "moves": ["f2h2", "h3f1"],
        "rating": 1048,
        "themes": ["endgame", "master", "mate", "mateIn1", "oneMove"]
    },
    {
        "fen": "r1bq3r/ppppnkpp/2n5/b5N1/4P3/B1P5/P4PPP/RN1QK2R b KQ - 1 9",
        "moves": ["f7f8", "d1f3", "f8e8", "f3f7"],
        "rating": 1249,
        "themes": ["mate", "mateIn2", "opening", "short"]
    },
    {
        "fen": "r1bk4/pppp3p/2n5/2b1prN1/8/1B6/PPPP2PP/RNB2RK1 w - - 1 14",
        "moves": ["g1h1", "f5f1"],
        "rating": 600,
        "themes": ["backRankMate", "hangingPiece", "mate", "mateIn1", "middlegame", "oneMove"]
    },
    {
        "fen": "8/8/1pr1p1kp/pbPp2pN/3Pp1P1/1P2K3/P6P/2R5 b - - 0 29",
        "moves": ["e6e5", "c5b6", "c6c1", "b6b7", "c1e1", "e3d2"],
        "rating": 2103,
        "themes": ["advancedPawn", "crushing", "endgame", "long", "master", "sacrifice"]
    },
    {
        "fen": "5k1r/p3Rpbp/3N2p1/4nbB1/2P5/3rP3/q4PPP/3Q1RK1 b - - 2 16",
        "moves": ["f7f6", "e7e8"],
        "rating": 910,
        "themes": ["middlegame"]
    },
    {
        "fen": "8/5R2/P7/2p1r3/2Pp2k1/3K4/5p2/8 b - - 1 54",
        "moves": ["e5f5", "f7f5", "g4f5", "d3e2", "f2f1q", "e2f1"],
        "rating": 1646,
        "themes": ["crushing", "endgame", "long", "rookEndgame"]
    },
    {
        "fen": "r2q1rk1/p3b1pp/2p5/4ppB1/4p1nP/2N5/PPP1QPP1/3R1RK1 b - - 8 15",
        "moves": ["d8c7", "e2c4", "g8h8", "c3d5", "c6d5", "c4c7"],
        "rating": 1919,
        "themes": ["crushing", "long", "middlegame"]
    },
    {
        "fen": "1k1r1r2/pp4p1/6q1/2Qp4/5bP1/2P4p/PPN3NP/R4R1K w - - 0 30",
        "moves": ["g2f4", "g6e4", "h1g1", "f8f4"],
        "rating": 1375,
        "themes": ["crushing", "fork", "intermezzo", "middlegame", "short"]
    },
    {
        "fen": "r1bqkb1r/ppp1n1p1/7p/3Pp1N1/2P5/8/PP3PPP/RNBQK2R w KQkq - 0 11",
        "moves": ["d1h5", "g7g6", "h5e2", "h6g5"],
        "rating": 1476,
        "themes": ["defensiveMove", "equality", "opening", "short"]
    },
    {
        "fen": "8/8/RP4p1/1r1N1pkp/P1n1p3/6P1/6P1/4K3 b - - 0 49",
        "moves": ["b5d5", "b6b7", "d5d8", "a6a8"],
        "rating": 1069,
        "themes": ["endgame"]
    },
    {
        "fen": "1r3rk1/pP2qppp/1b3n2/1Q2p3/4P3/2NP1bP1/PP2NP1P/R1B2RK1 w - - 1 15",
        "moves": ["c1g5", "e7e6", "e2f4", "e5f4"],
        "rating": 2122,
        "themes": ["crushing", "middlegame", "short"]
    },
    {
        "fen": "3r1b1r/2pn4/1p1p3p/2kP2qn/Q3Pp2/4Bp2/1P4PP/4R1K1 b - - 3 26",
        "moves": ["f4e3", "e1c1"],
        "rating": 1397,
        "themes": ["mate", "mateIn1", "middlegame", "oneMove"]
    },
    {
        "fen": "r6r/pQ2nkpp/4b3/2p1q3/4p3/2N5/PP1B1PPP/R4RK1 w - - 1 15",
        "moves": ["c3e4", "e6d5", "e4g5", "e5g5", "d2g5", "d5b7"],
        "rating": 1681,
        "themes": ["advantage", "long", "middlegame"]
    },
    {
        "fen": "8/3k4/1pp3p1/4Pp1p/2PK1P1P/pP6/P7/8 b - - 1 35",
        "moves": ["d7e6", "b3b4", "e6e7", "b4b5", "c6b5", "c4b5"],
        "rating": 2179,
        "themes": ["crushing", "endgame", "long", "pawnEndgame", "quietMove", "zugzwang"]
    },
    {
        "fen": "rnbqkb1r/pp3p1p/6pP/P1ppp3/6n1/3P1P2/1PP1P1P1/RNBQKBNR b KQkq - 0 7",
        "moves": ["g4h6", "c1h6", "f8h6", "h1h6"],
        "rating": 1313,
        "themes": ["advantage", "opening", "short"]
    },
    {
        "fen": "8/4k2p/Q1p1p3/p2pP1r1/q7/P6P/1P3PK1/2R2R2 w - - 1 28",
        "moves": ["g2f3", "a4e4"],
        "rating": 1356,
        "themes": ["endgame", "mate", "mateIn1", "oneMove"]
    },
    {
        "fen": "2kr1b1R/p5p1/8/3P1p2/8/4B3/PPPK1P2/8 w - - 1 25",
        "moves": ["c2c4", "f8b4", "d2d3", "d8h8"],
        "rating": 852,
        "themes": ["crushing", "discoveredAttack", "endgame", "short"]
    },
    {
        "fen": "r1b5/p4pkp/3p2p1/2pPr3/2P5/1P1B4/R4PPP/R5K1 w - - 0 24",
        "moves": ["a2a7", "a8a7", "a1a7", "e5e1", "d3f1", "c8f5"],
        "rating": 1556,
        "themes": ["advantage", "defensiveMove", "endgame", "long"]
    },
    {
        "fen": "r4q1k/2bn2p1/2p3pp/1pP5/1P1B2P1/1Q1P1r1P/5PB1/4RRK1 w - - 0 27",
        "moves": ["g2f3", "f8f4", "d4g7", "h8h7", "e1e5", "d7e5", "g7e5", "c7e5", "f1e1", "f4f3"],
        "rating": 2366,
        "themes": ["crushing", "fork", "master", "middlegame", "veryLong"]
    }
]

class PuzzleSystem:
    def __init__(self):
        self.current_puzzle = None
        self.puzzle_history = []
        self.current_rating = 1500
        self.current_move_index = 0
        self.puzzles = CHESS_PUZZLES
        self.board = None
        self.congratulation_messages = [
            "Brilliant solve! You're getting stronger!",
            "Excellent tactics! Keep it up!",
            "Perfect execution! You saw the key moves!",
            "Outstanding calculation! You're on fire!",
            "Beautiful solve! Your tactical eye is sharp!",
            "Masterful play! You found the winning idea!",
            "Impressive solving! You're making progress!",
            "Well done! Your tactical skills are improving!"
        ]
        self.current_congratulation = None
        self.hint_square = None  # Store the square to highlight
        
    def load_puzzle(self, rating_range=None):
        """Load a puzzle within the specified rating range"""
        if rating_range:
            min_rating, max_rating = rating_range
            suitable_puzzles = [p for p in self.puzzles 
                              if min_rating <= p['rating'] <= max_rating]
        else:
            # If no rating range specified, find puzzles near player's rating
            suitable_puzzles = [p for p in self.puzzles 
                              if abs(p['rating'] - self.current_rating) <= 200]
        
        if suitable_puzzles:
            self.current_puzzle = random.choice(suitable_puzzles)
            self.current_move_index = 0
            self.board = chess.Board(self.current_puzzle['fen'])
            return self.current_puzzle
        return None
    
    def make_first_move(self):
        """Make the first move of the puzzle (computer's move)"""
        if self.current_puzzle and self.current_move_index == 0:
            first_move = chess.Move.from_uci(self.current_puzzle['moves'][0])
            self.board.push(first_move)
            self.current_move_index = 1
            return first_move
        return None
    
    def verify_move(self, move):
        """Verify if the move matches the puzzle solution"""
        if not self.current_puzzle:
            return False
            
        expected_move = self.current_puzzle['moves'][self.current_move_index]
        if move.uci() == expected_move:
            self.current_move_index += 1
            return True
        return False
    
    def get_computer_response(self):
        """Get and make the computer's response move"""
        if (self.current_puzzle and self.current_move_index < len(self.current_puzzle['moves'])):
            computer_move = chess.Move.from_uci(self.current_puzzle['moves'][self.current_move_index])
            self.board.push(computer_move)
            self.current_move_index += 1
            return computer_move
        return None
    
    def complete_puzzle(self):
        """Handle puzzle completion - show one random congratulation message"""
        if not self.current_congratulation:  # Only set message if not already set
            self.current_congratulation = random.choice(self.congratulation_messages)
        return True

    def is_puzzle_complete(self):
        """Check if all moves in the puzzle have been played"""
        return (self.current_puzzle and 
                self.current_move_index >= len(self.current_puzzle['moves']))

    def get_completion_message(self):
        """Get the current congratulatory message"""
        return self.current_congratulation

    def clear_completion(self):
        """Clear the completion state"""
        self.current_congratulation = None

    def update_rating(self, success):
        """Update player rating based on puzzle success"""
        k_factor = 32
        expected_score = 1 / (1 + 10 ** ((self.current_puzzle['rating'] - self.current_rating) / 400))
        actual_score = 1 if success else 0
        self.current_rating += k_factor * (actual_score - expected_score)
    
    def get_similar_rating_puzzles(self):
        """Get puzzles with similar ratings"""
        return []
    
    def track_progress(self, puzzle_id, success):
        """Track puzzle completion and success"""
        self.puzzle_history.append({
            'puzzle_id': puzzle_id,
            'success': success,
            'timestamp': None  # Would normally use datetime.now()
        })

    def get_current_board(self):
        """Get the current board state"""
        return self.board if self.board else chess.Board()

    def load_random_puzzle(self):
        """Load a completely random puzzle from any rating range"""
        self.current_puzzle = random.choice(CHESS_PUZZLES)
        self.current_move_index = 0
        self.board = chess.Board(self.current_puzzle['fen'])

    def get_hint(self):
        """Get the square of the piece that needs to be moved"""
        if self.current_puzzle and self.current_move_index < len(self.current_puzzle['moves']):
            move = chess.Move.from_uci(self.current_puzzle['moves'][self.current_move_index])
            return move.from_square
        return None

    def clear_hint(self):
        """Clear the current hint"""
        self.hint_square = None
