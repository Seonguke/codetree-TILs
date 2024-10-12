from collections import deque
#((self.board[next_i][next_j] -self.board[start_i][start_j])==1 or\
#                                                 (self.board[next_i][next_j] -self.board[start_i][start_j])==0 ):
# dfs
# 걍 sorting이었음
class cTail():
    def __init__(self):
        self.plus = -9
        self.minus = -8

        self.n = 0  # 3 ≤ n ≤ 20
        self.m = 0  # 1 ≤ m ≤ 5
        self.k = 0  # 1 ≤ k ≤ 1000

        self.board = []
        self.ball_move = [[0, 1], [-1, 0], [0, -1], [1, 0]]
        self.people_move = [[0,1],[1,0],[0,-1],[-1,0]]
        # 0은 빈칸, 1은 머리사람, 2는 머리사람과 꼬리사람이 아닌 나머지, 3은 꼬리사람, 4
        self.team_tail = []
        self.team_head = []
        self.team_hit = []
        self.team_point = []
        self.team_arr = []
        self.team_pos = []

    def input_param(self):
        self.n, self.m, self.k = map(int, input().split())
        for i in range(self.n):
            arr = list(map(int, input().split()))
            self.board.append(arr)
        for k in range(self.m):
            self.team_hit.append(0)
            self.team_point.append(0)
    def update_ball_idx(self, round):
        start_i, start_j = 0, 0
        rot_idx = (round // (self.n)) % 4
        plus_minu = 0
        if rot_idx == 0:
            start_i = round % self.n
            plus_minu = self.plus
        elif rot_idx == 1:
            start_j = round % self.n
            plus_minu = self.minus
            start_i = (self.n - 1)
        elif rot_idx == 2:
            start_i = (self.n - 1) - round % self.n
            start_j = (self.n - 1)
            plus_minu = self.minus
        elif rot_idx == 3:

            start_j = (self.n - 1) - round % self.n
            plus_minu = self.plus

        return start_i, start_j, rot_idx, plus_minu

    def check_ball(self, round):
        start_i, start_j, dir, plus_minu = self.update_ball_idx(round)
        for k in range(self.n):
            next_i = start_i + (k * self.ball_move[dir][0])
            next_j = start_j + (k * self.ball_move[dir][1])

            # TODO cehck poepm
            #self.board[next_i][next_j] = round
            for team_idx ,team in enumerate(self.team_arr):
                if self.team_hit[team_idx] == 1 : continue
                for k, [p_idx,p_i,p_j] in enumerate(team):
                    if next_i == p_i and next_j == p_j and p_idx !=4:
                        self.team_point[team_idx] = (k+1)**2
                        self.team_hit[team_idx] = 1



    def print_arr(self):
        for i in range(self.n):
            for j in range(self.n):
                print(self.board[i][j], end=' ')
            print()

    def find_team(self):
        visit = [[0] * self.n for _ in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                if self.board[i][j]==1 and visit[i][j]==0:
                    self.update_team(i, j, visit,None)

    def update_team(self, cur_i, cur_j, visit,team_idx):
        #tail = [[self.board[cur_i][cur_j], cur_i, cur_j]]
        tail= []
        visit[cur_i][cur_j] = -1
        q = deque([[cur_i, cur_j]])
        while(q):
            start_i,start_j = q.pop()

            if self.board[start_i][start_j] == 1:
                self.team_head.append([start_i,start_j])
            elif self.board[start_i][start_j] == 3:
                self.team_tail.append([start_i,start_j])

            tail.append([self.board[start_i][start_j],start_i,start_j])
            for dir in self.people_move:
                next_i = start_i + dir[0]
                next_j = start_j + dir[1]
                if not(0<=next_i<self.n and 0<=next_j<self.n): continue
                if visit[next_i][next_j]==0 and ((self.board[next_i][next_j] -self.board[start_i][start_j])==1 or\
                                                 (self.board[next_i][next_j] -self.board[start_i][start_j])==0 ):
                    q.append([next_i,next_j])
                    visit[next_i][next_j]= -1
        team_q = deque(tail)
        while(team_q):
            k,i,j = team_q.popleft()
            if k == 1:
                team_q.appendleft([k,i,j])
                break
            else:
                team_q.append([k,i,j])
        team = list(team_q)
        if team_idx is None :
            self.team_arr.append(team)
        else:
            self.team_arr[team_idx] = team
    def move_team(self):
        for team_idx ,team in enumerate(self.team_arr):
            people = [t[0] for t in team]
            pos = [[t[1],t[2]] for t in team]
            people_q = deque(people)

            people_q.rotate(-1)
            team_arr= [ ]
            for p_idx,p_pos in zip(people_q,pos):
                arr = [p_idx]
                arr.extend(p_pos)
                team_arr.append(arr)
                if p_idx == 1:
                    self.team_head[team_idx] = p_pos
                elif p_idx ==3:
                    self.team_tail[team_idx] = p_pos

            team_q = deque(team_arr)
            while (team_arr):
                k, i, j = team_q.popleft()
                if k == 1:
                    team_q.appendleft([k, i, j])
                    break
                else:
                    team_q.append([k, i, j])

            self.team_arr[team_idx] = list(team_q)
            for k,i,j in self.team_arr[team_idx]:
                self.board[i][j]=k


    def change_head_tail(self):
        for team_idx ,team in enumerate(self.team_arr):
            if self.team_hit[team_idx] ==0 : continue
            temp_head = self.team_head[team_idx]
            temp_tail = self.team_tail[team_idx]
            self.board[temp_head[0]][temp_head[1]] = 3
            self.board[temp_tail[0]][temp_tail[1]] = 1
            visit = [[0] * self.n for _ in range(self.n)]
            self.update_team(temp_tail[0], temp_tail[1], visit,team_idx)
            self.team_hit[team_idx]=0

    def play(self):
        self.find_team()
        for round in range(self.k):
            if round % self.n == 0:
                a = 0

            # print(f"------{round}-------")
            self.move_team()
            self.check_ball(round)
            self.change_head_tail()
            #self.print_arr()
        count =0
        for point in self.team_point:
            count+=point
        print(count)


if __name__ == "__main__":
    tail = cTail()
    tail.input_param()
    tail.play()