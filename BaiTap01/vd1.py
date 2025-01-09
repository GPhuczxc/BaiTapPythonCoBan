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
    img = img.resize((300, 300))  # Thay đổi kích thước để hiển thị lớn hơn
    imgtk = ImageTk.PhotoImage(image=img)
    lbl_image.imgtk = imgtk
    lbl_image.configure(image=imgtk)

# Hàm thực hiện chức năng dựa trên lựa chọn
def apply_function():
    if img is not None:
        selected_function = function_choice.get()

        if selected_function == 1:  # Ảnh Âm Tính
            result_img = 255 - img
        elif selected_function == 2:  # Tăng Độ Tương Phản
            lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            cl = clahe.apply(l)
            limg = cv2.merge((cl, a, b))
            result_img = cv2.cvtColor(limg, cv2.COLOR_LAB2RGB)
        elif selected_function == 3:  # Biến Đổi Log
            img_float = img.astype(float)  # Chuyển ảnh về kiểu float để tránh tràn số
            epsilon = 1e-5  # Thêm giá trị epsilon để tránh log(0)
            c = 255 / np.log(1 + np.max(img_float))
            result_img = c * (np.log(1 + img_float + epsilon))
            result_img = np.array(result_img, dtype=np.uint8)
        elif selected_function == 4:  # Cân Bằng Histogram
            img_yuv = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
            img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
            result_img = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2RGB)

        display_image(result_img)

# Tạo giao diện Tkinter
root = Tk()
root.title("Gia Phúc")
root.geometry("600x700")  # Tăng kích thước của cửa sổ

# Tạo font lớn để giao diện đẹp hơn
font_large = tkFont.Font(family="Helvetica", size=18, weight="bold")
font_medium = tkFont.Font(family="Helvetica", size=14)

# Load ảnh nền
bg_image_path = 'img.png'
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
frame_bottom.place(x=100, y=450)

# Tiêu đề phần chọn chức năng
lbl_title = Label(frame_bottom, text="Chọn chức năng xử lý ảnh:", font=font_large, bg="lightblue")
lbl_title.pack(anchor="w", pady=5)

# Lựa chọn chức năng
function_choice = IntVar()
function_choice.set(1)  # Mặc định chọn chức năng đầu tiên

Radiobutton(frame_bottom, text="Ảnh Âm Tính (Negative Image)", variable=function_choice, value=1, font=font_medium, bg="lightblue").pack(anchor="w")
Radiobutton(frame_bottom, text="Tăng Độ Tương Phản (Increase Contrast)", variable=function_choice, value=2, font=font_medium, bg="lightblue").pack(anchor="w")
Radiobutton(frame_bottom, text="Biến Đổi Log (Log Transformation)", variable=function_choice, value=3, font=font_medium, bg="lightblue").pack(anchor="w")
Radiobutton(frame_bottom, text="Cân Bằng Histogram (Histogram Equalization)", variable=function_choice, value=4, font=font_medium, bg="lightblue").pack(anchor="w")

# Nút thực hiện chức năng
btn_apply = Button(frame_bottom, text="Áp Dụng Chức Năng", command=apply_function, font=font_large, width=20, bg="#2196F3", fg="white")
btn_apply.pack(pady=10)

# Khởi chạy giao diện
root.mainloop()
