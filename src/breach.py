import random
import time
from typing import List, Tuple

class Sequence:
    def __init__(self, sequence_data: List[str] = None, bonus: int = 0):
        self.sequence_data = sequence_data or []
        self.bonus = bonus

class SequenceTrie:
    def __init__(self):
        self.root = {}
        self.end_symbol = '*'

    def insert(self, sequence: Sequence):
        node = self.root
        for i, token in enumerate(sequence.sequence_data):
            if token not in node:
                node[token] = {}
            node = node[token]
            if i == len(sequence.sequence_data) - 1:
                if self.end_symbol not in node or sequence.bonus > node[self.end_symbol]:
                    node[self.end_symbol] = sequence.bonus

    def find_max_bonus(self, tokens: List[str]) -> int:
        node = self.root
        max_bonus = 0
        for i in range(len(tokens)):
            current_sequence = tokens[i:]
            current_node = node
            for token in current_sequence:
                if token not in current_node:
                    break
                current_node = current_node[token]
                if self.end_symbol in current_node:
                    max_bonus = max(max_bonus, current_node[self.end_symbol])
        return max_bonus

def create_sequence_trie(sequences: List[Sequence]) -> SequenceTrie:
    trie = SequenceTrie()
    for seq in sequences:
        trie.insert(seq)
    return trie

def find_best_sequence(board: List[List[str]], row_count: int, col_count: int, buffer_size: int, sequence_trie: SequenceTrie) -> Tuple[List[Tuple[str, int, int]], int]:
    best_sequence = []
    max_bonus = 0

    def check_sequence(sequence: List[Tuple[str, int, int]]):
        nonlocal best_sequence, max_bonus
        tokens = [item[0] for item in sequence]
        bonus = sequence_trie.find_max_bonus(tokens)
        if bonus > max_bonus:
            max_bonus = bonus
            best_sequence = sequence

    # Horizontal search
    for row in range(row_count):
        for col in range(col_count - buffer_size + 1):
            sequence = [(board[row][col+i], row, col+i) for i in range(buffer_size)]
            check_sequence(sequence)

    # Vertical search
    for col in range(col_count):
        for row in range(row_count - buffer_size + 1):
            sequence = [(board[row+i][col], row+i, col) for i in range(buffer_size)]
            check_sequence(sequence)

    return best_sequence, max_bonus

def generate_smart_board(row_count: int, col_count: int, tokens: List[str], sequences: List[Sequence]) -> List[List[str]]:
    board = [[random.choice(tokens) for _ in range(col_count)] for _ in range(row_count)]
    
    # Ensure at least one sequence is present
    if sequences:
        seq = random.choice(sequences)
        row = random.randint(0, row_count - 1)
        col = random.randint(0, col_count - len(seq.sequence_data))
        for i, token in enumerate(seq.sequence_data):
            board[row][col + i] = token
    
    return board

def create_sequence(total_sequence: int, max_sequence: int, tokens: List[str]) -> List[Sequence]:
    sequences = []
    for _ in range(total_sequence):
        sequence_length = random.randint(2, max_sequence)
        sequence_data = [random.choice(tokens) for _ in range(sequence_length)]
        bonus = random.randint(1, 10) * 5
        sequences.append(Sequence(sequence_data, bonus))
    return sequences

def print_matrix(board: List[List[str]]):
    for row in board:
        print(" ".join(row))

def print_sequence(sequences: List[Sequence]):
    for i, seq in enumerate(sequences, 1):
        print(f"Sequence {i}: {' '.join(seq.sequence_data)} Bonus: {seq.bonus}")

def get_cli_input() -> Tuple[List[str], int, int, int, int, int]:
    total_unique_token = int(input("Enter the number of unique tokens: "))
    tokens = input("Enter the tokens: ").split()
    
    if len(tokens) != total_unique_token:
        raise ValueError("Number of tokens does not match the specified count")

    buffer_size = int(input("Enter the buffer size: "))
    if buffer_size <= 0:
        raise ValueError("Buffer size must be greater than 0")

    row_count, col_count = map(int, input("Enter the matrix size (rows columns): ").split())
    total_sequence = int(input("Enter the number of sequences: "))
    max_sequence = int(input("Enter the maximum sequence length: "))

    return tokens, buffer_size, row_count, col_count, total_sequence, max_sequence

def get_file_input(filename: str) -> Tuple[List[List[str]], int, List[Sequence]]:
    with open(f"../test/{filename}.txt", "r") as file:
        lines = file.readlines()
        buffer_size = int(lines[0].strip())
        row_count, col_count = map(int, lines[1].split())
        
        board = [line.split() for line in lines[2:row_count+2]]
        
        total_sequence = int(lines[row_count+2])
        sequences = []
        for i in range(row_count+3, len(lines), 2):
            sequence_data = lines[i].split()
            bonus = int(lines[i+1].strip())
            sequences.append(Sequence(sequence_data, bonus))
    
    return board, buffer_size, sequences

def save_solution(filename: str, total_bonus: int, best_sequence: List[Tuple[str, int, int]], elapsed_time: float):
    with open(f"../test/{filename}.txt", "w") as file:
        file.write(f"{total_bonus}\n")
        if total_bonus != 0:
            file.write(" ".join(item[0] for item in best_sequence) + "\n")
            for item in best_sequence:
                file.write(f"{item[1]}, {item[2]}\n")
        file.write(f"\n{elapsed_time:.2f} ms")

def main():
    while True:
        print("Choose input type:")
        print("1. CLI")
        print("2. TXT")
        input_type = input("Select input type: ")

        if input_type == "1":
            tokens, buffer_size, row_count, col_count, total_sequence, max_sequence = get_cli_input()
            sequences = create_sequence(total_sequence, max_sequence, tokens)
            board = generate_smart_board(row_count, col_count, tokens, sequences)
        elif input_type == "2":
            filename = input("Enter the filename: ")
            board, buffer_size, sequences = get_file_input(filename)
            row_count, col_count = len(board), len(board[0])
        else:
            print("Invalid input")
            continue

        print("Sequences:")
        print_sequence(sequences)
        print("\nMatrix:")
        print_matrix(board)

        sequence_trie = create_sequence_trie(sequences)

        start_time = time.time()
        best_sequence, total_bonus = find_best_sequence(board, row_count, col_count, buffer_size, sequence_trie)
        end_time = time.time()

        elapsed_time_ms = (end_time - start_time) * 1000

        print(f"\nTotal Bonus: {total_bonus}")
        if total_bonus > 0:
            print("Best Sequence:")
            print(" ".join(item[0] for item in best_sequence))
            print("Coordinates:")
            for item in best_sequence:
                print(f"{item[1]}, {item[2]}")

        print(f"\nExecution Time: {elapsed_time_ms:.2f} ms")

        save_choice = input("Do you want to save the solution? (y/n) ").lower()
        if save_choice == 'y':
            output_filename = input("Enter the output filename: ")
            save_solution(output_filename, total_bonus, best_sequence, elapsed_time_ms)
            print(f"Solution saved to ../test/{output_filename}.txt")

        if input("Continue playing? (y/n) ").lower() != 'y':
            break

if __name__ == "__main__":
    main()