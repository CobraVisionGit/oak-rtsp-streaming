from datetime import timedelta
import string
from tracemalloc import start
import cv2
import time

from numpy import save
from constants import SERVER_ADDRESS, SERVER_PORT

def get_time():
    return time.time()

def calc_fps(num_frames, time_delta):
    fps = num_frames / time_delta
    fps = round(fps, 2)
    print("FPS:", fps)
    num_frames = 0
    start_time = time.time()
    return num_frames, start_time, fps

def set_text_location(frame, text_w, text_h):
    x = int((frame.shape[1] - text_w) / 20)
    y = int((frame.shape[0] + text_h) / 16)
    return x, y

def set_text():
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.0
    color = (255, 255, 255)  # White color
    thickness = 2
    return font, font_scale, color, thickness

def add_fps_to_frame(frame,txt=string):
    txt = f"FPS: {txt}"
    font, font_scale, color, thickness = set_text()
    (text_width, text_height), _ = cv2.getTextSize(txt, font, font_scale, thickness)
    X, Y = set_text_location(frame=frame, text_w= text_width, text_h=text_height)
    cv2.putText(frame, txt, (X, Y), font, font_scale, color, thickness)

def display_pixel_value(event, x, y, flags, param):
    save_count = 0
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel_value = image_rgb[y, x]
        print("Pixel value at (x={}, y={}): {}".format(x, y, pixel_value))

def capture_frames(frame, frame_count, num_to_cap, save_count):
     
     if frame_count in range(110,120) and save_count <= num_to_cap:
        cv2.imwrite(f'output_frame{frame_count}.jpg', frame)
        save_count+=1

# rtsp_url = "rtsp://localhost:8554/preview"
rtsp_url = f"rtsp://{SERVER_ADDRESS}:{SERVER_PORT}/preview"
print(rtsp_url)
buffer_size = 1
        
cap = cv2.VideoCapture(rtsp_url)
cap.set(cv2.CAP_PROP_BUFFERSIZE, buffer_size)

fps = 0.0
num_frames_to_capture = 10
count = 0
save_count = 0
frame_count = 0
start_time = get_time()
save_frames = True
# cv2.imshow()
if not cap.isOpened():
    print("Failed to open RTSP stream.")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        break
    count+=1
    frame_count += 1
    # print(count)

    time_delta = get_time() - start_time
        # time.sleep(1)
    if time_delta > 1.0:
        frame_count, start_time, fps = calc_fps(num_frames= frame_count, time_delta=time_delta)
    
    add_fps_to_frame(frame=frame, txt=fps)

    cv2.namedWindow("RTSP Stream", cv2.WINDOW_NORMAL)
    cv2.imshow(winname="RTSP Stream", mat=frame)

    if save_frames:
        capture_frames(frame=frame, frame_count=count, num_to_cap=num_frames_to_capture, save_count=save_count)
        # if frame_count in range(110,120) and save_count <= num_frames_to_capture:
        #     cv2.imwrite(f'output_frame{count}.jpg', frame)
        #     save_count+=1
        

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break