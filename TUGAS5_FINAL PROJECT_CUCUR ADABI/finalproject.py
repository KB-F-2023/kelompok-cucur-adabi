import cv2
import numpy as np

# Load model dan konfigurasi YOLO
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Mendapatkan layer output
layer_names = net.getLayerNames()
output_layers = [layer_names[i- 1] for i in net.getUnconnectedOutLayers()]

# Mendefinisikan fungsi untuk mendeteksi objek
def detect_objects(image):
    height, width, channels = image.shape

    # Membuat blob dari gambar
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    # Melakukan deteksi menggunakan YOLO
    net.setInput(blob)
    outs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []
    object_info = []

    # Mengolah hasil deteksi
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5:
                # Mendapatkan informasi objek yang terdeteksi
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Menghitung titik-titik sudut kotak pembatas objek
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                # Menyimpan informasi objek
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    # Melakukan non-maximum suppression untuk menghilangkan deteksi yang tumpang tindih
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            # confidence = confidences[i]

            # Menggambar kotak pembatas dan label pada gambar
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Menghitung tinggi dan lebar objek
            obj_height = h
            obj_width = w

            # Menyimpan informasi objek
            object_info.append({
                'nama': label,
                'tinggi': obj_height,
                'lebar': obj_width
            })

    return image, object_info

# Memulai video capture
cap = cv2.VideoCapture('in.avi')

while True:
    # Membaca frame dari video
    ret, frame = cap.read()

    if not ret:
        break

    # Mendeteksi objek dalam frame
    result_frame, object_info = detect_objects(frame)

    # Menampilkan frame hasil deteksi
    cv2.imshow("Deteksi Objek", result_frame)

    # Menampilkan informasi objek
    for info in object_info:
        print("Nama: {}, Tinggi: {}, Lebar: {}".format(
            info['nama'], info['tinggi'], info['lebar']))

    # Keluar dari program jika tombol 'q' ditekan
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Membersihkan dan menutup jendela
cap.release()
cv2.destroyAllWindows()
