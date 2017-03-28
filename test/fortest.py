import cv2
import logging
from logging import config
from cv2 import *
from PIL import ImageGrab,Image
import numpy as np
from conf.global_config import Const

class graphMatcher:
    def __init__(self, sourceimg):
        self.sourceimg = sourceimg

    def find(self, templateimg, xy_scaling=(1.0,1.0), threshold=0.4):


        # image = cv2.imread(self.sourceimg)
        image = cv2.imdecode(np.fromfile(self.sourceimg, dtype=np.uint8), 1)
        template = cv2.imread(templateimg)

        tw, th = template.shape[:-1]
        # thumb1 = cv2.resize(template, None, fx=1, fy=1, interpolation=cv2.INTER_CUBIC)
        # cv2.imshow("test", mat=thumb1)
        # # cv2.imshow("test",mat=result)
        # while (1):
        #     k = cv2.waitKey(5) & 0xFF
        #     if k == 27:
        #         break
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        similarity = cv2.minMaxLoc(result)[1]
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        top_left = max_loc
        # w, h = template.shape[::-1]

        bottom_right = (top_left[0] + th, top_left[1] + tw)
        cv2.rectangle(image, top_left, bottom_right, 255, 2)
        thumb = cv2.resize(image, None, fx=xy_scaling[0], fy=xy_scaling[1], interpolation=cv2.INTER_CUBIC)
        cv2.imshow("test", mat=thumb)
        # cv2.imshow("test",mat=result)

        while (1):
            k = cv2.waitKey(5) & 0xFF
            if k == 27:
                break
        # for similarity in cv2.minMaxLoc(result):
            # print("similarity:", templateimg, similarity)
            # print("result.shape:", templateimg, repr(result.shape))
        # if similarity < threshold:
        #     return similarity
        # else:
        #     return np.unravel_index(result.argmax(), result.shape)
        y,x = np.unravel_index(result.argmax(), result.shape)
        return (x,y)



        # if phwnd:
        #     hwnd = user32.GetTopWindow(phwnd)
        #     if hwnd is None:
        #         hwnd = phwnd
        # else:
        #     hwnd = self.hwnd
        # hwnd = user32.GetWindow(hwnd, win32con.GW_HWNDNEXT)
        # hwnd = win32gui.
        # hwnd = win32gui.GetWindow(phwnd,win32con.GW_HWNDFIRST)
        # print(phwnd,repr(win32gui.GetClassName(phwnd)))
        # print(hwnd,repr(win32gui.GetClassName(hwnd)))
        #
        # hwnds = self.getAllChildHwnds(hwnd)
        # for hwnd in hwnds:
        # print(hwnd,repr(win32gui.GetClassName(hwnd)))
if __name__=="__main__":
    # aaimg = capture_img()
    # cv2.namedWindow("test", 1)
    # cv2.imshow("test",mat=np.asarray(aaimg))
    # cv2.imshow("test",mat=result)
    # while (1):
    #     k = cv2.waitKey(5) & 0xFF
    #     if k == 27:
    #         break
    # matcher = graphMatcher("D:\\Devlopment\\按键精灵\\阴阳师\\阴阳师\\阴阳师\\pic\\截图\\状态界面.bmp")
    # matcher = graphMatcher("d:\\Devlopment\\Python\\GamePlugin\\source\\imgs\\图.bmp")
    # for img in [
    #     # 'd:\\Devlopment\\Python\\GamePlugin\\source\\imgs\\585.png',
    #     #         'D:\\Devlopment\\按键精灵\\阴阳师\\阴阳师\\阴阳师\\pic\\阴阳寮1.bmp',
    #     #         'D:\\Devlopment\\按键精灵\\阴阳师\\阴阳师\\阴阳师\\pic\\组队1.bmp',
    #             'd:\\Devlopment\\Python\\GamePlugin\\source\\imgs\\583.png',
    #             'd:\\Devlopment\\Python\\GamePlugin\\source\\imgs\\zd.bmp',
    #             'd:\\Devlopment\\Python\\GamePlugin\\source\\imgs\\zd2.bmp',
    #             # 'd:\\Devlopment\\Python\\GamePlugin\\source\\imgs\\582.png',
    #             ]:
    #     print(img, matcher.find(img))

    # # 调用截屏函数
    # window_capture("d:\\")
    pass