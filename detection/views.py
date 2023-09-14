from django.shortcuts import render
# from django.http import HttpResponse
from .models import *
# from django.core.mail import EmailMessage
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
from django.http import JsonResponse
from .Processor import process_image_from_camera
import cv2
import base64

# from PIL import Image
# from django.core.files.storage import default_storage
# from django.core.files.base import ContentFile

from .camera_manager import Get_video_capture, read, Open_threading

# Create your views here.
@gzip.gzip_page
def index(request):
    return render(request, 'detection/my_template.html')
    try:
        cam1 = VideoCamera()
        cam2 = VideoCamera()
        return StreamingHttpResponse(gen(cam1), content_type="multipart/x-mixed-replace;boundary=frame")
        return StreamingHttpResponse(gen(cam2), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass     

import time, random, os
def get_image_from_camera(IP_camera_1,IP_camera_2):
    Get_video_capture(IP_camera_1, IP_camera_2)

    Open_threading()     # (+ việc lấy model)

    # Phụ: Lấy hình ảnh về máy
    #path = 'detection/abc/'                                                                           # Phụ
    
    image_from_camera_1, image_from_camera_2 = read()
    # image_from_camera_1 = read(1)
    # _, width_1,_ = image_from_camera_1.shape
    # if width_1 < 700:
    #     print("Không thể đọc khung hình từ camera ", IP_camera_1)
    # else:
    #     print("Đã nhận được ảnh từ camera ", IP_camera_1)
    #     #random1 = random.randint(1, 100000)                                                             # Phụ
    #     #cv2.imwrite(os.path.join(path, 'frame_' + str(random1) + '.jpg'),image_from_camera_1)           # Phụ

    # image_from_camera_2 = read(2)
    # _, width_2,_ = image_from_camera_2.shape
    # if width_2 < 700:
    #     print("Không thể đọc khung hình từ camera ", IP_camera_2)
    # else:
    #     print("Đã nhận được ảnh từ camera ", IP_camera_2)
    #     #random2 = random.randint(1, 100000)                                                             # Phụ
    #     #cv2.imwrite(os.path.join(path, 'frame_' + str(random2) + '.jpg'),image_from_camera_2)           # Phụ

    return image_from_camera_1, image_from_camera_2

def calib(image):
    # Kích thước ảnh
    image_height, image_width, _ = image.shape

    # Kích thước dấu cộng
    cross_size = min(image_width, image_height) // 30

    # Tọa độ x, y của điểm giữa ảnh
    center_x = image_width // 2
    center_y = image_height // 2

    # Vẽ dấu cộng
    cv2.line(image, (center_x - cross_size, center_y),
            (center_x + cross_size, center_y), (255, 0, 0), 2)
    cv2.line(image, (center_x, center_y - cross_size),
            (center_x, center_y + cross_size), (255, 0, 0), 2)
    
    return image

# import json
def stream_view(request):
    # IP của hai camera
    time_start = time.time()
    IP_camera_1 = request.GET.get('ip_camera_1')
    IP_camera_2 = request.GET.get('ip_camera_2')
    IP_jammer = request.GET.get('ip_jammer')
    
    x_coordinate_of_camera_1_str = request.GET.get('x_coordinate_of_camera_1')
    if x_coordinate_of_camera_1_str != '':
        x_coordinate_of_camera_1 = int(x_coordinate_of_camera_1_str)
    else:
        x_coordinate_of_camera_1 = 0
    y_coordinate_of_camera_1_str = request.GET.get('y_coordinate_of_camera_1')
    if y_coordinate_of_camera_1_str != '':
        y_coordinate_of_camera_1 = int(y_coordinate_of_camera_1_str)
    else:
        y_coordinate_of_camera_1 = 0
    z_coordinate_of_camera_1_str = request.GET.get('z_coordinate_of_camera_1')
    if z_coordinate_of_camera_1_str != '':
        z_coordinate_of_camera_1 = int(z_coordinate_of_camera_1_str)
    else:
        z_coordinate_of_camera_1 = 0
    theta_angle_of_camera_1_str = request.GET.get('theta_angle_of_camera_1')
    if theta_angle_of_camera_1_str != '':
        theta_angle_of_camera_1 = int(theta_angle_of_camera_1_str)
    else:
        theta_angle_of_camera_1 = 45
    phi_angle_of_camera_1_str = request.GET.get('phi_angle_of_camera_1')
    if phi_angle_of_camera_1_str != '':
        phi_angle_of_camera_1 = int(phi_angle_of_camera_1_str)
    else:
        phi_angle_of_camera_1 = 45

    x_coordinate_of_camera_2_str = request.GET.get('x_coordinate_of_camera_2')
    if x_coordinate_of_camera_2_str != '':
        x_coordinate_of_camera_2 = int(x_coordinate_of_camera_2_str)
    else:
        x_coordinate_of_camera_2 = 0
    y_coordinate_of_camera_2_str = request.GET.get('y_coordinate_of_camera_2')
    if y_coordinate_of_camera_2_str != '':
        y_coordinate_of_camera_2 = int(y_coordinate_of_camera_2_str)
    else:
        y_coordinate_of_camera_2 = 0
    z_coordinate_of_camera_2_str = request.GET.get('z_coordinate_of_camera_2')
    if z_coordinate_of_camera_2_str != '':
        z_coordinate_of_camera_2 = int(z_coordinate_of_camera_2_str)
    else:
        z_coordinate_of_camera_2 = 0
    theta_angle_of_camera_2_str = request.GET.get('theta_angle_of_camera_2')
    if theta_angle_of_camera_2_str != '':
        theta_angle_of_camera_2 = int(theta_angle_of_camera_2_str)
    else:
        theta_angle_of_camera_2 = 45
    phi_angle_of_camera_2_str = request.GET.get('phi_angle_of_camera_2')
    if phi_angle_of_camera_2_str != '':
        phi_angle_of_camera_2 = int(phi_angle_of_camera_2_str)
    else:
        phi_angle_of_camera_2 = 135

    x_coordinate_of_jammer_str = request.GET.get('x_coordinate_of_jammer')
    if x_coordinate_of_jammer_str != '':
        x_coordinate_of_jammer = int(x_coordinate_of_jammer_str)
    else:
        x_coordinate_of_jammer = 0
    y_coordinate_of_jammer_str = request.GET.get('y_coordinate_of_jammer')
    if y_coordinate_of_jammer_str != '':
        y_coordinate_of_jammer = int(y_coordinate_of_jammer_str)
    else:
        y_coordinate_of_jammer = 0
    z_coordinate_of_jammer_str = request.GET.get('z_coordinate_of_jammer')
    if z_coordinate_of_jammer_str != '':
        z_coordinate_of_jammer = int(z_coordinate_of_jammer_str)
    else:
        z_coordinate_of_jammer = 0

    threshold_predict_str = request.GET.get('threshold_predict')
    if threshold_predict_str != '':
        threshold_predict = int(threshold_predict_str)
    else:
        threshold_predict = 0
    goc_camera_str = request.GET.get('goc_camera')
    if goc_camera_str != '':
        goc_camera = int(goc_camera_str)
    else:
        goc_camera = 90
    
    theta_angle_of_jammer_str = request.GET.get('theta_angle_of_jammer')
    if theta_angle_of_jammer_str != '':
        theta_angle_of_jammer = int(theta_angle_of_jammer_str)
    else:
        theta_angle_of_jammer = 0
    phi_angle_of_jammer_str = request.GET.get('phi_angle_of_jammer')
    if phi_angle_of_jammer_str != '':
        phi_angle_of_jammer = int(phi_angle_of_jammer_str)
    else:
        phi_angle_of_jammer = 135


    time_get_IP = time.time()
    print("Time get IP = ", time_get_IP - time_start)
    
    # Lấy hình ảnh từ camera IP
    camera1_image, camera2_image = get_image_from_camera(IP_camera_1,IP_camera_2)  # Thay thế bằng hàm lấy hình ảnh từ camera IP 1
    time_get_img = time.time()
    print("Time get image = ", time_get_img - time_get_IP)
    
    # Lấy hình ảnh trực tiếp và xử lý hình ảnh từ camera IP bằng file Processor.py
    processed_image1, processed_image2, coordinate = process_image_from_camera(camera1_image, camera2_image, x_coordinate_of_camera_1, y_coordinate_of_camera_1,
                                                                               z_coordinate_of_camera_1, theta_angle_of_camera_1, phi_angle_of_camera_1,  x_coordinate_of_camera_2, y_coordinate_of_camera_2,
                                                                               z_coordinate_of_camera_2, theta_angle_of_camera_2, phi_angle_of_camera_2, x_coordinate_of_jammer, y_coordinate_of_jammer,
                                                                               z_coordinate_of_jammer, threshold_predict, goc_camera, theta_angle_of_jammer, phi_angle_of_jammer, IP_jammer)
    time_process = time.time()
    print("Time process = ", time_process - time_get_img)

    # Vẽ một dấy cộng ở giữa bức hình để calib
    processed_image1 = calib(processed_image1)
    processed_image2 = calib(processed_image2)
    
    _ , buffer_1 = cv2.imencode('.jpg', processed_image1)
    # retval_2
    _ , buffer_2 = cv2.imencode('.jpg', processed_image2)

    base64_image1 = base64.b64encode(buffer_1).decode('utf-8')
    base64_image2 = base64.b64encode(buffer_2).decode('utf-8')

    # Đóng gói các ảnh thành đối tượng JSON
    response = {
        'image1': base64_image1,
        'image2': base64_image2,
        'coordinate': coordinate
    }

    time_end = time.time()
    print("Time đóng gói = ", time_end - time_process)
    print("Thời gian xử lý toàn bộ là: ", time_end - time_start)

    return JsonResponse(response)

import socket,json
from django.conf import settings

def jamming(request):
    # ip_jammer = request.GET.get('ip_jammer')  # Lấy dữ liệu từ request
    # print("Đã nhận được ip: ", ip_jammer)
    # port = 8266
    # data = settings.SEND_JAMMER
    # data_str = json.dumps(data)

    # try:
    #     # Tạo socket và kết nối đến ESP8266
    #     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     sock.connect((ip_jammer, port))
    #     print("Connected to ESP8266")

    #     # Gửi dữ liệu đến ESP8266
    #     sock.sendall(data_str.encode())
    #     print("Data sent:", data_str)

    #     # Đợi phản hồi từ ESP8266 (nếu cần)
    #     response = sock.recv(1024)
    #     print("Response received:", response.decode())

    #     # Đóng kết nối
    #     sock.close()
    #     print("Connection closed")
    # except Exception as e:
    #     print("Error:", str(e))
    
    return JsonResponse({'status': 'success'})  # Gửi phản hồi JSON nếu xử lý thành công