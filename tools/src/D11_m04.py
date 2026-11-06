import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, C, E, Q, M, lesson, write_module

REF = [{"book": "Machine Learning Yearning (Andrew Ng)", "chapters": "bab 16 sampai 19"}]

l1 = lesson(
    "D11-04-1",
    "Membersihkan label yang salah di dev dan test set",
    35,
    [
        "Menghitung berapa bagian error dev set yang berasal dari label salah",
        "Memutuskan kapan label salah layak dibersihkan dan kapan boleh diabaikan",
        "Membedakan efek noise acak dan noise sistematis pada training set",
        "Menjelaskan mengapa koreksi hanya pada contoh yang salah menimbulkan bias",
    ],
    [
        T("""
        ## Ketika labelnya yang keliru

        Saat melakukan error analysis pada klasifikasi kucing, kamu mungkin menemukan bahwa sebagian contoh dev set yang dianggap salah sebenarnya tidak salah. Penyebabnya label manusia yang keliru: gambar yang berisi kucing diberi label bukan kucing, atau sebaliknya. Pertanyaannya, apakah label yang salah itu layak ditambahkan ke daftar kategori di tabel error analysis dan diperbaiki?

        Jawabannya bergantung pada seberapa besar pengaruhnya terhadap kemampuanmu menilai sistem. Hal penting yang perlu dipahami: label yang salah di training set umumnya tidak terlalu berbahaya, dan label yang salah di dev atau test set baru menjadi masalah jika jumlahnya cukup besar untuk mengacaukan keputusan.

        Dua kondisi ini harus dibedakan. Di training set, algoritma belajar dari banyak contoh sehingga kesalahan acak yang kecil cenderung teredam. Di dev dan test set, kamu memakai angka error sebagai penunjuk arah. Jika penunjuk itu bergeser karena label yang salah, kamu bisa memilih model yang sebenarnya lebih buruk.
        """),
        T("""
        ## Seberapa besar bagian error yang berasal dari label salah

        Misalkan error dev set 10 persen dan kamu menemukan bahwa 0,6 persen dari seluruh contoh dev memiliki label yang salah. Bagian error akibat label adalah 0,6 persen dibagi 10 persen, yaitu 6 persen dari semua kesalahan. Memperbaiki label hanya menurunkan error terukur dari 10 persen ke sekitar 9,4 persen. Itu kecil dibanding masalah lain yang mungkin lebih menjanjikan, sehingga kamu boleh menundanya.

        Sekarang bayangkan sistem sudah jauh lebih baik dengan error 2 persen. Dengan 0,6 persen label salah yang sama, bagian error akibat label naik menjadi 0,6 dibagi 2, yaitu 30 persen. Hampir sepertiga kesalahan terukur kini bukan kesalahan model sama sekali. Perbaikan model sebesar 0,1 poin persen akan tenggelam dalam derau label sehingga sulit dibedakan dari fluktuasi.

        Pelajarannya: label salah yang sama bisa tidak penting pada awal proyek dan menjadi sangat penting di akhir. Karena itu, hitung bagian ini sebagai satu kolom lagi di tabel error analysis dari lesson sebelumnya, dan perbarui hitungan ketika error model berubah.
        """),
        T("""
        ## Aturan keputusan dan cara memperbaiki

        Pertanyaan ujinya adalah apakah label yang salah menghalangimu menilai mana dari dua model yang lebih baik. Jika perbedaan error antar model yang sedang kamu bandingkan lebih kecil dari bagian error akibat label, hasil dev set tidak lagi bisa dipercaya dan pembersihan label layak dilakukan.

        Jika kamu memutuskan memperbaiki label dev set, ikuti beberapa pedoman. Pertama, terapkan proses yang sama pada dev dan test set sehingga keduanya tetap berasal dari distribusi yang sama. Kedua, pertimbangkan memeriksa contoh yang algoritmamu klasifikasikan dengan benar, bukan hanya yang salah. Mungkin label asli dan prediksi sama-sama keliru, dan jika kamu hanya memperbaiki contoh yang salah, kamu menambahkan bias ke estimasi: contoh yang prediksinya sama dengan label keliru tetap dihitung benar. Memeriksa yang benar memakan waktu jauh lebih lama karena jumlahnya jauh lebih banyak, sehingga sering tidak dilakukan. Jika error classifier hanya 2 persen, memeriksa 98 persen sisanya jauh lebih mahal.

        Ketiga, boleh saja training set tidak ikut dibersihkan sehingga distribusinya sedikit berbeda dari dev dan test. Itu masih aman dan sering lebih efisien, karena mempelajari data yang agak berbeda tetap berguna.
        """),
        T("""
        ## Noise acak melawan noise sistematis

        Algoritma pembelajaran cukup tahan terhadap kesalahan acak di training set. Jika label dibalik secara acak dan independen dari fitur, model tetap belajar pola utama karena kesalahan itu saling meniadakan. Hasilnya turun sedikit saja walau beberapa persen label salah.

        Kesalahan sistematis lain ceritanya. Misalkan pelabel selalu menandai anjing berbulu putih sebagai kucing. Kesalahan itu punya pola yang bisa dipelajari, sehingga model ikut mempelajarinya sebagai kebenaran. Karena itu perlu dibedakan label yang salah karena kelalaian acak dan label yang salah karena kebiasaan atau instruksi pelabelan yang keliru. Jenis kedua perlu dicari penyebabnya, bukan hanya dikoreksi satu per satu.

        Rumus terukur untuk noise acak simetris dengan laju η dan error asli e adalah `e * (1 - η) + (1 - e) * η`. Suku pertama adalah kesalahan model yang labelnya benar. Suku kedua adalah prediksi yang benar tetapi labelnya salah sehingga tampak keliru. Rumus ini menjelaskan mengapa error yang terukur lebih besar dari error sebenarnya ketika e kecil.
        """),
        K(
            "warning",
            """
            Jangan hanya mengoreksi contoh yang diklasifikasikan salah lalu mengukur ulang error. Contoh yang prediksinya cocok dengan label keliru tetap dianggap benar, sehingga error terukur menjadi terlalu optimis.
            """,
        ),
        C(
            """
for err in [0.10, 0.02]:
    label_salah = 0.006
    bagian = label_salah / err
    print(f"error dev {err:.0%}: bagian akibat label {bagian:.0%}, error setelah label dibersihkan {err - label_salah:.3f}")
""",
            """
            error dev 10%: bagian akibat label 6%, error setelah label dibersihkan 0.094
            error dev 2%: bagian akibat label 30%, error setelah label dibersihkan 0.014
            """,
            """
            Label salah yang sama, 0,6 persen, menjadi 6 persen kesalahan saat error 10 persen tetapi 30 persen saat error 2 persen. Prioritas pembersihan label naik seiring model membaik.
            """,
        ),
        C(
            """
import numpy as np
from sklearn.linear_model import LogisticRegression

rng = np.random.default_rng(0)
def data(m):
    X = rng.normal(size=(m, 5))
    y = (X[:, 0] + 0.8 * X[:, 1] - 0.5 * X[:, 2] + 0.3 * rng.normal(size=m) > 0).astype(int)
    return X, y

X, y = data(6000)
Xd, yd = data(3000)
print("training bersih      :", round(LogisticRegression().fit(X, y).score(Xd, yd), 3))
for eta in [0.05, 0.10, 0.20]:
    flip = rng.random(len(y)) < eta
    yn = np.where(flip, 1 - y, y)
    print(f"noise acak {eta:.0%}       :", round(LogisticRegression().fit(X, yn).score(Xd, yd), 3))
yn = y.copy()
yn[(X[:, 0] > 1) & (y == 1)] = 0
print("noise sistematis 15% :", round(LogisticRegression().fit(X, yn).score(Xd, yd), 3))
""",
            """
            training bersih 0.937
            noise acak 5%, 10%, 20% sekitar 0.934 sampai 0.937
            noise sistematis 15% sekitar 0.757
            """,
            """
            Label acak yang dibalik sampai 20 persen hampir tidak menurunkan akurasi pada dev yang bersih. Noise sistematis yang sebagian pola dibalik menjatuhkan akurasi sekitar 18 poin. Inilah perbedaan antara derau yang diredam dan bias yang dipelajari.
            """,
        ),
        C(
            """
def terukur(e, eta):
    return e * (1 - eta) + (1 - e) * eta

for e in [0.10, 0.02]:
    print(f"error asli {e:.2f}, label salah 1%: terukur {terukur(e, 0.01):.4f}")
""",
            """
            error asli 0.10, label salah 1%: terukur 0.1080
            error asli 0.02, label salah 1%: terukur 0.0296
            """,
            """
            Pada error asli 2 persen, label salah 1 persen membuat error terukur 2,96 persen, naik hampir 50 persen secara relatif. Pada error asli 10 persen, kenaikannya hanya 8 persen secara relatif.
            """,
        ),
        E(
            "D11-04-1-ex1",
            "mudah",
            """
            Tulis fungsi `fraksi_error_label(err_total, frac_label_salah)` yang mengembalikan bagian kesalahan yang berasal dari label salah, yaitu `frac_label_salah / err_total`, dibulatkan 4 desimal.
            """,
            """
            def fraksi_error_label(err_total, frac_label_salah):
                # TODO: implementasikan
                pass
            """,
            """
            assert fraksi_error_label(0.10, 0.006) == 0.06
            assert fraksi_error_label(0.02, 0.006) == 0.3
            assert fraksi_error_label(0.05, 0.0) == 0.0
            """,
            "Bagi frac_label_salah dengan err_total lalu bulatkan dengan round(..., 4).",
            """
            def fraksi_error_label(err_total, frac_label_salah):
                return round(frac_label_salah / err_total, 4)
            """,
        ),
        E(
            "D11-04-1-ex2",
            "sedang",
            """
            Tulis fungsi `perlu_bersihkan(err_total, frac_label_salah, ambang)` yang mengembalikan `True` bila bagian kesalahan akibat label salah (`frac_label_salah / err_total`) lebih besar atau sama dengan `ambang`, dan `False` selainnya. Jika `err_total <= 0` kembalikan `False`.
            """,
            """
            def perlu_bersihkan(err_total, frac_label_salah, ambang):
                # TODO: implementasikan
                pass
            """,
            """
            assert perlu_bersihkan(0.10, 0.006, 0.25) is False
            assert perlu_bersihkan(0.02, 0.006, 0.25) is True
            assert perlu_bersihkan(0.02, 0.005, 0.25) is True
            assert perlu_bersihkan(0.0, 0.01, 0.25) is False
            """,
            "Tangani err_total nol atau negatif lebih dulu, lalu bandingkan rasio dengan ambang.",
            """
            def perlu_bersihkan(err_total, frac_label_salah, ambang):
                if err_total <= 0:
                    return False
                return bool(frac_label_salah / err_total >= ambang)
            """,
        ),
        E(
            "D11-04-1-ex3",
            "sedang",
            """
            Tulis fungsi `error_terukur(e, eta)` untuk noise acak simetris: `e * (1 - eta) + (1 - e) * eta`, dibulatkan 6 desimal.
            """,
            """
            def error_terukur(e, eta):
                # TODO: implementasikan
                pass
            """,
            """
            assert error_terukur(0.02, 0.01) == 0.0296
            assert error_terukur(0.10, 0.0) == 0.1
            assert error_terukur(0.5, 0.2) == 0.5
            assert error_terukur(0.0, 0.1) == 0.1
            """,
            "Terapkan rumus langsung lalu round(nilai, 6).",
            """
            def error_terukur(e, eta):
                return round(e * (1 - eta) + (1 - e) * eta, 6)
            """,
        ),
        E(
            "D11-04-1-ex4",
            "menantang",
            """
            Simulasikan bias dari koreksi yang hanya menyentuh contoh salah. Tulis `koreksi_hanya_salah(n, e, eta, seed)`. Pakai `rng = np.random.default_rng(seed)`. Buat label benar `y = rng.integers(0, 2, n)`. Prediksi `pred = np.where(rng.random(n) < e, 1 - y, y)`. Label teramati `y_obs = np.where(rng.random(n) < eta, 1 - y, y)`. Error sebelum koreksi adalah `mean(pred != y_obs)`. Koreksi hanya contoh dengan `pred != y_obs` dengan mengganti label teramati menjadi label benar `y`, lalu hitung `mean(pred != y_baru)`. Kembalikan tuple `(sebelum, sesudah)` dibulatkan 4 desimal.
            """,
            """
            import numpy as np

            def koreksi_hanya_salah(n, e, eta, seed):
                # TODO: implementasikan
                pass
            """,
            """
            sebelum, sesudah = koreksi_hanya_salah(200000, 0.10, 0.05, 0)
            assert abs(sebelum - 0.14) < 0.005
            assert abs(sesudah - 0.095) < 0.005
            assert sesudah < 0.10
            assert koreksi_hanya_salah(1000, 0.1, 0.05, 3) == koreksi_hanya_salah(1000, 0.1, 0.05, 3)
            """,
            "Urutan penarikan acak penting: y, lalu pred, lalu y_obs. Label baru dibuat dengan np.where(pred != y_obs, y, y_obs).",
            """
            import numpy as np

            def koreksi_hanya_salah(n, e, eta, seed):
                rng = np.random.default_rng(seed)
                y = rng.integers(0, 2, n)
                pred = np.where(rng.random(n) < e, 1 - y, y)
                y_obs = np.where(rng.random(n) < eta, 1 - y, y)
                sebelum = float(np.mean(pred != y_obs))
                y_baru = np.where(pred != y_obs, y, y_obs)
                sesudah = float(np.mean(pred != y_baru))
                return round(sebelum, 4), round(sesudah, 4)
            """,
        ),
    ],
    [
        M(
            "Membersihkan label tanpa menghitung dulu seberapa besar bagian error yang berasal dari label.",
            "Hitung bagian error akibat label salah dan bandingkan dengan perbedaan antar model.",
        ),
        M(
            "Membersihkan label dev set tetapi tidak test set.",
            "Terapkan proses pembersihan yang sama pada dev dan test agar distribusinya tetap sama.",
        ),
        M(
            "Menyamakan noise acak dengan noise sistematis.",
            "Noise acak teredam oleh algoritma, noise sistematis dipelajari sebagai pola dan harus dicari sumbernya.",
        ),
    ],
    [
        Q(
            "Error dev 2 persen dan 0,6 persen contoh berlabel salah. Berapa bagian error akibat label?",
            ["6 persen", "30 persen", "0,6 persen", "60 persen"],
            1,
            "0,6 dibagi 2 sama dengan 0,3, yaitu 30 persen dari semua kesalahan.",
        ),
        Q(
            "Mengapa label salah acak di training set biasanya tidak terlalu berbahaya?",
            ["Karena training set selalu bersih", "Karena algoritma meredam kesalahan acak yang saling meniadakan", "Karena label tidak dipakai", "Karena dev set menimpanya"],
            1,
            "Kesalahan acak tidak punya pola yang bisa dipelajari, sehingga pengaruhnya kecil.",
        ),
        Q(
            "Label dev set diperbaiki. Apa yang harus dilakukan pada test set?",
            ["Dibiarkan", "Diproses sama agar dev dan test tetap satu distribusi", "Dihapus", "Digabung ke training"],
            1,
            "Dev dan test harus berasal dari distribusi yang sama.",
        ),
        Q(
            "Mengapa hanya memperbaiki contoh yang salah klasifikasi menimbulkan bias?",
            ["Karena terlalu cepat", "Karena contoh yang prediksinya sama dengan label keliru tetap dianggap benar", "Karena mengubah training", "Karena menaikkan error"],
            1,
            "Kesalahan label pada contoh yang tampak benar tidak tersentuh, sehingga error terukur terlalu optimis.",
        ),
        Q(
            "Pelabel selalu menandai anjing putih sebagai kucing. Jenis noise apa itu?",
            ["Acak", "Sistematis, sehingga model bisa ikut mempelajarinya", "Tidak berpengaruh", "Hanya di test set"],
            1,
            "Pola yang konsisten bisa dipelajari model, sehingga sumbernya harus dicari dan diperbaiki.",
        ),
    ],
    [
        "Bagian error akibat label salah sama dengan fraksi label salah dibagi error total.",
        "Label salah yang sama makin penting seiring error model mengecil.",
        "Perlakukan dev dan test sama, dan jangan hanya mengoreksi contoh yang diklasifikasikan salah.",
        "Noise acak teredam, noise sistematis dipelajari model dan harus dicari sumbernya.",
    ],
    ["Machine Learning Yearning, bab 16 (Andrew Ng): memperbaiki contoh dev dan test yang berlabel salah"],
)

l2 = lesson(
    "D11-04-2",
    "Eyeball dev set dan Blackbox dev set",
    35,
    [
        "Menjelaskan alasan membagi dev set menjadi Eyeball dan Blackbox",
        "Memakai selisih error eyeball dan blackbox untuk mendeteksi overfit ke dev set",
        "Menghitung berapa kesalahan yang diharapkan berada di eyeball dev set",
        "Mensimulasikan efek memilih model terbaik dari banyak kandidat pada satu dev set",
    ],
    [
        T("""
        ## Dev set yang terlalu sering dilihat

        Misalkan dev set berisi 5.000 contoh dan sistemmu salah pada 20 persen, yaitu 1.000 contoh. Memeriksa seribu contoh secara manual terlalu lama. Kamu mungkin memeriksa sebagian saja, misalnya 100 sampai 500 contoh, untuk error analysis.

        Masalah muncul dari kebiasaan melihat dev set berulang kali. Setiap kali kamu mempelajari contoh yang salah, kamu mendapat ide fitur atau aturan yang cocok dengan contoh-contoh itu. Dengan banyak putaran, model lama-lama menyesuaikan diri dengan dev set secara halus. Kamu overfit ke dev set lewat dirimu sendiri, bukan lewat algoritma.

        Solusinya membelah dev set menjadi dua bagian. **Eyeball dev set** boleh kamu lihat dan analisis manual. **Blackbox dev set** tidak boleh dilihat satu contoh pun. Blackbox dipakai hanya untuk mengukur error, memilih model, dan menyetel hyperparameter. Karena tidak pernah dilihat manusia, ia tidak ikut menyesuaikan diri dengan intuisimu.
        """),
        T("""
        ## Membaca selisih eyeball dan blackbox

        Setelah dua bagian itu ada, kamu mendapat alat deteksi overfit yang sederhana. Bandingkan error pada eyeball dan blackbox. Jika performa pada eyeball jauh lebih baik daripada pada blackbox, kamu sudah overfit ke eyeball dev set. Saat itu, buang eyeball lama dan buat yang baru, misalnya dengan memindahkan sebagian contoh blackbox ke eyeball atau mengumpulkan data berlabel baru.

        Hal ini membuat blackbox berfungsi sebagai pengukur jujur kemajuan. Selama error blackbox terus turun seiring perbaikanmu, kemajuan itu nyata. Bila error eyeball turun tetapi blackbox mendatar, kamu hanya menghafal contoh yang kamu lihat.

        Hubungannya dengan test set: blackbox adalah bagian dev set dan tetap dipakai untuk memilih model, sehingga tidak menggantikan test set. Test set tetap disimpan untuk estimasi akhir yang tidak pernah dipakai mengambil keputusan.
        """),
        T("""
        ## Dari mana derau seleksi berasal

        Ada alasan statistik yang jelas mengapa error terbaik di dev set cenderung terlalu optimis. Bayangkan kamu mencoba lima puluh variasi model yang sebenarnya sama baiknya, semuanya dengan error sejati 20 persen. Pada dev set berukuran terbatas, error terukur tiap model bergoyang di sekitar 20 persen karena derau sampling. Jika kamu memilih yang terendah, kamu hampir pasti memilih model yang kebetulan beruntung pada dev set itu. Error terukurnya mungkin 15 persen padahal error sejatinya tetap 20 persen.

        Ini disebut winner's curse atau bias seleksi. Makin banyak kandidat dan makin kecil dev set, makin besar optimisme itu. Blackbox dev set yang tidak dipakai memilih tidak terkena bias tersebut, sehingga error blackbox model terpilih tetap sekitar 20 persen. Selisih keduanya mengukur seberapa besar kamu tertipu.
        """),
        T("""
        ## Berapa kesalahan yang diharapkan ada di eyeball

        Jumlah kesalahan yang bisa kamu pelajari di eyeball sama dengan ukuran eyeball dikali error. Dari dev set 5.000 contoh dengan error 20 persen, eyeball 500 contoh berisi sekitar 100 kesalahan, jumlah yang pas untuk error analysis. Blackbox 4.500 contoh sisanya berisi sekitar 900 kesalahan yang tidak pernah kamu lihat satu per satu.

        Kalau error model turun menjadi 5 persen, eyeball 500 contoh hanya berisi sekitar 25 kesalahan. Itu terlalu sedikit untuk gambaran yang meyakinkan, sehingga eyeball perlu diperbesar. Lesson berikutnya membahas ukuran yang disarankan dengan lebih rinci.
        """),
        T("""
        ## Aturan main yang menjaga blackbox tetap jujur

        Blackbox hanya berguna selama disiplin menjaganya. Beberapa aturan sederhana membantu tim. Pertama, tulis di dokumen tim bahwa blackbox tidak boleh dibuka contohnya, hanya angka agregat yang boleh dibaca. Kedua, batasi siapa yang boleh menjalankan evaluasi blackbox bila tim besar, atau catat setiap evaluasi agar jumlah pemakaiannya terlihat.

        Ketiga, hati-hati dengan kebocoran halus. Jika sebuah grafik error per kategori dari blackbox ditampilkan, orang bisa menyimpulkan kategori mana yang bermasalah dan memperbaikinya secara khusus. Itu sudah merupakan bentuk melihat blackbox. Cukup laporkan satu atau dua angka ringkasan.

        Keempat, anggap blackbox bisa habis. Setelah dipakai untuk puluhan keputusan, ia tidak lagi sepenuhnya bersih. Saat itu tiba, ambil data segar dan rotasikan perannya. Pemantauan seperti ini murah dibanding risiko meluncurkan model yang sebenarnya hanya beruntung di dev set.
        """),
        K(
            "note",
            """
            Eyeball dan blackbox dipilih acak dari dev set yang sama, jadi keduanya berasal dari distribusi yang sama. Jangan membagi berdasarkan urutan data atau waktu kecuali dev set memang disusun demikian dengan sengaja.
            """,
        ),
        C(
            """
import numpy as np

n_dev = 5000
rng = np.random.default_rng(42)
perm = rng.permutation(n_dev)
eyeball = np.sort(perm[:500])
blackbox = np.sort(perm[500:])
print("eyeball:", len(eyeball), "blackbox:", len(blackbox))
print("irisan kosong:", len(set(eyeball) & set(blackbox)) == 0)
print("kesalahan diharapkan di eyeball:", 500 * 0.20)
""",
            """
            eyeball: 500 blackbox: 4500
            irisan kosong: True
            kesalahan diharapkan di eyeball: 100.0
            """,
            """
            Pembagian acak tanpa pengembalian menghasilkan dua himpunan yang saling lepas. Eyeball 500 contoh dengan error 20 persen berisi sekitar 100 kesalahan untuk dianalisis.
            """,
        ),
        C(
            """
import numpy as np

rng = np.random.default_rng(0)
e = 0.20
n_eye, n_black = 200, 20000
print("k kandidat  error eyeball model terpilih  error blackbox")
for k in [1, 5, 50, 500]:
    eye = rng.binomial(n_eye, e, size=k) / n_eye
    terbaik = eye.min()
    black = rng.binomial(n_black, e) / n_black
    print(f"{k:10d}  {terbaik:27.3f}  {black:15.3f}")
""",
            """
            error eyeball model terpilih turun dari sekitar 0.20 ke sekitar 0.12 saat kandidat bertambah
            error blackbox tetap sekitar 0.20
            """,
            """
            Semua kandidat sebenarnya sama baik dengan error sejati 20 persen. Semakin banyak kandidat, semakin rendah error eyeball model terpilih, padahal error blackbox tetap sekitar 20 persen. Selisih itu adalah optimisme akibat seleksi.
            """,
        ),
        C(
            """
import numpy as np

def selisih_overfit(err_eye, err_black, margin):
    return (err_black - err_eye) > margin

print(selisih_overfit(0.10, 0.20, 0.03))
print(selisih_overfit(0.19, 0.20, 0.03))
""",
            """
            True
            False
            """,
            """
            Aturan sederhana untuk memantau overfit: bila blackbox lebih buruk dari eyeball melebihi margin, anggap eyeball sudah terlalu sering dipakai. Margin ditentukan dari ukuran dev set, karena dev set kecil memang berderau lebih besar.
            """,
        ),
        E(
            "D11-04-2-ex1",
            "mudah",
            """
            Tulis fungsi `bagi_eyeball(n, n_eyeball, seed)` yang mengembalikan tuple `(eyeball, blackbox)`. Pakai `rng = np.random.default_rng(seed)` dan `perm = rng.permutation(n)`. `eyeball` adalah `np.sort(perm[:n_eyeball])` dan `blackbox` adalah `np.sort(perm[n_eyeball:])`.
            """,
            """
            import numpy as np

            def bagi_eyeball(n, n_eyeball, seed):
                # TODO: implementasikan
                pass
            """,
            """
            import numpy as np
            a, b = bagi_eyeball(1000, 100, 0)
            assert len(a) == 100 and len(b) == 900
            assert set(a).isdisjoint(set(b))
            assert sorted(set(a) | set(b)) == list(range(1000))
            assert list(a) == sorted(a)
            a2, b2 = bagi_eyeball(1000, 100, 0)
            assert list(a) == list(a2)
            """,
            "Buat permutasi, potong di n_eyeball, lalu urutkan masing-masing potongan.",
            """
            import numpy as np

            def bagi_eyeball(n, n_eyeball, seed):
                rng = np.random.default_rng(seed)
                perm = rng.permutation(n)
                return np.sort(perm[:n_eyeball]), np.sort(perm[n_eyeball:])
            """,
        ),
        E(
            "D11-04-2-ex2",
            "sedang",
            """
            Tulis fungsi `jumlah_salah_diharapkan(n_eyeball, err)` yang mengembalikan banyak kesalahan yang diharapkan pada eyeball dev set (`n_eyeball * err`), dibulatkan 2 desimal. Tulis juga `cukup_untuk_analisis(n_eyeball, err, minimal)` yang mengembalikan `True` bila hasil pertama lebih besar atau sama dengan `minimal`.
            """,
            """
            def jumlah_salah_diharapkan(n_eyeball, err):
                # TODO: implementasikan
                pass

            def cukup_untuk_analisis(n_eyeball, err, minimal):
                # TODO: implementasikan
                pass
            """,
            """
            assert jumlah_salah_diharapkan(500, 0.2) == 100.0
            assert jumlah_salah_diharapkan(500, 0.05) == 25.0
            assert cukup_untuk_analisis(500, 0.2, 100) is True
            assert cukup_untuk_analisis(500, 0.05, 50) is False
            """,
            "Gunakan fungsi pertama di dalam fungsi kedua dan kembalikan bool murni.",
            """
            def jumlah_salah_diharapkan(n_eyeball, err):
                return round(n_eyeball * err, 2)

            def cukup_untuk_analisis(n_eyeball, err, minimal):
                return bool(jumlah_salah_diharapkan(n_eyeball, err) >= minimal)
            """,
        ),
        E(
            "D11-04-2-ex3",
            "sedang",
            """
            Tulis fungsi `eyeball_overfit(err_eyeball, err_blackbox, margin)` yang mengembalikan `True` bila `err_blackbox - err_eyeball > margin` (dibulatkan 6 desimal sebelum dibandingkan) dan `False` selainnya.
            """,
            """
            def eyeball_overfit(err_eyeball, err_blackbox, margin):
                # TODO: implementasikan
                pass
            """,
            """
            assert eyeball_overfit(0.10, 0.20, 0.03) is True
            assert eyeball_overfit(0.19, 0.20, 0.03) is False
            assert eyeball_overfit(0.17, 0.20, 0.03) is False
            assert eyeball_overfit(0.20, 0.15, 0.03) is False
            """,
            "Hitung selisih, bulatkan 6 desimal, lalu bandingkan dengan margin. Kasus 0.17 versus 0.20 tepat sama dengan margin sehingga hasilnya False.",
            """
            def eyeball_overfit(err_eyeball, err_blackbox, margin):
                return bool(round(err_blackbox - err_eyeball, 6) > margin)
            """,
        ),
        E(
            "D11-04-2-ex4",
            "menantang",
            """
            Tulis fungsi `simulasi_pilih_terbaik(k, n_eye, n_black, e, seed)`. Pakai `rng = np.random.default_rng(seed)`. Tarik `eye = rng.binomial(n_eye, e, size=k) / n_eye` dan ambil `terbaik = eye.min()`. Lalu tarik `black = rng.binomial(n_black, e) / n_black`. Kembalikan `(terbaik, black)` dibulatkan 4 desimal.
            """,
            """
            import numpy as np

            def simulasi_pilih_terbaik(k, n_eye, n_black, e, seed):
                # TODO: implementasikan
                pass
            """,
            """
            terbaik, black = simulasi_pilih_terbaik(50, 200, 20000, 0.2, 0)
            assert terbaik < 0.17
            assert abs(black - 0.2) < 0.015
            satu, _ = simulasi_pilih_terbaik(1, 200, 20000, 0.2, 0)
            assert terbaik <= satu
            assert simulasi_pilih_terbaik(5, 100, 1000, 0.1, 7) == simulasi_pilih_terbaik(5, 100, 1000, 0.1, 7)
            """,
            "Urutan penarikan penting: eye lebih dulu, lalu black. Ambil minimum dari array eye.",
            """
            import numpy as np

            def simulasi_pilih_terbaik(k, n_eye, n_black, e, seed):
                rng = np.random.default_rng(seed)
                eye = rng.binomial(n_eye, e, size=k) / n_eye
                terbaik = float(eye.min())
                black = float(rng.binomial(n_black, e) / n_black)
                return round(terbaik, 4), round(black, 4)
            """,
        ),
    ],
    [
        M(
            "Memakai seluruh dev set untuk error analysis sekaligus untuk memilih model.",
            "Pisahkan eyeball untuk dilihat dan blackbox untuk mengukur dan memilih.",
        ),
        M(
            "Melihat contoh blackbox sesekali karena penasaran.",
            "Jangan pernah memeriksa contoh blackbox, atau ia berhenti menjadi pengukur jujur.",
        ),
        M(
            "Menganggap error dev terbaik dari banyak percobaan sebagai estimasi akhir.",
            "Gunakan error blackbox dan test set untuk estimasi yang bebas bias seleksi.",
        ),
    ],
    [
        Q(
            "Apa fungsi Blackbox dev set?",
            ["Dilihat satu per satu untuk error analysis", "Mengukur error dan memilih model tanpa pernah diperiksa manual", "Menggantikan training set", "Disimpan sebagai test"],
            1,
            "Blackbox tidak boleh dilihat contohnya, sehingga tidak ikut menyesuaikan diri dengan intuisimu.",
        ),
        Q(
            "Error eyeball 8 persen dan blackbox 15 persen. Apa artinya?",
            ["Sistem sangat baik", "Kemungkinan overfit ke eyeball dev set", "Blackbox terlalu mudah", "Test set bocor"],
            1,
            "Selisih besar menandakan eyeball sudah terlalu sering dipelajari.",
        ),
        Q(
            "Mengapa memilih model terbaik dari 50 kandidat setara menimbulkan optimisme?",
            ["Karena model berubah", "Karena yang terpilih cenderung yang kebetulan beruntung di dev set", "Karena blackbox bias", "Karena data hilang"],
            1,
            "Minimum dari banyak nilai berderau cenderung berada di bawah nilai sejatinya.",
        ),
        Q(
            "Dev set 5000 contoh, error 20 persen, eyeball 500 contoh. Kira-kira berapa kesalahan di eyeball?",
            ["10", "100", "500", "1000"],
            1,
            "500 dikali 0,2 sama dengan 100 kesalahan.",
        ),
        Q(
            "Apa yang dilakukan setelah mendeteksi overfit ke eyeball?",
            ["Menghapus blackbox", "Membuat eyeball baru, misalnya dengan memindahkan contoh dari blackbox atau mengumpulkan data baru", "Menambah layer", "Mengabaikan"],
            1,
            "Eyeball lama sudah terpakai, sehingga perlu data segar untuk analisis berikutnya.",
        ),
    ],
    [
        "Dev set dibagi menjadi eyeball yang boleh dilihat dan blackbox yang tidak boleh dilihat.",
        "Selisih error blackbox di atas eyeball mengindikasikan overfit ke eyeball.",
        "Memilih yang terbaik dari banyak kandidat menimbulkan optimisme seleksi pada dev set.",
        "Jumlah kesalahan di eyeball sama dengan ukuran eyeball dikali error.",
    ],
    ["Machine Learning Yearning, bab 17 (Andrew Ng): Eyeball dan Blackbox dev set"],
)

l3 = lesson(
    "D11-04-3",
    "Ukuran eyeball dan blackbox dev set",
    35,
    [
        "Menentukan ukuran eyeball dev set dari error model dan jumlah kesalahan yang ingin dipelajari",
        "Menaksir ketidakpastian estimasi fraksi kategori dari jumlah kesalahan yang diperiksa",
        "Menilai kualitas error analysis menurut jumlah kesalahan di eyeball",
        "Menyusun rencana pembagian dev set ketika data terbatas",
    ],
    [
        T("""
        ## Ukuran eyeball ditentukan oleh jumlah kesalahan

        Ukuran eyeball dev set harus cukup besar agar mengandung cukup banyak contoh yang salah untuk dianalisis. Ukuran yang relevan bukan jumlah contoh, melainkan jumlah kesalahan di dalamnya. Pedoman kasarnya: jika classifier-mu membuat 10 persen kesalahan, eyeball dengan 1.000 contoh berisi sekitar 100 kesalahan. Jika error hanya 5 persen, kamu butuh 2.000 contoh untuk mendapat jumlah kesalahan yang sama.

        Rumus sederhananya: `ukuran_eyeball = ceil(kesalahan_target / error)`. Semakin baik model, semakin besar eyeball yang dibutuhkan. Inilah alasan error analysis makin mahal pada model yang sudah bagus: kesalahan makin langka dan kamu harus memeriksa lebih banyak contoh yang benar demi menemukan satu yang salah.

        Jika classifier-mu hanya salah 2 persen, untuk mendapat 100 kesalahan kamu butuh 5.000 contoh. Pada titik itu kamu perlu bertanya apakah usaha ini sepadan, atau apakah kamu lebih baik memakai metode lain seperti mencari kesalahan dari log produksi.
        """),
        T("""
        ## Berapa banyak kesalahan yang cukup

        Pedoman praktis berdasarkan jumlah kesalahan di eyeball adalah sebagai berikut. Dengan sekitar 10 kesalahan, kamu mendapat gambaran awal tentang sumber kesalahan utama, tetapi sangat berderau. Dengan sekitar 20 kesalahan, kamu mulai bisa menebak sumber kesalahan terbesar. Dengan sekitar 50 kesalahan, kamu mendapat gambaran cukup baik. Dengan sekitar 100 kesalahan, gambaran itu sangat baik. Dengan lebih dari itu manfaatnya makin kecil.

        Alasannya statistik. Fraksi kategori dari n kesalahan yang diperiksa memiliki interval kepercayaan 95 persen dengan setengah lebar sekitar `1,96 * sqrt(p * (1 - p) / n)`. Untuk p sama dengan 0,5, setengah lebar itu sekitar 0,31 pada n sama dengan 10, 0,22 pada n sama dengan 20, 0,14 pada n sama dengan 50, dan 0,10 pada n sama dengan 100. Mengganda ukuran sampel tidak menggandakan ketepatan, hanya memperbaiki sekitar 1,4 kali.

        Artinya, keputusan prioritas cukup dengan puluhan sampai seratusan kesalahan. Tidak perlu menunggu ribuan karena yang dicari hanya urutan kasar kategori, bukan angka persis.
        """),
        T("""
        ## Ukuran blackbox dan dev set yang kecil

        Blackbox dev set sebesar 1.000 sampai 10.000 contoh cukup untuk banyak aplikasi sebagai bahan memilih model dan menyetel hyperparameter. Makin kecil perbedaan antar model yang ingin kamu deteksi, makin besar blackbox yang diperlukan. Untuk memilih antara dua model yang selisih errornya 0,1 poin persen, ribuan contoh tidak lagi cukup.

        Bagaimana jika dev set terlalu kecil untuk dibagi dua dengan nyaman? Jika kamu hanya punya 1.500 contoh, pembagian akan membuat salah satunya terlalu kecil. Dalam keadaan itu sebagian besar atau seluruh dev set dijadikan eyeball, karena kemampuan melakukan error analysis lebih mendesak. Kamu kehilangan alat deteksi overfit yang bersih, sehingga lebih hati-hati memakai heuristik, intuisi, dan test set di akhir.

        Jika eyeball seluruhnya kamu lihat dan data terbatas, keputusan memakai kombinasi pedoman: tetap sederhana, jangan terlalu banyak putaran penyetelan, dan cadangkan test set untuk estimasi akhir.
        """),
        T("""
        ## Rencana sederhana dan hubungannya dengan metrik

        Alur kerja praktis: tentukan jumlah kesalahan target, misalnya 100. Hitung ukuran eyeball dari error saat ini. Jika sisa dev set setelah eyeball masih cukup untuk blackbox minimum yang masuk akal, pisahkan. Jika tidak, jadikan semua sebagai eyeball.

        Saat model membaik, ulangi perhitungan. Eyeball yang tadinya cukup bisa menjadi terlalu kecil karena error menurun. Kamu mungkin perlu mengumpulkan data dev baru yang diberi label, atau memindahkan sebagian blackbox menjadi eyeball.

        Perhatikan juga hubungannya dengan modul sebelumnya. Metrik tunggal, dev set, dan test set menentukan apa yang kamu ukur. Eyeball dan blackbox menentukan bagaimana kamu mempelajari hasilnya tanpa menipu diri sendiri. Kedua lapis ini bekerja bersama untuk iterasi yang cepat dan jujur.
        """),
        K(
            "tip",
            """
            Catat jumlah kesalahan yang diperiksa di samping tiap angka fraksi kategori. Fraksi 40 persen dari 20 kesalahan jauh kurang bisa dipercaya daripada fraksi 40 persen dari 100 kesalahan.
            """,
        ),
        C(
            """
import math

def ukuran_eyeball(err, target):
    return math.ceil(round(target / err, 6))

for err in [0.20, 0.10, 0.05, 0.02]:
    print(f"error {err:.2f}: butuh eyeball {ukuran_eyeball(err, 100)} untuk 100 kesalahan")
""",
            """
            error 0.20: butuh eyeball 500 untuk 100 kesalahan
            error 0.10: butuh eyeball 1000 untuk 100 kesalahan
            error 0.05: butuh eyeball 2000 untuk 100 kesalahan
            error 0.02: butuh eyeball 5000 untuk 100 kesalahan
            """,
            """
            Makin rendah error, makin besar eyeball untuk jumlah kesalahan yang sama. Pada error 2 persen eyeball harus 5.000 contoh, dan di titik itu error analysis manual makin mahal.
            """,
        ),
        C(
            """
import math

for n in [10, 20, 50, 100, 200]:
    setengah = 1.96 * math.sqrt(0.5 * 0.5 / n)
    print(f"{n:4d} kesalahan: setengah lebar CI untuk p=0.5 adalah {setengah:.3f}")
""",
            """
            10 kesalahan: 0.310
            20 kesalahan: 0.219
            50 kesalahan: 0.139
            100 kesalahan: 0.098
            200 kesalahan: 0.069
            """,
            """
            Ketepatan membaik dengan akar jumlah sampel. Dari 100 ke 200 kesalahan, setengah lebar CI turun dari 0,098 ke 0,069 saja. Karena itu seratusan kesalahan sudah memadai untuk memprioritaskan kategori.
            """,
        ),
        C(
            """
import math

def rencana(n_dev, err, target=100, blackbox_min=1000):
    perlu = math.ceil(round(target / err, 6))
    if n_dev >= perlu + blackbox_min:
        return {"eyeball": perlu, "blackbox": n_dev - perlu}
    return {"eyeball": n_dev, "blackbox": 0}

print(rencana(5000, 0.10))
print(rencana(1500, 0.10))
print(rencana(10000, 0.05))
""",
            """
            {'eyeball': 1000, 'blackbox': 4000}
            {'eyeball': 1500, 'blackbox': 0}
            {'eyeball': 2000, 'blackbox': 8000}
            """,
            """
            Rencana pembagian menyesuaikan ukuran eyeball dengan error, lalu menyisakan sisanya untuk blackbox bila cukup. Saat data terbatas, seluruh dev set dijadikan eyeball dan overfit dipantau dengan cara lain.
            """,
        ),
        E(
            "D11-04-3-ex1",
            "mudah",
            """
            Tulis fungsi `ukuran_eyeball(err, target)` yang mengembalikan ukuran eyeball minimum agar berisi sekitar `target` kesalahan: `ceil(target / err)`. Bulatkan hasil bagi ke 6 desimal sebelum `math.ceil` untuk menghindari galat floating point.
            """,
            """
            import math

            def ukuran_eyeball(err, target):
                # TODO: implementasikan
                pass
            """,
            """
            assert ukuran_eyeball(0.05, 100) == 2000
            assert ukuran_eyeball(0.10, 100) == 1000
            assert ukuran_eyeball(0.20, 50) == 250
            assert ukuran_eyeball(0.03, 100) == 3334
            """,
            "Gunakan math.ceil(round(target / err, 6)).",
            """
            import math

            def ukuran_eyeball(err, target):
                return math.ceil(round(target / err, 6))
            """,
        ),
        E(
            "D11-04-3-ex2",
            "sedang",
            """
            Tulis fungsi `setengah_lebar_ci(p, n)` yang mengembalikan setengah lebar interval kepercayaan 95 persen: `1.96 * sqrt(p * (1 - p) / n)`, dibulatkan 4 desimal. Jika `n <= 0` kembalikan `1.0`.
            """,
            """
            import math

            def setengah_lebar_ci(p, n):
                # TODO: implementasikan
                pass
            """,
            """
            assert setengah_lebar_ci(0.5, 100) == 0.098
            assert setengah_lebar_ci(0.5, 10) == 0.3099
            assert setengah_lebar_ci(0.0, 50) == 0.0
            assert setengah_lebar_ci(0.5, 0) == 1.0
            assert setengah_lebar_ci(0.5, 50) < setengah_lebar_ci(0.5, 20)
            """,
            "Tangani n tidak positif lebih dulu, lalu terapkan rumus dan round 4.",
            """
            import math

            def setengah_lebar_ci(p, n):
                if n <= 0:
                    return 1.0
                return round(1.96 * math.sqrt(p * (1 - p) / n), 4)
            """,
        ),
        E(
            "D11-04-3-ex3",
            "sedang",
            """
            Tulis fungsi `kualitas_eyeball(n_salah)` yang mengembalikan string menurut jumlah kesalahan: kurang dari 10 adalah `"terlalu sedikit"`, 10 sampai 19 adalah `"sangat kasar"`, 20 sampai 49 adalah `"kasar"`, 50 sampai 99 adalah `"baik"`, 100 atau lebih adalah `"sangat baik"`.
            """,
            """
            def kualitas_eyeball(n_salah):
                # TODO: implementasikan
                pass
            """,
            """
            assert kualitas_eyeball(5) == "terlalu sedikit"
            assert kualitas_eyeball(10) == "sangat kasar"
            assert kualitas_eyeball(19) == "sangat kasar"
            assert kualitas_eyeball(20) == "kasar"
            assert kualitas_eyeball(49) == "kasar"
            assert kualitas_eyeball(50) == "baik"
            assert kualitas_eyeball(99) == "baik"
            assert kualitas_eyeball(100) == "sangat baik"
            """,
            "Gunakan rangkaian if berurutan dari ambang terkecil.",
            """
            def kualitas_eyeball(n_salah):
                if n_salah < 10:
                    return "terlalu sedikit"
                if n_salah < 20:
                    return "sangat kasar"
                if n_salah < 50:
                    return "kasar"
                if n_salah < 100:
                    return "baik"
                return "sangat baik"
            """,
        ),
        E(
            "D11-04-3-ex4",
            "menantang",
            """
            Tulis fungsi `rencana_dev(n_dev, err, target, blackbox_min)` yang menghitung `perlu = ceil(round(target / err, 6))`. Jika `n_dev >= perlu + blackbox_min` kembalikan `{"eyeball": perlu, "blackbox": n_dev - perlu}`. Selainnya kembalikan `{"eyeball": n_dev, "blackbox": 0}`.
            """,
            """
            import math

            def rencana_dev(n_dev, err, target, blackbox_min):
                # TODO: implementasikan
                pass
            """,
            """
            assert rencana_dev(5000, 0.10, 100, 1000) == {"eyeball": 1000, "blackbox": 4000}
            assert rencana_dev(1500, 0.10, 100, 1000) == {"eyeball": 1500, "blackbox": 0}
            assert rencana_dev(10000, 0.05, 100, 1000) == {"eyeball": 2000, "blackbox": 8000}
            assert rencana_dev(3000, 0.05, 100, 1000) == {"eyeball": 2000, "blackbox": 1000}
            assert rencana_dev(2999, 0.05, 100, 1000) == {"eyeball": 2999, "blackbox": 0}
            """,
            "Hitung kebutuhan eyeball dulu. Bandingkan n_dev dengan perlu + blackbox_min untuk memutuskan cabang.",
            """
            import math

            def rencana_dev(n_dev, err, target, blackbox_min):
                perlu = math.ceil(round(target / err, 6))
                if n_dev >= perlu + blackbox_min:
                    return {"eyeball": perlu, "blackbox": n_dev - perlu}
                return {"eyeball": n_dev, "blackbox": 0}
            """,
        ),
    ],
    [
        M(
            "Menentukan ukuran eyeball dari jumlah contoh saja.",
            "Tentukan dari jumlah kesalahan yang ingin dipelajari dibagi error model.",
        ),
        M(
            "Menunggu ribuan kesalahan sebelum mengambil keputusan prioritas.",
            "Puluhan sampai seratusan kesalahan sudah cukup memberi urutan kasar kategori.",
        ),
        M(
            "Memaksa pembagian eyeball dan blackbox ketika dev set sangat kecil.",
            "Jika data terbatas, jadikan sebagian besar dev set sebagai eyeball dan jaga disiplin penyetelan.",
        ),
    ],
    [
        Q(
            "Error 5 persen dan ingin 100 kesalahan. Berapa ukuran eyeball?",
            ["500", "1000", "2000", "5000"],
            2,
            "100 dibagi 0,05 sama dengan 2000.",
        ),
        Q(
            "Mengapa error analysis makin mahal pada model yang sudah bagus?",
            ["Karena GPU mahal", "Karena kesalahan makin langka sehingga eyeball harus lebih besar", "Karena label berubah", "Karena metrik berubah"],
            1,
            "Dengan error kecil, kamu harus memeriksa banyak contoh benar demi menemukan kesalahan.",
        ),
        Q(
            "Setengah lebar CI untuk p sama dengan 0,5 turun dari sekitar 0,31 ke 0,10 ketika sampel naik dari 10 ke 100. Apa pelajarannya?",
            ["Ketepatan naik linear", "Ketepatan membaik sebanding akar jumlah sampel", "Sampel tidak berpengaruh", "CI selalu 0,5"],
            1,
            "Jumlah sampel naik 10 kali, tetapi lebar CI turun sekitar 3 kali.",
        ),
        Q(
            "Kisaran ukuran blackbox yang sering memadai?",
            ["10 sampai 50", "1.000 sampai 10.000", "1 juta", "Tidak perlu"],
            1,
            "Ribuan contoh umumnya cukup untuk memilih model dan menyetel hyperparameter.",
        ),
        Q(
            "Dev set hanya 1.500 contoh. Apa yang masuk akal?",
            ["Membuang dev set", "Menjadikan sebagian besar atau seluruhnya eyeball dan berhati-hati menyetel", "Membuat blackbox 1.400", "Menambah layer"],
            1,
            "Error analysis lebih mendesak, dengan konsekuensi kehilangan alat deteksi overfit yang bersih.",
        ),
    ],
    [
        "Ukuran eyeball sama dengan kesalahan target dibagi error model.",
        "Puluhan sampai seratusan kesalahan cukup untuk menentukan prioritas kategori.",
        "Blackbox 1.000 sampai 10.000 contoh memadai untuk banyak aplikasi.",
        "Ketika data terbatas, utamakan eyeball dan jaga disiplin penyetelan.",
    ],
    ["Machine Learning Yearning, bab 18 dan 19 (Andrew Ng): ukuran Eyeball dan Blackbox dev set"],
)

video = {
    "needed": True,
    "kind": "ai_slides",
    "reason": "Pembagian dev set menjadi eyeball dan blackbox serta efek seleksi paling mudah dipahami dengan diagram bertahap.",
    "brief": [
        "Slide 1: dev set 5000 contoh dibelah acak menjadi eyeball 500 dan blackbox 4500",
        "Slide 2: siklus kerja: lihat kesalahan di eyeball, perbaiki model, ukur di blackbox",
        "Slide 3: grafik error eyeball turun sementara blackbox mendatar sebagai tanda overfit",
        "Slide 4: tabel ukuran eyeball untuk error 20, 10, 5, dan 2 persen dengan target 100 kesalahan",
    ],
}

write_module(
    "D11",
    4,
    "Label salah, Eyeball dan Blackbox dev set",
    105,
    [
        "Memutuskan kapan label salah di dev dan test set layak dibersihkan",
        "Memisahkan dev set menjadi eyeball dan blackbox dan membaca selisihnya",
        "Menentukan ukuran eyeball dan blackbox dari error dan data tersedia",
    ],
    [l1, l2, l3],
    video,
    REF,
)
