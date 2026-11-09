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

def bentuk_hasil(s1, s2):
    return np.broadcast_shapes(s1, s2)
"""
F2 = """
import numpy as np

def bisa_broadcast(s1, s2):
    try:
        np.broadcast_shapes(s1, s2)
        return True
    except ValueError:
        return False
"""
F3 = """
import numpy as np

def tabel_jumlah(kolom, baris):
    return (np.array(kolom)[:, None] + np.array(baris)).tolist()
"""
F4 = """
import numpy as np

def ulang_baris(v, n):
    return np.broadcast_to(v, (n, len(v))).copy()
"""

l1 = lesson(
    "B1-03-1",
    "Aturan broadcasting",
    35,
    [
        "Menjelaskan apa itu broadcasting dan mengapa berguna",
        "Menerapkan aturan penyelarasan shape dari kanan",
        "Memprediksi shape hasil dan mengenali galat",
        "Memakai broadcast_shapes dan broadcast_to",
    ],
    [
        tb("Operasi antar array berbeda bentuk", "Sejauh ini kita mengoperasikan array berbentuk sama atau array dengan satu skalar. Namun sering kita perlu mengurangi rata-rata kolom dari seluruh matriks, atau mengalikan tiap kolom dengan bobot berbeda. Menulis perulangan untuk itu lambat dan panjang. **Broadcasting** adalah aturan NumPy yang memungkinkan array berbeda bentuk dioperasikan langsung, dengan array yang lebih kecil seolah-olah diulang untuk menyesuaikan yang lebih besar."),
        tb("Skalar sebagai kasus paling sederhana", "Kasus broadcasting paling dikenal adalah skalar dan array. Menulis `a * 2` mengalikan setiap elemen dengan dua, seolah-olah dua diulang menjadi array berbentuk sama. Kata seolah-olah penting: NumPy tidak benar-benar membuat salinan berulang di memori. Ia mengatur cara membaca data agar elemen yang sama dibaca berkali-kali, sehingga broadcasting hemat memori dan cepat."),
        tb("Vektor dan matriks", "Vektor dapat dijumlahkan ke setiap baris matriks selama panjangnya sama dengan jumlah kolom. Vektor tiga elemen ditambahkan ke matriks dua kali tiga akan diulang untuk tiap baris. Sementara itu, matriks dua kali satu ditambahkan ke matriks dua kali tiga akan diulang untuk tiap kolom. Arah pengulangan ditentukan oleh sumbu yang berukuran satu."),
        C(
            ind("""
import numpy as np

a = np.array([1, 2, 3])
m = np.arange(6).reshape(2, 3)
print((a * 2).tolist())
print((m + a).tolist())
print((m + np.array([[10], [20]])).tolist())
"""),
            ind("""
[2, 4, 6]
[[1, 3, 5], [4, 6, 8]]
[[10, 11, 12], [23, 24, 25]]
"""),
            "Vektor diulang tiap baris, sedangkan kolom berukuran satu diulang tiap kolom.",
            filename="broadcast_dasar.py",
        ),
        tb("Aturan penyelarasan", "NumPy membandingkan shape dari sumbu paling kanan ke kiri. Pada tiap pasangan sumbu, dua ukuran harus sama, atau salah satunya satu. Ukuran satu direntangkan mengikuti pasangannya. Bila satu array memiliki lebih sedikit sumbu, shape-nya dilengkapi angka satu di sisi kiri. Bila ada pasangan yang berbeda dan tidak ada yang satu, operasi gagal dengan `ValueError`."),
        tb("Contoh langkah demi langkah", "Misalkan shape tiga kali satu ditambah shape satu kali empat. Bandingkan dari kanan: satu dengan empat menjadi empat, lalu tiga dengan satu menjadi tiga. Hasilnya shape tiga kali empat. Contoh lain: shape dua, tiga, empat dengan shape tiga kali satu. Yang kedua dilengkapi menjadi satu, tiga, satu, lalu hasilnya dua, tiga, empat. Latihan menelusuri seperti ini membuat prediksi shape menjadi refleks."),
        C(
            ind("""
import numpy as np

print(np.broadcast_shapes((3, 1), (1, 4)))
print(np.broadcast_shapes((2, 3, 4), (3, 1)))
print(np.broadcast_shapes((5,), (5, 1)))
c = np.array([[0], [10], [20]])
r = np.array([1, 2, 3])
print((c + r).tolist())
print((c + r).shape)
"""),
            ind("""
(3, 4)
(2, 3, 4)
(5, 5)
[[1, 2, 3], [11, 12, 13], [21, 22, 23]]
(3, 3)
"""),
            "Kolom dan baris bila dijumlahkan membentuk tabel penuh. Vektor lima dan kolom lima menghasilkan matriks lima kali lima.",
            filename="aturan_shape.py",
        ),
        tb("Ketika gagal", "Bila dua shape tidak cocok, NumPy melaporkan galat yang menyebut kedua shape. Contohnya shape tiga dan shape empat tidak dapat dioperasikan karena sumbu kanan berbeda dan tidak ada yang satu. Begitu pula dua kali tiga dengan dua: dua dilengkapi menjadi satu kali dua, lalu sumbu kanan tiga melawan dua gagal. Galat ini sering muncul dan membaca pesannya dengan teliti biasanya langsung menunjuk sumbu yang salah."),
        C(
            ind("""
import numpy as np

def cek(s1, s2):
    try:
        np.broadcast_shapes(s1, s2)
        return 'cocok'
    except ValueError:
        return 'gagal'

print(cek((3,), (4,)))
print(cek((2, 3), (2,)))
print(cek((2, 3), (2, 1)))
print(cek((1,), (7, 5)))
"""),
            ind("""
gagal
gagal
cocok
cocok
"""),
            "Vektor dua tidak cocok dengan matriks dua kali tiga, tetapi kolom dua kali satu cocok.",
            filename="broadcast_gagal.py",
        ),
        tb("Menambah sumbu dengan newaxis", "Sering kali array punya shape yang salah arah, misalnya vektor yang kita inginkan sebagai kolom. Indeks `None`, juga ditulis `np.newaxis`, menambah sumbu berukuran satu pada posisi itu. Vektor tiga elemen menjadi kolom tiga kali satu dengan `v[:, None]` dan menjadi baris satu kali tiga dengan `v[None, :]`. Teknik ini kunci untuk membangun tabel dari dua vektor."),
        tb("broadcast_to", "Fungsi `np.broadcast_to(a, shape)` merentangkan array ke shape tertentu secara eksplisit. Hasilnya read-only view dengan langkah memori nol pada sumbu yang diulang, membuktikan bahwa tidak ada data yang disalin. Bila Anda perlu mengubah hasilnya, panggil `.copy()` untuk membuat salinan nyata. Fungsi ini berguna untuk menguji aturan dan untuk membuat matriks berulang."),
        C(
            ind("""
import numpy as np

v = np.array([1, 2, 3])
b = np.broadcast_to(v, (2, 3))
print(b.tolist())
print(b.strides)
c = b.copy()
c[0, 0] = 99
print(c.tolist())
print(v.tolist())
"""),
            ind("""
[[1, 2, 3], [1, 2, 3]]
(0, 8)
[[99, 2, 3], [1, 2, 3]]
[1, 2, 3]
"""),
            "Langkah nol menunjukkan baris yang sama dibaca ulang tanpa salinan. Salinan nyata dapat diubah bebas.",
            filename="broadcast_to.py",
        ),
        tb("Mengapa ini penting", "Broadcasting menghapus hampir semua perulangan ganda dalam kode numerik. Menormalkan data, menghitung jarak, memberi bobot, dan membuat tabel semua dapat ditulis dalam satu ekspresi. Kode menjadi lebih pendek, lebih cepat karena dijalankan di C, dan lebih dekat dengan notasi matematika. Dua pelajaran berikutnya menunjukkan pola-pola praktis dan cara menghindari jebakan."),
        K("tip", "Tulis shape di sebelah kanan ke kiri dan lengkapi dengan satu di kiri. Bila tiap pasangan sama atau ada satu, operasi berhasil.", title="Cara memeriksa cepat"),
        tb("Dimensi ukuran satu", "Sumbu berukuran satu adalah satu-satunya yang boleh direntangkan, jadi mengenali mereka penting. Array berbentuk tiga kali satu kadang disebut vektor kolom, dan satu kali tiga vektor baris. Keduanya berisi tiga angka, tetapi berperilaku berbeda saat dioperasikan. Vektor satu dimensi berbentuk tiga dianggap seperti satu kali tiga saat dilengkapi di kiri."),
        tb("Operasi apa saja bisa", "Broadcasting berlaku untuk semua operasi elemen demi elemen, bukan hanya penjumlahan. Pengurangan, perkalian, pembagian, pangkat, perbandingan, dan operasi logika semuanya mengikuti aturan yang sama. Anda cukup mengingat satu aturan penyelarasan, lalu menerapkannya pada seluruh fungsi universal yang dibahas pada modul berikutnya."),
        E(
            "B1-03-1-ex1",
            "mudah",
            "Tulis fungsi `bentuk_hasil(s1, s2)` yang mengembalikan tuple shape hasil broadcasting dua shape, memakai `np.broadcast_shapes`.",
            ind("""
import numpy as np

def bentuk_hasil(s1, s2):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

assert bentuk_hasil((3, 1), (1, 4)) == (3, 4)
assert bentuk_hasil((2, 3, 4), (3, 1)) == (2, 3, 4)
assert bentuk_hasil((5,), (5, 1)) == (5, 5)
assert bentuk_hasil((), (2, 2)) == (2, 2)
"""),
            "Panggil np.broadcast_shapes dengan kedua shape.",
            F1.strip("\n"),
        ),
        E(
            "B1-03-1-ex2",
            "sedang",
            "Tulis fungsi `bisa_broadcast(s1, s2)` yang mengembalikan `True` bila dua shape kompatibel untuk broadcasting dan `False` bila tidak.",
            ind("""
import numpy as np

def bisa_broadcast(s1, s2):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

assert bisa_broadcast((3, 1), (1, 4)) is True
assert bisa_broadcast((3,), (4,)) is False
assert bisa_broadcast((2, 3), (2,)) is False
assert bisa_broadcast((2, 3), (2, 1)) is True
assert bisa_broadcast((1,), (7, 5)) is True
"""),
            "Tangkap ValueError dari np.broadcast_shapes.",
            F2.strip("\n"),
        ),
        E(
            "B1-03-1-ex3",
            "sedang",
            "Tulis fungsi `tabel_jumlah(kolom, baris)` yang menerima dua list bilangan dan mengembalikan, sebagai list Python, tabel yang sel baris ke-i kolom ke-j berisi `kolom[i] + baris[j]`, tanpa perulangan Python.",
            ind("""
import numpy as np

def tabel_jumlah(kolom, baris):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

assert tabel_jumlah([0, 10, 20], [1, 2, 3]) == [[1, 2, 3], [11, 12, 13], [21, 22, 23]]
assert tabel_jumlah([1], [1, 2]) == [[2, 3]]
assert tabel_jumlah([1, 2], [5]) == [[6], [7]]
assert tabel_jumlah([], [1, 2]) == []
"""),
            "Ubah kolom menjadi tiga kali satu dengan None.",
            F3.strip("\n"),
        ),
        E(
            "B1-03-1-ex4",
            "menantang",
            "Tulis fungsi `ulang_baris(v, n)` yang mengembalikan array dua dimensi berisi `n` baris, tiap barisnya salinan vektor `v`. Hasilnya harus dapat diubah tanpa memengaruhi `v`.",
            ind("""
import numpy as np

def ulang_baris(v, n):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

v = np.array([1, 2, 3])
r = ulang_baris(v, 2)
assert r.shape == (2, 3)
r[0, 0] = 99
assert r[1, 0] == 1
assert v.tolist() == [1, 2, 3]
assert ulang_baris(v, 3).tolist() == [[1, 2, 3]] * 3
"""),
            "Rentangkan dengan broadcast_to lalu salin agar bisa ditulis.",
            F4.strip("\n"),
        ),
    ],
    [
        M("Mengira array diulang di memori.", "Broadcasting mengatur cara baca, bukan menyalin."),
        M("Menambah vektor panjang dua ke matriks dua kali tiga.", "Ubah vektor menjadi kolom dua kali satu."),
        M("Mengubah hasil broadcast_to.", "Salin dulu dengan copy."),
    ],
    [
        Q("Aturan broadcasting dibaca dari?", ["Kanan ke kiri", "Kiri ke kanan", "Tengah", "Acak"], 0, "Sumbu paling kanan dulu.", hint="Kanan."),
        Q("Shape (3,1) dan (1,4) menghasilkan?", ["(3, 4)", "(3, 1)", "(1, 4)", "Galat"], 0, "Tiap sumbu direntangkan.", hint="Satu direntangkan."),
        Q("Shape (3,) dan (4,)?", ["Gagal", "(4,)", "(3,)", "(12,)"], 0, "Tidak sama dan tidak ada satu.", hint="Beda."),
        Q("v[:, None] menghasilkan?", ["Kolom", "Baris", "Skalar", "Matriks identitas"], 0, "Sumbu baru di akhir.", hint="Kolom."),
        Q("broadcast_to menghasilkan?", ["View read-only", "Salinan", "List", "Skalar"], 0, "Langkah nol.", hint="View."),
    ],
    [
        "Broadcasting memungkinkan operasi antar array berbeda shape.",
        "Shape diselaraskan dari kanan, tiap pasangan harus sama atau satu.",
        "Sumbu baru dibuat dengan None atau np.newaxis.",
        "broadcast_to merentangkan tanpa menyalin data.",
    ],
    [],
)

G1 = """
import numpy as np

def pusatkan_kolom(X):
    return X - X.mean(axis=0)
"""
G2 = """
import numpy as np

def proporsi_baris(X):
    return X / X.sum(axis=1, keepdims=True)
"""
G3 = """
import numpy as np

def tabel_kali(n):
    k = np.arange(1, n + 1)
    return (k[:, None] * k).tolist()
"""
G4 = """
import numpy as np

def jarak_pasangan(P):
    selisih = P[:, None, :] - P[None, :, :]
    return np.sqrt((selisih ** 2).sum(axis=-1))
"""

l2 = lesson(
    "B1-03-2",
    "Pola broadcasting yang sering dipakai",
    35,
    [
        "Memusatkan dan menormalkan data per kolom",
        "Memakai keepdims agar hasil ringkasan cocok untuk broadcasting",
        "Membangun tabel dari dua vektor",
        "Menghitung jarak antar semua pasangan titik",
    ],
    [
        tb("Dari aturan ke pekerjaan nyata", "Setelah memahami aturan, saatnya melihat pola yang muncul hampir di setiap proyek data. Empat pola utama adalah mengurangi atau membagi dengan ringkasan per kolom atau baris, memberi bobot per kolom, membangun tabel dari dua vektor, dan menghitung jarak antar titik. Semuanya memanfaatkan satu ide: ubah shape sehingga sumbu yang ingin direntangkan berukuran satu."),
        tb("Memusatkan per kolom", "Data matriks biasanya menyimpan satu sampel per baris dan satu fitur per kolom. Untuk memusatkan tiap fitur di sekitar nol, kurangi rata-rata kolom dari seluruh matriks. Rata-rata dengan `axis=0` menghasilkan vektor sepanjang jumlah kolom, dan vektor itu otomatis diulang pada tiap baris. Sumbu nol adalah sumbu yang diringkas, jadi ia hilang dari hasil."),
        tb("Standarisasi", "Standarisasi, atau skor z, memusatkan lalu membagi dengan simpangan baku kolom. Hasilnya tiap fitur punya rata-rata nol dan simpangan baku satu, sehingga fitur berskala berbeda dapat dibandingkan setara. Banyak algoritma pembelajaran mesin, seperti regresi dengan regularisasi dan k-nearest neighbors, bekerja jauh lebih baik pada data yang telah distandarisasi."),
        C(
            ind("""
import numpy as np

X = np.array([[1., 2.], [3., 6.], [5., 10.]])
mu = X.mean(axis=0)
sd = X.std(axis=0)
print(mu.tolist())
print((X - mu).tolist())
print(((X - mu) / sd).round(3).tolist())
"""),
            ind("""
[3.0, 6.0]
[[-2.0, -4.0], [0.0, 0.0], [2.0, 4.0]]
[[-1.225, -1.225], [0.0, 0.0], [1.225, 1.225]]
"""),
            "Rata-rata kolom dikurangkan ke tiap baris. Setelah dibagi simpangan baku, kedua kolom yang berskala berbeda menjadi identik.",
            filename="standarisasi.py",
        ),
        tb("keepdims", "Ringkasan per baris punya masalah: hasil `X.sum(axis=1)` berbentuk vektor tiga elemen, padahal untuk dibagi ke matriks tiga kali dua ia harus berupa kolom tiga kali satu. Argumen `keepdims=True` mempertahankan sumbu yang diringkas dengan ukuran satu, sehingga hasil langsung kompatibel. Ini cara paling bersih menghindari kesalahan arah dan lebih aman daripada menambah sumbu manual."),
        C(
            ind("""
import numpy as np

X = np.array([[1., 2.], [3., 6.], [5., 10.]])
print(X.sum(axis=1).shape)
print(X.sum(axis=1, keepdims=True).shape)
print((X / X.sum(axis=1, keepdims=True)).round(3).tolist())
M2 = np.arange(6).reshape(2, 3)
print((M2 - M2.mean(axis=1, keepdims=True)).tolist())
print((M2 - M2.mean(axis=0)).tolist())
"""),
            ind("""
(3,)
(3, 1)
[[0.333, 0.667], [0.333, 0.667], [0.333, 0.667]]
[[-1.0, 0.0, 1.0], [-1.0, 0.0, 1.0]]
[[-1.5, -1.5, -1.5], [1.5, 1.5, 1.5]]
"""),
            "Keepdims menjaga sumbu sehingga pembagian per baris benar. Pemusatan per baris dan per kolom memberi hasil berbeda.",
            filename="keepdims.py",
        ),
        tb("Bobot per kolom", "Memberi bobot pada tiap fitur cukup dengan mengalikan matriks dengan vektor bobot sepanjang jumlah kolom. Setiap baris dikalikan elemen demi elemen dengan bobot yang sama. Pola serupa dipakai untuk mengubah satuan kolom berbeda, misalnya satu kolom dikali seribu dan kolom lain dikali satu. Vektor bobot dapat disimpan dan dipakai ulang untuk data baru."),
        tb("Tabel dari dua vektor", "Mengubah satu vektor menjadi kolom dan membiarkan yang lain sebagai baris membuat operasi apa pun berlaku untuk semua pasangan. Perkalian menghasilkan tabel perkalian, penjumlahan menghasilkan tabel jumlah, dan perbandingan menghasilkan matriks boolean. Fungsi `np.add.outer` dan `np.multiply.outer` melakukan hal yang sama dengan nama yang lebih eksplisit."),
        C(
            ind("""
import numpy as np

k = np.arange(1, 4)
print((k[:, None] * k).tolist())
print(np.add.outer([1, 2], [10, 20, 30]).tolist())
print((np.array([1, 2, 3]) > np.array([[0], [2]])).tolist())
w = np.array([0.5, 1, 2])
print((np.array([[2, 4, 6], [1, 1, 1]]) * w).tolist())
"""),
            ind("""
[[1, 2, 3], [2, 4, 6], [3, 6, 9]]
[[11, 21, 31], [12, 22, 32]]
[[True, True, True], [False, False, True]]
[[1.0, 4.0, 12.0], [0.5, 1.0, 2.0]]
"""),
            "Satu kolom dan satu baris menghasilkan tabel semua pasangan. Bobot per kolom diterapkan ke setiap baris.",
            filename="tabel_pasangan.py",
        ),
        tb("Jarak antar titik", "Menghitung jarak antara setiap pasangan dari n titik dalam dua dimensi biasanya memerlukan perulangan ganda. Dengan broadcasting, ubah titik menjadi shape n, satu, dua dan satu, n, dua. Pengurangan menghasilkan selisih berbentuk n, n, dua untuk semua pasangan. Kuadratkan, jumlahkan sepanjang sumbu terakhir, dan akarkan untuk mendapat matriks jarak n kali n."),
        C(
            ind("""
import numpy as np

P = np.array([[0, 0], [3, 4], [6, 8]])
selisih = P[:, None, :] - P[None, :, :]
print(selisih.shape)
D = np.sqrt((selisih ** 2).sum(axis=-1))
print(D.tolist())
print(bool((D == D.T).all()))
"""),
            ind("""
(3, 3, 2)
[[0.0, 5.0, 10.0], [5.0, 0.0, 5.0], [10.0, 5.0, 0.0]]
True
"""),
            "Selisih semua pasangan dibentuk tanpa perulangan, dan matriks jarak simetris dengan diagonal nol.",
            filename="jarak_pasangan.py",
        ),
        tb("Peringatan memori", "Pola jarak membuat array perantara berukuran n kali n kali d. Untuk sepuluh ribu titik, itu seratus juta elemen per dimensi dan dapat menghabiskan memori. Broadcasting menghemat penyalinan input, tetapi hasil perantara tetap nyata. Untuk data besar, proses per potongan atau gunakan fungsi khusus seperti yang disediakan scipy untuk jarak pasangan."),
        tb("Ringkasan pelajaran", "Hampir semua pola praktis adalah kombinasi ringkasan dengan keepdims dan operasi aritmetika. Memusatkan dan menstandarkan, membobot kolom, membuat tabel pasangan, dan menghitung jarak semua ditulis dalam satu hingga tiga baris. Kuncinya selalu sama: pastikan sumbu yang ingin diulang berukuran satu."),
        K("tip", "Gunakan keepdims=True pada ringkasan yang akan dioperasikan kembali dengan array asal. Ini menghindari kesalahan arah.", title="Kebiasaan aman"),
        tb("Memilih sumbu ringkasan", "Kesalahan sumbu sering terjadi karena arti angka sumbu tidak intuitif. Sumbu nol adalah arah turun melintasi baris, sehingga ringkasan dengan sumbu nol memberi satu angka per kolom. Sumbu satu adalah arah ke kanan melintasi kolom, sehingga memberi satu angka per baris. Cara mengingat: sumbu yang disebut adalah yang menghilang dari hasil."),
        tb("Normalisasi min-max", "Selain standarisasi, normalisasi min-max menskalakan tiap kolom ke rentang nol sampai satu dengan rumus nilai dikurangi minimum kolom lalu dibagi rentang kolom. Kedua ringkasan dihitung dengan sumbu nol dan dioperasikan langsung dengan matriks. Hati-hati pada kolom konstan karena rentangnya nol dan pembagian menjadi tidak terdefinisi."),
        tb("Pembagian dengan nol", "Standarisasi pada kolom yang seluruh nilainya sama menghasilkan simpangan baku nol dan hasil tidak terhingga atau tidak terdefinisi. Tangani dengan mengganti simpangan baku nol menjadi satu sebelum membagi, atau menghapus kolom konstan lebih dulu. Kolom tanpa variasi memang tidak membawa informasi untuk model, jadi menghapusnya biasanya aman."),
        E(
            "B1-03-2-ex1",
            "mudah",
            "Tulis fungsi `pusatkan_kolom(X)` yang mengurangi rata-rata tiap kolom dari matriks `X` dan mengembalikan matriks hasilnya.",
            ind("""
import numpy as np

def pusatkan_kolom(X):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

X = np.array([[1., 2.], [3., 6.], [5., 10.]])
r = pusatkan_kolom(X)
assert r.tolist() == [[-2.0, -4.0], [0.0, 0.0], [2.0, 4.0]]
assert np.allclose(r.mean(axis=0), 0)
assert r.shape == X.shape
assert X[0, 0] == 1.0
"""),
            "Kurangi X dengan X.mean(axis=0).",
            G1.strip("\n"),
        ),
        E(
            "B1-03-2-ex2",
            "sedang",
            "Tulis fungsi `proporsi_baris(X)` yang membagi tiap elemen matriks `X` dengan jumlah barisnya, sehingga tiap baris berjumlah satu.",
            ind("""
import numpy as np

def proporsi_baris(X):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

X = np.array([[1., 2.], [3., 6.], [5., 10.]])
r = proporsi_baris(X)
assert np.allclose(r.sum(axis=1), 1)
assert np.allclose(r[0], [1 / 3, 2 / 3])
assert r.shape == (3, 2)
assert np.allclose(proporsi_baris(np.array([[1., 1., 2.]])), [[0.25, 0.25, 0.5]])
"""),
            "Jumlahkan dengan axis=1 dan keepdims=True lalu bagi.",
            G2.strip("\n"),
        ),
        E(
            "B1-03-2-ex3",
            "sedang",
            "Tulis fungsi `tabel_kali(n)` yang mengembalikan tabel perkalian 1 sampai `n` sebagai list Python berukuran `n` kali `n`, tanpa perulangan Python.",
            ind("""
import numpy as np

def tabel_kali(n):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

assert tabel_kali(3) == [[1, 2, 3], [2, 4, 6], [3, 6, 9]]
assert tabel_kali(1) == [[1]]
assert tabel_kali(4)[3] == [4, 8, 12, 16]
assert tabel_kali(0) == []
"""),
            "Kalikan kolom 1 sampai n dengan baris yang sama.",
            G3.strip("\n"),
        ),
        E(
            "B1-03-2-ex4",
            "menantang",
            "Tulis fungsi `jarak_pasangan(P)` yang menerima matriks `P` berukuran `n` kali `d` berisi titik-titik dan mengembalikan matriks jarak Euclid `n` kali `n` antar semua pasangan, tanpa perulangan Python.",
            ind("""
import numpy as np

def jarak_pasangan(P):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

P = np.array([[0, 0], [3, 4], [6, 8]])
D = jarak_pasangan(P)
assert D.shape == (3, 3)
assert np.allclose(D, [[0, 5, 10], [5, 0, 5], [10, 5, 0]])
assert np.allclose(D, D.T)
assert np.allclose(jarak_pasangan(np.array([[1.0], [4.0]])), [[0, 3], [3, 0]])
"""),
            "Bentuk selisih n, n, d dengan dua sumbu baru lalu akarkan jumlah kuadrat.",
            G4.strip("\n"),
        ),
    ],
    [
        M("Membagi per baris tanpa keepdims.", "Gunakan keepdims=True agar arah benar."),
        M("Mengurangi rata-rata baris dari kolom.", "Pakai axis=0 untuk kolom dan axis=1 untuk baris."),
        M("Menghitung jarak semua pasangan pada data raksasa.", "Proses per potongan atau pakai scipy."),
    ],
    [
        Q("Memusatkan kolom memakai?", ["X - X.mean(axis=0)", "X - X.mean()", "X / X.max", "X.T"], 0, "Rata-rata per kolom.", hint="axis=0."),
        Q("keepdims=True berguna untuk?", ["Menjaga sumbu ukuran satu", "Mempercepat", "Mengubah tipe", "Mengurutkan"], 0, "Siap untuk broadcasting.", hint="Jaga."),
        Q("Tabel semua pasangan butuh?", ["Satu kolom dan satu baris", "Dua matriks sama", "Satu skalar", "Dua list"], 0, "Sumbu berbeda.", hint="Kolom dan baris."),
        Q("Selisih semua titik berbentuk?", ["n, n, d", "n, d", "n, n", "d, d"], 0, "Dua sumbu titik.", hint="Pasangan."),
        Q("Standarisasi menghasilkan?", ["Rata-rata nol dan simpangan baku satu", "Nilai antara nol dan satu", "Nilai bulat", "Data terurut"], 0, "Skor z.", hint="Nol dan satu."),
    ],
    [
        "Pemusatan dan standarisasi memakai ringkasan per kolom.",
        "keepdims menjaga sumbu agar ringkasan kompatibel.",
        "Tabel pasangan dibuat dari satu kolom dan satu baris.",
        "Jarak antar titik memakai selisih berbentuk n, n, d.",
    ],
    [],
)

H1 = """
import numpy as np

def one_hot(label, k):
    return (np.array(label)[:, None] == np.arange(k)).astype(int).tolist()
"""
H2 = """
import numpy as np

def bandingkan_ambang(x, ambang):
    return (np.array(x)[None, :] > np.array(ambang)[:, None]).tolist()
"""
H3 = """
import numpy as np

def skala_kolom(X, w):
    return X * w
"""
H4 = """
import numpy as np

def kurangi_rata_baris(M):
    return M - M.mean(axis=1, keepdims=True)
"""

l3 = lesson(
    "B1-03-3",
    "Jebakan, debugging, dan performa broadcasting",
    35,
    [
        "Mengenali kesalahan arah antara vektor dan kolom",
        "Membuat one-hot dan matriks perbandingan dengan broadcasting",
        "Menjelaskan mengapa broadcasting cepat dan hemat memori",
        "Memeriksa shape secara sistematis saat hasil mengejutkan",
    ],
    [
        tb("Broadcasting yang salah diam-diam", "Bahaya terbesar broadcasting bukan galat, melainkan hasil yang salah tanpa pesan. Bila vektor panjang tiga dan kolom tiga kali satu dijumlahkan, kita mendapat matriks tiga kali tiga, bukan vektor tiga elemen yang mungkin kita kira. Program berjalan mulus dan angka tampak masuk akal, tetapi ukuran dan nilainya keliru. Karena itu memeriksa shape adalah kebiasaan wajib."),
        C(
            ind("""
import numpy as np

v = np.array([1, 2, 3])
k = np.array([[10], [20], [30]])
print((v + k).shape)
print((v + v).shape)
print((v + k.ravel()).shape)
y = np.array([1, 2, 3])
pred = np.array([[1], [2], [4]])
print((y == pred).shape)
print((y == pred.ravel()).tolist())
"""),
            ind("""
(3, 3)
(3,)
(3,)
(3, 3)
[True, True, False]
"""),
            "Vektor dan kolom menghasilkan matriks penuh. Membandingkan label dengan prediksi berbentuk kolom menghasilkan matriks, bukan hasil per elemen yang diinginkan.",
            filename="salah_arah.py",
        ),
        tb("Contoh klasik", "Kesalahan paling terkenal terjadi pada evaluasi model. Label asli berbentuk vektor tiga elemen, sedangkan prediksi keluar dari model sebagai kolom tiga kali satu. Membandingkan keduanya dengan sama dengan menghasilkan matriks tiga kali tiga, dan rata-ratanya jauh dari akurasi sebenarnya. Solusinya meratakan salah satunya dengan `ravel` atau `reshape` agar keduanya berbentuk sama sebelum dibandingkan."),
        tb("Strategi debugging", "Bila hasil mengejutkan, cetak shape setiap operan dan hasil setiap langkah. Tuliskan shape yang Anda harapkan sebelum menjalankan, lalu bandingkan. Tambahkan assert pada shape di titik-titik penting, misalnya `assert pred.shape == y.shape`. Assert murah dan menangkap kesalahan di tempat kejadian, bukan beberapa langkah kemudian ketika sumber masalah sudah sulit dilacak."),
        tb("One-hot dengan broadcasting", "Representasi one-hot mengubah label kategori menjadi vektor berisi satu pada posisi kelas dan nol di tempat lain. Dengan broadcasting, bandingkan label berbentuk kolom dengan deret kelas berbentuk baris. Hasilnya matriks boolean berukuran jumlah sampel kali jumlah kelas, dan konversi ke bilangan bulat menghasilkan matriks one-hot tanpa perulangan."),
        C(
            ind("""
import numpy as np

lab = np.array([0, 2, 1, 2])
oh = (lab[:, None] == np.arange(3)).astype(int)
print(oh.tolist())
print(oh.sum(axis=0).tolist())
print(oh.argmax(axis=1).tolist())
"""),
            ind("""
[[1, 0, 0], [0, 0, 1], [0, 1, 0], [0, 0, 1]]
[1, 1, 2]
[0, 2, 1, 2]
"""),
            "Satu perbandingan menghasilkan matriks one-hot. Jumlah kolom memberi frekuensi tiap kelas dan argmax mengembalikan label.",
            filename="one_hot.py",
        ),
        tb("Perbandingan banyak ambang", "Pola serupa menguji beberapa ambang sekaligus. Dengan data sebagai baris dan ambang sebagai kolom, satu perbandingan menghasilkan matriks yang menunjukkan data mana yang melewati ambang mana. Jumlah sepanjang sumbu data memberi banyaknya elemen yang lolos untuk tiap ambang. Ini dasar menghitung kurva presisi dan recall pada berbagai ambang keputusan."),
        C(
            ind("""
import numpy as np

x = np.array([1, 2, 3])
ambang = np.array([0, 2])
hasil = x[None, :] > ambang[:, None]
print(hasil.tolist())
print(hasil.sum(axis=1).tolist())
skor = np.array([0.2, 0.8, 0.5, 0.9])
print((skor[None, :] >= np.array([0.5, 0.9])[:, None]).sum(axis=1).tolist())
"""),
            ind("""
[[True, True, True], [False, False, True]]
[3, 1]
[3, 1]
"""),
            "Satu ekspresi menguji dua ambang sekaligus. Jumlah per baris memberi banyaknya yang lolos tiap ambang.",
            filename="banyak_ambang.py",
        ),
        tb("Mengapa cepat", "Perulangan Python mengeksekusi satu instruksi interpreter per elemen, dan tiap elemen adalah objek lengkap. Broadcasting menjalankan perulangan di dalam kode C yang dikompilasi, bekerja langsung pada memori berurutan. Selisih kecepatannya sering puluhan hingga ratusan kali. Tambahan keuntungannya, kode menjadi lebih pendek dan lebih mirip rumus matematika sehingga lebih mudah diverifikasi."),
        tb("Batas broadcasting", "Broadcasting bukan obat segala masalah. Bila hasil perantara berukuran raksasa, seperti pada jarak semua pasangan dengan data besar, memori dapat habis. Bila logika tiap elemen bergantung pada elemen sebelumnya, seperti rekursi, vectorization sulit dilakukan. Pada kasus itu pertimbangkan pemrosesan per potongan, alat seperti numba, atau algoritma yang tidak membentuk hasil perantara besar."),
        tb("Daftar periksa", "Sebelum mempercayai hasil broadcasting, jawab empat pertanyaan. Berapa shape setiap operan? Berapa shape hasil yang diharapkan? Sumbu mana yang direntangkan? Apakah ada ringkasan yang kehilangan sumbu dan perlu keepdims? Menjawab keempatnya hanya butuh satu menit dan menyelamatkan Anda dari jam-jam mencari angka yang salah."),
        tb("Ringkasan modul", "Anda telah mempelajari aturan penyelarasan dari kanan, pola pemusatan, standarisasi, tabel pasangan, dan jarak, serta jebakan arah yang senyap. Dengan kebiasaan memeriksa shape dan memakai keepdims, broadcasting menjadi alat yang aman. Modul berikutnya membahas operasi vectorized dan ufunc yang menjadi dasar perhitungan elemen demi elemen."),
        K("warn", "Broadcasting yang salah arah tidak menimbulkan galat, hanya hasil yang keliru. Periksa shape dan tambahkan assert di titik penting.", title="Galat senyap"),
        tb("Uji dengan contoh kecil", "Sebelum menerapkan ekspresi broadcasting pada data besar, ujilah pada contoh kecil yang hasilnya dapat Anda hitung dengan tangan, misalnya matriks dua kali tiga. Bandingkan dengan perulangan lambat yang jelas benar. Bila keduanya sama pada beberapa kasus, termasuk kasus tepi seperti satu baris atau satu kolom, kepercayaan pada kode meningkat."),
        tb("Membaca pesan galat", "Pesan galat broadcasting menyebut dua shape yang tidak cocok, misalnya operands could not be broadcast together with shapes dua koma tiga dan dua. Tuliskan keduanya sejajar dari kanan lalu cari pasangan yang berbeda dan bukan satu. Sumbu itulah yang perlu diubah, biasanya dengan menambah sumbu baru atau mengubah ringkasan menjadi keepdims."),
        tb("Gaya penulisan yang jelas", "Beri nama variabel yang menyiratkan bentuknya, seperti kolom_bobot atau baris_rata, dan tuliskan komentar shape di sebelah dokumentasi fungsi. Orang yang membaca kode, termasuk Anda sendiri nanti, dapat memahami ekspresi broadcasting tanpa menelusuri ulang setiap shape."),
        E(
            "B1-03-3-ex1",
            "mudah",
            "Tulis fungsi `one_hot(label, k)` yang menerima list label bilangan bulat dari 0 sampai `k - 1` dan mengembalikan matriks one-hot sebagai list Python bertipe bilangan bulat, tanpa perulangan Python.",
            ind("""
import numpy as np

def one_hot(label, k):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

assert one_hot([0, 2, 1, 2], 3) == [[1, 0, 0], [0, 0, 1], [0, 1, 0], [0, 0, 1]]
assert one_hot([1], 2) == [[0, 1]]
assert one_hot([], 3) == []
assert np.array(one_hot([0, 1, 2], 3)).sum() == 3
"""),
            "Bandingkan label kolom dengan arange(k) lalu ubah ke int.",
            H1.strip("\n"),
        ),
        E(
            "B1-03-3-ex2",
            "sedang",
            "Tulis fungsi `bandingkan_ambang(x, ambang)` yang mengembalikan matriks boolean sebagai list Python dengan baris untuk tiap ambang dan kolom untuk tiap elemen `x`, bernilai `True` bila `x[j] > ambang[i]`.",
            ind("""
import numpy as np

def bandingkan_ambang(x, ambang):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

assert bandingkan_ambang([1, 2, 3], [0, 2]) == [[True, True, True], [False, False, True]]
assert bandingkan_ambang([5], [1, 9]) == [[True], [False]]
assert np.array(bandingkan_ambang([1, 2, 3, 4], [2, 3, 4])).shape == (3, 4)
assert bandingkan_ambang([1, 2], [3]) == [[False, False]]
"""),
            "Ubah x menjadi baris dan ambang menjadi kolom.",
            H2.strip("\n"),
        ),
        E(
            "B1-03-3-ex3",
            "sedang",
            "Tulis fungsi `skala_kolom(X, w)` yang mengalikan tiap kolom matriks `X` dengan elemen vektor `w` yang bersesuaian dan mengembalikan matriks hasilnya.",
            ind("""
import numpy as np

def skala_kolom(X, w):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

X = np.array([[2, 4, 6], [1, 1, 1]])
w = np.array([0.5, 1, 2])
assert skala_kolom(X, w).tolist() == [[1.0, 4.0, 12.0], [0.5, 1.0, 2.0]]
assert skala_kolom(np.ones((2, 2)), np.array([3, 4])).tolist() == [[3.0, 4.0], [3.0, 4.0]]
assert skala_kolom(X, np.ones(3)).shape == (2, 3)
assert skala_kolom(np.zeros((1, 3)), w).sum() == 0
"""),
            "Kalikan langsung dengan vektor bobot.",
            H3.strip("\n"),
        ),
        E(
            "B1-03-3-ex4",
            "menantang",
            "Tulis fungsi `kurangi_rata_baris(M)` yang mengurangi rata-rata tiap baris dari baris itu sendiri dan mengembalikan matriks hasilnya, sehingga tiap baris berjumlah nol.",
            ind("""
import numpy as np

def kurangi_rata_baris(M):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

M = np.arange(6).reshape(2, 3)
r = kurangi_rata_baris(M)
assert r.tolist() == [[-1.0, 0.0, 1.0], [-1.0, 0.0, 1.0]]
assert np.allclose(r.sum(axis=1), 0)
assert r.shape == M.shape
assert np.allclose(kurangi_rata_baris(np.array([[2., 4.], [10., 20.]])), [[-1, 1], [-5, 5]])
"""),
            "Hitung rata-rata sumbu satu dengan keepdims lalu kurangkan.",
            H4.strip("\n"),
        ),
    ],
    [
        M("Menjumlahkan vektor dan kolom lalu mengira hasilnya vektor.", "Periksa shape, ratakan salah satunya bila perlu."),
        M("Membandingkan label dengan prediksi berbentuk kolom.", "Samakan shape sebelum membandingkan."),
        M("Memakai broadcasting pada data raksasa tanpa memikirkan memori.", "Proses per potongan."),
    ],
    [
        Q("Vektor (3,) plus kolom (3,1) menghasilkan?", ["(3, 3)", "(3,)", "(3, 1)", "Galat"], 0, "Keduanya direntangkan.", hint="Matriks."),
        Q("One-hot dibuat dengan?", ["Label kolom == arange(k)", "Label + 1", "Label * k", "Label.T"], 0, "Bandingkan kolom dan baris.", hint="Bandingkan."),
        Q("Cara menangkap salah arah?", ["Assert pada shape", "Menghapus data", "Mengubah tipe", "Mengurutkan"], 0, "Periksa di tempat.", hint="Assert."),
        Q("Broadcasting cepat karena?", ["Perulangan di kode C", "Memakai GPU otomatis", "Menyalin data", "Memakai list"], 0, "Dikompilasi.", hint="C."),
        Q("Batas broadcasting?", ["Hasil perantara besar", "Tidak ada", "Hanya skalar", "Hanya vektor"], 0, "Memori.", hint="Perantara."),
    ],
    [
        "Broadcasting yang salah arah menghasilkan hasil keliru tanpa galat.",
        "One-hot dan perbandingan ambang dapat dibuat tanpa perulangan.",
        "Broadcasting cepat karena perulangan berjalan di kode C.",
        "Periksa shape dan assert di titik penting.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perintah yang cukup jelas dalam teks.", "brief": []}

write_module(
    "B1",
    3,
    "Broadcasting",
    105,
    [
        "Menerapkan aturan broadcasting dan memprediksi shape",
        "Memakai pola pemusatan, standarisasi, tabel pasangan, dan jarak",
        "Menghindari jebakan arah dan memeriksa shape secara sistematis",
    ],
    [l1, l2, l3],
    video,
    REF,
)
