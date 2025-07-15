import cv2
import mediapipe as mp

# Mediapipe kütüphanesini başlat
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Kamera bağlantısını açın
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Görüntüyü BGR'den RGB'ye dönüştür
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Görüntüyü Mediapipe'ye işle
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            finger_count = 0  # Parmak sayısını saklamak için bir değişken

            # Parmakları saymak için her bir uç noktayı döngüye alın
            for landmark in landmarks.landmark:
                if landmark.y < landmarks.landmark[mp_hands.HandLandmark.WRIST].y:
                    finger_count += 1

            # Parmakları çizmek için
            mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

            cv2.putText(frame, f"Finger Count: {finger_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Parmak Sayma", frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()