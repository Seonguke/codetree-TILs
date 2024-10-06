from collections import deque


class CXmas():
    def __init__(self):
        self.is_dear=1
        self.is_none =2
        self.is_santa =3
        self.n = 0
        self.m = 0
        self.santa_cnt = 0  # p
        self.dear_power = 0
        self.santa_power = 0
        # self.dear_cur_ij = 0
        self.dear_move_dir = [[-1, -1], [-1, 0], [-1, 1],
                              [0, -1], [0, 1],
                              [1, -1], [1, 0], [1, 1]]
        self.santa_move_dir = [[-1, 0],
                               [0, 1],
                               [1, 0],
                               [0, -1]]
        self.santa = {}  # prev_i,prev_j,
        self.dear = []

        self.arr_2d = []
    def input_param(self):

        is_out = False
        is_sleep = 0
        prev_move_dir = None

        self.n, self.m, self.santa_cnt, self.dear_power, self.santa_power = map(int, input().split())
        self.arr_2d = [[None] * self.n for _ in range(self.n)]
        ########dear_input################################
        dear_i, dear_j = map(int, input().split())
        self.dear = [dear_i - 1, dear_j - 1, prev_move_dir]
        self.arr_2d[self.dear[0]][self.dear[1]]=self.dear
        ########santa_input################################
        for k in range(self.santa_cnt):
            santa_num, i, j = map(int, input().split())
            santa = [i - 1, j - 1, prev_move_dir, 0, is_sleep, is_out]
            self.santa[santa_num]=santa
            self.arr_2d[santa[0]][santa[1]] = santa_num
        ########initialize_arr2d

        santa_dict = sorted(self.santa.items(),key= lambda x : x)
        self.santa = dict(santa_dict)

    def array_out_check(self,i,j):
        if 0<=i< self.n and 0<=j<self.n:
            return  True
        else :
            return False
    def distance2d(self, src_i, src_j, dst_i, dst_j):
        dist = (src_i - dst_i) ** 2 + (src_j - dst_j) ** 2
        return dist

    def dear_move(self):

        move_arr = []
        for i, dear_dir in enumerate(self.dear_move_dir):

            next_dear_i = self.dear[0] + dear_dir[0]
            next_dear_j = self.dear[1] + dear_dir[1]
            if self.array_out_check(next_dear_i,next_dear_j) == True:
                for _,santa in self.santa.items():
                    sant_i, sant_j, prev_move_dir, santa_power, is_sleep, is_out = santa
                    if is_out:continue
                    dist = self.distance2d(next_dear_i, next_dear_j, sant_i, sant_j)
                    move_arr.append([dist, sant_i, sant_j, next_dear_i, next_dear_j, i])

        move_arr.sort(key=lambda x: (x[0], -x[1], -x[2]))

        self.arr_2d[self.dear[0]][self.dear[1]] = None
        _, _, _, next_dear_i, next_dear_j, move_dir = move_arr[0]
        self.dear = [next_dear_i, next_dear_j, move_dir]
        if self.arr_2d[next_dear_i][next_dear_j] is not None and self.arr_2d[next_dear_i][next_dear_j] >0:
            self.dear_meet_santa()

        self.arr_2d[self.dear[0]][self.dear[1]] = self.dear
    def check_arr_2d(self,i,j):
        if self.arr_2d[i][j] == None:
            return self.is_none
        elif self.arr_2d[i][j] == self.dear:
            return self.is_dear
        else:
            return self.is_santa
    def dear_meet_santa(self):
        next_dear_i, next_dear_j, move_dir = self.dear
        santa_num = self.arr_2d[next_dear_i][next_dear_j]
        #prev_santa_num = None
        q = deque([[None,santa_num]])

        while(q):
            prev_santa_num,santa_num = q.pop()

            santa = self.santa[santa_num]
            sant_i, sant_j, prev_move_dir, santa_power, is_sleep, is_out = santa

            if prev_santa_num == None:
                santa_power+=self.dear_power

                sant_next_i = sant_i + (self.dear_move_dir[move_dir][0]*self.dear_power)
                sant_next_j = sant_j + (self.dear_move_dir[move_dir][1]*self.dear_power)

                is_sleep=2

                if self.array_out_check(sant_next_i,sant_next_j) == False:
                    is_out = True
                else:
                    is_in = self.check_arr_2d(sant_next_i,sant_next_j)
                    if is_in ==self.is_santa:
                        q.append([santa_num,self.arr_2d[sant_next_i][sant_next_j]])

                santa = [sant_next_i,sant_next_j,prev_move_dir,santa_power,is_sleep,is_out]
                self.santa[santa_num]=santa
                try:
                    self.arr_2d[sant_i][sant_j] = None
                except:
                    a=0
                if is_out == False:
                    self.arr_2d[sant_next_i][sant_next_j] = santa_num
            else:
                #santa_power +=self.santa_power

                sant_next_i = sant_i + self.dear_move_dir[move_dir][0]
                sant_next_j = sant_j + self.dear_move_dir[move_dir][1]

                if self.array_out_check(sant_next_i,sant_next_j) == False:
                    is_out = True
                else:
                    is_in = self.check_arr_2d(sant_next_i,sant_next_j)
                    if is_in ==self.is_santa:
                        q.append([santa_num,self.arr_2d[sant_next_i][sant_next_j]])

                santa = [sant_next_i,sant_next_j,prev_move_dir,santa_power,is_sleep,is_out]
                self.santa[santa_num]=santa
                if self.arr_2d[sant_i][sant_j] == santa_num:
                    self.arr_2d[sant_i][sant_j] = None
                if is_out == False:
                    self.arr_2d[sant_next_i][sant_next_j] = santa_num


    def santa_move(self):
        for santa_num,santa in self.santa.items():
            move_arr = []
            sant_i, sant_j, prev_move_dir, santa_power, is_sleep, is_out = santa
            cur_dist = self.distance2d(sant_i,sant_j,self.dear[0],self.dear[1])
            if is_sleep > 0 or is_out == True:
                continue
            for move_dir,sant_move_dir in enumerate(self.santa_move_dir):
                next_sant_i = sant_i + sant_move_dir[0]
                next_sant_j = sant_j + sant_move_dir[1]
                dist = self.distance2d(next_sant_i,next_sant_j,self.dear[0],self.dear[1])

                if self.array_out_check(next_sant_i, next_sant_j) == True and\
                    self.check_arr_2d(next_sant_i,next_sant_j) !=self.is_santa\
                        and cur_dist > dist:
                    move_arr.append([dist,move_dir,next_sant_i,next_sant_j])

            if move_arr:
                move_arr.sort(key= lambda x : (x[0],x[1]))
                _,move_dir,next_sant_i, next_sant_j = move_arr[0]

                santa = [next_sant_i, next_sant_j, move_dir, santa_power, is_sleep, is_out]
                self.santa[santa_num] = santa
                if self.arr_2d[next_sant_i][next_sant_j] == self.dear:
                    self.santa_meet_deer(santa_num)
                else:
                    self.arr_2d[sant_i][sant_j] = None
                    self.arr_2d[next_sant_i][next_sant_j] = santa_num




    def santa_meet_deer(self,santa_num):

        q = deque([[None, santa_num]])

        while (q):
            prev_santa_num, santa_num = q.pop()

            santa = self.santa[santa_num]
            sant_i, sant_j, prev_move_dir, santa_power, is_sleep, is_out = santa

            if prev_santa_num == None:
                santa_power += self.santa_power
                prev_move_dir = (prev_move_dir+2)%4

                sant_next_i = sant_i + (self.santa_move_dir[prev_move_dir][0]*self.santa_power)
                sant_next_j = sant_j + (self.santa_move_dir[prev_move_dir][1]*self.santa_power)

                if self.array_out_check(sant_next_i, sant_next_j) == False:
                    is_out = True
                else:
                    is_in = self.check_arr_2d(sant_next_i, sant_next_j)
                    if is_in == self.is_santa:
                        q.append([santa_num, self.arr_2d[sant_next_i][sant_next_j]])
                is_sleep = 2
                santa = [sant_next_i, sant_next_j, prev_move_dir, santa_power, is_sleep, is_out]
                self.santa[santa_num] = santa
                if is_out == False:
                    self.arr_2d[sant_next_i][sant_next_j] = santa_num
                self.arr_2d[sant_i + self.santa_move_dir[prev_move_dir][0]][
                    sant_j + self.santa_move_dir[prev_move_dir][1]] = None


            else:

                prev_santa = self.santa[prev_santa_num]
                sant_i, sant_j, prev_dir, prev_santa_power, pre_is_sleep, is_out = prev_santa

                sant_next_i = sant_i + self.santa_move_dir[prev_dir][0]
                sant_next_j = sant_j + self.santa_move_dir[prev_dir][1]

                if self.array_out_check(sant_next_i, sant_next_j) == False:
                    is_out = True
                else:
                    is_in = self.check_arr_2d(sant_next_i, sant_next_j)
                    if is_in == self.is_santa:
                        q.append([santa_num, self.arr_2d[sant_next_i][sant_next_j]])

                santa = [sant_next_i, sant_next_j, prev_move_dir, santa_power, is_sleep, is_out]
                self.santa[santa_num] = santa
                #self.arr_2d[sant_i][sant_j] = None

                if is_out == False:
                    self.arr_2d[sant_next_i][sant_next_j] = santa_num



    def update_is_sleep(self):
        for santa_num, santa in self.santa.items():
            sant_i, sant_j, prev_move_dir, santa_power, is_sleep, is_out = santa
            if is_sleep > 0 :
                is_sleep -=1
            santa = [sant_i, sant_j, prev_move_dir, santa_power, is_sleep, is_out]
            self.santa[santa_num]=santa
    def check_is_over(self):
        cnt = 0
        for santa_num, santa in self.santa.items():
            sant_i, sant_j, prev_move_dir, santa_power, is_sleep, is_out = santa
            if is_out == True:
                cnt+=1

        if cnt == self.santa_cnt :
            return True

        else:
            return False

    def game_start(self):
        for k in range(self.m):
            if k== 6:
                a=0
            self.dear_move()
            self.santa_move()
            self.update_is_sleep()
            if self.check_is_over() == True:
                break
            for santa_num, santa in self.santa.items():
                sant_i, sant_j, prev_move_dir, santa_power, is_sleep, is_out = santa
                if is_out == True :
                    continue
                self.santa[santa_num] = [sant_i, sant_j, prev_move_dir, santa_power+1, is_sleep, is_out]

            # print(f"------------------{k}-----------------")
            # for i in range(self.n):
            #     for j in range(self.n):
            #         print(f"{self.arr_2d[i][j]}", end=' ')
            #     print()
            # for k,v in self.santa.items():
            #     print(f"{k}:{v[3]}/ nuck_down {v[4]}")

        for santa_num, santa in self.santa.items():
            sant_i, sant_j, prev_move_dir, santa_power, is_sleep, is_out = santa
            print(santa_power,end=' ')


if __name__ == "__main__":
    xmas = CXmas()
    xmas.input_param()
    xmas.game_start()