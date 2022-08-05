class Node:
    def __init__(self, row: int, column: int, score: int = 0):
        self.row = row
        self.column = column
        self.parents = []
        self.score = score

    def set_score(self, score: int):
        self.score = score

    def set_row(self, row: int):
        self.row = row

    def set_column(self, column: int):
        self.column = column

    def add_parent(self, node):
        self.parents.append(node)
