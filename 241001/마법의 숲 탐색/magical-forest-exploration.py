from collections import deque


class CMagicForest():
    def __init__(self):
        self.r = 0
        self.c = 0
        self.k = 0

        self.forest_arr = []
        self.golam = []
        self.exit_dir = [[-1, 0],  # 북
                         [0, 1],  # 동
                         [1, 0],  # 남
                         [0, -1]]  # 서

        self.fairy_i_cnt = 0  # if r==6  0~7   더할때 i - 1   0,1 장외
        self.margin = 3

    def input_param(self):
        self.r, self.c, self.k = map(int, input().split())
        self.forest_arr = [[0] * self.c for _ in range(self.r + self.margin)]

        for i in range(self.k):
            c, d = map(int, input().split())  # 출발, 출구 방향
            self.golam.append([0, c - 1, d])  # i,j,d

    def golam_move_arr(self, cur_i, cur_j, golam_dir):

        move_dir = []

        if golam_dir == 0:
            # 0,1,2,3 북 동 남 서
            move_dir = [
                [cur_i + 1, cur_j + 1],
                [cur_i + 1, cur_j - 1],
                [cur_i + 2, cur_j]
            ]

        elif golam_dir == 1:
            move_dir = [
                [cur_i - 1, cur_j - 1],
                [cur_i, cur_j - 2],
                [cur_i + 1, cur_j - 1],
                [cur_i + 1, cur_j - 2],
                [cur_i + 2, cur_j - 1],
            ]
        elif golam_dir == 2:
            move_dir = [
                [cur_i - 1, cur_j + 1],
                [cur_i, cur_j + 2],
                [cur_i + 1, cur_j + 1],
                [cur_i + 1, cur_j + 2],
                [cur_i + 2, cur_j + 1],
            ]

        return move_dir

    def golam_can_move(self, cur_i, cur_j, golam_dir):
        ret = True

        move_arr = self.golam_move_arr(cur_i, cur_j, golam_dir)

        for move_pos in move_arr:
            move_i, move_j = move_pos
            if move_i < 0 or move_j < 0 or move_i >= self.r + self.margin or move_j >= self.c:
                ret = False
                break
            if self.forest_arr[move_pos[0]][move_pos[1]] != 0:
                ret = False
                break

        return ret

    def add_forest_gol_num(self, cur_i, cur_j, num):
        self.forest_arr[cur_i][cur_j] = num

        for dij in self.exit_dir:
            next_i = cur_i + dij[0]
            next_j = cur_j + dij[1]
            if 0 <= next_i < self.r +self.margin and 0 <= next_j < self.c:
                self.forest_arr[next_i][next_j] = num

    def golam_exit_check(self, cur_i, cur_j, exit_dir, move_dir, golam_num):

        move_exit_dir = exit_dir

        if move_dir == 0:
            move_exit_dir = exit_dir
        elif move_dir == 1:  # 서
            move_exit_dir -= 1
        else:
            move_exit_dir += 1

        move_exit_dir %= 4
        exit_pos_i = cur_i + self.exit_dir[move_exit_dir][0]
        exit_pos_j = cur_j + self.exit_dir[move_exit_dir][1]
        self.forest_arr[exit_pos_i][exit_pos_j] = -golam_num

        return move_exit_dir

    def move_cur_pos(self, cur_i, cur_j, golam_p):
        move_i = None
        move_j = None
        if golam_p == 0:
            move_i = cur_i + 1
            move_j = cur_j
        elif golam_p == 1:
            move_i = cur_i + 1
            move_j = cur_j - 1
        elif golam_p == 2:
            move_i = cur_i + 1
            move_j = cur_j + 1

        return move_i, move_j

    def golam_move(self, golam, golam_num):
        cur_i, cur_j, exit_dir = golam

        for golam_priority in range(3):

            if self.golam_can_move(cur_i, cur_j, golam_priority) == True:
                move_i, move_j = self.move_cur_pos(cur_i, cur_j, golam_priority)

                if self.golam_cent[0] < move_i:
                    self.add_forest_gol_num(cur_i, cur_j, 0)
                    self.add_forest_gol_num(move_i, move_j, golam_num)
                    moved_exit_dir = self.golam_exit_check(move_i, move_j, exit_dir, golam_priority, golam_num)

                    golam = [move_i, move_j, moved_exit_dir]
                    self.golam_cent = [move_i, move_j, moved_exit_dir]
                    self.golam_move(golam, golam_num)

    def golam_check(self, cur_i):
        ret = False
        if cur_i > 1:
            ret = True
        return ret

    def fairy_move(self):

        q = deque([[self.fairy_cent[0],self.fairy_cent[1]]])

        self.visit = [[0] * self.c for _ in range(self.r+self.margin)]

        while(q):
            cur_i,cur_j = q.pop()

            if self.fairy_cent[0] < cur_i:
                self.fairy_cent = [cur_i, cur_j]

            for dij in self.exit_dir:
                next_i = cur_i + dij[0]
                next_j = cur_j + dij[1]



                if 0 <= next_i < self.r +self.margin and 0 <= next_j < self.c:
                    cur_num = self.forest_arr[cur_i][cur_j]

                    if self.visit[next_i][next_j] != 0:
                        continue

                    if cur_num < 0:  # ext_num
                        if self.forest_arr[next_i][next_j] != 0 :
                            q.append([next_i, next_j])
                            self.visit[cur_i][cur_j]=1

                    elif cur_num > 0:
                        if self.forest_arr[next_i][next_j] == cur_num or self.forest_arr[next_i][next_j] == -cur_num:
                            q.append([next_i, next_j])
                            self.visit[cur_i][cur_j] = 1

    def run(self):

        for i, golam in enumerate(self.golam):

            golam_num = i + 1
            self.golam_cent = golam[:]

            self.golam_move(golam, golam_num)

            if self.golam_cent[0] <= 3:
                self.forest_arr = [[0] * self.c for _ in range(self.r + self.margin)]
                continue


            self.fairy_cent = self.golam_cent[:]
            self.fairy_move()
            self.fairy_i_cnt += self.fairy_cent[0] - 2
            #print(self.fairy_i_cnt)
        print(self.fairy_i_cnt)


if __name__ == "__main__":
    mf = CMagicForest()
    mf.input_param()
    mf.run()