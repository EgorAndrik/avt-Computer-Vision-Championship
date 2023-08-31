# -*- coding: utf-8 -*-
from typing import Tuple

import cv2
import numpy as np
# TODO: Допишите импорт библиотек, которые собираетесь использовать


def load_models():
    """ Функция осуществляет загрузку модели(ей) нейросети(ей) из файла(ов).
        Выходные параметры: загруженный(е) модели(и)

        Если вы не собираетесь использовать эту функцию, пусть возвращает пустой список []
        Если вы используете несколько моделей, возвращайте их список [model1, model2]

        То, что вы вернёте из этой функции, будет передано вторым аргументом в функцию detect_traffic_light
    """

    # TODO: Отредактируйте функцию по своему усмотрению.
    # Модель нейронной сети, загрузите на онайн-платформу вместе с eval.py.

    # Пример загрузки моделей из файлов
    # Yolo-модели
    # net = cv2.dnn.readNetFromDarknet('yolo.cfg', 'yolo.weights')
    # yolo_model = cv2.dnn_DetectionModel(net)
    # yolo_model.setInputParams(scale=1/255, size=(416, 416), swapRB=True)
    # models = [yolo_model]

    # Пример загрузки модели TensorFlow (не забудьте импортировать библиотеку tensorflow)
    # tf_model = tf.keras.models.load_model('model.h5')
    # models.append(tf_model)
    # models = [yolo_model]
    net = cv2.dnn.readNet('yolov4-tiny-obj_best.weights', 'yolov4-tiny-obj.cfg')

    yoloCVmodel = cv2.dnn_DetectionModel(net)
    yoloCVmodel.setInputParams(size=(416, 416), scale=1 / 255, swapRB=True)

    models = [yoloCVmodel]
    return models


def detect_traffic_light(image, models) -> Tuple:
    """
        Функция для детектирования сфетофоров.

        Входные данные: изображение (bgr), прочитано cv2.imread
        Выходные данные: кортеж (tuple) с координатами рамки, ограничивающей светофор на изображении
            в формате: (x, y, w, h),
            где x, y - целочисленные координаты верхнего левого угла ограничивающей рамки,
            w, h - целочисленные ширина и высота ограничивающей рамки.

        Примеры вывода:
            (12, 23, 20, 20)

            (403, 233, 45, 60)

    """

  # TODO: Отредактируйте эту функцию по своему усмотрению.
    # Для удобства можно создать собственные функции в этом файле.
    # Алгоритм проверки один раз вызовет функцию load_models
    # и для каждого тестового изображения будет вызывать функцию detect_traffic_light
    # Все остальные функции должны вызываться из вышеперечисленных.

    yolo_model = models[0]
    classes, scores, boxes = yolo_model.detect(image, 0.5, 0.4)
    if len(boxes):
        bbox = boxes[0]
        x, y, w, h = [i for i in bbox]
        # cv2.rectangle(image, (x, y), (w + x, h + y), (255, 255, 0), thickness=2)
        # cv2.imshow("contur", image)
        # cv2.waitKey(0)
        return (
            int(x), int(y), int(w), int(h)
        )
    bbox = (0, 0, 0, 0)
    return bbox
