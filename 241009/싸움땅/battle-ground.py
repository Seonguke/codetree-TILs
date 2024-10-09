class CGunner():
    def __init__(self):
        self.n = 0
        self.m = 0
        self.k = 0
        self.move_dir = [[-1, 0], [0, 1], [1, 0], [0, -1]]
        self.player = {}
        self.board = []
        self.board_player = []
        self.point = {}

    def input_param(self):
        self.n, self.m, self.k = map(int, input().split())
        self.board = [[[0]] * self.n for _ in range(self.n)]
        for i in range(self.n):
            arr = list(map(int, input().split()))

            for j in range(self.n):
                self.board[i][j] = [arr[j]]
        self.board_player = [[None] * self.n for _ in range(self.n)]

        for k in range(self.m):
            i, j, d, s = map(int, input().split())
            self.player[k] = [i - 1, j - 1, d, s, 0]
            self.board_player[i - 1][j - 1] = k
            self.point[k] = 0

    def move_check(self, i, j):
        ret = True
        if not (0 <= i < self.n and 0 <= j < self.n):
            ret = False
        return ret

    def get_next_move(self, i, j, d):
        next_i = i + self.move_dir[d][0]
        next_j = j + self.move_dir[d][1]
        return next_i, next_j

    def get_board_gun_max(self, i, j):
        self.board[i][j].sort()
        board_gun = self.board[i][j].pop()
        return board_gun

    def get_fight(self, cur_player, fight_player):
        winner = -1
        loser = -1
        _, _, _, init_power, gun = self.player[cur_player]
        _, _, _, counter_init_power, counter_gun = self.player[fight_player]
        counter_sum = counter_init_power + counter_gun
        cur_sum = init_power + gun
        if cur_sum == counter_sum:
            if init_power > counter_init_power:  # 수치가 같은 경우에는 플레이어의 초기 능력치가 높은 플레이어가 승리
                winner = cur_player
                loser = fight_player
            else:
                winner = fight_player
                loser = cur_player
        elif cur_sum > counter_sum:  # 초기 능력치와 가지고 있는 총의 공격력의 합을 비교하여 더 큰 플레이어가 이기
            winner = cur_player
            loser = fight_player
        else:
            winner = fight_player
            loser = cur_player
        point = abs(cur_sum - counter_sum)
        self.point[winner] += point
        return winner, loser

    def loser_act(self, idx):
        loser_i, loser_j, d, init_power, gun = self.player[idx]
        self.board[loser_i][loser_j].append(gun)
        gun = 0
        for i in range(4):
            d = (d + i) % 4
            next_i, next_j = self.get_next_move(loser_i, loser_j, d)
            if self.move_check(next_i,
                               next_j) == False: continue  # (조건)만약 해당 방향으로 나갈 때 격자를 벗어나는 경우에는 정반대 방향으로 방향을 바꾸어서 1만큼 이동
            if self.board_player[next_i][next_j] is not None:
                continue
            self.board_player[loser_i][loser_j] = None
            self.board_player[next_i][next_j] = idx
            board_gun = self.get_board_gun_max(next_i, next_j)
            if board_gun > gun:
                self.board[next_i][next_j].append(gun)
                gun = board_gun
            else:
                self.board[next_i][next_j].append(board_gun)
            self.player[idx] = [next_i, next_j, d, init_power, gun]
            break

    def winner_act(self, idx):
        winner_i, winner_j, d, init_power, gun = self.player[idx]
        board_gun = self.get_board_gun_max(winner_i, winner_j)
        if board_gun > gun:
            self.board[winner_i][winner_j].append(gun)
            gun = board_gun
        else:
            self.board[winner_i][winner_j].append(board_gun)
        self.board_player[winner_i][winner_j] = idx

        self.player[idx] = [winner_i, winner_j, d, init_power, gun]

    def move_player(self):
        for k, v in self.player.items():
            cur_i, cur_j, d, init_power, gun = v
            d_d = d
            self.board_player[cur_i][cur_j] = None
            next_i, next_j = self.get_next_move(cur_i, cur_j, d)
            if self.move_check(next_i, next_j) == False:  # (조건)만약 해당 방향으로 나갈 때 격자를 벗어나는 경우에는 정반대 방향으로 방향을 바꾸어서 1만큼 이동
                d = (d + 2) % 4

                next_i, next_j = self.get_next_move(cur_i, cur_j, d)
            if self.board_player[next_i][next_j] is None:  # (조건)만약 이동한 방향에 플레이어가 없다면 해당 칸에 총이 있는지 확인
                board_gun = self.get_board_gun_max(next_i, next_j)
                if board_gun > gun:  # (조건) 총이 있는 경우, 해당 플레이어는 총을 획득
                    self.board[next_i][next_j].append(gun)  # (중요)  더 쎈 총을 획득하고, 나머지 총들은 해당 격자에 둡
                    gun = board_gun
                else:
                    self.board[next_i][next_j].append(board_gun)
                self.board_player[next_i][next_j] = k
                self.player[k] = [next_i, next_j, d, init_power, gun]
            else:  # 만약 이동한 방향에 플레이어가 있는 경우에는 두 플레이어가 싸움
                counter_idx = self.board_player[next_i][next_j]
                winner, loser = self.get_fight(k, counter_idx)
                self.player[k] = [next_i, next_j, d, init_power, gun]
                self.loser_act(loser)
                self.winner_act(winner)

    def play(self):
        for round in range(self.k):
            self.move_player()

        for v in self.point.values():
            print(v, end=' ')


if __name__ == "__main__":
    gunner = CGunner()
    gunner.input_param()
    gunner.play()