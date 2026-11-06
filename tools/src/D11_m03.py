import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, C, E, Q, M, lesson, write_module

REF = [{"book": "Machine Learning Yearning (Andrew Ng)", "chapters": "bab 13 sampai 15 dan bab 19"}]

SPAM = """
import numpy as np

def buat_spam(m, seed):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(m, 10))
    skor = X[:, :4] @ np.array([1.0, 0.8, 0.6, 0.4]) + 0.4 * X[:, 4:8].sum(axis=1) + 0.05 * X[:, 8:].sum(axis=1)
    y = (skor + 0.5 * rng.normal(size=m) > 0).astype(int)
    return X, y

GRUP = {"teks": [0, 1, 2, 3], "header": [4, 5, 6, 7], "volume": [8, 9]}
"""

l1 = lesson(
    "D11-03-1",
    "Bangun sistem pertama dengan cepat, lalu iterasi",
    35,
    [
        "Menjelaskan mengapa sistem sempurna tidak perlu dirancang di awal",
        "Membangun baseline dan membaca perilakunya untuk menemukan arah investasi",
        "Memakai ablasi kelompok fitur untuk mendapat petunjuk cepat",
        "Mengenali kapan saran ini berlaku untuk pembangun aplikasi dan kapan tidak untuk peneliti",
    ],
    [
        T("""
        ## Masalah: terlalu banyak arah yang masuk akal

        Kamu ingin membangun sistem anti-spam email baru. Tim punya beberapa ide. Kumpulkan training set spam yang sangat besar, misalnya dengan honeypot: sengaja mengirim alamat email palsu ke para spammer yang diketahui, sehingga pesan spam yang mereka kirim bisa dipanen otomatis. Kembangkan fitur untuk memahami isi teks email. Kembangkan fitur dari amplop atau header email yang menunjukkan server internet mana yang dilewati pesan. Dan masih banyak lagi.

        Bahkan orang yang sudah lama bekerja di bidang anti-spam akan kesulitan memilih satu arah dengan yakin. Bagi yang bukan ahli di bidang aplikasinya, memilih lebih sulit lagi. Setiap ide terdengar masuk akal, dan setiap ide memakan waktu. Menebak tanpa data hanyalah berjudi dengan berminggu-minggu kerja.

        Saran utamanya sederhana: jangan mulai dengan merancang dan membangun sistem yang sempurna. Bangun dan latih sistem dasar secepat mungkin, mungkin hanya dalam beberapa hari. Walau jauh dari sistem terbaik yang bisa kamu buat, memeriksa cara sistem dasar itu bekerja sangat berharga: kamu akan cepat menemukan petunjuk tentang arah paling menjanjikan untuk menanam waktumu.
        """),
        T("""
        ## Apa saja isi sistem dasar

        Sistem dasar tidak perlu canggih. Ia perlu lengkap dari ujung ke ujung agar bisa dievaluasi. Daftar periksanya:

        1. Data yang tersedia sekarang, bukan data ideal, dibagi menjadi training, dev, dan test dengan benar.
        2. Satu metrik tunggal yang disepakati tim.
        3. Model sederhana yang cepat dilatih, seperti regresi logistik atau pohon kecil.
        4. Skrip evaluasi yang menghasilkan error training, error dev, dan daftar contoh yang salah.
        5. Catatan hasil agar eksperimen berikutnya bisa dibandingkan.

        Targetnya hari, bukan minggu. Kecepatan bukan tujuan sendiri. Dengan baseline di tangan, kamu mendapat bahan nyata untuk diagnosis: berapa error training, berapa selisihnya ke dev, fitur kelompok mana yang paling berpengaruh, dan contoh seperti apa yang salah. Tanpa baseline, semua diskusi tim hanya berupa opini.
        """),
        T("""
        ## Petunjuk apa yang dicari dari baseline

        Setelah baseline berjalan, ada beberapa pertanyaan murah yang menghasilkan petunjuk kuat.

        **Seberapa besar error training dan selisihnya ke dev?** Ini memisahkan masalah bias dari variance, topik yang dibahas penuh di modul 5.

        **Fitur kelompok mana yang paling berpengaruh?** Ablasi sederhana: latih ulang tanpa satu kelompok fitur dan lihat berapa turun akurasinya. Jika membuang fitur teks menjatuhkan akurasi jauh dan membuang fitur header nyaris tidak berpengaruh, investasi pada fitur teks lebih menjanjikan daripada fitur header.

        **Apa yang terjadi bila data ditambah?** Learning curve dari lesson sebelumnya menunjukkan apakah data baru, misalnya dari honeypot, layak dikejar.

        **Contoh apa yang salah?** Ini jalan masuk ke error analysis yang dibahas di lesson berikutnya.

        Petunjuk-petunjuk ini tidak memberi jawaban pasti, tetapi mengubah tebakan buta menjadi tebakan terdidik. Itulah inti pendekatan iteratif: bangun cepat, baca petunjuk, perbaiki, ulangi.
        """),
        T("""
        ## Untuk siapa saran ini berlaku

        Penting dipahami cakupannya. Saran membangun sistem dasar dengan cepat ditujukan untuk pembaca yang ingin membangun aplikasi AI, bukan untuk yang tujuannya menerbitkan makalah akademik. Dalam riset, kebaruan metode dan perbandingan yang adil dengan karya lain sering menentukan, dan itu menuntut pendekatan yang berbeda. Untuk produk, nilai terbesar ada pada kecepatan belajar dari data nyata.

        Satu catatan lagi tentang kerendahan hati. Walau kamu ahli di bidang tertentu, intuisi tentang arah paling menjanjikan sering meleset. Sistem dasar yang dibangun dalam beberapa hari akan menunjukkan kapan intuisi itu keliru, dan menunjukkannya pada tahap ketika koreksi masih murah.
        """),
        K(
            "tip",
            """
            Tetapkan batas waktu keras untuk baseline, misalnya tiga hari. Jika kamu tergoda menambah satu fitur lagi sebelum menjalankan evaluasi pertama, itu pertanda kamu sedang merancang sistem sempurna, bukan membangun baseline.
            """,
        ),
        C(
            SPAM
            + """
from sklearn.linear_model import LogisticRegression

X_tr, y_tr = buat_spam(3000, 1)
X_dev, y_dev = buat_spam(1500, 2)
model = LogisticRegression(max_iter=1000).fit(X_tr, y_tr)
print("error train:", round(1 - model.score(X_tr, y_tr), 3))
print("error dev  :", round(1 - model.score(X_dev, y_dev), 3))
print("jumlah contoh dev yang salah:", int((model.predict(X_dev) != y_dev).sum()))
""",
            """
            error train sekitar 0.086
            error dev sekitar 0.084
            jumlah contoh dev yang salah sekitar 126
            """,
            """
            Baseline lengkap dari ujung ke ujung hanya butuh beberapa baris. Dengan tiga angka ini kamu sudah punya bahan diagnosis: selisih train dan dev kecil, dan ada lebih dari seratus contoh salah yang bisa dianalisis. Kecepatan di sini bukan soal terburu-buru, tetapi soal cepat memperoleh bukti.
            """,
        ),
        C(
            SPAM
            + """
from sklearn.linear_model import LogisticRegression

X_tr, y_tr = buat_spam(3000, 1)
X_dev, y_dev = buat_spam(1500, 2)
penuh = LogisticRegression(max_iter=1000).fit(X_tr, y_tr).score(X_dev, y_dev)
print("akurasi dev penuh:", round(penuh, 3))
for nama, kol in GRUP.items():
    sisa = [i for i in range(10) if i not in kol]
    akurasi = LogisticRegression(max_iter=1000).fit(X_tr[:, sisa], y_tr).score(X_dev[:, sisa], y_dev)
    print(f"tanpa {nama:7s}: akurasi {akurasi:.3f}  turun {penuh - akurasi:.3f}")
""",
            """
            tanpa teks: turun sekitar 0.27
            tanpa header: turun sekitar 0.10
            tanpa volume: turun hampir nol
            """,
            """
            Ablasi membuang satu kelompok fitur lalu mengukur penurunan akurasi dev. Fitur teks memikul sebagian besar sinyal, header menyumbang sedang, dan volume nyaris tidak berarti. Petunjuk ini langsung menyarankan investasi pada fitur teks dan menunda fitur volume.
            """,
        ),
        C(
            SPAM
            + """
from sklearn.linear_model import LogisticRegression

X_dev, y_dev = buat_spam(1500, 2)
print("m_train  error dev")
for m in [100, 300, 1000, 3000, 9000]:
    X_tr, y_tr = buat_spam(m, 1)
    err = 1 - LogisticRegression(max_iter=1000).fit(X_tr, y_tr).score(X_dev, y_dev)
    print(f"{m:7d}  {err:.3f}")
""",
            """
            error dev turun dari sekitar 0.12 ke sekitar 0.085 lalu mendatar
            """,
            """
            Learning curve untuk model dasar menunjukkan manfaat data tambahan, misalnya dari honeypot. Jika kurva sudah mendatar di sekitar ukuran data sekarang, mengumpulkan data jauh lebih banyak tidak akan membantu model ini. Ini contoh petunjuk murah yang menghemat berminggu-minggu.
            """,
        ),
        E(
            "D11-03-1-ex1",
            "mudah",
            """
            Tulis fungsi `bangun_baseline(X_tr, y_tr, X_dev, y_dev)` yang melatih `LogisticRegression(max_iter=1000)` pada training lalu mengembalikan dictionary `{"err_train": ..., "err_dev": ...}` dengan nilai error (1 dikurangi akurasi) dibulatkan ke 4 desimal.
            """,
            """
            from sklearn.linear_model import LogisticRegression

            def bangun_baseline(X_tr, y_tr, X_dev, y_dev):
                # TODO: implementasikan
                pass
            """,
            """
            import numpy as np
            rng = np.random.default_rng(0)
            X = rng.normal(size=(800, 4))
            y = (X[:, 0] + X[:, 1] > 0).astype(int)
            hasil = bangun_baseline(X[:500], y[:500], X[500:], y[500:])
            assert set(hasil) == {"err_train", "err_dev"}
            assert 0.0 <= hasil["err_train"] < 0.1
            assert 0.0 <= hasil["err_dev"] < 0.1
            assert hasil["err_train"] == round(hasil["err_train"], 4)
            """,
            "Fit model lalu hitung 1 - model.score untuk training dan dev, dibulatkan dengan round(..., 4).",
            """
            from sklearn.linear_model import LogisticRegression

            def bangun_baseline(X_tr, y_tr, X_dev, y_dev):
                model = LogisticRegression(max_iter=1000).fit(X_tr, y_tr)
                return {
                    "err_train": round(1 - model.score(X_tr, y_tr), 4),
                    "err_dev": round(1 - model.score(X_dev, y_dev), 4),
                }
            """,
        ),
        E(
            "D11-03-1-ex2",
            "sedang",
            """
            Tulis fungsi `ablasi(X_tr, y_tr, X_dev, y_dev, grup)`. `grup` adalah dictionary nama kelompok ke list indeks kolom. Untuk tiap kelompok, latih `LogisticRegression(max_iter=1000)` tanpa kolom kelompok itu dan hitung penurunan akurasi dev dibanding model dengan semua kolom. Kembalikan dictionary nama ke penurunan, dibulatkan 4 desimal.
            """,
            """
            from sklearn.linear_model import LogisticRegression

            def ablasi(X_tr, y_tr, X_dev, y_dev, grup):
                # TODO: implementasikan
                pass
            """,
            """
            import numpy as np
            rng = np.random.default_rng(0)
            def data(m):
                X = rng.normal(size=(m, 6))
                y = (3 * X[:, 0] + 3 * X[:, 1] + 0.3 * X[:, 2] + 0.3 * rng.normal(size=m) > 0).astype(int)
                return X, y
            X_tr, y_tr = data(800)
            X_dev, y_dev = data(600)
            grup = {"a": [0, 1], "b": [2, 3], "c": [4, 5]}
            d = ablasi(X_tr, y_tr, X_dev, y_dev, grup)
            assert set(d) == {"a", "b", "c"}
            assert d["a"] > 0.2
            assert abs(d["c"]) < 0.05
            assert d["a"] > d["b"] >= -0.05
            """,
            "Hitung akurasi model penuh sekali. Untuk tiap kelompok bentuk daftar kolom sisa dan latih ulang hanya dengan kolom itu.",
            """
            from sklearn.linear_model import LogisticRegression

            def ablasi(X_tr, y_tr, X_dev, y_dev, grup):
                n = X_tr.shape[1]
                penuh = LogisticRegression(max_iter=1000).fit(X_tr, y_tr).score(X_dev, y_dev)
                hasil = {}
                for nama, kol in grup.items():
                    sisa = [i for i in range(n) if i not in kol]
                    akurasi = LogisticRegression(max_iter=1000).fit(X_tr[:, sisa], y_tr).score(X_dev[:, sisa], y_dev)
                    hasil[nama] = round(penuh - akurasi, 4)
                return hasil
            """,
        ),
        E(
            "D11-03-1-ex3",
            "sedang",
            """
            Tulis fungsi `rekomendasi(err_train, err_dev, drop)` yang menerima dictionary `drop` hasil ablasi. Hitung `celah = round(err_dev - err_train, 6)`. Jika `celah > 0.03` kembalikan `"kumpulkan data atau tambah regularisasi"`. Jika tidak, kembalikan `"perbaiki fitur kelompok " + nama` dengan `nama` kelompok yang penurunan akurasinya terbesar (jika seri pilih nama paling awal secara abjad).
            """,
            """
            def rekomendasi(err_train, err_dev, drop):
                # TODO: implementasikan
                pass
            """,
            """
            assert rekomendasi(0.05, 0.12, {"teks": 0.3}) == "kumpulkan data atau tambah regularisasi"
            assert rekomendasi(0.10, 0.11, {"teks": 0.3, "header": 0.1}) == "perbaiki fitur kelompok teks"
            assert rekomendasi(0.10, 0.11, {"b": 0.2, "a": 0.2}) == "perbaiki fitur kelompok a"
            assert rekomendasi(0.10, 0.13, {"x": 0.1}) == "perbaiki fitur kelompok x"
            """,
            "Bulatkan celah dahulu. Untuk memilih kelompok gunakan min dengan key (-nilai, nama).",
            """
            def rekomendasi(err_train, err_dev, drop):
                celah = round(err_dev - err_train, 6)
                if celah > 0.03:
                    return "kumpulkan data atau tambah regularisasi"
                nama = min(drop, key=lambda n: (-drop[n], n))
                return "perbaiki fitur kelompok " + nama
            """,
        ),
        E(
            "D11-03-1-ex4",
            "menantang",
            """
            Ablasi dari satu training set bisa berderau. Tulis fungsi `ablasi_bootstrap(X_tr, y_tr, X_dev, y_dev, grup, k, seed)`. Buat `rng = np.random.default_rng(seed)`. Ulangi `k` kali: ambil `idx = rng.integers(0, len(X_tr), len(X_tr))`, hitung `ablasi` pada `X_tr[idx], y_tr[idx]`. Kembalikan rata-rata penurunan tiap kelompok, dibulatkan 4 desimal. Fungsi `ablasi` sudah disediakan.
            """,
            """
            import numpy as np
            from sklearn.linear_model import LogisticRegression

            def ablasi(X_tr, y_tr, X_dev, y_dev, grup):
                n = X_tr.shape[1]
                penuh = LogisticRegression(max_iter=1000).fit(X_tr, y_tr).score(X_dev, y_dev)
                hasil = {}
                for nama, kol in grup.items():
                    sisa = [i for i in range(n) if i not in kol]
                    akurasi = LogisticRegression(max_iter=1000).fit(X_tr[:, sisa], y_tr).score(X_dev[:, sisa], y_dev)
                    hasil[nama] = round(penuh - akurasi, 4)
                return hasil

            def ablasi_bootstrap(X_tr, y_tr, X_dev, y_dev, grup, k, seed):
                # TODO: implementasikan
                pass
            """,
            """
            rng = np.random.default_rng(0)
            def data(m):
                X = rng.normal(size=(m, 6))
                y = (3 * X[:, 0] + 3 * X[:, 1] + 0.3 * X[:, 2] + 0.3 * rng.normal(size=m) > 0).astype(int)
                return X, y
            X_tr, y_tr = data(800)
            X_dev, y_dev = data(600)
            grup = {"a": [0, 1], "b": [2, 3], "c": [4, 5]}
            r = ablasi_bootstrap(X_tr, y_tr, X_dev, y_dev, grup, 5, 0)
            assert set(r) == {"a", "b", "c"}
            assert max(r, key=r.get) == "a"
            assert r["a"] > 0.2
            assert r == ablasi_bootstrap(X_tr, y_tr, X_dev, y_dev, grup, 5, 0)
            """,
            "Kumpulkan hasil ablasi tiap putaran dalam list, lalu rata-ratakan per kelompok dengan np.mean dan round.",
            """
            import numpy as np
            from sklearn.linear_model import LogisticRegression

            def ablasi(X_tr, y_tr, X_dev, y_dev, grup):
                n = X_tr.shape[1]
                penuh = LogisticRegression(max_iter=1000).fit(X_tr, y_tr).score(X_dev, y_dev)
                hasil = {}
                for nama, kol in grup.items():
                    sisa = [i for i in range(n) if i not in kol]
                    akurasi = LogisticRegression(max_iter=1000).fit(X_tr[:, sisa], y_tr).score(X_dev[:, sisa], y_dev)
                    hasil[nama] = round(penuh - akurasi, 4)
                return hasil

            def ablasi_bootstrap(X_tr, y_tr, X_dev, y_dev, grup, k, seed):
                rng = np.random.default_rng(seed)
                kumpul = {nama: [] for nama in grup}
                for _ in range(k):
                    idx = rng.integers(0, len(X_tr), len(X_tr))
                    d = ablasi(X_tr[idx], y_tr[idx], X_dev, y_dev, grup)
                    for nama, nilai in d.items():
                        kumpul[nama].append(nilai)
                return {nama: round(float(np.mean(v)), 4) for nama, v in kumpul.items()}
            """,
        ),
    ],
    [
        M(
            "Merancang sistem sempurna selama berminggu-minggu sebelum evaluasi pertama.",
            "Bangun baseline lengkap dalam beberapa hari lalu gunakan hasilnya untuk memilih arah.",
        ),
        M(
            "Menganggap baseline harus mendekati performa akhir.",
            "Nilai baseline dari seberapa banyak petunjuk yang diberikannya, bukan dari seberapa tinggi akurasinya.",
        ),
        M(
            "Membaca satu kali ablasi sebagai kebenaran pasti.",
            "Ulangi dengan beberapa resampling untuk memastikan urutan kelompok fitur stabil.",
        ),
    ],
    [
        Q(
            "Mengapa tidak langsung merancang sistem anti-spam yang sempurna?",
            ["Karena komputasi mahal", "Karena sulit menebak arah paling menjanjikan tanpa melihat perilaku sistem nyata", "Karena spam tidak berubah", "Karena data tidak ada"],
            1,
            "Bahkan ahli kesulitan memilih arah tanpa data. Sistem dasar memberi petunjuk nyata dengan cepat.",
        ),
        Q(
            "Apa isi minimal sistem dasar yang baik?",
            ["Model paling canggih", "Alur lengkap dari data sampai evaluasi dengan satu metrik", "Dashboard produksi", "Fitur sebanyak mungkin"],
            1,
            "Alur ujung ke ujung dengan metrik tunggal sudah cukup untuk menghasilkan diagnosis.",
        ),
        Q(
            "Ablasi menunjukkan membuang fitur teks menjatuhkan akurasi 25 poin sedangkan membuang volume tidak berpengaruh. Kesimpulan?",
            ["Investasi pada fitur teks lebih menjanjikan", "Hapus semua fitur", "Tambah fitur volume", "Ganti metrik"],
            0,
            "Kelompok fitur yang membawa sinyal paling banyak adalah tempat perbaikan paling mungkin berdampak.",
        ),
        Q(
            "Saran membangun sistem dasar dengan cepat terutama ditujukan untuk siapa?",
            ["Peneliti yang menerbitkan makalah", "Pembangun aplikasi AI", "Penguji perangkat keras", "Pengelola basis data"],
            1,
            "Saran ini untuk pembaca yang ingin membangun aplikasi, bukan untuk tujuan publikasi akademik.",
        ),
        Q(
            "Jika learning curve baseline sudah mendatar, apa implikasinya untuk ide mengumpulkan data honeypot yang sangat besar?",
            ["Pasti sangat bermanfaat", "Mungkin tidak membantu model ini, sehingga perlu dipertimbangkan ulang", "Wajib dilakukan", "Menggantikan dev set"],
            1,
            "Kurva mendatar menunjukkan data tambahan tidak lagi menurunkan error untuk model itu.",
        ),
    ],
    [
        "Bangun dan latih sistem dasar dalam hitungan hari, lalu iterasi.",
        "Sistem dasar harus lengkap dari ujung ke ujung dengan metrik tunggal.",
        "Error train dev, ablasi fitur, dan learning curve memberi petunjuk murah tentang arah investasi.",
        "Saran ini untuk pembangun aplikasi, sedangkan riset akademik punya pertimbangan berbeda.",
    ],
    ["Machine Learning Yearning, bab 13 (Andrew Ng): bangun sistem pertama dengan cepat lalu iterasi"],
)

l2 = lesson(
    "D11-03-2",
    "Error analysis: hitung dulu sebelum membangun",
    35,
    [
        "Melakukan error analysis dengan memeriksa sampel contoh dev yang salah",
        "Menghitung batas atas manfaat sebuah proyek dari fraksi kategori error",
        "Memperkirakan ketidakpastian fraksi dari sampel kecil",
        "Memutuskan apakah sebuah proyek layak dengan perbandingan manfaat dan biaya",
    ],
    [
        T("""
        ## Skenario: anjing yang dikira kucing

        Saat mencoba aplikasi kucingmu, kamu melihat beberapa contoh ketika anjing keliru diklasifikasikan sebagai kucing. Beberapa anjing memang mirip kucing. Seorang rekan tim mengusulkan memasang perangkat lunak pihak ketiga agar sistem lebih baik pada gambar anjing. Pekerjaannya makan waktu sebulan dan rekan itu sangat antusias. Apakah kamu langsung menyuruhnya jalan?

        Sebelum menanam sebulan, perkirakan dulu seberapa besar proyek itu akan memperbaiki akurasi. Baru setelah itu kamu bisa memutuskan secara rasional apakah sebulan itu sepadan, atau waktu itu lebih baik dipakai untuk tugas lain.

        Antusiasme dan intuisi itu penting, tetapi bukan bukti. Banyak insinyur enggan melakukan error analysis. Rasanya lebih seru langsung mengimplementasikan ide daripada mempertanyakan apakah ide itu layak waktunya. Itu kesalahan umum: tim bisa menghabiskan sebulan hanya untuk menyadari kemudian bahwa hasilnya nyaris tidak ada.
        """),
        T("""
        ## Prosedur error analysis

        Langkahnya sederhana dan murah.

        1. Kumpulkan sampel 100 contoh dev set yang **salah diklasifikasikan** oleh sistemmu.
        2. Periksa contoh itu secara manual dan hitung berapa pecahan yang berupa gambar anjing.

        Proses memeriksa contoh yang salah ini disebut **error analysis**. Misalkan hanya 5 persen contoh salah yang berupa anjing. Sebesar apa pun kamu memperbaiki performa pada gambar anjing, kamu tidak akan menghilangkan lebih dari 5 persen error. Angka 5 persen adalah **batas atas** (ceiling) manfaat proyek itu. Jika sistem sekarang akurat 90 persen (error 10 persen), perbaikan itu paling banyak membawa akurasi ke 90,5 persen (error 9,5 persen).

        Sebaliknya, jika 50 persen kesalahan berupa anjing, kamu bisa lebih yakin proyek itu berdampak besar. Akurasi bisa naik dari 90 ke 95 persen, yaitu penurunan error relatif 50 persen. Prosedur menghitung sederhana ini memberi dasar kuantitatif untuk memutuskan apakah investasi itu dilakukan.
        """),
        T("""
        ## Dua jam melawan satu bulan

        Memeriksa 100 contoh secara manual tidak lama. Bahkan dengan satu menit per gambar, kamu selesai dalam waktu kurang dari dua jam. Dua jam itu bisa menyelamatkanmu dari sebulan usaha yang sia-sia. Perbandingan biaya ini adalah alasan terkuat melakukan error analysis sebelum proyek besar apa pun.

        Ada tiga bilangan yang perlu kamu bedakan. **Error total** adalah proporsi contoh dev yang salah, misalnya 10 persen. **Fraksi kategori** adalah bagian dari kesalahan yang berasal dari kategori tertentu, misalnya 5 persen dari kesalahan itu anjing. **Batas atas perbaikan** dalam poin persen adalah error total dikali fraksi kategori, yaitu 0,10 kali 0,05 sama dengan 0,5 poin persen.

        Error analysis juga menginspirasi arah baru, bukan hanya menilai ide yang sudah ada. Saat melihat contoh yang salah, kamu sering menemukan pola yang tidak terpikirkan sebelumnya.
        """),
        T("""
        ## Ketidakpastian dari sampel kecil

        Fraksi yang kamu hitung dari 100 contoh adalah estimasi, bukan nilai pasti. Jika dalam 100 contoh ada 5 anjing, fraksi sebenarnya bisa 2 persen atau 10 persen. Rumus interval kepercayaan 95 persen pendekatan normal adalah `p ± 1,96 * sqrt(p * (1 - p) / n)`, dengan `p` fraksi terhitung dan `n` banyaknya contoh salah yang diperiksa.

        Untuk keputusan prioritas, ketidakpastian seperti itu biasanya bisa diterima. Kamu hanya perlu tahu apakah batas atas manfaat itu sekitar 5 persen atau sekitar 50 persen. Perbedaan sebesar itu terlihat jelas bahkan dari sampel kecil. Yang perlu diwaspadai adalah ketika dua kategori fraksinya mirip, misalnya 30 dan 35 persen dari sampel 50 contoh. Pada kasus itu pilihan antara keduanya harus dipandu faktor lain seperti biaya dan peluang berhasil.
        """),
        K(
            "note",
            """
            Batas atas bukan prediksi. Proyek yang menyasar kategori dengan fraksi 50 persen hanya bisa menghilangkan paling banyak setengah error, dan hampir tidak pernah menghilangkan semuanya. Anggap batas atas sebagai alat menyingkirkan ide yang tidak layak, bukan menjanjikan hasil.
            """,
        ),
        C(
            """
err_total = 0.10
for frac in [0.05, 0.50]:
    err_setelah = err_total * (1 - frac)
    relatif = (err_total - err_setelah) / err_total
    print(f"fraksi anjing {frac:.0%}: error terbaik {err_setelah:.3f}, penurunan relatif {relatif:.0%}")
""",
            """
            fraksi anjing 5%: error terbaik 0.095, penurunan relatif 5%
            fraksi anjing 50%: error terbaik 0.050, penurunan relatif 50%
            """,
            """
            Dua skenario dibandingkan. Jika hanya 5 persen kesalahan berupa anjing, error terbaik yang mungkin 9,5 persen. Jika 50 persen, error bisa turun ke 5 persen. Perhitungan ini butuh beberapa detik dan menentukan apakah sebulan kerja layak.
            """,
        ),
        C(
            """
import numpy as np

rng = np.random.default_rng(0)
n_salah = 1000
kategori = rng.choice(["anjing", "kucing_besar", "buram", "lain"], size=n_salah, p=[0.08, 0.30, 0.40, 0.22])
sampel = rng.choice(kategori, size=100, replace=False)

for nama in ["anjing", "kucing_besar", "buram", "lain"]:
    k = int(np.sum(sampel == nama))
    p = k / 100
    s = 1.96 * np.sqrt(p * (1 - p) / 100)
    benar = np.mean(kategori == nama)
    print(f"{nama:13s} sampel {p:.2f} (CI {max(0, p - s):.2f} sampai {min(1, p + s):.2f})  sebenarnya {benar:.2f}")
""",
            """
            tiap kategori: fraksi sampel dekat fraksi sebenarnya dan CI menutupinya
            """,
            """
            Dari 1000 kesalahan yang diketahui kategori sebenarnya, kita memeriksa sampel 100. Fraksi sampel mendekati fraksi sebenarnya dan interval kepercayaan menutupinya. Untuk keputusan prioritas, sampel 100 cukup membedakan kategori besar dari kategori kecil.
            """,
        ),
        C(
            """
def layak(frac, err_total, biaya_hari, ambang_poin_per_hari):
    gain_poin = frac * err_total * 100
    return gain_poin / biaya_hari >= ambang_poin_per_hari

print("anjing (5%), 30 hari :", layak(0.05, 0.10, 30, 0.05))
print("buram (61%), 10 hari :", layak(0.61, 0.10, 10, 0.05))
""",
            """
            anjing (5%), 30 hari : False
            buram (61%), 10 hari : True
            """,
            """
            Batas atas manfaat dibagi biaya memberi manfaat per hari kerja, yang dibandingkan dengan ambang yang kamu tetapkan. Proyek anjing hanya memberi paling banyak 0,5 poin persen dalam 30 hari, sementara proyek gambar buram bisa memberi hingga 6,1 poin dalam 10 hari.
            """,
        ),
        E(
            "D11-03-2-ex1",
            "mudah",
            """
            Tulis fungsi `batas_atas(frac, err_total)` yang mengembalikan tuple `(err_terbaik, penurunan_relatif)`. `err_terbaik = err_total * (1 - frac)` dan `penurunan_relatif = frac`. Bulatkan keduanya ke 6 desimal.
            """,
            """
            def batas_atas(frac, err_total):
                # TODO: implementasikan
                pass
            """,
            """
            assert batas_atas(0.05, 0.10) == (0.095, 0.05)
            assert batas_atas(0.5, 0.10) == (0.05, 0.5)
            assert batas_atas(0.0, 0.2) == (0.2, 0.0)
            assert batas_atas(1.0, 0.2) == (0.0, 1.0)
            """,
            "Hitung err_total * (1 - frac) dan bulatkan dengan round(nilai, 6).",
            """
            def batas_atas(frac, err_total):
                return round(err_total * (1 - frac), 6), round(frac, 6)
            """,
        ),
        E(
            "D11-03-2-ex2",
            "sedang",
            """
            Tulis fungsi `ambil_sampel_salah(y_true, y_pred, k, seed)` yang mengembalikan array indeks sampel acak berukuran `min(k, jumlah_salah)` dari contoh yang salah prediksi (`y_true != y_pred`), tanpa pengembalian. Gunakan `np.random.default_rng(seed)` dan `rng.choice(..., replace=False)`. Indeks harus terurut naik.
            """,
            """
            import numpy as np

            def ambil_sampel_salah(y_true, y_pred, k, seed):
                # TODO: implementasikan
                pass
            """,
            """
            import numpy as np
            y_true = np.array([0, 1, 1, 0, 1, 0, 0, 1, 1, 0])
            y_pred = np.array([0, 0, 1, 1, 1, 0, 1, 0, 1, 0])
            salah = set(np.where(y_true != y_pred)[0])
            s = ambil_sampel_salah(y_true, y_pred, 3, 0)
            assert len(s) == 3 and set(s) <= salah
            assert list(s) == sorted(s)
            semua = ambil_sampel_salah(y_true, y_pred, 100, 0)
            assert set(semua) == salah
            assert list(ambil_sampel_salah(y_true, y_pred, 3, 0)) == list(s)
            """,
            "Cari indeks salah dengan np.where, tentukan ukuran min(k, len(salah)), pilih dengan rng.choice, lalu urutkan dengan np.sort.",
            """
            import numpy as np

            def ambil_sampel_salah(y_true, y_pred, k, seed):
                y_true = np.asarray(y_true)
                y_pred = np.asarray(y_pred)
                salah = np.where(y_true != y_pred)[0]
                n = min(k, len(salah))
                rng = np.random.default_rng(seed)
                return np.sort(rng.choice(salah, size=n, replace=False))
            """,
        ),
        E(
            "D11-03-2-ex3",
            "sedang",
            """
            Tulis fungsi `layak_dikerjakan(frac, err_total, biaya_hari, ambang)` yang menghitung `gain = frac * err_total * 100` (poin persen), lalu mengembalikan `True` bila `gain / biaya_hari >= ambang` dan `False` selain itu. Jika `biaya_hari <= 0` kembalikan `True` bila `gain > 0`.
            """,
            """
            def layak_dikerjakan(frac, err_total, biaya_hari, ambang):
                # TODO: implementasikan
                pass
            """,
            """
            assert layak_dikerjakan(0.05, 0.10, 30, 0.05) is False
            assert layak_dikerjakan(0.61, 0.10, 10, 0.05) is True
            assert layak_dikerjakan(0.5, 0.1, 0, 0.05) is True
            assert layak_dikerjakan(0.0, 0.1, 0, 0.05) is False
            """,
            "Tangani biaya nol atau negatif lebih dulu, lalu bandingkan gain per hari dengan ambang. Kembalikan nilai bool murni.",
            """
            def layak_dikerjakan(frac, err_total, biaya_hari, ambang):
                gain = frac * err_total * 100
                if biaya_hari <= 0:
                    return bool(gain > 0)
                return bool(gain / biaya_hari >= ambang)
            """,
        ),
        E(
            "D11-03-2-ex4",
            "menantang",
            """
            Tulis fungsi `interval_fraksi(k, n)` yang mengembalikan interval kepercayaan 95 persen pendekatan normal `(bawah, atas)` untuk fraksi `k / n`: `p = k / n`, `s = 1.96 * sqrt(p * (1 - p) / n)`. Potong hasil ke rentang 0 sampai 1 dan bulatkan ke 4 desimal. Untuk `n = 0` kembalikan `(0.0, 1.0)`.
            """,
            """
            import math

            def interval_fraksi(k, n):
                # TODO: implementasikan
                pass
            """,
            """
            lo, hi = interval_fraksi(50, 100)
            assert abs(lo - 0.4020) < 1e-4 and abs(hi - 0.5980) < 1e-4
            lo, hi = interval_fraksi(0, 100)
            assert lo == 0.0 and hi == 0.0
            lo, hi = interval_fraksi(100, 100)
            assert lo == 1.0 and hi == 1.0
            assert interval_fraksi(0, 0) == (0.0, 1.0)
            lo, hi = interval_fraksi(5, 100)
            assert 0.0 <= lo < 0.05 < hi < 0.12
            """,
            "Tangani n sama dengan nol lebih dulu. Gunakan max(0.0, ...) dan min(1.0, ...) untuk memotong, lalu round 4.",
            """
            import math

            def interval_fraksi(k, n):
                if n == 0:
                    return 0.0, 1.0
                p = k / n
                s = 1.96 * math.sqrt(p * (1 - p) / n)
                return round(max(0.0, p - s), 4), round(min(1.0, p + s), 4)
            """,
        ),
    ],
    [
        M(
            "Langsung mengerjakan proyek besar karena rekan tim antusias.",
            "Lakukan error analysis dulu untuk memperkirakan batas atas manfaat.",
        ),
        M(
            "Memeriksa contoh yang benar atau contoh acak, bukan contoh yang salah.",
            "Kumpulkan sampel contoh yang salah diklasifikasikan lalu kelompokkan penyebabnya.",
        ),
        M(
            "Menganggap batas atas sebagai hasil yang pasti tercapai.",
            "Perlakukan batas atas sebagai alat penyaring ide, dan pertimbangkan peluang berhasil dan biaya.",
        ),
    ],
    [
        Q(
            "Hanya 5 persen kesalahan berupa anjing dengan error total 10 persen. Berapa error terbaik bila semua masalah anjing teratasi?",
            ["0 persen", "9,5 persen", "5 persen", "10 persen"],
            1,
            "10 persen dikali (1 dikurangi 0,05) sama dengan 9,5 persen.",
        ),
        Q(
            "Berapa kira-kira contoh salah yang disarankan diperiksa awalnya?",
            ["Sekitar 5", "Sekitar 100", "Sekitar 100.000", "Seluruh dataset"],
            1,
            "Sekitar 100 contoh yang salah cukup untuk gambaran awal dan hanya butuh sekitar dua jam.",
        ),
        Q(
            "Mengapa error analysis sering dihindari insinyur?",
            ["Terlalu mahal", "Terasa kurang seru dibanding langsung mengimplementasikan ide", "Tidak bisa dilakukan manual", "Butuh GPU"],
            1,
            "Banyak insinyur lebih suka langsung membangun, padahal itu bisa membuang waktu sebulan.",
        ),
        Q(
            "Dua kategori punya fraksi 30 dan 35 persen dari 50 contoh. Apa yang sebaiknya dilakukan?",
            ["Selalu pilih yang 35 persen", "Pertimbangkan biaya dan peluang berhasil karena perbedaannya dalam ketidakpastian", "Abaikan keduanya", "Tambah test set"],
            1,
            "Perbedaan kecil pada sampel kecil tidak membedakan kategori secara meyakinkan, jadi faktor lain ikut menentukan.",
        ),
        Q(
            "Apa arti batas atas manfaat suatu proyek?",
            ["Hasil pasti proyek", "Maksimum error yang bisa dihilangkan jika kategori itu terselesaikan sempurna", "Biaya proyek", "Jumlah contoh dev"],
            1,
            "Batas atas adalah plafon: paling banyak sebesar fraksi kategori itu yang bisa dihilangkan.",
        ),
    ],
    [
        "Error analysis adalah memeriksa contoh dev yang salah untuk memahami penyebab kesalahan.",
        "Fraksi kategori dikali error total memberi batas atas manfaat sebuah proyek.",
        "Sampel sekitar 100 contoh salah cukup untuk prioritas, dan interval kepercayaan menunjukkan ketidakpastian.",
        "Dua jam error analysis bisa menyelamatkan sebulan usaha yang sia-sia.",
    ],
    ["Machine Learning Yearning, bab 14 (Andrew Ng): error analysis dengan melihat contoh dev set"],
)

l3 = lesson(
    "D11-03-3",
    "Evaluasi banyak ide paralel dengan spreadsheet",
    35,
    [
        "Membangun tabel error analysis dengan beberapa kategori sekaligus",
        "Menghitung persentase tiap kategori dan memahami mengapa totalnya bisa lebih dari 100 persen",
        "Menambah kategori baru saat contoh diperiksa ulang",
        "Menggabungkan persentase kategori dengan usaha dan peluang untuk menentukan prioritas",
    ],
    [
        T("""
        ## Satu tabel untuk banyak ide

        Tim punya beberapa ide untuk memperbaiki detektor kucing: perbaiki masalah anjing yang dikira kucing, perbaiki masalah kucing besar seperti singa dan macan kumbang yang dikira kucing rumahan, dan perbaiki performa pada gambar buram.

        Semua ide itu bisa dievaluasi secara paralel dengan satu tabel. Caranya, buat spreadsheet dan isi sambil memeriksa kira-kira 100 gambar dev yang salah. Setiap baris adalah satu gambar. Setiap kolom adalah satu kategori masalah (Anjing, Kucing besar, Buram) dan kamu beri tanda centang bila gambar itu termasuk kategori tersebut. Tambahkan kolom Komentar untuk mencatat hal yang akan membantumu mengingat contoh tertentu, misalnya "singa di kebun binatang saat hujan".

        Di bagian bawah, hitung persentase tiap kolom dari total baris. Satu tabel kecil itu menggantikan perdebatan panjang: kamu melihat berapa persen kesalahan yang disentuh tiap ide.
        """),
        T("""
        ## Satu contoh bisa punya banyak kategori

        Gambar tertentu bisa tercentang di lebih dari satu kolom. Misalnya gambar singa di kebun binatang saat hujan masuk kategori Kucing besar sekaligus Buram. Karena itu persentase di bagian bawah tidak harus berjumlah 100 persen. Ini bukan kesalahan. Tiap persentase menjawab pertanyaan berbeda: berapa persen kesalahan yang tersentuh bila kategori ini diselesaikan.

        Dalam contoh hasil akhir, setelah memeriksa 100 contoh, kamu mungkin mendapat Anjing 8 persen, Kucing besar 43 persen, dan Buram 61 persen. Maka proyek anjing paling banyak menghilangkan 8 persen error. Proyek kucing besar atau gambar buram bisa menghilangkan jauh lebih banyak, jadi kamu memilih salah satunya. Jika tim cukup besar, sebagian insinyur bisa mengerjakan kucing besar dan lainnya mengerjakan gambar buram secara paralel.
        """),
        T("""
        ## Kategori baru muncul sambil bekerja

        Kamu boleh mulai dengan kategori yang sudah dipikirkan, tetapi dalam praktik, begitu mulai memeriksa contoh, kamu akan terinspirasi mengusulkan kategori baru. Misalnya setelah selusin gambar kamu sadar banyak kesalahan terjadi pada foto yang diberi filter Instagram. Kamu bisa kembali dan menambah kolom Instagram ke tabel, lalu memeriksa ulang gambar sebelumnya dengan kategori baru.

        Kategori yang paling berguna adalah yang kamu punya ide perbaikannya. Misalnya kategori Instagram paling berguna bila kamu punya ide membatalkan filter dan memulihkan gambar asli. Tetapi kamu tidak perlu membatasi diri pada kategori yang sudah kamu tahu cara memperbaikinya. Tujuan proses ini membangun intuisi tentang area yang paling menjanjikan.

        Error analysis bersifat iteratif. Tidak masalah jika kamu mulai tanpa kategori apa pun. Setelah melihat beberapa gambar, kategori akan muncul, dan setelah mengategorikan sebagian, muncul kategori lain yang membuatmu meninjau ulang gambar-gambar tadi.
        """),
        T("""
        ## Dari persentase ke prioritas

        Error analysis tidak menghasilkan rumus matematika kaku yang langsung menunjuk tugas berprioritas tertinggi. Kamu juga harus memperhitungkan seberapa besar kemajuan yang kamu harapkan pada tiap kategori dan seberapa banyak usaha yang dibutuhkan untuk menanganinya.

        Skor sederhana yang membantu: `skor = persen_kategori * kemajuan_diharapkan / usaha`. `kemajuan_diharapkan` adalah pecahan kategori itu yang menurutmu bisa benar-benar dibereskan (misalnya 0,5 bila kamu yakin separuhnya bisa teratasi). `usaha` adalah estimasi hari kerja. Skor ini heuristik, sama seperti skor prioritas di awal course. Fungsinya memaksa tim menuliskan asumsi, bukan menggantikan penilaian.

        Dengan pandas, tabel error analysis menjadi DataFrame boolean yang mudah dihitung, difilter, dan disimpan sebagai CSV, sehingga hasilnya bisa dibaca ulang beberapa minggu kemudian.
        """),
        T("""
        ## Praktik menjalankan sesi error analysis

        Beberapa kebiasaan membuat sesi ini jauh lebih efektif. Pertama, sediakan alat untuk melihat contoh dengan cepat. Jika tiap gambar atau teks butuh beberapa klik untuk dibuka, seratus contoh akan terasa seperti pekerjaan seharian. Siapkan notebook yang menampilkan contoh bersama label, prediksi, dan skor model dalam satu layar.

        Kedua, jangan lakukan sendirian bila ada rekan yang bisa membantu. Dua orang yang mengategorikan contoh yang sama sering berbeda pendapat pada contoh yang ambigu. Perbedaan itu bukan gangguan. Itu petunjuk bahwa definisi kategori perlu dipertajam sebelum proyek perbaikannya dirancang.

        Ketiga, simpan contoh yang menarik. Kolom komentar bukan formalitas. Beberapa minggu kemudian, ketika tim berdebat apakah kategori buram benar-benar dominan, contoh nyata yang tersimpan lebih meyakinkan daripada angka saja.

        Keempat, ulangi secara berkala. Setelah satu proyek perbaikan selesai, distribusi kesalahan berubah. Kategori yang tadinya 61 persen mungkin tinggal 20 persen, dan kategori lain naik menjadi yang terbesar. Error analysis bukan acara sekali jalan, melainkan bagian dari ritme kerja tim.
        """),
        K(
            "tip",
            """
            Simpan tabel error analysis bersama versi model yang dianalisis. Ketika model berubah, error analysis lama menjadi usang dan harus diulang pada contoh salah yang baru.
            """,
        ),
        C(
            """
import pandas as pd

df = pd.DataFrame(
    {
        "anjing": [True, False, False, False],
        "kucing_besar": [False, False, True, True],
        "buram": [False, True, True, False],
        "komentar": ["pitbull warna tidak biasa", "", "singa di kebun binatang saat hujan", "macan kumbang di balik pohon"],
    }
)
kategori = ["anjing", "kucing_besar", "buram"]
print((df[kategori].mean() * 100).round(1))
print("jumlah persen:", float((df[kategori].mean() * 100).sum()))
""",
            """
            anjing          25.0
            kucing_besar    50.0
            buram           50.0
            jumlah persen: 125.0
            """,
            """
            Tabel kecil empat gambar menghasilkan persentase tiap kategori. Totalnya 125 persen karena satu gambar punya dua kategori sekaligus. Itu normal untuk tabel error analysis.
            """,
        ),
        C(
            """
import pandas as pd

df = pd.DataFrame(
    {
        "anjing": [True, False, False, False],
        "kucing_besar": [False, False, True, True],
        "buram": [False, True, True, False],
    }
)
df["instagram"] = [False, False, False, True]
persen = df.mean() * 100
progres = {"anjing": 0.7, "kucing_besar": 0.4, "buram": 0.5, "instagram": 0.9}
usaha = {"anjing": 30, "kucing_besar": 20, "buram": 5, "instagram": 3}
tabel = pd.DataFrame({"persen": persen, "progres": pd.Series(progres), "usaha": pd.Series(usaha)})
tabel["skor"] = tabel["persen"] * tabel["progres"] / tabel["usaha"]
print(tabel.sort_values("skor", ascending=False).round(2))
""",
            """
            baris diurutkan menurut skor, dengan kategori murah dan lumayan besar di atas
            """,
            """
            Kategori baru (instagram) ditambahkan langsung sebagai kolom. Persen dari tabel digabung dengan perkiraan kemajuan dan usaha untuk menghasilkan skor prioritas. Perhatikan kategori kecil tetapi murah bisa mengalahkan kategori besar yang mahal.
            """,
        ),
        C(
            """
import pandas as pd

df = pd.DataFrame(
    {
        "anjing": [True, False, False, False, True],
        "kucing_besar": [False, False, True, True, False],
        "buram": [False, True, True, False, False],
    }
)
jumlah_label = df.sum(axis=1)
print("gambar dengan 2 kategori atau lebih:", int((jumlah_label >= 2).sum()))
print("gambar tanpa kategori:", int((jumlah_label == 0).sum()))
print(pd.crosstab(df["kucing_besar"], df["buram"]))
""",
            """
            gambar dengan 2 kategori atau lebih: 1
            gambar tanpa kategori: 0
            """,
            """
            Menghitung tumpang tindih kategori membantu memahami hubungan masalah. Jika banyak kucing besar juga buram, memperbaiki satu bisa sekaligus membantu yang lain. Tabel silang mempermudah melihat hubungan itu.
            """,
        ),
        E(
            "D11-03-3-ex1",
            "mudah",
            """
            Tulis fungsi `persen_kategori(df, kolom)` yang menerima DataFrame boolean `df` dan list `kolom`, lalu mengembalikan `pandas.Series` berisi persentase baris bernilai `True` pada tiap kolom (0 sampai 100), dibulatkan 1 desimal.
            """,
            """
            import pandas as pd

            def persen_kategori(df, kolom):
                # TODO: implementasikan
                pass
            """,
            """
            import pandas as pd
            df = pd.DataFrame({"a": [True, False, False, False], "b": [True, True, False, False]})
            s = persen_kategori(df, ["a", "b"])
            assert isinstance(s, pd.Series)
            assert s["a"] == 25.0 and s["b"] == 50.0
            assert list(s.index) == ["a", "b"]
            """,
            "Ambil df[kolom].mean() lalu kalikan 100 dan round(1).",
            """
            import pandas as pd

            def persen_kategori(df, kolom):
                return (df[kolom].mean() * 100).round(1)
            """,
        ),
        E(
            "D11-03-3-ex2",
            "sedang",
            """
            Tulis fungsi `tabel_prioritas(df, kolom, progres, usaha)` yang mengembalikan DataFrame dengan kolom `persen`, `skor` dan indeks nama kategori, diurutkan dari skor tertinggi. `persen` adalah persentase `True` per kolom (tanpa pembulatan), dan `skor = persen * progres[nama] / usaha[nama]`.
            """,
            """
            import pandas as pd

            def tabel_prioritas(df, kolom, progres, usaha):
                # TODO: implementasikan
                pass
            """,
            """
            import pandas as pd
            df = pd.DataFrame({"a": [True, False, False, False], "b": [True, True, False, False], "c": [False, False, False, True]})
            t = tabel_prioritas(df, ["a", "b", "c"], {"a": 1.0, "b": 0.5, "c": 1.0}, {"a": 5, "b": 10, "c": 1})
            assert list(t.columns) == ["persen", "skor"]
            assert list(t.index) == ["c", "a", "b"]
            assert abs(t.loc["c", "skor"] - 25.0) < 1e-9
            assert abs(t.loc["a", "skor"] - 5.0) < 1e-9
            assert abs(t.loc["b", "skor"] - 2.5) < 1e-9
            """,
            "Bangun DataFrame dari persen, lalu hitung skor dengan mengambil nilai dictionary lewat indeks, dan urutkan dengan sort_values.",
            """
            import pandas as pd

            def tabel_prioritas(df, kolom, progres, usaha):
                persen = df[kolom].mean() * 100
                t = pd.DataFrame({"persen": persen})
                t["skor"] = [persen[n] * progres[n] / usaha[n] for n in t.index]
                return t.sort_values("skor", ascending=False)
            """,
        ),
        E(
            "D11-03-3-ex3",
            "sedang",
            """
            Tulis fungsi `jumlah_tumpang_tindih(df, kolom)` yang mengembalikan banyak baris yang tercentang pada dua kolom kategori atau lebih (sebagai integer).
            """,
            """
            def jumlah_tumpang_tindih(df, kolom):
                # TODO: implementasikan
                pass
            """,
            """
            import pandas as pd
            df = pd.DataFrame({"a": [True, False, True, False], "b": [True, True, True, False], "c": [True, False, False, False]})
            assert jumlah_tumpang_tindih(df, ["a", "b", "c"]) == 2
            assert jumlah_tumpang_tindih(df, ["a", "c"]) == 1
            assert isinstance(jumlah_tumpang_tindih(df, ["a", "b"]), int)
            """,
            "Jumlahkan kolom per baris dengan df[kolom].sum(axis=1), lalu hitung baris dengan jumlah >= 2.",
            """
            def jumlah_tumpang_tindih(df, kolom):
                return int((df[kolom].sum(axis=1) >= 2).sum())
            """,
        ),
        E(
            "D11-03-3-ex4",
            "menantang",
            """
            Tulis fungsi `tambah_kategori(df, nama, indeks)` yang mengembalikan DataFrame baru dengan kolom boolean `nama`, bernilai `True` pada baris dengan posisi (nomor baris, bukan label) yang ada di `indeks` dan `False` selainnya. DataFrame asli tidak boleh berubah.
            """,
            """
            import pandas as pd

            def tambah_kategori(df, nama, indeks):
                # TODO: implementasikan
                pass
            """,
            """
            import pandas as pd
            df = pd.DataFrame({"a": [True, False, False, False]}, index=[10, 20, 30, 40])
            baru = tambah_kategori(df, "ig", [1, 3])
            assert list(baru["ig"]) == [False, True, False, True]
            assert baru["ig"].dtype == bool
            assert "ig" not in df.columns
            assert list(baru.index) == [10, 20, 30, 40]
            kosong = tambah_kategori(df, "x", [])
            assert not kosong["x"].any()
            """,
            "Salin DataFrame dengan df.copy(). Buat list boolean dengan i in set(indeks) untuk setiap posisi i lalu pasang sebagai kolom.",
            """
            import pandas as pd

            def tambah_kategori(df, nama, indeks):
                baru = df.copy()
                pos = set(indeks)
                baru[nama] = [i in pos for i in range(len(baru))]
                return baru
            """,
        ),
    ],
    [
        M(
            "Mengira persentase kategori harus berjumlah 100 persen.",
            "Satu contoh boleh punya banyak kategori, jadi total persentase bisa melebihi 100 persen.",
        ),
        M(
            "Menetapkan kategori di awal lalu tidak pernah mengubahnya.",
            "Tambah kategori baru saat kamu menemukannya dan tinjau ulang contoh lama.",
        ),
        M(
            "Memilih proyek hanya dari persentase terbesar.",
            "Pertimbangkan juga kemajuan yang diharapkan dan usaha yang dibutuhkan.",
        ),
    ],
    [
        Q(
            "Mengapa total persentase kategori di tabel error analysis bisa lebih dari 100 persen?",
            ["Karena ada kesalahan hitung", "Karena satu contoh bisa masuk lebih dari satu kategori", "Karena sampel terlalu kecil", "Karena dev set bocor"],
            1,
            "Tiap persentase menyatakan bagian kesalahan yang tersentuh oleh kategori itu, dan kategori boleh tumpang tindih.",
        ),
        Q(
            "Anjing 8 persen, kucing besar 43 persen, buram 61 persen. Proyek mana yang menyentuh error paling banyak?",
            ["Anjing", "Kucing besar", "Buram", "Semua sama"],
            2,
            "Buram menyentuh 61 persen kesalahan, tertinggi di tabel.",
        ),
        Q(
            "Kapan menambah kategori baru ke tabel?",
            ["Tidak boleh setelah dimulai", "Saat menemukan pola baru ketika memeriksa contoh", "Hanya di akhir proyek", "Hanya jika ada GPU"],
            1,
            "Error analysis iteratif. Kategori baru yang muncul dipakai lalu contoh lama diperiksa ulang.",
        ),
        Q(
            "Kategori mana yang paling berguna ditambahkan?",
            ["Yang paling jarang muncul", "Yang kamu punya ide perbaikannya", "Yang paling rumit", "Yang tidak punya komentar"],
            1,
            "Kategori yang punya ide perbaikan langsung bisa diubah menjadi proyek.",
        ),
        Q(
            "Apa peran skor prioritas dari persen, kemajuan, dan usaha?",
            ["Menggantikan semua penilaian", "Memandu diskusi dengan menuliskan asumsi", "Menentukan akurasi final", "Mengganti test set"],
            1,
            "Skor adalah heuristik yang memaksa tim menuliskan asumsi, bukan kebenaran mutlak.",
        ),
    ],
    [
        "Satu tabel error analysis mengevaluasi banyak ide secara paralel.",
        "Satu contoh boleh punya banyak kategori sehingga total persentase boleh melebihi 100 persen.",
        "Kategori baru muncul saat kamu memeriksa contoh, dan proses ini iteratif.",
        "Gabungkan persen, kemajuan yang diharapkan, dan usaha untuk menyusun prioritas.",
    ],
    ["Machine Learning Yearning, bab 15 (Andrew Ng): evaluasi beberapa ide secara paralel saat error analysis"],
)

video = {
    "needed": False,
    "kind": "none",
    "reason": "Isi modul berupa kode dan tabel yang cukup jelas dalam teks dan latihan.",
    "brief": [],
}

write_module(
    "D11",
    3,
    "Sistem pertama dan error analysis dasar",
    105,
    [
        "Membangun sistem dasar dengan cepat dan membaca petunjuk dari baseline",
        "Melakukan error analysis dan menghitung batas atas manfaat tiap proyek",
        "Menyusun tabel error analysis multi-kategori dan menurunkannya menjadi prioritas",
    ],
    [l1, l2, l3],
    video,
    REF,
)
