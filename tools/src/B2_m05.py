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
    'nama': ['Ani', 'Budi', 'Cici', 'Dedi', 'Eka'],
    'umur': [25, np.nan, 31, np.nan, 28],
    'kota': ['Jakarta', 'Bandung', None, 'Jakarta', 'Medan'],
    'gaji': [8.0, 6.5, np.nan, 5.0, 7.0],
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

def hitung_hilang(df):
    return df.isna().sum().to_dict()
"""
F12 = """
import pandas as pd

def persen_hilang(df, kolom):
    return round(float(df[kolom].isna().mean() * 100), 2)
"""
F13 = """
import pandas as pd

def baris_lengkap(df):
    return df.dropna()['nama'].tolist()
"""
F14 = """
import pandas as pd

def kolom_hilang(df):
    return sorted(df.columns[df.isna().any()].tolist())
"""

l1 = lesson(
    "B2-05-1",
    "Mendeteksi nilai hilang",
    35,
    [
        "Memahami NaN sebagai penanda nilai hilang",
        "Menghitung dan memetakan nilai hilang dengan isna",
        "Menjelaskan mengapa perbandingan dengan NaN selalu salah",
        "Melihat dampak NaN pada agregasi",
    ],
    [
        tb("Mengapa nilai hilang penting", "Hampir semua data nyata memiliki sel kosong. Responden melewati pertanyaan, sensor gagal membaca, atau penggabungan tabel tidak menemukan pasangan. Cara kita menangani sel kosong memengaruhi rata-rata, korelasi, dan model. Langkah pertama selalu sama: ketahui di mana dan berapa banyak nilai hilang sebelum memutuskan apa pun, karena keputusan yang tergesa dapat mengubah kesimpulan analisis."),
        tb("NaN dan None", "Pandas menandai nilai hilang pada kolom angka dengan `NaN`, singkatan dari not a number, yang berasal dari standar bilangan desimal. Pada kolom teks nilai hilang juga ditampilkan sebagai NaN, meskipun Anda mengisinya dengan `None`. Metode pandas memperlakukan keduanya sebagai hilang. Karena NaN bertipe desimal, kolom bilangan bulat yang memiliki NaN otomatis menjadi desimal."),
        tb("Data contoh", "Pelajaran ini memakai tabel lima orang dengan kolom `nama`, `umur`, `kota`, dan `gaji`. Umur Budi dan Dedi kosong, kota Cici kosong, dan gaji Cici kosong. Tabel kecil ini memudahkan Anda memeriksa tiap hasil dengan mata sebelum menerapkan metode yang sama ke tabel besar yang tidak mungkin diperiksa satu per satu."),
        C(
            P("""
print(df.isna().sum().to_dict())
print(df.notna().sum().to_dict())
print(df['umur'].isna().tolist())
print(df.isna().any(axis=1).tolist())
print(df.isna().sum(axis=1).tolist())
print(df.isna().mean().round(2).to_dict())
"""),
            ind("""
{'nama': 0, 'umur': 2, 'kota': 1, 'gaji': 1}
{'nama': 5, 'umur': 3, 'kota': 4, 'gaji': 4}
[False, True, False, True, False]
[False, True, True, True, False]
[0, 1, 2, 1, 0]
{'nama': 0.0, 'umur': 0.4, 'kota': 0.2, 'gaji': 0.2}
"""),
            "Isna menghasilkan tabel boolean. Sum menghitung hilang per kolom, dan mean memberi proporsinya.",
            filename="deteksi_hilang.py",
        ),
        tb("isna dan notna", "Metode `isna()` menghasilkan objek berbentuk sama berisi True di tempat nilai hilang, dan `notna()` kebalikannya. Karena True bernilai satu, `sum()` menghitung jumlah hilang dan `mean()` menghitung proporsinya. Menjumlahkan pada `axis=1` menghitung hilang per baris, sedangkan `any(axis=1)` menandai baris yang memiliki setidaknya satu nilai hilang."),
        tb("Peta nilai hilang", "Untuk tabel lebar, hitung hilang per kolom lalu urutkan menurun agar kolom paling bermasalah tampak di atas. Proporsi lebih informatif dari jumlah mutlak: seribu hilang dari sepuluh ribu baris berbeda dari seribu hilang dari seribu lima ratus baris. Kolom yang kosong lebih dari separuh sering lebih baik dibuang daripada diisi paksa."),
        C(
            P("""
print(df['umur'].mean(), df['umur'].sum(), df['umur'].count())
print(df['umur'].sum(skipna=False))
print(len(df), df['umur'].size, df['umur'].count())
print(np.nan == np.nan)
print((df['umur'] == np.nan).tolist())
print(df['umur'].isna().sum() / len(df))
"""),
            ind("""
28.0 84.0 3
nan
5 5 3
False
[False, False, False, False, False]
0.4
"""),
            "Agregasi pandas melewati NaN secara bawaan. Perbandingan langsung dengan NaN selalu salah, jadi pakai isna.",
            filename="nan_agregasi.py",
        ),
        tb("Perbandingan dengan NaN", "NaN tidak sama dengan apa pun, bahkan dengan dirinya sendiri. Karena itu `kolom == np.nan` selalu salah dan tidak pernah menemukan nilai hilang. Ini kesalahan klasik pemula. Gunakan selalu `isna()` atau `pd.isna(nilai)` untuk memeriksa. Sifat ini dipakai pula oleh trik lama `x != x` yang benar hanya untuk NaN, tetapi isna jauh lebih jelas dibaca."),
        tb("NaN dalam agregasi", "Secara bawaan, `sum`, `mean`, `min`, `max`, dan `std` pada pandas melewati NaN dengan `skipna=True`. Rata-rata umur di atas dihitung dari tiga nilai, bukan lima. Bila Anda memakai `skipna=False`, satu NaN membuat hasil NaN. Perhatikan bahwa melewati NaN diam-diam mengubah penyebut, sehingga rata-rata dari tiga orang dapat berbeda dari populasi penuh."),
        tb("Hilang acak atau tidak", "Mengapa data hilang menentukan cara menanganinya. Bila hilang murni acak, membuang atau mengisi baris hanya sedikit mengubah hasil. Bila hilang berkaitan dengan nilai itu sendiri, misalnya orang berpenghasilan tinggi enggan melaporkan gaji, maka pembuangan atau pengisian rata-rata dapat membiaskan kesimpulan. Pahami proses pengumpulan data sebelum memutuskan strategi."),
        tb("Nilai hilang yang menyamar", "Tidak semua nilai hilang berupa NaN. Data nyata sering memakai penanda seperti nol, minus satu, 999, teks `N/A`, `-`, atau string kosong. Pandas hanya mengenali sebagian di antaranya saat `read_csv`. Periksa dengan `value_counts` untuk menemukan nilai mencurigakan, lalu ganti dengan `replace` menjadi NaN agar penanganan berikutnya konsisten."),
        C(
            S("""
s = pd.Series(['10', 'N/A', '30', '-', ''])
print(pd.to_numeric(s, errors='coerce').tolist())
t = pd.Series([5, -1, 7, -1, 9])
print(t.replace(-1, np.nan).tolist())
print(t.replace(-1, np.nan).isna().sum())
print(pd.read_csv(__import__('io').StringIO('a,b\\n1,NA\\n2,\\n3,x'))['b'].isna().tolist())
"""),
            ind("""
[10.0, nan, 30.0, nan, nan]
[5.0, nan, 7.0, nan, 9.0]
2
[True, True, False]
"""),
            "To_numeric dengan coerce dan replace mengubah penanda palsu menjadi NaN. Read_csv mengenali NA dan sel kosong secara bawaan.",
            filename="hilang_menyamar.py",
        ),
        tb("Mencatat temuan", "Dokumentasikan kolom yang memiliki nilai hilang, jumlahnya, dan dugaan penyebabnya. Catatan ini berguna ketika Anda atau orang lain kembali ke analisis berbulan-bulan kemudian dan bertanya mengapa baris tertentu dibuang. Laporan hilang yang singkat dalam notebook adalah bagian dari analisis yang dapat diulang, sama pentingnya dengan seed acak dan versi pustaka."),
        tb("Ringkasan pelajaran", "Anda telah belajar bahwa NaN menandai hilang, bahwa `isna` dan `notna` memetakannya, bahwa perbandingan `== np.nan` tidak pernah bekerja, dan bahwa agregasi melewati NaN secara bawaan. Pelajaran berikutnya membahas dua tindakan utama: membuang baris atau kolom, dan mengisi nilai dengan strategi yang masuk akal."),
        K("warn", "Jangan periksa nilai hilang dengan == np.nan. Hasilnya selalu False. Pakai isna.", title="Jebakan NaN"),
        tb("Hilang dalam praktik", "Dalam proyek nyata, pemeriksaan hilang adalah langkah rutin pertama setelah memuat data, sejajar dengan memeriksa bentuk dan tipe kolom. Biasakan menjalankan `df.info()` dan hitungan isna segera setelah `read_csv`, sebelum menulis satu pun transformasi.", ),
        E(
            "B2-05-1-ex1",
            "mudah",
            "Tulis fungsi `hitung_hilang(df)` yang mengembalikan dict jumlah nilai hilang per kolom.",
            ind("""
import pandas as pd

def hitung_hilang(df):
    # TODO: implementasikan
    pass
"""),
            P("""
assert hitung_hilang(df) == {'nama': 0, 'umur': 2, 'kota': 1, 'gaji': 1}
assert hitung_hilang(df[['nama']]) == {'nama': 0}
assert hitung_hilang(df.dropna()) == {'nama': 0, 'umur': 0, 'kota': 0, 'gaji': 0}
assert sum(hitung_hilang(df).values()) == 4
"""),
            "isna lalu sum per kolom dan ubah ke dict.",
            X(F11),
        ),
        E(
            "B2-05-1-ex2",
            "sedang",
            "Tulis fungsi `persen_hilang(df, kolom)` yang mengembalikan persentase nilai hilang pada kolom itu, dibulatkan ke dua desimal.",
            ind("""
import pandas as pd

def persen_hilang(df, kolom):
    # TODO: implementasikan
    pass
"""),
            P("""
assert persen_hilang(df, 'umur') == 40.0
assert persen_hilang(df, 'kota') == 20.0
assert persen_hilang(df, 'nama') == 0.0
assert persen_hilang(df.iloc[:3], 'umur') == 33.33
"""),
            "Rata-rata isna dikali seratus lalu bulatkan.",
            X(F12),
        ),
        E(
            "B2-05-1-ex3",
            "sedang",
            "Tulis fungsi `baris_lengkap(df)` yang mengembalikan list `nama` untuk baris yang tidak memiliki nilai hilang sama sekali.",
            ind("""
import pandas as pd

def baris_lengkap(df):
    # TODO: implementasikan
    pass
"""),
            P("""
assert baris_lengkap(df) == ['Ani', 'Eka']
assert baris_lengkap(df.iloc[[1, 2]]) == []
assert baris_lengkap(df.iloc[[0]]) == ['Ani']
assert baris_lengkap(df[['nama', 'gaji']]) == ['Ani', 'Budi', 'Dedi', 'Eka']
"""),
            "dropna lalu ambil kolom nama.",
            X(F13),
        ),
        E(
            "B2-05-1-ex4",
            "menantang",
            "Tulis fungsi `kolom_hilang(df)` yang mengembalikan list nama kolom yang memiliki setidaknya satu nilai hilang, terurut abjad.",
            ind("""
import pandas as pd

def kolom_hilang(df):
    # TODO: implementasikan
    pass
"""),
            P("""
assert kolom_hilang(df) == ['gaji', 'kota', 'umur']
assert kolom_hilang(df.dropna()) == []
assert kolom_hilang(df[['nama', 'umur']]) == ['umur']
assert kolom_hilang(df.iloc[[0]]) == []
"""),
            "Pilih kolom dengan any pada isna lalu urutkan.",
            X(F14),
        ),
    ],
    [
        M("Memeriksa hilang dengan == np.nan.", "Pakai isna atau pd.isna."),
        M("Mengabaikan penanda palsu seperti -1 dan N/A.", "Ganti dengan NaN memakai replace atau to_numeric."),
        M("Mengira rata-rata memakai seluruh baris.", "Agregasi melewati NaN dan penyebutnya berkurang."),
    ],
    [
        Q("Cara benar memeriksa hilang?", ["isna", "== np.nan", "== None saja", "len"], 0, "NaN tak sama dengan dirinya.", hint="isna."),
        Q("np.nan == np.nan bernilai?", ["False", "True", "Galat", "None"], 0, "Selalu salah.", hint="False."),
        Q("Mean pandas terhadap NaN?", ["Melewati NaN", "Menghasilkan NaN", "Galat", "Menghitung nol"], 0, "skipna True.", hint="Lewati."),
        Q("df.isna().sum() menghasilkan?", ["Hilang per kolom", "Hilang total saja", "Baris lengkap", "Persen"], 0, "Per kolom.", hint="Kolom."),
        Q("Penanda palsu diubah dengan?", ["replace ke NaN", "dropna", "sort", "cut"], 0, "Samakan penanda.", hint="Replace."),
    ],
    [
        "NaN menandai nilai hilang dan isna memetakannya.",
        "Perbandingan dengan NaN selalu salah.",
        "Agregasi melewati NaN secara bawaan.",
        "Waspadai penanda hilang yang menyamar.",
    ],
    [],
)

G11 = """
import pandas as pd

def isi_nol(df, kolom):
    return df[kolom].fillna(0).tolist()
"""
G12 = """
import pandas as pd

def isi_rata(df, kolom):
    return df[kolom].fillna(df[kolom].mean()).tolist()
"""
G13 = """
import pandas as pd

def isi_kota(df, pengganti):
    return df['kota'].fillna(pengganti).tolist()
"""
G14 = """
import pandas as pd

def hapus_minimal(df, thresh):
    return df.dropna(thresh=thresh)['nama'].tolist()
"""

l2 = lesson(
    "B2-05-2",
    "Membuang dan mengisi nilai hilang",
    35,
    [
        "Membuang baris atau kolom dengan dropna",
        "Mengisi nilai dengan fillna memakai konstanta, rata-rata, atau median",
        "Memilih strategi menurut tipe kolom",
        "Menyadari efek samping tiap strategi",
    ],
    [
        tb("Dua tindakan utama", "Setelah menemukan nilai hilang, ada dua tindakan utama: membuang atau mengisi. Membuang sederhana tetapi mengurangi data dan dapat membiaskan. Mengisi mempertahankan baris tetapi menyuntikkan asumsi. Tidak ada jawaban universal. Pilihan bergantung pada banyaknya hilang, tipe kolom, dan tujuan analisis. Pelajaran ini menunjukkan perintah dan konsekuensinya."),
        tb("dropna", "Metode `dropna()` membuang semua baris yang memiliki nilai hilang. Argumen `subset` membatasi pemeriksaan pada kolom tertentu, `how='all'` membuang hanya baris yang seluruhnya kosong, dan `thresh=n` mempertahankan baris yang memiliki sekurang-kurangnya n nilai terisi. Dengan `axis=1`, ia membuang kolom, bukan baris. Metode ini mengembalikan tabel baru dan tidak mengubah asalnya."),
        C(
            P("""
print(len(df.dropna()), df.dropna()['nama'].tolist())
print(df.dropna(subset=['gaji'])['nama'].tolist())
print(df.dropna(how='all').shape)
print(df.dropna(thresh=3)['nama'].tolist())
print(df.dropna(thresh=4)['nama'].tolist())
print(df.dropna(axis=1).columns.tolist())
print(df.shape)
"""),
            ind("""
2 ['Ani', 'Eka']
['Ani', 'Budi', 'Dedi', 'Eka']
(5, 4)
['Ani', 'Budi', 'Dedi', 'Eka']
['Ani', 'Eka']
['nama']
(5, 4)
"""),
            "Dropna memiliki subset, how, thresh, dan axis. Tabel asal tidak berubah.",
            filename="dropna.py",
        ),
        tb("Kapan membuang", "Membuang cocok bila hilang sedikit dan acak, atau bila nilai yang dibutuhkan model benar-benar tidak ada, misalnya target. Waspadai membuang terlalu banyak: bila dropna tanpa argumen menyisakan dua dari lima baris, Anda kehilangan enam puluh persen data. Gunakan `subset` agar hanya kolom yang relevan menentukan pembuangan, bukan setiap kolom."),
        tb("fillna dengan konstanta", "Metode `fillna(nilai)` mengganti NaN dengan nilai tertentu. Untuk teks, nilai seperti `'Tidak diketahui'` menjaga baris sekaligus menandai ketiadaan data sebagai kategori sendiri. Untuk angka, nol hanya sah bila nol memang berarti tidak ada, misalnya jumlah pembelian. Mengisi umur dengan nol jelas salah dan merusak rata-rata."),
        tb("Isi dengan statistik", "Untuk kolom angka, pengganti umum adalah rata-rata atau median. Median lebih tahan terhadap pencilan sehingga lebih aman untuk data miring seperti gaji. Untuk kategori, gunakan modus, yaitu nilai paling sering. Hitung statistik hanya dari data latih agar tidak terjadi kebocoran informasi saat membangun model prediksi."),
        C(
            P("""
print(df['umur'].fillna(0).tolist())
print(df['umur'].fillna(df['umur'].mean()).tolist())
print(df['umur'].fillna(df['umur'].median()).tolist())
print(df['kota'].fillna('Tidak diketahui').tolist())
print(df['kota'].fillna(df['kota'].mode()[0]).tolist())
print(df.fillna({'umur': 0, 'kota': '?', 'gaji': df['gaji'].mean()}).values.tolist())
"""),
            ind("""
[25.0, 0.0, 31.0, 0.0, 28.0]
[25.0, 28.0, 31.0, 28.0, 28.0]
[25.0, 28.0, 31.0, 28.0, 28.0]
['Jakarta', 'Bandung', 'Tidak diketahui', 'Jakarta', 'Medan']
['Jakarta', 'Bandung', 'Jakarta', 'Jakarta', 'Medan']
[['Ani', 25.0, 'Jakarta', 8.0], ['Budi', 0.0, 'Bandung', 6.5], ['Cici', 31.0, '?', 6.625], ['Dedi', 0.0, 'Jakarta', 5.0], ['Eka', 28.0, 'Medan', 7.0]]
"""),
            "Fillna menerima nilai tunggal, statistik, atau dict per kolom.",
            filename="fillna.py",
        ),
        tb("fillna dengan dict", "Memberi dict ke `fillna` mengisi setiap kolom dengan nilainya sendiri dalam satu perintah, sehingga strategi berbeda per kolom tertulis rapi di satu tempat. Kolom yang tidak disebut dalam dict tidak diubah. Pendekatan ini lebih mudah ditinjau dan diuji dibanding rangkaian penugasan terpisah yang tersebar di notebook."),
        tb("Efek pada sebaran", "Mengisi dengan rata-rata menumpuk banyak nilai pada satu titik, sehingga simpangan baku mengecil dan korelasi melemah. Ini tampak kecil pada sepuluh persen hilang, tetapi nyata pada empat puluh persen. Bila hilang banyak, pertimbangkan metode lebih canggih seperti imputasi berbasis model, atau setidaknya tambahkan kolom penanda hilang agar model dapat belajar dari pola ketiadaan."),
        C(
            S("""
s = pd.Series([10.0, np.nan, 30.0, np.nan, 50.0])
filled = s.fillna(s.mean())
print(round(s.std(), 2), round(filled.std(), 2))
print(s.mean(), filled.mean())
print(filled.tolist())
print(s.isna().astype(int).tolist())
"""),
            ind("""
20.0 14.14
30.0 30.0
[10.0, 30.0, 30.0, 30.0, 50.0]
[0, 1, 0, 1, 0]
"""),
            "Isi rata-rata mempertahankan mean tetapi menyusutkan simpangan baku. Penanda hilang menyimpan informasi ketiadaan.",
            filename="efek_isi.py",
        ),
        tb("Inplace dan penugasan ulang", "Metode seperti `dropna` dan `fillna` mengembalikan objek baru. Argumen `inplace=True` sudah tidak dianjurkan karena membingungkan dan tidak lebih efisien. Tulis `df = df.dropna()` atau simpan ke kolom: `df['umur'] = df['umur'].fillna(0)`. Gaya ini eksplisit, bekerja dalam rantai metode, dan menghindari peringatan salinan pada pandas."),
        tb("Urutan pekerjaan", "Urutan yang sehat: deteksi hilang, putuskan strategi per kolom, terapkan, lalu verifikasi dengan menghitung hilang lagi sampai nol. Jangan lupa memeriksa dampak: bandingkan statistik sebelum dan sesudah. Bila perbedaannya besar, pikirkan ulang strategi. Catat keputusan agar orang lain memahami asal tiap angka dalam laporan."),
        K("tip", "Setelah mengisi, hitung hilang lagi dan bandingkan statistik sebelum dan sesudah untuk memastikan strategi tidak merusak sebaran data.", title="Verifikasi"),
        tb("Membuang kolom", "Kolom yang hampir seluruhnya kosong jarang berguna. Bila delapan puluh persen sel sebuah kolom hilang, mengisinya berarti mengarang sebagian besar isinya. Pertimbangkan membuang kolom itu dengan `drop(columns=...)` atau `dropna(axis=1, thresh=...)`. Pastikan dulu bahwa kolom itu tidak penting secara bisnis, misalnya kolom yang hanya terisi untuk kasus langka tetapi sangat bermakna."),
        tb("Mengisi kategori", "Untuk kolom kategori, ada dua pilihan utama. Pertama, mengisi dengan modus, yang mempertahankan sebaran kira-kira sama tetapi menguatkan kategori dominan. Kedua, membuat kategori khusus seperti `Tidak diketahui`, yang jujur terhadap ketiadaan data dan membiarkan model atau analis memperlakukannya terpisah. Pilihan kedua biasanya lebih aman bila alasan hilang tidak jelas."),
        tb("Mengisi tanpa kebocoran", "Dalam pemodelan, hitung rata-rata atau median hanya dari data latih, lalu pakai angka itu untuk mengisi data latih maupun uji. Bila statistik dihitung dari seluruh data, informasi dari data uji bocor ke pelatihan dan membuat skor evaluasi terlalu optimistis. Kebiasaan ini mudah dilupakan ketika bekerja cepat di notebook, jadi tulis langkah pengisian sebagai bagian dari pipeline."),
        E(
            "B2-05-2-ex1",
            "mudah",
            "Tulis fungsi `isi_nol(df, kolom)` yang mengembalikan list isi kolom itu dengan nilai hilang diganti nol.",
            ind("""
import pandas as pd

def isi_nol(df, kolom):
    # TODO: implementasikan
    pass
"""),
            P("""
assert isi_nol(df, 'umur') == [25.0, 0.0, 31.0, 0.0, 28.0]
assert isi_nol(df, 'gaji') == [8.0, 6.5, 0.0, 5.0, 7.0]
assert isi_nol(df, 'nama') == ['Ani', 'Budi', 'Cici', 'Dedi', 'Eka']
assert sum(isi_nol(df, 'umur')) == 84.0
"""),
            "fillna dengan nol lalu ubah ke list.",
            X(G11),
        ),
        E(
            "B2-05-2-ex2",
            "sedang",
            "Tulis fungsi `isi_rata(df, kolom)` yang mengisi nilai hilang kolom angka dengan rata-rata kolom itu dan mengembalikan list.",
            ind("""
import pandas as pd

def isi_rata(df, kolom):
    # TODO: implementasikan
    pass
"""),
            P("""
assert isi_rata(df, 'umur') == [25.0, 28.0, 31.0, 28.0, 28.0]
assert isi_rata(df, 'gaji') == [8.0, 6.5, 6.625, 5.0, 7.0]
assert isi_rata(df.iloc[[0, 1]], 'umur') == [25.0, 25.0]
assert len(isi_rata(df, 'gaji')) == 5
"""),
            "fillna dengan mean dari kolom yang sama.",
            X(G12),
        ),
        E(
            "B2-05-2-ex3",
            "sedang",
            "Tulis fungsi `isi_kota(df, pengganti)` yang mengisi kota hilang dengan teks `pengganti` dan mengembalikan list kota.",
            ind("""
import pandas as pd

def isi_kota(df, pengganti):
    # TODO: implementasikan
    pass
"""),
            P("""
assert isi_kota(df, 'Tidak diketahui') == ['Jakarta', 'Bandung', 'Tidak diketahui', 'Jakarta', 'Medan']
assert isi_kota(df, '?')[2] == '?'
assert isi_kota(df.iloc[[0]], 'X') == ['Jakarta']
assert isi_kota(df, 'Jakarta').count('Jakarta') == 3
"""),
            "fillna pada kolom kota.",
            X(G13),
        ),
        E(
            "B2-05-2-ex4",
            "menantang",
            "Tulis fungsi `hapus_minimal(df, thresh)` yang membuang baris dengan kurang dari `thresh` nilai terisi dan mengembalikan list `nama` yang tersisa.",
            ind("""
import pandas as pd

def hapus_minimal(df, thresh):
    # TODO: implementasikan
    pass
"""),
            P("""
assert hapus_minimal(df, 4) == ['Ani', 'Eka']
assert hapus_minimal(df, 3) == ['Ani', 'Budi', 'Dedi', 'Eka']
assert hapus_minimal(df, 2) == ['Ani', 'Budi', 'Cici', 'Dedi', 'Eka']
assert hapus_minimal(df, 5) == []
"""),
            "dropna dengan argumen thresh lalu ambil nama.",
            X(G14),
        ),
    ],
    [
        M("Mengisi umur dengan nol.", "Pakai median atau rata-rata bila nol tidak bermakna."),
        M("Membuang terlalu banyak baris dengan dropna tanpa subset.", "Batasi pada kolom yang relevan dengan subset."),
        M("Memakai inplace dan lupa penugasan ulang.", "Tulis df = df.dropna()."),
    ],
    [
        Q("dropna secara bawaan membuang?", ["Baris dengan hilang", "Kolom dengan hilang", "Duplikat", "Pencilan"], 0, "Baris.", hint="Baris."),
        Q("thresh pada dropna berarti?", ["Minimum nilai terisi", "Maksimum hilang", "Jumlah kolom", "Ambang rata-rata"], 0, "Minimum terisi.", hint="Terisi."),
        Q("Isi lebih tahan pencilan?", ["Median", "Rata-rata", "Maksimum", "Jumlah"], 0, "Median.", hint="Median."),
        Q("fillna dengan dict?", ["Isi per kolom", "Isi per baris", "Hapus", "Urutkan"], 0, "Per kolom.", hint="Kolom."),
        Q("Isi rata-rata terhadap simpangan baku?", ["Mengecil", "Membesar", "Tetap", "Nol"], 0, "Menumpuk.", hint="Kecil."),
    ],
    [
        "dropna membuang baris atau kolom dengan subset, how, dan thresh.",
        "fillna mengisi dengan konstanta, statistik, atau dict per kolom.",
        "Setiap strategi punya efek samping pada sebaran.",
        "Verifikasi hasil setelah menangani hilang.",
    ],
    [],
)

H11 = """
import pandas as pd

def interpolasi(s):
    return pd.Series(s, dtype=float).interpolate().tolist()
"""
H12 = """
import pandas as pd

def penanda_hilang(df, kolom):
    return df[kolom].isna().astype(int).tolist()
"""
H13 = """
import pandas as pd

def isi_maju(df, kolom):
    return df[kolom].ffill().tolist()
"""
H14 = """
import pandas as pd

def ringkas_hilang(df):
    p = (df.isna().mean() * 100).round(2)
    return p[p > 0].to_dict()
"""

l3 = lesson(
    "B2-05-3",
    "Strategi isi lanjutan",
    35,
    [
        "Memakai ffill, bfill, dan interpolate untuk data berurutan",
        "Menambah kolom penanda hilang",
        "Mengisi nilai per kelompok dengan transform",
        "Memilih strategi menurut konteks data",
    ],
    [
        tb("Data berurutan", "Untuk data deret waktu atau data yang urutannya bermakna, mengisi dengan rata-rata keseluruhan sering kurang tepat. Suhu pukul tiga lebih mirip suhu pukul dua daripada rata-rata setahun. Pandas menyediakan `ffill` untuk menyalin nilai sebelumnya ke depan, `bfill` untuk menyalin nilai berikutnya ke belakang, dan `interpolate` untuk mengisi dengan garis lurus di antara tetangga."),
        C(
            P("""
print(df['gaji'].ffill().tolist())
print(df['gaji'].bfill().tolist())
print(df['gaji'].interpolate().tolist())
print(df['umur'].interpolate().tolist())
print(df['umur'].cumsum().tolist())
print(df['gaji'].where(df['gaji'] > 6).tolist())
"""),
            ind("""
[8.0, 6.5, 6.5, 5.0, 7.0]
[8.0, 6.5, 5.0, 5.0, 7.0]
[8.0, 6.5, 5.75, 5.0, 7.0]
[25.0, 28.0, 31.0, 29.5, 28.0]
[25.0, nan, 56.0, nan, 84.0]
[8.0, 6.5, nan, nan, 7.0]
"""),
            "Ffill menyalin ke depan, bfill ke belakang, dan interpolate menarik garis lurus. Cumsum melewati NaN tetapi mempertahankannya.",
            filename="isi_berurutan.py",
        ),
        tb("Hati-hati dengan urutan", "Metode isi berurutan mengandalkan urutan baris. Bila data belum diurutkan menurut waktu, hasilnya menyesatkan. Urutkan dulu dengan `sort_values` atau `sort_index`. Perhatikan pula bahwa ffill pada awal data tetap menyisakan NaN karena belum ada nilai sebelumnya. Tambahkan `bfill` sesudahnya bila perlu, atau gunakan argumen `limit` agar celah panjang tidak terisi sembarangan."),
        tb("Interpolasi", "Metode `interpolate` secara bawaan linear: nilai hilang diisi sepanjang garis lurus antara dua tetangga terdekat. Untuk indeks tanggal, argumen `method='time'` memperhitungkan jarak waktu sebenarnya. Interpolasi cocok untuk besaran yang berubah mulus seperti suhu, tetapi tidak cocok untuk kategori atau besaran yang melompat seperti harga barang yang berganti tiba-tiba."),
        tb("Penanda hilang", "Bila ketiadaan data itu sendiri informatif, simpan informasi itu sebagai kolom baru bernilai nol atau satu sebelum mengisi. Misalnya orang yang tidak mengisi gaji mungkin berbeda dari yang mengisi. Dengan kolom penanda, model dapat menangkap pola tersebut, sedangkan hanya mengisi rata-rata akan menghapus jejaknya. Penanda murah dibuat dan sering berguna."),
        C(
            P("""
d = df.assign(umur_hilang=df['umur'].isna().astype(int))
print(d['umur_hilang'].tolist())
print(d['umur_hilang'].sum())
d['umur'] = d['umur'].fillna(d['umur'].median())
print(d['umur'].tolist())
print(d[['umur_hilang', 'umur']].values.tolist())
"""),
            ind("""
[0, 1, 0, 1, 0]
2
[25.0, 28.0, 31.0, 28.0, 28.0]
[[0.0, 25.0], [1.0, 28.0], [0.0, 31.0], [1.0, 28.0], [0.0, 28.0]]
"""),
            "Penanda dibuat sebelum mengisi sehingga jejak hilang tetap tersimpan.",
            filename="penanda_hilang.py",
        ),
        tb("Isi per kelompok", "Mengisi dengan statistik global mengabaikan kelompok. Gaji tenaga senior berbeda dari magang, jadi mengisi dengan rata-rata per jabatan lebih masuk akal. Pola idiomnya adalah `df['x'].fillna(df.groupby('g')['x'].transform('mean'))`. Metode `transform` mengembalikan Series sepanjang tabel berisi statistik kelompok tiap baris, sehingga dapat dipakai langsung sebagai pengisi."),
        C(
            S("""
d = pd.DataFrame({'g': ['a', 'a', 'b', 'b', 'b'], 'x': [1.0, np.nan, 10.0, np.nan, 30.0]})
rata = d.groupby('g')['x'].transform('mean')
print(rata.tolist())
print(d['x'].fillna(rata).tolist())
print(d['x'].fillna(d['x'].mean()).tolist())
print(d.groupby('g')['x'].apply(lambda s: s.isna().sum()).to_dict())
"""),
            ind("""
[1.0, 1.0, 20.0, 20.0, 20.0]
[1.0, 1.0, 10.0, 20.0, 30.0]
[1.0, 13.666666666666666, 10.0, 13.666666666666666, 30.0]
{'a': 1, 'b': 1}
"""),
            "Transform menghasilkan statistik kelompok per baris. Hasilnya lebih masuk akal daripada rata-rata global.",
            filename="isi_kelompok.py",
        ),
        tb("Baris yang kelompoknya hilang", "Isi per kelompok gagal bila kolom kelompoknya sendiri hilang, atau bila seluruh kelompok kosong. Dalam kasus ini statistik kelompok berupa NaN dan baris tetap kosong. Tambahkan langkah cadangan dengan `fillna` statistik global sesudahnya. Selalu hitung hilang lagi di akhir untuk memastikan tidak ada sel yang terlewat oleh strategi bertingkat."),
        tb("Imputasi berbasis model", "Selain metode sederhana, ada imputasi berbasis model seperti k tetangga terdekat dan imputasi iteratif yang menebak nilai hilang dari kolom lain. Pustaka scikit-learn menyediakan `SimpleImputer`, `KNNImputer`, dan `IterativeImputer`. Metode ini lebih akurat bila hilang banyak, tetapi lebih rumit, lebih lambat, dan wajib dipasang hanya pada data latih agar tidak bocor."),
        tb("Memilih strategi", "Pilih menurut konteks. Hilang sangat sedikit dan acak: buang. Kolom angka tanpa urutan: median. Kategori: modus atau kategori khusus. Data berurutan: ffill atau interpolasi. Ada kelompok bermakna: isi per kelompok. Ketiadaan informatif: tambah penanda. Kolom hampir kosong: buang kolomnya. Tulis alasan pilihan agar dapat ditinjau."),
        tb("Ringkasan modul", "Anda telah belajar mendeteksi nilai hilang, membuang dan mengisinya dengan konstanta atau statistik, serta memakai metode berurutan, penanda, dan isi per kelompok. Prinsip utamanya: pahami mengapa data hilang, pilih strategi yang sesuai konteks, verifikasi hasilnya, dan dokumentasikan keputusan. Modul berikutnya membahas groupby dan agregasi."),
        K("tip", "Tambahkan kolom penanda hilang sebelum mengisi bila ketiadaan data mungkin informatif.", title="Simpan jejak"),
        tb("Batas pengisian", "Argumen `limit` pada `ffill`, `bfill`, dan `interpolate` membatasi berapa banyak nilai hilang berurutan yang boleh diisi. Ini berguna agar celah panjang, misalnya sensor mati sepanjang hari, tidak diisi dengan nilai usang yang menyesatkan. Celah yang melebihi batas tetap NaN dan dapat ditangani terpisah atau dilaporkan sebagai data yang tidak tersedia."),
        tb("Mengisi data deret waktu", "Pada deret waktu berindeks tanggal, sering lebih tepat mengisi menurut musim, misalnya rata-rata jam yang sama pada hari lain. Pendekatan ini memakai groupby pada jam atau hari dalam pekan lalu transform seperti pada isi per kelompok. Metode sederhana seperti ffill cukup untuk celah pendek, tetapi tidak menangkap pola harian yang berulang."),
        tb("Menguji strategi isi", "Cara jujur menilai strategi isi adalah menyembunyikan sebagian nilai yang diketahui dengan sengaja, mengisinya dengan tiap strategi, lalu membandingkan hasil dengan nilai asli memakai galat rata-rata. Strategi dengan galat terkecil pada data uji layak dipilih. Teknik ini mengganti perdebatan selera dengan bukti dan mudah dilakukan dengan beberapa baris kode."),
        E(
            "B2-05-3-ex1",
            "mudah",
            "Tulis fungsi `interpolasi(s)` yang menerima list angka dengan NaN dan mengembalikan list hasil interpolasi linear.",
            ind("""
import pandas as pd

def interpolasi(s):
    # TODO: implementasikan
    pass
"""),
            P("""
assert interpolasi([1, np.nan, 3]) == [1.0, 2.0, 3.0]
assert interpolasi(df['gaji']) == [8.0, 6.5, 5.75, 5.0, 7.0]
assert interpolasi([0, np.nan, np.nan, 3]) == [0.0, 1.0, 2.0, 3.0]
assert interpolasi([5, 6]) == [5.0, 6.0]
"""),
            "Ubah ke Series desimal lalu panggil interpolate.",
            X(H11),
        ),
        E(
            "B2-05-3-ex2",
            "sedang",
            "Tulis fungsi `penanda_hilang(df, kolom)` yang mengembalikan list 1 untuk baris yang hilang pada kolom itu dan 0 untuk lainnya.",
            ind("""
import pandas as pd

def penanda_hilang(df, kolom):
    # TODO: implementasikan
    pass
"""),
            P("""
assert penanda_hilang(df, 'umur') == [0, 1, 0, 1, 0]
assert penanda_hilang(df, 'kota') == [0, 0, 1, 0, 0]
assert penanda_hilang(df, 'nama') == [0, 0, 0, 0, 0]
assert sum(penanda_hilang(df, 'gaji')) == 1
"""),
            "isna lalu ubah ke bilangan bulat.",
            X(H12),
        ),
        E(
            "B2-05-3-ex3",
            "sedang",
            "Tulis fungsi `isi_maju(df, kolom)` yang menyalin nilai terakhir yang ada ke depan pada kolom itu dan mengembalikan list.",
            ind("""
import pandas as pd

def isi_maju(df, kolom):
    # TODO: implementasikan
    pass
"""),
            P("""
assert isi_maju(df, 'gaji') == [8.0, 6.5, 6.5, 5.0, 7.0]
assert isi_maju(df, 'umur') == [25.0, 25.0, 31.0, 31.0, 28.0]
assert isi_maju(df, 'kota') == ['Jakarta', 'Bandung', 'Bandung', 'Jakarta', 'Medan']
assert isi_maju(df.iloc[[1, 2]], 'gaji') == [6.5, 6.5]
"""),
            "ffill pada kolom yang dipilih.",
            X(H13),
        ),
        E(
            "B2-05-3-ex4",
            "menantang",
            "Tulis fungsi `ringkas_hilang(df)` yang mengembalikan dict `{kolom: persen_hilang}` hanya untuk kolom yang memiliki hilang, dibulatkan dua desimal.",
            ind("""
import pandas as pd

def ringkas_hilang(df):
    # TODO: implementasikan
    pass
"""),
            P("""
assert ringkas_hilang(df) == {'umur': 40.0, 'kota': 20.0, 'gaji': 20.0}
assert ringkas_hilang(df.dropna()) == {}
assert ringkas_hilang(df[['nama', 'umur']]) == {'umur': 40.0}
assert ringkas_hilang(df.iloc[:3]) == {'umur': 33.33, 'kota': 33.33, 'gaji': 33.33}
"""),
            "Rata-rata isna dikali seratus, bulatkan, lalu saring yang positif.",
            X(H14),
        ),
    ],
    [
        M("Memakai ffill pada data yang belum terurut.", "Urutkan dulu menurut waktu atau kunci."),
        M("Mengisi per kelompok tanpa cadangan.", "Tambahkan fillna global sesudahnya."),
        M("Mengisi tanpa menyimpan penanda.", "Buat kolom penanda sebelum mengisi."),
    ],
    [
        Q("ffill menyalin nilai ke?", ["Depan", "Belakang", "Acak", "Median"], 0, "Maju.", hint="Depan."),
        Q("interpolate bawaan?", ["Linear", "Kuadrat", "Acak", "Modus"], 0, "Garis lurus.", hint="Linear."),
        Q("transform mengembalikan?", ["Series sepanjang tabel", "Satu angka", "Dict", "Tabel kecil"], 0, "Per baris.", hint="Panjang sama."),
        Q("Penanda hilang dibuat?", ["Sebelum mengisi", "Sesudah mengisi", "Tak perlu", "Saat plot"], 0, "Jejak.", hint="Sebelum."),
        Q("Data deret waktu cocok dengan?", ["ffill atau interpolate", "Isi nol", "dropna saja", "Acak"], 0, "Berurutan.", hint="Urutan."),
    ],
    [
        "ffill, bfill, dan interpolate cocok untuk data berurutan.",
        "Penanda hilang menyimpan jejak ketiadaan.",
        "Isi per kelompok memakai groupby dan transform.",
        "Pilih strategi menurut konteks dan dokumentasikan.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perintah yang cukup jelas dalam teks.", "brief": []}

write_module(
    "B2",
    5,
    "Missing value dasar",
    105,
    [
        "Mendeteksi dan memetakan nilai hilang",
        "Membuang atau mengisi nilai hilang dengan strategi yang sesuai",
        "Memakai isi berurutan, penanda, dan isi per kelompok",
    ],
    [l1, l2, l3],
    video,
    REF,
)
