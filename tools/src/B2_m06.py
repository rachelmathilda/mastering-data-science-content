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
    'wilayah': ['Barat', 'Timur', 'Barat', 'Timur', 'Barat', 'Utara'],
    'produk': ['A', 'A', 'B', 'B', 'A', 'B'],
    'qty': [10, 5, 8, 12, 6, 4],
    'harga': [100, 100, 200, 200, 100, 200],
})
df['omzet'] = df['qty'] * df['harga']
"""


def tb(h, b):
    return T("## " + h + "\n\n" + b)


def ind(s):
    return textwrap.indent(s.strip("\n"), "            ")


def P(body):
    return ind(DFX + "\n" + textwrap.dedent(body).strip("\n"))


def X(c):
    return textwrap.dedent(c).strip("\n")


F11 = """
import pandas as pd

def total_per_wilayah(df):
    return df.groupby('wilayah')['qty'].sum().to_dict()
"""
F12 = """
import pandas as pd

def rata_omzet(df):
    return df.groupby('wilayah')['omzet'].mean().round(2).to_dict()
"""
F13 = """
import pandas as pd

def jumlah_baris(df, kolom):
    return df.groupby(kolom).size().to_dict()
"""
F14 = """
import pandas as pd

def wilayah_terbesar(df):
    return df.groupby('wilayah')['qty'].sum().idxmax()
"""

l1 = lesson(
    "B2-06-1",
    "Dasar groupby",
    35,
    [
        "Memahami pola pisah, terapkan, gabung",
        "Mengelompokkan dengan groupby dan satu agregasi",
        "Memakai size, count, dan beberapa fungsi agregasi",
        "Mengurutkan dan memilih hasil kelompok",
    ],
    [
        tb("Pertanyaan per kelompok", "Hampir setiap analisis bisnis bertanya per kelompok: total penjualan per wilayah, rata-rata nilai per kelas, jumlah pengguna per kota. Pandas menjawabnya dengan `groupby`. Prinsipnya pisah, terapkan, gabung: tabel dipecah menurut nilai kunci, fungsi diterapkan pada tiap potongan, dan hasilnya digabung menjadi satu tabel kecil. Menguasai groupby membuka sebagian besar analisis tabular."),
        tb("Data contoh", "Pelajaran ini memakai tabel enam transaksi dengan kolom `wilayah`, `produk`, `qty`, `harga`, dan `omzet` yang dihitung sebagai qty dikali harga. Wilayah Barat memiliki tiga transaksi, Timur dua, dan Utara satu. Tabel sekecil ini memungkinkan Anda memeriksa tiap total dengan kalkulator dan memastikan Anda paham apa yang dilakukan groupby sebelum memakainya pada jutaan baris."),
        C(
            P("""
g = df.groupby('wilayah')
print(g['qty'].sum().to_dict())
print(g['qty'].mean().round(2).to_dict())
print(g['qty'].max().to_dict())
print(g['omzet'].sum().to_dict())
print(g.size().to_dict())
print(g['qty'].count().to_dict())
"""),
            ind("""
{'Barat': 24, 'Timur': 17, 'Utara': 4}
{'Barat': 8.0, 'Timur': 8.5, 'Utara': 4.0}
{'Barat': 10, 'Timur': 12, 'Utara': 4}
{'Barat': 3200, 'Timur': 2900, 'Utara': 800}
{'Barat': 3, 'Timur': 2, 'Utara': 1}
{'Barat': 3, 'Timur': 2, 'Utara': 1}
"""),
            "Groupby diikuti pemilihan kolom dan fungsi agregasi menghasilkan satu nilai per kelompok.",
            filename="groupby_dasar.py",
        ),
        tb("Anatomi satu perintah", "Perintah `df.groupby('wilayah')['qty'].sum()` terdiri dari tiga bagian: kunci pengelompokan, kolom yang dihitung, dan fungsi agregasi. Hasilnya Series dengan nilai kunci sebagai indeks. Objek `groupby` sendiri malas: ia belum menghitung apa pun sampai Anda memanggil agregasi. Karena itu Anda dapat menyimpannya dalam variabel dan memakainya berulang kali."),
        tb("size dan count", "Metode `size()` menghitung jumlah baris per kelompok, termasuk baris dengan nilai hilang, sedangkan `count()` menghitung nilai tidak hilang pada kolom tertentu. Pada data bersih keduanya sama, tetapi pada data dengan NaN keduanya berbeda. Pilih `size` untuk pertanyaan berapa transaksi dan `count` untuk pertanyaan berapa nilai yang terisi."),
        tb("Fungsi agregasi umum", "Fungsi agregasi yang sering dipakai meliputi `sum`, `mean`, `median`, `min`, `max`, `std`, `var`, `count`, `nunique`, `first`, dan `last`. Semuanya melewati nilai hilang secara bawaan. Anda juga dapat memberi beberapa fungsi sekaligus lewat `agg(['sum', 'mean', 'max'])` yang menghasilkan satu kolom per fungsi, sehingga satu perintah menggantikan banyak perintah terpisah."),
        C(
            P("""
g = df.groupby('wilayah')
print(g['qty'].agg(['sum', 'mean', 'max']).values.tolist())
print(g['qty'].median().to_dict())
print(g['qty'].std().round(2).to_dict())
print(g['qty'].nunique().to_dict())
print(g['qty'].first().to_dict())
print(df.groupby('produk')['omzet'].sum().to_dict(), df['omzet'].sum())
"""),
            ind("""
[[24.0, 8.0, 10.0], [17.0, 8.5, 12.0], [4.0, 4.0, 4.0]]
{'Barat': 8.0, 'Timur': 8.5, 'Utara': 4.0}
{'Barat': 2.0, 'Timur': 4.95, 'Utara': nan}
{'Barat': 3, 'Timur': 2, 'Utara': 1}
{'Barat': 10, 'Timur': 5, 'Utara': 4}
{'A': 2100, 'B': 4800} 6900
"""),
            "Agg dengan list menghitung beberapa fungsi. Simpangan baku kelompok satu baris adalah NaN.",
            filename="groupby_agg_list.py",
        ),
        tb("Kelompok satu anggota", "Simpangan baku dan varians memerlukan sekurang-kurangnya dua nilai. Kelompok berisi satu baris menghasilkan NaN, seperti wilayah Utara di atas. Ini bukan galat, tetapi tanda bahwa kelompok terlalu kecil untuk statistik yang bermakna. Selalu periksa ukuran kelompok dengan `size()` sebelum menafsirkan rata-rata atau simpangan baku dari kelompok yang sangat kecil."),
        tb("Mengurutkan hasil", "Hasil groupby diurutkan menurut kunci secara bawaan. Untuk peringkat, urutkan menurut nilai dengan `sort_values(ascending=False)`. Metode `nlargest(n)` dan `nsmallest(n)` mengambil n teratas atau terbawah langsung, dan `idxmax` memberi kunci dengan nilai terbesar. Peringkat adalah pertanyaan paling umum setelah agregasi, jadi rangkaian groupby, sum, dan sort perlu terasa otomatis."),
        C(
            P("""
t = df.groupby('wilayah')['qty'].sum()
print(t.sort_values(ascending=False).index.tolist())
print(t.idxmax(), t.max())
print(t.nlargest(2).to_dict())
print(df.groupby('wilayah', as_index=False)['qty'].sum().values.tolist())
print(t.reset_index().columns.tolist())
print([(k, len(v)) for k, v in df.groupby('wilayah')])
"""),
            ind("""
['Barat', 'Timur', 'Utara']
Barat 24
{'Barat': 24, 'Timur': 17}
[['Barat', 24], ['Timur', 17], ['Utara', 4]]
['wilayah', 'qty']
[('Barat', 3), ('Timur', 2), ('Utara', 1)]
"""),
            "Sort, idxmax, dan nlargest membuat peringkat. As_index False dan reset_index mengembalikan kunci sebagai kolom. Perulangan atas groupby menghasilkan pasangan kunci dan potongan tabel.",
            filename="groupby_urut.py",
        ),
        tb("Kunci sebagai kolom", "Secara bawaan kunci pengelompokan menjadi indeks hasil. Pakai `as_index=False` atau `reset_index()` agar kunci menjadi kolom biasa, bentuk yang lebih mudah digabung dengan tabel lain, disimpan ke CSV, atau digambar. Bila Anda sering menulis `reset_index` di akhir, pertimbangkan `as_index=False` di awal agar kode lebih ringkas."),
        tb("Persentase dari total", "Pertanyaan umum: berapa persen tiap kelompok dari total. Bagi hasil agregasi dengan jumlah seluruhnya lalu kalikan seratus, misalnya `t / t.sum() * 100`. Pada contoh, omzet Barat 3200 dari total 6900 adalah 46,4 persen. Pembulatan sebaiknya dilakukan di akhir, hanya untuk tampilan, agar tidak menumpuk galat pembulatan dalam hitungan lanjutan."),
        tb("Kelompok dengan NaN", "Baris yang kuncinya NaN dibuang secara bawaan dari groupby. Pada data nyata ini dapat menghilangkan sebagian baris tanpa peringatan. Gunakan `dropna=False` untuk memasukkan NaN sebagai kelompok sendiri. Periksa total hasil agregasi terhadap total tabel asal: bila berbeda, kemungkinan ada baris yang kuncinya hilang dan terbuang diam-diam."),
        K("tip", "Bandingkan jumlah hasil groupby dengan jumlah tabel asal. Selisih menandakan baris dengan kunci NaN yang terbuang.", title="Rekonsiliasi"),
        tb("Memeriksa hasil dengan tangan", "Sebelum mempercayai groupby pada data besar, hitung satu kelompok dengan tangan pada contoh kecil. Wilayah Barat memiliki qty sepuluh, delapan, dan enam yang berjumlah dua puluh empat dan berata-rata delapan. Bila angka tangan sama dengan hasil pandas, Anda yakin memahami perintahnya. Kebiasaan ini mencegah kesalahan seperti salah memilih kolom atau salah memakai fungsi agregasi yang baru terlihat ketika laporan sudah dibaca banyak orang."),
        E(
            "B2-06-1-ex1",
            "mudah",
            "Tulis fungsi `total_per_wilayah(df)` yang mengembalikan dict jumlah `qty` per `wilayah`.",
            ind("""
import pandas as pd

def total_per_wilayah(df):
    # TODO: implementasikan
    pass
"""),
            P("""
assert total_per_wilayah(df) == {'Barat': 24, 'Timur': 17, 'Utara': 4}
assert total_per_wilayah(df.iloc[:2]) == {'Barat': 10, 'Timur': 5}
assert sum(total_per_wilayah(df).values()) == int(df['qty'].sum())
assert total_per_wilayah(df.iloc[[5]]) == {'Utara': 4}
"""),
            "groupby wilayah lalu sum pada qty.",
            X(F11),
        ),
        E(
            "B2-06-1-ex2",
            "sedang",
            "Tulis fungsi `rata_omzet(df)` yang mengembalikan dict rata-rata `omzet` per `wilayah`, dibulatkan dua desimal.",
            ind("""
import pandas as pd

def rata_omzet(df):
    # TODO: implementasikan
    pass
"""),
            P("""
assert rata_omzet(df) == {'Barat': 1066.67, 'Timur': 1450.0, 'Utara': 800.0}
assert rata_omzet(df.iloc[:2]) == {'Barat': 1000.0, 'Timur': 500.0}
assert rata_omzet(df.iloc[[2, 4]]) == {'Barat': 1100.0}
assert len(rata_omzet(df)) == 3
"""),
            "groupby wilayah, mean pada omzet, lalu round.",
            X(F12),
        ),
        E(
            "B2-06-1-ex3",
            "sedang",
            "Tulis fungsi `jumlah_baris(df, kolom)` yang mengembalikan dict banyaknya baris per nilai pada kolom yang diberikan.",
            ind("""
import pandas as pd

def jumlah_baris(df, kolom):
    # TODO: implementasikan
    pass
"""),
            P("""
assert jumlah_baris(df, 'wilayah') == {'Barat': 3, 'Timur': 2, 'Utara': 1}
assert jumlah_baris(df, 'produk') == {'A': 3, 'B': 3}
assert jumlah_baris(df.iloc[:1], 'produk') == {'A': 1}
assert sum(jumlah_baris(df, 'harga').values()) == 6
"""),
            "groupby kolom lalu size.",
            X(F13),
        ),
        E(
            "B2-06-1-ex4",
            "menantang",
            "Tulis fungsi `wilayah_terbesar(df)` yang mengembalikan nama wilayah dengan jumlah `qty` terbesar.",
            ind("""
import pandas as pd

def wilayah_terbesar(df):
    # TODO: implementasikan
    pass
"""),
            P("""
assert wilayah_terbesar(df) == 'Barat'
assert wilayah_terbesar(df.iloc[[1, 3, 5]]) == 'Timur'
assert wilayah_terbesar(df.iloc[[5]]) == 'Utara'
assert wilayah_terbesar(df[df['produk'] == 'B']) == 'Timur'
"""),
            "Jumlahkan qty per wilayah lalu idxmax.",
            X(F14),
        ),
    ],
    [
        M("Menghitung per kelompok dengan perulangan manual.", "Pakai groupby dengan agregasi."),
        M("Menafsirkan simpangan baku kelompok satu baris.", "Periksa ukuran kelompok dengan size."),
        M("Lupa baris dengan kunci NaN terbuang.", "Bandingkan total atau pakai dropna False."),
    ],
    [
        Q("Pola groupby?", ["Pisah, terapkan, gabung", "Urut, potong, tempel", "Baca, tulis, simpan", "Ubah, hapus, isi"], 0, "Split apply combine.", hint="Pisah."),
        Q("size menghitung?", ["Baris per kelompok", "Kolom", "Nilai unik", "Rata-rata"], 0, "Baris.", hint="Baris."),
        Q("Kelompok satu baris std?", ["NaN", "0", "1", "Galat"], 0, "Butuh dua nilai.", hint="NaN."),
        Q("Kunci jadi kolom dengan?", ["as_index False", "sort", "drop", "cut"], 0, "Reset.", hint="as_index."),
        Q("Nilai terbesar kunci dengan?", ["idxmax", "argsort", "rank", "cut"], 0, "Indeks maksimum.", hint="idxmax."),
    ],
    [
        "Groupby memisahkan, menerapkan fungsi, dan menggabung hasil.",
        "Pilih kolom dan fungsi agregasi setelah groupby.",
        "size menghitung baris dan count menghitung nilai terisi.",
        "Urutkan dengan sort_values atau nlargest untuk peringkat.",
    ],
    [],
)

G11 = """
import pandas as pd

def ringkas_wilayah(df):
    return df.groupby('wilayah').agg(total=('qty', 'sum'), maks=('qty', 'max')).values.tolist()
"""
G12 = """
import pandas as pd

def tabel_silang(df):
    return df.groupby(['wilayah', 'produk'])['qty'].sum().unstack(fill_value=0).values.tolist()
"""
G13 = """
import pandas as pd

def total_kunci_ganda(df):
    s = df.groupby(['wilayah', 'produk'])['qty'].sum()
    return {w + '-' + p: int(v) for (w, p), v in s.items()}
"""
G14 = """
import pandas as pd

def n_teratas(df, n):
    return df.groupby('wilayah')['omzet'].sum().nlargest(n).index.tolist()
"""

l2 = lesson(
    "B2-06-2",
    "Agregasi bernama dan banyak kunci",
    35,
    [
        "Memberi nama pada kolom hasil dengan named aggregation",
        "Mengelompokkan dengan dua kunci atau lebih",
        "Mengubah hasil bertingkat dengan unstack",
        "Memakai fungsi agregasi buatan sendiri",
    ],
    [
        tb("Lebih dari satu ringkasan", "Laporan nyata jarang meminta satu angka. Biasanya kita ingin total, rata-rata, dan maksimum sekaligus, dengan nama kolom yang jelas. Named aggregation menjawabnya: `agg(nama_baru=('kolom', 'fungsi'))`. Setiap argumen bernama menjadi satu kolom hasil, sehingga tabel keluaran siap dibaca atau disimpan tanpa mengganti nama kolom lagi."),
        C(
            P("""
r = df.groupby('wilayah').agg(total=('qty', 'sum'), rata=('omzet', 'mean'))
print(r.columns.tolist())
print(r.values.tolist())
print(r.index.tolist())
r2 = df.groupby('produk').agg(n=('qty', 'size'), maks=('qty', 'max'), omzet=('omzet', 'sum'))
print(r2.values.tolist())
print(r2.columns.tolist())
"""),
            ind("""
['total', 'rata']
[[24.0, 1066.6666666666667], [17.0, 1450.0], [4.0, 800.0]]
['Barat', 'Timur', 'Utara']
[[3, 10, 2100], [3, 12, 4800]]
['n', 'maks', 'omzet']
"""),
            "Named aggregation memberi nama kolom hasil secara langsung.",
            filename="agg_bernama.py",
        ),
        tb("Fungsi dan lambda", "Fungsi agregasi dapat berupa teks seperti `'sum'`, fungsi pustaka seperti `np.sum`, atau fungsi buatan sendiri yang menerima Series kelompok dan mengembalikan satu nilai. Misalnya rentang nilai, `lambda s: s.max() - s.min()`. Fungsi bawaan dengan nama teks lebih cepat karena dioptimalkan, jadi pakai fungsi buatan sendiri hanya bila tidak ada padanan bawaan."),
        C(
            P("""
print(df.groupby('wilayah')['qty'].apply(lambda s: s.max() - s.min()).to_dict())
print(df.groupby('produk')['qty'].agg(lambda s: s.sum() / len(s)).to_dict())
print(df.groupby('wilayah').agg(rentang=('qty', lambda s: s.max() - s.min()))['rentang'].to_dict())
print(df.groupby('wilayah')['harga'].agg(lambda s: s.mode()[0]).to_dict())
"""),
            ind("""
{'Barat': 4, 'Timur': 7, 'Utara': 0}
{'A': 7.0, 'B': 8.0}
{'Barat': 4, 'Timur': 7, 'Utara': 0}
{'Barat': 100, 'Timur': 100, 'Utara': 200}
"""),
            "Fungsi buatan sendiri menerima Series kelompok. Lambda dapat dipakai lewat apply atau agg.",
            filename="agg_kustom.py",
        ),
        tb("Dua kunci", "Memberi list ke groupby mengelompokkan menurut kombinasi kunci, misalnya wilayah dan produk. Hasilnya Series dengan indeks bertingkat, satu tingkat per kunci. Ini cocok untuk pertanyaan seperti penjualan tiap produk di tiap wilayah. Kombinasi yang tidak ada di data, seperti produk A di Utara, tidak muncul sama sekali dalam hasil bawaan."),
        tb("Indeks bertingkat", "Indeks bertingkat tampak rumit tetapi sebenarnya hanya tuple kunci. Anda dapat mengambil satu tingkat dengan `.loc['Barat']`, atau mengulang pasangan lewat `items()`. Metode `reset_index()` meratakannya menjadi kolom biasa. Untuk laporan, bentuk lebar yang dibuat dengan `unstack` biasanya lebih mudah dibaca daripada bentuk panjang bertingkat."),
        C(
            P("""
s = df.groupby(['wilayah', 'produk'])['qty'].sum()
print({w + '-' + p: int(v) for (w, p), v in s.items()})
print(s.loc['Barat'].to_dict())
w = s.unstack(fill_value=0)
print(w.values.tolist())
print(w.columns.tolist(), w.index.tolist())
print(w.sum(axis=1).to_dict())
print(pd.pivot_table(df, index='wilayah', columns='produk', values='qty', aggfunc='sum', fill_value=0).values.tolist())
"""),
            ind("""
{'Barat-A': 16, 'Barat-B': 8, 'Timur-A': 5, 'Timur-B': 12, 'Utara-B': 4}
{'A': 16, 'B': 8}
[[16, 8], [5, 12], [0, 4]]
['A', 'B'] ['Barat', 'Timur', 'Utara']
{'Barat': 24, 'Timur': 17, 'Utara': 4}
[[16, 8], [5, 12], [0, 4]]
"""),
            "Unstack memutar satu tingkat indeks menjadi kolom. Pivot_table memberi hasil sama dalam satu perintah.",
            filename="dua_kunci.py",
        ),
        tb("unstack dan fill_value", "Metode `unstack` memutar tingkat terdalam indeks menjadi kolom, menghasilkan tabel silang. Kombinasi yang tidak ada diisi NaN, dan `fill_value=0` menggantinya dengan nol sehingga tipe tetap bilangan bulat. Bentuk ini ideal untuk peta panas dan laporan. Pembahasan lebih lanjut tentang pivot ada di modul reshape nanti."),
        tb("Peringkat teratas", "Rangkaian groupby, sum, dan nlargest menjawab pertanyaan n teratas. Untuk n teratas di dalam tiap kelompok, gunakan `sort_values` lalu `groupby(...).head(n)`. Dua pola ini mencakup sebagian besar kebutuhan peringkat. Periksa perilaku saat nilai seri: `nlargest` secara bawaan mempertahankan yang pertama muncul, yang dapat diatur lewat argumen `keep`."),
        tb("Pitfall urutan kolom", "Pada named aggregation urutan kolom hasil mengikuti urutan argumen, bukan urutan abjad. Saat menyimpan ke CSV atau menyerahkan ke pihak lain, urutan itu membentuk kontrak. Tulis urutan secara sengaja dan hindari bergantung pada urutan bawaan, karena perubahan kecil pada kode agregasi dapat menggeser kolom diam-diam dan merusak konsumen laporan."),
        K("tip", "Pakai named aggregation agar kolom hasil bernama jelas dan urutannya sengaja.", title="Nama jelas"),
        tb("Banyak kolom sekaligus", "Named aggregation dapat mengagregasi kolom berbeda dengan fungsi berbeda dalam satu perintah, misalnya jumlah qty, rata-rata harga, dan jumlah unik produk. Ini menggantikan beberapa groupby terpisah yang kemudian harus digabung. Hasilnya satu tabel rapi, dihitung dalam satu lintasan data, sehingga lebih cepat dan lebih mudah dirawat daripada rangkaian perintah yang tersebar."),
        tb("Memeriksa kelompok kosong", "Dengan dua kunci, ada kombinasi yang tidak terjadi dalam data, seperti produk A di wilayah Utara. Dalam laporan, ketiadaan ini sering perlu ditampilkan sebagai nol, bukan dihilangkan, karena pembaca mungkin mengira data hilang. Gunakan unstack dengan fill_value nol, atau reindex dengan produk lengkap, agar semua kombinasi muncul secara eksplisit dan konsisten di setiap periode laporan."),
        tb("Menamai hasil untuk pembaca", "Nama kolom hasil adalah antarmuka bagi pembaca laporan. Nama seperti total_qty dan rata_omzet lebih jelas daripada sum dan mean. Hindari singkatan yang hanya Anda pahami, dan konsisten memakai satuan dalam nama bila relevan, misalnya omzet_rupiah. Nama baik mengurangi pertanyaan ulang dan kesalahan tafsir ketika tabel berpindah dari notebook ke presentasi atau dasbor orang lain."),
        tb("Agregasi dan penyaringan bersama", "Sering kita ingin agregasi hanya pada sebagian baris, misalnya total omzet produk B saja. Saring tabel lebih dulu dengan syarat boolean, lalu panggil groupby pada hasil saringan. Urutan ini lebih jelas daripada menaruh syarat di dalam fungsi agregasi. Bila Anda perlu membandingkan beberapa saringan, hitung masing-masing terpisah dengan nama yang menjelaskan isinya agar hasil mudah ditinjau dan diuji ulang oleh rekan kerja."),
        tb("Menggabung hasil agregasi", "Hasil dua agregasi dengan kunci sama dapat digabung dengan `pd.concat(axis=1)` atau `join`, karena keduanya berindeks kunci. Namun bila kedua ringkasan dapat dihitung dalam satu perintah agg, lakukan itu agar hanya satu lintasan data. Gabung hanya bila ringkasan berasal dari saringan atau tabel yang berbeda, dan periksa bahwa kunci yang tidak ada di salah satu sisi ditangani dengan sengaja."),
        E(
            "B2-06-2-ex1",
            "mudah",
            "Tulis fungsi `ringkas_wilayah(df)` yang memakai named aggregation untuk kolom `total` (jumlah qty) dan `maks` (qty terbesar) per wilayah, dan mengembalikan `values.tolist()`.",
            ind("""
import pandas as pd

def ringkas_wilayah(df):
    # TODO: implementasikan
    pass
"""),
            P("""
assert ringkas_wilayah(df) == [[24, 10], [17, 12], [4, 4]]
assert ringkas_wilayah(df.iloc[:2]) == [[10, 10], [5, 5]]
assert ringkas_wilayah(df.iloc[[5]]) == [[4, 4]]
assert len(ringkas_wilayah(df)) == 3
"""),
            "groupby wilayah lalu agg dengan dua argumen bernama.",
            X(G11),
        ),
        E(
            "B2-06-2-ex2",
            "sedang",
            "Tulis fungsi `tabel_silang(df)` yang menjumlahkan `qty` per `wilayah` (baris) dan `produk` (kolom), mengisi kombinasi kosong dengan nol, dan mengembalikan `values.tolist()`.",
            ind("""
import pandas as pd

def tabel_silang(df):
    # TODO: implementasikan
    pass
"""),
            P("""
assert tabel_silang(df) == [[16, 8], [5, 12], [0, 4]]
assert tabel_silang(df[df['produk'] == 'A']) == [[16], [5]]
assert tabel_silang(df.iloc[[0, 2]]) == [[10, 8]]
assert sum(sum(r) for r in tabel_silang(df)) == 45
"""),
            "groupby dua kunci, sum, lalu unstack dengan fill_value nol.",
            X(G12),
        ),
        E(
            "B2-06-2-ex3",
            "sedang",
            "Tulis fungsi `total_kunci_ganda(df)` yang mengembalikan dict jumlah `qty` per pasangan, dengan kunci berupa teks `wilayah-produk` (misalnya `Barat-A`).",
            ind("""
import pandas as pd

def total_kunci_ganda(df):
    # TODO: implementasikan
    pass
"""),
            P("""
assert total_kunci_ganda(df) == {'Barat-A': 16, 'Barat-B': 8, 'Timur-A': 5, 'Timur-B': 12, 'Utara-B': 4}
assert total_kunci_ganda(df.iloc[:1]) == {'Barat-A': 10}
assert 'Utara-A' not in total_kunci_ganda(df)
assert sum(total_kunci_ganda(df).values()) == 45
"""),
            "groupby dua kunci lalu bangun dict dari items.",
            X(G13),
        ),
        E(
            "B2-06-2-ex4",
            "menantang",
            "Tulis fungsi `n_teratas(df, n)` yang mengembalikan list `n` wilayah dengan jumlah `omzet` terbesar, dari yang terbesar.",
            ind("""
import pandas as pd

def n_teratas(df, n):
    # TODO: implementasikan
    pass
"""),
            P("""
assert n_teratas(df, 2) == ['Barat', 'Timur']
assert n_teratas(df, 1) == ['Barat']
assert n_teratas(df, 3) == ['Barat', 'Timur', 'Utara']
assert n_teratas(df.iloc[[0, 1]], 1) == ['Barat']
"""),
            "Jumlahkan omzet per wilayah lalu nlargest dan ambil indeksnya.",
            X(G14),
        ),
    ],
    [
        M("Mengganti nama kolom hasil sesudah agregasi.", "Pakai named aggregation sejak awal."),
        M("Memakai lambda padahal ada fungsi bawaan.", "Pakai nama teks seperti sum agar cepat."),
        M("Bingung dengan indeks bertingkat.", "Pakai reset_index atau unstack."),
    ],
    [
        Q("Named aggregation ditulis?", ["nama=('kolom','fungsi')", "kolom:fungsi", "fungsi(kolom)", "kolom->fungsi"], 0, "Tuple.", hint="Argumen bernama."),
        Q("groupby dua kunci memberi?", ["Indeks bertingkat", "Dua tabel", "Galat", "Satu kolom"], 0, "MultiIndex.", hint="Bertingkat."),
        Q("unstack?", ["Memutar indeks ke kolom", "Mengurutkan", "Menghapus", "Menggabung"], 0, "Lebar.", hint="Kolom."),
        Q("fill_value=0 pada unstack mengisi?", ["Kombinasi kosong", "Semua", "Indeks", "Nama"], 0, "NaN jadi nol.", hint="Kosong."),
        Q("Fungsi agregasi buatan menerima?", ["Series kelompok", "Satu angka", "Tabel penuh", "Indeks"], 0, "Per kelompok.", hint="Series."),
    ],
    [
        "Named aggregation membuat kolom hasil bernama jelas.",
        "Dua kunci menghasilkan indeks bertingkat.",
        "unstack dan pivot_table membentuk tabel silang.",
        "Fungsi bawaan lebih cepat dari lambda.",
    ],
    [],
)

H11 = """
import pandas as pd

def persen_wilayah(df):
    return (df['qty'] / df.groupby('wilayah')['qty'].transform('sum')).round(3).tolist()
"""
H12 = """
import pandas as pd

def kumulatif_wilayah(df):
    return df.groupby('wilayah')['qty'].cumsum().tolist()
"""
H13 = """
import pandas as pd

def wilayah_besar(df, batas):
    return df.groupby('wilayah').filter(lambda x: x['qty'].sum() > batas)['qty'].tolist()
"""
H14 = """
import pandas as pd

def peringkat_dalam(df):
    return df.groupby('wilayah')['qty'].rank(ascending=False).tolist()
"""

l3 = lesson(
    "B2-06-3",
    "transform, filter, dan peringkat",
    35,
    [
        "Menambah statistik kelompok ke tiap baris dengan transform",
        "Menghitung kumulatif dan peringkat dalam kelompok",
        "Menyaring seluruh kelompok dengan filter",
        "Membedakan agg, transform, dan apply",
    ],
    [
        tb("Agregasi yang mempertahankan baris", "Agregasi biasa mengecilkan tabel menjadi satu baris per kelompok. Kadang kita ingin statistik kelompok tetap menempel pada tiap baris asal, misalnya porsi tiap transaksi terhadap total wilayahnya. Itu pekerjaan `transform`: ia menghitung fungsi per kelompok lalu mengembalikan hasil dengan panjang dan indeks yang sama seperti tabel asal."),
        C(
            P("""
t = df.groupby('wilayah')['qty'].transform('sum')
print(t.tolist())
print((df['qty'] / t).round(3).tolist())
print(df.groupby('wilayah')['qty'].transform('mean').tolist())
print(df.groupby('wilayah')['qty'].cumsum().tolist())
print(df.groupby('wilayah')['qty'].rank(ascending=False).tolist())
print(len(t) == len(df))
"""),
            ind("""
[24, 17, 24, 17, 24, 4]
[0.417, 0.294, 0.333, 0.706, 0.25, 1.0]
[8.0, 8.5, 8.0, 8.5, 8.0, 4.0]
[10, 5, 18, 17, 24, 4]
[1.0, 2.0, 2.0, 1.0, 3.0, 1.0]
True
"""),
            "Transform mengembalikan Series sepanjang tabel. Cumsum dan rank juga bekerja per kelompok.",
            filename="transform.py",
        ),
        tb("Porsi dalam kelompok", "Porsi tiap baris terhadap total kelompoknya dihitung dengan membagi kolom dengan hasil `transform('sum')`. Pola ini muncul di mana-mana: persen penjualan produk dalam kategorinya, kontribusi tiap siswa terhadap nilai kelas, atau selisih terhadap rata-rata kelompok. Karena hasilnya sejajar dengan tabel, ia dapat langsung ditugaskan sebagai kolom baru."),
        tb("Kumulatif dan peringkat", "Fungsi `cumsum`, `cummax`, `rank`, `shift`, dan `diff` bekerja dalam kelompok bila dipanggil setelah groupby, sehingga perhitungan tidak melintasi batas kelompok. `rank(ascending=False)` memberi peringkat satu pada nilai terbesar. Nilai seri mendapat peringkat rata-rata secara bawaan, dan argumen `method='min'` atau `'first'` mengubah perlakuan seri."),
        tb("Memilih baris teratas per kelompok", "Untuk mengambil n baris teratas dalam tiap kelompok, urutkan tabel lebih dulu lalu panggil `groupby('kunci').head(n)`. Alternatifnya, hitung peringkat dengan rank dan saring peringkat sekurang-kurangnya n. Pola ini menjawab pertanyaan seperti transaksi terbesar tiap wilayah atau tiga produk terlaris tiap kategori."),
        C(
            P("""
print(df.groupby('wilayah').filter(lambda x: x['qty'].sum() > 10)['qty'].tolist())
print(df.groupby('wilayah').filter(lambda x: len(x) >= 2)['wilayah'].tolist())
top = df.sort_values('qty', ascending=False).groupby('wilayah').head(1)
print(top.sort_index()['qty'].tolist())
print(df.groupby('wilayah')['qty'].first().to_dict())
print(df.groupby('wilayah')['qty'].last().to_dict())
"""),
            ind("""
[10, 5, 8, 12, 6]
['Barat', 'Timur', 'Barat', 'Timur', 'Barat']
[10, 12, 4]
{'Barat': 10, 'Timur': 5, 'Utara': 4}
{'Barat': 6, 'Timur': 12, 'Utara': 4}
"""),
            "Filter menyaring seluruh kelompok. Head setelah sort memilih baris teratas per kelompok.",
            filename="filter_head.py",
        ),
        tb("filter menyaring kelompok", "Metode `filter(fungsi)` membuang seluruh kelompok yang fungsinya mengembalikan False, dan mempertahankan baris asli kelompok yang lolos. Berbeda dari filter boolean biasa yang bekerja per baris, ini bekerja per kelompok, misalnya hanya wilayah dengan total lebih dari sepuluh. Hasilnya tetap berbentuk baris asli, bukan ringkasan."),
        tb("agg, transform, atau apply", "Ringkasnya: `agg` mengecilkan setiap kelompok menjadi satu nilai, `transform` mengembalikan satu nilai per baris asal, dan `apply` menerima fungsi yang bebas mengembalikan apa saja. Pilih yang paling sempit yang menyelesaikan masalah, karena yang sempit lebih cepat, lebih mudah diprediksi bentuk hasilnya, dan lebih jelas niatnya bagi pembaca kode."),
        tb("Performa groupby", "Groupby dengan fungsi bawaan seperti sum dan mean sangat cepat karena berjalan dalam kode terkompilasi. Fungsi lambda dan apply memanggil Python per kelompok sehingga jauh lebih lambat pada ribuan kelompok. Bila banyak kelompok, cari padanan bawaan atau ekspresikan hitungan dengan operasi kolom sebelum atau sesudah groupby dibanding menulis fungsi per kelompok."),
        tb("Ringkasan modul", "Anda telah belajar groupby dengan agregasi dasar, named aggregation, banyak kunci dengan unstack, serta transform, filter, dan peringkat. Prinsipnya: pikirkan bentuk hasil yang diinginkan lebih dulu, lalu pilih agg, transform, atau filter yang cocok. Modul berikutnya membahas penggabungan tabel dengan merge, join, dan concat."),
        K("tip", "Pilih agg bila ingin satu baris per kelompok, transform bila ingin menempelkan statistik ke tiap baris.", title="Pilih bentuk hasil"),
        tb("shift dan diff dalam kelompok", "Fungsi `shift` menggeser nilai satu baris dalam tiap kelompok, dan `diff` menghitung selisih dengan baris sebelumnya. Keduanya menghasilkan NaN pada baris pertama setiap kelompok karena belum ada pendahulu. Ini berguna untuk mengukur perubahan antar transaksi berurutan dalam wilayah yang sama, asalkan data sudah diurutkan menurut waktu sebelum groupby dipanggil."),
        C(
            P("""
g = df.groupby('wilayah')['qty']
print(g.shift().tolist())
print(g.diff().tolist())
print(g.cummax().tolist())
print(g.transform('max').tolist())
print((df['qty'] == g.transform('max')).tolist())
"""),
            ind("""
[nan, nan, 10.0, 5.0, 8.0, nan]
[nan, nan, -2.0, 7.0, -2.0, nan]
[10, 5, 10, 12, 10, 4]
[10, 12, 10, 12, 10, 4]
[True, False, False, True, False, True]
"""),
            "Shift dan diff bekerja dalam kelompok. Membandingkan nilai dengan transform max menandai baris terbesar tiap kelompok.",
            filename="shift_diff.py",
        ),
        tb("Menandai baris terbesar", "Membandingkan kolom dengan `transform('max')` menghasilkan penanda boolean untuk baris terbesar dalam tiap kelompok. Pola ini lebih sederhana daripada mengurutkan lalu memilih, dan mempertahankan urutan baris asal. Hal yang sama berlaku untuk minimum, atau untuk baris yang di atas rata-rata kelompok, yang sering dipakai dalam analisis pencilan per kelompok."),
        tb("Urutan sebelum groupby", "Fungsi yang bergantung pada urutan seperti `first`, `last`, `shift`, `cumsum`, dan `diff` memakai urutan baris sebagaimana adanya. Bila data belum terurut menurut waktu, hasilnya salah tanpa peringatan. Urutkan dengan `sort_values` pada kolom waktu lebih dulu, lalu panggil groupby. Memeriksa urutan adalah langkah kecil yang menyelamatkan banyak analisis deret waktu per kelompok dari kesimpulan keliru."),
        tb("Contoh analisis lengkap", "Gabungkan semuanya pada satu pertanyaan: wilayah mana yang berkontribusi paling besar dan transaksi mana yang paling menentukan. Hitung total per wilayah dengan agg, porsi tiap transaksi dengan transform, lalu tandai transaksi terbesar tiap wilayah. Tiga langkah kecil yang masing-masing mudah diperiksa menghasilkan jawaban yang dapat dipertanggungjawabkan, jauh lebih baik daripada satu rumus panjang yang sulit diverifikasi."),
        E(
            "B2-06-3-ex1",
            "mudah",
            "Tulis fungsi `persen_wilayah(df)` yang mengembalikan list porsi `qty` tiap baris terhadap total `qty` wilayahnya, dibulatkan tiga desimal.",
            ind("""
import pandas as pd

def persen_wilayah(df):
    # TODO: implementasikan
    pass
"""),
            P("""
assert persen_wilayah(df) == [0.417, 0.294, 0.333, 0.706, 0.25, 1.0]
assert persen_wilayah(df.iloc[[5]]) == [1.0]
assert persen_wilayah(df.iloc[[0, 2]]) == [0.556, 0.444]
assert len(persen_wilayah(df)) == 6
"""),
            "Bagi qty dengan transform sum per wilayah.",
            X(H11),
        ),
        E(
            "B2-06-3-ex2",
            "sedang",
            "Tulis fungsi `kumulatif_wilayah(df)` yang mengembalikan list jumlah kumulatif `qty` dalam tiap `wilayah` mengikuti urutan baris.",
            ind("""
import pandas as pd

def kumulatif_wilayah(df):
    # TODO: implementasikan
    pass
"""),
            P("""
assert kumulatif_wilayah(df) == [10, 5, 18, 17, 24, 4]
assert kumulatif_wilayah(df.iloc[[0, 2]]) == [10, 18]
assert kumulatif_wilayah(df.iloc[[5]]) == [4]
assert kumulatif_wilayah(df)[-1] == 4
"""),
            "groupby wilayah lalu cumsum pada qty.",
            X(H12),
        ),
        E(
            "B2-06-3-ex3",
            "sedang",
            "Tulis fungsi `wilayah_besar(df, batas)` yang mengembalikan list `qty` dari baris-baris wilayah yang total `qty`-nya lebih dari `batas`.",
            ind("""
import pandas as pd

def wilayah_besar(df, batas):
    # TODO: implementasikan
    pass
"""),
            P("""
assert wilayah_besar(df, 10) == [10, 5, 8, 12, 6]
assert wilayah_besar(df, 20) == [10, 8, 6]
assert wilayah_besar(df, 100) == []
assert wilayah_besar(df, 0) == [10, 5, 8, 12, 6, 4]
"""),
            "groupby lalu filter dengan jumlah qty kelompok.",
            X(H13),
        ),
        E(
            "B2-06-3-ex4",
            "menantang",
            "Tulis fungsi `peringkat_dalam(df)` yang mengembalikan list peringkat `qty` dalam tiap wilayah, dengan peringkat 1 untuk `qty` terbesar.",
            ind("""
import pandas as pd

def peringkat_dalam(df):
    # TODO: implementasikan
    pass
"""),
            P("""
assert peringkat_dalam(df) == [1.0, 2.0, 2.0, 1.0, 3.0, 1.0]
assert peringkat_dalam(df.iloc[[0, 2, 4]]) == [1.0, 2.0, 3.0]
assert peringkat_dalam(df.iloc[[5]]) == [1.0]
assert max(peringkat_dalam(df)) == 3.0
"""),
            "groupby wilayah lalu rank menurun pada qty.",
            X(H14),
        ),
    ],
    [
        M("Memakai agg lalu bingung bentuk hasil mengecil.", "Pakai transform bila butuh sepanjang tabel."),
        M("Mengira filter bekerja per baris.", "Filter groupby bekerja per kelompok."),
        M("Memakai apply untuk hal yang punya padanan bawaan.", "Pakai agg, transform, atau cumsum."),
    ],
    [
        Q("transform mengembalikan?", ["Sepanjang tabel asal", "Satu per kelompok", "Dict", "Tabel kosong"], 0, "Sejajar.", hint="Panjang sama."),
        Q("agg mengembalikan?", ["Satu nilai per kelompok", "Per baris", "Galat", "Acak"], 0, "Ringkas.", hint="Per kelompok."),
        Q("filter groupby membuang?", ["Kelompok utuh", "Baris tunggal", "Kolom", "Indeks"], 0, "Per kelompok.", hint="Kelompok."),
        Q("rank ascending False untuk terbesar?", ["Peringkat 1", "Peringkat terakhir", "NaN", "0"], 0, "Menurun.", hint="Satu."),
        Q("Cumsum setelah groupby?", ["Dalam kelompok", "Melintasi kelompok", "Galat", "Acak"], 0, "Per kelompok.", hint="Dalam."),
    ],
    [
        "transform menempelkan statistik kelompok pada tiap baris.",
        "cumsum dan rank bekerja dalam kelompok setelah groupby.",
        "filter membuang seluruh kelompok yang tidak lolos syarat.",
        "Pilih agg, transform, atau apply yang paling sempit.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perintah yang cukup jelas dalam teks.", "brief": []}

write_module(
    "B2",
    6,
    "GroupBy dan agregasi",
    105,
    [
        "Mengelompokkan dan mengagregasi dengan groupby",
        "Memakai named aggregation, banyak kunci, dan unstack",
        "Memakai transform, filter, dan peringkat per kelompok",
    ],
    [l1, l2, l3],
    video,
    REF,
)
