from PyQt5.QtCore import QPoint, QRect, QSize, Qt, QPointF, QRectF
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QVBoxLayout, QGridLayout, QLabel, QSpinBox,
        QWidget, QPushButton, QSpacerItem, QSizePolicy, QGroupBox, QScrollArea )
from PyQt5.QtGui import (QBrush, QConicalGradient, QLinearGradient, QPainter,
		QPainterPath, QPalette, QPen, QPixmap, QPolygon, QRadialGradient, QColor, 
		QTransform, QPolygonF, QKeySequence, QIcon, QFont)
import math

class TextCanvas(QWidget):
    
    def __init__(self, win_parent, title):
        super(TextCanvas, self).__init__(win_parent)
        self.win_parent = win_parent
        self.pen = QPen()
        self.brush = QBrush()
        self.antialiased = True
    
        self.layout = QVBoxLayout(self)
        self.scrollarea = QScrollArea(self)
        self.scrollarea.setWidgetResizable(True)

        self.group_layout = QGridLayout()
        self.group_layout.setRowStretch(0,0)
        
        self.group = QGroupBox(self)
        self.scrollarea.setWidget(self.group)


        self.tokens_title_label = QLabel("Tokens:")
        self.lemmas_title_label = QLabel("Lemmas:")
        self.tags_title_label = QLabel("Tags:")

        self.tokens_title_label.setStyleSheet("QLabel {font: 12pt Comic Sans MS red; font-weight:600; color:magenta}")
        self.lemmas_title_label.setStyleSheet("QLabel {font: 12pt Comic Sans MS red; font-weight:600; color:red}")
        self.tags_title_label.setStyleSheet("QLabel {font: 12pt Comic Sans MS bold; font-weight:600; color:orange}")

        self.tokens_label = QLabel()
        self.lemmas_label = QLabel()
        self.tags_label = QLabel()
        
        # verticalSpacer = QSpacerItem(0, 500)
        
        self.group_layout.addWidget(self.tokens_title_label,0,0)
        self.group_layout.addWidget(self.tokens_label,1,0)
        self.group_layout.addWidget(self.lemmas_title_label,0,1)
        self.group_layout.addWidget(self.lemmas_label,1,1)
        self.group_layout.addWidget(self.tags_title_label,0,2)
        self.group_layout.addWidget(self.tags_label,1,2)
        # self.group_layout.addItem(verticalSpacer)
        self.group.setLayout(self.group_layout)        
        self.layout.addWidget(self.scrollarea)
    
    def update(self, tokens, lemmas, tags):
        tokens_str = []
        for token in tokens:
            tokens_str.append("'"+token+"'\n")
        self.tokens_label.setText("".join(tokens_str))

        lemmas_str = []
        for lemma in lemmas:
            lemmas_str.append("'"+lemma+"'\n")
        self.lemmas_label.setText("".join(lemmas_str))

        tags_str = []
        for tag in tags:
            tags_str.append("'"+tag+"'\n")
        self.tags_label.setText("".join(tags_str))

