import dlib
import os, cv2
import xml.etree.ElementTree as pars


dir = r'C:\Users\Egor\PycharmProjects\pythonProject1\firstAndSecondTASK\pythonImg'
images, annots = [], []

ImgNameList = os.listdir(dir + "/images")

for FileName in ImgNameList:
    image = cv2.imread(dir + "/images/" + FileName)
    # cv2.imshow('img', image)
    # cv2.waitKey(0)

    OnlyFileName = FileName.split('.')[0]
    e = pars.parse(dir + '/annots/' + OnlyFileName + '.xml')
    root = e.getroot()

    for object in root.findall("object"):
        object = object.find('bndbox')

        x = int(object.find('xmin').text)
        y = int(object.find('ymin').text)
        x2 = int(object.find('xmax').text)
        y2 = int(object.find('ymax').text)

        # img_viz = image.copy()
        # cv2.rectangle(img_viz, (x, y), (x2, y2), (0, 200, 0))
        # cv2.imshow('img_viz', img_viz)
        # cv2.waitKey(0)

        images.append(image)
        annots.append([dlib.rectangle(left=x, top=y, right=x2, bottom=y2)])

options = dlib.simple_object_detector_training_options()
options.be_verbose = True
options.epsilon = 0.0001
options.C = 3

detector = dlib.train_simple_object_detector(images, annots, options)

detector.save('pythonImg.svm')

