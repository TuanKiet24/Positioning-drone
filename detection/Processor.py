import time
import cv2
import numpy as np
from ultralytics import YOLO
import math
import random
import os
from django.conf import settings
from .camera_manager import get_model, bat_coi
import winsound
import threading



def run_model(image):
    # Model để detect
    model = get_model(1)

    threshold_detect = 0.2
    class_name_dict = { 0: 'Drone', 1: 'Bird'}
    results = model(image)[0]
    list_drone = []
    
    # Xử lý hình ảnh (Vẽ khung chữ nhật xung quanh drone)
    # Lấy thông tin từ hình ảnh
    # Lấy những kết quả có drone vào list_drone
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > threshold_detect and int(class_id) == 0:
            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 1)
            cv2.putText(image, class_name_dict[int(class_id)].upper() + " - "+str(round(score*100, 0))+"%", (int(x1), int(y1 - 5)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5 , (0, 0, 255), 1, cv2.LINE_AA)
            
            height, width, _ = image.shape
            x = (x1 + x2 - width) / (2 * width)                 # x,y = [-0.5,0.5]
            y = - (y1 + y2 - height) / (2 * height)
            list_drone.append([x,y,score])                                             
    
    return image, list_drone

def distance_between_lines(line1, line2):
    # Đường thẳng thứ nhất đi qua 2 điểm A và B
    A1 = line1[0]
    B1 = line1[1]
    v1 = B1 - A1

    # Đường thẳng thứ hai đi qua 2 điểm C và D
    A2 = line2[0]
    B2 = line2[1]
    v2 = B2 - A2

    # Tìm vecto pháp tuyến chung
    vecto_n = np.cross(v1, v2)                             #??? Phải chuyển về vector đơn vị (ko)
    # length = np.linalg.norm(n)
    # vecto_n = n / length

    # Tìm mặt phẳng đi qua line2 và vecto pháp tuyến là vecto_n
    # vecto_n[0]*x + vecto_n[1]*y + vecto_n[2]*z + D = 0
    D = -np.dot(A2, vecto_n)

    # Tìm hình chiếu của A1 xuống mặt phẳng
    proj_A1 = A1 - (np.dot(A1, vecto_n) + D) / np.dot(vecto_n, vecto_n) * vecto_n

    # Tìm giao điểm của đường thẳng proj_A1 + t*v1 và đường thẳng line2_start + s*line2_direction
    v1_equation = [v1[0], -v2[0]]
    v2_equation = [v1[1], -v2[1]]
    A = [v1_equation, v2_equation]
    b = [A2[0] - proj_A1[0], A2[1] - proj_A1[1]]
    t,s = np.linalg.solve(A, b)
    m2 = proj_A1 + t*v1

    # Tìm hình chiếu m2 lên đường thẳng line1
    # Tính vector chỉ phương của đường thẳng
    u = v1 / np.linalg.norm(v1)

    # Tìm giao điểm giữa vector m2 và vector u
    p = A1 + np.dot((m2 - A1), u) * u

    # Tính hình chiếu của điểm m2 xuống đường thẳng
    m1 = p

    # Tính khoảng cách ngắn nhất giữa 2 đường thẳng
    distance = np.linalg.norm(m1 - m2)
    # print("m1 = ", m1)
    # print("m2 = ", m2)
    # print("distance = ", distance)

    return distance, (m1+m2)/2

# def qualified_distance(x1,y1,x2,y2):
    
    
#     # print("distance =", distance)
#     return check, midpoint

def spherical_to_cartesian(r, theta, phi):
    x = r * math.cos(theta) * math.cos(phi)
    y = r * math.cos(theta) * math.sin(phi)
    z = r * math.sin(theta)
    return x, y, z

def find_intersection(line1, line2):
    # Lấy thông tin về các hệ số của đường thẳng thứ nhất
    a1, b1, c1 = line1

    # Lấy thông tin về các hệ số của đường thẳng thứ hai
    a2, b2, c2 = line2

    # Tính delta
    delta = a1 * b2 - a2 * b1

    # Kiểm tra nếu delta bằng 0, tức là hai đường thẳng song song hoặc trùng nhau
    if delta == 0:
        return None  # Không có giao điểm

    # Tính toán tọa độ của điểm giao điểm
    x = (b1 * c2 - b2 * c1) / delta
    y = (a2 * c1 - a1 * c2) / delta

    # Trả về tọa độ của điểm giao điểm
    return x, y

def play_horn():
    print("Còi đang chạy...")
    # Thiết lập tần số và thời gian phát âm thanh
    frequency = 440  # Tần số (đơn vị Hz)
    duration = 5000  # Thời gian phát âm thanh (đơn vị ms)

    # Phát âm thanh hú
    winsound.Beep(frequency, duration)

def angle_jamming(drone_coordinates, coordinate_of_jammer, phi_angle_of_jammer, theta_angle_of_jammer):
    # Tính hướng phát tín hiệu jamming
    
    # Lấy tọa độ drone đầu để jamming
    drone_coordinates_1 = drone_coordinates[0]
    vector_jammer = drone_coordinates_1 - coordinate_of_jammer
    print("vector_jammer = ",vector_jammer)

    # Tính ra giá trị 2 góc [góc phương vị, góc nâng]
    phi_angle_of_jammer_to_drone = math.degrees(math.atan(vector_jammer[1]/vector_jammer[0])) - phi_angle_of_jammer
    
    if phi_angle_of_jammer_to_drone < -90:
        phi_angle_of_jammer_to_drone = phi_angle_of_jammer_to_drone + 180
    elif phi_angle_of_jammer_to_drone > 90:
        phi_angle_of_jammer_to_drone = phi_angle_of_jammer_to_drone - 180
        
    theta_angle_of_jammer_to_drone = math.degrees(math.atan(vector_jammer[2] / math.sqrt(vector_jammer[0]**2 + vector_jammer[1]**2)))
    send_jammer = [phi_angle_of_jammer_to_drone, theta_angle_of_jammer_to_drone]
    
    print(send_jammer)
    return send_jammer

# import keyboard
def process_image_from_camera(image_from_camera_1, image_from_camera_2, x_coordinate_of_camera_1, y_coordinate_of_camera_1,
    z_coordinate_of_camera_1, theta_angle_of_camera_1, phi_angle_of_camera_1,  x_coordinate_of_camera_2, y_coordinate_of_camera_2,
    z_coordinate_of_camera_2, theta_angle_of_camera_2, phi_angle_of_camera_2, x_coordinate_of_jammer, y_coordinate_of_jammer,
    z_coordinate_of_jammer, threshold_predict, goc_camera, theta_angle_of_jammer, phi_angle_of_jammer, IP_jammer):
    # Kiểm tra tọa độ đã được lưu trong database chưa, nếu chưa thì yêu cầu người dùng nhập

    event = threading.Event()
    image_fix_2 = None 
    list_drone_from_camera_2 = None
    def run_model_2():
        nonlocal image_fix_2, list_drone_from_camera_2
        nonlocal image_from_camera_2

        # Model để detect
        model = get_model(2)

        threshold_detect = 0.2
        class_name_dict = { 0: 'Drone', 1: 'Bird'}
        # cv2.imshow('Camera2', cv2.resize(image_from_camera_2, (640, 360)))
        # keyboard.wait('enter')
        results = model(image_from_camera_2)[0]
        list_drone = []
        
        # Xử lý hình ảnh (Vẽ khung chữ nhật xung quanh drone)
        # Lấy thông tin từ hình ảnh
        # Lấy những kết quả có drone vào list_drone
        for result in results.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = result

            if score > threshold_detect and int(class_id) == 0:
                cv2.rectangle(image_from_camera_2, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 1)
                cv2.putText(image_from_camera_2, class_name_dict[int(class_id)].upper() + " - "+str(round(score*100, 0))+"%", (int(x1), int(y1 - 5)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5 , (0, 0, 255), 1, cv2.LINE_AA)
                
                height, width, _ = image_from_camera_2.shape
                x = (x1 + x2 - width) / (2 * width)                 # x,y = [-0.5,0.5]
                y = - (y1 + y2 - height) / (2 * height)
                list_drone.append([x,y,score])                                             
        
        image_fix_2 = image_from_camera_2
        list_drone_from_camera_2 = list_drone
        event.set()
        # return image, list_drone

    # Luồng còi
    horn_thread = None
    
    # Ngưỡng hay độ nhạy detect (Đọc giá trị từ giao diện)
    # threshold_predict = 0.5
    threshold_predict = threshold_predict / 100
    # print("threshold_predict = ", threshold_predict)

    # Góc rộng và góc đứng camera
    # goc_camera = 90
    goc_camera = math.radians(goc_camera)
    # goc_rong = 2 * math.degrees(math.atan((16 * math.tan(math.radians(goc_camera)/2)) / (math.sqrt(9**2 + 16**2))))
    # goc_dung = 2 * math.degrees(math.atan((9 * math.tan(math.radians(goc_camera)/2)) / (math.sqrt(9**2 + 16**2))))

    # Biến lưu trữ thông tin của N = 10 hình ảnh gần nhất
    # Giá trị ban đầu là 10 danh sách con trống
    N = 10
    list_N_latest_infor = settings.GLOBAL_LIST                    # N = 10                  ????? Nên để rỗng hay để tập 0

    # Tọa độ và góc của camera
    # x_coordinate_of_camera_1 = 0
    # y_coordinate_of_camera_1 = 0
    # z_coordinate_of_camera_1 = 85
    # theta_angle_of_camera_1 = 45                    # Góc nâng = 45 độ
    # phi_angle_of_camera_1 = 45                      # Góc phương vị = 45 độ
    """ print("x_coordinate_of_camera_1 = ",x_coordinate_of_camera_1)
    print("y_coordinate_of_camera_1 = ",y_coordinate_of_camera_1)
    print("z_coordinate_of_camera_1 = ",z_coordinate_of_camera_1)
    print("theta_angle_of_camera_1 = ",theta_angle_of_camera_1)
    print("phi_angle_of_camera_1 = ",phi_angle_of_camera_1) """

    theta_angle_of_camera_1 = math.radians(theta_angle_of_camera_1)
    phi_angle_of_camera_1 = math.radians(phi_angle_of_camera_1)

    # Tìm hiểu về góc trong tọa độ cầu
    # https://vi.wikipedia.org/wiki/Hệ_tọa_độ_cầu

    # x_coordinate_of_camera_2 = 900        # 1000 cm = 10m
    # y_coordinate_of_camera_2 = 900         # 1000 cm = 10m
    # z_coordinate_of_camera_2 = 85
    # theta_angle_of_camera_2 = 45                    # Góc nâng = 45 độ
    # phi_angle_of_camera_2 = -135                   # Góc phương vị = -135 độ

    theta_angle_of_camera_2 = math.radians(theta_angle_of_camera_2)
    phi_angle_of_camera_2 = math.radians(phi_angle_of_camera_2)

    # Tọa độ Jammer
    # x_coordinate_of_jammer = 1000
    # y_coordinate_of_jammer = 0
    # z_coordinate_of_jammer = 0
    coordinate_of_jammer = np.array([x_coordinate_of_jammer, y_coordinate_of_jammer, z_coordinate_of_jammer])

    #theta_angle_of_jammer = 0 # Nhớ đổi về độ
    #phi_angle_of_jammer = 135    
    
    # Lấy thông tin và xử lý hình ảnh từ camera 1
    thread2 = threading.Thread(target=run_model_2)
    thread2.start()
    image_fix_1, list_drone_from_camera_1 = run_model(image_from_camera_1)
    event.wait()
    # image_fix_2, list_drone_from_camera_2 = run_model(image_from_camera_2)

    print("list_drone_from_camera_1 = ", list_drone_from_camera_1)
    print("list_drone_from_camera_2 = ", list_drone_from_camera_2)

    # Lùi kết quả
    for i in range(N - 1):
        list_N_latest_infor[i] = list_N_latest_infor[i+1]
    
    # Từ hai thông tin của 2 ảnh, ta phân tích về một thông tin bao quát
    # Tọa độ drone
    drone_coordinates = []

    # Lưu trữ kết quả phân tích vào list N mới nhất
    if list_drone_from_camera_1 == [] and list_drone_from_camera_2 == []:
        list_N_latest_infor[N-1] = 0
    elif list_drone_from_camera_1 == [] and list_drone_from_camera_2 != []:
        sublist = []
        for sublist1 in list_drone_from_camera_2:
            sublist.append(sublist1[2])
        list_N_latest_infor[N-1] = sum(sublist) / len(sublist) / 2
    elif list_drone_from_camera_1 != [] and list_drone_from_camera_2 == []:
        sublist = []
        for sublist1 in list_drone_from_camera_1:
            sublist.append(sublist1[2])
        list_N_latest_infor[N-1] = sum(sublist) / len(sublist) / 2
    else:
        for i in list_drone_from_camera_1:
            for j in list_drone_from_camera_2:
                # Tọa độ mặc định của drone
                mid = np.array([0,0,0])
                x1 = i[0] * 16
                y1 = i[1] * 9
                x2 = j[0] * 16
                y2 = j[1] * 9

                # Ảnh 1
                # Tìm tọa độ tâm ảnh 1 theo tỉ lệ (16/9)
                # Độ dài tiêu cự camera 1
                TC1 = math.sqrt(9**2 + 16**2) / (2 * math.tan(goc_camera/2))
                coordinate_of_image_1_center = spherical_to_cartesian(TC1, theta_angle_of_camera_1, phi_angle_of_camera_1)
                
                # Chiếu ảnh lên mặt phẳng Oxy
                # coordinate_of_image_1_center_Oxy = [coordinate_of_image_1_center[0], coordinate_of_image_1_center[1]]
                
                phi_x1_Oxy = math.atan(- x1 / math.sqrt(coordinate_of_image_1_center[0]**2 + coordinate_of_image_1_center[1]**2)) + phi_angle_of_camera_1
                r_x1_Oxy = math.sqrt(coordinate_of_image_1_center[0]**2 + coordinate_of_image_1_center[1]**2 + x1**2)
                r_y1_Oxy = math.sqrt(coordinate_of_image_1_center[0]**2 + coordinate_of_image_1_center[1]**2) - y1*math.sin(theta_angle_of_camera_1)

                x1_Oxy = spherical_to_cartesian(r_x1_Oxy, 0, phi_x1_Oxy)
                y1_Oxy = spherical_to_cartesian(r_y1_Oxy, 0, phi_angle_of_camera_1)

                # Chiếu điểm drone lên mặt phẳng Oxy
                # print("coordinate_of_image_1_center = [{}, {}, {}]".format(coordinate_of_image_1_center[0], coordinate_of_image_1_center[1], coordinate_of_image_1_center[2]))
                line1_Oxy = (coordinate_of_image_1_center[0], coordinate_of_image_1_center[1], - coordinate_of_image_1_center[0] * y1_Oxy[0] - coordinate_of_image_1_center[1] * y1_Oxy[1])
                line2_Oxy = (- coordinate_of_image_1_center[1], coordinate_of_image_1_center[0], coordinate_of_image_1_center[1] * x1_Oxy[0] - coordinate_of_image_1_center[0] * x1_Oxy[1])
                # print("line1_Oxy = {}              line2_Oxy = {}".format(line1_Oxy, line2_Oxy))
                sub_x1, sub_y1 = find_intersection(line1_Oxy, line2_Oxy)
                sub_z1 = coordinate_of_image_1_center[2] + y1 * math.cos(theta_angle_of_camera_1)
                line1 = (np.array([x_coordinate_of_camera_1,y_coordinate_of_camera_1,z_coordinate_of_camera_1]), np.array([sub_x1 + x_coordinate_of_camera_1,sub_y1 + y_coordinate_of_camera_1,sub_z1 + z_coordinate_of_camera_1]))
                print("line1 = {}".format(line1))

                # Ảnh 2
                # Tìm tọa độ tâm ảnh 2 theo tỉ lệ (16/9)
                # Độ dài tiêu cự camera 1
                TC2 = math.sqrt(9**2 + 16**2) / (2 * math.tan(goc_camera/2))
                coordinate_of_image_2_center = spherical_to_cartesian(TC2, theta_angle_of_camera_2, phi_angle_of_camera_2)
                print("Tọa độ trung điểm ảnh 2 = ",coordinate_of_image_2_center)
                
                # Chiếu ảnh lên mặt phẳng Oxy
                # coordinate_of_image_1_center_Oxy = [coordinate_of_image_1_center[0], coordinate_of_image_1_center[1]]
                
                phi_x2_Oxy = math.atan(- x2 / math.sqrt(coordinate_of_image_2_center[0]**2 + coordinate_of_image_2_center[1]**2)) + phi_angle_of_camera_2
                print("phi_x2_Oxy = ",phi_x2_Oxy)
                r_x2_Oxy = math.sqrt(coordinate_of_image_2_center[0]**2 + coordinate_of_image_2_center[1]**2 + x2**2)
                r_y2_Oxy = math.sqrt(coordinate_of_image_2_center[0]**2 + coordinate_of_image_2_center[1]**2) - y2*math.sin(theta_angle_of_camera_2)

                x2_Oxy = spherical_to_cartesian(r_x2_Oxy, 0, phi_x2_Oxy)
                y2_Oxy = spherical_to_cartesian(r_y2_Oxy, 0, phi_angle_of_camera_2)

                # Chiếu điểm drone lên mặt phẳng Oxy (điểm M)
                line1_Oxy = (coordinate_of_image_2_center[0], coordinate_of_image_2_center[1], - coordinate_of_image_2_center[0] * y2_Oxy[0] - coordinate_of_image_2_center[1] * y2_Oxy[1])
                line2_Oxy = (- coordinate_of_image_2_center[1], coordinate_of_image_2_center[0], coordinate_of_image_2_center[1] * x2_Oxy[0] - coordinate_of_image_2_center[0] * x2_Oxy[1])
                # print("line1_Oxy = {}              line2_Oxy = {}".format(line1_Oxy, line2_Oxy))
                sub_x2, sub_y2 = find_intersection(line1_Oxy, line2_Oxy)
                sub_z2 = coordinate_of_image_2_center[2] + y2 * math.cos(theta_angle_of_camera_2)
                line2 = (np.array([x_coordinate_of_camera_2,y_coordinate_of_camera_2,z_coordinate_of_camera_2]), np.array([sub_x2 + x_coordinate_of_camera_2,sub_y2 + y_coordinate_of_camera_2,sub_z2 + z_coordinate_of_camera_2]))      
                print("line2 = {}".format(line2))

                distance, mid = distance_between_lines(line1, line2)
                # Khoảng cách bé hơn đường chéo mặt sân / 20
                if distance < math.sqrt((x_coordinate_of_camera_2 - x_coordinate_of_camera_1)**2 +
                                        (y_coordinate_of_camera_2 - y_coordinate_of_camera_1)**2) / 7:
                    check = True
                else:
                    check = False

                print("check = {} distance = {} mid = {}".format(check, distance, mid))
                # check, mid = qualified_distance(x1,y1,x2,y2)
                if check == True:
                    list_N_latest_infor[N-1] = 1
                    sub_mid = [round(x, 2) for x in mid]
                    drone_coordinates.append(sub_mid)
                else:
                    if len(list_drone_from_camera_1) > len(list_drone_from_camera_2):
                        sublist = []
                        for sublist1 in list_drone_from_camera_2:
                            sublist.append(sublist1[2])
                        list_N_latest_infor[N-1] = sum(sublist) / len(sublist) / 2
                    else:
                        sublist = []
                        for sublist1 in list_drone_from_camera_1:
                            sublist.append(sublist1[2])
                        list_N_latest_infor[N-1] = sum(sublist) / len(sublist) / 2


    # print(list_N_latest_infor)
    settings.GLOBAL_LIST = list_N_latest_infor
    
    # Phân tích thông tin lưu trữ, đưa ra dự đoán về khả năng xuất hiện drone
    # print("list_N_latest_infor: ", list_N_latest_infor)
    means = sum(list_N_latest_infor) / len(list_N_latest_infor)
    
    # print("drone_coordinates = ", drone_coordinates)
    # print(list_N_latest_infor)
    # print(means)
    if means > threshold_predict and drone_coordinates != []:
        print("Bật chuông cảnh báo - duy trì trong 1s")

        bat_coi.set()
        # if horn_thread is None or not horn_thread.is_alive():
        #     print("Bật còi")
        #     horn_thread = threading.Thread(target=play_horn)
        #     horn_thread.start()
        # else:
        #     print("Còi đã được bật trước đó")

        # settings.SEND_JAMMER = angle_jamming(drone_coordinates, coordinate_of_jammer) + [phi_angle_of_jammer, theta_angle_of_jammer]
        send(angle_jamming(drone_coordinates, coordinate_of_jammer, phi_angle_of_jammer, theta_angle_of_jammer), IP_jammer)

    else:
        # print("Không phát hiện drone")
        drone_coordinates = [[0, 0, 0]]
        bat_coi.clear()

    # drone_coordinates = [[429.85, 459.52, 507.51], [524.52, 568.49, 603.89]]
    print("drone_coordinates = ", drone_coordinates)
    return image_fix_1, image_fix_2, drone_coordinates
    
    # Nếu dự đoán cao, tổng hợp thành một video gửi lên cloud

import json,socket
# import serial

def send(data, IP_jammer):
    # data = [phi, theta]
    print("Đã nhận được ip: ", IP_jammer)
    port = 8266
    data_str = json.dumps(data)
    
    try:
        # Tạo socket và kết nối đến ESP8266
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((IP_jammer, port))
        print("Connected to ESP8266")

        # Gửi dữ liệu đến ESP8266
        sock.sendall(data_str.encode())
        print("Data sent:", data_str)

        # Đợi phản hồi từ ESP8266 (nếu cần)
        # response = sock.recv(1024)
        # print("Response received:", response.decode())

        # Đóng kết nối
        sock.close()
        print("Connection closed")
    except Exception as e:
        print("Error:", str(e))
