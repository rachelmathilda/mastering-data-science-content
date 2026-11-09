import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

l1 = lesson(
    "A3-04-1",
    "Aturan rantai dan graf komputasi",
    35,
    [
        "Menerapkan aturan rantai pada komposisi bertingkat",
        "Menggambar perhitungan sebagai graf komputasi",
        "Menjalankan pass maju dan pass mundur secara manual",
        "Menangani variabel yang dipakai lebih dari sekali",
    ],
    [
        T("""
        ## Mengapa aturan rantai sentral

        Model ML adalah komposisi banyak fungsi sederhana: perkalian matriks, penjumlahan bias, aktivasi, lalu loss. Untuk melatihnya kita butuh turunan loss terhadap setiap parameter, dan itu hanya mungkin lewat **aturan rantai**. Bila `y = f(u)` dan `u = g(x)`, maka `dy/dx = dy/du * du/dx`. Laju perubahan bertingkat saling mengalikan.

        Intuisinya sederhana. Bila `u` berubah tiga kali lebih cepat dari `x`, dan `y` berubah dua kali lebih cepat dari `u`, maka `y` berubah enam kali lebih cepat dari `x`. Aturan rantai hanyalah pembukuan faktor penguatan sepanjang rantai. Untuk rantai panjang, kalikan semua faktor lokal dari satu ujung ke ujung lain.
        """),
        T("""
        ## Graf komputasi

        Cara terbaik memahami aturan rantai adalah menggambar perhitungan sebagai **graf komputasi**: simpul adalah nilai antara dan sisi adalah operasi. Misalkan `L = (w x + b - t)^2`. Kita uraikan menjadi langkah elementer: `u = w x`, `v = u + b`, `d = v - t`, `L = d^2`. Tiap langkah memiliki turunan lokal yang sangat sederhana.

        Menghitung nilai `L` dari masukan ke keluaran disebut **pass maju**. Menghitung turunan `L` terhadap semua simpul dari keluaran ke masukan disebut **pass mundur**. Pada pass mundur kita mulai dari `dL/dL = 1`, lalu menyebarkan turunan ke belakang, di tiap simpul mengalikan turunan yang datang dengan turunan lokal operasi itu.
        """),
        C(
            """
            x, w, b, t = 2.0, 3.0, 1.0, 5.0
            u = w * x
            v = u + b
            d = v - t
            L = d ** 2
            print(u, v, d, L)

            dL_dd = 2 * d
            dL_dv = dL_dd
            dL_du = dL_dv
            dL_db = dL_dv
            dL_dw = dL_du * x
            dL_dx = dL_du * w
            print(dL_dw, dL_db, dL_dx)

            def L_fn(x, w, b, t=5.0):
                return (w * x + b - t) ** 2

            h = 1e-6
            print(round((L_fn(x, w + h, b) - L_fn(x, w - h, b)) / (2 * h), 4),
                  round((L_fn(x, w, b + h) - L_fn(x, w, b - h)) / (2 * h), 4),
                  round((L_fn(x + h, w, b) - L_fn(x - h, w, b)) / (2 * h), 4))
            """,
            """
            6.0 7.0 2.0 4.0
            8.0 4.0 12.0
            8.0 4.0 12.0
            """,
            """
            Pass mundur menghasilkan turunan terhadap `w`, `b`, dan `x`, dan hasilnya sama dengan turunan numerik. Penjumlahan meneruskan turunan apa adanya, sedangkan perkalian menukar faktornya.
            """,
            filename="graf_komputasi.py",
        ),
        T("""
        ## Aturan lokal tiap operasi

        Backpropagation bekerja karena setiap operasi dasar punya aturan turunan lokal yang mudah. Pada **penjumlahan**, turunan yang datang diteruskan sama ke kedua masukan. Pada **perkalian** `a b`, turunan untuk `a` adalah turunan datang dikali `b`, dan untuk `b` dikali `a`: faktornya saling menukar. Pada **pangkat dua**, turunan datang dikali dua kali masukan. Pada **tanh**, dikali `1 - tanh^2`.

        Dengan tabel kecil ini, turunan fungsi serumit apa pun dapat dihitung secara mekanis: uraikan menjadi operasi dasar, lakukan pass maju sambil menyimpan nilai antara, lalu pass mundur sambil mengalikan aturan lokal. Itulah seluruh rahasia pustaka diferensiasi otomatis.
        """),
        K(
            "tip",
            """
            Simpan nilai antara dari pass maju. Aturan lokal seperti perkalian membutuhkan nilai masukan, jadi jika tidak disimpan kamu harus menghitungnya ulang saat pass mundur.
            """,
            title="Cache nilai antara",
        ),
        T("""
        ## Rantai yang panjang

        Aturan rantai meluas ke sebanyak apa pun lapisan. Untuk `h(x) = sin(e^(x^2))`, kita punya tiga mata rantai: `a = x^2`, `b = e^a`, `h = sin b`. Turunannya adalah `cos(b) * e^a * 2x`, hasil kali tiga faktor lokal. Setiap faktor dihitung dari nilai antara yang bersesuaian.

        Dalam jaringan dalam puluhan atau ratusan lapisan membuat hasil kali ini sangat panjang. Bila faktor-faktornya cenderung kurang dari satu, hasil kali menyusut dan gradien menghilang. Bila cenderung lebih dari satu, ia meledak. Itu sebabnya perilaku turunan lokal tiap lapisan sangat menentukan keberhasilan pelatihan.
        """),
        C(
            """
            import math

            def h(x):
                return math.sin(math.exp(x ** 2))

            x = 0.5
            a = x ** 2
            b = math.exp(a)
            analitik = math.cos(b) * b * 2 * x
            eps = 1e-6
            numerik = (h(x + eps) - h(x - eps)) / (2 * eps)
            print(round(analitik, 4), round(numerik, 4))
            """,
            """
            0.3632 0.3632
            """,
            """
            Hasil kali tiga faktor lokal sama dengan turunan numerik fungsi komposisi.
            """,
            filename="rantai_panjang.py",
        ),
        T("""
        ## Variabel yang dipakai lebih dari sekali

        Bagaimana bila satu variabel masuk ke beberapa operasi? Contohnya `z = x * x`, atau `f(x) = x sin(x)` yang memakai `x` di dua tempat. Turunan terhadap `x` adalah **jumlah** kontribusi dari semua jalur yang berangkat dari `x` menuju keluaran. Inilah aturan rantai multivariabel versi sederhana.

        Untuk `z = x * x`: jalur pertama lewat operand kiri menyumbang `x`, jalur kedua lewat operand kanan menyumbang `x`, total `2x`. Untuk `x sin(x)`: jalur lewat faktor pertama menyumbang `sin(x)`, jalur lewat `sin` menyumbang `x cos(x)`. Dalam implementasi, ini berarti gradien diakumulasi dengan `+=`, bukan diganti dengan `=`. Lupa akumulasi adalah bug klasik pada autograd buatan sendiri.
        """),
        C(
            """
            import math

            x = 3.0
            gx = 0.0
            gx += x
            gx += x
            print(gx)

            x = 1.0
            analitik = math.sin(x) + x * math.cos(x)
            f = lambda t: t * math.sin(t)
            numerik = (f(x + 1e-6) - f(x - 1e-6)) / 2e-6
            print(round(analitik, 4), round(numerik, 4))
            """,
            """
            6.0
            1.3818 1.3818
            """,
            """
            Dua jalur dari `x` ke `x * x` masing-masing menyumbang `x` dan dijumlahkan. Pada `x sin(x)` dua jalur menghasilkan dua suku yang cocok dengan turunan numerik.
            """,
            filename="bercabang.py",
        ),
        T("""
        ## Kebiasaan menghitung turunan

        Saat menemui fungsi baru, biasakan tiga langkah. Pertama, uraikan fungsi menjadi operasi dasar dan gambar grafnya, walau hanya di kertas. Kedua, tuliskan turunan lokal tiap simpul. Ketiga, kalikan sepanjang jalur dan jumlahkan di tempat jalur bertemu. Tiga langkah ini membuat turunan serumit apa pun terasa terkendali. Latih kebiasaan ini pada beberapa contoh kecil sebelum memakai pustaka, supaya hasil otomatisnya bisa kamu periksa dengan akal sehat.
        """),
        E(
            "A3-04-1-ex1",
            "mudah",
            """
            Tulis fungsi `maju_mundur_linear(x, w, b, t)` untuk graf `L = (w x + b - t)^2` dan kembalikan tuple `(L, dL/dw, dL/db, dL/dx)` sebagai bilangan float. Hindari `-0.0`.
            """,
            """
            def maju_mundur_linear(x, w, b, t):
                # TODO: implementasikan
                pass
            """,
            """
            assert maju_mundur_linear(2, 3, 1, 5) == (4.0, 8.0, 4.0, 12.0)
            assert maju_mundur_linear(1, 1, 0, 1) == (0.0, 0.0, 0.0, 0.0)
            assert maju_mundur_linear(0, 2, 3, 0) == (9.0, 0.0, 6.0, 12.0)
            assert maju_mundur_linear(1, -1, 0, 2) == (9.0, -6.0, -6.0, 6.0)
            """,
            "Hitung d = w x + b - t lalu turunan L terhadap d adalah dua kali d. Kalikan dengan aturan lokal.",
            """
            def maju_mundur_linear(x, w, b, t):
                d = w * x + b - t
                L = d ** 2
                dd = 2 * d
                return (float(L) + 0.0, float(dd * x) + 0.0, float(dd) + 0.0, float(dd * w) + 0.0)
            """,
        ),
        E(
            "A3-04-1-ex2",
            "sedang",
            """
            Tulis fungsi `rantai_tiga(df, dg, dh, g, h, x)` yang mengembalikan turunan `f(g(h(x)))` terhadap `x` yaitu `df(g(h(x))) * dg(h(x)) * dh(x)`, dibulatkan 4 desimal.
            """,
            """
            import math

            def rantai_tiga(df, dg, dh, g, h, x):
                # TODO: implementasikan
                pass
            """,
            """
            f1 = lambda u: u * u
            df1 = lambda u: 2 * u
            g1 = lambda u: u + 1
            dg1 = lambda u: 1
            h1 = lambda x: x ** 3
            dh1 = lambda x: 3 * x ** 2
            assert rantai_tiga(df1, dg1, dh1, g1, h1, 1) == 12.0
            assert rantai_tiga(df1, dg1, dh1, g1, h1, 2) == 216.0
            g2 = lambda u: 2 * u
            dg2 = lambda u: 2
            h2 = lambda x: x + 1
            dh2 = lambda x: 1
            assert rantai_tiga(math.exp, dg2, dh2, g2, h2, 0) == 14.7781
            assert rantai_tiga(math.exp, dg2, dh2, g2, h2, -1) == 2.0
            """,
            "Hitung nilai antara h(x) lalu g(h(x)) dan kalikan tiga turunan lokal.",
            """
            import math

            def rantai_tiga(df, dg, dh, g, h, x):
                a = h(x)
                b = g(a)
                return round(df(b) * dg(a) * dh(x), 4)
            """,
        ),
        E(
            "A3-04-1-ex3",
            "sedang",
            """
            Tulis fungsi `jumlah_jalur(jalur)` yang menerima list jalur, tiap jalur adalah list turunan lokal sepanjang jalur itu, dan mengembalikan jumlah hasil kali tiap jalur. Bila tidak ada jalur kembalikan `0`.
            """,
            """
            def jumlah_jalur(jalur):
                # TODO: implementasikan
                pass
            """,
            """
            assert jumlah_jalur([[2, 3], [4]]) == 10
            assert jumlah_jalur([[1, 1, 1]]) == 1
            assert jumlah_jalur([[0.5, 0.5], [0.5, 0.5]]) == 0.5
            assert jumlah_jalur([]) == 0
            """,
            "Kalikan turunan sepanjang tiap jalur lalu jumlahkan semua jalur.",
            """
            def jumlah_jalur(jalur):
                total = 0
                for j in jalur:
                    hasil = 1
                    for v in j:
                        hasil *= v
                    total += hasil
                return total
            """,
        ),
        E(
            "A3-04-1-ex4",
            "menantang",
            """
            Tulis fungsi `backward_skalar(masukan, ops)` untuk graf komputasi skalar. `masukan` adalah list nilai, dan `ops` adalah list operasi, tiap operasi membuat simpul baru bernomor `len(masukan) + indeks_operasi`. Operasi berbentuk `('add', i, j)`, `('sub', i, j)`, `('mul', i, j)`, atau `('pow2', i)` yang merujuk nomor simpul. Hitung nilai maju lalu turunan simpul terakhir terhadap tiap masukan dengan pass mundur dan akumulasi gradien. Kembalikan list turunan masukan dibulatkan 4 desimal, hindari `-0.0`.
            """,
            """
            def backward_skalar(masukan, ops):
                # TODO: implementasikan
                pass
            """,
            """
            assert backward_skalar([2, 3], [('mul', 0, 1)]) == [3.0, 2.0]
            assert backward_skalar([2, -3, 10], [('mul', 0, 1), ('add', 3, 2)]) == [-3.0, 2.0, 1.0]
            assert backward_skalar([2, 3, 1, 5], [('mul', 1, 0), ('add', 4, 2), ('sub', 5, 3), ('pow2', 6)]) == [12.0, 8.0, 4.0, -4.0]
            assert backward_skalar([3], [('mul', 0, 0)]) == [6.0]
            """,
            "Simpan semua nilai simpul lalu telusuri operasi dari belakang dan tambahkan kontribusi ke gradien operand.",
            """
            def backward_skalar(masukan, ops):
                n = len(masukan)
                nilai = [float(v) for v in masukan]
                for op in ops:
                    if op[0] == 'add':
                        nilai.append(nilai[op[1]] + nilai[op[2]])
                    elif op[0] == 'sub':
                        nilai.append(nilai[op[1]] - nilai[op[2]])
                    elif op[0] == 'mul':
                        nilai.append(nilai[op[1]] * nilai[op[2]])
                    else:
                        nilai.append(nilai[op[1]] ** 2)
                grad = [0.0] * len(nilai)
                grad[-1] = 1.0
                for k in range(len(ops) - 1, -1, -1):
                    op = ops[k]
                    g = grad[n + k]
                    if op[0] == 'add':
                        grad[op[1]] += g
                        grad[op[2]] += g
                    elif op[0] == 'sub':
                        grad[op[1]] += g
                        grad[op[2]] -= g
                    elif op[0] == 'mul':
                        grad[op[1]] += g * nilai[op[2]]
                        grad[op[2]] += g * nilai[op[1]]
                    else:
                        grad[op[1]] += g * 2 * nilai[op[1]]
                return [round(v, 4) + 0.0 for v in grad[:n]]
            """,
        ),
    ],
    [
        M("Mengganti gradien dengan = saat variabel dipakai berkali-kali.", "Akumulasikan dengan +=."),
        M("Lupa menyimpan nilai antara dari pass maju.", "Simpan agar pass mundur tidak menghitung ulang."),
        M("Menukar faktor pada aturan perkalian.", "Turunan ke a adalah turunan datang kali b."),
    ],
    [
        Q("Aturan rantai?", ["dy/dx = dy/du du/dx", "dy/dx = dy + du", "dy/dx = du/dy", "dy/dx = y/x"], 0, "Faktor perubahan dikalikan.", hint="Kalikan."),
        Q("Pass mundur dimulai dari?", ["Masukan", "Loss dengan turunan satu", "Parameter", "Data"], 1, "dL/dL = 1.", hint="Ujung graf."),
        Q("Pada penjumlahan turunan?", ["Dikalikan nol", "Diteruskan sama", "Dibagi dua", "Dihapus"], 1, "Kedua masukan menerima turunan yang sama.", hint="Pipa."),
        Q("Pada perkalian a b turunan ke a?", ["Turunan datang kali b", "Turunan datang kali a", "Turunan datang", "Nol"], 0, "Faktor menukar.", hint="Silang."),
        Q("Variabel dipakai dua kali?", ["Pakai salah satu jalur", "Jumlahkan kontribusi semua jalur", "Kalikan jalur", "Abaikan"], 1, "Gradien diakumulasi.", hint="Plus."),
    ],
    [
        "Aturan rantai mengalikan turunan lokal sepanjang rantai.",
        "Graf komputasi mengurai fungsi menjadi operasi dengan turunan sederhana.",
        "Pass maju menghitung nilai dan pass mundur menghitung turunan.",
        "Variabel yang dipakai berulang menerima gradien yang dijumlahkan.",
    ],
    [],
)

l2 = lesson(
    "A3-04-2",
    "Backpropagation pada lapisan dan jaringan",
    35,
    [
        "Menurunkan turunan lapisan linear dalam bentuk vektor",
        "Menyusun backward pass untuk aktivasi ReLU dan tanh",
        "Menghitung gradien jaringan dua lapis kecil",
        "Mengenali gradien menghilang pada aktivasi jenuh",
    ],
    [
        T("""
        ## Dari skalar ke vektor

        Pelajaran sebelumnya memakai skalar. Jaringan nyata memakai vektor dan matriks, tetapi ide dasarnya sama. Sebuah lapisan linear menghitung `y = W x`, dengan `W` berukuran `m x n` dan `x` berukuran `n`. Misalkan dari lapisan berikutnya datang turunan `dy = dL/dy` berukuran `m`. Kita ingin `dW` dan `dx`.

        Hasilnya rapi. `dW = dy x^T`, yaitu perkalian luar `dy` dan `x`, berukuran `m x n` sama seperti `W`. Dan `dx = W^T dy`, berukuran `n`. Perhatikan pola transposnya: untuk menyebar turunan mundur kita memakai transpos matriks maju. Dua rumus ini adalah jantung backpropagation pada lapisan padat.
        """),
        C(
            """
            import numpy as np

            W = np.array([[1.0, 2.0, 0.0], [0.0, 1.0, -1.0]])
            x = np.array([1.0, 2.0, 3.0])
            y = W @ x
            L = float(np.sum(y ** 2))
            print(y.tolist(), L)
            dy = 2 * y
            dW = np.outer(dy, x)
            dx = W.T @ dy
            print(dW.tolist())
            print(dx.tolist())

            def loss(W, x):
                return float(np.sum((W @ x) ** 2))

            h = 1e-6
            dx_num = np.array([(loss(W, x + h * e) - loss(W, x - h * e)) / (2 * h) for e in np.eye(3)])
            print(np.allclose(dx, dx_num, atol=1e-4))
            """,
            """
            [5.0, -1.0] 26.0
            [[10.0, 20.0, 30.0], [-2.0, -4.0, -6.0]]
            [10.0, 18.0, 2.0]
            True
            """,
            """
            Gradien bobot adalah perkalian luar turunan keluaran dan masukan, dan gradien masukan memakai transpos bobot. Hasilnya cocok dengan turunan numerik.
            """,
            filename="lapisan_vektor.py",
        ),
        T("""
        ## Backward untuk aktivasi

        Aktivasi bekerja per elemen sehingga backward-nya sederhana: kalikan turunan datang dengan turunan aktivasi pada masukan lapisan itu, elemen demi elemen. Untuk **ReLU** turunan lokalnya satu bila masukan positif dan nol bila tidak, sehingga ReLU bertindak sebagai **topeng** yang meneruskan gradien hanya di unit yang aktif. Untuk **tanh** turunan lokalnya `1 - tanh^2`, dan untuk sigmoid `s (1 - s)`.

        Perhatikan bahwa backward ReLU membuang gradien unit yang tidak aktif. Bila sebuah unit selalu tidak aktif untuk semua data, bobotnya tidak pernah diperbarui. Kondisi ini disebut ReLU mati, dan salah satu alasan variasi seperti leaky ReLU diciptakan.
        """),
        C(
            """
            import numpy as np

            z = np.array([-1.0, 2.0, 0.5, -3.0])
            g = np.ones(4)
            print((g * (z > 0)).tolist())

            def sigmoid(z):
                return 1 / (1 + np.exp(-z))

            z2 = np.array([-10.0, 0.0, 10.0])
            s = sigmoid(z2)
            print((s * (1 - s)).round(4).tolist())
            print(f"{0.25 ** 10:.4e}")
            """,
            """
            [0.0, 1.0, 1.0, 0.0]
            [0.0, 0.25, 0.0]
            9.5367e-07
            """,
            """
            Gradien ReLU hanya lewat di unit aktif. Sigmoid jenuh memiliki turunan hampir nol dan hasil kali sepuluh turunan maksimalnya sudah di bawah sepersejuta.
            """,
            filename="relu_masker.py",
        ),
        K(
            "warning",
            """
            Sigmoid dalam lapisan tersembunyi pada jaringan dalam hampir selalu menyebabkan gradien menghilang karena turunan maksimalnya hanya 0,25. Pilih ReLU atau varian modernnya untuk lapisan tersembunyi.
            """,
            title="Gradien menghilang",
        ),
        T("""
        ## Jaringan dua lapis

        Mari rakit jaringan kecil: masukan `x` berdimensi dua, lapisan tersembunyi tiga unit dengan aktivasi tanh, lalu keluaran skalar linear, dengan loss kuadrat terhadap target `t`. Pass maju: `z1 = W1 x + b1`, `h = tanh(z1)`, `y = w2 . h + b2`, `L = (y - t)^2`.

        Pass mundur mengikuti urutan terbalik. `dy = 2 (y - t)`. Lalu `dw2 = dy h` dan `db2 = dy`. Turunan ke `h` adalah `dh = dy w2`. Melewati tanh: `dz1 = dh * (1 - h^2)`. Akhirnya `dW1 = outer(dz1, x)`, `db1 = dz1`. Enam baris ini adalah backpropagation lengkap untuk jaringan dua lapis. Jaringan lebih dalam hanya mengulang pola yang sama untuk tiap lapisan.
        """),
        C(
            """
            import numpy as np

            W1 = np.array([[0.1, 0.2], [0.3, -0.1], [-0.2, 0.4]])
            b1 = np.zeros(3)
            w2 = np.array([0.5, -0.3, 0.8])
            b2 = 0.1
            x = np.array([1.0, 2.0])
            t = 1.0

            def maju(W1, b1, w2, b2):
                z1 = W1 @ x + b1
                h = np.tanh(z1)
                y = float(w2 @ h + b2)
                return z1, h, y, (y - t) ** 2

            z1, h, y, L = maju(W1, b1, w2, b2)
            dy = 2 * (y - t)
            dw2 = dy * h
            db2 = dy
            dh = dy * w2
            dz1 = dh * (1 - h ** 2)
            dW1 = np.outer(dz1, x)
            db1 = dz1
            print(round(L, 4))

            eps = 1e-6
            W1p = W1.copy()
            W1p[2, 1] += eps
            W1m = W1.copy()
            W1m[2, 1] -= eps
            num = (maju(W1p, b1, w2, b2)[3] - maju(W1m, b1, w2, b2)[3]) / (2 * eps)
            print(round(float(dW1[2, 1]), 4), round(num, 4))
            w2p = w2.copy()
            w2p[0] += eps
            w2m = w2.copy()
            w2m[0] -= eps
            num2 = (maju(W1, b1, w2p, b2)[3] - maju(W1, b1, w2m, b2)[3]) / (2 * eps)
            print(round(float(dw2[0]), 4), round(num2, 4))
            """,
            """
            0.0725
            -0.613 -0.613
            -0.2488 -0.2488
            """,
            """
            Dua elemen gradien yang dipilih cocok dengan turunan numerik. Pemeriksaan seperti ini adalah gradient check pada jaringan penuh.
            """,
            filename="jaringan_dua_lapis.py",
        ),
        T("""
        ## Pola umum backpropagation

        Dari contoh tadi kita bisa menyimpulkan pola umum. Tiap lapisan menyimpan masukan dan keluarannya pada pass maju. Pada pass mundur tiap lapisan menerima turunan dari lapisan berikutnya, menghitung turunan terhadap parameternya sendiri, dan meneruskan turunan terhadap masukannya ke lapisan sebelumnya. Antarmuka seragam ini membuat jaringan bisa dirakit seperti balok lego.

        Itulah mengapa pustaka deep learning mendefinisikan setiap lapisan dengan dua fungsi, `forward` dan `backward`. Tugasmu sebagai pengguna cukup merangkai lapisan, dan mesin mengatur urutan pass mundur. Namun memahami mekanismenya membuatmu mampu mengecek gradien, mendesain lapisan kustom, dan memahami sumber kegagalan pelatihan.
        """),
        T("""
        ## Ukuran dan bentuk gradien

        Aturan praktis yang sangat membantu: gradien parameter selalu memiliki bentuk yang sama dengan parameternya. Bila `W` berukuran dua kali tiga maka `dW` juga dua kali tiga. Bila hasil perhitungan gradienmu berbentuk lain, hampir pasti ada transpos yang salah atau perkalian yang tertukar.

        Aturan ini juga berlaku untuk bias dan masukan. Memeriksa bentuk adalah gradient check termurah yang bisa dilakukan, dan menangkap sebagian besar kesalahan sebelum kamu sempat menjalankan pelatihan. Biasakan menulis pernyataan assert bentuk di kode backward buatan sendiri.
        """),
        T("""
        ## Batch data

        Pada praktiknya kita memproses banyak sampel sekaligus dalam satu batch. Masukan menjadi matriks `X` berukuran `batch x n`, dan lapisan linear menjadi `Y = X W^T`. Rumus mundurnya berubah sedikit: `dW = dY^T X` dan `dX = dY W`, dengan gradien dijumlahkan atau dirata-ratakan atas batch.

        Penjumlahan atas batch muncul secara alami dari aturan akumulasi: parameter yang sama dipakai oleh setiap sampel, sehingga gradiennya adalah jumlah kontribusi tiap sampel. Itu alasan loss biasanya dirata-ratakan atas batch agar skala gradien tidak bergantung pada ukuran batch.
        """),
        E(
            "A3-04-2-ex1",
            "mudah",
            """
            Tulis fungsi `relu_backward(z, g)` yang menerima list masukan `z` dan list turunan datang `g` dan mengembalikan list turunan setelah melewati ReLU: `g_i` bila `z_i > 0` dan `0.0` bila tidak.
            """,
            """
            def relu_backward(z, g):
                # TODO: implementasikan
                pass
            """,
            """
            assert relu_backward([-1, 2, 0.5, -3], [1, 1, 1, 1]) == [0, 1, 1, 0]
            assert relu_backward([1, 2], [0.5, 0.25]) == [0.5, 0.25]
            assert relu_backward([0], [5]) == [0]
            assert relu_backward([], []) == []
            """,
            "Teruskan g hanya di posisi tempat z positif.",
            """
            def relu_backward(z, g):
                return [gi if zi > 0 else 0.0 for zi, gi in zip(z, g)]
            """,
        ),
        E(
            "A3-04-2-ex2",
            "sedang",
            """
            Tulis fungsi `linear_backward(W, x, dy)` untuk lapisan `y = W x` (list of list dan list). Kembalikan tuple `(dW, dx)` dengan `dW[i][j] = dy[i] * x[j]` dan `dx[j] = sum_i W[i][j] * dy[i]`.
            """,
            """
            def linear_backward(W, x, dy):
                # TODO: implementasikan
                pass
            """,
            """
            assert linear_backward([[1, 2, 0], [0, 1, -1]], [1, 2, 3], [10, -2]) == ([[10, 20, 30], [-2, -4, -6]], [10, 18, 2])
            assert linear_backward([[2]], [3], [1]) == ([[3]], [2])
            assert linear_backward([[1, 0], [0, 1]], [1, 1], [0, 0]) == ([[0, 0], [0, 0]], [0, 0])
            assert linear_backward([[1, 2]], [1, 1], [2]) == ([[2, 2]], [2, 4])
            """,
            "Bentuk perkalian luar untuk dW dan perkalian transpos W dengan dy untuk dx.",
            """
            def linear_backward(W, x, dy):
                m, n = len(W), len(x)
                dW = [[dy[i] * x[j] for j in range(n)] for i in range(m)]
                dx = [sum(W[i][j] * dy[i] for i in range(m)) for j in range(n)]
                return (dW, dx)
            """,
        ),
        E(
            "A3-04-2-ex3",
            "sedang",
            """
            Tulis fungsi `mse_backward(y, t)` yang mengembalikan tuple `(loss, dy)`. `loss` adalah rata-rata `(y_i - t_i)^2` dibulatkan 4 desimal dan `dy` adalah list `2 (y_i - t_i) / n` dibulatkan 4 desimal. Hindari `-0.0`.
            """,
            """
            def mse_backward(y, t):
                # TODO: implementasikan
                pass
            """,
            """
            assert mse_backward([1, 2], [0, 0]) == (2.5, [1.0, 2.0])
            assert mse_backward([3], [3]) == (0.0, [0.0])
            assert mse_backward([0, 0, 0], [1, 1, 1]) == (1.0, [-0.6667, -0.6667, -0.6667])
            assert mse_backward([2, 4], [1, 6]) == (2.5, [1.0, -2.0])
            """,
            "Hitung galat per elemen lalu rata-ratakan kuadratnya untuk loss dan bagi dua kali galat dengan n untuk turunan.",
            """
            def mse_backward(y, t):
                n = len(y)
                galat = [a - b for a, b in zip(y, t)]
                loss = round(sum(e * e for e in galat) / n, 4)
                dy = [round(2 * e / n, 4) + 0.0 for e in galat]
                return (loss, dy)
            """,
        ),
        E(
            "A3-04-2-ex4",
            "menantang",
            """
            Tulis fungsi `backprop_mlp(x, W1, b1, W2, b2, t)` untuk jaringan dengan lapisan tersembunyi ReLU dan keluaran linear: `h = relu(W1 x + b1)`, `y = W2 h + b2`, `L = sum (y - t)^2`. Semua masukan list atau list of list. Kembalikan tuple `(L, dW1, db1, dW2, db2)` sebagai float, tanpa `-0.0`.
            """,
            """
            def backprop_mlp(x, W1, b1, W2, b2, t):
                # TODO: implementasikan
                pass
            """,
            """
            assert backprop_mlp([1], [[2]], [0], [[3]], [0], [0]) == (36.0, [[36.0]], [36.0], [[24.0]], [12.0])
            assert backprop_mlp([-1], [[2]], [0], [[3]], [0], [0]) == (0.0, [[0.0]], [0.0], [[0.0]], [0.0])
            assert backprop_mlp([1, 2], [[1, 0], [0, 1]], [0, -5], [[1, 1]], [0], [0]) == (1.0, [[2.0, 4.0], [0.0, 0.0]], [2.0, 0.0], [[2.0, 0.0]], [2.0])
            """,
            "Lakukan pass maju sambil menyimpan z dan h lalu pass mundur dengan rumus linear dan topeng ReLU.",
            """
            def backprop_mlp(x, W1, b1, W2, b2, t):
                m, n = len(W1), len(x)
                k = len(W2)
                z = [sum(W1[i][j] * x[j] for j in range(n)) + b1[i] for i in range(m)]
                h = [v if v > 0 else 0.0 for v in z]
                y = [sum(W2[r][i] * h[i] for i in range(m)) + b2[r] for r in range(k)]
                L = sum((y[r] - t[r]) ** 2 for r in range(k))
                dy = [2 * (y[r] - t[r]) for r in range(k)]
                dW2 = [[dy[r] * h[i] for i in range(m)] for r in range(k)]
                db2 = list(dy)
                dh = [sum(W2[r][i] * dy[r] for r in range(k)) for i in range(m)]
                dz = [dh[i] if z[i] > 0 else 0.0 for i in range(m)]
                dW1 = [[dz[i] * x[j] for j in range(n)] for i in range(m)]
                db1 = list(dz)
                f = lambda v: float(v) + 0.0
                return (f(L), [[f(v) for v in r] for r in dW1], [f(v) for v in db1], [[f(v) for v in r] for r in dW2], [f(v) for v in db2])
            """,
        ),
    ],
    [
        M("Lupa transpos pada gradien masukan lapisan linear.", "dx = W^T dy."),
        M("Memakai sigmoid pada banyak lapisan tersembunyi.", "Pakai ReLU atau varian agar gradien tidak menghilang."),
        M("Tidak memeriksa gradien dengan turunan numerik.", "Lakukan gradient check pada jaringan kecil."),
    ],
    [
        Q("Gradien bobot lapisan y = W x?", ["dy x^T", "W dy", "x dy^T W", "dy + x"], 0, "Perkalian luar.", hint="Ukuran sama dengan W."),
        Q("Gradien masukan?", ["W dy", "W^T dy", "dy", "x"], 1, "Pakai transpos.", hint="Mundur."),
        Q("ReLU pada backward?", ["Mengalikan dua", "Topeng unit aktif", "Menjumlah", "Mengurangi"], 1, "Gradien hanya lewat di unit positif.", hint="Aktif."),
        Q("Turunan lokal tanh?", ["1 - tanh^2", "tanh", "1 + tanh", "tanh^2"], 0, "Satu dikurangi kuadrat.", hint="Maksimum satu."),
        Q("Gradien menghilang karena?", ["Banyak faktor kecil dikalikan", "Learning rate", "Data kurang", "Bias"], 0, "Hasil kali menyusut.", hint="Sigmoid."),
    ],
    [
        "Lapisan linear menurunkan dW sebagai perkalian luar dan dx lewat transpos W.",
        "ReLU meneruskan gradien hanya di unit aktif dan tanh mengalikan 1 - tanh^2.",
        "Backprop jaringan dua lapis memakai enam langkah mundur.",
        "Aktivasi jenuh dan rantai panjang menyebabkan gradien menghilang.",
    ],
    [],
)

l3 = lesson(
    "A3-04-3",
    "Membangun mini autograd dari nol",
    35,
    [
        "Mengimplementasikan kelas Value yang melacak graf komputasi",
        "Menjalankan backward dengan urutan topologis",
        "Melatih parameter sederhana memakai autograd buatan sendiri",
        "Memverifikasi autograd dengan turunan numerik",
    ],
    [
        T("""
        ## Ide autograd

        Menurunkan tangan setiap model tidak praktis. **Diferensiasi otomatis** menghitung turunan secara mekanis dari program yang menghitung fungsi. Ide intinya: bungkus tiap bilangan dalam objek yang mengingat dari operasi mana ia berasal. Setiap operasi mencatat siapa masukannya dan bagaimana menyebarkan gradien mundur. Setelah nilai akhir dihitung, kita menelusuri catatan itu dari belakang.

        Pada pelajaran ini kamu membangun versi mini, kelas `Value`, dalam sekitar tiga puluh baris. Meski kecil, ia memuat seluruh gagasan PyTorch dan TensorFlow: graf dinamis, pass mundur, dan akumulasi gradien. Setelah ini kerja pustaka besar tidak lagi terasa seperti sihir.
        """),
        T("""
        ## Rancangan kelas Value

        Tiap `Value` menyimpan empat hal: `data` yaitu nilainya, `grad` yaitu turunan keluaran akhir terhadap nilai ini, `_prev` yaitu himpunan simpul masukannya, dan `_back` yaitu fungsi kecil yang menyebarkan `grad` ke simpul-simpul masukan. Operasi seperti `+` dan `*` membuat `Value` baru dan mendefinisikan `_back` yang sesuai dengan aturan lokal.

        Untuk penjumlahan, `_back` menambahkan `out.grad` ke kedua masukan. Untuk perkalian, ia menambahkan `out.grad` dikali nilai masukan lainnya. Perhatikan `+=`: gradien harus diakumulasi karena sebuah simpul boleh dipakai berkali-kali. Gradien awal semua simpul adalah nol, dan simpul keluaran diberi gradien satu.
        """),
        C(
            """
            import math

            class Value:
                def __init__(self, data, anak=()):
                    self.data = data
                    self.grad = 0.0
                    self._back = lambda: None
                    self._prev = set(anak)

                def __add__(self, o):
                    o = o if isinstance(o, Value) else Value(o)
                    out = Value(self.data + o.data, (self, o))
                    def _b():
                        self.grad += out.grad
                        o.grad += out.grad
                    out._back = _b
                    return out

                __radd__ = __add__

                def __mul__(self, o):
                    o = o if isinstance(o, Value) else Value(o)
                    out = Value(self.data * o.data, (self, o))
                    def _b():
                        self.grad += o.data * out.grad
                        o.grad += self.data * out.grad
                    out._back = _b
                    return out

                __rmul__ = __mul__

                def __neg__(self):
                    return self * -1

                def __sub__(self, o):
                    o = o if isinstance(o, Value) else Value(o)
                    return self + (-o)

                def __pow__(self, n):
                    out = Value(self.data ** n, (self,))
                    def _b():
                        self.grad += n * self.data ** (n - 1) * out.grad
                    out._back = _b
                    return out

                def tanh(self):
                    t = math.tanh(self.data)
                    out = Value(t, (self,))
                    def _b():
                        self.grad += (1 - t * t) * out.grad
                    out._back = _b
                    return out

                def backward(self):
                    urut, terlihat = [], set()
                    def bangun(v):
                        if v not in terlihat:
                            terlihat.add(v)
                            for p in v._prev:
                                bangun(p)
                            urut.append(v)
                    bangun(self)
                    self.grad = 1.0
                    for v in reversed(urut):
                        v._back()

            a, b, c = Value(2.0), Value(-3.0), Value(10.0)
            d = a * b + c
            d.backward()
            print(d.data, a.grad, b.grad, c.grad)
            x, w, bb = Value(2.0), Value(3.0), Value(1.0)
            L = (w * x + bb - 5) ** 2
            L.backward()
            print(L.data, w.grad, bb.grad, x.grad)
            z = Value(3.0)
            q = z * z
            q.backward()
            print(z.grad)
            """,
            """
            4.0 -3.0 2.0 1.0
            4.0 8.0 4.0 12.0
            6.0
            """,
            """
            Hasilnya sama dengan hitungan tangan pada pelajaran sebelumnya, termasuk akumulasi pada `z * z` yang memakai `z` dua kali.
            """,
            filename="mini_autograd.py",
        ),
        T("""
        ## Urutan topologis

        Fungsi `backward` perlu memproses simpul dalam urutan yang benar: sebuah simpul hanya boleh menyebarkan gradiennya setelah semua simpul yang bergantung padanya selesai menyumbang. Urutan seperti itu disebut **urutan topologis** graf berarah tanpa siklus. Kita membangunnya dengan penelusuran depth-first: kunjungi semua masukan lebih dulu, lalu tambahkan simpul itu ke daftar.

        Daftar yang dihasilkan memuat masukan sebelum keluaran. Membaliknya memberi urutan pass mundur yang tepat. Tanpa urutan ini gradien bisa disebarkan terlalu cepat sebelum nilainya lengkap, dan hasilnya salah secara diam-diam, jenis bug yang sulit ditemukan.
        """),
        K(
            "warning",
            """
            Selalu nol-kan gradien parameter sebelum pass mundur baru. Karena gradien diakumulasi dengan `+=`, gradien lama akan menumpuk dan merusak pembaruan.
            """,
            title="Nol-kan gradien",
        ),
        T("""
        ## Melatih dengan autograd

        Dengan autograd, melatih model menjadi perulangan sederhana. Bungkus parameter dalam `Value`. Pada tiap iterasi: hitung loss lewat pass maju, nol-kan gradien parameter, panggil `loss.backward()`, lalu perbarui setiap parameter dengan `data -= lr * grad`. Tidak ada turunan yang ditulis tangan, karena semuanya datang dari graf yang direkam.

        Contoh di bawah mencocokkan `y = 2x + 1` dari empat titik data dengan model `w x + b`. Meski mini, perulangan ini bentuknya identik dengan pelatihan di PyTorch: maju, nol-kan, mundur, perbarui. Satu-satunya perbedaan adalah skala dan kecepatan.
        """),
        C(
            """
            import math

            class Value:
                def __init__(self, data, anak=()):
                    self.data = data
                    self.grad = 0.0
                    self._back = lambda: None
                    self._prev = set(anak)

                def __add__(self, o):
                    o = o if isinstance(o, Value) else Value(o)
                    out = Value(self.data + o.data, (self, o))
                    def _b():
                        self.grad += out.grad
                        o.grad += out.grad
                    out._back = _b
                    return out

                __radd__ = __add__

                def __mul__(self, o):
                    o = o if isinstance(o, Value) else Value(o)
                    out = Value(self.data * o.data, (self, o))
                    def _b():
                        self.grad += o.data * out.grad
                        o.grad += self.data * out.grad
                    out._back = _b
                    return out

                __rmul__ = __mul__

                def __neg__(self):
                    return self * -1

                def __sub__(self, o):
                    o = o if isinstance(o, Value) else Value(o)
                    return self + (-o)

                def __pow__(self, n):
                    out = Value(self.data ** n, (self,))
                    def _b():
                        self.grad += n * self.data ** (n - 1) * out.grad
                    out._back = _b
                    return out

                def backward(self):
                    urut, terlihat = [], set()
                    def bangun(v):
                        if v not in terlihat:
                            terlihat.add(v)
                            for p in v._prev:
                                bangun(p)
                            urut.append(v)
                    bangun(self)
                    self.grad = 1.0
                    for v in reversed(urut):
                        v._back()

            xs = [0.0, 1.0, 2.0, 3.0]
            ys = [1.0, 3.0, 5.0, 7.0]
            w, b = Value(0.0), Value(0.0)
            for _ in range(500):
                loss = Value(0.0)
                for x, y in zip(xs, ys):
                    loss = loss + (w * x + b - y) ** 2
                loss = loss * (1 / len(xs))
                w.grad = 0.0
                b.grad = 0.0
                loss.backward()
                w.data -= 0.1 * w.grad
                b.data -= 0.1 * b.grad
            print(round(w.data, 3), round(b.data, 3), round(loss.data, 4))
            """,
            """
            2.0 1.0 0.0
            """,
            """
            Setelah 500 iterasi parameter mendekati dua dan satu, yaitu garis yang membentuk data, dan loss mendekati nol.
            """,
            filename="latih_neuron.py",
        ),
        T("""
        ## Memverifikasi autograd

        Setiap autograd harus diuji. Cara baku: hitung gradien dengan autograd dan bandingkan dengan turunan numerik pada beberapa fungsi, terutama yang memakai operasi berbeda dan variabel berulang. Bila selisihnya kecil, implementasimu benar. Bila tidak, curigai aturan lokal yang salah atau gradien yang tidak diakumulasi.

        Contoh di bawah memeriksa fungsi `tanh(x y + x)`, yang memakai `x` dua kali dan satu operasi nonlinear. Autograd harus menghasilkan turunan terhadap `x` dan `y` yang sama dengan turunan numerik sampai beberapa desimal.
        """),
        C(
            """
            import math

            class Value:
                def __init__(self, data, anak=()):
                    self.data = data
                    self.grad = 0.0
                    self._back = lambda: None
                    self._prev = set(anak)

                def __add__(self, o):
                    o = o if isinstance(o, Value) else Value(o)
                    out = Value(self.data + o.data, (self, o))
                    def _b():
                        self.grad += out.grad
                        o.grad += out.grad
                    out._back = _b
                    return out

                def __mul__(self, o):
                    o = o if isinstance(o, Value) else Value(o)
                    out = Value(self.data * o.data, (self, o))
                    def _b():
                        self.grad += o.data * out.grad
                        o.grad += self.data * out.grad
                    out._back = _b
                    return out

                def tanh(self):
                    t = math.tanh(self.data)
                    out = Value(t, (self,))
                    def _b():
                        self.grad += (1 - t * t) * out.grad
                    out._back = _b
                    return out

                def backward(self):
                    urut, terlihat = [], set()
                    def bangun(v):
                        if v not in terlihat:
                            terlihat.add(v)
                            for p in v._prev:
                                bangun(p)
                            urut.append(v)
                    bangun(self)
                    self.grad = 1.0
                    for v in reversed(urut):
                        v._back()

            def f(x, y):
                return math.tanh(x * y + x)

            x, y = Value(0.5), Value(1.5)
            out = (x * y + x).tanh()
            out.backward()
            eps = 1e-6
            gx = (f(0.5 + eps, 1.5) - f(0.5 - eps, 1.5)) / (2 * eps)
            gy = (f(0.5, 1.5 + eps) - f(0.5, 1.5 - eps)) / (2 * eps)
            print(round(out.data, 4))
            print(round(x.grad, 4), round(gx, 4))
            print(round(y.grad, 4), round(gy, 4))
            """,
            """
            0.8483
            0.701 0.701
            0.1402 0.1402
            """,
            """
            Gradien autograd terhadap `x` dan `y` cocok dengan turunan numerik, termasuk kontribusi dua jalur dari `x`.
            """,
            filename="gradient_check_autograd.py",
        ),
        T("""
        ## Dari mini ke pustaka nyata

        Autograd mini tadi bekerja pada skalar sehingga lambat. Pustaka nyata memakai tensor dan menjalankan operasi pada GPU, tetapi mekanismenya sama: simpul menyimpan fungsi mundur, graf dibangun saat pass maju, dan backward menelusuri urutan topologis. Pada PyTorch, `loss.backward()` melakukan persis hal ini dan `optimizer.zero_grad()` menol-kan gradien.

        Setelah membangun sendiri, pesan galat pustaka akan terasa lebih masuk akal. Misalnya galat bahwa gradien tidak bisa dihitung terhadap bilangan bulat, atau peringatan bahwa graf sudah dibebaskan, kini punya arti konkret bagimu.
        """),
        T("""
        ## Merangkum modul

        Kamu mulai dari aturan rantai satu variabel, melihat bahwa ia adalah pembukuan faktor penguatan, lalu menggambarnya sebagai graf komputasi. Kamu menurunkan backpropagation untuk lapisan linear, ReLU, dan jaringan dua lapis, dan akhirnya membangun mesin autograd sendiri yang melatih model sederhana.

        Dengan fondasi ini, modul berikutnya yaitu gradient descent dari nol akan terasa wajar. Tinggal menambah perulangan pelatihan dan memilih ukuran langkah yang tepat di atas mesin turunan yang sudah kamu pahami.
        """),
        E(
            "A3-04-3-ex1",
            "mudah",
            """
            Tulis fungsi `langkah_sgd(params, grads, lr)` yang mengembalikan list parameter baru `p - lr * g` dibulatkan 4 desimal. Hindari `-0.0`.
            """,
            """
            def langkah_sgd(params, grads, lr):
                # TODO: implementasikan
                pass
            """,
            """
            assert langkah_sgd([1, 2], [0.5, -1], 0.1) == [0.95, 2.1]
            assert langkah_sgd([0], [0], 1) == [0.0]
            assert langkah_sgd([5], [10], 0.5) == [0.0]
            assert langkah_sgd([1, 1, 1], [1, 2, 3], 0.1) == [0.9, 0.8, 0.7]
            """,
            "Kurangkan lr kali gradien dari tiap parameter.",
            """
            def langkah_sgd(params, grads, lr):
                return [round(p - lr * g, 4) + 0.0 for p, g in zip(params, grads)]
            """,
        ),
        E(
            "A3-04-3-ex2",
            "mudah",
            """
            Tulis fungsi `tanh_backward(z, g)` yang mengembalikan `g * (1 - tanh(z)^2)` dibulatkan 4 desimal. Hindari `-0.0`.
            """,
            """
            import math

            def tanh_backward(z, g):
                # TODO: implementasikan
                pass
            """,
            """
            assert tanh_backward(0, 1) == 1.0
            assert tanh_backward(1, 1) == 0.42
            assert tanh_backward(1, 2) == 0.8399
            assert tanh_backward(-1, 0.5) == 0.21
            assert tanh_backward(10, 1) == 0.0
            """,
            "Kalikan turunan datang dengan satu dikurangi kuadrat tanh.",
            """
            import math

            def tanh_backward(z, g):
                return round(g * (1 - math.tanh(z) ** 2), 4) + 0.0
            """,
        ),
        E(
            "A3-04-3-ex3",
            "sedang",
            """
            Tulis fungsi `urutan_topologis(graf)` yang menerima dict dari nama simpul ke list nama simpul masukannya, dan mengembalikan list nama semua simpul sehingga setiap simpul muncul setelah semua masukannya. Telusuri dengan DFS.
            """,
            """
            def urutan_topologis(graf):
                # TODO: implementasikan
                pass
            """,
            """
            g1 = {'L': ['d'], 'd': ['v', 't'], 'v': ['u', 'b'], 'u': ['w', 'x'], 'w': [], 'x': [], 'b': [], 't': []}
            r1 = urutan_topologis(g1)
            assert sorted(r1) == sorted(g1)
            assert all(r1.index(p) < r1.index(n) for n in g1 for p in g1[n])
            g2 = {'a': [], 'b': ['a'], 'c': ['a', 'b']}
            r2 = urutan_topologis(g2)
            assert r2 == ['a', 'b', 'c']
            g3 = {'x': []}
            assert urutan_topologis(g3) == ['x']
            g4 = {'z': ['y'], 'y': ['x'], 'x': []}
            assert urutan_topologis(g4) == ['x', 'y', 'z']
            """,
            "Kunjungi masukan dahulu secara rekursif lalu tambahkan simpul ke hasil.",
            """
            def urutan_topologis(graf):
                hasil, terlihat = [], set()
                def kunjungi(n):
                    if n in terlihat:
                        return
                    terlihat.add(n)
                    for p in graf[n]:
                        kunjungi(p)
                    hasil.append(n)
                for n in graf:
                    kunjungi(n)
                return hasil
            """,
        ),
        E(
            "A3-04-3-ex4",
            "menantang",
            """
            Tulis kelas `Value` autograd mini: konstruktor `Value(data)`, atribut `data` dan `grad` (awal `0.0`), operator `+`, `-`, `*`, `**` dengan pangkat bilangan biasa, dukungan bilangan biasa di kiri atau kanan untuk `+` dan `*`, metode `tanh()`, dan metode `backward()` dengan urutan topologis dan akumulasi gradien.
            """,
            """
            class Value:
                # TODO: implementasikan
                pass
            """,
            """
            a, b, c = Value(2.0), Value(-3.0), Value(10.0)
            d = a * b + c
            d.backward()
            assert (d.data, a.grad, b.grad, c.grad) == (4.0, -3.0, 2.0, 1.0)
            x, w, bb = Value(2.0), Value(3.0), Value(1.0)
            L = (w * x + bb - 5) ** 2
            L.backward()
            assert (L.data, w.grad, bb.grad, x.grad) == (4.0, 8.0, 4.0, 12.0)
            z = Value(3.0)
            q = z * z
            q.backward()
            assert z.grad == 6.0
            t = Value(0.5)
            y = t.tanh()
            y.backward()
            assert round(y.data, 4) == 0.4621 and round(t.grad, 4) == 0.7864
            r = Value(2.0)
            s = 3 + r * 4 - r
            s.backward()
            assert s.data == 9.0 and r.grad == 3.0
            """,
            "Tiap operasi membuat Value baru dengan fungsi _back yang menambahkan gradien ke masukan sesuai aturan lokal.",
            """
            import math

            class Value:
                def __init__(self, data, anak=()):
                    self.data = data
                    self.grad = 0.0
                    self._back = lambda: None
                    self._prev = set(anak)

                def __add__(self, o):
                    o = o if isinstance(o, Value) else Value(o)
                    out = Value(self.data + o.data, (self, o))
                    def _b():
                        self.grad += out.grad
                        o.grad += out.grad
                    out._back = _b
                    return out

                __radd__ = __add__

                def __mul__(self, o):
                    o = o if isinstance(o, Value) else Value(o)
                    out = Value(self.data * o.data, (self, o))
                    def _b():
                        self.grad += o.data * out.grad
                        o.grad += self.data * out.grad
                    out._back = _b
                    return out

                __rmul__ = __mul__

                def __neg__(self):
                    return self * -1

                def __sub__(self, o):
                    o = o if isinstance(o, Value) else Value(o)
                    return self + (-o)

                def __pow__(self, n):
                    out = Value(self.data ** n, (self,))
                    def _b():
                        self.grad += n * self.data ** (n - 1) * out.grad
                    out._back = _b
                    return out

                def tanh(self):
                    t = math.tanh(self.data)
                    out = Value(t, (self,))
                    def _b():
                        self.grad += (1 - t * t) * out.grad
                    out._back = _b
                    return out

                def backward(self):
                    urut, terlihat = [], set()
                    def bangun(v):
                        if v not in terlihat:
                            terlihat.add(v)
                            for p in v._prev:
                                bangun(p)
                            urut.append(v)
                    bangun(self)
                    self.grad = 1.0
                    for v in reversed(urut):
                        v._back()
            """,
        ),
    ],
    [
        M("Tidak menol-kan gradien sebelum backward berikutnya.", "Reset grad parameter tiap iterasi."),
        M("Memproses simpul tanpa urutan topologis.", "Telusuri DFS lalu balik daftarnya."),
        M("Mengganti gradien dengan = bukan +=.", "Akumulasikan agar variabel berulang benar."),
    ],
    [
        Q("Apa yang disimpan Value?", ["Hanya data", "Data, grad, masukan, dan fungsi mundur", "Hanya grad", "Hanya operasi"], 1, "Empat hal itu.", hint="Rekam."),
        Q("Mengapa urutan topologis?", ["Agar cepat", "Gradien lengkap sebelum disebarkan", "Agar rapi", "Agar acak"], 1, "Simpul keluaran harus selesai dulu.", hint="Bergantung."),
        Q("Gradien simpul keluaran awal?", ["0", "1", "Loss", "Tak terdefinisi"], 1, "dL/dL = 1.", hint="Mulai."),
        Q("Langkah latih setelah backward?", ["Hapus graf", "data -= lr * grad", "Tambah data", "Ganti loss"], 1, "Perbarui parameter.", hint="Turun."),
        Q("Cara menguji autograd?", ["Lihat kode saja", "Bandingkan dengan turunan numerik", "Tambah lapisan", "Tanpa uji"], 1, "Gradient check.", hint="Numerik."),
    ],
    [
        "Autograd merekam operasi dan menyebarkan gradien mundur dengan aturan lokal.",
        "Backward memakai urutan topologis dan akumulasi gradien.",
        "Pelatihan: maju, nol-kan gradien, mundur, perbarui.",
        "Uji autograd dengan turunan numerik.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perhitungan yang cukup jelas dalam teks.", "brief": []}

write_module(
    "A3",
    4,
    "Chain rule dan turunan komposisi",
    105,
    [
        "Menerapkan aturan rantai dan graf komputasi",
        "Menurunkan backpropagation untuk lapisan dan jaringan kecil",
        "Membangun dan memakai mini autograd",
    ],
    [l1, l2, l3],
    video,
    REF,
)
