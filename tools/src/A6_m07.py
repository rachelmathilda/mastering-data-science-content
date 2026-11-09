import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

SQL_DB = """
CREATE TABLE transaksi (id INTEGER PRIMARY KEY, nama TEXT, email TEXT, tanggal TEXT, jumlah INTEGER);
INSERT INTO transaksi VALUES
(1, 'Ani Putri', 'ani@mail.com', '2026-01-15', 100),
(2, 'budi santoso', 'BUDI@kantor.co.id', '2026-01-31', 200),
(3, 'Citra Dewi', 'citra@mail.com', '2026-02-10', 150),
(4, ' Dewi Lestari ', 'dewi@kantor.co.id', '2026-02-28', 80),
(5, 'Eko Prasetyo', 'eko@mail.com', '2026-03-05', 120);
"""

SETUP = textwrap.indent("import sqlite3\n\nc = sqlite3.connect(':memory:')\nc.executescript('''" + SQL_DB + "''')\n", '            ')

FIX = textwrap.indent("import sqlite3\n\ndef _db():\n    c = sqlite3.connect(':memory:')\n    c.executescript('''" + textwrap.indent(SQL_DB, '    ') + "    ''')\n    return c\n\n", '            ')
l1 = lesson(
    "A6-07-1",
    "Tanggal ISO, strftime, dan pengelompokan waktu",
    35,
    [
        "Menjelaskan mengapa SQLite menyimpan tanggal sebagai teks ISO",
        "Mengekstrak tahun, bulan, dan hari dengan strftime",
        "Mengelompokkan data per bulan dan per hari dalam minggu",
        "Menyaring rentang tanggal dengan batas setengah terbuka",
    ],
    [
        T("""
        ## Tanggal di SQLite

        SQLite tidak punya tipe tanggal khusus. Tanggal disimpan sebagai teks, angka, atau bilangan Julian, dan fungsi tanggal bawaan memahami ketiganya. Praktik terbaik adalah memakai **teks ISO 8601**, yaitu `YYYY-MM-DD` untuk tanggal dan `YYYY-MM-DD HH:MM:SS` untuk tanggal dengan waktu.

        Format ISO punya sifat penting: urutan alfabetnya sama dengan urutan kronologisnya. Karena itu `ORDER BY tanggal` dan perbandingan `tanggal >= '2026-02-01'` bekerja benar tanpa konversi. Format seperti `15/01/2026` merusak sifat itu dan harus dihindari.
        """),
        T("""
        ## Tabel contoh

        Modul ini memakai tabel `transaksi` dengan kolom `id`, `nama`, `email`, `tanggal`, dan `jumlah`. Ada lima baris dari Januari sampai Maret 2026. Nama dan email sengaja ditulis tidak seragam: ada huruf kecil, huruf besar, dan spasi di tepi, sebagaimana data nyata yang kotor.

        Pelajaran pertama dan kedua membahas tanggal, dan pelajaran ketiga membahas teks. Keduanya kerap dipakai bersamaan saat membersihkan data sebelum dianalisis.
        """),
        T("""
        ## strftime

        `strftime(format, nilai)` mengubah tanggal menjadi teks sesuai format. Kode yang sering dipakai: `%Y` tahun empat digit, `%m` bulan dua digit, `%d` hari dua digit, `%w` hari dalam minggu dari 0 untuk Minggu sampai 6 untuk Sabtu, dan `%j` hari ke berapa dalam tahun.

        Hasilnya selalu teks, bahkan untuk kode numerik. Bila perlu angka, bungkus dengan `CAST(... AS INTEGER)`. Lupa hal ini menimbulkan perbandingan teks yang aneh, misalnya `'10' < '9'` bernilai benar.
        """),
        C(
            SETUP + """
            q = '''
            SELECT id, strftime('%Y', tanggal), strftime('%m', tanggal), strftime('%d', tanggal)
            FROM transaksi ORDER BY id
            '''
            for r in c.execute(q).fetchall():
                print(r)
            print(c.execute("SELECT '10' < '9', 10 < 9").fetchone())
            """,
            """
            (1, '2026', '01', '15')
            (2, '2026', '01', '31')
            (3, '2026', '02', '10')
            (4, '2026', '02', '28')
            (5, '2026', '03', '05')
            (1, 0)
            """,
            """
            Hasil strftime berupa teks, sehingga perbandingan teks sepuluh dan sembilan bernilai benar sedangkan perbandingan angkanya salah.
            """,
            filename="strftime_dasar.py",
        ),
        T("""
        ## Mengelompokkan per bulan

        Laporan periodik hampir selalu mengelompokkan per bulan. Cukup ambil `strftime('%Y-%m', tanggal)` dan jadikan kunci `GROUP BY`. Menyertakan tahun penting: tanpa itu, Januari 2025 dan Januari 2026 tercampur menjadi satu kelompok.

        Alias kolom boleh dipakai di `GROUP BY` dan `ORDER BY` pada SQLite. Format `YYYY-MM` juga terurut kronologis secara alfabet sehingga `ORDER BY` langsung benar.
        """),
        C(
            SETUP + """
            q = '''
            SELECT strftime('%Y-%m', tanggal) AS bulan, SUM(jumlah), COUNT(*)
            FROM transaksi GROUP BY bulan ORDER BY bulan
            '''
            print(c.execute(q).fetchall())
            """,
            """
            [('2026-01', 300, 2), ('2026-02', 230, 2), ('2026-03', 120, 1)]
            """,
            """
            Total dan banyak transaksi per bulan: Januari 300 dari dua transaksi, Februari 230, dan Maret 120.
            """,
            filename="group_bulan.py",
        ),
        T("""
        ## Hari dalam minggu

        Pola mingguan, seperti hari tersibuk, dapat dilihat dengan `strftime('%w', tanggal)`. Kodenya angka dari nol sampai enam, dan nol adalah hari Minggu. Hasilnya teks, jadi ubah ke bilangan bulat bila ingin membandingkan atau memakai sebagai kunci numerik.

        Ingat bahwa urutan hari dimulai dari Minggu. Bila laporan harus dimulai dari Senin, geser dengan `(CAST(strftime('%w', tanggal) AS INTEGER) + 6) % 7`.
        """),
        C(
            SETUP + """
            q = '''
            SELECT CAST(strftime('%w', tanggal) AS INTEGER) AS hari, SUM(jumlah)
            FROM transaksi GROUP BY hari ORDER BY hari
            '''
            print(c.execute(q).fetchall())
            """,
            """
            [(2, 150), (4, 220), (6, 280)]
            """,
            """
            Penjualan terkumpul pada hari Selasa, Kamis, dan Sabtu sesuai kode dua, empat, dan enam.
            """,
            filename="hari_minggu.py",
        ),
        T("""
        ## Menyaring rentang tanggal

        Cara paling aman menyaring satu bulan adalah batas **setengah terbuka**: `tanggal >= '2026-02-01' AND tanggal < '2026-03-01'`. Batas bawah termasuk dan batas atas tidak. Cara ini berfungsi baik untuk tanggal murni maupun untuk tanggal dengan waktu.

        `BETWEEN '2026-02-01' AND '2026-02-28'` terlihat ringkas tetapi berbahaya: bila kolom memuat waktu seperti `2026-02-28 15:30:00`, nilai itu lebih besar dari `'2026-02-28'` sehingga transaksi sore hari terlewat.
        """),
        C(
            SETUP + """
            q = '''
            SELECT id FROM transaksi
            WHERE tanggal >= '2026-02-01' AND tanggal < '2026-03-01' ORDER BY id
            '''
            print([r[0] for r in c.execute(q).fetchall()])
            c.execute("INSERT INTO transaksi VALUES (6, 'X', 'x@mail.com', '2026-02-28 15:30:00', 10)")
            q1 = "SELECT id FROM transaksi WHERE tanggal BETWEEN '2026-02-01' AND '2026-02-28' ORDER BY id"
            q2 = "SELECT id FROM transaksi WHERE tanggal >= '2026-02-01' AND tanggal < '2026-03-01' ORDER BY id"
            print([r[0] for r in c.execute(q1).fetchall()])
            print([r[0] for r in c.execute(q2).fetchall()])
            """,
            """
            [3, 4]
            [3, 4]
            [3, 4, 6]
            """,
            """
            BETWEEN melewatkan transaksi enam yang bertanggal dua puluh delapan pukul 15:30, sedangkan batas setengah terbuka menangkapnya.
            """,
            filename="rentang_tanggal.py",
        ),
        T("""
        ## Menyimpan tanggal dengan benar

        Simpan tanggal sebagai teks ISO di kolom bertipe `TEXT` dan jangan mencampur dengan format lain. Satu baris berformat salah dapat merusak pengurutan dan fungsi tanggal, yang akan mengembalikan `NULL` untuk teks tak dikenali. Bila data berasal dari sumber luar, normalkan formatnya saat impor.

        Pertimbangkan pula zona waktu. Cara praktis adalah menyimpan waktu dalam UTC lalu mengonversinya saat ditampilkan. Mencampur zona waktu dalam satu kolom adalah sumber galat yang sulit dilacak.
        """),
        K(
            "warn",
            """
            Jangan memakai BETWEEN untuk tanggal yang bisa memuat waktu. Pakai batas bawah termasuk dan batas atas tidak termasuk.
            """,
            title="Batas setengah terbuka",
        ),
        T("""
        ## Tanggal dengan waktu

        Kolom yang memuat waktu, seperti `2026-02-28 15:30:00`, tetap berformat ISO dan tetap terurut benar. Untuk mengambil bagian tanggalnya saja, pakai `date(kolom)` atau `substr(kolom, 1, 10)`. Mengelompokkan per hari berarti mengelompokkan menurut `date(kolom)`, bukan menurut teks lengkap berikut waktunya.

        Kelalaian umum adalah membandingkan kolom ber-waktu dengan tanggal murni memakai tanda sama dengan. Nilai `2026-02-28 15:30:00` tidak sama dengan `2026-02-28`, sehingga baris itu tidak ditemukan.
        """),
        E(
            "A6-07-1-ex1",
            "mudah",
            """
            Tulis fungsi `bulan_dari(c)` yang mengembalikan list teks `YYYY-MM` dari kolom `tanggal` semua transaksi, terurut menurut id.
            """,
            """
            import sqlite3

            def bulan_dari(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert bulan_dari(c) == ['2026-01', '2026-01', '2026-02', '2026-02', '2026-03']
            c.execute("INSERT INTO transaksi VALUES (6, 'X', 'x@mail.com', '2025-12-31', 5)")
            assert bulan_dari(c)[-1] == '2025-12'
            assert len(bulan_dari(c)) == 6
            """,
            "Pakai strftime dengan format %Y-%m.",
            """
            import sqlite3

            def bulan_dari(c):
                q = "SELECT strftime('%Y-%m', tanggal) FROM transaksi ORDER BY id"
                return [r[0] for r in c.execute(q).fetchall()]
            """,
        ),
        E(
            "A6-07-1-ex2",
            "sedang",
            """
            Tulis fungsi `total_per_bulan(c)` yang mengembalikan list tuple `(bulan, total_jumlah)` dengan bulan berformat `YYYY-MM`, terurut kronologis.
            """,
            """
            import sqlite3

            def total_per_bulan(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert total_per_bulan(c) == [('2026-01', 300), ('2026-02', 230), ('2026-03', 120)]
            c.execute("INSERT INTO transaksi VALUES (6, 'X', 'x@mail.com', '2026-03-20', 30)")
            assert total_per_bulan(c)[-1] == ('2026-03', 150)
            c.execute("INSERT INTO transaksi VALUES (7, 'Y', 'y@mail.com', '2025-03-20', 7)")
            assert total_per_bulan(c)[0] == ('2025-03', 7)
            """,
            "GROUP BY strftime tahun dan bulan.",
            """
            import sqlite3

            def total_per_bulan(c):
                q = '''
                SELECT strftime('%Y-%m', tanggal) AS bulan, SUM(jumlah)
                FROM transaksi GROUP BY bulan ORDER BY bulan
                '''
                return c.execute(q).fetchall()
            """,
        ),
        E(
            "A6-07-1-ex3",
            "sedang",
            """
            Tulis fungsi `transaksi_bulan(c, awal)` yang menerima tanggal awal bulan berformat `YYYY-MM-01` dan mengembalikan list id transaksi pada bulan itu, terurut menurut id, memakai batas setengah terbuka dan `date(awal, '+1 month')`.
            """,
            """
            import sqlite3

            def transaksi_bulan(c, awal):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert transaksi_bulan(c, '2026-02-01') == [3, 4]
            assert transaksi_bulan(c, '2026-01-01') == [1, 2]
            assert transaksi_bulan(c, '2026-03-01') == [5]
            assert transaksi_bulan(c, '2026-04-01') == []
            """,
            "Batas atas adalah date(awal, '+1 month') dan tidak termasuk.",
            """
            import sqlite3

            def transaksi_bulan(c, awal):
                q = "SELECT id FROM transaksi WHERE tanggal >= ? AND tanggal < date(?, '+1 month') ORDER BY id"
                return [r[0] for r in c.execute(q, (awal, awal)).fetchall()]
            """,
        ),
        E(
            "A6-07-1-ex4",
            "menantang",
            """
            Tulis fungsi `jumlah_per_hari(c)` yang mengembalikan dict `{kode_hari: total_jumlah}` dengan `kode_hari` bilangan bulat dari `strftime('%w')` (0 Minggu sampai 6 Sabtu).
            """,
            """
            import sqlite3

            def jumlah_per_hari(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert jumlah_per_hari(c) == {2: 150, 4: 220, 6: 280}
            c.execute("INSERT INTO transaksi VALUES (6, 'X', 'x@mail.com', '2026-03-08', 40)")
            assert jumlah_per_hari(c)[0] == 40
            c.execute("INSERT INTO transaksi VALUES (7, 'Y', 'y@mail.com', '2026-03-12', 10)")
            assert jumlah_per_hari(c)[4] == 230
            """,
            "Ubah hasil strftime menjadi bilangan bulat dengan CAST lalu GROUP BY.",
            """
            import sqlite3

            def jumlah_per_hari(c):
                q = '''
                SELECT CAST(strftime('%w', tanggal) AS INTEGER) AS hari, SUM(jumlah)
                FROM transaksi GROUP BY hari
                '''
                return dict(c.execute(q).fetchall())
            """,
        ),
    ],
    [
        M("Menyimpan tanggal dengan format 15/01/2026.", "Simpan sebagai teks ISO YYYY-MM-DD."),
        M("Memakai BETWEEN untuk kolom yang memuat waktu.", "Pakai batas bawah termasuk dan batas atas tidak."),
        M("Mengelompokkan per bulan tanpa tahun.", "Gunakan format %Y-%m."),
    ],
    [
        Q("Format tanggal terbaik di SQLite?", ["Teks ISO 8601", "DD/MM/YYYY", "Nama bulan", "Angka acak"], 0, "Urutan alfabet sama dengan kronologis.", hint="ISO."),
        Q("Kode strftime untuk bulan dua digit?", ["%m", "%M", "%b", "%d"], 0, "%m bulan.", hint="Kecil."),
        Q("Hasil strftime bertipe?", ["Teks", "Bilangan bulat", "Tanggal", "Boolean"], 0, "Selalu teks.", hint="Teks."),
        Q("Kode %w bernilai nol untuk hari?", ["Minggu", "Senin", "Sabtu", "Jumat"], 0, "Minggu sampai Sabtu 0 sampai 6.", hint="Awal minggu."),
        Q("Batas aman rentang bulan?", ["Setengah terbuka", "BETWEEN dua tanggal", "LIKE", "Tanpa batas"], 0, "Tangkap waktu pada hari terakhir.", hint="Setengah."),
    ],
    [
        "Simpan tanggal sebagai teks ISO agar urutan alfabet sama dengan kronologis.",
        "strftime mengekstrak bagian tanggal sebagai teks.",
        "Kelompokkan per bulan dengan format tahun dan bulan.",
        "Gunakan batas setengah terbuka untuk rentang tanggal.",
    ],
    [],
)

l2 = lesson(
    "A6-07-2",
    "Aritmetika tanggal dan jebakannya",
    35,
    [
        "Menambah dan mengurangi hari, bulan, dan tahun dengan date",
        "Mencari awal dan akhir bulan",
        "Menghitung selisih hari dengan julianday",
        "Mengenali tanggal tidak valid dan jebakan luapan",
    ],
    [
        T("""
        ## Fungsi date dan modifier

        `date(nilai, modifier, ...)` menghasilkan tanggal ISO setelah menerapkan satu atau lebih **modifier** berurutan. Modifier yang umum: `'+7 days'`, `'-1 month'`, `'+1 year'`, `'start of month'`, `'start of year'`, dan `'weekday 1'` untuk maju ke Senin berikutnya.

        Modifier diterapkan dari kiri ke kanan sehingga urutannya berpengaruh. Karena itu `date(x, 'start of month', '+1 month', '-1 day')` menghasilkan hari terakhir bulan itu: mulai dari awal bulan, maju sebulan, mundur sehari.
        """),
        C(
            SETUP + """
            q = '''
            SELECT id, date(tanggal, '+7 days'), date(tanggal, '+1 month')
            FROM transaksi ORDER BY id
            '''
            for r in c.execute(q).fetchall():
                print(r)
            """,
            """
            (1, '2026-01-22', '2026-02-15')
            (2, '2026-02-07', '2026-03-03')
            (3, '2026-02-17', '2026-03-10')
            (4, '2026-03-07', '2026-03-28')
            (5, '2026-03-12', '2026-04-05')
            """,
            """
            Menambah tujuh hari dan satu bulan. Perhatikan baris dua: tiga puluh satu Januari ditambah satu bulan menjadi tiga Maret, bukan akhir Februari.
            """,
            filename="modifier_date.py",
        ),
        T("""
        ## Jebakan akhir bulan

        Menambah satu bulan pada tanggal 31 Januari menghasilkan 31 Februari yang tidak ada. SQLite tidak menolaknya tetapi meluapkannya ke bulan berikutnya, sehingga hasilnya 3 Maret pada tahun 2026. Banyak pemula mengira hasilnya 28 Februari.

        Bila Anda membutuhkan akhir bulan berikutnya, jangan memakai `+1 month` pada tanggal akhir bulan. Gunakan pola awal bulan, tambah satu bulan, lalu kurangi sehari agar selalu tepat.
        """),
        C(
            SETUP + """
            print(c.execute("SELECT date('2026-01-31', '+1 month')").fetchone())
            q = '''
            SELECT id, date(tanggal, 'start of month'),
                   date(tanggal, 'start of month', '+1 month', '-1 day')
            FROM transaksi ORDER BY id
            '''
            for r in c.execute(q).fetchall():
                print(r)
            """,
            """
            ('2026-03-03',)
            (1, '2026-01-01', '2026-01-31')
            (2, '2026-01-01', '2026-01-31')
            (3, '2026-02-01', '2026-02-28')
            (4, '2026-02-01', '2026-02-28')
            (5, '2026-03-01', '2026-03-31')
            """,
            """
            Awal dan akhir bulan dihitung benar tanpa terjebak luapan, termasuk Februari yang berakhir pada dua puluh delapan.
            """,
            filename="awal_akhir_bulan.py",
        ),
        T("""
        ## Selisih hari dengan julianday

        `julianday(tanggal)` mengubah tanggal menjadi bilangan Julian, yaitu jumlah hari sejak titik acuan kuno, sebagai bilangan desimal. Selisih dua bilangan Julian adalah selisih hari. Bungkus dengan `CAST(... AS INTEGER)` atau `ROUND` untuk mendapatkan hari bulat.

        Gunakan pola ini untuk usia akun, lama pengiriman, atau jumlah hari sejak transaksi terakhir. Selisih bertanda: bila tanggal pertama lebih akhir, hasilnya negatif.
        """),
        C(
            SETUP + """
            q = '''
            SELECT id, CAST(julianday('2026-03-31') - julianday(tanggal) AS INTEGER)
            FROM transaksi ORDER BY id
            '''
            print([r[1] for r in c.execute(q).fetchall()])
            print(c.execute("SELECT CAST(julianday('2026-03-01') - julianday('2026-03-05') AS INTEGER)").fetchone())
            """,
            """
            [75, 59, 49, 31, 26]
            (-4,)
            """,
            """
            Jarak setiap transaksi ke tiga puluh satu Maret dalam hari, dan selisih negatif bila urutan dibalik.
            """,
            filename="julianday_selisih.py",
        ),
        T("""
        ## Tanggal tidak valid

        Fungsi tanggal mengembalikan `NULL` untuk teks yang tidak dapat dibaca sama sekali, misalnya `'bukan'` atau bulan ketiga belas. Tetapi tanggal dengan hari berlebih seperti `'2026-02-30'` tidak ditolak: ia diluapkan menjadi `'2026-03-02'`.

        Untuk memeriksa validitas yang ketat, bandingkan `date(s)` dengan `s` itu sendiri. Bila berbeda atau `NULL`, string itu bukan tanggal ISO yang valid. Pemeriksaan ini berguna saat membersihkan data impor.
        """),
        C(
            """
            import sqlite3

            c = sqlite3.connect(':memory:')
            print(c.execute("SELECT date('2026-02-30'), date('bukan'), date('2026-13-01')").fetchone())
            for s in ['2026-02-28', '2026-02-30', 'bukan']:
                print(s, bool(c.execute('SELECT date(?) = ?', (s, s)).fetchone()[0]))
            """,
            """
            ('2026-03-02', None, None)
            2026-02-28 True
            2026-02-30 False
            bukan False
            """,
            """
            Hari berlebih diluapkan alih-alih ditolak, dan perbandingan date dengan teks asli menangkap kedua jenis tanggal rusak.
            """,
            filename="tanggal_valid.py",
        ),
        T("""
        ## Maju ke hari tertentu

        Modifier `weekday N` memajukan tanggal ke hari ke-N berikutnya, dengan nol Minggu dan satu Senin. Bila tanggal itu sudah jatuh pada hari tersebut, ia tidak berubah. Ini berguna untuk menghitung tenggat berikutnya yang selalu jatuh pada Senin.

        Gabungkan dengan modifier lain, misalnya `date(x, '+7 days', 'weekday 1')`, untuk mendapatkan Senin pertama sesudah satu minggu. Selalu uji dengan beberapa tanggal contoh sebelum mempercayai rumus waktu.
        """),
        T("""
        ## Tanggal sekarang

        `date('now')` menghasilkan tanggal hari ini dalam UTC, dan `datetime('now')` menyertakan waktu. Tambahkan modifier `'localtime'` untuk waktu setempat. Karena hasilnya berubah tiap hari, query yang memakai `'now'` tidak dapat diuji dengan hasil tetap.

        Untuk pengujian dan laporan yang dapat diulang, kirim tanggal acuan sebagai parameter alih-alih memakai `'now'` di dalam query. Dengan begitu hasilnya deterministik dan mudah diverifikasi.
        """),
        K(
            "warn",
            """
            Menambah satu bulan pada tanggal 29 sampai 31 dapat meluap ke bulan berikutnya. Untuk akhir bulan pakai awal bulan, tambah satu bulan, kurangi satu hari.
            """,
            title="Luapan akhir bulan",
        ),
        T("""
        ## Usia dan masa berlaku

        Selisih hari bermanfaat untuk banyak pertanyaan bisnis: sudah berapa hari sejak pelanggan terakhir membeli, berapa hari lagi langganan berakhir, atau berapa lama tiket tertunda. Hitung dengan `julianday(acuan) - julianday(tanggal)` dan beri tanggal acuan sebagai parameter agar hasil dapat diulang.

        Untuk usia dalam tahun, jangan membagi hari dengan 365 begitu saja karena tahun kabisat menggeser hasil. Bandingkan bagian tahun dan koreksi bila ulang tahun tahun ini belum tiba.
        """),
        T("""
        ## Menyusun kalender dengan CTE rekursif

        Data sering memiliki hari tanpa transaksi, sehingga grafik harian berlubang. Solusinya membangun tabel kalender dengan CTE rekursif yang menambah satu hari tiap langkah, lalu menggabungkannya dengan LEFT JOIN ke data. Hari tanpa transaksi muncul dengan jumlah kosong yang dapat diganti nol dengan COALESCE.

        Teknik ini menggabungkan beberapa pelajaran sebelumnya: CTE rekursif, LEFT JOIN, dan fungsi tanggal. Ia sangat umum dalam laporan deret waktu.
        """),
        T("""
        ## Zona waktu dan konsistensi

        Fungsi tanggal SQLite bekerja dalam UTC kecuali diberi modifier `'localtime'`. Bila sebagian data tercatat dalam waktu lokal dan sebagian dalam UTC, hasil penjumlahan per hari menjadi salah karena transaksi larut malam jatuh ke hari berbeda.

        Tetapkan satu konvensi sejak awal, idealnya menyimpan UTC, dan dokumentasikan. Konversi hanya saat menampilkan. Konsistensi di sini lebih penting daripada pilihan zona yang dipakai.
        """),
        E(
            "A6-07-2-ex1",
            "mudah",
            """
            Tulis fungsi `tambah_hari(c, tgl, n)` yang mengembalikan teks tanggal `tgl` ditambah `n` hari (n boleh negatif) memakai `date`.
            """,
            """
            import sqlite3

            def tambah_hari(c, tgl, n):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert tambah_hari(c, '2026-01-31', 1) == '2026-02-01'
            assert tambah_hari(c, '2026-02-28', 1) == '2026-03-01'
            assert tambah_hari(c, '2026-03-05', -5) == '2026-02-28'
            assert tambah_hari(c, '2026-03-05', 0) == '2026-03-05'
            """,
            "Susun modifier dengan n || ' days'.",
            """
            import sqlite3

            def tambah_hari(c, tgl, n):
                return c.execute("SELECT date(?, ? || ' days')", (tgl, n)).fetchone()[0]
            """,
        ),
        E(
            "A6-07-2-ex2",
            "sedang",
            """
            Tulis fungsi `selisih_hari(c, a, b)` yang mengembalikan bilangan bulat jumlah hari dari tanggal `a` sampai tanggal `b` (negatif bila `b` lebih awal).
            """,
            """
            import sqlite3

            def selisih_hari(c, a, b):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert selisih_hari(c, '2026-01-15', '2026-03-31') == 75
            assert selisih_hari(c, '2026-03-01', '2026-03-01') == 0
            assert selisih_hari(c, '2026-03-05', '2026-03-01') == -4
            assert selisih_hari(c, '2026-01-01', '2027-01-01') == 365
            """,
            "Kurangkan dua julianday lalu ubah ke bilangan bulat.",
            """
            import sqlite3

            def selisih_hari(c, a, b):
                q = 'SELECT CAST(ROUND(julianday(?) - julianday(?)) AS INTEGER)'
                return c.execute(q, (b, a)).fetchone()[0]
            """,
        ),
        E(
            "A6-07-2-ex3",
            "sedang",
            """
            Tulis fungsi `akhir_bulan(c)` yang mengembalikan list tuple `(id, akhir_bulan)` untuk semua transaksi, terurut menurut id, dengan `akhir_bulan` adalah hari terakhir bulan dari `tanggal`.
            """,
            """
            import sqlite3

            def akhir_bulan(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            r = akhir_bulan(c)
            assert r[0] == (1, '2026-01-31')
            assert r[2] == (3, '2026-02-28')
            assert r[4] == (5, '2026-03-31')
            c.execute("INSERT INTO transaksi VALUES (6, 'X', 'x@mail.com', '2028-02-10', 1)")
            assert akhir_bulan(c)[-1] == (6, '2028-02-29')
            """,
            "Awal bulan, tambah satu bulan, kurangi satu hari.",
            """
            import sqlite3

            def akhir_bulan(c):
                q = "SELECT id, date(tanggal, 'start of month', '+1 month', '-1 day') FROM transaksi ORDER BY id"
                return c.execute(q).fetchall()
            """,
        ),
        E(
            "A6-07-2-ex4",
            "menantang",
            """
            Tulis fungsi `tanggal_valid(c, s)` yang mengembalikan `True` hanya bila teks `s` adalah tanggal ISO valid yang ketat, artinya `date(s)` sama persis dengan `s`.
            """,
            """
            import sqlite3

            def tanggal_valid(c, s):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert tanggal_valid(c, '2026-02-28') is True
            assert tanggal_valid(c, '2026-02-30') is False
            assert tanggal_valid(c, 'bukan') is False
            assert tanggal_valid(c, '2028-02-29') is True
            """,
            "Bandingkan date(s) dengan s dan ubah hasil NULL menjadi False.",
            """
            import sqlite3

            def tanggal_valid(c, s):
                r = c.execute('SELECT date(?) = ?', (s, s)).fetchone()[0]
                return bool(r)
            """,
        ),
    ],
    [
        M("Menambah satu bulan pada tanggal 31 dan mengira hasilnya akhir bulan.", "Pakai awal bulan, tambah satu bulan, kurangi satu hari."),
        M("Menganggap date menolak tanggal 30 Februari.", "Ia meluapkan ke Maret, jadi bandingkan dengan teks asli."),
        M("Memakai 'now' di query yang harus diuji.", "Kirim tanggal acuan sebagai parameter."),
    ],
    [
        Q("date('2026-01-31', '+1 month') menghasilkan?", ["2026-03-03", "2026-02-28", "2026-02-31", "NULL"], 0, "Meluap ke Maret.", hint="Luapan."),
        Q("Selisih hari dihitung dengan?", ["julianday", "strftime", "length", "round"], 0, "Bilangan Julian.", hint="Julian."),
        Q("Akhir bulan dihitung dengan?", ["Awal bulan, tambah satu bulan, kurangi satu hari", "Tambah 30 hari", "Tambah satu bulan saja", "Ambil hari 28"], 0, "Selalu tepat.", hint="Awal."),
        Q("date('bukan') menghasilkan?", ["NULL", "Error", "Hari ini", "Nol"], 0, "Teks tak dikenali.", hint="Kosong."),
        Q("Modifier diterapkan?", ["Dari kiri ke kanan", "Dari kanan ke kiri", "Acak", "Sekaligus"], 0, "Urutan berpengaruh.", hint="Urut."),
    ],
    [
        "Modifier date diterapkan berurutan dan urutannya berpengaruh.",
        "Penambahan bulan pada tanggal akhir bulan dapat meluap.",
        "julianday memudahkan selisih hari.",
        "Validasi ketat membandingkan date(s) dengan s.",
    ],
    [],
)

l3 = lesson(
    "A6-07-3",
    "Fungsi teks dan pembersihan data",
    35,
    [
        "Memakai UPPER, LOWER, TRIM, dan LENGTH",
        "Memotong teks dengan SUBSTR dan INSTR",
        "Menyusun teks dengan penggabungan dan PRINTF",
        "Membersihkan data kotor sebelum pengelompokan",
    ],
    [
        T("""
        ## Data teks yang kotor

        Data teks di dunia nyata jarang rapi. Nama ditulis dengan huruf besar dan kecil acak, email memuat huruf kapital, dan spasi berlebih menempel di tepi. Bila data seperti ini langsung dikelompokkan, `kantor.co.id` dan `KANTOR.CO.ID` menjadi dua kelompok berbeda.

        Karena itu pembersihan teks adalah langkah awal analisis. SQL menyediakan fungsi yang cukup untuk sebagian besar kebutuhan: ubah huruf, pangkas spasi, potong bagian, cari posisi, dan ganti isi.
        """),
        T("""
        ## UPPER, LOWER, TRIM, LENGTH

        `UPPER` dan `LOWER` mengubah huruf besar atau kecil, dan pada SQLite hanya berlaku untuk huruf ASCII. `TRIM` membuang spasi di kedua tepi, `LTRIM` hanya kiri, `RTRIM` hanya kanan. `LENGTH` menghitung jumlah karakter.

        Urutan penting: `LENGTH(TRIM(nama))` menghitung panjang setelah dipangkas, sedangkan `LENGTH(nama)` menghitung juga spasi tepi. Perbedaan dua hitungan itu justru cara cepat mendeteksi spasi tak diinginkan.
        """),
        C(
            SETUP + """
            q = '''
            SELECT id, UPPER(nama), LOWER(email), LENGTH(nama), LENGTH(TRIM(nama))
            FROM transaksi ORDER BY id
            '''
            for r in c.execute(q).fetchall():
                print(r)
            """,
            """
            (1, 'ANI PUTRI', 'ani@mail.com', 9, 9)
            (2, 'BUDI SANTOSO', 'budi@kantor.co.id', 12, 12)
            (3, 'CITRA DEWI', 'citra@mail.com', 10, 10)
            (4, ' DEWI LESTARI ', 'dewi@kantor.co.id', 14, 12)
            (5, 'EKO PRASETYO', 'eko@mail.com', 12, 12)
            """,
            """
            Hanya baris empat yang panjangnya berubah setelah TRIM, menandakan spasi di tepi.
            """,
            filename="teks_dasar.py",
        ),
        T("""
        ## SUBSTR dan INSTR

        `SUBSTR(teks, mulai, panjang)` mengambil potongan, dengan posisi dimulai dari satu. Posisi negatif menghitung dari belakang, dan panjang boleh dihilangkan untuk mengambil sampai akhir. `INSTR(teks, cari)` mengembalikan posisi kemunculan pertama, atau nol bila tidak ada.

        Keduanya bersama-sama memecah teks pada pemisah. Domain email adalah potongan setelah tanda `@`: `SUBSTR(email, INSTR(email, '@') + 1)`. Bagian sebelum `@` adalah `SUBSTR(email, 1, INSTR(email, '@') - 1)`.
        """),
        C(
            SETUP + """
            q = '''
            SELECT id, SUBSTR(email, 1, INSTR(email, '@') - 1),
                   SUBSTR(email, INSTR(email, '@') + 1)
            FROM transaksi ORDER BY id
            '''
            for r in c.execute(q).fetchall():
                print(r)
            print(c.execute("SELECT INSTR('abc', 'z'), SUBSTR('abcdef', 2, 3), SUBSTR('abcdef', -3)").fetchone())
            """,
            """
            (1, 'ani', 'mail.com')
            (2, 'BUDI', 'kantor.co.id')
            (3, 'citra', 'mail.com')
            (4, 'dewi', 'kantor.co.id')
            (5, 'eko', 'mail.com')
            (0, 'bcd', 'def')
            """,
            """
            Email dipecah menjadi nama pengguna dan domain, dan contoh terakhir menunjukkan INSTR nol saat tidak ketemu serta SUBSTR dari belakang.
            """,
            filename="substr_instr.py",
        ),
        T("""
        ## Menggabungkan teks

        Operator `||` menggabungkan teks. Waspadai `NULL`: `'a' || NULL` menghasilkan `NULL`, sehingga satu kolom kosong menghapus seluruh hasil gabungan. Gunakan `COALESCE(kolom, '')` untuk mengganti `NULL` dengan teks kosong sebelum menggabungkan.

        `REPLACE(teks, lama, baru)` mengganti semua kemunculan. Untuk format angka, `PRINTF('%05d', id)` memberi nol di depan sehingga satu menjadi `00001`, dan `PRINTF('%.1f', x)` membulatkan ke satu desimal.
        """),
        C(
            SETUP + """
            q = '''
            SELECT id, nama || ' <' || LOWER(email) || '>', REPLACE(email, '@', '[at]'), PRINTF('%05d', id)
            FROM transaksi WHERE id <= 2 ORDER BY id
            '''
            for r in c.execute(q).fetchall():
                print(r)
            print(c.execute("SELECT 'a' || NULL, 'a' || COALESCE(NULL, '')").fetchone())
            """,
            """
            (1, 'Ani Putri <ani@mail.com>', 'ani[at]mail.com', '00001')
            (2, 'budi santoso <budi@kantor.co.id>', 'BUDI[at]kantor.co.id', '00002')
            (None, 'a')
            """,
            """
            Penggabungan dan format teks bekerja, dan NULL menghapus seluruh hasil gabungan kecuali diganti COALESCE.
            """,
            filename="gabung_teks.py",
        ),
        T("""
        ## Membersihkan sebelum mengelompokkan

        Pola umum: normalkan dulu, kelompokkan kemudian. Domain email dinormalkan dengan `LOWER` sebelum dipakai di `GROUP BY`, sehingga `Mail.com` dan `mail.com` menjadi satu kelompok. Tanpa langkah ini, hitungan terpecah dan laporan menyesatkan.

        Lakukan pembersihan dalam CTE atau subquery agar logikanya terpisah dari agregasi. Hasilnya query yang mudah diperiksa dan dapat dipakai ulang untuk kolom lain.
        """),
        C(
            SETUP + """
            q = '''
            SELECT LOWER(SUBSTR(email, INSTR(email, '@') + 1)) AS domain, COUNT(*), SUM(jumlah)
            FROM transaksi GROUP BY domain ORDER BY domain
            '''
            print(c.execute(q).fetchall())
            c.execute("INSERT INTO transaksi VALUES (6, 'Fani', 'f@MAIL.com', '2026-03-30', 30)")
            print(c.execute(q).fetchall())
            """,
            """
            [('kantor.co.id', 2, 280), ('mail.com', 3, 370)]
            [('kantor.co.id', 2, 280), ('mail.com', 4, 400)]
            """,
            """
            Domain dengan huruf kapital tetap masuk kelompok mail.com karena dinormalkan lebih dulu.
            """,
            filename="bersih_kelompok.py",
        ),
        T("""
        ## LIKE dan pencarian pola

        `LIKE` memakai `%` untuk sembarang deret karakter dan `_` untuk satu karakter. Pada SQLite, `LIKE` tidak peka huruf besar untuk ASCII, sehingga `nama LIKE '%dewi%'` menemukan `Citra Dewi` dan ` Dewi Lestari `. Pada basis data lain perilaku ini berbeda.

        Untuk pencarian awalan yang tidak terpengaruh spasi, pangkas dulu: `LOWER(TRIM(nama)) LIKE 'd%'`. Pencarian dengan `%` di depan tidak dapat memanfaatkan indeks, jadi hati-hati pada tabel besar.
        """),
        T("""
        ## Mengambil kata pertama

        Nama depan adalah bagian sebelum spasi pertama. Setelah memangkas, `SUBSTR(t, 1, INSTR(t || ' ', ' ') - 1)` mengambilnya, dengan trik menambahkan spasi di belakang agar nama satu kata tetap berhasil. Tanpa trik itu, `INSTR` mengembalikan nol dan hasilnya salah.

        Trik kecil seperti ini sering menyelamatkan query dari kasus tepi. Selalu uji dengan nama satu kata, kolom kosong, dan spasi berlebih.
        """),
        K(
            "tip",
            """
            Normalkan teks dengan LOWER dan TRIM sebelum GROUP BY atau JOIN agar variasi penulisan tidak memecah kelompok.
            """,
            title="Normalkan dulu",
        ),
        T("""
        ## Memeriksa kualitas teks

        Sebelum membersihkan, ukur dulu seberapa kotor datanya. Hitung baris yang panjangnya berubah setelah `TRIM`, baris yang emailnya tidak memuat `@`, dan baris dengan huruf kapital campur. Angka-angka ini memberi gambaran skala masalah dan membantu memutuskan aturan pembersihan.

        Simpan hasil pemeriksaan sebagai bagian dokumentasi. Bila data baru datang, jalankan pemeriksaan yang sama untuk memastikan kualitasnya tidak memburuk.
        """),
        T("""
        ## Batas fungsi teks bawaan

        Fungsi teks SQLite sederhana. `UPPER` dan `LOWER` hanya memahami ASCII, sehingga huruf beraksen tidak berubah. Tidak ada fungsi bawaan untuk ekspresi reguler pada instalasi standar. Pembersihan rumit seperti memecah alamat atau menormalkan nama sering lebih mudah dilakukan di Python atau pandas.

        Gunakan SQL untuk pembersihan ringan yang selaras dengan kueri, dan pindahkan pekerjaan rumit ke tahap pengolahan data berikutnya. Memilih alat yang tepat lebih penting daripada memaksakan satu alat.
        """),
        E(
            "A6-07-3-ex1",
            "mudah",
            """
            Tulis fungsi `nama_bersih(c)` yang mengembalikan list nama yang sudah dipangkas spasi tepinya, terurut menurut id.
            """,
            """
            import sqlite3

            def nama_bersih(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert nama_bersih(c) == ['Ani Putri', 'budi santoso', 'Citra Dewi', 'Dewi Lestari', 'Eko Prasetyo']
            c.execute("INSERT INTO transaksi VALUES (6, '  Fani  ', 'f@x.com', '2026-03-30', 1)")
            assert nama_bersih(c)[-1] == 'Fani'
            assert len(nama_bersih(c)) == 6
            """,
            "Pakai TRIM pada kolom nama.",
            """
            import sqlite3

            def nama_bersih(c):
                q = 'SELECT TRIM(nama) FROM transaksi ORDER BY id'
                return [r[0] for r in c.execute(q).fetchall()]
            """,
        ),
        E(
            "A6-07-3-ex2",
            "sedang",
            """
            Tulis fungsi `domain_email(c)` yang mengembalikan list domain email berhuruf kecil untuk semua transaksi, terurut menurut id.
            """,
            """
            import sqlite3

            def domain_email(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert domain_email(c) == ['mail.com', 'kantor.co.id', 'mail.com', 'kantor.co.id', 'mail.com']
            c.execute("INSERT INTO transaksi VALUES (6, 'F', 'f@MAIL.COM', '2026-03-30', 1)")
            assert domain_email(c)[-1] == 'mail.com'
            assert len(domain_email(c)) == 6
            """,
            "Ambil teks setelah tanda @ lalu ubah ke huruf kecil.",
            """
            import sqlite3

            def domain_email(c):
                q = "SELECT LOWER(SUBSTR(email, INSTR(email, '@') + 1)) FROM transaksi ORDER BY id"
                return [r[0] for r in c.execute(q).fetchall()]
            """,
        ),
        E(
            "A6-07-3-ex3",
            "sedang",
            """
            Tulis fungsi `jumlah_per_domain(c)` yang mengembalikan list tuple `(domain, total_jumlah)` dengan domain berhuruf kecil, terurut menurut domain.
            """,
            """
            import sqlite3

            def jumlah_per_domain(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert jumlah_per_domain(c) == [('kantor.co.id', 280), ('mail.com', 370)]
            c.execute("INSERT INTO transaksi VALUES (6, 'F', 'f@MAIL.com', '2026-03-30', 30)")
            assert jumlah_per_domain(c)[1] == ('mail.com', 400)
            c.execute("INSERT INTO transaksi VALUES (7, 'G', 'g@baru.id', '2026-03-31', 5)")
            assert jumlah_per_domain(c)[0] == ('baru.id', 5)
            """,
            "Normalkan domain dengan LOWER lalu GROUP BY.",
            """
            import sqlite3

            def jumlah_per_domain(c):
                q = '''
                SELECT LOWER(SUBSTR(email, INSTR(email, '@') + 1)) AS domain, SUM(jumlah)
                FROM transaksi GROUP BY domain ORDER BY domain
                '''
                return c.execute(q).fetchall()
            """,
        ),
        E(
            "A6-07-3-ex4",
            "menantang",
            """
            Tulis fungsi `nama_depan(c)` yang mengembalikan list kata pertama dari nama yang sudah dipangkas, terurut menurut id. Nama satu kata harus tetap berhasil.
            """,
            """
            import sqlite3

            def nama_depan(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert nama_depan(c) == ['Ani', 'budi', 'Citra', 'Dewi', 'Eko']
            c.execute("INSERT INTO transaksi VALUES (6, 'Fani', 'f@x.com', '2026-03-30', 1)")
            assert nama_depan(c)[-1] == 'Fani'
            c.execute("INSERT INTO transaksi VALUES (7, '  Gita Rahma', 'g@x.com', '2026-03-31', 1)")
            assert nama_depan(c)[-1] == 'Gita'
            """,
            "Pangkas dulu lalu potong sebelum spasi pertama dengan menambahkan spasi di belakang.",
            """
            import sqlite3

            def nama_depan(c):
                q = '''
                SELECT SUBSTR(TRIM(nama), 1, INSTR(TRIM(nama) || ' ', ' ') - 1)
                FROM transaksi ORDER BY id
                '''
                return [r[0] for r in c.execute(q).fetchall()]
            """,
        ),
    ],
    [
        M("Mengelompokkan teks tanpa menormalkan huruf.", "Gunakan LOWER dan TRIM terlebih dahulu."),
        M("Menggabungkan kolom yang bisa NULL dengan ||.", "Bungkus dengan COALESCE."),
        M("Memotong nama satu kata tanpa trik spasi.", "Tambahkan spasi di belakang sebelum INSTR."),
    ],
    [
        Q("TRIM berfungsi?", ["Membuang spasi di tepi", "Mengubah huruf besar", "Memotong teks", "Mengganti teks"], 0, "Spasi tepi.", hint="Tepi."),
        Q("INSTR mengembalikan nol bila?", ["Teks tidak ditemukan", "Teks kosong", "Ada spasi", "Ada NULL"], 0, "Tidak ketemu.", hint="Nol."),
        Q("'a' || NULL menghasilkan?", ["NULL", "a", "Kosong", "Error"], 0, "NULL menular.", hint="Menular."),
        Q("Fungsi untuk memotong bagian teks?", ["SUBSTR", "TRIM", "UPPER", "REPLACE"], 0, "Mulai dan panjang.", hint="Sub."),
        Q("LOWER sebelum GROUP BY berguna untuk?", ["Menyatukan variasi huruf", "Mempercepat", "Mengurutkan", "Menghapus NULL"], 0, "Normalisasi.", hint="Huruf."),
    ],
    [
        "Normalkan teks dengan LOWER dan TRIM sebelum mengelompokkan.",
        "SUBSTR dan INSTR memecah teks pada pemisah.",
        "NULL pada penggabungan perlu COALESCE.",
        "Uji kasus tepi seperti nama satu kata.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perintah yang cukup jelas dalam teks.", "brief": []}

write_module(
    "A6",
    7,
    "Fungsi tanggal dan teks",
    105,
    [
        "Mengekstrak dan mengelompokkan data berdasarkan waktu",
        "Menghitung tanggal dengan benar tanpa jebakan luapan",
        "Membersihkan dan memecah teks sebelum analisis",
    ],
    [l1, l2, l3],
    video,
    REF,
)
