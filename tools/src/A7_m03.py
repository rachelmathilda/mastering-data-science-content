import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []


def J(prefix, body):
    return prefix.strip("\n") + "\n\n" + textwrap.dedent(body).strip("\n")


FIXK = textwrap.indent("""def _k():
    return {
        'c1': {'parent': None, 'pesan': 'awal'},
        'c2': {'parent': 'c1', 'pesan': 'dua'},
        'c3': {'parent': 'c2', 'pesan': 'main'},
        'c4': {'parent': 'c2', 'pesan': 'fitur'},
        'c5': {'parent': 'c4', 'pesan': 'fitur lagi'},
    }

""", '            ')

DATAK = """
commits = {
    'c1': {'parent': None, 'pesan': 'awal'},
    'c2': {'parent': 'c1', 'pesan': 'dua'},
    'c3': {'parent': 'c2', 'pesan': 'main'},
    'c4': {'parent': 'c2', 'pesan': 'fitur'},
    'c5': {'parent': 'c4', 'pesan': 'fitur lagi'},
}
"""

ANC = """
def leluhur_set(commits, ident):
    hasil = set()
    sekarang = ident
    while sekarang is not None:
        hasil.add(sekarang)
        sekarang = commits[sekarang]['parent']
    return hasil
"""

FF_FN = """
def bisa_fast_forward(commits, a, b):
    sekarang = b
    while sekarang is not None:
        if sekarang == a:
            return True
        sekarang = commits[sekarang]['parent']
    return False
"""

BASE_FN = """
def merge_base(commits, a, b):
    milik_b = set()
    sekarang = b
    while sekarang is not None:
        milik_b.add(sekarang)
        sekarang = commits[sekarang]['parent']
    sekarang = a
    while sekarang is not None:
        if sekarang in milik_b:
            return sekarang
        sekarang = commits[sekarang]['parent']
    return None
"""

JENIS_FN = BASE_FN + """

def jenis_merge(commits, a, b):
    dasar = merge_base(commits, a, b)
    if dasar == b:
        return 'sudah terbaru'
    if dasar == a:
        return 'fast-forward'
    return 'merge commit'
"""

GABUNG_FN = """
def gabung_file(basis, a, b):
    hasil = {}
    konflik = []
    for nama in sorted(set(basis) | set(a) | set(b)):
        v0, va, vb = basis.get(nama), a.get(nama), b.get(nama)
        if va == vb:
            pilih = va
        elif va == v0:
            pilih = vb
        elif vb == v0:
            pilih = va
        else:
            konflik.append(nama)
            continue
        if pilih is not None:
            hasil[nama] = pilih
    return (hasil, konflik)
"""

l1 = lesson(
    "A7-03-1",
    "Merge: fast-forward dan tiga arah",
    35,
    [
        "Membedakan fast-forward, merge commit, dan keadaan sudah terbaru",
        "Menemukan merge base dua cabang",
        "Menggabungkan snapshot file dengan aturan tiga arah",
        "Menjelaskan kapan penggabungan menimbulkan konflik",
    ],
    [
        T("""
        ## Menyatukan kembali dua jalur

        Cabang membuat pekerjaan paralel menjadi mudah, dan **merge** menyatukan hasilnya. Perintah `git merge fitur` yang dijalankan dari cabang `main` memasukkan pekerjaan cabang `fitur` ke `main`. Bagian menariknya adalah bagaimana Git memutuskan apa yang masuk dan bagaimana ia mengenali bentrokan.

        Semua keputusan itu bertumpu pada graf commit yang sudah kita pelajari. Merge bukan penyalinan file, melainkan operasi yang membandingkan tiga snapshot dan menghasilkan satu commit baru.
        """),
        T("""
        ## Fast-forward

        Kasus paling sederhana terjadi ketika `main` tidak bergerak sejak cabang `fitur` dibuat. Commit ujung `main` adalah leluhur ujung `fitur`, sehingga tidak ada yang perlu digabung. Git cukup memajukan penunjuk `main` ke ujung `fitur`, yang disebut **fast-forward**. Tidak ada commit baru dibuat dan riwayat tetap garis lurus.

        Git menolak membuat commit merge ketika fast-forward cukup, kecuali kita meminta lewat opsi `--no-ff`.
        """),
        T("""
        ## Merge commit

        Bila kedua cabang sama-sama bergerak, fast-forward tidak mungkin. Git membuat **merge commit**, yaitu commit baru dengan dua induk: ujung cabang kita dan ujung cabang yang digabung. Snapshot-nya adalah hasil penggabungan perubahan kedua sisi.

        Merge commit mengikat dua jalur riwayat sehingga graf tidak lagi garis lurus. Itulah sebabnya riwayat proyek yang aktif tampak seperti rel kereta dengan percabangan dan pertemuan.
        """),
        T("""
        ## Merge base

        Untuk menggabungkan dengan cerdas, Git perlu tahu dari mana kedua jalur berpisah. Titik itu disebut **merge base**, yaitu leluhur bersama terdekat dari kedua ujung cabang. Perubahan tiap sisi dihitung relatif terhadap merge base: apa yang kita ubah sejak berpisah, dan apa yang mereka ubah sejak berpisah.

        Tanpa merge base, Git tidak dapat membedakan perubahan dari keadaan awal. Itulah mengapa penggabungan disebut tiga arah: basis, sisi kita, dan sisi mereka.
        """),
        C(
            J(DATAK, """

            def merge_base(commits, a, b):
                milik_b = set()
                sekarang = b
                while sekarang is not None:
                    milik_b.add(sekarang)
                    sekarang = commits[sekarang]['parent']
                sekarang = a
                while sekarang is not None:
                    if sekarang in milik_b:
                        return sekarang
                    sekarang = commits[sekarang]['parent']
                return None

            print(merge_base(commits, 'c3', 'c5'))
            print(merge_base(commits, 'c2', 'c5'))
            print(merge_base(commits, 'c3', 'c3'))
            print(merge_base(commits, 'c5', 'c1'))
            """),
            """
            c2
            c2
            c3
            c1
            """,
            """
            Cabang main dan fitur berpisah di commit kedua. Bila satu ujung adalah leluhur yang lain, merge base adalah ujung yang lebih lama.
            """,
            filename="merge_base.py",
        ),
        T("""
        ## Menentukan jenis merge

        Dari merge base kita dapat menyimpulkan jenis penggabungan. Bila merge base sama dengan ujung cabang yang hendak digabung, semuanya sudah ada di cabang kita dan tidak ada yang perlu dilakukan. Bila merge base sama dengan ujung cabang kita, fast-forward cukup. Selain itu, dibutuhkan merge commit sungguhan.

        Tiga keadaan ini adalah seluruh keputusan awal `git merge`. Sisanya adalah menggabungkan isi file.
        """),
        C(
            J(DATAK, """

            def merge_base(commits, a, b):
                milik_b = set()
                sekarang = b
                while sekarang is not None:
                    milik_b.add(sekarang)
                    sekarang = commits[sekarang]['parent']
                sekarang = a
                while sekarang is not None:
                    if sekarang in milik_b:
                        return sekarang
                    sekarang = commits[sekarang]['parent']
                return None

            def jenis_merge(commits, a, b):
                dasar = merge_base(commits, a, b)
                if dasar == b:
                    return 'sudah terbaru'
                if dasar == a:
                    return 'fast-forward'
                return 'merge commit'

            print(jenis_merge(commits, 'c2', 'c5'))
            print(jenis_merge(commits, 'c3', 'c5'))
            print(jenis_merge(commits, 'c5', 'c2'))
            """),
            """
            fast-forward
            merge commit
            sudah terbaru
            """,
            """
            Menggabungkan fitur ke commit kedua cukup fast-forward. Menggabungkannya ke main yang sudah bergerak butuh merge commit, dan menggabungkan leluhur tidak mengubah apa-apa.
            """,
            filename="jenis_merge.py",
        ),
        T("""
        ## Penggabungan tiga arah pada file

        Untuk setiap file, Git membandingkan tiga versi: basis, sisi kita, dan sisi mereka. Bila kedua sisi sama, pakai itu. Bila hanya sisi mereka yang berubah dari basis, ambil versi mereka. Bila hanya sisi kita yang berubah, pertahankan versi kita. Bila kedua sisi berubah dengan cara berbeda, terjadi **konflik** yang harus diselesaikan manusia.

        Aturan sederhana ini menyelesaikan sebagian besar penggabungan otomatis, dan hanya perubahan yang benar-benar bertabrakan yang diserahkan kepada kita.
        """),
        C(
            """
            def gabung_file(basis, a, b):
                hasil = {}
                konflik = []
                for nama in sorted(set(basis) | set(a) | set(b)):
                    v0, va, vb = basis.get(nama), a.get(nama), b.get(nama)
                    if va == vb:
                        pilih = va
                    elif va == v0:
                        pilih = vb
                    elif vb == v0:
                        pilih = va
                    else:
                        konflik.append(nama)
                        continue
                    if pilih is not None:
                        hasil[nama] = pilih
                return (hasil, konflik)

            basis = {'a.py': '1', 'b.py': '1', 'c.py': '1'}
            kita = {'a.py': '2', 'b.py': '1', 'c.py': '2'}
            mereka = {'a.py': '1', 'b.py': '2', 'c.py': '3', 'd.py': 'baru'}
            print(gabung_file(basis, kita, mereka))
            print(gabung_file(basis, {'a.py': '1', 'c.py': '1'}, basis))
            """,
            """
            ({'a.py': '2', 'b.py': '2', 'd.py': 'baru'}, ['c.py'])
            ({'a.py': '1', 'c.py': '1'}, [])
            """,
            """
            File a hanya berubah di sisi kita, b hanya di sisi mereka, dan d ditambah mereka. File c diubah kedua sisi secara berbeda sehingga konflik. Penghapusan satu sisi diterima bila sisi lain tidak mengubahnya.
            """,
            filename="gabung_file.py",
        ),
        T("""
        ## Perintah merge

        ```bash
        git switch main
        git merge fitur
        git merge --no-ff fitur
        git merge --abort
        git branch -d fitur
        ```

        Pindah dulu ke cabang yang akan menerima, lalu jalankan `git merge` dengan nama cabang sumber. Opsi `--abort` membatalkan penggabungan yang sedang berlangsung dan mengembalikan keadaan semula, berguna ketika konflik terasa terlalu rumit untuk diselesaikan sekarang.
        """),
        T("""
        ## Merge atau rebase

        Ada cara lain mengintegrasikan perubahan: **rebase**. Alih-alih membuat merge commit, rebase memutar ulang commit cabang kita di atas ujung cabang tujuan, menghasilkan riwayat garis lurus. Hasilnya rapi, tetapi commit yang diputar ulang mendapat hash baru, jadi rebase menulis ulang riwayat.

        Aturan praktis: rebase untuk merapikan pekerjaan lokal sebelum dibagikan, merge untuk menggabungkan pekerjaan yang sudah dibagikan. Tim berbeda memilih konvensi berbeda, jadi ikuti kesepakatan tim Anda.
        """),
        K(
            "tip",
            """
            Sebelum merge, pastikan working directory bersih dan cabang tujuan terbaru. Penggabungan di atas pekerjaan yang belum dicommit mempersulit pembatalan.
            """,
            title="Persiapan merge",
        ),
        T("""
        ## Merge dan riwayat yang terbaca

        Setelah penggabungan selesai, cabang fitur biasanya dihapus karena tugasnya selesai. Commit-commitnya tidak hilang, sebab masih terjangkau lewat merge commit. Yang hilang hanyalah nama cabang, sehingga daftar cabang tetap ringkas.
        """),
        E(
            "A7-03-1-ex1",
            "mudah",
            """
            Tulis fungsi `bisa_fast_forward(commits, a, b)` yang mengembalikan `True` bila commit `a` adalah leluhur dari `b` (atau sama dengan `b`) sehingga menggabungkan `b` ke `a` cukup fast-forward, dan `False` bila tidak.
            """,
            """
            def bisa_fast_forward(commits, a, b):
                # TODO: implementasikan
                pass
            """,
            FIXK + """
            k = _k()
            assert bisa_fast_forward(k, 'c2', 'c5') is True
            assert bisa_fast_forward(k, 'c3', 'c5') is False
            assert bisa_fast_forward(k, 'c5', 'c2') is False
            assert bisa_fast_forward(k, 'c4', 'c4') is True
            """,
            "Telusuri induk dari b dan cari a.",
            FF_FN.strip("\n"),
        ),
        E(
            "A7-03-1-ex2",
            "sedang",
            """
            Tulis fungsi `merge_base(commits, a, b)` yang mengembalikan id leluhur bersama terdekat dari commit `a` dan `b` (commit sendiri dihitung sebagai leluhurnya), atau `None` bila tidak ada.
            """,
            """
            def merge_base(commits, a, b):
                # TODO: implementasikan
                pass
            """,
            FIXK + """
            k = _k()
            assert merge_base(k, 'c3', 'c5') == 'c2'
            assert merge_base(k, 'c2', 'c5') == 'c2'
            assert merge_base(k, 'c3', 'c3') == 'c3'
            k['x1'] = {'parent': None, 'pesan': 'lain'}
            assert merge_base(k, 'x1', 'c5') is None
            """,
            "Kumpulkan leluhur b lalu telusuri a sampai menemukan yang ada di himpunan itu.",
            BASE_FN.strip("\n"),
        ),
        E(
            "A7-03-1-ex3",
            "sedang",
            """
            Tulis fungsi `jenis_merge(commits, a, b)` untuk menggabungkan `b` ke `a`. Kembalikan `'sudah terbaru'` bila `b` leluhur `a` (atau sama), `'fast-forward'` bila `a` leluhur `b`, dan `'merge commit'` selain itu.
            """,
            """
            def jenis_merge(commits, a, b):
                # TODO: implementasikan
                pass
            """,
            FIXK + """
            k = _k()
            assert jenis_merge(k, 'c2', 'c5') == 'fast-forward'
            assert jenis_merge(k, 'c3', 'c5') == 'merge commit'
            assert jenis_merge(k, 'c5', 'c2') == 'sudah terbaru'
            assert jenis_merge(k, 'c3', 'c3') == 'sudah terbaru'
            """,
            "Cari merge base lalu bandingkan dengan a dan b.",
            JENIS_FN.strip("\n"),
        ),
        E(
            "A7-03-1-ex4",
            "menantang",
            """
            Tulis fungsi `gabung_file(basis, a, b)` yang menerima tiga dict `{nama: isi}` (basis, sisi kita, sisi mereka) dan mengembalikan tuple `(hasil, konflik)`. Per file: bila `a` dan `b` sama pakai itu, bila hanya `b` berubah dari basis pakai `b`, bila hanya `a` berubah pakai `a`, selain itu masukkan nama ke list `konflik` terurut. File yang nilainya akhirnya tidak ada tidak dimasukkan ke `hasil`.
            """,
            """
            def gabung_file(basis, a, b):
                # TODO: implementasikan
                pass
            """,
            """
            basis = {'a': '1', 'b': '1', 'c': '1'}
            kita = {'a': '2', 'b': '1', 'c': '2'}
            mereka = {'a': '1', 'b': '2', 'c': '3', 'd': 'baru'}
            assert gabung_file(basis, kita, mereka) == ({'a': '2', 'b': '2', 'd': 'baru'}, ['c'])
            assert gabung_file(basis, {'a': '1', 'c': '1'}, basis) == ({'a': '1', 'c': '1'}, [])
            assert gabung_file({}, {'x': '1'}, {'x': '2'}) == ({}, ['x'])
            assert gabung_file({'x': '1'}, {}, {}) == ({}, [])
            """,
            "Bandingkan versi basis, kita, dan mereka untuk setiap nama file.",
            GABUNG_FN.strip("\n"),
        ),
    ],
    [
        M("Mengira merge selalu membuat commit baru.", "Bila fast-forward cukup, hanya penunjuk yang maju."),
        M("Menggabungkan tanpa tahu merge base.", "Perubahan dihitung relatif terhadap leluhur bersama."),
        M("Melakukan rebase pada riwayat yang sudah dibagikan.", "Rebase hanya untuk pekerjaan lokal."),
    ],
    [
        Q("Fast-forward terjadi bila?", ["Cabang tujuan adalah leluhur cabang sumber", "Ada konflik", "Cabang dihapus", "Tag dibuat"], 0, "Cukup memajukan penunjuk.", hint="Leluhur."),
        Q("Merge commit memiliki?", ["Dua induk", "Satu induk", "Tanpa induk", "Tiga induk"], 0, "Menyatukan dua jalur.", hint="Dua."),
        Q("Merge base adalah?", ["Leluhur bersama terdekat", "Commit terbaru", "Cabang utama", "Tag pertama"], 0, "Titik berpisah.", hint="Bersama."),
        Q("Konflik terjadi bila?", ["Kedua sisi mengubah bagian sama secara berbeda", "Satu sisi berubah", "File dihapus semua", "Tidak ada perubahan"], 0, "Bentrok.", hint="Berbeda."),
        Q("Rebase menghasilkan?", ["Riwayat garis lurus dengan hash baru", "Merge commit", "Tag", "Cabang baru"], 0, "Menulis ulang riwayat.", hint="Lurus."),
    ],
    [
        "Merge dapat berupa fast-forward, merge commit, atau tidak perlu apa-apa.",
        "Merge base adalah leluhur bersama yang menjadi acuan perubahan.",
        "Penggabungan tiga arah menyelesaikan otomatis perubahan yang tidak bertabrakan.",
        "Rebase menulis ulang riwayat, jadi hanya untuk pekerjaan lokal.",
    ],
    [],
)

MARK_FN = """
def ada_konflik(teks):
    baris = teks.splitlines()
    return any(b.startswith('<<<<<<<') for b in baris) and any(b.startswith('>>>>>>>') for b in baris)
"""

GBARIS_FN = """
def gabung_baris(basis, a, b, nama='fitur'):
    x0, xa, xb = basis.splitlines(), a.splitlines(), b.splitlines()
    if not (len(x0) == len(xa) == len(xb)):
        raise ValueError('jumlah baris berbeda')
    hasil = []
    konflik = 0
    for v0, va, vb in zip(x0, xa, xb):
        if va == vb:
            hasil.append(va)
        elif va == v0:
            hasil.append(vb)
        elif vb == v0:
            hasil.append(va)
        else:
            hasil += ['<<<<<<< HEAD', va, '=======', vb, '>>>>>>> ' + nama]
            konflik += 1
    return ('\\n'.join(hasil), konflik)
"""

SELESAI_FN = """
def selesaikan(teks, pilihan):
    hasil = []
    mode = None
    indeks = 0
    for b in teks.splitlines():
        if b.startswith('<<<<<<<'):
            mode = 'kita'
        elif b.startswith('=======') and mode == 'kita':
            mode = 'mereka'
        elif b.startswith('>>>>>>>') and mode == 'mereka':
            mode = None
            indeks += 1
        elif mode is None:
            hasil.append(b)
        else:
            p = pilihan[indeks]
            if p == 'keduanya' or p == mode:
                hasil.append(b)
    return '\\n'.join(hasil)
"""

DATAT = """
basis = 'judul\\nrata-rata = 10\\nbatas = 5'
kita = 'judul\\nrata-rata = 12\\nbatas = 5'
mereka = 'judul baru\\nrata-rata = 15\\nbatas = 5'
"""

l2 = lesson(
    "A7-03-2",
    "Konflik: membaca dan menyelesaikannya",
    35,
    [
        "Mengenali penanda konflik pada file",
        "Menggabungkan teks per baris dan menghasilkan penanda konflik",
        "Menyelesaikan konflik dengan memilih salah satu sisi atau keduanya",
        "Menerapkan langkah aman saat menghadapi konflik",
    ],
    [
        T("""
        ## Konflik bukan bencana

        Konflik terdengar menakutkan, tetapi sebenarnya hanya cara Git berkata bahwa ia tidak dapat memutuskan sendiri. Dua orang mengubah baris yang sama dengan cara berbeda, dan Git menyerahkan keputusan kepada manusia. Ia tidak menghapus apa pun: kedua versi disimpan di file dengan penanda khusus.

        Konflik adalah bagian normal dari kerja tim. Yang membedakan pengguna berpengalaman adalah ketenangan: mereka tahu cara membaca penanda dan menyelesaikannya langkah demi langkah.
        """),
        T("""
        ## Penanda konflik

        Ketika konflik terjadi, Git menulis kedua versi ke dalam file dengan tiga penanda. Baris `<<<<<<< HEAD` membuka bagian milik sisi kita, baris `=======` memisahkan, dan baris `>>>>>>> nama-cabang` menutup bagian milik cabang yang digabung.

        ```text
        <<<<<<< HEAD
        rata-rata = 12
        =======
        rata-rata = 15
        >>>>>>> fitur
        ```

        Tugas kita adalah mengedit bagian itu menjadi isi akhir yang diinginkan dan menghapus ketiga penanda.
        """),
        T("""
        ## Penggabungan per baris

        Pada tingkat baris, aturan tiga arah sama seperti pada tingkat file. Bila kedua sisi mengubah baris yang sama dengan isi berbeda, terjadi konflik. Bila hanya satu sisi mengubahnya, perubahan itu diterima. Git sungguhan memakai algoritma diff untuk menyelaraskan baris yang bergeser, tetapi model kita menyederhanakannya dengan mengasumsikan jumlah baris sama.

        Asumsi itu cukup untuk memahami prinsipnya: perubahan di baris berbeda digabung otomatis, perubahan di baris yang sama berbenturan.
        """),
        C(
            J(DATAT, """

            def gabung_baris(basis, a, b, nama='fitur'):
                x0, xa, xb = basis.splitlines(), a.splitlines(), b.splitlines()
                if not (len(x0) == len(xa) == len(xb)):
                    raise ValueError('jumlah baris berbeda')
                hasil = []
                konflik = 0
                for v0, va, vb in zip(x0, xa, xb):
                    if va == vb:
                        hasil.append(va)
                    elif va == v0:
                        hasil.append(vb)
                    elif vb == v0:
                        hasil.append(va)
                    else:
                        hasil += ['<<<<<<< HEAD', va, '=======', vb, '>>>>>>> ' + nama]
                        konflik += 1
                return ('\\n'.join(hasil), konflik)

            teks, n = gabung_baris(basis, kita, mereka)
            print(n)
            print(teks)
            """),
            """
            1
            judul baru
            <<<<<<< HEAD
            rata-rata = 12
            =======
            rata-rata = 15
            >>>>>>> fitur
            batas = 5
            """,
            """
            Judul hanya diubah di sisi mereka sehingga diterima otomatis. Baris rata-rata diubah kedua sisi berbeda sehingga ditulis dengan penanda konflik.
            """,
            filename="gabung_baris.py",
        ),
        T("""
        ## Langkah menyelesaikan konflik

        Pertama, jalankan `git status` untuk melihat file mana yang berkonflik. Kedua, buka tiap file, cari penanda, dan putuskan isi akhir: ambil versi kita, versi mereka, gabungan keduanya, atau tulis baru. Ketiga, hapus semua penanda. Keempat, jalankan `git add` pada file itu untuk menandainya selesai, lalu `git commit` untuk menyelesaikan penggabungan.

        Banyak editor dan alat grafis menampilkan konflik berdampingan sehingga keputusan lebih mudah. Apa pun alatnya, hasil akhirnya tetap teks tanpa penanda.
        """),
        C(
            """
            def selesaikan(teks, pilihan):
                hasil = []
                mode = None
                indeks = 0
                for b in teks.splitlines():
                    if b.startswith('<<<<<<<'):
                        mode = 'kita'
                    elif b.startswith('=======') and mode == 'kita':
                        mode = 'mereka'
                    elif b.startswith('>>>>>>>') and mode == 'mereka':
                        mode = None
                        indeks += 1
                    elif mode is None:
                        hasil.append(b)
                    else:
                        p = pilihan[indeks]
                        if p == 'keduanya' or p == mode:
                            hasil.append(b)
                return '\\n'.join(hasil)

            teks = 'a\\n<<<<<<< HEAD\\nkita\\n=======\\nmereka\\n>>>>>>> fitur\\nz'
            print(selesaikan(teks, ['kita']).splitlines())
            print(selesaikan(teks, ['mereka']).splitlines())
            print(selesaikan(teks, ['keduanya']).splitlines())
            """,
            """
            ['a', 'kita', 'z']
            ['a', 'mereka', 'z']
            ['a', 'kita', 'mereka', 'z']
            """,
            """
            Memilih sisi kita, sisi mereka, atau keduanya menghasilkan teks bersih tanpa penanda konflik.
            """,
            filename="selesaikan_konflik.py",
        ),
        T("""
        ## Mendeteksi sisa penanda

        Kesalahan klasik adalah mencommit file yang masih berisi penanda konflik. Kode seperti itu tidak akan berjalan, dan lebih buruk lagi, penanda dapat tersimpan di riwayat tanpa disadari. Periksa dengan mencari awalan `<<<<<<<` dan `>>>>>>>` sebelum commit.

        Banyak tim memasang pemeriksaan otomatis yang menolak commit yang masih memuat penanda. Pemeriksaan kecil seperti ini menyelamatkan banyak waktu.
        """),
        C(
            """
            def ada_konflik(teks):
                baris = teks.splitlines()
                return any(b.startswith('<<<<<<<') for b in baris) and any(b.startswith('>>>>>>>') for b in baris)

            print(ada_konflik('a\\n<<<<<<< HEAD\\nx\\n=======\\ny\\n>>>>>>> f'))
            print(ada_konflik('a\\nb\\nc'))
            print(ada_konflik('perbandingan a >>>>>>> b'))
            """,
            """
            True
            False
            False
            """,
            """
            Pemeriksaan hanya menganggap konflik bila ada penanda pembuka dan penutup di awal baris, sehingga teks biasa yang kebetulan mengandung tanda lebih besar tidak salah dikenali.
            """,
            filename="ada_konflik.py",
        ),
        T("""
        ## Mencegah konflik

        Konflik tidak dapat dihindari sepenuhnya, tetapi dapat dikurangi. Sering-seringlah menarik perubahan terbaru dari cabang utama, sehingga cabang kita tidak menyimpang terlalu jauh. Bagi pekerjaan agar orang berbeda mengerjakan file berbeda. Komunikasikan bila akan mengubah berkas yang dipakai bersama.

        Format kode otomatis yang konsisten juga membantu, karena perbedaan spasi dan tanda kutip yang tidak penting tidak lagi menimbulkan konflik palsu.
        """),
        T("""
        ## Konflik pada notebook dan data

        File notebook Jupyter berisi JSON dengan banyak metadata dan keluaran, sehingga dua orang yang menjalankan sel yang sama memicu konflik besar walau isi kodenya tidak berubah. Cara mengurangi: bersihkan keluaran sebelum commit, dan simpan logika penting di skrip atau modul yang diimpor notebook.

        File data biner tidak dapat digabung per baris sama sekali. Untuk itu, tentukan siapa yang berwenang mengubahnya, atau simpan di luar repositori.
        """),
        K(
            "warn",
            """
            Jangan mencommit file yang masih memuat penanda konflik. Cari awalan penanda sebelum commit.
            """,
            title="Sisa penanda",
        ),
        T("""
        ## Memahami maksud kedua sisi

        Menyelesaikan konflik bukan sekadar memilih salah satu baris. Pahami mengapa kedua orang mengubahnya. Mungkin kedua perubahan benar dan perlu digabungkan, mungkin salah satu sudah usang, atau mungkin keduanya perlu diganti dengan penyelesaian baru. Bila ragu, tanyakan kepada rekan yang mengubahnya.

        Penyelesaian yang dibuat tanpa memahami maksud sering melahirkan bug halus yang baru muncul berminggu-minggu kemudian.
        """),
        T("""
        ## Menguji setelah menyelesaikan

        Setelah konflik diselesaikan, jalankan kode atau analisis sebelum commit. Teks yang tampak benar belum tentu berjalan benar, terutama bila dua perubahan yang masing-masing valid ternyata tidak cocok bila digabung. Pengujian singkat setelah merge adalah asuransi murah terhadap kejutan.
        """),
        T("""
        ## Alat bantu penyelesaian

        Banyak editor kode menyorot konflik dan menyediakan tombol untuk menerima perubahan kita, perubahan mereka, atau keduanya. Alat tiga panel menampilkan basis, kedua sisi, dan hasil akhir sekaligus. Alat ini mempercepat pekerjaan, tetapi keputusan tetap berada di tangan kita.
        """),
        E(
            "A7-03-2-ex1",
            "mudah",
            """
            Tulis fungsi `ada_konflik(teks)` yang mengembalikan `True` bila ada baris yang diawali `<<<<<<<` dan ada baris yang diawali `>>>>>>>`, dan `False` bila tidak.
            """,
            """
            def ada_konflik(teks):
                # TODO: implementasikan
                pass
            """,
            """
            assert ada_konflik('a\\n<<<<<<< HEAD\\nx\\n=======\\ny\\n>>>>>>> f') is True
            assert ada_konflik('a\\nb') is False
            assert ada_konflik('x >>>>>>> y') is False
            assert ada_konflik('<<<<<<< HEAD') is False
            """,
            "Periksa awalan setiap baris dengan startswith.",
            MARK_FN.strip("\n"),
        ),
        E(
            "A7-03-2-ex2",
            "sedang",
            """
            Tulis fungsi `gabung_baris(basis, a, b, nama='fitur')` untuk teks dengan jumlah baris sama (jika berbeda lemparkan `ValueError`). Per baris: bila `a` dan `b` sama pakai itu, bila hanya `b` berubah dari basis pakai `b`, bila hanya `a` berubah pakai `a`, selain itu tulis lima baris `<<<<<<< HEAD`, baris `a`, `=======`, baris `b`, dan `>>>>>>> ` diikuti `nama`. Kembalikan tuple `(teks_gabungan, jumlah_konflik)` dengan baris digabung `\\n`.
            """,
            """
            def gabung_baris(basis, a, b, nama='fitur'):
                # TODO: implementasikan
                pass
            """,
            """
            basis = 'j\\nr = 10\\nb = 5'
            kita = 'j\\nr = 12\\nb = 5'
            mereka = 'j2\\nr = 15\\nb = 5'
            teks, n = gabung_baris(basis, kita, mereka)
            assert n == 1
            assert teks == 'j2\\n<<<<<<< HEAD\\nr = 12\\n=======\\nr = 15\\n>>>>>>> fitur\\nb = 5'
            assert gabung_baris(basis, basis, basis) == (basis, 0)
            assert gabung_baris(basis, kita, basis, 'x') == (kita, 0)
            try:
                gabung_baris('a', 'a\\nb', 'a')
                ditolak = False
            except ValueError:
                ditolak = True
            assert ditolak is True
            """,
            "Periksa jumlah baris, lalu proses tiga baris sejajar dengan zip.",
            GBARIS_FN.strip("\n"),
        ),
        E(
            "A7-03-2-ex3",
            "sedang",
            """
            Tulis fungsi `selesaikan(teks, pilihan)` yang menghapus penanda konflik dari `teks` dan menyisakan bagian yang dipilih. `pilihan` adalah list dengan satu elemen per konflik, berisi `'kita'`, `'mereka'`, atau `'keduanya'`. Baris di luar konflik selalu dipertahankan. Kembalikan teks dengan baris digabung `\\n`.
            """,
            """
            def selesaikan(teks, pilihan):
                # TODO: implementasikan
                pass
            """,
            """
            t = 'a\\n<<<<<<< HEAD\\nkita\\n=======\\nmereka\\n>>>>>>> f\\nz'
            assert selesaikan(t, ['kita']) == 'a\\nkita\\nz'
            assert selesaikan(t, ['mereka']) == 'a\\nmereka\\nz'
            assert selesaikan(t, ['keduanya']) == 'a\\nkita\\nmereka\\nz'
            assert selesaikan('x\\ny', []) == 'x\\ny'
            """,
            "Lacak mode kita atau mereka saat membaca baris antar penanda.",
            SELESAI_FN.strip("\n"),
        ),
        E(
            "A7-03-2-ex4",
            "menantang",
            """
            Tulis fungsi `selesaikan_banyak(teks, pilihan)` untuk teks dengan beberapa konflik, memakai logika yang sama dengan `selesaikan` (satu pilihan per konflik berurutan). Fungsi harus melempar `ValueError` bila jumlah konflik di teks tidak sama dengan panjang `pilihan`.
            """,
            """
            def selesaikan_banyak(teks, pilihan):
                # TODO: implementasikan
                pass
            """,
            """
            t = 'a\\n<<<<<<< HEAD\\n1\\n=======\\n2\\n>>>>>>> f\\nb\\n<<<<<<< HEAD\\n3\\n=======\\n4\\n>>>>>>> f\\nz'
            assert selesaikan_banyak(t, ['kita', 'mereka']) == 'a\\n1\\nb\\n4\\nz'
            assert selesaikan_banyak(t, ['keduanya', 'kita']) == 'a\\n1\\n2\\nb\\n3\\nz'
            for salah in (['kita'], ['kita', 'kita', 'kita']):
                try:
                    selesaikan_banyak(t, salah)
                    ditolak = False
                except ValueError:
                    ditolak = True
                assert ditolak is True
            """,
            "Hitung jumlah penanda pembuka dan cocokkan dengan panjang pilihan sebelum memproses.",
            SELESAI_FN.strip("\n").replace("def selesaikan(teks, pilihan):\n", "def selesaikan_banyak(teks, pilihan):\n    jumlah = sum(1 for b in teks.splitlines() if b.startswith('<<<<<<<'))\n    if jumlah != len(pilihan):\n        raise ValueError('jumlah pilihan tidak sama')\n", 1),
        ),
    ],
    [
        M("Panik dan menghapus file saat melihat konflik.", "Baca penanda dan pilih isi akhir."),
        M("Mencommit file yang masih berpenanda.", "Cari awalan penanda sebelum commit."),
        M("Membiarkan cabang menyimpang berminggu-minggu.", "Tarik perubahan terbaru sering-sering."),
    ],
    [
        Q("Penanda pembuka konflik?", ["<<<<<<< HEAD", "=======", ">>>>>>>", "#####"], 0, "Membuka bagian sisi kita.", hint="Kurung kiri."),
        Q("Garis pemisah dua versi?", ["=======", "<<<<<<<", ">>>>>>>", "-------"], 0, "Di tengah.", hint="Sama dengan."),
        Q("Setelah menyelesaikan konflik, jalankan?", ["git add lalu git commit", "git reset", "git clone", "git init"], 0, "Menandai selesai.", hint="Add."),
        Q("Konflik di notebook sering akibat?", ["Keluaran dan metadata", "Nama file", "Ukuran disk", "Nama cabang"], 0, "JSON besar.", hint="Keluaran."),
        Q("Cara mengurangi konflik?", ["Sering menarik perubahan terbaru", "Menunda merge", "Mengubah file sama bersamaan", "Menghapus riwayat"], 0, "Cabang tidak menyimpang jauh.", hint="Sering."),
    ],
    [
        "Konflik muncul ketika kedua sisi mengubah bagian yang sama secara berbeda.",
        "Penanda konflik memisahkan versi kita dan versi mereka.",
        "Selesaikan dengan memilih isi akhir, menghapus penanda, add, lalu commit.",
        "Kurangi konflik dengan integrasi sering dan pembagian kerja.",
    ],
    [],
)

AHEAD_FN = """
def ahead_behind(commits, a, b):
    def telusur(ident):
        hasil = set()
        sekarang = ident
        while sekarang is not None:
            hasil.add(sekarang)
            sekarang = commits[sekarang]['parent']
        return hasil
    sa, sb = telusur(a), telusur(b)
    return (len(sa - sb), len(sb - sa))
"""

BISA_PUSH_FN = """
def bisa_push(commits, lokal, remote):
    if remote is None:
        return True
    sekarang = lokal
    while sekarang is not None:
        if sekarang == remote:
            return True
        sekarang = commits[sekarang]['parent']
    return False
"""

PUSH_FN = """
def push(lokal, remote, cabang):
    tip = lokal['cabang'][cabang]
    tip_remote = remote['cabang'].get(cabang)
    boleh = tip_remote is None
    sekarang = tip
    while sekarang is not None and not boleh:
        if sekarang == tip_remote:
            boleh = True
        sekarang = lokal['commits'][sekarang]['parent']
    if not boleh:
        raise ValueError('ditolak: tarik dan gabung dulu')
    remote['commits'].update(lokal['commits'])
    remote['cabang'][cabang] = tip
    return tip
"""

FETCH_FN = """
def fetch(lokal, remote):
    baru = sorted(i for i in remote['commits'] if i not in lokal['commits'])
    for i in baru:
        lokal['commits'][i] = remote['commits'][i]
    for nama, tip in remote['cabang'].items():
        lokal['cabang']['origin/' + nama] = tip
    return baru
"""

FIXL = textwrap.indent("""def _lokal():
    k = {
        'c1': {'parent': None, 'pesan': 'awal'},
        'c2': {'parent': 'c1', 'pesan': 'dua'},
        'c4': {'parent': 'c2', 'pesan': 'fitur'},
        'c5': {'parent': 'c4', 'pesan': 'fitur lagi'},
    }
    return {'commits': k, 'cabang': {'main': 'c5'}}

def _remote(tip, ids):
    semua = {
        'c1': {'parent': None, 'pesan': 'awal'},
        'c2': {'parent': 'c1', 'pesan': 'dua'},
        'c3': {'parent': 'c2', 'pesan': 'main'},
    }
    return {'commits': {i: semua[i] for i in ids}, 'cabang': {'main': tip}}

""", '            ')

l3 = lesson(
    "A7-03-3",
    "Kolaborasi: remote, push, dan pull",
    35,
    [
        "Menjelaskan repositori jarak jauh dan cabang pelacak",
        "Membedakan fetch, pull, dan push",
        "Menghitung berapa commit lokal di depan dan di belakang remote",
        "Menjelaskan alur kerja pull request dan etika kolaborasi",
    ],
    [
        T("""
        ## Repositori jarak jauh

        Sampai sekarang kita bekerja dengan satu repositori lokal. Kolaborasi menambahkan **remote**, yaitu salinan repositori yang tersimpan di server, misalnya GitHub atau GitLab. Remote utama biasanya bernama `origin`. Setiap anggota tim memiliki salinan lokal lengkap dan menyinkronkannya dengan remote.

        Karena setiap salinan memuat seluruh riwayat, Git bersifat terdistribusi: kita dapat bekerja tanpa internet dan baru menyinkronkan ketika siap.
        """),
        T("""
        ## Cabang pelacak

        Cabang `origin/main` di salinan lokal bukan cabang yang kita edit, melainkan **cabang pelacak**: catatan lokal tentang posisi `main` di remote terakhir kali kita berkomunikasi. Ia hanya bergerak ketika kita menyinkronkan, bukan ketika orang lain melakukan push.

        Dengan membandingkan `main` lokal dengan `origin/main`, kita dapat tahu apakah kita di depan, di belakang, atau sudah menyimpang dari remote.
        """),
        T("""
        ## Fetch, pull, dan push

        `git fetch` mengunduh commit baru dari remote dan memperbarui cabang pelacak, tanpa mengubah pekerjaan kita. `git pull` adalah fetch diikuti merge cabang pelacak ke cabang aktif. `git push` mengirim commit lokal ke remote.

        ```bash
        git clone https://contoh.id/proyek.git
        git fetch origin
        git pull origin main
        git push origin main
        ```

        Pemula sering langsung memakai pull. Kebiasaan yang lebih hati-hati adalah fetch dahulu, lihat apa yang masuk, baru gabungkan.
        """),
        C(
            """
            def fetch(lokal, remote):
                baru = sorted(i for i in remote['commits'] if i not in lokal['commits'])
                for i in baru:
                    lokal['commits'][i] = remote['commits'][i]
                for nama, tip in remote['cabang'].items():
                    lokal['cabang']['origin/' + nama] = tip
                return baru

            lokal = {'commits': {'c1': {'parent': None, 'pesan': 'a'}}, 'cabang': {'main': 'c1'}}
            remote = {'commits': {'c1': {'parent': None, 'pesan': 'a'}, 'c2': {'parent': 'c1', 'pesan': 'b'}}, 'cabang': {'main': 'c2'}}
            print(fetch(lokal, remote))
            print(lokal['cabang'])
            print(fetch(lokal, remote))
            """,
            """
            ['c2']
            {'main': 'c1', 'origin/main': 'c2'}
            []
            """,
            """
            Fetch membawa commit baru dan memajukan origin/main, tetapi main lokal tidak berubah. Fetch kedua tidak menemukan apa-apa baru.
            """,
            filename="fetch.py",
        ),
        T("""
        ## Di depan dan di belakang

        Setelah fetch, kita dapat menghitung selisih antara cabang lokal dan pelacaknya. **Ahead** adalah jumlah commit yang kita miliki tetapi belum ada di remote, dan **behind** adalah jumlah commit di remote yang belum kita miliki. Keduanya muncul di `git status` sebagai kalimat seperti "ahead by 2 commits".

        Bila behind nol dan ahead positif, push akan lancar. Bila keduanya positif, riwayat menyimpang dan kita harus menggabungkan dulu.
        """),
        C(
            """
            def ahead_behind(commits, a, b):
                def telusur(ident):
                    hasil = set()
                    sekarang = ident
                    while sekarang is not None:
                        hasil.add(sekarang)
                        sekarang = commits[sekarang]['parent']
                    return hasil
                sa, sb = telusur(a), telusur(b)
                return (len(sa - sb), len(sb - sa))

            commits = {
                'c1': {'parent': None},
                'c2': {'parent': 'c1'},
                'c3': {'parent': 'c2'},
                'c4': {'parent': 'c2'},
                'c5': {'parent': 'c4'},
            }
            print(ahead_behind(commits, 'c3', 'c5'))
            print(ahead_behind(commits, 'c5', 'c3'))
            print(ahead_behind(commits, 'c2', 'c5'))
            print(ahead_behind(commits, 'c3', 'c3'))
            """,
            """
            (1, 2)
            (2, 1)
            (0, 2)
            (0, 0)
            """,
            """
            Cabang lokal di commit ketiga berada satu commit di depan dan dua commit di belakang remote di commit kelima, sehingga riwayatnya menyimpang.
            """,
            filename="ahead_behind.py",
        ),
        T("""
        ## Push ditolak

        Server menolak push bila akan menghilangkan commit milik orang lain. Secara teknis, push hanya diterima bila ujung remote adalah leluhur ujung kita, sehingga remote cukup maju cepat. Bila tidak, kita harus fetch, menggabungkan perubahan mereka ke pekerjaan kita, lalu push lagi.

        Penolakan ini melindungi kerja tim. Godaan memakai `git push --force` untuk memaksa harus dilawan, karena ia menimpa pekerjaan orang lain.
        """),
        C(
            """
            def push(lokal, remote, cabang):
                tip = lokal['cabang'][cabang]
                tip_remote = remote['cabang'].get(cabang)
                boleh = tip_remote is None
                sekarang = tip
                while sekarang is not None and not boleh:
                    if sekarang == tip_remote:
                        boleh = True
                    sekarang = lokal['commits'][sekarang]['parent']
                if not boleh:
                    raise ValueError('ditolak: tarik dan gabung dulu')
                remote['commits'].update(lokal['commits'])
                remote['cabang'][cabang] = tip
                return tip

            k = {
                'c1': {'parent': None},
                'c2': {'parent': 'c1'},
                'c3': {'parent': 'c2'},
                'c4': {'parent': 'c2'},
            }
            lokal = {'commits': k, 'cabang': {'main': 'c4'}}
            remote = {'commits': {i: k[i] for i in ('c1', 'c2')}, 'cabang': {'main': 'c2'}}
            print(push(lokal, remote, 'main'))
            print(sorted(remote['commits']))
            remote2 = {'commits': {i: k[i] for i in ('c1', 'c2', 'c3')}, 'cabang': {'main': 'c3'}}
            try:
                push(lokal, remote2, 'main')
            except ValueError as e:
                print(e)
            """,
            """
            c4
            ['c1', 'c2', 'c3', 'c4']
            ditolak: tarik dan gabung dulu
            """,
            """
            Push berhasil ketika remote hanya tertinggal, tetapi ditolak ketika remote punya commit yang tidak kita miliki.
            """,
            filename="push.py",
        ),
        T("""
        ## Pull request dan tinjauan kode

        Di platform seperti GitHub, kolaborasi biasanya lewat **pull request**. Kita mendorong cabang fitur ke remote, lalu membuka permintaan agar cabang itu digabung ke `main`. Rekan tim meninjau diff, memberi komentar, dan menyetujui, baru kemudian penggabungan dilakukan.

        Tinjauan kode menangkap kesalahan lebih awal dan menyebarkan pengetahuan. Untuk analisis data, ia memastikan logika perhitungan angka penting dilihat oleh lebih dari satu pasang mata.
        """),
        T("""
        ## Etika kolaborasi

        Beberapa kebiasaan membuat kerja tim lancar. Tarik perubahan terbaru sebelum mulai bekerja. Buat commit kecil dengan pesan jelas. Jangan mendorong langsung ke cabang utama bila tim memakai pull request. Jangan menulis ulang riwayat yang sudah dibagikan. Dan jangan pernah mendorong rahasia atau data pribadi.

        Etika ini sederhana tetapi menentukan: tim yang disiplin menghabiskan waktu untuk pekerjaan, bukan untuk memperbaiki kekacauan riwayat.
        """),
        T("""
        ## Fork dan kontribusi terbuka

        Pada proyek sumber terbuka, kita biasanya tidak punya izin menulis ke repositori utama. Solusinya adalah **fork**, yaitu menyalin repositori ke akun kita di server, bekerja di salinan itu, lalu mengajukan pull request ke repositori asli. Pemelihara memutuskan apakah perubahan diterima.

        Mekanisme ini memungkinkan ribuan orang berkontribusi tanpa memberi mereka kendali atas proyek, dan menjadi dasar kolaborasi terbuka di dunia perangkat lunak dan sains data.
        """),
        K(
            "warn",
            """
            Hindari git push --force pada cabang bersama. Ia dapat menimpa pekerjaan rekan tim.
            """,
            title="Push paksa",
        ),
        T("""
        ## Menyinkronkan dengan teratur

        Rutinitas sederhana mencegah banyak masalah: tarik di awal hari, dorong di akhir sesi kerja. Dengan begitu cadangan pekerjaan selalu ada di remote, dan rekan tim melihat kemajuan Anda lebih cepat. Pekerjaan yang hanya ada di satu laptop adalah pekerjaan yang berisiko hilang.
        """),
        T("""
        ## Cabang pelacak dan nama

        Saat cabang lokal dibuat dari cabang remote, Git dapat mengatur hubungan pelacakan sehingga status dan pull tahu pasangannya. Hubungan itu diatur dengan opsi `-u` saat push pertama. Setelahnya, perintah push dan pull tidak lagi memerlukan nama remote dan cabang secara eksplisit.
        """),
        E(
            "A7-03-3-ex1",
            "mudah",
            """
            Tulis fungsi `ahead_behind(commits, a, b)` yang mengembalikan tuple `(ahead, behind)`: `ahead` adalah jumlah commit yang terjangkau dari `a` tetapi tidak dari `b`, dan `behind` sebaliknya. Penelusuran mengikuti `parent`.
            """,
            """
            def ahead_behind(commits, a, b):
                # TODO: implementasikan
                pass
            """,
            FIXK + """
            k = _k()
            assert ahead_behind(k, 'c3', 'c5') == (1, 2)
            assert ahead_behind(k, 'c5', 'c3') == (2, 1)
            assert ahead_behind(k, 'c3', 'c3') == (0, 0)
            assert ahead_behind(k, 'c2', 'c5') == (0, 2)
            """,
            "Kumpulkan himpunan leluhur masing-masing lalu hitung selisih himpunan.",
            AHEAD_FN.strip("\n"),
        ),
        E(
            "A7-03-3-ex2",
            "sedang",
            """
            Tulis fungsi `bisa_push(commits, lokal, remote)` yang mengembalikan `True` bila `remote` adalah `None` (cabang baru) atau merupakan leluhur dari `lokal` (termasuk sama), dan `False` bila tidak.
            """,
            """
            def bisa_push(commits, lokal, remote):
                # TODO: implementasikan
                pass
            """,
            FIXK + """
            k = _k()
            assert bisa_push(k, 'c5', 'c4') is True
            assert bisa_push(k, 'c3', 'c5') is False
            assert bisa_push(k, 'c3', 'c3') is True
            assert bisa_push(k, 'c3', None) is True
            assert bisa_push(k, 'c3', 'c4') is False
            """,
            "Telusuri induk dari lokal dan cari remote, atau kembalikan True bila remote kosong.",
            BISA_PUSH_FN.strip("\n"),
        ),
        E(
            "A7-03-3-ex3",
            "sedang",
            """
            Tulis fungsi `fetch(lokal, remote)` yang menyalin ke `lokal['commits']` semua commit di `remote['commits']` yang belum ada, mengatur `lokal['cabang']['origin/' + nama]` untuk setiap cabang remote ke ujungnya, dan mengembalikan list terurut id commit yang baru disalin. Cabang lokal lain tidak boleh berubah.
            """,
            """
            def fetch(lokal, remote):
                # TODO: implementasikan
                pass
            """,
            FIXL + """
            lokal = _lokal()
            remote = _remote('c3', ['c1', 'c2', 'c3'])
            assert fetch(lokal, remote) == ['c3']
            assert lokal['cabang']['origin/main'] == 'c3'
            assert lokal['cabang']['main'] == 'c5'
            assert 'c3' in lokal['commits']
            assert fetch(lokal, remote) == []
            """,
            "Salin commit yang belum ada lalu catat ujung tiap cabang remote dengan awalan origin/.",
            FETCH_FN.strip("\n"),
        ),
        E(
            "A7-03-3-ex4",
            "menantang",
            """
            Tulis fungsi `push(lokal, remote, cabang)` yang mengirim cabang `cabang` dari `lokal` ke `remote` (keduanya dict berkunci `commits` dan `cabang`). Push diterima hanya bila cabang belum ada di remote atau ujung remote adalah leluhur (atau sama dengan) ujung lokal. Bila diterima, salin semua commit lokal ke remote, atur ujung cabang remote, dan kembalikan ujungnya. Bila ditolak, lemparkan `ValueError` tanpa mengubah remote.
            """,
            """
            def push(lokal, remote, cabang):
                # TODO: implementasikan
                pass
            """,
            FIXL + """
            lokal = _lokal()
            remote = _remote('c2', ['c1', 'c2'])
            assert push(lokal, remote, 'main') == 'c5'
            assert remote['cabang']['main'] == 'c5'
            assert 'c4' in remote['commits'] and 'c5' in remote['commits']
            r2 = _remote('c3', ['c1', 'c2', 'c3'])
            try:
                push(lokal, r2, 'main')
                ditolak = False
            except ValueError:
                ditolak = True
            assert ditolak is True
            assert r2['cabang']['main'] == 'c3' and 'c4' not in r2['commits']
            lokal['cabang']['fitur'] = 'c4'
            assert push(lokal, r2, 'fitur') == 'c4'
            assert r2['cabang']['fitur'] == 'c4'
            """,
            "Periksa apakah ujung remote ada di jalur induk lokal sebelum menyalin dan memindah penunjuk.",
            PUSH_FN.strip("\n"),
        ),
    ],
    [
        M("Memakai git push --force untuk mengatasi penolakan.", "Fetch, gabungkan, lalu push."),
        M("Mengira origin/main selalu terkini.", "Ia hanya diperbarui saat fetch atau pull."),
        M("Mendorong rahasia ke remote.", "Gunakan .gitignore dan variabel lingkungan."),
    ],
    [
        Q("Remote utama biasanya bernama?", ["origin", "master", "remote1", "server"], 0, "Nama bawaan.", hint="Asal."),
        Q("git fetch?", ["Mengunduh commit tanpa mengubah cabang kita", "Mengirim commit", "Menggabung otomatis", "Menghapus cabang"], 0, "Hanya mengunduh.", hint="Unduh."),
        Q("git pull sama dengan?", ["fetch lalu merge", "push lalu fetch", "commit lalu push", "reset lalu fetch"], 0, "Dua langkah.", hint="Gabung."),
        Q("Push ditolak bila?", ["Remote punya commit yang tidak kita miliki", "Pesan terlalu panjang", "Cabang baru", "File kecil"], 0, "Riwayat menyimpang.", hint="Menyimpang."),
        Q("Pull request digunakan untuk?", ["Meninjau dan menggabungkan perubahan", "Menghapus repo", "Membuat tag", "Mengompres riwayat"], 0, "Tinjauan kode.", hint="Tinjau."),
    ],
    [
        "Remote adalah salinan repositori di server, dilacak lewat cabang origin.",
        "Fetch mengunduh, pull menggabungkan, push mengirim.",
        "Ahead dan behind menunjukkan posisi relatif terhadap remote.",
        "Pull request dan etika kolaborasi menjaga kualitas kerja tim.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perintah yang cukup jelas dalam teks.", "brief": []}

write_module(
    "A7",
    3,
    "Merge, konflik, dan kolaborasi",
    105,
    [
        "Menjelaskan jenis merge dan menemukan merge base",
        "Membaca dan menyelesaikan konflik penggabungan",
        "Memakai remote dengan fetch, pull, dan push secara aman",
    ],
    [l1, l2, l3],
    video,
    REF,
)
