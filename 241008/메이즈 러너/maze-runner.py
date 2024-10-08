class Cmazerunner():
    def __init__(self):
        self.n = 0
        self.m = 0
        self.k = 0
        # (조건)움직일 수 있는 칸이 2개 이상이라면, 상하로 움직이는 것을 우선
        self.move_dir = [[-1, 0], [1, 0], [0, 1], [0, -1]]
        self.board = []
        self.board_run = []
        self.runner = {}
        self.runner_moved = {}

        self.cur_exit = [0, 0]
        self.EXIT = -1
        # 1. 빈칸 - 이동 가능
        # 2. 벽 - 이동x, 1<=내구도<=9, 회전할때 -- , 내구도 0 -> 빈 칸
        # 3. 출구 - 해당 칸 도착 탈출 -1

    def input_param(self):
        self.n, self.m, self.k = map(int, input().split())

        for i in range(self.n):
            arr = list(map(int, input().split()))
            self.board.append(arr)

        for runner_cnt in range(self.m):
            is_exist = False
            r, c = map(int, input().split())  # 좌상단은 (1,1) i,j
            self.runner[runner_cnt + 1] = [r - 1, c - 1, is_exist]
            self.runner_moved[runner_cnt+1] = 0

        r, c = map(int, input().split())
        self.cur_exit = [r - 1, c - 1]
        self.board[r - 1][c - 1] = self.EXIT

    def distance2d(self, src_i, src_j, dst_i, dst_j):
        # (x1,y1), (x2,y2)의 최단거리는 ∣x1−x2∣+∣y1−y2∣로 정의
        return abs(src_i - dst_i) + abs(src_j - dst_j)

    def runner_move(self):
        board_run = [[None] * self.n for _ in range(self.n)]

        for k, v in self.runner.items():
            cur_i, cur_j, is_exist = v
            if is_exist: continue

            is_moved = False
            cur_dist = self.distance2d(cur_i, cur_j, self.cur_exit[0], self.cur_exit[1])
            for dir in self.move_dir:  # 상하로 움직이는 것을 우선

                next_i = dir[0] + cur_i
                next_j = dir[1] + cur_j
                if not (0 <= next_i < self.n and 0 <= next_j < self.n): continue
                next_dist = self.distance2d(next_i, next_j, self.cur_exit[0], self.cur_exit[1])
                if self.board[next_i][next_j] <= 0 and cur_dist > next_dist:
                    # 움직인 칸은 현재 머물러 있던 칸보다 출구까지의 최단 거리가 가까워
                    cur_dist = next_dist
                    self.runner[k] = [next_i, next_j,is_exist]
                    self.runner_moved[k]+=1
                    if board_run[next_i][next_j] is None:
                        board_run[next_i][next_j] = [k]
                    else:
                        # 한 칸에 2명 이상의 참가자가 있을 수 있
                        board_run[next_i][next_j].append(k)
                    is_moved = True
                    break
            if is_moved == False:
                if board_run[cur_i][cur_j] is None:
                    board_run[cur_i][cur_j] = [k]
                else:
                    # 한 칸에 2명 이상의 참가자가 있을 수 있
                    board_run[cur_i][cur_j].append(k)

        return board_run
    def find_miro(self, board_runner):
        arr = []  # [N,starti,startj]
        for start_i in range(self.n):
            if start_i ==1:
                a=0
            for start_j in range(self.n):
                for n in range(self.n):
                    end_i = start_i + n + 1
                    end_j = start_j + n + 1
                    if not (0 <= end_i < self.n and 0 <= end_j < self.n): continue
                    arr_pos = []
                    for i in range(start_i , end_i):
                        for j in range(start_j , end_j):
                            if board_runner[i][j] is not None or self.board[i][j] == self.EXIT:
                                arr_pos.append([i, j])
                    if len(arr_pos) >= 2 and self.cur_exit in arr_pos:
                        arr.append([n, start_i, start_j])
        return arr

    def rotate_partial_arr(self,board_part,n):
        board_copy = [arr[:] for arr in self.board]
        for i in range(0, n + 1):
            for j in range(0, n + 1):
                if board_part[i][j] >0:
                    board_copy[j][n-i] = board_part[i][j] -1
                else:
                    board_copy[j][n-i] = board_part[i][j]
        return board_part

    def rotate_arr(self,board_runner,square):
        n,start_i,start_j = square
        #board_runer_rotated = [arr[:] for arr in board_runner]
        #board_rotated = [arr[:] for arr in self.board]
        board_runer_part = [[None]*(n+1) for _ in range(n+1)]
        board_part = [[0]*(n+1) for _ in range(n+1)]
        ii=0
        for i in range(start_i,start_i + n + 1):
            jj=0
            for j in range(start_j,start_j + n + 1):
                board_part[ii][jj] = self.board[i][j]
                board_runer_part[ii][jj] = board_runner[i][j]
                jj+=1
            ii+=1

        board_runer_part_cp = [[None] * (n+1) for _ in range((n+1))]
        board_part_cp = [[0] * (n+1) for _ in range((n+1))]
        for i in range(0, n + 1):
            for j in range(0, n + 1):
                if board_part[i][j] >0:
                    board_part_cp[j][n-i] = board_part[i][j] -1
                else:
                    board_part_cp[j][n-i] = board_part[i][j]
                board_runer_part_cp[j][n-i]= board_runer_part[i][j]
        ii=0
        for i in range(start_i,start_i + n + 1):
            jj=0
            for j in range(start_j,start_j + n + 1):
                self.board[i][j] = board_part_cp[ii][jj]
                board_runner[i][j] = board_runer_part_cp[ii][jj]
                jj+=1
            ii+=1

        return board_runner


    def rotate_miro(self, board_runner):
        arr_square = self.find_miro(board_runner)
        # (Sort)정사각형이 2개 이상이라면, 좌상단 r 좌표가 작은 것이 우선되고,
        # 그래도 같으면 c 좌표가 작은 것
        arr_square.sort(key=lambda x: (x[0],x[1],x[2]))
        square = arr_square[0]

        return self.rotate_arr(board_runner,square)


    def update_runer(self,board_runner):
        for i in range(self.n):
            for j in range(self.n):
                if self.board[i][j] == self.EXIT:
                    self.cur_exit = [i, j]
                if board_runner[i][j] is not None:
                    for runner_k in board_runner[i][j]:
                        if self.board[i][j] == self.EXIT:
                            self.runner[runner_k][-1] = True
                        else:
                            self.runner[runner_k] = [i,j,False]

    def check_runner(self):
        cnt = len(self.runner)

        for k ,v in self.runner.items():
            i,j,is_exist =v
            if is_exist == True:
                cnt -=1

        return cnt
    def play(self):
        for k in range(self.k):
            #print(k)
            board_runner = self.runner_move()
            board_rot_runner = self.rotate_miro(board_runner)
            self.update_runer(board_rot_runner)
            cnt = self.check_runner()
            if cnt ==0:
                break
        dist = 0
        for k, v in self.runner_moved.items():
            dist += v

        print(dist)
        print(f"{self.cur_exit[0]+1} {self.cur_exit[1]+1}")

if __name__ == "__main__":
    maze = Cmazerunner()
    maze.input_param()
    maze.play()