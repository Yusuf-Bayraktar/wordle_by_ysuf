# 🟩 Wordle Türkçe

![CI](https://github.com/Yusuf-Bayraktar/wordle_by_ysuf/actions/workflows/ci.yml/badge.svg)

Popüler kelime bulma oyunu Wordle'ın zengin Türkçe sözlük altyapısı ve modern masaüstü arayüzüyle yeniden geliştirilmiş versiyonu.

---

## 🎯 Projenin Amacı

Wordle Türkçe; oyuncuların kelime dağarcığını test ederken eğlenceli ve akıcı bir deneyim sunmayı amaçlar. Türkçe'nin kendine özgü harf yapısını (`İ/I`, `Ğ`, `Ş`, `Ç`, `Ö`, `Ü`) ve dil kurallarını tam anlamıyla destekleyen, harf değerlendirme mantığı standart kurallara dayanan, modern ve sade bir masaüstü kelime oyunu oluşturmak projenin temel hedefidir.

---

## ✨ Özellikler

- **Zengin Türkçe Sözlük:** 14.000'den fazla 5 harfli geçerli kelime havuzu ve özenle filtrelenmiş hedef kelimeler.
- **Kusursuz Türkçe Karakter Desteği:** Türkçe büyük-küçük harf kurallarına (`ı/I`, `i/İ`) tam uyum.
- **Doğru Harf Eşleştirme Mantığı:** Mükerrer harfleri ve kısmi eşleşmeleri adil ve standartlara uygun değerlendiren oyun motoru.
- **Kullanıcı Dostu Tasarım:**
  - Gözü yormayan modern koyu tema (Dark Mode).
  - Geometrik tam kare harf hücreleri ve anlık görsel geri bildirim.
  - Fiziksel klavye (harfler, Enter, Backspace) ve sanal ekrandan tıklanabilir klavye desteği.
  - Öncelik korumalı akıllı klavye tuş renklendirmesi (Yeşil > Sarı > Gri).
  - Kesintisiz oyun deneyimi için tek tıkla **Yeni Oyun** başlatma imkânı.
- **Güvenilirlik:** Tamamı test edilmiş modüler mimari.

---

## 🕹️ Nasıl Oynanır?

1. Hedef, rastgele seçilen **5 harfli gizli kelimeyi 6 denemede** bulmaktır.
2. Her tahmin geçerli 5 harfli bir Türkçe kelime olmalıdır.
3. Tahmininizi yazıp **ENTER** tuşuna bastığınızda harf kutularının renkleri ipucu verir:
   - 🟩 **Yeşil:** Harf kelimede var ve doğru konumda.
   - 🟨 **Sarı:** Harf kelimede var ancak farklı bir konumda.
   - ⬛ **Gri:** Harf kelimede hiç yer almıyor.
4. Klavyenizdeki tuş renklerini takip ederek sonraki tahminlerinizi stratejik olarak yapabilirsiniz.

---

## 🚀 Kurulum

### Gereksinimler
- **Python 3.12** veya üzeri
- [uv](https://docs.astral.sh/uv/) paket yöneticisi (veya standart `pip`)

### Adımlar

1. **Depoyu Klonlayın:**
   ```bash
   git clone https://github.com/Yusuf-Bayraktar/wordle_by_ysuf.git
   cd wordle
   ```

2. **Bağımlılıkları Kurun:**
   ```bash
   uv sync
   ```

---

## 🎮 Kullanım

Oyunu başlatmak için terminalinizde şu komutu çalıştırmanız yeterlidir:

```bash
uv run wordle
```

Alternatif olarak Python modülü olarak da çalıştırabilirsiniz:
```bash
uv run python -m wordle
```

---

## 📌 Sonuç

Wordle Türkçe; temiz kod prensiplerine uygun, genişletilebilir ve hem klavyeden hem fareyle rahatça oynanabilen keyifli bir masaüstü oyun deneyimi sunar.
