from __future__ import print_function  # 确保代码同时在Python2.7和Python3上兼容

import datetime
import tkinter
import numpy as np
import cv2

from 人流量检测系统.数据操作 import datainsert

trackerTypes = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']

multiTracker = cv2.MultiTracker_create()


# 创建各自类型的track跟踪器函数
def createTrackerByName(trackerType):
    # Create a tracker based on tracker name
    if trackerType == trackerTypes[0]:
        tracker = cv2.TrackerBoosting_create()
    elif trackerType == trackerTypes[1]:
        tracker = cv2.TrackerMIL_create()
    elif trackerType == trackerTypes[2]:
        tracker = cv2.TrackerKCF_create()
    elif trackerType == trackerTypes[3]:
        tracker = cv2.TrackerTLD_create()
    elif trackerType == trackerTypes[4]:
        tracker = cv2.TrackerMedianFlow_create()
    elif trackerType == trackerTypes[5]:
        tracker = cv2.TrackerGOTURN_create()
    elif trackerType == trackerTypes[6]:
        tracker = cv2.TrackerMOSSE_create()
    elif trackerType == trackerTypes[7]:
        tracker = cv2.TrackerCSRT_create()
    else:
        tracker = None
        print('Incorrect tracker name')
        print('Available trackers are:')
        for t in trackerTypes:
            print(t)

    return tracker


# 判断两个团块是否重合的函数
# 两个检测框框是否有交叉，如果有交集则返回1, 如果没有交集则返回 0


def overbox(x1, y1, w1, h1, x2, y2, w2, h2):
    '''
    说明：图像中，从左往右是 x 轴（0~无穷大），从上往下是 y 轴（0~无穷大），从左往右是宽度 w ，从上往下是高度 h
    :param x1: 第一个框的左上角 x 坐标
    :param y1: 第一个框的左上角 y 坐标
    :param w1: 第一幅图中的检测框的宽度
    :param h1: 第一幅图中的检测框的高度
    :param x2: 第二个框的左上角 x 坐标
    :param y2:
    :param w2:
    :param h2:
    :return: 两个如果有交集则返回 1, 如果没有交集则返回 0
    '''
    if (x1 > x2 + w2):
        return 0
    if (y1 > y2 + h2):
        return 0
    if (x1 + w1 < x2):
        return 0
    if (y1 + h1 < y2):
        return 0

    else:
        return 1


def peopleDetect(place, datapath):
    if datapath == '' or place == '请选择地点':
        # 设置提交按钮弹出对话框
        tkinter.messagebox.askokcancel(title='提示:', message='请填写完整信息！')
    else:
        # 初始化团块队列bboxes    数目统计变量count
        bboxes = []
        peopleboxes = []
        count = 0
        # 用以第一次运行的标识符
        first = 0
        bs = cv2.createBackgroundSubtractorKNN(detectShadows=False)  # 背景减除器，设置阴影检测
        # 训练帧数
        history = 20
        bs.setHistory(history)
        frames = 0
        camera = cv2.VideoCapture(datapath)
        # 获取人流量统计的开始时间date，存入数据库
        date = datetime.datetime.today()
        # 获取当前时间，用以计算时间差
        beforetime = datetime.datetime.now()
        while True:
            ret, frame = camera.read()  # ret=True/False,判断是否读取到了图片 frame为每一帧图片
            if ret == True:
                fgmask = bs.apply(frame)  # 计算前景掩码，包含 前景的白色值 以及 阴影的灰色值
                if frames < history:
                    frames += 1
                    continue

                # -------------------------------------------------------------------------------------------
                # 1、对团块队列中的团块对象进行更新
                # 如果团块队列中存在团块
                if np.any(bboxes):
                    # 对团块对象进行信息更新。
                    success, bboxes = multiTracker.update(frame)
                    # 设置判断是否
                    for i, newbox in enumerate(bboxes):
                        p1 = (int(newbox[0]), int(newbox[1]))
                        p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
                        cv2.putText(frame, "track:%s" % (i + 1), (int(newbox[0]), int(newbox[1])),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                                    (0, 0, 0), 1, cv2.LINE_AA)
                        cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)

                # 如果没有团块，则继续向下执行
                # -------------------------------------------------------------------------------------------
                # 2、利用findContours函数，查找图像中的动态运动物体
                # 对原始帧膨胀去噪，
                th = cv2.threshold(fgmask.copy(), 244, 255, cv2.THRESH_BINARY)[1]
                # 前景区域形态学处理
                # 进行图像腐蚀。腐蚀可以使白色的小点消失，从而起到消除白色小躁点的作用。iteration的值越高，模糊程度(腐蚀程度)就越高 呈正相关关系
                th = cv2.erode(th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=2)
                # 进行图像的膨胀。图像的膨胀，使白色的点变大，用于去除图像当中的黑点
                dilated = cv2.dilate(th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 3)), iterations=2)
                # 检测运动团块，返回运动团块集合contours
                contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                # -------------------------------------------------------------------------------------------
                # 将第一帧中的检测团块放入bboxes，对其进行跟踪
                # if first == 0:
                #     for c in contours:
                #         if cv2.contourArea(c) > 1000:
                #            (x, y, w, h) = cv2.boundingRect(c)
                #            bbox = x, y, w, h
                #            bboxes.append(bbox)
                #            multiTracker.add(createTrackerByName("CSRT"), frame2, bbox)
                #            count += 1
                #            print(count)
                #     first = 1
                #     continue
                # -------------------------------------------------------------------------------------------
                # 3、遍历检测的动态运动物体团块
                # 遍历所有团块
                for c in contours:
                    # 设置重合标识变量
                    over = 0
                    # 对轮廓设置最小区域限制，筛选掉噪点框
                    # -------------------------------------------------------------------------------------------
                    # 5、消除图像中较小的团块
                    # contourArea是计算面积，只保留面积大于1000的团块，由此消除较小错误模块 如噪点
                    if cv2.contourArea(c) > 1000:
                        # 获取矩形框边界坐标   boundingRect作用是获取 最小外接矩形
                        (x, y, w, h) = cv2.boundingRect(c)
                        # -------------------------------------------------------------------------------------------
                        # 6、判断此动态运动团块是否与团块队列中的团块重合
                        # 如果团块队列中包含团块
                        if np.any(bboxes):
                            # 遍历团块队列
                            # 当遍历pedestrians到最后一个团块后则不再循环
                            # 继续执行后续代码，将新团块装入团块队列
                            for i, box in enumerate(bboxes):
                                # 获取每个团块队列中团块对象的坐标
                                oldx, oldy, oldw, oldh = box
                                # 比较新团块与当前团块对象是否重合
                                # 如果重合则跳出此循环，不将新团块放入团块对列中
                                if overbox(x, y, w, h, oldx, oldy, oldw, oldh):
                                    over = 1
                                    break

                        if over == 0:
                            # 创建一个团块对象
                            count += 1
                            bbox = x, y, w, h

                            bboxes = list(bboxes)
                            bboxes.append(bbox)
                            multiTracker.add(createTrackerByName("CSRT"), frame, bbox)
                            cv2.rectangle(frame, (int(x), int(y)), (int(x + w), int(y + h)), (255, 0, 0), 2, 1)
                            # 将团块对象存储到pedestrians列表中
                            print(count)
                        else:
                            break

                cv2.putText(frame, "Click 'q' to exit!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 170, 50), 2)
                # cv2.imwrite("frame%d.jpg" % count, fgmask) #保存处理后的每一帧图片，JPEG格式的图片
                # cv2.imshow("mog", fgmask)
                # cv2.imshow("thresh", th)
                # cv2.imshow("dilated", dilated)
                # cv2.imshow("diff", frame & cv2.cvtColor(fgmask, cv2.COLOR_GRAY2BGR))
                cv2.imshow("detection", frame)
                if cv2.waitKey(60) & 0xFF == ord('q'):
                    break
            else:
                break

        camera.release()
        cv2.destroyAllWindows()

        # 将data，time，place，peoplecount数据写入数据库
        # 获取当前时间，计算时间差

        aftertime = datetime.datetime.now()
        time = aftertime - beforetime
        datainsert(date, time, place, count)
        tkinter.messagebox.askokcancel(title='完成',
                                       message="人流量检测开始时间：\n" + str(date) + "\n人流量检测时常：" + str(time) + "\n统计人数总人数为：" + str(count) + "\n数据已成功存入数据库！")
