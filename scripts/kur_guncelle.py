"""TCMB gösterge niteliğindeki döviz SATIŞ kurlarını (ForexSelling) indirip kurlar.json dosyasına yazar.

Kullanım:
    python scripts/kur_guncelle.py                    # son kayıtlı tarihten bugüne kadar günceller
    python scripts/kur_guncelle.py --baslangic 2025-01-01

kurlar.json biçimi:
    {"kaynak": "...", "guncelleme": "...", "kurlar": {"2026-11-13": {"USD": 50.283, "EUR": ..., "GBP": ...}, ...}}
Anahtar tarih, kurların TCMB tarafından ilan edildiği gündür.
"""
import argparse
import datetime as dt
import json
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

PARALAR = ["USD", "EUR", "GBP"]
DOSYA = Path(__file__).resolve().parent.parent / "kurlar.json"
TR = dt.timezone(dt.timedelta(hours=3))


def getir(gun: dt.date):
    url = f"https://www.tcmb.gov.tr/kurlar/{gun:%Y%m}/{gun:%d%m%Y}.xml"
    istek = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (kur-guncelle)"})
    for deneme in range(3):
        try:
            with urllib.request.urlopen(istek, timeout=30) as yanit:
                veri = yanit.read()
            break
        except urllib.error.HTTPError as e:
            if e.code == 404:          # hafta sonu / resmi tatil: kur ilan edilmemiş
                return None
            if deneme == 2:
                raise
        except urllib.error.URLError:
            if deneme == 2:
                raise
        time.sleep(2)
    kok = ET.fromstring(veri)
    sonuc = {}
    for c in kok.findall("Currency"):
        kod = c.get("CurrencyCode")
        if kod in PARALAR:
            satis = (c.findtext("ForexSelling") or "").strip()
            birim = float((c.findtext("Unit") or "1").strip() or 1)
            if satis:
                sonuc[kod] = round(float(satis) / birim, 4)
    return sonuc or None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--baslangic", help="YYYY-AA-GG (varsayılan: son kayıtlı tarihten 10 gün önce, yoksa 2025-01-01)")
    args = ap.parse_args()

    mevcut = {}
    if DOSYA.exists():
        mevcut = json.loads(DOSYA.read_text(encoding="utf-8")).get("kurlar", {})

    bugun = dt.datetime.now(TR).date()
    if args.baslangic:
        bas = dt.date.fromisoformat(args.baslangic)
    elif mevcut:
        bas = dt.date.fromisoformat(max(mevcut)) - dt.timedelta(days=10)
    else:
        bas = dt.date(2025, 1, 1)

    yeni = 0
    gun = bas
    while gun <= bugun:
        if gun.weekday() < 5:          # hafta sonu ilan yok
            k = getir(gun)
            if k:
                if mevcut.get(gun.isoformat()) != k:
                    yeni += 1
                mevcut[gun.isoformat()] = k
            time.sleep(0.15)
        gun += dt.timedelta(days=1)

    cikti = {
        "kaynak": "TCMB gösterge niteliğindeki döviz satış kurları (ForexSelling) - https://www.tcmb.gov.tr/kurlar/",
        "guncelleme": dt.datetime.now(TR).strftime("%Y-%m-%d %H:%M"),
        "kurlar": dict(sorted(mevcut.items())),
    }
    DOSYA.write_text(json.dumps(cikti, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"{yeni} gün eklendi/güncellendi, toplam {len(mevcut)} gün. Son: {max(mevcut) if mevcut else '-'}")


if __name__ == "__main__":
    main()
