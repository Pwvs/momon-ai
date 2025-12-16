import os
import sys
import time
import random
import platform
import re
import base64
import urllib.parse
import uuid
import requests
import psutil
from datetime import datetime

G = "\033[92m"
R = "\033[91m"
Y = "\033[93m"
C = "\033[96m"
W = "\033[0m"

CONFIG_FILE = "config.cfg"
LOG_FILE = "history.log"
STATS_FILE = "stats.cfg"

config = {
    "anim": "1",
    "speed": "0.003"
}

stats = {
    "run": 0
}

def load_config():
    """Load configuration from file"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    config[key] = value
    else:
        save_config()

def save_config():
    """Save configuration to file"""
    with open(CONFIG_FILE, "w") as f:
        for key, value in config.items():
            f.write(f"{key}={value}\n")

def load_stats():
    """Load statistics from file"""
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE) as f:
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    stats[key] = int(value)
    stats["run"] = stats.get("run", 0) + 1

def save_stats():
    """Save statistics to file"""
    with open(STATS_FILE, "w") as f:
        for key, value in stats.items():
            f.write(f"{key}={value}\n")

def log(action):
    """Log an action to the log file and update statistics"""
    with open(LOG_FILE, "a") as f:
        timestamp = datetime.now().strftime('%H:%M:%S')
        f.write(f"[{timestamp}] {action}\n")
    
    stats[action] = stats.get(action, 0) + 1
    save_stats()

def slow(text):
    """Print text with typing animation if enabled"""
    if config["anim"] == "0":
        print(text)
        return
    
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(float(config["speed"]))
    print()

def clear_screen():
    """Clear the terminal screen"""
    os.system("clear" if os.name == "posix" else "cls")

def show_banner():
    """Display the application banner"""
    clear_screen()
    slow(G + r"""
 ██╗   ███╗ ██████╗   ███╗   ███╗ ██████╗ ███╗   ██╗
 ████╗ ████║██╔═══██╗ ████╗ ████║██╔═══██╗████╗  ██║
 ██╔████╔██║██║   ██║ ██╔████╔██║██║   ██║██╔██╗ ██║
 ██║╚██╔╝██║██║   ██║ ██║╚██╔╝██║██║   ██║██║╚██╗██║
 ██║ ═╝  ██║╚██████╔╝ ██║ ═╝  ██║╚██████╔╝██║ █████║
 ╚═╝     ╚═╝ ╚═════╝  ╚═╝     ╚═╝ ╚═════╝ ╚═╝   ╚═╝

           MOMON-AI | TERMINAL ASSISTANT
""" + W)

def show_main_menu():
    """Display the main menu"""
    slow(C + """
[ MENU UTAMA ]
[1] Fake Scan System
[2] System Info
[3] Kalkulator
[4] Tools Teks
[5] Password Tools
[6] Encoder / Decoder
[7] Random Generator
[8] Cek URL
[9] Activity Log
[10] Settings
[11] Statistics
[12] Command Mode
[13] Internet Tools
[14] Entertainment
[15] System Tools
[16] About Developer       [NEW]
[0] Exit
""" + W)

def show_settings_menu():
    """Display the settings menu"""
    slow(C + f"""
[ SETTINGS ]
Animasi: {'ON' if config['anim'] == '1' else 'OFF'}
Speed: {config['speed']}

[1] Toggle Animasi
[2] Speed Animasi
[0] Kembali
""" + W)

def fake_scan():
    """Simulate a system scan"""
    slow(G + "[+] Scanning system...")
    for i in range(0, 101, 20):
        slow(f"[+] {i}%")
        time.sleep(0.5)
    slow(G + "[✓] System Secure" + W)
    log("Fake Scan")

def system_info():
    """Display system information"""
    slow(G + f"""
OS      : {platform.system()}
Version : {platform.release()}
Machine : {platform.machine()}
""" + W)
    log("System Info")

def calculator():
    """Simple calculator"""
    while True:
        slow(C + """
[ KALKULATOR ]
[1] +
[2] -
[3] *
[4] /
[0] Kembali
""" + W)
        choice = input("Pilih > ")
        if choice == "0":
            break
        
        try:
            num1 = float(input("Angka 1: "))
            num2 = float(input("Angka 2: "))
            
            operations = {
                "1": num1 + num2,
                "2": num1 - num2,
                "3": num1 * num2,
                "4": num1 / num2 if num2 != 0 else "Error: Pembagian dengan nol"
            }
            
            result = operations[choice]
            slow(G + f"Hasil: {result}" + W)
            log(f"Kalkulator {num1} {choice} {num2} = {result}")
        except (KeyError, ValueError, ZeroDivisionError):
            slow(R + "Error" + W)

def text_tools():
    """Text manipulation tools"""
    while True:
        slow(C + """
[ TEXT TOOLS ]
[1] Print Teks Berulang
[2] Uppercase
[3] Lowercase
[4] Title Case
[5] Hapus Spasi Berlebih
[6] Hitung Kata/Karakter
[0] Kembali
""" + W)
        choice = input("Pilih > ")
        
        if choice == "0":
            break
        elif choice == "1":
            text = input("Teks: ")
            count = int(input("Jumlah: "))
            for i in range(count):
                print(f"{i+1}. {text}")
            log("Print Teks Berulang")
        elif choice in ["2", "3", "4", "5", "6"]:
            text = input("Teks: ")
            if choice == "2":
                result = text.upper()
            elif choice == "3":
                result = text.lower()
            elif choice == "4":
                result = text.title()
            elif choice == "5":
                result = " ".join(text.split())
            elif choice == "6":
                result = f"Kata: {len(text.split())} | Karakter: {len(text)}"
            
            print("Hasil:", result)
            log(f"Text Tools - Option {choice}")

def password_tools():
    """Password generation and strength checking"""
    while True:
        slow(C + """
[ PASSWORD TOOLS ]
[1] Generate Password
[2] Cek Kekuatan Password
[0] Kembali
""" + W)
        choice = input("Pilih > ")
        
        if choice == "0":
            break
        elif choice == "1":
            chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%"
            length = int(input("Panjang: "))
            password = ''.join(random.choice(chars) for _ in range(length))
            slow(G + password + W)
            log("Generate Password")
        elif choice == "2":
            password = input("Password: ")
            score = len(password)
            if re.search(r"[A-Z]", password):
                score += 2
            if re.search(r"[0-9]", password):
                score += 2
            if re.search(r"[!@#$%^&*]", password):
                score += 2
            
            if score < 8:
                status = "LEMAH"
            elif score < 12:
                status = "SEDANG"
            else:
                status = "KUAT"
            
            slow(G + status + W)
            log("Check Password Strength")

def encoder_decoder():
    """Encoding/decoding tools"""
    while True:
        slow(C + """
[ ENCODE / DECODE ]
[1] Base64 Encode
[2] Base64 Decode
[3] URL Encode
[4] URL Decode
[5] ROT13
[0] Kembali
""" + W)
        choice = input("Pilih > ")
        if choice == "0":
            break
        
        text = input("Teks: ")
        
        try:
            if choice == "1":
                result = base64.b64encode(text.encode()).decode()
            elif choice == "2":
                result = base64.b64decode(text).decode()
            elif choice == "3":
                result = urllib.parse.quote(text)
            elif choice == "4":
                result = urllib.parse.unquote(text)
            elif choice == "5":
                result = text.translate(str.maketrans(
                    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                    "NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm"))
            
            print("Hasil:", result)
            log("Encoder/Decoder")
        except Exception as e:
            slow(R + f"Error: {e}" + W)

def random_generator():
    """Random data generator"""
    while True:
        slow(C + """
[ RANDOM GENERATOR ]
[1] Username
[2] Token
[3] UUID
[4] Email
[5] Nama
[6] Quote
[0] Kembali
""" + W)
        choice = input("Pilih > ")
        
        if choice == "0":
            break
        elif choice == "1":
            result = "user_" + ''.join(random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(6))
        elif choice == "2":
            result = ''.join(random.choice("abcdef0123456789") for _ in range(32))
        elif choice == "3":
            result = str(uuid.uuid4())
        elif choice == "4":
            result = f"user{random.randint(1,999)}@mail.com"
        elif choice == "5":
            result = random.choice(["Alex", "Rizky", "Dio", "Naufal", "Budi", "Sari"])
        elif choice == "6":
            result = random.choice([
                "Stay curious.", "Code never lies.", "Learn every day.",
                "Knowledge is power.", "Practice makes perfect."
            ])
        
        print("Hasil:", result)
        log("Random Generator")

def url_checker():
    """URL safety checker"""
    url = input("URL: ").lower()
    score = 0
    
    if not url.startswith("https"):
        score += 2
    if re.search(r"(login|bonus|verify|password|account)", url):
        score += 2
    
    if score < 2:
        status = "AMAN"
        color = G
    elif score < 4:
        status = "WASPADA"
        color = Y
    else:
        status = "BERBAHAYA"
        color = R
    
    slow(color + status + W)
    log(f"URL Check {status}")

def show_history():
    """Display activity log"""
    if not os.path.exists(LOG_FILE):
        slow(R + "Belum ada log" + W)
        return
    
    with open(LOG_FILE) as f:
        content = f.read()
        if content:
            print(content)
        else:
            slow(Y + "Log file kosong" + W)

def settings_menu():
    """Application settings"""
    while True:
        show_settings_menu()
        choice = input("> ")
        
        if choice == "0":
            break
        elif choice == "1":
            config["anim"] = "0" if config["anim"] == "1" else "1"
            slow(G + f"Animasi: {'ON' if config['anim'] == '1' else 'OFF'}" + W)
        elif choice == "2":
            try:
                new_speed = input("Speed (contoh 0.001): ")
                float(new_speed)  # Validasi
                config["speed"] = new_speed
                slow(G + f"Speed diubah menjadi: {new_speed}" + W)
            except ValueError:
                slow(R + "Speed harus angka!" + W)
        
        save_config()
        log("Settings")

def show_statistics():
    """Display usage statistics"""
    if not stats:
        slow(Y + "Belum ada statistics" + W)
        return
    
    slow(C + "\n[ STATISTICS ]" + W)
    for key, value in sorted(stats.items()):
        print(f"{key}: {value}")

def command_mode():
    """Interactive command mode"""
    slow(G + "Command mode (ketik 'help' untuk bantuan, 'exit' untuk keluar)" + W)
    
    while True:
        command = input("momon > ").lower().strip()
        
        if command == "exit":
            break
        elif command == "help":
            print("""
Perintah yang tersedia:
- genpass    : Generate password
- time       : Waktu sekarang
- encode <teks> : Encode base64
- decode <teks> : Decode base64
- clear      : Bersihkan layar
- exit       : Keluar command mode
            """)
        elif command == "genpass":
            chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%"
            password = ''.join(random.choice(chars) for _ in range(12))
            print("Password:", password)
        elif command == "time":
            print("Waktu:", datetime.now().strftime("%H:%M:%S"))
        elif command.startswith("encode "):
            text = command[7:]
            encoded = base64.b64encode(text.encode()).decode()
            print("Encoded:", encoded)
        elif command.startswith("decode "):
            text = command[7:]
            try:
                decoded = base64.b64decode(text).decode()
                print("Decoded:", decoded)
            except:
                print("Error: Tidak bisa decode")
        elif command == "clear":
            clear_screen()
        else:
            print("Perintah tidak dikenali. Ketik 'help' untuk bantuan.")
        
        log(f"Command Mode: {command}")

def internet_tools():
    """Tools untuk koneksi dan analisis internet"""
    while True:
        slow(C + """
[ INTERNET TOOLS ]
[1] Check Website Status
[2] Ping Website
[3] Download File (Simple)
[4] Get Public IP
[5] Check Internet Speed (Basic)
[0] Kembali
""" + W)
        choice = input("Pilih > ")
        
        if choice == "0":
            break
        elif choice == "1":
            url = input("Masukkan URL (contoh: https://google.com): ")
            try:
                if not url.startswith(('http://', 'https://')):
                    url = 'https://' + url
                
                response = requests.get(url, timeout=10)
                status_color = G if response.status_code == 200 else Y if 300 <= response.status_code < 400 else R
                slow(f"Status: {status_color}{response.status_code} {response.reason}{W}")
                slow(f"Server: {response.headers.get('Server', 'Tidak diketahui')}")
                log(f"Check Website Status: {url} - {response.status_code}")
            except requests.exceptions.RequestException as e:
                slow(R + f"Error: {e}" + W)
        
        elif choice == "2":
            host = input("Host/IP: ")
            try:
                param = "-n" if platform.system().lower() == "windows" else "-c"
                result = os.system(f"ping {param} 4 {host}")
                if result == 0:
                    slow(G + "Ping berhasil!" + W)
                else:
                    slow(R + "Ping gagal!" + W)
                log(f"Ping: {host}")
            except:
                slow(R + "Error!" + W)
        
        elif choice == "3":
            url = input("URL file: ")
            filename = input("Nama file output: ")
            try:
                response = requests.get(url, stream=True)
                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                slow(G + f"File berhasil didownload: {filename}" + W)
                log(f"Download File: {filename}")
            except Exception as e:
                slow(R + f"Error: {e}" + W)
        
        elif choice == "4":
            try:
                response = requests.get('https://httpbin.org/ip', timeout=10)
                ip_data = response.json()
                slow(G + f"Public IP: {ip_data['origin']}" + W)
                log("Get Public IP")
            except:
                slow(R + "Tidak bisa mendapatkan IP" + W)
        
        elif choice == "5":
            slow(Y + "Testing internet speed (basic)...")
            start_time = time.time()
            try:
                response = requests.get('https://www.google.com', timeout=10)
                end_time = time.time()
                speed = len(response.content) / (end_time - start_time) / 1024
                slow(G + f"Speed: {speed:.2f} KB/s" + W)
                log("Internet Speed Test")
            except:
                slow(R + "Speed test gagal!" + W)

def entertainment():
    """Fitur hiburan dan permainan"""
    while True:
        slow(C + """
[ ENTERTAINMENT ]
[1] Quote of the Day
[2] Random Joke
[3] Coin Flip
[4] Dice Roll
[5] Number Guessing Game
[6] Rock Paper Scissors
[7] ASCII Art Generator
[0] Kembali
""" + W)
        choice = input("Pilih > ")
        
        if choice == "0":
            break
        elif choice == "1":
            quotes = [
                "The only way to do great work is to love what you do. - Steve Jobs",
                "Innovation distinguishes between a leader and a follower. - Steve Jobs",
                "Stay hungry, stay foolish. - Steve Jobs",
                "Code is like humor. When you have to explain it, it's bad. - Cory House",
                "The best error message is the one that never shows up. - Thomas Fuchs"
            ]
            quote = random.choice(quotes)
            slow(Y + "Quote of the Day:\n" + G + quote + W)
            log("Quote of the Day")
        
        elif choice == "2":
            jokes = [
                "Why do programmers prefer dark mode? Because light attracts bugs!",
                "Why don't programmers like nature? It has too many bugs.",
                "How many programmers does it take to change a light bulb? None, that's a hardware problem!",
                "Why do Java developers wear glasses? Because they can't C#!",
                "I would tell you a joke about UDP... but you might not get it."
            ]
            joke = random.choice(jokes)
            slow(G + "Joke: " + Y + joke + W)
            log("Random Joke")
        
        elif choice == "3":
            result = random.choice(["HEADS", "TAILS"])
            slow(Y + "Flipping coin... " + G + result + "!" + W)
            log("Coin Flip")
        
        elif choice == "4":
            roll = random.randint(1, 6)
            dice_faces = {
                1: "┌───────┐\n│       │\n│   ●   │\n│       │\n└───────┘",
                2: "┌───────┐\n│ ●     │\n│       │\n│     ● │\n└───────┘",
                3: "┌───────┐\n│ ●     │\n│   ●   │\n│     ● │\n└───────┘",
                4: "┌───────┐\n│ ●   ● │\n│       │\n│ ●   ● │\n└───────┘",
                5: "┌───────┐\n│ ●   ● │\n│   ●   │\n│ ●   ● │\n└───────┘",
                6: "┌───────┐\n│ ●   ● │\n│ ●   ● │\n│ ●   ● │\n└───────┘"
            }
            slow(Y + f"You rolled: {roll}\n" + G + dice_faces[roll] + W)
            log("Dice Roll")
        
        elif choice == "5":
            number = random.randint(1, 10)
            slow(Y + "Saya telah memilih angka antara 1-10. Tebak angka tersebut!" + W)
            for attempt in range(3):
                guess = int(input(f"Tebakan {attempt + 1}: "))
                if guess == number:
                    slow(G + "Selamat! Tebakan Anda benar!" + W)
                    log("Number Guessing Game - Win")
                    break
                elif guess < number:
                    slow("Terlalu rendah!")
                else:
                    slow("Terlalu tinggi!")
            else:
                slow(R + f"Game over! Angka yang benar adalah {number}" + W)
                log("Number Guessing Game - Lose")
        
        elif choice == "6":
            options = ["batu", "kertas", "gunting"]
            computer = random.choice(options)
            user = input("Pilih (batu/kertas/gunting): ").lower()
            
            if user not in options:
                slow(R + "Pilihan tidak valid!" + W)
                continue
            
            slow(f"Computer memilih: {computer}")
            
            if user == computer:
                result = "SERI!"
            elif (user == "batu" and computer == "gunting") or \
                 (user == "kertas" and computer == "batu") or \
                 (user == "gunting" and computer == "kertas"):
                result = G + "ANDA MENANG!" + W
            else:
                result = R + "COMPUTER MENANG!" + W
            
            slow(result)
            log(f"Rock Paper Scissors: {user} vs {computer}")
        
        elif choice == "7":
            text = input("Masukkan teks: ")[:10]
            ascii_art = f"""
     ╔══════════════════════════════╗
             ASCII ART             ║
                                  
     ║         {text:^10}           
     ║                               ║
    ══════════════════════════════╝
            """
            slow(G + ascii_art + W)
            log("ASCII Art Generator")

def system_tools():
    """Tools untuk monitoring dan manajemen sistem"""
    while True:
        slow(C + """
[ SYSTEM TOOLS ]
[1] Disk Usage
[2] CPU Usage
[3] Memory Usage
[4] Running Processes
[5] System Uptime
[6] Battery Status
[7] Network Info
[0] Kembali
""" + W)
        choice = input("Pilih > ")
        
        if choice == "0":
            break
        elif choice == "1":
            try:
                disk = psutil.disk_usage('/')
                slow(f"""
Disk Usage:
Total: {disk.total // (1024**3)} GB
Used: {disk.used // (1024**3)} GB
Free: {disk.free // (1024**3)} GB
Usage: {disk.percent}%
                """)
                log("Disk Usage Check")
            except:
                slow(R + "Tidak bisa membaca disk usage" + W)
        
        elif choice == "2":
            try:
                cpu_percent = psutil.cpu_percent(interval=1)
                cpu_count = psutil.cpu_count()
                slow(f"""
CPU Info:
Cores: {cpu_count}
Usage: {cpu_percent}%
                """)
                log("CPU Usage Check")
            except:
                slow(R + "Tidak bisa membaca CPU info" + W)
        
        elif choice == "3":
            try:
                memory = psutil.virtual_memory()
                slow(f"""
Memory Usage:
Total: {memory.total // (1024**3)} GB
Used: {memory.used // (1024**3)} GB
Available: {memory.available // (1024**3)} GB
Usage: {memory.percent}%
                """)
                log("Memory Usage Check")
            except:
                slow(R + "Tidak bisa membaca memory info" + W)
        
        elif choice == "4":
            try:
                processes = []
                for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
                    processes.append(proc.info)
                
                processes.sort(key=lambda x: x['memory_percent'] or 0, reverse=True)
                
                slow("Top 10 Processes by Memory:")
                for i, proc in enumerate(processes[:10]):
                    slow(f"{i+1}. PID: {proc['pid']} | {proc['name']} | Memory: {proc['memory_percent']:.1f}%")
                
                log("Running Processes Check")
            except:
                slow(R + "Tidak bisa membaca processes" + W)
        
        elif choice == "5":
            try:
                boot_time = psutil.boot_time()
                uptime = time.time() - boot_time
                hours = int(uptime // 3600)
                minutes = int((uptime % 3600) // 60)
                slow(f"System Uptime: {hours} jam, {minutes} menit")
                log("System Uptime Check")
            except:
                slow(R + "Tidak bisa membaca uptime" + W)
        
        elif choice == "6":
            try:
                battery = psutil.sensors_battery()
                if battery:
                    slow(f"""
Battery Status:
Percent: {battery.percent}%
Plugged: {'Yes' if battery.power_plugged else 'No'}
Time Left: {battery.secsleft // 3600} jam {(battery.secsleft % 3600) // 60} menit
                    """)
                else:
                    slow(Y + "Battery info tidak tersedia" + W)
                log("Battery Status Check")
            except:
                slow(R + "Tidak bisa membaca battery status" + W)
        
        elif choice == "7":
            try:
                net_io = psutil.net_io_counters()
                slow(f"""
Network Info:
Bytes Sent: {net_io.bytes_sent // 1024} KB
Bytes Received: {net_io.bytes_recv // 1024} KB
Packets Sent: {net_io.packets_sent}
Packets Received: {net_io.packets_recv}
                """)
                log("Network Info Check")
            except:
                slow(R + "Tidak bisa membaca network info" + W)

def about_developer():
    """Menampilkan informasi tentang pengembang aplikasi"""
    while True:
        slow(C + """
[ ABOUT DEVELOPER ]
[1] Profile Developer
[2] Skills & Expertise
[3] Contact Information
[4] View Source Code
[5] License Information
[0] Kembali
""" + W)
        choice = input("Pilih > ")
        
        if choice == "0":
            break
        elif choice == "1":
            slow(G + r"""
╔════════════════════════════════════════╗
║           DEVELOPER PROFILE             ║
╠════════════════════════════════════════╣
║                                        
║  Nama    : MOMONP-Pxl                   ║
║  Role    : Full-Stack Developer        
║  Exp     : 5+ Years                     ║
║  Passion : AI &  design                 ║
║                                        
║  "Creating tools that make life easier"║
║                                        
╚════════════════════════════════════════╝
""" + W)
            log("View Developer Profile")
        
        elif choice == "2":
            slow(Y + """
╔════════════════════════════════════════╗
║          SKILLS & EXPERTISE            
╠════════════════════════════════════════╣
║                                        
║  • Python Programming                  
║  • Web Development                     
║  • AI & Machine Learning                ║
║  • System Automation                    ║
║  • Cybersecurity Basics                
║  • Terminal Applications                ║
║  • Open Source Development              ║
║  • Design all poster,ui/ux              ║
║                                        
╚════════════════════════════════════════╝
""" + W)
            log("View Developer Skills")
        
        elif choice == "3":
            slow(C + """
╔════════════════════════════════════════╗
║         CONTACT INFORMATION             ║
╠════════════════════════════════════════╣
║                                         ║
║  Email   : adhil13062008@gmail.com      ║
║  GitHub  : github.com/Pwds         
║  Website : https://momonpxl-portofolio-001.netlify.app/ ║
║                                        
║  For collaboration, bug reports,       
║  or feature requests, please contact    ║
║  us through the channels above.         ║
║                                        
╚════════════════════════════════════════╝
""" + W)
            log("View Contact Information")
        
        elif choice == "4":
            slow(G + """
╔════════════════════════════════════════╗
║           SOURCE CODE                  
╠════════════════════════════════════════╣
║                                        
║  MOMON-AI is an open source project    
║  built with Python.                     ║
║                                        
║  Main Technologies:                    
║  • Python 3.8+                          ║
║  • Standard Library                    
║  • requests library                     ║
║  • psutil library                       ║
║                                        
║  Repository:                           
║  https://github.com/momon-ai/momon-ai  
║                                         ║
╚════════════════════════════════════════╝
""" + W)
            
            view_code = input("\nLihat source code? (y/n): ").lower()
            if view_code == 'y':
                slow(Y + "\n[Source Code Preview]" + W)
                print("=" * 50)
                with open(__file__, 'r') as f:
                    lines = f.readlines()
                    for i, line in enumerate(lines[:30]):
                        print(f"{i+1:3}: {line}", end='')
                print("=" * 50)
                slow(G + "\n... [truncated] ..." + W)
            log("View Source Code")
        
        elif choice == "5":
            slow(Y + """
╔════════════════════════════════════════╗
║           LICENSE INFORMATION          
╠════════════════════════════════════════╣
║                                        
║  MOMON-AI Terminal Assistant            ║
║  Version: 2.0.0                         ║
║  License: MIT License                   ║
║                                        
║  Copyright (c) 2024 MOMON-AI Team      
║                                         ║
║  Permission is hereby granted, free of 
║  charge, to any person obtaining a      ║
║  copy of this software...               ║
║                                        
║  [Full license text available in       
║   LICENSE file in repository]           ║
║                                        
╚════════════════════════════════════════╝
""" + W)
            log("View License Information")
        
        input("\nTekan ENTER untuk melanjutkan...")

def main():
    load_config()
    load_stats()
    
    while True:
        show_banner()
        show_main_menu()
        choice = input("Pilih > ")
        
        if choice == "1":
            fake_scan()
        elif choice == "2":
            system_info()
        elif choice == "3":
            calculator()
        elif choice == "4":
            text_tools()
        elif choice == "5":
            password_tools()
        elif choice == "6":
            encoder_decoder()
        elif choice == "7":
            random_generator()
        elif choice == "8":
            url_checker()
        elif choice == "9":
            show_history()
        elif choice == "10":
            settings_menu()
        elif choice == "11":
            show_statistics()
        elif choice == "12":
            command_mode()
        elif choice == "13":
            internet_tools()
        elif choice == "14":
            entertainment()
        elif choice == "15":
            system_tools()
        elif choice == "16":
            about_developer()
        elif choice == "0":
            slow(G + "Terima kasih telah menggunakan MOMON-AI!" + W)
            break
        else:
            slow(R + "Pilihan tidak valid!" + W)
        
        if choice != "0":
            input("\nTekan ENTER untuk melanjutkan...")

if __name__ == "__main__":
    main()

