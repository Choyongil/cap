import numpy as np
import cv2


point_list = [] # 마우스로 찍은 위치의 좌표값 넣을 배열
point_list2 = []
i = 0

def mouse_callback(event, x, y, flags, param):
    global point_list, point_list2, img_original, i


    # 마우스 왼쪽 버튼 누를 때마다 좌표를 리스트에 저장
    if event == cv2.EVENT_LBUTTONDOWN:
        print('i :', i)
        if i < 4:
            print("(%d, %d)" % (x, y))
            point_list.append((x, y))
            i = i + 1
            cv2.circle(img_original, (x, y), 0, (0, 0, 0), 0)
            print(point_list)
        elif i == 4:
            point_list2.append((x, y))
            print("2 : (%d, %d)" % (x, y))
            cv2.circle(img_original, (x, y), 2, (0, 0, 255), -1)
            print(point_list2)
            i = i + 1
        elif i == 5:
            point_list2.append((x, y))
            print("2 : (%d, %d)" % (x, y))
            cv2.circle(img_original, (x, y), 2, (255, 0, 0), -1)
            print(point_list2)
            i = i + 1
        elif i == 6:
            point_list2.append((x, y))
            print("2 : (%d, %d)" % (x, y))
            cv2.circle(img_original, (x, y), 2, (0, 255, 0), -1)
            print(point_list2)
            i = i + 1


cv2.namedWindow('original')
cv2.setMouseCallback('original', mouse_callback)

# 원본 이미지
img_original = cv2.imread('위치2-1.jpeg') # test3.jpg 파일을 img_original 변수에 저장
img_original2 = cv2.imread('빈다이3.png') # test3.jpg 파일을 img_original 변수에 저장
img_original2 = cv2.resize(img_original2, dsize=(650, 344), interpolation=cv2.INTER_AREA)
# img_original3 = cv2.imread('빈다이3.png') # test3.jpg 파일을 img_original 변수에 저장
# img_original3 = cv2.resize(img_original3, dsize=(650, 346), interpolation=cv2.INTER_AREA)


while(True):

    cv2.imshow("original", img_original)


    height, width = 315, 612 # return 되는 이미지의 크기 값


    if cv2.waitKey(1)&0xFF == 32: # spacebar를 누르면 루프 탈출.
        break

print(list(point_list2[0]))
# 좌표 순서 - 상단왼쪽 끝, 상단오른쪽 끝, 하단왼쪽 끝, 하단오른쪽 끝
pts1 = np.float32([list(point_list[0]),list(point_list[1]),list(point_list[2]),list(point_list[3])])
pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])


print('pts1 : ',pts1)
print('pts2 : ',pts2)


M = cv2.getPerspectiveTransform(pts1,pts2)      # pts1의 좌표를 pts2의 좌표로 변환 시킬 변수 M 설정
a = 1
b = 2

img_result = cv2.warpPerspective(img_original, M, (width,height))      # 이미지 와핑
img_result2 = img_original2

r=0     # red볼을 둘 공간을 찾았을 때 조건문을 돌리지 않기 위한 변수
b=0     # blue볼을 둘 공간을 찾았을 때 조건문을 돌리지 않기 위한 변수
g=0     # green볼을 둘 공간을 찾았을 때 조건문을 돌리지 않기 위한 변수

for y in range(15,300):
    for x in range(15,610):
        if img_result[y,x][0] == 0 and img_result[y,x][1] == 0 and img_result[y,x][2] == 255 and r == 0:
            img_result2 = cv2.circle(img_result2, (x+25,y+14),7,(0,0,255),-1)       # 해당 좌표값에 공 그리기
            r = r + 1
            print('<red>\ny, x :',y,', ',x)
        elif img_result[y,x][0] == 255 and img_result[y,x][1] == 0 and img_result[y,x][2] == 0 and g == 0:
            img_result2 = cv2.circle(img_result2, (x+25,y+14),7,(255,0,0),-1)
            g = g + 1
            print('<green>\ny, x :',y,', ',x)
        elif img_result[y,x][0] == 0 and img_result[y,x][1] == 255 and img_result[y,x][2] == 0 and b == 0:
            img_result2 = cv2.circle(img_result2, (x+25,y+14),7,(0,255,0),-1)
            b = b + 1
            print('<blue>\ny, x :',y,', ',x)

        if r == 1 and b == 1 and g == 1:
            k=1
            break
    if r == 1 and b == 1 and g == 1:
        break


# img_original3[19:19 + img_result2.shape[0], 20:20+img_result2.shape[1]] = img_result2

print('\nok I know where they are')

cv2.imshow("result1", img_original)
cv2.imshow("result2", img_result2)
# cv2.imshow("result3", img_original3)
cv2.waitKey(0)