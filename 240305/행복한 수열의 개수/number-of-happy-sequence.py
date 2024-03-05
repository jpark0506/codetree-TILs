n,m = map(int,input().split())
data = [list(map(int,input().split())) for i in range(n)]
happy_arr = 0
#m이 행복함의 기준
for i in range(n):
    ref_x = data[i][0]
    cnt_x = 1
    for j in range(1,n):
        if data[i][j] != ref_x:
            ref_x = data[i][j]
            cnt_x = 1
        else:
            cnt_x += 1
            if cnt_x == m :
                happy_arr += 1
                break
       
for i in range(n):
    ref_y = data[0][i]
    cnt_y = 1
    for j in range(1,n):
        if data[j][i] != ref_y:
            ref_y = data[j][i]
            cnt_y = 1
        else:
            cnt_y += 1
            if cnt_y == m:
                happy_arr += 1
                break
print(happy_arr)