import cv2
import os
import imutils
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from rotate import *
from filter import *

class RotateGUI:
    def __init__(self, image):
        # 创建主窗口
        self.window = tk.Tk()
        self.window.title("Rotate GUI")
        self.window.option_add("*Font", ("Helvetica", 18))

        # 设置窗口大小
        window_width = 650
        window_height = 450
        self.window.geometry(f"{window_width}x{window_height}")
        
        # 图片展示窗口
        self.image = image
        self.image_width = 256
        self.image_height = 256
        self.image_tk = cv2.resize(image, (self.image_width, self.image_height))
        self.image_tk = Image.fromarray(self.image_tk)
        self.image_tk = ImageTk.PhotoImage(self.image_tk)
        self.image_show = tk.Label(self.window, image=self.image_tk, width=self.image_width, height=self.image_height)
        self.image_show.place(x=25, y=20)

        # 旋转度数显示文本框
        self.angle=0
        self.size_label = tk.Label(self.window, text="Rotate angle: %s °" % str(self.angle))
        self.size_label.place(x=40, y=330)

        # 创建右侧的控件
        self.controls_frame = tk.Frame(self.window)
        self.controls_frame.grid(row=0, column=1, rowspan=2, padx=330, pady=40)

        # 旋转角度输入框
        self.rotate_label = tk.Label(self.controls_frame, text="旋转度数：")
        self.rotate_label.pack()
        self.rotate_entry = tk.Entry(self.controls_frame)
        self.rotate_entry.pack()

        # 旋转方式下拉框
        self.interpolation_label = tk.Label(self.controls_frame, text="旋转方式：")
        self.interpolation_label.pack()
        self.interpolation_combobox = ttk.Combobox(self.controls_frame, values=["Method 1", "Method 2", "Method 3"])
        self.interpolation_combobox.pack()

        # 平滑滤波下拉框
        self.filtering_label = tk.Label(self.controls_frame, text="平滑滤波：")
        self.filtering_label.pack()
        self.filtering_combobox = ttk.Combobox(self.controls_frame, values=["None", "Mean", "Gaussian", "Boxed", "Edge Mean"])
        self.filtering_combobox.pack()

        # 创建一个容器框架用于放置apply按钮
        self.apply_frame = tk.Frame(self.controls_frame)
        self.apply_frame.pack(side="bottom", pady=25)

        # apply按钮
        self.apply_button = tk.Button(self.apply_frame, text="Apply", command=self.apply_rotate)
        self.apply_button.pack()

        self.window.mainloop()
    

    def apply_rotate(self):
        # 执行旋转
        self.angle = float(self.rotate_entry.get())
        self.interpolation = self.interpolation_combobox.get()
        self.smoothfilter = self.filtering_combobox.get()
        rotate_image = self.rotate()

        # 更新图片展示窗口
        rotate_image_show = cv2.resize(rotate_image, (self.image_width, self.image_height))  # 调整图片大小
        rotate_image_tk = ImageTk.PhotoImage(Image.fromarray(rotate_image_show))
        self.image_show.configure(image=rotate_image_tk)
        self.image_show.image = rotate_image_tk

        # 更新角度显示文本框
        self.size_label.config(text="Rotate angel: %s°" % str(self.angle))

        # 保存旋转后图片
        self.save_image(rotate_image)


    # 图片旋转函数
    def rotate(self):
        kernel_size = 3

        if self.interpolation == "Method 1":
            #方法1
            rotated_img = rotate_img(self.image, self.angle)
        elif self.interpolation == "Method 2":
            #方法2
            rotated_img = imutils.rotate_bound(self.image, -self.angle)
        elif self.interpolation == "Method 3":
            #方法3
            rotated_img = imutils.rotate(self.image, self.angle)

        if self.smoothfilter == "Mean":
            # 均值滤波
            rotated_img = cv2.blur(rotated_img, (kernel_size, kernel_size))
        elif self.smoothfilter == "Gaussian":
            # 高斯滤波
            rotated_img = cv2.GaussianBlur(rotated_img, (kernel_size, kernel_size), 0)
        elif self.smoothfilter == "Boxed":
            # 邻域平均滤波
            rotated_img = cv2.boxFilter(rotated_img, -1, (kernel_size, kernel_size), normalize=True)
        elif self.smoothfilter == "Edge Mean":
            # 边缘均值滤波
            rotated_img = edge_mean_filter(rotated_img, kernel_size)
        
        return rotated_img
    
    # 保存图片
    def save_image(self, image):
        path = "rotate_result/%s_%s_%s.jpg" % (self.interpolation, self.angle, self.smoothfilter)
        if os.path.exists(path):
            # 删除图片
            os.remove(path)
            #保存图片
        cv2.imwrite(path, image)
        print("save image!")
    

Cameraman=cv2.imread("original/Cameraman.bmp")
Lena = cv2.imread("original/Lena.bmp")
Peppers = cv2.imread("original/Peppers.bmp")

gui = RotateGUI(Lena)