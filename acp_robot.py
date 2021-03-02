import decimal
import time

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QInputDialog, QFormLayout
import pyautogui
import keyboard
import csv
from datetime import datetime
import re
import json
import os


class App(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Window Settings
        # self.x, self.y, self.w, self.h = 0, 0, 300, 200
        # self.setGeometry(self.x, self.y, self.w, self.h)
        self.setStyleSheet('.QPushButton { font-size: 12px;}')
        self.window = MainWindow(self)
        self.setCentralWidget(self.window)
        self.setWindowTitle("Auto Click Program")  # Window Title
        self.show()


class SettingWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(SettingWidget, self).__init__(parent)

        if not os.path.exists('setting.json'):
            default_settings = {
                'moving_speed': 0.3,
                'typing_speed': 0.1,
                'email': 'marcuslee1333@gmail.com'
            }

            with open('setting.json', 'w') as outfile:
                json.dump(default_settings, outfile)

        with open('setting.json') as f:
            data = json.load(f)
        #print(data.get('moving_speed'))

        lay = QFormLayout(self)

        self.mMovingSpeeding = QtWidgets.QDoubleSpinBox()
        self.mMovingSpeeding.setDecimals(1)
        self.mMovingSpeeding.setStepType(1)

        self.mTypingSpeeding = QtWidgets.QDoubleSpinBox()
        self.mTypingSpeeding.setDecimals(1)
        self.mTypingSpeeding.setStepType(1)

        self.mMovingSpeeding.setValue(data.get('moving_speed'))
        self.mTypingSpeeding.setValue(data.get('typing_speed'))

        self.mEmail = QtWidgets.QLineEdit(data.get('email'))
        QtWidgets.QLineEdit(data.get('email'))
        # Add widgets to the layout
        lay.addRow("Mouse Moving Speed (second):", self.mMovingSpeeding)
        lay.addRow("Typing Speed (second):", self.mTypingSpeeding)
        lay.addRow("Email:", self.mEmail)

        mBtnSave = QtWidgets.QPushButton('Save')
        mBtnSave.clicked.connect(self.on_mBtnSave_clicked)
        lay.addRow("", mBtnSave)

    def on_mBtnSave_clicked(self):
        default_settings = {
            'moving_speed': self.mMovingSpeeding.value(),
            'typing_speed': self.mTypingSpeeding.value(),
            'email': self.mEmail.text()
        }

        print(default_settings)

        with open('setting.json', 'w') as outfile:
            json.dump(default_settings, outfile)



class HomeWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(HomeWidget, self).__init__(parent)
        self.switch = True
        lay = QtWidgets.QVBoxLayout(self)
        # Buttons
        mBtnStart = QtWidgets.QPushButton("START")  # self.lang["btn_start"])
        mBtnStop = QtWidgets.QPushButton("STOP")  # self.lang["btn_stop"])

        # Button Extra
        mBtnStart.clicked.connect(self.on_mBtnStart_clicked)
        mBtnStop.clicked.connect(self.on_mBtnStop_clicked)

        lay.addWidget(mBtnStart)
        # lay.addWidget(mBtnStop)
        lay.addStretch()

    @QtCore.pyqtSlot()
    def on_mBtnStart_clicked(self):
        print('start...')
        self.window().showMinimized()
        with open('setting.json') as f:
            settings = json.load(f)

        try:
            pyautogui.FAILSAFE = False
            while self.switch:
                if keyboard.is_pressed("esc"):
                    self.switch = False

                time.sleep(1)
                now = datetime.now()
                current_time = now.strftime("%H:%M")

                with open('data.csv', 'r') as data:
                    reader = csv.DictReader(data)
                    for row in reader:
                        # print(row['Time'] +' and ' + current_time)
                        if row['Time'] == current_time:

                            # if current_time == '15':
                            flist = open('script.txt').readlines()
                            actionslist = [s.rstrip('\n') for s in flist]
                            for action in actionslist:
                                if 'Move Mouse To' in action:
                                    position = re.search('\[([^]]+)', action).group(1).split(',')
                                    pyautogui.moveTo(int(position[0]), int(position[1]), duration=settings.get('moving_speed'))
                                    pyautogui.click()
                                elif 'Click' in action:
                                    times = int(re.search('\[([^]]+)', action).group(1))
                                    for i in range(times):
                                        pyautogui.click()
                                elif 'Key in' in action:
                                    field = re.search('\[([^]]+)', action).group(1)
                                    # print('typing....' + row[field])
                                    pyautogui.hotkey('ctrl', 'a')
                                    pyautogui.typewrite(row[field], interval=settings.get('typing_speed'))
                                elif 'Wait' in action:
                                    second = re.search('\[([^]]+)', action).group(1)
                                    time.sleep(decimal.Decimal(second))

        except Exception as e:
            # send email TODO
            print(f"error : {e}")

        self.window().showNormal()

    @QtCore.pyqtSlot()
    def on_mBtnStop_clicked(self):
        self.switch = False
        self.window().showMinimized()


class SetupWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(SetupWidget, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        lay = QtWidgets.QHBoxLayout(self)
        self.mInput = QtWidgets.QListWidget()
        self.mOuput = QtWidgets.QListWidget()

        self.mBtnMoveTo = QtWidgets.QPushButton("Move Mouse To [X,Y]")
        self.mBtnMouseClick = QtWidgets.QPushButton("Mouse Click")
        self.mBtnTyping = QtWidgets.QPushButton("Typing [Field Name]")
        self.mBtnWait = QtWidgets.QPushButton("Wait")

        # self.mButtonToSelected = QtWidgets.QPushButton(">>")
        # self.mBtnMoveToAvailable= QtWidgets.QPushButton(">")
        # self.mBtnMoveToSelected= QtWidgets.QPushButton("<")
        # self.mButtonToAvailable = QtWidgets.QPushButton("<<")

        vlay = QtWidgets.QVBoxLayout()
        # vlay.addStretch()
        vlay.addWidget(self.mBtnMoveTo)
        vlay.addWidget(self.mBtnMouseClick)
        vlay.addWidget(self.mBtnTyping)
        vlay.addWidget(self.mBtnWait)
        vlay.addStretch()

        self.mBtnSave = QtWidgets.QPushButton("Save")
        self.mBtnTest = QtWidgets.QPushButton("Test")

        vlay1 = QtWidgets.QVBoxLayout()
        vlay1.addWidget(self.mOuput)
        vlay1.addWidget(self.mBtnSave)
        vlay1.addWidget(self.mBtnTest)

        self.mBtnUp = QtWidgets.QPushButton("Up")
        self.mBtnDown = QtWidgets.QPushButton("Down")
        self.mBtnRemove = QtWidgets.QPushButton("Remove")
        self.mBtnRemoveAll = QtWidgets.QPushButton("Remove All")

        vlay2 = QtWidgets.QVBoxLayout()
        # vlay2.addStretch()
        vlay2.addWidget(self.mBtnUp)
        vlay2.addWidget(self.mBtnDown)
        vlay2.addWidget(self.mBtnRemove)
        vlay2.addWidget(self.mBtnRemoveAll)
        vlay2.addStretch()

        # lay.addWidget(self.mInput)
        lay.addLayout(vlay)
        lay.addLayout(vlay1)

        lay.addLayout(vlay2)

        self.update_buttons_status()
        self.connections()
        self.get_script()

    def get_script(self):
        flist = open('script.txt').readlines()
        self.mOuput.addItems([s.rstrip('\n') for s in flist])

    @QtCore.pyqtSlot()
    def update_buttons_status(self):

        self.mBtnUp.setDisabled(not bool(self.mOuput.selectedItems()) or self.mOuput.currentRow() == 0)
        self.mBtnDown.setDisabled(
            not bool(self.mOuput.selectedItems()) or self.mOuput.currentRow() == (self.mOuput.count() - 1))

        self.mBtnRemove.setDisabled(not bool(self.mOuput.selectedItems()))
        self.mBtnRemoveAll.setDisabled(self.mOuput.currentRow() == 0)
        # self.mBtnMoveToAvailable.setDisabled(not bool(self.mInput.selectedItems()) or self.mOuput.currentRow() == 0)
        # self.mBtnMoveToSelected.setDisabled(not bool(self.mOuput.selectedItems()))

    def connections(self):
        # self.mInput.itemSelectionChanged.connect(self.update_buttons_status)
        self.mOuput.itemSelectionChanged.connect(self.update_buttons_status)

        self.mBtnMoveTo.clicked.connect(self.on_mBtnMoveTo_clicked)
        self.mBtnMouseClick.clicked.connect(self.on_mBtnMoveClick_clicked)
        self.mBtnTyping.clicked.connect(self.on_mBtnMoveTyping_clicked)
        self.mBtnWait.clicked.connect(self.on_mBtnWait_clicked)

        self.mBtnUp.clicked.connect(self.on_mBtnUp_clicked)
        self.mBtnDown.clicked.connect(self.on_mBtnDown_clicked)
        self.mBtnRemove.clicked.connect(self.on_mBtnRemove_clicked)
        self.mBtnRemoveAll.clicked.connect(self.on_mBtnRemoveAll_clicked)

        self.mBtnSave.clicked.connect(self.on_BtnSave_clicked)
        self.mBtnTest.clicked.connect(self.on_BtnTest_clicked)

    @QtCore.pyqtSlot()
    def on_BtnTest_clicked(self):
        try:
            self.window().showMinimized()
            with open('setting.json') as f:
                settings = json.load(f)

            with open('data_test.csv', 'r') as data:
                reader = csv.DictReader(data)
                for row in reader:
                    # print(row['Time'] +' and ' + current_time)

                    # if current_time == '15':
                    flist = open('script.txt').readlines()
                    actionslist = [s.rstrip('\n') for s in flist]
                    for action in actionslist:
                        if 'Move Mouse To' in action:
                            position = re.search('\[([^]]+)', action).group(1).split(',')
                            pyautogui.moveTo(int(position[0]), int(position[1]),
                                             duration=settings.get('moving_speed'))
                            pyautogui.click()
                        elif 'Click' in action:
                            times = int(re.search('\[([^]]+)', action).group(1))

                            for i in range(times):
                                #print(f'click {i} times')`
                                pyautogui.click()
                        elif 'Key in' in action:
                            field = re.search('\[([^]]+)', action).group(1)
                            # print('typing....' + row[field])
                            pyautogui.hotkey('ctrl', 'a')
                            pyautogui.typewrite(row[field],
                                                interval=settings.get('typing_speed'))
                        elif 'Wait' in action:
                            second = re.search('\[([^]]+)', action).group(1)
                            time.sleep(decimal.Decimal(second))
            self.window().showNormal()
        except Exception as e:
            self.window().showNormal()
            print("error :".e)



    @QtCore.pyqtSlot()
    def on_BtnSave_clicked(self):
        try:
            _actionlist = [self.mOuput.item(i).text() for i in range(self.mOuput.count())]
            print(_actionlist)
            with open('script.txt', 'w') as f:
                f.write("\n".join(_actionlist))

        except Exception as e:
            print("error :".format(e))

    @QtCore.pyqtSlot()
    def on_mBtnMoveTo_clicked(self):
        self.window().showMinimized()
        keyboard.wait('esc')
        x, y = pyautogui.position()
        self.mOuput.addItem(f'Move Mouse To [{x},{y}]')
        self.window().showNormal()

    @QtCore.pyqtSlot()
    def on_mBtnMoveClick_clicked(self):
        times, okPressed = QInputDialog.getInt(self, "Select click time", "Click:", 1, 0, 999, 1)
        self.mOuput.addItem(f'Click [{times}] time')

    @QtCore.pyqtSlot()
    def on_mBtnMoveTyping_clicked(self):
        items = next(csv.reader(open('data.csv')))
        data, okPressed = QInputDialog.getItem(self, "Select data", "Data:", items, 0, False)
        if okPressed and data:
            self.mOuput.addItem("Key in [" + data + "]")

    @QtCore.pyqtSlot()
    def on_mBtnWait_clicked(self):
        second, okPressed = QInputDialog.getDouble(self, "Select second", "Second:", 1, 0, 100, 1)
        if okPressed:
            self.mOuput.addItem(f'Wait [{second}] second')

    @QtCore.pyqtSlot()
    def on_mBtnUp_clicked(self):
        row = self.mOuput.currentRow()
        currentItem = self.mOuput.takeItem(row)
        self.mOuput.insertItem(row - 1, currentItem)
        self.mOuput.setCurrentRow(row - 1)

    @QtCore.pyqtSlot()
    def on_mBtnDown_clicked(self):
        row = self.mOuput.currentRow()
        currentItem = self.mOuput.takeItem(row)
        self.mOuput.insertItem(row + 1, currentItem)
        self.mOuput.setCurrentRow(row + 1)

    @QtCore.pyqtSlot()
    def on_mBtnRemove_clicked(self):
        row = self.mOuput.currentRow()
        self.mOuput.takeItem(row)

    @QtCore.pyqtSlot()
    def on_mBtnRemoveAll_clicked(self):
        self.mOuput.clear()


class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent):
        super(MainWindow, self).__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)
        # Run this after settings
        # self.lang = getLang(config.get("Main", "language"))
        # Initialize tabs
        tab_holder = QtWidgets.QTabWidget()  # Create tab holder
        tab_1 = HomeWidget()  # Tab one
        tab_2 = SetupWidget()  # Tab two
        tab_3 = SettingWidget()  # Tab three
        # Add tabs
        tab_holder.addTab(tab_1, "Main")
        tab_holder.addTab(tab_2, "Setup")
        tab_holder.addTab(tab_3, "Setting")

        layout.addWidget(tab_holder)


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
