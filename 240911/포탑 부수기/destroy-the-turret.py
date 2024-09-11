from collections import deque
class Tower():
    power = 0
    is_target = False
    is_side_target = False
    attacker = False
    sum_of_row_col = 0
    col = 0
    attack_k = 0
    cur_pos = None


class Action():
    def __init__(self):
        self.K = 0
        self.N = 0
        self.M = 0
        self.tower_arr = []
        self.dircetion_priority = [[0, 1], [-1, 0], [1, 0], [0, -1]]  # 우/하/상/좌
        self.bomb_pos = [[-1, -1], [-1, 0], [-1, 1],
                         [0, -1], [0, 0], [0, 1],
                         [1, -1], [1, 0], [1, 1]]
        self.attacker_idx = [-1, -1]
        self.target_idx = [-1, -1]

    def init_param(self):
        self.N, self.M, self.K = map(int, input().split())

    def initialize_tower(self):
        for i in range(self.N):
            row_tower = []
            power_arr = list(map(int, input().split()))
            for j in range(self.M):
                cTower = Tower()
                cTower.power = power_arr[j]
                cTower.sum_of_row_col = i + j + 2
                cTower.col = i + 1
                cTower.cur_pos = [i, j]
                row_tower.append(cTower)
            self.tower_arr.append(row_tower)

    def print_tower_arr(self):
        print()
        for i in range(self.N):
            for j in range(self.M):
                print(f'{self.tower_arr[i][j].power}', end=' ')
            print('')

    def find_low_power_tower(self):
        tmp_tower = Tower()
        tmp_tower.power = 5001
        tmp_tower.sum_of_row_col = -1
        tmp_tower.col = -1
        for i in range(self.N):
            for j in range(self.M):

                cur_tower = self.tower_arr[i][j]

                if cur_tower.power == 0: continue

                if tmp_tower.power > cur_tower.power:
                    tmp_tower = cur_tower
                elif tmp_tower.power == cur_tower.power:
                    if tmp_tower.attack_k < cur_tower.attack_k:
                        tmp_tower = cur_tower
                    elif tmp_tower.attack_k == cur_tower.attack_k:
                        if tmp_tower.sum_of_row_col < cur_tower.sum_of_row_col:
                            tmp_tower = cur_tower
                        elif tmp_tower.sum_of_row_col == cur_tower.sum_of_row_col:
                            if tmp_tower.col < cur_tower.col:
                                tmp_tower = cur_tower

        self.attacker_idx = tmp_tower.cur_pos

    def find_high_power_tower(self):
        tmp_tower = Tower()
        tmp_tower.power = -1
        tmp_tower.sum_of_row_col = self.N + self.M + 3
        tmp_tower.col = self.N + 2
        for i in range(self.N):
            for j in range(self.M):

                cur_tower = self.tower_arr[i][j]

                if cur_tower.power == 0: continue

                if tmp_tower.power < cur_tower.power:
                    tmp_tower = cur_tower
                elif tmp_tower.power == cur_tower.power:
                    if tmp_tower.attack_k > cur_tower.attack_k:
                        tmp_tower = cur_tower
                    elif tmp_tower.attack_k == cur_tower.attack_k:
                        if tmp_tower.sum_of_row_col > cur_tower.sum_of_row_col:
                            tmp_tower = cur_tower
                        elif tmp_tower.sum_of_row_col == cur_tower.sum_of_row_col:
                            if tmp_tower.col > cur_tower.col:
                                tmp_tower = cur_tower

        self.target_idx = tmp_tower.cur_pos

    def attack(self, time):

        attacker_i, attacker_j = self.attacker_idx
        target_i, target_j = self.target_idx

        self.tower_arr[attacker_i][attacker_j].attack_k = time +1
        self.tower_arr[attacker_i][attacker_j].attacker = True
        self.tower_arr[attacker_i][attacker_j].power += self.N + self.M

        self.tower_arr[target_i][target_j].is_target = True
        #elf.tower_arr[target_i][target_j].power -= self.tower_arr[attacker_i][attacker_j].power

        if not self.attack_laser():
            self.attack_bomb()

    def attack_laser(self):
        #TODO 다시
        attacker_i, attacker_j = self.attacker_idx

        ret_q = self.bfs(attacker_i, attacker_j)

        if ret_q:
            for side in ret_q:
                side_i,side_j = side
                if self.tower_arr[side_i][side_j].is_target==True:
                    self.tower_arr[side_i][side_j].power -= self.tower_arr[attacker_i][attacker_j].power
                else:

                    self.tower_arr[side_i][side_j].is_side_target=True
                    self.tower_arr[side_i][side_j].power -= self.tower_arr[attacker_i][attacker_j].power // 2
            return True
        else:
            return False

    def bfs(self, attacker_i, attacker_j):
        q = deque([])
        q.append([attacker_i, attacker_j,[]])
        visist = [[False]*self.M for _ in range(self.N)]
        visist[attacker_i][attacker_j]= True
        routess = []
        while (q):
            cur_i, cur_j,route = q.popleft()
            for i in range(4):
                di, dj = self.dircetion_priority[i]
                next_i = (cur_i + di) % self.N #범위 반대 공격
                next_j = (cur_j + dj) % self.M #
                if self.tower_arr[next_i][next_j].power == 0 or visist[next_i][next_j]: continue
                if self.tower_arr[next_i][next_j].is_target == True:
                    route.append([next_i,next_j])
                    return  route[:]

                qrotes = route[:]
                qrotes.append([next_i,next_j])
                visist[next_i][next_j] = True
                q.append([next_i,next_j,qrotes])

        return routess

    def attack_bomb(self):
        attacker_i, attacker_j = self.attacker_idx
        target_i, target_j = self.target_idx
        #TODO 다시
        for di, dj in self.bomb_pos:
            next_i = (di + target_i) % self.N
            next_j = (dj + target_j) % self.M

            if next_i == attacker_i and next_j == attacker_j:continue
            if next_i == target_i and next_j == target_j:
                self.tower_arr[next_i][next_j].power -= self.tower_arr[attacker_i][attacker_j].power
                continue
            if self.tower_arr[next_i][next_j].power==0:continue
            self.tower_arr[next_i][next_j].power -= self.tower_arr[attacker_i][attacker_j].power//2
            self.tower_arr[next_i][next_j].is_side_target =True

    def heal_tower(self):

        for i in range(self.N):
            for j in range(self.M):
                if self.tower_arr[i][j].is_target or self.tower_arr[i][j].is_side_target \
                    or self.tower_arr[i][j].attacker :
                    self.tower_arr[i][j].is_target = False
                    self.tower_arr[i][j].attacker = False
                    self.tower_arr[i][j].is_side_target = False

                else:
                    if self.tower_arr[i][j].power> 0  :
                        self.tower_arr[i][j].power +=1
                if self.tower_arr[i][j].power < 0:
                    self.tower_arr[i][j].power=0
    def print_max_tower(self):
        max_power = -1
        for i in range(self.N):
            for j in range(self.M):
                if self.tower_arr[i][j].power> 0  :
                    max_power =max(max_power,self.tower_arr[i][j].power)
        print(max_power)

    def check_tower(self):
        cnt = 0
        for i in range(self.N):
            for j in range(self.M):
                if self.tower_arr[i][j].power > 0:
                    cnt+=1

        if cnt <2: return False
        else: return
    def play(self):
        for i in range(self.K):
            if self.check_tower() == False : break
            #if i==36:
            #    a=0
            #print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
            #print(i)
            self.find_low_power_tower()
            self.find_high_power_tower()
            self.attack(i)
            self.heal_tower()


            #self.print_tower_arr()
            #print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
        self.print_max_tower()




if __name__ == "__main__":
    cAction = Action()
    cAction.init_param()
    cAction.initialize_tower()
    #cAction.print_tower_arr()
    cAction.play()