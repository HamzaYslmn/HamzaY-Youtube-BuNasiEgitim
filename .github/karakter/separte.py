from PIL import Image
import os
import re

def split_image(in_path, rows=2, cols=2, out_dir=None):
    img = Image.open(in_path)
    w, h = img.size
    if rows <= 0 or cols <= 0:
        raise ValueError("rows and cols must be positive integers")

    widths = [w // cols] * cols
    widths[-1] += w % cols
    heights = [h // rows] * rows
    heights[-1] += h % rows

    out_dir = out_dir or os.path.dirname(os.path.abspath(in_path))
    os.makedirs(out_dir, exist_ok=True)
    base, ext = os.path.splitext(os.path.basename(in_path))
    ext = ext or ".png"

    y = 0
    for r, h_r in enumerate(heights):
        x = 0
        for c, w_c in enumerate(widths):
            part = img.crop((x, y, x + w_c, y + h_r))
            out_path = os.path.join(out_dir, f"{base}_r{r+1}c{c+1}{ext}")
            part.save(out_path)
            print("Saved:", out_path)
            x += w_c
        y += h_r

def parse_grid(grid_str):
    m = re.split(r'\s*[x]\s*', grid_str.lower())
    if len(m) == 2:
        return int(m[0]), int(m[1])
    raise ValueError("Geçersiz grid formatı")

if __name__ == "__main__":
    in_path = input("Görselin dosya yolunu girin: ").strip()
    if not in_path:
        print("Dosya yolu verilmedi. Çıkılıyor.")
    else:
        grid_input = input("Grid (örnek: 2x2, 2x3, 3x2) — boş bırakılırsa 2x2 kullanılır: ").strip()
        try:
            rows, cols = parse_grid(grid_input) if grid_input else (2, 2)
        except Exception as e:
            print("Geçersiz grid. Varsayılan 2x2 kullanılacak. Hata:", e)
            rows, cols = 2, 2

        out_dir = input("Çıktı klasörü (boş bırakırsanız giriş dosyası klasörü kullanılır): ").strip() or None
        try:
            split_image(in_path, rows, cols, out_dir)
        except FileNotFoundError:
            print("Dosya bulunamadı:", in_path)
        except Exception as e:
            print("Hata:", e)