import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

DFX = """
import numpy as np
import pandas as pd

df = pd.DataFrame({
    'nama': ['Ani Putri', 'Budi Santoso', 'Cici Lestari', 'Dedi Kurnia'],
    'divisi': ['IT', 'HR', 'IT', 'Ops'],
    'gaji': [8000000, 6000000, 9500000, 5000000],
    'masuk': ['2020-03-15', '2019-11-01', '2022-07-20', '2021-01-10'],
    'skor': [88.5, 72.0, 95.0, 64.5],
})
"""


def tb(h, b):
    return T("## " + h + "\n\n" + b)


def ind(s):
    return textwrap.indent(s.strip("\n"), "            ")


def P(body):
    return ind(DFX + "\n" + textwrap.dedent(body).strip("\n"))


F1 = """
import pandas as pd

def tambah_bonus(df, persen):
    return df.assign(bonus=df['gaji'] * persen / 100)['bonus'].tolist()
"""
F2 = """
import numpy as np
import pandas as pd

def kategori_skor(df):
    return np.select([df['skor'] >= 90, df['skor'] >= 70], ['A', 'B'], default='C').tolist()
"""
F3 = """
import pandas as pd

def kelompok_cut(df):
    return pd.cut(df['skor'], [0, 70, 90, 100], labels=['rendah', 'sedang', 'tinggi']).astype(str).tolist()
"""
F4 = """
import pandas as pd

def normalisasi_minmax(s):
    s = pd.Series(s, dtype=float)
    return ((s - s.min()) / (s.max() - s.min())).round(3).tolist()
"""

l1 = lesson(
    "B2-04-1",
    "Kolom turunan yang vectorized",
    35,
    [
        "Membuat kolom baru dari operasi antar kolom",
        "Memberi label bersyarat dengan np.where dan np.select",
        "Mengelompokkan angka dengan pd.cut dan pd.qcut",
        "Membatasi, membulatkan, dan mengubah tipe kolom",
    ],
    [
        tb("Mengapa kolom turunan", "Data mentah jarang langsung menjawab pertanyaan. Kita perlu bonus dari gaji, kategori dari skor, atau masa kerja dari tanggal masuk. Kolom turunan adalah kolom baru yang dihitung dari kolom yang sudah ada. Membuatnya dengan benar adalah jantung rekayasa fitur, dan cara terbaik adalah operasi vectorized yang bekerja pada seluruh kolom sekaligus, bukan perulangan baris demi baris."),
        tb("Data contoh", "Pelajaran ini memakai tabel karyawan kecil dengan kolom `nama`, `divisi`, `gaji`, `masuk` berupa teks tanggal, dan `skor` penilaian kinerja. Empat baris cukup untuk memeriksa hasil dengan tangan. Kebiasaan memeriksa kolom turunan pada contoh kecil sebelum menerapkannya ke jutaan baris menangkap banyak kesalahan rumus dengan biaya hampir nol."),
        C(
            P("""
d = df.assign(bonus=df['gaji'] * 0.1, gaji_juta=df['gaji'] / 1e6)
print(d['bonus'].tolist())
print(d['gaji_juta'].tolist())
print(df.columns.tolist())
print(d.columns.tolist())
df['gaji_k'] = df['gaji'] // 1000
print(df['gaji_k'].tolist())
"""),
            ind("""
[800000.0, 600000.0, 950000.0, 500000.0]
[8.0, 6.0, 9.5, 5.0]
['nama', 'divisi', 'gaji', 'masuk', 'skor']
['nama', 'divisi', 'gaji', 'masuk', 'skor', 'bonus', 'gaji_juta']
[8000, 6000, 9500, 5000]
"""),
            "Assign mengembalikan tabel baru, sedangkan penugasan langsung menambah kolom pada tabel itu sendiri.",
            filename="kolom_turunan.py",
        ),
        tb("Aritmetika antar kolom", "Operator aritmetika antar kolom bekerja per baris dan selaras dengan indeks. Rasio, selisih, persentase, dan rumus gabungan ditulis seperti rumus matematika. Perhatikan pembagian dengan nol yang menghasilkan tak hingga, dan nilai hilang yang menular: bila salah satu operan NaN, hasilnya NaN. Tangani keduanya dengan sengaja sebelum mempercayai kolom turunan."),
        tb("Label bersyarat", "Untuk memberi label berdasarkan syarat, `np.where(syarat, nilai_benar, nilai_salah)` memilih antara dua nilai per baris. Untuk lebih dari dua kategori, `np.select(daftar_syarat, daftar_nilai, default=...)` memeriksa syarat berurutan dan memakai nilai syarat pertama yang cocok. Urutan syarat penting: tulis yang paling spesifik lebih dulu karena pemeriksaan berhenti pada kecocokan pertama."),
        C(
            P("""
print(np.where(df['skor'] >= 80, 'baik', 'cukup').tolist())
print(np.select([df['skor'] >= 90, df['skor'] >= 70], ['A', 'B'], default='C').tolist())
df['kat'] = np.where(df['gaji'] >= 8000000, 'tinggi', 'biasa')
print(df['kat'].tolist())
print(df.groupby('kat').size().to_dict())
"""),
            ind("""
['baik', 'cukup', 'baik', 'cukup']
['B', 'B', 'A', 'C']
['tinggi', 'biasa', 'tinggi', 'biasa']
{'biasa': 2, 'tinggi': 2}
"""),
            "Where memilih dua nilai, select memilih banyak nilai menurut syarat berurutan dengan default untuk sisanya.",
            filename="label_bersyarat.py",
        ),
        tb("Mengelompokkan dengan cut", "Fungsi `pd.cut(kolom, batas, labels=...)` membagi angka kontinu ke dalam kelompok menurut batas yang Anda tentukan. Batas dengan n elemen menghasilkan n minus satu kelompok. Secara bawaan tiap kelompok tertutup di kanan, ditulis `(70, 90]`, dan argumen `right=False` membaliknya. Nilai di luar semua batas menjadi NaN, jadi pastikan batas mencakup seluruh rentang data."),
        tb("Kuantil dengan qcut", "Fungsi `pd.qcut(kolom, q)` membagi data menurut kuantil sehingga tiap kelompok berisi jumlah baris kira-kira sama. Misalnya `q=4` menghasilkan kuartil. Berbeda dari `cut` yang batasnya tetap, batas `qcut` mengikuti sebaran data. Ia cocok untuk membuat tingkat relatif seperti kelompok pendapatan terendah sampai tertinggi, sedangkan `cut` cocok untuk ambang yang bermakna bisnis seperti rentang usia."),
        C(
            P("""
print(pd.cut(df['skor'], [0, 70, 90, 100], labels=['rendah', 'sedang', 'tinggi']).astype(str).tolist())
print(pd.cut(df['skor'], [0, 70, 90, 100]).astype(str).tolist())
print(pd.cut(df['skor'], [0, 70, 90, 100], right=False, labels=False).tolist())
print(pd.qcut(df['gaji'], 2, labels=['bawah', 'atas']).astype(str).tolist())
print(pd.qcut(df['gaji'], 4, labels=False).tolist())
"""),
            ind("""
['sedang', 'sedang', 'tinggi', 'rendah']
['(70, 90]', '(70, 90]', '(90, 100]', '(0, 70]']
[1, 1, 2, 0]
['atas', 'bawah', 'atas', 'bawah']
[2, 1, 3, 0]
"""),
            "Cut memakai batas tetap dan qcut memakai kuantil. Labels False mengembalikan nomor kelompok.",
            filename="cut_qcut.py",
        ),
        tb("Membatasi dan membulatkan", "Metode `clip(bawah, atas)` membatasi nilai ke dalam rentang, `round(n)` membulatkan ke n desimal, dan `astype` mengubah tipe. Ingat bahwa `round` pandas membulatkan setengah ke genap terdekat seperti NumPy, jadi 88,5 menjadi 88 dan 64,5 menjadi 64. Konversi ke bilangan bulat dengan `astype(int)` memotong pecahan dan gagal bila ada nilai hilang, kecuali Anda memakai tipe bilangan bulat yang mendukung hilang seperti `Int64`."),
        C(
            P("""
print(df['skor'].clip(70, 90).tolist())
print(df['skor'].round().tolist())
print(df['skor'].astype(int).tolist())
print(df['gaji'].pct_change().round(3).tolist())
print(df['gaji'].diff().tolist())
print((df['gaji'] / df['gaji'].sum() * 100).round(1).tolist())
"""),
            ind("""
[88.5, 72.0, 90.0, 70.0]
[88.0, 72.0, 95.0, 64.0]
[88, 72, 95, 64]
[nan, -0.25, 0.583, -0.474]
[nan, -2000000.0, 3500000.0, -4500000.0]
[28.1, 21.1, 33.3, 17.5]
"""),
            "Clip membatasi rentang, round membulatkan setengah ke genap, dan pct_change serta diff menghasilkan nilai hilang pada baris pertama.",
            filename="clip_round.py",
        ),
        tb("Normalisasi min-max", "Normalisasi min-max mengubah kolom ke rentang nol sampai satu dengan rumus nilai dikurangi minimum dibagi rentang. Kolom turunan ini membuat fitur berskala berbeda dapat dibandingkan dan sering diperlukan algoritma pembelajaran mesin berbasis jarak. Tangani kolom konstan yang rentangnya nol agar tidak terjadi pembagian dengan nol, misalnya dengan menggantinya nol sebelum membagi."),
        tb("Dummy dan kode kategori", "Algoritma numerik membutuhkan angka, sehingga kategori sering diubah. `pd.get_dummies` membuat satu kolom nol dan satu per kategori, disebut pengkodean one-hot, dan `astype('category').cat.codes` memberi nomor urut tiap kategori. Gunakan one-hot untuk kategori tanpa urutan, dan kode berurutan hanya bila kategori memang memiliki urutan bermakna."),
        tb("Hindari perulangan baris", "Godaan terbesar pemula adalah perulangan `for` atas baris untuk menghitung kolom baru. Hampir semuanya dapat ditulis vectorized dengan operasi kolom, `np.where`, `np.select`, atau `cut`. Versi vectorized puluhan hingga ratusan kali lebih cepat dan lebih pendek. Pelajaran berikutnya membahas `map` dan `apply` untuk kasus yang benar-benar membutuhkan fungsi per elemen atau per baris."),
        K("tip", "Sebelum menulis perulangan atas baris, tanyakan apakah operasi kolom, np.where, np.select, atau cut dapat mengerjakannya sekaligus.", title="Vectorized dulu"),
        tb("Memeriksa kolom turunan", "Setelah membuat kolom baru, periksa tiga hal: tipe datanya, jumlah nilai hilang, dan beberapa baris contoh yang dihitung dengan tangan. Kesalahan umum meliputi urutan syarat yang terbalik, batas cut yang tidak mencakup seluruh data, dan pembagian bilangan bulat yang tidak sesuai harapan. Pemeriksaan singkat ini murah dan menyelamatkan Anda dari kesimpulan yang salah akibat satu rumus keliru di hulu analisis."),
        E(
            "B2-04-1-ex1",
            "mudah",
            "Tulis fungsi `tambah_bonus(df, persen)` yang menghitung kolom bonus sebesar `persen` persen dari `gaji` dan mengembalikan kolom itu sebagai list, tanpa mengubah tabel asal.",
            ind("""
import pandas as pd

def tambah_bonus(df, persen):
    # TODO: implementasikan
    pass
"""),
            P("""
assert tambah_bonus(df, 10) == [800000.0, 600000.0, 950000.0, 500000.0]
assert tambah_bonus(df, 0) == [0.0, 0.0, 0.0, 0.0]
assert tambah_bonus(df, 100) == [8000000.0, 6000000.0, 9500000.0, 5000000.0]
assert 'bonus' not in df.columns
"""),
            "assign kolom baru dari gaji dikali persen dibagi seratus.",
            F1.strip("\n"),
        ),
        E(
            "B2-04-1-ex2",
            "sedang",
            "Tulis fungsi `kategori_skor(df)` yang mengembalikan list kategori: `'A'` bila `skor` sekurang-kurangnya 90, `'B'` bila sekurang-kurangnya 70, dan `'C'` untuk lainnya, memakai `np.select`.",
            ind("""
import numpy as np
import pandas as pd

def kategori_skor(df):
    # TODO: implementasikan
    pass
"""),
            P("""
assert kategori_skor(df) == ['B', 'B', 'A', 'C']
assert kategori_skor(df.iloc[[2]]) == ['A']
assert kategori_skor(df.iloc[[3, 1]]) == ['C', 'B']
assert kategori_skor(pd.DataFrame({'skor': [90.0, 70.0, 69.9]})) == ['A', 'B', 'C']
"""),
            "np.select dengan dua syarat berurutan dan default C.",
            F2.strip("\n"),
        ),
        E(
            "B2-04-1-ex3",
            "sedang",
            "Tulis fungsi `kelompok_cut(df)` yang mengelompokkan `skor` dengan `pd.cut` pada batas 0, 70, 90, 100 berlabel `'rendah'`, `'sedang'`, `'tinggi'`, dan mengembalikan labelnya sebagai list string.",
            ind("""
import pandas as pd

def kelompok_cut(df):
    # TODO: implementasikan
    pass
"""),
            P("""
assert kelompok_cut(df) == ['sedang', 'sedang', 'tinggi', 'rendah']
assert kelompok_cut(df.iloc[[0]]) == ['sedang']
assert kelompok_cut(pd.DataFrame({'skor': [70.0, 90.0, 100.0]})) == ['rendah', 'sedang', 'tinggi']
assert len(kelompok_cut(df)) == 4
"""),
            "pd.cut dengan bins dan labels lalu ubah ke string.",
            F3.strip("\n"),
        ),
        E(
            "B2-04-1-ex4",
            "menantang",
            "Tulis fungsi `normalisasi_minmax(s)` yang menerima list atau Series angka dan mengembalikan list nilai ternormalisasi min-max ke rentang 0 sampai 1, dibulatkan ke tiga desimal.",
            ind("""
import pandas as pd

def normalisasi_minmax(s):
    # TODO: implementasikan
    pass
"""),
            P("""
assert normalisasi_minmax([2, 4, 6]) == [0.0, 0.5, 1.0]
assert normalisasi_minmax(df['gaji']) == [0.667, 0.222, 1.0, 0.0]
assert normalisasi_minmax([10, 20]) == [0.0, 1.0]
assert normalisasi_minmax(df['skor'])[2] == 1.0
"""),
            "Kurangi minimum lalu bagi dengan rentang dan bulatkan.",
            F4.strip("\n"),
        ),
    ],
    [
        M("Memakai perulangan baris untuk kolom turunan.", "Pakai operasi kolom, where, select, atau cut."),
        M("Menulis syarat select dari yang paling umum.", "Tulis yang paling spesifik lebih dulu."),
        M("Batas cut tidak mencakup seluruh data.", "Pastikan batas melingkupi minimum dan maksimum."),
    ],
    [
        Q("np.select dipakai untuk?", ["Banyak kategori bersyarat", "Mengurutkan", "Menggabung", "Mengacak"], 0, "Berurutan.", hint="Banyak."),
        Q("pd.cut memakai?", ["Batas tetap", "Kuantil", "Acak", "Indeks"], 0, "Bins.", hint="Batas."),
        Q("pd.qcut memakai?", ["Kuantil", "Batas tetap", "Acak", "Label"], 0, "Jumlah sama.", hint="Kuantil."),
        Q("pct_change baris pertama?", ["NaN", "0", "1", "Galat"], 0, "Tak ada sebelumnya.", hint="NaN."),
        Q("One-hot dibuat dengan?", ["pd.get_dummies", "pd.cut", "pd.rank", "np.select"], 0, "Dummies.", hint="Dummies."),
    ],
    [
        "Kolom turunan dibuat dengan operasi kolom vectorized.",
        "np.where dan np.select memberi label bersyarat.",
        "cut dan qcut mengelompokkan angka kontinu.",
        "Hindari perulangan baris untuk kolom turunan.",
    ],
    [],
)

G1 = """
import pandas as pd

def petakan_divisi(df, peta):
    return df['divisi'].map(peta).fillna('Lainnya').tolist()
"""
G2 = """
import pandas as pd

def kode_baris(df):
    return df.apply(lambda r: r['nama'].split()[0] + '-' + r['divisi'], axis=1).tolist()
"""
G3 = """
import pandas as pd

def rentang_kolom(df, kolom):
    return df[kolom].apply(lambda c: c.max() - c.min()).to_dict()
"""
G4 = """
import numpy as np
import pandas as pd

def gaji_setelah_naik(df, batas, faktor):
    return np.where(df['skor'] >= batas, df['gaji'] * faktor, df['gaji'] * 1.0).tolist()
"""

l2 = lesson(
    "B2-04-2",
    "map, replace, dan apply",
    35,
    [
        "Memetakan nilai dengan map dan replace",
        "Menerapkan fungsi pada kolom dengan apply dan map",
        "Menerapkan fungsi pada baris dengan apply axis satu",
        "Mengetahui kapan apply lambat dan bagaimana menghindarinya",
    ],
    [
        tb("Fungsi per elemen", "Terkadang kita perlu memetakan nilai secara khusus: kode divisi menjadi nama lengkap, atau menerapkan fungsi buatan sendiri yang tidak ada padanan vectorized-nya. Pandas menyediakan `map` untuk Series, `replace` untuk mengganti nilai, dan `apply` untuk menerapkan fungsi pada kolom atau baris. Ketiganya fleksibel tetapi lebih lambat dari operasi vectorized, jadi gunakan hanya bila diperlukan."),
        tb("map dengan dict", "Metode `map` pada Series menerima dict, fungsi, atau Series. Dengan dict, setiap nilai diganti menurut pasangannya, dan nilai yang tidak ada pada dict menjadi NaN. Sifat ini penting: `map` tidak mempertahankan nilai asal bila tidak ditemukan. Bila Anda ingin sisanya tetap, pakai `replace`, atau lengkapi hasil `map` dengan `fillna` yang tepat."),
        C(
            P("""
peta = {'IT': 'Teknologi', 'HR': 'SDM'}
print(df['divisi'].map(peta).tolist())
print(df['divisi'].map(peta).fillna('Lainnya').tolist())
print(df['divisi'].replace(peta).tolist())
print(df['divisi'].map(str.lower).tolist())
print(df['divisi'].map(len).tolist())
"""),
            ind("""
['Teknologi', 'SDM', 'Teknologi', nan]
['Teknologi', 'SDM', 'Teknologi', 'Lainnya']
['Teknologi', 'SDM', 'Teknologi', 'Ops']
['it', 'hr', 'it', 'ops']
[2, 2, 2, 3]
"""),
            "Map mengubah yang tak dikenal menjadi NaN, sedangkan replace mempertahankannya. Map juga menerima fungsi.",
            filename="map_replace.py",
        ),
        tb("apply pada Series", "Metode `apply(fungsi)` pada Series memanggil fungsi sekali untuk setiap elemen dan mengumpulkan hasilnya. Untuk Series, `map` dan `apply` hampir setara dengan fungsi per elemen. Fungsi dapat berupa lambda atau fungsi bernama. Bila fungsi Anda hanya terdiri dari aritmetika dasar, tulis ulang sebagai operasi vectorized yang jauh lebih cepat dan tidak membutuhkan apply sama sekali."),
        tb("apply pada baris", "Pada DataFrame, `apply(fungsi, axis=1)` memanggil fungsi sekali per baris dengan baris sebagai Series yang indeksnya nama kolom. Ini berguna ketika hasil bergantung pada beberapa kolom dengan logika yang rumit. Namun biayanya besar karena pandas membuat Series untuk setiap baris, sehingga pada jutaan baris ia sangat lambat. Selalu pertimbangkan versi vectorized dengan `np.where` atau `np.select` lebih dulu."),
        C(
            P("""
print(df.apply(lambda r: r['nama'].split()[0] + '-' + r['divisi'], axis=1).tolist())
print(df['gaji'].apply(lambda g: g // 1000000).tolist())
print(df['skor'].map(lambda x: 'lulus' if x >= 70 else 'gagal').tolist())
print(df.apply(lambda r: r['gaji'] * (1.1 if r['skor'] >= 80 else 1.0), axis=1).tolist())
print(np.where(df['skor'] >= 80, df['gaji'] * 1.1, df['gaji'] * 1.0).tolist())
"""),
            ind("""
['Ani-IT', 'Budi-HR', 'Cici-IT', 'Dedi-Ops']
[8, 6, 9, 5]
['lulus', 'lulus', 'lulus', 'gagal']
[8800000.0, 6000000.0, 10450000.0, 5000000.0]
[8800000.0, 6000000.0, 10450000.0, 5000000.0]
"""),
            "Apply per baris dan versi vectorized dengan np.where memberi hasil sama, tetapi versi kedua jauh lebih cepat.",
            filename="apply_baris.py",
        ),
        tb("apply pada kolom", "Pada DataFrame, `apply(fungsi)` dengan `axis=0` secara bawaan memanggil fungsi sekali per kolom dengan kolom sebagai Series. Ini cocok untuk menerapkan transformasi yang sama pada banyak kolom, seperti normalisasi atau rentang. Fungsi yang mengembalikan satu nilai menghasilkan Series ringkasan, dan fungsi yang mengembalikan Series berpanjang sama menghasilkan DataFrame transformasi."),
        C(
            P("""
num = df[['gaji', 'skor']]
print(num.apply(lambda c: c.max() - c.min()).to_dict())
norm = num.apply(lambda c: (c - c.min()) / (c.max() - c.min()))
print(norm.round(3).values.tolist())
print(num.agg(['min', 'max']).values.tolist())
print(num.agg({'gaji': 'sum', 'skor': 'mean'}).to_dict())
"""),
            ind("""
{'gaji': 4500000.0, 'skor': 30.5}
[[0.667, 0.787], [0.222, 0.246], [1.0, 1.0], [0.0, 0.0]]
[[5000000.0, 64.5], [9500000.0, 95.0]]
{'gaji': 28500000.0, 'skor': 80.0}
"""),
            "Apply per kolom meringkas atau mentransformasi tiap kolom. Agg menjalankan beberapa ringkasan sekaligus.",
            filename="apply_kolom.py",
        ),
        tb("Mengukur kecepatan", "Bila ragu memakai apply atau vectorized, ukur dengan `time.perf_counter` atau `%timeit`. Pada puluhan ribu baris, apply per baris sering seratus kali lebih lambat. Pada tabel kecil perbedaannya tak terasa, dan kejelasan kode lebih penting. Aturan pegangan: tulis vectorized bila bisa, pakai apply bila logikanya benar-benar sulit dinyatakan vectorized dan data tidak besar."),
        tb("Fungsi dengan argumen", "Argumen tambahan dapat diteruskan ke fungsi apply lewat `args=(...)` atau `**kwargs`, sehingga fungsi bernama dapat dipakai ulang dengan parameter berbeda. Misalnya `df['skor'].apply(kategori, batas=70)`. Bungkus logika rumit dalam fungsi bernama dengan dokumentasi, bukan lambda panjang, agar mudah diuji terpisah dan dibaca orang lain."),
        tb("Mengganti banyak nilai", "Metode `replace` menerima dict nilai lama ke nilai baru, atau dua list sejajar. Ia dapat bekerja pada seluruh tabel sekaligus dan juga menerima ekspresi reguler dengan `regex=True`. Untuk mengganti nilai tertentu menjadi NaN, atau sebaliknya, `replace` adalah alat yang tepat. Pada kolom teks, `str.replace` bekerja pada isi tiap teks, bukan pada nilai utuh."),
        tb("Penanganan nilai hilang saat map", "Karena `map` menghasilkan NaN untuk kunci yang tak dikenal, kolom hasilnya dapat berubah tipe dari bilangan bulat menjadi desimal. Selalu periksa jumlah NaN setelah `map`: `hasil.isna().sum()` memberi tahu berapa nilai tidak terpetakan. Angka itu sering menunjukkan kode baru atau salah ketik pada data yang perlu ditambahkan ke kamus."),
        K("tip", "Map menghasilkan NaN untuk kunci tak dikenal. Hitung NaN setelah map untuk menemukan kode yang belum terpetakan.", title="Cek hasil map"),
        tb("Memilih alat yang tepat", "Urutan pilihan yang sehat adalah operasi vectorized lebih dulu, lalu `np.where` atau `np.select` untuk syarat, lalu `map` untuk kamus nilai, lalu `apply` untuk logika yang rumit. Setiap tingkat lebih fleksibel dan lebih lambat dari sebelumnya. Dengan mengikuti urutan ini, kode Anda tetap cepat pada data besar dan tetap mudah dibaca. Saat memakai apply, tuliskan alasannya dalam nama fungsi agar pembaca tahu mengapa pilihan itu diambil."),
        tb("Menguji fungsi terpisah", "Fungsi bernama yang dipakai dalam apply dapat diuji terpisah pada satu nilai atau satu baris sebelum diterapkan ke seluruh tabel. Ambil satu baris dengan `df.iloc[0]`, panggil fungsi, dan periksa hasilnya. Cara ini jauh lebih mudah ditelusuri dibanding mencari galat di tengah apply atas jutaan baris, dan pesan galat pandas pada apply sering kurang jelas tentang baris mana yang bermasalah."),
        E(
            "B2-04-2-ex1",
            "mudah",
            "Tulis fungsi `petakan_divisi(df, peta)` yang memetakan kolom `divisi` memakai dict `peta` dan mengganti divisi yang tidak ada pada dict dengan `'Lainnya'`, lalu mengembalikan hasilnya sebagai list.",
            ind("""
import pandas as pd

def petakan_divisi(df, peta):
    # TODO: implementasikan
    pass
"""),
            P("""
assert petakan_divisi(df, {'IT': 'Teknologi', 'HR': 'SDM'}) == ['Teknologi', 'SDM', 'Teknologi', 'Lainnya']
assert petakan_divisi(df, {}) == ['Lainnya'] * 4
assert petakan_divisi(df, {'IT': 'A', 'HR': 'B', 'Ops': 'C'}) == ['A', 'B', 'A', 'C']
assert petakan_divisi(df.iloc[[3]], {'Ops': 'Operasi'}) == ['Operasi']
"""),
            "map dengan dict lalu fillna.",
            G1.strip("\n"),
        ),
        E(
            "B2-04-2-ex2",
            "sedang",
            "Tulis fungsi `kode_baris(df)` yang untuk tiap baris menggabungkan kata pertama `nama`, tanda minus, dan `divisi` (misalnya `Ani-IT`), memakai `apply` per baris, dan mengembalikannya sebagai list.",
            ind("""
import pandas as pd

def kode_baris(df):
    # TODO: implementasikan
    pass
"""),
            P("""
assert kode_baris(df) == ['Ani-IT', 'Budi-HR', 'Cici-IT', 'Dedi-Ops']
assert kode_baris(df.iloc[[1]]) == ['Budi-HR']
assert kode_baris(df.iloc[::-1])[0] == 'Dedi-Ops'
assert len(kode_baris(df)) == 4
"""),
            "apply dengan axis satu dan lambda yang memecah nama.",
            G2.strip("\n"),
        ),
        E(
            "B2-04-2-ex3",
            "sedang",
            "Tulis fungsi `rentang_kolom(df, kolom)` yang menerapkan `apply` pada kolom-kolom numerik yang disebut dalam list `kolom` dan mengembalikan dict `{kolom: nilai_maks_dikurangi_nilai_min}`.",
            ind("""
import pandas as pd

def rentang_kolom(df, kolom):
    # TODO: implementasikan
    pass
"""),
            P("""
assert rentang_kolom(df, ['gaji', 'skor']) == {'gaji': 4500000.0, 'skor': 30.5}
assert rentang_kolom(df, ['skor']) == {'skor': 30.5}
assert rentang_kolom(df, ['gaji']) == {'gaji': 4500000}
assert rentang_kolom(df.iloc[[0]], ['skor']) == {'skor': 0.0}
"""),
            "Pilih kolom lalu apply fungsi maksimum dikurangi minimum.",
            G3.strip("\n"),
        ),
        E(
            "B2-04-2-ex4",
            "menantang",
            "Tulis fungsi `gaji_setelah_naik(df, batas, faktor)` yang mengembalikan list gaji setelah dikalikan `faktor` untuk karyawan dengan `skor` sekurang-kurangnya `batas`, dan tetap untuk yang lain (sebagai float), tanpa memakai `apply` per baris.",
            ind("""
import numpy as np
import pandas as pd

def gaji_setelah_naik(df, batas, faktor):
    # TODO: implementasikan
    pass
"""),
            P("""
r = gaji_setelah_naik(df, 80, 1.1)
assert np.allclose(r, [8800000.0, 6000000.0, 10450000.0, 5000000.0])
assert gaji_setelah_naik(df, 100, 2) == [8000000.0, 6000000.0, 9500000.0, 5000000.0]
assert gaji_setelah_naik(df, 0, 2) == [16000000.0, 12000000.0, 19000000.0, 10000000.0]
assert all(isinstance(x, float) for x in r)
"""),
            "np.where dengan syarat skor dan dua perhitungan gaji.",
            G4.strip("\n"),
        ),
    ],
    [
        M("Memakai map lalu heran muncul NaN.", "Map tidak mempertahankan nilai tak dikenal, pakai replace atau fillna."),
        M("Memakai apply axis=1 pada jutaan baris.", "Pakai np.where atau np.select."),
        M("Menulis lambda panjang dan rumit.", "Buat fungsi bernama yang dapat diuji."),
    ],
    [
        Q("map dengan dict untuk kunci tak dikenal menghasilkan?", ["NaN", "Nilai asal", "Galat", "Nol"], 0, "Tidak ditemukan.", hint="NaN."),
        Q("replace untuk kunci tak dikenal?", ["Mempertahankan nilai asal", "NaN", "Galat", "Nol"], 0, "Tidak diganti.", hint="Tetap."),
        Q("apply axis=1 memanggil fungsi per?", ["Baris", "Kolom", "Sel", "Tabel"], 0, "Baris.", hint="Baris."),
        Q("Operasi mana lebih cepat?", ["Vectorized", "apply per baris", "Perulangan for", "Sama"], 0, "Kode C.", hint="Vectorized."),
        Q("agg dipakai untuk?", ["Beberapa ringkasan sekaligus", "Mengurutkan", "Menggabung", "Mengacak"], 0, "Ringkasan.", hint="Agregasi."),
    ],
    [
        "map memetakan nilai dengan dict atau fungsi dan memberi NaN untuk kunci tak dikenal.",
        "apply per baris fleksibel tetapi lambat.",
        "apply per kolom menerapkan transformasi yang sama pada banyak kolom.",
        "Ukur kecepatan dan pilih vectorized bila memungkinkan.",
    ],
    [],
)

H1 = """
import pandas as pd

def nama_belakang(df):
    return df['nama'].str.split().str[-1].tolist()
"""
H2 = """
import pandas as pd

def tahun_masuk(df):
    return pd.to_datetime(df['masuk']).dt.year.tolist()
"""
H3 = """
import pandas as pd

def masa_kerja_hari(df, acuan):
    return (pd.Timestamp(acuan) - pd.to_datetime(df['masuk'])).dt.days.tolist()
"""
H4 = """
import pandas as pd

def masuk_setelah(df, tanggal):
    t = pd.to_datetime(df['masuk'])
    return df.loc[t >= pd.Timestamp(tanggal), 'nama'].tolist()
"""

l3 = lesson(
    "B2-04-3",
    "Kolom teks dan tanggal",
    35,
    [
        "Mengolah teks dengan atribut str",
        "Mengubah teks menjadi tanggal dengan to_datetime",
        "Mengambil tahun, bulan, dan hari dengan atribut dt",
        "Menghitung selisih tanggal dan memfilter menurut waktu",
    ],
    [
        tb("Dua jenis kolom khusus", "Teks dan tanggal adalah dua tipe kolom yang paling sering membutuhkan turunan. Dari nama lengkap kita perlu nama depan, dari alamat kita perlu kota, dari tanggal masuk kita perlu masa kerja. Pandas menyediakan atribut khusus `str` untuk teks dan `dt` untuk tanggal. Keduanya memuat metode vectorized yang bekerja pada seluruh kolom sekaligus tanpa perulangan."),
        tb("Atribut str", "Atribut `str` memuat padanan hampir semua metode teks Python: `upper`, `lower`, `strip`, `replace`, `split`, `contains`, `startswith`, `len`. Metode ini mengabaikan nilai hilang dengan menghasilkan NaN, bukan galat. Hasil `split` adalah kolom berisi list, dan `str[indeks]` mengambil elemen tertentu dari list tersebut, sehingga `str.split().str[0]` mengambil kata pertama."),
        C(
            P("""
print(df['nama'].str.split().str[0].tolist())
print(df['nama'].str.split().str[-1].tolist())
print(df['nama'].str.extract(r'(\\w+) (\\w+)')[1].tolist())
print(df['nama'].str.replace(' ', '_').tolist())
print(df['nama'].str.len().tolist())
print(df['nama'].str.upper().tolist())
"""),
            ind("""
['Ani', 'Budi', 'Cici', 'Dedi']
['Putri', 'Santoso', 'Lestari', 'Kurnia']
['Putri', 'Santoso', 'Lestari', 'Kurnia']
['Ani_Putri', 'Budi_Santoso', 'Cici_Lestari', 'Dedi_Kurnia']
[9, 12, 12, 11]
['ANI PUTRI', 'BUDI SANTOSO', 'CICI LESTARI', 'DEDI KURNIA']
"""),
            "Split memecah teks, indeks negatif mengambil kata terakhir, dan extract mengambil bagian dengan ekspresi reguler.",
            filename="atribut_str.py",
        ),
        tb("Ekstraksi dengan regex", "Metode `str.extract(pola)` mengambil bagian teks yang cocok dengan grup dalam ekspresi reguler dan mengembalikan DataFrame satu kolom per grup. Ia berguna untuk menarik kode dari teks berformat, misalnya nomor faktur dari kalimat. Baris yang tidak cocok menghasilkan NaN, jadi periksa jumlah NaN untuk menemukan format yang tak terduga."),
        tb("Dari teks ke tanggal", "Tanggal yang dibaca dari file biasanya berupa teks. Fungsi `pd.to_datetime` mengubahnya menjadi tipe tanggal sehingga dapat dihitung. Bila format tidak standar, beri argumen `format`, misalnya `format='%d/%m/%Y'`. Argumen `errors='coerce'` mengubah teks yang tidak dapat dibaca menjadi NaT, nilai hilang untuk tanggal, sehingga Anda bisa menghitung berapa yang bermasalah."),
        C(
            P("""
t = pd.to_datetime(df['masuk'])
print(t.dt.year.tolist())
print(t.dt.month.tolist())
print(t.dt.dayofweek.tolist())
print(t.dt.day_name().tolist())
print(t.dt.strftime('%d/%m/%Y').tolist())
print(t.dt.to_period('M').astype(str).tolist())
print(pd.to_datetime('15/03/2020', format='%d/%m/%Y').strftime('%Y-%m-%d'))
"""),
            ind("""
[2020, 2019, 2022, 2021]
[3, 11, 7, 1]
[6, 4, 2, 6]
['Sunday', 'Friday', 'Wednesday', 'Sunday']
['15/03/2020', '01/11/2019', '20/07/2022', '10/01/2021']
['2020-03', '2019-11', '2022-07', '2021-01']
2020-03-15
"""),
            "Atribut dt mengambil bagian tanggal, strftime memformat, dan to_period membulatkan ke bulan. Hari dimulai dari nol untuk Senin.",
            filename="atribut_dt.py",
        ),
        tb("Atribut tanggal", "Atribut `dt` menyediakan `year`, `month`, `day`, `dayofweek`, `quarter`, `is_month_start`, dan lainnya, serta `day_name()` dan `month_name()` untuk nama. Nomor hari dalam pekan dimulai dari nol untuk Senin sampai enam untuk Minggu. Metode `strftime` memformat tanggal menjadi teks, dan `to_period` membulatkannya ke bulan atau kuartal untuk pengelompokan."),
        tb("Selisih tanggal", "Mengurangkan dua kolom tanggal menghasilkan kolom selisih waktu bertipe timedelta. Atribut `dt.days` mengambil jumlah hari sebagai bilangan bulat. Untuk masa kerja dalam tahun, bagi hari dengan 365,25. Mengurangkan satu tanggal tetap dari seluruh kolom bekerja lewat broadcasting. Selalu tetapkan tanggal acuan secara eksplisit, bukan memakai hari ini, agar hasil analisis dapat diulang."),
        C(
            P("""
t = pd.to_datetime(df['masuk'])
acuan = pd.Timestamp('2024-12-31')
print((acuan - t).dt.days.tolist())
print(((acuan - t).dt.days / 365.25).round(1).tolist())
print((t >= '2021-01-01').tolist())
print(df.loc[t >= '2021-01-01', 'nama'].tolist())
print(t.min().strftime('%Y-%m-%d'), (t.max() - t.min()).days)
"""),
            ind("""
[1752, 1887, 895, 1451]
[4.8, 5.2, 2.5, 4.0]
[False, False, True, True]
['Cici Lestari', 'Dedi Kurnia']
2019-11-01 992
"""),
            "Selisih dengan tanggal acuan memberi masa kerja dalam hari, dan perbandingan dengan teks tanggal memfilter menurut waktu.",
            filename="selisih_tanggal.py",
        ),
        tb("Tanggal acuan yang tetap", "Memakai `pd.Timestamp.today()` di dalam analisis membuat hasilnya berubah setiap hari, sehingga tidak dapat diulang atau diverifikasi. Tetapkan tanggal acuan sebagai parameter atau konstanta yang tercatat, misalnya tanggal pengambilan data. Prinsip yang sama berlaku untuk seed acak: apa pun yang berubah diam-diam antar run merusak reproduksibilitas."),
        tb("Zona waktu dan format", "Tanggal dengan zona waktu menambah kerumitan. Pandas mendukung zona waktu lewat `tz_localize` dan `tz_convert`. Aturan pegangan: simpan waktu dalam UTC, ubah ke zona lokal hanya saat menampilkan. Perhatikan juga format tanggal ambigu seperti 01/02/2024 yang bisa berarti satu Februari atau dua Januari, dan selalu nyatakan format secara eksplisit dengan argumen `format`."),
        tb("Ringkasan modul", "Anda telah belajar membuat kolom turunan dengan operasi vectorized, memetakan dan menerapkan fungsi dengan map dan apply, serta mengolah teks dan tanggal dengan str dan dt. Aturan utamanya: pilih operasi kolom lebih dulu, gunakan apply hanya bila perlu, dan selalu periksa NaN pada hasil. Modul berikutnya membahas nilai hilang secara dasar."),
        K("tip", "Tetapkan tanggal acuan secara eksplisit. Memakai tanggal hari ini membuat hasil analisis berubah dan tidak dapat diulang.", title="Acuan tetap"),
        tb("Teks kotor dan konsisten", "Data teks dari dunia nyata jarang bersih. Spasi di tepi, huruf besar dan kecil bercampur, dan variasi ejaan membuat pengelompokan gagal karena dianggap nilai berbeda. Rangkaian `str.strip().str.lower()` adalah langkah pembersihan paling umum. Lakukan sebelum `groupby`, `merge`, atau `value_counts` agar nilai yang sama benar-benar dihitung sebagai satu kategori yang sama."),
        tb("Memeriksa tanggal bermasalah", "Setelah `to_datetime` dengan `errors='coerce'`, hitung `isna().sum()` untuk mengetahui berapa tanggal gagal dibaca, lalu lihat baris asalnya untuk memahami polanya. Tanggal yang salah sering berasal dari format campuran dalam satu kolom, nilai placeholder seperti nol, atau salah ketik. Menemukan pola ini lebih awal mencegah analisis waktu yang diam-diam kehilangan sebagian data."),
        E(
            "B2-04-3-ex1",
            "mudah",
            "Tulis fungsi `nama_belakang(df)` yang mengembalikan list kata terakhir dari kolom `nama` pada tiap baris.",
            ind("""
import pandas as pd

def nama_belakang(df):
    # TODO: implementasikan
    pass
"""),
            P("""
assert nama_belakang(df) == ['Putri', 'Santoso', 'Lestari', 'Kurnia']
assert nama_belakang(df.iloc[[0]]) == ['Putri']
assert nama_belakang(pd.DataFrame({'nama': ['A B C', 'X']})) == ['C', 'X']
assert len(nama_belakang(df)) == 4
"""),
            "str.split lalu str dengan indeks minus satu.",
            H1.strip("\n"),
        ),
        E(
            "B2-04-3-ex2",
            "sedang",
            "Tulis fungsi `tahun_masuk(df)` yang mengubah kolom `masuk` menjadi tanggal dan mengembalikan list tahun tiap baris.",
            ind("""
import pandas as pd

def tahun_masuk(df):
    # TODO: implementasikan
    pass
"""),
            P("""
assert tahun_masuk(df) == [2020, 2019, 2022, 2021]
assert tahun_masuk(df.iloc[[2]]) == [2022]
assert tahun_masuk(pd.DataFrame({'masuk': ['2024-12-31']})) == [2024]
assert tahun_masuk(df.iloc[::-1])[0] == 2021
"""),
            "to_datetime lalu atribut dt year.",
            H2.strip("\n"),
        ),
        E(
            "B2-04-3-ex3",
            "sedang",
            "Tulis fungsi `masa_kerja_hari(df, acuan)` yang mengembalikan list jumlah hari dari tanggal `masuk` tiap baris sampai tanggal `acuan` (teks tanggal ISO).",
            ind("""
import pandas as pd

def masa_kerja_hari(df, acuan):
    # TODO: implementasikan
    pass
"""),
            P("""
assert masa_kerja_hari(df, '2024-12-31') == [1752, 1887, 895, 1451]
assert masa_kerja_hari(df, '2020-03-15')[0] == 0
assert masa_kerja_hari(df.iloc[[1]], '2019-11-02') == [1]
assert all(isinstance(x, int) for x in masa_kerja_hari(df, '2024-12-31'))
"""),
            "Kurangkan tanggal masuk dari Timestamp acuan lalu ambil dt days.",
            H3.strip("\n"),
        ),
        E(
            "B2-04-3-ex4",
            "menantang",
            "Tulis fungsi `masuk_setelah(df, tanggal)` yang mengembalikan list `nama` untuk karyawan yang `masuk`-nya pada atau setelah `tanggal` (teks tanggal ISO).",
            ind("""
import pandas as pd

def masuk_setelah(df, tanggal):
    # TODO: implementasikan
    pass
"""),
            P("""
assert masuk_setelah(df, '2021-01-01') == ['Cici Lestari', 'Dedi Kurnia']
assert masuk_setelah(df, '2023-01-01') == []
assert masuk_setelah(df, '2019-01-01') == ['Ani Putri', 'Budi Santoso', 'Cici Lestari', 'Dedi Kurnia']
assert masuk_setelah(df, '2022-07-20') == ['Cici Lestari']
"""),
            "Ubah masuk ke tanggal lalu bandingkan dengan Timestamp.",
            H4.strip("\n"),
        ),
    ],
    [
        M("Memakai tanggal hari ini sebagai acuan analisis.", "Tetapkan tanggal acuan eksplisit."),
        M("Membiarkan tanggal bertipe teks.", "Ubah dengan to_datetime."),
        M("Format tanggal ambigu tanpa format eksplisit.", "Tulis argumen format."),
    ],
    [
        Q("Atribut metode teks vectorized?", ["str", "txt", "text", "chr"], 0, "Str.", hint="str."),
        Q("Atribut bagian tanggal?", ["dt", "date", "time", "cal"], 0, "Dt.", hint="dt."),
        Q("dayofweek untuk Senin?", ["0", "1", "6", "7"], 0, "Mulai nol.", hint="Nol."),
        Q("errors coerce menghasilkan?", ["NaT untuk yang gagal", "Galat", "Nol", "Hari ini"], 0, "Nilai hilang.", hint="NaT."),
        Q("Selisih dua tanggal bertipe?", ["Timedelta", "Integer", "String", "Boolean"], 0, "Selisih waktu.", hint="Delta."),
    ],
    [
        "Atribut str mengolah teks dan str.extract mengambil bagian dengan regex.",
        "to_datetime mengubah teks menjadi tanggal dan atribut dt mengambil bagiannya.",
        "Selisih tanggal menghasilkan timedelta dengan dt.days.",
        "Tetapkan tanggal acuan eksplisit agar analisis dapat diulang.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perintah yang cukup jelas dalam teks.", "brief": []}

write_module(
    "B2",
    4,
    "Kolom turunan, map, dan apply",
    105,
    [
        "Membuat kolom turunan dengan operasi vectorized dan pengelompokan",
        "Memakai map, replace, dan apply dengan sadar akan biayanya",
        "Mengolah teks dan tanggal dengan atribut str dan dt",
    ],
    [l1, l2, l3],
    video,
    REF,
)
