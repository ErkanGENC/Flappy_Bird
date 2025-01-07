from PIL import Image, ImageDraw

def create_animated_background():
    # Arka plan boyutları eski değerlerde
    width = 500   # 800 olmalı
    height = 800  # 1000 olmalı
    frames = []
    
    # 10 frame'lik basit bir animasyon oluştur
    for i in range(10):
        # Yeni bir frame oluştur
        frame = Image.new('RGBA', (width, height), (135, 206, 235, 255))  # Açık mavi
        draw = ImageDraw.Draw(frame)
        
        # Hareketli bulutlar çiz
        cloud_offset = i * 20  # Her frame'de bulutları biraz kaydır
        draw.ellipse([cloud_offset, 100, cloud_offset + 100, 150], fill=(255, 255, 255, 200))
        draw.ellipse([cloud_offset + 200, 150, cloud_offset + 300, 200], fill=(255, 255, 255, 200))
        
        frames.append(frame)
    
    # GIF olarak kaydet
    frames[0].save(
        'flappy-bird-game/src/assets/images/background.gif',
        save_all=True,
        append_images=frames[1:],
        duration=100,
        loop=0
    )

if __name__ == "__main__":
    create_animated_background() 