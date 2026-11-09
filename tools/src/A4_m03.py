import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

l1 = lesson(
    "A4-03-1",
    "Variabel acak diskrit dan PMF",
    35,
    [
        "Mendefinisikan variabel acak sebagai fungsi dari hasil ke bilangan",
        "Menyusun fungsi massa peluang dari enumerasi dan hitungan",
        "Menghitung peluang rentang dari PMF",
        "Menurunkan distribusi variabel acak hasil transformasi",
    ],
    [
        T("""
        ## Dari hasil ke bilangan

        Hasil percobaan acak sering berupa objek yang sulit dihitung, misalnya urutan kepala dan ekor atau pasangan dadu. Yang biasanya kita pedulikan adalah ringkasan numerik: berapa kepala, berapa jumlah dadu, berapa pelanggan yang datang dalam satu jam. **Variabel acak** adalah fungsi yang memetakan setiap hasil ruang sampel ke sebuah bilangan.

        Dengan variabel acak, kita berpindah dari bahasa himpunan ke bahasa bilangan. Pertanyaan seperti berapa peluang jumlah dadu minimal sepuluh menjadi pertanyaan tentang nilai `X`. Semua alat aljabar dan statistika kemudian bisa dipakai, karena kita berurusan dengan bilangan.
        """),
        T("""
        ## Diskrit dan kontinu

        Variabel acak **diskrit** hanya mengambil nilai yang dapat dihitung, biasanya bilangan bulat: jumlah kepala, jumlah klik, jumlah cacat. Variabel acak **kontinu** mengambil nilai dalam rentang bilangan real, seperti tinggi badan atau waktu tunggu. Modul ini membahas yang diskrit, dan modul berikutnya yang kontinu.

        Perbedaan ini penting karena cara menyatakan peluangnya berbeda. Pada yang diskrit, kita bisa memberi peluang pada tiap nilai. Pada yang kontinu, peluang tiap titik tunggal adalah nol dan kita memakai kepadatan. Memahami yang diskrit lebih dulu membuat konsep kontinu terasa wajar.
        """),
        T("""
        ## Fungsi massa peluang

        **Fungsi massa peluang** atau PMF memberi peluang untuk setiap nilai: `p(x) = P(X = x)`. Ia harus memenuhi dua syarat. Setiap nilai peluang tidak negatif, dan semua peluang berjumlah tepat satu karena pasti terjadi salah satu nilai.

        Cara termudah membangun PMF adalah menghitung berapa hasil yang memetakan ke tiap nilai lalu membaginya dengan ukuran ruang sampel. Di Python, `collections.Counter` melakukan hitungan itu dengan satu baris, sehingga PMF dari enumerasi menjadi pekerjaan yang singkat.
        """),
        C(
            """
            from collections import Counter
            from itertools import product

            hitung = Counter(a + b for a, b in product(range(1, 7), repeat=2))
            pmf = {k: v / 36 for k, v in hitung.items()}
            print(round(pmf[7], 4), round(pmf[2], 4), round(sum(pmf.values()), 4))
            """,
            """
            0.1667 0.0278 1.0
            """,
            """
            Jumlah tujuh punya enam cara dari tiga puluh enam, jumlah dua hanya satu cara, dan seluruh peluang berjumlah satu.
            """,
            filename="pmf_dadu.py",
        ),
        T("""
        ## PMF banyaknya kepala

        Misalkan `X` adalah banyaknya kepala dalam tiga lemparan koin adil. Dari delapan hasil sama mungkin, nol kepala muncul satu kali, satu kepala tiga kali, dua kepala tiga kali, dan tiga kepala satu kali. Maka PMF-nya adalah `1/8, 3/8, 3/8, 1/8`.

        Pola bentuk lonceng kecil ini bukan kebetulan. Ia adalah distribusi binomial yang akan kita bahas rinci nanti. Untuk sekarang, perhatikan bahwa nilai tengah lebih mungkin daripada ekstrem karena ada lebih banyak urutan yang menghasilkan satu atau dua kepala daripada nol atau tiga.
        """),
        C(
            """
            from collections import Counter
            from itertools import product

            hitung = Counter(h.count("H") for h in map("".join, product("HT", repeat=3)))
            pmf = {k: hitung[k] / 8 for k in range(4)}
            print([pmf[k] for k in range(4)])
            print(sum(p for k, p in pmf.items() if k >= 2))
            """,
            """
            [0.125, 0.375, 0.375, 0.125]
            0.5
            """,
            """
            PMF tiga lemparan simetris, dan peluang minimal dua kepala adalah setengah.
            """,
            filename="pmf_koin.py",
        ),
        T("""
        ## Peluang rentang

        Peluang `X` berada dalam himpunan nilai tertentu didapat dengan menjumlahkan PMF atas nilai-nilai itu. Peluang `2 <= X <= 3` adalah `p(2) + p(3)`. Peluang minimal dua kepala adalah `p(2) + p(3) = 0,5`. Tidak ada rumus ajaib: semuanya penjumlahan massa.

        Karena total massa adalah satu, kita juga bisa memakai komplemen: `P(X >= 1) = 1 - p(0)`. Seperti pada modul sebelumnya, memilih antara menjumlahkan langsung dan memakai komplemen bergantung pada mana yang lebih sedikit sukunya.
        """),
        T("""
        ## Fungsi dari variabel acak

        Bila `X` variabel acak dan `f` fungsi, maka `Y = f(X)` juga variabel acak. PMF `Y` didapat dengan mengelompokkan nilai `X` yang menghasilkan `Y` sama lalu menjumlahkan peluangnya. Misalnya `Y = X^2` untuk banyak kepala: nilai 0, 1, 2, 3 menjadi 0, 1, 4, 9 dengan peluang yang sama.

        Bila fungsinya tidak satu-satu, misalnya nilai mutlak, beberapa nilai `X` runtuh ke nilai `Y` yang sama dan peluangnya dijumlahkan. Ini muncul saat kita mentransformasi data, misalnya membuat kategori dari hitungan.
        """),
        C(
            """
            pmf = {0: 0.125, 1: 0.375, 2: 0.375, 3: 0.125}
            y = {}
            for x, p in pmf.items():
                y[x * x] = y.get(x * x, 0) + p
            print(sorted(y.items()))
            """,
            """
            [(0, 0.125), (1, 0.375), (4, 0.375), (9, 0.125)]
            """,
            """
            Karena kuadrat satu-satu pada nilai nol sampai tiga, peluang tiap nilai baru sama dengan peluang nilai lama.
            """,
            filename="transformasi_pmf.py",
        ),
        K(
            "tip",
            """
            Setelah membangun PMF, selalu cek bahwa semua peluang tidak negatif dan jumlahnya satu. Pemeriksaan ini menangkap banyak bug enumerasi.
            """,
            title="Cek jumlah satu",
        ),
        T("""
        ## PMF empiris dari data

        Dalam data nyata kita tidak tahu PMF sebenarnya, tetapi bisa menaksirnya dari frekuensi relatif. Hitung berapa kali tiap nilai muncul lalu bagi dengan jumlah data. Hasilnya PMF empiris yang makin mendekati PMF sebenarnya bila datanya banyak.

        Kebiasaan ini fundamental dalam data science: bandingkan distribusi empiris dengan model teoritis untuk menilai apakah model masuk akal. Simulasi kecil dengan `random` memperlihatkan bagaimana frekuensi relatif mendekati peluang teoritis bila jumlah percobaan membesar.
        """),
        C(
            """
            import random
            from collections import Counter

            random.seed(1)
            data = [sum(random.choice("HT") == "H" for _ in range(3)) for _ in range(20000)]
            frek = Counter(data)[1] / 20000
            print(abs(frek - 0.375) < 0.02)
            """,
            """
            True
            """,
            """
            Frekuensi relatif satu kepala dari dua puluh ribu percobaan sangat dekat dengan peluang teoritis tiga per delapan.
            """,
            filename="pmf_empiris.py",
        ),
        E(
            "A4-03-1-ex1",
            "mudah",
            """
            Tulis fungsi `pmf_dari_hitung(hitung)` yang menerima dict hitungan nilai dan mengembalikan dict PMF dengan peluang dibulatkan 4 desimal.
            """,
            """
            def pmf_dari_hitung(hitung):
                # TODO: implementasikan
                pass
            """,
            """
            assert pmf_dari_hitung({1: 2, 2: 2}) == {1: 0.5, 2: 0.5}
            assert pmf_dari_hitung({0: 1, 1: 3}) == {0: 0.25, 1: 0.75}
            assert pmf_dari_hitung({5: 7}) == {5: 1.0}
            assert pmf_dari_hitung({1: 1, 2: 1, 3: 1}) == {1: 0.3333, 2: 0.3333, 3: 0.3333}
            """,
            "Bagi tiap hitungan dengan jumlah semua hitungan.",
            """
            def pmf_dari_hitung(hitung):
                total = sum(hitung.values())
                return {k: round(v / total, 4) for k, v in hitung.items()}
            """,
        ),
        E(
            "A4-03-1-ex2",
            "sedang",
            """
            Tulis fungsi `pmf_kepala(n)` yang mengembalikan dict PMF banyaknya kepala pada `n` lemparan koin adil dengan kunci `0..n` dan peluang dibulatkan 4 desimal. Gunakan enumerasi dengan itertools.
            """,
            """
            from itertools import product

            def pmf_kepala(n):
                # TODO: implementasikan
                pass
            """,
            """
            assert pmf_kepala(2) == {0: 0.25, 1: 0.5, 2: 0.25}
            assert pmf_kepala(3) == {0: 0.125, 1: 0.375, 2: 0.375, 3: 0.125}
            assert pmf_kepala(0) == {0: 1.0}
            assert pmf_kepala(4)[2] == 0.375
            assert len(pmf_kepala(5)) == 6
            """,
            "Hitung banyak hasil dengan k kepala lalu bagi dengan 2 pangkat n.",
            """
            from itertools import product

            def pmf_kepala(n):
                hitung = {k: 0 for k in range(n + 1)}
                for h in product('HT', repeat=n):
                    hitung[h.count('H')] += 1
                return {k: round(v / 2 ** n, 4) for k, v in hitung.items()}
            """,
        ),
        E(
            "A4-03-1-ex3",
            "sedang",
            """
            Tulis fungsi `peluang_rentang(pmf, a, b)` yang mengembalikan `P(a <= X <= b)` dari dict PMF, dibulatkan 4 desimal.
            """,
            """
            def peluang_rentang(pmf, a, b):
                # TODO: implementasikan
                pass
            """,
            """
            pmf = {0: 0.125, 1: 0.375, 2: 0.375, 3: 0.125}
            assert peluang_rentang(pmf, 1, 2) == 0.75
            assert peluang_rentang(pmf, 2, 3) == 0.5
            assert peluang_rentang(pmf, 4, 9) == 0.0
            assert peluang_rentang(pmf, 0, 3) == 1.0
            """,
            "Jumlahkan peluang nilai yang berada dalam rentang.",
            """
            def peluang_rentang(pmf, a, b):
                return round(sum(p for x, p in pmf.items() if a <= x <= b), 4)
            """,
        ),
        E(
            "A4-03-1-ex4",
            "menantang",
            """
            Tulis fungsi `pmf_transformasi(pmf, f)` yang mengembalikan dict PMF dari `Y = f(X)`, menjumlahkan peluang nilai `X` yang menghasilkan `Y` sama. Bulatkan 4 desimal.
            """,
            """
            def pmf_transformasi(pmf, f):
                # TODO: implementasikan
                pass
            """,
            """
            pmf = {-1: 0.25, 0: 0.5, 1: 0.25}
            assert pmf_transformasi(pmf, abs) == {0: 0.5, 1: 0.5}
            assert pmf_transformasi(pmf, lambda x: x * x) == {0: 0.5, 1: 0.5}
            assert pmf_transformasi(pmf, lambda x: x + 1) == {0: 0.25, 1: 0.5, 2: 0.25}
            assert pmf_transformasi(pmf, lambda x: 0) == {0: 1.0}
            """,
            "Kumpulkan peluang pada kunci f(x) dengan menjumlahkan bila kunci sama.",
            """
            def pmf_transformasi(pmf, f):
                y = {}
                for x, p in pmf.items():
                    y[f(x)] = y.get(f(x), 0) + p
                return {k: round(v, 4) for k, v in y.items()}
            """,
        ),
    ],
    [
        M("Tidak memeriksa bahwa PMF berjumlah satu.", "Selalu cek total dan nilai non-negatif."),
        M("Memakai ukuran ruang sampel yang salah sebagai penyebut.", "Enumerasi pada hasil sama mungkin."),
        M("Lupa menjumlahkan peluang saat transformasi tidak satu-satu.", "Kelompokkan nilai Y yang sama."),
    ],
    [
        Q("Variabel acak adalah?", ["Fungsi dari hasil ke bilangan", "Peluang", "Rata-rata", "Himpunan"], 0, "Memetakan hasil ke angka.", hint="Fungsi."),
        Q("Jumlah seluruh PMF sama dengan?", ["0", "0,5", "1", "Banyak nilai"], 2, "Pasti terjadi salah satu.", hint="Total."),
        Q("PMF dipakai untuk variabel?", ["Diskrit", "Kontinu", "Keduanya sama", "Tidak ada"], 0, "Peluang per nilai.", hint="Hitungan."),
        Q("PMF jumlah kepala tiga koin untuk 1 kepala?", ["1/8", "3/8", "1/2", "1/4"], 1, "Tiga urutan dari delapan.", hint="Tiga cara."),
        Q("Y = |X| bila X simetris, peluang nilai Y?", ["Dijumlahkan", "Dibuang", "Dikali", "Tetap"], 0, "Nilai X berbeda runtuh ke Y sama.", hint="Kelompokkan."),
    ],
    [
        "Variabel acak memetakan hasil ke bilangan.",
        "PMF memberi peluang tiap nilai dan berjumlah satu.",
        "Peluang rentang adalah penjumlahan PMF.",
        "Transformasi mengelompokkan nilai dan menjumlahkan peluangnya.",
    ],
    [],
)

l2 = lesson(
    "A4-03-2",
    "Fungsi distribusi kumulatif dan kuantil",
    35,
    [
        "Menghitung CDF dari PMF diskrit",
        "Memakai CDF untuk peluang interval",
        "Menentukan kuantil dan median variabel diskrit",
        "Menghitung CDF empiris dan peluang waktu tunggu",
    ],
    [
        T("""
        ## Mengapa kumulatif

        PMF menjawab berapa peluang nilai tepat `x`. Seringkali pertanyaan nyata berbunyi berapa peluang nilai paling banyak `x`, misalnya peluang paling banyak dua cacat atau peluang menunggu tidak lebih dari tiga percobaan. Untuk itu kita memakai **fungsi distribusi kumulatif** atau CDF.

        CDF didefinisikan `F(x) = P(X <= x)`. Ia menjumlahkan massa dari nilai terkecil sampai `x`. CDF berlaku untuk variabel diskrit maupun kontinu, sehingga menjadi bahasa umum yang menyatukan keduanya.
        """),
        T("""
        ## Sifat-sifat CDF

        CDF selalu tidak menurun, karena menambah nilai hanya menambah massa. Nilainya mendekati nol di sisi paling kiri dan mendekati satu di sisi paling kanan. Untuk variabel diskrit, CDF berupa fungsi tangga: datar di antara nilai yang mungkin dan melompat naik tepat di tiap nilai yang mungkin, dengan tinggi lompatan sama dengan PMF di titik itu.

        Karena itu PMF dapat dipulihkan dari CDF dengan mengambil selisih: `p(x) = F(x) - F(x-1)` untuk bilangan bulat berurutan. CDF dan PMF membawa informasi yang sama dalam bentuk berbeda.
        """),
        C(
            """
            from itertools import accumulate

            pmf = [0.125, 0.375, 0.375, 0.125]
            cdf = list(accumulate(pmf))
            print(cdf)
            """,
            """
            [0.125, 0.5, 0.875, 1.0]
            """,
            """
            Penjumlahan kumulatif PMF banyak kepala menghasilkan CDF yang naik bertahap dan berakhir di satu.
            """,
            filename="cdf.py",
        ),
        T("""
        ## Peluang interval

        Peluang `X` di antara dua nilai didapat dari selisih CDF: `P(a < X <= b) = F(b) - F(a)`. Perhatikan batas kiri yang eksklusif dan batas kanan yang inklusif. Untuk bilangan bulat, `P(X >= a)` sama dengan `1 - F(a - 1)`.

        Detail inklusif dan eksklusif adalah sumber kesalahan satu-satuan yang umum. Biasakan menulis ulang pertanyaan dalam bentuk `P(X <= b) - P(X <= a - 1)` untuk bilangan bulat dan mengecek dengan kasus kecil.
        """),
        C(
            """
            cdf = [0.125, 0.5, 0.875, 1.0]
            print(round(cdf[2] - cdf[0], 4))
            print(round(1 - cdf[1], 4))
            """,
            """
            0.75
            0.5
            """,
            """
            Peluang satu sampai dua kepala adalah selisih CDF di dua dan nol. Peluang minimal dua kepala adalah satu dikurangi CDF di satu.
            """,
            filename="peluang_interval.py",
        ),
        T("""
        ## Kuantil dan median

        **Kuantil** `q` adalah nilai terkecil `x` sehingga `F(x) >= q`. Median adalah kuantil 0,5, nilai tengah yang separuh massa ada di sisi bawahnya. Kuantil 0,9 adalah nilai yang tidak dilampaui dengan peluang sembilan puluh persen, dan dipakai dalam perencanaan kapasitas serta manajemen risiko.

        Untuk variabel diskrit kita mencari nilai pertama tempat CDF menyentuh atau melampaui `q`. Karena CDF berbentuk tangga, kuantil selalu salah satu nilai yang mungkin, bukan nilai di antara.
        """),
        C(
            """
            nilai = [0, 1, 2, 3]
            cdf = [0.125, 0.5, 0.875, 1.0]

            def kuantil(q):
                for x, f in zip(nilai, cdf):
                    if f >= q:
                        return x

            print(kuantil(0.5), kuantil(0.9), kuantil(0.1))
            """,
            """
            1 3 0
            """,
            """
            Median banyak kepala adalah satu, kuantil sembilan puluh persen adalah tiga, dan kuantil sepuluh persen adalah nol.
            """,
            filename="kuantil.py",
        ),
        T("""
        ## CDF empiris

        Dari data, kita bisa membentuk **CDF empiris**: `F(x)` adalah proporsi data yang kurang dari atau sama dengan `x`. Ia berbentuk tangga yang melompat satu per jumlah data di tiap pengamatan. Tanpa asumsi apa pun tentang bentuk distribusi, CDF empiris adalah penaksir yang baik bagi CDF sebenarnya.

        CDF empiris dipakai luas: membandingkan dua sampel, menguji kecocokan distribusi, dan menghitung persentil data. Persentil ke-90 suatu dataset tidak lain adalah kuantil 0,9 dari CDF empirisnya.
        """),
        C(
            """
            data = [2, 3, 3, 5, 7]

            def ecdf(x):
                return sum(1 for d in data if d <= x) / len(data)

            print(ecdf(3), ecdf(1), ecdf(7), ecdf(4))
            """,
            """
            0.6 0.0 1.0 0.6
            """,
            """
            Tiga dari lima data kurang dari atau sama dengan tiga, tidak ada yang kurang dari satu, semua kurang dari atau sama dengan tujuh, dan empat memberi nilai sama dengan tiga.
            """,
            filename="ecdf.py",
        ),
        K(
            "tip",
            """
            Untuk bilangan bulat, ingat bahwa P(a < X <= b) = F(b) - F(a) dan P(X >= a) = 1 - F(a - 1). Uji dengan contoh kecil agar tidak salah satu-satuan.
            """,
            title="Batas inklusif",
        ),
        T("""
        ## Waktu tunggu dan ekor

        Contoh klasik CDF adalah waktu tunggu sampai sukses pertama. Bila tiap percobaan berhasil dengan peluang `p` secara independen, peluang belum ada sukses setelah `k` percobaan adalah `(1 - p)^k`. Maka CDF-nya `1 - (1 - p)^k`. Untuk dadu, peluang mendapat angka enam dalam tiga lemparan pertama adalah sekitar 0,4213.

        Peluang bahwa kita harus menunggu lebih dari sepuluh lemparan, yaitu ekor distribusinya, adalah `(5/6)^10`, sekitar 0,1615. Mengukur ekor penting untuk perencanaan: seberapa sering kita harus menunggu sangat lama.
        """),
        C(
            """
            print(round(1 - (5 / 6) ** 3, 4), round((5 / 6) ** 10, 4))
            """,
            """
            0.4213 0.1615
            """,
            """
            Sekitar empat puluh dua persen peluang mendapat enam dalam tiga lemparan, dan sekitar enam belas persen peluang menunggu lebih dari sepuluh lemparan.
            """,
            filename="waktu_tunggu.py",
        ),
        T("""
        ## Memakai CDF dalam praktik

        Dalam perencanaan layanan, CDF langsung menjawab pertanyaan kapasitas. Bila CDF jumlah pelanggan per jam di nilai dua puluh adalah 0,95, maka menyiapkan layanan untuk dua puluh pelanggan cukup untuk sembilan puluh lima persen jam. Menaikkan kapasitas ke nilai berikutnya memberi tambahan peluang yang makin kecil, sehingga ada titik impas antara biaya dan risiko.

        Cara berpikir ini sama dengan memilih persentil sebagai target mutu, misalnya latensi persentil ke-99 pada layanan daring. Kuantil membuat target itu terukur dan bisa dibandingkan antar sistem.
        """),
        E(
            "A4-03-2-ex1",
            "mudah",
            """
            Tulis fungsi `cdf_dari_pmf(pmf)` yang menerima dict PMF dan mengembalikan dict CDF dengan nilai kumulatif menurut urutan kunci menaik, dibulatkan 4 desimal.
            """,
            """
            def cdf_dari_pmf(pmf):
                # TODO: implementasikan
                pass
            """,
            """
            assert cdf_dari_pmf({0: 0.125, 1: 0.375, 2: 0.375, 3: 0.125}) == {0: 0.125, 1: 0.5, 2: 0.875, 3: 1.0}
            assert cdf_dari_pmf({1: 1.0}) == {1: 1.0}
            assert cdf_dari_pmf({3: 0.5, 1: 0.5}) == {1: 0.5, 3: 1.0}
            assert cdf_dari_pmf({0: 0.2, 1: 0.3, 2: 0.5}) == {0: 0.2, 1: 0.5, 2: 1.0}
            """,
            "Urutkan kunci lalu jumlahkan peluang secara kumulatif.",
            """
            def cdf_dari_pmf(pmf):
                total = 0.0
                hasil = {}
                for k in sorted(pmf):
                    total += pmf[k]
                    hasil[k] = round(total, 4)
                return hasil
            """,
        ),
        E(
            "A4-03-2-ex2",
            "sedang",
            """
            Tulis fungsi `kuantil_diskrit(pmf, q)` yang mengembalikan nilai terkecil `x` dengan `F(x) >= q`, memakai toleransi `1e-12` pada perbandingan.
            """,
            """
            def kuantil_diskrit(pmf, q):
                # TODO: implementasikan
                pass
            """,
            """
            pmf = {0: 0.125, 1: 0.375, 2: 0.375, 3: 0.125}
            assert kuantil_diskrit(pmf, 0.5) == 1
            assert kuantil_diskrit(pmf, 0.9) == 3
            assert kuantil_diskrit(pmf, 0.1) == 0
            assert kuantil_diskrit(pmf, 1.0) == 3
            assert kuantil_diskrit(pmf, 0.125) == 0
            assert kuantil_diskrit(pmf, 0.126) == 1
            """,
            "Jumlahkan kumulatif menurut urutan nilai dan berhenti saat mencapai q.",
            """
            def kuantil_diskrit(pmf, q):
                total = 0.0
                for k in sorted(pmf):
                    total += pmf[k]
                    if total >= q - 1e-12:
                        return k
            """,
        ),
        E(
            "A4-03-2-ex3",
            "sedang",
            """
            Tulis fungsi `ecdf(data, x)` yang mengembalikan proporsi data yang kurang dari atau sama dengan `x`, dibulatkan 4 desimal.
            """,
            """
            def ecdf(data, x):
                # TODO: implementasikan
                pass
            """,
            """
            d = [2, 3, 3, 5, 7]
            assert ecdf(d, 3) == 0.6
            assert ecdf(d, 1) == 0.0
            assert ecdf(d, 7) == 1.0
            assert ecdf(d, 4) == 0.6
            assert ecdf(d, 10) == 1.0
            """,
            "Hitung data yang kurang dari atau sama dengan x lalu bagi dengan jumlah data.",
            """
            def ecdf(data, x):
                return round(sum(1 for d in data if d <= x) / len(data), 4)
            """,
        ),
        E(
            "A4-03-2-ex4",
            "menantang",
            """
            Tulis fungsi `peluang_hingga(p, k)` yang mengembalikan peluang sukses pertama terjadi dalam `k` percobaan independen pertama dengan peluang sukses `p`, dibulatkan 4 desimal. Untuk `k <= 0` kembalikan 0.0.
            """,
            """
            def peluang_hingga(p, k):
                # TODO: implementasikan
                pass
            """,
            """
            assert peluang_hingga(1 / 6, 3) == 0.4213
            assert peluang_hingga(0.5, 0) == 0.0
            assert peluang_hingga(0.5, 2) == 0.75
            assert peluang_hingga(0.1, 10) == 0.6513
            assert peluang_hingga(0.3, -2) == 0.0
            """,
            "Pakai komplemen dari belum ada sukses setelah k percobaan.",
            """
            def peluang_hingga(p, k):
                if k <= 0:
                    return 0.0
                return round(1 - (1 - p) ** k, 4)
            """,
        ),
    ],
    [
        M("Salah satu-satuan pada batas inklusif.", "P(a < X <= b) = F(b) - F(a)."),
        M("Menganggap kuantil bisa di antara dua nilai diskrit.", "Kuantil diskrit adalah nilai yang mungkin."),
        M("Mengira CDF bisa menurun.", "CDF tidak pernah menurun."),
    ],
    [
        Q("CDF F(x) adalah?", ["P(X = x)", "P(X <= x)", "P(X > x)", "x / n"], 1, "Peluang kumulatif.", hint="Paling banyak."),
        Q("CDF diskrit berbentuk?", ["Garis lurus", "Tangga", "Parabola", "Konstan"], 1, "Melompat di tiap nilai.", hint="Lompat."),
        Q("Median adalah kuantil?", ["0,1", "0,25", "0,5", "1"], 2, "Separuh massa di bawah.", hint="Tengah."),
        Q("P(a < X <= b) sama dengan?", ["F(b) + F(a)", "F(b) - F(a)", "F(a) - F(b)", "F(b)F(a)"], 1, "Selisih CDF.", hint="Selisih."),
        Q("Ekor distribusi menyatakan?", ["P(X > x)", "P(X = x)", "Rata-rata", "Simpangan"], 0, "Peluang melampaui.", hint="Lebih dari."),
    ],
    [
        "CDF menjumlahkan massa sampai x dan tidak pernah menurun.",
        "Peluang interval adalah selisih CDF.",
        "Kuantil diskrit adalah nilai pertama dengan CDF mencapai q.",
        "CDF empiris menaksir CDF dari data.",
    ],
    [],
)

l3 = lesson(
    "A4-03-3",
    "Distribusi gabungan dan marginal",
    35,
    [
        "Membaca dan membangun PMF gabungan dua variabel",
        "Menghitung distribusi marginal dari tabel gabungan",
        "Menghitung PMF bersyarat",
        "Menguji independensi dua variabel acak diskrit",
    ],
    [
        T("""
        ## Dua variabel sekaligus

        Dunia nyata jarang menyangkut satu variabel. Kita ingin tahu hubungan antara jumlah kunjungan dan jumlah pembelian, atau antara kelas pelanggan dan status berhenti. **PMF gabungan** memberi peluang untuk pasangan nilai: `p(x, y) = P(X = x dan Y = y)`. Seluruh peluang dalam tabel berjumlah satu.

        PMF gabungan menyimpan semua informasi tentang dua variabel dan hubungannya. Dari tabel itu kita bisa mengekstrak distribusi masing-masing variabel, distribusi bersyarat, dan ukuran hubungan seperti kovarians yang dibahas nanti.
        """),
        C(
            """
            joint = {(0, 0): 0.1, (0, 1): 0.2, (1, 0): 0.3, (1, 1): 0.4}
            px = {}
            py = {}
            for (x, y), p in joint.items():
                px[x] = px.get(x, 0) + p
                py[y] = py.get(y, 0) + p
            print({k: round(v, 4) for k, v in sorted(px.items())})
            print({k: round(v, 4) for k, v in sorted(py.items())})
            """,
            """
            {0: 0.3, 1: 0.7}
            {0: 0.4, 1: 0.6}
            """,
            """
            Menjumlahkan baris menghasilkan distribusi X dan menjumlahkan kolom menghasilkan distribusi Y.
            """,
            filename="marginal.py",
        ),
        T("""
        ## Distribusi marginal

        Dari tabel gabungan, distribusi satu variabel saja diperoleh dengan menjumlahkan semua nilai variabel lainnya: `p_X(x) = jumlah atas y dari p(x, y)`. Hasilnya disebut distribusi **marginal** karena secara tradisi dijumlahkan di tepi tabel. Ini hukum peluang total yang sama dengan sebelumnya, diterapkan pada tabel.

        Marginal menjawab pertanyaan tentang satu variabel dengan mengabaikan yang lain. Tetapi marginal tidak cukup untuk merekonstruksi gabungan: banyak tabel gabungan berbeda dapat memiliki marginal yang sama, dan perbedaannya terletak pada hubungan antar variabel.
        """),
        T("""
        ## PMF bersyarat

        PMF bersyarat memberi distribusi `Y` bila kita tahu nilai `X`: `p(y | x) = p(x, y) / p_X(x)`. Ini peluang bersyarat dari modul sebelumnya, kini untuk seluruh nilai `Y` sekaligus. Hasilnya distribusi peluang yang valid, berjumlah satu untuk tiap `x`.

        Dalam pembelajaran mesin, memprediksi `Y` dari `X` pada dasarnya mengestimasi `p(y | x)`. Tabel gabungan dibagi menjadi baris-baris, tiap baris dinormalisasi, dan itulah model sederhana yang disebut tabel peluang bersyarat.
        """),
        C(
            """
            joint = {(0, 0): 0.1, (0, 1): 0.2, (1, 0): 0.3, (1, 1): 0.4}
            px1 = joint[(1, 0)] + joint[(1, 1)]
            print(round(joint[(1, 1)] / px1, 4), round(joint[(1, 0)] / px1, 4))
            """,
            """
            0.5714 0.4286
            """,
            """
            Bila X bernilai satu, peluang Y bernilai satu sekitar lima puluh tujuh persen dan Y bernilai nol sekitar empat puluh tiga persen.
            """,
            filename="bersyarat_tabel.py",
        ),
        T("""
        ## Independensi dua variabel

        Dua variabel acak diskrit independen bila `p(x, y) = p_X(x) * p_Y(y)` untuk **semua** pasangan. Cukup satu pasangan yang melanggar untuk membuktikan ketergantungan. Pada tabel di atas, `p(0, 0) = 0,1` sedangkan `p_X(0) * p_Y(0) = 0,3 * 0,4 = 0,12`, sehingga tidak independen.

        Setara dengan itu, `p(y | x)` tidak bergantung pada `x`: semua baris tabel bersyarat identik. Memeriksa kesamaan baris sering lebih mudah dilihat daripada mengalikan marginal.
        """),
        C(
            """
            joint = {(0, 0): 0.1, (0, 1): 0.2, (1, 0): 0.3, (1, 1): 0.4}
            px = {0: 0.3, 1: 0.7}
            py = {0: 0.4, 1: 0.6}
            print(all(abs(joint[(x, y)] - px[x] * py[y]) < 1e-9 for x in px for y in py))

            ind = {(x, y): px[x] * py[y] for x in px for y in py}
            print(all(abs(ind[(x, y)] - px[x] * py[y]) < 1e-9 for x in px for y in py))
            """,
            """
            False
            True
            """,
            """
            Tabel pertama tidak independen. Tabel yang dibangun dari hasil kali marginal tentu independen.
            """,
            filename="uji_independen.py",
        ),
        K(
            "warn",
            """
            Marginal yang sama tidak menjamin gabungan yang sama. Dua tabel dapat memiliki marginal identik tetapi hubungan antar variabel yang sangat berbeda.
            """,
            title="Marginal tidak cukup",
        ),
        T("""
        ## Contoh dua dadu

        Misalkan `X` adalah dadu pertama dan `Y` adalah nilai maksimum kedua dadu. Keduanya jelas tidak independen: bila `X = 6` maka `Y` pasti 6. Dari enumerasi 36 hasil kita dapat menghitung bahwa `P(Y = 6) = 11/36`, sekitar 0,3056, tetapi `P(Y = 6 | X = 3) = 1/6`, sekitar 0,1667.

        Perbedaan antara peluang marginal dan bersyarat adalah bukti langsung ketergantungan. Pengetahuan tentang `X` mengubah keyakinan kita tentang `Y`, dan itulah yang dipelajari model prediktif dari data.
        """),
        C(
            """
            from itertools import product

            S = list(product(range(1, 7), repeat=2))
            y6 = sum(1 for a, b in S if max(a, b) == 6) / 36
            x3 = [h for h in S if h[0] == 3]
            y6_x3 = sum(1 for a, b in x3 if max(a, b) == 6) / len(x3)
            print(round(y6, 4), round(y6_x3, 4))
            """,
            """
            0.3056 0.1667
            """,
            """
            Peluang maksimum enam secara umum lebih besar daripada peluangnya bila dadu pertama diketahui tiga, sehingga kedua variabel bergantung.
            """,
            filename="dadu_maks.py",
        ),
        T("""
        ## Dari tabel ke model

        Seluruh bahasan ini adalah fondasi model prediktif. Memodelkan hubungan antara fitur dan label berarti menaksir distribusi gabungan atau bersyarat dari data. Naive Bayes menaksir `p(fitur | kelas)` dengan asumsi independen bersyarat, regresi logistik menaksir `p(kelas | fitur)` langsung.

        Menguasai tabel gabungan, marginal, dan bersyarat membuat berbagai model terasa seperti variasi dari ide yang sama. Latihan berikut membuatmu menghitung ketiganya dari tabel dan menguji independensi.
        """),
        T("""
        ## Membangun tabel gabungan dari data

        Dalam praktik kamu jarang diberi tabel gabungan jadi. Biasanya kamu punya daftar pengamatan berpasangan, misalnya jumlah kunjungan dan apakah pelanggan membeli. Hitung berapa kali tiap pasangan muncul, bagi dengan jumlah total, dan hasilnya adalah PMF gabungan empiris.

        Dengan pandas, `pd.crosstab` melakukan hitungan itu dan opsi normalisasi menghasilkan peluang gabungan, baris, atau kolom. Memahami apa yang dihitung di balik fungsi itu membuat kamu tahu persis penyebut mana yang dipakai, sumber kebingungan yang sangat umum.
        """),
        T("""
        ## Tiga tabel dari satu data

        Satu tabel hitungan dapat dinormalisasi tiga cara. Dibagi total keseluruhan menghasilkan peluang gabungan. Dibagi total tiap baris menghasilkan peluang kolom bersyarat pada baris. Dibagi total tiap kolom menghasilkan peluang baris bersyarat pada kolom. Ketiganya menjawab pertanyaan berbeda, dan memilih yang salah adalah kesalahan interpretasi paling sering pada laporan tabel silang.

        Selalu tulis kalimat pertanyaannya dulu, misalnya di antara pelanggan yang menerima promo berapa persen yang berhenti, lalu pilih normalisasi yang cocok.
        """),
        E(
            "A4-03-3-ex1",
            "mudah",
            """
            Tulis fungsi `marginal(joint, sumbu)` yang menerima dict PMF gabungan berkunci tuple `(x, y)` dan mengembalikan dict marginal. Bila `sumbu` bernilai 0 kembalikan marginal `X`, bila 1 marginal `Y`. Bulatkan 4 desimal.
            """,
            """
            def marginal(joint, sumbu):
                # TODO: implementasikan
                pass
            """,
            """
            j = {(0, 0): 0.1, (0, 1): 0.2, (1, 0): 0.3, (1, 1): 0.4}
            assert marginal(j, 0) == {0: 0.3, 1: 0.7}
            assert marginal(j, 1) == {0: 0.4, 1: 0.6}
            assert marginal({(0, 0): 1.0}, 0) == {0: 1.0}
            assert marginal({(1, 'a'): 0.5, (2, 'a'): 0.5}, 1) == {'a': 1.0}
            """,
            "Jumlahkan peluang semua pasangan yang memiliki nilai sama pada sumbu yang dipilih.",
            """
            def marginal(joint, sumbu):
                hasil = {}
                for kunci, p in joint.items():
                    hasil[kunci[sumbu]] = hasil.get(kunci[sumbu], 0) + p
                return {k: round(v, 4) for k, v in hasil.items()}
            """,
        ),
        E(
            "A4-03-3-ex2",
            "sedang",
            """
            Tulis fungsi `bersyarat(joint, x, y)` yang mengembalikan `P(Y = y | X = x)` dari PMF gabungan berkunci tuple, dibulatkan 4 desimal. Kembalikan 0.0 bila pasangan tidak ada.
            """,
            """
            def bersyarat(joint, x, y):
                # TODO: implementasikan
                pass
            """,
            """
            j = {(0, 0): 0.1, (0, 1): 0.2, (1, 0): 0.3, (1, 1): 0.4}
            assert bersyarat(j, 1, 1) == 0.5714
            assert bersyarat(j, 0, 0) == 0.3333
            assert bersyarat(j, 1, 0) == 0.4286
            assert bersyarat(j, 0, 1) == 0.6667
            assert bersyarat({(0, 0): 1.0}, 0, 5) == 0.0
            """,
            "Bagi peluang pasangan dengan marginal X pada nilai x.",
            """
            def bersyarat(joint, x, y):
                px = sum(p for (a, b), p in joint.items() if a == x)
                return round(joint.get((x, y), 0) / px, 4)
            """,
        ),
        E(
            "A4-03-3-ex3",
            "sedang",
            """
            Tulis fungsi `peluang_kejadian_gabungan(joint, syarat)` yang menjumlahkan peluang semua pasangan `(x, y)` yang memenuhi `syarat(x, y)` dan mengembalikannya dibulatkan 4 desimal.
            """,
            """
            def peluang_kejadian_gabungan(joint, syarat):
                # TODO: implementasikan
                pass
            """,
            """
            j = {(0, 0): 0.1, (0, 1): 0.2, (1, 0): 0.3, (1, 1): 0.4}
            assert peluang_kejadian_gabungan(j, lambda x, y: x == y) == 0.5
            assert peluang_kejadian_gabungan(j, lambda x, y: x + y >= 1) == 0.9
            assert peluang_kejadian_gabungan(j, lambda x, y: x > y) == 0.3
            assert peluang_kejadian_gabungan(j, lambda x, y: False) == 0.0
            """,
            "Jumlahkan peluang pasangan yang lolos syarat.",
            """
            def peluang_kejadian_gabungan(joint, syarat):
                return round(sum(p for (x, y), p in joint.items() if syarat(x, y)), 4)
            """,
        ),
        E(
            "A4-03-3-ex4",
            "menantang",
            """
            Tulis fungsi `apakah_independen_joint(joint)` yang mengembalikan True bila `p(x, y) = p_X(x) * p_Y(y)` untuk semua pasangan nilai `x` dan `y` yang muncul (pasangan yang tidak ada dalam dict dianggap peluang 0), dengan toleransi `1e-9`.
            """,
            """
            def apakah_independen_joint(joint):
                # TODO: implementasikan
                pass
            """,
            """
            j = {(0, 0): 0.1, (0, 1): 0.2, (1, 0): 0.3, (1, 1): 0.4}
            assert apakah_independen_joint(j) is False
            assert apakah_independen_joint({(0, 0): 0.12, (0, 1): 0.18, (1, 0): 0.28, (1, 1): 0.42}) is True
            assert apakah_independen_joint({(0, 0): 0.25, (0, 1): 0.25, (1, 0): 0.25, (1, 1): 0.25}) is True
            assert apakah_independen_joint({(0, 0): 0.5, (1, 1): 0.5}) is False
            """,
            "Hitung marginal lalu bandingkan setiap sel termasuk yang tidak tercatat.",
            """
            def apakah_independen_joint(joint):
                px = {}
                py = {}
                for (x, y), p in joint.items():
                    px[x] = px.get(x, 0) + p
                    py[y] = py.get(y, 0) + p
                return all(abs(joint.get((x, y), 0) - px[x] * py[y]) < 1e-9 for x in px for y in py)
            """,
        ),
    ],
    [
        M("Mengira marginal cukup untuk merekonstruksi gabungan.", "Marginal tidak memuat hubungan."),
        M("Menguji independensi hanya pada satu pasangan.", "Harus semua pasangan, satu pelanggaran cukup untuk menolak."),
        M("Lupa pasangan yang tidak tercatat bernilai nol.", "Anggap peluangnya nol."),
    ],
    [
        Q("PMF gabungan p(x,y) adalah?", ["P(X=x atau Y=y)", "P(X=x dan Y=y)", "P(X=x)+P(Y=y)", "P(Y=y | X=x)"], 1, "Pasangan nilai.", hint="Dan."),
        Q("Marginal X diperoleh dengan?", ["Menjumlahkan atas y", "Mengalikan", "Membagi", "Mengurangi"], 0, "Peluang total.", hint="Jumlahkan."),
        Q("p(y|x) dihitung?", ["p(x,y)/p_X(x)", "p(x,y)/p_Y(y)", "p_X p_Y", "p(x,y)+p_X"], 0, "Normalisasi baris.", hint="Bagi marginal X."),
        Q("Independen bila p(x,y) sama dengan?", ["p_X(x) p_Y(y)", "p_X(x)+p_Y(y)", "1", "0"], 0, "Untuk semua pasangan.", hint="Hasil kali."),
        Q("Marginal sama berarti gabungan sama?", ["Ya", "Tidak selalu", "Selalu", "Hanya diskrit"], 1, "Hubungan bisa berbeda.", hint="Tidak cukup."),
    ],
    [
        "PMF gabungan memberi peluang pasangan nilai.",
        "Marginal didapat dengan menjumlahkan variabel lain.",
        "PMF bersyarat menormalisasi baris tabel.",
        "Independen berarti gabungan sama dengan hasil kali marginal di semua sel.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perhitungan yang cukup jelas dalam teks.", "brief": []}

write_module(
    "A4",
    3,
    "Variabel acak diskrit",
    105,
    [
        "Menyusun dan memakai PMF",
        "Memakai CDF dan kuantil",
        "Menghitung marginal dan bersyarat dari tabel gabungan",
    ],
    [l1, l2, l3],
    video,
    REF,
)
