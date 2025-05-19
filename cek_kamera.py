import cv2

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Tambahkan CAP_DSHOW jika di Windows
if not cap.isOpened():
    print("Kamera tidak bisa dibuka.")
else:
    print("Kamera berhasil dibuka.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Gagal menangkap gambar.")
            break
        cv2.imshow('Uji Kamera', frame)
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
