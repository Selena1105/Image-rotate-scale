import cv2
import numpy as np

def edge_mean_filter(image, kernel_size):
    # 对图像进行边缘检测
    edges = cv2.Canny(image, 100, 200)

    # 构建一个与原始图像大小相同的空白图像
    smoothed_image = np.zeros_like(image)

    # 应用均值平滑处理到图像的边缘部分
    smoothed_image[edges != 0] = cv2.boxFilter(image, -1, (kernel_size, kernel_size), normalize=True)[edges != 0]
    
    # 将未处理的图像部分复制到平滑图像中
    smoothed_image[edges == 0] = image[edges == 0]

    return smoothed_image


# 平滑滤波器
def conv_filter(image, kernel_size):
    # 均值滤波
    mean_filtered = cv2.blur(image, (kernel_size, kernel_size))
    # 高斯滤波
    gaussian_filtered = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    # 邻域平均滤波
    boxed_image = cv2.boxFilter(image, -1, (kernel_size, kernel_size), normalize=True)
    # 边缘均值滤波
    edge_image = edge_mean_filter(image, kernel_size)

    print("filter done!")

    return mean_filtered, gaussian_filtered, boxed_image, edge_image