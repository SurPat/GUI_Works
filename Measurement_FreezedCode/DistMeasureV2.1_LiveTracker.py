
#all good to go

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel, QFileDialog
from PyQt5.QtGui import QImage, QPixmap
import cv2, numpy as np
from PyQt5.QtCore import QTimer
from random import randint
from scipy.spatial import distance as dist

global path, flag
flag = 0
global bboxes, colors, mid_points, trackerTypes
trackerTypes = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
bboxes = []
colors = []
mid_points = []
path = 0
class Ui_output_dialogue(object):

    def setupUi(self, output_dialogue):
        output_dialogue.setObjectName("output_dialogue")
        output_dialogue.resize(898, 638)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("logo1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        output_dialogue.setWindowIcon(icon)
        self.range_but = QtWidgets.QPushButton(output_dialogue)
        self.range_but.setGeometry(QtCore.QRect(130, 520, 201, 31))
        self.range_but.setStyleSheet("background-color:rgb(85, 170, 255);\n"
                                        "min-width:10px;\n"
                                        "paddng:6px;\n"
                                        "font:bold 14px;\n"
                                        "border-color:black;\n"
                                        "color:black;\n"
                                        "border-style:outset;\n"
                                        "border-width:2px;\n"
                                        "\n"
                                        "\n"
                                        "")
        self.range_but.setObjectName("range_but")
        self.range_text = QtWidgets.QTextEdit(output_dialogue)
        self.range_text.setGeometry(QtCore.QRect(60, 520, 61, 31))
        self.range_text.setObjectName("range_text")


        self.startstop = QtWidgets.QPushButton(output_dialogue)
        self.startstop.setGeometry(QtCore.QRect(410, 520, 131, 31))
        self.startstop.setStyleSheet("background-color:lightgreen;\n"
                                        "min-width:10px;\n"
                                        "paddng:6px;\n"
                                        "font:bold 14px;\n"
                                        "border-color:black;\n"
                                        "border-radius:10px;\n"
                                        "color:black;\n"
                                        "border-style:outset;\n"
                                        "border-width:2px;\n"
                                        "\n"
                                        "\n"
                                        "")
        self.startstop.setObjectName("startstop")
        self.timer = QTimer()
        self.timer.timeout.connect(self.point_selector)
        self.startstop.clicked.connect(lambda: self.controlTimer(path))

        self.OutPutScreen = QtWidgets.QLabel(output_dialogue)
        self.OutPutScreen.setGeometry(QtCore.QRect(60, 20, 781, 471))
        self.OutPutScreen.setFrameShape(QtWidgets.QFrame.Box)
        self.OutPutScreen.setFrameShadow(QtWidgets.QFrame.Raised)
        self.OutPutScreen.setLineWidth(6)
        self.OutPutScreen.setText("")
        self.OutPutScreen.setObjectName("OutPutScreen")


        self.restart = QtWidgets.QPushButton(output_dialogue)
        self.restart.setGeometry(QtCore.QRect(600, 520, 91, 31))
        self.restart.setStyleSheet("background-color:grey;\n"
                                    "min-width:10px;\n"
                                    "paddng:6px;\n"
                                    "font:bold 14px;\n"
                                    "border-color:black;\n"
                                    "\n"
                                    "color:black;\n"
                                    "border-style:outset;\n"
                                    "border-width:2px;\n"
                                    "\n"
                                    "\n"
                                    "")
        self.restart.setObjectName("restart")
        self.restart.clicked.connect(self.Restart_proc)


        self.back = QtWidgets.QPushButton(output_dialogue)
        self.back.setGeometry(QtCore.QRect(710, 520, 91, 31))
        self.back.setStyleSheet("background-color:yellow;\n"
                                    "min-width:10px;\n"
                                    "paddng:6px;\n"
                                    "font:bold 14px;\n"
                                    "border-color:black;\n"
                                    "color:black;\n"
                                    "border-style:outset;\n"
                                    "border-width:2px;\n"
                                    "\n"
                                    "\n"
                                    "")
        self.back.setObjectName("back")



        self.Browse_Video = QtWidgets.QPushButton(output_dialogue)
        self.Browse_Video.setGeometry(QtCore.QRect(410, 580, 161, 31))
        self.Browse_Video.setStyleSheet("background-color:lightgreen;\n"
                                            "min-width:10px;\n"
                                            "paddng:6px;\n"
                                            "font:bold 14px;\n"
                                            "border-color:black;\n"
                                            "border-radius:10px;\n"
                                            "color:black;\n"
                                            "border-style:outset;\n"
                                            "border-width:2px;\n"
                                            "\n"
                                            "\n"
                                            "")
        self.Browse_Video.setObjectName("Browse_Video")
        self.Browse_Video.clicked.connect(self.file_open)

        self.retranslateUi(output_dialogue)
        QtCore.QMetaObject.connectSlotsByName(output_dialogue)

    def createTrackerByName(self, trackerType):
        # Create a tracker based on tracker name
        if trackerType == trackerTypes[0]:
            tracker = cv2.legacy.TrackerBoosting_create()
        elif trackerType == trackerTypes[1]:
            tracker = cv2.legacy.TrackerMIL_create()
        elif trackerType == trackerTypes[2]:
            tracker = cv2.legacy.TrackerKCF_create()
        elif trackerType == trackerTypes[3]:
            tracker = cv2.legacy.TrackerTLD_create()
        elif trackerType == trackerTypes[4]:
            tracker = cv2.legacy.TrackerMedianFlow_create()
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

    def browse(self):
        fname = QFileDialog.getOpenFileName(self, "open File", "", "All Files(*);;Python Files (*.mp4)")
        if fname:
            self.label.setText(fname[0])

    def point_selector(self):
        ret, image = self.cap.read()
        global flag
        if flag == 0:
            while True:
                flag = 1
                bbox = cv2.selectROI('MultiTracker', image)
                bboxes.append(bbox)
                colors.append((randint(0, 255), randint(0, 255), randint(0, 255)))
                print("Press q to quit selecting boxes and start tracking")
                print("Press any other key to select next object")
                k = cv2.waitKey(0) & 0xFF
                print(k)
                if k == 113:  # q is pressed
                    cv2.destroyAllWindows()
                    break
        print("BBoxes: ", bboxes)
        self.Initializer(bboxes, image)
        # else:
        #     self.viewCam(bboxes,image,multiTracker)

    def Initializer(self,bboxes,image):
        print("In Initializer... ")
        trackerType = "CSRT"
        tracker = self.createTrackerByName(trackerType)
        # Create MultiTracker object
        multiTracker = cv2.MultiTracker_create()
        # Initialize MultiTracker
        for bbox in bboxes:
            multiTracker.add(self.createTrackerByName(trackerType), image, bbox)
        self.viewCam(bboxes, image, multiTracker)

    def file_open(a, b):
        global path
        print("file Name: ", b)
        filename = QFileDialog.getOpenFileName()
        path = filename[0]
        print(path)

    def viewCam(self, bboxes,frame,multiTracker):
        global mid_points
        print("In View Cam... ")
        ret, frame = self.cap.read()
        success, boxes = multiTracker.update(frame)
        print("Success: ", success)
        print("Checkpt... ")
        if success:
            print("over loop.. ")
            for i, newbox in enumerate(boxes):
                print("Check 1")
                p1 = (int(newbox[0]), int(newbox[1]))
                p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
                print("Check 2")
                cv2.rectangle(frame, p1, p2, colors[i], 2, 1)
                print("Check 3")
                mid_point = (int((p1[0] + p2[0]) / 2), int((p1[1] + p2[1]) / 2))
                cv2.circle(frame, mid_point, 5, (0, 0, 255), -1)
                print("Check 4")
                cv2.putText(frame, "p" + str(i), (mid_point[0] + 5, mid_point[1] + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                            (0, 0, 255), 2)
                mid_points.append(mid_point)
                print("Check 5")
                if len(mid_points) == 2:
                    cv2.line(frame, mid_points[0], mid_points[1], (0, 0, 255), 2)
                    Distance = dist.euclidean(mid_points[0], mid_points[1])
                    cv2.putText(frame, "P0 to P1: " + str(Distance), (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
                    mid_points = []
                    # if Threshold_Distance <= int(Distance):
                    #     cv2.putText(frame, "Distance increased, Machine Malfunction", (frame_width - 500, 80),
                    #                 cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                    #                 (0, 0, 255), 2)
        else:
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # get image infos
        height, width, channel = image.shape
        step = channel * width
        # create QImage from image
        qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
        # show image in img_label
        self.OutPutScreen.setPixmap(QPixmap.fromImage(qImg))

    def Restart_proc(self):
        print("resetting things... ")
        global path, flag
        path = 1
        flag = 0

    # start/stop timer
    def controlTimer(self, path):
        # if timer is stopped
        if not self.timer.isActive():
            # create video capture
            if path == 0:
                self.cap = cv2.VideoCapture(0)
            else:
                self.cap = cv2.VideoCapture(path)
            # start timer
            self.timer.start(20)
            # update control_bt text
            self.startstop.setText("Stop")
        # if timer is started
        else:
            # stop timer
            self.timer.stop()
            # release video capture
            self.cap.release()
            image = np.full((500, 500, 3),
                        255, dtype = np.uint8)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            height, width, channel = image.shape
            step = channel * width
            qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
            # show image in img_label
            self.OutPutScreen.setPixmap(QPixmap.fromImage(qImg))
            # update control_bt text
            self.startstop.setText("Start")

    def retranslateUi(self, output_dialogue):
        _translate = QtCore.QCoreApplication.translate
        output_dialogue.setWindowTitle(_translate("output_dialogue", "LTTS Services"))
        self.range_but.setText(_translate("output_dialogue", "Enter and Press"))
        self.startstop.setText(_translate("output_dialogue", "Start/Stop"))
        self.restart.setText(_translate("output_dialogue", "Restart"))
        self.back.setText(_translate("output_dialogue", "Back"))
        self.Browse_Video.setText(_translate("output_dialogue", "Browse Video"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    output_dialogue = QtWidgets.QDialog()
    ui = Ui_output_dialogue()
    ui.setupUi(output_dialogue)
    output_dialogue.show()
    sys.exit(app.exec_())
