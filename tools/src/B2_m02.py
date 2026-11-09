import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

DFX = """
import pandas as pd

df = pd.DataFrame({
    'nama': ['Ani', 'Budi', 'Cici', 'Dedi'],
    'umur': [20, 25, 22, 30],
    'kota': ['A', 'B', 'A', 'C'],
    'skor': [80.0, 70.0, 90.0, 60.0],
}, index=['p1', 'p2', 'p3', 'p4'])
"""


def tb(h, b):
    return T("## " + h + "\n\n" + b)


def ind(s):
    return textwrap.indent(s.strip("\n"), "            ")


def P(body):
    return ind(DFX + "\n" + textwrap.dedent(body).strip("\n"))


def S(body):
    return ind("import pandas as pd\n\n" + textwrap.dedent(body).strip("\n"))


F1 = """
import pandas as pd

def nama_baris(df, label):
    return df.loc[label, 'nama']
"""
F2 = """
import pandas as pd

def blok_label(df, a, b, kolom):
    return df.loc[a:b, kolom].values.tolist()
"""
F3 = """
import pandas as pd

def blok_posisi(df, r0, r1, c0, c1):
    return df.iloc[r0:r1, c0:c1].values.tolist()
"""
F4 = """
import pandas as pd

def selang_kolom(df, kolom):
    return df[kolom].iloc[::2].tolist()
"""

l1 = lesson(
    "B2-02-1",
    "loc dan iloc untuk baris dan kolom",
    35,
    [
        "Membedakan pemilihan berbasis label (loc) dan posisi (iloc)",
        "Memilih sel, baris, kolom, dan blok",
        "Memahami perbedaan slice inklusif dan eksklusif",
        "Memakai at dan iat untuk akses satu sel",
    ],
    [
        tb("Dua pintu masuk", "Pandas memberi dua pintu utama untuk memilih bagian tabel. `loc` memilih menurut **label** indeks dan nama kolom, sedangkan `iloc` memilih menurut **posisi** bilangan bulat. Keduanya memakai bentuk yang sama: `tabel.loc[baris, kolom]` dan `tabel.iloc[baris, kolom]`, dengan koma memisahkan sumbu baris dan kolom. Menguasai kedua pintu ini menghilangkan sebagian besar kebingungan pemilihan data."),
        tb("Data contoh", "Pada pelajaran ini kita memakai tabel kecil berisi empat orang dengan indeks berlabel `p1` sampai `p4` dan kolom `nama`, `umur`, `kota`, dan `skor`. Indeks berupa teks sengaja dipakai agar perbedaan label dan posisi terlihat jelas. Bila indeks hanya nomor urut bawaan, label dan posisi kebetulan sama dan perbedaan keduanya tersembunyi sampai data difilter."),
        C(
            P("""
print(df.loc['p2', 'nama'])
print(df.iloc[1, 0])
print(df.loc['p2'].to_dict())
print(df.loc[:, 'umur'].tolist())
print(df.iloc[:, -1].tolist())
"""),
            ind("""
Budi
Budi
{'nama': 'Budi', 'umur': 25, 'kota': 'B', 'skor': 70.0}
[20, 25, 22, 30]
[80.0, 70.0, 90.0, 60.0]
"""),
            "Loc memakai label p2 dan nama, iloc memakai posisi satu dan nol, keduanya memilih sel yang sama. Titik dua berarti seluruh sumbu.",
            filename="loc_iloc_dasar.py",
        ),
        tb("Satu baris atau satu kolom", "Memberi satu label pada `loc` tanpa kolom mengembalikan satu baris sebagai Series yang indeksnya nama kolom. Titik dua pada posisi baris dengan satu nama kolom mengembalikan satu kolom. Hasil satu baris bertipe campuran dipaksa ke tipe umum, sehingga angka dapat berubah menjadi desimal atau objek. Itu sebabnya mengambil satu kolom sebagai Series biasanya lebih bersih daripada satu baris."),
        tb("Slice: inklusif dan eksklusif", "Perbedaan terpenting antara dua pintu: slice `loc` menyertakan ujung akhir, sedangkan slice `iloc` tidak. Menulis `df.loc['p1':'p3']` mengembalikan tiga baris, dan `df.iloc[0:3]` juga tiga baris, tetapi karena alasan berbeda. Alasan `loc` menyertakan ujung akhir adalah label tidak punya konsep label berikutnya yang pasti, sehingga ujung akhir yang disebutkan dianggap bagian dari rentang."),
        C(
            P("""
print(df.loc['p1':'p3'].index.tolist())
print(df.iloc[0:3].index.tolist())
print(df.loc['p2':'p3', ['nama', 'skor']].values.tolist())
print(df.iloc[1:3, [0, 3]].values.tolist())
print(df.loc[:, 'nama':'kota'].columns.tolist())
print(df.iloc[-2:].index.tolist())
"""),
            ind("""
['p1', 'p2', 'p3']
['p1', 'p2', 'p3']
[['Budi', 70.0], ['Cici', 90.0]]
[['Budi', 70.0], ['Cici', 90.0]]
['nama', 'umur', 'kota']
['p3', 'p4']
"""),
            "Slice label menyertakan p3 dan slice kolom label menyertakan kota. Slice posisi berhenti sebelum angka akhir.",
            filename="slice_label_posisi.py",
        ),
        tb("List label dan list posisi", "Di dalam `loc` atau `iloc` boleh diberikan list untuk memilih baris atau kolom tertentu dalam urutan yang Anda tulis. List label yang tidak ada pada indeks menimbulkan `KeyError`, dan posisi di luar jangkauan menimbulkan `IndexError`. Urutan list menentukan urutan hasil, sehingga cara ini juga dipakai untuk menyusun ulang kolom."),
        tb("at dan iat", "Untuk mengakses atau mengubah satu sel, `at` dan `iat` lebih cepat daripada `loc` dan `iloc`. `at` memakai label baris dan kolom, `iat` memakai posisi baris dan kolom. Keduanya hanya menerima satu sel, bukan slice atau list. Dalam perulangan yang menyentuh banyak sel satu per satu, perbedaan kecepatan terasa, meskipun idealnya perulangan seperti itu diganti operasi vectorized."),
        C(
            P("""
print(df.at['p3', 'skor'])
print(df.iat[2, 3])
print(df.loc[['p4', 'p1'], 'nama'].tolist())
print(df.iloc[[0, -1], 1].tolist())
print(df.columns.get_loc('skor'), df.index.get_loc('p3'))
try:
    df.loc['p9']
except KeyError:
    print('keyerror')
"""),
            ind("""
90.0
90.0
['Dedi', 'Ani']
[20, 30]
3 2
keyerror
"""),
            "At dan iat membaca satu sel. List memilih sesuai urutan, dan label tak dikenal menimbulkan KeyError. Get_loc menerjemahkan label menjadi posisi.",
            filename="at_iat.py",
        ),
        tb("Kapan memakai yang mana", "Gunakan `loc` bila Anda memikirkan data dengan nama: baris untuk pelanggan tertentu, kolom untuk fitur tertentu. Gunakan `iloc` bila Anda memikirkan posisi: lima baris pertama, kolom terakhir, setiap baris kedua. Kode berbasis label lebih tahan terhadap perubahan urutan data, sedangkan kode berbasis posisi rapuh bila kolom bertambah atau urutan berubah, jadi utamakan label bila memungkinkan."),
        tb("Pemilihan dengan langkah", "Slice dengan langkah juga bekerja pada kedua pintu. `df.iloc[::2]` mengambil setiap baris kedua mulai dari baris pertama, dan `df.iloc[::-1]` membalik urutan baris. `df.loc[::2]` pada indeks label bekerja dengan cara yang sama berdasarkan urutan penyimpanan. Gunakan ini untuk sampel berurutan sederhana, bukan untuk sampel acak yang butuh pengacakan."),
        tb("head dan tail", "Metode `head(n)` dan `tail(n)` mengambil n baris pertama dan terakhir, setara dengan `iloc[:n]` dan `iloc[-n:]`. Nilai bawaannya lima. Keduanya sering dipakai untuk melihat sekilas isi data. Untuk menjajaki file besar, ingat bahwa `head` tidak menjamin urutan acak, sehingga baris awal belum tentu mewakili keseluruhan data."),
        tb("Menugaskan nilai", "`loc`, `iloc`, `at`, dan `iat` juga dapat berada di sisi kiri tanda sama dengan untuk mengubah isi. Penugasan `df.loc['p1', 'umur'] = 21` mengubah satu sel, dan `df.iloc[0, 3] = 85.0` melakukan hal sama lewat posisi. Penugasan dengan satu pemilih yang tegas inilah cara yang benar mengubah data, berbeda dari penugasan berantai yang dibahas pada pelajaran berikutnya."),
        K("tip", "Slice loc menyertakan ujung akhir, slice iloc tidak. Utamakan loc dengan label agar kode tahan terhadap perubahan urutan.", title="Ingat perbedaannya"),
        E(
            "B2-02-1-ex1",
            "mudah",
            "Tulis fungsi `nama_baris(df, label)` yang mengembalikan isi kolom `nama` pada baris berlabel `label`.",
            ind("""
import pandas as pd

def nama_baris(df, label):
    # TODO: implementasikan
    pass
"""),
            P("""
assert nama_baris(df, 'p2') == 'Budi'
assert nama_baris(df, 'p4') == 'Dedi'
assert nama_baris(df, 'p1') == 'Ani'
assert nama_baris(df.iloc[::-1], 'p3') == 'Cici'
"""),
            "Pakai loc dengan label baris dan nama kolom.",
            F1.strip("\n"),
        ),
        E(
            "B2-02-1-ex2",
            "sedang",
            "Tulis fungsi `blok_label(df, a, b, kolom)` yang mengembalikan, sebagai list Python, nilai `kolom` (nama kolom atau list nama kolom) untuk baris berlabel `a` sampai `b` inklusif.",
            ind("""
import pandas as pd

def blok_label(df, a, b, kolom):
    # TODO: implementasikan
    pass
"""),
            P("""
assert blok_label(df, 'p2', 'p3', ['nama', 'skor']) == [['Budi', 70.0], ['Cici', 90.0]]
assert blok_label(df, 'p1', 'p2', 'umur') == [20, 25]
assert blok_label(df, 'p4', 'p4', 'nama') == ['Dedi']
assert blok_label(df, 'p1', 'p4', 'kota') == ['A', 'B', 'A', 'C']
"""),
            "Slice label pada loc menyertakan ujung akhir.",
            F2.strip("\n"),
        ),
        E(
            "B2-02-1-ex3",
            "sedang",
            "Tulis fungsi `blok_posisi(df, r0, r1, c0, c1)` yang mengembalikan, sebagai list Python, blok tabel dari baris posisi `r0` sampai sebelum `r1` dan kolom posisi `c0` sampai sebelum `c1`.",
            ind("""
import pandas as pd

def blok_posisi(df, r0, r1, c0, c1):
    # TODO: implementasikan
    pass
"""),
            P("""
assert blok_posisi(df, 1, 3, 0, 1) == [['Budi'], ['Cici']]
assert blok_posisi(df, 0, 2, 1, 2) == [[20], [25]]
assert blok_posisi(df, 3, 4, 3, 4) == [[60.0]]
assert blok_posisi(df, 0, 0, 0, 4) == []
"""),
            "Slice iloc pada kedua sumbu.",
            F3.strip("\n"),
        ),
        E(
            "B2-02-1-ex4",
            "menantang",
            "Tulis fungsi `selang_kolom(df, kolom)` yang mengembalikan, sebagai list Python, nilai kolom `kolom` pada setiap baris kedua mulai dari baris pertama, berdasarkan posisi.",
            ind("""
import pandas as pd

def selang_kolom(df, kolom):
    # TODO: implementasikan
    pass
"""),
            P("""
assert selang_kolom(df, 'umur') == [20, 22]
assert selang_kolom(df, 'nama') == ['Ani', 'Cici']
assert selang_kolom(df.iloc[::-1], 'nama') == ['Dedi', 'Budi']
assert selang_kolom(df.iloc[:3], 'skor') == [80.0, 90.0]
"""),
            "Ambil kolom lalu iloc dengan langkah dua.",
            F4.strip("\n"),
        ),
    ],
    [
        M("Mengira slice loc tidak menyertakan ujung akhir.", "Slice loc menyertakan ujung akhir."),
        M("Memakai posisi pada tabel yang urutannya sering berubah.", "Pakai label dengan loc."),
        M("Mengira satu baris tetap bertipe asli tiap kolom.", "Satu baris dipaksa ke tipe umum."),
    ],
    [
        Q("loc memilih berdasarkan?", ["Label", "Posisi", "Tipe", "Nilai"], 0, "Label indeks dan kolom.", hint="Label."),
        Q("df.iloc[0:3] mengembalikan?", ["Tiga baris", "Empat baris", "Dua baris", "Satu baris"], 0, "Akhir tidak termasuk.", hint="Tiga."),
        Q("df.loc['p1':'p3'] mengembalikan?", ["Tiga baris", "Dua baris", "Satu baris", "Empat baris"], 0, "Menyertakan p3.", hint="Inklusif."),
        Q("Akses satu sel tercepat?", ["at atau iat", "loc list", "iloc slice", "head"], 0, "Satu sel.", hint="at."),
        Q("Label tak dikenal pada loc menimbulkan?", ["KeyError", "IndexError", "Nol", "NaN"], 0, "Label tidak ada.", hint="Key."),
    ],
    [
        "loc memilih dengan label dan iloc dengan posisi.",
        "Slice loc menyertakan ujung akhir, slice iloc tidak.",
        "at dan iat mengakses satu sel dengan cepat.",
        "Pilih label bila memungkinkan agar kode tahan perubahan urutan.",
    ],
    [],
)

G1 = """
import pandas as pd

def nama_lulus(df, batas):
    return df.loc[df['skor'] >= batas, 'nama'].tolist()
"""
G2 = """
import pandas as pd

def nama_kombinasi(df, umur_min, kota):
    mask = (df['umur'] >= umur_min) & df['kota'].isin(kota)
    return df.loc[mask, 'nama'].tolist()
"""
G3 = """
import pandas as pd

def batasi_skor(df, minimum):
    hasil = df.copy()
    hasil.loc[hasil['skor'] < minimum, 'skor'] = minimum
    return hasil
"""
G4 = """
import pandas as pd

def beri_kategori(df, batas):
    hasil = df.copy()
    hasil['kat'] = 'rendah'
    hasil.loc[hasil['skor'] >= batas, 'kat'] = 'tinggi'
    return hasil
"""

l2 = lesson(
    "B2-02-2",
    "Filter boolean dan penugasan bersyarat",
    35,
    [
        "Menyaring baris dengan mask boolean",
        "Menggabungkan syarat dengan operator logika",
        "Memakai isin, between, dan str untuk syarat umum",
        "Mengubah nilai bersyarat dengan loc tanpa peringatan",
    ],
    [
        tb("Menyaring berdasarkan isi", "Pemilihan paling sering dalam analisis data adalah menyaring baris berdasarkan isinya: pelanggan yang umurnya di atas dua puluh lima, transaksi yang gagal, produk dengan stok kurang dari sepuluh. Caranya sama seperti pada NumPy: buat mask boolean dari perbandingan, lalu gunakan mask itu untuk memilih baris. Pada pandas, mask adalah Series boolean yang indeksnya sejajar dengan tabel."),
        C(
            P("""
m = df['skor'] > 65
print(m.tolist())
print(df.loc[m, 'nama'].tolist())
print(df[m].shape)
print(int(m.sum()), float(m.mean()))
print(df.loc[~m, 'nama'].tolist())
"""),
            ind("""
[True, True, True, False]
['Ani', 'Budi', 'Cici']
(3, 4)
3 0.75
['Dedi']
"""),
            "Mask berasal dari perbandingan satu kolom. Jumlah mask menghitung baris lolos, dan tilde membalik pilihan.",
            filename="filter_dasar.py",
        ),
        tb("Menggabungkan syarat", "Gabungkan beberapa syarat dengan `&` untuk dan, `|` untuk atau, dan `~` untuk bukan. Seperti pada NumPy, tiap perbandingan harus diapit kurung karena `&` lebih diutamakan daripada operator perbandingan. Kata `and` dan `or` tidak dapat dipakai pada Series dan menimbulkan galat nilai ambigu. Menyimpan tiap syarat dalam variabel bernama membuat ekspresi panjang mudah dibaca."),
        tb("Syarat umum", "Metode `isin` memeriksa keanggotaan dalam list, `between` memeriksa rentang inklusif, dan `str.contains`, `str.startswith`, serta `str.endswith` memeriksa pola teks. Metode `isna` dan `notna` memeriksa nilai hilang. Semuanya mengembalikan Series boolean yang dapat digabung dengan operator logika, sehingga hampir semua pertanyaan seleksi dapat dinyatakan dengan beberapa baris."),
        C(
            P("""
print(df.loc[(df['umur'] >= 22) & (df['kota'] == 'A'), 'nama'].tolist())
print(df.loc[(df['umur'] < 22) | (df['skor'] < 65), 'nama'].tolist())
print(df.loc[df['kota'].isin(['A', 'C']), 'nama'].tolist())
print(df.loc[df['umur'].between(22, 25), 'nama'].tolist())
print(df.loc[df['nama'].str.startswith('C'), 'nama'].tolist())
print(df.loc[lambda d: d['skor'] > 75, 'nama'].tolist())
"""),
            ind("""
['Cici']
['Ani', 'Dedi']
['Ani', 'Cici', 'Dedi']
['Budi', 'Cici']
['Cici']
['Ani', 'Cici']
"""),
            "Dua syarat digabung dengan kurung. Isin, between, dan metode teks membuat mask khusus, dan fungsi lambda membaca tabel saat itu.",
            filename="filter_gabung.py",
        ),
        tb("Hasil kosong", "Bila tidak ada baris yang memenuhi syarat, hasilnya tabel kosong dengan kolom yang sama, bukan galat. Periksa dengan atribut `empty` atau `len`. Hasil ringkasan seperti `max` pada Series kosong menghasilkan NaN atau galat, jadi periksa lebih dulu bila bagian kode berikutnya bergantung pada adanya data."),
        tb("Mengubah nilai bersyarat", "Cara yang benar mengubah nilai pada baris tertentu adalah `df.loc[mask, 'kolom'] = nilai`, satu pemilih tunggal yang memuat baris dan kolom sekaligus. Cara ini memodifikasi tabel asal secara langsung dan tegas. Bentuk berantai seperti `df[mask]['kolom'] = nilai` tidak bekerja dengan andal: ia mengubah salinan sementara dan tabel asal tetap tidak berubah, disertai peringatan."),
        C(
            P("""
d2 = df.copy()
d2.loc[d2['skor'] < 65, 'skor'] = 65.0
print(d2['skor'].tolist())
print(df['skor'].tolist())
d2.loc[d2['kota'] == 'A', 'kota'] = 'Z'
print(d2['kota'].tolist())
d2['kat'] = 'rendah'
d2.loc[d2['skor'] >= 80, 'kat'] = 'tinggi'
print(d2['kat'].tolist())
"""),
            ind("""
[80.0, 70.0, 90.0, 65.0]
[80.0, 70.0, 90.0, 60.0]
['Z', 'B', 'Z', 'C']
['tinggi', 'rendah', 'tinggi', 'rendah']
"""),
            "Loc dengan mask mengubah baris terpilih pada salinan, sementara tabel asal tetap utuh. Kolom kategori dibuat dengan nilai bawaan lalu ditimpa bersyarat.",
            filename="penugasan_bersyarat.py",
        ),
        tb("Penugasan berantai", "Peringatan SettingWithCopy atau ChainedAssignment muncul ketika Anda mengubah hasil dari pemilihan sebelumnya. Penyebabnya adalah pandas tidak menjamin apakah pemilihan pertama mengembalikan tampilan atau salinan. Pada pandas versi baru dengan aturan copy-on-write, penugasan berantai tidak pernah memengaruhi tabel asal. Aturan praktisnya: satu langkah, satu `loc`."),
        tb("Salinan eksplisit", "Bila Anda memang ingin bekerja pada bagian tabel secara terpisah, buat salinan eksplisit dengan `.copy()`: `kecil = df[df['umur'] > 21].copy()`. Setelah itu mengubah `kecil` tidak memengaruhi `df` dan tidak menimbulkan peringatan. Kebiasaan ini menjelaskan niat kode dan menghindari bug halus ketika tabel asal berubah di tempat lain."),
        tb("where dan mask", "Metode `where(cond, other)` mempertahankan nilai bila syarat benar dan menggantinya dengan `other` bila salah, sedangkan `mask` melakukan kebalikannya. Keduanya mengembalikan objek baru dan berguna untuk mengganti nilai tanpa menugaskan. Untuk memilih antara dua nilai berdasarkan syarat, `np.where` pada kolom sering lebih ringkas, dan `np.select` menangani banyak kategori."),
        tb("Kolom kategori dari syarat", "Pola umum: buat kolom baru berisi label berdasarkan syarat pada kolom lain. Untuk dua kategori, pakai `np.where(syarat, 'a', 'b')`. Untuk banyak kategori berurutan, pakai `np.select` atau `pd.cut` bila batasnya berupa rentang numerik. Menyimpan hasil sebagai tipe `category` menghemat memori dan membuat pengelompokan berikutnya lebih cepat."),
        K("warn", "Gunakan satu loc untuk mengubah bagian tabel. Penugasan berantai seperti df[mask]['kolom'] = nilai tidak mengubah tabel asal.", title="Satu langkah"),
        tb("Bahaya nilai hilang pada mask", "Mask dari kolom yang memuat NaN menghasilkan False pada baris tersebut untuk perbandingan seperti lebih besar, sehingga baris bernilai hilang diam-diam keluar dari hasil. Bila itu bukan yang Anda inginkan, tangani nilai hilang secara eksplisit dengan `isna` atau `fillna` sebelum menyaring. Selalu bandingkan jumlah baris sebelum dan sesudah filter agar tidak ada kehilangan yang tak disadari."),
        tb("Menghitung hasil filter", "Setelah menyaring, pertanyaan lanjutan hampir selalu tentang jumlah dan proporsi: berapa baris yang lolos, berapa persen dari total. `len(hasil)` atau `mask.sum()` memberi jumlah dan `mask.mean()` memberi proporsi. Biasakan melaporkan keduanya bersama angka ringkasan, karena rata-rata dari hanya dua baris punya arti sangat berbeda dari rata-rata ribuan baris."),
        tb("Filter bertingkat", "Untuk logika rumit, pecah syarat menjadi beberapa mask bernama lalu gabungkan. Misalnya `dewasa = df['umur'] >= 18`, `aktif = df['status'] == 'aktif'`, lalu `df.loc[dewasa & aktif]`. Nama variabel menjelaskan makna bisnis tiap syarat, mudah diuji terpisah, dan dipakai ulang. Cara ini jauh lebih mudah dirawat daripada satu ekspresi panjang berkurung bertumpuk."),
        E(
            "B2-02-2-ex1",
            "mudah",
            "Tulis fungsi `nama_lulus(df, batas)` yang mengembalikan list `nama` untuk baris dengan `skor` sekurang-kurangnya `batas`, memakai `loc`.",
            ind("""
import pandas as pd

def nama_lulus(df, batas):
    # TODO: implementasikan
    pass
"""),
            P("""
assert nama_lulus(df, 75) == ['Ani', 'Cici']
assert nama_lulus(df, 60) == ['Ani', 'Budi', 'Cici', 'Dedi']
assert nama_lulus(df, 100) == []
assert nama_lulus(df, 90) == ['Cici']
"""),
            "Mask skor dibandingkan dengan batas lalu loc dengan kolom nama.",
            G1.strip("\n"),
        ),
        E(
            "B2-02-2-ex2",
            "sedang",
            "Tulis fungsi `nama_kombinasi(df, umur_min, kota)` yang mengembalikan list `nama` untuk baris dengan `umur` sekurang-kurangnya `umur_min` dan `kota` yang termasuk dalam list `kota`.",
            ind("""
import pandas as pd

def nama_kombinasi(df, umur_min, kota):
    # TODO: implementasikan
    pass
"""),
            P("""
assert nama_kombinasi(df, 22, ['A']) == ['Cici']
assert nama_kombinasi(df, 20, ['A', 'C']) == ['Ani', 'Cici', 'Dedi']
assert nama_kombinasi(df, 40, ['A', 'B', 'C']) == []
assert nama_kombinasi(df, 0, ['B']) == ['Budi']
"""),
            "Gabungkan dua mask dengan ampersand dan kurung.",
            G2.strip("\n"),
        ),
        E(
            "B2-02-2-ex3",
            "sedang",
            "Tulis fungsi `batasi_skor(df, minimum)` yang mengembalikan salinan `df` dengan semua `skor` di bawah `minimum` diganti `minimum`. Tabel asli tidak boleh berubah.",
            ind("""
import pandas as pd

def batasi_skor(df, minimum):
    # TODO: implementasikan
    pass
"""),
            P("""
r = batasi_skor(df, 65.0)
assert r['skor'].tolist() == [80.0, 70.0, 90.0, 65.0]
assert df['skor'].tolist() == [80.0, 70.0, 90.0, 60.0]
assert batasi_skor(df, 0.0)['skor'].tolist() == df['skor'].tolist()
assert batasi_skor(df, 100.0)['skor'].tolist() == [100.0] * 4
"""),
            "Salin lalu loc dengan mask pada kolom skor.",
            G3.strip("\n"),
        ),
        E(
            "B2-02-2-ex4",
            "menantang",
            "Tulis fungsi `beri_kategori(df, batas)` yang mengembalikan salinan `df` dengan kolom baru `kat` bernilai `'tinggi'` bila `skor` sekurang-kurangnya `batas` dan `'rendah'` bila tidak. Tabel asli tidak boleh berubah.",
            ind("""
import pandas as pd

def beri_kategori(df, batas):
    # TODO: implementasikan
    pass
"""),
            P("""
r = beri_kategori(df, 80)
assert r['kat'].tolist() == ['tinggi', 'rendah', 'tinggi', 'rendah']
assert 'kat' not in df.columns
assert beri_kategori(df, 0)['kat'].tolist() == ['tinggi'] * 4
assert beri_kategori(df, 100)['kat'].tolist() == ['rendah'] * 4
"""),
            "Beri nilai bawaan rendah lalu timpa bersyarat dengan loc.",
            G4.strip("\n"),
        ),
    ],
    [
        M("Memakai and atau or antar syarat.", "Pakai & dan | dengan kurung."),
        M("Mengubah hasil filter dengan penugasan berantai.", "Pakai satu loc atau copy eksplisit."),
        M("Mengira filter tanpa hasil menimbulkan galat.", "Hasilnya tabel kosong, periksa dengan empty."),
    ],
    [
        Q("Menggabungkan syarat dengan?", ["& dan |", "and dan or", "+ dan -", "== dan !="], 0, "Operator elemen.", hint="Ampersand."),
        Q("isin memeriksa?", ["Keanggotaan dalam list", "Rentang", "Nilai hilang", "Tipe"], 0, "Anggota.", hint="Dalam."),
        Q("Cara benar mengubah baris terpilih?", ["df.loc[mask, 'kolom'] = nilai", "df[mask]['kolom'] = nilai", "df.mask = nilai", "df.set(mask)"], 0, "Satu loc.", hint="Satu langkah."),
        Q("Filter tanpa hasil memberi?", ["Tabel kosong", "Galat", "None", "Nol"], 0, "Kolom tetap ada.", hint="Kosong."),
        Q("between memeriksa?", ["Rentang inklusif", "Awalan teks", "Nilai hilang", "Duplikat"], 0, "Batas bawah dan atas.", hint="Rentang."),
    ],
    [
        "Mask boolean dari perbandingan menyaring baris tabel.",
        "Gabungkan syarat dengan &, |, dan ~ berkurung.",
        "isin, between, dan metode str membuat syarat umum.",
        "Ubah nilai bersyarat dengan satu loc, bukan penugasan berantai.",
    ],
    [],
)

H1 = """
import pandas as pd

def reindeks_hilang(df, labels):
    return int(df.reindex(labels).isna().sum().sum())
"""
H2 = """
import pandas as pd

def nama_skor_tertinggi(df):
    return df.loc[df['skor'].idxmax(), 'nama']
"""
H3 = """
import pandas as pd

def label_setelah_filter(df, umur_min):
    f = df[df['umur'] >= umur_min]
    return (f.index.tolist(), f.reset_index(drop=True).index.tolist())
"""
H4 = """
import pandas as pd

def aman_ambil(df, label, kolom, default):
    if label in df.index and kolom in df.columns:
        return df.at[label, kolom]
    return default
"""

l3 = lesson(
    "B2-02-3",
    "Indeks, reindex, dan jebakan pemilihan",
    35,
    [
        "Memahami bahwa label indeks bertahan setelah filter",
        "Memakai reset_index, reindex, dan sort_index",
        "Mencari baris dengan idxmax dan nlargest",
        "Mengakses data dengan aman bila label mungkin tidak ada",
    ],
    [
        tb("Indeks yang bertahan", "Satu fakta sering mengejutkan pemula: setelah menyaring baris, indeks asli tetap menempel pada baris yang tersisa. Tabel yang awalnya berindeks nol sampai sembilan, setelah difilter, dapat berindeks dua, lima, dan tujuh. Akibatnya `loc[0]` mungkin tidak ada lagi, sedangkan `iloc[0]` mengambil baris pertama yang tersisa. Memahami ini mencegah kekeliruan antara label dan posisi."),
        C(
            ind("""
import pandas as pd

r = pd.DataFrame({'v': [1, 2, 3, 4]})
rf = r[r['v'] > 1]
print(rf.index.tolist())
print(rf.loc[1, 'v'], rf.iloc[0, 0])
print(rf.reset_index(drop=True).index.tolist())
print(rf.reset_index(drop=True).loc[0, 'v'])
try:
    rf.loc[0]
except KeyError:
    print('keyerror')
"""),
            ind("""
[1, 2, 3]
2 2
[0, 1, 2]
2
keyerror
"""),
            "Setelah filter, label satu masih ada tetapi nol tidak. Reset_index dengan drop membuat nomor urut baru.",
            filename="indeks_bertahan.py",
        ),
        tb("reset_index", "Metode `reset_index(drop=True)` menomori ulang baris mulai dari nol dan membuang indeks lama. Tanpa `drop=True`, indeks lama menjadi kolom baru bernama `index`. Gunakan setelah penyaringan atau penggabungan bila Anda ingin nomor urut bersih, dan bila label lama tidak lagi bermakna. Namun jangan reset bila indeks lama membawa informasi penting."),
        tb("Mencari baris ekstrem", "Fungsi `idxmax` dan `idxmin` pada Series mengembalikan label baris dengan nilai terbesar atau terkecil, yang dapat langsung dipakai pada `loc`. Metode `nlargest(n, kolom)` dan `nsmallest` mengembalikan n baris dengan nilai kolom terbesar atau terkecil sebagai tabel utuh. Keduanya lebih ringkas dan lebih cepat daripada mengurutkan seluruh tabel hanya untuk mengambil beberapa baris teratas."),
        C(
            P("""
print(df.loc[df['skor'].idxmax(), 'nama'])
print(df.nlargest(2, 'skor').index.tolist())
print(df.nsmallest(1, 'umur')['nama'].tolist())
print(df.sort_values('skor').index.tolist())
print(df.sort_values('skor').iloc[0].name)
print(df.sort_index(ascending=False).index.tolist())
"""),
            ind("""
Cici
['p3', 'p1']
['Ani']
['p4', 'p2', 'p1', 'p3']
p4
['p4', 'p3', 'p2', 'p1']
"""),
            "Idxmax memberi label yang dipakai loc. Nlargest mengambil baris teratas, dan setelah diurutkan nama baris tetap membawa labelnya.",
            filename="baris_ekstrem.py",
        ),
        tb("reindex", "Metode `reindex(labels)` menyusun ulang tabel mengikuti daftar label yang Anda berikan. Label yang tidak ada pada tabel menghasilkan baris NaN, dan label yang tidak disebutkan dibuang. Ini berbeda dari `loc` dengan list yang menimbulkan galat untuk label hilang. Reindex berguna untuk menyelaraskan beberapa tabel pada kerangka yang sama, misalnya semua tanggal dalam sebulan."),
        C(
            P("""
r = df.reindex(['p4', 'p1'])
print(r.index.tolist())
print(int(df.reindex(['p1', 'p9']).isna().sum().sum()))
print(df.reindex(['p1', 'p9']).index.tolist())
print(df.reindex(columns=['skor', 'nama']).columns.tolist())
"""),
            ind("""
['p4', 'p1']
4
['p1', 'p9']
['skor', 'nama']
"""),
            "Reindex menyusun ulang menurut label, dan label baru p9 menghasilkan empat sel hilang untuk empat kolom.",
            filename="reindex_dasar.py",
        ),
        tb("Akses aman", "Bila label atau kolom mungkin tidak ada, periksa dulu dengan `in`: `label in df.index` dan `kolom in df.columns`. Untuk Series, `get(label, default)` mengembalikan nilai bawaan bila label tidak ada. Pada DataFrame, `get(kolom, default)` bekerja untuk kolom. Pemeriksaan ini menggantikan blok try dan except dan membuat niat kode jelas."),
        C(
            P("""
print(df.get('umur').tolist())
print(df.get('zzz', 'tak ada'))
print('umur' in df, 'p1' in df.index, 'p9' in df.index)
print(df['skor'].get('p9', -1))
print(df.loc[df['kota'] == 'Q', 'nama'].tolist(), df[df['kota'] == 'Q'].empty)
"""),
            ind("""
[20, 25, 22, 30]
tak ada
True True False
-1
[] True
"""),
            "Get memberi nilai bawaan untuk kolom atau label yang tidak ada. In memeriksa keberadaan, dan filter kosong ditandai empty.",
            filename="akses_aman.py",
        ),
        tb("Indeks duplikat", "Indeks pandas boleh berisi label berulang. Pada kasus itu `loc[label]` mengembalikan semua baris yang cocok sebagai tabel, bukan satu baris. Kode yang mengharapkan satu baris dapat rusak diam-diam. Periksa `df.index.is_unique` sebelum mengandalkan label sebagai kunci, dan gunakan `duplicated` untuk menemukan pengulangannya. Bila perlu kunci unik, buat kolom kunci eksplisit."),
        tb("Posisi dan label bercampur", "Kesalahan umum: memakai angka pada kurung siku langsung, misalnya `df[0]`, yang mencari kolom berlabel nol dan bukan baris pertama. Pada Series dengan indeks bilangan bulat, `s[0]` mencari label nol, tidak selalu posisi. Biasakan memakai `loc` atau `iloc` secara eksplisit sehingga niat kode tidak ambigu dan hasilnya tidak berubah ketika indeks berubah."),
        tb("Ringkasan modul", "Anda telah belajar memilih sel, baris, dan kolom dengan loc dan iloc, menyaring dengan mask, mengubah nilai bersyarat dengan satu loc, serta mengenali jebakan indeks yang bertahan. Aturan pegangan: label untuk makna, posisi untuk urutan, satu loc untuk penugasan, dan reset_index setelah filter bila nomor urut bersih diperlukan. Modul berikutnya membahas filtering, sorting, dan query secara lebih mendalam."),
        K("tip", "Setelah memfilter, indeks lama bertahan. Bedakan label (loc) dan posisi (iloc), dan reset_index bila perlu nomor urut baru.", title="Indeks bertahan"),
        tb("Memilih dengan urutan kustom", "Untuk menyusun baris dalam urutan kustom, gunakan `loc` dengan list label atau `reindex`. Misalnya menampilkan hari dalam urutan Senin sampai Minggu, bukan urutan abjad. Alternatifnya, ubah kolom menjadi tipe kategori berurutan dengan `pd.Categorical` sehingga `sort_values` mengikuti urutan yang Anda tentukan. Cara terakhir membuat urutan konsisten di seluruh analisis."),
        tb("Memilih elemen acak", "Metode `sample(n, random_state=seed)` mengambil n baris acak yang dapat diulang, dan `frac` mengambil sebagian proporsi. Ini lebih baik daripada `head` untuk melihat sekilas isi data karena baris awal sering tidak mewakili keseluruhan. Selalu tetapkan `random_state` agar sampel yang sama muncul saat analisis dijalankan ulang, sesuai prinsip reproduksibilitas."),
        tb("Membandingkan dua tabel", "Untuk mencari baris yang ada di satu tabel tetapi tidak di yang lain, gunakan `isin` pada indeks atau kolom kunci. Misalnya `a.loc[~a.index.isin(b.index)]` memberi baris yang hanya ada di a. Perbandingan berbasis label seperti ini aman karena tidak bergantung pada urutan baris, dan menjadi dasar sebelum membahas penggabungan tabel pada modul berikutnya."),
        E(
            "B2-02-3-ex1",
            "mudah",
            "Tulis fungsi `reindeks_hilang(df, labels)` yang menyusun ulang `df` mengikuti list `labels` dengan `reindex` dan mengembalikan jumlah sel hilang pada hasilnya sebagai int.",
            ind("""
import pandas as pd

def reindeks_hilang(df, labels):
    # TODO: implementasikan
    pass
"""),
            P("""
assert reindeks_hilang(df, ['p1', 'p9']) == 4
assert reindeks_hilang(df, ['p1', 'p2']) == 0
assert reindeks_hilang(df, ['x', 'y', 'z']) == 12
assert type(reindeks_hilang(df, ['p1'])) is int
"""),
            "reindex lalu jumlahkan isna dua kali.",
            H1.strip("\n"),
        ),
        E(
            "B2-02-3-ex2",
            "sedang",
            "Tulis fungsi `nama_skor_tertinggi(df)` yang mengembalikan `nama` pada baris dengan `skor` terbesar, memakai `idxmax` dan `loc`.",
            ind("""
import pandas as pd

def nama_skor_tertinggi(df):
    # TODO: implementasikan
    pass
"""),
            P("""
assert nama_skor_tertinggi(df) == 'Cici'
assert nama_skor_tertinggi(df.iloc[::-1]) == 'Cici'
assert nama_skor_tertinggi(df.iloc[:2]) == 'Ani'
assert nama_skor_tertinggi(df.iloc[3:]) == 'Dedi'
"""),
            "idxmax memberi label, loc mengambil nama.",
            H2.strip("\n"),
        ),
        E(
            "B2-02-3-ex3",
            "sedang",
            "Tulis fungsi `label_setelah_filter(df, umur_min)` yang menyaring baris dengan `umur` sekurang-kurangnya `umur_min` lalu mengembalikan tuple berisi list label indeks hasil filter dan list indeks setelah `reset_index(drop=True)`.",
            ind("""
import pandas as pd

def label_setelah_filter(df, umur_min):
    # TODO: implementasikan
    pass
"""),
            P("""
assert label_setelah_filter(df, 22) == (['p2', 'p3', 'p4'], [0, 1, 2])
assert label_setelah_filter(df, 30) == (['p4'], [0])
assert label_setelah_filter(df, 99) == ([], [])
assert label_setelah_filter(df, 0)[0] == ['p1', 'p2', 'p3', 'p4']
"""),
            "Filter lalu ambil index dan index setelah reset_index.",
            H3.strip("\n"),
        ),
        E(
            "B2-02-3-ex4",
            "menantang",
            "Tulis fungsi `aman_ambil(df, label, kolom, default)` yang mengembalikan nilai sel pada baris `label` dan kolom `kolom`, atau `default` bila label atau kolom tidak ada, tanpa memakai try dan except.",
            ind("""
import pandas as pd

def aman_ambil(df, label, kolom, default):
    # TODO: implementasikan
    pass
"""),
            P("""
assert aman_ambil(df, 'p2', 'nama', 'x') == 'Budi'
assert aman_ambil(df, 'p9', 'nama', 'x') == 'x'
assert aman_ambil(df, 'p1', 'zzz', -1) == -1
assert aman_ambil(df, 'p3', 'skor', 0) == 90.0
"""),
            "Periksa keberadaan label dan kolom dengan in sebelum at.",
            H4.strip("\n"),
        ),
    ],
    [
        M("Mengira loc[0] selalu baris pertama.", "Setelah filter, gunakan iloc atau reset_index."),
        M("Memakai df[0] untuk baris pertama.", "Pakai df.iloc[0]."),
        M("Mengandalkan label tanpa memeriksa keunikan.", "Cek index.is_unique."),
    ],
    [
        Q("Setelah filter indeks lama?", ["Bertahan", "Hilang", "Diacak", "Menjadi kolom"], 0, "Label menempel.", hint="Menempel."),
        Q("reset_index(drop=True) menghasilkan?", ["Nomor urut baru", "Indeks sama", "Kolom baru", "Tabel kosong"], 0, "Nol sampai n.", hint="Baru."),
        Q("idxmax mengembalikan?", ["Label", "Nilai", "Posisi", "Rata-rata"], 0, "Label terbesar.", hint="Label."),
        Q("reindex pada label tak ada memberi?", ["Baris NaN", "Galat", "Nol", "Dibuang"], 0, "Baris hilang.", hint="NaN."),
        Q("Cara aman memeriksa label?", ["label in df.index", "df.label", "df[label]", "df.loc[label]"], 0, "In.", hint="in."),
    ],
    [
        "Indeks lama bertahan setelah filter, bedakan label dan posisi.",
        "reset_index, sort_index, dan reindex mengatur ulang indeks.",
        "idxmax dan nlargest menemukan baris ekstrem.",
        "Periksa keberadaan label dan kolom sebelum akses.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perintah yang cukup jelas dalam teks.", "brief": []}

write_module(
    "B2",
    2,
    "Memilih data dengan loc dan iloc",
    105,
    [
        "Memilih sel, baris, dan kolom dengan loc dan iloc",
        "Menyaring dan mengubah data bersyarat dengan aman",
        "Mengelola indeks dan menghindari jebakan pemilihan",
    ],
    [l1, l2, l3],
    video,
    REF,
)
