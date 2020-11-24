import ctypes
from dronekit import connect, LocationGlobalRelative
from pymavlink import mavutil
from dronekit.mavlink import APIException
import sys
import socket
import threading
import datetime
from PyQt5.QtGui import QPixmap, QIcon, QRegExpValidator
from PyQt5.QtCore import Qt, QTimer, QRegExp, pyqtSignal, QThread
from PyQt5.QtWidgets import QSplashScreen, QMessageBox, QApplication, QLabel, QWidget, QFileDialog, QMainWindow, \
    QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox

print(threading.active_count())
class Window(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.lock = threading.RLock()
        self.th1 = None
        self.filename = None
        self.sock1 = None
        self.th2 = None
        self.th3 = None
        self.label3 = None
        self.label4 = None
        self.label5 = None
        self.label6 = None
        self.label7 = None
        self.text = False
        self.setGeometry(450, 50, 460, 500)
        self.setFixedWidth(460)
        self.setWindowTitle("NPNT CLIENT")
        self.setWindowIcon(QIcon("icon.png"))
        widget = QWidget()
        self.setCentralWidget(widget)
        self.vbox = QVBoxLayout()
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        widget.setLayout(self.vbox)
        self.vbox.addLayout(self.hbox1)
        h_label = QLabel()
        pix = QPixmap('logo250x100.jpg')
        pix.scaled(250, 700)
        #h_label.setFixedSize(250,100)
        h_label.setPixmap(pix)
        h_label.show()
        self.hbox1.addWidget(h_label)

        self.connect_vbox = QVBoxLayout()
        """        self.lineEdit = QLineEdit()
        self.lineEdit.setPlaceholderText("192.168.168.168")
        my_regex = QRegExp("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
        my_validator = QRegExpValidator(my_regex, self.lineEdit)
        self.lineEdit.setValidator(my_validator)
        self.connect_vbox.addWidget(self.lineEdit)"""
        self.combobox()
        self.con = 'Connect'
        self.connectButton = QPushButton(self.con)
        self.connectButton.setFixedHeight(40)
        self.hbox1.addLayout(self.connect_vbox)
        self.connect_vbox.addWidget(self.connectButton)
        self.connectButton.setStyleSheet("font:bold 10pt Arial;background-color:rgb(230, 236, 242)")
        self.connectButton.clicked.connect(self.connection_th)
        self.wid = QWidget()
        self.wid.setStyleSheet("background-color:rgb(0,0,0)")
        self.minor_vbox = QVBoxLayout()

        self.wid.setLayout(self.minor_vbox)
        self.label1 = QLabel('Console Messages>>')
        self.label1.setStyleSheet("font:bold 12pt Arial; text-align:center ;background-color: black;color:white")
        self.label1.setAlignment(Qt.AlignLeft)
        self.minor_vbox.addWidget(self.label1)
        self.vbox.addWidget(self.wid)
        self.consoleLabels()

        self.msg1 = "Connect with RFM"
        self.label2 = QLabel(self.msg1)
        self.label2.setStyleSheet("font:Normal 12pt Arial; background-color: black;color:white")
        self.label2.setFixedHeight(50)
        self.vbox.addWidget(self.label2)
        self.vbox.addLayout(self.hbox2)
        self.lowerButtons()
        print(threading.active_count())
    def consoleLabels(self):
        self.label3 = QLabel("Connect with Vehicle to Download logs")
        self.label3.setStyleSheet("font:normal 12pt Arial; text-align:center ;background-color: black;color:white")
        self.label3.setAlignment(Qt.AlignLeft)
        self.minor_vbox.addWidget(self.label3)
        self.label3.setWordWrap(True)

        self.label4 = QLabel("Choose PA file (.xml) to start PA Validation")
        self.label4.setStyleSheet("font:normal 12pt Arial; text-align:center ;background-color: black;color:white")
        self.label4.setAlignment(Qt.AlignLeft)
        self.minor_vbox.addWidget(self.label4)

        self.label5 = QLabel('UAV will arm only if PA is Valid')
        self.label5.setStyleSheet("font:normal 12pt Arial; text-align:center ;background-color: black;color:white")
        self.label5.setAlignment(Qt.AlignLeft)
        self.minor_vbox.addWidget(self.label5)

        self.label6 = QLabel('')
        self.label6.setStyleSheet("font:normal 12pt Arial; text-align:center ;background-color: black;color:white")
        self.label6.setAlignment(Qt.AlignLeft)
        self.label6.setWordWrap(True)
        self.minor_vbox.addWidget(self.label6)

        self.label7 = QLabel('')
        self.label7.setStyleSheet("font:normal 12pt Arial; text-align:center ;background-color: black;color:white")
        self.label7.setAlignment(Qt.AlignLeft)
        self.minor_vbox.addWidget(self.label7)
    def combobox(self):
        self.vehicle.message_factory.send_long_command_encode
        self.combobox1 = QComboBox()
        self.combobox1.addItem("Select/Enter COM Port")
        self.combobox1.addItem("/dev/ttyACM1")
        self.combobox1.addItem("/dev/ttyACM0")
        self.combobox1.addItem("/dev/ttyUSB0")
        self.combobox1.addItem("SITL")
        # self.combobox1.setEditable(True)
        # self.combobox1.InsertAtTop
        self.combobox1.activated[str].connect(self.combo_text)

        self.combobox2 = QComboBox()
        self.combobox2.addItem("Select/Enter Baud")
        self.combobox2.addItem("57600")
        self.combobox2.addItem("115200")
        self.combobox2.activated[str].connect(self.combo_text)
        self.connect_vbox.addWidget(self.combobox1)
        self.connect_vbox.addWidget(self.combobox2)
    def combo_text(self):
        self.connection_string = str(self.combobox1.currentText())
        self.baud = str(self.combobox2.currentText())
        print("inside combo", self.connection_string, self.baud)
    def connect(self):
        self.lock.acquire()
        try:
            self.connectButton.setText("Connecting")
            self.connectButton.setDisabled(True)
            self.label2.setText("Connecting on -> Port: " + self.connection_string + ", Baud: " + self.baud)
            if self.connection_string == "SITL":
                import dronekit_sitl
                self.sitl = dronekit_sitl.start_default()
                self.connection_string = self.sitl.connection_string()
                self.vehicle = connect(self.connection_string, wait_ready=True)
                print("connected. Vehicle id =", self.vehicle)
            else:
                if self.connection_string != "Select/Enter COM Port" and self.baud != "Select/Enter Baud":
                    self.connectButton.setText("Connecting")
                    self.vehicle = connect(self.connection_string, wait_ready=True, baud=self.baud)
                    print("connected. Vehicle id =", self.vehicle)
                else:
                    print("select port and baud")
            if self.vehicle:
                self.vehicle.armed = False
                print(self.vehicle.version)
                print(self.vehicle._vehicle_type, self.vehicle.armed, sep='\n')
                self.connectButton.setText("Disconnect")
                self.label3.setText("MavLink Connection is established")
                self.label2.setText("Select Permission Artefact")
                self.connectButton.clicked.disconnect()
                self.connectButton.clicked.connect(self.disconnect_rfm)
        except APIException as e:
            print(e)
        except Exception as e:
            print(e)
            self.connectButton.setText("Connect")
            self.label2.setText("Connection Break {-}")
            self.label3.setText("Error: " + str(e))
            self.connectButton.setStyleSheet("background-color:#F5B7B1")

        finally:
            self.connectButton.setDisabled(False)
            self.downloadLogsButton.setDisabled(False)
            self.combobox1.setCurrentIndex(0)
            self.combobox2.setCurrentIndex(0)
        self.lock.release()
    def connection_th(self):
        print(threading.active_count())
        self.th1 = threading.Thread(target=self.connect, args=(), name='connectionThread', daemon=True)
        self.th1.start()
    def disconnect_rfm(self):
        self.connectButton.clicked.disconnect()
        self.connectButton.setText('Connect')
        self.connectButton.setStyleSheet("background-color:rgb(230, 236, 242)")
        self.connectButton.clicked.connect(self.connection_th)
        self.vehicle.close()
        del self.vehicle
        print("vehicle closed and object deleted")
        self.label2.setText("Disconnected to Vehicle")
    def selectPA(self):
        print("selectPA")
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.filename, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                       "XML Files (*.xml)", options=options)
        if self.filename == None or self.filename == '':
            self.label2.setText("Select valid PA")
        else:
            self.verifyPAButton.setDisabled(False)
            self.label2.setText("Validate PA")
            self.label6.setText(self.filename+" Selected")
    def showDialog(self, msg):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(msg)
        msgBox.setWindowTitle("Message")
        msgBox.setStandardButtons(QMessageBox.Ok)
        returnValue = msgBox.exec()

    def downloadLogs(self):
        self.th2 = threading.Thread(target=self.download_logsThread)
        self.th2.start()
    def download_logsThread(self):
        pass
    def lowerButtons(self):
        selectPAButton = QPushButton("Select PA")
        selectPAButton.clicked.connect(self.selectPA)

        self.verifyPAButton = QPushButton("Verify PA")
        self.verifyPAButton.clicked.connect(self.verifyPA)
        self.verifyPAButton.setDisabled(True)

        self.armDroneButton = QPushButton("Arm Drone")
        self.armDroneButton.clicked.connect(self.armDrone)
        self.armDroneButton.setDisabled(True)

        #sendToRfmButton = QPushButton("Send To RFM")
        #sendToRfmButton.clicked.connect(self.onclick)

        self.downloadLogsButton = QPushButton("Download Logs")
        self.downloadLogsButton.clicked.connect(self.downloadLogs)
        self.downloadLogsButton.setDisabled(True)
        selectPAButton.setStyleSheet("font:bold 10pt Arial;")
        #sendToRfmButton.setStyleSheet("font:bold 10pt Arial;")
        self.downloadLogsButton.setStyleSheet("font:bold 10pt Arial;")

        self.hbox2.addWidget(selectPAButton)
        self.hbox2.addWidget(self.verifyPAButton)
        self.hbox2.addWidget(self.armDroneButton)
        #self.hbox2.addWidget(sendToRfmButton)
        self.hbox2.addWidget(self.downloadLogsButton)


    def verifyPA(self):
        if self.filename == None or self.filename == '':
            self.label2.setText("Select valid PA")
        else:
            verify_pa_thread = threading.Thread(target=self.verifyPaThread, daemon=True)
            verify_pa_thread.start()
    def verifyPaThread(self):
        self.lock.acquire()
        self.label2.setText("Validating...")
        print("inside verifyPaThread")
        import rpi_server
        verification = rpi_server.RPi_server()
        pa, timeCheck, geo_fenceCheck, signatureCheck = verification.receive_pa(self.filename)
        if timeCheck == True:
            print(101)
            self.label4.setText("Time Check Passed")
        else:
            print(102)
            self.label4.setText("Time Check Failed")
        if geo_fenceCheck == True:
            print(103)
            self.label5.setText("Geo-Fence Check Passed")
        else:
            print(104)
            self.label5.setText("Geo-Fence Check Failed")
        if signatureCheck == True:
            print(105)
            self.label6.setText("Signature Verified")
        else:
            print(106)
            self.label6.setText("Signature Check Failed")
        if pa == True:
            self.label2.setText("Permission Artifact is Valid")
            self.armDroneButton.setDisabled(False)
            self.label7.setText("Your Drone is ready to Arm")
        else:
            self.label2.setText("Permission Artifact is not Valid")
            self.label7.setText("Choose a valid PA and try to validate again")
        self.lock.release()
    def armDrone(self):
        pass
if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash_pix = QPixmap("logo250x100.jpg")
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.show()


    def start():
        splash.close()
        global gui
        gui = Window()
        gui.show()


    QTimer.singleShot(5000, start)
    sys.exit(app.exec_())