#!/usr/bin/env python3

# Author: Kamlesh Kumar
# Released: June/2022
# mail(author): kamlesh.kumar.19e@iitram.ac.in/patelkamleshpatel364@gmail.com
# version: 1.0.0


# import required libraries
import tensorflow as tf
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (QApplication, QLabel,
                             QMessageBox, QPushButton)
from PyQt5.QtGui import QImage, QPixmap, QIcon
import cv2
import os
import numpy as np
from random import choice
import time
import pandas as pd

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # Setting up the GUI
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowIcon(QIcon('icon.png'))
        MainWindow.resize(950, 770)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)

        # other action buttons
        self.Start = QPushButton(MainWindow)
        self.Start.setGeometry(QtCore.QRect(20, 40, 130, 35))
        self.Start.setObjectName("Start")
        self.Start.setStyleSheet(
            "QPushButton::hover""{""background-color:lightgreen;""}""QPushButton""{""border:None;border-style: outset; border-radius:5px; background-color:rgb(255, 170, 127); font-size:15pt""}")

        self.Exit = QPushButton(MainWindow)
        self.Exit.setGeometry(QtCore.QRect(800, 40, 130, 35))
        self.Exit.setStyleSheet(
            "QPushButton::hover""{""background-color:rgb(255,0,0);""}""QPushButton""{""border:None;border-style: outset; border-radius:5px; background-color:rgb(230, 0, 0); font-size:15pt""}")
        self.Exit.setObjectName("Exit")

        # space to show weCam images and computer guess
        self.ComputerSide = QLabel(MainWindow)
        self.ComputerSide.setGeometry(QtCore.QRect(510, 100, 420, 310))
        self.ComputerSide.setBaseSize(QtCore.QSize(0, 0))
        self.ComputerSide.setAutoFillBackground(True)
        self.ComputerSide.setStyleSheet(
            "border: 2px solid rgb(0,0,0); border-radius: 5px; font-size: 18pt")  # Stylesheet
        self.ComputerSide.setLineWidth(3)
        self.ComputerSide.setTextFormat(QtCore.Qt.PlainText)
        self.ComputerSide.setAlignment(QtCore.Qt.AlignCenter)
        self.ComputerSide.setOpenExternalLinks(False)
        self.ComputerSide.setObjectName("ComputerSide")

        self.PatientSide = QLabel(MainWindow)
        self.PatientSide.setGeometry(QtCore.QRect(20, 100, 420, 310))
        self.PatientSide.setBaseSize(QtCore.QSize(0, 0))
        self.PatientSide.setAutoFillBackground(True)
        self.PatientSide.setStyleSheet(
            "border: 2px solid rgb(0,0,0); border-radius: 5px; font-size: 18pt")  # Stylesheet
        self.PatientSide.setLineWidth(3)
        self.PatientSide.setTextFormat(QtCore.Qt.PlainText)
        self.PatientSide.setAlignment(QtCore.Qt.AlignCenter)
        self.PatientSide.setOpenExternalLinks(False)
        self.PatientSide.setObjectName("PatientSide")

        # to show results and other information
        self.ResultPanal = QLabel(MainWindow)
        self.ResultPanal.setGeometry(QtCore.QRect(65, 420, 820, 310))
        self.ResultPanal.setBaseSize(QtCore.QSize(0, 0))
        self.ResultPanal.setAutoFillBackground(True)
        self.ResultPanal.setStyleSheet(
            "border: 2px solid rgb(0,0,0); border-radius: 5px; font-size: 40pt")  # Stylesheet
        self.ResultPanal.setLineWidth(3)
        self.ResultPanal.setTextFormat(QtCore.Qt.PlainText)
        self.ResultPanal.setAlignment(QtCore.Qt.AlignCenter)
        self.ResultPanal.setOpenExternalLinks(False)
        self.ResultPanal.setObjectName("ResultPanal")

        # setup GUI for initial
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Defining the clicking actions of GUI buttons
        self.Start.clicked.connect(self.start_scanning)
        self.Exit.clicked.connect(self.exit_gui)

        # required variables
        self.fileName = None
        self.stop = False
        self.model = tf.keras.models.load_model("my_model1.h5") # load the pre-trained model for detection
        self.guess = ["rock", "scissors", "paper"]

    # tp setup GUI at initial 
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate(
            "MainWindow", "Real Time teeth segmentation"))
        self.Exit.setText(_translate("MainWindow", "Exit"))
        self.Start.setText(_translate("MainWindow", "Start"))
        self.ComputerSide.setText(_translate(
            "MainWindow", "You'll see me here!"))
        self.PatientSide.setText(_translate(
            "MainWindow", "I'll see you here!"))
        self.ResultPanal.setText(_translate(
            "MainWindow", "Result will be displayed here!\n"+"Adjust your hand and start"))

    # to make prediction
    def predictor(self, test_image, model):
        test_image = test_image[:, :, 0]
        test_image = cv2.resize(test_image, (150, 150))
        test_image = np.expand_dims(test_image, axis=0)
        result = model.predict(test_image)
        if result[0][1] == 1:
            move = "rock"
        elif result[0][2] == 1:
            move = "paper"
        else:
            move = "scissors"

        df = pd.read_excel("logs\logs.xlsx")
        df1 = pd.DataFrame({"Patient's Move": [move]})
        df = df.append(df1)
        df.to_excel("logs.xlsx")
        return move
            
    # to check who won
    def check_winner(self, prediction, guess):
        if prediction == guess:
            return "weWon"
        elif (prediction == "paper" and guess == "rock") or (prediction == "rock" and guess == "scissors") or (prediction == "scissors" and guess == "paper"):
            return "youWon"
        else:
            return "iWon"

    # to start the game
    def start_scanning(self):
        # load the pre-trained model for detection
        if self.model is None:
            try:
                self.model = tf.keras.models.load_model("my_model1.h5")
            except Exception as e:
                print("Could not load the model for detection for because {}".format(e))
                return

        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if ret:
                frame = cv2.resize(frame, (410, 300))
                detection_result = self.predictor(frame, self.model)        # to identify the response of patient.
                guess = choice(['rock', 'paper', 'scissors'])                # to guess the response of other side.
                guess_image = cv2.imread("guess/"+guess+".png")
                guess_image = cv2.resize(guess_image, (410, 300))
                self.displayTo(frame, self.PatientSide)                     # to show patient's response on screen.
                self.displayTo(guess_image, self.ComputerSide)              # to show computer's response on screen.
                winning_result = self.check_winner(detection_result, guess) # to check, who won.
                if winning_result == "weWon":
                    self.ResultPanal.setText("It's a tie!")
                    self.ResultPanal.setAlignment(QtCore.Qt.AlignCenter)
                elif winning_result == "youWon":
                    self.ResultPanal.setText("Congrats!\n"+"You won!")
                    self.ResultPanal.setAlignment(QtCore.Qt.AlignCenter)
                else:
                    self.ResultPanal.setText("Better luck next time!")
                    self.ResultPanal.setAlignment(QtCore.Qt.AlignCenter)
                QApplication.processEvents()
                time.sleep(3)
                self.ResultPanal.setText("Show me another move in...!")
                self.ResultPanal.setAlignment(QtCore.Qt.AlignCenter)
                QApplication.processEvents()
                time.sleep(1)
                for i in range(0, 3, 1):
                    self.ResultPanal.setText(str(i))
                    self.ResultPanal.setAlignment(QtCore.Qt.AlignCenter)
                    QApplication.processEvents()
                    time.sleep(1)
            else:
                # messsage box
                msg = QMessageBox()
                msg.setWindowTitle("Alert!")
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Your camera is not working!")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return

    # To display the image image in GUI, with or without detection
    def displayTo(self, image, frame):
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        # image = cv2.resize(image, (410, 300))
        height, width, channel = image.shape
        step = channel * width
        # create QImage from image
        qImg = QImage(image, width, height, step, QImage.Format_RGB888)
        frame.setPixmap(QPixmap.fromImage(qImg))
        frame.setAlignment(QtCore.Qt.AlignHCenter)
        QApplication.processEvents()

    # To close the GUI
    def exit_gui(self):
        sys.exit()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QDialog()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
