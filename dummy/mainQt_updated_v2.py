import sys
import os
import socket
import threading
import datetime
import time
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QIcon, QTextCursor, QIntValidator, QRegExpValidator
from PyQt5.QtCore import Qt, QTimer, QRegExp
from PyQt5.QtWidgets import QSplashScreen, QMessageBox, QApplication, QLabel, QWidget, QFileDialog, QMainWindow, \
    QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QTextEdit, QLineEdit


class Window(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
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
        self.lock = threading.Lock()
        self.setGeometry(450, 50, 400, 500)
        self.setWindowTitle("NPNT CLIENT")
        #self.setWindowIcon(QIcon("icon.png"))
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
        # h_label.setFixedSize(250,100)
        h_label.setPixmap(pix)
        h_label.show()
        self.hbox1.addWidget(h_label)

        self.connect_vbox = QVBoxLayout()
        self.lineEdit = QLineEdit()
        self.lineEdit.setPlaceholderText("192.168.168.168")
        my_regex = QRegExp("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
        my_validator = QRegExpValidator(my_regex, self.lineEdit)
        self.lineEdit.setValidator(my_validator)
        self.connect_vbox.addWidget(self.lineEdit)
        self.con = 'Connect'
        self.connectButton = QPushButton(self.con)
        self.connectButton.setFixedHeight(60)
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
        self.msg1 = "Connect with RFM"
        self.label2 = QLabel(self.msg1)
        self.label2.setStyleSheet("font:bold 15pt Arial; background-color: black;color:white")
        self.label2.setFixedHeight(50)
        self.vbox.addWidget(self.label2)
        # self.label1()
        # self.label2()
        self.vbox.addLayout(self.hbox2)
        self.lowerButtons()

    def connect(self):
        self.lock.acquire()
        if self.lineEdit.text():
            print("connection string received")
            self.connection_string = self.lineEdit.text()
        else:
            print("No string Received")
            self.label2.setText("Enter I P")
            return
        print(self.connection_string)
        try:
            self.lineEdit.setReadOnly(True)
            self.label2.setText("Connecting on " + self.connection_string)
            self.sock1 = socket.socket()
            host = self.connection_string
            port = 1499
            self.connectButton.setText("Connecting")
            self.sock1.connect((host, port))
            self.sock1.send(b'Connected')
            self.connectButton.setText('Disconnect')
            self.connectButton.setStyleSheet("background-color:lightgreen")
            self.label2.setText("Select Permission Artefact")
            self.connectButton.clicked.disconnect()
            self.connectButton.clicked.connect(self.disconnect_rfm)

        except:
            self.label2.setText("Connection Break {-}")
            self.lineEdit.setReadOnly(False)
            self.connectButton.setText("Connect")
            self.lineEdit.clear()
            self.lineEdit.setPlaceholderText("192.168.168.168")
            self.connectButton.setStyleSheet("background-color:#F5B7B1")
        self.lock.release()
    def connection_th(self):
        self.lineEdit.setReadOnly(False)
        if self.connectButton.text() == "Connecting":
            self.connectButton.setText("Connect")
            self.lineEdit.clear()
            self.label2.setText("Enter I P")
            return
        try:
            print(threading.active_count())
            self.sock1.shutdown(socket.SHUT_RDWR)
        except Exception as e:
            print(e)
        try:
            self.sock1.close()
            print("try")
        except Exception as e:
            print(e)
        self.th1 = threading.Thread(target=self.connect, args=(), name='connectionThread', daemon= True)
        self.th1.start()
    def disconnect_rfm(self):
        self.connectButton.clicked.disconnect()
        self.sock1.send(b'Disc')
        self.connectButton.setText('Connect')
        self.connectButton.setStyleSheet("background-color:rgb(230, 236, 242)")
        self.connectButton.clicked.connect(self.connection_th)
        self.sock1.close()
        self.clear_all()
    def clear_all(self):
        try:
            self.label7.clear()
            self.label6.clear()
            self.label3.clear()
            
            self.label5.clear()
            self.label4.clear()
        except:
            print('clear')
        try:
            del self.label7
            del self.label3
            del self.label4
            del self.label5
            del self.label6
            
        except:
            print('del')
        try:
            del self.create_label1
            del self.create_label2
            del self.create_label3
            del self.create_label4
            del self.create_label5
        except:
            print('create')
    def selectPA(self):
        print("selectPA")
        
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.filename, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                       "XML Files (*.xml)", options=options)
        if self.filename == None or self.filename == '':
            self.label2.setText("Select valid PA")
        else:
            self.label2.setText("Send PA to RFM")
        self.clear_all()
    def showDialog(self, msg):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(msg)
        msgBox.setWindowTitle("Message")
        msgBox.setStandardButtons(QMessageBox.Ok)
        returnValue = msgBox.exec()
    def send_to_rpa(self):
        self.clear_all()
        print("send to RFM")
        msg = 'NPNT'
        msg = msg.encode('utf-8')
        self.sock1.send(msg)
        i=1
        send_file = self.filename
        f = open(send_file, "rb")
        while f:
            read_file = f.read(1024)
            self.sock1.send(read_file)
            print(read_file)
            if read_file == b'':
                time.sleep(2)
                self.sock1.send(b'END')
                print('send it')
                break
        msg = 'Successfully Send'
        self.label2.setText("Checking PA...")
        self.showDialog(msg)

        while True:
            var = self.sock1.recv(5)
            if var == b'timec':
                self.create_label1("Time Check Pass")
            if var == b'Geofc':
                self.create_label2("Geofence Check Pass")
            if var == b"GPSPF" or var == b'Geofn':
                self.create_label5('Waiting for GPS LOCK...')
            if var == b'SpuPA':
                self.create_label3("Spurious Permission Artefact Check Pass")
            if var == b'Valid':
                self.create_label4("Permission Artefact is Valid")
                self.label2.setText("Ready to Arm")
                break
            if var == b'timef':
                self.create_label1("Time Check Fail")
            if var == b'Geoff':
                self.create_label2("Geofence Check Pass Fail")
            if var == b'SpuPf':
                self.create_label3("Spurious Permission Artefact Check Fail")
            if var == b'faill':
                self.create_label4("Permission Artefact is not Valid")
                self.label2.setText("Send Valid PA")
                break

    

    def onclick(self):
        check_st=self.connectButton.text()
        print(check_st)
        if self.filename == None or self.filename == '':
            self.label2.setText("Select valid PA")
        elif check_st=='Connect':
            self.label2.setText("First Connect with RFM")
        else:
            self.send_to_rpa()

    def lal_set(self):
        self.th2 = threading.Thread(target=self.downloadLogs)
        self.th2.start()

    def downloadLogs(self):
        try:
            user = os.environ['USERNAME']
            datei = datetime.datetime.now()
            filename = 'C:/Users/{}/Desktop/J_NPNT/LOG_FILES/Date_{}-{}-{}/{}_{}.json'.format(user, datei.day,
                                                                                              datei.month, datei.year,
                                                                                              datei.hour, datei.minute)
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            msgg = "down"
            ms = msgg.encode('utf-8')
            self.sock1.send(ms)
            self.label2.setText("Downloading...")
            f = open(
                'C:/Users/{}/Desktop/J_NPNT/LOG_FILES/Date_{}-{}-{}/{}_{}.json'.format(user, datei.day, datei.month,
                                                                                       datei.year, datei.hour,
                                                                                       datei.minute), 'wb')
            while True:
                l = self.sock1.recv(1024)
                if l != b'END':
                    f.write(l)
                if l == b'END':
                    print('empty')
                    break
            f.close()
            print('file Closed')
            self.label2.setText("Download Complete")
        except:
            self.label2.setText(">>First Connect with RFM")

    # def label1(self):
    # label = QLabel('Connected')
    # label.setStyleSheet("font:normal 12pt Comic Sans MS;text-align: top;background-color: black;color:white")
    # self.vbox.addWidget(label)
    # def label2(self,msg='Connect Your Vehicle'):
    # label = QLabel(msg)
    # label.setStyleSheet("font:bold 15pt Comic Sans MS; background-color: black;color:white ")
    # label.setFixedHeight(50)
    # self.vbox.addWidget(label)
    def lowerButtons(self):

        self.selectPAButton = QPushButton("SelectPA")
        self.selectPAButton.clicked.connect(self.selectPA)
        sendToRfmButton = QPushButton("Send To RFM")
        sendToRfmButton.clicked.connect(self.onclick)
        downloadLogsButton = QPushButton("Download Logs")
        downloadLogsButton.clicked.connect(self.lal_set)
        self.selectPAButton.setStyleSheet("font:bold 10pt Arial;")
        sendToRfmButton.setStyleSheet("font:bold 10pt Arial;")
        downloadLogsButton.setStyleSheet("font:bold 10pt Arial;")
        self.hbox2.addWidget(self.selectPAButton)
        self.hbox2.addWidget(sendToRfmButton)
        self.hbox2.addWidget(downloadLogsButton)

    def create_label1(self, head):
        self.label3 = QLabel(head)
        self.label3.setStyleSheet("font:bold 8pt Arial;color:white;background-color: black;padding:0px ")
        self.minor_vbox.addWidget(self.label3)
        self.label3.setAlignment(Qt.AlignLeft)

    def create_label2(self, head):
        self.label4 = QLabel(head)
        self.label4.setStyleSheet("font:bold 8pt Arial;color:white;background-color: black;padding:0px ")
        self.minor_vbox.addWidget(self.label4)
        self.label4.setAlignment(Qt.AlignLeft)

    def create_label3(self, head):
        self.label6 = QLabel(head)
        self.label6.setStyleSheet("font:bold 8pt Arial;color:white;background-color: black;padding:0px ")
        self.minor_vbox.addWidget(self.label6)
        self.label6.setAlignment(Qt.AlignLeft)

    def create_label4(self, head):
        self.label5 = QLabel(head)
        self.label5.setStyleSheet("font:bold 8pt Arial;color:white;background-color: black;padding:0px ")
        self.minor_vbox.addWidget(self.label5)
        self.label5.setAlignment(Qt.AlignLeft)

    def create_label5(self, head):
        self.label7 = QLabel(head)
        self.label7.setStyleSheet("font:bold 8pt Arial;color:white;background-color: black;padding:0px ")
        self.minor_vbox.addWidget(self.label7)
        self.label7.setAlignment(Qt.AlignLeft)


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
