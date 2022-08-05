from score_matrix import PAM250
from node import Node
import numpy as np

gap_penalty = 9
first_sequence, second_sequence = "", ""
score_matrix = None
node_dict = {}
new_node_dict = {}
final_path = []


def define_optimum_alignment_score():
    global score_matrix
    first_sequence_length = len(first_sequence) + 1
    second_sequence_length = len(second_sequence) + 1
    score_matrix = np.zeros((second_sequence_length, first_sequence_length))
    for i in range(0, first_sequence_length):
        score_matrix[0][i] = 0
    for i in range(0, second_sequence_length):
        score_matrix[i][0] = 0
    for i in range(1, second_sequence_length):
        for j in range(1, first_sequence_length):
            score_matrix[i][j] = max(
                score_matrix[i - 1][j - 1] + PAM250[second_sequence[i - 1:i]][first_sequence[j - 1:j]],
                score_matrix[i - 1][j] - gap_penalty, score_matrix[i][j - 1] - gap_penalty)

            parents = []
            if score_matrix[i][j] == score_matrix[i - 1][j - 1] + PAM250[second_sequence[i - 1:i]][
                first_sequence[j - 1:j]]:
                parents.append((i - 1, j - 1))
            if score_matrix[i][j] == score_matrix[i - 1][j] - gap_penalty:
                parents.append((i - 1, j))
            if score_matrix[i][j] == score_matrix[i][j - 1] - gap_penalty:
                parents.append((i, j - 1))

            new_node = None
            if (i, j) in node_dict:
                new_node = node_dict[(i, j)]
            else:
                new_node = Node(row=i, column=j)
            for parent in parents:
                if parent in node_dict:
                    new_node.add_parent(node_dict[parent])
                else:
                    parent_node = Node(row=parent[0], column=parent[1])
                    new_node.add_parent(parent_node)
            new_node.set_score(score_matrix[i][j])
            node_dict[(i, j)] = new_node


def get_input():
    global first_sequence, second_sequence
    first_string = input()
    second_string = input()
    first_sequence = first_string
    second_sequence = second_string


def get_destination_nodes(node_list):
    destination_list = []
    first_sequence_length = len(first_sequence)
    second_sequence_length = len(second_sequence)
    for l in node_list:
        if l.row == second_sequence_length or l.column == first_sequence_length:
            if not destination_list or l.score == destination_list[0].score:
                destination_list.append(l)
    return destination_list


def back_track(first_sequence, second_sequence, node_list, path):
    first_sequence_length = len(first_sequence)
    second_sequence_length = len(second_sequence)
    destination_nodes = node_list
    dest_node = destination_nodes[0]
    while True:
        row = dest_node.row
        column = dest_node.column
        parents = dest_node.parents
        if row == 0 or column == 0:
            dash = ""
            remainder = ""
            if row == 0:
                for i in range(column):
                    dash += "-"
                    remainder += first_sequence[first_sequence_length - 2 - i:first_sequence_length - 1 - i]
                path = [(path[0][0] + first_sequence[column - 1:column] + remainder, path[0][1] + dash)]
            else:
                for i in range(row):
                    dash += "-"
                    remainder += second_sequence[second_sequence_length - 2 - i:second_sequence_length - 1 - i]
                path = [(path[0][0] + dash, path[0][1] + second_sequence[row - 1:row] + remainder)]
            final_path.append((path[0][0][::-1], path[0][1][::-1]))
            break
        if not path:
            dash = ""
            remainder = ""
            if row == second_sequence_length:
                for i in range(first_sequence_length - column):
                    dash += "-"
                    remainder += first_sequence[first_sequence_length - 1 - i:first_sequence_length - i]
                path.append((remainder, dash))
            else:
                for i in range(second_sequence_length - row):
                    dash += "-"
                    remainder += second_sequence[second_sequence_length - 1 - i:second_sequence_length - i]
                path.append((dash, remainder))
        for parent in parents:
            if parent.row < row and parent.column < column:
                path2 = [(path[0][0] + first_sequence[column - 1:column], path[0][1] + second_sequence[row - 1:row])]
                back_track(first_sequence[:column - 1], second_sequence[:row - 1], [parent], path2)
            elif parent.row == row and parent.column < column:
                path3 = [(path[0][0] + first_sequence[column - 1:column], path[0][1] + "-")]
                back_track(first_sequence[:column - 1], second_sequence, [parent], path3)
            else:
                path4 = [(path[0][0] + "-", path[0][1] + second_sequence[row - 1:row])]
                back_track(first_sequence, second_sequence[:row - 1], [parent], path4)
        break


def final_back_track(first_sequence, second_sequence, node_list):
    for node in node_list:
        back_track(first_sequence, second_sequence, [node], [])


def print_result(node_list):
    print(int(node_list[0].score))
    sortedSeq = [i[0] + i[1] for i in final_path]
    sortedSeq.sort()
    for i in sortedSeq:
        print(i[0:int(len(i) / 2)])
        print(i[int(len(i) / 2):])


if __name__ == "__main__":
    get_input()
    define_optimum_alignment_score()
    node_list = sorted(node_dict.values(), key=lambda node: node.score, reverse=True)
    for l in node_list:
        new_node_dict[(l.row, l.column)] = l
    dest_node_list = get_destination_nodes(node_list)
    final_back_track(first_sequence, second_sequence, dest_node_list)
    print_result(dest_node_list)
