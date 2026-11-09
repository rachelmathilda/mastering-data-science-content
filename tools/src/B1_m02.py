import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []


def tb(h, b):
    return T("## " + h + "\n\n" + b)


def ind(s):
    return textwrap.indent(s.strip("\n"), "            ")


F1 = """
import numpy as np

def ambil_tepi(a):
    return [a[0].item(), a[-1].item()]
"""
F2 = """
import numpy as np

def blok(m, r0, r1, c0, c1):
    return m[r0:r1, c0:c1].tolist()
"""
F3 = """
import numpy as np

def selang_seling(m):
    return m[::2, ::2].tolist()
"""
F4 = """
import numpy as np

def ubah_tengah(a, nilai):
    c = a.copy()
    c[1:-1] = nilai
    return c
"""

l1 = lesson(
    "B1-02-1",
    "Indexing dan slicing",
    35,
    [
        "Mengambil elemen dengan indeks positif dan negatif",
        "Memotong array satu dan dua dimensi dengan slice",
        "Memakai langkah dan langkah negatif",
        "Memahami bahwa slice adalah view",
    ],
    [
        tb("Mengakses data array", "Setelah data masuk ke array, pekerjaan sehari-hari adalah mengambil sebagian darinya: satu nilai, satu baris, satu kolom, atau satu blok. NumPy memakai notasi kurung siku yang mirip list, tetapi diperluas untuk banyak dimensi. Menguasai notasi ini membuat Anda dapat memilih data tanpa perulangan, yang lebih singkat dan jauh lebih cepat. Pelajaran ini membahas indeks dan slice, dua pelajaran berikutnya membahas mask dan fancy indexing."),
        tb("Indeks satu dimensi", "Indeks dimulai dari nol. Elemen pertama adalah `a[0]` dan indeks negatif menghitung dari belakang, jadi `a[-1]` adalah elemen terakhir dan `a[-2]` yang sebelum terakhir. Mengakses indeks di luar batas menimbulkan `IndexError`. Hasil indeks tunggal pada array satu dimensi adalah skalar NumPy, bukan array, dan dapat diubah ke tipe Python dengan metode `item`."),
        tb("Slice satu dimensi", "Slice memakai bentuk `awal:akhir:langkah`. Indeks awal termasuk, indeks akhir tidak termasuk, dan langkah menentukan loncatan. Semua bagian boleh dikosongkan: awal kosong berarti dari depan, akhir kosong berarti sampai belakang, langkah kosong berarti satu. Langkah negatif membalik arah, sehingga `a[::-1]` membalik seluruh array. Slice di luar batas tidak menimbulkan galat, ia hanya memotong secukupnya."),
        C(
            ind("""
import numpy as np

a = np.arange(10)
print(a[2], a[-1])
print(a[2:7].tolist())
print(a[::3].tolist())
print(a[::-1].tolist())
print(a[-3:].tolist())
"""),
            ind("""
2 9
[2, 3, 4, 5, 6]
[0, 3, 6, 9]
[9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
[7, 8, 9]
"""),
            "Awal termasuk dan akhir tidak. Langkah tiga mengambil tiap elemen ketiga, dan langkah negatif membalik.",
            filename="slice_1d.py",
        ),
        tb("Indeks dua dimensi", "Pada matriks, tulis satu indeks per sumbu dipisah koma: `m[1, 2]` adalah baris satu kolom dua. Bentuk `m[1][2]` memberi hasil sama tetapi membuat array sementara, jadi gaya dengan koma lebih disarankan. Bila hanya memberi satu indeks, `m[1]` mengambil seluruh baris satu. Untuk mengambil satu kolom, gunakan titik dua pada sumbu baris: `m[:, 2]`."),
        tb("Slice pada banyak sumbu", "Slice dapat diterapkan pada tiap sumbu secara terpisah. Ungkapan `m[0:2, 1:3]` mengambil dua baris pertama dan kolom satu sampai dua, menghasilkan blok dua kali dua. Dengan langkah, `m[::2, ::2]` mengambil tiap baris dan kolom kedua. Titik dua tunggal berarti seluruh sumbu. Cara berpikir yang membantu adalah menentukan sumbu satu per satu dari kiri ke kanan."),
        C(
            ind("""
import numpy as np

m = np.arange(12).reshape(3, 4)
print(m[1, 2], m[1][2])
print(m[1].tolist())
print(m[:, 2].tolist())
print(m[0:2, 1:3].tolist())
print(m[::2, ::2].tolist())
print(m[-1, -1])
"""),
            ind("""
6 6
[4, 5, 6, 7]
[2, 6, 10]
[[1, 2], [5, 6]]
[[0, 2], [8, 10]]
11
"""),
            "Satu indeks mengambil baris, titik dua mengambil seluruh sumbu, dan slice pada dua sumbu menghasilkan blok.",
            filename="slice_2d.py",
        ),
        tb("Elips untuk banyak dimensi", "Pada array dengan banyak sumbu, menulis titik dua untuk tiap sumbu melelahkan. Tanda elips `...` menggantikan sebanyak mungkin titik dua yang diperlukan. Contohnya `x[..., 0]` mengambil indeks nol pada sumbu terakhir, apa pun jumlah sumbu lain. Notasi ini sering ditemui pada data gambar dengan sumbu tinggi, lebar, dan kanal warna, ketika kita ingin mengambil satu kanal saja."),
        tb("Slice adalah view", "Berbeda dari list, slice array tidak menyalin data. Hasilnya adalah view yang berbagi memori dengan array asal, sehingga mengubah slice ikut mengubah aslinya. Perilaku ini efisien untuk data besar, tetapi harus diingat. Bila Anda membutuhkan data terpisah, panggil `.copy()` pada hasil slice. Ini mengulang pelajaran view dari modul sebelumnya, dan di sini ia paling sering menjebak."),
        C(
            ind("""
import numpy as np

a = np.arange(10)
s = a[2:5]
s[0] = 99
print(a.tolist())
c = a[2:5].copy()
c[1] = -1
print(a.tolist())
print(np.shares_memory(a, s), np.shares_memory(a, c))
"""),
            ind("""
[0, 1, 99, 3, 4, 5, 6, 7, 8, 9]
[0, 1, 99, 3, 4, 5, 6, 7, 8, 9]
True False
"""),
            "Mengubah slice mengubah array asal, sedangkan salinan eksplisit tidak memengaruhinya.",
            filename="slice_view.py",
        ),
        tb("Penugasan lewat slice", "Slice juga dapat berada di sisi kiri tanda sama dengan untuk mengisi sebagian array. Menulis `a[1:-1] = 0` mengisi semua elemen kecuali tepi dengan nol. Nilai di kanan boleh skalar yang disebarkan ke seluruh slice, atau array dengan jumlah elemen yang cocok. Cara ini mengubah array di tempat, jadi pastikan Anda memang ingin mengubah aslinya."),
        tb("Pola umum", "Beberapa pola slice muncul terus. `a[:n]` mengambil n elemen pertama dan `a[-n:]` n elemen terakhir. `a[::-1]` membalik. `m[:, 0]` mengambil kolom pertama dan `m[0]` baris pertama. `m[1:, :-1]` membuang baris pertama dan kolom terakhir. Menghafal pola ini mempercepat penulisan kode analisis dan membuatnya mudah dibaca oleh orang lain yang akrab dengan NumPy."),
        K("tip", "Slice mengikuti aturan awal termasuk dan akhir tidak, sama seperti range. Panjang hasilnya adalah akhir dikurangi awal bila langkah satu.", title="Aturan slice"),
        tb("Slice di luar batas", "Berbeda dari indeks tunggal, slice yang melewati batas tidak menimbulkan galat. Menulis `a[8:100]` pada array sepuluh elemen cukup mengembalikan dua elemen terakhir, dan `a[20:30]` mengembalikan array kosong. Sifat ini nyaman untuk mengambil n elemen pertama tanpa memeriksa panjang, tetapi juga dapat menyembunyikan kesalahan indeks, jadi periksa shape hasil bila jumlah elemen penting."),
        E(
            "B1-02-1-ex1",
            "mudah",
            "Tulis fungsi `ambil_tepi(a)` yang mengembalikan list berisi elemen pertama dan elemen terakhir array satu dimensi `a` sebagai bilangan Python.",
            ind("""
import numpy as np

def ambil_tepi(a):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

assert ambil_tepi(np.arange(10)) == [0, 9]
assert ambil_tepi(np.array([5, 6, 7])) == [5, 7]
assert ambil_tepi(np.array([4])) == [4, 4]
assert ambil_tepi(np.array([1.5, 2.5])) == [1.5, 2.5]
"""),
            "Indeks nol dan minus satu, ubah dengan item.",
            F1.strip("\n"),
        ),
        E(
            "B1-02-1-ex2",
            "sedang",
            "Tulis fungsi `blok(m, r0, r1, c0, c1)` yang mengembalikan, sebagai list Python, blok matriks `m` dari baris `r0` sampai sebelum `r1` dan kolom `c0` sampai sebelum `c1`.",
            ind("""
import numpy as np

def blok(m, r0, r1, c0, c1):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

m = np.arange(12).reshape(3, 4)
assert blok(m, 0, 2, 1, 3) == [[1, 2], [5, 6]]
assert blok(m, 1, 3, 0, 1) == [[4], [8]]
assert blok(m, 0, 3, 0, 4) == m.tolist()
assert blok(m, 2, 2, 0, 4) == []
"""),
            "Gunakan dua slice dipisah koma.",
            F2.strip("\n"),
        ),
        E(
            "B1-02-1-ex3",
            "sedang",
            "Tulis fungsi `selang_seling(m)` yang mengembalikan, sebagai list Python, elemen matriks `m` pada baris dan kolom berindeks genap saja.",
            ind("""
import numpy as np

def selang_seling(m):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

m = np.arange(12).reshape(3, 4)
assert selang_seling(m) == [[0, 2], [8, 10]]
assert selang_seling(np.arange(9).reshape(3, 3)) == [[0, 2], [6, 8]]
assert selang_seling(np.arange(4).reshape(2, 2)) == [[0]]
assert selang_seling(np.arange(5).reshape(1, 5)) == [[0, 2, 4]]
"""),
            "Langkah dua pada kedua sumbu.",
            F3.strip("\n"),
        ),
        E(
            "B1-02-1-ex4",
            "menantang",
            "Tulis fungsi `ubah_tengah(a, nilai)` yang mengembalikan salinan array satu dimensi `a` dengan semua elemen selain yang pertama dan terakhir diganti `nilai`. Array asli tidak boleh berubah.",
            ind("""
import numpy as np

def ubah_tengah(a, nilai):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

a = np.arange(10)
r = ubah_tengah(a, 0)
assert r.tolist() == [0, 0, 0, 0, 0, 0, 0, 0, 0, 9]
assert a.tolist() == list(range(10))
assert ubah_tengah(np.array([1, 2, 3]), 7).tolist() == [1, 7, 3]
assert ubah_tengah(np.array([1, 2]), 7).tolist() == [1, 2]
"""),
            "Salin dulu, lalu isi slice dari indeks satu sampai minus satu.",
            F4.strip("\n"),
        ),
    ],
    [
        M("Mengira akhir slice termasuk.", "Akhir tidak termasuk."),
        M("Mengubah slice lalu heran data asal berubah.", "Panggil copy bila butuh data terpisah."),
        M("Memakai m[1][2] di perulangan besar.", "Pakai m[1, 2] agar tanpa array sementara."),
    ],
    [
        Q("a[-1] adalah?", ["Elemen terakhir", "Elemen pertama", "Galat", "Panjang"], 0, "Indeks negatif dari belakang.", hint="Belakang."),
        Q("a[::-1] melakukan?", ["Membalik array", "Menghapus", "Mengurutkan", "Menyalin tanpa urutan"], 0, "Langkah negatif.", hint="Balik."),
        Q("m[:, 2] mengambil?", ["Kolom kedua", "Baris kedua", "Elemen kedua", "Diagonal"], 0, "Seluruh baris, kolom dua.", hint="Titik dua."),
        Q("Slice menghasilkan?", ["View", "Salinan", "List", "Galat"], 0, "Berbagi memori.", hint="Bagi."),
        Q("a[2:5] memiliki berapa elemen?", ["3", "2", "5", "4"], 0, "Akhir dikurangi awal.", hint="Kurang."),
    ],
    [
        "Indeks mulai dari nol dan indeks negatif menghitung dari belakang.",
        "Slice berbentuk awal:akhir:langkah dan akhirnya tidak termasuk.",
        "Pada matriks tulis satu slice per sumbu dipisah koma.",
        "Slice adalah view, gunakan copy untuk data terpisah.",
    ],
    [],
)

G1 = """
import numpy as np

def jumlah_di_atas(x, batas):
    return int((x > batas).sum())
"""
G2 = """
import numpy as np

def rentang_tertutup(x, lo, hi):
    return x[(x >= lo) & (x <= hi)].tolist()
"""
G3 = """
import numpy as np

def batasi_atas(x, batas):
    y = x.copy()
    y[y > batas] = batas
    return y
"""
G4 = """
import numpy as np

def label_genap_ganjil(x):
    return np.where(x % 2 == 0, 'genap', 'ganjil').tolist()
"""

l2 = lesson(
    "B1-02-2",
    "Boolean masking dan np.where",
    35,
    [
        "Membuat mask boolean dari perbandingan",
        "Menyaring array dengan mask",
        "Menggabungkan syarat dengan operator logika elemen",
        "Memakai np.where untuk memilih nilai dan menemukan posisi",
    ],
    [
        tb("Memilih berdasarkan syarat", "Sering kali kita tidak memilih data menurut posisi, melainkan menurut isinya: semua suhu di atas 30, semua transaksi yang negatif, semua nilai yang hilang. Untuk itu NumPy memakai **mask boolean**, yaitu array True dan False berbentuk sama dengan datanya. Posisi bernilai True dipilih dan posisi bernilai False dibuang. Ini adalah alat penyaringan data paling penting dalam NumPy dan pandas."),
        tb("Membuat mask", "Mask lahir dari perbandingan. Menulis `x > 6` menghasilkan array boolean, satu nilai untuk tiap elemen, tanpa perulangan. Semua operator perbandingan bekerja: lebih besar, lebih kecil, sama dengan, tidak sama dengan. Mask dapat disimpan dalam variabel dan dipakai berulang, yang membuat kode lebih mudah dibaca daripada menulis syarat panjang di dalam kurung siku."),
        C(
            ind("""
import numpy as np

x = np.array([5, 12, 7, 20, 3, 15])
mk = x > 6
print(mk.tolist())
print(x[mk].tolist())
print(int(mk.sum()))
print(x[x % 2 == 0].tolist())
"""),
            ind("""
[False, True, True, True, False, True]
[12, 7, 20, 15]
4
[12, 20]
"""),
            "Mask berisi satu boolean per elemen. Indeks dengan mask menyaring, dan jumlah mask menghitung berapa yang memenuhi syarat.",
            filename="mask_dasar.py",
        ),
        tb("Menghitung dengan mask", "Karena True dihitung satu dan False nol, `mask.sum()` memberi jumlah elemen yang memenuhi syarat, dan `mask.mean()` memberi proporsinya. Dua ungkapan ini sangat sering dipakai dalam analisis: berapa persen pelanggan yang membeli, berapa banyak pengukuran yang melewati ambang. Fungsi `np.any` dan `np.all` merangkum mask menjadi satu jawaban: adakah satu yang benar, dan apakah semuanya benar."),
        tb("Menggabungkan syarat", "Untuk menggabungkan dua mask, pakai operator `&` untuk dan, `|` untuk atau, dan `~` untuk bukan. Kata `and`, `or`, dan `not` Python tidak bekerja pada array karena mencoba menilai seluruh array sebagai satu nilai, dan menghasilkan galat. Pasang kurung di sekeliling tiap perbandingan, karena `&` lebih diutamakan daripada `>`, dan tanpa kurung hasilnya salah atau galat."),
        C(
            ind("""
import numpy as np

x = np.array([5, 12, 7, 20, 3, 15])
print(((x > 6) & (x < 16)).tolist())
print(x[(x < 6) | (x > 14)].tolist())
print(x[~(x > 6)].tolist())
print(bool(np.any(x > 19)), bool(np.all(x > 2)))
"""),
            ind("""
[False, True, True, False, False, True]
[5, 20, 3, 15]
[5, 3]
True True
"""),
            "Gunakan ampersand, garis tegak, dan tilde dengan kurung. Any menyatakan ada yang benar dan all menyatakan semuanya benar.",
            filename="mask_gabung.py",
        ),
        tb("Mengubah nilai dengan mask", "Mask juga dapat berada di sisi kiri penugasan. Menulis `x[x > 10] = 10` membatasi semua nilai di atas sepuluh menjadi sepuluh. Teknik ini dipakai untuk memotong pencilan, mengganti nilai tidak valid, atau menandai kategori. Karena mengubah array di tempat, salin dahulu bila array asal harus tetap utuh. Fungsi `np.clip` melakukan pembatasan dua sisi dengan satu panggilan."),
        tb("np.where tiga argumen", "Fungsi `np.where(syarat, a, b)` memilih elemen dari `a` bila syarat benar dan dari `b` bila salah, menghasilkan array baru berbentuk sama. Ini versi vectorized dari ungkapan if-else, dan lebih ringkas daripada perulangan. Nilai `a` dan `b` boleh skalar atau array, termasuk teks, sehingga cocok untuk memberi label pada data."),
        C(
            ind("""
import numpy as np

x = np.array([5, 12, 7, 20, 3, 15])
print(np.where(x > 10, x, 0).tolist())
print(np.where(x % 2 == 0, 'genap', 'ganjil').tolist())
y = x.copy()
y[y > 10] = 10
print(y.tolist())
print(np.clip(x, 5, 15).tolist())
"""),
            ind("""
[0, 12, 0, 20, 0, 15]
['ganjil', 'genap', 'ganjil', 'genap', 'ganjil', 'ganjil']
[5, 10, 7, 10, 3, 10]
[5, 12, 7, 15, 5, 15]
"""),
            "Where memilih antara dua pilihan per elemen, penugasan mask membatasi di tempat, dan clip membatasi dua sisi.",
            filename="where_tiga.py",
        ),
        tb("np.where satu argumen", "Dipanggil hanya dengan syarat, `np.where(syarat)` mengembalikan posisi elemen yang benar, dalam bentuk tuple indeks satu per sumbu. Untuk array satu dimensi, ambil elemen nol tuple untuk mendapat array indeks. Fungsi `np.nonzero` melakukan hal yang sama. Posisi berguna ketika kita perlu tahu di mana nilai tertentu berada, bukan hanya nilainya."),
        tb("Mask pada matriks", "Mask bekerja pula pada matriks. Mask dengan shape sama menyaring elemen dan menghasilkan array satu dimensi, karena sisa elemen tidak lagi membentuk persegi panjang. Mask satu dimensi pada satu sumbu memilih seluruh baris atau kolom, misalnya `m[m[:, 0] > 0]` memilih baris yang kolom pertamanya positif. Bentuk hasil bergantung pada bentuk mask, jadi periksa shape setelahnya."),
        tb("Hasil kosong", "Bila tidak ada elemen yang memenuhi syarat, hasilnya array kosong berbentuk nol, bukan galat. Itu wajar, tetapi fungsi seperti `max` pada array kosong menimbulkan galat. Periksa `size` atau gunakan `mask.any()` sebelum menghitung ringkasan dari hasil penyaringan agar program tidak gagal karena data yang kebetulan tidak memenuhi syarat."),
        K("warn", "Gunakan & dan | dengan kurung di sekeliling tiap perbandingan. Kata and dan or tidak bekerja pada array.", title="Operator logika"),
        tb("Mask sebagai variabel", "Menyimpan mask dalam variabel bernama jelas, misalnya `lulus = nilai >= 60`, membuat kode terbaca seperti kalimat. Mask yang sama dapat dipakai untuk menyaring beberapa array sejajar, seperti nama dan nilai, sehingga data tetap konsisten. Cara ini juga menghindari menghitung ulang syarat yang sama berkali-kali pada data besar."),
        tb("Perbandingan dengan nilai hilang", "Nilai hilang pada array desimal direpresentasikan dengan `np.nan`, dan nilai ini tidak sama dengan apa pun, bahkan dirinya sendiri. Karena itu `x == np.nan` selalu salah. Gunakan `np.isnan(x)` untuk membuat mask nilai hilang dan `~np.isnan(x)` untuk menyaring yang valid. Ini kebiasaan penting sebelum menghitung rata-rata pada data nyata yang tidak bersih."),
        tb("Membandingkan dua array", "Mask tidak harus dari perbandingan dengan skalar. Membandingkan dua array berbentuk sama menghasilkan mask elemen demi elemen, misalnya prediksi yang sama dengan label asli. Rata-rata mask itu langsung memberi akurasi. Pola `np.mean(prediksi == label)` adalah salah satu baris paling sering muncul dalam evaluasi model klasifikasi."),
        tb("Fungsi isin", "Untuk memeriksa keanggotaan, `np.isin(x, daftar)` menghasilkan mask yang bernilai True bila elemen termasuk dalam daftar. Ini pengganti ringkas dari rangkaian syarat atau yang panjang, misalnya memilih transaksi dari beberapa kode wilayah. Mask hasilnya dapat digabung dengan operator logika seperti mask lainnya."),
        tb("Ringkasan pelajaran", "Mask boolean memindahkan logika penyaringan dari perulangan ke ekspresi tunggal. Buat mask dari perbandingan, gabungkan dengan operator elemen, lalu gunakan untuk menyaring, menghitung, atau mengganti nilai. Bersama np.where, mask menjawab hampir semua pertanyaan seleksi data."),
        E(
            "B1-02-2-ex1",
            "mudah",
            "Tulis fungsi `jumlah_di_atas(x, batas)` yang mengembalikan banyaknya elemen array `x` yang lebih besar dari `batas`, sebagai bilangan bulat Python.",
            ind("""
import numpy as np

def jumlah_di_atas(x, batas):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

x = np.array([5, 12, 7, 20, 3, 15])
assert jumlah_di_atas(x, 6) == 4
assert jumlah_di_atas(x, 100) == 0
assert jumlah_di_atas(x, 0) == 6
assert type(jumlah_di_atas(x, 6)) is int
"""),
            "Jumlahkan mask perbandingan lalu ubah ke int.",
            G1.strip("\n"),
        ),
        E(
            "B1-02-2-ex2",
            "sedang",
            "Tulis fungsi `rentang_tertutup(x, lo, hi)` yang mengembalikan list elemen `x` yang nilainya dari `lo` sampai `hi` inklusif, dengan urutan asli.",
            ind("""
import numpy as np

def rentang_tertutup(x, lo, hi):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

x = np.array([5, 12, 7, 20, 3, 15])
assert rentang_tertutup(x, 6, 15) == [12, 7, 15]
assert rentang_tertutup(x, 3, 5) == [5, 3]
assert rentang_tertutup(x, 50, 60) == []
assert rentang_tertutup(x, 20, 20) == [20]
"""),
            "Gabungkan dua perbandingan dengan ampersand dan kurung.",
            G2.strip("\n"),
        ),
        E(
            "B1-02-2-ex3",
            "sedang",
            "Tulis fungsi `batasi_atas(x, batas)` yang mengembalikan salinan `x` dengan semua nilai di atas `batas` diganti `batas`. Array asli tidak boleh berubah.",
            ind("""
import numpy as np

def batasi_atas(x, batas):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

x = np.array([5, 12, 7, 20, 3, 15])
r = batasi_atas(x, 10)
assert r.tolist() == [5, 10, 7, 10, 3, 10]
assert x.tolist() == [5, 12, 7, 20, 3, 15]
assert batasi_atas(x, 100).tolist() == x.tolist()
assert batasi_atas(x, 0).tolist() == [0, 0, 0, 0, 0, 0]
"""),
            "Salin dulu lalu isi lewat mask.",
            G3.strip("\n"),
        ),
        E(
            "B1-02-2-ex4",
            "menantang",
            "Tulis fungsi `label_genap_ganjil(x)` yang mengembalikan list string `'genap'` atau `'ganjil'` untuk tiap elemen bilangan bulat `x`, tanpa perulangan Python.",
            ind("""
import numpy as np

def label_genap_ganjil(x):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

x = np.array([5, 12, 7, 20, 3, 15])
assert label_genap_ganjil(x) == ['ganjil', 'genap', 'ganjil', 'genap', 'ganjil', 'ganjil']
assert label_genap_ganjil(np.array([0, -2, -3])) == ['genap', 'genap', 'ganjil']
assert label_genap_ganjil(np.array([], dtype=int)) == []
assert label_genap_ganjil(np.array([[1, 2], [3, 4]]).ravel()) == ['ganjil', 'genap', 'ganjil', 'genap']
"""),
            "np.where dengan syarat sisa bagi dua sama dengan nol.",
            G4.strip("\n"),
        ),
    ],
    [
        M("Memakai and atau or untuk menggabungkan mask.", "Pakai & dan | dengan kurung."),
        M("Lupa kurung pada perbandingan gabungan.", "Bungkus tiap perbandingan dengan kurung."),
        M("Menghitung max pada hasil saring kosong.", "Periksa size lebih dulu."),
    ],
    [
        Q("Mask boolean adalah?", ["Array True dan False", "Array angka", "Daftar indeks", "Tipe teks"], 0, "Satu boolean per elemen.", hint="Boolean."),
        Q("Jumlah mask memberi?", ["Banyak elemen True", "Total data", "Rata-rata data", "Galat"], 0, "True dihitung satu.", hint="Hitung."),
        Q("Operator dan pada mask?", ["&", "and", "&&", "+"], 0, "Elemen demi elemen.", hint="Ampersand."),
        Q("np.where(c, a, b) memilih?", ["a bila c benar", "b bila c benar", "selalu a", "indeks"], 0, "If-else vectorized.", hint="Jika benar."),
        Q("np.where(c) satu argumen memberi?", ["Posisi elemen True", "Nilai elemen", "Jumlah", "Mask"], 0, "Indeks.", hint="Posisi."),
    ],
    [
        "Mask boolean berasal dari perbandingan dan menyaring data.",
        "Gabungkan syarat dengan &, |, dan ~ berkurung.",
        "Jumlah dan rata-rata mask menghitung banyak dan proporsi.",
        "np.where memilih nilai atau menemukan posisi.",
    ],
    [],
)

H1 = """
import numpy as np

def ambil_indeks(x, idx):
    return x[idx].tolist()
"""
H2 = """
import numpy as np

def tiga_terbesar(x):
    return x[np.argsort(x)[::-1][:3]].tolist()
"""
H3 = """
import numpy as np

def sudut(m, baris, kolom):
    return m[np.ix_(baris, kolom)].tolist()
"""
H4 = """
import numpy as np

def tambah_duplikat(w, idx, n):
    r = w.copy()
    np.add.at(r, idx, n)
    return r
"""

l3 = lesson(
    "B1-02-3",
    "Fancy indexing dan penugasan",
    35,
    [
        "Memilih elemen dengan array indeks",
        "Memakai argsort, argmax, dan argmin untuk mencari posisi",
        "Memilih sub-matriks dengan np.ix_",
        "Memahami penugasan dengan indeks berulang",
    ],
    [
        tb("Memilih dengan daftar indeks", "Selain slice dan mask, NumPy mengizinkan indeks berupa list atau array bilangan bulat. Hasilnya memilih elemen pada posisi-posisi itu, dalam urutan yang Anda tulis, dan posisi boleh berulang. Teknik ini disebut **fancy indexing**. Ia berguna untuk mengambil sampel, mengurutkan ulang, atau memilih kolom tertentu dari matriks sesuai daftar yang dihitung program."),
        tb("Hasilnya adalah salinan", "Berbeda dari slice, fancy indexing selalu membuat salinan data. Mengubah hasilnya tidak memengaruhi array asal. Perbedaan ini sering membingungkan karena sintaksnya mirip slice. Aturan praktis: slice dengan titik dua menghasilkan view, sedangkan indeks list atau mask boolean menghasilkan salinan. Bila ragu, uji dengan `np.shares_memory`."),
        C(
            ind("""
import numpy as np

x = np.array([5, 12, 7, 20, 3, 15])
print(x[[0, 2, 2, 5]].tolist())
print(x[[-1, 0]].tolist())
h = x[[1, 3]]
h[0] = 0
print(x.tolist())
print(np.take(x, [1, 3]).tolist())
"""),
            ind("""
[5, 7, 7, 15]
[15, 5]
[5, 12, 7, 20, 3, 15]
[12, 20]
"""),
            "Posisi boleh berulang dan negatif. Hasil adalah salinan sehingga array asal tidak berubah.",
            filename="fancy_dasar.py",
        ),
        tb("Pasangan indeks pada matriks", "Pada matriks, dua list indeks bekerja berpasangan, bukan membentuk blok. Ungkapan `m[[0, 2], [1, 3]]` mengambil elemen pada posisi baris nol kolom satu dan baris dua kolom tiga, menghasilkan dua nilai. Bila yang diinginkan blok berisi semua kombinasi baris dan kolom terpilih, perlu cara lain. Salah paham ini menghasilkan bentuk yang tidak terduga, jadi cetak shape hasilnya."),
        tb("Blok dengan np.ix_", "Fungsi `np.ix_` membangun indeks silang dari beberapa list sehingga `m[np.ix_([0, 2], [1, 3])]` menghasilkan blok dua kali dua berisi semua kombinasi. Alternatifnya, lakukan dua langkah: pilih baris dulu lalu kolom, seperti `m[[0, 2]][:, [1, 3]]`. Keduanya memberi hasil sama, tetapi `np.ix_` lebih ringkas dan dapat dipakai langsung pada penugasan."),
        C(
            ind("""
import numpy as np

m = np.arange(12).reshape(3, 4)
print(m[[0, 2], [1, 3]].tolist())
print(m[np.ix_([0, 2], [1, 3])].tolist())
print(m[[0, 2]][:, [1, 3]].tolist())
print(m[:, [0, -1]].tolist())
"""),
            ind("""
[1, 11]
[[1, 3], [9, 11]]
[[1, 3], [9, 11]]
[[0, 3], [4, 7], [8, 11]]
"""),
            "Dua list berpasangan menghasilkan dua nilai, sedangkan ix_ menghasilkan blok semua kombinasi.",
            filename="fancy_matriks.py",
        ),
        tb("Mencari posisi dengan arg", "Fungsi berawalan arg mengembalikan posisi, bukan nilai. `np.argmax` dan `np.argmin` memberi indeks nilai terbesar dan terkecil. `np.argsort` memberi urutan indeks yang akan mengurutkan array. Dengan indeks itu, kita dapat mengurutkan array lain mengikuti urutan array pertama, misalnya mengurutkan nama berdasarkan skor. Fancy indexing dan fungsi arg hampir selalu dipakai bersama."),
        C(
            ind("""
import numpy as np

x = np.array([5, 12, 7, 20, 3, 15])
print(np.argsort(x).tolist())
print(x[np.argsort(x)[::-1][:3]].tolist())
print(int(np.argmax(x)), int(np.argmin(x)))
nama = np.array(['a', 'b', 'c', 'd', 'e', 'f'])
print(nama[np.argsort(x)].tolist())
"""),
            ind("""
[4, 0, 2, 1, 5, 3]
[20, 15, 12]
3 4
['e', 'a', 'c', 'b', 'f', 'd']
"""),
            "Argsort memberi urutan indeks. Dibalik dan dipotong, ia memberi tiga terbesar, dan dapat mengurutkan array lain.",
            filename="arg_posisi.py",
        ),
        tb("Penugasan dengan indeks", "Fancy indexing juga dapat berada di sisi kiri: `z[[1, 3]] = 7` mengisi posisi satu dan tiga. Slice berisi list nilai juga boleh, asalkan jumlahnya cocok. Penugasan ini mengubah array di tempat. Untuk pembaruan berpola seperti mengisi kolom tertentu, gabungan indeks dan penugasan jauh lebih ringkas daripada perulangan dan berjalan di kode C."),
        tb("Indeks berulang saat penugasan", "Ada jebakan halus: `w[[0, 0, 1]] += 10` tidak menambah posisi nol dua kali. Operasi dibaca sebagai membaca, menambah, lalu menulis, dan penulisan kedua ke posisi nol menimpa yang pertama, sehingga hanya sepuluh yang ditambahkan. Untuk menambah akumulatif pada indeks berulang, pakai `np.add.at(w, idx, n)`, yang memproses tiap indeks satu per satu."),
        C(
            ind("""
import numpy as np

w = np.array([1, 2, 3, 4])
w[[0, 0, 1]] += 10
print(w.tolist())
v = np.array([1, 2, 3, 4])
np.add.at(v, [0, 0, 1], 10)
print(v.tolist())
z = np.zeros(5, dtype=int)
z[[1, 3]] = 7
print(z.tolist())
z[1:4] = [1, 2, 3]
print(z.tolist())
"""),
            ind("""
[11, 12, 3, 4]
[21, 12, 3, 4]
[0, 7, 0, 7, 0]
[0, 1, 2, 3, 0]
"""),
            "Penambahan biasa pada indeks berulang hanya terhitung sekali. Add.at menghitung semuanya.",
            filename="penugasan_indeks.py",
        ),
        tb("Memilih mana yang tepat", "Gunakan slice bila posisi membentuk pola teratur, karena cepat dan berupa view. Gunakan mask bila memilih menurut isi. Gunakan fancy indexing bila posisinya acak atau dihitung, atau bila perlu urutan berbeda. Menggabungkan ketiganya, misalnya mask lalu argsort pada hasilnya, adalah cara umum menjawab pertanyaan seperti lima transaksi terbesar yang berstatus selesai."),
        K("tip", "Slice menghasilkan view, sedangkan indeks list dan mask menghasilkan salinan. Ingat perbedaan ini sebelum menugaskan.", title="View atau salinan"),
        tb("Fancy indexing pada penugasan matriks", "Penugasan lewat indeks silang juga mungkin. Menulis `m[np.ix_([0, 2], [1, 3])] = 0` mengisi blok kombinasi dengan nol. Ini berguna untuk menutupi wilayah tertentu pada gambar atau menetapkan nilai awal pada sebagian matriks. Karena penugasan mengubah array asal, salin lebih dulu bila diperlukan."),
        tb("Mengurutkan baris matriks", "Argsort pada satu kolom dapat dipakai untuk mengurutkan seluruh baris matriks mengikuti kolom itu. Tulis `m[np.argsort(m[:, 1])]` untuk mengurutkan baris menurut kolom kedua. Pola ini mengganti pengurutan manual dengan perulangan, dan menjaga setiap baris tetap utuh sehingga data yang berhubungan tidak tercerai."),
        tb("Fungsi take dan put", "Fungsi `np.take(a, indeks)` setara dengan fancy indexing dan menerima argumen `axis` untuk memilih sepanjang sumbu tertentu. Pasangannya, `np.put`, menulis nilai pada posisi pada array yang diratakan. Keduanya jarang wajib dipakai, tetapi berguna bila indeks dihitung dan Anda ingin menyatakan sumbunya secara eksplisit."),
        tb("Unik dan hitungan", "Fungsi `np.unique` mengembalikan nilai berbeda dalam urutan terurut, dan dengan `return_counts=True` juga mengembalikan jumlah kemunculan tiap nilai. Hasil indeks balik dapat dipakai untuk memetakan tiap elemen ke kelompoknya. Fungsi ini jembatan alami dari pemilihan data ke penghitungan frekuensi kategori."),
        tb("Ringkasan pelajaran", "Fancy indexing memberi kebebasan memilih posisi apa pun dalam urutan apa pun, dengan harga berupa salinan. Dipadukan dengan fungsi arg, ia mengurutkan dan memberi peringkat, dan dengan np.ix_ ia memilih blok. Hati-hati pada indeks berulang saat penugasan, dan gunakan np.add.at bila perlu akumulasi."),
        E(
            "B1-02-3-ex1",
            "mudah",
            "Tulis fungsi `ambil_indeks(x, idx)` yang mengembalikan, sebagai list Python, elemen array `x` pada posisi-posisi di list `idx`, sesuai urutan `idx`.",
            ind("""
import numpy as np

def ambil_indeks(x, idx):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

x = np.array([5, 12, 7, 20, 3, 15])
assert ambil_indeks(x, [0, 2, 2, 5]) == [5, 7, 7, 15]
assert ambil_indeks(x, [-1, 0]) == [15, 5]
assert ambil_indeks(x, []) == []
assert ambil_indeks(x, [3]) == [20]
"""),
            "Indeks array dengan list lalu tolist.",
            H1.strip("\n"),
        ),
        E(
            "B1-02-3-ex2",
            "sedang",
            "Tulis fungsi `tiga_terbesar(x)` yang mengembalikan list tiga nilai terbesar array `x`, dari terbesar ke terkecil, memakai `argsort`.",
            ind("""
import numpy as np

def tiga_terbesar(x):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

assert tiga_terbesar(np.array([5, 12, 7, 20, 3, 15])) == [20, 15, 12]
assert tiga_terbesar(np.array([1, 2, 3])) == [3, 2, 1]
assert tiga_terbesar(np.array([9, 9, 1, 5])) == [9, 9, 5]
assert tiga_terbesar(np.array([4, 8])) == [8, 4]
"""),
            "Urutkan indeks, balik, ambil tiga pertama, lalu indeks array.",
            H2.strip("\n"),
        ),
        E(
            "B1-02-3-ex3",
            "sedang",
            "Tulis fungsi `sudut(m, baris, kolom)` yang mengembalikan, sebagai list Python, sub-matriks `m` berisi semua kombinasi baris di list `baris` dan kolom di list `kolom`.",
            ind("""
import numpy as np

def sudut(m, baris, kolom):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

m = np.arange(12).reshape(3, 4)
assert sudut(m, [0, 2], [1, 3]) == [[1, 3], [9, 11]]
assert sudut(m, [1], [0, 3]) == [[4, 7]]
assert sudut(m, [0, 1, 2], [2]) == [[2], [6], [10]]
assert sudut(m, [2, 0], [0]) == [[8], [0]]
"""),
            "np.ix_ membangun indeks silang.",
            H3.strip("\n"),
        ),
        E(
            "B1-02-3-ex4",
            "menantang",
            "Tulis fungsi `tambah_duplikat(w, idx, n)` yang mengembalikan salinan `w` setelah `n` ditambahkan pada tiap posisi di `idx`, termasuk posisi yang muncul berulang (tiap kemunculan menambah `n` lagi). Array asli tidak boleh berubah.",
            ind("""
import numpy as np

def tambah_duplikat(w, idx, n):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

w = np.array([1, 2, 3, 4])
r = tambah_duplikat(w, [0, 0, 1], 10)
assert r.tolist() == [21, 12, 3, 4]
assert w.tolist() == [1, 2, 3, 4]
assert tambah_duplikat(w, [3, 3, 3], 1).tolist() == [1, 2, 3, 7]
assert tambah_duplikat(w, [], 5).tolist() == [1, 2, 3, 4]
"""),
            "Salin lalu panggil np.add.at.",
            H4.strip("\n"),
        ),
    ],
    [
        M("Mengira fancy indexing menghasilkan view.", "Hasilnya salinan."),
        M("Memakai += pada indeks berulang.", "Pakai np.add.at."),
        M("Mengira dua list indeks membentuk blok.", "Pakai np.ix_ untuk blok."),
    ],
    [
        Q("Fancy indexing menghasilkan?", ["Salinan", "View", "Skalar", "Galat"], 0, "Selalu menyalin.", hint="Salin."),
        Q("argsort mengembalikan?", ["Urutan indeks", "Array terurut", "Nilai terbesar", "Jumlah"], 0, "Posisi pengurutan.", hint="Indeks."),
        Q("np.ix_ dipakai untuk?", ["Blok kombinasi baris dan kolom", "Mengurutkan", "Menghitung", "Mengubah tipe"], 0, "Indeks silang.", hint="Silang."),
        Q("m[[0,2],[1,3]] menghasilkan?", ["Dua nilai berpasangan", "Blok dua kali dua", "Dua baris", "Galat"], 0, "Berpasangan.", hint="Pasangan."),
        Q("Penambahan akumulatif pada indeks berulang?", ["np.add.at", "+=", "np.sum", "np.take"], 0, "Memproses tiap indeks.", hint="add.at."),
    ],
    [
        "Fancy indexing memilih elemen dengan array indeks dan menghasilkan salinan.",
        "argsort, argmax, dan argmin mencari posisi.",
        "np.ix_ memilih blok kombinasi baris dan kolom.",
        "Indeks berulang pada penugasan butuh np.add.at.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perintah yang cukup jelas dalam teks.", "brief": []}

write_module(
    "B1",
    2,
    "Indexing, slicing, dan masking",
    105,
    [
        "Mengambil data dengan indeks dan slice",
        "Menyaring data dengan mask boolean dan np.where",
        "Memilih dan mengubah data dengan fancy indexing",
    ],
    [l1, l2, l3],
    video,
    REF,
)
