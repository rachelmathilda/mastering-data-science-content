import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

l1 = lesson(
    "A2-06-1",
    "Konsep Singular Value Decomposition",
    35,
    [
        "Memahami bentuk A = U S V^T untuk matriks sembarang ukuran",
        "Membaca bentuk dan arti U, S, dan V^T dari np.linalg.svd",
        "Menghubungkan nilai singular dengan eigenvalue dari A^T A",
        "Memakai nilai singular untuk peringkat dan bilangan kondisi",
    ],
    [
        T("""
        ## Dari eigen ke SVD

        Eigenvalue dan eigenvector hanya didefinisikan untuk matriks persegi, dan tidak semua matriks persegi bisa didiagonalkan. Padahal data nyata hampir selalu berbentuk persegi panjang: seribu baris sampel dan dua puluh kolom fitur. Kita butuh alat yang bekerja untuk matriks apa pun. Alat itu adalah **Singular Value Decomposition** atau SVD, dan sering disebut dekomposisi paling berguna dalam aljabar linear terapan.

        Teoremanya sederhana: setiap matriks `A` berukuran `m x n` dapat ditulis sebagai `A = U S V^T`. Matriks `U` berukuran `m x m` dan `V` berukuran `n x n` keduanya ortogonal, sedangkan `S` berukuran `m x n` berisi bilangan tak negatif yang disebut **nilai singular** pada diagonalnya, terurut dari terbesar ke terkecil. Tidak ada syarat simetris, persegi, atau bisa didiagonalkan. SVD selalu ada.
        """),
        T("""
        ## Tafsir geometris

        Ortogonal berarti rotasi atau pencerminan, jadi SVD menguraikan transformasi apa pun menjadi tiga langkah. Pertama `V^T` memutar ruang masukan. Kedua `S` meregangkan tiap sumbu dengan faktor nilai singular, sekaligus mengubah dimensi bila matriksnya persegi panjang. Ketiga `U` memutar hasilnya di ruang keluaran. Jadi lingkaran satuan selalu berubah menjadi elips, dan nilai singular adalah panjang sumbu elips itu.

        Kolom `V` disebut **vektor singular kanan** dan kolom `U` disebut **vektor singular kiri**. Vektor singular kanan ke-`i` dipetakan oleh `A` menjadi vektor singular kiri ke-`i` dikalikan nilai singular ke-`i`. Nilai singular terbesar adalah peregangan maksimum yang bisa dilakukan `A` pada vektor satuan, yang sama dengan norma spektral matriks.
        """),
        C(
            """
            import numpy as np

            A = np.array([[3.0, 2.0, 2.0], [2.0, 3.0, -2.0]])
            U, s, Vt = np.linalg.svd(A)
            print(U.shape, s.shape, Vt.shape)
            print(s.round(4).tolist())
            S = np.zeros((2, 3))
            S[:2, :2] = np.diag(s)
            print(np.allclose(U @ S @ Vt, A))
            U2, s2, Vt2 = np.linalg.svd(A, full_matrices=False)
            print(Vt2.shape)
            """,
            """
            (2, 2) (2,) (3, 3)
            [5.0, 3.0]
            True
            (2, 3)
            """,
            """
            Fungsi mengembalikan nilai singular sebagai vektor satu dimensi sehingga `S` harus dirakit sendiri. Opsi `full_matrices=False` memberi bentuk ringkas yang lebih hemat dan cukup untuk hampir semua keperluan.
            """,
            filename="bentuk_svd.py",
        ),
        T("""
        ## Hubungan dengan eigenvalue

        SVD terkait erat dengan eigen. Dari `A = U S V^T` kita peroleh `A^T A = V S^T S V^T`. Ruas kanan adalah dekomposisi spektral matriks simetris `A^T A`, sehingga kolom `V` adalah eigenvector dari `A^T A`, dan kuadrat nilai singular adalah eigenvalue-nya. Dengan cara serupa, kolom `U` adalah eigenvector dari `A A^T`.

        Akibatnya, nilai singular adalah akar dari eigenvalue `A^T A`, dan selalu tak negatif karena `A^T A` positif semidefinit. Untuk matriks persegi, hasil kali semua nilai singular sama dengan nilai mutlak determinan. Bila matriksnya simetris positif definit, nilai singular sama dengan eigenvalue. Hubungan ini menjelaskan mengapa SVD dan PCA begitu dekat: PCA pada data terpusat adalah SVD dari matriks data itu sendiri.
        """),
        C(
            """
            import numpy as np

            A = np.array([[4.0, 0.0], [3.0, -5.0]])
            nilai = np.linalg.eigvalsh(A.T @ A)[::-1]
            print(np.sqrt(nilai).round(4).tolist())
            s = np.linalg.svd(A, compute_uv=False)
            print(s.round(4).tolist())
            print(round(float(np.prod(s)), 4), round(abs(float(np.linalg.det(A))), 4))
            print(round(float(np.linalg.norm(A, 2)), 4), round(float(s[0]), 4))
            """,
            """
            [6.3246, 3.1623]
            [6.3246, 3.1623]
            20.0 20.0
            6.3246 6.3246
            """,
            """
            Akar eigenvalue dari `A^T A` sama dengan nilai singular. Hasil kali nilai singular sama dengan determinan mutlak dan nilai singular terbesar sama dengan norma spektral.
            """,
            filename="hubungan_eigen.py",
        ),
        K(
            "tip",
            """
            Untuk menghitung nilai singular saja pakai `np.linalg.svd(A, compute_uv=False)`. Jangan membentuk `A^T A` secara eksplisit pada matriks yang kondisinya buruk karena itu mengkuadratkan bilangan kondisi dan menghilangkan presisi.
            """,
            title="Jangan lewat A^T A",
        ),
        T("""
        ## Peringkat dan bilangan kondisi

        Nilai singular memberi cara paling andal untuk menghitung **peringkat**: peringkat adalah jumlah nilai singular yang tidak nol. Dalam komputer tidak ada angka yang tepat nol, jadi kita memakai ambang kecil. Nilai di bawah ambang dianggap nol. Itulah yang dilakukan `np.linalg.matrix_rank` secara internal.

        Rasio nilai singular terbesar terhadap terkecil disebut **bilangan kondisi**. Bilangan ini mengukur seberapa besar galat kecil pada masukan diperbesar pada penyelesaian sistem linear. Nilai dekat satu berarti matriks sehat dan nilai sangat besar berarti hampir singular, sehingga hasil perhitungannya tidak bisa dipercaya. Dalam regresi, bilangan kondisi besar adalah tanda kolinearitas antar fitur.
        """),
        C(
            """
            import numpy as np

            B = np.array([[1.0, 2.0, 3.0], [2.0, 4.0, 6.0], [1.0, 0.0, 1.0]])
            s = np.linalg.svd(B, compute_uv=False)
            print(int(np.sum(s > 1e-10)), np.linalg.matrix_rank(B))
            print(bool(s[-1] < 1e-10))
            A = np.array([[3.0, 2.0, 2.0], [2.0, 3.0, -2.0]])
            print(round(float(np.linalg.cond(A)), 4))
            """,
            """
            2 2
            True
            1.6667
            """,
            """
            Baris kedua `B` adalah dua kali baris pertama sehingga satu nilai singularnya hampir nol dan peringkatnya dua. Bilangan kondisi `A` adalah 5 dibagi 3.
            """,
            filename="peringkat_svd.py",
        ),
        T("""
        ## Mengapa SVD begitu penting

        SVD sering disebut pisau lipat aljabar linear karena satu dekomposisi ini menjawab banyak pertanyaan sekaligus. Dari nilai singular kita membaca peringkat, bilangan kondisi, dan norma matriks. Dari vektor singular kita memperoleh basis ortonormal untuk ruang kolom dan ruang baris, serta ruang nol. Dari potongan sebagian suku kita mendapat aproksimasi terbaik berperingkat rendah, dan dari semuanya bersama kita menyusun pseudoinvers.

        Karena faktor `U` dan `V` ortogonal, algoritmenya stabil secara numerik. Rotasi tidak memperbesar galat pembulatan, jadi SVD menjadi pilihan utama saat ketepatan penting. Harganya adalah waktu hitung yang lebih besar dari dekomposisi lain, tetapi untuk data berukuran menengah biaya itu hampir selalu layak dibayar. Pelajaran berikutnya menunjukkan hasil yang bisa dipetik darinya.
        """),
        E(
            "A2-06-1-ex1",
            "mudah",
            """
            Tulis fungsi `bentuk_svd(m, n, penuh)` yang mengembalikan tuple tiga bentuk `(bentuk_U, bentuk_s, bentuk_Vt)` untuk matriks `m x n`. Bila `penuh` bernilai `True` gunakan bentuk penuh, bila tidak gunakan bentuk ringkas.
            """,
            """
            def bentuk_svd(m, n, penuh):
                # TODO: implementasikan
                pass
            """,
            """
            assert bentuk_svd(2, 3, True) == ((2, 2), (2,), (3, 3))
            assert bentuk_svd(2, 3, False) == ((2, 2), (2,), (2, 3))
            assert bentuk_svd(5, 2, False) == ((5, 2), (2,), (2, 2))
            assert bentuk_svd(4, 4, True) == ((4, 4), (4,), (4, 4))
            """,
            "Banyak nilai singular adalah min(m, n). Pada bentuk penuh U adalah m x m dan Vt adalah n x n.",
            """
            def bentuk_svd(m, n, penuh):
                k = min(m, n)
                if penuh:
                    return ((m, m), (k,), (n, n))
                return ((m, k), (k,), (k, n))
            """,
        ),
        E(
            "A2-06-1-ex2",
            "mudah",
            """
            Tulis fungsi `peringkat(s, tol=1e-10)` yang menerima list nilai singular dan mengembalikan banyaknya nilai yang lebih besar dari `tol`.
            """,
            """
            def peringkat(s, tol=1e-10):
                # TODO: implementasikan
                pass
            """,
            """
            assert peringkat([5.0, 3.0]) == 2
            assert peringkat([4.0, 1e-12]) == 1
            assert peringkat([0.0, 0.0]) == 0
            assert peringkat([3.0, 0.5, 0.01], tol=0.1) == 2
            """,
            "Hitung elemen yang melebihi ambang.",
            """
            def peringkat(s, tol=1e-10):
                return sum(1 for x in s if x > tol)
            """,
        ),
        E(
            "A2-06-1-ex3",
            "sedang",
            """
            Tulis fungsi `nilai_singular(A)` yang menerima list of list dan mengembalikan nilai singular terurut menurun sebagai list dibulatkan 4 desimal, dengan menghitung akar eigenvalue dari `A^T A` memakai `np.linalg.eigvalsh`. Potong nilai negatif kecil menjadi nol dan hanya ambil `min(m, n)` nilai terbesar.
            """,
            """
            import numpy as np

            def nilai_singular(A):
                # TODO: implementasikan
                pass
            """,
            """
            assert nilai_singular([[3, 0], [0, 4]]) == [4.0, 3.0]
            assert nilai_singular([[4, 0], [3, -5]]) == [6.3246, 3.1623]
            assert nilai_singular([[1, 1], [1, 1]]) == [2.0, 0.0]
            assert nilai_singular([[3, 2, 2], [2, 3, -2]]) == [5.0, 3.0]
            assert nilai_singular([[2]]) == [2.0]
            """,
            "Bentuk A.T @ A lalu eigvalsh mengurutkan naik. Balik urutannya dan ambil akar.",
            """
            import numpy as np

            def nilai_singular(A):
                A = np.array(A, dtype=float)
                k = min(A.shape)
                nilai = np.linalg.eigvalsh(A.T @ A)[::-1][:k]
                nilai = np.clip(nilai, 0, None)
                return [round(float(x) ** 0.5 + 0.0, 4) for x in nilai]
            """,
        ),
        E(
            "A2-06-1-ex4",
            "menantang",
            """
            Tulis fungsi `rekonstruksi_k(A, k)` yang mengembalikan pendekatan peringkat `k` dari `A` (list of list) dengan memakai `np.linalg.svd` dan hanya `k` nilai singular pertama. Bulatkan setiap elemen 4 desimal dan hindari `-0.0`.
            """,
            """
            import numpy as np

            def rekonstruksi_k(A, k):
                # TODO: implementasikan
                pass
            """,
            """
            assert rekonstruksi_k([[3, 0], [0, 4]], 1) == [[0.0, 0.0], [0.0, 4.0]]
            assert rekonstruksi_k([[3, 2, 2], [2, 3, -2]], 2) == [[3.0, 2.0, 2.0], [2.0, 3.0, -2.0]]
            assert rekonstruksi_k([[1, 1], [1, 1]], 1) == [[1.0, 1.0], [1.0, 1.0]]
            assert rekonstruksi_k([[2, 0], [0, 1]], 2) == [[2.0, 0.0], [0.0, 1.0]]
            """,
            "Kalikan kolom U pertama dengan nilai singular lalu dengan baris Vt pertama.",
            """
            import numpy as np

            def rekonstruksi_k(A, k):
                U, s, Vt = np.linalg.svd(np.array(A, dtype=float), full_matrices=False)
                R = (U[:, :k] * s[:k]) @ Vt[:k]
                return [[round(float(x), 4) + 0.0 for x in baris] for baris in R]
            """,
        ),
    ],
    [
        M("Mengira nilai singular sama dengan eigenvalue untuk semua matriks.", "Nilai singular adalah akar eigenvalue dari A^T A."),
        M("Lupa bahwa svd mengembalikan s sebagai vektor dan Vt sudah transpos.", "Rakit S dengan np.diag dan pakai Vt langsung."),
        M("Memakai A^T A untuk matriks berkondisi buruk.", "Pakai svd langsung agar presisi terjaga."),
    ],
    [
        Q("Bentuk SVD?", ["A = U S V^T", "A = P D P^-1", "A = L U", "A = Q R"], 0, "U dan V ortogonal serta S berisi nilai singular.", hint="Tiga faktor."),
        Q("SVD berlaku untuk?", ["Hanya matriks simetris", "Hanya matriks persegi", "Semua matriks", "Hanya matriks invertibel"], 2, "SVD selalu ada.", hint="Tanpa syarat."),
        Q("Kuadrat nilai singular adalah eigenvalue dari?", ["A", "A^T A", "A^-1", "I"], 1, "A^T A = V S^T S V^T.", hint="Simetris."),
        Q("Peringkat sama dengan?", ["Jumlah nilai singular", "Banyak nilai singular bukan nol", "Nilai terbesar", "Determinan"], 1, "Hitung yang melebihi ambang.", hint="Bukan nol."),
        Q("Bilangan kondisi adalah?", ["s terkecil dibagi terbesar", "s terbesar dibagi terkecil", "Jumlah s", "Trace"], 1, "Rasio terbesar terhadap terkecil.", hint="Besar berarti buruk."),
    ],
    [
        "SVD menulis matriks apa pun sebagai A = U S V^T dengan U dan V ortogonal.",
        "Nilai singular adalah akar eigenvalue dari A^T A dan tak pernah negatif.",
        "Peringkat dan bilangan kondisi dibaca dari nilai singular.",
        "Pakai np.linalg.svd langsung dan bentuk ringkas bila memungkinkan.",
    ],
    [],
)

l2 = lesson(
    "A2-06-2",
    "Aproksimasi peringkat rendah dan kompresi",
    35,
    [
        "Memahami teorema Eckart-Young tentang aproksimasi terbaik",
        "Menghitung galat aproksimasi dari nilai singular yang dibuang",
        "Memilih jumlah komponen dari energi kumulatif",
        "Menghitung penghematan penyimpanan dari kompresi peringkat rendah",
    ],
    [
        T("""
        ## Jumlah matriks peringkat satu

        Tulis `A = U S V^T` kolom demi kolom, dan hasilnya adalah jumlah `s1 u1 v1^T + s2 u2 v2^T + ...`. Tiap suku adalah matriks peringkat satu: perkalian luar dua vektor yang diskalakan oleh nilai singular. Suku pertama membawa bagian terbesar dari `A`, suku kedua bagian terbesar berikutnya, dan seterusnya. Nilai singular bertindak seperti bobot kepentingan.

        Bila kita hanya menyimpan `k` suku pertama, kita mendapat matriks `A_k` berperingkat `k`. Pertanyaannya: seberapa bagus pendekatan itu? Jawabannya luar biasa. Sering kali beberapa suku pertama sudah menangkap hampir seluruh isi matriks, dan sisanya hanya derau. Inilah dasar kompresi, penghilangan derau, dan reduksi dimensi.
        """),
        T("""
        ## Teorema Eckart-Young

        **Teorema Eckart-Young** menyatakan bahwa `A_k` adalah pendekatan peringkat `k` terbaik dari `A`, baik diukur dengan norma Frobenius maupun norma spektral. Tidak ada matriks berperingkat `k` lain yang lebih dekat ke `A`. Jadi pemotongan SVD bukan sekadar heuristik, melainkan optimal secara matematis.

        Galatnya pun mudah dihitung tanpa membentuk `A_k`. Galat Frobenius sama dengan akar jumlah kuadrat nilai singular yang dibuang, yaitu `sqrt(s_{k+1}^2 + ... + s_r^2)`. Galat norma spektral sama dengan `s_{k+1}`, nilai singular pertama yang dibuang. Dari nilai singular saja kita sudah tahu seberapa mahal sebuah kompresi sebelum melakukannya.
        """),
        C(
            """
            import numpy as np

            rng = np.random.default_rng(1)
            X = rng.normal(size=(6, 4))
            U, s, Vt = np.linalg.svd(X, full_matrices=False)
            for k in (1, 2, 3):
                Ak = (U[:, :k] * s[:k]) @ Vt[:k]
                galat = np.linalg.norm(X - Ak)
                print(k, np.allclose(galat, np.sqrt((s[k:] ** 2).sum())), np.linalg.matrix_rank(Ak))
            """,
            """
            1 True 1
            2 True 2
            3 True 3
            """,
            """
            Galat Frobenius persis sama dengan akar jumlah kuadrat nilai singular yang dibuang dan peringkat hasil pemotongan sama dengan `k`.
            """,
            filename="peringkat_rendah.py",
        ),
        T("""
        ## Energi dan memilih k

        Bagaimana memilih `k`? Kuadrat nilai singular disebut **energi**. Total energi `sum(s^2)` sama dengan kuadrat norma Frobenius `A`. Proporsi energi komponen ke-`i` adalah `s_i^2` dibagi total, dan **energi kumulatif** adalah jumlah proporsi dari komponen pertama sampai ke-`k`.

        Aturan praktis yang umum: pilih `k` terkecil yang energi kumulatifnya mencapai ambang seperti sembilan puluh lima persen. Cara lain adalah mencari siku pada grafik nilai singular, yaitu titik tempat penurunan tajam berubah menjadi landai. Dalam PCA ini setara dengan memilih jumlah komponen utama berdasarkan variansi yang dijelaskan, dan kamu akan memakainya langsung pada modul berikutnya.
        """),
        C(
            """
            import numpy as np

            A = np.diag([10.0, 5.0, 2.0, 1.0])
            s = np.linalg.svd(A, compute_uv=False)
            energi = s ** 2 / np.sum(s ** 2)
            print(energi.round(4).tolist())
            kum = np.cumsum(energi)
            print(kum.round(4).tolist())
            print(int(np.searchsorted(kum, 0.95)) + 1)
            """,
            """
            [0.7692, 0.1923, 0.0308, 0.0077]
            [0.7692, 0.9615, 0.9923, 1.0]
            2
            """,
            """
            Dua komponen pertama menjelaskan sekitar 96 persen energi sehingga cukup untuk ambang 95 persen.
            """,
            filename="energi.py",
        ),
        K(
            "warning",
            """
            Untuk PCA matriks data harus dipusatkan dulu dengan mengurangkan rata-rata tiap kolom. Tanpa itu komponen pertama hanya menunjuk ke arah rata-rata data, bukan arah variasi terbesar.
            """,
            title="Pusatkan data dulu",
        ),
        T("""
        ## Kompresi dan penghilangan derau

        Menyimpan matriks `m x n` utuh membutuhkan `m n` angka. Menyimpan `A_k` cukup membutuhkan `k` vektor `u` berukuran `m`, `k` vektor `v` berukuran `n`, dan `k` nilai singular, yaitu `k (m + n + 1)` angka. Bila `k` jauh lebih kecil daripada ukuran matriks, penghematannya besar. Inilah cara sederhana mengompres gambar abu-abu: perlakukan gambar sebagai matriks piksel dan simpan hanya komponen terkuat.

        Dekomposisi yang sama menghilangkan derau. Sinyal asli biasanya berperingkat rendah sehingga berkumpul pada nilai singular besar, sedangkan derau acak menyebar rata ke semua nilai singular kecil. Membuang nilai singular kecil membersihkan data. Pemakaian lain adalah sistem rekomendasi, saat matriks pengguna dan film dianggap berperingkat rendah karena selera orang mengikuti beberapa pola.
        """),
        C(
            """
            import numpy as np

            img = np.add.outer(np.arange(8), np.arange(8)).astype(float)
            U, s, Vt = np.linalg.svd(img, full_matrices=False)
            print(np.linalg.matrix_rank(img))
            rekon2 = (U[:, :2] * s[:2]) @ Vt[:2]
            print(np.allclose(rekon2, img))
            m, n = img.shape
            k = 2
            print(k * (m + n + 1), m * n, round(k * (m + n + 1) / (m * n), 3))
            rekon1 = (U[:, :1] * s[:1]) @ Vt[:1]
            print(round(float(np.linalg.norm(img - rekon1)), 4), round(float(s[1]), 4))
            """,
            """
            2
            True
            34 64 0.531
            5.4664 5.4664
            """,
            """
            Gambar sintetis ini berperingkat dua sehingga dua komponen merekonstruksinya sempurna dengan penyimpanan sekitar separuh. Galat memakai satu komponen sama dengan nilai singular kedua.
            """,
            filename="kompres_gambar.py",
        ),
        T("""
        ## Intuisi lewat contoh

        Bayangkan tabel penilaian film oleh seribu orang untuk lima ratus film. Selera orang tidak acak: ada kelompok pencinta aksi, pencinta drama, dan pencinta komedi. Dengan beberapa komponen saja kita dapat menjelaskan sebagian besar pola penilaian karena setiap komponen mewakili satu pola selera. Matriks besar itu berperingkat efektif rendah walau secara aljabar berperingkat penuh akibat derau kecil.

        Nilai singular mencerminkan hal itu. Beberapa nilai pertama besar dan sisanya turun cepat mendekati nol. Grafik nilai singular yang menurun tajam adalah tanda bahwa data mudah dikompres. Sebaliknya bila nilai singular turun landai, data tidak punya struktur sederhana dan kompresi akan mengorbankan banyak informasi.
        """),
        T("""
        ## Hubungan dengan PCA

        PCA pada data terpusat `X` berukuran `n x d` sebenarnya adalah SVD dari `X`. Vektor singular kanan adalah arah utama, nilai singular kuadrat dibagi `n - 1` adalah variansi tiap komponen, dan `U S` memberi skor tiap sampel pada komponen itu. Itu sebabnya banyak pustaka menghitung PCA lewat SVD, bukan lewat matriks kovariansi, karena cara itu lebih stabil dan menghindari pembentukan `X^T X`.

        Dengan pemahaman ini, memilih jumlah komponen PCA sama persis dengan memilih `k` pada pemotongan SVD, dan variansi yang dijelaskan sama dengan energi kumulatif. Modul berikutnya membangun PCA dari nol berdasarkan hubungan ini.
        """),
        E(
            "A2-06-2-ex1",
            "mudah",
            """
            Tulis fungsi `energi_kumulatif(s)` yang menerima list nilai singular terurut menurun dan mengembalikan list energi kumulatif (jumlah kuadrat sampai posisi itu dibagi total kuadrat) dibulatkan 4 desimal.
            """,
            """
            def energi_kumulatif(s):
                # TODO: implementasikan
                pass
            """,
            """
            assert energi_kumulatif([10, 5, 2, 1]) == [0.7692, 0.9615, 0.9923, 1.0]
            assert energi_kumulatif([1, 1]) == [0.5, 1.0]
            assert energi_kumulatif([3]) == [1.0]
            assert energi_kumulatif([3, 4]) == [0.36, 1.0]
            """,
            "Hitung kuadrat tiap nilai lalu jumlahkan secara kumulatif dan bagi total.",
            """
            def energi_kumulatif(s):
                kuadrat = [x * x for x in s]
                total = sum(kuadrat)
                hasil = []
                berjalan = 0.0
                for x in kuadrat:
                    berjalan += x
                    hasil.append(round(berjalan / total, 4))
                return hasil
            """,
        ),
        E(
            "A2-06-2-ex2",
            "mudah",
            """
            Tulis fungsi `pilih_k(s, ambang)` yang mengembalikan `k` terkecil sehingga energi kumulatif dari `k` nilai singular pertama minimal `ambang`. Gunakan toleransi 1e-12.
            """,
            """
            def pilih_k(s, ambang):
                # TODO: implementasikan
                pass
            """,
            """
            assert pilih_k([10, 5, 2, 1], 0.95) == 2
            assert pilih_k([10, 5, 2, 1], 0.99) == 3
            assert pilih_k([10, 5, 2, 1], 0.5) == 1
            assert pilih_k([4, 3], 1.0) == 2
            """,
            "Telusuri kumulatif dan berhenti pada posisi pertama yang mencapai ambang.",
            """
            def pilih_k(s, ambang):
                total = sum(x * x for x in s)
                berjalan = 0.0
                for i, x in enumerate(s, start=1):
                    berjalan += x * x
                    if berjalan / total >= ambang - 1e-12:
                        return i
                return len(s)
            """,
        ),
        E(
            "A2-06-2-ex3",
            "sedang",
            """
            Tulis fungsi `penyimpanan(m, n, k)` yang mengembalikan tuple `(kompres, asli, rasio)` dengan `kompres = k * (m + n + 1)`, `asli = m * n`, dan `rasio = kompres / asli` dibulatkan 4 desimal.
            """,
            """
            def penyimpanan(m, n, k):
                # TODO: implementasikan
                pass
            """,
            """
            assert penyimpanan(100, 50, 5) == (755, 5000, 0.151)
            assert penyimpanan(8, 8, 1) == (17, 64, 0.2656)
            assert penyimpanan(10, 10, 10) == (210, 100, 2.1)
            assert penyimpanan(4, 6, 2) == (22, 24, 0.9167)
            """,
            "Rumusnya langsung dari k kali (m + n + 1).",
            """
            def penyimpanan(m, n, k):
                kompres = k * (m + n + 1)
                asli = m * n
                return (kompres, asli, round(kompres / asli, 4))
            """,
        ),
        E(
            "A2-06-2-ex4",
            "menantang",
            """
            Tulis fungsi `galat_peringkat(s, k)` yang mengembalikan galat Frobenius pendekatan peringkat `k`, yaitu akar jumlah kuadrat nilai singular setelah `k` pertama, dibulatkan 4 desimal. Gunakan `math.sqrt`.
            """,
            """
            import math

            def galat_peringkat(s, k):
                # TODO: implementasikan
                pass
            """,
            """
            assert galat_peringkat([5, 3], 1) == 3.0
            assert galat_peringkat([5, 3], 0) == 5.831
            assert galat_peringkat([5, 3], 2) == 0.0
            assert galat_peringkat([13, 4, 3], 1) == 5.0
            """,
            "Jumlahkan kuadrat elemen mulai indeks k lalu ambil akar.",
            """
            import math

            def galat_peringkat(s, k):
                return round(math.sqrt(sum(x * x for x in s[k:])) + 0.0, 4)
            """,
        ),
    ],
    [
        M("Mengira pemotongan SVD hanya heuristik.", "Eckart-Young menjamin hasilnya pendekatan terbaik."),
        M("Memilih k tanpa melihat energi kumulatif.", "Gunakan ambang energi atau siku nilai singular."),
        M("Lupa memusatkan data sebelum SVD untuk PCA.", "Kurangi rata-rata tiap kolom dulu."),
    ],
    [
        Q("Pendekatan peringkat k terbaik berasal dari?", ["Pemotongan SVD", "Pemotongan acak", "Transpos", "Invers"], 0, "Teorema Eckart-Young.", hint="Optimal."),
        Q("Galat Frobenius sama dengan?", ["s terbesar", "Akar jumlah kuadrat s yang dibuang", "Jumlah s", "Nol"], 1, "Hanya bergantung pada s yang dibuang.", hint="Kuadrat lalu akar."),
        Q("Energi komponen ke-i?", ["s_i", "s_i kuadrat", "1 / s_i", "u_i"], 1, "Proporsi dihitung dari kuadrat.", hint="Variansi."),
        Q("Penyimpanan peringkat k untuk matriks m x n?", ["k(m+n+1)", "m n k", "m + n", "k k"], 0, "k vektor u, k vektor v, dan k nilai singular.", hint="Tiga bagian."),
        Q("Derau acak cenderung berada di?", ["Nilai singular besar", "Nilai singular kecil", "Hanya U", "Diagonal"], 1, "Sinyal berkumpul di nilai besar.", hint="Menyebar rata."),
    ],
    [
        "A adalah jumlah matriks peringkat satu berbobot nilai singular.",
        "Pemotongan SVD memberi aproksimasi peringkat rendah terbaik.",
        "Energi kumulatif membantu memilih jumlah komponen.",
        "Kompresi menyimpan k(m+n+1) angka dan menyaring derau.",
    ],
    [],
)

l3 = lesson(
    "A2-06-3",
    "Penerapan: pseudoinvers, kuadrat terkecil, dan LSA",
    35,
    [
        "Menyusun pseudoinvers Moore-Penrose dari SVD",
        "Menyelesaikan kuadrat terkecil dan sistem rank-deficient",
        "Menafsirkan bilangan kondisi untuk kestabilan numerik",
        "Membangun mini latent semantic analysis dari matriks term dokumen",
    ],
    [
        T("""
        ## Pseudoinvers

        Matriks yang tidak persegi atau singular tidak punya invers biasa. Namun lewat SVD kita dapat membuat penggantinya, yaitu **pseudoinvers Moore-Penrose** `A+ = V S+ U^T`. Matriks `S+` dibentuk dengan membalik tiap nilai singular tak nol menjadi kebalikannya dan membiarkan yang nol tetap nol, lalu mentranspos bentuknya.

        Pseudoinvers memberi jawaban terbaik yang masuk akal untuk `A x = b`. Bila sistem punya banyak solusi, `A+ b` memilih solusi dengan norma terkecil. Bila sistem tidak punya solusi tepat, `A+ b` memilih `x` yang membuat galat `||A x - b||` sekecil mungkin. Dua kasus yang tampak berbeda ditangani oleh satu rumus yang sama, dan bila `A` punya invers maka pseudoinversnya sama dengan invers biasa.
        """),
        C(
            """
            import numpy as np

            A = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
            U, s, Vt = np.linalg.svd(A, full_matrices=False)
            Ap = Vt.T @ np.diag(1 / s) @ U.T
            print(np.allclose(Ap, np.linalg.pinv(A)))
            b = np.array([1.0, 2.0, 2.0])
            x = Ap @ b
            print(x.round(4).tolist())
            x2 = np.linalg.lstsq(A, b, rcond=None)[0]
            print(np.allclose(x, x2))
            print(np.allclose(A @ Ap @ A, A))
            """,
            """
            True
            [-0.6667, 0.9167]
            True
            True
            """,
            """
            Rakitan manual dari SVD sama dengan `np.linalg.pinv`. Penyelesaian lewat pseudoinvers sama dengan `lstsq` dan memenuhi sifat dasar `A A+ A = A`.
            """,
            filename="pseudoinvers.py",
        ),
        T("""
        ## Kuadrat terkecil dan matriks defisit peringkat

        Regresi linear mencari `x` yang meminimalkan `||A x - b||`, dengan `A` matriks fitur yang tinggi dan sempit. Persamaan normal `A^T A x = A^T b` memang menyelesaikannya, tetapi bila fitur saling berkolinear `A^T A` hampir singular dan penyelesaiannya tidak stabil. Pendekatan SVD jauh lebih tahan karena tidak pernah membentuk `A^T A`.

        Ketika `A` defisit peringkat, ada banyak `x` yang sama baiknya. Pseudoinvers memilih yang normanya terkecil dengan mengabaikan nilai singular di bawah ambang. Perilaku ini sama dengan regularisasi: arah yang hampir tidak membawa informasi tidak diizinkan memperbesar galat. Pustaka seperti scikit-learn memakai ide ini di balik layar pada banyak penaksir linear.
        """),
        C(
            """
            import numpy as np

            A = np.array([[1.0, 1.0], [1.0, 1.0]])
            b = np.array([2.0, 2.0])
            print(np.linalg.pinv(A).round(4).tolist())
            print((np.linalg.pinv(A) @ b).round(4).tolist())

            i = np.arange(4)
            H = 1.0 / (i[:, None] + i[None, :] + 1)
            s = np.linalg.svd(H, compute_uv=False)
            print(round(float(s[0] / s[-1]), 1))
            print(round(float(np.linalg.cond(H)), 1))
            """,
            """
            [[0.25, 0.25], [0.25, 0.25]]
            [1.0, 1.0]
            15513.7
            15513.7
            """,
            """
            Untuk sistem dengan dua persamaan sama, pseudoinvers memilih solusi bernorma terkecil yaitu `[1, 1]`. Matriks Hilbert terkenal berkondisi buruk sehingga bilangan kondisinya jauh lebih besar dari satu.
            """,
            filename="kondisi.py",
        ),
        K(
            "tip",
            """
            Gunakan `np.linalg.lstsq` atau `np.linalg.pinv` untuk regresi. Hindari `np.linalg.inv(A.T @ A)` karena membesar-besarkan galat numerik saat fitur berkolinear.
            """,
            title="Cara aman regresi",
        ),
        T("""
        ## Latent semantic analysis

        **Latent Semantic Analysis** atau LSA memakai SVD untuk menemukan topik tersembunyi dalam teks. Susun **matriks term dokumen**: baris adalah kata, kolom adalah dokumen, isinya frekuensi kemunculan. Dua dokumen yang membahas topik sama sering memakai kata berbeda, sehingga kemiripan langsung antar kolom rendah walau maknanya dekat.

        SVD terpotong mengatasi ini. Dengan menyimpan hanya `k` komponen pertama, tiap dokumen diwakili oleh `k` koordinat laten, dan kata yang sering muncul bersama terkumpul pada arah yang sama. Kemiripan kosinus pada ruang laten ini menangkap hubungan makna yang tidak terlihat pada hitungan kata mentah. Gagasan ini menjadi pendahulu penyematan kata modern dan masih berguna sebagai baseline yang cepat dan transparan.
        """),
        C(
            """
            import numpy as np

            A = np.array([
                [1, 1, 0, 0],
                [1, 0, 0, 0],
                [1, 1, 0, 0],
                [0, 0, 1, 1],
                [0, 0, 1, 0],
                [0, 0, 1, 1],
            ], dtype=float)
            U, s, Vt = np.linalg.svd(A, full_matrices=False)
            k = 2
            doc = (np.diag(s[:k]) @ Vt[:k]).T
            norma = np.linalg.norm(doc, axis=1)
            sim = (doc @ doc.T) / np.outer(norma, norma)
            print(np.abs(sim).round(4).tolist())

            q = np.array([0, 1, 0, 0, 0, 0], dtype=float)
            qk = (U[:, :k].T @ q) / s[:k]
            sims = doc @ qk / (norma * np.linalg.norm(qk))
            print(int(np.argmax(sims)) < 2, bool(np.all(sims[:2] > 0.99)))
            """,
            """
            [[1.0, 1.0, 0.0, 0.0], [1.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 1.0], [0.0, 0.0, 1.0, 1.0]]
            True True
            """,
            """
            Dokumen nol dan satu membahas hewan sedangkan dua dan tiga membahas kendaraan. Pada ruang laten kemiripan dalam topik adalah satu dan antar topik nol, dan kueri tentang anjing paling dekat dengan dokumen hewan.
            """,
            filename="lsa_mini.py",
        ),
        T("""
        ## Regularisasi lewat SVD

        Mengabaikan nilai singular kecil adalah bentuk regularisasi paling sederhana, disebut SVD terpotong. Bentuk yang lebih halus adalah regresi ridge. Pada ridge, tiap nilai singular `s` pada pseudoinvers diganti dengan `s / (s^2 + lambda)` sehingga arah berinformasi rendah diredam secara mulus, bukan dipotong tiba-tiba. Parameter `lambda` mengatur kekuatan peredaman.

        Sudut pandang SVD menjelaskan mengapa regularisasi menolong. Galat kecil pada `b` diperbesar sebesar `1 / s` pada arah ke-`i`. Arah dengan `s` sangat kecil memperbesar derau secara dramatis, sehingga memotong atau meredamnya menukar sedikit bias dengan penurunan variansi yang besar.
        """),
        T("""
        ## Memilih k pada LSA

        Memilih jumlah dimensi laten pada LSA adalah seni. Terlalu kecil membuat topik berbeda menyatu, sedangkan terlalu besar mengembalikan derau dan kata yang jarang muncul. Praktisi biasanya mencoba beberapa nilai antara seratus dan tiga ratus pada korpus besar, lalu menilai hasilnya pada tugas hilir seperti pengelompokan atau pencarian. Pada contoh mini kita dua dimensi sudah cukup karena hanya ada dua topik.

        Satu catatan penting: frekuensi mentah memberi bobot besar pada kata umum. Pembobotan seperti TF-IDF biasanya diterapkan sebelum SVD agar kata yang informatif lebih menentukan. Dengan begitu komponen laten lebih mencerminkan topik daripada kata penghubung yang muncul di mana-mana.
        """),
        T("""
        ## Merangkum modul

        Kita mulai dari bentuk `A = U S V^T` yang berlaku untuk matriks apa pun, membaca nilai singular sebagai peregangan sepanjang arah utama, lalu memotongnya untuk mendapat pendekatan terbaik. Dari sana lahir kompresi, penyaringan derau, pseudoinvers, penyelesaian kuadrat terkecil yang stabil, dan penemuan topik laten pada teks.

        Benang merahnya satu: data berdimensi tinggi sering kali punya struktur berdimensi rendah, dan SVD adalah cara paling langsung untuk menemukannya. Kamu sudah memegang semua alat yang dibutuhkan untuk modul PCA berikutnya.
        """),
        E(
            "A2-06-3-ex1",
            "mudah",
            """
            Tulis fungsi `pseudoinvers_diagonal(s, tol=1e-10)` yang mengembalikan list kebalikan tiap nilai singular yang lebih besar dari `tol` dan `0.0` untuk yang lain, dibulatkan 4 desimal.
            """,
            """
            def pseudoinvers_diagonal(s, tol=1e-10):
                # TODO: implementasikan
                pass
            """,
            """
            assert pseudoinvers_diagonal([2, 4]) == [0.5, 0.25]
            assert pseudoinvers_diagonal([3, 0]) == [0.3333, 0.0]
            assert pseudoinvers_diagonal([0.0]) == [0.0]
            assert pseudoinvers_diagonal([1e-12, 5]) == [0.0, 0.2]
            """,
            "Balik hanya nilai yang melewati ambang.",
            """
            def pseudoinvers_diagonal(s, tol=1e-10):
                return [round(1 / x, 4) if x > tol else 0.0 for x in s]
            """,
        ),
        E(
            "A2-06-3-ex2",
            "mudah",
            """
            Tulis fungsi `bilangan_kondisi(s)` yang menerima list nilai singular terurut menurun dan mengembalikan rasio nilai terbesar terhadap terkecil dibulatkan 4 desimal. Bila nilai terkecil nol kembalikan `None`.
            """,
            """
            def bilangan_kondisi(s):
                # TODO: implementasikan
                pass
            """,
            """
            assert bilangan_kondisi([5, 3]) == 1.6667
            assert bilangan_kondisi([10, 10]) == 1.0
            assert bilangan_kondisi([4, 0]) is None
            assert bilangan_kondisi([100, 1]) == 100.0
            """,
            "Bagi elemen pertama dengan elemen terakhir.",
            """
            def bilangan_kondisi(s):
                if s[-1] == 0:
                    return None
                return round(s[0] / s[-1], 4)
            """,
        ),
        E(
            "A2-06-3-ex3",
            "sedang",
            """
            Tulis fungsi `kuadrat_terkecil(A, b)` yang mengembalikan solusi kuadrat terkecil bernorma minimum sebagai list dibulatkan 4 desimal, dengan memakai `np.linalg.svd` ringkas dan mengabaikan nilai singular di bawah 1e-10. Hindari `-0.0`.
            """,
            """
            import numpy as np

            def kuadrat_terkecil(A, b):
                # TODO: implementasikan
                pass
            """,
            """
            assert kuadrat_terkecil([[1, 0], [0, 1], [0, 0]], [1, 2, 3]) == [1.0, 2.0]
            assert kuadrat_terkecil([[1, 1], [1, 2], [1, 3]], [1, 2, 2]) == [0.6667, 0.5]
            assert kuadrat_terkecil([[2]], [6]) == [3.0]
            assert kuadrat_terkecil([[1, 1], [1, 1]], [2, 2]) == [1.0, 1.0]
            """,
            "Hitung x = V diag(1/s) U^T b dengan 1/s diganti nol untuk nilai kecil.",
            """
            import numpy as np

            def kuadrat_terkecil(A, b):
                U, s, Vt = np.linalg.svd(np.array(A, dtype=float), full_matrices=False)
                sinv = np.array([1 / x if x > 1e-10 else 0.0 for x in s])
                x = Vt.T @ (sinv * (U.T @ np.array(b, dtype=float)))
                return [round(float(v), 4) + 0.0 for v in x]
            """,
        ),
        E(
            "A2-06-3-ex4",
            "menantang",
            """
            Tulis fungsi `kemiripan_dokumen(A, k)` yang menerima matriks term dokumen (list of list) dan mengembalikan matriks kemiripan kosinus antar dokumen (kolom) pada ruang laten `k` dimensi, memakai koordinat `diag(s[:k]) @ Vt[:k]`. Bulatkan 4 desimal dan hindari `-0.0`.
            """,
            """
            import numpy as np

            def kemiripan_dokumen(A, k):
                # TODO: implementasikan
                pass
            """,
            """
            B = [[1, 1, 0, 0], [1, 0, 0, 0], [1, 1, 0, 0], [0, 0, 1, 1], [0, 0, 1, 0], [0, 0, 1, 1]]
            assert kemiripan_dokumen(B, 2) == [[1.0, 1.0, 0.0, 0.0], [1.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 1.0], [0.0, 0.0, 1.0, 1.0]]
            assert kemiripan_dokumen([[1, 2], [2, 4]], 1) == [[1.0, 1.0], [1.0, 1.0]]
            assert kemiripan_dokumen([[1, 0], [0, 1]], 2) == [[1.0, 0.0], [0.0, 1.0]]
            """,
            "Bentuk koordinat dokumen lalu hitung hasil kali dalam dibagi hasil kali norma.",
            """
            import numpy as np

            def kemiripan_dokumen(A, k):
                U, s, Vt = np.linalg.svd(np.array(A, dtype=float), full_matrices=False)
                doc = (np.diag(s[:k]) @ Vt[:k]).T
                norma = np.linalg.norm(doc, axis=1)
                sim = (doc @ doc.T) / np.outer(norma, norma)
                return [[round(float(x), 4) + 0.0 for x in baris] for baris in sim]
            """,
        ),
    ],
    [
        M("Memakai inv(A.T @ A) untuk regresi.", "Pakai pinv atau lstsq yang berbasis SVD."),
        M("Membalik semua nilai singular termasuk yang hampir nol.", "Abaikan nilai di bawah ambang."),
        M("Membandingkan dokumen hanya dengan hitungan kata mentah.", "Bandingkan pada ruang laten hasil SVD terpotong."),
    ],
    [
        Q("Rumus pseudoinvers?", ["V S+ U^T", "U S V^T", "S^-1", "A^T"], 0, "Balik nilai singular tak nol.", hint="Faktor dibalik."),
        Q("Pseudoinvers memilih solusi?", ["Norma terbesar", "Norma terkecil", "Acak", "Nol"], 1, "Solusi bernorma minimum.", hint="Paling hemat."),
        Q("Bilangan kondisi besar berarti?", ["Matriks sehat", "Matriks hampir singular", "Matriks identitas", "Matriks nol"], 1, "Galat kecil diperbesar.", hint="Tidak stabil."),
        Q("Baris matriks term dokumen adalah?", ["Dokumen", "Kata", "Topik", "Norma"], 1, "Baris kata dan kolom dokumen.", hint="Term."),
        Q("Kenapa LSA memakai SVD terpotong?", ["Untuk menambah derau", "Untuk menangkap topik laten", "Untuk mengurutkan kata", "Untuk menghapus dokumen"], 1, "Kata sekonteks berkumpul pada arah yang sama.", hint="Makna tersembunyi."),
    ],
    [
        "Pseudoinvers dari SVD memberi solusi kuadrat terkecil bernorma minimum.",
        "Pendekatan SVD stabil untuk fitur berkolinear.",
        "Bilangan kondisi mengukur kestabilan sistem linear.",
        "LSA membandingkan dokumen pada ruang laten dari SVD terpotong.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa perhitungan dan contoh kode yang cukup jelas dalam teks.", "brief": []}

write_module(
    "A2",
    6,
    "Singular Value Decomposition",
    105,
    [
        "Memahami dan menghitung SVD",
        "Memakai aproksimasi peringkat rendah untuk kompresi",
        "Menerapkan SVD pada pseudoinvers, kuadrat terkecil, dan LSA",
    ],
    [l1, l2, l3],
    video,
    REF,
)
