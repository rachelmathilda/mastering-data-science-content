import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

l1 = lesson(
    "A2-01-1",
    "Vektor dan operasi dasarnya",
    35,
    [
        "Memahami vektor sebagai daftar angka, titik, dan panah",
        "Menjumlahkan vektor dan mengalikannya dengan skalar",
        "Menghitung kombinasi linear dari beberapa vektor",
        "Merepresentasikan data sebagai vektor dengan NumPy",
    ],
    [
        T("""
        ## Apa itu vektor

        **Vektor** adalah daftar angka berurutan. Dalam data science, satu baris data hampir selalu dipandang sebagai vektor: seorang pelanggan dengan umur, penghasilan, dan jumlah belanja adalah vektor tiga komponen `[32, 8.5, 12]`. Jumlah komponen disebut **dimensi** vektor. Vektor dengan dua komponen bisa digambar sebagai titik atau panah di bidang, dan vektor tiga komponen sebagai titik di ruang. Untuk dimensi lebih tinggi kita tidak bisa menggambarnya, tetapi aturan matematikanya tetap sama.

        Ada tiga cara berpikir tentang vektor yang saling melengkapi. Cara pertama adalah daftar angka, cara yang paling dekat dengan kode. Cara kedua adalah titik dalam ruang, berguna untuk memahami jarak dan pengelompokan. Cara ketiga adalah panah dengan panjang dan arah, berguna untuk memahami gerak, gaya, dan gradien.

        Menguasai ketiganya membuatmu mampu pindah antara intuisi geometris dan perhitungan di komputer, kemampuan yang dipakai terus dalam pembelajaran mesin.
        """),
        C(
            """
            import numpy as np

            pelanggan = np.array([32, 8.5, 12])
            print(pelanggan, pelanggan.shape, pelanggan.ndim)
            print(pelanggan[0], pelanggan[-1], pelanggan[1:])
            dua_d = np.array([3, 4])
            print(len(dua_d), dua_d.dtype, pelanggan.dtype)
            print(np.zeros(3), np.ones(2), np.arange(5))
            """,
            """
            [32.   8.5 12. ] (3,) 1
            32.0 12.0 [ 8.5 12. ]
            2 int64 float64
            [0. 0. 0.] [1. 1.] [0 1 2 3 4]
            """,
            """
            Array NumPy satu dimensi merepresentasikan vektor. Atribut `shape` berisi dimensi, dan tipe data otomatis naik ke float bila ada pecahan.
            """,
            filename="vektor_numpy.py",
        ),
        T("""
        ## Penjumlahan dan perkalian skalar

        Menjumlahkan dua vektor berdimensi sama dilakukan komponen demi komponen: `[1, 2] + [3, 4] = [4, 6]`. Secara geometris, kamu menaruh ekor panah kedua di ujung panah pertama, dan hasilnya adalah panah dari awal ke ujung akhir. Pengurangan serupa: `[4, 6] - [3, 4] = [1, 2]`, dan hasilnya adalah panah dari ujung vektor kedua ke ujung vektor pertama.

        **Perkalian skalar** mengalikan setiap komponen dengan satu bilangan: `3 * [1, 2] = [3, 6]`. Skalar positif memperpanjang atau memperpendek panah tanpa mengubah arah, dan skalar negatif membalik arah. Skalar nol menghasilkan vektor nol.

        Hati-hati dengan perbedaan penting antara list Python dan array NumPy. `[1, 2] + [3, 4]` pada list menyambung menjadi `[1, 2, 3, 4]`, sedangkan pada array NumPy menjumlahkan komponen. Inilah salah satu alasan kita memakai NumPy untuk matematika vektor.
        """),
        C(
            """
            import numpy as np

            a = np.array([1, 2])
            b = np.array([3, 4])
            print(a + b, b - a, 3 * a, -a)
            print([1, 2] + [3, 4])
            print(a * b)
            print((2 * a + b).tolist())
            try:
                np.array([1, 2, 3]) + a
            except ValueError:
                print("dimensi tidak cocok")
            """,
            """
            [4 6] [2 2] [3 6] [-1 -2]
            [1, 2, 3, 4]
            [3 8]
            [5, 8]
            dimensi tidak cocok
            """,
            """
            Operasi array dilakukan per komponen. `a * b` pada array adalah perkalian per elemen, bukan dot product. Dimensi berbeda tidak bisa dijumlahkan.
            """,
            filename="operasi_vektor.py",
        ),
        K(
            "warning",
            """
            Operator `*` pada array NumPy adalah perkalian per komponen, bukan dot product. Dot product ditulis `np.dot(a, b)` atau `a @ b` dan akan dibahas di pelajaran ketiga.
            """,
            title="Bintang bukan dot product",
        ),
        T("""
        ## Kombinasi linear

        **Kombinasi linear** adalah penjumlahan beberapa vektor yang masing-masing dikalikan skalar: `c1 * v1 + c2 * v2 + ... + ck * vk`. Ini adalah konsep paling mendasar dalam aljabar linear. Hampir semua yang dilakukan model linear, dari regresi sampai lapisan jaringan saraf, adalah membentuk kombinasi linear dari fitur.

        Contoh: prediksi harga rumah `harga = 50 * luas + 20 * kamar + 5 * umur_balik` adalah kombinasi linear dari vektor fitur dengan bobot `[50, 20, 5]`. Himpunan semua kombinasi linear yang mungkin dari vektor tertentu disebut *span*, yaitu semua titik yang bisa dicapai dengan memvariasikan bobot.

        Dua vektor tidak sejajar di bidang bisa mencapai titik mana pun di bidang itu dengan kombinasi linear yang tepat. Gagasan ini kelak menjadi dasar konsep basis, dimensi, dan peringkat matriks.
        """),
        C(
            """
            import numpy as np

            v1 = np.array([1, 0])
            v2 = np.array([0, 1])
            titik = 3 * v1 + 4 * v2
            print(titik)

            u = np.array([2, 1])
            w = np.array([1, 3])
            print((2 * u - w).tolist(), (0.5 * u + 0.5 * w).tolist())
            fitur = np.array([[100, 3, 10], [60, 2, 5]])
            bobot = np.array([50, 20, 5])
            print((fitur * bobot).sum(axis=1).tolist())
            """,
            """
            [3 4]
            [3, -1] [1.5, 2.0]
            [5110, 3065]
            """,
            """
            `[3, 4]` adalah kombinasi linear dari vektor basis standar. Titik tengah dua vektor adalah kombinasi linear dengan bobot 0.5 dan 0.5. Prediksi linear adalah jumlah fitur berbobot.
            """,
            filename="kombinasi_linear.py",
        ),
        T("""
        ## Data sebagai vektor

        Alasan aljabar linear begitu sentral dalam data science adalah karena data hampir selalu diubah menjadi vektor. Gambar menjadi vektor piksel, teks menjadi vektor hitungan kata atau embedding, dan pelanggan menjadi vektor fitur. Setelah semua menjadi vektor, kita bisa memakai alat yang sama: jarak, kemiripan, proyeksi, dan transformasi.

        Penting untuk memastikan komponen vektor punya makna yang konsisten. Posisi pertama harus selalu berarti hal yang sama pada semua vektor, misalnya umur. Membandingkan vektor yang urutan fiturnya berbeda menghasilkan angka tanpa arti.

        Selain itu, skala komponen penting. Bila satu komponen bernilai jutaan dan komponen lain bernilai satuan, komponen besar akan mendominasi hampir semua perhitungan jarak. Karena itu kita sering menormalkan fitur sebelum memakainya. Topik ini akan muncul lagi saat membahas jarak dan rekayasa fitur.
        """),
        T("""
        ## Vektor dalam kode: list versus array

        Kamu bisa menulis operasi vektor dengan list Python biasa menggunakan comprehension dan `zip`: `[x + y for x, y in zip(a, b)]`. Cara ini jelas dan baik untuk belajar, tetapi lambat untuk data besar. NumPy menyimpan angka dalam blok memori yang rapat dan menjalankan operasi dalam bahasa C, sehingga bisa ratusan kali lebih cepat.

        Dalam latihan di pelajaran ini kamu menulis fungsi dengan list biasa agar konsepnya terlihat jelas. Di dunia nyata kamu akan memakai NumPy. Membandingkan keduanya memperkuat pemahaman karena kamu melihat persis apa yang dilakukan NumPy di balik layar.
        """),
        E(
            "A2-01-1-ex1",
            "mudah",
            """
            Tulis fungsi `tambah(a, b)` yang menjumlahkan dua vektor (list) berdimensi sama dan mengembalikan list baru.
            """,
            """
            def tambah(a, b):
                # TODO: implementasikan
                pass
            """,
            """
            assert tambah([1, 2], [3, 4]) == [4, 6]
            assert tambah([0, 0, 0], [1, 2, 3]) == [1, 2, 3]
            assert tambah([], []) == []
            assert tambah([-1, 1], [1, -1]) == [0, 0]
            """,
            "Gunakan zip dan comprehension.",
            """
            def tambah(a, b):
                return [x + y for x, y in zip(a, b)]
            """,
        ),
        E(
            "A2-01-1-ex2",
            "mudah",
            """
            Tulis fungsi `kali_skalar(c, v)` yang mengalikan setiap komponen vektor `v` dengan skalar `c`.
            """,
            """
            def kali_skalar(c, v):
                # TODO: implementasikan
                pass
            """,
            """
            assert kali_skalar(3, [1, 2]) == [3, 6]
            assert kali_skalar(0, [5, 6]) == [0, 0]
            assert kali_skalar(-1, [1, -2]) == [-1, 2]
            assert kali_skalar(0.5, [2, 4]) == [1.0, 2.0]
            """,
            "Kalikan tiap komponen dalam comprehension.",
            """
            def kali_skalar(c, v):
                return [c * x for x in v]
            """,
        ),
        E(
            "A2-01-1-ex3",
            "sedang",
            """
            Tulis fungsi `kombinasi_linear(bobot, vektor)` yang menerima list bobot dan list vektor (sama banyak) lalu mengembalikan vektor hasil kombinasi linearnya. Semua vektor berdimensi sama dan minimal ada satu vektor.
            """,
            """
            def kombinasi_linear(bobot, vektor):
                # TODO: implementasikan
                pass
            """,
            """
            assert kombinasi_linear([3, 4], [[1, 0], [0, 1]]) == [3, 4]
            assert kombinasi_linear([2, -1], [[2, 1], [1, 3]]) == [3, -1]
            assert kombinasi_linear([1], [[5, 6, 7]]) == [5, 6, 7]
            assert kombinasi_linear([0.5, 0.5], [[2, 1], [1, 3]]) == [1.5, 2.0]
            """,
            "Untuk tiap indeks komponen jumlahkan bobot kali komponen dari tiap vektor.",
            """
            def kombinasi_linear(bobot, vektor):
                dim = len(vektor[0])
                return [sum(b * v[i] for b, v in zip(bobot, vektor)) for i in range(dim)]
            """,
        ),
        E(
            "A2-01-1-ex4",
            "menantang",
            """
            Tulis fungsi `titik_tengah(titik)` yang menerima list vektor berdimensi sama dan mengembalikan vektor rata-rata (sentroid) semua titik. Bila list kosong kembalikan `None`.
            """,
            """
            def titik_tengah(titik):
                # TODO: implementasikan
                pass
            """,
            """
            assert titik_tengah([[0, 0], [2, 4]]) == [1.0, 2.0]
            assert titik_tengah([[1, 2, 3]]) == [1.0, 2.0, 3.0]
            assert titik_tengah([]) is None
            assert titik_tengah([[1, 1], [2, 2], [3, 3]]) == [2.0, 2.0]
            """,
            "Jumlahkan semua vektor lalu bagi dengan banyaknya, atau rata-ratakan per komponen.",
            """
            def titik_tengah(titik):
                if not titik:
                    return None
                n = len(titik)
                dim = len(titik[0])
                return [sum(p[i] for p in titik) / n for i in range(dim)]
            """,
        ),
    ],
    [
        M("Mengira + pada list Python menjumlahkan komponen.", "List menyambung, pakai NumPy atau zip untuk penjumlahan komponen."),
        M("Menjumlahkan vektor berdimensi berbeda.", "Pastikan dimensi sama sebelum operasi."),
        M("Mengira * pada array adalah dot product.", "Pakai np.dot atau @ untuk dot product."),
    ],
    [
        Q("Dimensi vektor [3, 1, 4, 1]?", ["1", "3", "4", "9"], 2, "Dimensi adalah jumlah komponen.", hint="Hitung elemennya."),
        Q("Hasil [1, 2] + [3, 4] pada array NumPy?", ["[1,2,3,4]", "[4,6]", "[3,8]", "error"], 1, "Penjumlahan dilakukan per komponen.", hint="Bukan penyambungan."),
        Q("Apa efek perkalian dengan skalar negatif?", ["Memperpanjang saja", "Membalik arah", "Tidak berubah", "Nol"], 1, "Skalar negatif membalik arah panah.", hint="Panah berbalik."),
        Q("Apa itu kombinasi linear?", ["Perkalian dua vektor", "Jumlah vektor yang dikalikan skalar", "Panjang vektor", "Jarak"], 1, "Jumlah dari vektor-vektor berbobot.", hint="Bobot dikali vektor lalu dijumlahkan."),
        Q("Mengapa NumPy lebih cepat dari list untuk vektor?", ["Pakai C pada blok memori rapat", "Lebih pendek", "Pakai internet", "Tidak lebih cepat"], 0, "Operasi dijalankan di C pada memori yang rapat.", hint="Tidak ada perulangan Python."),
    ],
    [
        "Vektor adalah daftar angka, titik, atau panah dengan dimensi tertentu.",
        "Penjumlahan dan perkalian skalar dilakukan per komponen.",
        "Kombinasi linear adalah dasar prediksi model linear.",
        "Data sering diubah menjadi vektor agar bisa dihitung.",
    ],
    [],
)

l2 = lesson(
    "A2-01-2",
    "Norma dan jarak",
    35,
    [
        "Menghitung norma L1, L2, dan L tak hingga",
        "Menghitung jarak Euclid dan Manhattan antar vektor",
        "Menormalkan vektor menjadi vektor satuan",
        "Memahami pengaruh skala fitur terhadap jarak",
    ],
    [
        T("""
        ## Panjang sebuah vektor

        **Norma** mengukur ukuran atau panjang sebuah vektor. Norma yang paling dikenal adalah norma Euclid atau **norma L2**, yaitu akar dari jumlah kuadrat komponen: `||v||2 = sqrt(v1^2 + v2^2 + ... + vn^2)`. Untuk `[3, 4]` hasilnya `sqrt(9 + 16) = 5`, persis teorema Pythagoras.

        **Norma L1** adalah jumlah nilai mutlak komponen: `||v||1 = |v1| + |v2| + ... + |vn|`. Untuk `[3, -4]` hasilnya 7. Dinamai juga norma Manhattan karena menghitung jarak berjalan di jalan kota berpetak. **Norma L tak hingga** adalah nilai mutlak komponen terbesar: untuk `[3, -4]` hasilnya 4.

        Ketiganya memenuhi sifat norma: tidak negatif, nol hanya untuk vektor nol, `||c v|| = |c| ||v||`, dan ketaksamaan segitiga `||u + v|| <= ||u|| + ||v||`. Dalam pembelajaran mesin, norma muncul sebagai ukuran kesalahan dan sebagai penalti regularisasi.
        """),
        C(
            """
            import numpy as np

            v = np.array([3, -4])
            print(np.linalg.norm(v), np.linalg.norm(v, 1), np.linalg.norm(v, np.inf))
            print(np.sqrt((v ** 2).sum()), np.abs(v).sum(), np.abs(v).max())
            print(np.linalg.norm(2 * v) == 2 * np.linalg.norm(v))
            u = np.array([1, 2])
            w = np.array([4, 6])
            print(np.linalg.norm(u + w) <= np.linalg.norm(u) + np.linalg.norm(w))
            """,
            """
            5.0 7.0 4.0
            5.0 7 4
            True
            True
            """,
            """
            `np.linalg.norm` menghitung norma L2 secara bawaan, dan argumen kedua memilih norma lain. Sifat skala dan ketaksamaan segitiga berlaku.
            """,
            filename="norma.py",
        ),
        T("""
        ## Jarak antar vektor

        Jarak antara dua vektor adalah norma dari selisihnya: `d(u, v) = ||u - v||`. **Jarak Euclid** memakai norma L2 dan merupakan garis lurus antar dua titik. **Jarak Manhattan** memakai norma L1 dan merupakan jumlah selisih mutlak per komponen. **Jarak Chebyshev** memakai norma L tak hingga dan merupakan selisih terbesar pada satu komponen.

        Pilihan jarak memengaruhi hasil algoritma. Euclid cocok bila semua dimensi setara dan kamu peduli pada garis lurus. Manhattan lebih tahan terhadap pencilan karena tidak mengkuadratkan selisih, dan sering dipilih pada data berdimensi tinggi. Algoritma seperti k-nearest neighbors, k-means, dan DBSCAN semuanya bergantung pada jarak.

        Semua fungsi jarak yang baik memenuhi: simetris, tidak negatif, nol hanya bila kedua vektor sama, dan memenuhi ketaksamaan segitiga. Sifat-sifat ini menjamin jarak berperilaku masuk akal.
        """),
        C(
            """
            import numpy as np

            a = np.array([1, 2])
            b = np.array([4, 6])
            print(np.linalg.norm(a - b))
            print(np.abs(a - b).sum())
            print(np.abs(a - b).max())
            titik = np.array([[0, 0], [3, 4], [6, 8]])
            asal = np.array([0, 0])
            print(np.linalg.norm(titik - asal, axis=1).tolist())
            print(np.linalg.norm(a - b) == np.linalg.norm(b - a))
            """,
            """
            5.0
            7
            4
            [0.0, 5.0, 10.0]
            True
            """,
            """
            Jarak adalah norma selisih. Argumen `axis=1` menghitung jarak setiap baris ke titik asal sekaligus.
            """,
            filename="jarak.py",
        ),
        K(
            "tip",
            """
            Untuk menghitung jarak satu titik ke banyak titik sekaligus, kurangkan titik itu dari seluruh matriks lalu pakai `np.linalg.norm(..., axis=1)`. Tidak perlu perulangan.
            """,
            title="Hindari perulangan",
        ),
        T("""
        ## Vektor satuan dan normalisasi

        **Vektor satuan** adalah vektor dengan norma 1. Kamu mengubah vektor tak nol menjadi vektor satuan dengan membaginya dengan normanya: `v / ||v||`. Hasilnya menunjuk arah yang sama tetapi panjangnya satu. Proses ini disebut normalisasi dan berguna saat kamu hanya peduli pada arah, bukan ukuran.

        Contoh: vektor `[3, 4]` menjadi `[0.6, 0.8]`. Vektor nol tidak bisa dinormalkan karena membagi dengan nol, jadi kasus ini perlu ditangani eksplisit. Banyak sistem rekomendasi dan pencarian teks menormalkan vektor sebelum membandingkan, sehingga dokumen panjang tidak otomatis tampak lebih mirip hanya karena kata-katanya lebih banyak.

        Jangan campur aduk dengan normalisasi fitur dalam preprocessing, yang biasanya berarti menskalakan kolom data ke rentang tertentu. Di sini kita menormalkan satu vektor menjadi panjang satu.
        """),
        C(
            """
            import numpy as np

            v = np.array([3.0, 4.0])
            satuan = v / np.linalg.norm(v)
            print(satuan.tolist(), np.linalg.norm(satuan))
            nol = np.array([0.0, 0.0])
            print(np.linalg.norm(nol))
            baris = np.array([[3.0, 4.0], [1.0, 0.0], [0.0, 2.0]])
            norm_baris = baris / np.linalg.norm(baris, axis=1, keepdims=True)
            print(norm_baris.round(2).tolist())
            """,
            """
            [0.6, 0.8] 1.0
            0.0
            [[0.6, 0.8], [1.0, 0.0], [0.0, 1.0]]
            """,
            """
            Membagi dengan norma menghasilkan vektor satuan. `keepdims=True` menjaga bentuk agar pembagian per baris bekerja.
            """,
            filename="vektor_satuan.py",
        ),
        T("""
        ## Skala fitur dan jarak

        Jarak Euclid dihitung dari kuadrat selisih, sehingga fitur berskala besar mendominasi. Bayangkan dua pelanggan dengan fitur umur dan penghasilan dalam rupiah. Selisih umur sepuluh tahun terlihat kecil dibanding selisih penghasilan satu juta rupiah, padahal secara makna keduanya penting. Jarak hampir sepenuhnya ditentukan oleh penghasilan.

        Solusinya adalah menyetarakan skala fitur sebelum menghitung jarak. Dua cara umum: standardisasi (kurangi rata-rata lalu bagi simpangan baku) dan penskalaan min-maks ke rentang nol sampai satu. Setelah itu tiap fitur menyumbang secara sebanding.

        Ini salah satu kesalahan paling umum pada pemula yang memakai k-nearest neighbors atau k-means pada data mentah. Selalu periksa skala fitur sebelum memakai algoritma berbasis jarak.
        """),
        T("""
        ## Memilih norma untuk tujuan tertentu

        Pilihan norma bukan sekadar teknis, melainkan keputusan pemodelan. Dalam regresi, meminimalkan norma L2 dari galat (kuadrat terkecil) menghukum galat besar lebih berat, sehingga sensitif terhadap pencilan. Meminimalkan norma L1 (galat mutlak) lebih tahan pencilan karena setiap galat dihukum sebanding dengan besarnya.

        Pada regularisasi, penalti L2 pada bobot (ridge) mengecilkan semua bobot secara halus, sedangkan penalti L1 (lasso) cenderung mendorong sebagian bobot tepat menjadi nol sehingga menghasilkan model yang jarang. Perbedaan perilaku ini berasal langsung dari bentuk geometris bola satuan tiap norma: bola L2 bulat dan bola L1 berujung runcing pada sumbu.

        Karena itu kamu akan bertemu norma lagi di hampir setiap bab pembelajaran mesin. Menguasai definisinya sekarang membuat konsep-konsep itu terasa familiar.
        """),
        E(
            "A2-01-2-ex1",
            "mudah",
            """
            Tulis fungsi `norma_l2(v)` yang mengembalikan norma Euclid vektor `v` (list) tanpa NumPy. Hasil dibulatkan 6 desimal.
            """,
            """
            def norma_l2(v):
                # TODO: implementasikan
                pass
            """,
            """
            assert norma_l2([3, 4]) == 5.0
            assert norma_l2([0, 0]) == 0.0
            assert norma_l2([1, 1]) == 1.414214
            assert norma_l2([-3, 4]) == 5.0
            """,
            "Akar dari jumlah kuadrat komponen.",
            """
            def norma_l2(v):
                return round(sum(x * x for x in v) ** 0.5, 6)
            """,
        ),
        E(
            "A2-01-2-ex2",
            "mudah",
            """
            Tulis fungsi `jarak_manhattan(a, b)` yang mengembalikan jumlah selisih mutlak per komponen dari dua vektor.
            """,
            """
            def jarak_manhattan(a, b):
                # TODO: implementasikan
                pass
            """,
            """
            assert jarak_manhattan([1, 2], [4, 6]) == 7
            assert jarak_manhattan([0, 0], [0, 0]) == 0
            assert jarak_manhattan([-1, -1], [1, 1]) == 4
            assert jarak_manhattan([5], [2]) == 3
            """,
            "Jumlahkan abs(x - y) untuk tiap pasangan.",
            """
            def jarak_manhattan(a, b):
                return sum(abs(x - y) for x, y in zip(a, b))
            """,
        ),
        E(
            "A2-01-2-ex3",
            "sedang",
            """
            Tulis fungsi `normalkan(v)` yang mengembalikan vektor satuan arah `v` dengan komponen dibulatkan 4 desimal. Untuk vektor nol kembalikan list nol dengan panjang sama.
            """,
            """
            def normalkan(v):
                # TODO: implementasikan
                pass
            """,
            """
            assert normalkan([3, 4]) == [0.6, 0.8]
            assert normalkan([0, 0]) == [0, 0]
            assert normalkan([0, 5]) == [0.0, 1.0]
            assert normalkan([1, 1]) == [0.7071, 0.7071]
            """,
            "Hitung norma, tangani nol, lalu bagi tiap komponen dan bulatkan.",
            """
            def normalkan(v):
                n = sum(x * x for x in v) ** 0.5
                if n == 0:
                    return [0] * len(v)
                return [round(x / n, 4) for x in v]
            """,
        ),
        E(
            "A2-01-2-ex4",
            "menantang",
            """
            Tulis fungsi `terdekat(titik, target)` yang menerima list titik (vektor) dan satu vektor target, lalu mengembalikan indeks titik terdekat menurut jarak Euclid. Bila seri ambil indeks terkecil. List kosong menghasilkan `None`.
            """,
            """
            def terdekat(titik, target):
                # TODO: implementasikan
                pass
            """,
            """
            assert terdekat([[0, 0], [3, 4], [1, 1]], [1, 2]) == 2
            assert terdekat([[5, 5]], [0, 0]) == 0
            assert terdekat([], [1, 1]) is None
            assert terdekat([[2, 0], [0, 2]], [0, 0]) == 0
            """,
            "Bandingkan jumlah kuadrat selisih, tidak perlu akar untuk perbandingan.",
            """
            def terdekat(titik, target):
                if not titik:
                    return None
                def kuadrat_jarak(p):
                    return sum((x - y) ** 2 for x, y in zip(p, target))
                return min(range(len(titik)), key=lambda i: kuadrat_jarak(titik[i]))
            """,
        ),
    ],
    [
        M("Menormalkan vektor nol.", "Periksa norma nol sebelum membagi."),
        M("Memakai jarak Euclid pada fitur berskala berbeda.", "Seragamkan skala fitur lebih dulu."),
        M("Menyamakan normalisasi vektor dengan penskalaan kolom data.", "Normalisasi vektor membuat panjang satu, penskalaan mengubah rentang kolom."),
    ],
    [
        Q("Norma L2 dari [3, 4]?", ["7", "5", "12", "25"], 1, "sqrt(9 + 16) = 5.", hint="Pythagoras."),
        Q("Norma L1 dari [3, -4]?", ["7", "5", "-1", "1"], 0, "|3| + |-4| = 7.", hint="Jumlah nilai mutlak."),
        Q("Jarak Euclid adalah norma dari apa?", ["Jumlah vektor", "Selisih vektor", "Hasil kali", "Rata-rata"], 1, "d(u, v) = ||u - v||.", hint="Kurangkan dulu."),
        Q("Hasil membagi vektor dengan normanya?", ["Vektor nol", "Vektor satuan", "Skalar", "Matriks"], 1, "Vektor satuan berpanjang 1 dengan arah sama.", hint="Panjang menjadi satu."),
        Q("Mengapa skala fitur penting bagi jarak?", ["Tidak penting", "Fitur berskala besar mendominasi", "Jarak jadi negatif", "Hanya untuk grafik"], 1, "Selisih besar mendominasi jumlah kuadrat.", hint="Rupiah versus tahun."),
    ],
    [
        "Norma mengukur panjang vektor, L2 adalah garis lurus dan L1 adalah jumlah mutlak.",
        "Jarak antar vektor adalah norma selisihnya.",
        "Vektor satuan didapat dengan membagi vektor dengan normanya.",
        "Skala fitur memengaruhi jarak sehingga perlu diseragamkan.",
    ],
    [],
)

l3 = lesson(
    "A2-01-3",
    "Dot product, sudut, dan kemiripan",
    35,
    [
        "Menghitung dot product dan menafsirkan artinya",
        "Menghitung sudut antar vektor dan memeriksa ortogonalitas",
        "Menghitung proyeksi satu vektor pada vektor lain",
        "Memakai cosine similarity untuk mengukur kemiripan",
    ],
    [
        T("""
        ## Dot product

        **Dot product** (hasil kali titik) dua vektor berdimensi sama adalah jumlah dari hasil kali komponen yang bersesuaian: `u . v = u1 v1 + u2 v2 + ... + un vn`. Hasilnya satu bilangan, bukan vektor. Untuk `[1, 2, 3] . [4, 5, 6]` hasilnya `4 + 10 + 18 = 32`.

        Dot product muncul di mana-mana. Prediksi model linear adalah dot product antara vektor bobot dan vektor fitur. Setiap neuron pada jaringan saraf menghitung dot product antara masukan dan bobotnya. Dua vektor dengan dot product besar dan positif cenderung menunjuk arah yang mirip, dot product nol berarti tegak lurus, dan negatif berarti berlawanan arah.

        Dot product juga menghubungkan ke norma: `v . v = ||v||^2`. Karena itu norma L2 sebuah vektor adalah akar dari dot product vektor itu dengan dirinya sendiri.
        """),
        C(
            """
            import numpy as np

            u = np.array([1, 2, 3])
            v = np.array([4, 5, 6])
            print(np.dot(u, v), u @ v, (u * v).sum())
            print(u @ u, np.linalg.norm(u) ** 2)
            print(np.array([1, 0]) @ np.array([0, 1]))
            print(np.array([1, 2]) @ np.array([-2, -1]))
            bobot = np.array([0.5, 2.0])
            fitur = np.array([10, 3])
            print(bobot @ fitur)
            """,
            """
            32 32 32
            14 14.0
            0
            -4
            11.0
            """,
            """
            Tiga cara menulis dot product memberi hasil sama. Dot product dengan dirinya sendiri sama dengan kuadrat norma, dan prediksi linear adalah dot product bobot dan fitur.
            """,
            filename="dot_product.py",
        ),
        T("""
        ## Sudut dan ortogonalitas

        Dot product memiliki tafsir geometris: `u . v = ||u|| ||v|| cos(theta)`, dengan theta sudut antar kedua vektor. Dari sini kita mendapat rumus sudut: `cos(theta) = (u . v) / (||u|| ||v||)`. Nilai cosinus berkisar dari -1 untuk arah berlawanan, 0 untuk tegak lurus, sampai 1 untuk arah sama.

        Dua vektor disebut **ortogonal** bila dot product-nya nol, artinya saling tegak lurus. Ortogonalitas adalah konsep yang sangat berguna: vektor ortogonal membawa informasi yang tidak saling tumpang tindih. Basis ortogonal membuat banyak perhitungan jauh lebih sederhana, dan ide ini menjadi inti PCA dan dekomposisi matriks.

        Saat menghitung sudut di komputer, hasil cosinus kadang sedikit melewati 1 karena pembulatan desimal, misalnya 1.0000000002. Potong ke rentang -1 sampai 1 dengan `np.clip` sebelum memanggil `arccos` agar tidak muncul `nan`.
        """),
        C(
            """
            import numpy as np

            def sudut(u, v):
                c = (u @ v) / (np.linalg.norm(u) * np.linalg.norm(v))
                return np.degrees(np.arccos(np.clip(c, -1, 1)))

            print(round(float(sudut(np.array([1, 0]), np.array([0, 1]))), 2))
            print(round(float(sudut(np.array([1, 1]), np.array([1, 0]))), 2))
            print(round(float(sudut(np.array([1, 2]), np.array([2, 4]))), 2))
            print(round(float(sudut(np.array([1, 0]), np.array([-1, 0]))), 2))
            print(np.array([2, 3]) @ np.array([-3, 2]) == 0)
            """,
            """
            90.0
            45.0
            0.0
            180.0
            True
            """,
            """
            Vektor tegak lurus berjarak sudut 90 derajat, searah 0 derajat, dan berlawanan 180 derajat. `np.clip` mencegah galat pembulatan pada `arccos`.
            """,
            filename="sudut_vektor.py",
        ),
        K(
            "warning",
            """
            Sebelum memanggil `np.arccos`, potong nilai cosinus dengan `np.clip(c, -1, 1)`. Galat pembulatan bisa membuat cosinus sedikit melewati 1 dan menghasilkan `nan`.
            """,
            title="Hati-hati arccos",
        ),
        T("""
        ## Proyeksi

        **Proyeksi** vektor `u` pada vektor `v` adalah bayangan `u` di sepanjang arah `v`. Rumusnya `proj_v(u) = ((u . v) / (v . v)) * v`. Hasilnya adalah vektor yang sejajar dengan `v`, dan sisa `u - proj_v(u)` tegak lurus terhadap `v`. Dengan kata lain, proyeksi memecah `u` menjadi bagian searah `v` dan bagian ortogonal.

        Proyeksi adalah fondasi dari regresi kuadrat terkecil, di mana vektor target diproyeksikan ke ruang yang dibentang oleh fitur, dan dari PCA, di mana data diproyeksikan ke arah variansi terbesar. Memahami proyeksi sekarang membuat topik itu terasa wajar nantinya.

        Komponen skalar `(u . v) / ||v||` menyatakan seberapa jauh bayangan itu sepanjang arah `v`. Bila `v` vektor satuan, nilainya sama dengan `u . v` langsung, itulah alasan vektor satuan sering dipakai sebagai sumbu.
        """),
        C(
            """
            import numpy as np

            u = np.array([3.0, 4.0])
            v = np.array([1.0, 0.0])
            proj = (u @ v) / (v @ v) * v
            sisa = u - proj
            print(proj.tolist(), sisa.tolist(), float(proj @ sisa))

            w = np.array([1.0, 1.0])
            p = (u @ w) / (w @ w) * w
            print(p.tolist(), round(float((u - p) @ w), 10))
            """,
            """
            [3.0, 0.0] [0.0, 4.0] 0.0
            [3.5, 3.5] 0.0
            """,
            """
            Proyeksi memecah vektor menjadi bagian searah dan bagian tegak lurus. Sisa selalu ortogonal terhadap arah proyeksi.
            """,
            filename="proyeksi.py",
        ),
        T("""
        ## Cosine similarity

        **Cosine similarity** adalah cosinus sudut antar dua vektor, `(u . v) / (||u|| ||v||)`. Ia mengukur kemiripan arah tanpa terpengaruh panjang. Dua dokumen yang memakai kata dengan proporsi sama tetapi berbeda panjang akan memiliki cosine similarity tinggi, sedangkan jarak Euclid-nya bisa besar.

        Karena sifat ini, cosine similarity dipakai luas pada pencarian teks, sistem rekomendasi, dan embedding. Untuk vektor dengan komponen tidak negatif seperti hitungan kata, nilainya berkisar nol sampai satu. Cosine distance sering didefinisikan sebagai satu dikurangi cosine similarity.

        Bila vektor sudah dinormalkan menjadi panjang satu, cosine similarity sama dengan dot product biasa. Banyak sistem pencarian vektor menormalkan semua vektor di awal agar perhitungannya menjadi dot product yang sangat cepat.
        """),
        C(
            """
            import numpy as np

            def cosine(u, v):
                return float(u @ v / (np.linalg.norm(u) * np.linalg.norm(v)))

            a = np.array([1, 1, 0, 0])
            b = np.array([2, 2, 0, 0])
            c = np.array([0, 0, 1, 1])
            d = np.array([1, 0, 1, 0])
            print(round(cosine(a, b), 4), cosine(a, c), round(cosine(a, d), 4))
            print(round(float(np.linalg.norm(a - b)), 4), round(cosine(a, b), 4))
            dokumen = {"A": a, "C": c, "D": d}
            tertinggi = max(dokumen, key=lambda k: cosine(b, dokumen[k]))
            print(tertinggi)
            """,
            """
            1.0 0.0 0.5
            1.4142 1.0
            A
            """,
            """
            Vektor `b` adalah dua kali `a` sehingga cosine-nya satu walau jaraknya tidak nol. Dokumen dengan cosine tertinggi dianggap paling mirip.
            """,
            filename="cosine_similarity.py",
        ),
        T("""
        ## Rangkuman cara berpikir

        Ringkasnya, tiga operasi inti pada vektor adalah menjumlahkan dengan penskalaan, mengukur dengan norma, dan membandingkan dengan dot product. Hampir semua algoritma pembelajaran mesin dibangun dari kombinasi tiga hal ini. Selalu tanyakan: apakah yang kubutuhkan ukuran, jarak, atau arah? Jawabannya menentukan alat yang dipakai.

        Satu kebiasaan baik untuk menutup: setiap kali menghitung sesuatu dengan vektor, uji dulu pada contoh dua dimensi yang bisa kamu gambar di kertas. Bila hasil kode cocok dengan gambar, barulah percayai kode itu pada dimensi tinggi di mana intuisi visual tidak lagi tersedia.
        """),
        E(
            "A2-01-3-ex1",
            "mudah",
            """
            Tulis fungsi `dot(a, b)` yang mengembalikan dot product dua vektor (list) tanpa NumPy.
            """,
            """
            def dot(a, b):
                # TODO: implementasikan
                pass
            """,
            """
            assert dot([1, 2, 3], [4, 5, 6]) == 32
            assert dot([1, 0], [0, 1]) == 0
            assert dot([], []) == 0
            assert dot([-1, 2], [3, 4]) == 5
            """,
            "Jumlahkan hasil kali pasangan komponen.",
            """
            def dot(a, b):
                return sum(x * y for x, y in zip(a, b))
            """,
        ),
        E(
            "A2-01-3-ex2",
            "mudah",
            """
            Tulis fungsi `ortogonal(a, b)` yang mengembalikan `True` bila dua vektor tegak lurus (dot product nol).
            """,
            """
            def ortogonal(a, b):
                # TODO: implementasikan
                pass
            """,
            """
            assert ortogonal([1, 0], [0, 1]) is True
            assert ortogonal([2, 3], [-3, 2]) is True
            assert ortogonal([1, 1], [1, 1]) is False
            assert ortogonal([0, 0], [5, 7]) is True
            """,
            "Bandingkan dot product dengan nol.",
            """
            def ortogonal(a, b):
                return sum(x * y for x, y in zip(a, b)) == 0
            """,
        ),
        E(
            "A2-01-3-ex3",
            "sedang",
            """
            Tulis fungsi `cosine(a, b)` yang mengembalikan cosine similarity dua vektor dibulatkan 4 desimal. Bila salah satu vektor nol kembalikan 0.0.
            """,
            """
            def cosine(a, b):
                # TODO: implementasikan
                pass
            """,
            """
            assert cosine([1, 1], [2, 2]) == 1.0
            assert cosine([1, 0], [0, 1]) == 0.0
            assert cosine([1, 2], [2, 1]) == 0.8
            assert cosine([0, 0], [1, 1]) == 0.0
            assert cosine([1, 0], [-1, 0]) == -1.0
            """,
            "Hitung dot product dibagi hasil kali norma dan tangani norma nol.",
            """
            def cosine(a, b):
                na = sum(x * x for x in a) ** 0.5
                nb = sum(y * y for y in b) ** 0.5
                if na == 0 or nb == 0:
                    return 0.0
                return round(sum(x * y for x, y in zip(a, b)) / (na * nb), 4)
            """,
        ),
        E(
            "A2-01-3-ex4",
            "menantang",
            """
            Tulis fungsi `proyeksi(u, v)` yang mengembalikan vektor proyeksi `u` pada `v` sebagai list dengan komponen dibulatkan 4 desimal. Bila `v` vektor nol kembalikan list nol dengan panjang sama.
            """,
            """
            def proyeksi(u, v):
                # TODO: implementasikan
                pass
            """,
            """
            assert proyeksi([3, 4], [1, 0]) == [3.0, 0.0]
            assert proyeksi([3, 4], [1, 1]) == [3.5, 3.5]
            assert proyeksi([1, 2], [0, 0]) == [0, 0]
            assert proyeksi([2, 2], [3, 0]) == [2.0, 0.0]
            """,
            "Skalar sama dengan dot(u, v) dibagi dot(v, v), lalu kalikan ke v.",
            """
            def proyeksi(u, v):
                vv = sum(y * y for y in v)
                if vv == 0:
                    return [0] * len(v)
                c = sum(x * y for x, y in zip(u, v)) / vv
                return [round(c * y, 4) for y in v]
            """,
        ),
    ],
    [
        M("Mengira dot product menghasilkan vektor.", "Dot product menghasilkan satu bilangan."),
        M("Lupa memotong cosinus sebelum arccos.", "Pakai np.clip(c, -1, 1)."),
        M("Memakai jarak Euclid untuk kemiripan dokumen berbeda panjang.", "Pakai cosine similarity yang tidak terpengaruh panjang."),
    ],
    [
        Q("Dot product [1,2,3] dan [4,5,6]?", ["15", "32", "21", "[4,10,18]"], 1, "4 + 10 + 18 = 32.", hint="Jumlahkan hasil kali komponen."),
        Q("Apa arti dot product nol?", ["Sama arah", "Berlawanan", "Tegak lurus", "Sama panjang"], 2, "Dot product nol berarti ortogonal.", hint="Sudut 90 derajat."),
        Q("Rentang nilai cosine similarity?", ["0 sampai 1 saja", "-1 sampai 1", "0 sampai tak hingga", "-10 sampai 10"], 1, "Cosinus berkisar dari -1 sampai 1.", hint="Fungsi cosinus."),
        Q("Sisa u dikurangi proyeksinya pada v bersifat?", ["Sejajar v", "Tegak lurus v", "Nol", "Sama dengan u"], 1, "Sisa ortogonal terhadap v.", hint="Memecah menjadi dua bagian."),
        Q("Mengapa cosine cocok untuk dokumen berbeda panjang?", ["Tidak terpengaruh panjang", "Lebih cepat", "Selalu nol", "Memakai kata"], 0, "Ia hanya membandingkan arah.", hint="Dibagi norma."),
    ],
    [
        "Dot product menjumlahkan hasil kali komponen dan menghasilkan satu bilangan.",
        "Sudut dihitung dari dot product dibagi hasil kali norma.",
        "Proyeksi memecah vektor menjadi bagian searah dan tegak lurus.",
        "Cosine similarity mengukur kemiripan arah tanpa terpengaruh panjang.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa perhitungan dan contoh kode yang cukup jelas dalam teks.", "brief": []}

write_module(
    "A2",
    1,
    "Vektor, norma, dan jarak",
    105,
    [
        "Mengoperasikan vektor dengan penjumlahan, skalar, dan kombinasi linear",
        "Menghitung norma dan jarak antar vektor",
        "Memakai dot product, proyeksi, dan cosine similarity",
    ],
    [l1, l2, l3],
    video,
    REF,
)
