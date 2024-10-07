from collections import deque


class Cking_order():
    def __init__(self):
        self.EMPTY = 0
        self.DUT = 1
        self.WALL = 2
        # 0 : 빈칸, 1 : 함정 , 2 : 벽
        self.move_direct = [[-1, 0], [0, 1], [1, 0], [0, -1]]
        # d는 0, 1, 2, 3 중에 하나이며 각각 위쪽, 오른쪽, 아래쪽, 왼쪽
        self.order = []
        self.knight = {}
        self.board = []
        self.board_knight = []
        self.knight_heart = {}
        self.knight_damage = {}

    def input_param(self):
        self.board_size, self.knight_cnt, self.order_cnt = map(int, input().split())
        # (r,c)를 좌측 상단 꼭지점으로 하며 세로 길이가 h, 가로 길이가 w인 직사각형 초기 체력이 k
        # l LxL n knight_cnt
        for i in range(self.board_size):
            self.board.append(list(map(int, input().split())))

        for i in range(self.knight_cnt):
            r, c, h, w, k = map(int, input().split())
            knight_num = 41 + i
            self.knight[knight_num]=[r - 1, c - 1, h, w]
            self.knight_heart[knight_num]=k
            self.knight_damage[knight_num]=0

        for _ in range(self.order_cnt):
            king_num, d = map(int, input().split())
            self.order.append([king_num + 40, d])

        self.board_knight =[[0]*self.board_size for _ in range(self.board_size)]
        for knight_num,knight in self.knight.items():
            self.draw_rectangle(knight_num,knight,self.board_knight)
    def draw_rectangle(self,knight_num,knight,board):
        r, c, h, w =knight
        for i in range(h):
            for j in range(w):
                board[r+i][c+j]=knight_num
    def can_move(self, knight_num, d):

        q = deque([knight_num])
        Ret = True

        cur_i,cur_j,h,w = self.knight[knight_num]
        move_list = []
        while (q):
            cur_knight_num = q.pop()
            cur_i,cur_j,h,w = self.knight[cur_knight_num]
            next_i = self.move_direct[d][0] + cur_i
            next_j = self.move_direct[d][1] + cur_j

            move_list.append(cur_knight_num)
            if (0 <= next_i < self.board_size and 0 <= next_j < self.board_size):
                for i in range(h):
                    for j in range(w):
                        if (self.board_knight[next_i + i][next_j + j] != cur_knight_num and self.board_knight[next_i + i][next_j + j] != 0):
                            q.append(self.board_knight[next_i + i][next_j + j])
                        elif (self.board[next_i + i][next_j + j] == self.WALL):
                            Ret = False
                            break
            else:
                Ret = False
                break

        return Ret,move_list

    def move_knight(self,move_list,d):
        move_list =move_list[::-1]

        for knight_num in move_list:
            cur_i, cur_j, h, w = self.knight[knight_num]
            self.board_knight[cur_i][cur_j]=0
            self.draw_rectangle(0,self.knight[knight_num],self.board_knight)
            next_i = self.move_direct[d][0] + cur_i
            next_j = self.move_direct[d][1] + cur_j
            self.knight[knight_num] = [next_i,next_j,h,w]
            self.draw_rectangle(knight_num, self.knight[knight_num], self.board_knight)

    def check_damage(self,attack_num,move_list):
        for i in range(self.board_size):
            for j in range(self.board_size):
                knight_num = self.board_knight[i][j]
                board_num = self.board[i][j]
                if knight_num != attack_num and knight_num in move_list:
                    if board_num == self.DUT and \
                            knight_num>0 and\
                            (self.knight_heart[knight_num]-self.knight_damage[knight_num]) >0:
                        self.knight_damage[knight_num]+=1



    def knight_move(self):

        for knight_num, d in self.order:
            # 체스판에서 사라진 기사에게 명령을 내리면 아무런 반응이 없게
            if self.knight_heart[knight_num] - self.knight_damage[knight_num] <= 0:
                continue
            ret,move_list= self.can_move(knight_num,d)
            if ret == False:
                continue
            else:
                move_list = list(dict.fromkeys(move_list))
                self.move_knight(move_list,d)
                self.check_damage(knight_num,move_list)
        cnt =0
        for k,v in self.knight_damage.items():
            if (self.knight_heart[k]-v)>0:
                cnt+=v
        print(cnt)


if __name__ == "__main__":
    king = Cking_order()
    king.input_param()
    king.knight_move()