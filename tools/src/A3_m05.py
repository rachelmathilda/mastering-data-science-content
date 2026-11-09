import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

l1 = lesson(
    "A3-05-1",
    "Algoritma gradient descent dan learning rate",
    35,
    [
        "Menjelaskan gradient descent sebagai pembaruan berulang melawan gradien",
        "Mensimulasikan gradient descent satu dimensi",
        "Membedakan konvergen, osilasi, dan divergen akibat learning rate",
        "Menentukan kriteria berhenti yang masuk akal",
    ],
    [
        T("""
        ## Menuruni lembah dalam kabut

        Bayangkan berdiri di lereng gunung berkabut dan ingin turun ke lembah. Kamu tidak melihat lembah, tetapi merasakan kemiringan tanah di bawah kaki. Strategi sederhana: selangkah demi selangkah, bergeraklah ke arah yang paling menurun. Itulah **gradient descent**. Algoritma ini tidak perlu melihat bentuk seluruh fungsi, hanya kemiringan lokal di posisinya sekarang.

        Secara formal, mulai dari titik `x0`. Pada tiap iterasi hitung gradien `g = f'(x)` lalu perbarui `x = x - lr * g`. Bilangan `lr` adalah **learning rate**, ukuran langkah. Karena gradien menunjuk kenaikan tercuram, mengurangkannya menggerakkan titik ke arah penurunan. Ulangi sampai berhenti. Hanya itu algoritmanya, dan ia melatih hampir semua model ML modern.
        """),
        C(
            """
            def grad(x):
                return 2 * (x - 3)

            x = 0.0
            jalur = []
            for _ in range(5):
                x -= 0.1 * grad(x)
                jalur.append(round(x, 4))
            print(jalur)

            x = 0.0
            for _ in range(50):
                x -= 0.1 * grad(x)
            print(round(x, 4), round((x - 3) ** 2 + 1, 4))
            """,
            """
            [0.6, 1.08, 1.464, 1.7712, 2.017]
            3.0 1.0
            """,
            """
            Fungsi `(x - 3)^2 + 1` berminimum di `x = 3` dengan nilai satu. Titik mulai dari nol bergerak mendekati tiga dengan langkah yang makin kecil karena gradiennya mengecil.
            """,
            filename="gd_1d.py",
        ),
        T("""
        ## Mengapa langkah makin kecil

        Perhatikan bahwa langkah makin pendek saat mendekati minimum, padahal learning rate tetap. Alasannya, ukuran langkah adalah `lr * gradien`, dan gradien mengecil menuju nol di dekat minimum. Perilaku ini otomatis dan sangat berguna: algoritma melambat sendiri saat mendekati tujuan sehingga tidak melompat melewatinya, asalkan `lr` tidak terlalu besar.

        Untuk fungsi kuadrat `f = a/2 (x - m)^2`, galat `x - m` dikalikan faktor `(1 - lr a)` pada tiap langkah. Bila faktor itu bernilai mutlak kurang dari satu, galat menyusut secara geometris dan algoritma konvergen. Rumus kecil ini menjelaskan hampir seluruh perilaku learning rate, jadi layak diingat.
        """),
        T("""
        ## Learning rate: terlalu kecil, pas, terlalu besar

        Learning rate terlalu kecil membuat konvergensi sangat lambat: faktor `(1 - lr a)` dekat satu sehingga galat berkurang tipis tiap langkah. Learning rate yang pas, pada kuadrat sederhana `lr = 1 / a`, jatuh tepat ke minimum dalam satu langkah. Bila `lr a` antara satu dan dua, titik melompati minimum tetapi tetap konvergen dengan berosilasi. Tepat pada `lr a = 2` titik memantul bolak-balik tanpa pernah mendekat. Di atas itu galat justru membesar: **divergen**.

        Pada model nyata batas `2 / a` ditentukan oleh kelengkungan terbesar fungsi loss, jadi tidak diketahui di muka. Itulah sebabnya learning rate adalah hiperparameter paling penting dan sering paling merepotkan untuk disetel.
        """),
        C(
            """
            def jalankan(lr, langkah=10, x0=0.0):
                x = x0
                for _ in range(langkah):
                    x -= lr * 2 * (x - 3)
                return round(x, 4)

            for lr in (0.01, 0.1, 0.9, 1.0, 1.1):
                print(lr, jalankan(lr))
            """,
            """
            0.01 0.5488
            0.1 2.6779
            0.9 2.6779
            1.0 0.0
            1.1 -15.5752
            """,
            """
            Learning rate kecil baru separuh jalan setelah sepuluh langkah. Nilai 0,9 berosilasi namun mengecil, 1,0 memantul tanpa kemajuan, dan 1,1 menjauh dari tiga.
            """,
            filename="learning_rate.py",
        ),
        K(
            "tip",
            """
            Saat loss mendadak naik atau menjadi `nan` pada pelatihan, penyebab pertama yang perlu dicurigai adalah learning rate terlalu besar. Coba turunkan sepuluh kali lipat dan lihat apakah kurva loss menurun mulus.
            """,
            title="Tanda learning rate besar",
        ),
        T("""
        ## Kriteria berhenti

        Kapan iterasi dihentikan? Ada beberapa kriteria umum. Pertama, **norma gradien** lebih kecil dari ambang: gradien hampir nol berarti kita dekat titik datar. Kedua, **perubahan loss** antar iterasi lebih kecil dari ambang: tidak ada kemajuan berarti. Ketiga, **batas iterasi** maksimum, jaring pengaman agar program tidak berjalan selamanya bila algoritma tidak konvergen.

        Praktisi biasanya menggabungkan ketiganya. Dalam deep learning, kriteria yang paling umum adalah berhenti dini berdasarkan loss pada data validasi: bila loss validasi tidak membaik beberapa epoch berturut-turut, pelatihan dihentikan walau loss latih masih turun, untuk mencegah overfitting.
        """),
        C(
            """
            x = 0.0
            n = 0
            while abs(2 * (x - 3)) >= 1e-6 and n < 10000:
                x -= 0.1 * 2 * (x - 3)
                n += 1
            print(n, round(x, 4))

            x = 0.0
            n = 0
            while abs(2 * (x - 3)) >= 1e-6 and n < 100:
                x -= 1.0 * 2 * (x - 3)
                n += 1
            print(n, x)
            """,
            """
            70 3.0
            100 0.0
            """,
            """
            Dengan learning rate 0,1 gradien turun di bawah ambang setelah 70 langkah. Dengan learning rate 1,0 titik memantul sehingga hanya batas iterasi yang menghentikan perulangan.
            """,
            filename="berhenti.py",
        ),
        T("""
        ## Kondisi buruk dan ngarai

        Pada fungsi satu variabel, satu learning rate cukup. Pada banyak variabel kelengkungan berbeda antar arah. Bayangkan lembah panjang dan sempit: sangat curam ke kiri kanan, sangat landai sepanjang dasar. Learning rate harus kecil agar tidak memantul di dinding curam, tetapi maka kemajuan sepanjang dasar sangat lambat.

        Untuk kuadrat dengan kelengkungan `a_max` dan `a_min` pada dua arah, learning rate terbaik adalah `2 / (a_max + a_min)` dengan laju konvergensi `(a_max - a_min) / (a_max + a_min)`. Bila rasio `a_max / a_min` besar, laju mendekati satu dan konvergensi lambat. Rasio itu adalah bilangan kondisi Hessian, yang sudah kamu kenal dari modul aljabar linear.
        """),
        T("""
        ## Gradient descent dalam gambaran besar

        Gradient descent adalah algoritma sederhana yang menopang hampir seluruh pembelajaran mesin modern. Variasinya banyak, tetapi inti ide tetap sama: ukur kemiringan, bergerak sedikit melawannya, ulangi. Pelajaran berikutnya menerapkannya pada model nyata, jadi pastikan kamu nyaman dengan versi satu dimensi ini lebih dulu.
        """),
        E(
            "A3-05-1-ex1",
            "mudah",
            """
            Tulis fungsi `gd_1d(grad, x0, lr, langkah)` yang menjalankan gradient descent satu dimensi dan mengembalikan `x` akhir dibulatkan 4 desimal.
            """,
            """
            def gd_1d(grad, x0, lr, langkah):
                # TODO: implementasikan
                pass
            """,
            """
            g = lambda x: 2 * (x - 3)
            assert gd_1d(g, 0, 0.1, 1) == 0.6
            assert gd_1d(g, 0, 0.1, 5) == 2.017
            assert gd_1d(g, 0, 0.5, 1) == 3.0
            assert gd_1d(g, 10, 1.0, 3) == -4.0
            """,
            "Ulangi x = x - lr * grad(x) sebanyak langkah.",
            """
            def gd_1d(grad, x0, lr, langkah):
                x = float(x0)
                for _ in range(langkah):
                    x -= lr * grad(x)
                return round(x, 4)
            """,
        ),
        E(
            "A3-05-1-ex2",
            "sedang",
            """
            Tulis fungsi `langkah_konvergen(grad, x0, lr, tol=1e-6, maks=10000)` yang mengulang gradient descent sampai `abs(grad(x)) < tol` atau mencapai `maks` iterasi, lalu mengembalikan banyaknya iterasi yang dilakukan.
            """,
            """
            def langkah_konvergen(grad, x0, lr, tol=1e-6, maks=10000):
                # TODO: implementasikan
                pass
            """,
            """
            g = lambda x: 2 * (x - 3)
            assert langkah_konvergen(g, 0, 0.1) == 70
            assert langkah_konvergen(g, 0, 0.5) == 1
            assert langkah_konvergen(g, 0, 1.0, maks=100) == 100
            assert langkah_konvergen(g, 3, 0.5) == 0
            """,
            "Periksa kriteria berhenti sebelum tiap pembaruan dan hitung jumlah pembaruan.",
            """
            def langkah_konvergen(grad, x0, lr, tol=1e-6, maks=10000):
                x = float(x0)
                n = 0
                while abs(grad(x)) >= tol and n < maks:
                    x -= lr * grad(x)
                    n += 1
                return n
            """,
        ),
        E(
            "A3-05-1-ex3",
            "sedang",
            """
            Untuk fungsi kuadrat `f = a/2 x^2` (gradien `a x`), tulis fungsi `kategori_lr(lr, a)` yang mengembalikan `'konvergen'` bila `abs(1 - lr * a) < 1`, `'osilasi'` bila sama dengan 1 (toleransi 1e-12), dan `'divergen'` bila lebih dari 1.
            """,
            """
            def kategori_lr(lr, a):
                # TODO: implementasikan
                pass
            """,
            """
            assert kategori_lr(0.1, 2) == 'konvergen'
            assert kategori_lr(1.0, 2) == 'osilasi'
            assert kategori_lr(1.1, 2) == 'divergen'
            assert kategori_lr(0.5, 2) == 'konvergen'
            """,
            "Hitung faktor mutlak satu dikurangi lr kali a lalu bandingkan dengan satu.",
            """
            def kategori_lr(lr, a):
                f = abs(1 - lr * a)
                if abs(f - 1) < 1e-12:
                    return 'osilasi'
                return 'konvergen' if f < 1 else 'divergen'
            """,
        ),
        E(
            "A3-05-1-ex4",
            "menantang",
            """
            Tulis fungsi `lr_dan_laju(a_max, a_min)` yang mengembalikan tuple `(lr_terbaik, laju)` dengan `lr_terbaik = 2 / (a_max + a_min)` dan `laju = (a_max - a_min) / (a_max + a_min)`, keduanya dibulatkan 4 desimal.
            """,
            """
            def lr_dan_laju(a_max, a_min):
                # TODO: implementasikan
                pass
            """,
            """
            assert lr_dan_laju(2, 2) == (0.5, 0.0)
            assert lr_dan_laju(10, 1) == (0.1818, 0.8182)
            assert lr_dan_laju(100, 1) == (0.0198, 0.9802)
            assert lr_dan_laju(4, 2) == (0.3333, 0.3333)
            """,
            "Langsung terapkan dua rumus lalu bulatkan.",
            """
            def lr_dan_laju(a_max, a_min):
                s = a_max + a_min
                return (round(2 / s, 4), round((a_max - a_min) / s, 4))
            """,
        ),
    ],
    [
        M("Memakai learning rate sembarang tanpa memantau loss.", "Pantau kurva loss dan turunkan lr bila naik."),
        M("Menunggu gradien tepat nol.", "Pakai ambang kecil dan batas iterasi."),
        M("Mengira satu learning rate cocok untuk semua arah.", "Lembah berkondisi buruk butuh strategi tambahan."),
    ],
    [
        Q("Pembaruan gradient descent?", ["x = x + lr g", "x = x - lr g", "x = lr g", "x = x / g"], 1, "Bergerak melawan gradien.", hint="Turun."),
        Q("Learning rate terlalu besar menyebabkan?", ["Konvergen cepat", "Osilasi atau divergen", "Tidak ada efek", "Loss nol"], 1, "Langkah melompati lembah.", hint="Melompat."),
        Q("Mengapa langkah mengecil dekat minimum?", ["lr berubah", "Gradien mengecil", "Data berubah", "Acak"], 1, "Langkah sama dengan lr kali gradien.", hint="Gradien."),
        Q("Kriteria berhenti yang umum?", ["Norma gradien kecil", "Jumlah data", "Nama model", "Jumlah fitur"], 0, "Gradien hampir nol.", hint="Titik datar."),
        Q("Faktor galat pada kuadrat?", ["1 - lr a", "lr a", "1 + lr a", "a / lr"], 0, "Konvergen bila nilai mutlaknya kurang dari satu.", hint="Geometris."),
    ],
    [
        "Gradient descent memperbarui x melawan gradien dengan learning rate.",
        "Learning rate menentukan konvergen, osilasi, atau divergen.",
        "Kriteria berhenti memakai norma gradien, perubahan loss, dan batas iterasi.",
        "Bilangan kondisi memperlambat konvergensi pada lembah sempit.",
    ],
    [],
)

l2 = lesson(
    "A3-05-2",
    "Gradient descent untuk regresi linear",
    35,
    [
        "Menerapkan gradient descent multivariabel pada regresi linear dengan NumPy",
        "Memahami pentingnya normalisasi fitur untuk laju konvergensi",
        "Membedakan batch, stochastic, dan mini-batch gradient descent",
        "Memantau kurva loss untuk memeriksa pelatihan",
    ],
    [
        T("""
        ## Regresi linear dengan gradient descent

        Kita rakit semua bahan pada masalah nyata pertama: regresi linear banyak fitur. Model `y_hat = X w` dengan kolom satu di `X` untuk bias. Loss MSE `L = (1/n) ||X w - y||^2` memiliki gradien `(2/n) X^T (X w - y)`, hasil yang kamu turunkan di modul gradien. Gradient descent memperbarui `w = w - lr * gradien` berulang kali.

        Walau regresi linear bisa diselesaikan langsung dengan persamaan normal, gradient descent penting dipelajari karena model lain seperti regresi logistik dan jaringan saraf tidak punya solusi tertutup. Regresi linear adalah laboratorium yang ideal: kita tahu jawaban benarnya sehingga bisa memeriksa algoritma kita.
        """),
        C(
            """
            import numpy as np

            rng = np.random.default_rng(0)
            X = rng.normal(size=(100, 2))
            y = 3 * X[:, 0] - 2 * X[:, 1] + 1
            Xb = np.column_stack([X, np.ones(100)])
            w = np.zeros(3)
            riwayat = []
            for _ in range(500):
                err = Xb @ w - y
                riwayat.append(float(np.mean(err ** 2)))
                w -= 0.1 * 2 / 100 * Xb.T @ err
            print(w.round(3).tolist())
            print(round(riwayat[0], 4), round(riwayat[-1], 6))
            print(all(a >= b for a, b in zip(riwayat, riwayat[1:])))
            """,
            """
            [3.0, -2.0, 1.0]
            10.8555 0.0
            True
            """,
            """
            Parameter mendekati nilai sebenarnya tiga, minus dua, dan satu. Loss turun setiap iterasi tanpa pernah naik, tanda learning rate aman.
            """,
            filename="regresi_gd.py",
        ),
        T("""
        ## Kurva loss

        Alat diagnosis terpenting adalah **kurva loss**: grafik loss terhadap iterasi. Kurva sehat turun cepat di awal lalu melandai. Kurva yang naik atau bergerigi liar menandakan learning rate terlalu besar. Kurva yang hampir datar sejak awal menandakan learning rate terlalu kecil atau gradien menghilang. Kurva yang turun pada data latih tetapi naik pada data validasi menandakan overfitting.

        Biasakan menyimpan loss tiap iterasi atau tiap epoch dan melihat grafiknya sebelum menyimpulkan apa pun tentang model. Dalam contoh sebelumnya kita memeriksa bahwa riwayat loss monoton menurun, versi sederhana dari pemeriksaan ini tanpa menggambar grafik.
        """),
        T("""
        ## Normalisasi fitur

        Bila fitur memiliki skala sangat berbeda, misalnya satu fitur berkisar satuan dan fitur lain ribuan, lembah loss menjadi sangat sempit. Hessian `2/n X^T X` memiliki eigenvalue yang berbeda jauh, bilangan kondisinya besar, dan learning rate stabil harus sangat kecil sehingga konvergensi lambat. Itulah mengapa praktisi **menstandardisasi** fitur: kurangi rata-rata dan bagi simpangan baku.

        Setelah standardisasi, kolom memiliki variansi satu sehingga skala eigenvalue serupa, kontur lebih mendekati lingkaran, dan gradient descent bergerak hampir lurus menuju minimum. Standardisasi sering menurunkan jumlah iterasi dari ribuan menjadi puluhan. Ingat untuk menyimpan rata-rata dan simpangan baku data latih dan memakainya pula pada data baru.
        """),
        C(
            """
            import numpy as np

            rng = np.random.default_rng(1)
            x1 = rng.normal(size=200)
            x2 = 1000 * rng.normal(size=200) + 5000
            X = np.column_stack([x1, x2])
            Xs = (X - X.mean(axis=0)) / X.std(axis=0)

            def kondisi(A):
                return float(np.linalg.cond(A.T @ A / len(A)))

            print(kondisi(X) > 1e5, round(kondisi(Xs), 2))
            lam_mentah = np.linalg.eigvalsh(2 * X.T @ X / len(X))[-1]
            lam_std = np.linalg.eigvalsh(2 * Xs.T @ Xs / len(Xs))[-1]
            print(lam_mentah > 1e6, round(1 / lam_std, 2))
            """,
            """
            True 1.09
            True 0.48
            """,
            """
            Bilangan kondisi data mentah sangat besar sedangkan data terstandardisasi mendekati satu. Learning rate maksimum yang aman pada data mentah sangat kecil dibanding data terstandardisasi.
            """,
            filename="normalisasi_fitur.py",
        ),
        K(
            "warning",
            """
            Jangan menghitung rata-rata dan simpangan baku dari seluruh data termasuk data uji. Hitung dari data latih lalu terapkan ke data uji, atau informasi data uji bocor ke pelatihan.
            """,
            title="Hindari kebocoran",
        ),
        T("""
        ## Batch, stochastic, dan mini-batch

        Gradien MSE menjumlahkan seluruh data. **Batch gradient descent** memakai seluruh data pada tiap pembaruan: gradien akurat tetapi mahal bila data besar. **Stochastic gradient descent** atau SGD memakai satu sampel acak per pembaruan: sangat murah dan sering, tetapi gradiennya berderau sehingga lintasannya bergerigi. **Mini-batch** memakai sekumpulan kecil sampel, misalnya 32 atau 256, dan merupakan kompromi standar.

        Mini-batch menang karena dua alasan. Gradiennya jauh lebih murah daripada batch penuh namun deraunya lebih kecil daripada SGD, dan operasi pada batch cocok dengan perkalian matriks pada GPU. Satu lintasan penuh atas seluruh data disebut satu **epoch**. Untuk data berukuran `n` dan batch `b`, satu epoch berisi `n / b` pembaruan.
        """),
        C(
            """
            import numpy as np

            rng = np.random.default_rng(0)
            X = rng.normal(size=(100, 2))
            y = 3 * X[:, 0] - 2 * X[:, 1] + 1
            Xb = np.column_stack([X, np.ones(100)])
            w = np.zeros(3)
            batch = 10
            pembaruan = 0
            for epoch in range(30):
                idx = rng.permutation(100)
                for i in range(0, 100, batch):
                    b = idx[i:i + batch]
                    err = Xb[b] @ w - y[b]
                    w -= 0.05 * 2 / len(b) * Xb[b].T @ err
                    pembaruan += 1
            print(pembaruan, 100 // batch)
            print(np.allclose(w, [3, -2, 1], atol=0.05))
            """,
            """
            300 10
            True
            """,
            """
            Tiga puluh epoch dengan sepuluh pembaruan masing-masing menghasilkan 300 pembaruan, dan parameter tetap mendekati solusi sebenarnya.
            """,
            filename="sgd_minibatch.py",
        ),
        T("""
        ## Mengacak data tiap epoch

        Pada SGD dan mini-batch, data diacak ulang setiap epoch. Bila data berurutan, misalnya semua contoh kelas satu dulu baru kelas dua, gradien beberapa langkah berturut-turut akan berat sebelah dan pelatihan bergoyang atau macet. Mengacak memastikan tiap mini-batch mewakili distribusi data secara kira-kira.

        Gunakan generator acak dengan seed tetap agar hasil bisa direproduksi. Pada latihan di bawah kita tidak mengacak agar hasilnya deterministik dan mudah diperiksa, tetapi pada pelatihan nyata pengacakan hampir selalu dipakai.
        """),
        T("""
        ## Persamaan normal sebagai pembanding

        Untuk regresi linear, jawaban tepat bisa diperoleh dari persamaan normal `X^T X w = X^T y`. Karena itu hasil gradient descent selalu bisa diverifikasi dengan membandingkannya ke solusi tertutup. Kebiasaan ini membangun kepercayaan pada kode pelatihan, sebelum kamu beralih ke model yang tidak punya solusi tertutup dan tidak bisa dibandingkan semudah ini.
        """),
        T("""
        ## Memilih ukuran batch

        Ukuran batch memengaruhi kecepatan dan kualitas. Batch kecil memberi banyak pembaruan berderau dan kadang membantu generalisasi. Batch besar memberi gradien halus dan memanfaatkan GPU dengan baik tetapi butuh learning rate lebih besar dan memori lebih banyak. Nilai tiga puluh dua sampai dua ratus lima puluh enam adalah titik awal yang wajar.
        """),
        E(
            "A3-05-2-ex1",
            "mudah",
            """
            Tulis fungsi `prediksi(w, x)` untuk model linear dengan bias. `w` berisi bobot fitur diikuti bias di elemen terakhir, dan `x` adalah list fitur. Kembalikan hasil prediksi.
            """,
            """
            def prediksi(w, x):
                # TODO: implementasikan
                pass
            """,
            """
            assert prediksi([3, -2, 1], [1, 2]) == 0
            assert prediksi([1, 1, 0], [2, 3]) == 5
            assert prediksi([2], []) == 2
            assert prediksi([0.5, 0.5, 0.5], [1, 1]) == 1.5
            """,
            "Jumlahkan bobot kali fitur lalu tambahkan elemen terakhir w.",
            """
            def prediksi(w, x):
                return sum(a * b for a, b in zip(w[:-1], x)) + w[-1]
            """,
        ),
        E(
            "A3-05-2-ex2",
            "sedang",
            """
            Tulis fungsi `gradien_regresi(X, y, w)` yang mengembalikan list gradien MSE terhadap `w` (bobot fitur lalu bias di elemen terakhir), dibulatkan 4 desimal. Hindari `-0.0`.
            """,
            """
            def gradien_regresi(X, y, w):
                # TODO: implementasikan
                pass
            """,
            """
            assert gradien_regresi([[1], [2], [3]], [2, 4, 6], [0, 0]) == [-18.6667, -8.0]
            assert gradien_regresi([[1], [2], [3]], [2, 4, 6], [2, 0]) == [0.0, 0.0]
            assert gradien_regresi([[1, 2]], [0], [1, 1, 0]) == [6.0, 12.0, 6.0]
            assert gradien_regresi([[0]], [1], [0, 0]) == [0.0, -2.0]
            """,
            "Hitung galat tiap sampel lalu rata-ratakan dua kali galat kali fitur serta dua kali galat untuk bias.",
            """
            def gradien_regresi(X, y, w):
                n = len(X)
                d = len(w) - 1
                err = [sum(w[k] * r[k] for k in range(d)) + w[-1] - t for r, t in zip(X, y)]
                g = [2 * sum(e * r[k] for e, r in zip(err, X)) / n for k in range(d)]
                g.append(2 * sum(err) / n)
                return [round(v, 4) + 0.0 for v in g]
            """,
        ),
        E(
            "A3-05-2-ex3",
            "sedang",
            """
            Tulis fungsi `standarisasi_kolom(X)` yang menstandardisasi tiap kolom matriks `X` (list of list) dengan rata-rata dan simpangan baku sampel (dibagi `n - 1`), dibulatkan 4 desimal. Kolom dengan simpangan baku nol menjadi nol semua. Hindari `-0.0`.
            """,
            """
            def standarisasi_kolom(X):
                # TODO: implementasikan
                pass
            """,
            """
            assert standarisasi_kolom([[1, 10], [2, 20], [3, 30]]) == [[-1.0, -1.0], [0.0, 0.0], [1.0, 1.0]]
            assert standarisasi_kolom([[5], [5]]) == [[0.0], [0.0]]
            assert standarisasi_kolom([[0], [2]]) == [[-0.7071], [0.7071]]
            """,
            "Hitung rata-rata dan simpangan baku tiap kolom lalu ubah tiap elemen menjadi z-score.",
            """
            def standarisasi_kolom(X):
                n, d = len(X), len(X[0])
                hasil = [[0.0] * d for _ in range(n)]
                for j in range(d):
                    kol = [r[j] for r in X]
                    m = sum(kol) / n
                    sd = (sum((v - m) ** 2 for v in kol) / (n - 1)) ** 0.5
                    for i in range(n):
                        hasil[i][j] = 0.0 if sd == 0 else round((kol[i] - m) / sd, 4) + 0.0
                return hasil
            """,
        ),
        E(
            "A3-05-2-ex4",
            "menantang",
            """
            Tulis fungsi `epoch_minibatch(X, y, w, lr, batch)` yang menjalankan satu epoch mini-batch gradient descent tanpa pengacakan: bagi data berurutan menjadi kelompok berukuran `batch` (kelompok terakhir boleh lebih kecil), dan perbarui `w` (bobot lalu bias di elemen terakhir) setelah tiap kelompok memakai gradien MSE kelompok itu. Kembalikan `w` dibulatkan 4 desimal.
            """,
            """
            def epoch_minibatch(X, y, w, lr, batch):
                # TODO: implementasikan
                pass
            """,
            """
            X = [[1], [2], [3], [4]]
            y = [2, 4, 6, 8]
            assert epoch_minibatch(X, y, [0, 0], 0.01, 2) == [0.5708, 0.1918]
            assert epoch_minibatch(X, y, [0, 0], 0.01, 4) == [0.3, 0.1]
            assert epoch_minibatch(X, y, [0, 0], 0.01, 1) == [0.971, 0.338]
            assert epoch_minibatch([[1, 2]], [0], [1, 1, 0], 0.1, 1) == [0.4, -0.2, -0.6]
            """,
            "Untuk tiap kelompok hitung gradien dari w terbaru dan perbarui sebelum kelompok berikutnya.",
            """
            def epoch_minibatch(X, y, w, lr, batch):
                w = [float(v) for v in w]
                d = len(w) - 1
                for i in range(0, len(X), batch):
                    xb = X[i:i + batch]
                    yb = y[i:i + batch]
                    n = len(xb)
                    err = [sum(w[k] * r[k] for k in range(d)) + w[-1] - t for r, t in zip(xb, yb)]
                    g = [2 * sum(e * r[k] for e, r in zip(err, xb)) / n for k in range(d)]
                    g.append(2 * sum(err) / n)
                    w = [a - lr * b for a, b in zip(w, g)]
                return [round(v, 4) + 0.0 for v in w]
            """,
        ),
    ],
    [
        M("Tidak menstandardisasi fitur berskala berbeda.", "Standardisasi agar learning rate stabil lebih besar."),
        M("Tidak mengacak data tiap epoch pada SGD.", "Acak agar tiap batch mewakili data."),
        M("Tidak menggambar kurva loss.", "Pantau kurva loss untuk mendiagnosis pelatihan."),
    ],
    [
        Q("Gradien MSE regresi?", ["(2/n) X^T (X w - y)", "X w", "X^T y", "(X w - y)"], 0, "Transpos data dikali residual.", hint="Dua per n."),
        Q("Kurva loss naik berarti?", ["Model bagus", "Learning rate terlalu besar", "Data bagus", "Selesai"], 1, "Langkah melompat.", hint="Divergen."),
        Q("Standardisasi membantu karena?", ["Menambah data", "Memperbaiki bilangan kondisi", "Menghapus fitur", "Mempercepat CPU"], 1, "Skala eigenvalue serupa.", hint="Lembah bundar."),
        Q("Mini-batch adalah?", ["Seluruh data", "Satu sampel", "Kelompok kecil sampel", "Tanpa data"], 2, "Kompromi batch dan SGD.", hint="32 atau 256."),
        Q("Satu epoch berarti?", ["Satu pembaruan", "Satu lintasan seluruh data", "Satu fitur", "Satu lapisan"], 1, "Semua data terlihat sekali.", hint="Lintasan."),
    ],
    [
        "Gradient descent regresi memakai gradien (2/n) X^T (X w - y).",
        "Kurva loss adalah alat diagnosis utama.",
        "Standardisasi fitur mempercepat konvergensi.",
        "Mini-batch menyeimbangkan biaya dan derau gradien.",
    ],
    [],
)

l3 = lesson(
    "A3-05-3",
    "Regresi logistik dengan gradient descent",
    35,
    [
        "Memodelkan peluang dengan sigmoid pada regresi logistik",
        "Menghitung loss cross-entropy biner dan gradiennya",
        "Melatih klasifier dengan gradient descent dan memeriksa gradien",
        "Membandingkan gradient descent dengan solusi tertutup pada regresi linear",
    ],
    [
        T("""
        ## Dari regresi ke klasifikasi

        Regresi linear memprediksi bilangan kontinu. Untuk klasifikasi biner, keluarannya harus peluang antara nol dan satu. **Regresi logistik** menyelesaikannya dengan memasukkan keluaran linear `z = w x + b` ke fungsi sigmoid: `p = 1 / (1 + e^-z)`. Nilai `p` ditafsirkan sebagai peluang kelas positif, dan kita memprediksi kelas satu bila `p > 0,5`, yaitu `z > 0`.

        Batas keputusan adalah himpunan titik dengan `z = 0`, yang berupa garis atau bidang lurus. Jadi regresi logistik adalah klasifier linear walau memakai sigmoid. Meski sederhana, ia sangat kuat sebagai baseline, mudah ditafsirkan, dan merupakan sel dasar jaringan saraf: satu neuron sigmoid sama dengan satu regresi logistik.
        """),
        T("""
        ## Loss cross-entropy

        Galat kuadrat kurang cocok untuk peluang karena menghasilkan loss tak cembung pada regresi logistik dan gradien yang mengecil saat prediksi jenuh. Pilihan standar adalah **cross-entropy biner**: `L = -(1/n) sum [ y log p + (1 - y) log (1 - p) ]`. Bila label satu, loss `-log p` kecil bila `p` dekat satu dan sangat besar bila `p` dekat nol. Prediksi yakin tetapi salah dihukum sangat berat.

        Loss ini berasal dari prinsip kemungkinan maksimum: meminimalkannya sama dengan memaksimalkan peluang yang diberikan model pada label yang diamati. Satu catatan praktis: `log 0` tidak terdefinisi, jadi nilai `p` dipotong ke rentang kecil agar aman, misalnya antara `1e-12` dan `1 - 1e-12`.
        """),
        T("""
        ## Gradien yang elegan

        Turunan cross-entropy terhadap parameter ternyata sangat sederhana. Dengan aturan rantai, faktor turunan sigmoid saling meniadakan dengan penyebut turunan log, sehingga `dL/dz = p - y`. Maka `dL/dw = (1/n) sum (p_i - y_i) x_i` dan `dL/db = (1/n) sum (p_i - y_i)`. Bentuknya sama persis dengan gradien regresi linear, hanya prediksi diganti peluang.

        Kesederhanaan ini bukan kebetulan: sigmoid dan cross-entropy adalah pasangan yang cocok. Gradien sama dengan galat `p - y` yang tetap besar saat prediksi sangat salah, berbeda dengan galat kuadrat yang gradiennya padam pada kondisi itu. Itulah mengapa cross-entropy dipakai di hampir semua klasifier modern.
        """),
        C(
            """
            import numpy as np

            x = np.array([-3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0])
            y = np.array([0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0])

            def sigmoid(z):
                return 1 / (1 + np.exp(-z))

            def loss(w, b):
                p = np.clip(sigmoid(w * x + b), 1e-12, 1 - 1e-12)
                return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))

            w, b = 0.0, 0.0
            print(round(loss(w, b), 4))
            for _ in range(1000):
                p = sigmoid(w * x + b)
                w -= 0.1 * np.mean((p - y) * x)
                b -= 0.1 * np.mean(p - y)
            print(round(w, 3), round(b, 3), round(loss(w, b), 4))
            akurasi = np.mean((sigmoid(w * x + b) > 0.5) == y)
            print(round(float(akurasi), 4))
            """,
            """
            0.6931
            1.251 0.641 0.3559
            0.7143
            """,
            """
            Loss awal sama dengan log dua karena semua peluang 0,5. Setelah pelatihan loss turun dan sebagian besar titik terklasifikasi benar. Data ini tidak terpisah sempurna karena satu titik berada di sisi yang salah.
            """,
            filename="regresi_logistik.py",
        ),
        K(
            "tip",
            """
            Pada data yang terpisah sempurna bobot regresi logistik tanpa regularisasi terus membesar tanpa batas karena loss selalu bisa diturunkan dengan memperbesar keyakinan. Tambahkan regularisasi L2 atau batasi iterasi.
            """,
            title="Data terpisah sempurna",
        ),
        T("""
        ## Memeriksa gradien

        Karena gradien dihitung dengan rumus buatan sendiri, bandingkan dengan turunan numerik sebelum memercayainya. Pilih beberapa nilai parameter acak, hitung gradien analitik lewat rumus `p - y`, hitung gradien numerik lewat selisih pusat pada loss, lalu pastikan keduanya hampir sama. Pemeriksaan ini hanya membutuhkan beberapa baris dan menyelamatkan berjam-jam debugging.

        Dalam praktik, kesalahan paling umum adalah lupa membagi dengan `n`, menukar tanda `p - y` menjadi `y - p`, atau lupa bias. Gradient check menangkap ketiganya sekaligus karena hasil numeriknya bergantung hanya pada loss, bukan pada rumus yang ingin diuji.
        """),
        C(
            """
            import numpy as np

            rng = np.random.default_rng(3)
            X = rng.normal(size=(50, 2))
            y = (X[:, 0] - X[:, 1] > 0).astype(float)

            def sigmoid(z):
                return 1 / (1 + np.exp(-z))

            def loss(w, b):
                p = np.clip(sigmoid(X @ w + b), 1e-12, 1 - 1e-12)
                return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))

            w = np.array([0.3, -0.2])
            b = 0.1
            p = sigmoid(X @ w + b)
            dw = X.T @ (p - y) / len(y)
            db = float(np.mean(p - y))
            eps = 1e-6
            dw_num = np.array([(loss(w + eps * e, b) - loss(w - eps * e, b)) / (2 * eps) for e in np.eye(2)])
            db_num = (loss(w, b + eps) - loss(w, b - eps)) / (2 * eps)
            print(np.allclose(dw, dw_num, atol=1e-6), abs(db - db_num) < 1e-6)
            print(dw.round(4).tolist(), round(db, 4))
            """,
            """
            True True
            [-0.2073, 0.2244] -0.0296
            """,
            """
            Gradien analitik cocok dengan gradien numerik untuk bobot dan bias. Rumus `p - y` terbukti benar.
            """,
            filename="gradcheck_logistik.py",
        ),
        T("""
        ## Membandingkan dengan solusi tertutup

        Untuk regresi linear kita punya dua jalan: persamaan normal atau gradient descent. Persamaan normal memberi jawaban tepat dalam satu langkah tetapi membutuhkan penyelesaian sistem linear berukuran jumlah fitur, yang mahal bila fitur sangat banyak. Gradient descent mendekati jawaban secara iteratif dengan biaya per langkah yang murah dan bisa dihentikan lebih awal.

        Bila keduanya diterapkan pada soal yang sama, hasilnya harus sama pada akhir pelatihan. Kesesuaian ini adalah cara terbaik memverifikasi implementasi gradient descent: bandingkan dengan `np.linalg.lstsq`. Bila berbeda jauh, curigai learning rate, jumlah iterasi, atau gradien yang salah.
        """),
        C(
            """
            import numpy as np

            rng = np.random.default_rng(2)
            X = rng.normal(size=(100, 2))
            y = 3 * X[:, 0] - 2 * X[:, 1] + 1 + 0.1 * rng.normal(size=100)
            Xb = np.column_stack([X, np.ones(100)])
            w_tutup = np.linalg.lstsq(Xb, y, rcond=None)[0]
            w = np.zeros(3)
            for _ in range(2000):
                w -= 0.1 * 2 / 100 * Xb.T @ (Xb @ w - y)
            print(w_tutup.round(3).tolist(), w.round(3).tolist())
            print(np.allclose(w, w_tutup, atol=1e-6))
            """,
            """
            [3.005, -2.015, 0.984] [3.005, -2.015, 0.984]
            True
            """,
            """
            Solusi gradient descent setelah 2000 iterasi identik dengan solusi tertutup sampai enam desimal, memverifikasi implementasi.
            """,
            filename="bandingkan_solusi.py",
        ),
        T("""
        ## Dari regresi logistik ke jaringan saraf

        Satu neuron sigmoid dengan loss cross-entropy tak lain dari regresi logistik. Jaringan saraf menumpuk banyak neuron seperti itu dan melatihnya dengan backpropagation. Jadi semua yang kamu pelajari di modul ini, yaitu gradien, pembaruan, dan pemeriksaan, berlaku langsung pada model yang jauh lebih besar.
        """),
        T("""
        ## Menafsirkan bobot

        Bobot regresi logistik mudah ditafsirkan. Bobot positif berarti fitur itu menaikkan peluang kelas positif dan bobot negatif menurunkannya. Besarnya menunjukkan kekuatan pengaruh bila fitur berskala sebanding, itulah satu lagi alasan standardisasi berguna. Interpretasi ini membuat regresi logistik tetap dipakai di bidang yang menuntut penjelasan.
        """),
        E(
            "A3-05-3-ex1",
            "mudah",
            """
            Tulis fungsi `prob_logistik(w, b, x)` yang mengembalikan peluang sigmoid dari `w . x + b` dibulatkan 4 desimal, stabil untuk masukan ekstrem, memakai `math.exp`.
            """,
            """
            import math

            def prob_logistik(w, b, x):
                # TODO: implementasikan
                pass
            """,
            """
            assert prob_logistik([1], 0, [0]) == 0.5
            assert prob_logistik([2], -1, [1]) == 0.7311
            assert prob_logistik([1, 1], 0, [-5, -5]) == 0.0
            assert prob_logistik([0], 3, [7]) == 0.9526
            assert prob_logistik([1], 0, [-1000]) == 0.0
            """,
            "Hitung z lalu terapkan sigmoid dengan cabang untuk z negatif.",
            """
            import math

            def prob_logistik(w, b, x):
                z = sum(a * c for a, c in zip(w, x)) + b
                if z >= 0:
                    p = 1 / (1 + math.exp(-z))
                else:
                    e = math.exp(z)
                    p = e / (1 + e)
                return round(p, 4)
            """,
        ),
        E(
            "A3-05-3-ex2",
            "sedang",
            """
            Tulis fungsi `bce(p, y)` yang mengembalikan rata-rata cross-entropy biner dari list peluang `p` dan label `y`, dengan `p` dipotong ke `[1e-12, 1 - 1e-12]`, dibulatkan 4 desimal.
            """,
            """
            import math

            def bce(p, y):
                # TODO: implementasikan
                pass
            """,
            """
            assert bce([0.5], [1]) == 0.6931
            assert bce([0.9, 0.1], [1, 0]) == 0.1054
            assert bce([1.0], [1]) == 0.0
            assert bce([0.0], [1]) == 27.631
            """,
            "Potong p lalu rata-ratakan minus y log p minus satu dikurangi y kali log satu dikurangi p.",
            """
            import math

            def bce(p, y):
                eps = 1e-12
                total = 0.0
                for a, t in zip(p, y):
                    a = min(max(a, eps), 1 - eps)
                    total += -(t * math.log(a) + (1 - t) * math.log(1 - a))
                return round(total / len(p), 4)
            """,
        ),
        E(
            "A3-05-3-ex3",
            "sedang",
            """
            Tulis fungsi `gradien_logistik(X, y, w, b)` yang mengembalikan tuple `(dw, db)`, dengan `dw` list gradien bobot dan `db` gradien bias dari cross-entropy rata-rata, dibulatkan 4 desimal. Hindari `-0.0`. Gunakan `math.exp` untuk sigmoid.
            """,
            """
            import math

            def gradien_logistik(X, y, w, b):
                # TODO: implementasikan
                pass
            """,
            """
            X = [[-3], [-2], [-1], [0], [1], [2], [3]]
            y = [0, 0, 1, 0, 1, 1, 1]
            assert gradien_logistik(X, y, [0], 0) == ([-0.7143], -0.0714)
            assert gradien_logistik([[1, 2]], [1], [0, 0], 0) == ([-0.5, -1.0], -0.5)
            assert gradien_logistik([[0]], [0], [5], 0) == ([0.0], 0.5)
            assert gradien_logistik([[1]], [1], [10], 0) == ([0.0], 0.0)
            """,
            "Hitung galat p minus y per sampel lalu rata-ratakan galat dikali fitur dan galat itu sendiri.",
            """
            import math

            def gradien_logistik(X, y, w, b):
                n = len(X)
                d = len(w)
                galat = []
                for r, t in zip(X, y):
                    z = sum(w[k] * r[k] for k in range(d)) + b
                    if z >= 0:
                        p = 1 / (1 + math.exp(-z))
                    else:
                        e = math.exp(z)
                        p = e / (1 + e)
                    galat.append(p - t)
                dw = [round(sum(g * r[k] for g, r in zip(galat, X)) / n, 4) + 0.0 for k in range(d)]
                db = round(sum(galat) / n, 4) + 0.0
                return (dw, db)
            """,
        ),
        E(
            "A3-05-3-ex4",
            "menantang",
            """
            Tulis fungsi `latih_logistik(X, y, lr, langkah)` yang melatih regresi logistik dengan gradient descent batch mulai dari bobot nol dan bias nol, dan mengembalikan tuple `(w, b)` dengan `w` list dibulatkan 3 desimal dan `b` dibulatkan 3 desimal. Gunakan `math.exp` dan hindari overflow dengan cabang untuk `z` negatif.
            """,
            """
            import math

            def latih_logistik(X, y, lr, langkah):
                # TODO: implementasikan
                pass
            """,
            """
            def akurasi(X, y, w, b):
                benar = 0
                for r, t in zip(X, y):
                    z = sum(a * c for a, c in zip(w, r)) + b
                    benar += int((z > 0) == bool(t))
                return benar / len(y)

            X1 = [[-2], [-1], [1], [2]]
            y1 = [0, 0, 1, 1]
            w1, b1 = latih_logistik(X1, y1, 0.5, 2000)
            assert w1[0] > 0 and akurasi(X1, y1, w1, b1) == 1.0
            X2 = [[0, 0], [0, 1], [1, 0], [1, 1]]
            y2 = [0, 0, 0, 1]
            w2, b2 = latih_logistik(X2, y2, 1.0, 5000)
            assert akurasi(X2, y2, w2, b2) == 1.0
            assert b2 < 0 and w2[0] > 0 and w2[1] > 0
            w3, b3 = latih_logistik(X1, y1, 0.5, 0)
            assert w3 == [0.0] and b3 == 0.0
            """,
            "Pada tiap iterasi hitung galat p minus y, rata-ratakan galat dikali fitur untuk bobot dan galat untuk bias, lalu perbarui.",
            """
            import math

            def latih_logistik(X, y, lr, langkah):
                n = len(X)
                d = len(X[0])
                w = [0.0] * d
                b = 0.0
                for _ in range(langkah):
                    galat = []
                    for r, t in zip(X, y):
                        z = sum(w[k] * r[k] for k in range(d)) + b
                        if z >= 0:
                            p = 1 / (1 + math.exp(-z))
                        else:
                            e = math.exp(z)
                            p = e / (1 + e)
                        galat.append(p - t)
                    gw = [sum(g * r[k] for g, r in zip(galat, X)) / n for k in range(d)]
                    gb = sum(galat) / n
                    w = [a - lr * c for a, c in zip(w, gw)]
                    b -= lr * gb
                return ([round(v, 3) + 0.0 for v in w], round(b, 3) + 0.0)
            """,
        ),
    ],
    [
        M("Memakai galat kuadrat untuk regresi logistik.", "Pakai cross-entropy agar gradien tetap informatif."),
        M("Menukar tanda p - y.", "Gradient check menangkap kesalahan tanda."),
        M("Melatih data terpisah sempurna tanpa regularisasi.", "Batasi iterasi atau tambah regularisasi L2."),
    ],
    [
        Q("Keluaran regresi logistik?", ["Bilangan bebas", "Peluang antara 0 dan 1", "Kelas langsung", "Gradien"], 1, "Sigmoid dari z.", hint="Sigmoid."),
        Q("dL/dz cross-entropy dengan sigmoid?", ["p - y", "y - p kuadrat", "p y", "1 - p"], 0, "Bentuk sederhana yang indah.", hint="Galat."),
        Q("Batas keputusan regresi logistik?", ["Lengkung acak", "Garis atau bidang lurus", "Lingkaran", "Titik"], 1, "z = 0.", hint="Linear."),
        Q("Mengapa memotong p pada cross-entropy?", ["Mempercepat", "Menghindari log nol", "Menghapus data", "Mengurangi fitur"], 1, "log 0 tidak terdefinisi.", hint="Aman."),
        Q("Cara memverifikasi gradient descent regresi linear?", ["Bandingkan dengan lstsq", "Tambah data", "Kurangi fitur", "Ganti loss"], 0, "Solusi tertutup sebagai acuan.", hint="Persamaan normal."),
    ],
    [
        "Regresi logistik memakai sigmoid dan cross-entropy biner.",
        "Gradiennya berbentuk (p - y) dikali fitur dan dirata-rata.",
        "Gradient check dan perbandingan dengan solusi tertutup memverifikasi implementasi.",
        "Data terpisah sempurna membutuhkan regularisasi atau batas iterasi.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perhitungan yang cukup jelas dalam teks.", "brief": []}

write_module(
    "A3",
    5,
    "Gradient descent dari nol",
    105,
    [
        "Memahami dan mengimplementasikan gradient descent",
        "Menerapkannya pada regresi linear dengan normalisasi dan mini-batch",
        "Menerapkannya pada regresi logistik dan memverifikasi gradien",
    ],
    [l1, l2, l3],
    video,
    REF,
)
