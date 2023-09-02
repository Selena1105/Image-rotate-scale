import cv2
import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from scale import *
from filter import *

class ScaleGUI:
    def __init__(self, image):
        # 创建主窗口
        self.window = tk.Tk()
        self.window.title("Scale GUI")
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
        self.image_tk = Image.fromarray(self.image)
        self.image_tk = ImageTk.PhotoImage(self.image_tk)
        self.image_show = tk.Label(self.window, image=self.image_tk, width=self.image_width, height=self.image_height)
        self.image_show.place(x=25, y=20)

        # 创建尺寸显示文本框
        self.size_label = tk.Label(self.window, text="Image size: " + str(self.get_size(self.image)))
        self.size_label.place(x=40, y=330)

        # 创建右侧的控件
        self.controls_frame = tk.Frame(self.window)
        self.controls_frame.grid(row=0, column=1, rowspan=2, padx=330, pady=40)

        # 缩放倍数输入框
        self.scale_label = tk.Label(self.controls_frame, text="缩放倍数：")
        self.scale_label.pack()
        self.scale_entry = tk.Entry(self.controls_frame)
        self.scale_entry.pack()

        # 插值方式下拉框
        self.interpolation_label = tk.Label(self.controls_frame, text="插值方式：")
        self.interpolation_label.pack()
        self.interpolation_combobox = ttk.Combobox(self.controls_frame, values=["Nearest", "Bilinear", "Bicubic"])
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
        self.apply_button = tk.Button(self.apply_frame, text="Apply", command=self.apply_scale)
        self.apply_button.pack()

        self.window.mainloop()
    

    def apply_scale(self):
        # 执行缩放
        self.factor = float(self.scale_entry.get())
        self.interpolation = self.interpolation_combobox.get()
        self.smoothfilter = self.filtering_combobox.get()
        scale_image = self.scale()

        # 更新图片展示窗口
        scale_image_show = cv2.resize(scale_image, (self.image_width, self.image_height))  
        scale_image_tk = ImageTk.PhotoImage(Image.fromarray(scale_image_show))
        self.image_show.configure(image=scale_image_tk)
        self.image_show.image = scale_image_tk

        # 更新尺寸显示文本框
        self.size_label.config(text="Image size: " + str(self.get_size(scale_image)))

        # 保存缩放后图片
        self.save_image(scale_image)


    # 图片缩放函数
    def scale(self):
        height, width = self.image.shape[:2]
        kernel_size = 3

        if self.interpolation == "Nearest":
            # 最近邻
            scale_img = Nearest(self.image, int(self.factor * height), int(self.factor * width))
        elif self.interpolation == "Bilinear":
            # 双线性
            scale_img = Bilinear(self.image, int(self.factor * height), int(self.factor * width))
        elif self.interpolation == "Bicubic":
            # 双立方
            scale_img = Bicubic(self.image, int(self.factor * height), int(self.factor * width))
        

        if self.smoothfilter == "Mean":
            # 均值滤波
            scale_img = cv2.blur(scale_img, (kernel_size, kernel_size))
        elif self.smoothfilter == "Gaussian":
            # 高斯滤波
            scale_img = cv2.GaussianBlur(scale_img, (kernel_size, kernel_size), 0)
        elif self.smoothfilter == "Boxed":
            # 邻域平均滤波
            scale_img = cv2.boxFilter(scale_img, -1, (kernel_size, kernel_size), normalize=True)
        elif self.smoothfilter == "Edge Mean":
            # 边缘均值滤波
            scale_img = edge_mean_filter(scale_img, kernel_size)
        
        return scale_img
    
    # 保存图片
    def save_image(self, image):
        path = "scale_result/%s_%s_%s.jpg" % (self.interpolation, self.factor, self.smoothfilter)
        if os.path.exists(path):
            # 删除图片
            os.remove(path)
            #保存图片
        cv2.imwrite(path, image)
        print("save image!")

    # 获取图片尺寸
    def get_size(self, image):
        height, width = image.shape[:2]
        string = "%d x %d" % (height, width)
        return string


Cameraman=cv2.imread("original/Cameraman.bmp")
Lena = cv2.imread("original/Lena.bmp")
Peppers = cv2.imread("original/Peppers.bmp")

gui = ScaleGUI(Cameraman)