# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
from sys import platform
import argparse
import csv


# Import Openpose (Windows/Ubuntu/OSX)
dir_path = os.path.dirname(os.path.realpath(__file__))
try:
    # Windows Import
    if platform == "win32":
        # Change these variables to point to the correct folder (Release/x64 etc.) 
        sys.path.append(dir_path + '/../../python/openpose/Release');
        os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + '/../../x64/Release;' +  dir_path + '/../../bin;'
        import pyopenpose as op
    else:
        # Change these variables to point to the correct folder (Release/x64 etc.) 
        sys.path.append('../../python');
        # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
        # sys.path.append('/usr/local/python')
        from openpose import pyopenpose as op
except ImportError as e:
    print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
    raise e

# Flags
parser = argparse.ArgumentParser()
parser.add_argument("--image_path", default=None, help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
args = parser.parse_known_args()

# Custom Params (refer to include/openpose/flags.hpp for more parameters)
params = dict()
params["model_folder"] = "../../../models/"
params["face"] = False
params["hand"] = False

# Add others in path?
for i in range(0, len(args[1])):
    curr_item = args[1][i]
    if i != len(args[1])-1: next_item = args[1][i+1]
    else: next_item = "1"
    if "--" in curr_item and "--" in next_item:
        key = curr_item.replace('-','')
        if key not in params:  params[key] = "1"
    elif "--" in curr_item and "--" not in next_item:
        key = curr_item.replace('-','')
        if key not in params: params[key] = next_item

# Construct it from system arguments
# op.init_argv(args[1])
# oppython = op.OpenposePython()



coordinate_file = open(sys.argv[1],'w')
target_human_x_min = int(sys.argv[2])
target_human_x_max = int(sys.argv[3])
target_human_y = int(sys.argv[4])
target_movie = str(sys.argv[5])
#print(target_human_x)
#print(target_human_y)

try:
    # Starting OpenPose
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    # Process Image
    datum = op.Datum()

    cap = cv2.VideoCapture(target_movie)

    #print(cap)

    #print("test 1")

    frame_counter = 0

    while(True):
        # Capture frame-by-frame

        #print("test 2")
        ret,frame = cap.read()
        #print("test 3")
        
        #imageToProcess =cv2.rectangle(frame, (200, 0), (3400, 1920), (255, 255, 255), thickness=-1)

        
        imageToProcess = frame
        #print(imageToProcess.shape)
        #print("test 4")
        #cv2.imshow("test",frame)
        datum.cvInputData = imageToProcess
        opWrapper.emplaceAndPop([datum])

        
        # Display Image
        
        print(frame_counter)
        frame_counter = frame_counter + 1

        human_count = 0
        while human_count < len(datum.poseKeypoints):
            
            #print(datum.poseKeypoints[human_count][1][0])

            if target_human_x_min < datum.poseKeypoints[human_count][1][0] and datum.poseKeypoints[human_count][1][0] < target_human_x_max and datum.poseKeypoints[human_count][1][1] < target_human_y:
                write_1 = (str(datum.poseKeypoints[human_count][1][0])+",")
                write_2 = (str(datum.poseKeypoints[human_count][1][1])+"\n")
            human_count = human_count + 1


        print(write_1)
        coordinate_file.write(write_1)
        coordinate_file.write(write_2)

        #print("Face keypoints: \n" + str(datum.faceKeypoints))
        #print("Left hand keypoints: \n" + str(datum.handKeypoints[0]))
        #print("Right hand keypoints: \n" + str(datum.handKeypoints[1]))
        
        #cv2.imshow("OpenPose 1.5.0 - Tutorial Python API", datum.cvOutputData)
   

        if frame_counter == 6000:
            break
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    print("test 5")

    
except Exception as e:
    # print(e)
    sys.exit(-1)
