import dlib
import cv2
import os

kruzhok_model = dlib.simple_object_detector('cPP.svm')
dir = r'C:\Users\Egor\PycharmProjects\pythonProject1\firstAndSecondTASK\cPP'

ImgNameList = os.listdir(dir + "/images")

for FileName in ImgNameList:
    image = cv2.imread(dir + "/images/" + FileName)
    img_viz = image.copy()

    boxes = kruzhok_model(image)
    if len(boxes):
        print('--------', boxes[0])
        (x, y, x2, y2) = [boxes[0].left(), boxes[0].top(), boxes[0].right(), boxes[0].bottom()]
        cv2.rectangle(img_viz, (x, y), (x2, y2), (0, 200, 0), 2)
        cv2.imshow('img_viz', img_viz)
        cv2.waitKey(0)
        print(type([boxes[0].left(), boxes[0].top(), boxes[0].right(), boxes[0].bottom()]))
        print('ok')
    else:
        print('no boxes')
