import sys
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QSplashScreen, QComboBox, QApplication, QLabel,QWidget,QFileDialog, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout
class Window(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        self.setGeometry(450, 0, 350, 500)
        self.setWindowTitle("Permission Validator")
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
        self.connectButton = QPushButton("Connect")
        self.connectButton.setFixedHeight(100)
        self.hbox1.addWidget(self.connectButton)
        self.connectButton.clicked.connect(self.connect)
        self.label1()
        self.label2()
        self.vbox.addLayout(self.hbox2)
        self.lowerButtons()
    def combobox(self):
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
    def connect(self):
        import dronekit_sitl
        self.sitl = dronekit_sitl.start_default()
        connection_string = self.sitl.connection_string()
        print('Connecting to vehicle on: %s' % connection_string)
        self.vehicle = connect("tcp:127.0.0.1:5760", wait_ready=True)
    def selectPA(self):
        print("selectPA")
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "Python Files (*.py)", options=options)
        print(filename)
    def sendToRfm(self):
        print("send to RFM")
    def downloadLogs(self):
        print("download Logs")
    def label1(self):
        label = QLabel("Hello World")
        label.setStyleSheet("font:normal 12pt Comic Sans MS;text-align: top;background-color: black;color:white")
        self.vbox.addWidget(label)
    def label2(self):
        label = QLabel("Hello World")
        label.setStyleSheet("font:bold 15pt Comic Sans MS; background-color: black;color:white ")
        label.setFixedHeight(50)
        self.vbox.addWidget(label)
    def lowerButtons(self):

        selectPAButton = QPushButton("SelectPA")
        selectPAButton.clicked.connect(self.selectPA)
        sendToRfmButton = QPushButton("Send To Rfm")
        sendToRfmButton.clicked.connect(self.sendToRfm)
        downloadLogsButton = QPushButton("Download Logs")
        downloadLogsButton.clicked.connect(self.downloadLogs)
        self.hbox2.addWidget(selectPAButton)
        self.hbox2.addWidget(sendToRfmButton)
        self.hbox2.addWidget(downloadLogsButton)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash_pix = QPixmap("logo.png")
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.show()
    def start():
        splash.close()
        global gui
        gui = Window()
        gui.show()
    QTimer.singleShot(5000, start)
    sys.exit(app.exec_())