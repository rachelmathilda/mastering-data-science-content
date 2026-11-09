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
    'umur': [22, 25, np.nan, 31, 35, np.nan, 41, 45],
    'gaji': [5.0, 6.0, 6.5, np.nan, 8.0, 9.0, np.nan, 11.0],
    'kota': ['A', 'A', 'B', None, 'B', 'A', 'B', 'A'],
    'lulus': [0, 0, 1, 1, 1, 0, 1, 1],
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

def pola_hilang(df):
    return df.isna().astype(int).astype(str).agg(''.join, axis=1).tolist()
"""
F12 = """
import pandas as pd

def rata_menurut_hilang(df, cek, nilai):
    return df.groupby(df[cek].isna())[nilai].mean().round(2).to_dict()
"""
F13 = """
import pandas as pd

def hilang_bersama(df, a, b):
    return int((df[a].isna() & df[b].isna()).sum())
"""
F14 = """
import pandas as pd

def hitung_pola(df):
    pola = df.isna().astype(int).astype(str).agg(''.join, axis=1)
    return pola.value_counts().to_dict()
"""

l1 = lesson(
    "B3-02-1",
    "Mengapa data hilang: tiga mekanisme",
    35,
    [
        "Membedakan hilang acak penuh, hilang acak bersyarat, dan hilang tidak acak",
        "Memeriksa apakah hilangnya nilai berkaitan dengan kolom lain",
        "Membaca pola hilang antar kolom",
        "Menilai dampak tiap mekanisme pada rata-rata",
    ],
    [
        tb("Hilang itu punya alasan", "Pada modul sebelumnya Anda belajar mengisi atau membuang nilai hilang. Namun cara yang benar bergantung pada pertanyaan yang lebih dasar: mengapa nilai itu hilang. Data yang hilang karena sensor kehabisan baterai secara acak berbeda dari gaji yang hilang karena orang berpenghasilan tinggi enggan melaporkannya. Mengisi keduanya dengan rata-rata menghasilkan kesimpulan yang sangat berbeda kualitasnya. Pelajaran ini mengenalkan tiga mekanisme hilang yang diperkenalkan statistikawan Donald Rubin, dan cara memeriksa mekanisme mana yang paling mungkin bekerja pada data Anda."),
        tb("Hilang acak penuh", "Mekanisme pertama adalah hilang acak penuh, disingkat MCAR dari missing completely at random. Probabilitas sebuah nilai hilang tidak bergantung pada apa pun, baik nilai itu sendiri maupun kolom lain. Contohnya tabung sampel yang pecah secara kebetulan atau sambungan jaringan yang putus acak. Pada kondisi ini, data yang tersisa adalah sampel acak dari seluruh data, sehingga membuang baris yang hilang tidak membiaskan hasil, hanya mengurangi jumlah data. MCAR adalah skenario paling ramah, tetapi juga yang paling jarang terjadi dalam data nyata, dan jarang dapat dibuktikan, hanya dapat diuji bahwa tidak ada bukti yang menolaknya."),
        tb("Hilang acak bersyarat", "Mekanisme kedua adalah hilang acak bersyarat, atau MAR dari missing at random. Probabilitas hilang bergantung pada kolom lain yang teramati, tetapi tidak pada nilai yang hilang itu sendiri setelah memperhitungkan kolom lain. Contohnya, pelanggan muda lebih sering melewatkan kolom pendapatan, sehingga hilang berkaitan dengan umur yang kita ketahui. Pada kondisi ini membuang baris dapat membiaskan, tetapi imputasi yang memanfaatkan kolom lain, seperti rata-rata per kelompok umur atau model regresi, dapat memperbaikinya. MAR adalah asumsi kerja yang paling umum dalam metode imputasi modern, walau namanya menyesatkan karena hilangnya tidak benar-benar acak."),
        tb("Hilang tidak acak", "Mekanisme ketiga adalah hilang tidak acak, atau MNAR dari missing not at random. Probabilitas hilang bergantung pada nilai yang hilang itu sendiri. Orang berpenghasilan sangat tinggi menyembunyikan gajinya, pasien yang sangat sakit tidak datang ke pemeriksaan lanjutan, atau sensor jenuh dan tidak merekam nilai di atas batas tertentu. Ini mekanisme paling berbahaya karena informasi tentang mengapa hilang ada pada nilai yang tidak kita punya. Tidak ada teknik statistik murni yang memperbaikinya tanpa asumsi tambahan, sehingga solusinya biasanya berupa pengetahuan domain, data tambahan, atau analisis sensitivitas yang menguji seberapa goyah kesimpulan terhadap asumsi."),
        tb("Data contoh", "Pelajaran ini memakai tabel delapan orang dengan kolom `umur`, `gaji` dalam juta, `kota`, dan `lulus` bernilai nol atau satu. Umur hilang pada dua orang, gaji pada dua orang, dan kota pada satu orang. Tidak ada yang hilang pada `lulus`, sehingga kolom itu dapat dipakai untuk bertanya apakah hilangnya kolom lain berkaitan dengan hasil. Tabel kecil ini dapat Anda periksa dengan mata, sementara teknik yang sama diterapkan pada tabel besar sehingga pola tidak dapat lagi dilihat langsung dan harus dihitung."),
        C(
            P("""
print(df.isna().sum().to_dict(), df.isna().sum().sum())
m = df['gaji'].isna()
print(m.tolist())
print(df.groupby(m)['umur'].mean().round(2).to_dict())
print(df.groupby(m)['lulus'].mean().round(2).to_dict())
print(df.groupby(df['umur'].isna())['gaji'].mean().round(2).to_dict())
print(df.isna().sum(axis=1).tolist())
"""),
            ind("""
{'umur': 2, 'gaji': 2, 'kota': 1, 'lulus': 0} 5
[False, False, False, True, False, False, True, False]
{False: 31.75, True: 36.0}
{False: 0.5, True: 1.0}
{False: 7.5, True: 7.75}
[0, 0, 1, 2, 0, 1, 1, 0]
"""),
            "Mengelompokkan menurut penanda hilang membandingkan kolom lain antara baris yang hilang dan yang lengkap. Selisih besar menandakan hilang berkaitan dengan kolom itu.",
            filename="periksa_hilang.py",
        ),
        tb("Menguji dengan membandingkan kelompok", "Cara praktis menyelidiki mekanisme adalah membandingkan baris yang nilainya hilang dengan yang lengkap pada kolom lain. Buat penanda `df['gaji'].isna()`, lalu hitung rata-rata kolom lain per kelompok penanda. Pada contoh, orang dengan gaji hilang memiliki rata-rata umur tiga puluh enam, lebih tinggi dari tiga puluh satu koma tujuh puluh lima pada yang lengkap, dan semuanya lulus sedangkan yang lengkap hanya separuh. Dengan hanya delapan baris perbedaan ini bisa kebetulan, tetapi pada data besar perbedaan konsisten adalah bukti bahwa hilang bukan MCAR."),
        tb("Batas dari pengujian", "Perlu diingat bahwa membandingkan kelompok hanya dapat mendeteksi ketergantungan pada kolom yang teramati, yaitu bukti terhadap MCAR. Pengujian tidak dapat membedakan MAR dari MNAR, karena itu memerlukan nilai yang hilang itu sendiri. Anda tidak pernah dapat membuktikan bahwa hilang adalah MAR, hanya meyakininya berdasarkan pemahaman tentang proses pengumpulan data. Karena itu wawancara dengan orang yang mengumpulkan data sering lebih informatif daripada statistik apa pun: mereka tahu kapan sensor mati, formulir mana yang opsional, dan siapa yang cenderung melewatkan pertanyaan."),
        tb("Pola hilang antar kolom", "Selain per kolom, lihat pola hilang antar kolom: baris mana yang hilang bersamaan. Ubah tabel hilang menjadi teks nol dan satu per baris, lalu hitung frekuensi tiap pola. Pada contoh, empat baris lengkap, dua baris hanya hilang umur, satu hanya hilang gaji, dan satu hilang gaji dan kota sekaligus. Pola yang sering muncul bersama menandakan penyebab bersama, misalnya satu formulir yang melewatkan beberapa kolom sekaligus. Mengenali pola membantu menemukan akar masalah dan memilih strategi, misalnya membuang kolom yang selalu hilang bersamaan bila memang tidak berguna."),
        C(
            P("""
pola = df.isna().astype(int).astype(str).agg(''.join, axis=1)
print(pola.tolist())
print(pola.value_counts().to_dict())
print((df['gaji'].isna() & df['kota'].isna()).sum(), (df['umur'].isna() & df['gaji'].isna()).sum())
print(df.isna().astype(int).corr().round(2).loc['umur', 'gaji'])
print(df['umur'].mean(), df['umur'].median(), df['gaji'].mean(), df['gaji'].median(), df['kota'].mode().tolist())
"""),
            ind("""
['0000', '0000', '1000', '0110', '0000', '1000', '0100', '0000']
{'0000': 4, '1000': 2, '0110': 1, '0100': 1}
1 0
-0.33
33.166666666666664 33.0 7.583333333333333 7.25 ['A']
"""),
            "Pola nol dan satu per baris merangkum hilang antar kolom. Korelasi antar penanda hilang menunjukkan kolom yang cenderung hilang bersama atau saling meniadakan.",
            filename="pola_hilang.py",
        ),
        tb("Simulasi dampak mekanisme", "Cara terbaik memahami bahayanya MNAR adalah mensimulasikannya. Ambil sepuluh nilai satu sampai sepuluh dengan rata-rata lima koma lima. Bila tiga nilai dibuang secara acak, rata-rata sisanya sekitar lima koma tujuh dan masih dekat dengan kebenaran. Bila tiga nilai terbesar yang hilang, rata-rata sisanya hanya empat, jauh meleset. Tidak ada teknik pengisian yang dapat memperbaikinya hanya dari nilai sisa, karena nilai yang hilang sistematis lebih besar. Itulah mengapa memahami proses hilang lebih penting daripada memilih algoritma imputasi."),
        C(
            S("""
x = pd.Series(np.arange(1, 11.0))
print(x.mean())
print(round(x.drop([1, 4, 7]).mean(), 3))
print(x[x < 8].mean())
print(round(x.fillna(x.mean()).mean(), 1))
print(x.drop([1, 4, 7]).mean() - x.mean() < 0.0, x[x < 8].mean() - x.mean())
"""),
            ind("""
5.5
5.714
4.0
5.5
False -1.5
"""),
            "Membuang tiga nilai acak sedikit menggeser rata-rata, sedangkan membuang tiga nilai terbesar menggesernya jauh. Pola hilang sistematis tidak dapat dipulihkan dari nilai yang tersisa.",
            filename="simulasi_mekanisme.py",
        ),
        tb("Konsekuensi untuk keputusan", "Hasil simulasi menunjukkan alasan memilah mekanisme. Bila Anda menduga MCAR, membuang baris hilang aman dan sederhana. Bila MAR, imputasi yang memakai kolom lain layak dan dapat memperbaiki bias. Bila MNAR, tidak ada jalan pintas: kumpulkan data tambahan, modelkan proses hilang secara eksplisit, atau laporkan hasil dengan peringatan jujur dan analisis sensitivitas. Dokumentasikan asumsi mekanisme dalam laporan agar pembaca dapat menilai kokohnya kesimpulan, dan jangan menyembunyikan ketidakpastian ini di balik angka yang tampak pasti."),
        tb("Pertanyaan untuk pengumpul data", "Sebelum menyelam ke kode, ajukan pertanyaan sederhana kepada orang yang mengumpulkan data. Apakah kolom ini wajib diisi? Apakah ada kondisi tertentu yang membuatnya sering kosong? Apakah ada perubahan formulir atau sistem pada tanggal tertentu? Apakah kosong berarti tidak ada atau tidak diketahui? Jawaban atas pertanyaan seperti ini sering menyingkap mekanisme dalam lima menit, sesuatu yang tidak dapat dilakukan analisis statistik selama berjam-jam. Catat jawabannya sebagai bagian dari kamus data."),
        K("warn", "Anda tidak dapat membuktikan bahwa hilang adalah MAR dari data itu sendiri. Asumsi mekanisme harus didukung pengetahuan tentang proses pengumpulan data.", title="Asumsi, bukan fakta"),
        E(
            "B3-02-1-ex1",
            "mudah",
            "Tulis fungsi `pola_hilang(df)` yang mengembalikan list teks per baris berisi `0` untuk sel terisi dan `1` untuk sel kosong, berurutan menurut kolom.",
            ind("""
import pandas as pd

def pola_hilang(df):
    # TODO: implementasikan
    pass
"""),
            P("""
assert pola_hilang(df) == ['0000', '0000', '1000', '0110', '0000', '1000', '0100', '0000']
assert pola_hilang(df[['umur']].iloc[:3]) == ['0', '0', '1']
assert pola_hilang(df[['gaji', 'kota']].iloc[[3]]) == ['11']
assert pola_hilang(df.dropna()) == ['0000'] * 4
"""),
            "isna ke bilangan bulat ke teks lalu gabungkan per baris.",
            X(F11),
        ),
        E(
            "B3-02-1-ex2",
            "sedang",
            "Tulis fungsi `rata_menurut_hilang(df, cek, nilai)` yang mengembalikan dict `{hilang: rata_rata_nilai}` dengan kunci `False` dan `True` menurut apakah kolom `cek` kosong, dibulatkan dua desimal.",
            ind("""
import pandas as pd

def rata_menurut_hilang(df, cek, nilai):
    # TODO: implementasikan
    pass
"""),
            P("""
assert rata_menurut_hilang(df, 'gaji', 'umur') == {False: 31.75, True: 36.0}
assert rata_menurut_hilang(df, 'umur', 'gaji') == {False: 7.5, True: 7.75}
assert rata_menurut_hilang(df, 'gaji', 'lulus') == {False: 0.5, True: 1.0}
assert rata_menurut_hilang(df, 'lulus', 'umur') == {False: 33.17}
"""),
            "groupby menurut isna kolom cek lalu rata-rata kolom nilai.",
            X(F12),
        ),
        E(
            "B3-02-1-ex3",
            "sedang",
            "Tulis fungsi `hilang_bersama(df, a, b)` yang mengembalikan bilangan bulat jumlah baris yang kolom `a` dan `b`-nya sama-sama kosong.",
            ind("""
import pandas as pd

def hilang_bersama(df, a, b):
    # TODO: implementasikan
    pass
"""),
            P("""
assert hilang_bersama(df, 'gaji', 'kota') == 1
assert hilang_bersama(df, 'umur', 'gaji') == 0
assert hilang_bersama(df, 'umur', 'umur') == 2
assert hilang_bersama(df, 'lulus', 'umur') == 0
"""),
            "Gabungkan dua isna dengan operator dan lalu jumlahkan.",
            X(F13),
        ),
        E(
            "B3-02-1-ex4",
            "menantang",
            "Tulis fungsi `hitung_pola(df)` yang mengembalikan dict `{pola: jumlah_baris}` dengan pola berupa teks nol dan satu per baris seperti pada latihan pertama.",
            ind("""
import pandas as pd

def hitung_pola(df):
    # TODO: implementasikan
    pass
"""),
            P("""
assert hitung_pola(df) == {'0000': 4, '1000': 2, '0110': 1, '0100': 1}
assert hitung_pola(df.dropna()) == {'0000': 4}
assert hitung_pola(df[['umur']]) == {'0': 6, '1': 2}
assert sum(hitung_pola(df).values()) == 8
"""),
            "Bangun pola teks per baris lalu value_counts ke dict.",
            X(F14),
        ),
    ],
    [
        M("Menganggap semua hilang itu acak.", "Periksa apakah hilang berkaitan dengan kolom lain."),
        M("Mengira statistik dapat membuktikan MAR.", "Dukung asumsi dengan pengetahuan proses pengumpulan data."),
        M("Mengabaikan pola hilang antar kolom.", "Hitung frekuensi pola untuk menemukan penyebab bersama."),
    ],
    [
        Q("MCAR berarti hilang?", ["Tidak bergantung pada apa pun", "Bergantung kolom lain", "Bergantung nilai itu sendiri", "Selalu di akhir"], 0, "Acak penuh.", hint="Acak penuh."),
        Q("MAR berarti hilang bergantung pada?", ["Kolom lain teramati", "Nilai hilang itu", "Tidak ada", "Urutan baris"], 0, "Bersyarat.", hint="Kolom lain."),
        Q("MNAR paling berbahaya karena?", ["Bergantung pada nilai yang hilang", "Terlalu banyak", "Terlalu sedikit", "Tipe salah"], 0, "Tak terlihat.", hint="Nilai sendiri."),
        Q("Membandingkan kelompok hilang dapat?", ["Menolak MCAR", "Membuktikan MAR", "Membuktikan MNAR", "Mengisi nilai"], 0, "Hanya indikasi.", hint="MCAR."),
        Q("Pola hilang antar kolom membantu?", ["Menemukan penyebab bersama", "Mengurutkan", "Menggabung", "Menghapus kolom"], 0, "Pola.", hint="Penyebab."),
    ],
    [
        "MCAR, MAR, dan MNAR adalah tiga mekanisme hilang dengan implikasi berbeda.",
        "Membandingkan kelompok hilang dan lengkap menguji ketergantungan pada kolom lain.",
        "Pola hilang antar kolom menunjukkan penyebab bersama.",
        "Asumsi mekanisme harus didukung pengetahuan proses data.",
    ],
    [],
)

G11 = """
import pandas as pd

def isi_median_grup(df, kolom, grup):
    return df[kolom].fillna(df.groupby(grup)[kolom].transform('median')).tolist()
"""
G12 = """
import pandas as pd

def isi_modus(df, kolom):
    return df[kolom].fillna(df[kolom].mode()[0]).tolist()
"""
G13 = """
import pandas as pd

def isi_dengan_statistik_latih(df, n):
    kolom = ['umur', 'gaji']
    med = df.iloc[:n][kolom].median()
    return df.iloc[n:][kolom].fillna(med).values.tolist()
"""
G14 = """
import pandas as pd

def tandai_dan_isi(df, kolom):
    penanda = df[kolom].isna().astype(int)
    isi = df[kolom].fillna(df[kolom].median())
    return pd.concat([penanda, isi], axis=1).values.tolist()
"""

l2 = lesson(
    "B3-02-2",
    "Imputasi sederhana yang aman",
    35,
    [
        "Mengisi dengan median, modus, dan statistik per kelompok",
        "Menghitung statistik pengisi hanya dari data latih",
        "Memakai SimpleImputer dengan fit dan transform",
        "Menambah penanda hilang sebagai fitur",
    ],
    [
        tb("Imputasi sebagai model kecil", "Mengisi nilai hilang dengan rata-rata tampak sepele, tetapi sebenarnya Anda sedang membangun model prediksi paling sederhana: tebakan satu angka untuk semua. Memahami hal ini mengubah cara berpikir. Seperti model lain, imputasi punya parameter yang dipelajari dari data, yaitu rata-rata atau median, dan ia dapat salah, bias, atau membocorkan informasi. Pelajaran ini membahas imputasi sederhana yang dilakukan dengan benar: pilih statistik yang tepat, hitung dari bagian data yang tepat, dan simpan jejak bahwa nilai itu hasil pengisian."),
        tb("Median, rata-rata, dan modus", "Untuk kolom angka, median biasanya lebih aman daripada rata-rata karena tidak tertarik pencilan. Pada kolom gaji dengan satu nilai ekstrem, rata-rata bisa sangat menyesatkan. Untuk kolom kategori, modus, yaitu nilai paling sering, adalah pilihan alami, atau kategori khusus seperti `Tidak diketahui` bila alasan hilang tak jelas. Rata-rata cocok bila sebaran simetris dan Anda memerlukan pengisian yang mempertahankan jumlah total. Pilihan ini kecil tetapi memengaruhi hasil, sehingga catat dan, bila perlu, bandingkan dua pilihan."),
        tb("Imputasi per kelompok", "Bila ada kolom yang berkaitan dengan nilai hilang, hitung statistik per kelompok kolom itu. Rata-rata umur orang yang lulus berbeda dari yang tidak lulus, sehingga mengisi umur hilang dengan median kelompoknya lebih masuk akal daripada median global. Polanya `fillna(groupby(g)[x].transform('median'))`. Perhatikan dua jebakan: kelompok yang seluruh anggotanya hilang menghasilkan NaN, dan kelompok yang kuncinya sendiri hilang juga tidak terisi. Siapkan pengisi cadangan global untuk sisa yang tidak terisi, dan periksa jumlah hilang setelahnya."),
        C(
            P("""
print(df['umur'].fillna(df['umur'].median()).tolist())
print(df.groupby('lulus')['umur'].transform('median').tolist())
print(df['umur'].fillna(df.groupby('lulus')['umur'].transform('median')).tolist())
print(df['gaji'].fillna(df.groupby('kota')['gaji'].transform('median')).tolist())
print(df['kota'].fillna('?').tolist(), df['kota'].fillna(df['kota'].mode()[0]).tolist())
print(df['gaji'].fillna(df.groupby('kota')['gaji'].transform('median')).fillna(df['gaji'].median()).tolist())
"""),
            ind("""
[22.0, 25.0, 33.0, 31.0, 35.0, 33.0, 41.0, 45.0]
[23.5, 23.5, 38.0, 38.0, 38.0, 23.5, 38.0, 38.0]
[22.0, 25.0, 38.0, 31.0, 35.0, 23.5, 41.0, 45.0]
[5.0, 6.0, 6.5, nan, 8.0, 9.0, 7.25, 11.0]
['A', 'A', 'B', '?', 'B', 'A', 'B', 'A'] ['A', 'A', 'B', 'A', 'B', 'A', 'B', 'A']
[5.0, 6.0, 6.5, 7.25, 8.0, 9.0, 7.25, 11.0]
"""),
            "Median per kelompok memakai kolom penjelas. Baris yang kelompoknya sendiri hilang tetap NaN, sehingga memerlukan pengisi cadangan global.",
            filename="isi_sederhana.py",
        ),
        tb("Kebocoran dari data uji", "Dalam pemodelan, data dibagi menjadi data latih dan data uji. Bila Anda menghitung median dari seluruh data lalu membaginya, median itu sudah memuat informasi dari data uji, kebocoran halus yang membuat skor evaluasi terlalu optimistis. Aturan yang benar: hitung statistik pengisi hanya dari data latih, lalu pakai angka yang sama untuk mengisi data latih dan data uji. Pada penerapan nyata, data baru yang masuk harus diisi dengan statistik yang tersimpan dari pelatihan, bukan dihitung ulang dari data baru itu."),
        tb("fit dan transform", "Pustaka scikit-learn menerapkan aturan ini lewat pola `fit` dan `transform`. Objek `SimpleImputer` mempelajari statistik pengisi pada `fit` dari data latih dan menyimpannya pada atribut `statistics_`. Metode `transform` kemudian memakai statistik tersimpan itu pada data mana pun. Pemisahan dua langkah ini memastikan data uji tidak memengaruhi statistik. Strategi yang tersedia mencakup `mean`, `median`, `most_frequent`, dan `constant`. Karena imputer dapat disimpan bersama model, data baru di produksi diisi persis seperti saat pelatihan."),
        C(
            P("""
from sklearn.impute import SimpleImputer
X = df[['umur', 'gaji']]
si = SimpleImputer(strategy='median')
print(si.fit_transform(X).tolist())
print(si.statistics_.tolist())
tr, te = X.iloc[:5], X.iloc[5:]
si2 = SimpleImputer(strategy='median').fit(tr)
print(si2.statistics_.tolist(), si2.transform(te).tolist())
print(SimpleImputer(strategy='mean').fit(X).statistics_.round(3).tolist())
"""),
            ind("""
[[22.0, 5.0], [25.0, 6.0], [33.0, 6.5], [31.0, 7.25], [35.0, 8.0], [33.0, 9.0], [41.0, 7.25], [45.0, 11.0]]
[33.0, 7.25]
[28.0, 6.25] [[28.0, 9.0], [41.0, 6.25], [45.0, 11.0]]
[33.167, 7.583]
"""),
            "Fit mempelajari statistik dari data latih, dan transform memakainya pada data uji. Statistik data latih berbeda dari statistik seluruh data.",
            filename="simple_imputer.py",
        ),
        tb("Statistik latih berbeda", "Pada contoh, median seluruh data adalah tiga puluh tiga untuk umur, sedangkan median lima baris pertama hanya dua puluh delapan. Bila baris berikutnya diisi dengan dua puluh delapan, itulah yang akan terjadi di produksi: Anda tidak tahu median masa depan. Memakai tiga puluh tiga berarti secara diam-diam memakai informasi dari baris yang sedang diisi. Perbedaan seperti ini tampak kecil, tetapi pada banyak fitur dan dataset kecil, kebocoran yang menumpuk dapat menggeser skor evaluasi secara berarti dan membuat model tampak lebih baik dari kenyataan."),
        tb("Penanda hilang sebagai fitur", "Sering kali fakta bahwa nilai hilang itu sendiri informatif. Orang yang tidak mengisi gaji mungkin berbeda dari yang mengisi. Tambahkan kolom penanda nol dan satu sebelum mengisi, sehingga model dapat belajar dari pola ketiadaan. `SimpleImputer(add_indicator=True)` menambahkan penanda otomatis untuk kolom yang memiliki hilang pada data latih. Penanda murah dan sering menolong, terutama pada MNAR di mana ketiadaan berkaitan dengan nilai yang tak teramati. Perhatikan jumlah kolom bertambah, dan penanda tidak berguna bila hilang benar-benar acak."),
        C(
            P("""
from sklearn.impute import SimpleImputer
X = df[['umur', 'gaji']]
si3 = SimpleImputer(strategy='median', add_indicator=True)
out = si3.fit_transform(X)
print(out.shape, out[:, 2:].tolist()[:3])
for c in ['umur', 'gaji']:
    f = df[c].fillna(df[c].median())
    i = df[c].isna().astype(int)
    print(pd.concat([i, f], axis=1).values.tolist()[2:4])
print(df.assign(umur_hilang=df['umur'].isna().astype(int))['umur_hilang'].tolist())
"""),
            ind("""
(8, 4) [[0.0, 0.0], [0.0, 0.0], [1.0, 0.0]]
[[1.0, 33.0], [0.0, 31.0]]
[[0.0, 6.5], [1.0, 7.25]]
[0, 0, 1, 0, 0, 1, 0, 0]
"""),
            "Penanda hilang disimpan berdampingan dengan nilai terisi. Add_indicator menambah kolom penanda otomatis dan menyimpan jejak hilang.",
            filename="penanda.py",
        ),
        tb("Kapan cukup sederhana", "Imputasi sederhana sering cukup. Bila hilang di bawah lima persen dan mendekati acak, median atau modus bekerja baik dan hasilnya hampir tidak berbeda dari metode canggih. Imputasi sederhana juga mudah dijelaskan, dapat diaudit, dan cepat. Naiklah ke metode lanjutan hanya bila hilang banyak, bila kolom saling berkaitan kuat sehingga informasinya dapat dimanfaatkan, atau bila evaluasi menunjukkan bahwa imputasi sederhana merusak hasil. Prinsipnya sama seperti pada banyak keputusan pemodelan: mulai dari yang paling sederhana dan naik hanya bila ada bukti perlunya."),
        K("warn", "Hitung statistik pengisi hanya dari data latih, lalu pakai angka yang sama untuk data uji dan data baru. Menghitungnya dari seluruh data membocorkan informasi.", title="Hindari kebocoran"),
        tb("Imputasi dan proporsi kategori", "Mengisi kategori hilang dengan modus punya efek samping yang perlu disadari: kategori yang paling sering menjadi makin dominan. Pada contoh kota, A muncul empat kali dan B tiga kali, tetapi setelah modus mengisi satu nilai hilang A menjadi lima. Bila hilang banyak, distribusi kategori bergeser dan model dapat belajar bahwa A lebih umum dari kenyataan. Alternatif yang lebih jujur adalah membuat kategori tersendiri bernama Tidak diketahui, sehingga informasi bahwa nilai itu tidak ada tetap terlihat dan tidak mencampuri kategori sungguhan. Pilihan ini sangat bergantung pada makna hilang dalam konteks data Anda."),
        tb("Imputasi pada data berderet waktu", "Untuk data yang berurutan menurut waktu, mengisi dengan median seluruh deret sering buruk karena mengabaikan tren. Nilai suhu pukul tiga pagi lebih mirip nilai pukul dua dan empat daripada rata-rata sepanjang hari. Pilihan yang lebih wajar adalah mengisi dengan nilai sebelumnya, nilai sesudahnya, atau interpolasi antara keduanya. Namun hati-hati dengan mengisi dari nilai sesudahnya pada data prediksi, karena itu memakai informasi masa depan yang tidak tersedia saat prediksi sungguhan dilakukan. Aturan kebocoran tetap berlaku: hanya pakai informasi yang ada pada saat keputusan dibuat."),
        tb("Mencatat apa yang Anda lakukan", "Setiap pengisian adalah keputusan analisis yang memengaruhi hasil, sehingga catat dalam kode dan laporan. Simpan statistik pengisi yang dipakai, jumlah nilai yang diisi per kolom, dan alasan memilih metode. Bila ada orang lain yang mengulang analisis, mereka dapat menghasilkan angka yang sama. Bila hasil berubah drastis ketika metode diganti, itu sinyal bahwa kesimpulan Anda sensitif terhadap imputasi dan perlu dilaporkan sebagai ketidakpastian. Kebiasaan mencatat ini juga memudahkan Anda mendeteksi kesalahan, misalnya kolom yang tanpa sengaja terisi seluruhnya oleh satu nilai."),
        E(
            "B3-02-2-ex1",
            "mudah",
            "Tulis fungsi `isi_median_grup(df, kolom, grup)` yang mengisi nilai hilang `kolom` dengan median kolom itu pada kelompok `grup` dan mengembalikan list hasilnya.",
            ind("""
import pandas as pd

def isi_median_grup(df, kolom, grup):
    # TODO: implementasikan
    pass
"""),
            P("""
assert isi_median_grup(df, 'umur', 'lulus') == [22.0, 25.0, 38.0, 31.0, 35.0, 23.5, 41.0, 45.0]
assert isi_median_grup(df.iloc[[0, 1]], 'umur', 'lulus') == [22.0, 25.0]
assert isi_median_grup(df, 'gaji', 'lulus')[3] == 8.0
assert len(isi_median_grup(df, 'umur', 'lulus')) == 8
"""),
            "fillna dengan groupby transform median.",
            X(G11),
        ),
        E(
            "B3-02-2-ex2",
            "sedang",
            "Tulis fungsi `isi_modus(df, kolom)` yang mengisi nilai hilang `kolom` dengan nilai paling sering dan mengembalikan list hasilnya.",
            ind("""
import pandas as pd

def isi_modus(df, kolom):
    # TODO: implementasikan
    pass
"""),
            P("""
assert isi_modus(df, 'kota') == ['A', 'A', 'B', 'A', 'B', 'A', 'B', 'A']
assert isi_modus(df, 'lulus') == [0, 0, 1, 1, 1, 0, 1, 1]
assert isi_modus(df.iloc[[2, 3]], 'kota') == ['B', 'B']
assert isi_modus(df, 'kota').count('A') == 5
"""),
            "fillna dengan elemen pertama mode.",
            X(G12),
        ),
        E(
            "B3-02-2-ex3",
            "sedang",
            "Tulis fungsi `isi_dengan_statistik_latih(df, n)` yang menghitung median kolom `umur` dan `gaji` dari `n` baris pertama, lalu memakainya mengisi nilai hilang pada baris ke-n dan seterusnya, dan mengembalikan `values.tolist()` baris tersebut.",
            ind("""
import pandas as pd

def isi_dengan_statistik_latih(df, n):
    # TODO: implementasikan
    pass
"""),
            P("""
assert isi_dengan_statistik_latih(df, 5) == [[28.0, 9.0], [41.0, 6.25], [45.0, 11.0]]
assert isi_dengan_statistik_latih(df, 7) == [[45.0, 11.0]]
assert isi_dengan_statistik_latih(df, 4)[0] == [35.0, 8.0]
assert len(isi_dengan_statistik_latih(df, 2)) == 6
"""),
            "median dari bagian latih lalu fillna pada bagian sisanya.",
            X(G13),
        ),
        E(
            "B3-02-2-ex4",
            "menantang",
            "Tulis fungsi `tandai_dan_isi(df, kolom)` yang mengembalikan `values.tolist()` dari tabel dua kolom: penanda nol atau satu untuk nilai hilang, dan nilai yang diisi dengan median kolom itu.",
            ind("""
import pandas as pd

def tandai_dan_isi(df, kolom):
    # TODO: implementasikan
    pass
"""),
            P("""
r = tandai_dan_isi(df, 'umur')
assert r[0] == [0.0, 22.0]
assert r[2] == [1.0, 33.0]
assert r[5] == [1.0, 33.0]
assert tandai_dan_isi(df, 'gaji')[3] == [1.0, 7.25]
"""),
            "Gabungkan penanda isna dan hasil fillna median dengan concat.",
            X(G14),
        ),
    ],
    [
        M("Menghitung median dari seluruh data lalu membagi latih dan uji.", "Hitung dari data latih saja dan pakai ulang."),
        M("Mengisi per kelompok tanpa cadangan.", "Tambahkan pengisi global untuk sisa."),
        M("Membuang jejak bahwa nilai itu hasil pengisian.", "Tambahkan kolom penanda hilang."),
    ],
    [
        Q("Median lebih aman dari rata-rata saat?", ["Ada pencilan", "Data simetris", "Data kategori", "Data kosong"], 0, "Tahan ekstrem.", hint="Pencilan."),
        Q("SimpleImputer mempelajari statistik pada?", ["fit", "transform", "predict", "score"], 0, "Fit.", hint="fit."),
        Q("Statistik pengisi dihitung dari?", ["Data latih", "Seluruh data", "Data uji", "Data baru"], 0, "Cegah kebocoran.", hint="Latih."),
        Q("add_indicator menambah?", ["Kolom penanda hilang", "Baris baru", "Indeks", "Label"], 0, "Jejak.", hint="Penanda."),
        Q("Imputasi per kelompok memakai?", ["groupby transform", "merge", "pivot", "concat"], 0, "Statistik kelompok.", hint="transform."),
    ],
    [
        "Imputasi adalah model kecil yang parameternya dipelajari dari data.",
        "Hitung statistik pengisi hanya dari data latih.",
        "SimpleImputer memisahkan fit dan transform.",
        "Penanda hilang menyimpan jejak ketiadaan.",
    ],
    [],
)

H11 = """
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer

def knn_isi(df):
    X = df[['umur', 'gaji']]
    return KNNImputer(n_neighbors=2).fit_transform(X).round(2).tolist()
"""
H12 = """
import numpy as np
import pandas as pd

def rmse_isi(full, idx, strategi):
    t = full.copy()
    t.loc[idx] = np.nan
    pengisi = getattr(t, strategi)()
    galat = pengisi - full.loc[idx]
    return round(float(np.sqrt((galat ** 2).mean())), 3)
"""
H13 = """
import numpy as np
import pandas as pd

def rasio_simpangan(s):
    s = pd.Series(s, dtype=float)
    return round(float(s.fillna(s.mean()).std() / s.std()), 3)
"""
H14 = """
import numpy as np
import pandas as pd

def isi_interpolasi(s):
    return pd.Series(s, dtype=float).interpolate().tolist()
"""

l3 = lesson(
    "B3-02-3",
    "Imputasi lanjutan dan cara menilainya",
    35,
    [
        "Memakai KNNImputer dan IterativeImputer",
        "Menilai metode imputasi dengan menyembunyikan nilai yang diketahui",
        "Menjelaskan efek imputasi pada simpangan baku dan korelasi",
        "Memutuskan kapan imputasi lanjutan layak dipakai",
    ],
    [
        tb("Memanfaatkan kolom lain", "Imputasi sederhana mengisi dengan satu angka yang sama tanpa melihat baris itu sendiri. Padahal bila umur, gaji, dan pengalaman saling berkaitan, kolom yang terisi pada baris itu memberi petunjuk tentang nilai yang hilang. Imputasi lanjutan memanfaatkan petunjuk ini. Dua yang populer adalah imputasi k tetangga terdekat dan imputasi iteratif. Keduanya tersedia di scikit-learn dan memakai antarmuka fit dan transform yang sama dengan SimpleImputer, sehingga mudah ditukar dan dibandingkan dalam satu alur kerja yang konsisten."),
        tb("Imputasi k tetangga", "KNNImputer mencari k baris yang paling mirip dengan baris yang memiliki nilai hilang, berdasarkan kolom yang terisi pada keduanya, lalu mengisi dengan rata-rata nilai tetangga itu. Idenya intuitif: orang yang mirip dalam umur dan kota kemungkinan bergaji mirip. Kelebihannya tidak mengasumsikan bentuk hubungan tertentu. Kekurangannya, ia peka terhadap skala kolom karena memakai jarak, sehingga kolom perlu distandarkan lebih dulu bila skalanya berbeda jauh, dan menjadi lambat pada data sangat besar karena harus membandingkan banyak baris."),
        C(
            P("""
from sklearn.impute import KNNImputer
X = df[['umur', 'gaji']]
kn = KNNImputer(n_neighbors=2)
print(kn.fit_transform(X).round(2).tolist())
print(X.isna().sum().to_dict())
print(np.isnan(kn.fit_transform(X)).sum())
"""),
            ind("""
[[22.0, 5.0], [25.0, 6.0], [30.0, 6.5], [31.0, 7.0], [35.0, 8.0], [40.0, 9.0], [41.0, 9.5], [45.0, 11.0]]
{'umur': 2, 'gaji': 2}
0
"""),
            "Nilai hilang diisi rata-rata dua tetangga terdekat menurut kolom lain yang terisi. Setelah transform tidak ada NaN tersisa.",
            filename="knn_imputer.py",
        ),
        tb("Imputasi iteratif", "IterativeImputer memodelkan setiap kolom dengan nilai hilang sebagai fungsi kolom lain, biasanya dengan regresi linear, lalu mengisinya berulang-ulang sampai stabil. Pendekatan ini mirip metode MICE dalam statistik. Ia dapat menangkap hubungan linear antar kolom dan sering memberi hasil akurat bila hubungannya kuat. Di scikit-learn, ia masih berstatus eksperimental dan harus diaktifkan dengan `from sklearn.experimental import enable_iterative_imputer`. Hasilnya bergantung pada model dasar dan jumlah iterasi, sehingga evaluasi tetap diperlukan."),
        tb("Menilai dengan menyembunyikan", "Bagaimana memilih antara metode imputasi? Anda tidak punya jawaban benar untuk nilai yang hilang, sehingga caranya menciptakan jawaban benar buatan: ambil baris yang lengkap, sembunyikan beberapa nilai dengan sengaja, isi dengan tiap metode, lalu bandingkan hasil dengan nilai asli memakai galat akar kuadrat rata-rata. Metode dengan galat terkecil layak dipilih. Teknik ini mengganti perdebatan selera dengan bukti dan dapat dilakukan dengan beberapa baris kode. Untuk hasil yang andal, ulangi dengan beberapa pilihan baris tersembunyi."),
        C(
            S("""
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer, KNNImputer
full = pd.DataFrame({'a': [1, 2, 3, 4, 5, 6, 7, 8], 'b': [2, 4, 6, 8, 10, 12, 14, 16]})
t = full.copy()
t.loc[[2, 5], 'b'] = np.nan
for strat in ['mean', 'median']:
    f = t['b'].fillna(getattr(t['b'], strat)())
    err = (f - full['b']).loc[[2, 5]]
    print(strat, f.loc[[2, 5]].tolist(), round(float(np.sqrt((err ** 2).mean())), 3))
print(t['b'].interpolate().tolist())
print(IterativeImputer(random_state=0).fit_transform(t).round(2)[[2, 5], 1].tolist())
print(KNNImputer(n_neighbors=2).fit_transform(t)[[2, 5], 1].tolist())
"""),
            ind("""
mean [9.0, 9.0] 3.0
median [9.0, 9.0] 3.0
[2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0]
[6.0, 12.0]
[6.0, 12.0]
"""),
            "Pada hubungan linear sempurna, imputasi yang memakai kolom lain memulihkan nilai tepat, sedangkan mean dan median meleset tiga satuan.",
            filename="bandingkan_imputasi.py",
        ),
        tb("Hubungan kuat, metode kuat", "Hasil contoh jelas: karena b selalu dua kali a, metode yang memakai a memulihkan b dengan tepat, sedangkan mean dan median hanya menebak sembilan. Pada data nyata hubungan tidak sempurna, tetapi prinsipnya berlaku. Semakin kuat hubungan antar kolom, semakin besar keuntungan imputasi lanjutan. Bila kolom nyaris tidak berkorelasi, imputasi lanjutan tidak lebih baik dari median dan hanya menambah kerumitan. Karena itu periksa korelasi antar kolom sebelum menaruh harapan besar pada metode canggih."),
        tb("Imputasi mengerutkan variasi", "Setiap pengisi satu angka, terutama rata-rata, mengerutkan variasi data. Nilai pengisi berada tepat di tengah, sehingga simpangan baku turun dan korelasi dengan kolom lain melemah. Pada deret contoh, simpangan baku turun dari 2,39 menjadi 1,95 setelah pengisian rata-rata, rasio sekitar 0,816. Efek ini membuat uji statistik tampak lebih yakin daripada seharusnya karena variasi tampak lebih kecil. Bila hasil akhir berupa inferensi, bukan prediksi, gunakan imputasi berganda yang memasukkan ketidakpastian pengisian, atau metode yang menangani data hilang langsung."),
        C(
            S("""
s = pd.Series([1, 2, np.nan, 4, 5, np.nan, 7.0])
print(round(s.std(), 3), round(s.fillna(s.mean()).std(), 3))
print(round(s.fillna(s.mean()).std() / s.std(), 3))
d2 = pd.DataFrame({'x': [1, 2, 3, 4, 5, 6.0], 'y': [2.1, 3.9, np.nan, 8.2, np.nan, 11.8]})
print(round(d2.corr().loc['x', 'y'], 3), round(d2.fillna(d2.mean()).corr().loc['x', 'y'], 3))
print(d2.dropna().shape, round(d2['y'].std(), 3), round(d2['y'].fillna(d2['y'].mean()).std(), 3))
print(pd.Series([1, np.nan, 3, np.nan, np.nan, 6.0]).interpolate().tolist())
"""),
            ind("""
2.387 1.949
0.816
0.999 0.917
(4, 2) 4.363 3.379
[1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
"""),
            "Pengisian rata-rata menurunkan simpangan baku dan melemahkan korelasi. Interpolasi memulihkan deret yang berubah linear.",
            filename="efek_variasi.py",
        ),
        tb("Pelemahan korelasi", "Contoh kedua menunjukkan korelasi x dan y turun dari 0,999 menjadi 0,917 setelah pengisian rata-rata, padahal hubungan sebenarnya hampir sempurna. Pengisi rata-rata menaruh titik datar di tengah yang tidak mengikuti garis, sehingga menarik korelasi ke bawah. Bila tujuan Anda mempelajari hubungan antar kolom, imputasi rata-rata adalah pilihan buruk. Imputasi berbasis regresi memperbaikinya, tetapi dapat membuat hubungan tampak lebih kuat dari kenyataan karena nilai pengisi persis di garis. Imputasi berganda adalah jawaban statistik untuk dilema ini."),
        tb("Kapan membuang lebih baik", "Imputasi bukan selalu jawaban. Bila hilang di bawah lima persen dan acak, membuang baris sering sah dan paling jujur: Anda tidak mengarang apa pun. Bila nilai yang hilang adalah target prediksi, buang barisnya, karena mengisi target berarti melatih model dengan jawaban karangan. Bila sebuah kolom lebih dari separuh kosong, pertimbangkan membuang kolomnya. Imputasi paling berguna di wilayah tengah: hilang cukup banyak sehingga membuang terlalu mahal, tetapi tidak sebanyak itu sehingga isinya hampir seluruhnya karangan."),
        tb("Alur keputusan", "Alur praktis: audit hilang dan mekanismenya, pisahkan data latih dan uji, mulai dengan imputasi sederhana ditambah penanda, ukur apakah hasil model atau analisis berubah bila dibandingkan dengan membuang baris, lalu coba imputasi lanjutan hanya bila ada alasan. Selalu nilai dengan menyembunyikan nilai yang diketahui, dan laporkan metode serta asumsinya. Keputusan yang terdokumentasi dan dapat diuji lebih berharga daripada metode tercanggih yang tidak dapat dibenarkan."),
        tb("Ringkasan modul", "Anda telah belajar tiga mekanisme hilang, cara memeriksa hubungan hilang dengan kolom lain, imputasi sederhana yang bebas kebocoran, serta KNN dan imputasi iteratif beserta cara menilainya dan efek sampingnya pada variasi dan korelasi. Pesan utama: pahami mengapa data hilang, pilih metode sesuai mekanisme, hitung dari data latih, dan nilai dengan bukti. Modul berikutnya membahas duplikat dan inkonsistensi."),
        K("tip", "Nilai metode imputasi dengan menyembunyikan nilai yang diketahui lalu membandingkan galatnya. Bukti mengalahkan selera.", title="Bukti, bukan selera"),
        tb("Skala dan KNN", "Karena KNNImputer memakai jarak, kolom bersatuan besar mendominasi pencarian tetangga. Bila umur berkisar dua puluh sampai enam puluh dan gaji dalam rupiah berkisar jutaan, jarak hampir sepenuhnya ditentukan oleh gaji. Standarkan kolom lebih dulu, misalnya dengan StandardScaler, isi dengan KNN, lalu kembalikan ke skala asal bila diperlukan. Pada contoh kita kedua kolom berskala sebanding sehingga hal ini tidak muncul, tetapi pada data nyata langkah ini hampir selalu perlu. Pilihan k juga memengaruhi hasil: k kecil peka noise, k besar meratakan terlalu banyak."),
        tb("Imputasi berganda", "Imputasi tunggal memperlakukan nilai pengisi seakan-akan nilai asli, padahal ia hanya tebakan. Imputasi berganda membuat beberapa salinan data dengan pengisian berbeda yang diambil dari sebaran kemungkinan, menganalisis tiap salinan, lalu menggabungkan hasil dengan aturan Rubin sehingga ketidakpastian pengisian ikut terhitung dalam galat baku. Untuk analisis inferensi seperti regresi dengan interval kepercayaan, pendekatan ini jauh lebih jujur. IterativeImputer dengan `sample_posterior=True` dapat dipakai untuk menghasilkan pengisian acak berulang, walau pustaka statsmodels menyediakan alat khusus yang lebih lengkap."),
        tb("Menjaga alur tetap bebas kebocoran", "Dalam praktik, taruh imputer di dalam Pipeline bersama model sehingga fit hanya terjadi pada data latih di tiap lipatan validasi silang. Bila Anda mengisi seluruh data lebih dulu lalu melakukan validasi silang, setiap lipatan sudah melihat statistik dari lipatan uji. Pipeline menyelesaikan ini secara otomatis dan juga menyederhanakan penerapan, karena satu objek mengurus pengisian sekaligus prediksi. Kebiasaan ini mengurangi kesalahan paling umum dalam proyek pembelajaran mesin yang melibatkan data hilang."),
        E(
            "B3-02-3-ex1",
            "mudah",
            "Tulis fungsi `knn_isi(df)` yang mengisi kolom `umur` dan `gaji` dengan `KNNImputer(n_neighbors=2)` dan mengembalikan `tolist()` hasilnya yang dibulatkan dua desimal.",
            ind("""
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer

def knn_isi(df):
    # TODO: implementasikan
    pass
"""),
            P("""
r = knn_isi(df)
assert r[2] == [30.0, 6.5]
assert r[3] == [31.0, 7.0]
assert r[0] == [22.0, 5.0]
assert len(r) == 8
"""),
            "KNNImputer dengan fit_transform pada dua kolom lalu round.",
            X(H11),
        ),
        E(
            "B3-02-3-ex2",
            "sedang",
            "Tulis fungsi `rmse_isi(full, idx, strategi)` yang menyembunyikan nilai Series `full` pada indeks `idx`, mengisinya dengan `strategi` (`'mean'` atau `'median'`) dari sisa nilai, dan mengembalikan akar kuadrat rata-rata galat pada posisi tersembunyi, dibulatkan tiga desimal.",
            ind("""
import numpy as np
import pandas as pd

def rmse_isi(full, idx, strategi):
    # TODO: implementasikan
    pass
"""),
            P("""
full = pd.Series([1, 2, 3, 10, 20, 5, 6, 7.0])
assert rmse_isi(full, [7], 'mean') == 0.286
assert rmse_isi(full, [7], 'median') == 2.0
assert rmse_isi(full, [3], 'mean') == 3.714
assert rmse_isi(full, [3], 'median') == 5.0
"""),
            "Salin, set NaN, isi dengan statistik, lalu hitung akar rata-rata kuadrat galat.",
            X(H12),
        ),
        E(
            "B3-02-3-ex3",
            "sedang",
            "Tulis fungsi `rasio_simpangan(s)` yang mengembalikan rasio simpangan baku deret setelah nilai hilang diisi rata-rata terhadap simpangan baku sebelum diisi, dibulatkan tiga desimal.",
            ind("""
import numpy as np
import pandas as pd

def rasio_simpangan(s):
    # TODO: implementasikan
    pass
"""),
            P("""
assert rasio_simpangan([1, np.nan, 3, np.nan, 5]) < 1.0
assert rasio_simpangan([1, 2, np.nan, 4, 5, np.nan, 7]) == 0.816
assert rasio_simpangan([1, 2, 3]) == 1.0
assert rasio_simpangan([2, 4, np.nan, 8]) < 1
"""),
            "std setelah fillna mean dibagi std awal.",
            X(H13),
        ),
        E(
            "B3-02-3-ex4",
            "menantang",
            "Tulis fungsi `isi_interpolasi(s)` yang menerima list angka dengan NaN dan mengembalikan list hasil interpolasi linear.",
            ind("""
import numpy as np
import pandas as pd

def isi_interpolasi(s):
    # TODO: implementasikan
    pass
"""),
            P("""
assert isi_interpolasi([1, np.nan, 3, np.nan, np.nan, 6]) == [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
assert isi_interpolasi([0, np.nan, 10]) == [0.0, 5.0, 10.0]
assert isi_interpolasi([4, 5]) == [4.0, 5.0]
assert isi_interpolasi([2, np.nan, np.nan, 8]) == [2.0, 4.0, 6.0, 8.0]
"""),
            "Series desimal lalu interpolate.",
            X(H14),
        ),
    ],
    [
        M("Memakai imputasi rata-rata lalu menganalisis korelasi.", "Sadari rata-rata melemahkan korelasi, pakai metode yang memakai kolom lain."),
        M("Memilih metode imputasi berdasarkan selera.", "Sembunyikan nilai diketahui dan bandingkan galat."),
        M("Mengisi kolom target dengan imputasi.", "Buang baris yang targetnya hilang."),
    ],
    [
        Q("KNNImputer mengisi dengan?", ["Rata-rata tetangga terdekat", "Median global", "Nol", "Modus"], 0, "Baris mirip.", hint="Tetangga."),
        Q("IterativeImputer perlu diaktifkan lewat?", ["enable_iterative_imputer", "fit_all", "turn_on", "dropna"], 0, "Eksperimental.", hint="enable."),
        Q("Menilai imputasi dengan?", ["Menyembunyikan nilai diketahui", "Melihat grafik saja", "Menebak", "Mengurutkan"], 0, "Galat terukur.", hint="Sembunyikan."),
        Q("Pengisian rata-rata terhadap simpangan baku?", ["Menurunkan", "Menaikkan", "Tetap", "Nol"], 0, "Mengerut.", hint="Turun."),
        Q("Target yang hilang sebaiknya?", ["Dibuang barisnya", "Diisi rata-rata", "Diisi nol", "Diacak"], 0, "Jangan dikarang.", hint="Buang."),
    ],
    [
        "KNN dan imputasi iteratif memanfaatkan kolom lain untuk mengisi nilai hilang.",
        "Sembunyikan nilai yang diketahui untuk membandingkan metode imputasi dengan galat.",
        "Pengisian satu angka mengerutkan variasi dan melemahkan korelasi.",
        "Mulai sederhana dan naik hanya bila ada bukti perlunya.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perintah yang cukup jelas dalam teks.", "brief": []}

write_module(
    "B3",
    2,
    "Strategi missing value",
    105,
    [
        "Membedakan mekanisme hilang dan memeriksanya pada data",
        "Menerapkan imputasi sederhana yang bebas kebocoran",
        "Menilai imputasi lanjutan dengan menyembunyikan nilai yang diketahui",
    ],
    [l1, l2, l3],
    video,
    REF,
)
