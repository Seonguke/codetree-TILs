from collections import deque


class CRotate():
    def __init__(self):
        self.k = 0  # 탐사
        self.m = 0  # 유물
        self.n = 5
        self.cent = 5 // 2
        self.arr_2d = []
        self.visit = None
        self.arr_1d = None
        self.move_dir = [[-1, 0],
                         [0, 1],
                         [1, 0],
                         [0, -1]]
        self.rot_degree = [2, 4, 6]  # 90, 180, 270
        self.rot_q_idx = [[-1, -1], [-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1]]

        self.rot_priority = [[-1 + self.cent, -1 + self.cent], [-1 + self.cent, 0 + self.cent],
                             [-1 + self.cent, 1 + self.cent],
                             [0 + self.cent, -1 + self.cent], [self.cent, self.cent], [0 + self.cent, 1 + self.cent],
                             [-1 + self.cent, -1 + self.cent], [-1 + self.cent, 0 + self.cent],
                             [-1 + self.cent, 1 + self.cent]]

    def input_param(self):
        self.k, self.m = map(int, input().split())

        for i in range(self.n):
            input_arr = list(map(int, input().split()))
            self.arr_2d.append(input_arr)

        self.arr_1d = list(map(int, input().split()))

    def get_rot_arr(self, temp_arr, cent_i, cent_j, rot_degree):
        arr = []
        for rot_q_idx in self.rot_q_idx:
            arr.append(temp_arr[cent_i + rot_q_idx[0]][cent_j + rot_q_idx[1]])
        rot_q = deque(arr)
        rot_q.rotate(rot_degree)

        for i, rot_q_idx in enumerate(self.rot_q_idx):
            temp_arr[cent_i + rot_q_idx[0]][cent_j + rot_q_idx[1]] = rot_q.popleft()

    def find_max_precious(self):
        q = deque(self.rot_priority)

        result_arr = []
        while (q):
            rt_cent_i, rt_cent_j = q.pop()
            for rot_degree in self.rot_degree:
                roate_arr = [arr[:] for arr in self.arr_2d]
                self.get_rot_arr(roate_arr, rt_cent_i, rt_cent_j, rot_degree)

                pos_arr = self.find_treasure(roate_arr)
                result_arr.append([len(pos_arr),rot_degree,rt_cent_i,rt_cent_j])

        return result_arr

    def find_same_num(self, cur_i, cur_j, visit,roate_arr,arr_pos):

        q = deque([[cur_i, cur_j]])

        visit[cur_i][cur_j] = roate_arr[cur_i][cur_j]

        while (q):
            c_i, c_j = q.pop()

            arr_pos.append([c_i, c_j])
            for next_ij in self.move_dir:
                n_i = c_i + next_ij[0]
                n_j = c_j + next_ij[1]

                if 0 <= n_i < self.n and 0 <= n_j < self.n and\
                    visit[n_i][n_j] is None and roate_arr[c_i][c_j] == roate_arr[n_i][n_j]:
                        q.append([n_i,n_j])
                        visit[n_i][n_j] = roate_arr[n_i][n_j]

    def find_treasure(self, roate_arr):
        visit = [[None] * self.n for _ in range(self.n)]

        #sum_treasure=0
        pos_arr = []

        for i in range(self.n):
            for j in range(self.n):
                if visit[i][j] is None and roate_arr[i][j] is not None:
                    arr_pos = []
                    self.find_same_num(i, j, visit, roate_arr, arr_pos)

                    if len(arr_pos) >= 3:

                        pos_arr.extend(arr_pos)

        return pos_arr
    def real_rotate(self,rot_degree,cent_i,cent_j):
        self.get_rot_arr(self.arr_2d, cent_i, cent_j, rot_degree)
        for i, rot_q_idx in enumerate(self.rot_q_idx):
            self.arr_2d[cent_i + rot_q_idx[0]][cent_j + rot_q_idx[1]] = None
    def run(self):

        treasure_q = deque(self.arr_1d)
        for k in range(self.k):
            treasure_num = 0
            result_arr=self.find_max_precious()
            if result_arr :
                result_arr.sort(key=lambda x: (-x[0], x[1], x[3], x[2]))
                treasure,rot_degree,cent_i,cent_j = result_arr[0]
                #treasure_num+=treasure
                if treasure <1 : break
                self.get_rot_arr(self.arr_2d, cent_i, cent_j, rot_degree)

                while(True):
                    pos_arr = self.find_treasure(self.arr_2d)
                    if pos_arr :
                        treasure_num+=len(pos_arr)
                        pos_arr.sort(key=lambda x: (x[1], -x[0]))

                        for i, pos in enumerate(pos_arr):
                            if treasure_q:
                                self.arr_2d[pos[0]][pos[1]] = treasure_q.popleft()
                            else :
                                self.arr_2d[pos[0]][pos[1]] = None
                    else:
                        break
            else:
                break

            print(treasure_num)
            # pos_arr.sort(key=lambda x:(x[1],-x[0]))
            # if no empty_arr : break
            # self.fiil_empty_arr


if __name__ == "__main__":
    cRot = CRotate()
    cRot.input_param()
    cRot.run()