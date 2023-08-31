# -*- coding: utf-8 -*-
from typing import Tuple
import cv2
import numpy as np
import dlib


# TODO: Импортируйте библиотеки, которые собираетесь использовать


def detect_logo(image) -> Tuple[str, Tuple]:
    """
        Функция для детектирования логотипов

        Входные данные: изображение (bgr), прочитано cv2.imread
        Выходные данные: кортеж (Tuple) с названием логотипа и координатами ограничивающей рамки
            (label, (x, y, w, h)),
                где label - строка с названием логотипа;
                x, y - целочисленные координаты левого верхнего угла рамки, ограничивающей логотип;
                w, h - целочисленные ширина и высота рамки, ограничивающей логотип.

        Примечание: Логотип на изображение всегда ровно один!

        Возможные название логотипов:
            cpp, avt, python, altair, kruzhok.

        Примеры вывода:
            ('cpp', (12, 23, 20, 20))

            ('avt', (403, 233, 45, 60))
    """

    # TODO: Отредактируйте эту функцию по своему усмотрению.
    # Для удобства можно создать собственные функции в этом файле.
    # Алгоритм проверки будет вызывать функцию detect_logo, остальные функции должны вызываться из неё.

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    kruzhok_model = dlib.simple_object_detector('detection/kruzhok.svm')
    altair_model = dlib.simple_object_detector('detection/altair.svm')
    cpp_model = dlib.simple_object_detector('detection/cPP.svm')
    python_model = dlib.simple_object_detector('detection/pythonImg.svm')
    avt_model = dlib.simple_object_detector('detection/avt.svm')

    conturs_kruzhok, conturs_altair = kruzhok_model(image), altair_model(image)
    conturs_cpp, conturs_python = cpp_model(image), python_model(image)
    conturs_avt = avt_model(image)
    if len(conturs_kruzhok):
        x, y, h, w = [conturs_kruzhok[0].left(), conturs_kruzhok[0].top(),
                   conturs_kruzhok[0].right(), conturs_kruzhok[0].bottom()]
        return (
            "kruzhok",
            (x, y, h - x, w - y)
        )
    elif len(conturs_altair):
        x, y, w, h = [conturs_altair[0].left(), conturs_altair[0].top(),
                      conturs_altair[0].right(), conturs_altair[0].bottom()]
        return (
            "altair",
            (x, y, w - x, h - y)
        )
    elif len(conturs_cpp):
        x, y, w, h = [conturs_cpp[0].left(), conturs_cpp[0].top(),
                      conturs_cpp[0].right(), conturs_cpp[0].bottom()]
        return (
            "cpp",
            (x, y, w - x, h - y)
        )
    elif len(conturs_python):
        x, y, w, h = [conturs_python[0].left(), conturs_python[0].top(),
                      conturs_python[0].right(), conturs_python[0].bottom()]
        return (
            "python",
            (x, y, w - x, h - y)
        )
    elif len(conturs_avt):
        x, y, w, h = [conturs_avt[0].left(), conturs_avt[0].top(),
                   conturs_avt[0].right(), conturs_avt[0].bottom()]
        return (
            "avt",
            (x, y, w - x, h - y)
        )
