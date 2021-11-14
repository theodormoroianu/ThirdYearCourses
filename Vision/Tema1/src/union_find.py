from typing import List


class UnionFind:
    tata: List[int]
    g: List[int]

    def to_id(self, x, y):
        return 9 * x + y
    
    def from_id(self, id):
        return id // 9, id % 9

    def __init__(self):
        self.tata = [i for i in range(81)]
        self.g = [1 for i in range(81)]

    def find(self, x):
        if self.tata[x] == x:
            return x
        self.tata[x] = self.find(self.tata[x])
        return self.tata[x]

    def join(self, a, b):
        a = self.find(a)
        b = self.find(b)

        if a == b:
            return False
        
        if self.g[a] == 9 and self.g[b] == 9:
            return False

        if self.g[a] + self.g[b] > 9:
            print("WARNING: UF atempted a join with size > 9! Join ignored.")
            return False
        
        self.tata[a] = b
        self.g[b] += self.g[a]

        return True

    def compute_classes(self):
        classes = [-1 for i in range(81)]
        cnt = 0

        mat = [[-1 for i in range(9)] for j in range(9)]

        for i in range(9):
            for j in range(9):
                repr = self.find(self.to_id(i, j))
                if classes[repr] == -1:
                    cnt = cnt + 1
                    classes[repr] = cnt
                mat[i][j] = classes[repr]

        return mat