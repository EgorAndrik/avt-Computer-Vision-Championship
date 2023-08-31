import math
import cv2
import mediapipe as mp
import pickle
import numpy as np


with open('comandsDetcet.bf', 'rb') as model:
    modelHands = pickle.load(model)


mp_drawing = mp.solutions.drawing_utils  # Утилиты MediaPipe для рисования лица, рук и тд
mp_face_mesh = mp.solutions.face_mesh  # Утилиты MediaPipe для работы с лицом: нахождения лица, точек на лице и тд
mp_hands = mp.solutions.hands  # Утилиты MediaPipe для работы с руками: нахождение рук, точек на руках и тд
mp_drawing_styles = mp.solutions.drawing_styles  # Утилиты MediaPipe с готовыми стилями рисования


# индексы пальцев
WRIST = 0       # запястье
PALM_CENTER = 9 # центр ладони
THUMB = 4       # большой палец
INDEX = 8       # указательный палец
MIDDLE = 12     # средний палец
RING = 16       # безымянный палец
PINKY = 20      # мизинец


def catDetect(landmarks) -> str:
    # получаем координаты по y точек руки
    wrist_y = landmarks[WRIST].y
    palm_center_y = landmarks[PALM_CENTER].y
    thumb_y = landmarks[THUMB].y
    index_y = landmarks[INDEX].y
    middle_y = landmarks[MIDDLE].y
    ring_y = landmarks[RING].y
    pinky_y = landmarks[PINKY].y

    return str(modelHands.predict(np.array([wrist_y, palm_center_y, thumb_y, index_y, middle_y, ring_y, pinky_y])))


# иницилизурем детектор рук
hands = mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=1,
    model_complexity=1,
    min_detection_confidence=0.5
)


cam = cv2.VideoCapture(0)
key = 0
while key != 27:
    ret, frame = cam.read()
    if ret:
        frame = cv2.resize(frame, (576, 416))
        cv2.imshow("Frame", frame)

        image = frame.copy()

        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        # Define the drawing styles for landmarks and connections
        landmark_drawing_spec = mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=1)
        connection_drawing_spec = mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=1)

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]

            # draw landmarks
            mp_drawing.draw_landmarks(
                image=image,
                landmark_list=hand_landmarks,
                connections=mp_hands.HAND_CONNECTIONS,
                landmark_drawing_spec=landmark_drawing_spec,
                connection_drawing_spec=connection_drawing_spec,
            )

        cv2.imshow('handsDetect', image)


        image = frame.copy()

        image_h, image_w = image.shape[:2]

        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        # задаем стили для точек и их соединений
        landmark_drawing_spec = mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=1)
        connection_drawing_spec = mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=1)

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]

            # draw landmarks
            mp_drawing.draw_landmarks(
                image=image,
                landmark_list=hand_landmarks,
                connections=mp_hands.HAND_CONNECTIONS,
                landmark_drawing_spec=landmark_drawing_spec,
                connection_drawing_spec=connection_drawing_spec,
            )

            for landmark_id, landmark in enumerate(hand_landmarks.landmark):
                # преобразование координат точек из относительных [0...1] к абсолютным
                # значениям коордиант пискелей на изображении
                x = int(landmark.x * image_w)
                y = int(landmark.y * image_h)

                cv2.putText(image, f'ID: {landmark_id}', (x - 30, y - 10), cv2.FONT_HERSHEY_PLAIN, 0.9, (255, 0, 0))

        cv2.imshow('ID_Hand', image)


        image = frame.copy()

        image_h, image_w = image.shape[:2]

        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        # задаем стили для точек и их соединений
        landmark_drawing_spec = mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=1)
        connection_drawing_spec = mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=1)

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]

            # draw landmarks
            mp_drawing.draw_landmarks(
                image=image,
                landmark_list=hand_landmarks,
                connections=mp_hands.HAND_CONNECTIONS,
                landmark_drawing_spec=landmark_drawing_spec,
                connection_drawing_spec=connection_drawing_spec,
            )

            gesture = catDetect(hand_landmarks.landmark)
            cv2.putText(image, f'Gesture: {gesture}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255))

        cv2.imshow('Boost', image)
    else:
        print('end of video')

    key = cv2.waitKey(1)

cam.release()
cv2.destroyAllWindows()
