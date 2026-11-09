import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

l1 = lesson(
    "A1-04-1",
    "Mendefinisikan fungsi dan nilai kembalian",
    35,
    [
        "Mendefinisikan fungsi dengan def, parameter, dan return",
        "Membedakan parameter dari argumen dan return dari print",
        "Menulis docstring dan memahami cakupan variabel lokal dan global",
        "Mengembalikan beberapa nilai dan memecah masalah menjadi fungsi kecil",
    ],
    [
        T("""
        ## Mengapa fungsi

        **Fungsi** adalah blok kode bernama yang bisa dipanggil berulang kali. Tanpa fungsi, kamu menyalin kode yang sama di banyak tempat, dan setiap perbaikan harus dilakukan di semua salinan. Dengan fungsi, logika ditulis sekali, diberi nama yang bermakna, lalu dipakai di mana saja. Dalam analisis data, fungsi membungkus langkah seperti membersihkan teks, menghitung metrik, atau memuat file, sehingga skripmu terbaca seperti rangkaian kalimat.

        Fungsi didefinisikan dengan kata kunci `def`, diikuti nama, parameter dalam kurung, tanda titik dua, lalu badan fungsi yang menjorok. Nilai yang dikirim saat pemanggilan disebut **argumen**, sedangkan nama yang menampungnya di dalam fungsi disebut **parameter**. Fungsi yang tidak mengembalikan apa pun secara eksplisit mengembalikan `None`.

        Nama fungsi sebaiknya berupa kata kerja yang jelas, seperti `hitung_rata_rata` atau `bersihkan_teks`. Nama yang baik menghemat banyak komentar.
        """),
        C(
            """
            def sapa(nama):
                return "Halo, " + nama

            def kuadrat(x):
                return x * x

            def cetak_saja(x):
                print("nilai", x)

            print(sapa("Sari"))
            print(kuadrat(7))
            hasil = cetak_saja(3)
            print(hasil)
            """,
            """
            Halo, Sari
            49
            nilai 3
            None
            """,
            """
            `return` mengirim nilai ke pemanggil, sedangkan `print` hanya menampilkan teks. Fungsi tanpa `return` mengembalikan `None`.
            """,
            filename="def_dasar.py",
        ),
        T("""
        ## return berbeda dari print

        Ini kebingungan paling umum bagi pemula. `print` menulis sesuatu ke layar untuk dibaca manusia, tetapi nilainya hilang setelah itu. `return` menyerahkan nilai kembali ke kode yang memanggil sehingga bisa disimpan, dihitung lagi, atau dikirim ke fungsi lain. Fungsi yang baik umumnya mengembalikan nilai dan membiarkan pemanggil memutuskan apakah akan mencetaknya.

        Begitu `return` dieksekusi, fungsi langsung berhenti. Baris setelahnya tidak dijalankan. Sifat ini sering dimanfaatkan untuk *early return*: periksa kondisi tidak valid di awal dan keluar segera, sehingga sisa kode tidak perlu bersarang dalam banyak `if`.

        Sebuah fungsi boleh punya beberapa `return` di cabang berbeda. Pastikan setiap jalur eksekusi mengembalikan sesuatu yang konsisten, karena jalur yang lupa `return` diam-diam menghasilkan `None` dan sering memicu error di tempat lain.
        """),
        C(
            """
            def kategori(nilai):
                if nilai < 0 or nilai > 100:
                    return "tidak valid"
                if nilai >= 75:
                    return "lulus"
                return "remedial"

            for n in [90, 60, 101]:
                print(n, kategori(n))

            def lupa_return(x):
                hasil = x * 2

            print(lupa_return(4))
            print(kategori(80).upper())
            """,
            """
            90 lulus
            60 remedial
            101 tidak valid
            None
            LULUS
            """,
            """
            Early return menyederhanakan percabangan. Fungsi yang lupa `return` menghasilkan `None`, dan hasil `return` bisa langsung dipakai dalam ekspresi lain.
            """,
            filename="return_dini.py",
        ),
        K(
            "tip",
            """
            Satu fungsi sebaiknya melakukan satu hal. Jika kamu sulit memberi nama yang singkat dan jelas, kemungkinan fungsinya terlalu besar dan perlu dipecah.
            """,
            title="Fungsi kecil lebih mudah diuji",
        ),
        T("""
        ## Docstring dan cakupan variabel

        **Docstring** adalah string tiga tanda kutip di baris pertama badan fungsi yang menjelaskan apa yang dilakukannya. Alat bantu seperti `help(fungsi)` dan editor menampilkannya, dan ia tersimpan di atribut `__doc__`. Tulis satu kalimat ringkas tentang tujuan, parameter, dan nilai kembalian.

        **Cakupan** (*scope*) menentukan di mana sebuah nama dapat dipakai. Variabel yang dibuat di dalam fungsi bersifat lokal dan lenyap saat fungsi selesai. Fungsi dapat membaca variabel global, tetapi menugaskan nama yang sama di dalam fungsi membuat variabel lokal baru, bukan mengubah yang global. Mengubah variabel global memerlukan kata kunci `global`, praktik yang sebaiknya dihindari karena membuat kode sulit dilacak.

        Cara yang lebih bersih: kirim data lewat parameter dan terima hasil lewat `return`. Fungsi seperti ini bersifat *murni*, hasilnya hanya bergantung pada argumen, sehingga mudah diuji dan diprediksi.
        """),
        C(
            """
            total = 100

            def tambah_lokal(x):
                total = x + 1
                return total

            def hitung_pajak(harga, tarif=0.1):
                \"\"\"Mengembalikan pajak dari harga dengan tarif tertentu.\"\"\"
                return harga * tarif

            print(tambah_lokal(5), total)
            print(hitung_pajak(200))
            print(hitung_pajak.__doc__)

            def min_maks_rata(d):
                return min(d), max(d), sum(d) / len(d)

            a, b, c = min_maks_rata([2, 4, 9])
            print(a, b, round(c, 2))
            """,
            """
            6 100
            20.0
            Mengembalikan pajak dari harga dengan tarif tertentu.
            2 9 5.0
            """,
            """
            Penugasan di dalam fungsi membuat variabel lokal sehingga `total` global tidak berubah. Fungsi dapat mengembalikan beberapa nilai sebagai tuple lalu di-unpack.
            """,
            filename="docstring_scope.py",
        ),
        T("""
        ## Memecah masalah menjadi fungsi

        Keahlian terpenting dalam menulis fungsi adalah dekomposisi. Ambil tugas besar, misalnya menghitung ringkasan nilai satu kelas, lalu pecah menjadi langkah kecil: membersihkan data, menghitung rata-rata, menentukan kategori, dan menyusun laporan. Setiap langkah menjadi satu fungsi yang bisa diuji sendiri.

        Manfaatnya terasa saat ada bug. Jika laporan salah, kamu menguji fungsi satu per satu dan menemukan bagian yang keliru dengan cepat. Tanpa dekomposisi, kamu harus menelusuri skrip panjang baris demi baris.

        Dalam proyek data science, pola ini berlanjut menjadi pipeline: fungsi muat data, fungsi bersihkan, fungsi hitung fitur, fungsi latih. Kebiasaan memecah sejak sekarang akan sangat menolongmu nanti. Kerjakan latihan di bawah dengan memikirkan satu tugas per fungsi.
        """),
        T("""
        ## Menguji fungsi dengan assert

        Cara paling sederhana memastikan fungsi benar adalah menuliskan beberapa pemanggilan beserta hasil yang kamu harapkan memakai `assert`. Bila ekspresi bernilai salah, Python menghentikan program dengan `AssertionError`. Pilih kasus yang mewakili: nilai umum, nilai batas seperti nol atau list kosong, dan nilai yang tidak valid.

        Kebiasaan ini disebut pengujian unit dan menjadi fondasi pengembangan perangkat lunak yang andal. Latihan di aplikasi ini bekerja persis dengan cara itu: kode kamu dijalankan lalu serangkaian assert memeriksa hasilnya. Biasakan memikirkan kasus batas sebelum menulis fungsi, karena di sanalah kebanyakan bug bersembunyi.

        Saat sebuah assert gagal, baca pesan galat dengan teliti. Ia menunjukkan baris yang gagal sehingga kamu tahu kasus mana yang belum tertangani.
        """),
        E(
            "A1-04-1-ex1",
            "mudah",
            """
            Tulis fungsi `luas_persegi_panjang(p, l)` yang mengembalikan luasnya.
            """,
            """
            def luas_persegi_panjang(p, l):
                # TODO: implementasikan
                pass
            """,
            """
            assert luas_persegi_panjang(3, 4) == 12
            assert luas_persegi_panjang(0, 5) == 0
            assert luas_persegi_panjang(2.5, 2) == 5.0
            """,
            "Kembalikan hasil kali dengan return.",
            """
            def luas_persegi_panjang(p, l):
                return p * l
            """,
        ),
        E(
            "A1-04-1-ex2",
            "mudah",
            """
            Tulis fungsi `genap(n)` yang mengembalikan `True` bila `n` genap dan `False` bila tidak.
            """,
            """
            def genap(n):
                # TODO: implementasikan
                pass
            """,
            """
            assert genap(4) is True
            assert genap(7) is False
            assert genap(0) is True
            assert genap(-2) is True
            """,
            "Pakai operator sisa bagi.",
            """
            def genap(n):
                return n % 2 == 0
            """,
        ),
        E(
            "A1-04-1-ex3",
            "sedang",
            """
            Tulis fungsi `statistik(daftar)` yang mengembalikan tuple `(minimum, maksimum, rata_rata)` dengan rata-rata dibulatkan 2 desimal. Bila list kosong kembalikan `None`.
            """,
            """
            def statistik(daftar):
                # TODO: implementasikan
                pass
            """,
            """
            assert statistik([2, 4, 9]) == (2, 9, 5.0)
            assert statistik([1, 2]) == (1, 2, 1.5)
            assert statistik([]) is None
            assert statistik([5]) == (5, 5, 5.0)
            assert statistik([1, 2, 2]) == (1, 2, 1.67)
            """,
            "Periksa list kosong lebih dulu lalu hitung dengan min, max, dan sum.",
            """
            def statistik(daftar):
                if not daftar:
                    return None
                return min(daftar), max(daftar), round(sum(daftar) / len(daftar), 2)
            """,
        ),
        E(
            "A1-04-1-ex4",
            "menantang",
            """
            Tulis fungsi `bilangan_prima(n)` yang mengembalikan `True` bila `n` bilangan prima dan `False` bila tidak. Bilangan kurang dari 2 bukan prima. Lalu tulis `prima_sampai(n)` yang mengembalikan list semua prima dari 2 sampai `n` termasuk, memakai `bilangan_prima`.
            """,
            """
            def bilangan_prima(n):
                # TODO: implementasikan
                pass

            def prima_sampai(n):
                # TODO: implementasikan
                pass
            """,
            """
            assert bilangan_prima(2) is True
            assert bilangan_prima(1) is False
            assert bilangan_prima(0) is False
            assert bilangan_prima(15) is False
            assert bilangan_prima(97) is True
            assert prima_sampai(20) == [2, 3, 5, 7, 11, 13, 17, 19]
            assert prima_sampai(1) == []
            assert prima_sampai(2) == [2]
            """,
            "Uji pembagi dari 2 sampai akar n, dan pakai fungsi pertama di fungsi kedua.",
            """
            def bilangan_prima(n):
                if n < 2:
                    return False
                i = 2
                while i * i <= n:
                    if n % i == 0:
                        return False
                    i += 1
                return True

            def prima_sampai(n):
                return [k for k in range(2, n + 1) if bilangan_prima(k)]
            """,
        ),
    ],
    [
        M("Memakai print di tempat yang seharusnya return.", "Gunakan return agar hasil bisa dipakai kode lain."),
        M("Lupa return di salah satu cabang.", "Pastikan setiap jalur mengembalikan nilai konsisten."),
        M("Mengira penugasan di fungsi mengubah variabel global.", "Penugasan membuat variabel lokal baru."),
    ],
    [
        Q("Apa yang dikembalikan fungsi tanpa return?", ["0", "''", "None", "False"], 2, "Tanpa return eksplisit Python mengembalikan None.", hint="Nilai khusus tidak ada."),
        Q("Beda parameter dan argumen?", ["Tidak ada beda", "Parameter di definisi, argumen saat pemanggilan", "Argumen di definisi, parameter saat pemanggilan", "Parameter hanya angka"], 1, "Parameter adalah nama di definisi dan argumen adalah nilai yang dikirim.", hint="Satu menampung, satu dikirim."),
        Q("Apa yang terjadi setelah return dieksekusi?", ["Fungsi lanjut", "Fungsi berhenti", "Error", "Fungsi diulang"], 1, "Eksekusi fungsi langsung berakhir.", hint="Baris sesudahnya tidak jalan."),
        Q("Fungsi mengembalikan return a, b. Apa tipenya?", ["list", "dict", "tuple", "set"], 2, "Koma membentuk tuple.", hint="Tidak ada kurung tetap sama."),
        Q("Variabel yang dibuat di dalam fungsi bersifat?", ["Global", "Lokal", "Permanen", "Konstan"], 1, "Variabel itu lenyap saat fungsi selesai.", hint="Ia hanya hidup di dalam fungsi."),
    ],
    [
        "def mendefinisikan fungsi dan return mengirim nilai ke pemanggil.",
        "return berbeda dari print dan menghentikan fungsi seketika.",
        "Variabel di dalam fungsi bersifat lokal, kirim data lewat parameter.",
        "Pecah tugas besar menjadi fungsi kecil yang bisa diuji sendiri.",
    ],
    [],
)

l2 = lesson(
    "A1-04-2",
    "Argumen: posisi, kata kunci, bawaan, args, dan kwargs",
    35,
    [
        "Memakai argumen posisi, argumen kata kunci, dan nilai bawaan",
        "Menghindari jebakan nilai bawaan yang bisa berubah",
        "Menerima jumlah argumen bebas dengan *args dan **kwargs",
        "Membongkar list dan dictionary menjadi argumen saat pemanggilan",
    ],
    [
        T("""
        ## Argumen posisi dan kata kunci

        Saat memanggil fungsi, argumen bisa dikirim berdasarkan **posisi** atau berdasarkan **nama** (kata kunci). `bagi(10, 2)` memetakan 10 ke parameter pertama dan 2 ke yang kedua. `bagi(b=2, a=10)` memetakan lewat nama sehingga urutan bebas. Argumen kata kunci membuat pemanggilan lebih mudah dibaca, terutama pada fungsi dengan banyak parameter, misalnya `buat_grafik(data, warna="biru", tebal=2)`.

        Aturannya: argumen posisi harus mendahului argumen kata kunci. Mengirim argumen yang kurang atau berlebih menimbulkan `TypeError`. Pustaka data science seperti pandas dan scikit-learn sangat banyak memakai argumen kata kunci, jadi kamu perlu nyaman membacanya.

        Kamu dapat memaksa parameter menjadi hanya-kata-kunci dengan menaruh tanda bintang sebelum parameter itu di definisi, misalnya `def f(a, *, b)`. Teknik ini mencegah kesalahan urutan pada fungsi dengan banyak opsi.
        """),
        C(
            """
            def bagi(a, b):
                return a / b

            print(bagi(10, 2), bagi(b=2, a=10), bagi(10, b=4))

            def f(a, *, b):
                return a - b

            print(f(5, b=2))
            try:
                f(5, 2)
            except TypeError as e:
                print("TypeError")
            try:
                bagi(1)
            except TypeError:
                print("kurang argumen")
            """,
            """
            5.0 5.0 2.5
            3
            TypeError
            kurang argumen
            """,
            """
            Argumen kata kunci boleh diurutkan bebas. Parameter setelah tanda bintang wajib dikirim dengan nama, dan argumen yang kurang menimbulkan `TypeError`.
            """,
            filename="argumen_posisi.py",
        ),
        T("""
        ## Nilai bawaan dan jebakannya

        Parameter dapat diberi **nilai bawaan** sehingga argumen menjadi opsional: `def hitung_pajak(harga, tarif=0.1)`. Parameter dengan nilai bawaan harus berada setelah parameter tanpa nilai bawaan. Ini membuat fungsi fleksibel: kasus umum cukup satu argumen, kasus khusus mengubah opsi.

        Ada jebakan terkenal: **jangan memakai objek yang bisa diubah**, seperti list atau dictionary kosong, sebagai nilai bawaan. Nilai bawaan dibuat sekali saat fungsi didefinisikan, bukan setiap pemanggilan. Akibatnya list yang sama dipakai bersama oleh semua pemanggilan dan terus bertambah isinya. Solusi standarnya: gunakan `None` sebagai bawaan lalu buat list baru di dalam fungsi bila nilainya `None`.

        Jebakan ini sering muncul pada kode yang terlihat benar dan baru bermasalah pada pemanggilan kedua. Mengenalinya sejak awal menghemat banyak waktu debugging.
        """),
        C(
            """
            def salah(x, hasil=[]):
                hasil.append(x)
                return hasil

            print(salah(1))
            print(salah(2))

            def benar(x, hasil=None):
                if hasil is None:
                    hasil = []
                hasil.append(x)
                return hasil

            print(benar(1))
            print(benar(2))
            print(benar(3, [9]))
            """,
            """
            [1]
            [1, 2]
            [1]
            [2]
            [9, 3]
            """,
            """
            List bawaan dibuat sekali sehingga dipakai bersama antar pemanggilan. Pola `None` lalu buat list baru menghindarinya.
            """,
            filename="bawaan_berubah.py",
        ),
        K(
            "warning",
            """
            Jangan pernah menulis `def f(x, daftar=[])` atau `def f(x, d={})`. Pakai `None` sebagai bawaan dan buat objek baru di dalam fungsi.
            """,
            title="Bawaan yang bisa diubah",
        ),
        T("""
        ## *args dan **kwargs

        Kadang jumlah argumen tidak diketahui sebelumnya. Parameter `*args` mengumpulkan semua argumen posisi tambahan ke dalam sebuah tuple, dan `**kwargs` mengumpulkan semua argumen kata kunci tambahan ke dalam sebuah dictionary. Nama `args` dan `kwargs` hanya konvensi, yang penting adalah tanda bintangnya.

        Contoh klasik adalah fungsi `jumlah(*angka)` yang menjumlahkan berapa pun bilangan. Fungsi bawaan `print` dan `max` bekerja dengan cara serupa. Pola `**kwargs` berguna untuk fungsi pembungkus yang meneruskan opsi ke fungsi lain tanpa harus menuliskan setiap opsi.

        Kebalikannya juga ada. Saat memanggil, `*daftar` membongkar list menjadi argumen posisi dan `**kamus` membongkar dictionary menjadi argumen kata kunci. Dua operator ini sering dipakai bersama untuk meneruskan konfigurasi dari satu fungsi ke fungsi lain.
        """),
        C(
            """
            def jumlah(*angka):
                return sum(angka)

            def info(**data):
                return sorted(data.items())

            def campur(a, *sisa, **opsi):
                return a, sisa, opsi

            print(jumlah(1, 2, 3), jumlah())
            print(info(nama="Sari", umur=21))
            print(campur(1, 2, 3, x=4))
            nilai = [4, 5, 6]
            print(jumlah(*nilai))
            konfig = {"a": 7, "x": 1}
            print(campur(**konfig))
            """,
            """
            6 0
            [('nama', 'Sari'), ('umur', 21)]
            (1, (2, 3), {'x': 4})
            15
            (7, (), {'x': 1})
            """,
            """
            `*args` menjadi tuple dan `**kwargs` menjadi dictionary di dalam fungsi. Saat pemanggilan, bintang membongkar list atau dictionary menjadi argumen.
            """,
            filename="args_kwargs.py",
        ),
        T("""
        ## Merancang tanda tangan fungsi yang baik

        Tanda tangan fungsi (nama dan parameternya) adalah antarmuka yang dipakai orang lain, termasuk dirimu di masa depan. Beberapa pedoman: letakkan parameter yang wajib lebih dulu, beri nilai bawaan yang masuk akal untuk opsi, gunakan nama parameter yang menjelaskan diri, dan jangan menerima terlalu banyak parameter. Bila fungsi butuh lebih dari lima atau enam parameter, pertimbangkan mengelompokkannya dalam dictionary atau objek.

        Untuk opsi berupa saklar benar atau salah, argumen kata kunci memperjelas niat: `urutkan(data, menurun=True)` jauh lebih terbaca daripada `urutkan(data, True)`. Pemanggil tidak perlu menghafal arti posisi.

        Latihan berikut meminta kamu memakai semua teknik di atas pada fungsi kecil. Jalankan solusi dengan beberapa pemanggilan berbeda untuk memeriksa perilaku bawaan dan kata kunci.
        """),
        T("""
        ## Membaca dokumentasi fungsi pustaka

        Kemampuan memahami argumen sangat berguna saat membaca dokumentasi pustaka. Tanda tangan seperti `sorted(iterable, /, *, key=None, reverse=False)` memberi tahu bahwa `iterable` dikirim secara posisi, sedangkan `key` dan `reverse` hanya boleh lewat nama. Garis miring dan bintang di dalam tanda tangan itu memakai aturan yang baru kamu pelajari.

        Begitu pula `print(*objects, sep=' ', end='\\n')`: bintang menandakan jumlah objek bebas, dan `sep` serta `end` adalah opsi kata kunci dengan nilai bawaan. Dengan memahami pola ini, kamu dapat membaca tanda tangan fungsi pandas dan scikit-learn tanpa kebingungan, bahkan yang memiliki puluhan opsi.

        Gunakan `help(nama_fungsi)` di kompiler untuk melihat tanda tangan dan docstring sebuah fungsi kapan pun kamu ragu.
        """),
        E(
            "A1-04-2-ex1",
            "mudah",
            """
            Tulis fungsi `pangkat(x, n=2)` yang mengembalikan `x` pangkat `n` dengan `n` bawaan 2.
            """,
            """
            def pangkat(x, n=2):
                # TODO: implementasikan
                pass
            """,
            """
            assert pangkat(3) == 9
            assert pangkat(2, 5) == 32
            assert pangkat(5, n=0) == 1
            assert pangkat(x=4, n=3) == 64
            """,
            "Gunakan operator **.",
            """
            def pangkat(x, n=2):
                return x ** n
            """,
        ),
        E(
            "A1-04-2-ex2",
            "mudah",
            """
            Tulis fungsi `rata_rata(*angka)` yang mengembalikan rata-rata semua argumen. Bila tidak ada argumen kembalikan 0.
            """,
            """
            def rata_rata(*angka):
                # TODO: implementasikan
                pass
            """,
            """
            assert rata_rata(2, 4, 6) == 4
            assert rata_rata(10) == 10
            assert rata_rata() == 0
            assert rata_rata(1, 2) == 1.5
            """,
            "angka adalah tuple. Periksa kosong lebih dulu.",
            """
            def rata_rata(*angka):
                if not angka:
                    return 0
                return sum(angka) / len(angka)
            """,
        ),
        E(
            "A1-04-2-ex3",
            "sedang",
            """
            Tulis fungsi `tambah_item(item, daftar=None)` yang menambahkan `item` ke `daftar` dan mengembalikannya. Bila `daftar` tidak diberikan, buat list baru. Pemanggilan tanpa `daftar` tidak boleh saling memengaruhi.
            """,
            """
            def tambah_item(item, daftar=None):
                # TODO: implementasikan
                pass
            """,
            """
            assert tambah_item(1) == [1]
            assert tambah_item(2) == [2]
            x = [9]
            assert tambah_item(3, x) == [9, 3]
            assert x == [9, 3]
            assert tambah_item("a") == ["a"]
            """,
            "Pakai None sebagai bawaan lalu buat list baru di dalam fungsi.",
            """
            def tambah_item(item, daftar=None):
                if daftar is None:
                    daftar = []
                daftar.append(item)
                return daftar
            """,
        ),
        E(
            "A1-04-2-ex4",
            "menantang",
            """
            Tulis fungsi `format_tag(nama, *isi, **atribut)` yang mengembalikan string tag HTML sederhana. Isi digabung dengan spasi. Atribut ditulis terurut menurut nama sebagai `kunci="nilai"` dipisah spasi. Contoh: `format_tag("a", "klik", "di", "sini", href="x", id="y")` menghasilkan `<a href="x" id="y">klik di sini</a>`. Tanpa atribut tidak ada spasi tambahan: `<p>hai</p>`.
            """,
            """
            def format_tag(nama, *isi, **atribut):
                # TODO: implementasikan
                pass
            """,
            """
            assert format_tag("p", "hai") == "<p>hai</p>"
            assert format_tag("a", "klik", "di", "sini", href="x", id="y") == '<a href="x" id="y">klik di sini</a>'
            assert format_tag("br") == "<br></br>"
            assert format_tag("b", "x", z="1", a="2") == '<b a="2" z="1">x</b>'
            """,
            "Bangun bagian atribut dari sorted(atribut.items()) dan tambahkan spasi awal hanya bila ada.",
            """
            def format_tag(nama, *isi, **atribut):
                attr = "".join(' ' + k + '="' + str(v) + '"' for k, v in sorted(atribut.items()))
                return "<" + nama + attr + ">" + " ".join(isi) + "</" + nama + ">"
            """,
        ),
    ],
    [
        M("Memakai list kosong sebagai nilai bawaan.", "Pakai None lalu buat list di dalam fungsi."),
        M("Menaruh parameter bernilai bawaan sebelum yang wajib.", "Parameter wajib harus di depan."),
        M("Lupa tanda bintang saat membongkar list ke argumen.", "Tulis f(*daftar) agar elemen jadi argumen terpisah."),
    ],
    [
        Q("Apa tipe *args di dalam fungsi?", ["list", "tuple", "dict", "set"], 1, "Argumen posisi tambahan dikumpulkan dalam tuple.", hint="Tidak bisa diubah."),
        Q("Apa tipe **kwargs di dalam fungsi?", ["list", "tuple", "dict", "str"], 2, "Argumen kata kunci dikumpulkan dalam dictionary.", hint="Ada nama dan nilai."),
        Q("Mengapa def f(x, a=[]) berbahaya?", ["Syntax error", "List bawaan dipakai bersama antar pemanggilan", "Lambat", "Tidak berbahaya"], 1, "Nilai bawaan dibuat sekali saat definisi.", hint="Kapan nilai bawaan dibuat?"),
        Q("Apa arti f(*[1,2,3])?", ["Satu argumen list", "Tiga argumen terpisah", "Error", "Pangkat"], 1, "Bintang membongkar list menjadi argumen posisi.", hint="Kebalikan dari *args."),
        Q("Dalam def f(a, *, b), bagaimana b dikirim?", ["Posisi", "Hanya kata kunci", "Bebas", "Tidak bisa"], 1, "Parameter setelah bintang wajib bernama.", hint="Bintang memisahkan jenis argumen."),
    ],
    [
        "Argumen bisa dikirim lewat posisi atau lewat nama.",
        "Nilai bawaan dibuat sekali, jangan memakai objek yang bisa diubah.",
        "*args menjadi tuple dan **kwargs menjadi dictionary.",
        "Bintang saat pemanggilan membongkar list atau dictionary.",
    ],
    [],
)

l3 = lesson(
    "A1-04-3",
    "Fungsi sebagai objek, lambda, dan fungsi tingkat tinggi",
    35,
    [
        "Memperlakukan fungsi sebagai nilai yang dapat disimpan dan dikirim",
        "Menulis ekspresi lambda untuk fungsi pendek sekali pakai",
        "Memakai sorted, map, filter, dan key dengan fungsi",
        "Memahami closure dan rekursi dasar",
    ],
    [
        T("""
        ## Fungsi adalah objek

        Di Python, fungsi adalah objek seperti angka dan string. Kamu dapat menyimpannya dalam variabel, memasukkannya ke list atau dictionary, mengirimnya sebagai argumen, dan mengembalikannya dari fungsi lain. Menulis `f = kuadrat` tidak memanggil fungsi, hanya memberi nama kedua pada objek yang sama. Tanda kurung `f(3)` yang memanggilnya.

        Kemampuan ini membuka pola yang kuat. Misalnya sebuah dictionary yang memetakan nama operasi ke fungsi menggantikan rangkaian `if elif` yang panjang. Atau fungsi `terapkan(f, data)` yang menjalankan operasi apa pun pada setiap elemen data.

        Fungsi yang menerima atau mengembalikan fungsi lain disebut **fungsi tingkat tinggi**. Konsep ini muncul di mana-mana dalam data science: `sorted(key=...)`, `df.apply(fungsi)`, dan banyak callback dalam pustaka pembelajaran mesin.
        """),
        C(
            """
            def kuadrat(x):
                return x * x

            def kubik(x):
                return x ** 3

            f = kuadrat
            print(f(4), kuadrat is f)

            operasi = {"kuadrat": kuadrat, "kubik": kubik}
            for nama, fn in operasi.items():
                print(nama, fn(3))

            def terapkan(fn, data):
                return [fn(x) for x in data]

            print(terapkan(kuadrat, [1, 2, 3]), terapkan(kubik, [1, 2]))
            """,
            """
            16 True
            kuadrat 9
            kubik 27
            [1, 4, 9] [1, 8]
            """,
            """
            Fungsi dapat disimpan dalam dictionary dan dikirim sebagai argumen. `terapkan` adalah fungsi tingkat tinggi sederhana.
            """,
            filename="fungsi_objek.py",
        ),
        T("""
        ## Lambda

        **Lambda** adalah fungsi anonim satu ekspresi, ditulis `lambda parameter: ekspresi`. Ia menghasilkan nilai ekspresi secara otomatis tanpa kata `return`. Lambda cocok untuk fungsi pendek yang dipakai sekali, terutama sebagai argumen `key`. `lambda x: x * 2` setara dengan `def dua_kali(x): return x * 2`.

        Batasannya: lambda hanya boleh satu ekspresi, tidak boleh berisi pernyataan seperti `if` bertingkat atau perulangan. Bila logika mulai rumit, tulis fungsi `def` biasa dengan nama yang jelas. Terlalu banyak lambda yang rumit justru menyulitkan pembaca.

        Penggunaan paling umum adalah mengurutkan data kompleks. `sorted(siswa, key=lambda s: s["nilai"])` mengurutkan list dictionary menurut kuncinya. Kamu juga dapat mengurutkan menurut beberapa kriteria dengan mengembalikan tuple, misalnya `key=lambda s: (-s["nilai"], s["nama"])`.
        """),
        C(
            """
            dua = lambda x: x * 2
            print(dua(5))

            siswa = [
                {"nama": "Budi", "nilai": 80},
                {"nama": "Ani", "nilai": 90},
                {"nama": "Citra", "nilai": 80},
            ]
            print([s["nama"] for s in sorted(siswa, key=lambda s: s["nilai"])])
            print([s["nama"] for s in sorted(siswa, key=lambda s: (-s["nilai"], s["nama"]))])
            print(max(siswa, key=lambda s: s["nilai"])["nama"])
            """,
            """
            10
            ['Budi', 'Citra', 'Ani']
            ['Ani', 'Budi', 'Citra']
            Ani
            """,
            """
            Lambda dipakai sebagai `key` untuk mengurutkan dan mencari maksimum. Tuple dengan nilai negatif mengurutkan menurun lalu menurut nama.
            """,
            filename="lambda_key.py",
        ),
        T("""
        ## map, filter, dan alternatifnya

        `map(fn, data)` menerapkan fungsi ke setiap elemen, dan `filter(fn, data)` mempertahankan elemen yang membuat fungsi bernilai benar. Keduanya mengembalikan iterator malas, jadi bungkus dengan `list(...)` untuk melihat hasil. Fungsi `sum`, `min`, `max`, `any`, dan `all` juga menerima iterator.

        Banyak programmer Python lebih suka comprehension daripada `map` dan `filter` karena lebih terbaca: `[x * 2 for x in data if x > 0]`. Kedua gaya benar. Yang penting kamu mampu membaca keduanya karena akan bertemu dalam kode orang lain.

        Fungsi `any` dan `all` layak dikenal. `any(kondisi)` benar bila ada satu yang benar, dan `all(kondisi)` benar bila semuanya benar. Keduanya menghemat banyak perulangan manual saat memvalidasi data.
        """),
        C(
            """
            data = [3, -1, 4, -5, 9]
            print(list(map(lambda x: x * 10, data)))
            print(list(filter(lambda x: x > 0, data)))
            print([x * 10 for x in data if x > 0])
            print(any(x < 0 for x in data), all(x < 10 for x in data))
            print(sum(x * x for x in data))
            """,
            """
            [30, -10, 40, -50, 90]
            [3, 4, 9]
            [30, 40, 90]
            True True
            132
            """,
            """
            `map` dan `filter` setara dengan comprehension. `any` dan `all` memeriksa kondisi pada semua elemen.
            """,
            filename="map_filter.py",
        ),
        T("""
        ## Closure dan rekursi

        **Closure** terjadi ketika fungsi dalam mengingat variabel dari fungsi luar yang sudah selesai. Contoh: `buat_pengali(n)` mengembalikan fungsi yang mengalikan dengan `n`. Setiap pemanggilan `buat_pengali` menghasilkan fungsi baru yang membawa nilai `n`-nya sendiri. Pola ini berguna untuk membuat fungsi khusus dari templat umum.

        **Rekursi** adalah fungsi yang memanggil dirinya sendiri. Setiap fungsi rekursif butuh *kasus dasar* yang menghentikan pemanggilan dan *langkah rekursif* yang mendekatkan masalah ke kasus dasar. Faktorial adalah contoh klasik: `faktorial(0)` adalah 1 dan `faktorial(n)` adalah `n * faktorial(n - 1)`.

        Python membatasi kedalaman rekursi, secara bawaan sekitar seribu, sehingga rekursi yang terlalu dalam menimbulkan `RecursionError`. Untuk perulangan sederhana, versi iteratif biasanya lebih aman. Rekursi paling cocok untuk struktur bersarang seperti pohon atau dictionary bersarang.
        """),
        C(
            """
            def buat_pengali(n):
                def kali(x):
                    return x * n
                return kali

            tiga = buat_pengali(3)
            sepuluh = buat_pengali(10)
            print(tiga(5), sepuluh(5))

            def faktorial(n):
                if n <= 1:
                    return 1
                return n * faktorial(n - 1)

            print(faktorial(5), faktorial(0))

            def ratakan(x):
                if not isinstance(x, list):
                    return [x]
                hasil = []
                for e in x:
                    hasil += ratakan(e)
                return hasil

            print(ratakan([1, [2, [3, 4]], 5]))
            """,
            """
            15 50
            120 1
            [1, 2, 3, 4, 5]
            """,
            """
            Closure membawa nilai `n` dari fungsi luar. Rekursi dengan kasus dasar meratakan list bersarang.
            """,
            filename="closure_rekursi.py",
        ),
        T("""
        ## Kapan memakai gaya fungsional

        Gaya fungsional, yaitu menyusun program dari fungsi kecil yang dirangkai, membuat kode ringkas dan mudah diuji karena tiap fungsi hanya bergantung pada inputnya. Dalam data science kamu akan sering menulis rangkaian transformasi: bersihkan teks, ubah ke huruf kecil, pecah menjadi kata, lalu hitung. Tiap langkah dapat berupa fungsi terpisah yang dirangkai.

        Meski begitu, jangan memaksakan gaya ini. Perulangan biasa kadang lebih jelas, terutama bila ada banyak langkah yang saling bergantung. Ukuran keberhasilannya sederhana: apakah orang lain, atau dirimu enam bulan lagi, dapat membaca kode itu tanpa kebingungan?

        Satu catatan tentang kinerja: fungsi bawaan seperti `sum`, `min`, dan `sorted` ditulis dalam bahasa C dan jauh lebih cepat daripada perulangan buatan sendiri. Bila ada fungsi bawaan yang melakukan tugasmu, pakai itu lebih dulu.

        Latihan berikut memadukan lambda, closure, dan rekursi. Kerjakan pelan-pelan dan jalankan setiap solusi dengan beberapa input sendiri.
        """),
        E(
            "A1-04-3-ex1",
            "mudah",
            """
            Tulis fungsi `urutkan_panjang(kata)` yang mengembalikan list kata terurut menurut panjang naik. Panjang sama mempertahankan urutan awal.
            """,
            """
            def urutkan_panjang(kata):
                # TODO: implementasikan
                pass
            """,
            """
            assert urutkan_panjang(["pisang", "kiwi", "apel"]) == ["kiwi", "apel", "pisang"]
            assert urutkan_panjang([]) == []
            assert urutkan_panjang(["bb", "a", "cc"]) == ["a", "bb", "cc"]
            """,
            "Pakai sorted dengan key=len.",
            """
            def urutkan_panjang(kata):
                return sorted(kata, key=len)
            """,
        ),
        E(
            "A1-04-3-ex2",
            "mudah",
            """
            Tulis fungsi `buat_penambah(n)` yang mengembalikan fungsi yang menambahkan `n` pada inputnya.
            """,
            """
            def buat_penambah(n):
                # TODO: implementasikan
                pass
            """,
            """
            tambah5 = buat_penambah(5)
            assert tambah5(10) == 15
            assert buat_penambah(0)(7) == 7
            a = buat_penambah(1)
            b = buat_penambah(100)
            assert a(1) == 2 and b(1) == 101
            """,
            "Definisikan fungsi dalam dan kembalikan tanpa memanggilnya.",
            """
            def buat_penambah(n):
                def tambah(x):
                    return x + n
                return tambah
            """,
        ),
        E(
            "A1-04-3-ex3",
            "sedang",
            """
            Tulis fungsi `peringkat(siswa)` yang menerima list dictionary dengan kunci `nama` dan `nilai`, lalu mengembalikan list nama terurut menurut nilai menurun, dan menurut nama naik bila nilai sama.
            """,
            """
            def peringkat(siswa):
                # TODO: implementasikan
                pass
            """,
            """
            s = [{"nama": "Budi", "nilai": 80}, {"nama": "Ani", "nilai": 90}, {"nama": "Citra", "nilai": 80}]
            assert peringkat(s) == ["Ani", "Budi", "Citra"]
            assert peringkat([]) == []
            assert peringkat([{"nama": "X", "nilai": 1}]) == ["X"]
            """,
            "Gunakan key yang mengembalikan tuple dengan nilai negatif.",
            """
            def peringkat(siswa):
                urut = sorted(siswa, key=lambda s: (-s["nilai"], s["nama"]))
                return [s["nama"] for s in urut]
            """,
        ),
        E(
            "A1-04-3-ex4",
            "menantang",
            """
            Tulis fungsi rekursif `kedalaman(x)` yang mengembalikan kedalaman maksimum list bersarang. Bukan list memiliki kedalaman 0, list kosong memiliki kedalaman 1, dan `[1, [2]]` memiliki kedalaman 2.
            """,
            """
            def kedalaman(x):
                # TODO: implementasikan
                pass
            """,
            """
            assert kedalaman(5) == 0
            assert kedalaman([]) == 1
            assert kedalaman([1, 2]) == 1
            assert kedalaman([1, [2]]) == 2
            assert kedalaman([[[1]], 2]) == 3
            """,
            "Kasus dasar bukan list. Untuk list ambil 1 ditambah maksimum kedalaman elemen.",
            """
            def kedalaman(x):
                if not isinstance(x, list):
                    return 0
                if not x:
                    return 1
                return 1 + max(kedalaman(e) for e in x)
            """,
        ),
    ],
    [
        M("Menulis f = kuadrat() padahal maksudnya menyimpan fungsi.", "Tanpa kurung berarti objek fungsi, dengan kurung berarti pemanggilan."),
        M("Menulis lambda yang terlalu rumit.", "Pakai def bila logika lebih dari satu ekspresi sederhana."),
        M("Rekursi tanpa kasus dasar.", "Selalu tentukan kasus dasar yang menghentikan pemanggilan."),
    ],
    [
        Q("Apa itu fungsi tingkat tinggi?", ["Fungsi sangat panjang", "Fungsi yang menerima atau mengembalikan fungsi", "Fungsi tanpa parameter", "Fungsi bawaan"], 1, "Ia memperlakukan fungsi sebagai nilai.", hint="Fungsi sebagai argumen."),
        Q("Berapa ekspresi yang boleh di dalam lambda?", ["Tak terbatas", "Satu", "Dua", "Nol"], 1, "Lambda hanya satu ekspresi tanpa pernyataan.", hint="Tidak ada return eksplisit."),
        Q("Apa yang dikembalikan map di Python 3?", ["List", "Iterator malas", "Tuple", "Set"], 1, "Bungkus dengan list untuk melihat isi.", hint="Tidak langsung dihitung."),
        Q("Apa yang diingat sebuah closure?", ["Variabel dari fungsi luar", "Semua global", "Hasil lama", "Tidak ada"], 0, "Fungsi dalam membawa variabel fungsi luar.", hint="Contoh buat_pengali."),
        Q("Apa yang wajib ada pada fungsi rekursif?", ["Lambda", "Kasus dasar", "Global", "Argumen bawaan"], 1, "Kasus dasar menghentikan pemanggilan.", hint="Tanpa itu terjadi RecursionError."),
    ],
    [
        "Fungsi adalah objek yang bisa disimpan dan dikirim.",
        "Lambda adalah fungsi satu ekspresi, cocok untuk key.",
        "map, filter, any, dan all menerima fungsi dan iterator.",
        "Closure membawa variabel luar dan rekursi butuh kasus dasar.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa kode dan contoh singkat yang cukup jelas dalam teks dan latihan.", "brief": []}

write_module(
    "A1",
    4,
    "Fungsi, argumen, dan lambda",
    105,
    [
        "Mendefinisikan fungsi dengan parameter dan nilai kembalian yang jelas",
        "Memakai argumen posisi, kata kunci, bawaan, args, dan kwargs",
        "Memakai lambda dan fungsi tingkat tinggi untuk mengolah data",
    ],
    [l1, l2, l3],
    video,
    REF,
)
