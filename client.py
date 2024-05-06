import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit,QInputDialog
from PyQt6.QtNetwork import QTcpSocket

class Client(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.username, ok = QInputDialog.getText(self, "Username", "Enter your username:")
        if not ok:
            sys.exit(0)
        self.setWindowTitle('Chat Client')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.label = QLabel("Server IP:")
        self.ip_textbox = QLineEdit()
        self.ip_textbox.setText("127.0.0.1")
        self.label2 = QLabel("Message:")
        self.message_textbox = QLineEdit()
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.connect_button = QPushButton("Connect")
        self.send_button = QPushButton("Send")

        layout.addWidget(self.label)
        layout.addWidget(self.ip_textbox)
        layout.addWidget(self.connect_button)
        layout.addWidget(self.chat_history)
        layout.addWidget(self.label2)
        layout.addWidget(self.message_textbox)
        layout.addWidget(self.send_button)

        self.setLayout(layout)

        self.connect_button.clicked.connect(self.connect_to_server)
        self.send_button.clicked.connect(self.send_message)

        self.socket = QTcpSocket()

    def connect_to_server(self):
        server_ip = self.ip_textbox.text()
        try:
            self.socket.connectToHost(server_ip, 12345)

            if self.socket.waitForConnected(1000):
                self.chat_history.append("Connected to server.")
                self.socket.readyRead.connect(self.receive_message)
            else:
                self.chat_history.append("Connection failed.")
        except:
            self.chat_history.append("Connection failed")

    def send_message(self):
        if self.socket.state() == QTcpSocket.SocketState.ConnectedState:
            message = self.message_textbox.text()
            message = f"{self.username}:{message}"
            self.socket.write(message.encode("utf-8"))
            self.message_textbox.clear()

    def receive_message(self):
        message = self.socket.readAll().data().decode("utf-8")
        self.chat_history.append(message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = Client()
    client.show()
    sys.exit(app.exec())
