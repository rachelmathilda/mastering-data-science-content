import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

import textwrap

DF = textwrap.indent("""
import pandas as pd

df = pd.DataFrame({
    'kota': ['A', 'A', 'B', 'B', 'B', 'C'],
    'gaji': [5, 6, 5, 7, 6, 100],
    'usia': [25, 30, 28, 35, 40, 50],
})
""", '            ')

l1 = lesson(
    "A5-06-1",
    "Meringkas kolom dengan describe dan value_counts",
    35,
    [
        "Membuat DataFrame kecil dan meringkas kolom numerik dengan describe",
        "Menghitung frekuensi dan proporsi kategori dengan value_counts",
        "Menghitung kuantil dengan quantile",
        "Menangani nilai hilang sebelum meringkas",
    ],
    [
        T("""
        ## Dari rumus ke pustaka

        Sepanjang modul ini kita menghitung ukuran ringkasan dengan tangan agar memahami maknanya. Dalam praktik, kita memakai **pandas**, pustaka tabel data Python yang sudah mengemas semuanya dalam satu baris. Memahami rumus tetap penting: kamu perlu tahu apa yang dihitung pandas, termasuk default seperti pembagi `n - 1` pada simpangan baku.

        Pelajaran ini membahas ringkasan satu kolom. Pelajaran berikutnya membahas ringkasan per kelompok, dan pelajaran terakhir membahas tabel silang, korelasi, dan pengelompokan nilai numerik ke dalam kategori.
        """),
        T("""
        ## DataFrame dan Series

        **DataFrame** adalah tabel dengan kolom bernama, dan setiap kolomnya adalah **Series**, deretan nilai berindeks. Kita membuat DataFrame dari dictionary yang kuncinya nama kolom dan nilainya list. Dataset kecil di bawah berisi kota, gaji dalam juta rupiah, dan usia enam orang, termasuk satu gaji pencilan seratus juta.

        Semua contoh di pelajaran ini memakai tabel kecil ini agar hasilnya bisa diperiksa dengan tangan. Pada data nyata, DataFrame biasanya dibaca dari berkas CSV atau basis data, tetapi cara meringkasnya sama persis.
        """),
        C(
            DF + """
            print(df.shape)
            print(df.columns.tolist())
            print(df['gaji'].tolist())
            """,
            """
            (6, 3)
            ['kota', 'gaji', 'usia']
            [5, 6, 5, 7, 6, 100]
            """,
            """
            Tabel berisi enam baris dan tiga kolom, dan kolom gaji menyimpan enam bilangan termasuk pencilan seratus.
            """,
            filename="dataframe.py",
        ),
        T("""
        ## describe: ringkasan sekaligus

        Metode `describe` pada kolom numerik mengembalikan banyak data, rata-rata, simpangan baku sampel, minimum, kuartil, dan maksimum dalam satu panggilan. Ia adalah ringkasan lima angka yang ditambah rata-rata dan simpangan baku, sehingga perbandingan rata-rata dengan median langsung terlihat.

        Pada gaji kita, rata-rata 21,5 jauh di atas median 6, dan simpangan baku 38,46 sangat besar dibanding kuartil yang rapat 5,25 sampai 6,75. Pola ini menandakan pencilan tanpa perlu menggambar apa pun.
        """),
        C(
            DF + """
            print(df['gaji'].describe().round(4).to_dict())
            """,
            """
            {'count': 6.0, 'mean': 21.5, 'std': 38.4643, 'min': 5.0, '25%': 5.25, '50%': 6.0, '75%': 6.75, 'max': 100.0}
            """,
            """
            Rata-rata dua puluh satu koma lima jauh dari median enam, dan kuartil rapat menandakan satu pencilan besar.
            """,
            filename="describe.py",
        ),
        T("""
        ## value_counts untuk kategori

        Untuk kolom kategori, ringkasan yang sesuai adalah frekuensi tiap nilai. Metode `value_counts` menghitungnya dan mengurutkan dari yang terbanyak. Dengan `normalize=True` ia mengembalikan proporsi yang berjumlah satu, sehingga tabel berukuran berbeda dapat dibandingkan.

        Kota B muncul tiga kali atau separuh data, kota A dua kali, dan kota C sekali. Modus kolom kategori adalah nilai paling atas pada hasil ini. Untuk kolom dengan banyak nilai unik, `head` atau parameter `dropna` membantu fokus pada yang penting.
        """),
        C(
            DF + """
            print(df['kota'].value_counts().to_dict())
            print(df['kota'].value_counts(normalize=True).round(4).to_dict())
            """,
            """
            {'B': 3, 'A': 2, 'C': 1}
            {'B': 0.5, 'A': 0.3333, 'C': 0.1667}
            """,
            """
            Kota B mencakup separuh data, kota A sepertiga, dan kota C seperenam.
            """,
            filename="value_counts.py",
        ),
        T("""
        ## quantile dan metode statistik tunggal

        Selain `describe`, tersedia metode untuk tiap ukuran: `mean`, `median`, `std`, `var`, `min`, `max`, `skew`, dan `kurt`. Metode `quantile` menerima satu proporsi atau list proporsi dan memakai interpolasi linear, definisi yang kita pakai di pelajaran kuantil.

        Ingat default pandas: `std` dan `var` memakai pembagi `n - 1`, sedangkan NumPy memakai `n`. Ketidaksesuaian ini sumber kebingungan klasik. Tentukan parameter `ddof` secara eksplisit saat membandingkan hasil antar pustaka atau mereproduksi perhitungan manual.
        """),
        C(
            DF + """
            print(df['gaji'].quantile([0.25, 0.5, 0.75]).tolist())
            print(round(df['gaji'].std(), 4), round(df['gaji'].std(ddof=0), 4))
            """,
            """
            [5.25, 6.0, 6.75]
            38.4643 35.1129
            """,
            """
            Kuartil sama dengan hasil manual, dan simpangan baku sampel sedikit lebih besar daripada versi populasi.
            """,
            filename="quantile.py",
        ),
        T("""
        ## Nilai hilang

        Data nyata hampir selalu memiliki nilai hilang, ditandai `NaN` di pandas. Sebagian besar metode statistik pandas mengabaikan `NaN` secara default, sehingga rata-rata dihitung dari nilai yang ada saja. Ini praktis tetapi bisa menyesatkan bila banyak nilai hilang atau hilangnya tidak acak.

        Selalu hitung jumlah hilang dengan `isna().sum()` sebelum meringkas. Strategi umum adalah membuang baris, mengisi dengan median yang kokoh, atau mengisi dengan model. Setiap pilihan mengubah ringkasan, jadi dokumentasikan yang kamu pakai.
        """),
        C(
            """
            import pandas as pd

            s = pd.Series([1, None, 2, None, 9])
            print(int(s.isna().sum()), s.mean(), s.fillna(s.median()).mean())
            """,
            """
            2 4.0 3.2
            """,
            """
            Dua nilai hilang, rata-rata dari yang ada empat, dan setelah diisi median dua rata-ratanya turun menjadi tiga koma dua.
            """,
            filename="nilai_hilang.py",
        ),
        K(
            "warn",
            """
            Metode std dan var pandas memakai pembagi n dikurangi satu, sedangkan NumPy memakai n. Tulis ddof secara eksplisit.
            """,
            title="Default berbeda",
        ),
        T("""
        ## Memeriksa tipe kolom

        Sebelum meringkas, periksa tipe tiap kolom dengan `dtypes` dan `info`. Kolom angka yang tersimpan sebagai teks karena ada karakter aneh akan diperlakukan sebagai kategori, sehingga `describe` memberi ringkasan yang salah tanpa peringatan. Ubah dengan `pd.to_numeric` dan parameter `errors` untuk melihat nilai bermasalah.

        Kebiasaan sederhana ini mencegah banyak kesalahan diam-diam. Ringkasan yang dihitung pada tipe salah tampak sah tetapi tidak bermakna, dan kamu baru menyadarinya jauh setelah laporan terkirim.
        """),
        T("""
        ## Menyesuaikan describe

        `describe` dapat disesuaikan. Parameter `percentiles` mengubah kuantil yang ditampilkan, misalnya persentil 5, 50, dan 95 untuk menggambarkan ekor. Pada DataFrame, `include='all'` meringkas kolom numerik dan kategori sekaligus, dan kolom kategori mendapat banyak unik, nilai teratas, dan frekuensinya.

        Menambah persentil ekor sangat berguna untuk data berpencilan. Selisih besar antara persentil sembilan puluh lima dan maksimum menandakan ekor yang jauh melampaui mayoritas data.
        """),
        E(
            "A5-06-1-ex1",
            "mudah",
            """
            Tulis fungsi `ringkas(data)` yang membuat `pd.Series` dari list dan mengembalikan dictionary dengan kunci `n`, `rata`, `median`, `std` (sampel), `min`, `max`. Nilai pecahan dibulatkan 4 desimal.
            """,
            """
            import pandas as pd

            def ringkas(data):
                # TODO: implementasikan
                pass
            """,
            """
            r = ringkas([5, 6, 5, 7, 6, 100])
            assert r == {'n': 6, 'rata': 21.5, 'median': 6.0, 'std': 38.4643, 'min': 5, 'max': 100}
            r2 = ringkas([2, 4, 4, 4, 5, 5, 7, 9])
            assert r2['rata'] == 5.0 and r2['std'] == 2.1381
            assert ringkas([3])['n'] == 1
            """,
            "Bungkus data dalam Series lalu panggil metode statistiknya dan ubah ke tipe Python.",
            """
            import pandas as pd

            def ringkas(data):
                s = pd.Series(data)
                return {
                    'n': int(s.count()),
                    'rata': round(float(s.mean()), 4),
                    'median': round(float(s.median()), 4),
                    'std': round(float(s.std()), 4),
                    'min': float(s.min()),
                    'max': float(s.max()),
                }
            """,
        ),
        E(
            "A5-06-1-ex2",
            "sedang",
            """
            Tulis fungsi `frekuensi(data, normalisasi=False)` yang mengembalikan dictionary frekuensi tiap nilai memakai `value_counts`. Bila `normalisasi` benar kembalikan proporsi dibulatkan 4 desimal.
            """,
            """
            import pandas as pd

            def frekuensi(data, normalisasi=False):
                # TODO: implementasikan
                pass
            """,
            """
            kota = ['A', 'A', 'B', 'B', 'B', 'C']
            assert frekuensi(kota) == {'B': 3, 'A': 2, 'C': 1}
            assert frekuensi(kota, normalisasi=True) == {'B': 0.5, 'A': 0.3333, 'C': 0.1667}
            assert frekuensi(['x']) == {'x': 1}
            """,
            "Pakai value_counts dengan parameter normalize lalu ubah ke dictionary Python.",
            """
            import pandas as pd

            def frekuensi(data, normalisasi=False):
                vc = pd.Series(data).value_counts(normalize=normalisasi)
                if normalisasi:
                    return {k: round(float(v), 4) for k, v in vc.items()}
                return {k: int(v) for k, v in vc.items()}
            """,
        ),
        E(
            "A5-06-1-ex3",
            "sedang",
            """
            Tulis fungsi `kuantil_pandas(data, qs)` yang mengembalikan list kuantil untuk tiap proporsi di `qs` memakai `Series.quantile`, sebagai float Python.
            """,
            """
            import pandas as pd

            def kuantil_pandas(data, qs):
                # TODO: implementasikan
                pass
            """,
            """
            assert kuantil_pandas([5, 6, 5, 7, 6, 100], [0.25, 0.5, 0.75]) == [5.25, 6.0, 6.75]
            assert kuantil_pandas([1, 2, 3, 4, 5], [0.1]) == [1.4]
            assert kuantil_pandas([10, 20], [0, 1]) == [10.0, 20.0]
            """,
            "Panggil quantile dengan list proporsi lalu ubah ke list Python.",
            """
            import pandas as pd

            def kuantil_pandas(data, qs):
                return [round(float(v), 4) for v in pd.Series(data).quantile(qs).tolist()]
            """,
        ),
        E(
            "A5-06-1-ex4",
            "menantang",
            """
            Tulis fungsi `ringkas_hilang(data)` yang menerima list dengan `None` sebagai nilai hilang dan mengembalikan tuple `(jumlah_hilang, rata_rata_tanpa_hilang, rata_rata_setelah_isi_median)`, dibulatkan 4 desimal.
            """,
            """
            import pandas as pd

            def ringkas_hilang(data):
                # TODO: implementasikan
                pass
            """,
            """
            assert ringkas_hilang([1, None, 2, None, 9]) == (2, 4.0, 3.2)
            assert ringkas_hilang([4, None]) == (1, 4.0, 4.0)
            assert ringkas_hilang([1, 2, 3]) == (0, 2.0, 2.0)
            """,
            "Hitung hilang dengan isna lalu bandingkan rata-rata sebelum dan sesudah fillna median.",
            """
            import pandas as pd

            def ringkas_hilang(data):
                s = pd.Series(data, dtype='float64')
                return (
                    int(s.isna().sum()),
                    round(float(s.mean()), 4),
                    round(float(s.fillna(s.median()).mean()), 4),
                )
            """,
        ),
    ],
    [
        M("Mengira std pandas dan NumPy sama.", "Atur ddof secara eksplisit."),
        M("Meringkas tanpa memeriksa nilai hilang.", "Hitung isna().sum() terlebih dahulu."),
        M("Memakai rata-rata saja pada kolom berpencilan.", "Bandingkan dengan median dari describe."),
    ],
    [
        Q("describe mengembalikan?", ["Banyak, rata, std, kuartil, min, maks", "Hanya rata-rata", "Hanya modus", "Korelasi"], 0, "Ringkasan sekaligus.", hint="Delapan angka."),
        Q("value_counts dengan normalize=True memberi?", ["Proporsi", "Banyak mutlak", "Rata-rata", "Median"], 0, "Jumlah satu.", hint="Proporsi."),
        Q("Default std pandas memakai?", ["n - 1", "n", "n + 1", "2n"], 0, "Sampel.", hint="Bessel."),
        Q("Nilai hilang ditandai?", ["NaN", "0", "Kosong string", "-1"], 0, "Not a Number.", hint="NaN."),
        Q("quantile memakai?", ["Interpolasi linear", "Pembulatan", "Modus", "Acak"], 0, "Default.", hint="Interpolasi."),
    ],
    [
        "describe merangkum kolom numerik dalam satu panggilan.",
        "value_counts meringkas kolom kategori dengan frekuensi dan proporsi.",
        "Default pandas memakai pembagi n dikurangi satu pada std.",
        "Periksa nilai hilang sebelum meringkas dan dokumentasikan penanganannya.",
    ],
    [],
)

l2 = lesson(
    "A5-06-2",
    "Meringkas per kelompok dengan groupby",
    35,
    [
        "Menghitung ringkasan per kelompok dengan groupby",
        "Memakai agg dengan beberapa fungsi dan nama kolom hasil",
        "Memakai transform untuk menghitung selisih terhadap rata-rata kelompok",
        "Menjelaskan pola split-apply-combine",
    ],
    [
        T("""
        ## Pola split-apply-combine

        Pertanyaan analisis yang paling umum adalah per kelompok: rata-rata gaji per kota, penjualan per bulan, waktu respons per layanan. Pola yang melandasinya disebut **split-apply-combine**: pisahkan data menjadi kelompok berdasarkan kunci, terapkan fungsi pada tiap kelompok, lalu gabungkan hasilnya menjadi satu tabel.

        Pandas menyediakannya lewat `groupby`. Ia mirip `GROUP BY` di SQL, sehingga kamu yang sudah mengenal SQL akan merasa akrab, dan banyak analisis dapat dilakukan dengan salah satunya secara setara.
        """),
        T("""
        ## groupby dasar

        Panggil `df.groupby('kota')` untuk membuat objek kelompok, lalu pilih kolom dan fungsi: `df.groupby('kota')['gaji'].mean()`. Hasilnya Series dengan indeks nama kota. Kota A rata-rata 5,5, kota B 6, dan kota C 100, tetapi kota C hanya berisi satu orang sehingga angkanya tidak mewakili apa pun.

        Itu pengingat penting: ringkasan per kelompok harus disertai ukuran kelompok. Rata-rata dari satu pengamatan atau dua pengamatan sangat tidak stabil, dan perbedaan antar kelompok kecil bisa murni kebetulan.
        """),
        C(
            DF + """
            print(df.groupby('kota')['gaji'].mean().to_dict())
            print(df.groupby('kota')['gaji'].size().to_dict())
            """,
            """
            {'A': 5.5, 'B': 6.0, 'C': 100.0}
            {'A': 2, 'B': 3, 'C': 1}
            """,
            """
            Rata-rata per kota jauh berbeda, tetapi kota C hanya berisi satu orang sehingga rata-ratanya tidak dapat diandalkan.
            """,
            filename="groupby_dasar.py",
        ),
        T("""
        ## agg dengan banyak ukuran

        Metode `agg` menerapkan beberapa fungsi sekaligus. Sintaks bernama `agg(n=('gaji', 'size'), rata=('gaji', 'mean'), med=('gaji', 'median'))` menamai kolom hasil sehingga tabelnya langsung siap dibaca. Menyandingkan rata-rata dan median per kelompok sekaligus memperlihatkan kelompok mana yang miring.

        Kamu juga bisa memberi fungsi buatan sendiri, misalnya rentang atau persentil tertentu. Gabungkan beberapa kolom sumber dengan menambah tuple lain ke `agg`, sehingga satu panggilan menghasilkan seluruh laporan per kelompok.
        """),
        C(
            DF + """
            hasil = df.groupby('kota').agg(
                n=('gaji', 'size'),
                rata=('gaji', 'mean'),
                med=('gaji', 'median'),
            )
            print(hasil.to_dict('index'))
            """,
            """
            {'A': {'n': 2, 'rata': 5.5, 'med': 5.5}, 'B': {'n': 3, 'rata': 6.0, 'med': 6.0}, 'C': {'n': 1, 'rata': 100.0, 'med': 100.0}}
            """,
            """
            Agregasi bernama menghasilkan tabel dengan ukuran, rata-rata, dan median untuk tiap kota dalam satu panggilan.
            """,
            filename="agg_bernama.py",
        ),
        T("""
        ## Fungsi buatan sendiri dengan apply

        Bila ukuran yang diinginkan tidak tersedia sebagai metode, gunakan `apply` dengan fungsi yang menerima Series tiap kelompok. Misalnya rentang per kelompok: `lambda s: s.max() - s.min()`. Kota A memiliki rentang satu, B dua, dan C nol karena hanya satu data.

        `apply` fleksibel tetapi lebih lambat daripada metode bawaan yang dioptimalkan. Pakai metode bawaan bila ada, dan `apply` hanya untuk kebutuhan khusus, terutama pada data besar dengan jutaan baris.
        """),
        C(
            DF + """
            print(df.groupby('kota')['gaji'].apply(lambda s: s.max() - s.min()).to_dict())
            """,
            """
            {'A': 1, 'B': 2, 'C': 0}
            """,
            """
            Rentang per kelompok dihitung dengan fungsi buatan sendiri, dan kota C bernilai nol karena satu data.
            """,
            filename="apply_rentang.py",
        ),
        T("""
        ## transform: hasil sebesar data asli

        Berbeda dengan `agg` yang menyusutkan tiap kelompok menjadi satu baris, `transform` mengembalikan hasil dengan panjang sama dengan data asli, tiap baris diisi hasil kelompoknya. Ini ideal untuk menghitung selisih terhadap rata-rata kelompok, standardisasi per kelompok, atau persentase dari total kelompok.

        Contoh: gaji dikurangi rata-rata kotanya menunjukkan siapa di atas atau di bawah rekan sekotanya. Hasilnya sejajar dengan baris asli sehingga mudah ditempel sebagai kolom baru.
        """),
        C(
            DF + """
            print((df['gaji'] - df.groupby('kota')['gaji'].transform('mean')).tolist())
            """,
            """
            [-0.5, 0.5, -1.0, 1.0, 0.0, 0.0]
            """,
            """
            Selisih dari rata-rata kota menunjukkan tiap orang relatif terhadap sekotanya, dan kota C selalu nol.
            """,
            filename="transform.py",
        ),
        T("""
        ## Pitfall groupby

        Beberapa jebakan umum. Pertama, kunci hilang diabaikan secara default, sehingga baris dengan kota kosong lenyap dari hasil. Kedua, mengelompokkan menurut dua kunci menghasilkan indeks bertingkat yang perlu `reset_index` bila diinginkan tabel datar. Ketiga, urutan kelompok mengikuti pengurutan kunci, bukan urutan kemunculan, kecuali diatur.

        Jebakan paling licin adalah paradoks Simpson yang dibahas sebelumnya: ringkasan per kelompok bisa berlawanan dengan ringkasan keseluruhan. Selalu bandingkan keduanya.
        """),
        K(
            "tip",
            """
            Sertakan ukuran kelompok bersama setiap ringkasan per kelompok. Kelompok kecil menghasilkan ringkasan yang tidak stabil.
            """,
            title="Sertakan n",
        ),
        T("""
        ## Beberapa kunci sekaligus

        Kamu dapat mengelompokkan menurut lebih dari satu kolom dengan memberi list kunci, misalnya kota dan jenis kelamin. Hasilnya memiliki indeks bertingkat dengan satu level per kunci. Panggil `reset_index` untuk mengubahnya menjadi kolom biasa agar tabel mudah digabung atau digambar.

        Semakin banyak kunci, semakin kecil tiap kelompok. Kombinasi yang terlalu rinci menghasilkan kelompok berisi satu atau dua baris sehingga ringkasannya tidak stabil. Pilih kunci yang sesuai pertanyaan, bukan sebanyak mungkin.
        """),
        T("""
        ## Membandingkan kelompok dengan keseluruhan

        Ringkasan per kelompok paling bermakna bila dibandingkan dengan keseluruhan. Hitung rata-rata keseluruhan lalu tampilkan selisih tiap kelompok terhadapnya, atau persentase kontribusi tiap kelompok pada total. Perbandingan ini menyoroti kelompok yang paling menyimpang.

        Kedua pandangan perlu dilihat bersama untuk menghindari paradoks Simpson. Bila arah perbedaan per kelompok berlawanan dengan keseluruhan, ada variabel pengganggu yang harus dipahami sebelum kesimpulan ditarik.
        """),
        T("""
        ## Pivot table

        `pivot_table` adalah bentuk lain dari groupby dua kunci yang menaruh satu kunci sebagai baris dan satu lagi sebagai kolom, dengan fungsi agregasi di sel. Ia mirip tabel pivot di spreadsheet dan membuat perbandingan dua dimensi mudah dibaca.

        Pada dataset kecil kita, pivot kota terhadap level gaji dengan jumlah baris sebagai agregasi sama persis dengan tabel silang. Perbedaannya, pivot dapat memakai agregasi apa pun, misalnya rata-rata gaji, sedangkan tabel silang hanya menghitung frekuensi.
        """),
        E(
            "A5-06-2-ex1",
            "mudah",
            """
            Tulis fungsi `rata_per_kelompok(kunci, nilai)` yang mengembalikan dictionary rata-rata `nilai` per `kunci` memakai groupby, sebagai float Python.
            """,
            """
            import pandas as pd

            def rata_per_kelompok(kunci, nilai):
                # TODO: implementasikan
                pass
            """,
            """
            assert rata_per_kelompok(['A', 'A', 'B', 'B', 'B', 'C'], [5, 6, 5, 7, 6, 100]) == {'A': 5.5, 'B': 6.0, 'C': 100.0}
            assert rata_per_kelompok(['x', 'y', 'x'], [1, 2, 3]) == {'x': 2.0, 'y': 2.0}
            assert rata_per_kelompok(['a'], [4]) == {'a': 4.0}
            """,
            "Buat DataFrame dari dua list lalu kelompokkan dan hitung rata-rata.",
            """
            import pandas as pd

            def rata_per_kelompok(kunci, nilai):
                df = pd.DataFrame({'k': kunci, 'v': nilai})
                return {k: float(v) for k, v in df.groupby('k')['v'].mean().items()}
            """,
        ),
        E(
            "A5-06-2-ex2",
            "sedang",
            """
            Tulis fungsi `agregat_kelompok(kunci, nilai)` yang mengembalikan dictionary per kunci berisi `n` (banyak), `rata`, dan `median`, memakai `agg` bernama. Nilai bertipe Python.
            """,
            """
            import pandas as pd

            def agregat_kelompok(kunci, nilai):
                # TODO: implementasikan
                pass
            """,
            """
            r = agregat_kelompok(['A', 'A', 'B', 'B', 'B', 'C'], [5, 6, 5, 7, 6, 100])
            assert r == {'A': {'n': 2, 'rata': 5.5, 'median': 5.5}, 'B': {'n': 3, 'rata': 6.0, 'median': 6.0}, 'C': {'n': 1, 'rata': 100.0, 'median': 100.0}}
            assert agregat_kelompok(['x', 'x'], [1, 3]) == {'x': {'n': 2, 'rata': 2.0, 'median': 2.0}}
            assert agregat_kelompok(['p', 'q', 'p'], [2, 8, 4]) == {'p': {'n': 2, 'rata': 3.0, 'median': 3.0}, 'q': {'n': 1, 'rata': 8.0, 'median': 8.0}}
            """,
            "Pakai agg bernama dengan size, mean, dan median lalu ubah ke dictionary bertingkat.",
            """
            import pandas as pd

            def agregat_kelompok(kunci, nilai):
                df = pd.DataFrame({'k': kunci, 'v': nilai})
                h = df.groupby('k').agg(n=('v', 'size'), rata=('v', 'mean'), median=('v', 'median'))
                return {
                    k: {'n': int(r['n']), 'rata': float(r['rata']), 'median': float(r['median'])}
                    for k, r in h.iterrows()
                }
            """,
        ),
        E(
            "A5-06-2-ex3",
            "sedang",
            """
            Tulis fungsi `rentang_per_kelompok(kunci, nilai)` yang mengembalikan dictionary selisih maksimum dan minimum `nilai` per `kunci` sebagai bilangan Python.
            """,
            """
            import pandas as pd

            def rentang_per_kelompok(kunci, nilai):
                # TODO: implementasikan
                pass
            """,
            """
            assert rentang_per_kelompok(['A', 'A', 'B', 'B', 'B', 'C'], [5, 6, 5, 7, 6, 100]) == {'A': 1, 'B': 2, 'C': 0}
            assert rentang_per_kelompok(['x', 'x'], [1.5, 4.0]) == {'x': 2.5}
            assert rentang_per_kelompok(['p', 'q', 'p', 'q'], [1, 10, 5, 4]) == {'p': 4.0, 'q': 6.0}
            """,
            "Pakai apply dengan fungsi maksimum dikurangi minimum pada tiap kelompok.",
            """
            import pandas as pd

            def rentang_per_kelompok(kunci, nilai):
                df = pd.DataFrame({'k': kunci, 'v': nilai})
                h = df.groupby('k')['v'].apply(lambda s: s.max() - s.min())
                return {k: float(v) for k, v in h.items()}
            """,
        ),
        E(
            "A5-06-2-ex4",
            "menantang",
            """
            Tulis fungsi `selisih_dari_rata_kelompok(kunci, nilai)` yang mengembalikan list selisih tiap nilai terhadap rata-rata kelompoknya memakai `transform`, sesuai urutan asli dan dibulatkan 4 desimal.
            """,
            """
            import pandas as pd

            def selisih_dari_rata_kelompok(kunci, nilai):
                # TODO: implementasikan
                pass
            """,
            """
            assert selisih_dari_rata_kelompok(['A', 'A', 'B', 'B', 'B', 'C'], [5, 6, 5, 7, 6, 100]) == [-0.5, 0.5, -1.0, 1.0, 0.0, 0.0]
            assert selisih_dari_rata_kelompok(['x', 'y', 'x'], [1, 2, 3]) == [-1.0, 0.0, 1.0]
            assert selisih_dari_rata_kelompok(['a', 'a'], [10, 20]) == [-5.0, 5.0]
            """,
            "Kurangi nilai dengan hasil transform mean per kelompok.",
            """
            import pandas as pd

            def selisih_dari_rata_kelompok(kunci, nilai):
                df = pd.DataFrame({'k': kunci, 'v': nilai})
                d = df['v'] - df.groupby('k')['v'].transform('mean')
                return [round(float(x), 4) + 0.0 for x in d.tolist()]
            """,
        ),
    ],
    [
        M("Melaporkan rata-rata per kelompok tanpa ukuran kelompok.", "Sertakan n pada setiap ringkasan."),
        M("Memakai apply untuk semua hal padahal ada metode bawaan.", "Pakai metode bawaan bila tersedia."),
        M("Lupa bahwa kunci hilang diabaikan oleh groupby.", "Periksa NaN pada kolom kunci."),
    ],
    [
        Q("Pola groupby disebut?", ["Split-apply-combine", "Map-reduce saja", "Sort-merge", "Fit-predict"], 0, "Pisah, terapkan, gabung.", hint="Tiga langkah."),
        Q("agg menghasilkan?", ["Satu baris per kelompok", "Baris sebanyak data", "Satu angka", "Grafik"], 0, "Menyusutkan.", hint="Ringkas."),
        Q("transform menghasilkan?", ["Panjang sama dengan data asli", "Satu per kelompok", "Satu angka", "Kosong"], 0, "Sejajar.", hint="Asli."),
        Q("size pada kelompok memberi?", ["Banyak baris", "Rata-rata", "Median", "Maks"], 0, "Ukuran.", hint="n."),
        Q("Rata-rata kelompok satu data?", ["Tidak stabil", "Sangat andal", "Nol", "Tak terdefinisi"], 0, "Sampel terlalu kecil.", hint="n kecil."),
    ],
    [
        "groupby memisahkan, menerapkan, dan menggabungkan ringkasan per kelompok.",
        "agg menyusutkan kelompok, transform mempertahankan panjang data asli.",
        "Selalu sertakan ukuran kelompok bersama ringkasan.",
        "Metode bawaan lebih cepat daripada apply buatan sendiri.",
    ],
    [],
)

l3 = lesson(
    "A5-06-3",
    "Tabel silang, korelasi, dan pengelompokan nilai",
    35,
    [
        "Membuat tabel silang dua kolom kategori",
        "Menghitung korelasi Pearson dan Spearman dengan pandas",
        "Mengubah kolom numerik menjadi kategori dengan cut",
        "Membatasi pencilan dengan clip",
    ],
    [
        T("""
        ## Dua kolom kategori

        Pada kolom kategori, pertanyaan alami adalah hubungan antara dua kolom: apakah kota tertentu lebih sering berpenghasilan tinggi? **Tabel silang** atau tabel kontingensi menghitung berapa baris jatuh pada setiap kombinasi dua kategori. Ini adalah padanan histogram untuk dua variabel kategori.

        Pandas menyediakannya lewat `pd.crosstab`. Hasilnya tabel dengan satu kategori sebagai baris dan kategori lain sebagai kolom, berisi frekuensi. Parameter `normalize` mengubahnya menjadi proporsi terhadap baris, kolom, atau total.
        """),
        C(
            DF + """
            df['level'] = ['rendah', 'tinggi', 'rendah', 'tinggi', 'tinggi', 'tinggi']
            print(pd.crosstab(df['kota'], df['level']).to_dict('index'))
            """,
            """
            {'A': {'rendah': 1, 'tinggi': 1}, 'B': {'rendah': 1, 'tinggi': 2}, 'C': {'rendah': 0, 'tinggi': 1}}
            """,
            """
            Tabel silang memperlihatkan banyaknya tiap kombinasi kota dan tingkat gaji, termasuk kombinasi yang tidak pernah muncul.
            """,
            filename="crosstab.py",
        ),
        T("""
        ## Membaca tabel silang

        Bandingkan proporsi, bukan frekuensi mentah, bila kelompok berbeda ukuran. Di kota B dua dari tiga orang bergaji tinggi, atau enam puluh tujuh persen, sedangkan di kota A separuh. Tetapi dengan ukuran sekecil ini, perbedaan itu bisa kebetulan sepenuhnya.

        Untuk menguji apakah dua kolom kategori berhubungan, dipakai uji khi-kuadrat yang membandingkan frekuensi teramati dengan frekuensi yang diharapkan bila keduanya independen. Tabel silang adalah titik awalnya, dan uji formal membutuhkan sampel lebih besar.
        """),
        T("""
        ## Korelasi dengan pandas

        Metode `corr` pada Series menghitung korelasi dengan Series lain, dan pada DataFrame menghitung matriks korelasi antar semua kolom numerik. Parameter `method` memilih `pearson`, `spearman`, atau `kendall`. Default-nya Pearson, dan kolom non-numerik harus dipilih terlebih dahulu.

        Pada data gaji dan usia, Pearson 0,82 lebih rendah dari Spearman 0,88, karena pencilan seratus menekan Pearson tetapi tidak mengubah urutan yang dipakai Spearman. Selisih seperti ini adalah petunjuk adanya pencilan atau hubungan nonlinear.
        """),
        C(
            DF + """
            print(round(df['gaji'].corr(df['usia']), 4))
            print(round(df['gaji'].corr(df['usia'], method='spearman'), 4))
            """,
            """
            0.8239
            0.8827
            """,
            """
            Korelasi Spearman lebih tinggi daripada Pearson karena pencilan menekan Pearson saja.
            """,
            filename="corr_pandas.py",
        ),
        T("""
        ## Mengelompokkan nilai numerik

        Kadang kolom numerik perlu diubah menjadi kategori: usia menjadi kelompok umur, gaji menjadi golongan. Fungsi `pd.cut` melakukannya dengan batas yang kita tentukan, dan `pd.qcut` membagi berdasarkan kuantil sehingga tiap kelompok berisi jumlah data hampir sama.

        Secara default `cut` memakai interval tertutup di kanan: nilai tepat di batas masuk kelompok bawahnya. Usia tiga puluh masuk kelompok muda bila batasnya nol, tiga puluh, empat puluh. Parameter `labels` memberi nama kelompok.
        """),
        C(
            DF + """
            kelompok = pd.cut(df['usia'], [0, 30, 40, 100], labels=['muda', 'tengah', 'senior'])
            print(kelompok.tolist())
            """,
            """
            ['muda', 'muda', 'muda', 'tengah', 'tengah', 'senior']
            """,
            """
            Usia dikelompokkan ke tiga kategori dan nilai tiga puluh masuk kelompok muda karena batas kanan tertutup.
            """,
            filename="cut.py",
        ),
        T("""
        ## Membatasi pencilan dengan clip

        Salah satu cara menangani pencilan tanpa membuang baris adalah **winsorisasi**: nilai di atas batas diganti batas itu sendiri. Di pandas, `clip(upper=...)` melakukannya. Dengan membatasi gaji pada sepuluh, rata-rata turun dari 21,5 menjadi 6,5, jauh lebih mewakili mayoritas.

        Winsorisasi mempertahankan jumlah data dan urutan, hanya menekan besarnya. Batas biasanya dipilih dari kuantil, misalnya persentil ke-99, atau dari pagar Tukey. Catat batas yang dipakai agar analisis dapat direproduksi.
        """),
        C(
            DF + """
            print(df['gaji'].mean(), df['gaji'].clip(upper=10).mean())
            """,
            """
            21.5 6.5
            """,
            """
            Membatasi gaji pada sepuluh menurunkan rata-rata dari dua puluh satu koma lima menjadi enam koma lima.
            """,
            filename="clip.py",
        ),
        T("""
        ## Alur ringkasan data eksploratif

        Rangkuman modul ini sebagai alur kerja: baca tabel, periksa bentuk dan tipe, hitung nilai hilang, ringkas kolom numerik dengan `describe` dan kolom kategori dengan `value_counts`, bandingkan antar kelompok dengan `groupby`, periksa hubungan dengan `corr` dan `crosstab`, lalu tangani pencilan dengan transformasi atau `clip`.

        Selalu gambar data di setiap tahap. Ringkasan angka adalah kompresi, dan setiap kompresi membuang informasi. Pelajaran berikutnya di kursus ini beralih ke SQL untuk analisis data, yang memberi cara lain untuk mengajukan pertanyaan serupa pada basis data.
        """),
        K(
            "tip",
            """
            Bandingkan Pearson dengan Spearman dan rata-rata dengan median. Selisih besar adalah sinyal paling murah dari pencilan.
            """,
            title="Sinyal murah",
        ),
        T("""
        ## Proporsi baris dan kolom

        Parameter `normalize` pada `crosstab` memilih penyebut. Dengan `normalize='index'` setiap baris berjumlah satu sehingga kamu membaca distribusi level di dalam tiap kota. Dengan `normalize='columns'` setiap kolom berjumlah satu sehingga kamu membaca komposisi kota di dalam tiap level.

        Pilih sesuai pertanyaan. Untuk melihat apakah kota memengaruhi level gaji, bandingkan proporsi baris. Memilih penyebut yang salah adalah sumber umum klaim yang tampak benar tetapi menjawab pertanyaan lain.
        """),
        T("""
        ## qcut untuk kelompok berukuran sama

        Bila `cut` memakai batas yang kamu tentukan, `qcut` memotong pada kuantil sehingga tiap kelompok berisi jumlah data hampir sama. Empat kelompok berarti kuartil, sepuluh berarti desil. Ini berguna untuk membuat peringkat relatif seperti lima puluh persen teratas atau dua puluh persen terbawah.

        Pada data sangat miring, batas `cut` yang sama lebar bisa membuat hampir semua data masuk satu kelompok, sedangkan `qcut` tetap membagi merata. Pilih sesuai tujuan: batas bermakna domain atau kelompok berukuran seimbang.
        """),
        T("""
        ## Dokumentasi keputusan

        Setiap langkah ringkasan membuat pilihan: cara menangani nilai hilang, batas pencilan, definisi kelompok, dan ukuran yang dilaporkan. Pilihan itu mengubah angka akhir, sehingga harus tercatat bersama hasilnya. Laporan yang hanya memuat angka tanpa pilihan di baliknya tidak bisa direproduksi atau dikritisi.

        Kebiasaan baik adalah menyimpan alur sebagai skrip atau notebook yang dapat dijalankan ulang dari data mentah. Dengan begitu perubahan pilihan dapat diuji dampaknya, dan orang lain dapat memeriksa pekerjaanmu.
        """),
        E(
            "A5-06-3-ex1",
            "mudah",
            """
            Tulis fungsi `tabel_silang(a, b)` yang mengembalikan dictionary bertingkat frekuensi kombinasi nilai `a` (baris) dan `b` (kolom) memakai `pd.crosstab`, dengan nilai bilangan bulat Python.
            """,
            """
            import pandas as pd

            def tabel_silang(a, b):
                # TODO: implementasikan
                pass
            """,
            """
            kota = ['A', 'A', 'B', 'B', 'B', 'C']
            level = ['rendah', 'tinggi', 'rendah', 'tinggi', 'tinggi', 'tinggi']
            assert tabel_silang(kota, level) == {'A': {'rendah': 1, 'tinggi': 1}, 'B': {'rendah': 1, 'tinggi': 2}, 'C': {'rendah': 0, 'tinggi': 1}}
            assert tabel_silang(['x', 'x'], ['p', 'p']) == {'x': {'p': 2}}
            assert tabel_silang(['a', 'b'], ['u', 'v']) == {'a': {'u': 1, 'v': 0}, 'b': {'u': 0, 'v': 1}}
            """,
            "Panggil crosstab pada dua Series lalu ubah ke dictionary bertingkat.",
            """
            import pandas as pd

            def tabel_silang(a, b):
                t = pd.crosstab(pd.Series(a), pd.Series(b))
                return {r: {c: int(t.loc[r, c]) for c in t.columns} for r in t.index}
            """,
        ),
        E(
            "A5-06-3-ex2",
            "sedang",
            """
            Tulis fungsi `korelasi_pandas(a, b, metode='pearson')` yang mengembalikan korelasi dua list memakai `Series.corr` dan parameter `method`, dibulatkan 4 desimal.
            """,
            """
            import pandas as pd

            def korelasi_pandas(a, b, metode='pearson'):
                # TODO: implementasikan
                pass
            """,
            """
            gaji = [5, 6, 5, 7, 6, 100]
            usia = [25, 30, 28, 35, 40, 50]
            assert korelasi_pandas(gaji, usia) == 0.8239
            assert korelasi_pandas(gaji, usia, 'spearman') == 0.8827
            assert korelasi_pandas([1, 2, 3, 4, 5], [5, 4, 3, 2, 1]) == -1.0
            """,
            "Bungkus kedua list dalam Series lalu panggil corr dengan metode yang diminta.",
            """
            import pandas as pd

            def korelasi_pandas(a, b, metode='pearson'):
                return round(float(pd.Series(a).corr(pd.Series(b), method=metode)), 4)
            """,
        ),
        E(
            "A5-06-3-ex3",
            "sedang",
            """
            Tulis fungsi `kategori_usia(usia, batas, label)` yang mengembalikan list label kategori tiap usia memakai `pd.cut` dengan interval tertutup di kanan.
            """,
            """
            import pandas as pd

            def kategori_usia(usia, batas, label):
                # TODO: implementasikan
                pass
            """,
            """
            u = [25, 30, 28, 35, 40, 50]
            assert kategori_usia(u, [0, 30, 40, 100], ['muda', 'tengah', 'senior']) == ['muda', 'muda', 'muda', 'tengah', 'tengah', 'senior']
            assert kategori_usia([10, 70], [0, 18, 100], ['anak', 'dewasa']) == ['anak', 'dewasa']
            assert kategori_usia([18, 19], [0, 18, 100], ['anak', 'dewasa']) == ['anak', 'dewasa']
            """,
            "Panggil pd.cut dengan batas dan label lalu ubah hasilnya ke list.",
            """
            import pandas as pd

            def kategori_usia(usia, batas, label):
                return [str(x) for x in pd.cut(pd.Series(usia), batas, labels=label).tolist()]
            """,
        ),
        E(
            "A5-06-3-ex4",
            "menantang",
            """
            Tulis fungsi `rata_dibatasi(data, batas_atas)` yang membatasi nilai di atas `batas_atas` dengan `clip` lalu mengembalikan rata-rata dibulatkan 4 desimal.
            """,
            """
            import pandas as pd

            def rata_dibatasi(data, batas_atas):
                # TODO: implementasikan
                pass
            """,
            """
            assert rata_dibatasi([5, 6, 5, 7, 6, 100], 10) == 6.5
            assert rata_dibatasi([1, 2, 3], 2) == 1.6667
            assert rata_dibatasi([1, 2, 3], 5) == 2.0
            """,
            "Pakai clip dengan parameter upper lalu hitung rata-rata.",
            """
            import pandas as pd

            def rata_dibatasi(data, batas_atas):
                return round(float(pd.Series(data).clip(upper=batas_atas).mean()), 4)
            """,
        ),
    ],
    [
        M("Menganggap perbedaan proporsi pada kelompok kecil pasti nyata.", "Pertimbangkan ukuran sampel dan uji formal."),
        M("Mengelompokkan numerik tanpa memahami batas tertutup di kanan.", "Periksa batas dan parameter right."),
        M("Membuang pencilan tanpa mencatat batas yang dipakai.", "Catat metode dan batas agar reprodusibel."),
    ],
    [
        Q("crosstab menghitung?", ["Frekuensi kombinasi dua kategori", "Korelasi", "Rata-rata", "Median"], 0, "Tabel kontingensi.", hint="Kombinasi."),
        Q("Metode corr default?", ["Pearson", "Spearman", "Kendall", "Tak ada"], 0, "Default.", hint="Linear."),
        Q("pd.cut membagi menurut?", ["Batas yang ditentukan", "Kuantil otomatis", "Acak", "Indeks"], 0, "Batas manual.", hint="Batas."),
        Q("clip upper melakukan?", ["Membatasi nilai maksimum", "Membuang baris", "Mengurutkan", "Menghapus NaN"], 0, "Winsorisasi.", hint="Batas atas."),
        Q("Spearman lebih tinggi dari Pearson menandakan?", ["Pencilan atau nonlinearitas", "Data bersih", "Sampel besar", "Tak ada"], 0, "Petunjuk.", hint="Selisih."),
    ],
    [
        "crosstab meringkas hubungan dua kolom kategori.",
        "corr mendukung Pearson, Spearman, dan Kendall lewat parameter method.",
        "cut mengubah numerik menjadi kategori dengan batas tertutup di kanan.",
        "clip membatasi pencilan tanpa membuang baris.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa konsep dan perhitungan yang cukup jelas dalam teks.", "brief": []}

write_module(
    "A5",
    6,
    "Meringkas data dengan pandas",
    105,
    [
        "Meringkas kolom numerik dan kategori dengan pandas",
        "Meringkas per kelompok dengan groupby dan agg",
        "Memakai crosstab, corr, cut, dan clip dalam alur eksplorasi",
    ],
    [l1, l2, l3],
    video,
    REF,
)
