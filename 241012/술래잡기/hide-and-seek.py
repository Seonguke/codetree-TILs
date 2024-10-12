class Csumba():
    def __init__(self):
        self.is_catcher = -1
        self.is_tree = -999
        self.n = 0  # 5 ≤ n ≤ 99
        self.m = 0  # 1 ≤ m, h ≤ n
        self.h = 0  #
        self.k = 0  # 1 ≤ k ≤ 100
        self.move_dir = [[-1, 0], [0, 1], [1, 0], [0, -1]]

        self.catcher_can_move = 1
        self.catcher_move_cnt = 0
        self.runner_catched = {}
        self.runner = {}
        self.board_tree = []
        self.board = []
        self.catcher = []
        self.is_reverse = False
        self.score=0

    def input_param(self):
        self.n, self.m, self.h, self.k = map(int, input().split())
        self.board_tree = [[0] * self.n for _ in range(self.n)]
        self.board = [[0] * self.n for _ in range(self.n)]
        for m in range(self.m):
            i, j, d = map(int, input().split())
            dir = 1
            if d == 1:
                dir = 1
            else:
                dir = 2
            self.runner[m + 1] = [i - 1, j - 1, dir]
            self.board[i - 1][j - 1] = m + 1
            self.runner_catched[m + 1] = False

        for h in range(self.h):
            i, j = map(int, input().split())
            self.board_tree[i - 1][j - 1] = self.is_tree
        self.catcher = [self.n // 2, self.n // 2, 0]
        self.board[self.n // 2][self.n // 2]=self.is_catcher
    def check_range(self, i, j):
        if 0 <= i < self.n and 0 <= j < self.n:
            return True
        else:
            return False

    def distance2d(self, src_i, src_j, dst_i, dst_j):
        return abs(src_i - dst_i) + abs(src_j - dst_j)

    def runner_move(self):
        pass

    def catcher_move(self):
        start_i, start_j, dir = self.catcher

        next_i = start_i + self.move_dir[dir][0]
        next_j = start_j + self.move_dir[dir][1]
        self.board[start_i][start_j] = 0
        self.catcher_move_cnt += 1

        if self.catcher_move_cnt == self.catcher_can_move:

            if self.is_reverse == False:
                if dir % 2 == 1 and not (next_i == 0 and next_j == 0):
                    self.catcher_can_move += 1
                dir = (dir + 1) % 4
            else:
                if dir % 2 == 0 and not (next_i == 0 and next_j == 0):
                    if not (next_i == self.n - 1 and next_j == 0):
                        self.catcher_can_move -= 1
                dir = (dir - 1) % 4
            self.catcher_move_cnt = 0

        if next_i == 0 and next_j == 0:
            self.is_reverse = True
            dir = 2
            self.catcher_move_cnt = 0
            self.catcher_can_move -= 1
        elif next_i == self.n // 2 and next_j == self.n // 2:
            self.is_reverse = False
            dir = 0
            self.catcher_move_cnt = 0
            self.catcher_can_move = 1

        self.board[next_i][next_j] = self.is_catcher
        self.catcher = [next_i, next_j, dir]

    def runner_move(self):
        for runner_idx, v in self.runner.items():
            if self.runner_catched[runner_idx] == True:
                continue
            start_i, start_j, dir = v
            catcher_i, catcher_j, _ = self.catcher
            dist = self.distance2d(start_i, start_j, catcher_i, catcher_j)
            if dist > 3: continue

            next_i = start_i + self.move_dir[dir][0]
            next_j = start_j + self.move_dir[dir][1]

            if self.check_range(next_i, next_j) == False:
                dir = (dir + 2) % 4
                next_i = start_i + self.move_dir[dir][0]
                next_j = start_j + self.move_dir[dir][1]

            if self.board[next_i][next_j] != self.is_catcher:
                self.board[start_i][start_j] = 0
                #self.board[next_i][next_j] = runner_idx
                self.runner[runner_idx] = [next_i, next_j, dir]

        for runner_idx, v in self.runner.items():
            if self.runner_catched[runner_idx] == True:
                continue
            start_i, start_j, dir = v
            self.board[start_i][start_j] =runner_idx

    def catch_runner(self):
        catcher_i, catcher_j, dir = self.catcher
        catch_cnt = 0
        for k in range(3):
            next_i = catcher_i + (k * self.move_dir[dir][0])
            next_j = catcher_j + (k * self.move_dir[dir][1])

            if self.check_range(next_i, next_j) == True:
                if self.board_tree[next_i][next_j] != self.is_tree and \
                        self.board[next_i][next_j] > 0:
                    runner_idx = self.board[next_i][next_j]
                    self.runner_catched[runner_idx] = True
                    self.board[next_i][next_j] = 0
                    catch_cnt +=1
        return catch_cnt
    def play(self):
        for round in range(1, self.k + 1):
            if round == 2 :
                a=0
            self.runner_move()
            self.catcher_move()
            catch_cnt = self.catch_runner()
            self.score += catch_cnt * round
        print(self.score)

if __name__ == "__main__":
    sumba = Csumba()
    sumba.input_param()
    sumba.play()