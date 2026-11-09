import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

SQL_PES = """
CREATE TABLE pesanan (id INTEGER PRIMARY KEY, pelanggan TEXT, kota TEXT, produk TEXT, jumlah INTEGER, total REAL, tanggal TEXT);
INSERT INTO pesanan VALUES
(1, 'Ani', 'Jakarta', 'Buku', 2, 24000, '2026-01-05'),
(2, 'Budi', 'Bandung', 'Tas', 1, 150000, '2026-01-09'),
(3, 'Citra', 'Jakarta', 'Pensil', 10, 25000, '2026-02-01'),
(4, 'Dewi', 'Surabaya', 'Botol', 3, 105000, '2026-02-14'),
(5, 'Eko', 'Bandung', 'Buku', 1, 12000, '2026-02-20'),
(6, 'Fajar', 'Jakarta', 'Tas', 2, 300000, '2026-03-03'),
(7, 'Gita', 'Medan', 'Penggaris', 5, 20000, '2026-03-15'),
(8, 'Hadi', 'Surabaya', 'Pensil', 20, 50000, '2026-03-22'),
(9, 'Indah', 'Bandung', 'Botol', NULL, 35000, '2026-04-01'),
(10, 'Joko', 'Jakarta', 'Buku', 4, 48000, '2026-04-10');
"""

SETUP = textwrap.indent("import sqlite3\n\nc = sqlite3.connect(':memory:')\nc.executescript('''" + SQL_PES + "''')\n", '            ')

FIX = textwrap.indent("import sqlite3\n\ndef _db():\n    c = sqlite3.connect(':memory:')\n    c.executescript('''" + textwrap.indent(SQL_PES, '    ') + "    ''')\n    return c\n\n", '            ')

l1 = lesson(
    "A6-03-1",
    "Fungsi agregat: COUNT, SUM, AVG, MIN, MAX",
    35,
    [
        "Meringkas seluruh tabel dengan fungsi agregat",
        "Menjelaskan perilaku agregat terhadap NULL dan tabel kosong",
        "Menghitung nilai unik dengan COUNT DISTINCT",
        "Menghindari kesalahan pembagian bulat pada rata-rata manual",
    ],
    [
        T("""
        ## Dari baris ke ringkasan

        Query yang kita tulis sejauh ini mengembalikan satu baris hasil untuk tiap baris sumber. **Fungsi agregat** mengubahnya: ia membaca banyak baris dan mengembalikan satu nilai ringkasan. Lima fungsi dasarnya adalah `COUNT` untuk banyak, `SUM` untuk jumlah, `AVG` untuk rata-rata, `MIN` untuk terkecil, dan `MAX` untuk terbesar.

        Agregasi adalah jantung analisis data dengan SQL. Alih-alih menarik jutaan baris ke Python lalu meringkasnya, kita meminta basis data meringkas langsung di sumbernya dan hanya mengirim hasil kecil yang kita butuhkan.
        """),
        C(
            SETUP + """
            q = 'SELECT COUNT(*), COUNT(jumlah), SUM(total), AVG(total), MIN(total), MAX(total) FROM pesanan'
            print(c.execute(q).fetchone())
            """,
            """
            (10, 9, 769000.0, 76900.0, 12000.0, 300000.0)
            """,
            """
            Sepuluh pesanan dengan sembilan jumlah terisi, total keseluruhan 769.000, rata-rata 76.900, terkecil 12.000, dan terbesar 300.000.
            """,
            filename="agregat_dasar.py",
        ),
        T("""
        ## COUNT dalam tiga bentuk

        `COUNT(*)` menghitung semua baris. `COUNT(kolom)` menghitung baris dengan kolom tidak `NULL`. `COUNT(DISTINCT kolom)` menghitung nilai unik non-NULL. Ketiganya menjawab pertanyaan berbeda: berapa baris, berapa baris punya data, dan berapa nilai berbeda.

        Selisih `COUNT(*)` dan `COUNT(kolom)` adalah banyak nilai hilang, pemeriksaan kualitas data tercepat yang dapat dilakukan. Pada tabel kita, sepuluh pesanan tetapi hanya sembilan memiliki jumlah, sehingga satu nilai hilang.
        """),
        T("""
        ## Agregat mengabaikan NULL

        Semua agregat kecuali `COUNT(*)` melewati nilai `NULL`. `AVG(jumlah)` membagi jumlah yang ada dengan banyak baris yang terisi, bukan dengan semua baris. Perilaku ini mirip pandas dan biasanya yang diinginkan, tetapi bisa menyesatkan bila nilai hilang berarti sesuatu, misalnya jumlah nol.

        Bila ingin memperlakukan `NULL` sebagai nol, ganti dulu dengan `COALESCE` di dalam agregat: `AVG(COALESCE(jumlah, 0))`. Itu mengubah makna hasil, jadi pastikan sesuai pertanyaan analisismu.
        """),
        C(
            SETUP + """
            q = 'SELECT SUM(jumlah), round(AVG(jumlah), 4), round(AVG(COALESCE(jumlah, 0)), 4) FROM pesanan'
            print(c.execute(q).fetchone())
            q = 'SELECT COUNT(DISTINCT kota), COUNT(DISTINCT produk) FROM pesanan'
            print(c.execute(q).fetchone())
            """,
            """
            (48, 5.3333, 4.8)
            (4, 5)
            """,
            """
            Rata-rata tanpa NULL lima koma tiga tiga, dengan NULL dianggap nol empat koma delapan, dan ada empat kota serta lima produk unik.
            """,
            filename="agregat_null.py",
        ),
        T("""
        ## Tabel kosong

        Agregat pada himpunan kosong memiliki perilaku khusus yang sering mengejutkan. `COUNT` mengembalikan nol, tetapi `SUM`, `AVG`, `MIN`, dan `MAX` mengembalikan `NULL`, bukan nol. Jumlah tanpa suku secara matematis nol, tetapi SQL memilih `NULL` untuk menandakan tidak ada data.

        Kode yang memakai hasilnya harus siap menerima `NULL`. Bungkus dengan `COALESCE(SUM(...), 0)` bila kamu menginginkan nol. Kasus tepi ini sering lolos dari pengujian karena data uji jarang kosong.
        """),
        C(
            SETUP + """
            q = "SELECT SUM(total), AVG(total), COUNT(*) FROM pesanan WHERE kota = 'Tidak ada'"
            print(c.execute(q).fetchone())
            q = "SELECT COALESCE(SUM(total), 0) FROM pesanan WHERE kota = 'Tidak ada'"
            print(c.execute(q).fetchone())
            """,
            """
            (None, None, 0)
            (0,)
            """,
            """
            Himpunan kosong memberi NULL untuk jumlah dan rata-rata tetapi nol untuk COUNT, dan COALESCE mengubah NULL menjadi nol.
            """,
            filename="agregat_kosong.py",
        ),
        T("""
        ## Jebakan pembagian bulat

        Menghitung rata-rata manual dengan `SUM(x) / COUNT(*)` rawan dua kesalahan. Pertama, bila `x` bilangan bulat maka pembagian bulat memotong pecahan. Kedua, `COUNT(*)` menghitung baris `NULL` sehingga penyebutnya lebih besar daripada yang dipakai `AVG`.

        Pada jumlah pesanan, `SUM(jumlah) / COUNT(*)` menghasilkan 4, sedangkan rata-rata yang benar 5,3333. Pakai `AVG` bila ingin perilaku standar, dan bila menulis manual kalikan dengan `1.0` serta pakai `COUNT(kolom)` sebagai penyebut.
        """),
        C(
            SETUP + """
            print(c.execute('SELECT SUM(jumlah) / COUNT(*) FROM pesanan').fetchone())
            print(c.execute('SELECT round(SUM(jumlah) * 1.0 / COUNT(jumlah), 4) FROM pesanan').fetchone())
            """,
            """
            (4,)
            (5.3333,)
            """,
            """
            Pembagian bulat dengan COUNT bintang memberi empat, sedangkan pembagian desimal dengan COUNT kolom memberi rata-rata yang benar.
            """,
            filename="rata_manual.py",
        ),
        T("""
        ## Agregat dengan filter

        Agregat bekerja pada baris yang lolos `WHERE`. `SELECT SUM(total) FROM pesanan WHERE kota = 'Jakarta'` menjumlahkan hanya pesanan Jakarta. Karena `WHERE` dievaluasi lebih dulu, agregat tidak pernah melihat baris yang tersaring.

        Kita juga dapat menaruh beberapa agregat dalam satu `SELECT` untuk mendapat ringkasan lengkap dalam satu lintasan data. Satu query dengan lima agregat jauh lebih efisien daripada lima query terpisah yang masing-masing membaca tabel sendiri.
        """),
        K(
            "tip",
            """
            Bandingkan COUNT bintang dengan COUNT kolom pada setiap kolom penting. Selisihnya langsung memberi jumlah nilai hilang.
            """,
            title="Cek nilai hilang",
        ),
        T("""
        ## Agregat dan tipe data

        Hasil agregat mengikuti tipe masukannya dengan beberapa kejutan. `SUM` pada kolom bulat menghasilkan bilangan bulat, sedangkan `AVG` selalu menghasilkan pecahan. `MIN` dan `MAX` bekerja pada teks juga, menurut urutan abjad, sehingga `MAX(tanggal)` memberi tanggal terbaru bila formatnya ISO.

        Pada kolom teks yang berisi angka, `SUM` mengonversinya diam-diam, dan teks non-numerik dianggap nol. Pastikan tipe kolom benar sejak awal agar agregat tidak menghasilkan angka yang tampak sah tetapi keliru.
        """),
        T("""
        ## Memeriksa hasil agregat

        Periksa agregat dengan tiga cara cepat. Bandingkan dengan perhitungan manual pada sampel kecil. Pastikan `COUNT(*)` sesuai ekspektasi setelah filter. Periksa nilai ekstrem dengan `MIN` dan `MAX` untuk menemukan pencilan atau kode khusus seperti 9999 yang berarti hilang.

        Kebiasaan menjalankan satu query ringkasan sebelum analisis mendalam, berisi COUNT, COUNT kolom, MIN, MAX, dan AVG, mengungkap sebagian besar masalah data dalam hitungan detik dan menghemat berjam-jam penelusuran kemudian.
        """),
        E(
            "A6-03-1-ex1",
            "mudah",
            """
            Tulis fungsi `statistik_total(c)` yang mengembalikan dictionary dengan kunci `n`, `jumlah`, `rata`, `min`, `max` dari kolom `total` seluruh tabel pesanan. `rata` dibulatkan 4 desimal. Untuk tabel kosong, semua selain `n` bernilai `None`.
            """,
            """
            import sqlite3

            def statistik_total(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert statistik_total(c) == {'n': 10, 'jumlah': 769000.0, 'rata': 76900.0, 'min': 12000.0, 'max': 300000.0}
            c.execute("INSERT INTO pesanan VALUES (11, 'Kiki', 'Bogor', 'Buku', 1, 100000, '2026-05-01')")
            assert statistik_total(c) == {'n': 11, 'jumlah': 869000.0, 'rata': 79000.0, 'min': 12000.0, 'max': 300000.0}
            c.execute('DELETE FROM pesanan')
            assert statistik_total(c) == {'n': 0, 'jumlah': None, 'rata': None, 'min': None, 'max': None}
            """,
            "Jalankan satu query dengan lima agregat lalu susun dictionary dari barisnya.",
            """
            import sqlite3

            def statistik_total(c):
                q = 'SELECT COUNT(*), SUM(total), round(AVG(total), 4), MIN(total), MAX(total) FROM pesanan'
                n, s, a, lo, hi = c.execute(q).fetchone()
                return {'n': n, 'jumlah': s, 'rata': a, 'min': lo, 'max': hi}
            """,
        ),
        E(
            "A6-03-1-ex2",
            "sedang",
            """
            Tulis fungsi `rata_jumlah(c)` yang mengembalikan rata-rata kolom `jumlah` dengan `AVG` (NULL diabaikan) dibulatkan 4 desimal, atau `None` bila tidak ada nilai.
            """,
            """
            import sqlite3

            def rata_jumlah(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert rata_jumlah(c) == 5.3333
            c.execute('UPDATE pesanan SET jumlah = 1 WHERE id = 9')
            assert rata_jumlah(c) == 4.9
            c.execute('UPDATE pesanan SET jumlah = NULL')
            assert rata_jumlah(c) is None
            """,
            "Pakai AVG pada kolom jumlah dan bulatkan di SQL.",
            """
            import sqlite3

            def rata_jumlah(c):
                return c.execute('SELECT round(AVG(jumlah), 4) FROM pesanan').fetchone()[0]
            """,
        ),
        E(
            "A6-03-1-ex3",
            "sedang",
            """
            Tulis fungsi `jumlah_unik(c, kolom)` yang mengembalikan banyak nilai unik non-NULL pada kolom tabel pesanan memakai `COUNT(DISTINCT ...)`.
            """,
            """
            import sqlite3

            def jumlah_unik(c, kolom):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert jumlah_unik(c, 'kota') == 4
            assert jumlah_unik(c, 'produk') == 5
            assert jumlah_unik(c, 'pelanggan') == 10
            assert jumlah_unik(c, 'jumlah') == 7
            """,
            "Susun COUNT DISTINCT dengan nama kolom pada f-string.",
            """
            import sqlite3

            def jumlah_unik(c, kolom):
                return c.execute(f'SELECT COUNT(DISTINCT {kolom}) FROM pesanan').fetchone()[0]
            """,
        ),
        E(
            "A6-03-1-ex4",
            "menantang",
            """
            Tulis fungsi `rata_naif_vs_benar(c)` yang mengembalikan tuple `(naif, benar)`: `naif` adalah `SUM(jumlah) * 1.0 / COUNT(*)` dan `benar` adalah `AVG(jumlah)`, keduanya dibulatkan 4 desimal di SQL.
            """,
            """
            import sqlite3

            def rata_naif_vs_benar(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert rata_naif_vs_benar(c) == (4.8, 5.3333)
            c.execute('UPDATE pesanan SET jumlah = 2 WHERE id = 9')
            assert rata_naif_vs_benar(c) == (5.0, 5.0)
            c.execute('UPDATE pesanan SET jumlah = NULL')
            assert rata_naif_vs_benar(c) == (None, None)
            """,
            "Hitung dua ekspresi dalam satu SELECT dan bulatkan keduanya.",
            """
            import sqlite3

            def rata_naif_vs_benar(c):
                q = 'SELECT round(SUM(jumlah) * 1.0 / COUNT(*), 4), round(AVG(jumlah), 4) FROM pesanan'
                return c.execute(q).fetchone()
            """,
        ),
    ],
    [
        M("Mengira SUM pada himpunan kosong bernilai nol.", "SUM kosong bernilai NULL, pakai COALESCE."),
        M("Menghitung rata-rata manual dengan SUM dibagi COUNT bintang.", "Pakai AVG atau COUNT kolom dan kalikan 1.0."),
        M("Mengabaikan selisih COUNT bintang dan COUNT kolom.", "Selisih itu adalah nilai hilang."),
    ],
    [
        Q("COUNT(kolom) menghitung?", ["Baris non-NULL", "Semua baris", "Nilai unik", "Kolom"], 0, "Mengabaikan NULL.", hint="Non-NULL."),
        Q("SUM pada himpunan kosong?", ["NULL", "0", "Error", "1"], 0, "NULL.", hint="Tidak ada data."),
        Q("AVG mengabaikan?", ["NULL", "Nol", "Negatif", "Duplikat"], 0, "NULL dilewati.", hint="Hilang."),
        Q("COUNT(DISTINCT x) menghitung?", ["Nilai unik non-NULL", "Semua", "NULL", "Duplikat"], 0, "Unik.", hint="Unik."),
        Q("SUM(int)/COUNT(*) pada integer?", ["Pembagian bulat", "Desimal", "NULL", "Error"], 0, "Memotong pecahan.", hint="Bulat."),
    ],
    [
        "Agregat meringkas banyak baris menjadi satu nilai.",
        "Agregat melewati NULL kecuali COUNT bintang.",
        "SUM, AVG, MIN, MAX pada himpunan kosong bernilai NULL.",
        "Hindari pembagian bulat pada rata-rata manual.",
    ],
    [],
)

l2 = lesson(
    "A6-03-2",
    "GROUP BY dan HAVING",
    35,
    [
        "Meringkas per kelompok dengan GROUP BY",
        "Memfilter kelompok dengan HAVING dan membedakannya dari WHERE",
        "Mengelompokkan menurut beberapa kolom",
        "Mengurutkan dan membatasi hasil kelompok",
    ],
    [
        T("""
        ## Meringkas per kelompok

        Agregat tanpa pengelompokan meringkas seluruh tabel menjadi satu baris. `GROUP BY` membagi baris menjadi kelompok berdasarkan nilai kolom, lalu menerapkan agregat pada tiap kelompok sehingga menghasilkan satu baris per kelompok. Ini padanan SQL dari `groupby` pandas dan pola split-apply-combine.

        Pertanyaan seperti total penjualan per kota, jumlah pesanan per bulan, dan rata-rata nilai per kelas semuanya diselesaikan dengan `GROUP BY`. Pola ini mungkin konstruksi SQL yang paling sering kamu tulis sebagai analis.
        """),
        C(
            SETUP + """
            q = 'SELECT kota, COUNT(*), SUM(total) FROM pesanan GROUP BY kota ORDER BY kota'
            for baris in c.execute(q):
                print(baris)
            """,
            """
            ('Bandung', 3, 197000.0)
            ('Jakarta', 4, 397000.0)
            ('Medan', 1, 20000.0)
            ('Surabaya', 2, 155000.0)
            """,
            """
            Setiap kota menjadi satu baris hasil dengan banyak pesanan dan total nilainya.
            """,
            filename="group_by.py",
        ),
        T("""
        ## Aturan kolom di SELECT

        Pada query dengan `GROUP BY`, setiap kolom di `SELECT` harus berupa kolom pengelompokan atau berada di dalam fungsi agregat. Alasannya logis: bila kamu mengelompokkan menurut kota lalu meminta nama pelanggan, basis data tidak tahu pelanggan mana yang harus ditampilkan dari empat pelanggan Jakarta.

        PostgreSQL menolak query semacam itu dengan galat. SQLite dan MySQL lama mengizinkannya dan mengambil nilai sembarang dari kelompok, sumber hasil yang tidak dapat diprediksi. Anggap itu kesalahan dan jangan pernah memanfaatkannya.
        """),
        T("""
        ## WHERE atau HAVING

        `WHERE` menyaring baris sebelum pengelompokan, sedangkan `HAVING` menyaring kelompok setelah agregasi. Untuk kota dengan total pesanan di atas 100.000 kita memakai `HAVING SUM(total) > 100000` karena kondisinya bergantung pada hasil agregat, sesuatu yang belum ada saat `WHERE` dievaluasi.

        Untuk menyaring pesanan tertentu sebelum diringkas, misalnya hanya pesanan di atas 30.000, kita memakai `WHERE`. Aturan praktis: bila kondisi mengacu pada nilai baris, pakai `WHERE`. Bila mengacu pada agregat, pakai `HAVING`. Menaruh yang bisa di `WHERE` ke `HAVING` boros karena baris diproses dulu baru dibuang.
        """),
        C(
            SETUP + """
            q = 'SELECT kota, SUM(total) FROM pesanan GROUP BY kota HAVING SUM(total) > 100000 ORDER BY kota'
            print(c.execute(q).fetchall())
            q = 'SELECT kota, COUNT(*) FROM pesanan WHERE total > 30000 GROUP BY kota ORDER BY kota'
            print(c.execute(q).fetchall())
            """,
            """
            [('Bandung', 197000.0), ('Jakarta', 397000.0), ('Surabaya', 155000.0)]
            [('Bandung', 2), ('Jakarta', 2), ('Surabaya', 2)]
            """,
            """
            HAVING menyaring kota menurut total agregat, sedangkan WHERE menyaring pesanan sebelum dihitung per kota.
            """,
            filename="having_where.py",
        ),
        T("""
        ## Banyak kolom pengelompokan

        Kita dapat mengelompokkan menurut lebih dari satu kolom: `GROUP BY kota, produk` membuat satu kelompok untuk setiap kombinasi unik kota dan produk. Hasilnya lebih rinci, dan jumlah kelompok bisa melonjak karena kombinasinya mengalikan banyak nilai tiap kolom.

        Makin rinci pengelompokan, makin kecil tiap kelompok, dan makin tidak stabil ringkasan statistiknya. Pilih tingkat rincian sesuai pertanyaan, dan selalu sertakan banyak baris per kelompok agar pembaca dapat menilai keandalannya.
        """),
        C(
            SETUP + """
            q = 'SELECT kota, produk, COUNT(*) FROM pesanan GROUP BY kota, produk ORDER BY kota, produk'
            hasil = c.execute(q).fetchall()
            print(len(hasil))
            print(hasil[0], hasil[3])
            """,
            """
            9
            ('Bandung', 'Botol', 1) ('Jakarta', 'Buku', 2)
            """,
            """
            Sembilan kombinasi kota dan produk unik, dan Jakarta memiliki dua pesanan buku.
            """,
            filename="group_by_banyak.py",
        ),
        T("""
        ## Mengurutkan dan membatasi kelompok

        Hasil `GROUP BY` bisa diurutkan menurut agregat memakai alias: `SELECT kota, COUNT(*) AS n ... ORDER BY n DESC`. Menambah `LIMIT` mengambil kelompok teratas. Karena alias dikenali di `ORDER BY`, query tetap mudah dibaca tanpa mengulang ekspresi agregat.

        Seperti biasa, tambahkan pemutus seri agar hasil deterministik. Peringkat kota menurut jumlah pesanan sering memiliki seri, dan tanpa pemutus seri dua eksekusi bisa menghasilkan urutan berbeda.
        """),
        C(
            SETUP + """
            q = 'SELECT kota, COUNT(*) AS n FROM pesanan GROUP BY kota ORDER BY n DESC, kota LIMIT 2'
            print(c.execute(q).fetchall())
            q = 'SELECT kota, round(AVG(total), 2) FROM pesanan GROUP BY kota HAVING COUNT(*) > 1 ORDER BY kota'
            print(c.execute(q).fetchall())
            """,
            """
            [('Jakarta', 4), ('Bandung', 3)]
            [('Bandung', 65666.67), ('Jakarta', 99250.0), ('Surabaya', 77500.0)]
            """,
            """
            Jakarta dan Bandung memiliki pesanan terbanyak, dan kota dengan satu pesanan disaring dari rata-rata dengan HAVING.
            """,
            filename="urut_kelompok.py",
        ),
        T("""
        ## Menggabungkan nilai dalam kelompok

        Fungsi `group_concat` di SQLite, `string_agg` di PostgreSQL, menggabungkan nilai teks tiap kelompok menjadi satu string, misalnya daftar nama pelanggan per kota. Berguna untuk laporan ringkas, tetapi urutan nilai dalam string tidak dijamin kecuali diatur khusus.

        Gunakan dengan hemat. Menyimpan daftar dalam satu sel menyulitkan analisis lanjutan, jadi pakai hanya untuk tampilan akhir, bukan sebagai langkah antara dalam pipeline analisis.
        """),
        K(
            "warn",
            """
            Setiap kolom di SELECT harus berada di GROUP BY atau di dalam agregat. Jangan memanfaatkan toleransi SQLite yang mengambil nilai sembarang dari kelompok.
            """,
            title="Kolom tak teragregasi",
        ),
        T("""
        ## Pola umum per kelompok

        Beberapa pola GROUP BY muncul terus-menerus. Penghitungan frekuensi: `SELECT kolom, COUNT(*) FROM tabel GROUP BY kolom` adalah padanan `value_counts` pandas. Pencarian duplikat: kelompokkan menurut kolom yang seharusnya unik dan tampilkan kelompok dengan `HAVING COUNT(*) > 1`. Ringkasan lengkap per segmen: satu baris dengan COUNT, SUM, AVG, MIN, dan MAX.

        Menguasai ketiga pola ini sudah menyelesaikan sebagian besar pertanyaan analisis harian. Sisanya adalah variasi dengan kondisi dan kolom berbeda.
        """),
        T("""
        ## Urutan evaluasi lengkap

        Dengan GROUP BY dan HAVING, urutan evaluasi logis menjadi FROM, WHERE, GROUP BY, HAVING, SELECT, DISTINCT, ORDER BY, lalu LIMIT. Urutan ini menjelaskan banyak aturan: WHERE tidak boleh memakai agregat karena kelompok belum terbentuk, HAVING boleh karena sudah terbentuk, dan ORDER BY boleh memakai alias karena SELECT sudah dievaluasi.

        Saat query memberi galat atau hasil mengejutkan, telusuri urutan ini selangkah demi selangkah. Hampir semua kebingungan SQL tingkat dasar berasal dari lupa pada urutan evaluasi.
        """),
        E(
            "A6-03-2-ex1",
            "mudah",
            """
            Tulis fungsi `total_per_kota(c)` yang mengembalikan dictionary `{kota: jumlah total}` dari tabel pesanan.
            """,
            """
            import sqlite3

            def total_per_kota(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert total_per_kota(c) == {'Bandung': 197000.0, 'Jakarta': 397000.0, 'Medan': 20000.0, 'Surabaya': 155000.0}
            c.execute("INSERT INTO pesanan VALUES (11, 'Kiki', 'Bogor', 'Buku', 1, 100000, '2026-05-01')")
            assert total_per_kota(c)['Bogor'] == 100000.0
            c.execute('DELETE FROM pesanan')
            assert total_per_kota(c) == {}
            """,
            "Kelompokkan menurut kota dan jumlahkan total lalu ubah ke dictionary.",
            """
            import sqlite3

            def total_per_kota(c):
                return dict(c.execute('SELECT kota, SUM(total) FROM pesanan GROUP BY kota').fetchall())
            """,
        ),
        E(
            "A6-03-2-ex2",
            "sedang",
            """
            Tulis fungsi `kota_besar(c, batas)` yang mengembalikan list nama kota dengan total pesanan lebih dari `batas`, terurut abjad, memakai `HAVING`.
            """,
            """
            import sqlite3

            def kota_besar(c, batas):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert kota_besar(c, 100000) == ['Bandung', 'Jakarta', 'Surabaya']
            assert kota_besar(c, 200000) == ['Jakarta']
            assert kota_besar(c, 1000000) == []
            assert kota_besar(c, 0) == ['Bandung', 'Jakarta', 'Medan', 'Surabaya']
            """,
            "Pakai HAVING dengan SUM total dan parameter batas.",
            """
            import sqlite3

            def kota_besar(c, batas):
                q = 'SELECT kota FROM pesanan GROUP BY kota HAVING SUM(total) > ? ORDER BY kota'
                return [r[0] for r in c.execute(q, (batas,)).fetchall()]
            """,
        ),
        E(
            "A6-03-2-ex3",
            "sedang",
            """
            Tulis fungsi `pesanan_per_kota_produk(c)` yang mengembalikan list tuple `(kota, produk, banyak)` terurut menurut kota lalu produk.
            """,
            """
            import sqlite3

            def pesanan_per_kota_produk(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            h = pesanan_per_kota_produk(c)
            assert len(h) == 9
            assert h[0] == ('Bandung', 'Botol', 1)
            assert ('Jakarta', 'Buku', 2) in h
            assert h == sorted(h)
            """,
            "Kelompokkan menurut dua kolom dan urutkan menurut keduanya.",
            """
            import sqlite3

            def pesanan_per_kota_produk(c):
                q = 'SELECT kota, produk, COUNT(*) FROM pesanan GROUP BY kota, produk ORDER BY kota, produk'
                return c.execute(q).fetchall()
            """,
        ),
        E(
            "A6-03-2-ex4",
            "menantang",
            """
            Tulis fungsi `rata_kota_min_n(c, n_min)` yang mengembalikan dictionary `{kota: rata-rata total dibulatkan 2 desimal}` hanya untuk kota yang memiliki paling sedikit `n_min` pesanan.
            """,
            """
            import sqlite3

            def rata_kota_min_n(c, n_min):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert rata_kota_min_n(c, 2) == {'Bandung': 65666.67, 'Jakarta': 99250.0, 'Surabaya': 77500.0}
            assert rata_kota_min_n(c, 3) == {'Bandung': 65666.67, 'Jakarta': 99250.0}
            assert rata_kota_min_n(c, 5) == {}
            assert rata_kota_min_n(c, 1)['Medan'] == 20000.0
            """,
            "Pakai HAVING COUNT bintang dan bulatkan AVG di SQL.",
            """
            import sqlite3

            def rata_kota_min_n(c, n_min):
                q = 'SELECT kota, round(AVG(total), 2) FROM pesanan GROUP BY kota HAVING COUNT(*) >= ?'
                return dict(c.execute(q, (n_min,)).fetchall())
            """,
        ),
    ],
    [
        M("Memasukkan kolom tak teragregasi ke SELECT.", "Masukkan ke GROUP BY atau agregasi."),
        M("Menaruh kondisi baris di HAVING.", "Pakai WHERE untuk kondisi baris."),
        M("Melaporkan rata-rata kelompok tanpa banyak baris.", "Sertakan COUNT per kelompok."),
    ],
    [
        Q("GROUP BY menghasilkan?", ["Satu baris per kelompok", "Satu baris per data", "Satu angka", "Kosong"], 0, "Per kelompok.", hint="Kelompok."),
        Q("HAVING menyaring?", ["Kelompok", "Baris sebelum agregasi", "Kolom", "Tabel"], 0, "Setelah agregasi.", hint="Agregat."),
        Q("WHERE dievaluasi?", ["Sebelum GROUP BY", "Setelah GROUP BY", "Setelah HAVING", "Terakhir"], 0, "Menyaring baris.", hint="Sebelum."),
        Q("Dua kolom di GROUP BY menghasilkan?", ["Satu kelompok per kombinasi", "Dua tabel", "Satu kelompok", "Error"], 0, "Kombinasi unik.", hint="Kombinasi."),
        Q("Alias agregat dapat dipakai di?", ["ORDER BY", "WHERE", "FROM", "GROUP BY"], 0, "Dievaluasi setelah SELECT.", hint="Setelah."),
    ],
    [
        "GROUP BY meringkas data per kelompok menjadi satu baris tiap kelompok.",
        "WHERE menyaring baris dan HAVING menyaring kelompok.",
        "Kolom SELECT harus berada di GROUP BY atau dalam agregat.",
        "Sertakan ukuran kelompok bersama ringkasan.",
    ],
    [],
)

l3 = lesson(
    "A6-03-3",
    "Agregasi bersyarat dan persentase",
    35,
    [
        "Meringkas per periode waktu dengan substr pada tanggal ISO",
        "Menghitung agregasi bersyarat dengan SUM dan CASE",
        "Menghitung persentase dari total dengan subquery skalar",
        "Mengambil kelompok teratas dengan aturan pemutus seri",
    ],
    [
        T("""
        ## Ringkasan per periode

        Analisis bisnis hampir selalu per periode: harian, mingguan, bulanan. Karena tanggal ISO adalah teks `YYYY-MM-DD`, kita dapat mengambil bulan dengan `substr(tanggal, 1, 7)` yang menghasilkan `YYYY-MM`. Mengelompokkan menurut ekspresi itu menghasilkan ringkasan bulanan.

        SQLite juga menyediakan `strftime('%Y-%m', tanggal)` yang lebih ekspresif dan mengerti format tanggal sungguhan. Pelajaran khusus tanggal dan teks membahasnya. Untuk format ISO sederhana, `substr` sudah memadai dan cepat.
        """),
        C(
            SETUP + """
            q = 'SELECT substr(tanggal, 1, 7) AS bulan, SUM(total) FROM pesanan GROUP BY bulan ORDER BY bulan'
            print(c.execute(q).fetchall())
            """,
            """
            [('2026-01', 174000.0), ('2026-02', 142000.0), ('2026-03', 370000.0), ('2026-04', 83000.0)]
            """,
            """
            Total pesanan per bulan memperlihatkan puncak pada Maret sebesar 370.000.
            """,
            filename="per_bulan.py",
        ),
        T("""
        ## Alias di GROUP BY

        Pada contoh, kita mengelompokkan menurut alias `bulan`. SQLite dan PostgreSQL mengizinkannya, tetapi standar SQL ketat dan beberapa basis data tidak. Bila perlu portabilitas, ulangi ekspresi di `GROUP BY` atau bungkus dalam subquery. Karena `GROUP BY` dievaluasi sebelum `SELECT`, pengizinan alias di sana adalah kemudahan, bukan aturan baku.

        Pada hasil per periode, periode tanpa data tidak muncul sama sekali. Untuk laporan yang membutuhkan semua bulan termasuk yang kosong, kita membutuhkan tabel kalender dan JOIN, topik modul berikutnya.
        """),
        T("""
        ## Agregasi bersyarat

        `SUM(CASE WHEN kondisi THEN 1 ELSE 0 END)` menghitung baris yang memenuhi kondisi dalam tiap kelompok. Dengan beberapa ekspresi seperti itu kita membangun tabel silang dalam satu query, misalnya jumlah pesanan besar dan kecil per kota berdampingan, tanpa perlu query terpisah.

        Pola ini disebut agregasi bersyarat atau pivot manual. Ia menggantikan banyak query dengan satu lintasan data dan sangat populer di laporan. Kondisinya bebas, sehingga kita dapat menghitung proporsi, rata-rata bersyarat, dan penanda lain.
        """),
        C(
            SETUP + """
            q = '''
            SELECT kota,
                   SUM(CASE WHEN total >= 100000 THEN 1 ELSE 0 END) AS besar,
                   SUM(CASE WHEN total < 100000 THEN 1 ELSE 0 END) AS kecil
            FROM pesanan GROUP BY kota ORDER BY kota
            '''
            print(c.execute(q).fetchall())
            """,
            """
            [('Bandung', 1, 2), ('Jakarta', 1, 3), ('Medan', 0, 1), ('Surabaya', 1, 1)]
            """,
            """
            Pesanan besar dan kecil dihitung berdampingan untuk tiap kota dalam satu query.
            """,
            filename="agregasi_bersyarat.py",
        ),
        T("""
        ## Persentase dari total

        Untuk menghitung kontribusi tiap kelompok pada total, kita membutuhkan total keseluruhan sebagai penyebut. Cara paling sederhana memakai subquery skalar: `(SELECT SUM(total) FROM pesanan)`, query kecil yang mengembalikan satu nilai dan dapat dipakai seperti konstanta di dalam query utama.

        Kalikan dengan `100.0` agar pembagian menjadi desimal. Hasilnya persentase yang berjumlah sekitar seratus. Pembulatan membuat jumlah bisa menyimpang sedikit dari seratus, dan itu wajar bila ditulis dengan jelas.
        """),
        C(
            SETUP + """
            q = '''
            SELECT kota, round(100.0 * SUM(total) / (SELECT SUM(total) FROM pesanan), 2)
            FROM pesanan GROUP BY kota ORDER BY kota
            '''
            hasil = c.execute(q).fetchall()
            print(hasil)
            print(round(sum(p for _, p in hasil), 2))
            """,
            """
            [('Bandung', 25.62), ('Jakarta', 51.63), ('Medan', 2.6), ('Surabaya', 20.16)]
            100.01
            """,
            """
            Jakarta menyumbang lebih dari separuh total, dan jumlah persentase bulat menyimpang sedikit menjadi seratus koma nol satu.
            """,
            filename="persen_total.py",
        ),
        T("""
        ## Rentang dan selisih per kelompok

        Agregat dapat dikombinasikan dalam ekspresi: `MAX(total) - MIN(total)` memberi rentang per kelompok, dan `SUM(total) * 1.0 / COUNT(*)` memberi rata-rata manual. Karena agregat adalah nilai biasa setelah dihitung, kita boleh memakainya dalam aritmetika, `CASE`, dan fungsi lain.

        Namun agregat tidak boleh bersarang langsung seperti `AVG(SUM(x))`. Untuk agregasi dua tingkat, bungkus tingkat pertama dalam subquery atau CTE, dua konstruksi yang dibahas pada modul subquery.
        """),
        T("""
        ## Kelompok teratas

        Untuk mengambil kelompok teratas, gabungkan `GROUP BY`, `ORDER BY` pada agregat, dan `LIMIT`: tiga kota dengan pesanan terbanyak, lima produk dengan pendapatan terbesar. Pastikan aturan pemutus seri eksplisit, misalnya nama kelompok, agar hasil stabil bila beberapa kelompok memiliki nilai sama.

        Bila yang kamu butuhkan adalah teratas per kelompok, misalnya produk terlaris di tiap kota, `LIMIT` biasa tidak cukup. Itu memerlukan fungsi window dengan peringkat, yang dibahas pada modul window function.
        """),
        K(
            "tip",
            """
            Untuk laporan silang, gunakan SUM dengan CASE di dalam GROUP BY. Satu query menggantikan banyak query terpisah.
            """,
            title="Pivot manual",
        ),
        T("""
        ## Tren dan perbandingan antar periode

        Ringkasan per bulan menjadi dasar analisis tren. Dari tabel bulanan kita dapat menghitung pertumbuhan bulan ke bulan, rata-rata bergerak, dan musiman. Pertumbuhan membutuhkan nilai bulan sebelumnya pada baris yang sama, yang dikerjakan dengan fungsi window atau dengan menggabungkan tabel ke dirinya sendiri.

        Untuk sekarang, cukup ingat bahwa hasil agregasi per periode adalah deret waktu yang siap dimasukkan ke pandas untuk analisis dan visualisasi lebih lanjut dengan alat yang telah dipelajari di modul sebelumnya.
        """),
        T("""
        ## Membaca persentase dengan hati-hati

        Persentase dari total mudah menyesatkan bila penyebutnya tidak jelas. Dari total apa? Seluruh tabel, hanya periode tertentu, atau hanya kelompok yang lolos filter? Subquery skalar di atas memakai seluruh tabel tanpa filter, sehingga bila query utama memfilter baris, persentasenya tidak berjumlah seratus.

        Samakan filter pada penyebut dan pembilang bila ingin persentase di dalam subset. Dan selalu tuliskan penyebut dalam judul laporan agar pembaca memahami angka itu persentase dari apa.
        """),
        T("""
        ## Kapan memakai SQL dan kapan pandas

        Agregasi di SQL unggul bila data besar dan berada di basis data: hanya hasil ringkas yang berpindah ke Python. Pandas unggul untuk eksplorasi interaktif pada data yang muat di memori, dengan fleksibilitas transformasi dan visualisasi. Praktik umum adalah menggabungkan keduanya: SQL meringkas, pandas menganalisis dan menggambar.

        Menguasai keduanya membuatmu bebas memilih alat yang paling sesuai. Pertanyaan yang sama sering dapat dijawab dengan salah satunya, dan pindah antar alat adalah keterampilan inti analis data.
        """),
        E(
            "A6-03-3-ex1",
            "mudah",
            """
            Tulis fungsi `total_per_bulan(c)` yang mengembalikan list tuple `(bulan, total)` dengan `bulan` berformat `YYYY-MM` diambil dari `tanggal`, terurut menurut bulan.
            """,
            """
            import sqlite3

            def total_per_bulan(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert total_per_bulan(c) == [('2026-01', 174000.0), ('2026-02', 142000.0), ('2026-03', 370000.0), ('2026-04', 83000.0)]
            c.execute("INSERT INTO pesanan VALUES (11, 'Kiki', 'Bogor', 'Buku', 1, 1000, '2026-05-01')")
            assert total_per_bulan(c)[-1] == ('2026-05', 1000.0)
            c.execute('DELETE FROM pesanan')
            assert total_per_bulan(c) == []
            """,
            "Ambil tujuh karakter pertama tanggal dan kelompokkan menurutnya.",
            """
            import sqlite3

            def total_per_bulan(c):
                q = 'SELECT substr(tanggal, 1, 7) AS bulan, SUM(total) FROM pesanan GROUP BY bulan ORDER BY bulan'
                return c.execute(q).fetchall()
            """,
        ),
        E(
            "A6-03-3-ex2",
            "sedang",
            """
            Tulis fungsi `besar_kecil_per_kota(c, batas)` yang mengembalikan dictionary `{kota: (besar, kecil)}` dengan `besar` banyak pesanan bertotal sama dengan atau di atas `batas` dan `kecil` banyak pesanan di bawahnya, memakai `SUM` dan `CASE`.
            """,
            """
            import sqlite3

            def besar_kecil_per_kota(c, batas):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert besar_kecil_per_kota(c, 100000) == {'Bandung': (1, 2), 'Jakarta': (1, 3), 'Medan': (0, 1), 'Surabaya': (1, 1)}
            assert besar_kecil_per_kota(c, 30000) == {'Bandung': (2, 1), 'Jakarta': (2, 2), 'Medan': (0, 1), 'Surabaya': (2, 0)}
            assert besar_kecil_per_kota(c, 0)['Medan'] == (1, 0)
            """,
            "Dua SUM CASE dengan kondisi berlawanan di dalam GROUP BY kota.",
            """
            import sqlite3

            def besar_kecil_per_kota(c, batas):
                q = '''
                SELECT kota,
                       SUM(CASE WHEN total >= ? THEN 1 ELSE 0 END),
                       SUM(CASE WHEN total < ? THEN 1 ELSE 0 END)
                FROM pesanan GROUP BY kota
                '''
                return {k: (b, s) for k, b, s in c.execute(q, (batas, batas)).fetchall()}
            """,
        ),
        E(
            "A6-03-3-ex3",
            "sedang",
            """
            Tulis fungsi `persen_per_kota(c)` yang mengembalikan dictionary `{kota: persentase total terhadap total keseluruhan dibulatkan 2 desimal}` memakai subquery skalar.
            """,
            """
            import sqlite3

            def persen_per_kota(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            p = persen_per_kota(c)
            assert p == {'Bandung': 25.62, 'Jakarta': 51.63, 'Medan': 2.6, 'Surabaya': 20.16}
            assert abs(sum(p.values()) - 100) < 0.05
            assert max(p, key=p.get) == 'Jakarta'
            """,
            "Bagi total tiap kota dengan SELECT SUM total keseluruhan lalu kalikan 100.0.",
            """
            import sqlite3

            def persen_per_kota(c):
                q = '''
                SELECT kota, round(100.0 * SUM(total) / (SELECT SUM(total) FROM pesanan), 2)
                FROM pesanan GROUP BY kota
                '''
                return dict(c.execute(q).fetchall())
            """,
        ),
        E(
            "A6-03-3-ex4",
            "menantang",
            """
            Tulis fungsi `kota_teratas(c, n)` yang mengembalikan list `n` nama kota dengan pesanan terbanyak, seri diputus dengan nama kota abjad.
            """,
            """
            import sqlite3

            def kota_teratas(c, n):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert kota_teratas(c, 2) == ['Jakarta', 'Bandung']
            assert kota_teratas(c, 1) == ['Jakarta']
            assert kota_teratas(c, 4) == ['Jakarta', 'Bandung', 'Surabaya', 'Medan']
            assert kota_teratas(c, 0) == []
            """,
            "Urutkan menurut COUNT menurun lalu kota lalu batasi.",
            """
            import sqlite3

            def kota_teratas(c, n):
                q = 'SELECT kota FROM pesanan GROUP BY kota ORDER BY COUNT(*) DESC, kota LIMIT ?'
                return [r[0] for r in c.execute(q, (n,)).fetchall()]
            """,
        ),
    ],
    [
        M("Menyarangkan agregat langsung seperti AVG(SUM(x)).", "Gunakan subquery atau CTE."),
        M("Mengira periode tanpa data muncul di hasil GROUP BY.", "Perlu tabel kalender dan JOIN."),
        M("Lupa mengalikan 100.0 sehingga persentase menjadi bulat.", "Kalikan dengan 100.0."),
    ],
    [
        Q("Agregasi bersyarat memakai?", ["SUM dengan CASE", "WHERE saja", "LIMIT", "DISTINCT"], 0, "Pivot manual.", hint="CASE."),
        Q("Ambil bulan dari tanggal ISO?", ["substr(tanggal,1,7)", "substr(tanggal,1,4)", "length", "upper"], 0, "YYYY-MM.", hint="Tujuh karakter."),
        Q("Subquery skalar mengembalikan?", ["Satu nilai", "Satu tabel", "Banyak baris", "Kolom"], 0, "Konstanta.", hint="Satu."),
        Q("Periode tanpa data di GROUP BY?", ["Tidak muncul", "Muncul nol", "Muncul NULL", "Error"], 0, "Tak ada baris.", hint="Hilang."),
        Q("Top N per kelompok butuh?", ["Fungsi window", "LIMIT biasa", "DISTINCT", "HAVING"], 0, "Peringkat.", hint="Window."),
    ],
    [
        "substr pada tanggal ISO menghasilkan ringkasan per periode.",
        "SUM dengan CASE menghasilkan agregasi bersyarat.",
        "Subquery skalar menjadi penyebut persentase.",
        "Pemutus seri membuat kelompok teratas stabil.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perintah yang cukup jelas dalam teks.", "brief": []}

write_module(
    "A6",
    3,
    "Agregasi dan GROUP BY",
    105,
    [
        "Memakai fungsi agregat dengan benar terhadap NULL dan tabel kosong",
        "Meringkas per kelompok dengan GROUP BY dan HAVING",
        "Membuat agregasi bersyarat dan persentase dari total",
    ],
    [l1, l2, l3],
    video,
    REF,
)
