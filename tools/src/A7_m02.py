import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []


def J(prefix, body):
    return prefix.strip("\n") + "\n\n" + textwrap.dedent(body).strip("\n")


FIXR = textwrap.indent("""def _repo():
    return {
        'commits': {
            'c1': {'parent': None, 'pesan': 'awal', 'snapshot': {'a.py': 'v1'}},
            'c2': {'parent': 'c1', 'pesan': 'tambah b', 'snapshot': {'a.py': 'v1', 'b.py': 'x'}},
            'c3': {'parent': 'c2', 'pesan': 'ubah a', 'snapshot': {'a.py': 'v2', 'b.py': 'x'}},
        },
        'cabang': {'main': 'c3'},
        'head': 'main',
    }

""", '            ')

DATA1 = """
commits = {
    'c1': {'parent': None, 'pesan': 'awal', 'snapshot': {'a.py': 'v1'}},
    'c2': {'parent': 'c1', 'pesan': 'tambah b', 'snapshot': {'a.py': 'v1', 'b.py': 'x'}},
    'c3': {'parent': 'c2', 'pesan': 'ubah a', 'snapshot': {'a.py': 'v2', 'b.py': 'x'}},
}
"""

LOG_FN = """
def daftar_id(commits, head):
    hasil = []
    sekarang = head
    while sekarang is not None:
        hasil.append(sekarang)
        sekarang = commits[sekarang]['parent']
    return hasil
"""

DIFF_FN = """
def diff_snapshot(a, b):
    ditambah = sorted(n for n in b if n not in a)
    dihapus = sorted(n for n in a if n not in b)
    diubah = sorted(n for n in a if n in b and a[n] != b[n])
    return (ditambah, dihapus, diubah)
"""

ANC_FN = """
def adalah_leluhur(commits, a, b):
    sekarang = b
    while sekarang is not None:
        if sekarang == a:
            return True
        sekarang = commits[sekarang]['parent']
    return False
"""

PESAN_FN = """
def pesan_terbaru(commits, head, n):
    hasil = []
    sekarang = head
    while sekarang is not None and len(hasil) < n:
        hasil.append(commits[sekarang]['pesan'])
        sekarang = commits[sekarang]['parent']
    return hasil
"""

l1 = lesson(
    "A7-02-1",
    "Commit dan membaca riwayat",
    35,
    [
        "Menjelaskan commit sebagai simpul dengan penunjuk ke induk",
        "Menelusuri riwayat dari commit terbaru ke commit pertama",
        "Menghitung perbedaan antar dua snapshot",
        "Menentukan hubungan leluhur antar commit",
    ],
    [
        T("""
        ## Commit sebagai simpul

        Pada modul sebelumnya kita melihat bahwa commit menyimpan snapshot dan penunjuk ke induknya. Bila digambar, commit membentuk rantai dari yang terbaru mundur ke yang pertama. Membaca riwayat berarti berjalan menyusuri penunjuk induk itu satu per satu sampai mencapai commit yang tidak punya induk.

        Pelajaran ini memodelkan riwayat dengan dict Python: kunci adalah id commit, dan nilainya berisi `parent`, `pesan`, serta `snapshot`. Model sederhana ini cukup untuk meniru perilaku inti Git.
        """),
        T("""
        ## Perintah commit dan log

        Di Git, `git commit -m "pesan"` merekam isi staging area sebagai commit baru yang induknya adalah commit saat ini. `git log` menelusuri riwayat dari commit saat ini mundur, dan `git log --oneline` menampilkan satu baris per commit.

        ```bash
        git commit -m "Tambah fungsi rata-rata"
        git log --oneline
        git log -n 3
        git show HEAD
        ```

        Perintah `git show` menampilkan satu commit lengkap dengan perubahannya, sedangkan opsi `-n` membatasi jumlah commit yang ditampilkan.
        """),
        C(
            J(DATA1, """

            def daftar_id(commits, head):
                hasil = []
                sekarang = head
                while sekarang is not None:
                    hasil.append(sekarang)
                    sekarang = commits[sekarang]['parent']
                return hasil

            ids = daftar_id(commits, 'c3')
            print(ids)
            print([commits[i]['pesan'] for i in ids])
            print(daftar_id(commits, 'c1'))
            """),
            """
            ['c3', 'c2', 'c1']
            ['ubah a', 'tambah b', 'awal']
            ['c1']
            """,
            """
            Penelusuran dimulai dari commit terbaru dan berhenti di commit pertama yang tidak punya induk. Mulai dari commit lama menghasilkan riwayat yang lebih pendek.
            """,
            filename="telusuri_riwayat.py",
        ),
        T("""
        ## Riwayat dibaca mundur

        Perhatikan arah penunjuk: setiap commit tahu induknya, tetapi tidak tahu anaknya. Karena itu riwayat selalu ditelusuri dari ujung ke pangkal, dan itulah sebabnya `git log` menampilkan commit terbaru di paling atas.

        Sifat ini membuat commit lama tidak pernah berubah ketika commit baru dibuat. Menambah commit hanya menambah simpul baru yang menunjuk ke belakang, tanpa menyentuh simpul yang sudah ada.
        """),
        T("""
        ## Diff antar commit

        Bila setiap commit adalah snapshot, maka perubahan antar commit dihitung dengan membandingkan dua snapshot. File yang hanya ada di snapshot baru adalah **ditambah**, yang hanya ada di snapshot lama adalah **dihapus**, dan yang ada di keduanya dengan isi berbeda adalah **diubah**.

        Git tidak menyimpan diff, ia menghitungnya saat diminta lewat `git diff`. Tentukan dua commit, misalnya `git diff c1 c3`, dan Git membandingkan snapshot keduanya.
        """),
        C(
            J(DATA1, """

            def diff_snapshot(a, b):
                ditambah = sorted(n for n in b if n not in a)
                dihapus = sorted(n for n in a if n not in b)
                diubah = sorted(n for n in a if n in b and a[n] != b[n])
                return (ditambah, dihapus, diubah)

            s1 = commits['c1']['snapshot']
            s3 = commits['c3']['snapshot']
            print(diff_snapshot(s1, s3))
            print(diff_snapshot(s3, s1))
            print(diff_snapshot(s3, s3))
            """),
            """
            (['b.py'], [], ['a.py'])
            ([], ['b.py'], ['a.py'])
            ([], [], [])
            """,
            """
            Dari commit pertama ke ketiga ada satu file ditambah dan satu diubah. Membalik arah menukar ditambah menjadi dihapus, dan membandingkan snapshot yang sama tidak menghasilkan perubahan.
            """,
            filename="diff_commit.py",
        ),
        T("""
        ## Leluhur dan keturunan

        Commit A adalah **leluhur** commit B bila kita bisa mencapai A dengan menelusuri induk dari B. Sebuah commit dianggap leluhur dirinya sendiri dalam penelusuran. Hubungan ini penting karena menentukan apa yang termasuk dalam riwayat sebuah cabang.

        Bila A leluhur B, seluruh pekerjaan di A sudah ada di B. Pemeriksaan ini dipakai Git untuk memutuskan apakah sebuah penggabungan cukup berupa maju cepat, topik yang kita bahas di pelajaran ketiga.
        """),
        C(
            J(DATA1, """

            def adalah_leluhur(commits, a, b):
                sekarang = b
                while sekarang is not None:
                    if sekarang == a:
                        return True
                    sekarang = commits[sekarang]['parent']
                return False

            print(adalah_leluhur(commits, 'c1', 'c3'))
            print(adalah_leluhur(commits, 'c3', 'c1'))
            print(adalah_leluhur(commits, 'c2', 'c2'))
            """),
            """
            True
            False
            True
            """,
            """
            Commit pertama adalah leluhur commit ketiga tetapi tidak sebaliknya, dan setiap commit dihitung sebagai leluhur dirinya sendiri.
            """,
            filename="leluhur.py",
        ),
        T("""
        ## Pesan commit dan riwayat yang bermakna

        Riwayat yang rapi tersusun dari commit kecil dan fokus. Satu commit sebaiknya satu gagasan: memperbaiki satu bug, menambah satu fungsi, atau memperbarui satu dokumen. Commit raksasa yang mencampur banyak hal sulit diulas dan sulit dibatalkan sebagian.

        Gunakan kalimat perintah pada baris pertama, misalnya `Perbaiki pembulatan pada laporan`. Bila perlu penjelasan, tambahkan baris kosong lalu paragraf alasan. Kebiasaan ini membuat `git log --oneline` terbaca seperti daftar isi proyek.
        """),
        T("""
        ## Melihat riwayat dengan cerdas

        Git menyediakan banyak cara menyaring riwayat. `git log --author=nama` menampilkan commit satu orang, `git log --since="2 weeks ago"` membatasi waktu, dan `git log --follow file.py` hanya menampilkan commit yang menyentuh file itu. Opsi `--graph` menggambar percabangan dengan karakter di terminal.

        Menguasai penyaringan ini mempercepat penyelidikan: bukannya menggulir ratusan commit, kita langsung menuju yang relevan dengan pertanyaan kita.
        """),
        K(
            "tip",
            """
            Satu commit satu gagasan. Commit kecil dan fokus lebih mudah diulas, dilacak, dan dibatalkan.
            """,
            title="Commit fokus",
        ),
        T("""
        ## Hash commit sebagai alamat

        Setiap commit punya hash unik yang menjadi alamatnya. Dalam praktik kita jarang mengetik 40 karakter penuh: tujuh sampai delapan karakter pertama biasanya cukup unik di repositori kecil. Perintah seperti `git show 3f2a9c1` menerima awalan itu selama tidak ambigu.

        Selain hash, Git mengenal alamat relatif seperti `HEAD~1` untuk induk commit saat ini dan `HEAD~2` untuk leluhur dua langkah ke belakang. Alamat relatif ini cepat dipakai saat menelusuri riwayat.
        """),
        T("""
        ## Riwayat sebagai bahan investigasi

        Riwayat bukan sekadar arsip, tetapi alat penyelidikan. Ketika angka laporan tiba-tiba berubah, kita dapat menelusuri commit demi commit untuk menemukan perubahan yang memicunya. Kemampuan menjawab kapan dan mengapa sesuatu berubah sering kali lebih berharga daripada kode itu sendiri.
        """),
        E(
            "A7-02-1-ex1",
            "mudah",
            """
            Tulis fungsi `pesan_terbaru(commits, head, n)` yang mengembalikan list paling banyak `n` pesan commit dimulai dari `head` menelusuri induk, urut dari terbaru.
            """,
            """
            def pesan_terbaru(commits, head, n):
                # TODO: implementasikan
                pass
            """,
            FIXR + """
            commits = _repo()['commits']
            assert pesan_terbaru(commits, 'c3', 2) == ['ubah a', 'tambah b']
            assert pesan_terbaru(commits, 'c3', 10) == ['ubah a', 'tambah b', 'awal']
            assert pesan_terbaru(commits, 'c3', 0) == []
            assert pesan_terbaru(commits, 'c2', 1) == ['tambah b']
            """,
            "Telusuri induk sambil menambah pesan sampai n atau commit pertama.",
            PESAN_FN.strip("\n"),
        ),
        E(
            "A7-02-1-ex2",
            "sedang",
            """
            Tulis fungsi `diff_snapshot(a, b)` yang menerima dua dict `{nama: isi}` dan mengembalikan tuple `(ditambah, dihapus, diubah)` berisi list terurut nama file: ditambah ada di `b` saja, dihapus ada di `a` saja, diubah ada di keduanya dengan isi berbeda.
            """,
            """
            def diff_snapshot(a, b):
                # TODO: implementasikan
                pass
            """,
            FIXR + """
            commits = _repo()['commits']
            s1 = commits['c1']['snapshot']
            s3 = commits['c3']['snapshot']
            assert diff_snapshot(s1, s3) == (['b.py'], [], ['a.py'])
            assert diff_snapshot(s3, s1) == ([], ['b.py'], ['a.py'])
            assert diff_snapshot(s3, s3) == ([], [], [])
            assert diff_snapshot({}, {'z': '1', 'y': '2'}) == (['y', 'z'], [], [])
            """,
            "Bandingkan kunci dan isi tiap file.",
            DIFF_FN.strip("\n"),
        ),
        E(
            "A7-02-1-ex3",
            "sedang",
            """
            Tulis fungsi `daftar_id(commits, head)` yang mengembalikan list id commit dari `head` menelusuri induk sampai commit pertama, urut dari terbaru.
            """,
            """
            def daftar_id(commits, head):
                # TODO: implementasikan
                pass
            """,
            FIXR + """
            commits = _repo()['commits']
            assert daftar_id(commits, 'c3') == ['c3', 'c2', 'c1']
            assert daftar_id(commits, 'c1') == ['c1']
            assert daftar_id(commits, 'c2') == ['c2', 'c1']
            commits['c4'] = {'parent': 'c1', 'pesan': 'x', 'snapshot': {}}
            assert daftar_id(commits, 'c4') == ['c4', 'c1']
            """,
            "Ulangi sampai induk bernilai None.",
            LOG_FN.strip("\n"),
        ),
        E(
            "A7-02-1-ex4",
            "menantang",
            """
            Tulis fungsi `adalah_leluhur(commits, a, b)` yang mengembalikan `True` bila commit `a` dapat dicapai dari commit `b` dengan menelusuri induk (termasuk bila `a` sama dengan `b`), dan `False` bila tidak.
            """,
            """
            def adalah_leluhur(commits, a, b):
                # TODO: implementasikan
                pass
            """,
            FIXR + """
            commits = _repo()['commits']
            assert adalah_leluhur(commits, 'c1', 'c3') is True
            assert adalah_leluhur(commits, 'c3', 'c1') is False
            assert adalah_leluhur(commits, 'c2', 'c2') is True
            commits['c4'] = {'parent': 'c1', 'pesan': 'x', 'snapshot': {}}
            assert adalah_leluhur(commits, 'c2', 'c4') is False
            assert adalah_leluhur(commits, 'c1', 'c4') is True
            """,
            "Telusuri induk dari b dan periksa kesamaan dengan a.",
            ANC_FN.strip("\n"),
        ),
    ],
    [
        M("Mengira commit menyimpan penunjuk ke anaknya.", "Commit hanya menunjuk induk."),
        M("Menumpuk banyak perubahan dalam satu commit.", "Buat commit kecil dan fokus."),
        M("Menulis pesan commit seperti perbaikan.", "Tulis kalimat perintah yang spesifik."),
    ],
    [
        Q("Riwayat ditelusuri dengan?", ["Mengikuti penunjuk induk", "Mengikuti nama file", "Mengurutkan hash", "Membaca log server"], 0, "Dari terbaru mundur.", hint="Induk."),
        Q("File yang hanya ada di snapshot baru disebut?", ["Ditambah", "Dihapus", "Diubah", "Digabung"], 0, "Muncul baru.", hint="Tambah."),
        Q("Git menyimpan diff atau snapshot?", ["Snapshot, diff dihitung saat diminta", "Hanya diff", "Hanya pesan", "Tidak keduanya"], 0, "Snapshot.", hint="Foto."),
        Q("Commit A leluhur B bila?", ["A dapat dicapai dari B lewat induk", "A lebih baru", "A bernama sama", "A di cabang lain"], 0, "Jalur induk.", hint="Mundur."),
        Q("Perintah menampilkan satu baris per commit?", ["git log --oneline", "git show", "git diff", "git add"], 0, "Ringkas.", hint="Oneline."),
    ],
    [
        "Riwayat ditelusuri mundur lewat penunjuk induk.",
        "Diff dihitung dari perbandingan dua snapshot.",
        "Leluhur ditentukan dengan menelusuri induk.",
        "Commit kecil dan fokus membuat riwayat bermakna.",
    ],
    [],
)

BRANCH_FNS = """
def buat_cabang(repo, nama):
    if nama in repo['cabang']:
        raise ValueError('cabang sudah ada')
    repo['cabang'][nama] = repo['cabang'][repo['head']]


def pindah(repo, nama):
    if nama not in repo['cabang']:
        raise ValueError('cabang tidak ada')
    repo['head'] = nama


def commit_baru(repo, pesan, perubahan):
    cabang = repo['head']
    induk = repo['cabang'][cabang]
    snap = dict(repo['commits'][induk]['snapshot'])
    for nama, isi in perubahan.items():
        if isi is None:
            snap.pop(nama, None)
        else:
            snap[nama] = isi
    baru = 'c%d' % (len(repo['commits']) + 1)
    repo['commits'][baru] = {'parent': induk, 'pesan': pesan, 'snapshot': snap}
    repo['cabang'][cabang] = baru
    return baru


def terjangkau(repo, cabang):
    hasil = []
    sekarang = repo['cabang'][cabang]
    while sekarang is not None:
        hasil.append(sekarang)
        sekarang = repo['commits'][sekarang]['parent']
    return hasil


def commit_unik(repo, a, b):
    lain = set(terjangkau(repo, b))
    return [c for c in terjangkau(repo, a) if c not in lain]
"""

REPO0 = """
repo = {
    'commits': {'c1': {'parent': None, 'pesan': 'awal', 'snapshot': {'a.py': 'v1'}}},
    'cabang': {'main': 'c1'},
    'head': 'main',
}
"""

l2 = lesson(
    "A7-02-2",
    "Branch dan HEAD",
    35,
    [
        "Menjelaskan cabang sebagai penunjuk bernama ke sebuah commit",
        "Membuat cabang dan berpindah antar cabang",
        "Memahami bahwa commit baru menggeser penunjuk cabang aktif",
        "Menghitung commit yang hanya ada di satu cabang",
    ],
    [
        T("""
        ## Cabang bukan salinan

        Banyak pemula membayangkan cabang sebagai salinan seluruh proyek. Di Git, cabang hanyalah **penunjuk bernama ke sebuah commit**, yaitu file kecil berisi satu hash. Membuat cabang tidak menyalin file apa pun, sehingga seketika dan murah.

        Karena itulah alur kerja Git menganjurkan cabang untuk hampir setiap pekerjaan: fitur baru, perbaikan bug, atau eksperimen analisis. Bila hasilnya buruk, cabang dibuang tanpa mengganggu jalur utama.
        """),
        T("""
        ## HEAD: kita sedang di mana

        `HEAD` adalah penunjuk khusus yang menandai cabang aktif, yaitu cabang yang akan bertambah ketika kita membuat commit. Ia menunjuk ke nama cabang, dan nama cabang menunjuk ke commit. Dengan dua tingkat penunjuk ini, commit baru cukup memindahkan penunjuk cabang aktif ke commit baru.

        Bila HEAD menunjuk langsung ke sebuah commit tanpa lewat cabang, keadaan itu disebut **detached HEAD**. Commit yang dibuat dalam keadaan itu mudah hilang, jadi buat cabang sebelum bekerja.
        """),
        T("""
        ## Perintah dasar cabang

        ```bash
        git branch fitur-laporan
        git switch fitur-laporan
        git switch -c eksperimen-baru
        git branch
        git branch -d fitur-laporan
        ```

        `git branch nama` membuat cabang di commit saat ini. `git switch nama` berpindah cabang, dan `git switch -c nama` membuat sekaligus berpindah. `git branch` tanpa argumen mencantumkan semua cabang, dan opsi `-d` menghapus cabang yang sudah digabung.
        """),
        C(
            J(REPO0, """

            def buat_cabang(repo, nama):
                if nama in repo['cabang']:
                    raise ValueError('cabang sudah ada')
                repo['cabang'][nama] = repo['cabang'][repo['head']]

            def pindah(repo, nama):
                if nama not in repo['cabang']:
                    raise ValueError('cabang tidak ada')
                repo['head'] = nama

            buat_cabang(repo, 'fitur')
            print(repo['cabang'])
            pindah(repo, 'fitur')
            print(repo['head'])
            try:
                buat_cabang(repo, 'main')
            except ValueError as e:
                print('gagal', e)
            """),
            """
            {'main': 'c1', 'fitur': 'c1'}
            fitur
            gagal cabang sudah ada
            """,
            """
            Cabang baru menunjuk commit yang sama dengan cabang asalnya, tidak ada yang disalin. Nama cabang yang sudah ada ditolak.
            """,
            filename="buat_cabang.py",
        ),
        T("""
        ## Commit menggeser penunjuk

        Ketika kita membuat commit di cabang aktif, commit baru mengambil commit saat ini sebagai induknya, lalu penunjuk cabang aktif berpindah ke commit baru. Cabang lain tidak ikut bergerak. Jadi setelah beberapa commit di cabang `fitur`, cabang `main` masih menunjuk commit lama.

        Keadaan itulah yang membuat riwayat bercabang: dua cabang memiliki leluhur bersama, lalu masing-masing menambah commit sendiri.
        """),
        C(
            J(REPO0, """

            def buat_cabang(repo, nama):
                repo['cabang'][nama] = repo['cabang'][repo['head']]

            def pindah(repo, nama):
                repo['head'] = nama

            def commit_baru(repo, pesan, perubahan):
                cabang = repo['head']
                induk = repo['cabang'][cabang]
                snap = dict(repo['commits'][induk]['snapshot'])
                for nama, isi in perubahan.items():
                    if isi is None:
                        snap.pop(nama, None)
                    else:
                        snap[nama] = isi
                baru = 'c%d' % (len(repo['commits']) + 1)
                repo['commits'][baru] = {'parent': induk, 'pesan': pesan, 'snapshot': snap}
                repo['cabang'][cabang] = baru
                return baru

            buat_cabang(repo, 'fitur')
            pindah(repo, 'fitur')
            print(commit_baru(repo, 'tambah fitur', {'f.py': 'x'}))
            pindah(repo, 'main')
            print(commit_baru(repo, 'perbaiki', {'a.py': 'v2'}))
            print(repo['cabang'])
            print(repo['commits']['c2']['parent'], repo['commits']['c3']['parent'])
            """),
            """
            c2
            c3
            {'main': 'c3', 'fitur': 'c2'}
            c1 c1
            """,
            """
            Kedua cabang bergerak sendiri-sendiri dan sama-sama berinduk commit pertama, sehingga riwayat bercabang.
            """,
            filename="cabang_menyimpang.py",
        ),
        T("""
        ## Melihat percabangan

        Setelah cabang menyimpang, kita sering ingin tahu commit apa yang hanya ada di satu cabang. Itu dihitung dengan mengambil commit yang terjangkau dari cabang pertama lalu membuang yang juga terjangkau dari cabang kedua. Git menyatakannya dengan `git log main..fitur`.

        Daftar ini adalah isi pekerjaan yang akan masuk ke `main` bila `fitur` digabung, sehingga berguna sebagai ringkasan sebelum penggabungan.
        """),
        C(
            J(REPO0, """

            def terjangkau(repo, cabang):
                hasil = []
                sekarang = repo['cabang'][cabang]
                while sekarang is not None:
                    hasil.append(sekarang)
                    sekarang = repo['commits'][sekarang]['parent']
                return hasil

            def commit_unik(repo, a, b):
                lain = set(terjangkau(repo, b))
                return [c for c in terjangkau(repo, a) if c not in lain]

            repo['commits']['c2'] = {'parent': 'c1', 'pesan': 'fitur', 'snapshot': {}}
            repo['commits']['c3'] = {'parent': 'c1', 'pesan': 'perbaikan', 'snapshot': {}}
            repo['cabang'] = {'main': 'c3', 'fitur': 'c2'}
            print(commit_unik(repo, 'fitur', 'main'))
            print(commit_unik(repo, 'main', 'fitur'))
            print(commit_unik(repo, 'main', 'main'))
            """),
            """
            ['c2']
            ['c3']
            []
            """,
            """
            Tiap cabang punya satu commit yang tidak ada di cabang lain, dan membandingkan cabang dengan dirinya sendiri tidak menghasilkan apa-apa.
            """,
            filename="commit_unik.py",
        ),
        T("""
        ## Pola penamaan dan umur cabang

        Beri nama cabang yang menjelaskan tujuannya, misalnya `perbaiki-null-laporan` atau `eksperimen-model-baru`. Cabang berumur pendek lebih sehat: semakin lama sebuah cabang menyimpang dari jalur utama, semakin sulit menggabungkannya kembali karena perubahan kedua pihak menumpuk.

        Kebiasaan yang baik adalah membuat cabang untuk satu tugas, menyelesaikannya dalam hitungan hari, menggabungkannya, lalu menghapusnya.
        """),
        T("""
        ## Cabang utama

        Hampir setiap repositori punya satu cabang utama, biasanya bernama `main` atau `master`. Cabang ini dijaga agar selalu dalam keadaan layak, misalnya kode yang berjalan dan analisis yang dapat dijalankan ulang. Pekerjaan baru dikerjakan di cabang lain lalu digabung setelah diperiksa.

        Pembagian ini melindungi hasil kerja bersama: kesalahan eksperimen tidak langsung merusak jalur yang dipakai orang lain.
        """),
        K(
            "warn",
            """
            Hindari bekerja dalam keadaan detached HEAD. Buat cabang lebih dulu agar commit baru tidak mudah hilang.
            """,
            title="Detached HEAD",
        ),
        T("""
        ## Menggabungkan pekerjaan

        Cabang baru berguna bila hasilnya dapat disatukan kembali. Pelajaran berikutnya membahas penggabungan: kapan Git dapat menggabungkan otomatis, kapan terjadi konflik, dan bagaimana menyelesaikannya. Semua itu bertumpu pada pemahaman bahwa cabang hanyalah penunjuk dan commit membentuk graf.

        Karena itu penting memahami model ini sekarang. Penggabungan adalah operasi pada graf, bukan penyalinan file.
        """),
        T("""
        ## Eksperimen tanpa takut

        Salah satu manfaat terbesar cabang bagi analis data adalah keberanian bereksperimen. Mencoba model baru, mengganti fitur, atau menulis ulang pembersihan data dapat dilakukan di cabang tersendiri. Bila hasilnya tidak lebih baik, cabang dibuang dan jalur utama tetap bersih.
        """),
        T("""
        ## Cabang jarak jauh

        Pada kerja tim, cabang juga ada di server, misalnya `origin/main`. Cabang lokal dan cabang jarak jauh adalah penunjuk terpisah yang disinkronkan lewat perintah seperti `fetch`, `pull`, dan `push`. Pelajaran ketiga modul berikutnya membahas alurnya secara lengkap.
        """),
        T("""
        ## Cabang untuk satu tujuan

        Disiplin sederhana membuat cabang tetap berguna: satu cabang untuk satu tujuan. Bila di tengah jalan kita menemukan masalah lain, buat cabang baru untuknya alih-alih menumpuknya di cabang yang sama.
        """),
        E(
            "A7-02-2-ex1",
            "mudah",
            """
            Tulis fungsi `buat_cabang(repo, nama)` yang menambahkan cabang `nama` pada `repo['cabang']` yang menunjuk commit yang sedang ditunjuk cabang aktif (`repo['head']`). Bila `nama` sudah ada, lemparkan `ValueError`.
            """,
            """
            def buat_cabang(repo, nama):
                # TODO: implementasikan
                pass
            """,
            FIXR + """
            r = _repo()
            buat_cabang(r, 'fitur')
            assert r['cabang']['fitur'] == 'c3'
            assert r['cabang']['main'] == 'c3' and r['head'] == 'main'
            try:
                buat_cabang(r, 'main')
                ditolak = False
            except ValueError:
                ditolak = True
            assert ditolak is True
            """,
            "Salin id commit dari cabang aktif ke nama baru setelah memeriksa duplikat.",
            """
            def buat_cabang(repo, nama):
                if nama in repo['cabang']:
                    raise ValueError('cabang sudah ada')
                repo['cabang'][nama] = repo['cabang'][repo['head']]
            """,
        ),
        E(
            "A7-02-2-ex2",
            "sedang",
            """
            Tulis fungsi `pindah(repo, nama)` yang mengubah `repo['head']` menjadi `nama`. Bila cabang `nama` tidak ada, lemparkan `ValueError` dan jangan ubah `head`.
            """,
            """
            def pindah(repo, nama):
                # TODO: implementasikan
                pass
            """,
            FIXR + """
            r = _repo()
            r['cabang']['fitur'] = 'c2'
            pindah(r, 'fitur')
            assert r['head'] == 'fitur'
            try:
                pindah(r, 'tidakada')
                ditolak = False
            except ValueError:
                ditolak = True
            assert ditolak is True and r['head'] == 'fitur'
            pindah(r, 'main')
            assert r['head'] == 'main'
            """,
            "Periksa keberadaan cabang sebelum mengubah head.",
            """
            def pindah(repo, nama):
                if nama not in repo['cabang']:
                    raise ValueError('cabang tidak ada')
                repo['head'] = nama
            """,
        ),
        E(
            "A7-02-2-ex3",
            "sedang",
            """
            Tulis fungsi `commit_baru(repo, pesan, perubahan)` yang membuat commit di cabang aktif. Snapshot baru adalah salinan snapshot commit ujung cabang aktif yang diperbarui dengan dict `perubahan` (nilai `None` berarti hapus file). Id baru berbentuk `'c'` diikuti jumlah commit setelah penambahan. Geser cabang aktif ke commit baru dan kembalikan id-nya.
            """,
            """
            def commit_baru(repo, pesan, perubahan):
                # TODO: implementasikan
                pass
            """,
            FIXR + """
            r = _repo()
            assert commit_baru(r, 'baru', {'c.py': 'z'}) == 'c4'
            assert r['cabang']['main'] == 'c4'
            assert r['commits']['c4']['snapshot'] == {'a.py': 'v2', 'b.py': 'x', 'c.py': 'z'}
            assert r['commits']['c4']['parent'] == 'c3'
            assert commit_baru(r, 'hapus', {'b.py': None}) == 'c5'
            assert 'b.py' not in r['commits']['c5']['snapshot']
            r2 = _repo()
            r2['cabang']['fitur'] = 'c3'
            r2['head'] = 'fitur'
            commit_baru(r2, 'x', {'f.py': '1'})
            assert r2['cabang']['main'] == 'c3' and r2['cabang']['fitur'] == 'c4'
            """,
            "Salin snapshot induk, terapkan perubahan, tambahkan commit, geser cabang aktif.",
            """
            def commit_baru(repo, pesan, perubahan):
                cabang = repo['head']
                induk = repo['cabang'][cabang]
                snap = dict(repo['commits'][induk]['snapshot'])
                for nama, isi in perubahan.items():
                    if isi is None:
                        snap.pop(nama, None)
                    else:
                        snap[nama] = isi
                baru = 'c%d' % (len(repo['commits']) + 1)
                repo['commits'][baru] = {'parent': induk, 'pesan': pesan, 'snapshot': snap}
                repo['cabang'][cabang] = baru
                return baru
            """,
        ),
        E(
            "A7-02-2-ex4",
            "menantang",
            """
            Tulis fungsi `commit_unik(repo, a, b)` yang mengembalikan list id commit yang terjangkau dari ujung cabang `a` (menelusuri induk) tetapi tidak terjangkau dari ujung cabang `b`, urut dari terbaru.
            """,
            """
            def commit_unik(repo, a, b):
                # TODO: implementasikan
                pass
            """,
            FIXR + """
            r = _repo()
            r['commits']['c4'] = {'parent': 'c2', 'pesan': 'x', 'snapshot': {}}
            r['cabang']['fitur'] = 'c4'
            assert commit_unik(r, 'fitur', 'main') == ['c4']
            assert commit_unik(r, 'main', 'fitur') == ['c3']
            assert commit_unik(r, 'main', 'main') == []
            r['cabang']['lama'] = 'c1'
            assert commit_unik(r, 'main', 'lama') == ['c3', 'c2']
            """,
            "Kumpulkan commit terjangkau dari b lalu saring commit terjangkau dari a.",
            """
            def commit_unik(repo, a, b):
                def terjangkau(cabang):
                    hasil = []
                    sekarang = repo['cabang'][cabang]
                    while sekarang is not None:
                        hasil.append(sekarang)
                        sekarang = repo['commits'][sekarang]['parent']
                    return hasil
                lain = set(terjangkau(b))
                return [c for c in terjangkau(a) if c not in lain]
            """,
        ),
    ],
    [
        M("Mengira cabang menyalin seluruh proyek.", "Cabang hanya penunjuk ke commit."),
        M("Bekerja lama di detached HEAD.", "Buat cabang sebelum membuat commit."),
        M("Membiarkan cabang fitur berumur sangat panjang.", "Gabungkan sering agar konflik kecil."),
    ],
    [
        Q("Cabang di Git adalah?", ["Penunjuk bernama ke commit", "Salinan proyek", "File data", "Pengguna"], 0, "Ringan.", hint="Penunjuk."),
        Q("HEAD menandai?", ["Cabang aktif", "Commit pertama", "Server", "File terbesar"], 0, "Tempat kita berada.", hint="Aktif."),
        Q("Commit baru menggeser?", ["Penunjuk cabang aktif", "Semua cabang", "Hanya tag", "Tidak ada"], 0, "Cabang aktif saja.", hint="Aktif."),
        Q("git switch -c nama?", ["Membuat dan berpindah ke cabang", "Menghapus cabang", "Menggabung", "Mengirim"], 0, "Buat plus pindah.", hint="-c."),
        Q("Detached HEAD berarti?", ["HEAD menunjuk commit langsung", "Cabang terhapus", "Repo rusak", "Server mati"], 0, "Tanpa cabang.", hint="Langsung."),
    ],
    [
        "Cabang hanyalah penunjuk bernama ke commit.",
        "HEAD menandai cabang aktif yang bergerak saat commit.",
        "Cabang yang menyimpang memiliki leluhur bersama.",
        "Cabang berumur pendek lebih mudah digabungkan.",
    ],
    [],
)

L3_FNS = """
def beri_tag(repo, nama, id_commit):
    tag = repo.setdefault('tag', {})
    if nama in tag:
        raise ValueError('tag sudah ada')
    if id_commit not in repo['commits']:
        raise ValueError('commit tidak ada')
    tag[nama] = id_commit
"""

RESET_FN = """
def reset_keras(repo, id_commit):
    sekarang = repo['cabang'][repo['head']]
    while sekarang is not None:
        if sekarang == id_commit:
            repo['cabang'][repo['head']] = id_commit
            return id_commit
        sekarang = repo['commits'][sekarang]['parent']
    raise ValueError('commit bukan leluhur')
"""

REVERT_FN = """
def balikkan(repo, target):
    cabang = repo['head']
    if repo['cabang'][cabang] != target:
        raise ValueError('target bukan ujung cabang')
    induk = repo['commits'][target]['parent']
    if induk is None:
        raise ValueError('tidak ada induk')
    baru = 'c%d' % (len(repo['commits']) + 1)
    repo['commits'][baru] = {
        'parent': target,
        'pesan': 'Revert: ' + repo['commits'][target]['pesan'],
        'snapshot': dict(repo['commits'][induk]['snapshot']),
    }
    repo['cabang'][cabang] = baru
    return baru
"""

FILE_FN = """
def riwayat_file(commits, head, nama):
    hasil = []
    sekarang = head
    while sekarang is not None:
        induk = commits[sekarang]['parent']
        snap = commits[sekarang]['snapshot']
        snap_induk = commits[induk]['snapshot'] if induk is not None else {}
        if snap.get(nama) != snap_induk.get(nama):
            hasil.append(sekarang)
        sekarang = induk
    return hasil
"""

l3 = lesson(
    "A7-02-3",
    "Membatalkan, menandai, dan menelusuri perubahan",
    35,
    [
        "Membedakan revert yang aman dan reset yang menulis ulang riwayat",
        "Menandai commit penting dengan tag",
        "Menelusuri riwayat satu file",
        "Memahami kapan perintah yang merusak riwayat boleh dipakai",
    ],
    [
        T("""
        ## Tiga cara membatalkan

        Kesalahan pasti terjadi, dan Git menyediakan beberapa cara membatalkan dengan konsekuensi berbeda. Mengubah file kembali ke keadaan commit terakhir hanya memengaruhi working directory. Membuat commit baru yang menghapus efek commit lama adalah **revert**. Memindahkan penunjuk cabang mundur ke commit lama adalah **reset**.

        Perbedaan ketiganya menentukan apakah riwayat dipertahankan atau ditulis ulang, dan itu menentukan apakah aman dilakukan pada pekerjaan yang sudah dibagikan.
        """),
        T("""
        ## Revert: membatalkan dengan menambah

        `git revert <commit>` membuat commit baru yang membalikkan perubahan commit yang ditunjuk. Riwayat lama tetap utuh, ditambah satu commit yang berkata bahwa perubahan itu dibatalkan. Karena riwayat hanya bertambah, revert aman dipakai pada cabang yang sudah dibagikan ke orang lain.

        Pada model kita, `balikkan` menyederhanakan kasus paling umum: membatalkan commit di ujung cabang dengan membuat commit baru yang snapshot-nya sama dengan snapshot induk commit itu.
        """),
        C(
            J(DATA1, """

            repo = {'commits': commits, 'cabang': {'main': 'c3'}, 'head': 'main'}

            def balikkan(repo, target):
                cabang = repo['head']
                if repo['cabang'][cabang] != target:
                    raise ValueError('target bukan ujung cabang')
                induk = repo['commits'][target]['parent']
                baru = 'c%d' % (len(repo['commits']) + 1)
                repo['commits'][baru] = {
                    'parent': target,
                    'pesan': 'Revert: ' + repo['commits'][target]['pesan'],
                    'snapshot': dict(repo['commits'][induk]['snapshot']),
                }
                repo['cabang'][cabang] = baru
                return baru

            print(balikkan(repo, 'c3'))
            print(repo['commits']['c4']['pesan'])
            print(repo['commits']['c4']['snapshot'])
            print(len(repo['commits']))
            """),
            """
            c4
            Revert: ubah a
            {'a.py': 'v1', 'b.py': 'x'}
            4
            """,
            """
            Commit pembatalan menambah satu simpul baru. Isinya kembali ke keadaan sebelum commit ketiga, dan semua commit lama tetap ada.
            """,
            filename="revert.py",
        ),
        T("""
        ## Reset: memundurkan penunjuk

        `git reset --hard <commit>` memindahkan penunjuk cabang ke commit lama dan membuang perubahan di staging dan working directory. Commit yang ditinggalkan tidak langsung terhapus, tetapi tidak lagi terjangkau dari cabang, sehingga hilang dari `git log`.

        Reset menulis ulang riwayat. Karena itu hindari memakainya pada cabang yang sudah dibagikan: rekan Anda masih memegang commit yang Anda buang, dan itu memicu kekacauan saat sinkronisasi.
        """),
        C(
            J(DATA1, """

            repo = {'commits': commits, 'cabang': {'main': 'c3'}, 'head': 'main'}

            def reset_keras(repo, id_commit):
                sekarang = repo['cabang'][repo['head']]
                while sekarang is not None:
                    if sekarang == id_commit:
                        repo['cabang'][repo['head']] = id_commit
                        return id_commit
                    sekarang = repo['commits'][sekarang]['parent']
                raise ValueError('commit bukan leluhur')

            print(reset_keras(repo, 'c1'))
            print(repo['cabang'])
            print(len(repo['commits']))
            try:
                reset_keras(repo, 'c3')
            except ValueError as e:
                print('gagal', e)
            """),
            """
            c1
            {'main': 'c1'}
            3
            gagal commit bukan leluhur
            """,
            """
            Penunjuk cabang mundur ke commit pertama sementara ketiga commit masih tersimpan di basis data. Setelah mundur, commit ketiga bukan lagi leluhur sehingga tidak bisa dijadikan sasaran reset.
            """,
            filename="reset_keras.py",
        ),
        T("""
        ## Reflog: jaring pengaman

        Karena commit yang ditinggalkan tidak langsung dihapus, Git menyimpan catatan pergerakan HEAD di `reflog`. Perintah `git reflog` menampilkan ke mana HEAD pernah menunjuk, sehingga reset yang keliru sering masih dapat dipulihkan dengan berpindah ke hash lama.

        Reflog bersifat lokal dan sementara, biasanya bertahan sekitar sembilan puluh hari. Anggap ia jaring pengaman terakhir, bukan alasan untuk ceroboh.
        """),
        T("""
        ## Tag: menandai versi penting

        **Tag** adalah nama tetap untuk sebuah commit, berbeda dari cabang yang bergerak. Gunakan tag untuk menandai versi yang penting, misalnya `v1.0` untuk laporan yang dikirim ke klien atau skrip yang menghasilkan angka publikasi. Dengan tag, kita dapat kembali ke versi itu kapan pun dengan satu nama.

        ```bash
        git tag v1.0
        git tag -a v1.1 -m "Versi untuk laporan Q3"
        git tag
        git switch --detach v1.0
        ```

        Bagi analis, tag adalah cara sederhana mewujudkan reproduksibilitas: laporan menyebut tag, dan siapa pun dapat memulihkan kode yang persis sama.
        """),
        C(
            J(DATA1, """

            repo = {'commits': commits, 'cabang': {'main': 'c3'}, 'head': 'main'}

            def beri_tag(repo, nama, id_commit):
                tag = repo.setdefault('tag', {})
                if nama in tag:
                    raise ValueError('tag sudah ada')
                if id_commit not in repo['commits']:
                    raise ValueError('commit tidak ada')
                tag[nama] = id_commit

            beri_tag(repo, 'v1.0', 'c2')
            print(repo['tag'])
            for nama, ident in [('v1.0', 'c3'), ('v2.0', 'c9')]:
                try:
                    beri_tag(repo, nama, ident)
                except ValueError as e:
                    print('gagal', e)
            """),
            """
            {'v1.0': 'c2'}
            gagal tag sudah ada
            gagal commit tidak ada
            """,
            """
            Tag menetapkan nama permanen pada commit tertentu, menolak nama yang sudah dipakai dan commit yang tidak ada.
            """,
            filename="beri_tag.py",
        ),
        T("""
        ## Menelusuri riwayat satu file

        Sering kita hanya peduli pada satu file: kapan fungsi ini berubah, dan siapa yang mengubahnya. `git log --follow nama_file` menampilkan commit yang menyentuh file itu, dan `git blame nama_file` menunjukkan commit terakhir yang mengubah tiap barisnya.

        Prinsipnya sederhana: sebuah commit menyentuh file bila isi file di snapshot-nya berbeda dari di snapshot induknya, termasuk ketika file baru ditambahkan atau dihapus.
        """),
        C(
            J(DATA1, """

            def riwayat_file(commits, head, nama):
                hasil = []
                sekarang = head
                while sekarang is not None:
                    induk = commits[sekarang]['parent']
                    snap = commits[sekarang]['snapshot']
                    snap_induk = commits[induk]['snapshot'] if induk is not None else {}
                    if snap.get(nama) != snap_induk.get(nama):
                        hasil.append(sekarang)
                    sekarang = induk
                return hasil

            print(riwayat_file(commits, 'c3', 'a.py'))
            print(riwayat_file(commits, 'c3', 'b.py'))
            print(riwayat_file(commits, 'c3', 'tidak.py'))
            """),
            """
            ['c3', 'c1']
            ['c2']
            []
            """,
            """
            File a.py ditambahkan di commit pertama dan diubah di commit ketiga, sedangkan b.py hanya muncul di commit kedua.
            """,
            filename="riwayat_file.py",
        ),
        T("""
        ## Memilih alat yang tepat

        Untuk membatalkan perubahan yang belum dicommit, kembalikan file dengan `git restore`. Untuk membatalkan commit yang sudah dibagikan, pakai `git revert`. Untuk merapikan commit lokal yang belum dibagikan, `git reset` boleh dipakai dengan hati-hati. Bila ragu, pilih revert karena ia tidak menghancurkan apa pun.

        Aturan emasnya: jangan menulis ulang riwayat yang sudah dilihat orang lain. Riwayat bersama adalah catatan kolektif, dan mengubahnya diam-diam merusak kepercayaan tim.
        """),
        K(
            "warn",
            """
            Jangan memakai reset keras atau menulis ulang riwayat pada cabang yang sudah dibagikan. Pakai revert yang menambah commit pembatalan.
            """,
            title="Riwayat bersama",
        ),
        T("""
        ## Membatalkan perubahan yang belum dicommit

        Tidak semua pembatalan melibatkan riwayat. File yang salah diedit dapat dikembalikan ke versi commit terakhir dengan `git restore nama_file`, dan perubahan yang sudah di-stage dapat dikeluarkan dengan `git restore --staged nama_file`. Kedua perintah itu hanya menyentuh working directory dan staging area.

        Hati-hati: perubahan yang belum pernah dicommit tidak tercatat di reflog. Sekali dibuang, ia tidak dapat dipulihkan.
        """),
        E(
            "A7-02-3-ex1",
            "mudah",
            """
            Tulis fungsi `beri_tag(repo, nama, id_commit)` yang menyimpan `id_commit` pada `repo['tag'][nama]` (buat dict `tag` bila belum ada). Lemparkan `ValueError` bila nama tag sudah ada atau commit tidak ada di `repo['commits']`.
            """,
            """
            def beri_tag(repo, nama, id_commit):
                # TODO: implementasikan
                pass
            """,
            FIXR + """
            r = _repo()
            beri_tag(r, 'v1', 'c2')
            assert r['tag'] == {'v1': 'c2'}
            for nama, ident in [('v1', 'c3'), ('v2', 'c9')]:
                try:
                    beri_tag(r, nama, ident)
                    ditolak = False
                except ValueError:
                    ditolak = True
                assert ditolak is True
            beri_tag(r, 'v2', 'c3')
            assert r['tag'] == {'v1': 'c2', 'v2': 'c3'}
            """,
            "Periksa duplikat nama dan keberadaan commit sebelum menyimpan.",
            L3_FNS.strip("\n"),
        ),
        E(
            "A7-02-3-ex2",
            "sedang",
            """
            Tulis fungsi `reset_keras(repo, id_commit)` yang memindahkan penunjuk cabang aktif ke `id_commit` dan mengembalikan `id_commit`. `id_commit` harus leluhur (atau sama dengan) ujung cabang aktif, jika tidak lemparkan `ValueError`. Commit di `repo['commits']` tidak boleh dihapus.
            """,
            """
            def reset_keras(repo, id_commit):
                # TODO: implementasikan
                pass
            """,
            FIXR + """
            r = _repo()
            assert reset_keras(r, 'c1') == 'c1'
            assert r['cabang']['main'] == 'c1'
            assert len(r['commits']) == 3
            try:
                reset_keras(r, 'c3')
                ditolak = False
            except ValueError:
                ditolak = True
            assert ditolak is True and r['cabang']['main'] == 'c1'
            r2 = _repo()
            r2['commits']['c4'] = {'parent': 'c1', 'pesan': 'x', 'snapshot': {}}
            try:
                reset_keras(r2, 'c4')
                ditolak = False
            except ValueError:
                ditolak = True
            assert ditolak is True
            """,
            "Telusuri induk dari ujung cabang aktif dan geser penunjuk bila ditemukan.",
            RESET_FN.strip("\n"),
        ),
        E(
            "A7-02-3-ex3",
            "sedang",
            """
            Tulis fungsi `balikkan(repo, target)` yang membuat commit baru di cabang aktif dengan pesan `'Revert: '` diikuti pesan target, snapshot salinan snapshot induk target, dan induk berupa `target`. `target` harus ujung cabang aktif, jika tidak lemparkan `ValueError`. Geser cabang aktif ke commit baru dan kembalikan id-nya (`'c'` diikuti jumlah commit setelah penambahan).
            """,
            """
            def balikkan(repo, target):
                # TODO: implementasikan
                pass
            """,
            FIXR + """
            r = _repo()
            assert balikkan(r, 'c3') == 'c4'
            assert r['commits']['c4']['snapshot'] == {'a.py': 'v1', 'b.py': 'x'}
            assert r['commits']['c4']['pesan'] == 'Revert: ubah a'
            assert r['commits']['c4']['parent'] == 'c3'
            assert r['cabang']['main'] == 'c4'
            try:
                balikkan(r, 'c2')
                ditolak = False
            except ValueError:
                ditolak = True
            assert ditolak is True and len(r['commits']) == 4
            """,
            "Salin snapshot induk target ke commit baru yang berinduk target.",
            REVERT_FN.strip("\n"),
        ),
        E(
            "A7-02-3-ex4",
            "menantang",
            """
            Tulis fungsi `riwayat_file(commits, head, nama)` yang mengembalikan list id commit, dari `head` menelusuri induk, yang menyentuh file `nama`: yaitu isi file di snapshot commit berbeda dari di snapshot induknya (file baru atau dihapus juga dihitung; commit pertama dibandingkan dengan snapshot kosong).
            """,
            """
            def riwayat_file(commits, head, nama):
                # TODO: implementasikan
                pass
            """,
            FIXR + """
            commits = _repo()['commits']
            assert riwayat_file(commits, 'c3', 'a.py') == ['c3', 'c1']
            assert riwayat_file(commits, 'c3', 'b.py') == ['c2']
            assert riwayat_file(commits, 'c3', 'tidak.py') == []
            commits['c4'] = {'parent': 'c3', 'pesan': 'hapus b', 'snapshot': {'a.py': 'v2'}}
            assert riwayat_file(commits, 'c4', 'b.py') == ['c4', 'c2']
            """,
            "Bandingkan isi file di snapshot dengan snapshot induk, dengan induk kosong untuk commit pertama.",
            FILE_FN.strip("\n"),
        ),
    ],
    [
        M("Memakai reset keras pada cabang yang sudah dibagikan.", "Pakai revert."),
        M("Mengira commit yang direset langsung hilang selamanya.", "Cek reflog untuk memulihkannya."),
        M("Menandai versi laporan hanya lewat nama file.", "Pakai tag agar versi kode dapat dipulihkan."),
    ],
    [
        Q("Revert bekerja dengan?", ["Menambah commit pembatalan", "Menghapus commit lama", "Menulis ulang riwayat", "Menghapus cabang"], 0, "Riwayat utuh.", hint="Tambah."),
        Q("Reset keras?", ["Memundurkan penunjuk cabang", "Menambah commit", "Membuat tag", "Menggabung"], 0, "Menulis ulang riwayat.", hint="Mundur."),
        Q("Tag berbeda dari cabang karena?", ["Tetap menunjuk satu commit", "Selalu bergerak", "Menyimpan file", "Menghapus riwayat"], 0, "Nama permanen.", hint="Tetap."),
        Q("Jaring pengaman setelah reset keliru?", ["reflog", "tag", "stash", "blame"], 0, "Catatan gerak HEAD.", hint="Reflog."),
        Q("git blame menunjukkan?", ["Commit terakhir tiap baris", "Daftar cabang", "Ukuran repo", "Nama server"], 0, "Siapa mengubah baris.", hint="Baris."),
    ],
    [
        "Revert menambah commit pembatalan dan aman untuk riwayat bersama.",
        "Reset memundurkan penunjuk dan menulis ulang riwayat.",
        "Tag menandai versi penting dengan nama permanen.",
        "Riwayat satu file ditelusuri dengan membandingkan snapshot induk.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perintah yang cukup jelas dalam teks.", "brief": []}

write_module(
    "A7",
    2,
    "Commit, branch, dan riwayat",
    105,
    [
        "Menelusuri dan membandingkan riwayat commit",
        "Membuat dan memakai cabang dengan memahami HEAD",
        "Membatalkan perubahan dengan aman memakai revert, reset, dan tag",
    ],
    [l1, l2, l3],
    video,
    REF,
)
