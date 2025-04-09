import pygame
import chess
import chess.svg
import io
import openai
from PIL import Image, ImageGrab
import time

# --- CONFIG ---
openai.api_key = "your-api-key"

# --- Initialize Pygame ---
pygame.init()
WIDTH, HEIGHT = 480, 480
SQUARE_SIZE = WIDTH // 8
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Chess")

import os
c=8
r=8

PIECE_FOLDER = "pieces"
PIECES = {}
for piece in ["P", "R", "N", "B", "Q", "K"]:
    for color in ["w", "b"]:
        name = f"{color}{piece}"
        path = os.path.join("pieces", f"{name}.png")
        PIECES[name] = pygame.transform.scale(pygame.image.load(path), (SQUARE_SIZE, SQUARE_SIZE))
def draw_board(board):
    colors = [pygame.Color("white"), pygame.Color("gray")]
    font = pygame.font.SysFont(None, 24)  # You can increase/decrease the size as needed

    for r in range(8):
        for c in range(8):
            color = colors[(r + c) % 2]
            rect = pygame.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, color, rect)

            # Draw piece
            square = chess.square(c, 7 - r)
            piece = board.piece_at(square)
            if piece:
                symbol = piece.symbol()
                color = 'w' if symbol.isupper() else 'b'
                key = f"{color}{symbol.upper()}"
                screen.blit(PIECES[key], rect)

            # Draw file (a-h) at the bottom
            if r == 7:
                label = font.render(chr(ord('a') + c), True, pygame.Color('black'))
                screen.blit(label, (c * SQUARE_SIZE + 2, 8 * SQUARE_SIZE - 18))

            # Draw rank (1-8) at the left
            if c == 0:
                label = font.render(str(8 - r), True, pygame.Color('black'))
                screen.blit(label, (2, r * SQUARE_SIZE + 2))

import base64

def get_best_move_from_gpt(image_path,board):
    with open(image_path, "rb") as img:
        base64_image = base64.b64encode(img.read()).decode('utf-8')

    response = openai.chat.completions.create(
        model="gpt-4o",  # or "gpt-4o" if that supports vision too
        messages=[
            {"role": "user", "content": [
                {"type": "text", "text": f"What is the next optimal move for {'White' if board.turn else 'Black'} to play? Respond ONLY with legal move in UCI format (e.g., e2e4)."},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
            ]}
        ],
        max_tokens=20,
    )
    return response.choices[0].message.content.strip()

def get_legal_gpt_move(image_path, board):
    max_attempts = 5
    attempt = 0

    while attempt < max_attempts:
        uci_move = get_best_move_from_gpt(image_path,board)
        print(f"GPT attempt {attempt+1}: {uci_move}")

        try:
            move = chess.Move.from_uci(uci_move)
            if move in board.legal_moves:
                return move
        except:
            pass  # Ignore bad UCI strings

        # Clarify and retry
        print("Invalid or illegal move. Reprompting...")
        attempt += 1

    raise ValueError("GPT failed to return a valid move after multiple attempts.")

# --- Autonomous Game Loop ---
board = chess.Board()
draw_board(board)
pygame.display.flip()
pygame.time.wait(500)
time.sleep(1)


while not board.is_game_over():
    # Draw and update the board
    draw_board(board)
    pygame.display.flip()
    pygame.time.wait(500)  # Wait for rendering

    # Save screenshot of the current board
    pygame.image.save(screen, "board.png")

    try:
        uci_move = get_best_move_from_gpt("board.png", board)
        print(f"{'White' if board.turn else 'Black'} GPT move: {uci_move}")
        uci_move = uci_move.replace("+", "").replace("#", "").replace("x", "").strip()
        move = chess.Move.from_uci(uci_move)

        if move in board.legal_moves:
            board.push(move)
            draw_board(board)
            pygame.display.flip()
        else:
            print("GPT move was invalid. Retrying...")
            move = get_legal_gpt_move("board.png", board)
            board.push(move)
            draw_board(board)
            pygame.display.flip()

    except Exception as e:
        print(f"GPT Error: {e}")
        break


# Game over
draw_board(board)
pygame.display.flip()
print("Game Over:", board.result())
pygame.time.wait(5000)
pygame.quit()
