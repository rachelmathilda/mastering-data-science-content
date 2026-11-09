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

def kali_matriks(A, B):
    return (np.asarray(A) @ np.asarray(B)).tolist()
"""
F2 = """
def bentuk_perkalian(s1, s2):
    if s1[1] != s2[0]:
        return None
    return (s1[0], s2[1])
"""
F3 = """
import numpy as np

def cosine(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    return round(float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b))), 4)
"""
F4 = """
import numpy as np

def kovarians_manual(X):
    X = np.asarray(X, dtype=float)
    Xc = X - X.mean(axis=0)
    return Xc.T @ Xc / (len(X) - 1)
"""

l1 = lesson(
    "B1-05-1",
    "Perkalian matriks, dot, dan norma",
    35,
    [
        "Membedakan perkalian elemen dan perkalian matriks",
        "Memakai operator @, dot, outer, dan trace",
        "Memeriksa syarat shape pada perkalian matriks",
        "Menghitung norma dan kemiripan kosinus",
    ],
    [
        tb("Mengapa aljabar linear", "Hampir seluruh pembelajaran mesin adalah aljabar linear yang disamarkan. Regresi linear, jaringan saraf, PCA, dan sistem rekomendasi semuanya bergantung pada perkalian matriks, penyelesaian sistem persamaan, dan penguraian matriks. NumPy menyediakan semua operasi ini lewat operator dan modul `np.linalg`, dengan implementasi yang memanfaatkan pustaka numerik yang sangat dioptimalkan seperti BLAS dan LAPACK."),
        tb("Dua jenis perkalian", "Operator bintang pada array melakukan perkalian elemen demi elemen, yang sudah kita kenal. Perkalian matriks yang sesungguhnya memakai operator `@`, atau fungsi `np.matmul` dan `np.dot`. Pada perkalian matriks, elemen baris ke-i kolom ke-j hasil adalah jumlah hasil kali baris ke-i matriks pertama dengan kolom ke-j matriks kedua. Mencampuradukkan keduanya adalah kesalahan pemula yang paling umum dan tidak menimbulkan galat bila shape kebetulan cocok."),
        C(
            ind("""
import numpy as np

A = np.array([[1, 2], [3, 4]])
B = np.array([[0, 1], [1, 0]])
print((A * B).tolist())
print((A @ B).tolist())
print(A.T.tolist())
print(int(np.trace(A)))
print(np.diag(A).tolist())
"""),
            ind("""
[[0, 2], [3, 0]]
[[2, 1], [4, 3]]
[[1, 3], [2, 4]]
5
[1, 4]
"""),
            "Bintang mengalikan elemen sepasang, sedangkan at melakukan perkalian matriks. Trace adalah jumlah diagonal.",
            filename="kali_matriks.py",
        ),
        tb("Syarat shape", "Perkalian matriks hanya terdefinisi bila jumlah kolom matriks pertama sama dengan jumlah baris matriks kedua. Matriks dua kali tiga dapat dikalikan dengan tiga kali empat dan menghasilkan dua kali empat: ukuran dalam harus sama dan ukuran luar menjadi hasilnya. Bila syarat itu dilanggar, NumPy melaporkan `ValueError`. Menuliskan shape di atas kertas sebelum menulis kode menghindari banyak galat."),
        C(
            ind("""
import numpy as np

print((np.ones((2, 3)) @ np.ones((3, 4))).shape)
try:
    np.ones((2, 3)) @ np.ones((2, 3))
except ValueError:
    print('gagal')
v = np.array([1, 2])
A = np.array([[1, 2], [3, 4]])
print((A @ v).tolist())
print(int(v @ v))
print(np.outer(v, [3, 4]).tolist())
"""),
            ind("""
(2, 4)
gagal
[5, 11]
5
[[3, 4], [6, 8]]
"""),
            "Ukuran dalam harus sama. Matriks kali vektor memberi vektor, dot dua vektor memberi skalar, dan outer memberi matriks.",
            filename="syarat_shape.py",
        ),
        tb("Vektor dalam perkalian matriks", "Operator `@` memperlakukan vektor satu dimensi dengan luwes. Matriks kali vektor menghasilkan vektor, dengan vektor dianggap kolom. Vektor kali matriks menganggap vektor sebagai baris. Dua vektor menghasilkan hasil kali dalam, yaitu satu skalar. Sementara `np.outer` menghasilkan matriks hasil kali luar, dengan elemen baris i kolom j adalah hasil kali elemen i vektor pertama dan elemen j vektor kedua."),
        tb("Interpretasi geometris", "Hasil kali dalam dua vektor sama dengan hasil kali panjang keduanya dengan kosinus sudut di antaranya. Bila hasilnya nol, vektor tegak lurus. Bila besar dan positif, arahnya mirip. Karena itu hasil kali dalam menjadi dasar ukuran kemiripan. Perkalian matriks dengan vektor dapat dipandang sebagai tiap baris matriks diukur kemiripannya dengan vektor itu, menghasilkan satu skor per baris."),
        tb("Norma", "Norma mengukur ukuran sebuah vektor. Fungsi `np.linalg.norm` secara bawaan menghitung norma Euclid, akar jumlah kuadrat elemen. Argumen kedua memilih jenis norma: satu untuk jumlah nilai mutlak, dua untuk Euclid, dan tak hingga untuk nilai mutlak terbesar. Untuk matriks, `'fro'` menghitung norma Frobenius, akar jumlah kuadrat semua elemen, yang sering dipakai untuk mengukur galat antar matriks."),
        C(
            ind("""
import numpy as np

print(float(np.linalg.norm([3, 4])))
print(float(np.linalg.norm([1, 2, 3], 1)))
print(round(float(np.linalg.norm([[1, 2], [3, 4]], 'fro')), 4))

def cos(a, b):
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    return round(float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b))), 4)

print(cos([1, 0], [0, 1]), cos([1, 1], [2, 2]), cos([1, 2], [2, 1]))
"""),
            ind("""
5.0
6.0
5.4772
0.0 1.0 0.8
"""),
            "Norma Euclid tiga empat adalah lima. Kemiripan kosinus nol untuk vektor tegak lurus dan satu untuk arah sama.",
            filename="norma_kosinus.py",
        ),
        tb("Kemiripan kosinus", "Kemiripan kosinus membagi hasil kali dalam dengan hasil kali norma, sehingga hanya mengukur arah dan mengabaikan panjang. Nilainya satu untuk arah sama, nol untuk tegak lurus, dan minus satu untuk berlawanan. Ukuran ini dipakai luas pada pencarian teks, rekomendasi, dan pembandingan embedding, karena dokumen panjang dan pendek dengan topik sama tetap dianggap mirip."),
        tb("Kovarians sebagai perkalian matriks", "Matriks kovarians fitur dapat dihitung dengan perkalian matriks. Pusatkan data per kolom, lalu hitung transpos data terpusat dikali data terpusat dan bagi dengan n dikurangi satu. Hasilnya matriks simetris dengan ragam di diagonal dan kovarians di luar diagonal. Rumus ini sama dengan yang dihitung `np.cov`, sehingga kita dapat memeriksa hasilnya satu sama lain."),
        C(
            ind("""
import numpy as np

X = np.array([[1, 2], [2, 4], [3, 6], [4, 8]], dtype=float)
Xc = X - X.mean(axis=0)
K = Xc.T @ Xc / (len(X) - 1)
print(np.round(K, 4).tolist())
print(bool(np.allclose(K, np.cov(X.T))))
print(np.linalg.matrix_power(np.array([[1, 2], [3, 4]]), 3).tolist())
"""),
            ind("""
[[1.6667, 3.3333], [3.3333, 6.6667]]
True
[[37, 54], [81, 118]]
"""),
            "Kovarians manual cocok dengan np.cov. Pangkat matriks adalah perkalian matriks berulang.",
            filename="kovarians_manual.py",
        ),
        tb("Efisiensi dan urutan", "Perkalian matriks bersifat asosiatif tetapi tidak komutatif. Mengalikan A dengan B umumnya tidak sama dengan B dengan A. Urutan pengelompokan memengaruhi biaya: pada tiga matriks, mengalikan dari kiri atau kanan dapat berbeda ukurannya secara drastis. Untuk rantai panjang, `np.linalg.multi_dot` memilih urutan termurah. Pada kebanyakan kasus Anda tidak perlu peduli, tetapi untuk matriks besar selisihnya terasa."),
        tb("Pustaka dan kecepatan", "Perkalian matriks NumPy untuk bilangan desimal diserahkan ke pustaka BLAS yang memanfaatkan beberapa inti prosesor dan instruksi vektor. Itu sebabnya `A @ B` bisa ratusan kali lebih cepat daripada tiga perulangan Python. Untuk bilangan bulat, NumPy memakai implementasi sendiri yang lebih lambat. Bila kecepatan penting dan ketelitian cukup, ubah ke float32 atau float64 sebelum mengalikan."),
        K("tip", "Tuliskan shape tiap matriks sebelum mengalikannya. Ukuran dalam harus sama dan ukuran luar menjadi hasil.", title="Cek cepat"),
        E(
            "B1-05-1-ex1",
            "mudah",
            "Tulis fungsi `kali_matriks(A, B)` yang mengembalikan hasil perkalian matriks `A` dan `B` sebagai list Python.",
            ind("""
import numpy as np

def kali_matriks(A, B):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

assert kali_matriks([[1, 2], [3, 4]], [[0, 1], [1, 0]]) == [[2, 1], [4, 3]]
assert kali_matriks([[1, 2, 3]], [[1], [1], [1]]) == [[6]]
assert kali_matriks(np.eye(2), [[5, 6], [7, 8]]) == [[5.0, 6.0], [7.0, 8.0]]
assert kali_matriks([[2]], [[3]]) == [[6]]
"""),
            "Gunakan operator at pada array.",
            F1.strip("\n"),
        ),
        E(
            "B1-05-1-ex2",
            "sedang",
            "Tulis fungsi `bentuk_perkalian(s1, s2)` yang menerima dua shape matriks `(baris, kolom)` dan mengembalikan shape hasil perkalian `s1 @ s2` sebagai tuple, atau `None` bila perkalian tidak terdefinisi.",
            ind("""
def bentuk_perkalian(s1, s2):
    # TODO: implementasikan
    pass
"""),
            ind("""
assert bentuk_perkalian((2, 3), (3, 4)) == (2, 4)
assert bentuk_perkalian((2, 3), (2, 3)) is None
assert bentuk_perkalian((1, 5), (5, 1)) == (1, 1)
assert bentuk_perkalian((4, 1), (1, 4)) == (4, 4)
"""),
            "Kolom pertama harus sama dengan baris kedua.",
            F2.strip("\n"),
        ),
        E(
            "B1-05-1-ex3",
            "sedang",
            "Tulis fungsi `cosine(a, b)` yang mengembalikan kemiripan kosinus dua vektor, dibulatkan ke empat desimal sebagai float Python.",
            ind("""
import numpy as np

def cosine(a, b):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

assert cosine([1, 0], [0, 1]) == 0.0
assert cosine([1, 1], [2, 2]) == 1.0
assert cosine([1, 2], [2, 1]) == 0.8
assert cosine([1, 0], [-1, 0]) == -1.0
"""),
            "Hasil kali dalam dibagi hasil kali norma.",
            F3.strip("\n"),
        ),
        E(
            "B1-05-1-ex4",
            "menantang",
            "Tulis fungsi `kovarians_manual(X)` yang menghitung matriks kovarians kolom matriks `X` (baris adalah sampel) dengan pembagi n minus satu, memakai perkalian matriks tanpa memanggil `np.cov`.",
            ind("""
import numpy as np

def kovarians_manual(X):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

X = np.array([[1, 2], [2, 4], [3, 6], [4, 8]], dtype=float)
K = kovarians_manual(X)
assert K.shape == (2, 2)
assert np.allclose(K, np.cov(X.T))
assert np.allclose(K, K.T)
Y = np.array([[1., 0.], [-1., 0.], [0., 1.], [0., -1.]])
assert np.allclose(kovarians_manual(Y), [[2 / 3, 0], [0, 2 / 3]])
"""),
            "Pusatkan kolom lalu hitung transpos dikali data dan bagi n minus satu.",
            F4.strip("\n"),
        ),
    ],
    [
        M("Memakai bintang untuk perkalian matriks.", "Pakai at atau np.matmul."),
        M("Mengalikan matriks dengan ukuran dalam berbeda.", "Periksa shape dulu."),
        M("Mengira A @ B sama dengan B @ A.", "Perkalian matriks tidak komutatif."),
    ],
    [
        Q("Perkalian matriks memakai operator?", ["@", "*", "&", "+"], 0, "At.", hint="At."),
        Q("(2,3) @ (3,4) berbentuk?", ["(2, 4)", "(3, 3)", "(2, 3)", "Galat"], 0, "Ukuran luar.", hint="Luar."),
        Q("Norma Euclid [3, 4]?", ["5", "7", "12", "25"], 0, "Akar 9 + 16.", hint="Pythagoras."),
        Q("Kosinus vektor tegak lurus?", ["0", "1", "-1", "0.5"], 0, "Hasil kali dalam nol.", hint="Nol."),
        Q("A @ B dan B @ A?", ["Umumnya berbeda", "Selalu sama", "Selalu nol", "Galat"], 0, "Tidak komutatif.", hint="Beda."),
    ],
    [
        "Bintang mengalikan elemen, at mengalikan matriks.",
        "Ukuran dalam perkalian matriks harus sama.",
        "Norma dan kosinus mengukur ukuran dan arah vektor.",
        "Kovarians dapat dihitung dengan perkalian matriks data terpusat.",
    ],
    [],
)

G1 = """
import numpy as np

def selesaikan(A, b):
    return np.round(np.linalg.solve(np.asarray(A, dtype=float), np.asarray(b, dtype=float)), 6).tolist()
"""
G2 = """
import numpy as np

def bisa_dibalik(A):
    A = np.asarray(A, dtype=float)
    return bool(A.shape[0] == A.shape[1] and np.linalg.matrix_rank(A) == A.shape[0])
"""
G3 = """
import numpy as np

def regresi_garis(x, y):
    x = np.asarray(x, dtype=float)
    X = np.column_stack([np.ones(len(x)), x])
    koef = np.linalg.lstsq(X, np.asarray(y, dtype=float), rcond=None)[0]
    return (np.round(koef, 6) + 0.0).tolist()
"""
G4 = """
import numpy as np

def kekurangan_rank(A):
    A = np.asarray(A, dtype=float)
    return int(min(A.shape) - np.linalg.matrix_rank(A))
"""

l2 = lesson(
    "B1-05-2",
    "Sistem persamaan, invers, dan kuadrat terkecil",
    35,
    [
        "Menyelesaikan sistem persamaan linear dengan solve",
        "Menghitung determinan, invers, dan rank",
        "Mengenali matriks singular",
        "Memakai lstsq untuk regresi linear",
    ],
    [
        tb("Sistem persamaan linear", "Banyak masalah dapat dituliskan sebagai satu persamaan matriks `A x = b`, dengan A matriks koefisien, x vektor yang dicari, dan b vektor hasil. Misalnya dua persamaan dengan dua bilangan tak diketahui. Fungsi `np.linalg.solve(A, b)` mencari x dengan metode faktorisasi yang cepat dan stabil. Hasilnya dapat diperiksa dengan mengalikan kembali A dengan x dan membandingkannya dengan b."),
        C(
            ind("""
import numpy as np

A = np.array([[1., 2.], [3., 4.]])
b = np.array([5., 11.])
x = np.linalg.solve(A, b)
print(np.round(x, 6).tolist())
print(bool(np.allclose(A @ x, b)))
A2 = np.array([[2., 1.], [1., 3.]])
print(np.round(np.linalg.solve(A2, np.array([3., 5.])), 6).tolist())
"""),
            ind("""
[1.0, 2.0]
True
[0.8, 1.4]
"""),
            "Solve menemukan x dan pemeriksaan A kali x menghasilkan kembali b.",
            filename="solve_dasar.py",
        ),
        tb("Determinan", "Determinan adalah satu angka yang merangkum sifat matriks persegi. Bila determinan nol, matriks tidak punya invers dan sistem tidak punya solusi tunggal. Fungsi `np.linalg.det` menghitungnya. Secara geometris, nilai mutlak determinan adalah faktor perubahan luas atau volume oleh transformasi matriks. Karena hasilnya desimal, bulatkan atau pakai toleransi saat membandingkan dengan nol."),
        tb("Invers", "Invers matriks A, ditulis A pangkat minus satu, adalah matriks yang bila dikalikan dengan A menghasilkan matriks identitas. Fungsi `np.linalg.inv` menghitungnya. Meskipun tampak alami, jarang bijak menghitung invers untuk menyelesaikan sistem: `solve` lebih cepat dan lebih teliti. Invers berguna bila memang dibutuhkan eksplisit, misalnya untuk kovarians presisi."),
        C(
            ind("""
import numpy as np

A = np.array([[1., 2.], [3., 4.]])
print(round(float(np.linalg.det(A)), 4))
inv = np.linalg.inv(A)
print(np.round(inv, 4).tolist())
print(np.round(A @ inv, 6).tolist())
print(round(float(np.linalg.det(np.eye(3) * 2)), 4))
"""),
            ind("""
-2.0
[[-2.0, 1.0], [1.5, -0.5]]
[[1.0, 0.0], [0.0, 1.0]]
8.0
"""),
            "Determinan bukan nol sehingga invers ada, dan kali invers menghasilkan identitas.",
            filename="det_inv.py",
        ),
        tb("Matriks singular", "Matriks yang determinannya nol disebut singular. Baris atau kolomnya bergantung linear, misalnya satu baris merupakan kelipatan baris lain. Matriks ini tidak punya invers, dan `inv` maupun `solve` melempar `LinAlgError`. Pada data nyata, singular persis jarang terjadi, tetapi nyaris singular sering muncul dan membuat hasil tidak stabil, ditandai angka sangat besar pada invers."),
        tb("Rank", "**Rank** matriks adalah jumlah baris atau kolom yang bebas linear. Matriks persegi berukuran n memiliki invers hanya bila rank-nya n. Fungsi `np.linalg.matrix_rank` menghitungnya dengan toleransi numerik. Selisih antara ukuran dan rank menunjukkan seberapa banyak informasi yang berlebihan, dan menjadi petunjuk adanya fitur yang berkorelasi sempurna pada data."),
        C(
            ind("""
import numpy as np

S = np.array([[1., 2.], [2., 4.]])
A = np.array([[1., 2.], [3., 4.]])
print(int(np.linalg.matrix_rank(S)), int(np.linalg.matrix_rank(A)))
print(round(float(np.linalg.det(S)), 6))
try:
    np.linalg.inv(S)
except np.linalg.LinAlgError:
    print('singular')
print(2 - int(np.linalg.matrix_rank(S)))
"""),
            ind("""
1 2
0.0
singular
1
"""),
            "Baris kedua adalah dua kali baris pertama sehingga rank hanya satu, determinan nol, dan invers gagal.",
            filename="singular.py",
        ),
        tb("Lebih banyak persamaan daripada bilangan tak diketahui", "Pada data nyata, kita sering punya lebih banyak pengamatan daripada parameter, dan tidak ada solusi yang memenuhi semuanya persis akibat derau. Pendekatan **kuadrat terkecil** mencari x yang meminimalkan jumlah kuadrat selisih antara `A x` dan b. Fungsi `np.linalg.lstsq` menyelesaikannya dan juga bekerja pada matriks yang tidak persegi atau berrank kurang."),
        tb("Regresi linear dengan lstsq", "Untuk menyesuaikan garis `y = a + b x`, bangun matriks desain berkolom satu dan x. Kolom satu mewakili intersep. Panggil `lstsq` dengan matriks itu dan y, dan hasil pertamanya adalah koefisien intersep dan kemiringan. Teknik ini setara dengan regresi linear sederhana, dan memperluasnya ke banyak fitur cukup dengan menambah kolom pada matriks desain."),
        C(
            ind("""
import numpy as np

x = np.array([1., 2., 3., 4.])
X = np.column_stack([np.ones(4), x])
for y in (np.array([2., 4., 6., 8.]), np.array([3., 5., 7., 9.])):
    koef, res, rank, sv = np.linalg.lstsq(X, y, rcond=None)
    print(np.round(koef, 6).tolist(), int(rank))
print(X.shape)
"""),
            ind("""
[0.0, 2.0]
2
[1.0, 2.0]
2
(4, 2)
"""),
            "Garis sempurna menghasilkan intersep dan kemiringan tepat. Kolom satu memungkinkan intersep.",
            filename="lstsq_garis.py",
        ),
        tb("Mengapa tidak memakai invers", "Rumus buku teks untuk regresi memakai invers dari transpos X kali X. Menghitungnya langsung dapat tidak stabil, terutama bila fitur berkorelasi tinggi. Fungsi `lstsq` memakai dekomposisi yang lebih stabil. Pada praktik, pustaka seperti scikit-learn juga menghindari invers eksplisit, jadi kebiasaan ini sejalan dengan yang dilakukan alat standar."),
        tb("Memeriksa kualitas solusi", "Setelah menyelesaikan, periksa residu, yaitu selisih antara `A @ x` dan b. Pada sistem persegi yang tepat, residu mendekati nol. Pada kuadrat terkecil, residu adalah galat model dan norma-nya menunjukkan kecocokan. Bila angka kondisi matriks besar, `np.linalg.cond`, solusi sangat peka terhadap derau kecil dan perlu dicurigai."),
        K("warn", "Hindari np.linalg.inv untuk menyelesaikan sistem. Pakai solve atau lstsq yang lebih cepat dan teliti.", title="Jangan balik matriks"),
        tb("Angka kondisi", "Angka kondisi, dihitung dengan `np.linalg.cond`, adalah rasio nilai singular terbesar terhadap terkecil. Angka kecil berarti sistem stabil, sedangkan angka sangat besar berarti perubahan kecil pada masukan dapat mengubah solusi secara drastis. Matriks nyaris singular memiliki angka kondisi raksasa. Periksa angka ini sebelum mempercayai solusi, terutama pada regresi dengan fitur yang berkorelasi tinggi."),
        tb("Regresi banyak fitur", "Perluasan ke banyak fitur sederhana: matriks desain berisi kolom satu diikuti satu kolom per fitur, dan `lstsq` mengembalikan satu koefisien per kolom. Prediksi untuk data baru adalah perkalian matriks desain baru dengan koefisien itu. Seluruh regresi linear berganda dengan demikian hanya beberapa baris NumPy, dan hasilnya sama dengan yang dikeluarkan pustaka statistik."),
        tb("Residu dan galat", "Residu adalah selisih antara nilai pengamatan dan prediksi. Jumlah kuadrat residu menunjukkan seberapa baik garis mencocokkan data, dan akar rata-ratanya adalah galat akar rata-rata kuadrat. Selalu hitung galat ini pada data yang tidak dipakai untuk menyesuaikan model agar tidak tertipu oleh kecocokan berlebihan."),
        E(
            "B1-05-2-ex1",
            "mudah",
            "Tulis fungsi `selesaikan(A, b)` yang mengembalikan solusi `x` dari `A x = b`, dibulatkan ke enam desimal sebagai list Python.",
            ind("""
import numpy as np

def selesaikan(A, b):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

assert selesaikan([[1, 2], [3, 4]], [5, 11]) == [1.0, 2.0]
assert selesaikan([[2, 1], [1, 3]], [3, 5]) == [0.8, 1.4]
assert selesaikan([[1, 0], [0, 1]], [7, 9]) == [7.0, 9.0]
assert selesaikan([[2]], [8]) == [4.0]
"""),
            "Gunakan np.linalg.solve lalu bulatkan.",
            G1.strip("\n"),
        ),
        E(
            "B1-05-2-ex2",
            "sedang",
            "Tulis fungsi `bisa_dibalik(A)` yang mengembalikan `True` bila matriks `A` persegi dan rank-nya penuh, dan `False` bila tidak, sebagai bool Python.",
            ind("""
import numpy as np

def bisa_dibalik(A):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

assert bisa_dibalik([[1, 2], [3, 4]]) is True
assert bisa_dibalik([[1, 2], [2, 4]]) is False
assert bisa_dibalik([[1, 2, 3], [4, 5, 6]]) is False
assert bisa_dibalik(np.eye(3)) is True
"""),
            "Periksa bentuk persegi dan rank sama dengan ukurannya.",
            G2.strip("\n"),
        ),
        E(
            "B1-05-2-ex3",
            "sedang",
            "Tulis fungsi `regresi_garis(x, y)` yang mengembalikan list `[intersep, kemiringan]` dari garis kuadrat terkecil `y = intersep + kemiringan * x`, dibulatkan ke enam desimal.",
            ind("""
import numpy as np

def regresi_garis(x, y):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

assert regresi_garis([1, 2, 3, 4], [2, 4, 6, 8]) == [0.0, 2.0]
assert regresi_garis([1, 2, 3, 4], [3, 5, 7, 9]) == [1.0, 2.0]
assert regresi_garis([0, 1, 2], [5, 5, 5]) == [5.0, 0.0]
assert regresi_garis([0, 1], [1, 0]) == [1.0, -1.0]
"""),
            "Bangun matriks desain dengan kolom satu dan x lalu pakai lstsq.",
            G3.strip("\n"),
        ),
        E(
            "B1-05-2-ex4",
            "menantang",
            "Tulis fungsi `kekurangan_rank(A)` yang mengembalikan selisih antara ukuran terkecil matriks `A` dan rank-nya sebagai bilangan bulat Python.",
            ind("""
import numpy as np

def kekurangan_rank(A):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

assert kekurangan_rank([[1, 2], [2, 4]]) == 1
assert kekurangan_rank([[1, 2], [3, 4]]) == 0
assert kekurangan_rank([[1, 2, 3], [2, 4, 6]]) == 1
assert kekurangan_rank(np.zeros((3, 3))) == 3
"""),
            "Kurangkan matrix_rank dari min shape.",
            G4.strip("\n"),
        ),
    ],
    [
        M("Menghitung invers untuk menyelesaikan sistem.", "Pakai solve atau lstsq."),
        M("Membandingkan determinan dengan nol memakai sama dengan.", "Pakai toleransi atau rank."),
        M("Lupa kolom satu untuk intersep pada regresi.", "Tambahkan kolom konstan pada matriks desain."),
    ],
    [
        Q("Fungsi menyelesaikan A x = b?", ["np.linalg.solve", "np.dot", "np.sum", "np.eye"], 0, "Solve.", hint="Solve."),
        Q("Matriks singular memiliki?", ["Determinan nol", "Determinan satu", "Rank penuh", "Invers"], 0, "Tidak punya invers.", hint="Nol."),
        Q("Rank menyatakan?", ["Jumlah baris bebas linear", "Jumlah elemen", "Jumlah nol", "Ukuran"], 0, "Bebas linear.", hint="Bebas."),
        Q("lstsq meminimalkan?", ["Jumlah kuadrat galat", "Jumlah elemen", "Determinan", "Rank"], 0, "Kuadrat terkecil.", hint="Kuadrat."),
        Q("Kolom satu pada matriks desain untuk?", ["Intersep", "Kemiringan", "Galat", "Rank"], 0, "Konstanta.", hint="Intersep."),
    ],
    [
        "solve menyelesaikan sistem persegi dengan stabil.",
        "Determinan nol atau rank kurang berarti matriks singular.",
        "Hindari invers eksplisit untuk menyelesaikan sistem.",
        "lstsq menyelesaikan kuadrat terkecil dan regresi linear.",
    ],
    [],
)

H1 = """
import numpy as np

def nilai_eigen_simetris(M):
    return np.round(np.linalg.eigvalsh(np.asarray(M, dtype=float)), 6).tolist()
"""
H2 = """
import numpy as np

def nilai_singular(M):
    return np.round(np.linalg.svd(np.asarray(M, dtype=float), compute_uv=False), 4).tolist()
"""
H3 = """
import numpy as np

def proporsi_varians_pertama(X):
    ev = np.linalg.eigvalsh(np.cov(np.asarray(X, dtype=float).T))
    return round(float(ev.max() / ev.sum()), 4)
"""
H4 = """
import numpy as np

def aproksimasi_rank1(M):
    U, s, Vt = np.linalg.svd(np.asarray(M, dtype=float))
    return (np.round(s[0] * np.outer(U[:, 0], Vt[0]), 4) + 0.0).tolist()
"""

l3 = lesson(
    "B1-05-3",
    "Eigen, SVD, dan aplikasinya",
    35,
    [
        "Menjelaskan nilai eigen dan vektor eigen",
        "Menghitung eigen untuk matriks simetris dengan eigh",
        "Menghitung SVD dan memakainya untuk aproksimasi rank rendah",
        "Menghubungkan eigen dan SVD dengan PCA",
    ],
    [
        tb("Arah yang tidak berubah", "Sebuah matriks mengubah vektor, biasanya mengubah arah sekaligus panjangnya. Namun ada vektor khusus yang arahnya tidak berubah, hanya panjangnya dikalikan suatu angka. Vektor itu disebut **vektor eigen** dan angkanya **nilai eigen**. Bila `A v = lambda v`, maka v vektor eigen dan lambda nilai eigennya. Konsep ini menangkap sumbu utama kerja sebuah transformasi linear."),
        tb("Menghitung eigen", "Fungsi `np.linalg.eig` menghitung nilai dan vektor eigen untuk matriks persegi umum, dan hasilnya bisa berupa bilangan kompleks. Untuk matriks simetris, seperti matriks kovarians, pakai `np.linalg.eigh`, yang lebih cepat, selalu menghasilkan bilangan real, dan mengurutkan nilai eigen dari kecil ke besar. Untuk hanya nilainya, `eigvalsh` cukup. Vektor eigen disimpan sebagai kolom matriks hasil."),
        C(
            ind("""
import numpy as np

M = np.array([[2., 1.], [1., 2.]])
w, V = np.linalg.eigh(M)
print(np.round(w, 6).tolist())
print(bool(np.allclose(M @ V, V * w)))
D = np.array([[2., 0.], [0., 3.]])
print(np.linalg.eigvalsh(D).tolist())
G = np.array([[4., 1.], [2., 3.]])
print(np.round(np.sort(np.linalg.eigvals(G).real), 4).tolist())
"""),
            ind("""
[1.0, 3.0]
True
[2.0, 3.0]
[2.0, 5.0]
"""),
            "Persamaan A kali V sama dengan V dikali w membuktikan kolom V adalah vektor eigen. Matriks diagonal punya nilai eigen pada diagonalnya.",
            filename="eigen_dasar.py",
        ),
        tb("Eigen dan matriks kovarians", "Pada matriks kovarians data, vektor eigen menunjuk arah variasi terbesar dalam data, dan nilai eigen yang bersesuaian adalah besar ragam pada arah itu. Itulah dasar **analisis komponen utama**, atau PCA. Arah dengan nilai eigen terbesar adalah komponen utama pertama, arah tegak lurusnya yang berikut adalah komponen kedua, dan seterusnya."),
        C(
            ind("""
import numpy as np

X = np.array([[1., 0.], [-1., 0.], [0., 1.], [0., -1.]])
ev = np.linalg.eigvalsh(np.cov(X.T))
print(round(float(ev.max() / ev.sum()), 4))
Y = np.array([[1., 2.], [2., 4.], [3., 6.], [4., 8.]])
ev2 = np.linalg.eigvalsh(np.cov(Y.T))
print(round(float(ev2.max() / ev2.sum()), 4))
print(np.round(ev2, 4).tolist())
"""),
            ind("""
0.5
1.0
[0.0, 8.3333]
"""),
            "Data tersebar merata memberi komponen pertama separuh ragam. Data yang terletak pada satu garis memberi seluruh ragam pada komponen pertama.",
            filename="eigen_pca.py",
        ),
        tb("Dekomposisi nilai singular", "SVD menguraikan sebarang matriks, tidak harus persegi, menjadi tiga faktor: `A = U S Vt`. U dan Vt berisi arah-arah yang saling tegak lurus, dan S adalah deretan nilai singular tidak negatif yang diurutkan dari besar ke kecil. Fungsi `np.linalg.svd` mengembalikan U, vektor nilai singular, dan Vt. SVD lebih umum dan lebih stabil daripada eigen, dan menjadi dasar banyak algoritma praktis."),
        tb("Nilai singular dan rank", "Banyaknya nilai singular yang tidak nol sama dengan rank matriks. Nilai singular yang sangat kecil menandakan arah yang nyaris tidak membawa informasi. Rasio nilai singular terbesar terhadap terkecil adalah angka kondisi, ukuran seberapa sensitif sistem terhadap derau. Dengan melihat spektrum nilai singular, kita dapat menilai berapa dimensi efektif data sebenarnya."),
        C(
            ind("""
import numpy as np

U, s, Vt = np.linalg.svd(np.array([[3., 0.], [0., 4.]]))
print(s.tolist())
print(np.round(np.linalg.svd(np.array([[1., 2.], [2., 4.]]), compute_uv=False), 4).tolist())
print(np.round(np.linalg.svd(np.array([[1., 2.], [3., 4.]]), compute_uv=False), 4).tolist())
M = np.array([[1., 2.], [3., 4.]])
U, s, Vt = np.linalg.svd(M)
print(bool(np.allclose(U @ np.diag(s) @ Vt, M)))
"""),
            ind("""
[4.0, 3.0]
[5.0, 0.0]
[5.465, 0.366]
True
"""),
            "Matriks rank satu hanya punya satu nilai singular tidak nol. Perkalian tiga faktor mengembalikan matriks asli.",
            filename="svd_dasar.py",
        ),
        tb("Aproksimasi rank rendah", "Teorema Eckart-Young menyatakan bahwa aproksimasi terbaik rank k dari sebuah matriks diperoleh dengan mempertahankan k nilai singular terbesar dan membuang sisanya. Aproksimasi rank satu adalah nilai singular pertama dikali hasil kali luar kolom pertama U dan baris pertama Vt. Teknik ini dipakai untuk mengompresi gambar, membuang derau, dan menemukan struktur laten pada data."),
        C(
            ind("""
import numpy as np

for M in ([[3., 0.], [0., 4.]], [[1., 2.], [2., 4.]], [[1., 2.], [3., 4.]]):
    U, s, Vt = np.linalg.svd(np.array(M))
    r1 = s[0] * np.outer(U[:, 0], Vt[0])
    print((np.round(r1, 4) + 0.0).tolist())
"""),
            ind("""
[[0.0, 0.0], [0.0, 4.0]]
[[1.0, 2.0], [2.0, 4.0]]
[[1.2736, 1.8072], [2.879, 4.0853]]
"""),
            "Matriks yang sudah rank satu tidak berubah. Matriks lain didekati oleh matriks rank satu terdekat.",
            filename="aproksimasi_rank1.py",
        ),
        tb("PCA lewat SVD", "Dalam praktik, PCA biasanya dihitung dengan SVD data terpusat, bukan dengan eigen dari kovarians, karena lebih stabil. Baris Vt adalah komponen utama, dan kuadrat nilai singular dibagi n dikurangi satu adalah ragam yang dijelaskan tiap komponen. Mengalikan data terpusat dengan komponen terpilih memproyeksikan data ke dimensi lebih rendah sambil mempertahankan sebanyak mungkin ragam."),
        tb("Kapan memakai yang mana", "Gunakan `eigh` untuk matriks simetris seperti kovarians, `eig` untuk matriks persegi umum, dan `svd` untuk matriks apa pun, terutama bila Anda butuh stabilitas atau aproksimasi rank rendah. Bila data besar dan hanya beberapa komponen yang dibutuhkan, algoritma terpotong dari scipy atau scikit-learn jauh lebih hemat dibanding SVD penuh dari NumPy."),
        tb("Ringkasan modul", "Anda telah belajar perkalian matriks, norma, penyelesaian sistem, kuadrat terkecil, eigen, dan SVD. Semuanya dipanggil dengan beberapa baris NumPy namun mendasari regresi, PCA, dan rekomendasi. Modul terakhir kursus ini membahas pembangkit acak, reproduksibilitas, dan performa, yang melengkapi perangkat NumPy Anda."),
        K("tip", "Matriks kovarians dan Gram simetris, jadi pakai eigh. Untuk matriks umum atau stabilitas lebih baik, pakai svd.", title="Pilih alat"),
        tb("Pengaruh skala", "Nilai singular dan eigen dipengaruhi skala fitur. Fitur berskala besar mendominasi komponen utama bila data tidak distandarisasi. Karena itu PCA biasanya didahului pemusatan dan sering standarisasi, terutama bila fitur memakai satuan berbeda. Lupa memusatkan data adalah kesalahan umum yang membuat komponen pertama sekadar menunjuk ke arah rata-rata."),
        tb("Tanda vektor eigen", "Vektor eigen tidak unik dalam tanda: jika v adalah vektor eigen, minus v juga. Hasil dari pustaka dapat berbeda tanda antar versi atau mesin. Jangan menulis uji yang membandingkan vektor eigen langsung, melainkan bandingkan besaran yang tidak bergantung tanda seperti nilai eigen, hasil kali luar, atau persamaan A v sama dengan lambda v."),
        E(
            "B1-05-3-ex1",
            "mudah",
            "Tulis fungsi `nilai_eigen_simetris(M)` yang mengembalikan nilai eigen matriks simetris `M` terurut naik, dibulatkan ke enam desimal, sebagai list Python.",
            ind("""
import numpy as np

def nilai_eigen_simetris(M):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

assert nilai_eigen_simetris([[2, 1], [1, 2]]) == [1.0, 3.0]
assert nilai_eigen_simetris([[2, 0], [0, 3]]) == [2.0, 3.0]
assert nilai_eigen_simetris([[5]]) == [5.0]
assert nilai_eigen_simetris([[0, 1], [1, 0]]) == [-1.0, 1.0]
"""),
            "Gunakan np.linalg.eigvalsh lalu bulatkan.",
            H1.strip("\n"),
        ),
        E(
            "B1-05-3-ex2",
            "sedang",
            "Tulis fungsi `nilai_singular(M)` yang mengembalikan nilai singular matriks `M` terurut turun, dibulatkan ke empat desimal, sebagai list Python.",
            ind("""
import numpy as np

def nilai_singular(M):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

assert nilai_singular([[3, 0], [0, 4]]) == [4.0, 3.0]
assert nilai_singular([[1, 2], [2, 4]]) == [5.0, 0.0]
assert nilai_singular([[1, 2], [3, 4]]) == [5.465, 0.366]
assert nilai_singular([[1, 0, 0]]) == [1.0]
"""),
            "svd dengan compute_uv bernilai False.",
            H2.strip("\n"),
        ),
        E(
            "B1-05-3-ex3",
            "sedang",
            "Tulis fungsi `proporsi_varians_pertama(X)` yang mengembalikan bagian ragam total yang dijelaskan komponen utama pertama dari data `X` (baris adalah sampel), yaitu nilai eigen kovarians terbesar dibagi jumlah semua nilai eigen, dibulatkan ke empat desimal.",
            ind("""
import numpy as np

def proporsi_varians_pertama(X):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

assert proporsi_varians_pertama([[1, 0], [-1, 0], [0, 1], [0, -1]]) == 0.5
assert proporsi_varians_pertama([[1, 2], [2, 4], [3, 6], [4, 8]]) == 1.0
assert proporsi_varians_pertama([[1, 0], [-1, 0], [2, 0], [-2, 0]]) == 1.0
assert 0.5 <= proporsi_varians_pertama([[1, 2], [2, 1], [3, 5], [4, 2]]) <= 1.0
"""),
            "Hitung eigvalsh dari np.cov(X.T) lalu bagi maksimum dengan jumlah.",
            H3.strip("\n"),
        ),
        E(
            "B1-05-3-ex4",
            "menantang",
            "Tulis fungsi `aproksimasi_rank1(M)` yang mengembalikan aproksimasi rank satu terbaik matriks `M` lewat SVD, dibulatkan ke empat desimal, sebagai list Python.",
            ind("""
import numpy as np

def aproksimasi_rank1(M):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

assert aproksimasi_rank1([[3, 0], [0, 4]]) == [[0.0, 0.0], [0.0, 4.0]]
assert aproksimasi_rank1([[1, 2], [2, 4]]) == [[1.0, 2.0], [2.0, 4.0]]
assert aproksimasi_rank1([[1, 2], [3, 4]]) == [[1.2736, 1.8072], [2.879, 4.0853]]
assert np.linalg.svd(np.array(aproksimasi_rank1([[1, 2], [3, 4]])), compute_uv=False)[1] < 0.001
"""),
            "Nilai singular pertama dikali outer dari kolom pertama U dan baris pertama Vt.",
            H4.strip("\n"),
        ),
    ],
    [
        M("Memakai eig untuk matriks simetris.", "Pakai eigh agar real dan terurut."),
        M("Mengira vektor eigen ada pada baris hasil.", "Vektor eigen adalah kolom."),
        M("Mengabaikan nilai singular yang sangat kecil.", "Nilai kecil menandakan rank kurang atau kondisi buruk."),
    ],
    [
        Q("A v = lambda v berarti v adalah?", ["Vektor eigen", "Vektor nol", "Invers", "Norma"], 0, "Arah tidak berubah.", hint="Eigen."),
        Q("Fungsi eigen untuk matriks simetris?", ["eigh", "solve", "inv", "dot"], 0, "Eigh.", hint="h."),
        Q("Komponen utama pertama adalah arah dengan?", ["Ragam terbesar", "Ragam nol", "Rata-rata terbesar", "Rank satu"], 0, "Nilai eigen terbesar.", hint="Terbesar."),
        Q("Banyak nilai singular tak nol sama dengan?", ["Rank", "Determinan", "Trace", "Norma"], 0, "Rank.", hint="Rank."),
        Q("Aproksimasi rank k mempertahankan?", ["k nilai singular terbesar", "k elemen pertama", "k baris", "k nol"], 0, "Eckart-Young.", hint="Terbesar."),
    ],
    [
        "Vektor eigen adalah arah yang tidak berubah oleh matriks.",
        "Untuk matriks simetris pakai eigh, untuk umum pakai svd.",
        "SVD menguraikan matriks dan menentukan rank serta aproksimasi.",
        "PCA memakai eigen kovarians atau SVD data terpusat.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perintah yang cukup jelas dalam teks.", "brief": []}

write_module(
    "B1",
    5,
    "Aljabar linear dengan NumPy",
    105,
    [
        "Mengalikan matriks dan mengukur vektor dengan benar",
        "Menyelesaikan sistem dan regresi dengan solve dan lstsq",
        "Memakai eigen dan SVD untuk PCA dan aproksimasi rank rendah",
    ],
    [l1, l2, l3],
    video,
    REF,
)
