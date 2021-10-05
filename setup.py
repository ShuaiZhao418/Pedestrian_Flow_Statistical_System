"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['系统界面.py']
DATA_FILES = ['数据操作.py','人流量检测.py']
OPTIONS = {'includes':['Tkinter','Tkinter.ttk','Tkinter.scrolledtext','PIL.Image','PIL.ImageTk','tkinter.filedialog.askdirectory','tkinter.messagebox','datetime','numpy','cv2','pymysql'],}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
