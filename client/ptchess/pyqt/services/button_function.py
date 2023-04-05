from time import sleep
from pyqt.game import GameFrame
import json
from PyQt5 import QtCore, QtGui, QtWidgets,sip
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtCore import pyqtSignal
from .service import *
from .ws import *



def take_signup_form(self):
        _translate = QtCore.QCoreApplication.translate

        #verification if password is the same
        if self.lineEdit_password.text()!=self.lineEdit_password_repeat.text():
            self.label.setText(_translate("MainWindow", "Passwords are not the same"))
            return

        res=signUpRequest(self.lineEdit_username.text(),self.lineEdit_email.text(),self.lineEdit_password.text())
        if res['status']==200:
            self.label.setText(_translate("MainWindow",res['message']))
            sip.delete(self.frame_sign_up)
            self.make_initial_frame()
            self.label = QtWidgets.QLabel(self.frame)
            self.label.setGeometry(QtCore.QRect(0, 40, 250, 71))
            self.label.setAlignment(QtCore.Qt.AlignCenter)
            self.label.setObjectName("label")
            self.label.setText(_translate("MainWindow", "Signed up success !"))
            self.label.setStyleSheet("QLabel{font-size:20pt;}")
        else:
            self.label.setText(_translate("MainWindow",res['message']))

def take_login_form(self):
        _translate = QtCore.QCoreApplication.translate
        tmp_user=self.lineEdit_username.text()
        res,s=logInRequest(self.lineEdit_username.text(),self.lineEdit_password.text())

        if res['status']==200:
            self.delete_frame()
            self.user=None
            
            
            #below code for matchmaking
            res_match=matchmaking(s)
            is_white=True
            if(res_match['message']=="Game found successfully"):
                is_white=False
            ws=run_ws_from_other_program(res_match['event_server_url'].split("/")[5],self)
           
            ### setup gameframe
            self.game_frame = GameFrame(self,is_white)
            self.game_frame.board.difficulty=1
            self.game_frame.board.username=tmp_user

            #set matchmaking params to board
            self.game_frame.board.id=res_match['id']
            self.game_frame.board.session=s
            self.game_frame.board.ws=ws
            self.horizontalLayout.addWidget(self.game_frame)
            ###widget do kolejnosci gry

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
            self.labelplayer1.setText(_translate("MainWindow", "BIALE"))
            self.labelplayer2.setText(_translate("MainWindow", "CZARNE"))
            self.horizontalLayout.addWidget(self.widget)

        else:
            self.label.setText(_translate("MainWindow", res['message']))    
