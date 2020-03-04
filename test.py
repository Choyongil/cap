import numpy as np
import cv2


point_list = []
count = 0

def mouse_callback(event, x, y, flags, param):
    global point_list, count, img_original


    # 마우스 왼쪽 버튼 누를 때마다 좌표를 리스트에 저장
    if event == cv2.EVENT_LBUTTONDOWN:
        print("(%d, %d)" % (x, y))
        point_list.append((x, y))

        print(point_list)
        cv2.circle(img_original, (x, y), 3, (0, 0, 255), -1)



cv2.namedWindow('original')
cv2.setMouseCallback('original', mouse_callback)

# 원본 이미지
img_original = cv2.imread('test1234.jpeg')
redball = cv2.imread('rball.png')
greenball = cv2.imread('greenball.png')
blueball = cv2.imread('blueball.png')
img_original[330:335,330:335] = [0,0,255]
img_original[220:225,330:335] = [255,0,0]
img_original[400:405,600:605] = [0,255,0]


rplogoImgDownscale = cv2.resize(redball, None, fx=0.7, fy=0.7, interpolation=cv2.INTER_AREA)
rplogoImgDownscale2 = cv2.resize(greenball, None, fx=0.7, fy=0.7, interpolation=cv2.INTER_AREA)
rplogoImgDownscale3 = cv2.resize(blueball, None, fx=0.7, fy=0.7, interpolation=cv2.INTER_AREA)
print('00',rplogoImgDownscale.shape[0])
print('11',rplogoImgDownscale.shape[1])



while(True):

    cv2.imshow("original", img_original)


    height, weight = 600, 1200


    if cv2.waitKey(1)&0xFF == 32: # spacebar를 누르면 루프에서 빠져나옵니다.
        break


# 좌표 순서 - 상단왼쪽 끝, 상단오른쪽 끝, 하단왼쪽 끝, 하단오른쪽 끝
pts1 = np.float32([list(point_list[0]),list(point_list[1]),list(point_list[2]),list(point_list[3])])
pts2 = np.float32([[0,0],[weight,0],[0,height],[weight,height]])


print('pts1 : ',pts1)
print('pts2 : ',pts2)

M = cv2.getPerspectiveTransform(pts1,pts2)

img_result2=cv2.warpPerspective(img_original, M, (weight,height))
img_result = cv2.warpPerspective(img_original, M, (weight,height))

k=0

for y in range(10,600):
    for x in range(10,1200):
        if img_result[y,x][0] == 0 and img_result[y,x][2] == 255:
            # img_result[y-15:y-15+rplogoImgDownscale.shape[0],x-15:x-15+rplogoImgDownscale.shape[1]]
            k=1
            break
    if k==1:
        break

k=0
for y2 in range(10,600):
    for x2 in range(10,1200):
        if img_result[y2,x2][0] == 0 and img_result[y2,x2][2] == 255:
            img_result[y2-15:y2-15+rplogoImgDownscale2.shape[0],x2-15:x2-15+rplogoImgDownscale2.shape[1]] = rplogoImgDownscale2
            k=1
            break
    if k==1:
        break

k=0
for y3 in range(10,600):
    for x3 in range(10,1200):
        if img_result[y3,x3][0] == 255 and img_result[y3,x3][1] == 0:
            img_result[y3-15:y3-15+rplogoImgDownscale3.shape[0],x3-15:x3-15+rplogoImgDownscale3.shape[1]] =rplogoImgDownscale3
            k=1
            break
    if k==1:
        break

print('ok I know where they are')

print('y, x:',y,',',x)
print('y2, x2:',y2,',',x2)
print('y3, x3:',y3,',',x3)


for c in range(0,3):
    print('c',c)

    img_result[y-15:y-15+rplogoImgDownscale.shape[0], x-15:x-15+rplogoImgDownscale.shape[1], c] = \
    rplogoImgDownscale[:,:,c] * (rplogoImgDownscale[:,:,2]/255.0) + \
    img_result[y-15:y-15+rplogoImgDownscale.shape[0], x-15:x-15+rplogoImgDownscale.shape[1], c] * (1.0 - rplogoImgDownscale[:,:,2]/255.0)


for c in range(0,3):
    print('c2',c)
    img_result[y2-15:y2-15+rplogoImgDownscale2.shape[0], x2-15:x2-15+rplogoImgDownscale2.shape[1], c] = \
    rplogoImgDownscale2[:,:,c] * (rplogoImgDownscale2[:,:,2]/255.0) + \
    img_result[y2-15:y2-15+rplogoImgDownscale2.shape[0], x2-15:x2-15+rplogoImgDownscale2.shape[1], c] * (1.0 - rplogoImgDownscale2[:,:,2]/255.0)

for c in range(0,3):
    print('c3',c)
    img_result[y3-15:y3-15+rplogoImgDownscale3.shape[0], x3-15:x3-15+rplogoImgDownscale3.shape[1], c] = \
    rplogoImgDownscale3[:,:,c] * (rplogoImgDownscale3[:,:,2]/255.0) + \
    img_result[y3-15:y3-15+rplogoImgDownscale3.shape[0], x3-15:x3-15+rplogoImgDownscale3.shape[1], c] * (1.0 - rplogoImgDownscale3[:,:,2]/255.0)


kernel = np.array([[-1, -1, -1], [-1,9,-1], [-1,-1,-1]])
sharpen = cv2.filter2D(img_result, -1, kernel)


cv2.imshow("result1", img_result)
cv2.imshow("result12", img_result2)
cv2.imshow("sharpen", sharpen)
cv2.waitKey(0)
cv2.destroyAllWindows()