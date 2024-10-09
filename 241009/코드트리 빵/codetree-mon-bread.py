from collections import deque


class CBread():
    def __init__(self):
        self.n = 0
        self.m = 0
        self.WALL = -1

        self.board = []
        self.move_dir = [[-1, 0],  # ↑
                         [0, -1],  # ←,
                         [0, 1],  # →
                         [1, 0]]  # ↓
        self.margin = 30
        self.home_arr = []
        self.person_store = {}
        self.person = {}  # 31~
        self.person_state = {}  # is_arrived?

    def input_param(self):
        self.n, self.m = map(int, input().split())
        for i in range(self.n):
            arr = list(map(int, input().split()))
            self.board.append(arr)
            for j in range(self.n):
                if arr[j] == 1:
                    self.home_arr.append([i, j])

        for k in range(1, self.m + 1):
            i, j = map(int, input().split())
            self.person[k + self.margin] = None
            self.person_store[k + self.margin] = [i - 1, j - 1]
            self.person_state[k + self.margin] = False

    def move(self, end_idx):
        for person_idx in self.person.keys():
            if person_idx >end_idx : continue
            if self.person[person_idx] is None : continue
            if self.person_state[person_idx]==True : continue

            start_i, start_j = self.person[person_idx]
            dst_i, dst_j = self.person_store[person_idx]

            #print(f"idx : {person_idx}")
            if person_idx == 57:
                b=0
            visit = [arr[:] for arr in self.board]
            q = deque([[start_i, start_j, []]])
            move_dir= -1
            while q:
                cur_i, cur_j, cur_arr = q.popleft()
                if cur_i == dst_i and cur_j == dst_j:
                    move_dir = cur_arr[0]
                    break

                for i,dir in enumerate(self.move_dir):
                    next_i = cur_i + dir[0]
                    next_j = cur_j + dir[1]
                    if not (0 <= next_i < self.n and 0 <= next_j < self.n): continue
                    if 0<=visit[next_i][next_j]<=1:
                        q.append([next_i,next_j,cur_arr+[i]])
                        visit[next_i][next_j]=999

            move_i = start_i + self.move_dir[move_dir][0]
            move_j = start_j + self.move_dir[move_dir][1]

            self.person[person_idx] = [move_i,move_j]
            if move_i == dst_i and move_j == dst_j:
                self.board[move_i][move_j]=-1
                self.person_state[person_idx]=True

    def arrive_check(self):
        cnt = len(self.person_state)
        for k, v in self.person_state.items():
            if v == True:
                cnt -= 1
        if cnt == 0:
            return True
        else:
            return False

    def start_at_home(self, time):
        person_max =max(self.person.keys())
        if person_max < time:return

        start_i, start_j = self.person_store[time]
        cnt = 2
        home_arr = []
        q = deque([[start_i, start_j, cnt]])
        visit = [arr[:] for arr in self.board]
        visit[start_i][start_j] = cnt
        while q:
            cur_i, cur_j, cur_cnt = q.popleft()

            if self.board[cur_i][cur_j] == 1:
                home_arr.append([cur_cnt, cur_i, cur_j])

            for dir in self.move_dir:
                next_i = cur_i + dir[0]
                next_j = cur_j + dir[1]
                if not (0 <= next_i < self.n and 0 <= next_j < self.n): continue
                if 0 <= visit[next_i][next_j] <= 1:
                    visit[next_i][next_j] = cur_cnt + 1
                    q.append([next_i, next_j, cur_cnt + 1])

        home_arr.sort(key=lambda x: (x[0], x[1], x[2]))
        _, dst_i, dst_j = home_arr[0]
        self.person[time] = [dst_i,dst_j]
        self.board[dst_i][dst_j] = self.WALL

    def run(self):
        time = 1
        while True:
            if time == 28:
                a = 0
            #rint(time)
            self.move(time + self.margin)
            if self.arrive_check() == True:
                break
            self.start_at_home(time + self.margin)
            time += 1

        print(time)


if __name__ == "__main__":
    bread = CBread()
    bread.input_param()
    bread.run()