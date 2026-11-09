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
    "A6-02-1",
    "WHERE dengan perbandingan dan logika",
    35,
    [
        "Menyaring baris dengan WHERE dan operator perbandingan",
        "Menggabungkan kondisi dengan AND, OR, dan NOT",
        "Menjelaskan prioritas operator dan memakai tanda kurung",
        "Menyaring dengan parameter secara aman",
    ],
    [
        T("""
        ## Menyaring baris

        Klausa `WHERE` menyaring baris: hanya baris yang kondisinya benar yang masuk ke hasil. Ia dievaluasi setelah `FROM` dan sebelum `SELECT`, jadi baris yang tersaring tidak pernah diproses lebih lanjut. Menyaring sedini mungkin adalah cara paling efektif mempercepat query pada tabel besar.

        Di modul ini kita memakai tabel pesanan sepuluh baris berisi pelanggan, kota, produk, jumlah, total, dan tanggal. Satu pesanan sengaja memiliki jumlah `NULL` untuk mengingatkan bahwa filter dan NULL punya aturan khusus.
        """),
        C(
            SETUP + """
            print(c.execute("SELECT id FROM pesanan WHERE kota = 'Jakarta'").fetchall())
            print(c.execute('SELECT id FROM pesanan WHERE total >= 100000').fetchall())
            """,
            """
            [(1,), (3,), (6,), (10,)]
            [(2,), (4,), (6,)]
            """,
            """
            Empat pesanan berasal dari Jakarta dan tiga pesanan bernilai seratus ribu atau lebih.
            """,
            filename="where_dasar.py",
        ),
        T("""
        ## Operator perbandingan

        Operator yang tersedia adalah `=`, `<>` atau `!=` untuk tidak sama, `<`, `<=`, `>`, dan `>=`. Perhatikan bahwa SQL memakai satu tanda sama dengan untuk perbandingan, bukan dua seperti di Python. Teks dibandingkan dalam tanda kutip tunggal, sedangkan tanda kutip ganda biasanya dipakai untuk nama kolom.

        Perbandingan teks bergantung pada kolasi basis data. Di SQLite perbandingan dengan `=` peka huruf besar-kecil secara default, sedangkan di MySQL biasanya tidak. Seragamkan huruf dengan `lower` bila ragu.
        """),
        T("""
        ## AND, OR, dan NOT

        Kondisi digabung dengan `AND` yang menuntut keduanya benar, `OR` yang cukup salah satu, dan `NOT` yang membalik. Kota Jakarta dengan total di atas 30.000 menghasilkan dua pesanan. Menambah `AND` mempersempit hasil sedangkan menambah `OR` memperluasnya, intuisi yang menghindari banyak kekeliruan.

        Dalam bahasa sehari-hari kita sering berkata "Jakarta dan Bandung" padahal maksudnya "Jakarta atau Bandung" karena satu baris tidak mungkin berada di dua kota sekaligus. Terjemahkan maksud ke logika dengan cermat.
        """),
        C(
            SETUP + """
            print(c.execute("SELECT id FROM pesanan WHERE kota = 'Jakarta' AND total > 30000").fetchall())
            print(c.execute("SELECT id FROM pesanan WHERE kota = 'Bandung' OR total > 100000").fetchall())
            print(c.execute("SELECT id FROM pesanan WHERE NOT kota = 'Jakarta'").fetchall())
            """,
            """
            [(6,), (10,)]
            [(2,), (4,), (5,), (6,), (9,)]
            [(2,), (4,), (5,), (7,), (8,), (9,)]
            """,
            """
            AND mempersempit hasil menjadi dua, OR memperluas menjadi lima, dan NOT mengambil semua selain Jakarta.
            """,
            filename="and_or_not.py",
        ),
        T("""
        ## Prioritas operator

        Seperti perkalian sebelum penjumlahan, `AND` dievaluasi sebelum `OR`. Kondisi `kota = 'Jakarta' OR kota = 'Bandung' AND total > 100000` dibaca sebagai Jakarta, atau Bandung yang bertotal besar, sehingga semua pesanan Jakarta ikut. Itu jarang maksud penulisnya.

        Aturan aman: selalu pakai tanda kurung bila mencampur `AND` dan `OR`. Dengan tanda kurung `(Jakarta OR Bandung) AND total > 100000` hanya dua pesanan lolos. Tanda kurung membuat maksud jelas bagi mesin dan pembaca.
        """),
        C(
            SETUP + """
            tanpa = "SELECT id FROM pesanan WHERE kota = 'Jakarta' OR kota = 'Bandung' AND total > 100000"
            dengan = "SELECT id FROM pesanan WHERE (kota = 'Jakarta' OR kota = 'Bandung') AND total > 100000"
            print(c.execute(tanpa).fetchall())
            print(c.execute(dengan).fetchall())
            """,
            """
            [(1,), (2,), (3,), (6,), (10,)]
            [(2,), (6,)]
            """,
            """
            Tanpa tanda kurung semua pesanan Jakarta ikut terpilih, sedangkan dengan tanda kurung hanya dua pesanan besar yang lolos.
            """,
            filename="prioritas.py",
        ),
        T("""
        ## NULL dan filter

        Ingat logika tiga nilai: baris yang kondisinya tidak diketahui tidak lolos `WHERE`. Pesanan 9 memiliki jumlah `NULL`, sehingga `jumlah > 2` tidak memasukkannya dan `NOT jumlah > 2` juga tidak. Kedua filter tidak saling melengkapi, dan pesanan 9 hilang dari keduanya.

        Bila ingin memasukkan baris `NULL`, tulis eksplisit dengan `OR jumlah IS NULL`. Menyadari baris yang hilang diam-diam adalah keterampilan SQL yang membedakan analis teliti dari yang ceroboh.
        """),
        C(
            SETUP + """
            besar = c.execute('SELECT id FROM pesanan WHERE jumlah > 2').fetchall()
            kecil = c.execute('SELECT id FROM pesanan WHERE NOT jumlah > 2').fetchall()
            print(besar)
            print(kecil)
            print(c.execute('SELECT id FROM pesanan WHERE jumlah IS NULL OR jumlah > 2 ORDER BY id').fetchall())
            """,
            """
            [(3,), (4,), (7,), (8,), (10,)]
            [(1,), (2,), (5,), (6,)]
            [(3,), (4,), (7,), (8,), (9,), (10,)]
            """,
            """
            Pesanan sembilan hilang dari kedua filter yang tampak saling melengkapi, dan baru muncul dengan IS NULL eksplisit.
            """,
            filename="null_filter.py",
        ),
        T("""
        ## Filter dengan parameter

        Nilai filter yang berasal dari luar, misalnya masukan pengguna, harus dikirim sebagai parameter: `WHERE kota = ?` dengan nilai pada tuple terpisah. Jangan menyusun query dengan f-string untuk nilai karena membuka celah injeksi SQL, di mana teks jahat diperlakukan sebagai bagian perintah.

        Parameter juga lebih efisien karena mesin dapat memakai ulang rencana eksekusi. Hanya nama tabel dan kolom yang tidak bisa diparameterkan, dan itu harus divalidasi terhadap daftar yang diizinkan.
        """),
        K(
            "warn",
            """
            Selalu pakai tanda kurung saat mencampur AND dan OR. Prioritas AND yang lebih tinggi sering menghasilkan filter yang berbeda dari maksud penulis.
            """,
            title="Kurung penyelamat",
        ),
        T("""
        ## Kondisi antar kolom

        Filter tidak harus membandingkan kolom dengan konstanta. Kamu dapat membandingkan dua kolom pada baris yang sama, misalnya `total > jumlah * 20000` untuk mencari pesanan dengan harga satuan di atas dua puluh ribu. Ekspresi aritmetika apa pun boleh muncul di sisi kiri maupun kanan kondisi.

        Perhatikan bahwa memakai fungsi pada kolom di sisi kiri, seperti `lower(kota) = 'jakarta'`, sering mencegah pemakaian indeks. Pada tabel besar, lebih baik menyimpan data dalam bentuk seragam daripada mengandalkan fungsi pada setiap pencarian.
        """),
        T("""
        ## Memeriksa hasil filter

        Setelah menulis filter, periksa hasilnya dengan tiga pertanyaan. Berapa banyak baris yang lolos dan apakah masuk akal? Adakah baris yang seharusnya lolos tetapi hilang, misalnya karena NULL? Adakah baris yang seharusnya tersaring tetapi lolos karena prioritas operator yang keliru?

        Cara cepat adalah membandingkan `COUNT(*)` dengan filter dan tanpa filter, atau menghitung dua filter yang seharusnya saling melengkapi dan memeriksa bahwa jumlahnya sama dengan total. Selisih menunjukkan baris yang jatuh di celah, biasanya NULL.
        """),
        E(
            "A6-02-1-ex1",
            "mudah",
            """
            Tulis fungsi `pesanan_kota(c, kota)` yang mengembalikan list `id` pesanan dari kota tertentu terurut menurut `id`, memakai parameter bertanda tanya.
            """,
            """
            import sqlite3

            def pesanan_kota(c, kota):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert pesanan_kota(c, 'Jakarta') == [1, 3, 6, 10]
            assert pesanan_kota(c, 'Medan') == [7]
            assert pesanan_kota(c, 'Bogor') == []
            c.execute("INSERT INTO pesanan VALUES (11, 'Kiki', 'Bogor', 'Buku', 1, 12000, '2026-05-01')")
            assert pesanan_kota(c, 'Bogor') == [11]
            """,
            "Pakai WHERE kota sama dengan tanda tanya dan kirim kota sebagai tuple.",
            """
            import sqlite3

            def pesanan_kota(c, kota):
                return [r[0] for r in c.execute('SELECT id FROM pesanan WHERE kota = ? ORDER BY id', (kota,)).fetchall()]
            """,
        ),
        E(
            "A6-02-1-ex2",
            "sedang",
            """
            Tulis fungsi `besar_di_kota(c, kota, minimum)` yang mengembalikan list `id` pesanan di kota itu dengan `total` lebih besar dari `minimum`, terurut menurut `id`.
            """,
            """
            import sqlite3

            def besar_di_kota(c, kota, minimum):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert besar_di_kota(c, 'Jakarta', 30000) == [6, 10]
            assert besar_di_kota(c, 'Bandung', 100000) == [2]
            assert besar_di_kota(c, 'Medan', 0) == [7]
            assert besar_di_kota(c, 'Jakarta', 1000000) == []
            """,
            "Gabungkan dua kondisi dengan AND dan dua parameter.",
            """
            import sqlite3

            def besar_di_kota(c, kota, minimum):
                q = 'SELECT id FROM pesanan WHERE kota = ? AND total > ? ORDER BY id'
                return [r[0] for r in c.execute(q, (kota, minimum)).fetchall()]
            """,
        ),
        E(
            "A6-02-1-ex3",
            "sedang",
            """
            Tulis fungsi `kota_atau_besar(c, kota, batas)` yang mengembalikan list `id` pesanan yang berasal dari kota itu ATAU bertotal lebih dari `batas`, terurut menurut `id`.
            """,
            """
            import sqlite3

            def kota_atau_besar(c, kota, batas):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert kota_atau_besar(c, 'Bandung', 100000) == [2, 4, 5, 6, 9]
            assert kota_atau_besar(c, 'Medan', 200000) == [6, 7]
            assert kota_atau_besar(c, 'Jakarta', 1000000) == [1, 3, 6, 10]
            """,
            "Pakai OR di antara kondisi kota dan kondisi total.",
            """
            import sqlite3

            def kota_atau_besar(c, kota, batas):
                q = 'SELECT id FROM pesanan WHERE kota = ? OR total > ? ORDER BY id'
                return [r[0] for r in c.execute(q, (kota, batas)).fetchall()]
            """,
        ),
        E(
            "A6-02-1-ex4",
            "menantang",
            """
            Tulis fungsi `jakbdg_besar(c, batas)` yang mengembalikan list `id` pesanan dari Jakarta atau Bandung yang bertotal lebih dari `batas`, terurut menurut `id`. Pastikan prioritas operator benar.
            """,
            """
            import sqlite3

            def jakbdg_besar(c, batas):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert jakbdg_besar(c, 100000) == [2, 6]
            assert jakbdg_besar(c, 40000) == [2, 6, 10]
            assert jakbdg_besar(c, 1000000) == []
            """,
            "Bungkus kondisi kota dengan tanda kurung sebelum AND total.",
            """
            import sqlite3

            def jakbdg_besar(c, batas):
                q = "SELECT id FROM pesanan WHERE (kota = 'Jakarta' OR kota = 'Bandung') AND total > ? ORDER BY id"
                return [r[0] for r in c.execute(q, (batas,)).fetchall()]
            """,
        ),
    ],
    [
        M("Mencampur AND dan OR tanpa tanda kurung.", "Selalu beri tanda kurung."),
        M("Menyusun filter dari input pengguna dengan f-string.", "Pakai parameter bertanda tanya."),
        M("Mengira filter dan negasinya mencakup semua baris.", "Baris NULL hilang dari keduanya."),
    ],
    [
        Q("WHERE dievaluasi?", ["Setelah FROM sebelum SELECT", "Setelah SELECT", "Setelah ORDER BY", "Terakhir"], 0, "Urutan logis.", hint="Setelah sumber."),
        Q("AND memiliki prioritas?", ["Lebih tinggi dari OR", "Lebih rendah dari OR", "Sama", "Tak ada"], 0, "Seperti kali dan tambah.", hint="Lebih tinggi."),
        Q("Operator tidak sama?", ["<> atau !=", "=!", "<=>", "=="], 0, "Standar.", hint="Tidak sama."),
        Q("Filter jumlah > 2 pada NULL?", ["Baris tidak lolos", "Lolos", "Error", "Dianggap nol"], 0, "Tidak diketahui.", hint="NULL."),
        Q("Nilai dari pengguna dikirim lewat?", ["Parameter", "f-string", "Komentar", "Nama tabel"], 0, "Cegah injeksi.", hint="Tanda tanya."),
    ],
    [
        "WHERE menyaring baris sebelum diproses lebih lanjut.",
        "AND mempersempit, OR memperluas, dan AND didahulukan.",
        "Baris NULL tidak lolos filter perbandingan dan negasinya.",
        "Parameter mencegah injeksi SQL.",
    ],
    [],
)

l2 = lesson(
    "A6-02-2",
    "IN, BETWEEN, dan LIKE",
    35,
    [
        "Menyaring dengan daftar nilai memakai IN",
        "Menyaring rentang memakai BETWEEN dan menyadari batas inklusif",
        "Mencocokkan pola teks dengan LIKE",
        "Menyaring tanggal teks dengan benar",
    ],
    [
        T("""
        ## IN untuk daftar nilai

        Operator `IN` memeriksa apakah nilai ada dalam daftar. `kota IN ('Medan', 'Surabaya')` setara dengan dua kondisi `OR` tetapi lebih ringkas dan mudah dibaca. Negasinya `NOT IN` mengambil baris yang nilainya tidak ada dalam daftar.

        Daftar nilai juga dapat berasal dari subquery, yang dibahas pada modul lain. Hati-hati dengan `NOT IN` bila daftar mengandung `NULL`: perbandingan dengan `NULL` tidak diketahui sehingga seluruh hasil bisa kosong tanpa peringatan.
        """),
        C(
            SETUP + """
            print(c.execute("SELECT id FROM pesanan WHERE kota IN ('Medan', 'Surabaya')").fetchall())
            print(c.execute("SELECT id FROM pesanan WHERE kota NOT IN ('Jakarta', 'Bandung')").fetchall())
            """,
            """
            [(4,), (7,), (8,)]
            [(4,), (7,), (8,)]
            """,
            """
            IN dan NOT IN dengan daftar yang saling melengkapi memberi tiga pesanan yang sama pada data ini.
            """,
            filename="in_daftar.py",
        ),
        T("""
        ## Daftar dinamis dengan parameter

        Bila daftar nilai berasal dari kode, kita menyusun tanda tanya sebanyak anggota daftar: `','.join('?' * n)`. Query akhirnya `WHERE kota IN (?, ?)` dengan tuple nilai sebagai parameter. Cara ini tetap aman dari injeksi karena hanya jumlah tanda tanya yang disusun dari kode, sedangkan nilai tetap dikirim terpisah.

        Daftar kosong perlu ditangani khusus: sebagian basis data menolak `IN ()`. Untuk daftar kosong, hasil yang benar secara logika adalah himpunan kosong, sehingga fungsi dapat langsung mengembalikan list kosong.
        """),
        T("""
        ## BETWEEN dan batas inklusif

        `total BETWEEN 20000 AND 50000` setara dengan `total >= 20000 AND total <= 50000`: kedua batas termasuk. Ini berbeda dari konvensi setengah terbuka yang sering dipakai dalam pemrograman. Pesanan dengan total tepat 20000 dan tepat 50000 sama-sama lolos.

        Karena inklusif, hati-hati saat membagi rentang menjadi potongan yang berurutan. Nilai di batas bersama muncul di dua potongan bila memakai `BETWEEN` untuk keduanya. Untuk potongan berurutan, pakai `>=` dan `<` agar tidak tumpang tindih.
        """),
        C(
            SETUP + """
            print(c.execute('SELECT id FROM pesanan WHERE total BETWEEN 20000 AND 50000').fetchall())
            print(c.execute('SELECT id FROM pesanan WHERE total >= 20000 AND total <= 50000').fetchall())
            """,
            """
            [(1,), (3,), (7,), (8,), (9,), (10,)]
            [(1,), (3,), (7,), (8,), (9,), (10,)]
            """,
            """
            BETWEEN sama dengan pasangan lebih-besar-sama dan kurang-dari-sama, dan pesanan bertotal tepat batas ikut lolos.
            """,
            filename="between.py",
        ),
        T("""
        ## Tanggal sebagai teks

        SQLite tidak memiliki tipe tanggal khusus. Tanggal disimpan sebagai teks berformat `YYYY-MM-DD`, dan format ini istimewa karena urutan abjad sama dengan urutan kronologis. Karena itu `BETWEEN '2026-02-01' AND '2026-02-28'` bekerja dengan benar untuk menyaring bulan Februari.

        Format lain seperti `DD/MM/YYYY` merusak sifat ini karena urutan abjad tidak lagi kronologis. Selalu simpan tanggal dalam format ISO. Basis data lain memiliki tipe `DATE` dan `TIMESTAMP` asli dengan fungsi tanggal lengkap.
        """),
        C(
            SETUP + """
            print(c.execute("SELECT id FROM pesanan WHERE tanggal BETWEEN '2026-02-01' AND '2026-02-28'").fetchall())
            print(c.execute("SELECT id FROM pesanan WHERE tanggal >= '2026-03-01' AND tanggal < '2026-04-01'").fetchall())
            """,
            """
            [(3,), (4,), (5,)]
            [(6,), (7,), (8,)]
            """,
            """
            Format ISO membuat perbandingan teks sama dengan perbandingan kronologis untuk bulan Februari dan Maret.
            """,
            filename="tanggal_iso.py",
        ),
        T("""
        ## LIKE untuk pola teks

        `LIKE` mencocokkan teks dengan pola. Tanda persen mewakili nol atau lebih karakter apa pun, dan garis bawah mewakili tepat satu karakter. `LIKE 'A%'` mencocokkan teks berawalan A, `LIKE '%a'` berakhiran a, `LIKE '%en%'` mengandung en, dan `LIKE '_o%'` berhuruf kedua o.

        Di SQLite `LIKE` tidak peka huruf besar-kecil untuk huruf ASCII, sedangkan PostgreSQL memakai `ILIKE` untuk itu dan `LIKE` peka huruf. Untuk pencocokan yang kompleks, tersedia ekspresi reguler, tetapi LIKE cukup untuk kebanyakan kebutuhan sehari-hari.
        """),
        C(
            SETUP + """
            for pola in ('%a', 'A%', '_o%', 'a%'):
                print(pola, c.execute('SELECT pelanggan FROM pesanan WHERE pelanggan LIKE ? ORDER BY id', (pola,)).fetchall())
            """,
            """
            %a [('Citra',), ('Gita',)]
            A% [('Ani',)]
            _o% [('Joko',)]
            a% [('Ani',)]
            """,
            """
            Pola huruf kecil a persen tetap cocok dengan Ani karena LIKE di SQLite tidak peka huruf besar-kecil.
            """,
            filename="like.py",
        ),
        T("""
        ## Karakter khusus dan performa

        Bila teks yang dicari mengandung tanda persen atau garis bawah literal, gunakan `ESCAPE`: `LIKE '50\\%%' ESCAPE '\\'`. Tanpa itu karakter tersebut ditafsirkan sebagai wildcard dan hasilnya mengejutkan.

        Soal performa: pola berawalan teks tetap seperti `'Ani%'` dapat memanfaatkan indeks, sedangkan pola berawalan wildcard seperti `'%ani'` memaksa pemindaian seluruh tabel. Untuk pencarian teks besar, basis data menyediakan indeks pencarian teks penuh khusus.
        """),
        K(
            "tip",
            """
            Simpan tanggal dalam format ISO YYYY-MM-DD. Urutan abjadnya sama dengan urutan waktu sehingga BETWEEN dan ORDER BY bekerja benar.
            """,
            title="Tanggal ISO",
        ),
        T("""
        ## Memilih antara IN dan OR

        Secara hasil, `IN` dan rangkaian `OR` setara, jadi pilihan murni soal keterbacaan dan pemeliharaan. Daftar sepuluh kota terbaca jauh lebih jelas dengan `IN` daripada sepuluh kondisi `OR`. Untuk daftar yang sangat panjang, simpan nilai dalam tabel tersendiri lalu gabungkan, daripada menulis ribuan nilai langsung di query.

        Mesin basis data modern mengoptimalkan keduanya dengan baik, sehingga tidak perlu khawatir soal kecepatan pada daftar pendek. Fokuskan perhatian pada kebenaran logika dan pada penanganan NULL.
        """),
        T("""
        ## Kombinasi pola dan rentang

        Dalam praktik, filter jarang berdiri sendiri. Pencarian pelanggan bernama berawalan tertentu pada rentang tanggal tertentu dari kota tertentu menggabungkan `LIKE`, `BETWEEN`, dan `IN` dengan `AND`. Tulis tiap kondisi pada baris terpisah dengan indentasi rapi agar mudah dibaca dan diubah.

        Uji tiap kondisi satu per satu sebelum menggabungkannya. Menghitung banyak baris setelah menambah tiap kondisi memperlihatkan seberapa besar pengaruh masing-masing, dan membantu menemukan kondisi yang salah ketik atau terlalu ketat.
        """),
        E(
            "A6-02-2-ex1",
            "mudah",
            """
            Tulis fungsi `di_kota_daftar(c, daftar)` yang mengembalikan list `id` pesanan dengan kota di dalam `daftar`, terurut menurut `id`. Untuk daftar kosong kembalikan list kosong.
            """,
            """
            import sqlite3

            def di_kota_daftar(c, daftar):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert di_kota_daftar(c, ['Medan', 'Surabaya']) == [4, 7, 8]
            assert di_kota_daftar(c, ['Jakarta']) == [1, 3, 6, 10]
            assert di_kota_daftar(c, []) == []
            assert di_kota_daftar(c, ['Bogor']) == []
            """,
            "Susun tanda tanya sebanyak anggota daftar dan kirim daftar sebagai parameter.",
            """
            import sqlite3

            def di_kota_daftar(c, daftar):
                if not daftar:
                    return []
                ph = ','.join('?' * len(daftar))
                q = f'SELECT id FROM pesanan WHERE kota IN ({ph}) ORDER BY id'
                return [r[0] for r in c.execute(q, tuple(daftar)).fetchall()]
            """,
        ),
        E(
            "A6-02-2-ex2",
            "sedang",
            """
            Tulis fungsi `rentang_total(c, lo, hi)` yang mengembalikan list `id` pesanan dengan `total` antara `lo` dan `hi` inklusif, terurut menurut `id`, memakai `BETWEEN`.
            """,
            """
            import sqlite3

            def rentang_total(c, lo, hi):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert rentang_total(c, 20000, 50000) == [1, 3, 7, 8, 9, 10]
            assert rentang_total(c, 12000, 12000) == [5]
            assert rentang_total(c, 400000, 500000) == []
            assert rentang_total(c, 0, 25000) == [1, 3, 5, 7]
            """,
            "Pakai BETWEEN dengan dua parameter.",
            """
            import sqlite3

            def rentang_total(c, lo, hi):
                q = 'SELECT id FROM pesanan WHERE total BETWEEN ? AND ? ORDER BY id'
                return [r[0] for r in c.execute(q, (lo, hi)).fetchall()]
            """,
        ),
        E(
            "A6-02-2-ex3",
            "sedang",
            """
            Tulis fungsi `tanggal_antara(c, awal, akhir)` yang mengembalikan list `id` pesanan dengan `tanggal` dari `awal` sampai `akhir` inklusif (teks ISO), terurut menurut `id`.
            """,
            """
            import sqlite3

            def tanggal_antara(c, awal, akhir):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert tanggal_antara(c, '2026-02-01', '2026-02-28') == [3, 4, 5]
            assert tanggal_antara(c, '2026-03-01', '2026-03-31') == [6, 7, 8]
            assert tanggal_antara(c, '2027-01-01', '2027-12-31') == []
            assert tanggal_antara(c, '2026-01-05', '2026-01-05') == [1]
            """,
            "Bandingkan teks tanggal dengan BETWEEN dua parameter.",
            """
            import sqlite3

            def tanggal_antara(c, awal, akhir):
                q = 'SELECT id FROM pesanan WHERE tanggal BETWEEN ? AND ? ORDER BY id'
                return [r[0] for r in c.execute(q, (awal, akhir)).fetchall()]
            """,
        ),
        E(
            "A6-02-2-ex4",
            "menantang",
            """
            Tulis fungsi `nama_pola(c, pola)` yang mengembalikan list nama `pelanggan` yang cocok dengan pola `LIKE`, terurut menurut `id`.
            """,
            """
            import sqlite3

            def nama_pola(c, pola):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert nama_pola(c, '%a') == ['Citra', 'Gita']
            assert nama_pola(c, 'A%') == ['Ani']
            assert nama_pola(c, '_o%') == ['Joko']
            assert nama_pola(c, '%i') == ['Ani', 'Budi', 'Dewi', 'Hadi']
            assert nama_pola(c, 'Z%') == []
            """,
            "Pakai LIKE dengan pola sebagai parameter.",
            """
            import sqlite3

            def nama_pola(c, pola):
                q = 'SELECT pelanggan FROM pesanan WHERE pelanggan LIKE ? ORDER BY id'
                return [r[0] for r in c.execute(q, (pola,)).fetchall()]
            """,
        ),
    ],
    [
        M("Mengira BETWEEN tidak mencakup batas atas.", "BETWEEN inklusif di kedua ujung."),
        M("Menyimpan tanggal dalam format DD/MM/YYYY.", "Pakai ISO YYYY-MM-DD."),
        M("Memakai NOT IN pada daftar yang mungkin berisi NULL.", "Buang NULL dari daftar atau pakai NOT EXISTS."),
    ],
    [
        Q("BETWEEN a AND b?", ["Inklusif kedua ujung", "Eksklusif", "Hanya atas", "Hanya bawah"], 0, "Sama dengan >= dan <=.", hint="Inklusif."),
        Q("Wildcard banyak karakter?", ["%", "_", "*", "?"], 0, "Persen.", hint="Persen."),
        Q("Wildcard satu karakter?", ["_", "%", "#", "."], 0, "Garis bawah.", hint="Satu."),
        Q("Format tanggal teks yang aman diurutkan?", ["YYYY-MM-DD", "DD/MM/YYYY", "MM-DD-YY", "D M Y"], 0, "ISO.", hint="Tahun dulu."),
        Q("LIKE pada pola berawalan wildcard?", ["Lambat karena pemindaian penuh", "Cepat dengan indeks", "Error", "Kosong"], 0, "Tidak bisa pakai indeks.", hint="Awalan."),
    ],
    [
        "IN meringkas banyak kondisi OR dan harus berhati-hati dengan NULL.",
        "BETWEEN inklusif di kedua ujung.",
        "Tanggal ISO membuat perbandingan teks sama dengan kronologis.",
        "LIKE memakai persen dan garis bawah sebagai wildcard.",
    ],
    [],
)

l3 = lesson(
    "A6-02-3",
    "ORDER BY, LIMIT, dan halaman",
    35,
    [
        "Mengurutkan hasil dengan ORDER BY naik dan turun",
        "Mengurutkan berdasarkan beberapa kolom",
        "Mengambil sebagian hasil dengan LIMIT dan OFFSET",
        "Menangani posisi NULL dan urutan seri",
    ],
    [
        T("""
        ## Hasil tanpa urutan

        Tabel relasional adalah himpunan baris, dan himpunan tidak memiliki urutan. Tanpa `ORDER BY`, urutan hasil tidak dijamin walaupun tampaknya konsisten. Mesin basis data bebas mengembalikan baris dalam urutan apa pun yang paling efisien, dan urutan itu bisa berubah setelah data atau indeks berubah.

        Karena itu, setiap kali urutan penting, misalnya untuk menampilkan peringkat atau mengambil lima teratas, tulis `ORDER BY` secara eksplisit. Jangan pernah mengandalkan urutan sisipan atau urutan kunci primer yang kebetulan tampak benar.
        """),
        C(
            SETUP + """
            print(c.execute('SELECT id, total FROM pesanan ORDER BY total DESC').fetchall())
            print(c.execute('SELECT id FROM pesanan ORDER BY total DESC LIMIT 3').fetchall())
            """,
            """
            [(6, 300000.0), (2, 150000.0), (4, 105000.0), (8, 50000.0), (10, 48000.0), (9, 35000.0), (3, 25000.0), (1, 24000.0), (7, 20000.0), (5, 12000.0)]
            [(6,), (2,), (4,)]
            """,
            """
            Urutan menurun menempatkan pesanan terbesar pertama, dan LIMIT tiga mengambil tiga teratas.
            """,
            filename="order_limit.py",
        ),
        T("""
        ## ASC, DESC, dan banyak kolom

        `ORDER BY kolom` mengurutkan naik secara default, atau tulis `ASC`. Tambahkan `DESC` untuk menurun. Beberapa kolom dipisah koma: kolom pertama menentukan urutan utama dan kolom berikutnya hanya memutus seri. `ORDER BY kota, total DESC` mengelompokkan menurut kota abjad lalu total terbesar dulu di tiap kota.

        Tiap kolom punya arah sendiri, sehingga kombinasi naik dan turun mudah ditulis. Urutan penulisan kolom penting: menukarnya mengubah hasil secara mendasar.
        """),
        C(
            SETUP + """
            print(c.execute('SELECT id FROM pesanan ORDER BY kota, total DESC').fetchall())
            """,
            """
            [(2,), (9,), (5,), (6,), (10,), (3,), (1,), (7,), (4,), (8,)]
            """,
            """
            Pesanan dikelompokkan menurut kota secara abjad, dan di tiap kota diurutkan dari total terbesar.
            """,
            filename="order_banyak.py",
        ),
        T("""
        ## Memutus seri

        Bila beberapa baris memiliki nilai urutan sama, urutan di antara mereka tidak dijamin. Pesanan 2 dan 6 sama-sama memiliki harga satuan 150.000, sehingga `ORDER BY satuan DESC LIMIT 3` bisa mengambil salah satunya secara tidak terduga dan hasilnya bisa berubah antar eksekusi.

        Solusinya menambahkan kolom pemutus seri yang unik, biasanya kunci primer: `ORDER BY satuan DESC, id`. Dengan begitu urutan menjadi deterministik, sifat yang wajib untuk hasil yang dapat direproduksi dan untuk halaman yang konsisten.
        """),
        C(
            SETUP + """
            q = 'SELECT id, total / jumlah AS satuan FROM pesanan ORDER BY satuan DESC, id LIMIT 3'
            print(c.execute(q).fetchall())
            """,
            """
            [(2, 150000.0), (6, 150000.0), (4, 35000.0)]
            """,
            """
            Penambahan id sebagai pemutus seri membuat pesanan dua dan enam selalu muncul dalam urutan yang sama.
            """,
            filename="pemutus_seri.py",
        ),
        T("""
        ## Posisi NULL

        Di mana `NULL` berada dalam urutan? SQLite menganggapnya paling kecil sehingga ia muncul pertama pada urutan naik dan terakhir pada urutan turun. PostgreSQL justru menganggapnya paling besar. Basis data modern menyediakan `NULLS FIRST` dan `NULLS LAST` untuk mengaturnya secara eksplisit.

        Di SQLite kita meniru dengan mengurutkan lebih dulu berdasarkan ekspresi `kolom IS NULL`, yang bernilai nol untuk baris berisi dan satu untuk `NULL`. Dengan begitu `NULL` selalu jatuh di akhir apa pun arah urutan kolom aslinya.
        """),
        C(
            SETUP + """
            print(c.execute('SELECT id, jumlah FROM pesanan ORDER BY jumlah, id LIMIT 4').fetchall())
            q = 'SELECT id FROM pesanan ORDER BY jumlah IS NULL, jumlah DESC, id'
            print([r[0] for r in c.execute(q).fetchall()])
            """,
            """
            [(9, None), (2, 1), (5, 1), (1, 2)]
            [8, 3, 7, 10, 4, 1, 6, 2, 5, 9]
            """,
            """
            NULL muncul pertama pada urutan naik, dan ekspresi IS NULL memindahkannya ke akhir pada urutan turun.
            """,
            filename="nulls_last.py",
        ),
        T("""
        ## LIMIT dan OFFSET

        `LIMIT n` membatasi hasil menjadi paling banyak `n` baris, dan `OFFSET m` melewati `m` baris pertama. Keduanya bersama membentuk **halaman**: halaman nomor `p` berukuran `u` memakai `LIMIT u OFFSET (p - 1) * u`. Tanpa `ORDER BY` deterministik, halaman bisa saling tumpang tindih atau melewatkan baris.

        Untuk tabel sangat besar, `OFFSET` besar lambat karena mesin tetap membaca dan membuang semua baris yang dilewati. Alternatif adalah paginasi kunci: ambil baris dengan `id` lebih besar dari id terakhir halaman sebelumnya.
        """),
        C(
            SETUP + """
            for p in (1, 2, 4, 5):
                q = 'SELECT id FROM pesanan ORDER BY id LIMIT 3 OFFSET ?'
                print(p, [r[0] for r in c.execute(q, ((p - 1) * 3,)).fetchall()])
            """,
            """
            1 [1, 2, 3]
            2 [4, 5, 6]
            4 [10]
            5 []
            """,
            """
            Halaman keempat hanya berisi satu baris sisa dan halaman kelima kosong.
            """,
            filename="halaman.py",
        ),
        T("""
        ## Top N dan pemakaiannya

        Pola `ORDER BY ... DESC LIMIT n` adalah cara standar mengambil n teratas: lima produk terlaris, sepuluh pelanggan terbesar, atau tiga pesanan terbaru. Pola ini sangat umum di laporan dan dasbor.

        Waspadai seri pada batas. Bila peringkat kelima dan keenam bernilai sama, `LIMIT 5` memotong salah satunya secara sewenang-wenang. Jika seri penting, gunakan fungsi window peringkat yang dibahas pada modul tersendiri atau tentukan aturan pemutus seri secara eksplisit.
        """),
        K(
            "tip",
            """
            Setiap query dengan LIMIT harus punya ORDER BY dengan pemutus seri unik, jika tidak hasilnya tidak deterministik.
            """,
            title="LIMIT butuh urutan",
        ),
        T("""
        ## Mengurutkan dengan ekspresi dan alias

        `ORDER BY` boleh memakai ekspresi, bukan hanya nama kolom: `ORDER BY total / jumlah` mengurutkan menurut harga satuan. Alias yang dibuat di `SELECT` juga dikenali di `ORDER BY` karena `ORDER BY` dievaluasi setelah `SELECT`, berbeda dari `WHERE`. Posisi kolom dengan angka seperti `ORDER BY 2` juga diizinkan tetapi rapuh.

        Hindari memakai angka posisi dalam query yang akan dipelihara lama. Perubahan urutan kolom di `SELECT` diam-diam mengubah urutan hasil tanpa pesan kesalahan.
        """),
        T("""
        ## Menguji urutan dan halaman

        Untuk memastikan paginasi benar, uji tiga sifat. Gabungan semua halaman harus sama dengan hasil lengkap, tidak ada baris yang muncul di dua halaman, dan tidak ada baris yang terlewat. Uji juga halaman terakhir yang berisi lebih sedikit baris serta halaman di luar rentang yang harus kosong.

        Bila data berubah saat pengguna menelusuri halaman, offset bisa menggeser baris. Paginasi berbasis kunci lebih tahan terhadap perubahan karena mengacu pada nilai kunci terakhir, bukan posisi.
        """),
        E(
            "A6-02-3-ex1",
            "mudah",
            """
            Tulis fungsi `terbesar(c, n)` yang mengembalikan list `id` `n` pesanan dengan `total` terbesar, dari terbesar ke terkecil.
            """,
            """
            import sqlite3

            def terbesar(c, n):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert terbesar(c, 3) == [6, 2, 4]
            assert terbesar(c, 1) == [6]
            assert terbesar(c, 0) == []
            assert terbesar(c, 20) == [6, 2, 4, 8, 10, 9, 3, 1, 7, 5]
            """,
            "Urutkan total menurun lalu batasi dengan LIMIT dan parameter.",
            """
            import sqlite3

            def terbesar(c, n):
                q = 'SELECT id FROM pesanan ORDER BY total DESC LIMIT ?'
                return [r[0] for r in c.execute(q, (n,)).fetchall()]
            """,
        ),
        E(
            "A6-02-3-ex2",
            "sedang",
            """
            Tulis fungsi `halaman(c, nomor, ukuran)` yang mengembalikan list `id` pesanan pada halaman `nomor` (mulai dari 1) berukuran `ukuran`, terurut menurut `id`, memakai `LIMIT` dan `OFFSET`.
            """,
            """
            import sqlite3

            def halaman(c, nomor, ukuran):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert halaman(c, 1, 3) == [1, 2, 3]
            assert halaman(c, 2, 3) == [4, 5, 6]
            assert halaman(c, 4, 3) == [10]
            assert halaman(c, 5, 3) == []
            assert halaman(c, 1, 20) == list(range(1, 11))
            """,
            "Hitung offset dari nomor dan ukuran lalu pakai LIMIT dan OFFSET.",
            """
            import sqlite3

            def halaman(c, nomor, ukuran):
                q = 'SELECT id FROM pesanan ORDER BY id LIMIT ? OFFSET ?'
                return [r[0] for r in c.execute(q, (ukuran, (nomor - 1) * ukuran)).fetchall()]
            """,
        ),
        E(
            "A6-02-3-ex3",
            "sedang",
            """
            Tulis fungsi `urut_kota_total(c)` yang mengembalikan list `id` semua pesanan terurut menurut `kota` abjad, lalu `total` menurun, lalu `id`.
            """,
            """
            import sqlite3

            def urut_kota_total(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert urut_kota_total(c) == [2, 9, 5, 6, 10, 3, 1, 7, 4, 8]
            c.execute("INSERT INTO pesanan VALUES (11, 'Kiki', 'Bandung', 'Buku', 1, 200000, '2026-05-01')")
            assert urut_kota_total(c) == [11, 2, 9, 5, 6, 10, 3, 1, 7, 4, 8]
            c.execute("INSERT INTO pesanan VALUES (12, 'Lia', 'Aceh', 'Tas', 1, 1000, '2026-05-02')")
            assert urut_kota_total(c)[0] == 12
            """,
            "Tulis tiga kunci urutan dengan arah masing-masing.",
            """
            import sqlite3

            def urut_kota_total(c):
                return [r[0] for r in c.execute('SELECT id FROM pesanan ORDER BY kota, total DESC, id').fetchall()]
            """,
        ),
        E(
            "A6-02-3-ex4",
            "menantang",
            """
            Tulis fungsi `jumlah_terbesar_null_akhir(c)` yang mengembalikan list `id` semua pesanan terurut menurut `jumlah` menurun, dengan `jumlah` `NULL` di akhir dan seri diputus menurut `id`.
            """,
            """
            import sqlite3

            def jumlah_terbesar_null_akhir(c):
                # TODO: implementasikan
                pass
            """,
            FIX + """
            c = _db()
            assert jumlah_terbesar_null_akhir(c) == [8, 3, 7, 10, 4, 1, 6, 2, 5, 9]
            c.execute('UPDATE pesanan SET jumlah = NULL WHERE id = 8')
            assert jumlah_terbesar_null_akhir(c) == [3, 7, 10, 4, 1, 6, 2, 5, 8, 9]
            c.execute('UPDATE pesanan SET jumlah = 99 WHERE id = 9')
            assert jumlah_terbesar_null_akhir(c) == [9, 3, 7, 10, 4, 1, 6, 2, 5, 8]
            """,
            "Urutkan lebih dulu menurut ekspresi jumlah IS NULL lalu jumlah menurun lalu id.",
            """
            import sqlite3

            def jumlah_terbesar_null_akhir(c):
                q = 'SELECT id FROM pesanan ORDER BY jumlah IS NULL, jumlah DESC, id'
                return [r[0] for r in c.execute(q).fetchall()]
            """,
        ),
    ],
    [
        M("Mengandalkan urutan hasil tanpa ORDER BY.", "Selalu tulis ORDER BY bila urutan penting."),
        M("Memakai LIMIT tanpa pemutus seri unik.", "Tambahkan id di akhir ORDER BY."),
        M("Mengira NULL selalu di akhir urutan.", "Posisi NULL bergantung basis data, atur eksplisit."),
    ],
    [
        Q("Tanpa ORDER BY urutan hasil?", ["Tidak dijamin", "Selalu menurut id", "Menurut abjad", "Acak murni"], 0, "Himpunan tak berurut.", hint="Tak dijamin."),
        Q("Halaman p berukuran u memakai OFFSET?", ["(p-1)*u", "p*u", "p+u", "u"], 0, "Lewati halaman sebelumnya.", hint="Dikurangi satu."),
        Q("Kolom kedua pada ORDER BY berfungsi?", ["Memutus seri", "Menggantikan kolom pertama", "Mengurutkan ulang semua", "Tak berfungsi"], 0, "Pemutus seri.", hint="Seri."),
        Q("NULL pada SQLite urutan naik?", ["Pertama", "Terakhir", "Dibuang", "Nol"], 0, "Dianggap terkecil.", hint="Terkecil."),
        Q("OFFSET besar pada tabel besar?", ["Lambat", "Cepat", "Gagal", "Tak berefek"], 0, "Tetap membaca baris yang dilewati.", hint="Dibuang."),
    ],
    [
        "ORDER BY wajib bila urutan penting karena tabel tak berurutan.",
        "Beberapa kolom urutan memutus seri secara berurutan.",
        "LIMIT dan OFFSET membentuk halaman dengan urutan deterministik.",
        "Posisi NULL dalam urutan harus diatur eksplisit.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perintah yang cukup jelas dalam teks.", "brief": []}

write_module(
    "A6",
    2,
    "Filter, urutan, dan limit",
    105,
    [
        "Menyaring baris dengan WHERE, IN, BETWEEN, dan LIKE",
        "Mengurutkan dengan ORDER BY dan memutus seri",
        "Membuat halaman dengan LIMIT dan OFFSET",
    ],
    [l1, l2, l3],
    video,
    REF,
)
