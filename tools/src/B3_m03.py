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
    'id': [1, 2, 3, 4, 5, 6, 7],
    'nama': ['Ani Putri', 'ani putri ', 'Budi', 'Cici', 'Budi', 'Dedi', 'cici'],
    'kota': ['Jakarta', 'jakarta', 'Bandung', 'BANDUNG', 'Bandung', 'Jkt', 'Surabaya'],
    'nilai': [80, 80, 70, 90, 70, 60, 90],
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

def jumlah_duplikat(df, subset):
    return int(df.duplicated(subset).sum())
"""
F12 = """
import pandas as pd

def id_kelompok_duplikat(df, subset):
    return df.loc[df.duplicated(subset, keep=False), 'id'].tolist()
"""
F13 = """
import pandas as pd

def normalisasi_kunci(df, kolom):
    return df[kolom].str.strip().str.lower().tolist()
"""
F14 = """
import pandas as pd

def id_setelah_normalisasi(df, subset):
    b = df.copy()
    for k in subset:
        if b[k].dtype == object or str(b[k].dtype).startswith('str'):
            b[k] = b[k].str.strip().str.lower()
    return b.drop_duplicates(subset)['id'].tolist()
"""

l1 = lesson(
    "B3-03-1",
    "Mendeteksi baris duplikat",
    35,
    [
        "Membedakan duplikat persis dan duplikat berdasarkan kunci",
        "Memakai duplicated dan drop_duplicates dengan subset dan keep",
        "Melihat seluruh anggota kelompok duplikat",
        "Menormalkan teks sebelum mendeteksi duplikat tersembunyi",
    ],
    [
        tb("Mengapa duplikat berbahaya", "Baris ganda tampak sepele, tetapi dampaknya nyata. Bila seorang pelanggan tercatat dua kali, total penjualan dan jumlah pelanggan menggembung. Bila baris duplikat jatuh ke data latih dan data uji sekaligus, model seakan-akan menghafal jawaban dan skor evaluasi menjadi terlalu bagus. Duplikat muncul dari banyak sumber: formulir yang dikirim dua kali, penggabungan beberapa file yang tumpang tindih, proses impor yang diulang, atau pengguna yang mendaftar dengan ejaan berbeda. Pelajaran ini membahas cara mendeteksi duplikat dengan pandas, termasuk duplikat yang tersembunyi di balik perbedaan huruf besar dan spasi."),
        tb("Data contoh", "Pelajaran ini memakai tabel tujuh baris dengan kolom `id`, `nama`, `kota`, dan `nilai`. Sekilas tidak ada baris yang sama persis karena `id` selalu berbeda. Namun mata manusia segera melihat bahwa Ani Putri muncul dua kali dengan huruf besar berbeda dan spasi di ujung, Budi muncul dua kali dengan kota dan nilai sama, dan Cici juga muncul dua kali. Kota juga ditulis dengan banyak cara. Tabel kecil ini sengaja dibuat berantakan agar setiap teknik dapat Anda periksa langsung dengan mata sebelum dipakai pada tabel besar."),
        tb("Duplikat persis dan duplikat kunci", "Ada dua makna duplikat. Duplikat persis berarti seluruh kolom sama. Duplikat kunci berarti kolom-kolom yang mengidentifikasi entitas sama, walaupun kolom lain boleh berbeda. Pada tabel pelanggan, kunci bisa berupa email, atau gabungan nama dan tanggal lahir. Kolom `id` yang dibuat otomatis hampir tidak pernah ikut kunci, karena ia selalu unik dan menyembunyikan duplikat. Langkah pertama yang baik adalah memutuskan secara eksplisit kolom mana yang membentuk kunci, lalu menuliskannya, sebab seluruh deteksi dan penghapusan bergantung pada keputusan ini."),
        tb("duplicated dan subset", "Metode `df.duplicated()` mengembalikan deret boolean yang bernilai benar untuk setiap baris yang sudah pernah muncul sebelumnya. Baris pertama dari suatu kelompok bernilai salah, dan sisanya benar. Parameter `subset` membatasi pemeriksaan pada kolom tertentu, misalnya `df.duplicated(['nama', 'kota'])`. Tanpa subset, semua kolom dibandingkan, sehingga pada contoh kita tidak ada duplikat karena `id` berbeda. Menjumlahkan deret boolean dengan `sum()` memberi jumlah baris berlebih, yaitu baris yang akan hilang bila Anda menghapus duplikat dan menyisakan satu wakil."),
        C(
            P("""
print(df.duplicated().tolist())
print(df.duplicated(['nama']).tolist())
print(df.duplicated(['nama', 'kota', 'nilai']).tolist())
print(df.duplicated(['nilai']).sum(), df.duplicated(['id']).sum())
print(df.duplicated().sum(), df.drop(columns='id').duplicated().sum())
"""),
            ind("""
[False, False, False, False, False, False, False]
[False, False, False, False, True, False, False]
[False, False, False, False, True, False, False]
3 0
0 1
"""),
            "Tanpa subset, kolom id yang unik menyembunyikan semua duplikat. Dengan subset nama dan kota dan nilai, hanya baris kelima yang terdeteksi sebagai pengulangan Budi.",
            filename="duplicated_dasar.py",
        ),
        tb("Memilih baris yang dipertahankan", "Parameter `keep` menentukan baris mana yang dianggap asli. Nilai bawaan `first` menandai kemunculan berikutnya sebagai duplikat dan mempertahankan yang pertama. Nilai `last` mempertahankan yang terakhir, berguna bila data lebih baru berada di bawah. Nilai `False` menandai semua anggota kelompok duplikat, termasuk yang pertama. Pilihan ini penting karena data tidak selalu terurut. Jika Anda mengira yang pertama adalah yang terbaru padahal sebaliknya, Anda membuang versi yang benar dan menyimpan yang usang. Selalu urutkan data secara sadar sebelum menghapus duplikat."),
        tb("Melihat semua anggota kelompok", "Sebelum menghapus, lihatlah seluruh anggota kelompok duplikat, bukan hanya pengulangannya. Dengan `keep=False`, deret boolean bernilai benar untuk semua anggota kelompok yang beranggota lebih dari satu. Menyaring dengan deret itu menampilkan pasangan atau kelompok yang akan dipangkas sehingga Anda dapat memeriksa apakah memang duplikat sungguhan. Kebiasaan ini mencegah kecelakaan, misalnya dua orang berbeda yang kebetulan bernama sama dan berasal dari kota sama. Hapus hanya setelah Anda yakin kunci Anda cukup tajam untuk membedakan entitas."),
        C(
            P("""
k = ['nama', 'kota', 'nilai']
print(df.duplicated(k, keep=False).tolist())
print(df.loc[df.duplicated(k, keep=False), 'id'].tolist())
print(df.drop_duplicates(k)['id'].tolist())
print(df.drop_duplicates(k, keep='last')['id'].tolist())
print(len(df.drop_duplicates(k)), len(df))
"""),
            ind("""
[False, False, True, False, True, False, False]
[3, 5]
[1, 2, 3, 4, 6, 7]
[1, 2, 4, 5, 6, 7]
6 7
"""),
            "Keep false menampilkan kedua anggota pasangan. Keep first mempertahankan id 3 sedangkan keep last mempertahankan id 5.",
            filename="keep_duplikat.py",
        ),
        tb("Duplikat tersembunyi", "Mata Anda melihat bahwa Ani Putri dan ani putri adalah orang yang sama, tetapi komputer membandingkan karakter satu demi satu sehingga huruf besar dan kecil dianggap berbeda, dan spasi di ujung juga dianggap karakter. Karena itu duplikat tersembunyi tidak terdeteksi. Solusinya menormalkan kolom kunci sebelum membandingkan: buang spasi di tepi dengan `str.strip`, samakan huruf dengan `str.lower`, dan bila perlu rapatkan spasi ganda di tengah. Normalisasi dilakukan pada salinan atau kolom bantu agar data asli tidak rusak."),
        tb("Menormalkan lalu mendeteksi", "Setelah nama dan kota dinormalkan menjadi huruf kecil tanpa spasi tepi, deteksi pada pasangan nama dan kota menemukan dua duplikat, yaitu baris kedua sebagai pengulangan Ani Putri dan baris kelima sebagai pengulangan Budi. Cici pada baris keempat dan ketujuh tidak dihitung duplikat karena kotanya berbeda, Bandung dan Surabaya, dan hal itu masuk akal bila kunci mencakup kota. Perhatikan bahwa hasil bergantung pada kunci. Perubahan kecil pada daftar kolom kunci mengubah jumlah duplikat, sehingga catat pilihan Anda dalam laporan."),
        C(
            P("""
b = df.assign(nama=df['nama'].str.strip().str.lower(), kota=df['kota'].str.strip().str.lower())
print(b['nama'].tolist())
print(b.duplicated(['nama', 'kota']).tolist())
print(b.drop_duplicates(['nama', 'kota'])['id'].tolist(), len(b.drop_duplicates(['nama', 'kota'])))
print(b.duplicated(['nama']).sum(), df.duplicated(['nama']).sum())
print(df['nama'].str.len().tolist(), df['nama'].str.strip().str.len().tolist())
"""),
            ind("""
['ani putri', 'ani putri', 'budi', 'cici', 'budi', 'dedi', 'cici']
[False, True, False, False, True, False, False]
[1, 3, 4, 6, 7] 5
3 1
[9, 10, 4, 4, 4, 4, 4]
[9, 9, 4, 4, 4, 4, 4]
"""),
            "Setelah normalisasi, duplikat meningkat dari satu menjadi tiga pada kolom nama saja. Spasi tepi terlihat dari panjang teks yang berbeda sebelum dan sesudah strip.",
            filename="duplikat_tersembunyi.py",
        ),
        tb("Memeriksa panjang untuk menemukan spasi", "Spasi di ujung teks tidak terlihat saat mencetak. Cara cepat menemukannya adalah membandingkan panjang teks sebelum dan sesudah `strip`. Pada contoh, nama kedua memiliki panjang sepuluh sebelum dan sembilan sesudah, tanda adanya spasi tersembunyi. Pemeriksaan serupa dapat dilakukan dengan `df['nama'] != df['nama'].str.strip()` untuk menyaring baris bermasalah. Karakter tak terlihat lain, seperti tab, pemisah baris, dan spasi tanpa putus dari salinan halaman web, juga sering menjadi biang duplikat tersembunyi pada data hasil tempel dari dokumen."),
        tb("Duplikat dan kebocoran data", "Pada pemodelan, duplikat punya risiko tambahan. Bila Anda membagi data menjadi latih dan uji secara acak sebelum menghapus duplikat, salinan baris yang sama dapat berada di kedua sisi. Model yang menghafal baris latih akan tampak menebak baris uji dengan sempurna, padahal itu hanya mengingat. Aturannya jelas: hapus atau kelompokkan duplikat sebelum membagi data. Bila baris hampir sama harus tetap ada, bagi data menurut kelompok kunci sehingga seluruh anggota satu kelompok masuk sisi yang sama."),
        K("warn", "Kolom id otomatis hampir selalu unik dan menyembunyikan duplikat. Tentukan kolom kunci secara eksplisit dan jangan memeriksa duplikat dengan semua kolom bila ada id.", title="Jangan ikutkan id"),
        tb("Contoh dari dunia nyata", "Bayangkan toko daring dengan tabel pesanan. Pelanggan menekan tombol bayar dua kali karena koneksi lambat, sehingga sistem menyimpan dua pesanan dengan isi sama dan selisih waktu satu detik. Laporan penjualan bulanan lalu melebih-lebihkan omzet. Kasus lain: tim pemasaran mengunggah daftar kontak dari tiga kegiatan berbeda, dan banyak orang hadir di lebih dari satu kegiatan, sehingga email yang sama muncul beberapa kali dengan nama ditulis berbeda. Kampanye surel lalu mengirim pesan ganda dan pelanggan merasa terganggu. Pola serupa terjadi di hampir setiap organisasi, dan mengenalinya adalah keterampilan dasar analis data."),
        tb("Menyusun daftar periksa deteksi", "Untuk membuat deteksi menjadi kebiasaan, susun daftar periksa singkat. Pertama, tentukan kolom kunci dan tulis alasannya. Kedua, hitung duplikat persis dan duplikat kunci. Ketiga, normalkan teks lalu hitung ulang dan bandingkan angkanya. Keempat, lihat seluruh anggota beberapa kelompok dengan keep False. Kelima, catat jumlah dan persentase dalam laporan kualitas. Daftar sederhana ini mudah diulang pada setiap dataset baru, dan perbandingan angka sebelum dan sesudah normalisasi segera memberi tahu seberapa tersembunyi masalah duplikat pada data yang sedang Anda hadapi."),
        E(
            "B3-03-1-ex1",
            "mudah",
            "Tulis fungsi `jumlah_duplikat(df, subset)` yang mengembalikan bilangan bulat jumlah baris yang dianggap duplikat menurut kolom `subset` (kemunculan pertama tidak dihitung).",
            ind("""
import pandas as pd

def jumlah_duplikat(df, subset):
    # TODO: implementasikan
    pass
"""),
            P("""
assert jumlah_duplikat(df, ['nama']) == 1
assert jumlah_duplikat(df, ['nilai']) == 3
assert jumlah_duplikat(df, ['id']) == 0
assert jumlah_duplikat(df, ['nama', 'kota', 'nilai']) == 1
"""),
            "duplicated dengan subset lalu sum.",
            X(F11),
        ),
        E(
            "B3-03-1-ex2",
            "sedang",
            "Tulis fungsi `id_kelompok_duplikat(df, subset)` yang mengembalikan list `id` semua baris yang menjadi anggota kelompok duplikat menurut `subset`, termasuk kemunculan pertama.",
            ind("""
import pandas as pd

def id_kelompok_duplikat(df, subset):
    # TODO: implementasikan
    pass
"""),
            P("""
assert id_kelompok_duplikat(df, ['nama', 'kota', 'nilai']) == [3, 5]
assert id_kelompok_duplikat(df, ['nilai']) == [1, 2, 3, 4, 5, 7]
assert id_kelompok_duplikat(df, ['id']) == []
assert id_kelompok_duplikat(df, ['nama']) == [3, 5]
"""),
            "duplicated dengan keep False sebagai penyaring baris.",
            X(F12),
        ),
        E(
            "B3-03-1-ex3",
            "sedang",
            "Tulis fungsi `normalisasi_kunci(df, kolom)` yang mengembalikan list nilai kolom teks setelah spasi tepi dibuang dan huruf diubah menjadi kecil.",
            ind("""
import pandas as pd

def normalisasi_kunci(df, kolom):
    # TODO: implementasikan
    pass
"""),
            P("""
assert normalisasi_kunci(df, 'nama') == ['ani putri', 'ani putri', 'budi', 'cici', 'budi', 'dedi', 'cici']
assert normalisasi_kunci(df, 'kota')[1] == 'jakarta'
assert normalisasi_kunci(df, 'kota')[3] == 'bandung'
assert len(set(normalisasi_kunci(df, 'kota'))) == 4
"""),
            "str.strip diikuti str.lower lalu tolist.",
            X(F13),
        ),
        E(
            "B3-03-1-ex4",
            "menantang",
            "Tulis fungsi `id_setelah_normalisasi(df, subset)` yang menormalkan (strip dan lower) kolom teks di `subset` pada salinan, menghapus duplikat menurut `subset`, dan mengembalikan list `id` yang tersisa.",
            ind("""
import pandas as pd

def id_setelah_normalisasi(df, subset):
    # TODO: implementasikan
    pass
"""),
            P("""
assert id_setelah_normalisasi(df, ['nama', 'kota']) == [1, 3, 4, 6, 7]
assert id_setelah_normalisasi(df, ['nama']) == [1, 3, 4, 6]
assert id_setelah_normalisasi(df, ['nama', 'kota', 'nilai']) == [1, 3, 4, 6, 7]
assert df['nama'].tolist()[1] == 'ani putri '
"""),
            "Normalkan kolom teks pada salinan lalu drop_duplicates dengan subset.",
            X(F14),
        ),
    ],
    [
        M("Memeriksa duplikat dengan semua kolom padahal ada id unik.", "Tentukan kolom kunci dan pakai subset."),
        M("Menghapus duplikat tanpa melihat anggota kelompoknya.", "Tampilkan dengan keep False dan periksa dulu."),
        M("Membandingkan teks tanpa normalisasi.", "Strip dan lower dulu pada kolom kunci."),
    ],
    [
        Q("Parameter yang membatasi kolom pemeriksaan?", ["subset", "keep", "axis", "inplace"], 0, "Subset.", hint="Daftar kolom."),
        Q("keep=False menandai?", ["Semua anggota kelompok duplikat", "Hanya yang pertama", "Hanya yang terakhir", "Tidak ada"], 0, "Semua anggota.", hint="Semua."),
        Q("Duplikat tersembunyi sering karena?", ["Huruf besar dan spasi", "Tipe int", "Indeks", "Urutan kolom"], 0, "Teks tidak seragam.", hint="Teks."),
        Q("Hapus duplikat sebaiknya sebelum?", ["Membagi data latih dan uji", "Membaca file", "Mencetak", "Menamai kolom"], 0, "Cegah kebocoran.", hint="Pembagian."),
        Q("Kolom id otomatis biasanya?", ["Tidak dipakai sebagai kunci", "Selalu kunci", "Diubah ke teks", "Dihapus pertama"], 0, "Selalu unik.", hint="Unik."),
    ],
    [
        "Duplikat persis berbeda dari duplikat berdasarkan kunci.",
        "duplicated dan drop_duplicates memakai subset dan keep.",
        "keep False menampilkan seluruh kelompok duplikat untuk diperiksa.",
        "Normalisasi teks mengungkap duplikat tersembunyi.",
    ],
    [],
)

G11 = """
import pandas as pd

def bersihkan_teks(daftar):
    return [' '.join(str(x).split()).lower() for x in daftar]
"""
G12 = """
import pandas as pd

def hitung_varian(df, kolom):
    mentah = int(df[kolom].nunique())
    bersih = int(df[kolom].astype(str).str.strip().str.lower().nunique())
    return (mentah, bersih)
"""
G13 = """
import pandas as pd

def terapkan_peta(df, kolom, peta):
    return df[kolom].str.strip().str.lower().replace(peta).tolist()
"""
G14 = """
import difflib

def cocok_terdekat(kata, baku, cutoff):
    hasil = difflib.get_close_matches(kata, baku, n=1, cutoff=cutoff)
    return hasil[0] if hasil else None
"""

l2 = lesson(
    "B3-03-2",
    "Inkonsistensi kategori dan ejaan",
    35,
    [
        "Menemukan varian penulisan dengan value_counts dan nunique",
        "Menyeragamkan huruf, spasi, dan ejaan dengan peta penggantian",
        "Memakai pencocokan mirip untuk ejaan yang salah",
        "Menyusun daftar nilai baku yang dapat dipakai ulang",
    ],
    [
        tb("Satu kota, banyak tulisan", "Kolom kategori adalah sumber inkonsistensi terbesar dalam data nyata. Jakarta bisa tertulis Jakarta, jakarta, JAKARTA, Jkt, atau Jakarta Pusat tergantung siapa yang mengetik. Bagi manusia semuanya jelas sama, tetapi untuk groupby atau model, setiap tulisan dianggap kategori terpisah. Hasilnya, rata-rata per kota terpecah menjadi potongan kecil yang menyesatkan, dan variabel boneka melonjak jumlahnya tanpa alasan. Pelajaran ini membahas cara menemukan dan menyeragamkan varian, dari yang mudah seperti huruf besar hingga ejaan salah yang memerlukan pencocokan mirip."),
        tb("Menemukan varian", "Langkah pertama selalu melihat daftar nilai unik beserta frekuensinya. `value_counts()` menampilkan tiap tulisan dan jumlahnya, sedangkan `nunique()` menghitung banyaknya tulisan berbeda. Pada contoh, kolom kota memiliki enam tulisan berbeda, padahal setelah huruf diseragamkan hanya tersisa empat. Selisih antara jumlah unik mentah dan jumlah unik setelah normalisasi adalah ukuran cepat seberapa berantakan suatu kolom. Selisih nol berarti kolom bersih dari masalah huruf dan spasi, sedangkan selisih besar menandakan pekerjaan pembersihan yang perlu direncanakan."),
        C(
            P("""
print(df['kota'].value_counts().to_dict())
print(df['kota'].nunique(), df['kota'].str.lower().nunique())
print(sorted(set(df['kota'].str.lower())))
print(df['nama'].nunique(), df['nama'].str.strip().str.lower().nunique())
print(df['kota'].str.strip().str.lower().value_counts().to_dict())
"""),
            ind("""
{'Bandung': 2, 'Jakarta': 1, 'jakarta': 1, 'BANDUNG': 1, 'Jkt': 1, 'Surabaya': 1}
6 4
['bandung', 'jakarta', 'jkt', 'surabaya']
6 4
{'bandung': 3, 'jakarta': 2, 'jkt': 1, 'surabaya': 1}
"""),
            "Jumlah unik turun dari enam menjadi empat setelah huruf diseragamkan. Daftar terurut nilai unik memperlihatkan sisa masalah, yaitu singkatan jkt.",
            filename="varian_kota.py",
        ),
        tb("Menyeragamkan huruf dan spasi", "Perbaikan paling sederhana dan paling aman adalah menyeragamkan huruf dan spasi. Gunakan `str.strip` untuk membuang spasi di tepi, `str.lower` atau `str.title` untuk menyamakan huruf, dan `' '.join(s.split())` atau ekspresi reguler untuk merapatkan spasi ganda di tengah. Pilih satu konvensi dan pakai konsisten: huruf kecil mudah untuk pencocokan dan kunci, sedangkan huruf judul lebih enak dibaca di laporan. Praktik umum menyimpan kolom bersih untuk analisis dan menampilkan versi cantik hanya pada tahap presentasi."),
        tb("Peta penggantian", "Setelah huruf seragam, sisa varian seperti singkatan dan nama lain ditangani dengan peta penggantian, yaitu kamus dari tulisan yang salah ke tulisan baku. Misalnya `{'jkt': 'jakarta'}`. Metode `replace` pada Series menerapkan peta itu dan membiarkan nilai yang tidak ada di peta. Peta ini adalah aset: simpan dalam berkas atau modul tersendiri, bukan tersebar dalam kode, sehingga dapat ditinjau dan diperbarui. Setiap kali data baru membawa varian baru, tambahkan entri peta dan jalankan ulang seluruh alur."),
        C(
            P("""
b = df['kota'].str.strip().str.lower()
peta = {'jkt': 'jakarta'}
c = b.replace(peta)
print(c.tolist())
print(c.value_counts().to_dict(), c.nunique())
print(b.map(peta).tolist())
print(b.map(lambda x: peta.get(x, x)).tolist() == c.tolist())
print(df['nama'].str.strip().str.title().tolist())
"""),
            ind("""
['jakarta', 'jakarta', 'bandung', 'bandung', 'bandung', 'jakarta', 'surabaya']
{'jakarta': 3, 'bandung': 3, 'surabaya': 1} 3
[nan, nan, nan, nan, nan, 'jakarta', nan]
True
['Ani Putri', 'Ani Putri', 'Budi', 'Cici', 'Budi', 'Dedi', 'Cici']
"""),
            "Replace mengganti hanya nilai yang ada di peta, sedangkan map menghasilkan NaN untuk nilai di luar peta. Gunakan get dengan nilai cadangan bila memakai map.",
            filename="peta_ganti.py",
        ),
        tb("Replace berbeda dari map", "Dua metode ini sering tertukar. `replace` dengan kamus hanya mengganti kunci yang cocok dan membiarkan yang lain, sehingga aman untuk perbaikan sebagian. `map` dengan kamus mengubah setiap nilai dan menghasilkan NaN untuk nilai yang tidak ada di kamus, yang berguna untuk pengodean penuh tetapi berbahaya bila peta tidak lengkap. Bila Anda memakai map untuk pembersihan, pakai `lambda x: peta.get(x, x)` agar nilai di luar peta tetap utuh. Periksa jumlah NaN setelah pemetaan untuk memastikan tidak ada data tak sengaja hilang."),
        tb("Ejaan salah dan pencocokan mirip", "Peta manual cukup bila variannya sedikit. Untuk ejaan salah yang beragam, seperti jakrta, jakartaa, atau bandun, pencocokan mirip membantu. Modul `difflib` bawaan Python menyediakan `get_close_matches(kata, daftar, n, cutoff)` yang mengembalikan kandidat dari daftar baku yang paling mirip dengan kata masukan, dengan ambang kemiripan antara nol dan satu. Ambang tinggi mengurangi salah cocok tetapi melewatkan koreksi, sedangkan ambang rendah menangkap lebih banyak tetapi berisiko mencocokkan kata yang sebenarnya berbeda. Tidak ada ambang yang benar untuk semua kasus."),
        C(
            P("""
import difflib
baku = ['jakarta', 'bandung', 'surabaya']
print(difflib.get_close_matches('jakrta', baku, n=1, cutoff=0.8))
print(difflib.get_close_matches('bandun', baku, n=1, cutoff=0.8))
print(difflib.get_close_matches('xyz', baku, n=1, cutoff=0.8))
print(difflib.get_close_matches('jkt', baku, n=1, cutoff=0.5))
print(round(difflib.SequenceMatcher(None, 'jakarta', 'jkt').ratio(), 2), round(difflib.SequenceMatcher(None, 'ani', 'ana').ratio(), 3))
"""),
            ind("""
['jakarta']
['bandung']
[]
['jakarta']
0.6 0.667
"""),
            "Kemiripan jakarta dan jkt hanya 0.6, sehingga ambang tinggi akan melewatkannya. Singkatan sebaiknya ditangani dengan peta manual, bukan pencocokan mirip.",
            filename="difflib_cocok.py",
        ),
        tb("Batas pencocokan mirip", "Pencocokan mirip bukan sihir. Ia mengukur kemiripan huruf, bukan makna. Ani dan Ana mirip hampir tujuh puluh persen padahal bisa jadi dua orang berbeda, sementara Jakarta dan Jkt hanya mirip enam puluh persen padahal sama. Karena itu hasilnya harus ditinjau manusia untuk kolom penting, atau dibatasi pada daftar baku yang kecil dan jelas seperti nama kota atau provinsi. Untuk nama orang, pencocokan otomatis berisiko menggabungkan orang berbeda. Lebih baik biarkan sebagai kandidat yang ditandai untuk ditinjau daripada digabungkan diam-diam."),
        tb("Daftar baku", "Cara paling kuat mencegah inkonsistensi adalah memiliki daftar baku, yaitu himpunan nilai sah untuk tiap kolom kategori. Dengan daftar ini Anda dapat memeriksa setiap data baru: nilai yang tidak ada dalam daftar ditandai, dikoreksi lewat peta, atau dicocokkan mirip lalu ditinjau. Di sistem sumber, cara terbaik tentu memakai menu pilihan alih-alih kolom teks bebas. Bila Anda tidak mengendalikan sumber, daftar baku di sisi analisis tetap memberi jaring pengaman. Simpan daftar baku di berkas konfigurasi agar tim lain memakai versi yang sama."),
        tb("Memeriksa kategori di luar daftar", "Setelah menormalkan, selalu periksa nilai yang berada di luar daftar baku dengan `~b.isin(baku)`. Hasilnya adalah baris bermasalah yang perlu ditangani, dan jumlahnya menjadi ukuran kualitas kolom. Laporkan persentase nilai di luar daftar sebelum dan sesudah pembersihan sehingga pembaca dapat melihat perbaikan nyata. Bila persentase masih tinggi setelah peta dan pencocokan, kemungkinan ada kategori sah baru yang belum masuk daftar, atau sumber data bermasalah yang perlu diperbaiki dari hulunya, bukan di sisi analisis saja."),
        K("tip", "Simpan peta penggantian dan daftar baku di berkas terpisah. Dengan begitu pembersihan dapat ditinjau, diperbarui, dan dipakai ulang di semua proyek.", title="Peta sebagai aset"),
        tb("Kasus huruf judul dan akronim", "Memakai `str.title` terlihat rapi tetapi dapat merusak akronim dan nama khusus. Kata seperti DKI, UI, atau McDonald akan menjadi Dki, Ui, dan Mcdonald. Untuk kolom kunci dan analisis, huruf kecil lebih aman karena tidak ada keputusan estetika. Gunakan huruf judul hanya pada tahap tampilan, dan bila perlu sediakan pengecualian untuk akronim yang dikenal. Begitu pula dengan menghapus tanda baca: titik dalam singkatan atau tanda hubung dalam nama dapat bermakna, sehingga periksa dulu apakah penghapusan menggabungkan dua nilai yang sebenarnya berbeda."),
        tb("Karakter tak terlihat", "Selain spasi biasa, teks hasil salinan sering membawa karakter tak terlihat seperti spasi tanpa putus, tab, pemisah baris, atau penanda urutan byte. Karakter ini lolos dari `strip` bawaan dalam beberapa kasus dan membuat dua teks yang tampak sama berbeda bagi komputer. Gejala khasnya adalah value_counts yang menampilkan dua baris yang tampak identik. Periksa dengan `repr` pada nilai mencurigakan, atau ganti kelas karakter spasi dengan ekspresi reguler `\\s+` menjadi satu spasi. Pembersihan semacam ini sebaiknya menjadi langkah pertama sebelum mendeteksi duplikat atau varian apa pun."),
        tb("Menyimpan hasil pembersihan", "Setelah kategori seragam, simpan hasilnya sebagai kolom baru atau berkas bersih, jangan menimpa kolom asli. Kolom asli berguna untuk menelusuri asal nilai dan untuk memperbaiki peta bila ternyata ada kesalahan. Beri nama jelas seperti kota_bersih, dan dokumentasikan aturan yang dipakai. Pada alur otomatis, jalankan pemeriksaan jumlah kategori unik setelah pembersihan dan beri peringatan bila angkanya melonjak, karena itu tanda varian baru muncul dari sumber data."),
        E(
            "B3-03-2-ex1",
            "mudah",
            "Tulis fungsi `bersihkan_teks(daftar)` yang menerima list teks dan mengembalikan list teks dengan spasi ganda dirapatkan menjadi satu, spasi tepi dibuang, dan semua huruf kecil.",
            ind("""
def bersihkan_teks(daftar):
    # TODO: implementasikan
    pass
"""),
            P("""
assert bersihkan_teks(['  Ani   Putri ', 'BUDI']) == ['ani putri', 'budi']
assert bersihkan_teks(['a  b   c']) == ['a b c']
assert bersihkan_teks([]) == []
assert bersihkan_teks(['  X ']) == ['x']
"""),
            "split lalu join dengan satu spasi lalu lower.",
            X(G11),
        ),
        E(
            "B3-03-2-ex2",
            "sedang",
            "Tulis fungsi `hitung_varian(df, kolom)` yang mengembalikan tuple `(unik_mentah, unik_bersih)` dengan jumlah nilai unik sebelum dan sesudah strip dan lower.",
            ind("""
import pandas as pd

def hitung_varian(df, kolom):
    # TODO: implementasikan
    pass
"""),
            P("""
assert hitung_varian(df, 'kota') == (6, 4)
assert hitung_varian(df, 'nama') == (6, 4)
assert hitung_varian(df, 'nilai') == (4, 4)
assert hitung_varian(df.iloc[[0, 1]], 'kota') == (2, 1)
"""),
            "nunique mentah dan nunique setelah astype str strip lower.",
            X(G12),
        ),
        E(
            "B3-03-2-ex3",
            "sedang",
            "Tulis fungsi `terapkan_peta(df, kolom, peta)` yang membuang spasi tepi, mengubah ke huruf kecil, lalu mengganti nilai sesuai `peta` (nilai di luar peta tetap) dan mengembalikan list.",
            ind("""
import pandas as pd

def terapkan_peta(df, kolom, peta):
    # TODO: implementasikan
    pass
"""),
            P("""
assert terapkan_peta(df, 'kota', {'jkt': 'jakarta'}) == ['jakarta', 'jakarta', 'bandung', 'bandung', 'bandung', 'jakarta', 'surabaya']
assert terapkan_peta(df, 'kota', {})[5] == 'jkt'
assert terapkan_peta(df, 'nama', {'cici': 'cc'})[3] == 'cc'
assert terapkan_peta(df, 'nama', {'cici': 'cc'})[2] == 'budi'
"""),
            "strip lower lalu replace dengan kamus.",
            X(G13),
        ),
        E(
            "B3-03-2-ex4",
            "menantang",
            "Tulis fungsi `cocok_terdekat(kata, baku, cutoff)` yang mengembalikan kata baku paling mirip memakai `difflib.get_close_matches` atau `None` bila tidak ada yang melewati ambang.",
            ind("""
import difflib

def cocok_terdekat(kata, baku, cutoff):
    # TODO: implementasikan
    pass
"""),
            P("""
baku = ['jakarta', 'bandung', 'surabaya']
assert cocok_terdekat('jakrta', baku, 0.8) == 'jakarta'
assert cocok_terdekat('bandun', baku, 0.8) == 'bandung'
assert cocok_terdekat('xyz', baku, 0.8) is None
assert cocok_terdekat('jkt', baku, 0.5) == 'jakarta'
"""),
            "get_close_matches dengan n satu lalu ambil elemen pertama atau None.",
            X(G14),
        ),
    ],
    [
        M("Mengabaikan varian huruf pada kolom kategori.", "Cek value_counts dan nunique sebelum groupby."),
        M("Memakai map untuk perbaikan sebagian.", "Pakai replace atau map dengan get cadangan."),
        M("Menyerahkan nama orang pada pencocokan mirip otomatis.", "Tandai kandidat dan tinjau manual."),
    ],
    [
        Q("Mengetahui varian tulisan memakai?", ["value_counts", "shape", "head", "dtypes"], 0, "Frekuensi.", hint="Hitung."),
        Q("replace dengan kamus untuk nilai di luar kamus?", ["Dibiarkan", "Menjadi NaN", "Dihapus", "Error"], 0, "Tetap.", hint="Tetap."),
        Q("map dengan kamus untuk nilai di luar kamus?", ["Menjadi NaN", "Dibiarkan", "Dihapus", "Nol"], 0, "NaN.", hint="NaN."),
        Q("difflib mengukur kemiripan?", ["Huruf", "Makna", "Panjang", "Frekuensi"], 0, "Huruf.", hint="Karakter."),
        Q("Daftar baku berguna untuk?", ["Memeriksa nilai sah", "Mengurutkan", "Menggabung", "Mengompres"], 0, "Validasi.", hint="Sah."),
    ],
    [
        "Selisih unik mentah dan bersih mengukur kekacauan kolom.",
        "Seragamkan huruf dan spasi lalu pakai peta untuk sisa varian.",
        "Replace dan map berbeda perilaku pada nilai di luar peta.",
        "Pencocokan mirip membantu tetapi butuh tinjauan manusia.",
    ],
    [],
)

H11 = """
import pandas as pd

def gabung_per_nama(df):
    b = df.assign(nama=df['nama'].str.strip().str.lower())
    g = b.groupby('nama').agg(n=('id', 'size'), rata=('nilai', 'mean'))
    return {k: (int(r.n), float(r.rata)) for k, r in g.iterrows()}
"""
H12 = """
import pandas as pd

def simpan_tertinggi(df):
    b = df.assign(nama=df['nama'].str.strip().str.lower())
    b = b.sort_values('nilai', ascending=False, kind='stable')
    return b.drop_duplicates('nama')['id'].tolist()
"""
H13 = """
import pandas as pd

def konflik_kunci(df, kunci, nilai):
    b = df.assign(**{kunci: df[kunci].str.strip().str.lower()})
    n = b.groupby(kunci)[nilai].nunique()
    return sorted(n[n > 1].index.tolist())
"""
H14 = """
import pandas as pd

def laporan_dedup(df, subset):
    b = df.copy()
    for k in subset:
        b[k] = b[k].str.strip().str.lower()
    sesudah = len(b.drop_duplicates(subset))
    return {'sebelum': len(df), 'sesudah': sesudah, 'dibuang': len(df) - sesudah}
"""

l3 = lesson(
    "B3-03-3",
    "Menyelesaikan duplikat dengan aman",
    35,
    [
        "Memilih strategi: buang, gabung, atau pertahankan versi terbaik",
        "Menggabungkan kelompok duplikat dengan groupby dan agregasi",
        "Mendeteksi konflik nilai di dalam kelompok duplikat",
        "Menyusun laporan deduplikasi yang dapat diaudit",
    ],
    [
        tb("Mendeteksi belum menyelesaikan", "Menemukan duplikat hanyalah separuh pekerjaan. Setelah kelompok duplikat teridentifikasi, Anda harus memutuskan apa yang dilakukan dengannya. Membuang semuanya kecuali satu tampak jelas, tetapi baris mana yang dipertahankan memengaruhi hasil bila isinya tidak persis sama. Dua catatan tentang Budi mungkin memuat nilai berbeda, atau satu catatan mungkin lengkap sedangkan lainnya kosong. Pelajaran ini membahas tiga strategi, yaitu membuang, menggabung, dan memilih versi terbaik, serta cara mendeteksi konflik dan mendokumentasikan keputusan agar dapat diaudit."),
        tb("Strategi pertama: buang", "Bila duplikat benar-benar identik pada semua kolom penting, cukup pertahankan satu dengan `drop_duplicates`. Ini kasus terbersih dan paling aman, misalnya hasil impor ganda. Namun sebelum membuang, pastikan baris itu memang identik pada kolom yang Anda pedulikan, bukan hanya pada kunci. Cara cepatnya membandingkan jumlah baris unik menurut kunci dengan jumlah baris unik menurut semua kolom non-id. Jika sama, tidak ada informasi yang hilang. Jika berbeda, ada konflik nilai yang perlu strategi lain, karena membuang akan menghilangkan data diam-diam."),
        tb("Strategi kedua: gabung", "Bila setiap catatan memuat sebagian informasi, gabungkan menjadi satu catatan lengkap. Gunakan `groupby` pada kunci yang telah dinormalkan lalu agregasi tiap kolom dengan aturan yang masuk akal: rata-rata atau maksimum untuk angka, nilai pertama yang tidak kosong untuk teks, jumlah untuk transaksi. Aturan agregasi ini adalah keputusan bisnis, bukan teknis, sehingga lakukan bersama pemilik data. Ingat bahwa menjumlahkan transaksi duplikat menggandakan nilai, sementara menjumlahkan transaksi terpisah milik satu pelanggan benar. Bedakan keduanya sebelum memilih agregasi."),
        C(
            P("""
b = df.assign(nama=df['nama'].str.strip().str.lower())
g = b.groupby('nama').agg(n=('id', 'size'), rata=('nilai', 'mean'))
print(g['n'].to_dict(), g['rata'].to_dict())
print(b.groupby('nama')['nilai'].nunique().to_dict())
print(b.groupby('nama')['kota'].first().to_dict())
print(b.drop(columns='id').duplicated().sum(), b.drop(columns='id').drop_duplicates().shape)
"""),
            ind("""
{'ani putri': 2, 'budi': 2, 'cici': 2, 'dedi': 1} {'ani putri': 80.0, 'budi': 70.0, 'cici': 90.0, 'dedi': 60.0}
{'ani putri': 1, 'budi': 1, 'cici': 1, 'dedi': 1}
{'ani putri': 'Jakarta', 'budi': 'Bandung', 'cici': 'BANDUNG', 'dedi': 'Jkt'}
1 (6, 3)
"""),
            "Setiap nama memiliki satu nilai unik sehingga tidak ada konflik nilai. Kota masih belum seragam, jadi first mengambil tulisan mentah yang berbeda-beda.",
            filename="gabung_duplikat.py",
        ),
        tb("Strategi ketiga: versi terbaik", "Kadang catatan duplikat berbeda kualitas atau waktu, dan Anda ingin mempertahankan yang terbaik. Contohnya yang paling baru, yang paling lengkap, atau yang bernilai tertinggi. Caranya urutkan baris menurut kriteria, lalu `drop_duplicates` pada kunci dengan `keep='first'`. Gunakan `kind='stable'` pada `sort_values` agar urutan baris sama kriterianya tetap deterministik. Tanpa itu, hasil bisa berubah antar versi pustaka. Aturan pemilihan harus tertulis jelas, misalnya catatan dengan tanggal pembaruan terbaru menang, sehingga orang lain dapat mengulang dan membenarkan hasilnya."),
        C(
            P("""
b = df.assign(nama=df['nama'].str.strip().str.lower())
s = b.sort_values('nilai', ascending=False, kind='stable')
print(s['id'].tolist())
print(s.drop_duplicates('nama')['id'].tolist())
print(b.sort_values('id', ascending=False).drop_duplicates('nama')['id'].tolist())
print(b.sort_values('id').drop_duplicates('nama', keep='last')['id'].tolist())
print(len(s.drop_duplicates('nama')))
"""),
            ind("""
[4, 7, 1, 2, 3, 5, 6]
[4, 1, 3, 6]
[7, 6, 5, 2]
[2, 5, 6, 7]
4
"""),
            "Urutan menentukan baris mana yang menang. Menurut nilai tertinggi yang menang adalah id 4, 1, 3, dan 6, sedangkan menurut id terbaru yang menang adalah id 7, 6, 5, dan 2.",
            filename="versi_terbaik.py",
        ),
        tb("Konflik di dalam kelompok", "Konflik terjadi ketika duplikat menurut kunci memiliki nilai berbeda pada kolom lain. Misalnya dua catatan Ani dengan nilai 80 dan 75. Mendeteksinya mudah: kelompokkan menurut kunci lalu hitung `nunique` kolom nilai, dan ambil kelompok dengan hasil lebih dari satu. Konflik adalah sinyal penting. Ia bisa berarti salah ketik, pembaruan data, atau dua entitas berbeda yang kuncinya terlalu longgar. Jangan menimpa konflik secara diam-diam. Tampilkan, tinjau, lalu putuskan aturan penyelesaian yang dapat dibenarkan, dan catat jumlah konflik dalam laporan."),
        C(
            P("""
d2 = df.assign(nilai=[80, 75, 70, 90, 70, 60, 90])
b = d2.assign(nama=d2['nama'].str.strip().str.lower())
n = b.groupby('nama')['nilai'].nunique()
print(n.to_dict(), sorted(n[n > 1].index.tolist()))
print(b.groupby('nama')['nilai'].agg(['min', 'max']).loc['ani putri'].tolist())
k = df.assign(kota=df['kota'].str.strip().str.lower()).groupby('kota')['nilai'].nunique()
print(k.to_dict(), sorted(k[k > 1].index.tolist()))
print(len(df), len(df.assign(nama=df['nama'].str.strip().str.lower()).drop_duplicates(['nama', 'kota'])))
"""),
            ind("""
{'ani putri': 2, 'budi': 1, 'cici': 1, 'dedi': 1} ['ani putri']
[75, 80]
{'bandung': 2, 'jakarta': 1, 'jkt': 1, 'surabaya': 1} ['bandung']
7 6
"""),
            "Hanya Ani yang memiliki dua nilai berbeda setelah nilai kedua diubah. Pada kunci kota, bandung memiliki dua nilai berbeda karena kotanya dipakai banyak orang.",
            filename="konflik.py",
        ),
        tb("Kunci terlalu longgar", "Konflik kadang bukan kesalahan data melainkan kunci yang terlalu longgar. Pada contoh terakhir, kota bukan kunci yang baik karena banyak orang tinggal di kota yang sama, sehingga nilai berbeda di dalam kelompok adalah hal biasa. Kunci yang baik cukup spesifik untuk membedakan entitas tetapi cukup longgar untuk menangkap penulisan berbeda dari entitas sama. Kombinasi nama, tanggal lahir, dan kota biasanya lebih tepat daripada nama saja. Uji kunci Anda dengan memeriksa beberapa kelompok duplikat secara manual: apakah anggotanya benar orang yang sama atau dua orang berbeda."),
        tb("Laporan deduplikasi", "Setiap deduplikasi sebaiknya menghasilkan laporan singkat: jumlah baris sebelum dan sesudah, jumlah yang dibuang, kunci yang dipakai, aturan memilih baris, dan jumlah konflik. Laporan ini memberi pembaca gambaran seberapa besar intervensi Anda, dan memungkinkan audit bila angka akhir dipertanyakan. Bila jumlah yang dibuang sangat besar, misalnya lebih dari sepuluh persen, itu patut dicurigai sebagai masalah sumber data atau kunci yang salah, bukan sekadar pembersihan rutin. Simpan laporan bersama data bersih di berkas terpisah agar jejaknya tidak hilang."),
        tb("Jangan menghapus data asli", "Prinsip penting: jangan menimpa data mentah. Simpan salinan asli, dan hasilkan data bersih sebagai berkas atau tabel terpisah. Bila ternyata aturan deduplikasi keliru, Anda dapat mengulang dari data asli. Bila perlu, simpan juga tabel baris yang dibuang beserta alasannya sehingga keputusan dapat ditinjau. Pendekatan ini sejalan dengan prinsip reproduksibilitas dalam alur kerja data: setiap langkah pembersihan adalah fungsi dari data mentah menuju data bersih, dan dapat dijalankan ulang kapan saja dengan hasil yang sama."),
        tb("Ringkasan modul", "Anda telah mempelajari cara mendeteksi duplikat persis dan duplikat kunci, menormalkan teks untuk menangkap duplikat tersembunyi, menyeragamkan kategori dengan peta penggantian dan pencocokan mirip, serta menyelesaikan kelompok duplikat dengan membuang, menggabung, atau memilih versi terbaik sambil melaporkan konflik. Pesan utamanya: tentukan kunci dengan sadar, jangan mengubah data diam-diam, dan dokumentasikan setiap keputusan. Modul berikutnya membahas pencilan."),
        K("tip", "Buat laporan singkat setiap kali menghapus duplikat: baris sebelum, sesudah, dibuang, kunci, dan konflik. Angka dibuang yang terlalu besar adalah tanda bahaya.", title="Laporan jejak"),
        tb("Menyimpan jejak keputusan", "Tulis keputusan deduplikasi sebagai fungsi yang menerima data mentah dan mengembalikan data bersih beserta laporan. Fungsi seperti ini dapat diuji dengan data kecil seperti tabel dalam pelajaran ini, dijalankan ulang ketika data baru tiba, dan ditinjau oleh rekan. Hindari langkah manual yang tidak tercatat, misalnya menghapus baris lewat spreadsheet, karena tidak dapat diulang. Bila terpaksa ada keputusan manual, simpan daftar id yang dibuang dalam berkas dengan alasannya. Dengan cara ini keputusan Anda dapat dipertanggungjawabkan berbulan-bulan kemudian ketika seseorang bertanya mengapa angka tidak sama."),
        tb("Menguji aturan dengan contoh kecil", "Sebelum menjalankan aturan deduplikasi pada jutaan baris, ujilah pada tabel kecil yang jawabannya sudah Anda ketahui. Buat contoh berisi pasangan duplikat, duplikat dengan konflik, dan pasangan yang mirip tetapi sebenarnya berbeda orang. Pastikan fungsi Anda membuang yang seharusnya dan mempertahankan yang seharusnya. Uji semacam ini menangkap kesalahan seperti kunci yang terlalu longgar atau urutan pengurutan yang salah. Tabel contoh juga menjadi dokumentasi hidup tentang perilaku yang Anda inginkan, dan berguna sebagai uji otomatis ketika aturan diubah di kemudian hari."),
        tb("Peran pemilik data", "Banyak keputusan deduplikasi tidak dapat diambil sendiri oleh analis. Apakah dua catatan dengan nama sama tetapi tanggal lahir berbeda adalah satu orang? Catatan mana yang dianggap resmi? Pemilik data atau pemangku kepentingan bisnis memegang jawabannya. Siapkan contoh konkret kasus ambigu, ajukan beberapa aturan beserta dampaknya terhadap angka, lalu minta mereka memilih. Keputusan yang disetujui bersama mengurangi sengketa nanti dan membuat laporan Anda lebih dipercaya karena aturan berasal dari pihak yang paham konteks."),
        E(
            "B3-03-3-ex1",
            "mudah",
            "Tulis fungsi `gabung_per_nama(df)` yang menormalkan `nama` (strip dan lower) lalu mengembalikan dict `{nama: (jumlah_baris, rata_rata_nilai)}` dengan jumlah bilangan bulat dan rata-rata float.",
            ind("""
import pandas as pd

def gabung_per_nama(df):
    # TODO: implementasikan
    pass
"""),
            P("""
r = gabung_per_nama(df)
assert r['ani putri'] == (2, 80.0)
assert r['dedi'] == (1, 60.0)
assert r['cici'] == (2, 90.0)
assert sorted(r) == ['ani putri', 'budi', 'cici', 'dedi']
"""),
            "groupby nama dengan agg size dan mean lalu bentuk dict tuple.",
            X(H11),
        ),
        E(
            "B3-03-3-ex2",
            "sedang",
            "Tulis fungsi `simpan_tertinggi(df)` yang menormalkan `nama`, mengurutkan menurun menurut `nilai` secara stabil, dan mengembalikan list `id` setelah hanya satu baris per nama dipertahankan.",
            ind("""
import pandas as pd

def simpan_tertinggi(df):
    # TODO: implementasikan
    pass
"""),
            P("""
assert simpan_tertinggi(df) == [4, 1, 3, 6]
assert simpan_tertinggi(df.iloc[[0, 1]]) == [1]
assert len(simpan_tertinggi(df)) == 4
assert simpan_tertinggi(df.iloc[[2, 4]]) == [3]
"""),
            "sort_values stabil menurun lalu drop_duplicates pada nama.",
            X(H12),
        ),
        E(
            "B3-03-3-ex3",
            "sedang",
            "Tulis fungsi `konflik_kunci(df, kunci, nilai)` yang menormalkan kolom `kunci` lalu mengembalikan list terurut kunci yang memiliki lebih dari satu nilai berbeda pada kolom `nilai`.",
            ind("""
import pandas as pd

def konflik_kunci(df, kunci, nilai):
    # TODO: implementasikan
    pass
"""),
            P("""
assert konflik_kunci(df, 'nama', 'nilai') == []
assert konflik_kunci(df.assign(nilai=[80, 75, 70, 90, 70, 60, 90]), 'nama', 'nilai') == ['ani putri']
assert konflik_kunci(df, 'kota', 'nilai') == ['bandung']
assert konflik_kunci(df.iloc[[0, 1]], 'kota', 'nilai') == []
"""),
            "groupby kunci ternormalisasi, nunique, lalu saring lebih dari satu.",
            X(H13),
        ),
        E(
            "B3-03-3-ex4",
            "menantang",
            "Tulis fungsi `laporan_dedup(df, subset)` yang menormalkan kolom `subset` pada salinan, menghapus duplikat menurut `subset`, dan mengembalikan dict dengan kunci `sebelum`, `sesudah`, dan `dibuang` berisi bilangan bulat.",
            ind("""
import pandas as pd

def laporan_dedup(df, subset):
    # TODO: implementasikan
    pass
"""),
            P("""
assert laporan_dedup(df, ['nama', 'kota']) == {'sebelum': 7, 'sesudah': 5, 'dibuang': 2}
assert laporan_dedup(df, ['nama']) == {'sebelum': 7, 'sesudah': 4, 'dibuang': 3}
assert laporan_dedup(df, ['kota'])['sesudah'] == 4
assert df['nama'].tolist()[1] == 'ani putri '
"""),
            "Normalkan salinan, drop_duplicates, lalu hitung selisih panjang.",
            X(H14),
        ),
    ],
    [
        M("Membuang duplikat tanpa memeriksa konflik nilai.", "Hitung nunique per kunci dan tinjau konflik."),
        M("Memakai kunci terlalu longgar seperti kota.", "Gabungkan beberapa kolom agar kunci spesifik."),
        M("Menimpa data mentah dengan hasil bersih.", "Simpan data mentah dan hasil bersih terpisah."),
    ],
    [
        Q("Bila duplikat memuat info berbeda, strategi yang cocok?", ["Gabung", "Hapus semua", "Abaikan", "Ubah tipe"], 0, "Agregasi.", hint="Satukan."),
        Q("sort_values stabil memakai?", ["kind='stable'", "inplace", "axis", "na_position"], 0, "Deterministik.", hint="stable."),
        Q("Konflik dideteksi dengan?", ["nunique per kunci", "shape", "head", "dtypes"], 0, "Lebih dari satu.", hint="Nunique."),
        Q("Jumlah dibuang sangat besar menandakan?", ["Kemungkinan masalah kunci atau sumber", "Hasil bagus", "Tidak apa", "Format salah"], 0, "Curigai.", hint="Tanda bahaya."),
        Q("Data mentah sebaiknya?", ["Disimpan tanpa diubah", "Ditimpa", "Dihapus", "Dikompres"], 0, "Reproduksibilitas.", hint="Aman."),
    ],
    [
        "Pilih strategi buang, gabung, atau versi terbaik sesuai isi duplikat.",
        "Konflik nilai dalam kelompok harus dideteksi dan dilaporkan.",
        "Kunci yang baik spesifik namun toleran terhadap ejaan.",
        "Laporan deduplikasi dan data mentah yang utuh menjaga keterauditan.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perintah yang cukup jelas dalam teks.", "brief": []}

write_module(
    "B3",
    3,
    "Duplikat dan inkonsistensi",
    105,
    [
        "Mendeteksi duplikat persis, duplikat kunci, dan duplikat tersembunyi",
        "Menyeragamkan kategori dan ejaan dengan peta dan pencocokan mirip",
        "Menyelesaikan duplikat dengan strategi yang dapat diaudit",
    ],
    [l1, l2, l3],
    video,
    REF,
)
