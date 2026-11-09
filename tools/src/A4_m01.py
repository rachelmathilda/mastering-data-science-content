import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

l1 = lesson(
    "A4-01-1",
    "Ruang sampel dan kejadian",
    35,
    [
        "Mendefinisikan percobaan acak, hasil, ruang sampel, dan kejadian",
        "Menyusun ruang sampel dengan himpunan dan itertools",
        "Menghitung peluang klasik dengan hasil sama mungkin",
        "Memakai operasi himpunan untuk menggabungkan kejadian",
    ],
    [
        T("""
        ## Mengapa probabilitas penting

        Data science hampir selalu berurusan dengan ketidakpastian. Pelanggan mana yang akan berhenti berlangganan, apakah hasil uji A/B hanya kebetulan, seberapa yakin model terhadap prediksinya: semuanya pertanyaan probabilistik. Probabilitas adalah bahasa untuk menyatakan ketidakpastian secara tepat, sehingga kita bisa menghitungnya, bukan sekadar merasakannya.

        Modul ini membangun fondasi paling dasar: ruang sampel, kejadian, dan aturan hitung peluang. Kita akan memakai Python untuk mengecek setiap rumus dengan enumerasi langsung, sehingga rumus tidak terasa seperti sihir melainkan ringkasan dari penghitungan yang bisa kamu lihat sendiri.
        """),
        T("""
        ## Percobaan acak dan ruang sampel

        **Percobaan acak** adalah proses dengan hasil yang tidak dapat dipastikan sebelumnya tetapi himpunan kemungkinannya diketahui. Melempar sebuah dadu, melempar koin tiga kali, atau mengambil satu pelanggan secara acak dari basis data adalah contohnya. Setiap hasil yang mungkin disebut **hasil** atau outcome.

        Himpunan semua hasil yang mungkin disebut **ruang sampel**, biasanya ditulis `S`. Untuk satu dadu, `S = {1, 2, 3, 4, 5, 6}`. Untuk dua koin, `S = {HH, HT, TH, TT}`. Langkah pertama setiap soal peluang adalah menuliskan ruang sampel dengan jelas, karena banyak kesalahan berawal dari ruang sampel yang kurang lengkap atau salah.
        """),
        T("""
        ## Kejadian

        **Kejadian** adalah himpunan bagian dari ruang sampel, yaitu kumpulan hasil yang kita pedulikan. Kejadian "dadu menunjukkan bilangan genap" adalah `A = {2, 4, 6}`. Kejadian "jumlah dua dadu sama dengan tujuh" adalah himpunan semua pasangan yang jumlahnya tujuh: `(1,6), (2,5), (3,4), (4,3), (5,2), (6,1)`.

        Kejadian kosong tidak pernah terjadi dan kejadian `S` selalu terjadi. Satu kejadian dikatakan terjadi bila hasil percobaan merupakan anggotanya. Karena kejadian berupa himpunan, kita bisa menggabungkan dan membandingkannya dengan operasi himpunan yang sudah kamu kenal.
        """),
        C(
            """
            from itertools import product

            S = list(product(range(1, 7), repeat=2))
            A = [h for h in S if h[0] + h[1] == 7]
            print(len(S))
            print(len(A))
            print(round(len(A) / len(S), 4))
            """,
            """
            36
            6
            0.1667
            """,
            """
            Dua dadu memiliki 36 hasil sama mungkin dan enam di antaranya berjumlah tujuh, sehingga peluangnya enam per tiga puluh enam.
            """,
            filename="dua_dadu.py",
        ),
        T("""
        ## Peluang klasik

        Bila semua hasil dalam ruang sampel **sama mungkin**, peluang kejadian `A` adalah banyaknya hasil dalam `A` dibagi banyaknya hasil dalam `S`: `P(A) = |A| / |S|`. Inilah definisi klasik. Ia cocok untuk dadu adil, koin adil, dan undian acak, tetapi tidak berlaku bila hasilnya tidak sama mungkin, misalnya dadu yang berat sebelah.

        Dari definisi ini langsung terlihat tiga sifat dasar. Peluang selalu antara nol dan satu. `P(S) = 1` karena pasti ada hasil. `P(kosong) = 0`. Seluruh teori probabilitas modern dibangun dari sifat-sifat sederhana ini yang disebut aksioma Kolmogorov.
        """),
        C(
            """
            from itertools import product

            S = list(product("HT", repeat=3))
            A = [h for h in S if h.count("H") >= 2]
            print(len(S))
            print(len(A))
            print(len(A) / len(S))
            """,
            """
            8
            4
            0.5
            """,
            """
            Tiga lemparan koin memiliki delapan hasil. Empat di antaranya memuat minimal dua kepala sehingga peluangnya setengah.
            """,
            filename="tiga_koin.py",
        ),
        T("""
        ## Operasi himpunan pada kejadian

        Gabungan `A atau B` ditulis `A | B` di Python, berisi hasil yang ada di salah satu atau kedua kejadian. Irisan `A dan B` ditulis `A & B`, berisi hasil yang ada di keduanya. Komplemen `bukan A` adalah `S - A`, semua hasil di luar `A`. Dua kejadian dengan irisan kosong disebut **saling lepas** karena tidak mungkin terjadi bersamaan.

        Dengan set Python, semua ini bisa dikerjakan langsung. Hasilnya mudah diperiksa dan menjadi cara belajar yang baik: tulis kejadian sebagai set, lalu hitung peluang sebagai rasio ukuran set.
        """),
        C(
            """
            S = {1, 2, 3, 4, 5, 6}
            A = {1, 2, 3, 4}
            B = {3, 4, 5, 6}
            print(sorted(A | B))
            print(sorted(A & B))
            print(sorted(S - A))
            """,
            """
            [1, 2, 3, 4, 5, 6]
            [3, 4]
            [5, 6]
            """,
            """
            Gabungan mencakup semua hasil, irisan hanya tiga dan empat, dan komplemen A berisi lima dan enam.
            """,
            filename="operasi_kejadian.py",
        ),
        K(
            "tip",
            """
            Sebelum menghitung peluang, tuliskan ruang sampel dan pastikan hasilnya sama mungkin. Pasangan dua dadu berjumlah 36 hasil, bukan 11 jumlah, karena jumlah tujuh lebih mungkin daripada jumlah dua.
            """,
            title="Ruang sampel dulu",
        ),
        T("""
        ## Jebakan umum

        Kesalahan klasik adalah menganggap semua hasil sama mungkin padahal tidak. Jumlah dua dadu memiliki sebelas nilai dari dua sampai dua belas, tetapi nilainya tidak sama mungkin: jumlah tujuh memiliki enam cara sedangkan jumlah dua hanya satu cara. Selalu enumerasi pada tingkat hasil dasar yang sama mungkin, yaitu pasangan berurutan.

        Jebakan lain adalah mengabaikan urutan. Koin `HT` dan `TH` adalah dua hasil berbeda, sehingga dua koin memiliki empat hasil, bukan tiga. Bila kamu ragu, tulis semua hasilnya dengan kode. Enumerasi kecil adalah alat verifikasi paling andal sebelum memakai rumus.
        """),
        T("""
        ## Peluang sebagai frekuensi jangka panjang

        Selain definisi klasik, ada tafsir frekuensi: peluang adalah proporsi kejadian bila percobaan diulang sangat banyak kali. Peluang `0,5` untuk kepala berarti kira-kira separuh lemparan menghasilkan kepala dalam jangka panjang. Tafsir ini menjadi dasar simulasi yang akan kita pakai di modul Monte Carlo.

        Ada pula tafsir subjektif yang dipakai di statistika Bayesian: peluang sebagai derajat keyakinan. Ketiganya memakai aturan hitung yang sama, sehingga untuk sekarang kita cukup berfokus pada aturan itu dan menguatkannya dengan latihan.
        """),
        E(
            "A4-01-1-ex1",
            "mudah",
            """
            Tulis fungsi `ukuran_ruang_dadu(n)` yang mengembalikan banyaknya hasil pada pelemparan `n` dadu enam sisi.
            """,
            """
            def ukuran_ruang_dadu(n):
                # TODO: implementasikan
                pass
            """,
            """
            assert ukuran_ruang_dadu(1) == 6
            assert ukuran_ruang_dadu(2) == 36
            assert ukuran_ruang_dadu(3) == 216
            assert ukuran_ruang_dadu(0) == 1
            """,
            "Tiap dadu punya enam kemungkinan sehingga total adalah perkalian.",
            """
            def ukuran_ruang_dadu(n):
                return 6 ** n
            """,
        ),
        E(
            "A4-01-1-ex2",
            "sedang",
            """
            Tulis fungsi `peluang_kejadian(S, syarat)` yang menerima koleksi hasil `S` dan fungsi `syarat` yang bernilai True untuk hasil dalam kejadian. Kembalikan peluang klasik dibulatkan 4 desimal.
            """,
            """
            def peluang_kejadian(S, syarat):
                # TODO: implementasikan
                pass
            """,
            """
            S = list(range(1, 7))
            assert peluang_kejadian(S, lambda x: x % 2 == 0) == 0.5
            assert peluang_kejadian(S, lambda x: x > 4) == 0.3333
            assert peluang_kejadian(S, lambda x: x > 6) == 0.0
            assert peluang_kejadian(S, lambda x: x > 0) == 1.0
            """,
            "Hitung hasil yang memenuhi syarat lalu bagi dengan ukuran S.",
            """
            def peluang_kejadian(S, syarat):
                S = list(S)
                return round(sum(1 for h in S if syarat(h)) / len(S), 4)
            """,
        ),
        E(
            "A4-01-1-ex3",
            "sedang",
            """
            Tulis fungsi `peluang_jumlah(k)` yang mengembalikan peluang jumlah dua dadu adil sama dengan `k`, dibulatkan 4 desimal.
            """,
            """
            from itertools import product

            def peluang_jumlah(k):
                # TODO: implementasikan
                pass
            """,
            """
            assert peluang_jumlah(7) == 0.1667
            assert peluang_jumlah(2) == 0.0278
            assert peluang_jumlah(12) == 0.0278
            assert peluang_jumlah(13) == 0.0
            assert peluang_jumlah(8) == 0.1389
            """,
            "Enumerasi 36 pasangan dengan product lalu hitung yang berjumlah k.",
            """
            from itertools import product

            def peluang_jumlah(k):
                S = list(product(range(1, 7), repeat=2))
                return round(sum(1 for a, b in S if a + b == k) / len(S), 4)
            """,
        ),
        E(
            "A4-01-1-ex4",
            "menantang",
            """
            Tulis fungsi `ruang_koin(n)` yang mengembalikan list string semua hasil pelemparan `n` koin dengan huruf `H` dan `T`, terurut alfabetis (H sebelum T). Untuk `n = 0` kembalikan list berisi satu string kosong.
            """,
            """
            from itertools import product

            def ruang_koin(n):
                # TODO: implementasikan
                pass
            """,
            """
            assert ruang_koin(1) == ['H', 'T']
            assert ruang_koin(2) == ['HH', 'HT', 'TH', 'TT']
            assert len(ruang_koin(3)) == 8
            assert ruang_koin(3)[-1] == 'TTT'
            assert ruang_koin(0) == ['']
            """,
            "Gunakan product dengan repeat lalu gabungkan tiap tuple menjadi string.",
            """
            from itertools import product

            def ruang_koin(n):
                return [''.join(h) for h in product('HT', repeat=n)]
            """,
        ),
    ],
    [
        M("Menganggap jumlah dua dadu sebelas hasil sama mungkin.", "Enumerasi 36 pasangan berurutan."),
        M("Menganggap HT dan TH hasil yang sama.", "Urutan membedakan hasil."),
        M("Memakai rumus klasik pada hasil tidak sama mungkin.", "Pastikan hasil sama mungkin dulu."),
    ],
    [
        Q("Ruang sampel adalah?", ["Satu hasil", "Himpunan semua hasil", "Peluang total", "Jumlah percobaan"], 1, "Semua hasil yang mungkin.", hint="Himpunan S."),
        Q("Kejadian adalah?", ["Himpunan bagian ruang sampel", "Bilangan", "Fungsi", "Rata-rata"], 0, "Kumpulan hasil yang diminati.", hint="Subset."),
        Q("P(S) sama dengan?", ["0", "0,5", "1", "Tak tentu"], 2, "Pasti ada hasil.", hint="Pasti."),
        Q("Berapa hasil pada dua dadu?", ["11", "12", "36", "6"], 2, "Enam kali enam.", hint="Pasangan."),
        Q("Dua kejadian saling lepas bila?", ["Irisan kosong", "Gabungan kosong", "Peluang sama", "Ukuran sama"], 0, "Tidak bisa terjadi bersamaan.", hint="Irisan."),
    ],
    [
        "Ruang sampel memuat semua hasil dan kejadian adalah himpunan bagiannya.",
        "Peluang klasik adalah rasio ukuran kejadian terhadap ruang sampel untuk hasil sama mungkin.",
        "Operasi himpunan menggabungkan kejadian.",
        "Enumerasi dengan kode memverifikasi rumus.",
    ],
    [],
)

l2 = lesson(
    "A4-01-2",
    "Aturan penjumlahan, komplemen, dan independensi",
    35,
    [
        "Memakai aturan komplemen untuk peluang minimal satu",
        "Menerapkan aturan penjumlahan dengan koreksi irisan",
        "Menjelaskan kejadian independen dan aturan perkalian",
        "Membedakan saling lepas dari independen",
    ],
    [
        T("""
        ## Aturan komplemen

        Peluang bahwa kejadian `A` **tidak** terjadi adalah `P(bukan A) = 1 - P(A)`. Aturan sederhana ini sangat berguna ketika menghitung `A` langsung sulit tetapi komplemennya mudah. Pertanyaan berbunyi "minimal satu" sering lebih mudah dijawab lewat kebalikannya, yaitu "tidak satu pun".

        Contoh: peluang mendapat minimal satu angka enam dalam empat lemparan dadu. Menghitung langsung harus menjumlahkan kasus satu, dua, tiga, dan empat enam. Lewat komplemen, cukup hitung peluang tidak ada enam sama sekali, lalu kurangkan dari satu.
        """),
        C(
            """
            p_tanpa_enam = (5 / 6) ** 4
            print(round(p_tanpa_enam, 4))
            print(round(1 - p_tanpa_enam, 4))
            """,
            """
            0.4823
            0.5177
            """,
            """
            Peluang tidak ada enam dalam empat lemparan adalah lima per enam pangkat empat, dan minimal satu enam adalah sisanya sekitar 0,5177.
            """,
            filename="komplemen.py",
        ),
        T("""
        ## Aturan penjumlahan

        Untuk dua kejadian sembarang, `P(A atau B) = P(A) + P(B) - P(A dan B)`. Pengurangan irisan diperlukan karena hasil yang ada di `A` dan `B` sekaligus terhitung dua kali bila kita hanya menjumlahkan. Bila `A` dan `B` saling lepas, irisannya kosong dan aturannya menyederhana menjadi `P(A) + P(B)`.

        Lupa mengurangi irisan adalah kesalahan paling umum. Peluang gabungan tidak pernah boleh melebihi satu, sehingga hasil di atas satu adalah tanda langsung bahwa irisan terlupa.
        """),
        C(
            """
            S = {1, 2, 3, 4, 5, 6}
            A = {2, 4, 6}
            B = {4, 5, 6}
            langsung = len(A | B) / len(S)
            rumus = len(A) / 6 + len(B) / 6 - len(A & B) / 6
            print(round(langsung, 4), round(rumus, 4))
            """,
            """
            0.6667 0.6667
            """,
            """
            Penghitungan langsung dan rumus penjumlahan memberi nilai sama, dengan irisan yang berisi empat dan enam dikurangkan satu kali.
            """,
            filename="penjumlahan.py",
        ),
        T("""
        ## Kejadian independen

        Dua kejadian **independen** bila terjadinya yang satu tidak mengubah peluang yang lain. Secara formal, `A` dan `B` independen bila `P(A dan B) = P(A) * P(B)`. Lemparan koin berturut-turut independen: hasil lemparan pertama tidak memengaruhi lemparan kedua. Dua kejadian dari dadu yang berbeda juga independen.

        Aturan perkalian ini memudahkan hitungan urutan kejadian. Peluang tiga kepala berturut-turut pada koin adil adalah `0,5 * 0,5 * 0,5 = 0,125`. Namun independensi adalah asumsi yang perlu dibuktikan atau dibenarkan, bukan sesuatu yang boleh diasumsikan sembarangan.
        """),
        C(
            """
            from itertools import product

            S = list(product(range(1, 7), repeat=2))
            A = [h for h in S if h[0] % 2 == 0]
            B = [h for h in S if h[1] > 4]
            AB = [h for h in S if h[0] % 2 == 0 and h[1] > 4]
            pa = len(A) / 36
            pb = len(B) / 36
            print(round(pa * pb, 4), round(len(AB) / 36, 4))
            """,
            """
            0.1667 0.1667
            """,
            """
            Dadu pertama genap dan dadu kedua lebih dari empat independen, sehingga peluang irisan sama dengan hasil kali peluangnya.
            """,
            filename="independen.py",
        ),
        T("""
        ## Saling lepas bukan independen

        Banyak pemula mencampuradukkan dua gagasan ini. Kejadian saling lepas tidak bisa terjadi bersamaan, jadi bila satu terjadi maka yang lain pasti tidak terjadi. Itu justru ketergantungan yang kuat: mengetahui `A` terjadi mengubah peluang `B` menjadi nol.

        Karena itu dua kejadian dengan peluang positif yang saling lepas tidak mungkin independen. Untuk keduanya independen, `P(A dan B) = P(A) * P(B)` yang positif, sedangkan saling lepas menuntut irisan peluang nol. Ingat perbedaan ini setiap kali memilih antara aturan penjumlahan dan perkalian.
        """),
        K(
            "warn",
            """
            Aturan penjumlahan untuk kejadian atau, aturan perkalian untuk kejadian dan. Perkalian sederhana hanya berlaku bila independen. Bila ragu, hitung irisan langsung dengan enumerasi.
            """,
            title="Atau dan dan",
        ),
        T("""
        ## Independensi dalam data nyata

        Dalam data nyata, banyak kejadian yang tampak independen ternyata tidak. Pelanggan yang membeli produk A cenderung membeli produk B, dan gejala penyakit saling berkaitan. Mengasumsikan independen di sana akan mengecilkan peluang kejadian bersama secara salah.

        Model Naive Bayes sengaja mengasumsikan independensi antar fitur untuk menyederhanakan hitungan, dan sering tetap bekerja baik walau asumsinya tidak tepat. Itu keputusan rekayasa yang sadar, bukan klaim bahwa dunia benar-benar independen.
        """),
        T("""
        ## Merangkai aturan

        Soal nyata biasanya menggabungkan beberapa aturan. Misalnya, peluang sebuah sistem gagal bila dua komponen cadangan harus gagal bersamaan adalah hasil kali peluang gagal masing-masing, jika independen. Peluang sistem tetap berjalan adalah komplemennya.

        Kerjakan dengan tiga langkah: definisikan kejadian dengan jelas, tentukan apakah soal meminta atau, dan, atau bukan, lalu pilih aturan yang sesuai dan periksa asumsinya. Verifikasi dengan enumerasi atau simulasi kecil bila ruang sampelnya memungkinkan.
        """),
        T("""
        ## Contoh gabungan dua aturan

        Sebuah toko daring menemukan bahwa 40 persen pengunjung membuka halaman promo dan 30 persen menambahkan barang ke keranjang. Bila 15 persen melakukan keduanya, peluang pengunjung melakukan minimal salah satu adalah `0,4 + 0,3 - 0,15 = 0,55`. Peluang tidak melakukan keduanya adalah komplemennya, yaitu `0,45`.

        Perhatikan bahwa kedua kejadian tidak independen di sini, karena `0,4 * 0,3 = 0,12` berbeda dari `0,15`. Selisih itu menandakan hubungan positif: pengunjung promo lebih sering menambah keranjang. Pengujian independensi seperti ini adalah langkah awal analisis hubungan antar variabel.
        """),
        T("""
        ## Latihan mandiri

        Setelah membaca, coba tulis ulang satu contoh dengan angka berbeda tanpa melihat kode. Ubah parameter, perkirakan hasilnya dengan tangan, lalu jalankan untuk mencocokkan. Kebiasaan menebak lalu memverifikasi melatih intuisi probabilistik jauh lebih cepat daripada hanya membaca rumus.
        """),
        E(
            "A4-01-2-ex1",
            "mudah",
            """
            Tulis fungsi `peluang_komplemen(p)` yang mengembalikan `1 - p` dibulatkan 4 desimal.
            """,
            """
            def peluang_komplemen(p):
                # TODO: implementasikan
                pass
            """,
            """
            assert peluang_komplemen(0.3) == 0.7
            assert peluang_komplemen(0) == 1.0
            assert peluang_komplemen(1) == 0.0
            assert peluang_komplemen(0.85) == 0.15
            """,
            "Kurangkan dari satu lalu bulatkan.",
            """
            def peluang_komplemen(p):
                return round(1 - p, 4)
            """,
        ),
        E(
            "A4-01-2-ex2",
            "sedang",
            """
            Tulis fungsi `peluang_gabungan(pa, pb, pab)` yang mengembalikan `P(A atau B)` dibulatkan 4 desimal.
            """,
            """
            def peluang_gabungan(pa, pb, pab):
                # TODO: implementasikan
                pass
            """,
            """
            assert peluang_gabungan(0.5, 0.4, 0.2) == 0.7
            assert peluang_gabungan(0.3, 0.3, 0) == 0.6
            assert peluang_gabungan(0.6, 0.5, 0.5) == 0.6
            assert peluang_gabungan(0.25, 0.25, 0.0625) == 0.4375
            """,
            "Jumlahkan kedua peluang lalu kurangi irisan.",
            """
            def peluang_gabungan(pa, pb, pab):
                return round(pa + pb - pab, 4)
            """,
        ),
        E(
            "A4-01-2-ex3",
            "sedang",
            """
            Tulis fungsi `minimal_satu(p, n)` yang mengembalikan peluang minimal satu sukses dalam `n` percobaan independen dengan peluang sukses `p` tiap percobaan, dibulatkan 4 desimal.
            """,
            """
            def minimal_satu(p, n):
                # TODO: implementasikan
                pass
            """,
            """
            assert minimal_satu(1 / 6, 4) == 0.5177
            assert minimal_satu(0.5, 1) == 0.5
            assert minimal_satu(0.5, 3) == 0.875
            assert minimal_satu(0.1, 0) == 0.0
            """,
            "Pakai komplemen dari tidak satu pun sukses.",
            """
            def minimal_satu(p, n):
                return round(1 - (1 - p) ** n, 4)
            """,
        ),
        E(
            "A4-01-2-ex4",
            "menantang",
            """
            Tulis fungsi `apakah_independen(pa, pb, pab)` yang mengembalikan True bila `pab` sama dengan `pa * pb` dengan toleransi `1e-9`, dan False bila tidak.
            """,
            """
            def apakah_independen(pa, pb, pab):
                # TODO: implementasikan
                pass
            """,
            """
            assert apakah_independen(0.5, 0.5, 0.25) is True
            assert apakah_independen(0.5, 0.5, 0.3) is False
            assert apakah_independen(0.2, 0.3, 0.06) is True
            assert apakah_independen(0.5, 0.4, 0.4) is False
            """,
            "Bandingkan pab dengan hasil kali menggunakan selisih mutlak kecil.",
            """
            def apakah_independen(pa, pb, pab):
                return abs(pab - pa * pb) < 1e-9
            """,
        ),
    ],
    [
        M("Lupa mengurangi irisan pada aturan penjumlahan.", "Kurangi P(A dan B)."),
        M("Memakai perkalian tanpa memeriksa independensi.", "Cek atau buktikan independen."),
        M("Menyamakan saling lepas dengan independen.", "Saling lepas justru ketergantungan kuat."),
    ],
    [
        Q("Rumus komplemen?", ["1 - P(A)", "P(A) + 1", "P(A)^2", "P(A)/2"], 0, "Bukan A.", hint="Sisa."),
        Q("Aturan penjumlahan umum?", ["P(A)+P(B)", "P(A)+P(B)-P(A dan B)", "P(A)P(B)", "P(A)-P(B)"], 1, "Kurangi irisan.", hint="Irisan dua kali."),
        Q("Independen berarti?", ["P(A dan B)=P(A)P(B)", "Irisan kosong", "P(A)=P(B)", "Gabungan S"], 0, "Hasil kali.", hint="Perkalian."),
        Q("Kejadian saling lepas dengan peluang positif?", ["Independen", "Tidak independen", "Selalu terjadi", "Mustahil"], 1, "Irisan nol tapi hasil kali positif.", hint="Beda."),
        Q("Peluang minimal satu paling mudah lewat?", ["Komplemen", "Gabungan", "Rata-rata", "Median"], 0, "Tidak satu pun lalu kurangkan.", hint="Kebalikan."),
    ],
    [
        "Komplemen memudahkan soal minimal satu.",
        "Aturan penjumlahan mengurangi irisan.",
        "Independen berarti irisan sama dengan hasil kali peluang.",
        "Saling lepas bukan independen.",
    ],
    [],
)

l3 = lesson(
    "A4-01-3",
    "Pencacahan: permutasi dan kombinasi",
    35,
    [
        "Memakai aturan perkalian untuk menghitung banyak cara",
        "Membedakan permutasi dan kombinasi",
        "Menghitung peluang dengan pencacahan",
        "Menyelesaikan masalah ulang tahun dan undian",
    ],
    [
        T("""
        ## Mengapa perlu menghitung cara

        Peluang klasik membutuhkan ukuran ruang sampel dan kejadian. Untuk soal kecil kita bisa mendaftar semuanya, tetapi untuk soal besar seperti memilih enam angka dari empat puluh sembilan, mendaftar tidak mungkin. **Pencacahan** atau kombinatorika memberi rumus untuk menghitung banyak cara tanpa mendaftarnya satu per satu.

        Dua alat utamanya adalah permutasi untuk susunan yang memperhatikan urutan dan kombinasi untuk pilihan yang tidak memperhatikan urutan. Keduanya bertumpu pada aturan perkalian: bila satu langkah punya `m` cara dan langkah berikutnya `n` cara, maka total `m * n` cara.
        """),
        T("""
        ## Faktorial dan permutasi

        Banyaknya cara menyusun `n` objek berbeda dalam satu baris adalah `n!`, dibaca n faktorial, yaitu `n * (n-1) * ... * 1`. Lima buku dapat disusun dalam `5! = 120` cara. Bila kita hanya memilih dan menyusun `k` dari `n` objek, banyak susunannya adalah **permutasi** `P(n, k) = n! / (n-k)!`.

        Contohnya memilih ketua, wakil, dan sekretaris dari lima orang: `5 * 4 * 3 = 60` cara. Urutan penting karena jabatan berbeda. Di Python tersedia `math.factorial` dan `math.perm` untuk menghitungnya langsung.
        """),
        T("""
        ## Kombinasi

        Bila urutan tidak penting, misalnya memilih panitia tiga orang dari lima tanpa jabatan, kita memakai **kombinasi** `C(n, k) = n! / (k! * (n-k)!)`. Setiap kelompok `k` orang muncul `k!` kali dalam hitungan permutasi karena bisa disusun ulang, sehingga permutasi dibagi `k!`.

        Untuk lima orang dan panitia tiga, `C(5, 3) = 10`, sedangkan permutasinya 60 dibagi `3! = 6`. Pertanyaan kunci untuk memilih alat: apakah menukar urutan menghasilkan hasil yang berbeda? Bila ya, permutasi. Bila tidak, kombinasi.
        """),
        C(
            """
            import math

            print(math.factorial(5))
            print(math.perm(5, 3))
            print(math.comb(5, 3))
            """,
            """
            120
            60
            10
            """,
            """
            Lima objek dapat disusun seratus dua puluh cara, memilih tiga berurutan memberi enam puluh, dan memilih tiga tanpa urutan memberi sepuluh.
            """,
            filename="hitung_cara.py",
        ),
        T("""
        ## Dengan dan tanpa pengulangan

        Bila objek boleh dipakai berulang, hitungannya lebih sederhana. Kata sandi tiga huruf dari 26 huruf dengan pengulangan punya `26 ** 3 = 17576` kemungkinan karena tiap posisi bebas dipilih. Bila huruf tidak boleh berulang, hitungannya permutasi `26 * 25 * 24 = 15600`.

        Perhatikan kata kunci dalam soal: boleh berulang atau tidak, urutan penting atau tidak. Dua pertanyaan ini menentukan rumus yang dipakai. Salah membaca keduanya adalah sumber utama kesalahan pada soal pencacahan.
        """),
        C(
            """
            import math

            print(26 ** 3)
            print(math.perm(26, 3))
            print(math.comb(49, 6))
            print(f"{1 / math.comb(49, 6):.3e}")
            """,
            """
            17576
            15600
            13983816
            7.151e-08
            """,
            """
            Sandi dengan pengulangan lebih banyak daripada tanpa pengulangan. Peluang menebak enam angka undian dari empat puluh sembilan sekitar tujuh per seratus juta.
            """,
            filename="sandi_undian.py",
        ),
        T("""
        ## Peluang dengan pencacahan

        Gabungkan pencacahan dengan peluang klasik: `P(A) = banyak cara A / banyak cara total`. Misalnya peluang mengambil tepat dua kartu as dalam lima kartu dari setumpuk 52. Ada `C(4, 2)` cara memilih dua as dan `C(48, 3)` cara memilih tiga kartu non-as, sedangkan total tangan lima kartu adalah `C(52, 5)`.

        Pola umum ini, memilih sebagian dari kelompok yang baik dan sebagian dari kelompok lain, disebut distribusi hipergeometrik. Pola ini muncul pada pengambilan sampel tanpa pengembalian, misalnya memeriksa barang cacat dari satu lot.
        """),
        K(
            "tip",
            """
            Untuk soal peluang dengan pengambilan, tentukan ukuran ruang sampel dengan kombinasi total, lalu hitung kejadian dengan perkalian kombinasi tiap kelompok. Bagi keduanya di akhir.
            """,
            title="Pola hipergeometrik",
        ),
        T("""
        ## Masalah ulang tahun

        Berapa orang dalam satu ruangan agar peluang dua orang berulang tahun sama melebihi setengah? Banyak orang menebak ratusan, padahal jawabannya hanya 23. Kuncinya komplemen: hitung peluang semua ulang tahun berbeda lalu kurangkan dari satu.

        Orang pertama bebas, orang kedua harus berbeda dengan peluang `364/365`, orang ketiga `363/365`, dan seterusnya. Hasil kali pecahan itu turun cepat karena banyak pasangan yang mungkin: untuk 23 orang ada 253 pasangan, masing-masing berpeluang kecil tetapi bersama-sama menjadi besar. Intuisi kita meremehkan efek jumlah pasangan.
        """),
        C(
            """
            p = 1.0
            for i in range(23):
                p *= (365 - i) / 365
            print(round(1 - p, 4))
            """,
            """
            0.5073
            """,
            """
            Dengan dua puluh tiga orang peluang minimal sepasang berulang tahun sama sudah sedikit di atas setengah.
            """,
            filename="ulang_tahun.py",
        ),
        T("""
        ## Memilih cara hitung

        Ringkasan memilih alat. Bila soal menyebut susunan, urutan, atau jabatan, pakai permutasi. Bila soal menyebut kelompok, tim, atau sampel tanpa peran, pakai kombinasi. Bila objek boleh dipakai ulang, pakai pangkat. Bila ada beberapa kelompok yang dipilih sekaligus, kalikan kombinasi tiap kelompok.

        Selalu uji rumusmu pada versi kecil yang bisa didaftar dengan itertools. Bila `permutations` dan `combinations` memberi jumlah yang sama dengan rumusmu, kamu bisa percaya rumus itu untuk ukuran besar.
        """),
        T("""
        ## Latihan mandiri

        Setelah membaca, coba tulis ulang satu contoh dengan angka berbeda tanpa melihat kode. Ubah parameter, perkirakan hasilnya dengan tangan, lalu jalankan untuk mencocokkan. Kebiasaan menebak lalu memverifikasi melatih intuisi probabilistik jauh lebih cepat daripada hanya membaca rumus.
        """),
        E(
            "A4-01-3-ex1",
            "mudah",
            """
            Tulis fungsi `permutasi(n, k)` yang mengembalikan banyak susunan `k` dari `n` objek berbeda. Kembalikan 0 bila `k > n`.
            """,
            """
            import math

            def permutasi(n, k):
                # TODO: implementasikan
                pass
            """,
            """
            assert permutasi(5, 3) == 60
            assert permutasi(4, 4) == 24
            assert permutasi(6, 0) == 1
            assert permutasi(3, 5) == 0
            """,
            "Hitung n faktorial dibagi n minus k faktorial atau pakai math.perm.",
            """
            import math

            def permutasi(n, k):
                if k > n:
                    return 0
                return math.factorial(n) // math.factorial(n - k)
            """,
        ),
        E(
            "A4-01-3-ex2",
            "sedang",
            """
            Tulis fungsi `kombinasi(n, k)` yang mengembalikan banyak pilihan `k` dari `n` objek tanpa urutan. Kembalikan 0 bila `k > n`.
            """,
            """
            import math

            def kombinasi(n, k):
                # TODO: implementasikan
                pass
            """,
            """
            assert kombinasi(5, 3) == 10
            assert kombinasi(49, 6) == 13983816
            assert kombinasi(6, 0) == 1
            assert kombinasi(3, 5) == 0
            assert kombinasi(10, 10) == 1
            """,
            "Bagi permutasi dengan k faktorial.",
            """
            import math

            def kombinasi(n, k):
                if k > n:
                    return 0
                return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))
            """,
        ),
        E(
            "A4-01-3-ex3",
            "sedang",
            """
            Tulis fungsi `peluang_tepat(total, baik, ambil, j)` yang mengembalikan peluang bahwa pengambilan `ambil` objek tanpa pengembalian dari `total` objek, yang memuat `baik` objek bagus, mendapat tepat `j` objek bagus. Bulatkan 4 desimal.
            """,
            """
            import math

            def peluang_tepat(total, baik, ambil, j):
                # TODO: implementasikan
                pass
            """,
            """
            assert peluang_tepat(10, 4, 3, 2) == 0.3
            assert peluang_tepat(52, 4, 5, 2) == 0.0399
            assert peluang_tepat(10, 4, 3, 0) == 0.1667
            assert peluang_tepat(10, 4, 3, 3) == 0.0333
            """,
            "Kalikan kombinasi objek bagus dan non-bagus lalu bagi dengan kombinasi total.",
            """
            import math

            def peluang_tepat(total, baik, ambil, j):
                return round(math.comb(baik, j) * math.comb(total - baik, ambil - j) / math.comb(total, ambil), 4)
            """,
        ),
        E(
            "A4-01-3-ex4",
            "menantang",
            """
            Tulis fungsi `peluang_ulang_tahun(n)` yang mengembalikan peluang minimal dua dari `n` orang berulang tahun sama pada tahun 365 hari, dibulatkan 4 desimal.
            """,
            """
            def peluang_ulang_tahun(n):
                # TODO: implementasikan
                pass
            """,
            """
            assert peluang_ulang_tahun(1) == 0.0
            assert peluang_ulang_tahun(2) == 0.0027
            assert peluang_ulang_tahun(23) == 0.5073
            assert peluang_ulang_tahun(60) == 0.9941
            """,
            "Kalikan pecahan (365 minus i) per 365 untuk i dari nol lalu ambil komplemennya.",
            """
            def peluang_ulang_tahun(n):
                p = 1.0
                for i in range(n):
                    p *= (365 - i) / 365
                return round(1 - p, 4)
            """,
        ),
    ],
    [
        M("Memakai kombinasi saat urutan penting.", "Urutan penting berarti permutasi."),
        M("Melupakan pembagian k faktorial pada kombinasi.", "Kombinasi sama dengan permutasi dibagi k faktorial."),
        M("Mengira masalah ulang tahun butuh ratusan orang.", "Hitung komplemen, cukup 23 orang."),
    ],
    [
        Q("Berapa cara menyusun 4 objek berbeda?", ["4", "16", "24", "12"], 2, "4 faktorial.", hint="Faktorial."),
        Q("Memilih panitia tanpa jabatan memakai?", ["Permutasi", "Kombinasi", "Faktorial saja", "Pangkat"], 1, "Urutan tidak penting.", hint="Tanpa urutan."),
        Q("C(5,3) sama dengan?", ["10", "60", "15", "125"], 0, "Lima faktorial dibagi tiga faktorial dua faktorial.", hint="Simetri."),
        Q("Kata sandi 3 huruf dengan pengulangan dari 26?", ["15600", "17576", "78", "2600"], 1, "26 pangkat 3.", hint="Tiap posisi bebas."),
        Q("Orang yang dibutuhkan agar peluang ulang tahun sama melebihi 0,5?", ["23", "100", "183", "365"], 0, "Lewat komplemen.", hint="Banyak pasangan."),
    ],
    [
        "Aturan perkalian menggandakan cara tiap langkah.",
        "Permutasi memperhatikan urutan dan kombinasi tidak.",
        "Peluang klasik memakai rasio banyak cara.",
        "Komplemen menyelesaikan masalah ulang tahun.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perhitungan yang cukup jelas dalam teks.", "brief": []}

write_module(
    "A4",
    1,
    "Ruang sampel dan aturan peluang",
    105,
    [
        "Menyusun ruang sampel dan kejadian",
        "Memakai aturan komplemen, penjumlahan, dan perkalian",
        "Menghitung peluang dengan permutasi dan kombinasi",
    ],
    [l1, l2, l3],
    video,
    REF,
)
