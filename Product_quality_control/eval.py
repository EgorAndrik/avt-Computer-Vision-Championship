# -*- coding: utf-8 -*-
import cv2
import numpy as np
import pickle


# TODO: Допишите импорт библиотек, которые собираетесь использовать


def detect_defective_parts(video) -> list:
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

    # i = 0
    # result = [random.randint(0, 1) for _ in range(random.choice([0, 3, 6, 9]))]  # пустой список для засенения результата
    Nut_flag = 0
    Last_nut = 0
    number_of_nuts = 0
    res = []
    with open('bestModelCBC.bf', 'rb') as model:
        modelGaki = pickle.load(model)
    while True:
        status, frame = video.read()
        if status == True:
            # h, w = frame.shape[:2]
            frame = cv2.resize(frame, (1280, 720))
            binary = cv2.inRange(frame, (0, 0, 0), (100, 100, 100))

            roy = binary[720 - 70:720 - 68, :]  # binary[h // 2 - 5:, :]
            normalIMG = frame[720 - 75:720 - 5, :]

            # roy = binary[720 - 72:720 - 70, :]  # binary[h // 2 - 5:, :]
            # normalIMG = frame[720 - 85:720 - 5, :]
            # roy = binary[720 - 70:720 - 68, :]  # binary[h // 2 - 5:, :]
            # normalIMG = frame[720 - 80:720 - 0, :]
            if np.sum(roy) > 1000:
                Nut_flag = 1
            else:
                Nut_flag = 0
            if Last_nut == 0 and Nut_flag == 1:

                binar = cv2.inRange(normalIMG, (0, 0, 0), (100, 100, 100))
                conturs, hierarchy = cv2.findContours(binar, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
                if conturs:
                    conturs = sorted(conturs, key=cv2.contourArea, reverse=True)
                    epsilon = 0.03 * cv2.arcLength(conturs[0], True)
                    approx = cv2.approxPolyDP(conturs[0], epsilon, True)

                    epsilon1 = 0.03 * cv2.arcLength(conturs[-1], True)
                    approx1 = cv2.approxPolyDP(conturs[-1], epsilon1, True)

                    area = cv2.contourArea(conturs[0])
                    per = cv2.arcLength(conturs[0], True)

                    # if area > 2000.0:
                    #     cntTmp = int(area) // 2000
                    #     data = np.array([
                    #             area,
                    #             per,
                    #             # area / per,
                    #             cv2.contourArea(conturs[-1]),
                    #             cv2.arcLength(conturs[-1], True),
                    #             # cv2.contourArea(conturs[-1]) / cv2.arcLength(conturs[-1], True),
                    #             len(conturs[0]),
                    #             len(approx),
                    #             # len(conturs[0]) / len(approx),
                    #             len(conturs[-1]),
                    #             # len(conturs[-1]) / len(approx),
                    #             len(approx1),
                    #             # len(conturs[0]) / len(approx1),
                    #             # len(conturs[-1]) / len(approx1)
                    #          ]) / cntTmp
                    #     for _ in range(cntTmp):
                    #         res.append(int(modelGaki.predict(data)))
                    # else:
                    #     res.append(
                    #         int(modelGaki.predict(
                    #             np.array([
                    #                 area,
                    #                 per,
                    #                 # area / per,
                    #                 cv2.contourArea(conturs[-1]),
                    #                 cv2.arcLength(conturs[-1], True),
                    #                 # cv2.contourArea(conturs[-1]) / cv2.arcLength(conturs[-1], True),
                    #                 len(conturs[0]),
                    #                 len(approx),
                    #                 # len(conturs[0]) / len(approx),
                    #                 len(conturs[-1]),
                    #                 # len(conturs[-1]) / len(approx),
                    #                 len(approx1),
                    #                 # len(conturs[0]) / len(approx1),
                    #                 # len(conturs[-1]) / len(approx1)
                    #             ])
                    #         ))
                    #     )

                    res.append(
                        int(modelGaki.predict(
                            np.array([
                                area,
                                per,
                                # area / per,
                                cv2.contourArea(conturs[-1]),
                                cv2.arcLength(conturs[-1], True),
                                # cv2.contourArea(conturs[-1]) / cv2.arcLength(conturs[-1], True),
                                len(conturs[0]),
                                len(approx),
                                # len(conturs[0]) / len(approx),
                                len(conturs[-1]),
                                # len(conturs[-1]) / len(approx),
                                len(approx1),
                                # len(conturs[0]) / len(approx1),
                                # len(conturs[-1]) / len(approx1)
                            ])
                        ))
                    )

                    # res.append(
                    #     round(modelGaki.predict_proba(
                    #         np.array([
                    #             area,
                    #             per,
                    #             # area / per,
                    #             cv2.contourArea(conturs[-1]),
                    #             cv2.arcLength(conturs[-1], True),
                    #             # cv2.contourArea(conturs[-1]) / cv2.arcLength(conturs[-1], True),
                    #             len(conturs[0]),
                    #             len(approx),
                    #             # len(conturs[0]) / len(approx),
                    #             len(conturs[-1]),
                    #             # len(conturs[-1]) / len(approx),
                    #             len(approx1),
                    #             # len(conturs[0]) / len(approx1),
                    #             # len(conturs[-1]) / len(approx1)
                    #         ])
                    #     )[-1])
                    # )

                    # if 8.0 < area / per <= 9.5 and \
                    #         12.8 < len(conturs[0]) / len(approx) < 20.0 and \
                    #         len(approx) == 6:
                    #     res.append(0)
                    # else:
                    #     res.append(1)
                    # if 4.5 <= area / per < 9 and len(approx) >= 6 and len(conturs[0]) / len(approx) > 19.1:
                    #     res.append(1)
                    # else:
                    #     res.append(0)
                # cv2.imshow('searcv', normalIMG)
                # cv2.waitKey(0)
                number_of_nuts += 1
            Last_nut = Nut_flag
        else:
            break

    return res
