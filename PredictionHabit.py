from keras.preprocessing import image
from PySide6.QtCore import QThread, Signal
from tensorflow import keras
import tensorflow as tf

class PredictionHabit(QThread):
    prediction_status_Signal = Signal(bool)
    prediction_result_Signal = Signal(str, bool)

    def __init__(self, habit_detection_network_path, image_path):
        super(PredictionHabit, self).__init__()
        self.habit_detection_network_Path = habit_detection_network_path
        self.image_path = image_path

    def run(self):
        self.prediction_status_Signal.emit(True)
        self.habit_detection_network = keras.models.load_model(self.habit_detection_network_Path)
        self.image_file = image.load_img(self.image_path, target_size=(224, 224))
        self.image_array = image.img_to_array(self.image_file)
        self.image_array = tf.expand_dims(self.image_array, axis=0)
        self.image_array /= 255.
        self.predictions = self.habit_detection_network.predict(self.image_array)
        if self.predictions[0][0] < 0.5:
            self.result = round((100 - (self.predictions[0][0] * 100)), 2)
            self.type = True
            self.predict = f"% {self.result} İhtimalle İyi Huylu Tümör Mevcut"
        else:
            self.result = round((self.predictions[0][0] * 100), 2)
            self.type = False
            self.predict = f"% {self.result} İhtimalle Kötü Huylu Tümör Mevcut"
        self.prediction_result_Signal.emit(self.predict, self.type)
        self.prediction_status_Signal.emit(False)
        self.quit()
        
        