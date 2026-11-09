import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

DFX = """
import pandas as pd

df = pd.DataFrame({
    'produk': ['Pena', 'Buku', 'Tas', 'Pena', 'Buku', 'Topi'],
    'wilayah': ['Jkt', 'Bdg', 'Jkt', 'Sby', 'Jkt', 'Bdg'],
    'qty': [10, 5, 3, 7, 8, 2],
    'harga': [3.0, 12.0, 50.0, 3.0, 12.0, 20.0],
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

def urut_qty_turun(df):
    return df.sort_values('qty', ascending=False).index.tolist()
"""
F2 = """
import pandas as pd

def urut_dua_kunci(df):
    return df.sort_values(['produk', 'qty'], ascending=[True, False]).index.tolist()
"""
F3 = """
import pandas as pd

def peringkat_qty(df):
    return df['qty'].rank(ascending=False, method='min').tolist()
"""
F4 = """
import pandas as pd

def top_n(df, kolom, n):
    return df.sort_values(kolom, ascending=False, kind='stable').head(n).index.tolist()
"""

l1 = lesson(
    "B2-03-1",
    "Mengurutkan data",
    35,
    [
        "Mengurutkan dengan sort_values pada satu dan banyak kolom",
        "Mengatur arah urutan dan posisi nilai hilang",
        "Memakai nlargest, nsmallest, dan rank",
        "Menjaga urutan tetap deterministik pada nilai kembar",
    ],
    [
        tb("Mengapa mengurutkan", "Mengurutkan adalah salah satu operasi analisis paling sering: produk terlaris di atas, pelanggan terlama di bawah, kesalahan terbesar lebih dulu. Pandas menyediakan `sort_values` untuk mengurutkan menurut isi kolom dan `sort_index` untuk mengurutkan menurut label indeks. Keduanya mengembalikan tabel baru dan tidak mengubah yang asli, kecuali Anda meminta `inplace=True`, yang tidak disarankan."),
        tb("Data contoh", "Pelajaran ini memakai tabel penjualan kecil berisi enam baris: kolom `produk`, `wilayah`, `qty`, dan `harga`. Beberapa produk dan wilayah berulang, dan ada nilai kembar pada `harga` dan `produk`. Nilai kembar sengaja disertakan karena pengurutan dengan kembaran adalah sumber ketidakpastian hasil yang sering luput diperhatikan, dan akan dibahas pada akhir pelajaran."),
        C(
            P("""
print(df.sort_values('qty')['qty'].tolist())
print(df.sort_values('qty', ascending=False).index.tolist())
print(df.sort_values('qty').index.tolist())
print(df.index.tolist())
print(df.sort_values('qty').reset_index(drop=True).index.tolist())
"""),
            ind("""
[2, 3, 5, 7, 8, 10]
[0, 4, 3, 1, 2, 5]
[5, 2, 1, 3, 4, 0]
[0, 1, 2, 3, 4, 5]
[0, 1, 2, 3, 4, 5]
"""),
            "Urutan menurun memakai ascending bernilai False. Indeks ikut berpindah bersama barisnya, dan tabel asal tidak berubah.",
            filename="sort_dasar.py",
        ),
        tb("Banyak kunci", "Beri list nama kolom untuk mengurutkan menurut beberapa kunci: baris diurutkan menurut kunci pertama, dan baris dengan kunci pertama sama diurutkan menurut kunci kedua, dan seterusnya. Argumen `ascending` dapat berupa list bertipe bool yang sepanjang list kunci, sehingga tiap kunci punya arah berbeda. Misalnya nama produk menaik dan jumlah menurun dalam satu pengurutan."),
        C(
            P("""
print(df.sort_values(['produk', 'qty'], ascending=[True, False]).index.tolist())
print(df.sort_values(['harga', 'qty'], ascending=[False, True]).index.tolist())
print(df.sort_values(['wilayah', 'qty'], ascending=[True, False])[['wilayah', 'qty']].values.tolist())
"""),
            ind("""
[4, 1, 0, 3, 2, 5]
[2, 5, 1, 4, 3, 0]
[['Bdg', 5], ['Bdg', 2], ['Jkt', 10], ['Jkt', 8], ['Jkt', 3], ['Sby', 7]]
"""),
            "Dua buku diurutkan menurut qty menurun, dan dalam tiap wilayah qty juga menurun.",
            filename="sort_banyak.py",
        ),
        tb("Nilai hilang", "Secara bawaan nilai hilang ditempatkan di akhir, baik urutan menaik maupun menurun. Argumen `na_position='first'` memindahkannya ke awal. Ini penting karena nilai hilang diam-diam dapat muncul di bagian bawah tabel yang Anda kira telah lengkap. Pertimbangkan apakah baris bernilai hilang perlu ditampilkan, dibuang, atau diisi sebelum mengurutkan."),
        C(
            P("""
import numpy as np

d = df.copy()
d.loc[1, 'qty'] = np.nan
print(d.sort_values('qty').index.tolist())
print(d.sort_values('qty', na_position='first').index.tolist())
print(d.sort_values('qty', ascending=False).index.tolist())
"""),
            ind("""
[5, 2, 3, 4, 0, 1]
[1, 5, 2, 3, 4, 0]
[0, 4, 3, 2, 5, 1]
"""),
            "Nilai hilang berada di akhir pada kedua arah kecuali na_position diubah ke first.",
            filename="sort_na.py",
        ),
        tb("Urutan teks", "Pengurutan teks mengikuti urutan kode karakter, sehingga huruf besar mendahului huruf kecil: Zebra muncul sebelum apel. Untuk urutan tak peka huruf, beri argumen `key` berupa fungsi yang dipakai hanya untuk perbandingan, misalnya `key=lambda s: s.str.lower()`. Fungsi `key` menerima seluruh kolom sekaligus, bukan satu elemen, dan tidak mengubah isi data."),
        tb("nlargest dan nsmallest", "Bila Anda hanya butuh beberapa baris teratas, `nlargest(n, kolom)` dan `nsmallest(n, kolom)` lebih ringkas dan lebih cepat daripada mengurutkan seluruh tabel lalu mengambil `head`. Mereka menerima list kolom untuk pemecah kembar. Argumen `keep` mengatur perlakuan nilai kembar pada batas: `first`, `last`, atau `all` yang mempertahankan semua kembaran sehingga hasil dapat lebih dari n baris."),
        C(
            P("""
print(df.nlargest(3, 'qty').index.tolist())
print(df.nsmallest(2, ['harga', 'qty']).index.tolist())
print(df.nlargest(2, 'harga', keep='all').index.tolist())
print(df['qty'].nlargest(2).tolist())
"""),
            ind("""
[0, 4, 3]
[3, 0]
[2, 5]
[10, 8]
"""),
            "Nlargest mengambil baris teratas. Nsmallest dengan dua kolom memakai kolom kedua sebagai pemecah kembar.",
            filename="nlargest_dasar.py",
        ),
        tb("Peringkat", "Metode `rank` memberi peringkat tiap nilai tanpa mengubah urutan baris. Untuk nilai kembar tersedia beberapa metode: `average` memberi rata-rata peringkat, `min` memberi peringkat terendah untuk semua kembaran seperti dalam kompetisi olahraga, `dense` memberi peringkat berurutan tanpa lompatan, dan `first` memberi peringkat menurut urutan kemunculan. Pilih yang sesuai dengan makna laporan Anda."),
        C(
            P("""
print(df['qty'].rank(ascending=False).tolist())
print(df['harga'].rank(method='min').tolist())
print(df['harga'].rank(method='dense').tolist())
print(df['harga'].rank(method='first').tolist())
"""),
            ind("""
[1.0, 4.0, 5.0, 3.0, 2.0, 6.0]
[1.0, 3.0, 6.0, 1.0, 3.0, 5.0]
[1.0, 2.0, 4.0, 1.0, 2.0, 3.0]
[1.0, 3.0, 6.0, 2.0, 4.0, 5.0]
"""),
            "Metode min memberi peringkat satu untuk dua kembaran lalu melompat, sedangkan dense tidak melompat dan first memecah kembar menurut urutan baris.",
            filename="rank_metode.py",
        ),
        tb("Kembar dan determinisme", "Bila banyak baris memiliki nilai kunci sama, urutan relatif mereka dapat berbeda antar algoritma. Algoritma bawaan `quicksort` tidak stabil, sedangkan `kind='stable'` menjaga urutan asli baris kembar. Untuk hasil yang dapat diulang, gunakan pengurutan stabil, atau tambahkan kolom pemecah kembar yang unik seperti id. Hasil yang berubah antar run adalah musuh reproduksibilitas."),
        tb("Mengurutkan indeks", "Metode `sort_index` mengurutkan baris menurut label indeks, dan dengan `axis=1` mengurutkan kolom menurut namanya. Ia berguna setelah penggabungan atau `reindex` ketika urutan baris berantakan, dan sebelum slice label yang mengandalkan indeks terurut. Pada indeks tanggal, indeks terurut membuat banyak operasi deret waktu jauh lebih cepat."),
        tb("Urutan kustom", "Untuk urutan yang bukan abjad atau numerik, seperti Senin sampai Minggu atau kecil, sedang, besar, ubah kolom menjadi kategori berurutan dengan `pd.Categorical(kolom, categories=[...], ordered=True)`. Setelah itu `sort_values` dan perbandingan mengikuti urutan yang Anda tentukan. Teknik ini menghindari kolom bantu numerik dan membuat maksud urutan tersurat pada tipe datanya."),
        K("tip", "Untuk hasil yang dapat diulang saat ada nilai kembar, pakai kind='stable' atau tambahkan kolom pemecah kembar yang unik.", title="Urutan deterministik"),
        tb("Urutan menurut panjang atau fungsi", "Argumen `key` pada `sort_values` memungkinkan pengurutan menurut nilai turunan tanpa membuat kolom baru, misalnya menurut panjang teks dengan `key=lambda s: s.str.len()` atau menurut nilai mutlak dengan `key=abs`. Fungsi key menerima seluruh kolom sekaligus dan harus mengembalikan Series berpanjang sama. Cara ini menjaga tabel tetap ringkas saat urutan hanya dibutuhkan sesaat."),
        E(
            "B2-03-1-ex1",
            "mudah",
            "Tulis fungsi `urut_qty_turun(df)` yang mengembalikan list label indeks baris setelah tabel diurutkan menurut `qty` dari terbesar ke terkecil.",
            ind("""
import pandas as pd

def urut_qty_turun(df):
    # TODO: implementasikan
    pass
"""),
            P("""
assert urut_qty_turun(df) == [0, 4, 3, 1, 2, 5]
assert urut_qty_turun(df.iloc[:2]) == [0, 1]
assert urut_qty_turun(df.iloc[::-1]) == [0, 4, 3, 1, 2, 5]
assert df.index.tolist() == [0, 1, 2, 3, 4, 5]
"""),
            "sort_values dengan ascending bernilai False lalu index.",
            F1.strip("\n"),
        ),
        E(
            "B2-03-1-ex2",
            "sedang",
            "Tulis fungsi `urut_dua_kunci(df)` yang mengembalikan list label indeks setelah tabel diurutkan menurut `produk` menaik dan, untuk produk sama, `qty` menurun.",
            ind("""
import pandas as pd

def urut_dua_kunci(df):
    # TODO: implementasikan
    pass
"""),
            P("""
assert urut_dua_kunci(df) == [4, 1, 0, 3, 2, 5]
assert urut_dua_kunci(df.iloc[:4]) == [1, 0, 3, 2]
assert urut_dua_kunci(df.iloc[[2]]) == [2]
assert urut_dua_kunci(df.iloc[::-1]) == [4, 1, 0, 3, 2, 5]
"""),
            "sort_values dengan dua kolom dan ascending berupa list.",
            F2.strip("\n"),
        ),
        E(
            "B2-03-1-ex3",
            "sedang",
            "Tulis fungsi `peringkat_qty(df)` yang mengembalikan list peringkat tiap baris menurut `qty` dari terbesar, di mana nilai kembar mendapat peringkat terendah yang sama (metode `min`).",
            ind("""
import pandas as pd

def peringkat_qty(df):
    # TODO: implementasikan
    pass
"""),
            P("""
assert peringkat_qty(df) == [1.0, 4.0, 5.0, 3.0, 2.0, 6.0]
t = pd.DataFrame({'qty': [5, 9, 5, 1]})
assert peringkat_qty(t) == [2.0, 1.0, 2.0, 4.0]
assert peringkat_qty(pd.DataFrame({'qty': [7]})) == [1.0]
assert peringkat_qty(pd.DataFrame({'qty': [3, 3, 3]})) == [1.0, 1.0, 1.0]
"""),
            "rank dengan ascending False dan method min.",
            F3.strip("\n"),
        ),
        E(
            "B2-03-1-ex4",
            "menantang",
            "Tulis fungsi `top_n(df, kolom, n)` yang mengembalikan list label indeks `n` baris dengan nilai `kolom` terbesar. Bila ada nilai kembar, baris yang muncul lebih dulu pada tabel harus didahulukan (pengurutan stabil).",
            ind("""
import pandas as pd

def top_n(df, kolom, n):
    # TODO: implementasikan
    pass
"""),
            P("""
assert top_n(df, 'qty', 3) == [0, 4, 3]
t = pd.DataFrame({'qty': [5, 9, 5, 1]})
assert top_n(t, 'qty', 3) == [1, 0, 2]
assert top_n(t, 'qty', 1) == [1]
assert top_n(df, 'harga', 2) == [2, 5]
"""),
            "Urutkan menurun dengan kind stabil lalu head.",
            F4.strip("\n"),
        ),
    ],
    [
        M("Mengira sort_values mengubah tabel asal.", "Tampung hasilnya."),
        M("Mengabaikan nilai hilang yang jatuh di akhir.", "Atur na_position atau tangani lebih dulu."),
        M("Mengandalkan urutan baris kembar.", "Pakai kind stable atau pemecah kembar unik."),
    ],
    [
        Q("sort_values mengembalikan?", ["Tabel baru", "None", "Series", "Perubahan di tempat"], 0, "Tanpa inplace.", hint="Baru."),
        Q("Nilai hilang secara bawaan di?", ["Akhir", "Awal", "Dibuang", "Tengah"], 0, "Last.", hint="Akhir."),
        Q("nlargest dipakai untuk?", ["Baris teratas tanpa mengurutkan semua", "Menghapus", "Mengacak", "Menjumlah"], 0, "Cepat.", hint="Teratas."),
        Q("rank method min pada kembar?", ["Peringkat terendah sama", "Rata-rata", "Berurutan", "Acak"], 0, "Gaya olahraga.", hint="Min."),
        Q("Pengurutan stabil?", ["Menjaga urutan baris kembar", "Lebih cepat selalu", "Mengacak", "Membuang kembar"], 0, "Deterministik.", hint="Stabil."),
    ],
    [
        "sort_values mengurutkan menurut satu atau banyak kolom dengan arah per kolom.",
        "na_position mengatur letak nilai hilang.",
        "nlargest, nsmallest, dan rank mencari urutan tanpa pengurutan penuh.",
        "Pengurutan stabil menjaga hasil deterministik pada nilai kembar.",
    ],
    [],
)

G1 = """
import pandas as pd

def query_wilayah(df, w):
    return df.query('wilayah == @w').index.tolist()
"""
G2 = """
import pandas as pd

def hapus_duplikat(df, kolom):
    return df.drop_duplicates(kolom).index.tolist()
"""
G3 = """
import pandas as pd

def di_atas_rata(df):
    return df.loc[df['qty'] > df['qty'].mean(), 'produk'].tolist()
"""
G4 = """
import pandas as pd

def semua_duplikat(df, kolom):
    return df.index[df.duplicated(kolom, keep=False)].tolist()
"""

l2 = lesson(
    "B2-03-2",
    "query, duplikat, dan filter lanjutan",
    35,
    [
        "Menulis filter ringkas dengan query",
        "Memakai variabel Python di dalam query",
        "Menemukan dan membuang duplikat",
        "Memfilter dengan statistik seperti rata-rata dan kuantil",
    ],
    [
        tb("Metode query", "Selain mask boolean, pandas menyediakan `query`, yang menerima syarat sebagai teks dan sering lebih mudah dibaca. Ekspresi `df.query('qty > 5 and wilayah == \"Jkt\"')` setara dengan `df[(df['qty'] > 5) & (df['wilayah'] == 'Jkt')]` tetapi tanpa kurung dan tanpa mengulang nama tabel. Di dalam query Anda boleh memakai `and`, `or`, dan `not`, berbeda dari mask yang membutuhkan operator simbol."),
        C(
            P("""
print(df.query('qty > 5').index.tolist())
print(df.query('qty > 5 and wilayah == "Jkt"').index.tolist())
print(df.query('wilayah in ["Bdg", "Sby"]').shape)
print(df.query('produk == "Pena" or harga > 40').index.tolist())
print(df.query('not (qty > 5)').index.tolist())
"""),
            ind("""
[0, 3, 4]
[0, 4]
(3, 4)
[0, 2, 3]
[1, 2, 5]
"""),
            "Query menulis syarat sebagai teks yang ringkas dan mendukung and, or, not, dan in.",
            filename="query_dasar.py",
        ),
        tb("Variabel di dalam query", "Untuk memakai variabel Python di dalam teks query, awali namanya dengan `@`. Ini memungkinkan batas dan daftar nilai ditentukan di luar teks sehingga query dapat dipakai ulang. Nama kolom yang mengandung spasi atau karakter khusus ditulis dengan tanda petik balik. Karena query berupa teks, kesalahan ketik baru ketahuan saat dijalankan, jadi mask boolean lebih aman untuk logika kompleks yang dihasilkan program."),
        C(
            P("""
batas = 6
print(df.query('qty >= @batas')['produk'].tolist())
w = 'Jkt'
print(df.query('wilayah == @w').index.tolist())
daftar = ['Tas', 'Topi']
print(df.query('produk in @daftar').index.tolist())
print(df.query('`qty` > 7').index.tolist())
"""),
            ind("""
['Pena', 'Pena', 'Buku']
[0, 2, 4]
[2, 5]
[0, 4]
"""),
            "Awalan at memanggil variabel Python di dalam query, termasuk list, dan tanda petik balik membungkus nama kolom.",
            filename="query_variabel.py",
        ),
        tb("Mendeteksi duplikat", "Metode `duplicated(kolom)` mengembalikan Series boolean yang bernilai True untuk baris yang merupakan pengulangan dari baris sebelumnya, berdasarkan kolom yang disebutkan atau seluruh kolom bila tidak disebutkan. Argumen `keep` mengatur baris mana yang dianggap asli: `first` menandai pengulangan setelah yang pertama, `last` menandai sebelum yang terakhir, dan `False` menandai semua baris yang berduplikat, termasuk yang pertama."),
        tb("Membuang duplikat", "Metode `drop_duplicates(kolom, keep=...)` membuang baris duplikat dan mengembalikan tabel baru. Tanpa `kolom`, baris dianggap duplikat bila seluruh nilainya sama. Pilih `keep` sesuai maksud: simpan kemunculan pertama bila data berurutan waktu dan yang awal dianggap asli, atau yang terakhir bila yang terbaru dianggap paling benar. Selalu hitung jumlah baris sebelum dan sesudah untuk memastikan pembersihan tidak berlebihan."),
        C(
            P("""
print(df.duplicated('produk').tolist())
print(df.drop_duplicates('produk').index.tolist())
print(df.drop_duplicates('produk', keep='last').index.tolist())
print(df.drop_duplicates(['produk', 'harga']).shape)
print(df.index[df.duplicated(['produk', 'harga'], keep=False)].tolist())
"""),
            ind("""
[False, False, False, True, True, False]
[0, 1, 2, 5]
[2, 3, 4, 5]
(4, 4)
[0, 1, 3, 4]
"""),
            "Keep first mempertahankan kemunculan pertama dan keep last yang terakhir. Keep False menandai semua anggota kelompok kembar.",
            filename="duplikat.py",
        ),
        tb("Filter teks", "Atribut `str` menyediakan `contains`, `startswith`, `endswith`, `match`, dan `len` untuk menyaring kolom teks. `contains` menerima ekspresi reguler secara bawaan, jadi tanda seperti titik dan tanda kurung punya makna khusus. Atur `regex=False` untuk pencarian teks biasa dan `case=False` untuk mengabaikan huruf besar kecil. Argumen `na=False` mencegah nilai hilang menjadi hasil campuran saat dipakai sebagai mask."),
        tb("Filter berdasarkan statistik", "Syarat tidak harus berupa angka tetap. Anda dapat membandingkan kolom dengan statistiknya sendiri: baris di atas rata-rata, di atas kuantil sembilan puluh, atau lebih dari dua simpangan baku dari rata-rata. Statistik dihitung dari seluruh kolom lalu dipakai dalam mask. Cara ini mendasari penemuan pencilan sederhana dan pemilihan kelompok teratas tanpa menetapkan ambang manual."),
        C(
            P("""
rata = df['qty'].mean()
print(round(float(rata), 4))
print(df.loc[df['qty'] > rata, 'produk'].tolist())
print(float(df['qty'].quantile(0.5)), float(df['qty'].quantile(0.25)))
print(df[df['qty'] >= df['qty'].quantile(0.5)].index.tolist())
print(df[df['produk'].str.contains('^P|^T')]['produk'].tolist())
print(df[df['produk'].str.contains('EN', case=False)].index.tolist())
"""),
            ind("""
5.8333
['Pena', 'Pena', 'Buku']
6.0 3.5
[0, 3, 4]
['Pena', 'Tas', 'Pena', 'Topi']
[0, 3]
"""),
            "Filter berdasarkan rata-rata dan kuantil serta pencarian teks dengan ekspresi reguler.",
            filename="filter_statistik.py",
        ),
        tb("Memeriksa semua kolom sekaligus", "Untuk memeriksa banyak kolom dengan syarat sama, bandingkan sub-tabel lalu ringkas dengan `any(axis=1)` atau `all(axis=1)`. Ungkapan `(df[['a', 'b']] > 5).any(axis=1)` benar untuk baris yang salah satu kolomnya lebih dari lima. Pola ini berguna untuk mencari baris yang memiliki nilai hilang pada kolom mana pun, atau yang semua kolom pentingnya terisi."),
        tb("Memilih dengan indeks", "Mask juga dapat dibuat dari indeks: `df.index.isin([0, 2, 4])` memilih baris menurut label, dan `df.index.str.startswith('p')` memilih menurut pola label teks. Ini berguna ketika indeks berisi kunci yang bermakna seperti kode wilayah atau tanggal. Gabungkan dengan mask kolom bila diperlukan, dan ingat bahwa pencocokan label tidak bergantung pada urutan baris."),
        tb("Memilih query atau mask", "Query unggul untuk kondisi pendek yang dibaca manusia, dan menghindari pengulangan nama tabel. Mask boolean unggul untuk kondisi yang dihitung program, yang menggunakan fungsi, atau yang akan dipakai ulang. Tidak ada yang selalu terbaik. Pilih yang membuat maksud paling jelas bagi pembaca, dan konsisten dalam satu proyek agar kode seragam."),
        K("tip", "Gunakan @ untuk memanggil variabel di dalam query, dan tanda petik balik untuk nama kolom yang mengandung spasi.", title="Query praktis"),
        tb("Menghitung hasil filter", "Setelah menyaring, selalu laporkan berapa baris yang lolos dan berapa persen dari total. Filter yang meloloskan terlalu sedikit baris membuat ringkasan tidak dapat dipercaya, dan filter yang meloloskan semuanya mungkin berarti syarat tidak bekerja. `len(hasil)` dan `len(hasil) / len(df)` adalah pemeriksaan kewarasan yang murah dan menangkap banyak kesalahan syarat."),
        tb("Duplikat dan kunci", "Sebelum membuang duplikat, tentukan apa arti duplikat bagi data Anda. Dua baris dengan produk sama dan harga sama mungkin transaksi sah yang berbeda, bukan salah entri. Duplikat sebenarnya biasanya memiliki seluruh kolom identik, termasuk id transaksi. Membuang berdasarkan kolom yang salah menghapus data sah, jadi kenali kunci unik yang benar sebelum membersihkan."),
        E(
            "B2-03-2-ex1",
            "mudah",
            "Tulis fungsi `query_wilayah(df, w)` yang mengembalikan list label indeks baris dengan `wilayah` sama dengan `w`, memakai `query` dengan variabel `@w`.",
            ind("""
import pandas as pd

def query_wilayah(df, w):
    # TODO: implementasikan
    pass
"""),
            P("""
assert query_wilayah(df, 'Jkt') == [0, 2, 4]
assert query_wilayah(df, 'Bdg') == [1, 5]
assert query_wilayah(df, 'Sby') == [3]
assert query_wilayah(df, 'XYZ') == []
"""),
            "df.query dengan teks wilayah sama dengan at w.",
            G1.strip("\n"),
        ),
        E(
            "B2-03-2-ex2",
            "sedang",
            "Tulis fungsi `hapus_duplikat(df, kolom)` yang mempertahankan kemunculan pertama tiap nilai `kolom` (nama kolom atau list) dan mengembalikan list label indeks baris yang tersisa.",
            ind("""
import pandas as pd

def hapus_duplikat(df, kolom):
    # TODO: implementasikan
    pass
"""),
            P("""
assert hapus_duplikat(df, 'produk') == [0, 1, 2, 5]
assert hapus_duplikat(df, ['produk', 'harga']) == [0, 1, 2, 5]
assert hapus_duplikat(df, 'wilayah') == [0, 1, 3]
assert hapus_duplikat(df, 'qty') == [0, 1, 2, 3, 4, 5]
"""),
            "drop_duplicates dengan kolom, lalu index.",
            G2.strip("\n"),
        ),
        E(
            "B2-03-2-ex3",
            "sedang",
            "Tulis fungsi `di_atas_rata(df)` yang mengembalikan list `produk` untuk baris yang `qty`-nya lebih besar dari rata-rata `qty`.",
            ind("""
import pandas as pd

def di_atas_rata(df):
    # TODO: implementasikan
    pass
"""),
            P("""
assert di_atas_rata(df) == ['Pena', 'Pena', 'Buku']
assert di_atas_rata(df.iloc[:2]) == ['Pena']
assert di_atas_rata(df.iloc[[0, 0]]) == []
assert di_atas_rata(df.iloc[[2, 5]]) == ['Tas']
"""),
            "Bandingkan qty dengan mean qty di dalam loc.",
            G3.strip("\n"),
        ),
        E(
            "B2-03-2-ex4",
            "menantang",
            "Tulis fungsi `semua_duplikat(df, kolom)` yang mengembalikan list label indeks semua baris yang nilai `kolom`-nya muncul lebih dari satu kali, termasuk kemunculan pertamanya.",
            ind("""
import pandas as pd

def semua_duplikat(df, kolom):
    # TODO: implementasikan
    pass
"""),
            P("""
assert semua_duplikat(df, ['produk', 'harga']) == [0, 1, 3, 4]
assert semua_duplikat(df, 'produk') == [0, 1, 3, 4]
assert semua_duplikat(df, 'qty') == []
assert semua_duplikat(df, 'wilayah') == [0, 1, 2, 4, 5]
"""),
            "duplicated dengan keep False lalu ambil index.",
            G4.strip("\n"),
        ),
    ],
    [
        M("Memakai & dan kurung di query.", "Di query pakai and, or, not."),
        M("Menulis variabel tanpa at di query.", "Awali dengan at agar dikenali sebagai variabel."),
        M("Membuang duplikat tanpa memeriksa jumlah baris.", "Bandingkan jumlah sebelum dan sesudah."),
    ],
    [
        Q("Variabel Python di query ditulis?", ["@nama", "$nama", "{nama}", "nama"], 0, "At.", hint="Alamat."),
        Q("keep=False pada duplicated?", ["Menandai semua kembaran", "Menandai pertama", "Menandai terakhir", "Tidak ada"], 0, "Semua.", hint="Semua."),
        Q("drop_duplicates tanpa kolom?", ["Seluruh kolom sama", "Kolom pertama", "Indeks", "Tidak ada"], 0, "Baris identik.", hint="Seluruh."),
        Q("str.contains menerima secara bawaan?", ["Ekspresi reguler", "Teks biasa", "Angka", "Tanggal"], 0, "Regex.", hint="Regex."),
        Q("any(axis=1) menyatakan?", ["Ada kolom yang benar per baris", "Semua kolom benar", "Jumlah", "Indeks"], 0, "Per baris.", hint="Ada."),
    ],
    [
        "query menulis filter sebagai teks ringkas dengan at untuk variabel.",
        "duplicated dan drop_duplicates menemukan dan membuang baris kembar.",
        "Filter dapat memakai statistik kolom seperti rata-rata dan kuantil.",
        "any dan all pada axis satu memeriksa banyak kolom sekaligus.",
    ],
    [],
)

H1 = """
import pandas as pd

def omzet_teratas(df, n):
    d = df.assign(omzet=df['qty'] * df['harga'])
    return d.nlargest(n, 'omzet')['produk'].tolist()
"""
H2 = """
import pandas as pd

def porsi_omzet(df):
    omzet = df['qty'] * df['harga']
    return (omzet / omzet.sum()).round(3).tolist()
"""
H3 = """
import pandas as pd

def omzet_kumulatif(df):
    omzet = (df['qty'] * df['harga']).sort_values(ascending=False)
    return omzet.cumsum().tolist()
"""
H4 = """
import pandas as pd

def pipeline_bersih(df, qty_min):
    return (
        df[df['qty'] >= qty_min]
        .sort_values(['wilayah', 'qty'], ascending=[True, False])
        .reset_index(drop=True)[['wilayah', 'qty']]
        .values.tolist()
    )
"""

l3 = lesson(
    "B2-03-3",
    "Pola praktis: peringkat, porsi, dan rantai metode",
    35,
    [
        "Menghitung omzet turunan dan memeringkatnya",
        "Menghitung porsi dan kumulatif untuk analisis Pareto",
        "Menulis rantai metode yang bersih dengan assign dan pipe",
        "Menjaga urutan langkah filter, sort, dan reset yang benar",
    ],
    [
        tb("Dari pertanyaan ke kode", "Pertanyaan bisnis hampir selalu berbentuk gabungan filter, urutan, dan ringkasan: produk apa yang menyumbang omzet terbesar, berapa persen dari total, dan berapa produk yang menyumbang delapan puluh persen pendapatan. Pelajaran ini menggabungkan alat yang sudah dipelajari menjadi pola-pola siap pakai yang akan sering Anda tulis ulang dalam berbagai bentuk."),
        tb("Kolom turunan", "Langkah pertama biasanya menghitung besaran yang belum ada di data, misalnya omzet sama dengan kuantitas dikali harga. Kolom baru dibuat dengan `assign` atau penugasan langsung, lalu dipakai untuk mengurutkan dan menyaring. Menulis rumus pada kolom utuh adalah vectorized sehingga cepat, dan hasilnya selaras dengan indeks tabel."),
        C(
            P("""
df['omzet'] = df['qty'] * df['harga']
print(df['omzet'].tolist())
print(df.nlargest(2, 'omzet')['produk'].tolist())
print(df.nlargest(3, 'omzet')['produk'].tolist())
print(float(df['omzet'].sum()))
print(df.sort_values('omzet', ascending=False).iloc[0]['produk'])
"""),
            ind("""
[30.0, 60.0, 150.0, 21.0, 96.0, 40.0]
['Tas', 'Buku']
['Tas', 'Buku', 'Buku']
397.0
Tas
"""),
            "Omzet dihitung per baris, dan baris teratas diambil dengan nlargest atau pengurutan.",
            filename="omzet_turunan.py",
        ),
        tb("Porsi dari total", "Porsi tiap baris terhadap total dihitung dengan membagi kolom dengan jumlahnya: `df['omzet'] / df['omzet'].sum()`. Hasilnya bilangan antara nol dan satu yang berjumlah satu. Kalikan seratus untuk persen. Porsi lebih mudah dibandingkan antar periode daripada nilai mutlak, karena mengabaikan skala total, dan menjadi dasar grafik komposisi seperti diagram lingkaran dan batang bertumpuk."),
        tb("Kumulatif dan analisis Pareto", "Urutkan dari terbesar lalu ambil jumlah kumulatif untuk melihat seberapa cepat total terkumpul. Prinsip Pareto menyatakan bahwa sebagian kecil penyumbang sering menghasilkan sebagian besar total. Dengan porsi kumulatif, Anda dapat menjawab berapa produk yang cukup untuk mencakup delapan puluh persen omzet, lalu memfokuskan perhatian pada mereka."),
        C(
            P("""
df['omzet'] = df['qty'] * df['harga']
porsi = df['omzet'] / df['omzet'].sum()
print(porsi.round(3).tolist())
print(round(float(porsi.sum()), 6))
urut = df.sort_values('omzet', ascending=False)
print(urut['omzet'].cumsum().tolist())
kum = (urut['omzet'] / df['omzet'].sum()).cumsum()
print(int((kum < 0.8).sum()) + 1)
print(urut['produk'].tolist())
"""),
            ind("""
[0.076, 0.151, 0.378, 0.053, 0.242, 0.101]
1.0
[150.0, 246.0, 306.0, 346.0, 376.0, 397.0]
4
['Tas', 'Buku', 'Buku', 'Topi', 'Pena', 'Pena']
"""),
            "Porsi berjumlah satu. Kumulatif setelah pengurutan menunjukkan empat baris cukup untuk mencapai delapan puluh persen omzet.",
            filename="porsi_pareto.py",
        ),
        tb("Rantai metode", "Metode pandas mengembalikan objek baru sehingga dapat dirangkai: filter, urutkan, reset, pilih kolom. Menulis rantai dalam kurung dengan satu metode per baris membuat alur terbaca seperti resep dan menghindari variabel perantara yang berserakan. Setiap langkah menerima hasil langkah sebelumnya, sehingga tidak ada keadaan tersembunyi yang berubah di tengah jalan."),
        C(
            P("""
hasil = (
    df[df['qty'] >= 3]
    .sort_values(['wilayah', 'qty'], ascending=[True, False])
    .reset_index(drop=True)[['wilayah', 'qty']]
    .values.tolist()
)
print(hasil)
d = df.assign(omzet=lambda t: t['qty'] * t['harga']).pipe(lambda t: t[t['omzet'] > 50])
print(d['produk'].tolist())
print('omzet' in df.columns)
"""),
            ind("""
[['Bdg', 5], ['Jkt', 10], ['Jkt', 8], ['Jkt', 3], ['Sby', 7]]
['Buku', 'Tas', 'Buku']
False
"""),
            "Rantai metode menyaring, mengurutkan, dan memilih kolom. Assign dengan lambda membuat kolom baru tanpa mengubah tabel asal.",
            filename="rantai_metode.py",
        ),
        tb("assign dan pipe", "Metode `assign` menambah kolom dan mengembalikan tabel baru, dengan lambda yang menerima tabel pada tahap itu sehingga dapat merujuk kolom yang baru dibuat di langkah sebelumnya. Metode `pipe` menerapkan fungsi apa pun pada tabel di tengah rantai, termasuk fungsi buatan Anda. Keduanya menjaga rantai tetap tak terputus tanpa perlu menyimpan hasil perantara."),
        tb("Urutan langkah penting", "Urutan filter, sort, dan reset memengaruhi hasil dan kecepatan. Filter lebih dulu bila memungkinkan agar pengurutan memproses lebih sedikit baris. Reset indeks di akhir, bukan di tengah, kecuali Anda memang membutuhkan nomor urut bersih lebih awal. Pilih kolom di akhir bila kolom lain diperlukan untuk langkah sebelumnya, dan periksa hasil tiap langkah saat debugging."),
        tb("Memeriksa hasil antara", "Rantai panjang sulit di-debug bila hasilnya mengejutkan. Pecah rantai pada titik curiga dan cetak `shape`, `head`, dan `dtypes`. Atau sisipkan `pipe` dengan fungsi yang mencetak lalu mengembalikan tabel yang sama. Setelah masalah ditemukan, satukan kembali. Kemudahan memotong rantai di tengah adalah salah satu keuntungan gaya ini dibanding blok penugasan panjang."),
        tb("Ringkasan modul", "Anda telah belajar mengurutkan dengan banyak kunci dan nilai kembar, menyaring dengan query dan statistik, mendeteksi duplikat, serta menyusun pola praktis seperti porsi, kumulatif, dan rantai metode. Pola ini muncul di hampir setiap analisis nyata. Modul berikutnya membahas pembuatan kolom turunan dengan map dan apply."),
        K("tip", "Tulis rantai metode dalam kurung dengan satu langkah per baris. Filter lebih dulu agar langkah berikutnya memproses lebih sedikit baris.", title="Rantai yang rapi"),
        tb("Pareto dengan kategori", "Analisis Pareto biasanya dilakukan per kategori, bukan per baris. Kelompokkan omzet per produk dengan `groupby`, urutkan menurun, hitung porsi kumulatif, lalu tandai kategori yang membentuk delapan puluh persen pertama. Alat pengelompokan dibahas mendalam pada modul tentang groupby, tetapi pola urutan dan kumulatif yang dipelajari di sini tetap menjadi langkah inti."),
        tb("Peringkat per kelompok", "Sering kita butuh peringkat di dalam kelompok, misalnya produk terlaris per wilayah. Urutkan seluruh tabel menurun lalu ambil `groupby('wilayah').head(1)` untuk satu terbaik per wilayah, atau gunakan `rank` di dalam groupby. Dua cara ini memberi hasil serupa, dan pola urut dulu lalu ambil teratas per kelompok sangat sering muncul dalam laporan."),
        tb("Menyimpan hasil antara", "Bila rantai metode menghasilkan tabel yang akan dipakai berulang, simpan dalam variabel bernama jelas, misalnya `top_produk`. Jangan menghitung ulang rantai panjang yang sama di banyak tempat. Namun jangan pula memecah rantai menjadi puluhan variabel sementara yang namanya tidak bermakna. Keseimbangannya: satu variabel per hasil yang bermakna secara bisnis."),
        E(
            "B2-03-3-ex1",
            "mudah",
            "Tulis fungsi `omzet_teratas(df, n)` yang menghitung omzet tiap baris (`qty` dikali `harga`) dan mengembalikan list `produk` untuk `n` baris dengan omzet terbesar, dari yang terbesar.",
            ind("""
import pandas as pd

def omzet_teratas(df, n):
    # TODO: implementasikan
    pass
"""),
            P("""
assert omzet_teratas(df, 2) == ['Tas', 'Buku']
assert omzet_teratas(df, 3) == ['Tas', 'Buku', 'Buku']
assert omzet_teratas(df, 1) == ['Tas']
assert 'omzet' not in df.columns
"""),
            "assign omzet lalu nlargest dan ambil kolom produk.",
            H1.strip("\n"),
        ),
        E(
            "B2-03-3-ex2",
            "sedang",
            "Tulis fungsi `porsi_omzet(df)` yang mengembalikan list porsi omzet tiap baris terhadap total omzet, dibulatkan ke tiga desimal.",
            ind("""
import pandas as pd

def porsi_omzet(df):
    # TODO: implementasikan
    pass
"""),
            P("""
assert porsi_omzet(df) == [0.076, 0.151, 0.378, 0.053, 0.242, 0.101]
assert porsi_omzet(df.iloc[[2]]) == [1.0]
assert sum(porsi_omzet(df)) > 0.99
assert porsi_omzet(df.iloc[[0, 3]]) == [0.588, 0.412]
"""),
            "Bagi omzet dengan jumlahnya lalu bulatkan.",
            H2.strip("\n"),
        ),
        E(
            "B2-03-3-ex3",
            "sedang",
            "Tulis fungsi `omzet_kumulatif(df)` yang mengurutkan omzet (`qty` dikali `harga`) dari terbesar lalu mengembalikan jumlah kumulatifnya sebagai list.",
            ind("""
import pandas as pd

def omzet_kumulatif(df):
    # TODO: implementasikan
    pass
"""),
            P("""
assert omzet_kumulatif(df) == [150.0, 246.0, 306.0, 346.0, 376.0, 397.0]
assert omzet_kumulatif(df.iloc[[0]]) == [30.0]
assert omzet_kumulatif(df.iloc[[0, 3]]) == [30.0, 51.0]
assert omzet_kumulatif(df)[-1] == 397.0
"""),
            "Urutkan menurun lalu cumsum.",
            H3.strip("\n"),
        ),
        E(
            "B2-03-3-ex4",
            "menantang",
            "Tulis fungsi `pipeline_bersih(df, qty_min)` yang menyaring baris dengan `qty` sekurang-kurangnya `qty_min`, mengurutkan menurut `wilayah` menaik lalu `qty` menurun, menomori ulang indeks, dan mengembalikan kolom `wilayah` dan `qty` sebagai list bersarang.",
            ind("""
import pandas as pd

def pipeline_bersih(df, qty_min):
    # TODO: implementasikan
    pass
"""),
            P("""
assert pipeline_bersih(df, 3) == [['Bdg', 5], ['Jkt', 10], ['Jkt', 8], ['Jkt', 3], ['Sby', 7]]
assert pipeline_bersih(df, 8) == [['Jkt', 10], ['Jkt', 8]]
assert pipeline_bersih(df, 99) == []
assert len(pipeline_bersih(df, 0)) == 6
"""),
            "Rantai filter, sort_values dengan dua arah, reset_index, dan pilih dua kolom.",
            H4.strip("\n"),
        ),
    ],
    [
        M("Menulis banyak variabel perantara untuk satu alur.", "Pakai rantai metode dalam kurung."),
        M("Mengurutkan sebelum memfilter.", "Filter lebih dulu agar pengurutan lebih ringan."),
        M("Menjumlahkan porsi tanpa memeriksa totalnya.", "Pastikan porsi berjumlah satu."),
    ],
    [
        Q("Porsi dihitung dengan?", ["Nilai dibagi total", "Nilai dikali total", "Nilai dikurangi total", "Nilai ditambah total"], 0, "Bagi.", hint="Bagi."),
        Q("Kumulatif setelah pengurutan menurun menunjukkan?", ["Seberapa cepat total terkumpul", "Rata-rata", "Median", "Jumlah baris"], 0, "Pareto.", hint="Terkumpul."),
        Q("assign mengembalikan?", ["Tabel baru", "None", "Series", "Perubahan di tempat"], 0, "Baru.", hint="Baru."),
        Q("pipe berguna untuk?", ["Menerapkan fungsi di tengah rantai", "Menggabungkan tabel", "Mengacak", "Menghapus"], 0, "Fungsi bebas.", hint="Pipa."),
        Q("Sebaiknya filter dilakukan?", ["Sebelum sort", "Sesudah sort", "Terakhir", "Tidak perlu"], 0, "Lebih sedikit baris.", hint="Awal."),
    ],
    [
        "Kolom turunan dihitung vectorized dan dipakai untuk peringkat dan filter.",
        "Porsi dan kumulatif mendukung analisis Pareto.",
        "Rantai metode dengan assign dan pipe menghasilkan alur yang bersih.",
        "Urutan langkah memengaruhi hasil dan kecepatan.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perintah yang cukup jelas dalam teks.", "brief": []}

write_module(
    "B2",
    3,
    "Filtering, sorting, dan query",
    105,
    [
        "Mengurutkan data dengan benar termasuk nilai kembar dan hilang",
        "Menyaring dengan query, statistik, dan deteksi duplikat",
        "Menyusun pola omzet, porsi, dan rantai metode",
    ],
    [l1, l2, l3],
    video,
    REF,
)
