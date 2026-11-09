import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

l1 = lesson(
    "A4-02-1",
    "Peluang bersyarat",
    35,
    [
        "Mendefinisikan peluang bersyarat sebagai penyempitan ruang sampel",
        "Menghitung peluang bersyarat dari enumerasi dan tabel",
        "Memakai aturan perkalian umum untuk urutan kejadian",
        "Menjelaskan hubungan peluang bersyarat dengan independensi",
    ],
    [
        T("""
        ## Informasi mengubah peluang

        Peluang tidak selalu tetap. Begitu kita mendapat informasi baru, peluang suatu kejadian bisa berubah. Peluang hujan hari ini berbeda bila kita tahu langit sedang mendung. Peluang pelanggan berhenti berlangganan berbeda bila kita tahu ia menerima promo. Cara matematis menyatakan perubahan ini adalah **peluang bersyarat**.

        Peluang bersyarat adalah dasar hampir semua pembelajaran mesin probabilistik. Setiap kali model memprediksi label berdasarkan fitur, ia sedang menghitung peluang label dengan syarat fitur itu. Karena itu pemahaman yang kokoh di sini akan terpakai terus sepanjang kursus.
        """),
        T("""
        ## Definisi

        Peluang `A` dengan syarat `B` ditulis `P(A | B)` dan dibaca peluang A diberikan B. Rumusnya `P(A | B) = P(A dan B) / P(B)`, dengan syarat `P(B) > 0`. Maknanya: kita menyempitkan ruang sampel menjadi hanya hasil yang masuk `B`, lalu bertanya berapa bagian dari ruang baru itu yang juga masuk `A`.

        Dengan hasil sama mungkin, ini setara dengan `|A dan B| / |B|`. Penyebutnya bukan lagi seluruh ruang sampel melainkan hanya hasil yang konsisten dengan informasi yang kita punya. Memahami pembagian ini sebagai penyempitan ruang jauh lebih bermanfaat daripada menghafal rumus.
        """),
        C(
            """
            from itertools import product

            S = list(product(range(1, 7), repeat=2))
            A = [h for h in S if h[0] + h[1] == 8]
            B = [h for h in S if h[0] % 2 == 0]
            AB = [h for h in A if h in B]
            print(round(len(A) / len(S), 4), round(len(AB) / len(B), 4))
            """,
            """
            0.1389 0.1667
            """,
            """
            Peluang jumlah delapan adalah lima per tiga puluh enam. Setelah tahu dadu pertama genap, ruang sampel menyempit menjadi delapan belas hasil dan peluangnya naik menjadi tiga per delapan belas.
            """,
            filename="bersyarat_dadu.py",
        ),
        T("""
        ## Aturan perkalian umum

        Dengan menata ulang definisi diperoleh `P(A dan B) = P(B) * P(A | B)`. Inilah aturan perkalian umum yang berlaku tanpa asumsi independensi. Kita hitung peluang kejadian pertama, lalu peluang kejadian kedua dengan memperhitungkan bahwa kejadian pertama sudah terjadi.

        Contohnya mengambil dua bola dari kantong tanpa pengembalian. Peluang bola kedua merah bergantung pada bola pertama karena komposisi isi kantong berubah. Aturan ini menyelesaikan semua soal pengambilan berurutan tanpa pengembalian dan menjadi dasar pohon peluang.
        """),
        C(
            """
            import math

            langsung = 5 / 8 * 4 / 7
            kombinasi = math.comb(5, 2) / math.comb(8, 2)
            print(round(langsung, 4), round(kombinasi, 4))
            """,
            """
            0.3571 0.3571
            """,
            """
            Lima merah dan tiga biru: peluang merah pertama lima per delapan dan merah kedua empat per tujuh. Hasil sama dengan hitungan kombinasi.
            """,
            filename="dua_bola.py",
        ),
        T("""
        ## Membaca tabel kontingensi

        Dalam data, peluang bersyarat paling mudah dihitung dari tabel silang jumlah. Misalnya 300 pelanggan: 100 menerima promo dan 200 tidak. Dari yang menerima promo, 10 berhenti berlangganan. Dari yang tidak, 40 berhenti. Maka `P(berhenti | promo) = 10/100 = 0,1` dan `P(berhenti | tanpa promo) = 40/200 = 0,2`.

        Perhatikan bahwa penyebutnya adalah total baris yang menjadi syarat, bukan total seluruh data. Kesalahan menggunakan total keseluruhan sebagai penyebut sangat umum dan menghasilkan peluang gabungan, bukan bersyarat.
        """),
        C(
            """
            promo = {"berhenti": 10, "tetap": 90}
            tanpa = {"berhenti": 40, "tetap": 160}
            p1 = promo["berhenti"] / sum(promo.values())
            p2 = tanpa["berhenti"] / sum(tanpa.values())
            total = (promo["berhenti"] + tanpa["berhenti"]) / (sum(promo.values()) + sum(tanpa.values()))
            print(round(p1, 4), round(p2, 4), round(total, 4))
            """,
            """
            0.1 0.2 0.1667
            """,
            """
            Berhenti berlangganan lebih jarang pada penerima promo. Peluang keseluruhan berada di antara keduanya.
            """,
            filename="tabel_kontingensi.py",
        ),
        K(
            "warn",
            """
            P(A | B) tidak sama dengan P(B | A). Peluang seseorang pemain basket bertinggi lebih dari 190 cm tidak sama dengan peluang orang bertinggi lebih dari 190 cm adalah pemain basket.
            """,
            title="Arah syarat",
        ),
        T("""
        ## Hubungan dengan independensi

        Bila `A` dan `B` independen maka mengetahui `B` tidak mengubah peluang `A`, yaitu `P(A | B) = P(A)`. Ini cara lain menyatakan independensi dan sering lebih intuitif daripada hasil kali. Sebaliknya, bila `P(A | B)` berbeda dari `P(A)`, kedua kejadian berhubungan.

        Pada contoh promo, `P(berhenti | promo) = 0,1` berbeda dari `P(berhenti) = 0,1667`, sehingga promo dan berhenti berlangganan tidak independen. Selisih itu adalah sinyal awal bahwa promo berasosiasi dengan retensi, walau belum membuktikan sebab akibat.
        """),
        T("""
        ## Kebiasaan yang baik

        Saat menghadapi soal bersyarat, tulis dulu mana syaratnya dan mana kejadian yang ditanyakan. Kata kunci seperti jika, diketahui bahwa, atau di antara menandakan syarat. Lalu pilih: hitung dengan penyempitan ruang sampel, dengan tabel, atau dengan aturan perkalian.

        Latih juga membalik pertanyaan secara sadar. Banyak kesalahan penalaran dalam berita dan laporan berawal dari menukar `P(A | B)` dengan `P(B | A)`. Pelajaran berikutnya memberi alat resmi, yaitu teorema Bayes, untuk membalik arah syarat dengan benar.
        """),
        T("""
        ## Pohon peluang

        Untuk kejadian berurutan, gambarlah pohon: tiap cabang membawa peluang bersyarat, dan peluang sebuah jalur adalah hasil kali peluang di sepanjang cabangnya. Pada pengambilan dua bola, cabang pertama merah atau biru, lalu cabang kedua bergantung pada hasil pertama.

        Pohon memaksa kita menuliskan semua kemungkinan dan memeriksa bahwa peluang cabang dari satu simpul berjumlah satu. Bila tidak berjumlah satu, ada kasus yang terlewat. Ini kebiasaan verifikasi yang murah dan sangat efektif.
        """),
        T("""
        ## Contoh penalaran

        Sebuah klinik mencatat bahwa 30 persen pasien datang dengan demam, dan 20 persen dari yang demam ternyata terkena infeksi tertentu. Peluang pasien demam dan terinfeksi adalah `0,3 * 0,2 = 0,06`. Perhatikan bahwa 20 persen tadi adalah peluang bersyarat, bukan peluang terhadap seluruh pasien. Menyebut keduanya dengan cermat mencegah salah baca laporan.
        """),
        E(
            "A4-02-1-ex1",
            "mudah",
            """
            Tulis fungsi `peluang_bersyarat(pab, pb)` yang mengembalikan `P(A | B)` dibulatkan 4 desimal.
            """,
            """
            def peluang_bersyarat(pab, pb):
                # TODO: implementasikan
                pass
            """,
            """
            assert peluang_bersyarat(0.2, 0.5) == 0.4
            assert peluang_bersyarat(0.1, 0.4) == 0.25
            assert peluang_bersyarat(0, 0.3) == 0.0
            assert peluang_bersyarat(0.3, 0.3) == 1.0
            """,
            "Bagi peluang irisan dengan peluang syarat.",
            """
            def peluang_bersyarat(pab, pb):
                return round(pab / pb, 4)
            """,
        ),
        E(
            "A4-02-1-ex2",
            "sedang",
            """
            Tulis fungsi `peluang_dua_merah(m, b)` yang mengembalikan peluang dua bola yang diambil tanpa pengembalian dari `m` merah dan `b` biru keduanya merah, dibulatkan 4 desimal.
            """,
            """
            def peluang_dua_merah(m, b):
                # TODO: implementasikan
                pass
            """,
            """
            assert peluang_dua_merah(5, 3) == 0.3571
            assert peluang_dua_merah(2, 0) == 1.0
            assert peluang_dua_merah(1, 5) == 0.0
            assert peluang_dua_merah(4, 4) == 0.2143
            """,
            "Kalikan peluang merah pertama dengan peluang merah kedua setelah satu merah terambil.",
            """
            def peluang_dua_merah(m, b):
                n = m + b
                return round(m / n * (m - 1) / (n - 1), 4)
            """,
        ),
        E(
            "A4-02-1-ex3",
            "sedang",
            """
            Tulis fungsi `peluang_kolom(tabel, baris, kolom)` yang menerima dict bersarang berisi jumlah, misalnya `{'promo': {'berhenti': 10, 'tetap': 90}}`, dan mengembalikan peluang `kolom` dengan syarat `baris`, dibulatkan 4 desimal.
            """,
            """
            def peluang_kolom(tabel, baris, kolom):
                # TODO: implementasikan
                pass
            """,
            """
            t = {'promo': {'berhenti': 10, 'tetap': 90}, 'tanpa': {'berhenti': 40, 'tetap': 160}}
            assert peluang_kolom(t, 'promo', 'berhenti') == 0.1
            assert peluang_kolom(t, 'tanpa', 'berhenti') == 0.2
            assert peluang_kolom(t, 'tanpa', 'tetap') == 0.8
            assert peluang_kolom(t, 'promo', 'tetap') == 0.9
            """,
            "Bagi jumlah sel dengan jumlah seluruh baris yang menjadi syarat.",
            """
            def peluang_kolom(tabel, baris, kolom):
                total = sum(tabel[baris].values())
                return round(tabel[baris][kolom] / total, 4)
            """,
        ),
        E(
            "A4-02-1-ex4",
            "menantang",
            """
            Tulis fungsi `peluang_jumlah_syarat(k, syarat)` yang mengembalikan peluang jumlah dua dadu adil sama dengan `k` dengan syarat `syarat(a, b)` bernilai True, dibulatkan 4 desimal. Bila tidak ada hasil yang memenuhi syarat, kembalikan 0.0.
            """,
            """
            from itertools import product

            def peluang_jumlah_syarat(k, syarat):
                # TODO: implementasikan
                pass
            """,
            """
            assert peluang_jumlah_syarat(8, lambda a, b: a % 2 == 0) == 0.1667
            assert peluang_jumlah_syarat(7, lambda a, b: max(a, b) == 6) == 0.1818
            assert peluang_jumlah_syarat(7, lambda a, b: a > b) == 0.2
            assert peluang_jumlah_syarat(7, lambda a, b: False) == 0.0
            """,
            "Saring pasangan yang memenuhi syarat lalu hitung yang berjumlah k di antaranya.",
            """
            from itertools import product

            def peluang_jumlah_syarat(k, syarat):
                S = [h for h in product(range(1, 7), repeat=2) if syarat(*h)]
                if not S:
                    return 0.0
                return round(sum(1 for a, b in S if a + b == k) / len(S), 4)
            """,
        ),
    ],
    [
        M("Memakai total seluruh data sebagai penyebut peluang bersyarat.", "Penyebutnya hanya total baris syarat."),
        M("Menukar P(A | B) dengan P(B | A).", "Arah syarat menentukan makna."),
        M("Mengira P(A | B) = P(A) selalu.", "Itu hanya berlaku bila independen."),
    ],
    [
        Q("P(A | B) dihitung sebagai?", ["P(A)P(B)", "P(A dan B) / P(B)", "P(A) + P(B)", "P(B) / P(A)"], 1, "Penyempitan ke B.", hint="Bagi dengan syarat."),
        Q("Penyebut peluang bersyarat adalah?", ["Seluruh data", "Peluang syarat", "Satu", "Peluang A"], 1, "P(B).", hint="Ruang baru."),
        Q("Bila independen maka P(A | B)?", ["0", "1", "P(A)", "P(B)"], 2, "Informasi tidak mengubah peluang.", hint="Tidak berubah."),
        Q("Aturan perkalian umum?", ["P(A)P(B)", "P(B)P(A | B)", "P(A)+P(B)", "P(A | B)+P(B)"], 1, "Tanpa asumsi independen.", hint="Berurutan."),
        Q("Pengambilan tanpa pengembalian membuat kejadian?", ["Independen", "Bergantung", "Mustahil", "Pasti"], 1, "Komposisi berubah.", hint="Isi berkurang."),
    ],
    [
        "Peluang bersyarat adalah penyempitan ruang sampel.",
        "P(A | B) tidak sama dengan P(B | A).",
        "Aturan perkalian umum berlaku tanpa independensi.",
        "Independen berarti syarat tidak mengubah peluang.",
    ],
    [],
)

l2 = lesson(
    "A4-02-2",
    "Peluang total dan teorema Bayes",
    35,
    [
        "Memakai hukum peluang total untuk menggabungkan skenario",
        "Menurunkan dan menerapkan teorema Bayes",
        "Menghitung posterior uji diagnostik dengan prevalensi",
        "Memperbarui keyakinan dengan bukti berurutan",
    ],
    [
        T("""
        ## Memecah menjadi skenario

        Sering kita tahu peluang suatu kejadian pada tiap skenario terpisah, tetapi ingin peluang keseluruhan. Pabrik punya dua mesin dengan tingkat cacat berbeda, dan kita ingin peluang sebuah produk acak cacat. Caranya: bobot tiap skenario dengan peluangnya, lalu jumlahkan. Ini **hukum peluang total**.

        Syaratnya skenario harus saling lepas dan bersama-sama mencakup seluruh ruang sampel, disebut partisi. Dengan partisi `B1, B2, ..., Bn`, peluang `A` adalah jumlah `P(A | Bi) * P(Bi)`. Hukum ini sederhana tetapi menjadi penyebut dalam teorema Bayes.
        """),
        C(
            """
            prior = [0.6, 0.4]
            cacat = [0.02, 0.05]
            total = sum(p * c for p, c in zip(prior, cacat))
            print(round(total, 4))
            """,
            """
            0.032
            """,
            """
            Mesin A menghasilkan enam puluh persen dengan cacat dua persen, mesin B empat puluh persen dengan cacat lima persen, sehingga cacat keseluruhan tiga koma dua persen.
            """,
            filename="peluang_total.py",
        ),
        T("""
        ## Membalik syarat: teorema Bayes

        Misalkan kita menemukan produk cacat dan ingin tahu mesin mana yang membuatnya. Itu `P(mesin | cacat)`, kebalikan dari yang kita ketahui yaitu `P(cacat | mesin)`. **Teorema Bayes** membalik arah syarat: `P(B | A) = P(A | B) * P(B) / P(A)`, dengan `P(A)` dihitung lewat hukum peluang total.

        Turunannya sederhana. Aturan perkalian memberi `P(A dan B) = P(A | B) P(B) = P(B | A) P(A)`. Membagi kedua sisi dengan `P(A)` menghasilkan rumus Bayes. Meski turunannya satu baris, dampaknya besar karena memungkinkan kita belajar dari bukti.
        """),
        T("""
        ## Prior, likelihood, dan posterior

        Dalam bahasa Bayes, `P(B)` disebut **prior**, keyakinan awal sebelum melihat bukti. `P(A | B)` disebut **likelihood**, seberapa mungkin bukti muncul bila hipotesis benar. `P(B | A)` disebut **posterior**, keyakinan setelah melihat bukti. `P(A)` adalah normalisasi agar posterior berjumlah satu.

        Pola pikirnya: posterior sebanding dengan prior kali likelihood. Hipotesis yang awalnya kurang meyakinkan bisa menjadi dominan bila bukti sangat cocok dengannya, dan sebaliknya. Kerangka ini menopang filter spam, diagnosis medis, dan banyak model prediksi.
        """),
        C(
            """
            prior = [0.6, 0.4]
            cacat = [0.02, 0.05]
            total = sum(p * c for p, c in zip(prior, cacat))
            post = [p * c / total for p, c in zip(prior, cacat)]
            print([round(x, 4) for x in post])
            """,
            """
            [0.375, 0.625]
            """,
            """
            Walau mesin A menghasilkan lebih banyak produk, produk cacat lebih mungkin berasal dari mesin B karena tingkat cacatnya lebih tinggi.
            """,
            filename="bayes_mesin.py",
        ),
        T("""
        ## Paradoks uji diagnostik

        Contoh paling terkenal: penyakit langka dengan prevalensi satu persen. Tes memiliki sensitivitas 95 persen, artinya mendeteksi 95 persen orang sakit, dan spesifisitas 90 persen, artinya 10 persen orang sehat tetap positif palsu. Bila seseorang positif, berapa peluang ia benar-benar sakit?

        Jawaban intuitifnya mendekati 95 persen, tetapi jawaban benarnya hanya sekitar 8,8 persen. Penyakit yang langka berarti sebagian besar orang sehat, dan 10 persen dari kelompok besar itu menghasilkan banyak positif palsu yang jumlahnya jauh melebihi positif benar.
        """),
        C(
            """
            prev, sens, spes = 0.01, 0.95, 0.90
            p_pos = prev * sens + (1 - prev) * (1 - spes)
            post = prev * sens / p_pos
            print(round(p_pos, 4), round(post, 4))
            """,
            """
            0.1085 0.0876
            """,
            """
            Sekitar sepuluh persen orang akan positif, tetapi hanya sekitar delapan koma delapan persen dari yang positif itu benar sakit.
            """,
            filename="uji_diagnostik.py",
        ),
        T("""
        ## Frekuensi alami

        Cara memahami hasil tadi tanpa rumus adalah memakai frekuensi alami. Bayangkan 10.000 orang. Satu persen atau 100 orang sakit, dan 95 di antaranya positif. Dari 9.900 orang sehat, 10 persen atau 990 positif palsu. Total positif 1.085, dan hanya 95 yang sakit.

        Jadi peluang sakit di antara yang positif adalah `95 / 1085`, sekitar 8,8 persen. Penjelasan dengan hitungan orang seperti ini jauh lebih mudah diterima oleh pasien dan manajer daripada rumus pecahan. Gunakan tiap kali kamu harus menjelaskan hasil Bayes kepada orang awam.
        """),
        C(
            """
            sakit = 10000 * 0.01
            tp = sakit * 0.95
            fp = (10000 - sakit) * 0.10
            print(int(tp), int(fp), round(tp / (tp + fp), 4))
            """,
            """
            95 990 0.0876
            """,
            """
            Sembilan puluh lima positif benar dan sembilan ratus sembilan puluh positif palsu, sehingga rasio positif benar terhadap seluruh positif sekitar delapan koma delapan persen.
            """,
            filename="frekuensi_alami.py",
        ),
        T("""
        ## Memperbarui berurutan

        Posterior dari satu bukti bisa menjadi prior untuk bukti berikutnya. Bila tes kedua yang independen juga positif, kita pakai posterior 8,8 persen sebagai prior baru dan ulangi rumus Bayes. Hasilnya melompat menjadi sekitar 47,7 persen, dan setelah tes ketiga sekitar 89,7 persen.

        Inilah alasan dokter meminta tes konfirmasi. Satu tes positif pada penyakit langka lemah, tetapi bukti yang saling bebas menumpuk dengan cepat. Pembaruan berurutan ini adalah inti inferensi Bayesian dan akan muncul lagi pada model yang belajar dari aliran data.
        """),
        T("""
        ## Mengomunikasikan hasil

        Hasil Bayes sering kontraintuitif sehingga cara menyampaikannya penting. Mulailah dengan frekuensi alami, seratus atau sepuluh ribu orang, lalu sebutkan berapa yang positif benar dan positif palsu. Baru setelah itu tunjukkan rumus bagi yang menginginkannya.

        Dalam laporan model klasifikasi, cantumkan prevalensi bersama presisi. Presisi model bergantung pada prevalensi, sehingga model yang tampak bagus pada data seimbang bisa menghasilkan banyak alarm palsu pada populasi nyata yang tidak seimbang.
        """),
        E(
            "A4-02-2-ex1",
            "mudah",
            """
            Tulis fungsi `peluang_total(prior, lik)` yang menerima list prior partisi dan list likelihood masing-masing, lalu mengembalikan peluang total dibulatkan 4 desimal.
            """,
            """
            def peluang_total(prior, lik):
                # TODO: implementasikan
                pass
            """,
            """
            assert peluang_total([0.6, 0.4], [0.02, 0.05]) == 0.032
            assert peluang_total([0.5, 0.5], [0.1, 0.3]) == 0.2
            assert peluang_total([1], [0.7]) == 0.7
            assert peluang_total([0.2, 0.3, 0.5], [0.1, 0.2, 0.3]) == 0.23
            """,
            "Jumlahkan hasil kali prior dan likelihood.",
            """
            def peluang_total(prior, lik):
                return round(sum(p * l for p, l in zip(prior, lik)), 4)
            """,
        ),
        E(
            "A4-02-2-ex2",
            "sedang",
            """
            Tulis fungsi `bayes(prior, lik, i)` yang mengembalikan peluang posterior skenario ke-`i` (dimulai dari 0) dibulatkan 4 desimal.
            """,
            """
            def bayes(prior, lik, i):
                # TODO: implementasikan
                pass
            """,
            """
            assert bayes([0.6, 0.4], [0.02, 0.05], 0) == 0.375
            assert bayes([0.6, 0.4], [0.02, 0.05], 1) == 0.625
            assert bayes([0.2, 0.3, 0.5], [0.1, 0.2, 0.3], 2) == 0.6522
            assert bayes([0.5, 0.5], [0.1, 0.1], 0) == 0.5
            """,
            "Bagi prior kali likelihood skenario i dengan peluang total.",
            """
            def bayes(prior, lik, i):
                total = sum(p * l for p, l in zip(prior, lik))
                return round(prior[i] * lik[i] / total, 4)
            """,
        ),
        E(
            "A4-02-2-ex3",
            "sedang",
            """
            Tulis fungsi `posterior_uji(prev, sens, spes)` yang mengembalikan peluang sakit bila hasil tes positif, dibulatkan 4 desimal. `sens` adalah peluang positif bagi yang sakit dan `spes` peluang negatif bagi yang sehat.
            """,
            """
            def posterior_uji(prev, sens, spes):
                # TODO: implementasikan
                pass
            """,
            """
            assert posterior_uji(0.01, 0.95, 0.9) == 0.0876
            assert posterior_uji(0.5, 0.9, 0.9) == 0.9
            assert posterior_uji(0.1, 0.9, 0.9) == 0.5
            assert posterior_uji(0.0, 0.9, 0.9) == 0.0
            """,
            "Positif palsu memiliki peluang satu dikurangi spesifisitas.",
            """
            def posterior_uji(prev, sens, spes):
                pos = prev * sens + (1 - prev) * (1 - spes)
                return round(prev * sens / pos, 4)
            """,
        ),
        E(
            "A4-02-2-ex4",
            "menantang",
            """
            Tulis fungsi `posterior_berurutan(prev, sens, spes, n)` yang memperbarui peluang sakit setelah `n` tes positif independen secara berurutan, memakai posterior tiap tes sebagai prior tes berikutnya. Bulatkan 4 desimal. Untuk `n = 0` kembalikan prior.
            """,
            """
            def posterior_berurutan(prev, sens, spes, n):
                # TODO: implementasikan
                pass
            """,
            """
            assert posterior_berurutan(0.01, 0.95, 0.9, 0) == 0.01
            assert posterior_berurutan(0.01, 0.95, 0.9, 1) == 0.0876
            assert posterior_berurutan(0.01, 0.95, 0.9, 2) == 0.4769
            assert posterior_berurutan(0.01, 0.95, 0.9, 3) == 0.8965
            assert posterior_berurutan(0.01, 0.99, 0.99, 2) == 0.99
            """,
            "Ulangi rumus Bayes n kali dengan posterior sebelumnya sebagai prior.",
            """
            def posterior_berurutan(prev, sens, spes, n):
                p = prev
                for _ in range(n):
                    p = p * sens / (p * sens + (1 - p) * (1 - spes))
                return round(p, 4)
            """,
        ),
    ],
    [
        M("Mengabaikan prior dan menganggap sensitivitas sama dengan posterior.", "Hitung dengan Bayes."),
        M("Lupa normalisasi dengan peluang total.", "Bagi dengan P(A) dari hukum total."),
        M("Menjumlahkan skenario yang tidak membentuk partisi.", "Skenario harus lepas dan lengkap."),
    ],
    [
        Q("Hukum peluang total menjumlahkan?", ["P(A|Bi)P(Bi)", "P(Bi)", "P(A)", "P(A|Bi)"], 0, "Bobot tiap skenario.", hint="Prior kali likelihood."),
        Q("Posterior sebanding dengan?", ["Prior kali likelihood", "Prior saja", "Likelihood saja", "Prior dibagi likelihood"], 0, "Rumus Bayes.", hint="Perkalian."),
        Q("Mengapa positif palsu mendominasi pada penyakit langka?", ["Tes buruk", "Banyak orang sehat", "Prior tinggi", "Sensitivitas nol"], 1, "Persen kecil dari kelompok besar.", hint="Basis besar."),
        Q("Spesifisitas adalah peluang?", ["Positif bagi sakit", "Negatif bagi sehat", "Sakit bagi positif", "Sehat bagi negatif"], 1, "Mengenali yang sehat.", hint="Sehat."),
        Q("Mengapa tes konfirmasi berguna?", ["Mengganti prior", "Bukti independen menumpuk", "Mengurangi biaya", "Meniadakan error"], 1, "Posterior menjadi prior baru.", hint="Berurutan."),
    ],
    [
        "Hukum peluang total menggabungkan skenario menjadi peluang tunggal.",
        "Bayes membalik syarat dengan prior, likelihood, dan normalisasi.",
        "Prevalensi rendah membuat positif palsu mendominasi.",
        "Bukti independen dapat diperbarui berurutan.",
    ],
    [],
)

l3 = lesson(
    "A4-02-3",
    "Bayes dalam praktik: filter spam dan Naive Bayes",
    35,
    [
        "Menerapkan Bayes untuk klasifikasi teks sederhana",
        "Memakai asumsi independen bersyarat Naive Bayes",
        "Mencegah underflow dengan log peluang",
        "Memakai smoothing Laplace untuk kata tak terlihat",
    ],
    [
        T("""
        ## Dari teorema ke klasifier

        Teorema Bayes dapat langsung dipakai sebagai klasifier. Untuk email dengan kata tertentu, kita ingin `P(spam | kata)`. Kita biasanya mudah mengestimasi arah sebaliknya dari data berlabel: seberapa sering kata itu muncul di email spam dan di email biasa. Bayes membalik keduanya menjadi peluang spam yang kita inginkan.

        Dengan satu kata, rumusnya persis seperti di pelajaran sebelumnya. Prior adalah proporsi spam, likelihood adalah frekuensi kata pada tiap kelas. Hasilnya posterior yang menyatakan seberapa mencurigakan email itu berdasarkan kata tersebut.
        """),
        C(
            """
            prior = 0.4
            p_kata_spam = 0.5
            p_kata_ham = 0.05
            spam = prior * p_kata_spam
            ham = (1 - prior) * p_kata_ham
            print(round(spam / (spam + ham), 4))
            """,
            """
            0.8696
            """,
            """
            Kata gratis jauh lebih sering di spam, sehingga email berkata itu memiliki peluang spam sekitar delapan puluh tujuh persen.
            """,
            filename="spam_satu_kata.py",
        ),
        T("""
        ## Banyak kata dan asumsi naif

        Email memiliki banyak kata, dan kombinasi kata sangat banyak. Menaksir peluang kombinasi lengkap butuh data yang tidak realistis. **Naive Bayes** menyederhanakan dengan asumsi bahwa kata-kata independen satu sama lain **bila kelas diketahui**. Maka likelihood seluruh email adalah hasil kali likelihood tiap kata.

        Asumsi ini jelas tidak sepenuhnya benar, karena kata gratis dan menang cenderung muncul bersama. Namun dalam praktik klasifier tetap bekerja baik karena yang dibutuhkan hanya urutan peringkat kelas yang benar, bukan peluang yang akurat sempurna. Kesederhanaan membuatnya cepat dilatih dan tahan terhadap data sedikit.
        """),
        C(
            """
            prior = 0.4
            spam_k = [0.5, 0.3]
            ham_k = [0.05, 0.02]
            s = prior
            for p in spam_k:
                s *= p
            h = 1 - prior
            for p in ham_k:
                h *= p
            print(round(s / (s + h), 4))
            """,
            """
            0.9901
            """,
            """
            Dua kata yang sama-sama dominan di spam menaikkan peluang spam menjadi sekitar sembilan puluh sembilan persen.
            """,
            filename="spam_dua_kata.py",
        ),
        T("""
        ## Underflow dan log

        Mengalikan banyak peluang kecil menghasilkan bilangan yang sangat kecil. Seratus kata dengan peluang masing-masing 0,01 menghasilkan `1e-200`, dan dua ratus kata menghasilkan nilai di bawah batas representasi float, yang dibulatkan menjadi nol. Peristiwa ini disebut **underflow** dan membuat dua kelas sama-sama bernilai nol sehingga tidak bisa dibandingkan.

        Solusi standar adalah bekerja dengan logaritma. Logaritma mengubah perkalian menjadi penjumlahan: `log(a * b) = log(a) + log(b)`. Karena log monoton naik, kelas dengan skor log terbesar juga kelas dengan peluang terbesar. Semua implementasi Naive Bayes yang serius memakai log peluang.
        """),
        C(
            """
            import math

            print(0.01 ** 200)
            print(round(200 * math.log(0.01), 2))
            """,
            """
            0.0
            -921.03
            """,
            """
            Hasil kali langsung menjadi nol karena underflow, sedangkan jumlah log tetap bilangan wajar yang bisa dibandingkan.
            """,
            filename="underflow.py",
        ),
        T("""
        ## Smoothing Laplace

        Masalah lain muncul bila sebuah kata tidak pernah terlihat di data latih untuk kelas tertentu. Estimasi frekuensinya nol, dan karena semua dikalikan, satu kata asing meniadakan seluruh skor kelas itu menjadi nol. Padahal kata baru mungkin saja muncul pada email spam yang asli.

        **Smoothing Laplace** menambahkan hitungan semu pada tiap kata: `p = (hitung + alpha) / (total + alpha * k)`, dengan `k` banyaknya kemungkinan nilai dan `alpha` biasanya satu. Estimasi tidak pernah nol dan, bila data banyak, hampir tidak berbeda dari frekuensi asli. Ini sama dengan menyatakan prior lemah bahwa semua kata mungkin muncul.
        """),
        C(
            """
            def laplace(hitung, total, alpha=1, k=2):
                return (hitung + alpha) / (total + alpha * k)

            print(round(laplace(0, 100), 4))
            print(round(laplace(50, 100), 4))
            """,
            """
            0.0098
            0.5
            """,
            """
            Kata yang tidak pernah terlihat tetap mendapat peluang kecil positif, sedangkan frekuensi seimbang tidak berubah.
            """,
            filename="smoothing.py",
        ),
        K(
            "tip",
            """
            Naive Bayes adalah baseline teks yang sangat baik. Latih dalam hitungan detik, bandingkan dengan model rumit, dan pakai log peluang serta smoothing sejak awal.
            """,
            title="Baseline cepat",
        ),
        T("""
        ## Kekuatan dan batas

        Naive Bayes cepat, butuh data sedikit, dan mudah diinterpretasikan: kamu bisa melihat kata mana yang paling menyumbang ke skor spam. Ia cocok untuk klasifikasi teks, filter spam, dan baseline awal. Peluang posterior yang dihasilkan sering terlalu ekstrem mendekati nol atau satu, jadi jangan diperlakukan sebagai peluang terkalibrasi.

        Batasnya muncul ketika fitur saling bergantung kuat. Model yang menangkap interaksi, seperti regresi logistik atau pohon keputusan, sering lebih akurat. Namun nilai Naive Bayes sebagai pembanding pertama tetap sulit disaingi dalam hal kesederhanaan.
        """),
        T("""
        ## Alur lengkap pelatihan

        Melatih Naive Bayes untuk teks mengikuti langkah yang pendek. Pecah tiap dokumen menjadi kata, hitung berapa kali tiap kata muncul pada tiap kelas, terapkan smoothing Laplace, lalu simpan log peluang per kata dan log prior per kelas. Seluruh pelatihan hanya satu kali melewati data.

        Saat prediksi, jumlahkan log prior dengan log peluang tiap kata dokumen untuk setiap kelas dan pilih kelas bernilai terbesar. Kata yang tidak ada di kosakata biasanya diabaikan. Karena hanya penjumlahan, prediksi sangat cepat dan cocok dijalankan langsung di perangkat tanpa server.
        """),
        T("""
        ## Memilih fitur teks

        Pilihan fitur memengaruhi hasil sama besarnya dengan pilihan model. Representasi kantong kata menghitung kemunculan, sedangkan versi biner hanya mencatat ada atau tidaknya kata. Menghapus kata sangat umum seperti dan atau yang sering membantu, dan menormalkan huruf kecil mengurangi kosakata tanpa kehilangan banyak makna.

        Bandingkan beberapa variasi dengan validasi silang pada data berlabelmu sendiri, karena bahasa Indonesia informal dan singkatan membuat aturan bawaan dari bahasa lain kurang cocok.
        """),
        T("""
        ## Mengevaluasi klasifier

        Akurasi saja menyesatkan bila spam hanya sepuluh persen email, karena klasifier yang selalu menjawab bukan spam sudah mencapai sembilan puluh persen. Gunakan presisi, yaitu berapa banyak yang ditandai spam benar-benar spam, dan recall, yaitu berapa banyak spam yang tertangkap. Pilih keseimbangan sesuai biaya: menandai email penting sebagai spam biasanya lebih mahal daripada membiarkan satu spam lolos.
        """),
        E(
            "A4-02-3-ex1",
            "mudah",
            """
            Tulis fungsi `posterior_spam(prior, p_kata_spam, p_kata_ham)` yang mengembalikan peluang spam bila sebuah kata muncul, dibulatkan 4 desimal. `prior` adalah peluang awal spam.
            """,
            """
            def posterior_spam(prior, p_kata_spam, p_kata_ham):
                # TODO: implementasikan
                pass
            """,
            """
            assert posterior_spam(0.4, 0.5, 0.05) == 0.8696
            assert posterior_spam(0.5, 0.5, 0.5) == 0.5
            assert posterior_spam(0.1, 0.9, 0.1) == 0.5
            assert posterior_spam(0.4, 0, 0.05) == 0.0
            """,
            "Bandingkan skor spam dan skor bukan spam lalu normalisasikan.",
            """
            def posterior_spam(prior, p_kata_spam, p_kata_ham):
                s = prior * p_kata_spam
                h = (1 - prior) * p_kata_ham
                return round(s / (s + h), 4)
            """,
        ),
        E(
            "A4-02-3-ex2",
            "sedang",
            """
            Tulis fungsi `posterior_banyak(prior, pk_spam, pk_ham)` untuk list peluang kata di kelas spam dan bukan spam yang diasumsikan independen bersyarat. Kembalikan peluang spam dibulatkan 4 desimal.
            """,
            """
            def posterior_banyak(prior, pk_spam, pk_ham):
                # TODO: implementasikan
                pass
            """,
            """
            assert posterior_banyak(0.4, [0.5, 0.3], [0.05, 0.02]) == 0.9901
            assert posterior_banyak(0.4, [], []) == 0.4
            assert posterior_banyak(0.5, [0.2], [0.2]) == 0.5
            assert posterior_banyak(0.4, [0.5], [0.05]) == 0.8696
            """,
            "Kalikan prior dengan semua peluang kata tiap kelas lalu normalisasikan.",
            """
            def posterior_banyak(prior, pk_spam, pk_ham):
                s = prior
                for p in pk_spam:
                    s *= p
                h = 1 - prior
                for p in pk_ham:
                    h *= p
                return round(s / (s + h), 4)
            """,
        ),
        E(
            "A4-02-3-ex3",
            "sedang",
            """
            Tulis fungsi `laplace(hitung, total, alpha=1, k=2)` yang mengembalikan estimasi `(hitung + alpha) / (total + alpha * k)` dibulatkan 4 desimal.
            """,
            """
            def laplace(hitung, total, alpha=1, k=2):
                # TODO: implementasikan
                pass
            """,
            """
            assert laplace(0, 100) == 0.0098
            assert laplace(50, 100) == 0.5
            assert laplace(10, 20, 1, 2) == 0.5
            assert laplace(0, 10, 1, 3) == 0.0769
            assert laplace(3, 10, 0.5, 2) == 0.3182
            """,
            "Tambahkan alpha pada pembilang dan alpha kali k pada penyebut.",
            """
            def laplace(hitung, total, alpha=1, k=2):
                return round((hitung + alpha) / (total + alpha * k), 4)
            """,
        ),
        E(
            "A4-02-3-ex4",
            "menantang",
            """
            Tulis fungsi `klasifikasi(prior, kata, tabel)` yang menerima dict prior kelas, list kata, dan dict tabel berisi peluang tiap kata per kelas. Kembalikan nama kelas dengan skor log terbesar (log prior ditambah jumlah log peluang kata). Harus tetap benar untuk daftar kata yang sangat panjang.
            """,
            """
            import math

            def klasifikasi(prior, kata, tabel):
                # TODO: implementasikan
                pass
            """,
            """
            prior = {'spam': 0.4, 'ham': 0.6}
            tabel = {'spam': {'gratis': 0.5, 'menang': 0.3, 'rapat': 0.01}, 'ham': {'gratis': 0.05, 'menang': 0.02, 'rapat': 0.4}}
            assert klasifikasi(prior, ['gratis', 'menang'], tabel) == 'spam'
            assert klasifikasi(prior, ['rapat'], tabel) == 'ham'
            assert klasifikasi(prior, ['gratis', 'rapat'], tabel) == 'ham'
            assert klasifikasi(prior, [], tabel) == 'ham'
            assert klasifikasi(prior, ['gratis', 'rapat'] * 400, tabel) == 'ham'
            """,
            "Jumlahkan log peluang daripada mengalikan peluang agar tidak underflow.",
            """
            import math

            def klasifikasi(prior, kata, tabel):
                def skor(c):
                    return math.log(prior[c]) + sum(math.log(tabel[c][w]) for w in kata)
                return max(prior, key=skor)
            """,
        ),
    ],
    [
        M("Mengalikan banyak peluang kecil langsung.", "Pakai jumlah log peluang."),
        M("Membiarkan peluang kata nol.", "Terapkan smoothing Laplace."),
        M("Menganggap posterior Naive Bayes terkalibrasi.", "Pakai untuk peringkat, kalibrasi terpisah."),
    ],
    [
        Q("Naive Bayes mengasumsikan fitur?", ["Sama", "Independen bersyarat pada kelas", "Berkorelasi", "Konstan"], 1, "Independen diberikan kelas.", hint="Naif."),
        Q("Mengapa memakai log peluang?", ["Agar lebih besar", "Mencegah underflow", "Menambah data", "Menghapus prior"], 1, "Perkalian jadi penjumlahan.", hint="Bilangan sangat kecil."),
        Q("Smoothing Laplace mencegah?", ["Peluang nol", "Peluang satu", "Overfitting data", "Prior"], 0, "Menambah hitungan semu.", hint="Kata baru."),
        Q("Kelas dipilih dengan?", ["Skor log terbesar", "Skor terkecil", "Acak", "Prior saja"], 0, "Log monoton naik.", hint="Maksimum."),
        Q("Kelebihan Naive Bayes?", ["Akurat selalu", "Cepat dan sederhana", "Tanpa asumsi", "Kalibrasi sempurna"], 1, "Baseline kuat.", hint="Sederhana."),
    ],
    [
        "Bayes membalik peluang kata di tiap kelas menjadi peluang kelas.",
        "Naive Bayes mengalikan peluang kata dengan asumsi independen bersyarat.",
        "Log peluang mencegah underflow.",
        "Smoothing Laplace menghindari peluang nol.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perhitungan yang cukup jelas dalam teks.", "brief": []}

write_module(
    "A4",
    2,
    "Peluang bersyarat dan teorema Bayes",
    105,
    [
        "Menghitung peluang bersyarat",
        "Menerapkan hukum peluang total dan teorema Bayes",
        "Membangun klasifier Naive Bayes sederhana",
    ],
    [l1, l2, l3],
    video,
    REF,
)
