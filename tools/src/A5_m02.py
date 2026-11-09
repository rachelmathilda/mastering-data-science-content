import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

l1 = lesson(
    "A5-02-1",
    "Rata-rata aritmetika dan variannya",
    35,
    [
        "Menghitung rata-rata aritmetika dan menjelaskan sifat-sifatnya",
        "Menghitung rata-rata berbobot dan menggabungkan rata-rata kelompok",
        "Menjelaskan sensitivitas rata-rata terhadap pencilan",
        "Menghitung rata-rata secara inkremental pada aliran data",
    ],
    [
        T("""
        ## Satu angka untuk mewakili semua

        Ketika kita memiliki ribuan nilai, kita sering membutuhkan satu angka yang mewakili pusat data. **Ukuran pemusatan** menjawab kebutuhan ini: di mana kira-kira nilai-nilai itu berkumpul. Tiga yang paling umum adalah rata-rata, median, dan modus, masing-masing menjawab arti pusat dengan cara berbeda.

        Pelajaran ini membahas rata-rata aritmetika, yang paling dikenal. Dua pelajaran berikutnya membahas median, modus, dan rata-rata lain. Memilih ukuran yang tepat bergantung pada skala data, bentuk distribusi, dan pertanyaan yang ingin dijawab.
        """),
        T("""
        ## Definisi dan tafsir

        **Rata-rata aritmetika** adalah jumlah semua nilai dibagi banyaknya nilai: `rata-rata = jumlah / n`. Secara fisik ia adalah titik keseimbangan: bila tiap nilai digambarkan sebagai bobot yang sama pada batang, rata-rata adalah titik tumpu tempat batang seimbang. Itu sebabnya nilai yang sangat jauh menarik rata-rata ke arahnya.

        Rata-rata hanya bermakna untuk data interval dan rasio. Untuk data nominal ia tidak punya arti, dan untuk ordinal ia mengasumsikan jarak sama antar tingkat. Pastikan skala data cocok sebelum menghitungnya.
        """),
        C(
            """
            d = [2, 4, 4, 4, 5, 5, 7, 9]
            m = sum(d) / len(d)
            print(m)
            """,
            """
            5.0
            """,
            """
            Jumlah empat puluh dibagi delapan nilai memberi rata-rata lima.
            """,
            filename="rata_rata.py",
        ),
        T("""
        ## Sifat-sifat penting

        Dua sifat membuat rata-rata sangat berguna. Pertama, jumlah selisih semua nilai dari rata-rata selalu nol, yang menjelaskan interpretasi titik keseimbangan. Kedua, rata-rata bersifat linear: bila kita mengubah tiap nilai menjadi `a * x + b`, rata-ratanya menjadi `a * rata-rata + b`. Mengubah satuan dari meter ke sentimeter cukup mengalikan rata-rata dengan seratus.

        Rata-rata juga meminimalkan jumlah kuadrat selisih: nilai `c` yang membuat `jumlah (x - c)^2` terkecil adalah rata-rata. Sifat ini menghubungkannya dengan regresi kuadrat terkecil dan varians.
        """),
        C(
            """
            d = [2, 4, 4, 4, 5, 5, 7, 9]
            m = sum(d) / len(d)
            print(round(sum(x - m for x in d), 10))
            print(sum(2 * x + 3 for x in d) / len(d))
            """,
            """
            0.0
            13.0
            """,
            """
            Jumlah selisih dari rata-rata adalah nol dan rata-rata dari dua kali nilai ditambah tiga sama dengan dua kali rata-rata ditambah tiga.
            """,
            filename="sifat_rata_rata.py",
        ),
        T("""
        ## Rata-rata berbobot

        Ketika nilai tidak sama pentingnya, kita memakai **rata-rata berbobot**: `jumlah (bobot * nilai) / jumlah bobot`. Contoh nilai mata kuliah dengan bobot SKS: nilai 80, 90, 70 dengan SKS 2, 3, 1 menghasilkan `(160 + 270 + 70) / 6`, sekitar 83,33. Mata kuliah dengan SKS lebih besar berpengaruh lebih besar.

        Rata-rata berbobot muncul di mana-mana: indeks harga konsumen, rata-rata kelas dengan jumlah siswa berbeda, dan rata-rata hasil gabungan beberapa survei. Rata-rata biasa adalah kasus khusus dengan semua bobot sama.
        """),
        C(
            """
            nilai = [80, 90, 70]
            bobot = [2, 3, 1]
            print(round(sum(n * b for n, b in zip(nilai, bobot)) / sum(bobot), 4))
            """,
            """
            83.3333
            """,
            """
            Bobot SKS membuat nilai tiga SKS lebih berpengaruh daripada nilai satu SKS.
            """,
            filename="rata_berbobot.py",
        ),
        T("""
        ## Menggabungkan kelompok

        Kesalahan klasik adalah merata-ratakan rata-rata kelompok tanpa memperhatikan ukuran kelompok. Bila kelas A berisi sepuluh siswa berrata-rata 50 dan kelas B berisi sembilan puluh siswa berrata-rata 70, rata-rata gabungan bukan 60, melainkan `(10 * 50 + 90 * 70) / 100 = 68`. Rata-rata gabungan adalah rata-rata berbobot dengan bobot ukuran kelompok.

        Kesalahan serupa memunculkan paradoks Simpson dan banyak laporan menyesatkan. Selalu simpan ukuran kelompok bersama rata-ratanya agar penggabungan dapat dilakukan dengan benar.
        """),
        C(
            """
            kelompok = [(10, 50), (90, 70)]
            gabungan = sum(n * m for n, m in kelompok) / sum(n for n, m in kelompok)
            naif = sum(m for n, m in kelompok) / len(kelompok)
            print(gabungan, naif)
            """,
            """
            68.0 60.0
            """,
            """
            Rata-rata gabungan berbobot ukuran adalah enam puluh delapan, jauh dari rata-rata naif enam puluh.
            """,
            filename="gabung_rata.py",
        ),
        T("""
        ## Sensitivitas terhadap pencilan

        Karena setiap nilai berkontribusi penuh, satu nilai ekstrem dapat menarik rata-rata jauh. Gaji lima orang sekitar 5 sampai 7 juta dan satu orang berpenghasilan 100 juta menghasilkan rata-rata 21,5 juta, angka yang tidak mewakili siapa pun. Tanpa nilai ekstrem itu rata-ratanya 5,8 juta.

        Kepekaan ini bukan cacat, melainkan sifat. Rata-rata memang menyampaikan total dibagi rata, yang relevan untuk anggaran. Tetapi untuk menggambarkan kondisi tipikal, ukuran yang tahan pencilan seperti median lebih jujur. Pelajaran berikutnya membahasnya.
        """),
        C(
            """
            g = [5, 6, 5, 7, 6, 100]
            print(sum(g) / len(g), sum(g[:-1]) / 5)
            """,
            """
            21.5 5.8
            """,
            """
            Satu nilai seratus mengangkat rata-rata dari lima koma delapan menjadi dua puluh satu koma lima.
            """,
            filename="sensitif_pencilan.py",
        ),
        T("""
        ## Rata-rata inkremental

        Untuk aliran data besar yang tidak muat di memori, kita bisa memperbarui rata-rata tanpa menyimpan semua nilai: `rata-rata_baru = rata-rata_lama + (x - rata-rata_lama) / n`, dengan `n` banyaknya data sejauh ini. Rumus ini juga lebih stabil secara numerik daripada menjumlahkan semuanya lalu membagi pada data berskala sangat besar.

        Teknik ini dipakai dalam pemantauan sistem dan pelatihan model daring, tempat data datang terus-menerus. Perhatikan bahwa ia memberi bobot sama pada semua data; untuk menekankan data terbaru dipakai rata-rata bergerak eksponensial.
        """),
        C(
            """
            m = 0.0
            hasil = []
            for n, x in enumerate([10, 20, 30, 40], start=1):
                m += (x - m) / n
                hasil.append(m)
            print(hasil)
            """,
            """
            [10.0, 15.0, 20.0, 25.0]
            """,
            """
            Pembaruan inkremental menghasilkan rata-rata berjalan yang sama dengan menjumlahkan lalu membagi.
            """,
            filename="inkremental.py",
        ),
        K(
            "warn",
            """
            Jangan merata-ratakan rata-rata kelompok tanpa bobot ukuran kelompok. Simpan ukuran kelompok bersama rata-ratanya.
            """,
            title="Rata-rata dari rata-rata",
        ),
        E(
            "A5-02-1-ex1",
            "mudah",
            """
            Tulis fungsi `rata_rata(data)` yang mengembalikan rata-rata aritmetika dibulatkan 4 desimal, dan `None` untuk list kosong.
            """,
            """
            def rata_rata(data):
                # TODO: implementasikan
                pass
            """,
            """
            assert rata_rata([2, 4, 4, 4, 5, 5, 7, 9]) == 5.0
            assert rata_rata([1, 2]) == 1.5
            assert rata_rata([7]) == 7.0
            assert rata_rata([]) is None
            assert rata_rata([1, 2, 2]) == 1.6667
            """,
            "Bagi jumlah dengan banyak data dan tangani list kosong.",
            """
            def rata_rata(data):
                if not data:
                    return None
                return round(sum(data) / len(data), 4)
            """,
        ),
        E(
            "A5-02-1-ex2",
            "sedang",
            """
            Tulis fungsi `rata_rata_berbobot(nilai, bobot)` yang mengembalikan rata-rata berbobot dibulatkan 4 desimal.
            """,
            """
            def rata_rata_berbobot(nilai, bobot):
                # TODO: implementasikan
                pass
            """,
            """
            assert rata_rata_berbobot([80, 90, 70], [2, 3, 1]) == 83.3333
            assert rata_rata_berbobot([1, 2, 3], [1, 1, 1]) == 2.0
            assert rata_rata_berbobot([10], [5]) == 10.0
            assert rata_rata_berbobot([1, 3], [0, 1]) == 3.0
            """,
            "Jumlahkan bobot kali nilai lalu bagi dengan jumlah bobot.",
            """
            def rata_rata_berbobot(nilai, bobot):
                return round(sum(n * b for n, b in zip(nilai, bobot)) / sum(bobot), 4)
            """,
        ),
        E(
            "A5-02-1-ex3",
            "sedang",
            """
            Tulis fungsi `gabung_rata(kelompok)` yang menerima list tuple `(n, rata_rata)` dan mengembalikan rata-rata gabungan semua pengamatan dibulatkan 4 desimal.
            """,
            """
            def gabung_rata(kelompok):
                # TODO: implementasikan
                pass
            """,
            """
            assert gabung_rata([(10, 50), (90, 70)]) == 68.0
            assert gabung_rata([(1, 5)]) == 5.0
            assert gabung_rata([(2, 10), (2, 20)]) == 15.0
            assert gabung_rata([(3, 1), (1, 5)]) == 2.0
            """,
            "Bobotkan tiap rata-rata dengan ukuran kelompoknya.",
            """
            def gabung_rata(kelompok):
                total = sum(n for n, m in kelompok)
                return round(sum(n * m for n, m in kelompok) / total, 4)
            """,
        ),
        E(
            "A5-02-1-ex4",
            "menantang",
            """
            Tulis fungsi `rata_berjalan_inkremental(stream)` yang mengembalikan list rata-rata berjalan memakai pembaruan `m = m + (x - m) / n` tanpa menyimpan jumlah total, dibulatkan 4 desimal.
            """,
            """
            def rata_berjalan_inkremental(stream):
                # TODO: implementasikan
                pass
            """,
            """
            assert rata_berjalan_inkremental([10, 20, 30, 40]) == [10.0, 15.0, 20.0, 25.0]
            assert rata_berjalan_inkremental([5]) == [5.0]
            assert rata_berjalan_inkremental([]) == []
            assert rata_berjalan_inkremental([1, 0, 1, 0]) == [1.0, 0.5, 0.6667, 0.5]
            """,
            "Perbarui rata-rata dengan selisih nilai baru dibagi banyak data sejauh ini.",
            """
            def rata_berjalan_inkremental(stream):
                m = 0.0
                hasil = []
                for n, x in enumerate(stream, start=1):
                    m += (x - m) / n
                    hasil.append(round(m, 4))
                return hasil
            """,
        ),
    ],
    [
        M("Merata-ratakan rata-rata kelompok tanpa bobot ukuran.", "Gunakan rata-rata berbobot ukuran kelompok."),
        M("Menghitung rata-rata data nominal.", "Pakai modus dan frekuensi."),
        M("Memakai rata-rata untuk data dengan pencilan besar tanpa memeriksa.", "Bandingkan dengan median."),
    ],
    [
        Q("Rata-rata aritmetika adalah?", ["Jumlah / n", "Nilai tengah", "Nilai terbanyak", "Maks - min"], 0, "Jumlah dibagi banyak data.", hint="Rata."),
        Q("Jumlah selisih dari rata-rata?", ["Nol", "Satu", "n", "Tak tentu"], 0, "Titik keseimbangan.", hint="Seimbang."),
        Q("Rata-rata gabungan kelompok memakai?", ["Rata-rata biasa", "Bobot ukuran kelompok", "Median", "Modus"], 1, "Berbobot.", hint="Ukuran."),
        Q("Rata-rata sensitif terhadap?", ["Pencilan", "Urutan", "Satuan", "Jumlah kolom"], 0, "Tiap nilai berkontribusi penuh.", hint="Ekstrem."),
        Q("Rata-rata linear berarti mean(aX+b)?", ["a mean + b", "mean + b", "a mean", "mean^a"], 0, "Transformasi linear.", hint="Skala dan geser."),
    ],
    [
        "Rata-rata adalah titik keseimbangan data interval dan rasio.",
        "Rata-rata gabungan harus berbobot ukuran kelompok.",
        "Satu pencilan dapat menggeser rata-rata jauh.",
        "Pembaruan inkremental menghitung rata-rata tanpa menyimpan semua data.",
    ],
    [],
)

l2 = lesson(
    "A5-02-2",
    "Median, modus, dan rata-rata terpangkas",
    35,
    [
        "Menghitung median dan menjelaskan ketahanannya terhadap pencilan",
        "Menghitung modus dan multimodus",
        "Membandingkan rata-rata, median, dan modus pada distribusi miring",
        "Menghitung rata-rata terpangkas dan kuantil",
    ],
    [
        T("""
        ## Median: nilai tengah

        **Median** adalah nilai yang membagi data terurut menjadi dua bagian sama banyak. Untuk banyak data ganjil, median adalah elemen tengah. Untuk genap, median adalah rata-rata dua elemen tengah. Karena hanya bergantung pada urutan, median tidak terpengaruh seberapa jauh nilai ekstrem berada.

        Karena itu median disebut **kokoh** atau robust. Data dengan satu nilai raksasa tetap memiliki median yang hampir sama, sedangkan rata-ratanya bergeser jauh. Median bermakna untuk data ordinal ke atas, sehingga lebih luas penggunaannya daripada rata-rata.
        """),
        C(
            """
            def median(d):
                s = sorted(d)
                n = len(s)
                if n % 2:
                    return s[n // 2]
                return (s[n // 2 - 1] + s[n // 2]) / 2

            print(median([3, 1, 2, 5, 4]), median([4, 1, 3, 2]))
            """,
            """
            3 2.5
            """,
            """
            Data ganjil memberi elemen tengah tiga, sedangkan data genap memberi rata-rata dua elemen tengah yaitu dua koma lima.
            """,
            filename="median.py",
        ),
        T("""
        ## Median pada data bergaji

        Kembali ke contoh gaji lima orang sekitar 5 sampai 7 juta dan satu orang 100 juta. Data terurut adalah 5, 5, 6, 6, 7, 100, sehingga median adalah rata-rata dua elemen tengah, yaitu enam. Median menggambarkan gaji tipikal dengan jujur, sementara rata-rata 21,5 menyesatkan.

        Inilah mengapa laporan pendapatan, harga rumah, dan waktu respons hampir selalu memakai median. Distribusi ini miring ke kanan, dengan ekor panjang nilai besar yang menarik rata-rata ke atas.
        """),
        C(
            """
            import statistics

            g = [5, 6, 5, 7, 6, 100]
            print(statistics.median(g), statistics.mean(g))
            """,
            """
            6.0 21.5
            """,
            """
            Median enam mewakili gaji tipikal, sedangkan rata-rata dua puluh satu koma lima ditarik oleh satu nilai besar.
            """,
            filename="median_gaji.py",
        ),
        T("""
        ## Modus

        **Modus** adalah nilai yang paling sering muncul. Ia satu-satunya ukuran pemusatan yang bermakna untuk data nominal, misalnya golongan darah terbanyak. Satu dataset bisa memiliki beberapa modus bila beberapa nilai sama-sama paling sering, disebut multimodus, dan bisa juga tidak berguna bila semua nilai unik.

        Untuk data kontinu, modus sendiri jarang bermakna karena nilai persisnya hampir tidak pernah berulang. Kita mengelompokkan data ke dalam kotak dan mencari kotak tersibuk, atau memakai puncak estimasi kepadatan kernel. Distribusi dengan dua puncak jelas menandakan dua subpopulasi yang bercampur.
        """),
        T("""
        ## Tiga ukuran pada distribusi miring

        Pada distribusi simetris ketiga ukuran berimpit. Pada distribusi miring ke kanan, urutannya biasanya modus lebih kecil dari median lebih kecil dari rata-rata. Ekor kanan menarik rata-rata ke atas, median setengah, dan modus tetap di puncak. Pada miring ke kiri urutannya terbalik.

        Perbedaan ketiganya adalah informasi: selisih besar antara rata-rata dan median menandakan kemiringan. Melaporkan ketiganya sekaligus memberi gambaran bentuk distribusi tanpa grafik.
        """),
        C(
            """
            import statistics

            d = [1, 1, 2, 2, 3, 4, 6, 9, 15, 30]
            print(statistics.mean(d), statistics.median(d), statistics.multimode(d))
            """,
            """
            7.3 3.5 [1, 2]
            """,
            """
            Rata-rata tujuh koma tiga jauh di atas median tiga koma lima, menandakan kemiringan ke kanan, dan ada dua modus yaitu satu dan dua.
            """,
            filename="tiga_ukuran.py",
        ),
        T("""
        ## Kokohnya median

        Seberapa kokoh median? Ganti nilai terbesar tiga puluh menjadi tiga ribu. Rata-rata melonjak dari 7,3 menjadi 304,3, tetapi median tetap 3,5. Median baru berubah bila lebih dari separuh data terkontaminasi, disebut titik patah lima puluh persen, sedangkan rata-rata bisa dirusak oleh satu nilai saja.

        Kekokohan ini penting pada data nyata yang jarang bersih. Tetapi median kurang efisien pada data normal bersih: ia memiliki varians sampling lebih besar daripada rata-rata, sehingga untuk data yang benar-benar simetris dan bersih rata-rata lebih presisi.
        """),
        C(
            """
            import statistics

            d = [1, 1, 2, 2, 3, 4, 6, 9, 15, 3000]
            print(statistics.median(d), statistics.mean(d))
            """,
            """
            3.5 304.3
            """,
            """
            Mengganti nilai terbesar dengan tiga ribu tidak mengubah median sama sekali, tetapi melonjakkan rata-rata.
            """,
            filename="median_kokoh.py",
        ),
        T("""
        ## Rata-rata terpangkas

        **Rata-rata terpangkas** adalah kompromi: buang sebagian kecil nilai terkecil dan terbesar, misalnya sepuluh persen di tiap ujung, lalu hitung rata-rata sisanya. Ia lebih kokoh daripada rata-rata biasa tetapi memanfaatkan lebih banyak data daripada median. Penilaian olahraga seperti senam sering memakainya dengan membuang nilai tertinggi dan terendah juri.

        Pemangkasan dua puluh persen sering dipakai sebagai default praktis. Dengan pangkas lima puluh persen di tiap ujung, rata-rata terpangkas menjadi median.
        """),
        C(
            """
            def terpangkas(data, p):
                k = int(p * len(data))
                s = sorted(data)[k:len(data) - k]
                return sum(s) / len(s)

            d = [1, 1, 2, 2, 3, 4, 6, 9, 15, 30]
            print(terpangkas(d, 0.1))
            """,
            """
            5.25
            """,
            """
            Membuang satu nilai terkecil dan satu terbesar menghasilkan rata-rata lima koma dua lima, di antara median dan rata-rata biasa.
            """,
            filename="terpangkas.py",
        ),
        K(
            "tip",
            """
            Laporkan rata-rata dan median bersama. Bila keduanya jauh berbeda, distribusi miring atau ada pencilan, dan median biasanya lebih mewakili kondisi tipikal.
            """,
            title="Dua angka lebih jujur",
        ),
        T("""
        ## Memilih ukuran dalam praktik

        Tidak ada ukuran yang selalu terbaik. Untuk anggaran dan total, rata-rata tepat karena ia mempertahankan jumlah. Untuk kondisi tipikal pada data miring seperti gaji, harga rumah, dan waktu muat halaman, median lebih jujur. Untuk kategori seperti merek favorit, hanya modus yang masuk akal. Bila ragu, hitung ketiganya lalu bandingkan.

        Kebiasaan baik lain adalah menyebut ukuran yang dipakai secara eksplisit di laporan. Kalimat rata-rata gaji dua puluh satu juta dan median enam juta menceritakan dua kisah berbeda, dan pembaca berhak tahu kisah mana yang sedang diceritakan kepadanya.
        """),
        T("""
        ## Kuantil sebagai perluasan median

        Median adalah kuantil ke-0,5. Kuantil lain seperti kuartil dan persentil membagi data pada proporsi berbeda: kuartil pertama memisahkan seperempat data terkecil, dan persentil sembilan puluh lima memisahkan lima persen terbesar. Karena kuantil juga bergantung pada urutan, ia sama kokohnya dengan median.

        Bila posisi kuantil jatuh di antara dua elemen, kita menginterpolasi linear di antara keduanya. Beberapa pustaka memakai aturan interpolasi berbeda, sehingga hasil kecil bisa tidak sama antar alat. Pelajaran berikutnya membahas kuantil lebih dalam sebagai ukuran sebaran.
        """),
        E(
            "A5-02-2-ex1",
            "mudah",
            """
            Tulis fungsi `median(data)` yang mengembalikan median. Untuk list kosong kembalikan `None`.
            """,
            """
            def median(data):
                # TODO: implementasikan
                pass
            """,
            """
            assert median([3, 1, 2, 5, 4]) == 3
            assert median([4, 1, 3, 2]) == 2.5
            assert median([7]) == 7
            assert median([]) is None
            assert median([5, 5, 6, 6, 7, 100]) == 6.0
            """,
            "Urutkan lalu ambil elemen tengah atau rata-rata dua elemen tengah.",
            """
            def median(data):
                if not data:
                    return None
                s = sorted(data)
                n = len(s)
                if n % 2:
                    return s[n // 2]
                return (s[n // 2 - 1] + s[n // 2]) / 2
            """,
        ),
        E(
            "A5-02-2-ex2",
            "sedang",
            """
            Tulis fungsi `rata_rata_terpangkas(data, p)` yang membuang `int(p * n)` nilai di tiap ujung data terurut lalu mengembalikan rata-rata sisanya dibulatkan 4 desimal.
            """,
            """
            def rata_rata_terpangkas(data, p):
                # TODO: implementasikan
                pass
            """,
            """
            d = [1, 1, 2, 2, 3, 4, 6, 9, 15, 30]
            assert rata_rata_terpangkas(d, 0.1) == 5.25
            assert rata_rata_terpangkas(d, 0) == 7.3
            assert rata_rata_terpangkas([1, 2, 3], 0.5) == 2.0
            assert rata_rata_terpangkas([5], 0.2) == 5.0
            """,
            "Hitung k dari p dan n, potong k elemen di tiap ujung data terurut, lalu rata-ratakan.",
            """
            def rata_rata_terpangkas(data, p):
                k = int(p * len(data))
                s = sorted(data)[k:len(data) - k]
                return round(sum(s) / len(s), 4)
            """,
        ),
        E(
            "A5-02-2-ex3",
            "sedang",
            """
            Tulis fungsi `kuantil(data, q)` yang mengembalikan kuantil `q` (0 sampai 1) dengan interpolasi linear: posisi `(n - 1) * q` pada data terurut, interpolasikan antara dua elemen terdekat. Bulatkan 4 desimal.
            """,
            """
            def kuantil(data, q):
                # TODO: implementasikan
                pass
            """,
            """
            assert kuantil([1, 2, 3, 4, 5], 0.5) == 3.0
            assert kuantil([1, 2, 3, 4, 5], 0.25) == 2.0
            assert kuantil([1, 2, 3, 4, 5], 0.1) == 1.4
            assert kuantil([10, 20], 0.5) == 15.0
            assert kuantil([7], 0.3) == 7.0
            """,
            "Hitung posisi pecahan lalu interpolasikan antara elemen bawah dan atas.",
            """
            def kuantil(data, q):
                s = sorted(data)
                p = (len(s) - 1) * q
                lo = int(p)
                hi = min(lo + 1, len(s) - 1)
                return round(s[lo] + (s[hi] - s[lo]) * (p - lo), 4)
            """,
        ),
        E(
            "A5-02-2-ex4",
            "menantang",
            """
            Tulis fungsi `ukuran_disarankan(data)` yang mengembalikan `'median'` bila `abs(rata-rata - median) > 0.1 * abs(median)` dan `'rata-rata'` bila tidak. Hitung median sendiri dari data terurut.
            """,
            """
            def ukuran_disarankan(data):
                # TODO: implementasikan
                pass
            """,
            """
            assert ukuran_disarankan([1, 1, 2, 2, 3, 4, 6, 9, 15, 30]) == 'median'
            assert ukuran_disarankan([10, 11, 12, 13, 14]) == 'rata-rata'
            assert ukuran_disarankan([5, 5, 6, 6, 7, 100]) == 'median'
            assert ukuran_disarankan([1, 2, 3, 4, 5]) == 'rata-rata'
            """,
            "Bandingkan selisih rata-rata dan median dengan sepuluh persen median.",
            """
            def ukuran_disarankan(data):
                s = sorted(data)
                n = len(s)
                med = s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2
                rata = sum(s) / n
                return 'median' if abs(rata - med) > 0.1 * abs(med) else 'rata-rata'
            """,
        ),
    ],
    [
        M("Memakai rata-rata untuk data berekor panjang tanpa melihat median.", "Laporkan median bersama rata-rata."),
        M("Mengira satu dataset hanya punya satu modus.", "Bisa multimodus atau tak ada."),
        M("Memakai median pada data nominal.", "Median butuh urutan, pakai modus."),
    ],
    [
        Q("Median kokoh terhadap?", ["Pencilan", "Urutan", "Skala", "Ukuran"], 0, "Hanya bergantung pada urutan.", hint="Ekstrem."),
        Q("Pada distribusi miring kanan?", ["Rata-rata di bawah median", "Rata-rata di atas median", "Sama", "Modus terbesar"], 1, "Ekor menarik rata-rata.", hint="Ekor."),
        Q("Modus bermakna untuk?", ["Semua skala termasuk nominal", "Hanya rasio", "Hanya interval", "Tidak ada"], 0, "Nilai terbanyak.", hint="Kategori."),
        Q("Rata-rata terpangkas?", ["Membuang nilai ekstrem lalu merata-ratakan", "Membuang median", "Mengalikan", "Menjumlah"], 0, "Kompromi.", hint="Pangkas."),
        Q("Median data genap?", ["Elemen tengah", "Rata-rata dua elemen tengah", "Rata-rata semua", "Maks"], 1, "Dua tengah.", hint="Genap."),
    ],
    [
        "Median kokoh terhadap pencilan dan bermakna untuk data ordinal.",
        "Modus satu-satunya pusat untuk nominal.",
        "Selisih rata-rata dan median menandakan kemiringan.",
        "Rata-rata terpangkas adalah kompromi kokoh dan efisien.",
    ],
    [],
)

l3 = lesson(
    "A5-02-3",
    "Rata-rata geometrik, harmonik, dan bergerak",
    35,
    [
        "Menghitung rata-rata geometrik untuk faktor pertumbuhan",
        "Menghitung rata-rata harmonik untuk rasio dan laju",
        "Menghitung rata-rata bergerak sederhana dan eksponensial",
        "Menghitung laju pertumbuhan tahunan majemuk",
    ],
    [
        T("""
        ## Tidak semua rata-rata aritmetika

        Rata-rata aritmetika cocok untuk besaran yang dijumlahkan. Tetapi untuk besaran yang dikalikan, seperti pertumbuhan, atau besaran berupa laju dan rasio, rata-rata aritmetika memberi jawaban yang salah. Ada dua rata-rata lain yang cocok untuk kasus itu: geometrik dan harmonik.

        Ketiganya sebenarnya satu keluarga, rata-rata pangkat, yang berbeda dalam transformasi sebelum dirata-ratakan. Memilih yang tepat adalah soal menentukan besaran mana yang seharusnya bersifat aditif dalam masalahmu.
        """),
        T("""
        ## Rata-rata geometrik

        **Rata-rata geometrik** dari `n` bilangan positif adalah akar pangkat `n` dari hasil kalinya. Ekuivalen, ia adalah eksponen dari rata-rata logaritma. Ia tepat untuk faktor pertumbuhan: bila investasi tumbuh 10 persen, 20 persen, lalu turun 10 persen, faktornya 1,1, 1,2, dan 0,9. Faktor tahunan tunggal yang menghasilkan total pertumbuhan sama adalah rata-rata geometrik, sekitar 1,0591, bukan rata-rata aritmetika 1,0667.

        Rata-rata aritmetika selalu melebihi geometrik, sehingga memakainya untuk pertumbuhan majemuk membesar-besarkan hasil jangka panjang.
        """),
        C(
            """
            import math

            g = [1.1, 1.2, 0.9]
            gm = math.exp(sum(math.log(x) for x in g) / len(g))
            print(round(gm, 4), round(sum(g) / len(g), 4))
            """,
            """
            1.0591 1.0667
            """,
            """
            Faktor pertumbuhan majemuk rata-rata adalah satu koma nol lima sembilan satu, lebih kecil dari rata-rata aritmetika.
            """,
            filename="rata_geometrik.py",
        ),
        T("""
        ## Rata-rata harmonik

        **Rata-rata harmonik** adalah kebalikan dari rata-rata kebalikan: `n / jumlah(1/x)`. Ia tepat untuk laju ketika jarak atau pekerjaan yang ditempuh sama. Bila kamu menempuh jarak sama dengan kecepatan 60 lalu 40 kilometer per jam, kecepatan rata-rata keseluruhan bukan 50, melainkan 48, harmonik dari keduanya. Alasannya, kamu menghabiskan lebih lama waktu pada kecepatan lebih rendah.

        Rata-rata harmonik juga muncul pada F1 score, yang merupakan harmonik presisi dan recall. Karena ia condong ke nilai kecil, skor tinggi hanya diperoleh bila kedua komponen sama-sama tinggi.
        """),
        C(
            """
            print(round(2 / (1 / 60 + 1 / 40), 4))
            """,
            """
            48.0
            """,
            """
            Kecepatan rata-rata untuk jarak sama pada enam puluh dan empat puluh adalah empat puluh delapan.
            """,
            filename="rata_harmonik.py",
        ),
        T("""
        ## Urutan tiga rata-rata

        Untuk bilangan positif, selalu berlaku `harmonik <= geometrik <= aritmetika`, dengan kesamaan hanya bila semua bilangan sama. Untuk data satu, empat, dan enam belas, aritmetika tujuh, geometrik empat, dan harmonik sekitar 2,29. Semakin besar sebaran, semakin jauh jarak antar ketiganya.

        Selisih ini sendiri berguna sebagai ukuran sebaran relatif. Memahami urutan ini membantu menyadari mengapa memakai rata-rata yang salah secara sistematis membesar-besarkan atau mengecilkan hasil.
        """),
        C(
            """
            import math

            d = [1, 4, 16]
            am = sum(d) / 3
            gm = math.exp(sum(math.log(x) for x in d) / 3)
            hm = 3 / sum(1 / x for x in d)
            print(am, round(gm, 4), round(hm, 4))
            """,
            """
            7.0 4.0 2.2857
            """,
            """
            Rata-rata aritmetika tujuh, geometrik empat, dan harmonik sekitar dua koma dua sembilan menunjukkan urutan yang selalu berlaku.
            """,
            filename="urutan_rata.py",
        ),
        T("""
        ## Rata-rata bergerak

        Untuk data deret waktu yang berfluktuasi, kita meratakan derau dengan **rata-rata bergerak**: rata-rata `w` nilai terakhir pada tiap titik. Jendela lebih lebar memberi kurva lebih mulus tetapi tertinggal lebih lama menanggapi perubahan nyata. Pada awal deret, belum ada cukup data sehingga hasilnya biasanya dimulai pada titik ke-`w`.

        Rata-rata bergerak eksponensial memberi bobot lebih pada data baru dengan rumus `ema = alpha * x + (1 - alpha) * ema_sebelumnya`. Ia tidak memerlukan jendela tetap dan memperbarui hanya dengan satu angka, sehingga sering dipakai pada pemantauan dan optimizer momentum.
        """),
        C(
            """
            x = [1, 2, 3, 4, 5, 6]
            w = 3
            print([sum(x[i:i + w]) / w for i in range(len(x) - w + 1)])
            ema = [10.0]
            for v in [20, 30]:
                ema.append(0.5 * v + 0.5 * ema[-1])
            print(ema)
            """,
            """
            [2.0, 3.0, 4.0, 5.0]
            [10.0, 15.0, 22.5]
            """,
            """
            Jendela tiga menghasilkan empat titik mulus, dan rata-rata eksponensial bergerak menuju nilai baru secara bertahap.
            """,
            filename="rata_bergerak.py",
        ),
        T("""
        ## Laju pertumbuhan majemuk

        Laju pertumbuhan tahunan majemuk atau CAGR menyatakan pertumbuhan rata-rata per periode: `(akhir / awal)^(1/tahun) - 1`. Ia adalah rata-rata geometrik faktor pertumbuhan dikurangi satu. Bila nilai tumbuh dari 100 menjadi 150 dalam tiga tahun, CAGR sekitar 14,47 persen, bukan 16,67 persen yang didapat dari membagi total pertumbuhan 50 persen dengan tiga.

        CAGR menyembunyikan fluktuasi di tengah periode, jadi dua jalur yang sangat berbeda bisa memiliki CAGR sama. Laporkan jalur lengkap bila volatilitas penting.
        """),
        C(
            """
            print(round(1.5 ** (1 / 3) - 1, 4))
            """,
            """
            0.1447
            """,
            """
            Pertumbuhan lima puluh persen dalam tiga tahun setara dengan sekitar empat belas koma empat tujuh persen per tahun.
            """,
            filename="cagr.py",
        ),
        K(
            "warn",
            """
            Jangan merata-ratakan persentase pertumbuhan secara aritmetika. Pakai rata-rata geometrik faktor pertumbuhan, yaitu satu ditambah laju.
            """,
            title="Pertumbuhan berlipat",
        ),
        T("""
        ## Memilih rata-rata yang tepat

        Pertanyaan kuncinya adalah besaran mana yang seharusnya aditif. Bila total yang bermakna, pakai aritmetika. Bila hasil kali yang bermakna, seperti pertumbuhan berlipat, pakai geometrik. Bila yang dijumlahkan adalah waktu atau biaya per satuan, seperti kecepatan dengan jarak sama, pakai harmonik. Salah memilih menghasilkan angka yang tampak wajar tetapi keliru secara sistematis.

        Satu cara memeriksa adalah menghitung ulang total dari rata-rata itu. Bila memakai faktor geometrik tahunan menghasilkan nilai akhir yang sama dengan jalur nyata, pilihanmu tepat. Bila tidak, ada yang salah dalam asumsi tentang apa yang dijumlahkan.
        """),
        T("""
        ## Rata-rata bergerak dalam praktik

        Rata-rata bergerak dipakai di keuangan, epidemiologi, dan pemantauan sistem untuk melihat tren di balik derau harian. Kasus yang sering dijumpai adalah rata-rata tujuh hari untuk kasus harian, yang meredam pola akhir pekan. Pilih lebar jendela sesuai siklus alami data agar pola berulang hilang dari kurva.

        Ingat bahwa rata-rata bergerak mewarisi kelemahan rata-rata biasa: satu pencilan menodai semua jendela yang memuatnya. Untuk data berpencilan, median bergerak lebih kokoh meski sedikit lebih mahal dihitung.
        """),
        E(
            "A5-02-3-ex1",
            "mudah",
            """
            Tulis fungsi `rata_geometrik(data)` yang mengembalikan rata-rata geometrik dibulatkan 4 desimal. Bila ada nilai tidak positif kembalikan `None`.
            """,
            """
            import math

            def rata_geometrik(data):
                # TODO: implementasikan
                pass
            """,
            """
            assert rata_geometrik([1, 4, 16]) == 4.0
            assert rata_geometrik([2, 8]) == 4.0
            assert rata_geometrik([5]) == 5.0
            assert rata_geometrik([1.1, 1.2, 0.9]) == 1.0591
            assert rata_geometrik([0, 1]) is None
            """,
            "Ambil eksponen dari rata-rata logaritma setelah memeriksa semua nilai positif.",
            """
            import math

            def rata_geometrik(data):
                if any(x <= 0 for x in data):
                    return None
                return round(math.exp(sum(math.log(x) for x in data) / len(data)), 4)
            """,
        ),
        E(
            "A5-02-3-ex2",
            "sedang",
            """
            Tulis fungsi `rata_harmonik(data)` yang mengembalikan `n / jumlah(1/x)` dibulatkan 4 desimal.
            """,
            """
            def rata_harmonik(data):
                # TODO: implementasikan
                pass
            """,
            """
            assert rata_harmonik([60, 40]) == 48.0
            assert rata_harmonik([1, 4, 16]) == 2.2857
            assert rata_harmonik([2, 2, 2]) == 2.0
            assert rata_harmonik([5]) == 5.0
            """,
            "Bagi banyak data dengan jumlah kebalikan tiap nilai.",
            """
            def rata_harmonik(data):
                return round(len(data) / sum(1 / x for x in data), 4)
            """,
        ),
        E(
            "A5-02-3-ex3",
            "sedang",
            """
            Tulis fungsi `rata_bergerak(data, w)` yang mengembalikan list rata-rata dari tiap jendela `w` elemen berurutan, dibulatkan 4 desimal. Bila `w` melebihi panjang data kembalikan list kosong.
            """,
            """
            def rata_bergerak(data, w):
                # TODO: implementasikan
                pass
            """,
            """
            assert rata_bergerak([1, 2, 3, 4, 5, 6], 3) == [2.0, 3.0, 4.0, 5.0]
            assert rata_bergerak([1, 2, 3], 1) == [1.0, 2.0, 3.0]
            assert rata_bergerak([1, 2], 5) == []
            assert rata_bergerak([10, 20], 2) == [15.0]
            """,
            "Geser jendela sepanjang data dan rata-ratakan tiap jendela.",
            """
            def rata_bergerak(data, w):
                return [round(sum(data[i:i + w]) / w, 4) for i in range(len(data) - w + 1)]
            """,
        ),
        E(
            "A5-02-3-ex4",
            "menantang",
            """
            Tulis fungsi `cagr(awal, akhir, tahun)` yang mengembalikan `(akhir / awal) ** (1 / tahun) - 1` dibulatkan 4 desimal. Hindari `-0.0`.
            """,
            """
            def cagr(awal, akhir, tahun):
                # TODO: implementasikan
                pass
            """,
            """
            assert cagr(100, 150, 3) == 0.1447
            assert cagr(100, 100, 5) == 0.0
            assert cagr(100, 200, 1) == 1.0
            assert cagr(200, 100, 2) == -0.2929
            """,
            "Hitung rasio akhir terhadap awal, pangkatkan satu per tahun, lalu kurangi satu.",
            """
            def cagr(awal, akhir, tahun):
                return round((akhir / awal) ** (1 / tahun) - 1, 4) + 0.0
            """,
        ),
    ],
    [
        M("Merata-ratakan persentase pertumbuhan secara aritmetika.", "Pakai rata-rata geometrik faktor pertumbuhan."),
        M("Merata-ratakan kecepatan dengan aritmetika untuk jarak sama.", "Pakai rata-rata harmonik."),
        M("Memakai jendela bergerak lebar tanpa menyadari ketertinggalan.", "Pilih lebar sesuai kecepatan perubahan."),
    ],
    [
        Q("Rata-rata geometrik cocok untuk?", ["Faktor pertumbuhan", "Nominal", "Jumlah", "Median"], 0, "Besaran yang dikalikan.", hint="Majemuk."),
        Q("Rata-rata harmonik cocok untuk?", ["Laju dengan jarak sama", "Pertumbuhan", "Nominal", "Jumlah"], 0, "Kebalikan.", hint="Kecepatan."),
        Q("Urutan benar?", ["H <= G <= A", "A <= G <= H", "G <= A <= H", "H >= A"], 0, "Selalu untuk positif.", hint="Harmonik terkecil."),
        Q("Jendela lebar pada rata-rata bergerak?", ["Lebih mulus dan lebih tertinggal", "Lebih kasar", "Tanpa efek", "Lebih cepat"], 0, "Trade-off.", hint="Mulus."),
        Q("CAGR memakai?", ["Rata-rata geometrik", "Aritmetika", "Harmonik", "Median"], 0, "Pertumbuhan majemuk.", hint="Per tahun."),
    ],
    [
        "Geometrik untuk faktor pertumbuhan, harmonik untuk laju.",
        "Harmonik <= geometrik <= aritmetika untuk bilangan positif.",
        "Rata-rata bergerak meratakan derau dengan trade-off ketertinggalan.",
        "CAGR adalah rata-rata geometrik pertumbuhan dikurangi satu.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perhitungan yang cukup jelas dalam teks.", "brief": []}

write_module(
    "A5",
    2,
    "Ukuran pemusatan",
    105,
    [
        "Menghitung dan memilih rata-rata, median, dan modus",
        "Memakai rata-rata geometrik dan harmonik dengan tepat",
        "Memakai rata-rata bergerak dan CAGR",
    ],
    [l1, l2, l3],
    video,
    REF,
)
