$(document).ready(function() {
    //var ip_camera_1 = document.getElementById("camera1-ip").value;
    //var ip_camera_2 = document.getElementById("camera2-ip").value;

    function updateImage() {
        // Gửi yêu cầu AJAX đến view Django để nhận hình ảnh mới
        console.log("Gửi yêu cầu về máy chủ")
        $.ajax({
            url: '/detection/stream/?ip_camera_1=' + document.getElementById("camera1-ip").value + '&ip_camera_2=' + document.getElementById("camera2-ip").value + 
                '&x_coordinate_of_camera_1=' + document.getElementById("x_coordinate_of_camera_1").value + '&y_coordinate_of_camera_1=' + document.getElementById("y_coordinate_of_camera_1").value +
                '&z_coordinate_of_camera_1=' + document.getElementById("z_coordinate_of_camera_1").value + '&theta_angle_of_camera_1=' + document.getElementById("theta_angle_of_camera_1").value +
                '&phi_angle_of_camera_1=' + document.getElementById("phi_angle_of_camera_1").value + '&x_coordinate_of_camera_2=' + document.getElementById("x_coordinate_of_camera_2").value +
                '&y_coordinate_of_camera_2=' + document.getElementById("y_coordinate_of_camera_2").value + '&z_coordinate_of_camera_2=' + document.getElementById("z_coordinate_of_camera_2").value +
                '&theta_angle_of_camera_2=' + document.getElementById("theta_angle_of_camera_2").value + '&phi_angle_of_camera_2=' + document.getElementById("phi_angle_of_camera_2").value +
                '&x_coordinate_of_jammer=' + document.getElementById("x_coordinate_of_jammer").value + '&y_coordinate_of_jammer=' + document.getElementById("y_coordinate_of_jammer").value +
                '&z_coordinate_of_jammer=' + document.getElementById("z_coordinate_of_jammer").value + '&threshold_predict=' + document.getElementById("threshold_predict").value +
                '&goc_camera=' + document.getElementById("goc_camera").value + '&theta_angle_of_jammer=' + document.getElementById("theta_angle_of_jammer").value + 
                '&phi_angle_of_jammer=' + document.getElementById("phi_angle_of_jammer").value + '&ip_jammer=' + document.getElementById("ip_jammer").value,
            type: 'GET',
            cache: false,
            success: function(response) {
                // Cập nhật hình ảnh trên trang web
                //console.log("Đây là data image1 nhận về: ", response.image1);
                //console.log("Đây là data image2 nhận về: ", response.image2);
                //console.log("Đây là coordinate nhận về: ", response.coordinate[0][1]);

                // Dữ liệu JSON
                var data = response.coordinate;
                
                // Lấy đối tượng div
                var divElement_x = document.getElementById("coordinate_x");
                var divElement_y = document.getElementById("coordinate_y");
                var divElement_z = document.getElementById("coordinate_z");

                // Duyệt qua các giá trị trong dữ liệu coordinate
                if (data[0][0] != 0){
                    //alert("Phát hiện có drone trong khu vực!");
                    console.log("Detect Drone")
                    setTimeout(function() {
                        var customAlert = document.getElementById('customAlert');
                        customAlert.textContent = 'PHÁT HIỆN DRONE!';
                    }, 100);
                }
                else {
                    setTimeout(function() {
                        var customAlert = document.getElementById('customAlert');
                        customAlert.textContent = '';
                    }, 100);
                }

                console.log("Coordinate = ", data[0])
                    
                for (var key in data) {
                if (data.hasOwnProperty(key)) {
                    divElement_x.innerText = "";
                    divElement_x.innerText += data[key][0] + "\n";
                    divElement_y.innerText = "";
                    divElement_y.innerText += data[key][1] + "\n";
                    divElement_z.innerText = "";
                    divElement_z.innerText += data[key][2] + "\n";
                }
                }
                // console.log("Coordinate = ", data)

                $('#stream-image-1').attr('src', 'data:image/jpeg;base64,' + response.image1);
                $('#stream-image-2').attr('src', 'data:image/jpeg;base64,' + response.image2);
                // Cập nhật hình ảnh từ response
                // $('#stream-image-1').attr('src', response.image1_url);
                // $('#stream-image-2').attr('src', response.image2_url);
            },
            error: function(xhr, status, error) {
                console.log('Error:', error);
                console.log('Lỗi khi lấy hình ảnh từ server.');
                setTimeout(updateImage, 1000);
            },            
            complete: function() {
                // Tiếp tục cập nhật hình ảnh sau một khoảng thời gian nhất định (ví dụ: 0.01 giây)
                setTimeout(updateImage, 10);
            }
        });
    }
    
    // Bắt đầu cập nhật hình ảnh
    updateImage();
});

function handleSubmit1() {
    // Lấy giá trị từ ô input
    var inputValue1 = document.getElementById("camera1-ip").value;
    
    // Thực hiện các hành động mong muốn khi nút submit được nhấn
    console.log("Giá trị ip nhập cho camera 1: " + inputValue1);
    
    // Ngăn chặn form gửi dữ liệu lên server (nếu có) để tránh làm tải lại trang
    return false;
}


function handleSubmit2() {
    // Lấy giá trị từ ô input
    var inputValue2 = document.getElementById("camera2-ip").value;
    
    // Thực hiện các hành động mong muốn khi nút submit được nhấn
    console.log("Giá trị ip nhập cho camera 2: " + inputValue2);
    
    // Ngăn chặn form gửi dữ liệu lên server (nếu có) để tránh làm tải lại trang
    return false;
}

$(document).ready(function() {
    $("#myButton").click(function() {
        var input_ip_jammer = document.getElementById("ip_jammer").value;  // Lấy giá trị từ input
        // $.ajax({
        //     type: "POST",
        //     url: '/detection/jamming/',
        //     data: {
        //         'ip_jammer': input_ip_jammer
        //     },
        //     success: function(response) {
        //         console.log(response);  // In phản hồi từ views.py trong console
        //     },
        //     error: function(response) {
        //         console.log(response);  // Xử lý lỗi nếu có
        //     }
        // });

        $.ajax({
            url: '/detection/jamming/?ip_jammer=' + document.getElementById("ip_jammer").value,
            type: 'GET',
            cache: false,
            success: function(response) {

                // Dữ liệu JSON
                var data = response.status;
            
                console.log("Status = ", data)
            },
            error: function(xhr, status, error) {
                console.log('Error:', error);
                console.log('Lỗi không phát tín hiệu gây nhiễu');
            },            
            complete: function() {
                // Tiếp tục cập nhật hình ảnh sau một khoảng thời gian nhất định (ví dụ: 10 giây)
                setTimeout(100);
            }
        });
    });
});