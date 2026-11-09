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


INFO = """
import numpy as np

def info_array(a):
    return (a.shape, a.ndim, a.size, str(a.dtype))
"""
SKALA = """
import numpy as np

def identitas_skala(n, k):
    return k * np.eye(n)
"""
TITIK = """
import numpy as np

def titik_seragam(a, b, n):
    return np.linspace(a, b, n)
"""
JENIS = """
import numpy as np

def jenis_hasil(daftar):
    return str(np.array(daftar).dtype)
"""

l1 = lesson(
    "B1-01-1",
    "Mengenal ndarray",
    35,
    [
        "Menjelaskan mengapa NumPy lebih cocok daripada list untuk data numerik",
        "Membuat array dari list dan dengan fungsi pembuat",
        "Membaca atribut shape, ndim, size, dan dtype",
        "Memilih fungsi pembuat array yang tepat",
    ],
    [
        tb("Mengapa NumPy", "Python menyediakan list untuk menyimpan banyak nilai, tetapi list dirancang serbaguna, bukan cepat. Setiap elemen adalah objek Python lengkap dengan tipe dan penghitung referensi, dan elemen tersebar di memori. NumPy menyediakan **ndarray**, yaitu larik berdimensi banyak yang menyimpan nilai bertipe sama secara berurutan di memori. Susunan ini membuat perhitungan jauh lebih cepat dan hemat memori, dan menjadi fondasi hampir seluruh ekosistem data science Python seperti pandas, scikit-learn, dan matplotlib."),
        tb("Dua sifat utama", "Ndarray punya dua sifat yang membedakannya dari list. Pertama, **homogen**: semua elemen bertipe sama, misalnya semuanya bilangan bulat atau semuanya desimal. Kedua, **berbentuk tetap**: ukurannya ditentukan saat dibuat dan menyatakan jumlah elemen pada tiap sumbu. Karena tipe dan bentuk diketahui, NumPy dapat menjalankan operasi massal dalam kode C yang dioptimalkan tanpa memeriksa tipe elemen satu per satu."),
        tb("Membuat array dari list", "Cara paling langsung membuat array adalah `np.array` yang menerima list. List bersarang menghasilkan array berdimensi lebih tinggi: list berisi angka menjadi vektor satu dimensi, list berisi list berukuran sama menjadi matriks dua dimensi. Konvensi impor yang dipakai di seluruh dunia adalah `import numpy as np`, jadi kita akan menulis `np.` di depan semua fungsi NumPy."),
        C(
            ind("""
import numpy as np

a = np.array([[1, 2, 3], [4, 5, 6]])
print(a.shape)
print(a.ndim)
print(a.size)
print(a.dtype)
print(a.tolist())
"""),
            ind("""
(2, 3)
2
6
int64
[[1, 2, 3], [4, 5, 6]]
"""),
            "Matriks dua baris tiga kolom punya shape (2, 3), dua dimensi, enam elemen, dan tipe bilangan bulat.",
            filename="array_dasar.py",
        ),
        tb("Membaca atribut array", "Empat atribut perlu dihafal. `shape` adalah tuple jumlah elemen tiap sumbu. `ndim` adalah jumlah sumbu, sama dengan panjang shape. `size` adalah jumlah seluruh elemen, hasil kali isi shape. `dtype` adalah tipe data elemen. Bila ragu tentang bentuk data saat debugging, hampir selalu jawabannya ada pada empat atribut ini, jadi biasakan mencetaknya lebih dulu sebelum menduga-duga."),
        tb("Fungsi pembuat array", "Menulis semua nilai dengan tangan tidak praktis. NumPy menyediakan `np.zeros` dan `np.ones` untuk array berisi nol atau satu, `np.full` untuk nilai tetap lain, `np.eye` untuk matriks identitas, `np.arange` untuk deret dengan langkah, dan `np.linspace` untuk sejumlah titik yang tersebar rata. Semuanya menerima shape atau parameter rentang, dan hasilnya langsung siap dipakai untuk perhitungan."),
        C(
            ind("""
import numpy as np

print(np.arange(0, 10, 3).tolist())
print(np.linspace(0, 1, 5).tolist())
print(np.eye(2).tolist())
print(np.full((2, 2), 7).tolist())
print(np.zeros(3).dtype)
"""),
            ind("""
[0, 3, 6, 9]
[0.0, 0.25, 0.5, 0.75, 1.0]
[[1.0, 0.0], [0.0, 1.0]]
[[7, 7], [7, 7]]
float64
"""),
            "Arange memakai langkah, linspace memakai jumlah titik dan menyertakan ujung akhir, dan zeros menghasilkan desimal secara bawaan.",
            filename="pembuat_array.py",
        ),
        tb("arange dan linspace", "Dua fungsi ini sering tertukar. `np.arange(awal, akhir, langkah)` mengikuti aturan `range`: ujung akhir tidak termasuk dan Anda mengatur selisih antar elemen. `np.linspace(awal, akhir, n)` menyertakan ujung akhir dan Anda mengatur jumlah titik, selisihnya dihitung otomatis. Gunakan arange untuk indeks dan hitungan bulat, dan linspace untuk sumbu grafik atau grid nilai kontinu."),
        tb("Tipe yang dipilih otomatis", "Saat membuat array dari list, NumPy memilih tipe yang dapat menampung semua elemen. List bilangan bulat menjadi `int64`, campuran bulat dan desimal menjadi `float64`, dan campuran angka dengan teks menjadi tipe teks sehingga angkanya berubah jadi string. Perilaku terakhir sering mengejutkan, karena satu elemen teks cukup untuk mengubah seluruh array dan merusak perhitungan berikutnya."),
        C(
            ind("""
import numpy as np

print(np.array([1, 2, 3]).dtype)
print(np.array([1, 2.5]).dtype)
print(np.array([True, 2]).dtype)
print(np.array([1, 'a']).dtype.kind)
"""),
            ind("""
int64
float64
int64
U
"""),
            "Tipe hasil mengikuti elemen paling umum. Campuran angka dan teks berakhir sebagai tipe teks berkode U.",
            filename="tipe_otomatis.py",
        ),
        tb("Array dan list tidak sama", "Operator pada array bekerja elemen demi elemen, sedangkan pada list bekerja pada seluruh objek. Menambah dua list menyambungkannya, tetapi menambah dua array menjumlahkan pasangan elemen. Mengalikan list dengan 2 menggandakan isinya, sedangkan mengalikan array dengan 2 menggandakan tiap nilai. Perbedaan ini adalah alasan utama NumPy terasa seperti matematika, dan dibahas penuh pada modul operasi vectorized."),
        tb("Kapan memilih NumPy", "Gunakan ndarray bila data numerik dalam jumlah besar dan diproses dengan rumus yang sama pada semua elemen, seperti sensor, piksel gambar, atau fitur model. Tetap pakai list bila isi data beragam tipe atau jumlahnya kecil dan sering bertambah. Menambah elemen ke array berarti membuat array baru, sehingga list lebih cocok untuk pengumpulan data yang terus tumbuh."),
        K("tip", "Setiap kali menerima array dari pihak lain, cetak shape dan dtype lebih dulu. Dua atribut itu menjawab sebagian besar kebingungan.", title="Kebiasaan debugging"),
        tb("Array kosong dan ukuran nol", "Array boleh berukuran nol, misalnya `np.zeros(0)`, dan semua atributnya tetap valid: shape berisi nol dan size nol. Kasus ini muncul saat penyaringan tidak menyisakan data, jadi kode yang baik tidak boleh mengasumsikan array selalu berisi. Periksa size sebelum mengambil elemen pertama atau menghitung rata-rata agar program tidak gagal diam-diam."),
        E(
            "B1-01-1-ex1",
            "mudah",
            "Tulis fungsi `info_array(a)` yang mengembalikan tuple `(shape, ndim, size, nama_dtype)` dari array `a`, dengan nama dtype berupa string.",
            ind("""
import numpy as np

def info_array(a):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

a = np.array([[1, 2, 3], [4, 5, 6]])
assert info_array(a) == ((2, 3), 2, 6, 'int64')
assert info_array(np.zeros(4)) == ((4,), 1, 4, 'float64')
assert info_array(np.ones((2, 1, 3))) == ((2, 1, 3), 3, 6, 'float64')
assert info_array(np.array([True, False])) == ((2,), 1, 2, 'bool')
"""),
            "Kembalikan atribut shape, ndim, size, dan str(dtype) dalam satu tuple.",
            INFO.strip("\n"),
        ),
        E(
            "B1-01-1-ex2",
            "sedang",
            "Tulis fungsi `identitas_skala(n, k)` yang mengembalikan array persegi berukuran `n` kali `n` dengan nilai `k` pada diagonal dan nol di tempat lain.",
            ind("""
import numpy as np

def identitas_skala(n, k):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

assert identitas_skala(2, 5).tolist() == [[5.0, 0.0], [0.0, 5.0]]
assert identitas_skala(3, 1).shape == (3, 3)
assert identitas_skala(3, 2).sum() == 6
assert identitas_skala(1, 9).tolist() == [[9.0]]
"""),
            "Kalikan np.eye(n) dengan k.",
            SKALA.strip("\n"),
        ),
        E(
            "B1-01-1-ex3",
            "sedang",
            "Tulis fungsi `titik_seragam(a, b, n)` yang mengembalikan array berisi `n` titik berjarak sama dari `a` sampai `b` inklusif.",
            ind("""
import numpy as np

def titik_seragam(a, b, n):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

assert titik_seragam(0, 1, 5).tolist() == [0.0, 0.25, 0.5, 0.75, 1.0]
assert titik_seragam(1, 2, 3).tolist() == [1.0, 1.5, 2.0]
assert titik_seragam(0, 10, 5).shape == (5,)
assert titik_seragam(5, 5, 3).tolist() == [5.0, 5.0, 5.0]
"""),
            "linspace menyertakan ujung akhir.",
            TITIK.strip("\n"),
        ),
        E(
            "B1-01-1-ex4",
            "menantang",
            "Tulis fungsi `jenis_hasil(daftar)` yang mengembalikan nama dtype (string) dari array yang dibuat dari list `daftar` oleh NumPy.",
            ind("""
import numpy as np

def jenis_hasil(daftar):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

assert jenis_hasil([1, 2, 3]) == 'int64'
assert jenis_hasil([1, 2.5]) == 'float64'
assert jenis_hasil([True, False]) == 'bool'
assert jenis_hasil([[1, 2], [3, 4.0]]) == 'float64'
"""),
            "Buat array lalu ubah dtype-nya menjadi string.",
            JENIS.strip("\n"),
        ),
    ],
    [
        M("Mencampur teks dan angka dalam satu array.", "Pisahkan, atau ubah tipe lebih dulu agar angkanya tetap numerik."),
        M("Mengira arange menyertakan ujung akhir.", "Arange tidak menyertakan, linspace menyertakan."),
        M("Menebak bentuk data.", "Cetak shape dan dtype."),
    ],
    [
        Q("Sifat utama ndarray?", ["Homogen dan berbentuk tetap", "Boleh campur tipe", "Selalu satu dimensi", "Hanya teks"], 0, "Semua elemen sama tipe.", hint="Homogen."),
        Q("Shape (2, 3) berarti?", ["Dua baris tiga kolom", "Tiga baris dua kolom", "Enam dimensi", "Dua elemen"], 0, "Urutan sumbu.", hint="Baris dulu."),
        Q("Size array shape (2, 3)?", ["6", "5", "2", "3"], 0, "Hasil kali shape.", hint="Kalikan."),
        Q("Fungsi dengan ujung akhir termasuk?", ["linspace", "arange", "range", "zeros"], 0, "Titik seragam inklusif.", hint="Titik."),
        Q("np.array([1, 2.5]) bertipe?", ["float64", "int64", "bool", "str"], 0, "Tipe paling umum.", hint="Desimal."),
    ],
    [
        "Ndarray homogen dan berbentuk tetap sehingga cepat.",
        "Atribut shape, ndim, size, dan dtype menjelaskan array.",
        "zeros, ones, full, eye, arange, dan linspace membuat array tanpa menulis nilai.",
        "Tipe array dipilih otomatis dari elemennya.",
    ],
    [],
)

UINT = """
import numpy as np

def ke_uint8(daftar):
    return np.array(daftar).astype(np.uint8).tolist()
"""
MEM = """
import numpy as np

def hemat_memori(a):
    return a.astype(np.float32).nbytes
"""
PANGKAS = """
import numpy as np

def pangkas_int(a):
    return a.astype(int).tolist()
"""
HASIL = """
import numpy as np

def dtype_hasil(a, b):
    return str(np.result_type(a, b))
"""

l2 = lesson(
    "B1-01-2",
    "dtype dan konversi tipe",
    35,
    [
        "Menjelaskan dtype dan ukurannya di memori",
        "Mengonversi tipe dengan astype dan memahami risikonya",
        "Memahami overflow pada bilangan bulat berukuran tetap",
        "Memprediksi tipe hasil operasi campuran",
    ],
    [
        tb("Tipe data dalam array", "Setiap array punya satu **dtype** yang menentukan cara membaca byte di memori. Tipe bilangan bulat berbertanda ditulis `int8`, `int16`, `int32`, `int64`, dan angka di belakangnya adalah jumlah bit. Versi tak bertanda diawali `u` seperti `uint8`. Desimal memakai `float16`, `float32`, `float64`, dan nilai logika memakai `bool`. Pilihan tipe memengaruhi rentang nilai, ketelitian, dan memori yang terpakai."),
        tb("Memori yang terpakai", "Atribut `itemsize` memberi jumlah byte per elemen dan `nbytes` memberi total byte seluruh array, yaitu size dikali itemsize. Array berisi satu juta bilangan `float64` memakai delapan megabyte, sedangkan versi `float32` hanya empat megabyte. Untuk gambar dan data sensor yang besar, memilih tipe lebih kecil dapat menghemat memori secara berarti asalkan rentang dan ketelitiannya masih cukup."),
        C(
            ind("""
import numpy as np

a = np.array([[1, 2, 3], [4, 5, 6]])
print(a.itemsize)
print(a.nbytes)
b = a.astype(np.int8)
print(b.itemsize, b.nbytes)
print(np.zeros((3, 4), dtype=np.float32).nbytes)
"""),
            ind("""
8
48
1 6
48
"""),
            "Enam elemen int64 memakai empat puluh delapan byte, tetapi int8 hanya enam. Array nol float32 berukuran tiga kali empat memakai empat puluh delapan byte.",
            filename="memori_dtype.py",
        ),
        tb("Mengubah tipe dengan astype", "Metode `astype` membuat array baru dengan tipe yang diminta, array asli tidak berubah. Mengubah bilangan bulat menjadi desimal aman. Mengubah desimal menjadi bilangan bulat memotong bagian pecahan menuju nol, bukan membulatkan, sehingga 1,9 menjadi 1 dan minus 1,9 menjadi minus 1. Bila ingin pembulatan, panggil `np.round` lebih dulu sebelum konversi."),
        C(
            ind("""
import numpy as np

x = np.array([[1.5, -2.7], [3.2, 0.9]])
print(x.astype(int).tolist())
print(np.round(x).astype(int).tolist())
print(x.dtype)
y = np.array([1, 2, 3]).astype(float)
print(y.dtype, y.tolist())
"""),
            ind("""
[[1, -2], [3, 0]]
[[2, -3], [3, 1]]
float64
float64 [1.0, 2.0, 3.0]
"""),
            "Konversi ke bilangan bulat memotong menuju nol. Pembulatan lebih dulu memberi hasil berbeda, dan array asli tetap float64.",
            filename="astype_dasar.py",
        ),
        tb("Overflow diam-diam", "Bilangan bulat berukuran tetap punya rentang terbatas. Tipe `uint8` hanya menampung nol sampai 255 dan `int8` hanya minus 128 sampai 127. Mengonversi nilai di luar rentang tidak menimbulkan galat, nilainya melilit begitu saja seperti odometer. Itu sebabnya 300 menjadi 44 pada `uint8` dan 200 menjadi minus 56 pada `int8`. Galat senyap ini berbahaya karena hasilnya tampak wajar."),
        C(
            ind("""
import numpy as np

print(np.array([300, -1, 5]).astype(np.uint8).tolist())
print(np.array([200]).astype(np.int8).tolist())
print(np.iinfo(np.uint8).max, np.iinfo(np.int8).min)
print(np.finfo(np.float32).eps > np.finfo(np.float64).eps)
"""),
            ind("""
[44, 255, 5]
[-56]
255 -128
True
"""),
            "Nilai di luar rentang melilit tanpa peringatan. Rentang dan ketelitian tiap tipe dapat ditanyakan lewat iinfo dan finfo.",
            filename="overflow_tipe.py",
        ),
        tb("Memeriksa rentang", "Fungsi `np.iinfo` melaporkan nilai minimum dan maksimum tipe bilangan bulat, dan `np.finfo` melaporkan ketelitian tipe desimal, misalnya `eps` yang merupakan selisih terkecil di dekat angka satu. Periksa rentang sebelum mengecilkan tipe. Pada pengolahan gambar, data piksel memang `uint8`, tetapi hitungan di atasnya sebaiknya dilakukan pada `float` lalu dikembalikan di akhir."),
        tb("Ketelitian desimal", "Tipe `float32` menyimpan sekitar tujuh digit penting dan `float64` sekitar enam belas. Angka 0,1 tidak dapat dinyatakan persis dalam biner, dan kesalahan itu lebih besar pada `float32`. Untuk perhitungan statistik dan model, `float64` adalah pilihan aman. Gunakan `float32` bila memori atau kecepatan pada GPU lebih penting dan ketelitian tujuh digit sudah cukup."),
        tb("Tipe hasil operasi campuran", "Ketika dua array bertipe berbeda dioperasikan, NumPy menaikkan ke tipe yang dapat memuat keduanya, disebut **type promotion**. `int8` dengan `int32` menghasilkan `int32`. `int64` dengan `float32` menghasilkan `float64`. `uint8` dengan `int8` menghasilkan `int16` karena tidak ada tipe 8 bit yang memuat keduanya. Fungsi `np.result_type` memberi tahu hasilnya tanpa menjalankan operasi."),
        C(
            ind("""
import numpy as np

print(np.result_type('int8', 'int32'))
print(np.result_type('int64', 'float32'))
print(np.result_type('uint8', 'int8'))
print((np.array([1, 2, 3]) / 2).tolist())
print((np.array([1, 2, 3]) // 2).dtype)
"""),
            ind("""
int32
float64
int16
[0.5, 1.0, 1.5]
int64
"""),
            "Promosi tipe memilih tipe terkecil yang memuat keduanya. Pembagian biasa selalu menghasilkan desimal, pembagian lantai mempertahankan bilangan bulat.",
            filename="promosi_tipe.py",
        ),
        tb("Mengatur dtype saat membuat", "Daripada membuat array lalu mengonversinya, tetapkan tipe sejak awal dengan argumen `dtype`, misalnya `np.zeros(3, dtype=int)` atau `np.array([1, 2], dtype=np.float32)`. Cara ini menghindari salinan sementara dan menjelaskan maksud kode. Untuk data dengan nilai kosong, ingat bahwa bilangan bulat tidak punya nilai NaN, jadi data demikian harus bertipe desimal."),
        K("warn", "Mengonversi ke tipe yang lebih kecil dapat melilitkan nilai tanpa galat. Periksa rentang dengan iinfo sebelum mengecilkan tipe.", title="Overflow senyap"),
        tb("Memilih tipe untuk gambar", "Gambar berwarna biasanya `uint8` dengan nilai nol sampai 255 per kanal. Bila Anda menambah kecerahan langsung pada `uint8`, nilai di atas 255 melilit menjadi gelap. Ubah ke `float` dulu, lakukan perhitungan, batasi nilai dengan `np.clip`, lalu kembalikan ke `uint8`. Pola tiga langkah ini adalah praktik standar pengolahan citra."),
        tb("Tipe bool dan hitungan", "Array `bool` memakai satu byte per elemen dan berperan sebagai mask pada modul berikutnya. Menjumlahkan array bool menghitung jumlah True karena True dianggap satu dan False dianggap nol. Trik ini sering dipakai untuk menghitung berapa elemen memenuhi syarat tanpa perulangan, dan hasilnya bertipe bilangan bulat."),
        E(
            "B1-01-2-ex1",
            "mudah",
            "Tulis fungsi `ke_uint8(daftar)` yang mengubah list bilangan menjadi array lalu mengonversinya ke `uint8` dan mengembalikannya sebagai list Python.",
            ind("""
import numpy as np

def ke_uint8(daftar):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

assert ke_uint8([1, 2, 3]) == [1, 2, 3]
assert ke_uint8([300, -1, 5]) == [44, 255, 5]
assert ke_uint8([256]) == [0]
assert ke_uint8([]) == []
"""),
            "Gunakan astype(np.uint8) lalu tolist.",
            UINT.strip("\n"),
        ),
        E(
            "B1-01-2-ex2",
            "sedang",
            "Tulis fungsi `hemat_memori(a)` yang mengembalikan jumlah byte yang dipakai array `a` bila dikonversi ke `float32`.",
            ind("""
import numpy as np

def hemat_memori(a):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

assert hemat_memori(np.zeros((3, 4))) == 48
assert hemat_memori(np.arange(10)) == 40
assert hemat_memori(np.zeros(0)) == 0
assert hemat_memori(np.ones((2, 2), dtype=np.int8)) == 16
"""),
            "Konversi dengan astype lalu baca nbytes.",
            MEM.strip("\n"),
        ),
        E(
            "B1-01-2-ex3",
            "sedang",
            "Tulis fungsi `pangkas_int(a)` yang mengonversi array desimal `a` ke bilangan bulat dengan memotong pecahan, lalu mengembalikannya sebagai list Python.",
            ind("""
import numpy as np

def pangkas_int(a):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

assert pangkas_int(np.array([1.9, -1.9])) == [1, -1]
assert pangkas_int(np.array([[1.5, -2.7], [3.2, 0.9]])) == [[1, -2], [3, 0]]
assert pangkas_int(np.array([2.0])) == [2]
assert pangkas_int(np.array([0.99])) == [0]
"""),
            "astype(int) memotong menuju nol.",
            PANGKAS.strip("\n"),
        ),
        E(
            "B1-01-2-ex4",
            "menantang",
            "Tulis fungsi `dtype_hasil(a, b)` yang menerima dua nama tipe (string) dan mengembalikan nama tipe hasil bila keduanya dioperasikan, dalam bentuk string.",
            ind("""
import numpy as np

def dtype_hasil(a, b):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

assert dtype_hasil('int8', 'int32') == 'int32'
assert dtype_hasil('int64', 'float32') == 'float64'
assert dtype_hasil('uint8', 'int8') == 'int16'
assert dtype_hasil('float32', 'float64') == 'float64'
"""),
            "np.result_type menerima nama tipe.",
            HASIL.strip("\n"),
        ),
    ],
    [
        M("Mengira astype membulatkan.", "astype memotong menuju nol, bulatkan dulu dengan np.round."),
        M("Mengecilkan tipe tanpa memeriksa rentang.", "Cek dengan np.iinfo sebelum konversi."),
        M("Memakai float32 untuk statistik teliti.", "Pakai float64 bila ketelitian penting."),
    ],
    [
        Q("nbytes sama dengan?", ["size dikali itemsize", "ndim dikali size", "shape pertama", "itemsize saja"], 0, "Total byte.", hint="Kali."),
        Q("astype(int) pada 1.9 menghasilkan?", ["1", "2", "1.9", "0"], 0, "Memotong.", hint="Potong."),
        Q("300 sebagai uint8 menjadi?", ["44", "255", "300", "galat"], 0, "Melilit.", hint="Lilit."),
        Q("int64 dan float32 menghasilkan?", ["float64", "int64", "float32", "int32"], 0, "Promosi tipe.", hint="Muat keduanya."),
        Q("Fungsi rentang bilangan bulat?", ["np.iinfo", "np.finfo", "np.size", "np.shape"], 0, "Informasi integer.", hint="i."),
    ],
    [
        "Dtype menentukan rentang, ketelitian, dan memori array.",
        "astype membuat salinan bertipe baru dan memotong pecahan.",
        "Overflow melilit nilai tanpa galat.",
        "Operasi campuran menaikkan ke tipe yang memuat keduanya.",
    ],
    [],
)

UBAH = """
import numpy as np

def ubah_bentuk(a, baris):
    return a.reshape(baris, -1).shape
"""
VERT = """
import numpy as np

def susun_vertikal(a, b):
    return np.vstack([a, b]).tolist()
"""
AMAN = """
import numpy as np

def salinan_aman(a):
    c = a.copy()
    c.flat[0] = 0
    return c
"""
VIEW = """
import numpy as np

def apakah_view(a, b):
    return bool(np.shares_memory(a, b))
"""

l3 = lesson(
    "B1-01-3",
    "Shape, reshape, dan view",
    35,
    [
        "Mengubah bentuk array dengan reshape, ravel, dan transpose",
        "Menggabungkan array dengan concatenate, vstack, hstack, dan stack",
        "Membedakan view dan salinan",
        "Menghindari bug akibat view yang memodifikasi data asal",
    ],
    [
        tb("Bentuk bisa diubah", "Data yang sama dapat dilihat dalam bentuk berbeda: dua belas angka bisa menjadi satu baris panjang, matriks tiga kali empat, atau tumpukan dua matriks tiga kali dua. Metode `reshape` mengubah shape selama jumlah elemen tetap. Salah satu ukuran boleh ditulis minus satu, dan NumPy menghitungnya otomatis dari ukuran lain. Ini sangat berguna ketika jumlah baris tidak diketahui sebelumnya."),
        C(
            ind("""
import numpy as np

a = np.arange(12)
print(a.reshape(3, 4).shape)
print(a.reshape(2, -1).shape)
print(a.reshape(2, 3, 2).shape)
try:
    a.reshape(5, 3)
except ValueError:
    print('ditolak')
"""),
            ind("""
(3, 4)
(2, 6)
(2, 3, 2)
ditolak
"""),
            "Reshape menjaga jumlah elemen. Minus satu dihitung otomatis, dan bentuk yang tidak cocok ditolak dengan ValueError.",
            filename="reshape_dasar.py",
        ),
        tb("Urutan pengisian", "Secara bawaan reshape mengisi baris demi baris, disebut urutan C. Elemen nol sampai lima pada shape dua kali tiga menjadi baris pertama nol, satu, dua dan baris kedua tiga, empat, lima. Metode `ravel` dan `flatten` melakukan kebalikannya: meratakan array menjadi satu dimensi. Bedanya, `ravel` sebisa mungkin mengembalikan view sedangkan `flatten` selalu membuat salinan."),
        tb("Transpose dan sumbu", "Transpose menukar sumbu. Untuk matriks, `a.T` menukar baris dan kolom sehingga shape dua kali tiga menjadi tiga kali dua. Untuk array tiga dimensi, `transpose` menerima urutan sumbu baru, misalnya `transpose(2, 0, 1)` memindahkan sumbu terakhir ke depan. Menambah sumbu berukuran satu dengan `np.expand_dims` atau indeks `None` sering dibutuhkan agar array cocok untuk operasi, dan akan dipakai lagi pada broadcasting."),
        C(
            ind("""
import numpy as np

m = np.arange(6).reshape(2, 3)
print(m.T.shape)
print(m.ravel().tolist())
print(m.flatten('F').tolist())
v = np.array([1, 2, 3])
print(v[:, None].shape, np.expand_dims(v, 0).shape)
print(np.arange(24).reshape(2, 3, 4).transpose(2, 0, 1).shape)
"""),
            ind("""
(3, 2)
[0, 1, 2, 3, 4, 5]
[0, 3, 1, 4, 2, 5]
(3, 1) (1, 3)
(4, 2, 3)
"""),
            "Transpose menukar sumbu, ravel meratakan baris demi baris, dan urutan F meratakan kolom demi kolom.",
            filename="transpose_dasar.py",
        ),
        tb("Menggabungkan array", "Untuk menyambung array sepanjang sumbu yang ada, pakai `np.concatenate` dengan argumen `axis`. Singkatannya, `np.vstack` menumpuk secara vertikal dan `np.hstack` berdampingan secara horizontal. Untuk membuat sumbu baru, pakai `np.stack`, yang menumpuk array berbentuk sama sepanjang sumbu baru. Pada semua penggabungan, ukuran pada sumbu lain harus cocok, kalau tidak NumPy melaporkan galat."),
        C(
            ind("""
import numpy as np

a = [[1, 2], [3, 4]]
print(np.vstack([a, a]).shape)
print(np.hstack([a, a]).tolist())
print(np.stack([[1, 2], [3, 4]], axis=1).tolist())
print(np.concatenate([np.ones((2, 2)), np.zeros((1, 2))]).shape)
"""),
            ind("""
(4, 2)
[[1, 2, 1, 2], [3, 4, 3, 4]]
[[1, 3], [2, 4]]
(3, 2)
"""),
            "Vstack menumpuk baris, hstack menyambung kolom, dan stack membuat sumbu baru.",
            filename="gabung_array.py",
        ),
        tb("View dan salinan", "Banyak operasi NumPy mengembalikan **view**, yaitu array baru yang berbagi memori dengan aslinya, bukan salinan. Reshape, transpose, ravel, dan slicing biasa menghasilkan view. Karena memori dibagi, mengubah elemen lewat view ikut mengubah array asal. Perilaku ini hemat memori dan cepat, tetapi menjadi sumber bug klasik bila tidak disadari."),
        C(
            ind("""
import numpy as np

b = np.arange(6)
v = b.reshape(2, 3)
v[0, 0] = 99
print(b.tolist())
print(np.shares_memory(b, v))
c = b.copy()
c[0] = 0
print(b[0])
print(np.shares_memory(b, c))
"""),
            ind("""
[99, 1, 2, 3, 4, 5]
True
99
False
"""),
            "Mengubah view ikut mengubah array asal. Salinan lewat copy tidak berbagi memori.",
            filename="view_salinan.py",
        ),
        tb("Mendeteksi dan menghindari", "Fungsi `np.shares_memory` memberi tahu apakah dua array berbagi data. Slicing biasa dan transpose menghasilkan view, sedangkan indeks daftar atau mask boolean menghasilkan salinan. Bila perlu mengubah hasil tanpa memengaruhi asal, panggil `.copy()` secara eksplisit. Menulis `.copy()` di tempat yang tepat adalah cara termurah menghindari bug yang sulit ditelusuri."),
        K("warn", "Reshape, transpose, dan slicing biasa memberi view. Ubah hasilnya dan data asal ikut berubah, kecuali Anda memanggil copy lebih dulu.", title="Berbagi memori"),
        tb("Memilih antara ravel dan flatten", "Gunakan `ravel` bila hanya membaca atau bila Anda ingin menghemat memori, karena ia mengembalikan view bila memungkinkan. Gunakan `flatten` bila hasilnya akan diubah dan array asal harus aman, karena ia selalu menyalin. Kedua fungsi menghasilkan isi sama, jadi perbedaannya hanya pada berbagi memori dan biaya penyalinan."),
        tb("Memecah array", "Kebalikan penggabungan adalah pemecahan. Fungsi `np.split` memotong array menjadi bagian sama besar sepanjang suatu sumbu, dan `np.array_split` mengizinkan bagian tidak sama besar. Hasilnya berupa list array yang umumnya berupa view dari array asal. Pemecahan dipakai untuk membagi data menjadi lipatan validasi silang atau kelompok pemrosesan."),
        tb("Menambah dan membuang sumbu", "Selain expand_dims, `np.squeeze` membuang sumbu berukuran satu, misalnya shape tiga kali satu menjadi tiga. Pasangan ini penting saat menyiapkan masukan model yang menuntut jumlah dimensi tertentu, dan saat hasil fungsi membawa sumbu berlebih. Selalu periksa shape sesudahnya agar tidak ada dimensi yang tertukar tanpa disadari."),
        tb("Contiguous dan kecepatan", "Array menyimpan data berurutan di memori. Transpose tidak memindahkan data, hanya mengubah cara membacanya, sehingga hasilnya tidak lagi berurutan menurut barisnya. Operasi pada array tidak berurutan bisa lebih lambat. Bila perlu, `np.ascontiguousarray` membuat salinan berurutan. Untuk sebagian besar pemakaian Anda tidak perlu peduli, tetapi bagus mengetahui alasannya bila performa menurun."),
        tb("Urutan F dan C","Urutan C mengisi baris lebih dulu dan urutan F mengisi kolom lebih dulu, seperti pada bahasa Fortran dan R. Reshape dan ravel menerima argumen order untuk memilihnya. Bila data berasal dari sistem yang memakai urutan kolom, pilih order F agar elemen jatuh pada posisi yang benar. Kesalahan urutan tidak menimbulkan galat, hanya hasil yang tertukar, jadi uji dengan contoh kecil."),
        tb("Ringkasan pelajaran","Anda telah melihat cara menyusun ulang data tanpa mengubah isinya. Reshape, transpose, dan ravel mengubah sudut pandang, penggabungan menyatukan potongan, dan pemahaman tentang view melindungi data dari perubahan tidak sengaja. Kebiasaan memeriksa shape setelah setiap langkah akan menghemat banyak waktu pada modul berikutnya."),
        E(
            "B1-01-3-ex1",
            "mudah",
            "Tulis fungsi `ubah_bentuk(a, baris)` yang mengubah array `a` menjadi `baris` baris dengan jumlah kolom dihitung otomatis, lalu mengembalikan shape-nya.",
            ind("""
import numpy as np

def ubah_bentuk(a, baris):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

assert ubah_bentuk(np.arange(12), 3) == (3, 4)
assert ubah_bentuk(np.arange(12), 2) == (2, 6)
assert ubah_bentuk(np.arange(6), 6) == (6, 1)
assert ubah_bentuk(np.arange(10).reshape(2, 5), 5) == (5, 2)
"""),
            "reshape(baris, -1) lalu ambil shape.",
            UBAH.strip("\n"),
        ),
        E(
            "B1-01-3-ex2",
            "sedang",
            "Tulis fungsi `susun_vertikal(a, b)` yang menumpuk dua array secara vertikal dan mengembalikan hasilnya sebagai list Python.",
            ind("""
import numpy as np

def susun_vertikal(a, b):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

assert susun_vertikal([[1, 2]], [[3, 4]]) == [[1, 2], [3, 4]]
assert susun_vertikal(np.zeros((1, 2)), np.ones((2, 2))) == [[0.0, 0.0], [1.0, 1.0], [1.0, 1.0]]
assert susun_vertikal([1, 2], [3, 4]) == [[1, 2], [3, 4]]
assert np.array(susun_vertikal(np.ones((2, 3)), np.ones((2, 3)))).shape == (4, 3)
"""),
            "np.vstack menerima dua array dalam list.",
            VERT.strip("\n"),
        ),
        E(
            "B1-01-3-ex3",
            "sedang",
            "Tulis fungsi `salinan_aman(a)` yang mengembalikan salinan array `a` dengan elemen pertama (urutan ratakan) diubah menjadi nol, tanpa mengubah `a`.",
            ind("""
import numpy as np

def salinan_aman(a):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

a = np.array([5, 6, 7])
r = salinan_aman(a)
assert r.tolist() == [0, 6, 7]
assert a.tolist() == [5, 6, 7]
m = np.array([[1, 2], [3, 4]])
r2 = salinan_aman(m)
assert r2.tolist() == [[0, 2], [3, 4]]
assert m.tolist() == [[1, 2], [3, 4]]
assert np.shares_memory(m, r2) == False
"""),
            "Salin dulu, lalu ubah elemen pertama lewat flat.",
            AMAN.strip("\n"),
        ),
        E(
            "B1-01-3-ex4",
            "menantang",
            "Tulis fungsi `apakah_view(a, b)` yang mengembalikan `True` bila array `a` dan `b` berbagi memori, dan `False` bila tidak.",
            ind("""
import numpy as np

def apakah_view(a, b):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

a = np.arange(6)
assert apakah_view(a, a.reshape(2, 3)) is True
assert apakah_view(a, a.T) is True
assert apakah_view(a, a[::2]) is True
assert apakah_view(a, a.copy()) is False
assert apakah_view(a, a[[0, 1]]) is False
"""),
            "np.shares_memory memeriksa memori yang dibagi. Ubah ke bool murni.",
            VIEW.strip("\n"),
        ),
    ],
    [
        M("Mengubah hasil reshape lalu heran data asal berubah.", "Panggil copy bila butuh data terpisah."),
        M("Menyambung array dengan ukuran sumbu tidak cocok.", "Periksa shape lebih dulu."),
        M("Memakai reshape dengan jumlah elemen berbeda.", "Pastikan hasil kali shape sama dengan size."),
    ],
    [
        Q("Minus satu pada reshape berarti?", ["Dihitung otomatis", "Dibuang", "Dibalik", "Galat"], 0, "Ukuran dilengkapi.", hint="Otomatis."),
        Q("a.T pada shape (2, 3) menghasilkan?", ["(3, 2)", "(2, 3)", "(6,)", "(1, 6)"], 0, "Tukar sumbu.", hint="Tukar."),
        Q("Fungsi membuat sumbu baru saat menumpuk?", ["np.stack", "np.vstack", "np.ravel", "np.copy"], 0, "Sumbu baru.", hint="Stack."),
        Q("Reshape menghasilkan?", ["View", "Salinan selalu", "List", "Galat"], 0, "Berbagi memori.", hint="Bagi."),
        Q("Indeks daftar menghasilkan?", ["Salinan", "View", "Tuple", "Galat"], 0, "Fancy indexing menyalin.", hint="Salin."),
    ],
    [
        "Reshape mengubah bentuk tanpa mengubah jumlah elemen.",
        "Transpose menukar sumbu dan ravel meratakan array.",
        "concatenate, vstack, hstack, dan stack menggabungkan array.",
        "View berbagi memori, copy tidak.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perintah yang cukup jelas dalam teks.", "brief": []}

write_module(
    "B1",
    1,
    "ndarray, dtype, dan shape",
    105,
    [
        "Membuat array dan membaca atributnya",
        "Memilih dan mengonversi dtype dengan sadar risikonya",
        "Mengubah bentuk, menggabungkan, dan membedakan view dari salinan",
    ],
    [l1, l2, l3],
    video,
    REF,
)
