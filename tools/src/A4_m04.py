import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

l1 = lesson(
    "A4-04-1",
    "Fungsi kepadatan peluang",
    35,
    [
        "Menjelaskan mengapa variabel kontinu memakai kepadatan, bukan massa",
        "Menghitung peluang sebagai luas di bawah kurva kepadatan",
        "Menghitung integral dengan aturan titik tengah dan trapesium",
        "Menormalkan fungsi menjadi kepadatan yang valid",
    ],
    [
        T("""
        ## Ketika nilai tak terhitung

        Tinggi badan, waktu tunggu, dan suhu dapat bernilai di sembarang titik pada suatu rentang. Peluang tinggi badan seseorang tepat 170,000000 cm adalah nol, karena ada tak terhingga banyak nilai yang mungkin dan massa peluang tidak mungkin dibagi ke semuanya. Karena itu variabel kontinu tidak memakai PMF.

        Sebagai gantinya kita memakai **fungsi kepadatan peluang** atau PDF, yang ditulis `f(x)`. PDF bukan peluang, melainkan kepadatan: peluang tinggal di rentang kecil di sekitar `x` kira-kira `f(x)` dikali lebar rentang. Peluang sebenarnya muncul ketika kita mengambil luas.
        """),
        T("""
        ## Peluang sebagai luas

        Untuk variabel kontinu `X` dengan PDF `f`, peluang `X` jatuh antara `a` dan `b` adalah luas di bawah kurva `f` dari `a` sampai `b`: `P(a <= X <= b) = integral f(x) dx` dari `a` ke `b`. Luas total di bawah kurva harus satu, dan `f(x)` tidak boleh negatif.

        Konsekuensinya, `P(X = a) = 0` karena luas dengan lebar nol adalah nol. Maka batas inklusif atau eksklusif tidak berpengaruh: `P(a < X < b)` sama dengan `P(a <= X <= b)`. Ini berbeda dari kasus diskrit dan sering membingungkan pemula.
        """),
        T("""
        ## Integral numerik

        Tidak semua PDF punya integral dengan rumus tertutup yang mudah. Kita bisa mengaproksimasi luas dengan membagi rentang menjadi `n` potongan kecil. **Aturan titik tengah** menghitung tinggi fungsi di tengah tiap potongan lalu menjumlahkan tinggi kali lebar. **Aturan trapesium** menganggap tiap potongan trapesium dan menjumlahkan luasnya.

        Kedua aturan makin akurat bila `n` membesar. Untuk fungsi mulus, kesalahan berkurang secara kuadrat dalam lebar potongan. Menulis integral numerik dari nol adalah latihan bagus karena ia memperlihatkan bahwa integral hanyalah penjumlahan banyak persegi panjang tipis.
        """),
        C(
            """
            def integral(f, a, b, n=10000):
                h = (b - a) / n
                return sum(f(a + (i + 0.5) * h) for i in range(n)) * h

            print(round(integral(lambda x: 2 * x, 0, 1), 4))
            print(round(integral(lambda x: 2 * x, 0.25, 0.75), 4))
            """,
            """
            1.0
            0.5
            """,
            """
            Kepadatan dua x pada nol sampai satu memiliki luas total satu, dan peluang antara seperempat dan tiga perempat adalah setengah.
            """,
            filename="integral_numerik.py",
        ),
        T("""
        ## Peluang titik adalah nol

        Mari periksa klaim bahwa peluang satu titik adalah nol. Integral pada interval dengan lebar nol bernilai nol. Pada interval yang sangat sempit, misalnya selebar `0,000001`, peluangnya kira-kira kepadatan kali lebar, yaitu bilangan yang sangat kecil.

        Ini bukan berarti nilai itu mustahil. Setelah kita mengamati sebuah nilai, nilai itu tentu terjadi, padahal peluangnya nol. Kita memakai peluang pada interval, bukan titik, untuk membicarakan kemungkinan. Di praktik, semua pengukuran berpresisi terbatas sehingga sebenarnya kita selalu mengamati interval kecil.
        """),
        C(
            """
            def integral(f, a, b, n=1000):
                h = (b - a) / n
                return sum(f(a + (i + 0.5) * h) for i in range(n)) * h

            f = lambda x: 2 * x
            print(integral(f, 0.5, 0.5))
            print(integral(f, 0.5, 0.500001) < 1e-5)
            """,
            """
            0.0
            True
            """,
            """
            Interval selebar nol memiliki luas nol dan interval yang sangat sempit memiliki peluang yang sangat kecil.
            """,
            filename="peluang_titik.py",
        ),
        T("""
        ## Distribusi seragam

        Distribusi paling sederhana adalah **seragam** pada `[a, b]`: kepadatan konstan `1/(b-a)` di dalam rentang dan nol di luar. Semua sub-interval dengan lebar sama punya peluang sama. Peluang `X` berada di `[2, 5]` pada seragam `[0, 10]` adalah lebar `3` dikali kepadatan `0,1`, yaitu `0,3`.

        Kepadatan boleh lebih dari satu! Pada seragam `[0, 0,5]` kepadatannya `2`. Yang harus satu adalah luas total, bukan tinggi kurva. Tinggi hanyalah peluang per satuan lebar, dan bila lebarnya kecil maka tingginya besar.
        """),
        C(
            """
            def pdf_seragam(x, a, b):
                return 1 / (b - a) if a <= x <= b else 0.0

            def integral(f, a, b, n=3000):
                h = (b - a) / n
                return sum(f(a + (i + 0.5) * h) for i in range(n)) * h

            print(pdf_seragam(5, 0, 10), pdf_seragam(11, 0, 10), round(integral(lambda x: pdf_seragam(x, 0, 10), 2, 5), 4))
            print(pdf_seragam(0.2, 0, 0.5))
            """,
            """
            0.1 0.0 0.3
            2.0
            """,
            """
            Kepadatan seragam nol sampai sepuluh adalah sepersepuluh di dalam rentang. Pada rentang yang sempit kepadatan bisa lebih dari satu.
            """,
            filename="seragam.py",
        ),
        K(
            "warn",
            """
            Nilai PDF di satu titik bukan peluang dan boleh lebih dari satu. Hanya luas di bawah kurva pada sebuah interval yang merupakan peluang.
            """,
            title="PDF bukan peluang",
        ),
        T("""
        ## Normalisasi

        Sering kita punya bentuk fungsi tetapi belum tahu konstantanya. Misalnya `f(x) = c * x` pada `[0, 2]`. Agar menjadi PDF, luasnya harus satu, sehingga `c = 1 / integral dari x`. Karena integral `x` dari nol sampai dua adalah dua, maka `c = 0,5`.

        Teknik ini sangat umum: tentukan bentuk yang sebanding dengan kepadatan, hitung luasnya, lalu bagi dengan luas itu. Statistik Bayesian memakai gagasan ini terus-menerus ketika posterior hanya dikenal sebanding dengan prior kali likelihood.
        """),
        T("""
        ## Ringkasan dan kebiasaan

        Ingat tiga hal. PDF tidak negatif dan luas totalnya satu. Peluang adalah luas, sehingga titik tunggal berpeluang nol. Nilai PDF boleh melebihi satu. Bila ragu apakah suatu fungsi adalah PDF yang valid, hitung integralnya secara numerik dan periksa nilai minimumnya.

        Latihan berikut membuat kamu mengimplementasikan integral numerik dan memakainya untuk menghitung peluang serta menormalkan fungsi. Pelajaran berikutnya memakai ide yang sama pada fungsi distribusi kumulatif dan kuantil.
        """),
        E(
            "A4-04-1-ex1",
            "mudah",
            """
            Tulis fungsi `pdf_seragam(x, a, b)` yang mengembalikan `1 / (b - a)` bila `a <= x <= b` dan `0.0` bila di luar rentang.
            """,
            """
            def pdf_seragam(x, a, b):
                # TODO: implementasikan
                pass
            """,
            """
            assert pdf_seragam(5, 0, 10) == 0.1
            assert pdf_seragam(11, 0, 10) == 0.0
            assert pdf_seragam(0.2, 0, 0.5) == 2.0
            assert pdf_seragam(-1, 0, 1) == 0.0
            assert pdf_seragam(0.5, 0, 1) == 1.0
            """,
            "Periksa apakah x berada dalam rentang lalu kembalikan kebalikan lebar.",
            """
            def pdf_seragam(x, a, b):
                return 1 / (b - a) if a <= x <= b else 0.0
            """,
        ),
        E(
            "A4-04-1-ex2",
            "sedang",
            """
            Tulis fungsi `integral_trapesium(f, a, b, n)` yang mengaproksimasi integral `f` dari `a` ke `b` dengan aturan trapesium memakai `n` potongan sama lebar. Bulatkan hasil 4 desimal.
            """,
            """
            def integral_trapesium(f, a, b, n):
                # TODO: implementasikan
                pass
            """,
            """
            assert integral_trapesium(lambda x: x, 0, 1, 1) == 0.5
            assert integral_trapesium(lambda x: x * x, 0, 1, 2) == 0.375
            assert integral_trapesium(lambda x: x * x, 0, 1, 10) == 0.335
            assert integral_trapesium(lambda x: 3, 0, 2, 5) == 6.0
            """,
            "Jumlahkan setengah tinggi ujung dan seluruh tinggi titik dalam lalu kalikan lebar potongan.",
            """
            def integral_trapesium(f, a, b, n):
                h = (b - a) / n
                total = (f(a) + f(b)) / 2
                for i in range(1, n):
                    total += f(a + i * h)
                return round(total * h, 4)
            """,
        ),
        E(
            "A4-04-1-ex3",
            "sedang",
            """
            Tulis fungsi `konstanta_normalisasi(f, a, b, n=10000)` yang mengembalikan konstanta `c` sehingga `c * f(x)` memiliki luas satu pada `[a, b]`, memakai aturan titik tengah dengan `n` potongan. Bulatkan 4 desimal.
            """,
            """
            def konstanta_normalisasi(f, a, b, n=10000):
                # TODO: implementasikan
                pass
            """,
            """
            assert konstanta_normalisasi(lambda x: x, 0, 2) == 0.5
            assert konstanta_normalisasi(lambda x: x * x, 0, 3) == 0.1111
            assert konstanta_normalisasi(lambda x: 1, 0, 4) == 0.25
            assert konstanta_normalisasi(lambda x: 2 * x, 0, 1) == 1.0
            """,
            "Hitung luas dengan titik tengah lalu ambil kebalikannya.",
            """
            def konstanta_normalisasi(f, a, b, n=10000):
                h = (b - a) / n
                luas = sum(f(a + (i + 0.5) * h) for i in range(n)) * h
                return round(1 / luas, 4)
            """,
        ),
        E(
            "A4-04-1-ex4",
            "menantang",
            """
            Tulis fungsi `peluang_rentang_pdf(f, a, b, n=20000)` yang mengembalikan `P(a <= X <= b)` dari PDF `f` memakai aturan titik tengah, dibulatkan 4 desimal.
            """,
            """
            def peluang_rentang_pdf(f, a, b, n=20000):
                # TODO: implementasikan
                pass
            """,
            """
            assert peluang_rentang_pdf(lambda x: 2 * x, 0.25, 0.75) == 0.5
            assert peluang_rentang_pdf(lambda x: 0.1, 2, 5) == 0.3
            assert peluang_rentang_pdf(lambda x: 3 * x * x, 0, 0.5) == 0.125
            assert peluang_rentang_pdf(lambda x: 2 * x, 0, 1) == 1.0
            assert peluang_rentang_pdf(lambda x: 2 * x, 0.5, 0.5) == 0.0
            """,
            "Bagi interval menjadi potongan kecil dan jumlahkan tinggi titik tengah kali lebar.",
            """
            def peluang_rentang_pdf(f, a, b, n=20000):
                h = (b - a) / n
                return round(sum(f(a + (i + 0.5) * h) for i in range(n)) * h, 4)
            """,
        ),
    ],
    [
        M("Menganggap nilai PDF sebagai peluang titik.", "Peluang adalah luas pada interval."),
        M("Mengira PDF tidak boleh lebih dari satu.", "Yang harus satu adalah luas total."),
        M("Peduli batas inklusif pada variabel kontinu.", "Titik tunggal berpeluang nol."),
    ],
    [
        Q("Peluang pada variabel kontinu adalah?", ["Nilai PDF", "Luas di bawah PDF", "Tinggi maksimum", "Rata-rata"], 1, "Integral PDF.", hint="Luas."),
        Q("P(X = a) pada variabel kontinu?", ["1", "0,5", "0", "Tak tentu"], 2, "Luas lebar nol.", hint="Titik."),
        Q("Luas total di bawah PDF?", ["0", "1", "Bergantung", "Tak hingga"], 1, "Peluang total.", hint="Satu."),
        Q("Bolehkah PDF bernilai lebih dari 1?", ["Tidak", "Ya", "Hanya seragam", "Hanya normal"], 1, "Ia kepadatan, bukan peluang.", hint="Rentang sempit."),
        Q("Aturan titik tengah mendekati integral dengan?", ["Mengurutkan", "Menjumlahkan persegi panjang", "Mengalikan", "Membagi"], 1, "Tinggi di tengah kali lebar.", hint="Potongan."),
    ],
    [
        "PDF adalah kepadatan dan peluang adalah luas di bawahnya.",
        "Titik tunggal berpeluang nol.",
        "Integral numerik menjumlahkan persegi panjang atau trapesium kecil.",
        "Normalisasi membagi dengan luas agar totalnya satu.",
    ],
    [],
)

l2 = lesson(
    "A4-04-2",
    "CDF kontinu, kuantil, dan sampling invers",
    35,
    [
        "Menghitung CDF dari PDF dan sebaliknya",
        "Menghitung CDF dan kuantil distribusi eksponensial dan seragam",
        "Memakai sampling transformasi invers",
        "Mengecek model dengan simulasi",
    ],
    [
        T("""
        ## CDF dan PDF saling terkait

        Untuk variabel kontinu, CDF tetap `F(x) = P(X <= x)`, yaitu luas di bawah PDF dari minus tak hingga sampai `x`. Sebaliknya, PDF adalah turunan CDF: `f(x) = F'(x)`. Kenaikan CDF yang curam berarti kepadatan tinggi di sana, dan CDF yang mendatar berarti kepadatan rendah.

        Berbeda dengan kasus diskrit, CDF kontinu mulus tanpa lompatan. Ia naik dari nol ke satu secara kontinu. Kita tetap memakainya untuk peluang interval: `P(a < X <= b) = F(b) - F(a)`.
        """),
        T("""
        ## Distribusi eksponensial

        Distribusi **eksponensial** memodelkan waktu tunggu sampai kejadian acak berikutnya, seperti waktu antar kedatangan pelanggan atau waktu hidup komponen. PDF-nya `f(x) = lambda * e^(-lambda x)` untuk `x >= 0`, dengan `lambda` laju kejadian. CDF-nya `F(x) = 1 - e^(-lambda x)`.

        Rata-rata waktu tunggu adalah `1/lambda`. Bila laju `0,5` per menit, rata-rata tunggu dua menit. Peluang menunggu lebih lama dari `x` adalah `e^(-lambda x)`, ekor yang meluruh secara eksponensial.
        """),
        C(
            """
            import math

            lam = 0.5
            print(round(1 - math.exp(-lam * 2), 4), round(math.exp(-lam * 4), 4), round(math.log(2) / lam, 4))
            """,
            """
            0.6321 0.1353 1.3863
            """,
            """
            Peluang menunggu paling lama dua menit adalah sekitar enam puluh tiga persen. Peluang menunggu lebih dari empat menit sekitar tiga belas persen, dan median waktu tunggu lebih pendek daripada rata-rata dua menit.
            """,
            filename="eksponensial.py",
        ),
        T("""
        ## Kuantil

        Kuantil adalah invers CDF: `Q(q) = F^(-1)(q)`, nilai `x` dengan `F(x) = q`. Untuk seragam `[a, b]`, `F(x) = (x - a)/(b - a)` sehingga `Q(q) = a + q (b - a)`. Untuk eksponensial, memecahkan `1 - e^(-lambda x) = q` menghasilkan `Q(q) = -ln(1 - q) / lambda`.

        Median adalah `Q(0,5)`. Pada eksponensial median `ln(2)/lambda` selalu lebih kecil daripada rata-rata `1/lambda`, ciri khas distribusi yang miring ke kanan: sedikit nilai yang sangat besar menarik rata-rata ke atas.
        """),
        C(
            """
            a, b = 2, 10
            print(a + 0.5 * (b - a), a + 0.9 * (b - a))
            """,
            """
            6.0 9.2
            """,
            """
            Median seragam dua sampai sepuluh adalah tepat di tengah dan kuantil sembilan puluh persen berada di sembilan koma dua.
            """,
            filename="kuantil_seragam.py",
        ),
        T("""
        ## Sampling transformasi invers

        Bila `U` seragam pada `[0, 1]`, maka `Q(U)` memiliki distribusi dengan CDF `F`. Inilah **transformasi invers**: cara umum menghasilkan sampel dari distribusi apa pun asalkan kita bisa menghitung kuantilnya. Komputer hanya menyediakan bilangan seragam, dan teknik ini mengubahnya menjadi distribusi lain.

        Alasannya intuitif. Pilih peluang `u` secara seragam lalu cari nilai yang memiliki peluang kumulatif `u`. Daerah dengan kepadatan tinggi memiliki CDF curam, sehingga banyak nilai `u` jatuh di sana dan nilai di daerah itu lebih sering terpilih.
        """),
        C(
            """
            import math

            us = [0.1, 0.5, 0.9]
            print([round(-math.log(1 - u) / 0.5, 4) for u in us])
            """,
            """
            [0.2107, 1.3863, 4.6052]
            """,
            """
            Tiga nilai seragam yang berbeda dipetakan menjadi waktu tunggu eksponensial yang makin panjang.
            """,
            filename="sampling_invers.py",
        ),
        T("""
        ## Memeriksa dengan simulasi

        Simulasi adalah cara terbaik memeriksa rumus. Ambil banyak sampel dengan transformasi invers dan bandingkan statistiknya dengan teori. Rata-rata sampel eksponensial dengan `lambda = 0,5` seharusnya mendekati dua, dan proporsi sampel di bawah dua mendekati `0,6321`.

        Kebiasaan memeriksa teori dengan simulasi dan simulasi dengan teori akan sangat berguna di modul Monte Carlo. Bila keduanya cocok, kita yakin bahwa rumus dan kode benar. Bila tidak cocok, ada bug di salah satunya dan kita mendapat petunjuk untuk mencarinya.
        """),
        C(
            """
            import math
            import random

            random.seed(7)
            lam = 0.5
            xs = [-math.log(1 - random.random()) / lam for _ in range(20000)]
            print(abs(sum(xs) / len(xs) - 2) < 0.1)
            print(abs(sum(1 for x in xs if x <= 2) / len(xs) - 0.6321) < 0.02)
            """,
            """
            True
            True
            """,
            """
            Rata-rata sampel mendekati dua dan proporsi di bawah dua mendekati nilai CDF teoretis.
            """,
            filename="simulasi_eksponensial.py",
        ),
        T("""
        ## PDF dari CDF secara numerik

        Karena PDF adalah turunan CDF, kita bisa menaksir kepadatan di suatu titik dengan selisih berhingga: `(F(x + e) - F(x - e)) / (2e)` untuk `e` kecil. Pada eksponensial dengan `lambda = 0,5`, kepadatan di `x = 1` adalah `0,5 * e^(-0,5)`, sekitar `0,3033`, dan selisih berhingga memberi angka yang sama sampai empat desimal.
        """),
        C(
            """
            import math

            F = lambda x: 1 - math.exp(-0.5 * x)
            e = 0.0001
            print(round(0.5 * math.exp(-0.5), 4), round((F(1 + e) - F(1 - e)) / (2 * e), 4))
            """,
            """
            0.3033 0.3033
            """,
            """
            Kepadatan teoretis dan taksiran turunan CDF memberi nilai yang sama.
            """,
            filename="pdf_dari_cdf.py",
        ),
        T("""
        ## Sifat tanpa ingatan

        Eksponensial punya sifat unik: tanpa ingatan. Peluang menunggu paling tidak sepuluh menit lagi, setelah kamu sudah menunggu lima menit, sama dengan peluang menunggu sepuluh menit dari awal. Waktu yang sudah berlalu tidak memberi informasi tentang sisa waktu tunggu.

        Sifat ini cocok untuk kejadian yang benar-benar acak seperti peluruhan radioaktif, tetapi tidak untuk komponen yang aus. Mesin yang makin tua lebih mungkin rusak, sehingga eksponensial salah dipakai di sana dan distribusi seperti Weibull lebih tepat. Selalu tanyakan apakah asumsi tanpa ingatan masuk akal.
        """),
        T("""
        ## Memilih model waktu tunggu

        Untuk data nyata, taksir `lambda` dengan satu per rata-rata sampel, lalu bandingkan CDF teoretis dengan CDF empiris. Bila kurvanya berimpit, model eksponensial layak dipakai. Bila CDF empiris naik lebih lambat di awal lalu lebih cepat, data punya penuaan dan model lain diperlukan.
        """),
        E(
            "A4-04-2-ex1",
            "mudah",
            """
            Tulis fungsi `cdf_eksponensial(x, lam)` yang mengembalikan `1 - exp(-lam * x)` dibulatkan 4 desimal, dan `0.0` untuk `x < 0`.
            """,
            """
            import math

            def cdf_eksponensial(x, lam):
                # TODO: implementasikan
                pass
            """,
            """
            assert cdf_eksponensial(2, 0.5) == 0.6321
            assert cdf_eksponensial(0, 1) == 0.0
            assert cdf_eksponensial(-1, 1) == 0.0
            assert cdf_eksponensial(1, 1) == 0.6321
            assert cdf_eksponensial(3, 0.1) == 0.2592
            """,
            "Kembalikan nol untuk x negatif dan pakai rumus satu dikurangi eksponensial untuk lainnya.",
            """
            import math

            def cdf_eksponensial(x, lam):
                if x < 0:
                    return 0.0
                return round(1 - math.exp(-lam * x), 4)
            """,
        ),
        E(
            "A4-04-2-ex2",
            "sedang",
            """
            Tulis fungsi `kuantil_eksponensial(q, lam)` yang mengembalikan `-ln(1 - q) / lam` dibulatkan 4 desimal. Hindari `-0.0`.
            """,
            """
            import math

            def kuantil_eksponensial(q, lam):
                # TODO: implementasikan
                pass
            """,
            """
            assert kuantil_eksponensial(0.5, 0.5) == 1.3863
            assert kuantil_eksponensial(0.5, 1) == 0.6931
            assert kuantil_eksponensial(0.9, 1) == 2.3026
            assert kuantil_eksponensial(0, 2) == 0.0
            assert kuantil_eksponensial(0.99, 0.1) == 46.0517
            """,
            "Balikkan CDF eksponensial dengan logaritma natural.",
            """
            import math

            def kuantil_eksponensial(q, lam):
                return round(-math.log(1 - q) / lam, 4) + 0.0
            """,
        ),
        E(
            "A4-04-2-ex3",
            "sedang",
            """
            Tulis fungsi `kuantil_seragam(q, a, b)` yang mengembalikan kuantil `q` distribusi seragam `[a, b]`, dibulatkan 4 desimal.
            """,
            """
            def kuantil_seragam(q, a, b):
                # TODO: implementasikan
                pass
            """,
            """
            assert kuantil_seragam(0.5, 2, 10) == 6.0
            assert kuantil_seragam(0.9, 2, 10) == 9.2
            assert kuantil_seragam(0, 3, 4) == 3.0
            assert kuantil_seragam(1, 3, 4) == 4.0
            """,
            "Mulai dari a lalu tambahkan q kali lebar rentang.",
            """
            def kuantil_seragam(q, a, b):
                return round(a + q * (b - a), 4)
            """,
        ),
        E(
            "A4-04-2-ex4",
            "menantang",
            """
            Tulis fungsi `sampel_invers(us, lam)` yang mengubah list bilangan seragam `us` pada `[0, 1)` menjadi list sampel eksponensial dengan transformasi invers, dibulatkan 4 desimal. Hindari `-0.0`.
            """,
            """
            import math

            def sampel_invers(us, lam):
                # TODO: implementasikan
                pass
            """,
            """
            assert sampel_invers([0.1, 0.5, 0.9], 0.5) == [0.2107, 1.3863, 4.6052]
            assert sampel_invers([0], 1) == [0.0]
            assert sampel_invers([0.5], 2) == [0.3466]
            assert sampel_invers([], 1) == []
            """,
            "Terapkan kuantil eksponensial pada tiap bilangan seragam.",
            """
            import math

            def sampel_invers(us, lam):
                return [round(-math.log(1 - u) / lam, 4) + 0.0 for u in us]
            """,
        ),
    ],
    [
        M("Mengira CDF kontinu memiliki lompatan.", "CDF kontinu mulus."),
        M("Menyamakan median dengan rata-rata pada distribusi miring.", "Median eksponensial lebih kecil dari rata-rata."),
        M("Memakai 1 - u salah pada sampling invers.", "Kuantil dihitung dari F invers."),
    ],
    [
        Q("PDF adalah apa dari CDF?", ["Integral", "Turunan", "Kuadrat", "Akar"], 1, "f = F'.", hint="Kemiringan."),
        Q("CDF eksponensial?", ["1 - e^(-lambda x)", "e^(-lambda x)", "lambda x", "x / lambda"], 0, "Peluang menunggu paling lama x.", hint="Satu kurang ekor."),
        Q("Median eksponensial?", ["1/lambda", "ln 2 / lambda", "2/lambda", "lambda"], 1, "Q(0,5).", hint="Log dua."),
        Q("Transformasi invers memakai?", ["U seragam dan kuantil", "Rata-rata", "Median saja", "Histogram"], 0, "Q(U) berdistribusi F.", hint="Seragam."),
        Q("Eksponensial miring ke?", ["Kiri", "Kanan", "Tidak miring", "Dua arah"], 1, "Ekor panjang di kanan.", hint="Rata-rata di atas median."),
    ],
    [
        "PDF adalah turunan CDF dan CDF adalah integral PDF.",
        "Kuantil adalah invers CDF.",
        "Transformasi invers mengubah bilangan seragam menjadi distribusi lain.",
        "Simulasi memeriksa kecocokan teori dan kode.",
    ],
    [],
)

l3 = lesson(
    "A4-04-3",
    "Estimasi kepadatan dari data",
    35,
    [
        "Membuat histogram berskala kepadatan",
        "Memakai kernel Gaussian untuk estimasi kepadatan",
        "Menjelaskan efek lebar jendela dan aturan Scott",
        "Memeriksa bahwa estimasi kepadatan berluas satu",
    ],
    [
        T("""
        ## Dari data ke kepadatan

        Dalam praktik kita tidak diberi rumus PDF. Kita hanya punya sampel, misalnya tinggi seribu orang, dan ingin memperkirakan bentuk distribusinya. Estimasi kepadatan adalah proses membuat taksiran PDF dari data. Dua alat utamanya adalah histogram dan estimasi kepadatan kernel atau KDE.

        Tujuannya bukan sekadar menggambar. Taksiran kepadatan membantu melihat apakah data tunggal puncak atau banyak puncak, simetris atau miring, dan memiliki ekor panjang atau tidak. Informasi ini menentukan model dan transformasi yang cocok.
        """),
        T("""
        ## Histogram sebagai kepadatan

        Histogram membagi rentang menjadi kotak dan menghitung berapa data jatuh di tiap kotak. Agar tinggi batang menjadi kepadatan, bagi hitungan dengan `n * lebar`: `tinggi = hitungan / (n * lebar)`. Maka luas semua batang berjumlah satu, sama seperti PDF.

        Tanpa normalisasi, tinggi hanyalah hitungan dan tidak bisa dibandingkan antar dataset berbeda ukuran atau antar lebar kotak berbeda. Opsi `density=True` pada `numpy.histogram` dan `matplotlib` melakukan normalisasi itu.
        """),
        C(
            """
            import numpy as np

            data = [1, 2, 2, 3, 3, 3, 4, 4, 5]
            tepi = [0, 2, 4, 6]
            h, _ = np.histogram(data, bins=tepi, density=True)
            print(np.round(h, 4).tolist())
            print(round(float((h * np.diff(tepi)).sum()), 4))
            """,
            """
            [0.0556, 0.2778, 0.1667]
            1.0
            """,
            """
            Tinggi batang adalah hitungan dibagi sembilan kali dua, dan luas seluruh batang tepat satu.
            """,
            filename="histogram_kepadatan.py",
        ),
        T("""
        ## Masalah histogram

        Histogram bergantung pada pilihan kotak: lebar dan posisi awal. Lebar terlalu kecil menghasilkan batang bergerigi yang mengikuti derau. Lebar terlalu besar menghaluskan sampai ciri penting hilang. Menggeser tepi kotak sedikit pun bisa mengubah kesan bentuk data.

        Selain itu histogram tidak mulus: kepadatan melompat di tiap tepi. Padahal banyak distribusi yang kita yakini mulus. KDE menjawab masalah ini dengan menaruh gundukan mulus pada setiap titik data dan menjumlahkannya.
        """),
        T("""
        ## Estimasi kepadatan kernel

        Untuk tiap titik data `xi`, letakkan sebuah kurva lonceng kecil, kernel, yang berpusat di `xi`. KDE adalah rata-rata semua lonceng itu: `f(x) = 1/(n h) * jumlah K((x - xi)/h)`. Dengan kernel Gaussian, `K(u) = e^(-u^2/2) / sqrt(2 pi)`.

        Parameter `h` disebut **lebar jendela** atau bandwidth. Nilai `h` kecil memberi lonceng sempit dan hasil bergerigi, dan `h` besar memberi lonceng lebar dan hasil yang terlalu halus. Memilih `h` adalah inti penyetelan KDE, seperti memilih lebar kotak pada histogram.
        """),
        C(
            """
            import math

            def phi(u):
                return math.exp(-u * u / 2) / math.sqrt(2 * math.pi)

            def kde(data, x, h):
                return sum(phi((x - v) / h) for v in data) / (len(data) * h)

            d = [1, 2, 3]
            print(round(kde(d, 2, 1), 4), round(kde(d, 2, 0.1), 4), round(kde(d, 2, 3), 4))
            """,
            """
            0.2943 1.3298 0.1282
            """,
            """
            Jendela sempit membuat lonceng menjulang di titik data. Jendela lebar menyebarkan massa sehingga puncaknya rendah.
            """,
            filename="kde.py",
        ),
        T("""
        ## Memilih lebar jendela

        Ada aturan praktis untuk data kira-kira berbentuk lonceng. **Aturan Scott** memakai `h = 1,06 * s * n^(-1/5)`, dengan `s` simpangan baku sampel dan `n` banyaknya data. Lebar jendela mengecil lambat seiring bertambahnya data, karena data lebih banyak memungkinkan detail lebih halus.

        Aturan ini cocok untuk distribusi yang mendekati normal. Untuk data dengan beberapa puncak, lebar dari aturan ini cenderung terlalu besar dan meratakan puncak. Selalu bandingkan beberapa nilai `h` secara visual dan, bila perlu, pilih dengan validasi silang.
        """),
        C(
            """
            import statistics

            d = [1, 2, 3]
            h = 1.06 * statistics.stdev(d) * len(d) ** (-0.2)
            print(round(h, 4))
            """,
            """
            0.8509
            """,
            """
            Untuk tiga data dengan simpangan baku satu, aturan Scott memberi lebar jendela sekitar nol koma delapan lima.
            """,
            filename="aturan_scott.py",
        ),
        T("""
        ## KDE tetap kepadatan

        KDE adalah rata-rata dari kepadatan yang masing-masing berluas satu, sehingga hasilnya juga berluas satu. Kita bisa memeriksa ini secara numerik dengan menjumlahkan nilai pada grid halus dikali lebar grid. Pemeriksaan ini adalah cara cepat menangkap kesalahan implementasi, misalnya lupa membagi dengan `h`.

        Karena KDE kepadatan valid, kita bisa mengintegralkannya untuk peluang interval dan menggambar kurvanya di atas histogram untuk membandingkan model dengan data.
        """),
        C(
            """
            import math

            def phi(u):
                return math.exp(-u * u / 2) / math.sqrt(2 * math.pi)

            def kde(data, x, h):
                return sum(phi((x - v) / h) for v in data) / (len(data) * h)

            grid = [i * 0.01 for i in range(-1000, 1301)]
            luas = sum(kde([1, 2, 3], x, 1) * 0.01 for x in grid)
            print(round(luas, 3))
            """,
            """
            1.0
            """,
            """
            Luas di bawah kurva KDE pada grid yang cukup lebar adalah satu.
            """,
            filename="kde_luas.py",
        ),
        K(
            "tip",
            """
            Selalu plot histogram berskala kepadatan bersama KDE. Bila keduanya menceritakan bentuk yang berbeda secara mencolok, periksa lebar kotak dan lebar jendela.
            """,
            title="Dua pandangan",
        ),
        T("""
        ## Kapan memilih histogram atau KDE

        Histogram sederhana, cepat, dan mudah dijelaskan kepada pemangku kepentingan non-teknis. Ia jujur menampilkan hitungan dan cocok untuk data diskrit atau data dalam jumlah sangat besar. KDE menghasilkan kurva mulus yang enak dilihat dan berguna untuk membandingkan beberapa kelompok dalam satu gambar.

        Namun KDE dapat menyesatkan di dekat batas alami. Data yang tidak boleh negatif, seperti durasi, akan menghasilkan KDE yang bocor ke sisi negatif. Pada kasus seperti itu, pakai transformasi log atau koreksi batas sebelum mengestimasi kepadatan.
        """),
        T("""
        ## Estimasi kepadatan dalam model

        Estimasi kepadatan bukan hanya alat gambar. Deteksi anomali memakai kepadatan rendah sebagai tanda data tidak biasa. Klasifier generatif menaksir kepadatan tiap kelas lalu memilih kelas yang paling mungkin. Simulasi memakai kepadatan hasil estimasi untuk mengambil sampel baru yang mirip data asli.

        Karena itu kemampuan menaksir dan memeriksa kepadatan, terutama menjaga luasnya satu dan memilih lebar jendela dengan wajar, adalah keterampilan dasar yang akan terus terpakai.
        """),
        E(
            "A4-04-3-ex1",
            "mudah",
            """
            Tulis fungsi `kepadatan_histogram(data, tepi)` yang mengembalikan list kepadatan tiap kotak (`hitungan / (n * lebar)`) dibulatkan 4 desimal. Kotak mencakup tepi kiri tetapi tidak tepi kanan, kecuali kotak terakhir yang mencakup keduanya.
            """,
            """
            def kepadatan_histogram(data, tepi):
                # TODO: implementasikan
                pass
            """,
            """
            d = [1, 2, 2, 3, 3, 3, 4, 4, 5]
            assert kepadatan_histogram(d, [0, 2, 4, 6]) == [0.0556, 0.2778, 0.1667]
            assert kepadatan_histogram(d, [1, 5]) == [0.25]
            assert kepadatan_histogram(d, [0, 3, 6]) == [0.1111, 0.2222]
            assert kepadatan_histogram([2], [0, 4]) == [0.25]
            """,
            "Hitung data per kotak lalu bagi dengan jumlah data kali lebar kotak.",
            """
            def kepadatan_histogram(data, tepi):
                n = len(data)
                hasil = []
                for i in range(len(tepi) - 1):
                    a, b = tepi[i], tepi[i + 1]
                    terakhir = i == len(tepi) - 2
                    c = sum(1 for v in data if a <= v < b or (terakhir and v == b))
                    hasil.append(round(c / (n * (b - a)), 4))
                return hasil
            """,
        ),
        E(
            "A4-04-3-ex2",
            "sedang",
            """
            Tulis fungsi `kernel_gauss(u)` yang mengembalikan `exp(-u^2 / 2) / sqrt(2 * pi)` dibulatkan 4 desimal.
            """,
            """
            import math

            def kernel_gauss(u):
                # TODO: implementasikan
                pass
            """,
            """
            assert kernel_gauss(0) == 0.3989
            assert kernel_gauss(1) == 0.242
            assert kernel_gauss(-1) == 0.242
            assert kernel_gauss(2) == 0.054
            assert kernel_gauss(3) == 0.0044
            """,
            "Pakai math.exp dan math.sqrt dengan konstanta math.pi.",
            """
            import math

            def kernel_gauss(u):
                return round(math.exp(-u * u / 2) / math.sqrt(2 * math.pi), 4)
            """,
        ),
        E(
            "A4-04-3-ex3",
            "sedang",
            """
            Tulis fungsi `kde(data, x, h)` yang mengembalikan estimasi kepadatan kernel Gaussian di titik `x` dengan lebar jendela `h`, dibulatkan 4 desimal.
            """,
            """
            import math

            def kde(data, x, h):
                # TODO: implementasikan
                pass
            """,
            """
            assert kde([1, 2, 3], 2, 1) == 0.2943
            assert kde([1, 2, 3], 2, 0.1) == 1.3298
            assert kde([5], 5, 1) == 0.3989
            assert kde([0], 10, 1) == 0.0
            assert kde([1, 2, 3], 2, 3) == 0.1282
            """,
            "Jumlahkan kernel pada jarak terskala lalu bagi dengan n kali h.",
            """
            import math

            def kde(data, x, h):
                def phi(u):
                    return math.exp(-u * u / 2) / math.sqrt(2 * math.pi)
                return round(sum(phi((x - v) / h) for v in data) / (len(data) * h), 4)
            """,
        ),
        E(
            "A4-04-3-ex4",
            "menantang",
            """
            Tulis fungsi `aturan_scott(data)` yang mengembalikan lebar jendela `1.06 * s * n ** (-1/5)` dengan `s` simpangan baku sampel (pembagi n minus 1), dibulatkan 4 desimal.
            """,
            """
            import statistics

            def aturan_scott(data):
                # TODO: implementasikan
                pass
            """,
            """
            assert aturan_scott([1, 2, 3]) == 0.8509
            assert aturan_scott([10, 20, 30, 40, 50]) == 12.1474
            assert aturan_scott([5, 5, 5]) == 0.0
            """,
            "Gunakan statistics.stdev dan pangkat negatif satu per lima dari n.",
            """
            import statistics

            def aturan_scott(data):
                return round(1.06 * statistics.stdev(data) * len(data) ** (-0.2), 4)
            """,
        ),
    ],
    [
        M("Memakai hitungan sebagai tinggi histogram saat membandingkan.", "Normalisasi ke kepadatan."),
        M("Memakai satu lebar jendela tanpa dicek.", "Bandingkan beberapa nilai h."),
        M("Lupa membagi dengan h pada KDE.", "Cek luas total sama dengan satu."),
    ],
    [
        Q("Tinggi histogram kepadatan?", ["hitungan", "hitungan / (n lebar)", "n / lebar", "lebar"], 1, "Luas total satu.", hint="Normalisasi."),
        Q("KDE adalah?", ["Rata-rata kernel di tiap data", "Median", "Regresi", "Korelasi"], 0, "Gundukan mulus dijumlahkan.", hint="Lonceng."),
        Q("h kecil menghasilkan?", ["Halus", "Bergerigi", "Datar", "Nol"], 1, "Mengikuti derau.", hint="Sempit."),
        Q("Aturan Scott memakai?", ["Median", "Simpangan baku dan n", "Maksimum", "Modus"], 1, "1,06 s n pangkat -1/5.", hint="Skala data."),
        Q("Luas di bawah KDE?", ["0", "1", "n", "h"], 1, "Rata-rata kepadatan.", hint="Kepadatan valid."),
    ],
    [
        "Histogram kepadatan membagi hitungan dengan n kali lebar.",
        "KDE menjumlahkan kernel mulus di tiap titik data.",
        "Lebar jendela mengatur keseimbangan halus dan bergerigi.",
        "Estimasi kepadatan yang valid berluas satu.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perhitungan yang cukup jelas dalam teks.", "brief": []}

write_module(
    "A4",
    4,
    "Variabel acak kontinu",
    105,
    [
        "Memahami PDF sebagai kepadatan dan peluang sebagai luas",
        "Memakai CDF, kuantil, dan sampling invers",
        "Mengestimasi kepadatan dari data",
    ],
    [l1, l2, l3],
    video,
    REF,
)
