from flask import Flask, render_template, Response, redirect, url_for, send_file
import cv2
import imutils
import pandas as pd
import datetime
import os
import matplotlib.pyplot as plt
import random
from centroidtracker import CentroidTracker

app = Flask(__name__)

# Inisialisasi kamera
cap = cv2.VideoCapture(1, cv2.CAP_MSMF)  # Ganti index jika perlu (0, 1, dll)

# Inisialisasi sistem
ct = CentroidTracker()
track = {}
masuk = 0
keluar = 0
garis_y = 250

# Inisialisasi detektor
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Simpan data ke log setiap jam
def simpan_log(masuk, keluar):
    waktu = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
    filepath = 'log_pengunjung.csv'

    if not os.path.exists(filepath):
        with open(filepath, 'w') as f:
            f.write("waktu,masuk,keluar\n")

    df = pd.read_csv(filepath)
    waktu_str = waktu.strftime('%Y-%m-%d %H:%M:%S')

    if waktu_str in df['waktu'].values:
        idx = df[df['waktu'] == waktu_str].index[0]
        df.at[idx, 'masuk'] = masuk
        df.at[idx, 'keluar'] = keluar
    else:
        df = pd.concat([df, pd.DataFrame([[waktu_str, masuk, keluar]], columns=['waktu', 'masuk', 'keluar'])])

    df.to_csv(filepath, index=False)

# Buat grafik harian
def buat_grafik_harian():
    filepath = 'log_pengunjung.csv'
    if not os.path.exists(filepath):
        return

    df = pd.read_csv(filepath)
    if df.empty:
        return

    df['waktu'] = pd.to_datetime(df['waktu'])
    hari_ini = pd.Timestamp.now().normalize()
    df_hari_ini = df[df['waktu'].dt.date == hari_ini.date()]

    if df_hari_ini.empty:
        return

    plt.figure(figsize=(8, 4))
    plt.plot(df_hari_ini['waktu'], df_hari_ini['masuk'], label='Masuk', marker='o')
    plt.plot(df_hari_ini['waktu'], df_hari_ini['keluar'], label='Keluar', marker='x')
    plt.title("Statistik Harian Pengunjung")
    plt.xlabel("Jam")
    plt.ylabel("Jumlah")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig('static/chart.png')
    plt.close()

# Jalankan kamera dan tracking
def gen_frames():
    global masuk, keluar, track
    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = imutils.resize(frame, width=600)
        rects, _ = hog.detectMultiScale(frame, winStride=(4,4), padding=(8,8), scale=1.05)
        objects = ct.update(rects)

        for (objectID, centroid) in objects.items():
            prev = track.get(objectID, None)
            track[objectID] = centroid

            if prev is not None:
                if prev[1] < garis_y and centroid[1] >= garis_y:
                    masuk += 1
                    simpan_log(masuk, keluar)
                elif prev[1] > garis_y and centroid[1] <= garis_y:
                    keluar += 1
                    simpan_log(masuk, keluar)

            cv2.putText(frame, f"ID {objectID}", (centroid[0]-10, centroid[1]-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
            cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)

        cv2.line(frame, (0, garis_y), (600, garis_y), (0, 0, 255), 2)
        cv2.putText(frame, f"Masuk: {masuk}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
        cv2.putText(frame, f"Keluar: {keluar}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Halaman utama
@app.route('/')
def index():
    buat_grafik_harian()
    return render_template('index.html', masuk=masuk, keluar=keluar)

# Streaming video dari kamera
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Reset data hari ini
@app.route('/reset_log')
def reset_log():
    filepath = 'log_pengunjung.csv'
    if os.path.exists(filepath):
        df = pd.read_csv(filepath)
        today = pd.Timestamp.now().normalize()
        df['waktu'] = pd.to_datetime(df['waktu'])
        df = df[df['waktu'].dt.date != today.date()]
        df.to_csv(filepath, index=False)
    return redirect(url_for('index'))

# Generate dummy data
@app.route('/generate_dummy')
def generate_dummy():
    filepath = 'log_pengunjung.csv'
    waktu_dasar = pd.Timestamp.now().replace(minute=0, second=0, microsecond=0)
    data = []

    for i in range(9, 17):  # jam 09.00 - 16.00
        waktu = waktu_dasar.replace(hour=i)
        m = random.randint(1, 10)
        k = random.randint(0, m)
        data.append([waktu.strftime('%Y-%m-%d %H:%M:%S'), m, k])

    df_dummy = pd.DataFrame(data, columns=['waktu', 'masuk', 'keluar'])

    if os.path.exists(filepath):
        df_existing = pd.read_csv(filepath)
        df_existing['waktu'] = pd.to_datetime(df_existing['waktu'])
        today = pd.Timestamp.now().normalize()
        df_existing = df_existing[df_existing['waktu'].dt.date != today.date()]
        df_combined = pd.concat([df_existing, df_dummy])
    else:
        df_combined = df_dummy

    df_combined.to_csv(filepath, index=False)
    return redirect(url_for('index'))

# Ekspor data ke Excel
@app.route('/download_excel')
def download_excel():
    filepath = 'log_pengunjung.xlsx'
    if os.path.exists('log_pengunjung.csv'):
        df = pd.read_csv('log_pengunjung.csv')
        df.to_excel(filepath, index=False)
    return send_file(filepath, as_attachment=True)

# Jalankan Flask
if __name__ == '__main__':
    app.run(debug=True)
