import cv2
import imutils
import os
from scale import *
from rotate import *

Cameraman=cv2.imread("original/Cameraman.bmp")
Lena = cv2.imread("original/Lena.bmp")
Peppers = cv2.imread("original/Peppers.bmp")

def save_image(path, image):
    if os.path.exists(path):
    # 删除图片
        os.remove(path)
    #保存图片
    cv2.imwrite(path, image)

def random_scale(image, factor, kernel_size):
    height, width = image.shape[:2]
    # 最近邻
    scale_near = Nearest(image, int(factor * height), int(factor * width))
    # 双线性
    scale_bi = Bilinear(image, int(factor * height), int(factor * width))
    # 双立方
    scale_cubic = Bicubic(image, int(factor * height), int(factor * width))

    # 保存结果
    save_image('scale_result/nearest_'+str(factor)+'.jpg',scale_near)
    save_image('scale_result/bilinear_'+str(factor)+'.jpg',scale_bi)
    save_image('scale_result/bicubic_'+str(factor)+'.jpg',scale_cubic)

    # 增加平滑滤波器
    mean_filtered, gaussian_filtered, boxed_image, edge_image = conv_filter(scale_near, kernel_size)
    # 保存结果
    save_image('scale_filter/mean_filtered_'+str(kernel_size)+'-'+str(factor)+'.jpg', mean_filtered)
    save_image('scale_filter/gaussian_filtered_'+str(kernel_size)+'-'+str(factor)+'.jpg', gaussian_filtered)
    save_image('scale_filter/box_filtered_'+str(kernel_size)+'-'+str(factor)+'.jpg', boxed_image)
    save_image('scale_filter/edge_mean_smoothing_'+str(kernel_size)+'-'+str(factor)+'.jpg', edge_image)


def random_scale_2(image, factor, kernel_size):
    # 增加平滑滤波器
    image, _,_,_= conv_filter(image, kernel_size)

    height, width = image.shape[:2]
    # 最近邻
    scale_near = Nearest(image, int(factor * height), int(factor * width))
    # 双线性
    scale_bi = Bilinear(image, int(factor * height), int(factor * width))
    # 双立方
    scale_cubic = Bicubic(image, int(factor * height), int(factor * width))

    # 保存结果
    save_image('scale_2/nearest_'+str(factor)+'.jpg',scale_near)
    save_image('scale_2/bilinear_'+str(factor)+'.jpg',scale_bi)
    save_image('scale_2/bicubic_'+str(factor)+'.jpg',scale_cubic)


def random_rotate(image, angle, kernel_size):
    #方法1
    rotated_img1 = rotate_img(image, angle)
    cv2.imwrite('rotate_result/rotate1_'+str(angle)+'.jpg', rotated_img1)
    #方法2
    rotated_img2 = imutils.rotate_bound(image, -angle)
    cv2.imwrite('rotate_result/rotate2_'+str(angle)+'.jpg', rotated_img2)
    #方法3
    rotated_img3 = imutils.rotate(image, angle)
    cv2.imwrite('rotate_result/rotate3_'+str(angle)+'.jpg', rotated_img3)

    print("rotate done")

    # 增加平滑滤波器
    mean_filtered, gaussian_filtered, boxed_image,  edge_image = conv_filter(rotated_img1, kernel_size)
    # 保存结果
    save_image('rotate_filter/mean_filtered_'+str(angle)+'.jpg', mean_filtered)
    save_image('rotate_filter/gaussian_filtered_'+str(angle)+'.jpg', gaussian_filtered)
    save_image('rotate_filter/box_filtered_'+str(angle)+'.jpg', boxed_image)
    save_image('rotate_filter/edge_mean_smoothing_'+str(angle)+'.jpg', edge_image)


# random_scale(Cameraman, 3, 7)
# random_scale_2(Cameraman, 3, 3)
# random_scale(Peppers, 0.4, 7)
# random_scale_2(Peppers, 0.4, 3)
random_rotate(Lena, 550, 3)


