# VALORANT // Replik Tahmin Oyunu (Mobil & Web Uyumlu)

VALORANT ajanlarının **%100 orijinal Türkçe yerelleştirilmiş repliklerini** tahmin etme ve arkadaş ortamında oynama oyunu.

🌐 **Canlı Web Oyunu (Doğrudan Oyna):** [https://toprakesen.github.io/valorant-replik/](https://toprakesen.github.io/valorant-replik/)

---

## 🎯 Özellikler

- **%100 Orijinal Türkçe Yerelleştirme:** İngilizceden çevrilmiş sahte/yapay replikler değil; VALORANT'ın resmi Türkçe seslendirmesinde yer alan esprili, deyimli ve argo replikler (ör. *"Karşıda da mı Jett varmış? Yok be bir Jett var, o da bizde! Onlarınki anca çakma!"*, *"Clove, gecenin 3'ünde oturmuş yemek videoları izliyordum... Hayatta nasıl duruyorsun ki?!"*).
- **Oyun İçi Saf Karakter Sesleri:** Text-to-speech veya YouTuber video kesitleri kesinlikle kullanılmaz. Sesler doğrudan oyun paketinden (`tr_TR_Audio-WindowsClient.pak`) alınmış olup replik bittiği salisede temizce sonlanır.
- **Arkadaş Ortamı / Pass & Play Formatı:** 4 şıklı seçenekler yerine, replik ekranda belirir, bir kişi okur veya sesli ipucunu çalar.
- **🔊 Sesli İpucu (Repliği Dinlet):** Orijinal karakter seslendirmesini dinletir.
- **👁️ Cevabı Göster:** Karakterin yüksek çözünürlüklü görselini, rolünü, bölgesini ve temasını açığa çıkarır.
- **Skor ve Seri Takibi:** Doğru bildi / bilemedi sayaçları, Web Audio API ile taktiksel ses efektleri (SFX Aç/Kapat seçeneği).
- **Mobil Öncelikli Tasarım:** Telefon ve tabletlerde mükemmel dokunmatik ergonomi.
- **Hush (Ajan 31) Dahil:** En güncel ajanlar veritabanına entegredir.

---

## 🚀 Çalıştırma

Proje yerel bir HTTP sunucusu üzerinden hemen kullanılabilir:

```powershell
cd D:\code-projects\valorant-replik
python -m http.server 8080
```

Tarayıcınızdan açın:
[http://localhost:8080](http://localhost:8080)
