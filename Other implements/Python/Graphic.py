#!/usr/bin/env python3

# Imports.
import sys
import os
import urllib.request
from PyQt4 import QtGui, QtCore


# Info about app.
Main_app = QtGui.QApplication(sys.argv)
Desktop = QtGui.QApplication.desktop()
x, y = Desktop.width(), Desktop.height()

# Root widget.
Root_window = QtGui.QWidget()
Root_window.setWindowFlags(QtCore.Qt.Popup)
Root_window.setGeometry(int(((x/100)*60)),
                        int(((y/100)*15)), 300, 100)
Root_window.setWindowOpacity(85)

# Palette - back of root window.
Palette_for_root = Root_window.palette()
Palette_for_root.setBrush(QtGui.QPalette.Normal, QtGui.QPalette.Background,
                          QtGui.QBrush(QtGui.QPixmap('/background.png')))
Root_window.setPalette(Palette_for_root)

# Picture.
Picture = QtGui.QLabel(parent=Root_window)

# Label.
Label = QtGui.QLabel(parent=Root_window)
Label.setStyleSheet("color: #ffffff; font-family: Inconsolata-LGC;")

# Button to close.
Button = QtGui.QPushButton("Х", parent=Root_window)
Button.setFlat(True)  # Hide border of button.
Button.setStyleSheet("color: #ffffff;")  # White text.
Button.setMaximumSize(15, 15)
QtCore.QObject.connect(Button, QtCore.SIGNAL("clicked()"),
                       lambda: Root_window.hide())
Button.setAutoDefault(True)

# Icon for tray. TODO: write menu-cw for while cycle.
trayIcon = QtGui.QSystemTrayIcon(QtGui.QIcon("icon.jpg"), Main_app)


# Functions.

def func_for_exit():
    """
       This function close application.
    """
    Root_window.hide()
    exit()


def timer():
    """
       Quit after 3 seconds(1st arg).
    """
    QtCore.QTimer.singleShot(10000, func_for_exit)


def formating(raw_string):
    if len(raw_string) > 30:
        text_messange = raw_string[0:30] + '\n' + raw_string[30:60] + '...\n'
        return text_messange
    else:
        return raw_string


def set_text(params_list):
    string = str('Новое сообщение в тред №' + params_list[2][1] + '.\n')
    string += str('Пост номер:' + params_list[0] + '.\n')
    raw_string = params_list[3]
    text_messange = formating(raw_string)
    string += str(text_messange)
    Label.setText(string)
    return True


def set_pic(params_list):
    print('Сейчас я ставлю пикчу')
    try:
        params_list[4].split('.')[2]
    except IndexError:
        pic = str('<img src="' + 'default.jpg' + '" width="100" height="100">') # Use HTML.
        Picture.setText(pic)
        return 0

    file_descr = params_list[4].split('.')[2]
    name_of_tmp = "tmp_pic." + file_descr

    if name_of_tmp in os.listdir():
        os.remove(name_of_tmp)
        pic_file = open(name_of_tmp, 'wb')
        pic_file.write(urllib.request.urlopen(params_list[4]).read())
    else:
        pic_file = open(name_of_tmp, 'wb')
        pic_file.write(urllib.request.urlopen(params_list[4]).read())

    pic = str('<img src="' + 'tmp_pic.' + file_descr + '" width="100" height="100">') # Use HTML.
    print(pic)
    Picture.setText(pic)

#@SimpleThread
def main(params_list):
    set_pic(params_list)
    set_text(params_list)
    Root_window.show()
#    trayIcon.show()
    timer()
    sys.exit(Main_app.exec_())

# Grid table layout.
Grid_for_widget = QtGui.QGridLayout()
Grid_for_widget.addWidget(Picture, 0, 0)
Grid_for_widget.addWidget(Label, 0, 1)
Grid_for_widget.addWidget(Button, 0, 2)
Root_window.setLayout(Grid_for_widget)
