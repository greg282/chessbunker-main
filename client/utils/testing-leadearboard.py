import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem,QVBoxLayout,QHeaderView,QAbstractItemView,QComboBox,QHBoxLayout,QLineEdit,QPushButton
from PyQt5.QtGui import QFont
import requests
import json
from PyQt5.QtCore import Qt
class Leaderboard(QWidget):
    def __init__(self, data):
        super().__init__()
        

        # Set font
      
        
        # Parse JSON data
        self.ranking = json.loads(data)['ranking']
        
        # Sort ranking by elo in descending order
        self.ranking.sort(key=lambda x: x['elo'], reverse=True)
        
        # Create table widget
        self.table = QTableWidget()
       

        self.table.setStyleSheet("QTableWidget::item  {margin: 10px; font-size: 12px}")
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Rank', 'Username', 'Elo', 'Wins/Losses'])
        self.table.setRowCount(len(self.ranking))

        #add combo box
        self.row_count_selector = QComboBox()
        self.row_count_selector.addItems(['All', '10', '20', '30', '40', '50'])
        self.row_count_selector.setCurrentIndex(0)
        self.row_count_selector.currentIndexChanged.connect(self.update_table)

        font = QFont('Arial', 20)
        self.table.setFont(font)  # set the font here
        # Populate table with data
        for i, player in enumerate(self.ranking):
            rank_item = QTableWidgetItem(str(i+1))
            username_item = QTableWidgetItem(player['username'])
            elo_item = QTableWidgetItem(str(player['elo']))
            wl_item = QTableWidgetItem('{}/{}'.format(player['games_won'], player['games_lost']))
            self.table.setItem(i, 0, rank_item)
            self.table.setItem(i, 1, username_item)
            self.table.setItem(i, 2, elo_item)
            self.table.setItem(i, 3, wl_item)
            
        # Set table dimensions
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for i in range(self.table.columnCount()):
            self.table.setColumnWidth(i, int(self.table.width() / self.table.columnCount()))
        self.table.resizeRowsToContents()
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers) # make table read-only

        ##
        self.search_bar = QLineEdit()
        self.search_button = QPushButton('Search')
        self.search_button.clicked.connect(self.search_username)
        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_bar)
        search_layout.addWidget(self.search_button)

        # Add table to widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.row_count_selector)
        self.layout.addLayout(search_layout)
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)
        self.table.setStyleSheet('''
            QTableWidget {
                background-color: #1c1c1c;
                border: 1px solid black;
            }
            QHeaderView::section {
                background-color: black;
                border: 1px solid black;
                padding: 4px;
                font-size: 24px;
                font-weight: bold;
            }
            QTableWidget::item {
                border: 1px solid #424141;
                padding: 4px;
                font-size: 12px;
                color: white;
            }
            QComboBox {
                font-size: 12px;
            }
        ''')
        self.show()
        
    def update_table(self):
        row_count = self.row_count_selector.currentText()
        if row_count == 'All':
            row_count = len(self.ranking)
        else:
            row_count = int(row_count)

        self.table.setRowCount(row_count)

        for i, player in enumerate(self.ranking[:row_count]):
            rank_item = QTableWidgetItem(str(i+1))
            username_item = QTableWidgetItem(player['username'])
            elo_item = QTableWidgetItem(str(player['elo']))
            wl_item = QTableWidgetItem('{}/{}'.format(player['games_won'], player['games_lost']))
            self.table.setItem(i, 0, rank_item)
            self.table.setItem(i, 1, username_item)
            self.table.setItem(i, 2, elo_item)
            self.table.setItem(i, 3, wl_item)
        self.table.resizeRowsToContents()

    def search_username(self):
        search_term = self.search_bar.text()
        for i in range(self.table.rowCount()):
            item = self.table.item(i, 1)
            if not item.text().startswith(search_term):
                self.table.setRowHidden(i, True)
            else:
                self.table.setRowHidden(i, False)


def getData():
    s = requests.Session()

    res = s.post('http://localhost:8000/api/player/ranking/', data=json.dumps({
        "limit": 50,
        "skip": 0
    }))
    return res.text

def run_leaderboard():
    app = QApplication(sys.argv)

    leaderboard = Leaderboard(getData())
    sys.exit(app.exec_())

