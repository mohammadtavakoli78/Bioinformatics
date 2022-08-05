def get_input():
    sequences = []
    numbers_of_sequences = int(input())
    for i in range(numbers_of_sequences):
        sequences.append(input())
    final_sequence = input()

    return sequences, final_sequence
