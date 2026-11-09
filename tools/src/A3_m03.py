import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

l1 = lesson(
    "A3-03-1",
    "Fungsi banyak variabel dan turunan parsial",
    35,
    [
        "Memahami fungsi dengan dua atau lebih masukan dan visualisasi kontur",
        "Menghitung turunan parsial dengan menahan variabel lain tetap",
        "Menyusun gradien sebagai vektor turunan parsial",
        "Memakai turunan parsial numerik untuk memeriksa hasil",
    ],
    [
        T("""
        ## Lebih dari satu masukan

        Pada modul sebelumnya fungsi hanya punya satu masukan. Model ML hampir selalu punya banyak parameter: regresi dengan sepuluh fitur punya sebelas parameter, jaringan saraf punya jutaan. Fungsi loss adalah fungsi dari semua parameter itu sekaligus, `L(w1, w2, ..., wn)`. Untuk mengoptimasinya kita perlu memperluas turunan ke fungsi banyak variabel.

        Fungsi dua variabel `f(x, y)` memetakan pasangan bilangan ke satu bilangan. Grafiknya berupa permukaan di ruang tiga dimensi: `x` dan `y` menentukan posisi di lantai, dan `f` menentukan tinggi. Bayangkan lanskap pegunungan: tiap titik di peta punya ketinggian. Tujuan optimasi adalah menemukan lembah terdalam lanskap itu.
        """),
        T("""
        ## Kontur sebagai peta ketinggian

        Permukaan tiga dimensi sulit digambar, sehingga kita sering memakai **kontur**, yaitu kurva yang menghubungkan titik-titik berketinggian sama, seperti garis tinggi pada peta topografi. Untuk `f(x, y) = x^2 + y^2` konturnya lingkaran konsentris dengan pusat di titik asal. Makin jauh dari pusat, makin tinggi nilainya.

        Jarak antar kontur memberi informasi. Kontur rapat berarti lereng curam karena tinggi berubah cepat pada jarak pendek. Kontur renggang berarti lereng landai. Pada fungsi loss yang berbentuk lembah memanjang, kontur berbentuk elips pipih, dan itulah penyebab gradient descent bergerak zig-zag yang akan kita bahas nanti.
        """),
        C(
            """
            import numpy as np

            def f(x, y):
                return x ** 2 + y ** 2

            titik = [(3, 4), (5, 0), (0, -5), (-4, 3)]
            print([f(x, y) for x, y in titik])
            x = np.linspace(-2, 2, 5)
            X, Y = np.meshgrid(x, x)
            Z = f(X, Y)
            print(Z.shape, Z.min(), Z.max())
            print([int(i) for i in np.unravel_index(Z.argmin(), Z.shape)])
            """,
            """
            [25, 25, 25, 25]
            (5, 5) 0.0 8.0
            [2, 2]
            """,
            """
            Keempat titik berada pada kontur yang sama yaitu lingkaran berjari-jari lima. Nilai terkecil pada grid berada di titik tengah.
            """,
            filename="kontur.py",
        ),
        T("""
        ## Turunan parsial

        Untuk menurunkan fungsi banyak variabel, kita menurunkannya terhadap satu variabel sambil menahan variabel lain tetap sebagai konstanta. Hasilnya disebut **turunan parsial**, ditulis `df/dx` atau `f_x`. Ia mengukur seberapa cepat `f` berubah bila hanya `x` yang digeser sedikit, sementara `y` dibiarkan.

        Contoh: `f(x, y) = x^2 y + 3 y`. Menurunkan terhadap `x` dengan `y` dianggap konstanta memberi `2 x y`. Menurunkan terhadap `y` dengan `x` dianggap konstanta memberi `x^2 + 3`. Semua aturan turunan satu variabel, yaitu pangkat, kali, bagi, dan rantai, tetap berlaku. Satu-satunya perubahan adalah kebiasaan membaca variabel lain sebagai angka biasa.
        """),
        C(
            """
            def f(x, y):
                return x ** 2 * y + 3 * y

            def pd_x(f, x, y, h=1e-6):
                return (f(x + h, y) - f(x - h, y)) / (2 * h)

            def pd_y(f, x, y, h=1e-6):
                return (f(x, y + h) - f(x, y - h)) / (2 * h)

            print(f(2, 1))
            print(round(pd_x(f, 2, 1), 4), round(pd_y(f, 2, 1), 4))
            print(2 * 2 * 1, 2 ** 2 + 3)
            """,
            """
            7
            4.0 7.0
            4 7
            """,
            """
            Turunan numerik cocok dengan rumus `2xy` dan `x^2 + 3` pada titik dua dan satu.
            """,
            filename="parsial_dasar.py",
        ),
        T("""
        ## Tafsir turunan parsial

        Turunan parsial adalah kemiringan lereng pada satu arah sumbu. `f_x` di suatu titik memberi tahu kemiringan bila kamu berjalan lurus ke arah sumbu `x`, dan `f_y` bila berjalan ke arah sumbu `y`. Tanda memberi arah: positif berarti naik, negatif turun. Besarnya memberi kecuraman.

        Dalam ML, turunan parsial loss terhadap satu parameter menjawab pertanyaan sederhana: bila parameter ini dinaikkan sedikit sementara parameter lain tetap, apakah loss naik atau turun, dan seberapa cepat? Jawaban untuk semua parameter, dikumpulkan bersama, adalah gradien yang menjadi pusat pelajaran berikutnya.
        """),
        K(
            "tip",
            """
            Saat menurunkan terhadap satu variabel, ganti variabel lain dengan angka sungguhan di kepalamu, misalnya `y = 5`. Ini mencegah kesalahan menurunkan variabel yang seharusnya konstan.
            """,
            title="Trik mental",
        ),
        T("""
        ## Gradien

        Kumpulan semua turunan parsial disusun menjadi vektor yang disebut **gradien**, ditulis `grad f` atau `nabla f`. Untuk `f(x, y)` gradiennya `[f_x, f_y]`. Untuk fungsi `n` variabel gradiennya vektor dengan `n` komponen. Gradien adalah padanan turunan untuk fungsi banyak variabel: ia merangkum seluruh informasi kemiringan di satu titik dalam satu vektor.

        Misalnya `f(x, y) = x^2 + 3xy + y^2` memiliki gradien `[2x + 3y, 3x + 2y]`. Di titik `(1, 2)` nilainya `[8, 7]`. Gradien ini bergantung pada titik, jadi ia adalah fungsi bernilai vektor. Pelajaran berikut menunjukkan bahwa vektor ini menunjuk ke arah kenaikan tercuram.
        """),
        C(
            """
            import numpy as np

            def f(p):
                x, y = p
                return x ** 2 + 3 * x * y + y ** 2

            def gradien(f, p, h=1e-6):
                p = np.array(p, dtype=float)
                g = np.zeros_like(p)
                for i in range(len(p)):
                    e = np.zeros_like(p)
                    e[i] = h
                    g[i] = (f(p + e) - f(p - e)) / (2 * h)
                return g

            g = gradien(f, [1, 2])
            print(g.round(4).tolist())
            print(round(float(np.linalg.norm(g)), 4))
            """,
            """
            [8.0, 7.0]
            10.6301
            """,
            """
            Gradien di `(1, 2)` adalah `[8, 7]` sesuai rumus `[2x + 3y, 3x + 2y]`. Panjangnya akar dari 113.
            """,
            filename="gradien_numerik.py",
        ),
        T("""
        ## Bidang singgung

        Pada satu variabel, garis singgung adalah aproksimasi linear terbaik fungsi. Pada dua variabel, perannya diambil oleh **bidang singgung**: `z = f(a, b) + f_x (x - a) + f_y (y - b)`. Bidang ini menyentuh permukaan di `(a, b)` dan sangat dekat dengan permukaan di sekitarnya.

        Aproksimasi linear ini adalah dasar banyak algoritma optimasi. Gradient descent memakai bidang singgung untuk memutuskan langkah, dengan asumsi bahwa untuk langkah yang cukup kecil permukaan lokal hampir datar. Karena itu learning rate yang kecil penting: pada langkah besar, aproksimasi bidang tidak lagi berlaku dan loss bisa justru naik.
        """),
        T("""
        ## Notasi yang akan kamu temui

        Gradien muncul dengan beberapa notasi. Selain `grad f`, kamu akan melihat simbol nabla `nabla f`, dan dalam kode sering `dL_dw` atau sekadar `grad`. Semuanya berarti hal sama: vektor turunan parsial. Pada buku pelajaran turunan parsial ditulis dengan simbol d bulat, sedangkan di sini kita memakai `f_x` agar mudah diketik.
        """),
        E(
            "A3-03-1-ex1",
            "mudah",
            """
            Tulis fungsi `parsial_x(f, x, y, h=1e-6)` yang mengembalikan turunan parsial `f` terhadap `x` di `(x, y)` dengan selisih pusat, dibulatkan 4 desimal. Hindari `-0.0`.
            """,
            """
            def parsial_x(f, x, y, h=1e-6):
                # TODO: implementasikan
                pass
            """,
            """
            assert parsial_x(lambda x, y: x ** 2 * y + 3 * y, 2, 1) == 4.0
            assert parsial_x(lambda x, y: x * y, 3, 4) == 4.0
            assert parsial_x(lambda x, y: y ** 3, 1, 2) == 0.0
            assert parsial_x(lambda x, y: x ** 2 + y ** 2, 3, 4) == 6.0
            """,
            "Geser x maju dan mundur sementara y tetap.",
            """
            def parsial_x(f, x, y, h=1e-6):
                return round((f(x + h, y) - f(x - h, y)) / (2 * h), 4) + 0.0
            """,
        ),
        E(
            "A3-03-1-ex2",
            "mudah",
            """
            Tulis fungsi `gradien_2d(f, x, y, h=1e-6)` yang mengembalikan list `[f_x, f_y]` di `(x, y)` dibulatkan 4 desimal. Hindari `-0.0`.
            """,
            """
            def gradien_2d(f, x, y, h=1e-6):
                # TODO: implementasikan
                pass
            """,
            """
            assert gradien_2d(lambda x, y: x ** 2 + 3 * x * y + y ** 2, 1, 2) == [8.0, 7.0]
            assert gradien_2d(lambda x, y: x * y, 3, 4) == [4.0, 3.0]
            assert gradien_2d(lambda x, y: 5, 1, 1) == [0.0, 0.0]
            assert gradien_2d(lambda x, y: x ** 2 + y ** 2, 0, 0) == [0.0, 0.0]
            """,
            "Hitung dua turunan parsial dan kembalikan dalam satu list.",
            """
            def gradien_2d(f, x, y, h=1e-6):
                fx = (f(x + h, y) - f(x - h, y)) / (2 * h)
                fy = (f(x, y + h) - f(x, y - h)) / (2 * h)
                return [round(fx, 4) + 0.0, round(fy, 4) + 0.0]
            """,
        ),
        E(
            "A3-03-1-ex3",
            "sedang",
            """
            Tulis fungsi `norma_gradien(g)` yang mengembalikan panjang (norma Euclidean) vektor `g` dibulatkan 4 desimal.
            """,
            """
            import math

            def norma_gradien(g):
                # TODO: implementasikan
                pass
            """,
            """
            assert norma_gradien([3, 4]) == 5.0
            assert norma_gradien([8, 7]) == 10.6301
            assert norma_gradien([0, 0]) == 0.0
            assert norma_gradien([1, 1, 1, 1]) == 2.0
            """,
            "Jumlahkan kuadrat komponen lalu ambil akar.",
            """
            import math

            def norma_gradien(g):
                return round(math.sqrt(sum(v * v for v in g)), 4)
            """,
        ),
        E(
            "A3-03-1-ex4",
            "menantang",
            """
            Tulis fungsi `bidang_singgung(f, x0, y0, x, y)` yang mengembalikan nilai bidang singgung `f` di `(x0, y0)` pada titik `(x, y)`, yaitu `f(x0, y0) + f_x (x - x0) + f_y (y - y0)`, dengan turunan parsial numerik selisih pusat `h=1e-6`. Bulatkan 4 desimal.
            """,
            """
            def bidang_singgung(f, x0, y0, x, y):
                # TODO: implementasikan
                pass
            """,
            """
            assert bidang_singgung(lambda x, y: x ** 2 + y ** 2, 1, 1, 1.1, 1.1) == 2.4
            assert bidang_singgung(lambda x, y: x * y, 2, 3, 2, 3) == 6.0
            assert bidang_singgung(lambda x, y: 2 * x + 3 * y + 1, 0, 0, 1, 1) == 6.0
            assert bidang_singgung(lambda x, y: x ** 2 * y, 1, 2, 1, 3) == 3.0
            """,
            "Hitung dua turunan parsial di titik acuan lalu rakit rumus bidang.",
            """
            def bidang_singgung(f, x0, y0, x, y):
                h = 1e-6
                fx = (f(x0 + h, y0) - f(x0 - h, y0)) / (2 * h)
                fy = (f(x0, y0 + h) - f(x0, y0 - h)) / (2 * h)
                return round(f(x0, y0) + fx * (x - x0) + fy * (y - y0), 4)
            """,
        ),
    ],
    [
        M("Menurunkan variabel yang seharusnya konstan.", "Anggap variabel lain sebagai angka."),
        M("Mengira gradien adalah satu bilangan.", "Gradien adalah vektor turunan parsial."),
        M("Mengabaikan bahwa gradien bergantung pada titik.", "Gradien berubah dari titik ke titik."),
    ],
    [
        Q("Turunan parsial menahan?", ["Semua variabel", "Variabel lain tetap", "Fungsi tetap", "Titik tetap"], 1, "Variabel lain dianggap konstanta.", hint="Satu variabel bergerak."),
        Q("Gradien f(x,y)?", ["Bilangan", "Vektor turunan parsial", "Matriks", "Integral"], 1, "[f_x, f_y].", hint="Vektor."),
        Q("Kontur adalah?", ["Titik maksimum", "Kurva ketinggian sama", "Gradien", "Turunan"], 1, "Seperti garis tinggi peta.", hint="Peta."),
        Q("f_x untuk x^2 y?", ["2x", "2xy", "x^2", "y"], 1, "y dianggap konstan.", hint="Aturan pangkat."),
        Q("Kontur rapat berarti?", ["Lereng landai", "Lereng curam", "Datar", "Tak terdefinisi"], 1, "Perubahan cepat.", hint="Dekat-dekat."),
    ],
    [
        "Turunan parsial menurunkan satu variabel dengan variabel lain tetap.",
        "Gradien adalah vektor semua turunan parsial.",
        "Kontur membantu membayangkan fungsi dua variabel.",
        "Bidang singgung adalah aproksimasi linear lokal.",
    ],
    [],
)

l2 = lesson(
    "A3-03-2",
    "Gradien dan arah penurunan tercuram",
    35,
    [
        "Menghitung turunan berarah dari gradien",
        "Memahami bahwa gradien menunjuk kenaikan tercuram",
        "Memahami bahwa gradien tegak lurus kontur",
        "Menyusun langkah penurunan gradien sederhana",
    ],
    [
        T("""
        ## Bergerak ke arah mana pun

        Turunan parsial hanya memberi kemiringan sepanjang sumbu. Tetapi kita bisa bergerak ke arah mana pun di permukaan. **Turunan berarah** `D_u f` mengukur laju perubahan `f` bila kita bergerak searah vektor satuan `u`. Rumusnya sangat sederhana: `D_u f = grad f . u`, yaitu hasil kali dalam gradien dengan arah.

        Rumus ini luar biasa berguna. Gradien dihitung sekali, lalu laju perubahan untuk arah mana pun cukup dengan hasil kali dalam. Bila `u` searah sumbu `x`, hasilnya `f_x`. Bila `u` miring, hasilnya campuran `f_x` dan `f_y` berbobot komponen `u`.
        """),
        C(
            """
            import numpy as np

            g = np.array([8.0, 7.0])
            n = np.linalg.norm(g)
            u = g / n
            print(round(float(n), 4), u.round(4).tolist())
            print(round(float(g @ u), 4))
            print(round(float(g @ -u), 4))
            tegak = np.array([-u[1], u[0]])
            print(round(float(g @ tegak), 4) + 0.0)
            """,
            """
            10.6301 [0.7526, 0.6585]
            10.6301
            -10.6301
            0.0
            """,
            """
            Bergerak searah gradien memberi laju sebesar norma gradien, berlawanan memberi minus norma, dan tegak lurus memberi nol.
            """,
            filename="arah_tercuram.py",
        ),
        T("""
        ## Gradien menunjuk kenaikan tercuram

        Hasil kali dalam dua vektor sama dengan hasil kali panjang keduanya dikali kosinus sudut di antaranya. Untuk `u` satuan, `grad f . u = ||grad f|| cos(theta)`. Nilai ini paling besar saat `cos(theta) = 1`, yaitu `u` searah gradien. Jadi arah kenaikan tercuram adalah arah gradien, dan laju kenaikan maksimumnya sama dengan panjang gradien.

        Sebaliknya, arah penurunan tercuram adalah **minus gradien**. Laju penurunannya juga sebesar panjang gradien. Dua kalimat sederhana ini adalah seluruh dasar gradient descent: untuk menurunkan loss secepat mungkin, bergeraklah ke arah minus gradien. Di titik tempat gradien nol, lereng datar di semua arah dan tidak ada arah penurunan lokal.
        """),
        C(
            """
            import numpy as np

            g = np.array([8.0, 7.0])
            u = np.array([0.6, 0.8])
            print(round(float(g @ u), 4))

            def f(p):
                x, y = p
                return x ** 2 + 3 * x * y + y ** 2

            p = np.array([1.0, 2.0])
            h = 1e-6
            numerik = (f(p + h * u) - f(p - h * u)) / (2 * h)
            print(round(float(numerik), 4))
            """,
            """
            10.4
            10.4
            """,
            """
            Turunan berarah dari rumus hasil kali dalam sama dengan hitungan numerik sepanjang arah yang sama.
            """,
            filename="turunan_arah.py",
        ),
        T("""
        ## Gradien tegak lurus kontur

        Sepanjang kontur nilai fungsi tidak berubah, sehingga turunan berarah sepanjang arah singgung kontur sama dengan nol. Karena `grad f . u = 0` untuk `u` singgung, gradien tegak lurus terhadap kontur. Pada peta topografi, ini berarti arah tanjakan paling curam memotong garis tinggi secara tegak lurus, seperti yang diketahui setiap pendaki.

        Untuk `f(x, y) = x^2 + y^2`, gradiennya `[2x, 2y]`, tak lain dari dua kali vektor posisi. Ia menunjuk radial keluar dari pusat, tegak lurus lingkaran. Fakta geometris ini menjelaskan banyak hal tentang perilaku gradient descent pada lembah berbentuk elips, yang akan segera kamu lihat.
        """),
        C(
            """
            import numpy as np

            p = np.array([3.0, 4.0])
            g = 2 * p
            singgung = np.array([-4.0, 3.0])
            print(float(g @ singgung) == 0.0)
            cos = float(g @ p) / (np.linalg.norm(g) * np.linalg.norm(p))
            print(round(cos, 4))
            """,
            """
            True
            1.0
            """,
            """
            Gradien lingkaran tegak lurus arah singgungnya dan sejajar vektor posisi.
            """,
            filename="gradien_kontur.py",
        ),
        K(
            "warning",
            """
            Rumus `grad f . u` hanya berlaku bila `u` vektor satuan. Bila arahnya belum dinormalkan, bagi dulu dengan panjangnya atau hasilnya terlalu besar.
            """,
            title="Normalkan arahnya",
        ),
        T("""
        ## Langkah penurunan gradien

        Gabungkan semua ide ini menjadi algoritma. Mulai dari titik `p`. Hitung gradien `g` di `p`. Bergerak sedikit ke arah `-g`: `p_baru = p - lr * g`, dengan `lr` adalah **learning rate**, ukuran langkah. Ulangi. Bila `lr` cukup kecil dan fungsinya halus, setiap langkah menurunkan nilai fungsi, dan titik bergerak menuju lembah.

        Contoh `f = x^2 + y^2` dengan gradien `[2x, 2y]`. Dengan `lr = 0.1` tiap langkah mengalikan koordinat dengan `0.8`, sehingga titik meluruh menuju nol. Dengan `lr = 0.5` titik jatuh tepat ke nol dalam satu langkah. Dengan `lr = 1.0` titik hanya membalik tanda tanpa mendekat, dan dengan `lr > 1` titik menjauh. Memilih learning rate adalah keputusan penting yang dibahas di modul-modul selanjutnya.
        """),
        T("""
        ## Lembah elips dan zig-zag

        Bila kontur berbentuk lingkaran, arah minus gradien menunjuk langsung ke pusat dan penurunan lancar. Tetapi pada fungsi seperti `f = x^2 + 10 y^2`, kontur berbentuk elips pipih. Minus gradien tegak lurus kontur sehingga di sisi elips ia tidak menunjuk ke pusat, melainkan miring, dan algoritma memantul bolak-balik melintasi lembah sambil perlahan maju sepanjang dasarnya.

        Gejala zig-zag ini adalah masalah klasik. Lembah yang sangat berbeda kemiringan pada dua arah disebut berkondisi buruk, terkait bilangan kondisi matriks Hessian. Teknik seperti momentum, normalisasi fitur, dan optimizer adaptif ada untuk mengurangi masalah ini, dan kamu akan mempelajarinya pada modul terakhir kursus ini.
        """),
        T("""
        ## Titik datar dan kriteria berhenti

        Di titik gradien nol, algoritma tidak lagi bergerak karena langkahnya nol. Itulah dasar kriteria berhenti paling umum: hentikan iterasi ketika norma gradien lebih kecil dari ambang kecil, atau ketika perubahan loss antar iterasi sudah sangat kecil. Kriteria tambahan adalah batas jumlah iterasi agar program tidak berjalan selamanya.

        Perlu diingat bahwa gradien nol belum menjamin minimum. Titik itu bisa minimum lokal, maksimum, atau titik pelana. Pada fungsi cembung seperti MSE regresi linear, setiap titik gradien nol adalah minimum global, sehingga algoritma pasti berakhir di jawaban terbaik. Pada jaringan saraf yang tidak cembung, jaminan itu hilang, namun dalam praktik minimum lokal yang ditemukan biasanya cukup baik.
        """),
        E(
            "A3-03-2-ex1",
            "mudah",
            """
            Tulis fungsi `turunan_arah(g, u)` yang mengembalikan hasil kali dalam gradien `g` dan arah satuan `u` dibulatkan 4 desimal. Hindari `-0.0`.
            """,
            """
            def turunan_arah(g, u):
                # TODO: implementasikan
                pass
            """,
            """
            assert turunan_arah([8, 7], [0.6, 0.8]) == 10.4
            assert turunan_arah([8, 7], [1, 0]) == 8.0
            assert turunan_arah([1, 2, 3], [0, 0, 1]) == 3.0
            assert turunan_arah([3, 4], [0.8, -0.6]) == 0.0
            """,
            "Jumlahkan hasil kali komponen yang berpasangan.",
            """
            def turunan_arah(g, u):
                return round(sum(a * b for a, b in zip(g, u)), 4) + 0.0
            """,
        ),
        E(
            "A3-03-2-ex2",
            "mudah",
            """
            Tulis fungsi `arah_tercuram(g)` yang mengembalikan vektor satuan searah `g` (list dibulatkan 4 desimal). Bila `g` vektor nol kembalikan vektor nol dengan panjang sama. Hindari `-0.0`.
            """,
            """
            import math

            def arah_tercuram(g):
                # TODO: implementasikan
                pass
            """,
            """
            assert arah_tercuram([3, 4]) == [0.6, 0.8]
            assert arah_tercuram([0, 5]) == [0.0, 1.0]
            assert arah_tercuram([0, 0]) == [0.0, 0.0]
            assert arah_tercuram([-8, -7]) == [-0.7526, -0.6585]
            """,
            "Bagi tiap komponen dengan norma kecuali norma nol.",
            """
            import math

            def arah_tercuram(g):
                n = math.sqrt(sum(v * v for v in g))
                if n == 0:
                    return [0.0] * len(g)
                return [round(v / n, 4) + 0.0 for v in g]
            """,
        ),
        E(
            "A3-03-2-ex3",
            "sedang",
            """
            Tulis fungsi `langkah_turun(titik, g, lr)` yang mengembalikan list `titik - lr * g` dibulatkan 4 desimal. Hindari `-0.0`.
            """,
            """
            def langkah_turun(titik, g, lr):
                # TODO: implementasikan
                pass
            """,
            """
            assert langkah_turun([1, 2], [8, 7], 0.1) == [0.2, 1.3]
            assert langkah_turun([0, 0], [1, -1], 0.5) == [-0.5, 0.5]
            assert langkah_turun([3], [6], 0.25) == [1.5]
            assert langkah_turun([1, 1], [0, 0], 1) == [1.0, 1.0]
            """,
            "Kurangkan lr kali gradien dari tiap koordinat.",
            """
            def langkah_turun(titik, g, lr):
                return [round(p - lr * v, 4) + 0.0 for p, v in zip(titik, g)]
            """,
        ),
        E(
            "A3-03-2-ex4",
            "menantang",
            """
            Tulis fungsi `turun_gradien(grad, mulai, lr, langkah)` yang menerima fungsi `grad` (menerima list titik dan mengembalikan list gradien), titik awal, learning rate, dan jumlah langkah. Ulangi `titik = titik - lr * grad(titik)` sebanyak `langkah` kali lalu kembalikan titik dibulatkan 4 desimal. Hindari `-0.0`.
            """,
            """
            def turun_gradien(grad, mulai, lr, langkah):
                # TODO: implementasikan
                pass
            """,
            """
            g1 = lambda p: [2 * p[0], 2 * p[1]]
            assert turun_gradien(g1, [1, 1], 0.1, 2) == [0.64, 0.64]
            assert turun_gradien(g1, [1, 1], 0.5, 1) == [0.0, 0.0]
            assert turun_gradien(g1, [1, 1], 1.0, 3) == [-1.0, -1.0]
            g2 = lambda p: [2 * (p[0] - 3), 2 * (p[1] + 1)]
            assert turun_gradien(g2, [0, 0], 0.25, 2) == [2.25, -0.75]
            """,
            "Perbarui seluruh koordinat dengan gradien dari titik yang sama pada tiap langkah.",
            """
            def turun_gradien(grad, mulai, lr, langkah):
                p = [float(v) for v in mulai]
                for _ in range(langkah):
                    g = grad(p)
                    p = [a - lr * b for a, b in zip(p, g)]
                return [round(v, 4) + 0.0 for v in p]
            """,
        ),
    ],
    [
        M("Memakai arah yang belum dinormalkan pada turunan berarah.", "Gunakan vektor satuan."),
        M("Bergerak searah gradien saat ingin meminimalkan.", "Minimisasi memakai minus gradien."),
        M("Menganggap gradien menunjuk ke minimum.", "Gradien hanya menunjuk kenaikan tercuram lokal."),
    ],
    [
        Q("Turunan berarah?", ["grad f . u", "grad f x u", "f(u)", "grad f / u"], 0, "Hasil kali dalam dengan arah satuan.", hint="Dot."),
        Q("Arah kenaikan tercuram?", ["Gradien", "Minus gradien", "Tegak lurus gradien", "Sumbu x"], 0, "Searah gradien.", hint="Kosinus satu."),
        Q("Gradien terhadap kontur?", ["Sejajar", "Tegak lurus", "Berimpit", "Tak berhubungan"], 1, "Sepanjang kontur laju nol.", hint="Dot nol."),
        Q("Arah minimisasi?", ["Gradien", "Minus gradien", "Acak", "Tetap"], 1, "Turun secepatnya.", hint="Berlawanan."),
        Q("Learning rate terlalu besar?", ["Selalu cepat", "Bisa menyebabkan divergen", "Tidak berpengaruh", "Menghapus gradien"], 1, "Langkah melompati lembah.", hint="Aproksimasi gagal."),
    ],
    [
        "Turunan berarah sama dengan hasil kali dalam gradien dan arah satuan.",
        "Gradien menunjuk kenaikan tercuram dan minus gradien penurunan tercuram.",
        "Gradien tegak lurus kontur.",
        "Gradient descent bergerak melawan gradien dengan learning rate.",
    ],
    [],
)

l3 = lesson(
    "A3-03-3",
    "Penerapan: gradien loss, Jacobian, dan Hessian",
    35,
    [
        "Menurunkan gradien MSE untuk regresi linear",
        "Menyusun gradien dalam bentuk matriks",
        "Menghitung Jacobian untuk fungsi vektor",
        "Menggunakan Hessian untuk menilai jenis titik kritis",
    ],
    [
        T("""
        ## Loss regresi linear

        Mari terapkan semuanya pada model sungguhan. Regresi linear sederhana memprediksi `y_hat = w x + b` dengan parameter `w` dan `b`. Loss rata-rata galat kuadrat (MSE) adalah `L = (1/n) sum (w x_i + b - y_i)^2`. Ini fungsi dua variabel dari `w` dan `b`, sehingga kita menghitung dua turunan parsial.

        Dengan aturan rantai: `dL/dw = (2/n) sum (y_hat_i - y_i) x_i` dan `dL/db = (2/n) sum (y_hat_i - y_i)`. Pola yang indah: gradien adalah rata-rata galat berbobot masukan. Galat positif, yaitu prediksi terlalu tinggi, mendorong parameter turun. Bentuk ini muncul lagi hampir tanpa perubahan di regresi logistik dan jaringan saraf.
        """),
        T("""
        ## Bentuk matriks

        Untuk banyak fitur, penulisan satu-satu menjadi rumit. Susun data dalam matriks `X` berukuran `n x d`, tambahkan kolom satu untuk bias, dan kumpulkan parameter dalam vektor `w`. Prediksi menjadi `X w` dan loss `L = (1/n) ||X w - y||^2`. Gradiennya menjadi `grad L = (2/n) X^T (X w - y)`.

        Satu rumus ringkas itu menghitung gradien untuk semua parameter sekaligus, dan memanfaatkan perkalian matriks yang sangat dioptimasi. Ini alasan kode ML ditulis dengan operasi vektor, bukan perulangan. Di bagian awal kursus kamu sudah belajar perkalian matriks, dan sekarang kamu melihat manfaat langsungnya.
        """),
        C(
            """
            import numpy as np

            x = np.array([1.0, 2.0, 3.0])
            y = np.array([2.0, 4.0, 6.0])
            X = np.column_stack([x, np.ones_like(x)])
            w = np.zeros(2)

            def mse(w):
                return np.mean((X @ w - y) ** 2)

            def grad(w):
                return 2 / len(y) * X.T @ (X @ w - y)

            print(round(float(mse(w)), 4), grad(w).round(4).tolist())
            gn = np.array([(mse(w + e) - mse(w - e)) / 2e-6 for e in (np.array([1e-6, 0.0]), np.array([0.0, 1e-6]))])
            print(np.allclose(grad(w), gn, atol=1e-4))
            w2 = np.array([2.0, 0.0])
            print(mse(w2), grad(w2).tolist())
            """,
            """
            18.6667 [-18.6667, -8.0]
            True
            0.0 [0.0, 0.0]
            """,
            """
            Pada parameter nol gradien negatif untuk kedua parameter sehingga keduanya harus dinaikkan. Pada solusi sebenarnya `w = 2` dan `b = 0` loss dan gradien nol.
            """,
            filename="mse_gradien.py",
        ),
        K(
            "tip",
            """
            Ingat bentuk `X^T (X w - y)`: transpos data dikali residual. Bila bentuk matriksmu tidak cocok saat mengalikan, hampir pasti transposnya terbalik.
            """,
            title="Periksa dimensi",
        ),
        T("""
        ## Jacobian

        Bagaimana bila fungsi mengembalikan vektor, bukan satu bilangan? Contohnya lapisan jaringan saraf yang memetakan `n` masukan ke `m` keluaran. Turunan fungsi seperti itu adalah matriks, disebut **Jacobian**, dengan `m` baris dan `n` kolom: baris ke-`i` adalah gradien keluaran ke-`i`, dan elemen `(i, j)` adalah `df_i / dx_j`.

        Jacobian adalah generalisasi turunan paling lengkap. Aturan rantai untuk komposisi menjadi perkalian matriks Jacobian: `J_(f o g) = J_f J_g`. Backpropagation sesungguhnya adalah perkalian rantai Jacobian dari lapisan terakhir ke awal. Untungnya pustaka mengurusnya, dan kita biasanya hanya perlu hasil kali Jacobian dengan vektor, yang jauh lebih murah daripada membentuk matriks penuh.
        """),
        C(
            """
            import math

            def F(p):
                x, y = p
                return [x ** 2 * y, 5 * x + math.sin(y)]

            def jacobian(F, p, h=1e-6):
                m = len(F(p))
                n = len(p)
                J = [[0.0] * n for _ in range(m)]
                for j in range(n):
                    a = list(p)
                    b = list(p)
                    a[j] += h
                    b[j] -= h
                    fa, fb = F(a), F(b)
                    for i in range(m):
                        J[i][j] = (fa[i] - fb[i]) / (2 * h)
                return J

            J = jacobian(F, [1.0, 2.0])
            print([[round(v, 4) for v in baris] for baris in J])
            """,
            """
            [[4.0, 1.0], [5.0, -0.4161]]
            """,
            """
            Jacobian analitiknya `[[2xy, x^2], [5, cos y]]` di `(1, 2)` bernilai `[[4, 1], [5, -0.4161]]`, sama dengan hasil numerik.
            """,
            filename="jacobian.py",
        ),
        T("""
        ## Hessian dan jenis titik kritis

        Turunan kedua untuk fungsi banyak variabel adalah matriks simetris **Hessian** `H`, dengan elemen `H_ij = d^2 f / (dx_i dx_j)`. Hessian mengukur kelengkungan permukaan pada tiap arah. Di titik kritis, tempat gradien nol, eigenvalue Hessian menentukan jenisnya.

        Bila semua eigenvalue positif, permukaan melengkung ke atas ke segala arah dan titik itu adalah minimum lokal. Bila semua negatif, maksimum lokal. Bila ada yang positif dan ada yang negatif, titik itu adalah **titik pelana**: lembah pada satu arah tetapi puncak pada arah lain. Di ruang berdimensi tinggi titik pelana jauh lebih umum daripada minimum lokal, dan itu sebabnya pelatihan jaringan sering melambat di dekatnya.
        """),
        C(
            """
            import numpy as np

            def f(p):
                x, y = p
                return x ** 2 + 3 * x * y + y ** 2

            def hessian(f, p, h=1e-3):
                p = np.array(p, dtype=float)
                n = len(p)
                H = np.zeros((n, n))
                for i in range(n):
                    for j in range(n):
                        ei = np.zeros(n)
                        ej = np.zeros(n)
                        ei[i] = h
                        ej[j] = h
                        H[i, j] = (f(p + ei + ej) - f(p + ei - ej) - f(p - ei + ej) + f(p - ei - ej)) / (4 * h * h)
                return H

            H = hessian(f, [0.0, 0.0])
            print(H.round(3).tolist())
            nilai = np.linalg.eigvalsh(H)
            print(nilai.round(3).tolist())
            print(bool(nilai.min() < 0 < nilai.max()))
            """,
            """
            [[2.0, 3.0], [3.0, 2.0]]
            [-1.0, 5.0]
            True
            """,
            """
            Hessian konstan `[[2, 3], [3, 2]]` memiliki eigenvalue minus satu dan lima, tanda bertentangan sehingga titik kritis di nol adalah titik pelana.
            """,
            filename="hessian.py",
        ),
        T("""
        ## Dari teori ke gradient descent

        Sekarang semua bahan sudah ada. Gradien memberi arah penurunan tercuram, learning rate menentukan ukuran langkah, dan Hessian menjelaskan bentuk lembah serta mengapa laju konvergensi berbeda antar arah. Modul-modul berikutnya menggabungkannya: aturan rantai untuk gradien jaringan, implementasi gradient descent dari nol, dan variasi seperti momentum.

        Latihan di akhir pelajaran ini membangun bagian-bagian praktis: hitungan MSE, gradiennya, pelatihan regresi linear dengan gradient descent, dan Jacobian numerik. Kerjakan semuanya, karena modul selanjutnya mengandaikan kamu sudah nyaman dengan potongan-potongan ini.
        """),
        T("""
        ## Memilih ukuran data per langkah

        Rumus gradien MSE menjumlahkan seluruh data. Untuk data besar, menghitungnya penuh pada tiap langkah mahal. Solusinya gradient descent stokastik: pakai sebagian kecil data acak, disebut mini-batch, untuk memperkirakan gradien. Perkiraan itu berderau tetapi tidak bias, dan jauh lebih murah, sehingga pembaruan bisa dilakukan jauh lebih sering.

        Ukuran mini-batch adalah kompromi. Batch kecil memberi derau besar yang kadang membantu keluar dari titik pelana, sedangkan batch besar memberi gradien halus tetapi lebih lambat per langkah. Modul gradient descent dari nol akan membahas hal ini lebih jauh, lengkap dengan kode yang bisa kamu jalankan.
        """),
        E(
            "A3-03-3-ex1",
            "mudah",
            """
            Tulis fungsi `mse(w, b, x, y)` yang mengembalikan rata-rata kuadrat galat model `w x + b` terhadap list `x` dan `y`, dibulatkan 4 desimal.
            """,
            """
            def mse(w, b, x, y):
                # TODO: implementasikan
                pass
            """,
            """
            assert mse(0, 0, [1, 2, 3], [2, 4, 6]) == 18.6667
            assert mse(2, 0, [1, 2, 3], [2, 4, 6]) == 0.0
            assert mse(1, 1, [1, 2], [2, 3]) == 0.0
            assert mse(0, 0, [1], [3]) == 9.0
            """,
            "Hitung selisih prediksi dan target, kuadratkan, lalu rata-ratakan.",
            """
            def mse(w, b, x, y):
                n = len(x)
                return round(sum((w * a + b - t) ** 2 for a, t in zip(x, y)) / n, 4)
            """,
        ),
        E(
            "A3-03-3-ex2",
            "sedang",
            """
            Tulis fungsi `gradien_mse(w, b, x, y)` yang mengembalikan tuple `(dL/dw, dL/db)` dari MSE regresi linear, dibulatkan 4 desimal. Hindari `-0.0`.
            """,
            """
            def gradien_mse(w, b, x, y):
                # TODO: implementasikan
                pass
            """,
            """
            assert gradien_mse(0, 0, [1, 2, 3], [2, 4, 6]) == (-18.6667, -8.0)
            assert gradien_mse(2, 0, [1, 2, 3], [2, 4, 6]) == (0.0, 0.0)
            assert gradien_mse(1, 1, [1, 2], [2, 3]) == (0.0, 0.0)
            assert gradien_mse(0, 0, [1], [3]) == (-6.0, -6.0)
            """,
            "Rata-ratakan dua kali galat untuk bias dan dua kali galat dikali x untuk bobot.",
            """
            def gradien_mse(w, b, x, y):
                n = len(x)
                galat = [w * a + b - t for a, t in zip(x, y)]
                dw = 2 * sum(e * a for e, a in zip(galat, x)) / n
                db = 2 * sum(galat) / n
                return (round(dw, 4) + 0.0, round(db, 4) + 0.0)
            """,
        ),
        E(
            "A3-03-3-ex3",
            "sedang",
            """
            Tulis fungsi `fit_gd(x, y, lr, langkah)` yang melatih `w` dan `b` dengan gradient descent pada MSE mulai dari nol selama `langkah` iterasi dan mengembalikan tuple `(w, b)` dibulatkan 3 desimal. Hindari `-0.0`.
            """,
            """
            def fit_gd(x, y, lr, langkah):
                # TODO: implementasikan
                pass
            """,
            """
            assert fit_gd([1, 2, 3], [2, 4, 6], 0.1, 2000) == (2.0, 0.0)
            assert fit_gd([0, 1, 2, 3], [1, 3, 5, 7], 0.05, 5000) == (2.0, 1.0)
            assert fit_gd([1, 2, 3], [5, 5, 5], 0.05, 5000) == (0.0, 5.0)
            """,
            "Perbarui w dan b bersamaan memakai gradien yang dihitung dari nilai sebelum diperbarui.",
            """
            def fit_gd(x, y, lr, langkah):
                n = len(x)
                w, b = 0.0, 0.0
                for _ in range(langkah):
                    galat = [w * a + b - t for a, t in zip(x, y)]
                    dw = 2 * sum(e * a for e, a in zip(galat, x)) / n
                    db = 2 * sum(galat) / n
                    w -= lr * dw
                    b -= lr * db
                return (round(w, 3) + 0.0, round(b, 3) + 0.0)
            """,
        ),
        E(
            "A3-03-3-ex4",
            "menantang",
            """
            Tulis fungsi `jacobian_numerik(f, titik, h=1e-6)` yang menerima fungsi `f` (menerima list dan mengembalikan list) dan list `titik`, lalu mengembalikan Jacobian sebagai list of list (baris adalah keluaran, kolom adalah masukan) dengan selisih pusat, dibulatkan 4 desimal. Hindari `-0.0`.
            """,
            """
            import math

            def jacobian_numerik(f, titik, h=1e-6):
                # TODO: implementasikan
                pass
            """,
            """
            assert jacobian_numerik(lambda p: [p[0] ** 2 * p[1], 5 * p[0] + math.sin(p[1])], [1, 2]) == [[4.0, 1.0], [5.0, -0.4161]]
            assert jacobian_numerik(lambda p: [p[0] + p[1]], [3, 4]) == [[1.0, 1.0]]
            assert jacobian_numerik(lambda p: [p[0] * 2, p[1] * 3], [1, 1]) == [[2.0, 0.0], [0.0, 3.0]]
            """,
            "Geser tiap masukan maju dan mundur lalu isi satu kolom Jacobian dari selisih seluruh keluaran.",
            """
            import math

            def jacobian_numerik(f, titik, h=1e-6):
                n = len(titik)
                m = len(f(list(titik)))
                J = [[0.0] * n for _ in range(m)]
                for j in range(n):
                    a = list(titik)
                    b = list(titik)
                    a[j] += h
                    b[j] -= h
                    fa, fb = f(a), f(b)
                    for i in range(m):
                        J[i][j] = round((fa[i] - fb[i]) / (2 * h), 4) + 0.0
                return J
            """,
        ),
    ],
    [
        M("Menukar transpos pada rumus gradien matriks.", "Gunakan X^T (X w - y) dengan dimensi yang cocok."),
        M("Mengira titik kritis selalu minimum.", "Periksa eigenvalue Hessian untuk membedakan pelana."),
        M("Memperbarui parameter satu per satu dengan gradien yang sudah berubah.", "Hitung semua gradien dari titik yang sama."),
    ],
    [
        Q("Gradien MSE dalam bentuk matriks?", ["(2/n) X^T (X w - y)", "X w", "X^T X", "y - X"], 0, "Transpos data dikali residual.", hint="Dua per n."),
        Q("Jacobian berukuran?", ["n x n selalu", "m x n", "1 x n", "n x 1"], 1, "m keluaran dan n masukan.", hint="Baris keluaran."),
        Q("Hessian berisi?", ["Turunan pertama", "Turunan kedua", "Integral", "Rata-rata"], 1, "Turunan parsial kedua.", hint="Kelengkungan."),
        Q("Eigenvalue campuran tanda berarti?", ["Minimum", "Maksimum", "Titik pelana", "Datar"], 2, "Naik di satu arah dan turun di arah lain.", hint="Pelana."),
        Q("Aturan rantai untuk vektor memakai?", ["Penjumlahan", "Perkalian Jacobian", "Integral", "Limit"], 1, "J_f J_g.", hint="Matriks."),
    ],
    [
        "Gradien MSE regresi linear adalah rata-rata galat berbobot masukan.",
        "Bentuk matriks menghitung semua gradien sekaligus.",
        "Jacobian adalah turunan fungsi vektor dan Hessian turunan kedua.",
        "Eigenvalue Hessian membedakan minimum, maksimum, dan titik pelana.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perhitungan yang cukup jelas dalam teks.", "brief": []}

write_module(
    "A3",
    3,
    "Turunan parsial dan gradien",
    105,
    [
        "Menghitung turunan parsial dan gradien",
        "Memahami gradien sebagai arah kenaikan tercuram",
        "Menerapkan gradien pada regresi linear serta memahami Jacobian dan Hessian",
    ],
    [l1, l2, l3],
    video,
    REF,
)
