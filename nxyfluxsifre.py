#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NxYFLuX Gelişmiş Şifre Oluşturma Aracı
Geliştirici: SeRCaN BeY / Telegram@nxyflux
Versiyon: 1.0
"""

import random
import string
import hashlib
import base64
import os
import sys
import json
from datetime import datetime
from getpass import getpass

class AdvancedPasswordGenerator:
    def __init__(self):
        self.history_file = os.path.expanduser("~/.password_history.json")
        self.config_file = os.path.expanduser("~/.password_config.json")
        self.load_config()

    def load_config(self):
        """Yapılandırmayı yükle"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {
                "default_length": 16,
                "save_history": True,
                "auto_copy": False
            }

    def save_config(self):
        """Yapılandırmayı kaydet"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)

    def generate_password(self, length=16, use_upper=True, use_lower=True, 
                         use_digits=True, use_symbols=True, use_spaces=False,
                         exclude_ambiguous=False, custom_charset=None):
        """
        Gelişmiş şifre oluştur

        Parametreler:
            length: Şifre uzunluğu
            use_upper: Büyük harfler (A-Z)
            use_lower: Küçük harfler (a-z)
            use_digits: Rakamlar (0-9)
            use_symbols: Özel karakterler (!@#$%^&*)
            use_spaces: Boşluk karakterleri
            exclude_ambiguous: Karışık karakterleri hariç tut (0, O, l, 1, I)
            custom_charset: Özel karakter seti
        """

        if custom_charset:
            charset = custom_charset
        else:
            charset = ""

            if use_lower:
                charset += string.ascii_lowercase
            if use_upper:
                charset += string.ascii_uppercase
            if use_digits:
                charset += string.digits
            if use_symbols:
                charset += "!@#$%^&*()_+-=[]{}|;:,.<>?"
            if use_spaces:
                charset += " "

            if exclude_ambiguous:
                ambiguous = "0O1lI"
                charset = ''.join(c for c in charset if c not in ambiguous)

        if not charset:
            raise ValueError("En az bir karakter seti seçilmelidir!")

        # Güvenli rastgele seçim
        password = ''.join(random.SystemRandom().choice(charset) for _ in range(length))

        return password

    def generate_passphrase(self, word_count=4, separator="-", capitalize=True):
        """
        Akılda kalıcı passphrase oluştur (Diceware tarzı)
        """
        # Basit İngilizce/Türkçe kelime listesi
        words = [
            "alfa", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel",
            "india", "juliet", "kilo", "lima", "mike", "november", "oscar", "papa",
            "quebec", "romeo", "sierra", "tango", "uniform", "victor", "whiskey", "xray",
            "yankee", "zulu", "kirmizi", "mavi", "yesil", "sari", "mor", "turuncu",
            "kedi", "kopek", "kus", "balik", "aslan", "kaplan", "ayi", "tavsan",
            "guney", "kuzey", "dogu", "bati", "yukari", "asagi", "sag", "sol",
            "bir", "iki", "uc", "dort", "bes", "alti", "yedi", "sekiz", "dokuz", "on"
        ]

        selected = [random.SystemRandom().choice(words) for _ in range(word_count)]

        if capitalize:
            selected = [w.capitalize() for w in selected]

        return separator.join(selected)

    def calculate_entropy(self, password):
        """Şifre güçlülük skoru hesapla"""
        length = len(password)

        # Karakter seti büyüklüğünü belirle
        charset_size = 0
        if any(c in string.ascii_lowercase for c in password):
            charset_size += 26
        if any(c in string.ascii_uppercase for c in password):
            charset_size += 26
        if any(c in string.digits for c in password):
            charset_size += 10
        if any(c in string.punctuation for c in password):
            charset_size += 32
        if any(c.isspace() for c in password):
            charset_size += 1

        if charset_size == 0:
            return 0

        entropy = length * (charset_size.bit_length() - 1)

        # Güç değerlendirmesi
        if entropy < 28:
            strength = "ÇOK ZAYIF"
            color = "\033[91m"  # Kırmızı
        elif entropy < 36:
            strength = "ZAYIF"
            color = "\033[93m"  # Sarı
        elif entropy < 60:
            strength = "ORTA"
            color = "\033[93m"  # Sarı
        elif entropy < 80:
            strength = "GÜÇLÜ"
            color = "\033[92m"  # Yeşil
        else:
            strength = "ÇOK GÜÇLÜ"
            color = "\033[92m"  # Yeşil

        return {
            "entropy": entropy,
            "strength": strength,
            "color": color,
            "length": length,
            "charset_size": charset_size
        }

    def hash_password(self, password, algorithm="sha256"):
        """Şifre hash'i oluştur"""
        if algorithm == "md5":
            return hashlib.md5(password.encode()).hexdigest()
        elif algorithm == "sha1":
            return hashlib.sha1(password.encode()).hexdigest()
        elif algorithm == "sha256":
            return hashlib.sha256(password.encode()).hexdigest()
        elif algorithm == "sha512":
            return hashlib.sha512(password.encode()).hexdigest()
        elif algorithm == "base64":
            return base64.b64encode(password.encode()).decode()
        else:
            raise ValueError(f"Bilinmeyen algoritma: {algorithm}")

    def save_to_history(self, password_info):
        """Şifreyi geçmişe kaydet"""
        if not self.config.get("save_history", True):
            return

        history = []
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                history = json.load(f)

        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": password_info.get("type", "password"),
            "length": len(password_info.get("password", "")),
            "strength": password_info.get("strength", {}),
            # Şifrenin kendisini kaydetme - sadece metadata
            "note": password_info.get("note", "")
        }

        history.append(entry)

        # Son 50 kaydı tut
        history = history[-50:]

        with open(self.history_file, 'w') as f:
            json.dump(history, f, indent=2)

    def show_history(self):
        """Geçmişi göster"""
        if not os.path.exists(self.history_file):
            print("\n[!] Henüz kayıt yok.")
            return

        with open(self.history_file, 'r') as f:
            history = json.load(f)

        print("\n" + "="*60)
        print("ŞİFRE OLUŞTURMA GEÇMİŞİ")
        print("="*60)

        for i, entry in enumerate(reversed(history[-10:]), 1):
            print(f"\n[{i}] {entry['timestamp']}")
            print(f"    Tip: {entry['type']}")
            print(f"    Uzunluk: {entry['length']}")
            if entry.get('strength'):
                print(f"    Güç: {entry['strength'].get('strength', 'N/A')} "
                      f"({entry['strength'].get('entropy', 0):.1f} bit)")
            if entry.get('note'):
                print(f"    Not: {entry['note']}")

        print("\n" + "="*60)

    def copy_to_clipboard(self, text):
        """Termux panoya kopyala"""
        try:
            # Termux clipboard
            os.system(f'termux-clipboard-set "{text}"')
            return True
        except:
            try:
                # Alternatif yöntem
                import subprocess
                subprocess.run(['termux-clipboard-set'], input=text.encode())
                return True
            except:
                return False


def print_banner():
    """Banner göster"""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║     🔐 NxYFLuX GELİŞMİŞ ŞİFRE OLUŞTURUCU v1.0 🔐           ║
║                                                           ║
║     Güvenli • Hızlı • Özelleştirilebilir                  ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_menu():
    """Menü göster"""
    menu = """
┌─────────────────────────────────────────────────────────┐
│  [1] 🎲 Hızlı Şifre Oluştur (Varsayılan Ayarlar)        │
│  [2] ⚙️  Özelleştirilmiş Şifre Oluştur                  │
│  [3] 📝 Passphrase Oluştur (Akılda Kalıcı)              │
│  [4] 🔢 PIN Kodu Oluştur                                  │
│  [5] 📊 Şifre Güç Analizi                               │
│  [6] #️⃣  Hash Oluştur                                   │
│  [7] 📜 Geçmişi Göster                                  │
│  [8] ⚙️  Ayarlar                                        │
│  [0] ❌ Çıkış                                           │
└─────────────────────────────────────────────────────────┘
    """
    print(menu)


def main():
    """Ana program"""
    generator = AdvancedPasswordGenerator()

    print_banner()

    while True:
        print_menu()
        choice = input("Seçiminiz: ").strip()

        if choice == "1":
            # Hızlı şifre
            pwd = generator.generate_password(length=16)
            entropy = generator.calculate_entropy(pwd)

            print(f"\n{'='*50}")
            print(f"🎲 OLUŞTURULAN ŞİFRE: {pwd}")
            print(f"📊 Güç: {entropy['color']}{entropy['strength']}\033[0m "
                  f"({entropy['entropy']:.1f} bit entropy)")
            print(f"📏 Uzunluk: {entropy['length']} karakter")
            print(f"{'='*50}")

            generator.save_to_history({
                "password": pwd,
                "type": "quick_password",
                "strength": entropy
            })

            copy = input("\n📋 Panoya kopyala? (E/H): ").lower()
            if copy == 'e':
                if generator.copy_to_clipboard(pwd):
                    print("✅ Panoya kopyalandı!")
                else:
                    print("❌ Kopyalama başarısız. Manuel olarak kopyalayın.")

        elif choice == "2":
            # Özelleştirilmiş şifre
            print("\n--- Özelleştirilmiş Şifre Ayarları ---")
            try:
                length = int(input("Uzunluk [16]: ") or "16")
                use_upper = input("Büyük harf? (E/H): ").lower() != 'h'
                use_lower = input("Küçük harf? (E/H): ").lower() != 'h'
                use_digits = input("Rakam? (E/H): ").lower() != 'h'
                use_symbols = input("Özel karakter? (E/H): ").lower() != 'h'
                exclude_ambiguous = input("Karışık karakterleri hariç tut? (E/H): ").lower() == 'e'

                pwd = generator.generate_password(
                    length=length,
                    use_upper=use_upper,
                    use_lower=use_lower,
                    use_digits=use_digits,
                    use_symbols=use_symbols,
                    exclude_ambiguous=exclude_ambiguous
                )

                entropy = generator.calculate_entropy(pwd)

                print(f"\n{'='*50}")
                print(f"⚙️  OLUŞTURULAN ŞİFRE: {pwd}")
                print(f"📊 Güç: {entropy['color']}{entropy['strength']}\033[0m")
                print(f"{'='*50}")

                generator.save_to_history({
                    "password": pwd,
                    "type": "custom_password",
                    "strength": entropy
                })

            except ValueError as e:
                print(f"❌ Hata: {e}")

        elif choice == "3":
            # Passphrase
            print("\n--- Passphrase Ayarları ---")
            word_count = int(input("Kelime sayısı [4]: ") or "4")
            separator = input("Ayraç [-]: ") or "-"
            capitalize = input("İlk harf büyük? (E/h): ").lower() != 'h'

            pwd = generator.generate_passphrase(word_count, separator, capitalize)
            entropy = generator.calculate_entropy(pwd)

            print(f"\n{'='*50}")
            print(f"📝 OLUŞTURULAN PASSPHRASE: {pwd}")
            print(f"📊 Güç: {entropy['color']}{entropy['strength']}\033[0m")
            print(f"{'='*50}")

            generator.save_to_history({
                "password": pwd,
                "type": "passphrase",
                "strength": entropy
            })

        elif choice == "4":
            # PIN
            length = int(input("PIN uzunluğu [4]: ") or "4")
            pin = ''.join(random.SystemRandom().choice(string.digits) for _ in range(length))

            print(f"\n{'='*50}")
            print(f"🔢 OLUŞTURULAN PIN: {pin}")
            print(f"{'='*50}")

            generator.save_to_history({
                "password": pin,
                "type": "pin",
                "strength": {"strength": "PIN", "entropy": length * 3.32}
            })

        elif choice == "5":
            # Analiz
            pwd = getpass("Analiz edilecek şifre: ")
            if pwd:
                entropy = generator.calculate_entropy(pwd)
                print(f"\n📊 ANALİZ SONUÇLARI:")
                print(f"   Uzunluk: {entropy['length']}")
                print(f"   Karakter seti: {entropy['charset_size']}")
                print(f"   Entropy: {entropy['entropy']:.2f} bit")
                print(f"   Güç: {entropy['color']}{entropy['strength']}\033[0m")

                # Tahmini kırma süresi
                if entropy['entropy'] < 28:
                    print("   ⚠️  Tahmini kırma süresi: Anında")
                elif entropy['entropy'] < 36:
                    print("   ⚠️  Tahmini kırma süresi: Saniyeler")
                elif entropy['entropy'] < 60:
                    print("   ⚠️  Tahmini kırma süresi: Saatler-Günler")
                elif entropy['entropy'] < 80:
                    print("   ✅ Tahmini kırma süresi: Yıllar")
                else:
                    print("   ✅ Tahmini kırma süresi: Yüzyıllar")

        elif choice == "6":
            # Hash
            pwd = getpass("Hash'lenecek metin: ")
            if pwd:
                print("\n--- Hash Algoritmaları ---")
                print("[1] MD5 (⚠️  Güvensiz)")
                print("[2] SHA1 (⚠️  Zayıf)")
                print("[3] SHA256 (✅ Önerilen)")
                print("[4] SHA512 (✅ En Güvenli)")
                print("[5] Base64 (Kodlama)")

                algo_choice = input("Seçim [3]: ").strip() or "3"
                algorithms = {"1": "md5", "2": "sha1", "3": "sha256", "4": "sha512", "5": "base64"}
                algo = algorithms.get(algo_choice, "sha256")

                hash_result = generator.hash_password(pwd, algo)
                print(f"\n{'='*50}")
                print(f"#️⃣  {algo.upper()} HASH:")
                print(f"{hash_result}")
                print(f"{'='*50}")

        elif choice == "7":
            generator.show_history()

        elif choice == "8":
            # Ayarlar
            print("\n--- Ayarlar ---")
            print(f"Varsayılan uzunluk: {generator.config.get('default_length', 16)}")
            print(f"Geçmiş kaydetme: {generator.config.get('save_history', True)}")

            new_length = input(f"Yeni varsayılan uzunluk [{generator.config.get('default_length', 16)}]: ")
            if new_length:
                generator.config['default_length'] = int(new_length)

            save_hist = input("Geçmiş kaydetme? (E/h): ").lower()
            generator.config['save_history'] = save_hist != 'h'

            generator.save_config()
            print("✅ Ayarlar kaydedildi!")

        elif choice == "0":
            print("\n👋 Güle güle! Güvenli kalın NxYFLuX Official Gururla Sunar.")
            break

        else:
            print("❌ Geçersiz seçim!")

        input("\nDevam etmek için Enter'a basın...")
        os.system('clear' if os.name != 'nt' else 'cls')
        print_banner()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Program sonlandırıldı.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Hata: {e}")
        sys.exit(1)
