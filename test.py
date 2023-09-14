import cv2

def main():
    # Địa chỉ IP của camera
    IP_ADDRESS = '192.168.0.96'
    
    # Tạo đối tượng VideoCapture để kết nối và đọc frame từ camera
    cap = cv2.VideoCapture('rtsp://' + IP_ADDRESS + '/live/ch00_1')
    
    # Kiểm tra xem kết nối đã được thiết lập thành công hay chưa
    if not cap.isOpened():
        print("Không thể kết nối đến camera.")
        return
    
    while True:
        # Đọc frame từ camera
        ret, frame = cap.read()
        
        # Kiểm tra xem frame có được đọc thành công hay không
        if not ret:
            print("Không thể đọc frame từ camera.")
            break
        
        # Hiển thị frame lên màn hình
        cv2.imshow('Camera', frame)
        
        # Kiểm tra xem người dùng đã nhấn phím 'q' để thoát hay không
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Giải phóng tài nguyên
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
