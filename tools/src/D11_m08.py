import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = [{"book": "Machine Learning Yearning (Andrew Ng)", "chapters": "bab 44 sampai 58"}]

PIPE = """
import numpy as np
import warnings
warnings.simplefilter("ignore")
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier

def data(n, seed):
    r = np.random.default_rng(seed)
    X = r.normal(size=(n, 10))
    z = (X[:, 0] + X[:, 1] > 0).astype(int)
    y = ((2 * z - 1) + 0.8 * X[:, 2] > 0).astype(int)
    return X, z, y
"""

SEARCH = """
import itertools
import numpy as np

def skor_urutan(u, b, s):
    return sum(u[x] for x in s) + sum(b[s[i - 1]][s[i]] for i in range(1, len(s)))

def greedy_decode(u, b, L):
    s = [int(np.argmax(u))]
    for _ in range(L - 1):
        s.append(int(np.argmax([u[v] + b[s[-1]][v] for v in range(len(u))])))
    return tuple(s)

def eksak(u, b, L):
    return max(itertools.product(range(len(u)), repeat=L), key=lambda s: skor_urutan(u, b, s))
"""

l1 = lesson(
    "D11-08-1",
    "Optimization Verification test",
    35,
    [
        "Menjelaskan sistem yang terdiri atas fungsi skor dan algoritma pencarian",
        "Menerapkan tes verifikasi dengan membandingkan skor jawaban benar dan jawaban keluaran",
        "Mengklasifikasikan kegagalan sebagai masalah pencarian atau masalah fungsi skor",
        "Memakai pola yang sama pada kasus umum termasuk reinforcement learning",
    ],
    [
        T("""
        ## Dua bagian yang bisa salah

        Banyak sistem pembelajaran mesin bekerja dengan dua komponen. Komponen pertama adalah **fungsi skor** yang menilai seberapa bagus sebuah jawaban kandidat untuk sebuah masukan. Komponen kedua adalah **algoritma pencarian** yang mencari jawaban dengan skor tertinggi. Contohnya pengenalan suara: fungsi skor menilai kecocokan sebuah kalimat dengan rekaman, dan pencarian (misalnya beam search) menelusuri ruang kalimat yang sangat besar untuk menemukan kalimat berskor tinggi.

        Ketika sistem salah, ada dua kemungkinan. Fungsi skor keliru: jawaban yang benar justru diberi skor lebih rendah dari jawaban yang salah, sehingga bahkan pencarian sempurna akan memilih jawaban salah. Atau pencarian gagal: jawaban benar sebenarnya berskor lebih tinggi, tetapi algoritma tidak menemukannya karena menelusuri ruang secara terbatas.

        Dua kemungkinan itu butuh perbaikan berbeda. Jika masalahnya fungsi skor, kamu melatih ulang atau memperbaiki model. Jika masalahnya pencarian, kamu memperbesar lebar beam atau memperbaiki algoritma pencariannya. Menebak yang mana membuang waktu berminggu-minggu.
        """),
        T("""
        ## Tes verifikasi

        Tes ini sederhana. Untuk satu contoh yang salah, ambil jawaban benar `y*` dari label manusia, dan jawaban keluaran sistem `y_out`. Hitung skor keduanya dengan fungsi skor yang sama, lalu bandingkan.

        Jika skor `y*` lebih besar daripada skor `y_out`, fungsi skor sudah menyukai jawaban benar, tetapi pencarian gagal menemukannya. Masalahnya ada di algoritma pencarian. Jika skor `y*` lebih kecil atau sama dengan skor `y_out`, pencarian sudah melakukan tugasnya: ia menemukan jawaban yang skornya setinggi atau lebih tinggi. Fungsi skor sendiri yang menyukai jawaban salah, dan itulah yang perlu diperbaiki.

        Tes ini murah karena hanya menghitung dua skor per contoh, dan tidak butuh menjalankan eksperimen pelatihan baru. Lakukan pada banyak contoh yang salah untuk melihat pecahan kegagalan masing-masing jenis.
        """),
        T("""
        ## Dari tes ke keputusan

        Misalkan dari 100 contoh dev yang salah, 55 tergolong kegagalan pencarian dan 45 kegagalan fungsi skor. Dengan begitu, kamu punya dasar kuantitatif seperti pada error analysis di modul 3: memperbaiki pencarian paling banyak menghilangkan 55 persen kesalahan, dan memperbaiki fungsi skor paling banyak 45 persen. Pilih berdasarkan batas atas manfaat dan biaya, bukan firasat.

        Sering kali tim terlalu cepat menyalahkan model dan mengumpulkan data lebih banyak, padahal pencarian yang terlalu sempit yang membuat jawaban benar terlewat. Kebalikannya juga terjadi: tim memperlebar beam berulang kali tanpa hasil karena fungsi skor memang menyukai jawaban yang salah. Tes verifikasi memutus kebuntuan itu dengan data.

        Sedikit catatan: tes ini berlaku bila jawaban benar bisa dinilai oleh fungsi skor yang sama. Jika ada beberapa jawaban benar yang berbeda, pakai yang skornya tertinggi atau periksa semuanya.
        """),
        T("""
        ## Bentuk umum dan reinforcement learning

        Pola ini bisa digeneralisasi. Nama bentuk umumnya: kamu punya fungsi nilai `Skor_x(y)` yang menilai jawaban `y` untuk masukan `x`, dan algoritma `A` yang mencoba memaksimalkannya. Hasil `y_out = A(x)`. Bandingkan `Skor_x(y*)` dengan `Skor_x(y_out)` untuk jawaban benar `y*`.

        Dalam reinforcement learning, fungsi skor adalah imbalan kumulatif yang diharapkan dari sebuah kebijakan atau lintasan, dan algoritma pencarian adalah prosedur optimisasi kebijakan. Misalkan sebuah agen mengendalikan helikopter dan jatuh. Jika lintasan pilot manusia mendapat imbalan lebih tinggi daripada lintasan agen menurut fungsi imbalan, optimisasi agen gagal dan perlu diperbaiki. Jika imbalan lintasan manusia justru lebih rendah, fungsi imbalan yang perlu direvisi, karena ia memberi nilai terlalu tinggi pada perilaku yang buruk.

        Poin pentingnya adalah memisahkan pertanyaan apakah yang kamu minta sudah benar dari pertanyaan apakah algoritma sudah mengerjakannya dengan baik.
        """),
        A(
            "Analogi navigasi",
            """
            Fungsi skor seperti peta yang menandai tujuan terbaik, sedangkan pencarian seperti pengemudi yang mencari jalannya. Jika pengemudi sampai di tempat yang peta nilai lebih rendah dari tujuan benar, ia tersesat. Jika ia sampai di tempat yang peta nilai tinggi tetapi bukan tujuan sebenarnya, petanya yang keliru.
            """,
        ),
        K(
            "tip",
            """
            Catat dua skor di samping tiap contoh yang salah, lalu hitung fraksi kegagalan pencarian dan fungsi skor. Dua kolom itu langsung menunjukkan ke mana usaha berikutnya diarahkan.
            """,
            title="Tips verifikasi",
        ),
        C(
            SEARCH
            + """
u = [1.0, 0.0]
b = [[-3.0, 0.0], [5.0, 0.0]]
out = greedy_decode(u, b, 2)
terbaik = eksak(u, b, 2)
print("greedy :", out, skor_urutan(u, b, out))
print("eksak  :", terbaik, skor_urutan(u, b, terbaik))
""",
            """
            greedy : (0, 1) 1.0
            eksak  : (1, 0) 6.0
            """,
            """
            Pencarian greedy memilih langkah pertama terbaik secara lokal lalu terjebak. Jawaban eksak berskor 6 tetapi greedy hanya mendapat 1. Jika jawaban benar adalah (1, 0), tes verifikasi menyalahkan pencarian, bukan fungsi skor.
            """,
            filename="greedy_vs_eksak.py",
        ),
        C(
            SEARCH
            + """
def verifikasi(skor_ref, skor_out):
    return "pencarian" if round(skor_ref - skor_out, 9) > 0 else "fungsi_skor"

hitung = {"pencarian": 0, "fungsi_skor": 0}
for seed in range(200):
    r0 = np.random.default_rng(seed)
    u = r0.normal(size=3)
    b = r0.normal(size=(3, 3))
    r1 = np.random.default_rng(1000 + seed)
    nu = u + 0.6 * r1.normal(size=3)
    nb = b + 0.6 * r1.normal(size=(3, 3))
    ref = eksak(nu, nb, 4)
    out = greedy_decode(u, b, 4)
    hitung[verifikasi(skor_urutan(u, b, ref), skor_urutan(u, b, out))] += 1
print(hitung)
""",
            """
            {'pencarian': 55, 'fungsi_skor': 145}
            """,
            """
            Dari 200 contoh, 55 kegagalan berasal dari pencarian dan 145 dari fungsi skor. Karena pecahan fungsi skor jauh lebih besar, memperlebar pencarian saja paling banyak memperbaiki sekitar seperempat kesalahan.
            """,
            filename="hitung_kegagalan.py",
        ),
        C(
            """
def fraksi(hitung):
    total = sum(hitung.values())
    return {k: round(v / total, 4) for k, v in hitung.items()}

print(fraksi({"pencarian": 55, "fungsi_skor": 145}))
""",
            """
            {'pencarian': 0.275, 'fungsi_skor': 0.725}
            """,
            """
            Fraksi kegagalan pencarian 27,5 persen dan fungsi skor 72,5 persen. Inilah batas atas manfaat tiap jenis perbaikan, setara dengan fraksi kategori pada error analysis.
            """,
            filename="fraksi.py",
        ),
        E(
            "D11-08-1-ex1",
            "mudah",
            """
            Tulis fungsi `verifikasi(skor_ref, skor_out)` yang mengembalikan `"pencarian"` bila `skor_ref` lebih besar dari `skor_out` (selisih dibulatkan 9 desimal) dan `"fungsi_skor"` selainnya.
            """,
            """
            def verifikasi(skor_ref, skor_out):
                # TODO: implementasikan
                pass
            """,
            """
            assert verifikasi(6.0, 1.0) == "pencarian"
            assert verifikasi(1.0, 1.0) == "fungsi_skor"
            assert verifikasi(0.5, 2.0) == "fungsi_skor"
            assert verifikasi(0.1 + 0.2, 0.3) == "fungsi_skor"
            """,
            "Jawaban benar yang berskor lebih tinggi berarti pencarian gagal menemukannya. Hati-hati dengan galat floating point pada selisih.",
            """
            def verifikasi(skor_ref, skor_out):
                return "pencarian" if round(skor_ref - skor_out, 9) > 0 else "fungsi_skor"
            """,
            names=[
                ("Pencarian gagal", "Skor jawaban benar lebih tinggi terdeteksi"),
                ("Skor sama", "Skor sama dianggap fungsi skor"),
                ("Fungsi skor keliru", "Jawaban salah berskor lebih tinggi terdeteksi"),
                ("Galat floating point", "Selisih dibulatkan dengan benar"),
            ],
        ),
        E(
            "D11-08-1-ex2",
            "sedang",
            """
            Tulis fungsi `hitung_kategori(pasangan)` yang menerima list tuple `(skor_ref, skor_out)` dan mengembalikan dictionary `{"pencarian": a, "fungsi_skor": b}` berisi jumlah tiap kategori memakai aturan tes verifikasi (selisih dibulatkan 9 desimal, lebih besar dari 0 berarti pencarian).
            """,
            """
            def hitung_kategori(pasangan):
                # TODO: implementasikan
                pass
            """,
            """
            p = [(6.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 4.0)]
            assert hitung_kategori(p) == {"pencarian": 2, "fungsi_skor": 2}
            assert hitung_kategori([]) == {"pencarian": 0, "fungsi_skor": 0}
            assert hitung_kategori([(1.0, 0.0)] * 3) == {"pencarian": 3, "fungsi_skor": 0}
            """,
            "Mulai dari dictionary dengan dua kunci bernilai nol lalu tambahkan satu per pasangan.",
            """
            def hitung_kategori(pasangan):
                hasil = {"pencarian": 0, "fungsi_skor": 0}
                for ref, out in pasangan:
                    hasil["pencarian" if round(ref - out, 9) > 0 else "fungsi_skor"] += 1
                return hasil
            """,
            names=[
                ("Campuran kategori", "Dua dan dua terhitung benar"),
                ("Daftar kosong", "Kasus kosong menghasilkan nol"),
                ("Semua pencarian", "Semua pasangan dikategorikan pencarian"),
            ],
        ),
        E(
            "D11-08-1-ex3",
            "sedang",
            """
            Tulis fungsi `skor_urutan(u, b, s)` yang mengembalikan jumlah `u[x]` untuk tiap elemen urutan `s` ditambah jumlah `b[s[i-1]][s[i]]` untuk `i` dari 1. Tulis juga `greedy_decode(u, b, L)` yang memilih elemen pertama dengan `argmax(u)` lalu tiap langkah berikutnya memilih `v` yang memaksimalkan `u[v] + b[sebelumnya][v]`. Kembalikan tuple integer sepanjang `L`.
            """,
            """
            import numpy as np

            def skor_urutan(u, b, s):
                # TODO: implementasikan
                pass

            def greedy_decode(u, b, L):
                # TODO: implementasikan
                pass
            """,
            """
            import numpy as np
            u = [1.0, 0.0]
            b = [[-3.0, 0.0], [5.0, 0.0]]
            assert skor_urutan(u, b, (1, 0)) == 6.0
            assert skor_urutan(u, b, (0, 1)) == 1.0
            assert greedy_decode(u, b, 2) == (0, 1)
            assert greedy_decode(u, b, 1) == (0,)
            assert all(isinstance(x, int) for x in greedy_decode(u, b, 3))
            """,
            "Untuk greedy simpan list hasil dan ubah menjadi tuple di akhir. Gunakan int(np.argmax(...)) agar tipe integer biasa.",
            """
            import numpy as np

            def skor_urutan(u, b, s):
                return sum(u[x] for x in s) + sum(b[s[i - 1]][s[i]] for i in range(1, len(s)))

            def greedy_decode(u, b, L):
                s = [int(np.argmax(u))]
                for _ in range(L - 1):
                    s.append(int(np.argmax([u[v] + b[s[-1]][v] for v in range(len(u))])))
                return tuple(s)
            """,
        ),
        E(
            "D11-08-1-ex4",
            "menantang",
            """
            Tulis fungsi `diagnosa_pencarian(u, b, L, y_ref)` yang memakai `greedy_decode` dan `skor_urutan` (sudah disediakan) untuk mendapat `y_out`, lalu mengembalikan tuple `(kategori, skor_ref, skor_out)` dengan `kategori` hasil tes verifikasi (`"pencarian"` bila skor ref lebih besar setelah pembulatan 9 desimal, selainnya `"fungsi_skor"`). Skor dikembalikan sebagai float.
            """,
            """
            import numpy as np

            def skor_urutan(u, b, s):
                return sum(u[x] for x in s) + sum(b[s[i - 1]][s[i]] for i in range(1, len(s)))

            def greedy_decode(u, b, L):
                s = [int(np.argmax(u))]
                for _ in range(L - 1):
                    s.append(int(np.argmax([u[v] + b[s[-1]][v] for v in range(len(u))])))
                return tuple(s)

            def diagnosa_pencarian(u, b, L, y_ref):
                # TODO: implementasikan
                pass
            """,
            """
            u = [1.0, 0.0]
            b = [[-3.0, 0.0], [5.0, 0.0]]
            assert diagnosa_pencarian(u, b, 2, (1, 0)) == ("pencarian", 6.0, 1.0)
            assert diagnosa_pencarian(u, b, 2, (0, 1)) == ("fungsi_skor", 1.0, 1.0)
            assert diagnosa_pencarian(u, b, 2, (1, 1)) == ("fungsi_skor", 0.0, 1.0)
            assert isinstance(diagnosa_pencarian(u, b, 2, (1, 0))[1], float)
            """,
            "Dekode dengan greedy_decode, hitung dua skor dengan skor_urutan, lalu bandingkan.",
            """
            import numpy as np

            def skor_urutan(u, b, s):
                return sum(u[x] for x in s) + sum(b[s[i - 1]][s[i]] for i in range(1, len(s)))

            def greedy_decode(u, b, L):
                s = [int(np.argmax(u))]
                for _ in range(L - 1):
                    s.append(int(np.argmax([u[v] + b[s[-1]][v] for v in range(len(u))])))
                return tuple(s)

            def diagnosa_pencarian(u, b, L, y_ref):
                out = greedy_decode(u, b, L)
                sr = float(skor_urutan(u, b, y_ref))
                so = float(skor_urutan(u, b, out))
                kategori = "pencarian" if round(sr - so, 9) > 0 else "fungsi_skor"
                return kategori, sr, so
            """,
        ),
    ],
    [
        M(
            "Langsung mengumpulkan data baru ketika sistem salah.",
            "Cek dulu apakah kegagalan berasal dari pencarian atau fungsi skor dengan tes verifikasi.",
        ),
        M(
            "Memperlebar beam atau pencarian berulang kali tanpa mengukur skor jawaban benar.",
            "Bandingkan skor jawaban benar dengan skor keluaran sebelum memutuskan.",
        ),
        M(
            "Membandingkan skor dari dua fungsi skor yang berbeda.",
            "Gunakan fungsi skor yang sama untuk jawaban benar dan jawaban keluaran.",
        ),
    ],
    [
        Q(
            "Skor jawaban benar 6, skor keluaran 1 pada fungsi skor yang sama. Kesimpulan?",
            ["Fungsi skor keliru", "Pencarian gagal menemukan jawaban benar", "Label salah", "Data kurang"],
            1,
            "Jawaban benar berskor lebih tinggi tetapi tidak ditemukan, jadi pencarian yang gagal.",
            hint="Bandingkan dua skor: mana yang lebih tinggi dan siapa yang seharusnya menemukannya.",
        ),
        Q(
            "Skor jawaban benar 1, skor keluaran 3. Kesimpulan?",
            ["Pencarian gagal", "Fungsi skor menyukai jawaban salah", "Tidak ada masalah", "Dev set bocor"],
            1,
            "Pencarian menemukan jawaban yang skornya lebih tinggi, sehingga fungsi skor yang keliru.",
            hint="Pencarian sudah menemukan skor lebih tinggi dari jawaban benar.",
        ),
        Q(
            "Apa keuntungan utama tes verifikasi?",
            ["Menaikkan akurasi langsung", "Murah dan memberi arah perbaikan yang tepat", "Menghapus bias", "Mengganti dev set"],
            1,
            "Hanya butuh menghitung dua skor per contoh dan menunjukkan komponen yang harus diperbaiki.",
            hint="Pikirkan biaya dan informasi yang diberikan.",
        ),
        Q(
            "Pada reinforcement learning, apa padanan fungsi skor?",
            ["Ukuran batch", "Imbalan kumulatif yang diharapkan", "Learning rate", "Jumlah episode"],
            1,
            "Fungsi imbalan menilai kebijakan atau lintasan, dan optimisasi kebijakan adalah pencariannya.",
            hint="Apa yang dinilai terhadap sebuah lintasan?",
        ),
        Q(
            "Dari 100 kesalahan, 80 kegagalan pencarian. Batas atas manfaat memperbaiki pencarian?",
            ["20 persen", "80 persen", "100 persen", "8 persen"],
            1,
            "Memperbaiki pencarian menghilangkan paling banyak kesalahan kategori itu, yaitu 80 persen.",
            hint="Sama seperti fraksi kategori pada error analysis.",
        ),
    ],
    [
        "Sistem punya fungsi skor dan algoritma pencarian yang bisa salah terpisah.",
        "Jika skor jawaban benar lebih tinggi dari skor keluaran, pencarian yang gagal.",
        "Jika tidak, fungsi skor yang perlu diperbaiki.",
        "Pola ini berlaku umum termasuk reinforcement learning.",
    ],
    ["Machine Learning Yearning, bab 44 sampai 46 (Andrew Ng): Optimization Verification test"],
)

l2 = lesson(
    "D11-08-2",
    "Pipeline melawan end-to-end learning",
    35,
    [
        "Membedakan sistem pipeline dan sistem end-to-end",
        "Menyebutkan keuntungan dan kerugian end-to-end learning",
        "Memilih komponen pipeline berdasarkan ketersediaan data dan kesederhanaan tugas",
        "Membandingkan keduanya secara empiris pada berbagai ukuran data",
    ],
    [
        T("""
        ## Dua cara menyusun sistem

        Banyak aplikasi tersusun dari beberapa tahap. Pengenalan suara klasik memakai urutan: rekaman audio, fitur akustik, fonem, kata, transkrip. Tiap tahap dibangun dan dilatih terpisah, dan keluaran satu tahap menjadi masukan tahap berikutnya. Ini disebut **pipeline**.

        Alternatifnya **end-to-end learning**: satu model besar langsung memetakan audio ke transkrip tanpa tahap perantara yang ditentukan manusia. Banyak aplikasi mengalami pergeseran dari pipeline ke end-to-end seiring data dan komputasi bertambah, termasuk pengenalan suara, terjemahan mesin, dan beberapa tugas citra.

        Pergeseran itu bukan jaminan bahwa end-to-end selalu lebih baik. Banyak tugas masih unggul dengan pipeline, terutama bila data pasangan masukan-keluaran terbatas. Memilih antara keduanya adalah keputusan rekayasa yang bisa dibuat berdasarkan data, bukan tren.
        """),
        T("""
        ## Kelebihan dan kekurangan end-to-end

        Kelebihan end-to-end: model belajar representasi perantara sendiri, tanpa kamu harus merancang tahap manual. Hasilnya bisa lebih baik bila data cukup, karena representasi yang dipelajari disesuaikan langsung dengan tujuan akhir. Pengembangan juga lebih sederhana: satu model, satu fungsi tujuan.

        Kekurangan: butuh banyak pasangan `(x, y)` lengkap, yang mungkin mahal. Ia juga membuang pengetahuan domain yang tertanam di komponen buatan tangan, dan sulit didiagnosis ketika salah karena tidak ada keluaran perantara yang bisa diperiksa.

        Pipeline sebaliknya. Ia memanfaatkan data untuk tiap tahap, yang sering lebih mudah dikumpulkan dan dilabeli. Keluaran perantaranya bisa diperiksa manusia. Kekurangannya adalah kesalahan menumpuk antar tahap, dan rancangan tahap yang buruk membatasi performa akhir.
        """),
        T("""
        ## Memilih komponen: ketersediaan data

        Jika kamu memilih pipeline, pertanyaan pertama untuk tiap komponen adalah apakah ada banyak data berlabel untuk melatihnya. Contoh mobil otonom. Kamu bisa memecah tugas menjadi detektor mobil, detektor pejalan kaki, dan perencana jalur. Detektor mobil dan pejalan kaki dapat dilatih dari data citra berlabel yang melimpah. Perencana jalur butuh data berupa pasangan lingkungan dan lintasan aman, yang lebih langka.

        Aturan umum: pecah tugas menjadi komponen yang masing-masing punya banyak data berlabel. Jika sebuah komponen tidak punya cukup data, sulit melatihnya dan lebih baik digabung dengan komponen lain atau dipelajari end-to-end bersama bagian yang punya data.

        Dalam praktiknya, hitung jumlah label per tahap. Jika data label tahap perantara jauh lebih banyak daripada data pasangan lengkap, pipeline hampir pasti menang pada ukuran data kecil.
        """),
        T("""
        ## Memilih komponen: kesederhanaan tugas

        Pertimbangan kedua adalah kesederhanaan. Komponen yang tugasnya sederhana lebih mudah dipelajari dengan sedikit data. Sebuah tahap yang hanya perlu menentukan apakah ada mobil di gambar jauh lebih mudah dipelajari daripada tahap yang menentukan niat pengemudi lain. Pecah tugas kompleks menjadi tugas yang dapat dipelajari manusia dengan jelas dan model dengan sedikit contoh.

        Dalam contoh penyaring pinjaman, tugas mengklasifikasikan risiko dari dokumen bisa dipecah: ekstraksi angka pendapatan dan utang dari dokumen, lalu model sederhana untuk risiko dari angka tersebut. Tahap ekstraksi mudah dilabeli, dan tahap risiko dapat dilatih dari sedikit contoh karena fiturnya sudah bersih.

        Kombinasi dua pertimbangan ini menjelaskan pola umum: ketika data pasangan lengkap sedikit, pipeline dengan komponen sederhana dan berlabel melimpah menang. Ketika data pasangan lengkap melimpah, end-to-end menyusul dan sering melampaui.
        """),
        T("""
        ## Membaca hasil eksperimen dengan hati-hati

        Hasil perbandingan pada data sintetis hanya menunjukkan pola, bukan hukum. Titik silang antara dua pendekatan bergeser bila model tahap kedua diganti, bila label perantara lebih berisik, atau bila hubungan antara tahap pertama dan jawaban akhir lebih rumit. Karena itu, lakukan perbandingan pada beberapa ukuran data pasangan dari kecil sampai besar, lalu gambar kurva error kedua pendekatan. Letak kurva berpotongan memberi tahu kapan investasi pengumpulan data pasangan layak dilakukan.

        Pertimbangkan juga biaya non-akurasi. Pipeline lebih mudah diaudit dan diperbaiki per bagian, sedangkan end-to-end lebih mudah dipelihara sebagai satu model. Tim kecil dengan data terbatas biasanya memulai dari pipeline sederhana, lalu beralih ketika data pasangan sudah cukup banyak.
        """),
        A(
            "Analogi dapur",
            """
            Pipeline seperti dapur dengan stasasiun terpisah: satu orang memotong, satu menumis, satu menyajikan, dan tiap orang bisa dilatih dengan cepat. End-to-end seperti satu koki yang belajar membuat hidangan utuh langsung dari resep dan hasil jadi. Koki tunggal bisa lebih halus, tetapi butuh jauh lebih banyak latihan penuh.
            """,
        ),
        K(
            "note",
            """
            Hasil di bawah memakai data sintetis kecil untuk menunjukkan pola, bukan angka universal. Titik silang antara pipeline dan end-to-end bergantung pada masalah, model, dan jumlah label perantara.
            """,
        ),
        C(
            PIPE
            + """
Xd, zd, yd = data(5000, 99)
Xa, za, _ = data(20000, 5)
s1 = LogisticRegression().fit(Xa, za)

def fitur(X):
    return np.c_[s1.predict_proba(X)[:, 1], X[:, 2]]

print("n_pasangan  err_end2end  err_pipeline")
for n in [100, 300, 1000, 5000]:
    X, z, y = data(n, 1)
    e2e = 1 - MLPClassifier((32,), max_iter=800, random_state=0).fit(X, y).score(Xd, yd)
    pipe = 1 - LogisticRegression().fit(fitur(X), y).score(fitur(Xd), yd)
    print(f"{n:10d}  {e2e:11.3f}  {pipe:12.3f}")
""",
            """
            n 100: end2end sekitar 0.18, pipeline sekitar 0.07
            n 300: end2end sekitar 0.16, pipeline sekitar 0.04
            n 1000: end2end sekitar 0.075, pipeline sekitar 0.04
            n 5000: end2end lebih rendah dari pipeline
            """,
            """
            Pipeline memakai 20.000 label perantara murah untuk tahap pertama dan hanya sedikit pasangan lengkap untuk tahap kedua. Ia unggul pada data pasangan kecil. End-to-end membutuhkan ribuan pasangan, lalu menyalip karena tidak dibatasi rancangan tahap manual.
            """,
            filename="pipeline_vs_e2e.py",
        ),
        C(
            """
def pilih(n_pasangan, n_label_perantara, ambang_e2e=2000):
    if n_pasangan >= ambang_e2e:
        return "end-to-end"
    if n_label_perantara >= 5 * max(1, n_pasangan):
        return "pipeline"
    return "pipeline dengan komponen lebih sederhana"

print(pilih(300, 20000))
print(pilih(5000, 20000))
print(pilih(300, 400))
""",
            """
            pipeline
            end-to-end
            pipeline dengan komponen lebih sederhana
            """,
            """
            Aturan praktis ini hanya heuristik awal. Ambang ditentukan dengan eksperimen seperti di contoh sebelumnya, tetapi struktur pertimbangannya jelas: bandingkan ukuran data pasangan dengan ukuran label perantara.
            """,
            filename="pilih_pendekatan.py",
        ),
        C(
            """
def rasio_data(n_pasangan, n_label_perantara):
    return round(n_label_perantara / n_pasangan, 2)

for n in [100, 300, 1000, 5000]:
    print(n, rasio_data(n, 20000))
""",
            """
            100 200.0
            300 66.67
            1000 20.0
            5000 4.0
            """,
            """
            Rasio label perantara terhadap pasangan lengkap mengecil seiring bertambahnya pasangan. Keunggulan pipeline menyusut ketika rasio mendekati satu.
            """,
            filename="rasio_data.py",
        ),
        E(
            "D11-08-2-ex1",
            "mudah",
            """
            Tulis fungsi `pilih_pendekatan(n_pasangan, ambang)` yang mengembalikan `"end-to-end"` bila `n_pasangan >= ambang` dan `"pipeline"` selainnya.
            """,
            """
            def pilih_pendekatan(n_pasangan, ambang):
                # TODO: implementasikan
                pass
            """,
            """
            assert pilih_pendekatan(5000, 2000) == "end-to-end"
            assert pilih_pendekatan(300, 2000) == "pipeline"
            assert pilih_pendekatan(2000, 2000) == "end-to-end"
            """,
            "Bandingkan dua angka dengan >=.",
            """
            def pilih_pendekatan(n_pasangan, ambang):
                return "end-to-end" if n_pasangan >= ambang else "pipeline"
            """,
        ),
        E(
            "D11-08-2-ex2",
            "sedang",
            """
            Tulis fungsi `komponen_layak(n_label_perantara, n_pasangan, rasio_min)` yang mengembalikan `True` bila `n_label_perantara >= rasio_min * n_pasangan` dan `False` selainnya. Jika `n_pasangan <= 0` kembalikan `True` bila `n_label_perantara > 0`.
            """,
            """
            def komponen_layak(n_label_perantara, n_pasangan, rasio_min):
                # TODO: implementasikan
                pass
            """,
            """
            assert komponen_layak(20000, 300, 5) is True
            assert komponen_layak(400, 300, 5) is False
            assert komponen_layak(1500, 300, 5) is True
            assert komponen_layak(10, 0, 5) is True
            assert komponen_layak(0, 0, 5) is False
            """,
            "Tangani n_pasangan nol atau negatif di awal. Pastikan hasilnya bool murni.",
            """
            def komponen_layak(n_label_perantara, n_pasangan, rasio_min):
                if n_pasangan <= 0:
                    return bool(n_label_perantara > 0)
                return bool(n_label_perantara >= rasio_min * n_pasangan)
            """,
        ),
        E(
            "D11-08-2-ex3",
            "sedang",
            """
            Tulis fungsi `titik_silang(ukuran, err_pipe, err_e2e)` yang mengembalikan ukuran pertama (menurut urutan list) ketika `err_e2e` lebih kecil dari `err_pipe` secara strict. Jika tidak pernah, kembalikan `None`. Tiga list sama panjang.
            """,
            """
            def titik_silang(ukuran, err_pipe, err_e2e):
                # TODO: implementasikan
                pass
            """,
            """
            u = [100, 300, 1000, 5000]
            assert titik_silang(u, [0.07, 0.04, 0.04, 0.03], [0.18, 0.16, 0.075, 0.01]) == 5000
            assert titik_silang(u, [0.07, 0.04, 0.04, 0.03], [0.18, 0.16, 0.075, 0.03]) is None
            assert titik_silang(u, [0.2, 0.2, 0.2, 0.2], [0.1, 0.3, 0.3, 0.3]) == 100
            assert titik_silang([], [], []) is None
            """,
            "Telusuri tiga list sekaligus dengan zip dan kembalikan ukuran pada kondisi pertama yang terpenuhi.",
            """
            def titik_silang(ukuran, err_pipe, err_e2e):
                for u, p, e in zip(ukuran, err_pipe, err_e2e):
                    if e < p:
                        return u
                return None
            """,
        ),
        E(
            "D11-08-2-ex4",
            "menantang",
            """
            Tulis fungsi `latih_pipeline(Xa, za, X, y)` yang melatih `LogisticRegression(max_iter=1000)` tahap pertama pada `(Xa, za)`, lalu membangun fitur `[proba_tahap1, X[:, 2]]` dan melatih `LogisticRegression(max_iter=1000)` tahap kedua pada `(fitur(X), y)`. Kembalikan fungsi `prediksi(Xbaru)` yang mengembalikan array label hasil tahap kedua.
            """,
            """
            import numpy as np
            from sklearn.linear_model import LogisticRegression

            def latih_pipeline(Xa, za, X, y):
                # TODO: implementasikan
                pass
            """,
            """
            import numpy as np
            def data(n, seed):
                r = np.random.default_rng(seed)
                X = r.normal(size=(n, 10))
                z = (X[:, 0] + X[:, 1] > 0).astype(int)
                y = ((2 * z - 1) + 0.8 * X[:, 2] > 0).astype(int)
                return X, z, y
            Xa, za, _ = data(5000, 5)
            X, z, y = data(200, 1)
            Xd, zd, yd = data(2000, 99)
            f = latih_pipeline(Xa, za, X, y)
            p = f(Xd)
            assert p.shape == (2000,)
            assert set(np.unique(p)) <= {0, 1}
            assert (p == yd).mean() > 0.9
            """,
            "Simpan model tahap pertama di closure. Fungsi fitur mengambil kolom proba kelas 1 dan kolom indeks 2 dari X.",
            """
            import numpy as np
            from sklearn.linear_model import LogisticRegression

            def latih_pipeline(Xa, za, X, y):
                s1 = LogisticRegression(max_iter=1000).fit(Xa, za)

                def fitur(Xn):
                    return np.c_[s1.predict_proba(Xn)[:, 1], Xn[:, 2]]

                s2 = LogisticRegression(max_iter=1000).fit(fitur(X), y)

                def prediksi(Xbaru):
                    return s2.predict(fitur(Xbaru))

                return prediksi
            """,
        ),
    ],
    [
        M(
            "Menganggap end-to-end selalu lebih baik.",
            "Bandingkan keduanya pada beberapa ukuran data dan pilih berdasarkan hasil.",
        ),
        M(
            "Memecah pipeline menjadi tahap yang tidak punya data berlabel.",
            "Pilih tahap yang punya banyak label dan tugas yang sederhana.",
        ),
        M(
            "Mengabaikan pengetahuan domain saat memakai end-to-end.",
            "Pertimbangkan komponen buatan tangan yang memberi informasi berharga ketika data pasangan terbatas.",
        ),
    ],
    [
        Q(
            "Pasangan lengkap hanya 300 sedangkan label perantara 20.000. Pendekatan yang kemungkinan unggul?",
            ["End-to-end", "Pipeline", "Keduanya sama", "Tidak bisa"],
            1,
            "Pipeline memanfaatkan label perantara melimpah sehingga unggul pada data pasangan kecil.",
            hint="Bandingkan jumlah data tiap tahap dengan data pasangan lengkap.",
        ),
        Q(
            "Kelemahan end-to-end yang utama?",
            ["Tidak bisa dilatih", "Butuh banyak pasangan masukan-keluaran lengkap", "Selalu lambat", "Tidak bisa dievaluasi"],
            1,
            "Tanpa data pasangan yang banyak, model tidak cukup belajar representasi perantara sendiri.",
            hint="Apa yang harus tersedia agar model belajar seluruh pemetaan?",
        ),
        Q(
            "Kelebihan pipeline dalam diagnosis?",
            ["Tidak perlu data", "Keluaran perantara bisa diperiksa manusia", "Selalu paling akurat", "Tidak punya bias"],
            1,
            "Keluaran tiap tahap bisa dilihat sehingga kesalahan lebih mudah dilacak.",
            hint="Pikirkan apa yang bisa dilihat di antara dua tahap.",
        ),
        Q(
            "Komponen pipeline sebaiknya?",
            ["Rumit dan unik", "Sederhana dengan banyak data berlabel", "Tanpa label", "Selalu satu"],
            1,
            "Tugas sederhana dengan label melimpah mudah dipelajari dan hemat data.",
            hint="Dua pertimbangan: data dan kesederhanaan.",
        ),
        Q(
            "Pola pada data sintetis: end-to-end menyalip pipeline ketika?",
            ["Data pasangan sedikit", "Data pasangan melimpah", "Label perantara hilang", "Model kecil"],
            1,
            "Dengan data pasangan banyak, model end-to-end tidak lagi dibatasi rancangan tahap manual.",
            hint="Lihat kolom ukuran data terbesar.",
        ),
    ],
    [
        "Pipeline memecah tugas menjadi tahap, end-to-end memetakan masukan ke keluaran langsung.",
        "End-to-end butuh banyak pasangan lengkap, pipeline memanfaatkan data per tahap.",
        "Pilih komponen yang punya banyak data berlabel dan tugas sederhana.",
        "Putuskan lewat perbandingan empiris pada beberapa ukuran data.",
    ],
    ["Machine Learning Yearning, bab 47 sampai 51 (Andrew Ng): end-to-end learning dan memilih komponen pipeline"],
)

l3 = lesson(
    "D11-08-3",
    "Error analysis per komponen dan pipeline yang cacat",
    35,
    [
        "Menghitung atribusi error ke komponen pipeline dengan mengganti keluaran komponen",
        "Menyusun tabel atribusi dan memilih komponen yang layak diperbaiki",
        "Membandingkan tiap komponen dengan performa manusia pada masukan yang sama",
        "Mengenali pipeline yang cacat dari komponen yang sudah setara manusia tetapi hasil akhir buruk",
    ],
    [
        T("""
        ## Dari error sistem ke error komponen

        Pada pipeline A, B, C, error akhir bisa berasal dari tahap mana pun. Error analysis per komponen menjawab pertanyaan: dari kesalahan akhir, berapa persen disebabkan A, berapa persen B, dan berapa persen C? Jawabannya menentukan komponen mana yang pantas diperbaiki lebih dulu.

        Caranya menggunakan substitusi keluaran. Untuk tiap contoh dev yang salah, ganti keluaran komponen A dengan keluaran yang benar (dari label manusia), lalu jalankan B dan C seperti biasa. Jika hasil akhir menjadi benar, kesalahan itu diatribusikan ke A. Jika masih salah, ganti keluaran A dan B dengan yang benar. Jika sekarang benar, atribusinya ke B. Jika masih salah, atribusinya ke C.

        Karena substitusi dilakukan berurutan dan kumulatif, tiap contoh salah mendapat tepat satu atribusi: komponen paling awal yang jika diperbaiki membuat hasil akhir benar.
        """),
        T("""
        ## Tabel atribusi

        Hasilnya berupa tabel. Misalkan dari 100 contoh dev yang salah: 45 diatribusikan ke A, 35 ke B, 20 ke C. Maka komponen A menjadi kandidat prioritas karena perbaikannya paling banyak menghilangkan kesalahan, dengan batas atas 45 persen. Seperti error analysis sebelumnya, angka ini adalah plafon, bukan janji.

        Atribusi bergantung pada urutan substitusi. Karena kita mengganti dari hulu ke hilir, kesalahan yang bisa diperbaiki lewat A maupun B akan dihitung ke A. Itu wajar jika kamu memang ingin menghitung komponen paling awal yang menyebabkan kegagalan. Untuk pipeline dengan banyak percabangan, ikuti urutan data mengalir.

        Satu hal yang perlu diwaspadai: substitusi keluaran yang benar memerlukan label perantara. Jika tahap perantara tidak punya label benar, kamu bisa meminta manusia melabeli contoh salah itu saja, sekitar seratus contoh.
        """),
        T("""
        ## Membandingkan dengan performa manusia

        Atribusi memberi tahu seberapa besar tiap komponen menyumbang kesalahan, tetapi tidak menjawab seberapa jauh komponen itu bisa diperbaiki. Untuk itu, bandingkan tiap komponen dengan performa manusia pada tugas komponen tersebut. Beri manusia masukan yang sama dengan yang diterima komponen dan ukur errornya.

        Misalkan komponen A salah 15 persen sementara manusia 1 persen: ada ruang 14 poin. Komponen B salah 4 persen dan manusia 2 persen: ruang 2 poin. Prioritaskan A. Untuk komponen yang sudah dekat manusia, tenaga lebih baik dialihkan.

        Hati-hati ketika masukan komponen berasal dari keluaran komponen sebelumnya yang bisa salah. Untuk perbandingan yang adil, berikan manusia masukan yang sama persis dengan yang diterima komponen, termasuk keluaran sebelumnya yang cacat. Dengan begitu kamu mengukur kesulitan komponen itu sendiri.
        """),
        T("""
        ## Mendeteksi pipeline yang cacat

        Bayangkan semua komponen sudah berkinerja setara manusia pada tugasnya masing-masing, tetapi sistem keseluruhan masih jauh di bawah manusia. Itu tanda pipeline cacat: rancangan komponennya membuang informasi yang diperlukan untuk jawaban akhir, atau urutan tahap tidak memadai.

        Contoh: sistem memprediksi apakah seorang pengemudi akan berhenti di lampu merah, dengan pipeline yang mendeteksi lampu, mendeteksi warna, dan memprediksi aksi. Jika komponen akhir hanya menerima warna lampu tanpa kecepatan kendaraan atau jarak, bahkan manusia yang hanya diberi warna lampu akan sering salah. Setiap komponen sempurna, tetapi informasi yang diteruskan tidak cukup.

        Perbaikannya mengubah rancangan: teruskan informasi tambahan ke tahap akhir, tambah tahap yang hilang, atau ganti dengan end-to-end yang mengakses seluruh masukan. Tidak ada jumlah penyetelan komponen yang akan membereskan masalah desain.
        """),
        T("""
        ## Langkah praktis menjalankan analisis

        Mulailah dengan mengambil seratus sampai dua ratus contoh dev yang salah. Untuk tiap contoh, catat keluaran asli tiap komponen dan keluaran yang seharusnya, yang kamu dapat dari label manusia atau dari pelabelan tambahan. Jalankan substitusi berurutan secara otomatis dengan skrip kecil agar bisa diulang setiap kali sistem berubah.

        Simpan hasilnya dalam spreadsheet dengan satu kolom per komponen. Ulangi analisis setelah tiap perbaikan besar, karena komponen yang tadinya kecil kontribusinya bisa menjadi penyebab utama setelah komponen lain membaik.
        """),
        K(
            "warning",
            """
            Atribusi ke komponen hanya valid bila substitusi keluaran benar-benar memperbaiki hasil akhir. Jika kamu mengganti keluaran A dan hasil akhir tetap salah padahal B dan C sempurna, curigai rancangan pipeline, bukan komponen.
            """,
            title="Hati-hati atribusi",
        ),
        C(
            """
def atribusi(fix_a, fix_ab):
    if fix_a:
        return "A"
    if fix_ab:
        return "B"
    return "C"

salah = [(True, True), (False, True), (False, False), (False, True), (True, True), (False, False)]
hasil = {"A": 0, "B": 0, "C": 0}
for fa, fab in salah:
    hasil[atribusi(fa, fab)] += 1
total = len(salah)
print({k: round(v / total, 4) for k, v in hasil.items()})
""",
            """
            {'A': 0.3333, 'B': 0.3333, 'C': 0.3333}
            """,
            """
            Enam contoh salah, masing-masing mendapat satu atribusi lewat substitusi kumulatif. Dua ke A, dua ke B, dua ke C. Tabel yang sama untuk ratusan contoh menunjukkan komponen prioritas.
            """,
            filename="atribusi.py",
        ),
        C(
            """
import numpy as np

def simulasi(n, pa, pb, pc, seed):
    r = np.random.default_rng(seed)
    a = r.random(n) < pa
    b = r.random(n) < pb
    c = r.random(n) < pc
    gagal = a | b | c
    ke_a = a & gagal
    ke_b = (~a) & b
    ke_c = (~a) & (~b) & c
    t = gagal.sum()
    return round(ke_a.sum() / t, 4), round(ke_b.sum() / t, 4), round(ke_c.sum() / t, 4)

print(simulasi(200000, 0.10, 0.05, 0.03, 0))
pa, pb, pc = 0.10, 0.05, 0.03
w = [pa, (1 - pa) * pb, (1 - pa) * (1 - pb) * pc]
print([round(x / sum(w), 4) for x in w])
""",
            """
            simulasi: (0.5887, 0.2606, 0.1507)
            teoretis: [0.586, 0.2637, 0.1503]
            """,
            """
            Tiga komponen dengan laju gagal 10, 5, dan 3 persen. Atribusi mengikuti komponen paling awal yang gagal, sehingga komponen hulu menanggung bagian terbesar meski laju gagal komponen lain tidak jauh berbeda. Simulasi dan rumus teoretis hampir identik.
            """,
            filename="simulasi_atribusi.py",
        ),
        C(
            """
manusia = {"A": 0.01, "B": 0.02, "C": 0.01}
sistem = {"A": 0.15, "B": 0.04, "C": 0.03}
celah = {k: round(sistem[k] - manusia[k], 4) for k in manusia}
print(celah)
print("prioritas:", max(celah, key=lambda k: (celah[k], k)))
""",
            """
            {'A': 0.14, 'B': 0.02, 'C': 0.02}
            prioritas: A
            """,
            """
            Selisih tiap komponen terhadap manusia menunjukkan ruang perbaikan. Komponen A punya celah 14 poin sehingga menjadi prioritas, sedangkan B dan C sudah dekat manusia.
            """,
            filename="celah_manusia.py",
        ),
        E(
            "D11-08-3-ex1",
            "mudah",
            """
            Tulis fungsi `atribusi(fix_a, fix_ab)` yang mengembalikan `"A"` bila `fix_a` benar, `"B"` bila `fix_a` salah tetapi `fix_ab` benar, dan `"C"` selainnya.
            """,
            """
            def atribusi(fix_a, fix_ab):
                # TODO: implementasikan
                pass
            """,
            """
            assert atribusi(True, True) == "A"
            assert atribusi(False, True) == "B"
            assert atribusi(False, False) == "C"
            assert atribusi(True, False) == "A"
            """,
            "Periksa A lebih dulu, lalu B, dan sisanya C.",
            """
            def atribusi(fix_a, fix_ab):
                if fix_a:
                    return "A"
                if fix_ab:
                    return "B"
                return "C"
            """,
            names=[
                ("Diperbaiki oleh A", "Substitusi A cukup untuk memperbaiki"),
                ("Diperbaiki oleh B", "Substitusi A dan B diperlukan"),
                ("Hanya C", "Masih salah setelah A dan B diganti"),
                ("A menang urutan", "A didahulukan saat kedua benar"),
            ],
        ),
        E(
            "D11-08-3-ex2",
            "sedang",
            """
            Tulis fungsi `fraksi_teoretis(pa, pb, pc)` yang menghitung bobot `wA = pa`, `wB = (1 - pa) * pb`, `wC = (1 - pa) * (1 - pb) * pc`, lalu mengembalikan tuple fraksi `(wA / total, wB / total, wC / total)` dibulatkan 4 desimal dengan `total = wA + wB + wC`.
            """,
            """
            def fraksi_teoretis(pa, pb, pc):
                # TODO: implementasikan
                pass
            """,
            """
            assert fraksi_teoretis(0.10, 0.05, 0.03) == (0.586, 0.2637, 0.1503)
            assert fraksi_teoretis(0.5, 0.0, 0.0) == (1.0, 0.0, 0.0)
            assert fraksi_teoretis(0.0, 0.5, 0.0) == (0.0, 1.0, 0.0)
            assert sum(fraksi_teoretis(0.2, 0.2, 0.2)) > 0.9999
            """,
            "Hitung tiga bobot, jumlahkan, lalu bagi satu per satu dan bulatkan.",
            """
            def fraksi_teoretis(pa, pb, pc):
                wa = pa
                wb = (1 - pa) * pb
                wc = (1 - pa) * (1 - pb) * pc
                t = wa + wb + wc
                return round(wa / t, 4), round(wb / t, 4), round(wc / t, 4)
            """,
        ),
        E(
            "D11-08-3-ex3",
            "sedang",
            """
            Tulis fungsi `komponen_prioritas(sistem, manusia)` yang menerima dua dictionary nama komponen ke error. Hitung celah `sistem[k] - manusia[k]` dibulatkan 4 desimal dan kembalikan nama komponen dengan celah terbesar. Jika seri pilih nama yang paling awal secara abjad.
            """,
            """
            def komponen_prioritas(sistem, manusia):
                # TODO: implementasikan
                pass
            """,
            """
            assert komponen_prioritas({"A": 0.15, "B": 0.04, "C": 0.03}, {"A": 0.01, "B": 0.02, "C": 0.01}) == "A"
            assert komponen_prioritas({"A": 0.05, "B": 0.05}, {"A": 0.01, "B": 0.01}) == "A"
            assert komponen_prioritas({"X": 0.1, "Y": 0.3}, {"X": 0.0, "Y": 0.25}) == "X"
            assert komponen_prioritas({"X": 0.1}, {"X": 0.1}) == "X"
            """,
            "Gunakan min dengan key tuple (-celah, nama) agar seri jatuh ke abjad.",
            """
            def komponen_prioritas(sistem, manusia):
                celah = {k: round(sistem[k] - manusia[k], 4) for k in sistem}
                return min(celah, key=lambda k: (-celah[k], k))
            """,
        ),
        E(
            "D11-08-3-ex4",
            "menantang",
            """
            Tulis fungsi `simulasi_atribusi(n, pa, pb, pc, seed)`. Pakai `r = np.random.default_rng(seed)` lalu tarik berurutan `a = r.random(n) < pa`, `b = r.random(n) < pb`, `c = r.random(n) < pc`. Contoh gagal adalah `a | b | c`. Atribusi ke A bila `a` benar, ke B bila `a` salah dan `b` benar, ke C bila keduanya salah dan `c` benar. Kembalikan tuple fraksi `(A, B, C)` di antara contoh gagal, dibulatkan 4 desimal.
            """,
            """
            import numpy as np

            def simulasi_atribusi(n, pa, pb, pc, seed):
                # TODO: implementasikan
                pass
            """,
            """
            a, b, c = simulasi_atribusi(200000, 0.10, 0.05, 0.03, 0)
            assert abs(a - 0.586) < 0.01
            assert abs(b - 0.2637) < 0.01
            assert abs(c - 0.1503) < 0.01
            assert abs(a + b + c - 1.0) < 0.001
            assert simulasi_atribusi(1000, 0.1, 0.1, 0.1, 2) == simulasi_atribusi(1000, 0.1, 0.1, 0.1, 2)
            """,
            "Gunakan operasi boolean NumPy. Bagi tiap hitungan dengan jumlah contoh gagal.",
            """
            import numpy as np

            def simulasi_atribusi(n, pa, pb, pc, seed):
                r = np.random.default_rng(seed)
                a = r.random(n) < pa
                b = r.random(n) < pb
                c = r.random(n) < pc
                gagal = a | b | c
                t = gagal.sum()
                ke_a = (a & gagal).sum()
                ke_b = ((~a) & b).sum()
                ke_c = ((~a) & (~b) & c).sum()
                return round(float(ke_a / t), 4), round(float(ke_b / t), 4), round(float(ke_c / t), 4)
            """,
        ),
    ],
    [
        M(
            "Memperbaiki komponen yang laju gagalnya tampak paling tinggi tanpa atribusi.",
            "Ganti keluaran komponen dengan yang benar secara berurutan dan hitung atribusinya.",
        ),
        M(
            "Membandingkan komponen dengan manusia tanpa memberi masukan yang sama.",
            "Beri manusia masukan persis seperti yang diterima komponen.",
        ),
        M(
            "Terus menyetel komponen ketika semuanya sudah setara manusia tetapi hasil akhir buruk.",
            "Curigai rancangan pipeline dan ubah aliran informasinya.",
        ),
    ],
    [
        Q(
            "Setelah keluaran A diganti dengan yang benar, hasil akhir menjadi benar. Atribusi?",
            ["A", "B", "C", "Pipeline"],
            0,
            "Komponen paling awal yang jika diperbaiki membuat hasil benar adalah A.",
            hint="Aturan: komponen paling awal yang memperbaiki hasil.",
        ),
        Q(
            "Atribusi 45 ke A, 35 ke B, 20 ke C. Prioritas awal?",
            ["A", "B", "C", "Tidak jelas"],
            0,
            "A punya batas atas manfaat terbesar yaitu 45 persen.",
            hint="Lihat angka terbesar.",
        ),
        Q(
            "Mengapa membandingkan dengan manusia selain atribusi?",
            ["Menggantikan atribusi", "Mengetahui seberapa banyak ruang perbaikan komponen", "Mengganti dev set", "Mengurangi data"],
            1,
            "Atribusi menunjukkan sumbangan error, perbandingan manusia menunjukkan seberapa bisa diperbaiki.",
            hint="Satu mengukur kontribusi, yang lain mengukur potensi.",
        ),
        Q(
            "Semua komponen setara manusia tetapi sistem buruk. Dugaan utama?",
            ["Kurang data", "Pipeline cacat karena informasi penting hilang antar tahap", "Dev set salah", "Metrik salah"],
            1,
            "Komponen sempurna tidak cukup bila informasi yang diteruskan kurang.",
            hint="Informasi apa yang sampai ke tahap akhir?",
        ),
        Q(
            "Mengapa manusia diberi masukan yang sama persis dengan komponen?",
            ["Agar lebih cepat", "Agar perbandingan adil terhadap kesulitan komponen itu sendiri", "Agar manusia salah", "Tidak perlu"],
            1,
            "Masukan yang berbeda mengukur tugas yang berbeda.",
            hint="Perbandingan adil perlu masukan yang sama.",
        ),
    ],
    [
        "Atribusi error dilakukan dengan mengganti keluaran komponen berurutan dengan yang benar.",
        "Tabel atribusi memberi batas atas manfaat memperbaiki tiap komponen.",
        "Bandingkan tiap komponen dengan manusia pada masukan yang sama untuk mengukur ruang perbaikan.",
        "Komponen setara manusia dengan hasil buruk menandakan pipeline cacat.",
    ],
    ["Machine Learning Yearning, bab 52 sampai 58 (Andrew Ng): error analysis per komponen dan pipeline yang cacat"],
)

video = {
    "needed": True,
    "kind": "ai_slides",
    "reason": "Substitusi keluaran berurutan dan tabel atribusi lebih jelas lewat diagram aliran bertahap.",
    "brief": [
        "Slide 1: diagram pipeline A ke B ke C dengan label keluaran perantara",
        "Slide 2: animasi substitusi keluaran benar pada A lalu A dan B",
        "Slide 3: tabel atribusi 45, 35, 20 persen dan tabel celah terhadap manusia",
        "Slide 4: contoh pipeline cacat dengan informasi hilang di tahap akhir",
    ],
}

write_module(
    "D11",
    8,
    "Pipeline, end-to-end, dan atribusi error",
    105,
    [
        "Memakai tes verifikasi untuk memisahkan kegagalan pencarian dari fungsi skor",
        "Memilih antara pipeline dan end-to-end berdasarkan data dan kesederhanaan tugas",
        "Mengatribusikan error ke komponen dan mendeteksi pipeline yang cacat",
    ],
    [l1, l2, l3],
    video,
    REF,
)
