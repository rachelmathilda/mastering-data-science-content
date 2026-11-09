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
    "A6-04-1",
    "INNER JOIN dan kunci asing",
    35,
    [
        "Menjelaskan mengapa data dipecah ke beberapa tabel dan dihubungkan dengan kunci asing",
        "Menggabungkan dua dan tiga tabel dengan INNER JOIN",
        "Memakai alias tabel dan menghindari kolom ambigu",
        "Menjelaskan baris yatim yang hilang pada INNER JOIN",
    ],
    [
        T("""
        ## Mengapa banyak tabel

        Basis data relasional memecah data ke beberapa tabel agar tidak ada pengulangan. Bayangkan tabel pesanan yang menyimpan nama pelanggan, kota, dan alamatnya di setiap baris: data pelanggan yang sama tertulis berulang, dan mengubah kota satu pelanggan berarti mengubah banyak baris. Proses memecah ini disebut **normalisasi**.

        Solusinya, tiap entitas mendapat tabel sendiri. Pesanan hanya menyimpan nomor pelanggan, sedangkan data lengkap pelanggan ada di tabel pelanggan. Untuk melihat data utuh, kita menggabungkan tabel dengan **JOIN**.
        """),
        T("""
        ## Kunci asing

        Kolom `pelanggan_id` di tabel pesanan disebut **kunci asing**: nilainya merujuk kunci primer tabel pelanggan. Kunci asing membangun hubungan antar tabel: satu pelanggan dapat memiliki banyak pesanan, tetapi satu pesanan hanya milik satu pelanggan. Hubungan satu-ke-banyak ini yang paling umum.

        Di modul ini kita memakai tiga tabel: pelanggan, produk, dan pesanan. Pesanan memiliki dua kunci asing, ke pelanggan dan ke produk. Satu pesanan sengaja merujuk pelanggan nomor 99 yang tidak ada, untuk mempelajari perilaku JOIN pada data yang tidak konsisten.
        """),
        T("""
        ## INNER JOIN

        `INNER JOIN` menggabungkan baris dua tabel yang memenuhi kondisi `ON`. Untuk tiap pasangan baris yang kondisinya benar, ia menghasilkan satu baris gabungan. Baris yang tidak memiliki pasangan di tabel lain dibuang dari hasil. Kata `INNER` boleh dihilangkan, sehingga `JOIN` saja berarti `INNER JOIN`.

        Kondisi `ON p.pelanggan_id = g.id` mencocokkan kunci asing dengan kunci primernya. Pada data kita, tujuh dari delapan pesanan menemukan pelanggan, sedangkan pesanan dengan pelanggan 99 tidak punya pasangan dan hilang.
        """),
        C(
            SETUP + """
            print(c.execute('SELECT COUNT(*) FROM pesanan').fetchone())
            q = 'SELECT COUNT(*) FROM pesanan p JOIN pelanggan g ON p.pelanggan_id = g.id'
            print(c.execute(q).fetchone())
            """,
            """
            (8,)
            (7,)
            """,
            """
            Delapan pesanan ada, tetapi hanya tujuh yang cocok dengan pelanggan sehingga INNER JOIN membuang satu.
            """,
            filename="inner_join.py",
        ),
        T("""
        ## Alias tabel

        Query JOIN panjang menjadi mudah dibaca dengan alias tabel: `FROM pesanan p JOIN pelanggan g`. Alias pendek memungkinkan awalan `p.id` dan `g.id` untuk membedakan dua kolom `id`. Tanpa awalan, kolom yang namanya ada di dua tabel menyebabkan galat kolom ambigu.

        Biasakan memberi awalan alias pada setiap kolom di query JOIN, bahkan yang tidak ambigu. Query tetap benar bila nanti seseorang menambahkan kolom bernama sama ke salah satu tabel, dan pembaca langsung tahu asal tiap kolom.
        """),
        C(
            SETUP + """
            q = '''
            SELECT p.id, g.nama, p.jumlah
            FROM pesanan p JOIN pelanggan g ON p.pelanggan_id = g.id
            ORDER BY p.id
            '''
            print(c.execute(q).fetchall())
            """,
            """
            [(1, 'Ani', 2), (2, 'Ani', 10), (3, 'Budi', 1), (4, 'Citra', 1), (5, 'Citra', 2), (6, 'Dewi', 20), (7, 'Budi', 3)]
            """,
            """
            Setiap pesanan kini menampilkan nama pelanggannya, dan pesanan delapan tidak muncul.
            """,
            filename="alias_tabel.py",
        ),
        T("""
        ## Menggabungkan tiga tabel

        JOIN dapat dirantai: hasil gabungan pertama menjadi sumber gabungan kedua. Untuk menampilkan nama pelanggan dan nama produk bersama jumlah pesanan, kita menggabungkan pesanan ke pelanggan, lalu ke produk. Setiap `JOIN` punya klausa `ON` sendiri.

        Baca query seperti aliran: mulai dari tabel pusat, yaitu pesanan, lalu tambahkan tabel pelengkap satu per satu. Tabel yang menyimpan kunci asing biasanya menjadi pusat, dan tabel yang dirujuk menjadi pelengkap.
        """),
        C(
            SETUP + """
            q = '''
            SELECT p.id, g.nama, k.nama, p.jumlah
            FROM pesanan p
            JOIN pelanggan g ON p.pelanggan_id = g.id
            JOIN produk k ON p.produk_id = k.id
            ORDER BY p.id
            '''
            for baris in c.execute(q):
                print(baris)
            """,
            """
            (1, 'Ani', 'Buku', 2)
            (2, 'Ani', 'Pensil', 10)
            (3, 'Budi', 'Tas', 1)
            (4, 'Citra', 'Buku', 1)
            (5, 'Citra', 'Botol', 2)
            (6, 'Dewi', 'Pensil', 20)
            (7, 'Budi', 'Buku', 3)
            """,
            """
            Tiga tabel digabung sehingga tiap pesanan menampilkan pelanggan dan produknya sekaligus.
            """,
            filename="tiga_tabel.py",
        ),
        T("""
        ## Menghitung dari kolom gabungan

        Setelah tabel digabung, kolom dari semua tabel dapat dipakai bersama dalam ekspresi. Nilai pesanan adalah jumlah dikali harga, di mana jumlah berasal dari pesanan dan harga dari produk. Perhitungan semacam ini mustahil tanpa JOIN karena kedua nilai hidup di tabel berbeda.

        Ini alasan JOIN begitu mendasar: analisis jarang cukup dengan satu tabel. Pertanyaan bisnis nyata, seperti total belanja per kota, menyentuh pelanggan, pesanan, dan produk sekaligus.
        """),
        C(
            SETUP + """
            q = '''
            SELECT p.id, p.jumlah * k.harga
            FROM pesanan p
            JOIN pelanggan g ON p.pelanggan_id = g.id
            JOIN produk k ON p.produk_id = k.id
            ORDER BY p.id
            '''
            print(c.execute(q).fetchall())
            """,
            """
            [(1, 24000.0), (2, 25000.0), (3, 150000.0), (4, 12000.0), (5, 70000.0), (6, 50000.0), (7, 36000.0)]
            """,
            """
            Nilai tiap pesanan dihitung dari jumlah pesanan dan harga produk yang berasal dari tabel berbeda.
            """,
            filename="nilai_gabungan.py",
        ),
        T("""
        ## Integritas referensial

        Pesanan nomor 8 merujuk pelanggan yang tidak ada. Basis data yang dirancang baik mencegahnya dengan **constraint kunci asing**, yang menolak penyisipan baris dengan referensi tak valid. SQLite mendukung constraint ini bila diaktifkan dengan `PRAGMA foreign_keys = ON`, tetapi tidak aktif secara default.

        Pada data nyata dari sumber yang tidak terkontrol, baris yatim seperti ini sering muncul. Selalu periksa apakah INNER JOIN menghilangkan baris yang tidak kamu duga, dengan membandingkan jumlah baris sebelum dan sesudah JOIN.
        """),
        K(
            "tip",
            """
            Hitung jumlah baris sebelum dan sesudah JOIN. Selisihnya menunjukkan baris yang tidak punya pasangan dan hilang diam-diam.
            """,
            title="Periksa JOIN",
        ),
        T("""
        ## Memilih kolom dari tabel gabungan

        Setelah JOIN, hindari `SELECT *` karena ia menarik semua kolom dari semua tabel, termasuk kolom bernama sama yang saling menimpa pada pustaka tertentu. Sebutkan kolom yang dibutuhkan dengan awalan alias, dan beri alias baru bila dua kolom bernama sama, misalnya `g.nama AS pelanggan` dan `k.nama AS produk`.

        Alias yang jelas membuat hasil query langsung siap dibaca ke pandas dengan nama kolom bermakna, tanpa perlu mengganti nama di kode Python.
        """),
        E(
            "A6-04-1-ex1",
            "mudah",
            """
            Tulis fungsi `nama_pembeli(c)` yang mengembalikan list tuple `(id_pesanan, nama_pelanggan)` untuk pesanan yang punya pelanggan, terurut menurut id pesanan, memakai INNER JOIN.
            """,
            """
            import sqlite3

            def nama_pembeli(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            h = nama_pembeli(c)
            assert h == [(1, 'Ani'), (2, 'Ani'), (3, 'Budi'), (4, 'Citra'), (5, 'Citra'), (6, 'Dewi'), (7, 'Budi')]
            assert all(i != 8 for i, _ in h)
            c.execute("INSERT INTO pelanggan VALUES (99, 'Zed', 'Bogor')")
            assert nama_pembeli(c)[-1] == (8, 'Zed')
            """,
            "Gabungkan pesanan dengan pelanggan lewat pelanggan_id dan id.",
            """
            import sqlite3

            def nama_pembeli(c):
                q = 'SELECT p.id, g.nama FROM pesanan p JOIN pelanggan g ON p.pelanggan_id = g.id ORDER BY p.id'
                return c.execute(q).fetchall()
            """,
        ),
        E(
            "A6-04-1-ex2",
            "sedang",
            """
            Tulis fungsi `detail_pesanan(c)` yang mengembalikan list tuple `(id_pesanan, nama_pelanggan, nama_produk, jumlah)` untuk pesanan yang punya pelanggan dan produk, terurut menurut id pesanan.
            """,
            """
            import sqlite3

            def detail_pesanan(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            h = detail_pesanan(c)
            assert len(h) == 7
            assert h[0] == (1, 'Ani', 'Buku', 2)
            assert h[-1] == (7, 'Budi', 'Buku', 3)
            assert h[4] == (5, 'Citra', 'Botol', 2)
            """,
            "Rantai dua JOIN dari pesanan ke pelanggan dan ke produk.",
            """
            import sqlite3

            def detail_pesanan(c):
                q = '''
                SELECT p.id, g.nama, k.nama, p.jumlah
                FROM pesanan p
                JOIN pelanggan g ON p.pelanggan_id = g.id
                JOIN produk k ON p.produk_id = k.id
                ORDER BY p.id
                '''
                return c.execute(q).fetchall()
            """,
        ),
        E(
            "A6-04-1-ex3",
            "sedang",
            """
            Tulis fungsi `pesanan_di_kota(c, kota)` yang mengembalikan list id pesanan milik pelanggan yang tinggal di kota itu, terurut menurut id pesanan.
            """,
            """
            import sqlite3

            def pesanan_di_kota(c, kota):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert pesanan_di_kota(c, 'Jakarta') == [1, 2, 4, 5]
            assert pesanan_di_kota(c, 'Bandung') == [3, 7]
            assert pesanan_di_kota(c, 'Medan') == []
            assert pesanan_di_kota(c, 'Surabaya') == [6]
            """,
            "Gabungkan pesanan dengan pelanggan dan saring kota dengan parameter.",
            """
            import sqlite3

            def pesanan_di_kota(c, kota):
                q = 'SELECT p.id FROM pesanan p JOIN pelanggan g ON p.pelanggan_id = g.id WHERE g.kota = ? ORDER BY p.id'
                return [r[0] for r in c.execute(q, (kota,)).fetchall()]
            """,
        ),
        E(
            "A6-04-1-ex4",
            "menantang",
            """
            Tulis fungsi `nilai_pesanan(c)` yang mengembalikan list tuple `(id_pesanan, nilai)` dengan `nilai = jumlah * harga` untuk pesanan yang punya pelanggan dan produk, terurut menurut id pesanan.
            """,
            """
            import sqlite3

            def nilai_pesanan(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert nilai_pesanan(c) == [(1, 24000.0), (2, 25000.0), (3, 150000.0), (4, 12000.0), (5, 70000.0), (6, 50000.0), (7, 36000.0)]
            c.execute('UPDATE produk SET harga = 1000 WHERE id = 1')
            assert nilai_pesanan(c)[1] == (2, 10000.0)
            c.execute("INSERT INTO pelanggan VALUES (99, 'Zed', 'Bogor')")
            assert nilai_pesanan(c)[-1] == (8, 1000.0)
            """,
            "Kalikan jumlah dari pesanan dengan harga dari produk setelah dua JOIN.",
            """
            import sqlite3

            def nilai_pesanan(c):
                q = '''
                SELECT p.id, p.jumlah * k.harga
                FROM pesanan p
                JOIN pelanggan g ON p.pelanggan_id = g.id
                JOIN produk k ON p.produk_id = k.id
                ORDER BY p.id
                '''
                return c.execute(q).fetchall()
            """,
        ),
    ],
    [
        M("Menulis kolom id tanpa awalan alias pada query JOIN.", "Selalu beri awalan alias tabel."),
        M("Tidak memeriksa baris yang hilang setelah INNER JOIN.", "Bandingkan jumlah baris sebelum dan sesudah."),
        M("Lupa kondisi ON sehingga menghasilkan semua kombinasi.", "Setiap JOIN butuh kondisi ON."),
    ],
    [
        Q("Kunci asing adalah?", ["Kolom yang merujuk kunci primer tabel lain", "Kolom teks", "Indeks", "Nama tabel"], 0, "Hubungan antar tabel.", hint="Rujukan."),
        Q("INNER JOIN mempertahankan?", ["Baris yang punya pasangan", "Semua baris kiri", "Semua baris kanan", "Semua kombinasi"], 0, "Hanya yang cocok.", hint="Cocok."),
        Q("Alias tabel berguna untuk?", ["Membedakan kolom bernama sama", "Mempercepat", "Menghapus data", "Mengurutkan"], 0, "Menghindari ambigu.", hint="Awalan."),
        Q("Normalisasi bertujuan?", ["Mengurangi pengulangan data", "Menambah duplikasi", "Menghapus kunci", "Mengurutkan"], 0, "Satu fakta satu tempat.", hint="Pengulangan."),
        Q("Pesanan dengan pelanggan 99 yang tak ada?", ["Hilang pada INNER JOIN", "Tampil dengan NULL", "Menyebabkan error", "Menjadi nol"], 0, "Tanpa pasangan.", hint="Yatim."),
    ],
    [
        "Normalisasi memecah data ke tabel terpisah yang dihubungkan kunci asing.",
        "INNER JOIN hanya mempertahankan baris yang punya pasangan.",
        "Alias tabel mencegah kolom ambigu dan memperjelas asal kolom.",
        "Periksa jumlah baris sebelum dan sesudah JOIN.",
    ],
    [],
)

l2 = lesson(
    "A6-04-2",
    "LEFT JOIN dan baris tanpa pasangan",
    35,
    [
        "Memakai LEFT JOIN untuk mempertahankan semua baris tabel kiri",
        "Menemukan baris tanpa pasangan dengan anti-join",
        "Menghitung dengan COUNT kolom pada LEFT JOIN",
        "Membedakan kondisi di ON dan di WHERE pada LEFT JOIN",
    ],
    [
        T("""
        ## Mempertahankan semua baris kiri

        INNER JOIN membuang baris tanpa pasangan, yang sering bukan yang kita inginkan. Bila kita ingin daftar semua pelanggan termasuk yang belum pernah memesan, kita memakai `LEFT JOIN`. Ia mempertahankan semua baris tabel kiri, dan bila tidak ada pasangan di tabel kanan, kolom dari kanan diisi `NULL`.

        Dengan begitu pelanggan Eko, yang belum punya pesanan, tetap muncul dengan kolom pesanan berisi `NULL`. LEFT JOIN adalah alat utama untuk menjawab pertanyaan tentang yang tidak ada atau yang hilang.
        """),
        C(
            SETUP + """
            q = '''
            SELECT p.id, g.nama
            FROM pesanan p LEFT JOIN pelanggan g ON p.pelanggan_id = g.id
            ORDER BY p.id
            '''
            print(c.execute(q).fetchall())
            """,
            """
            [(1, 'Ani'), (2, 'Ani'), (3, 'Budi'), (4, 'Citra'), (5, 'Citra'), (6, 'Dewi'), (7, 'Budi'), (8, None)]
            """,
            """
            Pesanan delapan kini tetap muncul, dengan nama pelanggan NULL karena pelanggannya tidak ada.
            """,
            filename="left_join.py",
        ),
        T("""
        ## Tabel kiri dan kanan

        Kiri dan kanan ditentukan oleh urutan penulisan: tabel setelah `FROM` adalah kiri dan tabel setelah `JOIN` adalah kanan. Menukar urutan mengubah hasil `LEFT JOIN`. `A LEFT JOIN B` mempertahankan semua baris A, sedangkan `B LEFT JOIN A` mempertahankan semua baris B.

        Pilih tabel kiri sebagai tabel yang barisnya ingin kamu pertahankan, yaitu entitas yang menjadi fokus pertanyaan. Untuk pertanyaan tentang pelanggan, taruh pelanggan di kiri. Untuk pertanyaan tentang pesanan, taruh pesanan di kiri.
        """),
        T("""
        ## Anti-join: yang tidak punya pasangan

        Pertanyaan umum: pelanggan mana yang belum pernah memesan? Jawabannya adalah **anti-join**: lakukan `LEFT JOIN`, lalu saring baris yang kolom kuncinya di tabel kanan `NULL` dengan `WHERE p.id IS NULL`. Baris yang tersisa adalah baris kiri tanpa pasangan.

        Pola ini juga menemukan masalah integritas data, misalnya pesanan yatim: `pesanan LEFT JOIN pelanggan ... WHERE g.id IS NULL`. Alternatif setara memakai `NOT EXISTS`, dibahas pada modul subquery.
        """),
        C(
            SETUP + """
            q = '''
            SELECT g.nama FROM pelanggan g
            LEFT JOIN pesanan p ON p.pelanggan_id = g.id
            WHERE p.id IS NULL
            '''
            print(c.execute(q).fetchall())
            q = '''
            SELECT p.id FROM pesanan p
            LEFT JOIN pelanggan g ON p.pelanggan_id = g.id
            WHERE g.id IS NULL
            '''
            print(c.execute(q).fetchall())
            """,
            """
            [('Eko',)]
            [(8,)]
            """,
            """
            Eko adalah pelanggan tanpa pesanan, dan pesanan delapan adalah pesanan tanpa pelanggan.
            """,
            filename="anti_join.py",
        ),
        T("""
        ## COUNT pada LEFT JOIN

        Menghitung pesanan per pelanggan dengan `LEFT JOIN` menyimpan jebakan klasik. `COUNT(*)` menghitung baris hasil, dan pelanggan Eko yang tidak punya pesanan tetap menghasilkan satu baris gabungan dengan kolom pesanan `NULL`, sehingga `COUNT(*)` menghitung satu, bukan nol.

        Pakai `COUNT(p.id)`, yang menghitung hanya nilai non-NULL dari tabel kanan, sehingga Eko benar bernilai nol. Aturan: pada LEFT JOIN, hitung kolom dari tabel kanan, jangan pernah `COUNT(*)`.
        """),
        C(
            SETUP + """
            q = '''
            SELECT g.nama, COUNT(p.id), COUNT(*)
            FROM pelanggan g LEFT JOIN pesanan p ON p.pelanggan_id = g.id
            GROUP BY g.id ORDER BY g.id
            '''
            print(c.execute(q).fetchall())
            """,
            """
            [('Ani', 2, 2), ('Budi', 2, 2), ('Citra', 2, 2), ('Dewi', 1, 1), ('Eko', 0, 1)]
            """,
            """
            Untuk Eko, COUNT kolom benar bernilai nol sedangkan COUNT bintang salah bernilai satu.
            """,
            filename="count_left.py",
        ),
        T("""
        ## ON atau WHERE

        Pada `INNER JOIN`, kondisi di `ON` dan di `WHERE` memberi hasil sama. Pada `LEFT JOIN` berbeda tajam. Kondisi di `ON` menentukan baris kanan mana yang dicocokkan, sedangkan baris kiri tetap dipertahankan. Kondisi di `WHERE` menyaring hasil akhir, sehingga baris kiri tanpa pasangan, yang kolom kanannya `NULL`, ikut terbuang.

        Untuk menghitung pesanan besar per pelanggan sambil mempertahankan semua pelanggan, taruh kondisi jumlah di `ON`. Menaruhnya di `WHERE` secara diam-diam mengubah LEFT JOIN menjadi INNER JOIN.
        """),
        C(
            SETUP + """
            q = '''
            SELECT g.nama, COUNT(p.id)
            FROM pelanggan g
            LEFT JOIN pesanan p ON p.pelanggan_id = g.id AND p.jumlah >= 10
            GROUP BY g.id ORDER BY g.id
            '''
            print(c.execute(q).fetchall())
            q = '''
            SELECT g.nama, COUNT(p.id)
            FROM pelanggan g
            LEFT JOIN pesanan p ON p.pelanggan_id = g.id
            WHERE p.jumlah >= 10
            GROUP BY g.id ORDER BY g.id
            '''
            print(c.execute(q).fetchall())
            """,
            """
            [('Ani', 1), ('Budi', 0), ('Citra', 0), ('Dewi', 1), ('Eko', 0)]
            [('Ani', 1), ('Dewi', 1)]
            """,
            """
            Kondisi di ON mempertahankan semua pelanggan dengan hitungan nol, sedangkan di WHERE membuang pelanggan tanpa pesanan besar.
            """,
            filename="on_vs_where.py",
        ),
        T("""
        ## RIGHT dan FULL JOIN

        `RIGHT JOIN` adalah cermin `LEFT JOIN` yang mempertahankan semua baris kanan, dan `FULL OUTER JOIN` mempertahankan semua baris kedua sisi. SQLite mendukung keduanya sejak versi 3.39, tetapi di praktik hampir semua kebutuhan dipenuhi `LEFT JOIN` dengan urutan tabel yang tepat.

        Menulis hanya `LEFT JOIN` membuat query seragam dan mudah dibaca dari kiri ke kanan. Bila butuh semua baris kedua sisi, `FULL JOIN` menjawabnya, misalnya saat mencocokkan dua daftar untuk mencari yang hanya ada di salah satunya.
        """),
        K(
            "warn",
            """
            Pada LEFT JOIN jangan taruh kondisi tabel kanan di WHERE kecuali ingin membuang baris tanpa pasangan. Taruh di ON.
            """,
            title="ON bukan WHERE",
        ),
        T("""
        ## Memeriksa kualitas lewat JOIN

        LEFT JOIN dengan filter NULL adalah alat audit data yang sangat berguna. Dengan satu query kamu dapat menemukan referensi yang rusak, entitas tanpa aktivitas, dan catatan yang tidak cocok antar sistem. Laporan kualitas data sering terdiri dari beberapa anti-join seperti ini.

        Jalankan pemeriksaan serupa setiap kali memuat data baru ke basis data. Menemukan pesanan yatim saat impor jauh lebih murah daripada menemukannya setelah laporan keuangan salah dan dibaca pimpinan.
        """),
        T("""
        ## Beberapa LEFT JOIN berantai

        Bila beberapa LEFT JOIN dirantai, perhatikan bahwa baris `NULL` dari join pertama akan membuat kondisi join berikutnya yang bergantung padanya juga tidak cocok. Hasilnya kolom berikutnya ikut `NULL`, yang biasanya benar secara logika tetapi bisa membingungkan saat membaca hasilnya.

        Bangun query bertahap: periksa hasil setelah tiap JOIN sebelum menambah yang berikutnya. Jumlah baris yang tidak berubah setelah LEFT JOIN menandakan hubungan satu-ke-satu, dan lonjakan jumlah baris menandakan hubungan satu-ke-banyak.
        """),
        E(
            "A6-04-2-ex1",
            "mudah",
            """
            Tulis fungsi `pesanan_dengan_nama(c)` yang mengembalikan list tuple `(id_pesanan, nama_pelanggan)` untuk SEMUA pesanan, dengan nama `None` bila pelanggan tidak ada, terurut menurut id pesanan.
            """,
            """
            import sqlite3

            def pesanan_dengan_nama(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            h = pesanan_dengan_nama(c)
            assert len(h) == 8
            assert h[0] == (1, 'Ani')
            assert h[-1] == (8, None)
            c.execute("INSERT INTO pelanggan VALUES (99, 'Zed', 'Bogor')")
            assert pesanan_dengan_nama(c)[-1] == (8, 'Zed')
            """,
            "Mulai dari pesanan lalu LEFT JOIN ke pelanggan.",
            """
            import sqlite3

            def pesanan_dengan_nama(c):
                q = 'SELECT p.id, g.nama FROM pesanan p LEFT JOIN pelanggan g ON p.pelanggan_id = g.id ORDER BY p.id'
                return c.execute(q).fetchall()
            """,
        ),
        E(
            "A6-04-2-ex2",
            "sedang",
            """
            Tulis fungsi `pelanggan_tanpa_pesanan(c)` yang mengembalikan list nama pelanggan yang belum memiliki pesanan, terurut menurut id pelanggan, memakai anti-join.
            """,
            """
            import sqlite3

            def pelanggan_tanpa_pesanan(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert pelanggan_tanpa_pesanan(c) == ['Eko']
            c.execute('INSERT INTO pesanan VALUES (9, 5, 1, 1)')
            assert pelanggan_tanpa_pesanan(c) == []
            c.execute("INSERT INTO pelanggan VALUES (6, 'Fani', 'Bogor')")
            assert pelanggan_tanpa_pesanan(c) == ['Fani']
            """,
            "LEFT JOIN dari pelanggan lalu saring id pesanan yang NULL.",
            """
            import sqlite3

            def pelanggan_tanpa_pesanan(c):
                q = '''
                SELECT g.nama FROM pelanggan g
                LEFT JOIN pesanan p ON p.pelanggan_id = g.id
                WHERE p.id IS NULL ORDER BY g.id
                '''
                return [r[0] for r in c.execute(q).fetchall()]
            """,
        ),
        E(
            "A6-04-2-ex3",
            "sedang",
            """
            Tulis fungsi `pesanan_yatim(c)` yang mengembalikan list id pesanan yang merujuk pelanggan yang tidak ada, terurut menurut id.
            """,
            """
            import sqlite3

            def pesanan_yatim(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert pesanan_yatim(c) == [8]
            c.execute('INSERT INTO pesanan VALUES (9, 77, 2, 1)')
            assert pesanan_yatim(c) == [8, 9]
            c.execute('DELETE FROM pesanan WHERE id IN (8, 9)')
            assert pesanan_yatim(c) == []
            """,
            "LEFT JOIN dari pesanan ke pelanggan lalu saring id pelanggan yang NULL.",
            """
            import sqlite3

            def pesanan_yatim(c):
                q = '''
                SELECT p.id FROM pesanan p
                LEFT JOIN pelanggan g ON p.pelanggan_id = g.id
                WHERE g.id IS NULL ORDER BY p.id
                '''
                return [r[0] for r in c.execute(q).fetchall()]
            """,
        ),
        E(
            "A6-04-2-ex4",
            "menantang",
            """
            Tulis fungsi `pesanan_per_pelanggan(c)` yang mengembalikan dictionary `{nama: banyak pesanan}` untuk SEMUA pelanggan termasuk yang tanpa pesanan (bernilai 0), memakai `LEFT JOIN` dan `COUNT` kolom kanan.
            """,
            """
            import sqlite3

            def pesanan_per_pelanggan(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert pesanan_per_pelanggan(c) == {'Ani': 2, 'Budi': 2, 'Citra': 2, 'Dewi': 1, 'Eko': 0}
            c.execute('INSERT INTO pesanan VALUES (9, 5, 1, 1)')
            assert pesanan_per_pelanggan(c)['Eko'] == 1
            c.execute("INSERT INTO pelanggan VALUES (6, 'Fani', 'Bogor')")
            assert pesanan_per_pelanggan(c)['Fani'] == 0
            """,
            "Pakai COUNT dari kolom id tabel pesanan, bukan COUNT bintang.",
            """
            import sqlite3

            def pesanan_per_pelanggan(c):
                q = '''
                SELECT g.nama, COUNT(p.id)
                FROM pelanggan g LEFT JOIN pesanan p ON p.pelanggan_id = g.id
                GROUP BY g.id
                '''
                return dict(c.execute(q).fetchall())
            """,
        ),
    ],
    [
        M("Memakai COUNT bintang pada LEFT JOIN.", "Hitung kolom dari tabel kanan."),
        M("Menaruh kondisi tabel kanan di WHERE pada LEFT JOIN.", "Taruh di ON."),
        M("Menukar urutan tabel tanpa menyadari efeknya.", "Tabel kiri adalah yang barisnya dipertahankan."),
    ],
    [
        Q("LEFT JOIN mempertahankan?", ["Semua baris tabel kiri", "Semua baris kanan", "Hanya yang cocok", "Tidak ada"], 0, "Kiri.", hint="Kiri."),
        Q("Anti-join memakai?", ["LEFT JOIN dan IS NULL", "INNER JOIN", "DISTINCT", "LIMIT"], 0, "Menemukan tanpa pasangan.", hint="NULL."),
        Q("COUNT pada LEFT JOIN sebaiknya?", ["Kolom tabel kanan", "Bintang", "Semua", "Tidak perlu"], 0, "Agar nol benar.", hint="Kanan."),
        Q("Kondisi tabel kanan yang menjaga baris kiri diletakkan di?", ["ON", "WHERE", "HAVING", "ORDER BY"], 0, "ON.", hint="Pencocokan."),
        Q("Kolom kanan tanpa pasangan bernilai?", ["NULL", "0", "Kosong", "Error"], 0, "NULL.", hint="NULL."),
    ],
    [
        "LEFT JOIN mempertahankan semua baris kiri dan mengisi NULL untuk yang tanpa pasangan.",
        "Anti-join dengan IS NULL menemukan baris tanpa pasangan.",
        "COUNT kolom kanan memberi nol yang benar untuk yang tanpa pasangan.",
        "Kondisi kanan di ON menjaga baris kiri, di WHERE membuangnya.",
    ],
    [],
)

l3 = lesson(
    "A6-04-3",
    "JOIN dengan agregasi, self join, dan duplikasi baris",
    35,
    [
        "Meringkas data gabungan per kelompok dari tabel lain",
        "Mengenali dan menghindari duplikasi baris akibat JOIN satu-ke-banyak",
        "Memakai self join untuk membandingkan baris satu tabel",
        "Menjelaskan CROSS JOIN dan EXISTS",
    ],
    [
        T("""
        ## Agregasi setelah JOIN

        Kekuatan sebenarnya muncul saat JOIN digabung dengan `GROUP BY`. Kota ada di tabel pelanggan sedangkan nilai belanja berasal dari pesanan dan produk. Dengan menggabungkan ketiganya kita bisa menghitung total belanja per kota, sesuatu yang tidak mungkin dijawab satu tabel saja.

        Alurnya: gabungkan tabel yang dibutuhkan, saring baris, kelompokkan menurut kolom dari tabel mana pun, lalu agregasikan. Karena kolom semua tabel tersedia setelah JOIN, kita bebas mengelompokkan dan menghitung dengan kolom dari tabel berbeda.
        """),
        C(
            SETUP + """
            q = '''
            SELECT g.kota, SUM(p.jumlah * k.harga)
            FROM pesanan p
            JOIN pelanggan g ON p.pelanggan_id = g.id
            JOIN produk k ON p.produk_id = k.id
            GROUP BY g.kota ORDER BY g.kota
            '''
            print(c.execute(q).fetchall())
            """,
            """
            [('Bandung', 186000.0), ('Jakarta', 131000.0), ('Surabaya', 50000.0)]
            """,
            """
            Total belanja dijumlahkan per kota dari tiga tabel, dan Medan tidak muncul karena tidak ada pesanan.
            """,
            filename="join_agregasi.py",
        ),
        T("""
        ## Duplikasi akibat satu-ke-banyak

        Hubungan satu-ke-banyak membuat baris sisi satu berlipat ganda setelah JOIN: pelanggan Ani yang memiliki dua pesanan muncul dua kali. Bila kita menghitung pelanggan per kota dengan `COUNT(*)` pada hasil gabungan, kita sebenarnya menghitung pesanan, bukan pelanggan.

        Ini kesalahan analisis paling umum pada JOIN. Gunakan `COUNT(DISTINCT g.id)` bila ingin menghitung entitas sisi satu. Selalu tanyakan: satu baris hasil gabungan mewakili apa? Jawabannya menentukan apa yang sebenarnya dihitung agregat.
        """),
        C(
            SETUP + """
            q = '''
            SELECT g.kota, COUNT(DISTINCT g.id), COUNT(*)
            FROM pelanggan g JOIN pesanan p ON p.pelanggan_id = g.id
            GROUP BY g.kota ORDER BY g.kota
            '''
            print(c.execute(q).fetchall())
            """,
            """
            [('Bandung', 1, 2), ('Jakarta', 2, 4), ('Surabaya', 1, 1)]
            """,
            """
            Jakarta memiliki dua pelanggan tetapi empat baris gabungan, sehingga COUNT bintang menghitung pesanan, bukan pelanggan.
            """,
            filename="duplikasi_join.py",
        ),
        T("""
        ## Fan-out pada SUM

        Duplikasi lebih berbahaya pada `SUM`. Bila kamu menggabungkan tabel pelanggan yang memiliki kolom saldo dengan tabel pesanan lalu menjumlahkan saldo, saldo tiap pelanggan terhitung sebanyak pesanannya. Hasilnya angka membengkak yang tampak sah tetapi salah.

        Pencegahannya adalah meringkas sisi banyak lebih dulu dalam subquery sehingga satu baris per pelanggan, baru digabung. Selalu periksa total hasil JOIN terhadap total sumber asli sebagai uji kewarasan.
        """),
        T("""
        ## Self join

        Sebuah tabel dapat digabung dengan dirinya sendiri dengan memberi dua alias berbeda. Ini berguna untuk membandingkan baris dalam tabel yang sama, misalnya mencari pasangan pelanggan sekota. Kondisi `a.kota = b.kota AND a.id < b.id` mencocokkan pasangan sekota dan mencegah pasangan terbalik serta pasangan dengan diri sendiri.

        Self join juga dipakai untuk data hierarkis, misalnya karyawan dan atasannya yang tersimpan di tabel sama dengan kolom `atasan_id` yang merujuk id karyawan lain.
        """),
        C(
            SETUP + """
            q = '''
            SELECT a.nama, b.nama
            FROM pelanggan a JOIN pelanggan b ON a.kota = b.kota AND a.id < b.id
            ORDER BY a.id, b.id
            '''
            print(c.execute(q).fetchall())
            """,
            """
            [('Ani', 'Citra')]
            """,
            """
            Hanya Ani dan Citra yang sekota, dan syarat id lebih kecil mencegah pasangan ganda.
            """,
            filename="self_join.py",
        ),
        T("""
        ## CROSS JOIN

        `CROSS JOIN` menghasilkan semua kombinasi baris kedua tabel tanpa kondisi, disebut produk Kartesius. Lima pelanggan dan empat produk menghasilkan dua puluh kombinasi. Berguna untuk membangun semua kombinasi yang mungkin, misalnya semua pasangan pelanggan dan produk untuk mencari yang belum dibeli.

        Namun berbahaya bila tidak sengaja. Lupa menulis kondisi `ON` pada JOIN biasa di beberapa basis data menghasilkan produk Kartesius, dan pada tabel jutaan baris itu berarti triliunan baris yang menghabiskan memori. Waspadai lonjakan jumlah baris yang tidak masuk akal.
        """),
        C(
            SETUP + """
            print(c.execute('SELECT COUNT(*) FROM pelanggan CROSS JOIN produk').fetchone())
            q = '''
            SELECT g.nama FROM pelanggan g
            WHERE EXISTS (SELECT 1 FROM pesanan p WHERE p.pelanggan_id = g.id)
            ORDER BY g.id
            '''
            print(c.execute(q).fetchall())
            """,
            """
            (20,)
            [('Ani',), ('Budi',), ('Citra',), ('Dewi',)]
            """,
            """
            CROSS JOIN menghasilkan dua puluh kombinasi, dan EXISTS memilih pelanggan yang punya pesanan tanpa menduplikasi baris.
            """,
            filename="cross_exists.py",
        ),
        T("""
        ## EXISTS sebagai alternatif

        `EXISTS` menguji apakah subquery menghasilkan minimal satu baris. Ia ideal untuk pertanyaan ada atau tidaknya, seperti pelanggan yang punya pesanan, tanpa masalah duplikasi karena hasilnya satu baris per pelanggan, tidak peduli berapa pesanannya.

        Bandingkan dengan JOIN yang menggandakan baris dan memerlukan `DISTINCT`. Untuk pertanyaan keberadaan, `EXISTS` lebih jelas niatnya dan sering lebih cepat. Pelajari ini lebih jauh pada modul subquery.
        """),
        K(
            "warn",
            """
            Tanyakan satu baris hasil JOIN mewakili apa. JOIN satu-ke-banyak menggandakan sisi satu dan membuat COUNT serta SUM membengkak.
            """,
            title="Waspada fan-out",
        ),
        T("""
        ## Membangun query JOIN bertahap

        Query JOIN panjang paling mudah dibangun dan dipecahkan bertahap. Mulai dari tabel pusat dengan beberapa kolom, jalankan, dan periksa jumlah baris. Tambahkan satu JOIN, jalankan, dan periksa lagi bahwa jumlahnya sesuai harapan. Baru setelah itu tambahkan pengelompokan dan agregasi.

        Pendekatan ini membuat setiap kesalahan terlihat tepat saat ia muncul, bukan terkubur di bawah lapisan agregasi. Banyak bug JOIN hanya kentara bila kamu melihat baris mentah sebelum diringkas.
        """),
        T("""
        ## Memilih antara JOIN dan subquery

        Banyak pertanyaan dapat dijawab dengan JOIN maupun subquery. JOIN unggul bila kamu butuh kolom dari kedua tabel dalam hasil. Subquery atau EXISTS unggul bila kamu hanya butuh menyaring berdasarkan keberadaan data di tabel lain, karena tidak menggandakan baris dan niatnya lebih jelas.

        Pilih yang membuat maksud query paling mudah dipahami. Mesin basis data modern sering menghasilkan rencana eksekusi yang sama untuk keduanya, sehingga keterbacaan biasanya menjadi pertimbangan utama.
        """),
        T("""
        ## Kinerja JOIN dan indeks

        JOIN pada tabel besar bergantung pada indeks di kolom kunci. Kunci primer otomatis berindeks, tetapi kunci asing seperti `pelanggan_id` sering tidak, sehingga JOIN memindai seluruh tabel untuk tiap baris. Menambah indeks pada kunci asing yang sering dipakai di JOIN dapat mempercepat query berkali lipat.

        Modul desain tabel dan indeks akan membahas cara membuat dan memeriksa indeks, termasuk `EXPLAIN QUERY PLAN` untuk melihat apakah indeks benar-benar dipakai oleh query.
        """),
        E(
            "A6-04-3-ex1",
            "mudah",
            """
            Tulis fungsi `belanja_per_kota(c)` yang mengembalikan dictionary `{kota: total jumlah * harga}` dari pesanan yang punya pelanggan dan produk.
            """,
            """
            import sqlite3

            def belanja_per_kota(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert belanja_per_kota(c) == {'Bandung': 186000.0, 'Jakarta': 131000.0, 'Surabaya': 50000.0}
            assert 'Medan' not in belanja_per_kota(c)
            c.execute('INSERT INTO pesanan VALUES (9, 5, 3, 1)')
            assert belanja_per_kota(c)['Medan'] == 150000.0
            """,
            "Gabungkan tiga tabel lalu kelompokkan menurut kota dan jumlahkan jumlah kali harga.",
            """
            import sqlite3

            def belanja_per_kota(c):
                q = '''
                SELECT g.kota, SUM(p.jumlah * k.harga)
                FROM pesanan p
                JOIN pelanggan g ON p.pelanggan_id = g.id
                JOIN produk k ON p.produk_id = k.id
                GROUP BY g.kota
                '''
                return dict(c.execute(q).fetchall())
            """,
        ),
        E(
            "A6-04-3-ex2",
            "sedang",
            """
            Tulis fungsi `produk_terjual(c)` yang mengembalikan list tuple `(nama_produk, total_jumlah)` untuk SEMUA produk, dengan 0 bila belum terjual, terurut menurut id produk. Pesanan dengan pelanggan tak dikenal tetap dihitung.
            """,
            """
            import sqlite3

            def produk_terjual(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert produk_terjual(c) == [('Pensil', 31), ('Buku', 6), ('Tas', 1), ('Botol', 2)]
            c.execute("INSERT INTO produk VALUES (5, 'Pulpen', 3000)")
            assert produk_terjual(c)[-1] == ('Pulpen', 0)
            c.execute('INSERT INTO pesanan VALUES (9, 1, 5, 4)')
            assert produk_terjual(c)[-1] == ('Pulpen', 4)
            """,
            "LEFT JOIN dari produk ke pesanan dan jumlahkan dengan COALESCE.",
            """
            import sqlite3

            def produk_terjual(c):
                q = '''
                SELECT k.nama, COALESCE(SUM(p.jumlah), 0)
                FROM produk k LEFT JOIN pesanan p ON p.produk_id = k.id
                GROUP BY k.id ORDER BY k.id
                '''
                return c.execute(q).fetchall()
            """,
        ),
        E(
            "A6-04-3-ex3",
            "sedang",
            """
            Tulis fungsi `pelanggan_aktif_per_kota(c)` yang mengembalikan dictionary `{kota: banyak pelanggan berbeda yang punya pesanan}` memakai `COUNT(DISTINCT ...)`.
            """,
            """
            import sqlite3

            def pelanggan_aktif_per_kota(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert pelanggan_aktif_per_kota(c) == {'Bandung': 1, 'Jakarta': 2, 'Surabaya': 1}
            c.execute('INSERT INTO pesanan VALUES (9, 1, 1, 1)')
            assert pelanggan_aktif_per_kota(c)['Jakarta'] == 2
            c.execute('INSERT INTO pesanan VALUES (10, 5, 1, 1)')
            assert pelanggan_aktif_per_kota(c)['Medan'] == 1
            """,
            "Hitung id pelanggan unik setelah JOIN dan kelompokkan menurut kota.",
            """
            import sqlite3

            def pelanggan_aktif_per_kota(c):
                q = '''
                SELECT g.kota, COUNT(DISTINCT g.id)
                FROM pelanggan g JOIN pesanan p ON p.pelanggan_id = g.id
                GROUP BY g.kota
                '''
                return dict(c.execute(q).fetchall())
            """,
        ),
        E(
            "A6-04-3-ex4",
            "menantang",
            """
            Tulis fungsi `pasangan_sekota(c)` yang mengembalikan list tuple `(nama_a, nama_b)` untuk pasangan pelanggan sekota dengan `a.id < b.id`, terurut menurut `a.id` lalu `b.id`, memakai self join.
            """,
            """
            import sqlite3

            def pasangan_sekota(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert pasangan_sekota(c) == [('Ani', 'Citra')]
            c.execute("INSERT INTO pelanggan VALUES (6, 'Fani', 'Bandung')")
            assert pasangan_sekota(c) == [('Ani', 'Citra'), ('Budi', 'Fani')]
            c.execute("INSERT INTO pelanggan VALUES (7, 'Gani', 'Jakarta')")
            assert pasangan_sekota(c) == [('Ani', 'Citra'), ('Ani', 'Gani'), ('Budi', 'Fani'), ('Citra', 'Gani')]
            """,
            "Gabungkan pelanggan dengan dirinya memakai kota sama dan id a lebih kecil dari id b.",
            """
            import sqlite3

            def pasangan_sekota(c):
                q = '''
                SELECT a.nama, b.nama
                FROM pelanggan a JOIN pelanggan b ON a.kota = b.kota AND a.id < b.id
                ORDER BY a.id, b.id
                '''
                return c.execute(q).fetchall()
            """,
        ),
    ],
    [
        M("Memakai COUNT bintang pada hasil JOIN untuk menghitung entitas sisi satu.", "Pakai COUNT DISTINCT pada id entitas."),
        M("Menjumlahkan kolom sisi satu setelah JOIN satu-ke-banyak.", "Ringkas sisi banyak dulu dalam subquery."),
        M("Lupa memastikan kondisi ON sehingga produk Kartesius terbentuk.", "Periksa jumlah baris hasil."),
    ],
    [
        Q("JOIN satu-ke-banyak menyebabkan?", ["Sisi satu berlipat ganda", "Baris hilang", "Kolom bertambah", "Tak ada efek"], 0, "Fan-out.", hint="Gandakan."),
        Q("Menghitung entitas unik setelah JOIN?", ["COUNT DISTINCT id", "COUNT bintang", "SUM", "MAX"], 0, "Hindari duplikasi.", hint="Distinct."),
        Q("Self join memakai?", ["Dua alias tabel sama", "Dua database", "CROSS saja", "Subquery wajib"], 0, "Alias.", hint="Alias."),
        Q("CROSS JOIN 5 kali 4 baris?", ["20", "9", "5", "4"], 0, "Produk Kartesius.", hint="Kali."),
        Q("EXISTS cocok untuk?", ["Menguji keberadaan", "Menjumlah", "Mengurutkan", "Membuat tabel"], 0, "Ada atau tidak.", hint="Ada."),
    ],
    [
        "JOIN dengan GROUP BY menjawab pertanyaan lintas tabel.",
        "JOIN satu-ke-banyak menggandakan sisi satu sehingga agregat bisa membengkak.",
        "Self join membandingkan baris dalam tabel yang sama.",
        "EXISTS menguji keberadaan tanpa menduplikasi baris.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perintah yang cukup jelas dalam teks.", "brief": []}

write_module(
    "A6",
    4,
    "JOIN antar tabel",
    105,
    [
        "Menggabungkan tabel dengan INNER JOIN dan LEFT JOIN",
        "Menemukan baris tanpa pasangan dengan anti-join",
        "Menghindari duplikasi baris dan fan-out pada agregasi gabungan",
    ],
    [l1, l2, l3],
    video,
    REF,
)
