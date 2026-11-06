import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, C, E, Q, M, lesson, write_module

REF = [{"book": "Machine Learning Yearning (Andrew Ng)", "chapters": "bab 1 sampai 4"}]

l1 = lesson(
    "D11-01-1",
    "Dilema memilih arah perbaikan",
    30,
    [
        "Menjelaskan mengapa memilih arah perbaikan tanpa diagnosis bisa membuang berbulan-bulan",
        "Menyusun daftar ide perbaikan lalu memberi skor prioritas dari peluang, potensi, dan biaya",
        "Membedakan sinyal bias dan variance dari error training dan error dev",
        "Memakai pendekatan course ini untuk meyakinkan rekan satu tim",
    ],
    [
        T("""
        ## Skenario: detektor kucing yang belum cukup akurat

        Bayangkan kamu membangun startup yang menyajikan foto kucing tanpa henti untuk para pecinta kucing. Inti produknya adalah sebuah jaringan saraf yang mendeteksi kucing di dalam gambar. Masalahnya, akurasinya belum cukup bagus, dan tekanan untuk memperbaikinya datang dari segala arah.

        Tim kamu punya banyak ide. Kumpulkan lebih banyak foto kucing. Kumpulkan data yang lebih beragam, misalnya kucing dengan pose tidak biasa, warna bulu aneh, atau foto dari berbagai pengaturan kamera. Latih algoritma lebih lama dengan lebih banyak iterasi gradient descent. Coba jaringan yang lebih besar dengan lebih banyak layer atau unit. Atau justru coba jaringan yang lebih kecil. Tambahkan regularisasi seperti L2. Ubah arsitektur, misalnya fungsi aktivasi dan jumlah hidden unit.

        Semua ide itu masuk akal. Itulah masalahnya. Jika kamu memilih dengan baik, kamu membangun platform foto kucing terbaik. Jika kamu memilih dengan buruk, kamu bisa menghabiskan berbulan-bulan untuk sesuatu yang tidak menggerakkan angka sama sekali.

        Hampir setiap masalah machine learning meninggalkan petunjuk tentang apa yang layak dicoba dan apa yang tidak. Course ini mengajarkan cara membaca petunjuk itu. Keterampilan ini sering menghemat berbulan-bulan atau bahkan bertahun-tahun waktu pengembangan, dan itu sebabnya modul pertama ini berhenti dulu pada pertanyaan sederhana: bagaimana cara memilih langkah berikutnya?
        """),
        T("""
        ## Setiap ide punya harga dan peluang

        Sebuah ide perbaikan tidak gratis. Mengumpulkan data baru bisa memakan berminggu-minggu. Menambah regularisasi mungkin cukup satu sore. Di sisi lain, tidak semua ide punya peluang berhasil yang sama, dan tidak semua ide kalau berhasil akan memberi dampak sebesar yang lain.

        Cara berpikir yang berguna adalah memberi tiga angka pada setiap ide.

        - **Peluang berhasil** (p): seberapa yakin kamu bahwa ide ini benar-benar menurunkan error pada masalahmu, antara 0 dan 1.
        - **Potensi perbaikan** (g): jika berhasil, berapa poin persen error turun.
        - **Biaya** (c): berapa hari kerja yang dibutuhkan.

        Skor prioritas sederhana adalah nilai harapan per hari kerja: `skor = p * g / c`. Ide dengan skor tertinggi dikerjakan lebih dulu. Angka-angka ini adalah tebakan terdidik, bukan fakta. Nilai pentingnya bukan ketepatan rumus, melainkan kebiasaan memaksa tim menuliskan asumsi dan membandingkan ide secara eksplisit sebelum menghabiskan hari kerja.

        Skor ini juga heuristik, bukan jaminan optimal. Di akhir lesson kamu akan melihat contoh kecil di mana urutan berdasarkan skor ternyata bukan urutan tercepat menuju target. Itu tidak mengurangi manfaatnya, tetapi mengingatkan bahwa kita sedang memandu keputusan, bukan menghitung kebenaran mutlak.
        """),
        T("""
        ## Diagnosis sebelum aksi

        Angka p dan g tidak boleh dikarang. Sumber terbaiknya adalah diagnosis: pengamatan sederhana atas perilaku model yang menunjukkan masalah apa yang sebenarnya sedang kamu hadapi.

        Dua pengamatan paling murah adalah error pada data training dan error pada data dev. Jika error training sudah tinggi, model bahkan tidak mampu mencocokkan data yang ia lihat sendiri. Menambah data hampir tidak akan membantu, karena masalahnya ada pada kapasitas atau cara berlatih. Jika error training rendah tetapi error dev jauh lebih tinggi, model menghafal training dan gagal menggeneralisasi. Di sini data tambahan atau regularisasi justru sangat relevan.

        Dua kondisi itu dikenal sebagai **bias** dan **variance**. Kamu akan mempelajarinya mendalam di modul 5. Untuk saat ini cukup pegang prinsipnya: satu ide perbaikan bisa sangat efektif pada satu diagnosis dan sia-sia pada diagnosis lain. Memilih ide tanpa diagnosis sama seperti minum obat tanpa tahu penyakitnya.

        Pengamatan kedua yang akan kamu pelajari di modul 4 adalah error analysis: melihat contoh yang salah diprediksi satu per satu, lalu mengelompokkannya. Itu memberi batas atas yang jujur tentang berapa banyak yang bisa diperoleh dari sebuah ide.
        """),
        K(
            "tip",
            """
            Sebelum menjalankan eksperimen yang butuh lebih dari satu hari, tulis satu kalimat: ide ini kuharapkan menurunkan error dari X ke Y karena diagnosis Z. Kalau kamu tidak bisa menuliskan diagnosis Z, kamu belum siap memulai eksperimen itu.
            """,
        ),
        T("""
        ## Cara memakai course ini bersama tim

        Setelah menyelesaikan course ini kamu akan paham cara menentukan arah teknis sebuah proyek machine learning. Tetapi rekan tim belum tentu paham mengapa kamu menyarankan suatu arah. Mungkin kamu ingin tim menetapkan satu metrik evaluasi, tetapi mereka belum yakin. Bagaimana kamu meyakinkan mereka?

        Karena itu lesson di course ini sengaja dibuat berdiri sendiri. Kamu bisa membuka satu lesson, mencetak ringkasannya, dan memintanya dibaca rekan tim. Beberapa perubahan kecil dalam prioritas dapat memberi dampak besar pada produktivitas tim. Dengan membantu tim melakukan beberapa perubahan itu, kamu bisa menjadi pahlawan tim.

        Tiap lesson punya contoh kode yang bisa dijalankan langsung di app, beberapa latihan bertingkat dengan uji otomatis, kuis, dan ringkasan. Kerjakan latihan sebelum membuka solusi, karena di situlah pemahaman terbentuk.
        """),
        C(
            """
            ide = {
                "data_baru": (0.5, 3.0, 20),
                "model_lebih_besar": (0.4, 2.0, 5),
                "regularisasi": (0.3, 1.0, 1),
                "augmentasi": (0.6, 1.5, 4),
            }
            skor = {nama: p * g / c for nama, (p, g, c) in ide.items()}
            for nama, nilai in sorted(skor.items(), key=lambda kv: -kv[1]):
                print(f"{nama:20s} {nilai:.3f}")
            """,
            """
            regularisasi         0.300
            augmentasi           0.225
            model_lebih_besar    0.160
            data_baru            0.075
            """,
            """
            Setiap ide diwakili tiga angka: peluang berhasil, potensi perbaikan dalam poin persen, dan biaya dalam hari. Skor adalah nilai harapan per hari. Perhatikan bahwa ide dengan potensi terbesar, yaitu data baru, justru berada paling bawah karena biayanya 20 hari. Prioritas ditentukan oleh perbandingan dampak terhadap biaya, bukan dampak saja.
            """,
        ),
        C(
            """
            import numpy as np

            ide = [("a", 1.0, 10), ("b", 0.5, 1), ("c", 2.0, 8), ("d", 0.8, 2), ("e", 1.5, 3)]
            target = 3.0
            rng = np.random.default_rng(0)

            def hari_sampai_target(urutan):
                total, hari = 0.0, 0
                for _, efek, biaya in urutan:
                    total += efek
                    hari += biaya
                    if total >= target:
                        return hari
                return hari

            acak = [hari_sampai_target([ide[i] for i in rng.permutation(len(ide))]) for _ in range(2000)]
            terurut = sorted(ide, key=lambda x: -x[1] / x[2])
            print("rata-rata urutan acak:", round(float(np.mean(acak)), 1))
            print("urutan berdasarkan skor:", hari_sampai_target(terurut))
            """,
            """
            rata-rata urutan acak: sekitar 15
            urutan berdasarkan skor: 14
            """,
            """
            Lima ide dengan efek dan biaya tetap dicoba dalam urutan acak sebanyak 2000 kali, lalu dibandingkan dengan urutan berdasarkan rasio efek per biaya. Urutan berdasarkan skor biasanya lebih cepat daripada rata-rata acak. Tetapi lihat bahwa hasilnya 14 hari, padahal ada urutan lain yang mencapai target lebih cepat. Skor rasio adalah heuristik yang bagus, bukan algoritma optimal.
            """,
        ),
        C(
            """
            import numpy as np
            from sklearn.datasets import make_classification
            from sklearn.linear_model import LogisticRegression

            X, y = make_classification(n_samples=3000, n_features=20, n_informative=8, flip_y=0.05, random_state=0)
            X_tr, y_tr = X[:2000], y[:2000]
            X_dev, y_dev = X[2000:], y[2000:]

            model = LogisticRegression(max_iter=1000).fit(X_tr, y_tr)
            err_train = 1 - model.score(X_tr, y_tr)
            err_dev = 1 - model.score(X_dev, y_dev)
            print("error train:", round(err_train, 3))
            print("error dev  :", round(err_dev, 3))
            print("selisih dev dan train:", round(err_dev - err_train, 3))
            """,
            """
            error train sekitar 0.09
            error dev sekitar 0.08
            selisih dev dan train sangat kecil
            """,
            """
            Dua angka sederhana sudah memberi petunjuk. Selisih antara error dev dan error training hampir nol, artinya variance bukan masalah utama dan menambah data tidak akan banyak membantu. Apakah error training sekitar 9 persen itu masalah, bergantung pada targetmu. Data ini sengaja diberi 5 persen label acak yang salah, jadi error di bawah sekitar 5 persen mustahil dicapai. Jika targetmu 6 persen, celah bias masih ada dan yang perlu diubah adalah kapasitas model atau fiturnya. Angka pastinya bisa sedikit berbeda antar versi library.
            """,
        ),
        E(
            "D11-01-1-ex1",
            "mudah",
            """
            Hitung skor prioritas `p * g / c` untuk setiap ide pada dictionary `ide`, lalu simpan nama ide yang diurutkan dari skor tertinggi ke terendah pada list `ranking`.
            """,
            """
            ide = {
                "data_baru": (0.5, 3.0, 20),
                "model_lebih_besar": (0.4, 2.0, 5),
                "regularisasi": (0.3, 1.0, 1),
                "augmentasi": (0.6, 1.5, 4),
            }
            ranking = None
            # TODO: isi ranking
            """,
            """
            assert isinstance(ranking, list)
            assert ranking == ["regularisasi", "augmentasi", "model_lebih_besar", "data_baru"]
            assert ranking[0] == "regularisasi" and ranking[-1] == "data_baru"
            assert len(ranking) == len(ide)
            """,
            "Buat dictionary skor dulu, lalu urutkan kunci-kuncinya dengan sorted dan key yang mengambil skor, dengan reverse=True.",
            """
            ide = {
                "data_baru": (0.5, 3.0, 20),
                "model_lebih_besar": (0.4, 2.0, 5),
                "regularisasi": (0.3, 1.0, 1),
                "augmentasi": (0.6, 1.5, 4),
            }
            skor = {n: p * g / c for n, (p, g, c) in ide.items()}
            ranking = sorted(skor, key=lambda n: skor[n], reverse=True)
            """,
        ),
        E(
            "D11-01-1-ex2",
            "sedang",
            """
            Tulis fungsi `pilih_ide(ide, anggaran_hari)` yang memilih ide secara greedy: urutkan berdasarkan skor, lalu ambil ide selama total biaya tidak melebihi anggaran. Fungsi mengembalikan tuple `(terpilih, gain)` dengan `terpilih` berupa list nama ide sesuai urutan pengambilan dan `gain` jumlah `p * g` ide terpilih. Ide yang tidak muat dilewati, tetapi pemeriksaan tetap berlanjut ke ide berikutnya.
            """,
            """
            def pilih_ide(ide, anggaran_hari):
                # TODO: implementasikan
                pass
            """,
            """
            ide = {
                "data_baru": (0.5, 3.0, 20),
                "model_lebih_besar": (0.4, 2.0, 5),
                "regularisasi": (0.3, 1.0, 1),
                "augmentasi": (0.6, 1.5, 4),
            }
            terpilih, gain = pilih_ide(ide, 10)
            assert terpilih == ["regularisasi", "augmentasi", "model_lebih_besar"]
            assert abs(gain - 2.0) < 1e-9
            terpilih2, gain2 = pilih_ide(ide, 0)
            assert terpilih2 == [] and gain2 == 0
            terpilih3, _ = pilih_ide(ide, 25)
            assert terpilih3 == ["regularisasi", "augmentasi", "model_lebih_besar", "data_baru"] or terpilih3 == ["regularisasi", "augmentasi", "model_lebih_besar"]
            """,
            "Urutkan nama ide berdasarkan skor, kumpulkan sisa anggaran, dan hanya tambahkan ide bila biayanya masih muat.",
            """
            def pilih_ide(ide, anggaran_hari):
                urut = sorted(ide, key=lambda n: ide[n][0] * ide[n][1] / ide[n][2], reverse=True)
                sisa = anggaran_hari
                terpilih = []
                gain = 0.0
                for n in urut:
                    p, g, c = ide[n]
                    if c <= sisa:
                        terpilih.append(n)
                        sisa -= c
                        gain += p * g
                return terpilih, gain
            """,
        ),
        E(
            "D11-01-1-ex3",
            "sedang",
            """
            Tulis fungsi `diagnosis(err_train, err_dev, err_target)`. Hitung `celah_bias = err_train - err_target` dan `celah_var = err_dev - err_train`, keduanya dibulatkan ke 6 desimal. Kembalikan `"bias"` jika celah bias lebih besar, `"variance"` jika celah variance lebih besar, dan `"seimbang"` jika sama.
            """,
            """
            def diagnosis(err_train, err_dev, err_target):
                # TODO: implementasikan
                pass
            """,
            """
            assert diagnosis(0.15, 0.16, 0.05) == "bias"
            assert diagnosis(0.06, 0.20, 0.05) == "variance"
            assert diagnosis(0.10, 0.15, 0.05) == "seimbang"
            assert diagnosis(0.05, 0.05, 0.05) == "seimbang"
            """,
            "Gunakan round(nilai, 6) pada kedua celah sebelum dibandingkan agar selisih desimal tidak membuat hasil keliru.",
            """
            def diagnosis(err_train, err_dev, err_target):
                celah_bias = round(err_train - err_target, 6)
                celah_var = round(err_dev - err_train, 6)
                if celah_bias > celah_var:
                    return "bias"
                if celah_var > celah_bias:
                    return "variance"
                return "seimbang"
            """,
        ),
        E(
            "D11-01-1-ex4",
            "menantang",
            """
            Dengan `ide` berupa list `(nama, efek, biaya)` dan `target = 3.0`, hitung dua angka. `hari_greedy` adalah hari yang dibutuhkan bila ide dikerjakan berurutan menurut rasio efek per biaya (urutan stabil, rasio terbesar lebih dulu) sampai total efek mencapai target. `hari_terbaik` adalah hari minimum yang mungkin dari semua urutan ide (brute force dengan `itertools.permutations`). Hari dihitung sebagai total biaya sampai total efek pertama kali mencapai target.
            """,
            """
            import itertools

            ide = [("a", 1.0, 10), ("b", 0.5, 1), ("c", 2.0, 8), ("d", 0.8, 2), ("e", 1.5, 3)]
            target = 3.0

            def hari_sampai(urutan):
                # TODO: kembalikan total hari sampai efek >= target
                pass

            hari_greedy = None
            hari_terbaik = None
            # TODO: isi hari_greedy dan hari_terbaik
            """,
            """
            assert hari_greedy == 14
            assert hari_terbaik == 11
            assert hari_terbaik < hari_greedy
            """,
            "Fungsi hari_sampai menjumlahkan efek dan biaya sambil berjalan di urutan, lalu berhenti begitu efek >= target. Untuk brute force, ambil min dari hari_sampai atas semua permutasi.",
            """
            import itertools

            ide = [("a", 1.0, 10), ("b", 0.5, 1), ("c", 2.0, 8), ("d", 0.8, 2), ("e", 1.5, 3)]
            target = 3.0

            def hari_sampai(urutan):
                efek, hari = 0.0, 0
                for _, e, c in urutan:
                    efek += e
                    hari += c
                    if efek >= target:
                        return hari
                return hari

            hari_greedy = hari_sampai(sorted(ide, key=lambda x: -x[1] / x[2]))
            hari_terbaik = min(hari_sampai(p) for p in itertools.permutations(ide))
            """,
        ),
    ],
    [
        M(
            "Mengerjakan ide yang paling mudah atau paling populer tanpa melihat diagnosis.",
            "Cek dulu error training dan error dev, lalu pilih ide yang cocok dengan diagnosisnya.",
        ),
        M(
            "Menganggap skor prioritas sebagai kebenaran mutlak.",
            "Perlakukan skor sebagai heuristik yang memandu diskusi, dan perbarui angkanya begitu ada hasil eksperimen baru.",
        ),
        M(
            "Selalu mengumpulkan lebih banyak data sebagai respons pertama.",
            "Data baru mahal dan hanya membantu bila masalahnya variance. Periksa dulu apakah error training sudah rendah.",
        ),
    ],
    [
        Q(
            "Mengapa memilih arah perbaikan secara acak berbahaya bagi proyek ML?",
            ["Model akan selalu gagal", "Beberapa ide bisa memakan berminggu-minggu tanpa menggerakkan metrik", "Data akan rusak", "Library akan error"],
            1,
            "Setiap ide punya biaya waktu. Tanpa diagnosis, tim bisa menghabiskan lama untuk ide yang tidak relevan dengan masalah sebenarnya.",
        ),
        Q(
            "Dalam skor `p * g / c`, apa arti `c`?",
            ["Peluang berhasil", "Potensi perbaikan", "Biaya dalam hari kerja", "Jumlah kelas"],
            2,
            "c adalah biaya. Skor adalah nilai harapan perbaikan per hari kerja.",
        ),
        Q(
            "Error training 20 persen, error dev 21 persen, target 5 persen. Masalah utamanya?",
            ["Variance tinggi", "Bias tinggi", "Data dev bocor", "Tidak ada masalah"],
            1,
            "Model tidak mampu mencocokkan data training sendiri, jadi celah terhadap target ada pada bias.",
        ),
        Q(
            "Error training 6 persen, error dev 20 persen, target 5 persen. Ide apa yang paling relevan?",
            ["Memperbesar model tanpa regularisasi", "Menambah data atau regularisasi", "Mengurangi data", "Menghapus fitur dev"],
            1,
            "Celah besar antara training dan dev adalah sinyal variance. Data tambahan dan regularisasi menurunkan variance.",
        ),
        Q(
            "Apa pelajaran dari contoh lima ide yang urutan skornya butuh 14 hari padahal ada urutan 11 hari?",
            ["Skor tidak berguna", "Skor adalah heuristik, bukan jaminan optimal", "Brute force selalu wajib", "Biaya tidak penting"],
            1,
            "Urutan berdasarkan rasio itu bagus sebagai panduan cepat, tetapi untuk target tertentu urutan lain bisa lebih cepat.",
        ),
    ],
    [
        "Banyak ide perbaikan itu normal, tantangannya memilih yang tepat.",
        "Beri tiap ide peluang, potensi, dan biaya, lalu urutkan dengan skor nilai harapan per hari.",
        "Diagnosis dari error training dan error dev menentukan ide mana yang relevan.",
        "Skor prioritas adalah heuristik yang memandu keputusan, bukan kebenaran mutlak.",
    ],
    ["Machine Learning Yearning, bab 1 dan 2 (Andrew Ng): motivasi strategi ML dan cara memakai buku bersama tim"],
)

l2 = lesson(
    "D11-01-2",
    "Prasyarat dan notasi supervised learning",
    30,
    [
        "Menyatakan definisi supervised learning dengan notasi x, y, dan m",
        "Membagi data menjadi training, dev, dan test secara manual",
        "Menghitung error rate dan memahami prediksi regresi logistik secara eksplisit",
    ],
    [
        T("""
        ## Supervised learning dalam satu halaman

        Course ini mengasumsikan kamu sudah akrab dengan **supervised learning**: mempelajari fungsi yang memetakan masukan `x` ke keluaran `y` menggunakan contoh berlabel `(x, y)`. Contohnya klasifikasi gambar menjadi kucing atau bukan, memprediksi harga rumah, atau menandai email sebagai spam. Algoritma supervised yang umum mencakup regresi linear, regresi logistik, dan jaringan saraf.

        Ada banyak bentuk machine learning, tetapi sebagian besar nilai praktisnya hari ini berasal dari supervised learning. Itu sebabnya strategi pada course ini berfokus di sana. Bila kamu belum nyaman dengan konsepnya, selesaikan dulu course Supervised Learning Foundations (D1), terutama modul kerangka supervised learning dan train test split.

        Jaringan saraf dalam atau deep learning akan sering disebut. Kamu hanya perlu pemahaman dasar bahwa jaringan saraf adalah keluarga model yang sangat fleksibel dan kapasitasnya bisa dinaikkan dengan menambah layer dan unit. Detailnya dibahas di track E.
        """),
        T("""
        ## Notasi yang dipakai di seluruh course

        Notasi berikut dipakai konsisten supaya diskusi tentang data dan error tidak ambigu.

        - `m` adalah jumlah contoh. Dengan subscript: `m_train`, `m_dev`, dan `m_test`.
        - `n` adalah jumlah fitur.
        - `X` adalah matriks fitur berukuran `(m, n)`. Satu baris adalah satu contoh.
        - `y` adalah vektor label berukuran `(m,)`. Untuk klasifikasi biner nilainya 0 atau 1.
        - `h(x)` adalah prediksi model untuk satu contoh.
        - `error = 1 - akurasi` untuk klasifikasi, yaitu proporsi prediksi yang salah.

        Tiga pembagian data muncul terus: **training set** untuk melatih, **dev set** untuk membuat keputusan pengembangan seperti memilih model dan hyperparameter, serta **test set** untuk mengevaluasi hasil akhir tanpa dipakai mengambil keputusan. Alasan ketiganya terpisah dibahas penuh di modul 2.
        """),
        T("""
        ## Regresi logistik secara eksplisit

        Agar notasi terasa konkret, lihat regresi logistik tanpa pustaka. Untuk satu contoh dengan vektor fitur `x`, model menghitung skor linear `z = w · x + b`, lalu mengubahnya menjadi peluang dengan fungsi sigmoid `p = 1 / (1 + exp(-z))`. Prediksi kelas adalah 1 bila `p >= 0.5`, selain itu 0.

        Parameter `w` dan `b` dipelajari dari training set. Setelah itu, mengevaluasi model berarti menghitung error pada set data tertentu. Perhatikan bahwa error training dan error dev dihitung dengan fungsi yang sama, hanya data masukannya berbeda. Selisih keduanya adalah petunjuk penting untuk diagnosis di lesson sebelumnya.

        Dengan notasi ini, kalimat seperti "model punya error dev 12 persen dengan `m_dev = 5000`" menjadi sangat jelas, termasuk betapa pentingnya angka `m_dev` itu untuk kepercayaan kita pada angka 12 persen.
        """),
        T("""
        ## Mengapa tiga set, bukan satu

        Pemula sering bertanya mengapa data harus dibagi tiga. Alasannya ada pada apa yang terjadi ketika kamu mengambil keputusan berulang-ulang berdasarkan satu set data. Setiap kali kamu mencoba hyperparameter baru dan memilih yang terbaik menurut dev set, informasi tentang dev set perlahan bocor ke dalam model pilihanmu. Setelah puluhan percobaan, angka dev menjadi sedikit terlalu optimis.

        Test set ada untuk menjaga satu angka yang jujur. Selama test set tidak dipakai mengambil keputusan, error test adalah estimasi yang tidak bias tentang performa pada data baru. Kamu akan melihat simulasi efek ini di modul 2.

        Pembagian yang rapi juga membuat percakapan tim lebih tajam. Ketika seseorang berkata "model ini bagus", pertanyaan berikutnya langsung jelas: bagus pada set yang mana, dan seberapa besar set itu? Notasi `m_train`, `m_dev`, dan `m_test` membuat pertanyaan itu bisa dijawab dengan angka, bukan dengan perasaan.
        """),
        K(
            "tip",
            """
            Biasakan menulis ukuran setiap set bersama setiap angka error yang kamu laporkan, misalnya "error dev 12 persen pada 5000 contoh". Angka tanpa ukuran sampel hampir tidak bisa dinilai kepercayaannya, dan kebiasaan kecil ini akan sangat berguna saat kamu membahas ukuran dev set di modul 2.
            """,
        ),
        C(
            """
            import numpy as np
            from sklearn.datasets import make_classification

            X, y = make_classification(n_samples=1000, n_features=10, n_informative=5, random_state=1)
            rng = np.random.default_rng(1)
            idx = rng.permutation(len(X))
            n_tr, n_dev = 600, 200
            tr, dev, te = idx[:n_tr], idx[n_tr:n_tr + n_dev], idx[n_tr + n_dev:]
            print("m_train, m_dev, m_test:", len(tr), len(dev), len(te))
            print("bentuk X_train:", X[tr].shape, "bentuk y_train:", y[tr].shape)
            print("tidak ada tumpang tindih:", not (set(tr) & set(dev)) and not (set(dev) & set(te)))
            """,
            """
            m_train, m_dev, m_test: 600 200 200
            bentuk X_train: (600, 10) bentuk y_train: (600,)
            tidak ada tumpang tindih: True
            """,
            """
            Data diacak dengan generator berseed, lalu diiris menjadi tiga bagian yang tidak saling tumpang tindih. Menyimpan indeks, bukan salinan data, memudahkan pelacakan contoh mana masuk set mana. Bentuk X adalah (m, n) dan bentuk y adalah (m,).
            """,
        ),
        C(
            """
            import numpy as np
            from sklearn.datasets import make_classification
            from sklearn.linear_model import LogisticRegression

            X, y = make_classification(n_samples=1000, n_features=10, n_informative=5, random_state=1)
            X_tr, y_tr, X_dev, y_dev = X[:700], y[:700], X[700:], y[700:]
            model = LogisticRegression(max_iter=1000).fit(X_tr, y_tr)

            def error_rate(y_true, y_pred):
                return float(np.mean(y_true != y_pred))

            print("error train:", round(error_rate(y_tr, model.predict(X_tr)), 3))
            print("error dev  :", round(error_rate(y_dev, model.predict(X_dev)), 3))
            """,
            """
            error train sekitar 0.19
            error dev sekitar 0.19
            """,
            """
            Fungsi error_rate membandingkan label sebenarnya dengan prediksi dan menghitung proporsi yang berbeda. Fungsi yang sama dipakai untuk training dan dev. Hanya data yang berbeda, dan itulah yang membuat selisih keduanya bermakna.
            """,
        ),
        C(
            """
            import numpy as np
            from sklearn.datasets import make_classification
            from sklearn.linear_model import LogisticRegression

            X, y = make_classification(n_samples=500, n_features=6, n_informative=4, random_state=3)
            model = LogisticRegression(max_iter=1000).fit(X, y)
            w, b = model.coef_[0], model.intercept_[0]

            z = X @ w + b
            p = 1 / (1 + np.exp(-z))
            pred_manual = (p >= 0.5).astype(int)

            print("prediksi manual sama dengan sklearn:", bool(np.all(pred_manual == model.predict(X))))
            print("peluang manual dekat predict_proba:", bool(np.allclose(p, model.predict_proba(X)[:, 1])))
            """,
            """
            prediksi manual sama dengan sklearn: True
            peluang manual dekat predict_proba: True
            """,
            """
            Prediksi regresi logistik hanyalah sigmoid dari skor linear. Menulisnya sendiri menghilangkan misteri dan membuktikan bahwa notasi w, b, dan x yang dipakai di buku sama persis dengan yang dihitung library.
            """,
        ),
        E(
            "D11-01-2-ex1",
            "mudah",
            """
            Tulis fungsi `ukuran_split(m, frac_dev, frac_test)` yang mengembalikan tuple `(m_train, m_dev, m_test)` berupa bilangan bulat. `m_dev` adalah `int(m * frac_dev)`, `m_test` adalah `int(m * frac_test)`, dan `m_train` adalah sisanya sehingga jumlahnya selalu `m`.
            """,
            """
            def ukuran_split(m, frac_dev, frac_test):
                # TODO: implementasikan
                pass
            """,
            """
            assert ukuran_split(1000, 0.2, 0.2) == (600, 200, 200)
            assert ukuran_split(1001, 0.1, 0.1) == (801, 100, 100)
            a, b, c = ukuran_split(777, 0.15, 0.25)
            assert a + b + c == 777
            """,
            "Hitung m_dev dan m_test dengan int, lalu m_train = m - m_dev - m_test.",
            """
            def ukuran_split(m, frac_dev, frac_test):
                m_dev = int(m * frac_dev)
                m_test = int(m * frac_test)
                return m - m_dev - m_test, m_dev, m_test
            """,
        ),
        E(
            "D11-01-2-ex2",
            "mudah",
            """
            Tulis fungsi `error_rate(y_true, y_pred)` yang mengembalikan proporsi prediksi yang salah sebagai float. Gunakan NumPy.
            """,
            """
            import numpy as np

            def error_rate(y_true, y_pred):
                # TODO: implementasikan
                pass
            """,
            """
            import numpy as np
            assert error_rate(np.array([1, 0, 1, 1]), np.array([1, 0, 0, 1])) == 0.25
            assert error_rate(np.array([0, 0]), np.array([0, 0])) == 0.0
            assert error_rate([1, 1, 1, 1], [0, 0, 0, 0]) == 1.0
            assert isinstance(error_rate(np.array([1]), np.array([0])), float)
            """,
            "Bandingkan dua array dengan !=, lalu ambil rata-rata dan ubah ke float. Pastikan input list juga bisa diterima dengan np.asarray.",
            """
            import numpy as np

            def error_rate(y_true, y_pred):
                y_true = np.asarray(y_true)
                y_pred = np.asarray(y_pred)
                return float(np.mean(y_true != y_pred))
            """,
        ),
        E(
            "D11-01-2-ex3",
            "sedang",
            """
            Tulis fungsi `prediksi(X, w, b)` yang menghitung `p = sigmoid(X @ w + b)` dan mengembalikan tuple `(p, kelas)`. `kelas` bernilai 1 bila `p >= 0.5` dan 0 selain itu, bertipe integer.
            """,
            """
            import numpy as np

            def prediksi(X, w, b):
                # TODO: implementasikan
                pass
            """,
            """
            import numpy as np
            X = np.array([[1.0, 2.0], [-1.0, -2.0], [0.0, 0.0]])
            w = np.array([1.0, 0.5])
            p, kelas = prediksi(X, w, 0.0)
            assert np.allclose(p, [1 / (1 + np.exp(-2.0)), 1 / (1 + np.exp(2.0)), 0.5])
            assert list(kelas) == [1, 0, 1]
            assert kelas.dtype.kind == "i"
            """,
            "Hitung z = X @ w + b, lalu p = 1 / (1 + np.exp(-z)). Kelas diperoleh dengan membandingkan p >= 0.5 lalu astype(int).",
            """
            import numpy as np

            def prediksi(X, w, b):
                z = X @ w + b
                p = 1 / (1 + np.exp(-z))
                return p, (p >= 0.5).astype(int)
            """,
        ),
        E(
            "D11-01-2-ex4",
            "menantang",
            """
            Tulis fungsi `bagi_tiga(m, n_dev, n_test, seed)` yang mengembalikan tuple tiga array indeks `(tr, dev, te)` dari `range(m)`. Gunakan `np.random.default_rng(seed).permutation(m)`. `dev` adalah `n_dev` indeks pertama, `te` adalah `n_test` berikutnya, dan `tr` sisanya. Ketiganya tidak boleh tumpang tindih dan gabungannya harus seluruh `range(m)`. Hasil harus sama untuk seed yang sama.
            """,
            """
            import numpy as np

            def bagi_tiga(m, n_dev, n_test, seed):
                # TODO: implementasikan
                pass
            """,
            """
            import numpy as np
            tr, dev, te = bagi_tiga(100, 20, 10, 0)
            assert len(dev) == 20 and len(te) == 10 and len(tr) == 70
            assert not (set(tr) & set(dev)) and not (set(tr) & set(te)) and not (set(dev) & set(te))
            assert sorted(list(tr) + list(dev) + list(te)) == list(range(100))
            tr2, dev2, te2 = bagi_tiga(100, 20, 10, 0)
            assert list(dev) == list(dev2) and list(tr) == list(tr2)
            tr3, dev3, te3 = bagi_tiga(100, 20, 10, 1)
            assert list(dev) != list(dev3)
            """,
            "Buat permutasi sekali, lalu iris: dev = idx[:n_dev], te = idx[n_dev:n_dev + n_test], tr = idx[n_dev + n_test:].",
            """
            import numpy as np

            def bagi_tiga(m, n_dev, n_test, seed):
                idx = np.random.default_rng(seed).permutation(m)
                dev = idx[:n_dev]
                te = idx[n_dev:n_dev + n_test]
                tr = idx[n_dev + n_test:]
                return tr, dev, te
            """,
        ),
    ],
    [
        M(
            "Mengacak data dengan seed berbeda setiap kali sehingga hasil tidak bisa direproduksi.",
            "Tetapkan seed pada generator acak dan catat bersama hasil eksperimen.",
        ),
        M(
            "Memakai test set untuk memilih model lalu tetap menyebutnya estimasi akhir.",
            "Gunakan dev set untuk semua keputusan pengembangan dan sentuh test set hanya untuk evaluasi akhir.",
        ),
        M(
            "Mencampur bentuk X sebagai (n, m) dan (m, n) di bagian kode yang berbeda.",
            "Pakai konvensi satu baris satu contoh, yaitu (m, n), di seluruh course.",
        ),
    ],
    [
        Q(
            "Pada notasi course ini, apa bentuk matriks fitur X?",
            ["(n, m)", "(m, n)", "(m,)", "(n,)"],
            1,
            "Satu baris adalah satu contoh, jadi bentuknya (m, n) dengan m contoh dan n fitur.",
        ),
        Q(
            "Set mana yang dipakai untuk menyetel hyperparameter?",
            ["Training set", "Dev set", "Test set", "Semua sekaligus"],
            1,
            "Dev set dipakai untuk keputusan pengembangan. Test set tidak boleh dipakai mengambil keputusan.",
        ),
        Q(
            "Apa prediksi kelas regresi logistik jika peluang p = 0.5?",
            ["0", "1", "Tidak terdefinisi", "Bergantung seed"],
            1,
            "Aturan yang dipakai adalah p >= 0.5 menjadi kelas 1, jadi tepat 0.5 masuk ke kelas 1.",
        ),
        Q(
            "Jika m_train = 600 dan m_dev = 200 dari total 1000, berapa m_test jika tiga set tidak tumpang tindih dan mencakup semua data?",
            ["100", "150", "200", "400"],
            2,
            "1000 - 600 - 200 = 200.",
        ),
        Q(
            "Mengapa error training dan error dev dihitung dengan fungsi yang sama?",
            ["Supaya kodenya lebih pendek", "Agar selisihnya hanya mencerminkan perbedaan data, bukan perbedaan cara menghitung", "Karena test set tidak ada", "Karena library mewajibkan"],
            1,
            "Dengan fungsi yang sama, selisih angka bisa diinterpretasi sebagai efek generalisasi.",
        ),
    ],
    [
        "Supervised learning mempelajari pemetaan x ke y dari contoh berlabel.",
        "Notasi m, n, X, y, dan h(x) dipakai konsisten di seluruh course.",
        "Data dibagi menjadi training, dev, dan test tanpa tumpang tindih dan dengan seed tetap.",
        "Error adalah proporsi prediksi salah, dan selisih error training dan dev adalah sinyal diagnosis.",
    ],
    ["Machine Learning Yearning, bab 3 (Andrew Ng): prasyarat dan notasi"],
)

l3 = lesson(
    "D11-01-3",
    "Skala mendorong kemajuan",
    35,
    [
        "Menjelaskan dua pendorong kemajuan deep learning: ketersediaan data dan skala komputasi",
        "Membaca learning curve untuk melihat plateau dan keuntungan model lebih besar",
        "Membangun fungsi learning curve sendiri dan membandingkan model berkapasitas berbeda",
    ],
    [
        T("""
        ## Mengapa ide lama baru meledak sekarang

        Banyak gagasan dalam deep learning sudah berumur puluhan tahun. Mengapa baru dalam beberapa tahun terakhir mereka melejit? Ada dua pendorong utama.

        **Ketersediaan data.** Orang kini menghabiskan banyak waktu di perangkat digital seperti laptop dan ponsel. Aktivitas digital itu menghasilkan data dalam jumlah besar yang bisa diberikan kepada algoritma pembelajaran.

        **Skala komputasi.** Baru beberapa tahun lalu kita mampu melatih jaringan saraf yang cukup besar untuk memanfaatkan dataset sebesar itu.

        Kedua faktor ini bekerja bersama. Dataset besar tanpa model yang cukup besar tidak termanfaatkan, dan model besar tanpa data besar hanya menghafal. Di sinilah kemajuan datang dari skala, bukan hanya dari trik baru.
        """),
        T("""
        ## Learning curve: plateau dan model yang lebih besar

        Cara paling jelas melihat efek ini adalah learning curve, yaitu grafik performa terhadap jumlah data training. Untuk algoritma klasik seperti regresi logistik, kurva biasanya naik di awal lalu **plateau**: kurva mendatar dan algoritma berhenti membaik walau data ditambah. Seolah-olah algoritma lama itu tidak tahu apa yang harus dilakukan dengan data sebanyak itu.

        Jika kamu melatih jaringan saraf kecil pada tugas yang sama, hasilnya mungkin sedikit lebih baik. Jika kamu melatih jaringan yang lebih besar lagi, performa terus naik seiring bertambahnya data. Performa terbaik datang ketika kamu (i) melatih model yang sangat besar dan (ii) memiliki data yang sangat banyak.

        Ada catatan penting. Pada dataset yang sangat kecil, misalnya 20 contoh, memilih regresi logistik atau jaringan saraf mungkin tidak banyak berpengaruh. Pada regime itu, rekayasa fitur manual lebih menentukan daripada pilihan algoritma. Keunggulan jaringan saraf menjadi jelas pada dataset besar.
        """),
        T("""
        ## Konsekuensi praktis dan batasnya

        Salah satu cara yang paling andal untuk meningkatkan performa adalah melatih model yang lebih besar dan mengumpulkan lebih banyak data. Tetapi kalimat itu bukan resep otomatis. Cara mencapai keduanya ternyata rumit: data baru harus berasal dari distribusi yang tepat, dan model yang lebih besar butuh komputasi dan strategi regularisasi.

        Karena itu course ini dimulai dari strategi umum yang berguna untuk algoritma tradisional maupun jaringan saraf, lalu naik ke strategi modern untuk sistem deep learning. Kamu akan terus kembali ke satu pertanyaan: apakah masalahku saat ini kurang kapasitas model, kurang data, atau hal lain? Learning curve adalah alat yang menjawabnya secara empiris.

        Mulai dari lesson ini, kamu akan membangun fungsi learning curve sendiri. Alat kecil ini akan terus dipakai di modul 5 dan 6.
        """),
        T("""
        ## Cara membaca learning curve

        Saat melihat learning curve, ada tiga hal yang patut diperhatikan. Pertama, **kemiringan di ujung kanan**. Jika kurva masih menurun tajam saat data bertambah, data tambahan bernilai tinggi. Jika sudah datar, data tambahan hampir tidak bernilai untuk model itu.

        Kedua, **jarak ke target**. Bandingkan error di titik terbaik kurva dengan error yang kamu inginkan. Bila jaraknya masih jauh dan kurva sudah datar, masalahnya ada pada kapasitas atau fitur. Bila jaraknya kecil, mungkin proyek sudah cukup dan usaha tambahan tidak sebanding.

        Ketiga, **biaya per titik**. Menggandakan data dari 4000 ke 8000 bisa berarti berminggu-minggu pelabelan, sedangkan menggandakan ukuran model mungkin hanya perlu satu sore. Learning curve membantu memperkirakan manfaat sebelum kamu membayar biayanya. Kebiasaan ini sejalan dengan skor prioritas yang kamu pelajari di lesson pertama.
        """),
        K(
            "note",
            """
            Learning curve pada lesson ini dibuat dari data sintetis dengan pola interaksi antarfitur. Bentuk persisnya bergantung pada masalah. Yang penting adalah membiasakan diri membaca bentuk kurvanya: plateau berarti menambah data saja tidak cukup, kurva yang masih naik berarti data tambahan layak dikejar.
            """,
        ),
        C(
            """
            import numpy as np

            def buat_data(m, seed):
                rng = np.random.default_rng(seed)
                X = rng.normal(size=(m, 20))
                y = (X[:, 0] * X[:, 1] + X[:, 2] * X[:, 3] > 0).astype(int)
                return X, y

            X_dev, y_dev = buat_data(2000, 99)
            from sklearn.linear_model import LogisticRegression
            from sklearn.neural_network import MLPClassifier

            print("m_train  LR dev error  MLP(64,64) dev error")
            for m in [200, 1000, 4000]:
                X_tr, y_tr = buat_data(m, 1)
                lr = LogisticRegression(max_iter=1000).fit(X_tr, y_tr)
                mlp = MLPClassifier(hidden_layer_sizes=(64, 64), max_iter=300, random_state=0).fit(X_tr, y_tr)
                print(f"{m:7d}  {1 - lr.score(X_dev, y_dev):12.3f}  {1 - mlp.score(X_dev, y_dev):20.3f}")
            """,
            """
            LR error sekitar 0.45 sampai 0.55 di semua ukuran data (plateau)
            MLP error turun jelas seiring m_train bertambah
            """,
            """
            Label dibuat dari interaksi perkalian antarfitur, pola yang tidak bisa ditangkap model linear. Regresi logistik tertahan di sekitar tebakan acak berapa pun datanya, itulah plateau. Jaringan saraf dua layer terus membaik saat data bertambah. Angka persisnya bisa berbeda tipis antar versi library, tetapi bentuk polanya sama.
            """,
        ),
        C(
            """
            import numpy as np
            from sklearn.neural_network import MLPClassifier

            def buat_data(m, seed):
                rng = np.random.default_rng(seed)
                X = rng.normal(size=(m, 20))
                y = (X[:, 0] * X[:, 1] + X[:, 2] * X[:, 3] > 0).astype(int)
                return X, y

            X_dev, y_dev = buat_data(2000, 99)
            X_tr, y_tr = buat_data(4000, 1)
            for nama, ukuran in [("kecil (4)", (4,)), ("sedang (16)", (16,)), ("besar (64,64)", (64, 64))]:
                model = MLPClassifier(hidden_layer_sizes=ukuran, max_iter=300, random_state=0).fit(X_tr, y_tr)
                print(f"{nama:15s} error dev = {1 - model.score(X_dev, y_dev):.3f}")
            """,
            """
            model kecil error dev sekitar 0.19, model sedang dan besar sekitar 0.04
            """,
            """
            Dengan data tetap 4000 contoh, kapasitas model dinaikkan. Model yang terlalu kecil tidak punya cukup unit untuk menangkap interaksi, jadi errornya tinggi. Model sedang sudah cukup menangkapnya, dan model besar tidak memberi keuntungan tambahan pada ukuran data ini. Inilah bagian pertama resep: kapasitas harus memadai, tetapi lebih besar belum tentu lebih baik bila data atau masalahnya tidak menuntutnya.
            """,
        ),
        C(
            """
            import io
            import numpy as np
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            from sklearn.linear_model import LogisticRegression
            from sklearn.neural_network import MLPClassifier

            def buat_data(m, seed):
                rng = np.random.default_rng(seed)
                X = rng.normal(size=(m, 20))
                y = (X[:, 0] * X[:, 1] + X[:, 2] * X[:, 3] > 0).astype(int)
                return X, y

            X_dev, y_dev = buat_data(1500, 99)
            ukuran = [200, 500, 1000, 2000, 4000]
            err_lr, err_mlp = [], []
            for m in ukuran:
                X_tr, y_tr = buat_data(m, 1)
                err_lr.append(1 - LogisticRegression(max_iter=1000).fit(X_tr, y_tr).score(X_dev, y_dev))
                err_mlp.append(1 - MLPClassifier(hidden_layer_sizes=(64, 64), max_iter=300, random_state=0).fit(X_tr, y_tr).score(X_dev, y_dev))

            fig, ax = plt.subplots(figsize=(5, 3))
            ax.plot(ukuran, err_lr, marker="o", label="regresi logistik")
            ax.plot(ukuran, err_mlp, marker="o", label="MLP besar")
            ax.set_xlabel("jumlah data training")
            ax.set_ylabel("error dev")
            ax.legend()
            buf = io.BytesIO()
            fig.savefig(buf, format="png")
            print("ukuran png > 1000 byte:", buf.tell() > 1000)
            """,
            """
            ukuran png > 1000 byte: True
            """,
            """
            Learning curve digambar dengan Matplotlib ke buffer memori sehingga tidak butuh file. Di app, gambar seperti ini akan tampil sebagai output sel notebook. Kurva regresi logistik mendatar, sedangkan kurva model besar turun.
            """,
        ),
        E(
            "D11-01-3-ex1",
            "mudah",
            """
            Diberikan list `akurasi` untuk ukuran data yang berlipat dua, hitung list `kenaikan` berisi selisih akurasi berturut-turut (akurasi berikutnya dikurangi sebelumnya), dibulatkan ke 4 desimal.
            """,
            """
            akurasi = [0.70, 0.78, 0.83, 0.84, 0.842]
            kenaikan = None
            # TODO: isi kenaikan
            """,
            """
            assert isinstance(kenaikan, list)
            assert len(kenaikan) == len(akurasi) - 1
            assert kenaikan == [0.08, 0.05, 0.01, 0.002]
            assert all(isinstance(x, float) for x in kenaikan)
            """,
            "Gunakan zip(akurasi[1:], akurasi[:-1]) atau indeks, dan round(selisih, 4).",
            """
            akurasi = [0.70, 0.78, 0.83, 0.84, 0.842]
            kenaikan = [round(b - a, 4) for a, b in zip(akurasi[:-1], akurasi[1:])]
            """,
        ),
        E(
            "D11-01-3-ex2",
            "sedang",
            """
            Tulis fungsi `apakah_plateau(akurasi, toleransi)` yang mengembalikan `True` bila dua kenaikan terakhir pada list akurasi keduanya lebih kecil dari `toleransi` (dibulatkan 6 desimal sebelum dibandingkan). Jika list kurang dari tiga elemen kembalikan `False`.
            """,
            """
            def apakah_plateau(akurasi, toleransi):
                # TODO: implementasikan
                pass
            """,
            """
            assert apakah_plateau([0.70, 0.78, 0.83, 0.84, 0.842], 0.015) is True
            assert apakah_plateau([0.70, 0.78, 0.83, 0.88], 0.015) is False
            assert apakah_plateau([0.7, 0.8], 0.01) is False
            assert apakah_plateau([0.80, 0.80, 0.80], 0.001) is True
            """,
            "Hitung dua selisih terakhir, bulatkan, lalu periksa keduanya < toleransi.",
            """
            def apakah_plateau(akurasi, toleransi):
                if len(akurasi) < 3:
                    return False
                k1 = round(akurasi[-2] - akurasi[-3], 6)
                k2 = round(akurasi[-1] - akurasi[-2], 6)
                return bool(k1 < toleransi and k2 < toleransi)
            """,
        ),
        E(
            "D11-01-3-ex3",
            "sedang",
            """
            Tulis fungsi `learning_curve(buat_model, X_tr, y_tr, X_dev, y_dev, ukuran)` yang untuk setiap `m` dalam `ukuran` melatih `buat_model()` pada `m` contoh pertama dari training, lalu mengumpulkan error dev (1 dikurangi `score`). Kembalikan list error sepanjang `ukuran`.
            """,
            """
            def learning_curve(buat_model, X_tr, y_tr, X_dev, y_dev, ukuran):
                # TODO: implementasikan
                pass
            """,
            """
            import numpy as np
            from sklearn.linear_model import LogisticRegression
            rng = np.random.default_rng(0)
            X = rng.normal(size=(600, 5))
            y = (X[:, 0] + 0.3 * rng.normal(size=600) > 0).astype(int)
            err = learning_curve(lambda: LogisticRegression(), X[:400], y[:400], X[400:], y[400:], [20, 100, 400])
            assert len(err) == 3
            assert all(0.0 <= e <= 1.0 for e in err)
            assert err[-1] <= err[0] + 0.05
            """,
            "Dalam loop, buat model baru, fit pada X_tr[:m], y_tr[:m], lalu hitung 1 - model.score(X_dev, y_dev).",
            """
            def learning_curve(buat_model, X_tr, y_tr, X_dev, y_dev, ukuran):
                hasil = []
                for m in ukuran:
                    model = buat_model()
                    model.fit(X_tr[:m], y_tr[:m])
                    hasil.append(1 - model.score(X_dev, y_dev))
                return hasil
            """,
        ),
        E(
            "D11-01-3-ex4",
            "menantang",
            """
            Gunakan fungsi `buat_data` yang sudah disediakan. Latih `LogisticRegression` dan `MLPClassifier(hidden_layer_sizes=(64, 64), max_iter=300, random_state=0)` pada 4000 contoh (`buat_data(4000, 1)`), lalu hitung `err_lr` dan `err_mlp` pada dev (`buat_data(2000, 99)`). Simpan `selisih = err_lr - err_mlp`. Tujuannya membuktikan bahwa model besar jauh lebih baik pada data ini.
            """,
            """
            import numpy as np
            from sklearn.linear_model import LogisticRegression
            from sklearn.neural_network import MLPClassifier

            def buat_data(m, seed):
                rng = np.random.default_rng(seed)
                X = rng.normal(size=(m, 20))
                y = (X[:, 0] * X[:, 1] + X[:, 2] * X[:, 3] > 0).astype(int)
                return X, y

            err_lr = None
            err_mlp = None
            selisih = None
            # TODO: isi ketiganya
            """,
            """
            assert 0.35 <= err_lr <= 0.65
            assert err_mlp < 0.35
            assert selisih > 0.1
            """,
            "Buat data training dan dev dengan buat_data, fit kedua model, lalu hitung 1 - score pada dev untuk masing-masing.",
            """
            import numpy as np
            from sklearn.linear_model import LogisticRegression
            from sklearn.neural_network import MLPClassifier

            def buat_data(m, seed):
                rng = np.random.default_rng(seed)
                X = rng.normal(size=(m, 20))
                y = (X[:, 0] * X[:, 1] + X[:, 2] * X[:, 3] > 0).astype(int)
                return X, y

            X_tr, y_tr = buat_data(4000, 1)
            X_dev, y_dev = buat_data(2000, 99)
            lr = LogisticRegression(max_iter=1000).fit(X_tr, y_tr)
            mlp = MLPClassifier(hidden_layer_sizes=(64, 64), max_iter=300, random_state=0).fit(X_tr, y_tr)
            err_lr = 1 - lr.score(X_dev, y_dev)
            err_mlp = 1 - mlp.score(X_dev, y_dev)
            selisih = err_lr - err_mlp
            """,
        ),
    ],
    [
        M(
            "Menyimpulkan bahwa model sederhana buruk hanya dari satu ukuran data.",
            "Gambar learning curve dengan beberapa ukuran data sebelum menarik kesimpulan.",
        ),
        M(
            "Mengira menambah data selalu membantu.",
            "Jika kurva sudah plateau dan error training tinggi, tambahkan kapasitas model atau perbaiki fitur, bukan hanya data.",
        ),
        M(
            "Membandingkan model pada dev set yang berbeda ukuran atau distribusinya.",
            "Gunakan dev set yang sama dan tetap untuk seluruh titik pada learning curve.",
        ),
    ],
    [
        Q(
            "Dua pendorong utama kemajuan deep learning menurut materi ini?",
            ["Ketersediaan data dan skala komputasi", "Ketersediaan data dan bahasa pemrograman baru", "Hanya arsitektur baru", "Hanya GPU murah"],
            0,
            "Data besar dan komputasi cukup untuk melatih model besar adalah dua pendorong yang disebut.",
        ),
        Q(
            "Apa arti plateau pada learning curve?",
            ["Model berhenti membaik walau data ditambah", "Model sempurna", "Data rusak", "Learning rate terlalu besar"],
            0,
            "Plateau berarti kurva mendatar: menambah data tidak lagi menurunkan error.",
        ),
        Q(
            "Pada dataset sangat kecil, apa yang sering lebih menentukan daripada pilihan algoritma?",
            ["Jumlah GPU", "Rekayasa fitur manual", "Warna grafik", "Nama library"],
            1,
            "Pada regime data kecil, kualitas fitur rancangan manusia lebih berpengaruh.",
        ),
        Q(
            "Di contoh interaksi perkalian antarfitur, mengapa regresi logistik tertahan di sekitar 50 persen error?",
            ["Karena datanya sedikit", "Karena modelnya linear dan tidak bisa menangkap interaksi", "Karena seed salah", "Karena dev set terlalu kecil"],
            1,
            "Batas keputusan linear tidak dapat merepresentasikan interaksi perkalian, sehingga data tambahan tidak membantu.",
        ),
        Q(
            "Jika learning curve model kecil sudah mendatar, ide mana yang paling masuk akal?",
            ["Menambah data persis sama", "Menaikkan kapasitas model atau fitur", "Mengurangi data", "Menghapus dev set"],
            1,
            "Plateau menunjukkan batas kapasitas model. Menaikkan kapasitas atau memperbaiki fitur adalah arah yang masuk akal.",
        ),
    ],
    [
        "Data besar dan komputasi besar mendorong kemajuan deep learning.",
        "Learning curve menunjukkan plateau pada model klasik dan perbaikan berkelanjutan pada model lebih besar.",
        "Pada data sangat kecil, fitur manual sering lebih menentukan daripada algoritma.",
        "Model lebih besar dan data lebih banyak adalah arah andal, tetapi harus dipilih lewat diagnosis.",
    ],
    ["Machine Learning Yearning, bab 4 (Andrew Ng): skala mendorong kemajuan machine learning"],
)

video = {
    "needed": True,
    "kind": "ai_slides",
    "reason": "Visual learning curve dan perbandingan model lebih mudah dipahami dengan animasi grafik.",
    "brief": [
        "Slide 1: skenario detektor kucing dan daftar ide perbaikan",
        "Slide 2: skor prioritas p kali g dibagi c dengan contoh angka",
        "Slide 3: diagnosis bias dan variance dari error train dan dev",
        "Slide 4: notasi m, n, X, y dan tiga set data",
        "Slide 5: learning curve regresi logistik plateau versus jaringan saraf besar",
        "Slide 6: ringkasan dan kapan menambah data atau kapasitas model",
    ],
}

write_module(
    "D11",
    1,
    "Mengapa strategi ML penting",
    95,
    [
        "Memilih arah perbaikan model berdasarkan diagnosis dan skor prioritas",
        "Memakai notasi supervised learning dan membagi data dengan benar",
        "Membaca learning curve untuk memutuskan antara menambah data dan menaikkan kapasitas model",
    ],
    [l1, l2, l3],
    video,
    REF,
)
