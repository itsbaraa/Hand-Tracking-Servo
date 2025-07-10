import cv2, mediapipe as mp, serial, time

ARDUINO_PORT = 'COM3'
arduino = serial.Serial(ARDUINO_PORT, 115200, timeout=1, write_timeout=None)
time.sleep(2)

mp_hands = mp.solutions.hands.Hands(max_num_hands=1)
draw     = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

last_angle = None 
last_sent  = 0.0

try:
    while cap.isOpened():
        ok, frame = cap.read()
        if not ok:
            time.sleep(0.01)
            continue
        frame = cv2.flip(frame, 1)

        res = mp_hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if res.multi_hand_landmarks:
            # Index-finger tip X coordinate
            tip_x = res.multi_hand_landmarks[0].landmark[8].x
            angle = max(0, min(int(tip_x * 180), 180))    # clamp 0–180
            now = time.time()
            # Send only if angle changed by ≥2° and at most 10 Hz
            if (last_angle is None or abs(angle - last_angle) >= 2) and now - last_sent > 0.1:
                try:
                    if arduino.out_waiting < 50:
                        arduino.write(f"{angle}\n".encode())
                    else:
                        # skip this frame if buffer backed up
                        pass
                    last_angle = angle
                    last_sent  = now
                except serial.SerialTimeoutException:
                    # Buffer full — skip this frame and continue
                    pass

            draw.draw_landmarks(frame, res.multi_hand_landmarks[0],
                                mp.solutions.hands.HAND_CONNECTIONS)
            cv2.putText(frame, f"{angle:3d}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        cv2.imshow("Hand-Servo", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    cap.release()
    cv2.destroyAllWindows()
    arduino.close()
