import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

SQL_DB = """
CREATE TABLE penjualan (id INTEGER PRIMARY KEY, sales TEXT, wilayah TEXT, bulan INTEGER, nilai INTEGER);
INSERT INTO penjualan VALUES
(1, 'Ani', 'Barat', 1, 100),
(2, 'Ani', 'Barat', 2, 150),
(3, 'Ani', 'Barat', 3, 120),
(4, 'Budi', 'Timur', 1, 200),
(5, 'Budi', 'Timur', 2, 180),
(6, 'Budi', 'Timur', 3, 220),
(7, 'Citra', 'Barat', 1, 150),
(8, 'Citra', 'Barat', 2, 150),
(9, 'Citra', 'Barat', 3, 90);
"""

SETUP = textwrap.indent("import sqlite3\n\nc = sqlite3.connect(':memory:')\nc.executescript('''" + SQL_DB + "''')\n", '            ')

FIX = textwrap.indent("import sqlite3\n\ndef _db():\n    c = sqlite3.connect(':memory:')\n    c.executescript('''" + textwrap.indent(SQL_DB, '    ') + "    ''')\n    return c\n\n", '            ')
l1 = lesson(
    "A6-06-1",
    "Konsep window function dan PARTITION BY",
    35,
    [
        "Menjelaskan perbedaan window function dan GROUP BY",
        "Menulis klausa OVER dengan PARTITION BY",
        "Menghitung total dan persentase per kelompok tanpa menghilangkan baris",
        "Memakai window function di dalam subquery untuk menyaring hasilnya",
    ],
    [
        T("""
        ## Masalah yang tidak terjawab GROUP BY

        `GROUP BY` meringkas banyak baris menjadi satu baris per kelompok. Itu tepat untuk laporan total, tetapi sering kita butuh keduanya sekaligus: detail tiap baris dan ringkasan kelompoknya. Misalnya, tampilkan setiap penjualan beserta total penjualan salesnya, supaya kita bisa menghitung berapa persen kontribusinya.

        Dengan `GROUP BY` kita harus menjalankan dua query lalu menggabungkannya lewat JOIN atau subquery berkorelasi. **Window function** menyelesaikannya dalam satu query: ia menghitung agregat atas sekumpulan baris terkait, tetapi tetap mempertahankan setiap baris asli di hasil.
        """),
        T("""
        ## Tabel contoh

        Pada modul ini kita memakai tabel `penjualan` dengan kolom `id`, `sales`, `wilayah`, `bulan`, dan `nilai`. Ada tiga sales, yaitu Ani dan Citra di wilayah Barat serta Budi di wilayah Timur, masing-masing dengan data tiga bulan. Total seluruh nilai adalah 1360.

        Tabel kecil ini sengaja dibuat agar semua hasil dapat dihitung dengan tangan. Cobalah memeriksa beberapa angka sendiri sebelum menjalankan kode, sebab kebiasaan memverifikasi hasil query adalah keterampilan terpenting analis data.
        """),
        T("""
        ## Klausa OVER

        Sebuah fungsi menjadi window function ketika diikuti klausa `OVER (...)`. Contoh `SUM(nilai) OVER ()` menjumlahkan nilai seluruh baris, dan hasilnya dicantumkan di setiap baris. Kurung kosong berarti jendelanya adalah seluruh himpunan hasil.

        Hampir semua fungsi agregat dapat dipakai sebagai window function: `SUM`, `AVG`, `COUNT`, `MIN`, dan `MAX`. Bedanya dengan agregat biasa, tidak ada pengurangan baris. Jumlah baris keluaran sama persis dengan jumlah baris masukan.
        """),
        C(
            SETUP + """
            q = 'SELECT id, nilai, SUM(nilai) OVER () FROM penjualan ORDER BY id'
            rows = c.execute(q).fetchall()
            print(rows[:3])
            print(len(rows))
            """,
            """
            [(1, 100, 1360), (2, 150, 1360), (3, 120, 1360)]
            9
            """,
            """
            Total 1360 muncul di setiap baris sementara jumlah baris tetap sembilan.
            """,
            filename="over_kosong.py",
        ),
        T("""
        ## PARTITION BY

        `PARTITION BY` membagi baris menjadi kelompok, dan fungsi dihitung terpisah di tiap kelompok. `SUM(nilai) OVER (PARTITION BY sales)` memberikan total per sales pada setiap baris milik sales itu. Ia mirip `GROUP BY` dari sisi pembagian kelompok, tetapi tanpa meruntuhkan baris.

        Anggap partisi sebagai jendela yang bergeser: untuk tiap baris, jendelanya hanya berisi baris sekelompok. Itu sebabnya fungsi ini dinamai window function.
        """),
        C(
            SETUP + """
            q = '''
            SELECT sales, bulan, nilai, SUM(nilai) OVER (PARTITION BY sales)
            FROM penjualan ORDER BY id
            '''
            for r in c.execute(q).fetchall():
                print(r)
            """,
            """
            ('Ani', 1, 100, 370)
            ('Ani', 2, 150, 370)
            ('Ani', 3, 120, 370)
            ('Budi', 1, 200, 600)
            ('Budi', 2, 180, 600)
            ('Budi', 3, 220, 600)
            ('Citra', 1, 150, 390)
            ('Citra', 2, 150, 390)
            ('Citra', 3, 90, 390)
            """,
            """
            Setiap baris membawa total salesnya sendiri: 370 untuk Ani, 600 untuk Budi, dan 390 untuk Citra.
            """,
            filename="partition_by.py",
        ),
        T("""
        ## Persentase dari total kelompok

        Karena detail dan total berada di baris yang sama, menghitung proporsi menjadi mudah: `nilai / SUM(nilai) OVER (PARTITION BY sales)`. Kalikan dengan 100.0, bukan 100, agar pembagian bertipe desimal. Pembagian bilangan bulat di SQLite memotong pecahan, jadi `150 / 370` menjadi nol.

        Pola persen dari total ini sangat sering dipakai: kontribusi produk terhadap penjualan kategorinya, porsi tiap wilayah, atau bagian tiap bulan dari total tahunan.
        """),
        C(
            SETUP + """
            q = '''
            SELECT sales, nilai,
                   ROUND(100.0 * nilai / SUM(nilai) OVER (PARTITION BY sales), 1)
            FROM penjualan ORDER BY id
            '''
            print([r[2] for r in c.execute(q).fetchall()])
            print(c.execute('SELECT 150 / 370, 150 * 1.0 / 370').fetchone())
            """,
            """
            [27.0, 40.5, 32.4, 33.3, 30.0, 36.7, 38.5, 38.5, 23.1]
            (0, 0.40540540540540543)
            """,
            """
            Persen dihitung per sales, dan contoh terakhir mengingatkan bahwa pembagian bilangan bulat di SQLite bernilai nol.
            """,
            filename="persen_total.py",
        ),
        T("""
        ## Beda dengan GROUP BY

        Ada tiga perbedaan utama. Pertama, `GROUP BY` mengurangi baris, window function tidak. Kedua, kolom yang dipilih bersama `GROUP BY` harus kolom pengelompokan atau agregat, sedangkan window function bebas ditampilkan bersama kolom apa pun. Ketiga, window function dievaluasi setelah `WHERE`, `GROUP BY`, dan `HAVING`, tepat sebelum `ORDER BY`.

        Urutan evaluasi inilah penyebab window function tidak boleh dipakai langsung di `WHERE`. Untuk menyaring berdasarkan hasilnya, bungkus dalam subquery atau CTE.
        """),
        T("""
        ## Menyaring hasil window function

        Misalnya kita ingin baris yang nilainya di atas rata-rata wilayahnya. Rata-rata wilayah dihitung dengan `AVG(nilai) OVER (PARTITION BY wilayah)`, tetapi `WHERE nilai > AVG(...) OVER (...)` ditolak karena window belum dihitung saat `WHERE` berjalan.

        Solusinya membungkus query dalam subquery di `FROM` atau CTE, lalu menyaring di luar. Pola dua lapis ini akan kita pakai berulang untuk pemeringkatan dan perbandingan.
        """),
        C(
            SETUP + """
            q = '''
            SELECT id FROM (
                SELECT id, nilai, AVG(nilai) OVER (PARTITION BY wilayah) AS rata
                FROM penjualan
            )
            WHERE nilai > rata
            ORDER BY id
            '''
            print([r[0] for r in c.execute(q).fetchall()])
            """,
            """
            [2, 6, 7, 8]
            """,
            """
            Baris dua tujuh dan delapan di atas rata-rata wilayah Barat, dan baris enam di atas rata-rata wilayah Timur.
            """,
            filename="saring_window.py",
        ),
        T("""
        ## Beberapa window dalam satu query

        Satu query boleh memuat beberapa window function dengan partisi berbeda. Kita dapat menampilkan total per sales, total per wilayah, dan total keseluruhan berdampingan, lalu menghitung berbagai persentase sekaligus.

        Karena tiap window dihitung independen, tidak ada pengaruh antar kolom. Bila partisinya sama dan dipakai berulang, SQL menyediakan klausa `WINDOW` bernama agar definisinya tidak ditulis ulang, tetapi menuliskannya langsung sudah cukup untuk sebagian besar kebutuhan.
        """),
        K(
            "warn",
            """
            Window function tidak boleh muncul di WHERE. Bungkus query dalam subquery atau CTE lalu saring di lapisan luar.
            """,
            title="Tidak di WHERE",
        ),
        T("""
        ## Kapan memakai window function

        Gunakan window function setiap kali kebutuhan melibatkan perbandingan sebuah baris dengan kelompoknya: persen dari total, selisih dari rata-rata, atau posisi dalam kelompok. Pola-pola ini sebelumnya memerlukan JOIN ke subquery agregat yang panjang dan mudah salah.

        Dengan window function, logika yang sama menjadi satu ekspresi yang terbaca langsung di daftar kolom. Hasilnya query lebih pendek, lebih jelas, dan sering lebih cepat.
        """),
        E(
            "A6-06-1-ex1",
            "mudah",
            """
            Tulis fungsi `nilai_dan_total(c)` yang mengembalikan list tuple `(id, nilai, total)` untuk semua baris `penjualan`, terurut menurut id, dengan `total` adalah jumlah seluruh nilai memakai `SUM() OVER ()`.
            """,
            """
            import sqlite3

            def nilai_dan_total(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            r = nilai_dan_total(c)
            assert len(r) == 9
            assert r[0] == (1, 100, 1360)
            c.execute("INSERT INTO penjualan VALUES (10, 'Dedi', 'Timur', 4, 40)")
            r = nilai_dan_total(c)
            assert len(r) == 10 and r[-1] == (10, 40, 1400)
            """,
            "Pakai SUM(nilai) OVER () pada setiap baris.",
            """
            import sqlite3

            def nilai_dan_total(c):
                q = 'SELECT id, nilai, SUM(nilai) OVER () FROM penjualan ORDER BY id'
                return c.execute(q).fetchall()
            """,
        ),
        E(
            "A6-06-1-ex2",
            "sedang",
            """
            Tulis fungsi `total_per_sales(c)` yang mengembalikan list tuple `(id, total_sales)` terurut menurut id, dengan `total_sales` adalah jumlah nilai seluruh baris milik sales yang sama.
            """,
            """
            import sqlite3

            def total_per_sales(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            r = total_per_sales(c)
            assert r[0] == (1, 370)
            assert r[3] == (4, 600)
            assert r[8] == (9, 390)
            c.execute("INSERT INTO penjualan VALUES (10, 'Ani', 'Barat', 4, 30)")
            assert total_per_sales(c)[0] == (1, 400)
            """,
            "Gunakan PARTITION BY sales.",
            """
            import sqlite3

            def total_per_sales(c):
                q = 'SELECT id, SUM(nilai) OVER (PARTITION BY sales) FROM penjualan ORDER BY id'
                return c.execute(q).fetchall()
            """,
        ),
        E(
            "A6-06-1-ex3",
            "sedang",
            """
            Tulis fungsi `persen_sales(c, sales)` yang mengembalikan list persentase kontribusi tiap bulan terhadap total sales tersebut, dibulatkan 1 desimal, terurut menurut bulan. Sales tak dikenal menghasilkan list kosong.
            """,
            """
            import sqlite3

            def persen_sales(c, sales):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert persen_sales(c, 'Ani') == [27.0, 40.5, 32.4]
            assert persen_sales(c, 'Budi') == [33.3, 30.0, 36.7]
            assert persen_sales(c, 'Citra') == [38.5, 38.5, 23.1]
            assert persen_sales(c, 'Zed') == []
            """,
            "Kalikan 100.0 dan bagi dengan SUM OVER PARTITION BY sales.",
            """
            import sqlite3

            def persen_sales(c, sales):
                q = '''
                SELECT ROUND(100.0 * nilai / SUM(nilai) OVER (PARTITION BY sales), 1)
                FROM penjualan WHERE sales = ? ORDER BY bulan
                '''
                return [r[0] for r in c.execute(q, (sales,)).fetchall()]
            """,
        ),
        E(
            "A6-06-1-ex4",
            "menantang",
            """
            Tulis fungsi `di_atas_rata_wilayah(c)` yang mengembalikan list id baris dengan `nilai` lebih besar dari rata-rata `nilai` wilayahnya, terurut menurut id.
            """,
            """
            import sqlite3

            def di_atas_rata_wilayah(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert di_atas_rata_wilayah(c) == [2, 6, 7, 8]
            c.execute("INSERT INTO penjualan VALUES (10, 'Dedi', 'Timur', 4, 300)")
            assert di_atas_rata_wilayah(c) == [2, 7, 8, 10]
            c.execute('DELETE FROM penjualan WHERE id = 10')
            assert di_atas_rata_wilayah(c) == [2, 6, 7, 8]
            """,
            "Hitung AVG OVER PARTITION BY wilayah di subquery lalu saring di luar.",
            """
            import sqlite3

            def di_atas_rata_wilayah(c):
                q = '''
                SELECT id FROM (
                    SELECT id, nilai, AVG(nilai) OVER (PARTITION BY wilayah) AS rata FROM penjualan
                )
                WHERE nilai > rata ORDER BY id
                '''
                return [r[0] for r in c.execute(q).fetchall()]
            """,
        ),
    ],
    [
        M("Memakai window function di WHERE.", "Bungkus dalam subquery atau CTE lalu saring di luar."),
        M("Membagi bilangan bulat untuk persen.", "Kalikan 100.0 agar hasil desimal."),
        M("Mengira window function mengurangi baris seperti GROUP BY.", "Jumlah baris tetap sama."),
    ],
    [
        Q("Window function ditandai oleh?", ["Klausa OVER", "Klausa HAVING", "Kata WINDOW di FROM", "Tanda kurung ganda"], 0, "OVER menentukan jendela.", hint="Over."),
        Q("Dibanding GROUP BY, window function?", ["Mempertahankan semua baris", "Menghapus duplikat", "Mengurutkan", "Menggabungkan tabel"], 0, "Baris tidak berkurang.", hint="Baris."),
        Q("PARTITION BY berfungsi?", ["Membagi baris menjadi kelompok", "Mengurutkan hasil", "Membatasi jumlah baris", "Menggabungkan kolom"], 0, "Perhitungan per kelompok.", hint="Kelompok."),
        Q("Untuk menyaring hasil window function?", ["Bungkus dalam subquery", "Pakai WHERE langsung", "Pakai DISTINCT", "Pakai LIMIT"], 0, "Window dihitung setelah WHERE.", hint="Bungkus."),
        Q("OVER () dengan kurung kosong berarti?", ["Seluruh hasil satu jendela", "Tidak ada jendela", "Satu baris", "Error"], 0, "Semua baris.", hint="Semua."),
    ],
    [
        "Window function menghitung agregat tanpa menghilangkan baris.",
        "PARTITION BY membagi baris menjadi kelompok untuk tiap perhitungan.",
        "Persentase dari total mudah dihitung karena detail dan total sebaris.",
        "Saring hasil window function lewat subquery atau CTE.",
    ],
    [],
)

l2 = lesson(
    "A6-06-2",
    "Peringkat dan fungsi navigasi",
    35,
    [
        "Membedakan ROW_NUMBER, RANK, dan DENSE_RANK",
        "Mengambil baris teratas per kelompok",
        "Memakai LAG dan LEAD untuk membandingkan dengan baris sebelumnya",
        "Menghitung selisih antar periode",
    ],
    [
        T("""
        ## ORDER BY di dalam OVER

        Selain `PARTITION BY`, klausa `OVER` menerima `ORDER BY` yang mengatur urutan baris di dalam jendela. Untuk fungsi peringkat dan navigasi, urutan ini wajib karena makna peringkat atau baris sebelumnya bergantung padanya. Urutan di dalam `OVER` tidak sama dengan `ORDER BY` di ujung query, yang hanya mengatur tampilan akhir.

        Keduanya independen. Kita bisa meranking berdasarkan nilai menurun di dalam window sambil menampilkan hasil terurut menurut id. Selalu tambahkan `ORDER BY` akhir bila urutan keluaran penting.
        """),
        T("""
        ## Tiga fungsi peringkat

        `ROW_NUMBER()` memberi nomor urut unik 1, 2, 3 tanpa peduli seri. `RANK()` memberi peringkat yang sama untuk nilai seri lalu melompati nomor berikutnya, sehingga muncul 1, 2, 2, 4. `DENSE_RANK()` juga menyamakan seri tetapi tidak melompat, menghasilkan 1, 2, 2, 3.

        Pilihan tergantung makna. Untuk memilih tepat satu baris per kelompok, gunakan `ROW_NUMBER`. Untuk papan peringkat yang adil terhadap seri, gunakan `RANK` atau `DENSE_RANK`.
        """),
        C(
            SETUP + """
            q = '''
            SELECT id,
                   ROW_NUMBER() OVER (ORDER BY nilai DESC, id),
                   RANK() OVER (ORDER BY nilai DESC),
                   DENSE_RANK() OVER (ORDER BY nilai DESC)
            FROM penjualan ORDER BY id
            '''
            for r in c.execute(q).fetchall():
                print(r)
            """,
            """
            (1, 8, 8, 6)
            (2, 4, 4, 4)
            (3, 7, 7, 5)
            (4, 2, 2, 2)
            (5, 3, 3, 3)
            (6, 1, 1, 1)
            (7, 5, 4, 4)
            (8, 6, 4, 4)
            (9, 9, 9, 7)
            """,
            """
            Baris dua tujuh dan delapan sama-sama bernilai 150 sehingga RANK memberi tiga kali empat lalu melompat ke sembilan, sedangkan DENSE_RANK berhenti di tujuh.
            """,
            filename="tiga_peringkat.py",
        ),
        T("""
        ## Menangani seri secara eksplisit

        `ROW_NUMBER` selalu memberi nomor berbeda, tetapi urutan antar baris seri tidak terdefinisi kecuali kita menambahkan pembeda di `ORDER BY`. Pada contoh, `ORDER BY nilai DESC, id` membuat baris tujuh selalu lebih dulu dari delapan. Tanpa `id`, hasil bisa berubah antar eksekusi.

        Kebiasaan baik: tambahkan kolom unik sebagai pemutus seri bila Anda memakai `ROW_NUMBER`, supaya laporan bersifat deterministik dan dapat diuji.
        """),
        T("""
        ## Baris teratas per kelompok

        Salah satu penggunaan paling berharga adalah mengambil N baris teratas dari tiap kelompok, misalnya bulan terbaik tiap sales. Beri nomor dengan `ROW_NUMBER() OVER (PARTITION BY sales ORDER BY nilai DESC, bulan)`, lalu di lapisan luar saring `rn = 1`.

        Ini hampir mustahil dilakukan rapi dengan `GROUP BY` saja, karena kolom pendamping seperti bulan tidak ikut agregat. Pola ini begitu umum sehingga layak dihafal.
        """),
        C(
            SETUP + """
            q = '''
            SELECT sales, bulan FROM (
                SELECT sales, bulan,
                       ROW_NUMBER() OVER (PARTITION BY sales ORDER BY nilai DESC, bulan) AS rn
                FROM penjualan
            )
            WHERE rn = 1 ORDER BY sales
            '''
            print(c.execute(q).fetchall())
            """,
            """
            [('Ani', 2), ('Budi', 3), ('Citra', 1)]
            """,
            """
            Bulan terbaik Ani adalah dua dan Budi tiga, sedangkan Citra seri di bulan satu dan dua sehingga bulan lebih awal yang dipilih.
            """,
            filename="top_per_kelompok.py",
        ),
        T("""
        ## LAG dan LEAD

        `LAG(kolom, n, default)` mengambil nilai dari n baris sebelumnya dalam jendela, dan `LEAD` dari n baris sesudahnya. Argumen n bawaannya satu, dan default dipakai ketika baris tidak ada, yang bila dihilangkan menghasilkan `NULL`.

        Keduanya membutuhkan `ORDER BY` di dalam `OVER` agar jelas mana yang sebelum dan sesudah. Bersama `PARTITION BY`, baris pertama tiap kelompok tidak punya pendahulu sehingga mendapat default.
        """),
        C(
            SETUP + """
            q = '''
            SELECT id, nilai, LAG(nilai) OVER (PARTITION BY sales ORDER BY bulan)
            FROM penjualan ORDER BY id
            '''
            print([r[2] for r in c.execute(q).fetchall()])
            q = '''
            SELECT id, LEAD(nilai) OVER (PARTITION BY sales ORDER BY bulan)
            FROM penjualan ORDER BY id
            '''
            print([r[1] for r in c.execute(q).fetchall()])
            """,
            """
            [None, 100, 150, None, 200, 180, None, 150, 150]
            [150, 120, None, 180, 220, None, 150, 90, None]
            """,
            """
            Bulan pertama tiap sales tidak punya bulan sebelumnya sehingga LAG bernilai NULL, dan bulan terakhir tidak punya LEAD.
            """,
            filename="lag_lead.py",
        ),
        T("""
        ## Selisih antar periode

        Pertumbuhan dihitung sebagai nilai sekarang dikurangi nilai periode sebelumnya, yang tepat dengan `nilai - LAG(nilai) OVER (...)`. Untuk baris pertama LAG bernilai `NULL` sehingga selisihnya `NULL`. Beri default sama dengan nilai itu sendiri, `LAG(nilai, 1, nilai)`, bila ingin selisih nol di awal.

        Pilih perlakuan awal dengan sadar. `NULL` menyatakan tidak ada pembanding, sedangkan nol menyatakan tidak ada perubahan. Dua makna itu berbeda dalam laporan.
        """),
        C(
            SETUP + """
            q = '''
            SELECT id, nilai - LAG(nilai, 1, nilai) OVER (PARTITION BY sales ORDER BY bulan)
            FROM penjualan ORDER BY id
            '''
            print([r[1] for r in c.execute(q).fetchall()])
            """,
            """
            [0, 50, -30, 0, -20, 40, 0, 0, -60]
            """,
            """
            Selisih bulanan tiap sales dengan nol pada bulan pertama sebagai nilai awal.
            """,
            filename="selisih_periode.py",
        ),
        T("""
        ## Persen pertumbuhan

        Dari selisih mudah diturunkan persen pertumbuhan: selisih dibagi nilai sebelumnya. Waspadai pembagian oleh nol dan nilai `NULL`. Bungkus penyebut dengan `NULLIF(x, 0)` agar pembagian dengan nol menghasilkan `NULL` alih-alih galat.

        Pertumbuhan bulan ke bulan dan tahun ke tahun adalah metrik standar dalam laporan bisnis, dan `LAG` dengan offset 12 untuk data bulanan memberikan perbandingan tahun ke tahun.
        """),
        K(
            "tip",
            """
            Tambahkan kolom unik sebagai pemutus seri pada ORDER BY di dalam OVER agar hasil ROW_NUMBER deterministik.
            """,
            title="Pemutus seri",
        ),
        T("""
        ## Papan peringkat yang adil

        Dalam kompetisi, nilai seri harus diperlakukan adil. Dua pemain dengan skor sama pantas menempati peringkat yang sama. `RANK` dan `DENSE_RANK` melakukannya, sedangkan `ROW_NUMBER` memaksa salah satu menjadi lebih tinggi tanpa dasar yang jelas.

        Karena itu, pilih fungsi berdasarkan makna bisnisnya. Bila yang dibutuhkan satu wakil per kelompok, gunakan `ROW_NUMBER`. Bila yang dibutuhkan urutan yang adil terhadap seri, gunakan dua fungsi lainnya dan jelaskan perbedaannya kepada pembaca laporan.
        """),
        T("""
        ## Offset dan nilai default pada LAG

        `LAG` menerima offset yang lebih besar dari satu. `LAG(nilai, 3)` mengambil nilai tiga baris sebelumnya, sehingga pada data bulanan `LAG(nilai, 12)` membandingkan dengan bulan yang sama tahun lalu. Nilai default sebagai argumen ketiga mengisi baris yang tidak punya pendahulu.

        Periksa selalu baris awal tiap kelompok pada hasil perbandingan. Di sanalah kesalahan paling sering bersembunyi, karena nilai `NULL` atau default mengubah rata-rata dan jumlah yang dihitung kemudian.
        """),
        E(
            "A6-06-2-ex1",
            "mudah",
            """
            Tulis fungsi `peringkat_global(c)` yang mengembalikan dict `{id: peringkat}` memakai `RANK()` dengan urutan `nilai` menurun di seluruh tabel.
            """,
            """
            import sqlite3

            def peringkat_global(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            d = peringkat_global(c)
            assert d[6] == 1
            assert d[7] == 4 and d[8] == 4
            assert d[9] == 9
            """,
            "RANK() OVER (ORDER BY nilai DESC).",
            """
            import sqlite3

            def peringkat_global(c):
                q = 'SELECT id, RANK() OVER (ORDER BY nilai DESC) FROM penjualan'
                return dict(c.execute(q).fetchall())
            """,
        ),
        E(
            "A6-06-2-ex2",
            "sedang",
            """
            Tulis fungsi `peringkat_padat(c)` yang mengembalikan dict `{id: peringkat}` memakai `DENSE_RANK()` dengan urutan `nilai` menurun di seluruh tabel.
            """,
            """
            import sqlite3

            def peringkat_padat(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            d = peringkat_padat(c)
            assert d[1] == 6
            assert d[9] == 7
            assert d[7] == 4 and d[8] == 4
            """,
            "DENSE_RANK tidak melompat setelah seri.",
            """
            import sqlite3

            def peringkat_padat(c):
                q = 'SELECT id, DENSE_RANK() OVER (ORDER BY nilai DESC) FROM penjualan'
                return dict(c.execute(q).fetchall())
            """,
        ),
        E(
            "A6-06-2-ex3",
            "sedang",
            """
            Tulis fungsi `bulan_terbaik(c)` yang mengembalikan list tuple `(sales, bulan)` berisi bulan dengan `nilai` tertinggi tiap sales, terurut menurut sales. Bila seri, pilih bulan lebih awal.
            """,
            """
            import sqlite3

            def bulan_terbaik(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert bulan_terbaik(c) == [('Ani', 2), ('Budi', 3), ('Citra', 1)]
            c.execute("INSERT INTO penjualan VALUES (10, 'Ani', 'Barat', 4, 500)")
            assert bulan_terbaik(c)[0] == ('Ani', 4)
            c.execute("INSERT INTO penjualan VALUES (11, 'Budi', 'Timur', 4, 220)")
            assert bulan_terbaik(c)[1] == ('Budi', 3)
            """,
            "ROW_NUMBER dengan PARTITION BY sales lalu saring nomor satu.",
            """
            import sqlite3

            def bulan_terbaik(c):
                q = '''
                SELECT sales, bulan FROM (
                    SELECT sales, bulan,
                           ROW_NUMBER() OVER (PARTITION BY sales ORDER BY nilai DESC, bulan) AS rn
                    FROM penjualan
                )
                WHERE rn = 1 ORDER BY sales
                '''
                return c.execute(q).fetchall()
            """,
        ),
        E(
            "A6-06-2-ex4",
            "menantang",
            """
            Tulis fungsi `selisih_bulanan(c)` yang mengembalikan list tuple `(id, selisih)` terurut menurut id, dengan `selisih` adalah `nilai` dikurangi `nilai` bulan sebelumnya milik sales yang sama, dan nol pada bulan pertama.
            """,
            """
            import sqlite3

            def selisih_bulanan(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert selisih_bulanan(c) == [(1, 0), (2, 50), (3, -30), (4, 0), (5, -20), (6, 40), (7, 0), (8, 0), (9, -60)]
            c.execute("INSERT INTO penjualan VALUES (10, 'Ani', 'Barat', 4, 200)")
            assert selisih_bulanan(c)[-1] == (10, 80)
            c.execute("INSERT INTO penjualan VALUES (11, 'Dedi', 'Timur', 1, 70)")
            assert selisih_bulanan(c)[-1] == (11, 0)
            """,
            "LAG dengan default nilai itu sendiri dan PARTITION BY sales ORDER BY bulan.",
            """
            import sqlite3

            def selisih_bulanan(c):
                q = '''
                SELECT id, nilai - LAG(nilai, 1, nilai) OVER (PARTITION BY sales ORDER BY bulan)
                FROM penjualan ORDER BY id
                '''
                return c.execute(q).fetchall()
            """,
        ),
    ],
    [
        M("Memakai ROW_NUMBER tanpa pemutus seri.", "Tambahkan kolom unik di ORDER BY."),
        M("Mengira RANK tidak melompat.", "RANK melompat setelah seri, DENSE_RANK tidak."),
        M("Lupa ORDER BY di dalam OVER untuk LAG.", "LAG dan LEAD membutuhkan urutan."),
    ],
    [
        Q("Fungsi yang memberi nomor unik tanpa seri?", ["ROW_NUMBER", "RANK", "DENSE_RANK", "NTILE"], 0, "Selalu berbeda.", hint="Row."),
        Q("RANK untuk nilai 10, 8, 8, 5 menghasilkan?", ["1, 2, 2, 4", "1, 2, 2, 3", "1, 2, 3, 4", "1, 1, 2, 3"], 0, "Melompat setelah seri.", hint="Lompat."),
        Q("DENSE_RANK untuk nilai 10, 8, 8, 5 menghasilkan?", ["1, 2, 2, 3", "1, 2, 2, 4", "1, 2, 3, 4", "1, 1, 1, 1"], 0, "Tidak melompat.", hint="Padat."),
        Q("LAG mengambil nilai dari?", ["Baris sebelumnya", "Baris sesudahnya", "Baris pertama", "Baris terakhir"], 0, "Sebelum.", hint="Sebelum."),
        Q("Baris pertama kelompok pada LAG tanpa default bernilai?", ["NULL", "0", "Sama dengan nilai", "Error"], 0, "Tidak ada pendahulu.", hint="Kosong."),
    ],
    [
        "ROW_NUMBER, RANK, dan DENSE_RANK berbeda dalam menangani seri.",
        "Top N per kelompok memakai ROW_NUMBER lalu saring di lapisan luar.",
        "LAG dan LEAD membandingkan baris dengan tetangganya.",
        "Tentukan perlakuan baris pertama dengan nilai default.",
    ],
    [],
)

l3 = lesson(
    "A6-06-3",
    "Frame, total berjalan, dan NTILE",
    35,
    [
        "Menjelaskan frame ROWS BETWEEN",
        "Menghitung total berjalan dan rata-rata bergerak",
        "Membagi data menjadi kelompok sama besar dengan NTILE",
        "Memakai FIRST_VALUE dan menghindari jebakan seri pada frame bawaan",
    ],
    [
        T("""
        ## Frame jendela

        Di dalam partisi, **frame** menentukan baris mana yang ikut dihitung untuk baris saat ini. Ia ditulis setelah `ORDER BY` di dalam `OVER`, misalnya `ROWS BETWEEN 1 PRECEDING AND CURRENT ROW` yang berarti baris sebelumnya dan baris saat ini.

        Penanda batasnya adalah `UNBOUNDED PRECEDING` untuk awal partisi, `n PRECEDING`, `CURRENT ROW`, `n FOLLOWING`, dan `UNBOUNDED FOLLOWING` untuk akhir partisi. Dengan kombinasi ini kita dapat menyusun jendela geser sesuai kebutuhan analisis.
        """),
        T("""
        ## Frame bawaan saat ada ORDER BY

        Bila `ORDER BY` ada di dalam `OVER` dan frame tidak ditulis, bawaannya adalah dari awal partisi sampai baris saat ini. Itulah sebabnya `SUM(nilai) OVER (PARTITION BY sales ORDER BY bulan)` menghasilkan total berjalan, bukan total seluruh partisi.

        Tanpa `ORDER BY`, frame mencakup seluruh partisi, sehingga `SUM(...) OVER (PARTITION BY sales)` memberi total kelompok. Dua perilaku bawaan ini sering membingungkan pemula, jadi hafalkan.
        """),
        C(
            SETUP + """
            q = '''
            SELECT id, SUM(nilai) OVER (PARTITION BY sales ORDER BY bulan)
            FROM penjualan ORDER BY id
            '''
            print([r[1] for r in c.execute(q).fetchall()])
            q = '''
            SELECT id, SUM(nilai) OVER (ORDER BY id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
            FROM penjualan ORDER BY id
            '''
            print([r[1] for r in c.execute(q).fetchall()])
            """,
            """
            [100, 250, 370, 200, 380, 600, 150, 300, 390]
            [100, 250, 370, 570, 750, 970, 1120, 1270, 1360]
            """,
            """
            Total berjalan per sales di baris pertama, dan total berjalan seluruh tabel di baris kedua yang berakhir pada 1360.
            """,
            filename="total_berjalan.py",
        ),
        T("""
        ## Rata-rata bergerak

        Rata-rata bergerak menghaluskan fluktuasi dengan merata-ratakan beberapa periode terakhir. Untuk dua bulan terakhir, pakai `AVG(nilai) OVER (PARTITION BY sales ORDER BY bulan ROWS BETWEEN 1 PRECEDING AND CURRENT ROW)`. Di awal partisi hanya ada satu baris sehingga rata-ratanya dari baris itu saja.

        Ukuran jendela menentukan kehalusan. Jendela kecil mengikuti data erat, jendela besar lebih halus tetapi tertinggal terhadap perubahan terbaru.
        """),
        C(
            SETUP + """
            q = '''
            SELECT id, AVG(nilai) OVER (
                PARTITION BY sales ORDER BY bulan
                ROWS BETWEEN 1 PRECEDING AND CURRENT ROW
            )
            FROM penjualan ORDER BY id
            '''
            print([r[1] for r in c.execute(q).fetchall()])
            """,
            """
            [100.0, 125.0, 135.0, 200.0, 190.0, 200.0, 150.0, 150.0, 120.0]
            """,
            """
            Bulan pertama memakai dirinya sendiri, sedangkan bulan berikutnya merata-ratakan bulan itu dengan bulan sebelumnya.
            """,
            filename="rata_bergerak.py",
        ),
        T("""
        ## ROWS dan RANGE

        `ROWS` menghitung berdasarkan posisi baris fisik, sedangkan `RANGE` berdasarkan nilai kolom pengurut sehingga baris seri dianggap satu kesatuan. Frame bawaan saat ada `ORDER BY` sebenarnya `RANGE`, bukan `ROWS`.

        Akibatnya, bila ada nilai seri pada kolom pengurut, baris-baris seri itu mendapat total berjalan yang sama. Untuk total berjalan yang benar-benar baris demi baris, tulis `ROWS` secara eksplisit dan tambahkan pembeda unik di `ORDER BY`.
        """),
        C(
            SETUP + """
            q = '''
            SELECT id, SUM(nilai) OVER (ORDER BY nilai)
            FROM penjualan WHERE sales = 'Citra' ORDER BY id
            '''
            print(c.execute(q).fetchall())
            """,
            """
            [(7, 390), (8, 390), (9, 90)]
            """,
            """
            Dua baris seri bernilai 150 sama-sama mendapat 390 karena RANGE menggabungkan baris seri.
            """,
            filename="range_seri.py",
        ),
        T("""
        ## NTILE

        `NTILE(n)` membagi baris terurut menjadi n kelompok sama besar dan memberi nomor kelompok 1 sampai n. Untuk sembilan baris dan `NTILE(3)`, tiap kelompok berisi tiga baris. Bila tidak habis dibagi, kelompok awal mendapat satu baris lebih banyak.

        Kegunaannya untuk membuat kuartil, desil, atau segmen pelanggan seperti kelompok tinggi, sedang, dan rendah. Tambahkan pembeda unik di `ORDER BY` agar penugasan kelompok stabil.
        """),
        C(
            SETUP + """
            q = '''
            SELECT id, NTILE(3) OVER (ORDER BY nilai, id)
            FROM penjualan ORDER BY id
            '''
            print([r[1] for r in c.execute(q).fetchall()])
            """,
            """
            [1, 2, 1, 3, 3, 3, 2, 2, 1]
            """,
            """
            Tiga baris bernilai terendah masuk kelompok satu, tiga tertinggi masuk kelompok tiga.
            """,
            filename="ntile.py",
        ),
        T("""
        ## FIRST_VALUE dan LAST_VALUE

        `FIRST_VALUE(kolom)` mengambil nilai baris pertama frame, berguna sebagai pembanding awal: seberapa jauh nilai sekarang dari bulan pertama. Pada frame bawaan hasilnya baris pertama partisi sesuai urutan.

        `LAST_VALUE` lebih licin. Frame bawaan berakhir di baris saat ini, sehingga `LAST_VALUE` mengembalikan nilai baris itu sendiri. Untuk mendapatkan nilai terakhir partisi, tulis frame `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`.
        """),
        C(
            SETUP + """
            q = '''
            SELECT id, nilai - FIRST_VALUE(nilai) OVER (PARTITION BY sales ORDER BY bulan)
            FROM penjualan ORDER BY id
            '''
            print([r[1] for r in c.execute(q).fetchall()])
            """,
            """
            [0, 50, 20, 0, -20, 20, 0, 0, -60]
            """,
            """
            Selisih setiap bulan terhadap bulan pertama sales yang sama.
            """,
            filename="first_value.py",
        ),
        T("""
        ## Memilih alat yang tepat

        Untuk ringkasan per kelompok yang meruntuhkan baris, pakai `GROUP BY`. Untuk detail bersama ringkasan, pakai window function. Untuk peringkat dan top N, pakai `ROW_NUMBER`, `RANK`, atau `DENSE_RANK`. Untuk perbandingan antar periode, pakai `LAG` dan `LEAD`. Untuk kumulatif dan rata-rata bergerak, pakai frame.

        Window function mengganti banyak subquery berkorelasi yang lambat dan sulit dibaca. Menguasainya adalah lompatan besar dari SQL dasar menuju analisis yang sesungguhnya.
        """),
        K(
            "tip",
            """
            Tulis frame ROWS secara eksplisit untuk total berjalan agar tidak terkena perilaku RANGE pada baris seri.
            """,
            title="Frame eksplisit",
        ),
        T("""
        ## Memeriksa frame dengan data kecil

        Frame mudah disalahpahami, jadi biasakan mengujinya pada data kecil yang hasilnya bisa dihitung dengan tangan. Jalankan query pada tiga atau empat baris, tuliskan perkiraan jawaban di kertas, lalu bandingkan dengan keluaran. Bila berbeda, hampir pasti ada salah paham tentang batas frame atau tentang seri.

        Setelah yakin, barulah terapkan pada data besar. Kebiasaan ini mencegah laporan keuangan yang tampak benar tetapi diam-diam menjumlahkan baris yang salah.
        """),
        T("""
        ## Kinerja window function

        Window function umumnya efisien karena data diurutkan sekali per partisi. Indeks pada kolom partisi dan pengurut dapat mempercepat langkah pengurutan itu. Hindari mendefinisikan banyak window dengan urutan berbeda pada tabel raksasa, sebab tiap urutan berbeda memerlukan pengurutan tersendiri.

        Bila beberapa kolom memakai partisi dan urutan yang sama, mesin basis data dapat berbagi satu pengurutan. Menyamakan definisi window antar kolom adalah optimasi sederhana yang sering berarti.
        """),
        E(
            "A6-06-3-ex1",
            "mudah",
            """
            Tulis fungsi `kumulatif_sales(c, sales)` yang mengembalikan list total berjalan `nilai` per bulan untuk sales tersebut, terurut menurut bulan. Sales tak dikenal menghasilkan list kosong.
            """,
            """
            import sqlite3

            def kumulatif_sales(c, sales):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert kumulatif_sales(c, 'Ani') == [100, 250, 370]
            assert kumulatif_sales(c, 'Budi') == [200, 380, 600]
            assert kumulatif_sales(c, 'Citra') == [150, 300, 390]
            assert kumulatif_sales(c, 'Zed') == []
            """,
            "SUM OVER dengan PARTITION BY sales ORDER BY bulan.",
            """
            import sqlite3

            def kumulatif_sales(c, sales):
                q = '''
                SELECT SUM(nilai) OVER (
                    ORDER BY bulan ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                )
                FROM penjualan WHERE sales = ? ORDER BY bulan
                '''
                return [r[0] for r in c.execute(q, (sales,)).fetchall()]
            """,
        ),
        E(
            "A6-06-3-ex2",
            "sedang",
            """
            Tulis fungsi `rata_bergerak(c, sales)` yang mengembalikan list rata-rata bergerak dua bulan (bulan ini dan sebelumnya) `nilai` untuk sales tersebut, terurut menurut bulan.
            """,
            """
            import sqlite3

            def rata_bergerak(c, sales):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert rata_bergerak(c, 'Ani') == [100.0, 125.0, 135.0]
            assert rata_bergerak(c, 'Budi') == [200.0, 190.0, 200.0]
            assert rata_bergerak(c, 'Citra') == [150.0, 150.0, 120.0]
            """,
            "AVG dengan ROWS BETWEEN 1 PRECEDING AND CURRENT ROW.",
            """
            import sqlite3

            def rata_bergerak(c, sales):
                q = '''
                SELECT AVG(nilai) OVER (
                    ORDER BY bulan ROWS BETWEEN 1 PRECEDING AND CURRENT ROW
                )
                FROM penjualan WHERE sales = ? ORDER BY bulan
                '''
                return [r[0] for r in c.execute(q, (sales,)).fetchall()]
            """,
        ),
        E(
            "A6-06-3-ex3",
            "sedang",
            """
            Tulis fungsi `kelompok_tiga(c)` yang mengembalikan list kelompok `NTILE(3)` untuk setiap baris, terurut menurut id, dengan baris diurutkan menurut `nilai` naik lalu `id` naik.
            """,
            """
            import sqlite3

            def kelompok_tiga(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert kelompok_tiga(c) == [1, 2, 1, 3, 3, 3, 2, 2, 1]
            c.execute('DELETE FROM penjualan WHERE id = 9')
            assert kelompok_tiga(c)[-1] == 2
            assert len(kelompok_tiga(c)) == 8
            """,
            "NTILE(3) OVER (ORDER BY nilai, id).",
            """
            import sqlite3

            def kelompok_tiga(c):
                q = 'SELECT NTILE(3) OVER (ORDER BY nilai, id) FROM penjualan ORDER BY id'
                return [r[0] for r in c.execute(q).fetchall()]
            """,
        ),
        E(
            "A6-06-3-ex4",
            "menantang",
            """
            Tulis fungsi `selisih_dari_awal(c)` yang mengembalikan list selisih `nilai` terhadap `nilai` bulan pertama sales yang sama untuk setiap baris, terurut menurut id.
            """,
            """
            import sqlite3

            def selisih_dari_awal(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert selisih_dari_awal(c) == [0, 50, 20, 0, -20, 20, 0, 0, -60]
            c.execute("INSERT INTO penjualan VALUES (10, 'Ani', 'Barat', 4, 130)")
            assert selisih_dari_awal(c)[-1] == 30
            c.execute("INSERT INTO penjualan VALUES (11, 'Dedi', 'Timur', 1, 70)")
            assert selisih_dari_awal(c)[-1] == 0
            """,
            "FIRST_VALUE dengan PARTITION BY sales ORDER BY bulan.",
            """
            import sqlite3

            def selisih_dari_awal(c):
                q = '''
                SELECT nilai - FIRST_VALUE(nilai) OVER (PARTITION BY sales ORDER BY bulan)
                FROM penjualan ORDER BY id
                '''
                return [r[0] for r in c.execute(q).fetchall()]
            """,
        ),
    ],
    [
        M("Mengira SUM OVER dengan ORDER BY menjumlahkan seluruh partisi.", "Ia menjadi total berjalan."),
        M("Memakai LAST_VALUE tanpa frame penuh.", "Tulis ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING."),
        M("Mengabaikan seri pada frame RANGE bawaan.", "Pakai ROWS dan pembeda unik."),
    ],
    [
        Q("Frame bawaan dengan ORDER BY?", ["Awal partisi sampai baris saat ini", "Seluruh partisi", "Hanya baris saat ini", "Satu baris sebelum"], 0, "Menjadi total berjalan.", hint="Berjalan."),
        Q("ROWS BETWEEN 1 PRECEDING AND CURRENT ROW mencakup?", ["Dua baris", "Satu baris", "Tiga baris", "Seluruh partisi"], 0, "Sebelumnya dan sekarang.", hint="Dua."),
        Q("NTILE(4) membagi menjadi?", ["Empat kelompok sama besar", "Empat baris", "Empat kolom", "Empat tabel"], 0, "Kuartil.", hint="Empat."),
        Q("RANGE memperlakukan baris seri sebagai?", ["Satu kesatuan", "Terpisah", "Dibuang", "Error"], 0, "Total sama.", hint="Seri."),
        Q("FIRST_VALUE berguna untuk?", ["Membandingkan dengan nilai awal", "Mengurutkan", "Menghapus baris", "Menggabungkan"], 0, "Pembanding awal.", hint="Awal."),
    ],
    [
        "Frame menentukan baris yang ikut dihitung di dalam partisi.",
        "Dengan ORDER BY, SUM OVER menjadi total berjalan.",
        "ROWS lebih dapat diprediksi daripada RANGE bila ada seri.",
        "NTILE membagi data menjadi kelompok sama besar.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perintah yang cukup jelas dalam teks.", "brief": []}

write_module(
    "A6",
    6,
    "Window function",
    105,
    [
        "Menghitung agregat per kelompok tanpa menghilangkan baris",
        "Membuat peringkat dan membandingkan antar periode",
        "Menghitung total berjalan, rata-rata bergerak, dan kelompok NTILE",
    ],
    [l1, l2, l3],
    video,
    REF,
)
