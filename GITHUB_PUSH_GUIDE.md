# GitHub Repository'ye Push Etme - Detaylı Kılavuz

## 📋 Ön Hazırlık

### 1. GitHub'da Repository Oluştur

1. **GitHub'a git:** https://github.com
2. **Sağ üst köşede "+" butonuna tıkla** → "New repository"
3. **Repository bilgilerini doldur:**
   - **Repository name:** `mobility-network-analysis`
   - **Description:** `Building-to-Building Accessibility Network Analysis for Transportation Infrastructure Planning`
   - **Public** veya **Private** seç (tercihinize göre)
   - **Initialize this repository with:** Hiçbirini işaretleme (README, .gitignore, license ekleme)
4. **"Create repository" butonuna tıkla**

### 2. Git Kurulumu Kontrolü

PowerShell'de şu komutu çalıştır:

```powershell
git --version
```

Eğer "git is not recognized" hatası alırsan, Git'i yükle:
- https://git-scm.com/download/win

---

## 🚀 Adım Adım Push İşlemi

### Adım 1: Proje Klasörüne Git

PowerShell'de:

```powershell
cd C:\mobility-network-analysis
```

### Adım 2: Git Repository Initialize Et

```powershell
git init
```

**Beklenen çıktı:**
```
Initialized empty Git repository in C:/mobility-network-analysis/.git/
```

### Adım 3: Tüm Dosyaları Stage'e Ekle

```powershell
git add .
```

**Açıklama:** Bu komut tüm dosyaları (`.gitignore`'a göre filtrelenmiş) staging area'ya ekler.

**Kontrol etmek için:**
```powershell
git status
```

**Beklenen çıktı:** Yeşil renkte "Changes to be committed" altında dosyalar listelenir.

### Adım 4: İlk Commit'i Yap

```powershell
git commit -m "Initial commit: Building-to-Building Accessibility Network Analysis

- Complete pipeline: 5 steps (extract, network, analyze, accessibility, visualize)
- CityGML parser with MultiSurface support and EPSG:5253 transformation
- Network analysis with centrality metrics (degree, betweenness, closeness, PageRank)
- Accessibility scoring (distance-based and network-based)
- Multiple visualizations (network graph, heatmap, paths, distributions)
- Comprehensive documentation (README, analysis report, setup guide)
- WPI research alignment: Network optimization and infrastructure planning"
```

**Beklenen çıktı:**
```
[main (root-commit) xxxxxxx] Initial commit: ...
 X files changed, Y insertions(+)
```

### Adım 5: GitHub Repository'yi Remote Olarak Ekle

**ÖNEMLİ:** `YOUR_USERNAME` yerine kendi GitHub kullanıcı adını yaz!

```powershell
git remote add origin https://github.com/YOUR_USERNAME/mobility-network-analysis.git
```

**Örnek:**
```powershell
git remote add origin https://github.com/suleymansarilar/mobility-network-analysis.git
```

**Kontrol etmek için:**
```powershell
git remote -v
```

**Beklenen çıktı:**
```
origin  https://github.com/YOUR_USERNAME/mobility-network-analysis.git (fetch)
origin  https://github.com/YOUR_USERNAME/mobility-network-analysis.git (push)
```

### Adım 6: Branch'i Main Olarak Ayarla

```powershell
git branch -M main
```

**Açıklama:** Git'in yeni versiyonlarında default branch "main" olarak değişti. Bu komut branch'i "main" olarak ayarlar.

### Adım 7: GitHub'a Push Et

```powershell
git push -u origin main
```

**İlk kez push ediyorsan:**
- GitHub kullanıcı adı ve şifre isteyebilir
- **ÖNEMLİ:** Şifre yerine **Personal Access Token (PAT)** kullanman gerekebilir

**Beklenen çıktı:**
```
Enumerating objects: XX, done.
Counting objects: 100% (XX/XX), done.
Delta compression using up to X threads
Compressing objects: 100% (XX/XX), done.
Writing objects: 100% (XX/XX), XX.XX KiB | X.XX MiB/s, done.
Total XX (delta X), reused 0 (delta 0), pack-reused 0
To https://github.com/YOUR_USERNAME/mobility-network-analysis.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

---

## 🔐 GitHub Authentication (İlk Kez Push Ediyorsan)

### Personal Access Token (PAT) Oluşturma

Eğer şifre ile push etmeye çalışırken hata alırsan:

1. **GitHub'a git:** https://github.com
2. **Sağ üst köşede profil fotoğrafına tıkla** → **Settings**
3. **Sol menüden:** "Developer settings"
4. **"Personal access tokens"** → **"Tokens (classic)"**
5. **"Generate new token"** → **"Generate new token (classic)"**
6. **Token bilgileri:**
   - **Note:** `mobility-network-analysis-push`
   - **Expiration:** İstediğin süre (örn: 90 days)
   - **Scopes:** `repo` işaretle (tüm repo işlemleri için)
7. **"Generate token"** butonuna tıkla
8. **Token'ı kopyala** (bir daha gösterilmeyecek!)

### Token ile Push Etme

Push komutunu çalıştırdığında:
- **Username:** GitHub kullanıcı adın
- **Password:** Token'ı yapıştır (şifre değil!)

---

## ✅ Push Sonrası Kontrol

### 1. GitHub'da Kontrol Et

1. **Repository sayfasına git:** https://github.com/YOUR_USERNAME/mobility-network-analysis
2. **Dosyaların yüklendiğini kontrol et:**
   - README.md görünmeli
   - scripts/ klasörü görünmeli
   - utils/ klasörü görünmeli
   - Diğer dosyalar görünmeli

### 2. README.md'nin Göründüğünü Kontrol Et

Repository ana sayfasında README.md otomatik olarak görünür. İçeriği kontrol et.

---

## 🔄 Sonraki Değişiklikler İçin

Eğer projede değişiklik yaparsan:

```powershell
# 1. Değişiklikleri kontrol et
git status

# 2. Değişiklikleri stage'e ekle
git add .

# 3. Commit yap
git commit -m "Açıklayıcı commit mesajı"

# 4. Push et
git push
```

---

## 🐛 Olası Hatalar ve Çözümleri

### Hata 1: "fatal: remote origin already exists"

**Çözüm:**
```powershell
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/mobility-network-analysis.git
```

### Hata 2: "error: failed to push some refs"

**Çözüm:** GitHub'da README veya başka dosya oluşturduysan:
```powershell
git pull origin main --allow-unrelated-histories
# Merge conflict varsa çöz, sonra:
git push -u origin main
```

### Hata 3: "Authentication failed"

**Çözüm:** Personal Access Token kullan (yukarıdaki PAT bölümüne bak)

### Hata 4: "Permission denied"

**Çözüm:** 
- Repository'nin sana ait olduğundan emin ol
- Token'ın `repo` scope'una sahip olduğundan emin

---

## 📝 Commit Mesajı Önerileri

İyi commit mesajları:
- ✅ "Add network analysis script with centrality metrics"
- ✅ "Fix accessibility calculation for disconnected graphs"
- ✅ "Update README with WPI research alignment"
- ✅ "Add visualization utilities for network graphs"

Kötü commit mesajları:
- ❌ "update"
- ❌ "fix"
- ❌ "changes"

---

## 🎯 Son Kontrol Listesi

Push etmeden önce:

- [ ] GitHub'da repository oluşturuldu
- [ ] Repository adı doğru: `mobility-network-analysis`
- [ ] `.gitignore` dosyası var (büyük dosyalar commit edilmeyecek)
- [ ] `README.md` güncel ve doğru
- [ ] Tüm script'ler çalışıyor
- [ ] Git kurulu ve çalışıyor (`git --version`)
- [ ] Remote URL doğru (kendi kullanıcı adınla)
- [ ] Personal Access Token hazır (gerekirse)

---

## 🚀 Hızlı Komut Özeti

Tüm işlem için tek seferde:

```powershell
cd C:\mobility-network-analysis
git init
git add .
git commit -m "Initial commit: Building-to-Building Accessibility Network Analysis"
git remote add origin https://github.com/YOUR_USERNAME/mobility-network-analysis.git
git branch -M main
git push -u origin main
```

**ÖNEMLİ:** `YOUR_USERNAME` yerine kendi GitHub kullanıcı adını yaz!

---

## 💡 İpuçları

1. **İlk push'tan sonra:** GitHub'da repository ayarlarına git:
   - **Topics ekle:** network-analysis, citygml, infrastructure-planning, python
   - **Description güncelle:** README'deki özeti kullan
   - **Website ekle:** Eğer portfolio siten varsa

2. **README.md otomatik görünür:** Repository ana sayfasında

3. **.gitignore çalışıyor mu kontrol et:**
   - `data/output/*.png` dosyaları commit edilmemeli
   - `data/processed/*.pkl` dosyaları commit edilmemeli
   - `__pycache__/` klasörleri commit edilmemeli

4. **Sonraki push'lar için:** Sadece `git add .`, `git commit -m "..."`, `git push` yeterli

---

**Başarılar!** 🎉

