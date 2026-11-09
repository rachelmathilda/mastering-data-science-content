import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

l1 = lesson(
    "A1-03-1",
    "List dan tuple",
    35,
    [
        "Membuat, mengakses, dan memotong list dengan indeks positif dan negatif",
        "Memakai metode list seperti append, extend, insert, remove, pop, dan sort",
        "Membedakan list yang bisa diubah dari tuple yang tidak bisa diubah",
        "Memakai unpacking untuk memecah urutan menjadi variabel",
    ],
    [
        T("""
        ## List: kumpulan berurutan yang bisa diubah

        **List** adalah struktur data paling sering dipakai di Python. Ia menyimpan nilai berurutan di dalam kurung siku, misalnya `[3, 1, 4]`, dan isinya boleh bertipe campuran. List bersifat *mutable*: kamu bisa menambah, menghapus, dan mengganti elemen setelah list dibuat.

        Elemen diakses dengan indeks yang dimulai dari nol. `daftar[0]` adalah elemen pertama dan `daftar[-1]` adalah elemen terakhir. Indeks negatif menghitung dari belakang, sehingga `daftar[-2]` adalah elemen kedua dari akhir. Mengakses indeks di luar rentang menimbulkan `IndexError`.

        Dalam data science, list sering menjadi wadah awal sebelum data dipindahkan ke NumPy atau pandas. Memahami list dengan baik berarti kamu memahami dasar cara data diiris, disaring, dan diurutkan di pustaka-pustaka tersebut.
        """),
        T("""
        ## Pemotongan (slicing)

        Pemotongan mengambil sebagian list dengan sintaks `daftar[awal:akhir:langkah]`. Indeks awal ikut, indeks akhir tidak ikut, dan langkah menentukan loncatan. Semua bagian boleh dihilangkan: `daftar[:3]` mengambil tiga elemen pertama, `daftar[2:]` mengambil dari indeks dua sampai akhir, dan `daftar[::-1]` membalik urutan.

        Pemotongan selalu menghasilkan list baru, jadi mengubah hasil potongan tidak memengaruhi list asal. Ini berbeda dari penugasan biasa. `b = a` tidak menyalin list, melainkan membuat dua nama yang menunjuk list yang sama. Mengubah lewat `b` ikut mengubah `a`. Untuk salinan dangkal, pakai `a.copy()` atau `a[:]`.

        Aturan setengah terbuka pada pemotongan sama dengan `range`, sehingga `daftar[:k] + daftar[k:]` selalu menghasilkan list asal. Sifat ini memudahkan kamu membagi data menjadi dua bagian tanpa tumpang tindih.
        """),
        C(
            """
            a = [10, 20, 30, 40, 50]
            print(a[0], a[-1], a[1:3], a[:2], a[2:], a[::-1], a[::2])
            b = a
            b[0] = 99
            print(a[0])
            c = a.copy()
            c[0] = 1
            print(a[0], c[0])
            print(a[:2] + a[2:] == a)
            """,
            """
            10 50 [20, 30] [10, 20] [30, 40, 50] [50, 40, 30, 20, 10] [10, 30, 50]
            99
            99 1
            True
            """,
            """
            Penugasan `b = a` membuat alias, sehingga mengubah `b[0]` ikut mengubah `a[0]`. `copy()` membuat salinan terpisah.
            """,
            filename="slicing_list.py",
        ),
        T("""
        ## Metode list yang wajib dikuasai

        Menambah satu elemen di akhir dengan `append`, menambah banyak elemen sekaligus dengan `extend`, menyisipkan di posisi tertentu dengan `insert`, menghapus nilai pertama yang cocok dengan `remove`, dan mengambil serta menghapus elemen dengan `pop` (bawaannya elemen terakhir). Metode `sort` mengurutkan list di tempat, sedangkan fungsi `sorted` mengembalikan list baru.

        Perhatikan bahwa banyak metode yang mengubah list mengembalikan `None`. Menulis `a = a.sort()` menghilangkan list kamu. Ingat juga perbedaan `append` dan `extend`: `append([1, 2])` menambahkan satu elemen berupa list, sedangkan `extend([1, 2])` menambahkan dua elemen.

        Untuk mengurutkan menurut aturan sendiri, beri argumen `key`, misalnya `sorted(kata, key=len)` mengurutkan menurut panjang. Argumen `reverse=True` membalik urutan. Pengurutan di Python stabil, artinya elemen dengan kunci sama mempertahankan urutan awalnya.
        """),
        C(
            """
            x = [3, 1, 2]
            x.append(5)
            x.extend([8, 9])
            x.insert(0, 7)
            print(x)
            x.remove(1)
            terakhir = x.pop()
            print(x, terakhir)
            hasil = x.sort()
            print(hasil, x)
            kata = ["pisang", "kiwi", "apel", "mangga"]
            print(sorted(kata), sorted(kata, key=len), sorted(kata, reverse=True))
            y = [1]
            y.append([2, 3])
            z = [1]
            z.extend([2, 3])
            print(y, z)
            """,
            """
            [7, 3, 1, 2, 5, 8, 9]
            [7, 3, 2, 5, 8] 9
            None [2, 3, 5, 7, 8]
            ['apel', 'kiwi', 'mangga', 'pisang'] ['kiwi', 'apel', 'pisang', 'mangga'] ['pisang', 'mangga', 'kiwi', 'apel']
            [1, [2, 3]] [1, 2, 3]
            """,
            """
            `sort` mengubah list dan mengembalikan `None`. `sorted` dengan `key=len` mengurutkan menurut panjang kata dengan urutan stabil.
            """,
            filename="metode_list.py",
        ),
        K(
            "warning",
            """
            Jangan menulis `a = a.sort()` atau `a = a.append(x)`. Metode itu mengubah list di tempat dan mengembalikan `None`, sehingga list kamu hilang.
            """,
            title="Jebakan nilai None",
        ),
        T("""
        ## Tuple dan unpacking

        **Tuple** mirip list tetapi *immutable*: setelah dibuat, isinya tidak bisa diubah. Ditulis dengan kurung biasa, `(1, 2)`, atau bahkan tanpa kurung, `1, 2`. Tuple satu elemen butuh koma di belakang, yaitu `(5,)`. Karena tidak bisa diubah, tuple cocok untuk data tetap seperti koordinat, pasangan nilai, dan kunci dictionary.

        **Unpacking** memecah urutan ke beberapa variabel dalam satu baris: `x, y = (3, 4)`. Tanda bintang menangkap sisa elemen, seperti `pertama, *tengah, terakhir = [1, 2, 3, 4, 5]`. Fungsi yang mengembalikan banyak nilai sebenarnya mengembalikan satu tuple yang di-unpack oleh pemanggil.

        Pilihan antara list dan tuple soal makna: list untuk kumpulan yang dapat berubah dan berisi elemen sejenis, tuple untuk rekaman tetap dengan elemen yang masing-masing punya peran berbeda.
        """),
        C(
            """
            titik = (3, 4)
            x, y = titik
            print(x, y, titik[0])
            pertama, *tengah, terakhir = [1, 2, 3, 4, 5]
            print(pertama, tengah, terakhir)
            satu = (5,)
            print(type(satu).__name__, type((5)).__name__)
            try:
                titik[0] = 9
            except TypeError as e:
                print("error:", e)
            def min_maks(d):
                return min(d), max(d)
            lo, hi = min_maks([4, 9, 2])
            print(lo, hi)
            """,
            """
            3 4 3
            1 [2, 3, 4] 5
            tuple int
            error: 'tuple' object does not support item assignment
            2 9
            """,
            """
            Unpacking memecah urutan ke variabel dan bintang menangkap sisanya. Mengubah elemen tuple menimbulkan `TypeError`. Fungsi mengembalikan dua nilai sebagai satu tuple.
            """,
            filename="tuple_unpacking.py",
        ),
        T("""
        ## Kapan memilih list dan kapan tuple

        Bayangkan data satu mahasiswa: nama, umur, dan jurusan. Ketiganya punya peran berbeda, jadi tuple cocok. Sekarang bayangkan daftar nilai ujian seratus mahasiswa. Semuanya sejenis dan jumlahnya bisa bertambah, jadi list cocok. Pembeda utamanya bukan sintaks, melainkan makna data yang kamu simpan.

        Tuple juga sedikit lebih hemat memori dan sedikit lebih cepat dibuat. Namun alasan utama memakainya adalah niat: pembaca kodemu langsung tahu bahwa isinya tidak akan berubah. Sifat tidak bisa diubah ini juga membuat tuple aman dipakai sebagai kunci dictionary dan elemen set, hal yang tidak bisa dilakukan list.

        Latihan di bawah menguji slicing, unpacking, dan pengelolaan salinan. Kerjakan berurutan dan jalankan tiap solusi untuk melihat perilaku sebenarnya.
        """),
        E(
            "A1-03-1-ex1",
            "mudah",
            """
            Tulis fungsi `ujung(daftar)` yang mengembalikan tuple `(pertama, terakhir)` dari list tidak kosong.
            """,
            """
            def ujung(daftar):
                # TODO: implementasikan
                pass
            """,
            """
            assert ujung([1, 2, 3]) == (1, 3)
            assert ujung([7]) == (7, 7)
            assert ujung(["a", "b"]) == ("a", "b")
            """,
            "Gunakan indeks 0 dan -1.",
            """
            def ujung(daftar):
                return daftar[0], daftar[-1]
            """,
        ),
        E(
            "A1-03-1-ex2",
            "mudah",
            """
            Tulis fungsi `bagi_dua(daftar)` yang mengembalikan tuple dua list: separuh pertama dan separuh kedua. Bila jumlah elemen ganjil, bagian pertama lebih pendek.
            """,
            """
            def bagi_dua(daftar):
                # TODO: implementasikan
                pass
            """,
            """
            assert bagi_dua([1, 2, 3, 4]) == ([1, 2], [3, 4])
            assert bagi_dua([1, 2, 3]) == ([1], [2, 3])
            assert bagi_dua([]) == ([], [])
            assert bagi_dua([9]) == ([], [9])
            """,
            "Hitung titik tengah dengan pembagian bulat lalu potong dua kali.",
            """
            def bagi_dua(daftar):
                m = len(daftar) // 2
                return daftar[:m], daftar[m:]
            """,
        ),
        E(
            "A1-03-1-ex3",
            "sedang",
            """
            Tulis fungsi `buang_duplikat(daftar)` yang mengembalikan list baru tanpa duplikat dengan urutan kemunculan pertama dipertahankan. Jangan mengubah list asal.
            """,
            """
            def buang_duplikat(daftar):
                # TODO: implementasikan
                pass
            """,
            """
            a = [3, 1, 3, 2, 1]
            assert buang_duplikat(a) == [3, 1, 2]
            assert a == [3, 1, 3, 2, 1]
            assert buang_duplikat([]) == []
            assert buang_duplikat(["x", "x"]) == ["x"]
            """,
            "Telusuri elemen dan tambahkan ke hasil bila belum ada di hasil.",
            """
            def buang_duplikat(daftar):
                hasil = []
                for x in daftar:
                    if x not in hasil:
                        hasil.append(x)
                return hasil
            """,
        ),
        E(
            "A1-03-1-ex4",
            "menantang",
            """
            Tulis fungsi `putar(daftar, k)` yang mengembalikan list baru hasil rotasi ke kanan sebanyak `k` posisi. Nilai `k` boleh lebih besar dari panjang list atau negatif (rotasi ke kiri). List kosong dikembalikan kosong.
            """,
            """
            def putar(daftar, k):
                # TODO: implementasikan
                pass
            """,
            """
            assert putar([1, 2, 3, 4, 5], 2) == [4, 5, 1, 2, 3]
            assert putar([1, 2, 3], 0) == [1, 2, 3]
            assert putar([1, 2, 3], 4) == [3, 1, 2]
            assert putar([1, 2, 3, 4], -1) == [2, 3, 4, 1]
            assert putar([], 3) == []
            """,
            "Pakai k modulo panjang list, lalu gabungkan dua potongan.",
            """
            def putar(daftar, k):
                if not daftar:
                    return []
                k %= len(daftar)
                if k == 0:
                    return list(daftar)
                return daftar[-k:] + daftar[:-k]
            """,
        ),
    ],
    [
        M("Mengira b = a menyalin list.", "Gunakan a.copy() atau a[:] untuk salinan."),
        M("Menulis a = a.sort().", "Panggil a.sort() saja atau pakai sorted(a)."),
        M("Mengakses indeks di luar rentang.", "Periksa len(daftar) atau pakai indeks negatif dengan hati-hati."),
    ],
    [
        Q("Hasil [10, 20, 30, 40][1:3]?", ["[10, 20]", "[20, 30]", "[20, 30, 40]", "[10, 20, 30]"], 1, "Indeks 1 ikut dan indeks 3 tidak ikut.", hint="Akhir tidak ikut."),
        Q("Apa nilai dari a.sort()?", ["List terurut", "None", "True", "Salinan"], 1, "sort mengubah di tempat dan mengembalikan None.", hint="Bandingkan dengan sorted."),
        Q("Setelah b = a lalu b.append(1), apa yang terjadi pada a?", ["Tidak berubah", "Ikut berubah", "Error", "Kosong"], 1, "Keduanya menunjuk list yang sama.", hint="Tidak ada salinan yang dibuat."),
        Q("Tuple satu elemen ditulis?", ["(5)", "(5,)", "[5]", "5()"], 1, "Koma di belakang yang membuatnya tuple.", hint="Kurung saja hanya pengelompokan."),
        Q("Apa fungsi tanda bintang pada a, *b, c = [1,2,3,4]?", ["Mengalikan", "Menangkap elemen sisa", "Menghapus", "Error"], 1, "b menangkap elemen di tengah sebagai list.", hint="Ini pengumpul sisa."),
    ],
    [
        "List bisa diubah, tuple tidak bisa diubah.",
        "Slicing menghasilkan list baru dan memakai aturan setengah terbuka.",
        "Metode sort dan append mengubah di tempat dan mengembalikan None.",
        "Unpacking memecah urutan ke variabel dengan bintang untuk sisa.",
    ],
    [],
)

l2 = lesson(
    "A1-03-2",
    "Dictionary",
    35,
    [
        "Membuat dictionary dan mengakses nilai dengan aman memakai get",
        "Menelusuri kunci, nilai, dan pasangan dengan keys, values, dan items",
        "Memakai pola penghitung dan pengelompokan dengan dictionary",
        "Menggunakan dictionary bersarang untuk data mirip JSON",
    ],
    [
        T("""
        ## Dictionary: pasangan kunci dan nilai

        **Dictionary** menyimpan data sebagai pasangan kunci dan nilai di dalam kurung kurawal: `{"nama": "Sari", "umur": 21}`. Kamu mengambil nilai lewat kuncinya, bukan lewat posisi, sehingga pencarian sangat cepat dibanding menelusuri list. Kunci harus bersifat *hashable*, artinya tidak bisa diubah: string, angka, dan tuple boleh, list tidak boleh.

        Mengakses kunci yang tidak ada dengan `d["x"]` menimbulkan `KeyError`. Gunakan `d.get("x")` untuk mendapat `None` saat kunci tidak ada, atau `d.get("x", nilai_awal)` untuk menentukan nilai bawaan. Untuk memeriksa keberadaan kunci, pakai `"x" in d`.

        Dictionary adalah format yang sama dengan objek JSON, jadi hampir semua data dari API web dan file konfigurasi akan datang dalam bentuk dictionary dan list yang bersarang.
        """),
        C(
            """
            d = {"nama": "Sari", "umur": 21}
            d["kota"] = "Depok"
            d["umur"] = 22
            print(d)
            print(d.get("kota"), d.get("hobi"), d.get("hobi", "belum diisi"))
            print("nama" in d, "alamat" in d, len(d))
            del d["kota"]
            print(d.pop("umur"), d)
            try:
                d["tidak ada"]
            except KeyError as e:
                print("KeyError:", e)
            """,
            """
            {'nama': 'Sari', 'umur': 22, 'kota': 'Depok'}
            Depok None belum diisi
            True False 3
            22 {'nama': 'Sari'}
            KeyError: 'tidak ada'
            """,
            """
            `get` aman untuk kunci yang mungkin tidak ada, sedangkan indeks langsung menimbulkan `KeyError`. `pop` mengembalikan nilai sambil menghapus kunci.
            """,
            filename="dasar_dict.py",
        ),
        T("""
        ## Menelusuri dictionary

        Menelusuri dictionary dengan `for` memberi kamu kunci. Untuk nilai gunakan `.values()`, dan untuk pasangan gunakan `.items()` yang menghasilkan tuple `(kunci, nilai)` sehingga bisa langsung di-unpack: `for k, v in d.items():`. Sejak Python 3.7 urutan penyisipan terjaga, jadi urutan penelusuran dapat diprediksi.

        Menggabungkan dua dictionary bisa dengan operator `|` (Python 3.9 ke atas) atau metode `update`. Bila ada kunci sama, nilai dari dictionary kedua yang menang. Jangan menambah atau menghapus kunci saat menelusuri dictionary yang sama, karena Python akan menimbulkan `RuntimeError`.

        Untuk membuat dictionary dari dua list sejajar, gabungkan dengan `zip`: `dict(zip(kunci, nilai))`. Pola ini sangat umum saat kamu mengubah baris data menjadi rekaman berlabel.
        """),
        C(
            """
            stok = {"apel": 5, "jeruk": 0, "mangga": 12}
            for k, v in stok.items():
                print(k, v)
            print(list(stok), list(stok.values()))
            tambahan = {"jeruk": 8, "kiwi": 3}
            gabung = stok | tambahan
            print(gabung)
            nama = ["a", "b", "c"]
            nilai = [1, 2, 3]
            print(dict(zip(nama, nilai)))
            tersedia = {k: v for k, v in stok.items() if v > 0}
            print(tersedia)
            """,
            """
            apel 5
            jeruk 0
            mangga 12
            ['apel', 'jeruk', 'mangga'] [5, 0, 12]
            {'apel': 5, 'jeruk': 8, 'mangga': 12, 'kiwi': 3}
            {'a': 1, 'b': 2, 'c': 3}
            {'apel': 5, 'mangga': 12}
            """,
            """
            Operator `|` menggabungkan dengan nilai kedua yang menang. `dict(zip(...))` membangun dictionary dari dua list, dan comprehension menyaring pasangan.
            """,
            filename="telusur_dict.py",
        ),
        T("""
        ## Penghitung dan pengelompokan

        Dua pola dictionary paling berguna dalam analisis data adalah menghitung dan mengelompokkan. Untuk menghitung, perbarui nilai dengan `d[k] = d.get(k, 0) + 1`. Untuk mengelompokkan, simpan list di tiap kunci dengan `d.setdefault(k, []).append(x)`.

        Pustaka standar menyediakan `collections.Counter` dan `collections.defaultdict` yang menyingkat kedua pola ini, dan kamu akan bertemu keduanya nanti. Namun menguasai versi manual lebih dulu membuatmu paham apa yang terjadi di baliknya.

        Kedua pola ini adalah versi mini dari operasi `value_counts` dan `groupby` di pandas. Jika kamu paham versi dictionary-nya, kamu akan langsung paham cara kerja operasi itu saat kamu mencapai modul pandas.
        """),
        C(
            """
            kata = "kopi teh kopi susu teh kopi".split()
            hitung = {}
            for k in kata:
                hitung[k] = hitung.get(k, 0) + 1
            print(hitung)

            transaksi = [("Ani", 10), ("Budi", 5), ("Ani", 7), ("Budi", 1), ("Citra", 3)]
            per_orang = {}
            for nama, jumlah in transaksi:
                per_orang.setdefault(nama, []).append(jumlah)
            print(per_orang)
            total = {n: sum(v) for n, v in per_orang.items()}
            print(total)
            terbanyak = max(total, key=total.get)
            print(terbanyak)
            """,
            """
            {'kopi': 3, 'teh': 2, 'susu': 1}
            {'Ani': [10, 7], 'Budi': [5, 1], 'Citra': [3]}
            {'Ani': 17, 'Budi': 6, 'Citra': 3}
            Ani
            """,
            """
            Pola penghitung dan pengelompokan adalah dasar `value_counts` dan `groupby`. Fungsi `max` dengan `key` mengambil kunci bernilai terbesar.
            """,
            filename="hitung_kelompok.py",
        ),
        T("""
        ## Dictionary bersarang dan data mirip JSON

        Nilai dictionary boleh berupa apa saja, termasuk dictionary lain dan list. Struktur bersarang ini persis bentuk JSON. Untuk mengambil nilai dalam, rangkai kunci: `data["pengguna"]["alamat"]["kota"]`. Bila ada tingkat yang mungkin tidak ada, rangkai `get` dengan nilai bawaan dictionary kosong: `data.get("pengguna", {}).get("alamat", {}).get("kota")`.

        Modul `json` mengubah string JSON menjadi dictionary dengan `json.loads` dan sebaliknya dengan `json.dumps`. Perbedaan kecil yang perlu diingat: JSON memakai `true`, `false`, dan `null`, yang di Python menjadi `True`, `False`, dan `None`.

        Dalam proyek data, kamu akan sering meratakan struktur bersarang menjadi tabel. Latihan menelusuri dictionary bersarang sekarang menyiapkan kamu untuk itu.
        """),
        C(
            """
            import json

            teks = '{"pengguna": {"nama": "Sari", "alamat": {"kota": "Depok"}}, "tag": ["a", "b"], "aktif": true, "skor": null}'
            data = json.loads(teks)
            print(data["pengguna"]["alamat"]["kota"], data["tag"][1], data["aktif"], data["skor"])
            print(data.get("pengguna", {}).get("telepon", {}).get("kode"))
            keluar = json.dumps({"a": [1, 2], "b": None, "c": True}, sort_keys=True)
            print(keluar)
            """,
            """
            Depok b True None
            None
            {"a": [1, 2], "b": null, "c": true}
            """,
            """
            JSON `true` dan `null` menjadi `True` dan `None` di Python. Rangkaian `get` dengan dictionary kosong menghindari `KeyError` pada tingkat yang tidak ada.
            """,
            filename="json_bersarang.py",
        ),
        T("""
        ## Mengapa dictionary begitu penting

        Hampir semua data nyata punya label. Sebuah baris transaksi punya tanggal, pelanggan, dan jumlah. Menyimpannya sebagai list angka membuatmu harus mengingat bahwa indeks ke-2 adalah jumlah. Dengan dictionary, kamu menulis `baris["jumlah"]` dan maknanya langsung jelas. Kode menjadi lebih mudah dibaca dan lebih tahan terhadap perubahan urutan kolom.

        Dictionary juga menjadi jembatan ke pandas. Sebuah DataFrame dapat dibuat dari dictionary yang kuncinya nama kolom dan nilainya list isi kolom, dan sebaliknya DataFrame dapat diubah kembali menjadi list of dictionary. Memahami keduanya membuat perpindahan antar bentuk data terasa wajar.

        Ingat pula bahwa dictionary tidak menjamin kunci yang sama muncul dua kali. Menulis kunci yang sudah ada hanya menimpa nilainya, sehingga data lama hilang tanpa peringatan. Periksa dulu dengan `in` bila penimpaan tidak diinginkan.

        Satu kebiasaan baik: bila kunci mungkin tidak ada, putuskan sejak awal apa yang harus terjadi. Gagal dengan error, memakai nilai bawaan, atau melewati rekaman itu. Memilih secara sadar mencegah bug senyap pada data yang kotor.
        """),
        E(
            "A1-03-2-ex1",
            "mudah",
            """
            Tulis fungsi `ambil(d, kunci, bawaan)` yang mengembalikan `d[kunci]` bila ada dan `bawaan` bila tidak ada.
            """,
            """
            def ambil(d, kunci, bawaan):
                # TODO: implementasikan
                pass
            """,
            """
            assert ambil({"a": 1}, "a", 0) == 1
            assert ambil({"a": 1}, "b", 0) == 0
            assert ambil({}, "x", None) is None
            assert ambil({"a": None}, "a", 5) is None
            """,
            "Method get sudah melakukan ini.",
            """
            def ambil(d, kunci, bawaan):
                return d.get(kunci, bawaan)
            """,
        ),
        E(
            "A1-03-2-ex2",
            "mudah",
            """
            Tulis fungsi `balik(d)` yang mengembalikan dictionary baru dengan kunci dan nilai bertukar. Asumsikan nilai unik dan hashable.
            """,
            """
            def balik(d):
                # TODO: implementasikan
                pass
            """,
            """
            assert balik({"a": 1, "b": 2}) == {1: "a", 2: "b"}
            assert balik({}) == {}
            assert balik({"x": "y"}) == {"y": "x"}
            """,
            "Telusuri items dan bangun dictionary baru.",
            """
            def balik(d):
                return {v: k for k, v in d.items()}
            """,
        ),
        E(
            "A1-03-2-ex3",
            "sedang",
            """
            Tulis fungsi `kelompokkan(pasangan)` yang menerima list tuple `(kunci, nilai)` dan mengembalikan dictionary kunci ke list nilai sesuai urutan kemunculan.
            """,
            """
            def kelompokkan(pasangan):
                # TODO: implementasikan
                pass
            """,
            """
            p = [("a", 1), ("b", 2), ("a", 3)]
            assert kelompokkan(p) == {"a": [1, 3], "b": [2]}
            assert kelompokkan([]) == {}
            assert kelompokkan([("x", 0)]) == {"x": [0]}
            assert list(kelompokkan(p)) == ["a", "b"]
            """,
            "Gunakan setdefault dengan list kosong lalu append.",
            """
            def kelompokkan(pasangan):
                hasil = {}
                for k, v in pasangan:
                    hasil.setdefault(k, []).append(v)
                return hasil
            """,
        ),
        E(
            "A1-03-2-ex4",
            "menantang",
            """
            Tulis fungsi `ambil_dalam(data, jalur, bawaan=None)` yang menerima dictionary bersarang dan list kunci `jalur`, lalu mengembalikan nilai di ujung jalur. Bila ada tingkat yang tidak ada atau bukan dictionary kembalikan `bawaan`.
            """,
            """
            def ambil_dalam(data, jalur, bawaan=None):
                # TODO: implementasikan
                pass
            """,
            """
            d = {"a": {"b": {"c": 5}}, "x": 1}
            assert ambil_dalam(d, ["a", "b", "c"]) == 5
            assert ambil_dalam(d, ["a", "z"]) is None
            assert ambil_dalam(d, ["a", "z"], "kosong") == "kosong"
            assert ambil_dalam(d, ["x", "y"], 0) == 0
            assert ambil_dalam(d, []) == d
            """,
            "Turun satu tingkat per kunci dan hentikan bila bukan dictionary atau kunci tidak ada.",
            """
            def ambil_dalam(data, jalur, bawaan=None):
                sekarang = data
                for k in jalur:
                    if not isinstance(sekarang, dict) or k not in sekarang:
                        return bawaan
                    sekarang = sekarang[k]
                return sekarang
            """,
        ),
    ],
    [
        M("Mengakses kunci yang mungkin tidak ada dengan d[k].", "Pakai d.get(k, bawaan) atau periksa k in d."),
        M("Memakai list sebagai kunci dictionary.", "Pakai tuple atau string yang hashable."),
        M("Mengubah dictionary saat menelusurinya.", "Telusuri list(d.items()) atau bangun dictionary baru."),
    ],
    [
        Q("Hasil {'a': 1}.get('b', 0)?", ["None", "0", "KeyError", "1"], 1, "Kunci tidak ada sehingga nilai bawaan dikembalikan.", hint="Argumen kedua adalah bawaan."),
        Q("Tipe apa yang tidak boleh jadi kunci dictionary?", ["str", "int", "tuple", "list"], 3, "List bisa diubah sehingga tidak hashable.", hint="Kunci harus tidak bisa diubah."),
        Q("Apa yang dihasilkan d.items()?", ["Kunci saja", "Pasangan (kunci, nilai)", "Nilai saja", "Jumlah"], 1, "items menghasilkan tuple pasangan.", hint="Cocok dengan unpacking dua variabel."),
        Q("Operator untuk menggabung dua dictionary di Python 3.9 ke atas?", ["+", "|", "&", "-"], 1, "Operator | menggabung dan nilai kedua menang.", hint="Mirip operasi himpunan."),
        Q("JSON null menjadi apa di Python?", ["0", "''", "None", "False"], 2, "null dipetakan ke None.", hint="Nilai khusus tidak ada."),
    ],
    [
        "Dictionary menyimpan pasangan kunci dan nilai dengan pencarian cepat.",
        "get memberi nilai bawaan dan items memberi pasangan untuk ditelusuri.",
        "Pola penghitung dan pengelompokan adalah dasar value_counts dan groupby.",
        "Dictionary bersarang berbentuk sama dengan JSON.",
    ],
    [],
)

l3 = lesson(
    "A1-03-3",
    "Set dan memilih struktur data",
    35,
    [
        "Membuat set dan memakai operasi himpunan seperti gabungan, irisan, dan selisih",
        "Menghapus duplikat dan memeriksa keanggotaan dengan cepat memakai set",
        "Memilih antara list, tuple, dictionary, dan set berdasarkan kebutuhan",
        "Mengukur perbedaan kecepatan pencarian antar struktur data",
    ],
    [
        T("""
        ## Set: kumpulan unik tanpa urutan

        **Set** adalah kumpulan elemen unik tanpa urutan, ditulis dengan kurung kurawal `{1, 2, 3}` atau dibuat dengan `set(...)`. Set kosong harus ditulis `set()` karena `{}` membuat dictionary kosong. Elemen set harus hashable, sama seperti kunci dictionary.

        Karena tidak berurutan, set tidak punya indeks dan tidak bisa diiris. Urutan penelusurannya tidak boleh diandalkan. Sebagai gantinya, set unggul dalam dua hal: menghapus duplikat dan memeriksa keanggotaan dengan sangat cepat.

        Mengubah list menjadi set lalu kembali ke list adalah cara tercepat untuk membuang duplikat, tetapi urutan asli hilang. Bila urutan kemunculan pertama perlu dipertahankan, pakai trik `list(dict.fromkeys(daftar))` yang memanfaatkan urutan penyisipan dictionary.
        """),
        C(
            """
            a = [3, 1, 3, 2, 1, 5]
            print(sorted(set(a)))
            print(list(dict.fromkeys(a)))
            kosong = set()
            print(type(kosong).__name__, type({}).__name__)
            s = {1, 2}
            s.add(3)
            s.add(2)
            s.discard(10)
            print(sorted(s), len(s), 2 in s, 9 in s)
            """,
            """
            [1, 2, 3, 5]
            [3, 1, 2, 5]
            set dict
            [1, 2, 3] 3 True False
            """,
            """
            `set` menghapus duplikat tanpa menjaga urutan, sedangkan `dict.fromkeys` menjaga urutan kemunculan pertama. `discard` tidak menimbulkan error bila elemen tidak ada.
            """,
            filename="dasar_set.py",
        ),
        T("""
        ## Operasi himpunan

        Set mendukung operasi dari matematika himpunan. **Gabungan** (`a | b`) berisi semua elemen dari keduanya. **Irisan** (`a & b`) berisi elemen yang ada di keduanya. **Selisih** (`a - b`) berisi elemen di a yang tidak ada di b. **Selisih simetris** (`a ^ b`) berisi elemen yang hanya ada di salah satu.

        Operasi ini sangat berguna dalam data: mencari pelanggan yang membeli produk A dan B (irisan), pelanggan yang membeli A tetapi tidak B (selisih), atau memeriksa apakah dua kumpulan fitur tumpang tindih. Metode `issubset`, `issuperset`, dan `isdisjoint` memeriksa hubungan antar himpunan.

        Selain itu, sifat irisan dan gabungan dipakai langsung dalam metrik kemiripan seperti indeks Jaccard, yaitu ukuran irisan dibagi ukuran gabungan, yang sering muncul dalam sistem rekomendasi dan analisis teks.
        """),
        C(
            """
            a = {1, 2, 3, 4}
            b = {3, 4, 5}
            print(sorted(a | b), sorted(a & b), sorted(a - b), sorted(a ^ b))
            print({1, 2} <= a, a.isdisjoint({9}), {3} < b)
            def jaccard(x, y):
                if not x and not y:
                    return 1.0
                return len(x & y) / len(x | y)
            print(round(jaccard(a, b), 4))
            """,
            """
            [1, 2, 3, 4, 5] [3, 4] [1, 2] [1, 2, 5]
            True True True
            0.4
            """,
            """
            Empat operasi himpunan menghasilkan gabungan, irisan, selisih, dan selisih simetris. Indeks Jaccard di sini 2 dibagi 5, yaitu 0.4.
            """,
            filename="operasi_set.py",
        ),
        T("""
        ## Seberapa cepat pencarian di tiap struktur?

        Memeriksa `x in daftar` pada list harus menelusuri elemen satu per satu, jadi waktunya tumbuh sebanding dengan panjang list. Memeriksa `x in himpunan` atau `x in dictionary` memakai tabel hash dan rata-rata tidak bergantung pada ukuran. Untuk seribu elemen perbedaannya kecil, tetapi untuk jutaan elemen perbedaannya bisa ribuan kali lipat.

        Karena itu, jika kamu berulang kali memeriksa keanggotaan terhadap koleksi yang besar, ubah dulu koleksi itu menjadi set. Biaya mengubahnya hanya sekali, sedangkan hemat waktunya terasa di tiap pemeriksaan.

        Pada contoh berikut kita mengukur waktu dengan modul `time`. Angka pastinya berbeda di tiap perangkat, jadi yang diperiksa adalah perbandingan relatifnya, bukan nilai mutlaknya.
        """),
        C(
            """
            import time

            n = 20000
            daftar = list(range(n))
            himpunan = set(daftar)
            target = list(range(n - 500, n + 500))

            t0 = time.perf_counter()
            a = sum(1 for x in target if x in daftar)
            t_list = time.perf_counter() - t0

            t0 = time.perf_counter()
            b = sum(1 for x in target if x in himpunan)
            t_set = time.perf_counter() - t0

            print(a, b, a == b)
            print("set lebih cepat dari list:", t_set < t_list)
            """,
            """
            500 500 True
            set lebih cepat dari list: True
            """,
            """
            Hasil pencarian sama, tetapi set jauh lebih cepat. Waktu mutlaknya bergantung perangkat sehingga yang diperiksa hanya perbandingannya.
            """,
            filename="waktu_pencarian.py",
        ),
        T("""
        ## Memilih struktur yang tepat

        Pilih struktur berdasarkan apa yang paling sering kamu lakukan. Butuh urutan dan indeks serta data berubah? **List**. Butuh rekaman tetap atau kunci komposit? **Tuple**. Butuh mencari nilai lewat label? **Dictionary**. Butuh keunikan dan pemeriksaan keanggotaan cepat atau operasi himpunan? **Set**.

        Dalam praktik, struktur ini sering digabung: list of dictionary untuk baris data, dictionary berisi list untuk pengelompokan, set of tuple untuk pasangan unik. Tidak ada struktur yang terbaik secara mutlak, hanya yang paling cocok untuk operasi dominan.

        Pustaka seperti NumPy dan pandas menggantikan sebagian besar struktur ini untuk data numerik berukuran besar karena jauh lebih efisien, tetapi struktur bawaan tetap menjadi bahasa yang kamu pakai di antara langkah-langkah analisis.
        """),
        T("""
        ## Contoh keputusan dalam praktik

        Misalkan kamu punya satu juta ID pengguna aktif dan sepuluh ribu ID baru yang ingin diperiksa apakah sudah terdaftar. Jika ID aktif disimpan dalam list, setiap pemeriksaan menelusuri sampai satu juta elemen. Jika disimpan dalam set, tiap pemeriksaan hampir seketika. Perbedaannya menentukan apakah program selesai dalam sepersekian detik atau berjalan berjam-jam.

        Contoh lain: kamu ingin tahu fitur mana yang dipakai model A tetapi tidak model B. Dengan dua set nama fitur, jawabannya satu ekspresi selisih. Tanpa set, kamu menulis dua perulangan bersarang yang lebih panjang dan lebih lambat.

        Ingat juga bahwa set hanya menyimpan elemen hashable. Mencoba memasukkan list ke dalam set menimbulkan `TypeError`, jadi ubah dulu list itu menjadi tuple bila memang perlu disimpan sebagai satu elemen. Pemahaman kecil ini mencegah error membingungkan saat kamu mengolah data bersarang.

        Aturan praktisnya: bila pertanyaannya soal keanggotaan, keunikan, atau perbandingan dua kumpulan, pikirkan set lebih dulu. Latihan berikut melatih refleks itu.
        """),
        E(
            "A1-03-3-ex1",
            "mudah",
            """
            Tulis fungsi `irisan(a, b)` yang mengembalikan list terurut elemen yang ada di kedua list.
            """,
            """
            def irisan(a, b):
                # TODO: implementasikan
                pass
            """,
            """
            assert irisan([1, 2, 3], [2, 3, 4]) == [2, 3]
            assert irisan([1], [2]) == []
            assert irisan([], [1]) == []
            assert irisan([3, 3, 1], [3]) == [3]
            """,
            "Ubah keduanya menjadi set lalu ambil irisan dan urutkan.",
            """
            def irisan(a, b):
                return sorted(set(a) & set(b))
            """,
        ),
        E(
            "A1-03-3-ex2",
            "mudah",
            """
            Tulis fungsi `ada_duplikat(daftar)` yang mengembalikan `True` bila ada elemen yang muncul lebih dari sekali.
            """,
            """
            def ada_duplikat(daftar):
                # TODO: implementasikan
                pass
            """,
            """
            assert ada_duplikat([1, 2, 1]) is True
            assert ada_duplikat([1, 2, 3]) is False
            assert ada_duplikat([]) is False
            assert ada_duplikat(["a", "a"]) is True
            """,
            "Bandingkan panjang list dengan panjang set-nya.",
            """
            def ada_duplikat(daftar):
                return len(set(daftar)) != len(daftar)
            """,
        ),
        E(
            "A1-03-3-ex3",
            "sedang",
            """
            Tulis fungsi `jaccard(a, b)` yang mengembalikan ukuran irisan dibagi ukuran gabungan dari dua koleksi (diperlakukan sebagai set), dibulatkan 4 desimal. Bila keduanya kosong kembalikan 1.0.
            """,
            """
            def jaccard(a, b):
                # TODO: implementasikan
                pass
            """,
            """
            assert jaccard([1, 2, 3, 4], [3, 4, 5]) == 0.4
            assert jaccard([], []) == 1.0
            assert jaccard([1], [2]) == 0.0
            assert jaccard([1, 1, 2], [2, 2, 1]) == 1.0
            """,
            "Konversi ke set dan tangani kasus kosong lebih dulu.",
            """
            def jaccard(a, b):
                x, y = set(a), set(b)
                if not x and not y:
                    return 1.0
                return round(len(x & y) / len(x | y), 4)
            """,
        ),
        E(
            "A1-03-3-ex4",
            "menantang",
            """
            Tulis fungsi `pelanggan_unik(transaksi)` yang menerima list tuple `(pelanggan, produk)` dan mengembalikan dictionary produk ke set pelanggan yang membelinya. Tulis juga `beli_a_bukan_b(transaksi, a, b)` yang mengembalikan list terurut pelanggan yang membeli produk `a` tetapi tidak `b`.
            """,
            """
            def pelanggan_unik(transaksi):
                # TODO: implementasikan
                pass

            def beli_a_bukan_b(transaksi, a, b):
                # TODO: implementasikan
                pass
            """,
            """
            t = [("ani", "kopi"), ("budi", "kopi"), ("ani", "teh"), ("citra", "teh"), ("ani", "kopi")]
            assert pelanggan_unik(t) == {"kopi": {"ani", "budi"}, "teh": {"ani", "citra"}}
            assert beli_a_bukan_b(t, "kopi", "teh") == ["budi"]
            assert beli_a_bukan_b(t, "teh", "kopi") == ["citra"]
            assert beli_a_bukan_b(t, "susu", "kopi") == []
            assert pelanggan_unik([]) == {}
            """,
            "Bangun dictionary produk ke set, lalu pakai operasi selisih. Gunakan get dengan set() untuk produk yang tidak ada.",
            """
            def pelanggan_unik(transaksi):
                hasil = {}
                for pelanggan, produk in transaksi:
                    hasil.setdefault(produk, set()).add(pelanggan)
                return hasil

            def beli_a_bukan_b(transaksi, a, b):
                p = pelanggan_unik(transaksi)
                return sorted(p.get(a, set()) - p.get(b, set()))
            """,
        ),
    ],
    [
        M("Menulis {} untuk set kosong.", "Pakai set() karena {} membuat dictionary."),
        M("Mengandalkan urutan elemen set.", "Urutkan dengan sorted bila urutan penting."),
        M("Mencari anggota di list besar berulang kali.", "Ubah dulu menjadi set untuk pemeriksaan cepat."),
    ],
    [
        Q("Apa tipe dari {}?", ["set", "dict", "list", "tuple"], 1, "Kurung kurawal kosong membuat dictionary.", hint="Set kosong butuh fungsi."),
        Q("Hasil {1,2,3} & {2,3,4}?", ["{1,2,3,4}", "{2,3}", "{1}", "{4}"], 1, "Irisan berisi elemen yang ada di keduanya.", hint="Operator & adalah irisan."),
        Q("Mengapa x in set lebih cepat dari x in list?", ["Set lebih kecil", "Set memakai tabel hash", "List tidak bisa dicari", "Tidak lebih cepat"], 1, "Tabel hash memberi pencarian rata-rata konstan.", hint="Pikirkan cara menemukan tanpa menelusuri semua."),
        Q("Cara membuang duplikat sambil menjaga urutan?", ["set(a)", "sorted(set(a))", "list(dict.fromkeys(a))", "a.sort()"], 2, "Dictionary menjaga urutan penyisipan sehingga kemunculan pertama dipertahankan.", hint="Set tidak menjaga urutan."),
        Q("Struktur paling cocok untuk mencari nilai lewat label?", ["List", "Tuple", "Dictionary", "String"], 2, "Dictionary memetakan kunci ke nilai.", hint="Pasangan kunci dan nilai."),
    ],
    [
        "Set menyimpan elemen unik tanpa urutan dengan pemeriksaan keanggotaan cepat.",
        "Operasi gabungan, irisan, selisih, dan selisih simetris berlaku pada set.",
        "Pencarian di set dan dictionary jauh lebih cepat dari list untuk data besar.",
        "Pilih struktur berdasarkan operasi yang paling dominan.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa kode dan contoh singkat yang cukup jelas dalam teks dan latihan.", "brief": []}

write_module(
    "A1",
    3,
    "List, tuple, dictionary, dan set",
    105,
    [
        "Mengolah list dan tuple dengan indeks, slicing, dan unpacking",
        "Memakai dictionary untuk pemetaan, penghitungan, dan data bersarang",
        "Memakai set untuk keunikan dan memilih struktur data yang tepat",
    ],
    [l1, l2, l3],
    video,
    REF,
)
