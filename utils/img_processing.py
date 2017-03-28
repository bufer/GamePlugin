import cv2
import logging
import PIL
import pytesseract
from logging import config
from cv2 import *
from PIL import ImageGrab, Image
import numpy as np
from conf.global_config import Const


# config.fileConfig(Const.LOG_CONFIG_FILE.value)
# logger = logging.getLogger(Const.BAT_LOGGER_NAME.value)
class ImgProcessing():

    def __init__(self, width=None, height=None):
        self.set_scaling(width, height)

    def set_scaling(self, width:float, height:float):
        """
        获取当前窗口相对于原始模板画面的缩放比例
        :param width:当前窗口宽度
        :param height:当前窗口高度
        :return:sw:宽度缩放比例,sh:高度缩放比例
        """
        if width is not None and width > 0:
            self.width_ratio = width / Const.ORIGINAL_TEMPLATE_WIDTH.value
        else:
            self.width_ratio = 1.0
        if height is not None and height > 0:
            self.height_ratio = height / Const.ORIGINAL_TEMPLATE_HEIGHT.value
        else:
            self.height_ratio = 1.0
        # return sw, sh

    def tailor_img(self, vimg: Image, box):
        """
        裁剪图片
        :param vimg:待裁剪图片
        :param box:裁剪区域
        :return:裁剪后图片
        """
        return vimg.crop(box)

    def capture_img(self, bbox=None):
        """
        屏幕截图
        :param bbox: 指定截图范围，默认全屏截图
        :return: 返回获得截图Image对象
        """
        return ImageGrab.grab(bbox)

    def __img2ndarray(self, img):
        """
        将图片资源转换为numpy的ndarray对象
        :param img:待转换图片资源，支持输入文件名，Image对象，ndarray对象
        :return:src：ndarray对象资源，转换失败返回None
        """
        src = None
        if isinstance(img, (Image.Image,)):
            src = np.asarray(img)
        elif isinstance(img, (str,)):
            try:
                src = cv2.imdecode(np.fromfile(img, dtype=np.uint8), 1)
            except Exception as e:
                # logger.error("读取图片%s错误！" % src_img)
                print("读取图片%s错误！" % img)
                # print(e)
        elif isinstance(img, (np.ndarray,)):
            src = img
        return src

    def match_graph(self, src_img, template_img, match_method=cv2.TM_CCOEFF_NORMED):
        """
        在图片中匹配模板图片
        :param src_img: 匹配图片
        :param template_name: 待匹配图片模板文件名
        :param fx: 模板X轴缩放比例
        :param fy: 模板Y轴缩放比例
        :param match_method: 匹配算法
                1. 差值平方和匹配 TM_SQDIFF 最好匹配为 0。 匹配越差，匹配值越大
                2. 标准化差值平方和匹配 TM_SQDIFF_NORMED 和差值平方和算法是类似的。只不过对图像和模板进行了标准化操作
                3. 相关匹配 TM_CCORR 较大的数表示匹配程度较高，0标识最坏的匹配效果。
                4. 标准相关匹配 TM_CCORR_NORMED 和 标准化差值平方和匹配 类似，都是去除了亮度线性变化对相似度计算的影响。可以保证图像和模板同时变亮或变暗k倍时结果不变。
                5. 相关匹配 TM_CCOEFF 这里是把图像和模板都减去了各自的平均值，使得这两幅图像都没有直流分量。
                6. 标准相关匹配 TM_CCOEFF_NORMED 1表示完全相同，-1 表示两幅图像的亮度正好相反，0 表示两幅图像之间没有线性关系
        :return: (bbox, similarity):bbox匹配区域坐标，similarity相似度，根据使用的匹配算法不同取值范围也不一样
        """
        top_x = None
        top_y = None
        similarity = None
        # 获取待查找图片资源
        src = self.__img2ndarray(src_img)
        template = self.__img2ndarray(template_img)

        if src is not None and template is not None:

            try:
                # 按比例缩放模板图片
                if (self.width_ratio == 1.0 and self.height_ratio == 1.0):
                    pass
                else:
                    template = cv2.resize(template, None, fx=self.width_ratio, fy=self.height_ratio,
                                          interpolation=cv2.INTER_CUBIC)
                th, tw = template.shape[:-1]
                # 匹配
                result = cv2.matchTemplate(src, template, match_method)
                similarity = cv2.minMaxLoc(result)[1]
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                # TODO 根据匹配模式分别获取坐标及精度
                if match_method in (cv2.TM_CCORR, cv2.TM_CCORR_NORMED):
                    similarity = min_val
                    top_y, top_x = np.unravel_index(result.argmin(), result.shape)
                else:
                    similarity = max_val
                    top_y, top_x = np.unravel_index(result.argmax(), result.shape)

                # if match_method in (cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED) and similarity < threshold:
                #     return similarity
                # else:
                #     return np.unravel_index(result.argmax(), result.shape)
                # top_y, top_x = np.unravel_index(result.argmax(), result.shape)
                # for test
                # thumb = cv2.rectangle(src, top_x, top_y, tw, th)
                # cv2.namedWindow("test", 1)
                # cv2.imshow("test", mat=src)

            except Exception as e:
                # logger.error("读取待查找模板图片%s错误！" % template_name)
                print(e)
                pass
        return ((top_x, top_y, top_x + tw, top_y + th), similarity) if top_x else similarity


    def en_img_ocr(self, en_img, training_mode=False):
        """
        识别图片中的英文
        :param digital_img: 英文图片，Image对象
        :param training_mode: 是否训练模式
        :return:识别结果字符串
        """
        return self.__img_ocr(en_img, lang='eng', boxes=training_mode)

    def cn_img_ocr(self, cn_img, training_mode=False, config=None):
        """
        识别图片中的汉字
        :param digital_img: 中文图片，Image对象
        :param training_mode: 是否训练模式
        :return:识别结果字符串
        """
        return self.__img_ocr(cn_img, lang='chi_sim', training_mode=training_mode, config=config)

    def digital_img_ocr(self, digital_img, training_mode=False):
        """
        识别图片中的数字
        :param digital_img: 数字图片，Image对象
        :param training_mode: 是否训练模式
        :return:识别结果字符串
        """
        return self.__img_ocr(digital_img, lang='eng', training_mode=training_mode, config='digits')

    def __img_ocr(self, ocr_img, training_mode=False, lang="eng", config=None):

        ocr_text = pytesseract.image_to_string(ocr_img, lang=lang, boxes=training_mode, config=config, encoding='UTF8')

        # if box_name is not None and os.path.exists(box_name):
        #     fp = open(box_name.replace('.jpeg', '.box'), mode='w')
        #     fp.write(ocr_text)
        #     fp.close()

        return ocr_text

    def specify_range_ocr(self, img, box, ocr_mode):

        pass


if __name__ == "__main__":
    img_pro = ImgProcessing()
    print(img_pro.match_graph(
        "d:\\Devlopment\\Python\\GamePlugin\\source\\imgs\\图.bmp",
        'd:\\Devlopment\\Python\\GamePlugin\\source\\imgs\\zd.bmp'
    ))
    print(img_pro.digital_img_ocr(Image.open("d:\\Devlopment\\Python\\GamePlugin\\source\\imgs\\金钱.bmp")))
    # print(digital_img_ocr(Image.open("D:\\Devlopment\\按键精灵\\阴阳师\\阴阳师\\阴阳师\\pic\\截图\\187.bmp")))
    # print(digital_img_ocr(Image.open("D:\\Devlopment\\按键精灵\\阴阳师\\阴阳师\\阴阳师\\pic\\截图\\13164.bmp")))
    # print(digital_img_ocr(Image.open("D:\\Devlopment\\按键精灵\\阴阳师\\阴阳师\\阴阳师\\pic\\截图\\13364.bmp")))
    # print(digital_img_ocr(Image.open("D:\\Devlopment\\按键精灵\\阴阳师\\阴阳师\\阴阳师\\pic\\截图\\23564.bmp")))
