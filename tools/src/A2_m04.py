import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

l1 = lesson(
    "A2-04-1",
    "Determinan",
    35,
    [
        "Menghitung determinan matriks 2x2 dan 3x3",
        "Menafsirkan determinan sebagai faktor perubahan luas atau volume",
        "Memakai sifat-sifat determinan untuk menyederhanakan perhitungan",
        "Mengaitkan determinan nol dengan matriks singular",
    ],
    [
        T("""
        ## Apa itu determinan

        **Determinan** adalah satu bilangan yang dihitung dari matriks persegi dan merangkum sifat pentingnya. Untuk matriks `2 x 2`, `[[a, b], [c, d]]`, determinannya `a d - b c`. Untuk `[[3, 1], [2, 4]]` hasilnya `12 - 2 = 10`. Determinan hanya terdefinisi untuk matriks persegi.

        Bilangan ini menjawab pertanyaan penting: apakah matriks bisa dibalik? Matriks punya invers tepat ketika determinannya tidak nol. Ia juga memberi tahu bagaimana transformasi yang diwakili matriks itu mengubah ukuran ruang. Dua tafsir ini, kemampuan dibalik dan faktor penskalaan, membuat determinan sangat berguna.

        Dalam praktik data, determinan jarang dihitung langsung untuk matriks besar karena rawan masalah numerik, tetapi pemahaman konsepnya diperlukan untuk menalar kapan sebuah sistem punya solusi tunggal dan kapan sebuah model mengalami masalah kolinearitas.
        """),
        C(
            """
            import numpy as np

            A = np.array([[3.0, 1.0], [2.0, 4.0]])
            print(round(float(np.linalg.det(A)), 6), 3 * 4 - 1 * 2)
            B = np.array([[1.0, 2.0], [2.0, 4.0]])
            print(round(float(np.linalg.det(B)), 6))
            I = np.eye(3)
            print(round(float(np.linalg.det(I)), 6))
            D = np.diag([2.0, 3.0, 4.0])
            print(round(float(np.linalg.det(D)), 6))
            C3 = np.array([[2.0, 0.0, 1.0], [1.0, 3.0, 2.0], [1.0, 1.0, 2.0]])
            print(round(float(np.linalg.det(C3)), 6))
            """,
            """
            10.0 10
            0.0
            1.0
            24.0
            6.0
            """,
            """
            Determinan matriks 2x2 adalah `ad - bc`. Matriks dengan baris kelipatan satu sama lain punya determinan nol, identitas bernilai satu, dan matriks diagonal bernilai hasil kali diagonalnya.
            """,
            filename="determinan_dasar.py",
        ),
        T("""
        ## Ekspansi kofaktor untuk 3x3

        Untuk matriks `3 x 3` kita bisa menghitung determinan dengan **ekspansi kofaktor** sepanjang baris pertama: `det = a11 * M11 - a12 * M12 + a13 * M13`, dengan `Mij` determinan `2 x 2` yang tersisa setelah menghapus baris `i` dan kolom `j`. Tanda bergantian plus dan minus seperti papan catur.

        Metode ini bekerja untuk ukuran berapa pun secara rekursif, tetapi biayanya tumbuh seperti faktorial, sehingga tidak praktis untuk matriks besar. Untuk `10 x 10` saja sudah jutaan operasi. Itulah mengapa perangkat lunak memakai eliminasi, yang hanya butuh sekitar `n` pangkat tiga operasi.

        Namun ekspansi kofaktor tetap penting untuk dipahami karena melatih intuisi dan muncul pada rumus teoretis seperti aturan Cramer dan rumus invers lewat adjugat. Kamu akan mengimplementasikannya sendiri di latihan.
        """),
        C(
            """
            def det2(m):
                return m[0][0] * m[1][1] - m[0][1] * m[1][0]

            def minor(m, i, j):
                return [[m[r][c] for c in range(len(m)) if c != j] for r in range(len(m)) if r != i]

            def det(m):
                if len(m) == 1:
                    return m[0][0]
                if len(m) == 2:
                    return det2(m)
                return sum((-1) ** j * m[0][j] * det(minor(m, 0, j)) for j in range(len(m)))

            A = [[2, 0, 1], [1, 3, 2], [1, 1, 2]]
            print(det(A))
            print(det([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
            print(det([[2, 0, 0, 0], [0, 3, 0, 0], [0, 0, 4, 0], [0, 0, 0, 5]]))
            print(det([[0, 1], [1, 0]]))
            """,
            """
            6
            0
            120
            -1
            """,
            """
            Ekspansi kofaktor rekursif menghitung determinan. Matriks `[[1,2,3],[4,5,6],[7,8,9]]` singular karena barisnya bergantung linear, dan menukar baris identitas memberi determinan minus satu.
            """,
            filename="kofaktor.py",
        ),
        T("""
        ## Tafsir geometris

        Determinan adalah faktor penskalaan luas atau volume. Dua kolom matriks `2 x 2` membentuk jajar genjang, dan **nilai mutlak determinan sama dengan luas jajar genjang itu**. Untuk `3 x 3`, tiga kolom membentuk paralelepipedum, dan nilai mutlak determinan adalah volumenya. Matriks yang mengubah vektor basis satuan menjadi kolom-kolomnya memetakan persegi satuan menjadi jajar genjang tersebut.

        Tanda determinan memberi informasi orientasi. Determinan positif berarti transformasi menjaga orientasi, seperti rotasi. Determinan negatif berarti ada pemantulan yang membalik orientasi. Determinan nol berarti ruang dipampatkan ke dimensi lebih rendah: bidang menjadi garis atau titik, volume menjadi nol, dan informasi hilang sehingga transformasi tidak bisa dibalik.

        Karena itu determinan nol identik dengan kolom-kolom yang bergantung linear: jajar genjang yang mereka bentuk datar sehingga luasnya nol.
        """),
        C(
            """
            import numpy as np

            a = np.array([3.0, 0.0])
            b = np.array([1.0, 2.0])
            M = np.column_stack([a, b])
            print(round(float(np.linalg.det(M)), 6))
            segitiga = 0.5 * abs(np.linalg.det(M))
            print(round(float(segitiga), 6))

            skala = np.array([[2.0, 0.0], [0.0, 3.0]])
            rotasi = np.array([[0.0, -1.0], [1.0, 0.0]])
            pantul = np.array([[1.0, 0.0], [0.0, -1.0]])
            for nama, T_ in [("skala", skala), ("rotasi", rotasi), ("pantul", pantul)]:
                print(nama, round(float(np.linalg.det(T_)), 6))

            datar = np.array([[1.0, 2.0], [2.0, 4.0]])
            print(round(float(np.linalg.det(datar)), 6))
            """,
            """
            6.0
            3.0
            skala 6.0
            rotasi 1.0
            pantul -1.0
            0.0
            """,
            """
            Luas jajar genjang dari dua kolom sama dengan nilai mutlak determinan. Skala dua kali tiga memperbesar luas enam kali, rotasi menjaga luas, dan pemantulan memberi determinan negatif.
            """,
            filename="determinan_geometri.py",
        ),
        K(
            "tip",
            """
            Determinan nol, kolom bergantung linear, peringkat kurang dari penuh, dan matriks singular adalah empat cara menyatakan hal yang sama pada matriks persegi.
            """,
            title="Satu gagasan, empat nama",
        ),
        T("""
        ## Sifat-sifat penting

        Beberapa sifat membuat determinan mudah dimanipulasi. Pertama, `det(A B) = det(A) det(B)`: determinan hasil kali sama dengan hasil kali determinan. Kedua, `det(A^T) = det(A)`. Ketiga, menukar dua baris membalik tanda. Keempat, mengalikan satu baris dengan `k` mengalikan determinan dengan `k`. Kelima, menambahkan kelipatan satu baris ke baris lain tidak mengubah determinan.

        Sifat kelima adalah dasar menghitung determinan dengan eliminasi: kita mengubah matriks menjadi segitiga tanpa mengubah determinan (kecuali tanda saat menukar baris), lalu mengalikan elemen diagonal. Untuk matriks segitiga, determinan memang hasil kali diagonal.

        Perhatikan bahwa `det(A + B)` secara umum **tidak** sama dengan `det(A) + det(B)`. Determinan tidak linear terhadap penjumlahan matriks, kesalahan yang cukup sering dibuat.
        """),
        C(
            """
            import numpy as np

            A = np.array([[2.0, 1.0], [1.0, 3.0]])
            B = np.array([[1.0, 4.0], [0.0, 2.0]])
            d = lambda m: round(float(np.linalg.det(m)), 6)
            print(d(A), d(B), d(A @ B), d(A) * d(B))
            print(d(A.T) == d(A))
            tukar = A[[1, 0]]
            print(d(tukar))
            skala_baris = A.copy()
            skala_baris[0] *= 5
            print(d(skala_baris))
            tambah = A.copy()
            tambah[1] += 3 * tambah[0]
            print(d(tambah))
            print(d(A + B), d(A) + d(B))
            """,
            """
            5.0 2.0 10.0 10.0
            True
            -5.0
            25.0
            5.0
            10.0 7.0
            """,
            """
            Determinan hasil kali sama dengan hasil kali determinan. Menukar baris membalik tanda, menskalakan baris mengalikan determinan, dan menambah kelipatan baris tidak mengubahnya. Determinan jumlah tidak sama dengan jumlah determinan.
            """,
            filename="sifat_determinan.py",
        ),
        T("""
        ## Kapan determinan menyesatkan

        Determinan kecil tidak selalu berarti matriks hampir singular, dan determinan besar tidak menjamin kondisi baik. Matriks `0.1` dikali identitas `10 x 10` punya determinan `1e-10` yang sangat kecil, padahal matriks itu sempurna berkondisi baik. Ukuran ketunggalan yang benar adalah bilangan kondisi atau nilai singular terkecil, bukan determinan.

        Selain itu, determinan matriks besar mudah menghasilkan luapan atau underflow karena hasil kali banyak angka. Untuk kebutuhan seperti kemungkinan Gaussian multivariat, dipakai logaritma determinan lewat `np.linalg.slogdet` yang stabil. Gunakan determinan sebagai alat konsep, dan alat numerik lain untuk keputusan praktis.
        """),
        E(
            "A2-04-1-ex1",
            "mudah",
            """
            Tulis fungsi `det2(m)` yang mengembalikan determinan matriks 2x2 (list of list).
            """,
            """
            def det2(m):
                # TODO: implementasikan
                pass
            """,
            """
            assert det2([[3, 1], [2, 4]]) == 10
            assert det2([[1, 2], [2, 4]]) == 0
            assert det2([[0, 1], [1, 0]]) == -1
            assert det2([[5, 0], [0, 5]]) == 25
            """,
            "Hitung a d dikurangi b c.",
            """
            def det2(m):
                return m[0][0] * m[1][1] - m[0][1] * m[1][0]
            """,
        ),
        E(
            "A2-04-1-ex2",
            "mudah",
            """
            Tulis fungsi `luas_jajar_genjang(u, v)` yang mengembalikan luas jajar genjang dari dua vektor 2D `u` dan `v` (nilai mutlak determinan matriks dengan kolom `u` dan `v`).
            """,
            """
            def luas_jajar_genjang(u, v):
                # TODO: implementasikan
                pass
            """,
            """
            assert luas_jajar_genjang([3, 0], [1, 2]) == 6
            assert luas_jajar_genjang([1, 0], [0, 1]) == 1
            assert luas_jajar_genjang([1, 2], [2, 4]) == 0
            assert luas_jajar_genjang([0, 1], [1, 0]) == 1
            """,
            "Determinan 2x2 dengan kolom u dan v adalah u0 v1 dikurangi v0 u1.",
            """
            def luas_jajar_genjang(u, v):
                return abs(u[0] * v[1] - v[0] * u[1])
            """,
        ),
        E(
            "A2-04-1-ex3",
            "sedang",
            """
            Tulis fungsi `determinan(m)` yang menghitung determinan matriks persegi (list of list, boleh ukuran berapa pun) dengan ekspansi kofaktor sepanjang baris pertama. Matriks 1x1 mengembalikan elemennya.
            """,
            """
            def determinan(m):
                # TODO: implementasikan
                pass
            """,
            """
            assert determinan([[7]]) == 7
            assert determinan([[3, 1], [2, 4]]) == 10
            assert determinan([[2, 0, 1], [1, 3, 2], [1, 1, 2]]) == 6
            assert determinan([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == 0
            assert determinan([[2, 0, 0, 0], [0, 3, 0, 0], [0, 0, 4, 0], [0, 0, 0, 5]]) == 120
            """,
            "Rekursi dengan tanda bergantian dan matriks minor tanpa baris 0 dan kolom j.",
            """
            def determinan(m):
                if len(m) == 1:
                    return m[0][0]
                total = 0
                for j in range(len(m)):
                    minor = [baris[:j] + baris[j + 1:] for baris in m[1:]]
                    total += (-1) ** j * m[0][j] * determinan(minor)
                return total
            """,
        ),
        E(
            "A2-04-1-ex4",
            "menantang",
            """
            Tulis fungsi `determinan_eliminasi(m)` yang menghitung determinan lewat eliminasi dengan pivoting sebagian tanpa NumPy. Kembalikan hasil dibulatkan 6 desimal. Ingat setiap penukaran baris membalik tanda, dan bila pivot terbesar nol kembalikan 0.0.
            """,
            """
            def determinan_eliminasi(m):
                # TODO: implementasikan
                pass
            """,
            """
            assert determinan_eliminasi([[3, 1], [2, 4]]) == 10.0
            assert determinan_eliminasi([[2, 0, 1], [1, 3, 2], [1, 1, 2]]) == 6.0
            assert determinan_eliminasi([[1, 2], [2, 4]]) == 0.0
            assert determinan_eliminasi([[0, 1], [1, 0]]) == -1.0
            assert determinan_eliminasi([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == 0.0
            """,
            "Pilih pivot terbesar, tukar baris dan balik tanda, hilangkan elemen di bawah pivot, lalu kalikan diagonal.",
            """
            def determinan_eliminasi(m):
                n = len(m)
                a = [list(map(float, b)) for b in m]
                tanda = 1.0
                for k in range(n):
                    p = max(range(k, n), key=lambda i: abs(a[i][k]))
                    if abs(a[p][k]) < 1e-12:
                        return 0.0
                    if p != k:
                        a[k], a[p] = a[p], a[k]
                        tanda = -tanda
                    for i in range(k + 1, n):
                        f = a[i][k] / a[k][k]
                        a[i] = [x - f * y for x, y in zip(a[i], a[k])]
                hasil = tanda
                for k in range(n):
                    hasil *= a[k][k]
                return round(hasil + 0.0, 6)
            """,
        ),
    ],
    [
        M("Menganggap det(A + B) = det(A) + det(B).", "Determinan tidak linear terhadap penjumlahan, tetapi det(AB) = det(A) det(B)."),
        M("Menilai kondisi matriks dari besar kecilnya determinan.", "Pakai bilangan kondisi atau nilai singular."),
        M("Lupa membalik tanda saat menukar baris.", "Setiap penukaran baris membalik tanda determinan."),
    ],
    [
        Q("Determinan [[3,1],[2,4]]?", ["14", "10", "12", "2"], 1, "3 kali 4 dikurangi 1 kali 2 sama dengan 10.", hint="ad dikurangi bc."),
        Q("Apa arti determinan nol?", ["Matriks identitas", "Matriks singular tak punya invers", "Matriks simetris", "Matriks ortogonal"], 1, "Ruang dipampatkan sehingga transformasi tidak bisa dibalik.", hint="Kolom bergantung linear."),
        Q("Nilai mutlak determinan 2x2 sama dengan?", ["Panjang kolom", "Luas jajar genjang dari kolom", "Jumlah elemen", "Peringkat"], 1, "Ia faktor perubahan luas.", hint="Geometri."),
        Q("det(AB) sama dengan?", ["det A + det B", "det A kali det B", "det A dibagi det B", "det(BA)^2"], 1, "Determinan bersifat multiplikatif.", hint="Kali."),
        Q("Efek menukar dua baris pada determinan?", ["Tidak berubah", "Tanda terbalik", "Menjadi nol", "Dikuadratkan"], 1, "Tanda berganti.", hint="Orientasi."),
    ],
    [
        "Determinan merangkum apakah matriks bisa dibalik dan bagaimana ia menskalakan luas atau volume.",
        "Ekspansi kofaktor bersifat rekursif, eliminasi jauh lebih efisien.",
        "det(AB) = det(A) det(B) tetapi determinan tidak linear terhadap penjumlahan.",
        "Gunakan bilangan kondisi, bukan determinan, untuk menilai kedekatan dengan singular.",
    ],
    [],
)

l2 = lesson(
    "A2-04-2",
    "Matriks invers",
    35,
    [
        "Memahami definisi invers dan kapan invers ada",
        "Menghitung invers 2x2 dengan rumus dan invers umum dengan NumPy",
        "Memakai sifat invers dan memeriksa hasilnya",
        "Memahami mengapa solve lebih baik daripada invers eksplisit",
    ],
    [
        T("""
        ## Definisi invers

        **Invers** matriks persegi `A`, ditulis `A^-1`, adalah matriks yang memenuhi `A A^-1 = A^-1 A = I`. Ia berperan seperti kebalikan bilangan: mengalikan dengan `A` lalu dengan `A^-1` mengembalikan keadaan semula. Bila `A` mewakili transformasi, `A^-1` membatalkannya.

        Invers hanya ada bila `A` persegi dan determinannya tidak nol. Matriks yang punya invers disebut *invertible* atau tak singular. Bila ada, inversnya tunggal. Matriks yang determinannya nol disebut singular dan tidak punya invers, karena transformasinya memampatkan ruang dan informasi tidak bisa dipulihkan.

        Bila `A` invertible, sistem `A x = b` punya tepat satu solusi, yaitu `x = A^-1 b`. Rumus ini indah secara konsep, tetapi seperti akan dijelaskan, jarang dipakai persis begitu dalam komputasi nyata.
        """),
        C(
            """
            import numpy as np

            A = np.array([[4.0, 7.0], [2.0, 6.0]])
            Ainv = np.linalg.inv(A)
            print(Ainv.round(4).tolist())
            print(np.allclose(A @ Ainv, np.eye(2)), np.allclose(Ainv @ A, np.eye(2)))
            b = np.array([1.0, 2.0])
            print((Ainv @ b).round(4).tolist(), np.linalg.solve(A, b).round(4).tolist())
            S = np.array([[1.0, 2.0], [2.0, 4.0]])
            try:
                np.linalg.inv(S)
            except np.linalg.LinAlgError:
                print("singular")
            """,
            """
            [[0.6, -0.7], [-0.2, 0.4]]
            True True
            [-0.8, 0.6] [-0.8, 0.6]
            singular
            """,
            """
            `inv` menghasilkan matriks yang bila dikalikan dengan `A` memberi identitas. Matriks singular memicu `LinAlgError`.
            """,
            filename="invers_dasar.py",
        ),
        T("""
        ## Rumus invers 2x2

        Untuk matriks `2 x 2`, `[[a, b], [c, d]]`, inversnya punya rumus tertutup: `(1 / (a d - b c)) * [[d, -b], [-c, a]]`. Tukar elemen diagonal, balik tanda elemen luar diagonal, lalu bagi dengan determinan. Rumus ini juga menunjukkan secara langsung bahwa determinan nol membuat invers tidak terdefinisi karena pembagian dengan nol.

        Untuk ukuran lebih besar, rumus serupa memakai matriks adjugat (transpos matriks kofaktor) dibagi determinan, tetapi tidak dipakai dalam praktik karena sangat mahal. Metode praktis adalah eliminasi Gauss-Jordan pada matriks augmented `[A | I]`: setelah `A` menjadi identitas, bagian kanan menjadi `A^-1`.

        Menghafal rumus 2x2 sangat berguna untuk pemeriksaan cepat dengan tangan, sebab banyak contoh mini di buku dan ujian memakainya.
        """),
        C(
            """
            def invers2(m):
                (a, b), (c, d) = m
                det = a * d - b * c
                if det == 0:
                    return None
                return [[d / det, -b / det], [-c / det, a / det]]

            print(invers2([[4, 7], [2, 6]]))
            print(invers2([[1, 2], [2, 4]]))
            print(invers2([[2, 0], [0, 5]]))

            import numpy as np
            print(np.allclose(invers2([[3, 1], [5, 2]]), np.linalg.inv(np.array([[3.0, 1.0], [5.0, 2.0]]))))
            """,
            """
            [[0.6, -0.7], [-0.2, 0.4]]
            None
            [[0.5, 0.0], [0.0, 0.2]]
            True
            """,
            """
            Rumus tertutup memberi invers 2x2 dan mengenali kasus singular. Hasilnya cocok dengan `np.linalg.inv`.
            """,
            filename="invers_2x2.py",
        ),
        K(
            "warning",
            """
            Jangan menyelesaikan `A x = b` dengan `np.linalg.inv(A) @ b`. Pakai `np.linalg.solve(A, b)` yang lebih cepat dan lebih akurat. Invers eksplisit jarang benar-benar dibutuhkan.
            """,
            title="Hindari invers eksplisit",
        ),
        T("""
        ## Sifat-sifat invers

        Beberapa sifat penting. Invers dari invers adalah matriks asal: `(A^-1)^-1 = A`. Invers hasil kali membalik urutan: `(A B)^-1 = B^-1 A^-1`, sama seperti memakai kaus kaki lalu sepatu, lalu melepasnya dalam urutan terbalik. Invers transpos sama dengan transpos invers: `(A^T)^-1 = (A^-1)^T`. Dan `det(A^-1) = 1 / det(A)`.

        Untuk matriks diagonal, inversnya adalah matriks diagonal dengan elemen kebalikan. Untuk matriks ortogonal, inversnya adalah transposnya. Mengenali struktur ini menghemat banyak komputasi: tidak perlu algoritma umum bila struktur sederhana tersedia.

        Sifat `(A B)^-1 = B^-1 A^-1` sering menjebak pemula yang menulis `A^-1 B^-1`. Hasilnya berbeda karena perkalian matriks tidak komutatif. Verifikasi numerik di bawah menunjukkan semua sifat tersebut.
        """),
        C(
            """
            import numpy as np

            A = np.array([[2.0, 1.0], [1.0, 3.0]])
            B = np.array([[1.0, 2.0], [0.0, 1.0]])
            inv = np.linalg.inv
            print(np.allclose(inv(inv(A)), A))
            print(np.allclose(inv(A @ B), inv(B) @ inv(A)))
            print(np.allclose(inv(A @ B), inv(A) @ inv(B)))
            print(np.allclose(inv(A.T), inv(A).T))
            print(round(float(np.linalg.det(inv(A))), 6), round(1 / float(np.linalg.det(A)), 6))
            D = np.diag([2.0, 4.0, 5.0])
            print(np.diag(inv(D)).tolist())
            """,
            """
            True
            True
            False
            True
            0.2 0.2
            [0.5, 0.25, 0.2]
            """,
            """
            Invers hasil kali membalik urutan faktor, sedangkan mempertahankan urutan memberi hasil salah. Invers matriks diagonal berisi kebalikan elemen diagonal.
            """,
            filename="sifat_invers.py",
        ),
        T("""
        ## Mengapa solve lebih baik

        Menghitung `A^-1` penuh membutuhkan sekitar tiga kali biaya menyelesaikan satu sistem, dan hasilnya membawa lebih banyak galat pembulatan. Bila yang kamu butuhkan hanyalah `x = A^-1 b`, menyelesaikan `A x = b` langsung dengan faktorisasi LU lebih cepat dan lebih akurat. Menyimpan invers juga boros untuk matriks besar yang jarang.

        Invers eksplisit memang kadang dibutuhkan, misalnya saat kamu ingin kovariansi parameter dalam regresi, `(X^T X)^-1`, atau elemen diagonalnya. Bahkan di sana, pustaka statistik memakai dekomposisi stabil di balik layar dan hanya menghitung bagian yang dibutuhkan.

        Pegangan praktis: bila kamu menulis `inv` di kodemu, tanyakan apakah `solve` cukup. Hampir selalu jawabannya ya. Latihan berikut membangun invers dari nol agar kamu paham cara kerjanya, tetapi di proyek nyata pakai fungsi pustaka.
        """),
        T("""
        ## Invers dan transformasi

        Bila `A` mewakili transformasi, `A^-1` adalah transformasi yang mengembalikan semuanya ke keadaan awal. Rotasi sebesar sudut tertentu dibatalkan oleh rotasi dengan sudut berlawanan, dan penskalaan dua kali dibatalkan oleh penskalaan setengah. Gambaran ini membantu memeriksa kewajaran sebuah invers: bila hasilmu tidak membatalkan transformasi aslinya, ada yang salah.

        Dalam grafika komputer dan robotika, rantai transformasi dibalik dengan membalik urutan inversnya, persis sifat `(AB)^-1 = B^-1 A^-1`. Dalam data science, pemutihan data (*whitening*) memakai invers akar kovariansi untuk membuat fitur tak berkorelasi dengan variansi satu. Konsep invers jadi terasa nyata ketika kamu melihatnya sebagai pembatalan operasi.
        """),
        E(
            "A2-04-2-ex1",
            "mudah",
            """
            Tulis fungsi `invers2(m)` yang mengembalikan invers matriks 2x2 (list of list) dengan nilai dibulatkan 6 desimal, atau `None` bila determinan nol.
            """,
            """
            def invers2(m):
                # TODO: implementasikan
                pass
            """,
            """
            assert invers2([[4, 7], [2, 6]]) == [[0.6, -0.7], [-0.2, 0.4]]
            assert invers2([[1, 2], [2, 4]]) is None
            assert invers2([[2, 0], [0, 4]]) == [[0.5, 0.0], [0.0, 0.25]]
            assert invers2([[1, 0], [0, 1]]) == [[1.0, 0.0], [0.0, 1.0]]
            """,
            "Gunakan rumus tertutup dan tambahkan 0.0 untuk menghindari nol negatif bila perlu.",
            """
            def invers2(m):
                (a, b), (c, d) = m
                det = a * d - b * c
                if det == 0:
                    return None
                return [[round(d / det + 0.0, 6), round(-b / det + 0.0, 6)], [round(-c / det + 0.0, 6), round(a / det + 0.0, 6)]]
            """,
        ),
        E(
            "A2-04-2-ex2",
            "mudah",
            """
            Tulis fungsi `bisa_dibalik(m)` yang mengembalikan `True` bila matriks 2x2 punya invers.
            """,
            """
            def bisa_dibalik(m):
                # TODO: implementasikan
                pass
            """,
            """
            assert bisa_dibalik([[4, 7], [2, 6]]) is True
            assert bisa_dibalik([[1, 2], [2, 4]]) is False
            assert bisa_dibalik([[0, 1], [1, 0]]) is True
            assert bisa_dibalik([[0, 0], [0, 0]]) is False
            """,
            "Determinan harus tidak nol.",
            """
            def bisa_dibalik(m):
                return m[0][0] * m[1][1] - m[0][1] * m[1][0] != 0
            """,
        ),
        E(
            "A2-04-2-ex3",
            "sedang",
            """
            Tulis fungsi `selesaikan_dengan_invers(A, b)` untuk sistem 2x2 yang mengembalikan `x` sebagai list dibulatkan 6 desimal memakai rumus invers 2x2, atau `None` bila `A` singular.
            """,
            """
            def selesaikan_dengan_invers(A, b):
                # TODO: implementasikan
                pass
            """,
            """
            assert selesaikan_dengan_invers([[4, 7], [2, 6]], [1, 2]) == [-0.8, 0.6]
            assert selesaikan_dengan_invers([[1, 2], [2, 4]], [1, 2]) is None
            assert selesaikan_dengan_invers([[1, 0], [0, 1]], [3, 4]) == [3.0, 4.0]
            assert selesaikan_dengan_invers([[2, 1], [1, -1]], [5, 1]) == [2.0, 1.0]
            """,
            "Hitung invers dengan rumus lalu kalikan dengan b.",
            """
            def selesaikan_dengan_invers(A, b):
                (a, bb), (c, d) = A
                det = a * d - bb * c
                if det == 0:
                    return None
                inv = [[d / det, -bb / det], [-c / det, a / det]]
                return [round(sum(inv[i][j] * b[j] for j in range(2)) + 0.0, 6) for i in range(2)]
            """,
        ),
        E(
            "A2-04-2-ex4",
            "menantang",
            """
            Tulis fungsi `invers(m)` yang menghitung invers matriks persegi berukuran berapa pun dengan eliminasi Gauss-Jordan pada `[A | I]` dengan pivoting sebagian tanpa NumPy. Kembalikan list of list dibulatkan 6 desimal, atau `None` bila singular (pivot mutlak di bawah 1e-12).
            """,
            """
            def invers(m):
                # TODO: implementasikan
                pass
            """,
            """
            assert invers([[4, 7], [2, 6]]) == [[0.6, -0.7], [-0.2, 0.4]]
            assert invers([[1, 2], [2, 4]]) is None
            assert invers([[2, 0, 0], [0, 4, 0], [0, 0, 5]]) == [[0.5, 0.0, 0.0], [0.0, 0.25, 0.0], [0.0, 0.0, 0.2]]
            assert invers([[1, 2], [3, 4]]) == [[-2.0, 1.0], [1.5, -0.5]]
            assert invers([[0, 1], [1, 0]]) == [[0.0, 1.0], [1.0, 0.0]]
            """,
            "Bentuk matriks augmented dengan identitas, eliminasi ke atas dan ke bawah, lalu bagi tiap baris dengan pivotnya.",
            """
            def invers(m):
                n = len(m)
                a = [list(map(float, m[i])) + [1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
                for k in range(n):
                    p = max(range(k, n), key=lambda i: abs(a[i][k]))
                    if abs(a[p][k]) < 1e-12:
                        return None
                    a[k], a[p] = a[p], a[k]
                    pivot = a[k][k]
                    a[k] = [x / pivot for x in a[k]]
                    for i in range(n):
                        if i != k:
                            f = a[i][k]
                            a[i] = [x - f * y for x, y in zip(a[i], a[k])]
                return [[round(x + 0.0, 6) for x in baris[n:]] for baris in a]
            """,
        ),
    ],
    [
        M("Menulis (AB)^-1 = A^-1 B^-1.", "Urutan terbalik: (AB)^-1 = B^-1 A^-1."),
        M("Memakai inv untuk menyelesaikan sistem.", "Pakai np.linalg.solve."),
        M("Mencoba membalik matriks singular.", "Periksa determinan atau peringkat lebih dulu."),
    ],
    [
        Q("Syarat A punya invers?", ["Simetris", "Persegi dan determinan tak nol", "Diagonal", "Ortogonal"], 1, "Matriks persegi dengan determinan tak nol.", hint="Tak singular."),
        Q("(AB)^-1 sama dengan?", ["A^-1 B^-1", "B^-1 A^-1", "AB", "A^-1 + B^-1"], 1, "Urutan terbalik.", hint="Kaus kaki dan sepatu."),
        Q("det(A^-1) sama dengan?", ["det A", "1 / det A", "-det A", "0"], 1, "Kebalikan determinan.", hint="Kebalikan."),
        Q("Cara terbaik menyelesaikan A x = b?", ["inv(A) @ b", "np.linalg.solve(A, b)", "A / b", "A.T @ b"], 1, "solve lebih cepat dan akurat.", hint="Hindari invers eksplisit."),
        Q("Invers matriks diagonal?", ["Diagonal berisi kebalikan elemen", "Transposnya", "Dirinya", "Tak ada"], 0, "Setiap elemen diagonal dibalik.", hint="1 dibagi elemen."),
    ],
    [
        "Invers ada untuk matriks persegi dengan determinan tak nol dan membatalkan transformasi.",
        "Rumus 2x2 dan Gauss-Jordan menghitung invers.",
        "Invers hasil kali membalik urutan faktor.",
        "Gunakan solve, bukan invers eksplisit, untuk sistem linear.",
    ],
    [],
)

l3 = lesson(
    "A2-04-3",
    "Kondisi, pseudoinvers, dan penerapan",
    35,
    [
        "Mengukur kondisi matriks dengan bilangan kondisi",
        "Mengenali matriks hampir singular lewat contoh matriks Hilbert dan kolinearitas",
        "Memakai pseudoinvers untuk matriks non-persegi atau singular",
        "Menerapkan konsep pada regresi dengan fitur berkorelasi",
    ],
    [
        T("""
        ## Bilangan kondisi

        Matriks tidak hanya terbagi menjadi singular dan tidak singular. Ada kelabu di antaranya: matriks yang secara teori punya invers tetapi hampir singular, sehingga perhitungan dengannya rapuh. **Bilangan kondisi** `cond(A)` mengukur ini. Ia adalah rasio nilai singular terbesar terhadap terkecil, dan menyatakan seberapa besar galat relatif pada `b` bisa diperkuat menjadi galat relatif pada solusi `x`.

        Bilangan kondisi 1 adalah terbaik, seperti matriks identitas atau ortogonal. Bilangan kondisi `10^k` berarti kamu bisa kehilangan sekitar `k` digit ketelitian. Dengan ketelitian ganda sekitar enam belas digit, bilangan kondisi `10^16` berarti hasil praktis tidak bermakna.

        Bilangan kondisi adalah ukuran yang tepat untuk menilai kedekatan dengan singular, bukan determinan. Matriks `0.1 I` memiliki determinan sangat kecil tetapi bilangan kondisi 1.
        """),
        C(
            """
            import numpy as np

            print(round(float(np.linalg.cond(np.eye(3))), 4))
            print(round(float(np.linalg.cond(0.1 * np.eye(10))), 4))
            print(round(float(np.linalg.det(0.1 * np.eye(10))), 12))

            hampir = np.array([[1.0, 1.0], [1.0, 1.0001]])
            print(round(float(np.linalg.cond(hampir)), 0))
            b1 = np.array([2.0, 2.0001])
            b2 = np.array([2.0, 2.0002])
            print(np.linalg.solve(hampir, b1).round(2).tolist())
            print(np.linalg.solve(hampir, b2).round(2).tolist())
            """,
            """
            1.0
            1.0
            1e-10
            40002.0
            [1.0, 1.0]
            [0.0, 2.0]
            """,
            """
            Bilangan kondisi identitas dan kelipatannya sama dengan satu walau determinan kecil. Pada matriks hampir singular, perubahan sangat kecil pada `b` mengubah solusi dari `[1, 1]` menjadi `[0, 2]`.
            """,
            filename="bilangan_kondisi.py",
        ),
        T("""
        ## Matriks Hilbert dan kolinearitas

        Contoh klasik matriks berkondisi buruk adalah matriks Hilbert dengan elemen `1 / (i + j - 1)`. Bilangan kondisinya meledak secara eksponensial terhadap ukuran. Pada ukuran sepuluh saja sudah sekitar `10^13`, sehingga menyelesaikan sistem dengannya hampir tidak memberi digit yang benar.

        Dalam data, penyebab umum kondisi buruk adalah **kolinearitas**: dua atau lebih fitur hampir merupakan kombinasi linear satu sama lain, misalnya tinggi dalam sentimeter dan tinggi dalam inci, atau jumlah beberapa kolom dummy yang sama dengan kolom intersep. Kolom `X` hampir bergantung linear, sehingga `X^T X` hampir singular.

        Akibatnya koefisien regresi menjadi sangat tidak stabil: perubahan kecil pada data membuat koefisien meloncat dan saling meniadakan. Prediksi mungkin masih baik, tetapi tafsir koefisien tak dapat dipercaya. Solusinya menghapus fitur redundan, memakai regularisasi, atau PCA.
        """),
        C(
            """
            import numpy as np

            def hilbert(n):
                return np.array([[1.0 / (i + j + 1) for j in range(n)] for i in range(n)])

            for n in [2, 4, 8]:
                print(n, "{:.1e}".format(np.linalg.cond(hilbert(n))))

            rng = np.random.default_rng(1)
            x1 = rng.normal(size=50)
            x2 = x1 + rng.normal(scale=1e-6, size=50)
            X = np.column_stack([np.ones(50), x1, x2])
            print(np.linalg.cond(X) > 1e5)
            print(np.linalg.matrix_rank(X))
            """,
            """
            2 1.9e+01
            4 1.6e+04
            8 1.5e+10
            True
            3
            """,
            """
            Bilangan kondisi matriks Hilbert naik sangat cepat terhadap ukuran. Dua fitur yang nyaris identik membuat matriks desain berkondisi buruk walau peringkatnya masih penuh secara numerik.
            """,
            filename="hilbert_kolinearitas.py",
        ),
        K(
            "tip",
            """
            Sebelum menjalankan regresi, hitung `np.linalg.cond` pada matriks fitur (setelah standardisasi). Nilai di atas sekitar 1000 adalah tanda perlu waspada terhadap kolinearitas.
            """,
            title="Cek kondisi fitur",
        ),
        T("""
        ## Pseudoinvers

        Bagaimana bila matriks tidak persegi atau singular? **Pseudoinvers** Moore-Penrose, ditulis `A^+`, memperluas konsep invers ke matriks apa pun. Ia memberi solusi kuadrat terkecil berpanjang minimum untuk `A x = b`: bila ada banyak solusi, ia memilih yang normanya terkecil, dan bila tidak ada solusi persis, ia memberi yang galatnya terkecil.

        Untuk `A` dengan kolom bebas linear, `A^+ = (A^T A)^-1 A^T`, yang tepat solusi persamaan normal. Untuk kasus umum, `np.linalg.pinv` menghitungnya lewat SVD, yang stabil. Bila `A` persegi dan tak singular, `A^+ = A^-1`.

        Pseudoinvers menjadi alat utama dalam regresi dengan fitur berkorelasi sempurna, sistem underdetermined, dan banyak algoritma pembelajaran mesin. Tetapi sama seperti invers biasa, untuk tujuan prediksi lebih baik memakai `lstsq` yang bekerja langsung tanpa membentuk `A^+`.
        """),
        C(
            """
            import numpy as np

            A = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
            b = np.array([1.0, 2.0, 2.0])
            P = np.linalg.pinv(A)
            print(P.shape, (P @ b).round(4).tolist())
            print(np.allclose(P @ b, np.linalg.lstsq(A, b, rcond=None)[0]))
            print(np.allclose(np.linalg.pinv(np.array([[4.0, 7.0], [2.0, 6.0]])), np.linalg.inv(np.array([[4.0, 7.0], [2.0, 6.0]]))))

            S = np.array([[1.0, 2.0], [2.0, 4.0]])
            y = np.array([3.0, 6.0])
            x = np.linalg.pinv(S) @ y
            print(x.round(4).tolist(), np.allclose(S @ x, y))
            """,
            """
            (2, 3) [-0.6667, 0.9167]
            True
            True
            [0.6, 1.2] True
            """,
            """
            Pseudoinvers memberi solusi kuadrat terkecil untuk sistem tidak persegi. Untuk matriks singular dengan banyak solusi ia memilih yang paling pendek, yaitu `[0.6, 1.2]`.
            """,
            filename="pseudoinvers.py",
        ),
        T("""
        ## Penerapan: variansi koefisien regresi

        Dalam regresi linear klasik, matriks kovariansi estimasi koefisien adalah `sigma^2 (X^T X)^-1`. Elemen diagonalnya adalah variansi tiap koefisien, dan akar kuadratnya adalah galat baku yang kamu lihat di tabel regresi. Ketika `X^T X` hampir singular, inversnya memiliki elemen sangat besar, sehingga galat baku membengkak. Itulah hubungan langsung antara kondisi buruk dan koefisien yang tidak bisa dipercaya.

        Ukuran praktis untuk ini adalah faktor inflasi variansi (VIF), yang menunjukkan seberapa besar variansi koefisien membesar akibat korelasi dengan fitur lain. VIF tinggi menandakan kolinearitas. Konsep ini muncul di kursus regresi, dan akarnya ada pada materi yang baru kamu pelajari.

        Latihan berikut menghitung bilangan kondisi, mendeteksi kolinearitas, dan menghitung pseudoinvers sederhana dari nol.
        """),
        T("""
        ## Langkah praktis mendiagnosis masalah

        Bila sebuah model linear menghasilkan koefisien aneh, ikuti urutan sederhana. Pertama, standardisasi fitur agar skala tidak menipu. Kedua, hitung bilangan kondisi matriks fitur. Ketiga, hitung korelasi antar fitur dan cari pasangan di atas 0.9. Keempat, hapus atau gabungkan fitur redundan, atau gunakan regularisasi. Dengan urutan ini, sebagian besar masalah kolinearitas dapat ditemukan dalam hitungan menit.

        Catat juga hasil diagnosis agar rekan kerja memahami alasan sebuah fitur dibuang.
        """),
        E(
            "A2-04-3-ex1",
            "mudah",
            """
            Tulis fungsi `kondisi_diagonal(d)` yang menerima list elemen diagonal tak nol dari matriks diagonal dan mengembalikan bilangan kondisinya (nilai mutlak terbesar dibagi nilai mutlak terkecil) dibulatkan 4 desimal.
            """,
            """
            def kondisi_diagonal(d):
                # TODO: implementasikan
                pass
            """,
            """
            assert kondisi_diagonal([1, 1, 1]) == 1.0
            assert kondisi_diagonal([10, 1]) == 10.0
            assert kondisi_diagonal([-4, 2, 8]) == 4.0
            assert kondisi_diagonal([0.1, 0.1]) == 1.0
            """,
            "Bagi nilai mutlak terbesar dengan nilai mutlak terkecil.",
            """
            def kondisi_diagonal(d):
                a = [abs(x) for x in d]
                return round(max(a) / min(a), 4)
            """,
        ),
        E(
            "A2-04-3-ex2",
            "mudah",
            """
            Tulis fungsi `korelasi(x, y)` yang mengembalikan koefisien korelasi Pearson dua list dibulatkan 4 desimal. Anggap variansi keduanya tidak nol.
            """,
            """
            def korelasi(x, y):
                # TODO: implementasikan
                pass
            """,
            """
            assert korelasi([1, 2, 3], [2, 4, 6]) == 1.0
            assert korelasi([1, 2, 3], [3, 2, 1]) == -1.0
            assert korelasi([1, 2, 3, 4], [1, 3, 2, 4]) == 0.8
            assert korelasi([1, 2, 3], [5, 5.5, 7]) == 0.9608
            """,
            "Kovariansi dibagi hasil kali akar jumlah kuadrat simpangan.",
            """
            def korelasi(x, y):
                n = len(x)
                mx, my = sum(x) / n, sum(y) / n
                sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
                sxx = sum((a - mx) ** 2 for a in x)
                syy = sum((b - my) ** 2 for b in y)
                return round(sxy / (sxx * syy) ** 0.5, 4)
            """,
        ),
        E(
            "A2-04-3-ex3",
            "sedang",
            """
            Tulis fungsi `kolinear(X, batas=0.99)` yang menerima matriks fitur `X` (list of list, baris pengamatan) dan mengembalikan list tuple indeks `(i, j)` dengan `i < j` untuk setiap pasangan kolom yang nilai mutlak korelasinya melebihi `batas`. Anggap variansi tiap kolom tidak nol.
            """,
            """
            def kolinear(X, batas=0.99):
                # TODO: implementasikan
                pass
            """,
            """
            X = [[1, 2, 5], [2, 4.01, 1], [3, 6, 4], [4, 7.99, 2]]
            assert kolinear(X) == [(0, 1)]
            assert kolinear([[1, 5], [2, 1], [3, 4], [4, 2]]) == []
            assert kolinear([[1, 2, -1], [2, 4, -2], [3, 6.1, -3.1]]) == [(0, 1), (0, 2), (1, 2)]
            assert kolinear([[1, 1], [2, 2.5], [3, 2]], batas=0.5) == [(0, 1)]
            """,
            "Hitung korelasi Pearson untuk semua pasangan kolom dari zip(*X).",
            """
            def kolinear(X, batas=0.99):
                kol = [list(k) for k in zip(*X)]
                def kor(x, y):
                    n = len(x)
                    mx, my = sum(x) / n, sum(y) / n
                    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
                    sxx = sum((a - mx) ** 2 for a in x)
                    syy = sum((b - my) ** 2 for b in y)
                    return sxy / (sxx * syy) ** 0.5
                hasil = []
                for i in range(len(kol)):
                    for j in range(i + 1, len(kol)):
                        if abs(kor(kol[i], kol[j])) > batas:
                            hasil.append((i, j))
                return hasil
            """,
        ),
        E(
            "A2-04-3-ex4",
            "menantang",
            """
            Tulis fungsi `pinv_kolom_penuh(A)` yang menghitung pseudoinvers `(A^T A)^-1 A^T` untuk matriks `A` berukuran `n x 2` (dua kolom bebas linear) tanpa NumPy dan mengembalikan list of list `2 x n` dibulatkan 6 desimal.
            """,
            """
            def pinv_kolom_penuh(A):
                # TODO: implementasikan
                pass
            """,
            """
            r = pinv_kolom_penuh([[1, 0], [0, 1], [0, 0]])
            assert r == [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
            r2 = pinv_kolom_penuh([[1, 1], [1, 2], [1, 3]])
            assert r2 == [[1.333333, 0.333333, -0.666667], [-0.5, 0.0, 0.5]]
            r3 = pinv_kolom_penuh([[2, 0], [0, 2]])
            assert r3 == [[0.5, 0.0], [0.0, 0.5]]
            """,
            "Hitung G = A^T A (2x2), balikkan dengan rumus 2x2, lalu kalikan dengan A^T.",
            """
            def pinv_kolom_penuh(A):
                a = sum(r[0] * r[0] for r in A)
                b = sum(r[0] * r[1] for r in A)
                d = sum(r[1] * r[1] for r in A)
                det = a * d - b * b
                inv = [[d / det, -b / det], [-b / det, a / det]]
                hasil = [[inv[i][0] * r[0] + inv[i][1] * r[1] for r in A] for i in range(2)]
                return [[round(x + 0.0, 6) for x in baris] for baris in hasil]
            """,
        ),
    ],
    [
        M("Menilai kondisi dari determinan.", "Pakai np.linalg.cond."),
        M("Mengabaikan kolinearitas antar fitur.", "Periksa korelasi dan bilangan kondisi sebelum regresi."),
        M("Memakai persamaan normal pada fitur yang hampir kembar.", "Pakai lstsq, pinv, atau regularisasi."),
    ],
    [
        Q("Bilangan kondisi terbaik?", ["0", "1", "10", "tak hingga"], 1, "Matriks identitas dan ortogonal bernilai 1.", hint="Rasio terkecil."),
        Q("Apa yang menyebabkan koefisien regresi tidak stabil?", ["Terlalu banyak data", "Kolinearitas antar fitur", "Intersep", "Normalisasi"], 1, "Kolom hampir bergantung linear.", hint="Fitur kembar."),
        Q("Fungsi NumPy untuk pseudoinvers?", ["np.linalg.inv", "np.linalg.pinv", "np.linalg.pseudo", "np.inv"], 1, "pinv menghitung Moore-Penrose.", hint="p untuk pseudo."),
        Q("Pseudoinvers memberi solusi apa pada sistem underdetermined?", ["Solusi terpanjang", "Solusi berpanjang minimum", "Tak ada", "Acak"], 1, "Norma terkecil di antara banyak solusi.", hint="Terpendek."),
        Q("Bilangan kondisi 10^6 berarti?", ["Hasil sempurna", "Bisa kehilangan sekitar 6 digit", "Matriks diagonal", "Singular pasti"], 1, "Galat diperkuat sekitar sejuta kali.", hint="Eksponen adalah digit."),
    ],
    [
        "Bilangan kondisi mengukur kedekatan dengan singular dan penguatan galat.",
        "Kolinearitas membuat matriks desain berkondisi buruk dan koefisien tidak stabil.",
        "Pseudoinvers memperluas invers ke matriks non-persegi atau singular.",
        "Variansi koefisien regresi bergantung pada (X^T X)^-1.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa perhitungan dan contoh kode yang cukup jelas dalam teks.", "brief": []}

write_module(
    "A2",
    4,
    "Determinan dan invers",
    105,
    [
        "Menghitung dan menafsirkan determinan",
        "Menghitung dan memakai matriks invers dengan benar",
        "Menilai kondisi matriks dan memakai pseudoinvers",
    ],
    [l1, l2, l3],
    video,
    REF,
)
