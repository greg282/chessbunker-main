import chess

board = chess.Board()

move = "e2e4"

print(board.is_game_over())
print(board.can_claim_draw())

print("white" if board.turn == chess.WHITE else "black")


if chess.Move.from_uci(move) in board.legal_moves:
    print("Legal move")
    board.push(chess.Move.from_uci(move))


print("white" if board.turn == chess.WHITE else "black")


print(board)
