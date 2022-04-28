from Assets import *
from datetime import datetime
from PredictionTumour import PredictionTumour
from PredictionHabit import PredictionHabit
from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon, Qt, QPixmap, QAction, QCloseEvent
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QStatusBar, QTabWidget, \
    QSizePolicy, QToolBar, QFileDialog, QGroupBox, QTextEdit, QMessageBox


class ControlPanel(QMainWindow):
    def __init__(self):
        super(ControlPanel, self).__init__()

        self.previous_tumour_detection_network_path = default_tumour_detection_network
        self.previous_habit_detection_network_path = default_habit_detection_network
        self.current_tumour_detection_network_path = default_tumour_detection_network
        self.current_habit_detection_network_path = default_habit_detection_network
        self.current_tumour_detection_network_name = path.basename(self.current_tumour_detection_network_path)
        self.current_habit_detection_network_name = path.basename(self.current_habit_detection_network_path)

        self.setWindowTitle(application_name + " - " + application_version)
        self.setWindowIcon(QIcon(application_icon16))
        self.setMinimumSize(1280, 720)

        self.main_Widget = QWidget()
        self.main_Layout = QVBoxLayout()
        self.main_Layout.setAlignment(Qt.AlignCenter)
        self.center_Layout = QHBoxLayout()

        self.status_Icon = QLabel()
        self.status_Pixmap = QPixmap(image_icon16)
        self.status_Icon.setPixmap(self.status_Pixmap)
        self.status_Message = QLabel("Tespiti Gerçekleştirilecek Doku Görüntüsü Bekleniyor...")

        self.statusBar = QStatusBar()
        self.statusBar.setStyleSheet('QStatusBar::item {border: None;}')
        self.statusBar.setSizeGripEnabled(False)
        self.author_Label = QLabel("Designed by " + application_author)
        self.author_Label.setDisabled(True)

        self.statusBar.addWidget(self.status_Icon)
        self.statusBar.addWidget(self.status_Message)
        self.statusBar.addPermanentWidget(self.author_Label)

        self.image_Tab = QTabWidget()
        self.image_SizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.image_Tab.setSizePolicy(self.image_SizePolicy)

        self.image_Widget = QWidget()
        self.image_Layout = QVBoxLayout()
        self.image_Layout.setAlignment(Qt.AlignCenter)
        self.image_Display = QLabel()
        self.image_Display.hide()
        self.image_Display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_Display.setScaledContents(True)
        self.image_Pixmap = QPixmap()
        self.image_Display.setPixmap(self.image_Pixmap.scaled(self.image_Display.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.image_Layout.addWidget(self.image_Display)
        self.image_Hint = QLabel("Doku görüntüsü eklemek için sağ üstte bulunan 'Tespit Gerçekleştirilecek Doku Görüntüsü Ekle' butonuna tıklayınız.")
        self.image_Hint2 = QLabel()
        self.image_Hint2.setAlignment(Qt.AlignCenter)
        self.image_Hint2_Pixmap = QPixmap(add_image_icon48)
        self.image_Hint2.setPixmap(self.image_Hint2_Pixmap)
        self.image_Hint_Layout = QVBoxLayout()
        self.image_Hint_Layout.addWidget(self.image_Hint2)
        self.image_Hint_Layout.addWidget(self.image_Hint)
        self.image_Layout.addLayout(self.image_Hint_Layout)

        self.image_Widget.setLayout(self.image_Layout)

        self.image_ToolBar = QToolBar()
        self.image_add_Action = QAction(QIcon(add_image_icon16), "Tespit Gerçekleştirilecek Doku Görüntüsü Ekle", self)
        self.image_add_Action.triggered.connect(self.add_image)
        self.image_edit_Action = QAction(QIcon(edit_image_icon16), "Tespit Gerçekleştirilecek Doku Görüntüsünü Değiştir", self)
        self.image_edit_Action.triggered.connect(self.edit_image)
        self.image_remove_Action = QAction(QIcon(remove_image_icon16), "Tespit Gerçekleştirilecek Doku Görüntüsünü Kaldır", self)
        self.image_remove_Action.triggered.connect(self.remove_image)
        self.image_ToolBar.addAction(self.image_add_Action)
        self.image_ToolBar.addAction(self.image_edit_Action)
        self.image_ToolBar.addAction(self.image_remove_Action)
        self.image_edit_Action.setVisible(False)
        self.image_remove_Action.setVisible(False)
        self.image_Tab.setCornerWidget(self.image_ToolBar)

        self.image_Tab.addTab(self.image_Widget, QIcon(image_icon16), "Tespit Gerçekleştirilecek Doku Görüntüsü - [Boş]")

        self.tumour_detection_file_GroupBox = QGroupBox(" Tümör Tespiti Gerçekleştirilecek Doku Görüntüsü Dosyası : ")
        self.tumour_detection_file_LineEdit = QLabel("-")
        self.tumour_detection_file_LineEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        #self.tumour_detection_file_LineEdit.setReadOnly(True)
        self.tumour_detection_file_LineEdit.setAlignment(Qt.AlignCenter)
        #self.tumour_detection_file_LineEdit.setMaxLength(255)
        self.tumour_detection_file_Layout = QVBoxLayout()
        self.tumour_detection_file_Layout.addWidget(self.tumour_detection_file_LineEdit)
        self.tumour_detection_file_GroupBox.setLayout(self.tumour_detection_file_Layout)

        self.tumour_network_GroupBox = QGroupBox(" Tümör Tespiti Gerçekleştirecek Sinir Ağı : ")
        self.tumour_network_LineEdit = QLabel("-")
        self.tumour_network_LineEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        #self.tumour_network_LineEdit.setReadOnly(True)
        self.tumour_network_LineEdit.setAlignment(Qt.AlignCenter)
        #self.tumour_network_LineEdit.setMaxLength(255)
        #self.tumour_network_LineEdit.textChanged.connect(self.tumour_detection_network_changed)
        self.tumour_network_Layout = QVBoxLayout()
        self.tumour_network_Layout.addWidget(self.tumour_network_LineEdit)
        self.tumour_network_GroupBox.setLayout(self.tumour_network_Layout)

        self.tumour_result_GroupBox = QGroupBox(" Tümör Tespiti Sonucu : ")
        self.tumour_result_LineEdit = QLabel("-")
        self.tumour_result_LineEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        #self.tumour_result_LineEdit.setReadOnly(True)
        self.tumour_result_LineEdit.setAlignment(Qt.AlignCenter)
        #self.tumour_result_LineEdit.setMaxLength(255)
        self.tumour_result_Layout = QVBoxLayout()
        self.tumour_result_Layout.addWidget(self.tumour_result_LineEdit)
        self.tumour_result_GroupBox.setLayout(self.tumour_result_Layout)

        self.tumour_prediction_Tab = QTabWidget()
        self.tumour_prediction_Tab.setDisabled(True)
        self.tumour_prediction_SizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.tumour_prediction_Tab.setSizePolicy(self.tumour_prediction_SizePolicy)
        self.tumour_Widget = QWidget()
        self.tumour_Layout = QVBoxLayout()
        self.tumour_Layout.setAlignment(Qt.AlignCenter)
        self.tumour_Layout.addWidget(self.tumour_detection_file_GroupBox)
        self.tumour_Layout.addWidget(self.tumour_network_GroupBox)
        self.tumour_Layout.addWidget(self.tumour_result_GroupBox)
        self.tumour_Widget.setLayout(self.tumour_Layout)

        self.tumour_ToolBar = QToolBar()
        self.tumour_change_network_Action = QAction(QIcon(change_network_icon16), "Tümör Tespiti Gerçekleştirecek Sinir Ağını Değiştir", self)
        self.tumour_change_network_Action.triggered.connect(self.change_tumour_detection_network)
        self.tumour_predict_Action = QAction(QIcon(prediction_icon16), "Tümör Tespiti Gerçekleştir", self)
        self.tumour_predict_Action.triggered.connect(self.predict_tumour)
        self.tumour_ToolBar.addAction(self.tumour_change_network_Action)
        self.tumour_ToolBar.addAction(self.tumour_predict_Action)
        self.tumour_prediction_Tab.setCornerWidget(self.tumour_ToolBar)

        self.tumour_prediction_Tab.addTab(self.tumour_Widget, QIcon(detection_icon16), "Doku Görüntüsü Üzerinde Tümör Tespiti")

        self.habit_detection_file_GroupBox = QGroupBox(" Huy Tespiti Gerçekleştirilecek Doku Görüntüsü Dosyası : ")
        self.habit_detection_file_LineEdit = QLabel("-")
        self.tumour_detection_file_LineEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        #self.habit_detection_file_LineEdit.setReadOnly(True)
        self.habit_detection_file_LineEdit.setAlignment(Qt.AlignCenter)
        #self.habit_detection_file_LineEdit.setMaxLength(255)
        self.habit_detection_file_Layout = QVBoxLayout()
        self.habit_detection_file_Layout.addWidget(self.habit_detection_file_LineEdit)
        self.habit_detection_file_GroupBox.setLayout(self.habit_detection_file_Layout)

        self.habit_network_GroupBox = QGroupBox(" Huy Tespiti Gerçekleştirecek Sinir Ağı : ")
        self.habit_network_LineEdit = QLabel("-")
        self.habit_network_LineEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        #self.habit_network_LineEdit.setReadOnly(True)
        self.habit_network_LineEdit.setAlignment(Qt.AlignCenter)
        #self.habit_network_LineEdit.setMaxLength(255)
        #self.habit_network_LineEdit.textChanged.connect(self.habit_detection_network_changed)
        self.habit_network_Layout = QVBoxLayout()
        self.habit_network_Layout.addWidget(self.habit_network_LineEdit)
        self.habit_network_GroupBox.setLayout(self.habit_network_Layout)

        self.habit_result_GroupBox = QGroupBox(" Huy Tespiti Sonucu : ")
        self.habit_result_LineEdit = QLabel("-")
        self.habit_result_LineEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        #self.habit_result_LineEdit.setReadOnly(True)
        self.habit_result_LineEdit.setAlignment(Qt.AlignCenter)
        #self.habit_result_LineEdit.setMaxLength(255)
        self.habit_result_Layout = QVBoxLayout()
        self.habit_result_Layout.addWidget(self.habit_result_LineEdit)
        self.habit_result_GroupBox.setLayout(self.habit_result_Layout)

        self.habit_prediction_Tab = QTabWidget()
        self.habit_prediction_Tab.setDisabled(True)
        self.habit_prediction_SizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.habit_prediction_Tab.setSizePolicy(self.habit_prediction_SizePolicy)
        self.habit_Widget = QWidget()
        self.habit_Layout = QVBoxLayout()
        self.habit_Layout.setAlignment(Qt.AlignCenter)
        self.habit_Layout.addWidget(self.habit_detection_file_GroupBox)
        self.habit_Layout.addWidget(self.habit_network_GroupBox)
        self.habit_Layout.addWidget(self.habit_result_GroupBox)
        self.habit_Widget.setLayout(self.habit_Layout)

        self.habit_ToolBar = QToolBar()
        self.habit_change_network_Action = QAction(QIcon(change_network_icon16), "Huy Tespiti Gerçekleştirecek Sinir Ağını Değiştir", self)
        self.habit_change_network_Action.triggered.connect(self.change_habit_detection_network)
        self.habit_predict_Action = QAction(QIcon(prediction_icon16), "Huy Tespiti Gerçekleştir", self)
        self.habit_predict_Action.triggered.connect(self.predict_habit)
        self.habit_ToolBar.addAction(self.habit_change_network_Action)
        self.habit_ToolBar.addAction(self.habit_predict_Action)
        self.habit_prediction_Tab.setCornerWidget(self.habit_ToolBar)

        self.habit_prediction_Tab.addTab(self.habit_Widget, QIcon(detection_icon16), "Doku Görüntüsü Üzerinde Huy Tespiti")


        self.prediction_results_Tab = QTabWidget()
        self.prediction_results_Widget = QWidget()
        self.prediction_results_TextEdit = QTextEdit()
        self.prediction_results_TextEdit.setLineWrapMode(QTextEdit.NoWrap)
        self.prediction_results_TextEdit.setAlignment(Qt.AlignLeft)
        self.prediction_results_TextEdit.setReadOnly(True)
        self.prediction_results_Layout = QVBoxLayout()
        self.prediction_results_Layout.setAlignment(Qt.AlignTop)
        self.prediction_results_Layout.addWidget(self.prediction_results_TextEdit)
        self.prediction_results_Widget.setLayout(self.prediction_results_Layout)

        self.prediction_results_ToolBar = QToolBar()
        self.save_results_Action = QAction(QIcon(save_results_icon16), "Tespit Sonuçları Geçmişini Kaydet", self)
        self.save_results_Action.triggered.connect(self.save_results)
        self.save_results_Action.setDisabled(True)
        self.clear_results_Action = QAction(QIcon(clear_results_icon16), "Tespit Sonuçları Geçmişini Temizle", self)
        self.clear_results_Action.triggered.connect(self.clear_results)
        self.clear_results_Action.setDisabled(True)
        self.prediction_results_ToolBar.addAction(self.clear_results_Action)
        self.prediction_results_ToolBar.addAction(self.save_results_Action)
        self.prediction_results_Tab.setCornerWidget(self.prediction_results_ToolBar)

        self.prediction_results_Tab.addTab(self.prediction_results_Widget, QIcon(prediction_results_icon16), "Tespit Sonuçları Geçmişi")

        self.prediction_Layout = QVBoxLayout()
        self.prediction_Layout.addWidget(self.tumour_prediction_Tab)
        self.prediction_Layout.addWidget(self.habit_prediction_Tab)
        self.prediction_Layout.addWidget(self.prediction_results_Tab)

        self.center_Layout.addWidget(self.image_Tab)
        self.center_Layout.addLayout(self.prediction_Layout)
        self.center_Layout.setStretch(0, 3)
        self.center_Layout.setStretch(1, 1)
        self.main_Layout.addLayout(self.center_Layout)
        self.main_Layout.addWidget(self.statusBar)
        self.main_Widget.setLayout(self.main_Layout)

        self.setCentralWidget(self.main_Widget)

        self.show()

    def add_image(self):
        self.image_path = QFileDialog.getOpenFileName(parent=self, caption="Tespit Gerçekleştirilecek Doku Görüntüsü Ekle", dir='assets\\example_images', filter="Görüntü Dosyaları (*.png)")
        self.image_path = self.image_path[0]
        self.file_name = path.basename(self.image_path)

        if self.image_path == '':
            self.image_Tab.setTabText(0, "Tespit Gerçekleştirilecek Doku Görüntüsü - [Boş]")
            self.image_Display.hide()
            self.image_add_Action.setVisible(True)
            self.image_edit_Action.setVisible(False)
            self.image_remove_Action.setVisible(False)
            self.tumour_prediction_Tab.setDisabled(True)
            self.habit_prediction_Tab.setDisabled(True)
            self.status_Pixmap = QPixmap(image_icon16)
            self.status_Icon.setPixmap(self.status_Pixmap)
            self.status_Message.setText("Tespit Gerçekleştirilecek Doku Görüntüsü Bekleniyor...")
            self.tumour_detection_file_LineEdit.setText("-")
            self.habit_detection_file_LineEdit.setText("-")
            self.tumour_network_LineEdit.setText("-")
            self.habit_network_LineEdit.setText("-")
            self.tumour_result_LineEdit.setText("-")
            self.habit_result_LineEdit.setText("-")
            self.image_Hint.show()
            self.image_Hint2.show()
        else:
            self.image_Tab.setTabText(0, "Tespit Gerçekleştirilecek Doku Görüntüsü - [" + self.file_name + "]")
            self.image_Hint.hide()
            self.image_Hint2.hide()
            self.image_add_Action.setVisible(False)
            self.image_edit_Action.setVisible(True)
            self.image_remove_Action.setVisible(True)
            self.tumour_prediction_Tab.setEnabled(True)
            self.habit_prediction_Tab.setEnabled(True)
            self.image_Pixmap = QPixmap(self.image_path)
            self.image_Display.setPixmap(self.image_Pixmap.scaled(self.image_Display.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.image_Display.show()
            self.status_Pixmap = QPixmap(detection_icon16)
            self.status_Icon.setPixmap(self.status_Pixmap)
            self.status_Message.setText("Doku Görüntüsü Üzerinde Tespit Gerçekleştirilmesi Bekleniyor...")
            self.tumour_detection_file_LineEdit.setText(self.file_name)
            self.habit_detection_file_LineEdit.setText(self.file_name)
            self.tumour_network_LineEdit.setText(self.current_tumour_detection_network_name)
            self.habit_network_LineEdit.setText(self.current_habit_detection_network_name)
            self.tumour_result_LineEdit.setText("Hesaplanmadı")
            self.habit_result_LineEdit.setText("Hesaplanmadı")
            self.tumour_result_LineEdit.setStyleSheet("color: black;")
            self.habit_result_LineEdit.setStyleSheet("color: black;")

    def edit_image(self):
        self.status_Pixmap = QPixmap(image_icon16)
        self.status_Icon.setPixmap(self.status_Pixmap)
        self.status_Message.setText("Tespit Gerçekleştirilecek Doku Görüntüsü Bekleniyor...")
        self.image_path = QFileDialog.getOpenFileName(parent=self, caption="Tespit Gerçekleştirilecek Doku Görüntüsünü Değiştir",
                                                      dir='assets\\example_images', filter="Görüntü Dosyaları (*.png)")
        self.image_path = self.image_path[0]
        self.file_name = path.basename(self.image_path)

        if self.image_path == '':
            self.image_Tab.setTabText(0, "Tespit Gerçekleştirilecek Doku Görüntüsü - [Boş]")
            self.image_Display.hide()
            self.image_add_Action.setVisible(True)
            self.image_edit_Action.setVisible(False)
            self.image_remove_Action.setVisible(False)
            self.tumour_prediction_Tab.setDisabled(True)
            self.habit_prediction_Tab.setDisabled(True)
            self.status_Pixmap = QPixmap(image_icon16)
            self.status_Icon.setPixmap(self.status_Pixmap)
            self.status_Message.setText("Tespit Gerçekleştirilecek Doku Görüntüsü Bekleniyor...")
            self.tumour_detection_file_LineEdit.setText("-")
            self.habit_detection_file_LineEdit.setText("-")
            self.tumour_network_LineEdit.setText("-")
            self.habit_network_LineEdit.setText("-")
            self.tumour_result_LineEdit.setText("-")
            self.habit_result_LineEdit.setText("-")
            self.image_Hint.show()
            self.image_Hint2.show()
        else:
            self.image_Tab.setTabText(0, "Tespit Gerçekleştirilecek Doku Görüntüsü - [" + self.file_name + "]")
            self.image_Hint.hide()
            self.image_Hint2.hide()
            self.image_add_Action.setVisible(False)
            self.image_edit_Action.setVisible(True)
            self.image_remove_Action.setVisible(True)
            self.tumour_prediction_Tab.setEnabled(True)
            self.habit_prediction_Tab.setEnabled(True)
            self.image_Pixmap = QPixmap(self.image_path)
            self.image_Display.setPixmap(
                self.image_Pixmap.scaled(self.image_Display.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.image_Display.show()
            self.status_Pixmap = QPixmap(detection_icon16)
            self.status_Icon.setPixmap(self.status_Pixmap)
            self.status_Message.setText("Doku Görüntüsü Üzerinde Tespit Gerçekleştirilmesi Bekleniyor...")
            self.tumour_detection_file_LineEdit.setText(self.file_name)
            self.habit_detection_file_LineEdit.setText(self.file_name)
            self.tumour_network_LineEdit.setText(self.current_tumour_detection_network_name)
            self.habit_network_LineEdit.setText(self.current_habit_detection_network_name)
            self.tumour_result_LineEdit.setText("Hesaplanmadı")
            self.habit_result_LineEdit.setText("Hesaplanmadı")
            self.tumour_result_LineEdit.setStyleSheet("color: black;")
            self.habit_result_LineEdit.setStyleSheet("color: black;")

    def remove_image(self):
        self.image_Tab.setTabText(0, "Tespit Gerçekleştirilecek Doku Görüntüsü - [Boş]")
        self.image_Display.hide()
        self.image_add_Action.setVisible(True)
        self.image_edit_Action.setVisible(False)
        self.image_remove_Action.setVisible(False)
        self.tumour_prediction_Tab.setDisabled(True)
        self.habit_prediction_Tab.setDisabled(True)
        self.status_Pixmap = QPixmap(image_icon16)
        self.status_Icon.setPixmap(self.status_Pixmap)
        self.status_Message.setText("Tespit Gerçekleştirilecek Doku Görüntüsü Bekleniyor...")
        self.tumour_detection_file_LineEdit.setText("-")
        self.habit_detection_file_LineEdit.setText("-")
        self.tumour_network_LineEdit.setText("-")
        self.habit_network_LineEdit.setText("-")
        self.tumour_result_LineEdit.setText("-")
        self.habit_result_LineEdit.setText("-")
        self.image_Hint.show()
        self.image_Hint2.show()

    def change_tumour_detection_network(self):
        self.status_Pixmap = QPixmap(change_network_icon16)
        self.status_Icon.setPixmap(self.status_Pixmap)
        self.status_Message.setText("Tümör Tespiti Gerçekleştirecek Sinir Ağı Değişimi Bekleniyor...")
        self.previous_tumour_detection_network_path = self.current_tumour_detection_network_path.replace("\\", "/")
        self.current_tumour_detection_network_path = QFileDialog.getOpenFileName(parent=self, caption="Tümör Tespiti Gerçekleştirecek Sinir Ağını Değiştir", dir='assets\\pretrained_neural_networks\\tumour_detection_network', filter="Sinir Ağı Dosyaları (*.h5)")
        self.current_tumour_detection_network_path = self.current_tumour_detection_network_path[0]
        self.current_tumour_detection_network_name = path.basename(self.current_tumour_detection_network_path)
        if self.current_tumour_detection_network_path == '' and self.tumour_network_LineEdit.text() == path.basename(default_tumour_detection_network):
            pass
        elif self.previous_tumour_detection_network_path != self.current_tumour_detection_network_path:
            self.tumour_result_LineEdit.setText("Hesaplanmadı")
            self.tumour_result_LineEdit.setStyleSheet("color: black;")
        self.status_Pixmap = QPixmap(detection_icon16)
        self.status_Icon.setPixmap(self.status_Pixmap)
        self.status_Message.setText("Doku Görüntüsü Üzerinde Tespit Gerçekleştirilmesi Bekleniyor...")
        if self.current_tumour_detection_network_path == '':
            self.current_tumour_detection_network_path = default_tumour_detection_network
            self.current_tumour_detection_network_name = path.basename(self.current_tumour_detection_network_path)
            self.tumour_network_LineEdit.setText(self.current_tumour_detection_network_name)
        else:
            self.tumour_network_LineEdit.setText(self.current_tumour_detection_network_name)

    def change_habit_detection_network(self):
        self.status_Pixmap = QPixmap(change_network_icon16)
        self.status_Icon.setPixmap(self.status_Pixmap)
        self.status_Message.setText("Huy Tespiti Gerçekleştirecek Sinir Ağı Değişimi Bekleniyor...")
        self.previous_habit_detection_network_path = self.current_habit_detection_network_path.replace("\\", "/")
        self.current_habit_detection_network_path = QFileDialog.getOpenFileName(parent=self, caption="Huy Tespiti Gerçekleştirecek Sinir Ağını Değiştir", dir='assets\\pretrained_neural_networks\\habit_detection_network', filter="Sinir Ağı Dosyaları (*.h5)")
        self.current_habit_detection_network_path = self.current_habit_detection_network_path[0]
        self.current_habit_detection_network_name = path.basename(self.current_habit_detection_network_path)
        if self.current_habit_detection_network_path == '' and self.habit_network_LineEdit.text() == path.basename(default_habit_detection_network):
            pass
        elif self.previous_habit_detection_network_path != self.current_habit_detection_network_path:
            self.habit_result_LineEdit.setText("Hesaplanmadı")
            self.habit_result_LineEdit.setStyleSheet("color: black;")
        self.status_Pixmap = QPixmap(detection_icon16)
        self.status_Icon.setPixmap(self.status_Pixmap)
        self.status_Message.setText("Doku Görüntüsü Üzerinde Tespit Gerçekleştirilmesi Bekleniyor...")
        if self.current_habit_detection_network_path == '':
            self.current_habit_detection_network_path = default_habit_detection_network
            self.current_habit_detection_network_name = path.basename(self.current_habit_detection_network_path)
            self.habit_network_LineEdit.setText(self.current_habit_detection_network_name)
        else:
            self.habit_network_LineEdit.setText(self.current_habit_detection_network_name)

    def predict_tumour(self):
        self.tumour_prediction_Thread = PredictionTumour(self.current_tumour_detection_network_path, self.image_path)
        self.tumour_prediction_Thread.prediction_status_Signal.connect(self.tumour_prediction_status_slot)
        self.tumour_prediction_Thread.prediction_result_Signal.connect(self.tumour_prediction_result_slot)
        self.tumour_prediction_Thread.start()

    def predict_habit(self):
        self.habit_prediction_Thread = PredictionHabit(self.current_habit_detection_network_path, self.image_path)
        self.habit_prediction_Thread.prediction_status_Signal.connect(self.habit_prediction_status_slot)
        self.habit_prediction_Thread.prediction_result_Signal.connect(self.habit_prediction_result_slot)
        self.habit_prediction_Thread.start()

    def clear_results(self):
        self.prediction_results_TextEdit.setText("")
        self.clear_results_Action.setDisabled(True)
        self.save_results_Action.setDisabled(True)

    def save_results(self):
        self.save_results_filename = "prediction_results-" + datetime.now().strftime("[%d.%m.%y-%H.%M.%S]")
        self.save_results_path = QFileDialog.getSaveFileName(self, caption="Tespit Sonuçları Geçmişini Kaydet", dir='assets\\prediction_histories\\' + self.save_results_filename, filter="Metin Belgesi (*.txt)",)
        self.save_results_path = self.save_results_path[0]
        with open(self.save_results_path, 'w', encoding="utf-8") as file:
            file.write(self.prediction_results_TextEdit.toPlainText())
            file.close()
        print(self.save_results_path)

    def closeEvent(self, event: QCloseEvent):
        self.close_MessageBox = QMessageBox()
        self.close_MessageBox.setWindowTitle("Kapat")
        self.close_MessageBox.setWindowIcon(QIcon(application_icon16))
        self.close_MessageBox.setIcon(QMessageBox.Question)
        self.close_MessageBox.setText("ESEC Göğüs Kanseri Tespiti programını kapatmak istediğine emin misin?")
        self.close_MessageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.close_MessageBox_Yes = self.close_MessageBox.button(QMessageBox.Yes)
        self.close_MessageBox_Yes.setText("Evet")
        self.close_MessageBox_No = self.close_MessageBox.button(QMessageBox.No)
        self.close_MessageBox_No.setText("Hayır")
        self.close_MessageBox.setDefaultButton(QMessageBox.No)

        self.close_deny_MessageBox = QMessageBox()
        self.close_deny_MessageBox.setWindowTitle("Kapat")
        self.close_deny_MessageBox.setWindowIcon(QIcon(application_icon16))
        self.close_deny_MessageBox.setIcon(QMessageBox.Critical)
        self.close_deny_MessageBox.setText("Doku görüntüsü üzerinde tespit gerçekleştirilirken program kapatılamaz.")
        self.close_deny_MessageBox.setStandardButtons(QMessageBox.Ok)
        self.close_deny_Ok = self.close_deny_MessageBox.button(QMessageBox.Ok)
        self.close_deny_Ok.setText("Tamam")
        self.close_deny_MessageBox.setDefaultButton(QMessageBox.Ok)

        try:
            if self.prediction_status is True:
                self.close_deny_MessageBox.exec()
                event.ignore()
            else:
                reply = self.close_MessageBox.exec()
                if reply != QMessageBox.Yes:
                    event.ignore()
        except AttributeError:
            reply = self.close_MessageBox.exec()
            if reply != QMessageBox.Yes:
                event.ignore()

    @Slot(bool)
    def tumour_prediction_status_slot(self, status):
        self.prediction_status = status
        if status:
            self.image_edit_Action.setDisabled(True)
            self.image_remove_Action.setDisabled(True)
            self.tumour_change_network_Action.setDisabled(True)
            self.habit_change_network_Action.setDisabled(True)
            self.tumour_predict_Action.setDisabled(True)
            self.habit_predict_Action.setDisabled(True)
            self.tumour_result_LineEdit.setStyleSheet("color: black;")
            self.tumour_result_LineEdit.setText("Hesaplanıyor...")
            self.status_Pixmap = QPixmap(prediction_icon16)
            self.status_Icon.setPixmap(self.status_Pixmap)
            self.status_Message.setText("Doku Görüntüsü Üzerinde Tümör Tespiti Gerçekleştiriliyor...")
        else:
            self.image_edit_Action.setEnabled(True)
            self.image_remove_Action.setEnabled(True)
            self.tumour_change_network_Action.setEnabled(True)
            self.habit_change_network_Action.setEnabled(True)
            self.tumour_predict_Action.setEnabled(True)
            self.habit_predict_Action.setEnabled(True)
            self.status_Pixmap = QPixmap(detection_icon16)
            self.status_Icon.setPixmap(self.status_Pixmap)
            self.status_Message.setText("Doku Görüntüsü Üzerinde Tespit Gerçekleştirilmesi Bekleniyor...")


    @Slot(str)
    def tumour_prediction_result_slot(self, result, result_type):
        if result_type:
            self.tumour_result_LineEdit.setStyleSheet("color: green;")
        else:
            self.tumour_result_LineEdit.setStyleSheet("color: red;")
        self.tumour_result_LineEdit.setText(result)
        self.prediction_results_TextEdit.append("• " + datetime.now().strftime("[%d.%m.%y - %H:%M:%S]") + " → " + self.file_name + " → " + result)
        self.clear_results_Action.setEnabled(True)
        self.save_results_Action.setEnabled(True)

    @Slot(bool)
    def habit_prediction_status_slot(self, status):
        self.prediction_status = status
        if status:
            self.image_edit_Action.setDisabled(True)
            self.image_remove_Action.setDisabled(True)
            self.tumour_change_network_Action.setDisabled(True)
            self.habit_change_network_Action.setDisabled(True)
            self.tumour_predict_Action.setDisabled(True)
            self.habit_predict_Action.setDisabled(True)
            self.habit_result_LineEdit.setStyleSheet("color: black;")
            self.habit_result_LineEdit.setText("Hesaplanıyor...")
            self.status_Pixmap = QPixmap(prediction_icon16)
            self.status_Icon.setPixmap(self.status_Pixmap)
            self.status_Message.setText("Doku Görüntüsü Üzerinde Huy Tespiti Gerçekleştiriliyor...")
        else:
            self.image_edit_Action.setEnabled(True)
            self.image_remove_Action.setEnabled(True)
            self.tumour_change_network_Action.setEnabled(True)
            self.habit_change_network_Action.setEnabled(True)
            self.tumour_predict_Action.setEnabled(True)
            self.habit_predict_Action.setEnabled(True)
            self.status_Pixmap = QPixmap(detection_icon16)
            self.status_Icon.setPixmap(self.status_Pixmap)
            self.status_Message.setText("Doku Görüntüsü Üzerinde Tespit Gerçekleştirilmesi Bekleniyor...")

    @Slot(str)
    def habit_prediction_result_slot(self, result, result_type):
        if result_type:
            self.habit_result_LineEdit.setStyleSheet("color: green;")
        else:
            self.habit_result_LineEdit.setStyleSheet("color: red;")
        self.habit_result_LineEdit.setText(result)
        self.prediction_results_TextEdit.append("• " + datetime.now().strftime("[%d.%m.%y - %H:%M:%S]") + " → " + self.file_name + " → " + result)
        self.clear_results_Action.setEnabled(True)
        self.save_results_Action.setEnabled(True)