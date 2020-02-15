# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'task.ui'
#
# Created by: PyQt5 UI code generator 5.6
# Run on Anaconda3-4.3.0-Windows-x86_64, Python Version 3.6.0
# WARNING! All changes made in this file will be lost!
import sys, os
import time
import timer
import numpy
import serial
import VideoPlayer, cdown #videos
import flank, verb, verbB, spaceA #tasks
import threading
from xinput3_KeyboardControll_NES_Shooter_addGameTask import sample_first_joystick
from PyQt5 import Qt, QtCore, QtGui, QtWidgets, QtMultimediaWidgets, QtMultimedia,QtTest
from PyQt5.QtCore import QThread ,  pyqtSignal,  QDateTime, Qt 
from PyQt5.QtWidgets import QApplication,  QDialog,  QLineEdit,QLabel, QVBoxLayout,QMessageBox
from EncoderNew import encoder
from pynput.keyboard import Key, Controller
from Powermeter_Test2 import *
from BackendThread import CalTimeThread, EncorderBackendThread,PedalThread


_translate = QtCore.QCoreApplication.translate
class Ui_root(QtWidgets.QMainWindow):
    _answer = QtCore.pyqtSignal(str) #QtSlot for answering questions in task subpy

    def task_run(self):
        ################################################### 
        ###############     RUN TASKS     #################
        # self.cd.run_cd(10)
        # for i in range(15):
        #     self.flnk.run_task(self.counter)
        # self.counter=0
        
        self.cd.run_cd(5)
        for i in range(1):
            self.vrb.run_task(self.counter)
        self.counter=0
        
        self.cd.run_cd(5)
        for i in range(1):
            self.spcA.run_task(self.counter)
        self.counter=0

        self.cd.run_cd(5)
        self.vrbb.run_task(self.counter)
        self.counter=0
        ###################################################

    class Controller(): #Create Controller Class
        
        def __init__(self): #intialise controller
            self.speed=0 #speed value

        #Controller Threading
        def thread_Controller(self):
            sample_first_joystick()

    def __init__(self):
        #values    
        super(Ui_root,self).__init__()
        self.setupUi(self)
        self.counter = 0 #counter value to change task difficulty
        self.disparr = [] #array to store values for displaying on buttons
        self.previousBalance=50 #default Force Balance Value
        self.ansdict={}
        self.timecount = 0

        self.StartBtn.clicked.connect(lambda:self.StartBtnPress())
        self.GameBtn.clicked.connect(lambda:self.GameBtnPress())

        self.initTaskSigSlot() #Connect signal slots used for Tasks

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.TimeDisplay) #connect QtTimer for Elapsed Time
        #self.vidFrame.startVid() #Start Video

# Task Stuff
    def initTaskSigSlot(self):
        
        #connect countdown
        self.cd = cdown.countdown_main()
        self.cd._qnsdisp.connect(self.disp_qns)

        #connect flank task
        self.flnk = flank.flank_main()
        self.flnk._qnsdisp.connect(self.disp_qns)
        self.flnk._ansdisp.connect(self.disp_ans)
        self.flnk._counter.connect(self.counter_add)
        self.flnk._level.connect(self.LevelDisplay)
        self.flnk._qnsshowhide.connect(self.showhideAnswers)
        self._answer.connect(self.flnk.append_ans)

        #connect verb task
        self.vrb = verb.verb_main()
        self.vrb._qnsdisp.connect(self.disp_qns)
        self.vrb._ansdisp.connect(self.disp_ans)
        self.vrb._counter.connect(self.counter_add)
        self.vrb._level.connect(self.LevelDisplay)
        self.vrb._qnsshowhide.connect(self.showhideAnswers)
        self._answer.connect(self.vrb.append_ans)

        #connect verbB task
        self.vrbb = verbB.verbB_main()
        self.vrbb._qnsdisp.connect(self.disp_qns)
        self.vrbb._ansdisp.connect(self.disp_ans)
        self.vrbb._counter.connect(self.counter_add)
        self.vrbb._level.connect(self.LevelDisplay)
        self.vrbb._qnsshowhide.connect(self.showhideAnswers)
        self._answer.connect(self.vrbb.append_ans)

        #connect spaceA task
        self.spcA = spaceA.spaceA_main()
        self.spcA._qnsdisp.connect(self.disp_qns)
        self.spcA._ansdisp.connect(self.disp_ans)
        self.spcA._counter.connect(self.counter_add)
        self.spcA._level.connect(self.LevelDisplay)
        self.spcA._qnsshowhide.connect(self.showhideAnswers)
        self._answer.connect(self.spcA.append_ans)

        #create shortcut for buttons
        self.QuesBtn_A.setShortcut("c")
        self.QuesBtn_B.setShortcut("v")
        self.QuesBtn_X.setShortcut("d")
        self.QuesBtn_Y.setShortcut("f")
        self.QuesBtn_Up.setShortcut(Qt.Key_Up)
        self.QuesBtn_Down.setShortcut(Qt.Key_Down)
        self.QuesBtn_Left.setShortcut(Qt.Key_Left)
        self.QuesBtn_Right.setShortcut(Qt.Key_Right)
        self.QuesBtn_ShldL.setShortcut("e")
        self.QuesBtn_ShldR.setShortcut("r")

        #connect the buttons to answering definition
        self.QuesBtn_A.clicked.connect(lambda:self.answer())
        self.QuesBtn_B.clicked.connect(lambda:self.answer())
        self.QuesBtn_X.clicked.connect(lambda:self.answer())
        self.QuesBtn_Y.clicked.connect(lambda:self.answer())
        self.QuesBtn_Up.clicked.connect(lambda:self.answer())
        self.QuesBtn_Down.clicked.connect(lambda:self.answer())
        self.QuesBtn_Left.clicked.connect(lambda:self.answer())
        self.QuesBtn_Right.clicked.connect(lambda:self.answer())
        self.QuesBtn_ShldL.clicked.connect(lambda:self.answer())
        self.QuesBtn_ShldR.clicked.connect(lambda:self.answer())

    def showhideAnswers(self,value): #Show/Hide UI buttons for displaying answers
        if value == 0:
            self.QuesBtn_Left.hide()
            self.QuesBtn_Down.hide()
            self.QuesBtn_Up.hide()
            self.QuesBtn_Right.hide()

            self.QuesBtn_X.hide()
            self.QuesBtn_Y.hide()
            self.QuesBtn_B.hide()
            self.QuesBtn_A.hide()

            self.QuesBtn_ShldL.hide()
            self.QuesBtn_ShldR.hide()
        elif value == 1:
            self.QuesBtn_Left.show()
            self.QuesBtn_Down.show()
            self.QuesBtn_Up.show()
            self.QuesBtn_Right.show()

            self.QuesBtn_X.show()
            self.QuesBtn_Y.show()
            self.QuesBtn_B.show()
            self.QuesBtn_A.show()

            self.QuesBtn_ShldL.show()
            self.QuesBtn_ShldR.show()
        else:
            pass

    def counter_add(self,boo): #Add/minus to counter
        if boo == 1:
            self.counter += 1
        else:
            #if self.counter > 0:
            self.counter -=1
        self.CntDisplay()

        if self.counter in (3, 5, 7): #change videos if counter reached X value(s)
            self.vidFrame.restartVid()
    
    def disp_qns(self,data,wid,hei): #Display list of Questions in TaskFrame
        pixmap = QtGui.QPixmap(os.path.join(os.path.dirname(__file__), data))
        #pixmap = pixmap.scaled(self.TaskFrame.width(),self.TaskFrame.height(),QtCore.Qt.KeepAspectRatio)
        pixmap = pixmap.scaled(wid,hei,QtCore.Qt.KeepAspectRatio)
        self.TaskFrame.setPixmap(pixmap)

    def disp_ans(self,data): #Display Answers in relevant buttons
        
        if len(data) != 10: #append to fit the list of buttons if list of values are not enough
            pad_len = 10 - len(data)
            for i in range(pad_len):
                data.append('Blank.png')
                #data.append('Blank.png')

        self.ansdict = {'A':data[0],'B':data[1],'X':data[2],'Y':data[3],'U':data[4],'D':data[5],'L':data[6],'R':data[7],'L1':data[8],'R1':data[9]} #dictionary to compare button to picture displayed
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(data[0]))
        self.QuesBtn_A.setIcon(icon)
        self.QuesBtn_A.setIconSize(QtCore.QSize(200,200))

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(data[1]))
        self.QuesBtn_B.setIcon(icon)
        self.QuesBtn_B.setIconSize(QtCore.QSize(200,200))
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(data[2]))
        self.QuesBtn_X.setIcon(icon)
        self.QuesBtn_X.setIconSize(QtCore.QSize(200,200))

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(data[3]))
        self.QuesBtn_Y.setIcon(icon)
        self.QuesBtn_Y.setIconSize(QtCore.QSize(200,200))

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(data[4]))
        self.QuesBtn_Up.setIcon(icon)
        self.QuesBtn_Up.setIconSize(QtCore.QSize(200,200))

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(data[5]))
        self.QuesBtn_Down.setIcon(icon)
        self.QuesBtn_Down.setIconSize(QtCore.QSize(200,200))

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(data[6]))
        self.QuesBtn_Left.setIcon(icon)
        self.QuesBtn_Left.setIconSize(QtCore.QSize(200,200))

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(data[7]))
        self.QuesBtn_Right.setIcon(icon)
        self.QuesBtn_Right.setIconSize(QtCore.QSize(200,200))

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(data[8]))
        self.QuesBtn_ShldL.setIcon(icon)
        self.QuesBtn_ShldL.setIconSize(QtCore.QSize(200,200))

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(data[9]))
        self.QuesBtn_ShldR.setIcon(icon)
        self.QuesBtn_ShldR.setIconSize(QtCore.QSize(200,200))
        '''
        self.QuesBtn_A.setText(data[0])
        self.QuesBtn_B.setText(data[1])
        self.QuesBtn_X.setText(data[2])
        self.QuesBtn_Y.setText(data[3])
        self.QuesBtn_Up.setText(data[4])
        self.QuesBtn_Down.setText(data[5])
        self.QuesBtn_Left.setText(data[6])
        self.QuesBtn_Right.setText(data[7])
        self.QuesBtn_ShldL.setText(data[8])
        self.QuesBtn_ShldR.setText(data[9])
        '''

    def answer(self): #emit answer to task subpy
        sender = self.sender()
        ans = self.ansdict[sender.text()] #check dict in disp_ans for correct value
        self._answer.emit(ans)

    def LevelDisplay(self, data):
        self.TaskValLevel.setText("<font color='White'>"+ str(data) +"</font>")

    def CntDisplay(self):
        self.TaskValCnt.setText("<font color='White'>"+ str(self.counter) +"</font>")

# Video Playing Stuff
    def pauseVid(self): #Pause video + Show warning "speed too low"
        self.vidFrame.pauseVid()
        self.WarnFrame.show()

    def playVid(self): #Play video + Hide warning "speed too low"
        self.vidFrame.startVid()
        self.WarnFrame.hide()

    def videoStartPause(self,data): #Play/Pause video if Speed more or less than
        pausespd = 10 #Pause/Play Threshold Speed
        #Pause video if speed <pausespd
        if data < pausespd:
            self.pauseVid()
        #start video if speed >=pausespd
        else:      
            self.playVid()

# Start Button Stuff                
    def StartBtnPress(self): #Start Video/Task Mode
        self.StartBtn.hide()
        self.GameBtn.hide()
        self.vidFrame.startVid() #Start video 

        #Initialize Controller
        self.controller=self.Controller()        
        th_Controller=threading.Thread(target=self.controller.thread_Controller, args=(),daemon=True)
        th_Controller.start()

        #start Backend signal slot connection
        self.initBackendThread()
 
        # Start thread(s)
        #self.timebackend.start()
        self.backend.start()
        self.pedalBackend.start()

        self.timer.start(1000)

        self.task_run()

    def GameBtnPress(self): #Start Game mode
        self.StartBtn.hide()
        self.GameBtn.hide()
        self.vidFrame.hide() #Hide Video Frames
        self.TaskFrame.hide()
        self.TaskLabCnt.hide()
        self.TaskValCnt.hide()
        self.TaskLabLevel.hide()
        self.TaskValLevel.hide()
        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint) #make window transparent
        
        #Initialize Controller
        self.controller=self.Controller()        
        th_Controller=threading.Thread(target=self.controller.thread_Controller, args=(),daemon=True)
        th_Controller.start()

        #start Backend signal slot connection
        self.initBackendThread()
        
        # Start thread(s)
        #self.timebackend.start()
        self.backend.start()
        self.pedalBackend.start()

        self.timer.start(1000)

# HUD Stuff

    def TimeDisplay(self):
        self.timecount += 1
        self.HUDValTime.setText("<font color='White'>"+ str(self.timecount) +"</font>")

    def HRDisplay(self):
        self.HUDValHR.setText("<font color='White'>"+ str(0) +"</font>")

    def EncoderDisplay(self, data): # UI Slot to recieve Encoder
        self._speed=str(data)
        self.HUDValSpd.setText("<font color='White'>"+ self._speed+"</font>")
        #self.HUDValSpd.setText(_translate("root", ("<font color='White'>"+str(data)+"</font>")))

    def InstantPower(self, data): # UI Slot to recieve InstantPower
        self._InstantPower=str(data)
        self.HUDValInstPwr.setText(_translate("root", "<font color='White'>"+self._InstantPower+"</font>"))

    def AccumPower(self, data): # UI Slot to recieve AccumPower
        self._AccumPower=str(data)
        self.HUDValAccPwr.setText(_translate("root","<font color='White'>"+ self._AccumPower+"</font>"))

    def InstantCandence(self, data): # UI Slot to recieve InstantCandence
        self._InstantCandence=str(data)
        self.HUDValInstCad.setText(_translate("root","<font color='White'>"+self._InstantCandence+"</font>"))

    def Balance(self, data): # UI Slot to recieve Balance
        if data>0:
            self.previousBalance=data
            self.HUDValPBalR.setText(_translate("root","<font color='White'>"+ str(int(round(data)))+"</font>"))
            self.HUDValPBalL.setText(_translate("root","<font color='White'>"+ str(int(round(100-data)))))

        else:
            self.HUDValPBalR.setText(_translate("root","<font color='White'>"+ str(int(round(self.previousBalance)))+"</font>"))
            self.HUDValPBalL.setText(_translate("root","<font color='White'>"+ str(int(round(100-self.previousBalance)))+"</font>"))

    def printSpeed(self,data): #Controller Slot to recieve Encoder Speed and translate to button inputs
        self.speed=data
        #print(data)
        keyboard = Controller()
        #while 1:
        #read speed
        #acceleration
        if self.speed>10:
            keyboard.press('z')            
            #time.sleep(1)
            QtTest.QTest.qWait(1000)
            #keyboard.release('z')                        
            #deceleration
        elif self.speed<10 and self.speed>=0:
            keyboard.release('z')
            #keyboard.press('a')
            #time.sleep(1)
            QtTest.QTest.qWait(1000)
             
        elif self.speed<0:
            keyboard.press('a')
            #time.sleep(1)
            QtTest.QTest.qWait(1000)
            keyboard.release('a') 

    def initBackendThread(self): #Initialize Signal Slots and Backend Threads
        
        # Create backend Threads
        self.timebackend=CalTimeThread()
        self.backend = EncorderBackendThread()
        self.pedalBackend=PedalThread()

        # Signal connect to Slots for Data
        #self.timebackend.time.connect(self.TimeDisplay)                     #Pass time to UI label0-1 
        self.backend.encorderSpeed.connect(self.EncoderDisplay)             #Pass Speed to UI label2 
        self.backend.encorderSpeed.connect(self.printSpeed)                 #Pass Speed to controller slot
        #Encoder Speed control Start/Pause video
        self.backend.encorderSpeed.connect(self.videoStartPause)                          
        self.pedalBackend.pedalInstantPower.connect(self.InstantPower)      #Pass InstantPower to UI label4
        self.pedalBackend.pedalAccumPower.connect(self.AccumPower)          #Pass AccumPower to UI label5
        self.pedalBackend.pedalInstantCandence.connect(self.InstantCandence)#Pass InstantCandence to UI label6
        self.pedalBackend.pedalBalance.connect(self.Balance)                #Pass Balance to UI label7 & 6
        #self.pedalBackend.pedalPowerBaseLine.connect(self.PowerBaseLine)    #Pass PowerBaseLine to UI label9

        # Signal connect to slots for 

# Setup UI Stuff
    def setupUi(self, root):
        root.setObjectName("MainWindow")
        root.resize(1600, 900)
        root.setMinimumSize(QtCore.QSize(1600, 900))
        root.setMaximumSize(QtCore.QSize(1600, 900))
        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)  #make window transparent/stay always on top
        root.setAttribute(QtCore.Qt.WA_TranslucentBackground,on=True)

        # Define Video Task as centralwidget
        self.vidFrame = VideoPlayer.MainWid(self)
        self.setCentralWidget(self.vidFrame)
        #self.vidFrame.hide() #hide video frame
        #self.centralwidget.setObjectName("centralwidget")

        # Define Start Button
        self.StartBtn = QtWidgets.QPushButton(self)
        self.StartBtn.setGeometry(QtCore.QRect(1250, 800, 100, 40))
        self.StartBtn.setFlat(False)
        self.StartBtn.setObjectName("StartBtn")

        # Define Game Button
        self.GameBtn = QtWidgets.QPushButton(self)
        self.GameBtn.setGeometry(QtCore.QRect(1250, 850, 100, 40))
        self.GameBtn.setFlat(False)
        self.GameBtn.setObjectName("GameBtn")

        #Define Warning Frame
        self.WarnFrame = QtWidgets.QLabel(self)
        self.WarnFrame.setGeometry(QtCore.QRect(300,100,800,100))
        self.WarnFrame.setMinimumSize(QtCore.QSize(0, 0))
        self.WarnFrame.setMaximumSize(QtCore.QSize(1000, 800))    
        self.WarnFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.WarnFrame.setText("")
        self.WarnFrame.setAlignment(QtCore.Qt.AlignCenter)
        self.WarnFrame.setObjectName("TaskFrame")
        pixmap = QtGui.QPixmap(os.path.join(os.path.dirname(__file__), "Pause.png"))
        self.WarnFrame.setPixmap(pixmap)
        self.WarnFrame.hide()

        #Define Task Frame
        self.TaskFrame = QtWidgets.QLabel(self)
        self.TaskFrame.setGeometry(QtCore.QRect(200, 40, 1000, 800))
        self.TaskFrame.setMinimumSize(QtCore.QSize(0, 0))
        self.TaskFrame.setMaximumSize(QtCore.QSize(1000, 800))
        self.TaskFrame.setAutoFillBackground(False)
        self.TaskFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.TaskFrame.setText("")
        self.TaskFrame.setAlignment(QtCore.Qt.AlignCenter)
        self.TaskFrame.setObjectName("TaskFrame")
        #pixmap = QtGui.QPixmap(os.path.join(os.path.dirname(__file__), "Center.png"))
        #pixmap = pixmap.scaled(self.TaskFrame.width(),self.TaskFrame.height(),QtCore.Qt.KeepAspectRatio)
        #self.TaskFrame.setPixmap(pixmap)

        font = QtGui.QFont("Gill Sans MT", pointSize = 36, weight = 50)

        self.TaskValLevel = QtWidgets.QLabel(self)
        self.TaskValLevel.setGeometry(QtCore.QRect(10, 50, 80, 50))
        self.TaskValLevel.setFont(font)
        self.TaskValLevel.setAlignment(QtCore.Qt.AlignCenter)
        self.TaskValLevel.setObjectName("TaskValLevel")

        self.TaskValCnt = QtWidgets.QLabel(self)
        self.TaskValCnt.setGeometry(QtCore.QRect(10, 140, 80, 50))
        self.TaskValCnt.setFont(font)
        self.TaskValCnt.setAlignment(QtCore.Qt.AlignCenter)
        self.TaskValCnt.setObjectName("TaskValCnt")

        # Define HUD Frame
        self.HUDFrame = QtWidgets.QWidget(self)
        self.HUDFrame.setGeometry(QtCore.QRect(1400, 0, 200, 900))
        self.HUDFrame.setMaximumSize(QtCore.QSize(1600, 900))
        #self.HUDFrame.setAutoFillBackground(False)
        self.HUDFrame.setObjectName("HUDFrame")
        self.HUDFrame.setStyleSheet("background-color: rgba(0,0,0,15%)")

        # Define Value Display
        font = QtGui.QFont("Gill Sans MT", pointSize = 48, weight = 50)

        self.HUDValTime = QtWidgets.QLabel(self.HUDFrame)
        self.HUDValTime.setGeometry(QtCore.QRect(0, 45, 200, 85))
        self.HUDValTime.setFont(font)
        self.HUDValTime.setAlignment(QtCore.Qt.AlignCenter)
        self.HUDValTime.setObjectName("HUDValTime")

        self.HUDValHR = QtWidgets.QLabel(self.HUDFrame)
        self.HUDValHR.setGeometry(QtCore.QRect(0, 155, 200, 85))
        self.HUDValHR.setFont(font)
        self.HUDValHR.setAlignment(QtCore.Qt.AlignCenter)
        self.HUDValHR.setObjectName("HUDValHR")

        self.HUDValSpd = QtWidgets.QLabel(self.HUDFrame)
        self.HUDValSpd.setGeometry(QtCore.QRect(0, 265, 200, 85))
        self.HUDValSpd.setFont(font)
        self.HUDValSpd.setAlignment(QtCore.Qt.AlignCenter)
        self.HUDValSpd.setObjectName("HUDValSpd")

        self.HUDValInstCad = QtWidgets.QLabel(self.HUDFrame)
        self.HUDValInstCad.setGeometry(QtCore.QRect(0, 375, 200, 85))
        self.HUDValInstCad.setFont(font)
        self.HUDValInstCad.setAlignment(QtCore.Qt.AlignCenter)
        self.HUDValInstCad.setObjectName("HUDValInstCad")

        self.HUDValAccPwr = QtWidgets.QLabel(self.HUDFrame)
        self.HUDValAccPwr.setGeometry(QtCore.QRect(0, 485, 200, 85))
        self.HUDValAccPwr.setFont(font)
        self.HUDValAccPwr.setAlignment(QtCore.Qt.AlignCenter)
        self.HUDValAccPwr.setObjectName("HUDValAccPwr")

        self.HUDValInstPwr = QtWidgets.QLabel(self.HUDFrame)
        self.HUDValInstPwr.setGeometry(QtCore.QRect(0, 595, 200, 85))
        self.HUDValInstPwr.setFont(font)
        self.HUDValInstPwr.setAlignment(QtCore.Qt.AlignCenter)
        self.HUDValInstPwr.setObjectName("HUDValInstPwr")

        self.HUDValPBalR = QtWidgets.QLabel(self.HUDFrame)
        self.HUDValPBalR.setGeometry(QtCore.QRect(100, 705, 100, 85))
        self.HUDValPBalR.setFont(font)
        self.HUDValPBalR.setAlignment(QtCore.Qt.AlignCenter)
        self.HUDValPBalR.setObjectName("HUDValPBalR")

        self.HUDValPBalL = QtWidgets.QLabel(self.HUDFrame)
        self.HUDValPBalL.setGeometry(QtCore.QRect(0, 705, 100, 85))
        self.HUDValPBalL.setFont(font)
        self.HUDValPBalL.setAlignment(QtCore.Qt.AlignCenter)
        self.HUDValPBalL.setObjectName("HUDValPBalL")

        # Define Labels
        font = QtGui.QFont("Gill Sans MT", pointSize = 14)

        self.TaskLabLevel = QtWidgets.QLabel(self)
        self.TaskLabLevel.setGeometry(QtCore.QRect(10, 20, 80, 25))
        self.TaskLabLevel.setFont(font)
        self.TaskLabLevel.setScaledContents(False)
        self.TaskLabLevel.setObjectName("TaskLabLevel")

        self.TaskLabCnt = QtWidgets.QLabel(self)
        self.TaskLabCnt.setGeometry(QtCore.QRect(10, 110, 80, 25))
        self.TaskLabCnt.setFont(font)
        self.TaskLabCnt.setScaledContents(False)
        self.TaskLabCnt.setObjectName("TaskLabCnt")

        self.HUDLabPedBal = QtWidgets.QLabel(self.HUDFrame)
        self.HUDLabPedBal.setGeometry(QtCore.QRect(10, 680, 200, 25))
        self.HUDLabPedBal.setFont(font)
        self.HUDLabPedBal.setScaledContents(False)
        self.HUDLabPedBal.setObjectName("HUDLabPedBal")

        self.HUDLabInstPwr = QtWidgets.QLabel(self.HUDFrame)
        self.HUDLabInstPwr.setGeometry(QtCore.QRect(10, 570, 200, 25))
        self.HUDLabInstPwr.setFont(font)
        self.HUDLabInstPwr.setScaledContents(False)
        self.HUDLabInstPwr.setObjectName("HUDLabInstPwr")

        self.HUDLabInstCad = QtWidgets.QLabel(self.HUDFrame)
        self.HUDLabInstCad.setGeometry(QtCore.QRect(10, 350, 200, 25))
        self.HUDLabInstCad.setFont(font)
        self.HUDLabInstCad.setScaledContents(False)
        self.HUDLabInstCad.setObjectName("HUDLabInstCad")

        self.HUDLabTime = QtWidgets.QLabel(self.HUDFrame)
        self.HUDLabTime.setGeometry(QtCore.QRect(10, 20, 200, 25))
        self.HUDLabTime.setFont(font)
        self.HUDLabTime.setScaledContents(False)
        self.HUDLabTime.setObjectName("HUDLabTime")

        self.HUDLabHR = QtWidgets.QLabel(self.HUDFrame)
        self.HUDLabHR.setGeometry(QtCore.QRect(10, 130, 200, 25))
        self.HUDLabHR.setFont(font)
        self.HUDLabHR.setScaledContents(False)
        self.HUDLabHR.setObjectName("HUDLabHR")

        self.HUDLabSpd = QtWidgets.QLabel(self.HUDFrame)
        self.HUDLabSpd.setGeometry(QtCore.QRect(10, 240, 200, 25))
        self.HUDLabSpd.setFont(font)
        self.HUDLabSpd.setScaledContents(False)
        self.HUDLabSpd.setObjectName("HUDLabSpd")

        self.HUDLabAccPwr = QtWidgets.QLabel(self.HUDFrame)
        self.HUDLabAccPwr.setGeometry(QtCore.QRect(10, 460, 200, 25))
        self.HUDLabAccPwr.setFont(font)
        self.HUDLabAccPwr.setScaledContents(False)
        self.HUDLabAccPwr.setObjectName("HUDLabAccPwr")

        # Define Force Balance Separator VLine
        self.HUDLabPedBalSpr = QtWidgets.QFrame(self.HUDFrame)
        self.HUDLabPedBalSpr.setGeometry(QtCore.QRect(100, 710, 3, 80))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.HUDLabPedBalSpr.sizePolicy().hasHeightForWidth())
        self.HUDLabPedBalSpr.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.HUDLabPedBalSpr.setFont(font)
        self.HUDLabPedBalSpr.setFrameShape(QtWidgets.QFrame.VLine)
        self.HUDLabPedBalSpr.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.HUDLabPedBalSpr.setObjectName("HUDLabPedBalSpr")

        #Define Question Buttons
        QBtnfont = QtGui.QFont("Gill Sans MT", pointSize = 1)
        self.QuesBtn_Left = QtWidgets.QPushButton(self)
        self.QuesBtn_Left.setGeometry(QtCore.QRect(40, 440, 200, 200))
        self.QuesBtn_Left.setFont(QBtnfont)
        self.QuesBtn_Left.setFlat(True)
        self.QuesBtn_Left.setObjectName("QuesBtn_Left")
        self.QuesBtn_Left.hide()

        self.QuesBtn_Down = QtWidgets.QPushButton(self)
        self.QuesBtn_Down.setGeometry(QtCore.QRect(240, 640, 200, 200))
        self.QuesBtn_Down.setFont(QBtnfont)
        self.QuesBtn_Down.setFlat(True)
        self.QuesBtn_Down.setObjectName("QuesBtn_Down")
        self.QuesBtn_Down.hide()

        self.QuesBtn_Up = QtWidgets.QPushButton(self)
        self.QuesBtn_Up.setGeometry(QtCore.QRect(240, 240, 200, 200))
        self.QuesBtn_Up.setFont(QBtnfont)
        self.QuesBtn_Up.setFlat(True)
        self.QuesBtn_Up.setObjectName("QuesBtn_Up")
        self.QuesBtn_Up.hide()

        self.QuesBtn_Right = QtWidgets.QPushButton(self)
        self.QuesBtn_Right.setGeometry(QtCore.QRect(440, 440, 200, 200))
        self.QuesBtn_Right.setFont(QBtnfont)
        self.QuesBtn_Right.setFlat(True)
        self.QuesBtn_Right.setObjectName("QuesBtn_Right")
        self.QuesBtn_Right.hide()

        self.QuesBtn_X = QtWidgets.QPushButton(self)
        self.QuesBtn_X.setGeometry(QtCore.QRect(760, 440, 200, 200))
        self.QuesBtn_X.setFont(QBtnfont)
        self.QuesBtn_X.setFlat(True)
        self.QuesBtn_X.setObjectName("QuesBtn_X")
        self.QuesBtn_X.hide()

        self.QuesBtn_Y = QtWidgets.QPushButton(self)
        self.QuesBtn_Y.setGeometry(QtCore.QRect(960, 240, 200, 200))
        self.QuesBtn_Y.setFont(QBtnfont)
        self.QuesBtn_Y.setFlat(True)
        self.QuesBtn_Y.setObjectName("QuesBtn_Y")
        self.QuesBtn_Y.hide()

        self.QuesBtn_B = QtWidgets.QPushButton(self)
        self.QuesBtn_B.setGeometry(QtCore.QRect(1160, 440, 200, 200))
        self.QuesBtn_B.setFont(QBtnfont)
        self.QuesBtn_B.setFlat(True)
        self.QuesBtn_B.setObjectName("QuesBtn_B")
        self.QuesBtn_B.hide()

        self.QuesBtn_A = QtWidgets.QPushButton(self)
        self.QuesBtn_A.setGeometry(QtCore.QRect(960, 640, 200, 200))
        self.QuesBtn_A.setFont(QBtnfont)
        self.QuesBtn_A.setFlat(True)
        self.QuesBtn_A.setObjectName("QuesBtn_A")
        self.QuesBtn_A.hide()

        self.QuesBtn_ShldL = QtWidgets.QPushButton(self)
        self.QuesBtn_ShldL.setGeometry(QtCore.QRect(240, 20, 200, 200))
        self.QuesBtn_ShldL.setFont(QBtnfont)
        self.QuesBtn_ShldL.setFlat(True)
        self.QuesBtn_ShldL.setObjectName("QuesBtn_ShldL")
        self.QuesBtn_ShldL.hide()

        self.QuesBtn_ShldR = QtWidgets.QPushButton(self)
        self.QuesBtn_ShldR.setGeometry(QtCore.QRect(960, 20, 200, 200))
        self.QuesBtn_ShldR.setFont(QBtnfont)
        self.QuesBtn_ShldR.setFlat(True)
        self.QuesBtn_ShldR.setObjectName("QuesBtn_ShldR")
        self.QuesBtn_ShldR.hide()
        #root.setCentralWidget(self.centralwidget)
 
        self.retranslateUi(root)
        QtCore.QMetaObject.connectSlotsByName(root)

    # Set UI Default Text
    def retranslateUi(self, root):
        root.setWindowTitle(_translate("root", "Cognitive Cycling"))
        #level
        self.TaskLabLevel.setText(_translate("root", "<font color='White'>Level</font>"))
        self.TaskValLevel.setText(_translate("root", "<font color='White'>0</font>"))
        #counter
        self.TaskLabCnt.setText(_translate("root", "<font color='White'>Counter</font>"))
        self.TaskValCnt.setText(_translate("root", "<font color='White'>0</font>"))
        #time
        self.HUDValTime.setText(_translate("root", "<font color='White'>0</font>"))
        #Heart rate
        self.HUDValHR.setText(_translate("root", "<font color='White'>0</font>"))
        #Speed
        self.HUDValSpd.setText(_translate("root", "<font color='White'>0</font>"))
        #cadence
        self.HUDValInstCad.setText(_translate("root", "<font color='White'>0</font>"))
        #Accumulate Power
        self.HUDValAccPwr.setText(_translate("root", "<font color='White'>0</font>"))
        #Instanceous Power
        self.HUDValInstPwr.setText(_translate("root", "<font color='White'>0</font>"))
        self.HUDLabPedBal.setText(_translate("root", "<font color='White'>Pedal Balance L/R (%)</font>"))
        #BalanceL
        self.HUDValPBalL.setText(_translate("root", "<font color='White'>50</font>"))
        self.HUDLabInstPwr.setText(_translate("root", "<font color='White'>Inst. Power (W)</font>"))
        self.HUDLabInstCad.setText(_translate("root", "<font color='White'>Inst. Cadence (RPM)</font>"))
        #BalanceR
        self.HUDValPBalR.setText(_translate("root", "<font color='White'>50</font>"))
        self.HUDLabTime.setText(_translate("root", "<font color='White'>Elapsed Time (s)</font>"))
        self.HUDLabHR.setText(_translate("root", "<font color='White'>Heart Rate (BPM)</font>"))
        self.HUDLabSpd.setText(_translate("root", "<font color='White'>Speed (RPM)</font>"))
        self.HUDLabAccPwr.setText(_translate("root", "<font color='White'>Accum. Power (W)</font>"))
        #Start Btn
        self.StartBtn.setText(_translate("root", "Start Task"))
        #Game Btn
        self.GameBtn.setText(_translate("root", "Start Game"))
        self.QuesBtn_Left.setText(_translate("root", "L"))
        self.QuesBtn_Down.setText(_translate("root", "D"))
        self.QuesBtn_Up.setText(_translate("root", "U"))
        self.QuesBtn_Right.setText(_translate("root", "R"))
        self.QuesBtn_X.setText(_translate("root", "X"))
        self.QuesBtn_Y.setText(_translate("root", "Y"))
        self.QuesBtn_B.setText(_translate("root", "B"))
        self.QuesBtn_A.setText(_translate("root", "A"))
        self.QuesBtn_ShldL.setText(_translate("root", "L1"))
        self.QuesBtn_ShldR.setText(_translate("root", "R1"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    ui = Ui_root()    #Initalise UI
    ui.show()     #Show UI

    sys.exit(app.exec_())

    