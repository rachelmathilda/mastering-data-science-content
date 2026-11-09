import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

l1 = lesson(
    "A1-02-1",
    "Percabangan: if, elif, else, dan match",
    35,
    [
        "Menulis percabangan if, elif, dan else dengan indentasi yang benar",
        "Menyusun kondisi majemuk dan memakai ekspresi kondisional satu baris",
        "Memanfaatkan truthiness untuk memeriksa nilai kosong",
        "Memakai match untuk memilih berdasarkan pola nilai",
    ],
    [
        T("""
        ## Program yang mengambil keputusan

        Program yang hanya berjalan lurus dari atas ke bawah sangat terbatas. Data nyata menuntut keputusan: jika nilai kosong maka lewati, jika suhu terlalu tinggi maka beri peringatan, jika akurasi di bawah target maka latih ulang. Pernyataan `if` adalah cara Python mengekspresikan keputusan tersebut.

        Bentuknya sederhana. Kata `if` diikuti sebuah kondisi, lalu tanda titik dua, lalu blok kode yang menjorok ke dalam. Blok itu hanya berjalan bila kondisinya benar. Di Python, indentasi bukan sekadar gaya penulisan. Indentasi adalah sintaks yang menentukan batas blok. Standar komunitas memakai empat spasi, dan kamu sebaiknya konsisten karena mencampur tab dan spasi menghasilkan `IndentationError`.

        Kondisi di `if` bisa berupa ekspresi apa pun yang menghasilkan nilai. Python akan menafsirkannya sebagai benar atau salah menurut aturan truthiness yang sudah kamu pelajari di modul sebelumnya.
        """),
        T("""
        ## if, elif, dan else

        Ketika ada lebih dari dua kemungkinan, rangkai `elif`, singkatan dari else if. Python memeriksa kondisi dari atas ke bawah dan menjalankan blok pertama yang kondisinya benar, lalu melewati sisanya. Blok `else` di akhir menangkap semua kasus yang tidak cocok dengan kondisi sebelumnya.

        Urutan kondisi sangat penting. Misalkan kamu mengelompokkan nilai ujian: jika nilai di atas 90 maka A, jika di atas 80 maka B. Bila kamu menulis kondisi di atas 80 lebih dulu, nilai 95 akan terjebak di B karena 95 memang lebih dari 80. Selalu susun dari kondisi paling spesifik atau paling ketat ke yang paling longgar.

        Hindari bertingkat terlalu dalam. Bila kamu menulis `if` di dalam `if` di dalam `if`, kodenya sulit dibaca. Gunakan kondisi majemuk dengan `and` dan `or`, atau pecah menjadi fungsi, atau gunakan pola guard: periksa kasus buruk di awal dan segera kembalikan hasil.
        """),
        C(
            """
            def predikat(nilai):
                if nilai >= 90:
                    return "A"
                elif nilai >= 80:
                    return "B"
                elif nilai >= 70:
                    return "C"
                else:
                    return "D"

            for n in [95, 85, 72, 40, 90, 80]:
                print(n, predikat(n))
            """,
            """
            95 A
            85 B
            72 C
            40 D
            90 A
            80 B
            """,
            """
            Kondisi diperiksa dari yang paling ketat. Nilai tepat 90 dan 80 jatuh ke batas atas kelasnya karena memakai `>=`.
            """,
            filename="predikat.py",
        ),
        T("""
        ## Kondisi majemuk dan ekspresi satu baris

        Kondisi bisa digabung memakai `and`, `or`, dan `not`. Contohnya `if umur >= 17 and punya_ktp:`. Ingat short-circuit: bila bagian kiri `and` sudah salah, bagian kanan tidak dievaluasi. Sifat ini berguna untuk mengamankan pemeriksaan, misalnya `if data and data[0] > 0`, yang tidak akan mengakses elemen pertama bila `data` kosong.

        Untuk memilih satu dari dua nilai, Python menyediakan **ekspresi kondisional**: `nilai_a if kondisi else nilai_b`. Bentuk ini ringkas untuk penugasan sederhana seperti `status = "lulus" if skor >= 60 else "remedial"`. Namun jangan dirantai berlebihan, karena ekspresi bersarang cepat menjadi sulit dibaca.

        Perbedaan penting dengan pernyataan `if` biasa: ekspresi kondisional menghasilkan nilai, sedangkan pernyataan `if` menjalankan blok. Pilih ekspresi hanya ketika kedua cabang berupa nilai singkat.
        """),
        K(
            "tip",
            """
            Gunakan pola guard untuk menghindari penumpukan indentasi. Tangani kasus tidak valid di awal fungsi dengan `return` atau `raise`, lalu biarkan jalur utama berada di tingkat indentasi paling luar.
            """,
            title="Pola guard",
        ),
        C(
            """
            def kategori_bmi(berat, tinggi_m):
                if tinggi_m <= 0 or berat <= 0:
                    return "tidak valid"
                bmi = berat / tinggi_m ** 2
                if bmi < 18.5:
                    return "kurang"
                if bmi < 25:
                    return "normal"
                return "lebih"

            print(kategori_bmi(50, 1.7), kategori_bmi(65, 1.7), kategori_bmi(90, 1.7), kategori_bmi(0, 1.7))
            data = []
            print(bool(data and data[0] > 0))
            skor = 72
            print("lulus" if skor >= 60 else "remedial")
            """,
            """
            kurang normal lebih tidak valid
            False
            lulus
            """,
            """
            Pola guard menangani input tidak valid di awal, sehingga jalur utama tidak bersarang. Pemeriksaan `data and data[0] > 0` aman untuk daftar kosong.
            """,
            filename="guard_bmi.py",
        ),
        T("""
        ## Kesalahan umum pada kondisi

        Ada beberapa jebakan yang sering menjerat pemula. Pertama, membandingkan nilai boolean dengan `== True`, padahal cukup menulis `if aktif:`. Kedua, memakai `is` untuk membandingkan angka atau teks, padahal `is` memeriksa identitas objek dan hanya tepat untuk `None`. Ketiga, lupa bahwa `if x == 1 or 2` selalu benar karena angka 2 bernilai benar sendiri. Tulislah `if x == 1 or x == 2`, atau lebih ringkas `if x in (1, 2)`.

        Operator `in` sangat berguna untuk memeriksa keanggotaan pada list, tuple, himpunan, dan string. Pemeriksaan di himpunan jauh lebih cepat daripada di list untuk data besar, sebuah hal yang akan kamu temui lagi di modul struktur data.
        """),
        T("""
        ## match untuk memilih berdasarkan pola

        Sejak Python 3.10 tersedia pernyataan `match` yang mirip switch di bahasa lain tetapi lebih kuat. Kamu mencocokkan sebuah nilai dengan beberapa pola `case`, dan blok pertama yang cocok dijalankan. Tanda garis bawah `_` adalah pola penangkap semua sisanya.

        Pola bisa berupa nilai literal, beberapa nilai digabung dengan garis tegak (`"a" | "b"`), atau struktur seperti tuple dan list. Ini nyaman ketika kamu memilih tindakan berdasarkan perintah teks atau berdasarkan bentuk data.

        Meski begitu, `if` dan `elif` tetap pilihan yang tepat untuk rentang numerik dan kondisi majemuk. Gunakan `match` ketika kamu membandingkan satu nilai dengan daftar kemungkinan diskret. Pyodide yang dipakai di app ini berbasis Python 3.12, jadi `match` tersedia.
        """),
        C(
            """
            def perintah(teks):
                match teks.split():
                    case ["mulai"]:
                        return "memulai"
                    case ["berhenti" | "stop"]:
                        return "berhenti"
                    case ["tambah", angka]:
                        return "tambah " + angka
                    case []:
                        return "kosong"
                    case _:
                        return "tidak dikenal"

            for t in ["mulai", "stop", "tambah 5", "", "loncat tinggi"]:
                print(repr(t), "->", perintah(t))
            """,
            """
            'mulai' -> memulai
            'stop' -> berhenti
            'tambah 5' -> tambah 5
            '' -> kosong
            'loncat tinggi' -> tidak dikenal
            """,
            """
            Pola list mencocokkan jumlah dan isi elemen. Pola `_` menangkap semua perintah lain.
            """,
            filename="match_perintah.py",
        ),
        E(
            "A1-02-1-ex1",
            "mudah",
            """
            Tulis fungsi `tanda(n)` yang mengembalikan `"positif"`, `"negatif"`, atau `"nol"` sesuai nilai `n`.
            """,
            """
            def tanda(n):
                # TODO: implementasikan
                pass
            """,
            """
            assert tanda(5) == "positif"
            assert tanda(-2) == "negatif"
            assert tanda(0) == "nol"
            assert tanda(0.1) == "positif"
            """,
            "Gunakan if, elif, else.",
            """
            def tanda(n):
                if n > 0:
                    return "positif"
                elif n < 0:
                    return "negatif"
                return "nol"
            """,
        ),
        E(
            "A1-02-1-ex2",
            "mudah",
            """
            Tulis fungsi `predikat(nilai)` yang mengembalikan "A" untuk nilai 90 ke atas, "B" untuk 80 sampai 89, "C" untuk 70 sampai 79, dan "D" selainnya.
            """,
            """
            def predikat(nilai):
                # TODO: implementasikan
                pass
            """,
            """
            assert predikat(95) == "A"
            assert predikat(90) == "A"
            assert predikat(85) == "B"
            assert predikat(70) == "C"
            assert predikat(69) == "D"
            """,
            "Periksa dari batas tertinggi ke terendah.",
            """
            def predikat(nilai):
                if nilai >= 90:
                    return "A"
                if nilai >= 80:
                    return "B"
                if nilai >= 70:
                    return "C"
                return "D"
            """,
        ),
        E(
            "A1-02-1-ex3",
            "sedang",
            """
            Tulis fungsi `tarif_tiket(umur, hari_libur)` yang mengembalikan harga: anak di bawah 5 tahun gratis (0), umur 5 sampai 12 harga 20000, umur 13 ke atas harga 35000. Bila `hari_libur` benar, tambahkan 10000 kecuali untuk anak gratis. Jika umur negatif naikkan `ValueError`.
            """,
            """
            def tarif_tiket(umur, hari_libur):
                # TODO: implementasikan
                pass
            """,
            """
            assert tarif_tiket(3, True) == 0
            assert tarif_tiket(8, False) == 20000
            assert tarif_tiket(8, True) == 30000
            assert tarif_tiket(20, True) == 45000
            def gagal():
                try:
                    tarif_tiket(-1, False)
                except ValueError:
                    return True
                return False
            assert gagal()
            """,
            "Tangani umur negatif di awal sebagai guard, lalu hitung harga dasar dan tambahan.",
            """
            def tarif_tiket(umur, hari_libur):
                if umur < 0:
                    raise ValueError("umur negatif")
                if umur < 5:
                    return 0
                harga = 20000 if umur <= 12 else 35000
                if hari_libur:
                    harga += 10000
                return harga
            """,
        ),
        E(
            "A1-02-1-ex4",
            "menantang",
            """
            Tulis fungsi `jalankan(teks)` memakai `match`. Perintah `"naik"` mengembalikan `(0, 1)`, `"turun"` mengembalikan `(0, -1)`, `"kiri"` mengembalikan `(-1, 0)`, `"kanan"` mengembalikan `(1, 0)`, dan `"lompat N"` dengan N bilangan bulat mengembalikan `(0, N)`. Perintah lain mengembalikan `None`.
            """,
            """
            def jalankan(teks):
                # TODO: implementasikan
                pass
            """,
            """
            assert jalankan("naik") == (0, 1)
            assert jalankan("turun") == (0, -1)
            assert jalankan("kiri") == (-1, 0)
            assert jalankan("kanan") == (1, 0)
            assert jalankan("lompat 3") == (0, 3)
            assert jalankan("terbang") is None
            assert jalankan("lompat x") is None
            """,
            "Pecah teks dengan split lalu cocokkan list. Untuk lompat, periksa bahwa argumen adalah angka dengan isdigit.",
            """
            def jalankan(teks):
                match teks.split():
                    case ["naik"]:
                        return (0, 1)
                    case ["turun"]:
                        return (0, -1)
                    case ["kiri"]:
                        return (-1, 0)
                    case ["kanan"]:
                        return (1, 0)
                    case ["lompat", n] if n.isdigit():
                        return (0, int(n))
                    case _:
                        return None
            """,
        ),
    ],
    [
        M("Menyusun elif dari kondisi longgar ke ketat.", "Mulai dari kondisi paling ketat agar tidak tertangkap lebih dulu."),
        M("Mencampur tab dan spasi pada indentasi.", "Pakai empat spasi secara konsisten."),
        M("Menumpuk if bersarang terlalu dalam.", "Pakai pola guard atau kondisi majemuk."),
    ],
    [
        Q("Mengapa urutan elif penting?", ["Python memeriksa dari atas dan berhenti di yang pertama benar", "Python memeriksa semua", "Urutan tidak berpengaruh", "Hanya else yang penting"], 0, "Blok pertama yang kondisinya benar dijalankan dan sisanya dilewati.", hint="Apa yang terjadi setelah satu kondisi benar?"),
        Q("Hasil dari 'lulus' if 50 >= 60 else 'remedial'?", ["lulus", "remedial", "True", "Error"], 1, "Kondisi salah sehingga cabang else dipakai.", hint="Evaluasi kondisi 50 >= 60 dulu."),
        Q("Apa fungsi case _ pada match?", ["Menangkap semua pola sisanya", "Menghentikan program", "Membuat variabel", "Mengulang"], 0, "Garis bawah cocok dengan apa pun sehingga menjadi pola default.", hint="Pikirkan peran else."),
        Q("Pernyataan if data and data[0] > 0 aman untuk list kosong karena?", ["Python mengabaikan error", "Short-circuit berhenti saat data kosong", "List kosong bernilai True", "and selalu benar"], 1, "List kosong bernilai salah sehingga bagian kanan tidak dievaluasi.", hint="Ingat short-circuit."),
        Q("Berapa spasi indentasi standar Python?", ["1", "2", "4", "8"], 2, "Konvensi PEP 8 memakai empat spasi.", hint="Ini angka yang paling umum."),
    ],
    [
        "if, elif, else memilih blok pertama yang kondisinya benar.",
        "Pola guard dan ekspresi kondisional mengurangi indentasi.",
        "match cocok untuk memilih dari nilai atau bentuk diskret.",
        "Indentasi adalah sintaks dan harus konsisten.",
    ],
    [],
)

l2 = lesson(
    "A1-02-2",
    "Perulangan: for, while, dan kendalinya",
    35,
    [
        "Menelusuri urutan dengan for dan range",
        "Memakai enumerate dan zip untuk menelusuri beberapa urutan",
        "Menulis while dengan kondisi berhenti yang pasti",
        "Mengendalikan perulangan dengan break, continue, dan else",
    ],
    [
        T("""
        ## for: menelusuri elemen satu per satu

        Perulangan `for` mengambil elemen dari sebuah urutan satu per satu dan menjalankan blok untuk tiap elemen. Urutan itu bisa berupa list, tuple, string, dictionary, atau objek apa pun yang bisa ditelusuri. Berbeda dengan bahasa yang memakai penghitung indeks, Python langsung memberi kamu elemennya: `for nama in daftar_nama:`.

        Untuk mengulang sejumlah kali tertentu, pakai `range`. `range(5)` menghasilkan 0 sampai 4, `range(2, 6)` menghasilkan 2 sampai 5, dan `range(0, 10, 3)` menghasilkan 0, 3, 6, 9. Ingat bahwa batas akhir tidak ikut. Aturan setengah terbuka ini konsisten di seluruh Python, termasuk pemotongan list.

        Kebiasaan buruk yang sering muncul adalah menulis `for i in range(len(daftar))` hanya untuk mengambil elemen. Pola itu jarang dibutuhkan. Telusuri elemennya langsung, dan bila butuh nomor urut pakai `enumerate`.
        """),
        C(
            """
            buah = ["apel", "jeruk", "mangga"]
            for b in buah:
                print(b.upper())
            print(list(range(5)), list(range(2, 6)), list(range(0, 10, 3)), list(range(5, 0, -2)))
            for i, b in enumerate(buah, start=1):
                print(i, b)
            harga = [5000, 7000, 12000]
            for b, h in zip(buah, harga):
                print(f"{b}: {h}")
            """,
            """
            APEL
            JERUK
            MANGGA
            [0, 1, 2, 3, 4] [2, 3, 4, 5] [0, 3, 6, 9] [5, 3, 1]
            1 apel
            2 jeruk
            3 mangga
            apel: 5000
            jeruk: 7000
            mangga: 12000
            """,
            """
            `enumerate` memberi nomor urut dan `zip` menelusuri dua urutan berpasangan. `range` bisa menurun dengan langkah negatif.
            """,
            filename="for_dasar.py",
        ),
        T("""
        ## Menelusuri string dan dictionary

        String juga urutan, jadi `for huruf in "data":` menelusuri huruf demi huruf. Dictionary menelusuri kuncinya secara bawaan. Untuk mendapatkan pasangan kunci dan nilai sekaligus, pakai `.items()`. Untuk nilainya saja, pakai `.values()`.

        Sejak Python 3.7, dictionary mempertahankan urutan penyisipan, sehingga hasil penelusuran dapat diprediksi. Jangan menambah atau menghapus kunci selagi menelusuri dictionary yang sama karena Python akan menimbulkan `RuntimeError`. Bila perlu mengubah, telusuri salinan seperti `list(d.items())`.
        """),
        T("""
        ## Pola akumulator

        Banyak perulangan memiliki pola yang sama: siapkan variabel awal, perbarui di setiap putaran, lalu gunakan hasilnya setelah selesai. Variabel itu disebut **akumulator**. Untuk menjumlahkan, mulai dari nol. Untuk mengalikan, mulai dari satu. Untuk mencari nilai terbesar, mulai dari elemen pertama atau dari nilai yang sangat kecil.

        Python sudah punya fungsi bawaan `sum`, `max`, `min`, dan `len` untuk kasus umum, dan kamu sebaiknya memakainya bila sesuai. Tetapi menulis akumulator sendiri penting karena melatih pola pikir yang sama untuk kasus yang tidak punya fungsi bawaan, seperti menghitung rata-rata bergerak atau menghitung frekuensi kata.

        Dalam data science kamu akan sering menulis perulangan yang menghitung statistik dari kumpulan baris. Pola akumulator adalah dasar dari semuanya, dan nanti kamu akan menggantikannya dengan operasi vektor di NumPy dan pandas.
        """),
        C(
            """
            nilai = [70, 85, 90, 65, 100]
            total = 0
            terbesar = nilai[0]
            for n in nilai:
                total += n
                if n > terbesar:
                    terbesar = n
            print(total, total / len(nilai), terbesar)

            kalimat = "kopi teh kopi susu teh kopi"
            frekuensi = {}
            for kata in kalimat.split():
                frekuensi[kata] = frekuensi.get(kata, 0) + 1
            print(frekuensi)
            """,
            """
            410 82.0 100
            {'kopi': 3, 'teh': 2, 'susu': 1}
            """,
            """
            Akumulator `total` dan `terbesar` diperbarui tiap putaran. Dictionary dipakai sebagai penghitung frekuensi dengan `get` untuk nilai awal nol.
            """,
            filename="akumulator.py",
        ),
        T("""
        ## while: berulang selama kondisi benar

        Perulangan `while` berjalan selama kondisinya benar. Gunakan `while` ketika jumlah putaran tidak diketahui sebelumnya, misalnya membaca input sampai valid atau mengulang optimasi sampai konvergen. Setiap `while` harus punya jalan keluar: sesuatu di dalam blok yang akhirnya membuat kondisi menjadi salah. Bila tidak, program terjebak dalam perulangan tak hingga.

        Pernyataan `break` menghentikan perulangan seketika, sedangkan `continue` melompat ke putaran berikutnya. Python juga punya klausa `else` pada perulangan yang berjalan hanya bila perulangan selesai normal tanpa `break`. Pola ini cocok untuk pencarian: `else` berarti tidak ketemu.

        Contoh nyata dalam machine learning adalah early stopping: latih model sampai galat validasi tidak membaik selama beberapa putaran berturut-turut. Perulangan `while` dengan penghitung kesabaran adalah bentuk paling alami untuk itu.
        """),
        C(
            """
            n = 27
            langkah = 0
            while n != 1:
                n = n // 2 if n % 2 == 0 else 3 * n + 1
                langkah += 1
            print("collatz 27:", langkah)

            for angka in range(2, 20):
                if angka % 2 == 0:
                    continue
                if angka > 11:
                    break
                print(angka, end=" ")
            print()

            for x in [3, 5, 7]:
                if x % 2 == 0:
                    print("ada genap")
                    break
            else:
                print("tidak ada genap")
            """,
            """
            collatz 27: 111
            3 5 7 9 11
            tidak ada genap
            """,
            """
            `while` berjalan sampai kondisi salah. `continue` melewati angka genap dan `break` menghentikan setelah 11. Klausa `else` pada `for` aktif karena tidak ada `break`.
            """,
            filename="while_break.py",
        ),
        T("""
        ## Memilih for atau while

        Aturan praktisnya sederhana. Bila kamu tahu apa yang ditelusuri, pakai `for`. Bila kamu menunggu sebuah kondisi tercapai tanpa tahu berapa lama, pakai `while`. Hampir semua perulangan `for` bisa ditulis sebagai `while`, tetapi bentuk `for` lebih aman karena tidak punya risiko lupa memperbarui penghitung, dan pembaca kodemu langsung tahu bahwa jumlah putarannya terbatas.

        Satu pola yang berguna adalah `while True` dengan `break` di dalam saat syarat berhenti terpenuhi. Pola ini menghindari penulisan ganda untuk membaca input pertama kali dan seterusnya. Pastikan selalu ada `break` yang dapat dicapai, atau program akan berjalan selamanya.

        Dalam eksperimen machine learning, pola ini muncul ketika kamu melatih model sampai metrik berhenti membaik. Tambahkan juga batas maksimum putaran sebagai pengaman, sehingga eksperimen tidak berjalan tanpa akhir bila metriknya tidak pernah stabil.
        """),
        K(
            "warning",
            """
            Jangan mengubah list yang sedang kamu telusuri dengan menambah atau menghapus elemennya. Hasilnya bisa melewatkan elemen. Buat salinan atau bangun list baru.
            """,
            title="Hati-hati memodifikasi saat menelusuri",
        ),
        E(
            "A1-02-2-ex1",
            "mudah",
            """
            Tulis fungsi `jumlah_kuadrat(n)` yang mengembalikan jumlah kuadrat bilangan 1 sampai `n`.
            """,
            """
            def jumlah_kuadrat(n):
                # TODO: implementasikan
                pass
            """,
            """
            assert jumlah_kuadrat(3) == 14
            assert jumlah_kuadrat(1) == 1
            assert jumlah_kuadrat(0) == 0
            assert jumlah_kuadrat(10) == 385
            """,
            "Gunakan range(1, n + 1) dan sebuah akumulator.",
            """
            def jumlah_kuadrat(n):
                total = 0
                for i in range(1, n + 1):
                    total += i * i
                return total
            """,
        ),
        E(
            "A1-02-2-ex2",
            "mudah",
            """
            Tulis fungsi `frekuensi_kata(kalimat)` yang mengembalikan dictionary jumlah kemunculan tiap kata, dengan kata dibuat huruf kecil.
            """,
            """
            def frekuensi_kata(kalimat):
                # TODO: implementasikan
                pass
            """,
            """
            assert frekuensi_kata("kopi teh kopi") == {"kopi": 2, "teh": 1}
            assert frekuensi_kata("A a A") == {"a": 3}
            assert frekuensi_kata("") == {}
            """,
            "Pecah dengan split dan pakai get untuk nilai awal.",
            """
            def frekuensi_kata(kalimat):
                hasil = {}
                for k in kalimat.lower().split():
                    hasil[k] = hasil.get(k, 0) + 1
                return hasil
            """,
        ),
        E(
            "A1-02-2-ex3",
            "sedang",
            """
            Tulis fungsi `langkah_collatz(n)` yang mengembalikan banyak langkah untuk mencapai 1: bila genap bagi dua, bila ganjil kalikan tiga tambah satu. Jika `n` kurang dari 1 naikkan `ValueError`.
            """,
            """
            def langkah_collatz(n):
                # TODO: implementasikan
                pass
            """,
            """
            assert langkah_collatz(1) == 0
            assert langkah_collatz(6) == 8
            assert langkah_collatz(27) == 111
            def gagal(x):
                try:
                    langkah_collatz(x)
                except ValueError:
                    return True
                return False
            assert gagal(0)
            assert gagal(-5)
            """,
            "Pakai while n != 1 dengan penghitung langkah.",
            """
            def langkah_collatz(n):
                if n < 1:
                    raise ValueError("n harus positif")
                langkah = 0
                while n != 1:
                    n = n // 2 if n % 2 == 0 else 3 * n + 1
                    langkah += 1
                return langkah
            """,
        ),
        E(
            "A1-02-2-ex4",
            "menantang",
            """
            Tulis fungsi `early_stop(loss, kesabaran)` yang menerima list loss validasi dan mengembalikan indeks putaran terbaik (loss terendah pertama). Perulangan berhenti bila selama `kesabaran` putaran berturut-turut tidak ada loss yang lebih rendah dari terbaik.
            """,
            """
            def early_stop(loss, kesabaran):
                # TODO: implementasikan
                pass
            """,
            """
            assert early_stop([0.9, 0.7, 0.6, 0.65, 0.66, 0.4], 2) == 2
            assert early_stop([0.9, 0.7, 0.6, 0.65, 0.66, 0.4], 3) == 5
            assert early_stop([0.5, 0.6, 0.7], 1) == 0
            assert early_stop([0.3], 5) == 0
            assert early_stop([0.9, 0.8, 0.7], 2) == 2
            """,
            "Simpan indeks dan nilai terbaik serta penghitung tanpa perbaikan. Reset penghitung saat ada loss yang lebih rendah.",
            """
            def early_stop(loss, kesabaran):
                terbaik = 0
                tanpa_perbaikan = 0
                for i in range(1, len(loss)):
                    if loss[i] < loss[terbaik]:
                        terbaik = i
                        tanpa_perbaikan = 0
                    else:
                        tanpa_perbaikan += 1
                        if tanpa_perbaikan >= kesabaran:
                            break
                return terbaik
            """,
        ),
    ],
    [
        M("Memakai range(len(x)) hanya untuk mengambil elemen.", "Telusuri elemennya langsung atau pakai enumerate bila butuh nomor urut."),
        M("Lupa memperbarui variabel kondisi di dalam while.", "Pastikan ada langkah yang akhirnya membuat kondisi salah."),
        M("Menambah atau menghapus elemen list saat menelusurinya.", "Buat list baru atau telusuri salinan."),
    ],
    [
        Q("Hasil list(range(2, 6))?", ["[2, 3, 4, 5, 6]", "[2, 3, 4, 5]", "[3, 4, 5]", "[2, 6]"], 1, "Batas akhir tidak ikut.", hint="Setengah terbuka."),
        Q("Apa yang dilakukan continue?", ["Menghentikan perulangan", "Melompat ke putaran berikutnya", "Mengulang dari awal program", "Keluar dari fungsi"], 1, "continue melewati sisa blok dan lanjut ke elemen berikutnya.", hint="Bedakan dengan break."),
        Q("Kapan else pada for dijalankan?", ["Selalu", "Saat perulangan selesai tanpa break", "Saat ada break", "Tidak pernah"], 1, "else pada perulangan berjalan bila tidak ada break.", hint="Cocok untuk pencarian tidak ketemu."),
        Q("Fungsi enumerate memberi?", ["Elemen saja", "Pasangan nomor dan elemen", "Hanya indeks", "Salinan list"], 1, "enumerate menghasilkan pasangan nomor urut dan elemen.", hint="Bandingkan dengan zip."),
        Q("Risiko utama while tanpa pembaruan kondisi?", ["Error sintaks", "Perulangan tak hingga", "Hasil salah tipe", "Tidak ada"], 1, "Kondisi tidak pernah salah sehingga program tidak berhenti.", hint="Apa yang membuat kondisi berubah?"),
    ],
    [
        "for menelusuri elemen langsung dan range menghasilkan angka berurutan.",
        "Pola akumulator menyiapkan nilai awal dan memperbaruinya tiap putaran.",
        "while cocok bila jumlah putaran tidak pasti dan harus punya jalan keluar.",
        "break, continue, dan else mengendalikan jalannya perulangan.",
    ],
    [],
)

l3 = lesson(
    "A1-02-3",
    "Perulangan bersarang dan pola umum",
    35,
    [
        "Menulis perulangan bersarang untuk data dua dimensi",
        "Menghitung total, filter, dan transformasi dengan perulangan",
        "Mengenali kompleksitas waktu sederhana dari kedalaman perulangan",
        "Menerapkan pola pencarian dan penyaringan pada data tabel kecil",
    ],
    [
        T("""
        ## Perulangan di dalam perulangan

        Data tabel memiliki baris dan kolom, dan menelusurinya butuh dua perulangan: satu untuk baris dan satu untuk kolom di dalamnya. Perulangan bersarang bekerja dengan aturan sederhana: untuk setiap putaran luar, perulangan dalam berjalan penuh dari awal sampai selesai. Jika luar berputar 3 kali dan dalam 4 kali, blok terdalam berjalan 12 kali.

        Representasi tabel yang paling sederhana di Python adalah list berisi list. Setiap list dalam adalah satu baris. Dengan `tabel[i][j]` kamu mengambil baris ke-i dan kolom ke-j. Pola ini adalah cikal bakal array dua dimensi di NumPy dan DataFrame di pandas, yang nanti akan melakukan hal sama dengan jauh lebih cepat.

        Karena indeks Python mulai dari nol, baris pertama adalah `tabel[0]`. Kesalahan satu-per-satu (off-by-one) adalah bug paling sering pada perulangan bersarang, jadi uji kasus tepi: tabel kosong, satu baris, dan satu kolom.
        """),
        C(
            """
            tabel = [
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 9],
            ]
            total_baris = []
            for baris in tabel:
                s = 0
                for sel in baris:
                    s += sel
                total_baris.append(s)
            print(total_baris)

            diagonal = 0
            for i in range(len(tabel)):
                diagonal += tabel[i][i]
            print(diagonal)

            transpos = []
            for j in range(len(tabel[0])):
                kolom = []
                for i in range(len(tabel)):
                    kolom.append(tabel[i][j])
                transpos.append(kolom)
            print(transpos)
            """,
            """
            [6, 15, 24]
            15
            [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
            """,
            """
            Jumlah per baris memakai dua perulangan, diagonal memakai satu indeks, dan transpos menukar peran baris dan kolom.
            """,
            filename="tabel_bersarang.py",
        ),
        T("""
        ## Memetakan indeks dengan benar

        Saat menelusuri tabel, jelaskan pada dirimu sendiri apa arti tiap indeks. Beri nama `baris` dan `kolom` alih-alih `i` dan `j` bila bentuk datanya tidak jelas. Nama yang bermakna mengurangi kekeliruan tertukar indeks, bug yang sulit ditemukan karena kode tetap berjalan tanpa error tetapi menghasilkan angka salah.

        Jika semua baris panjangnya sama, tabel disebut persegi panjang. Jika panjangnya berbeda, tabel disebut bergerigi dan kamu harus memeriksa panjang tiap baris. Dalam data nyata, baris bergerigi sering muncul karena nilai hilang, jadi jangan berasumsi semua baris sama panjang.
        """),
        T("""
        ## Menyaring dan mengubah data

        Dua tugas yang sangat sering muncul adalah menyaring (memilih elemen yang memenuhi syarat) dan mengubah (menghasilkan nilai baru dari tiap elemen). Dengan perulangan biasa, kamu membuat list kosong, menelusuri data, dan menambahkan ke list hasil dengan `append`.

        Penyaringan memakai `if` di dalam perulangan, sedangkan transformasi menambahkan nilai yang sudah diolah. Keduanya bisa digabung dalam satu perulangan. Di modul selanjutnya kamu akan mempelajari comprehension, yang menyingkat pola ini menjadi satu baris yang ekspresif, tetapi pemahaman bentuk perulangan eksplisitnya tetap fondasi.

        Waspadai biaya perulangan bersarang. Dua perulangan yang masing-masing menelusuri n elemen membuat n kali n operasi. Untuk seribu elemen itu sejuta operasi, masih cepat. Untuk sejuta elemen itu satu triliun operasi dan program tidak akan selesai. Mengenali pertumbuhan seperti ini sejak dini mencegah kode yang tidak skalabel.
        """),
        C(
            """
            data = [
                {"nama": "Ani", "kota": "Depok", "skor": 82},
                {"nama": "Budi", "kota": "Jakarta", "skor": 55},
                {"nama": "Citra", "kota": "Depok", "skor": 91},
                {"nama": "Dedi", "kota": "Bogor", "skor": 67},
            ]
            lulus = []
            for r in data:
                if r["skor"] >= 60:
                    lulus.append(r["nama"])
            print(lulus)

            per_kota = {}
            for r in data:
                per_kota.setdefault(r["kota"], []).append(r["skor"])
            rata = {}
            for kota, skors in per_kota.items():
                rata[kota] = sum(skors) / len(skors)
            print(rata)
            """,
            """
            ['Ani', 'Citra', 'Dedi']
            {'Depok': 86.5, 'Jakarta': 55.0, 'Bogor': 67.0}
            """,
            """
            Penyaringan memakai kondisi di dalam perulangan. Pengelompokan per kota memakai `setdefault` lalu rata-rata dihitung per kelompok.
            """,
            filename="saring_kelompok.py",
        ),
        T("""
        ## Menguji perulangan dengan contoh kecil

        Cara terbaik memastikan perulangan bersarang benar adalah menjalankannya dengan tangan pada contoh kecil. Tulis tabel tiga kali tiga, telusuri nilai indeks pada kertas, lalu bandingkan dengan keluaran program. Setelah cocok, uji kasus tepi: tabel kosong, satu baris, satu kolom, dan baris bergerigi.

        Kebiasaan ini menghemat waktu debugging berjam-jam kelak. Dalam proyek data science, pengujian kecil seperti ini juga mencegah kesalahan yang diam-diam merusak hasil analisis, karena angka yang salah sering tampak masuk akal.

        Biasakan menulis beberapa pernyataan assert sederhana setelah fungsi selesai ditulis. Assert yang memeriksa hasil pada contoh kecil bertindak sebagai jaring pengaman setiap kali kamu mengubah kode di kemudian hari.
        """),
        T("""
        ## Pola pencarian dan pasangan

        Pola umum lainnya adalah mencari pasangan elemen yang memenuhi syarat, misalnya dua bilangan yang berjumlah target. Cara langsung memakai dua perulangan: untuk tiap elemen i, periksa semua elemen j setelahnya. Ini berjalan dalam waktu kuadrat. Nanti kamu akan belajar bahwa memakai himpunan atau dictionary dapat menurunkannya menjadi linear.

        Saat menulis perulangan bersarang untuk pasangan, mulai indeks dalam dari `i + 1` supaya setiap pasangan hanya dihitung sekali dan elemen tidak dipasangkan dengan dirinya sendiri. Kesalahan memulai dari nol menghasilkan pasangan ganda dan pasangan dengan diri sendiri.

        Selalu uji dengan contoh kecil yang bisa kamu hitung tangan. Perulangan bersarang sulit dilacak di kepala, jadi cetak nilai indeks pada contoh kecil untuk memastikan urutannya sesuai harapan sebelum dijalankan pada data besar.
        """),
        C(
            """
            def pasangan_jumlah(angka, target):
                hasil = []
                for i in range(len(angka)):
                    for j in range(i + 1, len(angka)):
                        if angka[i] + angka[j] == target:
                            hasil.append((angka[i], angka[j]))
                return hasil

            print(pasangan_jumlah([1, 2, 3, 4, 5, 6], 7))
            print(pasangan_jumlah([2, 2, 2], 4))
            jumlah_operasi = 0
            n = 100
            for i in range(n):
                for j in range(n):
                    jumlah_operasi += 1
            print(jumlah_operasi)
            """,
            """
            [(1, 6), (2, 5), (3, 4)]
            [(2, 2), (2, 2), (2, 2)]
            10000
            """,
            """
            Indeks dalam dimulai dari `i + 1` sehingga tiap pasangan dihitung sekali. Dua perulangan 100 kali menghasilkan 10.000 operasi.
            """,
            filename="pasangan.py",
        ),
        E(
            "A1-02-3-ex1",
            "mudah",
            """
            Tulis fungsi `jumlah_tabel(tabel)` yang mengembalikan jumlah semua sel pada list berisi list angka.
            """,
            """
            def jumlah_tabel(tabel):
                # TODO: implementasikan
                pass
            """,
            """
            assert jumlah_tabel([[1, 2], [3, 4]]) == 10
            assert jumlah_tabel([]) == 0
            assert jumlah_tabel([[5]]) == 5
            assert jumlah_tabel([[1, 2, 3], []]) == 6
            """,
            "Dua perulangan bersarang dan satu akumulator.",
            """
            def jumlah_tabel(tabel):
                total = 0
                for baris in tabel:
                    for sel in baris:
                        total += sel
                return total
            """,
        ),
        E(
            "A1-02-3-ex2",
            "mudah",
            """
            Tulis fungsi `saring_lulus(data, batas)` yang menerima list dictionary dengan kunci `nama` dan `skor` dan mengembalikan list nama dengan skor di atas atau sama dengan `batas` sesuai urutan asal.
            """,
            """
            def saring_lulus(data, batas):
                # TODO: implementasikan
                pass
            """,
            """
            d = [{"nama": "A", "skor": 80}, {"nama": "B", "skor": 50}, {"nama": "C", "skor": 60}]
            assert saring_lulus(d, 60) == ["A", "C"]
            assert saring_lulus(d, 90) == []
            assert saring_lulus([], 10) == []
            """,
            "Perulangan dengan if dan append.",
            """
            def saring_lulus(data, batas):
                hasil = []
                for r in data:
                    if r["skor"] >= batas:
                        hasil.append(r["nama"])
                return hasil
            """,
        ),
        E(
            "A1-02-3-ex3",
            "sedang",
            """
            Tulis fungsi `transpos(tabel)` yang mengembalikan transpos list berisi list persegi panjang. Untuk tabel kosong kembalikan list kosong.
            """,
            """
            def transpos(tabel):
                # TODO: implementasikan
                pass
            """,
            """
            assert transpos([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]
            assert transpos([[1]]) == [[1]]
            assert transpos([]) == []
            assert transpos([[1, 2]]) == [[1], [2]]
            """,
            "Perulangan luar atas kolom dan perulangan dalam atas baris.",
            """
            def transpos(tabel):
                if not tabel:
                    return []
                hasil = []
                for j in range(len(tabel[0])):
                    kolom = []
                    for i in range(len(tabel)):
                        kolom.append(tabel[i][j])
                    hasil.append(kolom)
                return hasil
            """,
        ),
        E(
            "A1-02-3-ex4",
            "menantang",
            """
            Tulis fungsi `pasangan_jumlah(angka, target)` yang mengembalikan list tuple `(a, b)` dari pasangan indeks `i < j` dengan `angka[i] + angka[j] == target`, urut menurut `i` lalu `j`.
            """,
            """
            def pasangan_jumlah(angka, target):
                # TODO: implementasikan
                pass
            """,
            """
            assert pasangan_jumlah([1, 2, 3, 4, 5, 6], 7) == [(1, 6), (2, 5), (3, 4)]
            assert pasangan_jumlah([2, 2, 2], 4) == [(2, 2), (2, 2), (2, 2)]
            assert pasangan_jumlah([1, 2], 10) == []
            assert pasangan_jumlah([], 3) == []
            assert pasangan_jumlah([5], 10) == []
            """,
            "Indeks dalam dimulai dari i + 1.",
            """
            def pasangan_jumlah(angka, target):
                hasil = []
                for i in range(len(angka)):
                    for j in range(i + 1, len(angka)):
                        if angka[i] + angka[j] == target:
                            hasil.append((angka[i], angka[j]))
                return hasil
            """,
        ),
    ],
    [
        M("Memulai indeks dalam dari nol saat mencari pasangan.", "Mulai dari i + 1 agar pasangan tidak ganda."),
        M("Tidak menguji tabel kosong atau satu elemen.", "Selalu uji kasus tepi."),
        M("Memakai perulangan bersarang pada data sangat besar.", "Perkirakan jumlah operasi dan cari pendekatan yang lebih efisien."),
    ],
    [
        Q("Dua perulangan bersarang masing-masing 10 putaran menjalankan blok dalam berapa kali?", ["20", "10", "100", "1000"], 2, "Putaran dalam penuh untuk tiap putaran luar sehingga 10 kali 10.", hint="Kalikan kedua jumlah putaran."),
        Q("Pada tabel [[1,2],[3,4]], berapa tabel[1][0]?", ["1", "2", "3", "4"], 2, "Baris indeks 1 adalah [3, 4] dan kolom indeks 0 adalah 3.", hint="Baris dulu lalu kolom."),
        Q("Mengapa indeks dalam pasangan dimulai dari i + 1?", ["Agar lebih lambat", "Agar pasangan tidak ganda dan tidak dengan diri sendiri", "Aturan Python", "Agar urut"], 1, "Setiap pasangan hanya dihitung sekali.", hint="Pikirkan pasangan (a, b) dan (b, a)."),
        Q("Untuk n elemen, dua perulangan bersarang menjalankan blok dalam kira-kira?", ["n kali", "n kali n", "2 kali n", "log n"], 1, "Pertumbuhannya kuadrat terhadap n.", hint="Kalikan."),
        Q("Struktur data dasar untuk tabel tanpa pustaka?", ["String", "List berisi list", "Set", "Tuple kosong"], 1, "List dalam list merepresentasikan baris dan kolom.", hint="Cikal bakal array dua dimensi."),
    ],
    [
        "Perulangan bersarang menjalankan putaran dalam penuh untuk tiap putaran luar.",
        "Tabel kecil bisa dipakai sebagai list berisi list.",
        "Penyaringan dan transformasi memakai perulangan dengan if dan append.",
        "Perulangan bersarang tumbuh kuadrat sehingga perlu diwaspadai pada data besar.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa kode dan contoh singkat yang cukup jelas dalam teks dan latihan.", "brief": []}

write_module(
    "A1",
    2,
    "Kontrol alur: kondisi dan perulangan",
    105,
    [
        "Menulis percabangan dengan if, elif, else, dan match",
        "Memakai for dan while beserta break, continue, dan else",
        "Mengolah data tabel kecil dengan perulangan bersarang",
    ],
    [l1, l2, l3],
    video,
    REF,
)
