from flask import Flask, request, jsonify, render_template_string, redirect, url_for, session
import asyncio
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import binascii
import aiohttp
import json
import like_pb2
import like_count_pb2
import uid_generator_pb2
import sqlite3
import urllib3
from datetime import datetime
import os

# ---------- কনফিগারেশন ----------
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
DATABASE = 'ariyan_likes.db'
ADMIN_USERNAME = 'ARIYAN'
ADMIN_PASSWORD = 'nobita@#$321'

# আপনার টোকেন জেনারেটর স্ক্রিপ্ট যেই ফাইলগুলোতে টোকেন সেভ করবে তার নাম
TOKEN_FILES = {
    'BD': 'account_bd.json',
    'IND': 'account_ind.json',
    'BR': 'account_br.json',
    'US': 'account_us.json',
    'SAC': 'account_sac.json',
    'NA': 'account_na.json'
}

# ---------- ডাটাবেস সেটআপ ----------
def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    # ডেইলি লাইক লিমিট ট্র্যাক করার জন্য
    c.execute('''CREATE TABLE IF NOT EXISTS daily_limits
                 (uid TEXT PRIMARY KEY, last_date TEXT)''')
    # অ্যাডমিনকে দেখানোর জন্য কে কে লাইক নিলো তার হিস্ট্রি
    c.execute('''CREATE TABLE IF NOT EXISTS like_history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  uid TEXT, server TEXT, increment INTEGER, date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    # অ্যাডমিন প্যানেল থেকে বট একাউন্ট (গেস্ট) সেভ করার জন্য
    c.execute('''CREATE TABLE IF NOT EXISTS bot_accounts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  uid TEXT UNIQUE, password TEXT)''')
    conn.commit()
    conn.close()
    export_bots_to_txt() # স্টার্ট হওয়ার সময় account.txt আপডেট করবে

def check_daily_limit(uid):
    today = datetime.now().strftime('%Y-%m-%d')
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT last_date FROM daily_limits WHERE uid=?", (uid,))
    row = c.fetchone()
    conn.close()
    if row and row[0] == today:
        return False # আজকে নিয়ে নিয়েছে
    return True # আজকে নিতে পারবে

def update_daily_limit(uid):
    today = datetime.now().strftime('%Y-%m-%d')
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO daily_limits (uid, last_date) VALUES (?, ?)", (uid, today))
    conn.commit()
    conn.close()

def log_like_history(uid, server, increment):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO like_history (uid, server, increment) VALUES (?, ?, ?)", (uid, server, increment))
    conn.commit()
    conn.close()

def get_today_history():
    today = datetime.now().strftime('%Y-%m-%d')
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT uid, server, increment, date_time FROM like_history WHERE date_time LIKE ? ORDER BY id DESC", (f"{today}%",))
    rows = c.fetchall()
    conn.close()
    return rows

# ---------- বট একাউন্ট ম্যানেজমেন্ট ----------
def export_bots_to_txt():
    """বট একাউন্টগুলো account.txt ফাইলে সেভ করে যাতে token_generator.py ব্যবহার করতে পারে"""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT uid, password FROM bot_accounts")
    rows = c.fetchall()
    conn.close()
    try:
        with open('account.txt', 'w', encoding='utf-8') as f:
            for row in rows:
                f.write(f"{row[0]}:{row[1]}\n")
    except Exception as e:
        print("Error saving account.txt:", e)

def add_bot_account(uid, password):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO bot_accounts (uid, password) VALUES (?, ?)", (uid, password))
        conn.commit()
    except:
        pass # Already exists
    conn.close()
    export_bots_to_txt()

def get_all_bots():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT id, uid, password FROM bot_accounts")
    rows = c.fetchall()
    conn.close()
    return rows

def delete_bot(bot_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("DELETE FROM bot_accounts WHERE id=?", (bot_id,))
    conn.commit()
    conn.close()
    export_bots_to_txt()

# ---------- টোকেন লোডিং (লোকাল ফাইল থেকে) ----------
def load_tokens_from_file(server_name):
    if server_name not in TOKEN_FILES:
        return []
    path = TOKEN_FILES[server_name]
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # JSON array format: [{"token": "eyJ..."}, ...]
            return [item['token'] for item in data if 'token' in item]
    except Exception:
        return []

# ---------- এনক্রিপশন ও প্রোটোবাফ ----------
def encrypt_message(plaintext):
    key = b'Yg&tc%DEuh6%Zc^8'
    iv = b'6oyZDr22E3ychjM%'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(plaintext, AES.block_size)
    encrypted_message = cipher.encrypt(padded_message)
    return binascii.hexlify(encrypted_message).decode('utf-8')

def create_protobuf_message(user_id, region):
    message = like_pb2.like()
    message.uid = int(user_id)
    message.region = region
    return message.SerializeToString()

def create_protobuf_for_profile_check(uid):
    message = uid_generator_pb2.uid_generator()
    message.krishna_ = int(uid)
    message.teamXdarks = 1
    return message.SerializeToString()

def enc_profile_check_payload(uid):
    protobuf_data = create_protobuf_for_profile_check(uid)
    return encrypt_message(protobuf_data)

# ---------- লাইক পাঠানো ----------
async def send_single_like_request(session, encrypted_like_payload, token, url):
    if not token:
        return 999
    edata = bytes.fromhex(encrypted_like_payload)
    headers = {
        'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'Authorization': f"Bearer {token}",
        'Content-Type': "application/x-www-form-urlencoded",
        'Expect': "100-continue",
        'X-Unity-Version': "2018.4.11f1",
        'X-GA': "v1 1",
        'ReleaseVersion': "OB52"
    }
    try:
        async with session.post(url, data=edata, headers=headers, timeout=10) as response:
            return response.status
    except:
        return 997

async def send_likes_with_token_list(session, uid, server_region, like_api_url, token_list):
    if not token_list:
        return 0
    like_payload = create_protobuf_message(uid, server_region)
    encrypted = encrypt_message(like_payload)
    tasks = [send_single_like_request(session, encrypted, token, like_api_url) for token in token_list]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return sum(1 for r in results if isinstance(r, int) and r == 200)

def run_send_likes(uid, server_region, like_api_url, token_list):
    async def _run():
        async with aiohttp.ClientSession() as session:
            return await send_likes_with_token_list(session, uid, server_region, like_api_url, token_list)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(_run())
    finally:
        loop.close()

# ---------- প্রোফাইল চেক ----------
async def make_profile_check_request_async(session, encrypted_payload, server_name, token):
    if not token:
        return None
    if server_name == "IND":
        url = "https://client.ind.freefiremobile.com/GetPlayerPersonalShow"
    elif server_name in {"BR", "US", "SAC", "NA"}:
        url = "https://client.us.freefiremobile.com/GetPlayerPersonalShow"
    else:
        url = "https://clientbp.ggblueshark.com/GetPlayerPersonalShow"
    edata = bytes.fromhex(encrypted_payload)
    headers = {
        'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'Authorization': f"Bearer {token}",
        'Content-Type': "application/x-www-form-urlencoded",
        'Expect': "100-continue",
        'X-Unity-Version': "2018.4.11f1",
        'X-GA': "v1 1",
        'ReleaseVersion': "OB52"
    }
    try:
        async with session.post(url, data=edata, headers=headers, timeout=10) as response:
            if response.status != 200:
                return None
            binary_data = await response.read()
            items = like_count_pb2.Info()
            items.ParseFromString(binary_data)
            return items
    except:
        return None

async def get_profile_info_async(session, uid, server_name, token):
    encrypted = enc_profile_check_payload(uid)
    info = await make_profile_check_request_async(session, encrypted, server_name, token)
    if info and hasattr(info, 'AccountInfo'):
        likes = int(info.AccountInfo.Likes)
        nickname = str(info.AccountInfo.PlayerNickname) if info.AccountInfo.PlayerNickname else "N/A"
        uid_from = int(info.AccountInfo.UID) if info.AccountInfo.UID else int(uid)
        return likes, nickname, uid_from
    return None, None, None

def run_profile_check(uid, server_name, token):
    async def _run():
        async with aiohttp.ClientSession() as session:
            return await get_profile_info_async(session, uid, server_name, token)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(_run())
    finally:
        loop.close()

# ---------- Flask অ্যাপ ----------
app = Flask(__name__)
app.secret_key = os.urandom(24)
init_db()

# ==========================================================
# CUTE & COLORFUL HTML TEMPLATES
# ==========================================================

INDEX_HTML = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌸 ARIYAN FF LIKES 🌸</title>
    <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600;700&family=Baloo+Da+2:wght@500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Quicksand', 'Baloo Da 2', sans-serif;
            background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 99%, #fecfef 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            overflow-x: hidden;
        }
        /* Cute floating bubbles background */
        .bubble {
            position: absolute;
            background: rgba(255, 255, 255, 0.4);
            border-radius: 50%;
            animation: float 8s infinite ease-in-out;
            z-index: 0;
        }
        @keyframes float {
            0%, 100% { transform: translateY(0) scale(1); }
            50% { transform: translateY(-20px) scale(1.1); }
        }
        
        .container {
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px);
            max-width: 500px;
            width: 100%;
            border-radius: 30px;
            padding: 40px 30px;
            box-shadow: 0 15px 35px rgba(255, 105, 180, 0.2);
            text-align: center;
            position: relative;
            z-index: 10;
            border: 3px solid #fff;
        }
        .header h1 {
            color: #ff6b81;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 10px;
            text-shadow: 2px 2px 0px #ffeaa7;
        }
        .header p {
            color: #7bed9f;
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 30px;
            background: #f1f2f6;
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
        }
        .input-group { margin-bottom: 20px; text-align: left; }
        .input-group label {
            display: block;
            color: #ff4757;
            font-weight: 700;
            margin-bottom: 8px;
            font-size: 1rem;
        }
        input, select {
            width: 100%;
            padding: 15px;
            border: 2px solid #ffeaa7;
            border-radius: 20px;
            font-size: 1rem;
            font-family: 'Quicksand', sans-serif;
            color: #2f3542;
            background: #fff;
            transition: all 0.3s;
            outline: none;
        }
        input:focus, select:focus {
            border-color: #ff6b81;
            box-shadow: 0 0 15px rgba(255, 107, 129, 0.2);
            transform: scale(1.02);
        }
        .btn-submit {
            background: linear-gradient(45deg, #ff6b81, #ff7f50);
            color: white;
            border: none;
            width: 100%;
            padding: 15px;
            border-radius: 20px;
            font-size: 1.2rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 5px 15px rgba(255, 107, 129, 0.4);
            margin-top: 10px;
        }
        .btn-submit:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(255, 107, 129, 0.6);
        }
        .btn-submit:active { transform: translateY(1px); }
        .btn-submit.loading { opacity: 0.7; pointer-events: none; }
        
        .result-box {
            margin-top: 25px;
            background: #f1f2f6;
            border-radius: 20px;
            padding: 20px;
            display: none;
            animation: popIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            border: 2px dashed #ff6b81;
        }
        @keyframes popIn {
            0% { transform: scale(0.8); opacity: 0; }
            100% { transform: scale(1); opacity: 1; }
        }
        .result-item {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            border-bottom: 1px solid #dfe4ea;
            padding-bottom: 5px;
        }
        .result-item span:first-child { font-weight: 700; color: #747d8c; }
        .result-item span:last-child { font-weight: 700; color: #ff4757; }
        
        .footer { margin-top: 25px; }
        .footer a {
            color: #ff6b81;
            text-decoration: none;
            font-weight: 700;
            font-size: 0.9rem;
            border: 2px solid #ff6b81;
            padding: 5px 15px;
            border-radius: 20px;
            transition: all 0.3s;
        }
        .footer a:hover {
            background: #ff6b81;
            color: white;
        }
    </style>
</head>
<body>
    <!-- Background Bubbles -->
    <div class="bubble" style="width: 80px; height: 80px; top: 10%; left: 10%;"></div>
    <div class="bubble" style="width: 120px; height: 120px; top: 70%; left: 80%; animation-delay: 2s;"></div>
    <div class="bubble" style="width: 50px; height: 50px; top: 40%; left: 90%; animation-delay: 4s;"></div>
    <div class="bubble" style="width: 90px; height: 90px; top: 80%; left: 15%; animation-delay: 1s;"></div>

    <div class="container">
        <div class="header">
            <h1>🌸 ARIYAN FF 🌸</h1>
            <p>✨ Free Fire Auto Likes ✨</p>
        </div>

        <form id="likeForm">
            <div class="input-group">
                <label><i class="fas fa-gamepad"></i> তোমার গেম UID দাও</label>
                <input type="number" name="uid" placeholder="Example: 123456789" required>
            </div>
            
            <div class="input-group">
                <label><i class="fas fa-globe"></i> সার্ভার সিলেক্ট করো</label>
                <select name="server_name" required>
                    <option value="BD">🇧🇩 Bangladesh</option>
                    <option value="IND">🇮🇳 India</option>
                    <option value="BR">🇧🇷 Brazil</option>
                    <option value="US">🇺🇸 USA</option>
                    <option value="SAC">🌍 SAC</option>
                    <option value="NA">🌍 NA</option>
                </select>
            </div>
            
            <button type="submit" class="btn-submit" id="likeBtn">
                <i class="fas fa-heart"></i> লাইক নাও! 💖
            </button>
        </form>

        <div class="result-box" id="resultBox">
            <h3 style="color: #2ed573; margin-bottom: 15px;" id="statusMsg">✅ সফল হয়েছে!</h3>
            <div class="result-item"><span>নাম:</span> <span id="r_name">N/A</span></div>
            <div class="result-item"><span>UID:</span> <span id="r_uid">N/A</span></div>
            <div class="result-item"><span>আগের লাইক:</span> <span id="r_before">0</span></div>
            <div class="result-item"><span>এখন লাইক:</span> <span id="r_after">0</span></div>
            <div class="result-item"><span>প্লাস হয়েছে:</span> <span style="color: #2ed573; font-size: 1.2rem;" id="r_given">+0</span></div>
        </div>

        <div class="footer">
            <p style="margin-bottom: 10px; color: #a4b0be; font-size: 0.9rem;">প্রতিদিন ১ বার করে নিতে পারবে! 🎀</p>
            <a href="/admin/login"><i class="fas fa-lock"></i> Admin Panel</a>
        </div>
    </div>

    <script>
        document.getElementById('likeForm').onsubmit = async function(e) {
            e.preventDefault();
            const btn = document.getElementById('likeBtn');
            const resultBox = document.getElementById('resultBox');
            
            btn.classList.add('loading');
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> লাইক যাচ্ছে...';
            resultBox.style.display = 'none';
            
            const form = new FormData(this);
            const params = new URLSearchParams(form).toString();
            
            try {
                const res = await fetch('/like?' + params);
                const data = await res.json();
                
                document.getElementById('r_name').textContent = data.Nickname || 'N/A';
                document.getElementById('r_uid').textContent = data.UID || 'N/A';
                document.getElementById('r_before').textContent = data.Before || 'N/A';
                document.getElementById('r_after').textContent = data.After || 'N/A';
                document.getElementById('r_given').textContent = '+' + (data.Given || '0');
                
                const statusMsg = document.getElementById('statusMsg');
                if (data.Status === 1) {
                    statusMsg.innerHTML = '🎉 ওয়াও! লাইক সেন্ড হয়েছে!';
                    statusMsg.style.color = '#2ed573';
                } else if (data.Status === -1) {
                    statusMsg.innerHTML = '⚠️ ' + data.Message;
                    statusMsg.style.color = '#ff4757';
                } else {
                    statusMsg.innerHTML = '😢 ' + (data.Message || 'কিছু সমস্যা হয়েছে!');
                    statusMsg.style.color = '#ffa502';
                }
                
                resultBox.style.display = 'block';
            } catch (error) {
                alert('সার্ভার এরর! একটু পর ট্রাই করুন 🌸');
            } finally {
                btn.classList.remove('loading');
                btn.innerHTML = '<i class="fas fa-heart"></i> লাইক নাও! 💖';
            }
        };
    </script>
</body>
</html>
"""

ADMIN_HTML = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌸 Admin - ARIYAN 🌸</title>
    <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        body {
            font-family: 'Quicksand', sans-serif;
            background: #f8a5c2;
            padding: 20px;
            color: #303952;
        }
        .admin-container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 30px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 3px dashed #f8a5c2;
            padding-bottom: 15px;
            margin-bottom: 25px;
        }
        .header h1 { color: #e15f41; font-weight: 700; }
        .btn-logout {
            background: #e15f41; color: white; padding: 8px 20px; border-radius: 20px; text-decoration: none; font-weight: 700;
        }
        .stats-box {
            background: #f3a683; color: white; padding: 20px; border-radius: 20px; margin-bottom: 25px; font-size: 1.2rem; font-weight: 700; text-align: center;
        }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        @media (max-width: 768px) { .grid { grid-template-columns: 1fr; } }
        
        .card { background: #fdf1f3; padding: 20px; border-radius: 20px; border: 2px solid #f8a5c2; }
        .card h2 { color: #e15f41; margin-bottom: 15px; font-size: 1.3rem; }
        table { width: 100%; border-collapse: collapse; background: white; border-radius: 10px; overflow: hidden; }
        th, td { padding: 10px; text-align: left; border-bottom: 1px solid #f8a5c2; }
        th { background: #f8a5c2; color: white; }
        
        input { width: 100%; padding: 10px; margin-bottom: 10px; border: 2px solid #f8a5c2; border-radius: 10px; outline: none;}
        .btn-add { background: #786fa6; color: white; border: none; padding: 10px; width: 100%; border-radius: 10px; font-weight: bold; cursor: pointer; }
        .btn-del { background: #e15f41; color: white; text-decoration: none; padding: 4px 10px; border-radius: 10px; font-size: 0.8rem; }
    </style>
</head>
<body>
    <div class="admin-container">
        <div class="header">
            <h1>🌸 ARIYAN Admin Panel 🌸</h1>
            <a href="/admin/logout" class="btn-logout"><i class="fas fa-sign-out-alt"></i> Logout</a>
        </div>
        
        <div class="stats-box">
            আজকে মোট লাইক নিয়েছে: {{ today_history|length }} জন ✨
        </div>

        <div class="grid">
            <!-- Daily History Table -->
            <div class="card">
                <h2><i class="fas fa-history"></i> আজকের লাইক হিস্ট্রি</h2>
                <div style="max-height: 400px; overflow-y: auto;">
                    <table>
                        <tr><th>UID</th><th>Server</th><th>Given</th><th>Time</th></tr>
                        {% for row in today_history %}
                        <tr>
                            <td>{{ row[0] }}</td>
                            <td>{{ row[1] }}</td>
                            <td style="color:#2ed573; font-weight:bold;">+{{ row[2] }}</td>
                            <td style="font-size: 0.8rem;">{{ row[3][11:19] }}</td>
                        </tr>
                        {% else %}
                        <tr><td colspan="4" style="text-align:center;">আজকে কেউ লাইক নেয়নি 😢</td></tr>
                        {% endfor %}
                    </table>
                </div>
            </div>

            <!-- Bot Account Manager -->
            <div class="card">
                <h2><i class="fas fa-robot"></i> বট একাউন্ট (Guest UID/Pass)</h2>
                <p style="font-size: 0.9rem; color: #574b90; margin-bottom: 10px;">এখানে যা সেভ করবেন তা অটোমেটিক <b>account.txt</b> এ সেভ হবে।</p>
                <form action="/admin/add_bot" method="post" style="margin-bottom: 20px;">
                    <input type="number" name="uid" placeholder="Bot UID (Ex: 12345678)" required>
                    <input type="text" name="password" placeholder="Bot Password" required>
                    <button type="submit" class="btn-add"><i class="fas fa-plus"></i> সেভ করুন</button>
                </form>
                
                <div style="max-height: 250px; overflow-y: auto;">
                    <table>
                        <tr><th>UID</th><th>Password</th><th>Action</th></tr>
                        {% for bot in bots %}
                        <tr>
                            <td>{{ bot[1] }}</td>
                            <td>{{ bot[2][:4] }}***</td>
                            <td><a href="/admin/del_bot/{{ bot[0] }}" class="btn-del">Delete</a></td>
                        </tr>
                        {% endfor %}
                    </table>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

LOGIN_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Admin Login 🌸</title>
    <style>
        body { font-family: 'Quicksand', sans-serif; background: #f8a5c2; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
        .box { background: white; padding: 40px; border-radius: 30px; text-align: center; box-shadow: 0 10px 20px rgba(0,0,0,0.1); width: 300px; }
        input { width: 90%; padding: 10px; margin: 10px 0; border: 2px solid #f8a5c2; border-radius: 15px; outline: none; }
        button { background: #e15f41; color: white; border: none; padding: 10px 20px; border-radius: 15px; font-weight: bold; cursor: pointer; width: 100%; }
    </style>
</head>
<body>
    <div class="box">
        <h2 style="color: #e15f41;">🌸 ARIYAN Admin 🌸</h2>
        <form method="post">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">LOGIN</button>
        </form>
    </div>
</body>
</html>
"""

# ==========================================================
# FLASK ROUTES
# ==========================================================

@app.route('/')
def index():
    return render_template_string(INDEX_HTML)

@app.route('/like', methods=['GET'])
def handle_like():
    uid = request.args.get("uid", "").strip()
    server = request.args.get("server_name", "").strip().upper()
    
    if not uid or not server:
        return jsonify({"Status": -2, "Message": "UID বা সার্ভার দেওয়া হয়নি!"})

    # ১. চেক করুন ইউজার আজকে লাইক নিয়েছে কিনা
    if not check_daily_limit(uid):
        return jsonify({
            "Status": -1,
            "Message": "তুমি আজকে লাইক নিয়ে নিয়েছো! কালকে আবার এসো 🌸",
            "UID": uid, "Before": "N/A", "After": "N/A", "Given": 0
        })

    # ২. লোকাল ফাইল থেকে টোকেন লোড করুন
    tokens = load_tokens_from_file(server)
    if not tokens:
        return jsonify({
            "Status": -2, 
            "Message": f"আমাদের সিস্টেমে {server} সার্ভারের টোকেন শেষ! অ্যাডমিনকে জানান 😢"
        })

    # ৩. আগের লাইক চেক
    before_likes, nickname, uid_from = run_profile_check(uid, server, tokens[0])
    if before_likes is None:
        return jsonify({"Status": -2, "Message": "UID টি ভুল অথবা গেম সার্ভার ডাউন!"})

    # ৪. লাইক পাঠানো
    if server == "IND":
        like_api_url = "https://client.ind.freefiremobile.com/LikeProfile"
    elif server in {"BR", "US", "SAC", "NA"}:
        like_api_url = "https://client.us.freefiremobile.com/LikeProfile"
    else:
        like_api_url = "https://clientbp.ggblueshark.com/LikeProfile"

    success_count = run_send_likes(uid, server, like_api_url, tokens)

    # ৫. পরের লাইক চেক
    after_likes, _, _ = run_profile_check(uid, server, tokens[0])
    if after_likes is None:
        after_likes = before_likes + success_count # Fallback calculation

    increment = after_likes - before_likes

    if increment > 0:
        # সফল হলে ডেইলি লিমিটে যোগ করুন এবং হিস্ট্রিতে সেভ করুন
        update_daily_limit(uid)
        log_like_history(uid, server, increment)
        status = 1
    else:
        status = 0

    return jsonify({
        "Nickname": nickname,
        "UID": uid_from,
        "Before": before_likes,
        "After": after_likes,
        "Given": increment,
        "Status": status,
        "Message": ""
    })

# ========== ADMIN ROUTES ==========

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form['username'] == ADMIN_USERNAME and request.form['password'] == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('admin_panel'))
        return "ভুল ইউজারনেম বা পাসওয়ার্ড ❌", 401
    return render_template_string(LOGIN_HTML)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

@app.route('/admin')
def admin_panel():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    today_history = get_today_history()
    bots = get_all_bots()
    return render_template_string(ADMIN_HTML, today_history=today_history, bots=bots)

@app.route('/admin/add_bot', methods=['POST'])
def admin_add_bot():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    add_bot_account(request.form['uid'], request.form['password'])
    return redirect(url_for('admin_panel'))

@app.route('/admin/del_bot/<int:bot_id>')
def admin_del_bot(bot_id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    delete_bot(bot_id)
    return redirect(url_for('admin_panel'))

if __name__ == '__main__':
    # স্টার্ট হওয়ার সময় ফোল্ডার ও ডাটাবেস চেক করে নিবে
    init_db()
    app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=False)