
#all good to go


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage, QPixmap, QFont
import cv2, math, numpy as np, openpyxl, time,datetime
from PyQt5.QtCore import QTimer, QRect
from random import randint
from pyqtgraph import PlotWidget #import pyqtgraph as pg
global path, flag, image, thresh_val, c
flag = 0 ; c = 0
global bboxes, colors, mid_points, trackerTypes, multiTracker, angleArr
angleArr = []
global Thresh_Val, MaxAng, MinAng, Threshcount, ThreshcountFlag, x, y
x = 0
y = 0
global redcol
redcol = False,
MaxAng = 0
MinAng = 0
Threshcount = 0
trackerTypes = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
bboxes = []
multiTracker = None
ThreshcountFlag = 0
colors = []
mid_points = []
path = 0
class Ui_output_dialogue(object):

    def setupUi(self, output_dialogue):
        output_dialogue.setObjectName("output_dialogue")
        output_dialogue.resize(1310, 695)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("logo1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        output_dialogue.setWindowIcon(icon)
        """
        EDITED PART
        """
        self.threshlabel = QLabel(output_dialogue)
        self.threshlabel.setObjectName(u"rangeLabel")
        self.threshlabel.setGeometry(QRect(60, 560, 200, 41))
        font = QFont()
        font.setFamily(u"Rockwell")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.threshlabel.setFont(font)

        self.MaxAngleLabel = QtWidgets.QPushButton(output_dialogue)
        self.MaxAngleLabel.setGeometry(QtCore.QRect(960, 520, 300, 41))
        self.MaxAngleLabel.setStyleSheet("background-color:white;\n"
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
        self.MaxAngleLabel.setObjectName("startstop")


        self.ThreshCountLabel = QtWidgets.QPushButton(output_dialogue)
        self.ThreshCountLabel.setGeometry(QtCore.QRect(960, 600, 300, 41))
        self.ThreshCountLabel.setStyleSheet("background-color:white;\n"
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
        self.ThreshCountLabel.setObjectName("startstop")

        self.AlertLabel = QtWidgets.QPushButton(output_dialogue)
        self.AlertLabel.setGeometry(QtCore.QRect(660, 600, 100, 41))
        self.AlertLabel.setStyleSheet("background-color:light silver;\n"
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
        self.AlertLabel.setObjectName("startstop")

        """EDITED GRAPHICS PLOT"""
        self.centralwidget = QtWidgets.QWidget(output_dialogue)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = PlotWidget(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(730, 70, 571, 441))
        self.graphicsView.setObjectName("graphicsView")
        self.timer1 = QTimer()
        self.timer1.timeout.connect(self.update_Graph)
        self.timer1.start(1000)

        """EDITED GRAPHICS PLOT"""

        self.spinBox = QSpinBox(output_dialogue)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMaximum(360)
        self.spinBox.setGeometry(QRect(230, 560, 71, 41))
        self.spinBox.valueChanged.connect(self.Range_Locker)

        """END OF EDITED PART"""

        self.graphLabel = QLabel(output_dialogue)
        self.graphLabel.setObjectName(u"graphLabel")
        self.graphLabel.setGeometry(QRect(900, 10, 251, 71))
        font = QFont()
        font.setFamily(u"Rockwell")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.graphLabel.setFont(font)

        self.startstop = QtWidgets.QPushButton(output_dialogue)
        self.startstop.setGeometry(QtCore.QRect(410, 540, 160, 41))
        # self.startstop.setStyleSheet("background-color:lightgreen;\n"
        #                              "min-width:10px;\n"
        #                              "paddng:6px;\n"
        #                              "font:bold 14px;\n"
        #                              "border-color:black;\n"
        #                              "border-radius:10px;\n"
        #                              "color:black;\n"
        #                              "border-style:outset;\n"
        #                              "border-width:2px;\n"
        #                              "\n"
        #                              "\n"
        #                              "")
        self.startstop.setObjectName("startstop")
        self.startstop.clicked.connect(self.point_selector)

        self.OutPutScreen = QtWidgets.QLabel(output_dialogue)
        self.OutPutScreen.setGeometry(QtCore.QRect(20, 10, 691, 501))
        self.OutPutScreen.setFrameShape(QtWidgets.QFrame.Box)
        self.OutPutScreen.setFrameShadow(QtWidgets.QFrame.Raised)
        self.OutPutScreen.setLineWidth(6)
        self.OutPutScreen.setText("")
        self.OutPutScreen.setObjectName("OutPutScreen")

        self.restart = QtWidgets.QPushButton(output_dialogue)
        self.restart.setGeometry(QtCore.QRect(595, 540, 160, 41))
        # self.restart.setStyleSheet("background-color:grey;\n"
        #                            "min-width:10px;\n"
        #                            "paddng:6px;\n"
        #                            "font:bold 14px;\n"
        #                            "border-color:black;\n"
        #                            "\n"
        #                            "color:black;\n"
        #                            "border-style:outset;\n"
        #                            "border-width:2px;\n"
        #                            "\n"
        #                            "\n"
        #                            "")
        self.restart.setObjectName("restart")
        self.restart.clicked.connect(self.Restart_proc)

        self.back = QtWidgets.QPushButton(output_dialogue)
        self.back.setGeometry(QtCore.QRect(780, 540, 160, 41))
        # self.back.setStyleSheet("background-color:yellow;\n"
        #                         "min-width:10px;\n"
        #                         "paddng:6px;\n"
        #                         "font:bold 14px;\n"
        #                         "border-color:black;\n"
        #                         "color:black;\n"
        #                         "border-style:outset;\n"
        #                         "border-width:2px;\n"
        #                         "\n"
        #                         "\n"
        #                         "")
        self.back.setObjectName("back")
        self.timer2 = QTimer()
        self.timer2.timeout.connect(lambda: self.viewCam(bboxes, multiTracker))
        self.back.clicked.connect(lambda: self.controlTimer(path))

        self.Browse_Video = QtWidgets.QPushButton(output_dialogue)
        self.Browse_Video.setGeometry(QtCore.QRect(410, 600, 160, 41))
        # self.Browse_Video.setStyleSheet("background-color:lightgreen;\n"
        #                                 "min-width:10px;\n"
        #                                 "paddng:6px;\n"
        #                                 "font:bold 14px;\n"
        #                                 "border-color:black;\n"
        #                                 "border-radius:10px;\n"
        #                                 "color:black;\n"
        #                                 "border-style:outset;\n"
        #                                 "border-width:2px;\n"
        #                                 "\n"
        #                                 "\n"
        #                                 "")
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

    def update_Graph(self):
        global angleArr
        x = []; i =0
        self.graphicsView.clear()
        if len(angleArr) != 0:
            for count, i in enumerate(angleArr):
                x.append(count)
            #print("X: ", x)
            self.graphicsView.plot(x, angleArr, pen=(i, 3))
        else:
            print("NO values found...")

    def browse(self):
        fname = QFileDialog.getOpenFileName(self, "open File", "", "All Files(*);;Python Files (*.mp4)")
        if fname:
            self.label.setText(fname[0])

    def point_selector(self):
        global flag, image, path
        if flag == 0:
            cap = cv2.VideoCapture(path)
            ret, image = cap.read()
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
                    cap.release()
                    break
        #ret, image = self.cap.read()
        print("BBoxes: ", bboxes)
        self.Initializer(bboxes, image)
        # else:
        #     self.viewCam(bboxes,image,multiTracker)

    def Initializer(self,bboxes,image):
        global multiTracker
        print("In Initializer... ")
        trackerType = "CSRT"
        tracker = self.createTrackerByName(trackerType)
        # Create MultiTracker object
        multiTracker = cv2.MultiTracker_create()
        # Initialize MultiTracker
        for bbox in bboxes:
            multiTracker.add(self.createTrackerByName(trackerType), image, bbox)
        print("Done Selecting, start tracking.. ")

    def Range_Locker(self):
        global Thresh_Val
        Thresh_Val = self.spinBox.value()
        # setting value of spin box to the label
        print(f'Value set to {Thresh_Val}')
        #self.label.setText("Value : " + str(value))

    def file_open(a, b):
        global path
        print("file Name: ", b)
        filename = QFileDialog.getOpenFileName()
        path = filename[0]
        print(path)

    def viewCam(self, bboxes, multiTracker):
        global mid_points, Thresh_Val, MaxAng, Threshcount, ThreshcountFlag, redcol, angleArr
        if len(bboxes) != 0 and multiTracker != None:
            #print("In View Cam... ")
            ret, frame = self.cap.read()
            image = frame.copy()
            success, boxes = multiTracker.update(frame)
            if success:
                for i, newbox in enumerate(boxes):
                    p1 = (int(newbox[0]), int(newbox[1]))
                    p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
                    cv2.rectangle(frame, p1, p2, colors[i], 2, 1)
                    mid_point = (int((p1[0] + p2[0]) / 2), int((p1[1] + p2[1]) / 2))
                    cv2.circle(frame, mid_point, 5, (0, 0, 255), -1)
                    cv2.putText(frame, "p" + str(i), (mid_point[0] + 5, mid_point[1] + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                                (0, 0, 255), 2)
                    mid_points.append(mid_point)
                    if len(mid_points) == 3:
                        cv2.line(frame, mid_points[0], mid_points[1], (0, 0, 255), 2)
                        cv2.line(frame, mid_points[1], mid_points[2], (0, 255, 0), 2)
                        x = mid_points[-2][0] - mid_points[-3][0]
                        y = mid_points[-2][0] - mid_points[-1][0]
                        z = mid_points[-2][1] - mid_points[-3][1]
                        w = mid_points[-2][1] - mid_points[-1][1]

                        p = x * y + z * w

                        q = math.sqrt(pow(x, 2) + pow(z, 2))
                        r = math.sqrt(pow(y, 2) + pow(w, 2))

                        s = q * r

                        angle = p / s

                        theta = math.acos(angle)

                        theta = theta * 180 / math.pi  # conversion from rad to degree
                        angleArr.append(theta)
                        theta = round(theta, 2)
                        if theta > MaxAng:
                            MaxAng = theta
                            print(f"Setting max angle to {MaxAng}")
                            text = "Max Angle: " + str(theta)
                            self.MaxAngleLabel.setText(text)
                        if theta < Thresh_Val:
                            cv2.putText(frame, str(theta), (mid_points[-2][0] + 8, mid_points[-2][1] - 10),
                                        cv2.FONT_HERSHEY_SIMPLEX,
                                        0.8,
                                        (255, 255, 255), 2, cv2.LINE_AA)
                            ThreshcountFlag = 0

                            if redcol == False:
                                self.AlertLabel.setStyleSheet("background-color:light silver;\n"
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
                            self.recorder(theta)
                        else:
                            if ThreshcountFlag == 0:

                                Threshcount = 1 + int(Threshcount)
                                ThreshcountFlag = 1
                                text = "Max Angle: " + str(theta)
                                self.ThreshCountLabel.setText(f"Total threshold cross count: {str(Threshcount)}")

                            cv2.putText(frame, f'Value Exceeds Threshold {Thresh_Val}', (20,30),
                                        cv2.FONT_HERSHEY_SIMPLEX,
                                        0.8,
                                        (255, 255, 255), 2, cv2.LINE_AA)
                            cv2.putText(frame, str(theta), (mid_points[-2][0] + 8, mid_points[-2][1] - 10),
                                        cv2.FONT_HERSHEY_SIMPLEX,
                                        0.8,
                                        (255, 255, 255), 2, cv2.LINE_AA)
                            self.recorder(theta)
                            if redcol:
                                self.AlertLabel.setStyleSheet("background-color:red;\n"
                                                              "min-width:10px;\n"
                                                              "paddng:6px;\n"
                                                              "font:bold 14px;\n"
                                                              "border-color:red;\n"
                                                              "border-radius:10px;\n"
                                                              "color:red;\n"
                                                              "border-style:outset;\n"
                                                              "border-width:2px;\n"
                                                              "\n"
                                                              "\n"
                                                              "")
                                redcol = False
                            else:
                                self.AlertLabel.setStyleSheet("background-color:light silver;\n"
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
                                redcol = True
                        mid_points = []
            else:
                # Tracking failure
                cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255),
                            2)
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # get image infos
            height, width, channel = image.shape
            step = channel * width
            # create QImage from image
            qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
            # show image in img_label
            self.OutPutScreen.setPixmap(QPixmap.fromImage(qImg))

        else:
            image = np.full((500, 800, 3), 255, dtype=np.uint8)
            cv2.putText(image, "Choose points first.", (150, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 10), 2)
            cv2.putText(image, "Stop tracking and choose points.", (150, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                        (0, 255, 0),
                        2)
            # image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # get image infos
            height, width, channel = image.shape
            step = channel * width
            # create QImage from image
            qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
            # show image in img_label
            self.OutPutScreen.setPixmap(QPixmap.fromImage(qImg))

    def Restart_proc(self):
        print("resetting things... ")
        global path, flag, bboxes, MaxAng, MinAng
        path = 0
        flag = 0
        bboxes = []
        MaxAng = 0
        Threshcount = 0
        self.MaxAngleLabel.setText(f"Max Angle: {MaxAng}")
        self.ThreshCountLabel.setText(f'Total threshold cross count: {Threshcount}')
        cv2.destroyAllWindows()

    def recorder(self, data):
        global c
        now = datetime.datetime.now()
        try:
            workbook = openpyxl.load_workbook(r'AngleLog.xlsx')
            worksheet = workbook["Logs"]
        except:
            workbook  = openpyxl.Workbook('AngleLog.xlsx')
            worksheet = workbook.create_sheet("Logs")
        if c == 0:
            worksheet.append(("Time","Angle in Degrees"))
            worksheet.append((" ", " "))
            c+=1

        sec = time.time()
        info = (now.strftime("%H:%M:%S"), data)
        worksheet.append(info)
        workbook.save(r'AngleLog.xlsx')

    # start/stop timer
    def controlTimer(self, path):
        # if timer is stopped
        if not self.timer2.isActive():
            # create video capture
            if path == 0:
                self.cap = cv2.VideoCapture(0)
            else:
                self.cap = cv2.VideoCapture(path)
            # start timer
            self.timer2.start(20)
            # update control_bt text
            self.back.setText("Stop tracking")
        # if timer is started
        else:
            # stop timer
            self.timer2.stop()
            # release video capture
            self.cap.release()
            image = np.full((500, 800, 3),
                        255, dtype = np.uint8)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            height, width, channel = image.shape
            step = channel * width
            qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
            # show image in img_label
            self.OutPutScreen.setPixmap(QPixmap.fromImage(qImg))
            # update control_bt text
            self.back.setText("Start tracking")

    def retranslateUi(self, output_dialogue):
        _translate = QtCore.QCoreApplication.translate
        output_dialogue.setWindowTitle(_translate("output_dialogue", "LTTS Services"))
        self.startstop.setText(_translate("output_dialogue", "Point Select"))
        self.restart.setText(_translate("output_dialogue", "Restart"))
        self.back.setText(_translate("output_dialogue", "Start Tracking"))
        self.Browse_Video.setText(_translate("output_dialogue", "Browse Video"))
        self.MaxAngleLabel.setText(_translate("output_dialogue", f"Max Angle: {MaxAng}"))

        self.ThreshCountLabel.setText(_translate("output_dialogue", f"Total threshold cross count: {Threshcount}"))
        self.AlertLabel.setText(_translate("output_dialogue", f"ALERT"))
        self.graphLabel.setText(QtCore.QCoreApplication.translate("output_dialogue", u"DISTANCE-TIME PLOT", None))
        self.threshlabel.setText(QtCore.QCoreApplication.translate("output_dialogue", u"Select Threshold", None))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    output_dialogue = QtWidgets.QDialog()
    ui = Ui_output_dialogue()
    ui.setupUi(output_dialogue)
    output_dialogue.show()
    sys.exit(app.exec_())
