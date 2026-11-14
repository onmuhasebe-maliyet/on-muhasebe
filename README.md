# Ön Muhasebe & Maliyet

Tarayıcıda çalışan ön muhasebe ve maliyet programı. Kurulum gerektirmez.

## Özellikler
- Gider kayıtları (KDV, ödeme durumu, belge no) ve mal maliyet kalemleri (Tek Düzen Hesap Planı 710–780)
- Satış faturaları (müşteri, ürün/hizmet, miktar, fiyat, KDV, tahsilat takibi), ürün ve müşteri bazında satış özeti
- Ürünler, üretim miktarları, ürün bazında birim maliyet ve kârlılık
- Gider tablosu (aylık), maliyet tablosu (SMM ve gelir tablosu)
- Dönem açma/kapama, dönem kapanış raporu, tek tuşla aylık/yıllık devir, yıl devir fişi
- Çoklu para birimi: TL, USD, EUR, GBP. Dövizli işlemler TCMB döviz **satış** kuruyla TL'ye çevrilir;
  sorgular "Tümü (TL karşılığı)" veya her para birimi için ayrı ayrı alınabilir
- Elle, Excel'den kopyala-yapıştır veya .xlsx/.csv dosyasıyla toplu giriş

## Veriler nerede tutulur?
Kayıtlar, programı kullanan kişinin **kendi tarayıcısında** saklanır (sunucuya gönderilmez).
Her kullanıcının verisi ayrıdır. Düzenli olarak *Ayarlar → Yedek indir* ile yedek alın;
yedek dosyası başka bir bilgisayarda *Yedekten geri yükle* ile açılabilir.

## TCMB kurları
`kurlar.json` dosyası, GitHub Actions ile hafta içi her gün otomatik güncellenir
(`.github/workflows/kurlar.yml`, `scripts/kur_guncelle.py`). Kaynak: https://www.tcmb.gov.tr/kurlar/
