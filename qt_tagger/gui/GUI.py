import random
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from gui.textcanvas import TextCanvas
import json
current_color = 'green'

class ClickableLabel(QLabel):

    def __init__(self, txt, idx, parent = None):
        QLabel.__init__(self)
        self.idx = idx
        self.content = txt
        self.setText(self.content)
        self.parent = parent
        self.is_selected = False
        self.is_scope = False

    def enterEvent(self, event):
        # print(f'sobre {self.text()}')
        global current_color
        if not self.is_selected:
            self.setStyleSheet(f'background-color: {current_color}')
    
    def leaveEvent(self, event):
        if not self.is_selected:
            self.setStyleSheet('background-color: rgb(255,255,255); color: rgb(51,51,51)')

    def mousePressEvent(self, QMouseEvent):
        global current_color
        if QMouseEvent.button() == Qt.LeftButton:
            if not self.is_selected:
                self.setStyleSheet('background-color:' + current_color + '; color: rgb(51,51,51); text-decoration: underline')
                self.is_selected = True
                self.parent.cue_box.current_cue.add_content(self.content)
                self.parent.cue_box.current_cue.add_positon(self.idx)
                print('Añadido cue', self.parent.cue_box.current_cue.content)
            else:
                if self.is_scope:
                    
                    success = self.parent.cue_box.current_cue.delete_scope(self.idx, self.content)
                    if success != '404':
                        self.is_scope = False

                    print('eliminado scope', self.parent.cue_box.current_cue.scopes)
                else:
                    
                    #eliminar el cue del padre
                    self.parent.cue_box.current_cue.delete_content(self.content)
                    success = self.parent.cue_box.current_cue.delete_position(self.idx)
                    # self.setStyleSheet('background-color: rgb(255,255,255); color: rgb(51,51,51)')
                    print('eliminado cue', self.parent.cue_box.current_cue.content)
                if success != '404':
                    self.is_selected = False
        elif QMouseEvent.button() == Qt.RightButton:
            #añadir scopes al cue actual
            if not self.is_selected:
                self.is_scope = True
                self.setStyleSheet('background-color:' + current_color + '; color: rgb(51,51,51); font-style: italic')
                self.is_selected = True
                self.parent.cue_box.current_cue.add_scope(self.idx, self.content)
                print('añadido scope', self.parent.cue_box.current_cue.scopes)

            

class ClickableCue(QLabel):

    def __init__(self, txt, cue, color, parent = None):
        QLabel.__init__(self)
        self.cue = cue
        self.parent = parent
        self.setText(str(txt))
        self.color = color
        self.setStyleSheet('border: 1px solid black; background-color:' + self.color)

    def enterEvent(self, event):
        self.setStyleSheet('border: 3px solid black; background-color:' + self.color)
        print(f'current cue: {self.parent.get_current_cue_name()}')
    
    def leaveEvent(self, event):
        self.setStyleSheet('border: 1px solid black; background-color:' + self.color)

    def mousePressEvent(self, QMouseEvent):
        global current_color
        if QMouseEvent.button() == Qt.LeftButton:
            current_color = self.color
            self.parent.set_current_cue(self.cue)
        
            


class Cue:

    def __init__(self, color):
        self.content = []
        self.scopes = {'pos': [], 'content': []}
        self.positions = []
        self.ctype = None
        self.color = color

    def set_type(self, ctype):
        self.ctype = ctype

    def add_content(self, content):
        """ string literals that compose the cue"""
        self.content.append(content)

    def delete_content(self, content):
        try:
            self.content.remove(content)
        except:
            "404"

    def add_scope(self, token_pos, token_content):
        """ scope of the words affected by the cue"""
        self.scopes['pos'].append(token_pos)
        self.scopes['content'].append(token_content)

    def delete_scope(self, token_pos, token_content):
        try:
            self.scopes['pos'].remove(token_pos)
            self.scopes['content'].remove(token_content)
        except:
            return "404"

    def add_positon(self, pos):
        """ if the cue is multiword"""
        self.positions.append(pos)

    def delete_position(self, pos):
        try:
            self.positions.remove(pos)
            if len(self.positions) == 0:
                self.scopes['pos'] = []
                self.scopes['content'] = []
        except:
            return "404"

    def get_cue_info(self):
        
        cue = " ".join(self.content)
        if cue != '':
            info = {cue: {}}
            info[cue]['type'] = self.ctype
            info[cue]['position'] = self.positions
            info[cue]['scope'] = self.scopes

            return info
        return {}


class CueTools(QWidget):
    
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.parent = parent

        self.initUI()

        self.cues_count = -1
        self.current_cue = None
        self.current_type = 'negation'
        self.cues = []
        self.add_cue()

    def initUI(self):
        self.layout = QVBoxLayout(self)

        self.cue_box = QGroupBox(self)
        self.vlay = QVBoxLayout()
        self.cue_box_layout = QHBoxLayout()
        self.cue_box.setLayout(self.vlay)
        self.cue_box.setTitle('Cues')

        self.plus_btn = QPushButton('+')
        self.plus_btn.setFixedSize(30,30)
        self.plus_btn.clicked.connect(self.add_cue)

        group = QButtonGroup()
        self.negation_radio = QRadioButton('Negation')
        self.speculation_radio = QRadioButton('Speculation')
        self.negation_radio.setChecked(True)
        group.addButton(self.negation_radio)
        group.addButton(self.speculation_radio)
        self.negation_radio.toggled.connect(self.negaion_toggle)
        self.speculation_radio.toggled.connect(self.speculation_toggle)

        self.vlay.addLayout(self.cue_box_layout)
        self.vlay.addWidget(self.negation_radio)
        self.vlay.addWidget(self.speculation_radio)


        self.cue_box_layout.addWidget(self.plus_btn,0)
        self.layout.addWidget(self.cue_box)

    def negaion_toggle(self):
        if self.negation_radio.isChecked():
            self.current_type = 'negation'
            self.current_cue.set_type('negation')

    def speculation_toggle(self):
        if self.speculation_radio.isChecked():
            self.current_type = 'speculation'
            self.current_cue.set_type('speculation')


    def add_cue(self):
        global current_color
        self.cues_count += 1
        self.cue_box_layout.removeWidget(self.plus_btn)
        color = generate_random_color()
        current_color = color
        new_cue = Cue(color)
        self.current_cue = new_cue
        self.current_cue.set_type(self.current_type)
        self.cues.append(new_cue)
        new_b = self.create_button(new_cue, color)
        self.cue_box_layout.addWidget(new_b,self.cues_count)
        self.cue_box_layout.addWidget(self.plus_btn, self.cues_count+1)

    def create_button(self, cue, color):
        b = ClickableCue(self.cues_count, cue, color, self)
        b.setFixedSize(30,30)
        b.setAlignment(Qt.AlignCenter)
        
        return b

    def get_current_cue_name(self):
        return self.cues.index(self.current_cue)

    def set_current_cue(self, cue):
        self.current_cue = cue



class MainWindow(QWidget):

    updGUI = pyqtSignal()
    stopSIG = pyqtSignal()

    def __init__(self, parent=None):

        QWidget.__init__(self, parent)
        self.updGUI.connect(self.updateGUI)
        self.setStyleSheet('background-color: rgb(255,255,255)')
        # self.setFixedSize(800, 600)

        self.tokens = ['*', 'Te', 'puedes', 'bajar', 'juegos', 'ya', 'que', 'tiene', 'emocion', 'y', 'claro', 'tambien', 'tiene', 'internet', ',', 'no', 'lleva', 'juegos', 'incorporados', 'si', 'quieres', 'juegos', 'te', 'los', 'bajas', 'tu', 'de', 'internet', 'y', 'como', 'no', ',', 'los', 'pagas', ',', 'aun', 'que', 'eso', 'si', 'con', 'este', 'movil', 'yo', 'no', 'me', 'bajaria', 'ningun', 'juego', '(', 'y', 'no', 'porque', 'solo', 'me', 'durara', 'un', 'mes', ')', 'si', 'no', 'porque', 'es', 'un', 'movil', 'muy', 'lento', ',', 'actualice', 'bain', 'training', 'que', 'entraba', 'la', 'demo', 'en', 'el', 'movil', 'y', 'hasta', 'que', 'no', 'esta', 'cargado', 'el', 'dichoso', 'jego', ',', 'hasta', 'que', 'no', 'juegas', 'y', 'jugado', 'y', 'todo', ',', 'es', 'lentisimo', '.']
        self.labels = []
        self.data = {}
        self.prev_sent = -1
        self.current_sent = 0

        self.__setupUI()
    
    def __setupUI(self):

        # Layouts definition
        self.mainLayout = QVBoxLayout()
        self.text_layout = QGridLayout()
        self.tools_layout = QGridLayout()

        self.setStyleSheet("""
        background-color: white;
        QGroupBox {
            font: bold;
            border: 1px solid silver;
            border-radius: 6px;
            margin-top: 6px;
        }

        QGroupBox::title {
            subcontrol-origin: margin;
            left: 7px;
            padding: 0px 5px 0px 5px;
        }""")

        self.btn1 = QPushButton("Dale")
        self.btn1.clicked.connect(self.get_next_sent)

        self.cue_box = CueTools(self)
        status_group = QGroupBox()
        status_group.setTitle('Status')
        status_layout = QVBoxLayout()
        self.status_cue_label = QLabel('Current Cue:')
        self.status_type_label = QLabel('Current type:')
        self.status_scope = QLabel('Scope')
        status_layout.addWidget(self.status_cue_label)
        status_layout.addWidget(self.status_type_label)
        status_layout.addWidget(self.status_scope)
        status_group.setLayout(status_layout)

        json_group = QGroupBox()
        json_group.setTitle('Current cue')
        json_layout = QVBoxLayout()
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setFixedHeight(300)
        json_layout.addWidget(self.text_edit)
        json_group.setLayout(json_layout)

        json_group2 = QGroupBox()
        json_group2.setTitle('All data')
        json_layout2 = QVBoxLayout()
        self.text_edit2 = QTextEdit()
        self.text_edit2.setReadOnly(True)
        self.text_edit2.setFixedHeight(300)
        json_layout2.addWidget(self.text_edit2)
        json_group2.setLayout(json_layout2)


        self.tools_layout.addWidget(self.cue_box,0,0)
        self.tools_layout.addWidget(status_group,0,1)
        self.tools_layout.addWidget(json_group,0,2)
        self.tools_layout.addWidget(json_group2,0,3)
        self.tools_layout.addWidget(self.btn1,1,0)

        self.mainLayout.addLayout(self.text_layout)
        self.mainLayout.addLayout(self.tools_layout)
        self.setLayout(self.mainLayout)

        self.font = QFont('Arial', 18)
       
    def get_next_sent(self):
        self.prev_sent = self.current_sent
        self.current_sent += 1
        
        # get new tokens from text

        # generate labels from the tokens
        clear_layout(self.text_layout)
        # clear_layout(self.cue_box_layout)
        self.labels = []
        for idx, token in enumerate(self.tokens):
            lbl = ClickableLabel(token, idx, self)
            lbl.setFont(self.font)
            lbl.setStyleSheet('color: rgb(51,51,51)')
            lbl.setMouseTracking(True)
            lbl.setAlignment(Qt.AlignCenter)
            self.labels.append(lbl)
    
    def updateGUI(self):

        self.status_cue_label.setText('Current cue: ' + str(self.cue_box.get_current_cue_name()))
        self.status_type_label.setText('Current type: ' + str(self.cue_box.current_type).upper())
        self.status_scope.setText('Scope: ' + str(self.cue_box.current_cue.scopes['pos']))

        if len(self.cue_box.cues) > 0:
            info2 = ""
            for cue in self.cue_box.cues:
                info2 += json.dumps(cue.get_cue_info(), indent=4)

            self.text_edit2.setText(info2)

            info = json.dumps(self.cue_box.current_cue.get_cue_info(), indent=4)
            self.text_edit.setText(info)


        if self.prev_sent != self.current_sent:
            print('painting...')
            self.prev_sent = self.current_sent
            y = -1
            for index, label in enumerate(self.labels):
                x = index % 15
                if x == 0:
                    y += 2
                self.text_layout.addWidget(label,y, x)


def clear_layout(layout):
    for i in reversed(range(layout.count())): 
        layout.itemAt(i).widget().setParent(None)

def count_elements_in(layout):
    print(layout.count())

def generate_random_color():
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)

    r = (r + 255) // 2
    g = (g + 255) // 2
    b = (b + 255) // 2

    return '#%02x%02x%02x' % (r,g,b)


