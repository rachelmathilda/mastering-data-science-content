import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

SQL_DB = """
CREATE TABLE pelanggan (id INTEGER PRIMARY KEY, nama TEXT, kota TEXT, daftar TEXT);
CREATE TABLE produk (id INTEGER PRIMARY KEY, nama TEXT, kategori TEXT, harga INTEGER);
CREATE TABLE pesanan (id INTEGER PRIMARY KEY, pelanggan_id INTEGER, tanggal TEXT, status TEXT);
CREATE TABLE item (pesanan_id INTEGER, produk_id INTEGER, qty INTEGER);
INSERT INTO pelanggan VALUES
(1, 'Ani', 'Jakarta', '2026-01-05'),
(2, 'Budi', 'Bandung', '2026-01-20'),
(3, 'Citra', 'Jakarta', '2026-02-03'),
(4, 'Dewi', 'Surabaya', '2026-02-15'),
(5, 'Eko', 'Medan', '2026-03-01');
INSERT INTO produk VALUES
(1, 'Pensil', 'ATK', 2500),
(2, 'Buku', 'ATK', 12000),
(3, 'Tas', 'Fashion', 150000),
(4, 'Botol', 'Rumah', 35000),
(5, 'Lampu', 'Rumah', 20000);
INSERT INTO pesanan VALUES
(1, 1, '2026-01-10', 'selesai'),
(2, 2, '2026-01-25', 'selesai'),
(3, 1, '2026-02-05', 'selesai'),
(4, 3, '2026-02-10', 'batal'),
(5, 3, '2026-02-20', 'selesai'),
(6, 4, '2026-03-02', 'selesai'),
(7, 1, '2026-03-10', 'selesai'),
(8, 2, '2026-03-15', 'selesai'),
(9, 5, '2026-03-20', 'selesai');
INSERT INTO item VALUES
(1, 1, 10), (1, 2, 2), (2, 3, 1), (3, 4, 1), (3, 1, 4), (4, 3, 1), (5, 2, 3),
(5, 5, 2), (6, 3, 1), (6, 1, 2), (7, 5, 5), (8, 4, 2), (9, 2, 1), (9, 4, 1);
"""

SETUP = textwrap.indent("import sqlite3\n\nc = sqlite3.connect(':memory:')\nc.executescript('''" + SQL_DB + "''')\n", '            ')

FIX = textwrap.indent("import sqlite3\n\ndef _db():\n    c = sqlite3.connect(':memory:')\n    c.executescript('''" + textwrap.indent(SQL_DB, '    ') + "    ''')\n    return c\n\n", '            ')
BASE_SQL = "FROM pesanan o JOIN item i ON i.pesanan_id = o.id JOIN produk k ON k.id = i.produk_id WHERE o.status = 'selesai'"

l1 = lesson(
    "A6-09-1",
    "Memahami data dan metrik dasar penjualan",
    35,
    [
        "Memetakan tabel dan relasi sebelum menulis query analitik",
        "Menghitung pendapatan dengan JOIN dan menyaring pesanan batal",
        "Menghindari kesalahan hitung akibat fan-out",
        "Menyusun metrik per bulan dan per kategori serta nilai rata-rata pesanan",
    ],
    [
        T("""
        ## Analisis sungguhan dimulai dari pertanyaan

        Modul penutup ini menyatukan semua yang sudah dipelajari: SELECT, filter, agregasi, JOIN, subquery, CTE, window function, dan fungsi tanggal. Kita memakai satu kasus utuh, yaitu toko daring kecil, dan menjawab pertanyaan bisnis seperti seorang analis: berapa pendapatan, siapa pelanggan terbaik, dan bagaimana tren bulanan.

        Kunci analisis yang baik adalah memulai dari pertanyaan, bukan dari query. Tulis dulu apa yang ingin diketahui dan keputusan apa yang akan diambil dari jawabannya, baru pilih tabel dan rumusnya.
        """),
        T("""
        ## Memetakan skema

        Ada empat tabel. `pelanggan` memuat nama, kota, dan tanggal daftar. `produk` memuat nama, kategori, dan harga. `pesanan` memuat pelanggan, tanggal, dan status, yaitu `selesai` atau `batal`. `item` memuat rincian: pesanan mana, produk apa, dan berapa `qty`.

        Perhatikan bahwa nilai uang tidak tersimpan langsung. Nilai sebuah baris item adalah `qty * harga`, dihitung dengan menggabungkan `item` dan `produk`. Memahami di mana tiap fakta tinggal adalah langkah pertama sebelum menulis JOIN.
        """),
        T("""
        ## Definisikan metrik dengan jelas

        Sebelum menghitung, sepakati definisi. **Pendapatan** di sini adalah jumlah `qty * harga` dari pesanan berstatus `selesai`. Pesanan `batal` tidak dihitung. Satu pesanan dapat berisi banyak item, jadi **nilai pesanan** adalah jumlah semua itemnya.

        Definisi yang tidak jelas melahirkan angka yang saling bertentangan antar laporan. Tuliskan definisi sebagai komentar di dekat query atau di dokumentasi tim agar semua orang menghitung dengan cara yang sama.
        """),
        C(
            SETUP + """
            q = '''
            SELECT COUNT(DISTINCT o.id), SUM(i.qty * k.harga)
            FROM pesanan o
            JOIN item i ON i.pesanan_id = o.id
            JOIN produk k ON k.id = i.produk_id
            WHERE o.status = 'selesai'
            '''
            print(c.execute(q).fetchone())
            q = '''
            SELECT COUNT(*) FROM pesanan o JOIN item i ON i.pesanan_id = o.id
            WHERE o.status = 'selesai'
            '''
            print(c.execute(q).fetchone())
            print(c.execute("SELECT COUNT(*) FROM pesanan WHERE status = 'selesai'").fetchone())
            """,
            """
            (8, 692000)
            (13,)
            (8,)
            """,
            """
            Ada delapan pesanan selesai dengan pendapatan 692.000. Menghitung baris setelah JOIN ke item memberi tiga belas, bukan delapan, karena satu pesanan punya banyak item.
            """,
            filename="pendapatan_total.py",
        ),
        T("""
        ## Fan-out

        Peristiwa tadi disebut **fan-out**: JOIN satu-ke-banyak menggandakan baris sisi satu. Bila kita menghitung `COUNT(*)` setelah JOIN ke item, hasilnya jumlah item, bukan jumlah pesanan. Menjumlahkan kolom milik pesanan, seperti ongkos kirim, setelah JOIN seperti itu akan menghitung ganda.

        Pertahanannya: hitung banyak pesanan dengan `COUNT(DISTINCT o.id)`, dan jumlahkan hanya kolom milik sisi banyak, seperti `qty * harga`. Atau agregasi dulu di tingkat item sebelum digabung dengan pesanan.
        """),
        T("""
        ## Pendapatan per bulan

        Laporan paling umum adalah pendapatan per bulan. Kelompokkan menurut `strftime('%Y-%m', o.tanggal)` dan jumlahkan nilai item. Karena format tahun-bulan terurut kronologis secara alfabet, `ORDER BY` langsung benar.

        Jangan lupa menyaring status. Memasukkan pesanan batal akan menggelembungkan pendapatan, dan kesalahan semacam ini sering baru terlihat setelah laporan beredar. Biasakan menuliskan filter status sebagai syarat pertama di setiap query penjualan.
        """),
        C(
            SETUP + """
            q = '''
            SELECT strftime('%Y-%m', o.tanggal) AS bulan, SUM(i.qty * k.harga)
            FROM pesanan o
            JOIN item i ON i.pesanan_id = o.id
            JOIN produk k ON k.id = i.produk_id
            WHERE o.status = 'selesai'
            GROUP BY bulan ORDER BY bulan
            '''
            print(c.execute(q).fetchall())
            """,
            """
            [('2026-01', 199000), ('2026-02', 121000), ('2026-03', 372000)]
            """,
            """
            Pendapatan per bulan: Januari 199.000, Februari 121.000 yang turun, dan Maret 372.000 yang melonjak.
            """,
            filename="pendapatan_bulan.py",
        ),
        T("""
        ## Pendapatan per kategori

        Pertanyaan berikutnya: kategori mana yang paling menyumbang? Kelompokkan menurut `k.kategori`. Urutkan dari terbesar dan tambahkan nama kategori sebagai pemutus seri agar hasil deterministik.

        Perhatikan satu pola yang sering muncul di analisis: setiap pertanyaan baru hanyalah mengganti kunci `GROUP BY`, sedangkan fondasi JOIN dan filter tetap sama. Menyiapkan fondasi itu sekali lalu memakainya ulang menghemat banyak waktu.
        """),
        C(
            SETUP + """
            q = '''
            SELECT k.kategori, SUM(i.qty * k.harga) AS total
            FROM pesanan o
            JOIN item i ON i.pesanan_id = o.id
            JOIN produk k ON k.id = i.produk_id
            WHERE o.status = 'selesai'
            GROUP BY k.kategori ORDER BY total DESC, k.kategori
            '''
            print(c.execute(q).fetchall())
            q = '''
            SELECT ROUND(SUM(i.qty * k.harga) * 1.0 / COUNT(DISTINCT o.id), 1)
            FROM pesanan o
            JOIN item i ON i.pesanan_id = o.id
            JOIN produk k ON k.id = i.produk_id
            WHERE o.status = 'selesai'
            '''
            print(c.execute(q).fetchone())
            """,
            """
            [('Fashion', 300000), ('Rumah', 280000), ('ATK', 112000)]
            (86500.0,)
            """,
            """
            Kategori fashion terbesar dengan 300.000, dan nilai rata-rata pesanan 86.500 diperoleh dari total dibagi jumlah pesanan unik.
            """,
            filename="kategori_aov.py",
        ),
        T("""
        ## Nilai rata-rata pesanan

        **Nilai rata-rata pesanan**, atau AOV, adalah pendapatan dibagi jumlah pesanan. Ini metrik standar toko daring karena menunjukkan seberapa besar rata-rata belanja sekali transaksi. Perhatikan penyebutnya: harus jumlah pesanan unik, bukan jumlah baris item.

        Dengan fan-out, `AVG` atas baris item memberi rata-rata nilai item, bukan rata-rata pesanan. Dua angka itu berbeda jauh dan menjawab pertanyaan yang berbeda, jadi pilih dengan sadar.
        """),
        T("""
        ## Memverifikasi hasil

        Setelah menulis query, periksa kewajarannya. Jumlahkan pendapatan per bulan: apakah sama dengan total keseluruhan? Hitung jumlah pesanan dari dua jalur berbeda: apakah cocok? Perbandingan silang seperti ini menangkap kesalahan JOIN dan filter dengan cepat.

        Kebiasaan **rekonsiliasi** ini membedakan analis yang dapat dipercaya. Angka yang cocok dari dua jalur memberi keyakinan, sedangkan angka yang tidak cocok adalah petunjuk bahwa ada yang perlu diperiksa.
        """),
        K(
            "tip",
            """
            Setelah JOIN satu-ke-banyak, hitung entitas sisi satu dengan COUNT(DISTINCT id) dan rekonsiliasi total dari dua jalur.
            """,
            title="Rekonsiliasi",
        ),
        T("""
        ## Membaca data sebelum menganalisis

        Luangkan waktu menjelajahi tabel sebelum menulis query analitik. Lihat beberapa baris, hitung jumlah baris tiap tabel, dan periksa nilai unik pada kolom status. Langkah singkat ini sering mengungkap kejutan, misalnya status tak terduga atau pelanggan tanpa pesanan.

        Pengenalan data yang baik mencegah asumsi keliru. Analisis yang dibangun di atas asumsi yang belum diperiksa mudah runtuh saat seseorang bertanya dari mana angkanya berasal.
        """),
        E(
            "A6-09-1-ex1",
            "mudah",
            """
            Tulis fungsi `total_pendapatan(c)` yang mengembalikan total `qty * harga` seluruh item pada pesanan berstatus `selesai`.
            """,
            """
            import sqlite3

            def total_pendapatan(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert total_pendapatan(c) == 692000
            c.execute('INSERT INTO item VALUES (9, 3, 1)')
            assert total_pendapatan(c) == 842000
            c.execute('INSERT INTO item VALUES (4, 3, 5)')
            assert total_pendapatan(c) == 842000
            """,
            "Gabungkan pesanan, item, dan produk lalu saring status selesai.",
            """
            import sqlite3

            def total_pendapatan(c):
                q = '''
                SELECT SUM(i.qty * k.harga)
                FROM pesanan o
                JOIN item i ON i.pesanan_id = o.id
                JOIN produk k ON k.id = i.produk_id
                WHERE o.status = 'selesai'
                '''
                return c.execute(q).fetchone()[0]
            """,
        ),
        E(
            "A6-09-1-ex2",
            "sedang",
            """
            Tulis fungsi `pendapatan_per_bulan(c)` yang mengembalikan list tuple `(bulan, total)` dengan bulan berformat `YYYY-MM`, terurut kronologis, hanya untuk pesanan `selesai`.
            """,
            """
            import sqlite3

            def pendapatan_per_bulan(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert pendapatan_per_bulan(c) == [('2026-01', 199000), ('2026-02', 121000), ('2026-03', 372000)]
            c.execute("INSERT INTO pesanan VALUES (10, 1, '2026-04-02', 'selesai')")
            c.execute('INSERT INTO item VALUES (10, 3, 1)')
            assert pendapatan_per_bulan(c)[-1] == ('2026-04', 150000)
            c.execute("INSERT INTO pesanan VALUES (11, 1, '2026-05-02', 'batal')")
            c.execute('INSERT INTO item VALUES (11, 3, 1)')
            assert len(pendapatan_per_bulan(c)) == 4
            """,
            "GROUP BY strftime tahun dan bulan lalu jumlahkan qty kali harga.",
            """
            import sqlite3

            def pendapatan_per_bulan(c):
                q = '''
                SELECT strftime('%Y-%m', o.tanggal) AS bulan, SUM(i.qty * k.harga)
                FROM pesanan o
                JOIN item i ON i.pesanan_id = o.id
                JOIN produk k ON k.id = i.produk_id
                WHERE o.status = 'selesai'
                GROUP BY bulan ORDER BY bulan
                '''
                return c.execute(q).fetchall()
            """,
        ),
        E(
            "A6-09-1-ex3",
            "sedang",
            """
            Tulis fungsi `pendapatan_per_kategori(c)` yang mengembalikan list tuple `(kategori, total)` untuk pesanan `selesai`, terurut dari total terbesar lalu nama kategori.
            """,
            """
            import sqlite3

            def pendapatan_per_kategori(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert pendapatan_per_kategori(c) == [('Fashion', 300000), ('Rumah', 280000), ('ATK', 112000)]
            c.execute('INSERT INTO item VALUES (9, 2, 100)')
            assert pendapatan_per_kategori(c)[0] == ('ATK', 1312000)
            c.execute("INSERT INTO produk VALUES (6, 'Kursi', 'Rumah', 500000)")
            c.execute('INSERT INTO item VALUES (9, 6, 1)')
            assert pendapatan_per_kategori(c)[0] == ('ATK', 1312000)
            """,
            "GROUP BY kategori produk dengan filter status.",
            """
            import sqlite3

            def pendapatan_per_kategori(c):
                q = '''
                SELECT k.kategori, SUM(i.qty * k.harga) AS total
                FROM pesanan o
                JOIN item i ON i.pesanan_id = o.id
                JOIN produk k ON k.id = i.produk_id
                WHERE o.status = 'selesai'
                GROUP BY k.kategori ORDER BY total DESC, k.kategori
                '''
                return c.execute(q).fetchall()
            """,
        ),
        E(
            "A6-09-1-ex4",
            "menantang",
            """
            Tulis fungsi `rata_nilai_pesanan(c)` yang mengembalikan nilai rata-rata pesanan `selesai` (total pendapatan dibagi jumlah pesanan unik), dibulatkan 1 desimal.
            """,
            """
            import sqlite3

            def rata_nilai_pesanan(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert rata_nilai_pesanan(c) == 86500.0
            c.execute('INSERT INTO item VALUES (9, 3, 1)')
            assert rata_nilai_pesanan(c) == 105250.0
            c.execute("INSERT INTO pesanan VALUES (10, 1, '2026-04-02', 'batal')")
            c.execute('INSERT INTO item VALUES (10, 3, 9)')
            assert rata_nilai_pesanan(c) == 105250.0
            """,
            "Bagi total dengan COUNT(DISTINCT o.id) dan kalikan 1.0.",
            """
            import sqlite3

            def rata_nilai_pesanan(c):
                q = '''
                SELECT ROUND(SUM(i.qty * k.harga) * 1.0 / COUNT(DISTINCT o.id), 1)
                FROM pesanan o
                JOIN item i ON i.pesanan_id = o.id
                JOIN produk k ON k.id = i.produk_id
                WHERE o.status = 'selesai'
                '''
                return c.execute(q).fetchone()[0]
            """,
        ),
    ],
    [
        M("Menghitung COUNT(*) setelah JOIN ke item sebagai jumlah pesanan.", "Gunakan COUNT(DISTINCT o.id)."),
        M("Lupa menyaring pesanan batal.", "Tulis filter status di setiap query penjualan."),
        M("Memakai AVG atas baris item untuk rata-rata pesanan.", "Bagi total dengan jumlah pesanan unik."),
    ],
    [
        Q("Fan-out terjadi karena?", ["JOIN satu-ke-banyak menggandakan baris", "NULL", "ORDER BY", "LIMIT"], 0, "Baris sisi satu berulang.", hint="Gandakan."),
        Q("Jumlah pesanan setelah JOIN item dihitung dengan?", ["COUNT(DISTINCT o.id)", "COUNT(*)", "SUM(qty)", "MAX(id)"], 0, "Pesanan unik.", hint="Distinct."),
        Q("Nilai baris item dihitung?", ["qty dikali harga", "qty ditambah harga", "harga saja", "qty saja"], 0, "Kuantitas kali harga.", hint="Kali."),
        Q("Rekonsiliasi berarti?", ["Membandingkan angka dari dua jalur", "Menghapus data", "Mengurutkan", "Membuat index"], 0, "Pemeriksaan silang.", hint="Silang."),
        Q("Status yang tidak dihitung sebagai pendapatan?", ["batal", "selesai", "semua", "tidak ada"], 0, "Pesanan batal.", hint="Batal."),
    ],
    [
        "Mulai dari pertanyaan dan definisi metrik yang jelas.",
        "Waspadai fan-out saat JOIN satu-ke-banyak.",
        "Setiap pertanyaan baru sering hanya mengganti kunci GROUP BY.",
        "Rekonsiliasi angka dari dua jalur untuk menangkap kesalahan.",
    ],
    [],
)

l2 = lesson(
    "A6-09-2",
    "Analisis pelanggan",
    35,
    [
        "Memeringkat pelanggan berdasarkan total belanja",
        "Mengidentifikasi pelanggan berulang dan menghitung tingkat pembelian ulang",
        "Menghitung recency dengan selisih hari",
        "Mengambil pelanggan teratas per kota dengan window function",
    ],
    [
        T("""
        ## Dari produk ke pelanggan

        Pelajaran sebelumnya melihat toko dari sisi uang. Sekarang kita melihatnya dari sisi manusia: siapa yang membeli, seberapa sering, dan seberapa baru. Pemahaman pelanggan mendasari keputusan seperti siapa yang diberi promo, siapa yang perlu diingatkan, dan kota mana yang layak digarap.

        Fondasi query tetap sama, yaitu pesanan selesai digabung ke item dan produk. Perbedaannya hanya pada kunci pengelompokan, yang kini berupa pelanggan.
        """),
        T("""
        ## Peringkat belanja

        Total belanja per pelanggan diperoleh dengan menggabungkan `pelanggan` ke `pesanan`, `item`, dan `produk`, lalu mengelompokkan menurut pelanggan. Urutkan menurun dan beri nama pelanggan sebagai pemutus seri agar hasil stabil.

        Saat mengelompokkan menurut `g.id`, pilih juga `g.nama` yang bergantung penuh pada id itu. SQLite mengizinkannya, tetapi kebiasaan baik adalah menyertakan semua kolom non-agregat di `GROUP BY` bila basis data lain dipakai.
        """),
        C(
            SETUP + """
            q = '''
            SELECT g.nama, SUM(i.qty * k.harga) AS total
            FROM pelanggan g
            JOIN pesanan o ON o.pelanggan_id = g.id
            JOIN item i ON i.pesanan_id = o.id
            JOIN produk k ON k.id = i.produk_id
            WHERE o.status = 'selesai'
            GROUP BY g.id, g.nama ORDER BY total DESC, g.nama
            '''
            for r in c.execute(q).fetchall():
                print(r)
            """,
            """
            ('Budi', 220000)
            ('Ani', 194000)
            ('Dewi', 155000)
            ('Citra', 76000)
            ('Eko', 47000)
            """,
            """
            Budi menjadi pelanggan terbesar dengan 220.000, diikuti Ani, Dewi, Citra, dan Eko.
            """,
            filename="belanja_pelanggan.py",
        ),
        T("""
        ## Pelanggan berulang

        **Pelanggan berulang** adalah yang membeli lebih dari satu kali. Hitung pesanan selesai per pelanggan lalu saring dengan `HAVING COUNT(*) >= 2`. Di sini kita menghitung baris pesanan, bukan item, sehingga tidak perlu `DISTINCT` selama tidak ada JOIN ke item.

        **Tingkat pembelian ulang** adalah persentase pelanggan berulang di antara semua pelanggan yang pernah membeli. Ini indikator loyalitas yang murah dihitung namun sangat informatif.
        """),
        C(
            SETUP + """
            q = '''
            SELECT g.nama, COUNT(*) FROM pelanggan g
            JOIN pesanan o ON o.pelanggan_id = g.id
            WHERE o.status = 'selesai'
            GROUP BY g.id, g.nama HAVING COUNT(*) >= 2 ORDER BY g.id
            '''
            print(c.execute(q).fetchall())
            q = '''
            WITH n AS (
                SELECT pelanggan_id, COUNT(*) AS banyak FROM pesanan
                WHERE status = 'selesai' GROUP BY pelanggan_id
            )
            SELECT COUNT(*), SUM(banyak >= 2), ROUND(100.0 * SUM(banyak >= 2) / COUNT(*), 1) FROM n
            '''
            print(c.execute(q).fetchone())
            """,
            """
            [('Ani', 3), ('Budi', 2)]
            (5, 2, 40.0)
            """,
            """
            Ani dan Budi membeli berulang, sehingga dari lima pelanggan pembeli tingkat pembelian ulang adalah empat puluh persen.
            """,
            filename="pelanggan_berulang.py",
        ),
        T("""
        ## Recency

        **Recency** menghitung sudah berapa hari sejak pembelian terakhir. Ambil `MAX(o.tanggal)` per pelanggan, lalu kurangkan dari tanggal acuan memakai `julianday`. Kirim tanggal acuan sebagai konstanta atau parameter, bukan `'now'`, agar laporan dapat diulang dengan hasil sama.

        Pelanggan dengan recency besar adalah calon yang mulai menghilang, dan sasaran kampanye pemulihan. Recency bersama frekuensi dan nilai belanja membentuk kerangka RFM yang terkenal di pemasaran.
        """),
        C(
            SETUP + """
            q = '''
            SELECT g.nama, MAX(o.tanggal),
                   CAST(julianday('2026-03-31') - julianday(MAX(o.tanggal)) AS INTEGER)
            FROM pelanggan g JOIN pesanan o ON o.pelanggan_id = g.id
            WHERE o.status = 'selesai'
            GROUP BY g.id, g.nama ORDER BY g.id
            '''
            for r in c.execute(q).fetchall():
                print(r)
            """,
            """
            ('Ani', '2026-03-10', 21)
            ('Budi', '2026-03-15', 16)
            ('Citra', '2026-02-20', 39)
            ('Dewi', '2026-03-02', 29)
            ('Eko', '2026-03-20', 11)
            """,
            """
            Citra paling lama tidak membeli, yaitu tiga puluh sembilan hari sebelum tanggal acuan.
            """,
            filename="recency.py",
        ),
        T("""
        ## Kohort pendaftaran

        **Kohort** mengelompokkan pelanggan menurut bulan pendaftaran lalu melihat kapan mereka membeli. Gabungkan `strftime('%Y-%m', g.daftar)` sebagai kohort dengan `strftime('%Y-%m', o.tanggal)` sebagai bulan beli, lalu hitung pelanggan unik per pasangan.

        Tabel kohort menjawab pertanyaan penting: apakah pelanggan yang mendaftar Januari masih membeli di Maret? Penghitungan memakai `COUNT(DISTINCT g.id)` karena satu pelanggan bisa membeli beberapa kali dalam sebulan.
        """),
        C(
            SETUP + """
            q = '''
            SELECT strftime('%Y-%m', g.daftar) AS kohort, strftime('%Y-%m', o.tanggal) AS bulan,
                   COUNT(DISTINCT g.id)
            FROM pelanggan g JOIN pesanan o ON o.pelanggan_id = g.id
            WHERE o.status = 'selesai'
            GROUP BY kohort, bulan ORDER BY kohort, bulan
            '''
            for r in c.execute(q).fetchall():
                print(r)
            """,
            """
            ('2026-01', '2026-01', 2)
            ('2026-01', '2026-02', 1)
            ('2026-01', '2026-03', 2)
            ('2026-02', '2026-02', 1)
            ('2026-02', '2026-03', 1)
            ('2026-03', '2026-03', 1)
            """,
            """
            Kohort Januari punya dua pelanggan aktif di Januari dan tetap dua di Maret, tanda retensi yang baik.
            """,
            filename="kohort.py",
        ),
        T("""
        ## Pelanggan teratas per kota

        Untuk menemukan pelanggan terbesar di tiap kota, gabungkan agregasi dengan window function. Hitung total belanja per pelanggan lalu beri nomor urut dalam kota memakai `ROW_NUMBER() OVER (PARTITION BY kota ORDER BY total DESC, nama)`. Saring nomor satu di lapisan luar.

        Agregat boleh dipakai di dalam `ORDER BY` window function karena window dievaluasi setelah `GROUP BY`. Ini contoh bagaimana dua alat yang dipelajari terpisah bekerja bersama.
        """),
        T("""
        ## Menafsirkan hasil dengan hati-hati

        Angka pada contoh kecil ini hanya untuk latihan. Dengan lima pelanggan, satu pembelian besar mengubah seluruh gambaran. Pada data sungguhan, perhatikan ukuran sampel sebelum menarik kesimpulan, dan pertimbangkan apakah perbedaan antar kelompok benar-benar berarti.

        Query yang benar belum tentu analisis yang benar. Keduanya berbeda: yang pertama soal sintaks dan logika, yang kedua soal memilih pertanyaan yang tepat dan menafsirkan jawabannya dengan jujur.
        """),
        K(
            "tip",
            """
            Gunakan tanggal acuan tetap untuk recency agar laporan dapat diulang dan diuji.
            """,
            title="Tanggal acuan",
        ),
        T("""
        ## Segmentasi sederhana

        Dari peringkat belanja dan frekuensi, kita dapat membentuk segmen praktis. Pelanggan dengan belanja tinggi dan pembelian berulang adalah yang paling bernilai dan layak dijaga. Pelanggan belanja tinggi tetapi sekali beli adalah peluang untuk didorong kembali. Pelanggan belanja kecil dan jarang adalah yang paling rendah prioritasnya.

        Segmentasi tidak harus rumit. Aturan sederhana yang dipahami semua orang sering lebih berguna daripada model canggih yang tidak dipercaya.
        """),
        T("""
        ## Pelanggan tanpa pembelian

        Tidak semua pelanggan yang terdaftar pernah membeli. Untuk menemukan mereka, gunakan `NOT EXISTS` terhadap pesanan selesai, atau `LEFT JOIN` dengan penyaringan `IS NULL`. Hasilnya adalah daftar calon sasaran aktivasi.

        Perhatikan bahwa JOIN biasa dari pelanggan ke pesanan membuang pelanggan tanpa pesanan secara diam-diam. Itu sebabnya perhitungan seperti tingkat pembelian ulang harus menetapkan penyebut dengan jelas: semua pelanggan terdaftar atau hanya yang pernah membeli.
        """),
        E(
            "A6-09-2-ex1",
            "mudah",
            """
            Tulis fungsi `belanja_pelanggan(c)` yang mengembalikan list tuple `(nama, total)` total belanja pelanggan pada pesanan `selesai`, terurut dari total terbesar lalu nama.
            """,
            """
            import sqlite3

            def belanja_pelanggan(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            r = belanja_pelanggan(c)
            assert r[0] == ('Budi', 220000)
            assert r == [('Budi', 220000), ('Ani', 194000), ('Dewi', 155000), ('Citra', 76000), ('Eko', 47000)]
            c.execute('INSERT INTO item VALUES (9, 3, 2)')
            assert belanja_pelanggan(c)[0] == ('Eko', 347000)
            """,
            "Gabungkan empat tabel, saring selesai, GROUP BY pelanggan.",
            """
            import sqlite3

            def belanja_pelanggan(c):
                q = '''
                SELECT g.nama, SUM(i.qty * k.harga) AS total
                FROM pelanggan g
                JOIN pesanan o ON o.pelanggan_id = g.id
                JOIN item i ON i.pesanan_id = o.id
                JOIN produk k ON k.id = i.produk_id
                WHERE o.status = 'selesai'
                GROUP BY g.id, g.nama ORDER BY total DESC, g.nama
                '''
                return c.execute(q).fetchall()
            """,
        ),
        E(
            "A6-09-2-ex2",
            "sedang",
            """
            Tulis fungsi `pelanggan_berulang(c, minimal)` yang mengembalikan list nama pelanggan dengan paling sedikit `minimal` pesanan `selesai`, terurut menurut id pelanggan.
            """,
            """
            import sqlite3

            def pelanggan_berulang(c, minimal):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert pelanggan_berulang(c, 2) == ['Ani', 'Budi']
            assert pelanggan_berulang(c, 3) == ['Ani']
            assert pelanggan_berulang(c, 4) == []
            assert pelanggan_berulang(c, 1) == ['Ani', 'Budi', 'Citra', 'Dewi', 'Eko']
            """,
            "GROUP BY pelanggan lalu HAVING COUNT(*) >= minimal.",
            """
            import sqlite3

            def pelanggan_berulang(c, minimal):
                q = '''
                SELECT g.nama FROM pelanggan g
                JOIN pesanan o ON o.pelanggan_id = g.id
                WHERE o.status = 'selesai'
                GROUP BY g.id, g.nama HAVING COUNT(*) >= ? ORDER BY g.id
                '''
                return [r[0] for r in c.execute(q, (minimal,)).fetchall()]
            """,
        ),
        E(
            "A6-09-2-ex3",
            "sedang",
            """
            Tulis fungsi `recency(c, acuan)` yang mengembalikan list tuple `(nama, hari)` berisi jumlah hari dari pembelian `selesai` terakhir tiap pelanggan sampai tanggal `acuan` (teks `YYYY-MM-DD`), terurut menurut id pelanggan.
            """,
            """
            import sqlite3

            def recency(c, acuan):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert recency(c, '2026-03-31') == [('Ani', 21), ('Budi', 16), ('Citra', 39), ('Dewi', 29), ('Eko', 11)]
            assert recency(c, '2026-04-10')[0] == ('Ani', 31)
            assert recency(c, '2026-03-20')[-1] == ('Eko', 0)
            """,
            "Ambil MAX tanggal per pelanggan dan kurangkan dengan julianday.",
            """
            import sqlite3

            def recency(c, acuan):
                q = '''
                SELECT g.nama, CAST(ROUND(julianday(?) - julianday(MAX(o.tanggal))) AS INTEGER)
                FROM pelanggan g JOIN pesanan o ON o.pelanggan_id = g.id
                WHERE o.status = 'selesai'
                GROUP BY g.id, g.nama ORDER BY g.id
                '''
                return c.execute(q, (acuan,)).fetchall()
            """,
        ),
        E(
            "A6-09-2-ex4",
            "menantang",
            """
            Tulis fungsi `teratas_per_kota(c)` yang mengembalikan list tuple `(kota, nama)` berisi pelanggan dengan total belanja `selesai` terbesar di tiap kota, terurut menurut kota. Bila seri, pilih nama yang lebih awal secara alfabet.
            """,
            """
            import sqlite3

            def teratas_per_kota(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert teratas_per_kota(c) == [('Bandung', 'Budi'), ('Jakarta', 'Ani'), ('Medan', 'Eko'), ('Surabaya', 'Dewi')]
            c.execute("INSERT INTO pesanan VALUES (10, 3, '2026-03-25', 'selesai')")
            c.execute('INSERT INTO item VALUES (10, 3, 2)')
            assert teratas_per_kota(c)[1] == ('Jakarta', 'Citra')
            c.execute("DELETE FROM item WHERE pesanan_id = 10")
            assert teratas_per_kota(c)[1] == ('Jakarta', 'Ani')
            """,
            "ROW_NUMBER dengan PARTITION BY kota dan ORDER BY agregat menurun lalu nama.",
            """
            import sqlite3

            def teratas_per_kota(c):
                q = '''
                SELECT kota, nama FROM (
                    SELECT g.kota AS kota, g.nama AS nama,
                           ROW_NUMBER() OVER (
                               PARTITION BY g.kota
                               ORDER BY SUM(i.qty * k.harga) DESC, g.nama
                           ) AS rn
                    FROM pelanggan g
                    JOIN pesanan o ON o.pelanggan_id = g.id
                    JOIN item i ON i.pesanan_id = o.id
                    JOIN produk k ON k.id = i.produk_id
                    WHERE o.status = 'selesai'
                    GROUP BY g.id, g.kota, g.nama
                )
                WHERE rn = 1 ORDER BY kota
                '''
                return c.execute(q).fetchall()
            """,
        ),
    ],
    [
        M("Menghitung pesanan setelah JOIN ke item tanpa DISTINCT.", "Hitung dari tabel pesanan atau pakai COUNT(DISTINCT)."),
        M("Memakai 'now' untuk recency di laporan yang harus diulang.", "Pakai tanggal acuan tetap."),
        M("Menarik kesimpulan dari sampel sangat kecil.", "Periksa ukuran sampel dan kewajaran."),
    ],
    [
        Q("Pelanggan berulang adalah?", ["Membeli lebih dari satu kali", "Membeli sekali", "Belum membeli", "Membatalkan"], 0, "Dua pesanan atau lebih.", hint="Ulang."),
        Q("Recency mengukur?", ["Hari sejak pembelian terakhir", "Total belanja", "Jumlah pesanan", "Harga rata-rata"], 0, "Seberapa baru.", hint="Baru."),
        Q("Kohort mengelompokkan menurut?", ["Bulan pendaftaran", "Harga", "Kota saja", "Kategori"], 0, "Waktu masuk.", hint="Daftar."),
        Q("Pelanggan teratas per kota memakai?", ["ROW_NUMBER dengan PARTITION BY kota", "LIMIT 1", "DISTINCT", "UNION"], 0, "Top N per kelompok.", hint="Partisi."),
        Q("Tingkat pembelian ulang adalah?", ["Persen pelanggan berulang", "Total pendapatan", "Rata-rata harga", "Jumlah kota"], 0, "Berulang dibanding semua.", hint="Persen."),
    ],
    [
        "Pelanggan diperingkat dari total belanja yang digabung empat tabel.",
        "Pelanggan berulang dan tingkat pembelian ulang mengukur loyalitas.",
        "Recency dihitung dengan selisih hari dari tanggal acuan tetap.",
        "Window function mengambil pelanggan teratas per kota.",
    ],
    [],
)

l3 = lesson(
    "A6-09-3",
    "Laporan akhir: tren, kontribusi, dan pivot",
    35,
    [
        "Menghitung pertumbuhan bulanan dan total kumulatif",
        "Menghitung kontribusi produk terhadap total",
        "Membuat tabel pivot dengan agregasi bersyarat",
        "Menyusun laporan berlapis dengan CTE dan memverifikasinya",
    ],
    [
        T("""
        ## Menyusun laporan

        Bagian akhir ini merangkai potongan analisis menjadi laporan yang dapat dibaca pemangku kepentingan: tren pendapatan, kontribusi produk, dan tabel ringkas per kategori dan bulan. Alat yang dipakai adalah CTE untuk menyusun langkah, window function untuk perbandingan, dan agregasi bersyarat untuk pivot.

        Laporan yang baik menjawab satu pertanyaan jelas per bagian, memakai definisi yang konsisten, dan bisa direkonsiliasi dengan angka lain.
        """),
        T("""
        ## Pertumbuhan bulanan

        Pertumbuhan bulan ke bulan dihitung dengan `LAG` atas total bulanan: selisih dibagi nilai bulan sebelumnya, dikali seratus. Bulan pertama tidak punya pembanding sehingga hasilnya `NULL`, yang memang jujur menyatakan tidak ada data pembanding.

        Susun dalam dua langkah: CTE pertama menghitung total per bulan, query utama menambahkan `LAG`. Memisahkan langkah membuat tiap bagian mudah diperiksa terpisah.
        """),
        C(
            SETUP + """
            q = '''
            WITH b AS (
                SELECT strftime('%Y-%m', o.tanggal) AS bulan, SUM(i.qty * k.harga) AS total
                FROM pesanan o
                JOIN item i ON i.pesanan_id = o.id
                JOIN produk k ON k.id = i.produk_id
                WHERE o.status = 'selesai'
                GROUP BY bulan
            )
            SELECT bulan, total,
                   ROUND(100.0 * (total - LAG(total) OVER (ORDER BY bulan)) / LAG(total) OVER (ORDER BY bulan), 1),
                   SUM(total) OVER (ORDER BY bulan ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
            FROM b ORDER BY bulan
            '''
            for r in c.execute(q).fetchall():
                print(r)
            """,
            """
            ('2026-01', 199000, None, 199000)
            ('2026-02', 121000, -39.2, 320000)
            ('2026-03', 372000, 207.4, 692000)
            """,
            """
            Pendapatan turun tiga puluh sembilan koma dua persen di Februari lalu melonjak dua ratus tujuh koma empat persen di Maret, dan total kumulatif berakhir di 692.000.
            """,
            filename="pertumbuhan_kumulatif.py",
        ),
        T("""
        ## Kontribusi dan Pareto

        **Kontribusi** adalah persentase tiap produk terhadap total pendapatan, dihitung dengan `100.0 * nilai / SUM(nilai) OVER ()`. Kontribusi kumulatif, setelah produk diurutkan dari terbesar, menunjukkan seberapa terkonsentrasi pendapatan, gagasan di balik prinsip Pareto: sedikit produk sering menyumbang sebagian besar hasil.

        Pada contoh kita, satu produk menyumbang lebih dari empat puluh persen. Informasi ini membantu memutuskan produk mana yang layak dijaga stoknya dan diprioritaskan promosinya.
        """),
        C(
            SETUP + """
            q = '''
            WITH t AS (
                SELECT k.nama AS nama, SUM(i.qty * k.harga) AS v
                FROM pesanan o
                JOIN item i ON i.pesanan_id = o.id
                JOIN produk k ON k.id = i.produk_id
                WHERE o.status = 'selesai'
                GROUP BY k.id, k.nama
            )
            SELECT nama, v, ROUND(100.0 * v / SUM(v) OVER (), 1),
                   ROUND(100.0 * SUM(v) OVER (ORDER BY v DESC, nama) / SUM(v) OVER (), 1)
            FROM t ORDER BY v DESC, nama
            '''
            for r in c.execute(q).fetchall():
                print(r)
            """,
            """
            ('Tas', 300000, 43.4, 43.4)
            ('Botol', 140000, 20.2, 63.6)
            ('Lampu', 140000, 20.2, 83.8)
            ('Buku', 72000, 10.4, 94.2)
            ('Pensil', 40000, 5.8, 100.0)
            """,
            """
            Tas menyumbang 43,4 persen, dan tiga produk teratas sudah mencapai 83,8 persen dari total pendapatan.
            """,
            filename="kontribusi_pareto.py",
        ),
        T("""
        ## Tabel pivot dengan agregasi bersyarat

        SQL tidak punya perintah pivot bawaan, tetapi hasilnya dapat ditiru dengan agregasi bersyarat: `SUM(CASE WHEN bulan = '01' THEN nilai ELSE 0 END)` untuk tiap kolom bulan. Setiap kolom pivot adalah satu ekspresi seperti itu, dan baris adalah kunci pengelompokan, misalnya kategori.

        Hasilnya tabel silang yang mudah dibaca manusia: kategori di baris, bulan di kolom. Kelemahannya, daftar kolom harus ditulis tetap, sehingga bulan baru berarti menambah ekspresi.
        """),
        C(
            SETUP + """
            q = '''
            SELECT k.kategori,
                   SUM(CASE WHEN strftime('%m', o.tanggal) = '01' THEN i.qty * k.harga ELSE 0 END),
                   SUM(CASE WHEN strftime('%m', o.tanggal) = '02' THEN i.qty * k.harga ELSE 0 END),
                   SUM(CASE WHEN strftime('%m', o.tanggal) = '03' THEN i.qty * k.harga ELSE 0 END)
            FROM pesanan o
            JOIN item i ON i.pesanan_id = o.id
            JOIN produk k ON k.id = i.produk_id
            WHERE o.status = 'selesai'
            GROUP BY k.kategori ORDER BY k.kategori
            '''
            for r in c.execute(q).fetchall():
                print(r)
            """,
            """
            ('ATK', 49000, 46000, 17000)
            ('Fashion', 150000, 0, 150000)
            ('Rumah', 0, 75000, 205000)
            """,
            """
            Tabel silang kategori dan bulan: fashion tidak laku di Februari dan kategori rumah baru mulai di Februari.
            """,
            filename="pivot_kategori.py",
        ),
        T("""
        ## Rekonsiliasi akhir

        Sebelum laporan dibagikan, cocokkan angkanya. Jumlah pendapatan per bulan harus sama dengan total keseluruhan, jumlah baris pivot harus sama, dan kontribusi produk harus berjumlah seratus persen. Tiga pemeriksaan sederhana ini menangkap sebagian besar kesalahan JOIN dan filter.

        Dalam praktik, simpan pemeriksaan itu sebagai query uji yang dijalankan bersama laporan. Bila ada angka yang tidak cocok, laporan ditahan sampai penyebabnya jelas.
        """),
        T("""
        ## Menceritakan hasilnya

        Angka tanpa narasi jarang menggerakkan keputusan. Dari laporan ini kita bisa menyimpulkan: pendapatan sempat turun di Februari lalu melonjak di Maret, didorong kategori fashion dan rumah. Dua pelanggan membeli berulang, sedangkan Citra paling lama tidak kembali.

        Tutup setiap analisis dengan ringkasan satu paragraf yang menyebut temuan utama, batasannya, dan langkah berikutnya. Itulah bagian yang paling dibaca oleh orang yang tidak membaca query.
        """),
        T("""
        ## Melangkah ke tahap berikutnya

        Anda kini menguasai SQL untuk analisis: dari SELECT dasar sampai window function dan perancangan skema. Langkah selanjutnya adalah memadukannya dengan Python dan pandas untuk visualisasi, pemodelan, dan otomatisasi, di mana SQL menyiapkan data dan Python mengolahnya lebih jauh.

        Biasakan menulis query yang rapi, diuji, dan direkonsiliasi. Keterampilan itu akan terpakai di hampir setiap pekerjaan data.
        """),
        K(
            "tip",
            """
            Cocokkan jumlah per bulan, baris pivot, dan kontribusi dengan total keseluruhan sebelum membagikan laporan.
            """,
            title="Rekonsiliasi laporan",
        ),
        T("""
        ## Struktur laporan yang baik

        Mulailah laporan dengan ringkasan: angka utama dan temuan paling penting dalam beberapa kalimat. Lanjutkan dengan rincian per bagian, dan akhiri dengan catatan metodologi yang menyebut definisi metrik dan filter yang dipakai. Pembaca yang sibuk dapat berhenti setelah ringkasan tanpa kehilangan inti.

        Susunan ini meniru cara orang membaca laporan: pertama ingin tahu kesimpulannya, baru bila perlu memeriksa dasarnya. Query yang rapi mendukung rincian itu.
        """),
        T("""
        ## Dari query ke dashboard

        Query yang sudah teruji dapat menjadi dasar dashboard yang diperbarui otomatis. Simpan sebagai view atau skrip terjadwal, beri nama jelas, dan dokumentasikan definisinya. Dengan begitu pemangku kepentingan mendapat angka yang konsisten tanpa meminta analis menjalankan ulang setiap kali.

        Konsistensi inilah nilai terbesar dari pekerjaan analitik yang rapi: semua orang bicara dengan angka yang sama.
        """),
        T("""
        ## Batas dan asumsi

        Setiap laporan memiliki asumsi: periode data yang dicakup, definisi pendapatan, dan perlakuan pesanan batal. Catat semuanya di bagian akhir laporan. Pembaca yang mengetahui asumsi dapat menilai sendiri seberapa jauh angka itu boleh dipercaya.
        """),
        E(
            "A6-09-3-ex1",
            "mudah",
            """
            Tulis fungsi `pertumbuhan_bulanan(c)` yang mengembalikan list tuple `(bulan, total, persen)` untuk pesanan `selesai`, terurut kronologis, dengan `persen` pertumbuhan terhadap bulan sebelumnya dibulatkan 1 desimal dan `None` untuk bulan pertama.
            """,
            """
            import sqlite3

            def pertumbuhan_bulanan(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert pertumbuhan_bulanan(c) == [('2026-01', 199000, None), ('2026-02', 121000, -39.2), ('2026-03', 372000, 207.4)]
            c.execute("INSERT INTO pesanan VALUES (10, 1, '2026-04-02', 'selesai')")
            c.execute('INSERT INTO item VALUES (10, 3, 2)')
            assert pertumbuhan_bulanan(c)[-1] == ('2026-04', 300000, -19.4)
            c.execute('DELETE FROM item WHERE pesanan_id = 10')
            assert len(pertumbuhan_bulanan(c)) == 3
            """,
            "CTE total bulanan lalu LAG pada query utama.",
            """
            import sqlite3

            def pertumbuhan_bulanan(c):
                q = '''
                WITH b AS (
                    SELECT strftime('%Y-%m', o.tanggal) AS bulan, SUM(i.qty * k.harga) AS total
                    FROM pesanan o
                    JOIN item i ON i.pesanan_id = o.id
                    JOIN produk k ON k.id = i.produk_id
                    WHERE o.status = 'selesai'
                    GROUP BY bulan
                )
                SELECT bulan, total,
                       ROUND(100.0 * (total - LAG(total) OVER (ORDER BY bulan)) / LAG(total) OVER (ORDER BY bulan), 1)
                FROM b ORDER BY bulan
                '''
                return c.execute(q).fetchall()
            """,
        ),
        E(
            "A6-09-3-ex2",
            "sedang",
            """
            Tulis fungsi `kumulatif_bulanan(c)` yang mengembalikan list total pendapatan kumulatif per bulan (pesanan `selesai`), terurut kronologis.
            """,
            """
            import sqlite3

            def kumulatif_bulanan(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert kumulatif_bulanan(c) == [199000, 320000, 692000]
            c.execute("INSERT INTO pesanan VALUES (10, 1, '2026-04-02', 'selesai')")
            c.execute('INSERT INTO item VALUES (10, 1, 4)')
            assert kumulatif_bulanan(c) == [199000, 320000, 692000, 702000]
            c.execute("INSERT INTO pesanan VALUES (11, 1, '2026-04-09', 'batal')")
            c.execute('INSERT INTO item VALUES (11, 3, 9)')
            assert kumulatif_bulanan(c)[-1] == 702000
            """,
            "SUM total bulanan dengan frame dari awal sampai baris saat ini.",
            """
            import sqlite3

            def kumulatif_bulanan(c):
                q = '''
                WITH b AS (
                    SELECT strftime('%Y-%m', o.tanggal) AS bulan, SUM(i.qty * k.harga) AS total
                    FROM pesanan o
                    JOIN item i ON i.pesanan_id = o.id
                    JOIN produk k ON k.id = i.produk_id
                    WHERE o.status = 'selesai'
                    GROUP BY bulan
                )
                SELECT SUM(total) OVER (ORDER BY bulan ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
                FROM b ORDER BY bulan
                '''
                return [r[0] for r in c.execute(q).fetchall()]
            """,
        ),
        E(
            "A6-09-3-ex3",
            "sedang",
            """
            Tulis fungsi `kontribusi_produk(c)` yang mengembalikan list tuple `(nama, persen)` kontribusi tiap produk terhadap total pendapatan `selesai`, dibulatkan 1 desimal, terurut dari terbesar lalu nama.
            """,
            """
            import sqlite3

            def kontribusi_produk(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert kontribusi_produk(c) == [('Tas', 43.4), ('Botol', 20.2), ('Lampu', 20.2), ('Buku', 10.4), ('Pensil', 5.8)]
            assert abs(sum(p for _, p in kontribusi_produk(c)) - 100) < 0.5
            c.execute('INSERT INTO item VALUES (9, 3, 8)')
            assert kontribusi_produk(c)[0][0] == 'Tas'
            """,
            "Agregasi per produk di CTE lalu bagi dengan SUM OVER ().",
            """
            import sqlite3

            def kontribusi_produk(c):
                q = '''
                WITH t AS (
                    SELECT k.nama AS nama, SUM(i.qty * k.harga) AS v
                    FROM pesanan o
                    JOIN item i ON i.pesanan_id = o.id
                    JOIN produk k ON k.id = i.produk_id
                    WHERE o.status = 'selesai'
                    GROUP BY k.id, k.nama
                )
                SELECT nama, ROUND(100.0 * v / SUM(v) OVER (), 1)
                FROM t ORDER BY v DESC, nama
                '''
                return c.execute(q).fetchall()
            """,
        ),
        E(
            "A6-09-3-ex4",
            "menantang",
            """
            Tulis fungsi `pivot_kategori(c)` yang mengembalikan list tuple `(kategori, jan, feb, mar)` berisi pendapatan `selesai` per kategori untuk bulan 01, 02, dan 03, terurut menurut kategori, dengan 0 bila tidak ada penjualan.
            """,
            """
            import sqlite3

            def pivot_kategori(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert pivot_kategori(c) == [('ATK', 49000, 46000, 17000), ('Fashion', 150000, 0, 150000), ('Rumah', 0, 75000, 205000)]
            c.execute("INSERT INTO pesanan VALUES (10, 1, '2026-02-25', 'selesai')")
            c.execute('INSERT INTO item VALUES (10, 3, 1)')
            assert pivot_kategori(c)[1] == ('Fashion', 150000, 150000, 150000)
            c.execute("INSERT INTO pesanan VALUES (11, 1, '2026-01-25', 'batal')")
            c.execute('INSERT INTO item VALUES (11, 4, 7)')
            assert pivot_kategori(c)[2] == ('Rumah', 0, 75000, 205000)
            """,
            "SUM(CASE WHEN bulan = ... THEN nilai ELSE 0 END) untuk tiap kolom.",
            """
            import sqlite3

            def pivot_kategori(c):
                q = '''
                SELECT k.kategori,
                       SUM(CASE WHEN strftime('%m', o.tanggal) = '01' THEN i.qty * k.harga ELSE 0 END),
                       SUM(CASE WHEN strftime('%m', o.tanggal) = '02' THEN i.qty * k.harga ELSE 0 END),
                       SUM(CASE WHEN strftime('%m', o.tanggal) = '03' THEN i.qty * k.harga ELSE 0 END)
                FROM pesanan o
                JOIN item i ON i.pesanan_id = o.id
                JOIN produk k ON k.id = i.produk_id
                WHERE o.status = 'selesai'
                GROUP BY k.kategori ORDER BY k.kategori
                '''
                return c.execute(q).fetchall()
            """,
        ),
    ],
    [
        M("Menyajikan laporan tanpa rekonsiliasi.", "Cocokkan jumlah bagian dengan total keseluruhan."),
        M("Mencampur pesanan batal dalam tren.", "Saring status di CTE pertama."),
        M("Menyajikan angka tanpa narasi.", "Tutup dengan ringkasan temuan dan langkah berikutnya."),
    ],
    [
        Q("Pertumbuhan bulanan memakai?", ["LAG", "NTILE", "DISTINCT", "LIMIT"], 0, "Bandingkan bulan sebelumnya.", hint="Lag."),
        Q("Kontribusi produk dihitung dengan?", ["Nilai dibagi SUM OVER ()", "COUNT", "MAX", "ROW_NUMBER"], 0, "Persen dari total.", hint="Bagi total."),
        Q("Pivot di SQL ditiru dengan?", ["Agregasi bersyarat", "UNION", "LIMIT", "INDEX"], 0, "SUM CASE WHEN.", hint="Case."),
        Q("Prinsip Pareto menyatakan?", ["Sedikit produk menyumbang sebagian besar hasil", "Semua sama", "Harga tetap", "Data acak"], 0, "Konsentrasi.", hint="Sedikit."),
        Q("Tujuan rekonsiliasi?", ["Menangkap kesalahan angka", "Mempercepat", "Menghapus data", "Membuat tabel"], 0, "Pemeriksaan silang.", hint="Cocok."),
    ],
    [
        "Pertumbuhan dan kumulatif dihitung dengan window function di atas CTE.",
        "Kontribusi dan Pareto menunjukkan konsentrasi pendapatan.",
        "Pivot dibuat dengan agregasi bersyarat.",
        "Rekonsiliasi dan narasi menyempurnakan laporan.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perintah yang cukup jelas dalam teks.", "brief": []}

write_module(
    "A6",
    9,
    "Query analitik end-to-end",
    105,
    [
        "Menjawab pertanyaan bisnis nyata dengan query yang benar dan terverifikasi",
        "Menganalisis pelanggan dengan peringkat, pembelian ulang, recency, dan kohort",
        "Menyusun laporan tren, kontribusi, dan pivot",
    ],
    [l1, l2, l3],
    video,
    REF,
)
