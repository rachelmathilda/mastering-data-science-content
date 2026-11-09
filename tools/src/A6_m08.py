import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

IND = '            '

SETUP2 = textwrap.indent("""import sqlite3

c = sqlite3.connect(':memory:')
c.executescript('''
CREATE TABLE kategori (id INTEGER PRIMARY KEY, nama TEXT NOT NULL UNIQUE);
CREATE TABLE barang (
    id INTEGER PRIMARY KEY,
    kode TEXT NOT NULL UNIQUE,
    nama TEXT NOT NULL,
    harga INTEGER NOT NULL CHECK (harga >= 0),
    kategori_id INTEGER REFERENCES kategori(id)
);
INSERT INTO kategori VALUES (1, 'ATK'), (2, 'Elektronik'), (3, 'Kosong');
INSERT INTO barang (kode, nama, harga, kategori_id) VALUES ('P1', 'Pensil', 2500, 1), ('E1', 'Kabel', 15000, 2);
''')
""", IND)

FIX2 = textwrap.indent("""import sqlite3

def _db(fk=False):
    c = sqlite3.connect(':memory:')
    c.executescript('''
    CREATE TABLE kategori (id INTEGER PRIMARY KEY, nama TEXT NOT NULL UNIQUE);
    CREATE TABLE barang (
        id INTEGER PRIMARY KEY,
        kode TEXT NOT NULL UNIQUE,
        nama TEXT NOT NULL,
        harga INTEGER NOT NULL CHECK (harga >= 0),
        kategori_id INTEGER REFERENCES kategori(id)
    );
    INSERT INTO kategori VALUES (1, 'ATK'), (2, 'Elektronik'), (3, 'Kosong');
    INSERT INTO barang (kode, nama, harga, kategori_id) VALUES ('P1', 'Pensil', 2500, 1), ('E1', 'Kabel', 15000, 2);
    ''')
    if fk:
        c.execute('PRAGMA foreign_keys = ON')
    return c

""", IND)

SETUP3 = textwrap.indent("""import sqlite3

c = sqlite3.connect(':memory:')
c.execute('CREATE TABLE log (id INTEGER PRIMARY KEY, user_id INTEGER, aksi TEXT)')
c.executemany('INSERT INTO log (user_id, aksi) VALUES (?, ?)', [(i % 100, 'a' if i % 2 == 0 else 'b') for i in range(1000)])

def pakai_indeks(q):
    return any('INDEX' in r[3] for r in c.execute('EXPLAIN QUERY PLAN ' + q).fetchall())
""", IND)

FIX3 = textwrap.indent("""import sqlite3

def _db():
    c = sqlite3.connect(':memory:')
    c.executescript('''
    CREATE TABLE log (id INTEGER PRIMARY KEY, user_id INTEGER, aksi TEXT);
    CREATE TABLE pengguna (id INTEGER PRIMARY KEY, email TEXT);
    INSERT INTO pengguna VALUES (1, 'a@x.com'), (2, 'b@x.com'), (3, NULL);
    ''')
    c.executemany('INSERT INTO log (user_id, aksi) VALUES (?, ?)', [(i % 100, 'a' if i % 2 == 0 else 'b') for i in range(1000)])
    return c

def _pakai(c, q):
    return any('INDEX' in r[3] for r in c.execute('EXPLAIN QUERY PLAN ' + q).fetchall())

def _gagal(c, sql, args=()):
    try:
        c.execute(sql, args)
        return False
    except sqlite3.IntegrityError:
        return True

""", IND)

FIX1 = textwrap.indent("""import sqlite3

def _gagal(c, sql, args=()):
    try:
        c.execute(sql, args)
        return False
    except sqlite3.IntegrityError:
        return True

""", IND)
l1 = lesson(
    "A6-08-1",
    "Membuat tabel dan constraint",
    35,
    [
        "Menulis CREATE TABLE dengan tipe, PRIMARY KEY, dan DEFAULT",
        "Memakai NOT NULL, UNIQUE, dan CHECK untuk menjaga kualitas data",
        "Menangani pelanggaran constraint dengan IntegrityError",
        "Mendefinisikan primary key gabungan",
    ],
    [
        T("""
        ## Dari membaca ke merancang

        Lima modul SQL sebelumnya berfokus pada membaca data. Modul ini membahas sisi lain: **merancang tabel** yang menyimpan data dengan benar sejak awal. Data yang masuk tanpa aturan akan kotor, dan membersihkannya kemudian jauh lebih mahal daripada mencegahnya di pintu masuk.

        Alat pencegahnya adalah **constraint**, yaitu aturan yang ditegakkan basis data pada setiap penyisipan dan pembaruan. Constraint memastikan kualitas data tidak bergantung pada kedisiplinan setiap aplikasi yang menulis ke tabel.
        """),
        T("""
        ## CREATE TABLE

        Pernyataan `CREATE TABLE nama (kolom tipe aturan, ...)` mendefinisikan tabel. Setiap kolom punya nama, tipe, dan aturan opsional. SQLite memakai tipe dinamis dengan afinitas: `INTEGER`, `TEXT`, `REAL`, `BLOB`, dan `NUMERIC`. Tipe yang dideklarasikan menjadi petunjuk konversi, bukan pagar ketat seperti pada basis data lain.

        Karena itu constraint seperti `CHECK` menjadi penjaga yang lebih penting di SQLite: tipe saja tidak mencegah nilai aneh masuk.
        """),
        T("""
        ## PRIMARY KEY

        **Primary key** mengidentifikasi setiap baris secara unik. Kolom `id INTEGER PRIMARY KEY` di SQLite menjadi alias dari `rowid` dan terisi otomatis dengan nomor berikutnya bila tidak diberi nilai. Primary key tidak boleh duplikat, dan sebaiknya tidak pernah berubah selama hidup baris.

        Pilih kunci yang stabil dan tidak bermakna bisnis. Nomor identitas buatan lebih aman daripada nama atau email yang bisa berubah dan memaksa pembaruan di banyak tempat.
        """),
        T("""
        ## NOT NULL, UNIQUE, CHECK, DEFAULT

        `NOT NULL` melarang nilai kosong. `UNIQUE` melarang duplikat pada kolom itu. `CHECK (kondisi)` menolak baris yang kondisinya tidak benar, misalnya `harga >= 0`. `DEFAULT nilai` mengisi kolom bila penyisipan tidak menyebutkannya.

        Kombinasi ini menyatakan aturan bisnis langsung di skema. Kode `UNIQUE` pada kolom kode barang, misalnya, menjamin tidak ada dua barang berkode sama walau dua aplikasi berbeda menulis pada waktu bersamaan.
        """),
        C(
            """
            import sqlite3

            c = sqlite3.connect(':memory:')
            c.execute('''
            CREATE TABLE barang (
                id INTEGER PRIMARY KEY,
                kode TEXT NOT NULL UNIQUE,
                nama TEXT NOT NULL,
                harga INTEGER NOT NULL CHECK (harga >= 0),
                stok INTEGER NOT NULL DEFAULT 0 CHECK (stok >= 0)
            )
            ''')

            def coba(sql, args=()):
                try:
                    c.execute(sql, args)
                    return 'ok'
                except sqlite3.IntegrityError:
                    return 'ditolak'

            print(coba("INSERT INTO barang (kode, nama, harga) VALUES ('P1', 'Pensil', 2500)"))
            print(coba("INSERT INTO barang (kode, nama, harga) VALUES ('P1', 'Pena', 3000)"))
            print(coba("INSERT INTO barang (kode, nama, harga) VALUES ('P2', NULL, 3000)"))
            print(coba("INSERT INTO barang (kode, nama, harga) VALUES ('P3', 'X', -5)"))
            print(coba("INSERT INTO barang (kode, nama, harga, stok) VALUES ('P4', 'X', 5, -1)"))
            print(c.execute('SELECT * FROM barang').fetchall())
            """,
            """
            ok
            ditolak
            ditolak
            ditolak
            ditolak
            [(1, 'P1', 'Pensil', 2500, 0)]
            """,
            """
            Hanya penyisipan pertama yang lolos. Duplikat kode, nama kosong, harga negatif, dan stok negatif semuanya ditolak, dan stok bawaan nol terisi otomatis.
            """,
            filename="constraint_dasar.py",
        ),
        T("""
        ## Menangani pelanggaran

        Ketika constraint dilanggar, basis data melempar kesalahan dan baris tidak masuk. Di Python, kesalahan ini adalah `sqlite3.IntegrityError`. Aplikasi yang baik menangkapnya dan menampilkan pesan yang berguna, misalnya kode barang sudah dipakai, bukan membiarkan program berhenti.

        Perhatikan bahwa penolakan adalah fitur, bukan bug. Basis data yang menolak data buruk melindungi seluruh analisis di hilir. Lebih baik satu penyisipan gagal daripada seribu laporan salah.
        """),
        T("""
        ## Primary key gabungan

        Kadang identitas baris ditentukan oleh beberapa kolom sekaligus. Nilai ujian, misalnya, unik untuk pasangan siswa dan mata pelajaran: seorang siswa boleh punya banyak nilai, tetapi hanya satu per mata pelajaran. Tulis `PRIMARY KEY (siswa, mapel)` di akhir definisi.

        Dengan kunci gabungan, duplikasi pasangan ditolak walau tiap kolom sendiri boleh berulang. `CHECK (skor BETWEEN 0 AND 100)` melengkapinya dengan batas nilai wajar.
        """),
        C(
            """
            import sqlite3

            c = sqlite3.connect(':memory:')
            c.execute('''
            CREATE TABLE nilai (
                siswa INTEGER,
                mapel TEXT,
                skor INTEGER CHECK (skor BETWEEN 0 AND 100),
                PRIMARY KEY (siswa, mapel)
            )
            ''')

            def coba(sql):
                try:
                    c.execute(sql)
                    return 'ok'
                except sqlite3.IntegrityError:
                    return 'ditolak'

            print(coba("INSERT INTO nilai VALUES (1, 'MTK', 90)"))
            print(coba("INSERT INTO nilai VALUES (1, 'MTK', 80)"))
            print(coba("INSERT INTO nilai VALUES (1, 'IPA', 101)"))
            print(coba("INSERT INTO nilai VALUES (1, 'IPA', 100)"))
            print(coba("INSERT INTO nilai VALUES (2, 'MTK', 0)"))
            """,
            """
            ok
            ditolak
            ditolak
            ok
            ok
            """,
            """
            Pasangan siswa dan mapel yang sama ditolak dan skor di luar nol sampai seratus ditolak. Skor nol masih sah, dan siswa lain boleh punya mapel yang sama.
            """,
            filename="kunci_gabungan.py",
        ),
        T("""
        ## NULL dan UNIQUE

        Pada SQLite, kolom `UNIQUE` yang boleh kosong menerima banyak `NULL`, karena dua `NULL` dianggap tidak sama. Jadi `UNIQUE` saja tidak mencegah banyak baris tanpa email. Bila kolom wajib terisi dan unik, gabungkan `NOT NULL UNIQUE`.

        Pahami perbedaan ini sebelum bergantung pada `UNIQUE` untuk deduplikasi. Banyak bug identitas ganda berawal dari kolom unik yang diam-diam menerima `NULL`.
        """),
        K(
            "tip",
            """
            Letakkan aturan bisnis sederhana di skema dengan NOT NULL, UNIQUE, dan CHECK. Skema menegakkannya untuk semua aplikasi sekaligus.
            """,
            title="Aturan di skema",
        ),
        C(
            """
            import sqlite3

            c = sqlite3.connect(':memory:')
            c.execute('CREATE TABLE kontak (id INTEGER PRIMARY KEY, email TEXT UNIQUE)')
            c.execute('INSERT INTO kontak (email) VALUES (NULL)')
            c.execute('INSERT INTO kontak (email) VALUES (NULL)')
            c.execute("INSERT INTO kontak (email) VALUES ('a@x.com')")
            try:
                c.execute("INSERT INTO kontak (email) VALUES ('a@x.com')")
            except sqlite3.IntegrityError:
                print('duplikat ditolak')
            print(c.execute('SELECT COUNT(*) FROM kontak').fetchone())
            print(c.execute('SELECT COUNT(*) FROM kontak WHERE email IS NULL').fetchone())
            """,
            """
            duplikat ditolak
            (3,)
            (2,)
            """,
            """
            Dua NULL diterima pada kolom UNIQUE, tetapi email yang sama dua kali ditolak.
            """,
            filename="unique_null.py",
        ),
        T("""
        ## Merancang dengan hati-hati

        Sebelum menulis `CREATE TABLE`, tuliskan dulu pertanyaan yang harus dijawab tabel itu dan aturan yang harus selalu benar. Dari aturan itulah constraint ditentukan: kolom mana yang wajib, mana yang unik, dan batas nilai wajar. Merancang di atas kertas lebih murah daripada mengubah skema setelah data masuk.

        Ubah skema yang sudah berisi data memang mungkin, tetapi data lama yang melanggar aturan baru harus dibersihkan lebih dulu. Karena itu semakin awal aturan ditegakkan, semakin murah biayanya.
        """),
        T("""
        ## Skema sebagai kontrak

        Skema dengan constraint berfungsi sebagai kontrak antara basis data dan semua pengguna datanya. Analis dapat mengandalkan bahwa kolom wajib tidak kosong, kode unik benar-benar unik, dan harga tidak negatif, tanpa memeriksanya satu per satu di setiap laporan.

        Kontrak ini menghemat waktu seluruh tim. Semakin banyak aturan ditegakkan di skema, semakin sedikit kode pembersihan yang harus ditulis dan dipelihara di tempat lain.
        """),
        E(
            "A6-08-1-ex1",
            "mudah",
            """
            Tulis fungsi `buat_tabel_produk(c)` yang membuat tabel `produk` dengan kolom `id INTEGER PRIMARY KEY`, `kode TEXT` (wajib dan unik), dan `harga INTEGER` (wajib dan tidak boleh negatif).
            """,
            """
            import sqlite3

            def buat_tabel_produk(c):
                # TODO: implementasikan
                pass
            """,
            FIX1 + """
            c = sqlite3.connect(':memory:')
            buat_tabel_produk(c)
            c.execute("INSERT INTO produk (kode, harga) VALUES ('A', 10)")
            assert _gagal(c, "INSERT INTO produk (kode, harga) VALUES ('A', 20)")
            assert _gagal(c, "INSERT INTO produk (kode, harga) VALUES ('B', -1)")
            assert _gagal(c, "INSERT INTO produk (kode, harga) VALUES (NULL, 5)")
            assert not _gagal(c, "INSERT INTO produk (kode, harga) VALUES ('C', 0)")
            """,
            "Gabungkan NOT NULL UNIQUE untuk kode dan NOT NULL CHECK untuk harga.",
            """
            import sqlite3

            def buat_tabel_produk(c):
                c.execute('''
                CREATE TABLE produk (
                    id INTEGER PRIMARY KEY,
                    kode TEXT NOT NULL UNIQUE,
                    harga INTEGER NOT NULL CHECK (harga >= 0)
                )
                ''')
            """,
        ),
        E(
            "A6-08-1-ex2",
            "sedang",
            """
            Tulis fungsi `sisip_aman(c, kode, harga)` yang menyisipkan baris ke tabel `produk(kode, harga)` dan mengembalikan `True` bila berhasil atau `False` bila melanggar constraint (tangkap `sqlite3.IntegrityError`).
            """,
            """
            import sqlite3

            def sisip_aman(c, kode, harga):
                # TODO: implementasikan
                pass
            """,
            FIX1 + """
            c = sqlite3.connect(':memory:')
            c.execute('CREATE TABLE produk (id INTEGER PRIMARY KEY, kode TEXT NOT NULL UNIQUE, harga INTEGER NOT NULL CHECK (harga >= 0))')
            assert sisip_aman(c, 'A', 10) is True
            assert sisip_aman(c, 'A', 20) is False
            assert sisip_aman(c, 'B', -5) is False
            assert sisip_aman(c, None, 5) is False
            assert c.execute('SELECT COUNT(*) FROM produk').fetchone()[0] == 1
            """,
            "Bungkus INSERT dengan try dan tangkap sqlite3.IntegrityError.",
            """
            import sqlite3

            def sisip_aman(c, kode, harga):
                try:
                    c.execute('INSERT INTO produk (kode, harga) VALUES (?, ?)', (kode, harga))
                    return True
                except sqlite3.IntegrityError:
                    return False
            """,
        ),
        E(
            "A6-08-1-ex3",
            "sedang",
            """
            Tulis fungsi `buat_tabel_stok(c)` yang membuat tabel `stok` dengan `id INTEGER PRIMARY KEY`, `nama TEXT` wajib, `jumlah INTEGER` wajib berdefault 0 dan tidak negatif, serta `aktif INTEGER` wajib berdefault 1.
            """,
            """
            import sqlite3

            def buat_tabel_stok(c):
                # TODO: implementasikan
                pass
            """,
            FIX1 + """
            c = sqlite3.connect(':memory:')
            buat_tabel_stok(c)
            c.execute("INSERT INTO stok (nama) VALUES ('Pensil')")
            assert c.execute('SELECT jumlah, aktif FROM stok').fetchone() == (0, 1)
            assert _gagal(c, "INSERT INTO stok (nama, jumlah) VALUES ('X', -1)")
            assert _gagal(c, 'INSERT INTO stok (nama) VALUES (NULL)')
            assert not _gagal(c, "INSERT INTO stok (nama, jumlah, aktif) VALUES ('Y', 5, 0)")
            """,
            "Gunakan DEFAULT bersama NOT NULL dan CHECK pada jumlah.",
            """
            import sqlite3

            def buat_tabel_stok(c):
                c.execute('''
                CREATE TABLE stok (
                    id INTEGER PRIMARY KEY,
                    nama TEXT NOT NULL,
                    jumlah INTEGER NOT NULL DEFAULT 0 CHECK (jumlah >= 0),
                    aktif INTEGER NOT NULL DEFAULT 1
                )
                ''')
            """,
        ),
        E(
            "A6-08-1-ex4",
            "menantang",
            """
            Tulis fungsi `buat_tabel_nilai(c)` yang membuat tabel `nilai(siswa INTEGER, mapel TEXT, skor INTEGER)` dengan primary key gabungan `(siswa, mapel)` dan skor harus antara 0 dan 100 termasuk.
            """,
            """
            import sqlite3

            def buat_tabel_nilai(c):
                # TODO: implementasikan
                pass
            """,
            FIX1 + """
            c = sqlite3.connect(':memory:')
            buat_tabel_nilai(c)
            c.execute("INSERT INTO nilai VALUES (1, 'MTK', 90)")
            assert _gagal(c, "INSERT INTO nilai VALUES (1, 'MTK', 80)")
            assert _gagal(c, "INSERT INTO nilai VALUES (1, 'IPA', 101)")
            assert not _gagal(c, "INSERT INTO nilai VALUES (1, 'IPA', 100)")
            assert not _gagal(c, "INSERT INTO nilai VALUES (2, 'MTK', 0)")
            """,
            "Tulis PRIMARY KEY (siswa, mapel) di akhir dan CHECK dengan BETWEEN.",
            """
            import sqlite3

            def buat_tabel_nilai(c):
                c.execute('''
                CREATE TABLE nilai (
                    siswa INTEGER,
                    mapel TEXT,
                    skor INTEGER CHECK (skor BETWEEN 0 AND 100),
                    PRIMARY KEY (siswa, mapel)
                )
                ''')
            """,
        ),
    ],
    [
        M("Mengandalkan tipe kolom SQLite untuk menolak nilai aneh.", "Tambahkan CHECK untuk batas nilai."),
        M("Mengira UNIQUE menolak banyak NULL.", "Gabungkan NOT NULL UNIQUE."),
        M("Membiarkan IntegrityError mematikan program.", "Tangkap dan beri pesan yang jelas."),
    ],
    [
        Q("Constraint berfungsi?", ["Menegakkan aturan data di skema", "Mempercepat query", "Mengurutkan baris", "Menghapus duplikat lama"], 0, "Dijaga oleh basis data.", hint="Aturan."),
        Q("Pelanggaran constraint di Python menimbulkan?", ["sqlite3.IntegrityError", "ValueError", "KeyError", "Tidak ada"], 0, "IntegrityError.", hint="Integrity."),
        Q("CHECK (harga >= 0) mencegah?", ["Harga negatif", "Harga kosong", "Harga duplikat", "Harga desimal"], 0, "Kondisi harus benar.", hint="Negatif."),
        Q("Primary key gabungan berguna saat?", ["Identitas ditentukan beberapa kolom", "Tabel kosong", "Kolom bertipe teks", "Ingin mengurutkan"], 0, "Pasangan unik.", hint="Pasangan."),
        Q("Banyak NULL pada kolom UNIQUE diterima karena?", ["NULL dianggap tidak sama", "NULL dianggap nol", "Bug SQLite", "NULL dilarang"], 0, "Tidak dibandingkan sama.", hint="Tidak sama."),
    ],
    [
        "Constraint menegakkan kualitas data di pintu masuk.",
        "NOT NULL, UNIQUE, CHECK, dan DEFAULT menyatakan aturan bisnis di skema.",
        "Tangkap IntegrityError agar aplikasi tetap ramah.",
        "Primary key gabungan menjaga keunikan pasangan kolom.",
    ],
    [],
)

l2 = lesson(
    "A6-08-2",
    "Foreign key, normalisasi, dan perubahan skema",
    35,
    [
        "Mengaktifkan dan memakai foreign key untuk menjaga relasi",
        "Memilih aksi ON DELETE yang tepat",
        "Menjelaskan alasan normalisasi dan anomali data",
        "Mengubah skema dengan ALTER TABLE dan UPSERT",
    ],
    [
        T("""
        ## Menjaga relasi antar tabel

        Pada modul JOIN, kita melihat pesanan yatim: pesanan yang merujuk pelanggan yang tidak ada. Hal itu terjadi karena tidak ada yang menjaga rujukan. **Foreign key** adalah constraint yang memastikan nilai sebuah kolom selalu cocok dengan primary key di tabel lain.

        Ditulis sebagai `kategori_id INTEGER REFERENCES kategori(id)`. Dengan itu, menyisipkan barang dengan kategori yang tidak ada ditolak, dan menghapus kategori yang masih dipakai juga ditolak.
        """),
        T("""
        ## Foreign key harus diaktifkan

        Kejutan di SQLite: penegakan foreign key **mati secara bawaan** demi kompatibilitas. Aktifkan per koneksi dengan `PRAGMA foreign_keys = ON`. Pengaturan ini tidak tersimpan di berkas basis data, jadi setiap koneksi baru harus mengaturnya lagi.

        Lupa mengaktifkan PRAGMA ini adalah sumber data yatim paling umum pada aplikasi SQLite. Jadikan perintah itu bagian dari kode pembuka koneksi, bukan pekerjaan yang diingat manual.
        """),
        C(
            SETUP2 + """
            def coba(sql):
                try:
                    c.execute(sql)
                    return 'ok'
                except sqlite3.IntegrityError:
                    return 'ditolak'

            print(c.execute('PRAGMA foreign_keys').fetchone())
            print(coba("INSERT INTO barang (kode, nama, harga, kategori_id) VALUES ('X1', 'Yatim', 100, 99)"))
            c.execute('DELETE FROM barang WHERE kode = ?', ('X1',))
            c.commit()
            c.execute('PRAGMA foreign_keys = ON')
            print(c.execute('PRAGMA foreign_keys').fetchone())
            print(coba("INSERT INTO barang (kode, nama, harga, kategori_id) VALUES ('X1', 'Yatim', 100, 99)"))
            print(coba('DELETE FROM kategori WHERE id = 1'))
            print(coba('DELETE FROM kategori WHERE id = 3'))
            """,
            """
            (0,)
            ok
            (1,)
            ditolak
            ditolak
            ok
            """,
            """
            Saat foreign key mati, barang yatim lolos. Setelah diaktifkan, kategori dengan barang tidak dapat dihapus dan hanya kategori kosong yang boleh.
            """,
            filename="foreign_key.py",
        ),
        T("""
        ## Aksi ON DELETE

        Perilaku bawaan adalah menolak penghapusan induk yang masih punya anak. Alternatif lain ditulis pada definisi: `ON DELETE CASCADE` ikut menghapus anak, `ON DELETE SET NULL` mengosongkan rujukan anak, dan `ON DELETE RESTRICT` menolak tegas.

        Pilih sesuai makna bisnis. Menghapus pesanan seharusnya ikut menghapus rincian pesanan, jadi cocok `CASCADE`. Menghapus kategori sebaiknya tidak menghapus barang, jadi `SET NULL` atau penolakan lebih aman. Hati-hati dengan `CASCADE` karena satu penghapusan dapat meluas.
        """),
        C(
            """
            import sqlite3

            c = sqlite3.connect(':memory:')
            c.execute('PRAGMA foreign_keys = ON')
            c.executescript('''
            CREATE TABLE ortu (id INTEGER PRIMARY KEY);
            CREATE TABLE anak (
                id INTEGER PRIMARY KEY,
                ortu_id INTEGER REFERENCES ortu(id) ON DELETE CASCADE
            );
            INSERT INTO ortu VALUES (1), (2);
            INSERT INTO anak VALUES (1, 1), (2, 1), (3, 2);
            ''')
            c.execute('PRAGMA foreign_keys = ON')
            c.execute('DELETE FROM ortu WHERE id = 1')
            print(c.execute('SELECT id FROM anak ORDER BY id').fetchall())
            """,
            """
            [(3,)]
            """,
            """
            Menghapus induk satu ikut menghapus kedua anaknya, dan hanya anak ketiga yang tersisa.
            """,
            filename="on_delete_cascade.py",
        ),
        T("""
        ## Mengapa normalisasi

        **Normalisasi** adalah menata tabel agar setiap fakta disimpan di satu tempat. Bayangkan tabel pesanan yang menyimpan nama dan kota pelanggan di setiap baris. Bila pelanggan pindah kota, kita harus memperbarui puluhan baris, dan lupa satu saja menimbulkan data bertentangan.

        Masalah itu disebut **anomali pembaruan**. Ada pula anomali penyisipan, yaitu tidak bisa mencatat pelanggan sebelum ia memesan, dan anomali penghapusan, yaitu kehilangan data pelanggan saat pesanan terakhirnya dihapus.
        """),
        T("""
        ## Memecah tabel

        Solusinya memecah tabel menurut subjek. Data pelanggan masuk tabel `pelanggan`, data produk masuk `produk`, dan `pesanan` hanya menyimpan kunci asing ke keduanya. Setiap fakta kini tersimpan sekali, dan perubahan kota pelanggan cukup satu pembaruan.

        Aturan praktis: bila beberapa kolom hanya bergantung pada sebagian kunci, atau pada kolom non-kunci lain, pindahkan ke tabel sendiri. Untuk analitik, kadang sengaja didenormalisasi demi kecepatan, tetapi mulailah dari desain ternormalisasi.
        """),
        T("""
        ## UPSERT

        Sering kita ingin menyisipkan baris bila belum ada, atau memperbaruinya bila sudah ada. SQLite menyediakan `INSERT ... ON CONFLICT (kolom) DO UPDATE SET ...`. Bagian `excluded.kolom` merujuk nilai yang hendak disisipkan.

        Tanpa UPSERT, kita harus memeriksa dulu lalu memutuskan, yang rawan balapan antar proses. Dengan UPSERT, keputusan diambil atomik oleh basis data. Ada pula `INSERT OR IGNORE` yang diam-diam melewati baris yang melanggar constraint.
        """),
        C(
            SETUP2 + """
            q = '''
            INSERT INTO barang (kode, nama, harga) VALUES (?, ?, ?)
            ON CONFLICT (kode) DO UPDATE SET nama = excluded.nama, harga = excluded.harga
            '''
            c.execute(q, ('P1', 'Pensil 2B', 2600))
            c.execute(q, ('N1', 'Baru', 500))
            print(c.execute('SELECT kode, nama, harga FROM barang ORDER BY id').fetchall())
            print(c.execute("INSERT OR IGNORE INTO barang (kode, nama, harga) VALUES ('P1', 'Dup', 1)").rowcount)
            """,
            """
            [('P1', 'Pensil 2B', 2600), ('E1', 'Kabel', 15000), ('N1', 'Baru', 500)]
            0
            """,
            """
            Baris P1 diperbarui tanpa duplikat, N1 disisipkan baru, dan INSERT OR IGNORE melewati baris yang bentrok dengan hasil nol baris berubah.
            """,
            filename="upsert.py",
        ),
        T("""
        ## ALTER TABLE

        Skema berubah seiring waktu. `ALTER TABLE tabel ADD COLUMN kolom tipe` menambah kolom, dan baris lama mendapat nilai `DEFAULT` kolom itu atau `NULL`. SQLite juga mendukung `RENAME COLUMN`, `RENAME TO`, dan `DROP COLUMN` pada versi baru, tetapi tidak semua jenis perubahan didukung langsung.

        Untuk perubahan besar, pola aman adalah membuat tabel baru, menyalin data, menghapus tabel lama, lalu mengganti nama. Lakukan di dalam satu transaksi dan cadangkan data lebih dulu.
        """),
        K(
            "warn",
            """
            Foreign key di SQLite tidak aktif secara bawaan. Jalankan PRAGMA foreign_keys = ON di setiap koneksi baru.
            """,
            title="Aktifkan foreign key",
        ),
        T("""
        ## Transaksi menjaga konsistensi

        Perubahan yang terdiri dari beberapa langkah, seperti memindahkan stok dari satu barang ke barang lain, harus berhasil seluruhnya atau tidak sama sekali. **Transaksi** menjamin hal itu: bila satu langkah gagal, semua perubahan dibatalkan dengan `ROLLBACK`.

        Di Python, koneksi sqlite3 membuka transaksi otomatis pada perintah yang mengubah data dan baru menyimpannya saat `commit()` dipanggil. Ingat ini karena beberapa PRAGMA, termasuk `foreign_keys`, tidak berpengaruh bila dijalankan di tengah transaksi yang belum di-commit.
        """),
        T("""
        ## Nama dan konvensi

        Pilih nama tabel dan kolom yang konsisten: huruf kecil, tanpa spasi, dan memakai satu bahasa. Kunci asing biasanya dinamai `tabelinduk_id`, misalnya `kategori_id`, sehingga hubungannya langsung terbaca. Hindari singkatan yang membingungkan pembaca baru.

        Konvensi yang seragam membuat query lebih mudah ditulis dan diperiksa. Skema yang rapi adalah dokumentasi paling jujur tentang cara kerja data Anda.
        """),
        E(
            "A6-08-2-ex1",
            "mudah",
            """
            Tulis fungsi `aktifkan_fk(c)` yang mengaktifkan penegakan foreign key pada koneksi `c` dan mengembalikan nilai pengaturan itu sesudahnya (bilangan bulat).
            """,
            """
            import sqlite3

            def aktifkan_fk(c):
                # TODO: implementasikan
                pass
            """,
            FIX2 + """
            c = _db()
            assert c.execute('PRAGMA foreign_keys').fetchone()[0] == 0
            assert aktifkan_fk(c) == 1
            try:
                c.execute("INSERT INTO barang (kode, nama, harga, kategori_id) VALUES ('Z', 'Z', 1, 99)")
                ditolak = False
            except sqlite3.IntegrityError:
                ditolak = True
            assert ditolak
            """,
            "Jalankan PRAGMA foreign_keys = ON lalu baca nilainya.",
            """
            import sqlite3

            def aktifkan_fk(c):
                c.execute('PRAGMA foreign_keys = ON')
                return c.execute('PRAGMA foreign_keys').fetchone()[0]
            """,
        ),
        E(
            "A6-08-2-ex2",
            "sedang",
            """
            Tulis fungsi `hapus_kategori_aman(c, id)` yang menghapus kategori berdasarkan id dan mengembalikan `True` bila berhasil atau `False` bila ditolak oleh foreign key (tangkap `sqlite3.IntegrityError`).
            """,
            """
            import sqlite3

            def hapus_kategori_aman(c, id):
                # TODO: implementasikan
                pass
            """,
            FIX2 + """
            c = _db(True)
            assert hapus_kategori_aman(c, 1) is False
            assert c.execute('SELECT COUNT(*) FROM kategori').fetchone()[0] == 3
            assert hapus_kategori_aman(c, 3) is True
            assert c.execute('SELECT COUNT(*) FROM kategori').fetchone()[0] == 2
            assert hapus_kategori_aman(c, 2) is False
            """,
            "Bungkus DELETE dengan try dan tangkap IntegrityError.",
            """
            import sqlite3

            def hapus_kategori_aman(c, id):
                try:
                    c.execute('DELETE FROM kategori WHERE id = ?', (id,))
                    return True
                except sqlite3.IntegrityError:
                    return False
            """,
        ),
        E(
            "A6-08-2-ex3",
            "sedang",
            """
            Tulis fungsi `upsert_barang(c, kode, nama, harga)` yang menyisipkan barang baru atau memperbarui `nama` dan `harga` bila `kode` sudah ada, memakai `ON CONFLICT`.
            """,
            """
            import sqlite3

            def upsert_barang(c, kode, nama, harga):
                # TODO: implementasikan
                pass
            """,
            FIX2 + """
            c = _db()
            upsert_barang(c, 'P1', 'Pensil 2B', 2600)
            assert c.execute("SELECT nama, harga FROM barang WHERE kode = 'P1'").fetchone() == ('Pensil 2B', 2600)
            assert c.execute('SELECT COUNT(*) FROM barang').fetchone()[0] == 2
            upsert_barang(c, 'N1', 'Baru', 100)
            assert c.execute('SELECT COUNT(*) FROM barang').fetchone()[0] == 3
            upsert_barang(c, 'N1', 'Baru lagi', 150)
            assert c.execute("SELECT nama, harga FROM barang WHERE kode = 'N1'").fetchone() == ('Baru lagi', 150)
            """,
            "Pakai INSERT dengan ON CONFLICT (kode) DO UPDATE SET dan excluded.",
            """
            import sqlite3

            def upsert_barang(c, kode, nama, harga):
                q = '''
                INSERT INTO barang (kode, nama, harga) VALUES (?, ?, ?)
                ON CONFLICT (kode) DO UPDATE SET nama = excluded.nama, harga = excluded.harga
                '''
                c.execute(q, (kode, nama, harga))
            """,
        ),
        E(
            "A6-08-2-ex4",
            "menantang",
            """
            Tulis fungsi `tambah_kolom_aktif(c)` yang menambahkan kolom `aktif INTEGER NOT NULL DEFAULT 1` ke tabel `barang` lalu mengembalikan list nama kolom tabel itu sesuai urutan.
            """,
            """
            import sqlite3

            def tambah_kolom_aktif(c):
                # TODO: implementasikan
                pass
            """,
            FIX2 + """
            c = _db()
            assert tambah_kolom_aktif(c) == ['id', 'kode', 'nama', 'harga', 'kategori_id', 'aktif']
            assert [r[0] for r in c.execute('SELECT aktif FROM barang').fetchall()] == [1, 1]
            c.execute("INSERT INTO barang (kode, nama, harga) VALUES ('N1', 'Baru', 5)")
            assert c.execute("SELECT aktif FROM barang WHERE kode = 'N1'").fetchone()[0] == 1
            """,
            "Gunakan ALTER TABLE ADD COLUMN lalu baca PRAGMA table_info.",
            """
            import sqlite3

            def tambah_kolom_aktif(c):
                c.execute('ALTER TABLE barang ADD COLUMN aktif INTEGER NOT NULL DEFAULT 1')
                return [r[1] for r in c.execute('PRAGMA table_info(barang)').fetchall()]
            """,
        ),
    ],
    [
        M("Mengira foreign key aktif otomatis di SQLite.", "Jalankan PRAGMA foreign_keys = ON tiap koneksi."),
        M("Memakai CASCADE tanpa memikirkan jangkauannya.", "Pilih aksi sesuai makna bisnis."),
        M("Menyimpan data yang sama di banyak baris.", "Normalisasi agar tiap fakta satu tempat."),
    ],
    [
        Q("Foreign key menjaga?", ["Rujukan ke tabel lain tetap valid", "Urutan baris", "Kecepatan query", "Ukuran tabel"], 0, "Relasi.", hint="Rujukan."),
        Q("Pengaturan foreign key di SQLite secara bawaan?", ["Mati", "Hidup", "Acak", "Tidak ada"], 0, "Harus diaktifkan.", hint="Mati."),
        Q("ON DELETE CASCADE berarti?", ["Anak ikut terhapus", "Penghapusan ditolak", "Anak dikosongkan", "Tidak terjadi apa-apa"], 0, "Ikut hapus.", hint="Ikut."),
        Q("Normalisasi bertujuan?", ["Setiap fakta disimpan satu tempat", "Memperbesar tabel", "Menghapus kunci", "Mengurutkan data"], 0, "Menghindari anomali.", hint="Satu tempat."),
        Q("UPSERT dilakukan dengan?", ["ON CONFLICT DO UPDATE", "DROP TABLE", "SELECT DISTINCT", "LIMIT"], 0, "Sisip atau perbarui.", hint="Conflict."),
    ],
    [
        "Foreign key menjaga relasi, dan harus diaktifkan di SQLite.",
        "Pilih aksi ON DELETE sesuai makna bisnis.",
        "Normalisasi menghindari anomali pembaruan.",
        "UPSERT dan ALTER TABLE mengelola data dan skema yang berubah.",
    ],
    [],
)

l3 = lesson(
    "A6-08-3",
    "Index dan rencana eksekusi",
    35,
    [
        "Menjelaskan fungsi index dan biayanya",
        "Membuat index dan index gabungan",
        "Membaca rencana eksekusi dengan EXPLAIN QUERY PLAN",
        "Menentukan kolom yang layak diberi index",
    ],
    [
        T("""
        ## Mencari tanpa index

        Bayangkan mencari satu nama di buku telepon yang tidak terurut: Anda harus membaca halaman demi halaman. Tanpa index, basis data melakukan hal yang sama, yang disebut **table scan**: ia memeriksa setiap baris untuk menemukan yang cocok. Pada ribuan baris cepat, tetapi pada jutaan baris terasa lambat.

        **Index** adalah struktur tambahan yang terurut, mirip indeks di belakang buku. Dengan index pada kolom pencarian, basis data melompat langsung ke baris yang dicari tanpa membaca semuanya.
        """),
        T("""
        ## CREATE INDEX

        Sintaksnya `CREATE INDEX nama ON tabel (kolom)`. Setelah dibuat, basis data memakainya otomatis bila berguna, tanpa perubahan pada query. Primary key dan kolom `UNIQUE` sudah memiliki index otomatis, sehingga pencarian berdasarkan keduanya cepat sejak awal.

        Index tidak mengubah hasil query, hanya kecepatannya. Itu menjadikannya alat optimasi yang aman dicoba, asalkan kita mengukur hasilnya dan memahami biayanya.
        """),
        T("""
        ## EXPLAIN QUERY PLAN

        Untuk mengetahui apakah sebuah query memakai index, gunakan `EXPLAIN QUERY PLAN` di depan query itu. Hasilnya menjelaskan strategi: `SCAN` berarti membaca seluruh tabel, sedangkan `SEARCH ... USING INDEX` berarti memakai index untuk melompat ke baris yang cocok.

        Teks persisnya berbeda antar versi SQLite, jadi dalam kode otomatis kita memeriksa keberadaan kata `INDEX` pada kolom keterangan alih-alih mencocokkan kalimat penuh.
        """),
        C(
            SETUP3 + """
            q = 'SELECT * FROM log WHERE user_id = 5'
            print(pakai_indeks(q))
            c.execute('CREATE INDEX idx_log_user ON log (user_id)')
            print(pakai_indeks(q))
            print(c.execute('SELECT COUNT(*) FROM log WHERE user_id = 5').fetchone())
            print(pakai_indeks('SELECT * FROM log WHERE id = 5'))
            """,
            """
            False
            True
            (10,)
            False
            """,
            """
            Sebelum index, query memindai tabel. Setelah index, query memakainya dengan hasil tetap sepuluh baris. Pencarian berdasarkan id tidak memakai kata INDEX karena memakai primary key rowid langsung.
            """,
            filename="index_dasar.py",
        ),
        T("""
        ## Index gabungan

        Index dapat mencakup beberapa kolom: `CREATE INDEX idx ON log (user_id, aksi)`. Urutan kolom penting karena index terurut menurut kolom pertama, lalu kolom kedua di dalam tiap nilai kolom pertama. Aturan **awalan kiri** berlaku: index ini membantu query yang menyaring `user_id`, atau `user_id` dan `aksi`, tetapi tidak membantu query yang hanya menyaring `aksi`.

        Letakkan kolom yang paling sering disaring dengan kesamaan di depan. Satu index gabungan yang dirancang baik sering menggantikan beberapa index terpisah.
        """),
        C(
            SETUP3 + """
            c.execute('CREATE INDEX idx_log_user_aksi ON log (user_id, aksi)')
            print([r[2] for r in c.execute('PRAGMA index_info(idx_log_user_aksi)').fetchall()])
            print(pakai_indeks("SELECT * FROM log WHERE user_id = 5 AND aksi = 'b'"))
            print(pakai_indeks('SELECT * FROM log WHERE user_id = 5'))
            print(c.execute("SELECT COUNT(*) FROM log WHERE user_id = 5 AND aksi = 'b'").fetchone())
            print(c.execute("SELECT COUNT(*) FROM log WHERE user_id = 5 AND aksi = 'a'").fetchone())
            """,
            """
            ['user_id', 'aksi']
            True
            True
            (10,)
            (0,)
            """,
            """
            Index gabungan melayani query dengan kedua kolom maupun hanya kolom pertama. Pengguna lima selalu berada pada indeks ganjil sehingga seluruh sepuluh barisnya bertindakan b.
            """,
            filename="index_gabungan.py",
        ),
        T("""
        ## Biaya index

        Index tidak gratis. Ia memakan ruang penyimpanan, dan setiap `INSERT`, `UPDATE`, dan `DELETE` harus memperbarui semua index terkait sehingga penulisan melambat. Tabel dengan banyak index membaca cepat tetapi menulis lambat.

        Karena itu jangan memberi index pada setiap kolom. Beri index pada kolom yang sering muncul di `WHERE`, `JOIN`, dan `ORDER BY` pada query yang benar-benar dijalankan, lalu ukur manfaatnya.
        """),
        T("""
        ## Kapan index tidak membantu

        Index kurang berguna pada tabel kecil, karena memindai semua baris sudah cepat. Index juga sedikit membantu pada kolom dengan sedikit nilai berbeda, seperti jenis kelamin atau status aktif, karena hampir separuh tabel tetap harus dibaca.

        Pola query dapat pula menggagalkan index: membungkus kolom dengan fungsi, seperti `WHERE LOWER(email) = ...`, atau memakai `LIKE '%kata'` dengan tanda persen di depan, membuat index biasa tidak terpakai.
        """),
        T("""
        ## UNIQUE INDEX

        `CREATE UNIQUE INDEX` sekaligus mempercepat pencarian dan menegakkan keunikan. Ia setara dengan constraint `UNIQUE` tetapi dapat ditambahkan setelah tabel dibuat. Bila data yang ada sudah mengandung duplikat, pembuatannya gagal dan duplikat harus dibersihkan lebih dulu.

        Seperti `UNIQUE` biasa, banyak `NULL` tetap diterima. Gunakan ini untuk menambahkan aturan keunikan pada tabel lama tanpa membuat ulang tabelnya.
        """),
        K(
            "tip",
            """
            Ukur dulu dengan EXPLAIN QUERY PLAN sebelum dan sesudah membuat index. Index yang tidak terpakai hanya memperlambat penulisan.
            """,
            title="Ukur, jangan menebak",
        ),
        C(
            """
            import sqlite3

            c = sqlite3.connect(':memory:')
            c.execute('CREATE TABLE pengguna (id INTEGER PRIMARY KEY, email TEXT)')
            c.executemany('INSERT INTO pengguna (email) VALUES (?)', [('a@x.com',), ('b@x.com',), ('a@x.com',)])
            try:
                c.execute('CREATE UNIQUE INDEX idx_email ON pengguna (email)')
            except sqlite3.IntegrityError:
                print('ada duplikat')
            c.execute("DELETE FROM pengguna WHERE id = 3")
            c.execute('CREATE UNIQUE INDEX idx_email ON pengguna (email)')
            try:
                c.execute("INSERT INTO pengguna (email) VALUES ('b@x.com')")
            except sqlite3.IntegrityError:
                print('duplikat baru ditolak')
            print(c.execute("SELECT name FROM sqlite_master WHERE type = 'index'").fetchall())
            """,
            """
            ada duplikat
            duplikat baru ditolak
            [('idx_email',)]
            """,
            """
            Index unik gagal dibuat selama masih ada duplikat. Setelah duplikat dihapus ia berhasil dan menolak duplikat baru.
            """,
            filename="unique_index.py",
        ),
        T("""
        ## Merawat index

        Index perlu dievaluasi berkala. Query yang berubah dapat membuat index lama tidak terpakai lagi, dan index tak terpakai hanya membebani penulisan. Periksa daftar index lewat `sqlite_master`, lalu hapus yang tidak diperlukan dengan `DROP INDEX`.

        Setelah banyak perubahan data, statistik tabel dapat usang. Perintah `ANALYZE` memperbarui statistik agar perencana query memilih strategi yang tepat. Merawat index sama pentingnya dengan membuatnya.
        """),
        T("""
        ## Pola query dan index

        Rancang index dari query nyata, bukan dari kolom. Kumpulkan query yang paling sering atau paling lambat, lihat kolom di `WHERE`, `JOIN`, dan `ORDER BY`, lalu buat index yang melayani banyak query sekaligus. Index yang melayani satu query langka jarang sepadan.

        Untuk kunci asing, pertimbangkan memberi index pada kolom rujukan di tabel anak, karena JOIN dan penghapusan induk perlu mencari baris anak dengan cepat.
        """),
        E(
            "A6-08-3-ex1",
            "mudah",
            """
            Tulis fungsi `buat_indeks(c)` yang membuat index bernama `idx_log_user` pada kolom `user_id` tabel `log`.
            """,
            """
            import sqlite3

            def buat_indeks(c):
                # TODO: implementasikan
                pass
            """,
            FIX3 + """
            c = _db()
            q = 'SELECT * FROM log WHERE user_id = 5'
            assert _pakai(c, q) is False
            buat_indeks(c)
            assert _pakai(c, q) is True
            nama = [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type = 'index'").fetchall()]
            assert 'idx_log_user' in nama
            """,
            "CREATE INDEX idx_log_user ON log (user_id).",
            """
            import sqlite3

            def buat_indeks(c):
                c.execute('CREATE INDEX idx_log_user ON log (user_id)')
            """,
        ),
        E(
            "A6-08-3-ex2",
            "sedang",
            """
            Tulis fungsi `rencana_pakai_indeks(c, q)` yang menjalankan `EXPLAIN QUERY PLAN` untuk query `q` dan mengembalikan `True` bila ada langkah yang keterangannya memuat kata `INDEX`, atau `False` bila tidak.
            """,
            """
            import sqlite3

            def rencana_pakai_indeks(c, q):
                # TODO: implementasikan
                pass
            """,
            FIX3 + """
            c = _db()
            q = 'SELECT * FROM log WHERE user_id = 5'
            assert rencana_pakai_indeks(c, q) is False
            assert rencana_pakai_indeks(c, 'SELECT * FROM log WHERE id = 5') is False
            c.execute('CREATE INDEX idx_u ON log (user_id)')
            assert rencana_pakai_indeks(c, q) is True
            """,
            "Baca kolom keterangan (indeks 3) dari hasil EXPLAIN QUERY PLAN.",
            """
            import sqlite3

            def rencana_pakai_indeks(c, q):
                rows = c.execute('EXPLAIN QUERY PLAN ' + q).fetchall()
                return any('INDEX' in r[3] for r in rows)
            """,
        ),
        E(
            "A6-08-3-ex3",
            "sedang",
            """
            Tulis fungsi `buat_indeks_gabungan(c)` yang membuat index `idx_log_user_aksi` pada kolom `(user_id, aksi)` tabel `log` dan mengembalikan list nama kolom index itu sesuai urutan.
            """,
            """
            import sqlite3

            def buat_indeks_gabungan(c):
                # TODO: implementasikan
                pass
            """,
            FIX3 + """
            c = _db()
            assert buat_indeks_gabungan(c) == ['user_id', 'aksi']
            assert _pakai(c, "SELECT * FROM log WHERE user_id = 5 AND aksi = 'b'") is True
            assert c.execute("SELECT COUNT(*) FROM log WHERE user_id = 5 AND aksi = 'b'").fetchone()[0] == 10
            """,
            "Buat index lalu baca PRAGMA index_info dan ambil kolom nama.",
            """
            import sqlite3

            def buat_indeks_gabungan(c):
                c.execute('CREATE INDEX idx_log_user_aksi ON log (user_id, aksi)')
                return [r[2] for r in c.execute('PRAGMA index_info(idx_log_user_aksi)').fetchall()]
            """,
        ),
        E(
            "A6-08-3-ex4",
            "menantang",
            """
            Tulis fungsi `buat_indeks_unik(c)` yang membuat index unik bernama `idx_email` pada kolom `email` tabel `pengguna`, sehingga email ganda ditolak tetapi `NULL` berganda tetap diterima.
            """,
            """
            import sqlite3

            def buat_indeks_unik(c):
                # TODO: implementasikan
                pass
            """,
            FIX3 + """
            c = _db()
            buat_indeks_unik(c)
            assert _gagal(c, "INSERT INTO pengguna (email) VALUES ('a@x.com')")
            assert not _gagal(c, "INSERT INTO pengguna (email) VALUES ('c@x.com')")
            assert not _gagal(c, 'INSERT INTO pengguna (email) VALUES (NULL)')
            """,
            "CREATE UNIQUE INDEX idx_email ON pengguna (email).",
            """
            import sqlite3

            def buat_indeks_unik(c):
                c.execute('CREATE UNIQUE INDEX idx_email ON pengguna (email)')
            """,
        ),
    ],
    [
        M("Memberi index pada setiap kolom.", "Beri index pada kolom yang sering dipakai di WHERE dan JOIN."),
        M("Membungkus kolom ber-index dengan fungsi di WHERE.", "Bandingkan kolom apa adanya."),
        M("Menebak manfaat index tanpa mengukur.", "Periksa dengan EXPLAIN QUERY PLAN."),
    ],
    [
        Q("Index mempercepat?", ["Pencarian", "Penulisan", "Penghapusan tabel", "Pembuatan kolom"], 0, "Melompat ke baris.", hint="Cari."),
        Q("Biaya index?", ["Ruang dan penulisan lebih lambat", "Hasil query berubah", "Tabel terkunci", "Tidak ada"], 0, "Pembaruan index.", hint="Tulis."),
        Q("SCAN pada rencana berarti?", ["Membaca seluruh tabel", "Memakai index", "Query gagal", "Tabel kosong"], 0, "Tanpa index.", hint="Seluruh."),
        Q("Aturan awalan kiri berlaku pada?", ["Index gabungan", "Tabel kosong", "Foreign key", "CHECK"], 0, "Urutan kolom penting.", hint="Gabungan."),
        Q("Perintah melihat rencana query?", ["EXPLAIN QUERY PLAN", "SHOW PLAN", "DESCRIBE", "PRAGMA plan"], 0, "Diletakkan di depan query.", hint="Explain."),
    ],
    [
        "Index mempercepat pencarian tetapi menambah biaya penulisan.",
        "Index gabungan mengikuti aturan awalan kiri.",
        "EXPLAIN QUERY PLAN menunjukkan apakah index terpakai.",
        "Beri index secukupnya dan ukur manfaatnya.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perintah yang cukup jelas dalam teks.", "brief": []}

write_module(
    "A6",
    8,
    "Desain tabel, constraint, dan index",
    105,
    [
        "Merancang tabel dengan constraint yang menjaga kualitas data",
        "Menjaga relasi dengan foreign key dan memahami normalisasi",
        "Memakai index dan membaca rencana eksekusi",
    ],
    [l1, l2, l3],
    video,
    REF,
)
