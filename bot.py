# Membuat file bot.py
bot_code = '''import os
import requests
import time
import random
import string

# Mengambil token dari Environment Variables Render (aman dan rahasia)
TOKEN = os.getenv("TOKEN", "8845983211:AAEMiQlM2p4DpRBrhjq9qlEvYKLPW-XdaH8")
TOKEN = TOKEN.strip()

DANA_LINK = "https://link.dana.id/minta?full_url=https://qr.dana.id/v1/281012012024081027676859"
WEB_SITE_LINK = "https://situs-pastelku.com" 

# STOK KODE VIP 7 HARI (Nomor 1 - 20)
stok_vip_7 = [
    "PK-3XR4H-XAAZC", "PK-6NXT7-JRUFV", "PK-YGHNT-ZKM3N", "PK-WKV2G-P4TAT",
    "PK-8J77E-N4K85", "PK-8ALTZ-UTVL5", "PK-LTFSF-QU4LZ", "PK-4VSXW-L6LWY",
    "PK-4GZ49-7HGUP", "PK-T49RK-8UD7Y", "PK-8FECP-GZ44L", "PK-KYEKW-87Z55",
    "PK-MKCEC-FZTUB", "PK-XK3HC-CPS49", "PK-SNPJG-LJC2W", "PK-ALHZJ-S7U2R",
    "PK-QDFKB-PK4DF", "PK-D7YLG-MYKBU", "PK-4A92A-C79BQ", "PK-4PX7K-6P5Z7"
]

# STOK KODE VIP 30 HARI (Nomor 21 - 40)
stok_vip_30 = [
    "PK-K3B8M-NXZ33", "PK-7MRRJ-9CTV7", "PK-FZ2MF-7HFK7", "PK-H8MBE-DWRPS",
    "PK-F8EKJ-UMVTG", "PK-V87PA-KGR6P", "PK-VNA6N-MMVKA", "PK-E5MF8-R6A6Q",
    "PK-5JFXN-4E9KL", "PK-2E6FC-T4NWS", "PK-PZF5L-9URVJ", "PK-89HAA-7QHNS",
    "PK-RGLDF-3PC9H", "PK-TUM2H-7JBR4", "PK-4A9H8-8W6LE", "PK-MCAZN-ZMALV",
    "PK-XUBR7-MB4H6", "PK-SXKTF-TY4CA", "PK-2ZQZ9-T27KF", "PK-8D7K2-B94HK"
]

print("🌸 Bot VIP PastelKu (Render 24 Jam) aktif...")

offset = None

while True:
    url_get = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    if offset:
        url_get += f"?offset={offset}"
        
    try:
        response = requests.get(url_get).json()
        
        if response.get("result"):
            for result in response["result"]:
                offset = result["update_id"] + 1
                
                if "message" in result:
                    msg = result["message"]
                    chat_id = msg["chat"]["id"]
                    nama_user = msg["from"].get("first_name", "Kak")
                    
                    url_send_msg = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                    
                    # 1. JIKA ADMIN MEREPONSE DENGAN PERINTAH KODE (/vip7 atau /vip30)
                    if "reply_to_message" in msg and "text" in msg:
                        teks_perintah = msg["text"].strip().lower()
                        
                        if teks_perintah in ["/vip7", "/vip30"]:
                            durasi = "7" if teks_perintah == "/vip7" else "30"
                            nama_pembeli = msg["reply_to_message"]["from"].get("first_name", "Kak")
                            chat_id_pembeli = msg["reply_to_message"]["chat"]["id"]
                            
                            if teks_perintah == "/vip7":
                                if len(stok_vip_7) > 0:
                                    kode_unik = stok_vip_7.pop(0)
                                    sisa_stok = len(stok_vip_7)
                                else:
                                    requests.post(url_send_msg, json={"chat_id": chat_id, "text": "❌ Stok kode VIP 7 hari habis!"})
                                    continue
                            else:
                                if len(stok_vip_30) > 0:
                                    kode_unik = stok_vip_30.pop(0)
                                    sisa_stok = len(stok_vip_30)
                                else:
                                    requests.post(url_send_msg, json={"chat_id": chat_id, "text": "❌ Stok kode VIP 30 hari habis!"})
                                    continue
                            
                            pesan_sukses_pembeli = (
                                f"Pembayaran sudah kuterima, makasih ya kak {nama_pembeli}!\\n\\n"
                                f"Kode aktivasi VIP {durasi} hari kakak:\\n"
                                f"`{kode_unik}`\\n\\n"
                                f"Cara pakai:\\n"
                                f"1. Buka {WEB_SITE_LINK}\\n"
                                f"2. Ketuk tombol \\"Jadi VIP\\" di pojok kanan atas\\n"
                                f"3. Masukkan kode, lalu ketuk \\"Tukar kode\\"\\n\\n"
                                f"Catatan: kode ini untuk 1 HP saja dan jangan dibagikan ke orang lain. Jangan hapus data browser, ya, supaya status VIP-nya tidak hilang.\\n\\n"
                                f"Kalau ada kendala, kabari aku di sini. Selamat berkreasi!"
                            )
                            
                            payload_pembeli = {
                                "chat_id": chat_id_pembeli,
                                "text": pesan_sukses_pembeli,
                                "parse_mode": "Markdown"
                            }
                            requests.post(url_send_msg, json=payload_pembeli)
                            
                            payload_admin = {
                                "chat_id": chat_id,
                                "text": f"✅ Berhasil! Kode {kode_unik} (VIP {durasi} hari) terkirim ke {nama_pembeli}.\\n📦 Sisa stok kode {durasi} hari: {sisa_stok}"
                            }
                            requests.post(url_send_msg, json=payload_admin)
                            continue

                    # 2. JIKA PEMBELI MENGIRIM FOTO (BUKTI BAYAR)
                    if "photo" in msg:
                        payload = {
                            "chat_id": chat_id,
                            "text": (
                                f"Makasih banyak ya, Kak {nama_user}! 🙏\\n\\n"
                                f"Bukti transfernya sudah diterima oleh sistem. "
                                f"Admin akan segera mengeceknya dan mengirimkan akses VIP PastelKu secepatnya. Mohon ditunggu ya Kak!"
                            )
                        }
                        requests.post(url_send_msg, json=payload)
                    
                    # 3. JIKA PEMBELI MENGIRIM TEKS BIASA
                    elif "text" in msg:
                        pesan_masuk = msg["text"].lower()
                        
                        if "vip" in pesan_masuk or "beli" in pesan_masuk or "pastelku" in pesan_masuk:
                            teks_balasan = (
                                f"✨ *LANGGANAN VIP PASTELKU* ✨\\n\\n"
                                f"Halo Kak {nama_user}! Mau buka semua fitur premium PastelKu tanpa batas? Pilih paketnya di bawah:\\n\\n"
                                f"📌 *Paket 7 Hari:* Rp4.000\\n"
                                f"📌 *Paket 30 Hari:* Rp12.000\\n\\n"
                                f"💎 *Keuntungan VIP:*\\n"
                                f"• Semua item PRO terbuka\\n"
                                f"• Bebas iklan & tanpa watermark\\n"
                                f"• Akses fitur khusus terkunci\\n\\n"
                                f"💳 *Cara Pembayaran:*\\n"
                                f"1. Klik link DANA berikut untuk membayar:\\n"
                                f"{DANA_LINK}\\n\\n"
                                f"2. Sesuai nominal paket yang kamu pilih.\\n"
                                f"3. Jika sudah, *kirim screenshot bukti pembayaran* langsung ke chat ini ya!"
                            )
                            
                            payload = {
                                "chat_id": chat_id,
                                "text": teks_balasan,
                                "parse_mode": "Markdown"
                            }
                            requests.post(url_send_msg, json=payload)
                            
                        else:
                            if not msg["text"].startswith("/"):
                                payload = {
                                    "chat_id": chat_id,
                                    "text": f"Halo Kak {nama_user}! Ingin berlangganan VIP? Silakan ketik *'VIP'* atau *'beli'* untuk melihat rincian harganya ya."
                                }
                                requests.post(url_send_msg, json=payload)
                        
    except Exception as e:
        print(f"Kendala koneksi: {e}")
        
    time.sleep(2)
'''

with open("bot.py", "w", encoding="utf-8") as f:
    f.write(bot_code)

# Membuat file requirements.txt
with open("requirements.txt", "w", encoding="utf-8") as f:
    f.write("requests\\n")

print("File bot.py dan requirements.txt berhasil dibuat!")
