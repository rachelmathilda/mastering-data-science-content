import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []


def J(prefix, body):
    return prefix.strip('\n') + '\n\n' + textwrap.dedent(body).strip('\n')

DIFF_CODE = """
def diff_baris(a, b):
    x, y = a.splitlines(), b.splitlines()
    n, m = len(x), len(y)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            if x[i] == y[j]:
                dp[i][j] = dp[i + 1][j + 1] + 1
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j + 1])
    hasil = []
    i = j = 0
    while i < n and j < m:
        if x[i] == y[j]:
            hasil.append((' ', x[i]))
            i += 1
            j += 1
        elif dp[i + 1][j] >= dp[i][j + 1]:
            hasil.append(('-', x[i]))
            i += 1
        else:
            hasil.append(('+', y[j]))
            j += 1
    hasil += [('-', t) for t in x[i:]]
    hasil += [('+', t) for t in y[j:]]
    return hasil
"""

l1 = lesson(
    "A7-01-1",
    "Mengapa version control",
    35,
    [
        "Menjelaskan masalah pengelolaan versi file secara manual",
        "Membedakan penyimpanan snapshot dan perbedaan antar versi",
        "Menghitung diff baris sederhana antara dua versi teks",
        "Menjelaskan manfaat riwayat bagi analisis data dan kerja tim",
    ],
    [
        T("""
        ## Masalah file_final_v2_benar

        Hampir semua orang pernah punya folder berisi `laporan.docx`, `laporan_final.docx`, `laporan_final_v2.docx`, dan `laporan_final_v2_benar.docx`. Cara ini bekerja sampai kita lupa mana yang terbaru, mana yang dikirim ke atasan, dan apa persisnya yang berubah di antara keduanya.

        Pada analisis data masalahnya lebih serius. Sebuah angka di laporan berasal dari skrip tertentu pada versi tertentu dan data tertentu. Bila skrip berubah tanpa catatan, kita tidak dapat menjelaskan mengapa angka bulan lalu berbeda dari angka hari ini.
        """),
        T("""
        ## Apa itu version control

        **Version control**, atau sistem kendali versi, adalah alat yang mencatat setiap perubahan pada sekumpulan file dari waktu ke waktu. Ia menjawab pertanyaan dasar: siapa mengubah apa, kapan, dan mengapa. Ia juga memungkinkan kita kembali ke keadaan mana pun di masa lalu tanpa menyalin folder secara manual.

        Git adalah sistem kendali versi yang paling banyak dipakai saat ini. Course ini memakai Git sebagai contoh, tetapi gagasan yang dipelajari berlaku untuk hampir semua sistem serupa.
        """),
        T("""
        ## Riwayat sebagai daftar snapshot

        Cara paling sederhana memahami riwayat adalah sebagai daftar **snapshot**, yaitu salinan lengkap seluruh isi pada satu saat. Setiap kali menyimpan, kita menambahkan snapshot baru ke ujung daftar. Versi ke-3 berarti snapshot ketiga, dan kembali ke masa lalu berarti mengambil elemen lama dari daftar.

        Model ini tampak boros karena banyak file tidak berubah antar snapshot. Nanti kita lihat bahwa Git memecahkan pemborosan itu dengan cara cerdas, tanpa mengubah gagasan dasarnya.
        """),
        C(
            """
            riwayat = []

            def simpan(isi):
                riwayat.append(isi)
                return len(riwayat)

            print(simpan('judul v1'))
            print(simpan('judul v2'))
            print(simpan('judul v3'))
            print(riwayat[0])
            print(riwayat[-1])
            """,
            """
            1
            2
            3
            judul v1
            judul v3
            """,
            """
            Setiap penyimpanan menambah snapshot dan mengembalikan nomor versinya. Versi lama tetap utuh dan dapat diambil kapan saja.
            """,
            filename="riwayat_snapshot.py",
        ),
        T("""
        ## Diff: apa yang berubah

        Snapshot menjawab keadaan pada suatu saat, tetapi sering kita ingin tahu **apa yang berubah** di antara dua snapshot. Itulah **diff**: daftar baris yang ditambah dan dihapus. Diff adalah bahasa kerja sehari-hari para pengembang, karena ulasan kode dan penyelidikan bug selalu dimulai dari pertanyaan apa yang berubah.

        Diff paling sederhana membandingkan himpunan baris. Baris yang ada di versi baru tetapi tidak di versi lama adalah tambahan, dan sebaliknya adalah penghapusan.
        """),
        C(
            """
            a = 'x\\ny\\nz'
            b = 'x\\nz\\nw'
            sa = set(a.splitlines())
            sb = set(b.splitlines())
            print(sorted(sb - sa))
            print(sorted(sa - sb))
            """,
            """
            ['w']
            ['y']
            """,
            """
            Baris w ditambahkan dan baris y dihapus. Pendekatan himpunan cepat tetapi mengabaikan urutan dan baris yang berulang.
            """,
            filename="diff_himpunan.py",
        ),
        T("""
        ## Diff yang menghormati urutan

        Pendekatan himpunan gagal bila baris berpindah tempat atau muncul berulang. Diff sungguhan mencari **subsekuens persekutuan terpanjang**, atau LCS: urutan baris terpanjang yang muncul di kedua versi dengan urutan sama. Baris di luar LCS dianggap ditambah atau dihapus.

        LCS dihitung dengan pemrograman dinamis. Ide ini sama dengan yang dipakai alat `diff` klasik. Memahaminya membantu kita membaca keluaran Git dengan yakin, bukan sekadar menghafal tanda plus dan minus.
        """),
        C(
            J(DIFF_CODE, """
            for r in diff_baris('x\\ny\\nz', 'x\\nz\\nw'):
                print(r)
            """),
            """
            (' ', 'x')
            ('-', 'y')
            (' ', 'z')
            ('+', 'w')
            """,
            """
            Baris x dan z tetap, y dihapus, dan w ditambahkan di akhir. Tanda spasi menandai baris yang tidak berubah.
            """,
            filename="diff_lcs.py",
        ),
        T("""
        ## Snapshot atau delta

        Sistem kendali versi lama menyimpan **delta**, yaitu hanya perbedaan antar versi, untuk menghemat ruang. Memulihkan versi lama berarti menerapkan delta berurutan dari awal. Git memilih jalan berbeda: secara konseptual ia menyimpan snapshot utuh, tetapi file yang tidak berubah dipakai bersama sehingga tidak ada penyalinan sia-sia.

        Keuntungannya, berpindah ke versi mana pun cepat dan sederhana, karena tidak perlu menerapkan rantai delta yang panjang.
        """),
        T("""
        ## Manfaat bagi analis data

        Bagi analis data, version control bukan sekadar urusan programmer. Ia membuat analisis dapat diulang: kita bisa menandai versi skrip yang menghasilkan sebuah laporan dan memulihkannya kapan pun. Ia juga melindungi dari kesalahan, karena perubahan buruk dapat dibatalkan dalam hitungan detik.

        Dalam kerja tim, riwayat menjadi dokumentasi hidup. Pesan perubahan menjelaskan alasan keputusan, dan diff menunjukkan persis apa yang dikerjakan rekan sebelum kita menggabungkan hasilnya.
        """),
        T("""
        ## Apa yang layak dilacak

        Version control paling cocok untuk file teks: kode, skrip SQL, notebook yang dibersihkan, dokumen Markdown, dan berkas konfigurasi. Diff pada teks mudah dibaca manusia. File biner besar seperti basis data atau kumpulan data mentah kurang cocok karena diff-nya tidak bermakna dan ukurannya membengkakkan riwayat.

        Untuk data besar, simpan lokasi dan checksum-nya, bukan isinya. Kita akan kembali ke hal ini pada pelajaran workflow reproducible.
        """),
        K(
            "tip",
            """
            Lacak teks dan kode di version control. Untuk data besar, catat sumber dan checksum alih-alih menyimpan filenya.
            """,
            title="Yang dilacak",
        ),
        T("""
        ## Riwayat sebagai kebiasaan

        Version control paling bermanfaat bila dijadikan kebiasaan, bukan tindakan darurat. Simpan perubahan sering dengan pesan yang jelas, sehingga setiap langkah analisis punya titik kembali. Kebiasaan kecil ini menyelamatkan jam kerja saat eksperimen berjalan salah arah.
        """),
        E(
            "A7-01-1-ex1",
            "mudah",
            """
            Tulis fungsi `tambah_versi(riwayat, isi)` yang menambahkan `isi` ke akhir list `riwayat` dan mengembalikan nomor versi barunya (dimulai dari 1).
            """,
            """
            def tambah_versi(riwayat, isi):
                # TODO: implementasikan
                pass
            """,
            """
            r = []
            assert tambah_versi(r, 'a') == 1
            assert tambah_versi(r, 'b') == 2
            assert r == ['a', 'b']
            assert tambah_versi(r, 'c') == 3
            """,
            "Gunakan append lalu kembalikan panjang list.",
            """
            def tambah_versi(riwayat, isi):
                riwayat.append(isi)
                return len(riwayat)
            """,
        ),
        E(
            "A7-01-1-ex2",
            "sedang",
            """
            Tulis fungsi `baris_berubah(a, b)` yang mengembalikan tuple `(ditambah, dihapus)`. `ditambah` adalah list terurut baris yang ada di teks `b` tetapi tidak di `a`, dan `dihapus` adalah list terurut baris yang ada di `a` tetapi tidak di `b`. Pisahkan baris dengan `splitlines()`.
            """,
            """
            def baris_berubah(a, b):
                # TODO: implementasikan
                pass
            """,
            """
            assert baris_berubah('x\\ny\\nz', 'x\\nz\\nw') == (['w'], ['y'])
            assert baris_berubah('a', 'a') == ([], [])
            assert baris_berubah('', 'p\\nq') == (['p', 'q'], [])
            assert baris_berubah('p\\nq', '') == ([], ['p', 'q'])
            """,
            "Ubah setiap teks menjadi set baris lalu ambil selisih set.",
            """
            def baris_berubah(a, b):
                sa = set(a.splitlines())
                sb = set(b.splitlines())
                return (sorted(sb - sa), sorted(sa - sb))
            """,
        ),
        E(
            "A7-01-1-ex3",
            "sedang",
            """
            Tulis fungsi `kembalikan(riwayat, nomor)` yang mengembalikan snapshot versi ke-`nomor` (dimulai dari 1). Bila `nomor` kurang dari 1 atau lebih besar dari jumlah versi, lemparkan `ValueError`.
            """,
            """
            def kembalikan(riwayat, nomor):
                # TODO: implementasikan
                pass
            """,
            """
            r = ['a', 'b', 'c']
            assert kembalikan(r, 1) == 'a'
            assert kembalikan(r, 3) == 'c'
            for salah in (0, 4, -1):
                try:
                    kembalikan(r, salah)
                    diterima = True
                except ValueError:
                    diterima = False
                assert diterima is False
            """,
            "Periksa batas nomor lalu ambil elemen indeks nomor dikurangi satu.",
            """
            def kembalikan(riwayat, nomor):
                if nomor < 1 or nomor > len(riwayat):
                    raise ValueError('nomor versi tidak valid')
                return riwayat[nomor - 1]
            """,
        ),
        E(
            "A7-01-1-ex4",
            "menantang",
            """
            Tulis fungsi `diff_baris(a, b)` yang mengembalikan list tuple `(tanda, baris)` dengan tanda `' '` untuk baris tetap, `'-'` untuk dihapus, dan `'+'` untuk ditambah, berdasarkan LCS dengan aturan berikut: bila baris sama, ambil sebagai tetap. Bila beda dan menghapus baris `a` tidak mengurangi panjang LCS (`dp[i+1][j] >= dp[i][j+1]`), hapus baris `a`, jika tidak tambahkan baris `b`. Sisa baris di akhir dihapus lalu ditambah.
            """,
            """
            def diff_baris(a, b):
                # TODO: implementasikan
                pass
            """,
            """
            assert diff_baris('x\\ny\\nz', 'x\\nz\\nw') == [(' ', 'x'), ('-', 'y'), (' ', 'z'), ('+', 'w')]
            assert diff_baris('a\\nb', 'a\\nb') == [(' ', 'a'), (' ', 'b')]
            assert diff_baris('', 'p') == [('+', 'p')]
            assert diff_baris('p', '') == [('-', 'p')]
            """,
            "Bangun tabel LCS dari belakang lalu telusuri dari depan.",
            DIFF_CODE.strip("\n"),
        ),
    ],
    [
        M("Menyalin folder dan menamai file_final_v2.", "Gunakan version control agar riwayat tercatat."),
        M("Mengira diff himpunan cukup untuk semua kasus.", "Gunakan LCS agar urutan dihormati."),
        M("Menyimpan data mentah besar di riwayat.", "Catat sumber dan checksum saja."),
    ],
    [
        Q("Version control mencatat?", ["Perubahan file dari waktu ke waktu", "Kecepatan internet", "Isi memori", "Jumlah pengguna"], 0, "Siapa mengubah apa dan kapan.", hint="Perubahan."),
        Q("Diff menunjukkan?", ["Apa yang berubah antar versi", "Ukuran disk", "Nama pengguna", "Waktu eksekusi"], 0, "Baris ditambah dan dihapus.", hint="Beda."),
        Q("Snapshot adalah?", ["Salinan lengkap pada satu saat", "Hanya perbedaan", "Nama cabang", "Pesan commit"], 0, "Keadaan utuh.", hint="Foto."),
        Q("LCS dipakai untuk?", ["Mencari baris yang sama berurutan", "Mengurutkan file", "Mengompres data", "Membuat hash"], 0, "Subsekuens terpanjang.", hint="Urutan."),
        Q("Jenis file paling cocok di version control?", ["Teks dan kode", "Video besar", "Basis data biner besar", "Gambar mentah besar"], 0, "Diff bermakna.", hint="Teks."),
    ],
    [
        "Version control mencatat siapa mengubah apa, kapan, dan mengapa.",
        "Riwayat dapat dipahami sebagai daftar snapshot.",
        "Diff menunjukkan perubahan dan paling akurat dengan LCS.",
        "Lacak teks dan kode, bukan data biner besar.",
    ],
    [],
)

HASH_CODE = """
import hashlib

def hash_blob(teks):
    data = teks.encode('utf-8')
    return hashlib.sha1(b'blob %d\\0' % len(data) + data).hexdigest()
"""

TREE_CODE = HASH_CODE + """
def hash_tree(berkas):
    baris = [nama + ' ' + hash_blob(berkas[nama]) for nama in sorted(berkas)]
    return hashlib.sha1('\\n'.join(baris).encode('utf-8')).hexdigest()
"""

COMMIT_FN = """
def buat_commit(tree, parent, pesan):
    isi = 'tree ' + tree + '\\nparent ' + (parent or '') + '\\n\\n' + pesan
    return {'tree': tree, 'parent': parent, 'pesan': pesan, 'id': hashlib.sha1(isi.encode('utf-8')).hexdigest()}
"""

COMMIT_CODE = TREE_CODE + COMMIT_FN

l2 = lesson(
    "A7-01-2",
    "Git di balik layar: hash dan objek",
    35,
    [
        "Menjelaskan content-addressable storage dan fungsi hash",
        "Menghitung hash blob yang kompatibel dengan Git",
        "Memahami tree dan commit sebagai objek yang saling merujuk",
        "Menjelaskan mengapa riwayat Git tahan terhadap pengubahan diam-diam",
    ],
    [
        T("""
        ## Mengapa memahami bagian dalam

        Banyak orang memakai Git dengan menghafal perintah, lalu panik ketika sesuatu tidak berjalan seperti dugaan. Memahami cara Git menyimpan data mengubah kepanikan itu menjadi pemahaman. Perintah yang tampak ajaib ternyata operasi sederhana pada beberapa jenis objek.

        Pelajaran ini membangun model kecil Git dengan Python. Fungsi hash yang kita pakai identik dengan milik Git, sehingga hasilnya persis sama dengan perintah asli.
        """),
        T("""
        ## Fungsi hash

        **Fungsi hash** mengubah data apa pun menjadi deretan karakter berukuran tetap. Hash yang baik bersifat deterministik: isi sama selalu menghasilkan hash sama. Ia juga sensitif: perubahan sekecil satu karakter menghasilkan hash yang sama sekali berbeda. Dan ia searah: dari hash kita tidak dapat memulihkan isinya.

        Git memakai SHA-1, yang menghasilkan 40 karakter heksadesimal. Hash itulah yang menjadi nama setiap objek yang disimpan Git.
        """),
        T("""
        ## Content-addressable storage

        Git menyimpan objek dengan **alamat berdasarkan isi**: nama sebuah objek adalah hash dari isinya. Konsekuensinya menarik. Dua file dengan isi sama, di folder berbeda atau di commit berbeda, hanya disimpan satu kali karena hash-nya sama. Inilah rahasia penghematan ruang yang tadi dijanjikan.

        Konsekuensi lain: objek tidak pernah berubah. Mengubah isi berarti membuat objek baru dengan hash baru, sementara yang lama tetap ada di basis data.
        """),
        T("""
        ## Blob: isi sebuah file

        Objek paling dasar adalah **blob**, yaitu isi satu file tanpa nama. Git menghitung hash blob dari teks `blob`, spasi, panjang isi dalam byte, byte nol, lalu isinya. Dengan rumus ini, hash isi `hello` dengan baris baru adalah `ce013625030ba8dba906f756967f9e9ca394464a`, sama persis dengan keluaran perintah `git hash-object`.

        File kosong pun punya hash tetap yang terkenal, `e69de29b...`. Itu sebabnya Git dapat mengenali file kosong di repositori mana pun.
        """),
        C(
            J(HASH_CODE, """
            print(hash_blob('hello\\n'))
            print(hash_blob(''))
            print(hash_blob('hello\\n') == hash_blob('hello\\n'))
            print(hash_blob('hello\\n') == hash_blob('hello!\\n'))
            print(len(hash_blob('apa saja')))
            """),
            """
            ce013625030ba8dba906f756967f9e9ca394464a
            e69de29bb2d1d6434b8b29ae775ad8c2e48c5391
            True
            False
            40
            """,
            """
            Hash identik dengan milik Git: isi sama menghasilkan hash sama, perubahan kecil mengubahnya, dan panjangnya selalu empat puluh karakter.
            """,
            filename="hash_blob.py",
        ),
        T("""
        ## Tree: nama file dan struktur folder

        Blob tidak tahu nama filenya. Nama dicatat oleh objek **tree**, yaitu daftar pasangan nama dan hash isi, satu tree per folder. Sebuah tree dapat memuat tree lain untuk subfolder, sehingga seluruh struktur proyek terwakili oleh satu hash tree puncak.

        Model kita menyederhanakan format biner Git menjadi teks: baris `nama hash` yang terurut, lalu di-hash. Prinsipnya sama: isi dan nama yang sama menghasilkan hash tree yang sama, apa pun urutan penulisannya.
        """),
        C(
            J(TREE_CODE, """
            a = {'a.py': 'print(1)\\n', 'b.txt': 'x\\n'}
            b = {'b.txt': 'x\\n', 'a.py': 'print(1)\\n'}
            c = {'a.py': 'print(2)\\n', 'b.txt': 'x\\n'}
            print(hash_tree(a))
            print(hash_tree(a) == hash_tree(b))
            print(hash_tree(a) == hash_tree(c))
            """),
            """
            d797d9aafca8ed5e2e5354ac1138dca0a682d915
            True
            False
            """,
            """
            Urutan penulisan tidak memengaruhi hash tree, tetapi mengubah isi satu file menghasilkan hash tree yang berbeda.
            """,
            filename="hash_tree.py",
        ),
        T("""
        ## Commit: snapshot dengan konteks

        Objek **commit** menyimpan hash tree puncak, hash commit induk, serta pesan dan penulis. Dengan merujuk tree, commit mewakili snapshot lengkap. Dengan merujuk induk, commit-commit membentuk rantai, atau lebih tepatnya graf, yang merekam sejarah proyek.

        Commit pertama tidak punya induk. Commit hasil penggabungan punya dua induk. Selain itu, setiap commit hanya menunjuk ke belakang, ke pendahulunya.
        """),
        C(
            J(COMMIT_CODE, """
            a = {'a.py': 'print(1)\\n', 'b.txt': 'x\\n'}
            t = hash_tree(a)
            c1 = buat_commit(t, None, 'awal')
            c2 = buat_commit(t, c1['id'], 'kedua')
            print(c1['id'][:8], c2['id'][:8])
            c1x = buat_commit(t, None, 'awal!')
            c2x = buat_commit(t, c1x['id'], 'kedua')
            print(c1x['id'][:8], c2x['id'][:8])
            print(c2['id'] == c2x['id'])
            """),
            """
            21924f42 291dfe30
            6142e5a1 33388fff
            False
            """,
            """
            Mengubah pesan commit pertama mengubah hash-nya, dan karena commit kedua memuat hash induk, hash commit kedua ikut berubah.
            """,
            filename="hash_commit.py",
        ),
        T("""
        ## Riwayat yang tahan manipulasi

        Karena setiap commit memuat hash induknya, mengubah satu commit lama diam-diam akan mengubah hash-nya, lalu hash semua commit sesudahnya. Perubahan terselubung langsung ketahuan, sebab hash di ujung rantai tidak lagi cocok. Sifat ini mirip rantai blok pada teknologi blockchain.

        Bagi tim, artinya riwayat dapat dipercaya sebagai catatan. Bagi analis, ia berarti hash commit dapat dicatat bersama hasil analisis sebagai sidik jari versi kode yang menghasilkannya.
        """),
        T("""
        ## Rujukan: cabang dan HEAD

        Hash 40 karakter sulit diingat, jadi Git menyediakan **rujukan** bernama. Cabang adalah file kecil berisi hash commit terbaru di jalur itu. `HEAD` adalah penunjuk ke cabang yang sedang aktif. Membuat commit baru hanya menggeser rujukan cabang ke commit baru.

        Itulah sebabnya membuat cabang di Git murah: ia hanya membuat file kecil berisi satu hash, bukan menyalin proyek.
        """),
        K(
            "note",
            """
            Git memakai SHA-1 untuk memberi nama objek, bukan sebagai pengaman kata sandi. Tujuannya konsistensi dan deteksi perubahan.
            """,
            title="Tujuan hash",
        ),
        T("""
        ## Hash dan deteksi duplikasi

        Karena nama objek adalah hash isinya, Git mengenali duplikasi tanpa membandingkan file satu per satu. Dua salinan file yang sama persis, di mana pun letaknya, hanya disimpan sekali. Pada proyek dengan banyak versi, penghematan ini sangat besar.

        Gagasan yang sama dipakai di banyak sistem lain: penyimpanan cadangan, sinkronisasi berkas, dan pengelolaan paket perangkat lunak. Memahami hash membuka pemahaman tentang semuanya.
        """),
        T("""
        ## Tabrakan hash

        Dua isi berbeda dapat secara teori menghasilkan hash sama, yang disebut tabrakan. Untuk SHA-1 peluangnya sangat kecil pada pemakaian wajar, dan Git modern menambahkan pemeriksaan terhadap serangan yang diketahui. Karena itu kita aman menganggap hash yang sama berarti isi yang sama.
        """),
        E(
            "A7-01-2-ex1",
            "mudah",
            """
            Tulis fungsi `hash_blob(teks)` yang mengembalikan hash blob Git dalam heksadesimal: SHA-1 dari byte `blob`, spasi, panjang byte isi, byte nol, lalu isi (UTF-8).
            """,
            """
            import hashlib

            def hash_blob(teks):
                # TODO: implementasikan
                pass
            """,
            """
            assert hash_blob('hello\\n') == 'ce013625030ba8dba906f756967f9e9ca394464a'
            assert hash_blob('') == 'e69de29bb2d1d6434b8b29ae775ad8c2e48c5391'
            assert hash_blob('a') == '2e65efe2a145dda7ee51d1741299f848e5bf752e'
            assert len(hash_blob('xyz')) == 40
            """,
            "Gabungkan awalan blob, panjang byte, dan byte nol sebelum isi.",
            HASH_CODE.strip("\n"),
        ),
        E(
            "A7-01-2-ex2",
            "sedang",
            """
            Tulis fungsi `hash_tree(berkas)` yang menerima dict `{nama: isi}` dan mengembalikan SHA-1 heksadesimal dari teks gabungan baris `nama hash_blob(isi)` yang diurutkan menurut nama dan dipisah baris baru. Fungsi `hash_blob` sudah tersedia.
            """,
            """
            import hashlib

            def hash_blob(teks):
                data = teks.encode('utf-8')
                return hashlib.sha1(b'blob %d\\0' % len(data) + data).hexdigest()

            def hash_tree(berkas):
                # TODO: implementasikan
                pass
            """,
            """
            a = {'a.py': 'print(1)\\n', 'b.txt': 'x\\n'}
            b = {'b.txt': 'x\\n', 'a.py': 'print(1)\\n'}
            c = {'a.py': 'print(2)\\n', 'b.txt': 'x\\n'}
            assert hash_tree(a) == 'd797d9aafca8ed5e2e5354ac1138dca0a682d915'
            assert hash_tree(a) == hash_tree(b)
            assert hash_tree(a) != hash_tree(c)
            assert len(hash_tree({})) == 40
            """,
            "Urutkan nama, bentuk baris nama dan hash blob, gabungkan dengan baris baru.",
            TREE_CODE.strip("\n"),
        ),
        E(
            "A7-01-2-ex3",
            "sedang",
            """
            Tulis fungsi `buat_commit(tree, parent, pesan)` yang mengembalikan dict berkunci `tree`, `parent`, `pesan`, dan `id`. Nilai `id` adalah SHA-1 heksadesimal dari teks `tree ` + tree + `\\nparent ` + (parent atau string kosong) + `\\n\\n` + pesan.
            """,
            """
            import hashlib

            def buat_commit(tree, parent, pesan):
                # TODO: implementasikan
                pass
            """,
            """
            c1 = buat_commit('t' * 40, None, 'awal')
            c2 = buat_commit('t' * 40, c1['id'], 'awal')
            assert set(c1) == {'tree', 'parent', 'pesan', 'id'}
            assert len(c1['id']) == 40 and c1['parent'] is None
            assert c1['id'] != c2['id']
            assert buat_commit('t' * 40, None, 'awal')['id'] == c1['id']
            """,
            "Susun teks isi commit persis sesuai format lalu hash.",
            "import hashlib\n" + COMMIT_FN,
        ),
        E(
            "A7-01-2-ex4",
            "menantang",
            """
            Tulis fungsi `rantai_valid(commits)` yang menerima list commit dari yang paling lama ke terbaru (dict seperti hasil `buat_commit`) dan mengembalikan `True` hanya bila commit pertama tidak punya induk, setiap `parent` sama dengan `id` commit sebelumnya, dan setiap `id` sama dengan hash yang dihitung ulang dari `tree`, `parent`, dan `pesan` dengan rumus commit.
            """,
            """
            import hashlib

            def rantai_valid(commits):
                # TODO: implementasikan
                pass
            """,
            """
            import hashlib

            def _buat(tree, parent, pesan):
                isi = 'tree ' + tree + '\\nparent ' + (parent or '') + '\\n\\n' + pesan
                return {'tree': tree, 'parent': parent, 'pesan': pesan, 'id': hashlib.sha1(isi.encode('utf-8')).hexdigest()}

            t = 'a' * 40
            c1 = _buat(t, None, 'awal')
            c2 = _buat(t, c1['id'], 'kedua')
            c3 = _buat(t, c2['id'], 'ketiga')
            assert rantai_valid([c1, c2, c3]) is True
            assert rantai_valid([c1, c3]) is False
            rusak = dict(c2)
            rusak['pesan'] = 'diubah'
            assert rantai_valid([c1, rusak, c3]) is False
            assert rantai_valid([c2, c3]) is False
            """,
            "Telusuri berurutan dan hitung ulang id tiap commit.",
            """
            import hashlib

            def rantai_valid(commits):
                sebelumnya = None
                for c in commits:
                    if c['parent'] != sebelumnya:
                        return False
                    isi = 'tree ' + c['tree'] + '\\nparent ' + (c['parent'] or '') + '\\n\\n' + c['pesan']
                    if hashlib.sha1(isi.encode('utf-8')).hexdigest() != c['id']:
                        return False
                    sebelumnya = c['id']
                return True
            """,
        ),
    ],
    [
        M("Mengira nama file ikut tersimpan dalam blob.", "Nama dicatat oleh tree."),
        M("Mengira mengubah commit lama tidak meninggalkan jejak.", "Hash semua commit sesudahnya ikut berubah."),
        M("Menganggap SHA-1 Git sebagai pengaman rahasia.", "Ia untuk penamaan dan deteksi perubahan."),
    ],
    [
        Q("Nama objek Git berasal dari?", ["Hash isinya", "Waktu pembuatan", "Nama pengguna", "Nomor urut"], 0, "Content-addressable.", hint="Isi."),
        Q("Blob menyimpan?", ["Isi file tanpa nama", "Nama folder", "Pesan commit", "Cabang"], 0, "Hanya isi.", hint="Isi."),
        Q("Tree menyimpan?", ["Nama dan hash isi file", "Hanya pesan", "Hanya waktu", "Kata sandi"], 0, "Struktur folder.", hint="Nama."),
        Q("Commit merujuk ke?", ["Tree dan commit induk", "Hanya blob", "Hanya cabang", "Pengguna lain"], 0, "Snapshot dan pendahulu.", hint="Induk."),
        Q("Mengubah commit lama menyebabkan?", ["Hash commit sesudahnya berubah", "Tidak ada efek", "File terhapus", "Cabang hilang"], 0, "Rantai hash.", hint="Rantai."),
    ],
    [
        "Git menamai objek dengan hash isinya.",
        "Blob, tree, dan commit adalah tiga objek utama.",
        "Commit merujuk induknya sehingga riwayat membentuk rantai hash.",
        "Cabang dan HEAD hanyalah rujukan bernama ke commit.",
    ],
    [],
)

l3 = lesson(
    "A7-01-3",
    "Tiga area kerja dan alur dasar",
    35,
    [
        "Membedakan working directory, staging area, dan repository",
        "Menentukan status file dari perbandingan ketiga area",
        "Menjelaskan alur init, add, commit, status, dan log",
        "Membangun simulasi repositori mini dengan Python",
    ],
    [
        T("""
        ## Tiga tempat satu file

        Sebuah file dalam proyek Git dapat berada di tiga tempat. **Working directory** adalah folder tempat kita mengedit file seperti biasa. **Staging area**, atau index, adalah daftar perubahan yang kita pilih untuk masuk ke commit berikutnya. **Repository** adalah basis data riwayat berisi semua commit.

        Pemisahan ini sering membingungkan pemula, tetapi ia memberi kendali: kita boleh mengedit sepuluh file lalu membuat dua commit terpisah yang masing-masing rapi dan bermakna.
        """),
        T("""
        ## Alur dasar

        Alur kerja harian Git sederhana. Kita mengedit file di working directory, memilih perubahan dengan `git add`, lalu merekamnya dengan `git commit`. `git status` memberi tahu keadaan ketiga area, dan `git log` menampilkan riwayat. Sebelum semua itu, `git init` mengubah folder biasa menjadi repositori.

        ```bash
        git init
        git add laporan.py
        git commit -m "Tambah skrip laporan"
        git status
        git log
        ```
        """),
        T("""
        ## Mengapa ada staging area

        Staging area memungkinkan commit yang fokus. Misalkan kita memperbaiki bug sekaligus menambah fitur dalam satu sesi. Dengan staging, kita dapat memasukkan hanya file perbaikan bug ke commit pertama, lalu fitur ke commit kedua. Riwayat jadi mudah dibaca, dan perubahan buruk mudah dibatalkan secara terpisah.

        Tanpa staging, setiap commit akan menelan semua perubahan yang sedang berlangsung, mencampur topik yang tidak berkaitan.
        """),
        T("""
        ## Membaca status

        Status sebuah file ditentukan dengan membandingkan area-area. File yang ada di working directory tetapi belum pernah masuk repositori disebut **untracked**. File yang isinya berbeda antara working directory dan staging area disebut **modified** dan belum di-stage. File yang isinya di staging area berbeda dari commit terakhir disebut **staged**, siap dicommit.

        Tiga perbandingan sederhana inilah seluruh isi `git status`. Kita dapat menirunya dengan beberapa baris Python di atas dict nama ke isi.
        """),
        C(
            """
            kerja = {'a.py': 'v2', 'b.py': 'baru'}
            indeks = {'a.py': 'v1'}
            head = {'a.py': 'v1'}
            print(sorted(n for n in kerja if n not in head))
            print(sorted(n for n in kerja if n in indeks and kerja[n] != indeks[n]))
            print(sorted(n for n in indeks if head.get(n) != indeks[n]))
            """,
            """
            ['b.py']
            ['a.py']
            []
            """,
            """
            File b.py untracked, a.py sudah berubah tetapi belum di-stage, dan belum ada file yang siap dicommit.
            """,
            filename="status_sederhana.py",
        ),
        T("""
        ## Commit adalah snapshot staging

        Perhatikan detail penting: commit merekam isi **staging area**, bukan working directory. Bila kita mengedit file setelah `git add` tanpa menambahkannya lagi, perubahan terbaru tidak ikut commit. Banyak pemula bingung mengapa perubahan terakhir tidak tersimpan, dan jawabannya hampir selalu lupa menjalankan `add` ulang.

        Commit juga menolak membuat rekaman kosong: bila staging area sama dengan commit terakhir, tidak ada yang perlu direkam.
        """),
        T("""
        ## Simulasi repositori mini

        Kita dapat merangkum tiga area dalam kelas Python kecil. Ia menyimpan `kerja`, `indeks`, dan `riwayat` berisi snapshot. Metode `tulis` mengubah working directory, `add` menyalin ke indeks, dan `commit` merekam salinan indeks ke riwayat.

        Meski sederhana, kelas ini menampung perilaku inti Git: commit menyimpan snapshot lengkap, riwayat hanya bertambah, dan versi lama dapat dibaca kapan saja.
        """),
        C(
            """
            class MiniRepo:
                def __init__(self):
                    self.kerja = {}
                    self.indeks = {}
                    self.riwayat = []

                def tulis(self, nama, isi):
                    self.kerja[nama] = isi

                def add(self, nama):
                    self.indeks[nama] = self.kerja[nama]

                def commit(self, pesan):
                    terakhir = self.riwayat[-1]['snapshot'] if self.riwayat else {}
                    if self.indeks == terakhir:
                        raise ValueError('tidak ada perubahan')
                    self.riwayat.append({'pesan': pesan, 'snapshot': dict(self.indeks)})
                    return len(self.riwayat)

                def log(self):
                    return [r['pesan'] for r in reversed(self.riwayat)]

                def baca(self, nama, nomor):
                    return self.riwayat[nomor - 1]['snapshot'][nama]

            r = MiniRepo()
            r.tulis('a.py', 'v1')
            r.add('a.py')
            print(r.commit('awal'))
            r.tulis('a.py', 'v2')
            try:
                r.commit('kosong')
            except ValueError as e:
                print('gagal', e)
            r.add('a.py')
            print(r.commit('ubah'))
            print(r.log())
            print(r.baca('a.py', 1), r.baca('a.py', 2))
            """,
            """
            1
            gagal tidak ada perubahan
            2
            ['ubah', 'awal']
            v1 v2
            """,
            """
            Commit tanpa add ditolak karena indeks sama dengan commit terakhir. Setelah add, commit kedua berhasil dan kedua versi file dapat dibaca.
            """,
            filename="mini_repo.py",
        ),
        T("""
        ## Pesan commit yang baik

        Pesan commit adalah surat untuk diri sendiri di masa depan dan untuk rekan setim. Tulis baris pertama singkat dan menjelaskan apa yang berubah, misalnya `Perbaiki perhitungan rata-rata pada laporan bulanan`. Hindari pesan seperti `update` atau `perbaikan` yang tidak memberi informasi.

        Pesan yang baik menjawab mengapa perubahan dibuat, karena apa yang berubah sudah terlihat di diff. Beberapa bulan kemudian, alasan itulah yang paling sulit diingat.
        """),
        T("""
        ## Mengabaikan file

        Tidak semua file layak dilacak: berkas sementara, cache Python, kata sandi, dan data besar. Git mengenal file `.gitignore` yang memuat pola nama file yang diabaikan, misalnya `__pycache__/`, `*.csv`, dan `.env`. File yang cocok pola tidak akan muncul sebagai untracked.

        Buat `.gitignore` sejak awal proyek. Sekali kata sandi atau data sensitif masuk riwayat, menghapusnya tuntas jauh lebih sulit daripada mencegahnya masuk.
        """),
        K(
            "warn",
            """
            Jangan pernah mencommit kata sandi, token, atau data pribadi. Masukkan ke .gitignore sebelum commit pertama.
            """,
            title="Rahasia di riwayat",
        ),
        T("""
        ## Cabang dan kerja paralel

        Tiga area dan alur dasar sudah cukup untuk bekerja sendirian dengan satu garis riwayat. Pelajaran berikutnya memperkenalkan cabang, yang memungkinkan beberapa jalur pekerjaan berjalan paralel tanpa saling mengganggu, lalu digabungkan kembali saat siap.

        Fondasi yang kita pelajari di sini, yaitu commit sebagai snapshot yang merujuk induknya, adalah dasar dari semua kemampuan itu.
        """),
        T("""
        ## Memeriksa sebelum commit

        Biasakan menjalankan status dan melihat diff sebelum commit. Dua perintah ini memastikan kita hanya merekam apa yang dimaksudkan, bukan file sementara atau perubahan yang tidak sengaja. Lima detik pemeriksaan sering menghemat lima menit pembersihan riwayat.
        """),
        C(
            """
            pola = ['.csv', '.env', '__pycache__/']
            berkas = ['a.py', 'data.csv', '.env', '__pycache__/x.pyc', 'b.txt']

            def diabaikan(nama):
                return any(nama.endswith(p) or nama.startswith(p) for p in pola)

            print([n for n in berkas if not diabaikan(n)])
            """,
            """
            ['a.py', 'b.txt']
            """,
            """
            Berkas data, rahasia, dan cache tersaring sehingga hanya kode dan teks yang dilacak.
            """,
            filename="abaikan_berkas.py",
        ),
        E(
            "A7-01-3-ex1",
            "mudah",
            """
            Tulis fungsi `belum_ditrack(kerja, head)` yang menerima dua dict `{nama: isi}` dan mengembalikan list terurut nama file yang ada di `kerja` tetapi tidak ada di `head`.
            """,
            """
            def belum_ditrack(kerja, head):
                # TODO: implementasikan
                pass
            """,
            """
            assert belum_ditrack({'a': '1', 'b': '2'}, {'a': '1'}) == ['b']
            assert belum_ditrack({'a': '1'}, {'a': '1'}) == []
            assert belum_ditrack({'z': '1', 'y': '2'}, {}) == ['y', 'z']
            assert belum_ditrack({}, {'a': '1'}) == []
            """,
            "Saring nama di kerja yang tidak ada di head lalu urutkan.",
            """
            def belum_ditrack(kerja, head):
                return sorted(n for n in kerja if n not in head)
            """,
        ),
        E(
            "A7-01-3-ex2",
            "sedang",
            """
            Tulis fungsi `berubah_belum_stage(kerja, indeks)` yang mengembalikan list terurut nama file yang ada di kedua dict tetapi isinya berbeda.
            """,
            """
            def berubah_belum_stage(kerja, indeks):
                # TODO: implementasikan
                pass
            """,
            """
            assert berubah_belum_stage({'a': '2', 'b': '1'}, {'a': '1', 'b': '1'}) == ['a']
            assert berubah_belum_stage({'a': '1'}, {'a': '1'}) == []
            assert berubah_belum_stage({'a': '1', 'c': 'x'}, {'a': '9'}) == ['a']
            assert berubah_belum_stage({'n': '1'}, {}) == []
            """,
            "Bandingkan isi hanya untuk nama yang ada di indeks.",
            """
            def berubah_belum_stage(kerja, indeks):
                return sorted(n for n in kerja if n in indeks and kerja[n] != indeks[n])
            """,
        ),
        E(
            "A7-01-3-ex3",
            "sedang",
            """
            Tulis fungsi `siap_commit(indeks, head)` yang mengembalikan list terurut nama file di `indeks` yang tidak ada di `head` atau isinya berbeda dari di `head`.
            """,
            """
            def siap_commit(indeks, head):
                # TODO: implementasikan
                pass
            """,
            """
            assert siap_commit({'a': '2'}, {'a': '1'}) == ['a']
            assert siap_commit({'a': '1'}, {'a': '1'}) == []
            assert siap_commit({'b': '1', 'a': '1'}, {}) == ['a', 'b']
            assert siap_commit({'a': '1', 'b': '2'}, {'a': '1', 'b': '3'}) == ['b']
            """,
            "Gunakan head.get(nama) dan bandingkan dengan isi di indeks.",
            """
            def siap_commit(indeks, head):
                return sorted(n for n in indeks if head.get(n) != indeks[n])
            """,
        ),
        E(
            "A7-01-3-ex4",
            "menantang",
            """
            Tulis kelas `MiniRepo` dengan atribut `kerja`, `indeks` (dict) dan `riwayat` (list), serta metode `tulis(nama, isi)`, `add(nama)` yang menyalin isi dari `kerja` ke `indeks`, `commit(pesan)` yang menambahkan `{'pesan': pesan, 'snapshot': salinan indeks}` ke riwayat dan mengembalikan jumlah commit (lempar `ValueError` bila indeks sama dengan snapshot commit terakhir atau dengan `{}` bila belum ada commit), `log()` yang mengembalikan list pesan dari terbaru, dan `baca(nama, nomor)` yang mengembalikan isi file pada commit ke-`nomor` (mulai 1).
            """,
            """
            class MiniRepo:
                def __init__(self):
                    # TODO: implementasikan
                    pass
            """,
            """
            r = MiniRepo()
            r.tulis('a.py', 'v1')
            r.add('a.py')
            assert r.commit('awal') == 1
            r.tulis('a.py', 'v2')
            try:
                r.commit('kosong')
                gagal = False
            except ValueError:
                gagal = True
            assert gagal is True
            r.add('a.py')
            assert r.commit('ubah') == 2
            assert r.log() == ['ubah', 'awal']
            assert r.baca('a.py', 1) == 'v1' and r.baca('a.py', 2) == 'v2'
            """,
            "Simpan salinan indeks pada tiap commit dan bandingkan dengan snapshot terakhir.",
            """
            class MiniRepo:
                def __init__(self):
                    self.kerja = {}
                    self.indeks = {}
                    self.riwayat = []

                def tulis(self, nama, isi):
                    self.kerja[nama] = isi

                def add(self, nama):
                    self.indeks[nama] = self.kerja[nama]

                def commit(self, pesan):
                    terakhir = self.riwayat[-1]['snapshot'] if self.riwayat else {}
                    if self.indeks == terakhir:
                        raise ValueError('tidak ada perubahan')
                    self.riwayat.append({'pesan': pesan, 'snapshot': dict(self.indeks)})
                    return len(self.riwayat)

                def log(self):
                    return [r['pesan'] for r in reversed(self.riwayat)]

                def baca(self, nama, nomor):
                    return self.riwayat[nomor - 1]['snapshot'][nama]
            """,
        ),
    ],
    [
        M("Mengedit file setelah add lalu commit tanpa add ulang.", "Jalankan add lagi agar perubahan terbaru ikut."),
        M("Menulis pesan commit seperti update.", "Jelaskan apa dan mengapa berubah."),
        M("Mencommit file rahasia.", "Gunakan .gitignore sejak awal."),
    ],
    [
        Q("Commit merekam isi?", ["Staging area", "Working directory", "Internet", "Cabang lain"], 0, "Yang sudah di-add.", hint="Stage."),
        Q("File baru yang belum pernah dilacak disebut?", ["Untracked", "Staged", "Committed", "Merged"], 0, "Belum dikenal Git.", hint="Un."),
        Q("Perintah menyiapkan perubahan untuk commit?", ["git add", "git log", "git init", "git clone"], 0, "Memasukkan ke staging.", hint="Add."),
        Q("Fungsi .gitignore?", ["Mengabaikan file tertentu", "Menghapus riwayat", "Membuat cabang", "Mengunci repo"], 0, "Daftar pola.", hint="Abaikan."),
        Q("git init melakukan?", ["Membuat repositori baru", "Menghapus file", "Menggabungkan cabang", "Mengirim ke server"], 0, "Inisialisasi.", hint="Awal."),
    ],
    [
        "Tiga area: working directory, staging area, dan repository.",
        "Commit merekam staging area, bukan working directory.",
        "Status file didapat dari membandingkan ketiga area.",
        "Gunakan pesan commit bermakna dan .gitignore sejak awal.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perintah yang cukup jelas dalam teks.", "brief": []}

write_module(
    "A7",
    1,
    "Konsep version control",
    105,
    [
        "Menjelaskan manfaat version control bagi analis data",
        "Memahami objek blob, tree, dan commit serta rantai hash",
        "Membedakan tiga area kerja Git dan alur dasarnya",
    ],
    [l1, l2, l3],
    video,
    REF,
)
