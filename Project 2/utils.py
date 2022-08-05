def global_align(x, y, s_match, s_mismatch, s_gap):
    A = []

    for i in range(len(y) + 1):
        A.append([0] * (len(x) + 1))

    for i in range(len(y) + 1):
        A[i][0] = s_gap * i

    for i in range(len(x) + 1):
        A[0][i] = s_gap * i

    for i in range(1, len(y) + 1):

        for j in range(1, len(x) + 1):
            A[i][j] = max(

                A[i][j - 1] + s_gap,

                A[i - 1][j] + s_gap,

                A[i - 1][j - 1] + (s_match if (y[i - 1] == x[j - 1] and y[i - 1] != '-') else 0) + (

                    s_mismatch if (y[i - 1] != x[j - 1] and y[i - 1] != '-' and x[j - 1] != '-') else 0) + (

                    s_gap if (y[i - 1] == '-' or x[j - 1] == '-') else 0)

            )

    align_X = ""

    align_Y = ""

    i = len(x)

    j = len(y)

    while i > 0 or j > 0:

        current_score = A[j][i]

        if i > 0 and j > 0 and (

                ((x[i - 1] == y[j - 1] and y[j - 1] != '-') and current_score == A[j - 1][i - 1] + s_match) or

                ((y[j - 1] != x[i - 1] and y[j - 1] != '-' and x[i - 1] != '-') and current_score == A[j - 1][

                    i - 1] + s_mismatch) or

                ((y[j - 1] == '-' or x[i - 1] == '-') and current_score == A[j - 1][i - 1] + s_gap)

        ):

            align_X = x[i - 1] + align_X

            align_Y = y[j - 1] + align_Y

            i = i - 1

            j = j - 1

        elif i > 0 and (current_score == A[j][i - 1] + s_gap):

            align_X = x[i - 1] + align_X

            align_Y = "-" + align_Y

            i = i - 1

        else:

            align_X = "-" + align_X

            align_Y = y[j - 1] + align_Y

            j = j - 1

    return (align_X, align_Y, A[len(y)][len(x)])


def get_input():
    sequence_num = int(input())
    sequences = []
    for i in range(sequence_num):
        sequences.append(input())
    return sequences
