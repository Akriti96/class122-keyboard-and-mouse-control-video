import cv2
import mediapipe as mp


from pynput.keyboard import Key,Controller

state=None

keyBoard=Controller()

cap = cv2.VideoCapture(0)

drawing = mp.solutions.drawing_utils
hands = mp.solutions.hands

width=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print(width)
print(height)


hands_obj = hands.Hands(min_detection_confidence=0.75,
                        min_tracking_confidence=0.75,
                        max_num_hands=4)


def count_fingers(lst):
    global state
    cnt = 0

    thresh = (lst.landmark[0].y*100 - lst.landmark[9].y*100)/2

    if (lst.landmark[5].y*100 - lst.landmark[8].y*100) > thresh:
        cnt += 1

    if (lst.landmark[9].y*100 - lst.landmark[12].y*100) > thresh:
        cnt += 1

    if (lst.landmark[13].y*100 - lst.landmark[16].y*100) > thresh:
        cnt += 1

    if (lst.landmark[17].y*100 - lst.landmark[20].y*100) > thresh:
        cnt += 1

    # if (lst.landmark[5].x*100 - lst.landmark[4].x*100) > 6:
    #     cnt += 1

    totalFingers= cnt
    if totalFingers == 4:
        state="play"
    if totalFingers == 0 and state=="play":
        state="pause"
        keyBoard.press(Key.space)

    # move the video forward and backward
    finger_tip_x=(lst.landmark[8].x)*width

    if totalFingers == 1:
        if finger_tip_x<width-400:
            print("play backward")
            keyBoard.press(Key.left)
        if finger_tip_x>width-50:
            print("Play forward")
            keyBoard.press(Key.right)
  

    print("what is video state: ",state)
    return totalFingers


while True:
    success, image = cap.read()
    image = cv2.flip(image, 1)
    result = hands_obj.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    if result.multi_hand_landmarks:

        hand_keyPoints = result.multi_hand_landmarks[0]

        c = count_fingers(hand_keyPoints)
        # print(c)
        cv2.putText(image, "Fingures "+str(c), (200, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        drawing.draw_landmarks(image, hand_keyPoints, hands.HAND_CONNECTIONS)

    cv2.imshow("Media Controller", image)

    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()
