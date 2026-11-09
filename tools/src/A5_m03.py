import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

l1 = lesson(
    "A5-03-1",
    "Rentang, varians, dan simpangan baku",
    35,
    [
        "Menghitung rentang dan menjelaskan kelemahannya",
        "Menghitung varians dan simpangan baku populasi dan sampel",
        "Menjelaskan koreksi Bessel dengan pembagi n dikurangi satu",
        "Menghitung varians secara inkremental dengan satu kali lintasan",
    ],
    [
        T("""
        ## Mengapa pusat saja tidak cukup

        Dua kelas bisa memiliki nilai rata-rata sama persis, tetapi di kelas pertama semua siswa bernilai sekitar 70 sedangkan di kelas kedua separuhnya 40 dan separuhnya 100. Rata-rata menyembunyikan perbedaan besar itu. **Ukuran penyebaran** mengukur seberapa tersebar data di sekitar pusatnya, sehingga melengkapi ukuran pemusatan.

        Penyebaran menentukan seberapa dapat dipercaya rata-rata sebagai wakil data, seberapa besar risiko dalam keuangan, dan seberapa kuat sinyal dibanding derau. Pelajaran ini membahas tiga ukuran dasar: rentang, varians, dan simpangan baku.
        """),
        T("""
        ## Rentang

        **Rentang** adalah selisih nilai terbesar dan terkecil. Ia mudah dihitung dan mudah dijelaskan: data ini membentang dari sekian sampai sekian. Untuk data dua, empat, empat, empat, lima, lima, tujuh, sembilan, rentangnya tujuh.

        Kelemahannya serius. Rentang hanya memakai dua nilai paling ekstrem sehingga mengabaikan semua data di antaranya, dan satu pencilan langsung mengubahnya. Selain itu rentang cenderung membesar seiring bertambahnya data, karena peluang menemukan nilai ekstrem baru ikut naik. Karena itu rentang jarang dipakai sendirian dalam analisis serius.
        """),
        C(
            """
            d = [2, 4, 4, 4, 5, 5, 7, 9]
            print(max(d) - min(d))
            print(max(d + [100]) - min(d + [100]))
            """,
            """
            7
            98
            """,
            """
            Menambah satu pencilan seratus melompatkan rentang dari tujuh menjadi sembilan puluh delapan.
            """,
            filename="rentang.py",
        ),
        T("""
        ## Varians: rata-rata kuadrat simpangan

        Ide yang lebih baik adalah memakai semua data: ukur seberapa jauh tiap nilai dari rata-rata, lalu rata-ratakan. Namun jumlah simpangan selalu nol sehingga kita mengkuadratkannya dulu. **Varians populasi** adalah rata-rata kuadrat selisih nilai dari rata-rata: `jumlah (x - rata)^2 / n`.

        Mengkuadratkan membuat semua suku positif dan memberi bobot lebih pada simpangan besar. Satuan varians adalah kuadrat satuan data, misalnya meter persegi untuk data panjang, sehingga sulit ditafsirkan langsung.
        """),
        C(
            """
            d = [2, 4, 4, 4, 5, 5, 7, 9]
            m = sum(d) / len(d)
            print(sum((x - m) ** 2 for x in d) / len(d))
            """,
            """
            4.0
            """,
            """
            Rata-rata kuadrat simpangan dari rata-rata lima menghasilkan varians populasi empat.
            """,
            filename="varians.py",
        ),
        T("""
        ## Simpangan baku

        **Simpangan baku** adalah akar kuadrat varians. Akar mengembalikan satuan ke satuan data asli, sehingga bisa dibaca sebagai simpangan tipikal dari rata-rata. Untuk data di atas, simpangan baku populasi adalah dua: nilai biasanya berada sekitar dua satuan dari rata-rata lima.

        Pada data berbentuk lonceng, sekitar dua pertiga data berada dalam satu simpangan baku dari rata-rata dan sekitar sembilan puluh lima persen dalam dua simpangan baku. Aturan praktis ini menjadikan simpangan baku bahasa umum untuk menyatakan sebaran.
        """),
        T("""
        ## Populasi atau sampel

        Bila data adalah seluruh populasi, bagi dengan `n`. Tetapi bila data hanyalah sampel yang dipakai menaksir populasi, bagi dengan `n - 1`. Ini disebut **koreksi Bessel**. Alasannya, rata-rata sampel dihitung dari data yang sama sehingga data selalu sedikit lebih dekat ke rata-rata sampel daripada ke rata-rata populasi sebenarnya, dan pembagi `n` akan meremehkan varians.

        Untuk data contoh, varians sampel adalah 4,5714, sedikit lebih besar dari 4. Perbedaan mengecil seiring `n` membesar, tetapi pada sampel kecil cukup berarti. Pustaka berbeda memakai default berbeda, jadi selalu periksa.
        """),
        C(
            """
            import statistics

            d = [2, 4, 4, 4, 5, 5, 7, 9]
            print(statistics.pvariance(d), round(statistics.variance(d), 4))
            print(statistics.pstdev(d), round(statistics.stdev(d), 4))
            """,
            """
            4 4.5714
            2.0 2.1381
            """,
            """
            Pembagi n menghasilkan varians empat dan simpangan baku dua, sedangkan pembagi n dikurangi satu menghasilkan nilai sedikit lebih besar.
            """,
            filename="populasi_sampel.py",
        ),
        T("""
        ## Sifat penyebaran

        Penyebaran tidak berubah bila semua nilai digeser dengan konstanta, karena selisih terhadap rata-rata tetap. Tetapi bila semua nilai dikalikan `a`, simpangan baku dikalikan `|a|` dan varians dikalikan `a` kuadrat. Jadi mengubah meter menjadi sentimeter menggandakan simpangan baku seratus kali, sedangkan menambah sepuluh pada semua nilai tidak mengubahnya.

        Sifat ini menjelaskan mengapa simpangan baku dipakai untuk standardisasi dan mengapa varians dua variabel independen bisa dijumlahkan. Ia juga mengingatkan bahwa membandingkan simpangan baku antar satuan berbeda tidak bermakna.
        """),
        C(
            """
            import statistics

            d = [2, 4, 4, 4, 5, 5, 7, 9]
            print(statistics.pstdev([2 * x + 3 for x in d]))
            print(statistics.pstdev([x + 10 for x in d]))
            """,
            """
            4.0
            2.0
            """,
            """
            Mengalikan dengan dua menggandakan simpangan baku menjadi empat, sedangkan menggeser sepuluh tidak mengubahnya.
            """,
            filename="sifat_sebaran.py",
        ),
        T("""
        ## Varians dalam satu lintasan

        Rumus langsung memerlukan dua lintasan: satu untuk rata-rata dan satu untuk simpangan. Pada aliran data besar kita ingin satu lintasan. **Algoritma Welford** memperbarui rata-rata dan jumlah kuadrat simpangan `m2` secara inkremental: untuk tiap nilai baru `x`, hitung `delta = x - rata`, perbarui `rata += delta / n`, lalu `m2 += delta * (x - rata)`. Varians populasi adalah `m2 / n`.

        Algoritma ini stabil secara numerik, tidak seperti rumus `rata kuadrat dikurangi kuadrat rata` yang bisa memberi hasil negatif akibat pembulatan pada data besar.
        """),
        C(
            """
            rata = 0.0
            m2 = 0.0
            n = 0
            for x in [2, 4, 4, 4, 5, 5, 7, 9]:
                n += 1
                delta = x - rata
                rata += delta / n
                m2 += delta * (x - rata)
            print(rata, m2 / n)
            """,
            """
            5.0 4.0
            """,
            """
            Satu lintasan Welford menghasilkan rata-rata lima dan varians empat, sama dengan rumus dua lintasan.
            """,
            filename="welford.py",
        ),
        K(
            "warn",
            """
            Periksa default pustaka. NumPy memakai pembagi n secara default, sedangkan pandas memakai n dikurangi satu. Tentukan parameter ddof secara eksplisit.
            """,
            title="Default berbeda antar pustaka",
        ),
        E(
            "A5-03-1-ex1",
            "mudah",
            """
            Tulis fungsi `rentang(data)` yang mengembalikan selisih maksimum dan minimum, atau `None` untuk list kosong.
            """,
            """
            def rentang(data):
                # TODO: implementasikan
                pass
            """,
            """
            assert rentang([2, 4, 4, 4, 5, 5, 7, 9]) == 7
            assert rentang([5]) == 0
            assert rentang([3, 1]) == 2
            assert rentang([]) is None
            """,
            "Kurangi minimum dari maksimum setelah memeriksa list kosong.",
            """
            def rentang(data):
                if not data:
                    return None
                return max(data) - min(data)
            """,
        ),
        E(
            "A5-03-1-ex2",
            "sedang",
            """
            Tulis fungsi `varians(data, sampel=False)` yang mengembalikan varians dibulatkan 4 desimal. Bila `sampel` benar bagi dengan `n - 1`, bila tidak bagi dengan `n`.
            """,
            """
            def varians(data, sampel=False):
                # TODO: implementasikan
                pass
            """,
            """
            assert varians([2, 4, 4, 4, 5, 5, 7, 9]) == 4.0
            assert varians([2, 4, 4, 4, 5, 5, 7, 9], sampel=True) == 4.5714
            assert varians([1, 2, 3, 4, 5]) == 2.0
            assert varians([4, 8], sampel=True) == 8.0
            """,
            "Hitung jumlah kuadrat selisih dari rata-rata lalu bagi dengan pembagi yang sesuai.",
            """
            def varians(data, sampel=False):
                m = sum(data) / len(data)
                pembagi = len(data) - 1 if sampel else len(data)
                return round(sum((x - m) ** 2 for x in data) / pembagi, 4)
            """,
        ),
        E(
            "A5-03-1-ex3",
            "sedang",
            """
            Tulis fungsi `simpangan_baku(data, sampel=False)` yang mengembalikan akar varians dibulatkan 4 desimal. Untuk sampel dengan satu data kembalikan `None`.
            """,
            """
            import math

            def simpangan_baku(data, sampel=False):
                # TODO: implementasikan
                pass
            """,
            """
            assert simpangan_baku([2, 4, 4, 4, 5, 5, 7, 9]) == 2.0
            assert simpangan_baku([2, 4, 4, 4, 5, 5, 7, 9], sampel=True) == 2.1381
            assert simpangan_baku([10, 12, 14, 16, 18]) == 2.8284
            assert simpangan_baku([10, 12, 14, 16, 18], sampel=True) == 3.1623
            assert simpangan_baku([5], sampel=True) is None
            """,
            "Tangani kasus sampel satu data lalu ambil akar dari varians.",
            """
            import math

            def simpangan_baku(data, sampel=False):
                n = len(data)
                if sampel and n < 2:
                    return None
                m = sum(data) / n
                pembagi = n - 1 if sampel else n
                return round(math.sqrt(sum((x - m) ** 2 for x in data) / pembagi), 4)
            """,
        ),
        E(
            "A5-03-1-ex4",
            "menantang",
            """
            Tulis fungsi `varians_welford(stream)` yang menghitung varians populasi dalam satu lintasan dengan algoritma Welford dan mengembalikannya dibulatkan 4 desimal. List kosong mengembalikan `None`.
            """,
            """
            def varians_welford(stream):
                # TODO: implementasikan
                pass
            """,
            """
            assert varians_welford([2, 4, 4, 4, 5, 5, 7, 9]) == 4.0
            assert varians_welford([1, 2, 3, 4, 5]) == 2.0
            assert varians_welford([5]) == 0.0
            assert varians_welford([2, 4, 6, 8]) == 5.0
            assert varians_welford([]) is None
            """,
            "Perbarui rata-rata dan m2 untuk tiap nilai, lalu bagi m2 dengan n.",
            """
            def varians_welford(stream):
                rata = 0.0
                m2 = 0.0
                n = 0
                for x in stream:
                    n += 1
                    delta = x - rata
                    rata += delta / n
                    m2 += delta * (x - rata)
                if n == 0:
                    return None
                return round(m2 / n, 4) + 0.0
            """,
        ),
    ],
    [
        M("Memakai rentang sebagai satu-satunya ukuran sebaran.", "Pakai simpangan baku atau IQR."),
        M("Selalu membagi dengan n untuk data sampel.", "Pakai n dikurangi satu untuk sampel."),
        M("Membandingkan simpangan baku antar satuan berbeda.", "Pakai koefisien variasi."),
    ],
    [
        Q("Varians populasi adalah?", ["Rata-rata kuadrat simpangan", "Akar rata-rata", "Maks - min", "Median simpangan"], 0, "Kuadrat selisih dirata-ratakan.", hint="Kuadrat."),
        Q("Simpangan baku sampel memakai pembagi?", ["n", "n - 1", "n + 1", "2n"], 1, "Koreksi Bessel.", hint="Bessel."),
        Q("Menggeser semua nilai +10 mengubah simpangan baku?", ["Tidak berubah", "Bertambah 10", "Dikali 10", "Menjadi nol"], 0, "Selisih tetap.", hint="Geser."),
        Q("Kelemahan rentang?", ["Peka pada pencilan", "Terlalu rumit", "Selalu nol", "Memakai semua data"], 0, "Hanya dua nilai.", hint="Ekstrem."),
        Q("Keunggulan Welford?", ["Satu lintasan dan stabil", "Lebih lambat", "Hanya data kecil", "Tanpa rata-rata"], 0, "Inkremental.", hint="Stream."),
    ],
    [
        "Varians dan simpangan baku memakai semua data, rentang hanya dua nilai.",
        "Sampel memakai n dikurangi satu untuk menaksir varians populasi.",
        "Menggeser tidak mengubah sebaran, menskala mengalikan simpangan baku.",
        "Welford menghitung varians dalam satu lintasan secara stabil.",
    ],
    [],
)

l2 = lesson(
    "A5-03-2",
    "Kuartil, IQR, dan MAD yang kokoh",
    35,
    [
        "Menghitung kuartil dan IQR dengan interpolasi linear",
        "Menghitung median simpangan mutlak atau MAD",
        "Mendeteksi pencilan dengan aturan 1,5 kali IQR",
        "Menyusun ringkasan lima angka",
    ],
    [
        T("""
        ## Penyebaran yang tahan pencilan

        Simpangan baku sangat dipengaruhi pencilan karena simpangan dikuadratkan. Satu nilai ekstrem dapat melipatgandakannya. Untuk data berekor panjang atau kotor kita membutuhkan ukuran sebaran yang kokoh, seperti rentang antarkuartil dan median simpangan mutlak. Keduanya memadankan median pada sisi pemusatan.

        Dalam laporan, pasangan yang konsisten adalah rata-rata dengan simpangan baku untuk data simetris bersih, dan median dengan IQR atau MAD untuk data miring atau berpencilan. Mencampur pasangan itu membingungkan pembaca.
        """),
        T("""
        ## Kuartil dan IQR

        **Kuartil** membagi data terurut menjadi empat bagian sama banyak. Kuartil pertama Q1 adalah kuantil ke-0,25, median Q2 kuantil ke-0,5, dan Q3 kuantil ke-0,75. **Rentang antarkuartil** atau IQR adalah `Q3 - Q1`, lebar setengah data tengah. Pencilan di ujung tidak memengaruhinya selama tidak mencapai seperempat data.

        Untuk data satu sampai sembilan dan seratus, rentangnya 99 tetapi IQR hanya 4,5. IQR menggambarkan sebaran data utama dengan jujur sementara rentang terdistorsi oleh satu nilai.
        """),
        C(
            """
            def kuantil(data, q):
                s = sorted(data)
                p = (len(s) - 1) * q
                lo = int(p)
                hi = min(lo + 1, len(s) - 1)
                return s[lo] + (s[hi] - s[lo]) * (p - lo)

            d = [1, 2, 3, 4, 5, 6, 7, 8, 9, 100]
            q1, q3 = kuantil(d, 0.25), kuantil(d, 0.75)
            print(q1, q3, q3 - q1)
            """,
            """
            3.25 7.75 4.5
            """,
            """
            Kuartil pertama tiga koma dua lima dan ketiga tujuh koma tujuh lima memberi IQR empat koma lima walau ada pencilan seratus.
            """,
            filename="iqr.py",
        ),
        T("""
        ## Median simpangan mutlak

        **MAD** atau median absolute deviation adalah median dari nilai mutlak selisih tiap data terhadap median data. Ia mudah dihitung dan memiliki titik patah lima puluh persen, sama seperti median. Untuk data satu sampai sembilan dan seratus, median 5,5, selisih mutlaknya dimulai dari 0,5, dan MAD hasilnya 2,5.

        Untuk data berdistribusi normal, `1,4826 * MAD` mendekati simpangan baku, sehingga MAD terskala sering dipakai sebagai penaksir simpangan baku yang kokoh dalam deteksi anomali.
        """),
        C(
            """
            import statistics

            def mad(data):
                med = statistics.median(data)
                return statistics.median([abs(x - med) for x in data])

            print(mad([1, 2, 3, 4, 5, 6, 7, 8, 9, 100]))
            print(mad([5, 6, 5, 7, 6, 100]))
            """,
            """
            2.5
            1.0
            """,
            """
            MAD tetap kecil pada data dengan satu pencilan besar karena hanya bergantung pada median selisih.
            """,
            filename="mad.py",
        ),
        T("""
        ## Aturan pagar untuk pencilan

        John Tukey mengusulkan aturan sederhana: nilai di bawah `Q1 - 1,5 * IQR` atau di atas `Q3 + 1,5 * IQR` ditandai sebagai pencilan potensial. Batas itu disebut pagar. Pada data gaji lima, lima, enam, enam, tujuh, seratus, Q1 5,25 dan Q3 6,75 memberi IQR 1,5 dan pagar atas sembilan, sehingga seratus ditandai.

        Perhatikan kata potensial. Pencilan bisa berupa kesalahan input atau kejadian langka nyata yang justru paling menarik. Aturan hanya menunjuk kandidat, keputusan membuang atau menyimpan harus berdasarkan pemahaman domain.
        """),
        C(
            """
            def kuantil(data, q):
                s = sorted(data)
                p = (len(s) - 1) * q
                lo = int(p)
                hi = min(lo + 1, len(s) - 1)
                return s[lo] + (s[hi] - s[lo]) * (p - lo)

            g = [5, 6, 5, 7, 6, 100]
            q1, q3 = kuantil(g, 0.25), kuantil(g, 0.75)
            iqr = q3 - q1
            print(q1, q3, iqr)
            print([x for x in g if x < q1 - 1.5 * iqr or x > q3 + 1.5 * iqr])
            """,
            """
            5.25 6.75 1.5
            [100]
            """,
            """
            Pagar atas sembilan menandai gaji seratus juta sebagai pencilan potensial.
            """,
            filename="pagar_tukey.py",
        ),
        T("""
        ## Ringkasan lima angka

        **Ringkasan lima angka** terdiri atas minimum, Q1, median, Q3, dan maksimum. Dalam lima bilangan, ia menggambarkan pusat, sebaran, dan kemiringan sekaligus, tanpa asumsi bentuk distribusi. Bila jarak median ke Q3 jauh lebih besar daripada jarak median ke Q1, distribusi miring ke kanan.

        Diagram kotak atau boxplot adalah gambar dari ringkasan ini: kotak dari Q1 ke Q3 dengan garis di median, kumis hingga pagar, dan titik untuk pencilan. Pelajaran berikutnya membahas bentuk distribusi lebih dalam.
        """),
        C(
            """
            import statistics

            def kuantil(data, q):
                s = sorted(data)
                p = (len(s) - 1) * q
                lo = int(p)
                hi = min(lo + 1, len(s) - 1)
                return s[lo] + (s[hi] - s[lo]) * (p - lo)

            d = [1, 2, 3, 4, 5, 6, 7, 8, 9, 100]
            print(min(d), kuantil(d, 0.25), statistics.median(d), kuantil(d, 0.75), max(d))
            """,
            """
            1 3.25 5.5 7.75 100
            """,
            """
            Lima angka memperlihatkan pusat di sekitar lima koma lima dan ekor kanan yang sangat panjang akibat seratus.
            """,
            filename="lima_angka.py",
        ),
        T("""
        ## Metode kuantil berbeda

        Ada banyak definisi kuantil sampel. Interpolasi linear pada posisi `(n - 1) * q`, yang kita pakai, adalah default NumPy dan pandas. Excel memiliki dua fungsi berbeda, dan beberapa buku teks memakai aturan yang membagi dua bagian data lalu mengambil median masing-masing. Pada data kecil hasilnya bisa berbeda sedikit.

        Karena itu, saat membandingkan hasil antar alat atau mereproduksi laporan, periksa definisi yang dipakai. Perbedaan menjadi tidak berarti pada data besar, tetapi pada data berukuran puluhan ia bisa mengubah satu pencilan menjadi bukan pencilan.
        """),
        K(
            "tip",
            """
            Untuk data miring atau berpencilan, laporkan median bersama IQR atau MAD. Untuk data simetris bersih, rata-rata dengan simpangan baku sudah cukup.
            """,
            title="Pasangan yang konsisten",
        ),
        T("""
        ## Boxplot dan membaca bentuk

        Boxplot memadatkan distribusi menjadi gambar kecil yang mudah dibandingkan antar kelompok. Dengan menjajarkan beberapa kotak, kita langsung melihat kelompok mana yang bergeser, lebih lebar, atau lebih miring, tanpa membaca tabel angka. Inilah alasan boxplot menjadi alat standar pada analisis eksploratif.

        Namun boxplot menyembunyikan jumlah puncak. Dua distribusi dengan satu dan dua puncak bisa menghasilkan kotak serupa. Pasangkan boxplot dengan histogram atau plot biola bila bentuk detail penting bagi kesimpulanmu.
        """),
        T("""
        ## Kapan memakai yang kokoh

        Ukuran kokoh tidak selalu lebih baik. Pada data normal bersih, simpangan baku lebih efisien: ia memberi taksiran lebih presisi dari sampel sama banyak. Ukuran kokoh mengorbankan sedikit efisiensi demi perlindungan terhadap data kotor, dan pertukaran ini hampir selalu layak pada data nyata.

        Cara praktis adalah menghitung keduanya. Bila simpangan baku jauh lebih besar dari `1,4826 * MAD`, curigai pencilan atau ekor berat, lalu telusuri datanya sebelum memutuskan ukuran mana yang dilaporkan.
        """),
        E(
            "A5-03-2-ex1",
            "mudah",
            """
            Tulis fungsi `kuartil_iqr(data)` yang mengembalikan tuple `(q1, q3, iqr)` memakai interpolasi linear pada posisi `(n - 1) * q`.
            """,
            """
            def kuartil_iqr(data):
                # TODO: implementasikan
                pass
            """,
            """
            assert kuartil_iqr([1, 2, 3, 4, 5, 6, 7, 8, 9, 100]) == (3.25, 7.75, 4.5)
            assert kuartil_iqr([1, 2, 3, 4, 5, 6, 7, 8]) == (2.75, 6.25, 3.5)
            assert kuartil_iqr([1, 2, 3, 4, 5]) == (2.0, 4.0, 2.0)
            """,
            "Hitung dua kuantil dengan interpolasi lalu kurangkan.",
            """
            def kuartil_iqr(data):
                s = sorted(data)

                def kuantil(q):
                    p = (len(s) - 1) * q
                    lo = int(p)
                    hi = min(lo + 1, len(s) - 1)
                    return s[lo] + (s[hi] - s[lo]) * (p - lo)

                q1, q3 = kuantil(0.25), kuantil(0.75)
                return (q1, q3, q3 - q1)
            """,
        ),
        E(
            "A5-03-2-ex2",
            "sedang",
            """
            Tulis fungsi `mad(data)` yang mengembalikan median dari selisih mutlak tiap data terhadap median data.
            """,
            """
            def mad(data):
                # TODO: implementasikan
                pass
            """,
            """
            assert mad([1, 2, 3, 4, 5, 6, 7, 8, 9, 100]) == 2.5
            assert mad([5, 6, 5, 7, 6, 100]) == 1.0
            assert mad([1, 2, 3]) == 1
            assert mad([4, 4, 4]) == 0
            """,
            "Cari median data, lalu median dari selisih mutlaknya.",
            """
            def mad(data):
                def med(v):
                    s = sorted(v)
                    n = len(s)
                    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2

                m = med(data)
                return med([abs(x - m) for x in data])
            """,
        ),
        E(
            "A5-03-2-ex3",
            "sedang",
            """
            Tulis fungsi `pencilan_iqr(data)` yang mengembalikan list terurut nilai di luar pagar `Q1 - 1.5 * IQR` dan `Q3 + 1.5 * IQR`, memakai interpolasi linear.
            """,
            """
            def pencilan_iqr(data):
                # TODO: implementasikan
                pass
            """,
            """
            assert pencilan_iqr([1, 2, 3, 4, 5, 6, 7, 8, 9, 100]) == [100]
            assert pencilan_iqr([1, 2, 3, 4, 5]) == []
            assert pencilan_iqr([5, 6, 5, 7, 6, 100]) == [100]
            assert pencilan_iqr([-50, 5, 6, 5, 7, 6]) == [-50]
            """,
            "Hitung kuartil dan pagar lalu saring nilai di luarnya.",
            """
            def pencilan_iqr(data):
                s = sorted(data)

                def kuantil(q):
                    p = (len(s) - 1) * q
                    lo = int(p)
                    hi = min(lo + 1, len(s) - 1)
                    return s[lo] + (s[hi] - s[lo]) * (p - lo)

                q1, q3 = kuantil(0.25), kuantil(0.75)
                iqr = q3 - q1
                return [x for x in s if x < q1 - 1.5 * iqr or x > q3 + 1.5 * iqr]
            """,
        ),
        E(
            "A5-03-2-ex4",
            "menantang",
            """
            Tulis fungsi `ringkasan_lima(data)` yang mengembalikan tuple `(min, q1, median, q3, max)` memakai interpolasi linear untuk kuartil dan median.
            """,
            """
            def ringkasan_lima(data):
                # TODO: implementasikan
                pass
            """,
            """
            assert ringkasan_lima([1, 2, 3, 4, 5, 6, 7, 8, 9, 100]) == (1, 3.25, 5.5, 7.75, 100)
            assert ringkasan_lima([1, 2, 3, 4, 5]) == (1, 2.0, 3.0, 4.0, 5)
            assert ringkasan_lima([10, 20]) == (10, 12.5, 15.0, 17.5, 20)
            """,
            "Pakai satu fungsi kuantil untuk tiga nilai tengah lalu tambahkan minimum dan maksimum.",
            """
            def ringkasan_lima(data):
                s = sorted(data)

                def kuantil(q):
                    p = (len(s) - 1) * q
                    lo = int(p)
                    hi = min(lo + 1, len(s) - 1)
                    return s[lo] + (s[hi] - s[lo]) * (p - lo)

                return (s[0], kuantil(0.25), kuantil(0.5), kuantil(0.75), s[-1])
            """,
        ),
    ],
    [
        M("Membuang semua titik di luar pagar tanpa memeriksa penyebabnya.", "Selidiki dulu apakah kesalahan atau kejadian nyata."),
        M("Mencampur rata-rata dengan IQR dalam satu laporan.", "Pasangkan rata-rata dengan simpangan baku, median dengan IQR atau MAD."),
        M("Menganggap semua alat memakai definisi kuantil yang sama.", "Periksa metode interpolasi."),
    ],
    [
        Q("IQR adalah?", ["Q3 - Q1", "Maks - min", "Median - rata", "Q2 - Q1 + Q3"], 0, "Lebar setengah data tengah.", hint="Kuartil."),
        Q("MAD adalah?", ["Median selisih mutlak dari median", "Rata-rata selisih", "Akar varians", "Maks selisih"], 0, "Kokoh.", hint="Median."),
        Q("Pagar atas Tukey?", ["Q3 + 1.5 IQR", "Q3 + IQR", "Maks", "Q3 + 3 IQR"], 0, "Aturan 1,5.", hint="Satu setengah."),
        Q("Ringkasan lima angka memuat?", ["Min Q1 median Q3 maks", "Rata simpangan", "Modus", "Varians"], 0, "Lima bilangan.", hint="Boxplot."),
        Q("Untuk data berpencilan pasangkan median dengan?", ["IQR atau MAD", "Simpangan baku", "Rentang saja", "Varians"], 0, "Pasangan kokoh.", hint="Kokoh."),
    ],
    [
        "IQR dan MAD adalah ukuran sebaran yang kokoh terhadap pencilan.",
        "Aturan pagar Tukey menandai pencilan potensial.",
        "Ringkasan lima angka menggambarkan pusat, sebaran, dan kemiringan.",
        "Definisi kuantil berbeda antar alat sehingga perlu diperiksa.",
    ],
    [],
)

l3 = lesson(
    "A5-03-3",
    "Koefisien variasi, standardisasi, dan Chebyshev",
    35,
    [
        "Menghitung koefisien variasi untuk membandingkan sebaran relatif",
        "Menghitung z-score dan min-max scaling",
        "Menerapkan ketaksamaan Chebyshev",
        "Memilih skala yang tepat untuk membandingkan variabel",
    ],
    [
        T("""
        ## Membandingkan sebaran antar variabel

        Mana yang lebih tersebar: tinggi badan dengan simpangan baku 7 sentimeter, atau berat badan dengan simpangan baku 10 kilogram? Pertanyaan itu tidak bermakna bila diajukan langsung, karena satuannya berbeda. Kita membutuhkan ukuran tanpa satuan atau ukuran yang menyesuaikan dengan besar nilainya.

        Pelajaran ini membahas koefisien variasi untuk sebaran relatif, serta standardisasi dan penskalaan yang membawa banyak variabel ke skala yang sebanding. Keduanya sangat sering dipakai dalam persiapan data untuk pemodelan.
        """),
        T("""
        ## Koefisien variasi

        **Koefisien variasi** atau CV adalah simpangan baku dibagi rata-rata. Ia menyatakan sebaran sebagai pecahan dari rata-rata, tanpa satuan. Simpangan baku 10 pada rata-rata 1000 berarti sebaran satu persen, sedangkan simpangan baku 10 pada rata-rata 20 berarti lima puluh persen, dua situasi yang sangat berbeda meski simpangan bakunya sama.

        CV hanya bermakna untuk data rasio dengan nol alami dan rata-rata jauh dari nol. Bila rata-rata mendekati nol, CV meledak dan menyesatkan. Untuk data interval seperti suhu Celsius, CV tidak bermakna sama sekali.
        """),
        C(
            """
            import statistics

            a = [100, 200, 300]
            b = [10, 12, 14, 16, 18]
            print(round(statistics.stdev(a) / statistics.mean(a), 4))
            print(round(statistics.stdev(b) / statistics.mean(b), 4))
            """,
            """
            0.5 0.2259
            """,
            """
            Data pertama memiliki sebaran relatif lima puluh persen, jauh lebih besar dari data kedua walau simpangan bakunya besar.
            """,
            filename="koefisien_variasi.py",
        ),
        T("""
        ## Z-score

        **Z-score** menyatakan seberapa banyak simpangan baku sebuah nilai berada dari rata-rata: `(x - rata) / simpangan baku`. Nilai nol berarti tepat di rata-rata, nilai satu berarti satu simpangan baku di atasnya, dan nilai negatif berarti di bawahnya. Setelah standardisasi, data memiliki rata-rata nol dan simpangan baku satu.

        Z-score memungkinkan perbandingan antar variabel berbeda. Nilai ujian 85 pada ujian dengan rata-rata 70 dan simpangan baku 10 memiliki z 1,5, mungkin lebih baik daripada nilai 90 pada ujian berrata-rata 85 dan simpangan baku 10 dengan z 0,5.
        """),
        C(
            """
            import statistics

            x = [1, 2, 3, 4, 5]
            m = statistics.mean(x)
            s = statistics.pstdev(x)
            print([round((v - m) / s, 4) for v in x])
            """,
            """
            [-1.4142, -0.7071, 0.0, 0.7071, 1.4142]
            """,
            """
            Z-score simetris di sekitar nol dan menunjukkan jarak tiap nilai dari rata-rata dalam satuan simpangan baku.
            """,
            filename="zscore.py",
        ),
        T("""
        ## Min-max scaling

        **Min-max scaling** memetakan data secara linear ke rentang nol sampai satu: `(x - min) / (maks - min)`. Nilai terkecil menjadi nol, terbesar menjadi satu, dan lainnya proporsional. Hasilnya mudah ditafsirkan dan terbatas, yang berguna untuk algoritma yang mengharapkan masukan berrentang tetap seperti jaringan saraf dengan sigmoid.

        Kelemahannya adalah kepekaan pada pencilan: satu nilai ekstrem menekan semua nilai lain ke ujung sempit. Z-score kurang rentan, dan skala kokoh memakai median dan IQR sebagai pengganti rata-rata dan simpangan baku.
        """),
        C(
            """
            x = [10, 20, 40]
            lo, hi = min(x), max(x)
            print([round((v - lo) / (hi - lo), 4) for v in x])
            """,
            """
            [0.0, 0.3333, 1.0]
            """,
            """
            Nilai terkecil menjadi nol dan terbesar menjadi satu, dengan nilai tengah proporsional pada sepertiga.
            """,
            filename="minmax.py",
        ),
        T("""
        ## Ketaksamaan Chebyshev

        Bagaimana bila kita tidak tahu bentuk distribusi? **Ketaksamaan Chebyshev** menjamin bahwa untuk distribusi apa pun, paling sedikit `1 - 1/k^2` data berada dalam `k` simpangan baku dari rata-rata, untuk `k` lebih dari satu. Dengan `k` sama dengan dua, paling sedikit 75 persen data berada dalam dua simpangan baku, dan dengan tiga paling sedikit sekitar 89 persen.

        Batas ini longgar dibanding aturan distribusi normal yang menjamin 95 persen, tetapi berlaku tanpa asumsi. Ia berguna sebagai pengaman ketika kita tidak yakin dengan bentuk distribusi.
        """),
        C(
            """
            d = [2, 4, 4, 4, 5, 5, 7, 9]
            m = sum(d) / len(d)
            s = (sum((x - m) ** 2 for x in d) / len(d)) ** 0.5
            for k in (1, 2):
                dalam = sum(1 for x in d if abs(x - m) <= k * s) / len(d)
                print(k, dalam, round(1 - 1 / k ** 2, 4))
            """,
            """
            1 0.75 0.0
            2 1.0 0.75
            """,
            """
            Proporsi nyata dalam dua simpangan baku adalah satu, di atas jaminan Chebyshev tujuh puluh lima persen.
            """,
            filename="chebyshev.py",
        ),
        T("""
        ## Memilih skala

        Algoritma berbasis jarak seperti k-NN dan k-means sangat dipengaruhi skala fitur: fitur dengan angka besar mendominasi jarak. Standardisasi atau min-max menyamakan kontribusi. Model berbasis pohon tidak peka skala sehingga tidak memerlukannya. Regresi dengan regularisasi juga memerlukan skala sama agar penalti adil.

        Aturan penting: hitung parameter skala dari data latih saja, lalu terapkan ke data uji. Menghitung dari seluruh data membocorkan informasi uji ke pelatihan, kesalahan halus yang membuat evaluasi terlalu optimistis.
        """),
        K(
            "warn",
            """
            Hitung rata-rata dan simpangan baku untuk standardisasi dari data latih saja, lalu terapkan dengan angka yang sama ke data uji.
            """,
            title="Kebocoran data pada penskalaan",
        ),
        T("""
        ## Skala kokoh

        Padanan kokoh dari standardisasi mengurangi median lalu membagi dengan IQR, atau dengan MAD terskala. Hasilnya tidak terpengaruh pencilan, sehingga nilai normal tetap berada pada rentang masuk akal sementara pencilan tetap tampak ekstrem. Pustaka pembelajaran mesin umumnya menyediakannya sebagai skala kokoh.

        Pada data keuangan dan sensor yang sering berpencilan, pilihan ini sering lebih stabil daripada z-score biasa. Tetapi untuk model yang mengharapkan data berdistribusi mendekati normal, standardisasi biasa tetap pilihan lazim.
        """),
        T("""
        ## Standardisasi bukan normalisasi bentuk

        Standardisasi hanya menggeser dan menskala, sehingga bentuk distribusi tidak berubah. Data miring tetap miring setelah dijadikan z-score. Bila model membutuhkan data mendekati simetris, gunakan transformasi lain seperti logaritma terlebih dahulu, baru standardisasi.

        Kekeliruan umum adalah mengira z-score membuat data berdistribusi normal. Ia hanya membuat rata-rata nol dan simpangan baku satu. Menyebut data terstandardisasi sebagai data normal adalah klaim berbeda yang harus diuji tersendiri.
        """),
        E(
            "A5-03-3-ex1",
            "mudah",
            """
            Tulis fungsi `koefisien_variasi(data)` yang mengembalikan simpangan baku sampel dibagi rata-rata dibulatkan 4 desimal. Bila rata-rata nol kembalikan `None`.
            """,
            """
            import statistics

            def koefisien_variasi(data):
                # TODO: implementasikan
                pass
            """,
            """
            assert koefisien_variasi([100, 200, 300]) == 0.5
            assert koefisien_variasi([10, 12, 14, 16, 18]) == 0.2259
            assert koefisien_variasi([-1, 1]) is None
            """,
            "Bagi simpangan baku sampel dengan rata-rata setelah memeriksa rata-rata nol.",
            """
            import statistics

            def koefisien_variasi(data):
                m = statistics.mean(data)
                if m == 0:
                    return None
                return round(statistics.stdev(data) / m, 4)
            """,
        ),
        E(
            "A5-03-3-ex2",
            "sedang",
            """
            Tulis fungsi `zscore(data)` yang mengembalikan list z-score memakai simpangan baku populasi, dibulatkan 4 desimal. Bila simpangan baku nol kembalikan list nol.
            """,
            """
            import statistics

            def zscore(data):
                # TODO: implementasikan
                pass
            """,
            """
            assert zscore([1, 2, 3, 4, 5]) == [-1.4142, -0.7071, 0.0, 0.7071, 1.4142]
            assert zscore([5, 5, 5]) == [0.0, 0.0, 0.0]
            assert zscore([0, 10]) == [-1.0, 1.0]
            """,
            "Kurangi rata-rata lalu bagi simpangan baku populasi, tangani data konstan.",
            """
            import statistics

            def zscore(data):
                m = statistics.mean(data)
                s = statistics.pstdev(data)
                if s == 0:
                    return [0.0 for _ in data]
                return [round((x - m) / s, 4) + 0.0 for x in data]
            """,
        ),
        E(
            "A5-03-3-ex3",
            "sedang",
            """
            Tulis fungsi `minmax(data)` yang memetakan data ke rentang nol sampai satu dan mengembalikan list dibulatkan 4 desimal. Bila semua nilai sama kembalikan list nol.
            """,
            """
            def minmax(data):
                # TODO: implementasikan
                pass
            """,
            """
            assert minmax([1, 2, 3]) == [0.0, 0.5, 1.0]
            assert minmax([10, 20, 40]) == [0.0, 0.3333, 1.0]
            assert minmax([4, 4]) == [0.0, 0.0]
            """,
            "Kurangi minimum lalu bagi dengan rentang, tangani rentang nol.",
            """
            def minmax(data):
                lo, hi = min(data), max(data)
                if hi == lo:
                    return [0.0 for _ in data]
                return [round((x - lo) / (hi - lo), 4) for x in data]
            """,
        ),
        E(
            "A5-03-3-ex4",
            "menantang",
            """
            Tulis fungsi `proporsi_dalam(data, k)` yang mengembalikan proporsi data dengan `abs(x - rata) <= k * simpangan_baku_populasi`, dibulatkan 4 desimal.
            """,
            """
            def proporsi_dalam(data, k):
                # TODO: implementasikan
                pass
            """,
            """
            assert proporsi_dalam([1, 2, 3, 4, 5], 1) == 0.6
            assert proporsi_dalam([1, 2, 3, 4, 5], 2) == 1.0
            assert proporsi_dalam([2, 4, 4, 4, 5, 5, 7, 9], 1) == 0.75
            assert proporsi_dalam([2, 4, 4, 4, 5, 5, 7, 9], 2) == 1.0
            """,
            "Hitung rata-rata dan simpangan baku populasi lalu hitung porsi data dalam k simpangan baku.",
            """
            def proporsi_dalam(data, k):
                n = len(data)
                m = sum(data) / n
                s = (sum((x - m) ** 2 for x in data) / n) ** 0.5
                dalam = sum(1 for x in data if abs(x - m) <= k * s)
                return round(dalam / n, 4)
            """,
        ),
    ],
    [
        M("Membandingkan simpangan baku antar satuan berbeda.", "Pakai koefisien variasi atau z-score."),
        M("Menghitung parameter skala dari seluruh data sebelum membagi latih dan uji.", "Hitung dari data latih saja."),
        M("Memakai CV pada data dengan rata-rata mendekati nol.", "CV hanya untuk data rasio dengan rata-rata jauh dari nol."),
    ],
    [
        Q("Koefisien variasi adalah?", ["Simpangan baku / rata-rata", "Rata-rata / simpangan baku", "Varians / n", "IQR / median"], 0, "Sebaran relatif.", hint="Tanpa satuan."),
        Q("Z-score data standardisasi memiliki rata-rata?", ["Nol", "Satu", "Seratus", "Tak tentu"], 0, "Rata-rata nol dan simpangan baku satu.", hint="Pusat."),
        Q("Min-max memetakan ke?", ["0 sampai 1", "-1 sampai 1", "Rata-rata nol", "Tak terbatas"], 0, "Rentang tetap.", hint="Rentang."),
        Q("Chebyshev menjamin dalam 2 simpangan baku minimal?", ["75 persen", "95 persen", "50 persen", "99 persen"], 0, "1 - 1/4.", hint="1 - 1/k kuadrat."),
        Q("Parameter skala dihitung dari?", ["Data latih", "Data uji", "Seluruh data", "Acak"], 0, "Cegah kebocoran.", hint="Latih."),
    ],
    [
        "Koefisien variasi menyatakan sebaran relatif tanpa satuan.",
        "Z-score dan min-max menyamakan skala antar variabel.",
        "Chebyshev menjamin proporsi data tanpa asumsi distribusi.",
        "Parameter penskalaan dihitung dari data latih saja.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perhitungan yang cukup jelas dalam teks.", "brief": []}

write_module(
    "A5",
    3,
    "Ukuran penyebaran",
    105,
    [
        "Menghitung dan menafsirkan varians, simpangan baku, IQR, dan MAD",
        "Mendeteksi pencilan dengan aturan pagar Tukey",
        "Menstandardisasi dan menskalakan data dengan benar",
    ],
    [l1, l2, l3],
    video,
    REF,
)
