# Snail Chess Engine
 This is my attempt at making a chess engine, the repository contains **Snail Engine** which is a basic chess engine developed using NegaMax Alpha Beta Pruning algorithm that you can play against in `PyGame`. The repository also contains **Turtle Engine** which is a research work-in-progress notebook of developing an *Alpha-Zero-Like* Neural Network based engine. Both engines are implemented in Python.

<br>

## Files

**ChessEngine.py:** This file contains the logic for the chess game. It includes classes and functions that handle the game board, move generation, validation, and various utility functions.

**SnailEngine.py:** The SnailEngine file implements the AI for the chess engine. It uses the NegaMax algorithm with Alpha Beta Pruning to search for the best move at each turn. The AI evaluates positions using a combination of heuristics and position scoring.

**ChessMain.py:** This file brings everything together by rendering a playable chess game in the Pygame library. It provides a graphical user interface where users can interact with the chess engine, make moves, and play against the AI.

<br>

## How to Run

1. Clone the repository
2. Install the requirements using `pip install -r requirements.txt`
3. Run the ChessMain.py file using `python ChessMain.py`
4. Play against the AI!

<br>

## Controls
 - Press `r` to reset the game
 - Press `z` to undo a move
 - Press `e` to exit the game

<br>

# Algorithms

During the development of this project, I implemented multiple algorithms to evaluate the chess positions. The algorithms are listed below in the order of their implementation.

### Material Count
This algorithm simply counts the number of pieces on the board and assigns a score to each piece. The score is calculated by multiplying the number of pieces by a constant value. The constant value is positive for white pieces and negative for black pieces. This algorithm is very simple and does not take into account the position of the pieces on the board.

### Min Max Algorithm
This algorithm uses the Min Max algorithm to evaluate the positions. It assigns a score to each position by recursively searching the game tree. The algorithm assumes that the opponent will always make the best move and assigns a score to each position based on the best move the opponent can make. The algorithm then chooses the move that leads to the best position for the player. This algorithm is very slow and does not take into account the position of the pieces on the board.

### NegaMax Algorithm
This algorithm is similar to the Min Max algorithm but it uses the NegaMax algorithm to evaluate the positions. The NegaMax algorithm is a variation of the Min Max algorithm that simplifies the implementation. The NegaMax algorithm assumes that the opponent will always make the best move and assigns a score to each position based on the best move the opponent can make. The algorithm then chooses the move that leads to the best position for the player. This algorithm is faster than the Min Max algorithm but it does not take into account the position of the pieces on the board.

### NegaMax with Alpha Beta Pruning
This algorithm is similar to the NegaMax algorithm but it uses Alpha Beta Pruning to speed up the search. Alpha Beta Pruning is an optimization technique that reduces the number of nodes that are evaluated by the NegaMax algorithm. This algorithm is faster than the NegaMax algorithm but it does not take into account the position of the pieces on the board.

### NegaMax with Alpha Beta Pruning and Heuristics
This algorithm is similar to the NegaMax with Alpha Beta Pruning algorithm but it uses heuristics to evaluate the positions. The heuristics are used to assign a score to each position based on the position of the pieces on the board. This algorithm is faster than the NegaMax with Alpha Beta Pruning algorithm and it takes into account the position of the pieces on the board.

### Reinforcement Learning with Neural Networks
This algorithm uses a Neural Network to evaluate the positions. The Neural Network is trained using Reinforcement Learning. The Neural Network is trained by playing against itself and learning from the results. This algorithm is faster than the NegaMax with Alpha Beta Pruning and Heuristics algorithm and it takes into account the position of the pieces on the board and is the most accurate algorithm.

## Future Improvements

 - Draw by repetition, 3 fold repetition, 50 move rule, and insufficient material
 - Implement Neural Network Engine in PyGame
 - Speed up the search by using a transposition table and iterative deepening
 - Improve code efficiency by using bitboards and NumPy arrays instead of Python lists

# Sources

### Main Inspiration

* ["Chess engine in Python"](https://www.youtube.com/watch?v=EnYui0e73Rs&ab_channel=EddieSharick)
* [Eddie's YouTube channel](https://www.youtube.com/channel/UCaEohRz5bPHywGBwmR18Qww)

### Wikipedia articles & Library documentation

* [1]"Deep reinforcement learning," Wikipedia. Jan. 29, 2022. Accessed: Feb. 01, 2022. [Online]. Available: https://en.wikipedia.org/w/index.php?title=Deep_reinforcement_learning&oldid=1068657803

* [2]“Reinforcement learning,” Wikipedia. Jan. 15, 2022. Accessed: Feb. 01, 2022. [Online]. Available: https://en.wikipedia.org/w/index.php?title=Reinforcement_learning&oldid=1065862559

* [3]“AlphaZero,” Wikipedia. Jan. 15, 2022. Accessed: Feb. 01, 2022. [Online]. Available: https://en.wikipedia.org/w/index.php?title=AlphaZero&oldid=1065791194

* [4]“AlphaGo,” Wikipedia. Jan. 25, 2022. Accessed: Feb. 01, 2022. [Online]. Available: https://en.wikipedia.org/w/index.php?title=AlphaGo&oldid=1067772956

* [5]“AlphaGo Zero,” Wikipedia. Oct. 14, 2021. Accessed: Feb. 01, 2022. [Online]. Available: https://en.wikipedia.org/w/index.php?title=AlphaGo_Zero&oldid=1049954309

* [6]“Monte Carlo tree search,” Wikipedia. Jan. 23, 2022. Accessed: Feb. 01, 2022. [Online]. Available: https://en.wikipedia.org/w/index.php?title=Monte_Carlo_tree_search&oldid=1067396622

* [7]“Minimax,” Wikipedia. Jan. 18, 2022. Accessed: Feb. 01, 2022. [Online]. Available: https://en.wikipedia.org/w/index.php?title=Minimax&oldid=1066446492

* [8]“Alpha–beta pruning,” Wikipedia. Jan. 30, 2022. Accessed: Feb. 01, 2022. [Online]. Available: https://en.wikipedia.org/w/index.php?title=Alpha%E2%80%93beta_pruning&oldid=1068746141

* [9]“python-chess: a chess library for Python — python-chess 1.8.0 documentation.” https://python-chess.readthedocs.io/en/latest/ (accessed Feb. 01, 2022).

* [10]“Technical Explanation of Leela Chess Zero · LeelaChessZero/lc0 Wiki,” GitHub. https://github.com/LeelaChessZero/lc0 (accessed Feb. 01, 2022).


### AlphaZero & AlphaGo Zero specific articles & papers

* [11]D. Silver et al., “Mastering Chess and Shogi by Self-Play with a General Reinforcement Learning Algorithm,” arXiv:1712.01815 [cs], Dec. 2017, Accessed: Feb. 01, 2022. [Online]. Available: http://arxiv.org/abs/1712.01815

* [12]“A general reinforcement learning algorithm that masters chess, shogi, and Go through self-play.” https://www.science.org/doi/10.1126/science.aar6404 (accessed Feb. 01, 2022).

* [13]“engines - Understanding AlphaZero,” Chess Stack Exchange. https://chess.stackexchange.com/questions/19353/understanding-alphazero (accessed Feb. 01, 2022).

* [14]“How does AlphaZero learn to evaluate a position it has never seen?,” Chess Stack Exchange. https://chess.stackexchange.com/questions/19401/how-does-alphazero-learn-to-evaluate-a-position-it-has-never-seen (accessed Feb. 01, 2022).

* [15]“Figure 2: MCTS in AlphaGo Zero. | Nature”, Accessed: Feb. 01, 2022. [Online]. Available: https://www.nature.com/articles/nature24270/figures/2

* [16]J. Varty, “Alpha Zero And Monte Carlo Tree Search.” https://joshvarty.github.io/AlphaZero/ (accessed Feb. 01, 2022).

* [17]J. Varty, AlphaZeroSimple. 2022. Accessed: Feb. 01, 2022. [Online]. Available: https://github.com/JoshVarty/AlphaZeroSimple

* [18]“Was AlphaZero taught castling?,” Chess Stack Exchange. https://chess.stackexchange.com/questions/37468/was-alphazero-taught-castling (accessed Feb. 01, 2022).

* [19]T. M. Blog, “A Single-Player Alpha Zero Implementation in 250 Lines of Python.” https://tmoer.github.io/AlphaZero/ (accessed Feb. 01, 2022).

* [20]“AlphaZero |.” https://sebastianbodenstein.net/post/alphazero/ (accessed Feb. 01, 2022).

### Diagrams

* [21]“AlphaGo Zero Explained In One Diagram | by David Foster | Applied Data Science | Medium.” https://medium.com/applied-data-science/alphago-zero-explained-in-one-diagram-365f5abf67e0 (accessed Feb. 01, 2022).

### Tutorials

* [22]“AlphaZero, a novel Reinforcement Learning Algorithm, in JavaScript | by Carlos Aguayo | Towards Data Science.” https://towardsdatascience.com/alphazero-a-novel-reinforcement-learning-algorithm-deployed-in-javascript-56018503ad18 (accessed Feb. 01, 2022).

* [23]D. Foster, “How to build your own AlphaZero AI using Python and Keras,” Applied Data Science, Dec. 02, 2019. https://medium.com/applied-data-science/how-to-build-your-own-alphazero-ai-using-python-and-keras-7f664945c188 (accessed Feb. 01, 2022).

* [24]D. Foster, “How To Build Your Own MuZero AI Using Python (Part 1/3),” Applied Data Science, Feb. 23, 2021. https://medium.com/applied-data-science/how-to-build-your-own-muzero-in-python-f77d5718061a (accessed Feb. 01, 2022).

* [25]“Simple Alpha Zero.” https://web.stanford.edu/~surag/posts/alphazero.html (accessed Feb. 01, 2022).

* [26]D. Straus, “AlphaZero implementation and tutorial,” Medium, Jan. 27, 2020. https://towardsdatascience.com/alphazero-implementation-and-tutorial-f4324d65fdfc (accessed Feb. 01, 2022).
	* Updated article: [27]“How I trained a self-supervised neural network to beat GnuGo on small (7x7) boards | by Darin Straus | Analytics Vidhya | Medium.” https://medium.com/analytics-vidhya/how-i-trained-a-self-supervised-neural-network-to-beat-gnugo-on-small-7x7-boards-6b5b418895b7 (accessed Feb. 01, 2022).
	* [28]cody2007, alpha_go_zero_implementation. 2021. Accessed: Feb. 01, 2022. [Online]. Available: https://github.com/cody2007/alpha_go_zero_implementation



## Interesting videos

* [29]Lex Fridman, David Silver: AlphaGo, AlphaZero, and Deep Reinforcement Learning | Lex Fridman Podcast #86, (Apr. 03, 2020). Accessed: Feb. 01, 2022. [Online]. Available: https://www.youtube.com/watch?v=uPUEq8d73JI

* [30]DeepMind, RL Course by David Silver - Lecture 1: Introduction to Reinforcement Learning, (May 13, 2015). Accessed: Feb. 01, 2022. [Online]. Available: https://www.youtube.com/watch?v=2pWv7GOvuf0

* [31]Aske Plaat, Keynote David Silver NIPS 2017 Deep Reinforcement Learning Symposium AlphaZero, (Dec. 10, 2017). Accessed: Feb. 01, 2022. [Online]. Available: https://www.youtube.com/watch?v=A3ekFcZ3KNw

