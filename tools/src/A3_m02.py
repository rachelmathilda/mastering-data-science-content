import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

l1 = lesson(
    "A3-02-1",
    "Turunan sebagai laju perubahan",
    35,
    [
        "Memahami turunan sebagai limit rasio perubahan",
        "Menafsirkan turunan sebagai kemiringan garis singgung",
        "Menghitung turunan numerik dengan selisih maju dan pusat",
        "Menghitung turunan kedua dan menafsirkan kelengkungan",
    ],
    [
        T("""
        ## Seberapa cepat berubah

        Kecepatan mobil adalah laju perubahan posisi terhadap waktu. Bila posisi berubah seratus kilometer dalam dua jam, kecepatan rata-ratanya lima puluh kilometer per jam. Namun speedometer menunjukkan kecepatan **sesaat**, yaitu laju pada satu detik tertentu. Untuk mendapatkannya kita menghitung laju rata-rata pada selang yang makin pendek dan melihat nilai yang didekati. Itulah ide turunan.

        Turunan fungsi `f` di titik `x` didefinisikan sebagai limit `(f(x + h) - f(x)) / h` saat `h` menuju nol. Pembilangnya adalah perubahan nilai fungsi dan penyebutnya perubahan masukan. Hasilnya, ditulis `f'(x)` atau `df/dx`, memberi tahu seberapa cepat `f` berubah saat `x` bergeser sedikit.
        """),
        C(
            """
            def f(x):
                return x ** 2

            print([round((f(3 + h) - f(3)) / h, 4) for h in (0.1, 0.01, 0.001)])
            print(round((f(3 + 0.1) - f(3 - 0.1)) / 0.2, 4))
            """,
            """
            [6.1, 6.01, 6.001]
            6.0
            """,
            """
            Rasio perubahan mendekati enam saat `h` mengecil, sehingga turunan `x^2` di tiga adalah enam. Selisih pusat memberi enam bahkan dengan `h` yang masih besar.
            """,
            filename="turunan_definisi.py",
        ),
        T("""
        ## Kemiringan garis singgung

        Secara geometris, `(f(x + h) - f(x)) / h` adalah kemiringan garis yang melalui dua titik pada grafik, yang disebut garis **sekan**. Saat `h` mengecil, titik kedua mendekati titik pertama dan garis sekan mendekati **garis singgung**, yaitu garis yang menyentuh kurva di satu titik dengan arah yang sama. Jadi turunan adalah kemiringan garis singgung.

        Garis singgung di titik `a` memiliki persamaan `y = f(a) + f'(a) (x - a)`. Ini adalah aproksimasi linear terbaik fungsi di dekat `a`. Dalam optimasi, pendekatan ini penting: dengan melihat kemiringan lokal kita tahu arah mana yang menurunkan fungsi, tanpa harus mengetahui bentuk seluruh fungsi.
        """),
        C(
            """
            def f(x):
                return x ** 2 + 1

            def turunan(f, x, h=1e-6):
                return (f(x + h) - f(x - h)) / (2 * h)

            a = 2.0
            m = turunan(f, a)

            def garis(x):
                return f(a) + m * (x - a)

            print(round(m, 4), f(a))
            print(round(abs(f(2.1) - garis(2.1)), 4), round(abs(f(2.01) - garis(2.01)), 4))
            """,
            """
            4.0 5.0
            0.01 0.0001
            """,
            """
            Kemiringan di dua adalah empat. Galat aproksimasi garis singgung mengecil sangat cepat, sepersepuluh jarak menghasilkan seperseratus galat.
            """,
            filename="garis_singgung.py",
        ),
        T("""
        ## Tafsir tanda turunan

        Tanda turunan memberi informasi arah. Bila `f'(x) > 0` fungsi naik di sekitar `x`, bila `f'(x) < 0` fungsi turun, dan bila `f'(x) = 0` kemiringannya datar sehingga `x` adalah **titik kritis**: kandidat puncak, lembah, atau titik datar biasa. Besarnya turunan mengukur kecuraman. Turunan besar berarti perubahan cepat.

        Inilah dasar **gradient descent**. Untuk meminimalkan loss, geser parameter melawan tanda turunan: bila turunan positif, kurangi parameter, bila negatif, tambah. Turunan nol berarti kita sudah di titik datar. Seluruh pelatihan model modern, dari regresi sederhana sampai jaringan raksasa, bertumpu pada penggunaan turunan sebagai kompas ini.
        """),
        K(
            "tip",
            """
            Untuk fungsi berparameter banyak, turunan menjadi vektor turunan parsial yang disebut gradien. Modul berikutnya membahasnya. Konsep satu variabel di sini adalah fondasinya.
            """,
            title="Menuju gradien",
        ),
        T("""
        ## Turunan numerik

        Bila rumus turunan sulit didapat, kita bisa menghampirinya secara numerik. **Selisih maju** `(f(x + h) - f(x)) / h` sederhana tetapi galatnya sebanding dengan `h`. **Selisih pusat** `(f(x + h) - f(x - h)) / (2 h)` jauh lebih akurat karena galatnya sebanding dengan `h^2`. Karena itu selisih pusat jadi pilihan standar.

        Memilih `h` adalah kompromi. Bila terlalu besar, galat pemotongan membesar. Bila terlalu kecil, dua nilai fungsi hampir sama dan selisihnya dirusak galat pembulatan floating point. Nilai sekitar `1e-5` sampai `1e-6` untuk selisih pusat biasanya baik pada presisi ganda. Turunan numerik tidak efisien untuk melatih model, tetapi sangat berguna untuk memeriksa turunan analitik, teknik yang disebut gradient check.
        """),
        C(
            """
            import math

            def turun(f, x, h=1e-6):
                return (f(x + h) - f(x - h)) / (2 * h)

            hasil = [
                turun(lambda x: x ** 3, 2),
                turun(math.sqrt, 4),
                turun(lambda x: 1 / x, 2),
                turun(math.exp, 0),
                turun(math.log, 1),
                turun(math.sin, 0),
                turun(math.cos, 0),
            ]
            print([round(v, 4) for v in hasil])
            """,
            """
            [12.0, 0.25, -0.25, 1.0, 1.0, 1.0, 0.0]
            """,
            """
            Nilai numerik cocok dengan rumus analitik: `3x^2`, `1/(2 sqrt x)`, `-1/x^2`, `e^x`, `1/x`, `cos x`, dan `-sin x` pada titik masing-masing.
            """,
            filename="aturan_pangkat.py",
        ),
        T("""
        ## Turunan kedua dan kelengkungan

        Turunan dari turunan disebut **turunan kedua**, ditulis `f''(x)`. Ia mengukur bagaimana kemiringan berubah. Bila `f''(x) > 0` kurva melengkung ke atas seperti mangkuk, dan titik kritis di sana adalah minimum lokal. Bila `f''(x) < 0` kurva melengkung ke bawah dan titik kritisnya maksimum lokal.

        Secara numerik, turunan kedua dihampiri oleh `(f(x + h) - 2 f(x) + f(x - h)) / h^2`. Dalam optimasi turunan kedua menunjukkan seberapa cepat kemiringan berubah, informasi yang dimanfaatkan metode Newton dan memengaruhi pilihan learning rate. Fungsi dengan turunan kedua besar sangat melengkung sehingga langkah gradient descent harus kecil agar tidak melompat melewati lembah.
        """),
        T("""
        ## Turunan tidak selalu ada

        Tidak semua fungsi punya turunan di setiap titik. Fungsi `|x|` kontinu di nol tetapi bersiku sehingga kemiringan kiri minus satu dan kanan satu, jadi turunan di nol tidak ada. Fungsi yang melompat atau memiliki asimtot juga tidak diturunkan di titik putusnya. Karena itu bisa dikatakan bahwa dapat diturunkan lebih kuat daripada kontinu: setiap fungsi yang dapat diturunkan pasti kontinu, tetapi tidak sebaliknya.

        Dalam praktik ML, titik tak terturunkan seperti pada ReLU di nol diatasi dengan konvensi sederhana, dan hampir tidak pernah menjadi masalah karena peluang masukan tepat nol sangat kecil.
        """),
        E(
            "A3-02-1-ex1",
            "mudah",
            """
            Tulis fungsi `turunan_maju(f, x, h)` yang mengembalikan `(f(x + h) - f(x)) / h` dibulatkan 4 desimal.
            """,
            """
            def turunan_maju(f, x, h):
                # TODO: implementasikan
                pass
            """,
            """
            assert turunan_maju(lambda x: x ** 2, 3, 0.1) == 6.1
            assert turunan_maju(lambda x: x ** 2, 3, 0.01) == 6.01
            assert turunan_maju(lambda x: 2 * x + 1, 5, 0.5) == 2.0
            assert turunan_maju(lambda x: 7, 1, 0.1) == 0.0
            """,
            "Hitung selisih nilai fungsi lalu bagi dengan h.",
            """
            def turunan_maju(f, x, h):
                return round((f(x + h) - f(x)) / h, 4)
            """,
        ),
        E(
            "A3-02-1-ex2",
            "mudah",
            """
            Tulis fungsi `turunan_pusat(f, x, h=1e-5)` yang mengembalikan selisih pusat dibulatkan 4 desimal.
            """,
            """
            import math

            def turunan_pusat(f, x, h=1e-5):
                # TODO: implementasikan
                pass
            """,
            """
            assert turunan_pusat(lambda x: x ** 2, 3) == 6.0
            assert turunan_pusat(lambda x: x ** 3, 2) == 12.0
            assert turunan_pusat(math.sin, 0) == 1.0
            assert turunan_pusat(lambda x: 5, 2) == 0.0
            """,
            "Bagi selisih f(x + h) dikurangi f(x - h) dengan dua kali h.",
            """
            import math

            def turunan_pusat(f, x, h=1e-5):
                return round((f(x + h) - f(x - h)) / (2 * h) + 0.0, 4)
            """,
        ),
        E(
            "A3-02-1-ex3",
            "sedang",
            """
            Tulis fungsi `persamaan_singgung(f, a)` yang mengembalikan tuple `(kemiringan, intersep)` dari garis singgung `y = m x + c` di titik `a`, memakai selisih pusat `h=1e-6`. Bulatkan keduanya 4 desimal dan hindari `-0.0`.
            """,
            """
            def persamaan_singgung(f, a):
                # TODO: implementasikan
                pass
            """,
            """
            assert persamaan_singgung(lambda x: x ** 2, 2) == (4.0, -4.0)
            assert persamaan_singgung(lambda x: x ** 3, 1) == (3.0, -2.0)
            assert persamaan_singgung(lambda x: 2 * x + 1, 5) == (2.0, 1.0)
            assert persamaan_singgung(lambda x: x ** 2 + 1, 0) == (0.0, 1.0)
            """,
            "Intersep sama dengan f(a) dikurangi kemiringan kali a.",
            """
            def persamaan_singgung(f, a):
                h = 1e-6
                m = (f(a + h) - f(a - h)) / (2 * h)
                c = f(a) - m * a
                return (round(m, 4) + 0.0, round(c, 4) + 0.0)
            """,
        ),
        E(
            "A3-02-1-ex4",
            "menantang",
            """
            Tulis fungsi `turunan_kedua(f, x, h=1e-3)` yang mengembalikan `(f(x + h) - 2 f(x) + f(x - h)) / h^2` dibulatkan 3 desimal. Hindari `-0.0`.
            """,
            """
            import math

            def turunan_kedua(f, x, h=1e-3):
                # TODO: implementasikan
                pass
            """,
            """
            assert turunan_kedua(lambda x: x ** 3, 2) == 12.0
            assert turunan_kedua(math.sin, math.pi / 2) == -1.0
            assert turunan_kedua(lambda x: x ** 2, 5) == 2.0
            assert turunan_kedua(lambda x: x, 4) == 0.0
            """,
            "Gunakan tiga nilai fungsi: di x tambah h, di x, dan di x kurang h.",
            """
            import math

            def turunan_kedua(f, x, h=1e-3):
                return round((f(x + h) - 2 * f(x) + f(x - h)) / (h * h), 3) + 0.0
            """,
        ),
    ],
    [
        M("Menganggap turunan hanyalah rumus yang dihafal.", "Turunan adalah limit laju perubahan."),
        M("Memakai h terlalu kecil pada turunan numerik.", "Pakai sekitar 1e-5 sampai 1e-6 dengan selisih pusat."),
        M("Menyamakan turunan nol dengan minimum.", "Titik kritis bisa maksimum atau titik datar."),
    ],
    [
        Q("Turunan adalah?", ["Nilai fungsi", "Limit laju perubahan", "Integral", "Rata-rata"], 1, "Limit rasio perubahan.", hint="Laju."),
        Q("Turunan geometrisnya?", ["Luas", "Kemiringan garis singgung", "Panjang kurva", "Titik potong"], 1, "Kemiringan di satu titik.", hint="Singgung."),
        Q("Turunan positif berarti?", ["Fungsi turun", "Fungsi naik", "Fungsi datar", "Fungsi tak ada"], 1, "Fungsi naik.", hint="Arah."),
        Q("Selisih pusat lebih akurat karena?", ["Galat sebanding h kuadrat", "Memakai satu titik", "Tanpa pembagian", "Tanpa fungsi"], 0, "Galatnya orde dua.", hint="Simetris."),
        Q("Turunan kedua positif berarti?", ["Melengkung ke bawah", "Melengkung ke atas", "Garis lurus", "Tak terdefinisi"], 1, "Seperti mangkuk.", hint="Kelengkungan."),
    ],
    [
        "Turunan adalah limit laju perubahan dan kemiringan garis singgung.",
        "Tanda turunan menunjukkan fungsi naik atau turun.",
        "Selisih pusat adalah turunan numerik yang lebih akurat.",
        "Turunan kedua mengukur kelengkungan.",
    ],
    [],
)

l2 = lesson(
    "A3-02-2",
    "Aturan turunan",
    35,
    [
        "Menghitung turunan dengan aturan pangkat, jumlah, dan konstanta",
        "Memakai aturan kali dan aturan bagi",
        "Memakai aturan rantai untuk komposisi",
        "Menghafal turunan fungsi dasar eksponen, log, dan trigonometri",
    ],
    [
        T("""
        ## Dari definisi ke aturan

        Menghitung limit tiap kali tentu melelahkan. Untungnya ada aturan yang membuat turunan hampir mekanis. **Aturan konstanta**: turunan konstanta nol. **Aturan pangkat**: turunan `x^n` adalah `n x^(n-1)`. **Aturan kelipatan**: konstanta dapat dikeluarkan. **Aturan jumlah**: turunan jumlah adalah jumlah turunan. Dengan empat aturan ini polinom apa pun dapat diturunkan suku demi suku.

        Contoh: turunan `3x^4 - 2x^2 + 5x - 7` adalah `12x^3 - 4x + 5`. Aturan pangkat juga berlaku untuk pangkat pecahan dan negatif: `sqrt(x) = x^(1/2)` memiliki turunan `1/2 x^(-1/2)`, dan `1/x = x^-1` memiliki turunan `-x^-2`. Satu aturan sederhana mencakup sangat banyak kasus.
        """),
        T("""
        ## Turunan fungsi dasar

        Beberapa turunan perlu dihafal. Turunan `e^x` adalah `e^x` itu sendiri: fungsi yang laju pertumbuhannya sama dengan nilainya, itulah mengapa eksponen muncul di mana-mana dalam pertumbuhan alami. Turunan `ln x` adalah `1/x`. Turunan `sin x` adalah `cos x` dan turunan `cos x` adalah `-sin x`, dengan `x` dalam radian.

        Hafalan ini ditambah aturan di bawah cukup untuk menurunkan hampir semua fungsi yang kamu temui dalam ML. Selalu periksa jawaban dengan turunan numerik pada satu dua titik. Kebiasaan ini menangkap kesalahan aljabar sebelum menjadi bug di model.
        """),
        T("""
        ## Aturan kali dan bagi

        Turunan hasil kali bukan hasil kali turunan. **Aturan kali**: `(f g)' = f' g + f g'`. Ingat sebagai: turunkan yang pertama dikali yang kedua tetap, ditambah yang pertama tetap dikali turunan kedua. Intuisinya: luas persegi panjang `f x g` berubah karena kedua sisinya berubah, dan tiap sisi menyumbang sendiri.

        **Aturan bagi**: `(f / g)' = (f' g - f g') / g^2`. Tanda minus dan urutan suku penting, jadi hati-hati. Pada banyak kasus kamu bisa menulis ulang pembagian sebagai perkalian dengan pangkat negatif dan memakai aturan kali serta rantai, yang sering lebih sedikit salah.
        """),
        C(
            """
            import math

            def turun(f, x, h=1e-6):
                return (f(x + h) - f(x - h)) / (2 * h)

            f1 = lambda x: x ** 2 * math.sin(x)
            a1 = 2 * 1 * math.sin(1) + 1 ** 2 * math.cos(1)
            print(round(a1, 4), round(turun(f1, 1), 4))

            f2 = lambda x: math.sin(x) / x
            x0 = math.pi / 2
            a2 = (x0 * math.cos(x0) - math.sin(x0)) / x0 ** 2
            print(round(a2, 4), round(turun(f2, x0), 4))
            """,
            """
            2.2232 2.2232
            -0.4053 -0.4053
            """,
            """
            Rumus analitik aturan kali dan bagi cocok dengan turunan numerik pada kedua contoh.
            """,
            filename="aturan_kali_bagi.py",
        ),
        T("""
        ## Aturan rantai

        Aturan paling penting untuk ML adalah **aturan rantai**, untuk komposisi fungsi. Bila `h(x) = f(g(x))`, maka `h'(x) = f'(g(x)) g'(x)`. Turunkan fungsi luar di titik fungsi dalam, lalu kalikan dengan turunan fungsi dalam. Intuisinya, laju `f` terhadap `x` adalah laju `f` terhadap `g` dikali laju `g` terhadap `x`: faktor-faktor perubahan saling mengalikan.

        Contoh: `h(x) = (3x + 1)^5`. Fungsi luar `u^5` memiliki turunan `5u^4`, fungsi dalam `3x + 1` memiliki turunan tiga, sehingga `h'(x) = 15 (3x + 1)^4`. Contoh lain: `e^(-x^2)` memiliki turunan `-2x e^(-x^2)`. Untuk rantai panjang, kalikan turunan tiap mata rantai dari luar ke dalam.
        """),
        C(
            """
            import math

            def turun(f, x, h=1e-6):
                return (f(x + h) - f(x - h)) / (2 * h)

            a1 = 15 * (3 * 1 + 1) ** 4
            n1 = turun(lambda x: (3 * x + 1) ** 5, 1, 1e-5)
            print(a1, round(n1, 2))
            a2 = -2 * 1 * math.exp(-1)
            n2 = turun(lambda x: math.exp(-x ** 2), 1)
            print(round(a2, 4), round(n2, 4))
            """,
            """
            3840 3840.0
            -0.7358 -0.7358
            """,
            """
            Aturan rantai menghasilkan 3840 untuk pangkat lima dan sekitar minus 0,7358 untuk eksponen gaussian, sesuai hitungan numerik.
            """,
            filename="aturan_rantai.py",
        ),
        K(
            "warning",
            """
            Kesalahan paling umum dengan aturan rantai adalah lupa mengalikan turunan fungsi dalam. Turunan `sin(3x)` adalah `3 cos(3x)`, bukan `cos(3x)`.
            """,
            title="Jangan lupa faktor dalam",
        ),
        T("""
        ## Memeriksa dengan turunan kedua dan numerik

        Setelah menurunkan sekali, kamu dapat menurunkan lagi. Turunan kedua polinom diperoleh dengan menerapkan aturan pangkat dua kali, misalnya turunan kedua `x^3` adalah `6x`. Turunan kedua bernilai besar menandakan fungsi sangat melengkung, dan pada optimasi hal ini memengaruhi ukuran langkah yang aman.

        Untuk memverifikasi hasil, bandingkan dengan turunan numerik. Kedua hitungan harus sama sampai beberapa desimal. Bila tidak, ada kesalahan aljabar atau kesalahan kode. Pemeriksaan ini adalah praktik baku yang disebut gradient check, dan nanti akan kamu pakai pada model yang gradiennya ditulis tangan.
        """),
        C(
            """
            import math

            def kedua(f, x, h=1e-3):
                return (f(x + h) - 2 * f(x) + f(x - h)) / h ** 2

            print([round(kedua(lambda x: x ** 3, 2), 3), round(kedua(math.sin, math.pi / 2), 3)])
            print(6 * 2, round(-math.sin(math.pi / 2), 3))
            """,
            """
            [12.0, -1.0]
            12 -1.0
            """,
            """
            Turunan kedua numerik cocok dengan rumus `6x` untuk `x^3` dan `-sin x` untuk sinus.
            """,
            filename="turunan_tabel.py",
        ),
        T("""
        ## Latihan berpikir dengan aturan

        Cobalah menurunkan `f(x) = x e^(2x)` sebelum membaca lanjutan. Ini hasil kali `x` dan `e^(2x)`. Aturan kali memberi `1 * e^(2x) + x * (e^(2x) * 2)`, karena turunan `e^(2x)` memakai aturan rantai dengan faktor dua. Hasilnya `e^(2x) (1 + 2x)`. Langkah demi langkah seperti ini membuat soal yang tampak rumit menjadi pekerjaan mekanis.

        Kebiasaan baik: tulis dulu struktur fungsi, apakah penjumlahan, perkalian, pembagian, atau komposisi, lalu terapkan aturan yang sesuai dari luar ke dalam. Setelah itu verifikasi numerik di satu titik. Dua pemeriksaan ini menyelamatkanmu dari sebagian besar kesalahan.
        """),
        E(
            "A3-02-2-ex1",
            "mudah",
            """
            Tulis fungsi `turunan_pangkat(n, x)` yang mengembalikan turunan `x^n` di titik `x`, yaitu `n * x ** (n - 1)`.
            """,
            """
            def turunan_pangkat(n, x):
                # TODO: implementasikan
                pass
            """,
            """
            assert turunan_pangkat(3, 2) == 12
            assert turunan_pangkat(2, 5) == 10
            assert turunan_pangkat(0, 7) == 0
            assert turunan_pangkat(-1, 2) == -0.25
            """,
            "Terapkan aturan pangkat langsung.",
            """
            def turunan_pangkat(n, x):
                return n * x ** (n - 1)
            """,
        ),
        E(
            "A3-02-2-ex2",
            "sedang",
            """
            Tulis fungsi `turunan_polinom(koef)` yang menerima koefisien polinom dari pangkat tertinggi ke terendah dan mengembalikan koefisien turunannya dalam urutan yang sama. Untuk polinom konstan kembalikan `[0]`.
            """,
            """
            def turunan_polinom(koef):
                # TODO: implementasikan
                pass
            """,
            """
            assert turunan_polinom([1, 0, 1]) == [2, 0]
            assert turunan_polinom([3, 2, 1]) == [6, 2]
            assert turunan_polinom([5]) == [0]
            assert turunan_polinom([1, -3, 2, 4]) == [3, -6, 2]
            """,
            "Kalikan tiap koefisien dengan pangkatnya lalu buang suku konstan.",
            """
            def turunan_polinom(koef):
                n = len(koef) - 1
                if n == 0:
                    return [0]
                return [c * (n - i) for i, c in enumerate(koef[:-1])]
            """,
        ),
        E(
            "A3-02-2-ex3",
            "sedang",
            """
            Tulis fungsi `rantai(df, g, dg, x)` yang mengembalikan turunan komposisi `f(g(x))` di `x` dengan aturan rantai `df(g(x)) * dg(x)`, dibulatkan 4 desimal. Hindari `-0.0`.
            """,
            """
            import math

            def rantai(df, g, dg, x):
                # TODO: implementasikan
                pass
            """,
            """
            assert rantai(lambda u: 2 * u, lambda x: 3 * x + 1, lambda x: 3, 1) == 24.0
            assert rantai(math.cos, lambda x: x ** 2, lambda x: 2 * x, 0) == 0.0
            assert rantai(math.exp, lambda x: -x ** 2, lambda x: -2 * x, 1) == -0.7358
            assert rantai(lambda u: 1 / u, lambda x: x ** 2 + 1, lambda x: 2 * x, 1) == 1.0
            """,
            "Hitung turunan fungsi luar di g(x) lalu kalikan dengan turunan fungsi dalam.",
            """
            import math

            def rantai(df, g, dg, x):
                return round(df(g(x)) * dg(x), 4) + 0.0
            """,
        ),
        E(
            "A3-02-2-ex4",
            "menantang",
            """
            Tulis fungsi `turunan_dual(f, x)` yang menghitung turunan `f` di `x` dengan diferensiasi otomatis mode maju memakai bilangan dual. Definisikan kelas `Dual` dengan nilai dan turunan, yang mendukung `+`, `-`, `*`, `/` (termasuk dengan bilangan biasa di kiri atau kanan) dan `** n` untuk `n` bulat. Panggil `f(Dual(x, 1.0))` dan kembalikan turunannya dibulatkan 4 desimal. Bila `f` mengembalikan bilangan biasa kembalikan `0.0`.
            """,
            """
            def turunan_dual(f, x):
                # TODO: definisikan kelas Dual dan implementasikan
                pass
            """,
            """
            assert turunan_dual(lambda x: x * x * x + 2 * x, 2) == 14.0
            assert turunan_dual(lambda x: (x + 1) * (x - 1), 3) == 6.0
            assert turunan_dual(lambda x: x / (x + 1), 1) == 0.25
            assert turunan_dual(lambda x: x ** 3, 2) == 12.0
            assert turunan_dual(lambda x: 3, 5) == 0.0
            assert turunan_dual(lambda x: 1 / x, 2) == -0.25
            """,
            "Simpan pasangan nilai dan turunan lalu terapkan aturan jumlah, kali, bagi, dan pangkat pada setiap operasi.",
            """
            class Dual:
                def __init__(self, v, d=0.0):
                    self.v = v
                    self.d = d

                def _w(self, o):
                    return o if isinstance(o, Dual) else Dual(o, 0.0)

                def __add__(self, o):
                    o = self._w(o)
                    return Dual(self.v + o.v, self.d + o.d)

                __radd__ = __add__

                def __sub__(self, o):
                    o = self._w(o)
                    return Dual(self.v - o.v, self.d - o.d)

                def __rsub__(self, o):
                    return self._w(o) - self

                def __mul__(self, o):
                    o = self._w(o)
                    return Dual(self.v * o.v, self.d * o.v + self.v * o.d)

                __rmul__ = __mul__

                def __truediv__(self, o):
                    o = self._w(o)
                    return Dual(self.v / o.v, (self.d * o.v - self.v * o.d) / o.v ** 2)

                def __rtruediv__(self, o):
                    return self._w(o) / self

                def __pow__(self, n):
                    return Dual(self.v ** n, n * self.v ** (n - 1) * self.d)

            def turunan_dual(f, x):
                r = f(Dual(x, 1.0))
                if isinstance(r, Dual):
                    return round(float(r.d), 4) + 0.0
                return 0.0
            """,
        ),
    ],
    [
        M("Menurunkan hasil kali sebagai hasil kali turunan.", "Pakai aturan kali: f' g + f g'."),
        M("Lupa mengalikan turunan fungsi dalam pada aturan rantai.", "Kalikan dengan g'(x)."),
        M("Salah tanda pada aturan bagi.", "Pembilangnya f' g - f g' dan penyebutnya g kuadrat."),
    ],
    [
        Q("Turunan x^n?", ["n x^(n-1)", "x^(n+1)", "n x", "x^n"], 0, "Aturan pangkat.", hint="Pangkat turun satu."),
        Q("Turunan e^x?", ["x e^x", "e^x", "e^(x-1)", "1"], 1, "e^x tetap e^x.", hint="Dirinya sendiri."),
        Q("Aturan kali?", ["f' g'", "f' g + f g'", "f g", "f' / g'"], 1, "Turunkan satu per satu.", hint="Dua suku."),
        Q("Aturan rantai untuk f(g(x))?", ["f'(x) g'(x)", "f'(g(x)) g'(x)", "f(g'(x))", "f'(g'(x))"], 1, "Luar di dalam dikali turunan dalam.", hint="Rantai."),
        Q("Turunan ln x?", ["ln x", "1/x", "x", "e^x"], 1, "Satu per x.", hint="Kebalikan."),
    ],
    [
        "Aturan pangkat, jumlah, kali, bagi, dan rantai membuat turunan mekanis.",
        "Hafal turunan e^x, ln x, sin x, dan cos x.",
        "Aturan rantai adalah dasar backpropagation.",
        "Periksa hasil dengan turunan numerik.",
    ],
    [],
)

l3 = lesson(
    "A3-02-3",
    "Turunan dalam ML: aktivasi, neuron, dan gradient check",
    35,
    [
        "Menurunkan sigmoid, tanh, dan ReLU",
        "Menerapkan aturan rantai pada satu neuron",
        "Memverifikasi gradien dengan turunan numerik",
        "Menghitung gradien numerik fungsi dengan banyak parameter",
    ],
    [
        T("""
        ## Turunan fungsi aktivasi

        Fungsi aktivasi diturunkan di setiap langkah pelatihan, sehingga turunannya harus kamu kenal. Sigmoid `s(x) = 1 / (1 + e^-x)` memiliki turunan yang indah: `s'(x) = s(x) (1 - s(x))`. Turunan dihitung dari keluarannya sendiri, sehingga efisien. Nilai maksimumnya 0,25 di `x = 0` dan mengecil menuju nol di kedua ujung.

        Tanh memiliki turunan `1 - tanh(x)^2` dengan maksimum satu di nol. ReLU memiliki turunan nol untuk `x < 0` dan satu untuk `x > 0`, sedangkan di nol turunannya tidak terdefinisi dan praktiknya dipilih nol atau satu. Perbedaan turunan inilah yang membuat sigmoid mudah mengalami gradien menghilang pada jaringan dalam, sedangkan ReLU tidak untuk masukan positif.
        """),
        C(
            """
            import numpy as np

            def sigmoid(x):
                return 1 / (1 + np.exp(-x))

            def d_sigmoid(x):
                s = sigmoid(x)
                return s * (1 - s)

            def d_tanh(x):
                return 1 - np.tanh(x) ** 2

            def d_relu(x):
                return (x > 0).astype(float)

            def numerik(f, x, h=1e-6):
                return (f(x + h) - f(x - h)) / (2 * h)

            x = np.array([-2.0, 0.0, 2.0])
            print(d_sigmoid(x).round(4).tolist())
            print(d_tanh(np.array([-1.0, 0.0, 1.0])).round(4).tolist())
            print(d_relu(np.array([-1.0, 2.0])).tolist())
            print(np.allclose(d_sigmoid(x), numerik(sigmoid, x)), np.allclose(d_tanh(x), numerik(np.tanh, x)))
            """,
            """
            [0.105, 0.25, 0.105]
            [0.42, 1.0, 0.42]
            [0.0, 1.0]
            True True
            """,
            """
            Turunan sigmoid maksimal 0,25 di nol dan menyusut di ujung. Rumus analitik cocok dengan turunan numerik.
            """,
            filename="turunan_aktivasi.py",
        ),
        T("""
        ## Satu neuron dan aturan rantai

        Neuron paling sederhana menghitung `z = w x + b`, lalu `y = s(z)` dengan sigmoid, lalu loss kuadrat `L = (y - t)^2` terhadap target `t`. Ini rantai tiga fungsi: dari parameter ke `z`, dari `z` ke `y`, dari `y` ke `L`. Untuk mendapat `dL/dw` kita kalikan turunan tiap mata rantai.

        Dengan aturan rantai: `dL/dw = dL/dy * dy/dz * dz/dw`. Faktor pertama `2 (y - t)`, kedua `y (1 - y)`, ketiga `x`. Untuk bias, faktor ketiga `dz/db` sama dengan satu. Perhitungan ini persis yang dilakukan backpropagation, hanya pada skala jutaan parameter dan dengan bantuan komputer untuk mengurus pembukuannya.
        """),
        C(
            """
            import math

            def sigmoid(z):
                return 1 / (1 + math.exp(-z))

            w, b, x, t = 0.5, 0.1, 2.0, 1.0
            z = w * x + b
            y = sigmoid(z)
            dL_dy = 2 * (y - t)
            dy_dz = y * (1 - y)
            dz_dw = x
            dz_db = 1.0
            print(round(z, 4), round(y, 4), round((y - t) ** 2, 4))
            print(round(dL_dy * dy_dz * dz_dw, 4), round(dL_dy * dy_dz * dz_db, 4))
            """,
            """
            1.1 0.7503 0.0624
            -0.1872 -0.0936
            """,
            """
            Kedua turunan negatif: menaikkan `w` dan `b` akan menurunkan loss karena prediksi masih di bawah target.
            """,
            filename="neuron_rantai.py",
        ),
        T("""
        ## Gradient check

        Menulis turunan tangan rawan salah, dan bug pada gradien sering tidak menimbulkan galat, hanya model yang melatih buruk tanpa sebab jelas. Karena itu praktisi memakai **gradient check**: bandingkan gradien analitik dengan gradien numerik di beberapa titik. Bila selisih relatifnya sangat kecil, sekitar `1e-6` atau kurang, gradien kemungkinan benar.

        Selisih relatif umum dihitung sebagai norma selisih dibagi jumlah norma kedua vektor. Ukuran relatif lebih adil daripada selisih mutlak karena memperhitungkan besarnya gradien. Lakukan gradient check pada ukuran masalah kecil karena gradien numerik membutuhkan dua evaluasi fungsi per parameter, terlalu mahal untuk model besar.
        """),
        K(
            "tip",
            """
            Nonaktifkan dropout dan sumber keacakan lain saat gradient check. Bila fungsi berubah antar evaluasi, perbandingan numerik tidak bermakna.
            """,
            title="Hilangkan keacakan",
        ),
        C(
            """
            import numpy as np

            def sigmoid(z):
                return 1 / (1 + np.exp(-z))

            def loss(p, x=2.0, t=1.0):
                return (sigmoid(p[0] * x + p[1]) - t) ** 2

            def grad_analitik(p, x=2.0, t=1.0):
                y = sigmoid(p[0] * x + p[1])
                d = 2 * (y - t) * y * (1 - y)
                return np.array([d * x, d])

            def grad_numerik(f, p, h=1e-6):
                g = np.zeros_like(p)
                for i in range(len(p)):
                    e = np.zeros_like(p)
                    e[i] = h
                    g[i] = (f(p + e) - f(p - e)) / (2 * h)
                return g

            p = np.array([0.5, 0.1])
            ga = grad_analitik(p)
            gn = grad_numerik(loss, p)
            print(ga.round(4).tolist(), gn.round(4).tolist())
            rel = np.linalg.norm(ga - gn) / (np.linalg.norm(ga) + np.linalg.norm(gn))
            print(bool(rel < 1e-6))
            salah = ga * 1.1
            rel2 = np.linalg.norm(salah - gn) / (np.linalg.norm(salah) + np.linalg.norm(gn))
            print(bool(rel2 < 1e-6))
            """,
            """
            [-0.1872, -0.0936] [-0.1872, -0.0936]
            True
            False
            """,
            """
            Gradien analitik lolos pengecekan, sedangkan gradien yang salah sepuluh persen gagal. Gradient check mampu menangkap kesalahan kecil sekalipun.
            """,
            filename="gradient_check.py",
        ),
        T("""
        ## Dari satu neuron ke jaringan

        Perhitungan satu neuron tadi bisa diperluas. Jaringan berlapis hanyalah rantai yang lebih panjang: loss bergantung pada keluaran lapisan akhir, yang bergantung pada lapisan sebelumnya, dan seterusnya. Backpropagation menghitung turunan dari belakang ke depan dan menyimpan hasil antara agar tidak dihitung ulang, sehingga efisien.

        Pustaka seperti PyTorch dan TensorFlow melakukan ini otomatis dengan diferensiasi otomatis, versi canggih dari bilangan dual yang kamu bangun pada latihan sebelumnya. Meski begitu memahami aturan rantai tetap penting untuk men-debug gradien yang meledak atau menghilang dan untuk merancang fungsi loss kustom.
        """),
        T("""
        ## Gradien menghilang dan meledak

        Aturan rantai mengalikan banyak faktor turunan sepanjang lapisan. Bila faktor-faktor itu kecil, misalnya turunan sigmoid yang paling besar 0,25, hasil kali dari banyak lapisan menyusut secara eksponensial dan gradien di lapisan awal hampir nol. Itulah **gradien menghilang**: lapisan awal hampir tidak belajar. Sebaliknya bila faktornya besar, hasil kali meledak dan pelatihan menjadi tidak stabil.

        Karena alasan itu praktisi memilih aktivasi seperti ReLU yang turunannya satu pada daerah aktif, menginisialisasi bobot dengan skala yang tepat, dan memakai normalisasi lapisan serta koneksi residual. Semua teknik ini pada dasarnya menjaga hasil kali turunan berada pada skala yang wajar.
        """),
        T("""
        ## Memilih fungsi loss yang baik untuk turunan

        Pilihan fungsi loss memengaruhi gradien. Pada neuron sigmoid dengan loss kuadrat, gradien memuat faktor turunan sigmoid, sehingga bila neuron sangat salah tetapi jenuh, gradiennya kecil dan belajar lambat. Pada loss cross-entropy, faktor itu saling meniadakan dan gradien menjadi sekadar selisih prediksi dan target, yang tetap besar saat prediksi sangat salah.

        Itulah salah satu alasan klasifikasi hampir selalu memakai cross-entropy, bukan galat kuadrat. Pelajaran ini menunjukkan bahwa turunan bukan hanya alat hitung. Ia membantu kita merancang masalah optimasi yang mudah dipecahkan.
        """),
        T("""
        ## Merangkum modul

        Modul ini membawamu dari definisi turunan sebagai limit sampai penerapannya pada neuron. Kamu belajar bahwa turunan adalah kemiringan dan laju perubahan, bahwa aturan pangkat, kali, bagi, dan rantai membuat penghitungan mekanis, dan bahwa aturan rantai adalah mesin di balik backpropagation.

        Kamu juga memiliki alat verifikasi yang kuat: turunan numerik dan gradient check. Gunakan keduanya setiap kali menulis gradien sendiri. Modul berikutnya memperluas semua ini ke fungsi dengan banyak variabel, tempat turunan menjadi gradien dan gradient descent mulai bekerja pada banyak parameter sekaligus.
        """),
        E(
            "A3-02-3-ex1",
            "mudah",
            """
            Tulis fungsi `turunan_sigmoid(x)` yang mengembalikan `s(x) * (1 - s(x))` dibulatkan 4 desimal, dengan `s` adalah sigmoid, memakai `math.exp`. Gunakan versi stabil untuk masukan sangat negatif.
            """,
            """
            import math

            def turunan_sigmoid(x):
                # TODO: implementasikan
                pass
            """,
            """
            assert turunan_sigmoid(0) == 0.25
            assert turunan_sigmoid(2) == 0.105
            assert turunan_sigmoid(-2) == 0.105
            assert turunan_sigmoid(20) == 0.0
            assert turunan_sigmoid(-1000) == 0.0
            """,
            "Hitung sigmoid dengan cabang untuk masukan negatif lalu kalikan dengan satu dikurangi nilainya.",
            """
            import math

            def turunan_sigmoid(x):
                if x >= 0:
                    s = 1 / (1 + math.exp(-x))
                else:
                    z = math.exp(x)
                    s = z / (1 + z)
                return round(s * (1 - s), 4)
            """,
        ),
        E(
            "A3-02-3-ex2",
            "mudah",
            """
            Tulis fungsi `turunan_tanh(x)` yang mengembalikan `1 - tanh(x)^2` dibulatkan 4 desimal.
            """,
            """
            import math

            def turunan_tanh(x):
                # TODO: implementasikan
                pass
            """,
            """
            assert turunan_tanh(0) == 1.0
            assert turunan_tanh(1) == 0.42
            assert turunan_tanh(-1) == 0.42
            assert turunan_tanh(10) == 0.0
            """,
            "Pakai math.tanh lalu kuadratkan.",
            """
            import math

            def turunan_tanh(x):
                return round(1 - math.tanh(x) ** 2, 4)
            """,
        ),
        E(
            "A3-02-3-ex3",
            "sedang",
            """
            Tulis fungsi `gradien_neuron(w, b, x, t)` yang mengembalikan tuple `(dL/dw, dL/db)` untuk neuron `y = sigmoid(w x + b)` dengan loss `(y - t)^2`, dibulatkan 4 desimal. Hindari `-0.0`.
            """,
            """
            import math

            def gradien_neuron(w, b, x, t):
                # TODO: implementasikan
                pass
            """,
            """
            assert gradien_neuron(0.5, 0.1, 2, 1) == (-0.1872, -0.0936)
            assert gradien_neuron(0, 0, 1, 1) == (-0.25, -0.25)
            assert gradien_neuron(0, 0, 1, 0) == (0.25, 0.25)
            assert gradien_neuron(1, -1, 3, 0) == (0.5549, 0.185)
            assert gradien_neuron(2, 0, 0, 1) == (0.0, -0.25)
            """,
            "Kalikan tiga faktor rantai: dua kali selisih, turunan sigmoid, dan turunan z.",
            """
            import math

            def gradien_neuron(w, b, x, t):
                y = 1 / (1 + math.exp(-(w * x + b)))
                d = 2 * (y - t) * y * (1 - y)
                return (round(d * x, 4) + 0.0, round(d, 4) + 0.0)
            """,
        ),
        E(
            "A3-02-3-ex4",
            "menantang",
            """
            Tulis fungsi `gradien_numerik(f, titik, h=1e-5)` yang menerima fungsi `f` dengan satu argumen list dan list `titik`, lalu mengembalikan list turunan parsial dengan selisih pusat, dibulatkan 4 desimal. Hindari `-0.0`.
            """,
            """
            def gradien_numerik(f, titik, h=1e-5):
                # TODO: implementasikan
                pass
            """,
            """
            assert gradien_numerik(lambda p: p[0] ** 2 + 3 * p[1], [1, 2]) == [2.0, 3.0]
            assert gradien_numerik(lambda p: p[0] * p[1], [3, 4]) == [4.0, 3.0]
            assert gradien_numerik(lambda p: sum(v * v for v in p), [1, 2, 3]) == [2.0, 4.0, 6.0]
            assert gradien_numerik(lambda p: 5, [1, 1]) == [0.0, 0.0]
            """,
            "Geser satu koordinat saja maju dan mundur lalu ambil selisih pusat.",
            """
            def gradien_numerik(f, titik, h=1e-5):
                hasil = []
                for i in range(len(titik)):
                    maju = list(titik)
                    mundur = list(titik)
                    maju[i] += h
                    mundur[i] -= h
                    hasil.append(round((f(maju) - f(mundur)) / (2 * h), 4) + 0.0)
                return hasil
            """,
        ),
    ],
    [
        M("Menghitung gradien tanpa pernah memeriksanya.", "Lakukan gradient check pada kasus kecil."),
        M("Mengira turunan ReLU di nol terdefinisi.", "Praktiknya dipilih nol atau satu."),
        M("Melupakan faktor turunan sigmoid pada rantai.", "Kalikan dengan y(1 - y)."),
    ],
    [
        Q("Turunan sigmoid?", ["s(1-s)", "s", "1-s", "s^2"], 0, "Dihitung dari keluarannya.", hint="Maksimum 0,25."),
        Q("Turunan ReLU untuk x positif?", ["0", "1", "x", "Tak ada"], 1, "Kemiringan satu.", hint="Garis lurus."),
        Q("dL/dw pada neuron memakai?", ["Aturan rantai", "Aturan kali saja", "Integral", "Limit saja"], 0, "Kalikan turunan tiap mata rantai.", hint="Backprop."),
        Q("Tujuan gradient check?", ["Mempercepat model", "Memverifikasi gradien analitik", "Menambah data", "Mengurangi parameter"], 1, "Bandingkan dengan numerik.", hint="Debug."),
        Q("Mengapa gradient check hanya untuk model kecil?", ["Tidak akurat", "Butuh dua evaluasi per parameter", "Butuh label", "Tidak bisa dijalankan"], 1, "Biayanya besar.", hint="Per parameter."),
    ],
    [
        "Turunan sigmoid dihitung dari keluarannya dan maksimal 0,25.",
        "Aturan rantai menghitung gradien neuron dari loss ke parameter.",
        "Gradient check membandingkan gradien analitik dan numerik.",
        "Diferensiasi otomatis mengotomatisasi aturan rantai.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perhitungan yang cukup jelas dalam teks.", "brief": []}

write_module(
    "A3",
    2,
    "Turunan dan aturan dasarnya",
    105,
    [
        "Memahami turunan sebagai laju perubahan",
        "Memakai aturan turunan termasuk aturan rantai",
        "Menerapkan turunan pada neuron dan gradient check",
    ],
    [l1, l2, l3],
    video,
    REF,
)
