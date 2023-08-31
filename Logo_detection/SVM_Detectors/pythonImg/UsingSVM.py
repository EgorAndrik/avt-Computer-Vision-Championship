import dlib
import cv2
import os


kruzhok_model = dlib.simple_object_detector('pythonImg.svm')
dir = r'C:\Users\Egor\PycharmProjects\pythonProject1\firstAndSecondTASK\pythonImg'

ImgNameList = os.listdir(dir + "/images")

for FileName in ImgNameList:
    image = cv2.imread(dir + "/images/" + FileName)
    img_viz = image.copy()

    boxes = kruzhok_model(image)
    if len(boxes):
        for box in boxes:
            print('ok')
            (x, y, x2, y2) = [box.left(), box.top(), box.right(), box.bottom()]
            cv2.rectangle(img_viz, (x, y), (x2, y2), (0, 200, 0), 2)
            cv2.imshow('img_viz', img_viz)
            cv2.waitKey(0)
    else:
        print('no boxes')
