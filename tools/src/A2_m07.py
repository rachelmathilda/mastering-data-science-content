import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

l1 = lesson(
    "A2-07-1",
    "Ide PCA dan langkah-langkahnya",
    35,
    [
        "Memahami tujuan PCA sebagai pencarian arah variasi terbesar",
        "Memusatkan data dan menghitung matriks kovariansi",
        "Mengambil komponen utama dari eigenvector kovariansi",
        "Menghitung skor dan variansi tiap komponen",
    ],
    [
        T("""
        ## Masalah yang diselesaikan PCA

        Data nyata sering memiliki puluhan atau ratusan fitur, padahal banyak di antaranya saling terkait. Tinggi badan dan berat badan bergerak bersama. Harga rumah dan luas bangunan berkorelasi. Bila dua fitur membawa informasi yang hampir sama, menyimpan keduanya boros dan sering merusak model. **Principal Component Analysis** atau PCA mencari sumbu baru yang merangkum variasi data dengan sesedikit mungkin dimensi.

        Gagasannya: temukan arah tempat data paling menyebar, jadikan itu sumbu pertama. Cari arah berikutnya yang tegak lurus terhadap sumbu pertama dan menangkap sebanyak mungkin sisa variasi, jadikan sumbu kedua, lalu seterusnya. Sumbu-sumbu ini disebut **komponen utama**. Dengan mempertahankan beberapa sumbu pertama kita mereduksi dimensi sambil kehilangan sedikit informasi.
        """),
        T("""
        ## Mengapa variasi yang dicari

        Mengapa arah dengan variasi terbesar dianggap paling informatif? Fitur yang hampir konstan tidak membedakan satu sampel dari sampel lain, sehingga nyaris tidak berguna. Arah tempat sampel tersebar lebar adalah arah tempat perbedaan antar sampel terlihat jelas. PCA menganggap perbedaan besar sebagai sinyal dan perbedaan kecil sebagai derau.

        Asumsi ini tidak selalu benar. Kadang informasi penting justru tersembunyi pada arah variasi kecil, dan PCA akan membuangnya. PCA juga tidak mengenal label kelas: ia tak tahu mana variasi yang berguna untuk prediksi. Karena itu PCA adalah alat tanpa pengawasan yang cocok untuk eksplorasi, visualisasi, kompresi, dan penyaringan derau, tetapi bukan jaminan peningkatan akurasi model.
        """),
        T("""
        ## Langkah satu: pusatkan data

        Langkah pertama selalu memusatkan data dengan mengurangkan rata-rata tiap kolom. Hasilnya `Xc` memiliki rata-rata nol pada setiap fitur sehingga awan data berpusat di titik asal. Tanpa langkah ini komponen pertama hanya menunjuk dari titik asal ke pusat data, bukan ke arah penyebaran data.

        Langkah kedua adalah menghitung **matriks kovariansi** `C = Xc^T Xc / (n - 1)`. Diagonalnya berisi variansi tiap fitur dan elemen lainnya berisi kovariansi antar dua fitur. Kovariansi positif berarti dua fitur cenderung naik bersama, negatif berarti berlawanan, dan nol berarti tidak ada hubungan linear. Matriks ini simetris dan semua eigenvalue-nya tak negatif, sesuai pelajaran eigen sebelumnya.
        """),
        C(
            """
            import numpy as np

            X = np.array([[2.0, 2.0], [4.0, 3.0], [6.0, 7.0], [8.0, 8.0]])
            rata = X.mean(axis=0)
            Xc = X - rata
            print(rata.tolist())
            print(np.allclose(Xc.mean(axis=0), 0))
            n = X.shape[0]
            C = Xc.T @ Xc / (n - 1)
            print(C.round(4).tolist())
            print(np.allclose(C, np.cov(X.T)))
            """,
            """
            [5.0, 5.0]
            True
            [[6.6667, 7.3333], [7.3333, 8.6667]]
            True
            """,
            """
            Setelah dipusatkan rata-rata tiap kolom nol. Rumus kovariansi manual sama dengan `np.cov` yang membagi dengan `n - 1`.
            """,
            filename="pusat_data.py",
        ),
        T("""
        ## Langkah tiga: eigen dari kovariansi

        Inti PCA adalah fakta yang kamu pelajari pada modul sebelumnya: untuk matriks simetris, eigenvector saling ortogonal dan eigenvalue menyatakan variansi. Eigenvector dari matriks kovariansi adalah **komponen utama**, dan eigenvalue-nya adalah variansi data sepanjang komponen itu. Urutkan dari eigenvalue terbesar ke terkecil, dan komponen pertama adalah arah penyebaran maksimum.

        Jumlah semua eigenvalue sama dengan trace kovariansi, yaitu total variansi semua fitur. Jadi proporsi variansi yang dijelaskan komponen ke-`i` adalah eigenvalue-nya dibagi total. Untuk matriks simetris kita memakai `np.linalg.eigh`, yang mengurutkan eigenvalue naik, sehingga hasilnya perlu dibalik agar terbesar berada di depan.
        """),
        C(
            """
            import numpy as np

            X = np.array([[2.0, 2.0], [4.0, 3.0], [6.0, 7.0], [8.0, 8.0]])
            Xc = X - X.mean(axis=0)
            C = Xc.T @ Xc / (X.shape[0] - 1)
            nilai, vektor = np.linalg.eigh(C)
            nilai, vektor = nilai[::-1], vektor[:, ::-1]
            print(nilai.round(4).tolist())
            print((nilai / nilai.sum()).round(4).tolist())
            print(np.abs(vektor[:, 0]).round(4).tolist())
            print(round(float(vektor[:, 0] @ vektor[:, 1]), 6) + 0.0)
            """,
            """
            [15.0679, 0.2655]
            [0.9827, 0.0173]
            [0.6576, 0.7534]
            0.0
            """,
            """
            Komponen pertama menjelaskan hampir seluruh variansi karena kedua fitur naik bersama. Dua komponen saling tegak lurus sehingga hasil kali dalamnya nol.
            """,
            filename="pca_eigen.py",
        ),
        K(
            "warning",
            """
            Tanda eigenvector tidak tetap: komponen yang sama bisa muncul dengan tanda positif atau negatif pada pustaka atau versi berbeda. Itu bukan kesalahan karena arah berlawanan menunjuk sumbu yang sama.
            """,
            title="Tanda tidak penting",
        ),
        T("""
        ## Langkah empat: skor dan proyeksi

        Setelah komponen diketahui, kita memproyeksikan data ke sumbu baru. **Skor** sampel pada komponen ke-`i` adalah hasil kali dalam antara sampel yang dipusatkan dan eigenvector ke-`i`. Dalam bentuk matriks, `Z = Xc W` dengan `W` berisi komponen yang dipertahankan sebagai kolom. Bila `W` hanya memuat `k` kolom, `Z` berukuran `n x k`: data kita kini punya `k` fitur baru.

        Fitur baru ini punya sifat bagus. Mereka tidak berkorelasi satu sama lain, karena kovariansi `Z` diagonal. Variansi tiap kolom `Z` sama dengan eigenvalue yang bersesuaian. Jadi PCA sekaligus memutar data ke sistem koordinat yang fiturnya saling bebas secara linear, yang sering mempermudah model setelahnya.
        """),
        C(
            """
            import numpy as np

            X = np.array([[2.0, 2.0], [4.0, 3.0], [6.0, 7.0], [8.0, 8.0]])
            Xc = X - X.mean(axis=0)
            C = Xc.T @ Xc / (X.shape[0] - 1)
            nilai, vektor = np.linalg.eigh(C)
            nilai, vektor = nilai[::-1], vektor[:, ::-1]
            Z = Xc @ vektor
            print(np.abs(Z[:, 0]).round(4).tolist())
            print(np.allclose(Z.var(axis=0, ddof=1), nilai))
            kov = np.cov(Z.T)
            print(round(abs(float(kov[0, 1])), 6))
            """,
            """
            [4.2329, 2.1643, 2.1643, 4.2329]
            True
            0.0
            """,
            """
            Skor pada komponen pertama menyebar paling lebar. Variansi tiap skor sama dengan eigenvalue dan kovariansi antar skor nol.
            """,
            filename="proyeksi.py",
        ),
        T("""
        ## Ringkasan alur

        Alur PCA dapat dihafal dalam empat kata: pusatkan, kovariansi, eigen, proyeksikan. Pusatkan data agar berpusat di titik asal. Hitung kovariansi untuk mengukur hubungan antar fitur. Ambil eigenvector dan eigenvalue untuk menemukan arah dan variansinya. Proyeksikan data ke arah terbaik untuk mendapat fitur baru yang lebih ringkas.
        """),
        E(
            "A2-07-1-ex1",
            "mudah",
            """
            Tulis fungsi `pusatkan(kolom)` yang mengurangkan rata-rata dari tiap elemen list angka dan mengembalikan list dibulatkan 4 desimal. Hindari `-0.0`.
            """,
            """
            def pusatkan(kolom):
                # TODO: implementasikan
                pass
            """,
            """
            assert pusatkan([1, 2, 3]) == [-1.0, 0.0, 1.0]
            assert pusatkan([5, 5, 5]) == [0.0, 0.0, 0.0]
            assert pusatkan([2, 4, 6, 8]) == [-3.0, -1.0, 1.0, 3.0]
            assert pusatkan([10]) == [0.0]
            """,
            "Hitung rata-rata lalu kurangkan dari setiap elemen.",
            """
            def pusatkan(kolom):
                rata = sum(kolom) / len(kolom)
                return [round(x - rata, 4) + 0.0 for x in kolom]
            """,
        ),
        E(
            "A2-07-1-ex2",
            "mudah",
            """
            Tulis fungsi `kovariansi(x, y)` yang mengembalikan kovariansi sampel (dibagi `n - 1`) dua list sama panjang, dibulatkan 4 desimal. Hindari `-0.0`.
            """,
            """
            def kovariansi(x, y):
                # TODO: implementasikan
                pass
            """,
            """
            assert kovariansi([2, 4, 6, 8], [2, 3, 7, 8]) == 7.3333
            assert kovariansi([1, 2, 3], [1, 2, 3]) == 1.0
            assert kovariansi([1, 2, 3], [3, 2, 1]) == -1.0
            assert kovariansi([1, 2, 3], [5, 5, 5]) == 0.0
            """,
            "Jumlahkan hasil kali simpangan dari rata-rata lalu bagi n dikurangi satu.",
            """
            def kovariansi(x, y):
                n = len(x)
                mx, my = sum(x) / n, sum(y) / n
                return round(sum((a - mx) * (b - my) for a, b in zip(x, y)) / (n - 1), 4) + 0.0
            """,
        ),
        E(
            "A2-07-1-ex3",
            "sedang",
            """
            Tulis fungsi `matriks_kovariansi(X)` yang menerima list of list (baris adalah sampel, kolom adalah fitur) dan mengembalikan matriks kovariansi sampel sebagai list of list dibulatkan 4 desimal. Hindari `-0.0`.
            """,
            """
            def matriks_kovariansi(X):
                # TODO: implementasikan
                pass
            """,
            """
            assert matriks_kovariansi([[2, 2], [4, 3], [6, 7], [8, 8]]) == [[6.6667, 7.3333], [7.3333, 8.6667]]
            assert matriks_kovariansi([[1, 2], [2, 4], [3, 6]]) == [[1.0, 2.0], [2.0, 4.0]]
            assert matriks_kovariansi([[1], [2], [3]]) == [[1.0]]
            assert matriks_kovariansi([[1, 5], [2, 5], [3, 5]]) == [[1.0, 0.0], [0.0, 0.0]]
            """,
            "Pusatkan tiap kolom lalu hitung hasil kali dalam antar kolom dibagi n dikurangi satu.",
            """
            def matriks_kovariansi(X):
                n, d = len(X), len(X[0])
                rata = [sum(baris[j] for baris in X) / n for j in range(d)]
                return [[round(sum((baris[i] - rata[i]) * (baris[j] - rata[j]) for baris in X) / (n - 1), 4) + 0.0 for j in range(d)] for i in range(d)]
            """,
        ),
        E(
            "A2-07-1-ex4",
            "menantang",
            """
            Tulis fungsi `komponen_utama_2d(X)` yang menerima data dua fitur (list of list) dan mengembalikan tuple `(eigenvalue_terbesar, proporsi)` dari matriks kovariansinya, keduanya dibulatkan 4 desimal. Gunakan rumus trace dan determinan dan potong diskriminan negatif kecil menjadi nol.
            """,
            """
            def komponen_utama_2d(X):
                # TODO: implementasikan
                pass
            """,
            """
            assert komponen_utama_2d([[2, 2], [4, 3], [6, 7], [8, 8]]) == (15.0679, 0.9827)
            assert komponen_utama_2d([[1, 2], [2, 4], [3, 6]]) == (5.0, 1.0)
            assert komponen_utama_2d([[1, 0], [2, 0], [3, 0]]) == (1.0, 1.0)
            assert komponen_utama_2d([[1, 0], [-1, 0], [0, 1], [0, -1]]) == (0.6667, 0.5)
            """,
            "Bentuk kovariansi 2x2 lalu selesaikan lambda kuadrat dikurangi trace kali lambda ditambah determinan.",
            """
            def komponen_utama_2d(X):
                n = len(X)
                mx = sum(b[0] for b in X) / n
                my = sum(b[1] for b in X) / n
                a = sum((b[0] - mx) ** 2 for b in X) / (n - 1)
                d = sum((b[1] - my) ** 2 for b in X) / (n - 1)
                c = sum((b[0] - mx) * (b[1] - my) for b in X) / (n - 1)
                tr = a + d
                det = a * d - c * c
                disk = max(tr * tr - 4 * det, 0.0)
                lam = (tr + disk ** 0.5) / 2
                return (round(lam, 4), round(lam / tr, 4))
            """,
        ),
    ],
    [
        M("Lupa memusatkan data sebelum PCA.", "Kurangi rata-rata tiap kolom dulu."),
        M("Menganggap tanda eigenvector bermakna.", "Arah berlawanan menunjuk sumbu yang sama."),
        M("Mengira PCA memakai label kelas.", "PCA tanpa pengawasan dan hanya melihat variasi."),
    ],
    [
        Q("Apa yang dicari komponen pertama?", ["Arah variasi terbesar", "Arah variasi terkecil", "Rata-rata", "Median"], 0, "Sumbu tempat data paling menyebar.", hint="Penyebaran."),
        Q("Langkah pertama PCA?", ["Menghitung invers", "Memusatkan data", "Menghapus fitur", "Mengurutkan sampel"], 1, "Kurangi rata-rata tiap kolom.", hint="Pusat di titik asal."),
        Q("Komponen utama adalah eigenvector dari?", ["Matriks data", "Matriks kovariansi", "Matriks identitas", "Matriks label"], 1, "Eigenvector kovariansi.", hint="Simetris."),
        Q("Eigenvalue komponen menyatakan?", ["Mean", "Variansi sepanjang komponen", "Jumlah sampel", "Korelasi"], 1, "Variansi arah itu.", hint="Penyebaran."),
        Q("Sifat skor antar komponen?", ["Berkorelasi kuat", "Tidak berkorelasi", "Selalu sama", "Negatif"], 1, "Kovariansi skor diagonal.", hint="Ortogonal."),
    ],
    [
        "PCA mencari arah variasi terbesar dan memproyeksikan data ke sana.",
        "Pusatkan data lalu hitung kovariansi dan eigen-nya.",
        "Eigenvalue adalah variansi komponen dan jumlahnya sama dengan total variansi.",
        "Skor antar komponen tidak berkorelasi.",
    ],
    [],
)

l2 = lesson(
    "A2-07-2",
    "PCA lewat SVD dan rekonstruksi",
    35,
    [
        "Menghubungkan PCA dengan SVD dari data terpusat",
        "Menghitung variansi dan proporsi dari nilai singular",
        "Memakai PCA dari scikit-learn dan membandingkannya dengan versi manual",
        "Merekonstruksi data dari sebagian komponen dan mengukur galatnya",
    ],
    [
        T("""
        ## PCA sebagai SVD

        Pada pelajaran sebelumnya kita menghitung PCA lewat eigen dari matriks kovariansi. Ada jalan yang lebih stabil: SVD langsung dari matriks data terpusat. Tulis `Xc = U S V^T`. Maka `Xc^T Xc = V S^2 V^T`, sehingga kolom `V` adalah eigenvector kovariansi, yaitu komponen utama, dan variansinya adalah `s^2 / (n - 1)`.

        Keuntungannya nyata. Kita tidak perlu membentuk matriks kovariansi, yang mengkuadratkan bilangan kondisi dan membuang presisi. SVD juga bekerja dengan baik saat jumlah fitur lebih besar daripada jumlah sampel, kasus umum pada data gen atau teks. Skor sampel adalah `U S`, yang sama dengan `Xc V`. Karena itu hampir semua pustaka, termasuk scikit-learn, menghitung PCA dengan SVD.
        """),
        C(
            """
            import numpy as np

            X = np.array([[2.0, 2.0], [4.0, 3.0], [6.0, 7.0], [8.0, 8.0]])
            Xc = X - X.mean(axis=0)
            n = X.shape[0]
            U, s, Vt = np.linalg.svd(Xc, full_matrices=False)
            variansi = s ** 2 / (n - 1)
            nilai = np.linalg.eigvalsh(np.cov(X.T))[::-1]
            print(variansi.round(4).tolist())
            print(np.allclose(variansi, nilai))
            Z = U * s
            print(np.allclose(np.abs(Z), np.abs(Xc @ Vt.T)))
            print(np.abs(Vt[0]).round(4).tolist())
            """,
            """
            [15.0679, 0.2655]
            True
            True
            [0.6576, 0.7534]
            """,
            """
            Variansi dari nilai singular sama dengan eigenvalue kovariansi. Skor `U S` sama dengan `Xc V` sampai tanda.
            """,
            filename="pca_svd.py",
        ),
        T("""
        ## Variansi yang dijelaskan

        Setelah mendapat variansi tiap komponen, kita menghitung **proporsi variansi yang dijelaskan**: variansi komponen dibagi total. Jumlah kumulatifnya menunjukkan berapa banyak informasi yang bertahan bila kita hanya menyimpan sejumlah komponen pertama. Inilah dasar pemilihan `k` pada PCA, sama dengan energi kumulatif pada SVD.

        Dua konvensi lazim: ambil `k` terkecil dengan proporsi kumulatif minimal sembilan puluh lima persen, atau gunakan grafik scree dan pilih titik siku tempat penurunan tajam menjadi landai. Tidak ada angka ajaib. Untuk visualisasi dipakai dua atau tiga komponen berapa pun proporsinya, sedangkan untuk kompresi atau praproses model ambang lebih tinggi biasanya dipilih dan diuji lewat validasi silang.
        """),
        C(
            """
            import numpy as np
            from sklearn.decomposition import PCA

            X = np.array([[2.0, 2.0], [4.0, 3.0], [6.0, 7.0], [8.0, 8.0]])
            pca = PCA(n_components=2).fit(X)
            print(pca.explained_variance_.round(4).tolist())
            print(pca.explained_variance_ratio_.round(4).tolist())
            print(pca.mean_.tolist())
            print(pca.components_.shape)
            Z = pca.transform(X)
            print(Z.shape, np.allclose(Z.mean(axis=0), 0))
            """,
            """
            [15.0679, 0.2655]
            [0.9827, 0.0173]
            [5.0, 5.0]
            (2, 2)
            (4, 2) True
            """,
            """
            `PCA` dari scikit-learn memberi variansi dan proporsi yang sama dengan hitungan manual. Atribut `components_` menyimpan komponen sebagai baris dan `mean_` menyimpan rata-rata yang dikurangkan.
            """,
            filename="sklearn_pca.py",
        ),
        K(
            "tip",
            """
            Di scikit-learn komponen berada di baris `components_`, berbeda dengan eigenvector NumPy yang berada di kolom. Pada `transform` rata-rata dikurangkan otomatis, jadi jangan memusatkan data dua kali.
            """,
            title="Baris atau kolom",
        ),
        T("""
        ## Rekonstruksi dari komponen

        PCA dapat dibalik. Bila kita memproyeksikan ke `k` komponen untuk mendapat `Z = Xc W_k`, kita merekonstruksi pendekatan data dengan `X_hat = Z W_k^T + rata`. Hasilnya adalah titik-titik yang jatuh pada subruang berdimensi `k` yang paling dekat dengan data asli. Selisih antara `X` dan `X_hat` adalah informasi yang dibuang.

        **Galat rekonstruksi** rata-rata kuadrat sama dengan jumlah eigenvalue komponen yang dibuang, dibagi jumlah fitur. Jadi kualitas kompresi bisa dihitung hanya dari eigenvalue. Bila `k` sama dengan jumlah fitur, rekonstruksi sempurna. Ide ini dipakai untuk penyaringan derau: proyeksikan lalu rekonstruksi, dan derau yang tersebar di arah variasi kecil ikut terbuang.
        """),
        C(
            """
            import numpy as np

            X = np.array([[2.0, 0.0, 1.0], [3.0, 1.0, 2.0], [4.0, 1.0, 3.0],
                          [5.0, 2.0, 3.0], [6.0, 2.0, 5.0], [7.0, 3.0, 5.0]])
            rata = X.mean(axis=0)
            Xc = X - rata
            U, s, Vt = np.linalg.svd(Xc, full_matrices=False)
            for k in (1, 2, 3):
                W = Vt[:k].T
                Xh = (Xc @ W) @ W.T + rata
                print(k, round(float(np.mean((X - Xh) ** 2)), 4))
            print(np.allclose(Xh, X))
            """,
            """
            1 0.0552
            2 0.0044
            3 0.0
            True
            """,
            """
            Galat rekonstruksi turun saat komponen bertambah dan menjadi nol ketika semua komponen dipakai.
            """,
            filename="rekonstruksi_pca.py",
        ),
        T("""
        ## Penyaringan derau dan kompresi

        Dua pemakaian praktis rekonstruksi adalah penyaringan derau dan kompresi. Pada penyaringan derau, sinyal sebenarnya terkonsentrasi di sedikit komponen pertama sedangkan derau menyebar di semua arah dengan variansi kecil. Memproyeksikan ke `k` komponen lalu merekonstruksi menghapus sebagian besar derau tanpa banyak merusak sinyal.

        Pada kompresi, kita menyimpan `Z`, `W`, dan rata-rata saja alih-alih `X` penuh. Penghematannya besar bila `k` kecil. Contohnya pengenalan wajah klasik dengan eigenfaces: tiap wajah diwakili oleh puluhan koefisien, bukan ribuan piksel. Pendekatan ini masih dipakai sebagai baseline yang cepat sebelum beralih ke metode berbasis jaringan saraf.
        """),
        T("""
        ## Memilih antara eigen dan SVD

        Secara teori dua jalan memberi hasil sama, tetapi praktiknya berbeda. Jalur eigen cocok untuk pembelajaran karena langkahnya terlihat jelas: kovariansi, eigenvector, proyeksi. Jalur SVD cocok untuk produksi karena stabil dan efisien, terutama pada data lebar dengan banyak fitur dan sedikit sampel. Pada data seperti itu matriks kovariansi berukuran fitur kali fitur sangat besar dan tidak perlu dibentuk sama sekali.

        Scikit-learn bahkan menyediakan solver acak yang memakai SVD terpotong untuk menghitung hanya beberapa komponen pertama. Pada data besar ini jauh lebih cepat daripada dekomposisi penuh dan hasilnya hampir identik. Pahami dulu cara kerja manualnya agar kamu tahu apa yang terjadi di balik panggilan satu baris itu.
        """),
        T("""
        ## Membaca hasil dengan hati-hati

        Beberapa kebiasaan baik membantu saat memakai PCA. Selalu periksa proporsi variansi sebelum menafsirkan hasil: bila dua komponen pertama hanya menjelaskan tiga puluh persen, diagram dua dimensi tidak mewakili data dengan baik dan kesimpulan dari gambar itu lemah. Periksa juga loading untuk memastikan komponen punya arti yang masuk akal secara domain.

        Bandingkan galat rekonstruksi antar pilihan `k` pada data uji, bukan hanya data latih. Bila galat uji berhenti turun saat `k` bertambah, komponen tambahan hanya menangkap derau. Kebiasaan ini membuat reduksi dimensi menjadi keputusan berbasis bukti, bukan tebakan.
        """),
        E(
            "A2-07-2-ex1",
            "mudah",
            """
            Tulis fungsi `variansi_dari_singular(s, n)` yang menerima list nilai singular data terpusat dan jumlah sampel `n` lalu mengembalikan list `s^2 / (n - 1)` dibulatkan 4 desimal.
            """,
            """
            def variansi_dari_singular(s, n):
                # TODO: implementasikan
                pass
            """,
            """
            assert variansi_dari_singular([6, 2], 5) == [9.0, 1.0]
            assert variansi_dari_singular([3], 4) == [3.0]
            assert variansi_dari_singular([0, 0], 3) == [0.0, 0.0]
            assert variansi_dari_singular([4, 3], 3) == [8.0, 4.5]
            """,
            "Kuadratkan tiap nilai lalu bagi dengan n dikurangi satu.",
            """
            def variansi_dari_singular(s, n):
                return [round(x * x / (n - 1), 4) for x in s]
            """,
        ),
        E(
            "A2-07-2-ex2",
            "mudah",
            """
            Tulis fungsi `proporsi_kumulatif(variansi)` yang mengembalikan list proporsi kumulatif variansi (jumlah sampai posisi itu dibagi total) dibulatkan 4 desimal.
            """,
            """
            def proporsi_kumulatif(variansi):
                # TODO: implementasikan
                pass
            """,
            """
            assert proporsi_kumulatif([9, 1]) == [0.9, 1.0]
            assert proporsi_kumulatif([2, 1, 1]) == [0.5, 0.75, 1.0]
            assert proporsi_kumulatif([4]) == [1.0]
            assert proporsi_kumulatif([1, 1, 1, 1]) == [0.25, 0.5, 0.75, 1.0]
            """,
            "Akumulasikan variansi lalu bagi dengan total.",
            """
            def proporsi_kumulatif(variansi):
                total = sum(variansi)
                hasil = []
                berjalan = 0.0
                for v in variansi:
                    berjalan += v
                    hasil.append(round(berjalan / total, 4))
                return hasil
            """,
        ),
        E(
            "A2-07-2-ex3",
            "sedang",
            """
            Tulis fungsi `proyeksikan(X, arah)` yang memusatkan data `X` (list of list) lalu mengembalikan list skor, yaitu hasil kali dalam tiap baris terpusat dengan vektor `arah` (sudah satuan), dibulatkan 4 desimal. Hindari `-0.0`.
            """,
            """
            def proyeksikan(X, arah):
                # TODO: implementasikan
                pass
            """,
            """
            assert proyeksikan([[1, 2], [3, 4], [5, 6]], [1, 0]) == [-2.0, 0.0, 2.0]
            assert proyeksikan([[1, 2], [3, 4], [5, 6]], [0, 1]) == [-2.0, 0.0, 2.0]
            assert proyeksikan([[1, 2], [3, 4], [5, 6]], [0.6, 0.8]) == [-2.8, 0.0, 2.8]
            assert proyeksikan([[2, 2]], [1, 0]) == [0.0]
            """,
            "Hitung rata-rata tiap kolom lalu kurangkan sebelum mengalikan dengan arah.",
            """
            def proyeksikan(X, arah):
                n, d = len(X), len(X[0])
                rata = [sum(b[j] for b in X) / n for j in range(d)]
                return [round(sum((b[j] - rata[j]) * arah[j] for j in range(d)), 4) + 0.0 for b in X]
            """,
        ),
        E(
            "A2-07-2-ex4",
            "menantang",
            """
            Tulis fungsi `galat_rekonstruksi(X, arah)` yang memusatkan `X`, memproyeksikannya ke satu `arah` satuan, merekonstruksi, dan mengembalikan rata-rata kuadrat galat atas semua entri (jumlah kuadrat galat dibagi `n * d`), dibulatkan 4 desimal.
            """,
            """
            def galat_rekonstruksi(X, arah):
                # TODO: implementasikan
                pass
            """,
            """
            r = 0.5 ** 0.5
            assert galat_rekonstruksi([[1, 2], [3, 4], [5, 6]], [r, r]) == 0.0
            assert galat_rekonstruksi([[1, 2], [3, 4], [5, 6]], [1, 0]) == 1.3333
            assert galat_rekonstruksi([[1, 2], [3, 4], [5, 6]], [0, 1]) == 1.3333
            assert galat_rekonstruksi([[0, 0], [2, 0]], [1, 0]) == 0.0
            """,
            "Rekonstruksi satu baris adalah skor kali arah. Galat adalah selisih terpusat dikurangi rekonstruksi itu.",
            """
            def galat_rekonstruksi(X, arah):
                n, d = len(X), len(X[0])
                rata = [sum(b[j] for b in X) / n for j in range(d)]
                total = 0.0
                for b in X:
                    c = [b[j] - rata[j] for j in range(d)]
                    skor = sum(c[j] * arah[j] for j in range(d))
                    total += sum((c[j] - skor * arah[j]) ** 2 for j in range(d))
                return round(total / (n * d) + 0.0, 4)
            """,
        ),
    ],
    [
        M("Membentuk matriks kovariansi pada data berkondisi buruk.", "Pakai SVD dari data terpusat."),
        M("Memusatkan data dua kali saat memakai PCA scikit-learn.", "transform sudah mengurangkan rata-rata."),
        M("Menganggap components_ berisi kolom.", "Komponen ada di baris."),
    ],
    [
        Q("Variansi komponen dari nilai singular?", ["s", "s kuadrat dibagi n-1", "1/s", "s n"], 1, "Variansi adalah s kuadrat dibagi n-1.", hint="Kuadrat."),
        Q("Skor sampel sama dengan?", ["U S", "V", "S", "Vt"], 0, "Sama dengan Xc V.", hint="Proyeksi."),
        Q("Komponen pada components_ berada di?", ["Baris", "Kolom", "Diagonal", "Tidak ada"], 0, "Setiap baris adalah satu komponen.", hint="Beda dengan eigh."),
        Q("Galat rekonstruksi nol bila?", ["k = 1", "Semua komponen dipakai", "Data acak", "Tanpa pusat"], 1, "Tidak ada informasi dibuang.", hint="Rotasi penuh."),
        Q("Proporsi kumulatif dipakai untuk?", ["Memilih jumlah komponen", "Mengurutkan sampel", "Menghapus data", "Menghitung rata-rata"], 0, "Menentukan k.", hint="Ambang."),
    ],
    [
        "PCA dapat dihitung dari SVD data terpusat dengan variansi s kuadrat dibagi n-1.",
        "Proporsi kumulatif membantu memilih jumlah komponen.",
        "PCA scikit-learn menyimpan komponen di baris dan rata-rata di mean_.",
        "Rekonstruksi dari k komponen mengukur informasi yang dibuang.",
    ],
    [],
)

l3 = lesson(
    "A2-07-3",
    "Penerapan: standardisasi, pemilihan komponen, dan batasan",
    35,
    [
        "Memahami mengapa fitur harus distandardisasi sebelum PCA",
        "Memilih jumlah komponen pada data iris",
        "Memproyeksikan data ke dua dimensi untuk visualisasi",
        "Mengenali batasan PCA dan kapan memakainya",
    ],
    [
        T("""
        ## Skala fitur memengaruhi PCA

        PCA mencari variasi terbesar, sehingga fitur dengan satuan besar mendominasi hanya karena angkanya besar. Bila satu kolom dalam meter dan kolom lain dalam milimeter, kolom milimeter punya variansi satu juta kali lebih besar dan komponen pertama praktis hanya menunjuk ke kolom itu. Itu bukan temuan, melainkan artefak satuan.

        Solusinya **standardisasi**: kurangi rata-rata lalu bagi dengan simpangan baku tiap kolom sehingga setiap fitur punya rata-rata nol dan variansi satu. PCA pada data terstandardisasi setara dengan PCA pada **matriks korelasi**. Aturan praktis: bila fitur memiliki satuan atau rentang berbeda, standardisasi hampir selalu dianjurkan. Bila semuanya sudah dalam satuan sama dan perbedaan skala bermakna, misalnya piksel gambar, standardisasi bisa dilewati.
        """),
        C(
            """
            import numpy as np

            X = np.array([[1.0, 1000.0], [2.0, 2000.0], [3.0, 3200.0], [4.0, 4100.0]])
            Xc = X - X.mean(axis=0)
            nilai = np.linalg.eigvalsh(np.cov(X.T))[::-1]
            print((nilai / nilai.sum()).round(6).tolist())

            Z = Xc / X.std(axis=0, ddof=1)
            nilai2 = np.linalg.eigvalsh(np.cov(Z.T))[::-1]
            print((nilai2 / nilai2.sum()).round(4).tolist())
            print(np.allclose(np.cov(Z.T), np.corrcoef(X.T)))
            """,
            """
            [1.0, 0.0]
            [0.9993, 0.0007]
            True
            """,
            """
            Tanpa standardisasi komponen pertama menjelaskan hampir semua variansi hanya karena kolom kedua berskala ribuan. Setelah standardisasi kovariansi sama dengan matriks korelasi.
            """,
            filename="standardisasi.py",
        ),
        T("""
        ## Studi kasus: data iris

        Data iris adalah contoh klasik: seratus lima puluh bunga dengan empat ukuran, panjang dan lebar sepal serta petal, dari tiga spesies. Empat fitur cukup banyak untuk tidak bisa digambar langsung, tetapi PCA dapat mereduksinya ke dua dimensi untuk visualisasi. Fitur-fitur ini berkorelasi kuat, terutama ukuran petal, sehingga dua komponen biasanya sudah menjelaskan hampir semua variansi.

        Pada pelajaran ini kita membandingkan dua skenario: PCA pada data mentah dan PCA pada data terstandardisasi. Hasilnya berbeda karena ukuran petal berskala lebih besar dibanding lebar sepal. Perhatikan proporsi variansi tiap komponen dan berapa komponen yang diperlukan untuk mencapai ambang sembilan puluh lima persen.
        """),
        C(
            """
            import numpy as np
            from sklearn.datasets import load_iris
            from sklearn.decomposition import PCA
            from sklearn.preprocessing import StandardScaler

            X = load_iris().data
            mentah = PCA().fit(X).explained_variance_ratio_
            print(mentah.round(4).tolist())
            Z = StandardScaler().fit_transform(X)
            baku = PCA().fit(Z).explained_variance_ratio_
            print(baku.round(4).tolist())
            kum = np.cumsum(baku)
            print(int(np.searchsorted(kum, 0.95)) + 1)
            """,
            """
            [0.9246, 0.0531, 0.0171, 0.0052]
            [0.7296, 0.2285, 0.0367, 0.0052]
            2
            """,
            """
            Pada data mentah komponen pertama mendominasi karena skala petal. Setelah standardisasi diperlukan dua komponen untuk melewati 95 persen.
            """,
            filename="pilih_komponen.py",
        ),
        K(
            "tip",
            """
            Gunakan `StandardScaler` dan `PCA` dalam satu `Pipeline` agar pemusatan dan penskalaan dipelajari hanya dari data latih. Menghitungnya pada seluruh data sebelum membagi memunculkan kebocoran data.
            """,
            title="Hindari kebocoran data",
        ),
        T("""
        ## Visualisasi dua dimensi

        Penggunaan paling umum PCA adalah visualisasi. Proyeksikan data ke dua komponen pertama lalu buat diagram sebar. Sampel yang mirip akan berdekatan, dan kelompok alami sering tampak jelas walau data aslinya berdimensi tinggi. Pada iris, spesies setosa terpisah rapi dari dua spesies lain, sedangkan versicolor dan virginica sebagian bertumpuk.

        Ingat bahwa sumbu PCA adalah kombinasi linear fitur asli, bukan fitur yang bisa dibaca langsung. Untuk menafsirkannya lihat **loading**, yaitu bobot tiap fitur pada komponen. Fitur dengan loading mutlak besar sangat menentukan komponen itu. Dengan begitu kita bisa memberi nama, misalnya komponen pertama sebagai ukuran bunga secara umum.
        """),
        C(
            """
            import numpy as np
            from sklearn.datasets import load_iris
            from sklearn.decomposition import PCA
            from sklearn.preprocessing import StandardScaler

            data = load_iris()
            Z = StandardScaler().fit_transform(data.data)
            pca = PCA(n_components=2)
            T2 = pca.fit_transform(Z)
            print(T2.shape)
            print(round(abs(float(np.cov(T2.T)[0, 1])), 6))
            y = data.target
            pusat = [T2[y == c].mean(axis=0) for c in range(3)]
            print(round(float(np.linalg.norm(pusat[0] - pusat[1])), 2) > round(float(np.linalg.norm(pusat[1] - pusat[2])), 2))
            print(np.abs(pca.components_[0]).round(4).tolist())
            """,
            """
            (150, 2)
            0.0
            True
            [0.5211, 0.2693, 0.5804, 0.5649]
            """,
            """
            Hasil proyeksi berukuran 150 kali 2 dengan komponen tidak berkorelasi. Pusat setosa lebih jauh dari versicolor dibanding jarak versicolor ke virginica. Loading menunjukkan kontribusi tiap fitur.
            """,
            filename="proyeksi_iris.py",
        ),
        T("""
        ## Batasan PCA

        PCA bersifat linear. Ia hanya menemukan subruang datar, jadi data yang tersusun melengkung seperti spiral atau pita tergulung tidak terwakili dengan baik. Untuk struktur nonlinear ada metode lain seperti kernel PCA, t-SNE, dan UMAP, yang lebih cocok untuk visualisasi tetapi lebih sulit ditafsirkan.

        Batasan lain: PCA peka terhadap pencilan karena variansi dihitung dari kuadrat jarak, tidak menjamin pemisahan kelas, dan hasilnya sulit dijelaskan ketika komponen mencampur banyak fitur. Gunakan PCA sebagai alat eksplorasi dan praproses, ukur manfaatnya lewat validasi, dan jangan menganggap komponen pertama selalu paling penting untuk prediksi.
        """),
        T("""
        ## Praktik baik dalam proyek nyata

        Dalam proyek nyata PCA jarang berdiri sendiri. Urutan umumnya: bersihkan data, tangani nilai hilang, standardisasi, jalankan PCA, lalu pakai komponen untuk model atau visualisasi. Simpan objek scaler dan PCA yang sudah dilatih agar data baru diperlakukan persis sama saat inferensi.

        Dokumentasikan alasan memilih jumlah komponen, misalnya ambang variansi sembilan puluh lima persen, supaya orang lain bisa mereproduksi dan menilainya. Bila model sesudahnya tidak membaik, coba tanpa PCA untuk memastikan reduksi dimensi memang membantu dan bukan hanya menambah kompleksitas.
        """),
        T("""
        ## Dari data ke keputusan

        Misalkan kamu memiliki seratus fitur sensor dari sebuah mesin. Banyak sensor mengukur hal yang mirip sehingga berkorelasi tinggi. PCA dapat menunjukkan bahwa lima komponen sudah menjelaskan hampir semua variansi. Dengan lima fitur itu, pemantauan menjadi lebih mudah, penyimpanan lebih hemat, dan model deteksi anomali lebih cepat dilatih.

        Namun perhatikan juga komponen yang variansinya sangat kecil. Pada deteksi anomali, penyimpangan sering tampak justru pada arah variasi kecil, karena kondisi normal hampir tidak bervariasi di sana. Artinya komponen kecil bisa sangat berguna, dan membuangnya tanpa berpikir bisa menghapus sinyal terpenting.
        """),
        E(
            "A2-07-3-ex1",
            "mudah",
            """
            Tulis fungsi `standardisasi(kolom)` yang mengembalikan z-score tiap elemen list angka memakai simpangan baku sampel (dibagi `n - 1`), dibulatkan 4 desimal. Bila simpangan baku nol kembalikan list nol. Hindari `-0.0`.
            """,
            """
            def standardisasi(kolom):
                # TODO: implementasikan
                pass
            """,
            """
            assert standardisasi([1, 2, 3]) == [-1.0, 0.0, 1.0]
            assert standardisasi([2, 4, 6, 8]) == [-1.1619, -0.3873, 0.3873, 1.1619]
            assert standardisasi([5, 5, 5]) == [0.0, 0.0, 0.0]
            assert standardisasi([0, 10]) == [-0.7071, 0.7071]
            """,
            "Hitung rata-rata dan simpangan baku lalu bagi simpangan tiap elemen.",
            """
            def standardisasi(kolom):
                n = len(kolom)
                rata = sum(kolom) / n
                sd = (sum((x - rata) ** 2 for x in kolom) / (n - 1)) ** 0.5
                if sd == 0:
                    return [0.0] * n
                return [round((x - rata) / sd, 4) + 0.0 for x in kolom]
            """,
        ),
        E(
            "A2-07-3-ex2",
            "mudah",
            """
            Tulis fungsi `jumlah_komponen(rasio, ambang)` yang mengembalikan `k` terkecil sehingga jumlah `k` rasio pertama minimal `ambang`, dengan toleransi 1e-9.
            """,
            """
            def jumlah_komponen(rasio, ambang):
                # TODO: implementasikan
                pass
            """,
            """
            assert jumlah_komponen([0.7296, 0.2285, 0.0367, 0.0052], 0.95) == 2
            assert jumlah_komponen([0.7296, 0.2285, 0.0367, 0.0052], 0.99) == 3
            assert jumlah_komponen([0.5, 0.5], 1.0) == 2
            assert jumlah_komponen([1.0], 0.5) == 1
            """,
            "Akumulasikan rasio dan berhenti saat mencapai ambang.",
            """
            def jumlah_komponen(rasio, ambang):
                berjalan = 0.0
                for i, r in enumerate(rasio, start=1):
                    berjalan += r
                    if berjalan >= ambang - 1e-9:
                        return i
                return len(rasio)
            """,
        ),
        E(
            "A2-07-3-ex3",
            "sedang",
            """
            Tulis fungsi `korelasi_dari_kovariansi(K)` yang mengubah matriks kovariansi (list of list simetris dengan diagonal positif) menjadi matriks korelasi dengan `K[i][j] / sqrt(K[i][i] * K[j][j])`, dibulatkan 4 desimal. Hindari `-0.0`.
            """,
            """
            def korelasi_dari_kovariansi(K):
                # TODO: implementasikan
                pass
            """,
            """
            assert korelasi_dari_kovariansi([[4, 2], [2, 9]]) == [[1.0, 0.3333], [0.3333, 1.0]]
            assert korelasi_dari_kovariansi([[1, 0], [0, 1]]) == [[1.0, 0.0], [0.0, 1.0]]
            assert korelasi_dari_kovariansi([[2, -1], [-1, 2]]) == [[1.0, -0.5], [-0.5, 1.0]]
            assert korelasi_dari_kovariansi([[25]]) == [[1.0]]
            """,
            "Bagi tiap elemen dengan akar hasil kali dua variansi pada diagonal.",
            """
            def korelasi_dari_kovariansi(K):
                n = len(K)
                return [[round(K[i][j] / (K[i][i] * K[j][j]) ** 0.5, 4) + 0.0 for j in range(n)] for i in range(n)]
            """,
        ),
        E(
            "A2-07-3-ex4",
            "menantang",
            """
            Tulis fungsi `skor_pc1(X)` yang menerima data dua fitur (list of list), menghitung komponen utama pertama dari matriks kovariansinya dengan rumus 2x2, dan mengembalikan skor tiap sampel pada komponen itu dibulatkan 4 desimal. Pilih tanda eigenvector sehingga komponen pertamanya tidak negatif. Hindari `-0.0`.
            """,
            """
            def skor_pc1(X):
                # TODO: implementasikan
                pass
            """,
            """
            assert skor_pc1([[1, 2], [2, 4], [3, 6]]) == [-2.2361, 0.0, 2.2361]
            assert skor_pc1([[1, 0], [2, 0], [3, 0]]) == [-1.0, 0.0, 1.0]
            assert skor_pc1([[0, 1], [0, 2], [0, 3]]) == [-1.0, 0.0, 1.0]
            assert skor_pc1([[2, 2], [4, 3], [6, 7], [8, 8]]) == [-4.2329, -2.1643, 2.1643, 4.2329]
            """,
            "Cari eigenvalue terbesar lalu eigenvector (b, lambda minus a). Bila b nol pilih sumbu dengan variansi terbesar.",
            """
            def skor_pc1(X):
                n = len(X)
                mx = sum(b[0] for b in X) / n
                my = sum(b[1] for b in X) / n
                a = sum((b[0] - mx) ** 2 for b in X) / (n - 1)
                d = sum((b[1] - my) ** 2 for b in X) / (n - 1)
                c = sum((b[0] - mx) * (b[1] - my) for b in X) / (n - 1)
                tr = a + d
                det = a * d - c * c
                lam = (tr + max(tr * tr - 4 * det, 0.0) ** 0.5) / 2
                if abs(c) > 1e-12:
                    v = (c, lam - a)
                elif a >= d:
                    v = (1.0, 0.0)
                else:
                    v = (0.0, 1.0)
                norma = (v[0] ** 2 + v[1] ** 2) ** 0.5
                v = (v[0] / norma, v[1] / norma)
                if v[0] < -1e-12 or (abs(v[0]) < 1e-12 and v[1] < 0):
                    v = (-v[0], -v[1])
                return [round((b[0] - mx) * v[0] + (b[1] - my) * v[1], 4) + 0.0 for b in X]
            """,
        ),
    ],
    [
        M("Tidak menstandardisasi fitur berskala berbeda.", "Standardisasi agar tidak ada fitur yang mendominasi."),
        M("Menyesuaikan scaler dan PCA pada seluruh data sebelum membagi.", "Pelajari hanya dari data latih."),
        M("Mengira PCA menemukan struktur nonlinear.", "PCA hanya linear, pakai metode lain untuk lengkungan."),
    ],
    [
        Q("Mengapa standardisasi penting?", ["Agar data lebih kecil", "Agar fitur berskala besar tidak mendominasi", "Agar rata-rata naik", "Agar data acak"], 1, "Skala memengaruhi variansi.", hint="Satuan."),
        Q("PCA pada data terstandardisasi setara dengan PCA pada?", ["Matriks kovariansi mentah", "Matriks korelasi", "Matriks identitas", "Matriks label"], 1, "Variansi satu membuat kovariansi menjadi korelasi.", hint="Skala sama."),
        Q("Loading menyatakan?", ["Jumlah sampel", "Bobot fitur pada komponen", "Rata-rata", "Label"], 1, "Kontribusi fitur ke komponen.", hint="Tafsir."),
        Q("Batasan PCA?", ["Hanya linear", "Hanya data kecil", "Hanya teks", "Tidak butuh data"], 0, "Tidak menangkap lengkungan.", hint="Subruang datar."),
        Q("Cara menghindari kebocoran data?", ["Pipeline hanya dengan data latih", "Menskalakan semua data", "Menghapus label", "Memakai semua komponen"], 0, "Scaler dan PCA dipelajari dari data latih.", hint="Jangan lihat uji."),
    ],
    [
        "Standardisasi mencegah fitur berskala besar mendominasi PCA.",
        "Pilih jumlah komponen dari proporsi variansi kumulatif.",
        "Loading membantu menafsirkan komponen.",
        "PCA linear sehingga perlu metode lain untuk struktur nonlinear.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa perhitungan dan contoh kode yang cukup jelas dalam teks.", "brief": []}

write_module(
    "A2",
    7,
    "PCA dari nol",
    105,
    [
        "Membangun PCA dari kovariansi dan eigen",
        "Menghitung PCA lewat SVD dan merekonstruksi data",
        "Menerapkan PCA dengan standardisasi dan membaca batasannya",
    ],
    [l1, l2, l3],
    video,
    REF,
)
