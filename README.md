# 👣 People Counter Dashboard (Flask + OpenCV)

Sistem penghitung jumlah pengunjung masuk dan keluar perpustakaan berbasis Python, menggunakan webcam, Flask untuk dashboard real-time, dan OpenCV untuk deteksi orang.

---

## 🎥 Fitur Utama

- 📸 Deteksi orang dari webcam secara real-time
- 🧠 Pelacakan ID unik dengan Centroid Tracker
- 📊 Dashboard statistik harian berbasis web
- 🧾 Simpan log otomatis ke file `CSV` per jam
- 📈 Grafik pengunjung harian
- 📥 Ekspor data ke file Excel (.xlsx)
- 🔄 Tombol reset data & generate dummy data
- ✅ Siap dikompilasi ke `.exe` untuk pengguna non-programmer

---

## 🧱 Struktur Folder

```

people\_counter/
├── app.py
├── centroidtracker.py
├── log\_pengunjung.csv       ← Dibuat otomatis
├── static/
│   └── chart.png            ← Grafik harian
├── templates/
│   └── index.html           ← Dashboard Flask

````

---

## 🧰 Instalasi di Terminal Laragon

1. **Aktifkan terminal Laragon**
2. Pastikan sudah install Python (bisa cek dengan `where python`)

4. **Install semua dependensi**:

secara manual:

```bash
pip install flask opencv-python imutils pandas matplotlib openpyxl
```

---

## ▶️ Menjalankan Aplikasi

```bash
python app.py
```

Akses dashboard melalui browser:

```
http://localhost:5000
```

---

## 📦 Library yang Digunakan

| Library    | Fungsi                               |
| ---------- | ------------------------------------ |
| Flask      | Dashboard web real-time              |
| OpenCV     | Akses webcam dan deteksi orang (HOG) |
| Imutils    | Resize dan utilitas OpenCV           |
| Pandas     | Proses data log dan konversi         |
| Matplotlib | Membuat grafik harian                |
| Openpyxl   | Ekspor log ke file Excel             |

---

## 🔧 Tips Konfigurasi Kamera

Jika kamera tidak terdeteksi, ubah baris berikut di `app.py`:

```python
cap = cv2.VideoCapture(1, cv2.CAP_MSMF)
```

Ganti `1` menjadi `0`, `2`, dst, sesuai index kamera.

---

## 📄 Lisensi

MIT License – Silakan digunakan dan dimodifikasi sesuai kebutuhan.

---

## 👤 Author

Developed by Erwan Setyo Budi

## Preview

![preview](https://github.com/user-attachments/assets/0e53b434-ec36-48e6-8ea9-b0b911093e73)
![image](https://github.com/user-attachments/assets/a5c0cffd-e1f1-45a2-84c6-e5ac304138f9)


