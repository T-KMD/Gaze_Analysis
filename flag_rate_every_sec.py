import sys
import cv2
import os
from sys import platform
import argparse
import csv
import math


flag_count_screen = 0
flag_count_presenter = 0
flag_count_teacher = 0
flag_count_students = 0
flag_count_others = 0

def frame_checker(frame,counter_1,counter_2,counter_3,counter_4,counter_5):
    if frame == "1":
        counter_1 = counter_1 + 1
    
    if frame == "2" :
        counter_2 = counter_2 + 1

    if frame == "6":
        counter_3 = counter_3 + 1
    
    if frame == "3" or frame == "4" or frame == "5":
        counter_4 = counter_4 + 1

    if frame == "0":
        counter_5 = counter_5 + 1
    
    return counter_1,counter_2,counter_3,counter_4,counter_5 
 
    

synchro_file = open(sys.argv[1],'r')
flag_rate_file = open(sys.argv[2],'w')


print(synchro_file)

csv_reader = csv.reader(synchro_file, delimiter=',')
frame_counter = 1



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





usr_A = next(csv_reader)
usr_B = next(csv_reader)
usr_C = next(csv_reader)
usr_D = next(csv_reader)
usr_E = next(csv_reader)
usr_F = next(csv_reader)
usr_G = next(csv_reader)
usr_H = next(csv_reader)
usr_I = next(csv_reader)
usr_J = next(csv_reader)


#print(usr_A)
#print(usr_J)
flag_rate_file.write("時間（秒）,"+"スクリーン,"+"発表者,"+"先生,"+"生徒,"+"その他,"+"合計,"+"時間（秒）,"+"スクリーンの割合,"+"発表者の割合,"+"先生の割合,"+"生徒の割合,"+"その他の割合,"+"割合の合計,"+"\n")

while frame_counter <= 170:
    
    flag_count_screen,flag_count_presenter,flag_count_teacher,flag_count_students,flag_count_others = frame_checker(usr_A[frame_counter],flag_count_screen,flag_count_presenter,flag_count_teacher,flag_count_students,flag_count_others)
   
    
    flag_count_screen,flag_count_presenter,flag_count_teacher,flag_count_students,flag_count_others = frame_checker(usr_B[frame_counter],flag_count_screen,flag_count_presenter,flag_count_teacher,flag_count_students,flag_count_others)
    flag_count_screen,flag_count_presenter,flag_count_teacher,flag_count_students,flag_count_others = frame_checker(usr_C[frame_counter],flag_count_screen,flag_count_presenter,flag_count_teacher,flag_count_students,flag_count_others)
    flag_count_screen,flag_count_presenter,flag_count_teacher,flag_count_students,flag_count_others = frame_checker(usr_D[frame_counter],flag_count_screen,flag_count_presenter,flag_count_teacher,flag_count_students,flag_count_others)
    flag_count_screen,flag_count_presenter,flag_count_teacher,flag_count_students,flag_count_others = frame_checker(usr_E[frame_counter],flag_count_screen,flag_count_presenter,flag_count_teacher,flag_count_students,flag_count_others)
    flag_count_screen,flag_count_presenter,flag_count_teacher,flag_count_students,flag_count_others = frame_checker(usr_F[frame_counter],flag_count_screen,flag_count_presenter,flag_count_teacher,flag_count_students,flag_count_others)
    flag_count_screen,flag_count_presenter,flag_count_teacher,flag_count_students,flag_count_others = frame_checker(usr_G[frame_counter],flag_count_screen,flag_count_presenter,flag_count_teacher,flag_count_students,flag_count_others)
    flag_count_screen,flag_count_presenter,flag_count_teacher,flag_count_students,flag_count_others = frame_checker(usr_H[frame_counter],flag_count_screen,flag_count_presenter,flag_count_teacher,flag_count_students,flag_count_others)
    flag_count_screen,flag_count_presenter,flag_count_teacher,flag_count_students,flag_count_others = frame_checker(usr_I[frame_counter],flag_count_screen,flag_count_presenter,flag_count_teacher,flag_count_students,flag_count_others)
    flag_count_screen,flag_count_presenter,flag_count_teacher,flag_count_students,flag_count_others = frame_checker(usr_J[frame_counter],flag_count_screen,flag_count_presenter,flag_count_teacher,flag_count_students,flag_count_others)
    

    flag_sum = int(flag_count_screen) + int(flag_count_presenter) + int(flag_count_teacher) + int(flag_count_students) + int(flag_count_others)

    screen_rate = int(flag_count_screen) / flag_sum
    presenter_rate = int(flag_count_presenter) / flag_sum
    teacher_rate = int(flag_count_teacher) / flag_sum
    students_rate = int(flag_count_students) / flag_sum
    others_rate = int(flag_count_others) / flag_sum
    rate_sum = screen_rate + presenter_rate + teacher_rate + students_rate + others_rate 

    flag_rate_file.write(str(frame_counter)+","+str(flag_count_screen)+","+str(flag_count_presenter)+","+str(flag_count_teacher)+","+str(flag_count_students)+","+str(flag_count_others)+","+str(flag_sum)+","+str(frame_counter)+","+str(screen_rate)+","+str(presenter_rate)+","+str(teacher_rate)+","+str(students_rate)+","+str(others_rate)+","+str(rate_sum)+"\n")

    frame_counter = frame_counter + 1
    
    




    """
    print(str(flag_count_screen)+",")
    print(str(flag_count_presenter)+",")
    print(str(flag_count_teacher)+",")
    print(str(flag_count_students)+",")
    print(str(flag_count_others)+"\n")
    print(type(usr_A[frame_counter]))
    """
 
    flag_count_screen = 0
    flag_count_presenter = 0
    flag_count_teacher = 0
    flag_count_students = 0
    flag_count_others = 0



"""
flag_rate_file.write("状態,"+"フレーム数,"+"割合\n")
flag_rate_file.write("総数,"+str(frame_counter)+","+str(frame_counter/frame_counter)+"\n")
flag_rate_file.write("スクリーン,"+str(flag_count_id_1)+","+str(flag_count_id_1/frame_counter)+"\n")        
flag_rate_file.write("発表者,"+str(flag_count_id_2)+","+str(flag_count_id_2/frame_counter)+"\n")
flag_rate_file.write("生徒1,"+str(flag_count_id_3)+","+str(flag_count_id_3/frame_counter)+"\n")
flag_rate_file.write("生徒2,"+str(flag_count_id_4)+","+str(flag_count_id_4/frame_counter)+"\n")
flag_rate_file.write("生徒3,"+str(flag_count_id_5)+","+str(flag_count_id_5/frame_counter)+"\n")
flag_rate_file.write("先生,"+str(flag_count_id_6)+","+str(flag_count_id_6/frame_counter)+"\n")
flag_rate_file.write("サッケード,"+str(flag_count_id_7)+","+str(flag_count_id_7/frame_counter)+"\n")
flag_rate_file.write("瞬き,"+str(flag_count_id_8)+","+str(flag_count_id_8/frame_counter)+"\n")
flag_rate_file.write("左右不一致,"+str(flag_count_id_9)+","+str(flag_count_id_9/frame_counter)+"\n")
flag_rate_file.write("その他,"+str(flag_count_id_0)+","+str(flag_count_id_0/frame_counter)+"\n")
flag_rate_file.write("合計,"+str(frame_sum)+","+str(frame_sum/frame_counter)+"\n")

"""


