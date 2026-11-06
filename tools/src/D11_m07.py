import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, C, E, Q, M, lesson, write_module

REF = [{"book": "Machine Learning Yearning (Andrew Ng)", "chapters": "bab 36 sampai 43"}]

DOMAIN = """
import numpy as np
from sklearn.linear_model import LogisticRegression

def web(n, seed):
    r = np.random.default_rng(seed)
    X = r.normal(size=(n, 6))
    y = (X[:, 0] + 0.7 * X[:, 1] - 0.4 * X[:, 2] + 0.3 * r.normal(size=n) > 0).astype(int)
    return X, y

def mobile(n, seed):
    r = np.random.default_rng(seed)
    X = r.normal(size=(n, 6)) * 1.5 + np.array([1, 0, 0, 0, 0, 0])
    y = (0.4 * X[:, 0] + 0.9 * X[:, 1] - 0.4 * X[:, 2] - 0.4 + 0.3 * r.normal(size=n) > 0).astype(int)
    return X, y
"""

SINTETIS = """
import numpy as np
from sklearn.ensemble import RandomForestClassifier

T = 64
FREQ = [4, 9, 14]

def bangun(n, pool, seed, segar=False):
    r = np.random.default_rng(seed)
    kolam = r.normal(size=(pool, T)) * 0.5
    X, y = [], []
    for _ in range(n):
        k = r.integers(0, 3)
        t = np.arange(T)
        s = np.sin(2 * np.pi * FREQ[k] * t / T + r.uniform(0, 6.28)) * r.uniform(0.3, 0.6)
        bising = r.normal(size=T) * 0.5 if segar else kolam[r.integers(0, pool)]
        X.append(np.abs(np.fft.rfft(s + bising)))
        y.append(k)
    return np.array(X), np.array(y)
"""

l1 = lesson(
    "D11-07-1",
    "Melatih dan menguji pada distribusi berbeda",
    35,
    [
        "Menyusun pembagian data ketika sumber training berbeda dari sumber target",
        "Memutuskan kapan data dari sumber lain layak ikut dipakai",
        "Mengenali data yang pemetaannya tidak konsisten antar sumber",
        "Memakai bobot contoh untuk menyeimbangkan sumber yang jumlahnya timpang",
    ],
    [
        T("""
        ## Masalah: data banyak, tetapi bukan dari tempat yang kamu tuju

        Aplikasi pengenal kucing akan dipakai pengguna dengan foto dari ponsel. Foto ponsel agak buram, kurang tajam, dan komposisinya khas. Kamu punya 200.000 gambar dari web yang bersih dan terlabel, serta hanya 10.000 foto dari aplikasi. Data web berlimpah, tetapi bukan distribusi yang akan dihadapi sistem.

        Ada godaan besar untuk menggabung semuanya lalu membagi acak menjadi training, dev, dan test. Hasilnya, dev dan test kebanyakan berisi gambar web. Kamu lalu mengoptimalkan sesuatu yang bukan target. Seperti dibahas di modul 1, dev dan test harus mencerminkan data yang ingin kamu tangani di masa depan, bukan data yang kebetulan paling banyak.

        Aturan dasar: dev dan test berasal dari distribusi target (foto ponsel). Training boleh mengandung campuran, dan mungkin sebagian besar berasal dari sumber lain. Dengan begitu, error dev tetap mengukur hal yang penting, dan kamu bebas memanfaatkan data berlimpah untuk melatih.
        """),
        T("""
        ## Contoh pembagian

        Dari 10.000 foto ponsel, sisihkan sebagian untuk dev dan test, misalnya masing-masing 2.500. Sisanya 5.000 foto ponsel dimasukkan ke training bersama 200.000 gambar web. Ukuran: training 205.000, dev 2.500, test 2.500. Dev dan test sama-sama dari ponsel dan berasal dari distribusi yang sama.

        Konsekuensinya, distribusi training dan dev berbeda. Kamu harus siap menafsirkan error dev yang tinggi: bisa karena variance, bisa karena model belum belajar kekhasan ponsel. Lesson berikutnya memperkenalkan satu subset tambahan untuk membedakan keduanya.

        Alternatif yang sering lebih buruk: membagi data acak dari gabungan. Dengan 210.000 contoh, hanya sekitar 5 persen dev berisi foto ponsel. Sebagian besar kapasitas optimisasi tim lalu terbuang untuk gambar yang tidak penting bagi pengguna.
        """),
        T("""
        ## Apakah semua data layak dipakai

        Data dari sumber lain tidak selalu membantu. Pertanyaannya bergantung pada kapasitas model. Jika model cukup besar, ia mampu mempelajari dua sumber sekaligus tanpa saling mengganggu, dan data tambahan umumnya membantu atau minimal tidak merugikan. Jika model kecil, ia harus berkompromi untuk menyesuaikan diri dengan kedua distribusi dan performa pada target bisa turun dibanding hanya memakai data target.

        Data tambahan paling berguna jika ada kemiripan fitur mendasar. Gambar kucing dari web membantu karena bentuk kucing mirip di mana pun. Data yang sangat berbeda mengajari hal tidak relevan dan memakai kapasitas.

        Cara memutuskan paling jujur adalah eksperimen: latih dengan dan tanpa data tambahan, bandingkan error dev pada target. Jika sumber lain tidak menurunkan error dev, jangan paksa. Jika menurunkan, pertahankan dan pertimbangkan bobot.
        """),
        T("""
        ## Data dengan pemetaan tidak konsisten

        Bahaya lain muncul ketika input yang sama punya jawaban benar berbeda di dua sumber. Contoh: harga rumah. Rumah 100 meter persegi di kota A berharga satu kisaran, sedangkan rumah 100 meter persegi di kota B jauh lebih mahal. Jika kamu menggabungkan data kedua kota tanpa memberi tahu model kota mana, model harus menebak harga rata-rata yang salah untuk keduanya.

        Solusinya memberi model informasi yang membedakan sumber, misalnya fitur kota, atau fitur interaksi ukuran dikali kota. Model besar bisa menemukannya sendiri bila sinyalnya ada. Model sederhana perlu dibantu fitur eksplisit.

        Tanda peringatan: error training tinggi pada gabungan data walau model seharusnya cukup kuat. Itu sering berarti sumber saling bertentangan.
        """),
        T("""
        ## Memberi bobot pada data

        Ketika satu sumber jauh lebih banyak, kamu dapat memberi bobot lebih besar pada contoh dari sumber target. Jika ada 200.000 contoh web dan 5.000 contoh ponsel, memberi bobot 20 pada tiap contoh ponsel membuat 5.000 contoh itu setara 100.000 contoh dalam fungsi loss. Pengaruh efektif ponsel naik dari sekitar 2,4 persen menjadi sekitar 33 persen.

        Pembobotan dilakukan lewat parameter `sample_weight` pada banyak model scikit-learn. Bobot adalah hyperparameter: cobalah beberapa nilai, ukur error dev pada target, lalu pilih. Bobot yang terlalu besar membuat model menghafal contoh target yang sedikit.

        Dibanding membuang data web, pembobotan mempertahankan manfaat variasi sambil memusatkan perhatian ke target. Sering ini kompromi yang baik ketika kamu punya sedikit data target tetapi cukup untuk dev dan test.
        """),
        K(
            "warning",
            """
            Jangan pernah memindahkan contoh dev atau test ke training demi menambah data target. Ambil dari cadangan data target yang memang belum dipakai untuk evaluasi.
            """,
        ),
        C(
            """
def bagi_data(n_web, n_mobile, mobile_di_train):
    sisa = n_mobile - mobile_di_train
    dev = sisa // 2
    test = sisa - dev
    return {"train": n_web + mobile_di_train, "dev": dev, "test": test}

print(bagi_data(200000, 10000, 5000))
""",
            """
            {'train': 205000, 'dev': 2500, 'test': 2500}
            """,
            """
            Dev dan test hanya berisi foto ponsel. Training berisi seluruh gambar web ditambah sebagian foto ponsel. Dua himpunan evaluasi berasal dari distribusi target yang sama.
            """,
        ),
        C(
            DOMAIN
            + """
Xw, yw = web(20000, 0)
Xm, ym = mobile(1000, 1)
Xd, yd = mobile(3000, 2)

def err(X, y, sw=None):
    return 1 - LogisticRegression().fit(X, y, sample_weight=sw).score(Xd, yd)

print("hanya web      :", round(err(Xw, yw), 3))
print("hanya ponsel   :", round(err(Xm, ym), 3))
print("gabungan tanpa bobot:", round(err(np.vstack([Xw, Xm]), np.r_[yw, ym]), 3))
""",
            """
            hanya web sekitar 0.24
            hanya ponsel sekitar 0.058
            gabungan tanpa bobot sekitar 0.22
            """,
            """
            Model sederhana yang dilatih pada web gagal di target. Data ponsel kecil tetapi sangat berharga. Menggabung tanpa bobot nyaris tidak membantu karena web mendominasi 20 banding 1.
            """,
        ),
        C(
            DOMAIN
            + """
Xw, yw = web(20000, 0)
Xm, ym = mobile(1000, 1)
Xd, yd = mobile(3000, 2)
X = np.vstack([Xw, Xm])
y = np.r_[yw, ym]
print("bobot  mobile_efektif  err_dev")
for w in [1, 5, 20, 50]:
    sw = np.r_[np.ones(len(yw)), np.full(len(ym), w)]
    e = 1 - LogisticRegression().fit(X, y, sample_weight=sw).score(Xd, yd)
    ef = len(ym) * w / (len(yw) + len(ym) * w)
    print(f"{w:5d}  {ef:14.2f}  {e:7.3f}")
""",
            """
            error dev turun dari sekitar 0.22 pada bobot 1 ke sekitar 0.067 pada bobot 50
            """,
            """
            Bobot lebih besar pada contoh ponsel menurunkan error dev secara tajam. Bobot 50 mendekati hasil model yang hanya memakai data ponsel, tetapi tetap memanfaatkan data web sebagai tambahan.
            """,
        ),
        C(
            """
import numpy as np
from sklearn.linear_model import LinearRegression

def rumah(n, kota, seed):
    r = np.random.default_rng(seed)
    s = r.uniform(30, 150, n)
    p = (10 if kota == 0 else 25) * s + r.normal(0, 30, n)
    return s, p

sa, pa = rumah(500, 0, 1)
sb, pb = rumah(500, 1, 2)
S = np.r_[sa, sb]
P = np.r_[pa, pb]
C = np.r_[np.zeros(500), np.ones(500)]
m1 = LinearRegression().fit(S[:, None], P)
F = np.c_[S, C, S * C]
m2 = LinearRegression().fit(F, P)
print("RMSE tanpa fitur kota:", round(float(np.sqrt(np.mean((m1.predict(S[:, None]) - P) ** 2))), 1))
print("RMSE dengan kota dan interaksi:", round(float(np.sqrt(np.mean((m2.predict(F) - P) ** 2))), 1))
""",
            """
            RMSE tanpa fitur kota sekitar 718
            RMSE dengan kota dan interaksi sekitar 31
            """,
            """
            Dua kota punya harga per meter persegi berbeda. Tanpa fitur kota model tidak bisa membedakan dan galatnya besar. Dengan indikator kota dan interaksi dengan ukuran, galat turun ke tingkat derau.
            """,
        ),
        E(
            "D11-07-1-ex1",
            "mudah",
            """
            Tulis fungsi `bagi_data(n_web, n_mobile, mobile_di_train)` yang mengembalikan dictionary `{"train": ..., "dev": ..., "test": ...}`. `train = n_web + mobile_di_train`. Sisa ponsel `n_mobile - mobile_di_train` dibagi dua: `dev = sisa // 2`, `test = sisa - dev`.
            """,
            """
            def bagi_data(n_web, n_mobile, mobile_di_train):
                # TODO: implementasikan
                pass
            """,
            """
            assert bagi_data(200000, 10000, 5000) == {"train": 205000, "dev": 2500, "test": 2500}
            assert bagi_data(100, 11, 0) == {"train": 100, "dev": 5, "test": 6}
            assert bagi_data(0, 10, 10) == {"train": 10, "dev": 0, "test": 0}
            """,
            "Hitung sisa lebih dulu, lalu gunakan floor division untuk dev.",
            """
            def bagi_data(n_web, n_mobile, mobile_di_train):
                sisa = n_mobile - mobile_di_train
                dev = sisa // 2
                return {"train": n_web + mobile_di_train, "dev": dev, "test": sisa - dev}
            """,
        ),
        E(
            "D11-07-1-ex2",
            "sedang",
            """
            Tulis fungsi `bobot_efektif(n_web, n_mobile, w)` yang mengembalikan bagian bobot total yang berasal dari ponsel: `n_mobile * w / (n_web + n_mobile * w)`, dibulatkan 4 desimal.
            """,
            """
            def bobot_efektif(n_web, n_mobile, w):
                # TODO: implementasikan
                pass
            """,
            """
            assert bobot_efektif(200000, 5000, 1) == 0.0244
            assert bobot_efektif(200000, 5000, 20) == 0.3333
            assert bobot_efektif(100, 100, 1) == 0.5
            assert bobot_efektif(0, 10, 3) == 1.0
            """,
            "Terapkan rumus langsung lalu round(..., 4).",
            """
            def bobot_efektif(n_web, n_mobile, w):
                return round(n_mobile * w / (n_web + n_mobile * w), 4)
            """,
        ),
        E(
            "D11-07-1-ex3",
            "sedang",
            """
            Tulis fungsi `bobot_sampel(sumber, w_mobile)` yang menerima list atau array string `"web"` atau `"mobile"` dan mengembalikan array NumPy float: `w_mobile` untuk `"mobile"` dan `1.0` untuk selainnya.
            """,
            """
            import numpy as np

            def bobot_sampel(sumber, w_mobile):
                # TODO: implementasikan
                pass
            """,
            """
            import numpy as np
            b = bobot_sampel(["web", "mobile", "web", "mobile"], 20)
            assert isinstance(b, np.ndarray)
            assert list(b) == [1.0, 20.0, 1.0, 20.0]
            assert b.dtype == float
            assert len(bobot_sampel([], 5)) == 0
            """,
            "Gunakan np.where pada array sumber.",
            """
            import numpy as np

            def bobot_sampel(sumber, w_mobile):
                s = np.asarray(sumber, dtype=object)
                return np.where(s == "mobile", float(w_mobile), 1.0).astype(float)
            """,
        ),
        E(
            "D11-07-1-ex4",
            "menantang",
            """
            Tulis fungsi `bandingkan_bobot(Xw, yw, Xm, ym, Xd, yd, bobot_list)` yang melatih `LogisticRegression(max_iter=1000)` pada gabungan `vstack([Xw, Xm])` dan `r_[yw, ym]` dengan `sample_weight` bernilai 1 untuk contoh web dan `w` untuk contoh ponsel, untuk tiap `w` dalam `bobot_list`. Kembalikan list error dev (1 dikurangi akurasi) dibulatkan 4 desimal.
            """,
            """
            import numpy as np
            from sklearn.linear_model import LogisticRegression

            def bandingkan_bobot(Xw, yw, Xm, ym, Xd, yd, bobot_list):
                # TODO: implementasikan
                pass
            """,
            """
            import numpy as np
            def web(n, seed):
                r = np.random.default_rng(seed)
                X = r.normal(size=(n, 6))
                y = (X[:, 0] + 0.7 * X[:, 1] - 0.4 * X[:, 2] + 0.3 * r.normal(size=n) > 0).astype(int)
                return X, y
            def mobile(n, seed):
                r = np.random.default_rng(seed)
                X = r.normal(size=(n, 6)) * 1.5 + np.array([1, 0, 0, 0, 0, 0])
                y = (0.4 * X[:, 0] + 0.9 * X[:, 1] - 0.4 * X[:, 2] - 0.4 + 0.3 * r.normal(size=n) > 0).astype(int)
                return X, y
            Xw, yw = web(8000, 0)
            Xm, ym = mobile(400, 1)
            Xd, yd = mobile(2000, 2)
            r = bandingkan_bobot(Xw, yw, Xm, ym, Xd, yd, [1, 50])
            assert len(r) == 2
            assert r[1] < r[0] - 0.05
            assert all(0 <= v <= 1 for v in r)
            """,
            "Bangun vektor bobot dengan np.r_[np.ones(len(yw)), np.full(len(ym), w)] pada tiap putaran.",
            """
            import numpy as np
            from sklearn.linear_model import LogisticRegression

            def bandingkan_bobot(Xw, yw, Xm, ym, Xd, yd, bobot_list):
                X = np.vstack([Xw, Xm])
                y = np.r_[yw, ym]
                hasil = []
                for w in bobot_list:
                    sw = np.r_[np.ones(len(yw)), np.full(len(ym), float(w))]
                    model = LogisticRegression(max_iter=1000).fit(X, y, sample_weight=sw)
                    hasil.append(round(1 - model.score(Xd, yd), 4))
                return hasil
            """,
        ),
    ],
    [
        M(
            "Mengacak gabungan semua sumber lalu membagi menjadi training, dev, dan test.",
            "Dev dan test hanya dari distribusi target. Training boleh campuran.",
        ),
        M(
            "Selalu memakai semua data karena lebih banyak pasti lebih baik.",
            "Uji dengan dan tanpa data tambahan dan lihat error dev pada target.",
        ),
        M(
            "Menggabung dua sumber yang pemetaannya bertentangan tanpa penanda sumber.",
            "Tambahkan fitur sumber atau interaksi, atau pisahkan model.",
        ),
    ],
    [
        Q(
            "Aplikasi untuk foto ponsel, data web 200.000, ponsel 10.000. Dev set sebaiknya?",
            ["Campuran acak web dan ponsel", "Hanya foto ponsel", "Hanya web", "Tidak perlu dev"],
            1,
            "Dev dan test harus mencerminkan data target, yaitu foto ponsel.",
        ),
        Q(
            "Kapan data dari sumber berbeda cenderung tidak merugikan?",
            ["Model sangat kecil", "Model cukup besar dan fitur dasar mirip", "Tanpa dev set", "Data identik"],
            1,
            "Model besar bisa mempelajari dua sumber sekaligus tanpa saling mengganggu.",
        ),
        Q(
            "Rumah 100 meter persegi di dua kota berharga berbeda dan model tidak tahu kota. Masalahnya?",
            ["Variance", "Pemetaan tidak konsisten antar sumber", "Label bocor", "Metrik salah"],
            1,
            "Input sama dengan jawaban benar berbeda membuat model terpaksa merata-ratakan.",
        ),
        Q(
            "200.000 web dan 5.000 ponsel dengan bobot 20 pada ponsel. Bagian bobot efektif ponsel?",
            ["Sekitar 2 persen", "Sekitar 33 persen", "Sekitar 50 persen", "100 persen"],
            1,
            "5.000 kali 20 sama dengan 100.000 dibagi total 300.000, yaitu sekitar 33 persen.",
        ),
        Q(
            "Bobot contoh target dianggap apa?",
            ["Konstanta tetap", "Hyperparameter yang disetel pada dev", "Fitur", "Label"],
            1,
            "Nilai bobot dicoba beberapa kali dan dipilih berdasarkan error dev pada target.",
        ),
    ],
    [
        "Dev dan test harus dari distribusi target sedangkan training boleh campuran.",
        "Data dari sumber lain berguna bila model cukup besar dan fitur dasarnya mirip.",
        "Pemetaan yang bertentangan antar sumber perlu penanda sumber.",
        "Bobot contoh menyeimbangkan sumber dan disetel sebagai hyperparameter.",
    ],
    ["Machine Learning Yearning, bab 36 sampai 39 (Andrew Ng): melatih dan menguji pada distribusi berbeda"],
)

l2 = lesson(
    "D11-07-2",
    "Training-dev set dan data mismatch",
    35,
    [
        "Menjelaskan fungsi training-dev set",
        "Menguraikan error menjadi bias, variance, data mismatch, dan overfitting dev",
        "Mendeteksi mismatch dengan classifier domain",
        "Memilih langkah mengatasi data mismatch",
    ],
    [
        T("""
        ## Dilema membaca error dev

        Dalam konfigurasi dari lesson sebelumnya, training berisi gambar web dan dev berisi foto ponsel. Misalkan error training 1 persen dan error dev 10 persen. Di mana masalahnya? Bisa variance: model menghafal gambar web tanpa menggeneralisasi. Bisa juga karena distribusi dev berbeda sehingga model yang bagus untuk web memang tidak bagus untuk ponsel. Dua penyebab itu butuh tindakan berbeda, tetapi dari dua angka kamu tidak bisa membedakannya.

        Solusinya menambah satu subset: **training-dev set**. Ambil sebagian kecil data training secara acak, jangan dipakai melatih, dan gunakan hanya untuk evaluasi. Training-dev berasal dari distribusi yang sama dengan training, tetapi tidak dilihat model saat belajar. Jadi ia mengukur kemampuan menggeneralisasi dalam distribusi yang sama.

        Sekarang ada tiga angka dari tiga himpunan: training, training-dev, dan dev. Selisih antar-pasangan menjelaskan sumber error.
        """),
        T("""
        ## Lima angka, empat selisih

        Dengan error manusia (acuan optimal), training, training-dev, dev, dan test, kamu mendapat lima angka yang berurutan. Empat selisih di antaranya masing-masing punya nama.

        Training dikurangi manusia: **avoidable bias**. Training-dev dikurangi training: **variance**, karena distribusinya sama tetapi data tidak dilihat. Dev dikurangi training-dev: **data mismatch**, karena inilah efek perbedaan distribusi. Test dikurangi dev: **overfitting ke dev set**, karena keduanya satu distribusi.

        Contoh: manusia 1, training 2, training-dev 2,5, dev 10, test 10,3 (persen). Avoidable bias 1, variance 0,5, data mismatch 7,5, overfitting dev 0,3. Data mismatch jelas dominan sehingga memperbesar model atau menambah data web tidak banyak menolong. Arahnya adalah membuat training lebih mirip target.
        """),
        T("""
        ## Mengatasi data mismatch

        Tidak ada obat tunggal, tetapi ada langkah umum. Pertama, pahami perbedaannya dengan error analysis pada contoh dev yang salah. Bandingkan dengan contoh training yang benar dan cari pola: dev lebih buram, lebih gelap, berisi objek lain di latar? Kedua, jadikan data training lebih mirip dev. Caranya mengumpulkan data target tambahan, menambah bobot, atau mensintesis data yang meniru kekhasan target. Sintesis dibahas di lesson berikutnya dan perlu hati-hati.

        Jika perbedaan sulit dipahami manusia, kamu dapat mengukur kedekatan dua distribusi dengan classifier domain: latih model untuk membedakan contoh training dari contoh dev. Akurasi sekitar 50 persen berarti distribusinya mirip. Akurasi mendekati 100 persen berarti mereka mudah dibedakan, dan fitur mana yang paling membedakan memberi petunjuk tentang perbedaannya.
        """),
        T("""
        ## Tiga catatan praktis

        Pertama, training-dev tidak perlu besar. Cukup agar estimasi error cukup stabil, misalnya sebesar dev. Kedua, jika tidak ada mismatch (dev dan training satu distribusi), training-dev tidak diperlukan karena dev sudah memenuhi fungsinya. Ketiga, jika mismatch besar dan pengumpulan data target tidak mungkin, pertimbangkan apakah target realistis dan perbarui ekspektasi pemangku kepentingan. Tidak semua masalah mismatch bisa diselesaikan oleh teknik; kadang yang diperlukan adalah data nyata.
        """),
        T("""
        ## Contoh alur kerja lengkap

        Misalkan tim membangun pengenal kucing dengan 200.000 gambar web dan 5.000 foto ponsel di training, dev 2.500 foto ponsel, dan training-dev 2.500 gambar web yang disisihkan acak. Hasil: manusia 1 persen, training 2 persen, training-dev 2,5 persen, dev 10 persen. Data mismatch 7,5 poin adalah masalah utama, jadi tim memeriksa 100 foto ponsel yang salah dan menemukan sebagian besar buram dan gelap.

        Tim lalu menambah foto ponsel yang diberi bobot, dan menyintesis versi buram dari gambar web dengan filter kabur yang meniru kamera ponsel. Setelah dua iterasi, dev turun ke 5 persen sementara training-dev tetap 2,5 persen. Mismatch menyusut dari 7,5 ke 2,5 poin tanpa menyentuh arsitektur sama sekali. Contoh ini menunjukkan nilai diagnosis: kamu menghabiskan usaha di tempat error benar-benar berada.
        """),
        K(
            "tip",
            """
            Ambil training-dev dari training sebelum latihan dimulai dan simpan indeksnya. Jika kamu mengambilnya setelah latihan, sebagian contohnya sudah terlihat model.
            """,
        ),
        C(
            """
def uraikan(manusia, train, train_dev, dev, test):
    return {
        "avoidable_bias": round(train - manusia, 4),
        "variance": round(train_dev - train, 4),
        "data_mismatch": round(dev - train_dev, 4),
        "overfit_dev": round(test - dev, 4),
    }

print(uraikan(0.01, 0.02, 0.025, 0.10, 0.103))
""",
            """
            {'avoidable_bias': 0.01, 'variance': 0.005, 'data_mismatch': 0.075, 'overfit_dev': 0.003}
            """,
            """
            Lima angka diuraikan menjadi empat komponen. Di sini data mismatch jauh dominan sehingga prioritas adalah mendekatkan data training ke target.
            """,
        ),
        C(
            DOMAIN
            + """
Xw, yw = web(20000, 0)
Xd, yd = mobile(3000, 2)
Xtr, ytr = Xw[:15000], yw[:15000]
Xtd, ytd = Xw[15000:], yw[15000:]
m = LogisticRegression().fit(Xtr, ytr)
for nama, X, y in [("training", Xtr, ytr), ("training-dev", Xtd, ytd), ("dev (ponsel)", Xd, yd)]:
    print(f"{nama:13s}: {1 - m.score(X, y):.3f}")
""",
            """
            training sekitar 0.070
            training-dev sekitar 0.074
            dev sekitar 0.240
            """,
            """
            Training dan training-dev hampir sama sehingga variance kecil. Lonjakan di dev adalah data mismatch murni sekitar 17 poin. Tanpa training-dev kamu tidak bisa mengatakan ini.
            """,
        ),
        C(
            DOMAIN
            + """
from sklearn.model_selection import train_test_split

def skor_domain(Xa, Xb, seed):
    X = np.vstack([Xa, Xb])
    d = np.r_[np.zeros(len(Xa)), np.ones(len(Xb))]
    Xt, Xv, dt, dv = train_test_split(X, d, test_size=0.3, random_state=seed, stratify=d)
    return LogisticRegression(max_iter=1000).fit(Xt, dt).score(Xv, dv)

Xw1, _ = web(2000, 0)
Xw2, _ = web(2000, 1)
Xm, _ = mobile(2000, 2)
print("web vs web      :", round(skor_domain(Xw1, Xw2, 0), 3))
print("web vs ponsel   :", round(skor_domain(Xw1, Xm, 0), 3))
""",
            """
            web vs web sekitar 0.5
            web vs ponsel sekitar 0.65
            """,
            """
            Classifier domain pada dua sampel dari distribusi yang sama hanya menebak, jadi akurasi sekitar 50 persen. Pada web melawan ponsel akurasinya naik jelas di atas tebakan, sekitar 65 persen, tanda mismatch nyata walau fiturnya mirip.
            """,
        ),
        E(
            "D11-07-2-ex1",
            "mudah",
            """
            Tulis fungsi `uraikan(manusia, train, train_dev, dev, test)` yang mengembalikan dictionary dengan kunci `avoidable_bias` (`train - manusia`), `variance` (`train_dev - train`), `data_mismatch` (`dev - train_dev`), dan `overfit_dev` (`test - dev`). Semua dibulatkan 4 desimal.
            """,
            """
            def uraikan(manusia, train, train_dev, dev, test):
                # TODO: implementasikan
                pass
            """,
            """
            r = uraikan(0.01, 0.02, 0.025, 0.10, 0.103)
            assert r == {"avoidable_bias": 0.01, "variance": 0.005, "data_mismatch": 0.075, "overfit_dev": 0.003}
            r2 = uraikan(0.0, 0.0, 0.0, 0.0, 0.0)
            assert all(v == 0.0 for v in r2.values())
            assert set(r) == {"avoidable_bias", "variance", "data_mismatch", "overfit_dev"}
            """,
            "Empat pengurangan antar angka berurutan lalu round(..., 4).",
            """
            def uraikan(manusia, train, train_dev, dev, test):
                return {
                    "avoidable_bias": round(train - manusia, 4),
                    "variance": round(train_dev - train, 4),
                    "data_mismatch": round(dev - train_dev, 4),
                    "overfit_dev": round(test - dev, 4),
                }
            """,
        ),
        E(
            "D11-07-2-ex2",
            "sedang",
            """
            Tulis fungsi `komponen_dominan(manusia, train, train_dev, dev, test)` yang menguraikan error seperti latihan sebelumnya (dibulatkan 4 desimal) dan mengembalikan nama komponen dengan nilai terbesar. Jika seri pilih yang lebih awal menurut urutan `avoidable_bias`, `variance`, `data_mismatch`, `overfit_dev`.
            """,
            """
            def komponen_dominan(manusia, train, train_dev, dev, test):
                # TODO: implementasikan
                pass
            """,
            """
            assert komponen_dominan(0.01, 0.02, 0.025, 0.10, 0.103) == "data_mismatch"
            assert komponen_dominan(0.0, 0.1, 0.12, 0.13, 0.13) == "avoidable_bias"
            assert komponen_dominan(0.0, 0.01, 0.1, 0.11, 0.11) == "variance"
            assert komponen_dominan(0.0, 0.05, 0.05, 0.05, 0.05) == "avoidable_bias"
            assert komponen_dominan(0.0, 0.0, 0.0, 0.0, 0.05) == "overfit_dev"
            """,
            "Simpan nilai dalam list berurutan lalu pilih indeks maksimum pertama.",
            """
            def komponen_dominan(manusia, train, train_dev, dev, test):
                nama = ["avoidable_bias", "variance", "data_mismatch", "overfit_dev"]
                nilai = [
                    round(train - manusia, 4),
                    round(train_dev - train, 4),
                    round(dev - train_dev, 4),
                    round(test - dev, 4),
                ]
                return nama[nilai.index(max(nilai))]
            """,
        ),
        E(
            "D11-07-2-ex3",
            "sedang",
            """
            Tulis fungsi `bagi_train_dev(n, n_td, seed)` yang mengembalikan tuple `(train_idx, td_idx)`. Buat `rng = np.random.default_rng(seed)`, `perm = rng.permutation(n)`, `td_idx = np.sort(perm[:n_td])`, `train_idx = np.sort(perm[n_td:])`.
            """,
            """
            import numpy as np

            def bagi_train_dev(n, n_td, seed):
                # TODO: implementasikan
                pass
            """,
            """
            a, b = bagi_train_dev(100, 20, 0)
            assert len(a) == 80 and len(b) == 20
            assert set(a).isdisjoint(set(b))
            assert sorted(set(a) | set(b)) == list(range(100))
            a2, b2 = bagi_train_dev(100, 20, 0)
            assert list(b) == list(b2)
            """,
            "Permutasi lalu potong. Training-dev diambil dari awal permutasi.",
            """
            import numpy as np

            def bagi_train_dev(n, n_td, seed):
                rng = np.random.default_rng(seed)
                perm = rng.permutation(n)
                return np.sort(perm[n_td:]), np.sort(perm[:n_td])
            """,
        ),
        E(
            "D11-07-2-ex4",
            "menantang",
            """
            Tulis fungsi `skor_domain(Xa, Xb, seed)`. Gabungkan `X = vstack([Xa, Xb])` dan label domain `d = r_[zeros(len(Xa)), ones(len(Xb))]`. Pisahkan dengan `train_test_split(X, d, test_size=0.3, random_state=seed, stratify=d)`. Latih `LogisticRegression(max_iter=1000)` pada bagian training dan kembalikan akurasi pada bagian validasi sebagai float dibulatkan 4 desimal.
            """,
            """
            import numpy as np
            from sklearn.linear_model import LogisticRegression
            from sklearn.model_selection import train_test_split

            def skor_domain(Xa, Xb, seed):
                # TODO: implementasikan
                pass
            """,
            """
            import numpy as np
            rng = np.random.default_rng(0)
            A = rng.normal(size=(600, 4))
            B = rng.normal(size=(600, 4))
            C = rng.normal(size=(600, 4)) + np.array([2, 0, 0, 0])
            s_sama = skor_domain(A, B, 0)
            s_beda = skor_domain(A, C, 0)
            assert 0.4 < s_sama < 0.62
            assert s_beda > 0.8
            assert skor_domain(A, C, 0) == s_beda
            """,
            "Gunakan stratify=d agar proporsi domain seimbang di kedua bagian.",
            """
            import numpy as np
            from sklearn.linear_model import LogisticRegression
            from sklearn.model_selection import train_test_split

            def skor_domain(Xa, Xb, seed):
                X = np.vstack([Xa, Xb])
                d = np.r_[np.zeros(len(Xa)), np.ones(len(Xb))]
                Xt, Xv, dt, dv = train_test_split(X, d, test_size=0.3, random_state=seed, stratify=d)
                model = LogisticRegression(max_iter=1000).fit(Xt, dt)
                return round(float(model.score(Xv, dv)), 4)
            """,
        ),
    ],
    [
        M(
            "Membaca selisih training ke dev sebagai variance padahal distribusinya berbeda.",
            "Tambah training-dev set untuk memisahkan variance dari data mismatch.",
        ),
        M(
            "Mengambil training-dev setelah training sehingga sebagian sudah dilihat model.",
            "Sisihkan training-dev sebelum pelatihan dimulai.",
        ),
        M(
            "Menambah data web untuk mengatasi data mismatch.",
            "Mismatch dibantu dengan data yang lebih mirip target atau sintesis yang realistis.",
        ),
    ],
    [
        Q(
            "Apa fungsi training-dev set?",
            ["Menggantikan test set", "Mengukur generalisasi dalam distribusi training yang sama", "Mengukur distribusi dev", "Memberi label"],
            1,
            "Berasal dari distribusi training tetapi tidak dipakai melatih.",
        ),
        Q(
            "Training 2, training-dev 2,5, dev 10 (persen). Data mismatch?",
            ["0,5", "7,5", "8", "12,5"],
            1,
            "Dev dikurangi training-dev sama dengan 7,5.",
        ),
        Q(
            "Test dikurangi dev mengukur?",
            ["Bias", "Variance", "Overfitting ke dev set", "Mismatch"],
            2,
            "Keduanya satu distribusi sehingga selisihnya menunjukkan penyetelan berlebih pada dev.",
        ),
        Q(
            "Classifier domain memberi akurasi 50 persen. Artinya?",
            ["Distribusi sangat berbeda", "Distribusi sulit dibedakan, mirip", "Model rusak", "Label salah"],
            1,
            "Akurasi sekitar tebakan menunjukkan dua himpunan mirip.",
        ),
        Q(
            "Tindakan awal terhadap data mismatch?",
            ["Menambah layer", "Error analysis untuk memahami perbedaan lalu mendekatkan training ke target", "Ganti metrik", "Hapus dev"],
            1,
            "Pahami dulu perbedaan, lalu buat training lebih mirip target.",
        ),
    ],
    [
        "Training-dev set memisahkan variance dari data mismatch.",
        "Uraikan error menjadi avoidable bias, variance, data mismatch, dan overfitting dev.",
        "Classifier domain mengukur kedekatan dua distribusi.",
        "Atasi mismatch dengan memahami perbedaan lalu mendekatkan data training ke target.",
    ],
    ["Machine Learning Yearning, bab 40 sampai 42 (Andrew Ng): generalisasi, training-dev, dan data mismatch"],
)

l3 = lesson(
    "D11-07-3",
    "Sintesis data buatan",
    35,
    [
        "Menjelaskan manfaat dan risiko data sintesis",
        "Membuat sinyal bising sintetis dengan rasio sinyal terhadap derau tertentu",
        "Menunjukkan efek memakai kumpulan derau yang terlalu kecil",
        "Memutuskan seberapa banyak sumber derau dan variasi yang dibutuhkan",
    ],
    [
        T("""
        ## Membuat data yang tidak kamu punya

        Misalkan kamu membangun sistem pengenalan suara untuk di dalam mobil. Kamu punya banyak rekaman bersih yang diucapkan di ruang tenang, tetapi sangat sedikit rekaman di mobil yang melaju. Salah satu jalan adalah sintesis data: ambil rekaman bersih dan tambahkan rekaman derau mobil. Hasilnya terdengar seperti ucapan di mobil dan bisa dibuat dalam jumlah besar dengan biaya sangat rendah.

        Ide ini ampuh bila berhasil. Ia mengubah data bersih yang melimpah menjadi data yang menyerupai target. Banyak sistem produksi memakai sintesis, dari suara hingga teks dan citra.

        Namun sintesis membawa jebakan yang perlu dikenali. Data sintetis hanyalah perkiraan dari data nyata. Jika perkiraannya mengabaikan sesuatu, model belajar dari dunia yang sedikit berbeda dari dunia sebenarnya.
        """),
        T("""
        ## Jebakan kumpulan derau kecil

        Perhatikan skenario ini. Kamu punya 10.000 jam ucapan bersih tetapi hanya satu jam derau mobil. Kamu menempelkan satu jam derau itu berulang-ulang pada 10.000 jam ucapan. Manusia yang mendengar hasilnya merasa realistis, karena semua derau mobil terdengar mirip bagi telinga.

        Tetapi model bisa menghafal potongan derau yang sama itu yang berulang ribuan kali. Ia belajar bahwa pola khusus derau tersebut tidak relevan dan, lebih buruk lagi, bisa menyesuaikan diri terhadap pola itu. Pada data nyata yang berderau dengan variasi lain, performanya turun. Ini overfitting terhadap sumber derau.

        Perbaikannya mudah diucapkan: butuh lebih banyak variasi derau. Jika kamu punya 1.000 jam derau berbeda, masalah ini jauh mereda. Ukuran yang penting bukan jumlah data sintetis total, melainkan keberagaman sumber komponen yang disintesis.
        """),
        T("""
        ## Contoh lain dan aturan praktis

        Contoh lain: deteksi mobil pada citra dengan mensintesis mobil dari gim video. Kalau gim hanya memiliki dua puluh model mobil, sistem akan belajar mengenali dua puluh model itu. Manusia melihat gambar sintetis dan menganggap beragam, padahal dari sudut pandang model hanya ada dua puluh pola.

        Beberapa aturan praktis. Pertama, pastikan sumber yang kamu campurkan (derau, latar, objek) memiliki keragaman sebanding dengan dunia nyata. Kedua, jangan percaya telinga atau mata sebagai bukti kualitas sintesis; ukur lewat error dev pada data nyata. Ketiga, bandingkan beberapa komposisi: data sintetis penuh, campuran, dan tanpa sintetis. Keempat, jika akhirnya kamu bisa mengumpulkan data nyata, pakai sebagai dev dan test, sebab sintesis tidak boleh menjadi alat ukur.

        Satu hal terakhir: tentukan rasio sinyal terhadap derau yang realistis. Derau terlalu keras atau terlalu pelan menghasilkan distribusi yang tidak sesuai target.
        """),
        T("""
        ## Mengukur dan mengontrol SNR

        Rasio sinyal terhadap derau (SNR) dalam desibel dihitung `10 * log10(daya_sinyal / daya_derau)`. Daya adalah rata-rata kuadrat. Untuk menyintesis dengan SNR tertentu, skalakan derau agar dayanya sama dengan daya sinyal dibagi `10 ** (snr / 10)`. Dengan begitu kamu bisa menghasilkan contoh pada berbagai tingkat kesulitan, dari SNR tinggi (mudah) sampai SNR rendah (sulit), sesuai kondisi sebenarnya.

        Strategi yang efektif adalah memvariasikan SNR dalam rentang realistis agar model tidak hanya melihat satu tingkat kesulitan. Perlakukan SNR seperti hyperparameter data: cobalah beberapa rentang, lalu ukur pada dev set nyata.
        """),
        T("""
        ## Daftar periksa sebelum memakai data sintetis

        Sebelum mengandalkan sintesis, jawab empat pertanyaan. Apakah ada bukti dari dev nyata bahwa target punya kekhasan yang ingin ditiru, misalnya derau atau keburaman? Berapa sumber komponen berbeda yang tersedia, dan apakah jumlahnya sebanding dengan variasi dunia nyata? Apakah rentang parameter sintesis, seperti SNR atau tingkat kabur, mencakup kondisi nyata? Dan apakah kamu punya dev nyata untuk memastikan perbaikannya terukur?

        Jika jawaban salah satunya tidak, tunda sintesis dan kumpulkan dulu sedikit data nyata dari target. Sepuluh contoh nyata yang dianalisis sering lebih informatif daripada sejuta contoh sintetis yang dibuat dengan asumsi keliru.
        """),
        K(
            "warning",
            """
            Data sintetis boleh dipakai untuk training, tetapi jangan pernah untuk dev atau test. Jika dev ikut sintetis, kamu mengukur seberapa baik model menirukan generatormu, bukan dunia nyata.
            """,
        ),
        C(
            SINTETIS
            + """
Xd, yd = bangun(1000, 1, 99, segar=True)
print("pool derau  err_dev (derau segar)")
for pool in [1, 5, 500]:
    X, y = bangun(800, pool, 0)
    m = RandomForestClassifier(60, random_state=0).fit(X, y)
    print(f"{pool:10d}  {1 - m.score(Xd, yd):.3f}")
""",
            """
            pool 1: sekitar 0.13
            pool 5: sekitar 0.04
            pool 500: sekitar 0.02
            """,
            """
            Jumlah contoh sintetis tetap 800, hanya keberagaman derau yang berubah. Dengan satu potongan derau, model gagal pada derau baru. Dengan beberapa ratus potongan, galat turun besar.
            """,
        ),
        C(
            """
import numpy as np

def tambah_derau(sinyal, derau, snr_db):
    p_s = np.mean(sinyal ** 2)
    p_n = np.mean(derau ** 2)
    skala = np.sqrt(p_s / (p_n * 10 ** (snr_db / 10)))
    return sinyal + derau * skala

rng = np.random.default_rng(0)
s = np.sin(np.linspace(0, 20, 1000))
n = rng.normal(size=1000)
for snr in [20, 10, 0]:
    campur = tambah_derau(s, n, snr)
    derau_nyata = campur - s
    ukur = 10 * np.log10(np.mean(s ** 2) / np.mean(derau_nyata ** 2))
    print(f"target {snr:3d} dB, terukur {ukur:5.2f} dB")
""",
            """
            target 20 dB, terukur 20.00 dB
            target 10 dB, terukur 10.00 dB
            target 0 dB, terukur 0.00 dB
            """,
            """
            Penskalaan derau mengatur SNR dengan tepat. Dengan memvariasikan SNR kamu mensimulasikan berbagai kondisi dari mudah ke sulit.
            """,
        ),
        C(
            """
def rasio_pakai_ulang(n_sampel, n_potongan_derau):
    return round(n_sampel / n_potongan_derau, 2)

print(rasio_pakai_ulang(10000, 1))
print(rasio_pakai_ulang(10000, 1000))
""",
            """
            10000.0
            10.0
            """,
            """
            Rasio pemakaian ulang menunjukkan berapa kali rata-rata satu potongan derau muncul. Satu potongan dipakai 10.000 kali berisiko dihafal. Rasio 10 jauh lebih aman.
            """,
        ),
        E(
            "D11-07-3-ex1",
            "mudah",
            """
            Tulis fungsi `rasio_pakai_ulang(n_sampel, n_potongan)` yang mengembalikan `n_sampel / n_potongan` dibulatkan 2 desimal.
            """,
            """
            def rasio_pakai_ulang(n_sampel, n_potongan):
                # TODO: implementasikan
                pass
            """,
            """
            assert rasio_pakai_ulang(10000, 1) == 10000.0
            assert rasio_pakai_ulang(10000, 1000) == 10.0
            assert rasio_pakai_ulang(7, 3) == 2.33
            """,
            "Bagi lalu round(..., 2).",
            """
            def rasio_pakai_ulang(n_sampel, n_potongan):
                return round(n_sampel / n_potongan, 2)
            """,
        ),
        E(
            "D11-07-3-ex2",
            "sedang",
            """
            Tulis fungsi `tambah_derau(sinyal, derau, snr_db)` yang mengembalikan `sinyal + derau * skala` dengan `skala = sqrt(p_s / (p_n * 10 ** (snr_db / 10)))`, `p_s = mean(sinyal ** 2)`, `p_n = mean(derau ** 2)`.
            """,
            """
            import numpy as np

            def tambah_derau(sinyal, derau, snr_db):
                # TODO: implementasikan
                pass
            """,
            """
            import numpy as np
            rng = np.random.default_rng(0)
            s = np.sin(np.linspace(0, 20, 1000))
            n = rng.normal(size=1000)
            for snr in [20, 10, 0, -5]:
                hasil = tambah_derau(s, n, snr)
                d = hasil - s
                ukur = 10 * np.log10(np.mean(s ** 2) / np.mean(d ** 2))
                assert abs(ukur - snr) < 0.01
            assert tambah_derau(s, n, 10).shape == s.shape
            assert np.allclose(tambah_derau(s, n, 0) - s, n * np.sqrt(np.mean(s ** 2) / np.mean(n ** 2)))
            """,
            "Hitung daya sinyal dan derau lebih dulu, lalu skalakan derau.",
            """
            import numpy as np

            def tambah_derau(sinyal, derau, snr_db):
                p_s = np.mean(sinyal ** 2)
                p_n = np.mean(derau ** 2)
                skala = np.sqrt(p_s / (p_n * 10 ** (snr_db / 10)))
                return sinyal + derau * skala
            """,
        ),
        E(
            "D11-07-3-ex3",
            "sedang",
            """
            Tulis fungsi `buat_sintetis(n, pool, seed)` yang mengembalikan `(X, y)`. Pakai `r = np.random.default_rng(seed)`. Bangun `kolam = r.normal(size=(pool, 64)) * 0.5`. Untuk tiap contoh: `k = r.integers(0, 3)`, `s = np.sin(2*np.pi*FREQ[k]*t/64 + r.uniform(0, 6.28)) * r.uniform(0.3, 0.6)` dengan `t = np.arange(64)` dan `FREQ = [4, 9, 14]`, lalu `bising = kolam[r.integers(0, pool)]`, fitur `np.abs(np.fft.rfft(s + bising))`. `X` array bentuk (n, 33) dan `y` array label.
            """,
            """
            import numpy as np

            FREQ = [4, 9, 14]

            def buat_sintetis(n, pool, seed):
                # TODO: implementasikan
                pass
            """,
            """
            import numpy as np
            X, y = buat_sintetis(50, 3, 0)
            assert X.shape == (50, 33) and y.shape == (50,)
            assert set(y) <= {0, 1, 2}
            assert (X >= 0).all()
            X2, y2 = buat_sintetis(50, 3, 0)
            assert np.allclose(X, X2) and list(y) == list(y2)
            """,
            "Urutan tarikan acak dalam loop: k, fase, amplitudo, lalu indeks derau.",
            """
            import numpy as np

            FREQ = [4, 9, 14]

            def buat_sintetis(n, pool, seed):
                r = np.random.default_rng(seed)
                kolam = r.normal(size=(pool, 64)) * 0.5
                t = np.arange(64)
                X, y = [], []
                for _ in range(n):
                    k = r.integers(0, 3)
                    s = np.sin(2 * np.pi * FREQ[k] * t / 64 + r.uniform(0, 6.28)) * r.uniform(0.3, 0.6)
                    bising = kolam[r.integers(0, pool)]
                    X.append(np.abs(np.fft.rfft(s + bising)))
                    y.append(k)
                return np.array(X), np.array(y)
            """,
        ),
        E(
            "D11-07-3-ex4",
            "menantang",
            """
            Tulis fungsi `error_vs_pool(pools, n, seed)` yang untuk tiap `pool` membuat data latih lewat `buat_sintetis(n, pool, seed)` (sudah disediakan), melatih `RandomForestClassifier(60, random_state=0)`, dan mengukur error pada dev segar `dev` yang juga disediakan. Kembalikan list error dibulatkan 3 desimal.
            """,
            """
            import numpy as np
            from sklearn.ensemble import RandomForestClassifier

            FREQ = [4, 9, 14]

            def _bangun(n, pool, seed, segar=False):
                r = np.random.default_rng(seed)
                kolam = r.normal(size=(pool, 64)) * 0.5
                t = np.arange(64)
                X, y = [], []
                for _ in range(n):
                    k = r.integers(0, 3)
                    s = np.sin(2 * np.pi * FREQ[k] * t / 64 + r.uniform(0, 6.28)) * r.uniform(0.3, 0.6)
                    bising = r.normal(size=64) * 0.5 if segar else kolam[r.integers(0, pool)]
                    X.append(np.abs(np.fft.rfft(s + bising)))
                    y.append(k)
                return np.array(X), np.array(y)

            def buat_sintetis(n, pool, seed):
                return _bangun(n, pool, seed)

            def dev():
                return _bangun(1000, 1, 99, segar=True)

            def error_vs_pool(pools, n, seed):
                # TODO: implementasikan
                pass
            """,
            """
            r = error_vs_pool([1, 500], 800, 0)
            assert len(r) == 2
            assert r[0] > r[1] + 0.04
            assert all(0 <= v < 1 for v in r)
            """,
            "Panggil dev() sekali di awal. Latih satu forest per pool.",
            """
            import numpy as np
            from sklearn.ensemble import RandomForestClassifier

            FREQ = [4, 9, 14]

            def _bangun(n, pool, seed, segar=False):
                r = np.random.default_rng(seed)
                kolam = r.normal(size=(pool, 64)) * 0.5
                t = np.arange(64)
                X, y = [], []
                for _ in range(n):
                    k = r.integers(0, 3)
                    s = np.sin(2 * np.pi * FREQ[k] * t / 64 + r.uniform(0, 6.28)) * r.uniform(0.3, 0.6)
                    bising = r.normal(size=64) * 0.5 if segar else kolam[r.integers(0, pool)]
                    X.append(np.abs(np.fft.rfft(s + bising)))
                    y.append(k)
                return np.array(X), np.array(y)

            def buat_sintetis(n, pool, seed):
                return _bangun(n, pool, seed)

            def dev():
                return _bangun(1000, 1, 99, segar=True)

            def error_vs_pool(pools, n, seed):
                Xd, yd = dev()
                hasil = []
                for pool in pools:
                    X, y = buat_sintetis(n, pool, seed)
                    m = RandomForestClassifier(60, random_state=0).fit(X, y)
                    hasil.append(round(1 - m.score(Xd, yd), 3))
                return hasil
            """,
        ),
    ],
    [
        M(
            "Menganggap data sintetis berkualitas karena terdengar atau terlihat realistis.",
            "Ukur kualitas lewat error dev pada data nyata.",
        ),
        M(
            "Memakai satu sumber derau atau objek berulang untuk seluruh data sintetis.",
            "Perbanyak keberagaman sumber agar model tidak menghafal.",
        ),
        M(
            "Memakai data sintetis sebagai dev atau test.",
            "Dev dan test harus dari data nyata target.",
        ),
    ],
    [
        Q(
            "Mengapa satu jam derau yang diulang pada 10.000 jam ucapan berisiko?",
            ["Karena terlalu sedikit ucapan", "Karena model bisa menghafal pola derau itu", "Karena SNR berubah", "Karena dev bocor"],
            1,
            "Pola derau yang sama berulang ribuan kali bisa dihafal sehingga gagal pada derau baru.",
        ),
        Q(
            "Yang paling menentukan kualitas sintesis menurut pembahasan?",
            ["Jumlah total contoh", "Keberagaman sumber komponen yang disintesis", "Panjang rekaman", "Ukuran model"],
            1,
            "Variasi derau atau objek lebih penting daripada jumlah contoh total.",
        ),
        Q(
            "SNR 10 dB berarti rasio daya sinyal dan derau?",
            ["1", "10", "100", "0,1"],
            1,
            "10 dB sama dengan rasio daya 10 kali.",
        ),
        Q(
            "Mengapa tidak boleh memakai data sintetis untuk dev?",
            ["Terlalu mahal", "Kamu akan mengukur kemampuan menirukan generator, bukan dunia nyata", "Menaikkan bias", "Tidak ada alasan"],
            1,
            "Evaluasi harus mencerminkan target nyata.",
        ),
        Q(
            "Cara menilai apakah sintesis membantu?",
            ["Mendengarkan hasilnya", "Membandingkan error dev nyata dengan dan tanpa sintesis", "Melihat jumlah data", "Bertanya ke rekan"],
            1,
            "Eksperimen terkontrol pada dev nyata adalah ukuran yang sah.",
        ),
    ],
    [
        "Sintesis membuat data target dari data yang melimpah, dengan risiko menghafal sumber yang terbatas.",
        "Keberagaman sumber komponen lebih penting daripada jumlah total.",
        "SNR dikontrol dengan menskalakan derau dan sebaiknya divariasikan.",
        "Dev dan test tetap data nyata, dan efek sintesis diukur pada keduanya.",
    ],
    ["Machine Learning Yearning, bab 43 (Andrew Ng): sintesis data buatan"],
)

video = {
    "needed": True,
    "kind": "ai_slides",
    "reason": "Lima angka error dan alur training-dev set lebih mudah dipahami lewat diagram bertahap.",
    "brief": [
        "Slide 1: tiga himpunan training, training-dev, dev dengan panah sumber distribusi",
        "Slide 2: tangga lima angka error dan label empat selisih",
        "Slide 3: grafik error terhadap ukuran kolam derau sintetis",
        "Slide 4: diagram alur memilih langkah mengatasi data mismatch",
    ],
}

write_module(
    "D11",
    7,
    "Distribusi data yang berbeda",
    105,
    [
        "Menyusun pembagian data ketika training berbeda dari target",
        "Mendiagnosis data mismatch dengan training-dev set",
        "Menyintesis data dengan keberagaman cukup dan mengukurnya pada data nyata",
    ],
    [l1, l2, l3],
    video,
    REF,
)
