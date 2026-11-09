import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

l1 = lesson(
    "A1-05-1",
    "List comprehension",
    35,
    [
        "Mengubah perulangan for yang membangun list menjadi list comprehension",
        "Menambahkan kondisi filter dan ekspresi if else pada comprehension",
        "Memakai comprehension bersarang untuk matriks dan kombinasi",
        "Menilai kapan comprehension lebih jelas dan kapan perulangan lebih baik",
    ],
    [
        T("""
        ## Dari perulangan ke comprehension

        Salah satu pola paling sering dalam Python adalah membuat list baru dengan menelusuri list lain. Versi perulangan memakai tiga baris: buat list kosong, telusuri dengan `for`, lalu `append`. **List comprehension** menyatakan hal yang sama dalam satu ekspresi: `[ekspresi for item in urutan]`. Hasilnya adalah list baru berisi ekspresi yang dihitung untuk setiap item.

        Bentuk ini bukan sekadar singkat. Ia menyatakan niat dengan jelas: "buat list dari ini". Pembaca langsung melihat apa yang dihasilkan dan dari mana asalnya. Comprehension juga umumnya sedikit lebih cepat daripada perulangan dengan `append` karena dioptimalkan oleh interpreter.

        Dalam data science, comprehension dipakai terus-menerus untuk menurunkan fitur, membersihkan teks, dan menyaring baris sebelum data masuk ke NumPy atau pandas.
        """),
        C(
            """
            angka = [1, 2, 3, 4, 5]

            kuadrat = []
            for x in angka:
                kuadrat.append(x * x)
            print(kuadrat)

            print([x * x for x in angka])
            print([x + 0.5 for x in angka])
            kata = ["apel", "kiwi", "mangga"]
            print([k.upper() for k in kata])
            print([len(k) for k in kata])
            print([(i, k) for i, k in enumerate(kata)])
            """,
            """
            [1, 4, 9, 16, 25]
            [1, 4, 9, 16, 25]
            [1.5, 2.5, 3.5, 4.5, 5.5]
            ['APEL', 'KIWI', 'MANGGA']
            [4, 4, 6]
            [(0, 'apel'), (1, 'kiwi'), (2, 'mangga')]
            """,
            """
            Comprehension setara dengan perulangan `append` tetapi lebih ringkas. Ekspresinya boleh berupa operasi, pemanggilan metode, atau tuple.
            """,
            filename="comprehension_dasar.py",
        ),
        T("""
        ## Kondisi filter dan if else

        Tambahkan `if` di akhir untuk menyaring item: `[x for x in angka if x % 2 == 0]` hanya mengambil bilangan genap. Kondisi di akhir ini menentukan item mana yang ikut, sehingga panjang hasil bisa lebih pendek dari sumber.

        Berbeda dengan itu, `if else` di bagian ekspresi mengubah nilai setiap item tetapi tidak membuang apa pun: `["lulus" if n >= 75 else "remedial" for n in nilai]`. Posisinya penting. `if` saja ditaruh di akhir untuk menyaring, sedangkan `if else` ditaruh di depan untuk memilih nilai. Mencampurnya adalah kesalahan sintaks yang umum.

        Kamu boleh memakai keduanya sekaligus: saring dulu di akhir, lalu ubah nilai di depan. Namun bila kondisinya mulai rumit, pertimbangkan menulis fungsi pembantu agar comprehension tetap mudah dibaca.
        """),
        C(
            """
            angka = [1, 2, 3, 4, 5, 6]
            print([x for x in angka if x % 2 == 0])
            print([x * x for x in angka if x > 3])

            nilai = [90, 60, 75, 40]
            print(["lulus" if n >= 75 else "remedial" for n in nilai])
            print([n for n in nilai if n >= 60])
            print(["tinggi" if n > 80 else "sedang" for n in nilai if n >= 60])
            teks = "Halo Dunia 2025 Selamat Datang"
            print([c for c in teks if c.isdigit()])
            print([k for k in teks.split() if k[0].isupper()])
            """,
            """
            [2, 4, 6]
            [16, 25, 36]
            ['lulus', 'remedial', 'lulus', 'remedial']
            [90, 60, 75]
            ['tinggi', 'sedang', 'sedang']
            ['2', '0', '2', '5']
            ['Halo', 'Dunia', 'Selamat', 'Datang']
            """,
            """
            `if` di akhir menyaring item, `if else` di depan memilih nilai. Keduanya bisa dipakai bersama.
            """,
            filename="comprehension_kondisi.py",
        ),
        K(
            "warning",
            """
            Posisi `if` menentukan artinya. `[x for x in a if x > 0]` menyaring. `[x if x > 0 else 0 for x in a]` mengubah nilai. Menulis `[x for x in a if x > 0 else 0]` adalah SyntaxError.
            """,
            title="Dua kegunaan if",
        ),
        T("""
        ## Comprehension bersarang

        Comprehension dapat memiliki lebih dari satu klausa `for`. Urutan penulisannya sama dengan urutan perulangan bersarang yang ditulis biasa: klausa pertama adalah perulangan luar dan klausa berikutnya adalah perulangan dalam. `[(a, b) for a in [1, 2] for b in "xy"]` menghasilkan semua pasangan.

        Comprehension juga bisa bersarang sebagai ekspresi. Membuat matriks tabel kali: `[[i * j for j in range(1, 4)] for i in range(1, 4)]` menghasilkan list berisi list. Meratakan matriks menjadi satu list memakai dua klausa `for`: `[x for baris in matriks for x in baris]`.

        Dua bentuk ini mudah tertukar. Pegangan sederhana: bila hasil akhir berbentuk satu list datar, pakai dua klausa `for` berurutan. Bila hasil akhir berbentuk list berisi list, taruh comprehension kedua sebagai ekspresi pertama.
        """),
        C(
            """
            print([(a, b) for a in [1, 2] for b in "xy"])
            tabel = [[i * j for j in range(1, 4)] for i in range(1, 4)]
            print(tabel)
            print([x for baris in tabel for x in baris])
            transpos = [[baris[k] for baris in tabel] for k in range(3)]
            print(transpos == tabel)
            print([x for baris in tabel for x in baris if x % 2 == 0])
            """,
            """
            [(1, 'x'), (1, 'y'), (2, 'x'), (2, 'y')]
            [[1, 2, 3], [2, 4, 6], [3, 6, 9]]
            [1, 2, 3, 2, 4, 6, 3, 6, 9]
            True
            [2, 2, 4, 6, 6]
            """,
            """
            Dua klausa for berurutan menghasilkan list datar, sedangkan comprehension di dalam ekspresi menghasilkan list bersarang. Tabel kali simetris sehingga transposnya sama.
            """,
            filename="comprehension_bersarang.py",
        ),
        T("""
        ## Kapan comprehension, kapan perulangan

        Comprehension unggul bila tugasnya hanya membangun satu list dari satu sumber dengan transformasi dan filter sederhana. Bila kamu membutuhkan banyak langkah, efek samping seperti mencetak, atau beberapa kondisi yang saling terkait, perulangan `for` biasa lebih jelas.

        Panduan praktis: bila comprehension tidak muat nyaman dalam satu atau dua baris, atau kamu perlu membaca ulang untuk memahaminya, tulis ulang sebagai perulangan atau pecah menjadi fungsi pembantu. Kode yang pintar tetapi tidak terbaca adalah beban bagi tim.

        Jangan pula memakai comprehension hanya untuk efek samping, misalnya `[print(x) for x in data]`. Ia membuat list tak berguna berisi `None`. Untuk efek samping, gunakan perulangan biasa. Kerjakan latihan berikut dan putuskan sendiri bentuk mana yang paling jelas di tiap kasus.
        """),
        T("""
        ## Contoh nyata dalam analisis data

        Misalkan kamu punya daftar harga dalam bentuk teks seperti `"Rp12.500"` dari hasil scraping. Dengan comprehension kamu membersihkan semuanya sekaligus: buang awalan, hapus titik, lalu ubah menjadi bilangan. Misalkan pula kamu ingin memilih hanya baris dengan nilai tidak kosong, atau memberi label pada setiap nilai berdasarkan ambang tertentu.

        Pola yang sama muncul di pandas dalam bentuk operasi pada kolom, tetapi pada tahap awal dan untuk data berukuran kecil sampai menengah, comprehension sudah sangat memadai dan tidak butuh pustaka tambahan. Menguasainya melatih cara berpikir transformasi data yang kelak terbawa ke semua alat lain.
        """),
        E(
            "A1-05-1-ex1",
            "mudah",
            """
            Tulis fungsi `kuadrat_semua(daftar)` yang mengembalikan list kuadrat tiap elemen memakai comprehension.
            """,
            """
            def kuadrat_semua(daftar):
                # TODO: implementasikan
                pass
            """,
            """
            assert kuadrat_semua([1, 2, 3]) == [1, 4, 9]
            assert kuadrat_semua([]) == []
            assert kuadrat_semua([-2, 0]) == [4, 0]
            """,
            "Bentuknya [ekspresi for x in daftar].",
            """
            def kuadrat_semua(daftar):
                return [x * x for x in daftar]
            """,
        ),
        E(
            "A1-05-1-ex2",
            "mudah",
            """
            Tulis fungsi `genap_saja(daftar)` yang mengembalikan list elemen genap dengan urutan asli.
            """,
            """
            def genap_saja(daftar):
                # TODO: implementasikan
                pass
            """,
            """
            assert genap_saja([1, 2, 3, 4]) == [2, 4]
            assert genap_saja([1, 3]) == []
            assert genap_saja([]) == []
            assert genap_saja([0, -2, 5]) == [0, -2]
            """,
            "Tambahkan if di akhir comprehension.",
            """
            def genap_saja(daftar):
                return [x for x in daftar if x % 2 == 0]
            """,
        ),
        E(
            "A1-05-1-ex3",
            "sedang",
            """
            Tulis fungsi `label_nilai(nilai)` yang mengembalikan list label untuk tiap nilai: `"A"` bila 85 ke atas, `"B"` bila 70 sampai 84, selain itu `"C"`.
            """,
            """
            def label_nilai(nilai):
                # TODO: implementasikan
                pass
            """,
            """
            assert label_nilai([90, 70, 50]) == ["A", "B", "C"]
            assert label_nilai([85, 84, 69]) == ["A", "B", "C"]
            assert label_nilai([]) == []
            """,
            "Gunakan if else bertingkat di bagian ekspresi.",
            """
            def label_nilai(nilai):
                return ["A" if n >= 85 else "B" if n >= 70 else "C" for n in nilai]
            """,
        ),
        E(
            "A1-05-1-ex4",
            "menantang",
            """
            Tulis fungsi `diagonal_dan_ratakan(m)` yang menerima matriks persegi berupa list of list dan mengembalikan tuple `(diagonal, datar)`. `diagonal` adalah list elemen `m[i][i]` dan `datar` adalah semua elemen diratakan baris demi baris. Matriks kosong menghasilkan `([], [])`.
            """,
            """
            def diagonal_dan_ratakan(m):
                # TODO: implementasikan
                pass
            """,
            """
            m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
            assert diagonal_dan_ratakan(m) == ([1, 5, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9])
            assert diagonal_dan_ratakan([[5]]) == ([5], [5])
            assert diagonal_dan_ratakan([]) == ([], [])
            """,
            "Pakai range(len(m)) untuk diagonal dan dua klausa for untuk meratakan.",
            """
            def diagonal_dan_ratakan(m):
                diag = [m[i][i] for i in range(len(m))]
                datar = [x for baris in m for x in baris]
                return diag, datar
            """,
        ),
    ],
    [
        M("Menulis if else di akhir comprehension.", "if else harus di depan, if saja di akhir."),
        M("Memakai comprehension hanya untuk efek samping.", "Gunakan perulangan for biasa."),
        M("Membuat comprehension terlalu panjang dan rumit.", "Pecah menjadi fungsi pembantu atau perulangan."),
    ],
    [
        Q("Hasil [x*2 for x in [1,2,3]]?", ["[2,4,6]", "[1,2,3]", "[1,4,9]", "6"], 0, "Setiap elemen dikalikan dua.", hint="Ekspresi di depan."),
        Q("Di mana kondisi filter ditaruh?", ["Di depan", "Di akhir setelah for", "Di tengah", "Tidak bisa"], 1, "if setelah for menyaring item.", hint="Setelah klausa for."),
        Q("Bentuk mana yang mengubah nilai tanpa membuang item?", ["[x for x in a if c]", "[x if c else y for x in a]", "[x for x in a]", "[c for x in a]"], 1, "if else di depan memilih nilai per item.", hint="Panjang hasil sama dengan sumber."),
        Q("Cara meratakan matriks m?", ["[x for x in m]", "[x for baris in m for x in baris]", "[baris for x in m]", "m.flatten()"], 1, "Dua klausa for berurutan menghasilkan list datar.", hint="Luar dulu, dalam kemudian."),
        Q("Mengapa [print(x) for x in a] buruk?", ["Error", "Membuat list berisi None yang tidak berguna", "Terlalu cepat", "Tidak bisa"], 1, "Comprehension untuk membangun list, bukan efek samping.", hint="Apa yang dikembalikan print?"),
    ],
    [
        "Comprehension membangun list dalam satu ekspresi.",
        "if di akhir menyaring, if else di depan memilih nilai.",
        "Dua klausa for berurutan meratakan, ekspresi bersarang membuat matriks.",
        "Pilih perulangan bila comprehension menjadi sulit dibaca.",
    ],
    [],
)

l2 = lesson(
    "A1-05-2",
    "Comprehension untuk dictionary dan set",
    35,
    [
        "Membuat dictionary dengan dict comprehension dari list dan pasangan",
        "Menyaring dan membalik dictionary dengan comprehension",
        "Membuat set dengan set comprehension untuk nilai unik",
        "Menggabungkan comprehension dengan zip, enumerate, dan sorted",
    ],
    [
        T("""
        ## Dict comprehension

        Sama seperti list, dictionary dapat dibangun dengan comprehension. Bentuknya `{kunci: nilai for item in urutan}`. Ia menggantikan pola membuat dictionary kosong lalu mengisinya dalam perulangan. Contoh: `{k: len(k) for k in kata}` memetakan setiap kata ke panjangnya.

        Dict comprehension paling berguna untuk tiga hal: membangun pemetaan dari list, mengubah nilai dictionary yang sudah ada, dan menyaring pasangan. Menelusuri `d.items()` memberi pasangan kunci dan nilai yang bisa langsung di-unpack di klausa `for`.

        Bila ada kunci yang sama muncul lebih dari sekali, nilai terakhir menimpa yang sebelumnya, sama seperti penugasan biasa. Ingat ini saat sumber datamu mungkin mengandung duplikat.
        """),
        C(
            """
            kata = ["apel", "kiwi", "mangga"]
            print({k: len(k) for k in kata})
            print({i: k for i, k in enumerate(kata)})
            nama = ["a", "b", "c"]
            nilai = [1, 2, 3]
            print({n: v for n, v in zip(nama, nilai)})
            stok = {"apel": 5, "jeruk": 0, "mangga": 12}
            print({k: v * 2 for k, v in stok.items()})
            print({k: v for k, v in stok.items() if v > 0})
            print({v: k for k, v in stok.items()})
            """,
            """
            {'apel': 4, 'kiwi': 4, 'mangga': 6}
            {0: 'apel', 1: 'kiwi', 2: 'mangga'}
            {'a': 1, 'b': 2, 'c': 3}
            {'apel': 10, 'jeruk': 0, 'mangga': 24}
            {'apel': 5, 'mangga': 12}
            {5: 'apel', 0: 'jeruk', 12: 'mangga'}
            """,
            """
            Dict comprehension membangun, mengubah, menyaring, dan membalik dictionary dalam satu baris.
            """,
            filename="dict_comprehension.py",
        ),
        T("""
        ## Set comprehension

        Set comprehension memakai kurung kurawal tanpa pasangan kunci: `{ekspresi for item in urutan}`. Hasilnya set, sehingga duplikat otomatis hilang dan urutan tidak terjamin. Ia berguna untuk mengambil nilai unik setelah suatu transformasi, misalnya semua huruf awal berbeda atau semua panjang kata yang muncul.

        Perhatikan perbedaan sintaks tipis antara tiga jenis: kurung siku untuk list, kurung kurawal dengan pasangan `k: v` untuk dictionary, dan kurung kurawal tanpa pasangan untuk set. Set kosong tetap harus ditulis `set()`, sedangkan `{}` adalah dictionary kosong.

        Set comprehension sering dipakai dengan `sorted` agar hasil unik dapat dibaca dalam urutan yang pasti: `sorted({k[0] for k in kata})`.
        """),
        C(
            """
            kata = ["apel", "anggur", "kiwi", "kelapa", "mangga"]
            print(sorted({k[0] for k in kata}))
            print(sorted({len(k) for k in kata}))
            print(type({x for x in [1, 2]}).__name__, type({x: x for x in [1, 2]}).__name__)
            teks = "data science itu seru"
            print(sorted({c for c in teks if c.isalpha()}))
            """,
            """
            ['a', 'k', 'm']
            [4, 6]
            set dict
            ['a', 'c', 'd', 'e', 'i', 'n', 'r', 's', 't', 'u']
            """,
            """
            Set comprehension menghasilkan nilai unik. Dibungkus `sorted` supaya urutan pasti.
            """,
            filename="set_comprehension.py",
        ),
        T("""
        ## Pola gabungan yang berguna

        Comprehension sering dipadukan dengan fungsi bawaan. `zip` menggabungkan dua urutan sejajar, `enumerate` menambahkan indeks, dan `sorted` mengurutkan hasil. Pola `{k: v for k, v in sorted(d.items(), key=lambda p: p[1], reverse=True)}` membuat dictionary baru yang terurut menurut nilai menurun.

        Pola lain yang umum adalah membuat tabel pencarian: ubah list rekaman menjadi dictionary berkunci ID sehingga pencarian menjadi cepat, `{r["id"]: r for r in rekaman}`. Ini setara dengan membuat indeks pada basis data.

        Untuk mengambil N nilai teratas dari dictionary, urutkan pasangan lalu iris: `sorted(d.items(), key=lambda p: p[1], reverse=True)[:3]`. Hasilnya list tuple yang mudah dicetak atau diubah kembali menjadi dictionary.
        """),
        C(
            """
            skor = {"Ani": 80, "Budi": 95, "Citra": 70, "Dewi": 95}
            urut = sorted(skor.items(), key=lambda p: (-p[1], p[0]))
            print(urut)
            print(dict(urut[:2]))
            rekaman = [{"id": 7, "nama": "x"}, {"id": 9, "nama": "y"}]
            indeks = {r["id"]: r for r in rekaman}
            print(indeks[9]["nama"], sorted(indeks))
            lulus = {n for n, s in skor.items() if s >= 80}
            print(sorted(lulus))
            """,
            """
            [('Budi', 95), ('Dewi', 95), ('Ani', 80), ('Citra', 70)]
            {'Budi': 95, 'Dewi': 95}
            y [7, 9]
            ['Ani', 'Budi', 'Dewi']
            """,
            """
            Pengurutan dengan tuple kunci menangani nilai sama. Dictionary berkunci ID membuat pencarian cepat.
            """,
            filename="pola_gabungan.py",
        ),
        T("""
        ## Peringatan tentang keterbacaan dan memori

        Comprehension membangun seluruh koleksi di memori sekaligus. Untuk data sangat besar, ini bisa memboroskan memori, dan di pelajaran berikutnya kamu akan melihat generator sebagai alternatif yang menghasilkan nilai satu per satu. Untuk data kecil dan menengah, comprehension sangat tepat.

        Dari sisi keterbacaan, hindari menumpuk beberapa tingkat comprehension dan kondisi dalam satu baris. Bila kamu sulit menjelaskan comprehension itu dengan satu kalimat, pecah menjadi langkah-langkah dengan nama variabel yang jelas.

        Latihan berikut meminta kamu membangun dan mengubah dictionary serta set. Perhatikan jenis kurung yang kamu pakai, karena kesalahan kecil di sini menghasilkan tipe data yang berbeda.
        """),
        T("""
        ## Latihan berpikir: memilih bentuk yang tepat

        Sebelum menulis, tanyakan tiga hal. Pertama, apa bentuk hasil yang kamu butuhkan: urutan, pemetaan, atau kumpulan unik? Itu menentukan list, dictionary, atau set. Kedua, apakah ada item yang perlu dibuang? Itu menentukan perlunya `if` di akhir. Ketiga, apakah nilai tiap item perlu diubah? Itu menentukan isi ekspresi di depan.

        Contoh: dari daftar transaksi kamu ingin total per pelanggan. Hasilnya pemetaan, jadi dictionary. Namun total membutuhkan penjumlahan antar item, yang tidak bisa dinyatakan langsung dalam satu comprehension sederhana. Di sini pola `setdefault` atau pengelompokan dua tahap lebih jelas. Mengenali batas kemampuan comprehension sama pentingnya dengan menguasai sintaksnya.

        Contoh lain: kamu ingin tahu kota unik dari daftar alamat. Hasilnya kumpulan unik, jadi set comprehension dengan `sorted` untuk tampilan rapi. Dengan kebiasaan bertanya tiga hal tadi, pilihan bentuk menjadi hampir otomatis, dan kamu menulis kode yang tepat sasaran sejak percobaan pertama.
        """),
        T("""
        ## Kesalahan umum pada dictionary comprehension

        Kesalahan paling sering adalah lupa memakai `.items()` sehingga `for k, v in d` mencoba memecah kunci menjadi dua bagian dan menimbulkan error, atau lebih buruk, diam-diam memecah string dua huruf. Selalu telusuri `d.items()` bila butuh kunci dan nilai bersamaan.

        Kesalahan kedua adalah mengira urutan hasil acak. Sejak Python 3.7 dictionary mempertahankan urutan penyisipan, jadi urutan hasil mengikuti urutan sumber. Kesalahan ketiga adalah memakai kunci yang tidak hashable, misalnya list, yang menimbulkan `TypeError`. Ubah list menjadi tuple bila perlu dijadikan kunci.
        """),
        E(
            "A1-05-2-ex1",
            "mudah",
            """
            Tulis fungsi `panjang_kata(kata)` yang mengembalikan dictionary kata ke panjangnya.
            """,
            """
            def panjang_kata(kata):
                # TODO: implementasikan
                pass
            """,
            """
            assert panjang_kata(["a", "bb"]) == {"a": 1, "bb": 2}
            assert panjang_kata([]) == {}
            assert panjang_kata(["kiwi"]) == {"kiwi": 4}
            """,
            "Bentuknya {k: len(k) for k in kata}.",
            """
            def panjang_kata(kata):
                return {k: len(k) for k in kata}
            """,
        ),
        E(
            "A1-05-2-ex2",
            "mudah",
            """
            Tulis fungsi `huruf_awal(kata)` yang mengembalikan list terurut huruf awal unik dari list kata.
            """,
            """
            def huruf_awal(kata):
                # TODO: implementasikan
                pass
            """,
            """
            assert huruf_awal(["apel", "anggur", "kiwi"]) == ["a", "k"]
            assert huruf_awal([]) == []
            assert huruf_awal(["z"]) == ["z"]
            """,
            "Pakai set comprehension lalu sorted.",
            """
            def huruf_awal(kata):
                return sorted({k[0] for k in kata})
            """,
        ),
        E(
            "A1-05-2-ex3",
            "sedang",
            """
            Tulis fungsi `diskon(harga, persen)` yang menerima dictionary produk ke harga dan mengembalikan dictionary baru dengan harga setelah diskon, dibulatkan 2 desimal. Dictionary asli tidak boleh berubah.
            """,
            """
            def diskon(harga, persen):
                # TODO: implementasikan
                pass
            """,
            """
            h = {"a": 100, "b": 50}
            assert diskon(h, 10) == {"a": 90.0, "b": 45.0}
            assert h == {"a": 100, "b": 50}
            assert diskon({}, 5) == {}
            assert diskon({"x": 33}, 50) == {"x": 16.5}
            """,
            "Kalikan harga dengan (1 - persen / 100) di dict comprehension.",
            """
            def diskon(harga, persen):
                return {k: round(v * (1 - persen / 100), 2) for k, v in harga.items()}
            """,
        ),
        E(
            "A1-05-2-ex4",
            "menantang",
            """
            Tulis fungsi `tiga_teratas(skor)` yang menerima dictionary nama ke skor dan mengembalikan list tuple `(nama, skor)` untuk tiga skor tertinggi, urut skor menurun lalu nama naik bila sama. Bila kurang dari tiga, kembalikan semuanya.
            """,
            """
            def tiga_teratas(skor):
                # TODO: implementasikan
                pass
            """,
            """
            s = {"Ani": 80, "Budi": 95, "Citra": 70, "Dewi": 95}
            assert tiga_teratas(s) == [("Budi", 95), ("Dewi", 95), ("Ani", 80)]
            assert tiga_teratas({"x": 1}) == [("x", 1)]
            assert tiga_teratas({}) == []
            """,
            "Urutkan items dengan key tuple negatif lalu iris tiga pertama.",
            """
            def tiga_teratas(skor):
                return sorted(skor.items(), key=lambda p: (-p[1], p[0]))[:3]
            """,
        ),
    ],
    [
        M("Memakai {} untuk set kosong.", "Pakai set() karena {} adalah dictionary."),
        M("Mengira dict comprehension mempertahankan kunci duplikat.", "Kunci sama saling menimpa, nilai terakhir menang."),
        M("Mengubah dictionary asli di dalam comprehension.", "Comprehension membuat dictionary baru, asal tetap utuh."),
    ],
    [
        Q("Hasil {k: len(k) for k in ['a','bb']}?", ["{'a':1,'bb':2}", "['a','bb']", "{1,2}", "error"], 0, "Setiap kata dipetakan ke panjangnya.", hint="Ada pasangan k: v."),
        Q("Kurung mana yang membuat set comprehension?", ["[ ]", "{ } tanpa pasangan", "( )", "< >"], 1, "Kurung kurawal tanpa pasangan kunci nilai.", hint="Tidak ada tanda titik dua."),
        Q("Cara membalik dictionary d?", ["{v: k for k, v in d.items()}", "d.reverse()", "reversed(d)", "d[::-1]"], 0, "Tukar posisi kunci dan nilai saat menelusuri items.", hint="Pakai items()."),
        Q("Mengapa membungkus set dengan sorted?", ["Agar lebih cepat", "Agar urutan hasil pasti", "Agar jadi dict", "Tidak perlu"], 1, "Set tidak berurutan sehingga sorted memberi urutan tetap.", hint="Set tak punya urutan."),
        Q("Apa yang terjadi bila dua item menghasilkan kunci sama?", ["Error", "Nilai terakhir menimpa", "Nilai pertama dipertahankan", "Keduanya disimpan"], 1, "Kunci dictionary unik, penulisan ulang menimpa.", hint="Sama seperti d[k] = v."),
    ],
    [
        "Dict comprehension membangun, mengubah, menyaring, dan membalik dictionary.",
        "Set comprehension menghasilkan nilai unik tanpa urutan.",
        "Gabungkan dengan zip, enumerate, dan sorted untuk pola umum.",
        "Comprehension membangun seluruh koleksi di memori sekaligus.",
    ],
    [],
)

l3 = lesson(
    "A1-05-3",
    "Iterator dan generator",
    35,
    [
        "Memahami iterable dan iterator serta cara for bekerja",
        "Menulis generator dengan yield dan ekspresi generator",
        "Memahami evaluasi malas dan penghematan memori",
        "Memakai itertools dasar dan membangun pipeline generator",
    ],
    [
        T("""
        ## Iterable dan iterator

        Perulangan `for` bekerja pada apa pun yang *iterable*: list, string, dictionary, file, dan `range`. Di balik layar, `for` memanggil `iter(objek)` untuk mendapat **iterator**, lalu berulang kali memanggil `next(iterator)` sampai muncul `StopIteration`. Iterator mengingat posisinya dan hanya bisa maju, tidak bisa mundur atau mengulang.

        Perbedaan penting: list adalah iterable yang bisa ditelusuri berulang kali, sedangkan iterator sekali pakai. Setelah habis, ia kosong. Ini sering mengejutkan pemula saat menelusuri hasil `map` atau `zip` dua kali dan mendapati kedua kalinya kosong.

        Memahami protokol ini menjelaskan banyak hal, misalnya mengapa `range(10**9)` tidak menghabiskan memori: ia menghasilkan angka satu per satu saat diminta, bukan menyimpan semuanya.
        """),
        C(
            """
            it = iter([10, 20, 30])
            print(next(it), next(it), next(it))
            try:
                next(it)
            except StopIteration:
                print("habis")

            pasangan = zip([1, 2], ["a", "b"])
            print(list(pasangan))
            print(list(pasangan))
            print(sum(range(10**6)))
            """,
            """
            10 20 30
            habis
            [(1, 'a'), (2, 'b')]
            []
            499999500000
            """,
            """
            Iterator sekali pakai dan menimbulkan `StopIteration` saat habis. `zip` yang sudah ditelusuri menjadi kosong pada penelusuran kedua.
            """,
            filename="iterator_dasar.py",
        ),
        T("""
        ## Generator dengan yield

        **Generator** adalah cara mudah membuat iterator. Fungsi biasa yang memakai `yield` alih-alih `return` otomatis menjadi fungsi generator. Setiap kali `yield` dijalankan, fungsi menghasilkan satu nilai lalu berhenti sementara dengan seluruh keadaannya tersimpan. Pemanggilan berikutnya melanjutkan tepat setelah `yield` itu.

        Keunggulan utamanya adalah **evaluasi malas**: nilai dihitung hanya saat diminta. Generator dapat merepresentasikan barisan yang sangat panjang atau bahkan tak terbatas tanpa menyimpannya di memori. Ia cocok untuk membaca file besar baris demi baris atau memproses aliran data.

        Karena generator adalah iterator, ia sekali pakai. Untuk memakainya lagi kamu harus memanggil fungsi generator itu sekali lagi agar mendapat generator baru.
        """),
        C(
            """
            def hitung_mundur(n):
                while n > 0:
                    yield n
                    n -= 1

            g = hitung_mundur(3)
            print(next(g), next(g))
            print(list(g))
            print(list(g))

            def fibonacci():
                a, b = 0, 1
                while True:
                    yield a
                    a, b = b, a + b

            f = fibonacci()
            print([next(f) for _ in range(10)])
            """,
            """
            3 2
            [1]
            []
            [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
            """,
            """
            Generator melanjutkan dari titik terakhir dan sekali pakai. Generator Fibonacci tak terbatas aman karena nilai dihitung sesuai permintaan.
            """,
            filename="generator_yield.py",
        ),
        K(
            "tip",
            """
            Ekspresi generator ditulis seperti list comprehension tetapi dengan kurung biasa: `(x * x for x in data)`. Hasilnya generator, bukan list, sehingga hemat memori.
            """,
            title="Ekspresi generator",
        ),
        T("""
        ## Ekspresi generator dan penghematan memori

        Ekspresi generator memakai sintaks comprehension dengan kurung biasa dan menghasilkan generator. `sum(x * x for x in range(10**6))` menjumlahkan sejuta kuadrat tanpa pernah membuat list sejuta elemen. Saat generator menjadi satu-satunya argumen fungsi, kurung ekstra boleh dihilangkan seperti pada contoh itu.

        Untuk melihat perbedaannya, bandingkan ukuran objek: list sejuta elemen memakan megabyte memori, sedangkan generator yang setara hanya beberapa ratus byte. Di komputer sungguhan selisihnya bisa diukur dengan `sys.getsizeof`. Tentu generator tidak mendukung indeks atau `len`, dan hanya dapat ditelusuri sekali.

        Aturan praktis: bila hasil hanya akan ditelusuri sekali, misalnya untuk dijumlahkan, dicari maksimumnya, atau diteruskan ke langkah lain, pakai ekspresi generator. Bila perlu diakses acak atau berulang, pakai list.
        """),
        C(
            """
            besar_list = [x * x for x in range(100000)]
            besar_gen = (x * x for x in range(100000))
            print(sum(besar_list) == sum(besar_gen))
            print(type(besar_gen).__name__, type(besar_list).__name__)
            g = (x for x in [1, 2, 3])
            print(len(list(g)), len(list(g)))
            print(max(len(k) for k in ["a", "bbb", "cc"]))
            print(any(x > 99998 for x in range(100000)))
            """,
            """
            True
            generator list
            3 0
            3
            True
            """,
            """
            Generator memberi jumlah yang sama dengan list tanpa menyimpan semua elemen. Ia habis setelah satu kali telusur sehingga telusur kedua kosong.
            """,
            filename="ekspresi_generator.py",
        ),
        T("""
        ## Pipeline generator dan itertools

        Generator dapat dirangkai menjadi pipeline: satu generator membaca baris, berikutnya menyaring, berikutnya mengubah. Tiap nilai mengalir melalui seluruh rantai satu per satu sehingga data besar bisa diproses dengan memori konstan. Pola ini dipakai luas dalam pemrosesan log dan data aliran.

        Modul `itertools` di pustaka standar menyediakan banyak alat untuk iterator, seperti `islice` untuk mengambil sebagian dari iterator tak terbatas, `chain` untuk menyambung, `count` untuk menghitung tanpa batas, dan `groupby` untuk mengelompokkan elemen berurutan. `islice(fibonacci(), 10)` mengambil sepuluh nilai pertama tanpa menghabiskan generator tak terbatas.

        Menguasai generator memberi kamu landasan untuk memahami cara pustaka seperti pandas membaca file besar dalam potongan dan cara kerangka pembelajaran mesin memasok data ke model sepotong demi sepotong.
        """),
        C(
            """
            from itertools import islice, chain, count

            def baca(teks):
                for baris in teks.splitlines():
                    yield baris

            def tanpa_kosong(baris_iter):
                for b in baris_iter:
                    if b.strip():
                        yield b

            def huruf_besar(baris_iter):
                for b in baris_iter:
                    yield b.upper()

            data = "satu\\n\\ndua\\n  \\ntiga"
            print(list(huruf_besar(tanpa_kosong(baca(data)))))
            print(list(islice(count(5), 4)))
            print(list(chain([1, 2], (3,), "ab")))
            """,
            """
            ['SATU', 'DUA', 'TIGA']
            [5, 6, 7, 8]
            [1, 2, 3, 'a', 'b']
            """,
            """
            Tiga generator dirangkai sehingga tiap baris diproses satu per satu. `islice` dan `count` mengambil bagian dari barisan tak terbatas.
            """,
            filename="pipeline_generator.py",
        ),
        T("""
        ## Kapan generator tidak cocok

        Generator tidak cocok bila kamu perlu menelusuri data berkali-kali, mengakses elemen secara acak, atau mengetahui jumlah elemen di muka. Dalam kasus itu, simpan hasil dalam list. Generator juga lebih sulit di-debug karena nilainya tidak terlihat sampai diminta. Saat ragu, ubah sementara ke list dengan `list(generator)` untuk memeriksa isinya, tetapi hanya pada data kecil.

        Ingat pula bahwa generator menyimpan keadaan di antara pemanggilan, sehingga fungsi generator yang mengubah variabel luar dapat menimbulkan perilaku tak terduga. Jaga agar generator bersifat murni: hasilnya hanya bergantung pada masukannya.

        Terakhir, ingat bahwa menutup generator lebih awal tidak berbahaya. Bila kamu berhenti menelusurinya di tengah jalan, Python membersihkan sumber dayanya secara otomatis saat objek tidak lagi dipakai. Karena itu kamu boleh mengambil beberapa nilai pertama saja dari generator yang panjang atau tak terbatas tanpa khawatir.
        """),
        E(
            "A1-05-3-ex1",
            "mudah",
            """
            Tulis fungsi generator `genap_sampai(n)` yang menghasilkan bilangan genap dari 0 sampai `n` termasuk.
            """,
            """
            def genap_sampai(n):
                # TODO: implementasikan
                pass
            """,
            """
            assert list(genap_sampai(6)) == [0, 2, 4, 6]
            assert list(genap_sampai(0)) == [0]
            assert list(genap_sampai(-1)) == []
            assert list(genap_sampai(5)) == [0, 2, 4]
            """,
            "Gunakan yield di dalam perulangan.",
            """
            def genap_sampai(n):
                i = 0
                while i <= n:
                    yield i
                    i += 2
            """,
        ),
        E(
            "A1-05-3-ex2",
            "mudah",
            """
            Tulis fungsi `jumlah_kuadrat(n)` yang mengembalikan jumlah kuadrat 1 sampai `n` memakai ekspresi generator.
            """,
            """
            def jumlah_kuadrat(n):
                # TODO: implementasikan
                pass
            """,
            """
            assert jumlah_kuadrat(3) == 14
            assert jumlah_kuadrat(0) == 0
            assert jumlah_kuadrat(10) == 385
            """,
            "Pakai sum dengan ekspresi generator.",
            """
            def jumlah_kuadrat(n):
                return sum(x * x for x in range(1, n + 1))
            """,
        ),
        E(
            "A1-05-3-ex3",
            "sedang",
            """
            Tulis fungsi generator `jendela(daftar, k)` yang menghasilkan list berisi `k` elemen berurutan (jendela geser) dari `daftar`. Bila `k` lebih besar dari panjang daftar tidak ada yang dihasilkan.
            """,
            """
            def jendela(daftar, k):
                # TODO: implementasikan
                pass
            """,
            """
            assert list(jendela([1, 2, 3, 4], 2)) == [[1, 2], [2, 3], [3, 4]]
            assert list(jendela([1, 2, 3], 3)) == [[1, 2, 3]]
            assert list(jendela([1, 2], 3)) == []
            assert list(jendela([], 1)) == []
            """,
            "Telusuri indeks awal dari 0 sampai len(daftar) - k.",
            """
            def jendela(daftar, k):
                for i in range(len(daftar) - k + 1):
                    yield daftar[i:i + k]
            """,
        ),
        E(
            "A1-05-3-ex4",
            "menantang",
            """
            Tulis fungsi generator `prima()` yang menghasilkan bilangan prima tak terbatas (2, 3, 5, 7, ...). Lalu tulis `n_prima_pertama(n)` yang mengembalikan list `n` prima pertama memakai `itertools.islice`.
            """,
            """
            from itertools import islice

            def prima():
                # TODO: implementasikan
                pass

            def n_prima_pertama(n):
                # TODO: implementasikan
                pass
            """,
            """
            assert n_prima_pertama(5) == [2, 3, 5, 7, 11]
            assert n_prima_pertama(0) == []
            assert n_prima_pertama(10)[-1] == 29
            g = prima()
            assert next(g) == 2 and next(g) == 3
            """,
            "Uji tiap bilangan dengan pembagi yang sudah ditemukan lalu yield bila prima.",
            """
            from itertools import islice

            def prima():
                ditemukan = []
                n = 2
                while True:
                    if all(n % p != 0 for p in ditemukan if p * p <= n):
                        ditemukan.append(n)
                        yield n
                    n += 1

            def n_prima_pertama(n):
                return list(islice(prima(), n))
            """,
        ),
    ],
    [
        M("Menelusuri generator dua kali.", "Buat generator baru atau simpan hasil ke list bila perlu dipakai ulang."),
        M("Memakai return di tempat yang seharusnya yield.", "yield menghasilkan nilai satu per satu, return mengakhiri fungsi."),
        M("Memanggil len atau indeks pada generator.", "Ubah ke list dulu bila butuh akses acak."),
    ],
    [
        Q("Apa yang membuat sebuah fungsi menjadi generator?", ["Memakai lambda", "Memakai yield", "Memakai return", "Memakai global"], 1, "Kata kunci yield membuat fungsi generator.", hint="Menghasilkan nilai bertahap."),
        Q("Apa keunggulan utama generator?", ["Lebih mudah ditulis", "Evaluasi malas dan hemat memori", "Bisa diindeks", "Selalu lebih cepat"], 1, "Nilai dihitung saat diminta tanpa menyimpan semuanya.", hint="Pikirkan data sangat besar."),
        Q("Apa yang terjadi saat generator habis lalu next dipanggil?", ["None", "StopIteration", "0", "Mulai ulang"], 1, "Habisnya iterator ditandai StopIteration.", hint="Itu cara for tahu kapan berhenti."),
        Q("Cara menulis ekspresi generator?", ["[x for x in a]", "(x for x in a)", "{x for x in a}", "<x for x in a>"], 1, "Kurung biasa menghasilkan generator.", hint="Beda dari list comprehension."),
        Q("Fungsi itertools untuk mengambil sebagian iterator?", ["chain", "islice", "count", "repeat"], 1, "islice mengiris iterator.", hint="Mirip slicing list."),
    ],
    [
        "for bekerja lewat iter dan next hingga StopIteration.",
        "Generator memakai yield, malas, dan sekali pakai.",
        "Ekspresi generator hemat memori untuk hasil yang ditelusuri sekali.",
        "Generator dapat dirangkai menjadi pipeline dan itertools membantu.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa kode dan contoh singkat yang cukup jelas dalam teks dan latihan.", "brief": []}

write_module(
    "A1",
    5,
    "Comprehension dan generator",
    105,
    [
        "Menulis list, dictionary, dan set comprehension dengan filter",
        "Memahami iterator dan membuat generator dengan yield",
        "Memakai evaluasi malas untuk menghemat memori",
    ],
    [l1, l2, l3],
    video,
    REF,
)
