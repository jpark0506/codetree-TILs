n = int(input())
data = [list(data)for _ in range(n)]
max_coin = 0
def check(coor):
    cnt_coin = 0
    x,y = coor[0],coor[1]
    if x+2<n and y+2 <n:
        for i in range(0,3):
            for j in range(0,3):
                if data[i][j] == 1:
                    cnt_coin += 1
    if max_coin < cnt_coin:
        max_coin = cnt_coin
print(cnt_coin)