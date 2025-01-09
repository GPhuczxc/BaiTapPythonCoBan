import cv2
import numpy as np
from tkinter import Tk, Label, Button, Radiobutton, IntVar, filedialog, Frame, Canvas
from PIL import Image, ImageTk
import tkinter.font as tkFont

# Hàm chọn ảnh từ máy tính
def open_image():
    global img
    filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if filepath:
        img = cv2.imread(filepath)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        display_image(img)

# Hàm hiển thị ảnh trên giao diện
def display_image(img):
    img = Image.fromarray(img)
    img = img.resize((320, 320))  # Thay đổi kích thước để hiển thị lớn hơn
    imgtk = ImageTk.PhotoImage(image=img)
    lbl_image.imgtk = imgtk
    lbl_image.configure(image=imgtk)

# Hàm thực hiện chức năng dựa trên lựa chọn
def apply_function():
    # Kiểm tra xem có ảnh nào đang được mở hay không
    if img is not None:
        # Lấy chức năng xử lý ảnh mà người dùng đã chọn (Sobel, Laplacian, Gaussian Blur, hoặc Canny)
        selected_function = function_choice.get()

        # Nếu người dùng chọn Sobel (phát hiện cạnh Sobel)
        if selected_function == 1:
            # Chuyển đổi ảnh sang thang độ xám để dễ phát hiện cạnh (vì phát hiện cạnh thường làm trên ảnh xám)
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            # Tính đạo hàm theo trục X (Sobel X) để tìm các cạnh nằm dọc
            sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
            # Tính đạo hàm theo trục Y (Sobel Y) để tìm các cạnh nằm ngang
            sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
            # Tính độ lớn của gradient bằng cách kết hợp Sobel X và Sobel Y để tạo ra hình ảnh phát hiện cạnh tổng hợp
            sobel = np.sqrt(sobel_x ** 2 + sobel_y ** 2)
            # Chuyển đổi giá trị gradient thành giá trị tuyệt đối để dễ hiển thị dưới dạng ảnh
            result_img = cv2.convertScaleAbs(sobel)

        # Nếu người dùng chọn Laplacian (phát hiện cạnh Laplacian)
        elif selected_function == 2:
            # Chuyển đổi ảnh sang thang độ xám
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            # Áp dụng toán tử Laplacian để tính đạo hàm bậc hai của ảnh, phát hiện cạnh theo cả hai chiều
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            # Chuyển đổi kết quả thành giá trị tuyệt đối để dễ hiển thị dưới dạng ảnh
            result_img = cv2.convertScaleAbs(laplacian)

        # Nếu người dùng chọn Gaussian Blur (làm mờ ảnh bằng bộ lọc Gaussian)
        elif selected_function == 3:
            # Áp dụng bộ lọc Gaussian Blur để làm mờ ảnh, giúp giảm nhiễu và làm mượt các chi tiết
            # (15, 15) là kích thước của kernel, giá trị càng lớn thì ảnh càng bị làm mờ
            result_img = cv2.GaussianBlur(img, (15, 15), 0)

        # Nếu người dùng chọn Canny (phát hiện cạnh Canny)
        elif selected_function == 4:
            # Chuyển ảnh sang thang độ xám trước khi áp dụng Canny
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            # Áp dụng thuật toán phát hiện cạnh Canny với hai ngưỡng dưới và trên là 100 và 200
            # Các cạnh có độ gradient nằm giữa các ngưỡng này sẽ được giữ lại
            result_img = cv2.Canny(gray, 100, 200)

        # Hiển thị kết quả sau khi áp dụng chức năng xử lý ảnh
        display_image(result_img)

# Tạo giao diện Tkinter
root = Tk()
root.title("Gia Phúc")
root.geometry("600x700")  # Tăng kích thước của cửa sổ

# Tạo font lớn để giao diện đẹp hơn
font_large = tkFont.Font(family="Helvetica", size=18, weight="bold")
font_medium = tkFont.Font(family="Helvetica", size=14)

# Load ảnh nền
bg_image_path ='img.png'
bg_image = Image.open(bg_image_path)
bg_image = bg_image.resize((600, 700))  # Resize để phù hợp với kích thước cửa sổ
bg_photo = ImageTk.PhotoImage(bg_image)

# Tạo Canvas để hiển thị ảnh nền
canvas = Canvas(root, width=600, height=700)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Khung trên cùng để chọn và hiển thị ảnh
frame_top = Frame(root, bg="lightblue")
frame_top.place(x=135, y=20)

# Nút chọn ảnh
btn_open = Button(frame_top, text="Chọn Ảnh", command=open_image, font=font_large, width=20, bg="#4CAF50", fg="white")
btn_open.grid(row=0, column=0, padx=10)

# Khung hiển thị ảnh
lbl_image = Label(frame_top)
lbl_image.grid(row=1, column=0, pady=20)

# Khung dưới để chọn chức năng và thực hiện
frame_bottom = Frame(root, bg="lightblue")
frame_bottom.place(x=140, y=450)

# Tiêu đề phần chọn chức năng
lbl_title = Label(frame_bottom, text="Chọn chức năng xử lý ảnh:", font=font_large, bg="lightblue")
lbl_title.pack(anchor="w", pady=5)

# Lựa chọn chức năng
function_choice = IntVar()
function_choice.set(1)  # Mặc định chọn chức năng đầu tiên

Radiobutton(frame_bottom, text="Phát hiện cạnh Sobel", variable=function_choice, value=1, font=font_medium, bg="lightblue").pack(anchor="w")
Radiobutton(frame_bottom, text="Phát hiện cạnh Laplacian", variable=function_choice, value=2, font=font_medium, bg="lightblue").pack(anchor="w")
Radiobutton(frame_bottom, text="Làm mờ Gaussian", variable=function_choice, value=3, font=font_medium, bg="lightblue").pack(anchor="w")
Radiobutton(frame_bottom, text="Phát hiện cạnh Canny", variable=function_choice, value=4, font=font_medium, bg="lightblue").pack(anchor="w")

# Nút thực hiện chức năng
btn_apply = Button(frame_bottom, text="Áp Dụng Chức Năng", command=apply_function, font=font_large, width=20, bg="#2196F3", fg="white")
btn_apply.pack(pady=10)

# Khởi chạy giao diện
root.mainloop()
