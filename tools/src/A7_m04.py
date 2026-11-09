import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

ACAK_FN = """
import random

def acak_terkontrol(seed, n):
    rng = random.Random(seed)
    return [rng.randint(0, 100) for _ in range(n)]
"""

BAGI_FN = """
import random

def bagi_data(data, rasio, seed):
    salinan = list(data)
    random.Random(seed).shuffle(salinan)
    batas = int(len(salinan) * rasio)
    return (salinan[:batas], salinan[batas:])
"""

SIDIK_FN = """
import hashlib
import json

def sidik_jari(obj):
    teks = json.dumps(obj, sort_keys=True)
    return hashlib.sha256(teks.encode('utf-8')).hexdigest()
"""

STABIL_FN = """
import math

def jumlah_stabil(angka):
    return math.fsum(angka)
"""

l1 = lesson(
    "A7-04-1",
    "Mengapa hasil harus bisa diulang",
    35,
    [
        "Menjelaskan reproduksibilitas dan perbedaannya dengan replikasi",
        "Mengendalikan keacakan dengan seed",
        "Membagi data secara deterministik",
        "Membuat sidik jari hasil dan memahami pengaruh urutan perhitungan desimal",
    ],
    [
        T("""
        ## Angka yang tidak bisa dijelaskan

        Bayangkan atasan bertanya bagaimana angka 12,4 persen di laporan bulan lalu dihitung, dan Anda tidak bisa menghasilkannya lagi. Skrip sudah berubah, data sudah diperbarui, dan model dilatih dengan pengacakan yang berbeda. Situasi seperti ini sangat umum, dan merusak kepercayaan pada analisis.

        **Reproduksibilitas** berarti orang lain, atau diri Anda enam bulan kemudian, dapat menjalankan ulang analisis dengan kode dan data yang sama dan mendapat hasil yang sama.
        """),
        T("""
        ## Reproduksi dan replikasi

        Dua istilah ini sering tertukar. **Reproduksi** memakai kode dan data yang sama untuk mendapat hasil yang sama, sehingga terutama soal ketelitian teknis. **Replikasi** mengumpulkan data baru dengan metode serupa untuk melihat apakah kesimpulannya bertahan, sehingga soal kebenaran ilmiahnya.

        Reproduksi adalah syarat minimum. Bila analisis tidak dapat direproduksi, kita bahkan tidak bisa mulai menilai apakah temuannya bisa direplikasi.
        """),
        T("""
        ## Empat sumber ketidakpastian

        Hasil yang berubah hampir selalu berasal dari empat hal. **Kode** berubah tanpa tercatat. **Data** berubah atau diperbarui diam-diam. **Lingkungan**, yaitu versi bahasa dan pustaka, berbeda antar mesin. Dan **keacakan** yang tidak dikendalikan menghasilkan angka berbeda tiap dijalankan.

        Pelajaran ini membahas keacakan dan sidik jari hasil. Pelajaran berikutnya membahas lingkungan dan data, dan pelajaran terakhir membahas urutan langkah dan pencatatan.
        """),
        T("""
        ## Mengendalikan keacakan dengan seed

        Pembangkit bilangan acak komputer sebenarnya deterministik: ia menghasilkan deret yang tampak acak dari nilai awal yang disebut **seed**. Seed yang sama menghasilkan deret yang sama persis. Karena itu pengacakan, seperti pembagian data latih dan uji atau inisialisasi model, dapat diulang dengan menetapkan seed.

        Gunakan objek `random.Random(seed)` terpisah alih-alih pembangkit global. Dengan begitu bagian kode lain yang juga memakai pengacakan tidak mengubah deret yang kita harapkan.
        """),
        C(
            """
            import random

            def acak_terkontrol(seed, n):
                rng = random.Random(seed)
                return [rng.randint(0, 100) for _ in range(n)]

            print(acak_terkontrol(1, 5))
            print(acak_terkontrol(1, 5))
            print(acak_terkontrol(2, 5))
            print(acak_terkontrol(1, 5) == acak_terkontrol(1, 5))
            """,
            """
            [17, 72, 97, 8, 32]
            [17, 72, 97, 8, 32]
            [7, 11, 10, 46, 21]
            True
            """,
            """
            Seed yang sama menghasilkan deret yang sama persis, sedangkan seed berbeda menghasilkan deret berbeda.
            """,
            filename="seed_acak.py",
        ),
        T("""
        ## Pembagian data yang bisa diulang

        Membagi data menjadi bagian latih dan uji adalah langkah acak yang sangat sering dilakukan. Bila pembagiannya berubah tiap dijalankan, metrik model ikut berubah dan perbandingan antar eksperimen menjadi tidak adil. Tetapkan seed, acak salinan data, lalu potong pada rasio yang ditentukan.

        Perhatikan bahwa kita mengacak salinan, bukan data aslinya. Fungsi yang mengubah argumennya diam-diam adalah sumber bug yang sulit dilacak.
        """),
        C(
            """
            import random

            def bagi_data(data, rasio, seed):
                salinan = list(data)
                random.Random(seed).shuffle(salinan)
                batas = int(len(salinan) * rasio)
                return (salinan[:batas], salinan[batas:])

            data = list(range(10))
            latih, uji = bagi_data(data, 0.7, 7)
            print(latih)
            print(uji)
            print(data)
            print(bagi_data(data, 0.7, 7) == (latih, uji))
            """,
            """
            [8, 3, 1, 4, 7, 0, 9]
            [6, 2, 5]
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            True
            """,
            """
            Pembagian dengan seed tetap selalu sama, dan data asli tidak berubah urutannya.
            """,
            filename="bagi_data.py",
        ),
        T("""
        ## Sidik jari hasil

        Untuk membuktikan dua hasil identik, bandingkan **sidik jari**-nya, yaitu hash dari isi hasil. Ubah hasil menjadi teks yang kanonik, misalnya JSON dengan kunci terurut, lalu hitung SHA-256. Dua hasil yang sama selalu menghasilkan sidik jari sama, dan perbedaan sekecil apa pun mengubahnya total.

        Mengurutkan kunci penting: dua dict dengan isi sama tetapi urutan sisip berbeda harus punya sidik jari sama.
        """),
        C(
            """
            import hashlib
            import json

            def sidik_jari(obj):
                teks = json.dumps(obj, sort_keys=True)
                return hashlib.sha256(teks.encode('utf-8')).hexdigest()

            a = {'rata': 12.4, 'n': 100}
            b = {'n': 100, 'rata': 12.4}
            c = {'n': 100, 'rata': 12.5}
            print(sidik_jari(a) == sidik_jari(b))
            print(sidik_jari(a) == sidik_jari(c))
            print(len(sidik_jari(a)))
            """,
            """
            True
            False
            64
            """,
            """
            Urutan kunci tidak memengaruhi sidik jari, tetapi nilai berbeda mengubahnya. Panjangnya selalu enam puluh empat karakter.
            """,
            filename="sidik_jari.py",
        ),
        T("""
        ## Urutan perhitungan desimal

        Bahkan tanpa keacakan, hasil dapat berubah halus karena aritmetika desimal tidak asosiatif: `(a + b) + c` tidak selalu sama dengan `a + (b + c)`. Bila jumlah dihitung dari data yang urutannya berubah, misalnya hasil kueri tanpa `ORDER BY` atau pemrosesan paralel, angka terakhir bisa berbeda.

        Untuk menjumlahkan dengan stabil, gunakan `math.fsum`, yang melacak galat pembulatan sehingga hasilnya tidak bergantung pada urutan. Alternatifnya, urutkan data sebelum menjumlahkan.
        """),
        C(
            """
            import math

            def naif(angka):
                total = 0.0
                for x in angka:
                    total += x
                return total

            a = [1e16, 1.0, -1e16]
            b = [1e16, -1e16, 1.0]
            print(naif(a), naif(b))
            print(math.fsum(a), math.fsum(b))
            """,
            """
            0.0 1.0
            1.0 1.0
            """,
            """
            Penjumlahan berurutan memberi hasil berbeda tergantung urutan data, sedangkan fsum selalu memberi jawaban benar yang sama.
            """,
            filename="urutan_desimal.py",
        ),
        T("""
        ## Tingkat reproduksibilitas

        Reproduksibilitas bukan semua atau tidak sama sekali. Tingkat terendah: kode ada tetapi tidak jelas cara menjalankannya. Tingkat menengah: ada instruksi, versi pustaka dicatat, dan data dapat diverifikasi. Tingkat tinggi: seluruh analisis dapat dijalankan dengan satu perintah di mesin bersih dan menghasilkan sidik jari yang sama.

        Mulailah dari yang mudah dan naikkan bertahap. Seed, version control, dan catatan versi pustaka sudah memberi lompatan besar dengan usaha kecil.
        """),
        T("""
        ## Biaya tidak mengulang

        Analisis yang tidak dapat diulang mahal. Kesalahan tidak dapat dilacak, perbaikan tidak dapat diverifikasi, dan setiap pertanyaan lanjutan berarti memulai dari nol. Di dunia kerja, pemeriksa dan auditor sering meminta bukti bagaimana angka dihasilkan, dan di dunia akademik, jurnal makin mewajibkan kode dan data dibagikan.

        Menginvestasikan sedikit waktu di awal untuk kebiasaan reproduksibel menghemat banyak waktu di akhir.
        """),
        K(
            "tip",
            """
            Tetapkan seed pada setiap langkah acak, ubah hasil penting menjadi sidik jari, dan catat keduanya bersama hasilnya.
            """,
            title="Kebiasaan dasar",
        ),
        E(
            "A7-04-1-ex1",
            "mudah",
            """
            Tulis fungsi `acak_terkontrol(seed, n)` yang mengembalikan list `n` bilangan bulat acak antara 0 dan 100 (inklusif) memakai objek `random.Random(seed)`, sehingga seed sama selalu menghasilkan list sama.
            """,
            """
            import random

            def acak_terkontrol(seed, n):
                # TODO: implementasikan
                pass
            """,
            """
            a = acak_terkontrol(1, 5)
            assert len(a) == 5 and all(isinstance(x, int) and 0 <= x <= 100 for x in a)
            assert a == acak_terkontrol(1, 5)
            assert a != acak_terkontrol(2, 5)
            assert acak_terkontrol(3, 0) == []
            """,
            "Buat random.Random(seed) lokal lalu panggil randint sebanyak n.",
            ACAK_FN.strip("\n"),
        ),
        E(
            "A7-04-1-ex2",
            "sedang",
            """
            Tulis fungsi `bagi_data(data, rasio, seed)` yang mengacak salinan `data` dengan `random.Random(seed).shuffle`, lalu mengembalikan tuple `(latih, uji)` dengan `latih` berisi `int(len * rasio)` elemen pertama. Data asli tidak boleh berubah.
            """,
            """
            import random

            def bagi_data(data, rasio, seed):
                # TODO: implementasikan
                pass
            """,
            """
            data = list(range(10))
            latih, uji = bagi_data(data, 0.7, 7)
            assert len(latih) == 7 and len(uji) == 3
            assert sorted(latih + uji) == list(range(10))
            assert data == list(range(10))
            assert bagi_data(data, 0.7, 7) == (latih, uji)
            assert bagi_data(data, 0.7, 8) != (latih, uji)
            """,
            "Salin list, acak dengan Random(seed), lalu potong pada batas.",
            BAGI_FN.strip("\n"),
        ),
        E(
            "A7-04-1-ex3",
            "sedang",
            """
            Tulis fungsi `sidik_jari(obj)` yang mengembalikan SHA-256 heksadesimal dari `json.dumps(obj, sort_keys=True)` yang di-encode UTF-8.
            """,
            """
            import hashlib
            import json

            def sidik_jari(obj):
                # TODO: implementasikan
                pass
            """,
            """
            a = {'rata': 12.4, 'n': 100}
            b = {'n': 100, 'rata': 12.4}
            c = {'n': 100, 'rata': 12.5}
            assert len(sidik_jari(a)) == 64
            assert sidik_jari(a) == sidik_jari(b)
            assert sidik_jari(a) != sidik_jari(c)
            assert sidik_jari([1, 2]) != sidik_jari([2, 1])
            """,
            "Serialisasi dengan kunci terurut lalu hash.",
            SIDIK_FN.strip("\n"),
        ),
        E(
            "A7-04-1-ex4",
            "menantang",
            """
            Tulis fungsi `jumlah_stabil(angka)` yang menjumlahkan list bilangan desimal sehingga hasilnya tidak bergantung pada urutan elemen, memakai `math.fsum`.
            """,
            """
            import math

            def jumlah_stabil(angka):
                # TODO: implementasikan
                pass
            """,
            """
            assert jumlah_stabil([1e16, 1.0, -1e16]) == 1.0
            assert jumlah_stabil([1e16, -1e16, 1.0]) == 1.0
            assert jumlah_stabil([0.1] * 10) == 1.0
            assert jumlah_stabil([]) == 0.0
            """,
            "Gunakan math.fsum alih-alih perulangan penjumlahan biasa.",
            STABIL_FN.strip("\n"),
        ),
    ],
    [
        M("Memakai pembangkit acak global tanpa seed.", "Gunakan random.Random(seed) lokal."),
        M("Mengacak data asli di tempat.", "Acak salinan agar data asli tidak berubah."),
        M("Menyimpulkan hasil sama hanya karena mirip.", "Bandingkan sidik jari hasilnya."),
    ],
    [
        Q("Reproduksibilitas berarti?", ["Kode dan data sama memberi hasil sama", "Data baru memberi kesimpulan sama", "Kode lebih cepat", "Laporan lebih panjang"], 0, "Mengulang dengan bahan sama.", hint="Ulang."),
        Q("Seed berfungsi?", ["Menetapkan deret acak yang bisa diulang", "Mempercepat kode", "Mengurutkan data", "Menyimpan hasil"], 0, "Nilai awal pembangkit.", hint="Awal."),
        Q("Sidik jari hasil dibuat dengan?", ["Hash dari bentuk kanonik hasil", "Menyalin hasil", "Menghitung panjang", "Menghapus hasil"], 0, "SHA-256 atas JSON terurut.", hint="Hash."),
        Q("Penjumlahan desimal stabil memakai?", ["math.fsum", "sum biasa dengan urutan acak", "round", "int"], 0, "Tidak bergantung urutan.", hint="fsum."),
        Q("Replikasi berbeda dari reproduksi karena?", ["Memakai data baru", "Memakai kode lebih baru", "Lebih cepat", "Tanpa seed"], 0, "Menguji kebenaran ilmiah.", hint="Data baru."),
    ],
    [
        "Reproduksibilitas adalah mengulang analisis dengan kode dan data sama dan mendapat hasil sama.",
        "Seed tetap dan pembagian data deterministik membuat keacakan bisa diulang.",
        "Sidik jari hasil membuktikan dua hasil identik.",
        "Urutan perhitungan desimal dapat mengubah hasil, jadi gunakan penjumlahan stabil.",
    ],
    [],
)

REQ_FN = """
def parse_requirements(teks):
    hasil = {}
    for baris in teks.splitlines():
        b = baris.strip()
        if not b or b.startswith('#') or '==' not in b:
            continue
        nama, versi = b.split('==', 1)
        hasil[nama.strip().lower()] = versi.strip()
    return hasil
"""

PIN_FN = """
def belum_dipin(teks):
    hasil = []
    for baris in teks.splitlines():
        b = baris.strip()
        if not b or b.startswith('#') or '==' in b:
            continue
        hasil.append(b.lower())
    return sorted(hasil)
"""

VERIF_FN = """
import hashlib

def verifikasi_data(isi, harapan):
    return hashlib.sha256(isi.encode('utf-8')).hexdigest() == harapan
"""

STRUK_FN = """
def cek_struktur(daftar_path, wajib):
    hilang = []
    for nama in wajib:
        if not any(p.startswith(nama + '/') for p in daftar_path):
            hilang.append(nama)
    return sorted(hilang)
"""

REQ_TEXT = """
# lingkungan analisis
Pandas==2.2.1
numpy==1.26.4
scikit-learn
matplotlib==3.8.3
"""

l2 = lesson(
    "A7-04-2",
    "Struktur proyek, lingkungan, dan data",
    35,
    [
        "Menyusun struktur folder proyek analisis yang konsisten",
        "Mencatat dan mengunci versi pustaka dalam requirements",
        "Memverifikasi data dengan checksum",
        "Memisahkan konfigurasi dari kode",
    ],
    [
        T("""
        ## Proyek yang bisa dipahami orang lain

        Orang yang membuka proyek Anda untuk pertama kali, termasuk Anda sendiri setahun kemudian, harus segera tahu di mana data, di mana kode, dan bagaimana menjalankannya. Struktur folder yang konsisten menjawab pertanyaan itu tanpa penjelasan panjang.

        Tidak ada struktur tunggal yang benar, tetapi pola yang umum memisahkan data mentah, kode, notebook eksplorasi, dan laporan hasil. Yang penting adalah konsistensi antar proyek.
        """),
        T("""
        ## Tata letak yang umum

        ```text
        proyek/
          README.md
          requirements.txt
          .gitignore
          data/
            raw/
            processed/
          src/
          notebooks/
          reports/
        ```

        Folder `data/raw` berisi data asli yang tidak pernah diubah. `data/processed` berisi hasil pembersihan yang dapat dibuat ulang dari data mentah dan kode. `src` berisi fungsi yang dipakai ulang, `notebooks` berisi eksplorasi, dan `reports` berisi keluaran akhir.
        """),
        T("""
        ## Data mentah itu suci

        Aturan paling penting: jangan pernah mengubah data mentah. Semua pembersihan dilakukan oleh kode yang membaca data mentah dan menulis hasil ke folder lain. Dengan begitu kita selalu dapat mengulang dari awal, dan orang lain dapat memeriksa setiap keputusan pembersihan yang kita ambil.

        Bila data mentah diedit manual, tidak ada jejak apa yang berubah, dan reproduksibilitas hilang seketika.
        """),
        C(
            """
            def cek_struktur(daftar_path, wajib):
                hilang = []
                for nama in wajib:
                    if not any(p.startswith(nama + '/') for p in daftar_path):
                        hilang.append(nama)
                return sorted(hilang)

            paths = ['data/raw/a.csv', 'src/bersih.py', 'README.md', 'notebooks/eda.ipynb']
            print(cek_struktur(paths, ['data', 'src', 'notebooks', 'reports']))
            print(cek_struktur(paths + ['reports/laporan.md'], ['data', 'src', 'notebooks', 'reports']))
            """,
            """
            ['reports']
            []
            """,
            """
            Pemeriksaan sederhana menemukan folder wajib yang belum berisi apa pun.
            """,
            filename="cek_struktur.py",
        ),
        T("""
        ## Mengunci versi pustaka

        Kode yang berjalan hari ini bisa rusak bulan depan karena pustaka diperbarui dan perilakunya berubah. Solusinya mencatat versi persis yang dipakai dalam file `requirements.txt`, dengan format `paket==versi`. Perintah `pip freeze > requirements.txt` menghasilkannya dari lingkungan aktif, dan `pip install -r requirements.txt` memulihkannya.

        Mengunci versi dengan `==` membuat lingkungan identik di semua mesin. Paket yang ditulis tanpa versi akan mengambil yang terbaru saat itu, dan itulah sumber ketidakpastian.
        """),
        C(
            """
            def parse_requirements(teks):
                hasil = {}
                for baris in teks.splitlines():
                    b = baris.strip()
                    if not b or b.startswith('#') or '==' not in b:
                        continue
                    nama, versi = b.split('==', 1)
                    hasil[nama.strip().lower()] = versi.strip()
                return hasil

            def belum_dipin(teks):
                hasil = []
                for baris in teks.splitlines():
                    b = baris.strip()
                    if not b or b.startswith('#') or '==' in b:
                        continue
                    hasil.append(b.lower())
                return sorted(hasil)

            teks = '# lingkungan\\nPandas==2.2.1\\nnumpy==1.26.4\\nscikit-learn\\nmatplotlib==3.8.3'
            print(parse_requirements(teks))
            print(belum_dipin(teks))
            """,
            """
            {'pandas': '2.2.1', 'numpy': '1.26.4', 'matplotlib': '3.8.3'}
            ['scikit-learn']
            """,
            """
            Tiga paket terkunci pada versi tertentu, sedangkan scikit-learn belum dipin sehingga menjadi sumber risiko.
            """,
            filename="requirements.py",
        ),
        T("""
        ## Lingkungan virtual

        Setiap proyek sebaiknya punya **lingkungan virtual** sendiri agar pustakanya tidak bercampur dengan proyek lain. Perintah `python -m venv .venv` membuat satu, dan mengaktifkannya membuat `pip` memasang paket hanya di sana. Pengguna conda memakai `environment.yml` untuk tujuan yang sama.

        Folder `.venv` tidak dimasukkan ke version control karena besar dan bergantung mesin. Yang disimpan adalah `requirements.txt`, resep untuk membuatnya kembali.
        """),
        T("""
        ## Checksum data

        Bagaimana kita tahu data yang dipakai hari ini sama dengan yang dipakai saat analisis dibuat? Hitung **checksum**, yaitu hash isi file, dan simpan di repositori. Sebelum analisis berjalan, hitung ulang dan bandingkan. Bila berbeda, data telah berubah dan hasilnya tidak boleh dipercaya begitu saja.

        Untuk data besar yang tidak masuk repositori, checksum adalah bukti ringan bahwa versi yang tepat sedang dipakai.
        """),
        C(
            """
            import hashlib

            def verifikasi_data(isi, harapan):
                return hashlib.sha256(isi.encode('utf-8')).hexdigest() == harapan

            isi = 'id,nilai\\n1,10\\n2,20\\n'
            harapan = hashlib.sha256(isi.encode('utf-8')).hexdigest()
            print(verifikasi_data(isi, harapan))
            print(verifikasi_data(isi + '3,30\\n', harapan))
            print(len(harapan))
            """,
            """
            True
            False
            64
            """,
            """
            Data yang sama lolos verifikasi, dan menambah satu baris saja membuat checksum tidak cocok.
            """,
            filename="verifikasi_data.py",
        ),
        T("""
        ## Memisahkan konfigurasi dari kode

        Nilai seperti seed, rasio pembagian data, ambang batas, dan lokasi file sebaiknya tidak tertanam di tengah kode. Kumpulkan dalam satu tempat, misalnya dict konfigurasi atau file JSON, dan baca dari sana. Mengubah eksperimen cukup dengan mengubah konfigurasi, dan konfigurasi itu sendiri dapat dicatat bersama hasil.

        Rahasia seperti kata sandi dan token tidak boleh masuk konfigurasi yang dicommit. Simpan di variabel lingkungan atau file yang masuk `.gitignore`.
        """),
        T("""
        ## README sebagai pintu masuk

        File README adalah halaman pertama proyek. Isinya singkat: tujuan proyek, cara memasang lingkungan, cara menjalankan analisis, dan asal data. Dengan README yang baik, rekan baru dapat menjalankan proyek dalam hitungan menit tanpa bertanya.

        Uji README dengan cara sederhana: minta seseorang yang belum pernah melihat proyek mengikutinya dari awal. Setiap pertanyaan yang muncul menunjukkan bagian yang perlu diperjelas.
        """),
        K(
            "warn",
            """
            Jangan mengubah data mentah dan jangan mencommit rahasia. Data mentah dibaca saja, hasil olahan ditulis ke folder lain.
            """,
            title="Dua larangan",
        ),
        T("""
        ## Contoh isi README singkat

        Tulis judul proyek, satu paragraf tujuan, daftar langkah pemasangan seperti membuat lingkungan virtual dan menjalankan pip install, perintah untuk menjalankan analisis, serta sumber dan tanggal pengambilan data. Cantumkan juga siapa yang dapat dihubungi bila ada masalah. Dokumen sependek ini sudah cukup berguna dan jauh lebih baik daripada tidak ada sama sekali.
        """),
        T("""
        ## Nama file yang jelas

        Beri nama file dengan pola yang konsisten, misalnya awalan angka untuk urutan eksekusi seperti 01_ambil.py dan 02_bersih.py. Hindari nama seperti final_revisi_baru2. Nama yang jelas membuat urutan kerja terbaca dari daftar folder saja, dan riwayat version control mencatat perubahan sehingga versi lama tidak perlu ditumpuk dalam nama file.
        """),
        E(
            "A7-04-2-ex1",
            "mudah",
            """
            Tulis fungsi `parse_requirements(teks)` yang mengembalikan dict `{nama_paket: versi}` dari baris berformat `paket==versi`. Abaikan baris kosong, baris komentar berawalan `#`, dan baris tanpa `==`. Nama paket diubah ke huruf kecil dan spasi di tepi dibuang.
            """,
            """
            def parse_requirements(teks):
                # TODO: implementasikan
                pass
            """,
            """
            t = '# x\\nPandas==2.2.1\\n\\nnumpy == 1.26.4\\nscikit-learn\\n'
            assert parse_requirements(t) == {'pandas': '2.2.1', 'numpy': '1.26.4'}
            assert parse_requirements('') == {}
            assert parse_requirements('# saja') == {}
            assert parse_requirements('A==1\\nB==2') == {'a': '1', 'b': '2'}
            """,
            "Pisahkan setiap baris valid pada tanda sama dengan ganda.",
            REQ_FN.strip("\n"),
        ),
        E(
            "A7-04-2-ex2",
            "sedang",
            """
            Tulis fungsi `belum_dipin(teks)` yang mengembalikan list terurut nama paket (huruf kecil) pada baris yang tidak memuat `==`, dengan mengabaikan baris kosong dan komentar berawalan `#`.
            """,
            """
            def belum_dipin(teks):
                # TODO: implementasikan
                pass
            """,
            """
            t = '# x\\nPandas==2.2.1\\nscikit-learn\\nSeaborn\\n\\n'
            assert belum_dipin(t) == ['scikit-learn', 'seaborn']
            assert belum_dipin('a==1\\nb==2') == []
            assert belum_dipin('') == []
            assert belum_dipin('Zeta\\nAlfa') == ['alfa', 'zeta']
            """,
            "Kumpulkan baris valid tanpa tanda sama dengan ganda lalu urutkan.",
            PIN_FN.strip("\n"),
        ),
        E(
            "A7-04-2-ex3",
            "sedang",
            """
            Tulis fungsi `verifikasi_data(isi, harapan)` yang mengembalikan `True` bila SHA-256 heksadesimal dari `isi` (di-encode UTF-8) sama dengan `harapan`, dan `False` bila tidak.
            """,
            """
            import hashlib

            def verifikasi_data(isi, harapan):
                # TODO: implementasikan
                pass
            """,
            """
            import hashlib

            isi = 'id,nilai\\n1,10\\n'
            h = hashlib.sha256(isi.encode('utf-8')).hexdigest()
            assert verifikasi_data(isi, h) is True
            assert verifikasi_data(isi + 'x', h) is False
            assert verifikasi_data(isi, 'salah') is False
            assert verifikasi_data('', hashlib.sha256(b'').hexdigest()) is True
            """,
            "Hitung hash isi lalu bandingkan dengan nilai harapan.",
            VERIF_FN.strip("\n"),
        ),
        E(
            "A7-04-2-ex4",
            "menantang",
            """
            Tulis fungsi `cek_struktur(daftar_path, wajib)` yang mengembalikan list terurut nama folder dalam `wajib` yang belum berisi file apa pun, yaitu tidak ada path di `daftar_path` yang berawalan nama itu diikuti `/`.
            """,
            """
            def cek_struktur(daftar_path, wajib):
                # TODO: implementasikan
                pass
            """,
            """
            p = ['data/raw/a.csv', 'src/x.py', 'README.md']
            assert cek_struktur(p, ['data', 'src', 'reports']) == ['reports']
            assert cek_struktur(p, ['data', 'src']) == []
            assert cek_struktur([], ['b', 'a']) == ['a', 'b']
            assert cek_struktur(['datax/a.csv'], ['data']) == ['data']
            """,
            "Periksa awalan nama dengan garis miring agar folder bernama mirip tidak salah cocok.",
            STRUK_FN.strip("\n"),
        ),
    ],
    [
        M("Mengubah data mentah secara manual.", "Baca saja, tulis hasil ke folder lain."),
        M("Memasang pustaka tanpa mencatat versi.", "Kunci dengan requirements.txt dan =="),
        M("Mencommit kata sandi di konfigurasi.", "Pakai variabel lingkungan atau .gitignore."),
    ],
    [
        Q("Data mentah sebaiknya?", ["Tidak pernah diubah", "Diedit sesuka hati", "Dihapus setelah dipakai", "Disimpan di notebook"], 0, "Sumber kebenaran.", hint="Suci."),
        Q("requirements.txt berfungsi?", ["Mencatat versi pustaka", "Menyimpan data", "Menjalankan kode", "Menghapus cache"], 0, "Resep lingkungan.", hint="Versi."),
        Q("Checksum data berguna untuk?", ["Memastikan data tidak berubah", "Mempercepat baca", "Mengompres data", "Mengurutkan data"], 0, "Hash isi file.", hint="Hash."),
        Q("Lingkungan virtual bertujuan?", ["Memisahkan pustaka antar proyek", "Mempercepat internet", "Menyimpan data", "Membuat grafik"], 0, "Terisolasi.", hint="Pisah."),
        Q("Yang tidak masuk version control?", ["Folder .venv dan rahasia", "Kode sumber", "README", "requirements.txt"], 0, "Besar dan sensitif.", hint="Rahasia."),
    ],
    [
        "Struktur proyek yang konsisten memudahkan pemahaman dan pengulangan.",
        "Data mentah dibaca saja dan hasil olahan ditulis ke tempat lain.",
        "Kunci versi pustaka dengan requirements.txt dan lingkungan virtual.",
        "Checksum dan konfigurasi terpisah menjaga data dan eksperimen terkendali.",
    ],
    [],
)

URUT_FN = """
def urutan_langkah(deps):
    sisa = {k: set(v) for k, v in deps.items()}
    hasil = []
    while sisa:
        siap = sorted(k for k, v in sisa.items() if not (v - set(hasil)))
        if not siap:
            raise ValueError('ada siklus')
        langkah = siap[0]
        hasil.append(langkah)
        del sisa[langkah]
    return hasil
"""

ULANG_FN = URUT_FN + """

def perlu_dijalankan(deps, diubah):
    ulang = set()
    hasil = []
    for langkah in urutan_langkah(deps):
        if langkah in diubah or any(d in ulang for d in deps[langkah]):
            ulang.add(langkah)
            hasil.append(langkah)
    return hasil
"""

CATAT_FN = """
import hashlib
import json

def catat_run(params, hash_data, versi_kode):
    isi = {'params': params, 'hash_data': hash_data, 'versi_kode': versi_kode}
    teks = json.dumps(isi, sort_keys=True)
    isi['id'] = hashlib.sha256(teks.encode('utf-8')).hexdigest()[:12]
    return isi
"""

NB_FN = """
import copy

def bersihkan_notebook(nb):
    baru = copy.deepcopy(nb)
    for sel in baru['cells']:
        if sel['cell_type'] == 'code':
            sel['outputs'] = []
            sel['execution_count'] = None
    return baru
"""

DEPS = """
deps = {
    'ambil': [],
    'bersih': ['ambil'],
    'fitur': ['bersih'],
    'model': ['fitur'],
    'laporan': ['model', 'bersih'],
}
"""

DEPS_I = textwrap.indent(DEPS.strip("\n"), " " * 12)

l3 = lesson(
    "A7-04-3",
    "Pipeline, pencatatan run, dan notebook yang bersih",
    35,
    [
        "Mengurutkan langkah analisis berdasarkan ketergantungan",
        "Menentukan langkah yang perlu dijalankan ulang saat sesuatu berubah",
        "Mencatat parameter, data, dan versi kode pada setiap run",
        "Membersihkan notebook sebelum dicommit",
    ],
    [
        T("""
        ## Analisis sebagai rangkaian langkah

        Analisis nyata jarang satu skrip raksasa. Ia terdiri dari langkah-langkah: ambil data, bersihkan, bangun fitur, latih model, buat laporan. Tiap langkah menghasilkan keluaran yang dipakai langkah berikutnya. Memandang analisis sebagai **pipeline** membuat tiap bagian dapat diuji dan dijalankan ulang secara terpisah.

        Pipeline yang baik menyatakan ketergantungan antar langkah dengan jelas, sehingga siapa pun tahu urutan menjalankan dan apa yang terdampak bila satu langkah berubah.
        """),
        T("""
        ## Graf ketergantungan

        Ketergantungan antar langkah membentuk graf terarah tanpa siklus. Langkah `bersih` bergantung pada `ambil`, `fitur` pada `bersih`, dan seterusnya. Urutan menjalankan yang benar adalah **urutan topologis**: setiap langkah muncul setelah semua langkah yang menjadi prasyaratnya.

        Alat pembangun seperti Make dan banyak pengelola alur kerja bekerja dengan prinsip ini. Kita dapat meniru intinya dalam beberapa baris Python.
        """),
        C(
            """
            def urutan_langkah(deps):
                sisa = {k: set(v) for k, v in deps.items()}
                hasil = []
                while sisa:
                    siap = sorted(k for k, v in sisa.items() if not (v - set(hasil)))
                    if not siap:
                        raise ValueError('ada siklus')
                    langkah = siap[0]
                    hasil.append(langkah)
                    del sisa[langkah]
                return hasil

            deps = {
                'ambil': [],
                'bersih': ['ambil'],
                'fitur': ['bersih'],
                'model': ['fitur'],
                'laporan': ['model', 'bersih'],
            }
            print(urutan_langkah(deps))
            try:
                urutan_langkah({'a': ['b'], 'b': ['a']})
            except ValueError as e:
                print(e)
            """,
            """
            ['ambil', 'bersih', 'fitur', 'model', 'laporan']
            ada siklus
            """,
            """
            Langkah diurutkan sesuai prasyaratnya, dan ketergantungan melingkar ditolak karena tidak mungkin dijalankan.
            """,
            filename="urutan_langkah.py",
        ),
        T("""
        ## Menjalankan ulang secukupnya

        Bila hanya langkah `fitur` yang berubah, tidak perlu mengambil dan membersihkan data lagi. Cukup jalankan ulang `fitur` dan semua langkah di hilirnya, yaitu yang bergantung padanya secara langsung maupun tidak langsung. Menghemat waktu ini sangat berarti pada pipeline yang berjalan berjam-jam.

        Menentukan himpunan langkah terdampak adalah penelusuran sederhana di sepanjang urutan topologis: langkah perlu diulang bila ia berubah atau salah satu prasyaratnya diulang.
        """),
        C(
            """
            def urutan_langkah(deps):
                sisa = {k: set(v) for k, v in deps.items()}
                hasil = []
                while sisa:
                    siap = sorted(k for k, v in sisa.items() if not (v - set(hasil)))
                    if not siap:
                        raise ValueError('ada siklus')
                    langkah = siap[0]
                    hasil.append(langkah)
                    del sisa[langkah]
                return hasil

            def perlu_dijalankan(deps, diubah):
                ulang = set()
                hasil = []
                for langkah in urutan_langkah(deps):
                    if langkah in diubah or any(d in ulang for d in deps[langkah]):
                        ulang.add(langkah)
                        hasil.append(langkah)
                return hasil

            deps = {
                'ambil': [],
                'bersih': ['ambil'],
                'fitur': ['bersih'],
                'model': ['fitur'],
                'laporan': ['model', 'bersih'],
            }
            print(perlu_dijalankan(deps, {'fitur'}))
            print(perlu_dijalankan(deps, {'laporan'}))
            print(perlu_dijalankan(deps, {'ambil'}))
            """,
            """
            ['fitur', 'model', 'laporan']
            ['laporan']
            ['ambil', 'bersih', 'fitur', 'model', 'laporan']
            """,
            """
            Perubahan di hulu memicu seluruh langkah di hilirnya, sedangkan perubahan di langkah terakhir hanya menjalankan langkah itu.
            """,
            filename="perlu_dijalankan.py",
        ),
        T("""
        ## Mencatat setiap run

        Setiap kali analisis dijalankan, catat tiga hal: **parameter** yang dipakai, **sidik jari data**, dan **versi kode**, misalnya hash commit Git. Ketiganya bersama menentukan hasil. Gabungkan menjadi satu identitas run yang singkat, sehingga hasil dapat dihubungkan kembali dengan persis apa yang menghasilkannya.

        Catatan ini dapat berupa baris di file log, entri di basis data kecil, atau alat pelacak eksperimen. Bentuknya kurang penting dibanding kebiasaan melakukannya.
        """),
        C(
            """
            import hashlib
            import json

            def catat_run(params, hash_data, versi_kode):
                isi = {'params': params, 'hash_data': hash_data, 'versi_kode': versi_kode}
                teks = json.dumps(isi, sort_keys=True)
                isi['id'] = hashlib.sha256(teks.encode('utf-8')).hexdigest()[:12]
                return isi

            a = catat_run({'seed': 42, 'rasio': 0.8}, 'h1', 'v1')
            b = catat_run({'rasio': 0.8, 'seed': 42}, 'h1', 'v1')
            c = catat_run({'seed': 43, 'rasio': 0.8}, 'h1', 'v1')
            print(a['id'] == b['id'])
            print(a['id'] == c['id'])
            print(len(a['id']))
            print(sorted(a))
            """,
            """
            True
            False
            12
            ['hash_data', 'id', 'params', 'versi_kode']
            """,
            """
            Run dengan masukan sama punya identitas sama walau urutan parameter berbeda, dan mengubah seed menghasilkan identitas baru.
            """,
            filename="catat_run.py",
        ),
        T("""
        ## Notebook dan version control

        Notebook Jupyter nyaman untuk eksplorasi, tetapi kurang ramah version control. File `.ipynb` adalah JSON yang menyimpan kode, keluaran, gambar, dan nomor eksekusi. Setiap kali sel dijalankan ulang, nomor eksekusi dan keluaran berubah sehingga diff dipenuhi kebisingan walau kodenya tidak berubah.

        Praktik yang disarankan: bersihkan keluaran sebelum commit, dan pindahkan logika yang matang ke modul `.py` yang diimpor notebook, sehingga diff kode bersih dan dapat diuji.
        """),
        C(
            """
            import copy

            def bersihkan_notebook(nb):
                baru = copy.deepcopy(nb)
                for sel in baru['cells']:
                    if sel['cell_type'] == 'code':
                        sel['outputs'] = []
                        sel['execution_count'] = None
                return baru

            nb = {'cells': [
                {'cell_type': 'markdown', 'source': 'Judul'},
                {'cell_type': 'code', 'source': 'print(1)', 'outputs': ['1'], 'execution_count': 5},
            ]}
            bersih = bersihkan_notebook(nb)
            print(bersih['cells'][1]['outputs'], bersih['cells'][1]['execution_count'])
            print(nb['cells'][1]['outputs'], nb['cells'][1]['execution_count'])
            print(bersih['cells'][0] == nb['cells'][0])
            """,
            """
            [] None
            ['1'] 5
            True
            """,
            """
            Keluaran dan nomor eksekusi dibuang pada salinan, notebook asli tidak berubah, dan sel teks dibiarkan utuh.
            """,
            filename="bersihkan_notebook.py",
        ),
        T("""
        ## Satu perintah dari awal sampai akhir

        Tujuan akhir reproduksibilitas adalah satu perintah yang menjalankan seluruh analisis di mesin bersih: pasang lingkungan, verifikasi data, jalankan pipeline, hasilkan laporan. Bila perintah itu ada dan berhasil dijalankan orang lain, proyek Anda dapat dipercaya.

        Tidak perlu langsung sempurna. Mulailah dengan skrip `jalankan_semua` sederhana yang memanggil langkah-langkah berurutan, lalu perbaiki seiring waktu.
        """),
        T("""
        ## Ringkasan course

        Anda telah belajar bahwa version control mencatat riwayat, cabang memungkinkan kerja paralel, merge dan konflik menyatukannya, dan remote menghubungkan tim. Pada modul terakhir ini Anda melihat bagaimana semua itu bermuara pada analisis yang dapat diulang: seed, sidik jari, lingkungan terkunci, data terverifikasi, pipeline jelas, dan catatan run.

        Kebiasaan ini tidak hanya melindungi hasil Anda, tetapi juga membuat Anda lebih cepat dan lebih percaya diri dalam setiap proyek data berikutnya.
        """),
        K(
            "tip",
            """
            Catat parameter, sidik jari data, dan versi kode untuk setiap run penting. Ketiganya menjelaskan hasil sepenuhnya.
            """,
            title="Catatan run",
        ),
        T("""
        ## Menguji tiap langkah

        Karena setiap langkah adalah fungsi dengan masukan dan keluaran jelas, ia dapat diuji terpisah dengan contoh kecil. Uji bahwa pembersihan membuang baris rusak, bahwa fitur memiliki kolom yang diharapkan, dan bahwa metrik berada dalam rentang wajar. Pengujian otomatis menangkap kesalahan sebelum sampai ke laporan.
        """),
        T("""
        ## Menyimpan keluaran perantara

        Simpan keluaran tiap langkah ke folder processed bersama sidik jarinya. Bila sidik jari masukan tidak berubah sejak run terakhir, langkah dapat dilewati dan hasil lama dipakai ulang. Teknik caching ini menghemat waktu dan sekaligus memberi bukti bahwa hasil lama masih sah untuk masukan yang sama.
        """),
        T("""
        ## Membaca log run

        Log run yang baik dapat dijawab dengan tiga pertanyaan: apa yang dijalankan, dengan apa, dan hasilnya apa. Dengan identitas run, Anda dapat menemukan eksperimen yang menghasilkan metrik terbaik dan mengulangnya persis. Tanpa log, eksperimen terbaik sering hilang karena tidak ada yang ingat parameternya.
        """),
        E(
            "A7-04-3-ex1",
            "mudah",
            """
            Tulis fungsi `urutan_langkah(deps)` yang menerima dict `{langkah: [prasyarat, ...]}` dan mengembalikan list urutan topologis. Bila beberapa langkah siap sekaligus, pilih yang paling awal secara alfabet. Bila ada siklus, lemparkan `ValueError`.
            """,
            """
            def urutan_langkah(deps):
                # TODO: implementasikan
                pass
            """,
            DEPS_I + """

            assert urutan_langkah(deps) == ['ambil', 'bersih', 'fitur', 'model', 'laporan']
            assert urutan_langkah({'b': [], 'a': []}) == ['a', 'b']
            assert urutan_langkah({'x': ['y'], 'y': []}) == ['y', 'x']
            try:
                urutan_langkah({'a': ['b'], 'b': ['a']})
                ditolak = False
            except ValueError:
                ditolak = True
            assert ditolak is True
            """,
            "Ambil langkah yang semua prasyaratnya sudah selesai, paling awal secara alfabet, berulang.",
            URUT_FN.strip("\n"),
        ),
        E(
            "A7-04-3-ex2",
            "sedang",
            """
            Tulis fungsi `perlu_dijalankan(deps, diubah)` yang mengembalikan list langkah (dalam urutan topologis alfabetis seperti `urutan_langkah`) yang harus dijalankan ulang bila himpunan langkah `diubah` berubah: langkah itu sendiri dan semua langkah yang bergantung padanya, langsung maupun tidak langsung. Fungsi `urutan_langkah` sudah tersedia.
            """,
            """
            def urutan_langkah(deps):
                sisa = {k: set(v) for k, v in deps.items()}
                hasil = []
                while sisa:
                    siap = sorted(k for k, v in sisa.items() if not (v - set(hasil)))
                    if not siap:
                        raise ValueError('ada siklus')
                    langkah = siap[0]
                    hasil.append(langkah)
                    del sisa[langkah]
                return hasil

            def perlu_dijalankan(deps, diubah):
                # TODO: implementasikan
                pass
            """,
            DEPS_I + """

            assert perlu_dijalankan(deps, {'fitur'}) == ['fitur', 'model', 'laporan']
            assert perlu_dijalankan(deps, {'laporan'}) == ['laporan']
            assert perlu_dijalankan(deps, {'ambil'}) == ['ambil', 'bersih', 'fitur', 'model', 'laporan']
            assert perlu_dijalankan(deps, set()) == []
            """,
            "Telusuri urutan topologis dan tandai langkah yang berubah atau yang prasyaratnya ditandai.",
            ULANG_FN.strip("\n"),
        ),
        E(
            "A7-04-3-ex3",
            "sedang",
            """
            Tulis fungsi `catat_run(params, hash_data, versi_kode)` yang mengembalikan dict berkunci `params`, `hash_data`, `versi_kode`, dan `id`. Nilai `id` adalah 12 karakter pertama SHA-256 heksadesimal dari `json.dumps` dict tiga kunci pertama dengan `sort_keys=True` (di-encode UTF-8).
            """,
            """
            import hashlib
            import json

            def catat_run(params, hash_data, versi_kode):
                # TODO: implementasikan
                pass
            """,
            """
            a = catat_run({'seed': 42, 'rasio': 0.8}, 'h1', 'v1')
            b = catat_run({'rasio': 0.8, 'seed': 42}, 'h1', 'v1')
            c = catat_run({'seed': 43, 'rasio': 0.8}, 'h1', 'v1')
            assert set(a) == {'params', 'hash_data', 'versi_kode', 'id'}
            assert len(a['id']) == 12
            assert a['id'] == b['id']
            assert a['id'] != c['id']
            assert catat_run({}, 'h1', 'v1')['id'] != catat_run({}, 'h2', 'v1')['id']
            """,
            "Hash dict tiga kunci dengan kunci terurut lalu ambil dua belas karakter pertama.",
            CATAT_FN.strip("\n"),
        ),
        E(
            "A7-04-3-ex4",
            "menantang",
            """
            Tulis fungsi `bersihkan_notebook(nb)` yang mengembalikan salinan notebook (dict dengan list `cells`) di mana setiap sel berjenis `code` memiliki `outputs` berupa list kosong dan `execution_count` bernilai `None`. Sel lain tidak diubah dan notebook asli tidak boleh berubah.
            """,
            """
            import copy

            def bersihkan_notebook(nb):
                # TODO: implementasikan
                pass
            """,
            """
            nb = {'cells': [
                {'cell_type': 'markdown', 'source': 'Judul'},
                {'cell_type': 'code', 'source': 'print(1)', 'outputs': ['1'], 'execution_count': 5},
            ]}
            b = bersihkan_notebook(nb)
            assert b['cells'][1]['outputs'] == [] and b['cells'][1]['execution_count'] is None
            assert nb['cells'][1]['outputs'] == ['1'] and nb['cells'][1]['execution_count'] == 5
            assert b['cells'][0] == nb['cells'][0]
            assert b['cells'][1]['source'] == 'print(1)'
            """,
            "Salin dalam-dalam notebook lalu kosongkan keluaran pada sel kode.",
            NB_FN.strip("\n"),
        ),
    ],
    [
        M("Menjalankan ulang seluruh pipeline untuk perubahan kecil.", "Jalankan hanya langkah terdampak dan hilirnya."),
        M("Tidak mencatat parameter dan versi kode tiap run.", "Catat identitas run lengkap."),
        M("Mencommit notebook dengan semua keluaran.", "Bersihkan keluaran sebelum commit."),
    ],
    [
        Q("Urutan topologis berarti?", ["Prasyarat selalu lebih dulu", "Urut alfabet", "Urut ukuran", "Urut waktu edit"], 0, "Langkah setelah prasyaratnya.", hint="Prasyarat."),
        Q("Langkah hilir adalah?", ["Yang bergantung pada langkah berubah", "Langkah pertama", "Langkah paling lama", "Langkah gagal"], 0, "Terdampak.", hint="Bergantung."),
        Q("Identitas run mencakup?", ["Parameter, data, dan versi kode", "Hanya nama file", "Hanya waktu", "Hanya hasil"], 0, "Tiga penentu hasil.", hint="Tiga."),
        Q("Notebook sebaiknya sebelum commit?", ["Dibersihkan keluarannya", "Ditambah keluaran", "Dihapus", "Diubah ke PDF"], 0, "Diff bersih.", hint="Bersih."),
        Q("Ketergantungan melingkar menyebabkan?", ["Urutan tidak mungkin dibuat", "Pipeline lebih cepat", "Data hilang", "Kode lebih pendek"], 0, "Siklus.", hint="Siklus."),
    ],
    [
        "Pipeline menyatakan ketergantungan antar langkah dengan jelas.",
        "Hanya langkah terdampak dan hilirnya yang perlu dijalankan ulang.",
        "Catat parameter, sidik jari data, dan versi kode setiap run.",
        "Bersihkan notebook dan pindahkan logika matang ke modul.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perintah yang cukup jelas dalam teks.", "brief": []}

write_module(
    "A7",
    4,
    "Workflow analisis yang reproducible",
    105,
    [
        "Menjelaskan reproduksibilitas dan mengendalikan keacakan",
        "Menyusun proyek, lingkungan, dan data yang dapat diverifikasi",
        "Membangun pipeline yang tercatat dan dapat dijalankan ulang secukupnya",
    ],
    [l1, l2, l3],
    video,
    REF,
)
