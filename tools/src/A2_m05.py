import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

l1 = lesson(
    "A2-05-1",
    "Eigenvalue dan eigenvector",
    35,
    [
        "Memahami eigenvector sebagai arah yang hanya diskalakan oleh sebuah matriks",
        "Menghitung eigenvalue 2x2 lewat persamaan karakteristik",
        "Memakai np.linalg.eig dan memverifikasi hasilnya",
        "Menafsirkan eigenvalue sebagai faktor penskalaan sepanjang arah tertentu",
    ],
    [
        T("""
        ## Arah yang tidak berubah

        Sebuah matriks `A` mengubah hampir semua vektor: panjangnya berubah dan arahnya berputar. Namun untuk sebagian arah khusus, matriks hanya meregangkan atau memampatkan vektor tanpa mengubah arahnya. Vektor seperti itu disebut **eigenvector**, dan faktor peregangannya disebut **eigenvalue**. Secara matematis: `A v = lambda v`, dengan `v` tak nol dan `lambda` sebuah bilangan.

        Contoh: `A = [[2, 0], [0, 3]]` meregangkan sumbu pertama dua kali dan sumbu kedua tiga kali. Vektor `[1, 0]` adalah eigenvector dengan eigenvalue 2, dan `[0, 1]` adalah eigenvector dengan eigenvalue 3. Pada matriks yang tidak diagonal, arah khusus itu tidak lagi searah dengan sumbu koordinat, tetapi tetap ada.

        Mengapa ini penting? Bayangkan kamu menekan sebuah karet gelang pada dua arah berbeda: ada arah tempat karet hanya memanjang tanpa berputar. Itulah arah eigen. Eigenvector mengungkap struktur terdalam sebuah transformasi. Dalam data science, eigenvector matriks kovariansi menunjukkan arah variasi terbesar dalam data, dasar PCA. Dalam analisis jaringan, eigenvector menentukan simpul paling berpengaruh. Dalam sistem dinamis, eigenvalue menentukan apakah sebuah sistem stabil.
        """),
        C(
            """
            import numpy as np

            A = np.array([[2.0, 0.0], [0.0, 3.0]])
            for v in ([1.0, 0.0], [0.0, 1.0], [1.0, 1.0]):
                v = np.array(v)
                print((A @ v).tolist())

            B = np.array([[2.0, 1.0], [1.0, 2.0]])
            v = np.array([1.0, 1.0])
            print((B @ v).tolist())
            w = np.array([1.0, -1.0])
            print((B @ w).tolist())
            """,
            """
            [2.0, 0.0]
            [0.0, 3.0]
            [2.0, 3.0]
            [3.0, 3.0]
            [1.0, -1.0]
            """,
            """
            Pada matriks diagonal sumbu koordinat tetap searah setelah transformasi, sedangkan `[1, 1]` berubah arah. Pada `B`, vektor `[1, 1]` diskalakan tiga kali dan `[1, -1]` diskalakan satu kali.
            """,
            filename="arah_khusus.py",
        ),
        T("""
        ## Persamaan karakteristik

        Untuk mencari eigenvalue, tulis `A v = lambda v` sebagai `(A - lambda I) v = 0`. Agar ada `v` tak nol yang memenuhinya, matriks `A - lambda I` harus singular, yaitu determinannya nol: `det(A - lambda I) = 0`. Persamaan ini disebut **persamaan karakteristik**, dan akar-akarnya adalah eigenvalue.

        Untuk matriks `2 x 2`, `[[a, b], [c, d]]`, persamaannya menjadi `lambda^2 - (a + d) lambda + (a d - b c) = 0`. Koefisiennya punya makna: `a + d` adalah **trace** (jumlah diagonal) dan `a d - b c` adalah **determinan**. Jadi `lambda^2 - trace * lambda + det = 0`, yang bisa diselesaikan dengan rumus abc.

        Langkah ini tampak abstrak, tetapi pada praktiknya hanya perlu menghitung trace dan determinan lalu menyelesaikan persamaan kuadrat sederhana. Setelah eigenvalue ditemukan, eigenvector didapat dengan menyelesaikan `(A - lambda I) v = 0` untuk tiap `lambda`. Eigenvector tidak tunggal: kelipatan skalar eigenvector juga eigenvector, jadi biasanya kita menormalkannya menjadi panjang satu.
        """),
        C(
            """
            import numpy as np

            def eigen_2x2(m):
                (a, b), (c, d) = m
                tr = a + d
                det = a * d - b * c
                disk = tr * tr - 4 * det
                akar = disk ** 0.5
                return sorted([(tr - akar) / 2, (tr + akar) / 2])

            print(eigen_2x2([[2, 1], [1, 2]]))
            print(eigen_2x2([[4, 1], [2, 3]]))
            print(sorted(np.linalg.eigvals(np.array([[4.0, 1.0], [2.0, 3.0]])).real.round(4).tolist()))

            A = np.array([[4.0, 1.0], [2.0, 3.0]])
            for lam in (2.0, 5.0):
                print(round(float(np.linalg.det(A - lam * np.eye(2))), 6))
            """,
            """
            [1.0, 3.0]
            [2.0, 5.0]
            [2.0, 5.0]
            0.0
            0.0
            """,
            """
            Rumus trace dan determinan memberi eigenvalue 2x2. Pada eigenvalue yang benar, matriks `A - lambda I` singular sehingga determinannya nol.
            """,
            filename="persamaan_karakteristik.py",
        ),
        K(
            "tip",
            """
            Untuk matriks 2x2, jumlah eigenvalue sama dengan trace dan hasil kalinya sama dengan determinan. Ini jalan pintas bagus untuk memeriksa jawabanmu.
            """,
            title="Pemeriksaan cepat",
        ),
        T("""
        ## Memakai np.linalg.eig

        Untuk matriks umum, gunakan `np.linalg.eig(A)`. Fungsi ini mengembalikan dua hal: array eigenvalue, dan matriks yang **kolom-kolomnya** adalah eigenvector yang bersesuaian. Perhatikan bahwa eigenvector berada di kolom, bukan baris, kesalahan yang sangat umum. Eigenvector yang dikembalikan sudah dinormalkan menjadi panjang satu.

        Urutan eigenvalue tidak dijamin, dan tanda eigenvector bisa positif atau negatif. Karena itu jangan bergantung pada urutan atau tanda saat menulis tes. Cara andal memverifikasi hasil adalah memeriksa persamaan dasar: `A v` harus sama dengan `lambda v` untuk tiap pasangan.

        Eigenvalue bisa berupa bilangan kompleks, misalnya pada matriks rotasi, yang tidak punya arah real yang tetap. Untuk matriks simetris real, semua eigenvalue pasti real, dan lebih baik memakai `np.linalg.eigh` yang dirancang khusus untuk itu: lebih cepat, lebih akurat, dan mengurutkan eigenvalue dari kecil ke besar.
        """),
        C(
            """
            import numpy as np

            A = np.array([[4.0, 1.0], [2.0, 3.0]])
            nilai, vektor = np.linalg.eig(A)
            urut = np.argsort(-nilai.real)
            nilai, vektor = nilai.real[urut], vektor.real[:, urut]
            for i in range(2):
                v = vektor[:, i]
                print(round(float(nilai[i]), 4), np.allclose(A @ v, nilai[i] * v), round(float(np.linalg.norm(v)), 4))

            S = np.array([[2.0, 1.0], [1.0, 2.0]])
            n2, v2 = np.linalg.eigh(S)
            print(n2.round(4).tolist(), np.allclose(S @ v2, v2 * n2))

            R = np.array([[0.0, -1.0], [1.0, 0.0]])
            print(np.linalg.eigvals(R))
            """,
            """
            5.0 True 1.0
            2.0 True 1.0
            [1.0, 3.0] True
            [0.+1.j 0.-1.j]
            """,
            """
            Kolom matriks vektor adalah eigenvector dan memenuhi `A v = lambda v`. Matriks simetris memakai `eigh` dengan eigenvalue terurut, dan rotasi 90 derajat punya eigenvalue kompleks.
            """,
            filename="eig_numpy.py",
        ),
        T("""
        ## Tafsir geometris dan jumlah eigenvector

        Eigenvalue memberi tahu apa yang terjadi sepanjang tiap arah khusus. Nilai lebih besar dari satu meregangkan, antara nol dan satu memampatkan, negatif membalik arah sekaligus meregangkan atau memampatkan, dan nol meruntuhkan arah itu sepenuhnya. Matriks dengan eigenvalue nol singular, sebab ada arah yang hilang.

        Matriks `n x n` memiliki `n` eigenvalue bila dihitung dengan kelipatan dan boleh kompleks. Namun jumlah eigenvector yang bebas linear bisa kurang dari `n`. Matriks seperti `[[1, 1], [0, 1]]` hanya punya satu arah eigen walau eigenvalue 1 muncul dua kali. Matriks demikian disebut *defektif* dan tidak bisa didiagonalkan.

        Kabar baiknya, matriks simetris real, yang paling sering muncul dalam statistik, tidak pernah defektif. Ia selalu punya `n` eigenvector yang saling ortogonal. Itu fakta kunci di balik PCA dan akan dimanfaatkan penuh pada pelajaran selanjutnya.
        """),
        E(
            "A2-05-1-ex1",
            "mudah",
            """
            Tulis fungsi `trace(m)` yang mengembalikan jumlah elemen diagonal matriks persegi (list of list).
            """,
            """
            def trace(m):
                # TODO: implementasikan
                pass
            """,
            """
            assert trace([[2, 1], [1, 2]]) == 4
            assert trace([[5]]) == 5
            assert trace([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == 15
            assert trace([]) == 0
            """,
            "Jumlahkan m[i][i].",
            """
            def trace(m):
                return sum(m[i][i] for i in range(len(m)))
            """,
        ),
        E(
            "A2-05-1-ex2",
            "mudah",
            """
            Tulis fungsi `adalah_eigen(A, v, lam)` yang mengembalikan `True` bila `A v = lam v` dalam toleransi 1e-9, untuk `A` list of list, `v` list, dan `lam` bilangan.
            """,
            """
            def adalah_eigen(A, v, lam):
                # TODO: implementasikan
                pass
            """,
            """
            assert adalah_eigen([[2, 1], [1, 2]], [1, 1], 3) is True
            assert adalah_eigen([[2, 1], [1, 2]], [1, -1], 1) is True
            assert adalah_eigen([[2, 1], [1, 2]], [1, 0], 2) is False
            assert adalah_eigen([[2, 0], [0, 3]], [0, 5], 3) is True
            """,
            "Hitung A v lalu bandingkan dengan lam kali v komponen demi komponen.",
            """
            def adalah_eigen(A, v, lam):
                av = [sum(a * b for a, b in zip(baris, v)) for baris in A]
                return all(abs(x - lam * y) < 1e-9 for x, y in zip(av, v))
            """,
        ),
        E(
            "A2-05-1-ex3",
            "sedang",
            """
            Tulis fungsi `eigenvalue_2x2(m)` yang mengembalikan list dua eigenvalue real matriks 2x2 terurut naik, dibulatkan 6 desimal, memakai trace dan determinan. Bila diskriminan negatif kembalikan `None`.
            """,
            """
            def eigenvalue_2x2(m):
                # TODO: implementasikan
                pass
            """,
            """
            assert eigenvalue_2x2([[2, 1], [1, 2]]) == [1.0, 3.0]
            assert eigenvalue_2x2([[4, 1], [2, 3]]) == [2.0, 5.0]
            assert eigenvalue_2x2([[0, -1], [1, 0]]) is None
            assert eigenvalue_2x2([[5, 0], [0, 5]]) == [5.0, 5.0]
            """,
            "Selesaikan lambda kuadrat dikurangi trace kali lambda ditambah det sama dengan nol.",
            """
            def eigenvalue_2x2(m):
                (a, b), (c, d) = m
                tr, det = a + d, a * d - b * c
                disk = tr * tr - 4 * det
                if disk < 0:
                    return None
                akar = disk ** 0.5
                return [round((tr - akar) / 2, 6), round((tr + akar) / 2, 6)]
            """,
        ),
        E(
            "A2-05-1-ex4",
            "menantang",
            """
            Tulis fungsi `eigenvector_2x2(m, lam)` yang mengembalikan satu eigenvector satuan (list dua komponen dibulatkan 6 desimal, komponen pertama tidak negatif) untuk eigenvalue `lam` dari matriks 2x2 yang bukan kelipatan identitas. Selesaikan `(A - lam I) v = 0` dengan memakai baris yang tidak nol.
            """,
            """
            def eigenvector_2x2(m, lam):
                # TODO: implementasikan
                pass
            """,
            """
            r = eigenvector_2x2([[2, 1], [1, 2]], 3)
            assert r == [0.707107, 0.707107]
            r2 = eigenvector_2x2([[2, 1], [1, 2]], 1)
            assert r2 == [0.707107, -0.707107]
            r3 = eigenvector_2x2([[4, 1], [2, 3]], 5)
            assert r3 == [0.707107, 0.707107]
            r4 = eigenvector_2x2([[2, 0], [0, 3]], 3)
            assert r4 == [0.0, 1.0]
            """,
            "Dari baris (a - lam, b) vektor (b, lam - a) memenuhi persamaan. Bila baris itu nol pakai baris kedua. Normalkan dan atur tandanya.",
            """
            def eigenvector_2x2(m, lam):
                (a, b), (c, d) = m
                if abs(a - lam) > 1e-12 or abs(b) > 1e-12:
                    v = (b, lam - a)
                else:
                    v = (lam - d, c)
                if abs(v[0]) < 1e-12 and abs(v[1]) < 1e-12:
                    v = (lam - d, c)
                n = (v[0] ** 2 + v[1] ** 2) ** 0.5
                if n < 1e-12:
                    v = (1.0, 0.0)
                    n = 1.0
                x, y = v[0] / n, v[1] / n
                if x < -1e-12 or (abs(x) < 1e-12 and y < 0):
                    x, y = -x, -y
                return [round(x + 0.0, 6), round(y + 0.0, 6)]
            """,
        ),
    ],
    [
        M("Mengambil baris matriks eigenvector dari eig.", "Eigenvector ada di kolom."),
        M("Mengandalkan urutan atau tanda hasil eig.", "Verifikasi dengan A v = lambda v."),
        M("Memakai eig untuk matriks simetris.", "Pakai eigh yang lebih akurat dan terurut."),
    ],
    [
        Q("Persamaan dasar eigen?", ["A v = v", "A v = lambda v", "A + v = lambda", "A v = 0"], 1, "Eigenvector hanya diskalakan oleh eigenvalue.", hint="Arah tetap."),
        Q("Jumlah eigenvalue sama dengan?", ["Determinan", "Trace", "Peringkat", "Norma"], 1, "Jumlah diagonal.", hint="Diagonal."),
        Q("Hasil kali eigenvalue sama dengan?", ["Trace", "Determinan", "Nol", "Satu"], 1, "Hasil kali eigenvalue adalah determinan.", hint="Singular bila nol."),
        Q("Di mana eigenvector pada hasil eig?", ["Di baris", "Di kolom", "Di diagonal", "Tidak ada"], 1, "Kolom ke-i untuk eigenvalue ke-i.", hint="vektor[:, i]."),
        Q("Matriks simetris real memiliki eigenvalue?", ["Kompleks", "Selalu real", "Selalu nol", "Negatif"], 1, "Semua real dan eigenvectornya ortogonal.", hint="Dipakai PCA."),
    ],
    [
        "Eigenvector adalah arah yang hanya diskalakan oleh matriks dengan faktor eigenvalue.",
        "Eigenvalue berasal dari det(A - lambda I) = 0 dan jumlahnya sama dengan trace.",
        "np.linalg.eig mengembalikan eigenvector di kolom, eigh untuk matriks simetris.",
        "Matriks simetris real punya eigenvector ortogonal lengkap.",
    ],
    [],
)

l2 = lesson(
    "A2-05-2",
    "Diagonalisasi dan sifat eigen",
    35,
    [
        "Memahami diagonalisasi A = P D P^-1",
        "Menghitung pangkat matriks dengan diagonalisasi",
        "Memakai dekomposisi spektral untuk matriks simetris",
        "Menghubungkan eigenvalue dengan trace, determinan, dan invers",
    ],
    [
        T("""
        ## Diagonalisasi

        Bila matriks `A` berukuran `n x n` memiliki `n` eigenvector yang bebas linear, kita dapat menulis `A = P D P^-1`. Kolom-kolom `P` adalah eigenvector, dan `D` adalah matriks diagonal berisi eigenvalue yang bersesuaian. Proses ini disebut **diagonalisasi**. Intinya: dalam sistem koordinat yang sumbunya adalah eigenvector, transformasi `A` hanya meregangkan tiap sumbu, tanpa memutar.

        Bayangkan tiga langkah: `P^-1` mengubah koordinat dari sumbu biasa ke sumbu eigen, `D` meregangkan tiap sumbu, lalu `P` kembali ke sumbu biasa. Transformasi rumit menjadi sederhana bila dilihat dari sudut yang tepat. Ini ide besar aljabar linear: pilih basis yang membuat masalah mudah.

        Dengan kata lain, diagonalisasi adalah cara mengganti kacamata agar matriks yang tampak rumit terlihat sebagai peregangan sederhana. Tidak semua matriks bisa didiagonalkan. Syaratnya cukup eigenvector bebas linear. Matriks defektif gagal, tetapi matriks simetris real selalu berhasil, dan eigenvector-nya bahkan ortogonal sehingga `P^-1` sama dengan `P^T`.
        """),
        C(
            """
            import numpy as np

            A = np.array([[4.0, 1.0], [2.0, 3.0]])
            nilai, P = np.linalg.eig(A)
            nilai, P = nilai.real, P.real
            D = np.diag(nilai)
            print(np.allclose(P @ D @ np.linalg.inv(P), A))
            print(sorted(nilai.round(4).tolist()))

            S = np.array([[2.0, 1.0], [1.0, 2.0]])
            n, Q = np.linalg.eigh(S)
            print(np.allclose(Q @ np.diag(n) @ Q.T, S), np.allclose(Q.T @ Q, np.eye(2)))

            defektif = np.array([[1.0, 1.0], [0.0, 1.0]])
            nilai2, P2 = np.linalg.eig(defektif)
            print(nilai2.real.tolist(), round(float(abs(np.linalg.det(P2.real))), 6) < 1e-6)
            """,
            """
            True
            [2.0, 5.0]
            True True
            [1.0, 1.0] True
            """,
            """
            `P D P^-1` merekonstruksi `A`. Untuk matriks simetris `P` ortogonal sehingga inversnya adalah transpos. Matriks defektif menghasilkan `P` yang hampir singular.
            """,
            filename="diagonalisasi.py",
        ),
        T("""
        ## Pangkat matriks

        Keuntungan terbesar diagonalisasi adalah menghitung pangkat matriks. Karena `A = P D P^-1`, maka `A^2 = P D P^-1 P D P^-1 = P D^2 P^-1`, dan secara umum `A^k = P D^k P^-1`. Memangkatkan matriks diagonal mudah: cukup memangkatkan tiap elemen diagonal. Jadi alih-alih mengalikan matriks `k` kali, kita hanya memangkatkan `n` bilangan.

        Ini berguna untuk memahami perilaku jangka panjang. Bila semua eigenvalue bernilai mutlak kurang dari satu, `A^k` menuju nol saat `k` besar, sistem stabil. Bila ada eigenvalue yang bernilai mutlak lebih dari satu, `A^k` meledak. Bila eigenvalue terbesar tepat satu, sistem menuju keadaan tetap.

        Cara ini menghemat banyak komputasi, terutama bila pangkatnya sangat besar atau matriksnya berukuran besar. Contoh klasik adalah barisan Fibonacci, yang dapat dihitung dengan memangkatkan matriks `[[1, 1], [1, 0]]`. Eigenvalue terbesarnya adalah rasio emas, dan inilah mengapa Fibonacci tumbuh secara eksponensial dengan laju rasio emas.
        """),
        C(
            """
            import numpy as np

            A = np.array([[4.0, 1.0], [2.0, 3.0]])
            nilai, P = np.linalg.eig(A)
            nilai, P = nilai.real, P.real
            k = 5
            Ak = P @ np.diag(nilai ** k) @ np.linalg.inv(P)
            print(np.allclose(Ak, np.linalg.matrix_power(A, k)))
            print(Ak.round(2).tolist())

            F = np.array([[1.0, 1.0], [1.0, 0.0]])
            print(np.linalg.matrix_power(F, 10).astype(int).tolist())
            nf = np.linalg.eigvals(F).real
            print(round(float(max(nf)), 6), round((1 + 5 ** 0.5) / 2, 6))
            """,
            """
            True
            [[2094.0, 1031.0], [2062.0, 1063.0]]
            [[89, 55], [55, 34]]
            1.618034 1.618034
            """,
            """
            Memangkatkan eigenvalue lalu kembali ke basis asal setara dengan memangkatkan matriks. Fibonacci muncul dari pangkat matriks dan eigenvalue terbesarnya adalah rasio emas.
            """,
            filename="pangkat_matriks.py",
        ),
        K(
            "warning",
            """
            Rumus `A^k = P D^k P^-1` hanya berlaku bila `A` bisa didiagonalkan. Untuk matriks defektif, pakai `np.linalg.matrix_power` langsung.
            """,
            title="Syarat diagonalisasi",
        ),
        T("""
        ## Dekomposisi spektral untuk matriks simetris

        Untuk matriks simetris real `S`, diagonalisasi mengambil bentuk istimewa: `S = Q D Q^T` dengan `Q` ortogonal. Ini disebut **dekomposisi spektral** atau teorema spektral. Ia setara dengan menulis `S` sebagai jumlah `lambda1 v1 v1^T + lambda2 v2 v2^T + ...`, yaitu jumlah matriks peringkat satu, masing-masing sepanjang satu eigenvector dan berbobot eigenvalue.

        Bentuk jumlah ini sangat kuat. Bila kamu hanya menyimpan suku-suku dengan eigenvalue terbesar, kamu mendapat pendekatan terbaik peringkat rendah dari `S`. Itulah inti kompresi dan reduksi dimensi: buang arah-arah dengan eigenvalue kecil karena sumbangannya sedikit.

        Matriks kovariansi dan matriks korelasi selalu simetris, dan semua eigenvalue-nya tidak negatif. Eigenvalue nol atau sangat kecil menandakan arah tanpa variasi, tanda adanya redundansi antar fitur. Semua ini menjadi fondasi PCA di modul-modul berikutnya.
        """),
        C(
            """
            import numpy as np

            S = np.array([[4.0, 2.0], [2.0, 3.0]])
            nilai, Q = np.linalg.eigh(S)
            print(nilai.round(4).tolist())
            rekon = sum(nilai[i] * np.outer(Q[:, i], Q[:, i]) for i in range(2))
            print(np.allclose(rekon, S))
            peringkat1 = nilai[1] * np.outer(Q[:, 1], Q[:, 1])
            print(peringkat1.round(3).tolist())
            print(round(float(np.linalg.norm(S - peringkat1)), 4), round(float(nilai[0]), 4))

            rng = np.random.default_rng(0)
            X = rng.normal(size=(100, 3))
            kov = np.cov(X.T)
            print(bool(np.all(np.linalg.eigvalsh(kov) >= 0)))
            """,
            """
            [1.4384, 5.5616]
            True
            [[3.455, 2.698], [2.698, 2.106]]
            1.4384 1.4384
            True
            """,
            """
            Matriks simetris dapat ditulis sebagai jumlah matriks peringkat satu berbobot eigenvalue. Galat pendekatan peringkat satu sama dengan eigenvalue yang dibuang, dan matriks kovariansi memiliki eigenvalue tak negatif.
            """,
            filename="dekomposisi_spektral.py",
        ),
        T("""
        ## Hubungan eigenvalue dengan sifat lain

        Eigenvalue terhubung erat dengan konsep yang sudah kamu pelajari. Jumlahnya sama dengan trace, hasil kalinya sama dengan determinan, sehingga matriks singular tepat bila memiliki eigenvalue nol. Eigenvalue `A^-1` adalah kebalikan eigenvalue `A`, dengan eigenvector yang sama. Eigenvalue `A^k` adalah pangkat ke-`k` dari eigenvalue `A`. Eigenvalue `A + c I` adalah eigenvalue `A` ditambah `c`, dengan eigenvector sama.

        Untuk matriks simetris, bilangan kondisi sama dengan rasio nilai mutlak eigenvalue terbesar terhadap terkecil. Matriks simetris dengan semua eigenvalue positif disebut **positif definit**. Ini terjadi misalnya pada `X^T X` bila kolom `X` bebas linear. Matriks positif definit selalu punya invers dan menjadi syarat banyak algoritma optimasi.

        Pengetahuan ini memberimu alat cepat. Dari eigenvalue saja kamu bisa menyimpulkan singular atau tidak, stabil atau tidak, serta baik atau buruknya kondisi. Latihan berikut melatih penggunaannya.
        """),
        E(
            "A2-05-2-ex1",
            "mudah",
            """
            Tulis fungsi `pangkat_diagonal(d, k)` yang menerima list elemen diagonal dan bilangan bulat `k` dan mengembalikan list elemen diagonal matriks diagonal itu dipangkatkan `k`.
            """,
            """
            def pangkat_diagonal(d, k):
                # TODO: implementasikan
                pass
            """,
            """
            assert pangkat_diagonal([2, 3], 3) == [8, 27]
            assert pangkat_diagonal([5], 0) == [1]
            assert pangkat_diagonal([], 2) == []
            assert pangkat_diagonal([0.5, 2], 2) == [0.25, 4]
            """,
            "Pangkatkan tiap elemen.",
            """
            def pangkat_diagonal(d, k):
                return [x ** k for x in d]
            """,
        ),
        E(
            "A2-05-2-ex2",
            "mudah",
            """
            Tulis fungsi `stabil(eigenvalue)` yang mengembalikan `True` bila semua eigenvalue (list bilangan real) bernilai mutlak kurang dari 1, artinya pangkat matriks menuju nol.
            """,
            """
            def stabil(eigenvalue):
                # TODO: implementasikan
                pass
            """,
            """
            assert stabil([0.5, -0.9]) is True
            assert stabil([0.5, 1.0]) is False
            assert stabil([1.2, 0.1]) is False
            assert stabil([]) is True
            """,
            "Periksa semua nilai mutlak.",
            """
            def stabil(eigenvalue):
                return all(abs(x) < 1 for x in eigenvalue)
            """,
        ),
        E(
            "A2-05-2-ex3",
            "sedang",
            """
            Tulis fungsi `fibonacci_matriks(n)` yang mengembalikan bilangan Fibonacci ke-`n` (dengan F(0)=0, F(1)=1) memakai pemangkatan matriks `[[1,1],[1,0]]` dengan perkalian matriks 2x2 manual dan pangkat berulang (kuadrat berulang). `n` boleh sampai 90.
            """,
            """
            def fibonacci_matriks(n):
                # TODO: implementasikan
                pass
            """,
            """
            assert fibonacci_matriks(0) == 0
            assert fibonacci_matriks(1) == 1
            assert fibonacci_matriks(10) == 55
            assert fibonacci_matriks(50) == 12586269025
            assert fibonacci_matriks(90) == 2880067194370816120
            """,
            "Kalikan matriks 2x2 dengan fungsi bantu dan pangkatkan dengan pembagian dua.",
            """
            def fibonacci_matriks(n):
                def kali(a, b):
                    return [[a[0][0] * b[0][0] + a[0][1] * b[1][0], a[0][0] * b[0][1] + a[0][1] * b[1][1]],
                            [a[1][0] * b[0][0] + a[1][1] * b[1][0], a[1][0] * b[0][1] + a[1][1] * b[1][1]]]
                hasil = [[1, 0], [0, 1]]
                dasar = [[1, 1], [1, 0]]
                while n > 0:
                    if n % 2 == 1:
                        hasil = kali(hasil, dasar)
                    dasar = kali(dasar, dasar)
                    n //= 2
                return hasil[0][1]
            """,
        ),
        E(
            "A2-05-2-ex4",
            "menantang",
            """
            Tulis fungsi `rekonstruksi(nilai, vektor)` yang menerima list eigenvalue dan list eigenvector satuan (tiap eigenvector adalah list) dari matriks simetris, dan mengembalikan matriks `sum(lambda_i * v_i v_i^T)` sebagai list of list dibulatkan 6 desimal.
            """,
            """
            def rekonstruksi(nilai, vektor):
                # TODO: implementasikan
                pass
            """,
            """
            r = 0.5 ** 0.5
            assert rekonstruksi([3, 1], [[r, r], [r, -r]]) == [[2.0, 1.0], [1.0, 2.0]]
            assert rekonstruksi([2, 3], [[1, 0], [0, 1]]) == [[2.0, 0.0], [0.0, 3.0]]
            assert rekonstruksi([5], [[1]]) == [[5.0]]
            """,
            "Untuk tiap elemen (i, j) jumlahkan lambda kali v[i] kali v[j] atas seluruh pasangan.",
            """
            def rekonstruksi(nilai, vektor):
                n = len(vektor[0])
                return [[round(sum(l * v[i] * v[j] for l, v in zip(nilai, vektor)) + 0.0, 6) for j in range(n)] for i in range(n)]
            """,
        ),
    ],
    [
        M("Mendiagonalkan matriks defektif.", "Periksa apakah ada n eigenvektor bebas linear."),
        M("Memakai P^-1 mahal untuk matriks simetris.", "Cukup transpos karena P ortogonal."),
        M("Mengira eigenvalue nol tidak penting.", "Ia menandakan matriks singular."),
    ],
    [
        Q("Bentuk diagonalisasi?", ["A = P D P^-1", "A = P + D", "A = D P", "A = P^T"], 0, "P berisi eigenvector dan D eigenvalue.", hint="Basis eigen."),
        Q("Rumus pangkat dengan diagonalisasi?", ["A^k = P D^k P^-1", "A^k = k A", "A^k = D P^k", "A^k = A / k"], 0, "Cukup memangkatkan diagonal.", hint="Hanya D yang dipangkatkan."),
        Q("Dekomposisi spektral berlaku untuk?", ["Semua matriks", "Matriks simetris real", "Matriks singular", "Matriks nol"], 1, "S = Q D Q^T.", hint="Ortogonal."),
        Q("Eigenvalue mana menandakan sistem stabil?", ["Mutlak lebih dari 1", "Mutlak kurang dari 1", "Sama dengan 5", "Kompleks"], 1, "Pangkat menuju nol.", hint="Mengecil."),
        Q("Matriks singular memiliki eigenvalue?", ["Satu", "Nol", "Negatif", "Kompleks"], 1, "Determinan adalah hasil kali eigenvalue.", hint="Hasil kali nol."),
    ],
    [
        "Diagonalisasi menulis A = P D P^-1 dalam basis eigenvector.",
        "Pangkat matriks dihitung dengan memangkatkan eigenvalue.",
        "Matriks simetris memiliki dekomposisi spektral dengan basis ortogonal.",
        "Eigenvalue menentukan stabilitas, singularitas, dan kondisi matriks.",
    ],
    [],
)

l3 = lesson(
    "A2-05-3",
    "Penerapan: power iteration, rantai Markov, dan PageRank",
    35,
    [
        "Menghitung eigenvalue dominan dengan power iteration",
        "Memahami distribusi stasioner rantai Markov sebagai eigenvector",
        "Menyusun mini PageRank dari matriks tautan",
        "Menghubungkan eigenvalue kovariansi dengan variansi arah utama data",
    ],
    [
        T("""
        ## Power iteration

        Menghitung semua eigenvalue matriks besar mahal, padahal sering kita hanya butuh yang terbesar. **Power iteration** adalah algoritma sederhana untuk itu. Mulai dari vektor acak `v`, ulangi: kalikan dengan `A`, lalu normalkan menjadi panjang satu. Setelah beberapa langkah, `v` mendekati eigenvector dengan eigenvalue terbesar mutlak, dan `v^T A v` mendekati eigenvalue itu.

        Mengapa bekerja? Vektor awal adalah kombinasi eigenvector. Setiap perkalian dengan `A` meregangkan tiap komponen sesuai eigenvalue-nya, sehingga komponen dengan eigenvalue terbesar tumbuh paling cepat dan akhirnya mendominasi. Kecepatan konvergensi bergantung pada rasio eigenvalue terbesar kedua terhadap terbesar: makin kecil rasio, makin cepat.

        Algoritma ini hanya butuh perkalian matriks-vektor, sehingga cocok untuk matriks raksasa dan jarang. Ia menjadi inti PageRank Google, dan versi lanjutannya dipakai dalam berbagai pustaka untuk menghitung SVD dan PCA besar.
        """),
        C(
            """
            import numpy as np

            def power_iteration(A, langkah=100, benih=0):
                rng = np.random.default_rng(benih)
                v = rng.normal(size=A.shape[0])
                v /= np.linalg.norm(v)
                for _ in range(langkah):
                    w = A @ v
                    v = w / np.linalg.norm(w)
                return float(v @ A @ v), v

            S = np.array([[4.0, 2.0], [2.0, 3.0]])
            lam, v = power_iteration(S)
            print(round(lam, 4), round(float(np.linalg.eigvalsh(S)[-1]), 4))
            print(np.allclose(S @ v, lam * v))

            B = np.array([[2.0, 1.0, 0.0], [1.0, 3.0, 1.0], [0.0, 1.0, 4.0]])
            lam2, _ = power_iteration(B, 200)
            print(round(lam2, 4), round(float(np.linalg.eigvalsh(B)[-1]), 4))
            """,
            """
            5.5616 5.5616
            True
            4.7321 4.7321
            """,
            """
            Power iteration konvergen ke eigenvalue terbesar dan hasilnya cocok dengan `eigvalsh`. Vektor akhirnya memenuhi `A v = lambda v`.
            """,
            filename="power_iteration.py",
        ),
        T("""
        ## Rantai Markov

        **Rantai Markov** memodelkan sistem yang berpindah antar keadaan dengan peluang yang hanya bergantung pada keadaan saat ini. Peluang perpindahan disusun dalam **matriks transisi** `P`, dengan `P[i, j]` peluang pindah dari keadaan `i` ke `j`. Setiap baris berjumlah satu. Bila `pi` adalah vektor baris peluang keadaan sekarang, maka peluang setelah satu langkah adalah `pi P`.

        Setelah banyak langkah, banyak rantai konvergen ke **distribusi stasioner** `pi*` yang tidak lagi berubah: `pi* P = pi*`. Persamaan ini berbentuk `P^T v = v`, yaitu eigenvector dari `P^T` dengan eigenvalue satu. Jadi distribusi stasioner adalah eigenvector yang dinormalkan agar jumlahnya satu.

        Dengan begitu, memahami perilaku jangka panjang sistem cukup dengan melihat satu eigenvector. Teori menjamin eigenvalue terbesar matriks transisi adalah satu, dan sisanya bernilai mutlak kurang dari atau sama dengan satu. Bila rantainya tak reduksibel dan aperiodik, eigenvalue satu itu unik, dan konvergensi pasti terjadi. Contoh pemakaiannya: prakiraan cuaca sederhana, model perilaku pengguna, dan pembangkit teks tingkat kata.
        """),
        C(
            """
            import numpy as np

            P = np.array([[0.9, 0.1],
                          [0.5, 0.5]])
            pi = np.array([1.0, 0.0])
            for _ in range(50):
                pi = pi @ P
            print(pi.round(4).tolist())

            nilai, vektor = np.linalg.eig(P.T)
            i = int(np.argmax(nilai.real))
            stasioner = vektor[:, i].real
            stasioner = stasioner / stasioner.sum()
            print(round(float(nilai[i].real), 4), stasioner.round(4).tolist())
            print(np.allclose(stasioner @ P, stasioner))
            print(sorted(np.abs(nilai).round(4).tolist()))
            """,
            """
            [0.8333, 0.1667]
            1.0 [0.8333, 0.1667]
            True
            [0.4, 1.0]
            """,
            """
            Iterasi dari keadaan awal mana pun menuju distribusi stasioner `[5/6, 1/6]`. Distribusi itu adalah eigenvector `P^T` untuk eigenvalue satu, dan eigenvalue lainnya bernilai mutlak kurang dari satu.
            """,
            filename="rantai_markov.py",
        ),
        K(
            "tip",
            """
            Distribusi stasioner adalah eigenvector dari `P` transpos, bukan dari `P`. Ingat normalisasinya: bagi dengan jumlah elemen agar total peluang sama dengan satu, bukan dengan norma panjang.
            """,
            title="Dua jebakan klasik",
        ),
        T("""
        ## PageRank mini

        **PageRank** menilai pentingnya halaman web berdasarkan tautan masuk, dengan gagasan bahwa halaman penting adalah yang ditautkan oleh halaman penting lainnya. Bayangkan peselancar acak yang di setiap langkah mengikuti satu tautan keluar secara acak. Proporsi waktu jangka panjang yang ia habiskan di tiap halaman adalah skor halaman itu, yaitu distribusi stasioner rantai Markov web.

        Agar rantai selalu konvergen, dipakai faktor redaman `d`, biasanya 0,85: dengan peluang `d` peselancar mengikuti tautan, dan dengan peluang `1 - d` ia melompat ke halaman acak. Matriks yang terbentuk, `d M + (1 - d)/n * 1`, bersifat positif sehingga eigenvalue satunya unik, dan power iteration menemukan skornya dengan cepat.

        Peselancar acak itu hanyalah model, tetapi model sederhana ini terbukti sangat andal dalam memeringkat halaman. Ide ini jauh melampaui web. Ia dipakai untuk memeringkat simpul penting pada jaringan sosial, sitasi ilmiah, dan graf pengetahuan. Dengan eigenvector, pertanyaan "siapa yang berpengaruh" dijawab dengan satu perhitungan aljabar linear.
        """),
        C(
            """
            import numpy as np

            tautan = {0: [1, 2], 1: [2], 2: [0], 3: [2]}
            n = 4
            M = np.zeros((n, n))
            for dari, ke in tautan.items():
                for t in ke:
                    M[t, dari] = 1.0 / len(ke)
            d = 0.85
            G = d * M + (1 - d) / n * np.ones((n, n))
            r = np.ones(n) / n
            for _ in range(100):
                r = G @ r
            print(r.round(4).tolist(), round(float(r.sum()), 4))
            print(int(np.argmax(r)), int(np.argmin(r)))
            nilai, vektor = np.linalg.eig(G)
            i = int(np.argmax(nilai.real))
            v = vektor[:, i].real
            v = v / v.sum()
            print(np.allclose(v, r, atol=1e-6))
            """,
            """
            [0.3725, 0.1958, 0.3941, 0.0375] 1.0
            2 3
            True
            """,
            """
            Halaman 2 menerima tautan dari tiga halaman sehingga skornya tertinggi, sedangkan halaman 3 tanpa tautan masuk memiliki skor terendah. Hasil iterasi sama dengan eigenvector utama.
            """,
            filename="pagerank_mini.py",
        ),
        T("""
        ## Eigenvalue kovariansi dan arah utama

        Hubungan terpenting dengan data science: eigenvector matriks kovariansi adalah **arah utama** variasi data, dan eigenvalue-nya adalah variansi sepanjang arah itu. Eigenvector dengan eigenvalue terbesar menunjuk arah tempat data paling menyebar. Jumlah semua eigenvalue sama dengan jumlah variansi semua fitur, yaitu trace kovariansi.

        Proporsi variansi yang dijelaskan sebuah arah adalah eigenvalue-nya dibagi total. Bila dua eigenvalue pertama menjelaskan sembilan puluh lima persen variansi, data berdimensi tinggi pada dasarnya hidup dekat bidang dua dimensi, dan kita bisa mereduksinya tanpa banyak kehilangan informasi. Itulah PCA, topik modul terakhir kursus ini.

        Pahami dulu hubungan ini dengan baik, karena hampir semua metode reduksi dimensi bertumpu padanya. Latihan berikut membangun alat dasar yang akan dipakai di sana: power iteration, distribusi stasioner, dan proporsi variansi dari eigenvalue.
        """),
        E(
            "A2-05-3-ex1",
            "mudah",
            """
            Tulis fungsi `langkah_markov(pi, P)` yang mengembalikan vektor peluang baru `pi P` (list) dibulatkan 6 desimal untuk vektor baris `pi` dan matriks transisi `P` (list of list).
            """,
            """
            def langkah_markov(pi, P):
                # TODO: implementasikan
                pass
            """,
            """
            P = [[0.9, 0.1], [0.5, 0.5]]
            assert langkah_markov([1, 0], P) == [0.9, 0.1]
            assert langkah_markov([0.5, 0.5], P) == [0.7, 0.3]
            assert langkah_markov([0, 1], P) == [0.5, 0.5]
            assert langkah_markov([1], [[1]]) == [1.0]
            """,
            "Tiap komponen baru adalah jumlah pi[i] kali P[i][j].",
            """
            def langkah_markov(pi, P):
                n = len(P[0])
                return [round(sum(pi[i] * P[i][j] for i in range(len(pi))) + 0.0, 6) for j in range(n)]
            """,
        ),
        E(
            "A2-05-3-ex2",
            "mudah",
            """
            Tulis fungsi `proporsi_variansi(eigenvalue)` yang mengembalikan list proporsi tiap eigenvalue terhadap totalnya, terurut menurun, dibulatkan 4 desimal.
            """,
            """
            def proporsi_variansi(eigenvalue):
                # TODO: implementasikan
                pass
            """,
            """
            assert proporsi_variansi([1, 3]) == [0.75, 0.25]
            assert proporsi_variansi([2, 2, 4]) == [0.5, 0.25, 0.25]
            assert proporsi_variansi([5]) == [1.0]
            assert proporsi_variansi([1, 1, 1, 1]) == [0.25, 0.25, 0.25, 0.25]
            """,
            "Urutkan menurun lalu bagi tiap nilai dengan jumlah semuanya.",
            """
            def proporsi_variansi(eigenvalue):
                total = sum(eigenvalue)
                return [round(x / total, 4) for x in sorted(eigenvalue, reverse=True)]
            """,
        ),
        E(
            "A2-05-3-ex3",
            "sedang",
            """
            Tulis fungsi `eigenvalue_dominan(A, langkah=200)` yang menghitung eigenvalue terbesar mutlak matriks persegi `A` (list of list) dengan power iteration mulai dari vektor semua satu, tanpa NumPy. Kembalikan hasil dibulatkan 4 desimal. Gunakan hasil bagi Rayleigh `v.T A v` dengan `v` ternormalisasi.
            """,
            """
            def eigenvalue_dominan(A, langkah=200):
                # TODO: implementasikan
                pass
            """,
            """
            assert eigenvalue_dominan([[2, 0], [0, 3]]) == 3.0
            assert eigenvalue_dominan([[4, 2], [2, 3]]) == 5.5616
            assert eigenvalue_dominan([[2, 1], [1, 2]]) == 3.0
            assert eigenvalue_dominan([[2, 1, 0], [1, 3, 1], [0, 1, 4]]) == 4.7321
            """,
            "Kalikan matriks dengan v, normalkan, ulangi, lalu hitung v dot (A v) pada akhir.",
            """
            def eigenvalue_dominan(A, langkah=200):
                n = len(A)
                v = [1.0] * n
                def kali(v):
                    return [sum(a * b for a, b in zip(baris, v)) for baris in A]
                for _ in range(langkah):
                    w = kali(v)
                    norma = sum(x * x for x in w) ** 0.5
                    v = [x / norma for x in w]
                av = kali(v)
                return round(sum(a * b for a, b in zip(v, av)), 4)
            """,
        ),
        E(
            "A2-05-3-ex4",
            "menantang",
            """
            Tulis fungsi `distribusi_stasioner(P, langkah=500)` yang mengembalikan distribusi stasioner matriks transisi `P` (list of list, baris berjumlah satu, rantai tak reduksibel dan aperiodik) dengan mengulang perkalian `pi P` dari distribusi seragam. Kembalikan list dibulatkan 4 desimal.
            """,
            """
            def distribusi_stasioner(P, langkah=500):
                # TODO: implementasikan
                pass
            """,
            """
            assert distribusi_stasioner([[0.9, 0.1], [0.5, 0.5]]) == [0.8333, 0.1667]
            assert distribusi_stasioner([[0.5, 0.5], [0.5, 0.5]]) == [0.5, 0.5]
            r = distribusi_stasioner([[0.5, 0.25, 0.25], [0.5, 0.0, 0.5], [0.25, 0.25, 0.5]])
            assert r == [0.4, 0.2, 0.4]
            assert abs(sum(distribusi_stasioner([[0.2, 0.8], [0.6, 0.4]])) - 1) < 1e-3
            """,
            "Mulai dari 1/n untuk tiap keadaan dan kalikan berulang dengan P.",
            """
            def distribusi_stasioner(P, langkah=500):
                n = len(P)
                pi = [1.0 / n] * n
                for _ in range(langkah):
                    pi = [sum(pi[i] * P[i][j] for i in range(n)) for j in range(n)]
                return [round(x, 4) for x in pi]
            """,
        ),
    ],
    [
        M("Mengambil eigenvector P bukan P transpos untuk distribusi stasioner.", "Pakai P transpos untuk vektor kolom atau pi P untuk vektor baris."),
        M("Menormalkan distribusi dengan norma panjang.", "Bagi dengan jumlah elemen agar total satu."),
        M("Mengira power iteration memberi semua eigenvalue.", "Ia hanya memberi eigenvalue dominan."),
    ],
    [
        Q("Apa yang dihitung power iteration?", ["Semua eigenvalue", "Eigenvalue terbesar mutlak", "Determinan", "Invers"], 1, "Komponen dominan tumbuh paling cepat.", hint="Dominan."),
        Q("Distribusi stasioner memenuhi?", ["pi P = pi", "pi P = 0", "pi + P = 1", "P = I"], 0, "Tidak berubah setelah satu langkah.", hint="Eigenvalue satu."),
        Q("Jumlah tiap baris matriks transisi?", ["0", "1", "n", "Bebas"], 1, "Peluang total dari satu keadaan adalah satu.", hint="Peluang."),
        Q("Apa fungsi faktor redaman PageRank?", ["Mempercepat web", "Menjamin konvergensi lewat lompatan acak", "Menghapus tautan", "Mengurutkan"], 1, "Membuat matriks positif.", hint="Peselancar acak."),
        Q("Eigenvalue kovariansi menyatakan?", ["Mean", "Variansi sepanjang arah utama", "Korelasi", "Jumlah data"], 1, "Eigenvector menunjuk arah dan eigenvalue memberi variansi.", hint="PCA."),
    ],
    [
        "Power iteration menemukan eigenvalue dominan lewat perkalian berulang dan normalisasi.",
        "Distribusi stasioner rantai Markov adalah eigenvector P transpos untuk eigenvalue satu.",
        "PageRank adalah distribusi stasioner peselancar acak dengan redaman.",
        "Eigenvalue kovariansi memberi variansi sepanjang arah utama data.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa perhitungan dan contoh kode yang cukup jelas dalam teks.", "brief": []}

write_module(
    "A2",
    5,
    "Eigenvalue dan eigenvector",
    105,
    [
        "Menghitung dan menafsirkan eigenvalue serta eigenvector",
        "Memakai diagonalisasi dan dekomposisi spektral",
        "Menerapkan eigen pada power iteration, rantai Markov, dan PageRank",
    ],
    [l1, l2, l3],
    video,
    REF,
)
