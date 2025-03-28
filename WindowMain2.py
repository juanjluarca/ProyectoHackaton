from PyQt6 import QtCore, QtGui, QtWidgets
import tensorflow as tf
import numpy as np
import cv2

class Ui_Hackaton(object):
    def setupUi(self, Hackaton):
        Hackaton.setObjectName("Hackaton")
        Hackaton.resize(1250, 780)
        self.horizontalLayoutWidget = QtWidgets.QWidget(parent=Hackaton)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 2, 2))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ObjectMixto = QtWidgets.QLabel(parent=Hackaton)
        self.ObjectMixto.setGeometry(QtCore.QRect(130, 640, 101, 101))
        self.ObjectMixto.setStyleSheet("background-color: rgb(121, 121, 121);")
        self.ObjectMixto.setText("")
        self.ObjectMixto.setObjectName("ObjectMixto")
        self.ObjectPaper = QtWidgets.QLabel(parent=Hackaton)
        self.ObjectPaper.setGeometry(QtCore.QRect(720, 640, 101, 101))
        self.ObjectPaper.setStyleSheet("background-color: rgb(121, 121, 121);")
        self.ObjectPaper.setText("")
        self.ObjectPaper.setObjectName("ObjectPaper")
        self.ObjectOrganic = QtWidgets.QLabel(parent=Hackaton)
        self.ObjectOrganic.setGeometry(QtCore.QRect(430, 640, 101, 101))
        self.ObjectOrganic.setStyleSheet("background-color: rgb(121, 121, 121);")
        self.ObjectOrganic.setText("")
        self.ObjectOrganic.setObjectName("ObjectOrganic")
        self.ObjertBottle = QtWidgets.QLabel(parent=Hackaton)
        self.ObjertBottle.setGeometry(QtCore.QRect(1020, 640, 101, 101))
        self.ObjertBottle.setStyleSheet("background-color: rgb(121, 121, 121);")
        self.ObjertBottle.setText("")
        self.ObjertBottle.setObjectName("ObjertBottle")
        self.label = QtWidgets.QLabel(parent=Hackaton)
        self.label.setGeometry(QtCore.QRect(0, 0, 1250, 780))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../../Downloads/Green Illustrated Activity on Recycling Flashcards for Speech Therapy.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label.raise_()
        self.horizontalLayoutWidget.raise_()
        self.ObjectMixto.raise_()
        self.ObjectPaper.raise_()
        self.ObjectOrganic.raise_()
        self.ObjertBottle.raise_()

        self.retranslateUi(Hackaton)
        QtCore.QMetaObject.connectSlotsByName(Hackaton)

    def retranslateUi(self, Hackaton):
        _translate = QtCore.QCoreApplication.translate
        Hackaton.setWindowTitle(_translate("Hackaton", "Form"))
        # Hackaton.setWindowTitle(_translate("Form", "Form"))
        # self.label_2.setText(_translate("Form", "Deteccion y clasificación de desechos "))
        # self.label_5.setText(_translate("Form", "Mixto"))
        # self.label_6.setText(_translate("Form", "Orgánico"))
        # self.label_8.setText(_translate("Form", "Botellas"))
        # self.label_7.setToolTip(_translate("Form","<html><head/><body><p align=\"center\">Papel y </p><p align=\"center\">Carton</p><p align=\"center\"><br/></p></body></html>"))
        # self.label_7.setWhatsThis(_translate("Form", "<html><head/><body><p>Papel </p><p>y carton </p><p><br/></p></body></html>"))
        # self.label_7.setText(_translate("Form", "Papel y"))
        # self.label_9.setToolTip(_translate("Form","<html><head/><body><p align=\"center\">Papel y </p><p align=\"center\">Carton</p><p align=\"center\"><br/></p></body></html>"))
        # self.label_9.setWhatsThis(_translate("Form", "<html><head/><body><p>Papel </p><p>y carton </p><p><br/></p></body></html>"))
        # self.label_9.setText(_translate("Form", "Carton"))

    def encender_led(self, tipo_desecho):
        # Apagar todos los bloques al iniciar
        self.ObjectMixto.setStyleSheet("background-color: gray;")
        self.ObjectOrganic.setStyleSheet("background-color: gray;")
        self.ObjectPaper.setStyleSheet("background-color: gray;")
        self.ObjertBottle.setStyleSheet("background-color: gray;")

        # Encender el bloque correspondiente
        if tipo_desecho == "1 Mixto":
            self.ObjectMixto.setStyleSheet("background-color: red;")
        elif tipo_desecho == "0 Organico":
            self.ObjectOrganic.setStyleSheet("background-color: red;")
        elif tipo_desecho == "2 Papel y carton":
            self.ObjectPaper.setStyleSheet("background-color: red;")
        elif tipo_desecho == "3 Botellas":
            self.ObjertBottle.setStyleSheet("background-color: red;")
        elif tipo_desecho == "4 Fondo":
            pass

    def loadCamera(self):
        # 2 Papel y carton
        # 1 Mixto
        # 0 Organico
        # 3 Botellas
        # 4 Fondo
        # Se carga el modelo y se leen las etiquetas
        model = tf.keras.models.load_model("model/modelo.h5")
        with open("model/labels.txt", "r") as f:
            labels = [line.strip() for line in f.readlines()]

            # Se inicia la cámara
            cap = cv2.VideoCapture(0)  # '0' Se selecciona la cámara principal

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # Preprocesar el fotograma para el modelo
                img = cv2.resize(frame, (224, 224))  # Ajustar tamaño según tu modelo
                img = np.expand_dims(img, axis=0)  # Añadir dimensión para el batch
                img = img / 255.0  # Normalización

                # Predicción
                predictions = model.predict(img)
                predicted_label = labels[np.argmax(predictions)]

                # Mostrar el resultado en el video en vivo
                cv2.putText(frame, f"Tipo: {predicted_label}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow("Waste Sorter", frame)
                self.encender_led(predicted_label)

                # Salir con la tecla 'q'
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

            # Liberar recursos
            cap.release()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Hackaton = QtWidgets.QWidget()
    ui = Ui_Hackaton()
    ui.setupUi(Hackaton)
    Hackaton.show()
    ui.loadCamera()
    sys.exit(app.exec())
