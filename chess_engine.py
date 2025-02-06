import chess
import random
from typing import Tuple, List, Dict
import time

class ChessEngine:
    def __init__(self, depth: int):
        self.depth = depth
        self.nodes_searched = 0
        self.transposition_table = {}
        self.history_table: Dict[Tuple[int, int], int] = {}  # (from_square, to_square) -> score
        
        # Material values (standard + positional bonus)
        self.piece_values = {
            chess.PAWN: 100,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 20000
        }
        
        # Initialize piece-square tables
        self.pst = self._initialize_piece_square_tables()
        
        # Difficulty-specific parameters
        if depth == 2:  # Easy
            self.use_quiescence = False
            self.use_transposition = False
            self.use_move_ordering = True
            self.max_quiescence_depth = 0
            self.use_history = False
        elif depth == 3:  # Medium
            self.use_quiescence = True
            self.use_transposition = True
            self.use_move_ordering = True
            self.max_quiescence_depth = 4
            self.use_history = True
        else:  # Hard
            self.use_quiescence = True
            self.use_transposition = True
            self.use_move_ordering = True
            self.max_quiescence_depth = 6
            self.use_history = True

    def _initialize_piece_square_tables(self):
        # Advanced piece-square tables for better positional play
        pst = {
            chess.PAWN: [
                0,  0,  0,  0,  0,  0,  0,  0,
                50, 50, 50, 50, 50, 50, 50, 50,
                10, 10, 20, 30, 30, 20, 10, 10,
                5,  5, 10, 25, 25, 10,  5,  5,
                0,  0,  0, 20, 20,  0,  0,  0,
                5, -5,-10,  0,  0,-10, -5,  5,
                5, 10, 10,-20,-20, 10, 10,  5,
                0,  0,  0,  0,  0,  0,  0,  0
            ],
            chess.KNIGHT: [
                -50,-40,-30,-30,-30,-30,-40,-50,
                -40,-20,  0,  0,  0,  0,-20,-40,
                -30,  0, 10, 15, 15, 10,  0,-30,
                -30,  5, 15, 20, 20, 15,  5,-30,
                -30,  0, 15, 20, 20, 15,  0,-30,
                -30,  5, 10, 15, 15, 10,  5,-30,
                -40,-20,  0,  5,  5,  0,-20,-40,
                -50,-40,-30,-30,-30,-30,-40,-50
            ],
            chess.BISHOP: [
                -20,-10,-10,-10,-10,-10,-10,-20,
                -10,  0,  0,  0,  0,  0,  0,-10,
                -10,  0,  5, 10, 10,  5,  0,-10,
                -10,  5,  5, 10, 10,  5,  5,-10,
                -10,  0, 10, 10, 10, 10,  0,-10,
                -10, 10, 10, 10, 10, 10, 10,-10,
                -10,  5,  0,  0,  0,  0,  5,-10,
                -20,-10,-10,-10,-10,-10,-10,-20
            ],
            chess.ROOK: [
                0,  0,  0,  0,  0,  0,  0,  0,
                5, 10, 10, 10, 10, 10, 10,  5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                0,  0,  0,  5,  5,  0,  0,  0
            ],
            chess.QUEEN: [
                -20,-10,-10, -5, -5,-10,-10,-20,
                -10,  0,  0,  0,  0,  0,  0,-10,
                -10,  0,  5,  5,  5,  5,  0,-10,
                -5,  0,  5,  5,  5,  5,  0, -5,
                0,  0,  5,  5,  5,  5,  0, -5,
                -10,  5,  5,  5,  5,  5,  0,-10,
                -10,  0,  5,  0,  0,  0,  0,-10,
                -20,-10,-10, -5, -5,-10,-10,-20
            ],
            chess.KING: [
                -30,-40,-40,-50,-50,-40,-40,-30,
                -30,-40,-40,-50,-50,-40,-40,-30,
                -30,-40,-40,-50,-50,-40,-40,-30,
                -30,-40,-40,-50,-50,-40,-40,-30,
                -20,-30,-30,-40,-40,-30,-30,-20,
                -10,-20,-20,-20,-20,-20,-20,-10,
                20, 20,  0,  0,  0,  0, 20, 20,
                20, 30, 10,  0,  0, 10, 30, 20
            ]
        }
        return pst

    def evaluate_position(self, board: chess.Board) -> float:
        """Evaluate the current position"""
        if board.is_checkmate():
            return -10000 if board.turn else 10000
        
        # Basic piece values
        piece_values = {
            chess.PAWN: 100,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 20000
        }
        
        # Endgame piece values (pawns and king become more valuable)
        endgame_piece_values = {
            chess.PAWN: 150,  # Pawns more valuable in endgame
            chess.KNIGHT: 300,
            chess.BISHOP: 300,
            chess.ROOK: 550,
            chess.QUEEN: 900,
            chess.KING: 20000
        }
        
        # Determine if we're in endgame (no queens or both sides have <= 13 points in material)
        total_material = sum(len(board.pieces(piece_type, True)) * piece_values[piece_type] +
                            len(board.pieces(piece_type, False)) * piece_values[piece_type]
                            for piece_type in [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT])
        is_endgame = total_material <= 2600  # Roughly equivalent to each side having a queen or less
        
        current_values = endgame_piece_values if is_endgame else piece_values
        
        score = 0
        
        # Material and position evaluation
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is None:
                continue
            
            value = current_values[piece.piece_type]
            
            # Add position bonus
            rank = chess.square_rank(square)
            file = chess.square_file(square)
            
            if is_endgame:
                if piece.piece_type == chess.KING:
                    # King should be more active in endgame
                    center_distance = abs(3.5 - file) + abs(3.5 - rank)
                    value -= center_distance * 10
                
                if piece.piece_type == chess.PAWN:
                    # Passed and advanced pawns are very valuable in endgame
                    value += rank * 20 if piece.color else (7 - rank) * 20
            
            score += value if piece.color else -value
        
        # Additional endgame considerations
        if is_endgame:
            # Encourage moving king towards enemy king in endgame
            our_king = board.king(board.turn)
            their_king = board.king(not board.turn)
            if our_king and their_king:  # Make sure both kings exist
                king_distance = abs(chess.square_file(our_king) - chess.square_file(their_king)) + \
                              abs(chess.square_rank(our_king) - chess.square_rank(their_king))
                score += -king_distance * 10 if board.turn else king_distance * 10
        
        return score if board.turn else -score

    def _evaluate_piece_safety(self, piece: chess.Piece, attackers: int, defenders: int, value: int) -> int:
        if attackers == 0:
            return defenders * 10  # Bonus for defended pieces
        if defenders == 0:
            return -value // 2  # Heavy penalty for undefended pieces under attack
        if attackers > defenders:
            return -value // 3  # Penalty for pieces under attack with insufficient defense
        return 0

    def _evaluate_pawn_structure(self, board: chess.Board) -> int:
        score = 0
        
        # Evaluate pawn structure for both colors
        for color in [True, False]:
            pawns = board.pieces(chess.PAWN, color)
            
            # Doubled pawns penalty
            files = [chess.square_file(sq) for sq in pawns]
            doubled_pawns = len(files) - len(set(files))
            score += (-20 if color else 20) * doubled_pawns
            
            # Isolated pawns penalty
            for pawn in pawns:
                file = chess.square_file(pawn)
                isolated = True
                for adj_file in [file - 1, file + 1]:
                    if 0 <= adj_file <= 7:
                        for rank in range(8):
                            sq = chess.square(adj_file, rank)
                            if board.piece_at(sq) == chess.Piece(chess.PAWN, color):
                                isolated = False
                                break
                if isolated:
                    score += -15 if color else 15
        
        return score

    def _evaluate_king_safety(self, board: chess.Board) -> int:
        score = 0
        
        for color in [True, False]:
            king_square = board.king(color)
            if not king_square:
                continue
                
            # King attackers
            attackers = len(list(board.attackers(not color, king_square)))
            score += (-50 if color else 50) * attackers
            
            # Pawn shield
            king_file = chess.square_file(king_square)
            king_rank = chess.square_rank(king_square)
            
            shield_squares = []
            if color:  # White
                for f in range(max(0, king_file - 1), min(8, king_file + 2)):
                    shield_squares.extend([
                        chess.square(f, r) for r in range(max(0, king_rank - 1), min(8, king_rank + 2))
                    ])
            else:  # Black
                for f in range(max(0, king_file - 1), min(8, king_file + 2)):
                    shield_squares.extend([
                        chess.square(f, r) for r in range(max(0, king_rank - 1), min(8, king_rank + 2))
                    ])
            
            # Count friendly pieces near king
            defenders = sum(1 for sq in shield_squares if board.piece_at(sq) 
                          and board.piece_at(sq).color == color)
            score += (20 if color else -20) * defenders
        
        return score

    def _evaluate_piece_coordination(self, board: chess.Board) -> int:
        score = 0
        
        # Bonus for bishop pair
        if len(list(board.pieces(chess.BISHOP, True))) >= 2:
            score += 50
        if len(list(board.pieces(chess.BISHOP, False))) >= 2:
            score -= 50
        
        # Bonus for connected rooks
        for color in [True, False]:
            rooks = list(board.pieces(chess.ROOK, color))
            if len(rooks) >= 2:
                rook_files = [chess.square_file(sq) for sq in rooks]
                if any(abs(rook_files[i] - rook_files[i+1]) == 0 
                       for i in range(len(rook_files)-1)):
                    score += 30 if color else -30
        
        return score

    def _order_moves(self, board: chess.Board, moves: List[chess.Move]) -> List[chess.Move]:
        if not self.use_move_ordering:
            return moves
            
        move_scores = []
        for move in moves:
            score = 0
            
            # MVV-LVA (Most Valuable Victim - Least Valuable Attacker)
            if board.is_capture(move):
                victim = board.piece_at(move.to_square)
                attacker = board.piece_at(move.from_square)
                if victim and attacker:
                    score = 10 * self.piece_values[victim.piece_type] - self.piece_values[attacker.piece_type]
            
            # Promotion score
            if move.promotion:
                score += self.piece_values[move.promotion]
            
            # History heuristic
            if self.use_history:
                score += self.history_table.get((move.from_square, move.to_square), 0)
            
            # Check extension
            board.push(move)
            if board.is_check():
                score += 100
            board.pop()
            
            move_scores.append((move, score))
        
        return [move for move, _ in sorted(move_scores, key=lambda x: x[1], reverse=True)]

    def quiescence_search(self, board: chess.Board, alpha: float, beta: float, depth: int = -4) -> float:
        if not self.use_quiescence:
            return self.evaluate_position(board)
            
        stand_pat = self.evaluate_position(board)
        
        if depth == 0:
            return stand_pat
            
        if stand_pat >= beta:
            return beta
            
        alpha = max(alpha, stand_pat)
        
        for move in self._order_moves(board, list(board.legal_moves)):
            if board.is_capture(move):
                board.push(move)
                score = -self.quiescence_search(board, -beta, -alpha, depth + 1)
                board.pop()
                
                if score >= beta:
                    return beta
                alpha = max(alpha, score)
        
        return alpha

    def alpha_beta(self, board: chess.Board, depth: int, alpha: float, beta: float, maximizing: bool) -> Tuple[float, chess.Move]:
        self.nodes_searched += 1
        
        # Transposition table lookup
        board_hash = board.fen() if self.use_transposition else None
        if self.use_transposition and depth > 0 and board_hash in self.transposition_table:
            return self.transposition_table[board_hash]
        
        if depth == 0 or board.is_game_over():
            if self.use_quiescence:
                return self.quiescence_search(board, alpha, beta), None
            return self.evaluate_position(board), None

        best_move = None
        moves = self._order_moves(board, list(board.legal_moves))
        
        if maximizing:
            max_eval = float('-inf')
            for move in moves:
                board.push(move)
                eval, _ = self.alpha_beta(board, depth - 1, alpha, beta, False)
                board.pop()
                
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            
            if self.use_transposition:
                self.transposition_table[board_hash] = (max_eval, best_move)
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in moves:
                board.push(move)
                eval, _ = self.alpha_beta(board, depth - 1, alpha, beta, True)
                board.pop()
                
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            
            if self.use_transposition:
                self.transposition_table[board_hash] = (min_eval, best_move)
            return min_eval, best_move

    def get_best_move(self, board: chess.Board) -> chess.Move:
        self.nodes_searched = 0
        start_time = time.time()
        
        try:
            # Iterative deepening
            best_move = None
            for current_depth in range(1, self.depth + 1):
                _, move = self.alpha_beta(board, current_depth, float('-inf'), float('inf'), True)
                if move:
                    best_move = move
                
                # Time check
                if time.time() - start_time > 5:  # 5 second limit
                    break
            
            # Auto-promote to queen if it's a pawn move to the last rank
            if best_move and board.piece_at(best_move.from_square).piece_type == chess.PAWN:
                if chess.square_rank(best_move.to_square) in [0, 7]:
                    best_move = chess.Move(best_move.from_square, best_move.to_square, chess.QUEEN)
            
            return best_move
            
        except Exception as e:
            print(f"Error in search: {e}")
            return list(board.legal_moves)[0] 