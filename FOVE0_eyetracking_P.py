'''
起動時
第一引数　動きの無い対象の範囲を指定したファイル
第二引数　出力するファイル
第三引数　Unityで獲得した視線情報のファイル
第四引数　発表者の動きに応じて範囲を指定したファイル

プログラム概要
Unityで獲得した3次元ベクトルである視線情報を緯度・経度に変換し、
設定した対象の範囲に視線が存在したかフレーム毎に判定
講義映像の発表シーンに対応　

'''
import cv2
import csv
import math
import numpy as np
import sys
import openpyxl

# 緯度：latitude
# 経度：longitude
# (0,0)              W             (W-1,0)
# (-PI,PI/2)                       (PI,PI/2)
# +--------------------------------->
# |
# |
# |
# | H            (0.0,0.0,1.0)
# |
# |
# V
# (0,H-1)                          (W-1,H-1)
# (-PI,-PI/2)                      (PI,PI/2)


def calcLatLng(W, H, dirvec):
    lng = 0.0  # 経度：longitude
    lat = 0.0  # 緯度：latitude
    x = dirvec[0]
    y = dirvec[1]
    z = dirvec[2]
    # print(dirvec)
    dirvecLength = np.linalg.norm(dirvec) #ユークリッド距離の計算
    lng = math.pi * 0.5 - math.atan2(z, x)
    lat = math.asin(y / dirvecLength)

    return lat, lng


def calcPosInEquirectangularImage(W, H, lat, lng):
    x = (int)(W * ((lng + math.pi) * 0.5 / math.pi))
    y = (int)(H * ((-lat + math.pi * 0.5) / math.pi))
    return x, y


#正解範囲に視線が含まれているかチェックしフラグを返却
def checkAnswer(x,y,list1,list2):
    answerflag = 0
    
    #print(list1[1])
    
    
    for i in range(0,5):
        #print("checkAnswer test "+str(i))
        if i == 1:
            #print("do continue ")
            #continue
        elif list1[i][0] < x < list1[i][1] and list2[i][0] < y < list2[i][1]:
            answerflag = i + 1
            #print("checkAnswer test "+str(answerflag))
    return answerflag


def checkAnswer2(already_flag,flag_id,x,y,range_x_min,range_x_max,range_y_min,range_y_max):
    
    if range_x_min < x < range_x_max and range_y_min < y < range_y_max:
        return flag_id
    else:
        return already_flag
        

"""
flag_idのリスト
0　その他
1　スクリーン
2　発表者
3　学生１
4　学生２
5　学生３
6　先生
7　サッケード
8　瞬目
9　不一致



"""




def AnswerOpen(filename):
    

    #正解座標を記述したファイルを開きx,yの座標リストを作成する
    with open(filename,'r',newline='') as answerfile:
        csv_reader = csv.reader(answerfile, delimiter=',')
        
        XLists = ([],[],[],[],[])
        YLists = ([],[],[],[],[])
        

        for index in range(0,5):

            row = next(csv_reader)
            X1 = (int)(row[0])
            X2 = (int)(row[1])
            Y1 = (int)(row[2])
            Y2 = (int)(row[3])

            for list1 in (X1,X2):
                #print(list1)
                XLists[index].append(list1)
            for list2 in (Y1,Y2):
                #print(list2)
                YLists[index].append(list2)

    #print(XLists)
            
            
    return XLists,YLists



def CheckAngle(Vector1,Vector2):  #ベクトル間の角度を求める関数
    abs_Vec1 = math.sqrt(Vector1[0]**2 + Vector1[1]**2 + Vector1[2]**2)
    abs_Vec2 = math.sqrt(Vector2[0]**2 + Vector2[1]**2 + Vector2[2]**2)
    inner_product = Vector1[0]*Vector2[0] + Vector1[1]*Vector2[1] + Vector1[2]*Vector2[2]
    theta = math.acos(inner_product / (abs_Vec1*abs_Vec2))
    deg = math.degrees(theta)
    # deg = theta * 180.0 / math.pi
    return deg




def fove0_eyetracking():


    

    XLists,YLists = AnswerOpen(sys.argv[1])



    capture = cv2.VideoCapture('R0010027_er_2.mp4')

    if capture.isOpened() is False:
        raise("IO Error")

    # 1回キャプチャしてフレームサイズを調べる
    ret, image = capture.read()

    H = image.shape[0]
    W = image.shape[1]
    channel = image.shape[2]

    print("width  = ", W)
    print("height = ", H)
    print("channel = ", channel)

    """
    # 視点を描画するための画像
    layer = np.zeros((H, W, 3), np.uint8)  # y座標, x座標, チャンネル

    # 処理結果を動画として保存
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    writer = cv2.VideoWriter('output.avi', fourcc, 20.0, (W, H))

    #cv2.namedWindow("Capture", cv2.WINDOW_AUTOSIZE)
    """

    lefteye = [(-1,-1)] * 10
    righteye = [(-1,-1)] * 10
    index = 0
    flagfile = open(sys.argv[2],'w')
    pre_EyeVec_R = np.array([0.0,0.0,0.0])        #衝動性眼球運動を判別用の変数
    pre_eyeVec_L = np.array([0.0,0.0,0.0])
    
    First_flag = 0      #衝動性眼球運動の判別時に最初の判別をスキップするためのフラグ


    

    



    with open(sys.argv[3], 'r', newline='') as csvfile:
        target_range_file = open(sys.argv[4],'r')

        csv_reader = csv.reader(csvfile, delimiter=',')
        range_reader = csv.reader(target_range_file,delimiter=',')
        while True:

            deg_L = 0.0
            deg_R = 0.0
            #layer = np.zeros((H, W, 3), np.uint8) 
           

            # csvファイルから1行読み込み
            row = next(csv_reader)
            #print(row)
            target_range = next(range_reader)

            range_x_min = int(float(target_range[0]))
            range_x_max = int(float(target_range[1]))
            
            range_y_min = int(float(target_range[2]))
            range_y_max = int(float(target_range[3]))

            


            #左目
            # 視線ベクトル
            dX_L = (float)(row[0])
            dY_L = (float)(row[1])
            dZ_L = (float)(row[2])

            #右目
            # 視線ベクトル
            dX_R = (float)(row[3])
            dY_R = (float)(row[4])
            dZ_R = (float)(row[5])

            dirvec_L = np.array([dX_L, dY_L, dZ_L])
            dirvec_R = np.array([dX_R, dY_R, dZ_R])

            

            if dX_L > 900:
                LeftEyeFlag = 10
                RightEyeFlag = 10

            elif First_flag == 1:
                #print("dirvec_L: "+dirvec_L[0]+","+dirvec_L[1]+","+dirvec_L[2]+": pre_EyeVec_L: "+pre_EyeVec_L[0]+","+pre_EyeVec_L[1]+","+pre_EyeVec_L[2])
                #print("dirvec_L : ",end="")
                #print(dirvec_L)
                #print("pre_EyeVec_L : ",end="")
                #print(pre_EyeVec_L) 
                deg_L = CheckAngle(dirvec_L,pre_EyeVec_L)
                deg_R = CheckAngle(dirvec_R,pre_EyeVec_R)
                

            if (First_flag == 0 and dX_L < 900) or (dX_L < 900 and (deg_L < 1.5 and deg_R < 1.5 )):
                
                #左目の緯度経度計算
                lat_L, lng_L = calcLatLng(W, H, dirvec_L)
                #print("(Lat_L, Lng_L) = (" + str(lat_L) + ", " + str(lng_L) + ")")
                
                #左目の画像座標の計算
                x_L, y_L = calcPosInEquirectangularImage(W, H, lat_L, lng_L)
                if x_L > W :
                    x_L = x_L - W

                #print("(x_L, y_L) = (" + str(x_L) + ", " + str(y_L) + ")")    

                lefteye[index] = (x_L,y_L)
                #print(lefteye[index])

                LeftEyeFlag = checkAnswer(x_L,y_L,XLists,YLists)
                LeftEyeFlag = checkAnswer2(LeftEyeFlag,2,x_L,y_L,range_x_min,range_x_max,range_y_min,range_y_max)
                #print("flag check  "+str(LeftEyeFlag))
                

                #右目の緯度経度計算
                lat_R, lng_R = calcLatLng(W, H, dirvec_R)
                #print("(Lat_R, Lng_R) = (" + str(lat_R) + ", " + str(lng_R) + ")")

                #右目の画像座標の計算
                x_R, y_R = calcPosInEquirectangularImage(W, H, lat_R, lng_R)
                if x_R > W :
                    x_R = x_R - W

                #print("(x_R, y_R) = (" + str(x_R) + ", " + str(y_R) + ")")

                righteye[index] = (x_R,y_R)
                #print(righteye[index])
                RightEyeFlag = checkAnswer(x_R,y_R,XLists,YLists)
                RightEyeFlag = checkAnswer2(RightEyeFlag,2,x_R,y_R,range_x_min,range_x_max,range_y_min,range_y_max)
                
               
                

                #print(index)
                
                First_flag = 1

            
            if dX_L < 900 and First_flag == 1:
                pre_EyeVec_L = dirvec_L
                pre_EyeVec_R = dirvec_R

            if deg_L >= 1.5 or deg_R >= 1.5:
                LeftEyeFlag = 7
                RightEyeFlag = 7


            #print(deg_L)
            #print(deg_R)
            #print("flag")
            #print(LeftEyeFlag)

            flagfile.write((str)(LeftEyeFlag)+',')
            flagfile.write((str)(RightEyeFlag)+"\n")

        

            # 円を描画
            # 描画する画像，中心座標(x, y)，半径(画素数)，色，線の太さ，描画方法（省略可）
            
            '''
            for i in range(10):
                if lefteye[i] is not (-1,-1):  
                    cv2.circle(layer, lefteye[i], 30, (0, 0, 255), -1, 8)

                    image = cv2.add(image, layer)
            # 円を描画
            # 描画する画像，中心座標(x, y)，半径(画素数)，色，線の太さ，描画方法（省略可）
            for i in range(10):
                if righteye[i] is not (-1,-1):  
                    cv2.circle(layer, righteye[i], 30, (0, 0, 255), -1, 8)

                    image = cv2.add(image, layer)
            

            '''

            #cv2.imshow("Capture", image)
            #writer.write(image)

            if index < 10:
                index+=1
            if index == 10:
                
                index = 0

            
            

            if cv2.waitKey(1) >= 0:
                #cv2.imwrite("image.png", image)
                break

    #writer.release()
    #cv2.destroyAllWindows()
    flagfile.close()


if __name__ == "__main__":
    fove0_eyetracking()
