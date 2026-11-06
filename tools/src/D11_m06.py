import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, C, E, Q, M, lesson, write_module

REF = [{"book": "Machine Learning Yearning (Andrew Ng)", "chapters": "bab 28 sampai 35"}]

DATA = """
import numpy as np
import warnings
warnings.simplefilter("ignore")

def data(m, seed):
    r = np.random.default_rng(seed)
    x = r.uniform(0, 1, m)
    y = np.sin(2 * np.pi * x) + 0.3 * r.normal(size=m)
    return x, y

def kurva(derajat, ukuran, seeds=range(15)):
    xd, yd = data(4000, 999)
    tr_all, dv_all = [], []
    for m in ukuran:
        tr, dv = [], []
        for s in seeds:
            x, y = data(m, s)
            c = np.polyfit(x, y, derajat)
            tr.append(np.mean((np.polyval(c, x) - y) ** 2))
            dv.append(np.mean((np.polyval(c, xd) - yd) ** 2))
        tr_all.append(float(np.mean(tr)))
        dv_all.append(float(np.median(dv)))
    return tr_all, dv_all

OPTIMAL = 0.09
"""

l1 = lesson(
    "D11-06-1",
    "Learning curve untuk mendiagnosis bias dan variance",
    35,
    [
        "Membaca learning curve error dev dan error training terhadap ukuran data",
        "Mengenali pola high bias dan high variance dari bentuk kurva",
        "Memutuskan apakah menambah data layak dilakukan",
        "Memperkirakan ukuran data yang dibutuhkan untuk mencapai target error",
    ],
    [
        T("""
        ## Grafik yang menjawab dua pertanyaan

        Di lesson sebelumnya kamu membaca bias dan variance dari dua angka. Learning curve memperluasnya menjadi sebuah grafik: error dev (dan error training) sebagai fungsi ukuran training set. Dari bentuknya, kamu bisa menjawab dua pertanyaan penting. Apakah menambah data akan membantu? Dan di sisi mana model sedang berada, bias atau variance?

        Cara membuatnya: latih model pada 100 contoh, lalu 200, 400, dan seterusnya, ukur error dev dan error training pada tiap ukuran. Plot keduanya terhadap ukuran data. Tambahkan garis horizontal untuk error yang kamu inginkan atau error optimal sebagai pembanding.

        Dua pola umum terlihat dari arah kedua kurva. Error dev umumnya turun seiring data bertambah karena model mengenali pola yang lebih umum. Error training umumnya naik seiring data bertambah karena makin sulit menghafal banyak contoh. Kedua kurva mendekat satu sama lain. Pertanyaannya adalah ke mana mereka mendekat.
        """),
        T("""
        ## Pola high bias

        Pada masalah bias tinggi, kedua kurva mendatar di nilai tinggi, jauh di atas error yang diinginkan, dan celah antara keduanya kecil. Model terlalu sederhana: bahkan pada training set sendiri ia tidak cukup baik. Memperkirakan berapa data tambahan membantu mudah: tidak banyak, karena kurva sudah mendatar.

        Pada model polinomial derajat 1 untuk data sinus, error training sekitar 0,28 dan error dev sekitar 0,29, dan keduanya hampir tidak bergerak antara 120 dan 960 contoh. Garis error optimal 0,09 jauh di bawah. Menambah data sepuluh kali lipat tidak mengubah apa pun. Tindakan yang relevan adalah memperbesar model atau menambah fitur.

        Pelajaran khusus: kamu bisa mengetahui ini dengan ekstrapolasi murah dari kurva, tanpa mengumpulkan data baru. Itulah nilai learning curve: ia menghemat biaya pengumpulan data yang tidak akan berguna.
        """),
        T("""
        ## Pola high variance dan kombinasi

        Pada masalah variance tinggi, error training rendah sedangkan error dev jauh lebih tinggi, dan celahnya besar. Seiring data bertambah, error dev turun dan error training naik sehingga celah menutup. Polinomial derajat 9 memperlihatkannya: pada 30 contoh error dev jauh di atas error training, pada 480 contoh keduanya hampir sama di sekitar 0,09. Menambah data membantu, dan kurva memberi petunjuk seberapa banyak.

        Kasus gabungan, bias dan variance sama-sama tinggi, tampak sebagai error training yang jauh di atas error optimal sekaligus celah yang lebar. Di sini, kurva dev turun saat data bertambah, tetapi tetap tidak sampai target karena ada komponen bias. Jangan berharap data saja menyelesaikan; kamu perlu menurunkan bias juga.

        Satu kasus lagi: kedua kurva mendatar rendah dan berdekatan di dekat error optimal. Itu tanda sistem sudah baik, dan investasi tambahan memberi hasil kecil.
        """),
        T("""
        ## Memperkirakan data yang dibutuhkan

        Karena kurva dev biasanya turun halus, kamu dapat memperkirakan ukuran data untuk mencapai target tertentu dengan interpolasi pada skala log ukuran data. Misalnya error dev 0,30 pada 100 contoh, 0,20 pada 200, dan 0,10 pada 400. Target 0,15 berada di antara 200 dan 400, tepat di tengah pada skala log, sehingga perkiraannya sekitar 283 contoh.

        Perkiraan ini kasar. Kurva sebenarnya melandai dan mungkin tidak pernah mencapai target bila ada bias. Karena itu, periksa dulu apakah kurva training ikut mendekat ke target. Bila kedua kurva mendatar di atas target, jawabannya bukan lebih banyak data, melainkan perubahan model.
        """),
        T("""
        ## Alur membaca kurva dalam lima langkah

        Agar pembacaan konsisten, ikuti alur tetap. Langkah satu: tentukan error yang kamu inginkan dan gambar sebagai garis horizontal. Langkah dua: lihat kurva training. Jika di titik terakhir ia masih jauh di atas garis, tandai bias. Langkah tiga: lihat celah antara dev dan training di titik terakhir. Jika lebar, tandai variance. Langkah empat: lihat kemiringan kurva dev pada beberapa titik terakhir. Jika masih menurun jelas, data tambahan akan membantu. Langkah lima: tulis satu kalimat keputusan, misalnya "bias dominan, perbesar model sebelum mengumpulkan data".

        Kebiasaan menulis kalimat keputusan itu penting. Ia memaksamu menghubungkan grafik dengan tindakan, dan memberi catatan yang bisa dibaca rekan tim minggu depan. Grafik tanpa keputusan hanyalah dekorasi.
        """),
        K(
            "tip",
            """
            Gambar garis error yang diinginkan di grafik. Garis itu membuat keputusan hampir otomatis: jika kurva training sendiri tidak menyentuh garis, kamu punya masalah bias.
            """,
        ),
        C(
            DATA
            + """
ukuran = [30, 60, 120, 240, 480, 960]
tr, dv = kurva(1, ukuran)
print("derajat 1 (bias tinggi)")
for m, a, b in zip(ukuran, tr, dv):
    print(f"{m:5d}  train {a:.3f}  dev {b:.3f}  celah {b - a:.3f}")
""",
            """
            train sekitar 0.26 sampai 0.29 dan dev sekitar 0.29 sampai 0.30
            celah kecil dan hampir mendatar
            """,
            """
            Kedua kurva mendatar jauh di atas error optimal 0,09 dan celahnya kecil. Menambah data tidak menolong. Ini bias murni.
            """,
        ),
        C(
            DATA
            + """
ukuran = [30, 60, 120, 240, 480, 960]
tr, dv = kurva(9, ukuran)
print("derajat 9 (variance tinggi)")
for m, a, b in zip(ukuran, tr, dv):
    print(f"{m:5d}  train {a:.3f}  dev {b:.3f}  celah {b - a:.3f}")
""",
            """
            dev turun dari sekitar 0.14 ke sekitar 0.09
            train naik dari sekitar 0.05 ke sekitar 0.09
            celah menutup mendekati nol
            """,
            """
            Error dev turun dan error training naik hingga bertemu di sekitar error optimal. Ini variance yang disembuhkan data. Kurva jenis ini yang membuat penambahan data layak diusahakan.
            """,
        ),
        C(
            """
import math

def ukuran_perkiraan(ukuran, err, target):
    for i in range(len(ukuran) - 1):
        a, b = err[i], err[i + 1]
        if a >= target >= b and a != b:
            f = (a - target) / (a - b)
            return round(ukuran[i] * (ukuran[i + 1] / ukuran[i]) ** f)
    return None

print(ukuran_perkiraan([100, 200, 400], [0.30, 0.20, 0.10], 0.15))
print(ukuran_perkiraan([100, 200, 400], [0.30, 0.20, 0.18], 0.10))
""",
            """
            283
            None
            """,
            """
            Interpolasi pada skala log memberi ukuran sekitar 283 untuk target 0,15. Bila kurva tidak pernah menyentuh target dalam rentang yang diamati, fungsi mengembalikan None dan kamu harus curiga ada masalah bias.
            """,
        ),
        E(
            "D11-06-1-ex1",
            "mudah",
            """
            Tulis fungsi `ringkas_kurva(err_train, err_dev, optimal, toleransi)` yang menilai titik terakhir kurva. `bias = err_train[-1] - optimal`, `var = err_dev[-1] - err_train[-1]`, keduanya dibulatkan 4 desimal. Kembalikan `"keduanya"` bila keduanya lebih besar dari `toleransi`, `"bias"` bila hanya bias, `"variance"` bila hanya variance, dan `"baik"` selainnya.
            """,
            """
            def ringkas_kurva(err_train, err_dev, optimal, toleransi):
                # TODO: implementasikan
                pass
            """,
            """
            assert ringkas_kurva([0.2, 0.27], [0.4, 0.29], 0.09, 0.03) == "bias"
            assert ringkas_kurva([0.02, 0.05], [0.5, 0.2], 0.04, 0.03) == "variance"
            assert ringkas_kurva([0.2, 0.25], [0.5, 0.40], 0.09, 0.03) == "keduanya"
            assert ringkas_kurva([0.08, 0.09], [0.12, 0.10], 0.09, 0.03) == "baik"
            """,
            "Gunakan elemen terakhir dari kedua list dan perbandingan strict greater.",
            """
            def ringkas_kurva(err_train, err_dev, optimal, toleransi):
                b = round(err_train[-1] - optimal, 4)
                v = round(err_dev[-1] - err_train[-1], 4)
                if b > toleransi and v > toleransi:
                    return "keduanya"
                if b > toleransi:
                    return "bias"
                if v > toleransi:
                    return "variance"
                return "baik"
            """,
        ),
        E(
            "D11-06-1-ex2",
            "sedang",
            """
            Tulis fungsi `data_membantu(err_dev, ambang)` yang mengembalikan `True` bila penurunan error dev pada tiga titik terakhir (`err_dev[-3] - err_dev[-1]`, dibulatkan 6 desimal) lebih besar dari `ambang`. Jika list kurang dari 3 elemen kembalikan `False`.
            """,
            """
            def data_membantu(err_dev, ambang):
                # TODO: implementasikan
                pass
            """,
            """
            assert data_membantu([0.4, 0.3, 0.2, 0.15], 0.03) is True
            assert data_membantu([0.4, 0.3, 0.29, 0.288], 0.03) is False
            assert data_membantu([0.3, 0.2], 0.01) is False
            assert data_membantu([0.3, 0.25, 0.22], 0.08) is False
            """,
            "Cek panjang list dulu, lalu hitung err_dev[-3] - err_dev[-1].",
            """
            def data_membantu(err_dev, ambang):
                if len(err_dev) < 3:
                    return False
                return bool(round(err_dev[-3] - err_dev[-1], 6) > ambang)
            """,
        ),
        E(
            "D11-06-1-ex3",
            "sedang",
            """
            Tulis fungsi `kurva_poli(derajat, ukuran, seeds)` yang untuk tiap ukuran melatih `np.polyfit` pada data `x ~ U(0,1)`, `y = sin(2*pi*x) + 0.3*N(0,1)` untuk tiap seed (urutan `x = r.uniform(0, 1, m)` lalu `y = ...` dengan `r = np.random.default_rng(seed)`). Dev set tetap: `data(4000, 999)`. Kembalikan `(train, dev)` dua list: rata-rata MSE training dan median MSE dev atas seed untuk tiap ukuran, dibulatkan 4 desimal.
            """,
            """
            import numpy as np
            import warnings
            warnings.simplefilter("ignore")

            def kurva_poli(derajat, ukuran, seeds):
                # TODO: implementasikan
                pass
            """,
            """
            tr1, dv1 = kurva_poli(1, [60, 240], range(8))
            tr9, dv9 = kurva_poli(9, [30, 240], range(8))
            assert len(tr1) == 2 and len(dv9) == 2
            assert dv1[1] > 0.2
            assert tr1[1] > 0.2
            assert dv9[0] > dv9[1]
            assert tr9[0] < tr9[1]
            assert abs(dv9[1] - 0.09) < 0.02
            """,
            "Bangun fungsi pembangkit data lokal. Hitung train untuk setiap seed lalu np.mean, dan dev lalu np.median.",
            """
            import numpy as np
            import warnings
            warnings.simplefilter("ignore")

            def _data(m, seed):
                r = np.random.default_rng(seed)
                x = r.uniform(0, 1, m)
                y = np.sin(2 * np.pi * x) + 0.3 * r.normal(size=m)
                return x, y

            def kurva_poli(derajat, ukuran, seeds):
                xd, yd = _data(4000, 999)
                train, dev = [], []
                for m in ukuran:
                    tr, dv = [], []
                    for s in seeds:
                        x, y = _data(m, s)
                        c = np.polyfit(x, y, derajat)
                        tr.append(np.mean((np.polyval(c, x) - y) ** 2))
                        dv.append(np.mean((np.polyval(c, xd) - yd) ** 2))
                    train.append(round(float(np.mean(tr)), 4))
                    dev.append(round(float(np.median(dv)), 4))
                return train, dev
            """,
        ),
        E(
            "D11-06-1-ex4",
            "menantang",
            """
            Tulis fungsi `ukuran_perkiraan(ukuran, err, target)`. Telusuri pasangan titik berurutan `i`, `i+1`. Pada pasangan pertama dengan `err[i] >= target >= err[i+1]` dan `err[i] != err[i+1]`, hitung `f = (err[i] - target) / (err[i] - err[i+1])` dan kembalikan `round(ukuran[i] * (ukuran[i+1] / ukuran[i]) ** f)` sebagai integer. Jika tidak ada pasangan seperti itu kembalikan `None`.
            """,
            """
            def ukuran_perkiraan(ukuran, err, target):
                # TODO: implementasikan
                pass
            """,
            """
            assert ukuran_perkiraan([100, 200, 400], [0.30, 0.20, 0.10], 0.15) == 283
            assert ukuran_perkiraan([100, 200, 400], [0.30, 0.20, 0.18], 0.10) is None
            assert ukuran_perkiraan([100, 200, 400], [0.30, 0.20, 0.10], 0.20) == 200
            assert ukuran_perkiraan([100, 200], [0.3, 0.3], 0.3) is None
            assert isinstance(ukuran_perkiraan([100, 200, 400], [0.30, 0.20, 0.10], 0.15), int)
            """,
            "Pasangan dengan err sama dilewati. Target 0.20 cocok pada pasangan pertama dengan f = 1 sehingga menghasilkan 200.",
            """
            def ukuran_perkiraan(ukuran, err, target):
                for i in range(len(ukuran) - 1):
                    a, b = err[i], err[i + 1]
                    if a >= target >= b and a != b:
                        f = (a - target) / (a - b)
                        return int(round(ukuran[i] * (ukuran[i + 1] / ukuran[i]) ** f))
                return None
            """,
        ),
    ],
    [
        M(
            "Menambah data karena error dev tinggi tanpa melihat bentuk kurva.",
            "Plot learning curve dulu dan lihat apakah kurva training dan dev sudah mendatar.",
        ),
        M(
            "Hanya memplot error dev.",
            "Plot error training juga untuk membaca celah dan posisi terhadap error optimal.",
        ),
        M(
            "Mengekstrapolasi kurva yang mendatar di atas target seolah akan terus turun.",
            "Jika kedua kurva mendatar di atas target, masalahnya bias dan data bukan obatnya.",
        ),
    ],
    [
        Q(
            "Kedua kurva mendatar tinggi dan berdekatan. Diagnosisnya?",
            ["Variance tinggi", "Bias tinggi", "Sudah optimal", "Dev set bocor"],
            1,
            "Kurva yang mendatar di atas target dengan celah kecil adalah ciri bias tinggi.",
        ),
        Q(
            "Error training rendah, dev tinggi, celah menutup saat data bertambah. Apa yang bermanfaat?",
            ["Tambah data", "Perkecil fitur dan data", "Ganti metrik", "Kurangi layer"],
            0,
            "Celah yang menutup oleh data menandakan variance yang bisa dibantu data.",
        ),
        Q(
            "Mengapa error training umumnya naik saat data bertambah?",
            ["Karena label berubah", "Karena makin sulit menghafal banyak contoh", "Karena model mengecil", "Karena dev set naik"],
            1,
            "Dengan contoh lebih banyak model tidak bisa menyesuaikan diri sempurna pada semuanya.",
        ),
        Q(
            "Untuk apa garis error yang diinginkan pada grafik?",
            ["Hiasan", "Membantu melihat apakah training sendiri sudah mencapai target", "Mengukur dev", "Menghapus derau"],
            1,
            "Jika kurva training tidak menyentuh garis target, bias adalah masalahnya.",
        ),
        Q(
            "Error dev 0,30 pada 100 contoh, 0,20 pada 200, 0,10 pada 400. Perkiraan data untuk 0,15?",
            ["Sekitar 150", "Sekitar 283", "Sekitar 400", "Tidak mungkin"],
            1,
            "Interpolasi log antara 200 dan 400 di tengah menghasilkan sekitar 283.",
        ),
    ],
    [
        "Learning curve memplot error training dan dev terhadap ukuran data.",
        "Bias tinggi: kurva mendatar tinggi dan berdekatan, data tidak membantu.",
        "Variance tinggi: celah besar yang menutup dengan bertambahnya data.",
        "Interpolasi pada skala log ukuran data memberi perkiraan kasar kebutuhan data.",
    ],
    ["Machine Learning Yearning, bab 28 sampai 31 (Andrew Ng): diagnosis dengan learning curve"],
)

l2 = lesson(
    "D11-06-2",
    "Memetakan learning curve dengan benar",
    35,
    [
        "Memilih ukuran subset yang menghemat biaya namun informatif",
        "Merata-ratakan beberapa percobaan agar kurva tidak berderau",
        "Menjaga proporsi kelas pada subset yang diambil",
        "Melaporkan ketidakpastian kurva dengan standard error",
    ],
    [
        T("""
        ## Kurva yang berderau menyesatkan

        Pada praktiknya, learning curve jarang semulus gambar di buku. Ketika ukuran training set kecil, subset yang kebetulan diambil sangat memengaruhi hasil. Dua subset 100 contoh bisa menghasilkan error dev yang berbeda 5 poin hanya karena contoh mana yang terpilih. Kurva dari satu percobaan bisa naik turun tidak beraturan, dan kamu bisa salah membaca derau itu sebagai pola.

        Cara menanganinya adalah mengambil beberapa subset acak berbeda pada tiap ukuran, melatih model pada masing-masing, lalu merata-ratakan error. Rata-rata dari lima sampai sepuluh percobaan biasanya cukup menenangkan kurva, terutama pada ukuran kecil. Untuk ukuran besar, derau sudah kecil sehingga satu percobaan sering memadai.

        Dengan rata-rata, tambahkan juga ukuran ketidakpastiannya. Standard error dari rata-rata sama dengan simpangan baku antar percobaan dibagi akar jumlah percobaan. Jika dua kurva berbeda lebih kecil dari standard error-nya, perbedaan itu belum tentu nyata.
        """),
        T("""
        ## Menghemat biaya dengan ukuran geometrik

        Melatih model berkali-kali bisa mahal, terutama pada jaringan besar. Kamu tidak perlu memeriksa setiap ukuran dari 1 sampai N. Pilih ukuran yang tumbuh secara geometrik, misalnya 1.000, 2.000, 4.000, 8.000, dan seterusnya, atau 100, 300, 1.000, 3.000. Alasannya, perubahan error terhadap data biasanya bermakna pada skala kali lipat, bukan skala tambahan konstan. Tujuh sampai sepuluh titik sudah cukup untuk melihat bentuk.

        Jika pelatihan memakan waktu lama, mulai dengan ukuran kecil dulu. Kurva dari subset kecil sudah bisa mengungkap pola bias, dan jika itu terlihat, kamu bisa berhenti sebelum membuang waktu pada ukuran besar. Hanya jika kurvanya menjanjikan, lanjutkan ke ukuran lebih besar.

        Satu perincian yang sering terlewat: error training pada learning curve dihitung pada subset yang dipakai melatih, bukan pada seluruh training set. Jika kamu menghitung error training pada seluruh data, kurva training akan salah karena sebagian data tidak pernah dilihat model.
        """),
        T("""
        ## Menjaga proporsi kelas

        Jika data tidak seimbang, misalnya 5 persen positif, subset acak kecil bisa tidak memuat satu pun contoh positif atau memuat jauh lebih banyak dari proporsi sebenarnya. Hasilnya error dev yang aneh dan tidak mewakili apa pun. Ng menyarankan memastikan subset punya proporsi kelas yang sama dengan training set penuh, atau setidaknya bahwa tiap kelas terwakili.

        Praktik sederhana adalah stratified sampling: ambil sampel acak dari tiap kelas dengan fraksi yang sama. Pada data 1.000 contoh dengan 50 positif, subset 100 contoh akan memuat 5 positif dan 95 negatif. Dengan begitu variasi antar percobaan berkurang dan kurva lebih stabil.

        Untuk data yang sangat tidak seimbang, pertimbangkan metrik yang tidak mudah ditipu oleh kelas mayoritas, topik yang dibahas di modul awal. Learning curve dengan akurasi pada data 95 persen negatif hampir selalu mendatar di 95 persen tanpa memberi informasi.
        """),
        T("""
        ## Kesalahan umum

        Ada beberapa jebakan lain. Jangan mengubah hyperparameter di antara ukuran: jika regularisasi diubah untuk tiap ukuran, kurva mengukur dua hal sekaligus. Jangan memakai dev set yang berbeda per ukuran. Jangan mengacak ulang dev set antar percobaan. Gunakan dev set tetap yang sama untuk semua titik agar perbandingan adil.

        Hati-hati juga dengan model yang lambat konvergen. Jika kamu menghentikan pelatihan pada jumlah epoch tetap, ukuran kecil bisa mendapat terlalu banyak langkah per contoh dan ukuran besar terlalu sedikit. Tetapkan kriteria berhenti berdasarkan konvergensi, bukan epoch tetap, atau sesuaikan jumlah langkah.
        """),
        T("""
        ## Seberapa banyak percobaan cukup

        Jumlah percobaan yang pantas bergantung pada seberapa berderau modelmu. Model linear yang deterministik dengan data besar hampir tidak berderau antar subset, sehingga tiga percobaan cukup. Jaringan saraf yang dilatih dari inisialisasi acak berderau dari dua sumber sekaligus, subset dan inisialisasi, sehingga lima sampai sepuluh percobaan lebih aman. Aturan praktis: tambah percobaan hingga standard error pada ukuran terkecil lebih kecil dari beda yang ingin kamu bedakan.

        Bila biaya sangat mahal, kurangi jumlah ukuran sebelum mengurangi jumlah percobaan. Lima ukuran dengan lima percobaan lebih berguna daripada sepuluh ukuran dengan satu percobaan, karena kurva yang berderau tidak bisa dipercaya berapa pun jumlah titiknya.
        """),
        K(
            "note",
            """
            Grafik learning curve adalah alat diagnosis, bukan laporan hasil akhir. Jangan menghabiskan berhari-hari mempercantiknya. Tujuh titik dari lima percobaan sudah memberi jawaban.
            """,
        ),
        C(
            """
import math

def ukuran_geometrik(n_min, n_max, faktor):
    hasil = []
    n = n_min
    while n <= n_max:
        hasil.append(int(round(n)))
        n *= faktor
    return hasil

print(ukuran_geometrik(100, 6400, 2))
print(ukuran_geometrik(100, 10000, 3))
""",
            """
            [100, 200, 400, 800, 1600, 3200, 6400]
            [100, 300, 900, 2700, 8100]
            """,
            """
            Ukuran yang tumbuh geometrik menutup rentang luas dengan sedikit titik. Tujuh titik dari 100 sampai 6400 sudah menunjukkan bentuk kurva.
            """,
        ),
        C(
            """
import numpy as np
from sklearn.datasets import make_moons
from sklearn.linear_model import LogisticRegression

X, y = make_moons(n_samples=12000, noise=0.35, random_state=0)
Xd, yd = X[-4000:], y[-4000:]
Xp, yp = X[:8000], y[:8000]
ukuran = [20, 40, 80, 160, 320, 640]
satu, rata = [], []
for m in ukuran:
    errs = []
    for s in range(10):
        idx = np.random.default_rng(s).choice(len(Xp), m, replace=False)
        errs.append(1 - LogisticRegression().fit(Xp[idx], yp[idx]).score(Xd, yd))
    satu.append(errs[0])
    rata.append(float(np.mean(errs)))
print("m    satu percobaan   rata-rata 10")
for m, a, b in zip(ukuran, satu, rata):
    print(f"{m:4d}  {a:13.3f}   {b:12.3f}")
""",
            """
            kolom satu percobaan lebih berderau daripada rata-rata
            rata-rata turun lebih halus dari sekitar 0.20 ke sekitar 0.155
            """,
            """
            Satu percobaan pada ukuran kecil memberi angka yang meloncat. Rata-rata sepuluh percobaan jauh lebih stabil dan mudah dibaca.
            """,
        ),
        C(
            """
import numpy as np

rng = np.random.default_rng(0)
y = (rng.random(1000) < 0.05).astype(int)

def sampel_stratifikasi(y, n, seed):
    r = np.random.default_rng(seed)
    idx = []
    for kelas in np.unique(y):
        pos = np.where(y == kelas)[0]
        k = max(1, int(round(n * len(pos) / len(y))))
        idx.extend(r.choice(pos, k, replace=False))
    return np.sort(np.array(idx))

s = sampel_stratifikasi(y, 100, 0)
print("ukuran:", len(s), "positif:", int(y[s].sum()), "proporsi asli:", round(float(y.mean()), 3))
""",
            """
            ukuran: 100 positif: 4 proporsi asli: 0.045
            """,
            """
            Sampel stratifikasi mempertahankan proporsi kelas sehingga subset kecil tetap mewakili. Tiap kelas minimal mendapat satu contoh.
            """,
        ),
        E(
            "D11-06-2-ex1",
            "mudah",
            """
            Tulis fungsi `ukuran_geometrik(n_min, n_max, faktor)` yang mengembalikan list integer `n_min`, `n_min * faktor`, dan seterusnya (dibulatkan) selama nilainya tidak melebihi `n_max`.
            """,
            """
            def ukuran_geometrik(n_min, n_max, faktor):
                # TODO: implementasikan
                pass
            """,
            """
            assert ukuran_geometrik(100, 6400, 2) == [100, 200, 400, 800, 1600, 3200, 6400]
            assert ukuran_geometrik(100, 10000, 3) == [100, 300, 900, 2700, 8100]
            assert ukuran_geometrik(50, 40, 2) == []
            assert ukuran_geometrik(10, 10, 2) == [10]
            """,
            "Gunakan loop while dengan variabel n yang dikali faktor tiap putaran.",
            """
            def ukuran_geometrik(n_min, n_max, faktor):
                hasil = []
                n = n_min
                while n <= n_max:
                    hasil.append(int(round(n)))
                    n *= faktor
                return hasil
            """,
        ),
        E(
            "D11-06-2-ex2",
            "sedang",
            """
            Tulis fungsi `ringkas_runs(runs)`. `runs` adalah list berisi `k` list error dengan panjang sama (satu list per percobaan). Kembalikan list tuple `(rata, sem)` per titik, dengan `rata` rata-rata, `sem` standard error `std(ddof=1) / sqrt(k)`, keduanya dibulatkan 4 desimal. Jika `k == 1`, `sem` adalah `0.0`.
            """,
            """
            import numpy as np

            def ringkas_runs(runs):
                # TODO: implementasikan
                pass
            """,
            """
            r = ringkas_runs([[0.30, 0.20], [0.34, 0.22], [0.32, 0.18]])
            assert r[0][0] == 0.32 and r[1][0] == 0.2
            assert abs(r[0][1] - 0.0115) < 1e-4
            assert abs(r[1][1] - 0.0115) < 1e-4
            assert ringkas_runs([[0.3, 0.2]]) == [(0.3, 0.0), (0.2, 0.0)]
            """,
            "Ubah ke array dengan np.array(runs), lalu hitung mean dan std dengan ddof=1 sepanjang axis 0.",
            """
            import numpy as np

            def ringkas_runs(runs):
                a = np.array(runs, dtype=float)
                k = a.shape[0]
                rata = a.mean(axis=0)
                if k == 1:
                    sem = np.zeros(a.shape[1])
                else:
                    sem = a.std(axis=0, ddof=1) / np.sqrt(k)
                return [(round(float(r), 4), round(float(s), 4)) for r, s in zip(rata, sem)]
            """,
        ),
        E(
            "D11-06-2-ex3",
            "sedang",
            """
            Tulis fungsi `sampel_stratifikasi(y, n, seed)` yang mengembalikan array indeks terurut. Untuk tiap kelas (urutan `np.unique`) ambil `k = max(1, round(n * jumlah_kelas / len(y)))` indeks acak tanpa pengembalian dari kelas itu memakai `rng = np.random.default_rng(seed)` dan `rng.choice`. Gabungkan lalu urutkan dengan `np.sort`.
            """,
            """
            import numpy as np

            def sampel_stratifikasi(y, n, seed):
                # TODO: implementasikan
                pass
            """,
            """
            import numpy as np
            y = np.array([0] * 95 + [1] * 5)
            s = sampel_stratifikasi(y, 20, 0)
            assert len(s) == 20
            assert int(y[s].sum()) == 1
            assert list(s) == sorted(s)
            assert len(set(s)) == len(s)
            s2 = sampel_stratifikasi(y, 4, 0)
            assert int(y[s2].sum()) >= 1
            assert list(sampel_stratifikasi(y, 20, 0)) == list(s)
            """,
            "Kelas langka pada n kecil harus tetap mendapat minimal satu contoh lewat max(1, ...).",
            """
            import numpy as np

            def sampel_stratifikasi(y, n, seed):
                y = np.asarray(y)
                rng = np.random.default_rng(seed)
                idx = []
                for kelas in np.unique(y):
                    pos = np.where(y == kelas)[0]
                    k = max(1, int(round(n * len(pos) / len(y))))
                    idx.extend(rng.choice(pos, k, replace=False))
                return np.sort(np.array(idx))
            """,
        ),
        E(
            "D11-06-2-ex4",
            "menantang",
            """
            Tulis fungsi `kurva_rata(Xp, yp, Xd, yd, ukuran, k)` yang mengembalikan list rata-rata error dev (1 dikurangi akurasi) `LogisticRegression(max_iter=1000)` untuk tiap ukuran. Pada tiap ukuran, ulangi `k` kali: `idx = np.random.default_rng(s).choice(len(Xp), m, replace=False)` untuk `s` dari 0 sampai `k-1`, latih pada `Xp[idx], yp[idx]`. Kembalikan rata-rata dibulatkan 4 desimal.
            """,
            """
            import numpy as np
            from sklearn.linear_model import LogisticRegression

            def kurva_rata(Xp, yp, Xd, yd, ukuran, k):
                # TODO: implementasikan
                pass
            """,
            """
            from sklearn.datasets import make_moons
            X, y = make_moons(n_samples=3000, noise=0.3, random_state=0)
            r = kurva_rata(X[:2000], y[:2000], X[2000:], y[2000:], [20, 200, 1000], 3)
            assert len(r) == 3
            assert all(0 < v < 0.5 for v in r)
            assert r[0] >= r[2] - 0.02
            assert r == kurva_rata(X[:2000], y[:2000], X[2000:], y[2000:], [20, 200, 1000], 3)
            """,
            "Dua loop bersarang: ukuran di luar, seed di dalam. Hitung np.mean error tiap ukuran.",
            """
            import numpy as np
            from sklearn.linear_model import LogisticRegression

            def kurva_rata(Xp, yp, Xd, yd, ukuran, k):
                hasil = []
                for m in ukuran:
                    errs = []
                    for s in range(k):
                        idx = np.random.default_rng(s).choice(len(Xp), m, replace=False)
                        model = LogisticRegression(max_iter=1000).fit(Xp[idx], yp[idx])
                        errs.append(1 - model.score(Xd, yd))
                    hasil.append(round(float(np.mean(errs)), 4))
                return hasil
            """,
        ),
    ],
    [
        M(
            "Membaca satu percobaan sebagai bentuk kurva.",
            "Rata-ratakan beberapa subset acak terutama pada ukuran kecil.",
        ),
        M(
            "Menghitung error training pada seluruh training set untuk semua ukuran.",
            "Hitung error training pada subset yang dipakai melatih.",
        ),
        M(
            "Subset acak tanpa memperhatikan proporsi kelas.",
            "Gunakan sampel stratifikasi agar tiap kelas terwakili.",
        ),
    ],
    [
        Q(
            "Mengapa kurva dari satu percobaan pada ukuran kecil berderau?",
            ["Karena model tidak deterministik", "Karena subset yang terpilih sangat memengaruhi hasil", "Karena dev set berubah", "Karena metrik salah"],
            1,
            "Pada subset kecil, contoh mana yang terpilih membuat hasil bervariasi besar.",
        ),
        Q(
            "Mengapa ukuran geometrik (100, 200, 400, ...) dipilih?",
            ["Murah dan menangkap perubahan dalam skala kali lipat", "Mudah dihafal", "Wajib", "Menghilangkan bias"],
            0,
            "Error berubah bermakna pada skala kali lipat sehingga sedikit titik sudah cukup.",
        ),
        Q(
            "Data 5 persen positif. Subset acak 20 contoh. Risiko?",
            ["Tidak ada risiko", "Subset bisa tanpa contoh positif", "Pasti terlalu seimbang", "Model overfit"],
            1,
            "Dengan peluang 5 persen per contoh, 20 contoh bisa tidak memuat positif sama sekali.",
        ),
        Q(
            "Standard error rata-rata dari k percobaan dihitung sebagai?",
            ["std dikali akar k", "std dibagi akar k", "std dikali k", "std kuadrat"],
            1,
            "Standard error sama dengan simpangan baku dibagi akar jumlah percobaan.",
        ),
        Q(
            "Mengapa dev set harus tetap untuk semua titik kurva?",
            ["Agar perbandingan adil", "Agar lebih cepat", "Agar training naik", "Tidak penting"],
            0,
            "Dev set berbeda per titik mencampur perbedaan data dengan perbedaan ukuran training.",
        ),
    ],
    [
        "Rata-ratakan beberapa subset acak agar kurva tidak berderau.",
        "Pakai ukuran geometrik dengan sekitar tujuh sampai sepuluh titik.",
        "Jaga proporsi kelas dengan sampel stratifikasi.",
        "Dev set dan hyperparameter harus sama untuk semua titik.",
    ],
    ["Machine Learning Yearning, bab 32 (Andrew Ng): memplot learning curve dengan subset"],
)

l3 = lesson(
    "D11-06-3",
    "Performa manusia sebagai pembanding",
    35,
    [
        "Menjelaskan tiga alasan membandingkan sistem dengan performa manusia",
        "Mendefinisikan human-level dengan tim ahli terbaik sebagai perkiraan error optimal",
        "Menghitung avoidable bias dan variance terhadap acuan manusia",
        "Menjelaskan mengapa kemajuan melambat setelah melampaui manusia",
    ],
    [
        T("""
        ## Mengapa membandingkan dengan manusia

        Banyak sistem pembelajaran mesin dirancang untuk mengotomasi tugas yang bisa dilakukan manusia: mengenali gambar, transkripsi suara, membaca dokumen, menerjemahkan. Ada tiga alasan membandingkan dengan performa manusia.

        Pertama, **mudah mendapat label dari manusia**. Jika algoritmamu salah pada suatu contoh, kamu bisa meminta manusia memberi label dan melihat bagaimana manusia melakukannya. Itu membantu error analysis karena kamu bisa bertanya apa yang manusia lihat yang tidak dilihat model.

        Kedua, **error analysis bisa memakai intuisi manusia**. Jika manusia memahami contoh yang model gagal, kamu memperoleh ide fitur baru.

        Ketiga, **perkiraan error optimal**. Kamu bisa memakai performa manusia sebagai perkiraan error optimal. Tanpa acuan itu, kamu tidak tahu seberapa besar bagian error training yang tak terhindarkan. Ketiga alasan ini melemah ketika sistem melampaui manusia atau ketika tugasnya bukan tugas persepsi.
        """),
        T("""
        ## Mendefinisikan human-level

        Misalkan kamu membangun sistem membaca citra medis. Seorang dokter umum salah 3 persen. Seorang radiolog berpengalaman salah 1 persen. Tim radiolog yang berdiskusi salah 0,5 persen. Mana yang disebut human-level?

        Ng menyarankan memakai tingkat error terbaik yang bisa dicapai sekelompok ahli: 0,5 persen. Alasannya, tujuannya memperkirakan error optimal. Karena error optimal tidak mungkin lebih besar dari error tim terbaik, angka 0,5 persen adalah batas atas yang paling ketat. Memakai 3 persen akan membuat kamu mengira bias sudah hilang padahal masih ada banyak ruang.

        Namun kenyataan bisa menuntut kompromi. Tim ahli yang berdiskusi mahal dan sulit dikumpulkan untuk banyak contoh. Karena itu, definisikan sesuai tujuan: jika yang dicari perkiraan error optimal, pakai yang terbaik. Jika yang dicari target produk yang masuk akal, pakai tingkat dokter yang akan digantikan.
        """),
        T("""
        ## Membaca bias dan variance terhadap acuan manusia

        Dengan acuan manusia 0,5 persen, error training 5 persen, dan error dev 8 persen: avoidable bias 4,5 poin dan variance 3 poin. Bias dominan, jadi prioritas adalah model dan fitur. Dengan acuan yang sama tetapi error training 1 persen dan dev 8 persen: avoidable bias 0,5 poin dan variance 7 poin. Variance dominan, jadi data dan regularisasi.

        Perhatikan betapa acuan menentukan keputusan. Jika kamu memakai acuan dokter umum 3 persen, kasus kedua tampak bias negatif, yaitu training lebih baik dari manusia, dan kamu keliru menyimpulkan bahwa bias tidak ada. Sebaliknya, jika acuan terlalu rendah dari yang realistis, kamu mengejar bias yang sebenarnya tidak ada.

        Karena itu, catat dengan jelas bagaimana acuan manusia didefinisikan dan jangan mengubahnya diam-diam di tengah proyek.
        """),
        T("""
        ## Melampaui manusia

        Banyak tim menemukan kemajuan melambat setelah mencapai tingkat manusia. Ada beberapa alasan. Perkiraan error optimal tidak lagi jelas: apakah 0,3 persen sudah mendekati optimal atau masih jauh? Label dari manusia juga tidak lagi menjadi kebenaran yang bisa diandalkan, karena manusia sendiri salah lebih sering. Dan intuisi manusia tidak lagi menuntun fitur.

        Tetapi melampaui manusia bukan mustahil. Pada tugas dengan data terstruktur besar seperti rekomendasi iklan, prediksi lama perjalanan, atau skor kredit, mesin sudah lama lebih baik daripada manusia. Pada tugas persepsi, sistem terbaik juga melewati manusia untuk beberapa tugas sempit.

        Setelah titik ini, kamu perlu cara lain untuk mengukur kemajuan: dev set besar dan bersih, ukuran lebih halus, dan analisis oleh ahli yang lebih langka. Jangan memakai prosedur "tanya manusia kenapa" bila manusia tidak lebih baik dari sistemmu.
        """),
        T("""
        ## Menerapkan acuan dalam praktik tim

        Tuliskan acuan manusia di dokumen proyek pada hari pertama, lengkap dengan sumbernya. Misalnya "tim tiga radiolog dengan diskusi, error 0,5 persen pada 500 contoh". Catatan sumber itu penting karena angka acuan sendiri berasal dari sampel dan punya ketidakpastian. Acuan dari 50 contoh bisa meleset beberapa kali lipat dari acuan 5.000 contoh.

        Setelah itu, gunakan acuan sebagai bagian dari laporan mingguan: tampilkan error manusia, error training, dan error dev berdampingan. Tiga angka itu membuat diskusi tim berpusat pada bagian error yang masih bisa diperbaiki, dan menghindarkan perdebatan tentang model mana yang terasa lebih canggih.
        """),
        K(
            "note",
            """
            Human-level bukan angka tunggal. Selalu tulis siapa yang dimaksud: dokter umum, spesialis, atau tim ahli. Perbedaannya bisa beberapa kali lipat.
            """,
        ),
        C(
            """
manusia = {"dokter umum": 0.03, "radiolog": 0.01, "tim radiolog": 0.005}
acuan = min(manusia.values())
print("acuan human-level:", acuan)
for train, dev in [(0.05, 0.08), (0.01, 0.08)]:
    print(f"train {train}, dev {dev}: avoidable bias {train - acuan:.3f}, variance {dev - train:.3f}")
""",
            """
            acuan human-level: 0.005
            train 0.05, dev 0.08: avoidable bias 0.045, variance 0.030
            train 0.01, dev 0.08: avoidable bias 0.005, variance 0.070
            """,
            """
            Acuan diambil dari tim ahli terbaik. Skenario pertama bias dominan, skenario kedua variance dominan. Tanpa acuan yang tepat, kedua skenario sulit dibedakan arahnya.
            """,
        ),
        C(
            """
from math import comb

def error_voting(p, k):
    batas = k // 2 + 1
    return sum(comb(k, j) * p ** j * (1 - p) ** (k - j) for j in range(batas, k + 1))

for k in [1, 3, 5, 7]:
    print(f"{k} ahli independen dengan error 3 persen: error voting {error_voting(0.03, k):.6f}")
""",
            """
            1 ahli: 0.030000
            3 ahli: 0.002646
            5 ahli: 0.000258
            7 ahli: 0.000026
            """,
            """
            Jika kesalahan ahli saling independen, voting mayoritas menurunkan error dengan cepat. Kenyataannya ahli sering salah di kasus sulit yang sama, sehingga penurunan nyata lebih kecil. Ini sebabnya error tim bukan sekadar hitungan teoretis.
            """,
        ),
        C(
            """
def label_manusia_membantu(err_manusia, err_model):
    return err_manusia < err_model

print(label_manusia_membantu(0.01, 0.05))
print(label_manusia_membantu(0.01, 0.005))
""",
            """
            True
            False
            """,
            """
            Prosedur meminta manusia memberi label dan menjelaskan hanya bermanfaat selama manusia lebih baik dari model. Begitu model lebih baik, wawasan manusia tidak lagi menunjukkan arah perbaikan.
            """,
        ),
        E(
            "D11-06-3-ex1",
            "mudah",
            """
            Tulis fungsi `acuan_manusia(errors)` yang menerima dictionary nama ke error dan mengembalikan error terkecil sebagai tingkat human-level.
            """,
            """
            def acuan_manusia(errors):
                # TODO: implementasikan
                pass
            """,
            """
            assert acuan_manusia({"a": 0.03, "b": 0.01, "c": 0.005}) == 0.005
            assert acuan_manusia({"x": 0.2}) == 0.2
            assert acuan_manusia({"a": 0.5, "b": 0.5}) == 0.5
            """,
            "Gunakan min atas errors.values().",
            """
            def acuan_manusia(errors):
                return min(errors.values())
            """,
        ),
        E(
            "D11-06-3-ex2",
            "sedang",
            """
            Tulis fungsi `diagnosa_manusia(train, dev, human)` yang mengembalikan dictionary dengan kunci `"avoidable_bias"` (`train - human`), `"variance"` (`dev - train`) keduanya dibulatkan 4 desimal, dan `"dominan"` bernilai `"bias"` bila avoidable bias lebih besar atau sama dengan variance, selainnya `"variance"`.
            """,
            """
            def diagnosa_manusia(train, dev, human):
                # TODO: implementasikan
                pass
            """,
            """
            r = diagnosa_manusia(0.05, 0.08, 0.005)
            assert r == {"avoidable_bias": 0.045, "variance": 0.03, "dominan": "bias"}
            r = diagnosa_manusia(0.01, 0.08, 0.005)
            assert r == {"avoidable_bias": 0.005, "variance": 0.07, "dominan": "variance"}
            assert diagnosa_manusia(0.05, 0.10, 0.0)["dominan"] == "bias"
            """,
            "Bulatkan kedua selisih lalu bandingkan.",
            """
            def diagnosa_manusia(train, dev, human):
                b = round(train - human, 4)
                v = round(dev - train, 4)
                return {"avoidable_bias": b, "variance": v, "dominan": "bias" if b >= v else "variance"}
            """,
        ),
        E(
            "D11-06-3-ex3",
            "sedang",
            """
            Tulis fungsi `error_voting(p, k)` untuk `k` ahli ganjil yang salah secara independen dengan probabilitas `p` masing-masing. Error mayoritas adalah peluang paling sedikit `k // 2 + 1` ahli salah. Gunakan `math.comb`. Bulatkan hasil ke 6 desimal.
            """,
            """
            from math import comb

            def error_voting(p, k):
                # TODO: implementasikan
                pass
            """,
            """
            assert error_voting(0.03, 1) == 0.03
            assert error_voting(0.03, 3) == 0.002646
            assert error_voting(0.5, 5) == 0.5
            assert error_voting(0.0, 3) == 0.0
            assert error_voting(1.0, 3) == 1.0
            """,
            "Jumlahkan comb(k, j) * p**j * (1-p)**(k-j) untuk j dari k//2+1 sampai k.",
            """
            from math import comb

            def error_voting(p, k):
                batas = k // 2 + 1
                total = sum(comb(k, j) * p ** j * (1 - p) ** (k - j) for j in range(batas, k + 1))
                return round(total, 6)
            """,
        ),
        E(
            "D11-06-3-ex4",
            "menantang",
            """
            Simulasikan voting ahli yang saling berkorelasi. Tulis `voting_berkorelasi(n, p, k, rho, seed)`. Pakai `rng = np.random.default_rng(seed)`. Untuk tiap contoh, tarik `sulit = rng.random(n) < rho`. Pada contoh sulit semua ahli salah dengan probabilitas `p_sulit = min(1.0, p / rho)` bersama-sama (satu tarikan `rng.random(n) < p_sulit` dipakai untuk semua ahli). Pada contoh tidak sulit semua ahli benar. Kembalikan error mayoritas yaitu `mean(sulit & salah_bersama)` dibulatkan 4 desimal, dengan `salah_bersama = rng.random(n) < p_sulit`. Argumen `k` tidak mengubah hasil karena ahli bersepakat.
            """,
            """
            import numpy as np

            def voting_berkorelasi(n, p, k, rho, seed):
                # TODO: implementasikan
                pass
            """,
            """
            r = voting_berkorelasi(200000, 0.03, 3, 0.1, 0)
            assert abs(r - 0.03) < 0.003
            assert voting_berkorelasi(1000, 0.03, 3, 0.1, 1) == voting_berkorelasi(1000, 0.03, 9, 0.1, 1)
            assert voting_berkorelasi(1000, 0.0, 3, 0.1, 1) == 0.0
            """,
            "Urutan tarikan acak penting: sulit lebih dulu lalu salah_bersama. Hasilnya tidak bergantung pada k.",
            """
            import numpy as np

            def voting_berkorelasi(n, p, k, rho, seed):
                rng = np.random.default_rng(seed)
                sulit = rng.random(n) < rho
                p_sulit = min(1.0, p / rho)
                salah_bersama = rng.random(n) < p_sulit
                return round(float(np.mean(sulit & salah_bersama)), 4)
            """,
        ),
    ],
    [
        M(
            "Memakai performa dokter umum sebagai human-level padahal tim ahli jauh lebih baik.",
            "Pakai performa terbaik yang dicapai ahli saat tujuannya memperkirakan error optimal.",
        ),
        M(
            "Mengubah definisi human-level di tengah proyek tanpa mencatat.",
            "Tuliskan definisi acuan dan jangan mengubahnya diam-diam.",
        ),
        M(
            "Terus mengandalkan intuisi manusia setelah model melampaui manusia.",
            "Setelah itu, andalkan dev set besar bersih dan analisis ahli yang lebih langka.",
        ),
    ],
    [
        Q(
            "Dokter umum 3 persen, radiolog 1 persen, tim 0,5 persen. Acuan untuk perkiraan error optimal?",
            ["3 persen", "1 persen", "0,5 persen", "Rata-rata ketiganya"],
            2,
            "Error terbaik yang dicapai ahli memberi batas atas paling ketat bagi error optimal.",
        ),
        Q(
            "Train 5, dev 8, human 0,5 (persen). Komponen dominan?",
            ["Bias", "Variance", "Sama", "Tidak bisa"],
            0,
            "Avoidable bias 4,5 poin lebih besar dari variance 3 poin.",
        ),
        Q(
            "Mengapa kemajuan melambat setelah melampaui manusia?",
            ["Komputasi habis", "Acuan error optimal jadi tidak jelas dan intuisi manusia tidak lagi menuntun", "Dev set menyusut", "Model menjadi kecil"],
            1,
            "Setelah manusia tidak lebih baik, label dan intuisi manusia tidak lagi menunjuk arah perbaikan.",
        ),
        Q(
            "Mengapa voting teori ahli independen terlalu optimis?",
            ["Karena ahli sering salah di kasus sulit yang sama", "Karena rumusnya salah", "Karena p tetap", "Karena k kecil"],
            0,
            "Kesalahan ahli berkorelasi sehingga penurunan error nyata lebih kecil.",
        ),
        Q(
            "Manakah bukan alasan membandingkan dengan manusia?",
            ["Mudah mendapat label", "Intuisi untuk error analysis", "Perkiraan error optimal", "Menghilangkan kebutuhan test set"],
            3,
            "Perbandingan dengan manusia tidak menggantikan test set.",
        ),
    ],
    [
        "Performa manusia membantu pelabelan, error analysis, dan perkiraan error optimal.",
        "Human-level didefinisikan dengan ahli atau tim terbaik untuk perkiraan error optimal.",
        "Hitung avoidable bias dan variance terhadap acuan yang jelas.",
        "Setelah melampaui manusia, andalkan dev set besar dan ukuran yang lebih halus.",
    ],
    ["Machine Learning Yearning, bab 33 sampai 35 (Andrew Ng): membandingkan dengan performa manusia"],
)

video = {
    "needed": True,
    "kind": "ai_slides",
    "reason": "Bentuk learning curve dan perbandingan dengan acuan manusia paling jelas lewat grafik animasi.",
    "brief": [
        "Slide 1: dua grafik learning curve, kiri high bias dengan kurva mendatar tinggi, kanan high variance dengan celah yang menutup",
        "Slide 2: garis error yang diinginkan dan error optimal pada grafik yang sama",
        "Slide 3: tabel acuan dokter umum, radiolog, tim ahli dengan error 3, 1, 0,5 persen",
        "Slide 4: bagan alur memilih tindakan dari bias dominan atau variance dominan",
    ],
}

write_module(
    "D11",
    6,
    "Learning curve dan performa manusia",
    105,
    [
        "Membaca learning curve untuk memutuskan apakah data tambahan membantu",
        "Memetakan learning curve yang stabil dengan percobaan berulang dan stratifikasi",
        "Memakai performa manusia sebagai acuan error optimal dan membaca bias terhadapnya",
    ],
    [l1, l2, l3],
    video,
    REF,
)
