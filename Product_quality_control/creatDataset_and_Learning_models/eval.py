import pickle
import cv2
import numpy as np
import json

from typing import Dict


table = [['area1', 'area', 'per1', 'per', 'cont', 'apr', 'target']]

# TODO: Допишите импорт библиотек, которые собираетесь использовать

class Nut(object):
    def __init__(self, x, y, w, h, prediction: int = -1,
                 area=0, per=0, apr=0, cont=0, area1=0, per1=0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.prediction = prediction

        self.area = area
        self.per = per
        self.apr = apr
        self.cont = cont
        self.area1 = area1
        self.per1 = per1

    def set_position(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def setData(self, area: float = 0, per: float =0, apr=0, cont=0, area1=0, per1=0):
        self.area = area
        self.per = per
        self.apr = apr
        self.cont = cont
        self.area1 = area1
        self.per1 = per1

    @property
    def position(self):
        return self.x, self.y, self.w, self.h


def intersection(user_box, true_box):
    x, y, w, h = user_box
    user_box = (x, y, x + w, y + h)

    x, y, w, h = true_box
    true_box = (x, y, x + w, y + h)

    x1 = max(user_box[0], true_box[0])
    y1 = max(user_box[1], true_box[1])
    x2 = min(user_box[2], true_box[2])
    y2 = min(user_box[3], true_box[3])

    inter_area = max(0, x2 - x1 + 1) * max(0, y2 - y1 + 1)

    return inter_area > 0


def detect_defective_parts(video, resV) -> list:
    """
        Функция для детектирования бракованных гаек.

        Входные данные: объект, полученный cv2.VideoCapture, из объекта можно читать кадры методом .read
            На кадрах конвеер, транспортирующий гайки. Гайки перемещаются от нижней границы кадра к верхней.
            Некоторые гайки повреждены: не имеют центрального отверстия, сплющены, разорваны, деформированы.

        Выходные данные: list
            Необходимо вернуть список, состоящий из нулей и единиц, где 0 - гайка надлежащего качества,
                                                                        1 - бракованная гайка.
            Длина списка должна быть равна количеству гаек на видео.

        Примеры вывода:
            [0, 0, 0, 1] - первые 3 гайки целые, последняя - бракованная
            [1, 1, 1] - все 3 гайки бракованные
            [] - на видео не было гаек

    """
    # TODO: Отредактируйте эту функцию по своему усмотрению.
    # Для удобства можно создать собственные функции в этом файле.
    # Алгоритм проверки будет вызывать функцию detect_defective_parts, остальные функции должны вызываться из неё.

    # with open("bestModelCBC.bf", "rb") as file:
    #     model = pickle.load(file)

    nuts: Dict[int, Nut] = {}
    with open('forData.json', 'r') as data:
        forData = json.load(data)
    while True:  # цикл чтения кадров из видео
        status, frame = video.read()  # читаем кадр
        if not status:  # выходим из цикла, если видео закончилось
            break
        frame = cv2.resize(frame, (640, 360))
        frame = frame[:, 70:-70]
        h, w = frame.shape[:2]
        frame = cv2.flip(frame, 0)
        frame = cv2.GaussianBlur(frame, (3, 3), 1)

        start_zone = int(h * 0.25)
        end_zone = int(h * 0.75)

        binary = cv2.inRange(frame, (0, 0, 0), (100, 100, 100))
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(frame, contours, -1, (255, 0, 0), 2)
        if contours:
            dtFrame = [frame[::-1, ::], frame[::, ::-1],
                       frame[::-1, ::-1], frame]

            # contours = sorted(contours, key=cv2.contourArea, reverse=True)[1:]
            for i in contours:
                bbox_x1, bbox_y1, bbox_w, bbox_h = cv2.boundingRect(i)
                bbox_x2, bbox_y2 = bbox_x1 + bbox_w, bbox_y1 + bbox_h
                if bbox_y2 > start_zone and bbox_y1 < end_zone:
                    cv2.rectangle(frame, (bbox_x1, bbox_y1), (bbox_x2, bbox_y2), (255, 0, 0), 1)
                else:
                    cv2.rectangle(frame, (bbox_x1, bbox_y1), (bbox_x2, bbox_y2), (0, 255, 0), 1)

                nut_id = None
                for old_nut_id, old_bbox in nuts.items():
                    if intersection((bbox_x1, bbox_y1, bbox_w, bbox_h), old_bbox.position):
                        nut_id = old_nut_id
                        nuts[nut_id] = Nut(bbox_x1, bbox_y1, bbox_w, bbox_h, old_bbox.prediction)
                        break

                if nut_id is None and bbox_y2 > start_zone and bbox_y1 < end_zone:
                    nut_id = len(nuts)
                    nuts[nut_id] = Nut(bbox_x1, bbox_y1, bbox_w, bbox_h)

                if nut_id is not None:
                    if nuts[nut_id].prediction == -1:
                        nut = binary[bbox_y1 - 10:bbox_y2 + 10, bbox_x1 - 10:bbox_x2 + 10]

                        nut_contours, _ = cv2.findContours(nut, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                        # cv2.drawContours(frame, nut_contours, -1, (255, 255, 0), 4)
                        # nut_contours = sorted(nut_contours, key=cv2.contourArea, reverse=True)[1:]
                        if nut_contours:
                            dtFrame = [nut[::-1, ::], nut[::, ::-1],
                                       nut[::-1, ::-1], nut]
                            cv2.imshow('nut', dtFrame[0])
                            cv2.waitKey(1)
                            for elem in dtFrame:
                                nut_contours, _ = cv2.findContours(elem, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                                area: float = cv2.contourArea(nut_contours[0])
                                per: float = cv2.arcLength(nut_contours[0], True)
                                apd = cv2.approxPolyDP(nut_contours[0], 0.03 * per, True)

                                nuts[nut_id].setData(
                                    area,
                                    per,
                                    len(apd),
                                    len(nut_contours),
                                    cv2.contourArea(nut_contours[1]) if len(nut_contours) > 1 else 0,
                                    cv2.arcLength(nut_contours[1], True) if len(nut_contours) > 1 else 0
                                )
                                nuts[nut_id].area = area
                                nuts[nut_id].per = per
                                nuts[nut_id].area1 = cv2.contourArea(nut_contours[1]) if len(nut_contours) > 1 else 0
                                nuts[nut_id].per1 = cv2.arcLength(nut_contours[1], True) if len(nut_contours) > 1 else 0
                                nuts[nut_id].apr = len(apd)
                                nuts[nut_id].cont = len(nut_contours)
                                forData.append([
                                    area,
                                    per,
                                    len(apd),
                                    len(nut_contours),
                                    cv2.contourArea(nut_contours[1]) if len(nut_contours) > 1 else 0,
                                    cv2.arcLength(nut_contours[1], True) if len(nut_contours) > 1 else 0,
                                    resV[nut_id]
                                ])
                                cv2.imshow('chek', frame)

                if nut_id is not None and bbox_y1 >= end_zone:
                    nuts[nut_id].set_position(-1, -1, -1, -1)

        cv2.line(frame, (0, start_zone), (w, start_zone), (0, 0, 255), 1)
        cv2.line(frame, (0, end_zone), (w, end_zone), (0, 0, 255), 1)
        # cv2.imshow("Frame", frame)
        # cv2.imshow("python_binary", binary)
        # key = cv2.waitKey(10)
        # if key == 27:
        #     break
    print(nuts)
    ind = 0
    for elem in nuts.values():
        print(
            elem.area1,
            elem.area,
            elem.per1,
            elem.per,
            elem.cont,
            elem.apr
        )
        # forData.append(
        #     [
        #         elem.area1,
        #         elem.area,
        #         elem.per1,
        #         elem.per,
        #         elem.cont,
        #         elem.apr
        #         # resV[ind]
        #     ]
        # )
        ind += 1
    result = [i.prediction for i in nuts.values()]
    print(forData)
    print(len(forData))
    with open('forData.json', 'w') as data:
        json.dump(forData, data, indent=4)
    return result