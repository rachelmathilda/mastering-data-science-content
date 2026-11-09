import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

l1 = lesson(
    "A5-01-1",
    "Skala pengukuran: nominal, ordinal, interval, rasio",
    35,
    [
        "Membedakan empat skala pengukuran dan sifat-sifatnya",
        "Menentukan operasi matematis yang valid untuk tiap skala",
        "Memilih ukuran ringkasan yang sesuai skala",
        "Mengkodekan data ordinal dengan benar",
    ],
    [
        T("""
        ## Mengapa skala penting

        Sebelum menghitung rata-rata atau membuat grafik, tanyakan dulu: apa arti angka-angka ini? Nomor punggung pemain, peringkat lomba, suhu udara, dan tinggi badan semuanya berupa angka, tetapi hanya sebagian yang boleh dijumlahkan, dirata-ratakan, atau dibandingkan sebagai rasio. Memperlakukan semuanya sama menghasilkan kesimpulan yang tampak rapi tetapi tidak bermakna.

        **Skala pengukuran** adalah klasifikasi cara sebuah variabel diukur, dan menentukan operasi apa yang masuk akal. Klasifikasi empat tingkat dari Stevens, nominal, ordinal, interval, dan rasio, tetap menjadi kerangka paling umum dipakai dalam statistika dan sains data.
        """),
        T("""
        ## Nominal

        Skala **nominal** hanya memberi nama atau kategori tanpa urutan. Golongan darah, kota asal, warna favorit, dan jenis produk adalah contohnya. Satu-satunya hal yang bisa kita katakan adalah dua nilai sama atau berbeda. Bila kategori diberi angka, misalnya 1 untuk Jakarta dan 2 untuk Bandung, angka itu hanya label.

        Ringkasan yang masuk akal untuk nominal adalah hitungan, proporsi, dan modus. Rata-rata kode kota tidak bermakna. Grafik yang cocok adalah diagram batang frekuensi. Mengurutkan kategori nominal secara alfabet atau menurut frekuensi adalah keputusan penyajian, bukan sifat data.
        """),
        T("""
        ## Ordinal

        Skala **ordinal** memiliki urutan, tetapi jarak antar tingkat tidak jelas atau tidak sama. Tingkat pendidikan dari SD sampai S3, peringkat kepuasan satu sampai lima bintang, dan ukuran pakaian S, M, L, XL bersifat ordinal. Kita tahu S1 lebih tinggi dari SMA, tetapi tidak bisa mengatakan selisih S1 dan SMA sama dengan selisih SMA dan SMP.

        Untuk ordinal, median dan kuantil bermakna karena hanya butuh urutan. Rata-rata sering dipakai dalam praktik, misalnya rata-rata bintang ulasan, tetapi secara ketat mengasumsikan jarak sama antar tingkat. Sadari asumsi itu ketika melaporkannya.
        """),
        C(
            """
            from collections import Counter

            skala = {
                "golongan_darah": "nominal",
                "tingkat_pendidikan": "ordinal",
                "suhu_celsius": "interval",
                "tinggi_cm": "rasio",
                "jumlah_anak": "rasio",
                "kota": "nominal",
            }
            print(sorted(Counter(skala.values()).items()))
            """,
            """
            [('interval', 1), ('nominal', 2), ('ordinal', 1), ('rasio', 2)]
            """,
            """
            Setiap kolom dipetakan ke satu skala, dan hitungan memperlihatkan komposisi jenis variabel dalam dataset.
            """,
            filename="klasifikasi_skala.py",
        ),
        T("""
        ## Interval

        Skala **interval** memiliki urutan dan jarak yang bermakna, tetapi tidak punya nol mutlak. Suhu Celsius adalah contoh klasik: selisih 10 derajat berarti sama di mana pun pada skala, tetapi nol derajat bukan berarti tidak ada suhu. Tahun kalender dan skor tes standar juga interval.

        Karena nol bersifat sembarang, rasio tidak bermakna. Suhu 20 derajat Celsius tidak dua kali lebih panas dari 10 derajat. Rata-rata, simpangan baku, dan korelasi valid untuk interval, tetapi pernyataan seperti dua kali lebih tidak.
        """),
        C(
            """
            print(20 / 10, round(293.15 / 283.15, 4))
            """,
            """
            2.0 1.0353
            """,
            """
            Rasio naif dua puluh banding sepuluh adalah dua, tetapi pada skala Kelvin yang punya nol mutlak rasionya hanya sedikit di atas satu.
            """,
            filename="interval_vs_rasio.py",
        ),
        T("""
        ## Rasio

        Skala **rasio** memiliki urutan, jarak bermakna, dan nol mutlak yang berarti ketiadaan. Tinggi badan, berat, harga, jumlah pembelian, dan durasi adalah rasio. Karena nolnya nyata, pernyataan seperti dua kali lebih berat atau separuh harga memiliki arti.

        Semua operasi statistik valid pada rasio, termasuk rata-rata geometrik dan koefisien variasi. Perhatikan bahwa jumlah hitungan, seperti banyak anak, adalah rasio karena nol berarti tidak ada. Hierarki empat skala bersifat kumulatif: tiap tingkat mewarisi semua kemampuan tingkat sebelumnya ditambah satu sifat baru.
        """),
        C(
            """
            urutan = ["SD", "SMP", "SMA", "S1", "S2"]
            rank = {nama: i for i, nama in enumerate(urutan)}
            print(rank["S1"] > rank["SMA"])
            print(max(["SMP", "S1", "SMA"], key=rank.get))
            """,
            """
            True
            S1
            """,
            """
            Memberi peringkat pada kategori ordinal memungkinkan perbandingan dan pencarian nilai tertinggi tanpa mengasumsikan jarak yang sama.
            """,
            filename="ordinal_rank.py",
        ),
        T("""
        ## Memilih ringkasan sesuai skala

        Ringkasan mengikuti skala. Nominal memakai modus dan frekuensi. Ordinal menambah median dan kuantil. Interval menambah rata-rata dan simpangan baku. Rasio menambah rasio dan rata-rata geometrik. Memakai ringkasan dari tingkat lebih tinggi pada data yang lebih rendah adalah kesalahan paling umum, misalnya menghitung rata-rata kode produk.

        Dalam praktik batasnya kabur, dan banyak analis memperlakukan ordinal berpenyekat banyak, seperti skala satu sampai sepuluh, sebagai interval. Itu pilihan sadar yang perlu dijustifikasi, bukan kelalaian yang disembunyikan.
        """),
        C(
            """
            from collections import Counter

            golongan = ["A", "B", "A", "O", "A", "B"]
            print(Counter(golongan).most_common(1))
            """,
            """
            [('A', 3)]
            """,
            """
            Untuk data nominal ringkasan yang sah adalah modus, yaitu golongan darah A yang muncul tiga kali.
            """,
            filename="modus_nominal.py",
        ),
        K(
            "warn",
            """
            Angka tidak otomatis berarti skala numerik. Kode pos, nomor ID, dan nomor telepon berupa angka tetapi bersifat nominal. Jangan hitung rata-ratanya.
            """,
            title="Angka bukan berarti ukuran",
        ),
        T("""
        ## Dampak pada pemodelan

        Skala menentukan cara mengkodekan variabel untuk model. Variabel nominal dikodekan dengan one-hot agar model tidak mengira ada urutan. Variabel ordinal dapat dikodekan dengan peringkat bila urutan penting. Variabel interval dan rasio dipakai sebagai angka, sering setelah dinormalisasi. Salah mengkodekan nominal sebagai angka berurutan membuat model belajar hubungan palsu, misalnya menganggap kota nomor tiga di antara kota nomor dua dan empat.

        Karena itu mengenali skala adalah langkah pertama setiap proyek data, sebelum pembersihan dan visualisasi.
        """),
        E(
            "A5-01-1-ex1",
            "mudah",
            """
            Tulis fungsi `operasi_valid(skala)` yang mengembalikan list operasi yang sah. Nominal: `['hitung']`. Ordinal: `['hitung', 'urut']`. Interval: `['hitung', 'urut', 'selisih']`. Rasio: `['hitung', 'urut', 'selisih', 'rasio']`. Skala lain mengembalikan list kosong.
            """,
            """
            def operasi_valid(skala):
                # TODO: implementasikan
                pass
            """,
            """
            assert operasi_valid('nominal') == ['hitung']
            assert operasi_valid('ordinal') == ['hitung', 'urut']
            assert 'rasio' in operasi_valid('rasio')
            assert 'rasio' not in operasi_valid('interval')
            assert operasi_valid('lainnya') == []
            """,
            "Simpan pemetaan dari nama skala ke daftar operasinya.",
            """
            def operasi_valid(skala):
                peta = {
                    'nominal': ['hitung'],
                    'ordinal': ['hitung', 'urut'],
                    'interval': ['hitung', 'urut', 'selisih'],
                    'rasio': ['hitung', 'urut', 'selisih', 'rasio'],
                }
                return list(peta.get(skala, []))
            """,
        ),
        E(
            "A5-01-1-ex2",
            "sedang",
            """
            Tulis fungsi `tentukan_skala(berurutan, selisih_bermakna, nol_mutlak)` yang mengembalikan nama skala: `'nominal'` bila tidak berurutan, `'ordinal'` bila berurutan tetapi selisih tidak bermakna, `'interval'` bila selisih bermakna tetapi tanpa nol mutlak, dan `'rasio'` bila ada nol mutlak.
            """,
            """
            def tentukan_skala(berurutan, selisih_bermakna, nol_mutlak):
                # TODO: implementasikan
                pass
            """,
            """
            assert tentukan_skala(False, False, False) == 'nominal'
            assert tentukan_skala(True, False, False) == 'ordinal'
            assert tentukan_skala(True, True, False) == 'interval'
            assert tentukan_skala(True, True, True) == 'rasio'
            assert tentukan_skala(True, False, True) == 'ordinal'
            """,
            "Periksa sifat secara bertingkat dari urutan, selisih, lalu nol mutlak.",
            """
            def tentukan_skala(berurutan, selisih_bermakna, nol_mutlak):
                if not berurutan:
                    return 'nominal'
                if not selisih_bermakna:
                    return 'ordinal'
                if not nol_mutlak:
                    return 'interval'
                return 'rasio'
            """,
        ),
        E(
            "A5-01-1-ex3",
            "sedang",
            """
            Tulis fungsi `kode_ordinal(nilai, urutan)` yang mengubah list nilai ordinal menjadi list peringkat berbasis nol menurut list `urutan`. Nilai yang tidak ada dalam `urutan` diberi `-1`.
            """,
            """
            def kode_ordinal(nilai, urutan):
                # TODO: implementasikan
                pass
            """,
            """
            u = ['SD', 'SMP', 'SMA', 'S1', 'S2']
            assert kode_ordinal(['S1', 'SD'], u) == [3, 0]
            assert kode_ordinal([], u) == []
            assert kode_ordinal(['X'], u) == [-1]
            assert kode_ordinal(['S2', 'SMA', 'SMP'], u) == [4, 2, 1]
            """,
            "Buat kamus dari nilai ke indeksnya lalu pakai get dengan nilai bawaan minus satu.",
            """
            def kode_ordinal(nilai, urutan):
                rank = {n: i for i, n in enumerate(urutan)}
                return [rank.get(v, -1) for v in nilai]
            """,
        ),
        E(
            "A5-01-1-ex4",
            "menantang",
            """
            Tulis fungsi `modus(data)` yang mengembalikan list semua nilai dengan frekuensi tertinggi, terurut menaik. Untuk data kosong kembalikan list kosong.
            """,
            """
            from collections import Counter

            def modus(data):
                # TODO: implementasikan
                pass
            """,
            """
            assert modus(['A', 'B', 'A']) == ['A']
            assert modus([1, 2, 2, 3, 3]) == [2, 3]
            assert modus([5]) == [5]
            assert modus([]) == []
            """,
            "Hitung frekuensi lalu kumpulkan semua nilai yang frekuensinya sama dengan maksimum.",
            """
            from collections import Counter

            def modus(data):
                if not data:
                    return []
                c = Counter(data)
                m = max(c.values())
                return sorted(k for k, v in c.items() if v == m)
            """,
        ),
    ],
    [
        M("Menghitung rata-rata kode pos atau ID.", "Itu nominal, pakai modus dan frekuensi."),
        M("Menyebut 20 derajat dua kali lebih panas dari 10 derajat.", "Interval tidak punya nol mutlak."),
        M("Mengkodekan nominal sebagai angka berurutan untuk model.", "Gunakan one-hot."),
    ],
    [
        Q("Golongan darah berskala?", ["Nominal", "Ordinal", "Interval", "Rasio"], 0, "Kategori tanpa urutan.", hint="Tanpa urutan."),
        Q("Tingkat pendidikan berskala?", ["Nominal", "Ordinal", "Interval", "Rasio"], 1, "Berurutan, jarak tak sama.", hint="Urutan."),
        Q("Suhu Celsius berskala?", ["Ordinal", "Interval", "Rasio", "Nominal"], 1, "Tanpa nol mutlak.", hint="Nol sembarang."),
        Q("Tinggi badan berskala?", ["Interval", "Rasio", "Ordinal", "Nominal"], 1, "Nol mutlak.", hint="Nol berarti tidak ada."),
        Q("Ringkasan sah untuk nominal?", ["Rata-rata", "Modus", "Median", "Varians"], 1, "Hitungan dan modus.", hint="Frekuensi."),
    ],
    [
        "Skala menentukan operasi dan ringkasan yang bermakna.",
        "Nominal tanpa urutan, ordinal berurutan, interval berjarak, rasio bernol mutlak.",
        "Angka tidak otomatis berarti ukuran numerik.",
        "Pengkodean model mengikuti skala variabel.",
    ],
    [],
)

l2 = lesson(
    "A5-01-2",
    "Tipe data dan representasinya",
    35,
    [
        "Membedakan data numerik diskrit dan kontinu, kategorikal, teks, dan waktu",
        "Menebak tipe nilai dari representasi teks",
        "Mendiskretisasi variabel kontinu menjadi kategori",
        "Mengkodekan kategori dengan one-hot dan menghitung selisih tanggal",
    ],
    [
        T("""
        ## Dari skala ke tipe

        Skala pengukuran menjelaskan makna variabel, sedangkan **tipe data** menjelaskan bagaimana nilai disimpan di komputer. Keduanya berhubungan tetapi tidak identik. Kolom bertipe integer bisa bersifat nominal seperti kode pos, dan kolom bertipe teks bisa bersifat ordinal seperti tingkat kepuasan baik, cukup, buruk.

        Pemahaman keduanya penting. Skala memberi tahu analisis apa yang bermakna, sedangkan tipe memberi tahu operasi apa yang dimungkinkan dan efisien oleh perangkat lunak. Ketidakcocokan antara keduanya adalah sumber kesalahan yang halus tetapi sangat umum.
        """),
        T("""
        ## Numerik: diskrit dan kontinu

        Data numerik **diskrit** hanya mengambil nilai terhitung, biasanya bilangan bulat: jumlah pesanan, jumlah anak, jumlah klik. Data numerik **kontinu** dapat mengambil sembarang nilai pada rentang: tinggi, berat, waktu respons. Perbedaannya menentukan model yang cocok, seperti Poisson untuk hitungan dan normal untuk besaran kontinu.

        Dalam praktik semua pengukuran kontinu dibulatkan, sehingga tampak diskrit. Pembedaan konseptual tetap berguna: tanyakan apakah antara dua nilai yang bersebelahan masih mungkin ada nilai lain yang bermakna.
        """),
        T("""
        ## Kategorikal, teks, dan waktu

        Data **kategorikal** membagi observasi ke dalam kelompok, termasuk biner dengan dua kategori seperti ya atau tidak. Data **teks** bebas berisi kalimat atau dokumen dan butuh pemrosesan khusus sebelum dianalisis. Data **waktu** mencatat kapan sesuatu terjadi dan memiliki sifat unik seperti urutan, musiman, dan zona waktu.

        Tanggal sering tersimpan sebagai teks mentah yang tidak bisa dihitung selisihnya. Mengubahnya menjadi tipe tanggal sungguhan adalah langkah pembersihan yang hampir selalu diperlukan, dan membuka operasi seperti selisih hari dan hari dalam pekan.
        """),
        C(
            """
            from datetime import date

            def tebak_tipe(s):
                try:
                    int(s)
                    return "int"
                except ValueError:
                    pass
                try:
                    float(s)
                    return "float"
                except ValueError:
                    pass
                if s.lower() in ("true", "false"):
                    return "bool"
                try:
                    date.fromisoformat(s)
                    return "tanggal"
                except ValueError:
                    return "teks"

            print([tebak_tipe(v) for v in ["12", "3.5", "true", "2026-11-07", "halo"]])
            """,
            """
            ['int', 'float', 'bool', 'tanggal', 'teks']
            """,
            """
            Setiap string dicoba dikonversi dari tipe paling ketat ke paling longgar sampai satu berhasil, dan teks adalah pilihan terakhir.
            """,
            filename="tebak_tipe.py",
        ),
        T("""
        ## Bekerja dengan tanggal

        Setelah tanggal diurai menjadi objek `date`, kita bisa mengurangkannya untuk mendapat selisih hari, mengambil hari dalam pekan, atau mengelompokkan per bulan. Python menyediakan modul `datetime` untuk ini. Selisih dua objek tanggal berupa `timedelta` dengan atribut `days`.

        Hati-hati dengan zona waktu dan format tanggal yang ambigu. Tulisan 03/04/2026 bisa berarti tiga April atau empat Maret. Format ISO tahun-bulan-hari tidak ambigu dan dapat diurutkan secara alfabet, sehingga menjadi pilihan standar untuk penyimpanan.
        """),
        C(
            """
            from datetime import date

            a = date(2026, 1, 1)
            b = date(2026, 11, 7)
            print((b - a).days, b.weekday())
            """,
            """
            310 5
            """,
            """
            Tanggal tujuh November berjarak tiga ratus sepuluh hari dari awal tahun dan jatuh pada hari Sabtu yang bernomor lima bila Senin dihitung nol.
            """,
            filename="tanggal.py",
        ),
        T("""
        ## Diskretisasi

        Kadang kita mengubah variabel kontinu menjadi kategori dengan memotongnya pada batas tertentu, misalnya umur menjadi anak, dewasa, dan lansia. Ini disebut **diskretisasi** atau binning. Hasilnya ordinal karena kategori masih berurutan. Manfaatnya penyederhanaan dan kemudahan interpretasi, biayanya hilangnya informasi di dalam tiap kelompok.

        Pilih batas berdasarkan pengetahuan domain bila ada, seperti kelompok usia resmi, atau berdasarkan kuantil bila ingin kelompok berukuran sama. Hindari diskretisasi tanpa alasan karena model modern umumnya lebih baik menggunakan nilai kontinu aslinya.
        """),
        C(
            """
            umur = [5, 17, 25, 40, 65, 80]
            label = ["anak" if u < 18 else "dewasa" if u < 60 else "lansia" for u in umur]
            print(label)
            """,
            """
            ['anak', 'anak', 'dewasa', 'dewasa', 'lansia', 'lansia']
            """,
            """
            Batas delapan belas dan enam puluh membagi umur menjadi tiga kelompok berurutan.
            """,
            filename="diskretisasi.py",
        ),
        T("""
        ## One-hot encoding

        Model numerik membutuhkan angka, tetapi mengganti kategori nominal dengan 1, 2, 3 menciptakan urutan palsu. **One-hot encoding** membuat satu kolom biner per kategori: nilainya satu pada kolom kategori yang sesuai dan nol pada sisanya. Tidak ada urutan atau jarak yang diasumsikan.

        Konsekuensinya jumlah kolom bertambah sebesar banyaknya kategori. Variabel dengan ribuan kategori, seperti kode pos, menghasilkan ribuan kolom, sehingga teknik lain seperti pengkodean target atau embedding lebih cocok.
        """),
        C(
            """
            kategori = sorted(["merah", "hijau", "biru"])

            def one_hot(nilai):
                return [1 if k == nilai else 0 for k in kategori]

            print(kategori)
            print(one_hot("hijau"), one_hot("merah"))
            """,
            """
            ['biru', 'hijau', 'merah']
            [0, 1, 0] [0, 0, 1]
            """,
            """
            Kategori diurutkan tetap lalu tiap nilai menjadi vektor dengan satu angka satu pada posisi kategorinya.
            """,
            filename="one_hot.py",
        ),
        K(
            "tip",
            """
            Simpan daftar kategori dari data latih dan pakai daftar yang sama saat memproses data baru. Kategori yang belum pernah terlihat dikodekan sebagai semua nol.
            """,
            title="Konsistensi pengkodean",
        ),
        T("""
        ## Tipe data di pandas dan Python

        Di Python dasar kita bertemu int, float, str, bool, dan objek tanggal. Pustaka pandas menambahkan tipe untuk kategori dan waktu, dan kolom bertipe object biasanya berarti campuran atau teks. Kolom angka yang terbaca sebagai object hampir selalu menandakan ada sel bermasalah, seperti teks tidak numerik, yang memaksa seluruh kolom menjadi teks.

        Biasakan memeriksa tipe kolom segera setelah memuat data, lalu mengonversinya dengan sengaja. Tipe kategori menghemat memori untuk kolom dengan sedikit nilai unik dan membuat maksud analisis lebih jelas bagi pembaca kode.
        """),
        T("""
        ## Data terstruktur dan tak terstruktur

        Data terstruktur tersusun rapi dalam baris dan kolom, seperti tabel basis data atau berkas CSV. Data semi-terstruktur seperti JSON memiliki bidang bernama tetapi bentuknya bisa berbeda antar rekaman. Data tak terstruktur seperti teks bebas, gambar, dan audio tidak memiliki skema tetap dan harus diubah menjadi fitur numerik sebelum dianalisis dengan alat statistik klasik.

        Kursus ini berfokus pada data terstruktur, tetapi gagasan skala dan tipe berlaku sama pada fitur yang diekstrak dari data tak terstruktur.
        """),
        E(
            "A5-01-2-ex1",
            "mudah",
            """
            Tulis fungsi `tebak_tipe(s)` yang mengembalikan `'int'`, `'float'`, `'bool'`, `'tanggal'`, atau `'teks'` untuk string `s`. Coba berurutan int, float, bool (`true` atau `false` tanpa memandang huruf besar), tanggal ISO, lalu teks.
            """,
            """
            from datetime import date

            def tebak_tipe(s):
                # TODO: implementasikan
                pass
            """,
            """
            assert tebak_tipe('12') == 'int'
            assert tebak_tipe('-3') == 'int'
            assert tebak_tipe('3.5') == 'float'
            assert tebak_tipe('1e3') == 'float'
            assert tebak_tipe('True') == 'bool'
            assert tebak_tipe('false') == 'bool'
            assert tebak_tipe('2026-11-07') == 'tanggal'
            assert tebak_tipe('halo') == 'teks'
            assert tebak_tipe('') == 'teks'
            """,
            "Gunakan blok try dan except ValueError untuk tiap percobaan konversi.",
            """
            from datetime import date

            def tebak_tipe(s):
                try:
                    int(s)
                    return 'int'
                except ValueError:
                    pass
                try:
                    float(s)
                    return 'float'
                except ValueError:
                    pass
                if s.lower() in ('true', 'false'):
                    return 'bool'
                try:
                    date.fromisoformat(s)
                    return 'tanggal'
                except ValueError:
                    return 'teks'
            """,
        ),
        E(
            "A5-01-2-ex2",
            "sedang",
            """
            Tulis fungsi `diskretisasi(nilai, batas, label)` yang memberi tiap nilai label berdasarkan `batas` menaik: nilai kurang dari `batas[i]` mendapat `label[i]` pertama yang memenuhi, dan nilai yang lebih besar atau sama dengan batas terakhir mendapat `label[-1]`. Panjang `label` sama dengan panjang `batas` ditambah satu.
            """,
            """
            def diskretisasi(nilai, batas, label):
                # TODO: implementasikan
                pass
            """,
            """
            assert diskretisasi([5, 17, 25, 40, 65, 80], [18, 60], ['anak', 'dewasa', 'lansia']) == ['anak', 'anak', 'dewasa', 'dewasa', 'lansia', 'lansia']
            assert diskretisasi([18, 60], [18, 60], ['anak', 'dewasa', 'lansia']) == ['dewasa', 'lansia']
            assert diskretisasi([], [18, 60], ['anak', 'dewasa', 'lansia']) == []
            assert diskretisasi([1, 2], [], ['semua']) == ['semua', 'semua']
            """,
            "Cari batas pertama yang lebih besar dari nilai dan pakai labelnya, atau label terakhir bila tidak ada.",
            """
            def diskretisasi(nilai, batas, label):
                hasil = []
                for v in nilai:
                    for i, b in enumerate(batas):
                        if v < b:
                            hasil.append(label[i])
                            break
                    else:
                        hasil.append(label[-1])
                return hasil
            """,
        ),
        E(
            "A5-01-2-ex3",
            "sedang",
            """
            Tulis fungsi `one_hot(nilai, kategori)` yang mengembalikan list 0 dan 1 menurut `kategori` yang diurutkan alfabetis. Nilai yang tidak dikenal menghasilkan semua nol.
            """,
            """
            def one_hot(nilai, kategori):
                # TODO: implementasikan
                pass
            """,
            """
            k = ['merah', 'hijau', 'biru']
            assert one_hot('hijau', k) == [0, 1, 0]
            assert one_hot('merah', k) == [0, 0, 1]
            assert one_hot('ungu', k) == [0, 0, 0]
            assert one_hot('a', ['a']) == [1]
            """,
            "Urutkan kategori lalu beri satu pada posisi yang sama dengan nilai.",
            """
            def one_hot(nilai, kategori):
                return [1 if c == nilai else 0 for c in sorted(kategori)]
            """,
        ),
        E(
            "A5-01-2-ex4",
            "menantang",
            """
            Tulis fungsi `selisih_hari(a, b)` yang menerima dua string tanggal ISO `YYYY-MM-DD` dan mengembalikan banyak hari dari `a` ke `b` (negatif bila `b` lebih awal). Pakai `datetime.date`.
            """,
            """
            from datetime import date

            def selisih_hari(a, b):
                # TODO: implementasikan
                pass
            """,
            """
            assert selisih_hari('2026-01-01', '2026-11-07') == 310
            assert selisih_hari('2026-11-07', '2026-11-07') == 0
            assert selisih_hari('2026-11-07', '2026-01-01') == -310
            assert selisih_hari('2024-02-28', '2024-03-01') == 2
            """,
            "Urai kedua string dengan date.fromisoformat lalu kurangkan.",
            """
            from datetime import date

            def selisih_hari(a, b):
                return (date.fromisoformat(b) - date.fromisoformat(a)).days
            """,
        ),
    ],
    [
        M("Menganggap tipe integer berarti skala numerik.", "Kode pos integer tetap nominal."),
        M("Menyimpan tanggal sebagai teks mentah.", "Urai menjadi tipe tanggal."),
        M("Mengkodekan nominal dengan angka berurutan.", "Pakai one-hot."),
    ],
    [
        Q("Jumlah klik adalah data?", ["Kontinu", "Diskrit", "Teks", "Waktu"], 1, "Bilangan bulat terhitung.", hint="Hitungan."),
        Q("Waktu respons adalah data?", ["Diskrit", "Kontinu", "Nominal", "Biner"], 1, "Sembarang nilai pada rentang.", hint="Antara dua nilai."),
        Q("One-hot dipakai untuk?", ["Nominal", "Rasio", "Waktu", "Interval"], 0, "Tanpa urutan palsu.", hint="Kategori."),
        Q("Diskretisasi umur menghasilkan?", ["Nominal", "Ordinal", "Rasio", "Kontinu"], 1, "Kelompok berurutan.", hint="Urutan."),
        Q("Format tanggal tidak ambigu?", ["DD/MM/YYYY", "MM/DD/YYYY", "ISO YYYY-MM-DD", "Teks bebas"], 2, "Dapat diurutkan.", hint="Tahun dulu."),
    ],
    [
        "Skala adalah makna variabel, tipe adalah cara penyimpanan.",
        "Diskrit terhitung, kontinu di sembarang titik rentang.",
        "Tanggal sebaiknya berupa tipe tanggal dan format ISO.",
        "One-hot mengkodekan nominal tanpa urutan palsu.",
    ],
    [],
)

l3 = lesson(
    "A5-01-3",
    "Memeriksa kualitas data",
    35,
    [
        "Menghitung nilai hilang per kolom",
        "Menyeragamkan kategori teks dan menghapus duplikat",
        "Memeriksa rentang nilai yang tidak valid",
        "Mendeteksi pencilan dengan aturan IQR",
    ],
    [
        T("""
        ## Data kotor itu normal

        Data nyata hampir selalu kotor: ada sel kosong, baris ganda, nilai mustahil, ejaan beragam untuk kategori yang sama, dan pencilan akibat salah ketik atau kejadian langka. Analis berpengalaman menghabiskan sebagian besar waktunya membersihkan data, dan keputusan pembersihan sering lebih memengaruhi hasil daripada pilihan model.

        Pelajaran ini memberi daftar periksa dasar yang dapat dijalankan sebelum analisis apa pun. Tujuannya bukan membuat data sempurna, melainkan mengetahui masalahnya dan memutuskan secara sadar apa yang dilakukan dengan tiap masalah.
        """),
        T("""
        ## Nilai hilang

        Langkah pertama adalah menghitung berapa banyak nilai hilang di tiap kolom. Hilang bisa muncul sebagai sel kosong, string kosong, `None`, atau kode khusus seperti -999 atau tidak diketahui. Memeriksa semua bentuk ini penting karena kode khusus yang dibiarkan akan dianggap nilai asli dan merusak rata-rata.

        Mengapa data hilang sama pentingnya dengan berapa banyak. Bila hilang acak, menghapus baris relatif aman. Bila hilang bergantung pada nilai itu sendiri, misalnya orang berpenghasilan tinggi enggan mengisi pendapatan, menghapusnya membuat bias.
        """),
        C(
            """
            rows = [
                {"nama": "A", "umur": 20},
                {"nama": "B", "umur": None},
                {"nama": "C", "umur": None},
            ]
            kolom = {k for r in rows for k in r}
            hilang = {k: sum(1 for r in rows if r.get(k) in (None, "")) for k in sorted(kolom)}
            print(hilang)
            """,
            """
            {'nama': 0, 'umur': 2}
            """,
            """
            Dua dari tiga baris tidak memiliki umur, sedangkan nama lengkap.
            """,
            filename="nilai_hilang.py",
        ),
        T("""
        ## Konsistensi kategori

        Kolom kategorikal sering memuat varian ejaan yang sebenarnya sama: Jakarta, jakarta, JAKARTA, dan Jakarta dengan spasi di ujung. Bagi komputer ini kategori berbeda sehingga hitungan terpecah dan hasil analisis keliru. Normalisasi teks, yaitu membuang spasi di tepi, menyatukan huruf besar kecil, dan merapikan spasi ganda, menyelesaikan sebagian besar masalah ini.

        Untuk variasi yang lebih rumit seperti singkatan atau salah ketik, diperlukan pemetaan manual atau pencocokan kemiripan teks. Selalu periksa daftar nilai unik tiap kolom kategorikal sebelum menganalisis.
        """),
        C(
            """
            from collections import Counter

            kota = ["Jakarta", " jakarta", "JAKARTA", "Bandung"]
            bersih = [" ".join(k.split()).title() for k in kota]
            print(sorted(Counter(bersih).items()))
            """,
            """
            [('Bandung', 1), ('Jakarta', 3)]
            """,
            """
            Setelah dirapikan tiga ejaan menjadi satu kategori Jakarta dengan tiga kemunculan.
            """,
            filename="normalisasi_kategori.py",
        ),
        T("""
        ## Duplikat

        Baris ganda muncul dari penggabungan data, pengiriman ulang formulir, atau kesalahan ekspor. Duplikat mengembungkan hitungan dan memberi bobot ganda pada pengamatan tertentu. Namun tidak semua baris yang mirip adalah duplikat: dua transaksi identik pada waktu berbeda mungkin sah.

        Tentukan kunci yang mendefinisikan satu entitas unik, misalnya ID pelanggan ditambah tanggal, lalu hapus duplikat berdasarkan kunci itu sambil mempertahankan urutan. `dict.fromkeys` adalah cara ringkas di Python untuk menghapus duplikat dengan urutan terjaga.
        """),
        C(
            """
            data = [1, 2, 2, 3, 1]
            print(list(dict.fromkeys(data)), len(data) - len(set(data)))
            """,
            """
            [1, 2, 3] 2
            """,
            """
            Menghapus duplikat dengan urutan terjaga menghasilkan satu, dua, tiga, dan ada dua entri yang berlebih.
            """,
            filename="duplikat.py",
        ),
        T("""
        ## Rentang dan logika

        Nilai harus masuk akal secara domain. Umur negatif atau di atas seratus dua puluh, harga nol pada produk berbayar, tanggal lahir di masa depan, dan tanggal selesai sebelum tanggal mulai adalah tanda kesalahan. Tulis aturan validasi eksplisit sebagai kode sehingga dapat dijalankan ulang tiap data baru datang.

        Aturan lintas kolom juga penting: jumlah anggota keluarga tidak boleh lebih kecil dari jumlah anak. Pemeriksaan semacam ini menangkap kesalahan yang tidak terlihat pada satu kolom saja.
        """),
        C(
            """
            umur = [25, -3, 130, 40, 200]
            print([i for i, u in enumerate(umur) if not 0 <= u <= 120])
            """,
            """
            [1, 2, 4]
            """,
            """
            Posisi satu, dua, dan empat memiliki umur di luar rentang yang masuk akal.
            """,
            filename="validasi_rentang.py",
        ),
        T("""
        ## Pencilan dengan aturan IQR

        Pencilan adalah nilai yang jauh dari mayoritas data. Aturan IQR sederhana menandainya: hitung kuartil pertama `Q1` dan ketiga `Q3`, rentang antarkuartil `IQR = Q3 - Q1`, lalu tandai nilai di bawah `Q1 - 1,5 IQR` atau di atas `Q3 + 1,5 IQR`. Aturan ini tidak mengasumsikan distribusi normal.

        Menandai bukan berarti menghapus. Pencilan bisa kesalahan ketik yang perlu dikoreksi, atau kejadian nyata yang justru paling informatif, misalnya transaksi penipuan. Selidiki dulu sebelum memutuskan.
        """),
        C(
            """
            import statistics

            data = [10, 12, 11, 13, 12, 11, 95]
            q1, _, q3 = statistics.quantiles(data, n=4, method="inclusive")
            iqr = q3 - q1
            luar = [x for x in data if x < q1 - 1.5 * iqr or x > q3 + 1.5 * iqr]
            print(q1, q3, luar)
            """,
            """
            11.0 12.5 [95]
            """,
            """
            Kuartil pertama sebelas dan ketiga dua belas koma lima menghasilkan batas atas empat belas koma tujuh lima, sehingga sembilan puluh lima ditandai sebagai pencilan.
            """,
            filename="iqr.py",
        ),
        K(
            "tip",
            """
            Simpan kode pembersihan sebagai skrip yang bisa dijalankan ulang dan catat tiap keputusan. Pembersihan manual di spreadsheet tidak dapat direproduksi dan mudah menimbulkan kesalahan tak terlihat.
            """,
            title="Reproduksibilitas",
        ),
        T("""
        ## Daftar periksa sebelum analisis

        Susun kebiasaan pemeriksaan yang sama untuk tiap dataset. Lihat bentuk data, yaitu jumlah baris dan kolom. Periksa tipe tiap kolom. Hitung nilai hilang. Daftar nilai unik kolom kategorikal. Ringkas kolom numerik dengan minimum, maksimum, dan kuartil. Cari duplikat berdasarkan kunci. Cek aturan domain dan lintas kolom.

        Mengerjakannya sebagai fungsi yang dapat dijalankan pada dataset mana pun menghemat waktu dan mengurangi kemungkinan terlewat. Hasilnya adalah laporan kualitas data singkat yang berguna untuk dibagikan kepada pemilik data.
        """),
        T("""
        ## Mengomunikasikan keputusan pembersihan

        Setiap keputusan pembersihan adalah asumsi yang memengaruhi hasil. Menghapus baris dengan nilai hilang mengubah populasi yang dianalisis. Mengisi nilai hilang dengan rata-rata mengecilkan variasi. Menghapus pencilan mengubah rata-rata dan sebaran. Catat tiap keputusan, alasannya, dan berapa baris terdampak, lalu sertakan dalam laporan.

        Pembaca yang tahu apa yang kamu lakukan dapat menilai apakah kesimpulanmu layak dipercaya. Pembersihan yang disembunyikan merusak kepercayaan sekalipun hasilnya kebetulan benar.
        """),
        E(
            "A5-01-3-ex1",
            "mudah",
            """
            Tulis fungsi `hitung_hilang(rows)` yang menerima list dict dan mengembalikan dict kolom ke banyaknya nilai hilang, yaitu `None` atau string kosong atau kunci yang tidak ada pada baris itu. Kolom diambil dari gabungan semua kunci.
            """,
            """
            def hitung_hilang(rows):
                # TODO: implementasikan
                pass
            """,
            """
            rows = [{'nama': 'A', 'umur': 20}, {'nama': 'B', 'umur': None}, {'nama': 'C', 'umur': None}]
            assert hitung_hilang(rows) == {'nama': 0, 'umur': 2}
            assert hitung_hilang([]) == {}
            assert hitung_hilang([{'a': ''}, {'a': 'x'}]) == {'a': 1}
            assert hitung_hilang([{'a': 1}, {'b': 2}]) == {'a': 1, 'b': 1}
            """,
            "Kumpulkan semua kunci lalu hitung baris yang nilainya None, kosong, atau tidak ada.",
            """
            def hitung_hilang(rows):
                kolom = set()
                for r in rows:
                    kolom |= set(r)
                return {k: sum(1 for r in rows if r.get(k) in (None, '')) for k in kolom}
            """,
        ),
        E(
            "A5-01-3-ex2",
            "sedang",
            """
            Tulis fungsi `normalisasi_teks(s)` yang membuang spasi di tepi, merapikan spasi ganda menjadi satu, dan mengubah ke huruf kecil.
            """,
            """
            def normalisasi_teks(s):
                # TODO: implementasikan
                pass
            """,
            """
            assert normalisasi_teks('  Jakarta  Selatan ') == 'jakarta selatan'
            assert normalisasi_teks('BANDUNG') == 'bandung'
            assert normalisasi_teks('') == ''
            assert normalisasi_teks('a   b   c') == 'a b c'
            """,
            "Pecah dengan split lalu gabungkan dengan satu spasi dan ubah ke huruf kecil.",
            """
            def normalisasi_teks(s):
                return ' '.join(s.split()).lower()
            """,
        ),
        E(
            "A5-01-3-ex3",
            "sedang",
            """
            Tulis fungsi `hapus_duplikat(data)` yang menghapus elemen ganda dengan mempertahankan urutan kemunculan pertama.
            """,
            """
            def hapus_duplikat(data):
                # TODO: implementasikan
                pass
            """,
            """
            assert hapus_duplikat([1, 2, 2, 3, 1]) == [1, 2, 3]
            assert hapus_duplikat([]) == []
            assert hapus_duplikat(['a', 'A']) == ['a', 'A']
            assert hapus_duplikat([3, 3, 3]) == [3]
            """,
            "Pakai dict.fromkeys agar urutan terjaga.",
            """
            def hapus_duplikat(data):
                return list(dict.fromkeys(data))
            """,
        ),
        E(
            "A5-01-3-ex4",
            "menantang",
            """
            Tulis fungsi `deteksi_outlier_iqr(data, k=1.5)` yang mengembalikan list nilai pencilan menurut aturan IQR (di bawah `Q1 - k * IQR` atau di atas `Q3 + k * IQR`) dengan urutan asli data. Hitung kuartil dengan `statistics.quantiles(data, n=4, method='inclusive')`.
            """,
            """
            import statistics

            def deteksi_outlier_iqr(data, k=1.5):
                # TODO: implementasikan
                pass
            """,
            """
            assert deteksi_outlier_iqr([10, 12, 11, 13, 12, 11, 95]) == [95]
            assert deteksi_outlier_iqr([1, 2, 3, 4, 5]) == []
            assert deteksi_outlier_iqr([-50, 10, 11, 12, 13, 14, 15]) == [-50]
            assert deteksi_outlier_iqr([1, 2, 3, 4, 100], 3) == [100]
            """,
            "Hitung Q1 dan Q3 lalu saring nilai di luar batas bawah dan atas.",
            """
            import statistics

            def deteksi_outlier_iqr(data, k=1.5):
                q1, _, q3 = statistics.quantiles(data, n=4, method='inclusive')
                iqr = q3 - q1
                return [x for x in data if x < q1 - k * iqr or x > q3 + k * iqr]
            """,
        ),
    ],
    [
        M("Membiarkan kode khusus seperti -999 sebagai angka asli.", "Ganti dengan nilai hilang sebelum menghitung."),
        M("Membersihkan manual tanpa catatan.", "Tulis kode pembersihan yang dapat diulang."),
        M("Menghapus semua pencilan otomatis.", "Selidiki dulu, bisa jadi informatif."),
    ],
    [
        Q("Langkah pertama kualitas data?", ["Membuat model", "Menghitung nilai hilang dan memeriksa data", "Menghapus kolom", "Normalisasi"], 1, "Ketahui masalahnya dulu.", hint="Periksa."),
        Q("Jakarta dan jakarta?", ["Sama otomatis", "Kategori berbeda bagi komputer", "Selalu salah", "Tidak penting"], 1, "Perlu normalisasi.", hint="Huruf besar kecil."),
        Q("Duplikat sah bila?", ["Selalu salah", "Transaksi identik pada waktu berbeda", "Baris kosong", "Kolom sama"], 1, "Tentukan kunci unik.", hint="Kunci."),
        Q("Aturan IQR menandai di luar?", ["Q1-1,5IQR dan Q3+1,5IQR", "Rata-rata ± 1", "Median ± 2", "Min dan maks"], 0, "Tanpa asumsi normal.", hint="Kuartil."),
        Q("Pencilan sebaiknya?", ["Langsung dihapus", "Diselidiki", "Diabaikan", "Dikuadratkan"], 1, "Bisa informatif.", hint="Selidiki."),
    ],
    [
        "Hitung nilai hilang dalam semua bentuknya.",
        "Normalisasi teks dan hapus duplikat berdasarkan kunci.",
        "Validasi rentang dengan aturan eksplisit.",
        "Tandai pencilan dengan IQR lalu selidiki.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perhitungan yang cukup jelas dalam teks.", "brief": []}

write_module(
    "A5",
    1,
    "Jenis data dan skala pengukuran",
    105,
    [
        "Membedakan skala pengukuran dan tipe data",
        "Mengkodekan dan mendiskretisasi variabel dengan benar",
        "Memeriksa dan membersihkan kualitas data dasar",
    ],
    [l1, l2, l3],
    video,
    REF,
)
