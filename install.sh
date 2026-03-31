#!/data/data/com.termux/files/usr/bin/bash
# Termux Gelişmiş Şifre Oluşturucu Kurulum Scripti

echo "🔐 NxYFLuX Gelişmiş Şifre Oluşturucu Kurulumu"
echo "============================================"

# Renkler
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Python kontrol
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}📦 Python3 bulunamadı. Kuruluyor...${NC}"
    pkg update -y
    pkg install python -y
fi

# Gerekli dizinler
SCRIPT_DIR="$HOME/nxyflux-termux-sifre-tool"
mkdir -p "$SCRIPT_DIR"

# Dosyaları kopyala
echo -e "${GREEN}📁 Dosyalar kopyalanıyor...${NC}"
cp nxyfluxsifre.py "$SCRIPT_DIR/"
chmod +x "$SCRIPT_DIR/nxyfluxsifre.py"

# Alias ekle
BASHRC="$HOME/.bashrc"
ALIAS_CMD='alias sifre="python3 "$HOME/nxyflux-termux-sifre-tool/nxyfluxsifre.py""'

if ! grep -q "alias sifre=" "$BASHRC" 2>/dev/null; then
    echo -e "${GREEN}⚡ Kısayol ekleniyor...${NC}"
    echo "" >> "$BASHRC"
    echo "# NxYFLuX Sifre Olusturma Alias" >> "$BASHRC"
    echo "$ALIAS_CMD" >> "$BASHRC"
fi

# Termux API kontrol (isteğe bağlı)
if ! command -v termux-clipboard-set &> /dev/null; then
    echo -e "${YELLOW}💡 İpucu: Panoya kopyalama için 'termux-api' yükleyin:${NC}"
    echo "   pkg install termux-api"
fi

echo ""
echo -e "${GREEN}✅ Kurulum tamamlandı!${NC}"
echo ""
echo "🚀 Kullanım:"
echo "   1. Yeni terminal açın veya: source ~/.bashrc"
echo "   2. 'sifre' yazarak çalıştırın"
echo "   VEYA"
echo "   python3 $SCRIPT_DIR/nxyfluxsifre.py"
echo ""
echo "📁 Kurulum dizini: $SCRIPT_DIR"
echo ""
echo "⭐ Beğendiyseniz GitHub'da yıldız vermeyi unutmayın!"
