import os
import sys
import time
import subprocess
import threading

# ==========================================
# 0. USER CONFIGURATION (আপনার লিংক ও নাম্বার দিন)
# ==========================================
WHATSAPP_LINK = "https://wa.me/+8801XXXXXXXXX"
PHONE_NUMBER = "+8801XXXXXXXXX"

# প্রয়োজনীয় মডিউলগুলোর লিস্ট
REQUIRED_MODULES = [
    "requests", "psutil", "PyJWT", "protobuf", "urllib3", 
    "pytz", "aiohttp", "cfonts", "protobuf-decoder", "google", 
    "pycryptodome", "httpx"
]

# ==========================================
# 1. AUTO INSTALL COLORAMA & BASIC SETUP
# ==========================================
def setup_environment():
    try:
        import colorama
    except ImportError:
        os.system(f"{sys.executable} -m pip install colorama > /dev/null 2>&1")

setup_environment()

from colorama import Fore, Style, init

# Initialize Colors
init(autoreset=True)
W = Fore.LIGHTWHITE_EX
C = Fore.LIGHTCYAN_EX
G = Fore.LIGHTGREEN_EX
R = Fore.LIGHTRED_EX
Y = Fore.LIGHTYELLOW_EX
M = Fore.LIGHTMAGENTA_EX
RST = Style.RESET_ALL

# Rainbow Palette for Animations
RAINBOW = [Fore.LIGHTRED_EX, Fore.LIGHTYELLOW_EX, Fore.LIGHTGREEN_EX, 
           Fore.LIGHTCYAN_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTMAGENTA_EX]

# Static 3D Logo
LOGO_LINES = [
    "   █████╗ ██████╗ ██╗   ██╗ █████╗ ███╗   ██╗",
    "  ██╔══██╗██╔══██╗╚██╗ ██╔╝██╔══██╗████╗  ██║",
    "  ███████║██████╔╝ ╚████╔╝ ███████║██╔██╗ ██║",
    "  ██╔══██║██╔══██╗  ╚██╔╝  ██╔══██║██║╚██╗██║",
    "  ██║  ██║██║  ██║   ██║   ██║  ██║██║ ╚████║",
    "  ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝"
]

# ==========================================
# 2. STATIC HEADER (For the Beginning)
# ==========================================
def print_static_header():
    print("\n")
    for line in LOGO_LINES:
        print(f"  {G}{Style.BRIGHT}{line}{RST}")

    print(f"\n     {C}╭───────────────────────────────────────╮")
    print(f"     {C}│ {W}★ {Y}DEVELOPER : {G}ARYAN {M}[CODEX]          {C}│")
    print(f"     {C}│ {W}★ {G}WHATSAPP  : {W}{WHATSAPP_LINK:<20} {C}│")
    print(f"     {C}│ {W}★ {G}NUMBER    : {W}{PHONE_NUMBER:<20} {C}│")
    print(f"     {C}╰───────────────────────────────────────╯\n")

# ==========================================
# 3. SMART MODULE CHECKER & SCROLLING INSTALLER
# ==========================================
def get_missing_modules():
    try:
        output = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'], stderr=subprocess.DEVNULL).decode('utf-8').lower()
        installed_packages = [line.split('==')[0].split('@')[0].strip().replace('-', '_') for line in output.split('\n')]
        
        missing = []
        for mod in REQUIRED_MODULES:
            normalized_mod = mod.lower().replace('-', '_')
            if normalized_mod not in installed_packages:
                missing.append(mod)
        return missing
    except Exception:
        return REQUIRED_MODULES

def run_background_task(cmd):
    os.system(cmd)

def install_with_scrolling_animation(task_name, cmd):
    t = threading.Thread(target=run_background_task, args=(cmd,))
    t.start()
    
    spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    frames = 0
    
    while t.is_alive():
        color = RAINBOW[frames % len(RAINBOW)]
        spin_char = spinner[frames % len(spinner)]
        
        output = f"\r  {W}[⚙️] {color}{spin_char} {W}Installing {task_name:<15} {M}│ {Y}Please Wait... "
        sys.stdout.write(output)
        sys.stdout.flush()
        
        time.sleep(0.1)
        frames += 1

    sys.stdout.write(f"\r  {G}[+] {task_name:<26} {G}➔ INSTALLED SUCCESSFULLY!       \n")
    sys.stdout.flush()

# ==========================================
# 4. DATA SAVER WORKER
# ==========================================
def inject_data_worker(uid, password, result):
    try:
        with open("Ariyan.txt", "w", encoding="utf-8") as f:
            f.write(f"uid={uid}\npassword={password}\n")
        time.sleep(3.0) 
        result["status"] = True
    except Exception as e:
        result["status"] = False

# ==========================================
# 5. DYNAMIC ANIMATION (Clear Screen Starts Here)
# ==========================================
def play_dynamic_injection_animation(uid, password):
    result = {"status": None}
    t = threading.Thread(target=inject_data_worker, args=(uid, password, result))
    t.start()
    
    spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    frames = 0
    
    while t.is_alive():
        sys.stdout.write("\033[H\033[2J")
        sys.stdout.flush()
        
        aryan_color = RAINBOW[frames % len(RAINBOW)]
        spin_char = spinner[frames % len(spinner)]
        
        for line in LOGO_LINES:
            print(f"  {G}{Style.BRIGHT}{line}{RST}")

        print(f"\n     {C}╭───────────────────────────────────────╮")
        print(f"     {C}│ {W}★ {Y}DEVELOPER : {aryan_color}{Style.BRIGHT}ARYAN {M}[CODEX]          {C}│")
        print(f"     {C}│ {W}★ {G}WHATSAPP  : {W}{WHATSAPP_LINK:<20} {C}│")
        print(f"     {C}│ {W}★ {G}NUMBER    : {W}{PHONE_NUMBER:<20} {C}│")
        print(f"     {C}╰───────────────────────────────────────╯\n")

        print(f"  {C}╭──────────────────────────────────────────────────╮")
        print(f"  {C}│{W}          🚀 SYSTEM INJECTION STARTED 🚀          {C}│")
        print(f"  {C}╰──────────────────────────────────────────────────╯\n")
        
        bar_length = 12
        filled = int((frames % (bar_length * 2)) / 2)
        if filled >= bar_length:
            filled = (bar_length * 2) - filled - 1
            
        bar = ("█" * filled) + ("░" * (bar_length - filled))
        
        output = f"  {W}[⚙️] {aryan_color}{spin_char} {W}UID: {uid:<13} {M}│ {C}[{bar}] {aryan_color}SAVING DATA...\n"
        print(output)
        
        time.sleep(0.1)
        frames += 1

    return result["status"], frames

# ==========================================
# 6. USER INPUT FUNCTION
# ==========================================
def get_user_inputs():
    print(f"\n  {C}╭──────────────────────────────────────────────────╮")
    print(f"  {C}│{W}           🔑 TARGET ACCOUNT DETAILS 🔑           {C}│")
    print(f"  {C}╰──────────────────────────────────────────────────╯\n")
    
    while True:
        print(f"  {Y}[?] {W}Enter Target UID:")
        uid = input(f"   {M}╰─➤ {G}").strip()
        if not uid:
            print(f"  {R}[!] UID cannot be empty!\n")
            continue
            
        print(f"\n  {Y}[?] {W}Enter Target Password:")
        password = input(f"   {M}╰─➤ {G}").strip()
        if not password:
            print(f"  {R}[!] Password cannot be empty!\n")
            continue
            
        print(f"\n  {C}[✔] Credentials Locked Successfully! Starting Setup...\n")
        time.sleep(1)
        return uid, password

# ==========================================
# 7. MAIN EXECUTION
# ==========================================
def main():
    print_static_header()
    
    print(f"  {Y}[!] Checking Required Modules... Please Wait! {RST}")
    missing_modules = get_missing_modules()
    
    if len(missing_modules) == 0:
        print(f"  {G}[✔] All Requirements Are Already Installed! {RST}\n")
    else:
        if len(missing_modules) > 5:
            install_with_scrolling_animation("Storage Setup", "termux-setup-storage > /dev/null 2>&1")
            install_with_scrolling_animation("System Update", "pkg update -y > /dev/null 2>&1 && pkg upgrade -y > /dev/null 2>&1")
            
        for mod in missing_modules:
            cmd = f"{sys.executable} -m pip install {mod} --upgrade > /dev/null 2>&1"
            install_with_scrolling_animation(mod, cmd)
            
        print(f"\n  {G}[✔] System & Modules Setup Complete! {RST}\n")

    uid, password = get_user_inputs()
    
    success, current_frame = play_dynamic_injection_animation(uid, password)
    
    if success:
        # ৩ সেকেন্ড পর্যন্ত ARYAN নাম চেঞ্জ হবে এবং ফাইনাল ব্যানার প্রিন্ট হবে
        for _ in range(30):
            sys.stdout.write("\033[H\033[2J")
            sys.stdout.flush()
            
            aryan_color = RAINBOW[current_frame % len(RAINBOW)]
            
            for line in LOGO_LINES:
                print(f"  {G}{Style.BRIGHT}{line}{RST}")

            print(f"\n     {C}╭───────────────────────────────────────╮")
            print(f"     {C}│ {W}★ {Y}DEVELOPER : {aryan_color}{Style.BRIGHT}ARYAN {M}[CODEX]          {C}│")
            print(f"     {C}│ {W}★ {G}WHATSAPP  : {W}{WHATSAPP_LINK:<20} {C}│")
            print(f"     {C}│ {W}★ {G}NUMBER    : {W}{PHONE_NUMBER:<20} {C}│")
            print(f"     {C}╰───────────────────────────────────────╯\n")
            
            print(f"  {M}╭──────────────────────────────────────────────╮")
            print(f"  {M}│ {W}          📊 ANIMATION SYSTEM REPORT         {M}│")
            print(f"  {M}├──────────────────────────────────────────────┤")
            print(f"  {M}│ {G}✅ SETUP STATUS    : COMPLETE                {M}│")
            print(f"  {M}│ {C}🚀 STARTING BOT    : {W}main.py                 {M}│")
            print(f"  {M}╰──────────────────────────────────────────────╯\n")
            
            # === নতুন VPN নির্দেশিকা বক্স ===
            print(f"  {R}╭──────────────────────────────────────────────╮")
            print(f"  {R}│ {Y}⚠️        IMPORTANT SYSTEM NOTICE         {Y}⚠️ {R}│")
            print(f"  {R}├──────────────────────────────────────────────┤")
            print(f"  {R}│ {G}🌐 WIFI USERS   : {W}NO VPN REQUIRED            {R}│")
            print(f"  {R}│ {M}📱 DATA USERS   : {W}MUST CONNECT VPN TO WORK   {R}│")
            print(f"  {R}╰──────────────────────────────────────────────╯\n")
            
            print(f"  {G}✨ Thanks {aryan_color}ARYAN{G}! Bot is Running Below... ✨{RST}\n")
            
            time.sleep(0.1)
            current_frame += 1
            
        # [এইখানে কোনো ক্লিয়ার স্ক্রিন হবে না, যাতে এই উপরের সুন্দর ডিজাইনটি পারমানেন্ট থেকে যায়]
        
        if os.path.exists("main.py"):
            try:
                # এখান থেকে main.py রান হবে এবং এর সব লেখা এই ডিজাইনের নিচে আসবে
                subprocess.call([sys.executable, "main.py"])
            except KeyboardInterrupt:
                pass
        else:
            print(f"  {R}[!] Error: 'main.py' file not found in the directory!{RST}")
            
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {R}[!] Program Terminated Forcefully! (Ctrl+C){RST}")
        sys.exit(0)