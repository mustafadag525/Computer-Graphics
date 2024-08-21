# Gerekli modülleri içe aktar
import pygame
import random
import math

# Renkleri tanımla
BEYAZ = (255, 255, 255)
SİYAH = (0, 0, 0)
KIRMIZI = (255, 0, 0)
SARI = (255, 255, 0)
YEŞİL = (0, 255, 0)
PEMBE = (255, 192, 203)
MAVİ = (0, 0, 255)

# Ekran boyutunu tanımla
EK_BRE = 800
EK_YUK = 600

# Cisimlerin hızını tanımla
HIZ = 5

# Cisimlerin sayısını tanımla
CISIM_SAY = 10

# Cisimlerin listesini oluştur
cisimler = []

# Cisim sınıfını tanımla
class Cisim:
    # Cisim nesnesi oluştur constructor 
    def __init__(self, x, y, tip, renk, boyut):
        self.x = x # x konumu
        self.y = y # y konumu
        self.tip = tip # tipi (üçgen, daire, çokgen)
        self.renk = renk # rengi
        self.boyut = boyut # boyutu (yarıçap veya kenar uzunluğu)
        self.aci = 0 # rotasyon açısı
        self.donme = random.choice([-1, 1]) # rotasyon yönü (-1: saat yönünün tersi, 1: saat yönü)
        self.buyume = random.choice([-1, 1]) # büyüme yönü (-1: küçülme, 1: büyüme)
        self.hiz = HIZ # hızı

    # Cisim nesnesini güncelle
    def guncelle(self):
        # Cisim yukarıdan aşağı doğru hareket ettir
        self.y += self.hiz
        # Cisim ekranın dışına çıkarsa, y konumunu sıfırla
        if self.y > EK_YUK + self.boyut:
            self.y = -self.boyut
        # Cisim rotasyon yaparsa, açısını güncelle
        if self.tip == "üçgen" or self.tip == "çokgen":
            self.aci += self.donme
        # Cisim büyüyüp küçülürse, boyutunu güncelle
        if self.tip == "daire" or self.tip == "çokgen":
            self.boyut += self.buyume
            # Cisim minimum veya maksimum boyuta ulaşırsa, büyüme yönünü değiştir
            if self.boyut < 10 or self.boyut > 50:
                self.buyume = -self.buyume

    # Cisim nesnesini ekrana çiz
    def ciz(self):
        # Cisim tipine göre şekil çiz
        if self.tip == "üçgen":
            # Üçgenin köşe noktalarını hesapla
            nokta1 = (self.x, self.y - self.boyut)
            nokta2 = (self.x - self.boyut * math.sin(math.radians(60)), self.y + self.boyut / 2)
            nokta3 = (self.x + self.boyut * math.sin(math.radians(60)), self.y + self.boyut / 2)
           # self.boyut / 2 üçgen yüksekliği , 2 kenar arasındaki yüksek
            # Üçgenin köşe noktalarını rotasyona göre döndür
            nokta1 = dondur(nokta1, (self.x, self.y), self.aci)
            nokta2 = dondur(nokta2, (self.x, self.y), self.aci)
            nokta3 = dondur(nokta3, (self.x, self.y), self.aci)
            # Üçgeni ekrana çiz
            pygame.draw.polygon(ekran, self.renk, [nokta1, nokta2, nokta3])
        elif self.tip == "daire":
            # Daireyi ekrana çiz
            pygame.draw.circle(ekran, self.renk, (self.x, self.y), self.boyut)
        elif self.tip == "çokgen":
            # Çokgenin köşe sayısını rastgele belirle
            kose_say = random.randint(5, 8)
            # Çokgenin köşe noktalarını hesapla
            noktalar = []
            for i in range(kose_say):
                aci = i * 2 * math.pi / kose_say #çokgenin köşe noktalarını hesapla
                nokta = (self.x + self.boyut * math.cos(aci), self.y + self.boyut * math.sin(aci))
                # Çokgenin köşe noktalarını rotasyona ve büyümeye göre döndür
                nokta = dondur(nokta, (self.x, self.y), self.aci)
                noktalar.append(nokta)
            # Çokgeni ekrana çiz
            pygame.draw.polygon(ekran, self.renk, noktalar)

# Bir noktayı bir merkez etrafında belirli bir açı kadar döndüren fonksiyon
def dondur(nokta, merkez, aci):
    # Açıyı radyana çevir
    aci = math.radians(aci)
    # Noktanın merkeze göre x ve y farklarını hesapla
    dx = nokta[0] - merkez[0]
    dy = nokta[1] - merkez[1]
    # Noktanın yeni x ve y koordinatlarını hesapla
    x = merkez[0] + (dx * math.cos(aci) - dy * math.sin(aci))
    y = merkez[1] + (dx * math.sin(aci) + dy * math.cos(aci))
    # Noktayı tam sayı olarak döndür
    return (int(x), int(y))

# Doğru çizme algoritmasını uygulayan fonksiyon
def dogru_ciz(basla, bitis, renk):
    # Başlangıç ve bitiş noktalarının x ve y koordinatlarını al
    x1, y1 = basla
    x2, y2 = bitis
    # x ve y eksenlerindeki değişimi hesapla
    dx = x2 - x1
    dy = y2 - y1
    # x eksenindeki değişim sıfırsa, dikey bir doğru çiz
    if dx == 0:
        for y in range(min(y1, y2), max(y1, y2) + 1):
            ekran.set_at((x1, y), renk)
    # y eksenindeki değişim sıfırsa, yatay bir doğru çiz
    elif dy == 0:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            ekran.set_at((x, y1), renk)
    # x ve y eksenlerindeki değişim eşitse, 45 derecelik bir doğru çiz
    elif abs(dx) == abs(dy):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            y = y1 + (x - x1) * dy // dx
            ekran.set_at((x, y), renk)
    # x eksenindeki değişim y eksenindekinden büyükse, yatay yönlü bir doğru çiz
    elif abs(dx) > abs(dy):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            y = y1 + (x - x1) * dy // dx
            ekran.set_at((x, y), renk)
    # y eksenindeki değişim x eksenindekinden büyükse, dikey yönlü bir doğru çiz
    else:
        for y in range(min(y1,y2), max(y1, y2) + 1):
            x = x1 + (y - y1) * dx // dy
            ekran.set_at((x, y), renk)
# Bresenham çember çizme algoritmasını uygulayan fonksiyon
def cember_ciz(merkez, yaricap, renk):
    # Merkez noktasının x ve y koordinatlarını al
    x0, y0 = merkez
    # Çemberin ilk noktasının x ve y koordinatlarını belirle
    x = 0
    y = yaricap
    # Hata değerini hesapla
    hata = 1 - yaricap
    # Çemberin ilk çeyreğini ekrana çiz
    while x <= y:
        # Çemberin simetrik noktalarını ekrana çiz
        ekran.set_at((x0 + x, y0 + y), renk)
        ekran.set_at((x0 - x, y0 + y), renk)
        ekran.set_at((x0 + x, y0 - y), renk)
        ekran.set_at((x0 - x, y0 - y), renk)
        ekran.set_at((x0 + y, y0 + x), renk)
        ekran.set_at((x0 - y, y0 + x), renk)
        ekran.set_at((x0 + y, y0 - x), renk)
        ekran.set_at((x0 - y, y0 - x), renk)
        # x değerini bir artır
        x += 1
        # Hata değeri pozitifse, y değerini bir azalt ve hata değerini güncelle
        if hata > 0:
            y -= 1
            hata -= 2 * y
        # Hata değerine 2 * x + 1 ekle
        hata += 2 * x + 1

# Pygame'i başlat
pygame.init()

# Ekran nesnesi oluştur
ekran = pygame.display.set_mode((EK_BRE, EK_YUK))

# Ekran başlığını ayarla
pygame.display.set_caption("Cisimlerden Kaç")

# Saat nesnesi oluştur
saat = pygame.time.Clock()

# Oyun döngüsü çalışıyor mu?
calisiyor = True

# Oyun bitti mi?
bitti = False

# Puanı sıfırla
puan = 0

# Mavi dikdörtgenin x konumunu ortala
dik_x = EK_BRE // 2

# Mavi dikdörtgenin y konumunu sabitle
dik_y = EK_YUK - 50

# Mavi dikdörtgenin boyutlarını belirle
dik_bre = 100
dik_yuk = 50

# Mavi dikdörtgenin hızını belirle
dik_hiz = 10

# Cisimlerin listesini doldur
for i in range(CISIM_SAY):
    # Cisimlerin x konumlarını rastgele belirle
    x = random.randint(0, EK_BRE)
    # Cisimlerin y konumlarını rastgele belirle
    y = random.randint(-EK_YUK, 0)
    # Cisimlerin tiplerini rastgele belirle
    tip = random.choice(["üçgen", "daire", "çokgen"])
    # Cisimlerin renklerini rastgele belirle
    renk = random.choice([KIRMIZI, SARI, YEŞİL, PEMBE])
    # Cisimlerin boyutlarını rastgele belirle
    boyut = random.randint(10, 50)
    # Cisim nesnesi oluştur
    cisim = Cisim(x, y, tip, renk, boyut)
    # Cisim nesnesini listeye ekle
    cisimler.append(cisim)

# Oyun döngüsü
while calisiyor:
    # Olayları işle
    for olay in pygame.event.get():
        # Olay çıkış ise, oyun döngüsünü durdur
        if olay.type == pygame.QUIT:
            calisiyor = False
        elif olay.type == pygame.KEYDOWN:
            if olay.key == pygame.K_LEFT:
                dik_x -= dik_hiz
            elif olay.key == pygame.K_RIGHT:
                dik_x += dik_hiz
    # Ekranı beyaz renkle doldur
    ekran.fill(BEYAZ)
    # Arka plan için renkli doğrular çiz
    for i in range(0, EK_BRE, 10):
        renk = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        dogru_ciz((i, 0), (i, EK_YUK), renk)
    # Skor tablosu için siyah bir dikdörtgen çiz
    pygame.draw.rect(ekran, SİYAH, (0, 0, 200, 50))
    # Skor bilgisini beyaz renkle yaz
    font = pygame.font.SysFont("Arial", 32)
    metin = font.render("Puan: " + str(puan), True, BEYAZ)
    ekran.blit(metin, (10, 10))
    # Mavi dikdörtgenin x konumunu sınırla
    if dik_x < 0:
        dik_x = 0
    elif dik_x > EK_BRE - dik_bre:
        dik_x = EK_BRE - dik_bre
    # Mavi dikdörtgeni ekrana çiz
    pygame.draw.rect(ekran, MAVİ, (dik_x, dik_y, dik_bre, dik_yuk))
    # Cisimleri güncelle ve ekrana çiz
    for cisim in cisimler:
        cisim.guncelle()
        cisim.ciz()
        # Cisimlerden biri mavi dikdörtgen ile çakışırsa, oyunu bitir
        if cisim.y + cisim.boyut > dik_y and cisim.x + cisim.boyut > dik_x and cisim.x - cisim.boyut < dik_x + dik_bre:
            bitti = True
        # Cisimlerden biri ekranın altına ulaşırsa, puanı bir artır
        elif cisim.y == EK_YUK:
            puan += 1
    # Oyun bittiyse, sonuç bilgisini yaz
    if bitti:
        # Ekranı siyah renkle doldur
        ekran.fill(SİYAH)
        # Sonuç bilgisini beyaz renkle yaz
        font = pygame.font.SysFont("Arial", 64)
        metin = font.render("Oyun Bitti! Puan: " + str(puan), True, BEYAZ)
        ekran.blit(metin, (EK_BRE // 2 - metin.get_width() // 2, EK_YUK // 2 - metin.get_height() // 2))
        
        # Oyun döngüsünü durdur
        calisiyor = False
    # Ekranı güncelle
    pygame.display.flip()
    # Saati ayarla
    saat.tick(30)

# Pygame'i kapat
pygame.quit()