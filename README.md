# Jamb Game

A console-based implementation of the classic Jamb (also known as Yahtzee/Yatzy) dice game in Python, featuring a cryptographically-inspired random number generator, intelligent AI opponent using Monte Carlo simulation, and dynamic data structure optimization.

> **Note:** Jamb is a popular Balkan variant of Yahtzee/Yatzy, played with five dice and featuring unique column-based scoring rules.

## Features

### Core Game Mechanics
- **Jamb Game Rules**: Full implementation of the traditional Jamb (Yahtzee/Yatzy variant) dice game with:
  - Five dice rolled per turn
  - **Three rolls per turn maximum** with strategic dice holding between rolls
  - Three columns: Down, Up, and Free (Hand)
  - Standard scoring combinations: Numbers (1-6), Straight, Full House, Four of a Kind, Five of a Kind

#### How Dice Rolling Works:
1. **First Roll**: All five dice are rolled
2. **Choose which dice to keep**: After seeing the result, you select which dice to hold (keep) and which to reroll
3. **Second Roll**: Only the selected dice are rerolled, kept dice remain unchanged
4. **Choose again**: You can change your selection - hold different dice or release previously held ones
5. **Third Roll**: Final reroll opportunity with the same selection mechanism
6. **Submit Score**: After the third roll (or earlier if you choose), you must place your result in an available cell on the board

This strategic dice-holding mechanic is the core of the game - deciding which dice to keep and which to reroll based on your target combination and available scoring positions.

### Blum Blum Shub (BBS) Random Number Generator
- Cryptographically secure pseudorandom number generator
- Uses two large safe primes (p = 982451819, q = 982451863)
- Time-based seed generation for unpredictability
- Parity-based bit extraction for dice values (1-6)

### AI Opponent with Monte Carlo Simulation
- **Smart Decision Making**: AI uses probability-based strategy to determine optimal moves
- **Monte Carlo Method**: Simulates thousands of possible outcomes to calculate success probabilities
- **Adaptive Strategy**: Different approaches based on game state:
  - Option 1: Prioritizes special combinations when probability threshold (35%) is met
  - Option 2: Chooses column based on maximum dice count
  - Option 3: Compares probabilities between special combinations
  - Option 4: Falls back to number combinations when special combos unlikely

### Dynamic Data Structure Optimization
- **Coordinate List**: Efficient sparse matrix representation for early game
- **Automatic Conversion**: Switches to full matrix when data becomes dense
- **Memory Efficiency**: Minimizes storage by using appropriate structure for game state

## Game Rules

### Scoring Columns
1. **Down (D)**: Fill from top (1) to bottom (Jamb)
2. **Up (G)**: Fill from bottom (Jamb) to top (1)
3. **Free/Hand (R)**: Fill any row, but only on the first roll

### Scoring Combinations
- **Numbers (1-6)**: Sum of matching dice (e.g., three 4s = 12 points)
- **Straight (Kenta)**: 2-3-4-5 with 1 or 6
  - First roll: 66 points
  - Second roll: 56 points
  - Third roll: 46 points
- **Full House (Ful)**: Three of a kind + pair = 30 + 3×(triple value) + 2×(pair value)
- **Four of a Kind (Poker)**: Four matching dice = 40 + 4×(dice value)
- **Five of a Kind (Jamb)**: Five matching dice = 50 + 5×(dice value)

## Usage

### Starting the Game
When you run the program, you'll see the main menu:

```
Menu:
[1] Baci kocke (Roll dice - Human player)
[2] Pomoć prijatelja (AI assistance)
[N] Nova igra (New game)
[Q] Izlaz (Quit)
```

### Playing as Human
1. Choose option `[1]` to play manually
2. **First Roll**: All five dice are rolled automatically:
```
Bacanje #1:  2  3  4  4  5
             [A] [B] [C] [D] [E]
```
3. **Decision Time**: You have three options:
   - Press **ENTER** to accept the current result and submit your score
   - Type letters **A-E** (e.g., `ACE` or `B D`) to select which dice to **reroll**
   - The dice you DON'T select will be **held (kept)** for the next roll

4. **Example Turn**:
   ```
   Bacanje #1:  2  3  4  4  5     <- Initial roll
                [A] [B] [C] [D] [E]
   
   You type: A B E                 <- Reroll dice A, B, and E
                                     (Keep the two 4s at positions C and D)
   
   Bacanje #2:  6  1  4  4  3     <- New roll (positions C & D still show 4, 4)
                [A] [B] [C] [D] [E]
   
   You type: A E                   <- Reroll only A and E
                                     (Keep 4, 4, and the 1)
   
   Bacanje #3:  4  1  4  4  2     <- Final roll
                [A] [B] [C] [D] [E]
   
   You type: ENTER                 <- Accept result (you got three 4s!)
   ```

5. **Submit Score**: Choose where to write the result using column-row notation (e.g., `D4` for Down column, row 4 to score your three 4s = 12 points)

### Playing with AI Assistance
1. Choose option `[2]` to let the AI play
2. The AI will automatically:
   - Analyze the current dice roll
   - Decide which dice to keep and which to reroll based on probability calculations
   - Perform up to 3 rolls (stopping early if the target combination is achieved)
   - Determine the optimal scoring position
3. Watch as the AI displays its strategy:
```
Bacanje #1:  2  3  4  5  6
Sačuvamo:    .  ↑  ↑  ↑  ↑  (kenta)  <- AI keeps 3,4,5,6 and rerolls position A

Bacanje #2:  2  3  4  5  6
Sačuvamo:    ↑  ↑  ↑  ↑  ↑  (kenta)  <- Got straight! AI holds all dice
```

### Example Gameplay Output
```
-----------------------------------------
| CooList | Na dole | Na gore |  Ručna  |
-----------------------------------------
|       1 |         |         |         |
|       2 |         |         |         |
|       3 |         |         |         |
|       4 |         |         |         |
|       5 |         |         |         |
|       6 |         |         |         |
-----------------------------------------
|    Zbir |       0 |       0 |       0 |
-----------------------------------------
|   Kenta |         |         |         |
|     Ful |         |         |         |
|   Poker |         |         |         |
|    Jamb |         |         |         |
-----------------------------------------
|  Ukupno |       0 |       0 |       0 |
-----------------------------------------
```

## Technical Implementation

### Class Structure
- **`BBS`**: Blum Blum Shub random number generator
- **`Dices`**: Manages five dice, their values, and hold/release states
- **`Board`**: Game board logic, scoring, and round management
- **`Matrix`**: Standard 2D array implementation
- **`CoordinateList`**: Sparse matrix using binary search for efficiency
- **`Human`**: Human player interaction handler
- **`Robot`**: AI player with Monte Carlo simulation

### Key Algorithms
1. **Binary Search** (in `CoordinateList.find()`): O(log n) coordinate lookup
2. **Monte Carlo Simulation** (in `Robot.simulate()`): Probabilistic outcome prediction
3. **Parity Bit Extraction** (in `BBS.parity()`): Converts random quadratic residues to dice values

## AI Strategy Breakdown

The AI uses a threshold-based strategy (35% success probability):

```python
threshold = 0.35

# Example decision tree:
if position_down >= 6 and position_up < 6:
    if probability(special_combo) >= threshold:
        play_down_column()
    else:
        play_up_column()
```

## Performance Notes

- **Data Structure Transition**: Automatically switches from CoordinateList to Matrix when the sparse structure becomes inefficient
- **Simulation Samples**: Default 1,000 iterations for Monte Carlo (configurable via `n` parameter)
- **BBS Efficiency**: Uses bit-level operations for fast random number generation


