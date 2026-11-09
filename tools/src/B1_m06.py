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

def acak_seed(seed, n):
    return np.random.default_rng(seed).integers(0, 100, n).tolist()
"""
F2 = """
import numpy as np

def bagi_indeks(n, rasio, seed):
    urutan = np.random.default_rng(seed).permutation(n)
    batas = int(n * rasio)
    return (urutan[:batas].tolist(), urutan[batas:].tolist())
"""
F3 = """
import numpy as np

def dua_aliran(seed):
    anak = np.random.SeedSequence(seed).spawn(2)
    g1, g2 = [np.random.default_rng(s) for s in anak]
    return (g1.random(3).tolist(), g2.random(3).tolist())
"""
F4 = """
import numpy as np

def rata_normal(seed, n, mu, sigma):
    return float(np.random.default_rng(seed).normal(mu, sigma, n).mean())
"""

l1 = lesson(
    "B1-06-1",
    "Generator acak dan seed",
    35,
    [
        "Memakai Generator modern lewat default_rng",
        "Menghasilkan bilangan bulat, uniform, dan normal",
        "Mengocok dan mengambil permutasi secara terkendali",
        "Membuat aliran acak independen dengan SeedSequence",
    ],
    [
        tb("Keacakan di komputer", "Komputer tidak benar-benar menghasilkan bilangan acak. Ia memakai algoritma deterministik yang menghasilkan deret yang tampak acak dari nilai awal bernama **seed**. Seed yang sama selalu menghasilkan deret yang sama. Sifat ini sebenarnya anugerah bagi analisis data: kita dapat memakai pengacakan untuk simulasi dan pembagian data, sekaligus tetap dapat mengulang hasilnya persis, sesuai prinsip reproduksibilitas."),
        tb("Dua antarmuka NumPy", "NumPy memiliki antarmuka lama berupa `np.random.seed` dan fungsi seperti `np.random.rand`, dan antarmuka modern berupa objek **Generator** yang dibuat dengan `np.random.default_rng(seed)`. Antarmuka lama memakai satu keadaan global yang dipakai bersama semua kode, sehingga pustaka lain dapat mengganggunya. Antarmuka modern menyimpan keadaan dalam objek lokal, lebih aman, lebih cepat, dan direkomendasikan untuk semua kode baru."),
        tb("Membuat generator", "Panggil `rng = np.random.default_rng(42)` sekali di awal skrip atau fungsi, lalu pakai `rng` untuk semua pengacakan berikutnya. Jangan membuat generator baru dengan seed sama di tiap panggilan, karena setiap panggilan akan menghasilkan angka yang persis sama. Bila seed tidak diberikan, NumPy mengambil entropi dari sistem sehingga hasilnya berbeda setiap kali, cocok untuk eksplorasi tetapi tidak untuk hasil yang harus dilaporkan."),
        C(
            ind("""
import numpy as np

a = np.random.default_rng(1).integers(0, 100, 5).tolist()
b = np.random.default_rng(1).integers(0, 100, 5).tolist()
c = np.random.default_rng(2).integers(0, 100, 5).tolist()
print(a == b)
print(a == c)
rng = np.random.default_rng(1)
p = rng.integers(0, 100, 5).tolist()
q = rng.integers(0, 100, 5).tolist()
print(p == a, p == q)
"""),
            ind("""
True
False
True False
"""),
            "Seed sama menghasilkan deret sama. Namun generator yang sama dipanggil dua kali melanjutkan deretnya sehingga hasil kedua berbeda.",
            filename="seed_generator.py",
        ),
        tb("Jenis distribusi dasar", "Generator menyediakan metode untuk distribusi umum. `rng.random(n)` menghasilkan bilangan seragam di antara nol dan satu. `rng.integers(a, b, n)` menghasilkan bilangan bulat dari a sampai sebelum b. `rng.normal(mu, sigma, n)` menghasilkan sebaran normal. Ada pula `binomial`, `poisson`, `exponential`, dan banyak lagi. Argumen `size` boleh berupa tuple untuk menghasilkan array berdimensi banyak sekaligus."),
        C(
            ind("""
import numpy as np

rng = np.random.default_rng(3)
u = rng.random(5)
print(bool(((u >= 0) & (u < 1)).all()))
k = rng.integers(10, 20, 1000)
print(int(k.min()) >= 10, int(k.max()) <= 19)
x = rng.normal(10, 1, 100000)
print(abs(float(x.mean()) - 10) < 0.05)
print(abs(float(x.std()) - 1) < 0.05)
print(rng.random((2, 3)).shape)
"""),
            ind("""
True
True True
True
True
(2, 3)
"""),
            "Tiap metode menghasilkan array dengan sifat statistik yang diharapkan, dan argumen ukuran tuple membuat array berdimensi banyak.",
            filename="distribusi_dasar.py",
        ),
        tb("Menguji sifat, bukan nilai", "Karena aliran acak dapat berbeda antar versi pustaka, jangan menulis uji yang membandingkan angka persis hasil pengacakan. Ujilah sifatnya: panjang, rentang, rata-rata mendekati yang diharapkan, dan kesamaan antar dua run dengan seed sama. Dengan begitu uji tetap lolos walau implementasi internal NumPy berubah, tetapi tetap menangkap kesalahan nyata."),
        tb("Mengocok dan permutasi", "Metode `rng.shuffle(a)` mengocok array di tempat dan tidak mengembalikan apa-apa. Metode `rng.permutation(n)` mengembalikan permutasi baru dari bilangan nol sampai n minus satu, atau salinan terkocok bila diberi array. Permutasi indeks adalah dasar pembagian data: kocok indeks lalu potong. Cara ini juga memudahkan menjaga label dan fitur tetap sejajar."),
        C(
            ind("""
import numpy as np

rng = np.random.default_rng(0)
p = rng.permutation(10)
print(sorted(p.tolist()))
a = np.arange(6)
rng.shuffle(a)
print(sorted(a.tolist()))
rng2 = np.random.default_rng(0)
print(rng2.permutation(10).tolist() == p.tolist())
idx = np.random.default_rng(5).permutation(5)
x = np.array([10, 20, 30, 40, 50])
y = np.array([1, 2, 3, 4, 5])
print((x[idx] // 10 == y[idx]).all())
"""),
            ind("""
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
[0, 1, 2, 3, 4, 5]
True
True
"""),
            "Permutasi memuat semua indeks tepat sekali. Dengan indeks yang sama, fitur dan label tetap berpasangan.",
            filename="permutasi.py",
        ),
        tb("Aliran independen", "Dalam simulasi paralel atau eksperimen berulang, kita butuh banyak generator yang tidak saling berkorelasi. Memakai seed berurutan seperti 1, 2, 3 secara teori sah, tetapi cara resminya adalah `np.random.SeedSequence(seed).spawn(k)` yang menurunkan k benih anak yang dijamin independen. Setiap anak diberikan ke `default_rng`. Ini aman diulang, karena benih induk yang sama selalu menurunkan benih anak yang sama."),
        C(
            ind("""
import numpy as np

anak = np.random.SeedSequence(5).spawn(2)
g1, g2 = [np.random.default_rng(s) for s in anak]
r1 = g1.random(3).tolist()
r2 = g2.random(3).tolist()
print(r1 != r2)
anak2 = np.random.SeedSequence(5).spawn(2)
h1 = np.random.default_rng(anak2[0]).random(3).tolist()
print(h1 == r1)
"""),
            ind("""
True
True
"""),
            "Dua anak benih menghasilkan aliran berbeda, dan induk yang sama menurunkan anak yang sama sehingga dapat diulang.",
            filename="seed_sequence.py",
        ),
        tb("Menyimpan seed", "Catat seed yang dipakai bersama hasil analisis, misalnya di log run atau file konfigurasi. Bila hasil menarik muncul dari seed tertentu, tanpa catatan itu Anda tidak dapat mengulangnya. Hindari memilih seed demi hasil yang bagus karena itu bentuk manipulasi. Cara jujur: jalankan beberapa seed, laporkan sebaran hasilnya, dan sebutkan seed yang dipakai."),
        tb("Antarmuka lama", "Anda akan menemukan `np.random.seed(0)` dan `np.random.rand` pada banyak kode lama dan tutorial. Keduanya tetap berfungsi, tetapi memengaruhi keadaan global. Pustaka seperti scikit-learn menerima parameter `random_state` yang dapat berupa bilangan bulat atau generator. Bila menulis fungsi sendiri, terimalah parameter seed atau generator agar pemanggil mengendalikan keacakan."),
        K("tip", "Buat satu generator di awal dan teruskan ke fungsi yang membutuhkannya. Jangan membuat generator baru dengan seed sama berulang kali.", title="Satu generator"),
        tb("Keacakan dan tipe data", "Metode acak mengembalikan tipe sesuai kebutuhan. `integers` menghasilkan bilangan bulat, `random` menghasilkan desimal, dan `choice` mengembalikan tipe elemen sumbernya. Gunakan argumen `dtype` bila perlu menghemat memori, misalnya float32 untuk data besar. Ingat bahwa mengubah tipe tidak mengubah deret acak yang mendasarinya, hanya cara bilangan itu disimpan."),
        E(
            "B1-06-1-ex1",
            "mudah",
            "Tulis fungsi `acak_seed(seed, n)` yang mengembalikan list `n` bilangan bulat acak dari 0 sampai 99 memakai `np.random.default_rng(seed)`, sehingga seed sama selalu menghasilkan list sama.",
            ind("""
import numpy as np

def acak_seed(seed, n):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

a = acak_seed(1, 10)
assert len(a) == 10 and all(isinstance(v, int) and 0 <= v <= 99 for v in a)
assert a == acak_seed(1, 10)
assert a != acak_seed(2, 10)
assert acak_seed(3, 0) == []
"""),
            "Buat default_rng dengan seed lalu panggil integers dan tolist.",
            F1.strip("\n"),
        ),
        E(
            "B1-06-1-ex2",
            "sedang",
            "Tulis fungsi `bagi_indeks(n, rasio, seed)` yang mengocok indeks 0 sampai `n - 1` dengan `default_rng(seed).permutation` dan mengembalikan tuple `(latih, uji)` berupa dua list, dengan `latih` berisi `int(n * rasio)` indeks pertama.",
            ind("""
import numpy as np

def bagi_indeks(n, rasio, seed):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

latih, uji = bagi_indeks(10, 0.7, 4)
assert len(latih) == 7 and len(uji) == 3
assert sorted(latih + uji) == list(range(10))
assert set(latih).isdisjoint(set(uji))
assert bagi_indeks(10, 0.7, 4) == (latih, uji)
assert bagi_indeks(10, 0.7, 5) != (latih, uji)
"""),
            "Permutasi indeks lalu potong pada batas.",
            F2.strip("\n"),
        ),
        E(
            "B1-06-1-ex3",
            "sedang",
            "Tulis fungsi `dua_aliran(seed)` yang menurunkan dua benih anak dari `np.random.SeedSequence(seed).spawn(2)`, membuat satu generator dari tiap anak, dan mengembalikan tuple berisi tiga bilangan `random(3)` dari masing-masing generator sebagai dua list.",
            ind("""
import numpy as np

def dua_aliran(seed):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

r = dua_aliran(5)
assert len(r) == 2 and len(r[0]) == 3 and len(r[1]) == 3
assert r[0] != r[1]
assert dua_aliran(5) == r
assert dua_aliran(6) != r
"""),
            "Spawn dua anak lalu buat default_rng dari masing-masing.",
            F3.strip("\n"),
        ),
        E(
            "B1-06-1-ex4",
            "menantang",
            "Tulis fungsi `rata_normal(seed, n, mu, sigma)` yang mengembalikan rata-rata `n` bilangan acak berdistribusi normal dengan rata-rata `mu` dan simpangan baku `sigma` dari `default_rng(seed)`, sebagai float Python.",
            ind("""
import numpy as np

def rata_normal(seed, n, mu, sigma):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

m = rata_normal(1, 100000, 10, 1)
assert type(m) is float
assert abs(m - 10) < 0.05
assert m == rata_normal(1, 100000, 10, 1)
assert abs(rata_normal(2, 100000, -3, 2) + 3) < 0.1
"""),
            "Metode normal menerima rata-rata, simpangan baku, dan jumlah.",
            F4.strip("\n"),
        ),
    ],
    [
        M("Membuat generator baru dengan seed sama di tiap panggilan.", "Buat satu generator dan pakai berulang."),
        M("Menguji angka persis hasil pengacakan.", "Uji sifat dan kesamaan antar run."),
        M("Memakai np.random.seed global di pustaka.", "Terima seed atau generator sebagai parameter."),
    ],
    [
        Q("Seed berfungsi?", ["Menetapkan deret acak yang bisa diulang", "Mempercepat", "Mengurutkan", "Menyimpan"], 0, "Nilai awal.", hint="Awal."),
        Q("Antarmuka modern?", ["default_rng", "np.random.seed", "random.random", "np.rand"], 0, "Generator.", hint="Generator."),
        Q("rng.integers(0, 10, 5) menghasilkan?", ["Lima bilangan 0 sampai 9", "Lima bilangan 0 sampai 10", "Sepuluh bilangan", "Lima desimal"], 0, "Batas atas tidak termasuk.", hint="Tidak termasuk."),
        Q("Aliran independen dibuat dengan?", ["SeedSequence.spawn", "seed berurutan", "shuffle", "copy"], 0, "Anak benih.", hint="Spawn."),
        Q("Yang sebaiknya diuji pada kode acak?", ["Sifat hasil", "Angka persis", "Kecepatan", "Nama variabel"], 0, "Tahan perubahan versi.", hint="Sifat."),
    ],
    [
        "Seed membuat deret acak dapat diulang.",
        "default_rng membuat Generator lokal yang lebih aman dari keadaan global.",
        "permutation dan shuffle mengocok data, indeks dipakai agar label tetap sejajar.",
        "SeedSequence.spawn menurunkan aliran independen yang dapat diulang.",
    ],
    [],
)

G1 = """
import numpy as np

def sampel_tanpa_ulang(n, k, seed):
    return np.random.default_rng(seed).choice(n, k, replace=False).tolist()
"""
G2 = """
import numpy as np

def taksir_pi(seed, n):
    titik = np.random.default_rng(seed).random((n, 2))
    return float(4 * np.mean((titik ** 2).sum(axis=1) <= 1))
"""
G3 = """
import numpy as np

def bootstrap_rata(data, B, seed):
    rng = np.random.default_rng(seed)
    data = np.asarray(data, dtype=float)
    return np.array([rng.choice(data, len(data)).mean() for _ in range(B)])
"""
G4 = """
import numpy as np

def jalan_acak(seed, n):
    langkah = np.random.default_rng(seed).choice([-1, 1], n)
    return langkah.cumsum().tolist()
"""

l2 = lesson(
    "B1-06-2",
    "Sampling, simulasi, dan bootstrap",
    35,
    [
        "Mengambil sampel dengan dan tanpa pengembalian",
        "Menjalankan simulasi Monte Carlo sederhana",
        "Menghitung bootstrap untuk mengukur ketidakpastian",
        "Mensimulasikan jalan acak dengan jumlah kumulatif",
    ],
    [
        tb("Mengambil sampel", "Metode `rng.choice` memilih elemen secara acak dari array atau dari rentang bilangan. Argumen `size` menentukan jumlah pilihan, `replace` menentukan apakah elemen boleh terpilih berulang, dan `p` memberi probabilitas tiap elemen. Tanpa pengembalian cocok untuk mengambil sampel dari populasi tetap, sedangkan dengan pengembalian cocok untuk mensimulasikan pengamatan yang saling bebas."),
        C(
            ind("""
import numpy as np

rng = np.random.default_rng(7)
s = rng.choice(5, 3, replace=False)
print(s.shape, len(set(s.tolist())))
semua = np.random.default_rng(7).choice(5, 5, replace=False)
print(sorted(semua.tolist()))
u = np.random.default_rng(4).choice(['a', 'b'], 5, p=[1, 0]).tolist()
print(u)
dg = rng.choice([0, 1], 10000, p=[0.3, 0.7])
print(abs(float(dg.mean()) - 0.7) < 0.03)
"""),
            ind("""
(3,) 3
[0, 1, 2, 3, 4]
['a', 'a', 'a', 'a', 'a']
True
"""),
            "Tanpa pengembalian tidak menghasilkan duplikat. Probabilitas p mengatur seberapa sering tiap nilai terpilih.",
            filename="choice_dasar.py",
        ),
        tb("Simulasi Monte Carlo", "Metode Monte Carlo memakai pengacakan untuk memperkirakan besaran yang sulit dihitung langsung. Prinsipnya: ulangi percobaan acak sangat banyak kali, lalu rata-ratakan hasilnya. Berdasarkan hukum bilangan besar, rata-rata itu mendekati nilai sebenarnya. Dengan array NumPy, kita membangkitkan jutaan percobaan sekaligus tanpa perulangan, sehingga simulasi cepat."),
        tb("Memperkirakan pi", "Contoh klasik: ambil titik acak di persegi satuan. Titik yang jatuh dalam seperempat lingkaran berjari-jari satu adalah yang jumlah kuadrat koordinatnya tidak lebih dari satu. Luas seperempat lingkaran adalah pi per empat, jadi proporsi titik di dalam dikali empat memperkirakan pi. Semakin banyak titik, semakin dekat, dengan galat menyusut sekitar satu per akar n."),
        C(
            ind("""
import numpy as np

n = 200000
titik = np.random.default_rng(9).random((n, 2))
dalam = (titik ** 2).sum(axis=1) <= 1
est = float(4 * dalam.mean())
print(abs(est - 3.14159) < 0.05)
print(titik.shape)
kecil = np.random.default_rng(9).random((100, 2))
est2 = float(4 * ((kecil ** 2).sum(axis=1) <= 1).mean())
print(0 <= est2 <= 4)
"""),
            ind("""
True
(200000, 2)
True
"""),
            "Perkiraan pi dari dua ratus ribu titik cukup dekat. Dengan sedikit titik hasilnya lebih kasar.",
            filename="monte_carlo_pi.py",
        ),
        tb("Galat simulasi", "Hasil Monte Carlo selalu mengandung galat acak, yang menyusut sebanding dengan satu per akar jumlah percobaan. Untuk mengurangi galat sepuluh kali, perlu seratus kali lebih banyak percobaan. Karena itu laporkan jumlah percobaan dan idealnya sebaran hasil dari beberapa seed. Satu angka tanpa konteks galat dapat menyesatkan."),
        tb("Bootstrap", "Bootstrap adalah cara menaksir ketidakpastian suatu statistik tanpa asumsi distribusi. Dari data berukuran n, ambil sampel baru berukuran n dengan pengembalian, hitung statistiknya, dan ulangi ribuan kali. Sebaran statistik hasil ulangan menggambarkan seberapa jauh statistik itu berubah bila datanya sedikit berbeda. Persentil dua koma lima dan sembilan puluh tujuh koma lima membentuk selang kepercayaan dengan sembilan puluh lima persen."),
        C(
            ind("""
import numpy as np

rng = np.random.default_rng(2)
d = np.array([1., 2., 3., 4.])
bm = np.array([rng.choice(d, len(d)).mean() for _ in range(200)])
print(bm.shape)
print(bool((bm >= d.min()).all() and (bm <= d.max()).all()))
print(abs(float(bm.mean()) - float(d.mean())) < 0.3)
lo, hi = np.percentile(bm, [2.5, 97.5])
print(bool(lo <= d.mean() <= hi))
"""),
            ind("""
(200,)
True
True
True
"""),
            "Rata-rata ulangan berada dalam rentang data dan berpusat dekat rata-rata asli, dengan selang persentil mencakupnya.",
            filename="bootstrap.py",
        ),
        tb("Bootstrap dengan vectorization", "Perulangan Python untuk ribuan ulangan dapat dipercepat. Ambil seluruh indeks sekaligus dengan `rng.integers(0, n, (B, n))`, lalu indekskan data dan rata-ratakan sepanjang sumbu satu. Satu ekspresi menghasilkan semua rata-rata ulangan. Teknik ini menukar sedikit memori dengan kecepatan besar, dan cocok selama B kali n masih muat di memori."),
        tb("Jalan acak", "Jalan acak adalah deret posisi yang tiap langkahnya acak, misalnya naik satu atau turun satu dengan peluang sama. Dengan NumPy, bangkitkan seluruh langkah sekaligus lalu ambil jumlah kumulatif untuk mendapat lintasan. Model ini dipakai sebagai pendekatan harga saham, difusi partikel, dan dasar banyak model deret waktu. Perilakunya: simpangan dari awal tumbuh sekitar akar jumlah langkah."),
        C(
            ind("""
import numpy as np

langkah = np.random.default_rng(1).choice([-1, 1], 10)
lintasan = langkah.cumsum()
print(np.abs(np.diff(lintasan)).tolist())
print(int(abs(lintasan[0])))
print(len(lintasan))
besar = np.random.default_rng(3).choice([-1, 1], (500, 400)).cumsum(axis=1)[:, -1]
print(abs(float(besar.std()) - 20) < 3)
"""),
            ind("""
[1, 1, 1, 1, 1, 1, 1, 1, 1]
1
10
True
"""),
            "Tiap langkah mengubah posisi tepat satu. Simpangan setelah empat ratus langkah mendekati dua puluh, yaitu akar empat ratus.",
            filename="jalan_acak.py",
        ),
        tb("Simulasi sebagai alat berpikir", "Bila rumus pasti sulit diturunkan, simulasi sering menjawab lebih cepat: berapa peluang tiga dari sepuluh pelanggan membeli, berapa lama antrean rata-rata, berapa risiko portofolio. Jangan mengganti pemahaman dengan simulasi, tetapi gunakan keduanya untuk saling memeriksa. Simulasi memperlihatkan perilaku, sedangkan teori menjelaskan mengapa."),
        K("tip", "Galat Monte Carlo menyusut sebanding satu per akar n. Laporkan jumlah percobaan dan seed bersama hasilnya.", title="Laporkan galat"),
        tb("Distribusi non-seragam", "Tidak semua pengacakan seragam. Dengan `p` pada `choice`, kita memodelkan kelas yang tidak seimbang, misalnya sembilan puluh persen pelanggan tidak membeli. Distribusi `binomial` menghitung berapa keberhasilan dari sejumlah percobaan, `poisson` memodelkan jumlah kejadian per interval, dan `exponential` memodelkan waktu tunggu. Memilih distribusi yang sesuai membuat simulasi lebih realistis."),
        tb("Validasi simulasi", "Sebelum mempercayai simulasi, uji dengan kasus yang jawabannya diketahui. Simulasi pelemparan koin harus memberi rata-rata mendekati setengah, dan perkiraan pi harus mendekati tiga koma satu empat. Bila hasil menyimpang jauh, kemungkinan ada galat pada kode. Pengujian seperti ini murah dan menangkap kesalahan logika sebelum simulasi sebenarnya dijalankan."),
        tb("Selang kepercayaan dari bootstrap", "Setelah mendapat ribuan statistik bootstrap, ambil persentil dua koma lima dan sembilan puluh tujuh koma lima untuk selang kepercayaan sembilan puluh lima persen. Lebar selang menunjukkan ketidakpastian: data sedikit atau bervariasi menghasilkan selang lebar. Pendekatan ini bekerja untuk statistik apa pun, seperti median atau korelasi, yang rumus galat bakunya rumit."),
        tb("Simulasi berulang dengan seed berbeda", "Untuk menilai kestabilan hasil, jalankan simulasi yang sama dengan beberapa seed dan lihat sebaran hasilnya. Bila hasil bervariasi sedikit, kesimpulan kokoh. Bila bervariasi besar, tambah jumlah percobaan. Menurunkan seed dengan `SeedSequence.spawn` menjamin tiap run memakai aliran independen dan seluruh rangkaian tetap dapat diulang dari satu seed induk."),
        tb("Batas simulasi", "Simulasi memberi jawaban numerik, bukan bukti. Ia bergantung pada model yang Anda tulis, sehingga asumsi yang keliru menghasilkan jawaban keliru yang tampak meyakinkan. Catat asumsi, uji pada kasus sederhana, dan bandingkan dengan perhitungan analitik bila ada. Dengan disiplin ini simulasi menjadi alat yang andal untuk mengeksplorasi masalah rumit."),
        E(
            "B1-06-2-ex1",
            "mudah",
            "Tulis fungsi `sampel_tanpa_ulang(n, k, seed)` yang mengembalikan list `k` bilangan berbeda yang dipilih acak dari 0 sampai `n - 1` memakai `default_rng(seed).choice` tanpa pengembalian.",
            ind("""
import numpy as np

def sampel_tanpa_ulang(n, k, seed):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

s = sampel_tanpa_ulang(10, 4, 1)
assert len(s) == 4 and len(set(s)) == 4
assert all(0 <= v < 10 for v in s)
assert s == sampel_tanpa_ulang(10, 4, 1)
assert sorted(sampel_tanpa_ulang(5, 5, 2)) == [0, 1, 2, 3, 4]
"""),
            "choice menerima replace bernilai False.",
            G1.strip("\n"),
        ),
        E(
            "B1-06-2-ex2",
            "sedang",
            "Tulis fungsi `taksir_pi(seed, n)` yang memperkirakan pi dengan `n` titik acak seragam pada persegi satuan dan mengembalikan empat kali proporsi titik yang berada dalam seperempat lingkaran, sebagai float Python.",
            ind("""
import numpy as np

def taksir_pi(seed, n):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

e = taksir_pi(1, 200000)
assert type(e) is float
assert abs(e - 3.14159) < 0.05
assert e == taksir_pi(1, 200000)
assert 0 <= taksir_pi(2, 50) <= 4
"""),
            "Bangkitkan n kali dua titik dan hitung proporsi yang jumlah kuadratnya tidak lebih dari satu.",
            G2.strip("\n"),
        ),
        E(
            "B1-06-2-ex3",
            "sedang",
            "Tulis fungsi `bootstrap_rata(data, B, seed)` yang mengembalikan array berisi `B` rata-rata dari sampel bootstrap, yaitu sampel berukuran sama dengan `data` yang diambil dengan pengembalian, memakai `default_rng(seed)`.",
            ind("""
import numpy as np

def bootstrap_rata(data, B, seed):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

d = [1, 2, 3, 4]
b = bootstrap_rata(d, 200, 2)
assert b.shape == (200,)
assert bool((b >= 1).all() and (b <= 4).all())
assert np.allclose(b, bootstrap_rata(d, 200, 2))
assert abs(float(b.mean()) - 2.5) < 0.3
"""),
            "Ulangi choice dengan pengembalian sebanyak B kali dan rata-ratakan.",
            G3.strip("\n"),
        ),
        E(
            "B1-06-2-ex4",
            "menantang",
            "Tulis fungsi `jalan_acak(seed, n)` yang mengembalikan list posisi jalan acak sepanjang `n` langkah, tiap langkah minus satu atau satu dengan peluang sama, dihitung sebagai jumlah kumulatif langkah.",
            ind("""
import numpy as np

def jalan_acak(seed, n):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

j = jalan_acak(1, 20)
assert len(j) == 20
assert abs(j[0]) == 1
assert all(abs(j[i + 1] - j[i]) == 1 for i in range(19))
assert j == jalan_acak(1, 20)
assert jalan_acak(1, 0) == []
"""),
            "Pilih langkah dari minus satu dan satu lalu ambil jumlah kumulatif.",
            G4.strip("\n"),
        ),
    ],
    [
        M("Memakai sampel dengan pengembalian untuk populasi tetap.", "Atur replace=False."),
        M("Melaporkan hasil simulasi tanpa jumlah percobaan.", "Sebutkan n dan seed."),
        M("Menjalankan bootstrap dengan perulangan lambat tanpa perlu.", "Vektorkan dengan indeks dua dimensi."),
    ],
    [
        Q("replace=False berarti?", ["Tidak ada pengulangan", "Boleh berulang", "Tanpa acak", "Berurutan"], 0, "Tanpa pengembalian.", hint="Tidak berulang."),
        Q("Galat Monte Carlo menyusut sebanding?", ["Satu per akar n", "Satu per n", "n", "Kuadrat n"], 0, "Akar.", hint="Akar."),
        Q("Bootstrap mengambil sampel?", ["Dengan pengembalian", "Tanpa pengembalian", "Terurut", "Terbesar"], 0, "Ukuran sama.", hint="Dengan."),
        Q("Jalan acak dihitung dengan?", ["Jumlah kumulatif langkah", "Rata-rata", "Maksimum", "Selisih"], 0, "Cumsum.", hint="Kumulatif."),
        Q("Proporsi titik dalam lingkaran dikali empat?", ["Perkiraan pi", "Luas persegi", "Rata-rata", "Nol"], 0, "Seperempat lingkaran.", hint="Pi."),
    ],
    [
        "choice mengambil sampel dengan atau tanpa pengembalian.",
        "Monte Carlo memperkirakan besaran lewat banyak percobaan acak.",
        "Bootstrap menaksir ketidakpastian dengan sampel ulang.",
        "Jalan acak adalah jumlah kumulatif langkah acak.",
    ],
    [],
)

H1 = """
import numpy as np

def jumlah_kuadrat(x):
    return float((np.asarray(x, dtype=float) ** 2).sum())
"""
H2 = """
import numpy as np

def hitung_frekuensi(label, k):
    return np.bincount(label, minlength=k).tolist()
"""
H3 = """
import numpy as np

def rata_bergerak(x, k):
    c = np.cumsum(np.insert(np.asarray(x, dtype=float), 0, 0.0))
    return (c[k:] - c[:-k]) / k
"""
H4 = """
import numpy as np

def rata_per_grup(nilai, grup, k):
    jumlah = np.bincount(grup, weights=nilai, minlength=k)
    banyak = np.bincount(grup, minlength=k)
    return np.divide(jumlah, banyak, out=np.zeros(k), where=banyak > 0).tolist()
"""

l3 = lesson(
    "B1-06-3",
    "Performa dan praktik terbaik NumPy",
    35,
    [
        "Mengukur waktu dan memori dengan benar",
        "Mengganti perulangan dengan operasi array",
        "Memakai bincount dan cumsum untuk pola umum",
        "Menghindari penyalinan dan alokasi yang tidak perlu",
    ],
    [
        tb("Ukur sebelum mengoptimalkan", "Aturan emas performa: ukur sebelum mengubah. Dugaan tentang bagian yang lambat sering salah. Gunakan `time.perf_counter()` di skrip atau `%timeit` di notebook untuk mengukur, dan jalankan beberapa kali karena hasil bervariasi. Optimalkan hanya bagian yang benar-benar lambat, dan pastikan hasil versi cepat sama dengan versi asli sebelum mengganti."),
        C(
            ind("""
import time
import numpy as np

x = np.arange(100000, dtype=float)
t0 = time.perf_counter()
total_loop = 0.0
for v in x:
    total_loop += v * v
t_loop = time.perf_counter() - t0
t0 = time.perf_counter()
total_vec = float((x * x).sum())
t_vec = time.perf_counter() - t0
print(t_loop >= 0, t_vec >= 0)
print(abs(total_loop - total_vec) / total_vec < 1e-9)
"""),
            ind("""
True True
True
"""),
            "Pengukuran memakai perf_counter, dan yang terpenting hasil kedua versi harus sama sebelum membandingkan kecepatan.",
            filename="ukur_waktu.py",
        ),
        tb("Perulangan Python adalah musuh", "Setiap iterasi perulangan Python memiliki biaya tetap yang besar: pemeriksaan tipe, pembuatan objek, dan pemanggilan fungsi. Pada array jutaan elemen, biaya itu berlipat jutaan kali. Operasi array menjalankan perulangan di kode C pada memori berurutan sehingga biaya per elemen jauh lebih kecil. Karena itu aturan praktisnya: bila ada perulangan atas elemen array, cari padanan vectorized."),
        tb("np.vectorize bukan jalan pintas", "Fungsi `np.vectorize` terlihat seperti cara memvektorkan fungsi biasa, tetapi sebenarnya hanya membungkus perulangan Python dalam antarmuka array, jadi tidak lebih cepat. Ia berguna untuk kenyamanan, bukan kecepatan. Kecepatan sungguhan datang dari ufunc bawaan, ekspresi array, atau alat kompilasi seperti numba. Jangan menyangka kode sudah vectorized hanya karena memanggil np.vectorize."),
        tb("Pola penghitungan dengan bincount", "Menghitung frekuensi tiap kelas dengan perulangan lambat. Fungsi `np.bincount` melakukannya sekaligus: ia menghitung berapa kali tiap bilangan bulat tidak negatif muncul. Dengan argumen `weights`, ia menjumlahkan bobot per kelas, sehingga cocok untuk menjumlahkan nilai per kelompok. Argumen `minlength` menjamin panjang hasil tetap meski ada kelas yang tidak muncul."),
        C(
            ind("""
import numpy as np

print(np.bincount([0, 2, 2, 1, 2], minlength=4).tolist())
n = np.array([1., 2., 3., 4.])
g = np.array([0, 1, 0, 1])
jumlah = np.bincount(g, weights=n, minlength=3)
banyak = np.bincount(g, minlength=3)
print(jumlah.tolist(), banyak.tolist())
print(np.divide(jumlah, banyak, out=np.zeros(3), where=banyak > 0).tolist())
"""),
            ind("""
[1, 1, 3, 0]
[4.0, 6.0, 0.0] [2, 2, 0]
[2.0, 3.0, 0.0]
"""),
            "Bincount menghitung frekuensi, dan dengan bobot menjumlahkan nilai per kelompok. Kelompok kosong dijaga bernilai nol.",
            filename="bincount_grup.py",
        ),
        tb("Jumlah kumulatif untuk jendela", "Rata-rata bergerak dapat dihitung tanpa perulangan bersarang dengan jumlah kumulatif. Hitung jumlah kumulatif dengan nol di depan, lalu selisih dua posisi yang berjarak k memberi jumlah jendela berukuran k. Cara ini membutuhkan waktu sebanding panjang data, tidak peduli ukuran jendela, berbeda dari cara naif yang sebanding data kali jendela."),
        C(
            ind("""
import numpy as np

x = np.array([1., 2., 3., 4., 5.])
c = np.cumsum(np.insert(x, 0, 0.0))
print(((c[3:] - c[:-3]) / 3).tolist())
print(np.convolve(x, np.ones(3), 'valid').tolist())
"""),
            ind("""
[2.0, 3.0, 4.0]
[6.0, 9.0, 12.0]
"""),
            "Selisih jumlah kumulatif memberi jumlah tiap jendela, dibagi tiga menjadi rata-rata.",
            filename="jendela_kumulatif.py",
        ),
        tb("Prealokasi dan penyalinan", "Menambah elemen ke array dengan `np.append` atau `concatenate` di dalam perulangan menyalin seluruh array setiap kali sehingga waktunya kuadratik. Alokasikan array berukuran akhir lebih dulu dengan `np.empty` atau `np.zeros`, lalu isi. Lebih baik lagi, hitung seluruh hasil sekaligus tanpa perulangan. Pada data besar, hindari salinan yang tidak perlu dengan memakai view dan operasi di tempat."),
        tb("Operasi di tempat", "Operator seperti `+=` dan argumen `out` pada ufunc memodifikasi array tanpa membuat array baru, menghemat memori dan waktu alokasi. Gunakan hati-hati bila array digunakan di tempat lain, karena perubahan terlihat di semua rujukan. Perhatikan juga tipe: menambah desimal ke array bilangan bulat di tempat memicu galat atau pemotongan, jadi samakan tipe lebih dulu."),
        tb("Tipe dan memori", "Pilihan dtype memengaruhi kecepatan dan memori. Float32 memakai separuh memori float64 dan sering lebih cepat, tetapi kurang teliti. Bilangan bulat kecil seperti int8 menghemat ruang untuk label. Ukuran array dapat dicek dengan `nbytes`. Untuk data yang tidak muat di memori, pertimbangkan pemetaan file dengan `np.memmap` atau memproses per potongan."),
        tb("Kapan beralih alat", "NumPy sangat cepat untuk operasi yang dapat dinyatakan sebagai operasi array. Bila logika bergantung pada keputusan per elemen yang rumit, pertimbangkan numba untuk mengompilasi fungsi Python, atau Cython. Bila data sangat besar, pertimbangkan alat yang memproses di luar memori seperti dask. Namun kuasai dahulu NumPy, karena semua alat itu meminjam model array yang sama."),
        tb("Ringkasan course", "Anda telah menyelesaikan penguasaan NumPy: ndarray, dtype, indexing, broadcasting, ufunc, aljabar linear, keacakan, dan performa. Kebiasaan inti yang dibawa: periksa shape dan dtype, vektorkan perhitungan, kendalikan keacakan dengan seed, bandingkan desimal dengan toleransi, dan ukur sebelum mengoptimalkan. Dengan fondasi ini, pandas dan pustaka sains data lain akan terasa jauh lebih mudah."),
        K("tip", "Ukur dulu, pastikan hasil sama, baru ganti. Optimasi tanpa pengukuran sering sia-sia.", title="Urutan optimasi"),
        tb("Profil kode", "Bila tidak tahu bagian mana yang lambat, gunakan profiler seperti `cProfile` yang melaporkan waktu per fungsi. Di notebook, `%prun` dan `%lprun` membantu. Fokus pada bagian yang memakan sebagian besar waktu, karena mempercepat bagian yang hanya lima persen dari total tidak akan terasa. Prinsip ini dikenal sebagai hukum Amdahl dan menjaga usaha optimasi tetap efektif."),
        E(
            "B1-06-3-ex1",
            "mudah",
            "Tulis fungsi `jumlah_kuadrat(x)` yang mengembalikan jumlah kuadrat semua elemen `x` sebagai float Python tanpa perulangan Python.",
            ind("""
import numpy as np

def jumlah_kuadrat(x):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

assert jumlah_kuadrat([1, 2, 3]) == 14.0
assert jumlah_kuadrat(np.arange(1000)) == 332833500.0
assert jumlah_kuadrat([]) == 0.0
assert type(jumlah_kuadrat([2])) is float
"""),
            "Kuadratkan array lalu jumlahkan.",
            H1.strip("\n"),
        ),
        E(
            "B1-06-3-ex2",
            "sedang",
            "Tulis fungsi `hitung_frekuensi(label, k)` yang mengembalikan list frekuensi tiap kelas 0 sampai `k - 1` dari list label, dengan panjang hasil selalu `k`.",
            ind("""
import numpy as np

def hitung_frekuensi(label, k):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

assert hitung_frekuensi([0, 2, 2, 1, 2], 4) == [1, 1, 3, 0]
assert hitung_frekuensi([], 3) == [0, 0, 0]
assert hitung_frekuensi([1, 1], 2) == [0, 2]
assert sum(hitung_frekuensi([0, 1, 2, 2], 3)) == 4
"""),
            "np.bincount dengan minlength.",
            H2.strip("\n"),
        ),
        E(
            "B1-06-3-ex3",
            "sedang",
            "Tulis fungsi `rata_bergerak(x, k)` yang mengembalikan array rata-rata tiap jendela berukuran `k` pada `x` hanya untuk jendela yang penuh, memakai jumlah kumulatif tanpa perulangan Python.",
            ind("""
import numpy as np

def rata_bergerak(x, k):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

assert np.allclose(rata_bergerak([1, 2, 3, 4, 5], 3), [2, 3, 4])
assert np.allclose(rata_bergerak([2, 4, 6, 8], 2), [3, 5, 7])
assert np.allclose(rata_bergerak([5, 5, 5], 1), [5, 5, 5])
assert len(rata_bergerak(list(range(10)), 4)) == 7
"""),
            "Jumlah kumulatif dengan nol di depan lalu selisih berjarak k.",
            H3.strip("\n"),
        ),
        E(
            "B1-06-3-ex4",
            "menantang",
            "Tulis fungsi `rata_per_grup(nilai, grup, k)` yang mengembalikan list rata-rata `nilai` untuk tiap grup 0 sampai `k - 1`, dengan `0.0` untuk grup tanpa anggota, memakai `bincount` tanpa perulangan Python.",
            ind("""
import numpy as np

def rata_per_grup(nilai, grup, k):
    # TODO: implementasikan
    pass
"""),
            ind("""
import numpy as np

assert rata_per_grup([1, 2, 3, 4], [0, 1, 0, 1], 2) == [2.0, 3.0]
assert rata_per_grup([1, 2, 3, 4], [0, 1, 0, 1], 3) == [2.0, 3.0, 0.0]
assert rata_per_grup([5], [2], 3) == [0.0, 0.0, 5.0]
assert rata_per_grup([], [], 2) == [0.0, 0.0]
"""),
            "bincount dengan weights untuk jumlah dan tanpa weights untuk banyak, lalu bagi dengan where.",
            H4.strip("\n"),
        ),
    ],
    [
        M("Mengoptimalkan tanpa mengukur.", "Ukur dengan perf_counter atau timeit."),
        M("Mengira np.vectorize mempercepat.", "Ia hanya pembungkus perulangan."),
        M("Menambah elemen ke array dalam perulangan.", "Prealokasi atau hitung sekaligus."),
    ],
    [
        Q("Langkah pertama optimasi?", ["Mengukur", "Menulis ulang", "Mengganti tipe", "Menambah memori"], 0, "Ukur dulu.", hint="Ukur."),
        Q("np.vectorize?", ["Pembungkus perulangan Python", "Mempercepat seperti ufunc", "Mengompilasi kode", "Membuat GPU"], 0, "Kenyamanan.", hint="Pembungkus."),
        Q("bincount menghitung?", ["Frekuensi bilangan bulat", "Rata-rata", "Median", "Selisih"], 0, "Per nilai.", hint="Frekuensi."),
        Q("Rata-rata bergerak efisien dengan?", ["Jumlah kumulatif", "Perulangan bersarang", "Sort", "Reshape"], 0, "Selisih kumulatif.", hint="Kumulatif."),
        Q("np.append dalam perulangan?", ["Lambat karena menyalin", "Cepat", "Di tempat", "Wajib"], 0, "Kuadratik.", hint="Salin."),
    ],
    [
        "Ukur sebelum mengoptimalkan dan pastikan hasil sama.",
        "Ganti perulangan dengan operasi array, bincount, dan cumsum.",
        "Prealokasi dan operasi di tempat menghemat memori dan waktu.",
        "Alat lain seperti numba dan dask meminjam model array NumPy.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perintah yang cukup jelas dalam teks.", "brief": []}

write_module(
    "B1",
    6,
    "Random, reproducibility, dan performa",
    105,
    [
        "Mengendalikan keacakan dengan Generator dan seed",
        "Menjalankan sampling, simulasi, dan bootstrap",
        "Mengoptimalkan kode NumPy dengan pola vectorized",
    ],
    [l1, l2, l3],
    video,
    REF,
)
