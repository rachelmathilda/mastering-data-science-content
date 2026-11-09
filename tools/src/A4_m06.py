import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

l1 = lesson(
    "A4-06-1",
    "Ekspektasi atau nilai harapan",
    35,
    [
        "Menghitung ekspektasi variabel diskrit dan kontinu",
        "Memakai ekspektasi fungsi variabel acak",
        "Memakai linearitas ekspektasi",
        "Menerapkan nilai harapan pada keputusan bertaruh",
    ],
    [
        T("""
        ## Rata-rata jangka panjang

        Distribusi lengkap memuat banyak informasi, tetapi sering kita butuh satu angka ringkasan. Yang paling dasar adalah **ekspektasi** atau nilai harapan: rata-rata berbobot dari semua nilai yang mungkin, dengan bobot berupa peluangnya. Untuk variabel diskrit, `E[X] = jumlah x * p(x)`.

        Tafsirnya adalah rata-rata jangka panjang. Bila percobaan diulang sangat banyak kali, rata-rata hasilnya mendekati `E[X]`. Itu bukan nilai yang pasti muncul: ekspektasi satu dadu adalah `3,5`, padahal dadu tidak pernah menunjukkan 3,5. Ia adalah titik keseimbangan massa distribusi.
        """),
        C(
            """
            nilai = range(1, 7)
            e = sum(k * (1 / 6) for k in nilai)
            print(round(e, 4))
            """,
            """
            3.5
            """,
            """
            Rata-rata berbobot enam sisi dadu adalah tiga koma lima.
            """,
            filename="ekspektasi_dadu.py",
        ),
        T("""
        ## Ekspektasi fungsi

        Sering kita butuh ekspektasi suatu fungsi dari variabel acak, misalnya `X^2`. Kita tidak perlu mencari distribusi baru. Cukup hitung `E[g(X)] = jumlah g(x) * p(x)` memakai PMF aslinya. Aturan ini kadang disebut hukum ahli statistik tak sadar karena orang memakainya tanpa menyadari bahwa itu teorema.

        Perhatikan bahwa `E[g(X)]` umumnya tidak sama dengan `g(E[X])`. Untuk dadu, `E[X^2] = 91/6`, sekitar 15,17, sedangkan `E[X]^2 = 12,25`. Selisihnya adalah varians, topik pelajaran berikutnya.
        """),
        C(
            """
            pmf = {k: 1 / 6 for k in range(1, 7)}
            e1 = sum(k * p for k, p in pmf.items())
            e2 = sum(k * k * p for k, p in pmf.items())
            print(round(e2, 4), round(e1 ** 2, 4))
            """,
            """
            15.1667 12.25
            """,
            """
            Rata-rata kuadrat lebih besar daripada kuadrat rata-rata, dan selisih keduanya adalah varians.
            """,
            filename="lotus.py",
        ),
        T("""
        ## Linearitas

        Sifat paling berguna ekspektasi adalah **linearitas**: `E[aX + b] = a E[X] + b` dan `E[X + Y] = E[X] + E[Y]`. Yang luar biasa, aturan jumlah berlaku **tanpa** syarat independen. Ekspektasi jumlah dua variabel selalu jumlah ekspektasinya, seberapa pun kedua variabel itu berhubungan.

        Linearitas menyederhanakan banyak hitungan. Rata-rata jumlah dua dadu adalah `3,5 + 3,5 = 7` tanpa perlu menghitung tiga puluh enam hasil. Rata-rata binomial adalah `n p` karena jumlah `n` Bernoulli, masing-masing berekspektasi `p`.
        """),
        C(
            """
            from itertools import product

            S = list(product(range(1, 7), repeat=2))
            e_jumlah = sum(a + b for a, b in S) / 36
            e_ax = sum(2 * a + 1 for a, b in S) / 36
            print(round(e_jumlah, 4), round(e_ax, 4))
            """,
            """
            7.0 8.0
            """,
            """
            Jumlah dua dadu berekspektasi tujuh dan dua kali dadu pertama ditambah satu berekspektasi delapan, sesuai linearitas.
            """,
            filename="linearitas.py",
        ),
        T("""
        ## Ekspektasi kontinu

        Untuk variabel kontinu, penjumlahan menjadi integral: `E[X] = integral x * f(x) dx`. Idenya sama, rata-rata berbobot dengan kepadatan sebagai bobot. Pada eksponensial berlaju `0,5`, ekspektasinya `1/0,5 = 2`, sesuai pembahasan sebelumnya tentang waktu tunggu.

        Kita bisa menghitung integral ini secara numerik dengan aturan titik tengah. Cukup potong rentang menjadi banyak bagian kecil dan jumlahkan `x * f(x) * lebar`. Rentang atas harus cukup jauh agar sisa ekor tidak berarti.
        """),
        C(
            """
            import math

            lam = 0.5
            n = 60000
            h = 60 / n
            e = sum((i + 0.5) * h * lam * math.exp(-lam * (i + 0.5) * h) for i in range(n)) * h
            print(round(e, 3))
            """,
            """
            2.0
            """,
            """
            Integral numerik x dikali kepadatan eksponensial memberi nilai dua, yaitu satu per laju.
            """,
            filename="ekspektasi_kontinu.py",
        ),
        T("""
        ## Keputusan dengan nilai harapan

        Ekspektasi adalah dasar penilaian keputusan di bawah ketidakpastian. Tiket undian seharga sepuluh ribu dengan peluang 0,5 persen menang seribu ribu memiliki hadiah harapan lima ribu. Setelah dikurangi harga tiket, nilai harapan bersih adalah minus lima ribu per tiket. Dalam jangka panjang pembeli rugi rata-rata separuh harga tiket.

        Namun ekspektasi bukan satu-satunya pertimbangan. Orang menolak taruhan berisiko tinggi walau ekspektasinya positif, dan varians serta kerugian maksimum juga penting. Ekspektasi menjawab berapa untungnya rata-rata, bukan seberapa nyaman prosesnya.
        """),
        C(
            """
            hadiah = 1000 * 0.005
            print(round(hadiah, 4), hadiah - 10)
            """,
            """
            5.0 -5.0
            """,
            """
            Hadiah harapan lima dikurangi harga sepuluh memberi nilai harapan bersih negatif lima.
            """,
            filename="taruhan.py",
        ),
        K(
            "warn",
            """
            E[g(X)] tidak sama dengan g(E[X]) kecuali g linear. Menghitung fungsi dari rata-rata bukan rata-rata dari fungsi.
            """,
            title="Fungsi dan rata-rata",
        ),
        T("""
        ## Ekspektasi dalam model

        Hampir setiap fungsi kerugian dalam machine learning adalah ekspektasi. Galat kuadrat rata-rata adalah `E[(y - prediksi)^2]`. Pelatihan berusaha meminimalkan ekspektasi kerugian atas distribusi data, yang di praktik didekati dengan rata-rata atas sampel latih. Gagasan bahwa rata-rata sampel menaksir ekspektasi inilah yang diformalkan oleh hukum bilangan besar di akhir modul.

        Karena itu terbiasa menghitung dan menafsirkan ekspektasi, dari distribusi tabel maupun dari integral, akan membantu memahami hampir seluruh algoritma yang kamu temui nanti.
        """),
        T("""
        ## Median dan modus sebagai pembanding

        Ekspektasi bukan satu-satunya ukuran pusat. Median adalah nilai tengah yang membagi massa menjadi dua bagian sama, dan modus adalah nilai paling mungkin. Pada distribusi simetris ketiganya berimpit, tetapi pada distribusi miring mereka berpisah. Pendapatan, misalnya, miring ke kanan: sedikit orang berpenghasilan sangat besar menarik rata-rata jauh di atas median.

        Karena itu laporan yang jujur menyebut ekspektasi bersama median untuk data miring. Ekspektasi peka terhadap nilai ekstrem sedangkan median kokoh, dan perbedaan keduanya sendiri merupakan informasi tentang bentuk distribusi.
        """),
        T("""
        ## Hukum bilangan besar sekilas

        Mengapa rata-rata sampel menaksir ekspektasi? Karena rata-rata `n` pengamatan independen memiliki ekspektasi yang sama dengan ekspektasi satu pengamatan, dan variansnya mengecil menjadi `sigma^2 / n`. Makin banyak data, makin sempit sebaran rata-rata di sekitar nilai sebenarnya. Pelajaran terakhir modul ini mengulas hukum bilangan besar secara resmi dan memperlihatkannya lewat simulasi.
        """),
        E(
            "A4-06-1-ex1",
            "mudah",
            """
            Tulis fungsi `ekspektasi(pmf)` yang menerima dict PMF dan mengembalikan nilai harapan dibulatkan 4 desimal.
            """,
            """
            def ekspektasi(pmf):
                # TODO: implementasikan
                pass
            """,
            """
            assert ekspektasi({1: 0.5, 2: 0.5}) == 1.5
            assert ekspektasi({k: 1 / 6 for k in range(1, 7)}) == 3.5
            assert ekspektasi({5: 1.0}) == 5.0
            assert ekspektasi({0: 0.7, 10: 0.3}) == 3.0
            """,
            "Jumlahkan nilai kali peluangnya.",
            """
            def ekspektasi(pmf):
                return round(sum(x * p for x, p in pmf.items()), 4)
            """,
        ),
        E(
            "A4-06-1-ex2",
            "sedang",
            """
            Tulis fungsi `ekspektasi_fungsi(pmf, g)` yang mengembalikan `E[g(X)]` dibulatkan 4 desimal.
            """,
            """
            def ekspektasi_fungsi(pmf, g):
                # TODO: implementasikan
                pass
            """,
            """
            assert ekspektasi_fungsi({1: 0.5, 2: 0.5}, lambda x: x * x) == 2.5
            assert ekspektasi_fungsi({k: 1 / 6 for k in range(1, 7)}, lambda x: x * x) == 15.1667
            assert ekspektasi_fungsi({-1: 0.5, 1: 0.5}, abs) == 1.0
            assert ekspektasi_fungsi({0: 0.7, 10: 0.3}, lambda x: 2 * x + 1) == 7.0
            """,
            "Terapkan g pada tiap nilai lalu bobot dengan peluang.",
            """
            def ekspektasi_fungsi(pmf, g):
                return round(sum(g(x) * p for x, p in pmf.items()), 4)
            """,
        ),
        E(
            "A4-06-1-ex3",
            "sedang",
            """
            Tulis fungsi `nilai_harapan_taruhan(biaya, hadiah_pmf)` yang mengembalikan keuntungan bersih harapan, yaitu ekspektasi hadiah dikurangi `biaya`, dibulatkan 4 desimal. Hindari `-0.0`.
            """,
            """
            def nilai_harapan_taruhan(biaya, hadiah_pmf):
                # TODO: implementasikan
                pass
            """,
            """
            assert nilai_harapan_taruhan(10, {0: 0.995, 1000: 0.005}) == -5.0
            assert nilai_harapan_taruhan(5, {0: 0.5, 10: 0.5}) == 0.0
            assert nilai_harapan_taruhan(1, {2: 1.0}) == 1.0
            assert nilai_harapan_taruhan(0, {0: 1.0}) == 0.0
            """,
            "Hitung ekspektasi hadiah lalu kurangi biaya.",
            """
            def nilai_harapan_taruhan(biaya, hadiah_pmf):
                return round(sum(x * p for x, p in hadiah_pmf.items()) - biaya, 4) + 0.0
            """,
        ),
        E(
            "A4-06-1-ex4",
            "menantang",
            """
            Tulis fungsi `ekspektasi_kontinu(f, a, b, n=100000)` yang menghitung `E[X]` untuk PDF `f` pada `[a, b]` dengan aturan titik tengah, dibulatkan 4 desimal.
            """,
            """
            import math

            def ekspektasi_kontinu(f, a, b, n=100000):
                # TODO: implementasikan
                pass
            """,
            """
            import math
            assert ekspektasi_kontinu(lambda x: 2 * x, 0, 1) == 0.6667
            assert ekspektasi_kontinu(lambda x: 0.1, 0, 10) == 5.0
            assert ekspektasi_kontinu(lambda x: 0.5 * math.exp(-0.5 * x), 0, 60) == 2.0
            assert ekspektasi_kontinu(lambda x: 3 * x * x, 0, 1) == 0.75
            """,
            "Jumlahkan x kali f(x) kali lebar potongan di titik tengah tiap potongan.",
            """
            import math

            def ekspektasi_kontinu(f, a, b, n=100000):
                h = (b - a) / n
                total = 0.0
                for i in range(n):
                    x = a + (i + 0.5) * h
                    total += x * f(x)
                return round(total * h, 4)
            """,
        ),
    ],
    [
        M("Menyamakan E[g(X)] dengan g(E[X]).", "Itu hanya berlaku untuk g linear."),
        M("Mengira ekspektasi jumlah butuh independensi.", "Linearitas berlaku tanpa syarat."),
        M("Menganggap ekspektasi adalah nilai yang pasti muncul.", "Ia rata-rata jangka panjang."),
    ],
    [
        Q("Ekspektasi diskrit?", ["jumlah x p(x)", "jumlah p(x)", "max x", "median"], 0, "Rata-rata berbobot.", hint="Nilai kali peluang."),
        Q("E[dadu] sama dengan?", ["3", "3,5", "4", "6"], 1, "Rata-rata satu sampai enam.", hint="Tengah."),
        Q("E[X+Y] sama dengan?", ["E[X]E[Y]", "E[X]+E[Y]", "E[X]-E[Y]", "Tak tentu"], 1, "Linearitas tanpa syarat.", hint="Jumlah."),
        Q("E[X^2] vs E[X]^2?", ["Selalu sama", "Umumnya berbeda", "Selalu lebih kecil", "Nol"], 1, "Selisih adalah varians.", hint="Varians."),
        Q("Ekspektasi kontinu?", ["integral x f(x) dx", "integral f(x) dx", "f(x)", "x f(x)"], 0, "Rata-rata berbobot kepadatan.", hint="Integral."),
    ],
    [
        "Ekspektasi adalah rata-rata berbobot jangka panjang.",
        "E[g(X)] dihitung dengan PMF asli, bukan g(E[X]).",
        "Linearitas berlaku tanpa independensi.",
        "Ekspektasi dasar untuk menilai keputusan dan fungsi kerugian.",
    ],
    [],
)

l2 = lesson(
    "A4-06-2",
    "Varians dan simpangan baku",
    35,
    [
        "Menghitung varians dan simpangan baku dari distribusi",
        "Memakai rumus E[X^2] dikurangi kuadrat E[X]",
        "Memakai varians transformasi linear dan jumlah independen",
        "Membedakan varians populasi dan sampel",
    ],
    [
        T("""
        ## Mengukur sebaran

        Dua distribusi bisa memiliki rata-rata sama tetapi sebaran sangat berbeda. Gaji dua perusahaan yang rata-ratanya sama bisa terkonsentrasi di satu angka atau tersebar dari sangat rendah sampai sangat tinggi. **Varians** mengukur sebaran itu: rata-rata kuadrat selisih dari ekspektasi, `Var(X) = E[(X - mu)^2]`.

        Karena dikuadratkan, satuannya kuadrat dari satuan data. Maka kita sering memakai **simpangan baku**, akar varians, yang kembali ke satuan semula. Simpangan baku 1,7 pada dadu dapat dibaca sebagai selisih tipikal dari rata-rata 3,5.
        """),
        T("""
        ## Rumus praktis

        Menurut definisi, varians membutuhkan dua langkah: cari rata-rata lalu rata-rata kuadrat selisih. Aljabar sederhana memberi jalan pintas: `Var(X) = E[X^2] - (E[X])^2`. Rata-rata kuadrat dikurangi kuadrat rata-rata. Jalan pintas ini juga membuktikan bahwa `E[X^2] >= E[X]^2` karena varians tidak negatif.

        Peringatan numerik: untuk data besar dengan rata-rata jauh dari nol, pengurangan dua bilangan besar yang hampir sama dapat kehilangan ketelitian. Pustaka yang serius memakai algoritma yang lebih stabil, tetapi untuk perhitungan kecil rumus ini cukup.
        """),
        C(
            """
            pmf = {k: 1 / 6 for k in range(1, 7)}
            e1 = sum(k * p for k, p in pmf.items())
            e2 = sum(k * k * p for k, p in pmf.items())
            var = e2 - e1 ** 2
            print(round(var, 4), round(var ** 0.5, 4))
            """,
            """
            2.9167 1.7078
            """,
            """
            Varians dadu adalah tiga puluh lima per dua belas dan simpangan bakunya sekitar satu koma tujuh.
            """,
            filename="varians_dadu.py",
        ),
        T("""
        ## Transformasi linear

        Menambah konstanta tidak mengubah sebaran, hanya menggeser. Mengalikan dengan `a` memperbesar simpangan sebesar `|a|` dan varians sebesar `a^2`. Jadi `Var(aX + b) = a^2 Var(X)`. Konstanta `b` hilang dan tanda `a` tidak berpengaruh karena dikuadratkan.

        Ini menjelaskan mengapa mengubah satuan, misalnya meter menjadi sentimeter, mengalikan varians dengan sepuluh ribu. Ini juga dasar standarisasi: dengan `a = 1/sigma` dan `b = -mu/sigma`, hasilnya berrata-rata nol dan varians satu.
        """),
        C(
            """
            pmf = {k: 1 / 6 for k in range(1, 7)}
            y = {2 * k + 3: p for k, p in pmf.items()}
            e = sum(v * p for v, p in y.items())
            var_y = sum((v - e) ** 2 * p for v, p in y.items())
            var_x = sum((k - 3.5) ** 2 * p for k, p in pmf.items())
            print(round(var_y, 4), round(4 * var_x, 4))
            """,
            """
            11.6667 11.6667
            """,
            """
            Varians dua kali dadu ditambah tiga sama dengan empat kali varians dadu, dan konstanta tiga tidak berpengaruh.
            """,
            filename="varians_linear.py",
        ),
        T("""
        ## Varians jumlah

        Untuk variabel yang **independen**, varians jumlah adalah jumlah varians: `Var(X + Y) = Var(X) + Var(Y)`. Dua dadu independen memiliki varians jumlah `2 * 35/12`, sekitar 5,83. Berbeda dengan ekspektasi, varians jumlah membutuhkan independensi atau minimal ketidakberkorelasian. Bila ada hubungan, muncul suku kovarians yang dibahas di pelajaran berikutnya.

        Akibat penting: rata-rata `n` variabel independen dengan varians sama `sigma^2` memiliki varians `sigma^2 / n`. Rata-rata sampel makin presisi seiring bertambahnya data, dengan simpangan baku turun sebagai satu per akar `n`.
        """),
        C(
            """
            from itertools import product

            S = list(product(range(1, 7), repeat=2))
            e = sum(a + b for a, b in S) / 36
            v = sum((a + b - e) ** 2 for a, b in S) / 36
            print(round(v, 4), round(2 * 35 / 12, 4))
            """,
            """
            5.8333 5.8333
            """,
            """
            Varians jumlah dua dadu independen sama dengan dua kali varians satu dadu.
            """,
            filename="varians_jumlah.py",
        ),
        T("""
        ## Populasi dan sampel

        Varians populasi membagi dengan `n`. Namun bila kita menaksir varians dari sampel dengan rata-rata sampel, pembagi `n` cenderung terlalu kecil karena data lebih dekat ke rata-rata sampelnya sendiri daripada ke rata-rata sebenarnya. **Varians sampel** memakai pembagi `n - 1`, yang menghilangkan bias itu. Selisihnya kecil untuk `n` besar tetapi nyata untuk sampel kecil.

        Di Python, `statistics.pvariance` memakai `n` dan `statistics.variance` memakai `n - 1`. NumPy memakai `n` secara bawaan dan butuh `ddof=1` untuk `n - 1`. Perbedaan bawaan ini sumber kebingungan umum, jadi selalu periksa dokumentasinya.
        """),
        C(
            """
            import statistics

            d = [2, 4, 4, 4, 5, 5, 7, 9]
            print(float(statistics.pvariance(d)), round(statistics.variance(d), 4))
            print([round(p * (1 - p), 4) for p in (0.1, 0.5, 0.9)])
            """,
            """
            4.0 4.5714
            [0.09, 0.25, 0.09]
            """,
            """
            Pembagi n menghasilkan empat dan pembagi n minus satu menghasilkan sekitar empat koma enam. Varians Bernoulli terbesar pada peluang setengah.
            """,
            filename="varians_sampel.py",
        ),
        K(
            "tip",
            """
            Selalu cek apakah fungsi varians di pustakamu memakai pembagi n atau n minus 1. NumPy memakai n secara bawaan, pandas memakai n minus 1.
            """,
            title="Cek pembagi",
        ),
        T("""
        ## Ketaksamaan Chebyshev

        Tanpa mengetahui bentuk distribusi, varians tetap membatasi seberapa jauh nilai bisa menyimpang. **Ketaksamaan Chebyshev** menyatakan peluang menyimpang lebih dari `k` simpangan baku dari rata-rata paling banyak `1/k^2`. Maka paling sedikit 75 persen data berada dalam dua simpangan baku dan 89 persen dalam tiga, untuk distribusi apa pun.

        Batas ini longgar dibanding aturan normal, tetapi universal. Berguna ketika kita tidak mau mengasumsikan bentuk distribusi dan hanya mengetahui rata-rata dan simpangan baku.
        """),
        T("""
        ## Varians dalam praktik

        Varians muncul dalam banyak keputusan. Dua investasi dengan imbal hasil rata-rata sama tetapi varians berbeda menawarkan risiko berbeda, dan varians sering dipakai sebagai ukuran risiko. Dalam pengendalian mutu, varians proses yang besar berarti produk tidak konsisten walau rata-ratanya tepat sasaran.

        Dalam machine learning, dekomposisi galat prediksi menjadi bias dan varians menjelaskan overfitting. Model terlalu fleksibel memiliki varians tinggi: prediksinya berubah banyak bila data latih berganti. Memahami varians sebagai sensitivitas terhadap sampel membuat gagasan ini terasa konkret.
        """),
        T("""
        ## Simpangan baku sebagai skala

        Simpangan baku memberi skala alami untuk mengukur jarak dalam data. Menyebut sebuah nilai berjarak dua simpangan baku dari rata-rata lebih bermakna daripada menyebut selisihnya sepuluh satuan, karena yang pertama dapat dibandingkan lintas variabel. Skala ini dipakai pada z-score, deteksi pencilan, dan standarisasi fitur.
        """),
        E(
            "A4-06-2-ex1",
            "mudah",
            """
            Tulis fungsi `varians(pmf)` yang mengembalikan `Var(X) = E[X^2] - E[X]^2` dari dict PMF, dibulatkan 4 desimal. Hindari `-0.0`.
            """,
            """
            def varians(pmf):
                # TODO: implementasikan
                pass
            """,
            """
            assert varians({k: 1 / 6 for k in range(1, 7)}) == 2.9167
            assert varians({5: 1.0}) == 0.0
            assert varians({0: 0.5, 1: 0.5}) == 0.25
            assert varians({-1: 0.5, 1: 0.5}) == 1.0
            """,
            "Hitung rata-rata kuadrat lalu kurangi kuadrat rata-rata.",
            """
            def varians(pmf):
                e1 = sum(x * p for x, p in pmf.items())
                e2 = sum(x * x * p for x, p in pmf.items())
                return round(e2 - e1 ** 2, 4) + 0.0
            """,
        ),
        E(
            "A4-06-2-ex2",
            "sedang",
            """
            Tulis fungsi `varians_sampel(data, ddof=1)` yang mengembalikan varians dengan pembagi `n - ddof`, dibulatkan 4 desimal.
            """,
            """
            def varians_sampel(data, ddof=1):
                # TODO: implementasikan
                pass
            """,
            """
            d = [2, 4, 4, 4, 5, 5, 7, 9]
            assert varians_sampel(d, 0) == 4.0
            assert varians_sampel(d) == 4.5714
            assert varians_sampel([1, 2, 3]) == 1.0
            assert varians_sampel([5, 5], 0) == 0.0
            """,
            "Jumlahkan kuadrat selisih dari rata-rata lalu bagi dengan n dikurangi ddof.",
            """
            def varians_sampel(data, ddof=1):
                m = sum(data) / len(data)
                return round(sum((x - m) ** 2 for x in data) / (len(data) - ddof), 4)
            """,
        ),
        E(
            "A4-06-2-ex3",
            "sedang",
            """
            Tulis fungsi `varians_transformasi(var, a, b)` yang mengembalikan `Var(aX + b)` bila `Var(X) = var`, dibulatkan 4 desimal.
            """,
            """
            def varians_transformasi(var, a, b):
                # TODO: implementasikan
                pass
            """,
            """
            assert varians_transformasi(4, 3, 5) == 36.0
            assert varians_transformasi(1, -2, 0) == 4.0
            assert varians_transformasi(2.5, 0, 7) == 0.0
            assert varians_transformasi(0.25, 10, 1) == 25.0
            """,
            "Konstanta tidak berpengaruh dan koefisien dikuadratkan.",
            """
            def varians_transformasi(var, a, b):
                return round(a * a * var, 4)
            """,
        ),
        E(
            "A4-06-2-ex4",
            "menantang",
            """
            Tulis fungsi `varians_jumlah_independen(vars, koef)` yang mengembalikan varians kombinasi linear `c1 X1 + c2 X2 + ...` dari variabel independen berukuran varians `vars`, dibulatkan 4 desimal.
            """,
            """
            def varians_jumlah_independen(vars, koef):
                # TODO: implementasikan
                pass
            """,
            """
            assert varians_jumlah_independen([1, 2, 3], [1, 1, 1]) == 6.0
            assert varians_jumlah_independen([4, 9], [1, -1]) == 13.0
            assert varians_jumlah_independen([2], [3]) == 18.0
            assert varians_jumlah_independen([], []) == 0.0
            assert varians_jumlah_independen([4, 4, 4, 4], [0.25] * 4) == 1.0
            """,
            "Jumlahkan koefisien kuadrat kali varians masing-masing.",
            """
            def varians_jumlah_independen(vars, koef):
                return round(sum(c * c * v for c, v in zip(koef, vars)), 4)
            """,
        ),
    ],
    [
        M("Memakai pembagi n untuk varians sampel kecil.", "Pakai n minus 1 untuk taksiran tak bias."),
        M("Menjumlahkan varians tanpa independensi.", "Tambahkan suku kovarians."),
        M("Mengira Var(aX + b) = a Var(X) + b.", "Hasilnya a kuadrat kali Var(X)."),
    ],
    [
        Q("Varians adalah?", ["E[(X-mu)^2]", "E[X]", "Akar E[X]", "Median"], 0, "Rata-rata kuadrat selisih.", hint="Sebaran."),
        Q("Rumus praktis?", ["E[X^2]-E[X]^2", "E[X]-E[X^2]", "E[X]^2", "E[2X]"], 0, "Rata-rata kuadrat kurangi kuadrat rata-rata.", hint="Dua momen."),
        Q("Var(aX+b)?", ["a Var + b", "a^2 Var", "Var + b", "a Var"], 1, "Konstanta hilang.", hint="Kuadrat."),
        Q("Varians jumlah independen?", ["Jumlah varians", "Hasil kali", "Selisih", "Nol"], 0, "Tanpa kovarians.", hint="Tambah."),
        Q("Varians sampel memakai pembagi?", ["n", "n-1", "n+1", "2n"], 1, "Menghapus bias.", hint="Kurang satu."),
    ],
    [
        "Varians mengukur sebaran dan simpangan baku kembali ke satuan data.",
        "Var(aX + b) sama dengan a kuadrat kali Var(X).",
        "Varians jumlah independen adalah jumlah varians.",
        "Varians sampel memakai pembagi n minus 1.",
    ],
    [],
)

l3 = lesson(
    "A4-06-3",
    "Kovarians dan korelasi",
    35,
    [
        "Menghitung kovarians dari PMF gabungan dan dari data",
        "Menghitung koefisien korelasi Pearson",
        "Menjelaskan bahwa tak berkorelasi tidak berarti independen",
        "Memakai rumus varians jumlah dengan kovarians",
    ],
    [
        T("""
        ## Mengukur hubungan

        Varians mengukur sebaran satu variabel. Untuk dua variabel kita ingin tahu apakah mereka bergerak bersama. **Kovarians** mengukurnya: `Cov(X, Y) = E[(X - mu_X)(Y - mu_Y)] = E[XY] - E[X] E[Y]`. Bila `X` di atas rata-ratanya cenderung bersamaan dengan `Y` di atas rata-ratanya, hasil kali positif dan kovarians positif.

        Kovarians negatif berarti satu naik saat yang lain turun, dan kovarians nol berarti tidak ada hubungan linear. Besar kovarians bergantung pada satuan variabel, sehingga sulit ditafsirkan langsung. Itu motivasi korelasi.
        """),
        C(
            """
            joint = {(0, 0): 0.1, (0, 1): 0.2, (1, 0): 0.3, (1, 1): 0.4}
            ex = sum(x * p for (x, y), p in joint.items())
            ey = sum(y * p for (x, y), p in joint.items())
            exy = sum(x * y * p for (x, y), p in joint.items())
            print(round(exy - ex * ey, 4))
            """,
            """
            -0.02
            """,
            """
            Kovarians tabel gabungan ini sedikit negatif, menandakan hubungan lemah berlawanan arah.
            """,
            filename="kovarians_joint.py",
        ),
        T("""
        ## Independen berarti kovarians nol

        Bila `X` dan `Y` independen maka `E[XY] = E[X] E[Y]`, sehingga kovariansnya nol. Pada tabel gabungan yang dibangun dari hasil kali marginal, kovarians tepat nol. Arah sebaliknya tidak berlaku, seperti ditunjukkan contoh di bawah.

        Karena itu kovarians nol hanya bisa mengecualikan hubungan **linear**. Hubungan melengkung dapat tersembunyi sepenuhnya dari kovarians.
        """),
        C(
            """
            joint = {(0, 0): 0.12, (0, 1): 0.18, (1, 0): 0.28, (1, 1): 0.42}
            ex = sum(x * p for (x, y), p in joint.items())
            ey = sum(y * p for (x, y), p in joint.items())
            exy = sum(x * y * p for (x, y), p in joint.items())
            print(round(exy - ex * ey, 4) + 0.0)
            """,
            """
            0.0
            """,
            """
            Tabel yang dibangun dari hasil kali marginal memiliki kovarians nol.
            """,
            filename="kovarians_independen.py",
        ),
        T("""
        ## Tak berkorelasi bukan independen

        Misalkan `X` seragam pada `{-1, 0, 1}` dan `Y = X^2`. Jelas `Y` ditentukan sepenuhnya oleh `X`, jadi keduanya sangat bergantung. Namun `E[XY] = E[X^3] = 0` dan `E[X] = 0`, sehingga kovariansnya nol. Hubungannya simetris berbentuk parabola, dan kovarians hanya menangkap kecenderungan garis lurus.

        Pelajarannya: kovarians atau korelasi nol tidak membuktikan independensi. Selalu plot data sebelum menyimpulkan tidak ada hubungan.
        """),
        C(
            """
            joint = {(-1, 1): 1 / 3, (0, 0): 1 / 3, (1, 1): 1 / 3}
            ex = sum(x * p for (x, y), p in joint.items())
            ey = sum(y * p for (x, y), p in joint.items())
            exy = sum(x * y * p for (x, y), p in joint.items())
            print(round(exy - ex * ey, 4) + 0.0, round(ey, 4), 1.0)
            """,
            """
            0.0 0.6667 1.0
            """,
            """
            Kovarians nol, padahal peluang Y bernilai satu naik dari dua pertiga menjadi satu pasti bila X diketahui bukan nol, bukti ketergantungan.
            """,
            filename="tak_berkorelasi.py",
        ),
        T("""
        ## Koefisien korelasi

        **Korelasi Pearson** menormalkan kovarians: `rho = Cov(X, Y) / (sigma_X * sigma_Y)`. Hasilnya tak berdimensi dan selalu antara `-1` dan `1`. Nilai `1` berarti hubungan linear sempurna naik, `-1` linear sempurna turun, dan `0` tidak ada hubungan linear.

        Kini angka dapat dibandingkan antar pasangan variabel dengan satuan berbeda. Korelasi 0,77 antara jam belajar dan nilai ujian berarti hubungan linear positif cukup kuat. Namun korelasi bukan sebab akibat, dan sangat sensitif terhadap pencilan.
        """),
        C(
            """
            import numpy as np

            x = [1, 2, 3, 4, 5]
            y = [2, 4, 5, 4, 5]
            print(round(float(np.cov(x, y)[0, 1]), 4), round(float(np.corrcoef(x, y)[0, 1]), 4))
            """,
            """
            1.5 0.7746
            """,
            """
            Kovarians sampel satu koma lima dan korelasi sekitar tujuh puluh tujuh persen menunjukkan hubungan naik yang cukup kuat.
            """,
            filename="korelasi_data.py",
        ),
        T("""
        ## Varians jumlah dengan kovarians

        Rumus umum varians jumlah adalah `Var(X + Y) = Var(X) + Var(Y) + 2 Cov(X, Y)`. Bila independen suku terakhir nol dan kita kembali ke rumus sebelumnya. Bila berkorelasi positif, variansnya lebih besar karena kedua variabel saling memperkuat.

        Inilah dasar diversifikasi portofolio: menggabungkan aset yang berkorelasi rendah atau negatif menurunkan varians total. Juga alasan fitur yang sangat berkorelasi dalam regresi menimbulkan ketidakstabilan koefisien.
        """),
        C(
            """
            joint = {(0, 0): 0.1, (0, 1): 0.2, (1, 0): 0.3, (1, 1): 0.4}
            e = sum((x + y) * p for (x, y), p in joint.items())
            v = sum((x + y - e) ** 2 * p for (x, y), p in joint.items())
            print(round(v, 4), round(0.21 + 0.24 + 2 * (-0.02), 4))
            """,
            """
            0.41 0.41
            """,
            """
            Hitungan langsung dan rumus dengan kovarians memberi varians jumlah yang sama.
            """,
            filename="varians_dengan_kov.py",
        ),
        K(
            "warn",
            """
            Korelasi tinggi tidak membuktikan sebab akibat, dan korelasi nol tidak membuktikan independen. Selalu lihat diagram pencar sebelum menafsirkan.
            """,
            title="Batas korelasi",
        ),
        T("""
        ## Matriks kovarians

        Untuk banyak variabel, kovarians semua pasangan disusun dalam **matriks kovarians**. Diagonalnya adalah varians tiap variabel dan elemen di luar diagonal adalah kovarians antar pasangan. Matriks ini simetris dan, seperti dilihat di aljabar linear, memiliki nilai eigen tak negatif.

        Analisis komponen utama, yang sudah kamu bangun dari nol, bekerja pada matriks ini. Memahami kovarians sebagai ukuran hubungan memberi makna intuitif bagi arah komponen utama: arah tempat data paling bervariasi bersama.
        """),
        T("""
        ## Membaca diagram pencar

        Angka korelasi sebaiknya selalu ditemani diagram pencar. Empat dataset dapat memiliki korelasi, rata-rata, dan varians yang hampir identik tetapi bentuk titik yang sama sekali berbeda: satu garis bersih, satu parabola, satu dengan pencilan tunggal, satu vertikal kecuali satu titik. Contoh terkenal ini menekankan bahwa ringkasan angka bisa menyembunyikan struktur penting.

        Satu pencilan dapat mengubah korelasi dari hampir nol menjadi tinggi atau sebaliknya. Karena itu periksa pencilan dan pertimbangkan ukuran yang lebih kokoh seperti korelasi peringkat Spearman bila data memiliki ekor panjang.
        """),
        T("""
        ## Dari hubungan ke prediksi

        Korelasi tinggi berarti satu variabel membantu memprediksi variabel lain. Regresi linear sederhana memanfaatkannya: kemiringan garis terbaik sama dengan korelasi dikali rasio simpangan baku `y` terhadap `x`. Kuadrat korelasi, `R^2`, menyatakan proporsi varians `y` yang dijelaskan oleh `x`.

        Maka korelasi 0,77 berarti sekitar 60 persen varians dijelaskan secara linear. Sisanya dipengaruhi faktor lain atau derau. Hubungan antara kovarians, korelasi, dan regresi ini akan muncul kembali di kursus statistika dan machine learning.
        """),
        T("""
        ## Korelasi dan agregasi

        Hati-hati dengan agregasi. Korelasi pada data per kelompok dapat berbeda, bahkan berlawanan tanda, dengan korelasi pada data gabungan. Fenomena ini dikenal sebagai paradoks Simpson. Bila kelompok berbeda dalam rata-rata kedua variabel, menggabungkannya dapat menciptakan hubungan semu atau menyembunyikan hubungan nyata.

        Biasakan menanyakan apakah ada variabel pengelompokan yang tersembunyi sebelum menafsirkan korelasi dari data gabungan.
        """),
        E(
            "A4-06-3-ex1",
            "mudah",
            """
            Tulis fungsi `kovarians_joint(joint)` yang mengembalikan `E[XY] - E[X] E[Y]` dari dict PMF gabungan berkunci tuple `(x, y)`, dibulatkan 4 desimal. Hindari `-0.0`.
            """,
            """
            def kovarians_joint(joint):
                # TODO: implementasikan
                pass
            """,
            """
            j = {(0, 0): 0.1, (0, 1): 0.2, (1, 0): 0.3, (1, 1): 0.4}
            assert kovarians_joint(j) == -0.02
            assert kovarians_joint({(0, 0): 0.12, (0, 1): 0.18, (1, 0): 0.28, (1, 1): 0.42}) == 0.0
            assert kovarians_joint({(0, 0): 0.5, (1, 1): 0.5}) == 0.25
            assert kovarians_joint({(0, 1): 0.5, (1, 0): 0.5}) == -0.25
            """,
            "Hitung tiga ekspektasi dari tabel gabungan lalu kurangi.",
            """
            def kovarians_joint(joint):
                ex = sum(x * p for (x, y), p in joint.items())
                ey = sum(y * p for (x, y), p in joint.items())
                exy = sum(x * y * p for (x, y), p in joint.items())
                return round(exy - ex * ey, 4) + 0.0
            """,
        ),
        E(
            "A4-06-3-ex2",
            "sedang",
            """
            Tulis fungsi `korelasi_joint(joint)` yang mengembalikan korelasi Pearson dari dict PMF gabungan, dibulatkan 4 desimal. Hindari `-0.0`.
            """,
            """
            import math

            def korelasi_joint(joint):
                # TODO: implementasikan
                pass
            """,
            """
            j = {(0, 0): 0.1, (0, 1): 0.2, (1, 0): 0.3, (1, 1): 0.4}
            assert korelasi_joint(j) == -0.0891
            assert korelasi_joint({(0, 0): 0.5, (1, 1): 0.5}) == 1.0
            assert korelasi_joint({(0, 1): 0.5, (1, 0): 0.5}) == -1.0
            assert korelasi_joint({(0, 0): 0.12, (0, 1): 0.18, (1, 0): 0.28, (1, 1): 0.42}) == 0.0
            """,
            "Bagi kovarians dengan hasil kali simpangan baku kedua marginal.",
            """
            import math

            def korelasi_joint(joint):
                ex = sum(x * p for (x, y), p in joint.items())
                ey = sum(y * p for (x, y), p in joint.items())
                exy = sum(x * y * p for (x, y), p in joint.items())
                vx = sum(x * x * p for (x, y), p in joint.items()) - ex ** 2
                vy = sum(y * y * p for (x, y), p in joint.items()) - ey ** 2
                return round((exy - ex * ey) / math.sqrt(vx * vy), 4) + 0.0
            """,
        ),
        E(
            "A4-06-3-ex3",
            "sedang",
            """
            Tulis fungsi `kovarians_sampel(x, y)` yang mengembalikan kovarians sampel dengan pembagi `n - 1` dari dua list sama panjang, dibulatkan 4 desimal. Hindari `-0.0`.
            """,
            """
            def kovarians_sampel(x, y):
                # TODO: implementasikan
                pass
            """,
            """
            assert kovarians_sampel([1, 2, 3, 4, 5], [2, 4, 5, 4, 5]) == 1.5
            assert kovarians_sampel([1, 2, 3], [3, 2, 1]) == -1.0
            assert kovarians_sampel([1, 2, 3], [5, 5, 5]) == 0.0
            assert kovarians_sampel([1, 2], [1, 2]) == 0.5
            """,
            "Jumlahkan hasil kali selisih dari rata-rata masing-masing lalu bagi dengan n dikurangi satu.",
            """
            def kovarians_sampel(x, y):
                n = len(x)
                mx = sum(x) / n
                my = sum(y) / n
                return round(sum((a - mx) * (b - my) for a, b in zip(x, y)) / (n - 1), 4) + 0.0
            """,
        ),
        E(
            "A4-06-3-ex4",
            "menantang",
            """
            Tulis fungsi `korelasi_pearson(x, y)` yang mengembalikan koefisien korelasi Pearson dari dua list sama panjang, dibulatkan 4 desimal. Hindari `-0.0`.
            """,
            """
            import math

            def korelasi_pearson(x, y):
                # TODO: implementasikan
                pass
            """,
            """
            assert korelasi_pearson([1, 2, 3, 4, 5], [2, 4, 5, 4, 5]) == 0.7746
            assert korelasi_pearson([1, 2, 3], [3, 2, 1]) == -1.0
            assert korelasi_pearson([1, 2, 3], [2, 4, 6]) == 1.0
            assert korelasi_pearson([1, 2, 3, 4], [1, 0, 0, 1]) == 0.0
            """,
            "Bagi jumlah hasil kali selisih dengan akar hasil kali jumlah kuadrat selisih masing-masing.",
            """
            import math

            def korelasi_pearson(x, y):
                n = len(x)
                mx = sum(x) / n
                my = sum(y) / n
                sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
                sxx = sum((a - mx) ** 2 for a in x)
                syy = sum((b - my) ** 2 for b in y)
                return round(sxy / math.sqrt(sxx * syy), 4) + 0.0
            """,
        ),
    ],
    [
        M("Menyimpulkan independen dari korelasi nol.", "Korelasi hanya menangkap hubungan linear."),
        M("Menafsirkan korelasi sebagai sebab akibat.", "Korelasi hanya asosiasi."),
        M("Melupakan suku kovarians pada varians jumlah.", "Var(X+Y) memuat 2 Cov(X,Y)."),
    ],
    [
        Q("Kovarians positif berarti?", ["Naik bersama", "Berlawanan", "Independen", "Konstan"], 0, "Bergerak searah.", hint="Searah."),
        Q("Korelasi berkisar?", ["0 sampai 1", "-1 sampai 1", "Tak terbatas", "0 sampai 100"], 1, "Dinormalisasi.", hint="Batas."),
        Q("Korelasi nol berarti?", ["Independen", "Tidak ada hubungan linear", "Sebab akibat", "Konstan"], 1, "Hubungan lain mungkin ada.", hint="Linear saja."),
        Q("Var(X+Y)?", ["Var X + Var Y", "Var X + Var Y + 2Cov", "Var X Var Y", "Cov"], 1, "Dengan kovarians.", hint="Suku silang."),
        Q("Independen berarti Cov?", ["Satu", "Nol", "Negatif", "Tak tentu"], 1, "E[XY]=E[X]E[Y].", hint="Hasil kali."),
    ],
    [
        "Kovarians mengukur hubungan linear dan korelasi menormalkannya.",
        "Independen berimplikasi kovarians nol tetapi tidak sebaliknya.",
        "Var(X+Y) memuat dua kali kovarians.",
        "Korelasi bukan sebab akibat.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perhitungan yang cukup jelas dalam teks.", "brief": []}

write_module(
    "A4",
    6,
    "Ekspektasi, varians, dan kovarians",
    105,
    [
        "Menghitung ekspektasi dan memakai linearitas",
        "Menghitung varians dan simpangan baku",
        "Menghitung kovarians dan korelasi",
    ],
    [l1, l2, l3],
    video,
    REF,
)
