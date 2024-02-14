n = int(input())
data = [list(map(int,input().split())) for _ in range(n)]
max_coin = 0
def check(coor):
    global max_coin
    cnt_coin = 0
    x,y = coor[0],coor[1]
    if x+2<n and y+2 < n:
        for i in range(0,3):
            for j in range(0,3):
                if data[x+i][y+j] == 1:
                    cnt_coin += 1
    if max_coin < cnt_coin:
        max_coin = cnt_coin
for i in range(n):
    for j in range(n):
        check([i,j])
print(max_coin)