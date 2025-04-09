#  GPT-4 Vision Autonomous Chess

Welcome to **GPT-4 Vision Chess** – a Python-based chess engine where GPT-4o (OpenAI's multimodal model) plays against a human or itself using visual recognition and reasoning from board screenshots.

This project uses **Pygame** to render the GUI and **GPT-4o Vision** to analyze the current chessboard and suggest the best move for the current player.

---

##  Features

- ✔️ **Human vs AI** chess game
- 🤖 **GPT-4 Vision AI** opponent (reads board screenshots)
- 🔁 GPT auto-reprompts if move is invalid/illegal
- 📸 AI understands and plays based on visual input only
- 🏁 Board rendered with labels and chess piece images
- ⚙️ Easily switch to full **AI vs AI autonomous mode**

---

---

##  How It Works

1. The chessboard is rendered using **Pygame**.
2. After each move, the board is saved as a screenshot (`board.png`).
3. The screenshot is sent to **GPT-4o** with a prompt:  
   _"What is the best move for White/Black? Respond in UCI format (e.g., e2e4).”_
4. The model replies with a move based on the image.
5. The move is validated and played.

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/gpt-vision-chess.git
cd gpt-vision-chess
