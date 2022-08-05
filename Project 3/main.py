import math
from utils import *

PSEUDO_COUNT = 2
all_sequence = []


def AllKLength(given_set, k, window):
    n = len(given_set)
    AllKLengthRec(given_set, "", n, k, window)


def AllKLengthRec(given_set, prefix, n, k, window):
    if k == 0:
        if prefix.replace("-", "") in window[:-1]:
            all_sequence.append(prefix)
        return
    for i in range(n):
        new_prefix = prefix + given_set[i]
        AllKLengthRec(given_set, new_prefix, n, k - 1, window)


def get_unique_amino_acids(sequences: list):
    unique_str = ""
    for sequence in sequences:
        unique_str += sequence
    unique_str = "".join(dict.fromkeys(unique_str))

    return unique_str.replace("-", "") + "-"


def get_one_char_frequency(sequences: list, index: int, desired_char: str):
    counter = 0
    for sequence in sequences:
        if sequence[index] == desired_char:
            counter += 1
    return counter


def create_score_matrix(sequences: list, alphabets: str):
    one_sequence_length = len(sequences[0])
    number_of_sequences = len(sequences)
    alphabets_length = len(alphabets)
    score_matrix = {}
    for alphabet in alphabets:
        temp = []
        score_matrix[alphabet] = []
        for n in range(one_sequence_length):
            score = (get_one_char_frequency(sequences=sequences, index=n, desired_char=alphabet) + PSEUDO_COUNT) / (
                    number_of_sequences + alphabets_length * PSEUDO_COUNT)
            temp.append(score)
        sum_temp = sum(temp)
        overall_frequency = sum_temp / one_sequence_length
        new_temp = [math.log(x / overall_frequency, 2) for x in temp]
        score_matrix[alphabet] = new_temp
    return score_matrix


def get_one_sub_sequence_score(score_matrix: dict, sequence: str):
    score = 0
    for index, char in enumerate(sequence):
        score += score_matrix[char][index]
    return score


def get_best_sub_sequence(score_matrix: dict, final_sequence: str, one_sequence_length: int):
    final_score = 0
    final_sub_sequence = ""
    final_sequence_length = len(final_sequence)
    offset = 0
    while offset + one_sequence_length - 1 <= final_sequence_length:
        window = final_sequence[offset:offset + one_sequence_length - 1]
        window = window + "-"
        global all_sequence
        all_sequence = []
        AllKLength([char for char in window], one_sequence_length, window)
        offset += 1
        for seq in all_sequence:
            score = get_one_sub_sequence_score(score_matrix=score_matrix, sequence=seq)
            if score > final_score:
                final_score = score
                final_sub_sequence = seq
    return final_score, final_sub_sequence


if __name__ == "__main__":
    sequences, final_sequence = get_input()
    alphabets = get_unique_amino_acids(sequences=sequences)
    score_matrix = create_score_matrix(sequences=sequences, alphabets=alphabets)
    final_score, final_sub_sequence = get_best_sub_sequence(score_matrix=score_matrix, final_sequence=final_sequence,
                                                            one_sequence_length=len(sequences[0]))
    print(final_sub_sequence)
