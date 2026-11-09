import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

l1 = lesson(
    "A2-03-1",
    "Sistem persamaan linear dan bentuk matriks",
    35,
    [
        "Menulis sistem persamaan linear dalam bentuk matriks A x = b",
        "Menafsirkan solusi secara geometris sebagai perpotongan garis atau bidang",
        "Membedakan sistem dengan solusi tunggal, tak hingga, dan tanpa solusi",
        "Menyelesaikan sistem kecil dengan np.linalg.solve",
    ],
    [
        T("""
        ## Dari persamaan ke matriks

        **Sistem persamaan linear** adalah sekumpulan persamaan dengan beberapa variabel yang semuanya berpangkat satu. Contoh: `2x + y = 5` dan `x - y = 1`. Kita mencari nilai `x` dan `y` yang memenuhi semua persamaan sekaligus. Sistem seperti ini muncul di mana-mana: menyeimbangkan anggaran, menghitung aliran jaringan, hingga mencari bobot regresi.

        Semua sistem linear dapat ditulis dalam satu bentuk ringkas `A x = b`. Matriks `A` berisi koefisien, vektor `x` berisi variabel yang dicari, dan vektor `b` berisi sisi kanan. Untuk contoh tadi, `A = [[2, 1], [1, -1]]`, `x = [x, y]`, dan `b = [5, 1]`. Bentuk ini memungkinkan kita memakai seluruh alat aljabar linear, bukan sekadar trik per kasus.

        Menulis sistem sebagai `A x = b` juga menghubungkan ke pelajaran sebelumnya: `A x` adalah kombinasi linear kolom `A`, sehingga mencari `x` berarti mencari bobot yang membentuk `b` dari kolom-kolom itu.
        """),
        C(
            """
            import numpy as np

            A = np.array([[2.0, 1.0], [1.0, -1.0]])
            b = np.array([5.0, 1.0])
            x = np.linalg.solve(A, b)
            print(x.tolist())
            print((A @ x).tolist(), np.allclose(A @ x, b))
            kombinasi = x[0] * A[:, 0] + x[1] * A[:, 1]
            print(kombinasi.tolist())
            """,
            """
            [2.0, 1.0]
            [5.0, 1.0] True
            [5.0, 1.0]
            """,
            """
            `np.linalg.solve` menyelesaikan `A x = b`. Solusi diperiksa dengan mengalikan kembali, dan `b` adalah kombinasi linear kolom `A` berbobot solusi.
            """,
            filename="solve_dasar.py",
        ),
        T("""
        ## Tafsir geometris

        Setiap persamaan linear dua variabel menggambarkan sebuah garis di bidang. Solusi sistem adalah titik yang berada di semua garis, yaitu titik perpotongan. Untuk tiga variabel, tiap persamaan adalah bidang, dan solusinya adalah titik tempat bidang-bidang itu bertemu.

        Dari gambaran ini ada tiga kemungkinan untuk dua garis. Garis berpotongan di satu titik, artinya **solusi tunggal**. Garis sejajar dan berbeda, artinya **tidak ada solusi**. Garis berimpit, artinya **solusi tak hingga** karena setiap titik pada garis itu memenuhi kedua persamaan. Tidak pernah ada tepat dua atau tiga solusi: bila ada lebih dari satu, maka ada tak hingga.

        Pandangan kolom memberi tafsir lain. Sistem punya solusi bila dan hanya bila `b` terletak pada span kolom-kolom `A`. Bila `b` di luar span, tidak ada kombinasi linear yang menghasilkannya, sehingga sistem tak punya solusi.
        """),
        C(
            """
            import numpy as np

            tunggal = np.array([[1.0, 1.0], [1.0, -1.0]])
            sejajar = np.array([[1.0, 1.0], [2.0, 2.0]])
            print(round(float(np.linalg.det(tunggal)), 4), round(float(np.linalg.det(sejajar)), 4))
            print(np.linalg.matrix_rank(tunggal), np.linalg.matrix_rank(sejajar))
            try:
                np.linalg.solve(sejajar, np.array([2.0, 5.0]))
            except np.linalg.LinAlgError:
                print("matriks singular")
            aug_a = np.column_stack([sejajar, [2.0, 4.0]])
            aug_b = np.column_stack([sejajar, [2.0, 5.0]])
            print(np.linalg.matrix_rank(aug_a), np.linalg.matrix_rank(aug_b))
            """,
            """
            -2.0 0.0
            2 1
            matriks singular
            1 2
            """,
            """
            Determinan nol dan peringkat kurang dari penuh menandakan garis sejajar atau berimpit. Matriks augmented dengan peringkat sama menandakan solusi ada, dan peringkat lebih besar berarti tidak ada solusi.
            """,
            filename="jenis_solusi.py",
        ),
        K(
            "tip",
            """
            Sistem `A x = b` dengan `A` persegi punya solusi tunggal bila peringkat `A` sama dengan jumlah variabel. Bila peringkatnya lebih kecil, solusinya nol atau tak hingga, tergantung `b`.
            """,
            title="Peringkat menentukan jenis solusi",
        ),
        T("""
        ## Banyak persamaan, banyak variabel

        Jumlah persamaan tidak harus sama dengan jumlah variabel. Bila persamaan lebih banyak daripada variabel, sistem disebut **overdetermined**, dan umumnya tidak ada solusi persis. Inilah situasi regresi: banyak pengamatan, sedikit parameter. Kita lalu mencari solusi terbaik dalam arti kuadrat terkecil, topik yang dibahas pada modul berikutnya.

        Bila persamaan lebih sedikit daripada variabel, sistem **underdetermined**, dan umumnya ada tak hingga solusi. Kondisi ini muncul pada model dengan fitur lebih banyak daripada data, dan menjadi alasan teknik regularisasi dibutuhkan untuk memilih satu solusi di antara banyak yang mungkin.

        Pembedaan ini penting dalam praktik. Pustaka seperti scikit-learn menyelesaikan masalah overdetermined lewat kuadrat terkecil secara otomatis, tetapi memahami asal usulnya membantumu mendiagnosis mengapa sebuah model gagal atau tidak stabil.
        """),
        C(
            """
            import numpy as np

            A = np.array([[1.0, 1.0], [1.0, 2.0], [1.0, 3.0]])
            b = np.array([1.0, 2.0, 2.0])
            x, sisa, peringkat, sv = np.linalg.lstsq(A, b, rcond=None)
            print(x.round(4).tolist(), peringkat)
            print((A @ x).round(4).tolist())
            print(np.allclose(A @ x, b))
            """,
            """
            [0.6667, 0.5] 2
            [1.1667, 1.6667, 2.1667]
            False
            """,
            """
            Tiga persamaan dua variabel tidak punya solusi persis. `lstsq` memberi solusi terbaik dalam arti kuadrat terkecil, dan hasil kali tidak tepat sama dengan `b`.
            """,
            filename="overdetermined.py",
        ),
        T("""
        ## Kondisi dan ketelitian numerik

        Sistem bisa punya solusi tunggal secara teori tetapi sangat sulit dihitung dengan akurat. Bila baris-baris `A` hampir sejajar, perubahan kecil pada `b` dapat menyebabkan perubahan besar pada solusi. Matriks seperti ini disebut **berkondisi buruk**. Ukurannya adalah **bilangan kondisi**, yang diperoleh dengan `np.linalg.cond(A)`. Bilangan kondisi yang sangat besar memperingatkan bahwa hasil mungkin tidak dapat dipercaya.

        Dalam praktik data, kondisi buruk muncul ketika fitur-fitur sangat berkorelasi, sehingga kolom `X` hampir bergantung linear. Gejalanya: koefisien regresi meloncat tak masuk akal antar sampel data. Mengenali masalah ini lebih awal menghindarkan kesimpulan keliru.

        Satu prinsip penting: jangan pernah menghitung invers matriks lalu mengalikannya untuk menyelesaikan sistem. Gunakan `np.linalg.solve`, yang lebih cepat dan jauh lebih akurat secara numerik.
        """),
        T("""
        ## Ringkasan pemilihan alat

        Untuk sistem kecil dan persegi dengan solusi tunggal, `np.linalg.solve` adalah pilihan utama. Untuk sistem dengan lebih banyak persamaan daripada variabel, pakai `np.linalg.lstsq`. Untuk memeriksa apakah sistem punya solusi tunggal, lihat peringkat dan bilangan kondisi. Pilihan alat yang tepat sejak awal menghemat banyak waktu debugging.
        """),
        E(
            "A2-03-1-ex1",
            "mudah",
            """
            Tulis fungsi `ke_matriks(persamaan)` yang menerima list tuple `(a, b, c)` untuk persamaan `a x + b y = c` dan mengembalikan tuple `(A, rhs)` dengan `A` list of list koefisien dan `rhs` list sisi kanan.
            """,
            """
            def ke_matriks(persamaan):
                # TODO: implementasikan
                pass
            """,
            """
            assert ke_matriks([(2, 1, 5), (1, -1, 1)]) == ([[2, 1], [1, -1]], [5, 1])
            assert ke_matriks([(3, 4, 7)]) == ([[3, 4]], [7])
            assert ke_matriks([]) == ([], [])
            assert ke_matriks([(0, 1, 0), (1, 0, 0)]) == ([[0, 1], [1, 0]], [0, 0])
            """,
            "Pisahkan dua koefisien pertama dari elemen ketiga di tiap tuple.",
            """
            def ke_matriks(persamaan):
                return [[a, b] for a, b, _ in persamaan], [c for _, _, c in persamaan]
            """,
        ),
        E(
            "A2-03-1-ex2",
            "mudah",
            """
            Tulis fungsi `penuhi(A, x, b)` yang mengembalikan `True` bila `A x` sama dengan `b` (toleransi 1e-9) untuk `A` list of list, `x` dan `b` list.
            """,
            """
            def penuhi(A, x, b):
                # TODO: implementasikan
                pass
            """,
            """
            assert penuhi([[2, 1], [1, -1]], [2, 1], [5, 1]) is True
            assert penuhi([[2, 1], [1, -1]], [1, 1], [5, 1]) is False
            assert penuhi([[1, 0], [0, 1]], [3, 4], [3, 4]) is True
            assert penuhi([[0.1, 0.2]], [1, 1], [0.3]) is True
            """,
            "Hitung dot product tiap baris dengan x lalu bandingkan dengan toleransi.",
            """
            def penuhi(A, x, b):
                hasil = [sum(a * v for a, v in zip(baris, x)) for baris in A]
                return all(abs(h - t) < 1e-9 for h, t in zip(hasil, b))
            """,
        ),
        E(
            "A2-03-1-ex3",
            "sedang",
            """
            Tulis fungsi `selesaikan_2x2(a, b, c, d, e, f)` yang menyelesaikan sistem `a x + b y = e` dan `c x + d y = f` dengan aturan Cramer. Kembalikan tuple `(x, y)` dibulatkan 6 desimal, atau `None` bila determinan nol.
            """,
            """
            def selesaikan_2x2(a, b, c, d, e, f):
                # TODO: implementasikan
                pass
            """,
            """
            assert selesaikan_2x2(2, 1, 1, -1, 5, 1) == (2.0, 1.0)
            assert selesaikan_2x2(1, 1, 2, 2, 2, 4) is None
            assert selesaikan_2x2(1, 0, 0, 1, 3, 4) == (3.0, 4.0)
            assert selesaikan_2x2(3, 2, 1, 4, 7, 9) == (1.0, 2.0)
            """,
            "Determinan adalah a d dikurangi b c. x dan y diperoleh dari rasio determinan.",
            """
            def selesaikan_2x2(a, b, c, d, e, f):
                det = a * d - b * c
                if det == 0:
                    return None
                x = (e * d - b * f) / det
                y = (a * f - e * c) / det
                return round(x, 6), round(y, 6)
            """,
        ),
        E(
            "A2-03-1-ex4",
            "menantang",
            """
            Tulis fungsi `jenis_solusi(A, b)` untuk sistem 2x2 dengan `A` list of list dan `b` list. Kembalikan `"tunggal"` bila determinan tak nol. Bila determinan nol, kembalikan `"tak hingga"` bila `b` konsisten (baris kedua kelipatan baris pertama berikut sisi kanannya) dan `"tidak ada"` bila tidak. Anggap baris pertama tidak semuanya nol.
            """,
            """
            def jenis_solusi(A, b):
                # TODO: implementasikan
                pass
            """,
            """
            assert jenis_solusi([[2, 1], [1, -1]], [5, 1]) == "tunggal"
            assert jenis_solusi([[1, 1], [2, 2]], [2, 4]) == "tak hingga"
            assert jenis_solusi([[1, 1], [2, 2]], [2, 5]) == "tidak ada"
            assert jenis_solusi([[1, 2], [3, 6]], [1, 3]) == "tak hingga"
            """,
            "Bila determinan nol, cari kelipatan baris kedua terhadap baris pertama dan periksa sisi kanan.",
            """
            def jenis_solusi(A, b):
                (a, bb), (c, d) = A
                if a * d - bb * c != 0:
                    return "tunggal"
                if a != 0:
                    k = c / a
                else:
                    k = d / bb
                return "tak hingga" if abs(k * b[0] - b[1]) < 1e-9 else "tidak ada"
            """,
        ),
    ],
    [
        M("Menyelesaikan sistem dengan menghitung invers lalu mengalikan.", "Pakai np.linalg.solve yang lebih akurat dan cepat."),
        M("Mengira sistem singular punya solusi tunggal.", "Periksa determinan dan peringkat."),
        M("Mengabaikan bilangan kondisi yang besar.", "Waspadai hasil dan periksa korelasi antar fitur."),
    ],
    [
        Q("Bentuk matriks sistem persamaan linear?", ["A + x = b", "A x = b", "A / x = b", "A^x = b"], 1, "Koefisien dikali variabel sama dengan sisi kanan.", hint="Perkalian matriks."),
        Q("Dua garis sejajar berbeda menghasilkan?", ["Solusi tunggal", "Tak ada solusi", "Tak hingga solusi", "Dua solusi"], 1, "Tidak ada titik perpotongan.", hint="Tidak pernah bertemu."),
        Q("Sistem lebih banyak persamaan daripada variabel disebut?", ["Underdetermined", "Overdetermined", "Homogen", "Diagonal"], 1, "Biasanya tak ada solusi persis.", hint="Situasi regresi."),
        Q("Fungsi NumPy untuk solusi kuadrat terkecil?", ["np.solve", "np.linalg.lstsq", "np.fit", "np.lsq"], 1, "lstsq memberi solusi terbaik.", hint="Least squares."),
        Q("Apa yang ditunjukkan bilangan kondisi besar?", ["Solusi akurat", "Sistem sensitif dan hasil bisa tak andal", "Sistem diagonal", "Tak ada apa-apa"], 1, "Perubahan kecil memicu perubahan besar.", hint="Kondisi buruk."),
    ],
    [
        "Sistem linear ditulis A x = b dan b adalah kombinasi linear kolom A.",
        "Solusi bisa tunggal, tak hingga, atau tak ada tergantung geometri dan peringkat.",
        "Overdetermined dan underdetermined adalah dua kondisi umum dalam data.",
        "Pakai solve, bukan invers, dan waspadai bilangan kondisi.",
    ],
    [],
)

l2 = lesson(
    "A2-03-2",
    "Eliminasi Gauss",
    35,
    [
        "Menjalankan operasi baris elementer pada matriks augmented",
        "Menerapkan eliminasi maju dan substitusi mundur",
        "Memakai pivoting sebagian untuk menjaga kestabilan numerik",
        "Mengimplementasikan solver Gauss dari nol dan membandingkannya dengan NumPy",
    ],
    [
        T("""
        ## Ide eliminasi

        **Eliminasi Gauss** adalah algoritma sistematis untuk menyelesaikan `A x = b`. Idenya: ubah sistem menjadi bentuk segitiga yang mudah diselesaikan tanpa mengubah solusinya. Kita memakai tiga **operasi baris elementer**: menukar dua baris, mengalikan satu baris dengan bilangan tak nol, dan menambahkan kelipatan satu baris ke baris lain. Ketiganya tidak mengubah himpunan solusi.

        Kita bekerja pada **matriks augmented** `[A | b]`, yaitu `A` dengan `b` ditempelkan sebagai kolom terakhir. Dengan begitu setiap operasi baris otomatis berlaku untuk sisi kanan juga. Tujuannya membuat semua elemen di bawah diagonal menjadi nol, yang disebut bentuk eselon baris.

        Setelah segitiga, sistem diselesaikan dengan **substitusi mundur**: variabel terakhir langsung terbaca, lalu dimasukkan ke persamaan di atasnya, dan seterusnya naik. Algoritma ini sama dengan yang dijalankan di balik `np.linalg.solve`, dengan tambahan optimasi.
        """),
        C(
            """
            import numpy as np

            M = np.array([[2.0, 1.0, -1.0, 8.0],
                          [-3.0, -1.0, 2.0, -11.0],
                          [-2.0, 1.0, 2.0, -3.0]])
            M[1] = M[1] + 1.5 * M[0]
            M[2] = M[2] + 1.0 * M[0]
            print(M.round(4).tolist())
            M[2] = M[2] - 4.0 * M[1]
            print(M.round(4).tolist())
            z = M[2, 3] / M[2, 2]
            y = (M[1, 3] - M[1, 2] * z) / M[1, 1]
            x = (M[0, 3] - M[0, 1] * y - M[0, 2] * z) / M[0, 0]
            print(round(x, 4), round(y, 4), round(z, 4))
            """,
            """
            [[2.0, 1.0, -1.0, 8.0], [0.0, 0.5, 0.5, 1.0], [0.0, 2.0, 1.0, 5.0]]
            [[2.0, 1.0, -1.0, 8.0], [0.0, 0.5, 0.5, 1.0], [0.0, 0.0, -1.0, 1.0]]
            2.0 3.0 -1.0
            """,
            """
            Dua langkah eliminasi mengubah sistem tiga persamaan menjadi segitiga atas. Substitusi mundur lalu memberi `x`, `y`, dan `z` dari bawah ke atas.
            """,
            filename="gauss_manual.py",
        ),
        T("""
        ## Pivoting

        Elemen diagonal yang dipakai untuk menghilangkan elemen di bawahnya disebut **pivot**. Bila pivot nol, pembagian tidak mungkin, sehingga kita harus menukar baris dengan baris di bawahnya yang elemen kolomnya tak nol. Namun bahkan pivot yang sangat kecil berbahaya: membagi dengan bilangan hampir nol membesarkan galat pembulatan.

        Solusinya adalah **pivoting sebagian**: pada setiap langkah, pilih baris dengan elemen terbesar secara mutlak di kolom itu dan tukar ke posisi pivot. Strategi ini menjaga pengali tetap kecil dan hasil stabil. Hampir semua implementasi nyata memakainya.

        Contoh klasik: sistem dengan pivot `0.0001` memberi hasil salah bila dihitung tanpa menukar baris, padahal dengan pivoting hasilnya akurat. Perbedaan ini bukan teori semata, ia nyata pada data berskala campuran.
        """),
        C(
            """
            import numpy as np

            def gauss(A, b, pivot=True):
                M = np.column_stack([np.array(A, float), np.array(b, float)])
                n = len(M)
                for k in range(n):
                    if pivot:
                        p = k + int(np.argmax(np.abs(M[k:, k])))
                        M[[k, p]] = M[[p, k]]
                    for i in range(k + 1, n):
                        M[i] -= (M[i, k] / M[k, k]) * M[k]
                x = np.zeros(n)
                for i in range(n - 1, -1, -1):
                    x[i] = (M[i, n] - M[i, i + 1:n] @ x[i + 1:]) / M[i, i]
                return x

            A = [[1e-17, 1.0], [1.0, 1.0]]
            b = [1.0, 2.0]
            print(gauss(A, b, pivot=False).round(3).tolist())
            print(gauss(A, b, pivot=True).round(3).tolist())
            print(np.linalg.solve(np.array(A), np.array(b)).round(3).tolist())
            """,
            """
            [0.0, 1.0]
            [1.0, 1.0]
            [1.0, 1.0]
            """,
            """
            Tanpa pivoting pivot sangat kecil menghasilkan jawaban keliru untuk `x`. Dengan pivoting hasilnya cocok dengan `np.linalg.solve`.
            """,
            filename="pivoting.py",
        ),
        K(
            "warning",
            """
            Jangan menulis eliminasi Gauss tanpa pivoting untuk dipakai pada data nyata. Pivot kecil membesarkan galat pembulatan dan bisa menghasilkan jawaban yang salah total.
            """,
            title="Selalu pakai pivoting",
        ),
        T("""
        ## Biaya dan penggunaan ulang

        Eliminasi Gauss untuk matriks `n x n` membutuhkan sekitar dua pertiga `n` pangkat tiga operasi. Untuk seribu variabel itu sekitar enam ratus juta operasi, wajar untuk komputer modern. Bagian terbesar biayanya ada pada tahap eliminasi, sedangkan substitusi mundur hanya sekitar `n` kuadrat.

        Bila kamu perlu menyelesaikan banyak sistem dengan `A` yang sama tetapi `b` berbeda, mengulang eliminasi setiap kali boros. Dekomposisi **LU** menyimpan hasil eliminasi sebagai dua matriks segitiga, sehingga tiap `b` baru hanya butuh dua substitusi murah. Pustaka `scipy.linalg.lu_factor` dan `lu_solve` menyediakannya.

        Pola ini umum dalam komputasi ilmiah: lakukan pekerjaan mahal sekali, simpan hasil, dan pakai ulang. Ide serupa muncul pada dekomposisi Cholesky untuk matriks simetris positif definit yang sering dijumpai dalam statistik.
        """),
        T("""
        ## Mengecek solver sendiri

        Setelah menulis solver sendiri, bandingkan hasilnya dengan `np.linalg.solve` pada banyak sistem acak. Bila keduanya selalu cocok dalam toleransi kecil, implementasimu hampir pasti benar. Teknik membandingkan dengan implementasi acuan ini sangat berguna untuk semua algoritma numerik yang kamu tulis, sebab bug halus mudah lolos dari satu atau dua contoh tangan.

        Gunakan benih acak tetap agar pengujian dapat diulang. Bila pernah gagal, simpan sistem yang menyebabkan kegagalan sebagai kasus uji permanen. Kebiasaan ini mengubah setiap bug yang ditemukan menjadi perlindungan di masa depan.
        """),
        C(
            """
            import numpy as np

            def gauss(A, b):
                M = np.column_stack([np.array(A, float), np.array(b, float)])
                n = len(M)
                for k in range(n):
                    p = k + int(np.argmax(np.abs(M[k:, k])))
                    M[[k, p]] = M[[p, k]]
                    for i in range(k + 1, n):
                        M[i] -= (M[i, k] / M[k, k]) * M[k]
                x = np.zeros(n)
                for i in range(n - 1, -1, -1):
                    x[i] = (M[i, n] - M[i, i + 1:n] @ x[i + 1:]) / M[i, i]
                return x

            rng = np.random.default_rng(0)
            cocok = 0
            for _ in range(50):
                n = int(rng.integers(2, 7))
                A = rng.normal(size=(n, n))
                b = rng.normal(size=n)
                if np.allclose(gauss(A, b), np.linalg.solve(A, b)):
                    cocok += 1
            print(cocok)
            """,
            """
            50
            """,
            """
            Solver buatan sendiri dibandingkan dengan `np.linalg.solve` pada lima puluh sistem acak berbagai ukuran. Semuanya cocok.
            """,
            filename="uji_acak_solver.py",
        ),
        T("""
        ## Operasi baris dan determinan

        Eliminasi Gauss juga memberi cara menghitung determinan. Menukar dua baris membalik tanda determinan, menambah kelipatan satu baris ke baris lain tidak mengubahnya, dan mengalikan satu baris dengan skalar mengalikan determinan dengan skalar itu. Setelah matriks menjadi segitiga atas, determinannya adalah hasil kali elemen diagonal, dikalikan minus satu pangkat jumlah penukaran baris.

        Cara ini jauh lebih efisien daripada ekspansi kofaktor yang butuh faktorial operasi. Karena itu `np.linalg.det` memakai dekomposisi LU di balik layar. Determinan nol berarti ada pivot nol yang tak bisa ditukar, tanda bahwa baris-baris bergantung linear dan matriksnya singular.

        Pengetahuan ini menghubungkan tiga hal sekaligus: eliminasi, determinan, dan peringkat. Jumlah pivot tak nol setelah eliminasi sama dengan peringkat matriks, dan matriks persegi punya invers tepat ketika semua pivotnya tak nol. Satu algoritma sederhana menjawab ketiga pertanyaan itu.
        """),
        E(
            "A2-03-2-ex1",
            "mudah",
            """
            Tulis fungsi `tukar_baris(M, i, j)` yang mengembalikan salinan matriks (list of list) dengan baris `i` dan `j` ditukar. Matriks asal tidak boleh berubah.
            """,
            """
            def tukar_baris(M, i, j):
                # TODO: implementasikan
                pass
            """,
            """
            a = [[1, 2], [3, 4], [5, 6]]
            assert tukar_baris(a, 0, 2) == [[5, 6], [3, 4], [1, 2]]
            assert a == [[1, 2], [3, 4], [5, 6]]
            assert tukar_baris(a, 1, 1) == a
            assert tukar_baris([[1], [2]], 0, 1) == [[2], [1]]
            """,
            "Salin tiap baris dulu lalu tukar.",
            """
            def tukar_baris(M, i, j):
                hasil = [list(b) for b in M]
                hasil[i], hasil[j] = hasil[j], hasil[i]
                return hasil
            """,
        ),
        E(
            "A2-03-2-ex2",
            "mudah",
            """
            Tulis fungsi `tambah_kelipatan(M, tujuan, sumber, k)` yang mengembalikan salinan matriks dengan baris `tujuan` ditambah `k` kali baris `sumber`.
            """,
            """
            def tambah_kelipatan(M, tujuan, sumber, k):
                # TODO: implementasikan
                pass
            """,
            """
            a = [[1, 2], [3, 4]]
            assert tambah_kelipatan(a, 1, 0, -3) == [[1, 2], [0, -2]]
            assert a == [[1, 2], [3, 4]]
            assert tambah_kelipatan(a, 0, 1, 1) == [[4, 6], [3, 4]]
            assert tambah_kelipatan(a, 0, 1, 0) == a
            """,
            "Buat salinan lalu perbarui baris tujuan dengan zip.",
            """
            def tambah_kelipatan(M, tujuan, sumber, k):
                hasil = [list(b) for b in M]
                hasil[tujuan] = [t + k * s for t, s in zip(M[tujuan], M[sumber])]
                return hasil
            """,
        ),
        E(
            "A2-03-2-ex3",
            "sedang",
            """
            Tulis fungsi `substitusi_mundur(U, c)` yang menyelesaikan `U x = c` untuk matriks segitiga atas `U` (list of list) dengan diagonal tak nol, dan mengembalikan `x` sebagai list dibulatkan 6 desimal.
            """,
            """
            def substitusi_mundur(U, c):
                # TODO: implementasikan
                pass
            """,
            """
            assert substitusi_mundur([[2, 1], [0, 3]], [5, 6]) == [1.5, 2.0]
            assert substitusi_mundur([[1]], [4]) == [4.0]
            assert substitusi_mundur([[2, 1, -1], [0, 0.5, 0.5], [0, 0, -1]], [8, 1, 1]) == [2.0, 3.0, -1.0]
            assert substitusi_mundur([[1, 0], [0, 1]], [3, 4]) == [3.0, 4.0]
            """,
            "Mulai dari baris terakhir dan kurangi kontribusi variabel yang sudah diketahui.",
            """
            def substitusi_mundur(U, c):
                n = len(U)
                x = [0.0] * n
                for i in range(n - 1, -1, -1):
                    s = sum(U[i][j] * x[j] for j in range(i + 1, n))
                    x[i] = (c[i] - s) / U[i][i]
                return [round(v, 6) for v in x]
            """,
        ),
        E(
            "A2-03-2-ex4",
            "menantang",
            """
            Tulis fungsi `gauss(A, b)` yang menyelesaikan `A x = b` untuk matriks persegi dengan eliminasi Gauss dan pivoting sebagian tanpa NumPy. Kembalikan `x` sebagai list dibulatkan 6 desimal. Bila matriks singular (pivot terbesar bernilai mutlak di bawah 1e-12) kembalikan `None`.
            """,
            """
            def gauss(A, b):
                # TODO: implementasikan
                pass
            """,
            """
            assert gauss([[2, 1], [1, -1]], [5, 1]) == [2.0, 1.0]
            assert gauss([[2, 1, -1], [-3, -1, 2], [-2, 1, 2]], [8, -11, -3]) == [2.0, 3.0, -1.0]
            assert gauss([[1, 1], [2, 2]], [2, 4]) is None
            assert gauss([[0, 1], [1, 0]], [3, 4]) == [4.0, 3.0]
            """,
            "Untuk tiap kolom pilih baris dengan elemen mutlak terbesar, tukar, lalu hilangkan elemen di bawahnya. Akhiri dengan substitusi mundur.",
            """
            def gauss(A, b):
                n = len(A)
                M = [list(map(float, A[i])) + [float(b[i])] for i in range(n)]
                for k in range(n):
                    p = max(range(k, n), key=lambda i: abs(M[i][k]))
                    if abs(M[p][k]) < 1e-12:
                        return None
                    M[k], M[p] = M[p], M[k]
                    for i in range(k + 1, n):
                        f = M[i][k] / M[k][k]
                        M[i] = [a - f * c for a, c in zip(M[i], M[k])]
                x = [0.0] * n
                for i in range(n - 1, -1, -1):
                    s = sum(M[i][j] * x[j] for j in range(i + 1, n))
                    x[i] = (M[i][n] - s) / M[i][i]
                return [round(v, 6) for v in x]
            """,
        ),
    ],
    [
        M("Membagi dengan pivot nol atau sangat kecil.", "Tukar baris dengan pivoting sebagian."),
        M("Mengubah matriks asal saat operasi baris.", "Kerjakan pada salinan."),
        M("Lupa ikut mengubah sisi kanan saat operasi baris.", "Gunakan matriks augmented."),
    ],
    [
        Q("Operasi baris elementer yang sah?", ["Menukar baris", "Menghapus baris", "Mengkuadratkan baris", "Menjumlah kolom"], 0, "Tukar, kalikan konstanta tak nol, dan tambah kelipatan.", hint="Tiga operasi."),
        Q("Apa tujuan eliminasi maju?", ["Membuat matriks segitiga", "Membuat identitas", "Menghitung norma", "Transpos"], 0, "Nol di bawah diagonal.", hint="Segitiga atas."),
        Q("Mengapa pivoting sebagian dipakai?", ["Mempercepat", "Menjaga kestabilan numerik", "Mengurangi memori", "Tidak perlu"], 1, "Menghindari pembagian dengan angka kecil.", hint="Galat pembulatan."),
        Q("Apa itu matriks augmented?", ["A dikali b", "A dengan b ditempel sebagai kolom", "Transpos A", "Invers A"], 1, "Bentuk [A | b].", hint="Kolom tambahan."),
        Q("Keuntungan dekomposisi LU?", ["Menyimpan eliminasi untuk b berbeda", "Menghitung norma", "Mengurutkan", "Tak ada"], 0, "Eliminasi dipakai ulang untuk banyak b.", hint="Sekali mahal, banyak murah."),
    ],
    [
        "Eliminasi Gauss mengubah sistem menjadi segitiga dengan operasi baris elementer.",
        "Substitusi mundur menyelesaikan variabel dari bawah ke atas.",
        "Pivoting sebagian menjaga kestabilan numerik.",
        "LU menyimpan eliminasi untuk dipakai ulang pada banyak sisi kanan.",
    ],
    [],
)

l3 = lesson(
    "A2-03-3",
    "Kuadrat terkecil dan regresi linear",
    35,
    [
        "Memahami solusi kuadrat terkecil sebagai proyeksi pada ruang kolom",
        "Menurunkan dan memakai persamaan normal X^T X b = X^T y",
        "Menyusun matriks desain dengan kolom intersep",
        "Membandingkan solusi sendiri dengan np.linalg.lstsq",
    ],
    [
        T("""
        ## Ketika tidak ada solusi persis

        Pada data nyata, jumlah pengamatan jauh lebih banyak daripada parameter, sehingga sistem `X w = y` hampir pasti tidak punya solusi persis. Titik-titik data tidak terletak tepat pada satu garis. Kita lalu mencari `w` yang membuat `X w` sedekat mungkin dengan `y`. Ukuran kedekatannya adalah jumlah kuadrat galat, `||y - X w||^2`.

        Meminimalkan jumlah kuadrat ini disebut **kuadrat terkecil**. Secara geometris, `X w` selalu berada di ruang kolom `X`, yaitu semua kombinasi linear kolom `X`. Titik di ruang itu yang paling dekat dengan `y` adalah **proyeksi ortogonal** `y` pada ruang kolom. Galatnya, `y - X w`, tegak lurus terhadap seluruh kolom `X`.

        Syarat ketegaklurusan inilah yang menghasilkan persamaan normal. Karena galat ortogonal pada tiap kolom `X`, kita punya `X^T (y - X w) = 0`, yang berarti `X^T X w = X^T y`.
        """),
        C(
            """
            import numpy as np

            X = np.array([[1.0, 1.0], [1.0, 2.0], [1.0, 3.0], [1.0, 4.0]])
            y = np.array([2.0, 3.0, 5.0, 6.0])
            w = np.linalg.solve(X.T @ X, X.T @ y)
            print(w.round(4).tolist())
            galat = y - X @ w
            print(galat.round(4).tolist())
            print(np.allclose(X.T @ galat, 0))
            print(round(float(galat @ galat), 4))
            """,
            """
            [0.5, 1.4]
            [0.1, -0.3, 0.3, -0.1]
            True
            0.2
            """,
            """
            Persamaan normal memberi garis `y = 0.5 + 1.4 x`. Galatnya tegak lurus terhadap kedua kolom `X`, sehingga `X.T @ galat` bernilai nol.
            """,
            filename="persamaan_normal.py",
        ),
        T("""
        ## Matriks desain dan intersep

        Untuk memodelkan `y = b0 + b1 x`, kita membentuk **matriks desain** `X` dengan kolom pertama berisi angka satu (untuk intersep) dan kolom kedua berisi nilai `x`. Tiap baris `X` mewakili satu pengamatan, dan `w = [b0, b1]` memuat parameter yang dicari. Kolom satu penting agar garis tidak terpaksa melewati titik asal.

        Model lebih banyak fitur tinggal menambah kolom. Model polinomial, misalnya `y = b0 + b1 x + b2 x^2`, tetap linear terhadap parameter, sehingga cukup menambah kolom `x^2`. Inilah sebabnya regresi linear sangat fleksibel: linear merujuk pada parameter, bukan pada bentuk kurva.

        Setelah `w` didapat, prediksi untuk semua pengamatan dihitung dengan `X @ w`. Kualitas model diukur dari galat, misalnya galat kuadrat rata-rata, dan dari koefisien determinasi `R^2` yang membandingkan galat model dengan galat prediksi rata-rata saja.
        """),
        C(
            """
            import numpy as np

            x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
            y = np.array([1.2, 3.9, 9.1, 15.8, 25.2])
            X1 = np.column_stack([np.ones_like(x), x])
            X2 = np.column_stack([np.ones_like(x), x, x ** 2])

            def cocok(X):
                w = np.linalg.lstsq(X, y, rcond=None)[0]
                galat = y - X @ w
                r2 = 1 - (galat @ galat) / ((y - y.mean()) @ (y - y.mean()))
                return w.round(3).tolist(), round(float(r2), 4)

            print(cocok(X1))
            print(cocok(X2))
            """,
            """
            ([-6.93, 5.99], 0.9575)
            ([0.52, -0.396, 1.064], 0.9998)
            """,
            """
            Menambah kolom `x^2` membuat model tetap linear pada parameter namun cocok jauh lebih baik, dengan `R^2` naik dari sekitar 0.96 ke hampir 1.
            """,
            filename="matriks_desain.py",
        ),
        K(
            "warning",
            """
            Jangan lupa kolom satu untuk intersep. Tanpanya garis dipaksa melewati titik asal dan hasilnya bias bila data memang tidak lewat titik itu.
            """,
            title="Kolom intersep",
        ),
        T("""
        ## Stabilitas numerik: normal versus lstsq

        Menyelesaikan persamaan normal langsung memang mudah, tetapi membentuk `X^T X` mengkuadratkan bilangan kondisi `X`. Bila `X` sudah berkondisi buruk, `X^T X` jauh lebih buruk sehingga hasil kehilangan banyak digit ketelitian. Karena itu perangkat lunak nyata tidak memakai persamaan normal secara langsung.

        `np.linalg.lstsq` memakai dekomposisi yang lebih stabil, yaitu SVD, yang akan kamu pelajari beberapa modul lagi. Ia juga menangani kasus `X` yang kolomnya bergantung linear dengan memberi solusi berpanjang minimum, sedangkan persamaan normal akan gagal karena `X^T X` singular.

        Pegangan praktis: untuk pembelajaran dan data kecil yang rapi, persamaan normal aman dan memperjelas konsep. Untuk pekerjaan serius, pakai `lstsq` atau pustaka seperti scikit-learn dan statsmodels yang sudah menangani detail ini untukmu.
        """),
        C(
            """
            import numpy as np

            x = np.arange(1.0, 6.0)
            y = 2 * x + 1
            X = np.column_stack([np.ones_like(x), x, 2 * x])
            print(np.linalg.matrix_rank(X))
            try:
                np.linalg.solve(X.T @ X, X.T @ y)
                print("tanpa galat")
            except np.linalg.LinAlgError:
                print("X^T X singular")
            w = np.linalg.lstsq(X, y, rcond=None)[0]
            print(np.allclose(X @ w, y))
            """,
            """
            2
            X^T X singular
            True
            """,
            """
            Kolom ketiga adalah dua kali kolom kedua sehingga `X^T X` singular dan `solve` gagal. `lstsq` tetap memberi solusi yang cocok dengan data.
            """,
            filename="normal_vs_lstsq.py",
        ),
        T("""
        ## Dari kuadrat terkecil ke pembelajaran mesin

        Regresi linear adalah model pembelajaran mesin paling sederhana sekaligus fondasi bagi banyak model lain. Regresi logistik, regresi ridge, dan bahkan lapisan terakhir jaringan saraf memakai gagasan yang sama: cari parameter yang meminimalkan suatu galat atas data. Perbedaannya terletak pada fungsi galat dan cara meminimalkannya.

        Untuk galat kuadrat linear, solusi tertutup tersedia lewat persamaan normal. Untuk model yang lebih rumit, solusi tertutup tidak ada dan kita memakai optimasi iteratif seperti gradient descent, topik pada kursus kalkulus dan optimasi. Memahami solusi tertutup memberimu patokan untuk memeriksa apakah optimasi iteratifmu berjalan benar.

        Latihan berikut membangun regresi dari nol: menyusun matriks desain, menyelesaikan persamaan normal, dan menghitung galat serta R kuadrat.
        """),
        T("""
        ## Memeriksa asumsi

        Kuadrat terkecil memberi hasil, tetapi hasil itu hanya bermakna bila asumsinya wajar. Periksa grafik galat terhadap prediksi: bila polanya melengkung, model linear belum cukup. Periksa pencilan, karena satu titik ekstrem dapat menarik garis jauh dari mayoritas data akibat galat dikuadratkan. Periksa korelasi antar fitur, sebab fitur yang hampir kembar membuat koefisien tidak stabil.
        """),
        E(
            "A2-03-3-ex1",
            "mudah",
            """
            Tulis fungsi `matriks_desain(x)` yang menerima list nilai `x` dan mengembalikan matriks desain (list of list) dengan kolom pertama 1 dan kolom kedua `x`.
            """,
            """
            def matriks_desain(x):
                # TODO: implementasikan
                pass
            """,
            """
            assert matriks_desain([1, 2, 3]) == [[1, 1], [1, 2], [1, 3]]
            assert matriks_desain([]) == []
            assert matriks_desain([5]) == [[1, 5]]
            assert matriks_desain([0.5, -1]) == [[1, 0.5], [1, -1]]
            """,
            "Bangun satu baris [1, nilai] untuk tiap nilai x.",
            """
            def matriks_desain(x):
                return [[1, v] for v in x]
            """,
        ),
        E(
            "A2-03-3-ex2",
            "mudah",
            """
            Tulis fungsi `galat_kuadrat(y, prediksi)` yang mengembalikan jumlah kuadrat selisih dua list.
            """,
            """
            def galat_kuadrat(y, prediksi):
                # TODO: implementasikan
                pass
            """,
            """
            assert galat_kuadrat([1, 2, 3], [1, 2, 3]) == 0
            assert galat_kuadrat([1, 2], [2, 4]) == 5
            assert galat_kuadrat([], []) == 0
            assert galat_kuadrat([0], [3]) == 9
            """,
            "Jumlahkan (a - b) ** 2 untuk tiap pasangan.",
            """
            def galat_kuadrat(y, prediksi):
                return sum((a - b) ** 2 for a, b in zip(y, prediksi))
            """,
        ),
        E(
            "A2-03-3-ex3",
            "sedang",
            """
            Tulis fungsi `garis_terbaik(x, y)` yang mengembalikan tuple `(b0, b1)` dari regresi linear sederhana `y = b0 + b1 x` dengan rumus `b1 = kovariansi(x, y) / varians(x)` dan `b0 = rata(y) - b1 * rata(x)`, dibulatkan 6 desimal. Anggap varians `x` tidak nol.
            """,
            """
            def garis_terbaik(x, y):
                # TODO: implementasikan
                pass
            """,
            """
            assert garis_terbaik([1, 2, 3, 4], [2, 3, 5, 6]) == (0.5, 1.4)
            assert garis_terbaik([0, 1, 2], [1, 3, 5]) == (1.0, 2.0)
            assert garis_terbaik([1, 2, 3], [4, 4, 4]) == (4.0, 0.0)
            assert garis_terbaik([-1, 0, 1], [1, 0, 1]) == (0.666667, 0.0)
            """,
            "Hitung rata-rata, lalu jumlah hasil kali simpangan dibagi jumlah kuadrat simpangan x.",
            """
            def garis_terbaik(x, y):
                n = len(x)
                mx = sum(x) / n
                my = sum(y) / n
                b1 = sum((a - mx) * (b - my) for a, b in zip(x, y)) / sum((a - mx) ** 2 for a in x)
                b0 = my - b1 * mx
                return round(b0, 6), round(b1, 6)
            """,
        ),
        E(
            "A2-03-3-ex4",
            "menantang",
            """
            Tulis fungsi `r_kuadrat(y, prediksi)` yang mengembalikan koefisien determinasi `1 - SSE / SST` dibulatkan 4 desimal, dengan SSE jumlah kuadrat galat dan SST jumlah kuadrat simpangan `y` dari rata-ratanya. Bila SST nol kembalikan 1.0 jika SSE nol dan 0.0 bila tidak.
            """,
            """
            def r_kuadrat(y, prediksi):
                # TODO: implementasikan
                pass
            """,
            """
            assert r_kuadrat([1, 2, 3], [1, 2, 3]) == 1.0
            assert r_kuadrat([1, 2, 3], [2, 2, 2]) == 0.0
            assert r_kuadrat([2, 3, 5, 6], [1.9, 3.3, 4.7, 6.1]) == 0.98
            assert r_kuadrat([4, 4], [4, 4]) == 1.0
            assert r_kuadrat([4, 4], [5, 5]) == 0.0
            """,
            "Hitung SSE dan SST lalu tangani SST nol secara terpisah.",
            """
            def r_kuadrat(y, prediksi):
                rata = sum(y) / len(y)
                sse = sum((a - b) ** 2 for a, b in zip(y, prediksi))
                sst = sum((a - rata) ** 2 for a in y)
                if sst == 0:
                    return 1.0 if sse == 0 else 0.0
                return round(1 - sse / sst, 4)
            """,
        ),
    ],
    [
        M("Lupa kolom intersep pada matriks desain.", "Tambahkan kolom berisi satu."),
        M("Menyelesaikan persamaan normal pada X berkondisi buruk.", "Pakai np.linalg.lstsq."),
        M("Mengira regresi linear hanya untuk garis lurus.", "Linear pada parameter, kolom polinomial diperbolehkan."),
    ],
    [
        Q("Apa yang diminimalkan kuadrat terkecil?", ["Jumlah galat", "Jumlah kuadrat galat", "Galat terbesar", "Jumlah y"], 1, "||y - X w||^2.", hint="Dikuadratkan."),
        Q("Galat kuadrat terkecil terhadap kolom X bersifat?", ["Sejajar", "Tegak lurus", "Sama dengan nol selalu", "Sama dengan y"], 1, "X^T galat = 0.", hint="Proyeksi ortogonal."),
        Q("Persamaan normal?", ["X w = y", "X^T X w = X^T y", "X X^T w = y", "w = X y"], 1, "Hasil syarat ortogonalitas.", hint="Ada transpos di kedua sisi."),
        Q("Fungsi kolom satu di matriks desain?", ["Normalisasi", "Intersep", "Regularisasi", "Pencilan"], 1, "Mengizinkan garis tidak lewat titik asal.", hint="Konstanta."),
        Q("Mengapa lstsq lebih disukai?", ["Lebih pendek", "Lebih stabil secara numerik", "Selalu eksak", "Tak butuh data"], 1, "Tidak mengkuadratkan bilangan kondisi.", hint="Memakai SVD."),
    ],
    [
        "Kuadrat terkecil memproyeksikan y ke ruang kolom X.",
        "Persamaan normal X^T X w = X^T y memberi solusi tertutup.",
        "Matriks desain memakai kolom satu untuk intersep dan boleh berisi kolom polinomial.",
        "Pakai lstsq untuk kestabilan numerik.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa perhitungan dan contoh kode yang cukup jelas dalam teks.", "brief": []}

write_module(
    "A2",
    3,
    "Sistem persamaan linear",
    105,
    [
        "Menulis dan menafsirkan sistem persamaan linear dalam bentuk matriks",
        "Menyelesaikan sistem dengan eliminasi Gauss dan pivoting",
        "Memakai kuadrat terkecil untuk regresi linear",
    ],
    [l1, l2, l3],
    video,
    REF,
)
