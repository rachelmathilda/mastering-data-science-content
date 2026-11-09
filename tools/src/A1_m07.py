import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import T, K, A, C, E, Q, M, lesson, write_module

REF = []

l1 = lesson(
    "A1-07-1",
    "Membaca dan menulis file teks",
    35,
    [
        "Membuka file dengan open dan with serta memilih mode yang tepat",
        "Membaca isi file dengan read, readline, readlines, dan penelusuran baris",
        "Menulis dan menambah isi file dengan aman",
        "Menangani encoding, baris baru, dan file besar dengan benar",
    ],
    [
        T("""
        ## Mengapa file penting

        Hampir semua proyek data dimulai dari file: log, laporan teks, ekspor basis data, atau hasil scraping. Program yang hanya bekerja dengan data di memori akan kehilangan semuanya saat berhenti. Dengan file, hasil kerjamu bertahan, bisa dibagikan, dan bisa dibaca program lain.

        Python membuka file dengan fungsi `open(nama, mode)`. Mode `"r"` membaca (bawaan), `"w"` menulis dan menghapus isi lama, `"a"` menambah di akhir, dan `"x"` membuat file baru serta gagal bila sudah ada. Tambahkan `"b"` untuk mode biner, misalnya gambar. Selalu tentukan `encoding="utf-8"` untuk teks agar karakter non-Latin terbaca benar di semua sistem.

        Catatan: di aplikasi ini kode berjalan di lingkungan terisolasi, sehingga file yang kamu tulis ada di ruang sementara dan hilang saat kompiler diatur ulang. Pada komputer sungguhan, file tersimpan permanen.
        """),
        T("""
        ## Pernyataan with

        File yang dibuka harus ditutup agar data tertulis dengan benar dan sumber daya sistem dilepas. Cara paling aman adalah pernyataan `with open(...) as f:`. Blok `with` menutup file secara otomatis saat selesai, bahkan bila terjadi error di tengah jalan. Menutup manual dengan `f.close()` mudah terlupa dan menimbulkan bug yang sulit dilacak.

        Setelah blok `with` berakhir, objek file sudah tertutup dan tidak bisa dibaca lagi. Semua pembacaan harus dilakukan di dalam blok, atau isinya disimpan ke variabel selama blok masih terbuka. Biasakan menulis `with` setiap kali membuka file.

        Pola ini disebut *context manager* dan dipakai juga untuk koneksi basis data, kunci, dan sumber daya lain. Memahaminya sekarang akan membantumu di banyak bagian Python berikutnya.
        """),
        C(
            """
            with open("catatan.txt", "w", encoding="utf-8") as f:
                f.write("baris satu\\n")
                f.write("baris dua\\n")
                f.write("baris tiga\\n")

            with open("catatan.txt", "r", encoding="utf-8") as f:
                isi = f.read()
            print(repr(isi))
            print(f.closed)

            with open("catatan.txt", "a", encoding="utf-8") as f:
                f.write("baris empat\\n")

            with open("catatan.txt", encoding="utf-8") as f:
                print(len(f.read().splitlines()))
            """,
            """
            'baris satu\\nbaris dua\\nbaris tiga\\n'
            True
            4
            """,
            """
            Mode `w` menulis baru, mode `a` menambah di akhir. Setelah blok `with` selesai file otomatis tertutup sehingga `f.closed` bernilai `True`.
            """,
            filename="tulis_baca.py",
        ),
        T("""
        ## Cara membaca isi file

        `f.read()` membaca seluruh isi sebagai satu string. `f.readline()` membaca satu baris termasuk karakter baris baru di akhirnya. `f.readlines()` membaca semua baris sebagai list string. Namun cara paling idiomatik dan hemat memori adalah menelusuri objek file langsung: `for baris in f:` memberi satu baris per putaran tanpa memuat seluruh file.

        Setiap baris yang dibaca masih membawa `\\n` di ujungnya, jadi biasanya kamu memanggil `.strip()` atau `.rstrip("\\n")`. Lupa membuang baris baru adalah sumber bug klasik, misalnya saat membandingkan string atau mengubahnya menjadi angka.

        Untuk file besar sampai gigabyte, jangan pakai `read()` atau `readlines()` karena akan menghabiskan memori. Telusuri baris demi baris, yang pada dasarnya adalah generator seperti yang kamu pelajari sebelumnya.
        """),
        C(
            """
            with open("angka.txt", "w", encoding="utf-8") as f:
                f.write("10\\n20\\n\\n30\\n")

            with open("angka.txt", encoding="utf-8") as f:
                print(repr(f.readline()))
                print(f.readlines())

            total = 0
            with open("angka.txt", encoding="utf-8") as f:
                for baris in f:
                    baris = baris.strip()
                    if baris:
                        total += int(baris)
            print(total)

            with open("angka.txt", encoding="utf-8") as f:
                nilai = [int(b) for b in f if b.strip()]
            print(nilai, sum(nilai))
            """,
            """
            '10\\n'
            ['20\\n', '\\n', '30\\n']
            60
            [10, 20, 30] 60
            """,
            """
            Menelusuri file baris demi baris hemat memori. Tiap baris membawa karakter baris baru sehingga perlu `strip`, dan baris kosong dilewati dengan `if`.
            """,
            filename="baca_baris.py",
        ),
        K(
            "warning",
            """
            Mode `"w"` langsung menghapus isi file lama begitu dibuka. Gunakan `"a"` bila ingin menambah, dan periksa nama file dua kali sebelum menulis.
            """,
            title="Mode w menghapus",
        ),
        T("""
        ## Encoding, baris baru, dan penanganan error

        **Encoding** menentukan cara karakter diubah menjadi byte. Standar yang aman hampir selalu `utf-8`. Bila file dibaca dengan encoding yang salah, kamu mendapat `UnicodeDecodeError` atau karakter rusak. Selalu tulis `encoding="utf-8"` secara eksplisit agar perilaku sama di Windows, macOS, dan Linux.

        Saat membuka file yang tidak ada dengan mode `"r"`, Python menimbulkan `FileNotFoundError`. Tangkap dengan `try except` bila ketiadaan file adalah kemungkinan wajar, misalnya file konfigurasi opsional. Jangan menangkap semua error tanpa pandang bulu karena akan menyembunyikan bug sungguhan.

        Fungsi `print` bisa menulis ke file dengan argumen `file=f`, dan secara otomatis menambah baris baru. Ini kadang lebih nyaman daripada `f.write` karena tidak perlu menulis `\\n` manual. Untuk menulis banyak baris sekaligus, gunakan `f.writelines(daftar)`, ingat bahwa ia tidak menambah baris baru sendiri.
        """),
        C(
            """
            try:
                open("tidak_ada.txt", encoding="utf-8")
            except FileNotFoundError:
                print("file tidak ditemukan")

            with open("p.txt", "w", encoding="utf-8") as f:
                print("satu", file=f)
                print("dua", file=f)
                f.writelines(["tiga\\n", "empat\\n"])

            with open("p.txt", encoding="utf-8") as f:
                print([b.rstrip("\\n") for b in f])

            with open("utf.txt", "w", encoding="utf-8") as f:
                f.write("café ☕")
            with open("utf.txt", encoding="utf-8") as f:
                teks = f.read()
            print(teks, len(teks))
            """,
            """
            file tidak ditemukan
            ['satu', 'dua', 'tiga', 'empat']
            café ☕ 6
            """,
            """
            `FileNotFoundError` ditangkap secara spesifik. `print(file=f)` menambah baris baru otomatis, `writelines` tidak. UTF-8 menjaga karakter khusus.
            """,
            filename="encoding_error.py",
        ),
        T("""
        ## Pola umum: ringkasan file teks

        Satu tugas klasik adalah membaca file teks dan menghitung statistik sederhana: jumlah baris, jumlah kata, dan kata paling sering. Polanya selalu sama: buka dengan `with`, telusuri baris, bersihkan, lalu kumpulkan hasil di struktur data seperti dictionary penghitung.

        Karena latihan di aplikasi ini berjalan tanpa file eksternal, kamu akan memakai `io.StringIO`, objek yang berperilaku persis seperti file tetapi berada di memori. Fungsi yang kamu tulis menerima objek mirip-file sehingga bisa dipakai pada file sungguhan maupun StringIO tanpa perubahan. Desain seperti ini membuat fungsi mudah diuji.

        Prinsipnya: pisahkan logika dari sumber data. Fungsi yang menerima objek file atau iterable baris lebih fleksibel daripada fungsi yang membuka file di dalamnya.
        """),
        E(
            "A1-07-1-ex1",
            "mudah",
            """
            Tulis fungsi `hitung_baris(f)` yang menerima objek mirip-file dan mengembalikan jumlah baris yang tidak kosong (setelah dibersihkan spasi).
            """,
            """
            def hitung_baris(f):
                # TODO: implementasikan
                pass
            """,
            """
            import io
            assert hitung_baris(io.StringIO("a\\nb\\n\\nc\\n")) == 3
            assert hitung_baris(io.StringIO("")) == 0
            assert hitung_baris(io.StringIO("  \\n x \\n")) == 1
            """,
            "Telusuri f dan hitung baris yang strip-nya tidak kosong.",
            """
            def hitung_baris(f):
                return sum(1 for b in f if b.strip())
            """,
        ),
        E(
            "A1-07-1-ex2",
            "mudah",
            """
            Tulis fungsi `jumlah_angka(f)` yang menerima objek mirip-file berisi satu bilangan bulat per baris dan mengembalikan jumlahnya. Baris kosong dilewati.
            """,
            """
            def jumlah_angka(f):
                # TODO: implementasikan
                pass
            """,
            """
            import io
            assert jumlah_angka(io.StringIO("10\\n20\\n\\n30\\n")) == 60
            assert jumlah_angka(io.StringIO("")) == 0
            assert jumlah_angka(io.StringIO("-5\\n5")) == 0
            """,
            "Ubah tiap baris tak kosong menjadi int lalu jumlahkan.",
            """
            def jumlah_angka(f):
                return sum(int(b) for b in f if b.strip())
            """,
        ),
        E(
            "A1-07-1-ex3",
            "sedang",
            """
            Tulis fungsi `kata_terpanjang(f)` yang menerima objek mirip-file dan mengembalikan kata terpanjang dari seluruh isi. Bila ada beberapa yang sama panjang, ambil yang pertama muncul. Bila kosong kembalikan string kosong.
            """,
            """
            def kata_terpanjang(f):
                # TODO: implementasikan
                pass
            """,
            """
            import io
            assert kata_terpanjang(io.StringIO("a bb ccc\\ndd eee\\n")) == "ccc"
            assert kata_terpanjang(io.StringIO("")) == ""
            assert kata_terpanjang(io.StringIO("ab cd\\n")) == "ab"
            assert kata_terpanjang(io.StringIO("x\\n\\nyyyy zz")) == "yyyy"
            """,
            "Kumpulkan kata dari semua baris lalu pakai max dengan key=len.",
            """
            def kata_terpanjang(f):
                kata = [k for b in f for k in b.split()]
                return max(kata, key=len) if kata else ""
            """,
        ),
        E(
            "A1-07-1-ex4",
            "menantang",
            """
            Tulis fungsi `frekuensi_baris(f)` yang menerima objek mirip-file dan mengembalikan list tuple `(kata, jumlah)` untuk tiga kata paling sering di seluruh isi, huruf diseragamkan kecil. Urut jumlah menurun lalu kata naik bila sama.
            """,
            """
            def frekuensi_baris(f):
                # TODO: implementasikan
                pass
            """,
            """
            import io
            t = io.StringIO("Kopi teh kopi\\nSusu TEH kopi\\n")
            assert frekuensi_baris(t) == [("kopi", 3), ("teh", 2), ("susu", 1)]
            assert frekuensi_baris(io.StringIO("")) == []
            assert frekuensi_baris(io.StringIO("b a b a c")) == [("a", 2), ("b", 2), ("c", 1)]
            """,
            "Hitung dengan dictionary lalu urutkan dengan key tuple negatif dan iris tiga.",
            """
            def frekuensi_baris(f):
                hitung = {}
                for b in f:
                    for k in b.lower().split():
                        hitung[k] = hitung.get(k, 0) + 1
                return sorted(hitung.items(), key=lambda p: (-p[1], p[0]))[:3]
            """,
        ),
    ],
    [
        M("Lupa menutup file.", "Pakai with agar file tertutup otomatis."),
        M("Memakai mode w padahal ingin menambah.", "Pakai mode a untuk menambah di akhir."),
        M("Lupa membuang karakter baris baru.", "Panggil strip atau rstrip pada tiap baris."),
    ],
    [
        Q("Mode yang menambah isi di akhir file?", ["r", "w", "a", "x"], 2, "Mode a berarti append.", hint="Singkatan append."),
        Q("Keuntungan utama with open?", ["Lebih cepat", "File ditutup otomatis", "Tidak perlu nama file", "Mengunci file"], 1, "Blok with menutup file bahkan saat error.", hint="Pikirkan sumber daya."),
        Q("Cara hemat memori membaca file besar?", ["f.read()", "f.readlines()", "for baris in f", "list(f)"], 2, "Menelusuri file memberi satu baris per putaran.", hint="Mirip generator."),
        Q("Error saat membuka file yang tidak ada dengan mode r?", ["KeyError", "FileNotFoundError", "ValueError", "IndexError"], 1, "FileNotFoundError ditimbulkan.", hint="Nama menjelaskan."),
        Q("Encoding yang aman untuk teks?", ["ascii", "utf-8", "latin", "bin"], 1, "UTF-8 mendukung hampir semua karakter.", hint="Standar universal."),
    ],
    [
        "Gunakan with open agar file otomatis tertutup.",
        "Mode r, w, a, dan x menentukan cara membuka file.",
        "Telusuri file baris demi baris untuk file besar.",
        "Tentukan encoding utf-8 dan tangani FileNotFoundError.",
    ],
    [],
)

l2 = lesson(
    "A1-07-2",
    "Bekerja dengan CSV",
    35,
    [
        "Membaca dan menulis CSV dengan modul csv",
        "Memakai DictReader dan DictWriter untuk data berlabel",
        "Mengubah tipe data dan menangani nilai kosong dan koma di dalam sel",
        "Meringkas data CSV dengan agregasi sederhana",
    ],
    [
        T("""
        ## Format CSV

        **CSV** (*comma-separated values*) adalah format tabel paling umum untuk pertukaran data. Setiap baris adalah satu rekaman dan nilai dalam baris dipisah koma. Baris pertama biasanya berisi nama kolom. Hampir semua alat, dari spreadsheet sampai basis data dan pandas, bisa membaca dan menulis CSV.

        Kelihatannya sederhana, tetapi ada jebakan. Nilai yang mengandung koma harus dikutip dengan tanda kutip ganda, tanda kutip di dalam nilai harus digandakan, dan nilai bisa mengandung baris baru. Karena itu **jangan** mengurai CSV dengan `split(",")` buatan sendiri. Gunakan modul `csv` yang menangani semua aturan itu dengan benar.

        Semua nilai dari CSV dibaca sebagai string. Mengubahnya menjadi angka atau tanggal adalah tugasmu, dan di sinilah banyak bug muncul bila data mengandung sel kosong atau format tak terduga.
        """),
        C(
            """
            import csv, io

            teks = "nama,kota,skor\\nSari,Depok,85\\nBudi,\\"Jakarta, Selatan\\",90\\nCitra,Bandung,\\n"
            for baris in csv.reader(io.StringIO(teks)):
                print(baris)
            print("Jakarta, Selatan".split(","))
            """,
            """
            ['nama', 'kota', 'skor']
            ['Sari', 'Depok', '85']
            ['Budi', 'Jakarta, Selatan', '90']
            ['Citra', 'Bandung', '']
            ['Jakarta', ' Selatan']
            """,
            """
            `csv.reader` menangani nilai berkutip yang mengandung koma, sedangkan `split` memecahnya keliru. Semua nilai dibaca sebagai string dan sel kosong menjadi string kosong.
            """,
            filename="csv_reader.py",
        ),
        T("""
        ## DictReader dan DictWriter

        `csv.DictReader` membaca tiap baris sebagai dictionary yang kuncinya diambil dari baris header. Ini jauh lebih terbaca daripada mengakses kolom lewat indeks, dan tidak rusak bila urutan kolom berubah. `csv.DictWriter` menulis dictionary menjadi baris CSV, dengan `fieldnames` menentukan urutan kolom dan `writeheader()` menulis baris header.

        Saat menulis ke file sungguhan, buka dengan `newline=""` agar modul csv mengatur baris baru sendiri, sehingga tidak muncul baris kosong ganda di Windows. Untuk menulis ke memori, `io.StringIO` bekerja sama persis.

        Pola kerja umum: baca dengan `DictReader`, ubah tipe tiap nilai, saring atau hitung, lalu tulis hasil dengan `DictWriter`. Ini versi mini dari alur baca, ubah, tulis yang akan kamu lakukan dengan pandas.
        """),
        C(
            """
            import csv, io

            teks = "nama,skor\\nSari,85\\nBudi,90\\nCitra,70\\n"
            baca = list(csv.DictReader(io.StringIO(teks)))
            print(baca[0], baca[0]["nama"])
            for r in baca:
                r["skor"] = int(r["skor"])
            print(sum(r["skor"] for r in baca) / len(baca))

            keluar = io.StringIO()
            tulis = csv.DictWriter(keluar, fieldnames=["nama", "skor", "lulus"], lineterminator="\\n")
            tulis.writeheader()
            for r in baca:
                tulis.writerow({**r, "lulus": r["skor"] >= 75})
            print(keluar.getvalue())
            """,
            """
            {'nama': 'Sari', 'skor': '85'} Sari
            81.66666666666667
            nama,skor,lulus
            Sari,85,True
            Budi,90,True
            Citra,70,False
            """,
            """
            `DictReader` membaca baris sebagai dictionary berkunci header. Nilai diubah ke `int` secara manual dan `DictWriter` menulis kolom baru.
            """,
            filename="csv_dict.py",
        ),
        K(
            "warning",
            """
            Semua nilai CSV dibaca sebagai string. `"10" + "5"` menghasilkan `"105"`, bukan 15. Ubah dulu dengan `int` atau `float`.
            """,
            title="Semua nilai adalah teks",
        ),
        T("""
        ## Menangani sel kosong dan data kotor

        Data nyata penuh sel kosong, spasi tersembunyi, dan nilai tidak valid seperti `"n/a"` atau `"-"`. Langkah aman adalah membungkus konversi dalam fungsi pembantu yang mengembalikan `None` bila gagal, lalu memutuskan secara sadar bagaimana memperlakukan `None`: dilewati, diisi nilai bawaan, atau menghentikan proses.

        Jangan menelan semua error tanpa mencatat. Hitung berapa baris yang gagal dikonversi dan laporkan, karena jumlah data hilang memengaruhi kesimpulan analisismu. Mengabaikan diam-diam adalah cara tercepat mendapat hasil yang salah namun terlihat meyakinkan.

        Pustaka pandas nanti menyediakan penanganan nilai hilang yang jauh lebih kaya, tetapi dasarnya sama: kenali nilai hilang, putuskan strateginya, dan dokumentasikan keputusan itu.
        """),
        C(
            """
            import csv, io

            def ke_angka(s):
                s = s.strip()
                try:
                    return float(s)
                except ValueError:
                    return None

            teks = "id,harga\\n1,100\\n2,\\n3, 250 \\n4,n/a\\n5,75.5\\n"
            baris = list(csv.DictReader(io.StringIO(teks)))
            harga = [ke_angka(r["harga"]) for r in baris]
            print(harga)
            valid = [h for h in harga if h is not None]
            print(len(valid), len(baris) - len(valid), sum(valid) / len(valid))
            """,
            """
            [100.0, None, 250.0, None, 75.5]
            3 2 141.83333333333334
            """,
            """
            Fungsi pembantu mengembalikan `None` untuk nilai tak valid. Jumlah baris yang gagal dihitung dan dilaporkan, bukan diabaikan diam-diam.
            """,
            filename="csv_kotor.py",
        ),
        T("""
        ## Agregasi sederhana dari CSV

        Setelah data dibaca dan dibersihkan, kamu bisa meringkasnya dengan pola dictionary yang sudah dikenal: kelompokkan baris menurut satu kolom lalu hitung jumlah, rata-rata, atau maksimum per kelompok. Ini setara dengan `groupby` di pandas atau `GROUP BY` di SQL.

        Pola dasarnya: telusuri baris, ambil kunci kelompok, lalu akumulasikan nilai di dictionary. Untuk rata-rata, simpan jumlah dan banyaknya, lalu bagi di akhir. Hati-hati dengan pembagian nol bila kelompok bisa kosong.

        Meski pandas membuat ini sangat ringkas, memahami versi manualnya membuatmu mengerti apa yang sebenarnya terjadi dan membantumu men-debug hasil yang mengejutkan. Latihan berikut membangun ringkasan seperti itu dari data CSV dalam memori.
        """),
        T("""
        ## Kapan CSV tidak cukup

        CSV hebat untuk tabel datar, tetapi tidak menyimpan tipe data, tidak punya skema, dan canggung untuk struktur bersarang. Tanggal bisa ditulis dalam puluhan format, angka desimal memakai titik atau koma tergantung wilayah, dan tidak ada cara baku menandai nilai hilang. Karena itu selalu periksa beberapa baris awal file baru sebelum memproses seluruhnya.

        Untuk data besar atau yang butuh tipe tegas, format lain seperti Parquet atau basis data lebih tepat. Namun CSV tetap menjadi bahasa pertukaran universal, jadi menguasainya adalah keharusan. Kebiasaan baik: simpan file mentah tanpa diubah, lakukan pembersihan dalam kode yang bisa diulang, dan tulis hasil bersih ke file terpisah.

        Latihan berikut memakai teks CSV dalam memori sehingga bisa dijalankan di mana saja. Perhatikan setiap kasus batas: file hanya berisi header, sel kosong, dan nilai berkutip.
        """),
        E(
            "A1-07-2-ex1",
            "mudah",
            """
            Tulis fungsi `baca_csv(teks)` yang mengembalikan list dictionary dari teks CSV berheader.
            """,
            """
            import csv, io

            def baca_csv(teks):
                # TODO: implementasikan
                pass
            """,
            """
            t = "a,b\\n1,2\\n3,4\\n"
            assert baca_csv(t) == [{"a": "1", "b": "2"}, {"a": "3", "b": "4"}]
            assert baca_csv("a,b\\n") == []
            assert baca_csv('x,y\\n"p,q",z\\n') == [{"x": "p,q", "y": "z"}]
            """,
            "Bungkus teks dengan io.StringIO dan pakai DictReader.",
            """
            import csv, io

            def baca_csv(teks):
                return list(csv.DictReader(io.StringIO(teks)))
            """,
        ),
        E(
            "A1-07-2-ex2",
            "mudah",
            """
            Tulis fungsi `rata_kolom(teks, kolom)` yang mengembalikan rata-rata nilai numerik kolom `kolom` dari teks CSV berheader. Semua nilai valid dan ada minimal satu baris.
            """,
            """
            import csv, io

            def rata_kolom(teks, kolom):
                # TODO: implementasikan
                pass
            """,
            """
            t = "nama,skor\\nA,80\\nB,90\\nC,70\\n"
            assert rata_kolom(t, "skor") == 80
            assert rata_kolom("x\\n1\\n2\\n", "x") == 1.5
            assert rata_kolom("x\\n5\\n", "x") == 5
            """,
            "Baca dengan DictReader lalu ubah ke float dan rata-ratakan.",
            """
            import csv, io

            def rata_kolom(teks, kolom):
                nilai = [float(r[kolom]) for r in csv.DictReader(io.StringIO(teks))]
                return sum(nilai) / len(nilai)
            """,
        ),
        E(
            "A1-07-2-ex3",
            "sedang",
            """
            Tulis fungsi `total_per_kota(teks)` yang menerima CSV dengan kolom `kota` dan `jumlah`, dan mengembalikan dictionary kota ke total jumlah (int). Baris dengan jumlah kosong atau bukan angka dilewati.
            """,
            """
            import csv, io

            def total_per_kota(teks):
                # TODO: implementasikan
                pass
            """,
            """
            t = "kota,jumlah\\nDepok,5\\nBogor,3\\nDepok,2\\nBogor,\\nBekasi,x\\n"
            assert total_per_kota(t) == {"Depok": 7, "Bogor": 3}
            assert total_per_kota("kota,jumlah\\n") == {}
            assert total_per_kota("kota,jumlah\\nA, 4 \\n") == {"A": 4}
            """,
            "Coba ubah ke int dalam try dan lewati bila ValueError.",
            """
            import csv, io

            def total_per_kota(teks):
                hasil = {}
                for r in csv.DictReader(io.StringIO(teks)):
                    try:
                        n = int(r["jumlah"].strip())
                    except ValueError:
                        continue
                    hasil[r["kota"]] = hasil.get(r["kota"], 0) + n
                return hasil
            """,
        ),
        E(
            "A1-07-2-ex4",
            "menantang",
            """
            Tulis fungsi `ke_csv(baris, kolom)` yang menerima list dictionary dan list nama kolom dan mengembalikan teks CSV dengan header, memakai `csv.DictWriter` dan `lineterminator="\\n"`. Kunci yang tidak ada diisi kosong.
            """,
            """
            import csv, io

            def ke_csv(baris, kolom):
                # TODO: implementasikan
                pass
            """,
            """
            r = [{"a": 1, "b": "x,y"}, {"a": 2}]
            assert ke_csv(r, ["a", "b"]) == 'a,b\\n1,"x,y"\\n2,\\n'
            assert ke_csv([], ["a"]) == "a\\n"
            assert ke_csv([{"a": 1, "z": 9}], ["a"]) == "a\\n1\\n"
            """,
            "Tulis ke StringIO dengan DictWriter dan ambil getvalue. Gunakan restval kosong dan extrasaction ignore.",
            """
            import csv, io

            def ke_csv(baris, kolom):
                out = io.StringIO()
                w = csv.DictWriter(out, fieldnames=kolom, lineterminator="\\n", extrasaction="ignore")
                w.writeheader()
                w.writerows(baris)
                return out.getvalue()
            """,
        ),
    ],
    [
        M("Mengurai CSV dengan split koma.", "Pakai modul csv agar nilai berkutip benar."),
        M("Menjumlahkan nilai CSV tanpa mengubah tipe.", "Ubah dengan int atau float lebih dulu."),
        M("Mengabaikan baris rusak tanpa menghitung.", "Hitung dan laporkan jumlah baris yang gagal."),
    ],
    [
        Q("Tipe nilai yang dibaca dari CSV?", ["int", "float", "str", "otomatis"], 2, "Semua nilai dibaca sebagai string.", hint="Konversi manual."),
        Q("Keunggulan DictReader?", ["Lebih cepat", "Baris menjadi dictionary berkunci header", "Mengubah tipe otomatis", "Mengurutkan"], 1, "Akses kolom lewat nama.", hint="Header jadi kunci."),
        Q("Mengapa tidak memakai split koma?", ["Lambat", "Nilai berkutip bisa mengandung koma", "Tidak ada split", "Error"], 1, "Koma di dalam kutip tidak boleh memecah.", hint="Lihat contoh Jakarta, Selatan."),
        Q("Nilai kembalian fungsi konversi yang gagal sebaiknya?", ["0", "None", "error diam", "string kosong"], 1, "None menandai nilai hilang secara eksplisit.", hint="Beda dari nol."),
        Q("Operasi yang setara groupby?", ["Mengelompokkan baris lalu agregasi", "Mengurutkan", "Menyaring", "Menulis"], 0, "Kelompokkan menurut kolom lalu hitung per kelompok.", hint="GROUP BY di SQL."),
    ],
    [
        "CSV adalah tabel teks dan semua nilainya dibaca sebagai string.",
        "Gunakan modul csv, bukan split, untuk menangani kutip dan koma.",
        "DictReader dan DictWriter bekerja dengan dictionary berlabel.",
        "Tangani sel kosong secara sadar dan laporkan data yang hilang.",
    ],
    [],
)

l3 = lesson(
    "A1-07-3",
    "JSON dan serialisasi",
    35,
    [
        "Mengubah antara string JSON dan objek Python dengan json.loads dan json.dumps",
        "Memakai indent, sort_keys, dan ensure_ascii untuk keluaran yang rapi",
        "Membaca dan menulis file JSON dengan json.load dan json.dump",
        "Menangani tipe yang tidak didukung dan meratakan JSON bersarang",
    ],
    [
        T("""
        ## JSON sebagai bahasa data

        **JSON** (*JavaScript Object Notation*) adalah format teks untuk data terstruktur. Hampir semua API web mengirim dan menerima JSON, dan banyak file konfigurasi memakainya. Bentuknya mirip dictionary dan list Python: objek dengan kunci berupa string, array, string, angka, `true`, `false`, dan `null`.

        Modul `json` mengonversi dua arah. `json.loads(teks)` mengubah string JSON menjadi objek Python, dan `json.dumps(objek)` mengubah objek Python menjadi string JSON. Versi tanpa huruf s, `json.load(file)` dan `json.dump(objek, file)`, bekerja langsung dengan objek file. Cara mengingatnya: huruf s berarti string.

        Pemetaan tipe penting diketahui: objek menjadi dictionary, array menjadi list, `true` dan `false` menjadi `True` dan `False`, serta `null` menjadi `None`. Kunci JSON selalu string, sehingga kunci bilangan di dictionary berubah menjadi string setelah melewati JSON.
        """),
        C(
            """
            import json

            teks = '{"nama": "Sari", "umur": 21, "aktif": true, "skor": null, "tag": ["a", "b"]}'
            d = json.loads(teks)
            print(d["nama"], d["aktif"], d["skor"], d["tag"][1], type(d).__name__)

            obj = {"x": 1, "ok": True, "kosong": None, "daftar": [1, 2.5]}
            s = json.dumps(obj)
            print(s)
            print(type(s).__name__)
            print(json.loads(json.dumps({1: "a"})))
            """,
            """
            Sari True None b dict
            {"x": 1, "ok": true, "kosong": null, "daftar": [1, 2.5]}
            str
            {'1': 'a'}
            """,
            """
            `loads` mengurai string JSON dan `dumps` menghasilkan string JSON. Kunci bilangan berubah menjadi string setelah melewati JSON.
            """,
            filename="json_dasar.py",
        ),
        T("""
        ## Merapikan keluaran

        `json.dumps` secara bawaan menghasilkan satu baris padat. Argumen `indent=2` membuatnya berlekuk sehingga mudah dibaca manusia, `sort_keys=True` mengurutkan kunci agar keluaran stabil dan mudah dibandingkan, dan `ensure_ascii=False` mempertahankan karakter non-ASCII seperti huruf beraksen alih-alih mengubahnya menjadi kode `\\uXXXX`.

        Keluaran yang stabil sangat berguna saat menyimpan konfigurasi dalam kendali versi atau membandingkan dua hasil dengan teks. Kunci yang selalu terurut berarti dua dictionary yang sama isinya menghasilkan teks yang sama.

        Untuk mengirim data kecil antar program, bentuk padat sudah cukup. Untuk file yang akan dibaca manusia, pakai `indent`. Pilih sesuai pembacanya.
        """),
        C(
            """
            import json

            data = {"kota": "Yogyakarta", "tag": ["b", "a"], "nama": "José", "angka": 3}
            print(json.dumps(data, sort_keys=True))
            print(json.dumps({"a": 1, "b": [1, 2]}, indent=2))
            print(json.dumps({"n": "José"}))
            print(json.dumps({"n": "José"}, ensure_ascii=False))
            a = json.dumps({"x": 1, "y": 2}, sort_keys=True)
            b = json.dumps({"y": 2, "x": 1}, sort_keys=True)
            print(a == b)
            """,
            """
            {"angka": 3, "kota": "Yogyakarta", "nama": "Jos\\u00e9", "tag": ["b", "a"]}
            {
              "a": 1,
              "b": [
                1,
                2
              ]
            }
            {"n": "Jos\\u00e9"}
            {"n": "José"}
            True
            """,
            """
            `sort_keys` menstabilkan keluaran, `indent` merapikannya, dan `ensure_ascii=False` mempertahankan huruf beraksen.
            """,
            filename="json_format.py",
        ),
        K(
            "tip",
            """
            Ingat dengan huruf s: `loads` dan `dumps` bekerja dengan string, sedangkan `load` dan `dump` bekerja dengan objek file.
            """,
            title="Mengingat load dan loads",
        ),
        T("""
        ## File JSON dan tipe yang tidak didukung

        Untuk menyimpan ke file, buka dengan `with open("data.json", "w", encoding="utf-8") as f:` lalu `json.dump(obj, f, indent=2, ensure_ascii=False)`. Membacanya kembali dengan `json.load(f)`. Pola baca dan tulis ini dipakai untuk menyimpan hasil antara dan konfigurasi.

        Tidak semua objek Python bisa diubah ke JSON. Himpunan (`set`), tuple dengan perilaku khusus, tanggal, dan objek buatan sendiri tidak didukung langsung. Tuple menjadi array dan kembali sebagai list, sedangkan `set` menimbulkan `TypeError`. Solusinya mengubah dulu menjadi tipe yang didukung, misalnya `sorted(set)` menjadi list, atau memberi argumen `default=` berupa fungsi yang menjelaskan cara mengonversi.

        Perhatikan juga bahwa JSON tidak membedakan bilangan bulat dan desimal secara ketat, serta tidak mendukung `NaN` dan tak hingga menurut standar. Python mengizinkannya secara bawaan, tetapi program lain bisa menolaknya.
        """),
        C(
            """
            import json

            with open("data.json", "w", encoding="utf-8") as f:
                json.dump({"nama": "Sari", "nilai": [90, 85]}, f, indent=2)
            with open("data.json", encoding="utf-8") as f:
                kembali = json.load(f)
            print(kembali, kembali["nilai"][0])

            try:
                json.dumps({"s": {1, 2}})
            except TypeError:
                print("set tidak didukung")
            print(json.dumps({"s": sorted({2, 1})}))
            print(json.dumps({"t": (1, 2)}), json.loads('{"t": [1, 2]}'))
            print(json.dumps({"s": {3, 1}}, default=sorted))
            """,
            """
            {'nama': 'Sari', 'nilai': [90, 85]} 90
            set tidak didukung
            {"s": [1, 2]}
            {"t": [1, 2]} {'t': [1, 2]}
            {"s": [1, 3]}
            """,
            """
            `dump` dan `load` bekerja dengan file. Set tidak didukung langsung sehingga diubah ke list atau diberi `default`.
            """,
            filename="json_file.py",
        ),
        T("""
        ## Meratakan JSON bersarang

        Data dari API biasanya bersarang: objek berisi objek dan array. Untuk dianalisis sebagai tabel, struktur ini perlu diratakan. Pendekatan umum: telusuri struktur secara rekursif, gabungkan kunci bertingkat dengan pemisah seperti titik, dan hasilkan satu dictionary datar.

        Misalnya `{"a": {"b": 1}}` menjadi `{"a.b": 1}`. Array biasanya diperlakukan terpisah: bisa dijadikan satu sel, atau dipecah menjadi beberapa baris. Pilihan bergantung pada tujuan analisis. Pustaka pandas menyediakan `json_normalize` untuk ini, tetapi memahami versi manualnya membantumu mengatasi kasus yang tidak tertangani otomatis.

        Berhati-hatilah dengan JSON dari sumber tidak tepercaya. Parsing JSON sendiri aman, tetapi isinya bisa tidak sesuai harapan. Validasi bentuk data sebelum memakainya, dan jangan pernah mengevaluasinya sebagai kode.
        """),
        T("""
        ## Pola kerja dengan API

        Saat mengambil data dari API, alurnya hampir selalu sama: kirim permintaan, terima teks JSON, urai dengan `json.loads`, periksa bentuknya, lalu ekstrak bagian yang kamu butuhkan. Jangan berasumsi kunci selalu ada. Gunakan `get` dengan nilai bawaan atau tangkap `KeyError`, karena API sering mengubah atau menghilangkan kolom opsional.

        Simpan respons mentah ke file sebelum mengolahnya. Bila ada bug di kodemu, kamu tidak perlu memanggil API lagi, dan kamu bisa membandingkan hasil dari waktu ke waktu. Kebiasaan ini juga menghemat kuota panggilan yang sering dibatasi.

        Latihan berikut tidak memakai jaringan, hanya string JSON di memori. Itu cukup untuk melatih semua keterampilan penguraian dan perataan yang kamu butuhkan nanti saat bekerja dengan data nyata.

        Satu pesan terakhir: selalu tangani kegagalan penguraian. Teks yang bukan JSON valid akan menimbulkan galat, dan program yang baik menanganinya dengan jelas.
        """),
        E(
            "A1-07-3-ex1",
            "mudah",
            """
            Tulis fungsi `ambil_nama(teks)` yang menerima string JSON objek dan mengembalikan nilai kunci `nama`, atau `None` bila tidak ada.
            """,
            """
            import json

            def ambil_nama(teks):
                # TODO: implementasikan
                pass
            """,
            """
            assert ambil_nama('{"nama": "Sari"}') == "Sari"
            assert ambil_nama('{"umur": 3}') is None
            assert ambil_nama('{"nama": null}') is None
            """,
            "Urai dengan json.loads lalu gunakan get.",
            """
            import json

            def ambil_nama(teks):
                return json.loads(teks).get("nama")
            """,
        ),
        E(
            "A1-07-3-ex2",
            "mudah",
            """
            Tulis fungsi `ke_json(obj)` yang mengembalikan string JSON dengan kunci terurut dan tanpa mengubah karakter non-ASCII.
            """,
            """
            import json

            def ke_json(obj):
                # TODO: implementasikan
                pass
            """,
            """
            assert ke_json({"b": 1, "a": 2}) == '{"a": 2, "b": 1}'
            assert ke_json({"n": "é"}) == '{"n": "é"}'
            assert ke_json([]) == "[]"
            """,
            "Pakai sort_keys=True dan ensure_ascii=False.",
            """
            import json

            def ke_json(obj):
                return json.dumps(obj, sort_keys=True, ensure_ascii=False)
            """,
        ),
        E(
            "A1-07-3-ex3",
            "sedang",
            """
            Tulis fungsi `aman_json(teks, bawaan=None)` yang mengurai string JSON dan mengembalikan hasilnya, tetapi mengembalikan `bawaan` bila teks bukan JSON yang valid.
            """,
            """
            import json

            def aman_json(teks, bawaan=None):
                # TODO: implementasikan
                pass
            """,
            """
            assert aman_json('{"a": 1}') == {"a": 1}
            assert aman_json("bukan json") is None
            assert aman_json("{rusak", bawaan={}) == {}
            assert aman_json("[1, 2]") == [1, 2]
            assert aman_json("") is None
            """,
            "Tangkap json.JSONDecodeError atau ValueError.",
            """
            import json

            def aman_json(teks, bawaan=None):
                try:
                    return json.loads(teks)
                except ValueError:
                    return bawaan
            """,
        ),
        E(
            "A1-07-3-ex4",
            "menantang",
            """
            Tulis fungsi `ratakan(d, awalan="")` yang meratakan dictionary bersarang menjadi satu dictionary datar dengan kunci digabung titik. Nilai bukan dictionary (termasuk list) dibiarkan apa adanya. Contoh `{"a": {"b": 1, "c": {"d": 2}}, "e": 3}` menjadi `{"a.b": 1, "a.c.d": 2, "e": 3}`.
            """,
            """
            def ratakan(d, awalan=""):
                # TODO: implementasikan
                pass
            """,
            """
            assert ratakan({"a": {"b": 1, "c": {"d": 2}}, "e": 3}) == {"a.b": 1, "a.c.d": 2, "e": 3}
            assert ratakan({}) == {}
            assert ratakan({"x": [1, 2]}) == {"x": [1, 2]}
            assert ratakan({"a": {}}) == {}
            assert ratakan({"p": {"q": None}}) == {"p.q": None}
            """,
            "Telusuri items dan rekursif untuk nilai dictionary dengan awalan kunci.",
            """
            def ratakan(d, awalan=""):
                hasil = {}
                for k, v in d.items():
                    kunci = awalan + "." + k if awalan else k
                    if isinstance(v, dict):
                        hasil.update(ratakan(v, kunci))
                    else:
                        hasil[kunci] = v
                return hasil
            """,
        ),
    ],
    [
        M("Mengira loads membaca file.", "loads untuk string, load untuk objek file."),
        M("Menyimpan set langsung ke JSON.", "Ubah ke list terurut atau beri default."),
        M("Mengharapkan kunci bilangan tetap bilangan.", "Kunci JSON selalu string."),
    ],
    [
        Q("Fungsi untuk mengubah string JSON menjadi objek Python?", ["json.dumps", "json.loads", "json.dump", "json.read"], 1, "loads mengurai string.", hint="s untuk string."),
        Q("JSON null menjadi apa di Python?", ["0", "False", "None", "''"], 2, "null dipetakan ke None.", hint="Nilai kosong."),
        Q("Argumen untuk keluaran berlekuk?", ["pretty", "indent", "format", "space"], 1, "indent mengatur lekukan.", hint="Menjorok."),
        Q("Apa yang terjadi bila dumps menerima set?", ["Jadi list", "TypeError", "Jadi string", "Diabaikan"], 1, "Set tidak didukung.", hint="Perlu konversi."),
        Q("Fungsi untuk menulis objek ke file JSON?", ["json.dumps", "json.dump", "json.write", "json.save"], 1, "dump menulis ke objek file.", hint="Tanpa s."),
    ],
    [
        "loads dan dumps bekerja dengan string, load dan dump dengan file.",
        "indent, sort_keys, dan ensure_ascii merapikan keluaran.",
        "Set dan tipe khusus perlu dikonversi sebelum menjadi JSON.",
        "JSON bersarang diratakan dengan rekursi.",
    ],
    [],
)

video = {"needed": False, "kind": "none", "reason": "Isi modul berupa kode dan contoh singkat yang cukup jelas dalam teks dan latihan.", "brief": []}

write_module(
    "A1",
    7,
    "File I/O, CSV, dan JSON",
    105,
    [
        "Membaca dan menulis file teks dengan aman",
        "Mengolah data tabular dengan modul csv",
        "Mengubah data dari dan ke JSON",
    ],
    [l1, l2, l3],
    video,
    REF,
)
