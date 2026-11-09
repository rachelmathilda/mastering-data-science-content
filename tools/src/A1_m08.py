import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

l1 = lesson(
    "A1-08-1",
    "Penanganan error",
    35,
    [
        "Membaca traceback dan mengenali jenis exception umum",
        "Memakai try, except, else, dan finally dengan benar",
        "Menimbulkan exception dengan raise dan membuat exception sendiri",
        "Menulis validasi masukan yang jelas tanpa menelan bug",
    ],
    [
        T("""
        ## Error adalah informasi

        Setiap program akan menemui error. Pemula sering takut pada pesan merah, padahal traceback adalah peta yang sangat informatif. Baca dari bawah ke atas: baris terakhir menyebut jenis error dan pesannya, sedangkan baris di atasnya menunjukkan rangkaian pemanggilan yang menuju ke sana. Baris paling bawah dari kodemu biasanya tempat masalah muncul.

        Jenis exception yang paling sering: `SyntaxError` untuk tulisan yang salah, `NameError` untuk nama yang belum didefinisikan, `TypeError` untuk operasi pada tipe yang tidak cocok, `ValueError` untuk nilai bertipe benar tetapi tidak valid, `KeyError` untuk kunci dictionary yang tidak ada, `IndexError` untuk indeks di luar rentang, dan `ZeroDivisionError` untuk pembagian nol.

        Mengenali nama error memberimu petunjuk langsung tentang penyebabnya. Dalam data science, error paling sering muncul dari data tak terduga: nilai kosong, tipe salah, atau kolom yang hilang. Menanganinya dengan baik membedakan skrip rapuh dari pipeline andal.
        """),
        C(
            """
            kasus = [
                lambda: 1 / 0,
                lambda: int("abc"),
                lambda: [1, 2][5],
                lambda: {"a": 1}["b"],
                lambda: "3" + 4,
                lambda: undefined_name,
            ]
            for k in kasus:
                try:
                    k()
                except Exception as e:
                    print(type(e).__name__)
            """,
            """
            ZeroDivisionError
            ValueError
            IndexError
            KeyError
            TypeError
            NameError
            """,
            """
            Setiap jenis kesalahan memiliki exception tersendiri. Nama exception memberi petunjuk cepat tentang penyebabnya.
            """,
            filename="jenis_error.py",
        ),
        T("""
        ## try, except, else, dan finally

        Blok `try` berisi kode yang mungkin gagal. Bila terjadi exception, eksekusi lompat ke blok `except` yang sesuai. Selalu tangkap exception **spesifik** seperti `except ValueError`, bukan `except:` kosong atau `except Exception` yang menelan semua, termasuk bug yang seharusnya kamu ketahui. Satu `try` boleh punya beberapa `except` untuk jenis berbeda.

        Blok `else` dijalankan bila `try` selesai tanpa exception, cocok untuk kode yang hanya relevan saat berhasil. Blok `finally` selalu dijalankan, ada error atau tidak, dan cocok untuk pembersihan seperti menutup file, meski `with` biasanya lebih baik untuk itu.

        Simpan blok `try` sekecil mungkin, hanya baris yang memang mungkin gagal. Blok `try` yang besar menyembunyikan bagian mana yang sebenarnya bermasalah dan bisa menangkap error dari tempat yang tidak kamu duga.
        """),
        C(
            """
            def bagi(a, b):
                try:
                    hasil = a / b
                except ZeroDivisionError:
                    print("tidak bisa dibagi nol")
                    return None
                except TypeError:
                    print("tipe salah")
                    return None
                else:
                    print("berhasil")
                    return hasil
                finally:
                    print("selesai")

            print(bagi(10, 2))
            print(bagi(1, 0))
            print(bagi("a", 2))
            """,
            """
            berhasil
            selesai
            5.0
            tidak bisa dibagi nol
            selesai
            None
            tipe salah
            selesai
            None
            """,
            """
            `else` jalan saat sukses dan `finally` selalu jalan, bahkan saat ada `return` di dalam blok lain.
            """,
            filename="try_except.py",
        ),
        K(
            "warning",
            """
            Jangan menulis `except:` kosong atau `except Exception: pass`. Itu menelan error termasuk bug nyata, dan program terlihat berjalan padahal hasilnya salah.
            """,
            title="Jangan menelan semua error",
        ),
        T("""
        ## raise dan exception buatan sendiri

        Kamu menimbulkan exception sendiri dengan `raise`, misalnya `raise ValueError("umur tidak boleh negatif")`. Ini cara fungsi memberi tahu pemanggil bahwa masukan tidak valid, daripada diam-diam mengembalikan nilai ngawur. Pesan yang jelas menghemat banyak waktu debugging bagi siapa pun yang membaca error itu, termasuk dirimu sendiri nanti.

        Untuk kasus khusus aplikasi, buat kelas exception sendiri dengan mewarisi `Exception`: `class DataTidakValid(Exception): pass`. Exception khusus memudahkan pemanggil menangkap tepat kesalahan yang mereka antisipasi dan membedakannya dari bug lain.

        Di dalam blok `except`, `raise` tanpa argumen melempar ulang exception yang sedang ditangani. Pola ini berguna bila kamu ingin mencatat sesuatu lalu membiarkan error terus naik. Rantai exception dengan `raise Baru from asli` menyimpan penyebab aslinya untuk memudahkan penelusuran.
        """),
        C(
            """
            class DataTidakValid(Exception):
                pass

            def periksa_umur(umur):
                if not isinstance(umur, int):
                    raise TypeError("umur harus bilangan bulat")
                if umur < 0 or umur > 150:
                    raise DataTidakValid(f"umur di luar rentang: {umur}")
                return umur

            for u in [30, -5, "x", 200]:
                try:
                    print("ok", periksa_umur(u))
                except DataTidakValid as e:
                    print("data:", e)
                except TypeError as e:
                    print("tipe:", e)

            try:
                try:
                    int("x")
                except ValueError as e:
                    raise DataTidakValid("gagal membaca") from e
            except DataTidakValid as e:
                print(e, type(e.__cause__).__name__)
            """,
            """
            ok 30
            data: umur di luar rentang: -5
            tipe: umur harus bilangan bulat
            data: umur di luar rentang: 200
            gagal membaca ValueError
            """,
            """
            Exception buatan sendiri membedakan kesalahan data dari bug lain. `raise ... from` menyimpan penyebab asli di `__cause__`.
            """,
            filename="raise_kustom.py",
        ),
        T("""
        ## LBYL dan EAFP

        Ada dua gaya menangani kemungkinan gagal. **LBYL** (*look before you leap*) memeriksa kondisi dulu dengan `if`. **EAFP** (*easier to ask forgiveness than permission*) langsung mencoba lalu menangkap error. Python condong ke EAFP karena sering lebih ringkas dan menghindari kondisi balapan, misalnya saat file bisa dihapus di antara pengecekan dan pembukaan.

        Contoh LBYL: `if "k" in d: nilai = d["k"]`. Contoh EAFP: `try: nilai = d["k"] except KeyError: ...`. Untuk kasus sederhana seperti ini, `d.get("k")` sudah paling bersih. Pilih gaya yang membuat maksud kodemu paling jelas.

        Validasi masukan pengguna lebih cocok dengan LBYL karena kamu ingin memberi pesan yang ramah. Operasi yang bergantung pada keadaan luar seperti file dan jaringan lebih cocok dengan EAFP. Latihan berikut melatih keduanya.
        """),
        T("""
        ## Pesan error yang baik

        Pesan error yang baik menjawab tiga pertanyaan: apa yang salah, di mana, dan apa yang diharapkan. `ValueError("umur harus antara 0 dan 150, diterima -5")` jauh lebih berguna daripada `ValueError("salah")`. Sertakan nilai yang bermasalah dalam pesan agar penelusuran cepat, tetapi hati-hati agar tidak membocorkan data sensitif seperti kata sandi.

        Dalam pipeline data, pertimbangkan apakah error harus menghentikan seluruh proses atau cukup mencatat baris bermasalah lalu melanjutkan. Untuk data kecil dan kritis, hentikan. Untuk jutaan baris dengan sedikit data kotor, kumpulkan baris gagal dan laporkan di akhir. Keputusan ini bagian dari desain, bukan sekadar detail teknis.
        """),
        E(
            "A1-08-1-ex1",
            "mudah",
            """
            Tulis fungsi `ke_int(teks, bawaan=0)` yang mengembalikan `int(teks)` atau `bawaan` bila gagal mengubah.
            """,
            """
            def ke_int(teks, bawaan=0):
                # TODO: implementasikan
                pass
            """,
            """
            assert ke_int("42") == 42
            assert ke_int("abc") == 0
            assert ke_int("", bawaan=-1) == -1
            assert ke_int(" 7 ") == 7
            assert ke_int(None, 5) == 5
            """,
            "Tangkap ValueError dan TypeError.",
            """
            def ke_int(teks, bawaan=0):
                try:
                    return int(teks)
                except (ValueError, TypeError):
                    return bawaan
            """,
        ),
        E(
            "A1-08-1-ex2",
            "mudah",
            """
            Tulis fungsi `bagi_aman(a, b)` yang mengembalikan `a / b`, atau `None` bila `b` nol.
            """,
            """
            def bagi_aman(a, b):
                # TODO: implementasikan
                pass
            """,
            """
            assert bagi_aman(10, 4) == 2.5
            assert bagi_aman(1, 0) is None
            assert bagi_aman(0, 5) == 0
            assert bagi_aman(-6, 3) == -2
            """,
            "Tangkap ZeroDivisionError.",
            """
            def bagi_aman(a, b):
                try:
                    return a / b
                except ZeroDivisionError:
                    return None
            """,
        ),
        E(
            "A1-08-1-ex3",
            "sedang",
            """
            Tulis fungsi `periksa_nilai(n)` yang mengembalikan `n` bila 0 sampai 100 termasuk. Bila bukan bilangan bulat timbulkan `TypeError`, bila di luar rentang timbulkan `ValueError`. Perlakukan `True` dan `False` sebagai bukan bilangan bulat.
            """,
            """
            def periksa_nilai(n):
                # TODO: implementasikan
                pass
            """,
            """
            assert periksa_nilai(50) == 50
            assert periksa_nilai(0) == 0
            assert periksa_nilai(100) == 100
            for salah, jenis in [(101, ValueError), (-1, ValueError), ("5", TypeError), (2.5, TypeError), (True, TypeError)]:
                try:
                    periksa_nilai(salah)
                except jenis:
                    pass
                else:
                    raise AssertionError(salah)
            """,
            "Periksa tipe dulu dan pastikan bukan bool, lalu periksa rentang.",
            """
            def periksa_nilai(n):
                if not isinstance(n, int) or isinstance(n, bool):
                    raise TypeError("harus bilangan bulat")
                if n < 0 or n > 100:
                    raise ValueError("di luar rentang")
                return n
            """,
        ),
        E(
            "A1-08-1-ex4",
            "menantang",
            """
            Tulis fungsi `muat_semua(daftar)` yang menerima list string, mengubah tiap string menjadi `float`, dan mengembalikan tuple `(hasil, gagal)`. `hasil` adalah list float yang berhasil dan `gagal` adalah list string yang gagal diubah, keduanya dalam urutan asli.
            """,
            """
            def muat_semua(daftar):
                # TODO: implementasikan
                pass
            """,
            """
            assert muat_semua(["1", "2.5", "x", "", "3e2"]) == ([1.0, 2.5, 300.0], ["x", ""])
            assert muat_semua([]) == ([], [])
            assert muat_semua(["a"]) == ([], ["a"])
            assert muat_semua([" 4 "]) == ([4.0], [])
            """,
            "Telusuri tiap string dengan try dan simpan ke salah satu dari dua list.",
            """
            def muat_semua(daftar):
                hasil, gagal = [], []
                for s in daftar:
                    try:
                        hasil.append(float(s))
                    except ValueError:
                        gagal.append(s)
                return hasil, gagal
            """,
        ),
    ],
    [
        M("Memakai except kosong atau except Exception: pass.", "Tangkap exception spesifik dan tangani dengan jelas."),
        M("Membuat blok try terlalu besar.", "Taruh hanya baris yang mungkin gagal di dalam try."),
        M("Mengembalikan nilai ngawur untuk masukan tidak valid.", "Timbulkan exception dengan pesan jelas."),
    ],
    [
        Q("Exception untuk pembagian dengan nol?", ["ValueError", "ZeroDivisionError", "ArithmeticFail", "TypeError"], 1, "ZeroDivisionError khusus untuk pembagian nol.", hint="Namanya jelas."),
        Q("Kapan blok else pada try dijalankan?", ["Selalu", "Saat tidak ada exception", "Saat ada exception", "Tidak pernah"], 1, "else jalan bila try sukses.", hint="Kebalikan except."),
        Q("Kapan finally dijalankan?", ["Hanya saat sukses", "Hanya saat error", "Selalu", "Tidak pernah"], 2, "finally selalu dijalankan.", hint="Untuk pembersihan."),
        Q("Cara membuat exception sendiri?", ["Mewarisi Exception", "Memakai def", "Memakai lambda", "Memakai global"], 0, "Buat kelas yang mewarisi Exception.", hint="Kelas."),
        Q("Mengapa except kosong berbahaya?", ["Lambat", "Menelan semua error termasuk bug", "Tidak bisa dijalankan", "Tidak berbahaya"], 1, "Bug tersembunyi dan hasil bisa salah diam-diam.", hint="Terlalu luas."),
    ],
    [
        "Traceback dibaca dari bawah dan nama exception memberi petunjuk.",
        "Tangkap exception spesifik dengan try, except, else, dan finally.",
        "raise dan exception buatan sendiri memberi pesan yang jelas.",
        "Pilih LBYL untuk validasi dan EAFP untuk operasi bergantung keadaan luar.",
    ],
    [],
)

l2 = lesson(
    "A1-08-2",
    "Modul dan pustaka standar",
    35,
    [
        "Mengimpor modul dengan import, from import, dan alias",
        "Memahami __name__ dan pola if __name__ == '__main__'",
        "Memakai modul standar seperti math, random, datetime, dan collections",
        "Membaca dokumentasi modul dan memahami cara kerja pencarian modul",
    ],
    [
        T("""
        ## Modul dan impor

        **Modul** adalah file Python berisi definisi yang bisa dipakai ulang. Python hadir dengan pustaka standar yang sangat kaya, dan ekosistem pihak ketiga seperti NumPy dan pandas dipasang lewat `pip`. Kamu mengakses isi modul dengan `import`. Ada beberapa bentuk: `import math` lalu `math.sqrt(4)`, `from math import sqrt` lalu `sqrt(4)`, dan `import numpy as np` yang memberi alias pendek.

        Gunakan `import modul` bila ingin jelas dari mana sebuah fungsi berasal, dan alias untuk nama panjang yang sudah menjadi konvensi, seperti `np` dan `pd`. Hindari `from modul import *` karena menumpahkan semua nama ke ruang namamu dan menyulitkan pelacakan asal sebuah nama.

        Letakkan semua `import` di bagian atas file, dikelompokkan: pustaka standar dulu, lalu pihak ketiga, lalu modul milikmu. Konvensi ini membuat ketergantungan program terlihat sekilas.
        """),
        C(
            """
            import math
            from math import sqrt, pi
            import random as rnd
            from collections import Counter

            print(math.sqrt(16), sqrt(25), round(pi, 4))
            print(math.floor(2.7), math.ceil(2.1), math.gcd(12, 18))
            print(math.isclose(0.1 + 0.2, 0.3), 0.1 + 0.2 == 0.3)
            rnd.seed(1)
            a = [rnd.randint(1, 6) for _ in range(5)]
            rnd.seed(1)
            b = [rnd.randint(1, 6) for _ in range(5)]
            print(a == b)
            print(Counter("abracadabra").most_common(2))
            """,
            """
            4.0 5.0 3.1416
            2 3 6
            True False
            True
            [('a', 5), ('b', 2)]
            """,
            """
            Tiga bentuk impor memberi akses ke fungsi modul. `seed` membuat bilangan acak dapat diulang, dan `isclose` membandingkan desimal dengan toleransi.
            """,
            filename="impor_dasar.py",
        ),
        T("""
        ## __name__ dan skrip yang bisa diimpor

        Setiap modul punya variabel khusus `__name__`. Ketika file dijalankan langsung, nilainya `"__main__"`. Ketika file diimpor oleh file lain, nilainya adalah nama modul. Pola `if __name__ == "__main__":` memanfaatkannya: kode di dalam blok itu hanya jalan saat file dijalankan langsung, bukan saat diimpor.

        Ini memungkinkan satu file berfungsi sebagai pustaka sekaligus skrip. Fungsi-fungsinya dapat diimpor dan dipakai ulang tanpa efek samping, sedangkan bagian demonstrasi atau antarmuka baris perintah hanya jalan bila dijalankan langsung. Tanpa pola ini, mengimpor file akan menjalankan semua kode di dalamnya, termasuk yang mencetak atau membaca file.

        Dalam proyek data science, pola ini membantumu menyusun kode analisis menjadi modul yang bisa diuji dan dipakai di notebook tanpa mengeksekusi seluruh pipeline setiap kali diimpor.
        """),
        C(
            """
            def kuadrat(x):
                return x * x

            def main():
                print("menjalankan sebagai skrip", kuadrat(6))

            print(__name__)
            if __name__ == "__main__":
                main()
            """,
            """
            __main__
            menjalankan sebagai skrip 36
            """,
            """
            Saat dijalankan langsung `__name__` bernilai `__main__` sehingga `main()` berjalan. Bila diimpor, blok itu dilewati.
            """,
            filename="name_main.py",
        ),
        K(
            "tip",
            """
            Gunakan `dir(modul)` untuk melihat isi modul dan `help(modul.fungsi)` untuk membaca dokumentasinya langsung di kompiler.
            """,
            title="Menjelajah modul",
        ),
        T("""
        ## Pustaka standar yang paling berguna

        Beberapa modul standar akan sering kamu pakai. `math` untuk fungsi matematika, `random` untuk bilangan acak dan pengambilan sampel, `statistics` untuk rata-rata dan simpangan baku dasar, `datetime` untuk tanggal dan waktu, `collections` untuk struktur khusus seperti `Counter` dan `defaultdict`, `itertools` dan `functools` untuk alat fungsional, `json` dan `csv` untuk format data, serta `re` untuk regex.

        Kebiasaan penting: sebelum menulis fungsi sendiri, periksa apakah pustaka standar sudah menyediakannya. Fungsi pustaka umumnya sudah teruji, dioptimalkan, dan menangani kasus pinggir yang mudah terlewat. Menulis ulang pengurutan atau penghitung sendiri jarang berguna.

        Tentu bila membutuhkan operasi numerik berskala besar, NumPy dan pandas jauh lebih cepat daripada pustaka standar. Tetapi untuk skrip kecil dan pemrosesan teks, pustaka standar sering sudah cukup.
        """),
        C(
            """
            from collections import Counter, defaultdict
            from datetime import date, timedelta
            import statistics as st

            data = [4, 8, 6, 5, 3, 8]
            print(st.mean(data), st.median(data), st.mode(data))
            print(round(st.stdev(data), 3))

            c = Counter(["a", "b", "a", "c", "a", "b"])
            print(c["a"], c.most_common(1), c["z"])

            d = defaultdict(list)
            for k, v in [("x", 1), ("y", 2), ("x", 3)]:
                d[k].append(v)
            print(dict(d))

            hari = date(2024, 2, 28)
            print(hari + timedelta(days=2), (date(2024, 3, 1) - hari).days)
            print(hari.strftime("%d-%m-%Y"), hari.weekday())
            """,
            """
            5.666666666666667 5.5 8
            2.066
            3 [('a', 3)] 0
            {'x': [1, 3], 'y': [2]}
            2024-03-01 2
            28-02-2024 2
            """,
            """
            `Counter` dan `defaultdict` menyingkat pola penghitung dan pengelompokan. `datetime` menangani tanggal termasuk tahun kabisat, dan `statistics` memberi ringkasan dasar.
            """,
            filename="pustaka_standar.py",
        ),
        T("""
        ## Memasang pustaka pihak ketiga

        Di luar pustaka standar, kamu memasang paket dengan `pip install nama_paket` di terminal. Sebaiknya pakai lingkungan virtual agar tiap proyek punya versi paketnya sendiri dan tidak saling bertabrakan. Daftar paket beserta versinya dicatat di file seperti `requirements.txt` supaya orang lain bisa mereproduksi lingkunganmu.

        Pencatatan versi sangat penting dalam data science. Hasil analisis bisa berbeda antar versi pustaka, dan model yang dilatih dengan satu versi mungkin tidak dapat dimuat di versi lain. Reproduksibilitas dimulai dari lingkungan yang terdokumentasi.

        Di aplikasi ini kompiler sudah menyertakan pustaka populer seperti NumPy dan pandas bila tersedia, jadi kamu tidak perlu memasang apa pun untuk berlatih. Latihan berikut memakai pustaka standar saja.
        """),
        T("""
        ## Struktur proyek yang sehat

        Saat skripmu tumbuh, pecah menjadi beberapa file. Satu file untuk fungsi pembersihan data, satu untuk perhitungan fitur, satu untuk visualisasi, dan satu skrip utama yang merangkainya. Setiap file menjadi modul yang bisa diimpor dan diuji sendiri.

        Kelompokkan modul terkait dalam folder dengan file `__init__.py` sehingga menjadi paket. Beri nama modul pendek dan jelas dengan huruf kecil. Hindari memberi nama file sama dengan modul standar, misalnya `random.py` atau `json.py`, karena Python akan mengimpor file milikmu alih-alih pustaka aslinya dan menimbulkan error membingungkan.

        Kebiasaan menyusun proyek sejak awal sangat menghemat waktu saat proyek membesar. Latihan berikut memakai pustaka standar untuk menyelesaikan tugas kecil dengan cara yang bersih.
        """),
        E(
            "A1-08-2-ex1",
            "mudah",
            """
            Tulis fungsi `hipotenusa(a, b)` yang mengembalikan panjang sisi miring segitiga siku-siku memakai modul `math`.
            """,
            """
            import math

            def hipotenusa(a, b):
                # TODO: implementasikan
                pass
            """,
            """
            assert hipotenusa(3, 4) == 5
            assert hipotenusa(0, 2) == 2
            assert abs(hipotenusa(1, 1) - 2 ** 0.5) < 1e-12
            """,
            "Gunakan math.sqrt atau math.hypot.",
            """
            import math

            def hipotenusa(a, b):
                return math.hypot(a, b)
            """,
        ),
        E(
            "A1-08-2-ex2",
            "mudah",
            """
            Tulis fungsi `paling_sering(daftar)` yang mengembalikan elemen yang paling sering muncul memakai `Counter`. Bila seri, ambil yang pertama muncul. Bila kosong kembalikan `None`.
            """,
            """
            from collections import Counter

            def paling_sering(daftar):
                # TODO: implementasikan
                pass
            """,
            """
            assert paling_sering(["a", "b", "a"]) == "a"
            assert paling_sering([]) is None
            assert paling_sering([1, 2, 2, 1]) == 1
            assert paling_sering(["x"]) == "x"
            """,
            "most_common(1) mengembalikan list pasangan dan menjaga urutan kemunculan saat seri.",
            """
            from collections import Counter

            def paling_sering(daftar):
                if not daftar:
                    return None
                return Counter(daftar).most_common(1)[0][0]
            """,
        ),
        E(
            "A1-08-2-ex3",
            "sedang",
            """
            Tulis fungsi `selisih_hari(a, b)` yang menerima dua string tanggal berformat `YYYY-MM-DD` dan mengembalikan selisih hari (b dikurangi a) sebagai bilangan bulat, memakai `datetime.date`.
            """,
            """
            from datetime import date

            def selisih_hari(a, b):
                # TODO: implementasikan
                pass
            """,
            """
            assert selisih_hari("2024-02-28", "2024-03-01") == 2
            assert selisih_hari("2023-02-28", "2023-03-01") == 1
            assert selisih_hari("2024-05-01", "2024-05-01") == 0
            assert selisih_hari("2024-05-10", "2024-05-01") == -9
            """,
            "Ubah string dengan date.fromisoformat lalu kurangkan dan ambil days.",
            """
            from datetime import date

            def selisih_hari(a, b):
                return (date.fromisoformat(b) - date.fromisoformat(a)).days
            """,
        ),
        E(
            "A1-08-2-ex4",
            "menantang",
            """
            Tulis fungsi `ringkas(angka)` yang mengembalikan dictionary dengan kunci `rata`, `median`, `simpangan` (simpangan baku sampel) dibulatkan 3 desimal dan `modus`. Gunakan modul `statistics`. Anggap minimal dua nilai.
            """,
            """
            import statistics as st

            def ringkas(angka):
                # TODO: implementasikan
                pass
            """,
            """
            r = ringkas([4, 8, 6, 5, 3, 8])
            assert r == {"rata": 5.667, "median": 5.5, "simpangan": 2.066, "modus": 8}
            r2 = ringkas([1, 2, 3])
            assert r2["rata"] == 2 and r2["median"] == 2 and r2["simpangan"] == 1.0
            assert ringkas([2, 2])["modus"] == 2
            """,
            "Panggil mean, median, stdev, dan mode lalu bulatkan.",
            """
            import statistics as st

            def ringkas(angka):
                return {
                    "rata": round(st.mean(angka), 3),
                    "median": st.median(angka),
                    "simpangan": round(st.stdev(angka), 3),
                    "modus": st.mode(angka),
                }
            """,
        ),
    ],
    [
        M("Memakai from modul import * di mana-mana.", "Impor nama spesifik atau modul dengan alias."),
        M("Menulis ulang fungsi yang sudah ada di pustaka standar.", "Periksa pustaka standar lebih dulu."),
        M("Menaruh kode demonstrasi di tingkat atas modul.", "Bungkus dengan if __name__ == '__main__'."),
    ],
    [
        Q("Nilai __name__ saat file dijalankan langsung?", ["'main'", "'__main__'", "'file'", "None"], 1, "Ia bernilai __main__.", hint="Dengan garis bawah ganda."),
        Q("Fungsi untuk membandingkan float dengan toleransi?", ["math.same", "math.isclose", "math.equal", "math.near"], 1, "isclose membandingkan dengan toleransi.", hint="Dekat."),
        Q("Struktur untuk menghitung kemunculan?", ["Counter", "deque", "namedtuple", "OrderedSet"], 0, "Counter dari collections.", hint="Hitung."),
        Q("Mengapa from m import * tidak disarankan?", ["Error", "Menyulitkan pelacakan asal nama", "Lambat sekali", "Tidak ada"], 1, "Nama masuk ruang nama tanpa jelas asalnya.", hint="Asal nama."),
        Q("Fungsi untuk melihat isi modul?", ["dir", "list", "show", "open"], 0, "dir menampilkan nama dalam modul.", hint="Direktori."),
    ],
    [
        "import, from import, dan alias adalah cara mengakses modul.",
        "if __name__ == '__main__' memisahkan skrip dari pustaka.",
        "Pustaka standar menyediakan math, random, statistics, datetime, dan collections.",
        "Catat versi paket agar lingkungan dapat direproduksi.",
    ],
    [],
)

l3 = lesson(
    "A1-08-3",
    "Gaya kode, pengujian, dan kebiasaan baik",
    35,
    [
        "Menerapkan PEP 8 untuk penamaan, spasi, dan struktur kode",
        "Menulis docstring dan type hint yang berguna",
        "Menguji fungsi dengan assert dan memikirkan kasus batas",
        "Melakukan refactoring dan debugging secara sistematis",
    ],
    [
        T("""
        ## Kode dibaca lebih sering daripada ditulis

        Kode ditulis sekali tetapi dibaca puluhan kali, oleh rekan kerja dan oleh dirimu sendiri di masa depan. Karena itu keterbacaan adalah fitur, bukan kemewahan. **PEP 8** adalah panduan gaya resmi Python yang disepakati komunitas. Mengikutinya membuat kodemu terasa akrab bagi programmer Python mana pun.

        Aturan inti: nama variabel dan fungsi memakai huruf kecil dengan garis bawah (`hitung_rata_rata`), nama kelas memakai `HurufBesarDiAwalKata`, dan konstanta memakai `HURUF_BESAR`. Lekukan empat spasi, maksimal sekitar 79 sampai 100 karakter per baris, dua baris kosong antar fungsi tingkat atas, dan spasi di sekitar operator. Nama harus menjelaskan diri: `jumlah_pelanggan` jauh lebih baik daripada `jp` atau `x`.

        Alat otomatis seperti `black` dan `ruff` memformat dan memeriksa kode untukmu, sehingga kamu tidak perlu berdebat soal gaya. Pasang di editor dan biarkan alat bekerja.
        """),
        C(
            """
            MAKS_PERCOBAAN = 3

            def hitung_rata_rata(nilai_ujian):
                jumlah = sum(nilai_ujian)
                return jumlah / len(nilai_ujian)

            def buruk(l):
                s=0
                for i in l: s+=i
                return s/len(l)

            data = [80, 90, 70]
            print(hitung_rata_rata(data), buruk(data), hitung_rata_rata(data) == buruk(data))
            print(MAKS_PERCOBAAN)
            """,
            """
            80.0 80.0 True
            3
            """,
            """
            Kedua fungsi menghasilkan hasil sama, tetapi nama deskriptif dan spasi rapi membuat versi pertama jauh lebih mudah dibaca.
            """,
            filename="gaya_pep8.py",
        ),
        T("""
        ## Docstring dan type hint

        **Docstring** menjelaskan tujuan fungsi, parameter, dan nilai kembalian. Satu kalimat ringkas di baris pertama sudah sangat membantu, dan editor menampilkannya saat kamu mengarahkan kursor ke fungsi. Tulis apa yang dilakukan fungsi dan mengapa, bukan mengulang kode baris demi baris.

        **Type hint** menambahkan anotasi tipe pada parameter dan nilai kembalian: `def luas(p: float, l: float) -> float:`. Python tidak memaksakannya saat berjalan, tetapi editor dan alat seperti `mypy` memakainya untuk menangkap kesalahan lebih awal dan memberi pelengkapan kode yang lebih baik. Untuk koleksi, pakai `list[int]`, `dict[str, float]`, dan `str | None` untuk nilai opsional.

        Komentar berbeda dari docstring. Komentar menjelaskan *mengapa* ada keputusan yang tidak jelas, sedangkan kode yang baik sudah menjelaskan *apa* yang terjadi. Komentar yang berisi hal yang sudah jelas dari kode hanya menambah kebisingan dan cepat usang.
        """),
        C(
            """
            def luas_lingkaran(jari_jari: float) -> float:
                \"\"\"Mengembalikan luas lingkaran dengan jari-jari tertentu.\"\"\"
                return 3.14159 * jari_jari ** 2

            def cari(daftar: list[int], target: int) -> int | None:
                \"\"\"Mengembalikan indeks pertama target atau None bila tidak ada.\"\"\"
                for i, x in enumerate(daftar):
                    if x == target:
                        return i
                return None

            print(round(luas_lingkaran(2), 2))
            print(cari([5, 7, 9], 9), cari([5], 1))
            print(luas_lingkaran.__doc__)
            print(luas_lingkaran.__annotations__)
            """,
            """
            12.57
            2 None
            Mengembalikan luas lingkaran dengan jari-jari tertentu.
            {'jari_jari': <class 'float'>, 'return': <class 'float'>}
            """,
            """
            Type hint tersimpan di `__annotations__` dan dipakai alat bantu, tetapi tidak dipaksakan saat program berjalan.
            """,
            filename="docstring_hint.py",
        ),
        K(
            "tip",
            """
            Saat menamai sesuatu terasa sulit, itu sering tanda fungsinya melakukan terlalu banyak hal. Pecah fungsinya, dan nama yang tepat akan lebih mudah muncul.
            """,
            title="Nama sulit adalah petunjuk",
        ),
        T("""
        ## Menguji dan men-debug

        Cara paling sederhana menguji adalah `assert` dengan beberapa pemanggilan dan hasil yang diharapkan. Pikirkan kasus batas: nol, satu elemen, list kosong, nilai negatif, string kosong, dan masukan sangat besar. Bug paling sering bersembunyi di batas, bukan di kasus tengah. Pustaka `unittest` dan `pytest` menyediakan kerangka lebih lengkap untuk proyek yang lebih besar.

        Saat menemukan bug, bekerjalah sistematis. Reproduksi masalah dengan masukan sekecil mungkin, bentuk hipotesis tentang penyebabnya, lalu uji hipotesis itu dengan mencetak nilai antara atau memakai debugger. Hindari mengubah banyak hal sekaligus karena kamu tidak akan tahu perubahan mana yang memperbaiki atau malah merusak.

        Teknik klasik yang sangat efektif adalah *rubber duck debugging*: jelaskan kodemu baris demi baris kepada orang lain, atau bahkan bebek karet. Seringkali kamu menemukan kesalahannya sendiri di tengah menjelaskan. Biasakan juga menulis tes untuk setiap bug yang kamu temukan agar tidak muncul lagi.
        """),
        C(
            """
            def median(angka):
                urut = sorted(angka)
                n = len(urut)
                if n == 0:
                    raise ValueError("daftar kosong")
                tengah = n // 2
                if n % 2 == 1:
                    return urut[tengah]
                return (urut[tengah - 1] + urut[tengah]) / 2

            assert median([3, 1, 2]) == 2
            assert median([4, 1, 3, 2]) == 2.5
            assert median([7]) == 7
            try:
                median([])
            except ValueError:
                print("kosong ditolak")
            print("semua tes lulus")
            """,
            """
            kosong ditolak
            semua tes lulus
            """,
            """
            Tes mencakup jumlah ganjil, genap, satu elemen, dan kosong. Kasus batas diuji secara eksplisit.
            """,
            filename="uji_median.py",
        ),
        T("""
        ## Refactoring dan kebiasaan jangka panjang

        **Refactoring** adalah memperbaiki struktur kode tanpa mengubah perilakunya. Tanda kode butuh dirapikan: fungsi terlalu panjang, nama membingungkan, kode yang sama disalin di beberapa tempat, atau percabangan bersarang dalam. Tes yang baik membuatmu berani merapikan karena kamu langsung tahu bila ada yang rusak.

        Prinsip DRY (*don't repeat yourself*) menyarankan menjadikan logika berulang sebagai fungsi. Namun jangan berlebihan: abstraksi terlalu dini sering lebih buruk daripada sedikit pengulangan. Tunggu sampai pola muncul tiga kali sebelum membuat abstraksi.

        Terakhir, biasakan kendali versi dengan Git sejak awal, tulis pesan commit yang jelas, dan simpan proyekmu dengan struktur rapi. Kebiasaan kecil ini menjadi pembeda antara skrip sekali pakai dan pekerjaan profesional yang bisa dipertahankan. Kerjakan latihan berikut sambil memperhatikan nama, tes, dan kejelasan.
        """),
        T("""
        ## Membaca kode orang lain

        Keterampilan yang sama pentingnya dengan menulis adalah membaca. Saat menemui kode asing, mulai dari gambaran besar: apa tujuan file ini, fungsi mana yang menjadi pintu masuk, dan data apa yang mengalir. Baru kemudian turun ke detail satu fungsi. Jalankan kode dengan masukan kecil dan cetak nilai antara untuk memastikan pemahamanmu benar.

        Membaca kode pustaka populer di GitHub adalah cara belajar gaya dan pola yang baik. Perhatikan bagaimana mereka menamai, menyusun modul, dan menulis tes.
        """),
        E(
            "A1-08-3-ex1",
            "mudah",
            """
            Tulis fungsi `luas_segitiga(alas: float, tinggi: float) -> float` dengan type hint dan docstring yang mengembalikan luas segitiga.
            """,
            """
            def luas_segitiga(alas, tinggi):
                # TODO: implementasikan
                pass
            """,
            """
            assert luas_segitiga(4, 3) == 6
            assert luas_segitiga(0, 5) == 0
            assert luas_segitiga(2.5, 2) == 2.5
            assert luas_segitiga.__doc__ and luas_segitiga.__annotations__.get("return") is float
            """,
            "Tambahkan docstring tiga kutip dan anotasi -> float.",
            """
            def luas_segitiga(alas: float, tinggi: float) -> float:
                \"\"\"Mengembalikan luas segitiga dari alas dan tinggi.\"\"\"
                return alas * tinggi / 2
            """,
        ),
        E(
            "A1-08-3-ex2",
            "mudah",
            """
            Tulis fungsi `ke_snake_case(teks)` yang mengubah teks seperti `"Hitung Rata Rata"` menjadi `"hitung_rata_rata"`: huruf kecil dan spasi menjadi garis bawah. Spasi berlebih diabaikan.
            """,
            """
            def ke_snake_case(teks):
                # TODO: implementasikan
                pass
            """,
            """
            assert ke_snake_case("Hitung Rata Rata") == "hitung_rata_rata"
            assert ke_snake_case("  satu   dua ") == "satu_dua"
            assert ke_snake_case("") == ""
            assert ke_snake_case("Kata") == "kata"
            """,
            "Pecah dengan split, ubah kecil, dan gabung dengan garis bawah.",
            """
            def ke_snake_case(teks):
                return "_".join(teks.lower().split())
            """,
        ),
        E(
            "A1-08-3-ex3",
            "sedang",
            """
            Tulis fungsi `modus_semua(daftar)` yang mengembalikan list terurut semua nilai yang paling sering muncul. List kosong menghasilkan list kosong. Sertakan penanganan kasus seri.
            """,
            """
            def modus_semua(daftar):
                # TODO: implementasikan
                pass
            """,
            """
            assert modus_semua([1, 2, 2, 3, 3]) == [2, 3]
            assert modus_semua([5]) == [5]
            assert modus_semua([]) == []
            assert modus_semua(["b", "a", "a", "b", "c"]) == ["a", "b"]
            assert modus_semua([1, 1, 1, 2]) == [1]
            """,
            "Hitung kemunculan lalu ambil semua yang sama dengan hitungan maksimum.",
            """
            def modus_semua(daftar):
                if not daftar:
                    return []
                hitung = {}
                for x in daftar:
                    hitung[x] = hitung.get(x, 0) + 1
                puncak = max(hitung.values())
                return sorted(k for k, v in hitung.items() if v == puncak)
            """,
        ),
        E(
            "A1-08-3-ex4",
            "menantang",
            """
            Fungsi `buruk(l)` di bawah menghitung rata-rata tetapi gagal pada list kosong dan namanya tidak jelas. Tulis ulang sebagai `rata_rata(nilai)` yang mengembalikan rata-rata, menimbulkan `ValueError("daftar kosong")` untuk list kosong, dan memberi hasil sama untuk masukan lain.
            """,
            """
            def buruk(l):
                s=0
                for i in l: s+=i
                return s/len(l)

            def rata_rata(nilai):
                # TODO: tulis ulang dengan nama jelas dan penanganan kosong
                pass
            """,
            """
            assert rata_rata([80, 90, 70]) == 80
            assert rata_rata([5]) == 5
            assert rata_rata([1, 2]) == 1.5
            try:
                rata_rata([])
            except ValueError as e:
                assert str(e) == "daftar kosong"
            else:
                raise AssertionError("harus error")
            """,
            "Periksa kosong lebih dulu dengan raise lalu kembalikan sum dibagi len.",
            """
            def rata_rata(nilai):
                if not nilai:
                    raise ValueError("daftar kosong")
                return sum(nilai) / len(nilai)
            """,
        ),
    ],
    [
        M("Memakai nama singkat tak bermakna seperti x dan l.", "Beri nama yang menjelaskan isi dan tujuan."),
        M("Hanya menguji kasus tengah.", "Uji juga kosong, satu elemen, dan nilai batas."),
        M("Mengubah banyak hal sekaligus saat debugging.", "Ubah satu hal lalu uji ulang."),
    ],
    [
        Q("Gaya nama fungsi menurut PEP 8?", ["CamelCase", "snake_case", "KAPITAL", "kebab-case"], 1, "Huruf kecil dengan garis bawah.", hint="Tidak ada huruf besar."),
        Q("Fungsi type hint di Python?", ["Memaksa tipe saat berjalan", "Anotasi untuk alat bantu dan pembaca", "Mempercepat kode", "Mengganti docstring"], 1, "Tidak dipaksakan saat berjalan.", hint="Untuk editor dan mypy."),
        Q("Di mana bug paling sering bersembunyi?", ["Kasus tengah", "Kasus batas", "Nama variabel", "Komentar"], 1, "Batas seperti kosong dan nol.", hint="Tepi."),
        Q("Apa itu refactoring?", ["Menambah fitur", "Memperbaiki struktur tanpa mengubah perilaku", "Menghapus tes", "Menyalin kode"], 1, "Perilaku tetap, struktur lebih baik.", hint="Rapikan."),
        Q("Apa yang sebaiknya dijelaskan komentar?", ["Apa yang jelas dari kode", "Mengapa keputusan tidak jelas diambil", "Nama variabel", "Semua baris"], 1, "Komentar menjelaskan alasan.", hint="Mengapa, bukan apa."),
    ],
    [
        "PEP 8 menyeragamkan penamaan dan tata letak kode Python.",
        "Docstring dan type hint menjelaskan maksud fungsi.",
        "Uji kasus batas dan debug secara sistematis.",
        "Refactoring dan kendali versi menjaga kode tetap sehat.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa kode dan contoh singkat yang cukup jelas dalam teks dan latihan.", "brief": []}

write_module(
    "A1",
    8,
    "Error handling, modul, dan gaya kode",
    105,
    [
        "Menangani error dengan try, except, dan raise",
        "Memakai modul dan pustaka standar dengan benar",
        "Menulis kode yang rapi, teruji, dan mudah dirawat",
    ],
    [l1, l2, l3],
    video,
    REF,
)
