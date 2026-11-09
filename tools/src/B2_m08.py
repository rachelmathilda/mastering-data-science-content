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
    'bulan': [1, 1, 2, 2, 3, 3],
    'toko': ['A', 'B', 'A', 'B', 'A', 'B'],
    'omzet': [100, 80, 120, 90, 130, 70],
    'unit': [10, 8, 12, 9, 13, 7],
})
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

def lebar_omzet(df):
    return df.pivot(index='bulan', columns='toko', values='omzet').values.tolist()
"""
F12 = """
import pandas as pd

def total_toko(df):
    return pd.pivot_table(df, index='toko', values='omzet', aggfunc='sum')['omzet'].to_dict()
"""
F13 = """
import pandas as pd

def tabel_total(df):
    t = pd.pivot_table(df, index='toko', columns='bulan', values='omzet', aggfunc='sum', margins=True)
    return t.values.tolist()
"""
F14 = """
import pandas as pd

def pivot_aman(df, agg):
    t = pd.pivot_table(df, index='bulan', columns='toko', values='omzet', aggfunc=agg)
    return t.values.tolist()
"""

l1 = lesson(
    "B2-08-1",
    "Dari panjang ke lebar dengan pivot",
    35,
    [
        "Membedakan bentuk data panjang dan lebar",
        "Memakai pivot untuk memutar baris menjadi kolom",
        "Memakai pivot_table bila ada nilai ganda dan perlu agregasi",
        "Menambahkan total baris dan kolom dengan margins",
    ],
    [
        tb("Dua cara menulis tabel yang sama", "Informasi yang sama dapat ditulis dalam dua bentuk. Bentuk panjang menaruh satu pengamatan pada satu baris: setiap baris memuat bulan, toko, dan omzet. Bentuk lebar menaruh satu entitas pada satu baris dan membuka kolom untuk tiap kategori: setiap baris adalah satu bulan, dan toko A serta toko B masing-masing punya kolom sendiri. Isi datanya identik, hanya susunannya yang berbeda. Memahami kedua bentuk ini sangat penting karena alat yang berbeda menyukai bentuk yang berbeda, dan sebagian besar kerja pembersihan data sebenarnya adalah memindahkan data dari satu bentuk ke bentuk lain sampai cocok dengan alat yang akan dipakai."),
        tb("Mengapa bentuk penting", "Pustaka visualisasi seperti seaborn dan plotly menyukai bentuk panjang karena satu kolom dapat langsung menjadi warna, panel, atau sumbu. Groupby juga paling nyaman pada bentuk panjang. Sebaliknya, manusia lebih mudah membaca bentuk lebar karena dapat membandingkan toko dengan sekali lirik sepanjang baris, dan banyak operasi antar kolom seperti selisih atau rasio ditulis paling ringkas pada bentuk lebar. Sistem basis data dan log hampir selalu menyimpan data panjang, sedangkan laporan dan spreadsheet biasanya lebar. Karena itu seorang analis sering bolak-balik: simpan panjang, hitung lebar, tampilkan lebar, gambar panjang."),
        tb("Data contoh", "Pelajaran ini memakai tabel enam baris dengan kolom `bulan` berisi satu sampai tiga, `toko` berisi A dan B, `omzet`, dan `unit`. Setiap kombinasi bulan dan toko muncul tepat satu kali, sifat yang akan kita manfaatkan pada `pivot`. Angkanya sengaja kecil agar Anda dapat memeriksa tiap hasil dengan mata. Toko A mencatat 100, 120, dan 130 sepanjang tiga bulan, sedangkan toko B mencatat 80, 90, dan 70. Perhatikan bahwa total bulan satu adalah 180, bulan dua 210, dan bulan tiga 200, angka yang akan kita temui lagi dalam beberapa hasil di bawah."),
        C(
            P("""
w = df.pivot(index='bulan', columns='toko', values='omzet')
print(w.values.tolist())
print(w.index.tolist())
print(w.columns.tolist())
print(w.reset_index().columns.tolist())
print(w.columns.name, w.index.name)
print(df.pivot(index='toko', columns='bulan', values='omzet').values.tolist())
"""),
            ind("""
[[100, 80], [120, 90], [130, 70]]
[1, 2, 3]
['A', 'B']
['bulan', 'A', 'B']
toko bulan
[[100, 120, 130], [80, 90, 70]]
"""),
            "Pivot menentukan tiga hal: kolom yang menjadi indeks, kolom yang menjadi nama kolom baru, dan kolom yang mengisi sel. Menukar index dan columns memutar tabel.",
            filename="pivot_dasar.py",
        ),
        tb("Anatomi pivot", "Metode `pivot(index, columns, values)` membutuhkan tiga keputusan. Argumen `index` menentukan kolom mana yang nilai uniknya menjadi baris, `columns` menentukan kolom yang nilai uniknya menjadi kolom baru, dan `values` menentukan kolom yang isinya mengisi sel. Hasilnya tabel lebar dengan indeks bernama `bulan` dan kolom bernama `toko`. Nama sumbu itu tersimpan sebagai atribut `index.name` dan `columns.name`, dan sering mengejutkan pemula karena tampil sebagai judul kecil di atas tabel. Bila tidak diperlukan, `rename_axis(columns=None)` menghapusnya. Menukar peran `index` dan `columns` hanya memutar tabel, sehingga toko menjadi baris dan bulan menjadi kolom."),
        tb("Indeks menjadi kolom", "Hasil pivot menaruh kunci baris di indeks, bukan di kolom biasa. Untuk bekerja dengan kunci itu seperti kolom lain, atau untuk menyimpannya ke CSV, panggil `reset_index()`. Setelah itu kolom `bulan` kembali menjadi kolom biasa dan nama kolom toko tetap A dan B. Langkah ini hampir selalu muncul tepat sesudah pivot, jadi biasakan membaca keduanya sebagai satu kesatuan. Hal sebaliknya juga benar: sebelum pivot, kolom yang akan menjadi baris sudah harus berupa kolom biasa, dan seluruh sisa kolom yang tidak disebut dalam `index`, `columns`, atau `values` diabaikan, sehingga sebaiknya Anda menyaring kolom terlebih dahulu."),
        tb("Pivot menuntut keunikan", "Fungsi `pivot` tidak melakukan agregasi. Ia menganggap setiap pasangan nilai index dan columns muncul paling banyak sekali, dan melempar `ValueError` bila ada pasangan ganda karena tidak tahu harus memilih yang mana. Kegagalan ini justru berguna: ia memberi tahu bahwa data Anda tidak sebersih dugaan, misalnya ada transaksi tercatat dua kali atau ada kategori yang belum digabung. Daripada membungkam galat itu, selidiki dulu mengapa ada duplikat. Bila duplikat memang sah, misalnya beberapa transaksi dalam bulan yang sama, Anda perlu memutuskan cara meringkasnya, dan di situlah `pivot_table` dipakai."),
        tb("pivot_table untuk nilai ganda", "Fungsi `pd.pivot_table` adalah pivot yang melakukan agregasi. Ia menerima argumen `aggfunc` seperti `'sum'`, `'mean'`, atau `'count'` untuk meringkas semua nilai yang jatuh pada sel yang sama. Argumen `values` boleh berupa beberapa kolom, dan `aggfunc` boleh berupa dict yang memberi fungsi berbeda untuk tiap kolom. Argumen `fill_value` mengisi sel kosong. Seluruh perilakunya setara dengan groupby dengan dua kunci diikuti unstack, tetapi dengan sintaks yang lebih bersahabat bagi orang yang terbiasa dengan tabel pivot di spreadsheet. Bila Anda tidak yakin data unik, selalu pakai pivot_table."),
        C(
            P("""
d2 = pd.concat([df, pd.DataFrame({'bulan': [3], 'toko': ['A'], 'omzet': [10], 'unit': [1]})], ignore_index=True)
try:
    d2.pivot(index='bulan', columns='toko', values='omzet')
except ValueError:
    print('ValueError')
print(pd.pivot_table(d2, index='bulan', columns='toko', values='omzet', aggfunc='sum').values.tolist())
print(pd.pivot_table(d2, index='bulan', columns='toko', values='omzet', aggfunc='mean').values.tolist())
print(pd.pivot_table(df, index='toko', values='omzet', aggfunc='sum')['omzet'].to_dict())
print(pd.pivot_table(df, index='toko', values=['omzet', 'unit'], aggfunc={'omzet': 'sum', 'unit': 'mean'}).round(2).to_dict())
"""),
            ind("""
ValueError
[[100, 80], [120, 90], [140, 70]]
[[100.0, 80.0], [120.0, 90.0], [70.0, 70.0]]
{'A': 350, 'B': 240}
{'omzet': {'A': 350, 'B': 240}, 'unit': {'A': 11.67, 'B': 8.0}}
"""),
            "Pivot gagal pada duplikat, sedangkan pivot_table meringkasnya dengan aggfunc. Hasil berbeda tergantung fungsi yang dipilih, jadi pilihan aggfunc adalah keputusan analisis.",
            filename="pivot_table.py",
        ),
        tb("Pilihan aggfunc adalah keputusan", "Pada contoh di atas, bulan tiga toko A punya dua catatan, 130 dan 10. Dengan `sum` selnya 140, dengan `mean` selnya 70. Keduanya benar secara teknis tetapi menjawab pertanyaan berbeda. Omzet harus dijumlahkan, sedangkan harga satuan sebaiknya dirata-ratakan, dan jumlah transaksi dihitung dengan `count`. Memilih fungsi yang salah menghasilkan angka yang tampak wajar tetapi keliru, kesalahan yang paling sulit ditemukan karena tidak ada pesan galat. Karena itu tulis `aggfunc` secara eksplisit, jangan mengandalkan bawaan `mean`, dan pikirkan arti bisnis tiap kolom sebelum meringkasnya."),
        tb("Margins dan total", "Argumen `margins=True` menambah baris dan kolom `All` berisi total sesuai `aggfunc`. Total tampil di tepi tabel sehingga pembaca dapat memeriksa kesesuaian dengan angka yang mereka ketahui. Pada contoh di bawah, jumlah seluruh omzet 590 muncul di sudut kanan bawah. Nama label dapat diubah dengan `margins_name`. Perhatikan bahwa margins memakai fungsi agregasi yang sama untuk total, sehingga pada `mean` margin adalah rata-rata keseluruhan, bukan rata-rata dari rata-rata. Untuk laporan akhir, total sering ditambahkan di tahap penyajian saja, bukan dalam data yang akan dihitung lebih lanjut."),
        C(
            P("""
t = pd.pivot_table(df, index='toko', columns='bulan', values='omzet', aggfunc='sum', margins=True)
print(t.values.tolist())
print(t.index.tolist())
print(t.columns.tolist())
print(pd.crosstab(df['toko'], df['bulan']).values.tolist())
print(pd.crosstab(df['toko'], df['bulan'], values=df['omzet'], aggfunc='sum').values.tolist())
"""),
            ind("""
[[100, 120, 130, 350], [80, 90, 70, 240], [180, 210, 200, 590]]
['A', 'B', 'All']
[1, 2, 3, 'All']
[[1, 1, 1], [1, 1, 1]]
[[100, 120, 130], [80, 90, 70]]
"""),
            "Margins menambah total di tepi tabel. Crosstab adalah jalan pintas untuk tabel hitungan atau agregasi antara dua kolom kategori.",
            filename="margins_crosstab.py",
        ),
        tb("Crosstab untuk hitungan", "Fungsi `pd.crosstab(baris, kolom)` menghitung berapa kali tiap kombinasi dua kolom kategori muncul, dan dengan argumen `values` serta `aggfunc` ia bekerja seperti pivot_table. Ia lebih ringkas untuk pertanyaan seperti berapa pelanggan di tiap kota menurut jenis kelamin, dan argumen `normalize` mengubah hitungan menjadi proporsi per baris, per kolom, atau keseluruhan. Pada data ini setiap kombinasi muncul sekali, sehingga semua hitungannya satu. Crosstab sering menjadi langkah pertama sebelum uji kai kuadrat atau sebelum memutuskan apakah dua variabel kategori saling berkaitan."),
        tb("Sel kosong dan fill_value", "Bila kombinasi tertentu tidak ada dalam data, sel hasil pivot berisi NaN, dan kolom bilangan bulat berubah menjadi desimal karena NaN bertipe desimal. Pakai `fill_value=0` pada `pivot_table` bila ketiadaan memang berarti nol, misalnya tidak ada penjualan. Berhati-hatilah: mengisi nol menyembunyikan perbedaan antara tidak ada penjualan dan data yang belum masuk. Pertimbangkan membiarkan NaN bila perbedaan itu penting, dan dokumentasikan keputusan Anda agar pembaca laporan tidak salah menafsirkan sel nol sebagai kinerja buruk."),
        K("tip", "Pakai pivot bila pasangan kunci pasti unik, dan pivot_table dengan aggfunc eksplisit bila tidak. Galat pivot adalah informasi tentang data Anda.", title="Pivot atau pivot_table"),
        E(
            "B2-08-1-ex1",
            "mudah",
            "Tulis fungsi `lebar_omzet(df)` yang memutar `omzet` menjadi tabel lebar dengan `bulan` sebagai baris dan `toko` sebagai kolom, dan mengembalikan `values.tolist()`.",
            ind("""
import pandas as pd

def lebar_omzet(df):
    # TODO: implementasikan
    pass
"""),
            P("""
assert lebar_omzet(df) == [[100, 80], [120, 90], [130, 70]]
assert lebar_omzet(df.iloc[:2]) == [[100, 80]]
assert lebar_omzet(df.iloc[[0, 2, 4]]) == [[100], [120], [130]]
assert len(lebar_omzet(df)) == 3
"""),
            "pivot dengan index bulan, columns toko, values omzet.",
            X(F11),
        ),
        E(
            "B2-08-1-ex2",
            "sedang",
            "Tulis fungsi `total_toko(df)` yang memakai `pivot_table` dengan `toko` sebagai indeks untuk menjumlahkan `omzet`, dan mengembalikan dict `{toko: total}`.",
            ind("""
import pandas as pd

def total_toko(df):
    # TODO: implementasikan
    pass
"""),
            P("""
assert total_toko(df) == {'A': 350, 'B': 240}
assert total_toko(df.iloc[:2]) == {'A': 100, 'B': 80}
assert total_toko(df[df['bulan'] > 1]) == {'A': 250, 'B': 160}
assert sum(total_toko(df).values()) == 590
"""),
            "pivot_table dengan aggfunc sum lalu ambil kolom omzet.",
            X(F12),
        ),
        E(
            "B2-08-1-ex3",
            "sedang",
            "Tulis fungsi `tabel_total(df)` yang membuat pivot_table `omzet` dengan `toko` sebagai baris, `bulan` sebagai kolom, jumlah sebagai agregasi, dan total tepi, lalu mengembalikan `values.tolist()`.",
            ind("""
import pandas as pd

def tabel_total(df):
    # TODO: implementasikan
    pass
"""),
            P("""
assert tabel_total(df) == [[100, 120, 130, 350], [80, 90, 70, 240], [180, 210, 200, 590]]
assert tabel_total(df.iloc[:2]) == [[100, 100], [80, 80], [180, 180]]
assert tabel_total(df)[-1][-1] == 590
assert len(tabel_total(df)) == 3
"""),
            "pivot_table dengan margins True.",
            X(F13),
        ),
        E(
            "B2-08-1-ex4",
            "menantang",
            "Tulis fungsi `pivot_aman(df, agg)` yang membuat tabel lebar `omzet` per `bulan` dan `toko` dengan fungsi agregasi `agg`, sehingga tetap bekerja walau ada pasangan ganda, dan mengembalikan `values.tolist()`.",
            ind("""
import pandas as pd

def pivot_aman(df, agg):
    # TODO: implementasikan
    pass
"""),
            P("""
d2 = pd.concat([df, pd.DataFrame({'bulan': [3], 'toko': ['A'], 'omzet': [10], 'unit': [1]})], ignore_index=True)
assert pivot_aman(d2, 'sum') == [[100, 80], [120, 90], [140, 70]]
assert pivot_aman(d2, 'mean') == [[100.0, 80.0], [120.0, 90.0], [70.0, 70.0]]
assert pivot_aman(d2, 'count')[2] == [2, 1]
assert pivot_aman(df, 'sum') == [[100, 80], [120, 90], [130, 70]]
"""),
            "pivot_table dengan argumen aggfunc yang diteruskan.",
            X(F14),
        ),
    ],
    [
        M("Memakai pivot pada data dengan pasangan ganda.", "Pakai pivot_table dengan aggfunc eksplisit."),
        M("Membiarkan aggfunc bawaan mean.", "Tulis aggfunc sesuai arti kolom."),
        M("Mengisi sel kosong dengan nol tanpa berpikir.", "Bedakan tidak ada dan belum masuk."),
    ],
    [
        Q("Data panjang menaruh satu pengamatan di?", ["Satu baris", "Satu kolom", "Satu sel", "Satu tabel"], 0, "Panjang.", hint="Baris."),
        Q("pivot pada pasangan ganda?", ["ValueError", "Menjumlah", "Merata-rata", "Mengabaikan"], 0, "Tak mengagregasi.", hint="Galat."),
        Q("pivot_table memakai?", ["aggfunc", "melt", "merge", "concat"], 0, "Agregasi.", hint="aggfunc."),
        Q("margins True menambah?", ["Total tepi", "Kolom baru", "Indeks", "Duplikat"], 0, "All.", hint="Total."),
        Q("crosstab menghitung?", ["Kombinasi kategori", "Rata-rata", "Korelasi", "Median"], 0, "Frekuensi.", hint="Hitungan."),
    ],
    [
        "Data yang sama dapat ditulis panjang atau lebar.",
        "pivot memutar baris menjadi kolom dan menuntut pasangan unik.",
        "pivot_table meringkas nilai ganda dengan aggfunc.",
        "margins menambah total dan fill_value mengisi sel kosong.",
    ],
    [],
)

G11 = """
import pandas as pd

def melt_panjang(wide):
    m = wide.melt(id_vars='bulan', var_name='toko', value_name='omzet')
    return m.values.tolist()
"""
G12 = """
import pandas as pd

def melt_sebagian(wide, kolom):
    m = wide.melt(id_vars='bulan', value_vars=kolom, var_name='toko', value_name='omzet')
    return m.values.tolist()
"""
G13 = """
import pandas as pd

def tumpuk_dict(w):
    return w.stack().to_dict()
"""
G14 = """
import pandas as pd

def melt_kuartal(wd):
    m = wd.melt(id_vars='id', var_name='kuartal', value_name='nilai')
    return m.sort_values(['id', 'kuartal']).values.tolist()
"""

l2 = lesson(
    "B2-08-2",
    "Dari lebar ke panjang dengan melt dan stack",
    35,
    [
        "Mengubah kolom menjadi baris dengan melt",
        "Memilih id_vars, value_vars, dan nama kolom hasil",
        "Memakai stack dan unstack pada indeks bertingkat",
        "Membuktikan bahwa pivot dan melt saling membalik",
    ],
    [
        tb("Kebalikan dari pivot", "Banyak data tiba dalam bentuk lebar, terutama dari spreadsheet: satu kolom untuk tiap bulan, tiap kuartal, atau tiap pertanyaan survei. Bentuk itu enak dibaca tetapi sulit dianalisis, sebab menambah bulan baru berarti menambah kolom, dan mengelompokkan menurut bulan tidak dapat dilakukan karena bulan bukan nilai melainkan nama kolom. Metode `melt` melelehkan kolom-kolom itu menjadi baris sehingga nama kolom menjadi nilai dalam satu kolom baru, dan angkanya masuk ke kolom nilai. Hasilnya bentuk panjang yang cocok untuk groupby, seaborn, dan hampir semua alat analisis."),
        tb("Prinsip data rapi", "Konsep data rapi, atau tidy data, dari Hadley Wickham menyatakan tiga aturan: tiap variabel berada dalam satu kolom, tiap pengamatan berada dalam satu baris, dan tiap jenis satuan pengamatan berada dalam satu tabel. Tabel lebar dengan kolom A dan B melanggar aturan pertama karena toko adalah variabel yang tersebar di dua kolom. Setelah dilelehkan, kolom `toko` memuat variabel itu dan kolom `omzet` memuat nilainya. Data rapi bukan dogma, tetapi titik awal yang baik karena sebagian besar alat pandas dan seaborn dirancang untuknya, dan alasan sebuah pengecualian perlu bisa Anda jelaskan."),
        C(
            P("""
w = df.pivot(index='bulan', columns='toko', values='omzet')
wide = w.reset_index()
m = wide.melt(id_vars='bulan', var_name='toko', value_name='omzet')
print(m.values.tolist())
print(m.columns.tolist())
m2 = wide.melt(id_vars='bulan', value_vars=['A'], var_name='toko', value_name='omzet')
print(m2.values.tolist())
wd = pd.DataFrame({'id': [1, 2], 'q1': [5, 6], 'q2': [7, 8]})
print(wd.melt(id_vars='id').values.tolist())
"""),
            ind("""
[[1, 'A', 100], [2, 'A', 120], [3, 'A', 130], [1, 'B', 80], [2, 'B', 90], [3, 'B', 70]]
['bulan', 'toko', 'omzet']
[[1, 'A', 100], [2, 'A', 120], [3, 'A', 130]]
[[1, 'q1', 5], [2, 'q1', 6], [1, 'q2', 7], [2, 'q2', 8]]
"""),
            "Id_vars dipertahankan sebagai kolom, kolom lain dilelehkan. Tanpa var_name dan value_name, pandas memakai nama variable dan value.",
            filename="melt_dasar.py",
        ),
        tb("Memilih id_vars dan value_vars", "Argumen `id_vars` menyebut kolom yang dipertahankan apa adanya sebagai pengenal, dan `value_vars` menyebut kolom yang dilelehkan. Bila `value_vars` tidak disebut, semua kolom selain `id_vars` dilelehkan. Hasilnya berisi satu baris untuk setiap pasangan baris asal dan kolom yang dilelehkan, sehingga jumlah baris hasil adalah jumlah baris asal dikali jumlah kolom lelehan. Hitung dulu ukuran ini di kepala: melelehkan seratus kolom pada sejuta baris menghasilkan seratus juta baris, yang dapat menghabiskan memori dengan cepat."),
        tb("Menamai hasil", "Tanpa argumen tambahan, melt menamai kolom hasil `variable` dan `value`, nama generik yang cepat menjadi membingungkan setelah beberapa langkah. Berikan `var_name` untuk kolom yang memuat nama kolom lama dan `value_name` untuk kolom angka, misalnya `toko` dan `omzet`. Kebiasaan menamai sejak awal mencegah kebingungan ketika tabel dipakai lagi tiga langkah kemudian, dan membuat hasil langsung siap untuk groupby atau grafik tanpa `rename` tambahan. Nama yang baik adalah dokumentasi paling murah yang dapat Anda tulis."),
        tb("Mengurutkan setelah melt", "Urutan baris hasil melt mengikuti kolom: seluruh nilai kolom pertama, lalu seluruh nilai kolom kedua, dan seterusnya. Pada contoh, semua bulan toko A muncul dulu, baru toko B. Bila Anda menginginkan urutan per bulan, urutkan dengan `sort_values(['bulan', 'toko'])` dan, bila perlu, `reset_index(drop=True)`. Jangan bergantung pada urutan bawaan saat membandingkan dua hasil. Bila Anda menguji kode dengan membandingkan tabel, urutkan keduanya lebih dulu agar uji tidak gagal hanya karena perbedaan urutan baris yang tidak bermakna."),
        C(
            P("""
w = df.pivot(index='bulan', columns='toko', values='omzet')
m = w.reset_index().melt(id_vars='bulan', var_name='toko', value_name='omzet')
m3 = m.sort_values(['bulan', 'toko']).reset_index(drop=True)
print(m3.equals(df[['bulan', 'toko', 'omzet']]))
s = df.set_index(['bulan', 'toko'])['omzet']
print(s.unstack().values.tolist())
print(s.unstack(0).values.tolist())
print(s.unstack(0).index.tolist())
print(w.stack().to_dict())
print(w.T.values.tolist(), w.T.index.tolist())
"""),
            ind("""
True
[[100, 80], [120, 90], [130, 70]]
[[100, 120, 130], [80, 90, 70]]
['A', 'B']
{(1, 'A'): 100, (1, 'B'): 80, (2, 'A'): 120, (2, 'B'): 90, (3, 'A'): 130, (3, 'B'): 70}
[[100, 120, 130], [80, 90, 70]] ['A', 'B']
"""),
            "Pivot lalu melt mengembalikan tabel asal setelah diurutkan. Stack dan unstack memutar tingkat indeks, dan T menukar baris dan kolom.",
            filename="stack_unstack.py",
        ),
        tb("stack dan unstack", "Metode `stack` memindahkan kolom ke dalam indeks bertingkat, dan `unstack` memindahkan satu tingkat indeks ke kolom. Keduanya bekerja pada indeks, berbeda dari `melt` dan `pivot` yang bekerja pada kolom. Pada Series dengan indeks ganda, `unstack(0)` memutar tingkat pertama dan `unstack(1)` tingkat kedua, dan hasilnya berbeda orientasi. `stack` secara bawaan membuang NaN. Bila indeks Anda sudah bermakna, keduanya lebih ringkas daripada melt dan pivot, tetapi bila kunci masih berupa kolom, melt dan pivot lebih mudah dibaca."),
        tb("Transpos", "Atribut `T` menukar baris dan kolom, dan sering berguna bila tabel lebar terlalu lebar untuk dibaca. Ia berbeda dari pivot karena tidak mengubah isi atau bentuk logis tabel, hanya memutarnya. Waspadai tipe data: transpos tabel bertipe campuran menghasilkan kolom bertipe object sehingga sifat numeriknya hilang. Gunakan transpos untuk tampilan, bukan sebagai langkah dalam alur hitung, dan hindari pada tabel besar karena membuat salinan lengkap yang boros memori."),
        tb("Bolak-balik adalah normal", "Pivot dan melt adalah operasi yang saling membalik bila datanya unik. Anda dapat melelehkan tabel lebar menjadi panjang, menghitung dengan groupby, lalu memivotkannya kembali untuk tampilan. Pola ini begitu umum sehingga layak dilatih sampai otomatis. Bila hasil bolak-balik tidak sama dengan tabel asal setelah diurutkan, biasanya ada duplikat yang diagregasi, kolom yang tidak disebut dan terbuang, atau nilai hilang yang ikut terbuang oleh stack. Mengujinya dengan `equals` adalah cara cepat untuk memastikan tidak ada informasi yang hilang."),
        tb("Kolom bernama berpola", "Kadang kolom lebar bernama berpola, misalnya `skor_2021`, `skor_2022`, `skor_2023`. Melt saja belum cukup karena nama kolom memuat dua informasi, jenis ukuran dan tahun. Fungsi `pd.wide_to_long` memecah awalan dan akhiran itu menjadi dua kolom sekaligus. Alternatifnya, lelehkan dulu lalu pecah kolom variable dengan `str.split` atau `str.extract`. Pola ini sering muncul pada data survei dan data deret waktu yang diekspor dari spreadsheet, dan menguasainya menghemat banyak jam pembersihan manual."),
        K("tip", "Setelah melt, beri var_name dan value_name yang bermakna dan urutkan hasilnya bila urutan penting.", title="Beri nama"),
        tb("Memecah nama kolom berpola", "Pada data survei atau keuangan, nama kolom sering memuat dua informasi sekaligus, misalnya `skor_2021` dan `skor_2022`. Setelah melt, kolom `variable` berisi teks gabungan itu, dan langkah berikutnya memecahnya menjadi kolom terpisah dengan `str.split('_').str[1]` atau `str.extract` dengan ekspresi reguler. Kolom tahun yang baru dapat diubah menjadi bilangan bulat dengan `astype(int)` sehingga bisa diurutkan dan dikelompokkan dengan benar. Pola ini mengubah tabel dengan puluhan kolom bernama aneh menjadi tabel rapi dengan satu kolom tahun dan satu kolom nilai."),
        C(
            P("""
d = pd.DataFrame({'id': [1, 2], 'skor_2021': [5, 6], 'skor_2022': [7, 8]})
m = d.melt(id_vars='id')
m['tahun'] = m['variable'].str.split('_').str[1].astype(int)
print(m['tahun'].tolist())
print(m.groupby('tahun')['value'].sum().to_dict())
print(m['variable'].str.extract(r'_(\\d+)')[0].astype(int).tolist())
wl = pd.wide_to_long(pd.DataFrame({'id': [1, 2], 'v1': [5, 6], 'v2': [7, 8]}), 'v', 'id', 't').reset_index()
print(wl.values.tolist())
"""),
            ind("""
[2021, 2021, 2022, 2022]
{2021: 11, 2022: 15}
[2021, 2021, 2022, 2022]
[[1, 1, 5], [2, 1, 6], [1, 2, 7], [2, 2, 8]]
"""),
            "Pecah nama kolom hasil melt menjadi kolom baru, atau pakai wide_to_long untuk pola awalan dan akhiran.",
            filename="melt_berpola.py",
        ),
        tb("Memeriksa hasil melt", "Setelah melt, lakukan tiga pemeriksaan. Pertama, jumlah baris harus sama dengan baris asal dikali jumlah kolom lelehan. Kedua, kolom pengenal tidak boleh kehilangan nilai. Ketiga, jumlah seluruh nilai sebelum dan sesudah harus sama, sehingga `wide[kolom].sum().sum()` sama dengan `m['omzet'].sum()`. Pemeriksaan ketiga menangkap kolom yang tanpa sengaja ikut terlelehkan padahal bukan angka, atau baris yang terbuang. Memasukkan ketiganya sebagai `assert` di akhir fungsi pembersihan menjadikan kesalahan terdeteksi saat terjadi, bukan ketika grafik terlihat aneh."),
        tb("Dari spreadsheet ke analisis", "Skenario klasik: laporan spreadsheet dengan satu baris per produk dan kolom per bulan, ditambah baris total di bawah dan kolom total di kanan. Sebelum melt, buang baris dan kolom total, karena total adalah turunan, bukan pengamatan. Bila ikut terlelehkan, jumlah akan terhitung ganda dalam agregasi berikutnya. Setelah dilelehkan, ubah teks bulan menjadi tanggal sungguhan dengan `to_datetime`, sehingga deret waktu dapat diurutkan dan digambar. Seluruh alur ini adalah pekerjaan harian seorang analis data."),
        E(
            "B2-08-2-ex1",
            "mudah",
            "Tulis fungsi `melt_panjang(wide)` yang melelehkan tabel lebar dengan `bulan` sebagai pengenal menjadi kolom `toko` dan `omzet`, dan mengembalikan `values.tolist()`.",
            ind("""
import pandas as pd

def melt_panjang(wide):
    # TODO: implementasikan
    pass
"""),
            P("""
wide = df.pivot(index='bulan', columns='toko', values='omzet').reset_index()
assert melt_panjang(wide) == [[1, 'A', 100], [2, 'A', 120], [3, 'A', 130], [1, 'B', 80], [2, 'B', 90], [3, 'B', 70]]
assert melt_panjang(wide.iloc[:1]) == [[1, 'A', 100], [1, 'B', 80]]
assert len(melt_panjang(wide)) == 6
assert melt_panjang(wide[['bulan', 'A']]) == [[1, 'A', 100], [2, 'A', 120], [3, 'A', 130]]
"""),
            "melt dengan id_vars bulan, var_name toko, value_name omzet.",
            X(G11),
        ),
        E(
            "B2-08-2-ex2",
            "sedang",
            "Tulis fungsi `melt_sebagian(wide, kolom)` yang melelehkan hanya kolom dalam list `kolom` dengan `bulan` sebagai pengenal, menamai hasil `toko` dan `omzet`, dan mengembalikan `values.tolist()`.",
            ind("""
import pandas as pd

def melt_sebagian(wide, kolom):
    # TODO: implementasikan
    pass
"""),
            P("""
wide = df.pivot(index='bulan', columns='toko', values='omzet').reset_index()
assert melt_sebagian(wide, ['A']) == [[1, 'A', 100], [2, 'A', 120], [3, 'A', 130]]
assert melt_sebagian(wide, ['B']) == [[1, 'B', 80], [2, 'B', 90], [3, 'B', 70]]
assert len(melt_sebagian(wide, ['A', 'B'])) == 6
assert melt_sebagian(wide.iloc[[2]], ['B']) == [[3, 'B', 70]]
"""),
            "melt dengan value_vars.",
            X(G12),
        ),
        E(
            "B2-08-2-ex3",
            "sedang",
            "Tulis fungsi `tumpuk_dict(w)` yang menerima tabel lebar berindeks `bulan` dan berkolom `toko`, menumpuknya dengan `stack`, dan mengembalikan dict `{(bulan, toko): omzet}`.",
            ind("""
import pandas as pd

def tumpuk_dict(w):
    # TODO: implementasikan
    pass
"""),
            P("""
w = df.pivot(index='bulan', columns='toko', values='omzet')
assert tumpuk_dict(w) == {(1, 'A'): 100, (1, 'B'): 80, (2, 'A'): 120, (2, 'B'): 90, (3, 'A'): 130, (3, 'B'): 70}
assert tumpuk_dict(w.iloc[:1]) == {(1, 'A'): 100, (1, 'B'): 80}
assert tumpuk_dict(w[['A']]) == {(1, 'A'): 100, (2, 'A'): 120, (3, 'A'): 130}
assert len(tumpuk_dict(w)) == 6
"""),
            "stack lalu ubah ke dict.",
            X(G13),
        ),
        E(
            "B2-08-2-ex4",
            "menantang",
            "Tulis fungsi `melt_kuartal(wd)` yang melelehkan tabel dengan pengenal `id` menjadi kolom `kuartal` dan `nilai`, mengurutkan menurut `id` lalu `kuartal`, dan mengembalikan `values.tolist()`.",
            ind("""
import pandas as pd

def melt_kuartal(wd):
    # TODO: implementasikan
    pass
"""),
            P("""
wd = pd.DataFrame({'id': [1, 2], 'q1': [5, 6], 'q2': [7, 8]})
assert melt_kuartal(wd) == [[1, 'q1', 5], [1, 'q2', 7], [2, 'q1', 6], [2, 'q2', 8]]
assert melt_kuartal(wd[['id', 'q1']]) == [[1, 'q1', 5], [2, 'q1', 6]]
assert melt_kuartal(wd.iloc[[1]]) == [[2, 'q1', 6], [2, 'q2', 8]]
assert len(melt_kuartal(wd)) == 4
"""),
            "melt lalu sort_values pada dua kolom.",
            X(G14),
        ),
    ],
    [
        M("Melelehkan tanpa var_name dan value_name.", "Beri nama bermakna sejak awal."),
        M("Bergantung pada urutan baris hasil melt.", "Urutkan dengan sort_values sebelum membandingkan."),
        M("Melelehkan seratus kolom pada tabel raksasa.", "Hitung dulu ukuran hasil dan saring kolom."),
    ],
    [
        Q("melt mengubah?", ["Kolom menjadi baris", "Baris menjadi kolom", "Indeks menjadi nama", "Tipe data"], 0, "Lebar ke panjang.", hint="Kolom."),
        Q("id_vars adalah kolom yang?", ["Dipertahankan", "Dilelehkan", "Dibuang", "Diurutkan"], 0, "Pengenal.", hint="Tetap."),
        Q("unstack memindahkan?", ["Indeks ke kolom", "Kolom ke indeks", "Baris ke sel", "Nama ke nilai"], 0, "Putar indeks.", hint="Indeks."),
        Q("Hasil melt dari 3 baris dan 2 kolom lelehan?", ["6 baris", "5 baris", "3 baris", "2 baris"], 0, "Kali.", hint="Perkalian."),
        Q("Data rapi: tiap variabel dalam?", ["Satu kolom", "Satu baris", "Satu sel", "Satu tabel"], 0, "Tidy.", hint="Kolom."),
    ],
    [
        "melt mengubah tabel lebar menjadi panjang.",
        "id_vars, value_vars, var_name, dan value_name mengatur hasil.",
        "stack dan unstack bekerja pada indeks.",
        "Pivot dan melt saling membalik untuk data unik.",
    ],
    [],
)

H11 = """
import pandas as pd

def total_baris(w):
    return w.sum(axis=1).to_dict()
"""
H12 = """
import pandas as pd

def toko_terbaik(w):
    return w.idxmax(axis=1).tolist()
"""
H13 = """
import pandas as pd

def porsi_toko(w):
    return w.div(w.sum(axis=1), axis=0).round(3).values.tolist()
"""
H14 = """
import pandas as pd

def perubahan_bulanan(w):
    return w.diff().fillna(0).values.tolist()
"""

l3 = lesson(
    "B2-08-3",
    "Menganalisis tabel lebar dan memilih bentuk",
    35,
    [
        "Menghitung total, rata-rata, dan puncak antar kolom pada tabel lebar",
        "Menghitung porsi dan perubahan dengan operasi sejajar",
        "Memilih bentuk panjang atau lebar menurut tugas",
        "Merancang alur analisis yang bolak-balik dengan rapi",
    ],
    [
        tb("Kekuatan bentuk lebar", "Setelah pivot, banyak pertanyaan berubah menjadi operasi satu baris. Total tiap bulan adalah jumlah sepanjang baris, toko terbaik tiap bulan adalah kolom dengan nilai terbesar pada baris itu, dan selisih antar bulan adalah perbedaan baris berurutan. Operasi seperti ini hanya satu baris kode pada tabel lebar tetapi memerlukan groupby dan transform pada tabel panjang. Itulah alasan analis sering memivotkan data sementara hanya untuk menghitung, lalu kembali ke bentuk panjang bila diperlukan untuk visualisasi atau penyimpanan."),
        tb("Arah operasi dengan axis", "Hampir semua metode agregasi memiliki argumen `axis`. Nilai nol, bawaan, menghitung sepanjang baris untuk tiap kolom sehingga menghasilkan satu angka per kolom, sedangkan nilai satu menghitung sepanjang kolom untuk tiap baris dan menghasilkan satu angka per baris. Pemula sering terbalik karena `axis=1` berarti hasil per baris, bukan per kolom. Untuk menghafalnya, bayangkan axis sebagai arah yang runtuh: `axis=0` meruntuhkan baris, `axis=1` meruntuhkan kolom. Saat ragu, jalankan pada tabel kecil dan lihat bentuk hasilnya sebelum menerapkan pada data besar."),
        C(
            P("""
w = df.pivot(index='bulan', columns='toko', values='omzet')
print(w.sum().to_dict())
print(w.sum(axis=1).to_dict())
print(w.mean().round(1).to_dict())
print(w.idxmax(axis=1).tolist())
print(w.idxmax().to_dict())
print(w.add_prefix('toko_').columns.tolist())
"""),
            ind("""
{'A': 350, 'B': 240}
{1: 180, 2: 210, 3: 200}
{'A': 116.7, 'B': 80.0}
['A', 'A', 'A']
{'A': 3, 'B': 2}
['toko_A', 'toko_B']
"""),
            "Axis nol meringkas per kolom dan axis satu per baris. Idxmax memberi label nilai terbesar.",
            filename="axis_lebar.py",
        ),
        tb("Porsi dengan div dan axis", "Untuk porsi tiap toko terhadap total bulan, bagi tiap baris dengan jumlah barisnya: `w.div(w.sum(axis=1), axis=0)`. Argumen `axis=0` pada `div` memberi tahu pandas untuk menyejajarkan pembagi menurut indeks, yaitu satu pembagi per baris. Tanpa itu, pandas mencoba menyejajarkan menurut nama kolom dan menghasilkan NaN penuh. Ini jebakan broadcasting yang sama dengan NumPy tetapi lebih berbahaya karena tidak ada pesan galat. Hasilnya, porsi toko A bulan satu 0,556 dan toko B 0,444, dan tiap baris berjumlah satu."),
        tb("Perubahan antar periode", "Metode `diff` menghitung selisih dengan baris sebelumnya dan `pct_change` menghitung perubahan relatif. Keduanya menghasilkan NaN pada baris pertama karena belum ada pembanding. Pada tabel lebar, keduanya menghitung per kolom sekaligus, sehingga satu perintah memberi pertumbuhan tiap toko. Pastikan baris terurut menurut waktu sebelum memakainya, karena fungsi ini mengandalkan urutan baris. Pada contoh, toko A naik 20 lalu 10, sedangkan toko B naik 10 lalu turun 20, kontras yang langsung terlihat dari tabel selisih."),
        C(
            P("""
w = df.pivot(index='bulan', columns='toko', values='omzet')
print(w.div(w.sum(axis=1), axis=0).round(3).values.tolist())
print(w.diff().values.tolist())
print(w.pct_change().round(3).values.tolist())
print(w.diff().fillna(0).values.tolist())
print(w.loc[2:, :].values.tolist(), w.loc[:, 'A'].tolist())
"""),
            ind("""
[[0.556, 0.444], [0.571, 0.429], [0.65, 0.35]]
[[nan, nan], [20.0, 10.0], [10.0, -20.0]]
[[nan, nan], [0.2, 0.125], [0.083, -0.222]]
[[0.0, 0.0], [20.0, 10.0], [10.0, -20.0]]
[[120, 90], [130, 70]] [100, 120, 130]
"""),
            "Div dengan axis nol menyejajarkan pembagi menurut baris. Diff dan pct_change menghitung perubahan per kolom.",
            filename="porsi_perubahan.py",
        ),
        tb("Kapan memilih panjang", "Pilih bentuk panjang bila Anda akan memakai groupby, menggambar dengan seaborn atau plotly, menyimpan ke basis data, atau menambah kategori baru tanpa mengubah skema tabel. Satu kolom `toko` dapat menampung seribu toko tanpa mengubah kode, sedangkan bentuk lebar memerlukan seribu kolom. Bentuk panjang juga lebih jarang melibatkan NaN, sebab kombinasi yang tidak ada cukup tidak punya baris. Itu sebabnya sistem pencatatan dan basis data hampir selalu menyimpan data panjang."),
        tb("Kapan memilih lebar", "Pilih bentuk lebar bila Anda akan menampilkan laporan untuk manusia, menghitung operasi antar kolom, memasukkan data ke algoritma pembelajaran mesin yang mengharapkan satu fitur per kolom, atau membuat peta panas dan korelasi antar kategori. Matriks fitur untuk scikit-learn adalah bentuk lebar, di mana tiap baris adalah sampel dan tiap kolom adalah fitur. Karena itu, pemodelan hampir selalu berakhir dengan pivot, dan rekayasa fitur sering dimulai dengan melt."),
        tb("Alur kerja yang rapi", "Alur yang sehat: simpan dan bersihkan data dalam bentuk panjang, putar ke lebar tepat saat butuh operasi antar kolom atau tampilan, lalu putar kembali bila perlu. Beri nama kolom bermakna di setiap putaran, simpan tabel perantara dengan nama yang menjelaskan bentuknya seperti `omzet_panjang` dan `omzet_lebar`, dan periksa jumlah baris dan kolom setelah setiap perubahan bentuk. Kesalahan bentuk menghasilkan angka yang tampak wajar, sehingga pemeriksaan ukuran adalah pengaman termurah."),
        tb("Ringkasan modul", "Anda telah belajar membedakan data panjang dan lebar, memutar dengan pivot dan pivot_table, melelehkan dengan melt, memutar indeks dengan stack dan unstack, dan memakai tabel lebar untuk operasi antar kolom. Prinsipnya: pilih bentuk menurut tugas, jangan bergantung pada urutan, beri nama jelas, dan periksa ukuran setelah tiap perubahan bentuk. Modul berikutnya membahas data deret waktu di pandas."),
        K("tip", "Setelah tiap perubahan bentuk, cetak shape dan beberapa baris. Kesalahan bentuk menghasilkan angka yang tampak wajar.", title="Periksa ukuran"),
        tb("Peringkat dan kumulatif", "Pada tabel lebar, `rank(axis=1)` memberi peringkat tiap kolom dalam satu baris, misalnya peringkat toko tiap bulan, dan `cumsum` menjumlahkan kumulatif sepanjang baris untuk tiap kolom, misalnya omzet berjalan tiap toko. Keduanya satu baris kode pada bentuk lebar. Pada bentuk panjang, hal yang sama memerlukan groupby dengan rank dan cumsum. Memilih bentuk yang menyederhanakan kode adalah keterampilan praktis: jangan ragu memutar tabel hanya untuk satu perhitungan, selama Anda memeriksa ukuran dan mengingat bentuk mana yang sedang dipegang."),
        C(
            P("""
w = df.pivot(index='bulan', columns='toko', values='omzet')
print(w.cumsum().values.tolist())
print(w.rank(axis=1, ascending=False).values.tolist())
print(w.max().to_dict())
print((w['A'] - w['B']).tolist())
print((w['A'] > w['B']).all())
print(w.agg(['min', 'max']).values.tolist())
"""),
            ind("""
[[100, 80], [220, 170], [350, 240]]
[[1.0, 2.0], [1.0, 2.0], [1.0, 2.0]]
{'A': 130, 'B': 90}
[20, 30, 60]
True
[[100, 70], [130, 90]]
"""),
            "Cumsum, rank, dan selisih antar kolom ditulis ringkas pada tabel lebar. Agg dengan list memberi beberapa ringkasan sekaligus.",
            filename="lebar_lanjut.py",
        ),
        tb("Selisih antar kolom", "Mengurangkan satu kolom dari kolom lain, misalnya `w['A'] - w['B']`, memberi keunggulan toko A terhadap B tiap bulan. Operasi antar kolom sejajar menurut indeks sehingga tidak perlu perulangan. Hasilnya Series yang dapat ditambahkan kembali sebagai kolom turunan, dibandingkan dengan `all` atau `any`, atau digambar sebagai garis. Pada contoh, keunggulan A naik dari 20 menjadi 30 lalu 60, pola yang akan sulit terlihat bila data masih panjang dan tersebar di dua baris per bulan."),
        tb("Menggambar dari dua bentuk", "Metode `plot` pandas pada tabel lebar menggambar satu garis per kolom secara otomatis, dengan indeks sebagai sumbu x. Itu cara tercepat untuk grafik eksplorasi. Seaborn dan plotly menginginkan bentuk panjang, dengan kolom `toko` untuk argumen `hue`. Jadi pilihan bentuk juga ditentukan oleh pustaka grafik yang Anda pakai. Pengalaman praktis: lakukan perhitungan di bentuk lebar, lalu lelehkan hasilnya sebelum memberikannya ke seaborn untuk gambar akhir yang rapi."),
        tb("Kesalahan umum pada reshape", "Beberapa kesalahan berulang perlu diwaspadai. Pertama, memakai pivot pada data yang tidak unik. Kedua, lupa reset_index sehingga kunci tersembunyi di indeks dan hilang saat disimpan. Ketiga, salah axis sehingga operasi bekerja pada arah yang keliru. Keempat, mengabaikan NaN yang muncul dari kombinasi yang tidak ada. Kelima, bergantung pada urutan baris atau kolom bawaan. Kelima kesalahan ini jarang menimbulkan galat, hanya angka yang keliru, sehingga pemeriksaan ukuran dan jumlah total adalah kebiasaan yang paling berharga."),
        tb("Mengaudit perubahan bentuk", "Cara audit yang sederhana: bandingkan total keseluruhan sebelum dan sesudah. Jumlah omzet pada tabel panjang adalah 590 dan harus sama dengan jumlah seluruh sel pada tabel lebar. Bandingkan juga jumlah nilai tidak hilang. Bila total berbeda, ada nilai yang terbuang atau terhitung ganda. Satu pernyataan `assert` pada total ini mengunci perilaku yang benar dan menjadi dokumentasi hidup tentang apa yang seharusnya dipertahankan oleh transformasi."),
        E(
            "B2-08-3-ex1",
            "mudah",
            "Tulis fungsi `total_baris(w)` yang mengembalikan dict jumlah nilai sepanjang baris tabel lebar, dengan indeks sebagai kunci.",
            ind("""
import pandas as pd

def total_baris(w):
    # TODO: implementasikan
    pass
"""),
            P("""
w = df.pivot(index='bulan', columns='toko', values='omzet')
assert total_baris(w) == {1: 180, 2: 210, 3: 200}
assert total_baris(w.iloc[:1]) == {1: 180}
assert total_baris(w[['A']]) == {1: 100, 2: 120, 3: 130}
assert sum(total_baris(w).values()) == 590
"""),
            "sum dengan axis satu.",
            X(H11),
        ),
        E(
            "B2-08-3-ex2",
            "sedang",
            "Tulis fungsi `toko_terbaik(w)` yang mengembalikan list nama kolom dengan nilai terbesar pada tiap baris.",
            ind("""
import pandas as pd

def toko_terbaik(w):
    # TODO: implementasikan
    pass
"""),
            P("""
w = df.pivot(index='bulan', columns='toko', values='omzet')
assert toko_terbaik(w) == ['A', 'A', 'A']
w2 = w.copy()
w2.loc[3] = [50, 90]
assert toko_terbaik(w2) == ['A', 'A', 'B']
assert toko_terbaik(w.iloc[:1]) == ['A']
assert toko_terbaik(w[['B']]) == ['B', 'B', 'B']
"""),
            "idxmax dengan axis satu.",
            X(H12),
        ),
        E(
            "B2-08-3-ex3",
            "sedang",
            "Tulis fungsi `porsi_toko(w)` yang mengembalikan `values.tolist()` porsi tiap sel terhadap jumlah barisnya, dibulatkan tiga desimal.",
            ind("""
import pandas as pd

def porsi_toko(w):
    # TODO: implementasikan
    pass
"""),
            P("""
w = df.pivot(index='bulan', columns='toko', values='omzet')
assert porsi_toko(w) == [[0.556, 0.444], [0.571, 0.429], [0.65, 0.35]]
assert porsi_toko(w.iloc[:1]) == [[0.556, 0.444]]
assert porsi_toko(w[['A']]) == [[1.0], [1.0], [1.0]]
assert all(abs(sum(r) - 1) < 0.01 for r in porsi_toko(w))
"""),
            "div dengan jumlah baris dan axis nol.",
            X(H13),
        ),
        E(
            "B2-08-3-ex4",
            "menantang",
            "Tulis fungsi `perubahan_bulanan(w)` yang mengembalikan `values.tolist()` selisih tiap baris terhadap baris sebelumnya, dengan baris pertama diisi nol.",
            ind("""
import pandas as pd

def perubahan_bulanan(w):
    # TODO: implementasikan
    pass
"""),
            P("""
w = df.pivot(index='bulan', columns='toko', values='omzet')
assert perubahan_bulanan(w) == [[0.0, 0.0], [20.0, 10.0], [10.0, -20.0]]
assert perubahan_bulanan(w.iloc[:1]) == [[0.0, 0.0]]
assert perubahan_bulanan(w[['A']]) == [[0.0], [20.0], [10.0]]
assert perubahan_bulanan(w)[0] == [0.0, 0.0]
"""),
            "diff lalu fillna nol.",
            X(H14),
        ),
    ],
    [
        M("Terbalik memahami axis.", "Axis satu menghasilkan satu angka per baris."),
        M("Memakai div tanpa axis nol.", "Beri axis nol agar pembagi sejajar menurut baris."),
        M("Mengubah bentuk tanpa memeriksa ukuran.", "Cetak shape setelah tiap perubahan."),
    ],
    [
        Q("axis=1 pada sum menghasilkan?", ["Satu angka per baris", "Per kolom", "Satu angka", "Tabel"], 0, "Runtuhkan kolom.", hint="Baris."),
        Q("idxmax axis=1 memberi?", ["Label kolom terbesar per baris", "Nilai terbesar", "Indeks baris", "Rata-rata"], 0, "Label.", hint="Kolom."),
        Q("Matriks fitur scikit-learn berbentuk?", ["Lebar", "Panjang", "Bertingkat", "Dict"], 0, "Satu fitur per kolom.", hint="Lebar."),
        Q("Seaborn paling suka bentuk?", ["Panjang", "Lebar", "Transpos", "Acak"], 0, "Satu kolom per variabel.", hint="Panjang."),
        Q("diff baris pertama?", ["NaN", "0", "1", "Galat"], 0, "Tak ada pembanding.", hint="NaN."),
    ],
    [
        "Tabel lebar memudahkan operasi antar kolom dan tampilan laporan.",
        "Axis menentukan arah penghitungan.",
        "Bentuk panjang cocok untuk groupby dan visualisasi.",
        "Periksa ukuran setelah tiap perubahan bentuk.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perintah yang cukup jelas dalam teks.", "brief": []}

write_module(
    "B2",
    8,
    "Pivot, melt, dan reshape",
    105,
    [
        "Memutar data dengan pivot dan pivot_table",
        "Melelehkan tabel lebar dengan melt serta memakai stack dan unstack",
        "Memilih bentuk panjang atau lebar menurut tugas analisis",
    ],
    [l1, l2, l3],
    video,
    REF,
)
