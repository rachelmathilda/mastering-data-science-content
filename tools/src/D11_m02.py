import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, C, E, Q, M, lesson, write_module

REF = [{"book": "Machine Learning Yearning (Andrew Ng)", "chapters": "bab 5 sampai 12"}]

SAMPEL = """
import numpy as np

W_TRUE = np.array([1.0, -1.0, 0.5, 0.8, -0.6])

def sampel(m, noise, seed):
    rng = np.random.default_rng(seed)
    z = rng.normal(size=(m, 5))
    y = (z @ W_TRUE > 0).astype(int)
    x = z + noise * rng.normal(size=(m, 5))
    return x, y
"""

l1 = lesson(
    "D11-02-1",
    "Training, dev, dan test set serta distribusinya",
    40,
    [
        "Mendefinisikan training, dev, dan test set beserta peran masing-masing",
        "Memilih dev dan test set yang mencerminkan data masa depan, bukan sekadar data yang tersedia",
        "Menjelaskan mengapa dev dan test harus berasal dari distribusi yang sama",
        "Membagi data per segmen sehingga dev dan test seimbang",
    ],
    [
        T("""
        ## Cerita: detektor kucing yang bagus di lab tetapi buruk di aplikasi

        Kamu menjalankan aplikasi ponsel tempat pengguna mengunggah berbagai gambar, dan kamu ingin otomatis menemukan foto kucing. Tim mengunduh banyak gambar kucing (contoh positif) dan bukan kucing (contoh negatif) dari berbagai situs web. Dataset dibagi 70 persen untuk training dan 30 persen untuk test. Detektor bekerja bagus di keduanya.

        Begitu dipasang di aplikasi, performanya buruk sekali. Apa yang terjadi? Ternyata foto yang diunggah pengguna terlihat berbeda dari foto situs web. Foto ponsel resolusinya lebih rendah, lebih buram, dan pencahayaannya lebih buruk. Karena training dan test sama-sama dibuat dari gambar web, algoritma tidak pernah dilatih maupun diuji pada distribusi yang benar-benar penting, yaitu foto ponsel.

        Sebelum era big data, aturan umumnya adalah membagi acak 70 persen dan 30 persen. Cara itu masih bisa bekerja, tetapi menjadi ide buruk pada semakin banyak aplikasi, terutama ketika distribusi training (gambar web) berbeda dari distribusi yang akhirnya dipedulikan (gambar ponsel).
        """),
        T("""
        ## Tiga set dan tugas masing-masing

        Definisi yang dipakai di seluruh course:

        - **Training set**: tempat kamu menjalankan algoritma pembelajaran.
        - **Dev set** (development set): dipakai menyetel parameter, memilih fitur, dan membuat keputusan lain tentang algoritma. Kadang disebut hold-out cross validation set.
        - **Test set**: dipakai mengevaluasi performa algoritma, tetapi tidak untuk memutuskan algoritma atau parameter mana yang dipakai.

        Setelah dev set dan test set ditentukan, tim akan mencoba banyak ide, misalnya parameter yang berbeda, untuk melihat mana yang terbaik. Dev dan test set memungkinkan tim melihat dengan cepat seberapa baik algoritma bekerja.

        Dengan kata lain, **tujuan dev dan test set adalah mengarahkan tim ke perubahan paling penting pada sistem machine learning.** Itulah ukuran keberhasilan sebuah dev set: apakah ia menunjuk ke arah yang benar. Karena itu pemilihannya adalah keputusan strategis, bukan sekadar urusan teknis pemisahan data.
        """),
        T("""
        ## Pilih dev dan test set yang mencerminkan data masa depan

        Prinsip pertama: pilih dev dan test set yang mencerminkan data yang kamu harapkan diterima di masa depan dan ingin kamu kuasai. Test set tidak boleh hanya menjadi 30 persen dari data yang kebetulan tersedia, terutama bila kamu menduga data masa depan berbeda sifatnya dari data training.

        Bagaimana bila aplikasi belum diluncurkan dan belum ada pengguna? Kamu tetap bisa mendekati. Minta teman memotret kucing dengan ponsel lalu mengirimkannya. Setelah peluncuran, perbarui dev dan test dengan data pengguna nyata. Jika benar-benar tidak ada cara mendekati data masa depan, kamu bisa mulai dengan gambar web, tetapi sadari risikonya: sistem mungkin tidak menggeneralisasi dengan baik.

        Dibutuhkan penilaian untuk memutuskan seberapa besar investasi pada dev dan test set yang bagus. Tetapi jangan pernah berasumsi bahwa distribusi training sama dengan distribusi test. Usahakan memilih contoh test yang mencerminkan apa yang akhirnya ingin kamu kuasai, bukan data apa pun yang kebetulan kamu punya untuk training.
        """),
        T("""
        ## Dev dan test harus berasal dari distribusi yang sama

        Misalkan data aplikasi kucingmu terbagi menjadi empat wilayah pasar terbesar: (i) AS, (ii) Tiongkok, (iii) India, dan (iv) lainnya. Untuk membuat dev dan test set, kamu menaruh AS dan India di dev, sedangkan Tiongkok dan lainnya di test. Tampaknya sah, bukan?

        Tidak. Begitu dev dan test ditentukan, tim akan fokus memperbaiki performa dev. Dev set harus mencerminkan tugas yang paling ingin kamu tingkatkan: bagus di keempat wilayah, bukan hanya dua. Masalah kedua: ada kemungkinan tim membangun sesuatu yang bagus di dev tetapi buruk di test. Ini menyebabkan frustrasi dan usaha yang terbuang.

        Jika dev dan test berasal dari distribusi yang sama, diagnosisnya jelas: kamu overfit ke dev set, dan obatnya adalah menambah data dev. Tetapi jika distribusinya berbeda, ada beberapa kemungkinan: (1) overfit ke dev, (2) test lebih sulit dari dev sehingga algoritma sudah sebaik yang bisa diharapkan, atau (3) test tidak lebih sulit, hanya berbeda, sehingga banyak usaha pada dev terbuang. Tiga kemungkinan ini membuat prioritas sulit ditentukan.

        Pada benchmark pihak ketiga, pembuatnya mungkin menetapkan dev dan test dari distribusi berbeda. Keberuntungan akan lebih berpengaruh daripada keterampilan. Mengembangkan algoritma yang dilatih pada satu distribusi dan menggeneralisasi ke distribusi lain adalah topik riset penting. Tetapi jika tujuanmu memajukan aplikasi tertentu, pilih dev dan test dari distribusi yang sama agar tim lebih efisien.
        """),
        K(
            "warning",
            """
            Jangan mengambil satu wilayah, satu bulan, atau satu sumber penuh sebagai dev dan sumber lain sebagai test. Acak dulu dalam setiap segmen yang penting, lalu bagi. Dengan begitu dev dan test sama-sama mencerminkan campuran data yang akan kamu hadapi.
            """,
        ),
        C(
            SAMPEL
            + """
from sklearn.linear_model import LogisticRegression

X_web, y_web = sampel(4000, 0.3, 1)
X_web_test, y_web_test = sampel(2000, 0.3, 2)
X_hp, y_hp = sampel(2000, 2.0, 3)

model = LogisticRegression(max_iter=1000).fit(X_web, y_web)
print("akurasi pada test web   :", round(model.score(X_web_test, y_web_test), 3))
print("akurasi pada foto ponsel:", round(model.score(X_hp, y_hp), 3))
""",
            """
            akurasi pada test web sekitar 0.90
            akurasi pada foto ponsel sekitar 0.65
            """,
            """
            Data web dan data ponsel punya label yang ditentukan oleh variabel laten yang sama, tetapi fitur ponsel jauh lebih berisik. Model dilatih hanya dari data web, jadi test web terlihat memuaskan sementara performa pada ponsel jauh lebih rendah. Inilah persis kegagalan cerita kucing: test set tidak mencerminkan distribusi yang penting.
            """,
        ),
        C(
            """
import numpy as np
from sklearn.linear_model import LogisticRegression

W_TRUE = np.array([1.0, -1.0, 0.5, 0.8, -0.6])
NOISE = {"US": 0.3, "India": 0.8, "Other": 1.2, "China": 2.0}

def sampel(m, noise, seed):
    rng = np.random.default_rng(seed)
    z = rng.normal(size=(m, 5))
    y = (z @ W_TRUE > 0).astype(int)
    return z + noise * rng.normal(size=(m, 5)), y

X_tr = np.vstack([sampel(1000, NOISE[r], i)[0] for i, r in enumerate(NOISE)])
y_tr = np.concatenate([sampel(1000, NOISE[r], i)[1] for i, r in enumerate(NOISE)])
model = LogisticRegression(max_iter=1000).fit(X_tr, y_tr)

ev = {r: sampel(500, NOISE[r], 10 + i) for i, r in enumerate(NOISE)}
acc = lambda rs: np.mean([model.score(*ev[r]) for r in rs])
print("skema wilayah: dev(US,India)=%.3f  test(China,Other)=%.3f" % (acc(["US", "India"]), acc(["China", "Other"])))

Xp = np.vstack([ev[r][0] for r in ev])
yp = np.concatenate([ev[r][1] for r in ev])
idx = np.random.default_rng(0).permutation(len(Xp))
dev, te = idx[:1000], idx[1000:]
print("skema acak  : dev=%.3f  test=%.3f" % (model.score(Xp[dev], yp[dev]), model.score(Xp[te], yp[te])))
""",
            """
            skema wilayah: dev tinggi, test jauh lebih rendah (selisih besar)
            skema acak: dev dan test hampir sama
            """,
            """
            Dengan dev dari wilayah berderau rendah dan test dari wilayah berderau tinggi, angka dev menipu dan tim tidak bisa tahu apakah gap itu karena overfit atau karena test memang lebih sulit. Dengan pengacakan lintas wilayah, dev dan test hampir identik, dan gap yang tersisa bisa langsung ditafsirkan sebagai overfit.
            """,
        ),
        C(
            """
import numpy as np

region = np.array(["US"] * 40 + ["China"] * 31 + ["India"] * 20 + ["Other"] * 9)
rng = np.random.default_rng(0)
dev, te = [], []
for r in sorted(set(region)):
    idx = rng.permutation(np.where(region == r)[0])
    setengah = len(idx) // 2
    dev.extend(idx[:setengah])
    te.extend(idx[setengah:])

for r in sorted(set(region)):
    print(r, "dev:", int(np.sum(region[dev] == r)), "test:", int(np.sum(region[te] == r)))
""",
            """
            China dev: 15 test: 16
            India dev: 10 test: 10
            Other dev: 4 test: 5
            US dev: 20 test: 20
            """,
            """
            Setiap wilayah diacak sendiri lalu dibagi dua. Hasilnya setiap wilayah hadir di dev dan test dengan proporsi yang hampir sama. Teknik ini disebut stratifikasi, dan ia menjaga dev serta test tetap berasal dari distribusi yang sama.
            """,
        ),
        E(
            "D11-02-1-ex1",
            "mudah",
            """
            Tulis fungsi `hitung_region(region)` yang menerima list atau array nama wilayah dan mengembalikan dictionary jumlah kemunculan tiap wilayah.
            """,
            """
            def hitung_region(region):
                # TODO: implementasikan
                pass
            """,
            """
            assert hitung_region(["US", "India", "US"]) == {"US": 2, "India": 1}
            assert hitung_region([]) == {}
            assert hitung_region(["A"] * 5) == {"A": 5}
            """,
            "Gunakan dictionary dengan get atau collections.Counter lalu ubah menjadi dict.",
            """
            from collections import Counter

            def hitung_region(region):
                return dict(Counter(region))
            """,
        ),
        E(
            "D11-02-1-ex2",
            "sedang",
            """
            Tulis fungsi `bagi_per_region(region, seed)` yang menerima array nama wilayah dan mengembalikan `(dev_idx, test_idx)`. Untuk setiap wilayah (urut abjad) acak indeksnya dengan `np.random.default_rng(seed)` yang dibuat sekali, taruh `len // 2` indeks pertama ke dev dan sisanya ke test. Kembalikan keduanya sebagai array NumPy.
            """,
            """
            import numpy as np

            def bagi_per_region(region, seed):
                # TODO: implementasikan
                pass
            """,
            """
            import numpy as np
            region = np.array(["US"] * 50 + ["China"] * 41 + ["India"] * 30 + ["Other"] * 20)
            dev, te = bagi_per_region(region, 0)
            assert not (set(dev) & set(te))
            assert sorted(list(dev) + list(te)) == list(range(len(region)))
            for r in ["US", "China", "India", "Other"]:
                a = int(np.sum(region[dev] == r))
                b = int(np.sum(region[te] == r))
                assert abs(a - b) <= 1
            d2, t2 = bagi_per_region(region, 0)
            assert list(dev) == list(d2)
            """,
            "Buat rng sekali di luar loop. Di dalam loop ambil np.where(region == r)[0], acak dengan rng.permutation, lalu iris.",
            """
            import numpy as np

            def bagi_per_region(region, seed):
                region = np.asarray(region)
                rng = np.random.default_rng(seed)
                dev, te = [], []
                for r in sorted(set(region.tolist())):
                    idx = rng.permutation(np.where(region == r)[0])
                    setengah = len(idx) // 2
                    dev.extend(idx[:setengah].tolist())
                    te.extend(idx[setengah:].tolist())
                return np.array(dev), np.array(te)
            """,
        ),
        E(
            "D11-02-1-ex3",
            "sedang",
            """
            Tulis fungsi `ada_mismatch(a, b, batas=0.3)` untuk mendeteksi pergeseran distribusi pada satu fitur. Hitung `pergeseran = |mean(a) - mean(b)| / sqrt((var(a) + var(b)) / 2)` dengan `np.var` bawaan, lalu kembalikan `True` bila `pergeseran > batas`. Jika pembilang dan penyebut nol, anggap tidak ada mismatch.
            """,
            """
            import numpy as np

            def ada_mismatch(a, b, batas=0.3):
                # TODO: implementasikan
                pass
            """,
            """
            import numpy as np
            rng = np.random.default_rng(0)
            a = rng.normal(0, 1, 5000)
            b = rng.normal(0, 1, 5000)
            c = rng.normal(1.0, 1, 5000)
            assert ada_mismatch(a, b) is False
            assert ada_mismatch(a, c) is True
            assert ada_mismatch([1, 1, 1], [1, 1, 1]) is False
            """,
            "Gunakan np.asarray lalu hitung penyebut. Jika penyebut 0, kembalikan False.",
            """
            import numpy as np

            def ada_mismatch(a, b, batas=0.3):
                a = np.asarray(a, dtype=float)
                b = np.asarray(b, dtype=float)
                penyebut = np.sqrt((np.var(a) + np.var(b)) / 2)
                if penyebut == 0:
                    return False
                return bool(abs(a.mean() - b.mean()) / penyebut > batas)
            """,
        ),
        E(
            "D11-02-1-ex4",
            "menantang",
            """
            Tulis fungsi `diagnosis_celah(acc_dev, acc_test, sama_distribusi, batas=0.03)`. Hitung `celah = round(acc_dev - acc_test, 6)`. Jika `sama_distribusi` benar dan `celah > batas` kembalikan `"overfit dev: tambah data dev"`. Jika `sama_distribusi` salah dan `abs(celah) > batas` kembalikan `"ambigu: overfit, test lebih sulit, atau distribusi berbeda"`. Selain itu kembalikan `"ok"`.
            """,
            """
            def diagnosis_celah(acc_dev, acc_test, sama_distribusi, batas=0.03):
                # TODO: implementasikan
                pass
            """,
            """
            assert diagnosis_celah(0.92, 0.85, True) == "overfit dev: tambah data dev"
            assert diagnosis_celah(0.92, 0.85, False) == "ambigu: overfit, test lebih sulit, atau distribusi berbeda"
            assert diagnosis_celah(0.80, 0.90, False) == "ambigu: overfit, test lebih sulit, atau distribusi berbeda"
            assert diagnosis_celah(0.90, 0.89, True) == "ok"
            assert diagnosis_celah(0.80, 0.90, True) == "ok"
            assert diagnosis_celah(0.90, 0.87, True) == "ok"
            """,
            "Hitung celah dibulatkan dulu. Perhatikan: pada distribusi sama hanya celah positif yang berarti overfit, sedangkan pada distribusi berbeda selisih berapa pun arahnya membuat diagnosis ambigu.",
            """
            def diagnosis_celah(acc_dev, acc_test, sama_distribusi, batas=0.03):
                celah = round(acc_dev - acc_test, 6)
                if sama_distribusi and celah > batas:
                    return "overfit dev: tambah data dev"
                if (not sama_distribusi) and abs(celah) > batas:
                    return "ambigu: overfit, test lebih sulit, atau distribusi berbeda"
                return "ok"
            """,
        ),
    ],
    [
        M(
            "Membagi acak 70 persen dan 30 persen dari data yang tersedia tanpa memikirkan data masa depan.",
            "Tentukan dulu distribusi yang ingin dikuasai, lalu bentuk dev dan test dari data yang mencerminkannya.",
        ),
        M(
            "Menaruh wilayah atau periode berbeda di dev dan test.",
            "Acak dalam tiap segmen lalu bagi sehingga dev dan test berasal dari campuran yang sama.",
        ),
        M(
            "Berhenti memperbarui dev dan test setelah peluncuran.",
            "Perbarui keduanya dengan data pengguna nyata begitu tersedia.",
        ),
    ],
    [
        Q(
            "Apa tujuan utama dev dan test set?",
            ["Menambah jumlah data", "Mengarahkan tim ke perubahan terpenting pada sistem", "Mengurangi biaya komputasi", "Menggantikan training set"],
            1,
            "Dev dan test set dipakai untuk membuat keputusan pengembangan yang tepat.",
        ),
        Q(
            "Aplikasi belum diluncurkan dan belum punya pengguna. Apa langkah yang disarankan?",
            ["Tidak membuat dev set", "Mendekati data masa depan, misalnya minta teman memotret dengan ponsel", "Memakai test set sebagai training", "Menunggu setahun"],
            1,
            "Pendekatan data masa depan lebih baik daripada mengandalkan data yang kebetulan tersedia.",
        ),
        Q(
            "Dev dan test dari distribusi sama tetapi performa dev jauh di atas test. Diagnosisnya?",
            ["Overfit ke dev set", "Test lebih sulit", "Distribusi berbeda", "Metrik salah"],
            0,
            "Bila distribusinya sama, penjelasan paling jelas adalah overfit ke dev, dan obatnya menambah data dev.",
        ),
        Q(
            "Mengapa dev dan test yang berbeda distribusi menyulitkan prioritas?",
            ["Karena ukuran data berbeda", "Karena ada beberapa penjelasan yang mungkin sehingga arah perbaikan tidak jelas", "Karena library tidak mendukung", "Karena model membeku"],
            1,
            "Gap bisa disebabkan overfit, test yang lebih sulit, atau sekadar perbedaan distribusi, sehingga usaha mudah terbuang.",
        ),
        Q(
            "Apa keuntungan stratifikasi per wilayah saat membagi dev dan test?",
            ["Menambah jumlah contoh", "Menjaga proporsi tiap wilayah sama di dev dan test", "Mempercepat training", "Menghilangkan kebutuhan test set"],
            1,
            "Setiap wilayah hadir di kedua set dengan proporsi hampir sama sehingga distribusi kedua set sama.",
        ),
    ],
    [
        "Dev set mengarahkan keputusan pengembangan dan test set memberi estimasi akhir yang jujur.",
        "Pilih dev dan test yang mencerminkan data masa depan, bukan data yang kebetulan tersedia.",
        "Dev dan test harus berasal dari distribusi yang sama agar gap bisa didiagnosis dengan jelas.",
        "Stratifikasi per segmen menjaga dev dan test seimbang.",
    ],
    ["Machine Learning Yearning, bab 5 dan 6 (Andrew Ng): dev dan test set, serta distribusi yang sama"],
)

l2 = lesson(
    "D11-02-2",
    "Ukuran dev dan test set serta metrik tunggal",
    40,
    [
        "Menentukan ukuran dev set yang cukup untuk mendeteksi perbedaan antar algoritma",
        "Menjelaskan mengapa fraksi 30 persen untuk test set tidak selalu masuk akal",
        "Menggabungkan beberapa metrik menjadi satu angka dengan F1 dan rata-rata berbobot",
        "Memilih classifier terbaik memakai metrik tunggal",
    ],
    [
        T("""
        ## Seberapa besar dev set harus dibuat

        Dev set harus cukup besar untuk mendeteksi perbedaan antar algoritma yang sedang kamu coba. Misalkan classifier A memiliki akurasi 90,0 persen dan classifier B 90,1 persen. Dev set berisi 100 contoh tidak akan mampu mendeteksi selisih 0,1 persen itu. Dibandingkan masalah machine learning lain, dev set 100 contoh itu kecil. Ukuran 1.000 sampai 10.000 contoh umum dipakai. Dengan 10.000 contoh, kamu punya peluang yang baik mendeteksi perbaikan 0,1 persen.

        Untuk aplikasi matang dan penting, seperti iklan, pencarian web, dan rekomendasi produk, ada tim yang sangat termotivasi memeras perbaikan 0,01 persen karena berdampak langsung pada keuntungan. Dev set pada kasus itu bisa jauh lebih besar dari 10.000 agar perbaikan yang lebih kecil terdeteksi.

        Dalam teori, kamu juga bisa menguji apakah sebuah perubahan algoritma berbeda secara signifikan statistik pada dev set. Dalam praktik, kebanyakan tim tidak melakukannya kecuali menulis makalah akademik, dan uji signifikansi tidak terlalu berguna untuk mengukur kemajuan sementara. Meski begitu, memahami derau pengukuran tetap penting, dan kamu akan menghitungnya sendiri di bawah.
        """),
        T("""
        ## Derau pengukuran dan ukuran sampel

        Akurasi yang diukur pada n contoh adalah rata-rata dari n hasil benar atau salah. Jika akurasi sebenarnya p, simpangan baku estimasi akurasi (standard error) adalah `sqrt(p * (1 - p) / n)`. Untuk p = 0,9 dan n = 100 angka itu sekitar 0,03, yaitu 3 poin persen. Tiga poin persen jauh lebih besar dari selisih 0,1 poin persen yang ingin dideteksi, jadi selisih sekecil itu tenggelam dalam derau.

        Dengan n = 10.000, standard error turun menjadi 0,003, yaitu 0,3 poin persen. Selisih 0,1 poin persen masih berada di bawah derau satu pengukuran, tetapi dua classifier yang dievaluasi pada contoh yang sama punya derau yang berkorelasi sehingga selisihnya lebih mudah dideteksi daripada angka sederhana ini menyiratkan. Intinya: makin kecil perbaikan yang ingin kamu deteksi, makin besar dev set yang kamu butuhkan, dan kebutuhannya tumbuh sangat cepat.

        Simulasi di bawah memperlihatkan hal ini langsung. Kamu akan melihat seberapa sering classifier yang sebenarnya sedikit lebih baik justru terukur lebih buruk.
        """),
        T("""
        ## Ukuran test set dan mitos 30 persen

        Bagaimana dengan test set? Ia harus cukup besar untuk memberi keyakinan tinggi pada performa keseluruhan sistem. Satu heuristik populer adalah memakai 30 persen data untuk test. Ini bekerja baik bila jumlah contoh moderat, misalnya 100 sampai 10.000.

        Di era big data, ada masalah dengan lebih dari satu miliar contoh. Fraksi data untuk dev dan test terus mengecil walau jumlah absolutnya membesar. Tidak ada gunanya memiliki dev dan test jauh lebih besar dari yang dibutuhkan untuk mengevaluasi algoritma. Jadi kata kuncinya adalah **jumlah absolut yang cukup untuk tugasnya**, bukan persentase tetap.

        Contoh praktis: bila dataset 10 juta contoh dan kamu hanya butuh 20.000 contoh untuk mendeteksi perbaikan yang kamu pedulikan, maka dev dan test masing-masing cukup 0,2 persen dari data. Sisanya lebih berguna sebagai training karena model yang lebih besar bisa memanfaatkannya.
        """),
        T("""
        ## Satu angka untuk mengatur tim

        **Akurasi klasifikasi** adalah contoh metrik evaluasi bernilai tunggal: jalankan classifier pada dev set dan terima satu angka tentang pecahan contoh yang diklasifikasikan benar. Jika A mendapat 97 persen dan B 90 persen, A lebih unggul menurut metrik ini.

        Sebaliknya, **precision dan recall** bukan metrik tunggal karena memberi dua angka. Misalkan A memiliki precision 95 persen dan recall 90 persen, sedangkan B memiliki precision 98 persen dan recall 85 persen. Tidak ada yang jelas lebih unggul, sehingga perbandingan tidak mengarahkan pilihan.

        Jika kamu benar-benar peduli pada keduanya, gabungkan menjadi satu angka. Rata-rata sederhana bisa dipakai, tetapi **F1 score** yang merupakan rata-rata harmonik `2 / (1/P + 1/R)` bekerja lebih baik karena menghukum ketimpangan antara precision dan recall. Dengan F1, A mendapat sekitar 92,4 persen dan B sekitar 91,0 persen, sehingga A jelas dipilih.

        Contoh lain: kamu memantau akurasi di empat wilayah AS, Tiongkok, India, dan lainnya. Itu empat angka. Rata-rata atau rata-rata berbobot keempatnya menjadi satu angka. Rata-rata (berbobot) adalah salah satu cara paling umum menggabungkan beberapa metrik. Dengan satu angka, kamu dapat mengurutkan semua model dan segera memutuskan mana yang terbaik.
        """),
        K(
            "tip",
            """
            Ketika tim berdebat tanpa akhir tentang model mana yang lebih baik, sering penyebabnya adalah belum ada metrik tunggal yang disepakati. Menyepakati satu angka, walau belum sempurna, mengubah debat menjadi pengurutan.
            """,
        ),
        C(
            """
import numpy as np

p = 0.9
print("n        standard error")
for n in [100, 1000, 10000, 100000]:
    print(f"{n:7d}  {np.sqrt(p * (1 - p) / n):.4f}")
""",
            """
            n        standard error
                100  0.0300
               1000  0.0095
              10000  0.0030
             100000  0.0009
            """,
            """
            Standard error menurun dengan akar jumlah sampel. Untuk membuat derau 10 kali lebih kecil, kamu butuh data 100 kali lebih banyak. Itulah sebabnya mendeteksi perbaikan yang sangat kecil menuntut dev set yang sangat besar.
            """,
        ),
        C(
            """
import numpy as np

rng = np.random.default_rng(0)
a, b = 0.900, 0.901
trials = 4000
print("n        P(B terukur lebih baik dari A)")
for n in [100, 1000, 10000, 100000]:
    acc_a = rng.binomial(n, a, size=trials) / n
    acc_b = rng.binomial(n, b, size=trials) / n
    print(f"{n:7d}  {np.mean(acc_b > acc_a):.3f}")
""",
            """
            n        P(B terukur lebih baik dari A)
                100  sekitar 0.45
               1000  sekitar 0.50 sampai 0.53
              10000  sekitar 0.60
             100000  sekitar 0.77
            """,
            """
            Dua classifier dengan akurasi sebenarnya 90,0 persen dan 90,1 persen dievaluasi pada dev set independen. Pada n kecil, hasilnya hampir seperti lempar koin. Bahkan pada 10.000 contoh peluangnya baru sekitar 60 persen dalam simulasi independen ini, dan baru mendekati 77 persen pada 100.000 contoh. Evaluasi pada contoh yang sama membuat deteksi lebih mudah, tetapi pesan utamanya tetap: perbedaan sangat kecil butuh dev set sangat besar.
            """,
        ),
        C(
            """
import numpy as np
from sklearn.metrics import f1_score, precision_score, recall_score

rng = np.random.default_rng(1)
y_true = rng.integers(0, 2, 1000)
y_pred = np.where(rng.random(1000) < 0.85, y_true, 1 - y_true)

tp = np.sum((y_true == 1) & (y_pred == 1))
fp = np.sum((y_true == 0) & (y_pred == 1))
fn = np.sum((y_true == 1) & (y_pred == 0))
precision = tp / (tp + fp)
recall = tp / (tp + fn)
f1 = 2 / (1 / precision + 1 / recall)

print("F1 manual   :", round(float(f1), 4))
print("F1 sklearn  :", round(float(f1_score(y_true, y_pred)), 4))
print("cocok       :", bool(np.isclose(f1, f1_score(y_true, y_pred))))
""",
            """
            F1 manual dan sklearn sama
            cocok: True
            """,
            """
            Precision, recall, dan F1 dihitung dari jumlah true positive, false positive, dan false negative. F1 adalah rata-rata harmonik precision dan recall. Menghitungnya manual dan mencocokkannya dengan library memastikan kamu paham persis apa yang dioptimalkan oleh tim.
            """,
        ),
        E(
            "D11-02-2-ex1",
            "mudah",
            """
            Tulis fungsi `standard_error(p, n)` yang mengembalikan `sqrt(p * (1 - p) / n)` sebagai float.
            """,
            """
            import math

            def standard_error(p, n):
                # TODO: implementasikan
                pass
            """,
            """
            assert abs(standard_error(0.9, 100) - 0.03) < 1e-12
            assert abs(standard_error(0.5, 10000) - 0.005) < 1e-12
            assert isinstance(standard_error(0.9, 100), float)
            """,
            "Gunakan math.sqrt dan pastikan hasilnya float.",
            """
            import math

            def standard_error(p, n):
                return float(math.sqrt(p * (1 - p) / n))
            """,
        ),
        E(
            "D11-02-2-ex2",
            "sedang",
            """
            Tulis fungsi `n_minimum(p, se_target)` yang mengembalikan jumlah sampel integer terkecil agar `sqrt(p * (1 - p) / n) <= se_target`. Gunakan pembulatan ke atas dari `p * (1 - p) / se_target**2` dengan pengamanan terhadap galat floating point (bulatkan dulu ke 6 desimal).
            """,
            """
            import math

            def n_minimum(p, se_target):
                # TODO: implementasikan
                pass
            """,
            """
            assert n_minimum(0.9, 0.003) == 10000
            assert n_minimum(0.5, 0.01) == 2500
            assert n_minimum(0.9, 0.03) == 100
            """,
            "Dari rumus standard error, n = p(1-p) / se^2. Bulatkan ke 6 desimal sebelum math.ceil agar 10000.000000001 tidak menjadi 10001.",
            """
            import math

            def n_minimum(p, se_target):
                n = round(p * (1 - p) / se_target ** 2, 6)
                return int(math.ceil(n))
            """,
        ),
        E(
            "D11-02-2-ex3",
            "sedang",
            """
            Tulis fungsi `f1(precision, recall)` yang mengembalikan rata-rata harmonik `2 * P * R / (P + R)`. Jika `P + R` sama dengan nol kembalikan `0.0`.
            """,
            """
            def f1(precision, recall):
                # TODO: implementasikan
                pass
            """,
            """
            assert abs(f1(0.95, 0.90) - 0.924324324) < 1e-6
            assert abs(f1(0.98, 0.85) - 0.910382513) < 1e-6
            assert f1(0.0, 0.0) == 0.0
            assert f1(1.0, 1.0) == 1.0
            """,
            "Tangani kasus pembagi nol lebih dulu, lalu hitung 2 * P * R / (P + R).",
            """
            def f1(precision, recall):
                if precision + recall == 0:
                    return 0.0
                return 2 * precision * recall / (precision + recall)
            """,
        ),
        E(
            "D11-02-2-ex4",
            "menantang",
            """
            Tulis fungsi `pilih_terbaik(tabel, bobot)`. `tabel` memetakan nama classifier ke dictionary akurasi per wilayah, dan `bobot` memetakan wilayah ke bobot. Hitung rata-rata berbobot yang dinormalkan (jumlah bobot dibagi sehingga totalnya 1) untuk tiap classifier, lalu kembalikan tuple `(nama_terbaik, skor_terbaik)`. Jika seri, pilih nama yang lebih dulu secara abjad.
            """,
            """
            def pilih_terbaik(tabel, bobot):
                # TODO: implementasikan
                pass
            """,
            """
            tabel = {
                "A": {"US": 0.95, "China": 0.90, "India": 0.80, "Other": 0.85},
                "B": {"US": 0.92, "China": 0.93, "India": 0.85, "Other": 0.80},
            }
            bobot = {"US": 0.4, "China": 0.3, "India": 0.2, "Other": 0.1}
            nama, skor = pilih_terbaik(tabel, bobot)
            assert nama == "B"
            assert abs(skor - 0.897) < 1e-9
            bobot2 = {"US": 4, "China": 3, "India": 2, "Other": 1}
            nama2, skor2 = pilih_terbaik(tabel, bobot2)
            assert nama2 == "B" and abs(skor2 - 0.897) < 1e-9
            seri = {"X": {"US": 0.9}, "A": {"US": 0.9}}
            assert pilih_terbaik(seri, {"US": 1})[0] == "A"
            """,
            "Normalkan bobot dengan membaginya terhadap jumlah bobot. Urutkan kandidat berdasarkan (-skor, nama) untuk menangani seri.",
            """
            def pilih_terbaik(tabel, bobot):
                total = sum(bobot.values())
                skor = {}
                for nama, akurasi in tabel.items():
                    skor[nama] = sum(akurasi[w] * bobot[w] / total for w in bobot)
                terbaik = sorted(skor, key=lambda n: (-round(skor[n], 12), n))[0]
                return terbaik, skor[terbaik]
            """,
        ),
    ],
    [
        M(
            "Menganggap dev set 100 contoh cukup untuk membandingkan model yang beda 0,1 persen.",
            "Hitung standard error dan sesuaikan ukuran dev set dengan perbedaan terkecil yang ingin dideteksi.",
        ),
        M(
            "Selalu memakai 30 persen data sebagai test set pada dataset besar.",
            "Gunakan jumlah absolut yang cukup untuk tugasnya dan simpan sisanya untuk training.",
        ),
        M(
            "Membiarkan tim melacak precision dan recall tanpa satu angka gabungan.",
            "Gabungkan menjadi F1 atau rata-rata berbobot agar semua model bisa diurutkan.",
        ),
    ],
    [
        Q(
            "Pada akurasi 90 persen, standard error dengan n = 100 mendekati?",
            ["0,3", "0,03", "0,003", "0,0003"],
            1,
            "sqrt(0,9 * 0,1 / 100) = 0,03.",
        ),
        Q(
            "Apa yang terjadi pada standard error bila n dikali 100?",
            ["Turun menjadi 1/100", "Turun menjadi 1/10", "Tidak berubah", "Naik 10 kali"],
            1,
            "Standard error sebanding dengan 1 per akar n, jadi n dikali 100 membuatnya sepersepuluh.",
        ),
        Q(
            "Mengapa F1 lebih disukai daripada rata-rata aritmetika precision dan recall?",
            ["Lebih mudah dihitung", "Menghukum ketimpangan antara precision dan recall", "Selalu lebih besar", "Tidak butuh label"],
            1,
            "Rata-rata harmonik rendah jika salah satu dari keduanya rendah.",
        ),
        Q(
            "Dataset 10 juta contoh. Kebutuhan dev dan test masing-masing 20.000. Pendekatan yang benar?",
            ["Pakai 30 persen untuk test", "Pakai jumlah absolut yang cukup dan sisanya untuk training", "Tidak memakai test", "Pakai semua sebagai dev"],
            1,
            "Jumlah absolut yang cukup lebih penting daripada fraksi tetap pada dataset sangat besar.",
        ),
        Q(
            "Classifier A: precision 95 persen dan recall 90 persen. B: 98 persen dan 85 persen. Mana yang unggul menurut F1?",
            ["A", "B", "Seri", "Tidak bisa dihitung"],
            0,
            "F1 A sekitar 92,4 persen dan F1 B sekitar 91,0 persen.",
        ),
    ],
    [
        "Dev set harus cukup besar untuk mendeteksi perbedaan terkecil yang kamu pedulikan.",
        "Standard error menurun dengan akar n, sehingga perbaikan kecil membutuhkan data sangat besar.",
        "Ukuran test set ditentukan jumlah absolut yang cukup, bukan fraksi tetap seperti 30 persen.",
        "Metrik tunggal seperti akurasi, F1, atau rata-rata berbobot memungkinkan pengurutan model yang cepat.",
    ],
    ["Machine Learning Yearning, bab 7 dan 8 (Andrew Ng): ukuran dev dan test set, serta metrik evaluasi tunggal"],
)

l3 = lesson(
    "D11-02-3",
    "Optimizing, satisficing, iterasi, dan kapan mengubah",
    40,
    [
        "Memisahkan metrik menjadi satu optimizing metric dan beberapa satisficing metric",
        "Menjelaskan siklus ide, kode, eksperimen dan mengapa dev set serta metrik mempercepatnya",
        "Mengenali tiga penyebab dev set dan metrik harus diubah",
        "Mengukur inflasi akibat overfit ke dev set",
    ],
    [
        T("""
        ## Optimizing dan satisficing metric

        Ada cara lain menggabungkan beberapa metrik evaluasi. Misalkan kamu peduli akurasi sekaligus waktu eksekusi, dan harus memilih dari tiga classifier: A dengan akurasi 90 persen dan 80 ms, B dengan 92 persen dan 95 ms, serta C dengan 95 persen dan 1.500 ms.

        Memasukkan akurasi dan waktu eksekusi ke satu rumus, misalnya `akurasi - 0,5 * waktu`, terasa tidak wajar. Yang bisa dilakukan: tentukan dulu waktu eksekusi yang dapat diterima, misalnya apa pun di bawah 100 ms. Lalu maksimalkan akurasi dengan syarat classifier memenuhi batas waktu itu. Di sini waktu eksekusi adalah **satisficing metric**: classifier hanya perlu cukup baik. Akurasi adalah **optimizing metric**.

        Jika kamu menimbang N kriteria, misalnya ukuran berkas model (penting untuk aplikasi ponsel karena pengguna tidak ingin mengunduh aplikasi besar), waktu eksekusi, dan akurasi, pertimbangkan menetapkan N dikurangi 1 kriteria sebagai satisficing. Tetapkan ambang yang dapat diterima untuk ukuran berkas dan waktu, lalu optimalkan akurasi di bawah batasan itu.
        """),
        T("""
        ## Contoh wakeword

        Misalkan kamu membangun perangkat dengan mikrofon yang mendengarkan kata bangun tertentu, seperti "Alexa", "Hey Siri", "Okay Google", atau "Hello Baidu". Kamu peduli pada dua hal: false positive rate, yaitu seberapa sering sistem bangun walau tidak ada yang mengucapkan kata itu, dan false negative rate, yaitu seberapa sering sistem gagal bangun ketika kata itu diucapkan.

        Tujuan yang masuk akal: minimalkan false negative rate (optimizing metric) dengan syarat tidak lebih dari satu false positive per 24 jam operasi (satisficing metric). Perhatikan betapa jelasnya aturan ini. Kamu tidak perlu membobotkan dua jenis kesalahan dalam satu rumus yang sulit dijustifikasi. Cukup satu batas yang bisa dijelaskan kepada siapa pun, dan satu angka untuk dimaksimalkan.

        Setelah tim sepakat pada metrik yang dioptimalkan, mereka dapat bergerak jauh lebih cepat.
        """),
        T("""
        ## Dev set dan metrik mempercepat iterasi

        Hampir mustahil mengetahui di awal pendekatan mana yang paling berhasil untuk masalah baru. Peneliti berpengalaman pun biasanya mencoba puluhan ide sebelum menemukan yang memuaskan. Ketika membangun sistem machine learning, siklusnya: mulai dengan sebuah **ide**, implementasikan dalam **kode**, lalu jalankan **eksperimen** untuk melihat seberapa baik idenya. Biasanya beberapa ide pertama tidak berhasil. Berdasarkan hasil, kembali menghasilkan ide dan terus berputar.

        Semakin cepat putaran ini, semakin cepat kemajuan. Itulah mengapa dev set dan metrik penting. Tanpa keduanya, setiap classifier baru harus dimasukkan ke aplikasi dan dicoba berjam-jam untuk merasakan apakah lebih baik. Itu sangat lambat. Selain itu, perbaikan akurasi dari 95,0 persen ke 95,1 persen tidak terdeteksi dengan mencoba aplikasi secara manual, padahal banyak kemajuan sistem datang dari menumpuk puluhan perbaikan 0,1 persen. Dengan dev set dan metrik, ide yang memberi perbaikan kecil maupun besar terdeteksi cepat, sehingga kamu tahu ide mana yang dilanjutkan dan mana yang dibuang.
        """),
        T("""
        ## Kapan mengubah dev set, test set, dan metrik

        Saat memulai proyek baru, tentukan dev dan test set dengan cepat karena itu memberi tim target yang jelas. Biasanya tim diminta menentukan dev dan test awal serta metrik awal dalam waktu kurang dari seminggu, jarang lebih lama. Lebih baik memulai dengan sesuatu yang tidak sempurna daripada terlalu lama berpikir. Aturan satu minggu itu tidak berlaku untuk aplikasi matang seperti anti-spam, yang timnya bisa menghabiskan berbulan-bulan untuk dev dan test set yang lebih baik.

        Jika kemudian ternyata dev, test, atau metrik awal meleset, segera ubah. Tanda utamanya: dev dan metrik memeringkat A di atas B, tetapi tim yakin B lebih baik untuk produk. Ada tiga penyebab utama:

        1. **Distribusi sebenarnya berbeda.** Misalnya dev awal banyak berisi kucing dewasa, padahal pengguna banyak mengunggah anak kucing. Perbarui dev dan test agar lebih representatif.
        2. **Overfit ke dev set.** Mengevaluasi ide berulang kali pada dev set membuat algoritma perlahan overfit padanya. Jika performa dev jauh lebih baik dari test, ambil dev set baru.
        3. **Metrik mengukur hal yang salah.** Misalnya akurasi memeringkat A lebih baik, tetapi A membiarkan gambar tidak pantas lolos sesekali sehingga tidak dapat diterima. Ganti metrik, misalnya dengan hukuman berat untuk kesalahan itu.

        Boleh melacak kemajuan dengan mengevaluasi sistem secara berkala pada test set, misalnya mingguan. Tetapi jangan gunakan hasilnya untuk keputusan apa pun, termasuk memutuskan rollback. Jika dilakukan, kamu mulai overfit ke test set dan tidak bisa lagi mengandalkannya sebagai estimasi tidak bias.
        """),
        K(
            "warning",
            """
            Mengubah dev set atau metrik di tengah proyek itu normal. Yang berbahaya adalah mengubahnya tanpa memberi tahu tim. Setiap perubahan harus diumumkan agar semua orang mengejar target yang sama.
            """,
        ),
        C(
            """
models = {
    "A": {"akurasi": 0.90, "ms": 80},
    "B": {"akurasi": 0.92, "ms": 95},
    "C": {"akurasi": 0.95, "ms": 1500},
}
batas_ms = 100
layak = {n: m for n, m in models.items() if m["ms"] <= batas_ms}
terbaik = max(layak, key=lambda n: layak[n]["akurasi"])
print("layak:", sorted(layak))
print("terbaik:", terbaik)
""",
            """
            layak: ['A', 'B']
            terbaik: B
            """,
            """
            Waktu eksekusi dijadikan filter (satisficing), lalu akurasi dimaksimalkan di antara yang lolos (optimizing). C paling akurat tetapi gugur oleh batas waktu. Aturan ini bisa dijelaskan dalam satu kalimat kepada siapa pun di tim.
            """,
        ),
        C(
            """
kandidat = {
    "m1": {"fn": 0.08, "fp_per_24j": 0.6},
    "m2": {"fn": 0.05, "fp_per_24j": 1.4},
    "m3": {"fn": 0.06, "fp_per_24j": 0.9},
    "m4": {"fn": 0.12, "fp_per_24j": 0.1},
}
layak = {n: v for n, v in kandidat.items() if v["fp_per_24j"] <= 1.0}
terbaik = min(layak, key=lambda n: (layak[n]["fn"], layak[n]["fp_per_24j"]))
print("layak:", sorted(layak))
print("terbaik:", terbaik)
""",
            """
            layak: ['m1', 'm3', 'm4']
            terbaik: m3
            """,
            """
            Model m2 punya false negative terendah tetapi melanggar batas satu false positive per 24 jam, jadi tersingkir. Di antara yang layak, m3 memiliki false negative terendah. Pola ini sama dengan contoh wakeword pada teks.
            """,
        ),
        C(
            """
import numpy as np

rng = np.random.default_rng(0)
true_acc, n_dev, trials = 0.80, 500, 4000
print("jumlah model dicoba   rata-rata inflasi dev")
for n_model in [1, 5, 50, 500]:
    acc = rng.binomial(n_dev, true_acc, size=(trials, n_model)) / n_dev
    inflasi = float((acc.max(axis=1) - true_acc).mean())
    print(f"{n_model:19d}   {inflasi:.4f}")
""",
            """
            jumlah model dicoba   rata-rata inflasi dev
                              1   sekitar 0.0000
                              5   sekitar 0.02
                             50   sekitar 0.04
                            500   sekitar 0.05
            """,
            """
            Semua model sebenarnya sama baik (akurasi 80 persen). Tetapi bila kamu mencoba banyak ide lalu mengambil yang terbaik di dev set, angka dev yang kamu laporkan lebih tinggi dari kenyataan, dan inflasinya naik dengan banyaknya percobaan. Ini mekanisme overfit ke dev set, dan alasan test set yang tidak disentuh tetap diperlukan.
            """,
        ),
        E(
            "D11-02-3-ex1",
            "mudah",
            """
            Tulis fungsi `pilih_model(models, maks_ms)` yang memilih nama model dengan akurasi tertinggi di antara yang memiliki `ms <= maks_ms`. `models` berbentuk dictionary nama ke dictionary dengan kunci `akurasi` dan `ms`. Kembalikan `None` jika tidak ada yang layak.
            """,
            """
            def pilih_model(models, maks_ms):
                # TODO: implementasikan
                pass
            """,
            """
            models = {
                "A": {"akurasi": 0.90, "ms": 80},
                "B": {"akurasi": 0.92, "ms": 95},
                "C": {"akurasi": 0.95, "ms": 1500},
            }
            assert pilih_model(models, 100) == "B"
            assert pilih_model(models, 2000) == "C"
            assert pilih_model(models, 10) is None
            """,
            "Saring dulu model yang memenuhi batas waktu. Jika hasil saringan kosong kembalikan None, jika tidak ambil max berdasarkan akurasi.",
            """
            def pilih_model(models, maks_ms):
                layak = {n: m for n, m in models.items() if m["ms"] <= maks_ms}
                if not layak:
                    return None
                return max(layak, key=lambda n: layak[n]["akurasi"])
            """,
        ),
        E(
            "D11-02-3-ex2",
            "sedang",
            """
            Tulis fungsi `pilih_wakeword(kandidat, maks_fp)` yang memilih model dengan `fn` terkecil di antara yang `fp_per_24j <= maks_fp`. Jika seri pada `fn`, pilih `fp_per_24j` yang lebih kecil, lalu nama yang lebih dulu secara abjad. Kembalikan `None` jika tidak ada yang layak.
            """,
            """
            def pilih_wakeword(kandidat, maks_fp):
                # TODO: implementasikan
                pass
            """,
            """
            kandidat = {
                "m1": {"fn": 0.08, "fp_per_24j": 0.6},
                "m2": {"fn": 0.05, "fp_per_24j": 1.4},
                "m3": {"fn": 0.06, "fp_per_24j": 0.9},
                "m4": {"fn": 0.12, "fp_per_24j": 0.1},
            }
            assert pilih_wakeword(kandidat, 1.0) == "m3"
            assert pilih_wakeword(kandidat, 2.0) == "m2"
            assert pilih_wakeword(kandidat, 0.05) is None
            seri = {"b": {"fn": 0.1, "fp_per_24j": 0.5}, "a": {"fn": 0.1, "fp_per_24j": 0.5}, "c": {"fn": 0.1, "fp_per_24j": 0.2}}
            assert pilih_wakeword(seri, 1.0) == "c"
            """,
            "Saring dengan batas fp, lalu gunakan key tuple (fn, fp, nama) pada min.",
            """
            def pilih_wakeword(kandidat, maks_fp):
                layak = {n: v for n, v in kandidat.items() if v["fp_per_24j"] <= maks_fp}
                if not layak:
                    return None
                return min(layak, key=lambda n: (layak[n]["fn"], layak[n]["fp_per_24j"], n))
            """,
        ),
        E(
            "D11-02-3-ex3",
            "sedang",
            """
            Tulis fungsi `sinyal_ganti(dev_acc, test_acc, distribusi_berubah, ranking_sesuai_tim)` yang mengembalikan satu dari empat string. Jika `distribusi_berubah` benar kembalikan `"perbarui dev dan test"`. Jika tidak, dan `round(dev_acc - test_acc, 6) > 0.03` kembalikan `"ambil dev set baru"`. Jika tidak, dan `ranking_sesuai_tim` salah kembalikan `"ganti metrik"`. Selain itu kembalikan `"pertahankan"`.
            """,
            """
            def sinyal_ganti(dev_acc, test_acc, distribusi_berubah, ranking_sesuai_tim):
                # TODO: implementasikan
                pass
            """,
            """
            assert sinyal_ganti(0.9, 0.9, True, True) == "perbarui dev dan test"
            assert sinyal_ganti(0.95, 0.88, False, True) == "ambil dev set baru"
            assert sinyal_ganti(0.90, 0.89, False, False) == "ganti metrik"
            assert sinyal_ganti(0.90, 0.89, False, True) == "pertahankan"
            assert sinyal_ganti(0.90, 0.87, False, True) == "pertahankan"
            """,
            "Periksa kondisi secara berurutan sesuai prioritas yang diberikan.",
            """
            def sinyal_ganti(dev_acc, test_acc, distribusi_berubah, ranking_sesuai_tim):
                if distribusi_berubah:
                    return "perbarui dev dan test"
                if round(dev_acc - test_acc, 6) > 0.03:
                    return "ambil dev set baru"
                if not ranking_sesuai_tim:
                    return "ganti metrik"
                return "pertahankan"
            """,
        ),
        E(
            "D11-02-3-ex4",
            "menantang",
            """
            Tulis fungsi `inflasi_best_of_n(true_acc, n_dev, n_models, trials, seed)`. Buat `rng = np.random.default_rng(seed)`, ambil `acc = rng.binomial(n_dev, true_acc, size=(trials, n_models)) / n_dev`, lalu kembalikan rata-rata (float) dari `acc.max(axis=1) - true_acc`. Fungsi ini mengukur seberapa tinggi angka dev terbaik melebihi akurasi sebenarnya.
            """,
            """
            import numpy as np

            def inflasi_best_of_n(true_acc, n_dev, n_models, trials, seed):
                # TODO: implementasikan
                pass
            """,
            """
            i1 = inflasi_best_of_n(0.8, 500, 1, 4000, 0)
            i5 = inflasi_best_of_n(0.8, 500, 5, 4000, 0)
            i50 = inflasi_best_of_n(0.8, 500, 50, 4000, 0)
            assert abs(i1) < 0.003
            assert 0.012 < i5 < 0.03
            assert i5 < i50 < 0.07
            assert isinstance(i50, float)
            assert inflasi_best_of_n(0.8, 500, 5, 4000, 0) == i5
            """,
            "Satu panggilan rng.binomial dengan size=(trials, n_models) cukup. Gunakan max sepanjang axis=1 lalu mean.",
            """
            import numpy as np

            def inflasi_best_of_n(true_acc, n_dev, n_models, trials, seed):
                rng = np.random.default_rng(seed)
                acc = rng.binomial(n_dev, true_acc, size=(trials, n_models)) / n_dev
                return float((acc.max(axis=1) - true_acc).mean())
            """,
        ),
    ],
    [
        M(
            "Menggabungkan akurasi dan waktu eksekusi dalam rumus berbobot yang sulit dijustifikasi.",
            "Tetapkan batas yang dapat diterima untuk satu metrik (satisficing) lalu optimalkan metrik lain.",
        ),
        M(
            "Memakai test set mingguan untuk memutuskan rollback.",
            "Gunakan test set hanya untuk pelacakan, dan ambil keputusan dengan dev set.",
        ),
        M(
            "Terlalu lama menyempurnakan dev set dan metrik awal.",
            "Tetapkan versi pertama dalam kurang dari seminggu untuk aplikasi baru, lalu perbaiki saat terbukti meleset.",
        ),
    ],
    [
        Q(
            "Pada wakeword, mana yang menjadi optimizing metric?",
            ["False positive per 24 jam", "False negative rate", "Ukuran berkas model", "Waktu eksekusi"],
            1,
            "False negative rate diminimalkan dengan syarat false positive per 24 jam tidak lebih dari satu.",
        ),
        Q(
            "Jika menimbang N kriteria, berapa yang dijadikan satisficing?",
            ["N", "N - 1", "1", "0"],
            1,
            "Satu kriteria menjadi optimizing metric dan sisanya N - 1 menjadi satisficing dengan ambang.",
        ),
        Q(
            "Performa dev jauh lebih baik dari test pada distribusi yang sama. Tindakan yang disarankan?",
            ["Ganti metrik", "Ambil dev set baru", "Hapus test set", "Latih lebih lama"],
            1,
            "Itu tanda overfit ke dev set akibat evaluasi berulang, dan solusinya dev set baru.",
        ),
        Q(
            "Apa yang tidak boleh dilakukan dengan hasil evaluasi test set mingguan?",
            ["Dilaporkan ke tim", "Dipakai memutuskan rollback", "Dicatat", "Dibandingkan antar minggu"],
            1,
            "Memakai test set untuk keputusan membuatnya ikut overfit dan tidak lagi bisa menjadi estimasi tidak bias.",
        ),
        Q(
            "Mengapa angka dev terbaik dari 500 percobaan cenderung terlalu optimis?",
            ["Karena data berubah", "Karena memilih maksimum dari banyak pengukuran berderau", "Karena test lebih mudah", "Karena komputasi kurang"],
            1,
            "Maksimum dari banyak pengukuran berderau secara sistematis berada di atas nilai sebenarnya.",
        ),
    ],
    [
        "Pilih satu optimizing metric dan jadikan sisanya satisficing dengan ambang yang jelas.",
        "Siklus ide, kode, eksperimen berjalan jauh lebih cepat dengan dev set dan metrik.",
        "Ubah dev, test, atau metrik bila distribusi berubah, dev overfit, atau metrik salah, dan umumkan ke tim.",
        "Test set tidak dipakai untuk keputusan, dan percobaan berulang pada dev menginflasi angka dev.",
    ],
    ["Machine Learning Yearning, bab 9 sampai 12 (Andrew Ng): metrik optimizing dan satisficing, iterasi, kapan mengubah, dan ringkasan"],
)

video = {
    "needed": True,
    "kind": "ai_slides",
    "reason": "Diagram aliran data web ke ponsel dan ilustrasi derau pengukuran lebih jelas secara visual.",
    "brief": [
        "Slide 1: cerita kucing, training dari web dan pengguna dari ponsel",
        "Slide 2: tiga set data dan perannya",
        "Slide 3: empat wilayah dan mengapa dev dan test harus dicampur",
        "Slide 4: standard error dan ukuran dev set",
        "Slide 5: F1, rata-rata berbobot, dan metrik tunggal",
        "Slide 6: optimizing versus satisficing dengan contoh wakeword",
        "Slide 7: tiga penyebab mengganti dev set atau metrik",
    ],
}

write_module(
    "D11",
    2,
    "Dev set, test set, dan metrik tunggal",
    120,
    [
        "Menentukan dev dan test set dari distribusi yang sama dan mencerminkan data masa depan",
        "Memilih ukuran dev dan test set berdasarkan perbedaan terkecil yang ingin dideteksi",
        "Menetapkan satu metrik optimizing dengan batasan satisficing dan tahu kapan mengubahnya",
    ],
    [l1, l2, l3],
    video,
    REF,
)
