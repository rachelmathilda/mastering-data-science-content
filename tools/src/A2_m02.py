import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

l1 = lesson(
    "A2-02-1",
    "Matriks, bentuk, dan operasi per elemen",
    35,
    [
        "Memahami matriks sebagai tabel angka dengan baris dan kolom",
        "Mengakses elemen, baris, kolom, dan irisan matriks",
        "Melakukan penjumlahan, pengurangan, dan perkalian skalar matriks",
        "Menghitung transpos dan memahami bentuk matriks data",
    ],
    [
        T("""
        ## Matriks sebagai tabel angka

        **Matriks** adalah susunan angka dalam baris dan kolom. Matriks dengan `m` baris dan `n` kolom disebut matriks berukuran `m x n`. Dalam data science, matriks adalah bentuk paling alami untuk dataset: tiap baris adalah satu pengamatan (misalnya satu pelanggan) dan tiap kolom adalah satu fitur. Dataset dengan seribu pelanggan dan lima fitur adalah matriks `1000 x 5`.

        Elemen matriks ditulis `A[i, j]` untuk baris `i` dan kolom `j`. Di Python indeks dimulai dari nol, sedangkan di buku matematika biasanya dari satu. Hati-hati dengan perbedaan ini saat memindahkan rumus ke kode.

        Matriks juga bisa dipandang sebagai kumpulan vektor: tiap baris adalah vektor, atau tiap kolom adalah vektor. Kedua sudut pandang berguna. Pandangan baris menekankan pengamatan, pandangan kolom menekankan fitur.
        """),
        C(
            """
            import numpy as np

            A = np.array([[1, 2, 3],
                          [4, 5, 6]])
            print(A.shape, A.ndim, A.size)
            print(A[0, 1], A[1, 2], A[-1, -1])
            print(A[0].tolist(), A[:, 1].tolist())
            print(A[:, 1:].tolist())
            print(A[1, :2].tolist())
            data = np.zeros((1000, 5))
            print(data.shape)
            """,
            """
            (2, 3) 2 6
            2 6 6
            [1, 2, 3] [2, 5]
            [[2, 3], [5, 6]]
            [4, 5]
            (1000, 5)
            """,
            """
            `shape` memberi baris dan kolom. Indeks `A[i, j]` mengakses satu elemen, `A[i]` satu baris, dan `A[:, j]` satu kolom.
            """,
            filename="matriks_dasar.py",
        ),
        T("""
        ## Operasi per elemen

        Dua matriks berukuran sama dapat dijumlahkan dan dikurangkan elemen demi elemen. Perkalian skalar mengalikan setiap elemen. Operasi ini persis seperti pada vektor, hanya saja kini ada dua indeks. Matriks yang ukurannya berbeda tidak bisa dijumlahkan, dan percobaan melakukannya menimbulkan galat.

        Pada NumPy, operator `*` mengalikan per elemen, dikenal sebagai **hasil kali Hadamard**. Ini bukan perkalian matriks, yang memakai operator `@` dan dibahas di pelajaran berikutnya. Mencampur keduanya adalah kesalahan pemula yang sangat umum dan menghasilkan angka salah tanpa pesan galat bila ukurannya kebetulan cocok.

        NumPy juga mendukung *broadcasting*, yaitu perluasan otomatis ukuran yang lebih kecil agar cocok dengan yang lebih besar. Misalnya menambahkan vektor ke setiap baris matriks. Fitur ini sangat praktis tetapi perlu dipahami agar tidak menghasilkan hasil tak terduga.
        """),
        C(
            """
            import numpy as np

            A = np.array([[1, 2], [3, 4]])
            B = np.array([[10, 20], [30, 40]])
            print((A + B).tolist(), (B - A).tolist())
            print((2 * A).tolist(), (A * B).tolist())
            print((A ** 2).tolist())
            v = np.array([100, 200])
            print((A + v).tolist())
            try:
                A + np.ones((3, 2))
            except ValueError:
                print("ukuran tidak cocok")
            """,
            """
            [[11, 22], [33, 44]] [[9, 18], [27, 36]]
            [[2, 4], [6, 8]] [[10, 40], [90, 160]]
            [[1, 4], [9, 16]]
            [[101, 202], [103, 204]]
            ukuran tidak cocok
            """,
            """
            Operasi per elemen berlaku pada matriks seukuran. Broadcasting menambahkan vektor ke setiap baris, sedangkan ukuran yang tidak cocok menimbulkan `ValueError`.
            """,
            filename="operasi_elemen.py",
        ),
        K(
            "warning",
            """
            Pada NumPy, `A * B` adalah perkalian per elemen, bukan perkalian matriks. Untuk perkalian matriks sungguhan gunakan `A @ B` atau `np.matmul(A, B)`.
            """,
            title="Bintang bukan perkalian matriks",
        ),
        T("""
        ## Transpos

        **Transpos** matriks `A`, ditulis `A^T`, menukar baris dengan kolom: elemen `A[i, j]` menjadi `A^T[j, i]`. Matriks `2 x 3` menjadi `3 x 2`. Transpos dari transpos mengembalikan matriks asal, dan transpos dari jumlah sama dengan jumlah transpos.

        Transpos sangat sering dipakai dalam rumus statistik dan pembelajaran mesin. Misalnya matriks kovariansi data `X` yang sudah dipusatkan adalah `X^T X` dibagi jumlah pengamatan dikurangi satu. Persamaan normal regresi, `X^T X b = X^T y`, juga memakainya. Karena itu kamu perlu nyaman dengan ukuran: bila `X` berukuran `n x p`, maka `X^T` berukuran `p x n` dan `X^T X` berukuran `p x p`.

        Pada NumPy, transpos ditulis `A.T`. Operasi ini sangat murah karena tidak menyalin data, hanya mengubah cara membaca memori.
        """),
        C(
            """
            import numpy as np

            A = np.array([[1, 2, 3], [4, 5, 6]])
            print(A.T.tolist(), A.T.shape)
            print(np.array_equal(A.T.T, A))
            B = np.array([[1, 0], [2, 1], [0, 3]])
            print(np.array_equal((A + A).T, A.T + A.T))
            X = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
            print((X.T @ X).tolist(), (X.T @ X).shape)
            """,
            """
            [[1, 4], [2, 5], [3, 6]] (3, 2)
            True
            True
            [[35.0, 44.0], [44.0, 56.0]] (2, 2)
            """,
            """
            Transpos menukar baris dan kolom, dan transpos ganda mengembalikan matriks asal. `X.T @ X` selalu persegi dengan ukuran sama dengan jumlah fitur.
            """,
            filename="transpos.py",
        ),
        T("""
        ## Matriks data dan statistik per kolom

        Setelah dataset menjadi matriks, banyak ringkasan menjadi operasi sepanjang satu sumbu. Rata-rata tiap kolom (fitur) dihitung dengan `A.mean(axis=0)`, sedangkan rata-rata tiap baris (pengamatan) dengan `A.mean(axis=1)`. Argumen `axis` menyatakan sumbu yang dikurangi: `axis=0` menyusut menurut baris menghasilkan satu nilai per kolom.

        Pemusatan data, yaitu mengurangkan rata-rata kolom dari tiap kolom, dilakukan dengan `A - A.mean(axis=0)` berkat broadcasting. Langkah ini hampir selalu menjadi tahap awal sebelum PCA dan menghitung kovariansi.

        Ingat arti sumbu dengan benar karena kebalikannya menghasilkan angka yang masuk akal tetapi salah. Cara mengingatnya: sumbu yang kamu sebut adalah sumbu yang hilang dari hasil.
        """),
        T("""
        ## Memeriksa bentuk sebagai kebiasaan

        Kesalahan paling umum saat bekerja dengan matriks bukan salah rumus, melainkan salah bentuk. Biasakan mencetak `shape` setelah setiap langkah penting, terutama setelah transpos, irisan, dan perkalian. Irisan satu baris seperti `A[0]` menghasilkan array satu dimensi berbentuk `(n,)`, sedangkan `A[0:1]` menghasilkan matriks berbentuk `(1, n)`. Keduanya berperilaku berbeda pada perkalian dan broadcasting.

        Bila kamu butuh mengubah vektor menjadi kolom, gunakan `v.reshape(-1, 1)` atau `v[:, None]`. Tanda minus satu berarti biarkan NumPy menghitung ukurannya. Kebiasaan memeriksa bentuk akan menghemat banyak jam pencarian galat, dan akan terus berguna saat kamu bekerja dengan tensor di pembelajaran mendalam.
        """),
        E(
            "A2-02-1-ex1",
            "mudah",
            """
            Tulis fungsi `jumlah_matriks(A, B)` yang menjumlahkan dua matriks (list of list) berukuran sama dan mengembalikan matriks baru.
            """,
            """
            def jumlah_matriks(A, B):
                # TODO: implementasikan
                pass
            """,
            """
            assert jumlah_matriks([[1, 2], [3, 4]], [[10, 20], [30, 40]]) == [[11, 22], [33, 44]]
            assert jumlah_matriks([[0]], [[5]]) == [[5]]
            assert jumlah_matriks([], []) == []
            assert jumlah_matriks([[1, 2, 3]], [[1, 1, 1]]) == [[2, 3, 4]]
            """,
            "Gunakan comprehension bersarang dengan zip pada baris dan pada elemen.",
            """
            def jumlah_matriks(A, B):
                return [[x + y for x, y in zip(a, b)] for a, b in zip(A, B)]
            """,
        ),
        E(
            "A2-02-1-ex2",
            "mudah",
            """
            Tulis fungsi `transpos(A)` yang mengembalikan transpos matriks (list of list). Matriks kosong menghasilkan list kosong.
            """,
            """
            def transpos(A):
                # TODO: implementasikan
                pass
            """,
            """
            assert transpos([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]
            assert transpos([[1], [2]]) == [[1, 2]]
            assert transpos([]) == []
            assert transpos(transpos([[1, 2], [3, 4]])) == [[1, 2], [3, 4]]
            """,
            "zip(*A) mengelompokkan kolom, ubah tiap tuple menjadi list.",
            """
            def transpos(A):
                return [list(k) for k in zip(*A)]
            """,
        ),
        E(
            "A2-02-1-ex3",
            "sedang",
            """
            Tulis fungsi `rata_kolom(A)` yang mengembalikan list rata-rata tiap kolom matriks (list of list, tidak kosong).
            """,
            """
            def rata_kolom(A):
                # TODO: implementasikan
                pass
            """,
            """
            assert rata_kolom([[1, 2], [3, 4]]) == [2.0, 3.0]
            assert rata_kolom([[5, 10, 15]]) == [5.0, 10.0, 15.0]
            assert rata_kolom([[1], [2], [6]]) == [3.0]
            assert rata_kolom([[0, 0], [0, 0]]) == [0.0, 0.0]
            """,
            "Telusuri kolom lewat zip(*A) dan rata-ratakan.",
            """
            def rata_kolom(A):
                return [sum(k) / len(k) for k in zip(*A)]
            """,
        ),
        E(
            "A2-02-1-ex4",
            "menantang",
            """
            Tulis fungsi `pusatkan(A)` yang mengurangkan rata-rata tiap kolom dari kolom itu dan mengembalikan matriks baru (list of list) dengan nilai dibulatkan 4 desimal. Matriks tidak kosong.
            """,
            """
            def pusatkan(A):
                # TODO: implementasikan
                pass
            """,
            """
            assert pusatkan([[1, 2], [3, 4]]) == [[-1.0, -1.0], [1.0, 1.0]]
            assert pusatkan([[5, 5]]) == [[0.0, 0.0]]
            assert pusatkan([[1], [2], [6]]) == [[-2.0], [-1.0], [3.0]]
            assert pusatkan([[1, 10], [2, 20], [3, 30]]) == [[-1.0, -10.0], [0.0, 0.0], [1.0, 10.0]]
            """,
            "Hitung rata-rata kolom lebih dulu lalu kurangkan dari tiap elemen.",
            """
            def pusatkan(A):
                n = len(A)
                rata = [sum(k) / n for k in zip(*A)]
                return [[round(x - m, 4) for x, m in zip(baris, rata)] for baris in A]
            """,
        ),
    ],
    [
        M("Memakai * untuk perkalian matriks pada NumPy.", "Pakai @ untuk perkalian matriks."),
        M("Menjumlahkan matriks berukuran berbeda.", "Periksa shape sebelum operasi."),
        M("Terbalik memakai axis untuk rata-rata.", "axis=0 menghasilkan satu nilai per kolom."),
    ],
    [
        Q("Ukuran matriks dengan 3 baris dan 5 kolom?", ["5 x 3", "3 x 5", "15", "8"], 1, "Ditulis baris x kolom.", hint="Baris dulu."),
        Q("Hasil transpos matriks 2 x 3?", ["2 x 3", "3 x 2", "6 x 1", "1 x 6"], 1, "Baris dan kolom bertukar.", hint="Tukar ukuran."),
        Q("Operator * pada array NumPy melakukan?", ["Perkalian matriks", "Perkalian per elemen", "Dot product", "Pangkat"], 1, "Itu hasil kali Hadamard.", hint="Per elemen."),
        Q("Argumen untuk rata-rata tiap kolom?", ["axis=0", "axis=1", "axis=2", "axis=-0"], 0, "axis=0 menyusutkan baris sehingga tersisa satu nilai per kolom.", hint="Sumbu yang hilang."),
        Q("Ukuran X.T @ X bila X berukuran n x p?", ["n x n", "p x p", "n x p", "p x n"], 1, "(p x n) kali (n x p) menghasilkan p x p.", hint="Dalam harus cocok."),
    ],
    [
        "Matriks adalah tabel angka dan dataset umumnya berbentuk baris pengamatan kali kolom fitur.",
        "Penjumlahan dan skalar dilakukan per elemen pada matriks seukuran.",
        "Transpos menukar baris dan kolom dan sering muncul dalam rumus statistik.",
        "Rata-rata per kolom dan pemusatan memakai argumen axis.",
    ],
    [],
)

l2 = lesson(
    "A2-02-2",
    "Perkalian matriks",
    35,
    [
        "Menghitung perkalian matriks dengan vektor dan dengan matriks lain",
        "Memeriksa kecocokan ukuran dan menentukan ukuran hasil",
        "Memahami bahwa perkalian matriks tidak komutatif tetapi asosiatif",
        "Menafsirkan perkalian matriks sebagai transformasi dan komposisi",
    ],
    [
        T("""
        ## Perkalian matriks dengan vektor

        Perkalian matriks `A` (ukuran `m x n`) dengan vektor `x` (panjang `n`) menghasilkan vektor `y` (panjang `m`). Setiap komponen `y[i]` adalah dot product antara baris ke-`i` dari `A` dengan `x`. Cara kedua memandangnya: `y` adalah kombinasi linear dari kolom-kolom `A` dengan bobot komponen `x`.

        Kedua tafsir sama benarnya dan saling melengkapi. Tafsir baris membantu menghitung. Tafsir kolom membantu memahami: `A x` adalah semua titik yang bisa dicapai dari kolom `A`, dan ini dasar konsep ruang kolom dan peringkat.

        Dalam pembelajaran mesin, perkalian matriks dengan vektor muncul terus: prediksi untuk semua pengamatan sekaligus adalah `y = X w`, dengan `X` matriks fitur dan `w` vektor bobot. Satu operasi menggantikan perulangan atas seluruh baris data.
        """),
        C(
            """
            import numpy as np

            A = np.array([[1, 2, 3],
                          [4, 5, 6]])
            x = np.array([1, 0, -1])
            print((A @ x).tolist())
            print([sum(a * b for a, b in zip(baris, x.tolist())) for baris in A.tolist()])
            kombinasi = 1 * A[:, 0] + 0 * A[:, 1] + (-1) * A[:, 2]
            print(kombinasi.tolist())
            X = np.array([[1, 2], [1, 3], [1, 4]])
            w = np.array([10, 5])
            print((X @ w).tolist())
            """,
            """
            [-2, -2]
            [-2, -2]
            [-2, -2]
            [20, 25, 30]
            """,
            """
            Tiga cara menghitung memberi hasil sama: operator `@`, dot product tiap baris, dan kombinasi linear kolom. Prediksi untuk semua baris dihitung dengan satu perkalian `X @ w`.
            """,
            filename="matriks_vektor.py",
        ),
        T("""
        ## Perkalian dua matriks

        Perkalian `A B` dengan `A` berukuran `m x n` dan `B` berukuran `n x p` menghasilkan matriks `C` berukuran `m x p`. Elemen `C[i, j]` adalah dot product baris ke-`i` dari `A` dengan kolom ke-`j` dari `B`. Syarat mutlaknya: **jumlah kolom A sama dengan jumlah baris B**. Bila tidak, perkalian tidak terdefinisi.

        Cara mengingat ukuran: tulis `(m x n)(n x p)`. Dua angka dalam harus sama dan mereka lenyap, tersisa `m x p` di luar. Pemeriksaan ukuran ini adalah langkah pertama yang baik saat men-debug galat bentuk, yang sangat sering terjadi dalam pembelajaran mesin.

        Perkalian matriks bisa dipandang sebagai banyak perkalian matriks-vektor sekaligus: tiap kolom hasil adalah `A` dikalikan kolom yang bersesuaian dari `B`. Pandangan ini menjelaskan mengapa lapisan jaringan saraf memproses seluruh batch data dengan satu perkalian.
        """),
        C(
            """
            import numpy as np

            A = np.array([[1, 2], [3, 4], [5, 6]])
            B = np.array([[1, 0, 2], [0, 1, 3]])
            C = A @ B
            print(C.shape, C.tolist())
            print(C[1, 2], A[1] @ B[:, 2])
            try:
                B @ A.T
            except ValueError:
                print("ukuran tidak cocok")
            print((B @ A).shape)
            """,
            """
            (3, 3) [[1, 2, 8], [3, 4, 18], [5, 6, 28]]
            18 18
            ukuran tidak cocok
            (2, 2)
            """,
            """
            Hasil `3 x 2` kali `2 x 3` berukuran `3 x 3`. Elemen `C[1, 2]` adalah dot product baris 1 dari `A` dan kolom 2 dari `B`.
            """,
            filename="matriks_matriks.py",
        ),
        K(
            "tip",
            """
            Saat mendapat galat bentuk, tulis ukuran tiap matriks di kertas dalam bentuk `(m x n)(n x p)`. Dua angka dalam harus sama. Cara ini menyelesaikan sebagian besar galat dimensi.
            """,
            title="Periksa ukuran dalam",
        ),
        T("""
        ## Sifat perkalian matriks

        Perkalian matriks **tidak komutatif**: secara umum `A B` tidak sama dengan `B A`, bahkan ukurannya bisa berbeda atau salah satunya tidak terdefinisi. Urutan penting, dan membalikkannya mengubah hasil. Ini berbeda dari perkalian bilangan biasa.

        Namun perkalian matriks **asosiatif**: `(A B) C = A (B C)`, dan **distributif**: `A (B + C) = A B + A C`. Sifat asosiatif sangat berguna karena memungkinkan kita memilih urutan perhitungan yang paling murah. Untuk matriks berukuran sangat berbeda, urutan kurung dapat mengubah biaya komputasi dari jam menjadi detik.

        Transpos hasil kali membalik urutan: `(A B)^T = B^T A^T`. Sifat ini sering dipakai untuk menyederhanakan turunan dan rumus statistik, jadi baik untuk diingat. Berikut kita periksa semua sifat ini secara numerik.
        """),
        C(
            """
            import numpy as np

            A = np.array([[1, 2], [3, 4]])
            B = np.array([[0, 1], [1, 0]])
            C = np.array([[2, 0], [0, 3]])
            print((A @ B).tolist(), (B @ A).tolist())
            print(np.array_equal(A @ B, B @ A))
            print(np.array_equal((A @ B) @ C, A @ (B @ C)))
            print(np.array_equal(A @ (B + C), A @ B + A @ C))
            print(np.array_equal((A @ B).T, B.T @ A.T))
            """,
            """
            [[2, 1], [4, 3]] [[3, 4], [1, 2]]
            False
            True
            True
            True
            """,
            """
            `A @ B` berbeda dari `B @ A`, tetapi asosiatif, distributif, dan transpos hasil kali membalik urutan.
            """,
            filename="sifat_perkalian.py",
        ),
        T("""
        ## Transformasi dan komposisi

        Matriks bisa dipandang sebagai fungsi yang mengubah vektor. Matriks `A` mengubah `x` menjadi `A x`. Matriks tertentu memutar bidang, matriks lain menskalakan, menggeser miring, atau memantulkan. Misalnya `[[2, 0], [0, 2]]` memperbesar semua vektor dua kali.

        Melakukan dua transformasi berturutan sama dengan mengalikan matriksnya: menerapkan `B` lalu `A` setara dengan `(A B) x`. Perhatikan urutannya dibaca dari kanan ke kiri, karena transformasi pertama yang diterapkan paling dekat dengan vektor. Itulah mengapa perkalian matriks tidak komutatif: memutar lalu menskalakan berbeda dengan menskalakan lalu memutar bila skalanya tidak seragam.

        Jaringan saraf adalah tumpukan transformasi linear yang diselingi fungsi nonlinear. Setiap lapisan adalah satu perkalian matriks, sehingga memahaminya sebagai transformasi membantumu menalar apa yang dilakukan lapisan itu.
        """),
        T("""
        ## Biaya perkalian matriks

        Perkalian dua matriks `n x n` dengan cara dasar membutuhkan sekitar `n` pangkat tiga operasi. Untuk matriks berukuran seribu, itu miliaran operasi, namun pustaka seperti NumPy memanfaatkan perangkat keras dan pustaka teroptimasi sehingga selesai dalam sepersekian detik. Karena itu jangan pernah menulis perkalian matriks dengan tiga perulangan Python untuk data besar.

        Pada matriks panjang dan sempit, urutan kurung ikut menentukan biaya. Menghitung `(A B) x` bisa jauh lebih mahal daripada `A (B x)` karena yang kedua hanya melibatkan perkalian matriks-vektor. Mengatur urutan perkalian adalah optimasi sederhana yang sering menghemat waktu secara dramatis.
        """),
        E(
            "A2-02-2-ex1",
            "mudah",
            """
            Tulis fungsi `matriks_kali_vektor(A, x)` yang mengembalikan hasil kali matriks (list of list) dengan vektor (list) sebagai list.
            """,
            """
            def matriks_kali_vektor(A, x):
                # TODO: implementasikan
                pass
            """,
            """
            assert matriks_kali_vektor([[1, 2, 3], [4, 5, 6]], [1, 0, -1]) == [-2, -2]
            assert matriks_kali_vektor([[1, 0], [0, 1]], [7, 8]) == [7, 8]
            assert matriks_kali_vektor([[2, 2]], [1, 1]) == [4]
            assert matriks_kali_vektor([], [1]) == []
            """,
            "Tiap komponen hasil adalah dot product satu baris dengan x.",
            """
            def matriks_kali_vektor(A, x):
                return [sum(a * b for a, b in zip(baris, x)) for baris in A]
            """,
        ),
        E(
            "A2-02-2-ex2",
            "mudah",
            """
            Tulis fungsi `ukuran_hasil(a, b)` yang menerima ukuran dua matriks sebagai tuple `(baris, kolom)` dan mengembalikan ukuran hasil kali `A B` sebagai tuple, atau `None` bila perkalian tidak terdefinisi.
            """,
            """
            def ukuran_hasil(a, b):
                # TODO: implementasikan
                pass
            """,
            """
            assert ukuran_hasil((3, 2), (2, 5)) == (3, 5)
            assert ukuran_hasil((3, 2), (3, 2)) is None
            assert ukuran_hasil((1, 4), (4, 1)) == (1, 1)
            assert ukuran_hasil((4, 1), (1, 4)) == (4, 4)
            """,
            "Kolom pertama harus sama dengan baris kedua.",
            """
            def ukuran_hasil(a, b):
                if a[1] != b[0]:
                    return None
                return (a[0], b[1])
            """,
        ),
        E(
            "A2-02-2-ex3",
            "sedang",
            """
            Tulis fungsi `kali_matriks(A, B)` yang mengalikan dua matriks (list of list) tanpa NumPy dan mengembalikan matriks hasil. Bila ukuran tidak cocok timbulkan `ValueError`.
            """,
            """
            def kali_matriks(A, B):
                # TODO: implementasikan
                pass
            """,
            """
            assert kali_matriks([[1, 2], [3, 4]], [[0, 1], [1, 0]]) == [[2, 1], [4, 3]]
            assert kali_matriks([[1, 2, 3]], [[1], [1], [1]]) == [[6]]
            assert kali_matriks([[1, 0], [0, 1]], [[5, 6], [7, 8]]) == [[5, 6], [7, 8]]
            try:
                kali_matriks([[1, 2]], [[1, 2]])
            except ValueError:
                pass
            else:
                raise AssertionError("harus error")
            """,
            "Periksa kolom A dan baris B, lalu hitung dot product baris A dengan kolom B (zip(*B)).",
            """
            def kali_matriks(A, B):
                if len(A[0]) != len(B):
                    raise ValueError("ukuran tidak cocok")
                kolom = list(zip(*B))
                return [[sum(a * b for a, b in zip(baris, k)) for k in kolom] for baris in A]
            """,
        ),
        E(
            "A2-02-2-ex4",
            "menantang",
            """
            Tulis fungsi `pangkat_matriks(A, n)` yang menghitung `A` dipangkatkan `n` (bilangan bulat tidak negatif) untuk matriks persegi (list of list) dengan perkalian berulang. Pangkat nol menghasilkan matriks identitas. Gunakan fungsi `kali` yang sudah disediakan.
            """,
            """
            def kali(A, B):
                kolom = list(zip(*B))
                return [[sum(a * b for a, b in zip(baris, k)) for k in kolom] for baris in A]

            def pangkat_matriks(A, n):
                # TODO: implementasikan
                pass
            """,
            """
            assert pangkat_matriks([[1, 1], [1, 0]], 5) == [[8, 5], [5, 3]]
            assert pangkat_matriks([[2, 0], [0, 3]], 3) == [[8, 0], [0, 27]]
            assert pangkat_matriks([[1, 2], [3, 4]], 0) == [[1, 0], [0, 1]]
            assert pangkat_matriks([[1, 2], [3, 4]], 1) == [[1, 2], [3, 4]]
            """,
            "Mulai dari identitas lalu kalikan A sebanyak n kali.",
            """
            def kali(A, B):
                kolom = list(zip(*B))
                return [[sum(a * b for a, b in zip(baris, k)) for k in kolom] for baris in A]

            def pangkat_matriks(A, n):
                m = len(A)
                hasil = [[1 if i == j else 0 for j in range(m)] for i in range(m)]
                for _ in range(n):
                    hasil = kali(hasil, A)
                return hasil
            """,
        ),
    ],
    [
        M("Mengira AB sama dengan BA.", "Perkalian matriks tidak komutatif."),
        M("Mengalikan matriks dengan ukuran dalam berbeda.", "Kolom A harus sama dengan baris B."),
        M("Mencampur * dengan @ pada NumPy.", "* per elemen, @ perkalian matriks."),
    ],
    [
        Q("Ukuran hasil (3 x 2)(2 x 4)?", ["3 x 4", "2 x 2", "4 x 3", "tidak terdefinisi"], 0, "Dua angka dalam hilang, tersisa 3 x 4.", hint="Luar tersisa."),
        Q("Apakah AB selalu sama dengan BA?", ["Ya", "Tidak", "Hanya matriks persegi", "Hanya identitas"], 1, "Perkalian matriks tidak komutatif.", hint="Urutan penting."),
        Q("Komponen y[i] dari A x adalah?", ["Dot product baris i dengan x", "Jumlah kolom", "Norma x", "Transpos"], 0, "Baris ke-i dot x.", hint="Baris dikali vektor."),
        Q("Sifat yang benar untuk transpos hasil kali?", ["(AB)^T = A^T B^T", "(AB)^T = B^T A^T", "(AB)^T = AB", "(AB)^T = BA"], 1, "Urutan terbalik.", hint="Dibalik."),
        Q("Matriks A x dapat dipandang sebagai?", ["Kombinasi linear kolom A", "Baris acak", "Nol", "Jumlah semua elemen"], 0, "Bobot adalah komponen x.", hint="Kolom berbobot."),
    ],
    [
        "A x adalah dot product tiap baris dengan x atau kombinasi linear kolom.",
        "Perkalian matriks butuh kolom A sama dengan baris B dan menghasilkan m x p.",
        "Perkalian tidak komutatif tetapi asosiatif dan distributif.",
        "Matriks adalah transformasi dan perkaliannya adalah komposisi.",
    ],
    [],
)

l3 = lesson(
    "A2-02-3",
    "Matriks khusus dan kegunaannya",
    35,
    [
        "Mengenali matriks identitas, nol, diagonal, dan segitiga",
        "Memahami matriks simetris dan contohnya dalam statistik",
        "Memahami matriks ortogonal dan sifat menjaga panjang",
        "Menghitung matriks kovariansi dan matriks jarak sebagai penerapan",
    ],
    [
        T("""
        ## Matriks identitas dan diagonal

        **Matriks identitas** `I` adalah matriks persegi dengan angka satu di diagonal utama dan nol di tempat lain. Ia berperan seperti angka satu dalam perkalian: `I A = A I = A` untuk matriks `A` yang ukurannya cocok, dan `I x = x` untuk vektor mana pun. Di NumPy, `np.eye(n)` membuatnya.

        **Matriks diagonal** hanya memiliki elemen tak nol di diagonal utama. Perkalian dengan matriks diagonal sangat sederhana: mengalikan dari kiri menskalakan baris, mengalikan dari kanan menskalakan kolom. Menyimpan matriks diagonal cukup dengan vektor diagonalnya, sangat hemat memori. Banyak dekomposisi matriks, termasuk eigen dan SVD, menghasilkan matriks diagonal.

        **Matriks nol** semua elemennya nol dan berperan seperti angka nol dalam penjumlahan. Matriks **segitiga atas** dan **segitiga bawah** memiliki elemen nol di bawah atau di atas diagonal, dan sistem persamaan dengan matriks seperti ini sangat mudah diselesaikan.
        """),
        C(
            """
            import numpy as np

            I = np.eye(3)
            A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 10]])
            print(np.array_equal(I @ A, A), np.array_equal(A @ I, A))
            x = np.array([5, 6, 7])
            print((I @ x).tolist())

            D = np.diag([2, 3, 4])
            print(D.tolist())
            print((D @ A).tolist())
            print((A @ D).tolist())
            print(np.triu(A).tolist())
            print(np.diag(A).tolist())
            """,
            """
            True True
            [5.0, 6.0, 7.0]
            [[2, 0, 0], [0, 3, 0], [0, 0, 4]]
            [[2, 4, 6], [12, 15, 18], [28, 32, 40]]
            [[2, 6, 12], [8, 15, 24], [14, 24, 40]]
            [[1, 2, 3], [0, 5, 6], [0, 0, 10]]
            [1, 5, 10]
            """,
            """
            Identitas tidak mengubah apa pun. Perkalian diagonal dari kiri menskalakan baris, dari kanan menskalakan kolom. `np.triu` mengambil segitiga atas.
            """,
            filename="matriks_khusus.py",
        ),
        T("""
        ## Matriks simetris

        Matriks persegi `A` disebut **simetris** bila `A = A^T`, artinya elemen `A[i, j]` sama dengan `A[j, i]`. Simetris berarti cermin terhadap diagonal utama. Matriks seperti ini sangat penting karena muncul alami dalam statistik: matriks kovariansi, matriks korelasi, dan matriks jarak semuanya simetris.

        Matriks simetris memiliki sifat bagus yang akan kamu manfaatkan pada pelajaran eigenvalue: semua eigenvalue-nya real, dan eigenvector untuk eigenvalue berbeda saling ortogonal. Karena itu algoritma khusus untuk matriks simetris lebih cepat dan lebih stabil.

        Salah satu cara menghasilkan matriks simetris adalah `X^T X` untuk matriks `X` apa pun. Alasannya: `(X^T X)^T = X^T (X^T)^T = X^T X`. Pola ini muncul terus dalam regresi dan PCA. Dengan memeriksa `np.allclose(A, A.T)` kamu dapat menguji kesimetrisan numerik.
        """),
        C(
            """
            import numpy as np

            S = np.array([[2, 1, 0], [1, 3, 4], [0, 4, 5]])
            print(np.array_equal(S, S.T))
            X = np.array([[1.0, 2.0], [3.0, 5.0], [4.0, 1.0]])
            G = X.T @ X
            print(G.tolist(), np.allclose(G, G.T))
            nilai = np.linalg.eigvalsh(G)
            print(nilai.round(4).tolist())
            tidak = np.array([[1, 2], [3, 4]])
            print(np.allclose(tidak, tidak.T))
            """,
            """
            True
            [[26.0, 21.0], [21.0, 30.0]]
            True
            [6.905, 49.095]
            False
            """,
            """
            `X.T @ X` selalu simetris. Matriks simetris memiliki eigenvalue real sehingga `eigvalsh` bekerja.
            """,
            filename="matriks_simetris.py",
        ),
        K(
            "tip",
            """
            Karena galat pembulatan, uji kesimetrisan dengan `np.allclose(A, A.T)` dan bukan `np.array_equal`, kecuali untuk matriks bilangan bulat.
            """,
            title="Uji simetris yang aman",
        ),
        T("""
        ## Matriks ortogonal

        Matriks persegi `Q` disebut **ortogonal** bila kolom-kolomnya saling tegak lurus dan masing-masing berpanjang satu. Ciri utamanya: `Q^T Q = I`, sehingga transposnya sekaligus inversnya. Ini luar biasa praktis, sebab membalik transformasi cukup dengan mentranspos, tanpa komputasi mahal.

        Matriks ortogonal **menjaga panjang dan sudut**: `||Q x|| = ||x||` dan dot product tidak berubah. Secara geometris ia hanya merepresentasikan rotasi atau pemantulan, tanpa meregangkan atau memampatkan ruang. Karena itu transformasi ortogonal stabil secara numerik dan sering dipakai untuk menghindari galat yang membesar.

        Contoh paling dikenal adalah matriks rotasi dua dimensi. Hasil dekomposisi seperti QR, eigen untuk matriks simetris, dan SVD semuanya menghasilkan matriks ortogonal, yang menjadi alasan utama kamu perlu mengenalnya baik-baik.
        """),
        C(
            """
            import numpy as np

            t = np.pi / 6
            Q = np.array([[np.cos(t), -np.sin(t)],
                          [np.sin(t),  np.cos(t)]])
            print(np.allclose(Q.T @ Q, np.eye(2)))
            x = np.array([3.0, 4.0])
            print(round(float(np.linalg.norm(Q @ x)), 6), np.linalg.norm(x))
            y = np.array([1.0, 2.0])
            print(round(float((Q @ x) @ (Q @ y)), 6), x @ y)
            print(np.allclose(np.linalg.inv(Q), Q.T))
            R = np.array([[0, 1], [1, 0]])
            print((R @ np.array([2, 7])).tolist())
            """,
            """
            True
            5.0 5.0
            11.0 11.0
            True
            [7, 2]
            """,
            """
            Matriks rotasi ortogonal menjaga panjang dan dot product, dan inversnya sama dengan transposnya. Matriks permutasi memantulkan, yaitu menukar komponen.
            """,
            filename="matriks_ortogonal.py",
        ),
        T("""
        ## Penerapan: kovariansi dan jarak

        Dua penerapan klasik memperlihatkan semua yang kamu pelajari. Pertama, **matriks kovariansi** data `X` (ukuran `n x p`) setelah dipusatkan adalah `X^T X / (n - 1)`. Hasilnya `p x p`, simetris, dengan varians fitur di diagonal dan kovarians antar fitur di luar diagonal. Matriks ini adalah bahan utama PCA.

        Kedua, **matriks jarak**: untuk `n` titik, matriks `n x n` di mana elemen `(i, j)` adalah jarak titik `i` ke titik `j`. Matriks ini simetris dengan nol di diagonal. Ia dipakai pada pengelompokan hierarkis dan banyak algoritma kemiripan.

        Kedua contoh menunjukkan polanya: ubah data menjadi matriks, lakukan perkalian dan transpos, dan hasilnya adalah matriks khusus dengan sifat bagus yang bisa dimanfaatkan. Latihan berikut membangun keduanya dari nol.
        """),
        T("""
        ## Memilih struktur yang tepat untuk efisiensi

        Mengetahui bahwa sebuah matriks diagonal, simetris, atau jarang membuka penghematan besar. Matriks diagonal cukup disimpan sebagai vektor dan perkaliannya menjadi perkalian per elemen. Matriks jarang, yang hampir seluruh elemennya nol seperti matriks hitungan kata, disimpan hanya pada elemen tak nol dengan pustaka `scipy.sparse`, sehingga hemat memori ribuan kali lipat.

        Bila kamu mengenali struktur matriks, kamu dapat memakai algoritma khusus yang lebih cepat dan lebih stabil. Karena itu, sebelum menjalankan operasi mahal pada matriks besar, tanyakan dulu apakah ia punya struktur yang bisa dimanfaatkan.
        """),
        E(
            "A2-02-3-ex1",
            "mudah",
            """
            Tulis fungsi `identitas(n)` yang mengembalikan matriks identitas `n x n` sebagai list of list. Untuk `n = 0` kembalikan list kosong.
            """,
            """
            def identitas(n):
                # TODO: implementasikan
                pass
            """,
            """
            assert identitas(2) == [[1, 0], [0, 1]]
            assert identitas(1) == [[1]]
            assert identitas(0) == []
            assert identitas(3)[1] == [0, 1, 0]
            """,
            "Elemen bernilai 1 bila indeks baris sama dengan indeks kolom.",
            """
            def identitas(n):
                return [[1 if i == j else 0 for j in range(n)] for i in range(n)]
            """,
        ),
        E(
            "A2-02-3-ex2",
            "mudah",
            """
            Tulis fungsi `simetris(A)` yang mengembalikan `True` bila matriks persegi (list of list) simetris.
            """,
            """
            def simetris(A):
                # TODO: implementasikan
                pass
            """,
            """
            assert simetris([[1, 2], [2, 3]]) is True
            assert simetris([[1, 2], [3, 4]]) is False
            assert simetris([[5]]) is True
            assert simetris([]) is True
            """,
            "Bandingkan A dengan transposnya.",
            """
            def simetris(A):
                return [list(k) for k in zip(*A)] == [list(b) for b in A]
            """,
        ),
        E(
            "A2-02-3-ex3",
            "sedang",
            """
            Tulis fungsi `kovariansi(X)` yang menerima matriks data `X` (list of list dengan `n >= 2` baris pengamatan dan `p` kolom fitur) dan mengembalikan matriks kovariansi sampel `p x p` dengan nilai dibulatkan 4 desimal.
            """,
            """
            def kovariansi(X):
                # TODO: implementasikan
                pass
            """,
            """
            assert kovariansi([[1, 2], [3, 4], [5, 6]]) == [[4.0, 4.0], [4.0, 4.0]]
            assert kovariansi([[1, 0], [2, 0]]) == [[0.5, 0.0], [0.0, 0.0]]
            r = kovariansi([[1, 2], [2, 1], [3, 3], [4, 6]])
            assert r == [[1.6667, 2.3333], [2.3333, 4.6667]]
            assert r[0][1] == r[1][0]
            """,
            "Pusatkan tiap kolom lalu hitung dot product antar kolom dibagi n - 1.",
            """
            def kovariansi(X):
                n = len(X)
                kolom = list(zip(*X))
                pusat = [[x - sum(k) / n for x in k] for k in kolom]
                p = len(pusat)
                return [[round(sum(a * b for a, b in zip(pusat[i], pusat[j])) / (n - 1), 4) for j in range(p)] for i in range(p)]
            """,
        ),
        E(
            "A2-02-3-ex4",
            "menantang",
            """
            Tulis fungsi `matriks_jarak(titik)` yang menerima list titik (vektor) dan mengembalikan matriks jarak Euclid `n x n` dengan nilai dibulatkan 4 desimal. Diagonalnya nol dan matriks simetris.
            """,
            """
            def matriks_jarak(titik):
                # TODO: implementasikan
                pass
            """,
            """
            r = matriks_jarak([[0, 0], [3, 4], [6, 8]])
            assert r == [[0.0, 5.0, 10.0], [5.0, 0.0, 5.0], [10.0, 5.0, 0.0]]
            assert matriks_jarak([[1, 1]]) == [[0.0]]
            assert matriks_jarak([]) == []
            r2 = matriks_jarak([[0, 0], [1, 1]])
            assert r2[0][1] == r2[1][0] == 1.4142
            """,
            "Dua perulangan bersarang, jarak dari akar jumlah kuadrat selisih.",
            """
            def matriks_jarak(titik):
                def jarak(a, b):
                    return round(sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5, 4)
                return [[jarak(a, b) for b in titik] for a in titik]
            """,
        ),
    ],
    [
        M("Membalik matriks ortogonal dengan inversi mahal.", "Cukup transpos."),
        M("Menguji kesimetrisan float dengan kesamaan persis.", "Pakai np.allclose."),
        M("Lupa memusatkan data sebelum menghitung kovariansi.", "Kurangkan rata-rata kolom lebih dulu."),
    ],
    [
        Q("Apa sifat I A?", ["Nol", "Sama dengan A", "Transpos A", "Invers A"], 1, "Identitas tidak mengubah matriks.", hint="Seperti angka 1."),
        Q("Matriks simetris memenuhi?", ["A = -A", "A = A^T", "A = A^-1", "A = I"], 1, "Sama dengan transposnya.", hint="Cermin diagonal."),
        Q("Sifat utama matriks ortogonal?", ["Memperbesar vektor", "Menjaga panjang vektor", "Selalu diagonal", "Selalu nol"], 1, "Rotasi atau pemantulan murni.", hint="Panjang tetap."),
        Q("Invers matriks ortogonal adalah?", ["Dirinya", "Transposnya", "Negatifnya", "Tidak ada"], 1, "Q^T Q = I.", hint="Mudah dihitung."),
        Q("Ukuran matriks kovariansi untuk p fitur?", ["n x n", "p x p", "n x p", "1 x p"], 1, "Persegi sebesar jumlah fitur.", hint="Fitur lawan fitur."),
    ],
    [
        "Identitas, diagonal, dan segitiga adalah matriks khusus yang menyederhanakan perhitungan.",
        "Matriks simetris muncul dalam kovariansi dan jarak, dan X^T X selalu simetris.",
        "Matriks ortogonal menjaga panjang dan inversnya adalah transposnya.",
        "Kovariansi dan matriks jarak dibangun dari perkalian dan transpos.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa perhitungan dan contoh kode yang cukup jelas dalam teks.", "brief": []}

write_module(
    "A2",
    2,
    "Matriks dan operasi dasar",
    105,
    [
        "Mengoperasikan matriks dengan penjumlahan, transpos, dan perkalian",
        "Menafsirkan matriks sebagai transformasi dan data",
        "Mengenali matriks khusus dan memakainya dalam kovariansi dan jarak",
    ],
    [l1, l2, l3],
    video,
    REF,
)
