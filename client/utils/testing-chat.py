import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class ChatWindow(QWidget):

    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle('Game Chat')
        self.setGeometry(100, 100, 400, 500)

        # Create chat log display
        self.chat_log = QTextEdit(self)
        self.chat_log.setReadOnly(True)
        self.chat_log.setGeometry(10, 10, 380, 350)

        # Create input box
        self.input_box = QLineEdit(self)
        self.input_box.setGeometry(10, 370, 300, 30)
        self.input_box.returnPressed.connect(self.send_message)

        # Create send button
        self.send_button = QPushButton('Send', self)
        self.send_button.setGeometry(320, 370, 70, 30)
        self.send_button.clicked.connect(self.send_message)

    def send_message(self):
        message = self.input_box.text()
        if message:
            # Add message to chat log
            self.chat_log.append('You: {}'.format(message))

            # Clear input box
            self.input_box.clear()

            # Send message to other player
            # Example code: send_message_to_other_player(message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec_())
