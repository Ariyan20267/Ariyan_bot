import os
import sys
import time
import subprocess
import threading
import warnings

# ==========================================
#        1. BASIC SETUP (COLORAMA ONLY)
# ==========================================
# Suppress all deprecation and user warnings securely
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

def setup_colorama():
    try:
        import colorama
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama"], 
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

setup_colorama()
from colorama import Fore, Style, init

# Initialize Colors
init(autoreset=True)
W = Fore.LIGHTWHITE_EX
C = Fore.LIGHTCYAN_EX
G = Fore.LIGHTGREEN_EX
R = Fore.LIGHTRED_EX
Y = Fore.LIGHTYELLOW_EX
M = Fore.LIGHTMAGENTA_EX
B = Fore.LIGHTBLUE_EX
RST = Style.RESET_ALL

RAINBOW = [Fore.LIGHTRED_EX, Fore.LIGHTYELLOW_EX, Fore.LIGHTGREEN_EX, 
           Fore.LIGHTCYAN_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTMAGENTA_EX]

# ==========================================
#              CONFIGURATION
# ==========================================
# এখানে আপনার লিংক এবং নাম্বার বসিয়ে দিন:
WHATSAPP_LINK = "https://chat.whatsapp.com/LMO2lqCnie7HRFL8pIKzAH?mode=gi_t"
TELEGRAM_LINK = "Ariyan_ff_bot_devolpar" # আপনার টেলিগ্রাম লিংক দিন
PHONE_NUMBER  = "+01610369115" # আপনার নাম্বার দিন

TARGET_MAIN_FILE = "main.py"
TEMP_TXT_FILE = "ARIYAN.txt" # আপনার নির্দেশমতো ফাইলের নাম ARIYAN.txt দেওয়া হয়েছে

# ==========================================
#        VIP ANIMATION UTILITIES
# ==========================================
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def typewriter_effect(text, speed=0.02, color=W):
    for char in text:
        sys.stdout.write(f"{color}{Style.BRIGHT}{char}{RST}")
        sys.stdout.flush()
        time.sleep(speed)
    print()

def animated_logo():
    clear_screen()
    logo = [
        "      █████╗ ██████╗ ██╗   ██╗ █████╗ ███╗   ██╗",
        "     ██╔══██╗██╔══██╗╚██╗ ██╔╝██╔══██╗████╗  ██║",
        "     ███████║██████╔╝ ╚████╔╝ ███████║██╔██╗ ██║",
        "     ██╔══██║██╔══██╗  ╚██╔╝  ██╔══██║██║╚██╗██║",
        "     ██║  ██║██║  ██║   ██║   ██║  ██║██║ ╚████║",
        "     ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝"
    ]
    
    # Logo Rainbow Animation
    for i in range(8):  
        sys.stdout.write("\033[H")
        color = RAINBOW[i % len(RAINBOW)]
        print("\n")
        for line in logo:
            print(f"  {color}{Style.BRIGHT}{line}{RST}")
        time.sleep(0.08)

    # VIP Info Panel with Contacts
    print(f"\n  {C}╔═════════════════════════════════════════════════════╗")
    print(f"  {C}║  {Y}[👤] {W}DEVELOPER : {G}ARYAN [CODEX]                   {C}║")
    print(f"  {C}║  {Y}[👑] {W}STATUS    : {M}VIP PREMIUM EDITION             {C}║")
    print(f"  {C}║  {Y}[📞] {W}WHATSAPP  : {C}JOIN VIA LINK BELOW             {C}║")
    print(f"  {C}║  {Y}[✈️]  {W}TELEGRAM  : {C}JOIN VIA LINK BELOW             {C}║")
    print(f"  {C}║  {Y}[📱] {W}NUMBER    : {G}{PHONE_NUMBER:<31} {C}║")
    print(f"  {C}╚═════════════════════════════════════════════════════╝\n")

# ==========================================
#   2. SMART VIP MODULE INSTALLER
# ==========================================
def get_missing_packages():
    packages = [
        "requests", "httpx", "google", "protobuf", "pycryptodome", 
        "psutil", "PyJWT", "urllib3", "protobuf-decoder", "pytz", 
        "aiohttp", "cfonts", "Flask"
    ]
    missing = []
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            import pkg_resources
            installed = {pkg.key.lower() for pkg in pkg_resources.working_set}
            for pkg in packages:
                if pkg.lower() not in installed:
                    missing.append(pkg)
    except Exception:
        missing = packages 
    return missing

def install_packages_worker(result, packages_to_install):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q"] + packages_to_install,
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass
    result["done"] = True

def animated_module_installer():
    missing_packages = get_missing_packages()
    
    if not missing_packages:
        return 

    result = {"done": False}
    t = threading.Thread(target=install_packages_worker, args=(result, missing_packages))
    t.start()
    
    spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    frames = 0
    
    while t.is_alive():
        color = RAINBOW[frames % len(RAINBOW)]
        spin_char = spinner[frames % len(spinner)]
        
        bar_length = 15
        filled = int((frames % (bar_length * 2)) / 2)
        if filled >= bar_length:
            filled = (bar_length * 2) - filled - 1
            
        bar = ("█" * filled) + ("░" * (bar_length - filled))
        
        output = f"\r  {color}{spin_char} {W}INSTALLING MODULES... {M}│ {C}[{bar}] {color}PROCESSING... "
        sys.stdout.write(output.ljust(80))
        sys.stdout.flush()
        
        time.sleep(0.04)
        frames += 1

    sys.stdout.write("\r" + " " * 85 + "\r")
    print(f"  {G}✔ REQUIRED MODULES INSTALLED SUCCESSFULLY!{RST}\n")
    time.sleep(1)

def fake_injection_progress_neon():
    print(f"\n  {C}╭─── [ INITIATING SECURE INJECTION ]")
    spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    
    for i in range(101):
        color = RAINBOW[i % len(RAINBOW)]
        spin_char = spinner[i % len(spinner)]
        
        bar_length = 15
        filled = int((i % (bar_length * 2)) / 2)
        if filled >= bar_length:
            filled = (bar_length * 2) - filled - 1
            
        bar = ("█" * filled) + ("░" * (bar_length - filled))
        
        output = f"\r  {C}│  {color}{spin_char} {W}PROGRESS: {C}[{bar}] {color}{i}% INJECTING... "
        sys.stdout.write(output.ljust(65))
        sys.stdout.flush()
        time.sleep(0.02)
        
    print(f"\n  {C}╰────────────────────────────────────────────────╮")
    print(f"  {C}│  {G}✔ ACCESS GRANTED! LAUNCHING MAIN PAYLOAD...   {C}│")
    print(f"  {C}╰────────────────────────────────────────────────╯\n")
    time.sleep(1)

def cleanup_files():
    if os.path.exists(TEMP_TXT_FILE):
        try:
            os.remove(TEMP_TXT_FILE)
        except Exception:
            pass

# ==========================================
#               MAIN LOGIC
# ==========================================
def main():
    # 1. Start Directly with Animated Logo!
    animated_logo()
    
    # 2. Check for Modules
    animated_module_installer()

    # মেইন ফাইলটি আছে কি না তা যাচাই করা
    if not os.path.exists(TARGET_MAIN_FILE):
        print(f"  {R} [✖] ERROR: '{TARGET_MAIN_FILE}' NOT FOUND IN THIS DIRECTORY!{RST}\n")
        sys.exit()

    # 3. আগের সব ক্লিয়ার করে সুন্দর লগিন পোর্টাল
    clear_screen()
    print("\n\n")
    print(f"  {Y}╔═════════════════════════════════════════════════════╗")
    print(f"  {Y}║              {W}🔐 SECURE LOGIN PORTAL 🔐              {Y}║")
    print(f"  {Y}╠═════════════════════════════════════════════════════╣")
    
    sys.stdout.write(f"  {Y}║ {C}[➤] ENTER UID      {W}:{G} ")
    sys.stdout.flush()
    uid = input().strip()
    
    sys.stdout.write(f"  {Y}║ {C}[➤] ENTER PASSWORD {W}:{G} ")
    sys.stdout.flush()
    password = input().strip()
    print(f"  {Y}╚═════════════════════════════════════════════════════╝")

    if not uid or not password:
        print(f"\n  {R} [!] UID AND PASSWORD CANNOT BE EMPTY! ACCESS DENIED.{RST}")
        sys.exit()

    try:
        # Secret File Creation (ARIYAN.txt এর ভেতর {"UID": "PASSWORD"} হুবহু এরকম সেভ হবে)
        with open(TEMP_TXT_FILE, "w", encoding="utf-8") as f:
            f.write(f'{{"{uid}": "{password}"}}')
            
        # 4. Neon Injection Bar (0-100%)
        fake_injection_progress_neon()
        
        # 5. Run Target Script Directly
        subprocess.run([sys.executable, TARGET_MAIN_FILE])
        
    except KeyboardInterrupt:
        print(f"\n\n  {R} [!] SYSTEM TERMINATED FORCEFULLY BY USER! (Ctrl+C){RST}")
    except Exception as e:
        print(f"\n  {R} [✖] UNEXPECTED SYSTEM ERROR: {e}{RST}")
    finally:
        # Script শেষ হয়ে গেলে ফাইল অটো ডিলিট করে দেবে
        cleanup_files()
        print(f"\n  {M}✨ PREPARED BY ARYAN | SESSION COMPLETED SAFELY ✨{RST}\n")

if __name__ == "__main__":
    main()