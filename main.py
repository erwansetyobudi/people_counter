import cv2
import imutils
from centroidtracker import CentroidTracker
import datetime

cap = cv2.VideoCapture(0)
ct = CentroidTracker()
track = {}
masuk, keluar = 0, 0
garis_y = 250

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = imutils.resize(frame, width=600)
    rects, _ = hog.detectMultiScale(frame, winStride=(4,4), padding=(8,8), scale=1.05)
    objects = ct.update(rects)

    for (objectID, centroid) in objects.items():
        prev = track.get(objectID, None)
        track[objectID] = centroid
        if prev:
            if prev[1] < garis_y and centroid[1] >= garis_y:
                masuk += 1
            elif prev[1] > garis_y and centroid[1] <= garis_y:
                keluar += 1

        cv2.putText(frame, f"ID {objectID}", (centroid[0]-10, centroid[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
        cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)

    # Gambar garis dan info
    cv2.line(frame, (0, garis_y), (600, garis_y), (0, 0, 255), 2)
    cv2.putText(frame, f"Masuk: {masuk}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
    cv2.putText(frame, f"Keluar: {keluar}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)

    # Tampilkan waktu
    waktu = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(frame, waktu, (400, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,0), 1)

    cv2.imshow("Hitung Orang Masuk/Keluar", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
