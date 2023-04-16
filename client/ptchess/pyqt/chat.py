import json
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QTextEdit, QLineEdit, QPushButton, QLabel,QWidget

class ChatWindow(QMainWindow):

    def __init__(self,username,ws):
        super().__init__()
        self.username=username
        # Initialize UI elements
        self.chat_history = QTextEdit()
        self.chat_input = QLineEdit()
        self.player1_label = QLabel(username)
        self.send_button = QPushButton("Send")
        self.ws=ws
        # Set window properties
        self.setWindowTitle("Chat App")
        self.setFixedSize(500, 400)
        self.chat_history.setReadOnly(True)
        # Set layout
        layout = QGridLayout()
        layout.addWidget(self.chat_history, 0, 0, 1, 4)
        layout.addWidget(self.player1_label, 1, 0)
        layout.addWidget(self.chat_input, 2, 0, 1, 3)
        layout.addWidget(self.send_button, 2, 3)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Connect button press to send message
        self.send_button.clicked.connect(self.send_message_user)

    def send_message_user(self):
        message = self.chat_input.text()
        if message:
            # Display message in chat history
            self.chat_history.append(f"{self.username}: {message}\n")
            self.ws.send(json.dumps({
            "type": "event",
            "message": "chat@"+message+"@"+self.username
        }))
            self.chat_input.clear()


    
    def send_message_oponent(self,msg,username):
        message = msg
        if message:
            self.chat_history.append(f"{username}: {message}\n")
            self.chat_input.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ChatWindow("RUDY","KOSZYKARZ")
    window.show()
    window.send_message_oponent("Cześć")
    sys.exit(app.exec_())