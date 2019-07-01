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


def comparison(num1,num2,id_1,id_2):
    most_num = 0
    most_id = 0
    if num1 > num2:
        most_num = num1
        most_id = id_1
    else:
        most_num = num2
        most_id = id_2

    return most_num,most_id

def Most_id_check(count_id_1,count_id_2,count_id_3,count_id_4,count_id_5,count_id_6,count_id_7,count_id_8,count_id_9,count_id_10,id_1,id_2,id_3,id_4,id_5,id_6,id_7,id_8,id_9,id_10):
    
    first_comparison_result_1 = comparison(count_id_1,count_id_2,id_1,id_2)
    first_comparison_result_2 = comparison(count_id_3,count_id_4,id_3,id_4)
    first_comparison_result_3 = comparison(count_id_5,count_id_6,id_5,id_6)
    first_comparison_result_4 = comparison(count_id_7,count_id_8,id_7,id_8)
    first_comparison_result_5 = comparison(count_id_9,count_id_10,id_9,id_10)

    second_comparison_result_1 = comparison(first_comparison_result_1[0],first_comparison_result_2[0],first_comparison_result_1[1],first_comparison_result_2[1])
    second_comparison_result_2 = comparison(first_comparison_result_3[0],first_comparison_result_4[0],first_comparison_result_3[1],first_comparison_result_4[1])

    third_comparison_result = comparison(second_comparison_result_1[0],second_comparison_result_2[0],second_comparison_result_1[1],second_comparison_result_2[1])

    most_amount = comparison(third_comparison_result[0],first_comparison_result_5[0],third_comparison_result[1],first_comparison_result_5[1])

    return most_amount







   


state_file = open(sys.argv[1],'r')
synchro_file = open(sys.argv[2],'w')
all_synchro_result_file = open(sys.argv[3],'a')
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

time_series_list = []

set_total_frame_number = 5100
set_time = 30
set_time_counter = 0


while frame_counter < set_total_frame_number:
    frame_counter = frame_counter + 1
    set_time_counter = set_time_counter + 1
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
      

    if set_time_counter == set_time:
        most_id =  Most_id_check(flag_count_id_0,flag_count_id_1,flag_count_id_2,flag_count_id_3,flag_count_id_4,flag_count_id_5,flag_count_id_6,flag_count_id_7,flag_count_id_8,flag_count_id_9,0,1,2,3,4,5,6,7,8,9)
        time_series_list.append(most_id[1])
        set_time_counter = 0
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


print(time_series_list) 

counter = 0

frame_sum = flag_count_id_0 + flag_count_id_1 + flag_count_id_2 + flag_count_id_3 + flag_count_id_4 + flag_count_id_5 + flag_count_id_6 + flag_count_id_7 + flag_count_id_8 + flag_count_id_9

synchro_file.write("同期性\n")
all_synchro_result_file.write(usr_name+",")
while counter < (set_total_frame_number/set_time):
    
    synchro_file.write(str(time_series_list[counter])+",")
    all_synchro_result_file.write(str(time_series_list[counter])+",")
    counter = counter + 1

synchro_file.write("\n")
all_synchro_result_file.write("\n")


