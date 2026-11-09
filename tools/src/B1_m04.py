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

def akar_aman(x):
    return np.sqrt(np.maximum(x, 0))
"""
F2 = """
import numpy as np

def bagi_aman(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    return np.divide(a, b, out=np.zeros(a.shape), where=b != 0)
"""
F3 = """
import numpy as np

def bulatkan_dua(x):
    return np.round(x, 2).tolist()
"""
F4 = """
import numpy as np

def hitung_tak_hingga(x):
    with np.errstate(all='ignore'):
        hasil = 1 / np.asarray(x, dtype=float)
    return int(np.isinf(hasil).sum())
"""

l1 = lesson(
    "B1-04-1",
    "Operasi vectorized dan fungsi matematika",
    35,
    [
        "Menjelaskan vectorization dan manfaatnya dibanding perulangan",
        "Memakai ufunc matematika dasar",
        "Memahami pembulatan dan modulo pada NumPy",
        "Menangani pembagian dengan nol dan nilai tak terdefinisi",
    ],
    [
        tb("Berpikir dalam array utuh", "**Vectorization** berarti menulis operasi pada seluruh array sekaligus, tanpa perulangan eksplisit. Alih-alih menulis `for` yang menghitung akar tiap elemen, kita menulis `np.sqrt(x)`. Perulangan tetap terjadi, tetapi di dalam kode C yang dikompilasi dan bekerja pada memori berurutan, sehingga jauh lebih cepat. Kode juga lebih pendek dan lebih mudah dibaca karena menyerupai rumus matematika."),
        tb("Ufunc", "Fungsi yang bekerja elemen demi elemen pada array disebut **universal function**, disingkat ufunc. Operator aritmetika seperti tambah, kali, dan pangkat adalah ufunc, begitu pula fungsi seperti `np.sqrt`, `np.exp`, `np.log`, dan `np.abs`. Semua ufunc mendukung broadcasting, menerima skalar maupun array, dan mengembalikan array baru berbentuk sesuai aturan broadcasting."),
        C(
            ind("""
import numpy as np

x = np.array([1., 4., 9., 16.])
print(np.sqrt(x).tolist())
print(np.exp(np.array([0., 1.])).round(4).tolist())
print(np.log(np.array([1., np.e, 100.])).round(4).tolist())
print(np.abs(np.array([-3, 2])).tolist())
print((np.array([2, 3]) ** 3).tolist())
print(np.sign(np.array([-3, 0, 5])).tolist())
"""),
            ind("""
[1.0, 2.0, 3.0, 4.0]
[1.0, 2.7183]
[0.0, 1.0, 4.6052]
[3, 2]
[8, 27]
[-1, 0, 1]
"""),
            "Ufunc menerapkan fungsi pada tiap elemen. Log alami e bernilai satu dan sign mengembalikan tanda.",
            filename="ufunc_dasar.py",
        ),
        tb("Hasil sama, jauh lebih cepat", "Menjumlahkan satu juta bilangan dengan perulangan Python memakan waktu puluhan milidetik hingga ratusan, sedangkan `np.sum` pada array yang sama selesai dalam sekitar satu milidetik. Selisih sepuluh sampai seratus kali ini membuat vectorization menjadi syarat praktis untuk analisis data. Anda dapat mengukurnya sendiri dengan modul `time` atau perintah `%timeit` di notebook."),
        C(
            ind("""
import numpy as np

x = np.arange(1000, dtype=float)
total_loop = 0.0
for v in x:
    total_loop += v * v
total_vec = float((x * x).sum())
print(total_loop == total_vec)
print(total_vec)
y = [v * v for v in range(5)]
print(y == (np.arange(5) ** 2).tolist())
"""),
            ind("""
True
332833500.0
True
"""),
            "Perulangan dan versi vectorized memberi hasil sama, tetapi versi kedua jauh lebih singkat dan cepat.",
            filename="loop_vs_vec.py",
        ),
        tb("Pembulatan", "NumPy menyediakan `np.floor` untuk pembulatan ke bawah, `np.ceil` ke atas, `np.trunc` menuju nol, dan `np.round` ke bilangan terdekat. Hati-hati: `np.round` membulatkan setengah ke genap terdekat, jadi 0,5 menjadi 0, 1,5 menjadi 2, dan 2,5 menjadi 2. Aturan ini mengurangi bias pada penjumlahan banyak angka, tetapi mengejutkan bila Anda mengharapkan aturan sekolah."),
        C(
            ind("""
import numpy as np

print(np.floor([1.7, -1.2]).tolist())
print(np.ceil([1.2, -1.7]).tolist())
print(np.trunc([1.7, -1.7]).tolist())
print(np.round([0.5, 1.5, 2.5]).tolist())
print(np.round([2.567, 0.5], 2).tolist())
"""),
            ind("""
[1.0, -2.0]
[2.0, -1.0]
[1.0, -1.0]
[0.0, 2.0, 2.0]
[2.57, 0.5]
"""),
            "Floor menuju bawah, ceil menuju atas, trunc menuju nol. Round membulatkan setengah ke genap terdekat.",
            filename="pembulatan.py",
        ),
        tb("Modulo dan sisa bagi", "Operator `%` dan fungsi `np.mod` menghitung sisa bagi, dan hasilnya mengikuti tanda pembagi. Jadi minus tujuh modulo tiga adalah dua, bukan minus satu. Sifat ini berguna untuk menghitung posisi melingkar, misalnya hari dalam pekan atau indeks buffer. Fungsi `np.remainder` identik, sedangkan `np.fmod` mengikuti tanda yang dibagi seperti bahasa C."),
        tb("Pembagian dengan nol", "Berbeda dari Python murni, pembagian desimal dengan nol pada NumPy tidak menghentikan program. Hasilnya `inf`, `-inf`, atau `nan` disertai peringatan. Logaritma nol memberi minus tak hingga, dan logaritma bilangan negatif memberi nan. Nilai khusus ini mengalir melalui perhitungan berikutnya dan dapat mencemari hasil akhir, jadi penting mengenalinya dan menanganinya dengan sengaja."),
        C(
            ind("""
import numpy as np

with np.errstate(all='ignore'):
    print((np.array([1., 0., -1.]) / 0).tolist())
    print(np.log(np.array([0., -1.])).tolist())
    print((np.array([0.]) / 0).tolist())
print(np.mod(np.array([7, -7]), 3).tolist())
a = np.array([1., 2., 3.])
b = np.array([2., 0., 3.])
print(np.divide(a, b, out=np.zeros(3), where=b != 0).tolist())
"""),
            ind("""
[inf, nan, -inf]
[-inf, nan]
[nan]
[1, 2]
[0.5, 0.0, 1.0]
"""),
            "Pembagian dengan nol memberi inf atau nan. Parameter where bersama out membagi hanya yang aman dan menyisakan nol.",
            filename="pembagian_nol.py",
        ),
        tb("Mengendalikan peringatan", "Konteks `np.errstate` mengatur apa yang terjadi saat galat numerik seperti pembagian nol. Dengan `all='ignore'`, peringatan dibungkam dalam blok itu, dan dengan `all='raise'` setiap galat menjadi pengecualian. Membungkam hanya masuk akal bila Anda tahu nilai khusus itu akan muncul dan siap menanganinya, bukan sekadar agar layar bersih."),
        tb("Parameter out dan where", "Semua ufunc menerima `out` untuk menulis hasil ke array yang sudah ada, yang menghemat alokasi memori pada data besar. Parameter `where` membatasi operasi pada posisi yang mask-nya benar, dan posisi lain dibiarkan seperti isi `out`. Gabungan keduanya adalah cara bersih menghitung hanya pada elemen valid tanpa menyaring dan menyusun ulang array."),
        tb("Tipe hasil ufunc", "Fungsi seperti `np.sqrt` dan `np.exp` selalu menghasilkan desimal, walau masukannya bilangan bulat. Pembagian biasa dengan garis miring tunggal juga menghasilkan desimal, sedangkan pembagian lantai dengan dua garis miring mempertahankan bilangan bulat. Pahami aturan promosi tipe agar tidak terkejut saat hasil tiba-tiba berubah dari bulat menjadi desimal."),
        tb("Kapan perulangan tetap perlu", "Tidak semua perhitungan dapat divektorkan. Bila nilai tiap langkah bergantung pada hasil langkah sebelumnya dengan cara rumit, seperti simulasi dengan keputusan bercabang, perulangan mungkin lebih jelas. Namun sering kali bentuk kumulatif seperti `cumsum` atau `accumulate`, yang dibahas pada pelajaran berikutnya, menyederhanakan kasus yang tampak berurutan."),
        K("tip", "Bila menulis for atas elemen array, berhenti sejenak dan tanyakan apakah ada ufunc atau ringkasan NumPy yang melakukannya sekaligus.", title="Refleks vectorized"),
        tb("Fungsi trigonometri dan lainnya", "NumPy juga menyediakan `np.sin`, `np.cos`, `np.tan`, dan kebalikannya, yang bekerja dalam radian, serta `np.deg2rad` untuk mengubah dari derajat. Ada pula `np.hypot` untuk sisi miring, `np.log10` dan `np.log2` untuk basis lain, dan `np.expm1` serta `np.log1p` yang lebih teliti untuk nilai sangat kecil. Seluruhnya ufunc, sehingga cara memakainya sama dengan fungsi yang sudah dibahas."),
        E(
            "B1-04-1-ex1",
            "mudah",
            "Tulis fungsi `akar_aman(x)` yang mengembalikan akar kuadrat tiap elemen array `x`, dengan elemen negatif diperlakukan sebagai nol sehingga hasilnya nol.",
            ind("""
import numpy as np

def akar_aman(x):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

r = akar_aman(np.array([4., -1., 9.]))
assert r.tolist() == [2.0, 0.0, 3.0]
assert akar_aman(np.array([0.])).tolist() == [0.0]
assert akar_aman(np.array([-5., -2.])).tolist() == [0.0, 0.0]
assert akar_aman(np.array([16.])).shape == (1,)
"""),
            "Batasi minimum nol dengan np.maximum lalu akarkan.",
            F1.strip("\n"),
        ),
        E(
            "B1-04-1-ex2",
            "sedang",
            "Tulis fungsi `bagi_aman(a, b)` yang mengembalikan `a / b` per elemen sebagai array desimal, dengan hasil `0.0` pada posisi di mana `b` bernilai nol.",
            ind("""
import numpy as np

def bagi_aman(a, b):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

assert bagi_aman([1, 2, 3], [2, 0, 3]).tolist() == [0.5, 0.0, 1.0]
assert bagi_aman([5, 5], [0, 0]).tolist() == [0.0, 0.0]
assert bagi_aman([6, 9], [3, 3]).tolist() == [2.0, 3.0]
assert bagi_aman([0, 1], [0, 4]).tolist() == [0.0, 0.25]
"""),
            "Gunakan np.divide dengan out berisi nol dan where bukan nol.",
            F2.strip("\n"),
        ),
        E(
            "B1-04-1-ex3",
            "sedang",
            "Tulis fungsi `bulatkan_dua(x)` yang membulatkan tiap elemen array `x` ke dua angka desimal dan mengembalikannya sebagai list Python.",
            ind("""
import numpy as np

def bulatkan_dua(x):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

assert bulatkan_dua(np.array([2.567, 0.5])) == [2.57, 0.5]
assert bulatkan_dua(np.array([1.234, 9.999])) == [1.23, 10.0]
assert bulatkan_dua(np.array([3.0])) == [3.0]
assert bulatkan_dua(np.array([])) == []
"""),
            "np.round menerima jumlah desimal.",
            F3.strip("\n"),
        ),
        E(
            "B1-04-1-ex4",
            "menantang",
            "Tulis fungsi `hitung_tak_hingga(x)` yang menghitung `1 / x` per elemen dan mengembalikan banyaknya hasil yang tak hingga (positif atau negatif), sebagai bilangan bulat Python, tanpa memunculkan peringatan.",
            ind("""
import numpy as np

def hitung_tak_hingga(x):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

assert hitung_tak_hingga([0, 2, 0.0, -1]) == 2
assert hitung_tak_hingga([1, 2, 3]) == 0
assert hitung_tak_hingga([0, 0, 0]) == 3
assert type(hitung_tak_hingga([0])) is int
"""),
            "Bungkus pembagian dalam errstate lalu hitung isinf.",
            F4.strip("\n"),
        ),
    ],
    [
        M("Menulis for untuk operasi elemen sederhana.", "Pakai ufunc atau operator array."),
        M("Mengira np.round membulatkan setengah ke atas.", "Ia membulatkan setengah ke genap terdekat."),
        M("Membiarkan inf dan nan mengalir tanpa dicek.", "Tangani dengan errstate, where, atau pengecekan."),
    ],
    [
        Q("Ufunc bekerja?", ["Elemen demi elemen", "Hanya pada baris", "Hanya skalar", "Pada teks"], 0, "Pada tiap elemen.", hint="Elemen."),
        Q("np.round(2.5) menghasilkan?", ["2.0", "3.0", "2.5", "Galat"], 0, "Setengah ke genap.", hint="Genap."),
        Q("-7 % 3 pada NumPy?", ["2", "-1", "1", "-2"], 0, "Mengikuti tanda pembagi.", hint="Positif."),
        Q("1.0 / 0 pada array menghasilkan?", ["inf", "Galat berhenti", "0", "nan saja"], 0, "Dengan peringatan.", hint="Tak hingga."),
        Q("Parameter yang membatasi operasi ufunc?", ["where", "axis", "dtype", "size"], 0, "Mask posisi.", hint="Di mana."),
    ],
    [
        "Vectorization menjalankan perulangan di kode C sehingga cepat dan ringkas.",
        "Ufunc menerapkan fungsi elemen demi elemen dan mendukung broadcasting.",
        "np.round membulatkan setengah ke genap terdekat.",
        "Pembagian dengan nol memberi inf atau nan, tangani dengan sengaja.",
    ],
    [],
)

G1 = """
import numpy as np

def total_kolom(a):
    return np.asarray(a).sum(axis=0).tolist()
"""
G2 = """
import numpy as np

def rata_rata_valid(x):
    return float(np.nanmean(x))
"""
G3 = """
import numpy as np

def pertumbuhan(x):
    x = np.asarray(x, dtype=float)
    return np.diff(x) / x[:-1]
"""
G4 = """
import numpy as np

def jumlah_bergerak(x, k):
    return np.convolve(x, np.ones(k), 'valid').tolist()
"""

l2 = lesson(
    "B1-04-2",
    "Agregasi, sumbu, dan fungsi kumulatif",
    35,
    [
        "Meringkas array dengan sum, mean, std, min, dan max",
        "Memilih sumbu ringkasan dengan benar",
        "Memakai fungsi kumulatif dan diff",
        "Menangani nilai hilang dengan fungsi nan",
    ],
    [
        tb("Meringkas banyak nilai", "Analisis data hampir selalu berakhir pada ringkasan: total penjualan, rata-rata nilai, nilai tertinggi. NumPy menyediakan `sum`, `mean`, `std`, `var`, `min`, `max`, `prod`, dan banyak lagi, baik sebagai fungsi `np.sum(a)` maupun metode `a.sum()`. Tanpa argumen, ringkasan menyeluruh menghasilkan satu skalar. Dengan argumen `axis`, ringkasan dilakukan sepanjang sumbu tertentu."),
        tb("Memahami axis", "Argumen `axis` menyatakan sumbu yang diringkas, dan sumbu itu hilang dari hasil. Pada matriks, `axis=0` meringkas turun melintasi baris sehingga menghasilkan satu angka per kolom. `axis=1` meringkas ke kanan melintasi kolom dan menghasilkan satu angka per baris. Cara mengingat paling aman: sumbu yang Anda tulis adalah sumbu yang lenyap dari shape hasil."),
        C(
            ind("""
import numpy as np

a = np.array([[1, 2, 3], [4, 5, 6]])
print(a.sum())
print(a.sum(axis=0).tolist())
print(a.sum(axis=1).tolist())
print(a.mean(axis=0).tolist())
print(a.max(axis=1).tolist())
print(a.prod(axis=0).tolist())
"""),
            ind("""
21
[5, 7, 9]
[6, 15]
[2.5, 3.5, 4.5]
[3, 6]
[4, 10, 18]
"""),
            "Axis nol memberi satu hasil per kolom dan axis satu memberi satu hasil per baris.",
            filename="agregasi_axis.py",
        ),
        tb("Statistik deskriptif", "Selain total dan rata-rata, `np.std` dan `np.var` memberi simpangan baku dan ragam, `np.median` memberi nilai tengah, dan `np.percentile` memberi persentil. Perhatikan bahwa `std` dan `var` secara bawaan membagi dengan n, yaitu ragam populasi. Untuk ragam sampel, tambahkan argumen `ddof=1` yang membagi dengan n dikurangi satu. Pilihan ini memengaruhi hasil terutama pada sampel kecil."),
        C(
            ind("""
import numpy as np

d = [1, 2, 3, 4]
print(np.var(d), np.std(d, ddof=1).round(4))
print(np.median([5, 1, 3, 2]))
print(np.percentile([1, 2, 3, 4, 5], 50))
print(np.percentile([1, 2, 3, 4], 25))
print(np.ptp([3, 9, 1]))
"""),
            ind("""
1.25 1.291
2.5
3.0
1.75
8
"""),
            "Ragam bawaan membagi dengan n, sedangkan ddof satu memberi simpangan baku sampel. Ptp memberi rentang nilai.",
            filename="statistik_dasar.py",
        ),
        tb("Posisi nilai ekstrem", "Fungsi `argmax` dan `argmin` mengembalikan posisi nilai terbesar dan terkecil, bukan nilainya. Dengan `axis`, keduanya memberi posisi per baris atau kolom. Bila nilai ekstrem muncul lebih dari sekali, yang dikembalikan adalah posisi kemunculan pertama. Posisi ini sering dipakai untuk memilih kelas dengan skor tertinggi pada keluaran model klasifikasi."),
        tb("Fungsi kumulatif", "Fungsi `cumsum` dan `cumprod` mengembalikan jumlah dan hasil kali berjalan, dengan satu hasil untuk tiap posisi. Tanpa `axis`, array diratakan lebih dulu. Jumlah kumulatif dipakai untuk saldo berjalan dan distribusi kumulatif, sedangkan hasil kali kumulatif dipakai untuk pertumbuhan majemuk. Fungsi `np.diff` adalah kebalikannya: ia menghitung selisih antar elemen bertetangga, sehingga panjang hasil berkurang satu."),
        C(
            ind("""
import numpy as np

a = np.array([[1, 2, 3], [4, 5, 6]])
print(a.cumsum(axis=1).tolist())
print(a.cumsum().tolist())
print(np.cumprod([1, 2, 3, 4]).tolist())
print(np.diff([1, 4, 9, 16]).tolist())
print(np.argmax(a, axis=1).tolist())
"""),
            ind("""
[[1, 3, 6], [4, 9, 15]]
[1, 3, 6, 10, 15, 21]
[1, 2, 6, 24]
[3, 5, 7]
[2, 2]
"""),
            "Cumsum menjumlahkan berjalan, diff menghitung selisih bertetangga, dan argmax memberi posisi nilai terbesar.",
            filename="kumulatif.py",
        ),
        tb("reduce dan accumulate", "Cumsum dan sum adalah kasus khusus dari mekanisme ufunc yang lebih umum. Setiap ufunc biner memiliki metode `reduce`, yang melipat array menjadi satu nilai, dan `accumulate`, yang menyimpan hasil antara. Jadi `np.add.reduce` setara sum dan `np.multiply.accumulate` setara cumprod. Mekanisme umum ini memungkinkan ringkasan khusus seperti maksimum berjalan lewat `np.maximum.accumulate`."),
        C(
            ind("""
import numpy as np

print(int(np.add.reduce([1, 2, 3])))
print(np.add.accumulate([1, 2, 3]).tolist())
print(int(np.multiply.reduce([1, 2, 3, 4])))
print(np.maximum.accumulate([1, 3, 2, 5, 4]).tolist())
print(np.minimum.accumulate([5, 3, 4, 1]).tolist())
"""),
            ind("""
6
[1, 3, 6]
24
[1, 3, 3, 5, 5]
[5, 3, 3, 1]
"""),
            "Reduce melipat ke satu nilai dan accumulate menyimpan semua hasil antara. Maksimum berjalan hanya naik.",
            filename="reduce_accumulate.py",
        ),
        tb("Nilai hilang", "Data nyata sering memuat nilai hilang yang dinyatakan `np.nan`. Satu nan membuat `sum` dan `mean` biasa menghasilkan nan. Keluarga fungsi `nansum`, `nanmean`, `nanmax`, `nanstd`, dan sejenisnya mengabaikan nan. Gunakan `np.isnan` untuk menghitung atau menandai nilai hilang. Selalu laporkan berapa banyak nilai yang diabaikan, karena mengabaikannya diam-diam dapat menyembunyikan masalah kualitas data."),
        C(
            ind("""
import numpy as np

n = np.array([1., np.nan, 3.])
print(n.sum(), np.nansum(n))
print(np.nanmean(n), np.nanmax(n))
print(np.isnan(n).tolist(), int(np.isnan(n).sum()))
print(float(np.nanmean(n)) == 2.0)
"""),
            ind("""
nan 4.0
2.0 3.0
[False, True, False] 1
True
"""),
            "Satu nan mencemari sum. Fungsi nan mengabaikannya, dan isnan menghitung berapa banyak yang hilang.",
            filename="nilai_hilang.py",
        ),
        tb("Rata-rata bergerak", "Rata-rata bergerak menghaluskan data deret waktu dengan merata-ratakan jendela yang bergeser. Cara ringkas adalah konvolusi dengan vektor satu: `np.convolve(x, np.ones(k), 'valid')` menghasilkan jumlah tiap jendela berukuran k, lalu bagi dengan k bila ingin rata-rata. Argumen `valid` hanya menyimpan posisi ketika jendela penuh sehingga hasil lebih pendek dari masukan."),
        tb("Memilih sumbu dengan benar", "Kesalahan sumbu tidak memicu galat, hanya hasil yang keliru. Biasakan memeriksa shape hasil: matriks tiga kali empat diringkas dengan sumbu nol harus berbentuk empat, dan dengan sumbu satu berbentuk tiga. Pada array tiga dimensi, argumen sumbu boleh berupa tuple untuk meringkas dua sumbu sekaligus, dan `keepdims=True` menjaga hasil siap untuk broadcasting."),
        K("tip", "Setelah meringkas, periksa shape hasil. Sumbu yang Anda tulis harus lenyap dari shape.", title="Cek sumbu"),
        tb("Ringkasan bersyarat", "Menggabungkan mask dengan agregasi menghasilkan ringkasan bersyarat tanpa perulangan. Rata-rata nilai yang lulus ditulis `nilai[nilai >= 60].mean()`, banyaknya yang lulus `(nilai >= 60).sum()`, dan proporsi `(nilai >= 60).mean()`. Pola ini menggantikan banyak kueri yang biasa ditulis sebagai perulangan dengan penghitung, dan dapat dikombinasikan dengan sumbu untuk ringkasan per kolom."),
        tb("Urutan dan peringkat", "Fungsi `np.sort` mengembalikan salinan terurut, sedangkan `np.argsort` mengembalikan urutan indeksnya. Dua kali argsort menghasilkan peringkat tiap elemen. Untuk matriks, urutan dapat diterapkan per sumbu, sehingga `np.sort(a, axis=1)` mengurutkan tiap baris sendiri-sendiri. Median dan persentil pada dasarnya bergantung pada pengurutan ini."),
        tb("Kesalahan umum agregasi", "Dua kesalahan paling sering: meringkas dengan sumbu yang salah, dan mengabaikan tipe hasil. Jumlah bilangan bulat berukuran kecil dapat melilit, dan rata-rata bilangan bulat selalu desimal. Periksa tipe dan rentang sebelum meringkas data bertipe sempit seperti uint8, dan ubah ke tipe lebih lebar bila perlu dengan argumen dtype pada sum."),
        E(
            "B1-04-2-ex1",
            "mudah",
            "Tulis fungsi `total_kolom(a)` yang mengembalikan jumlah tiap kolom matriks `a` sebagai list Python.",
            ind("""
import numpy as np

def total_kolom(a):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

assert total_kolom([[1, 2, 3], [4, 5, 6]]) == [5, 7, 9]
assert total_kolom([[1], [2], [3]]) == [6]
assert total_kolom(np.ones((2, 2))) == [2.0, 2.0]
assert total_kolom([[0, 0]]) == [0, 0]
"""),
            "Jumlahkan sepanjang sumbu nol.",
            G1.strip("\n"),
        ),
        E(
            "B1-04-2-ex2",
            "sedang",
            "Tulis fungsi `rata_rata_valid(x)` yang mengembalikan rata-rata elemen `x` dengan mengabaikan nilai `nan`, sebagai bilangan Python.",
            ind("""
import numpy as np

def rata_rata_valid(x):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

assert rata_rata_valid(np.array([1., np.nan, 3.])) == 2.0
assert rata_rata_valid(np.array([2., 4.])) == 3.0
assert rata_rata_valid(np.array([np.nan, 5.])) == 5.0
assert type(rata_rata_valid(np.array([1., 2.]))) is float
"""),
            "np.nanmean mengabaikan nan.",
            G2.strip("\n"),
        ),
        E(
            "B1-04-2-ex3",
            "sedang",
            "Tulis fungsi `pertumbuhan(x)` yang menerima deret nilai dan mengembalikan array laju pertumbuhan antar periode, yaitu selisih dibagi nilai periode sebelumnya.",
            ind("""
import numpy as np

def pertumbuhan(x):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

assert np.allclose(pertumbuhan([100, 110, 121]), [0.1, 0.1])
assert np.allclose(pertumbuhan([50, 25]), [-0.5])
assert pertumbuhan([1, 2, 3, 4]).shape == (3,)
assert np.allclose(pertumbuhan([10, 10]), [0.0])
"""),
            "Hitung np.diff lalu bagi dengan semua elemen kecuali yang terakhir.",
            G3.strip("\n"),
        ),
        E(
            "B1-04-2-ex4",
            "menantang",
            "Tulis fungsi `jumlah_bergerak(x, k)` yang mengembalikan, sebagai list Python, jumlah tiap jendela berukuran `k` yang bergeser satu langkah pada `x`, hanya untuk jendela yang penuh.",
            ind("""
import numpy as np

def jumlah_bergerak(x, k):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

assert jumlah_bergerak([1, 2, 3, 4, 5], 3) == [6.0, 9.0, 12.0]
assert jumlah_bergerak([1, 2, 3], 1) == [1.0, 2.0, 3.0]
assert jumlah_bergerak([2, 4, 6, 8], 2) == [6.0, 10.0, 14.0]
assert len(jumlah_bergerak(list(range(10)), 4)) == 7
"""),
            "Konvolusi dengan vektor satu dalam mode valid.",
            G4.strip("\n"),
        ),
    ],
    [
        M("Menulis axis terbalik.", "Axis nol per kolom, axis satu per baris."),
        M("Memakai mean biasa pada data bernan.", "Gunakan nanmean dan laporkan jumlah nan."),
        M("Mengira std membagi dengan n minus satu.", "Atur ddof=1 untuk sampel."),
    ],
    [
        Q("axis=0 pada matriks memberi?", ["Satu hasil per kolom", "Satu hasil per baris", "Satu skalar", "Matriks sama"], 0, "Baris diringkas.", hint="Kolom."),
        Q("cumsum menghasilkan?", ["Jumlah berjalan", "Total saja", "Selisih", "Rata-rata"], 0, "Per posisi.", hint="Berjalan."),
        Q("np.diff memberi?", ["Selisih bertetangga", "Jumlah", "Ragam", "Indeks"], 0, "Panjang berkurang satu.", hint="Selisih."),
        Q("Satu nan pada sum menghasilkan?", ["nan", "0", "Galat", "Nilai lain"], 0, "Mencemari.", hint="nan."),
        Q("ddof=1 mengubah?", ["Pembagi menjadi n minus satu", "Sumbu", "Tipe", "Urutan"], 0, "Ragam sampel.", hint="Sampel."),
    ],
    [
        "Axis menyatakan sumbu yang diringkas dan lenyap dari hasil.",
        "cumsum, cumprod, dan diff menangani nilai berjalan dan selisih.",
        "reduce dan accumulate menggeneralisasi ringkasan untuk ufunc apa pun.",
        "Fungsi nan mengabaikan nilai hilang, tetapi laporkan jumlahnya.",
    ],
    [],
)

H1 = """
import numpy as np

def batas_bawah(x, b):
    return np.maximum(x, b).tolist()
"""
H2 = """
import numpy as np

def hampir_sama(a, b):
    return bool(np.allclose(a, b))
"""
H3 = """
import numpy as np

def kategori(x):
    x = np.asarray(x)
    return np.select([x < 5, x < 10], [0, 1], default=2).tolist()
"""
H4 = """
import numpy as np

def maks_berjalan(x):
    return np.maximum.accumulate(x).tolist()
"""

l3 = lesson(
    "B1-04-3",
    "Ufunc biner, perbandingan, dan kontrol kondisi",
    35,
    [
        "Memakai maximum, minimum, dan clip elemen demi elemen",
        "Membandingkan desimal dengan isclose dan allclose",
        "Memilih nilai bertingkat dengan select",
        "Menggabungkan ufunc logika dan kumulatif",
    ],
    [
        tb("Ufunc dengan dua masukan", "Banyak ufunc menerima dua array dan menggabungkannya elemen demi elemen sesuai aturan broadcasting. Penjumlahan dan perkalian adalah contoh yang sudah dikenal. Pasangan yang berguna untuk membatasi nilai adalah `np.maximum` dan `np.minimum`, yang mengambil yang lebih besar atau lebih kecil dari dua masukan per posisi. Berbeda dari `max` dan `min` biasa, keduanya tidak meringkas array menjadi satu nilai."),
        C(
            ind("""
import numpy as np

print(np.maximum([1, 5, 3], [4, 2, 6]).tolist())
print(np.minimum([1, 5, 3], 2).tolist())
print(np.clip([1, 5, 10], 2, 8).tolist())
print(int(np.max([1, 5, 3])))
print(np.maximum([1, 5, 3], 0).tolist())
"""),
            ind("""
[4, 5, 6]
[1, 2, 2]
[2, 5, 8]
5
[1, 5, 3]
"""),
            "Maximum membandingkan dua array per posisi, sedangkan max meringkas satu array menjadi satu nilai.",
            filename="maksimum_elemen.py",
        ),
        tb("Pembatasan nilai", "Untuk membatasi dari bawah, pakai `np.maximum(x, batas)`, dan dari atas `np.minimum(x, batas)`. Untuk dua sisi sekaligus, `np.clip(x, bawah, atas)` lebih ringkas. Operasi ini umum dipakai untuk memotong pencilan, menjaga probabilitas dalam rentang nol sampai satu, atau menghindari logaritma nol dengan menaikkan nilai ke angka kecil positif."),
        tb("Membandingkan desimal", "Bilangan desimal biner tidak mewakili banyak pecahan desimal dengan tepat, sehingga `0.1 + 0.2 == 0.3` bernilai salah. Jangan membandingkan hasil desimal dengan sama dengan. Gunakan `np.isclose` untuk perbandingan per elemen dan `np.allclose` untuk seluruh array, yang menerima toleransi relatif dan absolut. Dalam pengujian kode numerik, `allclose` adalah teman setia."),
        C(
            ind("""
import numpy as np

print(0.1 + 0.2 == 0.3)
print(bool(np.isclose(0.1 + 0.2, 0.3)))
print(bool(np.allclose([1, 2], [1.0000001, 2])))
print(bool(np.allclose([1, 2], [1.1, 2])))
print(np.isclose([1.0, 2.0], [1.0, 2.5]).tolist())
"""),
            ind("""
False
True
True
False
[True, False]
"""),
            "Perbandingan sama dengan pada desimal rapuh. Isclose dan allclose memakai toleransi.",
            filename="isclose_dasar.py",
        ),
        tb("Fungsi logika elemen", "Operasi logika memiliki padanan ufunc: `np.logical_and`, `np.logical_or`, `np.logical_not`, dan `np.logical_xor`. Mereka setara dengan operator `&`, `|`, dan `~` pada array boolean, tetapi lebih jelas terbaca dan tidak peka pada tanda kurung. Karena merupakan ufunc, mereka mendukung `reduce`, sehingga `np.logical_and.reduce` menyatakan semuanya benar dan `np.logical_or.reduce` menyatakan adakah yang benar."),
        tb("Pilihan bertingkat dengan select", "Fungsi `np.where` hanya memilih antara dua nilai. Untuk banyak kategori, `np.select(daftar_syarat, daftar_nilai, default)` memeriksa syarat berurutan dan memakai nilai pertama yang cocok, dengan default untuk sisanya. Ini versi vectorized dari rantai if, elif, dan else, dan sangat berguna untuk mengelompokkan nilai kontinu ke dalam kategori."),
        C(
            ind("""
import numpy as np

x = np.array([1., 4., 9., 16.])
print(np.select([x < 5, x < 10], [0, 1], default=2).tolist())
print(np.logical_and([True, False], [True, True]).tolist())
print(np.logical_not([True, False]).tolist())
print(bool(np.logical_or.reduce([False, False, True])))
print(bool(np.logical_and.reduce([True, True])))
"""),
            ind("""
[0, 0, 1, 2]
[True, False]
[False, True]
True
True
"""),
            "Select memilih nilai dari syarat pertama yang cocok, dan reduce dengan fungsi logika merangkum mask.",
            filename="select_logika.py",
        ),
        tb("Parameter out", "Menulis hasil ufunc ke array yang sudah ada dengan `out` menghemat alokasi memori. Untuk pembaruan berulang pada array besar, misalnya `np.add(a, b, out=a)`, tidak ada array baru yang dibuat. Namun array `out` harus berbentuk dan bertipe yang sesuai, dan menimpa masukan sendiri hanya aman untuk operasi elemen demi elemen. Gunakan fitur ini bila profil menunjukkan memori jadi masalah."),
        tb("Maksimum berjalan", "Menggabungkan `accumulate` dengan ufunc biner menghasilkan ringkasan berjalan khusus. `np.maximum.accumulate` memberi nilai tertinggi sejauh ini, berguna untuk menghitung rekor atau penurunan dari puncak pada deret harga. `np.logical_or.accumulate` memberi penanda apakah suatu kejadian sudah terjadi sampai titik tersebut. Pola ini menyederhanakan banyak perulangan berurutan."),
        tb("Penurunan dari puncak", "Contoh nyata: penurunan maksimum dalam deret nilai portofolio. Hitung puncak berjalan dengan `np.maximum.accumulate`, lalu selisih relatif antara nilai dan puncak berjalan menunjukkan seberapa jauh turun dari rekor sebelumnya. Nilai terkecil dari selisih itu adalah penurunan maksimum. Seluruh perhitungan hanya beberapa baris tanpa perulangan."),
        tb("Ringkasan modul", "Anda telah belajar bahwa ufunc menerapkan fungsi elemen demi elemen, agregasi meringkas sepanjang sumbu, dan ufunc biner serta fungsi logika memberi kendali kondisi. Dengan toleransi pada perbandingan desimal dan kewaspadaan terhadap nan dan inf, Anda siap menulis perhitungan numerik yang cepat dan benar. Modul berikutnya masuk ke aljabar linear."),
        K("warn", "Jangan membandingkan hasil desimal dengan sama dengan. Pakai isclose atau allclose dengan toleransi.", title="Perbandingan desimal"),
        tb("Tabel kebenaran", "Fungsi `np.any` dan `np.all` dapat dipakai per sumbu, sehingga `mask.all(axis=1)` menyatakan baris mana yang seluruh syaratnya terpenuhi. Pola ini umum untuk menyaring baris yang tidak punya nilai hilang: `~np.isnan(X).any(axis=1)` memilih baris lengkap. Hasilnya adalah mask satu dimensi yang dapat langsung dipakai untuk menyaring matriks."),
        tb("Menguji kode numerik", "Saat menguji fungsi numerik, bandingkan hasilnya dengan jawaban yang dihitung tangan menggunakan `allclose`, dan sertakan kasus tepi seperti array kosong, satu elemen, nilai negatif, dan nan. Menulis uji sebelum kode membantu memperjelas harapan. Uji yang baik menangkap perubahan perilaku halus ketika Anda mengoptimalkan kode menjadi versi vectorized."),
        tb("Memilih fungsi yang tepat", "Bila menghadapi masalah baru, tanyakan tiga hal berurutan. Apakah ada ufunc untuk operasi ini? Apakah ini ringkasan atau kumulatif yang dapat diberi sumbu? Apakah kondisinya dapat dinyatakan dengan mask atau select? Dengan tiga pertanyaan itu sebagian besar perhitungan dapat ditulis tanpa perulangan Python."),
        E(
            "B1-04-3-ex1",
            "mudah",
            "Tulis fungsi `batas_bawah(x, b)` yang mengembalikan, sebagai list Python, nilai `x` yang dinaikkan menjadi `b` bila lebih kecil dari `b`.",
            ind("""
import numpy as np

def batas_bawah(x, b):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

assert batas_bawah([1, 5, 3], 2) == [2, 5, 3]
assert batas_bawah([-1, -2], 0) == [0, 0]
assert batas_bawah(np.array([4, 9]), 1) == [4, 9]
assert batas_bawah([], 0) == []
"""),
            "np.maximum membandingkan per elemen.",
            H1.strip("\n"),
        ),
        E(
            "B1-04-3-ex2",
            "sedang",
            "Tulis fungsi `hampir_sama(a, b)` yang mengembalikan `True` bila semua pasangan elemen `a` dan `b` hampir sama menurut toleransi bawaan NumPy, dan `False` bila tidak, sebagai bool Python.",
            ind("""
import numpy as np

def hampir_sama(a, b):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

assert hampir_sama([0.1 + 0.2], [0.3]) is True
assert hampir_sama([1, 2], [1.1, 2]) is False
assert hampir_sama(np.array([1.0, 2.0]), np.array([1.0000001, 2.0])) is True
assert hampir_sama([1.0], [2.0]) is False
"""),
            "np.allclose lalu ubah ke bool Python.",
            H2.strip("\n"),
        ),
        E(
            "B1-04-3-ex3",
            "sedang",
            "Tulis fungsi `kategori(x)` yang mengembalikan list kode kategori untuk tiap elemen: 0 bila kurang dari 5, 1 bila kurang dari 10, dan 2 untuk lainnya.",
            ind("""
import numpy as np

def kategori(x):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

assert kategori([1, 4, 9, 16]) == [0, 0, 1, 2]
assert kategori([5, 10]) == [1, 2]
assert kategori([4.99, 9.99, 10.0]) == [0, 1, 2]
assert kategori([]) == []
"""),
            "np.select dengan dua syarat berurutan dan default dua.",
            H3.strip("\n"),
        ),
        E(
            "B1-04-3-ex4",
            "menantang",
            "Tulis fungsi `maks_berjalan(x)` yang mengembalikan, sebagai list Python, nilai tertinggi yang pernah muncul sampai tiap posisi pada `x`, tanpa perulangan Python.",
            ind("""
import numpy as np

def maks_berjalan(x):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

assert maks_berjalan([1, 3, 2, 5, 4]) == [1, 3, 3, 5, 5]
assert maks_berjalan([5, 4, 3]) == [5, 5, 5]
assert maks_berjalan([1, 2, 3]) == [1, 2, 3]
assert maks_berjalan(np.array([2.0, 1.0])) == [2.0, 2.0]
"""),
            "np.maximum.accumulate.",
            H4.strip("\n"),
        ),
    ],
    [
        M("Membandingkan desimal dengan sama dengan.", "Pakai isclose atau allclose."),
        M("Memakai max padahal butuh perbandingan per elemen.", "Pakai np.maximum untuk dua array."),
        M("Menulis rantai if untuk kategori.", "Pakai np.select."),
    ],
    [
        Q("np.maximum(a, b) melakukan?", ["Perbandingan per elemen", "Ringkasan satu nilai", "Pengurutan", "Penjumlahan"], 0, "Elemen demi elemen.", hint="Per posisi."),
        Q("Membandingkan desimal sebaiknya dengan?", ["np.isclose", "==", "is", "in"], 0, "Toleransi.", hint="Dekat."),
        Q("np.select dipakai untuk?", ["Banyak kategori bersyarat", "Mengurutkan", "Mengiris", "Menyalin"], 0, "If elif vectorized.", hint="Bertingkat."),
        Q("np.maximum.accumulate memberi?", ["Maksimum berjalan", "Total", "Rata-rata", "Posisi"], 0, "Sejauh ini.", hint="Berjalan."),
        Q("np.logical_or.reduce menyatakan?", ["Adakah yang benar", "Semuanya benar", "Jumlah", "Posisi"], 0, "Atau terlipat.", hint="Ada."),
    ],
    [
        "maximum, minimum, dan clip membatasi nilai per elemen.",
        "isclose dan allclose membandingkan desimal dengan toleransi.",
        "np.select menangani banyak kategori bersyarat.",
        "accumulate dengan ufunc biner menghasilkan ringkasan berjalan.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perintah yang cukup jelas dalam teks.", "brief": []}

write_module(
    "B1",
    4,
    "Operasi vectorized dan ufunc",
    105,
    [
        "Menerapkan ufunc dan menangani nilai khusus",
        "Meringkas dan menghitung kumulatif sepanjang sumbu",
        "Mengendalikan kondisi dan membandingkan desimal dengan benar",
    ],
    [l1, l2, l3],
    video,
    REF,
)
