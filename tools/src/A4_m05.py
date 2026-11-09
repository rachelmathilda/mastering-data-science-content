import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

l1 = lesson(
    "A4-05-1",
    "Bernoulli, binomial, dan geometrik",
    35,
    [
        "Mengenali percobaan Bernoulli dan membangun distribusi binomial",
        "Menghitung PMF dan CDF binomial",
        "Menghitung rata-rata dan varians binomial",
        "Memakai distribusi geometrik untuk waktu tunggu diskrit",
    ],
    [
        T("""
        ## Keluarga distribusi

        Dalam praktik kita tidak membuat PMF baru tiap kali. Sebagian besar situasi cocok dengan segelintir distribusi standar, masing-masing lahir dari cerita sederhana. Mengenali cerita di balik data memungkinkan kita memilih distribusi yang tepat dan memakai rumus yang sudah tersedia.

        Pelajaran ini membahas tiga distribusi diskrit yang bertumpu pada satu cerita: percobaan ya atau tidak yang diulang. Dua pelajaran berikutnya membahas Poisson untuk kejadian langka dan normal untuk besaran kontinu yang menumpuk dari banyak sumber kecil.
        """),
        T("""
        ## Percobaan Bernoulli

        **Percobaan Bernoulli** adalah percobaan dengan tepat dua hasil, sukses dengan peluang `p` dan gagal dengan peluang `1 - p`. Contohnya satu lemparan koin, satu pelanggan yang membeli atau tidak, satu email yang spam atau bukan. Variabel acaknya bernilai 1 untuk sukses dan 0 untuk gagal.

        Distribusi Bernoulli hanya punya satu parameter `p`, tetapi ia adalah batu bata bagi distribusi lain. Hampir setiap label biner dalam machine learning, seperti churn atau fraud, dapat dimodelkan sebagai Bernoulli dengan `p` yang bergantung pada fitur.
        """),
        T("""
        ## Distribusi binomial

        Ulangi percobaan Bernoulli `n` kali secara independen dengan peluang sukses sama `p`. Banyaknya sukses `X` berdistribusi **binomial**: `P(X = k) = C(n, k) * p^k * (1-p)^(n-k)`. Faktor `C(n, k)` menghitung banyaknya urutan yang memiliki tepat `k` sukses, dan sisanya adalah peluang satu urutan tertentu.

        Tiga syarat harus dipenuhi: jumlah percobaan tetap, tiap percobaan hanya dua hasil, dan percobaan independen dengan `p` konstan. Bila pengambilan dilakukan tanpa pengembalian dari populasi kecil, independensi runtuh dan distribusi hipergeometrik lebih tepat.
        """),
        C(
            """
            import math

            def pmf(k, n, p):
                return math.comb(n, k) * p ** k * (1 - p) ** (n - k)

            print(round(pmf(5, 10, 0.5), 4))
            print(round(sum(pmf(k, 10, 0.5) for k in range(4)), 4))
            """,
            """
            0.2461
            0.1719
            """,
            """
            Lima kepala dalam sepuluh lemparan paling mungkin dengan sekitar dua puluh lima persen, dan paling banyak tiga kepala berpeluang sekitar tujuh belas persen.
            """,
            filename="binomial.py",
        ),
        T("""
        ## Rata-rata dan varians

        Karena binomial adalah jumlah `n` Bernoulli independen, rata-ratanya `n * p` dan variansnya `n * p * (1 - p)`. Rata-rata 10 koin adil adalah lima kepala, dan simpangan bakunya `sqrt(2,5)`, sekitar 1,58. Varians terbesar terjadi pada `p = 0,5` dan mengecil saat `p` mendekati nol atau satu.

        Rumus ini bisa dicek dari definisi dengan menjumlahkan `k * P(k)` dan `(k - rata-rata)^2 * P(k)` atas semua `k`. Mencocokkan rumus dengan jumlah langsung adalah latihan yang menguatkan kepercayaan terhadap rumus.
        """),
        C(
            """
            import math

            n, p = 20, 0.1
            pmf = [math.comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(n + 1)]
            mean = sum(k * q for k, q in enumerate(pmf))
            var = sum((k - mean) ** 2 * q for k, q in enumerate(pmf))
            print(round(mean, 4), round(var, 4))
            """,
            """
            2.0 1.8
            """,
            """
            Jumlah langsung memberi rata-rata dua dan varians satu koma delapan, sama dengan n p dan n p dikali satu kurang p.
            """,
            filename="binomial_mean_var.py",
        ),
        T("""
        ## Contoh pengendalian mutu

        Sebuah pabrik memeriksa 50 produk dengan tingkat cacat dua persen. Peluang minimal satu cacat adalah komplemen dari tidak ada cacat sama sekali: `1 - 0,98^50`, sekitar `0,6358`. Walau tiap produk hanya dua persen cacat, dari 50 produk lebih dari separuh peluang memuat paling tidak satu cacat.

        Itulah mengapa pemeriksaan sampel kecil sering mendeteksi masalah lebih sering daripada intuisi kita. Perhitungan binomial semacam ini dasar bagi rencana sampling penerimaan dan pengujian A/B.
        """),
        C(
            """
            import math

            print(round(1 - math.comb(50, 0) * 0.98 ** 50, 4))
            """,
            """
            0.6358
            """,
            """
            Komplemen tidak ada cacat memberi peluang sekitar enam puluh empat persen untuk minimal satu cacat.
            """,
            filename="mutu.py",
        ),
        T("""
        ## Distribusi geometrik

        Bila kita mengulang percobaan Bernoulli sampai sukses pertama, banyaknya percobaan `X` berdistribusi **geometrik**: `P(X = k) = (1 - p)^(k-1) * p`. Gagal `k - 1` kali berturut-turut lalu sukses. Rata-ratanya `1/p`: bila peluang sukses seperlima, kita rata-rata butuh lima percobaan.

        Geometrik adalah padanan diskrit eksponensial dan juga tanpa ingatan. Contohnya jumlah lemparan dadu sampai muncul enam atau jumlah panggilan sales sampai ada yang membeli. Rumusnya sederhana, tetapi asumsi independensi tiap percobaan harus dibenarkan.
        """),
        C(
            """
            p = 0.2
            print(round((1 - p) ** 2 * p, 4), 1 / p)
            """,
            """
            0.128 5.0
            """,
            """
            Peluang sukses pertama tepat pada percobaan ketiga adalah nol koma satu dua delapan, dan rata-rata percobaan yang dibutuhkan adalah lima.
            """,
            filename="geometrik.py",
        ),
        K(
            "tip",
            """
            Sebelum memakai binomial, cek tiga hal: n tetap, dua hasil, dan independen dengan p konstan. Bila salah satu gagal, pertimbangkan distribusi lain.
            """,
            title="Tiga syarat binomial",
        ),
        T("""
        ## Memilih antara binomial dan geometrik

        Pertanyaan pembeda: apa yang tetap dan apa yang acak? Pada binomial jumlah percobaan tetap dan banyaknya sukses acak. Pada geometrik banyaknya sukses tetap, yaitu satu, dan jumlah percobaan yang acak. Menulis ulang soal dalam kalimat tersebut biasanya langsung memberi jawaban.

        Contohnya: berapa dari seratus email yang dibuka adalah binomial, sedangkan berapa email dikirim sampai ada yang dibuka pertama kali adalah geometrik. Kerangka dua pertanyaan ini mencegah salah pilih rumus.
        """),
        E(
            "A4-05-1-ex1",
            "mudah",
            """
            Tulis fungsi `pmf_binomial(k, n, p)` yang mengembalikan `P(X = k)` dibulatkan 4 desimal, dan `0.0` bila `k` di luar `0..n`.
            """,
            """
            import math

            def pmf_binomial(k, n, p):
                # TODO: implementasikan
                pass
            """,
            """
            assert pmf_binomial(5, 10, 0.5) == 0.2461
            assert pmf_binomial(0, 4, 0.5) == 0.0625
            assert pmf_binomial(3, 3, 0.5) == 0.125
            assert pmf_binomial(2, 5, 0.3) == 0.3087
            assert pmf_binomial(6, 5, 0.5) == 0.0
            """,
            "Kalikan banyak kombinasi dengan peluang urutan tertentu.",
            """
            import math

            def pmf_binomial(k, n, p):
                if k < 0 or k > n:
                    return 0.0
                return round(math.comb(n, k) * p ** k * (1 - p) ** (n - k), 4)
            """,
        ),
        E(
            "A4-05-1-ex2",
            "sedang",
            """
            Tulis fungsi `cdf_binomial(k, n, p)` yang mengembalikan `P(X <= k)` dibulatkan 4 desimal. Kembalikan `0.0` untuk `k < 0` dan `1.0` untuk `k >= n`.
            """,
            """
            import math

            def cdf_binomial(k, n, p):
                # TODO: implementasikan
                pass
            """,
            """
            assert cdf_binomial(3, 10, 0.5) == 0.1719
            assert cdf_binomial(10, 10, 0.3) == 1.0
            assert cdf_binomial(-1, 5, 0.5) == 0.0
            assert cdf_binomial(0, 3, 0.5) == 0.125
            assert cdf_binomial(2, 5, 0.5) == 0.5
            """,
            "Jumlahkan PMF dari nol sampai k.",
            """
            import math

            def cdf_binomial(k, n, p):
                if k < 0:
                    return 0.0
                if k >= n:
                    return 1.0
                return round(sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k + 1)), 4)
            """,
        ),
        E(
            "A4-05-1-ex3",
            "sedang",
            """
            Tulis fungsi `pmf_geometrik(k, p)` yang mengembalikan peluang sukses pertama terjadi tepat pada percobaan ke-`k`, dibulatkan 4 desimal. Kembalikan `0.0` bila `k < 1`.
            """,
            """
            def pmf_geometrik(k, p):
                # TODO: implementasikan
                pass
            """,
            """
            assert pmf_geometrik(3, 0.2) == 0.128
            assert pmf_geometrik(1, 0.5) == 0.5
            assert pmf_geometrik(4, 0.5) == 0.0625
            assert pmf_geometrik(0, 0.5) == 0.0
            assert pmf_geometrik(2, 1 / 6) == 0.1389
            """,
            "Gagal k minus satu kali lalu sukses sekali.",
            """
            def pmf_geometrik(k, p):
                if k < 1:
                    return 0.0
                return round((1 - p) ** (k - 1) * p, 4)
            """,
        ),
        E(
            "A4-05-1-ex4",
            "menantang",
            """
            Tulis fungsi `modus_binomial(n, p)` yang mengembalikan nilai `k` dengan PMF binomial terbesar. Gunakan PMF langsung dan hindari bergantung pada rumus tertutup.
            """,
            """
            import math

            def modus_binomial(n, p):
                # TODO: implementasikan
                pass
            """,
            """
            assert modus_binomial(10, 0.5) == 5
            assert modus_binomial(20, 0.1) == 2
            assert modus_binomial(5, 0.3) == 1
            assert modus_binomial(10, 0.9) == 9
            assert modus_binomial(4, 1.0) == 4
            """,
            "Cari k dengan nilai PMF maksimum memakai max dan key.",
            """
            import math

            def modus_binomial(n, p):
                return max(range(n + 1), key=lambda k: math.comb(n, k) * p ** k * (1 - p) ** (n - k))
            """,
        ),
    ],
    [
        M("Memakai binomial tanpa memeriksa independensi.", "Cek tiga syarat dulu."),
        M("Lupa faktor kombinasi pada PMF binomial.", "Banyak urutan dihitung C(n, k)."),
        M("Menukar geometrik dengan binomial.", "Geometrik menghitung percobaan sampai sukses pertama."),
    ],
    [
        Q("Binomial menghitung?", ["Waktu tunggu", "Banyak sukses dari n percobaan", "Rata-rata", "Kuantil"], 1, "Jumlah sukses.", hint="n percobaan."),
        Q("Rata-rata binomial?", ["p", "n p", "n/p", "n(1-p)"], 1, "Jumlah n Bernoulli.", hint="Jumlah."),
        Q("Varians binomial?", ["n p", "n p (1-p)", "p(1-p)", "n(1-p)"], 1, "n kali varians Bernoulli.", hint="Bernoulli kali n."),
        Q("Geometrik menghitung?", ["Percobaan sampai sukses pertama", "Jumlah sukses", "Jumlah gagal total", "Waktu kontinu"], 0, "Sampai sukses.", hint="Pertama."),
        Q("Rata-rata geometrik?", ["p", "1/p", "p^2", "1-p"], 1, "Lima bila p seperlima.", hint="Kebalikan."),
    ],
    [
        "Bernoulli adalah satu percobaan dua hasil.",
        "Binomial adalah jumlah sukses dari n percobaan independen.",
        "Rata-rata n p dan varians n p (1-p).",
        "Geometrik adalah banyak percobaan sampai sukses pertama.",
    ],
    [],
)

l2 = lesson(
    "A4-05-2",
    "Distribusi Poisson",
    35,
    [
        "Mengenali situasi yang cocok untuk Poisson",
        "Menghitung PMF dan CDF Poisson",
        "Menyesuaikan laju dengan skala waktu",
        "Memakai Poisson sebagai aproksimasi binomial kejadian langka",
    ],
    [
        T("""
        ## Menghitung kejadian langka

        Berapa panggilan masuk ke pusat layanan dalam satu jam? Berapa kecelakaan di satu persimpangan dalam sebulan? Berapa typo dalam satu halaman? Hitungan kejadian yang terjadi secara acak pada selang waktu atau ruang, dengan laju rata-rata yang kira-kira tetap, dimodelkan oleh distribusi **Poisson**.

        Distribusi ini hanya punya satu parameter, `lambda`, yaitu rata-rata banyaknya kejadian per selang. PMF-nya `P(X = k) = e^(-lambda) * lambda^k / k!` untuk `k = 0, 1, 2, ...`. Nilai `k` tidak punya batas atas, tetapi peluangnya menurun sangat cepat untuk `k` jauh di atas `lambda`.
        """),
        C(
            """
            import math

            def pois(k, lam):
                return math.exp(-lam) * lam ** k / math.factorial(k)

            print(round(pois(0, 3), 4), round(pois(2, 3), 4), round(1 - pois(0, 3), 4))
            """,
            """
            0.0498 0.224 0.9502
            """,
            """
            Dengan rata-rata tiga kejadian, peluang nol kejadian sekitar lima persen, tepat dua kejadian sekitar dua puluh dua persen, dan minimal satu kejadian sekitar sembilan puluh lima persen.
            """,
            filename="poisson.py",
        ),
        T("""
        ## Syarat Poisson

        Poisson cocok bila kejadian terjadi satu per satu, saling independen, dengan laju rata-rata konstan sepanjang selang. Panggilan telepon yang datang acak memenuhi ini. Tetapi kejadian berkerumun, seperti gempa susulan, atau laju yang berubah menurut jam sibuk, melanggarnya dan membuat variansnya jauh melebihi rata-rata.

        Ciri khas Poisson: rata-rata sama dengan varians, yaitu `lambda`. Bila data hitungan memiliki varians jauh lebih besar dari rata-rata, itu disebut overdispersi dan menandakan model lain, seperti binomial negatif, lebih sesuai.
        """),
        C(
            """
            import math

            lam = 3
            pmf = [math.exp(-lam) * lam ** k / math.factorial(k) for k in range(60)]
            mean = sum(k * p for k, p in enumerate(pmf))
            var = sum((k - mean) ** 2 * p for k, p in enumerate(pmf))
            print(round(mean, 4), round(var, 4))
            """,
            """
            3.0 3.0
            """,
            """
            Jumlah langsung membuktikan bahwa rata-rata dan varians Poisson sama dengan parameternya.
            """,
            filename="poisson_mean_var.py",
        ),
        T("""
        ## Menyesuaikan laju dengan skala

        Parameter `lambda` berlaku untuk selang tertentu, dan harus diskalakan bila selangnya berubah. Pusat layanan menerima empat panggilan per jam. Untuk setengah jam, `lambda = 2`. Untuk sepuluh menit, `lambda = 4/6`. Peluang tidak ada panggilan dalam setengah jam adalah `e^(-2)`, sekitar `0,1353`.

        Kesalahan umum adalah memakai `lambda` per jam untuk pertanyaan tentang menit. Selalu tulis satuan laju, dan ubah ke selang yang ditanyakan sebelum memakai rumus. Hubungan ini juga menghubungkan Poisson dengan eksponensial: waktu antar kejadian pada proses Poisson berdistribusi eksponensial dengan laju yang sama.
        """),
        C(
            """
            import math

            laju_per_jam = 4
            lam = laju_per_jam * 0.5
            print(round(math.exp(-lam), 4))
            """,
            """
            0.1353
            """,
            """
            Dalam setengah jam rata-rata dua panggilan, sehingga peluang tidak ada panggilan sekitar tiga belas persen.
            """,
            filename="skala_laju.py",
        ),
        T("""
        ## Poisson sebagai batas binomial

        Bila `n` besar dan `p` kecil dengan `n * p = lambda` sedang, binomial `(n, p)` sangat mirip Poisson `lambda`. Bayangkan satu jam dibagi menjadi seribu detik kecil, dan dalam tiap detik panggilan masuk dengan peluang kecil. Banyaknya panggilan adalah binomial dengan `n = 1000`, tetapi praktis berperilaku seperti Poisson.

        Aproksimasi ini berguna karena Poisson lebih mudah dihitung dan hanya butuh satu parameter. Ia akurat bila `n >= 100` dan `p <= 0,05` kira-kira. Untuk `p` yang besar, aproksimasi buruk dan binomial harus dipakai langsung.
        """),
        C(
            """
            import math

            n, p, k = 1000, 0.003, 2
            lam = n * p
            b = math.comb(n, k) * p ** k * (1 - p) ** (n - k)
            q = math.exp(-lam) * lam ** k / math.factorial(k)
            print(round(b, 4), round(q, 4))
            """,
            """
            0.2242 0.224
            """,
            """
            Binomial dengan seribu percobaan dan peluang kecil memberi hasil hampir sama dengan Poisson berparameter tiga.
            """,
            filename="binom_ke_poisson.py",
        ),
        K(
            "warn",
            """
            Bila varians hitungan jauh lebih besar dari rata-ratanya, Poisson tidak cocok. Periksa overdispersi sebelum memakainya.
            """,
            title="Cek varians",
        ),
        T("""
        ## Poisson dalam data science

        Poisson muncul sebagai model dasar untuk data hitungan: jumlah klik, jumlah pembelian, jumlah kesalahan sistem. Regresi Poisson memodelkan hitungan sebagai fungsi fitur dengan laju yang berubah tiap pengamatan, dan menjadi dasar banyak model permintaan dan risiko.

        Dalam pemantauan sistem, kita membandingkan hitungan yang diamati dengan peluang Poisson dari laju normal. Hitungan yang sangat tidak mungkin di bawah model Poisson, misalnya peluang di bawah seperseribu, menjadi alarm bahwa terjadi perubahan nyata.
        """),
        T("""
        ## Contoh perencanaan kapasitas

        Sebuah layanan menerima rata-rata dua belas permintaan per menit dan setiap server mampu menangani lima belas permintaan per menit. Dengan Poisson, peluang melebihi kapasitas pada satu menit adalah peluang minimal enam belas permintaan, yaitu ekor distribusi. Menghitung ekor ini menunjukkan seberapa sering antrean terbentuk walau rata-rata beban di bawah kapasitas.

        Inilah pelajaran inti perencanaan: rata-rata saja tidak cukup. Variabilitas Poisson berarti kapasitas harus dipasang di atas rata-rata dengan margin yang dipilih dari ekor distribusinya, bukan dari rata-ratanya.
        """),
        T("""
        ## Menguji kecocokan Poisson

        Untuk memeriksa apakah data hitungan cocok dengan Poisson, bandingkan rata-rata dan variansnya. Rasio mendekati satu mendukung model. Rasio jauh di atas satu menandakan overdispersi, dan jauh di bawah satu menandakan hitungan yang lebih teratur dari acak.

        Langkah kedua adalah membandingkan frekuensi relatif tiap nilai dengan PMF Poisson dari rata-rata sampel. Selisih besar pada nol, misalnya terlalu banyak hari tanpa kejadian, menandakan proses dengan banyak nol berlebih yang butuh model khusus.
        """),
        E(
            "A4-05-2-ex1",
            "mudah",
            """
            Tulis fungsi `pmf_poisson(k, lam)` yang mengembalikan `P(X = k)` dibulatkan 4 desimal, dan `0.0` bila `k < 0`.
            """,
            """
            import math

            def pmf_poisson(k, lam):
                # TODO: implementasikan
                pass
            """,
            """
            assert pmf_poisson(0, 3) == 0.0498
            assert pmf_poisson(2, 3) == 0.224
            assert pmf_poisson(5, 2) == 0.0361
            assert pmf_poisson(-1, 3) == 0.0
            assert pmf_poisson(0, 0) == 1.0
            """,
            "Pakai exp negatif lambda kali lambda pangkat k dibagi k faktorial.",
            """
            import math

            def pmf_poisson(k, lam):
                if k < 0:
                    return 0.0
                return round(math.exp(-lam) * lam ** k / math.factorial(k), 4)
            """,
        ),
        E(
            "A4-05-2-ex2",
            "sedang",
            """
            Tulis fungsi `cdf_poisson(k, lam)` yang mengembalikan `P(X <= k)` dibulatkan 4 desimal, dan `0.0` bila `k < 0`.
            """,
            """
            import math

            def cdf_poisson(k, lam):
                # TODO: implementasikan
                pass
            """,
            """
            assert cdf_poisson(2, 3) == 0.4232
            assert cdf_poisson(0, 3) == 0.0498
            assert cdf_poisson(-1, 3) == 0.0
            assert cdf_poisson(20, 3) == 1.0
            """,
            "Jumlahkan PMF dari nol sampai k.",
            """
            import math

            def cdf_poisson(k, lam):
                if k < 0:
                    return 0.0
                return round(sum(math.exp(-lam) * lam ** i / math.factorial(i) for i in range(k + 1)), 4)
            """,
        ),
        E(
            "A4-05-2-ex3",
            "sedang",
            """
            Tulis fungsi `peluang_minimal(lam, k)` yang mengembalikan `P(X >= k)` untuk Poisson, dibulatkan 4 desimal. Untuk `k <= 0` kembalikan 1.0.
            """,
            """
            import math

            def peluang_minimal(lam, k):
                # TODO: implementasikan
                pass
            """,
            """
            assert peluang_minimal(3, 1) == 0.9502
            assert peluang_minimal(3, 0) == 1.0
            assert peluang_minimal(3, 3) == 0.5768
            assert peluang_minimal(2, 4) == 0.1429
            """,
            "Pakai komplemen dari peluang paling banyak k minus satu.",
            """
            import math

            def peluang_minimal(lam, k):
                if k <= 0:
                    return 1.0
                return round(1 - sum(math.exp(-lam) * lam ** i / math.factorial(i) for i in range(k)), 4)
            """,
        ),
        E(
            "A4-05-2-ex4",
            "menantang",
            """
            Tulis fungsi `aproksimasi_poisson(n, p, k)` yang mengembalikan tuple `(binomial, poisson)` berisi `P(X = k)` binomial `(n, p)` dan Poisson dengan `lambda = n * p`, keduanya dibulatkan 4 desimal.
            """,
            """
            import math

            def aproksimasi_poisson(n, p, k):
                # TODO: implementasikan
                pass
            """,
            """
            assert aproksimasi_poisson(1000, 0.003, 2) == (0.2242, 0.224)
            assert aproksimasi_poisson(100, 0.05, 3) == (0.1396, 0.1404)
            b, q = aproksimasi_poisson(10, 0.5, 5)
            assert b == 0.2461 and q == 0.1755
            """,
            "Hitung PMF binomial dan PMF Poisson dengan lambda sama dengan n kali p.",
            """
            import math

            def aproksimasi_poisson(n, p, k):
                lam = n * p
                b = math.comb(n, k) * p ** k * (1 - p) ** (n - k)
                q = math.exp(-lam) * lam ** k / math.factorial(k)
                return (round(b, 4), round(q, 4))
            """,
        ),
    ],
    [
        M("Memakai laju per jam untuk pertanyaan per menit.", "Skalakan lambda ke selang yang ditanyakan."),
        M("Memakai Poisson pada data berkerumun.", "Periksa rata-rata sama dengan varians."),
        M("Memakai aproksimasi Poisson saat p besar.", "Gunakan binomial langsung."),
    ],
    [
        Q("Poisson memodelkan?", ["Jumlah kejadian per selang", "Waktu tunggu", "Rata-rata", "Proporsi"], 0, "Hitungan kejadian.", hint="Hitungan."),
        Q("Rata-rata dan varians Poisson?", ["Sama dengan lambda", "Berbeda", "Nol", "Satu"], 0, "Keduanya lambda.", hint="Satu parameter."),
        Q("Empat per jam, lambda untuk 30 menit?", ["4", "2", "8", "1"], 1, "Skalakan selang.", hint="Setengah."),
        Q("Poisson dekat binomial bila?", ["n besar p kecil", "n kecil p besar", "p setengah", "n satu"], 0, "Kejadian langka.", hint="Langka."),
        Q("Waktu antar kejadian Poisson?", ["Eksponensial", "Binomial", "Seragam", "Geometrik"], 0, "Laju sama.", hint="Waktu tunggu."),
    ],
    [
        "Poisson memodelkan hitungan kejadian acak per selang.",
        "Rata-rata dan varians sama dengan lambda.",
        "Lambda harus diskalakan sesuai selang.",
        "Poisson mengaproksimasi binomial untuk kejadian langka.",
    ],
    [],
)

l3 = lesson(
    "A4-05-3",
    "Distribusi normal",
    35,
    [
        "Menjelaskan bentuk dan parameter distribusi normal",
        "Menghitung CDF normal dengan fungsi galat dan z-score",
        "Memakai aturan 68-95-99,7",
        "Menghitung kuantil normal dan memeriksa asal normal dari banyak penjumlahan",
    ],
    [
        T("""
        ## Lonceng yang ada di mana-mana

        Distribusi **normal** atau Gaussian adalah kurva lonceng simetris yang muncul di banyak tempat: tinggi badan, galat pengukuran, skor tes, dan rata-rata sampel. Ia ditentukan dua parameter, rata-rata `mu` yang menentukan pusat dan simpangan baku `sigma` yang menentukan lebar. Sekitar `mu` kepadatan tertinggi, dan makin jauh makin rendah dengan cepat.

        Alasan kemunculannya yang luas adalah teorema limit pusat yang dibahas di modul akhir: jumlah banyak pengaruh kecil yang independen cenderung berdistribusi normal, apa pun distribusi asal masing-masing pengaruh.
        """),
        T("""
        ## Normal baku dan z-score

        Normal dengan `mu = 0` dan `sigma = 1` disebut **normal baku**. Semua normal dapat diubah ke normal baku dengan **z-score**: `z = (x - mu) / sigma`, yaitu berapa simpangan baku `x` dari rata-rata. Tinggi 186 cm pada populasi dengan rata-rata 170 dan simpangan baku 8 memiliki `z = 2`, dua simpangan baku di atas rata-rata.

        Transformasi ini membuat satu tabel atau satu fungsi cukup untuk semua normal. Z-score juga dipakai untuk membandingkan nilai dari skala berbeda dan untuk standarisasi fitur sebelum pelatihan model.
        """),
        T("""
        ## CDF normal

        CDF normal baku, ditulis `Phi(z)`, tidak punya rumus dasar tetapi dapat dihitung dengan fungsi galat: `Phi(z) = 0,5 * (1 + erf(z / sqrt(2)))`. Python menyediakan `math.erf`. Dengan `Phi`, peluang apa pun pada normal umum dihitung dengan mengubah ke z-score terlebih dahulu.

        Sifat simetri berguna: `Phi(-z) = 1 - Phi(z)`. Karena itu `Phi(0) = 0,5`, dan peluang di atas `z` sama dengan peluang di bawah `-z`. Ekor atas dihitung sebagai `1 - Phi(z)`.
        """),
        C(
            """
            import math

            def Phi(x):
                return 0.5 * (1 + math.erf(x / math.sqrt(2)))

            print(round(Phi(0), 4), round(Phi(1.96), 4), round(Phi(-1.96), 4))
            """,
            """
            0.5 0.975 0.025
            """,
            """
            Setengah massa di bawah rata-rata, dan nilai kritis seratus sembilan puluh enam menyisakan dua koma lima persen di tiap ekor.
            """,
            filename="phi.py",
        ),
        T("""
        ## Aturan 68-95-99,7

        Aturan empiris merangkum seberapa terkonsentrasi normal. Sekitar 68 persen massa berada dalam satu simpangan baku dari rata-rata, 95 persen dalam dua, dan 99,7 persen dalam tiga. Nilai yang lebih dari tiga simpangan baku dari rata-rata sangat jarang, sekitar tiga per seribu.

        Aturan ini membantu penilaian cepat: nilai dengan `|z| > 3` patut dicurigai sebagai pencilan atau kesalahan data. Namun ingat aturan ini hanya berlaku bila data memang kira-kira normal. Pada data berekor tebal, nilai ekstrem jauh lebih sering.
        """),
        C(
            """
            import math

            def Phi(x):
                return 0.5 * (1 + math.erf(x / math.sqrt(2)))

            print([round(Phi(k) - Phi(-k), 4) for k in (1, 2, 3)])
            mu, sigma, x = 170, 8, 186
            z = (x - mu) / sigma
            print(z, round(1 - Phi(z), 4))
            """,
            """
            [0.6827, 0.9545, 0.9973]
            2.0 0.0228
            """,
            """
            Aturan satu, dua, dan tiga simpangan baku cocok dengan hitungan. Tinggi di atas seratus delapan puluh enam senti hanya dimiliki sekitar dua persen populasi.
            """,
            filename="aturan_empiris.py",
        ),
        T("""
        ## Kuantil normal

        Untuk mencari nilai dengan peluang kumulatif tertentu kita perlu invers `Phi`. Karena tidak ada rumus tertutup sederhana, kita mencarinya secara numerik, misalnya dengan **bisection**: tebak rentang, ambil titik tengah, dan pilih setengah rentang yang masih mengandung jawaban. Dalam seratus iterasi hasilnya sangat teliti.

        Kuantil terkenal: 0,975 memberi `z = 1,96` yang dipakai untuk interval kepercayaan 95 persen, dan 0,95 memberi `1,645` untuk uji satu sisi. Pustaka seperti SciPy menyediakan fungsi ini langsung, tetapi menulisnya sekali membuat kamu paham cara kerjanya.
        """),
        C(
            """
            import math

            def Phi(x):
                return 0.5 * (1 + math.erf(x / math.sqrt(2)))

            def kuantil(q):
                lo, hi = -10.0, 10.0
                for _ in range(100):
                    mid = (lo + hi) / 2
                    if Phi(mid) < q:
                        lo = mid
                    else:
                        hi = mid
                return (lo + hi) / 2

            print(round(kuantil(0.975), 2), round(kuantil(0.9), 2))
            """,
            """
            1.96 1.28
            """,
            """
            Pencarian biner menemukan nilai kritis seratus sembilan puluh enam dan seratus dua puluh delapan.
            """,
            filename="kuantil_normal.py",
        ),
        T("""
        ## Normal dari penjumlahan

        Mengapa normal begitu umum? Jumlah banyak variabel kecil independen cenderung normal. Contoh klasik: jumlah dua belas bilangan seragam pada `[0, 1]` dikurangi enam memiliki rata-rata nol dan varians satu, dan bentuknya sudah sangat mirip normal baku. Dulu trik ini dipakai untuk menghasilkan bilangan normal di komputer sederhana.

        Fenomena ini adalah isi teorema limit pusat dan menjelaskan mengapa galat pengukuran, yang menumpuk dari banyak gangguan kecil, hampir selalu tampak normal.
        """),
        C(
            """
            import random
            import statistics

            random.seed(3)
            xs = [sum(random.random() for _ in range(12)) - 6 for _ in range(20000)]
            print(abs(statistics.mean(xs)) < 0.05)
            print(abs(statistics.pstdev(xs) - 1) < 0.05)
            """,
            """
            True
            True
            """,
            """
            Jumlah dua belas seragam yang dipusatkan memiliki rata-rata mendekati nol dan simpangan baku mendekati satu.
            """,
            filename="jumlah_seragam.py",
        ),
        K(
            "tip",
            """
            Sebelum memakai aturan 68-95-99,7 atau tabel normal, periksa kenormalan data dengan histogram atau plot kuantil. Data berekor tebal membuat aturan itu terlalu optimis.
            """,
            title="Cek kenormalan",
        ),
        T("""
        ## Standarisasi fitur

        Z-score bukan hanya alat hitung peluang. Dalam machine learning, standarisasi fitur, yaitu mengurangi rata-rata dan membagi simpangan baku, membuat semua fitur berskala sebanding. Model berbasis jarak seperti k-NN dan model berbasis gradien seperti regresi logistik jauh lebih stabil dan cepat konvergen ketika fitur terstandarisasi.

        Ingat untuk menghitung rata-rata dan simpangan baku hanya dari data latih lalu menerapkannya ke data uji. Menghitungnya dari seluruh data membocorkan informasi uji ke pelatihan dan membuat evaluasi terlalu optimis.
        """),
        E(
            "A4-05-3-ex1",
            "mudah",
            """
            Tulis fungsi `cdf_normal(x, mu, sigma)` yang mengembalikan `P(X <= x)` dibulatkan 4 desimal, memakai `math.erf` pada z-score.
            """,
            """
            import math

            def cdf_normal(x, mu, sigma):
                # TODO: implementasikan
                pass
            """,
            """
            assert cdf_normal(0, 0, 1) == 0.5
            assert cdf_normal(1.96, 0, 1) == 0.975
            assert cdf_normal(186, 170, 8) == 0.9772
            assert cdf_normal(-1.96, 0, 1) == 0.025
            assert cdf_normal(170, 170, 8) == 0.5
            """,
            "Ubah ke z-score lalu pakai setengah kali satu tambah erf z per akar dua.",
            """
            import math

            def cdf_normal(x, mu, sigma):
                z = (x - mu) / sigma
                return round(0.5 * (1 + math.erf(z / math.sqrt(2))), 4)
            """,
        ),
        E(
            "A4-05-3-ex2",
            "sedang",
            """
            Tulis fungsi `z_score(x, mu, sigma)` yang mengembalikan `(x - mu) / sigma` dibulatkan 4 desimal. Hindari `-0.0`.
            """,
            """
            def z_score(x, mu, sigma):
                # TODO: implementasikan
                pass
            """,
            """
            assert z_score(186, 170, 8) == 2.0
            assert z_score(160, 170, 8) == -1.25
            assert z_score(170, 170, 8) == 0.0
            assert z_score(5, 3, 0.5) == 4.0
            """,
            "Kurangi rata-rata lalu bagi dengan simpangan baku.",
            """
            def z_score(x, mu, sigma):
                return round((x - mu) / sigma, 4) + 0.0
            """,
        ),
        E(
            "A4-05-3-ex3",
            "sedang",
            """
            Tulis fungsi `peluang_antara(a, b, mu, sigma)` yang mengembalikan `P(a <= X <= b)` untuk normal `(mu, sigma)`, dibulatkan 4 desimal.
            """,
            """
            import math

            def peluang_antara(a, b, mu, sigma):
                # TODO: implementasikan
                pass
            """,
            """
            assert peluang_antara(-1, 1, 0, 1) == 0.6827
            assert peluang_antara(-2, 2, 0, 1) == 0.9545
            assert peluang_antara(160, 180, 170, 8) == 0.7887
            assert peluang_antara(0, 0, 0, 1) == 0.0
            """,
            "Kurangkan CDF batas bawah dari CDF batas atas.",
            """
            import math

            def peluang_antara(a, b, mu, sigma):
                F = lambda x: 0.5 * (1 + math.erf((x - mu) / sigma / math.sqrt(2)))
                return round(F(b) - F(a), 4)
            """,
        ),
        E(
            "A4-05-3-ex4",
            "menantang",
            """
            Tulis fungsi `kuantil_normal(q, mu, sigma)` yang mencari nilai `x` dengan CDF sama dengan `q` memakai bisection pada rentang `mu - 10 * sigma` sampai `mu + 10 * sigma` dengan 100 iterasi. Bulatkan 2 desimal dan hindari `-0.0`.
            """,
            """
            import math

            def kuantil_normal(q, mu, sigma):
                # TODO: implementasikan
                pass
            """,
            """
            assert kuantil_normal(0.975, 0, 1) == 1.96
            assert kuantil_normal(0.5, 0, 1) == 0.0
            assert kuantil_normal(0.5, 170, 8) == 170.0
            assert kuantil_normal(0.9, 0, 1) == 1.28
            assert kuantil_normal(0.025, 0, 1) == -1.96
            """,
            "Persempit rentang berulang kali dengan membandingkan CDF di titik tengah terhadap q.",
            """
            import math

            def kuantil_normal(q, mu, sigma):
                F = lambda x: 0.5 * (1 + math.erf((x - mu) / sigma / math.sqrt(2)))
                lo, hi = mu - 10 * sigma, mu + 10 * sigma
                for _ in range(100):
                    mid = (lo + hi) / 2
                    if F(mid) < q:
                        lo = mid
                    else:
                        hi = mid
                return round((lo + hi) / 2, 2) + 0.0
            """,
        ),
    ],
    [
        M("Memakai aturan 68-95-99,7 pada data tidak normal.", "Periksa bentuk distribusi dulu."),
        M("Lupa standarisasi sebelum memakai Phi.", "Hitung z-score lebih dulu."),
        M("Menafsirkan nilai PDF normal sebagai peluang.", "Pakai luas atau CDF."),
    ],
    [
        Q("Parameter normal?", ["Rata-rata dan simpangan baku", "n dan p", "Lambda", "a dan b"], 0, "Pusat dan lebar.", hint="Mu sigma."),
        Q("Z-score adalah?", ["(x - mu) / sigma", "x / sigma", "mu / x", "sigma - x"], 0, "Jarak dalam simpangan baku.", hint="Standarisasi."),
        Q("Massa dalam dua simpangan baku?", ["68%", "95%", "99,7%", "50%"], 1, "Aturan empiris.", hint="Dua."),
        Q("Phi(0)?", ["0", "0,5", "1", "-1"], 1, "Simetri.", hint="Setengah."),
        Q("Mengapa normal umum?", ["Semua data normal", "Jumlah banyak pengaruh kecil cenderung normal", "Mudah dihitung", "Selalu simetris"], 1, "Teorema limit pusat.", hint="Penjumlahan."),
    ],
    [
        "Normal ditentukan rata-rata dan simpangan baku.",
        "Z-score mengubah normal apa pun ke normal baku.",
        "Aturan 68-95-99,7 merangkum konsentrasi massa.",
        "Kuantil normal dihitung numerik dari invers CDF.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perhitungan yang cukup jelas dalam teks.", "brief": []}

write_module(
    "A4",
    5,
    "Distribusi yang sering dipakai",
    105,
    [
        "Memilih dan memakai binomial, geometrik, dan Poisson",
        "Menghitung probabilitas normal dengan z-score",
        "Mengenali cerita di balik tiap distribusi",
    ],
    [l1, l2, l3],
    video,
    REF,
)
