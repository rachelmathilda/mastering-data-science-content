import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, C, E, Q, M, lesson, write_module

REF = [{"book": "Machine Learning Yearning (Andrew Ng)", "chapters": "bab 20 sampai 27"}]

DATA = """
import numpy as np
import warnings
warnings.simplefilter("ignore")

def data(m, seed):
    r = np.random.default_rng(seed)
    x = r.uniform(0, 1, m)
    y = np.sin(2 * np.pi * x) + 0.3 * r.normal(size=m)
    return x, y

OPTIMAL = 0.09
"""

l1 = lesson(
    "D11-05-1",
    "Bias, variance, dan batas error optimal",
    35,
    [
        "Mendefinisikan bias dan variance sebagai sumber error yang praktis",
        "Menghitung avoidable bias dan variance dari error training dan dev",
        "Menjelaskan peran optimal error rate sebagai garis dasar",
        "Mendiagnosis kombinasi bias dan variance dari tiga angka sederhana",
    ],
    [
        T("""
        ## Dua sumber error besar

        Misalkan kamu berharap algoritmamu mencapai error 5 persen, tetapi hasilnya 15 persen. Dua puluh ide bisa muncul sekaligus: tambah data, tambah regularisasi, ganti arsitektur, tambah fitur. Tanpa panduan, kamu memilih berdasarkan firasat. Panduan paling berguna adalah memecah error menjadi dua komponen yang masing-masing punya obat berbeda.

        **Bias** adalah error yang tetap ada pada training set. Algoritmamu belum bisa menyesuaikan diri bahkan dengan data yang ia lihat sendiri. Contoh: classifier kucing memakai model linear sederhana, dan error training-nya 15 persen. Menambah data tidak akan membantu karena model memang terlalu sederhana untuk pola yang ada.

        **Variance** adalah seberapa jauh performa di dev set lebih buruk daripada di training set. Jika error training 1 persen tetapi error dev 11 persen, variance-nya sekitar 10 poin. Algoritmamu menghafal training set dan gagal menggeneralisasi.

        Definisi di sini bersifat praktis, bukan definisi statistik formal. Ng sengaja memakainya agar bias dan variance bisa dibaca langsung dari dua angka yang selalu kamu punya.
        """),
        T("""
        ## Bacalah dari tiga angka

        Tiga bilangan cukup: error training, error dev, dan perkiraan error optimal. Error training dan dev kamu ukur. Error optimal adalah error terbaik yang bisa dicapai sistem apa pun pada tugas itu, yang sering mendekati error manusia ahli atau derau yang melekat pada data.

        Dari ketiganya dihitung: **avoidable bias** sama dengan error training dikurangi error optimal. **Variance** sama dengan error dev dikurangi error training. Total error dev sama dengan error optimal ditambah avoidable bias ditambah variance.

        Contoh: error optimal 2 persen, error training 4 persen, error dev 15 persen. Avoidable bias 2 poin, variance 11 poin. Walau kedua komponen ada, variance jauh lebih besar sehingga perbaikan terbesar ada di sisi variance: data lebih banyak atau regularisasi. Mengupayakan bias di titik ini membuang waktu.
        """),
        T("""
        ## Mengapa perlu error optimal

        Tanpa garis dasar, angka error training hampir tidak bermakna. Error 15 persen pada training set tampak buruk, tetapi bila tugasnya adalah mengenali ucapan di tengah bising yang bahkan manusia salah 14 persen, maka 15 persen hampir sempurna. Ada derau yang memang tidak bisa dihilangkan, yang sering disebut error tak terhindarkan (unavoidable bias) atau Bayes error.

        Karena itu, jangan berhenti pada "bias tinggi" atau "bias rendah". Selalu tanyakan: dibanding apa? Perbandingan yang tepat adalah dengan error optimal. Selisihnya, avoidable bias, adalah satu-satunya bagian bias yang bisa diperbaiki.

        Untuk banyak tugas persepsi seperti gambar atau suara, error manusia ahli menjadi perkiraan yang baik. Untuk tugas dengan derau intrinsik seperti memprediksi respons pelanggan, error optimal bisa tinggi dan tidak diketahui. Dalam kasus itu, kamu menaksirnya dari eksperimen, misalnya dengan melihat di mana model yang makin besar berhenti membaik.
        """),
        T("""
        ## Kombinasi yang mungkin

        Dengan dua komponen, ada empat keadaan sederhana. Bias rendah dan variance rendah berarti kamu sudah dekat dengan optimal. Bias tinggi dan variance rendah berarti model kurang kuat (underfitting). Bias rendah dan variance tinggi berarti model menghafal (overfitting). Keduanya tinggi berarti model yang buruk di training sekaligus tidak menggeneralisasi dengan baik.

        Keadaan terakhir nyata dan terlihat paradoks. Model bisa underfit pada sebagian data dan overfit pada sebagian lainnya, misalnya bila ada kelompok contoh yang sangat berderau dan kelompok lain yang sistematis. Jangan terjebak dikotomi. Hitung kedua angka, lalu kerjakan yang lebih besar dulu.

        Kamu juga bisa melihat efek ini pada contoh regresi polinomial. Derajat 1 tidak mampu mengikuti kurva sinus sehingga error training dan dev sama-sama tinggi. Derajat tinggi dengan data sedikit mengikuti derau sehingga error training sangat rendah tetapi error dev melonjak. Derajat menengah berada di antara keduanya dan mendekati error optimal.
        """),
        K(
            "note",
            """
            Definisi bias dan variance di sini sengaja praktis agar bisa dihitung dari angka yang kamu miliki. Definisi statistik formal berbeda dalam detail, tetapi untuk memutuskan langkah berikutnya definisi praktis lebih berguna.
            """,
        ),
        C(
            """
def uraikan(optimal, train, dev):
    return {"avoidable_bias": round(train - optimal, 4), "variance": round(dev - train, 4)}

print(uraikan(0.02, 0.04, 0.15))
print(uraikan(0.05, 0.15, 0.16))
print(uraikan(0.01, 0.01, 0.11))
""",
            """
            {'avoidable_bias': 0.02, 'variance': 0.11}
            {'avoidable_bias': 0.1, 'variance': 0.01}
            {'avoidable_bias': 0.0, 'variance': 0.1}
            """,
            """
            Tiga skenario dengan total error berbeda tetapi obat berbeda. Skenario pertama didominasi variance. Kedua didominasi avoidable bias. Ketiga murni variance. Satu perhitungan dua pengurangan menunjukkan arah perbaikan.
            """,
        ),
        C(
            DATA
            + """
xt, yt = data(30, 1)
xd, yd = data(2000, 2)
print("derajat  error_train  error_dev  avoidable_bias  variance")
for d in [1, 3, 9, 12]:
    c = np.polyfit(xt, yt, d)
    tr = np.mean((np.polyval(c, xt) - yt) ** 2)
    dv = np.mean((np.polyval(c, xd) - yd) ** 2)
    print(f"{d:7d}  {tr:11.3f}  {dv:9.3f}  {tr - OPTIMAL:14.3f}  {dv - tr:8.3f}")
""",
            """
            derajat 1: error train sekitar 0.27 dan error dev sekitar 0.31
            derajat 3: error train sekitar 0.08 dan error dev sekitar 0.10
            derajat 12: error train sekitar 0.04 dan error dev sekitar 0.40
            """,
            """
            Data sintetis dibangkitkan dari sinus dengan derau berdeviasi baku 0,3, sehingga error optimal adalah variansinya, 0,09. Derajat 1 dominan di avoidable bias. Derajat 12 dominan di variance. Derajat 3 mendekati optimal pada keduanya.
            """,
        ),
        C(
            DATA
            + """
xd, yd = data(2000, 2)
print("m_train  error_train  error_dev")
for m in [20, 40, 80, 160, 640]:
    x, y = data(m, 1)
    c = np.polyfit(x, y, 9)
    tr = np.mean((np.polyval(c, x) - y) ** 2)
    dv = np.mean((np.polyval(c, xd) - yd) ** 2)
    print(f"{m:7d}  {tr:11.3f}  {dv:9.3f}")
""",
            """
            error dev turun dari sekitar 0.42 ke sekitar 0.09 saat data bertambah
            error train naik dari sekitar 0.06 ke sekitar 0.09
            """,
            """
            Model berderajat 9 punya variance besar pada 20 contoh, tetapi celahnya menutup saat data bertambah. Error training naik mendekati error optimal dan error dev turun mendekatinya dari atas. Ini pola khas masalah variance yang bisa dibantu data.
            """,
        ),
        E(
            "D11-05-1-ex1",
            "mudah",
            """
            Tulis fungsi `avoidable_bias(train, optimal)` dan `variance(dev, train)`. Masing-masing mengembalikan selisihnya dibulatkan 4 desimal.
            """,
            """
            def avoidable_bias(train, optimal):
                # TODO: implementasikan
                pass

            def variance(dev, train):
                # TODO: implementasikan
                pass
            """,
            """
            assert avoidable_bias(0.04, 0.02) == 0.02
            assert variance(0.15, 0.04) == 0.11
            assert avoidable_bias(0.10, 0.10) == 0.0
            assert variance(0.12, 0.12) == 0.0
            """,
            "Kurangkan lalu round(..., 4).",
            """
            def avoidable_bias(train, optimal):
                return round(train - optimal, 4)

            def variance(dev, train):
                return round(dev - train, 4)
            """,
        ),
        E(
            "D11-05-1-ex2",
            "sedang",
            """
            Tulis fungsi `diagnosa(optimal, train, dev, toleransi)` yang menghitung avoidable bias dan variance (dibulatkan 4 desimal). Jika keduanya lebih besar dari `toleransi` kembalikan `"bias dan variance"`. Jika hanya bias lebih besar kembalikan `"bias"`. Jika hanya variance lebih besar kembalikan `"variance"`. Jika tidak ada yang lebih besar kembalikan `"baik"`.
            """,
            """
            def diagnosa(optimal, train, dev, toleransi):
                # TODO: implementasikan
                pass
            """,
            """
            assert diagnosa(0.02, 0.04, 0.15, 0.01) == "bias dan variance"
            assert diagnosa(0.05, 0.15, 0.16, 0.02) == "bias"
            assert diagnosa(0.01, 0.01, 0.11, 0.02) == "variance"
            assert diagnosa(0.05, 0.06, 0.07, 0.02) == "baik"
            assert diagnosa(0.05, 0.07, 0.09, 0.02) == "baik"
            """,
            "Gunakan strict greater than. Nilai tepat sama dengan toleransi dianggap belum melewati batas.",
            """
            def diagnosa(optimal, train, dev, toleransi):
                b = round(train - optimal, 4)
                v = round(dev - train, 4)
                if b > toleransi and v > toleransi:
                    return "bias dan variance"
                if b > toleransi:
                    return "bias"
                if v > toleransi:
                    return "variance"
                return "baik"
            """,
        ),
        E(
            "D11-05-1-ex3",
            "sedang",
            """
            Tulis fungsi `error_poli(derajat, seed_train, seed_dev)` yang membangkitkan `x ~ U(0,1)` dan `y = sin(2*pi*x) + 0.3*N(0,1)` dengan `np.random.default_rng(seed)`. Gunakan 30 contoh untuk training dan 2000 untuk dev. Urutan: `x = r.uniform(0, 1, m)` lalu `y = np.sin(2 * np.pi * x) + 0.3 * r.normal(size=m)`. Fit `np.polyfit(x, y, derajat)`. Kembalikan `(mse_train, mse_dev)` dibulatkan 4 desimal.
            """,
            """
            import numpy as np
            import warnings
            warnings.simplefilter("ignore")

            def error_poli(derajat, seed_train, seed_dev):
                # TODO: implementasikan
                pass
            """,
            """
            tr1, dv1 = error_poli(1, 1, 2)
            tr3, dv3 = error_poli(3, 1, 2)
            tr12, dv12 = error_poli(12, 1, 2)
            assert tr1 > tr3 > tr12
            assert dv1 > dv3
            assert dv12 > dv3 * 2
            assert abs(dv3 - 0.09) < 0.04
            """,
            "Bangun fungsi pembangkit lokal. Gunakan rng baru per seed. MSE adalah rata-rata kuadrat selisih.",
            """
            import numpy as np
            import warnings
            warnings.simplefilter("ignore")

            def _data(m, seed):
                r = np.random.default_rng(seed)
                x = r.uniform(0, 1, m)
                y = np.sin(2 * np.pi * x) + 0.3 * r.normal(size=m)
                return x, y

            def error_poli(derajat, seed_train, seed_dev):
                xt, yt = _data(30, seed_train)
                xd, yd = _data(2000, seed_dev)
                c = np.polyfit(xt, yt, derajat)
                tr = np.mean((np.polyval(c, xt) - yt) ** 2)
                dv = np.mean((np.polyval(c, xd) - yd) ** 2)
                return round(float(tr), 4), round(float(dv), 4)
            """,
        ),
        E(
            "D11-05-1-ex4",
            "menantang",
            """
            Tulis fungsi `derajat_terbaik(derajat_list, seed_train, seed_dev)` yang memakai `error_poli` (sudah disediakan) dan mengembalikan derajat dengan MSE dev terendah. Jika seri pilih derajat terkecil.
            """,
            """
            import numpy as np
            import warnings
            warnings.simplefilter("ignore")

            def _data(m, seed):
                r = np.random.default_rng(seed)
                x = r.uniform(0, 1, m)
                y = np.sin(2 * np.pi * x) + 0.3 * r.normal(size=m)
                return x, y

            def error_poli(derajat, seed_train, seed_dev):
                xt, yt = _data(30, seed_train)
                xd, yd = _data(2000, seed_dev)
                c = np.polyfit(xt, yt, derajat)
                tr = np.mean((np.polyval(c, xt) - yt) ** 2)
                dv = np.mean((np.polyval(c, xd) - yd) ** 2)
                return round(float(tr), 4), round(float(dv), 4)

            def derajat_terbaik(derajat_list, seed_train, seed_dev):
                # TODO: implementasikan
                pass
            """,
            """
            assert derajat_terbaik([1, 3, 12], 1, 2) == 3
            assert derajat_terbaik([12, 1], 1, 2) == 1
            assert derajat_terbaik([3, 3], 1, 2) == 3
            assert derajat_terbaik([5, 3, 4], 1, 2) in (3, 4, 5)
            """,
            "Gunakan min dengan key berupa tuple (mse_dev, derajat).",
            """
            import numpy as np
            import warnings
            warnings.simplefilter("ignore")

            def _data(m, seed):
                r = np.random.default_rng(seed)
                x = r.uniform(0, 1, m)
                y = np.sin(2 * np.pi * x) + 0.3 * r.normal(size=m)
                return x, y

            def error_poli(derajat, seed_train, seed_dev):
                xt, yt = _data(30, seed_train)
                xd, yd = _data(2000, seed_dev)
                c = np.polyfit(xt, yt, derajat)
                tr = np.mean((np.polyval(c, xt) - yt) ** 2)
                dv = np.mean((np.polyval(c, xd) - yd) ** 2)
                return round(float(tr), 4), round(float(dv), 4)

            def derajat_terbaik(derajat_list, seed_train, seed_dev):
                return min(derajat_list, key=lambda d: (error_poli(d, seed_train, seed_dev)[1], d))
            """,
        ),
    ],
    [
        M(
            "Menilai error training tinggi sebagai bias buruk tanpa membandingkan dengan error optimal.",
            "Hitung avoidable bias sebagai error training dikurangi error optimal.",
        ),
        M(
            "Mengira bias dan variance saling meniadakan sehingga hanya salah satu yang ada.",
            "Keduanya bisa tinggi sekaligus, jadi hitung keduanya dan kerjakan yang lebih besar.",
        ),
        M(
            "Menambah data untuk masalah bias.",
            "Data tambahan membantu variance. Untuk bias ubah model atau fitur.",
        ),
    ],
    [
        Q(
            "Error optimal 2, error training 4, error dev 15 (persen). Berapa variance?",
            ["2", "11", "13", "15"],
            1,
            "Variance sama dengan error dev dikurangi error training, yaitu 15 dikurangi 4 sama dengan 11.",
        ),
        Q(
            "Apa arti avoidable bias?",
            ["Error dev dikurangi training", "Error training dikurangi error optimal", "Error test", "Selisih dua model"],
            1,
            "Bagian bias yang masih bisa dikurangi karena tidak termasuk error tak terhindarkan.",
        ),
        Q(
            "Error training 15 persen, tetapi manusia ahli juga salah 14 persen. Kesimpulan?",
            ["Bias sangat besar", "Avoidable bias kecil, sekitar 1 poin", "Variance besar", "Dev set rusak"],
            1,
            "Error manusia menjadi perkiraan error optimal, sehingga avoidable bias hanya sekitar 1 poin.",
        ),
        Q(
            "Model polinomial derajat tinggi dengan 30 contoh: error training sangat kecil, error dev besar. Masalahnya?",
            ["Bias", "Variance", "Label salah", "Metrik"],
            1,
            "Celah besar antara training dan dev adalah variance.",
        ),
        Q(
            "Bias dan variance sama-sama besar. Strategi paling masuk akal?",
            ["Tidak melakukan apa pun", "Kerjakan yang lebih besar dulu", "Ganti metrik", "Hapus dev set"],
            1,
            "Perbaikan terbesar ada di komponen yang lebih besar.",
        ),
    ],
    [
        "Bias adalah error pada training, variance adalah selisih dev terhadap training.",
        "Avoidable bias sama dengan error training dikurangi error optimal.",
        "Error optimal sering didekati error manusia ahli atau derau data.",
        "Total error dev sama dengan optimal ditambah avoidable bias ditambah variance.",
    ],
    ["Machine Learning Yearning, bab 20 sampai 22 (Andrew Ng): bias, variance, dan error optimal"],
)

l2 = lesson(
    "D11-05-2",
    "Mengatasi bias dan variance serta tradeoff-nya",
    35,
    [
        "Memetakan diagnosis bias atau variance ke tindakan perbaikan yang relevan",
        "Menjelaskan mengapa tradeoff bias variance tidak selalu berlaku di era data besar",
        "Menggunakan regularisasi dan kapasitas model sebagai tuas dan membacanya dari dua error",
        "Menentukan urutan prioritas ketika bias dan variance sama-sama ada",
    ],
    [
        T("""
        ## Rumus paling sederhana

        Ng meringkas strategi dasar dalam satu kalimat: jika avoidable bias tinggi, tambah kapasitas model, misalnya jaringan lebih besar atau lebih banyak lapisan. Jika variance tinggi, tambah data latih. Dalam banyak kasus, dua tindakan itu saja sudah menjadi sebagian besar kemajuan, selama kamu punya akses ke banyak data dan daya komputasi.

        Alasannya intuitif. Model yang lebih besar mampu menyesuaikan diri lebih baik dengan training set sehingga error training turun. Data yang lebih banyak membuat celah antara training dan dev menyempit karena model sulit menghafal sesuatu yang lebih besar. Dengan keduanya, kamu bisa terus mendorong angka ke bawah, asalkan kamu tahu sedang berada di sisi mana.

        Peringatan: model besar membawa risiko variance dan menuntut regularisasi bila data tidak cukup. Data besar membawa biaya pelabelan dan penyimpanan. Dua tuas itu bukan gratis, tetapi biayanya terukur, jauh lebih terukur daripada trial and error tanpa arah.
        """),
        T("""
        ## Tradeoff yang sering dibicarakan

        Dalam buku teks klasik, bias dan variance dianggap bertukar: menurunkan satu menaikkan yang lain. Menambah kapasitas model menurunkan bias tetapi menaikkan variance. Menambah regularisasi menurunkan variance tetapi menaikkan bias. Pada kurva derajat polinomial yang kamu lihat di lesson sebelumnya, itu terlihat jelas.

        Tetapi di era data besar, tradeoff itu tidak lagi menjadi batasan. Kalau kamu punya akses ke data yang sangat banyak, kamu bisa menambah ukuran model dan data sekaligus dan menurunkan keduanya. Regularisasi yang dirancang baik juga bisa menurunkan variance tanpa menaikkan bias secara berarti. Itu sebabnya Ng menekankan bahwa tradeoff bukan hukum alam, melainkan kondisi ketika sumber dayamu terbatas.

        Konsekuensi praktis: jangan pasrah pada alasan "ini tradeoff" bila kamu masih punya jalan lain. Tanyakan apakah menambah data atau memilih arsitektur lebih baik memungkinkan kamu bergerak ke arah yang lebih baik di kedua sumbu.
        """),
        T("""
        ## Regularisasi sebagai tuas

        Regularisasi membatasi kebebasan model. Pada ridge regression, penalti `alpha` pada kuadrat koefisien membuat koefisien kecil dan kurva lebih halus. Dengan alpha sangat kecil model menyesuaikan diri bebas dan variance besar. Dengan alpha sangat besar model hampir konstan dan bias besar. Di antaranya ada nilai yang meminimalkan error dev.

        Cara membaca hasilnya: lihat dua kolom, error training dan error dev. Ketika alpha naik, error training biasanya naik bertahap. Error dev awalnya turun karena variance berkurang, lalu naik ketika bias mulai mendominasi. Titik terendah error dev adalah pilihan alpha yang masuk akal, dan jumlah dua komponen (bias plus variance) sama dengan error di dev.

        Prosedur yang sama berlaku untuk tuas lain: ukuran jaringan, jumlah pohon, kedalaman pohon, early stopping. Selalu jalankan sapuan (sweep), catat error training dan dev, dan baca polanya, bukan hanya angka terendah.
        """),
        T("""
        ## Urutan prioritas

        Jika avoidable bias 8 poin dan variance 2 poin, mulailah dari bias. Jika bias 1 poin dan variance 9 poin, mulailah dari variance. Jika kedua hampir sama, pilih yang biayanya lebih rendah. Menambah data bisa mahal, sedangkan menambah ukuran model sering murah. Mengubah arsitektur menuntut waktu riset.

        Satu hal lagi yang sering dilupakan: setiap tindakan bisa menggeser sisi lain. Setelah menambah kapasitas model, ukur ulang kedua komponen. Jangan mengandaikan bias sudah teratasi hanya karena kamu membesarkan jaringan. Diagnosis adalah ritual yang diulang setiap iterasi, bukan satu kali di awal proyek.
        """),
        T("""
        ## Contoh alur keputusan dalam satu iterasi

        Misalkan classifier-mu menghasilkan error optimal 3 persen, training 9 persen, dev 12 persen. Avoidable bias 6 poin dan variance 3 poin. Kamu mulai dari bias dan memperbesar model dua kali lipat. Hasil baru: training 5 persen, dev 9 persen. Avoidable bias 2 poin, variance 4 poin. Perhatikan bahwa variance ikut naik karena model lebih besar. Sekarang komponen terbesar berpindah ke variance, jadi giliran regularisasi atau data.

        Setelah menambah regularisasi ringan: training 6 persen, dev 8 persen. Avoidable bias 3, variance 2. Total error dev turun dari 12 ke 8 persen dalam dua langkah, dan di tiap langkah kamu tahu mengapa memilih tindakan itu. Pola kerja yang sama bisa diulang sampai sisa error mendekati batas optimal atau sampai biaya perbaikan tidak lagi sepadan.
        """),
        K(
            "tip",
            """
            Setelah tiap perubahan, catat tiga angka: error training, error dev, dan error optimal. Tiga baris catatan itu cukup untuk menceritakan seluruh riwayat proyekmu.
            """,
        ),
        C(
            """
TINDAKAN = {
    "bias": ["perbesar model", "tambah fitur dari error analysis", "kurangi regularisasi", "ubah arsitektur"],
    "variance": ["tambah data latih", "tambah regularisasi", "early stopping", "kurangi ukuran model", "seleksi fitur"],
}

def saran(bias, variance):
    kunci = "bias" if bias >= variance else "variance"
    return kunci, TINDAKAN[kunci][:2]

print(saran(0.08, 0.02))
print(saran(0.01, 0.09))
""",
            """
            ('bias', ['perbesar model', 'tambah fitur dari error analysis'])
            ('variance', ['tambah data latih', 'tambah regularisasi'])
            """,
            """
            Fungsi sederhana memetakan komponen error terbesar ke dua tindakan teratas. Daftar lengkapnya dibahas di lesson berikutnya.
            """,
        ),
        C(
            DATA
            + """
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures

xt, yt = data(30, 1)
xd, yd = data(2000, 2)
P = PolynomialFeatures(9)
Xt = P.fit_transform(xt[:, None])
Xd = P.transform(xd[:, None])
print("alpha        train    dev")
for a in [1e-8, 1e-6, 1e-4, 1e-2, 1, 10]:
    m = Ridge(alpha=a).fit(Xt, yt)
    tr = np.mean((m.predict(Xt) - yt) ** 2)
    dv = np.mean((m.predict(Xd) - yd) ** 2)
    print(f"{a:8.0e}  {tr:7.3f}  {dv:6.3f}")
""",
            """
            error dev terendah sekitar 0.11 pada alpha sekitar 1e-4 sampai 1e-6
            error train naik terus dari sekitar 0.05 ke sekitar 0.37 saat alpha membesar
            """,
            """
            Alpha kecil membuat variance bertahan tinggi, alpha besar mengundang bias besar. Titik terbaik ada di tengah. Error training naik secara monoton, error dev berbentuk huruf U.
            """,
        ),
        C(
            DATA
            + """
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures

xd, yd = data(2000, 2)
P = PolynomialFeatures(9)
Xd = P.fit_transform(xd[:, None])
print("m_train  dev(alpha=1e-6)  dev(alpha=1e-2)")
for m in [20, 40, 80, 320, 1280]:
    x, y = data(m, 1)
    X = P.transform(x[:, None])
    d1 = np.mean((Ridge(alpha=1e-6).fit(X, y).predict(Xd) - yd) ** 2)
    d2 = np.mean((Ridge(alpha=1e-2).fit(X, y).predict(Xd) - yd) ** 2)
    print(f"{m:7d}  {d1:15.3f}  {d2:15.3f}")
""",
            """
            error dev kedua alpha turun dari sekitar 0.2 menuju 0.09 saat data bertambah
            pada data besar kedua alpha berhimpit di sekitar 0.09
            """,
            """
            Dengan data sangat sedikit regularisasi kuat sedikit membantu, tetapi pada ukuran menengah alpha kecil justru lebih baik. Ketika data bertambah, perbedaan menghilang karena data sendiri sudah mengurangi variance. Dua obat variance ini saling menggantikan.
            """,
        ),
        E(
            "D11-05-2-ex1",
            "mudah",
            """
            Tulis fungsi `tindakan_utama(bias, variance)` yang mengembalikan `"kapasitas"` bila `bias >= variance` dan `"data"` selainnya.
            """,
            """
            def tindakan_utama(bias, variance):
                # TODO: implementasikan
                pass
            """,
            """
            assert tindakan_utama(0.08, 0.02) == "kapasitas"
            assert tindakan_utama(0.01, 0.09) == "data"
            assert tindakan_utama(0.05, 0.05) == "kapasitas"
            """,
            "Bandingkan dua angka dengan >=.",
            """
            def tindakan_utama(bias, variance):
                return "kapasitas" if bias >= variance else "data"
            """,
        ),
        E(
            "D11-05-2-ex2",
            "sedang",
            """
            Tulis fungsi `alpha_terbaik(alphas, err_dev)` yang mengembalikan alpha dengan error dev terendah. Jika seri pilih alpha terkecil. Dua list sama panjang.
            """,
            """
            def alpha_terbaik(alphas, err_dev):
                # TODO: implementasikan
                pass
            """,
            """
            assert alpha_terbaik([0.001, 0.01, 0.1, 1], [0.30, 0.12, 0.15, 0.40]) == 0.01
            assert alpha_terbaik([1, 0.1, 10], [0.2, 0.2, 0.5]) == 0.1
            assert alpha_terbaik([5], [0.3]) == 5
            """,
            "Pasangkan tiap alpha dengan errornya dan ambil minimum atas (error, alpha).",
            """
            def alpha_terbaik(alphas, err_dev):
                return min(zip(err_dev, alphas))[1]
            """,
        ),
        E(
            "D11-05-2-ex3",
            "sedang",
            """
            Tulis fungsi `sapuan_ridge(Xt, yt, Xd, yd, alphas)` yang mengembalikan list tuple `(alpha, mse_train, mse_dev)` untuk tiap alpha memakai `sklearn.linear_model.Ridge(alpha=alpha)`. MSE dibulatkan 4 desimal.
            """,
            """
            import numpy as np
            from sklearn.linear_model import Ridge

            def sapuan_ridge(Xt, yt, Xd, yd, alphas):
                # TODO: implementasikan
                pass
            """,
            """
            import numpy as np
            rng = np.random.default_rng(0)
            Xt = rng.normal(size=(40, 8)); w = np.array([2.0, -1, 0, 0, 0, 0, 0, 0])
            yt = Xt @ w + rng.normal(size=40)
            Xd = rng.normal(size=(500, 8)); yd = Xd @ w + rng.normal(size=500)
            hasil = sapuan_ridge(Xt, yt, Xd, yd, [0.001, 1, 100])
            assert [h[0] for h in hasil] == [0.001, 1, 100]
            assert hasil[0][1] <= hasil[1][1] <= hasil[2][1]
            assert hasil[2][2] > hasil[1][2]
            assert all(len(h) == 3 for h in hasil)
            """,
            "Latih Ridge per alpha, hitung np.mean((prediksi - y) ** 2) untuk train dan dev.",
            """
            import numpy as np
            from sklearn.linear_model import Ridge

            def sapuan_ridge(Xt, yt, Xd, yd, alphas):
                hasil = []
                for a in alphas:
                    m = Ridge(alpha=a).fit(Xt, yt)
                    tr = float(np.mean((m.predict(Xt) - yt) ** 2))
                    dv = float(np.mean((m.predict(Xd) - yd) ** 2))
                    hasil.append((a, round(tr, 4), round(dv, 4)))
                return hasil
            """,
        ),
        E(
            "D11-05-2-ex4",
            "menantang",
            """
            Tulis fungsi `rencana(optimal, train, dev, biaya)` dengan `biaya` dictionary berisi kunci `"bias"` dan `"variance"` (biaya relatif per poin perbaikan). Hitung avoidable bias dan variance. Skor tiap komponen adalah `nilai / biaya`. Kembalikan `"bias"` bila skor bias lebih besar atau sama dengan skor variance, selainnya `"variance"`.
            """,
            """
            def rencana(optimal, train, dev, biaya):
                # TODO: implementasikan
                pass
            """,
            """
            assert rencana(0.02, 0.10, 0.12, {"bias": 1, "variance": 1}) == "bias"
            assert rencana(0.02, 0.04, 0.16, {"bias": 1, "variance": 1}) == "variance"
            assert rencana(0.02, 0.10, 0.12, {"bias": 10, "variance": 1}) == "variance"
            assert rencana(0.02, 0.06, 0.10, {"bias": 1, "variance": 1}) == "bias"
            """,
            "Bias 0.08 dengan biaya 10 menghasilkan skor 0.008, lebih kecil dari variance 0.02 dengan biaya 1.",
            """
            def rencana(optimal, train, dev, biaya):
                bias = round(train - optimal, 6)
                var = round(dev - train, 6)
                skor_b = bias / biaya["bias"]
                skor_v = var / biaya["variance"]
                return "bias" if skor_b >= skor_v else "variance"
            """,
        ),
    ],
    [
        M(
            "Menambah data untuk memperbaiki underfitting.",
            "Underfitting dibantu kapasitas dan fitur, bukan data tambahan.",
        ),
        M(
            "Menganggap tradeoff bias variance selalu mengikat.",
            "Dengan data dan komputasi cukup, kapasitas dan data bisa dinaikkan bersama.",
        ),
        M(
            "Mengambil nilai regularisasi dari satu angka terendah tanpa melihat training error.",
            "Baca kedua error dalam sapuan agar tahu apakah kamu di sisi bias atau variance.",
        ),
    ],
    [
        Q(
            "Avoidable bias tinggi. Tindakan paling relevan?",
            ["Tambah data", "Perbesar model atau tambah fitur", "Tambah dropout", "Kurangi ukuran model"],
            1,
            "Bias dibantu dengan kapasitas dan fitur yang lebih baik.",
        ),
        Q(
            "Variance tinggi. Tindakan paling relevan?",
            ["Kurangi regularisasi", "Tambah data latih", "Perbesar model", "Ganti metrik"],
            1,
            "Data lebih banyak mempersempit celah training dan dev.",
        ),
        Q(
            "Mengapa tradeoff bias variance tidak selalu mengikat?",
            ["Karena itu mitos", "Dengan data besar dan regularisasi baik, keduanya bisa turun bersama", "Karena model tidak punya bias", "Karena dev set kecil"],
            1,
            "Menambah data dan kapasitas sekaligus bisa menurunkan bias dan variance.",
        ),
        Q(
            "Alpha ridge naik dari kecil ke besar. Pola error training?",
            ["Turun", "Naik bertahap", "Konstan", "Acak"],
            1,
            "Regularisasi yang lebih kuat membatasi model sehingga error training naik.",
        ),
        Q(
            "Bias 1 poin dan variance 9 poin. Mulai dari mana?",
            ["Bias", "Variance", "Keduanya acak", "Metrik"],
            1,
            "Kerjakan komponen terbesar dulu.",
        ),
    ],
    [
        "Bias dibantu kapasitas dan fitur, variance dibantu data dan regularisasi.",
        "Tradeoff bias variance bukan hukum alam di era data besar.",
        "Sapuan hyperparameter dibaca dari dua error, bukan dari satu angka dev.",
        "Ukur ulang kedua komponen setelah setiap perubahan.",
    ],
    ["Machine Learning Yearning, bab 23 dan 24 (Andrew Ng): mengatasi bias dan variance serta tradeoff-nya"],
)

l3 = lesson(
    "D11-05-3",
    "Teknik mengurangi bias dan variance",
    35,
    [
        "Menyebutkan dan mengurutkan teknik untuk mengurangi avoidable bias",
        "Menyebutkan dan mengurutkan teknik untuk mengurangi variance",
        "Memakai early stopping dan ukuran model sebagai eksperimen terkontrol",
        "Menghitung efek penambahan data pada celah training dan dev",
    ],
    [
        T("""
        ## Teknik untuk mengurangi avoidable bias

        Berikut tuas untuk avoidable bias, diurutkan dari yang biasanya paling murah.

        **Perbesar model.** Tambah neuron, lapisan, pohon, atau derajat. Ini meningkatkan kemampuan model menyesuaikan diri dengan training set. Risiko variance naik, tetapi bila itu terjadi kamu menanganinya dengan regularisasi atau data. Dengan toolkit modern, tuas ini mudah dan sering ampuh.

        **Ubah fitur dari error analysis.** Periksa contoh training yang masih salah, cari pola, lalu tambah fitur yang menjawabnya. Fitur baru memberi model informasi yang tidak ia miliki sebelumnya.

        **Kurangi atau hilangkan regularisasi.** Regularisasi L2, L1, atau dropout membatasi model. Jika bias tinggi, longgarkan. Ingat bahwa ini menaikkan variance, jadi pantau celah.

        **Ubah arsitektur atau keluarga model.** Misalnya dari model linear ke pohon, atau dari jaringan penuh ke jaringan konvolusi. Ini lebih mahal dan hasilnya tidak pasti, tetapi kadang satu-satunya jalan bila model lama tidak cocok dengan struktur data.

        Teknik yang sering salah dipakai untuk bias adalah menambah data. Pada masalah bias murni, model tetap tidak mampu menyesuaikan diri dengan training, sehingga lebih banyak contoh tidak mengubah kemampuan tersebut.
        """),
        T("""
        ## Teknik untuk mengurangi variance

        Tuas untuk variance juga berderet.

        **Tambah data latih.** Ini cara paling andal selama kamu punya akses ke data yang sesuai distribusinya. Kelemahannya biaya: pengumpulan, pelabelan, penyimpanan, dan waktu latih.

        **Tambah regularisasi.** L2, L1, dropout, atau batas kedalaman pohon. Murah untuk dicoba, tetapi dapat menaikkan bias jika berlebihan.

        **Tambah early stopping.** Hentikan latihan saat error dev berhenti turun. Teknik ini menjaga model agar tidak menghafal. Konsekuensinya, error training tidak diminimalkan sepenuhnya, jadi bias bisa sedikit naik.

        **Seleksi fitur.** Buang fitur yang tidak membantu agar model tidak punya ruang untuk menghafal derau. Berguna bila banyak fitur dan sedikit data, dan kurang berguna ketika data melimpah.

        **Kurangi ukuran model.** Membuang neuron atau lapisan. Dalam praktik, ini kurang disukai karena regularisasi dan data lebih baik daripada sekadar membatasi kapasitas.

        **Modifikasi arsitektur.** Arsitektur dengan induktif bias yang cocok, seperti konvolusi untuk gambar, mengurangi parameter efektif dan variance.
        """),
        T("""
        ## Dua tuas yang tidak perlu mengorbankan keduanya

        Dua teknik layak disorot karena sering membantu kedua komponen sekaligus. Pertama, perubahan arsitektur yang cocok dengan masalah. Arsitektur yang tepat memberi model bias induktif yang benar sehingga ia belajar pola nyata dengan lebih sedikit parameter dan lebih sedikit derau.

        Kedua, ketika kamu menambah ukuran model dan data bersamaan. Model yang lebih besar menurunkan bias, dan data tambahan menutup celah variance yang ditimbulkan model besar itu. Kombinasi inilah yang melandasi perkembangan pembelajaran mendalam selama sepuluh tahun terakhir.

        Perlu dicatat pula bahwa teknik di atas bersifat heuristik. Ada kasus ketika perilakunya berbeda dari yang diharapkan. Karena itu, buat eksperimen terkontrol: ubah satu hal, ukur ulang tiga angka, lalu putuskan. Jangan menggabungkan lima perubahan dalam satu percobaan karena kamu tidak akan tahu mana yang bekerja.
        """),
        T("""
        ## Early stopping sebagai eksperimen

        Pada pelatihan iteratif seperti gradient descent, error training turun terus seiring epoch. Error dev biasanya turun lalu naik kembali ketika model mulai menghafal. Early stopping memilih epoch ketika error dev terendah. Implementasinya sederhana: simpan error dev tiap epoch, lalu ambil indeks minimum. Biasanya dipakai kesabaran (patience), yaitu berhenti bila tidak ada perbaikan selama beberapa epoch berturut-turut.

        Hati-hati: karena kamu memakai dev set untuk memilih epoch, dev set ikut dipakai untuk penyetelan. Seperti dibahas di modul sebelumnya, ini sah selama dev set tidak dipakai sampai habis dan test set tetap bersih.
        """),
        K(
            "warning",
            """
            Early stopping bukan obat universal. Jika bias tinggi, menghentikan pelatihan lebih awal justru memperburuk error training. Pakai hanya setelah bias kamu anggap cukup rendah.
            """,
        ),
        C(
            """
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import make_moons

X, y = make_moons(n_samples=1200, noise=0.35, random_state=0)
Xt, yt, Xd, yd = X[:200], y[:200], X[200:], y[200:]
print("neuron  err_train  err_dev")
for h in [1, 2, 8, 64]:
    m = MLPClassifier(hidden_layer_sizes=(h,), max_iter=3000, random_state=0, tol=1e-6).fit(Xt, yt)
    print(f"{h:6d}  {1 - m.score(Xt, yt):9.3f}  {1 - m.score(Xd, yd):7.3f}")
""",
            """
            error train turun dari sekitar 0.145 ke sekitar 0.075 saat neuron bertambah
            error dev turun dari sekitar 0.15 ke sekitar 0.10
            """,
            """
            Jaringan satu neuron hanya membuat batas linear sehingga tidak bisa mengikuti dua bulan sabit. Menambah neuron menurunkan error training dan dev. Celah antara keduanya melebar pada model besar, tanda variance mulai tumbuh.
            """,
        ),
        C(
            """
import numpy as np

dev = [0.40, 0.31, 0.25, 0.22, 0.21, 0.22, 0.24, 0.27]

def epoch_terbaik(errs, patience=2):
    terbaik, idx, sabar = float("inf"), 0, 0
    for i, e in enumerate(errs):
        if e < terbaik:
            terbaik, idx, sabar = e, i, 0
        else:
            sabar += 1
            if sabar >= patience:
                break
    return idx, terbaik

print(epoch_terbaik(dev))
""",
            """
            (4, 0.21)
            """,
            """
            Early stopping dengan kesabaran 2 berhenti setelah dua epoch tanpa perbaikan dan mengembalikan epoch ke-5 (indeks 4) dengan error dev 0,21. Lompatan kecil derau di epoch 3 tidak langsung memicu berhenti.
            """,
        ),
        C(
            """
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import make_moons

X, y = make_moons(n_samples=6000, noise=0.35, random_state=0)
Xd, yd = X[-2000:], y[-2000:]
print("m_train  err_train  err_dev  celah")
for m in [30, 100, 300, 1000, 4000]:
    k = KNeighborsClassifier(n_neighbors=1).fit(X[:m], y[:m])
    tr = 1 - k.score(X[:m], y[:m])
    dv = 1 - k.score(Xd, yd)
    print(f"{m:7d}  {tr:9.3f}  {dv:7.3f}  {dv - tr:5.3f}")
""",
            """
            error train 1-NN selalu 0
            error dev berkisar 0.145 sampai 0.165 dan hampir tidak turun
            celah tetap sekitar 0.15
            """,
            """
            Tetangga terdekat menghafal training sehingga error training nol dan seluruh error adalah variance. Karena label berderau, data tambahan nyaris tidak membantu model ini. Obat yang tepat adalah regularisasi, misalnya k tetangga yang lebih besar, bukan sekadar menambah data.
            """,
        ),
        E(
            "D11-05-3-ex1",
            "mudah",
            """
            Tulis fungsi `epoch_terbaik(errs)` yang mengembalikan indeks error dev terendah. Jika seri pilih indeks paling awal.
            """,
            """
            def epoch_terbaik(errs):
                # TODO: implementasikan
                pass
            """,
            """
            assert epoch_terbaik([0.4, 0.3, 0.25, 0.27]) == 2
            assert epoch_terbaik([0.3, 0.2, 0.2, 0.25]) == 1
            assert epoch_terbaik([0.5]) == 0
            """,
            "Gunakan min atas range dengan key (errs[i], i).",
            """
            def epoch_terbaik(errs):
                return min(range(len(errs)), key=lambda i: (errs[i], i))
            """,
        ),
        E(
            "D11-05-3-ex2",
            "sedang",
            """
            Tulis fungsi `early_stop(errs, patience)` yang membaca error dev urut per epoch. Simpan error terbaik dan hitung epoch berturut-turut tanpa perbaikan strict. Berhenti saat hitungan mencapai `patience`. Kembalikan tuple `(indeks_terbaik, error_terbaik)`. Jika tidak pernah berhenti, kembalikan terbaik dari seluruh list.
            """,
            """
            def early_stop(errs, patience):
                # TODO: implementasikan
                pass
            """,
            """
            dev = [0.40, 0.31, 0.25, 0.22, 0.21, 0.22, 0.24, 0.27]
            assert early_stop(dev, 2) == (4, 0.21)
            assert early_stop(dev, 5) == (4, 0.21)
            assert early_stop([0.3, 0.2, 0.19], 3) == (2, 0.19)
            assert early_stop([0.3, 0.31, 0.32, 0.2], 2) == (0, 0.3)
            assert early_stop([0.3, 0.31, 0.2], 2) == (2, 0.2)
            """,
            "Perbaikan harus strict lebih kecil. Reset hitungan saat ada perbaikan.",
            """
            def early_stop(errs, patience):
                terbaik, idx, sabar = float("inf"), 0, 0
                for i, e in enumerate(errs):
                    if e < terbaik:
                        terbaik, idx, sabar = e, i, 0
                    else:
                        sabar += 1
                        if sabar >= patience:
                            break
                return idx, terbaik
            """,
        ),
        E(
            "D11-05-3-ex3",
            "sedang",
            """
            Tulis fungsi `celah_vs_data(ukuran, err_train, err_dev)` yang menerima tiga list sama panjang dan mengembalikan list tuple `(ukuran, celah)` dengan `celah = round(err_dev - err_train, 4)`, diurutkan menurut ukuran naik.
            """,
            """
            def celah_vs_data(ukuran, err_train, err_dev):
                # TODO: implementasikan
                pass
            """,
            """
            r = celah_vs_data([100, 20, 50], [0.05, 0.0, 0.02], [0.15, 0.30, 0.20])
            assert r == [(20, 0.3), (50, 0.18), (100, 0.1)]
            assert celah_vs_data([], [], []) == []
            assert celah_vs_data([1], [0.1], [0.3]) == [(1, 0.2)]
            """,
            "Gabungkan dengan zip, hitung celah, lalu sorted.",
            """
            def celah_vs_data(ukuran, err_train, err_dev):
                return sorted((u, round(d - t, 4)) for u, t, d in zip(ukuran, err_train, err_dev))
            """,
        ),
        E(
            "D11-05-3-ex4",
            "menantang",
            """
            Tulis fungsi `ukuran_model_terbaik(ukuran_list, Xt, yt, Xd, yd)` yang melatih `MLPClassifier(hidden_layer_sizes=(h,), max_iter=2000, random_state=0)` untuk tiap h dan mengembalikan h dengan error dev terendah (jika seri, h terkecil). Hasilnya adalah integer.
            """,
            """
            import numpy as np
            from sklearn.neural_network import MLPClassifier

            def ukuran_model_terbaik(ukuran_list, Xt, yt, Xd, yd):
                # TODO: implementasikan
                pass
            """,
            """
            from sklearn.datasets import make_moons
            X, y = make_moons(n_samples=1000, noise=0.2, random_state=0)
            h = ukuran_model_terbaik([1, 8, 32], X[:300], y[:300], X[300:], y[300:])
            assert h in (8, 32)
            assert isinstance(h, int)
            assert ukuran_model_terbaik([8], X[:300], y[:300], X[300:], y[300:]) == 8
            """,
            "Hitung error dev tiap ukuran lalu pilih minimum atas tuple (error, h).",
            """
            import numpy as np
            from sklearn.neural_network import MLPClassifier

            def ukuran_model_terbaik(ukuran_list, Xt, yt, Xd, yd):
                hasil = []
                for h in ukuran_list:
                    m = MLPClassifier(hidden_layer_sizes=(h,), max_iter=2000, random_state=0).fit(Xt, yt)
                    hasil.append((round(1 - m.score(Xd, yd), 6), int(h)))
                return min(hasil)[1]
            """,
        ),
    ],
    [
        M(
            "Menggunakan early stopping saat bias masih tinggi.",
            "Pakai early stopping setelah bias cukup rendah, karena ia menghentikan pelatihan sebelum training diminimalkan.",
        ),
        M(
            "Mengubah banyak hal sekaligus dalam satu percobaan.",
            "Ubah satu tuas per percobaan lalu ukur ulang tiga angka.",
        ),
        M(
            "Mengurangi ukuran model sebagai pilihan pertama untuk variance.",
            "Prioritaskan data dan regularisasi karena mengurangi kapasitas bisa menaikkan bias.",
        ),
    ],
    [
        Q(
            "Mana yang bukan teknik untuk mengurangi avoidable bias?",
            ["Perbesar model", "Tambah fitur dari error analysis", "Tambah data latih saja pada bias murni", "Kurangi regularisasi"],
            2,
            "Pada bias murni, data tambahan tidak mengubah kemampuan model menyesuaikan diri.",
        ),
        Q(
            "Teknik early stopping bekerja dengan cara?",
            ["Menambah layer", "Menghentikan latihan di epoch dengan error dev terendah", "Mengganti metrik", "Menghapus fitur"],
            1,
            "Epoch ketika error dev minimum dipilih sebelum model menghafal.",
        ),
        Q(
            "Model 1-NN memberi error training 0. Error dev 17 persen. Komponen dominan?",
            ["Bias", "Variance", "Optimal", "Metrik"],
            1,
            "Semua error adalah selisih dev terhadap training, yaitu variance.",
        ),
        Q(
            "Mengapa tidak menggabungkan lima perubahan dalam satu eksperimen?",
            ["Terlalu mahal", "Tidak jelas mana yang bekerja", "Dilarang", "Menaikkan bias"],
            1,
            "Satu perubahan per percobaan membuat sebab akibat terbaca.",
        ),
        Q(
            "Kombinasi tuas yang menurunkan bias dan variance sekaligus?",
            ["Kurangi model dan kurangi data", "Perbesar model dan tambah data", "Hapus regularisasi", "Ganti metrik"],
            1,
            "Model besar menurunkan bias, data tambahan menutup celah variance yang ditimbulkannya.",
        ),
    ],
    [
        "Bias: perbesar model, tambah fitur, kurangi regularisasi, ubah arsitektur.",
        "Variance: tambah data, tambah regularisasi, early stopping, seleksi fitur.",
        "Early stopping memilih epoch dengan error dev terendah dan sebaiknya dipakai saat bias sudah rendah.",
        "Satu perubahan per eksperimen dan ukur ulang tiga angka.",
    ],
    ["Machine Learning Yearning, bab 25 sampai 27 (Andrew Ng): teknik mengurangi bias dan variance"],
)

video = {
    "needed": True,
    "kind": "ai_slides",
    "reason": "Konsep bias dan variance sangat terbantu animasi kurva polinomial dan diagram dekomposisi error.",
    "brief": [
        "Slide 1: bar bertumpuk error dev: optimal, avoidable bias, variance",
        "Slide 2: tiga plot polinomial derajat 1, 3, 12 pada titik data yang sama",
        "Slide 3: grafik error training dan dev terhadap alpha berbentuk U",
        "Slide 4: tabel dua kolom tindakan untuk bias dan untuk variance",
    ],
}

write_module(
    "D11",
    5,
    "Bias dan variance",
    105,
    [
        "Mendiagnosis bias dan variance dari error training, dev, dan optimal",
        "Memilih tindakan yang sesuai dengan komponen error dominan",
        "Menjalankan sapuan regularisasi, ukuran model, dan early stopping secara terkontrol",
    ],
    [l1, l2, l3],
    video,
    REF,
)
