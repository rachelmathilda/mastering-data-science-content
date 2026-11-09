import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

l1 = lesson(
    "A3-01-1",
    "Fungsi dan grafiknya",
    35,
    [
        "Memahami fungsi sebagai pemetaan dengan domain dan range",
        "Menyusun komposisi fungsi",
        "Mengenali fungsi yang sering muncul dalam ML",
        "Memakai eksponen dan logaritma dengan benar",
    ],
    [
        T("""
        ## Fungsi sebagai mesin

        **Fungsi** adalah aturan yang memetakan setiap masukan ke tepat satu keluaran. Tulis `y = f(x)`: `x` adalah masukan, `f` aturan, dan `y` keluaran. Himpunan masukan yang diizinkan disebut **domain**, dan himpunan keluaran yang benar-benar muncul disebut **range**. Fungsi `f(x) = sqrt(x)` hanya terdefinisi untuk `x` tak negatif, dan `f(x) = 1/x` tidak terdefinisi di nol.

        Dalam machine learning hampir semua hal adalah fungsi. Model adalah fungsi dari fitur ke prediksi. Fungsi loss memetakan parameter ke bilangan yang mengukur seberapa buruk model. Melatih model berarti mencari masukan fungsi loss yang memberi keluaran terkecil. Karena itu memahami perilaku fungsi adalah fondasi seluruh modul kalkulus ini.
        """),
        T("""
        ## Membaca grafik

        Grafik fungsi adalah kumpulan titik `(x, f(x))`. Dari grafik kita membaca banyak sifat sekaligus: di mana fungsi naik atau turun, di mana ia mencapai puncak atau lembah, dan apakah ia putus. Fungsi **naik** bila `f` makin besar saat `x` bertambah, dan **turun** bila sebaliknya. Titik tempat arah berubah adalah kandidat nilai maksimum atau minimum, yang menjadi pusat perhatian dalam optimasi.

        Sebuah kurva adalah grafik fungsi hanya bila setiap garis vertikal memotongnya paling banyak sekali. Lingkaran bukan fungsi dari `x` karena satu `x` memberi dua `y`. Uji garis vertikal ini sederhana tetapi berguna untuk memeriksa apakah suatu hubungan benar-benar fungsi.
        """),
        T("""
        ## Komposisi fungsi

        Dua fungsi dapat digabung dengan memasukkan keluaran satu ke yang lain: `(f o g)(x) = f(g(x))`. Urutan penting. Mengalikan dua lalu menambah satu berbeda dari menambah satu lalu mengalikan dua. Secara umum `f(g(x))` tidak sama dengan `g(f(x))`.

        Komposisi adalah cara kerja jaringan saraf: tiap lapisan adalah fungsi, dan jaringan penuh adalah komposisi banyak lapisan. Lapisan pertama mengubah masukan, lapisan kedua mengubah hasilnya, dan seterusnya sampai prediksi. Pada modul turunan nanti kamu akan melihat aturan rantai, alat untuk menurunkan komposisi, yang menjadi dasar algoritma backpropagation.
        """),
        C(
            """
            def f(x):
                return x ** 2 + 1

            def g(x):
                return 2 * x + 1

            def komposisi(f, g):
                return lambda x: f(g(x))

            print(f(3), g(3))
            fg = komposisi(f, g)
            gf = komposisi(g, f)
            print(fg(1), gf(1))
            print(fg(2) == gf(2))
            """,
            """
            10 7
            10 5
            False
            """,
            """
            `fg(1)` menghitung `f(g(1)) = f(3) = 10` sedangkan `gf(1)` menghitung `g(f(1)) = g(2) = 5`. Urutan komposisi memengaruhi hasil.
            """,
            filename="fungsi_dasar.py",
        ),
        T("""
        ## Fungsi yang sering muncul

        Beberapa keluarga fungsi muncul berulang kali. **Fungsi linear** `a x + b` membentuk garis lurus dan menjadi bahan dasar regresi. **Polinom** seperti `x^2` dan `x^3` membentuk kurva halus dan dipakai untuk memodelkan hubungan melengkung. **Eksponen** `e^x` tumbuh sangat cepat dan selalu positif, sedangkan **logaritma** `ln x` adalah kebalikannya dan tumbuh sangat lambat.

        Dalam ML ada fungsi aktivasi yang harus kamu kenal. **Sigmoid** `1 / (1 + e^-x)` memampatkan bilangan apa pun ke antara nol dan satu sehingga cocok sebagai peluang. **Tanh** serupa tetapi berkisar antara minus satu dan satu. **ReLU** `max(0, x)` mengembalikan nol untuk masukan negatif dan masukan itu sendiri untuk yang positif, sederhana dan cepat sehingga menjadi pilihan umum pada jaringan dalam.
        """),
        C(
            """
            import numpy as np

            def sigmoid(x):
                return 1 / (1 + np.exp(-x))

            def relu(x):
                return np.maximum(0, x)

            x = np.array([-2.0, 0.0, 2.0])
            print(sigmoid(x).round(4).tolist())
            print(relu(np.array([-3.0, 2.5])).tolist())
            print(np.tanh(x).round(4).tolist())
            print(np.allclose(sigmoid(x) + sigmoid(-x), 1))
            """,
            """
            [0.1192, 0.5, 0.8808]
            [0.0, 2.5]
            [-0.964, 0.0, 0.964]
            True
            """,
            """
            Sigmoid simetris di sekitar 0,5 sehingga `sigmoid(x) + sigmoid(-x)` selalu satu. ReLU memotong nilai negatif menjadi nol.
            """,
            filename="fungsi_ml.py",
        ),
        K(
            "tip",
            """
            Untuk masukan yang sangat negatif `np.exp(-x)` pada sigmoid bisa meluap. Pada kode produksi gunakan versi stabil yang memakai `e^x / (1 + e^x)` untuk `x` negatif.
            """,
            title="Hati-hati overflow",
        ),
        T("""
        ## Eksponen dan logaritma

        Eksponen dan logaritma adalah pasangan invers: `ln(e^x) = x` dan `e^(ln x) = x`. Logaritma mengubah perkalian menjadi penjumlahan: `ln(a b) = ln a + ln b`, dan pangkat menjadi perkalian: `ln(a^n) = n ln a`. Sifat ini sangat berguna dalam statistik karena peluang gabungan adalah hasil kali yang bisa menjadi sangat kecil, sehingga kita menjumlahkan log-peluangnya demi kestabilan numerik.

        Domain logaritma hanya bilangan positif. `ln 0` tak terhingga negatif dan `ln` bilangan negatif tidak terdefinisi pada bilangan real. Kesalahan umum dalam kode adalah menghitung log dari nol, misalnya saat peluang prediksi tepat nol pada cross-entropy. Biasanya kita menambahkan bilangan sangat kecil agar aman.
        """),
        C(
            """
            import math

            print(round(math.exp(1), 4), round(math.log(math.e ** 3), 4))
            print(round(math.log(6), 4), round(math.log(2) + math.log(3), 4))
            print(round(math.log2(8), 4), round(math.log10(1000), 4))
            """,
            """
            2.7183 3.0
            1.7918 1.7918
            3.0 3.0
            """,
            """
            Logaritma menjadikan hasil kali sebagai penjumlahan. Basis dua dan sepuluh memberi hasil bulat pada pangkat yang cocok.
            """,
            filename="eksponen_log.py",
        ),
        T("""
        ## Bentuk fungsi dan intuisinya

        Mengenali bentuk fungsi membantu menebak perilaku sebelum menghitung. Garis lurus memiliki laju perubahan tetap. Parabola `x^2` punya satu lembah di nol dan memiliki dua cabang simetris. Eksponen tumbuh makin cepat, logaritma makin lambat, dan sigmoid melandai di kedua ujungnya sehingga perubahan masukan besar hampir tidak mengubah keluaran.

        Intuisi ini kelak menjelaskan mengapa pelatihan jaringan bisa macet. Bila keluaran sigmoid sudah mendekati nol atau satu, kemiringan kurvanya hampir nol, dan sinyal untuk memperbaiki parameter menghilang. ReLU menghindari masalah itu untuk masukan positif. Memahami grafik adalah langkah pertama memahami perilaku optimasi.
        """),
        E(
            "A3-01-1-ex1",
            "mudah",
            """
            Tulis fungsi `f_polinom(koef, x)` yang menghitung nilai polinom dengan koefisien dari pangkat tertinggi ke terendah (skema Horner).
            """,
            """
            def f_polinom(koef, x):
                # TODO: implementasikan
                pass
            """,
            """
            assert f_polinom([1, 0, 1], 3) == 10
            assert f_polinom([2, 1], 3) == 7
            assert f_polinom([5], 10) == 5
            assert f_polinom([1, -3, 2], 1) == 0
            """,
            "Mulai dari nol lalu ulangi hasil kali x ditambah koefisien berikutnya.",
            """
            def f_polinom(koef, x):
                hasil = 0
                for c in koef:
                    hasil = hasil * x + c
                return hasil
            """,
        ),
        E(
            "A3-01-1-ex2",
            "mudah",
            """
            Tulis fungsi `komposisi(f, g)` yang mengembalikan fungsi baru yang menghitung `f(g(x))`.
            """,
            """
            def komposisi(f, g):
                # TODO: implementasikan
                pass
            """,
            """
            assert komposisi(lambda x: x + 1, lambda x: x * 2)(3) == 7
            assert komposisi(lambda x: x * 2, lambda x: x + 1)(3) == 8
            assert komposisi(abs, lambda x: x - 5)(2) == 3
            assert komposisi(lambda x: x ** 2, lambda x: x ** 2)(2) == 16
            """,
            "Kembalikan fungsi lambda yang memanggil g lalu f.",
            """
            def komposisi(f, g):
                return lambda x: f(g(x))
            """,
        ),
        E(
            "A3-01-1-ex3",
            "sedang",
            """
            Tulis fungsi `sigmoid(x)` dengan `math.exp` yang stabil untuk `x` sangat negatif atau sangat positif dan mengembalikan hasil dibulatkan 4 desimal.
            """,
            """
            import math

            def sigmoid(x):
                # TODO: implementasikan
                pass
            """,
            """
            assert sigmoid(0) == 0.5
            assert sigmoid(2) == 0.8808
            assert sigmoid(-2) == 0.1192
            assert sigmoid(10) == 1.0
            assert sigmoid(-1000) == 0.0
            """,
            "Untuk x nonnegatif pakai 1/(1+e^-x) dan untuk x negatif pakai e^x/(1+e^x).",
            """
            import math

            def sigmoid(x):
                if x >= 0:
                    return round(1 / (1 + math.exp(-x)), 4)
                z = math.exp(x)
                return round(z / (1 + z), 4)
            """,
        ),
        E(
            "A3-01-1-ex4",
            "menantang",
            """
            Tulis fungsi `softplus(x)` yaitu `ln(1 + e^x)` yang stabil untuk `x` besar (jangan menghitung `e^x` langsung untuk `x` besar). Gunakan identitas `max(x, 0) + ln(1 + e^-|x|)` dan bulatkan 4 desimal.
            """,
            """
            import math

            def softplus(x):
                # TODO: implementasikan
                pass
            """,
            """
            assert softplus(0) == 0.6931
            assert softplus(2) == 2.1269
            assert softplus(-2) == 0.1269
            assert softplus(100) == 100.0
            assert softplus(-100) == 0.0
            """,
            "Gunakan math.log1p dan exp dari minus nilai mutlak x.",
            """
            import math

            def softplus(x):
                return round(max(x, 0) + math.log1p(math.exp(-abs(x))), 4)
            """,
        ),
    ],
    [
        M("Mengira komposisi bersifat komutatif.", "Urutan f(g(x)) dan g(f(x)) umumnya berbeda."),
        M("Menghitung log dari nol atau bilangan negatif.", "Domain log hanya bilangan positif."),
        M("Memakai sigmoid naif untuk masukan sangat negatif.", "Gunakan versi stabil untuk menghindari overflow."),
    ],
    [
        Q("Fungsi memetakan setiap masukan ke?", ["Banyak keluaran", "Tepat satu keluaran", "Tidak ada keluaran", "Dua keluaran"], 1, "Satu masukan memberi satu keluaran.", hint="Uji garis vertikal."),
        Q("Domain adalah?", ["Himpunan keluaran", "Himpunan masukan yang diizinkan", "Kemiringan", "Titik puncak"], 1, "Masukan yang membuat fungsi terdefinisi.", hint="Masukan."),
        Q("Komposisi f(g(x)) berarti?", ["g dulu lalu f", "f dulu lalu g", "f dikali g", "f ditambah g"], 0, "Masukkan keluaran g ke f.", hint="Dalam ke luar."),
        Q("Sigmoid berkisar antara?", ["-1 dan 1", "0 dan 1", "0 dan tak hingga", "Semua bilangan"], 1, "Memampatkan ke antara nol dan satu.", hint="Peluang."),
        Q("ln(a b) sama dengan?", ["ln a ln b", "ln a + ln b", "ln a - ln b", "a ln b"], 1, "Log mengubah kali menjadi tambah.", hint="Sifat log."),
    ],
    [
        "Fungsi memetakan masukan ke satu keluaran dan memiliki domain dan range.",
        "Komposisi fungsi adalah dasar jaringan saraf.",
        "Sigmoid, tanh, dan ReLU adalah fungsi aktivasi penting.",
        "Logaritma mengubah perkalian menjadi penjumlahan dan hanya terdefinisi untuk bilangan positif.",
    ],
    [],
)

l2 = lesson(
    "A3-01-2",
    "Limit",
    35,
    [
        "Memahami limit sebagai nilai yang didekati fungsi",
        "Memeriksa limit secara numerik dari kiri dan kanan",
        "Memakai limit di tak hingga",
        "Mengenali limit penting yang mendasari turunan",
    ],
    [
        T("""
        ## Mendekati tanpa menyentuh

        **Limit** menjawab pertanyaan: ke nilai berapa `f(x)` mendekat saat `x` mendekati suatu titik `a`, tanpa harus mencapainya? Ditulis `lim x->a f(x) = L`. Yang penting adalah perilaku di sekitar `a`, bukan nilai di `a` itu sendiri. Fungsi bahkan boleh tidak terdefinisi di `a` namun tetap punya limit di sana.

        Contoh klasik `f(x) = (x^2 - 1) / (x - 1)`. Di `x = 1` penyebutnya nol, jadi `f(1)` tidak ada. Namun untuk `x` dekat satu, pembilangnya bisa difaktorkan menjadi `(x - 1)(x + 1)` sehingga `f(x) = x + 1`, dan nilainya mendekati dua. Limitnya dua walau fungsinya berlubang di satu.
        """),
        C(
            """
            def f(x):
                return (x ** 2 - 1) / (x - 1)

            for h in (0.1, 0.01, 0.001):
                print(round(f(1 - h), 4), round(f(1 + h), 4))
            """,
            """
            1.9 2.1
            1.99 2.01
            1.999 2.001
            """,
            """
            Dari kiri dan kanan nilainya mendekati 2 walau `f(1)` sendiri tidak terdefinisi. Bila kedua sisi mendekati bilangan sama, limitnya ada.
            """,
            filename="limit_numerik.py",
        ),
        T("""
        ## Limit satu sisi

        Kadang pendekatan dari kiri dan dari kanan menuju nilai berbeda. **Limit kiri** adalah nilai yang didekati saat `x` datang dari bawah dan **limit kanan** saat datang dari atas. Limit biasa hanya ada bila keduanya ada dan sama. Bila berbeda, kita katakan limit tidak ada, walau limit satu sisinya masing-masing ada.

        Contohnya fungsi tanda `|x| / x`. Untuk `x` positif nilainya satu dan untuk `x` negatif minus satu. Saat `x` mendekati nol dari kanan limitnya satu dan dari kiri minus satu. Grafiknya melompat di nol, dan tidak ada nilai tunggal yang didekati. Fungsi tangga yang dipakai dalam klasifikasi biner juga memiliki lompatan seperti ini.
        """),
        C(
            """
            def tanda(x):
                return abs(x) / x

            print(tanda(-1e-6), tanda(1e-6))
            print([1 / 10 ** k for k in range(1, 5)])
            print([tanda(-1 / 10 ** k) for k in range(1, 4)])
            """,
            """
            -1.0 1.0
            [0.1, 0.01, 0.001, 0.0001]
            [-1.0, -1.0, -1.0]
            """,
            """
            Limit kiri sama dengan minus satu dan limit kanan satu sehingga limit di nol tidak ada. Baris kedua menunjukkan `1/x` yang mengecil menuju nol saat `x` membesar.
            """,
            filename="limit_sisi.py",
        ),
        T("""
        ## Limit di tak hingga

        Kita juga bisa bertanya apa yang terjadi saat `x` membesar tanpa batas. `lim x->tak hingga 1/x = 0` karena pembagian dengan bilangan raksasa menghasilkan bilangan mendekati nol. Fungsi `(3x + 1) / (x + 2)` mendekati tiga karena untuk `x` besar suku konstan menjadi tidak berarti dan rasio mendekati `3x / x`.

        Limit di tak hingga menjelaskan perilaku jangka panjang. Dalam ML, sigmoid mendekati satu saat masukan besar dan nol saat sangat negatif, sehingga kedua ujung grafiknya memiliki **asimtot datar**. Learning rate yang menurun menuju nol, atau galat yang menurun seiring bertambahnya data, juga dijelaskan lewat konsep limit.
        """),
        K(
            "tip",
            """
            Untuk pecahan polinom saat `x` menuju tak hingga, lihat suku berpangkat tertinggi di pembilang dan penyebut. Bila pangkatnya sama, limitnya adalah rasio koefisien. Bila penyebut berpangkat lebih tinggi, limitnya nol.
            """,
            title="Jalan pintas",
        ),
        T("""
        ## Aturan limit

        Limit berperilaku rapi terhadap operasi aritmetika. Limit jumlah adalah jumlah limit, limit hasil kali adalah hasil kali limit, dan limit hasil bagi adalah hasil bagi limit selama limit penyebut tidak nol. Konstanta bisa dikeluarkan dari limit. Untuk fungsi polinom, limit di suatu titik cukup dengan mensubstitusikan titik itu.

        Bila substitusi menghasilkan bentuk tak tentu seperti `0/0`, kita perlu menyederhanakan dulu, misalnya dengan memfaktorkan seperti pada contoh sebelumnya, atau mengalikan dengan sekawan untuk bentuk akar. Teknik ini muncul lagi saat menurunkan fungsi dari definisi, karena definisi turunan selalu berbentuk `0/0`.
        """),
        T("""
        ## Limit-limit penting

        Beberapa limit khusus layak dihafal. `sin(x) / x` mendekati satu saat `x` menuju nol, dengan `x` dalam radian. `(1 + 1/n)^n` mendekati `e`, bilangan dasar logaritma natural, saat `n` membesar. `(e^h - 1) / h` mendekati satu saat `h` menuju nol, dan inilah alasan turunan `e^x` adalah `e^x` sendiri.

        Limit ini bukan hanya trik. Limit kedua menunjukkan asal bunga majemuk kontinu, dan limit ketiga menjadi dasar turunan fungsi eksponen. Kamu bisa memeriksa ketiganya secara numerik dengan nilai yang cukup dekat, seperti pada contoh berikut.
        """),
        C(
            """
            import math

            print(round(math.sin(0.1) / 0.1, 4), round(math.sin(0.01) / 0.01, 4))
            n = 10 ** 6
            print(round((1 + 1 / n) ** n, 4))
            h = 0.001
            print(round((math.exp(h) - 1) / h, 4))
            """,
            """
            0.9983 1.0
            2.7183
            1.0005
            """,
            """
            Setiap pendekatan numerik mendekati limit teoretisnya: satu, bilangan Euler, dan satu. Makin kecil `h` makin dekat hasilnya.
            """,
            filename="limit_penting.py",
        ),
        T("""
        ## Mengapa limit penting untuk ML

        Limit adalah landasan kalkulus, dan kalkulus adalah bahasa optimasi. Turunan yang menunjukkan arah perbaikan parameter didefinisikan sebagai limit rasio perubahan. Tanpa limit, gagasan kemiringan sesaat tidak punya arti yang tepat. Kamu juga akan memakai limit untuk memahami konvergensi algoritma: apakah galat pelatihan mendekati nilai tetap atau terus berubah.

        Secara praktis kita jarang menghitung limit dengan tangan. Kita memeriksa perilaku di sekitar titik secara numerik, seperti pada contoh tadi, lalu mengonfirmasinya dengan aljabar bila perlu. Kebiasaan menguji dengan nilai dekat ini sangat berguna saat men-debug fungsi loss atau gradien yang meledak.
        """),
        E(
            "A3-01-2-ex1",
            "mudah",
            """
            Tulis fungsi `nilai_pendekatan(f, a, h)` yang mengembalikan tuple `(f(a - h), f(a + h))` dibulatkan 4 desimal.
            """,
            """
            def nilai_pendekatan(f, a, h):
                # TODO: implementasikan
                pass
            """,
            """
            assert nilai_pendekatan(lambda x: (x ** 2 - 1) / (x - 1), 1, 0.1) == (1.9, 2.1)
            assert nilai_pendekatan(lambda x: x ** 2, 2, 0.01) == (3.9601, 4.0401)
            assert nilai_pendekatan(lambda x: 2 * x + 1, 0, 0.5) == (0.0, 2.0)
            assert nilai_pendekatan(lambda x: 5, 3, 0.1) == (5, 5)
            """,
            "Hitung f di kedua sisi lalu bulatkan masing-masing.",
            """
            def nilai_pendekatan(f, a, h):
                return (round(f(a - h), 4), round(f(a + h), 4))
            """,
        ),
        E(
            "A3-01-2-ex2",
            "sedang",
            """
            Tulis fungsi `limit_ada(f, a, h=1e-6, tol=1e-3)` yang mengembalikan `True` bila selisih mutlak `f(a - h)` dan `f(a + h)` kurang dari `tol`.
            """,
            """
            import math

            def limit_ada(f, a, h=1e-6, tol=1e-3):
                # TODO: implementasikan
                pass
            """,
            """
            assert limit_ada(lambda x: x ** 2, 3) is True
            assert limit_ada(lambda x: abs(x) / x, 0) is False
            assert limit_ada(lambda x: math.sin(x) / x, 0) is True
            assert limit_ada(lambda x: 1 / x, 0) is False
            """,
            "Bandingkan nilai di kiri dan kanan titik dengan toleransi.",
            """
            import math

            def limit_ada(f, a, h=1e-6, tol=1e-3):
                return abs(f(a - h) - f(a + h)) < tol
            """,
        ),
        E(
            "A3-01-2-ex3",
            "sedang",
            """
            Tulis fungsi `limit_tak_hingga(f, n=10**6)` yang mengembalikan `f(n)` dibulatkan 4 desimal sebagai pendekatan limit saat `x` menuju tak hingga.
            """,
            """
            def limit_tak_hingga(f, n=10 ** 6):
                # TODO: implementasikan
                pass
            """,
            """
            assert limit_tak_hingga(lambda x: 1 / x) == 0.0
            assert limit_tak_hingga(lambda x: (3 * x + 1) / (x + 2)) == 3.0
            assert limit_tak_hingga(lambda x: (1 + 1 / x) ** x) == 2.7183
            assert limit_tak_hingga(lambda x: x ** 2 / (x ** 2 + 1)) == 1.0
            """,
            "Evaluasi fungsi pada n yang sangat besar lalu bulatkan.",
            """
            def limit_tak_hingga(f, n=10 ** 6):
                return round(f(n), 4)
            """,
        ),
        E(
            "A3-01-2-ex4",
            "menantang",
            """
            Tulis fungsi `limit_kiri_kanan(f, a, h=1e-7)` yang mengembalikan tuple `(kiri, kanan, ada)`. `kiri` dan `kanan` adalah `f(a - h)` dan `f(a + h)` dibulatkan 3 desimal, dan `ada` bernilai `True` bila selisih mutlaknya kurang dari 1e-3.
            """,
            """
            def limit_kiri_kanan(f, a, h=1e-7):
                # TODO: implementasikan
                pass
            """,
            """
            assert limit_kiri_kanan(lambda x: abs(x) / x, 0) == (-1.0, 1.0, False)
            assert limit_kiri_kanan(lambda x: x ** 2, 2) == (4.0, 4.0, True)
            assert limit_kiri_kanan(lambda x: 0.0 if x < 1 else 1.0, 1) == (0.0, 1.0, False)
            assert limit_kiri_kanan(lambda x: (x ** 2 - 1) / (x - 1), 1) == (2.0, 2.0, True)
            """,
            "Hitung kedua nilai, bulatkan, dan bandingkan selisih sebelum pembulatan.",
            """
            def limit_kiri_kanan(f, a, h=1e-7):
                kiri = f(a - h)
                kanan = f(a + h)
                return (round(kiri, 3), round(kanan, 3), abs(kiri - kanan) < 1e-3)
            """,
        ),
    ],
    [
        M("Menganggap limit harus sama dengan nilai fungsi di titik itu.", "Limit hanya bergantung pada perilaku di sekitar titik."),
        M("Hanya memeriksa satu sisi.", "Periksa limit kiri dan kanan."),
        M("Mensubstitusikan langsung pada bentuk 0/0.", "Sederhanakan dulu dengan pemfaktoran."),
    ],
    [
        Q("Limit menggambarkan?", ["Nilai tepat di titik", "Nilai yang didekati", "Titik maksimum", "Kemiringan"], 1, "Nilai yang didekati fungsi.", hint="Mendekat."),
        Q("Limit ada bila?", ["Limit kiri dan kanan sama", "Fungsi terdefinisi", "Fungsi naik", "Fungsi genap"], 0, "Kedua sisi harus sepakat.", hint="Dua sisi."),
        Q("lim x->tak hingga 1/x?", ["1", "0", "Tak hingga", "Tidak ada"], 1, "Pembagi raksasa membuat hasil mendekati nol.", hint="Mengecil."),
        Q("lim sin(x)/x saat x menuju 0?", ["0", "1", "Tak hingga", "Tidak ada"], 1, "Limit klasik bernilai satu.", hint="Radian."),
        Q("Bentuk 0/0 menandakan?", ["Limit nol", "Perlu disederhanakan", "Limit tak ada", "Selalu satu"], 1, "Bentuk tak tentu.", hint="Faktorkan."),
    ],
    [
        "Limit menggambarkan nilai yang didekati fungsi, bukan nilai di titik.",
        "Limit ada bila limit kiri dan kanan sama.",
        "Limit di tak hingga menjelaskan perilaku jangka panjang dan asimtot.",
        "Limit khusus mendasari bilangan e dan turunan eksponen.",
    ],
    [],
)

l3 = lesson(
    "A3-01-3",
    "Kontinuitas dan pencarian akar",
    35,
    [
        "Mendefinisikan kontinuitas dengan limit",
        "Mengenali jenis titik diskontinu",
        "Memakai teorema nilai antara untuk menjamin akar",
        "Mencari akar dengan metode bisection",
    ],
    [
        T("""
        ## Fungsi tanpa putus

        Secara intuitif fungsi **kontinu** adalah fungsi yang grafiknya bisa digambar tanpa mengangkat pensil. Definisi tepatnya memakai limit: `f` kontinu di `a` bila tiga hal terpenuhi. Pertama `f(a)` terdefinisi. Kedua limit `f(x)` saat `x` menuju `a` ada. Ketiga keduanya sama: `lim f(x) = f(a)`. Bila salah satu gagal, fungsi diskontinu di titik itu.

        Fungsi polinom, eksponen, sinus, dan kosinus kontinu di mana-mana. Logaritma kontinu di domainnya, bilangan positif. Hasil jumlah, hasil kali, dan komposisi fungsi kontinu juga kontinu. Karena itu sebagian besar fungsi yang kamu pakai dalam ML, seperti sigmoid dan ReLU, kontinu.
        """),
        T("""
        ## Jenis diskontinuitas

        Ada beberapa cara sebuah fungsi putus. **Lubang** terjadi saat limit ada tetapi nilai fungsi tidak terdefinisi atau berbeda, seperti `(x^2 - 1)/(x - 1)` di satu. Lubang bisa ditambal dengan mendefinisikan ulang nilai di titik itu. **Lompatan** terjadi saat limit kiri dan kanan berbeda, seperti fungsi tangga. **Asimtot vertikal** terjadi saat fungsi membesar tanpa batas, seperti `1/x` di nol.

        Pembedaan ini penting dalam praktik. Fungsi tangga, yang kadang dipakai sebagai aktivasi pada model klasik, memiliki lompatan sehingga kemiringannya nol di mana-mana dan tak terdefinisi di lompatan. Itulah alasan modern kita memakai pengganti yang mulus seperti sigmoid, yang berperilaku mirip tetapi bisa dioptimasi dengan kalkulus.
        """),
        C(
            """
            import math

            def lompatan(f, a, h=1e-9):
                return round(abs(f(a + h) - f(a - h)), 4)

            print(lompatan(lambda x: x ** 2, 2))
            print(lompatan(lambda x: float(math.floor(x)), 1))
            print(lompatan(lambda x: abs(x) / x, 0))
            """,
            """
            0.0
            1.0
            2.0
            """,
            """
            Fungsi kuadrat tidak melompat. Fungsi lantai melompat satu di bilangan bulat dan fungsi tanda melompat dua di nol.
            """,
            filename="kontinu_cek.py",
        ),
        T("""
        ## Teorema nilai antara

        Kontinuitas memberi jaminan kuat. **Teorema nilai antara** menyatakan bahwa bila `f` kontinu pada selang tertutup `[a, b]` dan `N` adalah nilai di antara `f(a)` dan `f(b)`, maka ada `c` dalam `[a, b]` dengan `f(c) = N`. Secara visual, kurva tanpa putus yang mulai di bawah garis dan berakhir di atasnya pasti memotong garis itu.

        Kasus khusus yang paling berguna: bila `f(a)` dan `f(b)` berlawanan tanda, ada akar, yaitu titik `c` dengan `f(c) = 0`, di antara `a` dan `b`. Teorema hanya menjamin keberadaan, bukan lokasinya. Untuk menemukannya kita butuh algoritma, dan yang paling sederhana adalah metode bisection.
        """),
        T("""
        ## Metode bisection

        Metode **bisection** membagi dua selang berulang kali. Mulai dengan `[a, b]` yang `f(a)` dan `f(b)` berlawanan tanda. Hitung titik tengah `m`. Bila `f(m)` bertanda sama dengan `f(a)`, akar ada di `[m, b]`, bila tidak di `[a, m]`. Ganti selang dengan setengah yang berisi akar dan ulangi sampai selangnya cukup sempit.

        Metode ini lambat tetapi sangat andal: ia selalu konvergen bila `f` kontinu dan tanda berlawanan, dan lebar selang mengecil setengahnya tiap langkah. Setelah `n` langkah lebarnya `(b - a) / 2^n`, sehingga jumlah langkah yang dibutuhkan dapat dihitung di muka. Akar fungsi adalah masalah dasar optimasi, karena titik minimum sering dicari sebagai akar dari turunan.
        """),
        C(
            """
            def bisect(f, a, b, tol=1e-6):
                langkah = 0
                while b - a > tol:
                    m = (a + b) / 2
                    if f(a) * f(m) <= 0:
                        b = m
                    else:
                        a = m
                    langkah += 1
                return (a + b) / 2, langkah

            akar, n = bisect(lambda x: x ** 2 - 2, 1, 2)
            print(round(akar, 4), n)
            akar2, _ = bisect(lambda x: x ** 3 - x - 2, 1, 2)
            print(round(akar2, 4))
            """,
            """
            1.4142 20
            1.5214
            """,
            """
            Akar kuadrat dua ditemukan dalam 20 langkah karena lebar awal satu dibagi dua sebanyak 20 kali sudah di bawah 1e-6. Persamaan pangkat tiga juga berakar di selang yang diberikan.
            """,
            filename="bisection.py",
        ),
        K(
            "warning",
            """
            Bisection hanya menjamin hasil bila `f(a)` dan `f(b)` berlawanan tanda dan `f` kontinu. Selalu periksa kedua syarat itu sebelum memanggil algoritmanya.
            """,
            title="Periksa syaratnya",
        ),
        T("""
        ## Kontinu belum tentu mulus

        Kontinuitas tidak sama dengan kemulusan. ReLU kontinu di nol, tetapi grafiknya bersiku di sana sehingga kemiringannya berbeda di kiri dan kanan. Sigmoid kontinu dan juga mulus, kemiringannya sama di kedua sisi nol. Perbedaan ini akan menjadi pusat pembahasan pada modul turunan: fungsi kontinu belum tentu bisa diturunkan di setiap titik.

        Contoh berikut menghitung kemiringan di kiri dan kanan nol untuk dua fungsi aktivasi. Kamu akan melihat ReLU memiliki kemiringan nol di kiri dan satu di kanan, sedangkan sigmoid memiliki kemiringan sama.
        """),
        C(
            """
            import math

            def relu(x):
                return max(0.0, x)

            def sigmoid(x):
                return 1 / (1 + math.exp(-x))

            h = 1e-6
            kanan = (relu(h) - relu(0)) / h
            kiri = (relu(0) - relu(-h)) / h
            print(round(kanan, 4), round(kiri, 4))
            kanan = (sigmoid(h) - sigmoid(0)) / h
            kiri = (sigmoid(0) - sigmoid(-h)) / h
            print(round(kanan, 4), round(kiri, 4))
            """,
            """
            1.0 0.0
            0.25 0.25
            """,
            """
            ReLU kontinu tetapi bersiku di nol karena kemiringan kiri dan kanan berbeda. Sigmoid mulus sehingga kedua kemiringan sama.
            """,
            filename="aktivasi_kontinu.py",
        ),
        T("""
        ## Peran kontinuitas dalam optimasi

        Alasan utama kontinuitas penting dalam ML adalah jaminan keberadaan nilai ekstrem. Fungsi kontinu pada selang tertutup selalu mencapai nilai maksimum dan minimum. Jadi bila fungsi loss kontinu dan parameter dibatasi pada daerah tertutup, pasti ada parameter terbaik yang bisa dicari.

        Bisection sendiri jarang dipakai pada model besar, tetapi idenya muncul di mana-mana: pencarian ambang klasifikasi, pencarian learning rate, dan penyetelan hiperparameter sering memakai strategi membagi dua selang. Pemahaman dasar ini membuat algoritma yang lebih canggih terasa wajar.
        """),
        E(
            "A3-01-3-ex1",
            "mudah",
            """
            Fungsi `f(x) = x + c` untuk `x < 1` dan `f(x) = 3` untuk `x >= 1`. Tulis fungsi `kontinu_di_1(c)` yang mengembalikan `True` bila `f` kontinu di `x = 1`, yaitu bila `1 + c` sama dengan 3 dalam toleransi 1e-9.
            """,
            """
            def kontinu_di_1(c):
                # TODO: implementasikan
                pass
            """,
            """
            assert kontinu_di_1(2) is True
            assert kontinu_di_1(0) is False
            assert kontinu_di_1(2.0) is True
            assert kontinu_di_1(2.5) is False
            """,
            "Limit kiri adalah 1 + c dan nilai fungsi adalah 3.",
            """
            def kontinu_di_1(c):
                return abs((1 + c) - 3) < 1e-9
            """,
        ),
        E(
            "A3-01-3-ex2",
            "sedang",
            """
            Tulis fungsi `bisection(f, a, b, tol=1e-6)` yang mengembalikan akar hasil metode bisection dibulatkan 4 desimal, dengan `f(a)` dan `f(b)` berlawanan tanda.
            """,
            """
            import math

            def bisection(f, a, b, tol=1e-6):
                # TODO: implementasikan
                pass
            """,
            """
            assert bisection(lambda x: x ** 2 - 2, 1, 2) == 1.4142
            assert bisection(lambda x: x ** 3 - x - 2, 1, 2) == 1.5214
            assert bisection(lambda x: x - 3, 0, 10) == 3.0
            assert bisection(math.cos, 0, 3) == 1.5708
            """,
            "Bagi dua selang dan simpan setengah yang tandanya berubah.",
            """
            import math

            def bisection(f, a, b, tol=1e-6):
                while b - a > tol:
                    m = (a + b) / 2
                    if f(a) * f(m) <= 0:
                        b = m
                    else:
                        a = m
                return round((a + b) / 2, 4)
            """,
        ),
        E(
            "A3-01-3-ex3",
            "sedang",
            """
            Tulis fungsi `jumlah_langkah(a, b, tol)` yang mengembalikan banyaknya langkah bisection terkecil `n` sehingga `(b - a) / 2**n <= tol`.
            """,
            """
            def jumlah_langkah(a, b, tol):
                # TODO: implementasikan
                pass
            """,
            """
            assert jumlah_langkah(0, 1, 0.001) == 10
            assert jumlah_langkah(1, 2, 1e-6) == 20
            assert jumlah_langkah(0, 8, 1) == 3
            assert jumlah_langkah(0, 1, 1) == 0
            """,
            "Setengahkan lebar selang berulang sampai tidak melebihi toleransi.",
            """
            def jumlah_langkah(a, b, tol):
                lebar = b - a
                n = 0
                while lebar > tol:
                    lebar /= 2
                    n += 1
                return n
            """,
        ),
        E(
            "A3-01-3-ex4",
            "menantang",
            """
            Tulis fungsi `akar_semua(f, a, b, n=1000)` yang mencari semua akar `f` pada `[a, b]`. Bagi selang menjadi `n` bagian dengan `np.linspace(a, b, n + 1)`. Bila `f` bernilai nol pada titik grid catat titik itu, dan bila tanda berubah antar dua titik berturutan, cari akar di dalamnya dengan bisection (toleransi 1e-9). Kembalikan list terurut tanpa duplikat, dibulatkan 3 desimal, dan hindari `-0.0`.
            """,
            """
            import math
            import numpy as np

            def akar_semua(f, a, b, n=1000):
                # TODO: implementasikan
                pass
            """,
            """
            assert akar_semua(lambda x: x ** 2 - 1, -3, 3) == [-1.0, 1.0]
            assert akar_semua(lambda x: x * (x - 1) * (x + 2), -3, 3) == [-2.0, 0.0, 1.0]
            assert akar_semua(lambda x: x ** 2 + 1, -3, 3) == []
            assert akar_semua(math.sin, 1, 7) == [3.142, 6.283]
            """,
            "Telusuri pasangan titik grid dan kumpulkan akar di dalam set agar duplikat hilang.",
            """
            import math
            import numpy as np

            def akar_semua(f, a, b, n=1000):
                xs = np.linspace(a, b, n + 1)
                hasil = set()
                for i in range(n + 1):
                    x0 = float(xs[i])
                    f0 = f(x0)
                    if f0 == 0:
                        hasil.add(round(x0, 3) + 0.0)
                        continue
                    if i == n:
                        break
                    x1 = float(xs[i + 1])
                    f1 = f(x1)
                    if f0 * f1 < 0:
                        lo, hi = x0, x1
                        while hi - lo > 1e-9:
                            m = (lo + hi) / 2
                            if f(lo) * f(m) <= 0:
                                hi = m
                            else:
                                lo = m
                        hasil.add(round((lo + hi) / 2, 3) + 0.0)
                return sorted(hasil)
            """,
        ),
    ],
    [
        M("Mengira fungsi kontinu pasti mulus.", "ReLU kontinu tetapi bersiku di nol."),
        M("Memakai bisection tanpa memeriksa tanda ujung selang.", "Pastikan f(a) dan f(b) berlawanan tanda."),
        M("Mengira teorema nilai antara memberi lokasi akar.", "Teorema hanya menjamin keberadaan."),
    ],
    [
        Q("Fungsi kontinu di a bila?", ["Limit sama dengan f(a)", "f naik", "f(a) = 0", "Limit tak hingga"], 0, "Limit harus sama dengan nilai fungsi.", hint="Tiga syarat."),
        Q("Fungsi tangga memiliki?", ["Lubang", "Lompatan", "Asimtot", "Tidak ada putus"], 1, "Limit kiri dan kanan berbeda.", hint="Melompat."),
        Q("Teorema nilai antara menjamin?", ["Akar unik", "Akar ada bila tanda berlawanan", "Fungsi mulus", "Nilai maksimum"], 1, "Ada c dengan f(c) = 0.", hint="Kontinu."),
        Q("Lebar selang setelah n langkah bisection?", ["(b-a)/2^n", "(b-a)n", "(b-a)^n", "b-a"], 0, "Dibagi dua tiap langkah.", hint="Setengah."),
        Q("ReLU di nol?", ["Diskontinu", "Kontinu tetapi bersiku", "Mulus", "Tak terdefinisi"], 1, "Kemiringan kiri dan kanan berbeda.", hint="Siku."),
    ],
    [
        "Fungsi kontinu bila limit sama dengan nilai fungsi.",
        "Diskontinuitas dapat berupa lubang, lompatan, atau asimtot.",
        "Teorema nilai antara menjamin akar bila tanda berlawanan.",
        "Bisection menemukan akar dengan membagi dua selang berulang.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perhitungan yang cukup jelas dalam teks.", "brief": []}

write_module(
    "A3",
    1,
    "Fungsi, limit, dan kontinuitas",
    105,
    [
        "Memahami fungsi dan fungsi yang umum dalam ML",
        "Memahami limit dan kontinuitas",
        "Mencari akar dengan bisection",
    ],
    [l1, l2, l3],
    video,
    REF,
)
