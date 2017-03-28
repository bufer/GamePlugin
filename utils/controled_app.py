import time
import random

from PIL import Image
import os, win32gui, win32ui, win32con, win32api, win32process
import ctypes
from ctypes import windll
import psutil
import sys
import OpenGL

from utils.img_processing import ImgProcessing

user32 = windll.user32

def get_process_info(processName=None):
    process_info = dict()
    pids = psutil.pids()
    for pid in pids:
        try:
            p = psutil.Process(pid)    #实例化进程对象
            pname = p.name()
            if processName is None or pname == processName:     #判断实例进程名与输入的进程名是否一致（判断进程是否存活）
                process_info[pid] = pname
        except Exception as e:
            pass
    return process_info


def enumHandler(hwnd, hwnds:list):
    print("Child:",repr(hwnd),repr(win32gui.GetClassName(hwnd)))
    # phwnd = win32gui.GetParent(hwnd)
    # hwnds.get()
    # child_hwnds = hwnds.get('$child_hwnds')
    # if child_hwnds is None:
    #     phwnd
    hwnds.append(hwnd)
    # if win32gui.IsWindowVisible(hwnd):
    #     hwnds.append(hwnd)
    #     pass
        # print(repr(hwnd))
        # print(repr(win32gui.GetClassName(hwnd)))
        # print(repr(win32process.GetWindowThreadProcessId(hwnd)))
        # pss_hwnd = win32process.EnumProcessModules(hwnd)[0]
        # name = win32process.GetModuleFileNameEx(hwnd,pss_hwnd)
        # print(name)

        # if win32gui.GetClassName(hwnd) =='WindowsForms10.Window.8.app.0.33c0d9d':
        # if win32gui.GetClassName(hwnd) =='TaskManagerWindow':
        #     capture_window(hwnd)
        # print(repr(win32gui.GetWindowText(hwnd)))
        # print(repr(win32process.GetProcessId(hwnd)))
        # print(repr(win32process.GetModuleFileNameEx(hwnd, None)))
        # if 'Stack Overflow' in win32gui.GetWindowText(hwnd):
        #     win32gui.MoveWindow(hwnd, 0, 0, 760, 500, True)


def capture_window(hwnd):
    """"""
    img = None
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC=win32ui.CreateDCFromHandle(hwndDC)
    saveDC=mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()

    print(repr(win32gui.GetWindowText(hwnd)))
    print(repr(win32gui.GetWindowRect(hwnd)))
    print(repr(win32gui.GetClientRect(hwnd)))
    winrect = win32gui.GetClientRect(hwnd)

    print(repr(win32gui.ClientToScreen(hwnd, (0,0))))

    w,h = winrect[2] - winrect[0],winrect[3]-winrect[1]
    mx,my = win32gui.GetWindowRect(hwnd)[0:2]
    cx,cy = win32gui.ClientToScreen(hwnd, (0,0))
    # MoniterDev=win32api.EnumDisplayMonitors(None,None)
    # w = MoniterDev[0][2][2]
    # h = MoniterDev[0][2][3]
    #print w,h　　　＃图片大小
    if w and h:
    # if w and h:
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
        saveDC.SelectObject(saveBitMap)
        saveDC.BitBlt((0,0), (w,h), mfcDC, (cx-mx,cy-my), win32con.SRCCOPY)
        # windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(),1)
        # result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(),0)

        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)

        img = Image.frombuffer("RGB",(bmpinfo['bmWidth'],bmpinfo['bmHeight']),bmpstr, 'raw','BGRX',0,1)
        img.show()
        # cc=time.gmtime()
        # bmpname=str(cc[0])+str(cc[1])+str(cc[2])+str(cc[3]+8)+str(cc[4])+str(cc[5]) + "_" + str(hwnd)+".bmp"
        # saveBitMap.SaveBitmapFile(saveDC, bmpname)
        # Image.open(bmpname).save(bmpname[:-4]+".jpg")
        # os.remove(bmpname)
        # jpgname=bmpname[:-4]+".jpg"
        # djpgname=dpath+jpgname
        # copy_command = "move %s %s" % (jpgname, djpgname)
        # os.popen(copy_command)
        # return bmpname[:-4]+".jpg"
    # win32gui.DeleteDC()
    return img


def get_client_rect(hwnd):
    try:
        clientrect = win32gui.GetClientRect(hwnd)
        leftx,lefty = win32gui.ClientToScreen(hwnd, (clientrect[0], clientrect[1]))
        rightx = clientrect[2] + leftx
        righty = clientrect[3] + lefty
        return leftx, lefty, rightx, righty
    except Exception as e:
        print(e)
        pass





def process_info():
    for p in win32process.EnumProcesses():
        win32process.GetCurrentProcessId()


class Utils():
    def enum_all_window(self):
        """遍历窗口下的所有窗口"""
        pass

def moveCursor(hwnd, screen_pos):
    # screen_pos = win32gui.ClientToScreen(hwnd, client_pos)
    win32api.SetCursorPos(screen_pos)


class App():
    def __init__(self, file=None, params=None):
        if file is not None:
            self.run(file, params)
            # self._hwnd = None

    def run(self, file, params=None):
        # chwnd = win32ui.GetActiveWindow()
        # pinfo = win32api.ShellExecute(0, "open", file, params, '', 1)
        pinfo = win32process.CreateProcess(file, '', None, None, 0, win32process.CREATE_SHARED_WOW_VDM,
                                           None, None, win32process.STARTUPINFO())
        self._phwnd = pinfo[0]
        self._ppid = pinfo[2]
        print(repr(pinfo))

    def exit(self, exitCode=0):
        win32process.TerminateProcess(self._phwnd, exitCode)


class AppWindow():
    def __init__(self, hwnd=None, classname=None, pid=None):
        if hwnd:
            self.hwnd = hwnd
        elif classname:
            self.hwnd = self.getHwndByClassname(classname)
        elif pid:
            self.hwnd = self.getHwndByPid(pid)
        else:
            raise Exception("绑定窗口参数未输入！")

        self._window_rect = win32gui.GetWindowRect(self.hwnd)
        client_range = self.getClientRange()
        self.imgproc = ImgProcessing(client_range[2],client_range[3])

    def getPosOnScreen(self, client_pos):
        try:
            return win32gui.ClientToScreen(self.hwnd, (client_pos[0], client_pos[1]))
        except Exception as e:
            pass

    def getClientRange(self, hwnd=None):
        if hwnd is None:
            hwnd = self.hwnd
        client_rect = win32gui.GetWindowRect(hwnd)
        pos = self.getPosOnScreen(client_rect[0:2])
        if pos:
            client_range = (pos[0], pos[1], client_rect[2], client_rect[3])
            return client_range

    def getHwndByClassname(self, classname):
        return win32gui.FindWindow(classname, None)

    def captureWindow(self):
        """"""
        hwndDC = win32gui.GetWindowDC(self.hwnd)
        mfcDC=win32ui.CreateDCFromHandle(hwndDC)
        saveDC=mfcDC.CreateCompatibleDC()
        saveBitMap = win32ui.CreateBitmap()
        print(repr(win32gui.GetWindowRect(self.hwnd)))
        print(repr(win32gui.GetClientRect(self.hwnd)))
        winrect = win32gui.GetClientRect(self.hwnd)

        print("ClientToScreen:",repr(win32gui.ClientToScreen(self.hwnd, (0,0))))

        w,h = winrect[2] - winrect[0],winrect[3]-winrect[1]
        mx,my = win32gui.GetWindowRect(self.hwnd)[0:2]
        cx,cy = win32gui.ClientToScreen(self.hwnd, (0,0))
        # MoniterDev=win32api.EnumDisplayMonitors(None,None)
        # w = MoniterDev[0][2][2]
        # h = MoniterDev[0][2][3]
        if w and h:
            saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
            saveDC.SelectObject(saveBitMap)
            saveDC.BitBlt((0,0), (w,h), mfcDC, (cx-mx,cy-my), win32con.SRCCOPY)
            # windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(),1)
            # result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(),0)

            bmpinfo = saveBitMap.GetInfo()
            bmpstr = saveBitMap.GetBitmapBits(True)

            img = Image.frombuffer("RGB", (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                                   bmpstr, 'raw', 'BGRX', 0, 1)
            # img.show()
            return img

    def getWindowPid(self, hwnd):
        return win32process.GetWindowThreadProcessId(hwnd)

    def getHwndByPid(self, pid):
        def callback(hwnd, hwnds):
            if hwnd == 66744:
                pass
            if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
                _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
                if found_pid == pid:
                    hwnds.append(hwnd)
                return True

        hwnds = []
        win32gui.EnumWindows(callback, hwnds)
        return hwnds[0]

    def getAllChildHwnds(self, hwnd=None):
        hwnds = list()
        if hwnd is None:
            hwnd = self.hwnd
        win32gui.EnumChildWindows(hwnd, enumHandler, hwnds)
        return hwnds

    def click(self, point_range, dbclick=False):
        # TODO 多层次窗口获取点击位置窗口句柄不准确，无发精确定位
        if point_range[0] < point_range[2]:
            start_x = point_range[0]
            end_x = point_range[2]
        else:
            # 防止相等情况下报错，结束坐标加1
            start_x = point_range[2]
            end_x = point_range[0] + 1
        point_x = random.randrange(start_x, end_x)
        if point_range[1] < point_range[3]:
            start_y = point_range[1]
            end_y = point_range[3]
        else:
            # 防止相等情况下报错，结束坐标加1
            start_y = point_range[3]
            end_y = point_range[1] + 1
        point_y = random.randrange(start_y, end_y)
        point = (point_x, point_y)
        spoint=self.getPosOnScreen(point)
        dbclick_time = user32.GetDoubleClickTime()
        old_point = win32gui.GetCursorPos()
        # win32gui.SetForegroundWindow(self.hwnd)
        # win32api.SetCursorPos(spoint)
        # hwnd = win32gui.ChildWindowFromPointEx(self.hwnd,point,win32con.CWP_SKIPINVISIBLE+win32con.CWP_SKIPDISABLED+win32con.CWP_SKIPTRANSPARENT)
        # phwnd = win32gui.ChildWindowFromPointEx(self.hwnd,point,win32con.CWP_SKIPINVISIBLE+win32con.CWP_SKIPDISABLED+win32con.CWP_SKIPTRANSPARENT)
        phwnd = self.hwnd
        hwnd = phwnd
        ctypes_POINT = POINT(point_x, point_y)
        while True:
            print(phwnd, repr(win32gui.GetClassName(phwnd)))
            chwnd = user32.RealChildWindowFromPoint(phwnd, ctypes_POINT)
            if chwnd is None or chwnd == phwnd:
                hwnd = phwnd
            else:
                phwnd = chwnd
                break
        cpoint = win32gui.ScreenToClient(hwnd, spoint)
        print(hwnd, "point:", point, "old_point:", old_point, "spoint:", spoint,"cpoint:",cpoint)
        win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, 1, (cpoint[0] + (cpoint[1] << 16)))
        win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, 1, (cpoint[0] + (cpoint[1] << 16)))
        if dbclick:
            # 随机双击间隔时间
            time.sleep(random.randrange(1, dbclick_time)/1000.0)
            win32api.SendMessage(hwnd,win32con.WM_LBUTTONDOWN, 1, (cpoint[0]+(cpoint[1]<<16)))
            win32api.SendMessage(hwnd,win32con.WM_LBUTTONUP, 1, (cpoint[0]+(cpoint[1]<<16)))

        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        # win32api.SetCursorPos(old_point)

    def find_img(self, matching_img, match_mode='all', match_rect=None, similarity=0.6):
        src_img = self.captureWindow()
        if match_mode != 'all' and match_rect is None:
            raise RangeUnspecifiedError("非全局图片查找模式下查找范围未指定！")

        return self.imgproc.match_graph(src_img, template_img=matching_img)

    def find_img_click(self, matching_img, match_mode='all', match_rect=None, similarity=0.6, dbclick=False):
        # TODO 图片查找模式，1）all:全图范围查找；2）range:指定范围内查找；3）outrange:指定范围外查找；
        # TODO 图片查找后点击模式，1）inside:范围内随机坐标；2）outside:范围外随机坐标；3）offset:相对匹配图片左上角坐标偏移；
        # TODO 点击次数，默认1次，可设置多次点击，间隔时间随机，每次间隔应大于双击间隔
        match_result = self.find_img(matching_img, match_mode, match_rect, similarity)
        if match_result:
            matched_box, threshold = match_result
            print(matched_box, threshold)
            if threshold > similarity:
                self.click(matched_box, dbclick)
                return match_result


class RangeUnspecifiedError(Exception):
    pass

# class

LONG = ctypes.c_int32
sizeof = ctypes.sizeof


class Structure(ctypes.Structure):
    if sizeof(ctypes.c_void_p) == 4:
        _pack_ = 1


class POINT(Structure):
    _fields_ = [
        ('x',   LONG),
        ('y',   LONG),
    ]


if __name__ == "__main__":
    # win32gui.EnumWindows(enumHandler, "d:\\")
    appwin = AppWindow(classname="WindowsForms10.Window.8.app.0.33c0d9d")
    # appwin = AppWindow("TaskManagerWindow")
    # appwin = AppWindow("TTOTAL_CMD")
    # appwin.find_img_click('d:\\Devlopment\\Python\\GamePlugin\\source\\imgs\\tcyl.PNG')
    # appwin = AppWindow("ENMainFrame")
    appwin.find_img_click('d:\\Devlopment\\Python\\GamePlugin\\source\\imgs\\yys.png')
    # appwin.captureWindow()
    # appwin.getAllChildHwnds()
    # appwin.click((120,267,160,268), dbclick=False)
    # app.run("C:\Program Files\Evernote\Evernote\Evernote.exe")
    # app.run("C:\Program Files\BlueStacks\HD-StartLauncher.exe")
    # time.sleep(10)
    # print(str(app.getWinHwnds()))
    # hhwnd = win32gui.FindWindow("ENMainFrame", None)
    # hwnds = list()
    # win32gui.EnumChildWindows(hhwnd, enumHandler, hwnds)
    # print(hwnds)
    # FindWindowEx(hwnd, 0, "thundercommandbutton", "ok")
    # hhwnd = win32gui.FindWindow("WindowsForms10.Window.8.app.0.33c0d9d", None)
    # # hhwnd = win32gui.FindWindow("HH Parent", None)
    # # hhwnd = win32gui.FindWindow("ENMainFrame", None)
    # tid, pid = win32process.GetWindowThreadProcessId(hhwnd)
    # print("pid", str(pid))
    # # print("name", str(win32process.GetModuleFileNameEx(pid)))
    # print(str(hhwnd))
    # print(str(app.getHwndByClassname("BlueStacksApp")))
    #
    # print(str(hwnd))
    # print(get_client_rect(hwnd))
    # capture_window(hhwnd)
    # print(get_process_info())
    # print(get_process_info("chrome.exe"))
    # pss_hwnd = win32process.EnumProcessModules(hhwnd)[0]
    # name = win32process.GetModuleFileNameEx(hhwnd, pss_hwnd)
    # p = psutil.Process(pid)
    # print(p.name)
    # print(win32process.EnumProcesses())