import json
import os

MONGO_FILE = 'database/mongodb_data.json'
REDIS_FILE = 'database/redis_data.json'

def load_data(filepath):
    """Membaca data dari file JSON."""
    if not os.path.exists(filepath):
        return [] if 'mongo' in filepath else {}
    with open(filepath, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return [] if 'mongo' in filepath else {}

def save_data(filepath, data):
    """Menyimpan data ke file JSON."""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

def buat_catatan():
    print("\n--- TULIS CATATAN BARU ---")
    judul = input("Judul: ")
    isi = input("Isi: ")
    
    # 1. Simpan ke Database Utama (MongoDB)
    mongo_data = load_data(MONGO_FILE)
    new_note = {
        "id": len(mongo_data) + 1,
        "judul": judul,
        "isi": isi,
        "views": 0  # Catatan baru belum ada yang lihat
    }
    mongo_data.append(new_note)
    save_data(MONGO_FILE, mongo_data)
    print("✅ Catatan berhasil disimpan ke MongoDB (Permanen).")
    
    # 2. Hapus Cache (Cache Invalidation)
    # Karena ada data baru, cache lama di Redis harus dihapus agar tidak menampilkan data basi.
    save_data(REDIS_FILE, {})
    print("🔄 Cache di Redis dikosongkan (Cache Invalidated).")

def lihat_catatan_populer():
    print("\n--- MENCARI CATATAN POPULER ---")
    
    # 1. Cek di Cache (Redis) terlebih dahulu
    redis_data = load_data(REDIS_FILE)
    
    if "populer" in redis_data and redis_data["populer"]:
        # CACHE HIT: Data ditemukan di Redis, proses sangat cepat.
        print("⚡ [CACHE HIT] Mengambil data dari Redis (Cepat!)")
        catatan = redis_data["populer"]
    else:
        # CACHE MISS: Data tidak ada di Redis, harus ambil dari MongoDB.
        print("🐌 [CACHE MISS] Data tidak ada di cache. Mengambil dari MongoDB...")
        mongo_data = load_data(MONGO_FILE)
        
        # Simulasi proses berat: Mengurutkan semua data berdasarkan views tertinggi
        catatan = sorted(mongo_data, key=lambda x: x.get("views", 0), reverse=True)[:3]
        
        # 2. Simpan hasil query ke Cache (Redis) untuk pencarian berikutnya
        redis_data["populer"] = catatan
        save_data(REDIS_FILE, redis_data)
        print("💾 Hasil pencarian disimpan ke Redis untuk request selanjutnya.")
        
    # Tampilkan hasil
    print("\n⭐ TOP CATATAN POPULER ⭐")
    for idx, c in enumerate(catatan, 1):
        print(f"{idx}. {c['judul']} ({c.get('views', 0)} views)")

def main():
    # Pastikan folder database ada
    os.makedirs('database', exist_ok=True)
    
    while True:
        print("\n=== 📝 APLIKASI CATATAN POPULER ===")
        print("1. Buat Catatan Baru")
        print("2. Lihat Catatan Populer")
        print("3. Keluar")
        pilihan = input("Pilih menu (1/2/3): ")
        
        if pilihan == '1':
            buat_catatan()
        elif pilihan == '2':
            lihat_catatan_populer()
        elif pilihan == '3':
            print("👋 Keluar dari aplikasi. Sampai jumpa!")
            break
        else:
            print("❌ Pilihan tidak valid.")

if __name__ == "__main__":
    main()