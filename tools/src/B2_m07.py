import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

DFX = """
import numpy as np
import pandas as pd

pel = pd.DataFrame({
    'id': [1, 2, 3, 4],
    'nama': ['Ani', 'Budi', 'Cici', 'Dedi'],
    'kota': ['Jakarta', 'Bandung', 'Medan', 'Jakarta'],
})
pes = pd.DataFrame({
    'id_pel': [1, 1, 2, 5],
    'total': [100, 150, 200, 300],
})
"""


def tb(h, b):
    return T("## " + h + "\n\n" + b)


def ind(s):
    return textwrap.indent(s.strip("\n"), "            ")


def P(body):
    return ind(DFX + "\n" + textwrap.dedent(body).strip("\n"))


def S(code):
    return ind("import numpy as np\nimport pandas as pd\n\n" + textwrap.dedent(code).strip("\n"))


def X(c):
    return textwrap.dedent(c).strip("\n")


F11 = """
import pandas as pd

def nama_inner(pel, pes):
    m = pel.merge(pes, left_on='id', right_on='id_pel', how='inner')
    return m['nama'].tolist()
"""
F12 = """
import pandas as pd

def total_per_nama(pel, pes):
    m = pel.merge(pes, left_on='id', right_on='id_pel', how='left')
    m['total'] = m['total'].fillna(0)
    return m.groupby('nama')['total'].sum().to_dict()
"""
F13 = """
import pandas as pd

def tanpa_pesanan(pel, pes):
    return pel.loc[~pel['id'].isin(pes['id_pel']), 'nama'].tolist()
"""
F14 = """
import pandas as pd

def id_yatim(pel, pes):
    return pes.loc[~pes['id_pel'].isin(pel['id']), 'id_pel'].tolist()
"""

l1 = lesson(
    "B2-07-1",
    "Menggabung tabel dengan merge",
    35,
    [
        "Memahami kunci gabung dan jenis join",
        "Memakai merge dengan inner, left, right, dan outer",
        "Menggabung kolom kunci yang namanya berbeda",
        "Menemukan baris tanpa pasangan",
    ],
    [
        tb("Data tersebar di banyak tabel", "Data nyata jarang tinggal dalam satu tabel. Identitas pelanggan ada di satu tabel, pesanan di tabel lain, dan produk di tabel ketiga. Untuk menjawab pertanyaan seperti total belanja per kota, tabel-tabel itu harus digabung menurut kunci bersama. Fungsi `merge` pandas melakukan hal yang sama seperti JOIN pada SQL, dan memahami jenis join adalah syarat bekerja dengan data relasional."),
        tb("Data contoh", "Pelajaran ini memakai tabel `pel` berisi empat pelanggan dengan kolom `id`, `nama`, `kota`, dan tabel `pes` berisi empat pesanan dengan kolom `id_pel` dan `total`. Perhatikan bahwa Ani punya dua pesanan, Budi satu, Cici dan Dedi tidak punya, dan satu pesanan atas nama id lima tidak punya pelanggan. Ketidaksempurnaan ini disengaja agar perbedaan jenis join terlihat."),
        C(
            P("""
for how in ['inner', 'left', 'right', 'outer']:
    m = pel.merge(pes, left_on='id', right_on='id_pel', how=how)
    print(how, len(m), m['nama'].tolist(), m['total'].tolist())
print(m.columns.tolist())
"""),
            ind("""
inner 3 ['Ani', 'Ani', 'Budi'] [100, 150, 200]
left 5 ['Ani', 'Ani', 'Budi', 'Cici', 'Dedi'] [100.0, 150.0, 200.0, nan, nan]
right 4 ['Ani', 'Ani', 'Budi', nan] [100, 150, 200, 300]
outer 6 ['Ani', 'Ani', 'Budi', 'Cici', 'Dedi', nan] [100.0, 150.0, 200.0, nan, nan, 300.0]
['id', 'nama', 'kota', 'id_pel', 'total']
"""),
            "Empat jenis join menghasilkan jumlah baris berbeda dari data yang sama.",
            filename="jenis_join.py",
        ),
        tb("Inner join", "Inner join hanya mempertahankan baris yang kuncinya ada di kedua tabel. Ini bawaan `merge`. Hasilnya tiga baris: dua pesanan Ani dan satu pesanan Budi. Cici, Dedi, dan pesanan id lima hilang. Inner join cocok bila Anda hanya peduli pada pasangan yang lengkap, tetapi berbahaya bila Anda mengira semua baris asal selamat, sebab baris tanpa pasangan hilang tanpa peringatan."),
        tb("Left, right, dan outer", "Left join mempertahankan semua baris tabel kiri dan mengisi NaN bila tidak ada pasangan, sehingga Cici dan Dedi muncul dengan total NaN. Right join sebaliknya, mempertahankan seluruh tabel kanan. Outer join mempertahankan semuanya dari kedua sisi. Left join adalah pilihan paling umum dalam analisis karena tabel utama Anda tetap utuh dan tabel lain hanya memperkaya."),
        tb("Satu ke banyak", "Ani punya dua pesanan, sehingga barisnya muncul dua kali dalam hasil. Inilah hubungan satu ke banyak: satu baris di kiri berpasangan dengan beberapa baris di kanan. Jumlah baris hasil dapat melebihi tabel mana pun. Selalu periksa jumlah baris sebelum dan sesudah merge, karena kenaikan tak terduga adalah tanda kunci tidak unik di sisi yang Anda kira unik."),
        C(
            P("""
m = pel.merge(pes, left_on='id', right_on='id_pel', how='left')
print(m['total'].isna().sum(), m[m['total'].isna()]['nama'].tolist())
print(m.groupby('nama')['total'].sum().to_dict())
print(m.groupby('kota')['total'].sum().to_dict())
print(m.drop(columns='id_pel').columns.tolist())
print(m['total'].fillna(0).tolist())
"""),
            ind("""
2 ['Cici', 'Dedi']
{'Ani': 250.0, 'Budi': 200.0, 'Cici': 0.0, 'Dedi': 0.0}
{'Bandung': 200.0, 'Jakarta': 250.0, 'Medan': 0.0}
['id', 'nama', 'kota', 'total']
[100.0, 150.0, 200.0, 0.0, 0.0]
"""),
            "Left join lalu groupby menjawab total per pelanggan dan per kota. Kolom kunci kembar dapat dibuang.",
            filename="left_join_analisis.py",
        ),
        tb("Kunci dengan nama berbeda", "Bila kolom kunci di dua tabel bernama berbeda, pakai `left_on` dan `right_on`. Hasilnya memuat kedua kolom kunci, sehingga satu di antaranya biasanya dibuang dengan `drop`. Bila nama kunci sama di kedua tabel, cukup `on='id'` dan hasilnya hanya memuat satu kolom kunci. Mengganti nama kolom dengan `rename` sebelum merge adalah alternatif yang membuat kode lebih ringkas."),
        tb("Baris tanpa pasangan", "Menemukan baris yang tidak berpasangan sama pentingnya dengan menggabung. Pelanggan tanpa pesanan dapat dicari dengan `~pel['id'].isin(pes['id_pel'])`. Pesanan yatim, yang idnya tidak ada di tabel pelanggan, dicari dengan arah sebaliknya. Kedua pemeriksaan ini menemukan masalah integritas data seperti pesanan atas pelanggan yang dihapus atau kesalahan ketik pada kunci."),
        C(
            P("""
print(pel['id'].isin(pes['id_pel']).tolist())
print(pel.loc[~pel['id'].isin(pes['id_pel']), 'nama'].tolist())
print(pes.loc[~pes['id_pel'].isin(pel['id']), 'id_pel'].tolist())
m = pel.merge(pes, left_on='id', right_on='id_pel', how='outer', indicator=True)
print(m['_merge'].astype(str).tolist())
print(m['_merge'].astype(str).value_counts().to_dict())
"""),
            ind("""
[True, True, False, False]
['Cici', 'Dedi']
[5]
['both', 'both', 'both', 'left_only', 'left_only', 'right_only']
{'both': 3, 'left_only': 2, 'right_only': 1}
"""),
            "Isin menemukan pasangan tanpa merge, dan indicator menandai asal tiap baris hasil.",
            filename="tanpa_pasangan.py",
        ),
        tb("Argumen indicator", "Argumen `indicator=True` menambah kolom `_merge` yang berisi both, left_only, atau right_only untuk tiap baris. Ini cara cepat mengaudit hasil gabung: hitung masing-masing nilai dengan `value_counts` dan bandingkan dengan harapan Anda. Bila left_only jauh lebih banyak dari dugaan, kemungkinan kunci tidak cocok karena beda tipe, spasi tersembunyi, atau perbedaan huruf besar dan kecil."),
        tb("Tipe kunci harus sama", "Kunci yang satu bertipe bilangan bulat dan yang lain teks tidak akan cocok, dan pandas dapat menolak atau memberi hasil kosong. Samakan tipe dengan `astype` sebelum merge. Bersihkan juga teks kunci dengan `str.strip()` dan `str.lower()`. Sebagian besar kegagalan merge dalam praktik berasal dari kunci yang tampak sama tetapi berbeda halus, bukan dari kesalahan sintaks."),
        tb("Hitung baris sebelum dan sesudah", "Biasakan mencetak jumlah baris sebelum dan sesudah merge dan memikirkan apakah angkanya masuk akal. Left join dengan kunci unik di kanan harus mempertahankan jumlah baris kiri persis. Bila bertambah, ada duplikat kunci. Satu pernyataan `assert len(hasil) == len(kiri)` dapat menangkap kesalahan diam-diam yang akan merusak seluruh analisis hilir."),
        K("warn", "Setelah left join, jumlah baris yang bertambah menandakan kunci duplikat di tabel kanan. Periksa sebelum melanjutkan analisis.", title="Awas duplikasi"),
        tb("Merge dan SQL", "Bila Anda mengenal SQL, anggap merge sebagai JOIN. Inner join sama dengan INNER JOIN, left sama dengan LEFT JOIN, dan seterusnya. Perbedaan utamanya, pandas bekerja di memori sehingga cocok untuk data yang muat di RAM, sedangkan basis data cocok untuk data sangat besar."),
        E(
            "B2-07-1-ex1",
            "mudah",
            "Tulis fungsi `nama_inner(pel, pes)` yang menggabung pelanggan dan pesanan dengan inner join pada `id` dan `id_pel`, dan mengembalikan list `nama` hasilnya.",
            ind("""
import pandas as pd

def nama_inner(pel, pes):
    # TODO: implementasikan
    pass
"""),
            P("""
assert nama_inner(pel, pes) == ['Ani', 'Ani', 'Budi']
assert nama_inner(pel.iloc[[2, 3]], pes) == []
assert nama_inner(pel, pes.iloc[[2]]) == ['Budi']
assert len(nama_inner(pel, pes)) == 3
"""),
            "merge dengan left_on id dan right_on id_pel secara inner.",
            X(F11),
        ),
        E(
            "B2-07-1-ex2",
            "sedang",
            "Tulis fungsi `total_per_nama(pel, pes)` yang melakukan left join, mengisi total hilang dengan nol, dan mengembalikan dict jumlah `total` per `nama`.",
            ind("""
import pandas as pd

def total_per_nama(pel, pes):
    # TODO: implementasikan
    pass
"""),
            P("""
assert total_per_nama(pel, pes) == {'Ani': 250.0, 'Budi': 200.0, 'Cici': 0.0, 'Dedi': 0.0}
assert total_per_nama(pel.iloc[[0]], pes) == {'Ani': 250.0}
assert total_per_nama(pel.iloc[[3]], pes) == {'Dedi': 0.0}
assert sum(total_per_nama(pel, pes).values()) == 450.0
"""),
            "Left merge, fillna nol, lalu groupby nama dan sum.",
            X(F12),
        ),
        E(
            "B2-07-1-ex3",
            "sedang",
            "Tulis fungsi `tanpa_pesanan(pel, pes)` yang mengembalikan list `nama` pelanggan yang tidak punya pesanan, tanpa memakai merge.",
            ind("""
import pandas as pd

def tanpa_pesanan(pel, pes):
    # TODO: implementasikan
    pass
"""),
            P("""
assert tanpa_pesanan(pel, pes) == ['Cici', 'Dedi']
assert tanpa_pesanan(pel.iloc[[0, 1]], pes) == []
assert tanpa_pesanan(pel, pes.iloc[[0]]) == ['Budi', 'Cici', 'Dedi']
assert tanpa_pesanan(pel.iloc[[3]], pes) == ['Dedi']
"""),
            "Gunakan isin dengan negasi pada kolom id.",
            X(F13),
        ),
        E(
            "B2-07-1-ex4",
            "menantang",
            "Tulis fungsi `id_yatim(pel, pes)` yang mengembalikan list `id_pel` pada pesanan yang tidak punya pelanggan.",
            ind("""
import pandas as pd

def id_yatim(pel, pes):
    # TODO: implementasikan
    pass
"""),
            P("""
assert id_yatim(pel, pes) == [5]
assert id_yatim(pel.iloc[[0]], pes) == [2, 5]
assert id_yatim(pel, pes.iloc[[0, 1]]) == []
assert id_yatim(pel.iloc[[]], pes) == [1, 1, 2, 5]
"""),
            "Cari id_pel yang tidak ada dalam kolom id pelanggan.",
            X(F14),
        ),
    ],
    [
        M("Memakai inner join lalu heran barisnya berkurang.", "Pakai left join dan periksa baris tanpa pasangan."),
        M("Tidak memeriksa jumlah baris setelah merge.", "Bandingkan jumlah baris dan beri assert."),
        M("Kunci beda tipe atau berspasi.", "Samakan tipe dan bersihkan teks kunci."),
    ],
    [
        Q("Join bawaan merge?", ["inner", "left", "outer", "right"], 0, "Inner.", hint="Irisan."),
        Q("Left join mempertahankan?", ["Semua baris kiri", "Hanya pasangan", "Semua kanan", "Tak satu pun"], 0, "Kiri utuh.", hint="Kiri."),
        Q("Satu ke banyak menyebabkan?", ["Baris kiri berulang", "Baris hilang", "Galat", "Kolom hilang"], 0, "Duplikasi.", hint="Berulang."),
        Q("indicator True menambah kolom?", ["_merge", "_join", "_key", "_side"], 0, "Penanda asal.", hint="_merge."),
        Q("Kunci beda nama memakai?", ["left_on dan right_on", "on saja", "index", "drop"], 0, "Dua nama.", hint="left_on."),
    ],
    [
        "merge menggabung tabel menurut kunci seperti JOIN SQL.",
        "Inner, left, right, dan outer menghasilkan jumlah baris berbeda.",
        "Hubungan satu ke banyak menduplikasi baris sisi satu.",
        "Periksa baris tanpa pasangan dan jumlah baris hasil.",
    ],
    [],
)

G11 = """
import pandas as pd

def jumlah_baris_join(pel, pes, how):
    return len(pel.merge(pes, left_on='id', right_on='id_pel', how=how))
"""
G12 = """
import pandas as pd

def kolom_sufiks(kiri, kanan):
    return kiri.merge(kanan, on='k', suffixes=('_a', '_b')).columns.tolist()
"""
G13 = """
import pandas as pd

def total_kota(pel, pes):
    m = pel.merge(pes, left_on='id', right_on='id_pel', how='left')
    return m.groupby('kota')['total'].sum().to_dict()
"""
G14 = """
import pandas as pd

def asal_baris(pel, pes):
    m = pel.merge(pes, left_on='id', right_on='id_pel', how='outer', indicator=True)
    return m['_merge'].astype(str).tolist()
"""

l2 = lesson(
    "B2-07-2",
    "Kunci ganda, sufiks, dan validasi",
    35,
    [
        "Menggabung dengan lebih dari satu kunci",
        "Mengatasi nama kolom bentrok dengan sufiks",
        "Memvalidasi jenis hubungan dengan validate",
        "Memakai join berbasis indeks",
    ],
    [
        tb("Kunci lebih dari satu kolom", "Kadang satu kolom tidak cukup untuk mengidentifikasi baris. Penjualan per toko dan bulan memerlukan dua kunci. Berikan list ke `on`, misalnya `on=['toko', 'bulan']`, dan pandas mencocokkan baris yang kedua nilainya sama. Pastikan kombinasi itu memang unik di sisi yang Anda harapkan unik, sebab kombinasi ganda yang tidak unik menggandakan baris seperti pada kunci tunggal."),
        C(
            S("""
k = pd.DataFrame({'a': [1, 1, 2], 'b': ['x', 'y', 'x'], 'v': [1, 2, 3]})
l = pd.DataFrame({'a': [1, 2], 'b': ['x', 'x'], 'w': [9, 8]})
r = k.merge(l, on=['a', 'b'])
print(r['v'].tolist(), r['w'].tolist())
print(k.merge(l, on=['a', 'b'], how='left')['w'].tolist())
print(len(k.merge(l, on='a')))
"""),
            ind("""
[1, 3] [9, 8]
[9.0, nan, 8.0]
3
"""),
            "Dua kunci mencocokkan kombinasi. Memakai satu kunci saja menghasilkan lebih banyak pasangan.",
            filename="kunci_ganda.py",
        ),
        tb("Kolom bentrok dan sufiks", "Bila kedua tabel memiliki kolom bukan kunci dengan nama sama, pandas menambah sufiks `_x` dan `_y` agar tidak menimpa. Nama itu tidak informatif, jadi beri sufiks bermakna lewat `suffixes=('_lama', '_baru')`. Alternatifnya, ganti nama kolom sebelum merge. Kolom bentrok sering tidak disadari dan menghasilkan kolom ambigu dalam analisis lanjutan."),
        C(
            S("""
x1 = pd.DataFrame({'k': [1, 2], 'v': [1, 2]})
x2 = pd.DataFrame({'k': [1, 2], 'v': [3, 4]})
print(x1.merge(x2, on='k').columns.tolist())
print(x1.merge(x2, on='k', suffixes=('_a', '_b')).columns.tolist())
print(x1.merge(x2, on='k', suffixes=('_a', '_b'))[['v_a', 'v_b']].values.tolist())
print(x1.rename(columns={'v': 'lama'}).merge(x2.rename(columns={'v': 'baru'}), on='k').columns.tolist())
"""),
            ind("""
['k', 'v_x', 'v_y']
['k', 'v_a', 'v_b']
[[1, 3], [2, 4]]
['k', 'lama', 'baru']
"""),
            "Sufiks bawaan tidak informatif. Beri sufiks sendiri atau ganti nama sebelum merge.",
            filename="sufiks.py",
        ),
        tb("Validasi hubungan", "Argumen `validate` membuat pandas memeriksa asumsi Anda tentang jenis hubungan: `'one_to_one'`, `'one_to_many'`, `'many_to_one'`, atau `'many_to_many'`. Bila asumsi dilanggar, pandas melempar `MergeError` sehingga masalah tertangkap segera, bukan menghasilkan tabel membengkak diam-diam. Biasakan memakainya pada merge penting di pipeline, karena ia murah dan menyelamatkan dari kesalahan senyap."),
        C(
            S("""
d1 = pd.DataFrame({'k': [1, 1, 2], 'v': [1, 2, 3]})
d2 = pd.DataFrame({'k': [1, 1, 2], 'w': [10, 20, 30]})
print(len(d1.merge(d2, on='k')))
print(d1.merge(d2, on='k').values.tolist())
try:
    d1.merge(d2, on='k', validate='one_to_one')
except Exception as e:
    print(type(e).__name__)
print(len(d1.merge(d2.drop_duplicates('k'), on='k', validate='many_to_one')))
"""),
            ind("""
5
[[1, 1, 10], [1, 1, 20], [1, 2, 10], [1, 2, 20], [2, 3, 30]]
MergeError
3
"""),
            "Banyak ke banyak melipatgandakan baris. Validate menangkap pelanggaran asumsi dengan MergeError.",
            filename="validate.py",
        ),
        tb("Banyak ke banyak berbahaya", "Bila kunci duplikat di kedua tabel, tiap pasangan baris dicocokkan, sehingga dua baris kiri dan dua baris kanan menghasilkan empat baris. Hasil ini jarang yang Anda inginkan dan dapat membengkak sangat besar pada data nyata. Bila Anda menemukannya, hapus duplikat dengan `drop_duplicates`, agregasi dulu menjadi satu baris per kunci, atau pikirkan ulang model data Anda."),
        tb("Join berbasis indeks", "Metode `DataFrame.join` menggabung menurut indeks dan bawaannya left join. Ia ringkas bila kunci sudah menjadi indeks lewat `set_index`. Padanannya dengan merge: `a.join(b)` kira-kira sama dengan `a.merge(b, left_index=True, right_index=True, how='left')`. Pakai merge bila kunci berupa kolom dan join bila kunci sudah indeks, sehingga niat kode jelas."),
        tb("Menggabung hasil agregasi", "Pola yang sering muncul: agregasi dulu menjadi satu baris per kunci, lalu merge kembali ke tabel utama. Misalnya hitung total pesanan per pelanggan dengan groupby, lalu left join ke tabel pelanggan. Pola ini menghindari duplikasi satu ke banyak karena sisi kanan sudah unik, dan hasilnya tetap satu baris per pelanggan yang siap dianalisis."),
        tb("Performa merge", "Merge pada kolom bertipe teks lebih lambat daripada pada bilangan bulat. Untuk tabel besar, ubah kunci teks menjadi kategori atau kode bilangan bulat, dan pilih hanya kolom yang diperlukan sebelum merge agar memori tidak boros. Urutkan dan hapus duplikat dilakukan sebelum, bukan sesudah, menggabung. Optimasi ini sering mengubah proses menit menjadi detik tanpa mengubah hasil."),
        K("tip", "Pakai validate pada merge penting. Ia menangkap asumsi hubungan yang keliru sebelum menjadi kesalahan senyap.", title="Validasi merge"),
        tb("Kunci yang tampak sama", "Dua kunci yang tampak sama di layar bisa berbeda: spasi di ujung teks, huruf besar dan kecil, atau satu bilangan bulat dan satu desimal. Akibatnya merge menghasilkan banyak baris tanpa pasangan. Bersihkan dengan `str.strip()` dan `str.lower()`, samakan tipe dengan `astype`, lalu bandingkan jumlah kunci unik di kedua sisi sebelum merge sehingga masalah terlihat sejak awal."),
        tb("Merge pada indeks dan kolom", "Merge dapat memadukan indeks satu tabel dengan kolom tabel lain lewat `left_index=True` dan `right_on='kolom'`. Ini berguna ketika salah satu tabel sudah memakai kuncinya sebagai indeks, misalnya hasil groupby. Pastikan Anda memahami mana yang indeks dan mana yang kolom, sebab hasil merge bisa kehilangan indeks asal dan mengacaukan pengurutan yang Anda andalkan."),
        tb("Menggabung tiga tabel", "Untuk tiga tabel atau lebih, lakukan merge berantai satu per satu, dan periksa jumlah baris pada tiap langkah. Mulailah dari tabel utama lalu perkaya dengan tabel lain secara left join. Rantai merge yang panjang dapat dibaca lebih mudah dengan tanda kurung dan satu langkah per baris, dengan nama perantara yang menjelaskan isi tiap tahap penggabungan."),
        tb("Contoh audit merge", "Rutinitas audit yang baik terdiri dari empat pemeriksaan: jumlah baris sebelum dan sesudah, jumlah kunci unik di tiap sisi, hitungan kolom indicator, dan apakah ada kolom bentrok. Menjalankannya setiap kali merge penting dilakukan hanya butuh beberapa baris kode, tetapi menghindarkan analisis dari kesimpulan yang bersandar pada tabel gabungan yang salah."),
        E(
            "B2-07-2-ex1",
            "mudah",
            "Tulis fungsi `jumlah_baris_join(pel, pes, how)` yang menggabung `pel` dan `pes` dengan `id` dan `id_pel` memakai jenis join `how`, dan mengembalikan banyaknya baris hasil.",
            ind("""
import pandas as pd

def jumlah_baris_join(pel, pes, how):
    # TODO: implementasikan
    pass
"""),
            P("""
assert jumlah_baris_join(pel, pes, 'inner') == 3
assert jumlah_baris_join(pel, pes, 'left') == 5
assert jumlah_baris_join(pel, pes, 'right') == 4
assert jumlah_baris_join(pel, pes, 'outer') == 6
"""),
            "merge dengan argumen how dan hitung panjangnya.",
            X(G11),
        ),
        E(
            "B2-07-2-ex2",
            "sedang",
            "Tulis fungsi `kolom_sufiks(kiri, kanan)` yang menggabung dua tabel pada kolom `k` dengan sufiks `_a` dan `_b` untuk kolom bentrok, dan mengembalikan list nama kolom hasil.",
            ind("""
import pandas as pd

def kolom_sufiks(kiri, kanan):
    # TODO: implementasikan
    pass
"""),
            P("""
x1 = pd.DataFrame({'k': [1, 2], 'v': [1, 2]})
x2 = pd.DataFrame({'k': [1, 2], 'v': [3, 4]})
assert kolom_sufiks(x1, x2) == ['k', 'v_a', 'v_b']
y2 = pd.DataFrame({'k': [1, 2], 'w': [3, 4]})
assert kolom_sufiks(x1, y2) == ['k', 'v', 'w']
assert kolom_sufiks(x1, x2.assign(z=0)) == ['k', 'v_a', 'v_b', 'z']
assert len(kolom_sufiks(x1, x2)) == 3
"""),
            "merge dengan argumen suffixes berisi dua teks.",
            X(G12),
        ),
        E(
            "B2-07-2-ex3",
            "sedang",
            "Tulis fungsi `total_kota(pel, pes)` yang melakukan left join pelanggan dan pesanan lalu mengembalikan dict jumlah `total` per `kota`.",
            ind("""
import pandas as pd

def total_kota(pel, pes):
    # TODO: implementasikan
    pass
"""),
            P("""
assert total_kota(pel, pes) == {'Bandung': 200.0, 'Jakarta': 250.0, 'Medan': 0.0}
assert total_kota(pel.iloc[[0]], pes) == {'Jakarta': 250.0}
assert total_kota(pel.iloc[[1, 2]], pes) == {'Bandung': 200.0, 'Medan': 0.0}
assert sum(total_kota(pel, pes).values()) == 450.0
"""),
            "Left merge lalu groupby kota dan sum.",
            X(G13),
        ),
        E(
            "B2-07-2-ex4",
            "menantang",
            "Tulis fungsi `asal_baris(pel, pes)` yang melakukan outer join dengan `indicator=True` dan mengembalikan list nilai `_merge` sebagai teks.",
            ind("""
import pandas as pd

def asal_baris(pel, pes):
    # TODO: implementasikan
    pass
"""),
            P("""
assert asal_baris(pel, pes) == ['both', 'both', 'both', 'left_only', 'left_only', 'right_only']
assert asal_baris(pel.iloc[[0]], pes.iloc[[0]]) == ['both']
assert asal_baris(pel.iloc[[2]], pes.iloc[[3]]) == ['left_only', 'right_only']
assert asal_baris(pel, pes).count('both') == 3
"""),
            "merge outer dengan indicator lalu ubah _merge ke teks.",
            X(G14),
        ),
    ],
    [
        M("Banyak ke banyak tanpa disadari.", "Pakai validate dan hapus duplikat."),
        M("Membiarkan sufiks _x dan _y.", "Beri sufiks bermakna."),
        M("Merge tabel besar dengan semua kolom.", "Pilih kolom yang perlu sebelum merge."),
    ],
    [
        Q("Dua kunci diberikan dengan?", ["on dengan list", "dua merge", "index", "drop"], 0, "List.", hint="List."),
        Q("Kolom bentrok diberi sufiks bawaan?", ["_x dan _y", "_a dan _b", "_1 dan _2", "Tidak ada"], 0, "x y.", hint="x."),
        Q("validate melempar?", ["MergeError", "KeyError", "ValueError saja", "Tidak"], 0, "MergeError.", hint="Merge."),
        Q("Banyak ke banyak menghasilkan?", ["Perkalian baris", "Satu baris", "Nol", "Galat"], 0, "Silang.", hint="Perkalian."),
        Q("join DataFrame menggabung menurut?", ["Indeks", "Kolom pertama", "Nama", "Acak"], 0, "Indeks.", hint="Indeks."),
    ],
    [
        "Kunci ganda dicocokkan lewat list pada on.",
        "Sufiks mencegah nama kolom bentrok membingungkan.",
        "validate menangkap hubungan data yang keliru.",
        "Agregasi dulu lalu merge menghindari duplikasi.",
    ],
    [],
)

H11 = """
import pandas as pd

def tumpuk_x(p1, p2):
    return pd.concat([p1, p2], ignore_index=True)['x'].tolist()
"""
H12 = """
import pandas as pd

def sisi_samping(p1, p2):
    return pd.concat([p1, p2], axis=1).values.tolist()
"""
H13 = """
import pandas as pd

def baris_unik(p1, p2):
    return len(pd.concat([p1, p2], ignore_index=True).drop_duplicates())
"""
H14 = """
import pandas as pd

def kolom_gabungan(p1, p2, join):
    return pd.concat([p1, p2], join=join, ignore_index=True).columns.tolist()
"""

l3 = lesson(
    "B2-07-3",
    "Menumpuk tabel dengan concat",
    35,
    [
        "Menumpuk tabel vertikal dan horizontal dengan concat",
        "Mengelola indeks dengan ignore_index dan keys",
        "Menangani kolom yang tidak sama antar tabel",
        "Menghapus duplikat setelah menumpuk",
    ],
    [
        tb("Merge versus concat", "Merge menggabung tabel menyamping menurut nilai kunci. Concat menumpuk tabel begitu saja, biasanya ke bawah. Pakai concat bila tabel berbagi kolom yang sama dan Anda hanya ingin menambah baris, misalnya data bulanan dari file terpisah, atau potongan hasil dari beberapa proses. Concat tidak mencocokkan nilai, hanya menyejajarkan menurut indeks atau nama kolom."),
        C(
            S("""
p1 = pd.DataFrame({'x': [1, 2], 'y': ['a', 'b']})
p2 = pd.DataFrame({'x': [3], 'y': ['c']})
print(pd.concat([p1, p2]).index.tolist())
print(pd.concat([p1, p2], ignore_index=True).index.tolist())
print(pd.concat([p1, p2], ignore_index=True)['x'].tolist())
print(pd.concat({'u': p1, 'v': p2}).index.tolist())
print(pd.concat([p1, p2]).reset_index(drop=True).index.tolist())
"""),
            ind("""
[0, 1, 0]
[0, 1, 2]
[1, 2, 3]
[('u', 0), ('u', 1), ('v', 0)]
[0, 1, 2]
"""),
            "Concat mempertahankan indeks asal. Pakai ignore_index untuk nomor baru atau dict untuk menandai asal.",
            filename="concat_vertikal.py",
        ),
        tb("Indeks dan ignore_index", "Concat mempertahankan indeks tiap tabel, sehingga hasilnya dapat memiliki indeks duplikat seperti nol, satu, nol. Indeks duplikat membingungkan `loc`. Pakai `ignore_index=True` untuk nomor baru berurutan, atau beri dict untuk menandai asal tiap potongan dalam indeks bertingkat. Pilih menurut apakah asal baris perlu diingat setelah penggabungan."),
        tb("Menumpuk banyak file", "Pola umum untuk data bulanan: baca tiap file menjadi DataFrame, kumpulkan dalam list, lalu satu panggilan `pd.concat(daftar, ignore_index=True)`. Jangan menumpuk di dalam perulangan satu per satu, sebab setiap concat menyalin seluruh data dan waktu membengkak kuadratik. Satu concat di akhir jauh lebih cepat dan lebih mudah dibaca."),
        tb("Concat menyamping", "Dengan `axis=1`, concat menempelkan tabel berdampingan menurut indeks. Baris dengan indeks yang sama disejajarkan, dan indeks yang hanya ada di satu tabel menghasilkan NaN di tabel lain. Pastikan indeks kedua tabel memang berkorespondensi, sebab bila tidak, baris akan tersejajar salah tanpa peringatan dan menghasilkan kolom yang tampak masuk akal tetapi keliru."),
        C(
            S("""
p1 = pd.DataFrame({'x': [1, 2], 'y': ['a', 'b']})
p3 = pd.DataFrame({'z': [10, 20]})
print(pd.concat([p1, p3], axis=1).values.tolist())
p4 = pd.DataFrame({'x': [5], 'w': [1.5]})
print(pd.concat([p1, p4], ignore_index=True).columns.tolist())
print(pd.concat([p1, p4], ignore_index=True)['w'].isna().sum())
print(pd.concat([p1, p4], join='inner', ignore_index=True).columns.tolist())
"""),
            ind("""
[[1, 'a', 10], [2, 'b', 20]]
['x', 'y', 'w']
2
['x']
"""),
            "Kolom yang tidak sama diisi NaN pada join outer bawaan, dan hanya kolom bersama dipertahankan pada inner.",
            filename="concat_kolom.py",
        ),
        tb("Kolom tidak sama", "Bila tabel yang ditumpuk memiliki kolom berbeda, concat mengambil gabungan kolom dan mengisi NaN di tempat kosong, setara outer join. Dengan `join='inner'`, hanya kolom yang ada di semua tabel dipertahankan. Periksa kolom hasil setelah menumpuk. Kolom baru yang muncul sering menandakan kesalahan nama seperti `Umur` pada satu file dan `umur` pada file lain."),
        tb("Hapus duplikat", "Menumpuk potongan yang tumpang tindih menghasilkan baris ganda. Hapus dengan `drop_duplicates()`, dan atur `subset` bila hanya beberapa kolom yang menentukan keunikan, serta `keep` untuk memilih yang dipertahankan. Metode `duplicated()` menandai duplikat tanpa membuangnya, sehingga Anda dapat memeriksa lebih dulu apa yang akan hilang sebelum benar-benar membuangnya."),
        C(
            S("""
p1 = pd.DataFrame({'x': [1, 2], 'y': ['a', 'b']})
p2 = pd.DataFrame({'x': [3], 'y': ['c']})
t = pd.concat([p1, p1, p2])
print(t.duplicated().tolist())
print(t.drop_duplicates().shape)
print(t.drop_duplicates(subset='x', keep='last').index.tolist())
print(len(pd.concat([p1, p1], ignore_index=True).drop_duplicates()))
"""),
            ind("""
[False, False, True, True, False]
(3, 2)
[0, 1, 0]
2
"""),
            "Duplicated menandai, dan drop_duplicates membuang duplikat. Subset dan keep mengatur perilakunya.",
            filename="drop_dup.py",
        ),
        tb("Memeriksa hasil tumpukan", "Setelah menumpuk, periksa jumlah baris yang harus sama dengan jumlah semua potongan, periksa kolom, dan periksa tipe data. Jika satu file membaca angka sebagai teks karena ada karakter aneh, kolom hasil menjadi bertipe objek dan perhitungan diam-diam gagal. Pemeriksaan tiga hal ini cukup untuk menangkap sebagian besar masalah penumpukan data."),
        tb("Ringkasan modul", "Anda telah belajar merge dengan berbagai jenis join, kunci ganda, sufiks, validasi, serta concat vertikal dan horizontal dengan pengelolaan indeks dan duplikat. Prinsipnya: pilih merge untuk mencocokkan nilai dan concat untuk menumpuk, selalu periksa jumlah baris, dan validasi asumsi hubungan. Modul berikutnya membahas pivot, melt, dan reshape."),
        K("tip", "Kumpulkan semua potongan dalam list lalu panggil concat sekali, bukan menumpuk di dalam perulangan.", title="Satu concat"),
        tb("Concat dan merge bersama", "Dalam praktik, kedua alat dipakai bersama. Tumpuk dulu data bulanan dengan concat menjadi satu tabel besar, lalu perkaya dengan merge terhadap tabel acuan seperti daftar produk atau wilayah. Urutan ini menjaga setiap langkah sederhana: tumpuk untuk menambah baris, gabung untuk menambah kolom. Memisahkan peran keduanya membuat alur data mudah diaudit."),
        tb("Menandai sumber data", "Saat menumpuk beberapa file, tambahkan kolom penanda sumber sebelum concat, misalnya nama file atau bulan, dengan `assign(sumber='jan')`. Tanpa penanda, setelah menumpuk Anda tidak dapat lagi membedakan asal baris, padahal perbedaan antar bulan atau antar sumber sering menjadi inti analisis. Penanda murah ditambahkan di awal dan sulit direkonstruksi bila terlambat."),
        tb("Concat dan tipe data", "Bila satu potongan memiliki kolom bilangan bulat dan potongan lain memiliki kolom yang sama berisi teks, hasil concat memiliki tipe objek campuran dan perhitungan menjadi aneh atau lambat. Setelah menumpuk, periksa tipe dengan `dtypes` dan ubah dengan `astype` atau `to_numeric`. Kebiasaan ini mencegah kejutan ketika agregasi pertama gagal pada kolom yang kelihatannya numerik."),
        tb("Menumpuk dengan keys", "Argumen `keys` memberi label tiap potongan dalam indeks bertingkat, misalnya bulan atau sumber. Anda kemudian dapat memilih satu potongan dengan `loc['jan']` atau meratakannya dengan `reset_index(level=0)` sehingga label menjadi kolom. Teknik ini praktis bila asal baris perlu dilacak, dan menggantikan kolom penanda manual dengan cara yang lebih ringkas."),
        E(
            "B2-07-3-ex1",
            "mudah",
            "Tulis fungsi `tumpuk_x(p1, p2)` yang menumpuk dua tabel ke bawah dengan nomor baris baru dan mengembalikan list kolom `x`.",
            ind("""
import pandas as pd

def tumpuk_x(p1, p2):
    # TODO: implementasikan
    pass
"""),
            S("""
p1 = pd.DataFrame({'x': [1, 2], 'y': ['a', 'b']})
p2 = pd.DataFrame({'x': [3], 'y': ['c']})
assert tumpuk_x(p1, p2) == [1, 2, 3]
assert tumpuk_x(p2, p1) == [3, 1, 2]
assert tumpuk_x(p1, p1) == [1, 2, 1, 2]
assert len(tumpuk_x(p1, p2)) == 3
"""),
            "concat dengan ignore_index lalu ambil kolom x.",
            X(H11),
        ),
        E(
            "B2-07-3-ex2",
            "sedang",
            "Tulis fungsi `sisi_samping(p1, p2)` yang menempelkan dua tabel berdampingan dan mengembalikan `values.tolist()`.",
            ind("""
import pandas as pd

def sisi_samping(p1, p2):
    # TODO: implementasikan
    pass
"""),
            S("""
p1 = pd.DataFrame({'x': [1, 2], 'y': ['a', 'b']})
p3 = pd.DataFrame({'z': [10, 20]})
assert sisi_samping(p1, p3) == [[1, 'a', 10], [2, 'b', 20]]
assert sisi_samping(p3, p3) == [[10, 10], [20, 20]]
assert sisi_samping(p3, p1) == [[10, 1, 'a'], [20, 2, 'b']]
assert len(sisi_samping(p1, p3)) == 2
"""),
            "concat dengan axis satu.",
            X(H12),
        ),
        E(
            "B2-07-3-ex3",
            "sedang",
            "Tulis fungsi `baris_unik(p1, p2)` yang menumpuk dua tabel, membuang baris duplikat, dan mengembalikan banyaknya baris yang tersisa.",
            ind("""
import pandas as pd

def baris_unik(p1, p2):
    # TODO: implementasikan
    pass
"""),
            S("""
p1 = pd.DataFrame({'x': [1, 2], 'y': ['a', 'b']})
p2 = pd.DataFrame({'x': [3], 'y': ['c']})
assert baris_unik(p1, p1) == 2
assert baris_unik(p1, p2) == 3
assert baris_unik(p2, p2) == 1
assert baris_unik(p1, pd.concat([p1, p2])) == 3
"""),
            "concat lalu drop_duplicates dan hitung panjang.",
            X(H13),
        ),
        E(
            "B2-07-3-ex4",
            "menantang",
            "Tulis fungsi `kolom_gabungan(p1, p2, join)` yang menumpuk dua tabel dengan jenis `join` (`'outer'` atau `'inner'`) dan mengembalikan list nama kolom hasil.",
            ind("""
import pandas as pd

def kolom_gabungan(p1, p2, join):
    # TODO: implementasikan
    pass
"""),
            S("""
p1 = pd.DataFrame({'x': [1, 2], 'y': ['a', 'b']})
p4 = pd.DataFrame({'x': [5], 'w': [1.5]})
assert kolom_gabungan(p1, p4, 'outer') == ['x', 'y', 'w']
assert kolom_gabungan(p1, p4, 'inner') == ['x']
assert kolom_gabungan(p1, p1, 'outer') == ['x', 'y']
assert kolom_gabungan(p4, p1, 'inner') == ['x']
"""),
            "concat dengan argumen join dan ignore_index.",
            X(H14),
        ),
    ],
    [
        M("Menumpuk di dalam perulangan.", "Kumpulkan dalam list lalu satu concat."),
        M("Indeks duplikat setelah concat.", "Pakai ignore_index atau reset_index."),
        M("Nama kolom beda huruf besar kecil antar file.", "Samakan nama kolom sebelum menumpuk."),
    ],
    [
        Q("concat bawaan menumpuk ke?", ["Bawah", "Samping", "Acak", "Atas saja"], 0, "axis 0.", hint="Bawah."),
        Q("ignore_index True?", ["Nomor baris baru", "Hapus indeks", "Hapus kolom", "Urutkan"], 0, "Indeks baru.", hint="Baru."),
        Q("join inner pada concat?", ["Kolom bersama saja", "Semua kolom", "Tak ada", "Baris saja"], 0, "Irisan kolom.", hint="Bersama."),
        Q("drop_duplicates?", ["Membuang baris ganda", "Menambah", "Menggabung", "Mengurutkan"], 0, "Duplikat.", hint="Ganda."),
        Q("Menumpuk banyak file efisien dengan?", ["Satu concat atas list", "Concat dalam loop", "Merge", "Join"], 0, "Sekali.", hint="List."),
    ],
    [
        "concat menumpuk tabel vertikal atau horizontal tanpa mencocokkan nilai.",
        "ignore_index dan keys mengelola indeks hasil.",
        "Kolom tak sama diisi NaN pada outer dan dibuang pada inner.",
        "drop_duplicates membersihkan baris ganda.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perintah yang cukup jelas dalam teks.", "brief": []}

write_module(
    "B2",
    7,
    "Merge, join, dan concat",
    105,
    [
        "Menggabung tabel dengan merge dan memilih jenis join",
        "Mengelola kunci ganda, sufiks, dan validasi",
        "Menumpuk tabel dengan concat dan membersihkan duplikat",
    ],
    [l1, l2, l3],
    video,
    REF,
)
