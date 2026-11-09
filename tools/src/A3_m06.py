import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

l1 = lesson(
    "A3-06-1",
    "Momentum dan Nesterov",
    35,
    [
        "Menjelaskan mengapa gradient descent biasa lambat pada lembah sempit",
        "Menerapkan pembaruan momentum dengan variabel kecepatan",
        "Menjelaskan efek koefisien momentum terhadap overshoot dan laju",
        "Menerapkan momentum Nesterov dengan gradien di titik pandang ke depan",
    ],
    [
        T("""
        ## Masalah lembah sempit

        Pada modul sebelumnya kita melihat gradient descent bekerja baik di fungsi bundar tetapi lambat di lembah sempit. Contohnya `f(x, y) = (x^2 + 25 y^2) / 2`. Arah `y` sangat curam dan arah `x` sangat landai. Learning rate harus kecil agar tidak memantul di dinding curam, tetapi akibatnya kemajuan sepanjang dasar lembah sangat lambat.

        Gejalanya khas: lintasan bergerigi, memantul bolak-balik antar dinding sambil maju pelan sepanjang dasar. Gradien pada arah curam berganti tanda tiap langkah sehingga saling meniadakan, sedangkan gradien pada arah landai konsisten tetapi kecil. Kita butuh cara untuk meredam goyangan dan memperkuat gerakan yang konsisten. Itulah **momentum**.
        """),
        T("""
        ## Bola yang menggelinding

        Bayangkan bola berat menggelinding di lembah, bukan orang berjalan hati-hati. Bola punya kelembaman: ia tidak berbelok mendadak tiap kali kemiringan berubah, melainkan mengumpulkan **kecepatan**. Pada arah yang kemiringannya konsisten, kecepatan menumpuk dan bola melaju. Pada arah yang kemiringannya berganti tanda, kontribusi saling meniadakan dan goyangan teredam.

        Rumusnya sederhana. Simpan variabel kecepatan `v`. Pada tiap langkah: `v = beta * v + g`, lalu `x = x - lr * v`. Koefisien `beta` antara nol dan satu, biasanya `0,9`, menentukan seberapa banyak kecepatan lama dipertahankan. Dengan `beta = 0` kita kembali ke gradient descent biasa. Dengan `beta` mendekati satu, bola sangat licin dan sulit berhenti.
        """),
        C(
            """
            def lintasan(beta, langkah=4, x0=1.0, lr=0.1):
                x, v = x0, 0.0
                hasil = []
                for _ in range(langkah):
                    g = 2 * x
                    v = beta * v + g
                    x -= lr * v
                    hasil.append(round(x, 4))
                return hasil

            print(lintasan(0.9))
            print(lintasan(0.0))
            """,
            """
            [0.8, 0.46, 0.062, -0.3086]
            [0.8, 0.64, 0.512, 0.4096]
            """,
            """
            Dengan momentum titik melesat lebih cepat dan bahkan melewati minimum di nol sebelum berbalik, sedangkan tanpa momentum titik mendekat pelan secara geometris.
            """,
            filename="momentum_rumus.py",
        ),
        T("""
        ## Efek koefisien beta

        Momentum menukar kecepatan dengan overshoot. Pada fungsi kuadrat satu variabel, momentum yang kuat membuat titik melewati minimum dan berosilasi dengan amplitudo menyusut. Pada lembah sempit, momentum mempercepat sepanjang dasar. Secara efektif, momentum memperbesar learning rate pada arah yang konsisten dengan faktor sekitar `1 / (1 - beta)`: untuk `beta = 0,9` hingga sepuluh kali lebih cepat.

        Karena itu bila kamu menaikkan `beta`, kamu biasanya perlu menurunkan `lr`. Kombinasi `lr` kecil dan `beta` besar sering lebih stabil dan lebih cepat daripada `lr` besar tanpa momentum. Nilai `beta` sekitar `0,9` adalah titik awal standar, dan `0,99` dipakai untuk masalah yang sangat berderau.
        """),
        C(
            """
            import numpy as np

            def grad(p):
                return np.array([p[0], 25 * p[1]])

            def loss(p):
                return 0.5 * (p[0] ** 2 + 25 * p[1] ** 2)

            def jalankan(lr, beta, langkah=50):
                p = np.array([10.0, 1.0])
                v = np.zeros(2)
                for _ in range(langkah):
                    v = beta * v + grad(p)
                    p = p - lr * v
                return loss(p)

            print(f"{jalankan(0.02, 0.0):.4f}")
            print(f"{jalankan(0.02, 0.9):.4f}")
            """,
            """
            6.6310
            0.3357
            """,
            """
            Pada anggaran 50 langkah dan learning rate yang sama, momentum mencapai loss jauh lebih kecil daripada gradient descent biasa di lembah sempit.
            """,
            filename="ngarai.py",
        ),
        K(
            "tip",
            """
            Bila loss berosilasi liar setelah menambah momentum, turunkan learning rate atau turunkan `beta`. Momentum memperbesar langkah efektif sehingga learning rate lama bisa menjadi terlalu besar.
            """,
            title="Sesuaikan lr",
        ),
        T("""
        ## Nesterov: melihat ke depan

        Momentum biasa menghitung gradien di posisi sekarang lalu menambahkannya ke kecepatan. **Momentum Nesterov** lebih cerdik: ia menghitung gradien di posisi **pandang ke depan**, yaitu ke mana kecepatan lama akan membawa kita, `x - lr * beta * v`. Bila momentum akan membawa kita melewati minimum, gradien di titik ke depan sudah berbalik arah dan memberi koreksi lebih awal.

        Rumusnya: `v = beta * v + grad(x - lr * beta * v)`, lalu `x = x - lr * v`. Hanya satu perubahan kecil dari momentum biasa, tetapi sering memberi konvergensi sedikit lebih cepat dan osilasi lebih sedikit. Hampir semua pustaka menyediakan opsi `nesterov=True`.
        """),
        C(
            """
            import numpy as np

            def grad(p):
                return np.array([p[0], 25 * p[1]])

            def loss(p):
                return 0.5 * (p[0] ** 2 + 25 * p[1] ** 2)

            def jalankan(nesterov, lr=0.02, beta=0.9, langkah=50):
                p = np.array([10.0, 1.0])
                v = np.zeros(2)
                for _ in range(langkah):
                    g = grad(p - lr * beta * v) if nesterov else grad(p)
                    v = beta * v + g
                    p = p - lr * v
                return loss(p)

            print(f"{jalankan(False):.4f}")
            print(f"{jalankan(True):.4f}")
            """,
            """
            0.3357
            0.1081
            """,
            """
            Nesterov menghasilkan loss lebih kecil pada anggaran langkah yang sama berkat koreksi dini dari gradien titik pandang ke depan.
            """,
            filename="nesterov.py",
        ),
        T("""
        ## Kapan memakai momentum

        Momentum hampir selalu membantu pada pelatihan jaringan saraf dengan SGD. Gradien dari mini-batch berderau, dan momentum merata-ratakan derau itu dari langkah ke langkah sehingga lintasan lebih mulus. SGD dengan momentum sembilan persepuluh masih menjadi pilihan standar untuk banyak model visi komputer, sering mengalahkan optimizer adaptif pada akurasi akhir bila dituning dengan baik.

        Namun momentum menambah satu hiperparameter dan satu vektor memori sebesar parameter. Pada model sangat besar, memori itu bernilai. Pelajaran berikut membahas optimizer adaptif yang menyesuaikan langkah per parameter dan sering bekerja baik tanpa banyak penyetelan.
        """),
        T("""
        ## Membaca kurva loss

        Cara praktis menilai momentum adalah memplot loss terhadap langkah. Bila kurva turun mulus tetapi lambat, naikkan `beta` atau `lr`. Bila kurva turun cepat lalu naik-turun dengan amplitudo besar, momentum terlalu kuat atau `lr` terlalu besar. Osilasi kecil yang menyusut sendiri adalah wajar dan tanda momentum bekerja.

        Pada praktiknya, ubah satu hiperparameter sekali waktu dan simpan hasilnya. Penyetelan bersamaan membuat sebab dan akibat sulit dipisahkan, dan kamu mudah tertipu oleh satu lintasan acak yang kebetulan bagus. Ulangi dengan beberapa benih acak sebelum menyimpulkan.
        """),
        E(
            "A3-06-1-ex1",
            "mudah",
            """
            Tulis fungsi `momentum_langkah(x, v, g, lr, beta)` yang melakukan satu pembaruan momentum (`v = beta * v + g`, lalu `x = x - lr * v`) dan mengembalikan tuple `(x_baru, v_baru)` dibulatkan 4 desimal. Hindari `-0.0`.
            """,
            """
            def momentum_langkah(x, v, g, lr, beta):
                # TODO: implementasikan
                pass
            """,
            """
            assert momentum_langkah(1, 0, 2, 0.1, 0.9) == (0.8, 2.0)
            assert momentum_langkah(0.8, 2.0, 1.6, 0.1, 0.9) == (0.46, 3.4)
            assert momentum_langkah(5, 0, 0, 0.1, 0.9) == (5.0, 0.0)
            assert momentum_langkah(1, 1, 0, 0.5, 0.5) == (0.75, 0.5)
            """,
            "Perbarui kecepatan lebih dulu lalu gunakan kecepatan baru untuk memperbarui posisi.",
            """
            def momentum_langkah(x, v, g, lr, beta):
                v = beta * v + g
                x = x - lr * v
                return (round(x, 4) + 0.0, round(v, 4) + 0.0)
            """,
        ),
        E(
            "A3-06-1-ex2",
            "sedang",
            """
            Tulis fungsi `lintasan_momentum(grad, x0, lr, beta, langkah)` yang menjalankan momentum satu dimensi dari kecepatan nol dan mengembalikan list posisi setelah tiap langkah dibulatkan 4 desimal. Hindari `-0.0`.
            """,
            """
            def lintasan_momentum(grad, x0, lr, beta, langkah):
                # TODO: implementasikan
                pass
            """,
            """
            g = lambda x: 2 * x
            assert lintasan_momentum(g, 1, 0.1, 0.9, 4) == [0.8, 0.46, 0.062, -0.3086]
            assert lintasan_momentum(g, 1, 0.1, 0.0, 4) == [0.8, 0.64, 0.512, 0.4096]
            assert lintasan_momentum(lambda x: 0, 3, 0.1, 0.9, 2) == [3.0, 3.0]
            assert lintasan_momentum(g, 1, 0.1, 0.9, 0) == []
            """,
            "Ulangi pembaruan momentum dan simpan posisi tiap langkah.",
            """
            def lintasan_momentum(grad, x0, lr, beta, langkah):
                x, v = float(x0), 0.0
                hasil = []
                for _ in range(langkah):
                    v = beta * v + grad(x)
                    x -= lr * v
                    hasil.append(round(x, 4) + 0.0)
                return hasil
            """,
        ),
        E(
            "A3-06-1-ex3",
            "sedang",
            """
            Tulis fungsi `nesterov_langkah(grad, x, v, lr, beta)` yang melakukan satu pembaruan Nesterov: `v = beta * v + grad(x - lr * beta * v)`, lalu `x = x - lr * v`. Kembalikan tuple `(x_baru, v_baru)` dibulatkan 4 desimal.
            """,
            """
            def nesterov_langkah(grad, x, v, lr, beta):
                # TODO: implementasikan
                pass
            """,
            """
            g = lambda x: 2 * x
            assert nesterov_langkah(g, 1, 0, 0.1, 0.9) == (0.8, 2.0)
            assert nesterov_langkah(g, 0.8, 2.0, 0.1, 0.9) == (0.496, 3.04)
            assert nesterov_langkah(lambda x: 4, 0, 0, 0.5, 0.9) == (-2.0, 4.0)
            assert nesterov_langkah(g, 3, 5, 0.1, 0) == (2.4, 6.0)
            """,
            "Hitung gradien di titik pandang ke depan lalu perbarui kecepatan dan posisi.",
            """
            def nesterov_langkah(grad, x, v, lr, beta):
                v = beta * v + grad(x - lr * beta * v)
                x = x - lr * v
                return (round(x, 4) + 0.0, round(v, 4) + 0.0)
            """,
        ),
        E(
            "A3-06-1-ex4",
            "menantang",
            """
            Tulis fungsi `langkah_hingga(grad, x0, lr, beta, tol, maks)` yang menjalankan momentum satu dimensi dari kecepatan nol (`v = beta * v + grad(x)`, `x = x - lr * v`) sampai `abs(grad(x)) < tol` atau mencapai `maks` langkah. Kembalikan banyaknya langkah yang dilakukan.
            """,
            """
            def langkah_hingga(grad, x0, lr, beta, tol, maks):
                # TODO: implementasikan
                pass
            """,
            """
            g = lambda x: 0.2 * x
            assert langkah_hingga(g, 10, 0.1, 0, 1e-3, 10000) == 377
            assert langkah_hingga(g, 10, 0.1, 0.9, 1e-3, 10000) == 106
            assert langkah_hingga(g, 10, 0.1, 0.5, 1e-3, 10000) == 180
            assert langkah_hingga(g, 0, 0.1, 0.9, 1e-3, 10000) == 0
            assert langkah_hingga(g, 10, 0.1, 0.9, 1e-3, 5) == 5
            """,
            "Periksa norma gradien sebelum tiap pembaruan dan hitung jumlah pembaruan.",
            """
            def langkah_hingga(grad, x0, lr, beta, tol, maks):
                x, v, n = float(x0), 0.0, 0
                while abs(grad(x)) >= tol and n < maks:
                    v = beta * v + grad(x)
                    x -= lr * v
                    n += 1
                return n
            """,
        ),
    ],
    [
        M("Menaikkan beta tanpa menurunkan learning rate.", "Momentum memperbesar langkah efektif."),
        M("Lupa menginisialisasi kecepatan dengan nol.", "Mulai dari v = 0."),
        M("Menukar urutan pembaruan v dan x.", "Perbarui v dulu lalu x."),
    ],
    [
        Q("Momentum menyimpan?", ["Rata-rata data", "Kecepatan akumulasi gradien", "Jumlah epoch", "Bobot awal"], 1, "Variabel v.", hint="Bola."),
        Q("beta = 0 berarti?", ["Tanpa momentum", "Momentum penuh", "Learning rate nol", "Batch kecil"], 0, "Kembali ke gradient descent biasa.", hint="Tidak ada memori."),
        Q("Momentum membantu terutama pada?", ["Lembah sempit", "Data kecil", "Fitur sedikit", "Loss nol"], 0, "Meredam goyangan dan mempercepat dasar lembah.", hint="Zig-zag."),
        Q("Nesterov menghitung gradien di?", ["Titik sekarang", "Titik pandang ke depan", "Titik awal", "Titik acak"], 1, "x - lr beta v.", hint="Lookahead."),
        Q("Nilai beta umum?", ["0,1", "0,5", "0,9", "2"], 2, "Titik awal standar.", hint="Hampir satu."),
    ],
    [
        "Momentum mengakumulasi gradien menjadi kecepatan untuk meredam goyangan.",
        "Beta besar mempercepat tetapi dapat overshoot dan membutuhkan lr lebih kecil.",
        "Nesterov memakai gradien di titik pandang ke depan.",
        "Momentum standar pada SGD untuk banyak model.",
    ],
    [],
)

l2 = lesson(
    "A3-06-2",
    "Optimizer adaptif: AdaGrad, RMSProp, dan Adam",
    35,
    [
        "Menjelaskan ide learning rate per parameter",
        "Menerapkan pembaruan AdaGrad dan RMSProp",
        "Menerapkan Adam beserta koreksi bias",
        "Membandingkan optimizer pada lembah sempit",
    ],
    [
        T("""
        ## Satu learning rate untuk semua?

        Dengan SGD biasa, semua parameter memakai learning rate yang sama. Padahal parameter berbeda sifat. Pada model teks, kata langka muncul jarang sehingga parameternya jarang mendapat gradien, sedangkan kata umum mendapat gradien terus-menerus. Satu learning rate sulit cocok untuk keduanya. Fitur dengan skala berbeda juga menimbulkan masalah yang sama.

        **Optimizer adaptif** menyesuaikan langkah per parameter berdasarkan riwayat gradiennya. Parameter dengan gradien besar dan sering diberi langkah lebih kecil, sedangkan parameter dengan gradien kecil atau jarang diberi langkah relatif lebih besar. Hasilnya, pelatihan jauh lebih tahan terhadap pilihan learning rate dan skala fitur.
        """),
        T("""
        ## AdaGrad

        **AdaGrad** adalah optimizer adaptif pertama yang populer. Ia menyimpan jumlah kuadrat gradien `G` per parameter dan memperbarui `x = x - lr * g / (sqrt(G) + eps)`. Konstanta kecil `eps`, misalnya `1e-8`, mencegah pembagian nol. Pada langkah pertama, `g / sqrt(g^2)` sama dengan tanda gradien, sehingga setiap parameter bergerak sejauh `lr` tanpa peduli skala gradiennya.

        Kekuatan AdaGrad adalah menormalkan skala gradien. Kelemahannya: `G` hanya bertambah, sehingga learning rate efektif terus menyusut dan akhirnya terlalu kecil untuk belajar lebih lanjut. Pada pelatihan panjang jaringan dalam ini menjadi masalah, yang mendorong penciptaan RMSProp.
        """),
        C(
            """
            import numpy as np

            g = np.array([100.0, 0.01])
            lr = 0.1
            G = g ** 2
            langkah = lr * g / (np.sqrt(G) + 1e-8)
            print(langkah.round(4).tolist())

            rho = 0.9
            s = (1 - rho) * g ** 2
            langkah_rms = lr * g / (np.sqrt(s) + 1e-8)
            print(langkah_rms.round(4).tolist())
            """,
            """
            [0.1, 0.1]
            [0.3162, 0.3162]
            """,
            """
            Walau gradien berbeda sepuluh ribu kali lipat, langkah pertama AdaGrad sama untuk kedua parameter. RMSProp pada langkah pertama memberi langkah sekitar 3,16 kali learning rate.
            """,
            filename="adagrad_rmsprop.py",
        ),
        T("""
        ## RMSProp

        **RMSProp** memperbaiki kelemahan AdaGrad dengan mengganti jumlah kuadrat gradien menjadi **rata-rata bergerak eksponensial**: `s = rho * s + (1 - rho) * g^2`, dengan `rho` sekitar `0,9`. Lalu `x = x - lr * g / (sqrt(s) + eps)`. Karena rata-rata hanya mengingat gradien baru-baru ini, `s` tidak terus membesar dan learning rate efektif tidak menghilang.

        Intuisinya: bagi gradien dengan akar rata-rata kuadratnya, yaitu ukuran tipikal gradien terkini. Hasilnya adalah langkah berukuran kira-kira `lr` pada setiap parameter, apa pun skala gradien. Ini sangat membantu pada lembah sempit dan fitur berskala berbeda.
        """),
        T("""
        ## Adam

        **Adam** menggabungkan dua ide: momentum dan penskalaan adaptif. Ia menyimpan rata-rata bergerak gradien `m` (momentum, dengan `beta1` sekitar `0,9`) dan rata-rata bergerak kuadrat gradien `v` (seperti RMSProp, dengan `beta2` sekitar `0,999`). Pembaruannya `x = x - lr * m_hat / (sqrt(v_hat) + eps)`.

        Karena `m` dan `v` dimulai dari nol, pada awal pelatihan keduanya bias ke arah nol. Adam mengoreksinya: `m_hat = m / (1 - beta1^t)` dan `v_hat = v / (1 - beta2^t)`, dengan `t` nomor langkah. Tanpa koreksi, langkah awal terlalu kecil. Dengan koreksi, langkah pertama persis `lr` pada tiap parameter. Nilai bawaan `lr = 0,001`, `beta1 = 0,9`, `beta2 = 0,999` bekerja cukup baik pada banyak masalah, itulah mengapa Adam menjadi pilihan awal paling populer.
        """),
        C(
            """
            import math

            x, m, v = 5.0, 0.0, 0.0
            lr, b1, b2, eps = 0.1, 0.9, 0.999, 1e-8
            jalur = []
            for t in range(1, 4):
                g = 2 * x
                m = b1 * m + (1 - b1) * g
                v = b2 * v + (1 - b2) * g * g
                mh = m / (1 - b1 ** t)
                vh = v / (1 - b2 ** t)
                x -= lr * mh / (math.sqrt(vh) + eps)
                jalur.append(round(x, 4))
            print(jalur)

            for t in range(4, 101):
                g = 2 * x
                m = b1 * m + (1 - b1) * g
                v = b2 * v + (1 - b2) * g * g
                x -= lr * (m / (1 - b1 ** t)) / (math.sqrt(v / (1 - b2 ** t)) + eps)
            print(abs(x) < 0.5)
            """,
            """
            [4.9, 4.8001, 4.7002]
            True
            """,
            """
            Langkah pertama tepat sebesar learning rate berkat koreksi bias. Setelah seratus langkah titik berada dekat nol, walau Adam dengan learning rate tetap cenderung bergoyang kecil di sekitar minimum.
            """,
            filename="adam_manual.py",
        ),
        K(
            "tip",
            """
            Untuk Adam, learning rate bawaan 0,001 adalah titik awal yang aman. Bila pelatihan tidak stabil, coba 0,0003. Bila terlalu lambat, coba 0,003. Jarang perlu mengubah beta dan eps.
            """,
            title="Pengaturan awal",
        ),
        T("""
        ## Membandingkan optimizer

        Tidak ada optimizer yang selalu terbaik. SGD dengan momentum sering menghasilkan generalisasi bagus pada model visi komputer tetapi sensitif terhadap learning rate. Adam cepat konvergen dan tahan terhadap pilihan hiperparameter, cocok sebagai pilihan awal dan untuk model berbasis transformer, tetapi kadang generalisasinya sedikit lebih buruk. AdamW, yaitu Adam dengan peluruhan bobot yang dipisahkan dari gradien, menjadi standar untuk melatih model bahasa besar.

        Contoh berikut membandingkan beberapa optimizer pada lembah sempit yang sama dengan anggaran langkah sama. Perhatikan bahwa hasilnya bergantung pada penyetelan: perbandingan adil membutuhkan learning rate yang dituning untuk tiap optimizer, bukan satu nilai untuk semuanya.
        """),
        C(
            """
            import numpy as np

            def grad(p):
                return np.array([p[0], 25 * p[1]])

            def loss(p):
                return 0.5 * (p[0] ** 2 + 25 * p[1] ** 2)

            def sgd(lr, langkah=100):
                p = np.array([10.0, 1.0])
                for _ in range(langkah):
                    p = p - lr * grad(p)
                return loss(p)

            def momentum(lr, beta, langkah=100):
                p = np.array([10.0, 1.0])
                v = np.zeros(2)
                for _ in range(langkah):
                    v = beta * v + grad(p)
                    p = p - lr * v
                return loss(p)

            def rmsprop(lr, rho=0.9, langkah=100):
                p = np.array([10.0, 1.0])
                s = np.zeros(2)
                for _ in range(langkah):
                    g = grad(p)
                    s = rho * s + (1 - rho) * g ** 2
                    p = p - lr * g / (np.sqrt(s) + 1e-8)
                return loss(p)

            def adam(lr, langkah=100, b1=0.9, b2=0.999):
                p = np.array([10.0, 1.0])
                m = np.zeros(2)
                v = np.zeros(2)
                for t in range(1, langkah + 1):
                    g = grad(p)
                    m = b1 * m + (1 - b1) * g
                    v = b2 * v + (1 - b2) * g ** 2
                    p = p - lr * (m / (1 - b1 ** t)) / (np.sqrt(v / (1 - b2 ** t)) + 1e-8)
                return loss(p)

            print(f"sgd {sgd(0.07):.2e}")
            print(f"momentum {momentum(0.02, 0.9):.2e}")
            print(f"rmsprop {rmsprop(0.1):.2e}")
            print(f"adam {adam(0.3):.2e}")
            """,
            """
            sgd 2.49e-05
            momentum 9.98e-04
            rmsprop 3.91e-01
            adam 1.35e-03
            """,
            """
            Semua optimizer menurunkan loss jauh dari nilai awal 62,5. RMSProp pada learning rate ini masih bergoyang sehingga hasilnya paling besar. Angkanya bergantung pada penyetelan dan bukan peringkat universal.
            """,
            filename="bandingkan_optimizer.py",
        ),
        T("""
        ## Memori dan biaya

        Optimizer adaptif membutuhkan memori tambahan. Adam menyimpan dua vektor, `m` dan `v`, sebesar parameter model, sehingga memori optimizer kira-kira dua kali ukuran bobot. Untuk model dengan miliaran parameter, ini bernilai dan mendorong varian hemat memori. SGD dengan momentum hanya menyimpan satu vektor.

        Selain memori, ada soal kestabilan numerik. Konstanta `eps` melindungi pembagian dengan nol, tetapi nilainya memengaruhi perilaku ketika `v` sangat kecil. Nilai `1e-8` aman pada presisi ganda, sedangkan pada presisi rendah banyak praktisi memakai `1e-6` atau lebih besar agar tidak menghasilkan langkah raksasa.
        """),
        E(
            "A3-06-2-ex1",
            "mudah",
            """
            Tulis fungsi `adagrad_langkah(x, G, g, lr, eps=1e-8)` untuk list parameter, list akumulator `G`, dan list gradien `g`. Perbarui `G = G + g^2` lalu `x = x - lr * g / (sqrt(G) + eps)`. Kembalikan tuple `(x_baru, G_baru)` dibulatkan 4 desimal. Hindari `-0.0`.
            """,
            """
            import math

            def adagrad_langkah(x, G, g, lr, eps=1e-8):
                # TODO: implementasikan
                pass
            """,
            """
            r1 = adagrad_langkah([1, 1], [0, 0], [100, 0.01], 0.1)
            assert r1 == ([0.9, 0.9], [10000.0, 0.0001])
            r2 = adagrad_langkah(r1[0], [10000.0, 0.0001], [100, 0.01], 0.1)
            assert r2 == ([0.8293, 0.8293], [20000.0, 0.0002])
            assert adagrad_langkah([0], [0], [0], 0.1) == ([0.0], [0.0])
            assert adagrad_langkah([2], [0], [-4], 0.5) == ([2.5], [16.0])
            """,
            "Tambahkan kuadrat gradien ke akumulator lalu bagi gradien dengan akar akumulator.",
            """
            import math

            def adagrad_langkah(x, G, g, lr, eps=1e-8):
                Gb = [a + b * b for a, b in zip(G, g)]
                xb = [p - lr * b / (math.sqrt(c) + eps) for p, b, c in zip(x, g, Gb)]
                return ([round(v, 4) + 0.0 for v in xb], [round(v, 4) + 0.0 for v in Gb])
            """,
        ),
        E(
            "A3-06-2-ex2",
            "sedang",
            """
            Tulis fungsi `rmsprop_langkah(x, s, g, lr, rho=0.9, eps=1e-8)` yang memperbarui `s = rho * s + (1 - rho) * g^2` lalu `x = x - lr * g / (sqrt(s) + eps)` untuk list. Kembalikan tuple `(x_baru, s_baru)` dibulatkan 4 desimal. Hindari `-0.0`.
            """,
            """
            import math

            def rmsprop_langkah(x, s, g, lr, rho=0.9, eps=1e-8):
                # TODO: implementasikan
                pass
            """,
            """
            assert rmsprop_langkah([1], [0], [2], 0.1) == ([0.6838], [0.4])
            assert rmsprop_langkah([1], [0], [0], 0.1) == ([1.0], [0.0])
            assert rmsprop_langkah([1, 1], [0, 0], [100, 0.01], 0.1) == ([0.6838, 0.6838], [1000.0, 0.0])
            assert rmsprop_langkah([0], [1], [0], 0.1) == ([0.0], [0.9])
            """,
            "Perbarui rata-rata bergerak kuadrat gradien sebelum membagi.",
            """
            import math

            def rmsprop_langkah(x, s, g, lr, rho=0.9, eps=1e-8):
                sb = [rho * a + (1 - rho) * b * b for a, b in zip(s, g)]
                xb = [p - lr * b / (math.sqrt(c) + eps) for p, b, c in zip(x, g, sb)]
                return ([round(v, 4) + 0.0 for v in xb], [round(v, 4) + 0.0 for v in sb])
            """,
        ),
        E(
            "A3-06-2-ex3",
            "sedang",
            """
            Tulis fungsi `adam_langkah(x, m, v, g, t, lr, b1=0.9, b2=0.999, eps=1e-8)` untuk satu parameter skalar. Perbarui `m` dan `v`, hitung `m_hat` dan `v_hat` dengan koreksi bias memakai nomor langkah `t`, lalu perbarui `x`. Kembalikan tuple `(x_baru, m_baru, v_baru)` dibulatkan 4 desimal.
            """,
            """
            import math

            def adam_langkah(x, m, v, g, t, lr, b1=0.9, b2=0.999, eps=1e-8):
                # TODO: implementasikan
                pass
            """,
            """
            assert adam_langkah(5, 0, 0, 10, 1, 0.1) == (4.9, 1.0, 0.1)
            assert adam_langkah(4.9, 1.0, 0.1, 9.8, 2, 0.1) == (4.8001, 1.88, 0.1959)
            assert adam_langkah(5, 0, 0, -10, 1, 0.1) == (5.1, -1.0, 0.1)
            assert adam_langkah(3, 0, 0, 0, 1, 0.1) == (3.0, 0.0, 0.0)
            """,
            "Koreksi bias membagi m dengan satu dikurangi b1 pangkat t dan v dengan satu dikurangi b2 pangkat t.",
            """
            import math

            def adam_langkah(x, m, v, g, t, lr, b1=0.9, b2=0.999, eps=1e-8):
                m = b1 * m + (1 - b1) * g
                v = b2 * v + (1 - b2) * g * g
                mh = m / (1 - b1 ** t)
                vh = v / (1 - b2 ** t)
                x = x - lr * mh / (math.sqrt(vh) + eps)
                return (round(x, 4) + 0.0, round(m, 4) + 0.0, round(v, 4) + 0.0)
            """,
        ),
        E(
            "A3-06-2-ex4",
            "menantang",
            """
            Tulis fungsi `latih(nama, grad, x0, langkah, lr, beta=0.9)` yang menerima nama optimizer `'sgd'`, `'momentum'`, atau `'adam'`, fungsi `grad` (menerima list dan mengembalikan list), titik awal `x0` berupa list, jumlah langkah, learning rate, dan `beta`. Untuk Adam gunakan `beta1 = 0.9`, `beta2 = 0.999`, `eps = 1e-8` dengan koreksi bias. Kembalikan list posisi akhir dibulatkan 4 desimal. Hindari `-0.0`.
            """,
            """
            import math

            def latih(nama, grad, x0, langkah, lr, beta=0.9):
                # TODO: implementasikan
                pass
            """,
            """
            g = lambda p: [p[0], 25 * p[1]]
            L = lambda p: 0.5 * (p[0] ** 2 + 25 * p[1] ** 2)
            assert latih('sgd', g, [10, 1], 1, 0.07) == [9.3, -0.75]
            assert latih('momentum', g, [10, 1], 2, 0.01, 0.9) == [9.711, 0.3375]
            assert latih('adam', g, [10, 1], 1, 0.1) == [9.9, 0.9]
            assert L(latih('sgd', g, [10, 1], 100, 0.07)) < 1e-3
            assert L(latih('momentum', g, [10, 1], 300, 0.01, 0.9)) < 1e-4
            assert L(latih('adam', g, [10, 1], 300, 0.1)) < 0.5
            """,
            "Simpan keadaan optimizer per koordinat dan terapkan rumus masing-masing optimizer pada tiap langkah.",
            """
            import math

            def latih(nama, grad, x0, langkah, lr, beta=0.9):
                x = [float(v) for v in x0]
                n = len(x)
                v = [0.0] * n
                s = [0.0] * n
                b1, b2, eps = 0.9, 0.999, 1e-8
                for t in range(1, langkah + 1):
                    g = grad(x)
                    if nama == 'sgd':
                        x = [x[i] - lr * g[i] for i in range(n)]
                    elif nama == 'momentum':
                        v = [beta * v[i] + g[i] for i in range(n)]
                        x = [x[i] - lr * v[i] for i in range(n)]
                    else:
                        v = [b1 * v[i] + (1 - b1) * g[i] for i in range(n)]
                        s = [b2 * s[i] + (1 - b2) * g[i] * g[i] for i in range(n)]
                        x = [x[i] - lr * (v[i] / (1 - b1 ** t)) / (math.sqrt(s[i] / (1 - b2 ** t)) + eps) for i in range(n)]
                return [round(a, 4) + 0.0 for a in x]
            """,
        ),
    ],
    [
        M("Memakai satu learning rate adil untuk semua optimizer.", "Tuning learning rate tiap optimizer."),
        M("Lupa koreksi bias pada Adam.", "Bagi m dan v dengan 1 - beta pangkat t."),
        M("Mengira Adam selalu lebih baik dari SGD.", "Pilih sesuai masalah dan validasi."),
    ],
    [
        Q("Optimizer adaptif menyesuaikan?", ["Data", "Langkah per parameter", "Jumlah fitur", "Loss"], 1, "Berdasarkan riwayat gradien.", hint="Per parameter."),
        Q("Kelemahan AdaGrad?", ["Terlalu cepat", "Learning rate efektif menyusut terus", "Butuh label", "Tidak stabil"], 1, "Akumulator hanya bertambah.", hint="Menyusut."),
        Q("RMSProp memakai?", ["Jumlah kuadrat gradien", "Rata-rata bergerak kuadrat gradien", "Gradien kedua", "Momentum"], 1, "Rata-rata eksponensial.", hint="Rho."),
        Q("Adam menggabungkan?", ["SGD dan data", "Momentum dan penskalaan adaptif", "Dua loss", "Dua model"], 1, "m dan v.", hint="Dua rata-rata."),
        Q("Koreksi bias Adam diperlukan karena?", ["Gradien bias", "m dan v dimulai dari nol", "Learning rate", "Data kecil"], 1, "Awalnya condong ke nol.", hint="Awal pelatihan."),
    ],
    [
        "AdaGrad dan RMSProp menormalkan langkah per parameter dengan riwayat kuadrat gradien.",
        "Adam menggabungkan momentum dan RMSProp dengan koreksi bias.",
        "Langkah pertama Adam sebesar learning rate pada tiap parameter.",
        "Tidak ada optimizer terbaik universal dan perlu penyetelan.",
    ],
    [],
)

l3 = lesson(
    "A3-06-3",
    "Jadwal learning rate dan stabilisasi pelatihan",
    35,
    [
        "Menjelaskan mengapa learning rate perlu berubah selama pelatihan",
        "Menghitung jadwal step decay, eksponensial, dan cosine",
        "Menambahkan pemanasan pada awal pelatihan",
        "Memotong gradien untuk menstabilkan pelatihan",
    ],
    [
        T("""
        ## Satu nilai tidak cukup

        Learning rate besar membantu kemajuan cepat di awal pelatihan tetapi membuat parameter bergoyang di sekitar minimum pada akhirnya. Learning rate kecil memberi presisi di akhir tetapi lambat di awal. Jawaban alami: mulai besar, lalu kecilkan seiring waktu. Strategi ini disebut **jadwal learning rate** atau learning rate schedule.

        Analoginya mencari barang di ruangan gelap: awalnya kamu melangkah lebar untuk menjelajah, lalu menyempit dan hati-hati begitu dekat sasaran. Hampir semua pelatihan model serius memakai jadwal, dan sering memberi peningkatan akurasi yang nyata dibanding learning rate tetap, tanpa biaya komputasi tambahan.
        """),
        T("""
        ## Jadwal klasik

        **Step decay** mengalikan learning rate dengan faktor `gamma`, misalnya `0,5`, setiap beberapa epoch: `lr = lr0 * gamma^(epoch // setiap)`. Sederhana dan mudah dipahami. **Peluruhan eksponensial** mengalikan dengan faktor tetap tiap epoch: `lr = lr0 * gamma^epoch`, lebih mulus.

        **Cosine annealing** menurunkan learning rate mengikuti setengah gelombang kosinus dari `lr0` ke nol: `lr = lr0/2 * (1 + cos(pi * epoch / total))`. Penurunan awalnya lambat, tengahnya cepat, dan akhirnya lambat lagi. Jadwal ini sangat populer karena tidak butuh banyak hiperparameter selain total langkah, dan sering memberi hasil baik.
        """),
        C(
            """
            import math

            lr0 = 0.1
            epoch = [0, 10, 20, 30]
            step = [round(lr0 * 0.5 ** (e // 10), 4) for e in epoch]
            eksp = [round(lr0 * 0.95 ** e, 4) for e in epoch]
            cos = [round(0.5 * lr0 * (1 + math.cos(math.pi * e / 30)), 4) for e in epoch]
            print(step)
            print(eksp)
            print(cos)
            """,
            """
            [0.1, 0.05, 0.025, 0.0125]
            [0.1, 0.0599, 0.0358, 0.0215]
            [0.1, 0.075, 0.025, 0.0]
            """,
            """
            Step decay turun berundak, peluruhan eksponensial turun mulus, dan cosine turun ke nol tepat pada epoch terakhir.
            """,
            filename="jadwal_lr.py",
        ),
        T("""
        ## Pemanasan

        Pada awal pelatihan, parameter masih acak dan keadaan optimizer, seperti `m` dan `v` pada Adam, belum akurat. Learning rate besar sejak langkah pertama bisa menyebabkan ledakan dan pelatihan tidak stabil, terutama pada model besar seperti transformer. Solusinya **pemanasan**: naikkan learning rate secara linier dari nol sampai nilai target pada beberapa langkah pertama.

        Setelah pemanasan, jadwal normal berlaku, misalnya cosine. Kombinasi pemanasan linier lalu peluruhan cosine adalah resep standar untuk melatih model bahasa dan visi modern. Jumlah langkah pemanasan biasanya beberapa persen dari total pelatihan.
        """),
        C(
            """
            import math

            def lr_warmup_cosine(lr0, t, warm, total):
                if t < warm:
                    return lr0 * (t + 1) / warm
                progres = (t - warm) / (total - warm)
                return 0.5 * lr0 * (1 + math.cos(math.pi * progres))

            print([round(lr_warmup_cosine(0.1, t, 5, 25), 4) for t in range(8)])
            print([round(lr_warmup_cosine(0.1, t, 5, 25), 4) for t in (15, 20, 25)])
            """,
            """
            [0.02, 0.04, 0.06, 0.08, 0.1, 0.1, 0.0994, 0.0976]
            [0.05, 0.0146, 0.0]
            """,
            """
            Lima langkah pertama naik linier ke 0,1. Setelah itu learning rate turun mengikuti cosine dan mencapai 0,05 di pertengahan serta nol pada akhir.
            """,
            filename="warmup.py",
        ),
        K(
            "tip",
            """
            Bila pelatihan model besar tiba-tiba menjadi `nan` pada beberapa langkah awal, tambahkan pemanasan dan pemotongan gradien sebelum mencari penyebab lain.
            """,
            title="Resep stabilisasi",
        ),
        T("""
        ## Pemotongan gradien

        Pada jaringan tertentu, terutama jaringan rekuren dan transformer besar, gradien kadang meledak pada beberapa langkah: satu mini-batch yang tidak biasa menghasilkan gradien raksasa yang melempar parameter jauh dari kondisi baik. **Pemotongan gradien** membatasi besar gradien sebelum langkah dilakukan.

        Ada dua versi. **Pemotongan norma** mengecilkan seluruh vektor gradien bila normanya melebihi ambang, dengan mempertahankan arah: `g = g * maks / norma` bila `norma > maks`. **Pemotongan nilai** membatasi tiap komponen ke rentang `[-c, c]`, yang dapat mengubah arah. Pemotongan norma lebih umum karena arah penurunan terjaga.
        """),
        C(
            """
            import numpy as np

            def klip_norma(g, maks):
                g = np.array(g, dtype=float)
                n = np.linalg.norm(g)
                return g if n <= maks else g * maks / n

            print(klip_norma([3, 4], 1).round(4).tolist())
            print(klip_norma([0.3, 0.4], 1).round(4).tolist())
            print(np.clip([5, -7], -1, 1).tolist())
            """,
            """
            [0.6, 0.8]
            [0.3, 0.4]
            [1, -1]
            """,
            """
            Pemotongan norma menyusutkan vektor tiga empat menjadi panjang satu dengan arah sama, dan tidak mengubah vektor yang sudah pendek. Pemotongan nilai membatasi tiap komponen.
            """,
            filename="clip_gradien.py",
        ),
        T("""
        ## Memilih resep pelatihan

        Rangkuman praktis untuk memulai. Pilih Adam atau AdamW dengan `lr` sekitar `1e-3` untuk model kecil dan menengah, atau `3e-4` untuk transformer. Tambahkan pemanasan beberapa ratus langkah dan peluruhan cosine ke nol. Pasang pemotongan norma gradien di sekitar satu. Pantau kurva loss latih dan validasi, dan lakukan berhenti dini bila validasi stagnan.

        Untuk model visi dengan data besar, SGD dengan momentum `0,9`, `lr` sekitar `0,1` untuk batch 256, step decay atau cosine, dan peluruhan bobot kecil juga resep yang kokoh. Resep ini bukan hukum, melainkan titik awal. Selalu bandingkan beberapa konfigurasi pada data validasi sebelum memutuskan.
        """),
        T("""
        ## Menyetel jadwal dengan data

        Total langkah pada jadwal cosine sebaiknya sama dengan anggaran pelatihan sebenarnya. Bila pelatihan berhenti di tengah jadwal, learning rate masih besar dan hasil akhir kurang presisi. Karena itu tentukan dulu berapa epoch yang mampu dijalani, baru pasang jadwalnya.

        Untuk mencari learning rate puncak, banyak praktisi memakai uji rentang: naikkan learning rate secara eksponensial selama beberapa ratus langkah sambil mencatat loss, lalu pilih nilai sedikit di bawah titik loss mulai naik. Cara murah ini sering menghemat banyak percobaan acak.
        """),
        T("""
        ## Jadwal dan optimizer saling memengaruhi

        Jadwal learning rate tidak berdiri sendiri. Pada Adam, learning rate efektif sudah dinormalkan per parameter, tetapi jadwal tetap memberi manfaat besar karena langkah akhir yang lebih kecil meredam goyangan di sekitar minimum. Pada SGD murni, jadwal bahkan lebih penting karena tanpa penyesuaian skala, learning rate tetap terlalu besar di akhir.

        Bila kamu mengganti optimizer, siapkan untuk menyetel ulang learning rate puncak dan lama pemanasan. Resep yang bagus untuk satu kombinasi jarang langsung cocok untuk kombinasi lain.
        """),
        E(
            "A3-06-3-ex1",
            "mudah",
            """
            Tulis fungsi `lr_step_decay(lr0, gamma, setiap, epoch)` yang mengembalikan `lr0 * gamma ** (epoch // setiap)` dibulatkan 6 desimal.
            """,
            """
            def lr_step_decay(lr0, gamma, setiap, epoch):
                # TODO: implementasikan
                pass
            """,
            """
            assert lr_step_decay(0.1, 0.5, 10, 0) == 0.1
            assert lr_step_decay(0.1, 0.5, 10, 10) == 0.05
            assert lr_step_decay(0.1, 0.5, 10, 25) == 0.025
            assert lr_step_decay(0.1, 0.5, 10, 9) == 0.1
            """,
            "Hitung berapa kali peluruhan sudah terjadi dengan pembagian bulat.",
            """
            def lr_step_decay(lr0, gamma, setiap, epoch):
                return round(lr0 * gamma ** (epoch // setiap), 6)
            """,
        ),
        E(
            "A3-06-3-ex2",
            "sedang",
            """
            Tulis fungsi `lr_cosine(lr0, epoch, total)` yang mengembalikan `0.5 * lr0 * (1 + cos(pi * epoch / total))` dibulatkan 6 desimal. Hindari `-0.0`.
            """,
            """
            import math

            def lr_cosine(lr0, epoch, total):
                # TODO: implementasikan
                pass
            """,
            """
            assert lr_cosine(0.1, 0, 30) == 0.1
            assert lr_cosine(0.1, 10, 30) == 0.075
            assert lr_cosine(0.1, 15, 30) == 0.05
            assert lr_cosine(0.1, 30, 30) == 0.0
            """,
            "Pakai math.cos dan math.pi lalu bulatkan hasilnya.",
            """
            import math

            def lr_cosine(lr0, epoch, total):
                return round(0.5 * lr0 * (1 + math.cos(math.pi * epoch / total)), 6) + 0.0
            """,
        ),
        E(
            "A3-06-3-ex3",
            "sedang",
            """
            Tulis fungsi `lr_warmup_cosine(lr0, t, warm, total)`. Bila `t < warm` kembalikan `lr0 * (t + 1) / warm`. Bila tidak, kembalikan jadwal cosine dengan progres `(t - warm) / (total - warm)`, yaitu `0.5 * lr0 * (1 + cos(pi * progres))`. Bulatkan 6 desimal dan hindari `-0.0`.
            """,
            """
            import math

            def lr_warmup_cosine(lr0, t, warm, total):
                # TODO: implementasikan
                pass
            """,
            """
            assert lr_warmup_cosine(0.1, 0, 5, 25) == 0.02
            assert lr_warmup_cosine(0.1, 4, 5, 25) == 0.1
            assert lr_warmup_cosine(0.1, 5, 5, 25) == 0.1
            assert lr_warmup_cosine(0.1, 15, 5, 25) == 0.05
            assert lr_warmup_cosine(0.1, 25, 5, 25) == 0.0
            """,
            "Pisahkan dua fase dengan percabangan pada t dibanding warm.",
            """
            import math

            def lr_warmup_cosine(lr0, t, warm, total):
                if t < warm:
                    return round(lr0 * (t + 1) / warm, 6) + 0.0
                progres = (t - warm) / (total - warm)
                return round(0.5 * lr0 * (1 + math.cos(math.pi * progres)), 6) + 0.0
            """,
        ),
        E(
            "A3-06-3-ex4",
            "menantang",
            """
            Tulis fungsi `klip_norma(g, maks)` yang menerima list gradien dan ambang `maks`. Bila norma Euclidean melebihi `maks`, skalakan `g` sehingga normanya sama dengan `maks` dengan arah tetap. Kembalikan list dibulatkan 4 desimal dan hindari `-0.0`.
            """,
            """
            import math

            def klip_norma(g, maks):
                # TODO: implementasikan
                pass
            """,
            """
            assert klip_norma([3, 4], 1) == [0.6, 0.8]
            assert klip_norma([0.3, 0.4], 1) == [0.3, 0.4]
            assert klip_norma([0, 0], 1) == [0.0, 0.0]
            assert klip_norma([6, 8], 5) == [3.0, 4.0]
            assert klip_norma([-6, 8], 5) == [-3.0, 4.0]
            """,
            "Hitung norma lalu kalikan tiap komponen dengan maks dibagi norma hanya bila norma lebih besar.",
            """
            import math

            def klip_norma(g, maks):
                n = math.sqrt(sum(v * v for v in g))
                faktor = 1.0 if n <= maks else maks / n
                return [round(v * faktor, 4) + 0.0 for v in g]
            """,
        ),
    ],
    [
        M("Memakai learning rate tetap tinggi sampai akhir.", "Gunakan jadwal agar presisi di akhir."),
        M("Melatih model besar tanpa pemanasan.", "Tambahkan pemanasan untuk stabilitas awal."),
        M("Memotong nilai gradien yang mengubah arah.", "Pemotongan norma mempertahankan arah."),
    ],
    [
        Q("Mengapa learning rate dikecilkan?", ["Agar presisi di akhir", "Agar data besar", "Agar loss naik", "Agar fitur turun"], 0, "Mengurangi goyangan di sekitar minimum.", hint="Dekati sasaran."),
        Q("Cosine annealing menurunkan lr ke?", ["Dua kali", "Nol", "Satu", "Tak hingga"], 1, "Setengah gelombang kosinus.", hint="Mulus."),
        Q("Pemanasan berarti?", ["Menaikkan lr dari kecil di awal", "Menaikkan data", "Mengurangi batch", "Menambah fitur"], 0, "Linier ke nilai target.", hint="Awal."),
        Q("Pemotongan norma mempertahankan?", ["Besar", "Arah", "Tanda saja", "Tidak ada"], 1, "Skala vektor diperkecil.", hint="Arah."),
        Q("Resep awal umum?", ["Adam, pemanasan, cosine, klip norma", "SGD tanpa jadwal", "lr 10", "Tanpa validasi"], 0, "Kombinasi yang stabil.", hint="Titik awal."),
    ],
    [
        "Jadwal learning rate mulai besar lalu mengecil untuk presisi akhir.",
        "Step decay, eksponensial, dan cosine adalah jadwal klasik.",
        "Pemanasan menstabilkan awal pelatihan.",
        "Pemotongan norma gradien mencegah ledakan.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perhitungan yang cukup jelas dalam teks.", "brief": []}

write_module(
    "A3",
    6,
    "Momentum, learning rate, dan optimizer",
    105,
    [
        "Memahami momentum dan Nesterov",
        "Menerapkan AdaGrad, RMSProp, dan Adam",
        "Memakai jadwal learning rate dan pemotongan gradien",
    ],
    [l1, l2, l3],
    video,
    REF,
)
