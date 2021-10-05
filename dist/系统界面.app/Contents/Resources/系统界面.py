import datetime
import tkinter
from tkinter import ttk, scrolledtext
from PIL import Image, ImageTk
from tkinter.filedialog import askdirectory
import tkinter.messagebox

from 人流量检测系统.人流量检测 import peopleDetect
from 人流量检测系统.数据操作 import dataquery, datadelete, dataupdate, datainsert


def main():
    # -----------------------------------------人流量统计界面----------------------------------------------
    def peopleDetectinterface():
        # 创建上传与统计界面
        peopleDetectinterface = tkinter.Toplevel()
        # 设置窗口标题与大小
        peopleDetectinterface.title("统计界面")
        peopleDetectinterface['width'] = 400
        peopleDetectinterface['height'] = 250

        # 设置选择地点
        pointlabel = tkinter.Label(peopleDetectinterface, text="请选择统计地点：", font=('黑体', 15))
        pointlabel.place(x=20, y=20, width=150, height=30)
        # 设置地点选择的下拉框
        pointchoice = ttk.Combobox(peopleDetectinterface)
        pointchoice.place(x=140, y=55, width=100, height=25)
        # 设置下拉框的选项
        pointchoice['value'] = ('请选择地点', 'A', 'B', 'C', 'D', 'E', 'F', '无')
        # 设置下拉框的默认值
        pointchoice.current(0)

        # 设置路径选择函数
        def selectPath():

            # 选择文件path_接收文件地址
            path_ = tkinter.filedialog.askopenfilename()
            # path_ = askdirectory()
            path.set(path_)

        # 设置本地视频路径
        videolabel = tkinter.Label(peopleDetectinterface, text="请选择本地视频：", font=('黑体', 15))
        videolabel.place(x=20, y=85, width=150, height=30)
        path = tkinter.StringVar()
        buttonpath=ttk.Button(peopleDetectinterface, text="路径选择", command=selectPath)
        buttonpath.place(x=265, y=120, width=100, height=25)
        entrypath = tkinter.Entry(peopleDetectinterface, textvariable=path)
        entrypath.place(x=60, y=120, width=200, height=25)
        # 设置提交提示文本
        submitlabel = tkinter.Label(peopleDetectinterface, text="填完上述信息，请点击测试按钮：", font=('黑体', 15))
        submitlabel.place(x=25, y=150, width=240, height=30)
        # 设置提交按钮，调用人流量统计函数
        submitbutton = ttk.Button(peopleDetectinterface, text="测试", command=lambda: peopleDetect(pointchoice.get(), entrypath.get()))
        submitbutton.place(x=145, y=190, width=100, height=25)

        peopleDetectinterface.mainloop()

    # -----------------------------------------统计方法提示界面--------------------------------------------
    def statisticsinterface(place, time):
     if place == '请选择地点' or time == '请选择时间':
        # 设置提交按钮弹出对话框
        tkinter.messagebox.askokcancel(title='提示:', message='请选择地点类型和时间类型！')
     else:
        # 创建上传与统计界面
        statisticsinterface = tkinter.Toplevel()
        # 设置窗口大小
        statisticsinterface.title("统计方法参考")
        statisticsinterface['width'] = 1000
        statisticsinterface['height'] = 550
        # 判断地点选项
        if place == "选项一":
            path = "/Users/zhaoshuai/Desktop/选项一地点.png"
            placestring = "请传入A点处的录像视频进行统计。若A处因特殊原因受到影响，则可以用100米内的B、C、D点替换。"
            calstring = "总人流量：即A点测得人流量。"
        elif place == "选项二":
            path = "/Users/zhaoshuai/Desktop/选项二地点.png"
            placestring = "请依次传入A点和D点处的录像视频进行统计。若A处因特殊原因受到影响，则可以用100米内的B、C点替换，D点同理，也可以用E、F进行替换。"
            calstring = "总人流量：A处人流量+50%B处人流量。"
        elif place == "选项三":
            path = "/Users/zhaoshuai/Desktop/选项三地点.png"
            placestring = "请依次传入A点和D点处的录像视频进行统计。若A处因特殊原因受到影响，则可以用100米内的B、C点替换，D点同理，也可以用E、F进行替换。"
            calstring = "总人流量：A处人流量+B处人流量。"
        elif place == "选项四":
            path = "/Users/zhaoshuai/Desktop/选项四地点.png"
            placestring = "请传入A、B、C点处的录像视频进行统计。若A街角因特殊原因受到影响，则可以用100米内的D、E、F处替换。"
            calstring = "总人流量：B处人流量+C处人流量-A处人流量。"
        elif place == "选项五":
            path = "/Users/zhaoshuai/Desktop/选项五地点.png"
            placestring = "请传入A区域的录像视频进行统计。"
            calstring = "总人流量：即A点测得人流量。"
        elif place == "选项六":
            path = "/Users/zhaoshuai/Desktop/选项六地点.png"
            placestring = "请传入自定义区域的录像视频进行统计。"
            calstring = "总人流量：即A点测得人流量。"
        else:
            placestring = "您未选中地点选项！"
        # 判断时间选项
        if time == "选项一":
            timestring = "录像视频时间应为7:00-22:00，连续测得七天。"
        elif time == "选项二":
            timestring = "录像视频时间应为7:00-9:00/11:00-13:00/17:00-19:00/21:00-23:00，连续测得七天。"
        elif time == "选项三":
            timestring = "录像视频时间应为11:00-14:00/17:00-21:00，连续测得七天。"
        elif time == "选项四":
            timestring = "录像视频时间自定义"
        else:
            timestring = "您未选中时间选项！"
        # 以下为根据地点，时间选项，而给出的统计方法指示信息
        photo = ImageTk.PhotoImage(file=path)
        label = tkinter.Label(statisticsinterface, image=photo)
        label.place(x=320, y=20, width=350, height=300)

        placelabel = tkinter.Label(statisticsinterface, text=placestring, font=('黑体', 15))
        placelabel.place(x=10, y=310, width=1000, height=50)

        timelabel = tkinter.Label(statisticsinterface, text=timestring, font=('黑体', 15))
        timelabel.place(x=10, y=350, width=1000, height=50)

        callabel = tkinter.Label(statisticsinterface, text=calstring, font=('黑体', 15))
        callabel.place(x=10, y=390, width=1000, height=50)
        # 设置进入人流量检测界面的按钮
        startbutton = ttk.Button(statisticsinterface, text="进行人流量测算", command=peopleDetectinterface)
        startbutton.place(x=420, y=470, width=150, height=25)

        statisticsinterface.mainloop()

    # -----------------------------------------统计方法选择界面--------------------------------------------
    def choiceinterface():
        # 创建选择地点和时间的界面
        # choiceinterface = tkinter.Tk()
        choiceinterface = tkinter.Toplevel()
        # 设置窗口大小
        choiceinterface.title("选择测算时间和地点")
        choiceinterface['width'] = 1000
        choiceinterface['height'] = 700
        # 设置选择内容
        label = tkinter.Label(choiceinterface, text="选择地点类型:", font=('黑体', 30))
        label.place(x=10, y=20, width=250, height=50)
        label = tkinter.Label(choiceinterface, text="选择时间类型:", font=('黑体', 30))
        label.place(x=630, y=20, width=300, height=50)
        photo = ImageTk.PhotoImage(file="/Users/zhaoshuai/Desktop/选择时间和地点.png")
        label = tkinter.Label(choiceinterface, image=photo)
        label.place(x=40, y=60, width=900, height=550)
        # 设置地点选择提示
        label = tkinter.Label(choiceinterface, text="选择地点:")
        label.place(x=80, y=630, width=130, height=25)
        # 设置时间选择提示
        label = tkinter.Label(choiceinterface, text="选择时间:")
        label.place(x=380, y=630, width=130, height=25)
        # 设置地点选择的下拉框
        placechoice = ttk.Combobox(choiceinterface)
        placechoice.place(x=200, y=630, width=125, height=25)
        # 设置下拉框的选项
        placechoice['value'] = ('请选择地点', '选项一', '选项二', '选项三', '选项四', '选项五', '选项六')
        # 设置下拉框的默认值
        placechoice.current(0)
        # 设置时间选择的下拉框
        timechoice = ttk.Combobox(choiceinterface)
        timechoice.place(x=500, y=630, width=125, height=25)
        # 设置下拉框的选项
        timechoice['value'] = ('请选择时间', '选项一', '选项二', '选项三', '选项四')
        # 设置下拉框的默认值
        timechoice.current(0)
        # 设置提交按钮,并传递选项值
        button = ttk.Button(choiceinterface, text="提 交",
                                command=lambda: statisticsinterface(placechoice.get(), timechoice.get()))
        button.place(x=740, y=630, width=150, height=30)

        choiceinterface.mainloop()

    # -----------------------------------------统计说明界面-----------------------------------------------
    def agreeinterface():
        # 创建统计说明阅读界面
        agreeinterface = tkinter.Tk()
        # 设置窗口大小
        agreeinterface.title("说明")
        agreeinterface['width'] = 1000
        agreeinterface['height'] = 550
        # 设置统计说明内容
        label = tkinter.Label(agreeinterface, text="统计过程声明:", font=('黑体', 45))
        label.place(x=30, y=30, width=300, height=60)
        label = tkinter.Label(agreeinterface, text="1、测算时间一般为七天，时间内应避免重大活动、节假日等。", font=('黑体', 30))
        label.place(x=60, y=120, width=900, height=60)
        label = tkinter.Label(agreeinterface, text="2、如果有极端恶劣天气，如台风等，则应延后测试时间。", font=('黑体', 30))
        label.place(x=60, y=200, width=850, height=60)
        label = tkinter.Label(agreeinterface, text=" 一般天气情况下测算照常。", font=('黑体', 30))
        label.place(x=60, y=280, width=430, height=60)
        label = tkinter.Label(agreeinterface, text="3、测算过程中，会产生许多不可抗因素。测得数据仅以参考。", font=('黑体', 30))
        label.place(x=63, y=360, width=900, height=60)
        # 设置进入选择统计方法的按钮
        button = ttk.Button(agreeinterface, text="统计方法参考", command=choiceinterface)
        button.place(x=170, y=450, width=200, height=30)
        # 设置直接进行人流量检测的按钮
        button = ttk.Button(agreeinterface, text="人流量检测", command=peopleDetectinterface)
        button.place(x=600, y=450, width=200, height=30)

        agreeinterface.mainloop()

    # -----------------------------------------数据库操作界面--------------------------------------------
    def datainterface():
        # 创建数据查询界面
        datainterface = tkinter.Tk()
        # 设置窗口大小
        datainterface.title("测算记录")
        datainterface.geometry("650x500")
        # 滚动文本框
        scr = scrolledtext.ScrolledText(datainterface, width=45, height=13, font=("隶书", 18))  # 滚动文本框（宽，高（这里的高应该是以行数为单位），字体样式）
        scr.place(x=50, y=50)  # 滚动文本框在页面的位置
        data = dataquery()
        scr.insert('end', '                  日期                            时长             地点   人流数量\n')
        for i in data:
            for j in i:
               scr.insert('end', str(j)+'     |     ')
            scr.insert('end', '\n')

        # ------------------------------------------------------------------------------------------------
        # 设置查询操作函数
        def querydata():
            scr.delete(1.0, 'end')
            data = dataquery()
            scr.insert('end', '                  日期                            时长             地点   人流数量\n')
            for i in data:
                for j in i:
                    scr.insert('end', str(j) + '     |     ')
                scr.insert('end', '\n')
            tkinter.messagebox.askokcancel(title='提示:', message='查询数据成功！')

        # ------------------------------------------------------------------------------------------------
        # 设置删除操作界面
        def deletedatainterface():
            # 创建删除数据界面
            deletedatainterface = tkinter.Tk()
            # 设置窗口大小
            deletedatainterface.title("删除数据")
            deletedatainterface['width'] = 600
            deletedatainterface['height'] = 200
            # 设置提示信息
            label = tkinter.Label(deletedatainterface, text="请输入删除数据的日期：", font=('黑体', 30))
            label.place(x=30, y=30, width=350, height=30)
            # 设置输入框
            inputdate = tkinter.Entry(deletedatainterface)
            inputdate.place(x=150, y=90, width=300, height=30)
            # 设置删除数据函数
            def deletedata(data):
                datadelete(data)
                tkinter.messagebox.askokcancel(title='提示:', message='删除数据成功！')
            # 设置确定按钮
            button = ttk.Button(deletedatainterface, text="确   定", command=lambda: deletedata(inputdate.get()))
            button.place(x=215, y=140, width=150, height=30)
            deletedatainterface.mainloop()

        # ------------------------------------------------------------------------------------------------
        # 设置更新数据界面
        def updatedatainterface():
            # 创建更新数据界面
            updatedatainterface = tkinter.Tk()
            # 设置窗口大小
            updatedatainterface.title("更新数据")
            updatedatainterface['width'] = 530
            updatedatainterface['height'] = 400
            # 设置输入提示
            datalabel = tkinter.Label(updatedatainterface, text="请输入日期：", font=('黑体', 30))
            datalabel.place(x=30, y=30, width=200, height=30)
            timelabel = tkinter.Label(updatedatainterface, text="请输入时长：", font=('黑体', 30))
            timelabel.place(x=30, y=90, width=200, height=30)
            placelabel = tkinter.Label(updatedatainterface, text="请输入地点：", font=('黑体', 30))
            placelabel.place(x=30, y=150, width=200, height=30)
            peoplecountlabel = tkinter.Label(updatedatainterface, text="请输入人流量：", font=('黑体', 30))
            peoplecountlabel.place(x=30, y=210, width=200, height=30)
            # 设置输入框
            inputdate = tkinter.Entry(updatedatainterface)
            inputdate.place(x=250, y=30, width=200, height=30)
            inputtime = tkinter.Entry(updatedatainterface)
            inputtime.place(x=250, y=90, width=200, height=30)
            inputplace = tkinter.Entry(updatedatainterface)
            inputplace.place(x=250, y=150, width=200, height=30)
            inputpeoplecount = tkinter.Entry(updatedatainterface)
            inputpeoplecount.place(x=250, y=210, width=200, height=30)

            # 设置更新数据函数
            def updatedata(date, time, place, peoplecount):
                dataupdate(date, time, place, peoplecount)
                tkinter.messagebox.askokcancel(title='提示:', message='更新数据成功！')
            # 设置确定按钮
            button = ttk.Button(updatedatainterface, text="确   定", command=lambda: updatedata(inputdate.get(), inputtime.get(), inputplace.get(), inputpeoplecount.get()))
            button.place(x=200, y=300, width=150, height=30)

            updatedatainterface.mainloop()

        # ------------------------------------------------------------------------------------------------
        # 设置添加数据界面
        def adddatainterface():
            # 创建更新数据界面
            adddatainterface = tkinter.Tk()
            # 设置窗口大小
            adddatainterface.title("插入数据")
            adddatainterface['width'] = 530
            adddatainterface['height'] = 400
            # 设置输入提示
            datalabel = tkinter.Label(adddatainterface, text="请输入日期：", font=('黑体', 30))
            datalabel.place(x=30, y=30, width=200, height=30)
            timelabel = tkinter.Label(adddatainterface, text="请输入时长：", font=('黑体', 30))
            timelabel.place(x=30, y=90, width=200, height=30)
            placelabel = tkinter.Label(adddatainterface, text="请输入地点：", font=('黑体', 30))
            placelabel.place(x=30, y=150, width=200, height=30)
            peoplecountlabel = tkinter.Label(adddatainterface, text="请输入人流量：", font=('黑体', 30))
            peoplecountlabel.place(x=30, y=210, width=200, height=30)
            # 设置输入框
            inputdate = tkinter.Entry(adddatainterface)
            inputdate.place(x=250, y=30, width=200, height=30)
            inputtime = tkinter.Entry(adddatainterface)
            inputtime.place(x=250, y=90, width=200, height=30)
            inputplace = tkinter.Entry(adddatainterface)
            inputplace.place(x=250, y=150, width=200, height=30)
            inputpeoplecount = tkinter.Entry(adddatainterface)
            inputpeoplecount.place(x=250, y=210, width=200, height=30)

            # 设置插入数据函数
            def insertdata(date, time, place, peoplecount):
                datainsert(date, time, place, peoplecount)
                tkinter.messagebox.askokcancel(title='提示:', message='插入数据成功！')

            # 设置确定按钮
            button = ttk.Button(adddatainterface, text="确   定",
                                command=lambda: insertdata(inputdate.get(), inputtime.get(), inputplace.get(),
                                                           inputpeoplecount.get()))
            button.place(x=200, y=300, width=150, height=30)

            adddatainterface.mainloop()

        # 设置"增删查改"按钮
        button = ttk.Button(datainterface, text="增    加", command=adddatainterface)
        button.place(x=120, y=380, width=150, height=30)

        button = ttk.Button(datainterface, text="删    除", command=deletedatainterface)
        button.place(x=380, y=380, width=150, height=30)

        button = ttk.Button(datainterface, text="查    询", command=querydata)
        button.place(x=120, y=440, width=150, height=30)

        button = ttk.Button(datainterface, text="更    改", command=updatedatainterface)
        button.place(x=380, y=440, width=150, height=30)

        datainterface.mainloop()

    # -----------------------------------------统计系统初始界面--------------------------------------------
    def begininterface():
        # 创建进入开始界面
        begininterface = tkinter.Tk()
        # 设置窗口大小
        begininterface.title("智能人流量测算系统")
        begininterface['width'] = 1000
        begininterface['height'] = 550
        # 添加背景图片
        photo = ImageTk.PhotoImage(file="/Users/zhaoshuai/Desktop/开始界面背景.gif")
        label = tkinter.Label(begininterface, image=photo)
        label.place(x=0, y=0, width=1000, heigh=550)
        # 添加提示信息
        label = tkinter.Label(begininterface, text="欢迎使用", font=('黑体', 70), background="AliceBlue")
        label.place(x=40, y=50, width=300, height=80)
        label = tkinter.Label(begininterface, text="智能人流量测算系统", font=('黑体', 60), background="AliceBlue")
        label.place(x=210, y=230, width=570, height=70)
        # 添加"人流量测算"按钮
        button = ttk.Button(begininterface, text="人流量测算", command=agreeinterface)
        button.place(x=250, y=450, width=200, height=30)
        # 添加"查看测算记录"按钮
        button = ttk.Button(begininterface, text="查看测算记录", command=datainterface)
        button.place(x=550, y=450, width=200, height=30)

        begininterface.mainloop()

    begininterface()


if __name__ == "__main__":
    main()

# /Users/zhaoshuai/Desktop/python/venv/bin/py2applet