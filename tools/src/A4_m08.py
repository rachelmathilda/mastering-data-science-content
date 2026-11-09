import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

l1 = lesson(
    "A4-08-1",
    "Menaksir peluang dengan simulasi",
    35,
    [
        "Menjelaskan logika simulasi Monte Carlo",
        "Menaksir peluang kejadian sebagai proporsi hasil simulasi",
        "Menaksir nilai pi dengan titik acak",
        "Menyimulasikan masalah ulang tahun dan Monty Hall",
    ],
    [
        T("""
        ## Menghitung dengan mengulang

        Tidak semua peluang bisa dihitung dengan rumus. Sistem nyata seperti antrean, jaringan, atau permainan dengan banyak aturan terlalu rumit untuk dianalisis dengan tangan. Metode **Monte Carlo** mengambil jalan lain: jalankan percobaan acak itu di komputer berkali-kali dan lihat seberapa sering kejadian yang kita minati terjadi.

        Dasarnya adalah hukum bilangan besar yang sudah kamu pelajari. Proporsi kejadian dalam banyak ulangan mendekati peluang sebenarnya. Nama Monte Carlo berasal dari kasino, merujuk pada unsur kebetulan, dan metode ini diciptakan saat proyek fisika nuklir pada pertengahan abad ke-20.
        """),
        T("""
        ## Resep dasar

        Resepnya selalu tiga langkah. Pertama, tuliskan kode yang menyimulasikan satu kali percobaan dan mengembalikan benar atau salah untuk kejadian yang diminati. Kedua, ulangi `n` kali dengan angka acak independen. Ketiga, taksir peluang sebagai banyaknya benar dibagi `n`.

        Gunakan generator acak dengan benih tetap, misalnya `random.Random(seed)`, supaya hasil dapat diulang dan dicek. Tanpa benih, hasil berubah tiap dijalankan dan sulit mencari bug. Dalam produksi benih bisa dibuat acak, tetapi saat pengembangan benih tetap adalah sahabat debugging.
        """),
        C(
            """
            import random

            r = random.Random(1)
            n = 20000
            tujuh = sum(r.randint(1, 6) + r.randint(1, 6) == 7 for _ in range(n))
            print(abs(tujuh / n - 1 / 6) < 0.02)
            """,
            """
            True
            """,
            """
            Proporsi jumlah tujuh dari dua puluh ribu lemparan dua dadu mendekati satu per enam.
            """,
            filename="mc_dadu.py",
        ),
        T("""
        ## Menaksir pi

        Contoh klasik: taburkan titik acak seragam di persegi satuan `[0, 1] x [0, 1]`. Seperempat lingkaran berjari-jari satu menempati wilayah dengan `x^2 + y^2 <= 1`, dengan luas `pi / 4`. Proporsi titik yang jatuh di dalam seperempat lingkaran mendekati `pi / 4`, sehingga `pi` dapat ditaksir dengan empat kali proporsi itu.

        Contoh ini bukan cara efisien menghitung pi, karena galatnya hanya turun sebagai satu per akar `n`. Tetapi ia memperlihatkan ide inti: luas atau peluang yang sulit dihitung dapat ditaksir dengan menembakkan titik acak dan menghitung yang mengenai sasaran.
        """),
        C(
            """
            import random

            r = random.Random(2)
            n = 200000
            dalam = sum(r.random() ** 2 + r.random() ** 2 <= 1 for _ in range(n))
            print(abs(4 * dalam / n - 3.1416) < 0.05)
            """,
            """
            True
            """,
            """
            Empat kali proporsi titik di dalam seperempat lingkaran memberi taksiran pi yang dekat dengan nilai sebenarnya.
            """,
            filename="mc_pi.py",
        ),
        T("""
        ## Masalah ulang tahun lewat simulasi

        Di pelajaran sebelumnya kita menghitung peluang ulang tahun sama dengan rumus. Kini kita bisa menyimulasikannya tanpa rumus sama sekali: ambil `k` ulang tahun acak dari 365 hari dan periksa apakah ada duplikat dengan `len(set(...)) < k`. Ulangi banyak kali dan hitung proporsinya.

        Keunggulan simulasi di sini adalah mudah dimodifikasi. Bila kamu ingin menambah aturan, seperti tahun kabisat atau hari lahir yang tidak seragam, kodenya hanya perlu sedikit diubah, sedangkan rumus eksaknya mungkin tidak ada.
        """),
        C(
            """
            import random

            r = random.Random(3)
            k, n = 23, 20000
            sama = sum(len({r.randrange(365) for _ in range(k)}) < k for _ in range(n))
            print(abs(sama / n - 0.5073) < 0.03)
            """,
            """
            True
            """,
            """
            Simulasi untuk dua puluh tiga orang memberi peluang ulang tahun sama yang cocok dengan hitungan rumus.
            """,
            filename="mc_ulang_tahun.py",
        ),
        T("""
        ## Masalah Monty Hall

        Kamu memilih satu dari tiga pintu, satu menyembunyikan mobil. Pembawa acara yang tahu letak mobil membuka satu pintu lain yang kosong lalu menawarkan kamu berganti. Apakah berganti menguntungkan? Banyak orang menjawab peluangnya sama, setengah, tetapi jawaban benar: berganti menang dengan peluang dua pertiga.

        Simulasi menyelesaikan perdebatan ini tanpa argumen rumit. Tulis aturan persis seperti dalam soal, jalankan ribuan kali, dan hitung hasilnya. Simulasi yang jujur terhadap aturan lebih meyakinkan daripada intuisi yang bisa tertipu.
        """),
        C(
            """
            import random

            r = random.Random(4)
            n = 20000
            ganti = tetap = 0
            for _ in range(n):
                mobil = r.randrange(3)
                pilih = r.randrange(3)
                buka = next(p for p in range(3) if p != pilih and p != mobil)
                akhir = next(p for p in range(3) if p != pilih and p != buka)
                ganti += akhir == mobil
                tetap += pilih == mobil
            print(abs(ganti / n - 2 / 3) < 0.03, abs(tetap / n - 1 / 3) < 0.03)
            """,
            """
            True True
            """,
            """
            Berganti pintu menang sekitar dua pertiga kali dan bertahan menang sekitar sepertiga kali.
            """,
            filename="mc_monty_hall.py",
        ),
        K(
            "tip",
            """
            Selalu pakai random.Random(seed) yang dibuat sekali dan dipakai ulang, bukan random.seed global di tengah fungsi. Itu membuat simulasi dapat diulang dan tidak saling mengganggu.
            """,
            title="Benih acak",
        ),
        T("""
        ## Simulasi sebagai alat verifikasi

        Simulasi paling kuat bila dipakai berdampingan dengan teori. Untuk soal yang punya jawaban eksak, jalankan simulasi sebagai uji akal sehat: bila hasilnya jauh berbeda, ada kesalahan di rumus atau di kode. Untuk soal yang tidak punya jawaban eksak, simulasi adalah satu-satunya alat, dan keandalannya dinilai dari galat bakunya.

        Kebiasaan ini membuat kamu tidak percaya begitu saja pada rumus maupun kode. Dua pendekatan independen yang sepakat memberi keyakinan jauh lebih besar daripada salah satu saja.
        """),
        T("""
        ## Pembangkit bilangan acak

        Komputer tidak benar-benar acak. Fungsi acak memakai algoritma deterministik yang menghasilkan barisan bilangan yang secara statistik tampak acak, disebut pseudo-acak. Benih menentukan titik awal barisan: benih sama menghasilkan barisan sama. Untuk simulasi ilmiah ini justru keunggulan, karena hasilnya dapat direproduksi oleh orang lain.

        Untuk keamanan seperti kata sandi, pseudo-acak biasa tidak cukup karena dapat ditebak. Pakai modul khusus seperti secrets. Untuk simulasi Monte Carlo, generator standar sudah memadai selama kamu tidak menyalahgunakan benih yang sama untuk percobaan yang seharusnya independen.
        """),
        T("""
        ## Tiga kesalahan pemula

        Pertama, jumlah ulangan terlalu sedikit sehingga taksiran masih berderau. Kedua, menggunakan benih yang sama untuk dua simulasi yang seharusnya independen, yang membuat keduanya berkorelasi. Ketiga, tidak memeriksa hasil dengan kasus yang jawabannya diketahui. Menjalankan simulasi pada versi sederhana dengan jawaban pasti sebelum menyerang versi rumit adalah praktik yang sangat dianjurkan.
        """),
        E(
            "A4-08-1-ex1",
            "mudah",
            """
            Tulis fungsi `taksir_peluang(kejadian, trial, seed)` yang membuat `random.Random(seed)`, memanggil `kejadian(r)` sebanyak `trial` kali, dan mengembalikan proporsi pemanggilan yang bernilai True.
            """,
            """
            import random

            def taksir_peluang(kejadian, trial, seed):
                # TODO: implementasikan
                pass
            """,
            """
            assert abs(taksir_peluang(lambda r: r.random() < 0.3, 10000, 1) - 0.3) < 0.03
            assert abs(taksir_peluang(lambda r: r.randint(1, 6) + r.randint(1, 6) == 7, 20000, 2) - 1 / 6) < 0.02
            assert taksir_peluang(lambda r: False, 100, 3) == 0.0
            assert taksir_peluang(lambda r: True, 100, 3) == 1.0
            """,
            "Buat satu generator lalu hitung berapa kali kejadian bernilai benar.",
            """
            import random

            def taksir_peluang(kejadian, trial, seed):
                r = random.Random(seed)
                return sum(1 for _ in range(trial) if kejadian(r)) / trial
            """,
        ),
        E(
            "A4-08-1-ex2",
            "sedang",
            """
            Tulis fungsi `taksir_pi(n, seed)` yang menaksir pi dengan `n` titik acak seragam di persegi satuan memakai `random.Random(seed)`, yaitu `4 * (banyak titik dengan x^2 + y^2 <= 1) / n`.
            """,
            """
            import random

            def taksir_pi(n, seed):
                # TODO: implementasikan
                pass
            """,
            """
            assert abs(taksir_pi(100000, 1) - 3.1416) < 0.05
            assert abs(taksir_pi(50000, 2) - 3.1416) < 0.06
            assert 0 <= taksir_pi(10, 3) <= 4
            """,
            "Tarik x dan y dari generator lalu hitung titik yang berada dalam seperempat lingkaran.",
            """
            import random

            def taksir_pi(n, seed):
                r = random.Random(seed)
                dalam = 0
                for _ in range(n):
                    x = r.random()
                    y = r.random()
                    if x * x + y * y <= 1:
                        dalam += 1
                return 4 * dalam / n
            """,
        ),
        E(
            "A4-08-1-ex3",
            "sedang",
            """
            Tulis fungsi `simulasi_ulang_tahun(orang, trial, seed)` yang menaksir peluang minimal dua dari `orang` memiliki hari lahir sama (365 hari seragam) memakai `random.Random(seed)`, dan mengembalikan proporsinya.
            """,
            """
            import random

            def simulasi_ulang_tahun(orang, trial, seed):
                # TODO: implementasikan
                pass
            """,
            """
            assert abs(simulasi_ulang_tahun(23, 20000, 1) - 0.5073) < 0.03
            assert abs(simulasi_ulang_tahun(60, 5000, 2) - 0.9941) < 0.02
            assert simulasi_ulang_tahun(1, 100, 3) == 0.0
            """,
            "Ambil hari lahir acak untuk tiap orang dan periksa apakah ada duplikat memakai set.",
            """
            import random

            def simulasi_ulang_tahun(orang, trial, seed):
                r = random.Random(seed)
                sama = 0
                for _ in range(trial):
                    hari = [r.randrange(365) for _ in range(orang)]
                    if len(set(hari)) < orang:
                        sama += 1
                return sama / trial
            """,
        ),
        E(
            "A4-08-1-ex4",
            "menantang",
            """
            Tulis fungsi `simulasi_monty_hall(trial, seed, ganti)` yang menyimulasikan permainan tiga pintu dengan `random.Random(seed)` dan mengembalikan proporsi kemenangan. Pembawa acara membuka satu pintu kosong selain pilihan pemain. Bila `ganti` True pemain pindah ke pintu yang tersisa.
            """,
            """
            import random

            def simulasi_monty_hall(trial, seed, ganti):
                # TODO: implementasikan
                pass
            """,
            """
            assert abs(simulasi_monty_hall(20000, 1, True) - 2 / 3) < 0.03
            assert abs(simulasi_monty_hall(20000, 2, False) - 1 / 3) < 0.03
            assert abs(simulasi_monty_hall(10000, 5, True) + simulasi_monty_hall(10000, 5, False) - 1) < 0.06
            """,
            "Tentukan pintu yang dibuka lalu hitung pintu akhir sesuai strategi.",
            """
            import random

            def simulasi_monty_hall(trial, seed, ganti):
                r = random.Random(seed)
                menang = 0
                for _ in range(trial):
                    mobil = r.randrange(3)
                    pilih = r.randrange(3)
                    buka = next(p for p in range(3) if p != pilih and p != mobil)
                    akhir = next(p for p in range(3) if p != pilih and p != buka) if ganti else pilih
                    if akhir == mobil:
                        menang += 1
                return menang / trial
            """,
        ),
    ],
    [
        M("Tidak memakai benih sehingga hasil tidak dapat diulang.", "Pakai random.Random(seed)."),
        M("Percaya satu simulasi pendek.", "Periksa galat baku dan banyak ulangan."),
        M("Menyimulasikan aturan yang berbeda dari soal.", "Tulis aturan persis seperti soal."),
    ],
    [
        Q("Monte Carlo menaksir peluang dengan?", ["Rumus", "Proporsi hasil simulasi", "Tebakan", "Median"], 1, "Hukum bilangan besar.", hint="Ulangi."),
        Q("Taksiran pi memakai?", ["Titik acak dalam persegi", "Faktorial", "Deret", "Median"], 0, "Luas seperempat lingkaran.", hint="Titik."),
        Q("Berganti pintu pada Monty Hall menang?", ["1/3", "1/2", "2/3", "1"], 2, "Dua pertiga.", hint="Lebih dari setengah."),
        Q("Galat simulasi turun sebagai?", ["1/n", "1/akar n", "n", "tetap"], 1, "Seperti rata-rata.", hint="Akar."),
        Q("Mengapa benih tetap?", ["Agar hasil dapat diulang", "Agar lebih cepat", "Agar akurat", "Agar acak"], 0, "Memudahkan debugging.", hint="Ulang."),
    ],
    [
        "Monte Carlo menaksir peluang dengan proporsi hasil simulasi.",
        "Titik acak menaksir luas dan nilai pi.",
        "Simulasi memverifikasi dan menyelesaikan masalah tanpa rumus.",
        "Benih tetap membuat simulasi dapat diulang.",
    ],
    [],
)

l2 = lesson(
    "A4-08-2",
    "Integrasi Monte Carlo dan galat taksiran",
    35,
    [
        "Menaksir integral sebagai ekspektasi dari titik acak",
        "Menaksir galat baku taksiran Monte Carlo",
        "Menghitung ukuran simulasi yang dibutuhkan",
        "Menaksir luas wilayah dengan hit-or-miss",
    ],
    [
        T("""
        ## Integral sebagai rata-rata

        Integral `f` dari `a` sampai `b` dapat dilihat sebagai `(b - a)` kali nilai rata-rata `f` pada rentang itu. Bila `U` seragam pada `[a, b]`, maka rata-rata `f(U)` memiliki ekspektasi `integral / (b - a)`. Karena itu kita bisa menaksir integral dengan mengambil banyak titik acak seragam, menghitung `f` di tiap titik, merata-ratakan, dan mengalikan dengan lebar rentang.

        Ini integrasi Monte Carlo. Untuk fungsi satu dimensi yang mulus, aturan titik tengah lebih akurat. Keunggulan Monte Carlo tampak pada dimensi tinggi, tempat grid teratur menjadi mustahil karena jumlah titik meledak, sedangkan galat Monte Carlo tetap turun sebagai satu per akar `n` tanpa peduli dimensi.
        """),
        C(
            """
            import random

            r = random.Random(1)
            n = 100000
            est = sum(r.random() ** 2 for _ in range(n)) / n
            print(abs(est - 1 / 3) < 0.01)
            """,
            """
            True
            """,
            """
            Rata-rata x kuadrat di titik acak seragam mendekati sepertiga, yaitu integralnya dari nol sampai satu.
            """,
            filename="mc_integral.py",
        ),
        T("""
        ## Rentang umum

        Untuk rentang `[a, b]`, tarik `u = a + (b - a) * r.random()`, hitung `f(u)`, rata-ratakan, lalu kalikan dengan `b - a`. Integral `sin(x)` dari nol sampai pi bernilai tepat dua. Dengan seratus ribu titik, taksiran Monte Carlo biasanya berada dalam sekitar `0,01` dari dua.

        Keunggulan lain: tidak perlu turunan atau kehalusan fungsi. Selama kita dapat mengevaluasi `f`, kita dapat menaksir integralnya, bahkan bila `f` hasil simulasi lain atau model hitam.
        """),
        C(
            """
            import math
            import random

            r = random.Random(2)
            n = 100000
            a, b = 0, math.pi
            est = (b - a) * sum(math.sin(a + (b - a) * r.random()) for _ in range(n)) / n
            print(abs(est - 2) < 0.05)
            """,
            """
            True
            """,
            """
            Taksiran integral sinus dari nol sampai pi berada dekat dua.
            """,
            filename="mc_sin.py",
        ),
        T("""
        ## Galat baku taksiran

        Taksiran Monte Carlo adalah rata-rata sampel, sehingga galat bakunya `sigma / sqrt(n)` dengan `sigma` simpangan baku `f(U)` (dikali lebar rentang). Kita biasanya tidak tahu `sigma`, tetapi dapat menaksirnya dari simulasi yang sama dengan simpangan baku sampel. Maka setiap taksiran Monte Carlo seharusnya disertai galat bakunya.

        Dengan galat baku, kita dapat memberi interval kepercayaan `taksiran ± 1,96 SE`. Laporan tanpa galat adalah angka tanpa konteks: pembaca tidak tahu apakah dua desimal terakhir bermakna atau hanya derau.
        """),
        C(
            """
            import math
            import random
            import statistics

            r = random.Random(7)
            n = 50000
            nilai = [r.random() ** 2 for _ in range(n)]
            est = statistics.mean(nilai)
            se = statistics.stdev(nilai) / math.sqrt(n)
            print(abs(est - 1 / 3) < 3 * se, se < 0.002)
            """,
            """
            True True
            """,
            """
            Nilai sebenarnya berada dalam tiga galat baku dari taksiran, dan galat bakunya kecil untuk lima puluh ribu titik.
            """,
            filename="mc_galat.py",
        ),
        T("""
        ## Berapa banyak simulasi

        Karena `SE = sigma / sqrt(n)`, kita dapat merencanakan: untuk galat baku target `s`, butuh `n = (sigma / s)^2`. Fungsi `x^2` pada `[0, 1]` memiliki `sigma = sqrt(4/45)`, sekitar `0,298`. Galat baku `0,003` butuh sepuluh ribu titik, dan galat `0,0003` butuh satu juta titik.

        Hubungan akar ini menjelaskan batas praktis Monte Carlo: satu digit tambahan presisi menuntut seratus kali lebih banyak komputasi. Karena itu teknik pengurangan varians, yang menurunkan `sigma`, sangat berharga pada simulasi mahal.
        """),
        C(
            """
            import math

            sigma = math.sqrt(4 / 45)
            print(round(sigma / math.sqrt(100), 4), round(sigma / math.sqrt(10000), 4))
            """,
            """
            0.0298 0.003
            """,
            """
            Galat baku turun sepuluh kali lipat ketika jumlah titik naik seratus kali lipat.
            """,
            filename="mc_ukuran.py",
        ),
        T("""
        ## Hit-or-miss untuk luas

        Cara kedua menaksir luas wilayah tak beraturan: lingkupi dengan persegi panjang yang luasnya diketahui, taburkan titik acak seragam, dan hitung proporsi titik yang jatuh di wilayah. Luas wilayah sama dengan proporsi dikali luas persegi panjang. Ini generalisasi dari taksiran pi.

        Cukup tulis fungsi syarat yang mengembalikan benar bila titik berada di wilayah. Tidak perlu rumus luas, bahkan untuk bentuk rumit seperti irisan beberapa lingkaran atau wilayah yang didefinisikan oleh model.
        """),
        K(
            "tip",
            """
            Laporkan taksiran Monte Carlo bersama galat bakunya, dan pilih jumlah simulasi dari galat target, bukan dari tebakan.
            """,
            title="Selalu sertakan galat",
        ),
        T("""
        ## Dimensi tinggi

        Pada dimensi `d`, grid dengan sepuluh titik per sumbu membutuhkan `10^d` titik, sehingga mustahil untuk `d` di atas sedikit. Galat Monte Carlo tetap `sigma / sqrt(n)` terlepas dari dimensi. Inilah mengapa Monte Carlo menjadi alat utama di fisika, keuangan, dan statistika Bayesian, tempat integral berdimensi puluhan hingga ribuan harus dihitung.

        Namun `sigma` sendiri dapat membesar pada dimensi tinggi bila fungsi hanya bernilai besar di wilayah sangat kecil. Di situ pengambilan sampel penting atau metode rantai Markov lebih cocok daripada titik seragam.
        """),
        T("""
        ## Pengurangan varians

        Karena galat bergantung pada `sigma`, mengurangi `sigma` sama berharganya dengan menambah `n`. Salah satu teknik sederhana adalah variat antitetik: untuk tiap `u` yang ditarik, gunakan juga `1 - u`. Bila `f` monoton, `f(u)` dan `f(1 - u)` berkorelasi negatif sehingga rata-ratanya berfluktuasi lebih kecil daripada dua tarikan independen.

        Teknik lain adalah pengambilan sampel penting, yang menarik titik lebih sering di wilayah tempat fungsi bernilai besar lalu mengoreksi dengan bobot. Keduanya mengurangi varians tanpa menambah banyak komputasi, dan penting untuk simulasi yang mahal.
        """),
        T("""
        ## Kapan memakai Monte Carlo

        Pilih Monte Carlo ketika dimensi tinggi, aturan rumit, atau fungsi tidak mulus membuat metode analitik dan grid tidak praktis. Pilih metode deterministik seperti aturan titik tengah ketika dimensi rendah dan fungsi mulus, karena ia jauh lebih akurat untuk komputasi yang sama. Pemilihan alat yang tepat adalah bagian dari keterampilan, bukan sekadar menjalankan simulasi untuk semua hal.
        """),
        E(
            "A4-08-2-ex1",
            "mudah",
            """
            Tulis fungsi `integral_mc(f, a, b, n, seed)` yang menaksir integral `f` pada `[a, b]` dengan `n` titik seragam dari `random.Random(seed)`: `(b - a) * rata-rata f(u)`.
            """,
            """
            import random

            def integral_mc(f, a, b, n, seed):
                # TODO: implementasikan
                pass
            """,
            """
            import math
            assert abs(integral_mc(lambda x: x * x, 0, 1, 100000, 1) - 1 / 3) < 0.01
            assert abs(integral_mc(math.sin, 0, math.pi, 100000, 2) - 2) < 0.05
            assert integral_mc(lambda x: 3, 0, 2, 100, 3) == 6.0
            """,
            "Tarik titik seragam pada rentang dan rata-ratakan nilai fungsi.",
            """
            import random

            def integral_mc(f, a, b, n, seed):
                r = random.Random(seed)
                total = 0.0
                for _ in range(n):
                    total += f(a + (b - a) * r.random())
                return (b - a) * total / n
            """,
        ),
        E(
            "A4-08-2-ex2",
            "sedang",
            """
            Tulis fungsi `galat_baku_mc(f, a, b, n, seed)` yang mengembalikan tuple `(taksiran, se)` untuk integral `f` pada `[a, b]`. `se` adalah `(b - a) * stdev(f(u)) / sqrt(n)` dengan `statistics.stdev`.
            """,
            """
            import math
            import random
            import statistics

            def galat_baku_mc(f, a, b, n, seed):
                # TODO: implementasikan
                pass
            """,
            """
            est, se = galat_baku_mc(lambda x: x * x, 0, 1, 10000, 1)
            assert abs(se - 0.00298) < 0.0005
            assert abs(est - 1 / 3) < 4 * se
            est2, se2 = galat_baku_mc(lambda x: 5, 0, 3, 100, 2)
            assert est2 == 15.0 and se2 == 0.0
            """,
            "Simpan semua nilai fungsi lalu hitung rata-rata dan simpangan bakunya.",
            """
            import math
            import random
            import statistics

            def galat_baku_mc(f, a, b, n, seed):
                r = random.Random(seed)
                nilai = [f(a + (b - a) * r.random()) for _ in range(n)]
                est = (b - a) * statistics.mean(nilai)
                se = (b - a) * statistics.stdev(nilai) / math.sqrt(n)
                return (est, se)
            """,
        ),
        E(
            "A4-08-2-ex3",
            "sedang",
            """
            Tulis fungsi `n_diperlukan(sigma, target_se)` yang mengembalikan banyaknya titik terkecil (bilangan bulat) agar `sigma / sqrt(n) <= target_se`, yaitu `ceil((sigma / target_se) ** 2)`.
            """,
            """
            import math

            def n_diperlukan(sigma, target_se):
                # TODO: implementasikan
                pass
            """,
            """
            assert n_diperlukan(1, 0.1) == 100
            assert n_diperlukan(2, 0.01) == 40000
            assert n_diperlukan(0.5, 0.05) == 100
            assert n_diperlukan(3, 1) == 9
            """,
            "Balikkan rumus galat baku untuk n dan bulatkan ke atas.",
            """
            import math

            def n_diperlukan(sigma, target_se):
                return math.ceil((sigma / target_se) ** 2)
            """,
        ),
        E(
            "A4-08-2-ex4",
            "menantang",
            """
            Tulis fungsi `luas_mc(syarat, xr, yr, n, seed)` yang menaksir luas wilayah dengan hit-or-miss. `xr` dan `yr` adalah tuple `(min, max)` persegi panjang pembungkus, `syarat(x, y)` bernilai True di dalam wilayah. Kembalikan proporsi titik di dalam dikali luas persegi panjang.
            """,
            """
            import random

            def luas_mc(syarat, xr, yr, n, seed):
                # TODO: implementasikan
                pass
            """,
            """
            assert abs(luas_mc(lambda x, y: x * x + y * y <= 1, (-1, 1), (-1, 1), 100000, 1) - 3.1416) < 0.05
            assert abs(luas_mc(lambda x, y: x < y, (0, 1), (0, 1), 50000, 2) - 0.5) < 0.02
            assert luas_mc(lambda x, y: True, (0, 2), (0, 3), 100, 3) == 6.0
            assert luas_mc(lambda x, y: False, (0, 2), (0, 3), 100, 3) == 0.0
            """,
            "Tarik x dan y seragam pada persegi panjang dan hitung proporsi yang memenuhi syarat.",
            """
            import random

            def luas_mc(syarat, xr, yr, n, seed):
                r = random.Random(seed)
                dalam = 0
                for _ in range(n):
                    x = xr[0] + (xr[1] - xr[0]) * r.random()
                    y = yr[0] + (yr[1] - yr[0]) * r.random()
                    if syarat(x, y):
                        dalam += 1
                return dalam / n * (xr[1] - xr[0]) * (yr[1] - yr[0])
            """,
        ),
    ],
    [
        M("Melaporkan taksiran tanpa galat baku.", "Sertakan SE atau interval."),
        M("Mengira galat turun sebagai 1/n.", "Turun sebagai satu per akar n."),
        M("Lupa mengalikan rata-rata dengan lebar rentang.", "Integral sama dengan lebar kali rata-rata."),
    ],
    [
        Q("Integrasi MC menaksir integral sebagai?", ["Lebar kali rata-rata f", "Jumlah f", "Maks f", "Median f"], 0, "Ekspektasi dari titik seragam.", hint="Rata-rata."),
        Q("Galat baku MC?", ["sigma/akar n", "sigma/n", "sigma", "n sigma"], 0, "Seperti rata-rata.", hint="Akar."),
        Q("Untuk 10 kali lebih presisi butuh titik?", ["10 kali", "100 kali", "Sama", "2 kali"], 1, "Akar n.", hint="Kuadrat."),
        Q("Keunggulan MC di dimensi tinggi?", ["Galat tak bergantung dimensi", "Selalu eksak", "Tanpa acak", "Lebih cepat grid"], 0, "Tidak ada ledakan titik.", hint="Dimensi."),
        Q("Hit-or-miss menaksir?", ["Luas dari proporsi titik", "Median", "Varians", "Korelasi"], 0, "Proporsi kali luas pembungkus.", hint="Tembak titik."),
    ],
    [
        "Integral adalah lebar kali rata-rata fungsi di titik acak.",
        "Setiap taksiran MC perlu galat baku.",
        "Satu digit presisi tambahan butuh seratus kali lebih banyak simulasi.",
        "Hit-or-miss menaksir luas dari proporsi titik.",
    ],
    [],
)

l3 = lesson(
    "A4-08-3",
    "Bootstrap, permutasi, dan simulasi keputusan",
    35,
    [
        "Menyusun interval kepercayaan dengan bootstrap",
        "Menghitung nilai p dengan uji permutasi",
        "Menyimulasikan keputusan persediaan di bawah ketidakpastian",
        "Memilih keputusan optimal dari nilai harapan",
    ],
    [
        T("""
        ## Bootstrap

        Interval kepercayaan klasik bergantung pada rumus galat baku, yang tidak selalu ada untuk statistik rumit seperti median atau korelasi. **Bootstrap** menggantinya dengan simulasi: anggap sampelmu adalah populasi, ambil sampel ulang berukuran sama **dengan pengembalian** dari sampel itu, hitung statistik, dan ulangi ribuan kali. Sebaran statistik hasil ulang menaksir sebaran statistik sebenarnya.

        Gagasannya sederhana dan sangat umum. Selama sampel awal mewakili populasi, bootstrap memberi taksiran ketidakpastian untuk hampir semua statistik tanpa rumus matematika.
        """),
        C(
            """
            import random

            data = [12, 15, 14, 10, 18, 20, 11, 13, 16, 17]
            r = random.Random(3)
            rata = sorted(sum(r.choices(data, k=len(data))) / len(data) for _ in range(2000))
            lo, hi = rata[50], rata[1949]
            print(lo < 14.6 < hi, 2 < hi - lo < 6)
            """,
            """
            True True
            """,
            """
            Interval bootstrap memuat rata-rata sampel dan lebarnya sekitar empat, sesuai galat baku satu.
            """,
            filename="bootstrap.py",
        ),
        T("""
        ## Interval persentil

        Cara paling sederhana membentuk interval dari hasil bootstrap adalah memakai persentil. Urutkan statistik hasil ulang dan ambil nilai pada persentil ke-2,5 dan ke-97,5 untuk interval 95 persen. Tidak diperlukan asumsi normal, sehingga interval dapat asimetris bila sebaran statistiknya miring.

        Bootstrap membutuhkan sampel asli yang cukup besar dan mewakili. Untuk sampel sangat kecil atau statistik yang sensitif terhadap nilai ekstrem seperti maksimum, bootstrap bisa menyesatkan. Seperti metode lain, ia bukan sihir tetapi alat yang berguna bila dipakai dengan kritis.
        """),
        T("""
        ## Uji permutasi

        Misalkan dua kelompok memiliki rata-rata berbeda dan kita ingin tahu apakah perbedaan itu mungkin kebetulan. Bila tidak ada perbedaan nyata, label kelompok hanya penanda acak. **Uji permutasi** mengacak label berulang kali, menghitung selisih rata-rata tiap pengacakan, dan melihat seberapa sering selisih sebesar atau lebih besar dari yang teramati terjadi.

        Proporsi itu adalah nilai p. Nilai p kecil berarti selisih teramati jarang muncul bila label tidak bermakna, sehingga ada alasan menduga perbedaan nyata. Uji ini tidak berasumsi distribusi tertentu, dan untuk sampel kecil kita bisa menghitung semua permutasi secara eksak.
        """),
        C(
            """
            from itertools import combinations

            A = [5, 6, 7, 8, 9]
            B = [1, 2, 3, 4, 5]
            semua = A + B
            amati = sum(A) / 5 - sum(B) / 5
            lebih = total = 0
            for idx in combinations(range(10), 5):
                a = [semua[i] for i in idx]
                b = [semua[i] for i in range(10) if i not in idx]
                total += 1
                if sum(a) / 5 - sum(b) / 5 >= amati - 1e-12:
                    lebih += 1
            print(amati, lebih, total, round(lebih / total, 4))
            """,
            """
            4.0 2 252 0.0079
            """,
            """
            Hanya dua dari dua ratus lima puluh dua pembagian yang menghasilkan selisih sebesar itu, sehingga nilai p sekitar nol koma nol nol delapan.
            """,
            filename="uji_permutasi.py",
        ),
        T("""
        ## Simulasi keputusan

        Monte Carlo sangat berguna untuk keputusan di bawah ketidakpastian. Contoh persediaan: toko memesan `q` unit seharga 2 per unit dan menjual seharga 5 per unit. Permintaan harian tidak pasti, katakan seragam dari 1 sampai 10. Unit yang tidak laku hangus. Keuntungan hari itu `5 * min(q, permintaan) - 2 * q`.

        Memesan terlalu sedikit melewatkan penjualan dan terlalu banyak membuang uang. Keuntungan harapan sebagai fungsi `q` memberi jawaban jelas, dan dapat dihitung secara eksak maupun disimulasikan untuk aturan permintaan yang lebih rumit.
        """),
        C(
            """
            print([round(sum(5 * min(q, d) - 2 * q for d in range(1, 11)) / 10, 4) for q in range(5, 9)])
            """,
            """
            [10.0, 10.5, 10.5, 10.0]
            """,
            """
            Keuntungan harapan tertinggi dicapai dengan memesan enam atau tujuh unit, dan menurun bila memesan lebih sedikit atau lebih banyak.
            """,
            filename="persediaan.py",
        ),
        T("""
        ## Dari keuntungan ke keputusan

        Dengan nilai harapan untuk tiap pilihan, keputusan optimal adalah yang memaksimalkannya. Pada contoh tadi, enam dan tujuh unit sama baik, dan kita bisa memilih yang lebih kecil untuk mengurangi modal tertahan. Intuisinya: tambahkan unit selama peluang unit itu terjual dikali margin lebih besar daripada biaya.

        Simulasi mengizinkan kita menambahkan realisme: permintaan berubah menurut hari, pemasok terlambat, barang kedaluwarsa. Setiap aturan baru hanya satu baris kode, sedangkan analisis eksak mungkin tak ada. Namun selalu laporkan ketidakpastian taksiran dan uji sensitivitas terhadap asumsi permintaan.
        """),
        C(
            """
            import random

            r = random.Random(8)
            n = 20000
            q = 6
            untung = sum(5 * min(q, r.randint(1, 10)) - 2 * q for _ in range(n)) / n
            print(abs(untung - 10.5) < 0.3)
            """,
            """
            True
            """,
            """
            Simulasi keuntungan harian dengan memesan enam unit mendekati nilai harapan sepuluh koma lima.
            """,
            filename="sim_persediaan.py",
        ),
        K(
            "warn",
            """
            Hasil simulasi keputusan hanya sebaik asumsi masukannya. Uji sensitivitas terhadap distribusi permintaan sebelum mempercayai rekomendasi.
            """,
            title="Sampah masuk",
        ),
        T("""
        ## Bootstrap untuk statistik apa pun

        Keindahan bootstrap adalah generalitasnya. Untuk median, cukup ganti rata-rata dengan median pada setiap sampel ulang. Untuk korelasi, ambil sampel ulang pasangan data utuh lalu hitung korelasinya. Untuk rasio dua rata-rata atau akurasi model, polanya sama. Tidak perlu menurunkan rumus galat baku untuk tiap statistik baru.

        Kehati-hatian tetap perlu: ambil sampel ulang unit yang independen. Bila data berasal dari kelompok seperti beberapa pengamatan per pengguna, ambil sampel ulang pengguna, bukan pengamatan, supaya struktur ketergantungan dipertahankan.
        """),
        T("""
        ## Nilai p dan ukuran efek

        Nilai p menjawab seberapa mengejutkan data bila tidak ada efek, bukan seberapa besar efeknya. Dengan sampel sangat besar, perbedaan yang remeh secara praktis pun bisa memiliki nilai p sangat kecil. Sebaliknya, efek besar pada sampel kecil bisa gagal menembus ambang. Karena itu laporkan selisih beserta interval kepercayaannya, bukan hanya nilai p.

        Uji permutasi dan bootstrap sama-sama menghasilkan keduanya: nilai p dari pengacakan label dan interval dari sampel ulang. Gunakan keduanya bersama untuk gambaran yang utuh.
        """),
        T("""
        ## Perencanaan dengan skenario

        Simulasi keputusan paling bernilai bila dipakai untuk membandingkan skenario. Ubah distribusi permintaan menjadi lebih tinggi, tambahkan keterlambatan pemasok, atau naikkan biaya, lalu lihat apakah keputusan optimal berubah. Bila keputusan stabil di berbagai skenario masuk akal, kamu bisa yakin. Bila berubah drastis, ketidakpastian asumsi merupakan risiko utama dan layak diselidiki lebih dulu daripada dioptimalkan lebih lanjut.
        """),
        T("""
        ## Menutup modul probabilitas

        Dengan modul ini kamu telah membangun jalur lengkap dari aturan dasar peluang, peluang bersyarat dan Bayes, variabel acak diskrit dan kontinu, distribusi umum, ekspektasi dan varians, hingga limit pusat dan simulasi. Semua ini fondasi statistika inferensial, pembelajaran mesin probabilistik, dan sains data berbasis eksperimen. Kursus berikutnya membangun di atasnya dengan statistika deskriptif dan inferensial.
        """),
        E(
            "A4-08-3-ex1",
            "mudah",
            """
            Tulis fungsi `bootstrap_rata(data, b, seed)` yang memakai `random.Random(seed)` untuk menghasilkan list `b` rata-rata sampel ulang (`choices` dengan pengembalian, ukuran sama dengan data).
            """,
            """
            import random

            def bootstrap_rata(data, b, seed):
                # TODO: implementasikan
                pass
            """,
            """
            d = [12, 15, 14, 10, 18, 20, 11, 13, 16, 17]
            h = bootstrap_rata(d, 2000, 1)
            assert len(h) == 2000
            assert all(min(d) <= x <= max(d) for x in h)
            assert abs(sum(h) / len(h) - 14.6) < 0.3
            """,
            "Ulangi b kali pengambilan sampel dengan pengembalian dan hitung rata-ratanya.",
            """
            import random

            def bootstrap_rata(data, b, seed):
                r = random.Random(seed)
                n = len(data)
                return [sum(r.choices(data, k=n)) / n for _ in range(b)]
            """,
        ),
        E(
            "A4-08-3-ex2",
            "sedang",
            """
            Tulis fungsi `interval_persentil(nilai, level=0.95)` yang mengurutkan `nilai` dan mengembalikan tuple `(bawah, atas)`. Dengan `alpha = 1 - level` dan `n = len(nilai)`, bawah adalah elemen urut ke `int(round(alpha / 2 * n, 6))` dan atas adalah elemen urut ke `min(n - 1, int(round((1 - alpha / 2) * n, 6)))`.
            """,
            """
            def interval_persentil(nilai, level=0.95):
                # TODO: implementasikan
                pass
            """,
            """
            s = list(range(1, 101))
            assert interval_persentil(s, 0.9) == (6, 96)
            assert interval_persentil(s) == (3, 98)
            assert interval_persentil([5]) == (5, 5)
            assert interval_persentil(list(range(1, 11)), 0.8) == (2, 10)
            """,
            "Urutkan nilai lalu ambil indeks dari alpha dengan pembulatan agar tidak terkena galat desimal.",
            """
            def interval_persentil(nilai, level=0.95):
                s = sorted(nilai)
                n = len(s)
                alpha = 1 - level
                lo = int(round(alpha / 2 * n, 6))
                hi = min(n - 1, int(round((1 - alpha / 2) * n, 6)))
                return (s[lo], s[hi])
            """,
        ),
        E(
            "A4-08-3-ex3",
            "sedang",
            """
            Tulis fungsi `nilai_harapan_persediaan(q, harga, biaya, maks)` yang mengembalikan keuntungan harapan memesan `q` unit bila permintaan seragam dari 1 sampai `maks`, dengan keuntungan `harga * min(q, d) - biaya * q`. Bulatkan 4 desimal.
            """,
            """
            def nilai_harapan_persediaan(q, harga, biaya, maks):
                # TODO: implementasikan
                pass
            """,
            """
            assert nilai_harapan_persediaan(6, 5, 2, 10) == 10.5
            assert nilai_harapan_persediaan(5, 5, 2, 10) == 10.0
            assert nilai_harapan_persediaan(8, 5, 2, 10) == 10.0
            assert nilai_harapan_persediaan(0, 5, 2, 10) == 0.0
            assert nilai_harapan_persediaan(10, 5, 2, 10) == 7.5
            """,
            "Rata-ratakan keuntungan atas semua nilai permintaan yang sama mungkin.",
            """
            def nilai_harapan_persediaan(q, harga, biaya, maks):
                total = sum(harga * min(q, d) - biaya * q for d in range(1, maks + 1))
                return round(total / maks, 4) + 0.0
            """,
        ),
        E(
            "A4-08-3-ex4",
            "menantang",
            """
            Tulis fungsi `q_optimal(harga, biaya, maks)` yang mengembalikan jumlah pesanan `q` dari `0` sampai `maks` dengan keuntungan harapan terbesar (permintaan seragam 1 sampai `maks`, keuntungan `harga * min(q, d) - biaya * q`). Bila seri, pilih `q` terkecil. Bandingkan keuntungan setelah dibulatkan ke 9 desimal.
            """,
            """
            def q_optimal(harga, biaya, maks):
                # TODO: implementasikan
                pass
            """,
            """
            assert q_optimal(5, 2, 10) == 6
            assert q_optimal(5, 1, 10) == 8
            assert q_optimal(5, 6, 10) == 0
            assert q_optimal(3, 2, 4) == 2
            """,
            "Hitung keuntungan harapan tiap q dan ambil maksimum dengan aturan seri ke q terkecil.",
            """
            def q_optimal(harga, biaya, maks):
                def ep(q):
                    return sum(harga * min(q, d) - biaya * q for d in range(1, maks + 1)) / maks
                return max(range(maks + 1), key=lambda q: (round(ep(q), 9), -q))
            """,
        ),
    ],
    [
        M("Bootstrap tanpa pengembalian.", "Ambil sampel ulang dengan pengembalian."),
        M("Menyimpulkan dari nilai p kecil bahwa efek besar.", "Nilai p tidak mengukur ukuran efek."),
        M("Mempercayai simulasi dengan asumsi masukan buruk.", "Uji sensitivitas asumsi."),
    ],
    [
        Q("Bootstrap mengambil sampel ulang?", ["Tanpa pengembalian", "Dengan pengembalian", "Dari populasi baru", "Dari median"], 1, "Ukuran sama dengan data.", hint="Kembali."),
        Q("Uji permutasi mengacak?", ["Data", "Label kelompok", "Rata-rata", "Varians"], 1, "Di bawah hipotesis nol label tak bermakna.", hint="Label."),
        Q("Nilai p adalah?", ["Peluang hipotesis benar", "Proporsi hasil seekstrem teramati di bawah nol", "Ukuran efek", "Galat baku"], 1, "Di bawah asumsi tidak ada perbedaan.", hint="Seekstrem."),
        Q("Keputusan optimal dari?", ["Nilai harapan terbesar", "Nilai terkecil", "Median", "Rata-rata acak"], 0, "Maksimalkan keuntungan harapan.", hint="Harapan."),
        Q("Interval persentil bootstrap memakai?", ["Persentil 2,5 dan 97,5", "Min dan maks", "Rata-rata", "Median"], 0, "Untuk 95 persen.", hint="Dua ekor."),
    ],
    [
        "Bootstrap menaksir ketidakpastian dengan sampel ulang dengan pengembalian.",
        "Uji permutasi menghitung nilai p dengan mengacak label.",
        "Simulasi mengevaluasi keputusan dengan nilai harapan.",
        "Hasil simulasi bergantung pada asumsi masukan.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perhitungan yang cukup jelas dalam teks.", "brief": []}

write_module(
    "A4",
    8,
    "Simulasi Monte Carlo",
    105,
    [
        "Menaksir peluang dan integral dengan simulasi",
        "Menaksir galat baku taksiran Monte Carlo",
        "Memakai bootstrap, uji permutasi, dan simulasi keputusan",
    ],
    [l1, l2, l3],
    video,
    REF,
)
