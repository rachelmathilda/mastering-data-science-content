import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

l1 = lesson(
    "A4-07-1",
    "Hukum bilangan besar",
    35,
    [
        "Menjelaskan mengapa rata-rata sampel mendekati ekspektasi",
        "Menghitung rata-rata berjalan dan melihat konvergensinya",
        "Memakai ketaksamaan Chebyshev untuk rata-rata sampel",
        "Menentukan ukuran sampel dari batas Chebyshev",
    ],
    [
        T("""
        ## Dari satu percobaan ke banyak

        Satu lemparan koin sama sekali tidak bisa diprediksi. Seribu lemparan, sebaliknya, hampir pasti menghasilkan sekitar separuh kepala. Keteraturan yang muncul dari kekacauan inilah isi **hukum bilangan besar**: rata-rata `n` pengamatan independen dengan distribusi sama mendekati ekspektasi sebenarnya ketika `n` membesar.

        Hukum ini adalah jembatan antara teori dan data. Ia membenarkan praktik menaksir ekspektasi dengan rata-rata sampel, menaksir peluang dengan frekuensi relatif, dan memakai simulasi untuk menghitung besaran yang sulit dihitung secara analitik.
        """),
        T("""
        ## Pernyataan yang tepat

        Bentuk lemahnya menyatakan untuk setiap toleransi `epsilon` positif, peluang rata-rata sampel menyimpang lebih dari `epsilon` dari ekspektasi menuju nol bila `n` menuju tak hingga. Bentuk kuatnya menyatakan bahwa dengan peluang satu, barisan rata-rata konvergen ke ekspektasi.

        Syarat utamanya: pengamatan independen, berdistribusi sama, dan ekspektasi ada dan berhingga. Syarat terakhir penting. Distribusi Cauchy tidak memiliki ekspektasi berhingga, dan rata-rata sampelnya tidak pernah menstabil seberapa pun besar `n`. Asumsi bukan formalitas.
        """),
        C(
            """
            import random

            random.seed(11)
            n = 10000
            kepala = sum(random.random() < 0.5 for _ in range(n))
            print(abs(kepala / n - 0.5) < 0.03)
            """,
            """
            True
            """,
            """
            Proporsi kepala dari sepuluh ribu lemparan berada sangat dekat dengan setengah, sesuai hukum bilangan besar.
            """,
            filename="lln_koin.py",
        ),
        T("""
        ## Rata-rata berjalan

        Cara melihat hukum bilangan besar adalah menghitung rata-rata berjalan: rata-rata dari `k` pengamatan pertama untuk `k = 1, 2, 3, ...`. Pada awalnya rata-rata ini berfluktuasi besar karena sedikit data. Seiring bertambahnya data, fluktuasi mengecil dan kurva menempel pada ekspektasi.

        Menggambar rata-rata berjalan adalah diagnosis simulasi yang berguna: bila kurvanya belum mendatar, simulasi belum cukup panjang untuk dipercaya. Kebiasaan ini akan dipakai di pelajaran Monte Carlo.
        """),
        C(
            """
            data = [1, 2, 3, 4, 5]
            total = 0
            hasil = []
            for k, x in enumerate(data, start=1):
                total += x
                hasil.append(round(total / k, 4))
            print(hasil)
            """,
            """
            [1.0, 1.5, 2.0, 2.5, 3.0]
            """,
            """
            Rata-rata berjalan dihitung dengan menjumlahkan bertahap dan membagi dengan banyak data sejauh ini.
            """,
            filename="rata_berjalan.py",
        ),
        T("""
        ## Kesalahan penafsiran

        Hukum bilangan besar sering disalahpahami sebagai hukum rata-rata yang memaksa keseimbangan. Setelah lima kepala berturut-turut, lemparan berikutnya tetap berpeluang setengah. Koin tidak punya ingatan untuk mengimbangi. Yang terjadi adalah ketidakseimbangan awal **diencerkan** oleh banyaknya lemparan berikutnya, bukan dikoreksi.

        Selisih mutlak antara jumlah kepala dan jumlah ekor justru cenderung membesar seperti akar `n`. Yang mengecil adalah selisih proporsi. Membedakan keduanya mencegah kekeliruan gambler: menganggap kekalahan beruntun berarti kemenangan segera datang.
        """),
        T("""
        ## Ketaksamaan Chebyshev untuk rata-rata

        Rata-rata `n` pengamatan independen dengan varians `sigma^2` memiliki varians `sigma^2 / n`. Menerapkan Chebyshev pada rata-rata ini memberi `P(|rata-rata - mu| >= epsilon) <= sigma^2 / (n * epsilon^2)`. Batas ini turun sebagai satu per `n`, menjamin konvergensi tanpa asumsi bentuk distribusi.

        Batas Chebyshev longgar, tetapi universal. Ia sudah cukup untuk membuktikan hukum lemah dan untuk memberi perkiraan kasar ukuran sampel. Untuk batas yang lebih ketat kita pakai pendekatan normal dari teorema limit pusat di pelajaran berikut.
        """),
        C(
            """
            var = 35 / 12
            n = 100
            eps = 0.5
            print(round(var / (n * eps ** 2), 4))
            """,
            """
            0.1167
            """,
            """
            Untuk rata-rata seratus lemparan dadu, peluang menyimpang lebih dari setengah dari tiga koma lima paling banyak sekitar sebelas persen.
            """,
            filename="chebyshev_rata.py",
        ),
        T("""
        ## Memeriksa varians rata-rata

        Klaim bahwa varians rata-rata sampel adalah `sigma^2 / n` dapat diperiksa dengan simulasi. Ambil banyak sampel berukuran `n`, hitung rata-rata tiap sampel, lalu hitung varians dari rata-rata itu. Hasilnya harus mendekati `sigma^2 / n`.

        Untuk dadu dengan `n = 25`, variansnya `2,9167 / 25`, sekitar `0,1167`. Simulasi seperti ini memperlihatkan secara empiris mengapa data lebih banyak memberi taksiran yang lebih presisi, dengan simpangan baku yang turun sebagai satu per akar `n`.
        """),
        C(
            """
            import random
            import statistics

            r = random.Random(5)
            n = 25
            rata = [sum(r.randint(1, 6) for _ in range(n)) / n for _ in range(5000)]
            print(abs(statistics.pvariance(rata) - 35 / 12 / n) < 0.01)
            """,
            """
            True
            """,
            """
            Varians rata-rata dua puluh lima dadu hasil simulasi mendekati nilai teoretis sigma kuadrat per n.
            """,
            filename="varians_rata.py",
        ),
        K(
            "warn",
            """
            Hukum bilangan besar tidak berarti hasil acak akan menyeimbangkan diri. Ia hanya menyatakan proporsi dan rata-rata menstabil, bukan bahwa selisih mutlak mengecil.
            """,
            title="Kekeliruan gambler",
        ),
        T("""
        ## Simulasi Monte Carlo sebagai terapan

        Hukum bilangan besar adalah dasar metode Monte Carlo. Untuk menaksir besaran yang sulit dihitung, rancang percobaan acak yang ekspektasinya sama dengan besaran itu, ulangi banyak kali, dan ambil rata-ratanya. Peluang suatu kejadian ditaksir dengan proporsi kemunculannya dalam simulasi.

        Akurasi bergantung pada banyaknya ulangan lewat galat baku `sigma / sqrt(n)`. Untuk satu angka desimal tambahan ketelitian kita butuh seratus kali lebih banyak simulasi, sehingga Monte Carlo cocok untuk ketelitian sedang dan masalah berdimensi tinggi, bukan untuk presisi ekstrem pada masalah sederhana.
        """),
        T("""
        ## Ketika hukum ini gagal

        Selain distribusi tanpa ekspektasi seperti Cauchy, hukum bilangan besar juga bisa terasa gagal secara praktis bila distribusinya berekor sangat tebal. Ekspektasi ada tetapi kejadian ekstrem yang jarang menyumbang sangat besar, sehingga konvergensi memerlukan sampel yang jauh lebih banyak daripada biasanya. Kerugian keuangan dan ukuran bencana alam sering berperilaku begini.

        Pelajarannya: selalu periksa bentuk ekor data sebelum percaya rata-rata sampel. Satu nilai ekstrem dapat menggeser rata-rata sedemikian besar sehingga median atau rata-rata terpangkas lebih jujur.
        """),
        E(
            "A4-07-1-ex1",
            "mudah",
            """
            Tulis fungsi `rata_rata_berjalan(data)` yang mengembalikan list rata-rata dari `k` data pertama untuk tiap `k`, dibulatkan 4 desimal.
            """,
            """
            def rata_rata_berjalan(data):
                # TODO: implementasikan
                pass
            """,
            """
            assert rata_rata_berjalan([1, 2, 3, 4, 5]) == [1.0, 1.5, 2.0, 2.5, 3.0]
            assert rata_rata_berjalan([10]) == [10.0]
            assert rata_rata_berjalan([]) == []
            assert rata_rata_berjalan([1, 0, 1, 0]) == [1.0, 0.5, 0.6667, 0.5]
            """,
            "Simpan jumlah kumulatif dan bagi dengan banyak data sejauh ini.",
            """
            def rata_rata_berjalan(data):
                total = 0
                hasil = []
                for k, x in enumerate(data, start=1):
                    total += x
                    hasil.append(round(total / k, 4))
                return hasil
            """,
        ),
        E(
            "A4-07-1-ex2",
            "sedang",
            """
            Tulis fungsi `batas_chebyshev_rata(var, n, eps)` yang mengembalikan `min(1, var / (n * eps^2))` dibulatkan 4 desimal.
            """,
            """
            def batas_chebyshev_rata(var, n, eps):
                # TODO: implementasikan
                pass
            """,
            """
            assert batas_chebyshev_rata(35 / 12, 100, 0.5) == 0.1167
            assert batas_chebyshev_rata(1, 1, 0.5) == 1.0
            assert batas_chebyshev_rata(4, 100, 1) == 0.04
            assert batas_chebyshev_rata(1, 10000, 0.1) == 0.01
            """,
            "Bagi varians dengan n kali kuadrat toleransi dan batasi pada satu.",
            """
            def batas_chebyshev_rata(var, n, eps):
                return round(min(1, var / (n * eps ** 2)), 4)
            """,
        ),
        E(
            "A4-07-1-ex3",
            "sedang",
            """
            Tulis fungsi `ukuran_sampel_chebyshev(var, eps, delta)` yang mengembalikan `n` terkecil (bilangan bulat) dengan `var / (n * eps^2) <= delta`, yaitu pembulatan ke atas dari `var / (delta * eps^2)`.
            """,
            """
            import math

            def ukuran_sampel_chebyshev(var, eps, delta):
                # TODO: implementasikan
                pass
            """,
            """
            assert ukuran_sampel_chebyshev(4, 1, 0.05) == 80
            assert ukuran_sampel_chebyshev(1, 0.1, 0.01) == 10000
            assert ukuran_sampel_chebyshev(35 / 12, 0.5, 0.05) == 234
            assert ukuran_sampel_chebyshev(1, 1, 1) == 1
            """,
            "Balikkan batas untuk n lalu bulatkan ke atas dengan math.ceil.",
            """
            import math

            def ukuran_sampel_chebyshev(var, eps, delta):
                return math.ceil(var / (delta * eps ** 2))
            """,
        ),
        E(
            "A4-07-1-ex4",
            "menantang",
            """
            Tulis fungsi `simulasi_varians_rata(n, trial, seed)` yang memakai `random.Random(seed)` untuk menjalankan `trial` percobaan, masing-masing menghitung rata-rata `n` lemparan dadu (`randint(1, 6)`), lalu mengembalikan varians populasi dari rata-rata itu (pembagi `trial`).
            """,
            """
            import random

            def simulasi_varians_rata(n, trial, seed):
                # TODO: implementasikan
                pass
            """,
            """
            assert abs(simulasi_varians_rata(25, 5000, 1) - 35 / 12 / 25) < 0.01
            assert abs(simulasi_varians_rata(100, 5000, 2) - 35 / 12 / 100) < 0.005
            assert abs(simulasi_varians_rata(1, 5000, 3) - 35 / 12) < 0.3
            """,
            "Buat generator Random, kumpulkan rata-rata tiap percobaan, lalu hitung variansnya.",
            """
            import random

            def simulasi_varians_rata(n, trial, seed):
                r = random.Random(seed)
                rata = [sum(r.randint(1, 6) for _ in range(n)) / n for _ in range(trial)]
                m = sum(rata) / trial
                return sum((x - m) ** 2 for x in rata) / trial
            """,
        ),
    ],
    [
        M("Mengira hasil acak akan menyeimbangkan diri.", "Ketidakseimbangan awal hanya diencerkan."),
        M("Memakai hukum bilangan besar pada distribusi tanpa ekspektasi.", "Ekspektasi harus ada dan berhingga."),
        M("Mengira simpangan baku rata-rata turun sebagai satu per n.", "Turun sebagai satu per akar n."),
    ],
    [
        Q("Hukum bilangan besar menyatakan?", ["Rata-rata sampel mendekati ekspektasi", "Data selalu normal", "Varians nol", "Median tetap"], 0, "Untuk n besar.", hint="Konvergensi."),
        Q("Varians rata-rata sampel?", ["sigma^2", "sigma^2/n", "sigma/n", "n sigma^2"], 1, "Mengecil dengan n.", hint="Dibagi n."),
        Q("Kekeliruan gambler adalah?", ["Koin punya ingatan", "Koin adil", "n besar", "Rata-rata"], 0, "Lemparan independen.", hint="Tanpa ingatan."),
        Q("Chebyshev memberi batas?", ["Universal tapi longgar", "Ketat", "Hanya normal", "Hanya diskrit"], 0, "Tanpa asumsi bentuk.", hint="Longgar."),
        Q("Syarat penting hukum ini?", ["Ekspektasi berhingga", "Data normal", "n genap", "Varians nol"], 0, "Cauchy melanggarnya.", hint="Ekspektasi."),
    ],
    [
        "Rata-rata sampel mendekati ekspektasi bila n besar.",
        "Varians rata-rata adalah sigma kuadrat per n.",
        "Chebyshev memberi batas universal untuk penyimpangan rata-rata.",
        "Hukum ini tidak berarti keseimbangan paksa.",
    ],
    [],
)

l2 = lesson(
    "A4-07-2",
    "Teorema limit pusat",
    35,
    [
        "Menyatakan teorema limit pusat dan syaratnya",
        "Menghitung galat baku rata-rata",
        "Memakai pendekatan normal untuk peluang rata-rata",
        "Memakai pendekatan normal untuk binomial dengan koreksi kontinuitas",
    ],
    [
        T("""
        ## Bentuk distribusi rata-rata

        Hukum bilangan besar mengatakan ke mana rata-rata sampel menuju. **Teorema limit pusat** atau CLT mengatakan seperti apa sebarannya di sekitar tujuan itu. Untuk `n` besar, rata-rata `n` pengamatan independen dengan ekspektasi `mu` dan simpangan baku `sigma` berdistribusi mendekati normal dengan rata-rata `mu` dan simpangan baku `sigma / sqrt(n)`, **apa pun bentuk distribusi asalnya**.

        Itulah keajaibannya. Data asal bisa miring, berpuncak dua, atau diskrit, tetapi rata-ratanya cenderung berbentuk lonceng. Karena itu distribusi normal begitu sentral dalam statistika inferensial.
        """),
        T("""
        ## Galat baku

        Simpangan baku rata-rata sampel disebut **galat baku** atau standard error: `SE = sigma / sqrt(n)`. Ia mengukur seberapa jauh rata-rata sampel tipikalnya dari rata-rata populasi. Untuk menggandakan presisi atau mengecilkan galat separuh, kita butuh sampel empat kali lebih besar, bukan dua kali.

        Pengaruh akar `n` ini punya implikasi ekonomis: presisi tambahan makin mahal. Dari 100 ke 400 pengamatan galat turun separuh, tetapi dari 400 ke 1600 butuh tambahan 1200 pengamatan untuk separuh lagi.
        """),
        C(
            """
            import math

            sigma = math.sqrt(35 / 12)
            print(round(sigma / math.sqrt(100), 4), round(sigma / math.sqrt(400), 4))
            """,
            """
            0.1708 0.0854
            """,
            """
            Menaikkan sampel dari seratus ke empat ratus menurunkan galat baku rata-rata dadu separuhnya.
            """,
            filename="galat_baku.py",
        ),
        T("""
        ## Melihat CLT lewat simulasi

        Mari uji dengan distribusi yang jelas tidak normal: eksponensial dengan laju satu, sangat miring ke kanan. Ambil banyak sampel berukuran 30, hitung rata-ratanya, dan periksa seberapa sering rata-rata itu berada dalam `1,96` galat baku dari `mu`. Bila pendekatan normal baik, proporsinya mendekati `0,95`.

        Hasil simulasi mengonfirmasi bahwa walau data asal miring, rata-rata dari tiga puluh pengamatan sudah cukup normal untuk keperluan praktis. Untuk distribusi yang sangat miring atau berekor tebal, `n` yang dibutuhkan lebih besar.
        """),
        C(
            """
            import math
            import random

            r = random.Random(21)
            n = 30
            se = 1 / math.sqrt(n)
            dalam = 0
            for _ in range(5000):
                rata = sum(r.expovariate(1) for _ in range(n)) / n
                if abs(rata - 1) < 1.96 * se:
                    dalam += 1
            print(abs(dalam / 5000 - 0.95) < 0.03)
            """,
            """
            True
            """,
            """
            Walau data eksponensial miring, proporsi rata-rata dalam seratus sembilan puluh enam galat baku mendekati sembilan puluh lima persen.
            """,
            filename="clt_simulasi.py",
        ),
        T("""
        ## Peluang rata-rata dengan CLT

        Dengan CLT kita dapat menghitung peluang tentang rata-rata sampel memakai tabel normal. Untuk rata-rata seratus lemparan dadu, `mu = 3,5` dan `SE = 0,1708`. Peluang rata-rata melebihi `3,8` adalah `1 - Phi((3,8 - 3,5) / 0,1708)`, yaitu sekitar `0,0395`.

        Langkahnya selalu sama: hitung galat baku, ubah ke z-score, lalu gunakan CDF normal. Perhitungan ini dasar semua uji hipotesis dan interval kepercayaan yang akan dibahas di kursus statistika inferensial.
        """),
        T("""
        ## Normal untuk binomial

        Binomial adalah jumlah `n` Bernoulli independen, sehingga CLT berlaku: untuk `n` besar, binomial `(n, p)` mendekati normal dengan rata-rata `n p` dan simpangan baku `sqrt(n p (1-p))`. Karena binomial diskrit dan normal kontinu, kita memakai **koreksi kontinuitas**: peluang `X <= k` didekati dengan `P(Y <= k + 0,5)`.

        Koreksi setengah satuan itu memperbaiki akurasi dengan menjembatani lompatan diskrit. Pendekatan baik bila `n p` dan `n (1-p)` keduanya minimal sekitar sepuluh.
        """),
        C(
            """
            import math

            def Phi(x):
                return 0.5 * (1 + math.erf(x / math.sqrt(2)))

            n, p, k = 100, 0.5, 55
            tepat = sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k + 1))
            pendekatan = Phi((k + 0.5 - n * p) / math.sqrt(n * p * (1 - p)))
            print(round(tepat, 4), round(pendekatan, 4))
            """,
            """
            0.8644 0.8643
            """,
            """
            Pendekatan normal dengan koreksi kontinuitas hampir sama dengan hitungan binomial eksak.
            """,
            filename="normal_binomial.py",
        ),
        T("""
        ## Jumlah, bukan hanya rata-rata

        CLT juga berlaku untuk jumlah. Jumlah `n` pengamatan memiliki ekspektasi `n mu` dan simpangan baku `sigma sqrt(n)`. Jumlah tiga puluh lemparan dadu memiliki rata-rata `105` dan simpangan baku `9,354`. Dari sini kita bisa menghitung peluang total skor berada dalam rentang tertentu.

        Perhatikan perbedaan skala: simpangan baku jumlah tumbuh sebagai `sqrt(n)`, tetapi simpangan baku rata-rata mengecil sebagai `1/sqrt(n)`. Dua pernyataan ini sering tertukar, jadi periksa dulu apakah soal bertanya tentang jumlah atau rata-rata.
        """),
        C(
            """
            import math

            print(30 * 3.5, round(math.sqrt(30 * 35 / 12), 4))
            """,
            """
            105.0 9.3541
            """,
            """
            Jumlah tiga puluh dadu berpusat di seratus lima dengan simpangan baku sekitar sembilan koma tiga.
            """,
            filename="jumlah_dadu.py",
        ),
        K(
            "tip",
            """
            Sebelum memakai CLT, periksa seberapa miring distribusi asal. Makin miring atau berekor tebal, makin besar n yang dibutuhkan. Pedoman n minimal 30 adalah titik awal, bukan jaminan.
            """,
            title="Seberapa besar n",
        ),
        T("""
        ## Batas penggunaan CLT

        CLT bukan jaminan di setiap situasi. Ia membutuhkan pengamatan independen, varians berhingga, dan sampel yang cukup besar relatif terhadap kemiringan data. Data deret waktu yang berautokorelasi kuat melanggar independensi sehingga galat baku yang dihitung dengan rumus biasa terlalu kecil. Distribusi berekor sangat tebal dapat membuat konvergensi sangat lambat.

        Untuk kasus meragukan, bootstrap adalah alternatif praktis: ambil sampel ulang dengan pengembalian dari data sendiri, hitung statistik tiap kali, dan gunakan sebaran hasilnya sebagai taksiran sebaran statistik. Ide ini bergantung pada hukum bilangan besar yang sama.
        """),
        E(
            "A4-07-2-ex1",
            "mudah",
            """
            Tulis fungsi `galat_baku(sigma, n)` yang mengembalikan `sigma / sqrt(n)` dibulatkan 4 desimal.
            """,
            """
            import math

            def galat_baku(sigma, n):
                # TODO: implementasikan
                pass
            """,
            """
            assert galat_baku(2, 16) == 0.5
            assert galat_baku(10, 400) == 0.5
            assert galat_baku(1, 10000) == 0.01
            assert galat_baku(3, 2) == 2.1213
            """,
            "Bagi simpangan baku dengan akar banyaknya data.",
            """
            import math

            def galat_baku(sigma, n):
                return round(sigma / math.sqrt(n), 4)
            """,
        ),
        E(
            "A4-07-2-ex2",
            "sedang",
            """
            Tulis fungsi `peluang_rata_di_atas(mu, sigma, n, x)` yang mengembalikan peluang rata-rata sampel melebihi `x` menurut CLT, dibulatkan 4 desimal.
            """,
            """
            import math

            def peluang_rata_di_atas(mu, sigma, n, x):
                # TODO: implementasikan
                pass
            """,
            """
            assert peluang_rata_di_atas(3.5, math.sqrt(35 / 12), 100, 3.8) == 0.0395
            assert peluang_rata_di_atas(100, 15, 25, 103) == 0.1587
            assert peluang_rata_di_atas(0, 1, 1, 0) == 0.5
            assert peluang_rata_di_atas(10, 2, 100, 10) == 0.5
            """,
            "Hitung galat baku, ubah ke z-score, lalu ambil satu dikurangi CDF normal.",
            """
            import math

            def peluang_rata_di_atas(mu, sigma, n, x):
                z = (x - mu) / (sigma / math.sqrt(n))
                return round(1 - 0.5 * (1 + math.erf(z / math.sqrt(2))), 4)
            """,
        ),
        E(
            "A4-07-2-ex3",
            "sedang",
            """
            Tulis fungsi `aproks_normal_binom(n, p, k)` yang mengembalikan taksiran `P(X <= k)` untuk binomial `(n, p)` dengan normal dan koreksi kontinuitas (`k + 0.5`), dibulatkan 4 desimal.
            """,
            """
            import math

            def aproks_normal_binom(n, p, k):
                # TODO: implementasikan
                pass
            """,
            """
            assert aproks_normal_binom(100, 0.5, 55) == 0.8643
            assert aproks_normal_binom(100, 0.5, 50) == 0.5398
            assert aproks_normal_binom(10, 0.5, 5) == 0.6241
            assert aproks_normal_binom(20, 0.1, 2) == 0.6453
            """,
            "Pakai rata-rata n p dan simpangan baku akar n p satu kurang p pada titik k tambah setengah.",
            """
            import math

            def aproks_normal_binom(n, p, k):
                z = (k + 0.5 - n * p) / math.sqrt(n * p * (1 - p))
                return round(0.5 * (1 + math.erf(z / math.sqrt(2))), 4)
            """,
        ),
        E(
            "A4-07-2-ex4",
            "menantang",
            """
            Tulis fungsi `simulasi_clt(n, trial, seed)` yang memakai `random.Random(seed)` untuk mengambil `trial` sampel eksponensial laju satu (`expovariate(1)`) berukuran `n`, dan mengembalikan proporsi rata-rata sampel yang berjarak kurang dari `1.96 / sqrt(n)` dari satu.
            """,
            """
            import math
            import random

            def simulasi_clt(n, trial, seed):
                # TODO: implementasikan
                pass
            """,
            """
            assert abs(simulasi_clt(30, 5000, 1) - 0.95) < 0.03
            assert abs(simulasi_clt(100, 3000, 2) - 0.95) < 0.03
            assert abs(simulasi_clt(50, 3000, 4) - 0.95) < 0.03
            """,
            "Hitung rata-rata tiap sampel lalu hitung proporsi yang berada dalam batas galat baku.",
            """
            import math
            import random

            def simulasi_clt(n, trial, seed):
                r = random.Random(seed)
                batas = 1.96 / math.sqrt(n)
                dalam = 0
                for _ in range(trial):
                    rata = sum(r.expovariate(1) for _ in range(n)) / n
                    if abs(rata - 1) < batas:
                        dalam += 1
                return dalam / trial
            """,
        ),
    ],
    [
        M("Menukar simpangan baku jumlah dengan simpangan baku rata-rata.", "Jumlah: sigma akar n. Rata-rata: sigma per akar n."),
        M("Memakai CLT pada n sangat kecil dan data miring.", "Periksa bentuk dan n."),
        M("Lupa koreksi kontinuitas pada normal untuk binomial.", "Pakai k tambah setengah."),
    ],
    [
        Q("CLT menyatakan rata-rata sampel mendekati?", ["Normal", "Seragam", "Eksponensial", "Poisson"], 0, "Untuk n besar.", hint="Lonceng."),
        Q("Galat baku?", ["sigma/akar n", "sigma akar n", "sigma/n", "sigma^2"], 0, "SD rata-rata.", hint="Akar n."),
        Q("Presisi dua kali lipat butuh sampel?", ["Dua kali", "Empat kali", "Sepuluh kali", "Sama"], 1, "Akar n.", hint="Kuadrat."),
        Q("Koreksi kontinuitas?", ["k + 0,5", "k - 5", "2k", "k/2"], 0, "Menjembatani diskrit.", hint="Setengah."),
        Q("SD jumlah n pengamatan?", ["sigma/akar n", "sigma akar n", "n sigma", "sigma"], 1, "Tumbuh akar n.", hint="Jumlah."),
    ],
    [
        "CLT: rata-rata sampel mendekati normal apa pun distribusi asal.",
        "Galat baku sigma per akar n mengukur presisi rata-rata.",
        "Normal mengaproksimasi binomial dengan koreksi kontinuitas.",
        "Jumlah dan rata-rata punya skala simpangan baku berbeda.",
    ],
    [],
)

l3 = lesson(
    "A4-07-3",
    "Interval kepercayaan dan ukuran sampel",
    35,
    [
        "Menyusun interval kepercayaan 95 persen untuk rata-rata",
        "Menyusun interval kepercayaan untuk proporsi",
        "Menafsirkan interval kepercayaan dengan benar",
        "Menentukan ukuran sampel dari margin galat yang diinginkan",
    ],
    [
        T("""
        ## Dari titik ke rentang

        Rata-rata sampel adalah taksiran titik bagi rata-rata populasi, tetapi hampir pasti tidak tepat sama. Yang lebih jujur adalah memberi rentang: rata-rata kira-kira antara sekian dan sekian. **Interval kepercayaan** melakukan ini dengan tingkat keyakinan yang terukur, biasanya 95 persen.

        Berkat CLT, rata-rata sampel berdistribusi hampir normal di sekitar rata-rata populasi dengan simpangan baku `SE`. Maka kira-kira 95 persen rata-rata sampel berada dalam `1,96 SE` dari rata-rata sebenarnya. Membalik pernyataan ini menghasilkan interval `rata-rata sampel ± 1,96 SE`.
        """),
        C(
            """
            import math

            mean, sd, n = 50, 10, 100
            se = sd / math.sqrt(n)
            print(round(mean - 1.96 * se, 4), round(mean + 1.96 * se, 4))
            """,
            """
            48.04 51.96
            """,
            """
            Dengan seratus data, rata-rata lima puluh, dan simpangan baku sepuluh, galat baku satu menghasilkan interval empat puluh delapan sampai lima puluh dua.
            """,
            filename="ci_mean.py",
        ),
        T("""
        ## Menafsirkan dengan benar

        Tafsir yang tepat sering salah dipahami. Interval 95 persen **tidak** berarti peluang rata-rata populasi berada di interval itu adalah 95 persen, karena rata-rata populasi adalah konstanta tetap, bukan variabel acak. Yang acak adalah intervalnya. Tafsirnya: bila prosedur ini diulang pada banyak sampel, sekitar 95 persen interval yang dihasilkan akan memuat rata-rata populasi.

        Kita dapat memeriksa tafsir ini dengan simulasi: ambil banyak sampel dari populasi yang rata-ratanya diketahui, bangun intervalnya, dan hitung berapa kali interval memuat nilai sebenarnya.
        """),
        C(
            """
            import math
            import random

            r = random.Random(9)
            n = 30
            memuat = 0
            for _ in range(2000):
                rata = sum(r.gauss(0, 1) for _ in range(n)) / n
                se = 1 / math.sqrt(n)
                if rata - 1.96 * se <= 0 <= rata + 1.96 * se:
                    memuat += 1
            print(abs(memuat / 2000 - 0.95) < 0.03)
            """,
            """
            True
            """,
            """
            Sekitar sembilan puluh lima persen interval yang dibangun dari sampel berulang memuat rata-rata sebenarnya.
            """,
            filename="cakupan.py",
        ),
        T("""
        ## Interval untuk proporsi

        Proporsi adalah rata-rata variabel Bernoulli, sehingga CLT berlaku. Taksirannya `p_hat = x / n` dengan galat baku `sqrt(p_hat (1 - p_hat) / n)`. Interval 95 persennya `p_hat ± 1,96 * SE`. Misalnya 420 dari 1000 responden setuju: `p_hat = 0,42`, galat baku sekitar `0,0156`, dan intervalnya kira-kira `0,389` sampai `0,451`.

        Pendekatan ini kurang baik bila `p_hat` sangat dekat nol atau satu atau `n` kecil. Pada kasus itu interval bisa keluar dari rentang nol sampai satu, dan metode yang lebih baik seperti interval Wilson sebaiknya dipakai.
        """),
        C(
            """
            import math

            x, n = 420, 1000
            p = x / n
            se = math.sqrt(p * (1 - p) / n)
            print(round(p - 1.96 * se, 4), round(p + 1.96 * se, 4))
            """,
            """
            0.3894 0.4506
            """,
            """
            Empat ratus dua puluh dari seribu memberi interval sekitar tiga puluh sembilan sampai empat puluh lima persen.
            """,
            filename="ci_proporsi.py",
        ),
        T("""
        ## Ukuran sampel

        Kita bisa membalik rumus untuk merencanakan: berapa data yang dibutuhkan agar margin galat `1,96 SE` tidak melebihi nilai tertentu `m`? Untuk rata-rata, `n >= (1,96 * sigma / m)^2`. Dengan `sigma = 10` dan margin 2, `n` minimal 97.

        Rumus ini menunjukkan trade-off: margin separuh membutuhkan sampel empat kali lebih besar. Perencanaan sebelum mengumpulkan data jauh lebih murah daripada menyadari setelahnya bahwa sampelnya terlalu kecil untuk menjawab pertanyaan.
        """),
        C(
            """
            import math

            print(math.ceil((1.96 * 10 / 2) ** 2))
            print(math.ceil(1.96 ** 2 * 0.25 / 0.03 ** 2))
            """,
            """
            97
            1068
            """,
            """
            Untuk margin dua dan simpangan baku sepuluh dibutuhkan sembilan puluh tujuh data. Survei proporsi dengan margin tiga persen membutuhkan seribu enam puluh delapan responden pada kasus terburuk.
            """,
            filename="ukuran_sampel.py",
        ),
        T("""
        ## Kasus terburuk untuk proporsi

        Untuk survei kita belum tahu `p` sebelum mengumpulkan data. Karena `p (1 - p)` terbesar pada `p = 0,5`, memakai `0,5` menghasilkan ukuran sampel yang aman untuk berapa pun `p` sebenarnya. Itulah mengapa banyak survei nasional memakai sekitar seribu responden untuk margin galat kira-kira tiga persen.

        Bila kamu punya perkiraan awal `p` yang jauh dari setengah, misalnya sepuluh persen, ukuran sampel yang dibutuhkan bisa jauh lebih kecil. Namun perkiraan yang meleset membuat margin lebih lebar dari rencana, jadi banyak praktisi tetap memakai kasus terburuk.
        """),
        K(
            "warn",
            """
            Interval kepercayaan hanya menangkap galat acak pengambilan sampel. Sampel yang bias, misalnya responden yang tidak mewakili populasi, tidak diperbaiki dengan menambah data.
            """,
            title="Bias bukan galat acak",
        ),
        T("""
        ## Membandingkan dua kelompok

        Interval kepercayaan juga dipakai untuk perbedaan dua kelompok, misalnya dua versi halaman web pada uji A/B. Selisih rata-rata kedua kelompok memiliki galat baku `sqrt(SE1^2 + SE2^2)` bila kelompok independen. Interval selisih yang memuat nol menandakan bahwa perbedaan yang teramati masih bisa muncul karena kebetulan.

        Cara membaca ini lebih informatif daripada sekadar menyatakan signifikan atau tidak: interval memperlihatkan seberapa besar efek yang masuk akal, dari efek nyaris nol sampai efek besar. Keputusan bisnis bergantung pada ukuran efek, bukan hanya ada atau tidaknya.
        """),
        T("""
        ## Kesalahan umum

        Beberapa kesalahan sering muncul. Pertama, menafsirkan interval sebagai rentang tempat 95 persen data berada, padahal ia hanya tentang rata-rata. Kedua, membandingkan dua interval secara kasar dan menyimpulkan tidak berbeda hanya karena tumpang tindih. Ketiga, mengintip data berulang kali sambil memperbarui interval lalu berhenti ketika hasil tampak bagus, yang membengkakkan galat tipe satu.

        Hindari ketiganya dengan menentukan ukuran sampel di awal, menghitung interval untuk selisih secara langsung, dan membedakan interval taksiran dari interval prediksi data baru.
        """),
        E(
            "A4-07-3-ex1",
            "mudah",
            """
            Tulis fungsi `interval_mean(mean, sd, n, z=1.96)` yang mengembalikan tuple `(bawah, atas)` interval kepercayaan rata-rata, dibulatkan 4 desimal.
            """,
            """
            import math

            def interval_mean(mean, sd, n, z=1.96):
                # TODO: implementasikan
                pass
            """,
            """
            assert interval_mean(50, 10, 100) == (48.04, 51.96)
            assert interval_mean(0, 1, 4) == (-0.98, 0.98)
            assert interval_mean(10, 0, 25) == (10.0, 10.0)
            assert interval_mean(100, 15, 25, 1.645) == (95.065, 104.935)
            """,
            "Hitung galat baku lalu tambah dan kurangi z kali galat baku.",
            """
            import math

            def interval_mean(mean, sd, n, z=1.96):
                m = z * sd / math.sqrt(n)
                return (round(mean - m, 4), round(mean + m, 4))
            """,
        ),
        E(
            "A4-07-3-ex2",
            "sedang",
            """
            Tulis fungsi `interval_proporsi(x, n, z=1.96)` yang mengembalikan tuple `(bawah, atas)` interval kepercayaan untuk proporsi `x / n`, dibatasi pada rentang 0.0 sampai 1.0 dan dibulatkan 4 desimal.
            """,
            """
            import math

            def interval_proporsi(x, n, z=1.96):
                # TODO: implementasikan
                pass
            """,
            """
            assert interval_proporsi(420, 1000) == (0.3894, 0.4506)
            assert interval_proporsi(50, 100) == (0.402, 0.598)
            assert interval_proporsi(5, 10) == (0.1901, 0.8099)
            assert interval_proporsi(0, 10) == (0.0, 0.0)
            assert interval_proporsi(10, 10) == (1.0, 1.0)
            """,
            "Pakai galat baku akar p dikali satu kurang p per n lalu batasi hasil pada nol dan satu.",
            """
            import math

            def interval_proporsi(x, n, z=1.96):
                p = x / n
                m = z * math.sqrt(p * (1 - p) / n)
                return (round(max(0.0, p - m), 4), round(min(1.0, p + m), 4))
            """,
        ),
        E(
            "A4-07-3-ex3",
            "sedang",
            """
            Tulis fungsi `ukuran_sampel_mean(sigma, margin, z=1.96)` yang mengembalikan `n` terkecil (bilangan bulat) dengan `z * sigma / sqrt(n) <= margin`, yaitu `ceil((z * sigma / margin) ** 2)`.
            """,
            """
            import math

            def ukuran_sampel_mean(sigma, margin, z=1.96):
                # TODO: implementasikan
                pass
            """,
            """
            assert ukuran_sampel_mean(15, 2) == 217
            assert ukuran_sampel_mean(1, 0.1) == 385
            assert ukuran_sampel_mean(10, 10) == 4
            assert ukuran_sampel_mean(2.5, 0.5) == 97
            """,
            "Balikkan margin untuk n lalu bulatkan ke atas.",
            """
            import math

            def ukuran_sampel_mean(sigma, margin, z=1.96):
                return math.ceil((z * sigma / margin) ** 2)
            """,
        ),
        E(
            "A4-07-3-ex4",
            "menantang",
            """
            Tulis fungsi `ukuran_sampel_proporsi(margin, p=0.5, z=1.96)` yang mengembalikan `ceil(z ** 2 * p * (1 - p) / margin ** 2)`.
            """,
            """
            import math

            def ukuran_sampel_proporsi(margin, p=0.5, z=1.96):
                # TODO: implementasikan
                pass
            """,
            """
            assert ukuran_sampel_proporsi(0.03) == 1068
            assert ukuran_sampel_proporsi(0.05) == 385
            assert ukuran_sampel_proporsi(0.01) == 9604
            assert ukuran_sampel_proporsi(0.1) == 97
            assert ukuran_sampel_proporsi(0.05, 0.1) == 139
            """,
            "Pakai rumus kuadrat z kali p kali satu kurang p dibagi kuadrat margin lalu bulatkan ke atas.",
            """
            import math

            def ukuran_sampel_proporsi(margin, p=0.5, z=1.96):
                return math.ceil(z ** 2 * p * (1 - p) / margin ** 2)
            """,
        ),
    ],
    [
        M("Menafsirkan interval 95 persen sebagai peluang parameter ada di dalamnya.", "Tafsirkan lewat pengulangan prosedur."),
        M("Menambah sampel bias untuk memperbaiki hasil.", "Interval hanya mengatasi galat acak."),
        M("Memakai rumus normal pada proporsi ekstrem dengan n kecil.", "Pakai metode seperti Wilson."),
    ],
    [
        Q("Interval 95% rata-rata?", ["rata-rata ± 1,96 SE", "rata-rata ± SE", "rata-rata ± 2", "rata-rata saja"], 0, "Berdasarkan CLT.", hint="Z kritis."),
        Q("Margin separuh butuh sampel?", ["Dua kali", "Empat kali", "Sama", "Setengah"], 1, "Akar n.", hint="Kuadrat."),
        Q("Kasus terburuk proporsi memakai p?", ["0", "0,5", "1", "0,1"], 1, "p(1-p) maksimum.", hint="Tengah."),
        Q("Interval kepercayaan menangkap?", ["Galat acak sampling", "Bias", "Kesalahan ukur sistematis", "Semua galat"], 0, "Bukan bias.", hint="Acak."),
        Q("Tafsir benar interval 95%?", ["95% interval memuat parameter bila diulang", "Parameter acak", "95% data di dalam", "Peluang parameter 95%"], 0, "Prosedur diulang.", hint="Pengulangan."),
    ],
    [
        "Interval kepercayaan memberi rentang taksiran dengan keyakinan terukur.",
        "Tafsir interval lewat pengulangan prosedur, bukan peluang parameter.",
        "Proporsi memakai galat baku akar p(1-p)/n.",
        "Ukuran sampel dapat direncanakan dari margin galat.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perhitungan yang cukup jelas dalam teks.", "brief": []}

write_module(
    "A4",
    7,
    "Hukum bilangan besar dan CLT",
    105,
    [
        "Memahami hukum bilangan besar dan batas Chebyshev",
        "Memakai teorema limit pusat dan galat baku",
        "Menyusun interval kepercayaan dan merencanakan ukuran sampel",
    ],
    [l1, l2, l3],
    video,
    REF,
)
