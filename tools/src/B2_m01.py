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
import pandas as pd

def seri_dari_dict(d):
    return pd.Series(d).sort_index()
"""
F2 = """
import pandas as pd

def jumlah_selaras(a, b):
    return pd.Series(a).add(pd.Series(b), fill_value=0).sort_index().tolist()
"""
F3 = """
import pandas as pd

def tiga_teratas(s):
    return s.sort_values(ascending=False).head(3).index.tolist()
"""
F4 = """
import pandas as pd

def frekuensi(daftar):
    return {k: int(v) for k, v in pd.Series(daftar).value_counts().items()}
"""

l1 = lesson(
    "B2-01-1",
    "Series: larik berlabel",
    35,
    [
        "Menjelaskan Series sebagai larik satu dimensi berlabel",
        "Membuat Series dari list dan dict",
        "Mengakses data dengan label dan posisi",
        "Memahami perataan indeks pada operasi antar Series",
    ],
    [
        tb("Mengapa pandas", "NumPy unggul untuk larik angka, tetapi data nyata hampir selalu berupa tabel dengan nama kolom, tipe campuran, tanggal, dan nilai hilang. Pandas dibangun di atas NumPy untuk menangani data seperti itu. Ia menyediakan dua struktur utama: **Series** untuk satu kolom data berlabel, dan **DataFrame** untuk tabel dua dimensi. Hampir seluruh pekerjaan analisis data dengan Python bertumpu pada keduanya."),
        tb("Apa itu Series", "Series adalah larik satu dimensi yang setiap elemennya punya label, disebut **indeks**. Ia memiliki tiga bagian: nilai, indeks, dan secara opsional nama. Nilai disimpan sebagai array NumPy sehingga operasi vectorized tetap cepat. Indeks membuat kita dapat mengakses data dengan nama bermakna, misalnya kode produk atau tanggal, bukan hanya nomor posisi."),
        C(
            ind("""
import pandas as pd

s = pd.Series([10, 20, 30], index=['a', 'b', 'c'], name='nilai')
print(s.tolist())
print(s.index.tolist())
print(s.dtype)
print(s.name)
print(len(s), s.shape)
print((s * 2).tolist())
"""),
            ind("""
[10, 20, 30]
['a', 'b', 'c']
int64
nilai
3 (3,)
[20, 40, 60]
"""),
            "Series menyimpan nilai, indeks, dan nama. Operasi aritmetika bekerja pada seluruh nilai.",
            filename="series_dasar.py",
        ),
        tb("Membuat Series", "Series dapat dibuat dari list, array NumPy, atau dict. Dari list, indeks bawaan adalah bilangan nol sampai n minus satu. Argumen `index` memberi label sendiri. Dari dict, kunci menjadi indeks dan nilai menjadi data, cara yang praktis untuk mengubah hasil hitungan menjadi Series. Tipe data dipilih otomatis dari isi, mirip NumPy, dan daftar berisi nilai hilang menjadi desimal."),
        tb("Akses dengan label dan posisi", "Pandas menyediakan dua cara akses yang berbeda dan penting dibedakan. `s.loc[label]` memilih berdasarkan label indeks, sedangkan `s.iloc[posisi]` memilih berdasarkan nomor posisi mulai dari nol. Slice dengan label pada `loc` menyertakan ujung akhir, sedangkan slice posisi pada `iloc` tidak, sama seperti Python. Menulis kurung siku langsung `s['b']` berfungsi untuk label, tetapi `loc` dan `iloc` lebih jelas dan aman."),
        C(
            ind("""
import pandas as pd

s = pd.Series([10, 20, 30], index=['a', 'b', 'c'])
print(s.loc['b'], s.iloc[0], s.iloc[-1])
print(s.loc['a':'b'].tolist())
print(s.iloc[0:2].tolist())
print(s[s > 15].index.tolist())
print(s.index.is_unique)
"""),
            ind("""
20 10 30
[10, 20]
[10, 20]
['b', 'c']
True
"""),
            "Loc memakai label dan menyertakan ujung akhir, iloc memakai posisi. Mask boolean menyaring seperti pada NumPy.",
            filename="series_akses.py",
        ),
        tb("Perataan indeks", "Fitur paling khas pandas: operasi antar dua Series meratakan keduanya berdasarkan indeks, bukan posisi. Label yang ada di kedua Series dijumlahkan, sedangkan label yang hanya ada di satu sisi menghasilkan nilai hilang. Ini mencegah kesalahan menjumlahkan baris yang tidak berpasangan, tetapi dapat mengejutkan bila Anda tidak mengharapkannya. Metode seperti `add` dengan `fill_value` memberi kendali atas nilai hilang."),
        C(
            ind("""
import pandas as pd

s = pd.Series([10, 20, 30], index=['a', 'b', 'c'])
t = pd.Series({'a': 1, 'b': 2, 'd': 4})
print((s + t).tolist())
print(int((s + t).isna().sum()))
print(s.add(t, fill_value=0).tolist())
print(sorted(s.add(t, fill_value=0).index.tolist()))
"""),
            ind("""
[11.0, 22.0, nan, nan]
2
[11.0, 22.0, 30.0, 4.0]
['a', 'b', 'c', 'd']
"""),
            "Label c dan d tidak punya pasangan sehingga hasilnya hilang. Add dengan fill_value menganggap yang hilang sebagai nol.",
            filename="series_selaras.py",
        ),
        tb("Ringkasan dan hitungan", "Series mewarisi fungsi ringkasan NumPy: `sum`, `mean`, `max`, `min`, `std`. Metode `describe` memberi ringkasan statistik sekaligus. Untuk data kategori, `value_counts` menghitung kemunculan tiap nilai dan `unique` mengembalikan nilai berbeda. Fungsi `idxmax` dan `idxmin` mengembalikan label, bukan posisi, dari nilai ekstrem, yang sering lebih berguna daripada nilainya sendiri."),
        C(
            ind("""
import pandas as pd

s = pd.Series([10, 20, 30], index=['a', 'b', 'c'])
print(s.sum(), s.mean(), s.max(), s.idxmax())
d = s.describe()
print(d['count'], d['mean'], d['min'], d['max'])
v = pd.Series(['x', 'y', 'x', 'z', 'x'])
vc = v.value_counts()
print(int(vc['x']), v.nunique(), sorted(v.unique().tolist()))
print(int(v.isin(['x']).sum()))
"""),
            ind("""
60 20.0 30 c
3.0 20.0 10.0 30.0
3 3 ['x', 'y', 'z']
3
"""),
            "Describe merangkum statistik, value_counts menghitung frekuensi, dan idxmax memberi label nilai terbesar.",
            filename="series_ringkas.py",
        ),
        tb("Nilai hilang pada Series", "Pandas menyatakan nilai hilang dengan NaN, dan sebagian besar fungsi ringkasan mengabaikannya secara bawaan, berbeda dari NumPy. Metode `isna` menandai nilai hilang, `fillna` mengisinya, dan `dropna` membuangnya. Karena NaN bertipe desimal, kolom bilangan bulat yang memuat nilai hilang menjadi desimal. Tipe `Int64` berhuruf besar menyimpan bilangan bulat dengan nilai hilang, tetapi perlu diminta secara eksplisit."),
        tb("Operasi elemen dan metode string", "Operasi aritmetika, perbandingan, dan fungsi NumPy bekerja langsung pada Series. Untuk teks, atribut `str` menyediakan metode vectorized seperti `str.upper`, `str.strip`, dan `str.len`. Metode `map` menerapkan fungsi atau kamus pada tiap elemen, dan `between` membuat mask rentang. Semuanya mempertahankan indeks sehingga hasilnya tetap selaras dengan data asal."),
        tb("Mengurutkan", "Metode `sort_values` mengurutkan berdasarkan nilai dan `sort_index` berdasarkan label. Keduanya mengembalikan Series baru dan mempertahankan pasangan label dan nilai. Argumen `ascending=False` membalik urutan. Dikombinasikan dengan `head`, `sort_values` menjawab pertanyaan tiga produk terlaris dalam satu baris. Ingat bahwa indeks ikut berpindah, sehingga posisi baris bukan lagi urutan label."),
        tb("Series dan NumPy", "Setiap Series memiliki array NumPy di dalamnya, dapat diakses lewat `to_numpy`. Anda dapat bebas berpindah antara keduanya: lakukan perhitungan berat dengan NumPy, lalu bungkus hasilnya kembali ke Series dengan indeks yang sama. Memahami hubungan ini membuat Anda dapat memakai semua yang dipelajari di kursus NumPy langsung pada data pandas."),
        K("tip", "Pandas meratakan operasi berdasarkan label, bukan posisi. Periksa indeks bila hasil operasi antar Series mengandung banyak nilai hilang.", title="Perataan indeks"),
        tb("Indeks tidak harus unik", "Indeks Series boleh memuat label berulang. Pada kasus itu `loc` dengan label berulang mengembalikan Series berisi semua yang cocok, bukan satu nilai. Properti `index.is_unique` memeriksanya. Indeks tidak unik berguna bagi data seperti beberapa pengukuran per hari, tetapi dapat membuat penugasan dan penggabungan menghasilkan kejutan, jadi periksa sebelum mengandalkan label sebagai kunci."),
        E(
            "B2-01-1-ex1",
            "mudah",
            "Tulis fungsi `seri_dari_dict(d)` yang mengubah dict menjadi `Series` dengan kunci sebagai indeks, lalu mengurutkannya berdasarkan indeks.",
            ind("""
import pandas as pd

def seri_dari_dict(d):
    # TODO: implementasikan
    pass
"""),
            ind("""
import pandas as pd

s = seri_dari_dict({'c': 3, 'a': 1, 'b': 2})
assert s.index.tolist() == ['a', 'b', 'c']
assert s.tolist() == [1, 2, 3]
assert seri_dari_dict({}).shape == (0,)
assert seri_dari_dict({'x': 5}).loc['x'] == 5
"""),
            "pd.Series menerima dict, lalu sort_index.",
            F1.strip("\n"),
        ),
        E(
            "B2-01-1-ex2",
            "sedang",
            "Tulis fungsi `jumlah_selaras(a, b)` yang menerima dua dict, menjumlahkannya sebagai Series dengan label yang tidak berpasangan dianggap nol, dan mengembalikan nilainya sebagai list terurut menurut label.",
            ind("""
import pandas as pd

def jumlah_selaras(a, b):
    # TODO: implementasikan
    pass
"""),
            ind("""
import pandas as pd

assert jumlah_selaras({'a': 1, 'b': 2}, {'b': 3, 'c': 4}) == [1.0, 5.0, 4.0]
assert jumlah_selaras({'a': 1}, {'a': 2}) == [3.0]
assert jumlah_selaras({}, {'z': 9}) == [9.0]
assert jumlah_selaras({'x': 1, 'y': 2}, {}) == [1.0, 2.0]
"""),
            "Metode add dengan fill_value nol.",
            F2.strip("\n"),
        ),
        E(
            "B2-01-1-ex3",
            "sedang",
            "Tulis fungsi `tiga_teratas(s)` yang menerima Series dan mengembalikan list label tiga nilai terbesar, dari yang terbesar.",
            ind("""
import pandas as pd

def tiga_teratas(s):
    # TODO: implementasikan
    pass
"""),
            ind("""
import pandas as pd

s = pd.Series([5, 9, 1, 7], index=['a', 'b', 'c', 'd'])
assert tiga_teratas(s) == ['b', 'd', 'a']
assert tiga_teratas(pd.Series([1, 2], index=['x', 'y'])) == ['y', 'x']
assert tiga_teratas(pd.Series([4, 3, 2, 1])) == [0, 1, 2]
assert len(tiga_teratas(pd.Series(range(10)))) == 3
"""),
            "Urutkan turun lalu ambil tiga pertama dan labelnya.",
            F3.strip("\n"),
        ),
        E(
            "B2-01-1-ex4",
            "menantang",
            "Tulis fungsi `frekuensi(daftar)` yang mengembalikan dict `{nilai: banyak_kemunculan}` dari list `daftar` memakai `value_counts`, dengan banyak kemunculan berupa int Python.",
            ind("""
import pandas as pd

def frekuensi(daftar):
    # TODO: implementasikan
    pass
"""),
            ind("""
import pandas as pd

assert frekuensi(['x', 'y', 'x']) == {'x': 2, 'y': 1}
assert frekuensi([1, 1, 1]) == {1: 3}
assert frekuensi([]) == {}
r = frekuensi(['a', 'b', 'a', 'c', 'a'])
assert r == {'a': 3, 'b': 1, 'c': 1}
assert all(type(v) is int for v in r.values())
"""),
            "Value_counts menghasilkan Series, ubah ke dict dengan int.",
            F4.strip("\n"),
        ),
    ],
    [
        M("Mengira operasi antar Series berdasarkan posisi.", "Operasi berdasarkan label indeks."),
        M("Memakai s[0] dengan indeks label.", "Pakai iloc untuk posisi dan loc untuk label."),
        M("Mengira slice loc tidak menyertakan ujung akhir.", "Slice loc menyertakan ujung akhir."),
    ],
    [
        Q("Series terdiri dari?", ["Nilai, indeks, dan nama", "Hanya nilai", "Hanya indeks", "Dua kolom"], 0, "Tiga bagian.", hint="Label."),
        Q("iloc memilih berdasarkan?", ["Posisi", "Label", "Nilai", "Tipe"], 0, "Nomor urut.", hint="i."),
        Q("Jumlah dua Series dengan label berbeda?", ["NaN pada label tak berpasangan", "Galat", "Nol", "Posisi"], 0, "Perataan.", hint="Label."),
        Q("value_counts menghitung?", ["Kemunculan tiap nilai", "Rata-rata", "Panjang", "Tipe"], 0, "Frekuensi.", hint="Frekuensi."),
        Q("idxmax mengembalikan?", ["Label nilai terbesar", "Nilai terbesar", "Posisi", "Rata-rata"], 0, "Label.", hint="Label."),
    ],
    [
        "Series adalah larik berlabel dengan nilai, indeks, dan nama.",
        "loc memilih dengan label dan iloc dengan posisi.",
        "Operasi antar Series meratakan berdasarkan indeks.",
        "value_counts, describe, dan sort_values meringkas dan mengurutkan.",
    ],
    [],
)

G1 = """
import pandas as pd

def buat_df(nama, umur):
    return pd.DataFrame({'nama': nama, 'umur': umur})
"""
G2 = """
import pandas as pd

def tambah_kolom_dua(df):
    return df.assign(umur2=df['umur'] * 2)
"""
G3 = """
import pandas as pd

def pilih_kolom(df, kolom):
    return df[kolom]
"""
G4 = """
import pandas as pd

def rekap_numerik(df):
    return df.select_dtypes('number').mean().to_dict()
"""

l2 = lesson(
    "B2-01-2",
    "DataFrame: tabel berlabel",
    35,
    [
        "Membuat DataFrame dari dict, list dict, dan list bersarang",
        "Membaca shape, kolom, indeks, dan dtypes",
        "Memilih kolom dan menambah kolom baru",
        "Memakai set_index, rename, dan drop",
    ],
    [
        tb("Apa itu DataFrame", "DataFrame adalah tabel dua dimensi dengan baris berlabel dan kolom bernama. Anda dapat membayangkannya sebagai kumpulan Series yang berbagi indeks sama, satu Series per kolom. Setiap kolom boleh bertipe berbeda: angka, teks, tanggal. Struktur inilah yang paling sering dipakai dalam analisis data karena meniru lembar kerja dan tabel basis data."),
        tb("Membuat dari dict", "Cara paling umum membuat DataFrame adalah dari dict yang kuncinya nama kolom dan nilainya list data kolom. Semua list harus berpanjang sama. Bila dibuat dari list dict, setiap dict menjadi satu baris, dan kunci yang tidak ada pada suatu baris menjadi nilai hilang. Dari list bersarang, berikan nama kolom lewat argumen `columns`. Pilih bentuk sesuai bagaimana data Anda datang."),
        C(
            ind("""
import pandas as pd

d = pd.DataFrame({'nama': ['Ani', 'Budi', 'Cici'], 'umur': [20, 25, 22], 'kota': ['A', 'B', 'A']})
print(d.shape)
print(d.columns.tolist())
print(d.index.tolist())
print(len(d), d.size)
print(d.dtypes['umur'])
print(d.iloc[0].to_dict())
"""),
            ind("""
(3, 3)
['nama', 'umur', 'kota']
[0, 1, 2]
3 9
int64
{'nama': 'Ani', 'umur': 20, 'kota': 'A'}
"""),
            "Shape berisi baris dan kolom. Indeks bawaan berupa nomor urut dan satu baris dapat diambil sebagai dict.",
            filename="dataframe_dasar.py",
        ),
        tb("Membaca struktur", "Atribut `shape` memberi jumlah baris dan kolom, `columns` nama kolom, `index` label baris, dan `dtypes` tipe tiap kolom. Metode `info` mencetak ringkasan tipe dan jumlah nilai tidak hilang, sedangkan `describe` memberi statistik kolom numerik. Dua perintah ini adalah hal pertama yang dijalankan pada data baru, untuk mengenali ukuran, tipe, dan lubang data."),
        tb("Bentuk lain pembuatan", "List dict memudahkan data yang datang sebagai catatan, seperti respons API. List bersarang cocok untuk baris tanpa nama. Metode `to_dict` mengembalikan arah sebaliknya, dengan orient `list` memberi dict kolom dan orient `records` memberi list baris. Mampu berpindah antar bentuk ini membuat DataFrame mudah dihubungkan dengan kode Python biasa dan format JSON."),
        C(
            ind("""
import pandas as pd

a = pd.DataFrame([{'a': 1, 'b': 2}, {'a': 3}])
print(a.to_dict('list'))
b = pd.DataFrame([[1, 2], [3, 4]], columns=['x', 'y'])
print(b.to_dict('list'))
print(b.to_dict('records'))
print(b.values.tolist())
print(b.T.shape)
"""),
            ind("""
{'a': [1, 3], 'b': [2.0, nan]}
{'x': [1, 3], 'y': [2, 4]}
[{'x': 1, 'y': 2}, {'x': 3, 'y': 4}]
[[1, 2], [3, 4]]
(2, 2)
"""),
            "Baris tanpa kunci b menghasilkan nilai hilang, dan kolom b menjadi desimal. To_dict mengubah tabel kembali menjadi struktur Python.",
            filename="dataframe_bentuk.py",
        ),
        tb("Memilih kolom", "Kurung siku dengan satu nama kolom, `df['umur']`, mengembalikan Series. Kurung siku dengan list nama, `df[['nama', 'umur']]`, mengembalikan DataFrame yang lebih kecil. Perbedaan kurung tunggal dan ganda ini sering membingungkan pemula: dua kurung berarti list nama kolom di dalam kurung pemilihan. Akses atribut `df.umur` juga bekerja, tetapi gagal untuk nama dengan spasi atau yang bentrok dengan metode."),
        C(
            ind("""
import pandas as pd

d = pd.DataFrame({'nama': ['Ani', 'Budi', 'Cici'], 'umur': [20, 25, 22], 'kota': ['A', 'B', 'A']})
print(type(d['umur']).__name__)
print(type(d[['umur']]).__name__)
print(d[['nama', 'umur']].shape)
d['umur2'] = d['umur'] * 2
print(d.columns.tolist())
print(d['umur2'].tolist())
"""),
            ind("""
Series
DataFrame
(3, 2)
['nama', 'umur', 'kota', 'umur2']
[40, 50, 44]
"""),
            "Satu nama kolom memberi Series, list nama memberi DataFrame. Menugaskan ke nama baru membuat kolom baru.",
            filename="pilih_kolom.py",
        ),
        tb("Menambah dan mengubah kolom", "Menugaskan ke nama kolom baru menambahkan kolom, dan ke nama yang ada menimpanya. Hasil operasi antar kolom menjadi kolom baru dengan indeks selaras. Metode `assign` melakukan hal yang sama tetapi mengembalikan DataFrame baru tanpa mengubah aslinya, sehingga cocok untuk rangkaian metode. Pilih penugasan untuk skrip sederhana, dan assign bila ingin menghindari efek samping."),
        tb("Indeks sebagai kunci", "Metode `set_index('nama')` memindahkan sebuah kolom menjadi indeks, sehingga baris dapat dicari dengan labelnya lewat `loc`. Kebalikannya, `reset_index` mengembalikan indeks menjadi kolom biasa dan memberi nomor urut baru. Memilih kolom yang unik dan bermakna sebagai indeks memudahkan pencarian dan perataan antar tabel, tetapi indeks tidak harus unik, dan itu dapat menghasilkan kejutan."),
        C(
            ind("""
import pandas as pd

d = pd.DataFrame({'nama': ['Ani', 'Budi', 'Cici'], 'umur': [20, 25, 22]})
i = d.set_index('nama')
print(i.index.tolist(), i.shape)
print(i.loc['Budi', 'umur'])
print(i.reset_index().columns.tolist())
print(d.rename(columns={'nama': 'Nama'}).columns.tolist())
print(d.drop(columns='umur').columns.tolist())
print(d.columns.tolist())
"""),
            ind("""
['Ani', 'Budi', 'Cici'] (3, 1)
25
['nama', 'umur']
['Nama', 'umur']
['nama']
['nama', 'umur']
"""),
            "Set_index memindahkan kolom ke indeks. Rename dan drop mengembalikan tabel baru dan tidak mengubah aslinya.",
            filename="indeks_rename.py",
        ),
        tb("Mengubah nama dan membuang", "Metode `rename(columns={...})` mengubah nama kolom tertentu, dan `drop(columns=[...])` membuang kolom. Keduanya mengembalikan DataFrame baru, bukan mengubah di tempat, sehingga hasilnya harus ditampung. Pola ini konsisten di seluruh pandas: sebagian besar metode mengembalikan objek baru, dan itulah dasar penulisan berantai yang bersih."),
        tb("Statistik kolom", "Metode `describe` pada DataFrame meringkas kolom numerik, dan `select_dtypes` memilih kolom menurut tipe. Gunakan `nunique` untuk jumlah nilai berbeda per kolom, dan `isna().sum()` untuk jumlah nilai hilang per kolom. Rangkaian pemeriksaan singkat ini mengenali kolom konstan, kolom kategori dengan sedikit nilai, dan kolom yang banyak lubangnya sebelum analisis dimulai."),
        tb("Tabel dan NumPy", "Atribut `values` atau metode `to_numpy` mengembalikan isi DataFrame sebagai array NumPy. Bila kolom bertipe campuran, hasilnya bertipe objek yang lambat, jadi pilih kolom numerik lebih dulu. Menyerahkan data ke pustaka seperti scikit-learn biasanya dilakukan dengan cara ini, atau langsung dengan DataFrame karena sebagian besar pustaka menerimanya."),
        K("warn", "Sebagian besar metode pandas mengembalikan objek baru. Tampung hasilnya, atau rename dan drop tidak berpengaruh.", title="Tampung hasilnya"),
        tb("Salinan dan tampilan", "Memilih kolom dengan kurung siku dapat mengembalikan tampilan atau salinan, tergantung konteks internal. Pandas versi baru memakai aturan copy-on-write sehingga mengubah hasil pemilihan tidak memengaruhi tabel asal. Untuk aman pada kode lama, panggil `.copy()` secara eksplisit sebelum mengubah bagian tabel, dan hindari mengubah hasil pemilihan berantai."),
        E(
            "B2-01-2-ex1",
            "mudah",
            "Tulis fungsi `buat_df(nama, umur)` yang membuat DataFrame dengan dua kolom bernama `nama` dan `umur` dari dua list.",
            ind("""
import pandas as pd

def buat_df(nama, umur):
    # TODO: implementasikan
    pass
"""),
            ind("""
import pandas as pd

d = buat_df(['Ani', 'Budi'], [20, 25])
assert d.shape == (2, 2)
assert d.columns.tolist() == ['nama', 'umur']
assert d['umur'].tolist() == [20, 25]
assert buat_df([], []).shape == (0, 2)
"""),
            "Kirim dict dengan dua list ke pd.DataFrame.",
            G1.strip("\n"),
        ),
        E(
            "B2-01-2-ex2",
            "sedang",
            "Tulis fungsi `tambah_kolom_dua(df)` yang mengembalikan DataFrame baru dengan kolom tambahan `umur2` berisi dua kali kolom `umur`. DataFrame asli tidak boleh berubah.",
            ind("""
import pandas as pd

def tambah_kolom_dua(df):
    # TODO: implementasikan
    pass
"""),
            ind("""
import pandas as pd

d = pd.DataFrame({'nama': ['A', 'B'], 'umur': [20, 30]})
r = tambah_kolom_dua(d)
assert r.columns.tolist() == ['nama', 'umur', 'umur2']
assert r['umur2'].tolist() == [40, 60]
assert d.columns.tolist() == ['nama', 'umur']
assert tambah_kolom_dua(d.iloc[0:0]).shape == (0, 3)
"""),
            "Metode assign mengembalikan tabel baru.",
            G2.strip("\n"),
        ),
        E(
            "B2-01-2-ex3",
            "sedang",
            "Tulis fungsi `pilih_kolom(df, kolom)` yang mengembalikan bagian DataFrame yang hanya berisi kolom pada list `kolom`, sebagai DataFrame.",
            ind("""
import pandas as pd

def pilih_kolom(df, kolom):
    # TODO: implementasikan
    pass
"""),
            ind("""
import pandas as pd

d = pd.DataFrame({'a': [1, 2], 'b': [3, 4], 'c': [5, 6]})
r = pilih_kolom(d, ['a', 'c'])
assert isinstance(r, pd.DataFrame)
assert r.columns.tolist() == ['a', 'c']
assert r.shape == (2, 2)
assert pilih_kolom(d, ['b'])['b'].tolist() == [3, 4]
"""),
            "Kurung siku dengan list nama kolom.",
            G3.strip("\n"),
        ),
        E(
            "B2-01-2-ex4",
            "menantang",
            "Tulis fungsi `rekap_numerik(df)` yang mengembalikan dict `{kolom: rata_rata}` hanya untuk kolom bertipe numerik pada `df`.",
            ind("""
import pandas as pd

def rekap_numerik(df):
    # TODO: implementasikan
    pass
"""),
            ind("""
import pandas as pd

d = pd.DataFrame({'nama': ['A', 'B'], 'umur': [20, 30], 'skor': [1.5, 2.5]})
assert rekap_numerik(d) == {'umur': 25.0, 'skor': 2.0}
assert rekap_numerik(pd.DataFrame({'x': ['a', 'b']})) == {}
assert rekap_numerik(pd.DataFrame({'n': [1, 2, 3]})) == {'n': 2.0}
assert list(rekap_numerik(d)) == ['umur', 'skor']
"""),
            "select_dtypes dengan number lalu mean dan to_dict.",
            G4.strip("\n"),
        ),
    ],
    [
        M("Memakai satu kurung untuk memilih banyak kolom.", "Pakai list: df[['a', 'b']]."),
        M("Mengira rename dan drop mengubah tabel asal.", "Tampung hasil yang dikembalikan."),
        M("Membuat DataFrame dari list berbeda panjang.", "Pastikan semua kolom berpanjang sama."),
    ],
    [
        Q("df['a'] mengembalikan?", ["Series", "DataFrame", "List", "Skalar"], 0, "Satu kolom.", hint="Satu."),
        Q("df[['a']] mengembalikan?", ["DataFrame", "Series", "Array", "Skalar"], 0, "List nama.", hint="Dua kurung."),
        Q("shape DataFrame berisi?", ["Baris dan kolom", "Kolom saja", "Tipe", "Indeks"], 0, "Dua angka.", hint="Baris, kolom."),
        Q("assign mengembalikan?", ["DataFrame baru", "None", "Series", "Perubahan di tempat"], 0, "Tanpa efek samping.", hint="Baru."),
        Q("set_index berfungsi?", ["Memindahkan kolom ke indeks", "Mengurutkan", "Menghapus", "Mengubah tipe"], 0, "Indeks.", hint="Indeks."),
    ],
    [
        "DataFrame adalah tabel berlabel, kumpulan Series berbagi indeks.",
        "Satu nama kolom memberi Series, list nama memberi DataFrame.",
        "assign, rename, drop mengembalikan tabel baru.",
        "set_index dan reset_index memindahkan kolom dan indeks.",
    ],
    [],
)

H1 = """
import io
import pandas as pd

def baca_csv(teks):
    return pd.read_csv(io.StringIO(teks))
"""
H2 = """
import io
import pandas as pd

def hitung_hilang(teks):
    df = pd.read_csv(io.StringIO(teks), sep=';', na_values=['-'])
    return int(df.isna().sum().sum())
"""
H3 = """
import io
import pandas as pd

def bulan_dari_teks(teks):
    df = pd.read_csv(io.StringIO(teks), parse_dates=['tgl'])
    return df['tgl'].dt.month.tolist()
"""
H4 = """
import pandas as pd

def ke_csv_teks(df):
    return df.to_csv(index=False)
"""

l3 = lesson(
    "B2-01-3",
    "Membaca dan menulis data",
    35,
    [
        "Membaca CSV dengan read_csv dan opsi pentingnya",
        "Mengatur pemisah, nilai hilang, tanggal, dan indeks saat membaca",
        "Menulis DataFrame ke CSV",
        "Memeriksa data yang baru dibaca",
    ],
    [
        tb("Dari file ke tabel", "Sebagian besar data tiba sebagai file: CSV, Excel, JSON, atau basis data. Fungsi `pd.read_csv` membaca CSV menjadi DataFrame dengan satu panggilan, dan keluarganya `read_excel`, `read_json`, dan `read_sql` melakukan hal serupa untuk format lain. Untuk contoh pada pelajaran ini kita memakai `io.StringIO` agar teks dalam kode berperilaku seperti file, sehingga contoh dapat dijalankan tanpa berkas."),
        C(
            ind("""
import io
import pandas as pd

csv = "id,nama,nilai\\n1,Ani,80\\n2,Budi,\\n3,Cici,90\\n"
r = pd.read_csv(io.StringIO(csv))
print(r.shape)
print(r.columns.tolist())
print(int(r['nilai'].isna().sum()))
print(r['nilai'].dtype)
print(r['id'].dtype)
"""),
            ind("""
(3, 3)
['id', 'nama', 'nilai']
1
float64
int64
"""),
            "Baris pertama menjadi nama kolom. Kolom nilai menjadi desimal karena ada nilai kosong.",
            filename="read_csv_dasar.py",
        ),
        tb("Header dan nama kolom", "Secara bawaan baris pertama dianggap nama kolom. Bila file tidak punya header, beri `header=None` dan nama kolom lewat `names`. Bila ada baris pengantar sebelum header, lewati dengan `skiprows`. Pemeriksaan pertama setelah membaca selalu `shape` dan `columns`, karena kesalahan header membuat seluruh analisis berikutnya bergeser tanpa pesan galat."),
        tb("Pemisah dan nilai hilang", "Tidak semua CSV memakai koma. Data dari lokal tertentu memakai titik koma, dan data lain memakai tab. Atur dengan argumen `sep`. Nilai hilang dapat ditulis macam-macam: kosong, tanda minus, N/A, atau angka khusus seperti sembilan sembilan sembilan. Argumen `na_values` memberi tahu pandas teks mana yang harus dianggap hilang, sehingga kolomnya tetap berupa angka dan bukan teks."),
        C(
            ind("""
import io
import pandas as pd

teks = "a;b\\n1;x\\n2;-\\n3;-\\n"
r = pd.read_csv(io.StringIO(teks), sep=';', na_values=['-'])
print(r.shape)
print(r['b'].isna().tolist())
print(int(r.isna().sum().sum()))
print(r['a'].tolist())
"""),
            ind("""
(3, 2)
[False, True, True]
2
[1, 2, 3]
"""),
            "Pemisah titik koma dibaca dengan sep, dan tanda minus dianggap hilang lewat na_values.",
            filename="sep_na.py",
        ),
        tb("Memilih kolom dan indeks", "Argumen `usecols` membaca hanya kolom yang dibutuhkan, menghemat memori pada file besar. Argumen `index_col` menjadikan satu kolom sebagai indeks. Untuk file yang sangat besar, `nrows` membaca hanya sejumlah baris pertama untuk menjajaki, dan `chunksize` membaca per potongan. Membaca hanya yang perlu adalah optimasi paling sederhana dan efektif."),
        tb("Tanggal", "Secara bawaan kolom tanggal dibaca sebagai teks. Argumen `parse_dates` mengubah kolom tertentu menjadi tipe tanggal sehingga kita dapat mengambil bulan, hari, atau menghitung selisih waktu. Atau ubah setelah dibaca dengan `pd.to_datetime`. Menyimpan tanggal sebagai tipe tanggal, bukan teks, adalah syarat untuk semua analisis deret waktu."),
        C(
            ind("""
import io
import pandas as pd

csv = "id,nilai,tgl\\n1,80,2024-01-05\\n2,70,2024-02-10\\n3,90,2024-03-15\\n"
r = pd.read_csv(io.StringIO(csv), parse_dates=['tgl'], index_col='id')
print(pd.api.types.is_datetime64_any_dtype(r['tgl']))
print(r.index.tolist(), r.columns.tolist())
print(r['tgl'].dt.month.tolist())
k = pd.read_csv(io.StringIO(csv), usecols=['id', 'nilai'])
print(k.columns.tolist())
"""),
            ind("""
True
[1, 2, 3] ['nilai', 'tgl']
[1, 2, 3]
['id', 'nilai']
"""),
            "Parse_dates membuat kolom bertipe tanggal, index_col menjadikan id sebagai indeks, dan usecols membaca kolom terpilih.",
            filename="read_csv_opsi.py",
        ),
        tb("Menulis CSV", "Metode `to_csv` menulis DataFrame ke file, atau ke teks bila tanpa nama file. Secara bawaan indeks ikut ditulis sebagai kolom pertama, yang sering tidak diinginkan, jadi beri `index=False` kecuali indeks bermakna. Untuk Excel gunakan `to_excel`, dan untuk JSON `to_json`. Selalu baca ulang file hasil dengan `read_csv` pada pengujian untuk memastikan bentuknya sama."),
        C(
            ind("""
import io
import pandas as pd

d = pd.DataFrame({'nama': ['A', 'B'], 'umur': [20, 30], 'skor': [1.5, 2.5]})
teks = d.to_csv(index=False)
print(teks.splitlines())
balik = pd.read_csv(io.StringIO(teks))
print(balik.shape, balik.columns.tolist())
print(bool(balik.equals(d)))
"""),
            ind("""
['nama,umur,skor', 'A,20,1.5', 'B,30,2.5']
(2, 3) ['nama', 'umur', 'skor']
True
"""),
            "Tanpa indeks, CSV hanya berisi data. Membaca ulang menghasilkan tabel yang sama.",
            filename="to_csv.py",
        ),
        tb("Inspeksi pertama", "Setelah membaca, lakukan inspeksi rutin: `head` untuk melihat beberapa baris awal, `shape` untuk ukuran, `dtypes` atau `info` untuk tipe, `describe` untuk ringkasan, dan `isna().sum()` untuk nilai hilang. Perhatikan kolom yang seharusnya angka tetapi bertipe teks, tanda bahwa ada nilai tak terduga seperti simbol mata uang atau koma ribuan. Mengatasi masalah di awal menghemat waktu besar kemudian."),
        tb("Mengubah tipe", "Gunakan `astype` untuk mengubah tipe kolom, misalnya ke `float` atau `category`. Untuk teks yang mungkin mengandung sampah, `pd.to_numeric(kolom, errors='coerce')` mengubah yang tidak bisa menjadi NaN, sehingga Anda bisa menghitung berapa yang bermasalah. Tipe `category` menghemat memori besar bagi kolom dengan sedikit nilai berulang, dan mempercepat operasi pengelompokan nanti."),
        tb("Praktik baik", "Jangan mengubah file data mentah. Baca, bersihkan dalam kode, dan tulis hasilnya ke folder lain. Tuliskan opsi `read_csv` secara eksplisit, termasuk tipe kolom penting, agar pembacaan tidak bergantung pada tebakan pandas yang dapat berubah antar versi. Dokumentasikan asal data dan tanggal pengambilan, sehingga analisis dapat diulang dan diaudit sesuai prinsip reproduksibilitas."),
        K("tip", "Setelah membaca data, periksa shape, dtypes, dan jumlah nilai hilang sebelum melakukan hal lain.", title="Inspeksi pertama"),
        tb("Membaca Excel dan JSON", "Selain CSV, `pd.read_excel` membaca lembar Excel dan memerlukan pustaka tambahan seperti openpyxl. `pd.read_json` membaca JSON bentuk tabel, dan untuk JSON bersarang `pd.json_normalize` meratakannya menjadi kolom. Prinsip inspeksi tetap sama untuk semua format: periksa bentuk, tipe, dan nilai hilang segera setelah membaca."),
        tb("Membaca potongan", "Bila file terlalu besar untuk memori, `read_csv` dengan `chunksize` mengembalikan iterator potongan DataFrame. Anda memproses tiap potongan, misalnya menjumlahkan per kelompok, lalu menggabungkan hasil antara. Teknik ini memungkinkan analisis file berukuran gigabyte dengan memori kecil, dengan harga kode yang sedikit lebih rumit."),
        tb("Encoding dan karakter", "File teks dari sistem berbeda dapat memakai encoding yang berbeda, dan salah encoding menghasilkan karakter aneh. Pandas memakai UTF-8 secara bawaan. Bila muncul galat decode atau huruf berantakan, coba `encoding='latin-1'` atau `encoding='cp1252'` untuk file dari Windows lama. Mencatat encoding yang benar dalam dokumentasi data mencegah masalah yang sama berulang."),
        E(
            "B2-01-3-ex1",
            "mudah",
            "Tulis fungsi `baca_csv(teks)` yang membaca teks CSV (dibungkus `io.StringIO`) menjadi DataFrame dengan `pd.read_csv`.",
            ind("""
import io
import pandas as pd

def baca_csv(teks):
    # TODO: implementasikan
    pass
"""),
            ind("""
import pandas as pd

d = baca_csv("id,nama,nilai\\n1,Ani,80\\n2,Budi,\\n")
assert d.shape == (2, 3)
assert d.columns.tolist() == ['id', 'nama', 'nilai']
assert int(d['nilai'].isna().sum()) == 1
assert baca_csv("a\\n1\\n2\\n3\\n")['a'].tolist() == [1, 2, 3]
"""),
            "Bungkus teks dengan io.StringIO lalu pd.read_csv.",
            H1.strip("\n"),
        ),
        E(
            "B2-01-3-ex2",
            "sedang",
            "Tulis fungsi `hitung_hilang(teks)` yang membaca teks CSV berpemisah titik koma, menganggap tanda `-` sebagai nilai hilang, dan mengembalikan jumlah seluruh nilai hilang sebagai int.",
            ind("""
import io
import pandas as pd

def hitung_hilang(teks):
    # TODO: implementasikan
    pass
"""),
            ind("""
import pandas as pd

assert hitung_hilang("a;b\\n1;x\\n2;-\\n3;-\\n") == 2
assert hitung_hilang("a;b\\n1;x\\n") == 0
assert hitung_hilang("a;b\\n-;-\\n") == 2
assert type(hitung_hilang("a;b\\n1;-\\n")) is int
"""),
            "read_csv dengan sep dan na_values lalu jumlahkan isna.",
            H2.strip("\n"),
        ),
        E(
            "B2-01-3-ex3",
            "sedang",
            "Tulis fungsi `bulan_dari_teks(teks)` yang membaca teks CSV berkolom `tgl` bertanggal ISO sebagai tipe tanggal dan mengembalikan list nomor bulan tiap baris.",
            ind("""
import io
import pandas as pd

def bulan_dari_teks(teks):
    # TODO: implementasikan
    pass
"""),
            ind("""
import pandas as pd

assert bulan_dari_teks("tgl\\n2024-01-05\\n2024-03-15\\n") == [1, 3]
assert bulan_dari_teks("id,tgl\\n1,2024-12-31\\n") == [12]
assert bulan_dari_teks("tgl\\n2023-07-01\\n2023-07-31\\n") == [7, 7]
assert len(bulan_dari_teks("tgl\\n2024-02-29\\n")) == 1
"""),
            "parse_dates lalu atribut dt.month.",
            H3.strip("\n"),
        ),
        E(
            "B2-01-3-ex4",
            "menantang",
            "Tulis fungsi `ke_csv_teks(df)` yang mengembalikan teks CSV dari DataFrame `df` tanpa kolom indeks.",
            ind("""
import pandas as pd

def ke_csv_teks(df):
    # TODO: implementasikan
    pass
"""),
            ind("""
import io
import pandas as pd

d = pd.DataFrame({'nama': ['A', 'B'], 'umur': [20, 30]})
t = ke_csv_teks(d)
assert t.splitlines() == ['nama,umur', 'A,20', 'B,30']
assert pd.read_csv(io.StringIO(t)).equals(d)
assert ke_csv_teks(pd.DataFrame({'x': [1]})).splitlines() == ['x', '1']
assert len(ke_csv_teks(d).splitlines()) == 3
"""),
            "to_csv dengan index bernilai False.",
            H4.strip("\n"),
        ),
    ],
    [
        M("Menulis CSV dengan indeks tanpa sadar.", "Pakai index=False kecuali indeks bermakna."),
        M("Membiarkan kolom tanggal bertipe teks.", "Pakai parse_dates atau to_datetime."),
        M("Tidak memeriksa data setelah dibaca.", "Cek shape, dtypes, dan nilai hilang."),
    ],
    [
        Q("Fungsi membaca CSV?", ["pd.read_csv", "pd.open", "np.load", "pd.csv"], 0, "Read csv.", hint="read."),
        Q("Argumen mengatur pemisah?", ["sep", "delim", "split", "col"], 0, "Separator.", hint="sep."),
        Q("na_values berfungsi?", ["Menandai teks sebagai hilang", "Mengisi nilai", "Menghapus baris", "Mengubah tipe"], 0, "Nilai hilang.", hint="Hilang."),
        Q("parse_dates mengubah kolom menjadi?", ["Tipe tanggal", "Teks", "Angka", "Indeks"], 0, "Datetime.", hint="Tanggal."),
        Q("to_csv tanpa kolom indeks memakai?", ["index=False", "header=False", "skip=True", "drop=True"], 0, "Argumen index.", hint="index."),
    ],
    [
        "read_csv membaca CSV dengan opsi pemisah, nilai hilang, tanggal, dan indeks.",
        "usecols dan nrows menghemat memori saat membaca.",
        "to_csv dengan index=False menulis tabel tanpa kolom indeks.",
        "Inspeksi shape, dtypes, dan nilai hilang setelah membaca.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perintah yang cukup jelas dalam teks.", "brief": []}

write_module(
    "B2",
    1,
    "Series dan DataFrame",
    105,
    [
        "Memahami dan membuat Series dan DataFrame",
        "Memilih, menambah, dan mengubah kolom",
        "Membaca dan menulis data dengan opsi yang tepat",
    ],
    [l1, l2, l3],
    video,
    REF,
)
