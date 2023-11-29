import cv2
import time

# rtsp_url = "rtsp://localhost:8554/preview"
rtsp_url = "rtsp://10.0.0.53:8083/preview"
cap = cv2.VideoCapture(rtsp_url)
# cv2.imshow()
if not cap.isOpened():
    print("Failed to open RTSP stream.")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        break


    cv2.imshow(winname="RTSP Stream", mat=frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break