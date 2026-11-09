import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

l1 = lesson(
    "A5-04-1",
    "Histogram dan pemilihan kotak",
    35,
    [
        "Menghitung frekuensi tiap kotak histogram",
        "Memilih jumlah kotak dengan aturan Sturges",
        "Mengubah frekuensi menjadi proporsi dan mencari kotak modus",
        "Menjelaskan pengaruh lebar kotak pada bentuk yang terlihat",
    ],
    [
        T("""
        ## Melihat bentuk, bukan hanya angka

        Rata-rata dan simpangan baku meringkas data menjadi dua bilangan, tetapi banyak distribusi berbeda bisa memiliki dua bilangan sama. Satu puncak, dua puncak, atau ekor panjang hanya tampak bila kita melihat **bentuk distribusi**. Pelajaran di modul ini membahas cara menggambarkan bentuk dengan histogram, ukuran kemiringan, dan kuantil.

        Bentuk menentukan ukuran ringkasan mana yang tepat dan model mana yang masuk akal. Data miring ke kanan cocok ditransformasi logaritma, sedangkan data dua puncak mungkin berarti dua subpopulasi yang harus dipisah.
        """),
        T("""
        ## Histogram

        **Histogram** membagi rentang data menjadi kotak berlebar sama, lalu menghitung berapa nilai jatuh ke tiap kotak. Tinggi batang adalah frekuensi kotak. Berbeda dengan diagram batang untuk kategori, kotak histogram bersebelahan karena sumbu horizontalnya kontinu.

        Konvensi umum adalah kotak tertutup di kiri dan terbuka di kanan, kecuali kotak terakhir yang tertutup di kedua sisi supaya nilai maksimum tidak hilang. Konvensi ini harus konsisten, karena nilai tepat di batas bisa pindah kotak bila aturannya berbeda.
        """),
        C(
            """
            d = [1, 1, 2, 2, 3, 4, 6, 9, 15, 30]
            lo, lebar, k = 0, 10, 4
            hitung = [0] * k
            for x in d:
                i = min(int((x - lo) // lebar), k - 1)
                hitung[i] += 1
            print(hitung)
            """,
            """
            [8, 1, 0, 1]
            """,
            """
            Delapan nilai berada di kotak pertama, satu di kotak kedua, kosong di ketiga, dan satu di keempat, memperlihatkan ekor kanan.
            """,
            filename="histogram.py",
        ),
        T("""
        ## Lebar kotak mengubah cerita

        Pilihan lebar kotak sangat memengaruhi tampilan. Kotak terlalu lebar menyatukan puncak berbeda sehingga detail hilang. Kotak terlalu sempit membuat batang berguncang acak dan puncak palsu muncul dari derau. Tidak ada lebar yang benar mutlak, jadi biasakan mencoba beberapa lebar sebelum menyimpulkan.

        Dua puncak yang tampak pada satu lebar tetapi lenyap pada lebar lain patut dicurigai sebagai artefak. Puncak yang bertahan pada berbagai lebar lebih mungkin nyata.
        """),
        T("""
        ## Aturan Sturges

        Aturan **Sturges** memberi titik awal praktis: jumlah kotak sama dengan `ceil(log2(n)) + 1`. Untuk 100 data ia menyarankan 8 kotak, untuk 10 data 5 kotak, dan untuk 8 data 4 kotak. Aturan ini bekerja baik untuk data kecil dan berbentuk mendekati normal.

        Untuk data besar atau miring, Sturges cenderung memberi kotak terlalu sedikit. Aturan lain seperti Freedman-Diaconis memakai IQR dan akar pangkat tiga dari n untuk menentukan lebar kotak, sehingga lebih tahan pencilan. Ini titik awal, bukan hukum.
        """),
        C(
            """
            import math

            for n in (8, 10, 100):
                print(n, math.ceil(math.log2(n)) + 1)
            """,
            """
            8 4
            10 5
            100 8
            """,
            """
            Jumlah kotak yang disarankan Sturges naik pelan seiring n, yaitu empat untuk delapan data dan delapan untuk seratus data.
            """,
            filename="sturges.py",
        ),
        T("""
        ## Dari frekuensi ke proporsi

        Frekuensi mutlak sulit dibandingkan antar dataset berukuran berbeda. **Frekuensi relatif** membagi tiap frekuensi dengan total, sehingga semua batang berjumlah satu. Dua sampel berukuran seratus dan sepuluh ribu dapat dibandingkan langsung lewat proporsi.

        Versi lanjutannya adalah **kepadatan**, yaitu proporsi dibagi lebar kotak, sehingga luas total histogram satu. Kepadatan memungkinkan menggambar kurva teoretis di atas histogram dan membandingkannya dengan satuan sama.
        """),
        C(
            """
            hitung = [1, 2, 3, 2, 1]
            total = sum(hitung)
            print([round(h / total, 4) for h in hitung])
            """,
            """
            [0.1111, 0.2222, 0.3333, 0.2222, 0.1111]
            """,
            """
            Proporsi tiap kotak berjumlah satu dan memperlihatkan bentuk simetris satu puncak.
            """,
            filename="frekuensi_relatif.py",
        ),
        T("""
        ## Kotak modus dan puncak

        Pada data kontinu, modus diperkirakan dari kotak tersibuk. Kotak itu dinamai kotak modus, dan titik tengahnya sering dipakai sebagai taksiran kasar modus. Taksiran ini bergantung pada lebar dan titik awal kotak, jadi ia hanya perkiraan.

        Jumlah puncak sama pentingnya. Distribusi dengan dua puncak jelas, misalnya tinggi badan campuran pria dan wanita, menandakan campuran dua kelompok. Rata-rata dan median pada distribusi seperti itu bisa jatuh di lembah yang hampir tidak berisi data, sehingga menyesatkan.
        """),
        C(
            """
            d = [1, 2, 2, 3, 3, 3, 4, 4, 5]
            lo, lebar, k = 1, 1, 5
            hitung = [0] * k
            for x in d:
                hitung[min(int((x - lo) // lebar), k - 1)] += 1
            print(hitung, hitung.index(max(hitung)))
            """,
            """
            [1, 2, 3, 2, 1] 2
            """,
            """
            Kotak ketiga memiliki frekuensi tertinggi sehingga menjadi kotak modus.
            """,
            filename="kotak_modus.py",
        ),
        T("""
        ## Praktik membuat histogram

        Mulailah dengan melihat rentang dan pencilan, lalu coba tiga sampai lima lebar kotak. Beri label sumbu dengan satuan, dan gunakan skala logaritma bila data berekor sangat panjang seperti pendapatan. Untuk membandingkan kelompok, pakai kotak dan skala sumbu yang sama agar perbedaan yang tampak benar-benar nyata.

        Hindari histogram bertumpuk yang sulit dibaca. Garis kepadatan berdampingan, histogram kecil berjajar, atau boxplot berdampingan biasanya lebih jelas untuk membandingkan beberapa kelompok sekaligus.
        """),
        K(
            "tip",
            """
            Coba beberapa lebar kotak sebelum menyimpulkan jumlah puncak. Puncak yang hanya muncul pada satu lebar kemungkinan artefak.
            """,
            title="Uji ketahanan bentuk",
        ),
        T("""
        ## Histogram untuk dua kelompok

        Saat membandingkan dua kelompok, misalnya nilai ujian dua kelas, gambarlah histogram keduanya dengan kotak dan skala sumbu sama. Perbedaan posisi puncak menunjukkan selisih pusat, perbedaan lebar menunjukkan selisih sebaran, dan perbedaan bentuk menunjukkan perbedaan kemiringan atau jumlah puncak.

        Bila ukuran kelompok berbeda jauh, pakai proporsi atau kepadatan sebagai sumbu vertikal. Tanpa itu kelompok besar tampak mendominasi hanya karena jumlah datanya lebih banyak, bukan karena distribusinya berbeda.
        """),
        E(
            "A5-04-1-ex1",
            "mudah",
            """
            Tulis fungsi `histogram_counts(data, lo, lebar, k)` yang mengembalikan list frekuensi `k` kotak berlebar `lebar` mulai dari `lo`. Nilai yang melebihi kotak terakhir dimasukkan ke kotak terakhir.
            """,
            """
            def histogram_counts(data, lo, lebar, k):
                # TODO: implementasikan
                pass
            """,
            """
            assert histogram_counts([1, 1, 2, 2, 3, 4, 6, 9, 15, 30], 0, 10, 4) == [8, 1, 0, 1]
            assert histogram_counts([1, 2, 2, 3, 3, 3, 4, 4, 5], 1, 1, 5) == [1, 2, 3, 2, 1]
            assert histogram_counts([], 0, 1, 3) == [0, 0, 0]
            """,
            "Hitung indeks kotak dengan pembagian lantai dan batasi pada kotak terakhir.",
            """
            def histogram_counts(data, lo, lebar, k):
                hitung = [0] * k
                for x in data:
                    hitung[min(int((x - lo) // lebar), k - 1)] += 1
                return hitung
            """,
        ),
        E(
            "A5-04-1-ex2",
            "sedang",
            """
            Tulis fungsi `sturges(n)` yang mengembalikan `ceil(log2(n)) + 1` sebagai bilangan bulat.
            """,
            """
            import math

            def sturges(n):
                # TODO: implementasikan
                pass
            """,
            """
            assert sturges(100) == 8
            assert sturges(10) == 5
            assert sturges(8) == 4
            assert sturges(1) == 1
            """,
            "Pakai logaritma basis dua dan pembulatan ke atas.",
            """
            import math

            def sturges(n):
                return math.ceil(math.log2(n)) + 1
            """,
        ),
        E(
            "A5-04-1-ex3",
            "sedang",
            """
            Tulis fungsi `frekuensi_relatif(hitung)` yang mengembalikan list proporsi dibulatkan 4 desimal. Bila total nol kembalikan list nol.
            """,
            """
            def frekuensi_relatif(hitung):
                # TODO: implementasikan
                pass
            """,
            """
            assert frekuensi_relatif([8, 1, 0, 1]) == [0.8, 0.1, 0.0, 0.1]
            assert frekuensi_relatif([1, 2, 3, 2, 1]) == [0.1111, 0.2222, 0.3333, 0.2222, 0.1111]
            assert frekuensi_relatif([0, 0]) == [0.0, 0.0]
            """,
            "Bagi tiap frekuensi dengan total dan tangani total nol.",
            """
            def frekuensi_relatif(hitung):
                total = sum(hitung)
                if total == 0:
                    return [0.0 for _ in hitung]
                return [round(h / total, 4) for h in hitung]
            """,
        ),
        E(
            "A5-04-1-ex4",
            "menantang",
            """
            Tulis fungsi `kotak_modus(data, lo, lebar, k)` yang mengembalikan indeks kotak dengan frekuensi tertinggi. Bila seri, kembalikan indeks terkecil.
            """,
            """
            def kotak_modus(data, lo, lebar, k):
                # TODO: implementasikan
                pass
            """,
            """
            assert kotak_modus([1, 1, 2, 2, 3, 4, 6, 9, 15, 30], 0, 10, 4) == 0
            assert kotak_modus([1, 2, 2, 3, 3, 3, 4, 4, 5], 1, 1, 5) == 2
            assert kotak_modus([1, 5], 1, 1, 5) == 0
            """,
            "Bangun frekuensi kotak lalu cari indeks maksimum pertama.",
            """
            def kotak_modus(data, lo, lebar, k):
                hitung = [0] * k
                for x in data:
                    hitung[min(int((x - lo) // lebar), k - 1)] += 1
                return hitung.index(max(hitung))
            """,
        ),
    ],
    [
        M("Menyimpulkan jumlah puncak dari satu lebar kotak saja.", "Coba beberapa lebar dan lihat yang bertahan."),
        M("Membandingkan histogram dengan sumbu dan kotak berbeda.", "Samakan kotak dan skala."),
        M("Menganggap aturan Sturges selalu optimal.", "Pakai sebagai titik awal lalu sesuaikan."),
    ],
    [
        Q("Histogram untuk data?", ["Kontinu", "Nominal", "Hanya ordinal", "Teks"], 0, "Kotak pada sumbu kontinu.", hint="Rentang."),
        Q("Sturges memberi jumlah kotak?", ["ceil(log2 n) + 1", "n", "sqrt n", "n / 2"], 0, "Titik awal.", hint="Logaritma."),
        Q("Kotak terlalu sempit menyebabkan?", ["Puncak palsu dari derau", "Detail hilang", "Tanpa efek", "Data bertambah"], 0, "Guncangan acak.", hint="Derau."),
        Q("Frekuensi relatif berjumlah?", ["Satu", "n", "Nol", "Seratus"], 0, "Proporsi.", hint="Total."),
        Q("Dua puncak menandakan?", ["Kemungkinan dua subpopulasi", "Pasti kesalahan", "Distribusi normal", "Tanpa arti"], 0, "Campuran.", hint="Campuran."),
    ],
    [
        "Histogram memperlihatkan bentuk yang disembunyikan ringkasan angka.",
        "Lebar kotak memengaruhi bentuk yang terlihat sehingga perlu diuji.",
        "Sturges adalah titik awal jumlah kotak.",
        "Frekuensi relatif dan kepadatan membandingkan dataset berbeda ukuran.",
    ],
    [],
)

l2 = lesson(
    "A5-04-2",
    "Kemiringan dan kurtosis",
    35,
    [
        "Menghitung skewness dan menafsirkan tandanya",
        "Menghitung kurtosis lebih dan menafsirkan ekor",
        "Menghitung koefisien kemiringan Pearson dan Bowley",
        "Menerapkan transformasi logaritma untuk mengurangi kemiringan",
    ],
    [
        T("""
        ## Mengukur bentuk dengan angka

        Histogram memberi gambaran bentuk, tetapi kadang kita membutuhkan angka untuk dibandingkan, dilacak, atau dipakai sebagai uji otomatis. **Momen** tingkat tinggi menjawabnya: rata-rata adalah momen pertama, varians momen kedua terpusat, kemiringan momen ketiga terstandardisasi, dan kurtosis momen keempat.

        Dua ukuran bentuk ini tidak bersatuan, sehingga bisa dibandingkan antar variabel. Namun keduanya sangat sensitif pada pencilan karena memakai pangkat tiga dan empat, jadi tafsirkan dengan hati-hati pada sampel kecil.
        """),
        T("""
        ## Skewness

        **Skewness** adalah rata-rata dari `((x - rata) / simpangan baku)^3`. Pangkat tiga mempertahankan tanda, sehingga ekor kanan panjang menghasilkan nilai positif dan ekor kiri panjang negatif. Data simetris menghasilkan nilai sekitar nol.

        Aturan praktis menganggap nilai mutlak di bawah 0,5 hampir simetris, antara 0,5 dan 1 miring sedang, dan di atas 1 sangat miring. Batas ini hanya pedoman. Pada sampel kecil, skewness sendiri berfluktuasi besar sehingga jangan membaca terlalu banyak darinya.
        """),
        C(
            """
            def skew(x):
                n = len(x)
                m = sum(x) / n
                s = (sum((v - m) ** 2 for v in x) / n) ** 0.5
                return sum(((v - m) / s) ** 3 for v in x) / n

            d = [1, 1, 2, 2, 3, 4, 6, 9, 15, 30]
            print(round(skew([1, 2, 3, 4, 5]), 4))
            print(round(skew(d), 4))
            print(round(skew([-v for v in d]), 4))
            """,
            """
            0.0
            1.7516
            -1.7516
            """,
            """
            Data simetris memberi nol, ekor kanan memberi nilai positif, dan mencerminkan data membalik tandanya.
            """,
            filename="skewness.py",
        ),
        T("""
        ## Kurtosis

        **Kurtosis** adalah rata-rata dari `((x - rata) / simpangan baku)^4`. Distribusi normal memiliki kurtosis 3, sehingga sering dilaporkan sebagai **kurtosis lebih** dengan mengurangi 3. Nilai positif berarti ekor lebih berat dan puncak lebih runcing daripada normal, nilai negatif berarti ekor lebih ringan dan lebih datar.

        Kurtosis pada dasarnya mengukur seberapa sering nilai ekstrem muncul, bukan seberapa runcing puncaknya. Pada keuangan, kurtosis lebih tinggi berarti guncangan besar lebih sering terjadi daripada yang diperkirakan distribusi normal.
        """),
        C(
            """
            def kurt(x):
                n = len(x)
                m = sum(x) / n
                s = (sum((v - m) ** 2 for v in x) / n) ** 0.5
                return sum(((v - m) / s) ** 4 for v in x) / n - 3

            print(round(kurt([1, 2, 3, 4, 5]), 4))
            print(round(kurt([1, 1, 1, 1, 10]), 4))
            print(round(kurt([-1, 1]), 4))
            """,
            """
            -1.3
            0.25
            -2.0
            """,
            """
            Data seragam memiliki ekor ringan sehingga kurtosis lebih negatif, sedangkan satu nilai jauh membuat ekor lebih berat.
            """,
            filename="kurtosis.py",
        ),
        T("""
        ## Ukuran kemiringan alternatif

        Karena skewness peka pada pencilan, ada ukuran yang lebih kokoh. **Koefisien kedua Pearson** adalah `3 * (rata - median) / simpangan baku`, yang memanfaatkan selisih rata-rata dan median seperti yang dibahas di pelajaran pemusatan. **Koefisien Bowley** memakai kuartil: `(Q3 + Q1 - 2 * Q2) / (Q3 - Q1)`, bernilai antara minus satu dan satu.

        Bowley hanya memakai tengah data sehingga tahan pencilan. Ia bernilai nol bila jarak median ke kedua kuartil sama, dan positif bila Q3 lebih jauh dari median daripada Q1.
        """),
        C(
            """
            import statistics

            d = [1, 1, 2, 2, 3, 4, 6, 9, 15, 30]
            ps = 3 * (statistics.mean(d) - statistics.median(d)) / statistics.pstdev(d)
            print(round(ps, 4))
            """,
            """
            1.3216
            """,
            """
            Rata-rata jauh di atas median sehingga koefisien Pearson positif dan besar, menandakan kemiringan ke kanan.
            """,
            filename="pearson_skew.py",
        ),
        T("""
        ## Mengurangi kemiringan dengan transformasi

        Banyak model bekerja lebih baik pada data yang mendekati simetris. Untuk data miring ke kanan dengan nilai positif, transformasi logaritma menekan ekor panjang. Akar kuadrat adalah versi lebih lembut, dan transformasi Box-Cox mencari pangkat terbaik secara otomatis. Untuk miring ke kiri, transformasi dibalik dengan memantulkan data lebih dulu.

        Pada data contoh, logaritma menurunkan skewness dari sekitar 1,75 menjadi sekitar 0,38. Setelah transformasi, interpretasi berubah: selisih pada skala logaritma berarti rasio pada skala asli.
        """),
        C(
            """
            import math

            def skew(x):
                n = len(x)
                m = sum(x) / n
                s = (sum((v - m) ** 2 for v in x) / n) ** 0.5
                return sum(((v - m) / s) ** 3 for v in x) / n

            d = [1, 1, 2, 2, 3, 4, 6, 9, 15, 30]
            print(round(skew(d), 4), round(skew([math.log(v) for v in d]), 4))
            """,
            """
            1.7516 0.3806
            """,
            """
            Transformasi logaritma memotong skewness dari satu koma tujuh lima menjadi nol koma tiga delapan.
            """,
            filename="transformasi_log.py",
        ),
        T("""
        ## Menggabungkan semuanya

        Gambaran lengkap bentuk datang dari kombinasi: histogram untuk melihat, skewness dan kurtosis untuk mengukur, dan kuantil untuk menggambarkan ekor secara kokoh. Satu angka tidak pernah cukup, dan angka tanpa gambar bisa menyesatkan.

        Dalam praktik, mulailah dengan histogram, hitung skewness dan kurtosis sebagai ringkasan, lalu uji hipotesis kenormalan secara formal bila model membutuhkannya. Banyak uji tersedia, tetapi pada sampel besar uji hampir selalu menolak kenormalan sempurna walaupun penyimpangannya kecil dan tidak penting.
        """),
        K(
            "warn",
            """
            Skewness dan kurtosis sangat peka pada pencilan dan tidak stabil pada sampel kecil. Selalu lihat histogramnya sebelum menafsirkan angka.
            """,
            title="Momen tinggi itu rapuh",
        ),
        T("""
        ## Membaca pasangan skewness dan kurtosis

        Kedua angka sebaiknya dibaca berpasangan. Skewness mendekati nol dengan kurtosis lebih mendekati nol menandakan bentuk mendekati lonceng normal. Skewness besar dengan kurtosis besar biasanya menandakan ekor panjang sebelah dengan nilai ekstrem jarang tetapi besar, seperti pendapatan atau ukuran file.

        Skewness nol dengan kurtosis sangat negatif menandakan data merata seperti seragam atau dua kelompok terpisah jelas. Pola semacam ini mengarahkan pilihan model dan transformasi berikutnya.
        """),
        T("""
        ## Uji kenormalan secara praktis

        Banyak metode klasik mengasumsikan normalitas, sehingga kita perlu memeriksanya. Cara terbaik adalah visual: histogram, boxplot, dan plot kuantil-kuantil yang membandingkan kuantil data dengan kuantil normal. Bila titik mengikuti garis lurus, data mendekati normal, dan lengkungan menunjukkan kemiringan atau ekor berat.

        Uji formal seperti Shapiro-Wilk melengkapinya. Pada sampel kecil ujinya lemah, dan pada sampel besar terlalu sensitif, sehingga keputusan akhir tetap bertumpu pada gambar dan pemahaman tentang seberapa kuat metode terhadap penyimpangan.
        """),
        E(
            "A5-04-2-ex1",
            "mudah",
            """
            Tulis fungsi `skewness(data)` yang mengembalikan rata-rata `((x - rata) / simpangan_baku_populasi) ** 3` dibulatkan 4 desimal. Untuk data konstan kembalikan `0.0`.
            """,
            """
            def skewness(data):
                # TODO: implementasikan
                pass
            """,
            """
            assert skewness([1, 2, 3, 4, 5]) == 0.0
            assert skewness([1, 1, 2, 2, 3, 4, 6, 9, 15, 30]) == 1.7516
            assert skewness([-v for v in [1, 1, 2, 2, 3, 4, 6, 9, 15, 30]]) == -1.7516
            assert skewness([1, 1, 1, 1, 10]) == 1.5
            assert skewness([4, 4, 4]) == 0.0
            """,
            "Standardisasi data lalu rata-ratakan pangkat tiga, tangani simpangan baku nol.",
            """
            def skewness(data):
                n = len(data)
                m = sum(data) / n
                s = (sum((v - m) ** 2 for v in data) / n) ** 0.5
                if s == 0:
                    return 0.0
                return round(sum(((v - m) / s) ** 3 for v in data) / n, 4) + 0.0
            """,
        ),
        E(
            "A5-04-2-ex2",
            "sedang",
            """
            Tulis fungsi `kurtosis_lebih(data)` yang mengembalikan rata-rata pangkat empat nilai terstandardisasi dikurangi 3, dibulatkan 4 desimal. Untuk data konstan kembalikan `None`.
            """,
            """
            def kurtosis_lebih(data):
                # TODO: implementasikan
                pass
            """,
            """
            assert kurtosis_lebih([1, 2, 3, 4, 5]) == -1.3
            assert kurtosis_lebih([1, 1, 1, 1, 10]) == 0.25
            assert kurtosis_lebih([-1, 1]) == -2.0
            assert kurtosis_lebih([1, 1, 2, 2, 3, 4, 6, 9, 15, 30]) == 1.953
            assert kurtosis_lebih([3, 3]) is None
            """,
            "Standardisasi dengan simpangan baku populasi lalu pangkatkan empat dan kurangi tiga.",
            """
            def kurtosis_lebih(data):
                n = len(data)
                m = sum(data) / n
                s = (sum((v - m) ** 2 for v in data) / n) ** 0.5
                if s == 0:
                    return None
                return round(sum(((v - m) / s) ** 4 for v in data) / n - 3, 4)
            """,
        ),
        E(
            "A5-04-2-ex3",
            "sedang",
            """
            Tulis fungsi `pearson_skew(data)` yang mengembalikan `3 * (rata - median) / simpangan_baku_populasi` dibulatkan 4 desimal. Untuk data konstan kembalikan `0.0`.
            """,
            """
            def pearson_skew(data):
                # TODO: implementasikan
                pass
            """,
            """
            assert pearson_skew([1, 1, 2, 2, 3, 4, 6, 9, 15, 30]) == 1.3216
            assert pearson_skew([1, 2, 3, 4, 5]) == 0.0
            assert pearson_skew([2, 4, 4, 4, 5, 5, 7, 9]) == 0.75
            assert pearson_skew([6, 6, 6]) == 0.0
            """,
            "Hitung rata-rata, median, dan simpangan baku populasi lalu terapkan rumus.",
            """
            def pearson_skew(data):
                s = sorted(data)
                n = len(s)
                med = s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2
                m = sum(s) / n
                sd = (sum((v - m) ** 2 for v in s) / n) ** 0.5
                if sd == 0:
                    return 0.0
                return round(3 * (m - med) / sd, 4) + 0.0
            """,
        ),
        E(
            "A5-04-2-ex4",
            "menantang",
            """
            Tulis fungsi `bentuk(data)` yang mengembalikan `'miring kanan'` bila skewness populasi lebih dari 0.5, `'miring kiri'` bila kurang dari -0.5, dan `'simetris'` bila tidak.
            """,
            """
            def bentuk(data):
                # TODO: implementasikan
                pass
            """,
            """
            assert bentuk([1, 1, 2, 2, 3, 4, 6, 9, 15, 30]) == 'miring kanan'
            assert bentuk([-v for v in [1, 1, 2, 2, 3, 4, 6, 9, 15, 30]]) == 'miring kiri'
            assert bentuk([1, 2, 3, 4, 5]) == 'simetris'
            assert bentuk([2, 4, 4, 4, 5, 5, 7, 9]) == 'miring kanan'
            assert bentuk([1, 2, 3, 4, 5, 6]) == 'simetris'
            """,
            "Hitung skewness lalu bandingkan dengan batas plus minus nol koma lima.",
            """
            def bentuk(data):
                n = len(data)
                m = sum(data) / n
                s = (sum((v - m) ** 2 for v in data) / n) ** 0.5
                sk = 0.0 if s == 0 else sum(((v - m) / s) ** 3 for v in data) / n
                if sk > 0.5:
                    return 'miring kanan'
                if sk < -0.5:
                    return 'miring kiri'
                return 'simetris'
            """,
        ),
    ],
    [
        M("Menafsirkan skewness dari sampel sangat kecil.", "Perlu sampel cukup dan histogram."),
        M("Mengira kurtosis mengukur keruncingan puncak saja.", "Kurtosis terutama mengukur berat ekor."),
        M("Lupa mengurangi 3 dan membandingkan dengan nol.", "Kurtosis normal 3, kurtosis lebih normal nol."),
    ],
    [
        Q("Skewness positif berarti?", ["Ekor kanan panjang", "Ekor kiri panjang", "Simetris", "Tanpa ekor"], 0, "Pangkat tiga mempertahankan tanda.", hint="Kanan."),
        Q("Kurtosis lebih normal bernilai?", ["Nol", "Satu", "Tiga", "Negatif"], 0, "Kurtosis dikurangi tiga.", hint="Normal."),
        Q("Kurtosis tinggi berarti?", ["Ekor lebih berat", "Ekor lebih ringan", "Simetris", "Tanpa pencilan"], 0, "Ekstrem sering.", hint="Ekor."),
        Q("Transformasi pengurang miring kanan?", ["Logaritma", "Kuadrat", "Eksponen", "Kebalikan tanda"], 0, "Menekan ekor.", hint="Log."),
        Q("Bowley memakai?", ["Kuartil", "Momen ketiga", "Modus", "Rentang"], 0, "Kokoh.", hint="Q1 Q2 Q3."),
    ],
    [
        "Skewness mengukur arah kemiringan dan kurtosis mengukur berat ekor.",
        "Kedua momen tinggi sensitif pada pencilan dan sampel kecil.",
        "Pearson dan Bowley adalah ukuran kemiringan alternatif.",
        "Logaritma menekan ekor kanan panjang.",
    ],
    [],
)

l3 = lesson(
    "A5-04-3",
    "Kuantil, persentil, dan fungsi distribusi empiris",
    35,
    [
        "Menghitung fungsi distribusi empiris",
        "Menghitung peringkat persentil sebuah nilai",
        "Menghitung persentil dengan interpolasi linear",
        "Menghitung koefisien Bowley dari kuartil",
    ],
    [
        T("""
        ## Kuantil menggambarkan seluruh distribusi

        Kuantil menjawab pertanyaan dari dua arah. Diberi proporsi, kuantil menjawab nilai di bawah mana proporsi itu berada. Diberi nilai, **peringkat persentil** menjawab proporsi data yang berada di bawahnya. Keduanya memberi gambaran distribusi tanpa asumsi bentuk dan tahan pencilan.

        Kuantil dipakai di mana-mana: kurva pertumbuhan anak, skor ujian standar, batas waktu respons layanan, dan ambang pencilan. Pelajaran ini merangkum semuanya dan menutup modul bentuk distribusi.
        """),
        T("""
        ## Fungsi distribusi empiris

        **Fungsi distribusi empiris** atau ECDF di titik `t` adalah proporsi data yang bernilai kurang dari atau sama dengan `t`. Ia berbentuk tangga yang naik satu per `n` di setiap nilai data, mulai dari nol di kiri semua data hingga satu di kanan semua data.

        ECDF adalah penaksir tanpa asumsi bagi fungsi distribusi kumulatif sebenarnya. Berbeda dengan histogram, ia tidak bergantung pada pilihan lebar kotak, sehingga menampilkan semua data tanpa pengelompokan.
        """),
        C(
            """
            d = [1, 1, 2, 2, 3, 4, 6, 9, 15, 30]

            def ecdf(x, t):
                return sum(1 for v in x if v <= t) / len(x)

            print([ecdf(d, t) for t in (0, 3, 5, 30)])
            """,
            """
            [0.0, 0.5, 0.6, 1.0]
            """,
            """
            ECDF naik dari nol sebelum data sampai satu pada nilai maksimum, dengan separuh data berada pada tiga atau kurang.
            """,
            filename="ecdf.py",
        ),
        T("""
        ## Peringkat persentil

        **Peringkat persentil** sebuah nilai adalah persentase data yang lebih kecil darinya. Nilai ujian dengan peringkat persentil 80 berarti delapan puluh persen peserta mendapat nilai lebih rendah. Konsep ini mengubah nilai mentah menjadi posisi relatif sehingga bermakna antar ujian berbeda.

        Ada variasi definisi: sebagian menghitung nilai sama sebagai setengah di bawah. Kita memakai definisi ketat yang menghitung hanya nilai lebih kecil. Karena itu bedakan peringkat persentil dengan persentil, yang berjalan arah sebaliknya.
        """),
        C(
            """
            d = [1, 1, 2, 2, 3, 4, 6, 9, 15, 30]

            def peringkat(x, t):
                return 100 * sum(1 for v in x if v < t) / len(x)

            print(peringkat(d, 3), peringkat(d, 15))
            """,
            """
            40.0 80.0
            """,
            """
            Empat dari sepuluh data lebih kecil dari tiga dan delapan dari sepuluh lebih kecil dari lima belas.
            """,
            filename="peringkat_persentil.py",
        ),
        T("""
        ## Persentil

        **Persentil** ke-`p` adalah nilai yang melampaui `p` persen data. Persentil ke-50 adalah median, ke-25 dan ke-75 adalah kuartil, dan persentil ke-10, 20, sampai 90 adalah desil. Persentil sering dipakai dalam rekayasa layanan: p95 waktu respons berarti sembilan puluh lima persen permintaan lebih cepat dari nilai itu.

        Untuk menghitungnya pada sampel kita memakai posisi `(n - 1) * p / 100` pada data terurut dan menginterpolasi linear di antara dua elemen terdekat, definisi yang sama dengan pelajaran sebelumnya.
        """),
        C(
            """
            d = [1, 1, 2, 2, 3, 4, 6, 9, 15, 30]

            def persentil(x, p):
                s = sorted(x)
                pos = (len(s) - 1) * p / 100
                lo = int(round(pos, 6))
                hi = min(lo + 1, len(s) - 1)
                return s[lo] + (s[hi] - s[lo]) * (pos - lo)

            print([round(persentil(d, p), 4) for p in (10, 50, 90, 95)])
            """,
            """
            [1.0, 3.5, 16.5, 23.25]
            """,
            """
            Persentil sembilan puluh lima berada jauh di ekor kanan, sedangkan median hanya tiga koma lima.
            """,
            filename="persentil.py",
        ),
        T("""
        ## Ekor dan persentil tinggi

        Persentil tinggi menggambarkan ekor dengan jujur. Rata-rata waktu respons 200 milidetik bisa menyembunyikan bahwa satu persen permintaan memakan lima detik. Pengguna merasakan ekor itu, sehingga insinyur melaporkan p95, p99, bahkan p99,9 sebagai ukuran pengalaman terburuk yang realistis.

        Persentil tinggi memerlukan data sangat banyak agar stabil. Taksiran p99,9 dari seribu data hanya didasarkan pada satu atau dua nilai teratas, sehingga sangat berisik. Laporkan jumlah data bersama persentil ekstrem.
        """),
        T("""
        ## Kemiringan dari kuantil

        Kuartil juga memberi ukuran kemiringan kokoh, yaitu koefisien Bowley: `(Q3 + Q1 - 2 * Q2) / (Q3 - Q1)`. Pembilangnya membandingkan jarak median ke tiap kuartil, sementara penyebutnya adalah IQR sehingga hasilnya tanpa satuan dan terbatas antara minus satu dan satu.

        Untuk data contoh, Q1 adalah 2, median 3,5, dan Q3 8,25, sehingga Bowley sekitar 0,52, menandakan kemiringan ke kanan yang cukup jelas. Karena hanya memakai tengah data, nilainya tidak ikut bergoyang oleh pencilan.
        """),
        C(
            """
            def kuantil(x, q):
                s = sorted(x)
                p = (len(s) - 1) * q
                lo = int(round(p, 6))
                hi = min(lo + 1, len(s) - 1)
                return s[lo] + (s[hi] - s[lo]) * (p - lo)

            d = [1, 1, 2, 2, 3, 4, 6, 9, 15, 30]
            q1, q2, q3 = kuantil(d, 0.25), kuantil(d, 0.5), kuantil(d, 0.75)
            print(q1, q2, q3, round((q3 + q1 - 2 * q2) / (q3 - q1), 4))
            """,
            """
            2.0 3.5 8.25 0.52
            """,
            """
            Jarak median ke Q3 lebih besar daripada ke Q1 sehingga koefisien Bowley positif nol koma lima dua.
            """,
            filename="bowley.py",
        ),
        T("""
        ## Merangkum bentuk distribusi

        Rangkuman akhir modul: gambar histogram atau ECDF untuk melihat, ukur skewness dan kurtosis untuk meringkas, dan laporkan kuantil untuk ekor. Pilih transformasi bila model membutuhkan simetri. Setiap ukuran punya kelebihan dan kelemahan, dan kombinasinya memberi gambaran paling jujur.

        Modul berikutnya membahas hubungan antar variabel lewat kovariansi dan korelasi, setelah kita mampu menggambarkan tiap variabel sendiri-sendiri.
        """),
        K(
            "tip",
            """
            Untuk metrik layanan laporkan p50, p95, dan p99 bersama jumlah data. Rata-rata saja menyembunyikan pengalaman pengguna terburuk.
            """,
            title="Laporkan ekor",
        ),
        T("""
        ## Kuantil sebagai bahasa umum

        Kuantil menyatukan banyak konsep lain. Median, kuartil, desil, dan persentil hanyalah nama untuk kuantil tertentu. Pencilan Tukey, IQR, dan ukuran Bowley semuanya dibangun dari kuantil. Bahkan boxplot adalah gambar lima kuantil.

        Karena tahan pencilan dan tanpa asumsi bentuk, kuantil menjadi alat utama pada data nyata yang berantakan. Biasakan memikirkan distribusi sebagai fungsi kuantil: untuk tiap proporsi ada satu nilai, dan seluruh bentuk distribusi terbaca dari kurva ini.
        """),
        E(
            "A5-04-3-ex1",
            "mudah",
            """
            Tulis fungsi `ecdf(data, t)` yang mengembalikan proporsi data yang kurang dari atau sama dengan `t`.
            """,
            """
            def ecdf(data, t):
                # TODO: implementasikan
                pass
            """,
            """
            d = [1, 1, 2, 2, 3, 4, 6, 9, 15, 30]
            assert ecdf(d, 3) == 0.5
            assert ecdf(d, 0) == 0.0
            assert ecdf(d, 30) == 1.0
            assert ecdf(d, 5) == 0.6
            """,
            "Hitung banyak nilai yang tidak melebihi t lalu bagi dengan n.",
            """
            def ecdf(data, t):
                return sum(1 for v in data if v <= t) / len(data)
            """,
        ),
        E(
            "A5-04-3-ex2",
            "sedang",
            """
            Tulis fungsi `peringkat_persentil(data, t)` yang mengembalikan persentase data yang lebih kecil dari `t`.
            """,
            """
            def peringkat_persentil(data, t):
                # TODO: implementasikan
                pass
            """,
            """
            d = [1, 1, 2, 2, 3, 4, 6, 9, 15, 30]
            assert peringkat_persentil(d, 3) == 40.0
            assert peringkat_persentil(d, 15) == 80.0
            assert peringkat_persentil(d, 0) == 0.0
            assert peringkat_persentil(d, 100) == 100.0
            """,
            "Hitung nilai yang strictly lebih kecil lalu kalikan seratus dan bagi dengan n.",
            """
            def peringkat_persentil(data, t):
                return 100 * sum(1 for v in data if v < t) / len(data)
            """,
        ),
        E(
            "A5-04-3-ex3",
            "sedang",
            """
            Tulis fungsi `persentil(data, p)` untuk `p` antara 0 dan 100 dengan interpolasi linear pada posisi `(n - 1) * p / 100`, dibulatkan 4 desimal.
            """,
            """
            def persentil(data, p):
                # TODO: implementasikan
                pass
            """,
            """
            d = [1, 1, 2, 2, 3, 4, 6, 9, 15, 30]
            assert persentil(d, 10) == 1.0
            assert persentil(d, 50) == 3.5
            assert persentil(d, 90) == 16.5
            assert persentil(d, 95) == 23.25
            """,
            "Hitung posisi pecahan lalu interpolasikan antar dua elemen terurut.",
            """
            def persentil(data, p):
                s = sorted(data)
                pos = (len(s) - 1) * p / 100
                lo = int(round(pos, 6))
                hi = min(lo + 1, len(s) - 1)
                return round(s[lo] + (s[hi] - s[lo]) * (pos - lo), 4)
            """,
        ),
        E(
            "A5-04-3-ex4",
            "menantang",
            """
            Tulis fungsi `bowley(data)` yang mengembalikan `(Q3 + Q1 - 2 * Q2) / (Q3 - Q1)` dibulatkan 4 desimal dengan kuartil berinterpolasi linear. Bila IQR nol kembalikan `0.0`.
            """,
            """
            def bowley(data):
                # TODO: implementasikan
                pass
            """,
            """
            assert bowley([1, 1, 2, 2, 3, 4, 6, 9, 15, 30]) == 0.52
            assert bowley([1, 2, 3, 4, 5]) == 0.0
            assert bowley([5, 5, 5]) == 0.0
            assert bowley([-v for v in [1, 1, 2, 2, 3, 4, 6, 9, 15, 30]]) == -0.52
            """,
            "Hitung tiga kuartil dengan interpolasi lalu terapkan rumus dan tangani IQR nol.",
            """
            def bowley(data):
                s = sorted(data)

                def kuantil(q):
                    p = (len(s) - 1) * q
                    lo = int(round(p, 6))
                    hi = min(lo + 1, len(s) - 1)
                    return s[lo] + (s[hi] - s[lo]) * (p - lo)

                q1, q2, q3 = kuantil(0.25), kuantil(0.5), kuantil(0.75)
                if q3 == q1:
                    return 0.0
                return round((q3 + q1 - 2 * q2) / (q3 - q1), 4) + 0.0
            """,
        ),
    ],
    [
        M("Mengira peringkat persentil sama dengan persentil.", "Peringkat dari nilai ke proporsi, persentil dari proporsi ke nilai."),
        M("Melaporkan p99 dari sampel kecil.", "Persentil ekstrem butuh data sangat banyak."),
        M("Hanya melaporkan rata-rata waktu respons.", "Laporkan juga p95 dan p99."),
    ],
    [
        Q("ECDF di t adalah?", ["Proporsi data <= t", "Banyak data", "Rata-rata", "Median"], 0, "Fungsi tangga.", hint="Kumulatif."),
        Q("Persentil ke-50 adalah?", ["Median", "Rata-rata", "Modus", "Maksimum"], 0, "Kuantil 0,5.", hint="Tengah."),
        Q("Peringkat persentil menjawab?", ["Proporsi data di bawah nilai", "Nilai pada proporsi", "Rata-rata", "Sebaran"], 0, "Dari nilai ke proporsi.", hint="Arah."),
        Q("Bowley berada pada rentang?", ["-1 sampai 1", "0 sampai 1", "0 sampai tak hingga", "-3 sampai 3"], 0, "Terbatas.", hint="Terbatas."),
        Q("p95 waktu respons berarti?", ["95 persen permintaan lebih cepat", "Rata-rata 95", "95 permintaan", "5 persen lebih cepat"], 0, "Ekor.", hint="Persentil."),
    ],
    [
        "ECDF menaksir distribusi kumulatif tanpa pilihan kotak.",
        "Peringkat persentil dan persentil berjalan arah berlawanan.",
        "Persentil tinggi menggambarkan ekor dan perlu data banyak.",
        "Bowley mengukur kemiringan dari kuartil secara kokoh.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perhitungan yang cukup jelas dalam teks.", "brief": []}

write_module(
    "A5",
    4,
    "Bentuk distribusi dan kuantil",
    105,
    [
        "Menggambarkan bentuk distribusi dengan histogram dan ECDF",
        "Mengukur kemiringan dan kurtosis serta menafsirkannya",
        "Memakai kuantil dan persentil untuk menggambarkan ekor",
    ],
    [l1, l2, l3],
    video,
    REF,
)
