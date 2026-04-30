# Simulasi Aplikasi Catatan Populer (MongoDB & Redis)

Aplikasi ini adalah simulasi sederhana berbasis Python (`app.py`) untuk mendemonstrasikan konsep **Database Utama** (MongoDB) dan **In-Memory Cache** (Redis) menggunakan file JSON.

## Konsep yang Didemonstrasikan:
1. **Penyimpanan Permanen (MongoDB):** Saat *user* membuat catatan baru, data disimpan dengan aman di `mongodb_data.json`.
2. **Cache Hit & Cache Miss (Redis):**
   - Saat *user* memilih menu "Lihat Catatan Populer" untuk pertama kalinya, terjadi **Cache Miss**. Sistem harus membaca data dari MongoDB, melakukan proses pengurutan (*sorting*), lalu menyimpannya ke `redis_data.json`.
   - Jika *user* melihat catatan populer lagi, terjadi **Cache Hit**. Sistem langsung mengambil data dari Redis tanpa perlu mengakses MongoDB atau melakukan pengurutan ulang. Ini menyimulasikan performa pembacaan yang sangat cepat.
3. **Cache Invalidation:** Jika ada catatan baru yang ditambahkan ke MongoDB, sistem secara otomatis akan mengosongkan file `redis_data.json`. Hal ini penting untuk memastikan *user* tidak melihat data yang sudah usang (*stale data*).

## Cara Menjalankan
Buka terminal dan jalankan perintah:
```bash
python app.py