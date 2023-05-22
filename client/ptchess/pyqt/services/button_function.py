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

        res=signUpRequest(self.lineEdit_username.text(),self.lineEdit_password.text(),self.lineEdit_email.text())
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
            self.make_menu_frame()
            #connect it to matchmakebutton drawBoard(self,tmp_user,s)
            self.matchmake_button.clicked.connect(lambda: drawBoard(self,tmp_user,s))

        else:
            self.label.setText(_translate("MainWindow", res['message']))    

def bypass_login(self,s):
    self.matchmake_button.clicked.connect(lambda: drawBoard(self,self.game_frame.board.username,s))

def drawBoard(self,tmp_user,s):
    self.user=None
    
    
    #below code for matchmaking
    res_match=matchmaking(s)
    is_white=True

    ws=run_ws_from_other_program(res_match['event_server_url'].split("/")[5],self)

    if(res_match['message']=="Game found successfully"):
        is_white=False
        data=[self,res_match,s,tmp_user,is_white,ws]
        self.gameStartData=data
        self.game_frame = GameFrame(self,is_white)
        self.start_game(0)
    else:
        self.make_wait_screen(s,res_match)
        self.game_frame = GameFrame(self,is_white)
        #put into array self,res_match,s,tmp_user,is_white
        data=[self,res_match,s,tmp_user,is_white,ws]
        self.gameStartData=data
        
   

