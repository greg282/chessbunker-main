# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main-frame.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
from time import sleep
from pyqt.game import GameFrame
import json
from PyQt5 import QtCore, QtGui, QtWidgets,sip
from PyQt5.QtWidgets import QStackedWidget,QMessageBox
from PyQt5.QtCore import pyqtSignal,QThread
from pyqt.services.service  import *
from pyqt.services.button_function import *
from leaderboard import *
from pyqt.chat import *

class Ui_MainWindow(object):
    MainWindow_=None
    room_join_counter=0
    gameStartData=None
    def setupUi(self, MainWindow):
        MainWindow.closeEvent = self.closeEvent
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("background-color: rgb(36,36,36);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        self.make_initial_frame()

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 29))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.make_menubar()

        app.setStyleSheet("QLabel{font-size:30pt;} QLineEdit{font-size:30pt;} QPushButton{font-size:30pt;}")
        self.MainWindow_=MainWindow


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))


    def make_menubar(self):
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 771, 29))
        self.menubar.setObjectName("menubar")
        self.menuBack = QtWidgets.QMenu(self.menubar)
        self.menuBack.setObjectName("menuBack")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionBack = QtWidgets.QAction(MainWindow)
        self.actionBack.setObjectName("actionBack")
        self.menuBack.addAction(self.actionBack)
        self.menubar.addAction(self.menuBack.menuAction())

        _translate = QtCore.QCoreApplication.translate
        self.menuBack.setTitle(_translate("MainWindow", "Menu"))
        self.actionBack.setText(_translate("MainWindow", "Go back"))

    #Button functions below

    def delete_frame(self):
        sip.delete(self.frame)
    
    #websocket functions
    def chatMSG(self,message):
        if self.chat is not None:
            tmp_res=json.loads(json.loads(message)['message'])
            print(tmp_res)
            tmp_usr=tmp_res['username']
            tmp_msg=tmp_res['message']
            if tmp_usr!=self.game_frame.board.username:
                self.chat.send_message_oponent(tmp_msg,tmp_usr)

    def onMSG(self,ws,message):
        print(message)
        if json.loads(message)['message']!="ROOM_JOINED" and json.loads(json.loads(message)['message'])['type']=="chat":
            self.chatMSG(message)
            return
        if(json.loads(message)['message']=="ROOM_JOINED"):
            self.room_join_counter+=1
            print(self.room_join_counter)
            if(self.room_join_counter==2):
               print(self.room_join_counter)

               self.game_frame.board.threadJoin(self.gameStartData)
               self.game_frame.board.joinThread.start()
          
        if(json.loads(message)['message']!="ROOM_JOINED"):
            tmp_res=json.loads(json.loads(message)['message'])
            tmp_usr=tmp_res['username']
            tmp_move=int(tmp_res['move'])
        if(json.loads(message)['message']!="ROOM_JOINED" and self.game_frame.board.username!=tmp_usr):
            self.game_frame.board.opponent=tmp_usr
            self.game_frame.board.threadConstructor(int(tmp_move))
            self.game_frame.board.search_thread.start()
            #self.game_frame.board.getOnlineMove(int(json.loads(message)['message']))
    #End of button functions

    def make_initial_frame(self):
        #auto genrated code

        _translate = QtCore.QCoreApplication.translate
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setAutoFillBackground(False)
        self.frame.setStyleSheet("background-color: rgb(36, 36, 36);")
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setLineWidth(0)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.log_in_button = QtWidgets.QPushButton(self.frame)
        self.log_in_button.setObjectName("log_in_button")
        self.horizontalLayout_2.addWidget(self.log_in_button)
        self.sign_up_button = QtWidgets.QPushButton(self.frame)
        self.sign_up_button.setObjectName("sign_up_button")
        self.horizontalLayout_2.addWidget(self.sign_up_button)
        self.horizontalLayout.addWidget(self.frame)
        self.log_in_button.setText(_translate("MainWindow", "Log In"))
        self.sign_up_button.setText(_translate("MainWindow", "Sign Up"))
     
        #below adding listeners
        self.sign_up_button.clicked.connect(self.make_signup_form)
        self.log_in_button.clicked.connect(self.make_login_form)
        #self.log_in_button.clicked.connect(self.make_menu_frame)
        #self.log_in_button.clicked.connect(self.make_wait_screen)


    def make_signup_form(self):
        #auto genrated code
        self.delete_frame()
        self.frame_sign_up = QtWidgets.QFrame(self.centralwidget)
        self.frame_sign_up.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_sign_up.sizePolicy().hasHeightForWidth())
        self.frame_sign_up.setSizePolicy(sizePolicy)
        self.frame_sign_up.setAutoFillBackground(False)

        self.frame_sign_up.setStyleSheet("background-color: rgb(36, 36, 36);")
        self.frame_sign_up.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_sign_up.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_sign_up.setLineWidth(0)
        self.frame_sign_up.setObjectName("frame_sign_up")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_sign_up)
        self.gridLayout.setContentsMargins(200, 200, 200, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_signup = QtWidgets.QPushButton(self.frame_sign_up)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_signup.sizePolicy().hasHeightForWidth())
        self.pushButton_signup.setSizePolicy(sizePolicy)
        self.pushButton_signup.setMinimumSize(QtCore.QSize(200, 0))
        self.pushButton_signup.setMaximumSize(QtCore.QSize(200, 16777215))
        self.pushButton_signup.setFlat(False)
        self.pushButton_signup.setObjectName("pushButton_signup")
        self.gridLayout.addWidget(self.pushButton_signup, 6, 0, 1, 2, QtCore.Qt.AlignHCenter)
        self.lineEdit_username = QtWidgets.QLineEdit(self.frame_sign_up)
        self.lineEdit_username.setText("")
        self.lineEdit_username.setObjectName("lineEdit_username")
        self.gridLayout.addWidget(self.lineEdit_username, 1, 1, 1, 1)
        self.label_email = QtWidgets.QLabel(self.frame_sign_up)
        self.label_email.setObjectName("label_email")
        self.gridLayout.addWidget(self.label_email, 0, 0, 1, 1)
        self.label_password = QtWidgets.QLabel(self.frame_sign_up)
        self.label_password.setObjectName("label_password")
        self.gridLayout.addWidget(self.label_password, 2, 0, 1, 1)
        self.lineEdit_email = QtWidgets.QLineEdit(self.frame_sign_up)
        self.lineEdit_email.setObjectName("lineEdit_email")
        self.gridLayout.addWidget(self.lineEdit_email, 0, 1, 1, 1)
        self.label_username = QtWidgets.QLabel(self.frame_sign_up)
        self.label_username.setObjectName("label_username")
        self.gridLayout.addWidget(self.label_username, 1, 0, 1, 1)
        self.lineEdit_password = QtWidgets.QLineEdit(self.frame_sign_up)
        self.lineEdit_password.setText("")
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.gridLayout.addWidget(self.lineEdit_password, 2, 1, 1, 1)
        #adding password repeat
        self.lineEdit_password_repeat = QtWidgets.QLineEdit(self.frame_sign_up)
        self.lineEdit_password_repeat.setText("")
        self.lineEdit_password_repeat.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_password_repeat.setObjectName("lineEdit_password_repeat")
        self.gridLayout.addWidget(self.lineEdit_password_repeat, 3, 1, 1, 1)
        self.label_password_repeat = QtWidgets.QLabel(self.frame_sign_up)
        self.label_password_repeat.setObjectName("label_password_repeat")
        self.gridLayout.addWidget(self.label_password_repeat, 3, 0, 1, 1)
        ### end of adding password repeat
        self.label = QtWidgets.QLabel(self.frame_sign_up)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 4, 0, 1, 2)
        self.horizontalLayout.addWidget(self.frame_sign_up)

        _translate = QtCore.QCoreApplication.translate
        self.pushButton_signup.setText(_translate("MainWindow", "Sign Up"))
        self.label_email.setText(_translate("MainWindow", "Email"))
        self.label_password.setText(_translate("MainWindow", "Password"))
        self.label_username.setText(_translate("MainWindow", "Username"))
        self.label_password_repeat.setText(_translate("MainWindow", "Repeat Password"))


        #below adding listeners
        #self.pushButton_signup.clicked.connect(take_signup_form)
        #pass self instance into function from import
        self.pushButton_signup.clicked.connect(lambda: take_signup_form(self))
        self.actionBack.triggered.connect(self.regenInitalfromSignup)


    def regenInitalfromSignup(self):
        sip.delete(self.frame_sign_up)
        self.actionBack.triggered.disconnect()
        self.make_initial_frame()

    def make_login_form(self):
        self.delete_frame()

        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.formLayout = QtWidgets.QFormLayout(self.frame)
        self.formLayout.setContentsMargins(200, 200, 200, -1)
        self.formLayout.setObjectName("formLayout")
        self.label_username = QtWidgets.QLabel(self.frame)
        self.label_username.setObjectName("label_username")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_username)
        self.lineEdit_username = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_username.setMaxLength(208)
        self.lineEdit_username.setObjectName("lineEdit_username")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_username)
        self.label_password = QtWidgets.QLabel(self.frame)
        self.label_password.setTextFormat(QtCore.Qt.AutoText)
        self.label_password.setObjectName("label_password")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_password)
        self.lineEdit_password = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_password)
        self.pushButton_login = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_login.sizePolicy().hasHeightForWidth())
        self.pushButton_login.setSizePolicy(sizePolicy)
        self.pushButton_login.setObjectName("pushButton_login")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.pushButton_login)
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.label)
        self.horizontalLayout.addWidget(self.frame)

        _translate = QtCore.QCoreApplication.translate
        self.label_username.setText(_translate("MainWindow", "Username"))
        self.label_password.setText(_translate("MainWindow", "Password"))
        self.pushButton_login.setText(_translate("MainWindow", "Log In"))
        self.label.setText(_translate("MainWindow", ""))

        ##listeners below
        #self.pushButton_login.clicked.connect(self.take_login_form)
        #pass self instance into function from import
        self.pushButton_login.clicked.connect(lambda: take_login_form(self))
        self.actionBack.triggered.connect(self.regenerate_initial_frame)


    def make_menu_frame(self):
        self.delete_frame()
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.widget = QtWidgets.QWidget(self.frame)
        self.widget.setStyleSheet("")
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.matchmake_button = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.matchmake_button.sizePolicy().hasHeightForWidth())
        self.matchmake_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.matchmake_button.setFont(font)
        self.matchmake_button.setObjectName("matchmake_button")
        self.verticalLayout.addWidget(self.matchmake_button, 0, QtCore.Qt.AlignHCenter)
        self.globalrankin_button = QtWidgets.QPushButton(self.widget)
        self.globalrankin_button.clicked.connect(self.make_leadearboard)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.globalrankin_button.sizePolicy().hasHeightForWidth())
        self.globalrankin_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.globalrankin_button.setFont(font)
        self.globalrankin_button.setObjectName("globalrankin_button")
        self.verticalLayout.addWidget(self.globalrankin_button, 0, QtCore.Qt.AlignHCenter)
        self.horizontalLayout_2.addWidget(self.widget)
        self.horizontalLayout.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)
   

        _translate = QtCore.QCoreApplication.translate

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.matchmake_button.setText(_translate("MainWindow", "Matchmaking"))
        self.globalrankin_button.setText(_translate("MainWindow", "Global Ranking"))

        #connect actionBack to function
        self.actionBack.triggered.connect(self.regenerate_initial_frame)

    def regenerate_initial_frame(self):
        self.delete_frame()
        self.actionBack.triggered.disconnect()
        self.make_initial_frame()

    def make_wait_screen(self):
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.widget = QtWidgets.QWidget(self.frame)
        self.widget.setStyleSheet("")
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Comfortaa")
        font.setPointSize(25)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.horizontalLayout_2.addWidget(self.widget)
        self.horizontalLayout.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)

        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("MainWindow", "Please wait for opponent ..."))

    def start_game(self,signal):    
    
        self,res_match,s,tmp_user,is_white,ws=self.gameStartData[0],self.gameStartData[1],self.gameStartData[2],self.gameStartData[3],self.gameStartData[4],self.gameStartData[5]
        #intialize chat
        self.chat = ChatWindow(tmp_user,ws)
        self.chat.show()
        ### setup gameframe
        print(signal)
        self.delete_frame()
        #self.game_frame = GameFrame(self,is_white)
        self.game_frame.board.difficulty=1
        self.game_frame.board.username=tmp_user
        #set matchmaking params to board
        self.game_frame.board.id=res_match['id']
        self.game_frame.board.session=s
        self.game_frame.board.ws=ws
        self.horizontalLayout.addWidget(self.game_frame)
        ###widget do kolejnosci gr
        self.widget = QtWidgets.QWidget(self.game_frame)
        self.widget.setGeometry(QtCore.QRect(1000, 14, 161, 111))
        self.widget.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelplayer1 = QtWidgets.QLabel(self.widget)
        self.labelplayer1.setStyleSheet("background-color: rgb(46, 194, 126);")
        self.labelplayer1.setFrameShape(QtWidgets.QFrame.Box)
        self.labelplayer1.setAlignment(QtCore.Qt.AlignCenter)
        self.labelplayer1.setObjectName("labelplayer1")
        self.verticalLayout.addWidget(self.labelplayer1)
        self.labelplayer2 = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelplayer2.sizePolicy().hasHeightForWidth())
        self.labelplayer2.setSizePolicy(sizePolicy)
        self.labelplayer2.setStyleSheet("color: rgb(0, 0, 0);")
        self.labelplayer2.setFrameShape(QtWidgets.QFrame.Box)
        self.labelplayer2.setAlignment(QtCore.Qt.AlignCenter)
        self.labelplayer2.setObjectName("labelplayer2")
        self.verticalLayout.addWidget(self.labelplayer2)
        _translate = QtCore.QCoreApplication.translate
        self.labelplayer1.setText(_translate("MainWindow", "BIALE"))
        self.labelplayer2.setText(_translate("MainWindow", "CZARNE"))
        self.horizontalLayout.addWidget(self.widget)

    def make_leadearboard(self):
        self.leaderboard = Leaderboard(getData())
        self.leaderboard.show()

    #on close event resign user from match
    def closeEvent(self, event):
        print("closing")
        if hasattr(self, 'game_frame') and hasattr(self.game_frame,'board'):
            resign_game(self.game_frame.board.session,self.game_frame.board.id)
            #logout user
            logout(self.game_frame.board.session)
       


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    
    sys.exit(app.exec_())

