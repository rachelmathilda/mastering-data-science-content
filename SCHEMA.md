# Skema Konten v2

Skema ini dibuat mengikuti layar desain app. Semua teks bahasa Indonesia. Teks markdown mendukung kode inline dengan backtick.

## index.json

| Field | Dipakai di layar |
|---|---|
| `curriculum_version` | chip "Kurikulum v1.0" |
| `icons` | daftar nama ikon yang valid untuk `icon` |
| `courses[].title` | judul penuh (detail dan sertifikat) |
| `courses[].title_short` | judul di list kursus dan beranda (maksimal 20 karakter agar tidak terpotong) |
| `courses[].icon` | ikon kotak kiri kartu kursus |
| `courses[].track_label` | chip filter (Fondasi, Data, Statistik, Machine Learning, Deep Learning, Data Engineering, Capstone, MLOps, Elective) |
| `courses[].level` | chip level: Pemula, Menengah, Lanjutan |
| `courses[].module_count` | "8 Modul" |
| `courses[].total_minutes` | "Total 6 Jam" (perkiraan, modul belum siap dihitung 105 menit) |
| `courses[].exercise_count` | chip "24 Latihan Kode" |
| `courses[].prerequisites` | rekomendasi urutan. `lock_policy: recommended` berarti ikon gembok boleh dilewati |
| `courses[].modules_ready` | modul yang sudah punya file |

## courses/ID/outline.json

Semua field index ditambah:

| Field | Dipakai di layar |
|---|---|
| `certificate` | `title`, `scope` ("Modul kurikulum penuh"), `id_prefix` untuk nomor sertifikat |
| `sources` | kartu "Sumber acuan" di detail kursus (judul, penulis, bab). Kosong bila tidak ada |
| `modules[]` | baris daftar modul: `title`, `estimated_minutes`, `status` (ready atau todo) |
| `modules[].practice_preview` | kartu "Latihan interaktif Modul N": `level_label`, `code_preview`, `lesson_id`, `exercise_id` |

Status selesai, sedang dipelajari, dan belum dimulai adalah state app, bukan JSON.

## courses/ID/mNN.json

Tingkat modul: `schema_version` (2), `title`, `estimated_minutes`, `lesson_count`, `exercise_count`, `practice_preview`, `learning_outcomes`, `lessons[]`, `video`, `references`.

Tingkat lesson:

| Field | Layar |
|---|---|
| `title` | judul besar reading mode (boleh berisi backtick) |
| `read_minutes` | "4 mnt baca" |
| `parts[]` | 3 bagian, "BAGIAN 2 DARI 3" dan progres bar. Tiap part: `title`, `read_minutes`, `blocks[]`, `quick_check` |
| `parts[].blocks[]` | urutan blok layar: `text`, `analogy`, `code_example`, `code_static`, `callout` |
| `parts[].quick_check` | kartu "Cek pemahaman cepat" dengan 2 sampai 3 opsi |
| `exercises[]` | layar latihan |
| `quiz[]` | layar kuis, 5 pertanyaan atau lebih |
| `author_note` | kartu catatan di akhir reading mode. `source` bernilai `author` atau `common_mistake` |
| `notebook.cells` | tombol "Buka di Notebook", sel teks dan kode dari contoh lesson |
| `summary`, `objectives`, `further_reading`, `common_mistakes` | ringkasan dan pelengkap |

Blok:

- `text`: `markdown`
- `analogy`: `title`, `text`, `image` (opsional, boleh null)
- `code_example`: `filename` (nama file di header kartu kode), `runnable`, `code`, `expected_output_note`, `explanation`. Tombol "Jalankan" memakai `code`
- `callout`: `kind` (tip, note, warning), `title`, `markdown`

Latihan: `title` ("Latihan 2"), `level_label` (Mudah, Sedang, Tantangan), `instruction` (kalimat utama), `note` (catatan kecil di bawahnya, boleh null), `filename`, `starter_code`, `hint` (tombol Petunjuk dan teks bawah editor), `solution`, dan `tests`:

```
tests.setup            impor bersama
tests.cases[]          id, name, label, pass_message, fail_hint, code
```

Cara menjalankan tes: eksekusi `setup`, lalu tiap `cases[].code` berurutan dalam satu namespace. Kasus lolos bila tidak ada exception. Bila gagal tampilkan pesan `AssertionError` plus `fail_hint` bila ada. Kasus yang belum dijalankan berstatus menunggu.

Kuis: `q`, `code` (opsional, kotak kode di bawah pertanyaan), `options[]` (`label`, `description`), `answer_index`, `hint`, `explanation`. Header "QUESTION 3 OF 5", streak, dan nyawa adalah state app.

## Yang sengaja tidak ada di JSON

- Profil instruktur, rating, dan jumlah ulasan: tidak ada penulis perorangan atau data ulasan, sehingga kartu diganti "Sumber acuan" dari `sources`
- Penandatangan, akreditasi, dan status "terverifikasi" di sertifikat: konten ini tidak ditandatangani siapa pun. Sertifikat memakai `certificate` saja, ditambah nama pengguna, tanggal, dan nomor yang dibuat app
- Streak, progres, dan nyawa: disimpan lokal di app
