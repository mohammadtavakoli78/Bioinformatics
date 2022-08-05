from utils import *
from constant import Constant


def create_score_matrix(sequences: list):
    sequence_length = len(sequences)
    score_matrix = [0] * sequence_length
    for i in range(0, sequence_length):
        for j in range(i + 1, sequence_length):
            alignment_result = global_align(sequences[i], sequences[j], Constant.match, Constant.mismatch, Constant.gap)
            score_matrix[i] += alignment_result[2]
            score_matrix[j] += alignment_result[2]
    return score_matrix


def create_score_dict(sequences: list, score_matrix: list):
    score_dict = {}
    for index, seq in enumerate(sequences):
        score_dict[seq] = score_matrix[index]
    return score_dict


def second_create_score_dict(sequences: list, score_matrix: list):
    score_list = []
    for index, seq in enumerate(sequences):
        score_list.append((seq, score_matrix[index]))
    return score_list


def get_another_seq(sorted_score_list: list):
    sequence_length = len(sorted_score_list)
    score_matrix = {}
    for i in range(1, sequence_length):
        alignment_result = global_align(sorted_score_list[0], sorted_score_list[i], Constant.match, Constant.mismatch,
                                        Constant.gap)
        score_matrix[sorted_score_list[i]] = alignment_result[2]
    score_matrix = dict(sorted(score_matrix.items(), key=lambda x: x[1], reverse=True))
    return score_matrix


def second_get_another_seq(sorted_score_list: list):
    sequence_length = len(sorted_score_list)
    score_matrix = []
    for i in range(1, sequence_length):
        alignment_result = global_align(sorted_score_list[0][0], sorted_score_list[i][0], Constant.match,
                                        Constant.mismatch,
                                        Constant.gap)
        score_matrix.append((sorted_score_list[i][0], alignment_result[2]))
    score_matrix.sort(key=lambda x: x[1], reverse=True)
    return score_matrix


def align_sequences(score_dict: dict, sequences: list):
    sorted_score_dict = dict(sorted(score_dict.items(), key=lambda x: x[1], reverse=True))
    sorted_score_dict_length = len(sorted_score_dict)
    alignment_results = [0] * sorted_score_dict_length
    score_dict_key = list(sorted_score_dict.keys())
    temp_list = []
    temp_list.append(score_dict_key[0])
    temp = sequences.copy()
    temp.remove(score_dict_key[0])
    temp_list += temp
    another_seq_dict = get_another_seq(sorted_score_list=temp_list)
    another_seq_dict = [score_dict_key[0]] + list(another_seq_dict.keys())
    for i in range(1, sorted_score_dict_length):
        first_argument = alignment_results[i] if alignment_results[i] != 0 else another_seq_dict[i]
        second_argument = alignment_results[0] if alignment_results[0] != 0 else another_seq_dict[0]
        alignment_result = global_align(first_argument, second_argument, Constant.match, Constant.mismatch,
                                        Constant.gap)
        alignment_results[0] = alignment_result[1]
        alignment_results[i] = alignment_result[0]
        temp = []
        for j in range(1, i):
            if not temp:
                for counter, char in enumerate(alignment_results[0]):
                    if char == '-' and counter >= len(second_argument):
                        temp.append(counter)
                        second_argument += '-'
                        alignment_results[j] += '-'
                    if char != second_argument[counter]:
                        temp.append(counter)
                        alignment_results[j] = alignment_results[j][:counter] + '-' + alignment_results[j][counter:]
                        second_argument = second_argument[:counter] + '-' + second_argument[counter:]
            else:
                for counter in temp:
                    alignment_results[j] = alignment_results[j][:counter] + '-' + alignment_results[j][counter:]

    return alignment_results


def second_align_sequences(score_list: list, sequences: list):
    score_list.sort(key=lambda x: x[1], reverse=True)
    sorted_score_dict_length = len(score_list)
    alignment_results = [0] * sorted_score_dict_length

    # temp_score_list = sequences.copy()
    # temp_score_list.remove(score_list[0])
    # temp = score_list[0]
    # temp += temp_score_list

    another_seq_dict = second_get_another_seq(sorted_score_list=score_list)
    another_seq_dict = [score_list[0]] + another_seq_dict
    for i in range(1, sorted_score_dict_length):
        first_argument = alignment_results[i] if alignment_results[i] != 0 else another_seq_dict[i][0]
        second_argument = alignment_results[0] if alignment_results[0] != 0 else another_seq_dict[0][0]
        alignment_result = global_align(first_argument, second_argument, Constant.match, Constant.mismatch,
                                        Constant.gap)
        alignment_results[0] = alignment_result[1]
        alignment_results[i] = alignment_result[0]
        temp = []
        for j in range(1, i):
            if not temp:
                for counter, char in enumerate(alignment_results[0]):
                    if char == '-' and counter >= len(second_argument):
                        temp.append(counter)
                        second_argument += '-'
                        alignment_results[j] += '-'
                    if char != second_argument[counter]:
                        temp.append(counter)
                        alignment_results[j] = alignment_results[j][:counter] + '-' + alignment_results[j][counter:]
                        second_argument = second_argument[:counter] + '-' + second_argument[counter:]
            else:
                for counter in temp:
                    alignment_results[j] = alignment_results[j][:counter] + '-' + alignment_results[j][counter:]

    return alignment_results


def correct_order(sequences: list, alignment_results: list):
    alignment_results_length = len(alignment_results)
    final_alignment_results = [0] * alignment_results_length
    for seq in alignment_results:
        temp = seq.replace('-', '')
        new_index = sequences.index(temp)
        final_alignment_results[new_index] = seq

    return final_alignment_results


def second_correct_order(sequences: list, alignment_results: list):
    alignment_results_length = len(alignment_results)
    final_alignment_results = [0] * alignment_results_length
    for counter, seq in enumerate(alignment_results):
        temp = seq.replace('-', '')
        count = 0
        for i in range(0, counter):
            if alignment_results[i] == seq:
                count += 1
        new_index = [i for i, n in enumerate(sequences) if n == temp][count]
        final_alignment_results[new_index] = seq

    return final_alignment_results


def calculate_score(alignment_results: list):
    sequence_length = len(alignment_results[0])
    final_score = 0
    for i in range(sequence_length):
        temp = []
        temp_score = 0
        for j in alignment_results:
            temp.append(j[i])
        for k in range(0, len(temp)):
            for l in range(k + 1, len(temp)):
                if (temp[k] != '-' and temp[l] != '-') and temp[k] == temp[l]:
                    temp_score += Constant.match
                elif (temp[k] != '-' and temp[l] != '-') and temp[k] != temp[l]:
                    temp_score += Constant.mismatch
                elif temp[k] == '-' and temp[l] == '-':
                    temp_score += Constant.gap_gap
                else:
                    temp_score += Constant.gap
        final_score += temp_score

    return final_score


def print_result(sequences, score):
    print(score)
    for seq in sequences:
        print(seq)


def run_algorithm(sequences: list, main_sequences: list):
    score_matrix = create_score_matrix(sequences=sequences)
    score_dict = create_score_dict(sequences=sequences, score_matrix=score_matrix)
    alignment_results = align_sequences(score_dict=score_dict, sequences=sequences)
    final_alignment_result = correct_order(sequences=main_sequences, alignment_results=alignment_results)
    final_score = calculate_score(final_alignment_result)
    return final_alignment_result, final_score


def second_run_algorithm(sequences: list, main_sequences: list):
    score_matrix = create_score_matrix(sequences=sequences)
    score_list = second_create_score_dict(sequences=sequences, score_matrix=score_matrix)
    alignment_results = second_align_sequences(score_list=score_list, sequences=sequences)
    final_alignment_result = second_correct_order(sequences=main_sequences, alignment_results=alignment_results)
    final_score = calculate_score(final_alignment_result)
    return final_alignment_result, final_score


def find_desired_blocks(final_msa: list):
    sequences_length = len(final_msa[0])
    counter = 0
    first = 0
    blocks = []
    for num in range(sequences_length):
        temp = []
        for seq in final_msa:
            temp.append(seq[num])
        if len(list(dict.fromkeys(temp))) != 1 and counter == 0:
            first = num
            counter += 1
        elif len(list(dict.fromkeys(temp))) != 1 and counter != 0 and num < sequences_length - 1:
            counter += 1
        elif len(list(dict.fromkeys(temp))) != 1 and counter != 0 and num == sequences_length - 1:
            if counter >= 1:
                blocks.append(str(first) + ":" + str(num))
            first = 0
            counter = 0
        elif len(list(dict.fromkeys(temp))) == 1 and counter != 0:
            if counter > 1:
                blocks.append(str(first) + ":" + str(num - 1))
            first = 0
            counter = 0

    return blocks


def get_specific_blocks(final_msa: list, block: str):
    specific_sub_str = []
    start_index = int(block.split(":")[0])
    end_index = int(block.split(":")[1])
    for seq in final_msa:
        specific_sub_str.append(seq[start_index:end_index + 1])
    return specific_sub_str


def remove_dash(final_msa: list):
    specific_sub_str = []
    for seq in final_msa:
        specific_sub_str.append(seq.replace("-", ""))
    return specific_sub_str


def replace_refined_blocks_with_main_seq(final_msa: list, start_index: int, end_index: int, blocks: list):
    for counter, seq in enumerate(final_msa):
        if start_index == 0 and end_index == len(seq) - 1:
            temp = blocks[counter]
        elif start_index == 0:
            temp = blocks[counter] + seq[end_index + 1:]
        elif end_index == len(seq) - 1:
            temp = seq[:start_index] + blocks[counter]
        else:
            temp = seq[:start_index] + blocks[counter] + seq[end_index + 1:]
        final_msa[counter] = temp
    return final_msa


def refine_msa(blocks: list, final_msa: list, second_sequences: list, old_score: int):
    if len(blocks) == 0:
        return []
    else:
        for counter, block in enumerate(blocks):
            temp_blocks = find_desired_blocks(final_msa=final_msa)
            block = temp_blocks[counter]
            sequences = get_specific_blocks(final_msa=final_msa, block=block)
            new_sequences = remove_dash(sequences)
            if len(list(dict.fromkeys(new_sequences))) == len(new_sequences):
                final_alignment_result, final_score = run_algorithm(sequences=new_sequences,
                                                                    main_sequences=new_sequences)
            else:
                final_alignment_result, final_score = second_run_algorithm(sequences=new_sequences,
                                                                           main_sequences=new_sequences)
            start_index = int(block.split(":")[0])
            end_index = int(block.split(":")[1])
            final_msa_temp = replace_refined_blocks_with_main_seq(final_msa=final_msa.copy(), start_index=start_index,
                                                                  end_index=end_index,
                                                                  blocks=final_alignment_result)
            refined_final_alignment_result, new_score = run_algorithm(sequences=final_msa_temp,
                                                                      main_sequences=second_sequences)
            if new_score >= old_score:
                final_msa = refined_final_alignment_result
                old_score = new_score
        return final_msa


if __name__ == "__main__":
    sequences = get_input()
    second_sequences = remove_dash(sequences)
    final_alignment_result, final_score = run_algorithm(sequences=sequences, main_sequences=second_sequences)
    blocks = find_desired_blocks(final_msa=final_alignment_result)
    final_msa = refine_msa(blocks=blocks, final_msa=final_alignment_result.copy(), second_sequences=second_sequences,
                           old_score=final_score)
    if not final_msa:
        print_result(sequences=final_alignment_result, score=final_score)
    else:
        while True:
            refined_final_alignment_result, new_score = run_algorithm(sequences=final_msa.copy(),
                                                                      main_sequences=second_sequences)
            blocks = find_desired_blocks(final_msa=refined_final_alignment_result)
            final_msa = refine_msa(blocks=blocks, final_msa=refined_final_alignment_result.copy(),
                                   second_sequences=second_sequences,
                                   old_score=new_score)
            score = calculate_score(final_msa)
            if score == final_score:
                break
            else:
                final_score = score
        print_result(sequences=final_msa, score=score)
