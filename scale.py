import numpy as np
from filter import *

# 最近邻插值
def Nearest(img, change_height, change_width, channels=3):
    near_img = np.zeros( shape = ( change_height, change_width, channels ), dtype = np.uint8 )
    
    for i in range( 0, change_height ):
        for j in range( 0, change_width ):
            row = ( i / change_height ) * img.shape[0]
            col = ( j / change_width ) * img.shape[1]
            near_row =  round ( row ) # 找原图中最近的像素点
            near_col = round( col )
            if near_row == img.shape[0] or near_col == img.shape[1]: # 避免超过范围
                near_row -= 1
                near_col -= 1
                
            near_img[i][j] = img[near_row][near_col] 

    print("Nearest done!")
            
    return near_img


# 双线性插值
def Bilinear(img, change_height, change_width, channels=3):
    bilinear_img = np.zeros( shape = ( change_height, change_width, channels ), dtype = np.uint8 )
    
    for i in range( 0, change_height ):
        for j in range( 0, change_width ):
            row = ( i / change_height ) * img.shape[0]
            col = ( j / change_width ) * img.shape[1]
            row_int = int( row )
            col_int = int( col )
            u = row - row_int
            v = col - col_int
            if row_int == img.shape[0]-1 or col_int == img.shape[1]-1:
                row_int -= 1
                col_int -= 1

            # 双线性插值公式 
            bilinear_img[i][j] = (1-u)*(1-v) *img[row_int][col_int] + (1-u)*v*img[row_int][col_int+1] + u*(1-v)*img[row_int+1][col_int] + u*v*img[row_int+1][col_int+1]
    
    print("Bilinear done!")

    return bilinear_img

# bell分布
def Bicubic_Bell( num ):
    if  -1.5 <= num <= -0.5:
        return -0.5 * ( num + 1.5) ** 2
    if -0.5 < num <= 0.5:
        return 3/4 - num ** 2
    if 0.5 < num <= 1.5:
        return 0.5 * ( num - 1.5 ) ** 2
    else:
        return 0
        
# 双立方插值
def Bicubic (img, bigger_height, bigger_width, channels=3):
    Bicubic_img = np.zeros( shape = ( bigger_height, bigger_width, channels ), dtype = np.uint8 )
    
    for i in range( 0, bigger_height ):
        for j in range( 0, bigger_width ):
            row = ( i / bigger_height ) * img.shape[0]
            col = ( j / bigger_width ) * img.shape[1]
            row_int = int( row )
            col_int = int( col )
            u = row - row_int
            v = col - col_int
            tmp = 0
            for m in range(-1, 3):
                for n in range(-1, 3):
                    if ( row_int + m ) < 0 or (col_int+n) < 0 or ( row_int + m ) >= img.shape[0] or (col_int+n) >= img.shape[1]:
                        row_int = img.shape[0] - 1 - m
                        col_int = img.shape[1] - 1 - n

                    numm = img[row_int + m][col_int+n] * Bicubic_Bell( m-u ) * Bicubic_Bell( n-v ) 
                    tmp += np.abs( np.trunc( numm ) )
                    
            Bicubic_img[i][j] = tmp
    
    print("Bicubic done!")

    return Bicubic_img



