import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

l1 = lesson(
    "A5-05-1",
    "Kovariansi dan korelasi Pearson",
    35,
    [
        "Menghitung kovariansi populasi dan sampel",
        "Menghitung koefisien korelasi Pearson dan menafsirkannya",
        "Menjelaskan bahwa korelasi hanya mengukur hubungan linear",
        "Menghitung kovariansi secara inkremental",
    ],
    [
        T("""
        ## Dari satu variabel ke dua variabel

        Sejauh ini kita menggambarkan satu variabel pada satu waktu. Pertanyaan data sains yang paling menarik justru menyangkut hubungan: apakah jam belajar berkaitan dengan nilai, apakah iklan berkaitan dengan penjualan, apakah suhu berkaitan dengan konsumsi listrik. **Kovariansi** dan **korelasi** adalah ukuran pertama untuk menjawab apakah dua variabel bergerak bersama.

        Pelajaran ini membahas ukuran linear paling umum, korelasi Pearson. Pelajaran berikutnya membahas korelasi peringkat yang lebih fleksibel, lalu peringatan penting bahwa korelasi bukan kausalitas.
        """),
        T("""
        ## Kovariansi

        **Kovariansi** adalah rata-rata hasil kali simpangan dua variabel dari rata-ratanya: `jumlah (x - rata_x) * (y - rata_y) / n`. Bila nilai `x` yang di atas rata-rata cenderung berpasangan dengan nilai `y` yang di atas rata-rata, hasil kali positif mendominasi dan kovariansi positif. Bila berlawanan, kovariansi negatif.

        Kovariansi sebuah variabel dengan dirinya sendiri adalah varians. Seperti varians, untuk sampel kita membagi dengan `n - 1`. Kelemahan kovariansi adalah ukurannya bergantung satuan, sehingga sulit dibandingkan.
        """),
        C(
            """
            x = [1, 2, 3, 4, 5]
            y = [2, 4, 5, 4, 5]
            n = len(x)
            mx, my = sum(x) / n, sum(y) / n
            c = sum((a - mx) * (b - my) for a, b in zip(x, y))
            print(c / n, c / (n - 1))
            """,
            """
            1.2 1.5
            """,
            """
            Kovariansi populasi satu koma dua dan sampel satu koma lima bernilai positif, menandakan keduanya cenderung naik bersama.
            """,
            filename="kovariansi.py",
        ),
        T("""
        ## Korelasi Pearson

        **Korelasi Pearson** `r` adalah kovariansi dibagi hasil kali simpangan baku kedua variabel. Pembagian ini menghilangkan satuan sehingga `r` selalu berada antara minus satu dan satu. Nilai satu berarti hubungan linear positif sempurna, minus satu linear negatif sempurna, dan nol berarti tidak ada hubungan linear.

        Dengan data di atas, `r` sekitar 0,77, hubungan positif yang cukup kuat. Pedoman kasar menganggap nilai mutlak di bawah 0,3 lemah, 0,3 sampai 0,7 sedang, dan di atas 0,7 kuat, tetapi ambang yang bermakna bergantung bidang.
        """),
        C(
            """
            import math

            def corr(a, b):
                n = len(a)
                ma, mb = sum(a) / n, sum(b) / n
                c = sum((p - ma) * (q - mb) for p, q in zip(a, b))
                sa = math.sqrt(sum((p - ma) ** 2 for p in a))
                sb = math.sqrt(sum((q - mb) ** 2 for q in b))
                return c / (sa * sb)

            x = [1, 2, 3, 4, 5]
            print(round(corr(x, [2, 4, 5, 4, 5]), 4))
            print(round(corr(x, [2 * v + 1 for v in x]), 4))
            print(round(corr(x, [-v for v in x]), 4))
            """,
            """
            0.7746
            1.0
            -1.0
            """,
            """
            Hubungan linear sempurna menghasilkan satu atau minus satu, sedangkan data berderau menghasilkan nilai di antaranya.
            """,
            filename="korelasi.py",
        ),
        T("""
        ## Invarians terhadap skala dan geser

        Korelasi tidak berubah bila salah satu variabel digeser atau dikalikan konstanta positif, karena operasi itu hanya mengubah satuan. Korelasi tinggi badan dengan berat badan sama persis dalam meter atau sentimeter. Mengalikan dengan konstanta negatif membalik tanda korelasi.

        Sifat ini membuat korelasi cocok membandingkan hubungan antar pasangan variabel berbeda satuan. Kovariansi tidak memiliki sifat ini, sehingga korelasi adalah versi terstandardisasi dari kovariansi.
        """),
        T("""
        ## Hanya hubungan linear

        Kelemahan terbesar korelasi Pearson adalah ia hanya menangkap hubungan **linear**. Data `y = x kuadrat` dengan `x` simetris di sekitar nol memiliki hubungan sempurna, tetapi korelasinya nol, karena sisi kiri dan kanan saling meniadakan. Korelasi nol tidak berarti independen.

        Karena itu selalu gambar diagram pencar sebelum memercayai angka korelasi. Kumpulan data Anscombe memperlihatkan empat dataset berkorelasi sama persis, namun bentuknya sangat berbeda: garis, lengkung, garis dengan pencilan, dan titik vertikal dengan satu pencilan.
        """),
        C(
            """
            import math

            def corr(a, b):
                n = len(a)
                ma, mb = sum(a) / n, sum(b) / n
                c = sum((p - ma) * (q - mb) for p, q in zip(a, b))
                sa = math.sqrt(sum((p - ma) ** 2 for p in a))
                sb = math.sqrt(sum((q - mb) ** 2 for q in b))
                return c / (sa * sb)

            xs = [-2, -1, 0, 1, 2]
            print(round(corr(xs, [v * v for v in xs]), 4) + 0.0)
            print(round(corr([1, 2, 3, 4, 5], [1, 2, 3, 4, 50]), 4))
            """,
            """
            0.0
            0.7433
            """,
            """
            Hubungan kuadrat sempurna menghasilkan korelasi nol, dan satu pencilan menurunkan korelasi dari hubungan hampir sempurna menjadi nol koma tujuh empat.
            """,
            filename="hanya_linear.py",
        ),
        T("""
        ## Koefisien determinasi dan uji

        Kuadrat korelasi, `r^2`, disebut **koefisien determinasi**. Ia menyatakan proporsi variasi satu variabel yang dapat dijelaskan secara linear oleh variabel lain. Korelasi 0,77 berarti `r^2` sekitar 0,6, atau enam puluh persen variasi terjelaskan.

        Untuk menguji apakah korelasi berbeda dari nol, statistik `t = r * akar((n - 2) / (1 - r^2))` dibandingkan dengan distribusi t berderajat bebas `n - 2`. Pada sampel kecil, korelasi besar bisa muncul murni karena kebetulan, jadi jangan menafsirkan `r` tanpa mempertimbangkan ukuran sampel.
        """),
        C(
            """
            import math

            r = 0.7745966692
            n = 5
            print(round(r * r, 4), round(r * math.sqrt((n - 2) / (1 - r * r)), 4))
            """,
            """
            0.6 2.1213
            """,
            """
            Enam puluh persen variasi terjelaskan, dan statistik t sekitar dua koma satu dua pada tiga derajat bebas.
            """,
            filename="determinasi.py",
        ),
        T("""
        ## Kovariansi dalam satu lintasan

        Seperti varians, kovariansi dapat dihitung secara inkremental untuk aliran data. Untuk tiap pasangan baru `(x, y)`: tambah `n`, hitung `dx = x - rata_x`, perbarui `rata_x` dan `rata_y`, lalu tambahkan `dx * (y - rata_y_baru)` ke akumulator `c`. Kovariansi populasi adalah `c / n`.

        Teknik ini stabil dan hemat memori, dipakai pada pemantauan, penaksiran matriks kovariansi dalam filter Kalman, dan pelatihan daring yang menyesuaikan statistik data secara terus-menerus.
        """),
        K(
            "warn",
            """
            Korelasi nol tidak berarti tidak ada hubungan. Hubungan nonlinear bisa kuat dengan korelasi Pearson nol. Selalu lihat diagram pencar.
            """,
            title="Nol bukan independen",
        ),
        T("""
        ## Memilih ukuran dalam praktik

        Sebelum menghitung korelasi, periksa tiga hal: apakah kedua variabel numerik, apakah hubungannya tampak mendekati garis pada diagram pencar, dan apakah ada pencilan yang dominan. Bila ketiganya terpenuhi, korelasi Pearson ringkas dan informatif. Bila tidak, gunakan ukuran lain dari pelajaran berikutnya.

        Laporkan juga ukuran sampel. Korelasi 0,5 dari seribu data jauh lebih meyakinkan daripada korelasi 0,5 dari delapan data, yang bisa muncul hanya karena kebetulan.
        """),
        E(
            "A5-05-1-ex1",
            "mudah",
            """
            Tulis fungsi `kovariansi(a, b, sampel=False)` yang mengembalikan kovariansi dibulatkan 4 desimal. Bila `sampel` benar bagi dengan `n - 1`, bila tidak bagi dengan `n`.
            """,
            """
            def kovariansi(a, b, sampel=False):
                # TODO: implementasikan
                pass
            """,
            """
            x = [1, 2, 3, 4, 5]
            assert kovariansi(x, [2, 4, 5, 4, 5]) == 1.2
            assert kovariansi(x, [2, 4, 5, 4, 5], sampel=True) == 1.5
            assert kovariansi(x, [2 * v for v in x]) == 4.0
            assert kovariansi([-2, -1, 0, 1, 2], [4, 1, 0, 1, 4]) == 0.0
            """,
            "Jumlahkan hasil kali simpangan lalu bagi dengan pembagi yang sesuai.",
            """
            def kovariansi(a, b, sampel=False):
                n = len(a)
                ma, mb = sum(a) / n, sum(b) / n
                c = sum((p - ma) * (q - mb) for p, q in zip(a, b))
                return round(c / (n - 1 if sampel else n), 4) + 0.0
            """,
        ),
        E(
            "A5-05-1-ex2",
            "sedang",
            """
            Tulis fungsi `korelasi(a, b)` yang mengembalikan korelasi Pearson dibulatkan 4 desimal. Bila salah satu variabel konstan kembalikan `None`.
            """,
            """
            import math

            def korelasi(a, b):
                # TODO: implementasikan
                pass
            """,
            """
            x = [1, 2, 3, 4, 5]
            assert korelasi(x, [2, 4, 5, 4, 5]) == 0.7746
            assert korelasi(x, [-v for v in x]) == -1.0
            assert korelasi(x, [2 * v + 1 for v in x]) == 1.0
            assert korelasi([-2, -1, 0, 1, 2], [4, 1, 0, 1, 4]) == 0.0
            assert korelasi(x, [3, 3, 3, 3, 3]) is None
            """,
            "Bagi jumlah hasil kali simpangan dengan akar hasil kali jumlah kuadrat simpangan.",
            """
            import math

            def korelasi(a, b):
                n = len(a)
                ma, mb = sum(a) / n, sum(b) / n
                sa = math.sqrt(sum((p - ma) ** 2 for p in a))
                sb = math.sqrt(sum((q - mb) ** 2 for q in b))
                if sa == 0 or sb == 0:
                    return None
                c = sum((p - ma) * (q - mb) for p, q in zip(a, b))
                return round(c / (sa * sb), 4) + 0.0
            """,
        ),
        E(
            "A5-05-1-ex3",
            "sedang",
            """
            Tulis fungsi `determinasi_t(a, b)` yang mengembalikan tuple `(r2, t)` dengan `r2` kuadrat korelasi dan `t = r * sqrt((n - 2) / (1 - r2))`, masing-masing dibulatkan 4 desimal.
            """,
            """
            import math

            def determinasi_t(a, b):
                # TODO: implementasikan
                pass
            """,
            """
            assert determinasi_t([1, 2, 3, 4, 5], [2, 4, 5, 4, 5]) == (0.6, 2.1213)
            assert determinasi_t([1, 2, 3, 4, 5, 6], [2, 1, 4, 3, 6, 5])[0] == 0.6865
            assert determinasi_t([1, 2, 3, 4], [1, 3, 2, 4])[0] == 0.64
            """,
            "Hitung r dari simpangan lalu terapkan rumus statistik t.",
            """
            import math

            def determinasi_t(a, b):
                n = len(a)
                ma, mb = sum(a) / n, sum(b) / n
                c = sum((p - ma) * (q - mb) for p, q in zip(a, b))
                sa = math.sqrt(sum((p - ma) ** 2 for p in a))
                sb = math.sqrt(sum((q - mb) ** 2 for q in b))
                r = c / (sa * sb)
                r2 = r * r
                t = r * math.sqrt((n - 2) / (1 - r2))
                return (round(r2, 4), round(t, 4))
            """,
        ),
        E(
            "A5-05-1-ex4",
            "menantang",
            """
            Tulis fungsi `kovariansi_inkremental(pasangan)` yang menghitung kovariansi populasi dalam satu lintasan dari list tuple `(x, y)` dan mengembalikannya dibulatkan 4 desimal. List kosong mengembalikan `None`.
            """,
            """
            def kovariansi_inkremental(pasangan):
                # TODO: implementasikan
                pass
            """,
            """
            assert kovariansi_inkremental([(1, 2), (2, 4), (3, 5), (4, 4), (5, 5)]) == 1.2
            assert kovariansi_inkremental([(1, 1), (2, 2)]) == 0.25
            assert kovariansi_inkremental([(7, 3)]) == 0.0
            assert kovariansi_inkremental([]) is None
            """,
            "Perbarui rata-rata x dan y lalu tambahkan dx dikali selisih y baru ke akumulator.",
            """
            def kovariansi_inkremental(pasangan):
                mx = 0.0
                my = 0.0
                c = 0.0
                n = 0
                for x, y in pasangan:
                    n += 1
                    dx = x - mx
                    mx += dx / n
                    my += (y - my) / n
                    c += dx * (y - my)
                if n == 0:
                    return None
                return round(c / n, 4) + 0.0
            """,
        ),
    ],
    [
        M("Mengira korelasi nol berarti tidak ada hubungan.", "Hubungan nonlinear bisa kuat dengan korelasi nol."),
        M("Menafsirkan korelasi tanpa melihat diagram pencar.", "Gambar datanya terlebih dahulu."),
        M("Membandingkan kovariansi antar pasangan berbeda satuan.", "Pakai korelasi."),
    ],
    [
        Q("Korelasi Pearson berada di rentang?", ["-1 sampai 1", "0 sampai 1", "0 sampai 100", "Tak terbatas"], 0, "Kovariansi terstandardisasi.", hint="Batas."),
        Q("Korelasi mengukur hubungan?", ["Linear", "Apa saja", "Kausal", "Acak"], 0, "Hanya linear.", hint="Garis."),
        Q("r kuadrat disebut?", ["Koefisien determinasi", "Kovariansi", "Varians", "Galat"], 0, "Proporsi variasi terjelaskan.", hint="Determinasi."),
        Q("Menggeser satu variabel mengubah korelasi?", ["Tidak", "Ya bertambah", "Ya berkurang", "Menjadi nol"], 0, "Invarian.", hint="Geser."),
        Q("Kovariansi variabel dengan dirinya adalah?", ["Varians", "Korelasi", "Nol", "Satu"], 0, "Definisi.", hint="Diri."),
    ],
    [
        "Kovariansi mengukur gerak bersama dan bergantung satuan.",
        "Korelasi Pearson adalah kovariansi terstandardisasi antara minus satu dan satu.",
        "Korelasi hanya menangkap hubungan linear dan peka pada pencilan.",
        "r kuadrat adalah proporsi variasi yang terjelaskan secara linear.",
    ],
    [],
)

l2 = lesson(
    "A5-05-2",
    "Korelasi peringkat Spearman dan Kendall",
    35,
    [
        "Mengubah data menjadi peringkat dengan penanganan seri",
        "Menghitung korelasi Spearman",
        "Menghitung tau Kendall dari pasangan konkordan dan diskordan",
        "Memilih korelasi yang tepat untuk hubungan monoton dan data berpencilan",
    ],
    [
        T("""
        ## Ketika Pearson tidak cukup

        Korelasi Pearson mengasumsikan hubungan linear dan peka pada pencilan. Banyak hubungan nyata bersifat **monoton** tetapi tidak linear: makin besar `x`, makin besar `y`, namun tidak dengan laju tetap, misalnya hubungan dosis dengan respons. Data ordinal seperti peringkat kepuasan juga tidak cocok untuk Pearson.

        Korelasi peringkat menjawabnya dengan mengganti nilai dengan peringkatnya. Karena hanya urutan yang dipakai, ukuran ini kokoh terhadap pencilan dan menangkap hubungan monoton apa pun.
        """),
        T("""
        ## Peringkat dan seri

        Peringkat memberi angka satu pada nilai terkecil, dua pada berikutnya, dan seterusnya. Bila ada nilai sama, kita memakai **peringkat rata-rata**: dua nilai seri di posisi dua dan tiga masing-masing mendapat 2,5. Pendekatan ini menjaga jumlah peringkat tetap sama dan tidak menguntungkan salah satu nilai.

        Peringkat mengubah skala apa pun menjadi skala ordinal seragam. Setelah itu, semua yang kita pelajari untuk data berskala interval dapat dipakai pada peringkat tanpa terganggu pencilan.
        """),
        C(
            """
            def peringkat(data):
                s = sorted(data)
                hasil = []
                for v in data:
                    posisi = [i + 1 for i, w in enumerate(s) if w == v]
                    hasil.append(sum(posisi) / len(posisi))
                return hasil

            print(peringkat([10, 20, 20, 30]))
            print(peringkat([3, 1, 2]))
            """,
            """
            [1.0, 2.5, 2.5, 4.0]
            [3.0, 1.0, 2.0]
            """,
            """
            Dua nilai seri dua puluh berbagi peringkat dua koma lima, dan data tanpa seri mendapat peringkat bulat.
            """,
            filename="peringkat.py",
        ),
        T("""
        ## Korelasi Spearman

        **Korelasi Spearman** adalah korelasi Pearson yang dihitung pada peringkat, bukan nilai asli. Ia bernilai satu bila hubungan monoton naik sempurna, minus satu bila monoton turun sempurna, apa pun bentuk kurvanya. Hubungan `y = x pangkat tiga` tidak linear sehingga Pearson di bawah satu, tetapi Spearman tepat satu.

        Spearman sangat berguna ketika data berpencilan atau ordinal. Dalam contoh satu nilai y melonjak menjadi lima puluh, Pearson turun ke 0,74 sedangkan Spearman tetap satu karena urutan tidak berubah.
        """),
        C(
            """
            import math

            def peringkat(data):
                s = sorted(data)
                hasil = []
                for v in data:
                    posisi = [i + 1 for i, w in enumerate(s) if w == v]
                    hasil.append(sum(posisi) / len(posisi))
                return hasil

            def corr(a, b):
                n = len(a)
                ma, mb = sum(a) / n, sum(b) / n
                c = sum((p - ma) * (q - mb) for p, q in zip(a, b))
                sa = math.sqrt(sum((p - ma) ** 2 for p in a))
                sb = math.sqrt(sum((q - mb) ** 2 for q in b))
                return c / (sa * sb)

            x = [1, 2, 3, 4, 5]
            print(round(corr(peringkat(x), peringkat([v ** 3 for v in x])), 4))
            print(round(corr(peringkat(x), peringkat([1, 2, 3, 4, 50])), 4))
            print(round(corr(peringkat(x), peringkat([2, 4, 5, 4, 5])), 4))
            """,
            """
            1.0
            1.0
            0.7379
            """,
            """
            Hubungan monoton menghasilkan Spearman satu walau tidak linear, dan seri membuat nilainya sedikit di bawah Pearson.
            """,
            filename="spearman.py",
        ),
        T("""
        ## Tau Kendall

        **Tau Kendall** bekerja dari pasangan pengamatan. Sepasang titik adalah **konkordan** bila urutan keduanya pada `x` sama dengan pada `y`, dan **diskordan** bila berlawanan. Pasangan dengan seri pada salah satu variabel tidak dihitung. Tau-a adalah `(konkordan - diskordan) / jumlah semua pasangan`.

        Interpretasinya intuitif: selisih peluang memilih sepasang titik yang searah dengan yang berlawanan. Tau cenderung lebih kecil dari Spearman pada data yang sama dan lebih stabil pada sampel kecil dengan banyak seri.
        """),
        C(
            """
            def tau(a, b):
                k = d = 0
                n = len(a)
                for i in range(n):
                    for j in range(i + 1, n):
                        s = (a[i] - a[j]) * (b[i] - b[j])
                        k += s > 0
                        d += s < 0
                return k, d, round((k - d) / (n * (n - 1) / 2), 4)

            x = [1, 2, 3, 4, 5]
            print(tau(x, [2, 4, 5, 4, 5]))
            print(tau([1, 2, 3, 4], [1, 3, 2, 4]))
            print(tau(x, [5, 4, 3, 2, 1]))
            """,
            """
            (7, 1, 0.6)
            (5, 1, 0.6667)
            (0, 10, -1.0)
            """,
            """
            Tujuh pasangan konkordan dan satu diskordan memberi tau enam persepuluh, sedangkan urutan terbalik penuh memberi minus satu.
            """,
            filename="kendall.py",
        ),
        T("""
        ## Memilih ukuran korelasi

        Gunakan Pearson bila hubungan tampak linear, data interval atau rasio, dan tanpa pencilan berat. Gunakan Spearman bila hubungan monoton tetapi nonlinear, data ordinal, atau ada pencilan. Gunakan Kendall pada sampel kecil dengan banyak seri atau saat interpretasi probabilistik lebih disukai.

        Praktik terbaik adalah menghitung Pearson dan Spearman bersama. Bila Spearman jauh lebih besar dari Pearson, curigai hubungan nonlinear atau pencilan, dan buka diagram pencarnya untuk memahami sebabnya.
        """),
        T("""
        ## Keterbatasan semua ukuran korelasi

        Baik Pearson, Spearman, maupun Kendall hanya mengukur hubungan monoton atau linear. Hubungan berbentuk U atau melingkar bisa memiliki ketiga ukuran dekat nol padahal hubungannya sangat kuat. Untuk hubungan semacam itu, ukuran berbasis informasi timbal balik atau jarak korelasi lebih tepat.

        Karena itu, tidak ada satu angka yang menggantikan pengamatan visual. Korelasi adalah ringkasan, dan seperti semua ringkasan ia membuang informasi. Tugas analis adalah tahu informasi apa yang terbuang.
        """),
        K(
            "tip",
            """
            Hitung Pearson dan Spearman bersama. Selisih besar di antara keduanya menandakan nonlinearitas atau pencilan.
            """,
            title="Dua ukuran lebih informatif",
        ),
        T("""
        ## Spearman dalam data nyata

        Skala kepuasan pelanggan satu sampai lima adalah ordinal: jarak antara tiga dan empat belum tentu sama dengan antara empat dan lima. Memakai Pearson mengasumsikan jarak sama, sedangkan Spearman hanya memakai urutan sehingga lebih jujur. Peringkat ujian dan skala Likert adalah contoh lain yang cocok untuk korelasi peringkat.

        Pada data keuangan atau sensor berpencilan, Spearman sering lebih stabil. Satu lonjakan acak yang merusak Pearson hampir tidak memengaruhi Spearman, karena lonjakan hanya mengubah satu peringkat.
        """),
        T("""
        ## Menghitung dengan seri banyak

        Bila data memiliki banyak nilai sama, misalnya skala lima titik dengan ratusan responden, seri sangat sering. Peringkat rata-rata tetap benar, tetapi korelasi maksimum yang dapat dicapai turun karena banyak pasangan tidak bisa diurutkan. Varian Kendall yang memperhitungkan seri, disebut tau-b, mengoreksinya.

        Tau-a yang kita pakai di sini tidak mengoreksi seri, sehingga nilainya lebih kecil bila seri banyak. Pustaka seperti SciPy memakai tau-b secara default, jadi hasil bisa sedikit berbeda dari hitungan tangan.
        """),
        T("""
        ## Ukuran efek dan ketidakpastian

        Seperti Pearson, korelasi peringkat dihitung dari sampel sehingga memiliki ketidakpastian. Selang kepercayaan lewat bootstrap, yaitu mengambil sampel ulang berpengembalian lalu menghitung ulang korelasi, memberi gambaran seberapa stabil nilainya. Selang lebar menandakan data terlalu sedikit untuk menyimpulkan kekuatan hubungan.

        Selalu laporkan korelasi bersama selangnya. Satu angka tunggal memberi kesan presisi palsu, padahal pada sampel kecil nilai sebenarnya bisa berada di rentang yang sangat lebar.
        """),
        E(
            "A5-05-2-ex1",
            "mudah",
            """
            Tulis fungsi `peringkat(data)` yang mengembalikan list peringkat rata-rata (mulai dari satu) untuk tiap elemen sesuai urutan asli.
            """,
            """
            def peringkat(data):
                # TODO: implementasikan
                pass
            """,
            """
            assert peringkat([10, 20, 20, 30]) == [1.0, 2.5, 2.5, 4.0]
            assert peringkat([3, 1, 2]) == [3.0, 1.0, 2.0]
            assert peringkat([5, 5, 5]) == [2.0, 2.0, 2.0]
            assert peringkat([]) == []
            """,
            "Urutkan data lalu rata-ratakan posisi setiap nilai yang sama.",
            """
            def peringkat(data):
                s = sorted(data)
                hasil = []
                for v in data:
                    posisi = [i + 1 for i, w in enumerate(s) if w == v]
                    hasil.append(sum(posisi) / len(posisi))
                return hasil
            """,
        ),
        E(
            "A5-05-2-ex2",
            "sedang",
            """
            Tulis fungsi `spearman(a, b)` yang mengembalikan korelasi Pearson dari peringkat rata-rata kedua list, dibulatkan 4 desimal. Bila peringkat salah satu konstan kembalikan `None`.
            """,
            """
            import math

            def spearman(a, b):
                # TODO: implementasikan
                pass
            """,
            """
            x = [1, 2, 3, 4, 5]
            assert spearman(x, [v ** 3 for v in x]) == 1.0
            assert spearman(x, [1, 2, 3, 4, 50]) == 1.0
            assert spearman(x, [5, 4, 3, 2, 1]) == -1.0
            assert spearman(x, [2, 4, 5, 4, 5]) == 0.7379
            assert spearman(x, [7, 7, 7, 7, 7]) is None
            """,
            "Ubah kedua list menjadi peringkat lalu hitung korelasi Pearson.",
            """
            import math

            def spearman(a, b):
                def rank(data):
                    s = sorted(data)
                    out = []
                    for v in data:
                        pos = [i + 1 for i, w in enumerate(s) if w == v]
                        out.append(sum(pos) / len(pos))
                    return out

                ra, rb = rank(a), rank(b)
                n = len(ra)
                ma, mb = sum(ra) / n, sum(rb) / n
                sa = math.sqrt(sum((p - ma) ** 2 for p in ra))
                sb = math.sqrt(sum((q - mb) ** 2 for q in rb))
                if sa == 0 or sb == 0:
                    return None
                c = sum((p - ma) * (q - mb) for p, q in zip(ra, rb))
                return round(c / (sa * sb), 4) + 0.0
            """,
        ),
        E(
            "A5-05-2-ex3",
            "sedang",
            """
            Tulis fungsi `pasangan_konkordan(a, b)` yang mengembalikan tuple `(konkordan, diskordan)`: banyak pasangan indeks `i < j` dengan hasil kali `(a[i]-a[j])*(b[i]-b[j])` positif atau negatif.
            """,
            """
            def pasangan_konkordan(a, b):
                # TODO: implementasikan
                pass
            """,
            """
            assert pasangan_konkordan([1, 2, 3, 4, 5], [2, 4, 5, 4, 5]) == (7, 1)
            assert pasangan_konkordan([1, 2, 3, 4], [1, 3, 2, 4]) == (5, 1)
            assert pasangan_konkordan([1, 2, 3, 4, 5], [5, 4, 3, 2, 1]) == (0, 10)
            assert pasangan_konkordan([1], [1]) == (0, 0)
            """,
            "Periksa semua pasangan indeks dan hitung tanda hasil kali selisih.",
            """
            def pasangan_konkordan(a, b):
                k = d = 0
                n = len(a)
                for i in range(n):
                    for j in range(i + 1, n):
                        s = (a[i] - a[j]) * (b[i] - b[j])
                        if s > 0:
                            k += 1
                        elif s < 0:
                            d += 1
                return (k, d)
            """,
        ),
        E(
            "A5-05-2-ex4",
            "menantang",
            """
            Tulis fungsi `kendall_tau(a, b)` yang mengembalikan `(konkordan - diskordan) / (n * (n - 1) / 2)` dibulatkan 4 desimal. Untuk kurang dari dua data kembalikan `None`.
            """,
            """
            def kendall_tau(a, b):
                # TODO: implementasikan
                pass
            """,
            """
            assert kendall_tau([1, 2, 3, 4, 5], [2, 4, 5, 4, 5]) == 0.6
            assert kendall_tau([1, 2, 3, 4], [1, 3, 2, 4]) == 0.6667
            assert kendall_tau([1, 2, 3, 4, 5], [5, 4, 3, 2, 1]) == -1.0
            assert kendall_tau([1, 2, 3, 4, 5, 6], [2, 1, 4, 3, 6, 5]) == 0.6
            assert kendall_tau([1], [1]) is None
            """,
            "Hitung selisih pasangan konkordan dan diskordan lalu bagi dengan semua pasangan.",
            """
            def kendall_tau(a, b):
                n = len(a)
                if n < 2:
                    return None
                k = d = 0
                for i in range(n):
                    for j in range(i + 1, n):
                        s = (a[i] - a[j]) * (b[i] - b[j])
                        if s > 0:
                            k += 1
                        elif s < 0:
                            d += 1
                return round((k - d) / (n * (n - 1) / 2), 4)
            """,
        ),
    ],
    [
        M("Memakai Pearson pada data ordinal.", "Pakai Spearman atau Kendall."),
        M("Mengabaikan seri saat membuat peringkat.", "Pakai peringkat rata-rata."),
        M("Mengira Spearman menangkap semua hubungan nonlinear.", "Ia hanya menangkap hubungan monoton."),
    ],
    [
        Q("Spearman adalah Pearson pada?", ["Peringkat", "Kuadrat", "Logaritma", "Selisih"], 0, "Dihitung dari peringkat.", hint="Urutan."),
        Q("Spearman menangkap hubungan?", ["Monoton", "Hanya linear", "Melingkar", "Acak"], 0, "Urutan saja.", hint="Naik terus."),
        Q("Tau Kendall memakai?", ["Pasangan konkordan dan diskordan", "Rata-rata", "Varians", "Median"], 0, "Pasangan.", hint="Pasangan."),
        Q("Peringkat nilai seri?", ["Rata-rata posisi", "Terkecil", "Terbesar", "Dibuang"], 0, "Adil.", hint="Rata-rata."),
        Q("Pencilan paling memengaruhi?", ["Pearson", "Spearman", "Kendall", "Ketiganya sama"], 0, "Memakai nilai asli.", hint="Nilai."),
    ],
    [
        "Spearman dan Kendall kokoh dan menangkap hubungan monoton.",
        "Seri ditangani dengan peringkat rata-rata.",
        "Hitung Pearson dan Spearman bersama untuk mendeteksi nonlinearitas.",
        "Tidak ada ukuran korelasi yang menangkap semua bentuk hubungan.",
    ],
    [],
)

l3 = lesson(
    "A5-05-3",
    "Matriks korelasi, paradoks Simpson, dan kausalitas",
    35,
    [
        "Menyusun matriks korelasi untuk banyak variabel",
        "Menjelaskan paradoks Simpson dan mendeteksinya",
        "Membandingkan korelasi Pearson dan Spearman pada data berpencilan",
        "Menjelaskan mengapa korelasi tidak membuktikan sebab akibat",
    ],
    [
        T("""
        ## Dari pasangan ke banyak variabel

        Dataset nyata memiliki banyak kolom. **Matriks korelasi** menyusun korelasi semua pasangan kolom dalam satu tabel simetris dengan diagonal satu. Ia adalah alat eksplorasi pertama untuk melihat variabel mana yang berkelompok, mana yang redundan, dan mana yang berkaitan dengan target prediksi.

        Pada data berdimensi tinggi, matriks korelasi besar sulit dibaca sehingga biasanya divisualisasikan sebagai peta panas dengan gradasi warna, dan dikelompokkan agar variabel berkorelasi tinggi berdekatan.
        """),
        C(
            """
            import math

            def corr(a, b):
                n = len(a)
                ma, mb = sum(a) / n, sum(b) / n
                c = sum((p - ma) * (q - mb) for p, q in zip(a, b))
                sa = math.sqrt(sum((p - ma) ** 2 for p in a))
                sb = math.sqrt(sum((q - mb) ** 2 for q in b))
                return c / (sa * sb)

            kolom = [[1, 2, 3, 4], [2, 4, 6, 8], [4, 3, 2, 1]]
            for i in kolom:
                print([round(corr(i, j), 4) for j in kolom])
            """,
            """
            [1.0, 1.0, -1.0]
            [1.0, 1.0, -1.0]
            [-1.0, -1.0, 1.0]
            """,
            """
            Matriks simetris dengan diagonal satu menunjukkan kolom pertama dan kedua berkorelasi sempurna positif, dan keduanya berlawanan dengan kolom ketiga.
            """,
            filename="matriks_korelasi.py",
        ),
        T("""
        ## Multikolinearitas

        Bila dua fitur berkorelasi sangat tinggi, keduanya membawa informasi hampir sama. Dalam regresi, ini disebut **multikolinearitas** dan membuat koefisien tidak stabil: model bisa memberi koefisien besar positif pada satu fitur dan besar negatif pada fitur lain yang saling meniadakan.

        Matriks korelasi membantu mendeteksinya. Pasangan dengan korelasi mutlak di atas 0,9 patut diperiksa, dan satu di antaranya sering bisa dibuang atau digabung tanpa kehilangan kemampuan prediksi.
        """),
        T("""
        ## Paradoks Simpson

        **Paradoks Simpson** terjadi ketika hubungan yang tampak pada data gabungan berlawanan dengan hubungan di dalam setiap kelompok. Bayangkan dua kelompok, masing-masing menunjukkan hubungan negatif sempurna antara `x` dan `y`, tetapi kelompok kedua memiliki nilai `x` dan `y` keseluruhan lebih tinggi. Bila digabung, titik-titik membentuk tren naik.

        Penyebabnya adalah variabel kelompok yang memengaruhi kedua variabel. Menggabungkan data tanpa memperhitungkannya menghasilkan kesimpulan terbalik, yang bila ditindaklanjuti dapat menyesatkan keputusan.
        """),
        C(
            """
            import math

            def corr(a, b):
                n = len(a)
                ma, mb = sum(a) / n, sum(b) / n
                c = sum((p - ma) * (q - mb) for p, q in zip(a, b))
                sa = math.sqrt(sum((p - ma) ** 2 for p in a))
                sb = math.sqrt(sum((q - mb) ** 2 for q in b))
                return c / (sa * sb)

            A = ([1, 2, 3], [5, 4, 3])
            B = ([6, 7, 8], [10, 9, 8])
            print(round(corr(*A), 4), round(corr(*B), 4))
            print(round(corr(A[0] + B[0], A[1] + B[1]), 4))
            """,
            """
            -1.0 -1.0
            0.8072
            """,
            """
            Di dalam tiap kelompok korelasi minus satu, tetapi data gabungan berkorelasi positif nol koma delapan.
            """,
            filename="simpson.py",
        ),
        T("""
        ## Menghadapi paradoks

        Cara melindungi diri adalah selalu memeriksa hubungan di dalam subkelompok yang bermakna: wilayah, usia, kategori produk, atau kelompok perlakuan. Bila arah hubungan berbeda antara gabungan dan subkelompok, gunakan analisis terstratifikasi atau regresi yang memasukkan variabel kelompok sebagai kontrol.

        Menentukan apakah data gabungan atau terpisah yang benar bukan pertanyaan statistik semata. Jawabannya bergantung pada struktur sebab akibat yang mendasari, yang memerlukan pengetahuan domain di luar data.
        """),
        T("""
        ## Korelasi bukan kausalitas

        Dua variabel berkorelasi dapat terjadi karena empat alasan: `x` menyebabkan `y`, `y` menyebabkan `x`, variabel ketiga memengaruhi keduanya, atau kebetulan. Penjualan es krim berkorelasi dengan jumlah orang tenggelam, bukan karena es krim menenggelamkan, tetapi karena cuaca panas mendorong keduanya.

        Variabel ketiga itu disebut **perancu** atau confounder. Hanya eksperimen terkontrol dengan penugasan acak, atau analisis kausal yang cermat dengan asumsi eksplisit, yang dapat menjawab pertanyaan sebab akibat. Korelasi adalah petunjuk, bukan bukti.
        """),
        C(
            """
            import math

            def corr(a, b):
                n = len(a)
                ma, mb = sum(a) / n, sum(b) / n
                c = sum((p - ma) * (q - mb) for p, q in zip(a, b))
                sa = math.sqrt(sum((p - ma) ** 2 for p in a))
                sb = math.sqrt(sum((q - mb) ** 2 for q in b))
                return c / (sa * sb)

            suhu = [20, 24, 28, 32, 36]
            es = [10, 14, 22, 30, 41]
            tenggelam = [1, 2, 3, 5, 6]
            print(round(corr(es, tenggelam), 4))
            """,
            """
            0.9871
            """,
            """
            Penjualan es krim dan kasus tenggelam berkorelasi hampir sempurna walau keduanya hanya digerakkan oleh suhu.
            """,
            filename="perancu.py",
        ),
        T("""
        ## Korelasi palsu dan pemancingan data

        Dengan banyak variabel, korelasi tinggi pasti muncul murni karena kebetulan. Dari seratus variabel acak ada empat ribu sembilan ratus lima puluh pasangan, dan sebagian akan tampak berkorelasi kuat. Menyaring pasangan dengan korelasi terbesar lalu menceritakan kisahnya disebut pemancingan data atau p-hacking.

        Cara melindungi diri adalah menetapkan hipotesis sebelum melihat data, memakai koreksi untuk perbandingan berganda, dan menguji temuan pada data baru yang tidak dipakai untuk mencarinya.
        """),
        K(
            "warn",
            """
            Korelasi tinggi bukan bukti sebab akibat. Periksa perancu, arah hubungan, dan kemungkinan kebetulan sebelum menarik kesimpulan kausal.
            """,
            title="Korelasi bukan kausalitas",
        ),
        T("""
        ## Membaca peta panas korelasi

        Peta panas korelasi menggunakan warna untuk menandai kekuatan dan tanda. Pola blok di sepanjang diagonal menunjukkan kelompok variabel yang berkaitan erat, misalnya fitur ukuran rumah yang bersama-sama naik. Baris target yang memiliki warna kuat menunjukkan fitur berguna untuk prediksi linear.

        Namun peta panas hanya memperlihatkan hubungan berpasangan. Dua fitur lemah secara individu bisa kuat bersama dalam interaksi, dan korelasi pasangan tidak mengungkap hubungan nonlinear. Anggap peta panas sebagai langkah awal, bukan kesimpulan.
        """),
        T("""
        ## Korelasi parsial

        Untuk memisahkan pengaruh perancu, kita bisa menghitung korelasi parsial: korelasi antara dua variabel setelah menghilangkan pengaruh linear variabel ketiga. Caranya meregresikan masing-masing pada variabel ketiga, lalu menghitung korelasi sisaan keduanya.

        Pada contoh es krim, korelasi parsial es krim dengan tenggelam setelah mengontrol suhu akan mendekati nol, menunjukkan bahwa hubungan semula berasal dari suhu. Teknik ini membantu tetapi hanya berlaku bila perancu terukur dan hubungannya linear.
        """),
        T("""
        ## Eksperimen dan kausalitas

        Standar emas untuk kausalitas adalah eksperimen terkontrol dengan penugasan acak. Dengan mengacak siapa mendapat perlakuan, semua perancu, terukur maupun tidak, seimbang di antara kelompok secara rata-rata. Perbedaan hasil lalu dapat dikaitkan dengan perlakuan.

        Bila eksperimen tidak mungkin, ada metode kuasi-eksperimen seperti selisih-dalam-selisih dan variabel instrumen, tetapi semuanya bergantung asumsi yang harus dibenarkan. Pelajari asumsinya sebelum percaya hasilnya.
        """),
        E(
            "A5-05-3-ex1",
            "mudah",
            """
            Tulis fungsi `matriks_korelasi(kolom)` yang menerima list kolom dan mengembalikan matriks (list of list) korelasi Pearson tiap pasangan, dibulatkan 4 desimal.
            """,
            """
            import math

            def matriks_korelasi(kolom):
                # TODO: implementasikan
                pass
            """,
            """
            m = matriks_korelasi([[1, 2, 3, 4], [2, 4, 6, 8], [4, 3, 2, 1]])
            assert m == [[1.0, 1.0, -1.0], [1.0, 1.0, -1.0], [-1.0, -1.0, 1.0]]
            m2 = matriks_korelasi([[1, 2, 3, 4, 5], [2, 4, 5, 4, 5]])
            assert m2 == [[1.0, 0.7746], [0.7746, 1.0]]
            assert len(matriks_korelasi([[1, 2, 3]])) == 1
            """,
            "Hitung korelasi untuk setiap pasangan kolom dengan dua perulangan.",
            """
            import math

            def matriks_korelasi(kolom):
                def corr(a, b):
                    n = len(a)
                    ma, mb = sum(a) / n, sum(b) / n
                    c = sum((p - ma) * (q - mb) for p, q in zip(a, b))
                    sa = math.sqrt(sum((p - ma) ** 2 for p in a))
                    sb = math.sqrt(sum((q - mb) ** 2 for q in b))
                    return round(c / (sa * sb), 4) + 0.0

                return [[corr(i, j) for j in kolom] for i in kolom]
            """,
        ),
        E(
            "A5-05-3-ex2",
            "sedang",
            """
            Tulis fungsi `korelasi_gabungan(kelompok)` yang menerima list tuple `(xs, ys)`, menggabungkan semua titik dari semua kelompok, dan mengembalikan korelasi Pearson gabungan dibulatkan 4 desimal.
            """,
            """
            import math

            def korelasi_gabungan(kelompok):
                # TODO: implementasikan
                pass
            """,
            """
            A = ([1, 2, 3], [5, 4, 3])
            B = ([6, 7, 8], [10, 9, 8])
            assert korelasi_gabungan([A, B]) == 0.8072
            assert korelasi_gabungan([A]) == -1.0
            assert korelasi_gabungan([([1, 2, 3], [1, 2, 3]), ([4, 5, 6], [4, 5, 6])]) == 1.0
            """,
            "Gabungkan semua x dan semua y lalu hitung korelasi Pearson.",
            """
            import math

            def korelasi_gabungan(kelompok):
                a = [v for xs, ys in kelompok for v in xs]
                b = [v for xs, ys in kelompok for v in ys]
                n = len(a)
                ma, mb = sum(a) / n, sum(b) / n
                c = sum((p - ma) * (q - mb) for p, q in zip(a, b))
                sa = math.sqrt(sum((p - ma) ** 2 for p in a))
                sb = math.sqrt(sum((q - mb) ** 2 for q in b))
                return round(c / (sa * sb), 4) + 0.0
            """,
        ),
        E(
            "A5-05-3-ex3",
            "sedang",
            """
            Tulis fungsi `simpson_terdeteksi(kelompok)` yang menerima list tuple `(xs, ys)` dan mengembalikan `True` bila korelasi gabungan berbeda tanda dengan korelasi di dalam semua kelompok, dan semua kelompok bertanda sama. Bila tidak kembalikan `False`.
            """,
            """
            import math

            def simpson_terdeteksi(kelompok):
                # TODO: implementasikan
                pass
            """,
            """
            A = ([1, 2, 3], [5, 4, 3])
            B = ([6, 7, 8], [10, 9, 8])
            assert simpson_terdeteksi([A, B]) is True
            assert simpson_terdeteksi([([1, 2, 3], [1, 2, 3]), ([4, 5, 6], [4, 5, 6])]) is False
            assert simpson_terdeteksi([A]) is False
            """,
            "Hitung korelasi tiap kelompok dan gabungan lalu bandingkan tandanya.",
            """
            import math

            def simpson_terdeteksi(kelompok):
                def corr(a, b):
                    n = len(a)
                    ma, mb = sum(a) / n, sum(b) / n
                    c = sum((p - ma) * (q - mb) for p, q in zip(a, b))
                    sa = math.sqrt(sum((p - ma) ** 2 for p in a))
                    sb = math.sqrt(sum((q - mb) ** 2 for q in b))
                    return c / (sa * sb)

                dalam = [corr(xs, ys) for xs, ys in kelompok]
                a = [v for xs, ys in kelompok for v in xs]
                b = [v for xs, ys in kelompok for v in ys]
                gab = corr(a, b)
                semua_neg = all(r < 0 for r in dalam)
                semua_pos = all(r > 0 for r in dalam)
                return (semua_neg and gab > 0) or (semua_pos and gab < 0)
            """,
        ),
        E(
            "A5-05-3-ex4",
            "menantang",
            """
            Tulis fungsi `korelasi_pencilan(a, b)` yang mengembalikan tuple `(pearson, spearman)` dibulatkan 4 desimal. Spearman adalah Pearson dari peringkat rata-rata.
            """,
            """
            import math

            def korelasi_pencilan(a, b):
                # TODO: implementasikan
                pass
            """,
            """
            assert korelasi_pencilan([1, 2, 3, 4, 5], [1, 2, 3, 4, 50]) == (0.7433, 1.0)
            assert korelasi_pencilan([1, 2, 3, 4, 5], [2, 4, 5, 4, 5]) == (0.7746, 0.7379)
            assert korelasi_pencilan([1, 2, 3, 4, 5], [5, 4, 3, 2, 1]) == (-1.0, -1.0)
            """,
            "Buat fungsi korelasi dan fungsi peringkat lalu terapkan keduanya.",
            """
            import math

            def korelasi_pencilan(a, b):
                def corr(p, q):
                    n = len(p)
                    mp, mq = sum(p) / n, sum(q) / n
                    c = sum((u - mp) * (v - mq) for u, v in zip(p, q))
                    sp = math.sqrt(sum((u - mp) ** 2 for u in p))
                    sq = math.sqrt(sum((v - mq) ** 2 for v in q))
                    return round(c / (sp * sq), 4) + 0.0

                def rank(data):
                    s = sorted(data)
                    out = []
                    for v in data:
                        pos = [i + 1 for i, w in enumerate(s) if w == v]
                        out.append(sum(pos) / len(pos))
                    return out

                return (corr(a, b), corr(rank(a), rank(b)))
            """,
        ),
    ],
    [
        M("Menarik kesimpulan kausal dari korelasi.", "Pertimbangkan perancu, arah, dan kebetulan."),
        M("Menggabungkan kelompok tanpa memeriksa korelasi per kelompok.", "Periksa paradoks Simpson."),
        M("Mencari pasangan berkorelasi tertinggi dari ratusan variabel lalu menceritakan kisahnya.", "Tetapkan hipotesis dulu dan uji pada data baru."),
    ],
    [
        Q("Matriks korelasi memiliki diagonal?", ["Satu", "Nol", "Rata-rata", "Bervariasi"], 0, "Korelasi diri sendiri.", hint="Diri."),
        Q("Paradoks Simpson terjadi saat?", ["Tren gabungan berlawanan dengan tren kelompok", "Data kosong", "Korelasi nol", "Sampel besar"], 0, "Kelompok memengaruhi.", hint="Gabungan."),
        Q("Variabel ketiga yang memengaruhi keduanya?", ["Perancu", "Residu", "Target", "Indeks"], 0, "Confounder.", hint="Cuaca."),
        Q("Bukti kausal terbaik berasal dari?", ["Eksperimen acak terkontrol", "Korelasi tinggi", "Grafik", "Rata-rata"], 0, "Penugasan acak.", hint="Acak."),
        Q("Multikolinearitas adalah?", ["Fitur berkorelasi sangat tinggi", "Fitur tidak berkorelasi", "Sampel kecil", "Data hilang"], 0, "Informasi redundan.", hint="Redundan."),
    ],
    [
        "Matriks korelasi meringkas hubungan antar banyak variabel.",
        "Paradoks Simpson membalik tren saat kelompok digabung.",
        "Korelasi tinggi bisa berasal dari perancu atau kebetulan.",
        "Kausalitas butuh eksperimen terkontrol atau analisis kausal cermat.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perhitungan yang cukup jelas dalam teks.", "brief": []}

write_module(
    "A5",
    5,
    "Korelasi dan kovariansi",
    105,
    [
        "Menghitung dan menafsirkan kovariansi dan korelasi",
        "Memilih Pearson, Spearman, atau Kendall",
        "Mengenali paradoks Simpson dan batas inferensi kausal",
    ],
    [l1, l2, l3],
    video,
    REF,
)
