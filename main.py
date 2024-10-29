import tensorflow as tf
import numpy as np
import cv2

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
    cv2.putText(frame, f"Prediction: {predicted_label}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Waste Sorter", frame)

    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()

