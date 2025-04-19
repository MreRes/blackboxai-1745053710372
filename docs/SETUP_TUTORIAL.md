# WhatsApp AI Financial Planner Assistant Setup Tutorial

## English Version

This tutorial will guide you step-by-step to set up and run the WhatsApp AI Financial Planner Assistant project. It is designed to be beginner-friendly and includes common error handling tips.

### Prerequisites

- Python 3.11.0 installed on your system. Download from [python.org](https://www.python.org/downloads/).
- Google Chrome browser installed.
- Internet connection to download dependencies and ChromeDriver.

### Step 1: Clone or Download the Project

Download the project files or clone the repository to your local machine.

### Step 2: Install Python Packages

Open a terminal or command prompt in the project directory and run:

```
pip install -r requirements.txt
```

This installs all required Python packages including Flask, Selenium, transformers, and webdriver-manager.

### Step 3: Run the WhatsApp Bot

Run the WhatsApp bot with:

```
python whatsapp_bot.py
```

- The bot will automatically download the correct ChromeDriver version matching your installed Chrome browser.
- A Chrome window will open with WhatsApp Web.
- Scan the QR code with your WhatsApp mobile app to log in.
- The bot will listen for incoming messages and process financial transactions.

### Step 4: Run the Web Application

In a new terminal, run:

```
python web_app.py
```

- Open your browser and go to `http://localhost:5000` to access the dashboard.
- Use the navigation menu to view transactions, budgets, goals, reports, and manage contacts.

### Common Errors and Troubleshooting

- **ChromeDriver download issues:** Ensure you have internet access. If download fails, check firewall or proxy settings.
- **WhatsApp login issues:** If QR code does not appear or login fails, delete the `User_Data` folder and restart the bot.
- **Port conflicts:** If port 5000 is in use, stop the conflicting service or change the port in `web_app.py`.
- **Python package errors:** Make sure all packages are installed correctly using `pip install -r requirements.txt`.
- **Permission errors:** Run terminal or command prompt with administrator or appropriate permissions.
- **Database errors:** Check if `financial_data.db` is accessible and not corrupted.

For detailed logs, check `financial_planner.log`.

---

## Versi Bahasa Indonesia

Tutorial ini akan memandu Anda langkah demi langkah untuk mengatur dan menjalankan proyek WhatsApp AI Financial Planner Assistant. Tutorial ini dirancang agar mudah dipahami pemula dan menyertakan tips penanganan error umum.

### Persyaratan

- Python 3.11.0 sudah terpasang di sistem Anda. Unduh dari [python.org](https://www.python.org/downloads/).
- Browser Google Chrome sudah terpasang.
- Koneksi internet untuk mengunduh dependensi dan ChromeDriver.

### Langkah 1: Unduh atau Clone Proyek

Unduh file proyek atau clone repository ke komputer Anda.

### Langkah 2: Instal Paket Python

Buka terminal atau command prompt di direktori proyek dan jalankan:

```
pip install -r requirements.txt
```

Ini akan menginstal semua paket Python yang dibutuhkan termasuk Flask, Selenium, transformers, dan webdriver-manager.

### Langkah 3: Jalankan WhatsApp Bot

Jalankan bot WhatsApp dengan:

```
python whatsapp_bot.py
```

- Bot akan otomatis mengunduh versi ChromeDriver yang sesuai dengan browser Chrome yang terpasang.
- Jendela Chrome akan terbuka dengan WhatsApp Web.
- Pindai kode QR dengan aplikasi WhatsApp di ponsel Anda untuk login.
- Bot akan mendengarkan pesan masuk dan memproses transaksi keuangan.

### Langkah 4: Jalankan Aplikasi Web

Di terminal baru, jalankan:

```
python web_app.py
```

- Buka browser dan akses `http://localhost:5000` untuk melihat dashboard.
- Gunakan menu navigasi untuk melihat transaksi, anggaran, tujuan, laporan, dan mengelola kontak.

### Error Umum dan Cara Mengatasinya

- **Masalah pengunduhan ChromeDriver:** Pastikan koneksi internet aktif. Jika gagal, periksa pengaturan firewall atau proxy.
- **Masalah login WhatsApp:** Jika kode QR tidak muncul atau login gagal, hapus folder `User_Data` dan restart bot.
- **Port sudah digunakan:** Jika port 5000 sudah dipakai, hentikan layanan yang menggunakan port tersebut atau ubah port di `web_app.py`.
- **Error paket Python:** Pastikan semua paket terinstal dengan benar menggunakan `pip install -r requirements.txt`.
- **Error izin akses:** Jalankan terminal atau command prompt dengan hak administrator atau izin yang sesuai.
- **Error database:** Periksa apakah `financial_data.db` dapat diakses dan tidak korup.

Untuk log detail, periksa file `financial_planner.log`.

---

If you need further help, feel free to open an issue or contact the maintainer.

Jika Anda membutuhkan bantuan lebih lanjut, silakan buka issue atau hubungi maintainer.
