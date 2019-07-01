import sys
import cv2
import os
from sys import platform
import argparse
import csv
import math

#フラグ番号とidが一致すればカウンターを1増やして返却
def check_number(x_id_counter,flag_id,right_flag,left_flag):
    if flag_id == right_flag:
        x_id_counter = x_id_counter + 1
    return x_id_counter




state_file = open(sys.argv[1],'r')
count_file = open(sys.argv[2],'w')
all_count_result_file = open(sys.argv[3],'a')
usr_name = str(sys.argv[4])
print(state_file)

csv_reader = csv.reader(state_file, delimiter=',')
frame_counter = 0



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


flag_count_id_0 = 0
flag_count_id_1 = 0
flag_count_id_2 = 0
flag_count_id_3 = 0
flag_count_id_4 = 0
flag_count_id_5 = 0
flag_count_id_6 = 0
flag_count_id_7 = 0
flag_count_id_8 = 0
flag_count_id_9 = 0

set_total_frame_number = 5100


while frame_counter < set_total_frame_number:
    frame_counter = frame_counter + 1
    row = next(csv_reader)
    #print(row)

    right_flag = int(float(row[0]))
    left_flag = int(float(row[1]))

    

    if right_flag == left_flag:
        
        flag_count_id_0 = check_number(flag_count_id_0,0,right_flag,left_flag)
        flag_count_id_1 = check_number(flag_count_id_1,1,right_flag,left_flag)
        flag_count_id_2 = check_number(flag_count_id_2,2,right_flag,left_flag)
        flag_count_id_3 = check_number(flag_count_id_3,3,right_flag,left_flag)
        flag_count_id_4 = check_number(flag_count_id_4,4,right_flag,left_flag)
        flag_count_id_5 = check_number(flag_count_id_5,5,right_flag,left_flag)
        flag_count_id_6 = check_number(flag_count_id_6,6,right_flag,left_flag)
        flag_count_id_7 = check_number(flag_count_id_7,7,right_flag,left_flag)

        if right_flag == 10:
            right_flag = 8
            left_flag = 8
            flag_count_id_8 = check_number(flag_count_id_8,8,right_flag,left_flag)

    else:
        flag_count_id_9 = flag_count_id_9 + 1
      


print("test") 

frame_sum = flag_count_id_0 + flag_count_id_1 + flag_count_id_2 + flag_count_id_3 + flag_count_id_4 + flag_count_id_5 + flag_count_id_6 + flag_count_id_7 + flag_count_id_8 + flag_count_id_9

count_file.write("状態,"+"フレーム数,"+"割合\n")
count_file.write("総数,"+str(frame_counter)+","+str(frame_counter/frame_counter)+"\n")
count_file.write("スクリーン,"+str(flag_count_id_1)+","+str(flag_count_id_1/frame_counter)+"\n")        
count_file.write("発表者,"+str(flag_count_id_2)+","+str(flag_count_id_2/frame_counter)+"\n")
count_file.write("生徒1,"+str(flag_count_id_3)+","+str(flag_count_id_3/frame_counter)+"\n")
count_file.write("生徒2,"+str(flag_count_id_4)+","+str(flag_count_id_4/frame_counter)+"\n")
count_file.write("生徒3,"+str(flag_count_id_5)+","+str(flag_count_id_5/frame_counter)+"\n")
count_file.write("先生,"+str(flag_count_id_6)+","+str(flag_count_id_6/frame_counter)+"\n")
count_file.write("サッケード,"+str(flag_count_id_7)+","+str(flag_count_id_7/frame_counter)+"\n")
count_file.write("瞬き,"+str(flag_count_id_8)+","+str(flag_count_id_8/frame_counter)+"\n")
count_file.write("左右不一致,"+str(flag_count_id_9)+","+str(flag_count_id_9/frame_counter)+"\n")
count_file.write("その他,"+str(flag_count_id_0)+","+str(flag_count_id_0/frame_counter)+"\n")
count_file.write("合計,"+str(frame_sum)+","+str(frame_sum/frame_counter)+"\n")

all_count_result_file.write(usr_name+"\n")
all_count_result_file.write("状態,"+"フレーム数,"+"割合\n")
all_count_result_file.write("総数,"+str(frame_counter)+","+str(frame_counter/frame_counter)+"\n")
all_count_result_file.write("スクリーン,"+str(flag_count_id_1)+","+str(flag_count_id_1/frame_counter)+"\n")        
all_count_result_file.write("発表者,"+str(flag_count_id_2)+","+str(flag_count_id_2/frame_counter)+"\n")
all_count_result_file.write("生徒1,"+str(flag_count_id_3)+","+str(flag_count_id_3/frame_counter)+"\n")
all_count_result_file.write("生徒2,"+str(flag_count_id_4)+","+str(flag_count_id_4/frame_counter)+"\n")
all_count_result_file.write("生徒3,"+str(flag_count_id_5)+","+str(flag_count_id_5/frame_counter)+"\n")
all_count_result_file.write("先生,"+str(flag_count_id_6)+","+str(flag_count_id_6/frame_counter)+"\n")
all_count_result_file.write("サッケード,"+str(flag_count_id_7)+","+str(flag_count_id_7/frame_counter)+"\n")
all_count_result_file.write("瞬き,"+str(flag_count_id_8)+","+str(flag_count_id_8/frame_counter)+"\n")
all_count_result_file.write("左右不一致,"+str(flag_count_id_9)+","+str(flag_count_id_9/frame_counter)+"\n")
all_count_result_file.write("その他,"+str(flag_count_id_0)+","+str(flag_count_id_0/frame_counter)+"\n")
all_count_result_file.write("合計,"+str(frame_sum)+","+str(frame_sum/frame_counter)+"\n")
all_count_result_file.write("\n")


