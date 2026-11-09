import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

SQL_DB = """
CREATE TABLE pelanggan (id INTEGER PRIMARY KEY, nama TEXT, kota TEXT);
CREATE TABLE produk (id INTEGER PRIMARY KEY, nama TEXT, harga REAL);
CREATE TABLE pesanan (id INTEGER PRIMARY KEY, pelanggan_id INTEGER, produk_id INTEGER, jumlah INTEGER);
INSERT INTO pelanggan VALUES
(1, 'Ani', 'Jakarta'),
(2, 'Budi', 'Bandung'),
(3, 'Citra', 'Jakarta'),
(4, 'Dewi', 'Surabaya'),
(5, 'Eko', 'Medan');
INSERT INTO produk VALUES
(1, 'Pensil', 2500),
(2, 'Buku', 12000),
(3, 'Tas', 150000),
(4, 'Botol', 35000);
INSERT INTO pesanan VALUES
(1, 1, 2, 2),
(2, 1, 1, 10),
(3, 2, 3, 1),
(4, 3, 2, 1),
(5, 3, 4, 2),
(6, 4, 1, 20),
(7, 2, 2, 3),
(8, 99, 1, 1);
"""

SETUP = textwrap.indent("import sqlite3\n\nc = sqlite3.connect(':memory:')\nc.executescript('''" + SQL_DB + "''')\n", '            ')

FIX = textwrap.indent("import sqlite3\n\ndef _db():\n    c = sqlite3.connect(':memory:')\n    c.executescript('''" + textwrap.indent(SQL_DB, '    ') + "    ''')\n    return c\n\n", '            ')

l1 = lesson(
    "A6-05-1",
    "Subquery skalar dan IN",
    35,
    [
        "Menulis subquery skalar yang mengembalikan satu nilai",
        "Menyaring dengan IN dan NOT IN memakai subquery",
        "Menjelaskan jebakan NOT IN ketika subquery mengandung NULL",
        "Menggunakan subquery untuk membandingkan baris dengan agregat",
    ],
    [
        T("""
        ## Query di dalam query

        **Subquery** adalah query yang bersarang di dalam query lain, ditulis di dalam tanda kurung. Ia memungkinkan kita menjawab pertanyaan dua langkah dalam satu pernyataan: produk mana yang harganya di atas rata-rata? Langkah pertama menghitung rata-rata, langkah kedua membandingkan tiap produk dengannya.

        Tanpa subquery kita harus menjalankan dua query dan memindahkan angka rata-rata secara manual ke query kedua. Subquery menghilangkan langkah manual itu dan menjaga seluruh logika tetap berada di basis data.
        """),
        T("""
        ## Subquery skalar

        **Subquery skalar** menghasilkan tepat satu baris dengan satu kolom, sehingga dapat dipakai di mana pun nilai tunggal diizinkan: di `WHERE`, di daftar `SELECT`, atau di ekspresi. Bila ia menghasilkan lebih dari satu baris, sebagian basis data melempar galat dan SQLite diam-diam mengambil baris pertama, perilaku yang berbahaya.

        Pastikan subquery skalar memang menghasilkan satu nilai, biasanya lewat fungsi agregat tanpa `GROUP BY`. Bila hasilnya kosong, nilainya `NULL`, dan perbandingan dengan `NULL` menghasilkan tidak diketahui sehingga tak ada baris yang lolos.
        """),
        C(
            SETUP + """
            print(c.execute('SELECT AVG(harga) FROM produk').fetchone())
            q = 'SELECT nama FROM produk WHERE harga > (SELECT AVG(harga) FROM produk) ORDER BY id'
            print(c.execute(q).fetchall())
            q = 'SELECT nama, harga - (SELECT AVG(harga) FROM produk) FROM produk ORDER BY id'
            print(c.execute(q).fetchall())
            """,
            """
            (49875.0,)
            [('Tas',)]
            [('Pensil', -47375.0), ('Buku', -37875.0), ('Tas', 100125.0), ('Botol', -14875.0)]
            """,
            """
            Hanya tas yang harganya di atas rata-rata 49.875, dan selisih terhadap rata-rata dapat dihitung untuk setiap produk.
            """,
            filename="subquery_skalar.py",
        ),
        T("""
        ## Subquery dan agregat

        Salah satu kegunaan terpenting subquery skalar adalah membandingkan baris dengan agregat dari tabel yang sama. Pada query biasa kita tidak bisa menulis `WHERE harga > AVG(harga)` karena agregat belum ada saat `WHERE` dievaluasi. Subquery mengatasinya karena dihitung lebih dulu sebagai nilai tunggal.

        Pola ini muncul terus: pesanan di atas rata-rata, pelanggan dengan belanja di atas median, produk dengan harga tertinggi. Semuanya membandingkan sebuah baris dengan ringkasan seluruh data.
        """),
        T("""
        ## IN dengan subquery

        `IN` tidak harus berisi daftar tetap. Ia dapat berisi subquery yang menghasilkan satu kolom: `WHERE id IN (SELECT produk_id FROM pesanan WHERE jumlah >= 3)` memilih produk yang pernah dipesan minimal tiga unit. Subquery dievaluasi menjadi himpunan nilai, lalu tiap baris luar diperiksa keanggotaannya.

        Bentuk ini menyatakan maksud dengan jelas dan tidak menduplikasi baris seperti JOIN satu-ke-banyak. Itu sebabnya `IN` dengan subquery sering dipilih untuk pertanyaan keanggotaan.
        """),
        C(
            SETUP + """
            q = '''
            SELECT nama FROM produk
            WHERE id IN (SELECT produk_id FROM pesanan WHERE jumlah >= 3)
            ORDER BY id
            '''
            print(c.execute(q).fetchall())
            q = 'SELECT nama FROM pelanggan WHERE kota IN (SELECT kota FROM pelanggan WHERE nama = ?) ORDER BY id'
            print(c.execute(q, ('Ani',)).fetchall())
            """,
            """
            [('Pensil',), ('Buku',)]
            [('Ani',), ('Citra',)]
            """,
            """
            Pensil dan buku pernah dipesan minimal tiga unit, dan Ani sekota dengan Citra.
            """,
            filename="in_subquery.py",
        ),
        T("""
        ## NOT IN dan NULL

        `NOT IN` menyimpan jebakan paling terkenal di SQL. Bila subquery menghasilkan satu saja nilai `NULL`, maka `x NOT IN (...)` tidak pernah benar untuk semua baris: perbandingan dengan `NULL` tidak diketahui, sehingga seluruh hasil menjadi kosong tanpa peringatan.

        Contoh: tambahkan satu pesanan dengan `pelanggan_id` kosong. Kueri pelanggan tanpa pesanan dengan `NOT IN` tiba-tiba mengembalikan kosong, padahal Eko masih belum memesan. Query yang tadinya benar diam-diam menjadi salah saat data berubah.
        """),
        C(
            SETUP + """
            q = 'SELECT nama FROM pelanggan WHERE id NOT IN (SELECT pelanggan_id FROM pesanan) ORDER BY id'
            print(c.execute(q).fetchall())
            c.execute('INSERT INTO pesanan VALUES (9, NULL, 1, 1)')
            print(c.execute(q).fetchall())
            aman = '''
            SELECT nama FROM pelanggan
            WHERE id NOT IN (SELECT pelanggan_id FROM pesanan WHERE pelanggan_id IS NOT NULL)
            ORDER BY id
            '''
            print(c.execute(aman).fetchall())
            """,
            """
            [('Eko',)]
            []
            [('Eko',)]
            """,
            """
            Satu NULL pada subquery membuat NOT IN kosong, dan membuang NULL dari subquery memulihkan hasil yang benar.
            """,
            filename="not_in_null.py",
        ),
        T("""
        ## Dua perbaikan untuk NOT IN

        Ada dua cara aman. Pertama, buang `NULL` dari subquery dengan `WHERE kolom IS NOT NULL`, seperti pada contoh. Kedua, ganti `NOT IN` dengan `NOT EXISTS`, yang tidak terpengaruh `NULL` dan dibahas di pelajaran berikutnya. Banyak panduan gaya SQL melarang `NOT IN` pada subquery kecuali kolomnya dijamin tidak `NULL`.

        Aturan umum: setiap kali menulis `NOT IN` dengan subquery, tanyakan apakah kolom itu bisa `NULL`. Bila ya atau tidak yakin, pakai `NOT EXISTS`.
        """),
        K(
            "warn",
            """
            Satu NULL di dalam subquery NOT IN membuat seluruh hasil kosong. Gunakan NOT EXISTS atau buang NULL dengan IS NOT NULL.
            """,
            title="Jebakan NOT IN",
        ),
        T("""
        ## Subquery dan keterbacaan

        Subquery membuat pertanyaan bisnis terbaca hampir seperti kalimat: produk yang harganya di atas rata-rata, pelanggan yang pernah memesan, pesanan yang jumlahnya besar. Namun subquery yang terlalu dalam justru menyulitkan pembaca. Bila bersarang lebih dari dua tingkat, pertimbangkan memecahnya dengan CTE yang dibahas di pelajaran ketiga.

        Biasakan memberi indentasi pada subquery dan menaruh tanda kurungnya sejajar, sehingga batas bagian dalam dan luar terlihat jelas. Query yang rapi lebih mudah diperiksa, diuji, dan diperbaiki oleh rekan kerja.
        """),
        T("""
        ## Memeriksa subquery secara terpisah

        Saat query gagal atau hasilnya aneh, jalankan subquery bagian dalam sendirian lebih dulu. Lihat apakah ia menghasilkan satu nilai bila dimaksudkan skalar, atau kolom tanpa NULL bila dipakai di NOT IN. Setelah bagian dalam terbukti benar, barulah periksa bagian luar.

        Kebiasaan ini menghemat waktu karena kesalahan hampir selalu bersembunyi di salah satu lapisan saja. Menguji tiap lapisan terpisah jauh lebih cepat daripada menebak dari hasil akhir yang salah.
        """),
        E(
            "A6-05-1-ex1",
            "mudah",
            """
            Tulis fungsi `produk_di_atas_rata(c)` yang mengembalikan list nama produk dengan harga lebih besar dari rata-rata harga semua produk, terurut menurut id, memakai subquery skalar.
            """,
            """
            import sqlite3

            def produk_di_atas_rata(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert produk_di_atas_rata(c) == ['Tas']
            c.execute("INSERT INTO produk VALUES (5, 'Laptop', 5000000)")
            assert produk_di_atas_rata(c) == ['Laptop']
            c.execute('UPDATE produk SET harga = 10 WHERE id = 5')
            assert produk_di_atas_rata(c) == ['Tas']
            """,
            "Bandingkan harga dengan SELECT AVG harga dalam kurung.",
            """
            import sqlite3

            def produk_di_atas_rata(c):
                q = 'SELECT nama FROM produk WHERE harga > (SELECT AVG(harga) FROM produk) ORDER BY id'
                return [r[0] for r in c.execute(q).fetchall()]
            """,
        ),
        E(
            "A6-05-1-ex2",
            "sedang",
            """
            Tulis fungsi `produk_pesanan_besar(c, minimum)` yang mengembalikan list nama produk yang pernah dipesan dengan `jumlah` minimal `minimum`, terurut menurut id produk, memakai `IN` dengan subquery.
            """,
            """
            import sqlite3

            def produk_pesanan_besar(c, minimum):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert produk_pesanan_besar(c, 3) == ['Pensil', 'Buku']
            assert produk_pesanan_besar(c, 20) == ['Pensil']
            assert produk_pesanan_besar(c, 100) == []
            assert produk_pesanan_besar(c, 1) == ['Pensil', 'Buku', 'Tas', 'Botol']
            """,
            "Pakai IN dengan subquery yang memilih produk_id dari pesanan dengan syarat jumlah.",
            """
            import sqlite3

            def produk_pesanan_besar(c, minimum):
                q = 'SELECT nama FROM produk WHERE id IN (SELECT produk_id FROM pesanan WHERE jumlah >= ?) ORDER BY id'
                return [r[0] for r in c.execute(q, (minimum,)).fetchall()]
            """,
        ),
        E(
            "A6-05-1-ex3",
            "sedang",
            """
            Tulis fungsi `produk_belum_dipesan(c)` yang mengembalikan list nama produk yang belum pernah muncul di pesanan, terurut menurut id, memakai `NOT IN`.
            """,
            """
            import sqlite3

            def produk_belum_dipesan(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert produk_belum_dipesan(c) == []
            c.execute("INSERT INTO produk VALUES (5, 'Pulpen', 3000)")
            assert produk_belum_dipesan(c) == ['Pulpen']
            c.execute("INSERT INTO produk VALUES (6, 'Kertas', 1000)")
            assert produk_belum_dipesan(c) == ['Pulpen', 'Kertas']
            """,
            "Pakai NOT IN dengan subquery produk_id dari pesanan.",
            """
            import sqlite3

            def produk_belum_dipesan(c):
                q = 'SELECT nama FROM produk WHERE id NOT IN (SELECT produk_id FROM pesanan WHERE produk_id IS NOT NULL) ORDER BY id'
                return [r[0] for r in c.execute(q).fetchall()]
            """,
        ),
        E(
            "A6-05-1-ex4",
            "menantang",
            """
            Tulis fungsi `pelanggan_tanpa_pesanan_aman(c)` yang mengembalikan list nama pelanggan tanpa pesanan, terurut menurut id, dan tetap benar walau ada pesanan dengan `pelanggan_id` `NULL`.
            """,
            """
            import sqlite3

            def pelanggan_tanpa_pesanan_aman(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert pelanggan_tanpa_pesanan_aman(c) == ['Eko']
            c.execute('INSERT INTO pesanan VALUES (9, NULL, 1, 1)')
            assert pelanggan_tanpa_pesanan_aman(c) == ['Eko']
            c.execute('INSERT INTO pesanan VALUES (10, 5, 1, 1)')
            assert pelanggan_tanpa_pesanan_aman(c) == []
            """,
            "Buang NULL dari subquery atau pakai NOT EXISTS.",
            """
            import sqlite3

            def pelanggan_tanpa_pesanan_aman(c):
                q = '''
                SELECT nama FROM pelanggan
                WHERE id NOT IN (SELECT pelanggan_id FROM pesanan WHERE pelanggan_id IS NOT NULL)
                ORDER BY id
                '''
                return [r[0] for r in c.execute(q).fetchall()]
            """,
        ),
    ],
    [
        M("Memakai NOT IN pada subquery yang bisa berisi NULL.", "Buang NULL atau pakai NOT EXISTS."),
        M("Menulis subquery skalar yang bisa menghasilkan banyak baris.", "Pastikan agregat atau LIMIT satu baris."),
        M("Menulis WHERE harga > AVG(harga).", "Gunakan subquery skalar untuk rata-rata."),
    ],
    [
        Q("Subquery skalar mengembalikan?", ["Satu nilai", "Satu tabel", "Banyak kolom", "Tidak ada"], 0, "Satu baris satu kolom.", hint="Satu."),
        Q("Subquery ditulis di dalam?", ["Tanda kurung", "Kurung siku", "Kutip", "Komentar"], 0, "Kurung.", hint="Kurung."),
        Q("NOT IN dengan NULL di subquery menghasilkan?", ["Hasil kosong", "Semua baris", "Error", "Setengah"], 0, "Tidak diketahui.", hint="Kosong."),
        Q("Membandingkan baris dengan agregat membutuhkan?", ["Subquery skalar", "GROUP BY", "DISTINCT", "LIMIT"], 0, "Agregat belum ada di WHERE.", hint="Skalar."),
        Q("IN dengan subquery cocok untuk?", ["Keanggotaan", "Penjumlahan", "Pengurutan", "Pembuatan tabel"], 0, "Anggota himpunan.", hint="Anggota."),
    ],
    [
        "Subquery skalar memungkinkan membandingkan baris dengan agregat.",
        "IN dengan subquery menyaring berdasarkan keanggotaan tanpa menduplikasi baris.",
        "NOT IN gagal bila subquery mengandung NULL.",
        "Buang NULL atau pakai NOT EXISTS untuk keamanan.",
    ],
    [],
)

l2 = lesson(
    "A6-05-2",
    "Subquery berkorelasi dan EXISTS",
    35,
    [
        "Menjelaskan subquery berkorelasi yang merujuk baris luar",
        "Memakai EXISTS dan NOT EXISTS",
        "Menghitung nilai per baris dengan subquery di SELECT",
        "Membandingkan baris dengan rata-rata kelompoknya sendiri",
    ],
    [
        T("""
        ## Subquery yang merujuk query luar

        Pada subquery biasa, bagian dalam berdiri sendiri: ia dapat dijalankan terpisah. Pada **subquery berkorelasi**, bagian dalam merujuk kolom dari query luar sehingga hasilnya berbeda untuk setiap baris luar. Secara konsep, subquery itu dijalankan ulang untuk tiap baris query luar dengan nilai kolom yang sesuai.

        Contoh: untuk tiap pelanggan, hitung jumlah pesanannya dengan `(SELECT COUNT(*) FROM pesanan p WHERE p.pelanggan_id = g.id)`. Kondisi `p.pelanggan_id = g.id` menghubungkan subquery dengan baris pelanggan yang sedang diproses.
        """),
        C(
            SETUP + """
            q = '''
            SELECT g.nama, (SELECT COUNT(*) FROM pesanan p WHERE p.pelanggan_id = g.id) AS n
            FROM pelanggan g ORDER BY g.id
            '''
            print(c.execute(q).fetchall())
            """,
            """
            [('Ani', 2), ('Budi', 2), ('Citra', 2), ('Dewi', 1), ('Eko', 0)]
            """,
            """
            Subquery berkorelasi menghitung pesanan tiap pelanggan, dan Eko benar bernilai nol tanpa perlu LEFT JOIN.
            """,
            filename="korelasi_select.py",
        ),
        T("""
        ## Korelasi di WHERE

        Subquery berkorelasi juga umum di `WHERE`. `WHERE (SELECT COUNT(*) FROM pesanan p WHERE p.pelanggan_id = g.id) >= 2` memilih pelanggan dengan minimal dua pesanan. Hasilnya sama dengan `GROUP BY` plus `HAVING` pada JOIN, tetapi sebagian orang menganggapnya lebih mudah dibaca karena tidak mengubah baris hasil.

        Perlu diingat performanya: tanpa optimasi, subquery berkorelasi dijalankan sekali per baris luar. Mesin basis data modern sering mengubahnya menjadi JOIN secara internal, tetapi pada tabel sangat besar uji dengan rencana eksekusi.
        """),
        T("""
        ## EXISTS

        `EXISTS (subquery)` bernilai benar bila subquery menghasilkan minimal satu baris, tidak peduli isinya. Karena isinya diabaikan, kebiasaan menulis `SELECT 1` di dalamnya. Ia berhenti begitu menemukan baris pertama, sehingga efisien untuk pertanyaan ada-atau-tidak.

        Pelanggan yang pernah memesan: `WHERE EXISTS (SELECT 1 FROM pesanan p WHERE p.pelanggan_id = g.id)`. Karena tiap pelanggan muncul sekali tanpa menggandakan baris, tidak perlu `DISTINCT` seperti pada JOIN.
        """),
        C(
            SETUP + """
            q = '''
            SELECT g.nama FROM pelanggan g
            WHERE EXISTS (SELECT 1 FROM pesanan p WHERE p.pelanggan_id = g.id)
            ORDER BY g.id
            '''
            print(c.execute(q).fetchall())
            q = '''
            SELECT g.nama FROM pelanggan g
            WHERE NOT EXISTS (SELECT 1 FROM pesanan p WHERE p.pelanggan_id = g.id)
            ORDER BY g.id
            '''
            print(c.execute(q).fetchall())
            """,
            """
            [('Ani',), ('Budi',), ('Citra',), ('Dewi',)]
            [('Eko',)]
            """,
            """
            EXISTS memilih pelanggan yang pernah memesan, dan NOT EXISTS memilih yang belum, yaitu Eko.
            """,
            filename="exists.py",
        ),
        T("""
        ## NOT EXISTS lebih aman dari NOT IN

        `NOT EXISTS` tidak terpengaruh nilai `NULL` karena hanya menguji apakah ada baris, bukan membandingkan nilai. Pada pesanan dengan `pelanggan_id` `NULL`, `NOT IN` mengembalikan kosong tetapi `NOT EXISTS` tetap benar. Itu sebabnya ia menjadi bentuk anti-join pilihan banyak praktisi.

        Dua bentuk anti-join, `LEFT JOIN ... IS NULL` dan `NOT EXISTS`, setara hasilnya. Pilih yang paling jelas bagimu dan timmu, dan konsisten memakainya agar kode mudah dipelihara.
        """),
        C(
            SETUP + """
            c.execute('INSERT INTO pesanan VALUES (9, NULL, 1, 1)')
            q = '''
            SELECT g.nama FROM pelanggan g
            WHERE NOT EXISTS (SELECT 1 FROM pesanan p WHERE p.pelanggan_id = g.id)
            ORDER BY g.id
            '''
            print(c.execute(q).fetchall())
            """,
            """
            [('Eko',)]
            """,
            """
            NOT EXISTS tetap benar walau ada pesanan dengan pelanggan NULL.
            """,
            filename="not_exists_null.py",
        ),
        T("""
        ## Membandingkan dengan kelompok sendiri

        Subquery berkorelasi sangat cocok untuk membandingkan baris dengan agregat kelompoknya. Pesanan mana yang jumlahnya di atas rata-rata untuk produk yang sama? Subquery `SELECT AVG(jumlah) FROM pesanan WHERE produk_id = p.produk_id` menghitung rata-rata per produk sesuai baris luar.

        Hasilnya pesanan yang menonjol dibanding pesanan lain untuk produk sama, bukan dibanding seluruh pesanan. Fungsi window pada modul berikutnya melakukan hal serupa lebih ringkas dan cepat, tetapi subquery berkorelasi tetap penting dipahami.
        """),
        C(
            SETUP + """
            q = '''
            SELECT p.id FROM pesanan p
            WHERE p.jumlah > (SELECT AVG(jumlah) FROM pesanan WHERE produk_id = p.produk_id)
            ORDER BY p.id
            '''
            print(c.execute(q).fetchall())
            """,
            """
            [(6,), (7,)]
            """,
            """
            Pesanan enam dan tujuh jumlahnya di atas rata-rata untuk produk masing-masing.
            """,
            filename="korelasi_kelompok.py",
        ),
        T("""
        ## Kapan memakai yang mana

        Untuk keberadaan, pakai `EXISTS` atau `NOT EXISTS`. Untuk nilai per baris dari tabel lain, pakai subquery berkorelasi di `SELECT` atau JOIN dengan agregasi. Untuk membandingkan dengan agregat kelompok, pakai subquery berkorelasi atau fungsi window. Untuk menyaring berdasarkan daftar nilai, pakai `IN` dengan subquery yang tidak mengandung `NULL`.

        Tidak ada pilihan tunggal terbaik. Mulailah dengan yang paling jelas menyatakan niat, lalu ukur kinerja bila tabel besar. Keterbacaan jarang kalah penting dibanding kecepatan pada kebanyakan laporan harian.
        """),
        K(
            "tip",
            """
            Gunakan NOT EXISTS untuk anti-join. Hasilnya tidak terpengaruh NULL dan niatnya mudah dibaca.
            """,
            title="Anti-join aman",
        ),
        T("""
        ## Korelasi dan nama alias

        Pada subquery berkorelasi, alias tabel sangat penting. Bila tabel luar dan dalam sama, seperti pesanan dibandingkan dengan pesanan lain untuk produk yang sama, kita wajib memberi alias berbeda, misalnya `p` untuk luar dan tanpa alias atau `q` untuk dalam. Tanpa alias, nama kolom ambigu dan basis data merujuk ke tabel terdekat, yang sering bukan maksud kita.

        Selalu awali kolom dengan alias tabelnya di subquery berkorelasi. Itu menghilangkan keraguan tentang baris mana yang dirujuk dan membuat query lebih mudah dibaca.
        """),
        T("""
        ## Kinerja subquery berkorelasi

        Pada tabel kecil, subquery berkorelasi terasa instan. Pada jutaan baris tanpa indeks, menjalankannya per baris luar bisa sangat lambat. Indeks pada kolom penghubung, seperti `pelanggan_id` di tabel pesanan, mengubah pencarian tiap baris dari menyisir seluruh tabel menjadi lompatan langsung.

        Bila query lambat, bandingkan beberapa bentuk setara: EXISTS, JOIN dengan agregasi, dan fungsi window. Ukur waktunya pada data yang realistis, sebab pilihan tercepat bergantung pada ukuran data dan indeks yang tersedia.
        """),
        E(
            "A6-05-2-ex1",
            "mudah",
            """
            Tulis fungsi `banyak_pesanan(c)` yang mengembalikan list tuple `(nama_pelanggan, banyak_pesanan)` untuk semua pelanggan, terurut menurut id pelanggan, memakai subquery berkorelasi di `SELECT`.
            """,
            """
            import sqlite3

            def banyak_pesanan(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert banyak_pesanan(c) == [('Ani', 2), ('Budi', 2), ('Citra', 2), ('Dewi', 1), ('Eko', 0)]
            c.execute('INSERT INTO pesanan VALUES (9, 5, 1, 1)')
            assert banyak_pesanan(c)[-1] == ('Eko', 1)
            c.execute("INSERT INTO pelanggan VALUES (6, 'Fani', 'Bogor')")
            assert banyak_pesanan(c)[-1] == ('Fani', 0)
            """,
            "Hitung pesanan dengan subquery yang merujuk id pelanggan luar.",
            """
            import sqlite3

            def banyak_pesanan(c):
                q = '''
                SELECT g.nama, (SELECT COUNT(*) FROM pesanan p WHERE p.pelanggan_id = g.id)
                FROM pelanggan g ORDER BY g.id
                '''
                return c.execute(q).fetchall()
            """,
        ),
        E(
            "A6-05-2-ex2",
            "sedang",
            """
            Tulis fungsi `pelanggan_min_pesanan(c, n)` yang mengembalikan list nama pelanggan dengan paling sedikit `n` pesanan, terurut menurut id, memakai subquery berkorelasi di `WHERE`.
            """,
            """
            import sqlite3

            def pelanggan_min_pesanan(c, n):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert pelanggan_min_pesanan(c, 2) == ['Ani', 'Budi', 'Citra']
            assert pelanggan_min_pesanan(c, 1) == ['Ani', 'Budi', 'Citra', 'Dewi']
            assert pelanggan_min_pesanan(c, 3) == []
            assert pelanggan_min_pesanan(c, 0) == ['Ani', 'Budi', 'Citra', 'Dewi', 'Eko']
            """,
            "Bandingkan hitungan subquery berkorelasi dengan parameter n.",
            """
            import sqlite3

            def pelanggan_min_pesanan(c, n):
                q = '''
                SELECT g.nama FROM pelanggan g
                WHERE (SELECT COUNT(*) FROM pesanan p WHERE p.pelanggan_id = g.id) >= ?
                ORDER BY g.id
                '''
                return [r[0] for r in c.execute(q, (n,)).fetchall()]
            """,
        ),
        E(
            "A6-05-2-ex3",
            "sedang",
            """
            Tulis fungsi `pesanan_di_atas_rata_produk(c)` yang mengembalikan list id pesanan dengan `jumlah` lebih besar dari rata-rata `jumlah` pesanan untuk produk yang sama, terurut menurut id.
            """,
            """
            import sqlite3

            def pesanan_di_atas_rata_produk(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert pesanan_di_atas_rata_produk(c) == [6, 7]
            c.execute('INSERT INTO pesanan VALUES (9, 1, 3, 5)')
            assert pesanan_di_atas_rata_produk(c) == [6, 7, 9]
            c.execute('DELETE FROM pesanan WHERE id = 9')
            assert pesanan_di_atas_rata_produk(c) == [6, 7]
            """,
            "Subquery berkorelasi menghitung AVG jumlah untuk produk_id yang sama.",
            """
            import sqlite3

            def pesanan_di_atas_rata_produk(c):
                q = '''
                SELECT p.id FROM pesanan p
                WHERE p.jumlah > (SELECT AVG(jumlah) FROM pesanan WHERE produk_id = p.produk_id)
                ORDER BY p.id
                '''
                return [r[0] for r in c.execute(q).fetchall()]
            """,
        ),
        E(
            "A6-05-2-ex4",
            "menantang",
            """
            Tulis fungsi `teman_sekota(c, nama)` yang mengembalikan list nama pelanggan LAIN yang tinggal di kota yang sama dengan pelanggan bernama `nama`, terurut menurut id, memakai subquery skalar. Nama tak dikenal menghasilkan list kosong.
            """,
            """
            import sqlite3

            def teman_sekota(c, nama):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert teman_sekota(c, 'Ani') == ['Citra']
            assert teman_sekota(c, 'Citra') == ['Ani']
            assert teman_sekota(c, 'Budi') == []
            assert teman_sekota(c, 'Tidak ada') == []
            """,
            "Bandingkan kota dengan hasil subquery skalar dan kecualikan nama itu sendiri.",
            """
            import sqlite3

            def teman_sekota(c, nama):
                q = '''
                SELECT nama FROM pelanggan
                WHERE kota = (SELECT kota FROM pelanggan WHERE nama = ?) AND nama <> ?
                ORDER BY id
                '''
                return [r[0] for r in c.execute(q, (nama, nama)).fetchall()]
            """,
        ),
    ],
    [
        M("Mengira subquery berkorelasi dijalankan sekali.", "Secara konsep dijalankan per baris luar."),
        M("Memakai NOT IN padahal kolom bisa NULL.", "Pakai NOT EXISTS."),
        M("Menulis EXISTS dengan SELECT kolom besar.", "Cukup SELECT 1 karena isinya diabaikan."),
    ],
    [
        Q("Subquery berkorelasi?", ["Merujuk kolom query luar", "Berdiri sendiri", "Tanpa WHERE", "Selalu lambat"], 0, "Bergantung baris luar.", hint="Rujukan."),
        Q("EXISTS bernilai benar bila?", ["Subquery menghasilkan minimal satu baris", "Subquery kosong", "Ada NULL", "Ada duplikat"], 0, "Ada baris.", hint="Minimal satu."),
        Q("Anti-join paling aman terhadap NULL?", ["NOT EXISTS", "NOT IN", "<>", "!="], 0, "Tidak membandingkan nilai.", hint="Exists."),
        Q("Isi SELECT di dalam EXISTS?", ["Diabaikan", "Sangat penting", "Harus kolom id", "Harus bintang"], 0, "Hanya keberadaan.", hint="SELECT 1."),
        Q("Bandingkan baris dengan rata-rata kelompoknya memakai?", ["Subquery berkorelasi", "LIMIT", "DISTINCT", "ORDER BY"], 0, "Atau fungsi window.", hint="Korelasi."),
    ],
    [
        "Subquery berkorelasi bergantung pada baris query luar.",
        "EXISTS menguji keberadaan tanpa menduplikasi baris.",
        "NOT EXISTS aman terhadap NULL, tidak seperti NOT IN.",
        "Subquery berkorelasi membandingkan baris dengan agregat kelompoknya.",
    ],
    [],
)

l3 = lesson(
    "A6-05-3",
    "CTE dengan WITH dan subquery di FROM",
    35,
    [
        "Menulis CTE dengan WITH untuk memecah query rumit",
        "Memakai subquery di FROM untuk agregasi dua tingkat",
        "Merantai beberapa CTE",
        "Menulis CTE rekursif sederhana",
    ],
    [
        T("""
        ## Masalah query bersarang dalam

        Query dengan subquery bersarang beberapa lapis cepat menjadi sulit dibaca: kita harus membacanya dari dalam ke luar, dan satu subquery yang sama sering harus ditulis berulang. **CTE**, Common Table Expression, memperbaikinya dengan memberi nama pada hasil antara dan memakainya seperti tabel.

        CTE ditulis dengan `WITH nama AS (query)` di depan query utama. Bacanya dari atas ke bawah seperti langkah-langkah: langkah pertama menghasilkan tabel sementara, langkah berikutnya memakainya. Ini membuat query kompleks menjadi alur yang jelas.
        """),
        C(
            SETUP + """
            q = '''
            WITH belanja AS (
                SELECT p.pelanggan_id AS pid, SUM(p.jumlah * k.harga) AS total
                FROM pesanan p JOIN produk k ON k.id = p.produk_id
                GROUP BY p.pelanggan_id
            )
            SELECT g.nama, b.total
            FROM belanja b JOIN pelanggan g ON g.id = b.pid
            ORDER BY g.id
            '''
            print(c.execute(q).fetchall())
            """,
            """
            [('Ani', 49000.0), ('Budi', 186000.0), ('Citra', 82000.0), ('Dewi', 50000.0)]
            """,
            """
            CTE belanja menghitung total per pelanggan, lalu query utama menggabungkannya dengan nama pelanggan.
            """,
            filename="cte_dasar.py",
        ),
        T("""
        ## CTE dipakai berkali-kali

        Keunggulan CTE: ia dapat dirujuk lebih dari sekali dalam query yang sama. Untuk mencari pelanggan dengan belanja di atas rata-rata belanja semua pelanggan, kita memakai CTE `belanja` sekali untuk menghitung rata-rata dan sekali lagi untuk menyaring. Tanpa CTE, subquery panjang harus ditulis dua kali.

        Menulis ulang subquery yang sama berulang bukan hanya membosankan tetapi rawan kesalahan: mengubah yang satu dan lupa yang lain menimbulkan hasil tidak konsisten. CTE memberi satu sumber kebenaran.
        """),
        C(
            SETUP + """
            q = '''
            WITH belanja AS (
                SELECT p.pelanggan_id AS pid, SUM(p.jumlah * k.harga) AS total
                FROM pesanan p JOIN produk k ON k.id = p.produk_id
                GROUP BY p.pelanggan_id
            )
            SELECT AVG(total), MAX(total) FROM belanja
            '''
            print(c.execute(q).fetchone())
            q = '''
            WITH belanja AS (
                SELECT p.pelanggan_id AS pid, SUM(p.jumlah * k.harga) AS total
                FROM pesanan p JOIN produk k ON k.id = p.produk_id
                GROUP BY p.pelanggan_id
            )
            SELECT g.nama FROM belanja b JOIN pelanggan g ON g.id = b.pid
            WHERE b.total > (SELECT AVG(total) FROM belanja)
            ORDER BY g.id
            '''
            print(c.execute(q).fetchall())
            """,
            """
            (73900.0, 186000.0)
            [('Budi',), ('Citra',)]
            """,
            """
            Rata-rata belanja 73.900 dipakai untuk menyaring, sehingga hanya Budi dan Citra yang di atasnya.
            """,
            filename="cte_dua_kali.py",
        ),
        T("""
        ## Agregasi dua tingkat

        Pertanyaan seperti berapa rata-rata jumlah pesanan per pelanggan membutuhkan agregasi dua tingkat: pertama hitung pesanan per pelanggan dengan `GROUP BY`, lalu rata-ratakan hasilnya. Agregat tidak boleh bersarang langsung seperti `AVG(COUNT(*))`, jadi tingkat pertama dibungkus sebagai subquery di `FROM` atau sebagai CTE.

        Subquery di `FROM` wajib diberi alias pada beberapa basis data. Fungsinya sama dengan CTE, tetapi CTE biasanya lebih mudah dibaca karena ditulis di awal dan diberi nama jelas.
        """),
        C(
            SETUP + """
            q = '''
            SELECT AVG(n), MAX(n) FROM (
                SELECT COUNT(*) AS n
                FROM pesanan p JOIN pelanggan g ON g.id = p.pelanggan_id
                GROUP BY g.id
            ) AS per_pelanggan
            '''
            print(c.execute(q).fetchone())
            """,
            """
            (1.75, 2)
            """,
            """
            Rata-rata pesanan per pelanggan aktif satu koma tujuh lima dan paling banyak dua.
            """,
            filename="agregasi_dua_tingkat.py",
        ),
        T("""
        ## Merantai CTE

        Beberapa CTE dapat dirantai dengan koma: `WITH a AS (...), b AS (...)`, dan CTE berikutnya boleh memakai yang sebelumnya. Ini mengubah analisis berlapis menjadi daftar langkah bernama. Misalnya langkah pertama menjumlahkan jumlah per pelanggan, langkah kedua menyaring pelanggan dengan jumlah besar, dan query utama menampilkan namanya.

        Beri nama CTE yang menggambarkan isinya, bukan `a` dan `b` seperti contoh singkat ini. Nama yang baik membuat query berfungsi sebagai dokumentasi bagi pembacanya.
        """),
        C(
            SETUP + """
            q = '''
            WITH per_pelanggan AS (
                SELECT pelanggan_id, SUM(jumlah) AS unit
                FROM pesanan GROUP BY pelanggan_id
            ),
            besar AS (
                SELECT pelanggan_id FROM per_pelanggan WHERE unit >= 10
            )
            SELECT g.nama FROM besar b JOIN pelanggan g ON g.id = b.pelanggan_id
            ORDER BY g.id
            '''
            print(c.execute(q).fetchall())
            """,
            """
            [('Ani',), ('Dewi',)]
            """,
            """
            Dua CTE berantai menyaring pelanggan dengan total unit sepuluh atau lebih, yaitu Ani dan Dewi.
            """,
            filename="cte_berantai.py",
        ),
        T("""
        ## CTE rekursif

        CTE dapat merujuk dirinya sendiri dengan `WITH RECURSIVE`, berguna untuk deret, hierarki, dan graf. Strukturnya dua bagian digabung `UNION ALL`: bagian dasar yang menghasilkan baris awal, dan bagian rekursif yang memakai baris sebelumnya untuk menghasilkan baris berikutnya, berhenti saat kondisi tidak terpenuhi.

        Contoh paling sederhana membangkitkan angka satu sampai lima. Di praktik, CTE rekursif menelusuri struktur organisasi, kategori bersarang, dan rute. Selalu pasang kondisi berhenti agar tidak berulang selamanya.
        """),
        C(
            """
            import sqlite3

            c = sqlite3.connect(':memory:')
            q = '''
            WITH RECURSIVE n(x) AS (
                SELECT 1
                UNION ALL
                SELECT x + 1 FROM n WHERE x < 5
            )
            SELECT x FROM n
            '''
            print([r[0] for r in c.execute(q).fetchall()])
            print(c.execute(q.replace('SELECT x FROM n', 'SELECT SUM(x) FROM n')).fetchone())
            """,
            """
            [1, 2, 3, 4, 5]
            (15,)
            """,
            """
            CTE rekursif membangkitkan angka satu sampai lima dan jumlahnya lima belas.
            """,
            filename="cte_rekursif.py",
        ),
        T("""
        ## CTE atau tabel sementara atau view

        CTE hidup hanya selama satu query. Bila hasil antara dipakai oleh beberapa query, pertimbangkan `CREATE VIEW` yang menyimpan definisi query sebagai tabel virtual, atau tabel sementara yang menyimpan hasilnya. View berguna untuk membagi logika umum antar laporan, sedangkan tabel sementara cocok bila hasil antara mahal dihitung.

        Untuk kebanyakan analisis sekali jalan, CTE sudah paling tepat: tanpa objek tambahan di basis data, dan seluruh logika terlihat dalam satu skrip.
        """),
        K(
            "tip",
            """
            Beri CTE nama yang menggambarkan isinya. Query dengan CTE bernama baik terbaca seperti rangkaian langkah analisis.
            """,
            title="Nama bermakna",
        ),
        T("""
        ## Kapan CTE tidak cukup

        CTE membuat query terbaca, tetapi ia bukan penyimpanan. Tiap kali dirujuk, sebagian mesin basis data menghitung ulang isinya, sehingga CTE yang berat dan dirujuk berkali-kali bisa lambat. Mesin lain menyimpannya sekali sebagai hasil sementara. Perilaku ini berbeda antar produk dan versi.

        Karena itu CTE dipakai terutama demi kejelasan. Bila kinerja menjadi masalah nyata, ukur dulu, lalu pertimbangkan tabel sementara atau indeks yang sesuai pada tabel sumbernya.
        """),
        T("""
        ## Menyusun analisis bertahap

        Cara terbaik menulis query analitik panjang adalah bertahap. Mulai dari CTE pertama yang hanya menyaring dan menghitung, jalankan, periksa hasilnya, lalu tambahkan CTE berikutnya. Setiap langkah diverifikasi sebelum melangkah lebih jauh, seperti menulis fungsi kecil yang diuji satu per satu.

        Pendekatan ini mengurangi kesalahan dan memudahkan menemukan di mana angka mulai menyimpang. Hasil akhirnya query yang bisa dijelaskan langkah demi langkah kepada orang lain.
        """),
        E(
            "A6-05-3-ex1",
            "mudah",
            """
            Tulis fungsi `belanja_di_atas_rata(c)` yang mengembalikan list nama pelanggan yang total belanjanya (jumlah kali harga) di atas rata-rata total belanja semua pelanggan yang pernah belanja, terurut menurut id, memakai CTE.
            """,
            """
            import sqlite3

            def belanja_di_atas_rata(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert belanja_di_atas_rata(c) == ['Budi', 'Citra']
            c.execute('INSERT INTO pesanan VALUES (9, 1, 3, 1)')
            assert belanja_di_atas_rata(c) == ['Ani', 'Budi']
            c.execute('DELETE FROM pesanan')
            assert belanja_di_atas_rata(c) == []
            """,
            "Buat CTE belanja per pelanggan lalu bandingkan dengan AVG dari CTE itu.",
            """
            import sqlite3

            def belanja_di_atas_rata(c):
                q = '''
                WITH belanja AS (
                    SELECT p.pelanggan_id AS pid, SUM(p.jumlah * k.harga) AS total
                    FROM pesanan p JOIN produk k ON k.id = p.produk_id
                    GROUP BY p.pelanggan_id
                )
                SELECT g.nama FROM belanja b JOIN pelanggan g ON g.id = b.pid
                WHERE b.total > (SELECT AVG(total) FROM belanja)
                ORDER BY g.id
                '''
                return [r[0] for r in c.execute(q).fetchall()]
            """,
        ),
        E(
            "A6-05-3-ex2",
            "sedang",
            """
            Tulis fungsi `rata_pesanan_per_pelanggan(c)` yang mengembalikan tuple `(rata, maksimum)` dari banyak pesanan per pelanggan (hanya pesanan yang punya pelanggan), dengan rata dibulatkan 4 desimal, memakai subquery di FROM.
            """,
            """
            import sqlite3

            def rata_pesanan_per_pelanggan(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert rata_pesanan_per_pelanggan(c) == (1.75, 2)
            c.execute('INSERT INTO pesanan VALUES (9, 4, 1, 1)')
            assert rata_pesanan_per_pelanggan(c) == (2.0, 2)
            c.execute('INSERT INTO pesanan VALUES (10, 1, 1, 1)')
            c.execute('INSERT INTO pesanan VALUES (11, 1, 1, 1)')
            assert rata_pesanan_per_pelanggan(c) == (2.5, 4)
            """,
            "Hitung pesanan per pelanggan di subquery lalu ambil AVG dan MAX dari hasilnya.",
            """
            import sqlite3

            def rata_pesanan_per_pelanggan(c):
                q = '''
                SELECT round(AVG(n), 4), MAX(n) FROM (
                    SELECT COUNT(*) AS n
                    FROM pesanan p JOIN pelanggan g ON g.id = p.pelanggan_id
                    GROUP BY g.id
                ) AS per_pelanggan
                '''
                return c.execute(q).fetchone()
            """,
        ),
        E(
            "A6-05-3-ex3",
            "sedang",
            """
            Tulis fungsi `pelanggan_jumlah_besar(c, batas)` yang mengembalikan list nama pelanggan dengan total `jumlah` pesanan minimal `batas`, terurut menurut id, memakai dua CTE berantai.
            """,
            """
            import sqlite3

            def pelanggan_jumlah_besar(c, batas):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert pelanggan_jumlah_besar(c, 10) == ['Ani', 'Dewi']
            assert pelanggan_jumlah_besar(c, 20) == ['Dewi']
            assert pelanggan_jumlah_besar(c, 100) == []
            assert pelanggan_jumlah_besar(c, 3) == ['Ani', 'Budi', 'Citra', 'Dewi']
            """,
            "CTE pertama menjumlahkan unit per pelanggan, CTE kedua menyaring batas.",
            """
            import sqlite3

            def pelanggan_jumlah_besar(c, batas):
                q = '''
                WITH per_pelanggan AS (
                    SELECT pelanggan_id, SUM(jumlah) AS unit FROM pesanan GROUP BY pelanggan_id
                ),
                besar AS (
                    SELECT pelanggan_id FROM per_pelanggan WHERE unit >= ?
                )
                SELECT g.nama FROM besar b JOIN pelanggan g ON g.id = b.pelanggan_id ORDER BY g.id
                '''
                return [r[0] for r in c.execute(q, (batas,)).fetchall()]
            """,
        ),
        E(
            "A6-05-3-ex4",
            "menantang",
            """
            Tulis fungsi `deret(n)` yang memakai CTE rekursif pada basis data memori untuk mengembalikan list bilangan bulat 1 sampai `n`. Untuk `n` kurang dari 1 kembalikan list kosong.
            """,
            """
            import sqlite3

            def deret(n):
                # TODO: implementasikan
                pass
            """,
            """
            assert deret(5) == [1, 2, 3, 4, 5]
            assert deret(1) == [1]
            assert deret(0) == []
            assert sum(deret(10)) == 55
            """,
            "Bagian dasar mulai dari 1 dengan syarat n minimal 1, bagian rekursif menambah satu sampai n.",
            """
            import sqlite3

            def deret(n):
                c = sqlite3.connect(':memory:')
                q = '''
                WITH RECURSIVE r(x) AS (
                    SELECT 1 WHERE ? >= 1
                    UNION ALL
                    SELECT x + 1 FROM r WHERE x < ?
                )
                SELECT x FROM r
                '''
                return [row[0] for row in c.execute(q, (n, n)).fetchall()]
            """,
        ),
    ],
    [
        M("Menulis ulang subquery yang sama berulang kali.", "Bungkus dalam CTE bernama."),
        M("Menyarangkan agregat langsung seperti AVG(COUNT(*)).", "Hitung tingkat pertama di CTE atau subquery FROM."),
        M("CTE rekursif tanpa kondisi berhenti.", "Pasang kondisi WHERE yang menghentikan rekursi."),
    ],
    [
        Q("CTE dimulai dengan?", ["WITH", "FROM", "SELECT", "CASE"], 0, "WITH nama AS.", hint="With."),
        Q("Keunggulan CTE?", ["Dapat dirujuk berkali-kali dan terbaca berurutan", "Selalu lebih cepat", "Menyimpan permanen", "Mengganti tabel"], 0, "Keterbacaan.", hint="Nama."),
        Q("Agregasi dua tingkat membutuhkan?", ["Subquery FROM atau CTE", "DISTINCT", "LIMIT", "UNION"], 0, "Agregat tak bersarang langsung.", hint="Bungkus."),
        Q("CTE rekursif memiliki bagian?", ["Dasar dan rekursif", "Hanya dasar", "Hanya rekursif", "Tiga bagian"], 0, "UNION ALL.", hint="Dua."),
        Q("Umur CTE?", ["Satu query", "Satu sesi", "Permanen", "Satu hari"], 0, "Sementara.", hint="Query."),
    ],
    [
        "CTE memberi nama pada hasil antara agar query terbaca berurutan.",
        "Agregasi dua tingkat memakai subquery FROM atau CTE.",
        "CTE dapat dirantai dan dirujuk berkali-kali.",
        "CTE rekursif membangkitkan deret dengan kondisi berhenti.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perintah yang cukup jelas dalam teks.", "brief": []}

write_module(
    "A6",
    5,
    "Subquery dan CTE",
    105,
    [
        "Menulis subquery skalar, IN, dan EXISTS dengan benar",
        "Menghindari jebakan NOT IN dan NULL",
        "Memecah query rumit dengan CTE dan agregasi dua tingkat",
    ],
    [l1, l2, l3],
    video,
    REF,
)
