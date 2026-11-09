import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

SETUP = textwrap.indent("""
import sqlite3

c = sqlite3.connect(':memory:')
c.executescript('''
CREATE TABLE produk (id INTEGER PRIMARY KEY, nama TEXT, kategori TEXT, harga REAL, stok INTEGER);
INSERT INTO produk VALUES
(1, 'Pensil', 'alat tulis', 2500, 100),
(2, 'Buku', 'alat tulis', 12000, 40),
(3, 'Tas', 'perlengkapan', 150000, 8),
(4, 'Botol', 'perlengkapan', 35000, NULL),
(5, 'Penggaris', 'alat tulis', 4000, 60);
''')
""", '            ')

FIX = textwrap.indent("""
import sqlite3

def _db():
    c = sqlite3.connect(':memory:')
    c.executescript('''
    CREATE TABLE produk (id INTEGER PRIMARY KEY, nama TEXT, kategori TEXT, harga REAL, stok INTEGER);
    INSERT INTO produk VALUES
    (1, 'Pensil', 'alat tulis', 2500, 100),
    (2, 'Buku', 'alat tulis', 12000, 40),
    (3, 'Tas', 'perlengkapan', 150000, 8),
    (4, 'Botol', 'perlengkapan', 35000, NULL),
    (5, 'Penggaris', 'alat tulis', 4000, 60);
    ''')
    return c

""", '            ')

l1 = lesson(
    "A6-01-1",
    "Tabel, baris, kolom, dan tipe data",
    35,
    [
        "Menjelaskan model relasional: tabel, baris, kolom, dan kunci primer",
        "Membuat tabel dan mengisinya dengan sqlite3",
        "Membaca struktur tabel dan tipe nilai",
        "Menghitung banyak baris tabel",
    ],
    [
        T("""
        ## Mengapa SQL

        Hampir semua data bisnis hidup di basis data relasional: transaksi, pelanggan, log, dan inventaris. **SQL**, Structured Query Language, adalah bahasa standar untuk bertanya kepada basis data itu. Seorang analis data yang fasih SQL dapat mengambil dan meringkas jutaan baris langsung di sumbernya tanpa memindahkan datanya.

        Di kursus ini kita memakai SQLite, basis data kecil yang berjalan langsung di dalam Python lewat modul `sqlite3`. Sintaks dasarnya sama dengan PostgreSQL, MySQL, dan basis data lain, sehingga keterampilan yang dipelajari di sini dapat dipindahkan.
        """),
        T("""
        ## Model relasional

        Dalam model **relasional**, data disimpan dalam **tabel**. Tiap tabel mewakili satu jenis entitas, misalnya produk. Tiap **baris** mewakili satu entitas, yaitu satu produk, dan tiap **kolom** mewakili satu atribut, seperti nama atau harga. Tabel mirip DataFrame pandas, tetapi disimpan dan dikelola oleh mesin basis data.

        Sebuah tabel yang baik memiliki **kunci primer**, kolom yang nilainya unik untuk tiap baris dan mengidentifikasinya, biasanya `id`. Kunci primer memungkinkan baris dirujuk dari tabel lain, dasar dari JOIN yang dibahas pada modul berikutnya.
        """),
        T("""
        ## Membuat tabel dan mengisinya

        Pernyataan `CREATE TABLE` mendefinisikan nama tabel, kolom, dan tipe tiap kolom. Pernyataan `INSERT INTO ... VALUES` menambahkan baris. Tipe dasar SQLite adalah `INTEGER` untuk bilangan bulat, `REAL` untuk pecahan, `TEXT` untuk teks, dan `BLOB` untuk data biner. Nilai kosong ditulis `NULL`.

        Kita memakai tabel produk lima baris untuk seluruh modul ini. Satu baris sengaja memiliki stok `NULL` untuk mempelajari perilaku nilai kosong, topik yang sering menjebak pemula.
        """),
        C(
            SETUP + """
            print(c.execute('SELECT COUNT(*) FROM produk').fetchone())
            """,
            """
            (5,)
            """,
            """
            Tabel produk berisi lima baris, dan COUNT bintang mengembalikan satu baris hasil berisi angka lima.
            """,
            filename="buat_tabel.py",
        ),
        T("""
        ## Mengambil semua data

        Pernyataan paling dasar adalah `SELECT * FROM produk`. Tanda bintang berarti semua kolom, dan `FROM` menyebut tabel sumber. Metode `fetchall` mengembalikan hasilnya sebagai list tuple, satu tuple per baris. Urutan baris pada tabel tanpa `ORDER BY` tidak dijamin, jadi jangan mengandalkannya.

        Pada tabel besar, `SELECT *` boros karena membaca semua kolom. Praktik baik adalah memilih kolom yang dibutuhkan saja, yang dibahas pada pelajaran berikutnya.
        """),
        C(
            SETUP + """
            for baris in c.execute('SELECT * FROM produk ORDER BY id'):
                print(baris)
            """,
            """
            (1, 'Pensil', 'alat tulis', 2500.0, 100)
            (2, 'Buku', 'alat tulis', 12000.0, 40)
            (3, 'Tas', 'perlengkapan', 150000.0, 8)
            (4, 'Botol', 'perlengkapan', 35000.0, None)
            (5, 'Penggaris', 'alat tulis', 4000.0, 60)
            """,
            """
            Setiap baris menjadi tuple Python, dan NULL pada stok Botol muncul sebagai None.
            """,
            filename="select_semua.py",
        ),
        T("""
        ## Struktur tabel

        Kita dapat melihat struktur tabel dengan `PRAGMA table_info`, yang mengembalikan nama, tipe, dan apakah kolom itu kunci primer. Di basis data lain perintah setara adalah `DESCRIBE` atau tabel sistem `information_schema`. Memeriksa struktur adalah langkah pertama saat bertemu basis data baru.

        Tabel sistem `sqlite_master` menyimpan definisi semua tabel, termasuk teks `CREATE TABLE` aslinya. Dari sana kita dapat menemukan tabel apa saja yang ada dan bagaimana tiap tabel didefinisikan.
        """),
        C(
            SETUP + """
            info = c.execute('PRAGMA table_info(produk)').fetchall()
            print([kolom[1] for kolom in info])
            print([kolom[2] for kolom in info])
            """,
            """
            ['id', 'nama', 'kategori', 'harga', 'stok']
            ['INTEGER', 'TEXT', 'TEXT', 'REAL', 'INTEGER']
            """,
            """
            Struktur tabel memperlihatkan lima kolom beserta tipe deklarasinya.
            """,
            filename="struktur_tabel.py",
        ),
        T("""
        ## Tipe dinamis SQLite

        SQLite berbeda dari kebanyakan basis data karena tipenya dinamis: tipe melekat pada nilai, bukan hanya pada kolom. Fungsi `typeof` mengembalikan tipe nilai sebenarnya: `integer`, `real`, `text`, `blob`, atau `null`. Kolom bertipe `REAL` yang diisi angka bulat 2500 menyimpannya sebagai `real` karena afinitas kolom.

        Basis data lain seperti PostgreSQL bersifat statis dan akan menolak nilai bertipe salah. Di mana pun, memeriksa tipe nyata lewat `typeof` atau `CAST` membantu mendiagnosis hasil perhitungan yang aneh.
        """),
        C(
            SETUP + """
            print(c.execute('SELECT typeof(harga), typeof(stok), typeof(nama) FROM produk WHERE id = 4').fetchone())
            print(c.execute('SELECT typeof(stok) FROM produk WHERE id = 1').fetchone())
            """,
            """
            ('real', 'null', 'text')
            ('integer',)
            """,
            """
            Stok Botol bertipe null, sedangkan stok Pensil bertipe integer.
            """,
            filename="typeof.py",
        ),
        T("""
        ## Menghitung baris

        Fungsi agregat `COUNT(*)` menghitung banyak baris. Karena ia mengembalikan satu baris satu kolom, kita mengambilnya dengan `fetchone` dan indeks nol. Jumlah baris adalah pemeriksaan kewarasan yang selalu kamu lakukan: apakah tabel berisi sebanyak yang kamu harapkan setelah impor atau gabungan.

        Agregasi lebih lanjut dibahas pada pelajaran tersendiri. Untuk sekarang, ingat bahwa `COUNT(*)` menghitung semua baris, termasuk yang berisi `NULL`, perilaku yang akan kita bandingkan dengan `COUNT(kolom)`.
        """),
        K(
            "tip",
            """
            Setelah membuka basis data baru, jalankan PRAGMA table_info dan COUNT bintang untuk setiap tabel utama sebelum menulis query rumit.
            """,
            title="Kenali dulu datanya",
        ),
        T("""
        ## Parameter alih-alih penempelan string

        Saat memasukkan nilai dari luar ke query, jangan menempelkannya ke string dengan format. Pakai tanda tanya sebagai tempat nilai dan berikan nilainya sebagai tuple terpisah: `execute('SELECT * FROM produk WHERE id = ?', (4,))`. Mesin basis data memperlakukan nilai itu murni sebagai data, bukan kode.

        Kebiasaan ini mencegah serangan injeksi SQL, salah satu celah keamanan paling umum di dunia. Nama tabel dan kolom tidak bisa diparameterkan, jadi pada kasus itu validasi nama terhadap daftar yang diizinkan.
        """),
        T("""
        ## SQLite dan basis data lain

        SQLite menyimpan seluruh basis data dalam satu berkas, sehingga ideal untuk belajar, prototipe, dan aplikasi lokal. PostgreSQL, MySQL, dan SQL Server berjalan sebagai server yang melayani banyak pengguna bersamaan dengan fitur keamanan dan skala lebih besar.

        Bahasa SQL inti sama di semua, tetapi dialeknya berbeda pada fungsi tanggal, tipe data, dan beberapa sintaks. Kita akan menandai perbedaan penting saat muncul, dan menulis SQL standar sejauh mungkin supaya mudah dipindahkan.
        """),
        E(
            "A6-01-1-ex1",
            "mudah",
            """
            Tulis fungsi `jumlah_baris(c, tabel)` yang menerima koneksi sqlite3 dan nama tabel, lalu mengembalikan banyak baris tabel sebagai bilangan bulat.
            """,
            """
            import sqlite3

            def jumlah_baris(c, tabel):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert jumlah_baris(c, 'produk') == 5
            c.execute('CREATE TABLE kosong (x INTEGER)')
            assert jumlah_baris(c, 'kosong') == 0
            c.execute('INSERT INTO kosong VALUES (1), (2)')
            assert jumlah_baris(c, 'kosong') == 2
            """,
            "Susun query COUNT bintang dengan nama tabel lalu ambil nilai pertama.",
            """
            import sqlite3

            def jumlah_baris(c, tabel):
                return c.execute(f'SELECT COUNT(*) FROM {tabel}').fetchone()[0]
            """,
        ),
        E(
            "A6-01-1-ex2",
            "sedang",
            """
            Tulis fungsi `nama_kolom(c, tabel)` yang mengembalikan list nama kolom tabel sesuai urutan, memakai `PRAGMA table_info`.
            """,
            """
            import sqlite3

            def nama_kolom(c, tabel):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert nama_kolom(c, 'produk') == ['id', 'nama', 'kategori', 'harga', 'stok']
            c.execute('CREATE TABLE t (x INTEGER, y TEXT)')
            assert nama_kolom(c, 't') == ['x', 'y']
            c.execute('CREATE TABLE u (a REAL)')
            assert nama_kolom(c, 'u') == ['a']
            """,
            "Ambil elemen kedua dari tiap baris hasil PRAGMA.",
            """
            import sqlite3

            def nama_kolom(c, tabel):
                return [r[1] for r in c.execute(f'PRAGMA table_info({tabel})').fetchall()]
            """,
        ),
        E(
            "A6-01-1-ex3",
            "sedang",
            """
            Tulis fungsi `buat_dan_ringkas(baris)` yang membuat basis data memori dengan tabel `item(id INTEGER PRIMARY KEY, nama TEXT, harga REAL)`, memasukkan list tuple `baris` dengan `executemany`, lalu mengembalikan tuple `(jumlah_baris, total_harga)`. Total harga `None` bila tabel kosong.
            """,
            """
            import sqlite3

            def buat_dan_ringkas(baris):
                # TODO: implementasikan
                pass
            """,
            """
            assert buat_dan_ringkas([(1, 'a', 2.5), (2, 'b', 3.5)]) == (2, 6.0)
            assert buat_dan_ringkas([]) == (0, None)
            assert buat_dan_ringkas([(1, 'x', 10)]) == (1, 10.0)
            assert buat_dan_ringkas([(1, 'p', 1), (2, 'q', 2), (3, 'r', 3)]) == (3, 6.0)
            """,
            "Buat tabel, masukkan baris dengan executemany, lalu jalankan COUNT dan SUM.",
            """
            import sqlite3

            def buat_dan_ringkas(baris):
                c = sqlite3.connect(':memory:')
                c.execute('CREATE TABLE item (id INTEGER PRIMARY KEY, nama TEXT, harga REAL)')
                c.executemany('INSERT INTO item VALUES (?, ?, ?)', baris)
                return c.execute('SELECT COUNT(*), SUM(harga) FROM item').fetchone()
            """,
        ),
        E(
            "A6-01-1-ex4",
            "menantang",
            """
            Tulis fungsi `tipe_nilai(c, tabel, kolom, id_baris)` yang mengembalikan hasil `typeof` kolom pada baris dengan `id` tertentu sebagai string.
            """,
            """
            import sqlite3

            def tipe_nilai(c, tabel, kolom, id_baris):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert tipe_nilai(c, 'produk', 'harga', 4) == 'real'
            assert tipe_nilai(c, 'produk', 'stok', 4) == 'null'
            assert tipe_nilai(c, 'produk', 'nama', 4) == 'text'
            assert tipe_nilai(c, 'produk', 'stok', 1) == 'integer'
            """,
            "Susun SELECT typeof dengan nama kolom dan filter id memakai parameter.",
            """
            import sqlite3

            def tipe_nilai(c, tabel, kolom, id_baris):
                return c.execute(f'SELECT typeof({kolom}) FROM {tabel} WHERE id = ?', (id_baris,)).fetchone()[0]
            """,
        ),
    ],
    [
        M("Mengandalkan urutan baris tanpa ORDER BY.", "Tambahkan ORDER BY bila urutan penting."),
        M("Memakai SELECT bintang pada tabel besar.", "Pilih hanya kolom yang dibutuhkan."),
        M("Menyusun SQL dengan menempelkan input pengguna ke string.", "Gunakan parameter bertanda tanya."),
    ],
    [
        Q("Satu baris pada tabel mewakili?", ["Satu entitas", "Satu atribut", "Satu tipe", "Satu basis data"], 0, "Baris adalah entitas.", hint="Entitas."),
        Q("Kunci primer?", ["Kolom unik pengenal baris", "Kolom teks", "Nama tabel", "Indeks"], 0, "Mengidentifikasi.", hint="Unik."),
        Q("COUNT bintang menghitung?", ["Semua baris", "Hanya non-NULL", "Kolom", "Tabel"], 0, "Termasuk NULL.", hint="Semua."),
        Q("typeof mengembalikan?", ["Tipe nilai sebenarnya", "Nama kolom", "Panjang", "Indeks"], 0, "Tipe dinamis.", hint="Tipe."),
        Q("Nilai kosong di SQL ditulis?", ["NULL", "0", "kosong", "None"], 0, "NULL.", hint="NULL."),
    ],
    [
        "Tabel berisi baris sebagai entitas dan kolom sebagai atribut.",
        "Kunci primer mengidentifikasi tiap baris secara unik.",
        "PRAGMA table_info dan typeof membantu mengenali struktur dan tipe.",
        "COUNT bintang menghitung semua baris sebagai pemeriksaan kewarasan.",
    ],
    [],
)

l2 = lesson(
    "A6-01-2",
    "SELECT: kolom, alias, ekspresi, dan DISTINCT",
    35,
    [
        "Memilih kolom tertentu dari tabel",
        "Memberi nama alias pada kolom hasil",
        "Menulis ekspresi aritmetika dan teks dalam SELECT",
        "Mengambil nilai unik dengan DISTINCT",
    ],
    [
        T("""
        ## Memilih kolom

        Query `SELECT` memilih kolom yang ingin dilihat dengan menyebut namanya dipisah koma. Hanya kolom itu yang dibaca dan dikembalikan, sehingga lebih cepat dan hasilnya lebih ringkas daripada bintang. Urutan kolom pada hasil mengikuti urutan yang kamu tulis, bukan urutan dalam tabel.

        Tulis kata kunci SQL dengan huruf besar dan nama dengan huruf kecil sebagai kebiasaan keterbacaan. SQL tidak peka huruf besar-kecil untuk kata kunci, tetapi konsistensi membuat query panjang jauh lebih mudah dibaca.
        """),
        C(
            SETUP + """
            print(c.execute('SELECT nama, harga FROM produk ORDER BY id').fetchall())
            """,
            """
            [('Pensil', 2500.0), ('Buku', 12000.0), ('Tas', 150000.0), ('Botol', 35000.0), ('Penggaris', 4000.0)]
            """,
            """
            Hanya dua kolom yang dikembalikan, sebagai list pasangan nama dan harga.
            """,
            filename="pilih_kolom.py",
        ),
        T("""
        ## Alias dengan AS

        Hasil ekspresi biasanya tidak punya nama bagus. **Alias** memberinya nama dengan `AS`: `SELECT harga / 1000.0 AS ribu`. Alias berguna untuk keterbacaan hasil, dan nama kolom dalam hasil query mengikuti alias. Pada pustaka seperti pandas, alias menjadi nama kolom DataFrame hasil.

        Alias tidak dapat dipakai di klausa `WHERE` pada kebanyakan basis data karena `WHERE` dievaluasi sebelum `SELECT`. Urutan evaluasi logis query dibahas lebih lanjut pada pelajaran berikutnya.
        """),
        T("""
        ## Ekspresi aritmetika

        Di dalam `SELECT` kita dapat menghitung dengan operator `+`, `-`, `*`, `/`, dan `%` serta fungsi seperti `round`, `abs`, dan `length`. Perhitungan dilakukan per baris, menghasilkan satu nilai per baris. Contoh mengubah harga ke satuan ribuan dengan satu desimal.

        Hati-hati dengan pembagian bilangan bulat. Di SQLite dan banyak basis data lain, `7 / 2` menghasilkan 3, bukan 3,5, karena kedua operan bulat. Ubah salah satu operan ke pecahan, misalnya `7 / 2.0`, untuk mendapat hasil desimal.
        """),
        C(
            SETUP + """
            print(c.execute('SELECT nama, round(harga / 1000.0, 1) AS ribu FROM produk ORDER BY id').fetchall())
            print(c.execute('SELECT 7 / 2, 7 / 2.0, 7 % 2').fetchone())
            """,
            """
            [('Pensil', 2.5), ('Buku', 12.0), ('Tas', 150.0), ('Botol', 35.0), ('Penggaris', 4.0)]
            (3, 3.5, 1)
            """,
            """
            Harga dikonversi ke ribuan, dan pembagian bulat menghasilkan tiga sedangkan pembagian dengan pecahan menghasilkan tiga koma lima.
            """,
            filename="ekspresi_alias.py",
        ),
        T("""
        ## Menggabung teks

        Operator `||` menyambung teks. Ia berguna untuk membuat label dari beberapa kolom, misalnya nama dengan kategori dalam kurung. Fungsi teks lain meliputi `upper`, `lower`, `length`, `substr`, dan `replace`. Daftar lengkapnya bergantung pada basis data, tetapi fungsi dasarnya hampir seragam.

        Menyambung teks dengan `NULL` menghasilkan `NULL`, jebakan yang akan dibahas bersama NULL pada pelajaran berikutnya. Gunakan `COALESCE` untuk mengganti `NULL` sebelum menyambung.
        """),
        C(
            SETUP + """
            print(c.execute("SELECT nama || ' (' || kategori || ')' FROM produk WHERE id = 1").fetchone())
            print(c.execute('SELECT upper(nama), length(nama) FROM produk WHERE id = 2').fetchone())
            """,
            """
            ('Pensil (alat tulis)',)
            ('BUKU', 4)
            """,
            """
            Operator penyambung membentuk label gabungan, dan fungsi teks mengubah huruf serta menghitung panjang.
            """,
            filename="fungsi_teks.py",
        ),
        T("""
        ## DISTINCT

        Kata kunci `DISTINCT` membuang baris hasil yang duplikat. `SELECT DISTINCT kategori FROM produk` mengembalikan tiap kategori sekali saja. Ia bekerja pada kombinasi semua kolom yang dipilih, sehingga dengan dua kolom yang dibuang hanya baris yang kedua kolomnya sama.

        Untuk menghitung jumlah nilai unik gunakan `COUNT(DISTINCT kolom)`. Menggunakan `DISTINCT` untuk menutupi duplikat akibat JOIN yang keliru adalah anti-pola: perbaiki sumber duplikatnya, jangan hanya menyembunyikannya.
        """),
        C(
            SETUP + """
            print(c.execute('SELECT DISTINCT kategori FROM produk ORDER BY kategori').fetchall())
            print(c.execute('SELECT COUNT(DISTINCT kategori) FROM produk').fetchone())
            """,
            """
            [('alat tulis',), ('perlengkapan',)]
            (2,)
            """,
            """
            Dua kategori unik, dan COUNT DISTINCT menghitungnya sebagai dua.
            """,
            filename="distinct.py",
        ),
        T("""
        ## Urutan penulisan dan evaluasi

        Kita menulis query dengan urutan `SELECT`, `FROM`, `WHERE`, `GROUP BY`, `HAVING`, `ORDER BY`, `LIMIT`. Tetapi mesin mengevaluasinya dengan urutan logis berbeda: `FROM` lebih dulu untuk menentukan sumber, lalu `WHERE`, `GROUP BY`, `HAVING`, `SELECT`, `DISTINCT`, `ORDER BY`, dan terakhir `LIMIT`.

        Memahami urutan ini menjelaskan banyak perilaku, misalnya mengapa alias dari `SELECT` tidak dikenali di `WHERE` tetapi dikenali di `ORDER BY`. Pemahaman urutan evaluasi adalah kunci menulis SQL yang benar tanpa trial and error.
        """),
        K(
            "tip",
            """
            Tulis query bertahap: mulai dari FROM, tambahkan WHERE, lalu kolom dan agregasi. Jalankan setiap tahap dan periksa hasilnya.
            """,
            title="Bangun query bertahap",
        ),
        T("""
        ## Fungsi skalar umum

        Selain `round` dan `length`, ada banyak fungsi skalar yang dipakai sehari-hari: `abs` untuk nilai mutlak, `lower` dan `upper` untuk huruf, `trim` untuk membuang spasi tepi, `substr` untuk mengambil potongan teks, dan `replace` untuk mengganti teks. Semuanya bekerja per baris dan menghasilkan satu nilai.

        Fungsi-fungsi ini penting untuk membersihkan data langsung di query, misalnya menyeragamkan huruf sebelum membandingkan atau memangkas spasi yang tidak terlihat dan menyebabkan pencocokan gagal tanpa pesan kesalahan.
        """),
        T("""
        ## Kolom dengan nama sama

        Bila dua kolom hasil memiliki nama sama, misalnya setelah menggabungkan tabel, sebagian alat hanya menyimpan salah satunya sehingga datanya hilang diam-diam. Beri alias berbeda agar semua kolom punya nama unik, terutama ketika hasil query akan dibaca ke pandas atau kode lain.

        Memberi alias pada kolom hasil ekspresi juga membuat kode pemakai lebih aman. Mengakses hasil lewat nama yang bermakna lebih tahan terhadap perubahan urutan kolom daripada mengaksesnya lewat indeks angka.
        """),
        T("""
        ## Membaca hasil query di Python

        Metode `fetchone` mengambil satu baris, `fetchall` semua baris sebagai list tuple, dan iterasi langsung pada hasil `execute` mengambil baris satu per satu sehingga hemat memori pada hasil besar. Atribut `description` kursor memuat nama kolom hasil.

        Untuk analisis, hasil sering dibaca langsung ke DataFrame dengan `pandas.read_sql_query`. Cara itu memanfaatkan alias sebagai nama kolom, jadi menulis alias yang jelas di SQL langsung memperbaiki keterbacaan seluruh analisis di bawahnya.
        """),
        E(
            "A6-01-2-ex1",
            "mudah",
            """
            Tulis fungsi `nama_dan_harga(c)` yang mengembalikan list tuple `(nama, harga)` semua produk terurut menurut `id`.
            """,
            """
            import sqlite3

            def nama_dan_harga(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            h = nama_dan_harga(c)
            assert h[0] == ('Pensil', 2500.0)
            assert h[-1] == ('Penggaris', 4000.0)
            assert len(h) == 5
            assert h[2] == ('Tas', 150000.0)
            """,
            "Pilih dua kolom dan urutkan menurut id.",
            """
            import sqlite3

            def nama_dan_harga(c):
                return c.execute('SELECT nama, harga FROM produk ORDER BY id').fetchall()
            """,
        ),
        E(
            "A6-01-2-ex2",
            "sedang",
            """
            Tulis fungsi `harga_ribuan(c)` yang mengembalikan list tuple `(nama, ribu)` dengan `ribu` adalah harga dibagi 1000.0 dibulatkan satu desimal, terurut menurut `id`.
            """,
            """
            import sqlite3

            def harga_ribuan(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert harga_ribuan(c) == [('Pensil', 2.5), ('Buku', 12.0), ('Tas', 150.0), ('Botol', 35.0), ('Penggaris', 4.0)]
            c.execute("INSERT INTO produk VALUES (6, 'Kertas', 'alat tulis', 1260, 5)")
            assert harga_ribuan(c)[-1] == ('Kertas', 1.3)
            assert len(harga_ribuan(c)) == 6
            """,
            "Bagi harga dengan 1000.0, bulatkan, dan beri alias.",
            """
            import sqlite3

            def harga_ribuan(c):
                return c.execute('SELECT nama, round(harga / 1000.0, 1) AS ribu FROM produk ORDER BY id').fetchall()
            """,
        ),
        E(
            "A6-01-2-ex3",
            "sedang",
            """
            Tulis fungsi `kategori_unik(c)` yang mengembalikan list nama kategori unik terurut abjad sebagai string.
            """,
            """
            import sqlite3

            def kategori_unik(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert kategori_unik(c) == ['alat tulis', 'perlengkapan']
            c.execute("INSERT INTO produk VALUES (6, 'Apel', 'buah', 5000, 10)")
            assert kategori_unik(c) == ['alat tulis', 'buah', 'perlengkapan']
            c.execute("INSERT INTO produk VALUES (7, 'Jeruk', 'buah', 6000, 12)")
            assert kategori_unik(c) == ['alat tulis', 'buah', 'perlengkapan']
            """,
            "Pakai DISTINCT dengan ORDER BY lalu ratakan tuple menjadi string.",
            """
            import sqlite3

            def kategori_unik(c):
                return [r[0] for r in c.execute('SELECT DISTINCT kategori FROM produk ORDER BY kategori').fetchall()]
            """,
        ),
        E(
            "A6-01-2-ex4",
            "menantang",
            """
            Tulis fungsi `label_produk(c)` yang mengembalikan list string berformat `nama (kategori)` untuk semua produk terurut menurut `id`, memakai operator `||` di SQL.
            """,
            """
            import sqlite3

            def label_produk(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert label_produk(c) == ['Pensil (alat tulis)', 'Buku (alat tulis)', 'Tas (perlengkapan)', 'Botol (perlengkapan)', 'Penggaris (alat tulis)']
            c.execute("INSERT INTO produk VALUES (6, 'Apel', 'buah', 5000, 10)")
            assert label_produk(c)[-1] == 'Apel (buah)'
            assert len(label_produk(c)) == 6
            """,
            "Sambung nama, spasi, kurung buka, kategori, dan kurung tutup dengan operator penyambung.",
            """
            import sqlite3

            def label_produk(c):
                q = "SELECT nama || ' (' || kategori || ')' FROM produk ORDER BY id"
                return [r[0] for r in c.execute(q).fetchall()]
            """,
        ),
    ],
    [
        M("Mengira 7 / 2 di SQL menghasilkan 3,5.", "Pembagian bulat menghasilkan 3, pakai 2.0."),
        M("Memakai DISTINCT untuk menutupi duplikat akibat JOIN keliru.", "Perbaiki sumber duplikatnya."),
        M("Memakai alias SELECT di klausa WHERE.", "Ulangi ekspresinya atau pakai subquery."),
    ],
    [
        Q("Alias dibuat dengan?", ["AS", "IS", "IN", "ON"], 0, "Kata kunci AS.", hint="Nama lain."),
        Q("7 / 2 pada SQLite menghasilkan?", ["3", "3.5", "4", "2"], 0, "Pembagian bulat.", hint="Bulat."),
        Q("Operator penyambung teks?", ["||", "+", "&", "."], 0, "Standar SQL.", hint="Dua garis."),
        Q("DISTINCT melakukan?", ["Membuang baris duplikat", "Mengurutkan", "Menghitung", "Menghapus tabel"], 0, "Nilai unik.", hint="Unik."),
        Q("Urutan evaluasi pertama?", ["FROM", "SELECT", "ORDER BY", "LIMIT"], 0, "Sumber dulu.", hint="Sumber."),
    ],
    [
        "SELECT memilih kolom dan menghitung ekspresi per baris.",
        "Alias memberi nama pada hasil ekspresi.",
        "Pembagian bulat memotong pecahan, pakai operan desimal.",
        "DISTINCT mengembalikan nilai unik dan COUNT DISTINCT menghitungnya.",
    ],
    [],
)

l3 = lesson(
    "A6-01-3",
    "NULL, COALESCE, dan CASE",
    35,
    [
        "Menjelaskan logika tiga nilai yang melibatkan NULL",
        "Menguji NULL dengan IS NULL",
        "Mengganti NULL dengan COALESCE",
        "Membuat kolom kategori dengan CASE",
    ],
    [
        T("""
        ## NULL berarti tidak diketahui

        `NULL` bukan nol dan bukan string kosong. Ia berarti **tidak diketahui** atau tidak ada nilai. Karena itu operasi apa pun dengan `NULL` menghasilkan `NULL`: `NULL + 1` adalah `NULL`, dan bahkan `NULL = NULL` bukan benar melainkan `NULL`, sebab dua nilai yang tidak diketahui belum tentu sama.

        Ini sumber bug terbanyak bagi pemula SQL. Kondisi `WHERE stok = NULL` tidak pernah mengembalikan baris apa pun. Cara yang benar adalah `IS NULL`, operator khusus yang menguji kekosongan.
        """),
        C(
            SETUP + """
            print(c.execute('SELECT nama FROM produk WHERE stok = NULL').fetchall())
            print(c.execute('SELECT nama FROM produk WHERE stok IS NULL').fetchall())
            print(c.execute('SELECT NULL IS NULL, 1 IS NULL, NULL = NULL, NULL + 1').fetchone())
            """,
            """
            []
            [('Botol',)]
            (1, 0, None, None)
            """,
            """
            Perbandingan dengan sama dengan NULL tidak mengembalikan baris, sedangkan IS NULL menemukan Botol.
            """,
            filename="null_dasar.py",
        ),
        T("""
        ## Logika tiga nilai

        SQL memakai logika tiga nilai: benar, salah, dan tidak diketahui. Klausa `WHERE` hanya meloloskan baris yang kondisinya benar, jadi baris dengan kondisi tidak diketahui terbuang diam-diam. `stok > 10` pada baris dengan stok `NULL` bernilai tidak diketahui sehingga barisnya tidak ikut.

        Konsekuensinya, `WHERE stok > 10` dan `WHERE NOT stok > 10` tidak saling melengkapi: baris `NULL` tidak muncul di keduanya. Ingat hal ini setiap kali memfilter kolom yang mungkin berisi `NULL`.
        """),
        T("""
        ## NULL dalam agregasi

        Fungsi agregat mengabaikan `NULL`, kecuali `COUNT(*)` yang menghitung semua baris. `COUNT(stok)` menghitung hanya baris dengan stok terisi, sehingga pada tabel kita bernilai empat sedangkan `COUNT(*)` bernilai lima. `AVG`, `SUM`, `MIN`, dan `MAX` juga melewati `NULL`.

        Akibatnya rata-rata kolom dengan banyak `NULL` dihitung dari yang ada saja, mirip perilaku pandas. Selalu bandingkan `COUNT(*)` dengan `COUNT(kolom)` untuk mengetahui berapa banyak data hilang sebelum memercayai agregat.
        """),
        C(
            SETUP + """
            print(c.execute('SELECT COUNT(*), COUNT(stok), AVG(stok) FROM produk').fetchone())
            """,
            """
            (5, 4, 52.0)
            """,
            """
            Lima baris tetapi hanya empat stok terisi, dan rata-rata dihitung dari empat nilai saja yaitu lima puluh dua.
            """,
            filename="null_agregasi.py",
        ),
        T("""
        ## COALESCE

        `COALESCE(a, b, c)` mengembalikan argumen pertama yang bukan `NULL`. Ini cara standar mengganti `NULL` dengan nilai bawaan, misalnya `COALESCE(stok, 0)` untuk menganggap stok kosong sebagai nol. Ia juga berguna untuk memilih dari beberapa kolom alternatif berurutan.

        Berhati-hatilah: mengisi `NULL` dengan nol mengubah makna dari tidak diketahui menjadi nol. Untuk stok mungkin wajar, tetapi untuk nilai seperti suhu atau gaji, nol bisa menyesatkan agregat. Pilih nilai pengganti sesuai makna data.
        """),
        C(
            SETUP + """
            print(c.execute('SELECT nama, COALESCE(stok, 0) FROM produk ORDER BY id').fetchall())
            """,
            """
            [('Pensil', 100), ('Buku', 40), ('Tas', 8), ('Botol', 0), ('Penggaris', 60)]
            """,
            """
            Stok kosong Botol diganti nol, sedangkan stok lain tidak berubah.
            """,
            filename="coalesce.py",
        ),
        T("""
        ## CASE untuk logika kondisional

        Ekspresi `CASE WHEN kondisi THEN nilai ... ELSE nilai END` adalah if-else dalam SQL. Ia mengevaluasi kondisi berurutan dan mengembalikan nilai kondisi pertama yang benar. Tanpa `ELSE`, baris yang tidak cocok menghasilkan `NULL`. `CASE` dipakai untuk membuat kategori, label, dan penanda dari kolom numerik.

        Contoh golongan harga: di bawah 5.000 murah, di bawah 50.000 sedang, selebihnya mahal. Urutan `WHEN` penting karena hanya kondisi pertama yang benar yang dipakai.
        """),
        C(
            SETUP + """
            q = '''
            SELECT nama,
                   CASE WHEN harga < 5000 THEN 'murah'
                        WHEN harga < 50000 THEN 'sedang'
                        ELSE 'mahal' END AS golongan
            FROM produk ORDER BY id
            '''
            print(c.execute(q).fetchall())
            """,
            """
            [('Pensil', 'murah'), ('Buku', 'sedang'), ('Tas', 'mahal'), ('Botol', 'sedang'), ('Penggaris', 'murah')]
            """,
            """
            Tiap produk mendapat golongan harga sesuai kondisi pertama yang terpenuhi.
            """,
            filename="case_when.py",
        ),
        T("""
        ## NULL dalam perhitungan baris

        Perhitungan per baris yang melibatkan `NULL` menghasilkan `NULL`. Nilai stok dikali harga untuk Botol adalah `NULL` karena stoknya tidak diketahui. Ini perilaku yang benar: kita tidak tahu nilai stoknya. Mengubahnya menjadi nol dengan `COALESCE` akan berarti mengklaim stoknya kosong.

        Rancang query dengan sadar: tentukan apakah baris `NULL` harus tetap `NULL`, diganti, atau dibuang, lalu tulis keputusan itu secara eksplisit dalam query agar pembaca memahaminya.
        """),
        C(
            SETUP + """
            print(c.execute('SELECT nama, stok * harga FROM produk ORDER BY id').fetchall())
            """,
            """
            [('Pensil', 250000.0), ('Buku', 480000.0), ('Tas', 1200000.0), ('Botol', None), ('Penggaris', 240000.0)]
            """,
            """
            Nilai stok Botol tidak diketahui sehingga hasil perkaliannya juga tidak diketahui.
            """,
            filename="null_hitung.py",
        ),
        K(
            "warn",
            """
            Jangan menulis kolom sama dengan NULL. Pakai IS NULL atau IS NOT NULL. Perbandingan dengan NULL selalu tidak diketahui dan membuang baris.
            """,
            title="Jebakan NULL",
        ),
        T("""
        ## Mengisi atau membiarkan NULL

        Ada tiga strategi untuk NULL. Pertama membiarkannya dan menerima bahwa agregat mengabaikannya. Kedua menggantinya dengan nilai bawaan lewat `COALESCE`. Ketiga membuang barisnya dengan `WHERE kolom IS NOT NULL`. Tidak ada yang selalu benar, dan pilihan harus mencerminkan makna data serta pertanyaan analisis.

        Dokumentasikan pilihan itu di komentar atau catatan analisis. Dua analis yang memilih berbeda akan mendapat angka berbeda dari data sama, dan perbedaan itu harus bisa dijelaskan.
        """),
        T("""
        ## NULLIF dan pembagian aman

        Fungsi `NULLIF(a, b)` mengembalikan `NULL` bila `a` sama dengan `b`, selain itu `a`. Kegunaan paling umum adalah menghindari pembagian dengan nol: `harga / NULLIF(stok, 0)` menghasilkan `NULL` alih-alih galat saat stok nol. Dipasangkan dengan `COALESCE`, ia memberi cara ringkas menangani kasus tepi.

        Pada SQLite pembagian dengan nol sebenarnya menghasilkan `NULL`, tetapi PostgreSQL dan lainnya melempar galat. Menulis `NULLIF` membuat query aman di semua basis data.
        """),
        T("""
        ## CASE dalam agregasi

        `CASE` sangat kuat bila digabung dengan agregat, misalnya menghitung banyak produk murah dan mahal dalam satu query dengan `SUM(CASE WHEN harga < 5000 THEN 1 ELSE 0 END)`. Pola ini disebut agregasi bersyarat dan menggantikan banyak query terpisah dengan satu lintasan data.

        Kita akan memakainya lagi pada pelajaran agregasi dan GROUP BY. Menguasai CASE sekarang membuka cara menulis laporan silang yang ringkas tanpa harus mengolahnya di luar basis data.
        """),
        E(
            "A6-01-3-ex1",
            "mudah",
            """
            Tulis fungsi `produk_tanpa_stok(c)` yang mengembalikan list nama produk dengan stok `NULL`, terurut menurut `id`.
            """,
            """
            import sqlite3

            def produk_tanpa_stok(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert produk_tanpa_stok(c) == ['Botol']
            c.execute("INSERT INTO produk VALUES (6, 'Kertas', 'alat tulis', 1000, NULL)")
            assert produk_tanpa_stok(c) == ['Botol', 'Kertas']
            c.execute('UPDATE produk SET stok = 1 WHERE id = 4')
            assert produk_tanpa_stok(c) == ['Kertas']
            """,
            "Saring dengan IS NULL dan urutkan menurut id.",
            """
            import sqlite3

            def produk_tanpa_stok(c):
                return [r[0] for r in c.execute('SELECT nama FROM produk WHERE stok IS NULL ORDER BY id').fetchall()]
            """,
        ),
        E(
            "A6-01-3-ex2",
            "sedang",
            """
            Tulis fungsi `stok_aman(c)` yang mengembalikan list tuple `(nama, stok)` dengan stok `NULL` diganti 0, terurut menurut `id`.
            """,
            """
            import sqlite3

            def stok_aman(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert stok_aman(c) == [('Pensil', 100), ('Buku', 40), ('Tas', 8), ('Botol', 0), ('Penggaris', 60)]
            c.execute("INSERT INTO produk VALUES (6, 'Kertas', 'alat tulis', 1000, NULL)")
            assert stok_aman(c)[-1] == ('Kertas', 0)
            assert len(stok_aman(c)) == 6
            """,
            "Pakai COALESCE pada kolom stok.",
            """
            import sqlite3

            def stok_aman(c):
                return c.execute('SELECT nama, COALESCE(stok, 0) FROM produk ORDER BY id').fetchall()
            """,
        ),
        E(
            "A6-01-3-ex3",
            "sedang",
            """
            Tulis fungsi `golongan_harga(c)` yang mengembalikan list tuple `(nama, golongan)` dengan golongan `'murah'` bila harga di bawah 5000, `'sedang'` bila di bawah 50000, dan `'mahal'` selebihnya, terurut menurut `id`, memakai `CASE`.
            """,
            """
            import sqlite3

            def golongan_harga(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert golongan_harga(c) == [('Pensil', 'murah'), ('Buku', 'sedang'), ('Tas', 'mahal'), ('Botol', 'sedang'), ('Penggaris', 'murah')]
            c.execute("INSERT INTO produk VALUES (6, 'Laptop', 'elektronik', 5000000, 2)")
            assert golongan_harga(c)[-1] == ('Laptop', 'mahal')
            c.execute("INSERT INTO produk VALUES (7, 'Klip', 'alat tulis', 4999, 2)")
            assert golongan_harga(c)[-1] == ('Klip', 'murah')
            """,
            "Susun CASE WHEN dengan dua kondisi berurutan dan ELSE untuk sisanya.",
            """
            import sqlite3

            def golongan_harga(c):
                q = '''
                SELECT nama,
                       CASE WHEN harga < 5000 THEN 'murah'
                            WHEN harga < 50000 THEN 'sedang'
                            ELSE 'mahal' END
                FROM produk ORDER BY id
                '''
                return c.execute(q).fetchall()
            """,
        ),
        E(
            "A6-01-3-ex4",
            "menantang",
            """
            Tulis fungsi `nilai_stok(c)` yang mengembalikan list tuple `(nama, nilai)` dengan `nilai = stok * harga` apa adanya, sehingga `None` bila stok `NULL`, terurut menurut `id`.
            """,
            """
            import sqlite3

            def nilai_stok(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert nilai_stok(c) == [('Pensil', 250000.0), ('Buku', 480000.0), ('Tas', 1200000.0), ('Botol', None), ('Penggaris', 240000.0)]
            c.execute('UPDATE produk SET stok = 2 WHERE id = 4')
            assert nilai_stok(c)[3] == ('Botol', 70000.0)
            c.execute('UPDATE produk SET stok = NULL WHERE id = 1')
            assert nilai_stok(c)[0] == ('Pensil', None)
            """,
            "Kalikan kolom stok dan harga tanpa mengganti NULL.",
            """
            import sqlite3

            def nilai_stok(c):
                return c.execute('SELECT nama, stok * harga FROM produk ORDER BY id').fetchall()
            """,
        ),
    ],
    [
        M("Menulis WHERE kolom = NULL.", "Tulis WHERE kolom IS NULL."),
        M("Mengganti semua NULL dengan nol tanpa berpikir.", "Pilih pengganti sesuai makna data."),
        M("Mengira COUNT(kolom) sama dengan COUNT bintang.", "COUNT kolom mengabaikan NULL."),
    ],
    [
        Q("NULL = NULL bernilai?", ["NULL", "Benar", "Salah", "Nol"], 0, "Tidak diketahui.", hint="Tidak diketahui."),
        Q("Menguji kosong memakai?", ["IS NULL", "= NULL", "== NULL", "EMPTY"], 0, "Operator khusus.", hint="IS."),
        Q("COUNT(kolom) menghitung?", ["Baris non-NULL", "Semua baris", "Kolom", "NULL"], 0, "Mengabaikan NULL.", hint="Non-NULL."),
        Q("COALESCE mengembalikan?", ["Argumen pertama non-NULL", "Argumen terakhir", "Rata-rata", "NULL"], 0, "Pengganti.", hint="Pertama."),
        Q("CASE tanpa ELSE untuk baris tak cocok?", ["NULL", "0", "Kosong", "Error"], 0, "Default NULL.", hint="NULL."),
    ],
    [
        "NULL berarti tidak diketahui dan membuat perhitungan menjadi NULL.",
        "Gunakan IS NULL, bukan sama dengan NULL.",
        "Agregat mengabaikan NULL kecuali COUNT bintang.",
        "COALESCE dan CASE mengganti dan mengategorikan nilai secara eksplisit.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perintah yang cukup jelas dalam teks.", "brief": []}

write_module(
    "A6",
    1,
    "Pengantar relasional dan SELECT",
    105,
    [
        "Menjelaskan tabel, baris, kolom, dan kunci primer",
        "Menulis SELECT dengan alias, ekspresi, dan DISTINCT",
        "Menangani NULL dengan IS NULL, COALESCE, dan CASE",
    ],
    [l1, l2, l3],
    video,
    REF,
)
