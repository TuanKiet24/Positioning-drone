# Quản lý việc capture để không bị gọi lại

import cv2, queue, threading
from django.conf import settings
from ultralytics import YOLO

video_capture_1 = None
video_capture_2 = None
check = False # Đảm bảo chỉ chạy lần đầu tiên

queue1 = queue.Queue()
queue1.put(cv2.imread("detection/static_process/camera_img/no_image_available.jpg"))
queue2 = queue.Queue()
queue2.put(cv2.imread("detection/static_process/camera_img/no_image_available.jpg"))


model1 = None
model2 = None

bat_coi = threading.Event()

def Open_threading():
    global check
    global model1, model2
    if not check:
        check = True
        # Save model
        model1 = YOLO("detection/static_process/model/model8_1.pt")
        model2 = YOLO("detection/static_process/model/model8_1.pt")

        t1 = threading.Thread(target=_reader_1)
        t1.daemon = True
        t1.start()

        t2 = threading.Thread(target=_reader_2)
        t2.daemon = True
        t2.start()

        
        horn_thread = threading.Thread(target=play_horn)
        horn_thread.start()

import winsound
def play_horn():
    while bat_coi.is_set():
      print("Còi đang chạy...")
      # Thiết lập tần số và thời gian phát âm thanh
      frequency = 440  # Tần số (đơn vị Hz)
      duration = 2000  # Thời gian phát âm thanh (đơn vị ms)

      # Phát âm thanh hú
      winsound.Beep(frequency, duration)

def get_model(number):
    global model1, model2
    # if model == None:
    #     model = YOLO("detection/static_process/model/model8_1.pt")

    if number == 1:
       return model1
    else:
       return model2
    #return model

def Get_video_capture(IP_ADDRESS_1, IP_ADDRESS_2):
    global video_capture_1
    global video_capture_2

    if IP_ADDRESS_1 != settings.GLOBAL_STRING:
        # Khởi tạo đối tượng VideoCapture 1
        video_capture_1 = cv2.VideoCapture('rtsp://' + IP_ADDRESS_1 + '/live/ch00_1')                    #Sửa lại cho dễ
        if not video_capture_1.isOpened():
        # if True:                                                                                          #Sửa lại cho dễ
          print("Không thể kết nối đến camera ", IP_ADDRESS_1)
        else:
          print("Đã kết nối đến camera ", IP_ADDRESS_1)
          settings.GLOBAL_STRING = IP_ADDRESS_1

    if IP_ADDRESS_2 != settings.SECOND_STRING:
        # Khởi tạo đối tượng VideoCapture 2
        video_capture_2 = cv2.VideoCapture('rtsp://' + IP_ADDRESS_2 + '/live/ch00_1')                    #Sửa lại cho dễ
        if not video_capture_2.isOpened():
        # if True:                                                                                          #Sửa lại cho d
          print("Không thể kết nối đến camera ", IP_ADDRESS_2)
        else:
          print("Đã kết nối đến camera ", IP_ADDRESS_2)
          settings.SECOND_STRING = IP_ADDRESS_2

# read frames as soon as they are available, keeping only most recent one
def _reader_1():
  global video_capture_1
  global video_capture_2
  global queue1, queue2

  width = 800
  height = 450
  
  while True:
    ret1, frame1 = video_capture_1.read() #False, 1
    # cv2.imshow('Camera1', cv2.resize(frame1, (640, 360)))

    # Kiểm tra xem người dùng đã nhấn phím 'q' để thoát hay không
    # if cv2.waitKey(1) & 0xFF == ord('q'):                                                       # Để kiểm tra
    #  break

    if not ret1:
      # Đọc hình ảnh thay thế
      print("Không thể đọc khung hình từ camera 1")
      # "detection/static_process/camera_img/00310.jpg"
      image_path = "detection/static_process/camera_img/no_image_available.jpg"
      frame1 = cv2.imread(image_path)
      # frame1 = cv2.resize(frame1, (640, 360))
      # break
    # else:
      # print("Đã nhận được ảnh từ camera 1")

    if not queue1.empty():
      try:
        queue1.get_nowait()   # discard previous (unprocessed) frame
      except queue.Empty:
        pass
    
    frame1 = cv2.resize(frame1, (width, height))
    queue1.put(frame1)

def _reader_2():
  global video_capture_2
  global queue2

  width = 800
  height = 450
  
  while True:
    ret2, frame2 = video_capture_2.read() #False, 1
    # cv2.imshow('Camera2', cv2.resize(frame2, (640, 360)))

    # Kiểm tra xem người dùng đã nhấn phím 'q' để thoát hay không
    # if cv2.waitKey(1) & 0xFF == ord('q'):                                                       # Để kiểm tra
    #  break

    if not ret2:
      # Đọc hình ảnh thay thế
      # print("Không thể đọc khung hình từ camera 2")
      # "detection/static_process/camera_img/00310.jpg"
      image_path = "detection/static_process/camera_img/no_image_available.jpg"
      frame2 = cv2.imread(image_path)
      # frame2 = cv2.resize(frame2, (640, 360))
      # break
    # else:
      # print("Đã nhận được ảnh từ camera 2")

    if not queue2.empty():
      try:
        queue2.get_nowait()   # discard previous (unprocessed) frame
      except queue.Empty:
        pass

    frame2 = cv2.resize(frame2, (width, height))
    queue2.put(frame2)

def read():
  global queue1, queue2

  print("Đã read")
  
  return queue1.get(), queue2.get()
