# Mastering Data Science: Konten Course

Konten course untuk app Mastering Data Science. Semua materi berupa JSON statis yang dimuat per modul.

## Struktur

```
index.json                    daftar semua course
STATUS.md                     progres modul siap dan total
video_manifest.json           modul yang butuh video dan brief-nya
courses/<ID>/outline.json     daftar modul tiap course
courses/<ID>/mNN.json         satu modul (3 sampai 5 lesson)
tools/                        outline, builder, validator, dan sumber penulisan
```

## Alur akses di app

1. Unduh `index.json` dan tampilkan daftar course.
2. Saat course dibuka, unduh `courses/<ID>/outline.json`.
3. Saat modul dibuka, unduh `courses/<ID>/mNN.json` dan simpan di perangkat.

Modul dengan `status` bernilai `todo` di outline belum punya file.

## Isi satu modul

Tiap lesson berisi 3 bagian materi (teks, contoh kode yang bisa dijalankan, callout, dan cek cepat), latihan bertingkat dengan tes per kasus, kuis, catatan penulis, ringkasan, dan notebook. Detail field dan pemetaan ke layar ada di [SCHEMA.md](SCHEMA.md).

Kode dijalankan di Pyodide. Library yang diizinkan: numpy, pandas, scipy, scikit-learn, matplotlib, seaborn, statsmodels, networkx, sqlite3, dan pustaka standar.

## Validasi

```
python3 tools/validate.py courses/D11/m01.json
```

Validator memeriksa skema, batas minimum konten, import yang diizinkan, menjalankan semua contoh kode, memastikan solusi latihan lolos tes, dan memastikan kode awal latihan belum lolos tes.

Membangun ulang index dan status:

```
python3 tools/build_outlines.py
python3 tools/build_video_manifest.py
```

## Hak cipta

Silabus disusun dengan acuan struktur bab beberapa buku. Seluruh teks, contoh, dan kode di repo ini ditulis ulang secara asli dan tidak menyalin isi buku. Daftar buku acuan tercantum di field `references` tiap modul. Teks mentah buku tidak disertakan di repo ini.
