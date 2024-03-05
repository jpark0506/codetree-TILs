n,m = map(int,input().split())

data = [list(map(int,input().split())) for i in range(n)]

direction = [[0,1],[0,-1],[1,0],[-1,0]]
selections = []
max_sum = 0

def check_range(x,y):
    global n,m
    if 0 <= x < m and 0 <= y < n:
        return True
    else:
        return False

def check_sum(ref_coor, dir_coor1, dir_coor2):

    global data

    rx, ry = ref_coor[0],ref_coor[1]
    dx1, dy1 = dir_coor1[0],dir_coor1[1]
    dx2, dy2 = dir_coor2[0],dir_coor2[1]
    temp_sum = data[ry][rx] + data[ry+dy1][rx+dx1] + data[ry+dy2][rx+dx2]

    return temp_sum

for i in range(4):
    for j in range(4):
        if i != j:
            selections.append([i,j])

for sel_index1, sel_index2 in selections:

    for y in range(n):
        for x in range(m):

            sel_dir1_x, sel_dir1_y = direction[sel_index1][0],direction[sel_index1][1]
            sel_dir2_x, sel_dir2_y = direction[sel_index2][0],direction[sel_index2][1]

            if check_range(x+sel_dir1_x, y+sel_dir1_y) == True and check_range(x+sel_dir2_x, y+sel_dir2_y) == True:
                temp_sum = check_sum([x,y], [sel_dir1_x,sel_dir1_y], [sel_dir2_x,sel_dir2_y])
                if max_sum < temp_sum :
                    
                    max_sum = temp_sum
print(max_sum)