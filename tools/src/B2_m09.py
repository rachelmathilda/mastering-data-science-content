import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

DFX = """
import numpy as np
import pandas as pd

idx = pd.date_range('2024-01-29', periods=8, freq='D')
s = pd.Series([10, 12, 9, 15, 14, 20, 18, 22], index=idx, name='v')
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

def irisan_tanggal(s, awal, akhir):
    return s[awal:akhir].tolist()
"""
F12 = """
import pandas as pd

def rata_per_bulan(s):
    return s.groupby(s.index.month).mean().round(2).to_dict()
"""
F13 = """
import pandas as pd

def jumlah_per_hari_pekan(s):
    return s.groupby(s.index.dayofweek).sum().to_dict()
"""
F14 = """
import pandas as pd

def daftar_tanggal(awal, n, freq):
    return pd.date_range(awal, periods=n, freq=freq).strftime('%Y-%m-%d').tolist()
"""

l1 = lesson(
    "B2-09-1",
    "Indeks waktu dan pemotongan tanggal",
    35,
    [
        "Mengubah teks menjadi tanggal dan menjadikannya indeks",
        "Membuat rentang tanggal dengan date_range dan frekuensi",
        "Memotong deret waktu dengan label tanggal",
        "Menghitung dengan Timedelta dan DateOffset",
    ],
    [
        tb("Mengapa waktu istimewa", "Data deret waktu berbeda dari data tabel biasa karena urutan barisnya bermakna. Penjualan hari ini bergantung pada hari kemarin, suhu jam tiga mirip suhu jam dua, dan harga saham tidak dapat diacak tanpa merusak artinya. Karena itu pandas memberi tanggal dan waktu perlakuan khusus: tipe data tersendiri, indeks khusus, pemotongan berbasis label, dan operasi seperti resample dan rolling yang tidak ada untuk tipe lain. Mempelajari perangkat ini membuka seluruh keluarga analisis seperti tren, musiman, dan peramalan yang dibahas lebih dalam pada course deret waktu."),
        tb("Dari teks ke tanggal", "Tanggal yang dibaca dari file hampir selalu berupa teks. Fungsi `pd.to_datetime` mengubahnya menjadi tipe `datetime64`, dan pada kolom ia menghasilkan akses `dt` yang sudah Anda kenal. Setelah menjadi tanggal sungguhan, Anda dapat mengurutkan, mengurangkan, memotong, dan mengelompokkan menurut waktu. Bila format tidak standar, beri argumen `format`, misalnya `'%d/%m/%Y'`. Format ambigu seperti `03/05/2024` bisa berarti tiga Mei atau lima Maret, dan pandas tidak dapat menebaknya dengan aman, sehingga Anda harus menyatakan formatnya secara eksplisit atau memakai `dayfirst=True` dengan penuh kesadaran."),
        tb("Data contoh", "Pelajaran ini memakai deret harian delapan hari yang dimulai Senin 29 Januari 2024 sampai Senin 5 Februari 2024, dengan nilai 10, 12, 9, 15, 14, 20, 18, dan 22. Rentang ini sengaja melintasi pergantian bulan agar Anda melihat bagaimana pemotongan dan pengelompokan bulan bekerja, dan melintasi satu pekan penuh agar resample mingguan di pelajaran berikutnya bermakna. Indeksnya bertipe `DatetimeIndex`, jenis indeks yang membuka semua kemampuan waktu pandas."),
        C(
            P("""
print(idx[0].day_name(), idx[-1].strftime('%Y-%m-%d'), len(idx))
print(s['2024-01-30'])
print(s['2024-01-30':'2024-02-01'].tolist())
print(s['2024-02'].tolist())
print(s.loc['2024-01'].tolist())
print(s.index.dayofweek.tolist())
print(s.index.day_name().tolist()[:3])
print(s.index.month.tolist())
"""),
            ind("""
Monday 2024-02-05 8
12
[12, 9, 15]
[15, 14, 20, 18, 22]
[10, 12, 9]
[0, 1, 2, 3, 4, 5, 6, 0]
['Monday', 'Tuesday', 'Wednesday']
[1, 1, 1, 2, 2, 2, 2, 2]
"""),
            "Indeks tanggal memungkinkan pemotongan dengan teks tanggal sebagian seperti 2024-02, dan atribut seperti dayofweek dan month tersedia langsung pada indeks.",
            filename="indeks_waktu.py",
        ),
        tb("Pemotongan dengan label", "Dengan indeks tanggal, Anda memotong memakai teks tanggal. `s['2024-01-30']` mengambil satu hari, `s['2024-02']` mengambil seluruh bulan Februari, dan `s['2024-01-30':'2024-02-01']` mengambil rentang. Berbeda dari pemotongan posisi biasa, pemotongan label menyertakan kedua ujungnya. Tulis tanggal dalam format ISO tahun, bulan, hari agar tidak ambigu. Fitur teks tanggal sebagian ini sangat berguna: mengambil satu tahun atau satu bulan cukup dengan menulis `'2024'` atau `'2024-02'` tanpa menghitung batas akhirnya sendiri."),
        tb("Mengapa harus terurut", "Pemotongan rentang pada indeks tanggal mengandalkan keterurutan. Bila indeks tidak terurut, pandas dapat melempar galat atau memberi hasil yang membingungkan. Urutkan dengan `sort_index()` setelah memuat data, dan periksa dengan `s.index.is_monotonic_increasing`. Kebiasaan ini menghindari kejutan, terutama ketika data digabung dari beberapa file yang masing-masing terurut tetapi urutan antar file tidak terjamin. Sebuah alur analisis deret waktu yang baik hampir selalu memiliki langkah eksplisit memastikan indeks bertipe tanggal, terurut, dan tanpa duplikat."),
        tb("Atribut dari indeks", "Indeks tanggal menyediakan atribut `year`, `month`, `day`, `dayofweek`, `quarter`, `is_month_end`, serta `day_name()` dan `month_name()`, sama seperti `dt` pada kolom. Atribut ini adalah bahan baku pengelompokan: rata-rata per bulan dengan `groupby(s.index.month)`, jumlah per hari dalam pekan dengan `groupby(s.index.dayofweek)`. Perhatikan bahwa pengelompokan per bulan saja menggabungkan Januari semua tahun bila data mencakup banyak tahun, jadi untuk data multi-tahun kelompokkan menurut tahun dan bulan sekaligus atau pakai `to_period('M')`."),
        C(
            P("""
print(s.groupby(s.index.dayofweek).sum().to_dict())
print(s.groupby(s.index.month).mean().to_dict())
print(s.index.is_month_end.tolist()[:3])
print(s.index.to_period('M').astype(str).tolist()[:2])
print(s.idxmax().strftime('%Y-%m-%d'), s.nlargest(2).index.strftime('%d').tolist())
print(s.index.is_monotonic_increasing)
"""),
            ind("""
{0: 32, 1: 12, 2: 9, 3: 15, 4: 14, 5: 20, 6: 18}
{1: 10.333333333333334, 2: 17.8}
[False, False, True]
['2024-01', '2024-01']
2024-02-05 ['05', '03']
True
"""),
            "Atribut indeks menjadi kunci groupby. Idxmax mengembalikan tanggal dengan nilai tertinggi, dan hari Senin muncul dua kali sehingga jumlahnya 32.",
            filename="atribut_indeks.py",
        ),
        tb("Membuat rentang tanggal", "Fungsi `pd.date_range` membuat rangkaian tanggal teratur dari titik awal. Anda dapat menyebut awal dan akhir, atau awal dan jumlah periode `periods`. Argumen `freq` menentukan jarak: `'D'` harian, `'2D'` dua harian, `'W'` mingguan berakhir Minggu, `'B'` hari kerja Senin sampai Jumat. Alias frekuensi bulanan dan tahunan berubah antar versi pandas, sehingga bila Anda memerlukannya, periksa dokumentasi versi yang Anda pakai. Rentang yang dibuat sendiri berguna sebagai kerangka lengkap untuk menemukan tanggal yang hilang dari data."),
        C(
            P("""
print(pd.date_range('2024-01-01', periods=4, freq='W').strftime('%Y-%m-%d').tolist())
print(pd.date_range('2024-01-01', periods=5, freq='B').strftime('%a').tolist())
print(pd.date_range('2024-01-01', '2024-01-10', freq='3D').strftime('%d').tolist())
print(pd.Timestamp('2024-03-05').to_period('M'))
print((pd.Timestamp('2024-03-05') + pd.Timedelta(days=30)).strftime('%Y-%m-%d'))
print((pd.Timestamp('2024-01-31') + pd.DateOffset(months=1)).strftime('%Y-%m-%d'))
print(s.index.max() - s.index.min())
"""),
            ind("""
['2024-01-07', '2024-01-14', '2024-01-21', '2024-01-28']
['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
['01', '04', '07', '10']
2024-03
2024-04-04
2024-02-29
7 days 00:00:00
"""),
            "Date_range membuat kerangka tanggal. Timedelta menambah durasi tetap, sedangkan DateOffset menambah satuan kalender seperti bulan dengan penyesuaian akhir bulan.",
            filename="date_range.py",
        ),
        tb("Timedelta dan DateOffset", "Selisih dua tanggal bertipe `Timedelta`, durasi dengan atribut seperti `days` dan `total_seconds()`. Menambahkan `Timedelta(days=30)` menggeser tepat tiga puluh hari, sedangkan `DateOffset(months=1)` menggeser satu bulan kalender dan menyesuaikan bila bulan tujuan lebih pendek, sehingga 31 Januari ditambah satu bulan menjadi 29 Februari pada tahun kabisat. Pilih menurut maksud: durasi tetap untuk jarak waktu fisik, offset kalender untuk aturan bisnis seperti jatuh tempo tiap bulan atau akhir kuartal."),
        tb("Zona waktu", "Tanggal tanpa zona waktu disebut naif, dan tanggal dengan zona waktu disebut sadar zona. Pandas mendukung keduanya dengan `tz_localize` untuk menempelkan zona pada waktu naif dan `tz_convert` untuk memindahkan waktu sadar zona ke zona lain. Aturan emasnya: simpan dan hitung dalam UTC, ubah ke zona lokal hanya saat menampilkan. Mencampur waktu naif dan sadar zona menghasilkan galat, yang sebenarnya melindungi Anda dari kesalahan senyap berselisih tujuh jam antara Jakarta dan UTC."),
        K("tip", "Pastikan indeks bertipe tanggal, terurut, dan tanpa duplikat sebelum analisis. Tiga pemeriksaan ini menyelesaikan banyak galat deret waktu.", title="Tiga pemeriksaan"),
        tb("Contoh kerja: bulan dalam data", "Misalkan Anda diminta rata-rata penjualan tiap bulan dari data harian. Langkahnya: pastikan kolom tanggal bertipe tanggal, jadikan indeks dan urutkan, lalu kelompokkan menurut bulan. Pada contoh ini Januari hanya punya tiga hari dengan rata-rata 10,33 sedangkan Februari punya lima hari dengan rata-rata 17,8. Membandingkan keduanya langsung menyesatkan karena Januari parsial. Catat jumlah hari tiap bulan bersama rata-ratanya, dan pertimbangkan membandingkan hanya bulan dengan data penuh agar kesimpulan tidak dipengaruhi cakupan yang tidak sama."),
        tb("Pola kerja yang disarankan", "Urutan kerja yang andal untuk deret waktu: baca data, ubah kolom tanggal dengan format eksplisit, jadikan indeks, urutkan, buang atau tangani duplikat tanggal, periksa jarak antar tanggal, baru kemudian analisis. Setiap langkah mudah ditulis sebagai satu baris dan mudah diperiksa. Mengabaikan salah satunya menimbulkan kesalahan halus yang baru terlihat jauh di hilir, misalnya rata-rata bulanan yang menghitung satu hari dua kali karena ada duplikat tanggal pada data hasil gabungan dua sumber."),
        tb("Kesalahan umum dengan tanggal", "Tiga kesalahan paling sering: format ambigu yang terbaca terbalik antara hari dan bulan, tanggal yang dibiarkan bertipe teks sehingga terurut menurut huruf, dan indeks yang tidak terurut sehingga pemotongan memberi hasil aneh. Ketiganya dapat dicegah dengan satu baris pemeriksaan di awal alur. Periksa `dtypes`, cetak nilai minimum dan maksimum tanggal, dan bandingkan dengan rentang yang Anda harapkan dari sumber data."),
        E(
            "B2-09-1-ex1",
            "mudah",
            "Tulis fungsi `irisan_tanggal(s, awal, akhir)` yang mengembalikan list nilai deret `s` dari tanggal `awal` sampai `akhir` (teks ISO, kedua ujung disertakan).",
            ind("""
import pandas as pd

def irisan_tanggal(s, awal, akhir):
    # TODO: implementasikan
    pass
"""),
            P("""
assert irisan_tanggal(s, '2024-01-30', '2024-02-01') == [12, 9, 15]
assert irisan_tanggal(s, '2024-02-01', '2024-02-05') == [15, 14, 20, 18, 22]
assert irisan_tanggal(s, '2024-01-29', '2024-01-29') == [10]
assert irisan_tanggal(s, '2024-01', '2024-01') == [10, 12, 9]
"""),
            "Pemotongan label dengan titik dua pada indeks tanggal.",
            X(F11),
        ),
        E(
            "B2-09-1-ex2",
            "sedang",
            "Tulis fungsi `rata_per_bulan(s)` yang mengembalikan dict rata-rata nilai per nomor bulan, dibulatkan dua desimal.",
            ind("""
import pandas as pd

def rata_per_bulan(s):
    # TODO: implementasikan
    pass
"""),
            P("""
assert rata_per_bulan(s) == {1: 10.33, 2: 17.8}
assert rata_per_bulan(s['2024-02']) == {2: 17.8}
assert rata_per_bulan(s['2024-01']) == {1: 10.33}
assert len(rata_per_bulan(s)) == 2
"""),
            "groupby pada s.index.month lalu mean dan round.",
            X(F12),
        ),
        E(
            "B2-09-1-ex3",
            "sedang",
            "Tulis fungsi `jumlah_per_hari_pekan(s)` yang mengembalikan dict jumlah nilai per hari dalam pekan, dengan Senin bernomor 0.",
            ind("""
import pandas as pd

def jumlah_per_hari_pekan(s):
    # TODO: implementasikan
    pass
"""),
            P("""
assert jumlah_per_hari_pekan(s) == {0: 32, 1: 12, 2: 9, 3: 15, 4: 14, 5: 20, 6: 18}
assert jumlah_per_hari_pekan(s.iloc[:2]) == {0: 10, 1: 12}
assert jumlah_per_hari_pekan(s)[0] == 32
assert sum(jumlah_per_hari_pekan(s).values()) == 120
"""),
            "groupby pada s.index.dayofweek lalu sum.",
            X(F13),
        ),
        E(
            "B2-09-1-ex4",
            "menantang",
            "Tulis fungsi `daftar_tanggal(awal, n, freq)` yang mengembalikan list `n` tanggal berformat `YYYY-MM-DD` mulai dari `awal` dengan frekuensi `freq`.",
            ind("""
import pandas as pd

def daftar_tanggal(awal, n, freq):
    # TODO: implementasikan
    pass
"""),
            P("""
assert daftar_tanggal('2024-01-01', 3, 'D') == ['2024-01-01', '2024-01-02', '2024-01-03']
assert daftar_tanggal('2024-01-01', 3, '2D') == ['2024-01-01', '2024-01-03', '2024-01-05']
assert daftar_tanggal('2024-01-01', 5, 'B')[-1] == '2024-01-05'
assert daftar_tanggal('2024-01-01', 2, 'W') == ['2024-01-07', '2024-01-14']
"""),
            "date_range dengan periods dan freq lalu strftime.",
            X(F14),
        ),
    ],
    [
        M("Membiarkan tanggal bertipe teks.", "Ubah dengan to_datetime dan jadikan indeks."),
        M("Memotong pada indeks yang belum terurut.", "Panggil sort_index lebih dulu."),
        M("Mencampur waktu naif dan sadar zona.", "Simpan dalam UTC dan konversi saat tampil."),
    ],
    [
        Q("Pemotongan label tanggal menyertakan?", ["Kedua ujung", "Hanya awal", "Hanya akhir", "Tak satu pun"], 0, "Label inklusif.", hint="Kedua."),
        Q("freq 'B' berarti?", ["Hari kerja", "Bulanan", "Mingguan", "Per jam"], 0, "Business day.", hint="Kerja."),
        Q("Timedelta menambah?", ["Durasi tetap", "Bulan kalender", "Zona", "Format"], 0, "Durasi.", hint="Tetap."),
        Q("DateOffset months=1 pada 31 Jan 2024?", ["29 Feb 2024", "31 Feb", "1 Mar", "30 Jan"], 0, "Sesuaikan akhir bulan.", hint="Akhir bulan."),
        Q("Zona waktu simpan dalam?", ["UTC", "Lokal", "Acak", "Tanpa zona"], 0, "Aturan emas.", hint="UTC."),
    ],
    [
        "to_datetime dan DatetimeIndex membuka kemampuan waktu pandas.",
        "Pemotongan label memakai teks tanggal dan inklusif.",
        "date_range membuat kerangka tanggal teratur.",
        "Pilih Timedelta atau DateOffset menurut maksud.",
    ],
    [],
)

G11 = """
import pandas as pd

def jumlah_mingguan(s):
    return s.resample('W').sum().tolist()
"""
G12 = """
import pandas as pd

def rata_dua_hari(s):
    return s.resample('2D').mean().tolist()
"""
G13 = """
import pandas as pd

def rata_bergulir(s, k):
    return s.rolling(k).mean().round(2).fillna(0).tolist()
"""
G14 = """
import pandas as pd

def maks_berjalan(s):
    return s.expanding().max().tolist()
"""

l2 = lesson(
    "B2-09-2",
    "Resample, rolling, dan expanding",
    35,
    [
        "Mengubah frekuensi deret dengan resample",
        "Menghitung rata-rata bergulir dengan rolling",
        "Memakai expanding dan ewm untuk statistik kumulatif",
        "Menjelaskan nilai hilang di awal jendela",
    ],
    [
        tb("Mengubah resolusi waktu", "Data sering datang pada resolusi yang tidak sesuai pertanyaan. Sensor merekam tiap detik padahal Anda ingin rata-rata per jam, transaksi dicatat per menit padahal laporan bulanan. Metode `resample` mengelompokkan deret berindeks tanggal ke dalam jendela waktu teratur lalu menerapkan agregasi pada tiap jendela. Ia seperti groupby tetapi kuncinya adalah potongan waktu yang dibuat otomatis dari indeks, dan jendela kosong tetap muncul dalam hasil sehingga tidak ada celah tersembunyi dalam deret yang dihasilkan."),
        tb("Aturan jendela", "Resample mingguan dengan `'W'` menggunakan pekan yang berakhir pada hari Minggu, dan label hasilnya adalah tanggal akhir pekan itu. Pada data contoh, pekan pertama berakhir Minggu 4 Februari dan berisi enam hari pertama, jumlahnya 98, sedangkan Senin 5 Februari jatuh ke pekan kedua yang berjumlah 22. Memahami kapan jendela dimulai dan berakhir sangat penting, sebab angka yang tampak aneh biasanya hanya akibat batas jendela yang tidak sesuai dugaan. Argumen `label` dan `closed` mengatur sisi mana yang menjadi batas dan label."),
        C(
            P("""
print(s.resample('W').sum().tolist())
print(s.resample('W').sum().index.strftime('%m-%d').tolist())
print(s.resample('2D').mean().tolist())
print(s.resample('W').agg(['min', 'max']).values.tolist())
print(s.resample('W').last().tolist(), s.resample('W').count().tolist())
print(s.resample('W').sum().pct_change().round(3).tolist())
"""),
            ind("""
[98, 22]
['02-04', '02-11']
[11.0, 12.0, 17.0, 20.0]
[[9, 20], [22, 22]]
[18, 22] [7, 1]
[nan, -0.776]
"""),
            "Resample mengelompokkan menurut jendela waktu, lalu agregasi biasa diterapkan. Pekan pertama berisi tujuh hari dari Senin 29 Januari sampai Minggu 4 Februari.",
            filename="resample.py",
        ),
        tb("Pekan parsial", "Pekan terakhir pada contoh hanya berisi satu hari, Senin 5 Februari, tetapi muncul sebagai satu baris jumlah 22 di samping pekan penuh berjumlah 98. Membandingkan keduanya, atau menghitung pertumbuhan, menyesatkan karena ukuran jendelanya berbeda. Pertumbuhan minus 77,6 persen pada hasil di atas bukan penurunan nyata. Bersikaplah curiga pada jendela pertama dan terakhir, yang sering parsial, dan buang atau tandai dengan `count` bila membandingkan antar periode."),
        tb("Rolling untuk menghaluskan", "Metode `rolling(k)` membentuk jendela bergeser sepanjang k observasi, dan agregasi seperti `mean`, `sum`, `max`, atau `std` dihitung pada tiap posisi. Rata-rata bergulir menghaluskan fluktuasi harian sehingga tren terlihat. Berbeda dari resample yang mengurangi jumlah baris, rolling mempertahankan jumlah baris dan menghasilkan satu nilai per posisi. Jendela bertumpang tindih, sehingga nilai berdekatan saling berkorelasi, sebuah sifat yang perlu diingat ketika menafsirkan hasilnya sebagai observasi independen."),
        C(
            P("""
print(s.rolling(3).mean().round(2).tolist())
print(s.rolling(3, min_periods=1).sum().tolist())
print(s.rolling(3).max().tolist())
print(s.rolling('3D').sum().tolist())
print(s.expanding().max().tolist(), s.cumsum().tolist())
print(s.ewm(span=3, adjust=False).mean().round(2).tolist())
"""),
            ind("""
[nan, nan, 10.33, 12.0, 12.67, 16.33, 17.33, 20.0]
[10.0, 22.0, 31.0, 36.0, 38.0, 49.0, 52.0, 60.0]
[nan, nan, 12.0, 15.0, 15.0, 20.0, 20.0, 22.0]
[10.0, 22.0, 31.0, 36.0, 38.0, 49.0, 52.0, 60.0]
[10.0, 12.0, 12.0, 15.0, 15.0, 20.0, 20.0, 22.0] [10, 22, 31, 46, 60, 80, 98, 120]
[10.0, 11.0, 10.0, 12.5, 13.25, 16.62, 17.31, 19.66]
"""),
            "Rolling menghasilkan NaN sampai jendela penuh kecuali min_periods diatur. Jendela berbasis waktu seperti 3D menghitung menurut jarak tanggal, bukan jumlah baris.",
            filename="rolling.py",
        ),
        tb("NaN di awal jendela", "Rata-rata bergulir tiga hari baru dapat dihitung pada hari ketiga, sehingga dua nilai pertama NaN. Ini perilaku yang benar karena belum ada tiga observasi. Argumen `min_periods` menurunkan syarat itu, misalnya `min_periods=1` menghitung dengan data yang ada. Pilih dengan sadar: jendela yang belum penuh memberi angka yang lebih berisik dan tidak sebanding dengan jendela penuh. Pada pemodelan, NaN awal ini biasanya dibuang atau diisi dengan metode yang Anda dokumentasikan."),
        tb("Jendela berbasis waktu", "Argumen jendela dapat berupa teks durasi seperti `'3D'` untuk tiga hari, bukan jumlah baris. Bedanya terasa pada data yang tidak teratur: tiga baris bisa mencakup satu hari atau satu bulan, sedangkan `'3D'` selalu tiga hari kalender. Jendela berbasis waktu mensyaratkan indeks tanggal terurut. Pada data harian teratur keduanya identik, seperti pada contoh, tetapi pada data transaksi dengan jarak waktu acak, jendela berbasis waktu jauh lebih bermakna secara analisis."),
        tb("Expanding dan ewm", "Metode `expanding()` memakai semua observasi dari awal sampai posisi saat ini, sehingga `expanding().max()` adalah rekor tertinggi sampai hari itu dan `expanding().mean()` adalah rata-rata berjalan. Metode `ewm` menghitung rata-rata dengan bobot yang meluruh eksponensial, memberi bobot lebih pada observasi baru. Parameter `span` mengatur kecepatan peluruhan. Rata-rata eksponensial bereaksi lebih cepat terhadap perubahan daripada rata-rata bergulir biasa, sehingga populer pada pemantauan dan peramalan sederhana."),
        tb("Memilih lebar jendela", "Jendela pendek mengikuti data dengan setia tetapi masih berisik, jendela panjang halus tetapi terlambat bereaksi. Tidak ada angka ajaib, jadi pilih menurut siklus data: tujuh hari menghilangkan efek hari dalam pekan, dua belas bulan menghilangkan musiman tahunan. Gambarlah deret asli bersama beberapa lebar jendela dan pilih yang menghilangkan derau tanpa menyembunyikan perubahan yang ingin Anda deteksi. Keputusan ini adalah penilaian analis, bukan perhitungan."),
        K("warn", "Jendela pertama dan terakhir pada resample sering parsial. Jangan membandingkan pertumbuhannya dengan jendela penuh tanpa memeriksa count.", title="Pekan parsial"),
        C(
            P("""
print(s.resample('3D').sum().tolist())
print(s.resample('3D').agg(['sum', 'max']).values.tolist())
print(s.resample('W').mean().round(2).tolist())
print(s.resample('2D').sum().tolist())
print(s.resample('2D').max().tolist())
print(s.rolling(2).sum().tolist())
"""),
            ind("""
[31, 49, 40]
[[31, 12], [49, 20], [40, 22]]
[14.0, 22.0]
[22, 24, 34, 40]
[12, 15, 20, 22]
[nan, 22.0, 21.0, 24.0, 29.0, 34.0, 38.0, 40.0]
"""),
            "Satu deret dapat diringkas pada beberapa resolusi. Resample mengurangi baris menjadi satu per jendela, sedangkan rolling mempertahankan jumlah baris.",
            filename="resolusi_ganda.py",
        ),
        tb("Memilih agregasi saat resample", "Agregasi yang dipilih harus sesuai arti data. Jumlah cocok untuk besaran yang menumpuk seperti penjualan atau kunjungan, rata-rata cocok untuk besaran tingkat seperti suhu atau harga, nilai terakhir cocok untuk status seperti stok akhir periode, dan maksimum cocok untuk puncak seperti beban tertinggi. Memakai jumlah pada harga atau rata-rata pada penjualan harian menghasilkan angka yang tidak punya arti. Satu panggilan `agg` dengan beberapa fungsi memberi gambaran lengkap sebelum Anda memutuskan ringkasan mana yang dipublikasikan dalam laporan."),
        tb("Resample dan nilai hilang", "Jendela tanpa data muncul dalam hasil resample sebagai nol untuk `sum` dan NaN untuk `mean`, perbedaan yang halus. Nol dari jumlah kosong dapat menyesatkan: tidak ada transaksi pekan itu atau data pekan itu hilang. Gunakan `count` bersama agregasi untuk membedakannya, atau `min_count=1` pada sum agar jendela kosong menghasilkan NaN. Perlakukan jendela kosong sebagai informasi yang perlu dijelaskan, bukan sebagai nol yang aman, terutama ketika hasilnya dipakai menghitung pertumbuhan antar pekan."),
        tb("Hubungan resample dan groupby", "Resample mirip groupby dengan kunci waktu, dan keduanya dapat dipertukarkan pada banyak kasus. Perbedaannya, resample otomatis menyertakan jendela kosong dan menjaga urutan waktu, sedangkan groupby dengan `Grouper` atau atribut tanggal hanya menampilkan kelompok yang ada. Pakai resample untuk deret bersambung dan groupby bila Anda mengelompokkan menurut sifat kalender seperti hari dalam pekan yang tidak membentuk jendela berurutan. Memilih alat yang tepat membuat kode lebih ringkas dan hasil lebih mudah ditafsirkan."),
        tb("Rolling pada data banyak kelompok", "Bila data berisi banyak entitas, misalnya banyak toko dalam satu tabel panjang, rolling harus dijalankan per entitas, bukan pada seluruh kolom. Pola yang benar adalah `groupby('toko')['omzet'].rolling(3).mean()` atau `transform` dengan lambda. Menjalankan rolling langsung pada tabel campuran menghitung rata-rata lintas toko di perbatasan data, kesalahan halus yang menghasilkan angka masuk akal tetapi keliru. Kebiasaan ini juga berlaku untuk shift, diff, dan cumsum pada tabel panjang."),
        tb("Contoh kerja: laporan mingguan", "Untuk laporan mingguan, resample deret harian dengan jumlah, hitung juga count agar jendela parsial terlihat, lalu bandingkan pekan penuh saja. Tambahkan rata-rata bergulir empat pekan untuk menunjukkan tren tanpa gejolak pekanan. Tiga kolom ini, jumlah, count, dan rata-rata bergulir, sudah memberi gambaran jujur yang mudah dipahami pembaca non-teknis dan tidak menyembunyikan keterbatasan data."),
        E(
            "B2-09-2-ex1",
            "mudah",
            "Tulis fungsi `jumlah_mingguan(s)` yang mengembalikan list jumlah nilai per pekan (berakhir Minggu) memakai `resample`.",
            ind("""
import pandas as pd

def jumlah_mingguan(s):
    # TODO: implementasikan
    pass
"""),
            P("""
assert jumlah_mingguan(s) == [98, 22]
assert jumlah_mingguan(s.iloc[:3]) == [31]
assert jumlah_mingguan(s.iloc[6:]) == [18, 22]
assert sum(jumlah_mingguan(s)) == 120
"""),
            "resample dengan W lalu sum.",
            X(G11),
        ),
        E(
            "B2-09-2-ex2",
            "sedang",
            "Tulis fungsi `rata_dua_hari(s)` yang mengembalikan list rata-rata per jendela dua hari memakai `resample`.",
            ind("""
import pandas as pd

def rata_dua_hari(s):
    # TODO: implementasikan
    pass
"""),
            P("""
assert rata_dua_hari(s) == [11.0, 12.0, 17.0, 20.0]
assert rata_dua_hari(s.iloc[:2]) == [11.0]
assert rata_dua_hari(s.iloc[:3]) == [11.0, 9.0]
assert len(rata_dua_hari(s)) == 4
"""),
            "resample dengan 2D lalu mean.",
            X(G12),
        ),
        E(
            "B2-09-2-ex3",
            "sedang",
            "Tulis fungsi `rata_bergulir(s, k)` yang mengembalikan list rata-rata bergulir jendela `k`, dibulatkan dua desimal, dengan nilai yang belum bisa dihitung diisi nol.",
            ind("""
import pandas as pd

def rata_bergulir(s, k):
    # TODO: implementasikan
    pass
"""),
            P("""
assert rata_bergulir(s, 3) == [0.0, 0.0, 10.33, 12.0, 12.67, 16.33, 17.33, 20.0]
assert rata_bergulir(s, 2) == [0.0, 11.0, 10.5, 12.0, 14.5, 17.0, 19.0, 20.0]
assert rata_bergulir(s, 1) == [10.0, 12.0, 9.0, 15.0, 14.0, 20.0, 18.0, 22.0]
assert rata_bergulir(s, 8)[-1] == 15.0
"""),
            "rolling lalu mean, round, dan fillna nol.",
            X(G13),
        ),
        E(
            "B2-09-2-ex4",
            "menantang",
            "Tulis fungsi `maks_berjalan(s)` yang mengembalikan list nilai tertinggi yang pernah dicapai sampai tiap hari.",
            ind("""
import pandas as pd

def maks_berjalan(s):
    # TODO: implementasikan
    pass
"""),
            P("""
assert maks_berjalan(s) == [10, 12, 12, 15, 15, 20, 20, 22]
assert maks_berjalan(s.iloc[:3]) == [10, 12, 12]
assert maks_berjalan(s.iloc[[2, 0]]) == [9, 10]
assert maks_berjalan(s)[-1] == 22
"""),
            "expanding lalu max.",
            X(G14),
        ),
    ],
    [
        M("Membandingkan jendela parsial dengan jendela penuh.", "Periksa count tiap jendela."),
        M("Mengira rolling mengurangi jumlah baris.", "Rolling mempertahankan jumlah baris, resample menguranginya."),
        M("Memakai jendela berbasis baris pada data tak teratur.", "Pakai jendela berbasis waktu seperti 3D."),
    ],
    [
        Q("resample menghasilkan?", ["Satu baris per jendela waktu", "Satu per baris asal", "Dict", "Kolom"], 0, "Per jendela.", hint="Jendela."),
        Q("rolling(3) dua nilai pertama?", ["NaN", "0", "Rata-rata", "Galat"], 0, "Jendela belum penuh.", hint="NaN."),
        Q("min_periods=1?", ["Hitung dengan data yang ada", "Hapus awal", "Isi nol", "Galat"], 0, "Turunkan syarat.", hint="Satu."),
        Q("expanding max adalah?", ["Rekor sejauh ini", "Maks jendela tetap", "Rata-rata", "Median"], 0, "Kumulatif.", hint="Rekor."),
        Q("ewm memberi bobot lebih pada?", ["Data terbaru", "Data lama", "Rata", "Acak"], 0, "Eksponensial.", hint="Baru."),
    ],
    [
        "resample mengubah resolusi waktu dengan agregasi per jendela.",
        "rolling menghaluskan tanpa mengurangi jumlah baris.",
        "expanding dan ewm menghitung statistik kumulatif dan berbobot.",
        "Waspadai jendela parsial dan NaN di awal.",
    ],
    [],
)

H11 = """
import pandas as pd

def selisih_harian(s):
    return s.diff().fillna(0).tolist()
"""
H12 = """
import pandas as pd

def pertumbuhan_harian(s):
    return s.pct_change().round(3).fillna(0).tolist()
"""
H13 = """
import pandas as pd

def isi_celah(s):
    return s.asfreq('D').interpolate().round(2).tolist()
"""
H14 = """
import pandas as pd

def di_atas_rata(s, k):
    return (s > s.rolling(k).mean()).tolist()
"""

l3 = lesson(
    "B2-09-3",
    "Shift, selisih, dan celah dalam deret",
    35,
    [
        "Menggeser deret dengan shift untuk membuat nilai sebelumnya",
        "Menghitung selisih dan pertumbuhan dengan diff dan pct_change",
        "Menemukan dan mengisi tanggal yang hilang dengan asfreq dan reindex",
        "Menghindari kebocoran informasi dari masa depan",
    ],
    [
        tb("Melihat ke belakang", "Hampir semua analisis deret waktu membandingkan nilai sekarang dengan nilai sebelumnya. Metode `shift(1)` menggeser deret satu posisi ke bawah sehingga tiap baris memuat nilai hari kemarin, dan `shift(-1)` menggeser ke atas sehingga memuat nilai besok. Posisi yang kosong akibat pergeseran diisi NaN. Dari dasar ini lahir fitur lag untuk pemodelan, selisih, pertumbuhan, dan pemeriksaan apakah nilai hari ini lebih tinggi daripada kemarin. Satu operasi sederhana membuka banyak jenis analisis."),
        tb("diff dan pct_change", "Metode `diff()` menghitung selisih dengan baris sebelumnya, setara `s - s.shift(1)`, dan `pct_change()` menghitung perubahan relatif, setara `s / s.shift(1) - 1`. Keduanya menghasilkan NaN pada baris pertama. Selisih menjawab berapa naik, pertumbuhan menjawab berapa persen naik. Pada deret contoh, hari kedua naik dua poin atau dua puluh persen, hari ketiga turun tiga poin atau dua puluh lima persen. Pilih sesuai skala: pertumbuhan baik untuk membandingkan deret berskala berbeda, selisih baik untuk besaran yang bisa nol."),
        C(
            P("""
print(s.shift(1).tolist())
print(s.shift(-1).tolist())
print(s.diff().tolist())
print(s.pct_change().round(3).tolist())
print((s - s.shift(1)).dropna().tolist())
print(s.index.to_series().diff().dt.days.tolist())
"""),
            ind("""
[nan, 10.0, 12.0, 9.0, 15.0, 14.0, 20.0, 18.0]
[12.0, 9.0, 15.0, 14.0, 20.0, 18.0, 22.0, nan]
[nan, 2.0, -3.0, 6.0, -1.0, 6.0, -2.0, 4.0]
[nan, 0.2, -0.25, 0.667, -0.067, 0.429, -0.1, 0.222]
[2.0, -3.0, 6.0, -1.0, 6.0, -2.0, 4.0]
[nan, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
"""),
            "Shift menggeser, diff menghitung selisih, dan pct_change menghitung pertumbuhan relatif. Selisih tanggal pada indeks memeriksa keteraturan jarak.",
            filename="shift_diff_ts.py",
        ),
        tb("Memeriksa keteraturan", "Sebelum memakai shift atau rolling berbasis baris, pastikan jarak antar tanggal teratur. Selisih indeks `s.index.to_series().diff()` menunjukkan celah: bila semuanya satu hari, deret teratur. Celah berarti shift satu posisi tidak lagi berarti satu hari, dan rata-rata bergulir berbasis baris mencampur rentang waktu berbeda. Banyak kesalahan analisis deret waktu berasal dari asumsi teratur yang tidak pernah diperiksa, jadi jadikan pemeriksaan jarak langkah rutin pertama."),
        tb("Celah dengan asfreq", "Metode `asfreq('D')` memaksa deret ke frekuensi harian teratur, menyisipkan baris NaN untuk tanggal yang hilang. Argumen `method='ffill'` mengisinya dengan nilai sebelumnya. Metode `reindex` dengan `date_range` lengkap melakukan hal serupa dengan kontrol penuh atas rentang. Setelah celah muncul sebagai NaN, Anda dapat mengisinya dengan `interpolate` untuk besaran mulus atau ffill untuk status yang bertahan, seperti harga atau stok. Memilih pengisi adalah keputusan analisis yang harus dicatat."),
        C(
            P("""
g = s.drop(idx[[2, 3]])
print(len(g), g.asfreq('D').isna().sum())
print(g.asfreq('D').interpolate().round(2).tolist())
print(g.asfreq('D', method='ffill').tolist())
print(g.reindex(idx).tolist())
print(s.asfreq('2D').tolist())
print(s.truncate(before='2024-02-01').tolist())
"""),
            ind("""
6 2
[10.0, 12.0, 12.67, 13.33, 14.0, 20.0, 18.0, 22.0]
[10, 12, 12, 12, 14, 20, 18, 22]
[10.0, 12.0, nan, nan, 14.0, 20.0, 18.0, 22.0]
[10, 9, 14, 18]
[15, 14, 20, 18, 22]
"""),
            "Asfreq dan reindex membuat tanggal hilang tampak sebagai NaN. Interpolate dan ffill mengisinya dengan asumsi berbeda.",
            filename="celah_deret.py",
        ),
        tb("Bandingkan dengan rata-rata bergulir", "Pola analisis umum adalah membandingkan nilai dengan rata-rata bergulirnya. Nilai di atas rata-rata bergulir menunjukkan lonjakan relatif terhadap kondisi terbaru, dasar sederhana untuk deteksi anomali dan sinyal tren. Pada contoh, mulai hari keempat nilai selalu di atas rata-rata tiga hari terakhir, tanda tren naik. Hasilnya Series boolean yang dapat dipakai menyaring baris atau dihitung proporsinya. Dua nilai pertama False karena rata-rata belum dapat dihitung, dan perbandingan dengan NaN selalu salah."),
        tb("Kebocoran dari masa depan", "Kesalahan paling berbahaya pada deret waktu adalah membocorkan informasi masa depan ke dalam fitur. `shift(-1)` memberi nilai besok, yang sah sebagai target tetapi fatal sebagai fitur. Rolling yang terpusat, expanding dari seluruh data, atau standarisasi dengan rata-rata keseluruhan semuanya memakai data yang belum tersedia pada waktu prediksi. Model yang dilatih dengan kebocoran tampak sangat akurat dalam evaluasi lalu gagal di produksi. Untuk setiap fitur tanyakan: apakah nilainya sudah diketahui pada saat prediksi dibuat."),
        tb("Pemisahan latih dan uji berurutan", "Karena urutan bermakna, jangan mengacak data deret waktu saat memisahkan latih dan uji. Potong menurut waktu: data lama untuk melatih dan data baru untuk menguji, sehingga evaluasi meniru situasi nyata memprediksi masa depan dari masa lalu. Pemotongan label tanggal membuatnya ringkas, misalnya `s[:'2024-01-31']` untuk latih dan `s['2024-02':]` untuk uji. Pengacakan acak membocorkan pola waktu dari uji ke latih dan membuat skor terlalu optimistis."),
        tb("Ringkasan modul", "Anda telah belajar mengubah teks menjadi tanggal, memotong deret dengan label, membuat rentang tanggal, mengubah resolusi dengan resample, menghaluskan dengan rolling dan expanding, serta memakai shift, diff, dan asfreq untuk analisis perubahan dan celah. Pesan utama: periksa keteraturan, waspadai jendela parsial, dan hindari kebocoran masa depan. Modul terakhir pandas membahas idiom dan performa."),
        K("warn", "Setiap fitur deret waktu harus sudah diketahui pada saat prediksi. Shift negatif dan statistik dari seluruh data adalah sumber kebocoran umum.", title="Kebocoran masa depan"),
        C(
            P("""
lag = pd.DataFrame({'v': s, 'lag1': s.shift(1), 'lag2': s.shift(2)}).dropna()
print(lag.values.tolist())
print(lag.shape)
print(s[:'2024-02-01'].tolist())
print(s['2024-02-02':].tolist())
print(s.index[s > s.mean()].strftime('%d').tolist())
"""),
            ind("""
[[9.0, 12.0, 10.0], [15.0, 9.0, 12.0], [14.0, 15.0, 9.0], [20.0, 14.0, 15.0], [18.0, 20.0, 14.0], [22.0, 18.0, 20.0]]
(6, 3)
[10, 12, 9, 15]
[14, 20, 18, 22]
['03', '04', '05']
"""),
            "Fitur lag dibuat dengan shift, dan pemisahan latih dan uji dilakukan menurut tanggal, bukan acak.",
            filename="fitur_lag.py",
        ),
        tb("Fitur lag untuk pemodelan", "Untuk meramalkan nilai besok dari beberapa hari terakhir, bangun tabel fitur dengan beberapa kolom `shift`: nilai kemarin, dua hari lalu, dan seterusnya. Baris pertama akan memiliki NaN dan dibuang. Tabel ini dapat langsung dipakai model regresi biasa. Pada contoh, enam baris tersisa dengan tiga kolom. Semakin banyak lag, semakin banyak baris awal terbuang, sehingga jumlah lag adalah kompromi antara informasi dan ukuran data latih. Pada data kecil, pilih sedikit lag yang paling bermakna."),
        tb("Musiman dan hari dalam pekan", "Banyak deret memiliki pola berulang: penjualan lebih tinggi akhir pekan, lalu lintas lebih padat jam sibuk. Fitur kalender seperti hari dalam pekan, bulan, dan penanda hari libur sering lebih berguna daripada lag mentah. Ambil dari indeks tanggal dengan `index.dayofweek` dan `index.month`, lalu ubah menjadi dummy atau ambil rata-rata per hari dalam pekan sebagai fitur tambahan. Menggabungkan lag dan fitur kalender memberi model dasar yang kuat untuk banyak masalah peramalan harian."),
        tb("Nilai hilang pada deret waktu", "Menangani nilai hilang pada deret waktu berbeda dari tabel biasa karena urutan dan kedekatan bermakna. Interpolasi linear cocok untuk besaran yang berubah mulus seperti suhu, ffill cocok untuk status yang bertahan seperti harga, dan pengisian dengan rata-rata keseluruhan jarang tepat karena mengabaikan tren. Untuk celah panjang, pertimbangkan membiarkan NaN atau menandainya, sebab mengarang puluhan nilai berurutan menghasilkan deret yang tampak mulus tetapi tidak berdasarkan data."),
        tb("Mendeteksi lonjakan", "Setelah punya selisih dan rata-rata bergulir, lonjakan dapat dideteksi sederhana: tandai hari ketika perubahan melebihi beberapa kali simpangan baku bergulir. Metode ini bukan model canggih tetapi sering cukup untuk pemantauan awal dan menjadi pembanding yang baik bagi metode yang lebih rumit. Course deteksi anomali kelak membahas pendekatan yang lebih kuat. Yang penting sekarang: Anda sudah memiliki bahan dasarnya, yaitu shift, diff, dan rolling yang diterapkan dengan benar."),
        tb("Contoh kerja: menilai tren", "Untuk menilai tren, hitung rata-rata bergulir tujuh hari, bandingkan nilai terakhir dengan rata-rata itu, dan lihat selisih terhadap tujuh hari sebelumnya dengan `diff(7)`. Dua angka sederhana ini menjawab apakah kondisi sedang membaik atau memburuk tanpa model rumit. Catat selalu panjang data yang dipakai dan apakah ada celah, agar pembaca tahu seberapa kokoh kesimpulan tersebut."),
        E(
            "B2-09-3-ex1",
            "mudah",
            "Tulis fungsi `selisih_harian(s)` yang mengembalikan list selisih tiap hari terhadap hari sebelumnya, dengan hari pertama diisi nol.",
            ind("""
import pandas as pd

def selisih_harian(s):
    # TODO: implementasikan
    pass
"""),
            P("""
assert selisih_harian(s) == [0.0, 2.0, -3.0, 6.0, -1.0, 6.0, -2.0, 4.0]
assert selisih_harian(s.iloc[:2]) == [0.0, 2.0]
assert selisih_harian(s.iloc[:1]) == [0.0]
assert sum(selisih_harian(s)) == 12.0
"""),
            "diff lalu fillna nol.",
            X(H11),
        ),
        E(
            "B2-09-3-ex2",
            "sedang",
            "Tulis fungsi `pertumbuhan_harian(s)` yang mengembalikan list pertumbuhan relatif tiap hari terhadap hari sebelumnya, dibulatkan tiga desimal, dengan hari pertama diisi nol.",
            ind("""
import pandas as pd

def pertumbuhan_harian(s):
    # TODO: implementasikan
    pass
"""),
            P("""
assert pertumbuhan_harian(s) == [0.0, 0.2, -0.25, 0.667, -0.067, 0.429, -0.1, 0.222]
assert pertumbuhan_harian(s.iloc[:2]) == [0.0, 0.2]
assert pertumbuhan_harian(s.iloc[1:3]) == [0.0, -0.25]
assert pertumbuhan_harian(s)[0] == 0.0
"""),
            "pct_change, round, lalu fillna nol.",
            X(H12),
        ),
        E(
            "B2-09-3-ex3",
            "sedang",
            "Tulis fungsi `isi_celah(s)` yang memaksa deret ke frekuensi harian, mengisi tanggal yang hilang dengan interpolasi linear, membulatkan dua desimal, dan mengembalikan list.",
            ind("""
import pandas as pd

def isi_celah(s):
    # TODO: implementasikan
    pass
"""),
            P("""
g = s.drop(idx[[2, 3]])
assert isi_celah(g) == [10.0, 12.0, 12.67, 13.33, 14.0, 20.0, 18.0, 22.0]
assert isi_celah(s) == [10.0, 12.0, 9.0, 15.0, 14.0, 20.0, 18.0, 22.0]
assert isi_celah(s.drop(idx[[1]]))[1] == 9.5
assert len(isi_celah(g)) == 8
"""),
            "asfreq D lalu interpolate dan round.",
            X(H13),
        ),
        E(
            "B2-09-3-ex4",
            "menantang",
            "Tulis fungsi `di_atas_rata(s, k)` yang mengembalikan list boolean apakah nilai tiap hari lebih besar daripada rata-rata bergulir `k` hari yang berakhir pada hari itu.",
            ind("""
import pandas as pd

def di_atas_rata(s, k):
    # TODO: implementasikan
    pass
"""),
            P("""
assert di_atas_rata(s, 3) == [False, False, False, True, True, True, True, True]
assert di_atas_rata(s, 1) == [False] * 8
assert di_atas_rata(s, 8) == [False] * 7 + [True]
assert sum(di_atas_rata(s, 3)) == 5
"""),
            "Bandingkan s dengan rolling mean.",
            X(H14),
        ),
    ],
    [
        M("Mengabaikan celah tanggal.", "Periksa selisih indeks dan pakai asfreq."),
        M("Memakai shift negatif sebagai fitur.", "Shift negatif hanya untuk target."),
        M("Mengacak data deret waktu saat membagi.", "Potong menurut waktu."),
    ],
    [
        Q("shift(1) memberi tiap baris nilai?", ["Sebelumnya", "Berikutnya", "Rata-rata", "Maksimum"], 0, "Lag.", hint="Sebelum."),
        Q("pct_change baris pertama?", ["NaN", "0", "1", "Galat"], 0, "Tak ada pembanding.", hint="NaN."),
        Q("asfreq D menyisipkan?", ["NaN untuk tanggal hilang", "Nol", "Duplikat", "Rata-rata"], 0, "Baris kosong.", hint="NaN."),
        Q("Kebocoran berarti fitur memakai?", ["Info masa depan", "Info masa lalu", "Acak", "Median"], 0, "Belum diketahui.", hint="Masa depan."),
        Q("Pemisahan latih dan uji deret waktu?", ["Menurut waktu", "Acak", "Per kolom", "Per baris ganjil"], 0, "Berurutan.", hint="Waktu."),
    ],
    [
        "shift, diff, dan pct_change menghitung perubahan antar waktu.",
        "asfreq dan reindex membuat celah tanggal terlihat.",
        "Isi celah dengan interpolate atau ffill sesuai sifat besaran.",
        "Jaga fitur bebas kebocoran dan pisahkan data menurut waktu.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perintah yang cukup jelas dalam teks.", "brief": []}

write_module(
    "B2",
    9,
    "Time series di pandas",
    105,
    [
        "Memakai indeks tanggal, pemotongan label, dan date_range",
        "Mengubah resolusi dengan resample dan menghaluskan dengan rolling",
        "Menghitung perubahan dengan shift dan diff serta menangani celah",
    ],
    [l1, l2, l3],
    video,
    REF,
)
