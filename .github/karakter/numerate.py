import os

def numerate_images(folder_path, prefix="x"):
    import time
    timestamp = time.strftime("%Y%m%d%H%M%S")
    files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
    files.sort()  # İsteğe bağlı: alfabetik sırala
    for idx, fname in enumerate(files, 1):
        ext = os.path.splitext(fname)[1]
        new_name = f"{prefix}_{timestamp}_{idx}{ext}"
        src = os.path.join(folder_path, fname)
        dst = os.path.join(folder_path, new_name)
        if src != dst:
            os.rename(src, dst)
    print(f"{len(files)} dosya yeniden adlandırıldı.")

if __name__ == "__main__":
    in_path = input("Görselin dosya yolunu veya klasörünü girin: ").strip()
    if not in_path:
        print("Dosya yolu verilmedi. Çıkılıyor.")
    else:
        if os.path.isdir(in_path):
            numerate_images(in_path)
        else:
            print("Lütfen bir klasör yolu girin.")