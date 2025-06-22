# FP-GES

Repositori ini merupakan proyek tugas akhir (Final Project) yang dikembangkan oleh tim pada mata kuliah Game Edukasi dan Simulasi. Proyek ini dibuat menggunakan Ren'Py, sebuah engine visual novel berbasis Python, dengan struktur direktori yang dioptimalkan untuk pengembangan game visual novel.

## Daftar Isi

- [Deskripsi Proyek](#deskripsi-proyek)
- [Fitur](#fitur)
- [Instalasi](#instalasi)
- [Penggunaan](#penggunaan)
- [Struktur Direktori](#struktur-direktori)
- [Kontributor](#kontributor)
- [Lisensi](#lisensi)

## Deskripsi Proyek

FP-GES adalah singkatan dari Final Project - The Librarians Path. Proyek ini dibuat untuk memenuhi tugas akhir pada Game Edukasi & Simulasi. Game ini bertujuan untuk memberikan pengalaman interaktif berbasis cerita dengan multimedia.

## Fitur

- Cerita visual interaktif berbasis Ren'Py.
- Audio latar dan efek suara mendukung suasana permainan.
- Berbagai pilihan menu dan opsi yang mempengaruhi alur cerita.
- Sistem penyimpanan (save) dan pemuatan (load) progress pemain.

**Silakan tambah atau ubah fitur sesuai kebutuhan proyek Anda.**

## Instalasi

Pastikan sudah menginstal [Ren'Py](https://www.renpy.org/) versi terbaru.

1. Clone repositori ini:
   ```bash
   git clone https://github.com/Lyradd/FP-GES.git
   cd FP-GES
   ```

2. Jalankan Ren'Py dan buka folder proyek ini untuk memulai pengembangan atau menjalankan game.

## Penggunaan

- Buka Ren'Py, impor folder `FP-GES` sebagai proyek baru.
- Klik "Launch Project" pada Ren'Py Launcher untuk menjalankan game.
- Untuk mengedit cerita atau aset, ubah file yang ada di dalam folder `game`.

## Struktur Direktori

Struktur direktori utama proyek ini adalah sebagai berikut:

![image](https://github.com/user-attachments/assets/fe114808-63f4-453d-a23e-f1a9a18312ce)

Penjelasan struktur:
- `.vscode/`           : Konfigurasi editor (opsional).
- `game/`              : Folder utama aset dan script game.
  - `audio/`           : Menyimpan file audio seperti musik dan efek suara.
  - `fonts/`           : Menyimpan file font (jika ada).
  - `gui/`             : Komponen antarmuka pengguna.
  - `images/`          : Menyimpan gambar dan sprite.
  - `saves/`           : Data penyimpanan progress pemain.
  - `tl/`              : Untuk terjemahan atau localization (optional).
  - `custom_screens.rpy` : Script custom untuk layar-layar tambahan.
  - `definitions.rpy`    : Definisi variabel dan data global.
  - `gui.rpy`            : Script pengaturan GUI.
  - `images.rpy`         : Script pengaturan gambar.
  - `options.rpy`        : Konfigurasi pengaturan game.
  - `screens.rpy`        : Definisi tampilan layar custom.
  - `script.rpy`         : Script utama cerita visual novel.
- `errors.txt`, `log.txt`, `traceback.txt` : File log dan error untuk debugging.

## Kontributor

- [Nama Kontributor 1](https://github.com/username1)
- [Nama Kontributor 2](https://github.com/username2)
- [Nama Kontributor 3](https://github.com/username3)


---

> _Silakan lengkapi bagian yang masih kosong atau sesuaikan dengan kebutuhan proyek Anda._
