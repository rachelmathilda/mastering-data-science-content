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
    'id': [1, 2, 3, 3, 5, 6],
    'nama': ['Ani', ' budi', 'Cici', 'Cici', None, 'Fani'],
    'umur': [25, -3, 31, 31, 200, 28],
    'email': ['a@x.com', 'b@x', 'c@x.com', 'c@x.com', 'e@x.com', None],
    'kota': ['Jakarta', 'jakarta', 'Medan', 'Medan', 'Bandung', 'Jakarta'],
    'gaji': [8.0, 6.5, np.nan, np.nan, 7.0, 1000000.0],
})
"""

EMAIL = "r'^[^@\\\\s]+@[^@\\\\s]+\\\\.[^@\\\\s]+$'"


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

def jumlah_hilang_total(df):
    return int(df.isna().sum().sum())
"""
F12 = """
import pandas as pd

def kolom_kardinalitas_kecil(df, batas):
    return [c for c in df.columns if df[c].nunique() <= batas]
"""
F13 = """
import pandas as pd

def baris_duplikat(df, subset=None):
    return int(df.duplicated(subset=subset).sum())
"""
F14 = """
import pandas as pd

def ringkasan_numerik(df, kolom):
    s = df[kolom]
    return [float(s.min()), float(s.max()), float(s.median())]
"""

l1 = lesson(
    "B3-01-1",
    "Profil cepat sebuah tabel",
    35,
    [
        "Menjalankan pemeriksaan pertama pada tabel yang belum dikenal",
        "Membaca bentuk, tipe, hilang, dan kardinalitas dengan cepat",
        "Mengenali duplikat dan kolom yang mencurigakan",
        "Membaca ringkasan numerik untuk menemukan angka tak wajar",
    ],
    [
        tb("Jangan percaya data yang baru tiba", "Data yang baru Anda terima hampir selalu lebih kotor daripada dugaan. Ada sel kosong, tanggal yang terbaca sebagai teks, nama kota dengan tiga ejaan, usia negatif, dan baris yang tercatat dua kali. Model dan grafik yang dibangun di atas data seperti itu akan tampak meyakinkan tetapi salah, dan kesalahannya sulit dilacak karena tidak ada pesan galat. Audit kualitas data adalah langkah sistematis untuk menemukan masalah itu sebelum analisis dimulai. Pelajaran ini mengajarkan profil cepat: lima menit pemeriksaan yang menjawab pertanyaan apakah tabel ini layak dipercaya dan apa yang perlu diperbaiki lebih dulu."),
        tb("Pepatah lama yang masih benar", "Pepatah sampah masuk, sampah keluar berlaku keras dalam ilmu data. Algoritma paling canggih pun hanya meniru pola yang ada pada data latihnya, termasuk pola kesalahan. Chip Huyen dalam bukunya tentang sistem pembelajaran mesin menekankan bahwa data adalah fondasi dan bahwa sebagian besar masalah di produksi berakar pada data, bukan pada algoritma. Karena itu waktu yang dihabiskan memeriksa data hampir selalu lebih menguntungkan daripada waktu yang dihabiskan menyetel model. Audit juga menumbuhkan pemahaman tentang bagaimana data lahir, yang menjadi bahan penilaian saat memilih cara memperbaikinya."),
        tb("Data contoh", "Pelajaran ini memakai tabel enam baris yang sengaja berantakan. Kolom `id` berisi satu sampai enam tetapi angka tiga muncul dua kali dan empat hilang. Kolom `nama` memiliki satu nilai kosong dan satu nama dengan spasi di depan. Kolom `umur` mengandung nilai negatif dan nilai dua ratus. Kolom `email` memiliki satu alamat yang tidak lengkap dan satu yang kosong. Kolom `kota` menulis Jakarta dalam dua ejaan huruf besar dan kecil. Kolom `gaji` memiliki dua nilai kosong dan satu angka sejuta yang jauh di luar yang lain. Anggaplah tabel ini sebagai daftar periksa temuan."),
        C(
            P("""
print(df.shape, df.columns.tolist())
print(df.isna().sum().to_dict())
print(df.isna().mean().round(3).to_dict())
print(df.nunique().to_dict())
print(df.nunique(dropna=False).to_dict())
print(df.select_dtypes('number').columns.tolist())
print(df.isna().sum().sum(), df.isna().any(axis=1).sum())
"""),
            ind("""
(6, 6) ['id', 'nama', 'umur', 'email', 'kota', 'gaji']
{'id': 0, 'nama': 1, 'umur': 0, 'email': 1, 'kota': 0, 'gaji': 2}
{'id': 0.0, 'nama': 0.167, 'umur': 0.0, 'email': 0.167, 'kota': 0.0, 'gaji': 0.333}
{'id': 5, 'nama': 4, 'umur': 5, 'email': 4, 'kota': 4, 'gaji': 4}
{'id': 5, 'nama': 5, 'umur': 5, 'email': 5, 'kota': 4, 'gaji': 5}
['id', 'umur', 'gaji']
4 4
"""),
            "Bentuk, hilang, dan jumlah nilai unik adalah tiga angka pertama yang dilihat pada tabel baru. Nunique melewati NaN kecuali dropna False.",
            filename="profil_dasar.py",
        ),
        tb("Pertanyaan pertama: seberapa besar", "Mulailah dengan bentuk tabel: berapa baris dan kolom. Angka ini memberi rasa skala dan langsung berguna: bila Anda mengharapkan sejuta baris dan menerima sepuluh ribu, ada yang terpotong saat pengambilan. Bandingkan juga dengan dokumentasi sumber data atau jumlah dari sistem asal. Selisih antara jumlah yang diharapkan dan yang diterima adalah temuan pertama yang paling murah dan sering paling penting. Setelah itu lihat nama kolom: apakah sesuai kamus data, adakah kolom tak terduga, dan adakah kolom yang seharusnya ada tetapi hilang."),
        tb("Pertanyaan kedua: tipe dan hilang", "Periksa tipe tiap kolom dan jumlah nilai hilang. Kolom angka yang bertipe teks hampir selalu berarti ada nilai kotor seperti `N/A` atau tanda mata uang. Kolom tanggal bertipe teks perlu diurai. Proporsi hilang lebih informatif daripada jumlah mutlak: satu dari enam berbeda dari satu dari sejuta. Pada contoh, sepertiga gaji hilang, angka yang terlalu besar untuk diabaikan dan terlalu besar untuk diisi sembarangan. Catat kolom mana yang hilang dan perkirakan mengapa, sebab alasan hilang menentukan cara menanganinya."),
        tb("Pertanyaan ketiga: kardinalitas", "Kardinalitas adalah banyaknya nilai unik per kolom, dan memberi petunjuk cepat tentang peran kolom. Kolom dengan nilai unik sebanyak baris, seperti id, adalah pengenal. Kolom dengan sedikit nilai unik adalah kategori. Kolom dengan satu nilai unik tidak informatif dan dapat dibuang. Kolom yang kardinalitasnya aneh patut diselidiki: kota dengan empat nilai unik padahal hanya tiga kota nyata menandakan variasi ejaan. Bandingkan `nunique` dengan dan tanpa `dropna=False` untuk melihat seberapa besar peran nilai hilang pada kolom itu."),
        C(
            P("""
print(df.duplicated().tolist(), df.duplicated('id').tolist(), df.duplicated().sum())
print(df['id'].is_unique, df['id'].is_monotonic_increasing)
print(df['kota'].value_counts().to_dict())
print(df['kota'].str.lower().value_counts().to_dict())
print(df['kota'].nunique(), df['kota'].str.strip().str.lower().nunique())
print(df.loc[df.duplicated(keep=False), 'id'].tolist())
print(df.groupby('id').size().loc[lambda s: s > 1].to_dict())
"""),
            ind("""
[False, False, False, True, False, False] [False, False, False, True, False, False] 1
False True
{'Jakarta': 2, 'Medan': 2, 'jakarta': 1, 'Bandung': 1}
{'jakarta': 3, 'medan': 2, 'bandung': 1}
4 3
[3, 3]
{3: 2}
"""),
            "Duplicated menandai pengulangan, dan value_counts pada teks mentah membongkar variasi ejaan. Keep False menandai semua anggota kelompok duplikat, bukan hanya salinan kedua.",
            filename="duplikat_variasi.py",
        ),
        tb("Pertanyaan keempat: duplikat", "Periksa baris yang sama persis dengan `duplicated()`, dan periksa duplikat pada kolom yang seharusnya unik seperti pengenal dengan `duplicated('id')`. Keduanya menjawab hal berbeda. Duplikat seluruh baris biasanya akibat pemuatan ganda atau penggabungan keliru. Duplikat pada pengenal dengan isi berbeda lebih berbahaya karena berarti dua catatan bertentangan untuk entitas yang sama. Argumen `keep=False` menandai semua anggota kelompok duplikat sehingga Anda dapat melihat kedua salinannya berdampingan sebelum memutuskan mana yang dipertahankan."),
        tb("Pertanyaan kelima: variasi ejaan", "Tabel `value_counts` pada kolom teks menunjukkan setiap ejaan yang ada. Pada contoh, Jakarta dan jakarta dihitung sebagai dua kota padahal sama. Membandingkan hitungan sebelum dan sesudah menyeragamkan huruf besar dan spasi dengan `str.strip().str.lower()` menunjukkan seberapa besar masalah variasi. Selisih empat dan tiga pada contoh berarti satu kota terpecah. Temuan seperti ini merusak groupby dan merge diam-diam, sebab kelompok yang seharusnya satu terpecah menjadi dua dan total per kota keliru tanpa pesan galat apa pun."),
        tb("Ringkasan numerik", "Metode `describe` memberi hitungan, rata-rata, simpangan baku, minimum, kuartil, dan maksimum untuk kolom angka. Fokus pertama bukan pada rata-rata tetapi pada minimum dan maksimum, yang membongkar nilai mustahil. Usia minimum minus tiga dan maksimum dua ratus langsung menunjukkan masalah, begitu juga gaji maksimum sejuta ketika median hanya tujuh koma lima. Bandingkan rata-rata dengan median: selisih besar menandakan pencilan yang menarik rata-rata. Pada gaji, rata-rata dua ratus lima puluh ribu jauh dari median tujuh koma lima, tanda jelas ada nilai ekstrem."),
        C(
            P("""
print(df['umur'].describe().round(2).tolist())
print(df['gaji'].describe().round(1).tolist())
print(df['umur'].agg(['min', 'max']).tolist(), df['umur'].lt(0).sum(), df['umur'].gt(120).sum())
print(df['gaji'].median(), df['gaji'].mean())
print(df['gaji'].quantile([0.25, 0.5, 0.75]).tolist())
print(df['umur'].mode().tolist())
"""),
            ind("""
[6.0, 52.0, 73.64, -3.0, 25.75, 29.5, 31.0, 200.0]
[4.0, 250005.4, 499996.4, 6.5, 6.9, 7.5, 250006.0, 1000000.0]
[-3, 200] 1 1
7.5 250005.375
[6.875, 7.5, 250006.0]
[31]
"""),
            "Describe memuat delapan angka: hitungan, rata-rata, simpangan baku, minimum, tiga kuartil, dan maksimum. Selisih besar rata-rata dan median menandakan pencilan.",
            filename="ringkasan_numerik.py",
        ),
        tb("Membaca describe dengan curiga", "Saat membaca keluaran describe, ajukan tiga pertanyaan. Apakah minimum dan maksimum masuk akal secara dunia nyata? Apakah rata-rata dan median berdekatan? Apakah hitungan sama dengan jumlah baris, atau ada yang hilang? Hitungan empat pada gaji padahal ada enam baris langsung memberi tahu dua nilai hilang tanpa perlu menghitung terpisah. Jawaban atas ketiga pertanyaan ini biasanya sudah menunjuk ke masalah paling serius, dan merupakan alasan describe adalah perintah yang hampir selalu dijalankan pertama kali pada data baru."),
        tb("Jangan memperbaiki saat mengaudit", "Godaan terbesar saat menemukan masalah adalah langsung memperbaikinya. Tahanlah. Audit adalah tahap mengamati dan mencatat, bukan mengubah. Memperbaiki sebelum memahami seluruh masalah sering menghasilkan perbaikan yang saling bertabrakan, misalnya membuang baris duplikat sebelum menyadari bahwa duplikat itu menandai masalah penggabungan yang lebih besar. Catat setiap temuan dengan jumlah barisnya, lalu putuskan strategi perbaikan secara terpadu pada pelajaran dan modul berikutnya, dengan data mentah tetap utuh sebagai sumber kebenaran."),
        K("tip", "Jalankan lima pemeriksaan pertama pada setiap tabel baru: bentuk, tipe, hilang, kardinalitas dan duplikat, serta min dan maks. Jangan memperbaiki apa pun sebelum audit selesai.", title="Lima pemeriksaan"),
        E(
            "B3-01-1-ex1",
            "mudah",
            "Tulis fungsi `jumlah_hilang_total(df)` yang mengembalikan bilangan bulat jumlah seluruh sel kosong dalam tabel.",
            ind("""
import pandas as pd

def jumlah_hilang_total(df):
    # TODO: implementasikan
    pass
"""),
            P("""
assert jumlah_hilang_total(df) == 4
assert jumlah_hilang_total(df.dropna()) == 0
assert jumlah_hilang_total(df[['id', 'umur']]) == 0
assert jumlah_hilang_total(df[['gaji']]) == 2
"""),
            "isna lalu sum dua kali.",
            X(F11),
        ),
        E(
            "B3-01-1-ex2",
            "sedang",
            "Tulis fungsi `kolom_kardinalitas_kecil(df, batas)` yang mengembalikan list nama kolom dengan jumlah nilai unik (tanpa menghitung hilang) sebanyak-banyaknya `batas`, mengikuti urutan kolom.",
            ind("""
import pandas as pd

def kolom_kardinalitas_kecil(df, batas):
    # TODO: implementasikan
    pass
"""),
            P("""
assert kolom_kardinalitas_kecil(df, 4) == ['nama', 'email', 'kota', 'gaji']
assert kolom_kardinalitas_kecil(df, 5) == ['id', 'nama', 'umur', 'email', 'kota', 'gaji']
assert kolom_kardinalitas_kecil(df, 3) == []
assert kolom_kardinalitas_kecil(df[['kota']], 4) == ['kota']
"""),
            "nunique per kolom dibandingkan dengan batas.",
            X(F12),
        ),
        E(
            "B3-01-1-ex3",
            "sedang",
            "Tulis fungsi `baris_duplikat(df, subset=None)` yang mengembalikan bilangan bulat jumlah baris duplikat (salinan kedua dan seterusnya), dengan `subset` kolom opsional.",
            ind("""
import pandas as pd

def baris_duplikat(df, subset=None):
    # TODO: implementasikan
    pass
"""),
            P("""
assert baris_duplikat(df) == 1
assert baris_duplikat(df, ['id']) == 1
assert baris_duplikat(df, ['kota']) == 2
assert baris_duplikat(df.drop_duplicates()) == 0
"""),
            "duplicated dengan subset lalu jumlahkan.",
            X(F13),
        ),
        E(
            "B3-01-1-ex4",
            "menantang",
            "Tulis fungsi `ringkasan_numerik(df, kolom)` yang mengembalikan list tiga angka desimal `[minimum, maksimum, median]` kolom itu.",
            ind("""
import pandas as pd

def ringkasan_numerik(df, kolom):
    # TODO: implementasikan
    pass
"""),
            P("""
assert ringkasan_numerik(df, 'umur') == [-3.0, 200.0, 29.5]
assert ringkasan_numerik(df, 'gaji') == [6.5, 1000000.0, 7.5]
assert ringkasan_numerik(df, 'id') == [1.0, 6.0, 3.0]
assert ringkasan_numerik(df.iloc[[0]], 'umur') == [25.0, 25.0, 25.0]
"""),
            "min, max, dan median dari kolom lalu ubah ke float.",
            X(F14),
        ),
    ],
    [
        M("Langsung memperbaiki saat menemukan masalah.", "Audit dulu, catat semua, lalu putuskan strategi terpadu."),
        M("Hanya melihat rata-rata dan mengabaikan min dan maks.", "Baca min, maks, dan selisih rata-rata dengan median."),
        M("Mempercayai nilai unik teks tanpa menyeragamkan ejaan.", "Bandingkan nunique sebelum dan sesudah strip dan lower."),
    ],
    [
        Q("Langkah pertama audit?", ["Lihat bentuk dan tipe", "Hapus duplikat", "Isi hilang", "Latih model"], 0, "Kenali dulu.", hint="Bentuk."),
        Q("Kolom dengan satu nilai unik?", ["Tidak informatif", "Pengenal", "Target", "Kategori"], 0, "Konstan.", hint="Satu."),
        Q("keep False pada duplicated menandai?", ["Semua anggota kelompok", "Hanya yang pertama", "Hanya yang terakhir", "Tak satu pun"], 0, "Semua.", hint="Semua."),
        Q("Rata-rata jauh dari median menandakan?", ["Pencilan", "Data bersih", "Kolom teks", "Duplikat"], 0, "Tertarik ekstrem.", hint="Pencilan."),
        Q("Saat mengaudit sebaiknya?", ["Mencatat tanpa mengubah", "Mengubah langsung", "Menghapus data", "Mengacak"], 0, "Amati dulu.", hint="Catat."),
    ],
    [
        "Profil cepat meliputi bentuk, tipe, hilang, kardinalitas, duplikat, dan ringkasan numerik.",
        "Min, maks, dan perbandingan rata-rata dengan median membongkar nilai mustahil.",
        "Variasi ejaan terlihat dari nunique sebelum dan sesudah penyeragaman.",
        "Audit mencatat temuan, perbaikan menyusul kemudian.",
    ],
    [],
)

G11 = """
import pandas as pd

def umur_tidak_valid(df, bawah, atas):
    return int((~df['umur'].between(bawah, atas)).sum())
"""
G12 = """
import pandas as pd

def id_email_buruk(df):
    pola = r'^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$'
    ok = df['email'].str.match(pola, na=False)
    return df.loc[~ok, 'id'].tolist()
"""
G13 = """
import pandas as pd

def variasi_kota(df):
    mentah = df['kota'].nunique()
    bersih = df['kota'].str.strip().str.lower().nunique()
    return int(mentah - bersih)
"""
G14 = """
import pandas as pd

def kelengkapan(df):
    return (df.notna().mean() * 100).round(1).to_dict()
"""

l2 = lesson(
    "B3-01-2",
    "Dimensi kualitas dan aturan validasi",
    35,
    [
        "Menyebut dimensi kualitas data dan contoh pelanggarannya",
        "Menulis aturan validasi sebagai ekspresi boolean",
        "Memeriksa rentang, format, keunikan, dan konsistensi",
        "Menghitung kelengkapan dan pelanggaran per aturan",
    ],
    [
        tb("Kualitas bukan satu angka", "Kata kualitas data terdengar tunggal, padahal terdiri dari beberapa dimensi yang dapat gagal secara terpisah. Sebuah tabel bisa lengkap tetapi salah, benar tetapi duplikat, atau konsisten tetapi sudah usang. Memecah kualitas menjadi dimensi memberi kosakata untuk menyebut masalah dengan tepat dan daftar periksa untuk memastikan tidak ada yang terlewat. Pelajaran ini membahas dimensi yang paling berguna dalam praktik dan cara menerjemahkan masing-masing menjadi pemeriksaan kode yang dapat dijalankan ulang tiap kali data baru masuk."),
        tb("Kelengkapan", "Kelengkapan menanyakan apakah semua data yang seharusnya ada memang ada. Ukurannya sederhana: persentase sel terisi per kolom. Pada contoh, gaji hanya terisi enam puluh enam koma tujuh persen, nama dan email delapan puluh tiga koma tiga persen. Ketidaklengkapan tidak selalu buruk: kolom nomor telepon kedua memang boleh kosong. Yang penting membedakan kosong yang sah dari kosong yang menandakan kerusakan, dan menetapkan ambang yang dapat diterima per kolom berdasarkan perannya dalam analisis."),
        tb("Validitas dan keunikan", "Validitas menanyakan apakah nilai mematuhi aturan format dan rentang: usia antara nol dan seratus dua puluh, email berbentuk alamat, tanggal lahir tidak di masa depan. Keunikan menanyakan apakah entitas yang sama tercatat sekali: nomor identitas tidak boleh berulang. Keduanya dapat dituliskan sebagai ekspresi boolean yang menghasilkan satu nilai benar atau salah per baris, sehingga pelanggaran dapat dihitung, ditampilkan, dan dilacak. Menulis aturan sebagai kode, bukan sebagai catatan mental, membuat audit dapat diulang."),
        C(
            P("""
pat = r'^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$'
print(df['umur'].between(0, 120).tolist(), (~df['umur'].between(0, 120)).sum())
print(df['email'].str.match(pat, na=False).tolist())
print(df['id'].is_unique, (~df.duplicated('id', keep=False)).tolist())
print((df.notna().mean() * 100).round(1).to_dict())
print(df['umur'].where(df['umur'].between(0, 120)).tolist())
print(df['umur'].where(df['umur'].between(0, 120)).mean())
"""),
            ind("""
[True, False, True, True, False, True] 2
[True, False, True, True, True, False]
False [True, True, False, False, True, True]
{'id': 100.0, 'nama': 83.3, 'umur': 100.0, 'email': 83.3, 'kota': 100.0, 'gaji': 66.7}
[25.0, nan, 31.0, 31.0, nan, 28.0]
28.75
"""),
            "Aturan rentang, format, dan keunikan masing-masing menjadi satu Series boolean. Menandai nilai tidak valid sebagai NaN memperlihatkan dampaknya pada rata-rata.",
            filename="aturan_validasi.py",
        ),
        tb("Aturan sebagai Series boolean", "Setiap aturan ditulis sebagai ekspresi yang menghasilkan Series boolean dengan satu nilai per baris, di mana True berarti lolos. Aturan rentang memakai `between`, aturan format memakai `str.match` dengan ekspresi reguler, dan aturan keunikan memakai `duplicated` dengan `keep=False` yang dinegasikan. Argumen `na=False` pada `str.match` menetapkan bahwa nilai hilang tidak lolos aturan format, keputusan eksplisit yang menghindari NaN di dalam hasil boolean. Dengan bentuk seragam ini, semua aturan dapat digabung dan dihitung dengan cara yang sama."),
        tb("Konsistensi", "Konsistensi menanyakan apakah data yang sama ditulis dengan cara yang sama di seluruh tabel dan antar tabel. Jakarta dan jakarta adalah inkonsistensi format. Umur yang tidak cocok dengan tanggal lahir adalah inkonsistensi antar kolom. Kode pelanggan di tabel pesanan yang tidak ada di tabel pelanggan adalah inkonsistensi antar tabel. Inkonsistensi sulit ditangkap oleh aturan rentang, sehingga memerlukan pemeriksaan khusus: menyeragamkan lalu menghitung nilai unik, membandingkan kolom turunan, dan memeriksa integritas referensi antar tabel dengan `isin`."),
        tb("Ketepatan waktu dan akurasi", "Ketepatan waktu menanyakan apakah data cukup baru untuk keputusan yang akan diambil. Tabel harga kemarin tidak berguna untuk keputusan hari ini. Periksa tanggal terbaru dalam data dan bandingkan dengan harapan. Akurasi menanyakan apakah nilai mencerminkan kenyataan, dimensi tersulit karena memerlukan pembanding di luar data. Pembanding dapat berupa sumber lain, pengukuran ulang pada sampel kecil, atau aturan bisnis seperti total pesanan harus sama dengan jumlah rinciannya. Tanpa pembanding, akurasi hanya bisa diperkirakan lewat kewajaran."),
        C(
            P("""
pat = r'^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$'
print(df.loc[~df['email'].str.match(pat, na=False), 'id'].tolist())
print(df['kota'].nunique() - df['kota'].str.strip().str.lower().nunique())
print(df['kota'].map(df['kota'].value_counts()).tolist())
print(df['kota'].str.lower().isin(['jakarta', 'medan']).tolist())
print(df[~df['kota'].str.lower().isin(['jakarta', 'medan'])]['kota'].tolist())
print((df['nama'].notna() & (df['nama'] != df['nama'].str.strip())).tolist())
"""),
            ind("""
[2, 6]
1
[2, 1, 2, 2, 1, 2]
[True, True, True, True, False, True]
['Bandung']
[False, True, False, False, False, False]
"""),
            "Daftar nilai yang diizinkan dengan isin, spasi tak terlihat, dan variasi ejaan semuanya dapat dideteksi dengan ekspresi boolean sederhana.",
            filename="konsistensi.py",
        ),
        tb("Daftar nilai yang diizinkan", "Untuk kolom kategori dengan himpunan nilai yang diketahui, seperti kota yang dilayani atau status pesanan, aturan terbaik adalah memeriksa keanggotaan dengan `isin`. Nilai di luar daftar langsung terlihat, apakah itu kategori baru yang sah atau kesalahan ketik. Pada contoh, hanya Bandung yang tidak ada dalam daftar dua kota, dan itu perlu keputusan: kota baru atau salah ketik. Mencantumkan daftar itu sebagai konstanta yang dirawat bersama tim mencegah kategori liar menyelinap ke dalam analisis."),
        tb("Spasi dan karakter tak terlihat", "Salah satu penyebab masalah paling licik adalah spasi di awal atau akhir teks, serta karakter tak terlihat seperti spasi lebar nol atau tab. Nilai ` budi` dan `budi` tampak sama di layar tetapi berbeda bagi komputer, sehingga merge dan groupby gagal tanpa alasan terlihat. Bandingkan teks dengan versi yang dipangkas, `s != s.str.strip()`, untuk menemukannya, dan ingat memeriksa nilai hilang lebih dulu agar NaN tidak ikut ditandai. Pembersihan teks lebih dalam dibahas pada modul tersendiri."),
        tb("Integritas referensi", "Dalam data relasional, kolom penghubung antar tabel harus merujuk ke baris yang ada. Setiap id pelanggan di tabel pesanan harus ada di tabel pelanggan. Pelanggaran disebut baris yatim dan biasanya muncul akibat penghapusan yang tidak diikuti pembersihan, atau data yang dimuat dari sumber berbeda pada waktu berbeda. Periksa dengan `isin` pada dua arah, seperti dalam modul merge. Baris yatim membuat inner join menghilangkan data dan left join memunculkan NaN yang membingungkan, sehingga memeriksanya sebelum menggabung menghemat banyak kebingungan."),
        K("tip", "Tulis setiap aturan kualitas sebagai ekspresi boolean satu nilai per baris, dengan na=False agar nilai hilang diperlakukan eksplisit. Aturan sebagai kode dapat dijalankan ulang kapan saja.", title="Aturan sebagai kode"),
        C(
            P("""
pes_id = [1, 2, 9]
print(pd.Series(pes_id).isin(df['id']).tolist())
print(df['id'].isin(pes_id).tolist())
print(sorted(set(pes_id) - set(df['id'])))
print(round(float(df['umur'].between(0, 120).mean()), 3))
print(df.loc[df['umur'].between(0, 120), 'umur'].mean())
print(df.assign(ok=df['umur'].between(0, 120)).groupby('ok').size().to_dict())
"""),
            ind("""
[True, True, False]
[True, True, False, False, False, False]
[9]
0.667
28.75
{False: 2, True: 4}
"""),
            "Integritas referensi diperiksa dengan isin pada dua arah. Mengelompokkan menurut hasil aturan menunjukkan berapa baris lolos dan gagal.",
            filename="integritas.py",
        ),
        tb("Aturan antar kolom", "Beberapa aturan melibatkan lebih dari satu kolom: tanggal selesai tidak boleh sebelum tanggal mulai, total harus sama dengan jumlah rincian, kota harus sesuai provinsi. Aturan seperti ini lolos dari pemeriksaan per kolom dan hanya terlihat bila kolom dibandingkan. Tulis sebagai ekspresi boolean yang membandingkan kolom, misalnya `df['akhir'] >= df['mulai']`. Pelanggaran antar kolom sering menandakan kolom tertukar atau salah masuk, kesalahan sistematis yang menyentuh banyak baris sekaligus dan layak diselidiki akarnya."),
        tb("Menetapkan ambang yang realistis", "Menuntut seratus persen pada setiap aturan jarang realistis. Tetapkan ambang berdasarkan peran kolom: kolom kunci harus seratus persen, kolom pendukung boleh sembilan puluh lima persen. Ambang dapat diturunkan dari kebutuhan analisis, misalnya berapa nilai hilang yang masih dapat diimputasi tanpa merusak hasil. Catat ambang beserta alasannya agar tim sepakat tentang apa yang dimaksud data cukup baik, dan agar perubahan kualitas yang melewati ambang dapat memicu tindakan, bukan sekadar menjadi angka yang tidak dibaca siapa pun."),
        tb("Contoh menilai satu kolom", "Ambil kolom gaji sebagai contoh. Kelengkapannya enam puluh enam koma tujuh persen, sehingga sepertiga baris tidak punya gaji. Validitasnya: satu nilai sejuta jauh di luar yang lain, mungkin salah satuan. Keunikan tidak relevan. Konsistensi: bila gaji dicatat dalam juta pada sebagian baris dan rupiah penuh pada baris lain, itulah penyebab angka sejuta. Dengan menelusuri satu kolom melalui keempat dimensi, Anda memperoleh cerita lengkap tentang kesehatannya, bukan hanya daftar angka yang terpisah."),
        tb("Menimbang biaya salah", "Pilih seberapa ketat aturan berdasarkan biaya kesalahan. Pada data untuk laporan ringan, usia kosong mungkin tidak berarti apa-apa. Pada data untuk keputusan kredit, usia salah dapat berdampak hukum. Semakin tinggi taruhannya, semakin ketat aturannya dan semakin penting pemeriksaan manual atas sampel. Pertimbangan ini mencegah dua kegagalan sekaligus: terlalu longgar sehingga kesalahan lolos, dan terlalu ketat sehingga waktu habis memeriksa hal yang tidak berpengaruh pada keputusan."),
        E(
            "B3-01-2-ex1",
            "mudah",
            "Tulis fungsi `umur_tidak_valid(df, bawah, atas)` yang mengembalikan bilangan bulat jumlah baris dengan `umur` di luar rentang `bawah` sampai `atas` (kedua ujung dianggap valid).",
            ind("""
import pandas as pd

def umur_tidak_valid(df, bawah, atas):
    # TODO: implementasikan
    pass
"""),
            P("""
assert umur_tidak_valid(df, 0, 120) == 2
assert umur_tidak_valid(df, 0, 300) == 1
assert umur_tidak_valid(df, -10, 300) == 0
assert umur_tidak_valid(df, 28, 31) == 3
"""),
            "between lalu negasikan dan jumlahkan.",
            X(G11),
        ),
        E(
            "B3-01-2-ex2",
            "sedang",
            "Tulis fungsi `id_email_buruk(df)` yang mengembalikan list `id` baris yang emailnya kosong atau tidak berbentuk `nama@domain.tld` (pola `^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$`).",
            ind("""
import pandas as pd

def id_email_buruk(df):
    # TODO: implementasikan
    pass
"""),
            P("""
assert id_email_buruk(df) == [2, 6]
assert id_email_buruk(df.iloc[[0, 2]]) == []
assert id_email_buruk(df.iloc[[1]]) == [2]
assert id_email_buruk(df.iloc[[5]]) == [6]
"""),
            "str.match dengan na False lalu saring baris yang tidak lolos.",
            X(G12),
        ),
        E(
            "B3-01-2-ex3",
            "sedang",
            "Tulis fungsi `variasi_kota(df)` yang mengembalikan selisih jumlah nilai unik `kota` mentah dan setelah dipangkas serta diubah ke huruf kecil.",
            ind("""
import pandas as pd

def variasi_kota(df):
    # TODO: implementasikan
    pass
"""),
            P("""
assert variasi_kota(df) == 1
assert variasi_kota(df.iloc[[0, 1]]) == 1
assert variasi_kota(df.iloc[[0]]) == 0
assert variasi_kota(df.iloc[[2, 3]]) == 0
"""),
            "nunique mentah dikurangi nunique setelah strip dan lower.",
            X(G13),
        ),
        E(
            "B3-01-2-ex4",
            "menantang",
            "Tulis fungsi `kelengkapan(df)` yang mengembalikan dict persentase sel terisi per kolom, dibulatkan satu desimal.",
            ind("""
import pandas as pd

def kelengkapan(df):
    # TODO: implementasikan
    pass
"""),
            P("""
assert kelengkapan(df) == {'id': 100.0, 'nama': 83.3, 'umur': 100.0, 'email': 83.3, 'kota': 100.0, 'gaji': 66.7}
assert kelengkapan(df.dropna()) == {'id': 100.0, 'nama': 100.0, 'umur': 100.0, 'email': 100.0, 'kota': 100.0, 'gaji': 100.0}
assert kelengkapan(df[['gaji']]) == {'gaji': 66.7}
assert kelengkapan(df.iloc[:2])['gaji'] == 100.0
"""),
            "notna lalu rata-rata dikali seratus dan bulatkan.",
            X(G14),
        ),
    ],
    [
        M("Menganggap kualitas hanya soal data hilang.", "Periksa semua dimensi: kelengkapan, validitas, keunikan, konsistensi, waktu."),
        M("Aturan validasi hanya dalam kepala.", "Tulis sebagai kode yang dapat dijalankan ulang."),
        M("Mengabaikan spasi tak terlihat.", "Bandingkan teks dengan versi yang dipangkas."),
    ],
    [
        Q("Validitas menanyakan?", ["Format dan rentang nilai", "Jumlah baris", "Kecepatan", "Ukuran file"], 0, "Aturan nilai.", hint="Format."),
        Q("Keunikan menanyakan?", ["Entitas tercatat sekali", "Semua kolom unik", "Nilai positif", "Tanggal baru"], 0, "Tanpa duplikat.", hint="Sekali."),
        Q("Integritas referensi memakai?", ["isin antar tabel", "describe", "sort", "cut"], 0, "Kunci asing.", hint="isin."),
        Q("na=False pada str.match berarti?", ["Hilang tidak lolos", "Hilang lolos", "Galat", "Hapus baris"], 0, "Eksplisit.", hint="Tidak lolos."),
        Q("Aturan paling baik ditulis sebagai?", ["Kode boolean", "Catatan", "Komentar", "Ingatan"], 0, "Dapat diulang.", hint="Kode."),
    ],
    [
        "Kualitas data memiliki dimensi: kelengkapan, validitas, keunikan, konsistensi, ketepatan waktu, dan akurasi.",
        "Aturan validasi ditulis sebagai Series boolean per baris.",
        "Daftar nilai yang diizinkan dan integritas referensi memakai isin.",
        "Spasi tak terlihat dan variasi ejaan perlu dideteksi eksplisit.",
    ],
    [],
)

H11 = """
import pandas as pd

def laporan_aturan(df):
    pola = r'^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$'
    aturan = {
        'umur_valid': df['umur'].between(0, 120),
        'email_valid': df['email'].str.match(pola, na=False),
        'id_unik': ~df.duplicated('id', keep=False),
    }
    return {k: int((~v).sum()) for k, v in aturan.items()}
"""
H12 = """
import pandas as pd

def persen_lolos(df):
    pola = r'^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$'
    aturan = {
        'umur_valid': df['umur'].between(0, 120),
        'email_valid': df['email'].str.match(pola, na=False),
        'id_unik': ~df.duplicated('id', keep=False),
    }
    return {k: round(float(v.mean() * 100), 1) for k, v in aturan.items()}
"""
H13 = """
import pandas as pd

def baris_lolos_semua(df):
    pola = r'^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$'
    ok = (df['umur'].between(0, 120)
          & df['email'].str.match(pola, na=False)
          & ~df.duplicated('id', keep=False))
    return int(ok.sum())
"""
H14 = """
import pandas as pd

def prioritas(laporan):
    return sorted(laporan, key=lambda k: (-laporan[k], k))
"""

l3 = lesson(
    "B3-01-3",
    "Laporan audit dan prioritas perbaikan",
    35,
    [
        "Menggabung aturan menjadi laporan audit yang ringkas",
        "Menghitung pelanggaran dan persen lolos per aturan",
        "Menentukan prioritas perbaikan berdasarkan dampak",
        "Mengunci harapan kualitas dengan assert dan dokumentasi",
    ],
    [
        tb("Dari temuan ke laporan", "Pemeriksaan yang tersebar di sel-sel notebook tidak banyak membantu orang lain, bahkan Anda sendiri bulan depan. Audit yang baik berakhir dengan satu laporan ringkas: daftar aturan, jumlah pelanggaran masing-masing, dan persentase lolos. Laporan ini menjadi dasar keputusan: mana yang harus diperbaiki sebelum analisis, mana yang cukup dicatat, mana yang menandakan masalah di hulu pengumpulan data. Ia juga berfungsi sebagai bukti kondisi data pada saat analisis, berguna ketika hasil dipertanyakan atau data berubah di kemudian hari."),
        tb("Mengemas aturan dalam kamus", "Cara rapi menyusun audit adalah menyimpan aturan dalam kamus yang memetakan nama aturan ke Series boolean. Dengan begitu, satu perulangan atau satu komprehensi dict menghitung semua pelanggaran, dan menambah aturan baru hanya menambah satu baris. Nama aturan yang deskriptif seperti `umur_valid` atau `email_valid` membuat laporan terbaca tanpa penjelasan. Pola ini juga memudahkan pengujian: setiap aturan dapat diuji dengan tabel kecil yang pelanggarannya sudah diketahui, sehingga Anda yakin aturan itu benar-benar menangkap yang dimaksud."),
        C(
            P("""
pat = r'^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$'
rules = {
    'umur_valid': df['umur'].between(0, 120),
    'email_valid': df['email'].str.match(pat, na=False),
    'id_unik': ~df.duplicated('id', keep=False),
}
print({k: int((~v).sum()) for k, v in rules.items()})
print({k: round(float(v.mean() * 100), 1) for k, v in rules.items()})
ok = pd.concat(rules, axis=1).all(axis=1)
print(ok.tolist(), round(float(ok.mean()), 3))
print(int(ok.sum()), len(df) - int(ok.sum()))
"""),
            ind("""
{'umur_valid': 2, 'email_valid': 2, 'id_unik': 2}
{'umur_valid': 66.7, 'email_valid': 66.7, 'id_unik': 66.7}
[True, False, False, False, False, False] 0.167
1 5
"""),
            "Kamus aturan menghasilkan laporan pelanggaran dan persen lolos. Concat dengan all menandai baris yang lolos semua aturan sekaligus.",
            filename="laporan_audit.py",
        ),
        tb("Baris lolos semua aturan", "Selain pelanggaran per aturan, hitung berapa baris yang lolos seluruh aturan. Pada contoh, hanya satu dari enam baris yang bersih, angka yang sangat berbeda dari enam puluh enam koma tujuh persen lolos per aturan. Pelanggaran tersebar pada baris berbeda, sehingga bila Anda membuang setiap baris yang melanggar satu aturan pun, hampir seluruh data hilang. Perbandingan kedua angka ini membantu memutuskan apakah membuang baris layak atau perbaikan yang lebih halus diperlukan."),
        tb("Prioritas berdasarkan dampak", "Tidak semua pelanggaran sama pentingnya. Prioritas ditentukan oleh dua hal: seberapa banyak baris terdampak dan seberapa penting kolom itu bagi analisis. Pelanggaran pada kolom target atau kunci penggabungan lebih mendesak daripada pada kolom yang tidak dipakai. Urutkan temuan menurut dampak, dan pada hasil seri, urutkan menurut nama agar laporan stabil antar jalannya. Fokuskan upaya perbaikan pada beberapa temuan teratas yang menutup sebagian besar kerusakan, bukan pada kesempurnaan yang mahal dan jarang memberi nilai."),
        C(
            P("""
laporan = {'a': 2, 'b': 5, 'c': 2}
print(sorted(laporan, key=lambda k: (-laporan[k], k)))
print(sorted(laporan.items(), key=lambda kv: -kv[1])[0])
print(max(laporan, key=laporan.get))
print(sum(laporan.values()), [k for k, v in laporan.items() if v >= 2])
"""),
            ind("""
['b', 'a', 'c']
('b', 5)
b
9 ['a', 'b', 'c']
"""),
            "Kunci pengurutan dengan tanda minus menurunkan jumlah, dan nama sebagai pemutus seri menjaga urutan tetap deterministik.",
            filename="prioritas.py",
        ),
        tb("Mencari akar masalah", "Pelanggaran yang tampak banyak sering berasal dari satu akar. Seribu baris dengan kota berejaan berbeda mungkin hanya berasal dari satu formulir yang tidak membakukan isian. Seratus baris duplikat mungkin akibat satu proses yang berjalan dua kali. Sebelum memperbaiki gejala, tanyakan dari mana pelanggaran itu berasal: kelompokkan pelanggaran menurut sumber, tanggal, atau versi sistem. Memperbaiki akar di hulu mencegah masalah muncul kembali pada data kiriman berikutnya, sedangkan memperbaiki gejala hanya menunda masalah yang sama."),
        tb("Mengunci harapan dengan assert", "Setelah memperbaiki data, kunci harapan kualitas dengan pernyataan `assert` di awal alur analisis: id harus unik, umur harus antara nol dan seratus dua puluh, tidak ada kota di luar daftar. Bila data baru melanggar, alur berhenti dengan pesan jelas, bukan menghasilkan angka salah secara diam-diam. Pernyataan ini adalah dokumentasi hidup tentang apa yang Anda anggap benar, dan merupakan bentuk paling sederhana dari kontrak data. Pustaka khusus validasi memperluas gagasan yang sama untuk kasus besar."),
        tb("Mendokumentasikan keputusan", "Setiap keputusan pembersihan perlu dicatat: apa yang diubah, berapa baris terdampak, dan mengapa. Catatan singkat dalam notebook atau berkas README cukup. Dua bulan kemudian, ketika seseorang bertanya mengapa dua puluh baris hilang atau mengapa umur di atas seratus dua puluh diganti kosong, jawabannya sudah tersedia. Dokumentasi juga memaksa Anda berpikir jernih tentang pilihan itu, dan sering membuat Anda menyadari bahwa sebagian keputusan tidak dapat dibenarkan sehingga perlu ditinjau ulang sebelum dipakai lebih jauh."),
        tb("Data mentah tetap utuh", "Prinsip penting audit dan pembersihan: jangan pernah menimpa data mentah. Simpan salinan asli yang tidak diubah, lakukan pembersihan melalui kode yang menghasilkan versi bersih, dan simpan versi bersih terpisah. Dengan begitu pembersihan dapat diulang, ditinjau, dan diperbaiki bila ada keputusan yang ternyata keliru, tanpa kehilangan informasi asli. Ini selaras dengan prinsip reproduksibilitas yang dibahas pada course alur kerja: hasil bersih adalah turunan dari data mentah dan kode, bukan benda yang dirawat tangan."),
        tb("Ringkasan modul", "Anda telah belajar menjalankan profil cepat, mengenali dimensi kualitas data, menulis aturan validasi sebagai kode, menyusun laporan audit, dan menentukan prioritas perbaikan. Pesan utamanya: periksa sebelum percaya, tulis aturan sebagai kode, laporkan dengan angka, dan jangan menimpa data mentah. Modul berikutnya membahas strategi menangani nilai hilang secara lebih dalam, termasuk jenis mekanisme hilang dan pilihan imputasi yang lebih canggih."),
        K("tip", "Kunci harapan kualitas dengan assert di awal alur dan simpan data mentah tanpa diubah. Data baru yang melanggar akan menghentikan alur dengan jelas.", title="Kontrak data"),
        C(
            P("""
def periksa(d):
    assert d['id'].is_unique, 'id tidak unik'
    assert d['umur'].between(0, 120).all(), 'umur di luar rentang'
    return 'lolos'
try:
    periksa(df)
except AssertionError as e:
    print('gagal:', e)
bersih = df.drop_duplicates('id').query('umur >= 0 and umur <= 120')
print(periksa(bersih), len(bersih))
print(bersih['id'].tolist())
"""),
            ind("""
gagal: id tidak unik
lolos 3
[1, 3, 6]
"""),
            "Assert dengan pesan menghentikan alur pada data yang melanggar. Setelah dibersihkan, pemeriksaan yang sama lolos.",
            filename="kontrak_assert.py",
        ),
        tb("Pesan galat yang berguna", "Pernyataan assert sebaiknya menyertakan pesan yang menjelaskan apa yang salah dan, bila mungkin, berapa banyak. Pesan `id tidak unik` jauh lebih membantu daripada AssertionError kosong, apalagi bila disertai jumlah atau contoh baris. Pesan yang baik membuat orang yang menerima galat pada pukul dua pagi dapat langsung memahami masalahnya tanpa membaca kode. Untuk pemeriksaan yang tidak boleh dimatikan oleh opsi optimasi Python, tulis `if ... raise ValueError(...)` agar tetap berjalan di semua mode."),
        tb("Audit berulang", "Audit bukan kegiatan sekali jalan. Data baru terus datang, dan kualitasnya dapat memburuk tanpa disadari: formulir diubah, sensor rusak, sistem hulu diperbarui. Jalankan audit yang sama tiap kali data baru dimuat, simpan hasilnya bersama tanggal, dan bandingkan antar waktu. Tren yang memburuk, misalnya persentase hilang yang naik perlahan, adalah sinyal dini masalah di hulu yang dapat diperbaiki sebelum merusak keputusan. Banyak tim memantau metrik kualitas data seperti mereka memantau metrik layanan."),
        tb("Contoh laporan yang baik", "Laporan audit yang baik pendek: judul dan tanggal, jumlah baris dan kolom, tabel aturan dengan jumlah pelanggaran dan persen lolos, tiga temuan teratas beserta dugaan akar masalah, dan rekomendasi tindakan. Satu halaman cukup. Pembaca utamanya adalah orang yang memutuskan apakah data layak dipakai, bukan sesama analis, sehingga bahasa dan angka harus langsung bermakna bagi mereka. Lampirkan kode audit agar siapa pun dapat menjalankan ulang dan memeriksa angka tersebut."),
        tb("Siapa memiliki data", "Setiap tabel sebaiknya punya pemilik yang bertanggung jawab atas kualitasnya, orang atau tim yang dapat menjawab pertanyaan dan memperbaiki sumber masalah. Tanpa pemilik, temuan audit hanya menjadi daftar keluhan. Cantumkan pemilik pada laporan sehingga temuan mengalir ke orang yang tepat, dan jalin komunikasi rutin dengan pemilik data di hulu supaya perubahan format dan sistem diberitahukan lebih dulu, bukan ditemukan belakangan lewat analisis yang rusak.", ),
        E(
            "B3-01-3-ex1",
            "mudah",
            "Tulis fungsi `laporan_aturan(df)` yang mengembalikan dict jumlah pelanggaran untuk tiga aturan: `umur_valid` (umur 0 sampai 120), `email_valid` (pola `^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$`, kosong dianggap tidak valid), dan `id_unik` (id tidak berulang).",
            ind("""
import pandas as pd

def laporan_aturan(df):
    # TODO: implementasikan
    pass
"""),
            P("""
assert laporan_aturan(df) == {'umur_valid': 2, 'email_valid': 2, 'id_unik': 2}
assert laporan_aturan(df.iloc[[0]]) == {'umur_valid': 0, 'email_valid': 0, 'id_unik': 0}
assert laporan_aturan(df.iloc[[2, 3]]) == {'umur_valid': 0, 'email_valid': 0, 'id_unik': 2}
assert laporan_aturan(df.iloc[[1, 4]])['umur_valid'] == 2
"""),
            "Kamus aturan boolean lalu hitung yang tidak lolos.",
            X(H11),
        ),
        E(
            "B3-01-3-ex2",
            "sedang",
            "Tulis fungsi `persen_lolos(df)` yang mengembalikan dict persentase baris yang lolos tiap aturan yang sama (`umur_valid`, `email_valid`, `id_unik`), dibulatkan satu desimal.",
            ind("""
import pandas as pd

def persen_lolos(df):
    # TODO: implementasikan
    pass
"""),
            P("""
assert persen_lolos(df) == {'umur_valid': 66.7, 'email_valid': 66.7, 'id_unik': 66.7}
assert persen_lolos(df.iloc[[0]]) == {'umur_valid': 100.0, 'email_valid': 100.0, 'id_unik': 100.0}
assert persen_lolos(df.iloc[[0, 1]])['umur_valid'] == 50.0
assert persen_lolos(df.iloc[[2, 3]])['id_unik'] == 0.0
"""),
            "Rata-rata Series boolean dikali seratus.",
            X(H12),
        ),
        E(
            "B3-01-3-ex3",
            "sedang",
            "Tulis fungsi `baris_lolos_semua(df)` yang mengembalikan bilangan bulat jumlah baris yang lolos ketiga aturan sekaligus.",
            ind("""
import pandas as pd

def baris_lolos_semua(df):
    # TODO: implementasikan
    pass
"""),
            P("""
assert baris_lolos_semua(df) == 1
assert baris_lolos_semua(df.iloc[[0]]) == 1
assert baris_lolos_semua(df.iloc[[1, 4, 5]]) == 0
assert baris_lolos_semua(df.iloc[[0, 5]]) == 1
"""),
            "Gabungkan aturan dengan operator dan lalu jumlahkan.",
            X(H13),
        ),
        E(
            "B3-01-3-ex4",
            "menantang",
            "Tulis fungsi `prioritas(laporan)` yang menerima dict `{aturan: jumlah_pelanggaran}` dan mengembalikan list nama aturan dari pelanggaran terbanyak, dengan pemutus seri menurut abjad.",
            ind("""
import pandas as pd

def prioritas(laporan):
    # TODO: implementasikan
    pass
"""),
            P("""
assert prioritas({'a': 2, 'b': 5, 'c': 2}) == ['b', 'a', 'c']
assert prioritas({'x': 0}) == ['x']
assert prioritas({'b': 1, 'a': 1}) == ['a', 'b']
assert prioritas({}) == []
"""),
            "sorted dengan kunci minus jumlah lalu nama.",
            X(H14),
        ),
    ],
    [
        M("Menyebar pemeriksaan di banyak sel tanpa laporan.", "Susun kamus aturan dan satu laporan ringkas."),
        M("Memperbaiki gejala tanpa mencari akar.", "Kelompokkan pelanggaran menurut sumber."),
        M("Menimpa data mentah dengan versi bersih.", "Simpan mentah utuh dan hasilkan bersih lewat kode."),
    ],
    [
        Q("Kamus aturan memetakan?", ["Nama aturan ke Series boolean", "Kolom ke tipe", "Baris ke id", "Nilai ke label"], 0, "Rapi.", hint="Boolean."),
        Q("Baris lolos semua biasanya?", ["Lebih sedikit dari lolos per aturan", "Lebih banyak", "Sama", "Nol"], 0, "Pelanggaran tersebar.", hint="Sedikit."),
        Q("Prioritas ditentukan oleh?", ["Dampak dan pentingnya kolom", "Abjad", "Urutan kolom", "Acak"], 0, "Dampak.", hint="Dampak."),
        Q("assert di awal alur berfungsi sebagai?", ["Kontrak data", "Hiasan", "Cache", "Log"], 0, "Menghentikan data buruk.", hint="Kontrak."),
        Q("Data mentah sebaiknya?", ["Tidak diubah", "Ditimpa", "Dihapus", "Dikompres saja"], 0, "Sumber kebenaran.", hint="Utuh."),
    ],
    [
        "Laporan audit merangkum pelanggaran dan persen lolos per aturan.",
        "Kamus aturan memudahkan penambahan dan pengujian aturan.",
        "Prioritas ditentukan oleh dampak dan pentingnya kolom.",
        "Assert dan dokumentasi mengunci harapan, dan data mentah tetap utuh.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perintah yang cukup jelas dalam teks.", "brief": []}

write_module(
    "B3",
    1,
    "Audit kualitas data",
    105,
    [
        "Menjalankan profil cepat pada tabel yang belum dikenal",
        "Menulis aturan validasi sebagai kode untuk beberapa dimensi kualitas",
        "Menyusun laporan audit dan menentukan prioritas perbaikan",
    ],
    [l1, l2, l3],
    video,
    REF,
)
