import cv2
import pandas as pd
import os


csv_path = 'annotations.csv'
img_path = ''
yolo_annots_path = 'YOLOannots/'

table = pd.read_csv(csv_path, delimiter=",")

row_num = len(table.axes[0])
col_num = len(table.axes[0])

for row in table.itertuples():
    image_name = row[1]
    x, y, w, h = row[2], row[3], row[4], row[5]
    img = cv2.imread(img_path + image_name)
    img_H, img_W = img.shape[:2]

    image_name = os.path.split(image_name)[1]
    annots_name = image_name.split('.')[0]

    x = x + w / 2
    y = y + h / 2

    with open(yolo_annots_path + annots_name + '.txt', 'w') as f:
        f.write('0 ' + str(x / img_W) + ' ' + str(y / img_H) + ' ' + str(w / img_W) + ' ' + str(h / img_H))
    print(annots_name + '.txt')
