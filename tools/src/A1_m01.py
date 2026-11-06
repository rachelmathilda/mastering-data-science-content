import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

l1 = lesson(
    "A1-01-1",
    "Variabel dan tipe data dasar",
    35,
    [
        "Menjelaskan variabel sebagai nama yang menunjuk ke sebuah nilai",
        "Mengenali tipe int, float, str, bool, dan None serta memeriksanya dengan type()",
        "Menerapkan aturan penamaan variabel dan konvensi snake_case",
        "Mengubah tipe nilai dengan int(), float(), str(), dan bool()",
    ],
    [
        T("""
        ## Variabel sebagai nama untuk sebuah nilai

        Setiap program mengolah data, dan data itu perlu diberi nama agar bisa dipakai lagi. Di Python, **variabel** adalah nama yang menunjuk ke sebuah nilai di memori. Kamu membuatnya dengan tanda sama dengan: `umur = 21` berarti nama `umur` sekarang menunjuk ke angka 21. Tanda sama dengan di sini bukan pernyataan kesetaraan seperti di matematika, melainkan perintah penugasan: simpan nilai di kanan ke nama di kiri.

        Python tidak meminta kamu mendeklarasikan tipe lebih dulu. Tipe melekat pada nilai, bukan pada nama. Nama yang sama boleh menunjuk ke angka sekarang dan ke teks beberapa baris kemudian. Kelonggaran ini membuat kode singkat, tetapi juga berarti kamu perlu disiplin: nama yang jelas dan tipe yang konsisten menghindarkan kejutan di tengah program.

        Dalam data science, hampir semua pekerjaan dimulai dengan menamai data: `harga`, `jumlah_baris`, `rata_rata`, `nama_kolom`. Kebiasaan menamai dengan baik sejak awal akan menyelamatkanmu ketika notebook sudah berisi ratusan baris.
        """),
        T("""
        ## Lima tipe yang paling sering muncul

        Ada lima tipe dasar yang wajib kamu kenal. **int** adalah bilangan bulat seperti `7` atau `-3`, dan Python mengizinkan ukurannya sebesar apa pun selama memori cukup. **float** adalah bilangan pecahan seperti `3.14` atau `2.0`, yang disimpan sebagai pendekatan biner sehingga kadang tidak persis. **str** adalah teks yang diapit tanda kutip tunggal atau ganda, misalnya `"Jakarta"`. **bool** hanya punya dua nilai, `True` dan `False`, dan muncul dari hasil perbandingan. Terakhir **None**, nilai khusus yang berarti tidak ada nilai.

        Fungsi `type()` memberi tahu tipe sebuah nilai, dan ini alat pertama saat kamu bingung mengapa kode berperilaku aneh. Banyak galat pemula sebenarnya galat tipe: menjumlahkan teks dengan angka, atau mengira `"5"` sama dengan `5`.

        Perhatikan bahwa `True` dan `False` ditulis dengan huruf kapital di awal. Menulis `true` akan memunculkan `NameError` karena Python menganggapnya nama biasa yang belum didefinisikan.
        """),
        A(
            "Analogi label pada kotak",
            """
            Bayangkan nilai sebagai kotak berisi barang, dan variabel sebagai label yang ditempel pada kotak. Satu kotak boleh punya dua label, dan label boleh dipindah ke kotak lain. Barang di dalam kotak punya jenis sendiri, sedangkan label hanyalah nama untuk menemukannya.
            """,
        ),
        C(
            """
            umur = 21
            tinggi = 170.5
            kota = "Depok"
            aktif = True
            catatan = None

            for nilai in [umur, tinggi, kota, aktif, catatan]:
                print(nilai, type(nilai).__name__)
            """,
            """
            21 int
            170.5 float
            Depok str
            True bool
            None NoneType
            """,
            """
            Lima nilai dengan lima tipe berbeda. Atribut `__name__` pada hasil `type()` memberi nama tipe yang lebih rapi dibaca.
            """,
            filename="lima_tipe.py",
        ),
        T("""
        ## Aturan dan konvensi penamaan

        Nama variabel boleh berisi huruf, angka, dan garis bawah, tetapi tidak boleh diawali angka dan tidak boleh berupa kata kunci Python seperti `if`, `for`, atau `class`. Python membedakan huruf besar dan kecil, jadi `Total` dan `total` adalah dua nama yang berbeda.

        Di luar aturan wajib, komunitas Python memakai konvensi **snake_case**: huruf kecil semua dengan garis bawah sebagai pemisah kata, seperti `rata_rata_harga`. Nama konstanta ditulis huruf besar semua, misalnya `BATAS_MAKSIMAL`. Nama yang menjelaskan isi lebih baik daripada singkatan samar. `n_pelanggan` jauh lebih jelas daripada `x1`.

        Hindari menimpa nama bawaan seperti `list`, `str`, `sum`, atau `max`. Jika kamu menulis `sum = 10`, fungsi `sum()` bawaan tidak bisa lagi dipanggil di sesi yang sama, dan error yang muncul berikutnya membingungkan.
        """),
        K(
            "warning",
            """
            Menimpa nama bawaan adalah sumber bug yang sulit dilacak di notebook, karena sel lama masih menyimpan nama yang sudah tertimpa. Jika terlanjur, restart kernel atau jalankan `del sum` untuk mengembalikan nama bawaan.
            """,
            title="Jangan timpa nama bawaan",
        ),
        C(
            """
            x = 10
            y = x
            x = 25
            print(x, y)

            a = b = 0
            a = a + 5
            print(a, b)

            p, q = 3, 4
            p, q = q, p
            print(p, q)
            """,
            """
            25 10
            5 0
            4 3
            """,
            """
            Penugasan `y = x` menyalin acuan ke nilai, bukan hubungan permanen, jadi mengubah `x` kemudian tidak memengaruhi `y`. Python juga mendukung penugasan ganda dan pertukaran dua nilai tanpa variabel bantu.
            """,
            filename="penugasan.py",
        ),
        T("""
        ## Konversi tipe

        Data dari file atau input pengguna hampir selalu datang sebagai teks. Untuk menghitung, kamu perlu mengubahnya. `int("42")` menghasilkan 42, `float("3.5")` menghasilkan 3.5, dan `str(99)` menghasilkan `"99"`. Konversi yang mustahil, seperti `int("halo")`, menimbulkan `ValueError`.

        Fungsi `int()` pada float memotong bagian pecahan menuju nol, bukan membulatkan. Jadi `int(3.9)` adalah 3 dan `int(-3.9)` adalah -3. Untuk pembulatan gunakan `round()`.

        Fungsi `bool()` mengubah nilai apa pun menjadi benar atau salah. Angka nol, string kosong, dan `None` dianggap `False`. Hampir semua nilai lain dianggap `True`. Sifat ini disebut *truthiness* dan akan sering kamu pakai pada kondisi `if`.
        """),
        C(
            """
            print(int("42") + 1)
            print(float("3.5") * 2)
            print(str(99) + "!")
            print(int(3.9), int(-3.9), round(3.9))
            print(bool(0), bool(""), bool(None), bool("0"), bool(-1))
            """,
            """
            43
            7.0
            99!
            3 -3 4
            False False False True True
            """,
            """
            `int()` memotong menuju nol sedangkan `round()` membulatkan. String `"0"` bernilai `True` karena tidak kosong.
            """,
            filename="konversi.py",
        ),
        E(
            "A1-01-1-ex1",
            "mudah",
            """
            Tulis fungsi `nama_tipe(nilai)` yang mengembalikan nama tipe nilai sebagai string, misalnya `"int"` atau `"str"`.
            """,
            """
            def nama_tipe(nilai):
                # TODO: implementasikan
                pass
            """,
            """
            assert nama_tipe(5) == "int"
            assert nama_tipe(2.5) == "float"
            assert nama_tipe("a") == "str"
            assert nama_tipe(True) == "bool"
            assert nama_tipe(None) == "NoneType"
            """,
            "Gunakan type(nilai).__name__.",
            """
            def nama_tipe(nilai):
                return type(nilai).__name__
            """,
        ),
        E(
            "A1-01-1-ex2",
            "mudah",
            """
            Tulis fungsi `tukar(a, b)` yang mengembalikan tuple `(b, a)` tanpa memakai variabel bantu.
            """,
            """
            def tukar(a, b):
                # TODO: implementasikan
                pass
            """,
            """
            assert tukar(1, 2) == (2, 1)
            assert tukar("x", "y") == ("y", "x")
            assert tukar(None, 0) == (0, None)
            """,
            "Python bisa langsung mengembalikan b, a.",
            """
            def tukar(a, b):
                return b, a
            """,
        ),
        E(
            "A1-01-1-ex3",
            "sedang",
            """
            Tulis fungsi `ke_angka(teks)` yang mengubah string menjadi int bila bisa. Jika tidak bisa tetapi bisa menjadi float kembalikan float. Jika keduanya gagal kembalikan `None`.
            """,
            """
            def ke_angka(teks):
                # TODO: implementasikan
                pass
            """,
            """
            assert ke_angka("42") == 42 and isinstance(ke_angka("42"), int)
            assert ke_angka("3.5") == 3.5
            assert ke_angka("halo") is None
            assert ke_angka("-7") == -7
            assert ke_angka("") is None
            """,
            "Coba int() dalam blok try, lalu float(), tangkap ValueError.",
            """
            def ke_angka(teks):
                try:
                    return int(teks)
                except ValueError:
                    pass
                try:
                    return float(teks)
                except ValueError:
                    return None
            """,
        ),
        E(
            "A1-01-1-ex4",
            "menantang",
            """
            Tulis fungsi `valid_nama(nama)` yang mengembalikan `True` bila `nama` adalah nama variabel Python yang sah menurut aturan penamaan dan tidak ada di himpunan `RESERVED` yang sudah disediakan.
            """,
            """
            RESERVED = {"for", "if", "class", "def", "while", "return"}

            def valid_nama(nama):
                # TODO: implementasikan
                pass
            """,
            """
            assert valid_nama("rata_rata") is True
            assert valid_nama("_x1") is True
            assert valid_nama("1x") is False
            assert valid_nama("for") is False
            assert valid_nama("return") is False
            assert valid_nama("a-b") is False
            assert valid_nama("") is False
            """,
            "String punya metode isidentifier(). Gabungkan dengan pemeriksaan keanggotaan di RESERVED.",
            """
            RESERVED = {"for", "if", "class", "def", "while", "return"}

            def valid_nama(nama):
                return nama.isidentifier() and nama not in RESERVED
            """,
        ),
    ],
    [
        M("Menulis true atau false dengan huruf kecil.", "Tulis True dan False dengan huruf kapital di awal."),
        M("Menjumlahkan teks dan angka langsung.", "Ubah dulu salah satunya dengan str() atau int()."),
        M("Memakai nama bawaan seperti list atau sum sebagai variabel.", "Pilih nama lain yang lebih deskriptif."),
    ],
    [
        Q("Apa tipe dari nilai 7.0?", ["int", "float", "str", "bool"], 1, "Angka dengan titik desimal bertipe float meski bagian pecahannya nol.", hint="Perhatikan ada tidaknya titik desimal."),
        Q("Hasil int(-3.9)?", ["-4", "-3", "3", "Error"], 1, "int() memotong menuju nol sehingga -3.9 menjadi -3.", hint="int() tidak membulatkan."),
        Q("Nama variabel mana yang tidak sah?", ["harga_2", "_total", "2harga", "Harga"], 2, "Nama tidak boleh diawali angka.", hint="Lihat karakter pertama."),
        Q("Hasil bool('0')?", ["False", "True", "Error", "None"], 1, "String tidak kosong selalu True, termasuk '0'.", hint="Yang menentukan hanya apakah string kosong."),
        Q("Setelah x = 10, y = x, x = 25, berapa y?", ["25", "10", "35", "Error"], 1, "y tetap menunjuk ke nilai 10 karena penugasan tidak menghubungkan dua nama.", hint="Mengubah x tidak menyentuh y."),
    ],
    [
        "Variabel adalah nama yang menunjuk ke nilai dan tipe melekat pada nilai.",
        "Lima tipe dasar adalah int, float, str, bool, dan None.",
        "Gunakan snake_case dan jangan menimpa nama bawaan.",
        "Konversi dengan int, float, str, bool dan kenali truthiness.",
    ],
    [],
)

l2 = lesson(
    "A1-01-2",
    "Operator aritmetika, perbandingan, dan logika",
    35,
    [
        "Memakai operator aritmetika termasuk //, %, dan **",
        "Menjelaskan mengapa 0.1 + 0.2 tidak persis 0.3 dan cara membandingkan float",
        "Menyusun ekspresi perbandingan termasuk perbandingan berantai",
        "Menggabungkan kondisi dengan and, or, not dan memahami short-circuit",
    ],
    [
        T("""
        ## Operator aritmetika

        Python menyediakan operator aritmetika yang familiar: `+`, `-`, `*`, dan `/`. Perhatikan bahwa pembagian `/` selalu menghasilkan float, bahkan bila hasilnya bulat: `6 / 3` adalah `2.0`. Untuk pembagian bulat yang membuang pecahan, pakai `//`. Untuk sisa bagi, pakai `%`. Untuk pangkat, pakai `**`.

        Operator sisa bagi sangat berguna. Ia mengecek bilangan genap atau ganjil (`n % 2`), mengelompokkan indeks secara melingkar, dan mengubah detik menjadi menit dan sisa detik. Pembagian bulat dan sisa bagi saling melengkapi: untuk bilangan positif, `a == (a // b) * b + a % b` selalu benar.

        Untuk bilangan negatif, `//` membulatkan ke bawah menuju minus tak hingga, bukan menuju nol. Jadi `-7 // 2` adalah `-4`. Perilaku ini berbeda dengan sebagian bahasa lain, dan menjadi sumber kejutan bila kamu terbiasa dengan bahasa tersebut.
        """),
        C(
            """
            print(7 / 2, 7 // 2, 7 % 2, 2 ** 10)
            print(-7 // 2, -7 % 2)
            detik = 3725
            menit, sisa = divmod(detik, 60)
            jam, menit = divmod(menit, 60)
            print(jam, menit, sisa)
            """,
            """
            3.5 3 1 1024
            -4 1
            1 2 5
            """,
            """
            `divmod` mengembalikan hasil bagi bulat dan sisa sekaligus, cocok untuk konversi satuan waktu.
            """,
            filename="aritmetika.py",
        ),
        T("""
        ## Galat pembulatan pada float

        Komputer menyimpan float dalam biner, dan banyak pecahan desimal sederhana tidak punya representasi biner yang tepat. Akibatnya `0.1 + 0.2` menghasilkan `0.30000000000000004`, bukan `0.3`. Ini bukan bug Python, melainkan sifat standar IEEE 754 yang dipakai hampir semua bahasa.

        Konsekuensinya, jangan pernah membandingkan dua float dengan `==` bila keduanya hasil perhitungan. Gunakan toleransi: dua angka dianggap sama bila selisih mutlaknya sangat kecil. Modul `math` menyediakan `math.isclose(a, b)` untuk itu.

        Dalam data science kamu akan sering menghitung rata-rata, jumlah, dan rasio dari float, sehingga kebiasaan ini penting. Untuk uang, pertimbangkan menyimpan sebagai bilangan bulat dalam satuan terkecil, misalnya sen, atau memakai modul `decimal`.
        """),
        C(
            """
            import math

            print(0.1 + 0.2)
            print(0.1 + 0.2 == 0.3)
            print(math.isclose(0.1 + 0.2, 0.3))
            print(round(0.1 + 0.2, 2) == 0.3)
            """,
            """
            0.30000000000000004
            False
            True
            True
            """,
            """
            Perbandingan `==` gagal karena galat biner kecil. `math.isclose` dan pembulatan sama-sama memberi jawaban yang diharapkan.
            """,
            filename="float_galat.py",
        ),
        T("""
        ## Operator perbandingan dan hasilnya

        Operator perbandingan adalah `==`, `!=`, `<`, `>`, `<=`, dan `>=`. Hasilnya selalu bertipe bool. Jangan keliru antara `=` yang menugaskan dan `==` yang membandingkan. Menulis `if x = 3` menimbulkan `SyntaxError`, yang justru membantu menangkap kesalahan itu.

        Python mengizinkan perbandingan berantai yang terbaca seperti matematika: `0 <= x < 10` bernilai benar bila x berada di rentang nol sampai sebelum sepuluh. Ini lebih ringkas dan lebih jelas daripada `x >= 0 and x < 10`.

        Teks juga bisa dibandingkan dan diurutkan secara leksikografis berdasarkan kode karakter. Huruf kapital berurutan sebelum huruf kecil, jadi `"Z" < "a"` bernilai benar. Karena itu, untuk perbandingan tanpa peduli kapitalisasi, ubah kedua teks ke huruf kecil lebih dulu.
        """),
        T("""
        ## Operator logika dan short-circuit

        Operator `and`, `or`, dan `not` menggabungkan kondisi. `and` benar bila keduanya benar, `or` benar bila salah satunya benar, dan `not` membalik nilai. Prioritasnya: `not` lebih dulu, lalu `and`, lalu `or`. Gunakan tanda kurung agar maksud kamu jelas bagi pembaca.

        Python mengevaluasi dengan **short-circuit**: pada `A and B`, bila A salah maka B tidak pernah dievaluasi karena hasilnya sudah pasti salah. Pada `A or B`, bila A benar maka B dilewati. Sifat ini dipakai untuk menjaga keamanan, misalnya `n != 0 and 10 / n > 2` tidak akan pernah membagi dengan nol.

        Satu detail menarik: `and` dan `or` mengembalikan salah satu operandnya, bukan selalu True atau False. `"" or "default"` menghasilkan `"default"`. Pola ini sering dipakai untuk nilai bawaan.
        """),
        C(
            """
            x = 7
            print(0 <= x < 10, 10 <= x < 20)
            n = 0
            print(n != 0 and 10 / n > 2)
            print("" or "default", "isi" or "default")
            print(not (x > 5 and x < 6), x > 5 or 1 / 0)
            print("Z" < "a", "z".lower() == "Z".lower())
            """,
            """
            True False
            False
            default isi
            True True
            True True
            """,
            """
            Short-circuit mencegah pembagian dengan nol dan membuat ekspresi `x > 5 or 1 / 0` aman. Operator `or` mengembalikan operand pertama yang bernilai benar.
            """,
            filename="logika.py",
        ),
        T("""
        ## Penugasan gabungan dan urutan evaluasi

        Operator penugasan gabungan seperti `+=`, `-=`, `*=`, dan `//=` menyingkat pola `x = x + 1` menjadi `x += 1`. Pola ini ada di hampir setiap perulangan penghitung. Python tidak punya operator `++`, jadi kamu menulis `x += 1`.

        Urutan evaluasi mengikuti prioritas: tanda kurung, lalu pangkat, lalu perkalian dan pembagian, lalu penjumlahan dan pengurangan, kemudian perbandingan, dan terakhir operator logika. Meski begitu, jangan mengandalkan hafalan. Tanda kurung tambahan tidak merugikan dan membuat maksud langsung terbaca. Ekspresi seperti `-2 ** 2` bernilai `-4`, karena pangkat lebih kuat dari tanda minus, dan ini sering mengejutkan pemula.

        Latih kebiasaan memecah ekspresi panjang menjadi beberapa baris dengan variabel perantara yang bernama jelas. Kode data science yang mudah dibaca sama pentingnya dengan kode yang benar.
        """),
        K(
            "note",
            """
            Operator `==` membandingkan nilai, sedangkan `is` memeriksa apakah dua nama menunjuk ke objek yang sama. Untuk angka dan teks gunakan `==`. Gunakan `is` hanya untuk `None`, misalnya `if hasil is None`, karena `None` hanya ada satu di seluruh program dan itulah cara yang dianjurkan.
            """,
            title="Perbedaan == dan is",
        ),
        E(
            "A1-01-2-ex1",
            "mudah",
            """
            Tulis fungsi `genap(n)` yang mengembalikan `True` bila bilangan bulat `n` genap.
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
            "Sisa bagi dengan 2 sama dengan nol.",
            """
            def genap(n):
                return n % 2 == 0
            """,
        ),
        E(
            "A1-01-2-ex2",
            "mudah",
            """
            Tulis fungsi `ke_jam(detik)` yang mengembalikan tuple `(jam, menit, sisa_detik)`.
            """,
            """
            def ke_jam(detik):
                # TODO: implementasikan
                pass
            """,
            """
            assert ke_jam(3725) == (1, 2, 5)
            assert ke_jam(59) == (0, 0, 59)
            assert ke_jam(7200) == (2, 0, 0)
            """,
            "Pakai divmod dua kali.",
            """
            def ke_jam(detik):
                menit, sisa = divmod(detik, 60)
                jam, menit = divmod(menit, 60)
                return jam, menit, sisa
            """,
        ),
        E(
            "A1-01-2-ex3",
            "sedang",
            """
            Tulis fungsi `hampir_sama(a, b, toleransi)` yang mengembalikan `True` bila selisih mutlak `a` dan `b` tidak lebih dari `toleransi`.
            """,
            """
            def hampir_sama(a, b, toleransi):
                # TODO: implementasikan
                pass
            """,
            """
            assert hampir_sama(0.1 + 0.2, 0.3, 1e-9) is True
            assert hampir_sama(1.0, 1.1, 0.05) is False
            assert hampir_sama(5, 5, 0) is True
            assert hampir_sama(1.0, 1.05, 0.05) is True
            """,
            "Gunakan abs(a - b) <= toleransi. Perhatikan galat float pada kasus terakhir, uji dengan nilai yang aman.",
            """
            def hampir_sama(a, b, toleransi):
                return abs(a - b) <= toleransi + 1e-12
            """,
        ),
        E(
            "A1-01-2-ex4",
            "menantang",
            """
            Tulis fungsi `tahun_kabisat(tahun)` yang mengembalikan `True` bila tahun kabisat: habis dibagi 4, kecuali habis dibagi 100 tetapi tidak habis dibagi 400.
            """,
            """
            def tahun_kabisat(tahun):
                # TODO: implementasikan
                pass
            """,
            """
            assert tahun_kabisat(2024) is True
            assert tahun_kabisat(2023) is False
            assert tahun_kabisat(1900) is False
            assert tahun_kabisat(2000) is True
            assert tahun_kabisat(2100) is False
            """,
            "Gabungkan tiga kondisi dengan and dan or serta tanda kurung.",
            """
            def tahun_kabisat(tahun):
                return (tahun % 4 == 0 and tahun % 100 != 0) or tahun % 400 == 0
            """,
        ),
    ],
    [
        M("Membandingkan float hasil hitungan dengan ==.", "Pakai math.isclose atau toleransi selisih."),
        M("Menukar = dengan == pada kondisi.", "Pakai == untuk membandingkan dan = hanya untuk menugaskan."),
        M("Mengira // selalu membulatkan menuju nol.", "Ingat bahwa // membulatkan ke bawah, jadi -7 // 2 adalah -4."),
    ],
    [
        Q("Hasil 7 // 2?", ["3.5", "3", "4", "1"], 1, "Pembagian bulat membuang pecahan sehingga hasilnya 3.", hint="Operator // memberi bagian bulat."),
        Q("Hasil -7 // 2?", ["-3", "-4", "3", "-3.5"], 1, "Pembagian bulat membulatkan ke bawah.", hint="Ke bawah berarti makin negatif."),
        Q("Mengapa 0.1 + 0.2 == 0.3 bernilai False?", ["Bug Python", "Float disimpan sebagai pendekatan biner", "Operator salah", "Angka terlalu kecil"], 1, "Banyak pecahan desimal tidak punya representasi biner tepat.", hint="Pikirkan cara komputer menyimpan float."),
        Q("Hasil dari 0 <= 5 < 10?", ["True", "False", "Error", "None"], 0, "Perbandingan berantai memeriksa kedua sisi sekaligus.", hint="Baca seperti notasi matematika."),
        Q("Hasil dari '' or 'default'?", ["''", "'default'", "True", "False"], 1, "or mengembalikan operand pertama yang bernilai benar, dan string kosong salah.", hint="Operand mana yang pertama benar?"),
    ],
    [
        "Gunakan /, //, %, dan ** sesuai kebutuhan dan ingat // membulatkan ke bawah.",
        "Float punya galat biner sehingga bandingkan dengan toleransi.",
        "Perbandingan bisa dirantai dan menghasilkan bool.",
        "and dan or memakai short-circuit dan mengembalikan operand.",
    ],
    [],
)

l3 = lesson(
    "A1-01-3",
    "Output terformat dan input yang aman",
    35,
    [
        "Menampilkan nilai dengan print() dan mengatur sep serta end",
        "Menyusun teks dengan f-string termasuk format angka dan lebar kolom",
        "Mengolah input pengguna yang selalu berupa teks",
        "Membuat fungsi yang menolak input tidak valid dengan pesan yang jelas",
    ],
    [
        T("""
        ## print dan pengaturannya

        Fungsi `print()` menampilkan nilai ke layar. Ia menerima banyak argumen dan memisahkannya dengan spasi. Parameter `sep` mengubah pemisah, dan parameter `end` mengubah akhiran baris yang secara bawaan adalah baris baru. `print(1, 2, 3, sep="-")` menampilkan `1-2-3`, dan `print("a", end="")` tidak pindah baris.

        Dalam eksplorasi data, `print` adalah alat debugging paling cepat. Kamu menampilkan nilai perantara untuk memastikan perhitungan benar. Di notebook, nilai ekspresi terakhir sebuah sel ditampilkan otomatis, tetapi `print` tetap berguna ketika kamu ingin beberapa keluaran dari satu sel.

        Kebiasaan baik adalah menampilkan label bersama nilai, misalnya `print("rata-rata:", rata)`, supaya keluaran berbaris-baris tidak membingungkan.
        """),
        T("""
        ## f-string untuk teks yang rapi

        Cara modern menyisipkan nilai ke dalam teks adalah **f-string**: awali string dengan huruf `f` dan taruh ekspresi di dalam kurung kurawal. `f"Halo {nama}"` mengganti `{nama}` dengan isi variabel. Ekspresi apa pun boleh berada di dalam kurung kurawal, termasuk perhitungan.

        Setelah ekspresi kamu bisa menambah spesifikasi format dengan titik dua. `{harga:.2f}` menampilkan dua angka di belakang koma, `{n:,}` memberi pemisah ribuan, `{rasio:.1%}` menampilkan persentase, dan `{teks:>10}` menyelaraskan ke kanan dalam lebar sepuluh karakter. Format ini membuat tabel teks rapi tanpa pustaka tambahan.

        Menyisipkan tanda `{` literal dilakukan dengan menggandakannya: `{{`. Dan sejak Python 3.8 ada bentuk `{nilai=}` yang menampilkan nama dan nilai sekaligus, sangat berguna untuk debugging cepat.
        """),
        C(
            """
            nama = "Sari"
            harga = 1234567.891
            rasio = 0.4567
            print(f"Halo {nama}, total {harga:,.2f}")
            print(f"Akurasi {rasio:.1%}")
            print(f"[{nama:>8}] [{nama:<8}] [{nama:^8}]")
            print(f"{2 * 3 + 1 = }")
            print(1, 2, 3, sep="-", end="!\\n")
            """,
            """
            Halo Sari, total 1,234,567.89
            Akurasi 45.7%
            [    Sari] [Sari    ] [  Sari  ]
            2 * 3 + 1 = 7
            1-2-3!
            """,
            """
            F-string mendukung ribuan, persentase, dan perataan. Bentuk `{ekspresi = }` menampilkan teks ekspresi bersama hasilnya.
            """,
            filename="fstring.py",
        ),
        T("""
        ## Input selalu berupa teks

        Fungsi `input()` membaca satu baris dari pengguna dan selalu mengembalikan string. Jika pengguna mengetik 25, hasilnya adalah `"25"`, bukan angka. Untuk menghitung kamu harus mengonversinya, dan konversi itu bisa gagal bila pengguna mengetik hal lain.

        Aturan emas pemrograman: jangan percaya input. Selalu anggap input bisa kosong, berisi spasi berlebih, salah ketik, atau di luar rentang. Bersihkan dengan `strip()`, ubah dengan `int()` di dalam `try`, lalu periksa rentang nilainya.

        Pola ini tetap dipakai ketika kamu membaca CSV atau JSON di modul berikutnya. Data dari luar program selalu berpotensi kotor, dan fungsi yang kuat melaporkan masalah dengan pesan yang jelas, bukan crash tanpa penjelasan.
        """),
        A(
            "Analogi petugas pintu",
            """
            Anggap fungsi kamu sebagai gedung dan input sebagai tamu. Petugas pintu memeriksa identitas tamu sebelum mengizinkan masuk. Validasi input adalah petugas itu: tamu yang salah ditolak dengan sopan dan alasan yang jelas, bukan dibiarkan masuk lalu merusak isi gedung.
            """,
        ),
        C(
            """
            def baca_umur(teks):
                teks = teks.strip()
                if not teks:
                    raise ValueError("umur kosong")
                umur = int(teks)
                if not 0 <= umur <= 130:
                    raise ValueError(f"umur di luar rentang: {umur}")
                return umur

            for contoh in [" 25 ", "", "abc", "200"]:
                try:
                    print(baca_umur(contoh))
                except ValueError as e:
                    print("galat:", e)
            """,
            """
            25
            galat: umur kosong
            galat: invalid literal for int() with base 10: 'abc'
            galat: umur di luar rentang: 200
            """,
            """
            Fungsi membersihkan spasi, mengonversi, lalu memeriksa rentang. Setiap kegagalan menghasilkan `ValueError` dengan pesan yang bisa ditampilkan ke pengguna.
            """,
            filename="validasi_umur.py",
        ),
        T("""
        ## Membangun laporan teks dari data

        Setelah mampu memformat satu nilai, kamu bisa merakit laporan kecil. Misalkan kamu punya nama produk, harga, dan jumlah terjual. Satu baris laporan memuat nama yang rata kiri, harga dengan pemisah ribuan, dan jumlah rata kanan. Dengan lebar kolom tetap, banyak baris akan sejajar rapi di layar atau file teks.

        Pola ini sering dipakai untuk log eksperimen. Setelah melatih model, kamu mencetak satu baris berisi nomor epoch, loss, dan akurasi dengan format tetap, sehingga perkembangan mudah dipindai mata. Konsistensi format juga memudahkan pemrosesan log itu kemudian dengan skrip lain.

        Perlu diingat bahwa spesifikasi format hanya mengubah tampilan, bukan nilai asli. Nilai `3.14159` tetap utuh di variabel meski ditampilkan sebagai `3.14`. Bila kamu ingin nilainya benar-benar dibulatkan untuk perhitungan lanjutan, gunakan `round()`.
        """),
        C(
            """
            produk = [("Kopi", 15000, 3), ("Teh", 7500.5, 12), ("Roti", 22000, 1)]
            total = 0
            for nama, harga, jumlah in produk:
                print(f"{nama:<8}{harga:>12,.2f}{jumlah:>4}")
                total += harga * jumlah
            print(f"{'Total':<8}{total:>12,.2f}")
            """,
            """
            Kopi       15,000.00   3
            Teh         7,500.50  12
            Roti       22,000.00   1
            Total     157,006.00
            """,
            """
            Lebar kolom tetap membuat angka sejajar. Total dihitung dari nilai asli, sedangkan format hanya memengaruhi tampilan.
            """,
            filename="laporan_teks.py",
        ),
        T("""
        ## Escape dan teks multibaris

        Beberapa karakter khusus ditulis dengan garis miring terbalik. `\\n` adalah baris baru, `\\t` adalah tab, dan `\\\\` adalah garis miring itu sendiri. Untuk teks yang membentang beberapa baris, apit dengan tiga tanda kutip ganda, dan Python mempertahankan baris barunya. Prefiks `r` membuat string mentah yang tidak memproses escape, berguna untuk jalur file Windows dan ekspresi reguler.

        Gabungkan semua ini dan kamu bisa dengan cepat membuat laporan kecil yang terstruktur tanpa pustaka apa pun, cukup dari f-string, lebar kolom, dan baris baru. Latih dengan mengubah lebar dan perataan sampai tampilannya rapi.
        """),
        K(
            "tip",
            """
            Saat membuat log pelatihan, pakai f-string dengan lebar tetap seperti `{epoch:>3} {loss:.4f}` agar kolom selalu sejajar.
            """,
            title="Tips log rapi",
        ),
        E(
            "A1-01-3-ex1",
            "mudah",
            """
            Tulis fungsi `sapa(nama, umur)` yang mengembalikan string `"Halo <nama>, umur <umur> tahun"`.
            """,
            """
            def sapa(nama, umur):
                # TODO: implementasikan
                pass
            """,
            """
            assert sapa("Sari", 21) == "Halo Sari, umur 21 tahun"
            assert sapa("Budi", 30) == "Halo Budi, umur 30 tahun"
            assert sapa("", 0) == "Halo , umur 0 tahun"
            """,
            "Gunakan f-string dengan dua ekspresi.",
            """
            def sapa(nama, umur):
                return f"Halo {nama}, umur {umur} tahun"
            """,
        ),
        E(
            "A1-01-3-ex2",
            "mudah",
            """
            Tulis fungsi `persen(rasio)` yang mengembalikan string persentase dengan satu desimal, misalnya `0.4567` menjadi `"45.7%"`.
            """,
            """
            def persen(rasio):
                # TODO: implementasikan
                pass
            """,
            """
            assert persen(0.4567) == "45.7%"
            assert persen(1) == "100.0%"
            assert persen(0) == "0.0%"
            """,
            "Spesifikasi format .1% sudah mengalikan dengan 100.",
            """
            def persen(rasio):
                return f"{rasio:.1%}"
            """,
        ),
        E(
            "A1-01-3-ex3",
            "sedang",
            """
            Tulis fungsi `baca_umur(teks)` yang membersihkan spasi, mengubah ke int, dan mengembalikan umur. Jika teks kosong atau bukan angka atau di luar 0 sampai 130, naikkan `ValueError`.
            """,
            """
            def baca_umur(teks):
                # TODO: implementasikan
                pass
            """,
            """
            assert baca_umur(" 25 ") == 25
            def gagal(t):
                try:
                    baca_umur(t)
                except ValueError:
                    return True
                return False
            assert gagal("")
            assert gagal("abc")
            assert gagal("200")
            assert gagal("-1")
            """,
            "int() sudah menaikkan ValueError untuk teks bukan angka. Periksa rentang sendiri.",
            """
            def baca_umur(teks):
                teks = teks.strip()
                if not teks:
                    raise ValueError("umur kosong")
                umur = int(teks)
                if not 0 <= umur <= 130:
                    raise ValueError("umur di luar rentang")
                return umur
            """,
        ),
        E(
            "A1-01-3-ex4",
            "menantang",
            """
            Tulis fungsi `baris_tabel(nama, harga, jumlah)` yang mengembalikan satu baris teks: nama rata kiri lebar 10, harga rata kanan lebar 12 dengan pemisah ribuan dan dua desimal, jumlah rata kanan lebar 5. Pisahkan kolom dengan satu spasi.
            """,
            """
            def baris_tabel(nama, harga, jumlah):
                # TODO: implementasikan
                pass
            """,
            """
            assert baris_tabel("Kopi", 15000, 3) == "Kopi          15,000.00     3"
            assert baris_tabel("Teh", 7500.5, 12) == "Teh            7,500.50    12"
            assert len(baris_tabel("X", 1, 1)) == 10 + 1 + 12 + 1 + 5
            """,
            "Gunakan {nama:<10} {harga:>12,.2f} {jumlah:>5}.",
            """
            def baris_tabel(nama, harga, jumlah):
                return f"{nama:<10} {harga:>12,.2f} {jumlah:>5}"
            """,
        ),
    ],
    [
        M("Mengira input() mengembalikan angka.", "Ubah hasilnya dengan int() atau float() di dalam try."),
        M("Menyusun teks dengan + dan lupa mengubah angka menjadi str.", "Pakai f-string agar konversi otomatis."),
        M("Percaya input pengguna tanpa memeriksa.", "Bersihkan, konversi, lalu periksa rentang dan laporkan galat dengan jelas."),
    ],
    [
        Q("Tipe hasil input()?", ["int", "float", "str", "bool"], 2, "input() selalu mengembalikan string.", hint="Apa pun yang diketik pengguna adalah teks."),
        Q("Format {x:.2f} untuk x = 3.14159?", ["3.1", "3.14", "3.142", "3"], 1, "Spesifikasi .2f menampilkan dua desimal.", hint="Angka setelah titik adalah jumlah desimal."),
        Q("Fungsi parameter end pada print?", ["Pemisah argumen", "Akhiran baris", "Lebar teks", "Jumlah cetak"], 1, "end menentukan apa yang dicetak di akhir, bawaannya baris baru.", hint="Bandingkan dengan sep."),
        Q("Apa hasil f'{0.25:.0%}'?", ["25%", "0%", "0.25%", "2%"], 0, "Format persen mengalikan dengan 100.", hint="Format % mengalikan seratus."),
        Q("Mengapa memvalidasi input?", ["Agar kode lebih panjang", "Karena data luar bisa kotor atau salah", "Python mewajibkan", "Untuk mempercepat"], 1, "Input luar tidak bisa dipercaya sehingga perlu diperiksa dan dilaporkan jelas.", hint="Pikirkan siapa yang mengetik."),
    ],
    [
        "print punya sep dan end untuk mengatur keluaran.",
        "f-string mendukung format angka, persen, dan perataan.",
        "input() selalu string sehingga perlu dikonversi dengan aman.",
        "Validasi input dengan pesan galat yang jelas.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa kode dan contoh singkat yang cukup jelas dalam teks dan latihan.", "brief": []}

write_module(
    "A1",
    1,
    "Variabel, tipe data, dan operator",
    105,
    [
        "Menggunakan variabel dan lima tipe dasar Python dengan benar",
        "Menulis ekspresi aritmetika, perbandingan, dan logika yang aman",
        "Memformat keluaran dan memvalidasi input pengguna",
    ],
    [l1, l2, l3],
    video,
    REF,
)
