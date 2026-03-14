# ================================================================
#                  SECURITY & STATUS CONFIGURATION (NEW)
# ================================================================
import urllib.request
import urllib.error

GITHUB_STATUS_URL = "https://raw.githubusercontent.com/Ariyan20267/Ariyan_bot/refs/heads/main/Check_Aryan.txt"
WHATSAPP_LINK = "https://chat.whatsapp.com/LMO2lqCnie7HRFL8pIKzAH?mode=gi_t"
TELEGRAM_LINK = "Ariyan_ff_bot_devolpar"
PHONE_NUMBER  = "+01610369115"
STATUS_CHECK_INTERVAL = 300 # 5 Minutes
import os
import sys
import time
import json
import random
import asyncio
import signal
import threading
import socket
import ssl
import re
import base64
import binascii
import datetime
import re
import asyncio

# ========================= THIRD PARTY ==========================
import requests
import psutil
import jwt
import pickle
import urllib3
import pytz
import aiohttp

from flask import Flask, jsonify, request
from cfonts import render, say
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

# ========================= CRYPTO ===============================
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# ========================= PROTOBUF =============================
from protobuf_decoder.protobuf_decoder import Parser
from google.protobuf.timestamp_pb2 import Timestamp

from Pb2 import (
    DEcwHisPErMsG_pb2,
    MajoRLoGinrEs_pb2,
    PorTs_pb2,
    MajoRLoGinrEq_pb2,
    sQ_pb2,
    Team_msg_pb2
)

# ========================= LOCAL FILES ==========================
from xC4 import *
from xHeaders import *

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ================================================================
#                        WORD TO LEVEL MAP
# ================================================================

WORD_TO_LEVEL = {
    # 🔫 Weapons
    "ak": 1,
    "scar": 2,
    "mp40": 3,
    "mp40b": 4,
    "m10g": 5,
    "m10r": 6,
    "xm8": 7,
    "famas": 8,
    "ump": 9,
    "m18": 10,
    "fist": 11,
    "groza": 12,
    "m4a1": 13,
    "tn": 14,
    "g18": 15,
    "parafal": 16,
    "p90": 17,
    "m60": 18,
    "an94": 19,
    "wr": 20,

    # ❤️ Emotions / Emotes
    "rose": 42,
    "love": 43,
    "sad": 44,
    "rose2": 61,
    "lol2": 33,
    "lol": 99,
    "sad2": 166,
    "rose3": 65,
    "love1": 46
}


# ================================================================
#                        GLOBAL VARIABLES
# ================================================================

# ---------- Connection ----------
online_writer = None
whisper_writer = None
insquad = None
joining_team = False
senthi = False
error_shown = False

# ---------- Spam / Room ----------
spam_room = False
spammer_uid = None
spam_chat_id = None
spam_uid = None

# ---------- Spy / Chat ----------
Spy = False
Chat_Leave = False

# ---------- Fast Spam ----------
fast_spam_running = False
fast_spam_task = None
v_dance_task = None

custom_spam_running = False
custom_spam_task = None

spam_request_running = False
spam_request_task = None

# ---------- Evo Spam ----------
evo_fast_spam_running = False
evo_fast_spam_task = None

evo_custom_spam_running = False
evo_custom_spam_task = None

evo_cycle_running = False
evo_cycle_task = None

# ---------- Reject / Lag ----------
reject_spam_running = False
reject_spam_task = None

lag_running = False
lag_task = None

# ---------- Freeze ----------
freeze_running = False
freeze_task = None
FREEZE_EMOTES = [909052008, 909052008, 909052008]
FREEZE_DURATION = 120  # seconds
BLOCKED_NAMES = ["ARIYAN"]
# ================================================================
#                    EVOLUTION EMOTE IDS
# ================================================================

evo_emotes = {
    "1": "909000063",   # AK
    "2": "909000068",   # SCAR
    "3": "909000075",   # 1st MP40
    "4": "909040010",   # 2nd MP40
    "5": "909000081",   # 1st M1014
    "6": "909039011",   # 2nd M1014
    "7": "909000085",   # XM8
    "8": "909000090",   # Famas
    "9": "909000098",   # UMP
    "10": "909035007",  # M1887
    "11": "909042008",  # Woodpecker
    "12": "909041005",  # Groza
    "13": "909033001",  # M4A1
    "14": "909038010",  # Thompson
    "15": "909038012",  # G18
    "16": "909045001",  # Parafal
    "17": "909049010",  # P90
    "18": "909051003"   # M60
}


# ================================================================
#                           END SECTION
# ================================================================

# ================================================================
#                         ADMIN FUNCTIONS
# ================================================================

def is_admin(uid):
    """Check if given UID is admin"""
    return str(uid) == ADMIN_UID


# ================================================================
#                         BOT STATUS / MUTE
# ================================================================

def is_off():
    """Check if bot is disabled"""
    return not bot_enabled


def ff_num(val):
    """Format Free Fire number safely"""
    return xMsGFixinG(str(val)) if val not in (None, "") else "N/A"


def human_time(ts):
    """Convert timestamp to readable format"""
    try:
        ts = int(ts)
        return datetime.fromtimestamp(ts).strftime("%d %b %Y, %I:%M %p")
    except Exception:
        return "N/A"


# ================================================================
#                  LOAD EMOTES FROM JSON (SINGLE SOURCE)
# ================================================================

def load_emotes_from_json():
    """
    Load emotes from emotes.json
    Returns dict: {Number: Id}
    """
    try:
        with open("emotes.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        emote_map = {}
        for item in data:
            num = item.get("Number")
            eid = item.get("Id")

            if num is not None and eid is not None:
                emote_map[str(num)] = int(eid)

        print(f"✅ Loaded {len(emote_map)} emotes from emotes.json")
        return emote_map

    except FileNotFoundError:
        print("❌ emotes.json not found!")
        return {}

    except Exception as e:
        print("❌ emotes.json load error:", e)
        return {}


# Global emote maps (kept both names as in your original code)
GENERAL_EMOTES_MAP = load_emotes_from_json()
EMOTE_MAP = GENERAL_EMOTES_MAP


# ================================================================
#                     NEW VARIABLES
# ================================================================

bot_enabled = True
Uid = None
Pw = None



# ================================================================
#                  BOT AUTO EMOTE SYSTEM (STABLE)
# ================================================================

DEFAULT_BOT_UID = 14716877021
ADMIN_BOT_UID = 14716877021

BOT_STATE = {
    "running": False,
    "task": None,
    "uid": DEFAULT_BOT_UID
}


# ------------------------------------------------
# Send Single Emote To Target (Join → Emote → Leave)
# ------------------------------------------------
async def emote_to_user_once(team_code, emote_number, target_uid, key, iv, region):

    emote_id = GENERAL_EMOTES_MAP.get(str(emote_number))
    if not emote_id:
        print("❌ Emote not found in emotes.json")
        return

    try:
        # Join squad
        join_packet = await GenJoinSquadsPacket(team_code, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)

        await asyncio.sleep(0.1)

        # Send emote
        emote_packet = await Emote_k(
            int(target_uid),
            int(emote_id),
            key,
            iv,
            region
        )

        await SEndPacKeT(
            whisper_writer,
            online_writer,
            'OnLine',
            emote_packet
        )

        await asyncio.sleep(0.1)

        # Leave squad
        leave_packet = await ExiT(None, key, iv)
        await SEndPacKeT(
            whisper_writer,
            online_writer,
            'OnLine',
            leave_packet
        )

        print(f"✅ Emote {emote_number} sent to UID {target_uid}")

    except Exception as e:
        print("❌ EMOTE ERROR:", e)


# ------------------------------------------------
# Continuous Bot Emote Loop
# ------------------------------------------------
async def bot_emote_loop(key, iv, region, delay=6):

    emote_ids = list(GENERAL_EMOTES_MAP.values())

    if not emote_ids:
        print("❌ No emotes loaded. Loop stopped.")
        return

    print(f"🤖 BOT LOOP STARTED for UID {BOT_STATE['uid']}")

    while BOT_STATE["running"]:

        try:
            emote_id = random.choice(emote_ids)

            packet = await Emote_k(
                int(BOT_STATE["uid"]),
                int(emote_id),
                key,
                iv,
                region
            )

            await SEndPacKeT(
                whisper_writer,
                online_writer,
                'OnLine',
                packet
            )

        except Exception as e:
            print("❌ BOT EMOTE ERROR:", e)

        # Delay handling with safe stop check
        for _ in range(delay):
            if not BOT_STATE["running"]:
                break
            await asyncio.sleep(1)

    print("🛑 BOT LOOP STOPPED")


# ================================================================
#                          END SECTION
# ================================================================

# Badge values for s1 to s5 commands - using your exact values
BADGE_VALUES = {
    "s1": 1048576,    # Your first badge
    "s2": 32768,      # Your second badge  
    "s3": 2048,       # Your third badge
    "s4": 262144     # Your seventh badge
}


# Helper functions for ghost join
def dec_to_hex(decimal):
    """Convert decimal to hex string"""
    hex_str = hex(decimal)[2:]
    return hex_str.upper() if len(hex_str) % 2 == 0 else '0' + hex_str.upper()


async def encrypt_packet(packet_hex, key, iv):
    """Encrypt packet using AES CBC"""
    cipher = AES.new(key, AES.MODE_CBC, iv)
    packet_bytes = bytes.fromhex(packet_hex)
    padded_packet = pad(packet_bytes, AES.block_size)
    encrypted = cipher.encrypt(padded_packet)
    return encrypted.hex()

async def nmnmmmmn(packet_hex, key, iv):
    """Wrapper for encrypt_packet"""
    return await encrypt_packet(packet_hex, key, iv)
    



def get_idroom_by_idplayer(packet_hex):
    """Extract room ID from packet - converted from your other TCP"""
    try:
        json_result = get_available_room(packet_hex)
        parsed_data = json.loads(json_result)
        json_data = parsed_data["5"]["data"]
        data = json_data["1"]["data"]
        idroom = data['15']["data"]
        return idroom
    except Exception as e:
        print(f"Error extracting room ID: {e}")
        return None

async def check_player_in_room(target_uid, key, iv):
    """Check if player is in a room by sending status request"""
    try:
        # Send status request packet
        status_packet = await GeT_Status(int(target_uid), key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', status_packet)
        
        # You'll need to capture the response packet and parse it
        # For now, return True and we'll handle room detection in the main loop
        return True
    except Exception as e:
        print(f"Error checking player room status: {e}")
        return False
        
        
# ===============================
# LOAD EMOTES
# ===============================

def load_emotes(filename="emotes.json"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

            # Ensure it's a list
            if isinstance(data, list):
                return data
            else:
                print("Emote file is not list format!")
                return []

    except Exception as e:
        print(f"Emote Load Error: {e}")
        return []


# ===============================
# CREATE PAGES (LIST SAFE)
# ===============================

def make_pages(emote_list, per_page=20):
    pages = []
    message = ""
    count = 0

    for emote in emote_list:
        try:
            name = emote.get("name", "unknown")
            emote_id = emote.get("id", "0")

            message += f"[FFFFFF]{name} → {emote_id}\n"
            count += 1

            if count >= per_page:
                pages.append(message)
                message = ""
                count = 0

        except:
            continue

    if message:
        pages.append(message)

    return pages


# ===============================
# SEND ELIST
# ===============================

async def send_elist(chat_type, uid, chat_id, key, iv, whisper_writer, online_writer):

    emote_list = load_emotes()
    if not emote_list:
        print("No emotes found.")
        return

    pages = make_pages(emote_list)

    for page in pages:
        try:
            P = await SEndMsG(chat_type, page, uid, chat_id, key, iv)
            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)

            await asyncio.sleep(1)

        except Exception as e:
            print(f"Elist Send Error: {e}")
            break        
    
    
def ghost_pakcet(player_id , secret_code , key ,iv):
    fields = {
        1: 61,
        2: {
            1: int(player_id),  
            2: {
                1: int(player_id),  
                2: 1159,  
                3: f"ARIYAN",  
                5: 12,  
                6: 15,
                7: 1,
                8: {
                    2: 1,
                    3: 1,
                },
                9: 3,
            },
            3: secret_code,},}
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()), '0515', key, iv)
            
async def SEnd_InV_with_Cosmetics(Nu, Uid, K, V, region):
    """Simple version - just add field 5 with basic cosmetics"""
    region = "ind"
    fields = {
        1: 2, 
        2: {
            1: int(Uid), 
            2: region, 
            4: int(Nu),
            # Simply add field 5 with basic cosmetics
            5: {
                1: "BOT",                    # Name
                2: int(await get_random_avatar()),     # Avatar
                5: random.choice([1048576, 32768, 2048]),  # Random badge
            }
        }
    }

    if region.lower() == "ind":
        packet = '0514'
    elif region.lower() == "bd":
        packet = "0519"
    else:
        packet = "0515"
        
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet, K, V)   

async def KickTarget(target_uid, key, iv):
    fields = {1: 35, 2: {1: int(target_uid)}}
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '0515' , key, iv)

async def freeze_emote_spam(uid, key, iv, region, chat_type, chat_id, sender_uid):
    """Send 3 freeze emotes in 1-second cycles for 10 seconds"""
    global freeze_running
    
    try:
        cycles = 0
        max_cycles = FREEZE_DURATION  # 10 seconds
        
        while freeze_running and cycles < max_cycles:
            # Send all 3 emotes in sequence
            for i, emote_id in enumerate(FREEZE_EMOTES):
                if not freeze_running:
                    break
                    
                try:
                    # Send emote
                    emote_packet = await Emote_k(int(uid), emote_id, key, iv, region)
                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', emote_packet)
                    
                    print(f"❄️ Freeze emote {i+1}/{len(FREEZE_EMOTES)} sent: {emote_id}")
                    
                    # Small delay between emotes (0.3 seconds)
                    await asyncio.sleep(0.3)
                    
                except Exception as e:
                    print(f"❌ Error sending freeze emote {i+1}: {e}")
            
            cycles += 1
            print(f"🌀 Freeze cycle {cycles}/{max_cycles} completed")
            
            # Wait for next cycle (total 1 second per cycle)
            remaining_time = 1.0 - (0.3 * len(FREEZE_EMOTES))
            if remaining_time > 0:
                await asyncio.sleep(remaining_time)
        
        print(f"✅ Freeze sequence completed: {cycles} cycles")
        return cycles
        
    except Exception as e:
        print(f"❌ Freeze function error: {e}")
        return 0
        
async def handle_freeze_completion(freeze_task, uid, sender_uid, chat_id, chat_type, key, iv):
    """Handle freeze command completion"""
    try:
        cycles_completed = await freeze_task
        
        completion_msg = f"""[B][C][00FFFF]❄️ FREEZE COMMAND COMPLETED!

🎯 Target: {uid}
⏱️ Duration: {cycles_completed} seconds
🎭 Emotes sent: {cycles_completed * 3}
❄️ Sequence: 
  • 909052008 (Ice)
  • 909052008 (Frozen)
  • 909052008 (Freeze)

✅ Status: Complete!
"""
        await safe_send_message(chat_type, completion_msg, sender_uid, chat_id, key, iv)
        
    except asyncio.CancelledError:
        print("🛑 Freeze command cancelled")
    except Exception as e:
        error_msg = f"[B][C][FF0000]❌ Freeze error: {str(e)}\n"
        await safe_send_message(chat_type, error_msg, sender_uid, chat_id, key, iv)
            
async def join_custom_room(room_id, room_password, key, iv, region):
    """Join custom room with proper Free Fire packet structure"""
    fields = {
        1: 61,  # Room join packet type (verified for Free Fire)
        2: {
            1: int(room_id),
            2: {
                1: int(room_id),  # Room ID
                2: int(time.time()),  # Timestamp
                3: "BOT",  # Player name
                5: 12,  # Unknown
                6: 9999999,  # Unknown
                7: 1,  # Unknown
                8: {
                    2: 1,
                    3: 1,
                },
                9: 3,  # Room type
            },
            3: str(room_password),  # Room password
        }
    }
    
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
        
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet_type, key, iv)
    
async def leave_squad(key, iv, region):
    """Leave squad - converted from your old TCP leave_s()"""
    fields = {
        1: 7,
        2: {
            1: 12480598706  # Your exact value from old TCP
        }
    }
    
    packet = (await CrEaTe_ProTo(fields)).hex()
    
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
        
    return await GeneRaTePk(packet, packet_type, key, iv)    
    
async def request_join_with_badge(target_uid, badge_value, key, iv, region):
    """Send join request with specific badge - converted from your old TCP"""
    fields = {
        1: 33,
        2: {
            1: int(target_uid),
            2: region.upper(),
            3: 1,
            4: 1,
            5: bytes([1, 7, 9, 10, 11, 18, 25, 26, 32]),
            6: "iG:[C][B][FF0000] ARIYAN",
            7: 330,
            8: 1000,
            10: region.upper(),
            11: bytes([49, 97, 99, 52, 98, 56, 48, 101, 99, 102, 48, 52, 55, 56,
                       97, 52, 52, 50, 48, 51, 98, 102, 56, 102, 97, 99, 54, 49, 50, 48, 102, 53]),
            12: 1,
            13: int(target_uid),
            14: {
                1: 2203434355,
                2: 8,
                3: "\u0010\u0015\b\n\u000b\u0013\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"
            },
            16: 1,
            17: 1,
            18: 312,
            19: 46,
            23: bytes([16, 1, 24, 1]),
            24: int(await get_random_avatar()),
            26: "",
            28: "",
            31: {
                1: 1,
                2: badge_value  # Dynamic badge value
            },
            32: badge_value,    # Dynamic badge value
            34: {
                1: int(target_uid),
                2: 8,
                3: bytes([15,6,21,8,10,11,19,12,17,4,14,20,7,2,1,5,16,3,13,18])
            }
        },
        10: "en",
        13: {
            2: 1,
            3: 1
        }
    }
    
    packet = (await CrEaTe_ProTo(fields)).hex()
    
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
        
    return await GeneRaTePk(packet, packet_type, key, iv)    
    
async def reset_bot_state(key, iv, region):
    """Reset bot to solo mode before spam - Critical step from your old TCP"""
    try:
        # Leave any current squad (using your exact leave_s function)
        leave_packet = await leave_squad(key, iv, region)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave_packet)
        await asyncio.sleep(0.5)
        
        print("✅ Bot state reset - left squad")
        return True
        
    except Exception as e:
        print(f"❌ Error resetting bot: {e}")
        return False    
    
async def create_custom_room(room_name, room_password, max_players, key, iv, region):
    """Create a custom room"""
    fields = {
        1: 3,  # Create room packet type
        2: {
            1: room_name,
            2: room_password,
            3: max_players,  # 2, 4, 8, 16, etc.
            4: 1,  # Room mode
            5: 1,  # Map
            6: "en",  # Language
            7: {   # Player info
                1: "BotHost",
                2: int(await get_random_avatar()),
                3: 330,
                4: 1048576,
                5: "BOTCLAN"
            }
        }
    }
    
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
        
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet_type, key, iv)              
            


async def handle_badge_command(cmd, inPuTMsG, uid, chat_id, key, iv, region, chat_type):
    """Handle individual badge commands"""
    parts = inPuTMsG.strip().split()
    if len(parts) < 2:
        error_msg = f"[B][C][FF0000]❌ Usage: /{cmd} (uid)\nExample: /{cmd} 123456789\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
        return
    
    target_uid = parts[1]
    badge_value = BADGE_VALUES.get(cmd, 1048576)
    
    if not target_uid.isdigit():
        error_msg = f"[B][C][FF0000]❌ Please write a valid player ID!\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
        return
    
    # Send initial message
    initial_msg = f"[B][C][1E90FF]🌀 Request received! Preparing to spam {target_uid}...\n"
    await safe_send_message(chat_type, initial_msg, uid, chat_id, key, iv)
    
    try:
        # Reset bot state
        await reset_bot_state(key, iv, region)
        
        # Create and send join packets
        join_packet = await request_join_with_badge(target_uid, badge_value, key, iv, region)
        spam_count = 10
        
        for i in range(spam_count):
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
            print(f"✅ Sent /{cmd} request #{i+1} with badge {badge_value}")
            await asyncio.sleep(0.1)
        
        success_msg = f"[B][C][00FF00]✅ Successfully Sent {spam_count} Join Requests!\n🎯 Target: {target_uid}\n🏷️ Badge: {badge_value}\n"
        await safe_send_message(chat_type, success_msg, uid, chat_id, key, iv)
        
        # Cleanup
        await asyncio.sleep(1)
        await reset_bot_state(key, iv, region)
        
    except Exception as e:
        error_msg = f"[B][C][FF0000]❌ Error in /{cmd}: {str(e)}\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)

async def create_authenticated_join(target_uid, account_uid, key, iv, region):
    """Create join request that appears to come from the specific account"""
    try:
        # Use the standard invite function but ensure it uses account context
        join_packet = await SEnd_InV(5, int(target_uid), key, iv, region)
        return join_packet
    except Exception as e:
        print(f"❌ Error creating join packet: {e}")
        return None        
    

    
    
async def auto_rings_emote_dual(sender_uid, key, iv, region):
    """Send RANDOM emote to both sender and bot (dual emote effect)"""
    try:
        emote_ids = [
            909000062,  # Rings
            909000010,
            909049012
        ]

        random_emote_id = random.choice(emote_ids)
        bot_uid = 13793280064

        # Send emote to USER
        emote_to_sender = await Emote_k(
            int(sender_uid),
            int(random_emote_id),
            key, iv, region
        )
        await SEndPacKeT(
            whisper_writer,
            online_writer,
            'OnLine',
            emote_to_sender
        )

        await asyncio.sleep(0.5)

        # Send emote to BOT
        emote_to_bot = await Emote_k(
            int(bot_uid),
            int(random_emote_id),
            key, iv, region
        )
        await SEndPacKeT(
            whisper_writer,
            online_writer,
            'OnLine',
            emote_to_bot
        )

        print(f"🔥 Dual RANDOM emote sent | Emote ID: {random_emote_id}")

    except Exception as e:
        print(f"❌ Dual random emote error: {e}")
        
        # Small delay between emotes
        await asyncio.sleep(0.5)
        
        # Send emote to BOT (bot performs emote on itself)
        emote_to_bot = await Emote_k(int(bot_uid), rings_emote_id, key, iv, region)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', emote_to_bot)
        
        print(f"🤖 Bot performed dual Rings emote with sender {sender_uid} and bot {bot_uid}!")
        
    except Exception as e:
        print(f"Error sending dual rings emote: {e}")    
        

async def magic_bundle_sequence(team_code, chat_type, chat_id, uid, key, iv, region):
    try:
        for i in range(1, 12):

            # 🔴 Leave squad
            leave_packet = await ExiT(None, key, iv)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave_packet)
            await asyncio.sleep(1.2)

            # 🟢 Join squad (IMPORTANT FIX)
            join_packet = await GenJoinSquadsPacket(team_code, key, iv)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
            await asyncio.sleep(0.25)

            # 📦 Silent random bundle change (NO visible /b message)
            try:
                bundle_packet = await bundle_packet_async(i, key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', bundle_packet)
                print(f"✅ Silent bundle changed: {i}")
            except Exception as e:
                print("Bundle change error:", e)

            await asyncio.sleep(2)

        # 🟢 FINAL JOIN (stay in team, no leave)
        final_join = await GenJoinSquadsPacket(team_code, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', final_join)

        await safe_send_message(
            chat_type,
            "[B][C][00FF00]✨ Magic completed! Bot is now staying in team.",
            uid,
            chat_id,
            key,
            iv
        )

    except Exception as e:
        print("❌ Magic bundle error:", e)
        
async def Room_Spam(Uid, Rm, Nm, K, V):
   
    same_value = random.choice([32768])  #you can add any badge value 
    
    fields = {
        1: 78,
        2: {
            1: int(Rm),  
            2: "iG:[C][B][FF0000] ARIYAN",  
            3: {
                2: 1,
                3: 1
            },
            4: 330,      
            5: 6000,     
            6: 201,      
            10: int(await get_random_avatar()),  
            11: int(Uid), # Target UID
            12: 1,       
            15: {
                1: 1,
                2: same_value  
            },
            16: same_value,    
            18: {
                1: 11481904755,  
                2: 8,
                3: "\u0010\u0015\b\n\u000b\u0013\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"
            },
            
            31: {
                1: 1,
                2: same_value  
            },
            32: same_value,    
            34: {
                1: int(Uid),   
                2: 8,
                3: bytes([15,6,21,8,10,11,19,12,17,4,14,20,7,2,1,5,16,3,13,18])
            }
        }
    }
    
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '0e15', K, V)
    
async def evo_cycle_spam(uids, key, iv, region):
    """Cycle through all evolution emotes one by one with 5-second delay"""
    global evo_cycle_running
    
    cycle_count = 0
    while evo_cycle_running:
        cycle_count += 1
        print(f"Starting evolution emote cycle #{cycle_count}")
        
        for emote_number, emote_id in evo_emotes.items():
            if not evo_cycle_running:
                break
                
            print(f"Sending evolution emote {emote_number} (ID: {emote_id})")
            
            for uid in uids:
                try:
                    uid_int = int(uid)
                    H = await Emote_k(uid_int, int(emote_id), key, iv, region)
                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                    print(f"Sent emote {emote_number} to UID: {uid}")
                except Exception as e:
                    print(f"Error sending evo emote {emote_number} to {uid}: {e}")
            
            # Wait 5 seconds before moving to next emote (as requested)
            if evo_cycle_running:
                print(f"Waiting 5 seconds before next emote...")
                for i in range(5):
                    if not evo_cycle_running:
                        break
                    await asyncio.sleep(1)
        
        # Small delay before restarting the cycle
        if evo_cycle_running:
            print("Completed one full cycle of all evolution emotes. Restarting...")
            await asyncio.sleep(2)
    
    print("Evolution emote cycle stopped")
    
async def reject_spam_loop(target_uid, key, iv):
    """Send reject spam packets to target in background"""
    global reject_spam_running
    
    count = 0
    max_spam = 150
    
    while reject_spam_running and count < max_spam:
        try:
            # Send both packets
            packet1 = await banecipher1(target_uid, key, iv)
            packet2 = await banecipher(target_uid, key, iv)
            
            # Send to Online connection
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', packet1)
            await asyncio.sleep(0.1)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', packet2)
            
            count += 1
            print(f"Sent reject spam #{count} to {target_uid}")
            
            # 0.2 second delay between spam cycles
            await asyncio.sleep(0.2)
            
        except Exception as e:
            print(f"Error in reject spam: {e}")
            break
    
    return count    
    
async def handle_reject_completion(spam_task, target_uid, sender_uid, chat_id, chat_type, key, iv):
    """Handle completion of reject spam and send final message"""
    try:
        spam_count = await spam_task
        
        # Send completion message
        if spam_count >= 150:
            completion_msg = f"[B][C][00FF00]✅ Reject Spam Completed Successfully for ID {target_uid}\n✅ Total packets sent: {spam_count * 2}\n"
        else:
            completion_msg = f"[B][C][FFFF00]⚠️ Reject Spam Partially Completed for ID {target_uid}\n⚠️ Total packets sent: {spam_count * 2}\n"
        
        await safe_send_message(chat_type, completion_msg, sender_uid, chat_id, key, iv)
        
    except asyncio.CancelledError:
        print("Reject spam was cancelled")
    except Exception as e:
        error_msg = f"[B][C][FF0000]❌ ERROR in reject spam: {str(e)}\n"
        await safe_send_message(chat_type, error_msg, sender_uid, chat_id, key, iv)    
    
async def banecipher(client_id, key, iv):
    """Create reject spam packet 1 - Converted to new async format"""
    banner_text = f"""
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][0000FF]======================================================================================================================================================================================================================================================
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███




"""        
    fields = {
        1: 5,
        2: {
            1: int(client_id),
            2: 1,
            3: int(client_id),
            4: banner_text
        }
    }
    
    # Use CrEaTe_ProTo from xC4.py (async)
    packet = await CrEaTe_ProTo(fields)
    packet_hex = packet.hex()
    
    # Use EnC_PacKeT from xC4.py (async)
    encrypted_packet = await EnC_PacKeT(packet_hex, key, iv)
    
    # Calculate header length
    header_length = len(encrypted_packet) // 2
    header_length_final = await DecodE_HeX(header_length)
    
    # Build final packet based on header length
    if len(header_length_final) == 2:
        final_packet = "0515000000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 3:
        final_packet = "051500000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 4:
        final_packet = "05150000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 5:
        final_packet = "0515000" + header_length_final + encrypted_packet
    else:
        final_packet = "0515000000" + header_length_final + encrypted_packet

    return bytes.fromhex(final_packet)

async def banecipher1(client_id, key, iv):
    """Create reject spam packet 2 - Converted to new async format"""
    gay_text = f"""
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][0000FF]======================================================================================================================================================================================================================================================
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███




"""        
    fields = {
        1: int(client_id),
        2: 5,
        4: 50,
        5: {
            1: int(client_id),
            2: gay_text,
        }
    }
    
    # Use CrEaTe_ProTo from xC4.py (async)
    packet = await CrEaTe_ProTo(fields)
    packet_hex = packet.hex()
    
    # Use EnC_PacKeT from xC4.py (async)
    encrypted_packet = await EnC_PacKeT(packet_hex, key, iv)
    
    # Calculate header length
    header_length = len(encrypted_packet) // 2
    header_length_final = await DecodE_HeX(header_length)
    
    # Build final packet based on header length
    if len(header_length_final) == 2:
        final_packet = "0515000000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 3:
        final_packet = "051500000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 4:
        final_packet = "05150000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 5:
        final_packet = "0515000" + header_length_final + encrypted_packet
    else:
        final_packet = "0515000000" + header_length_final + encrypted_packet

    return bytes.fromhex(final_packet)
    

async def lag_team_loop(team_code, key, iv, region):
    """Rapid join/leave loop to create lag"""
    global lag_running
    count = 0
    
    while lag_running:
        try:
            # Join the team
            join_packet = await GenJoinSquadsPacket(team_code, key, iv)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
            
            # Very short delay before leaving
            await asyncio.sleep(0.01)  # 10 milliseconds
            
            # Leave the team
            leave_packet = await ExiT(None, key, iv)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave_packet)
            
            count += 1
            print(f"Lag cycle #{count} completed for team: {team_code}")
            
            # Short delay before next cycle
            await asyncio.sleep(0.01)  # 10 milliseconds between cycles
            
        except Exception as e:
            print(f"Error in lag loop: {e}")
            # Continue the loop even if there's an error
            await asyncio.sleep(0.1)

async def general_emote_spam(uids, emote_number, key, iv, region):
    """Send general emotes based on number mapping from JSON file"""
    try:
        emote_id = GENERAL_EMOTES_MAP.get(str(emote_number))
        if not emote_id:
            return False, f"Invalid emote number! Use numbers from 1-{len(GENERAL_EMOTES_MAP)}"
        
        success_count = 0
        for uid in uids:
            try:
                uid_int = int(uid)
                H = await Emote_k(uid_int, emote_id, key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                success_count += 1
                await asyncio.sleep(0.1)
            except Exception as e:
                print(f"Error sending general emote to {uid}: {e}")
        
        return True, f"Sent emote {emote_number} (ID: {emote_id}) to {success_count} player(s)"
    
    except Exception as e:
        return False, f"Error in general_emote_spam: {str(e)}"
 
####################################
#SPAM REQUESTS
def spam_requests(player_id):
    # This URL now correctly points to the Flask app you provided
    url = f"https://like2.vercel.app/send_requests?uid={player_id}&server={server2}&key={key2}"
    try:
        res = requests.get(url, timeout=20) # Added a timeout
        if res.status_code == 200:
            data = res.json()
            # Return a more descriptive message based on the API's JSON response
            return f"API Status: Success [{data.get('success_count', 0)}] Failed [{data.get('failed_count', 0)}]"
        else:
            # Return the error status from the API
            return f"API Error: Status {res.status_code}"
    except requests.exceptions.RequestException as e:
        # Handle cases where the API isn't running or is unreachable
        print(f"Could not connect to spam API: {e}")
        return "Failed to connect to spam API."
####################################

async def animation_packet(animation_id, key, iv):

    fields = {
        1: 88,
        2: {
            1: {
                1: int(animation_id)
            }
        }
    }

    proto_bytes = await CrEaTe_ProTo(fields)
    packet_hex = proto_bytes.hex()

    encrypted_packet = await encrypt_packet(packet_hex, key, iv)

    packet_length = len(encrypted_packet) // 2

    # 🔥 built-in hex conversion
    hex_length = format(packet_length, 'x')

    final_packet = "051500" + "0" * (6 - len(hex_length)) + hex_length + encrypted_packet

    return bytes.fromhex(final_packet)

async def bundle_packet_async(bundle_id, key, iv, region="bd"):
    """Create bundle packet"""
    fields = {
        1: 88,
        2: {
            1: {
                1: bundle_id,
                2: 1
            },
            2: 2
        }
    }
    
    # Use your CrEaTe_ProTo function
    packet = await CrEaTe_ProTo(fields)
    packet_hex = packet.hex()
    
    # Use your encrypt_packet function
    encrypted = await encrypt_packet(packet_hex, key, iv)
    
    # Use your DecodE_HeX function
    header_length = len(encrypted) // 2
    header_length_hex = await DecodE_HeX(header_length)
    
    # Build final packet based on region
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
    
    # Determine header based on length
    if len(header_length_hex) == 2:
        final_header = f"{packet_type}000000"
    elif len(header_length_hex) == 3:
        final_header = f"{packet_type}00000"
    elif len(header_length_hex) == 4:
        final_header = f"{packet_type}0000"
    elif len(header_length_hex) == 5:
        final_header = f"{packet_type}000"
    else:
        final_header = f"{packet_type}000000"
    
    final_packet_hex = final_header + header_length_hex + encrypted
    return bytes.fromhex(final_packet_hex)
        
    async def run_spam(chat_type, message, count, uid, chat_id, key, iv):
        try:
            for i in range(count):
                await safe_send_message(chat_type, message, uid, chat_id, key, iv)
                await asyncio.sleep(0.12)
        except Exception as e:
            print("Spam Error:", e)
        
async def send_title_msg(self, chat_id, key, iv):
        """Build title packet using dictionary structure like GenResponsMsg"""
    
        fields = {
            1: 1,  # type
            2: {   # data
                1: "13777777720",  # uid
                2: str(chat_id),   # chat_id  
                3: f"{{\"TitleID\":{get_random_title()},\"type\":\"Title\"}}",  # title
                4: int(datetime.now().timestamp()),  # timestamp
                5: 0,   # chat_type
                6: "en", # language
                9: {    # field9 - player details
                    1: "[C][B][FF0000] KRN ON TOP",  # Nickname
                    2: await get_random_avatar(),          # avatar_id
                    3: 330,                          # rank
                    4: 102000015,                    # badge
                    5: "TEMP GUILD",                 # Clan_Name
                    6: 1,                            # field10
                    7: 1,                            # global_rank_pos
                    8: {                             # badge_info
                        1: 2                         # value
                    },
                    9: {                             # prime_info
                        1: 1158053040,               # prime_uid
                        2: 8,                        # prime_level
                        3: "\u0010\u0015\b\n\u000b\u0015\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"  # prime_hex
                    }
                },
                13: {   # field13 - url options
                    1: 2,   # url_type
                    2: 1    # curl_platform
                },
                99: b""  # empty_field
            }
        }

        # **EXACTLY like GenResponsMsg:**
        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_length = len(encrypt_packet(packet, key, iv)) // 2
        header_length_final = dec_to_hex(header_length)
    
        # **KEY: Use 0515 for title packets instead of 1215**
        if len(header_length_final) == 2:
            final_packet = "0515000000" + header_length_final + self.nmnmmmmn(packet)
        elif len(header_length_final) == 3:
            final_packet = "051500000" + header_length_final + self.nmnmmmmn(packet)
        elif len(header_length_final) == 4:
            final_packet = "05150000" + header_length_final + self.nmnmmmmn(packet)
        elif len(header_length_final) == 5:
            final_packet = "0515000" + header_length_final + self.nmnmmmmn(packet)
    
        return bytes.fromhex(final_packet)
        
        
def get_player_info(uid):
    try:
        url = f"https://info-api-mg24-pro.vercel.app/get?uid={uid}"
        res = requests.get(url, timeout=10)

        if res.status_code != 200:
            return None, f"API Error: {res.status_code}"

        data = res.json()

        # basic validation
        if "AccountInfo" not in data:
            return None, "Invalid API response"

        return data

    except requests.exceptions.Timeout:
        return None, "Request timeout"

    except Exception as e:
        return None, str(e)

# ADD FRIEND 
def add_friend(uid, pw, target_uid):
    try:
        url = (
            "https://danger-friend-manager.vercel.app/adding_friend"
            f"?uid={Uid}&password={Pw}&friend_uid={target_uid}"
        )

        res = requests.get(url, timeout=10)
        if res.status_code != 200:
            return "[C][B][FF5C8A]API ERROR"

        data = res.json()

        success = data.get("success", False)
        name = data.get("nickname", "Unknown")
        region = data.get("region", "N/A")
        friend_uid = data.get("friend_uid", target_uid)

        if success:
            status_color = "4CFFB0"
            status_text = "FRIEND ADDED"
        else:
            status_color = "FF5C8A"
            status_text = "FAILED"

        return f"""
[C][B][5DA9FF]━━━━━━━━━━━━━
[C][B][FF6EC7]FRIEND MANAGER
[C][5DA9FF]━━━━━━━━━━━━━
[C][E6E6FA]Action   : [{status_color}]{status_text}
[C][E6E6FA]Bot Name     : [9AD0FF]{name}
[C][E6E6FA]Target Uid : [9AD0FF]{xMsGFixinG(friend_uid)}
[C][E6E6FA]Region   : [9AD0FF]{region}
[C][B][5DA9FF]━━━━━━━━━━━━━
"""

    except Exception as e:
        return f"[C][B][FF5C8A]ERROR: {e}"

def remove_friend(uid, pw, target_uid):
    try:
        url = (
            "https://danger-friend-manager.vercel.app/remove_friend"
            f"?uid={Uid}&password={Pw}&friend_uid={target_uid}"
        )

        res = requests.get(url, timeout=10)
        if res.status_code != 200:
            return "[C][B][FF5C8A]API ERROR"

        data = res.json()

        success = data.get("success", False)
        name = data.get("nickname", "Unknown")
        region = data.get("region", "N/A")
        friend_uid = data.get("friend_uid", target_uid)

        if success:
            status_color = "FF6EC7"
            status_text = "FRIEND REMOVED"
        else:
            status_color = "FF5C8A"
            status_text = "FAILED"

        return f"""
[C][B][5DA9FF]━━━━━━━━━━━━━
[C][B][FF6EC7]FRIEND MANAGER
[C][5DA9FF]━━━━━━━━━━━━━
[C][E6E6FA]Action   : [{status_color}]{status_text}
[C][E6E6FA]Bot Name     : [9AD0FF]{name}
[C][E6E6FA]Target Uid : [9AD0FF]{xMsGFixinG(friend_uid)}
[C][E6E6FA]Region   : [9AD0FF]{region}
[C][B][5DA9FF]━━━━━━━━━━━━━
"""

    except Exception as e:
        return f"[C][B][FF5C8A]ERROR: {e}"

# GET FRIEND LIST
def get_friends_list_game_style(uid, pw):
    try:
        url = f"https://danger-friend-manager.vercel.app/get_friends_list?uid={uid}&password={pw}"
        res = requests.get(url, timeout=10)
        if res.status_code != 200:
            return "[C][B][FF5C8A]API ERROR"

        data = res.json()
        print("API RESPONSE:", data)  # Debug

        friends = data.get("friends", [])
        success = data.get("success", False)

        if not success or not friends:
            return (
                "[C][B][5DA9FF]━━━━━━━━━━━━━\n"
                "[C][B][FF6EC7]FRIEND MANAGER\n"
                "[C][5DA9FF]━━━━━━━━━━━━━\n"
                "[C][E6E6FA]No friends found\n"
                "[C][B][5DA9FF]━━━━━━━━━━━━━"
            )

        friend_text = ""
        for i, friend in enumerate(friends, 1):
            nickname = friend.get("nickname", "Unknown")
            friend_uid = friend.get("uid", "N/A")

            # Game-style UID formatting (digit separators)
            str_uid_game = "🗿".join(list(str(friend_uid)))

            friend_text += (
                f"[C][E6E6FA]{i}. [9AD0FF]{nickname} [E6E6FA]| UID: [9AD0FF]{str_uid_game}\n"
            )

        return (
            "[C][B][5DA9FF]━━━━━━━━━━━━━\n"
            "[C][B][FF6EC7]FRIEND MANAGER\n"
            "[C][5DA9FF]━━━━━━━━━━━━━\n"
            f"{friend_text}"
            "[C][B][5DA9FF]━━━━━━━━━━━━━"
        )

    except Exception as e:
        return f"[C][B][FF5C8A]ERROR: {e}"

#GET PLAYER BIO 
def get_player_bio(uid):
    try:
        url = f"https://info-api-mg24-pro.vercel.app.vercel.app/get?uid={uid}"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            # Bio is inside socialInfo -> signature
            bio = data.get('socialinfo', {}).get('signature', 'No Bio Found')
            if bio:
                return bio
            else:
                return "No bio available"
        else:
            return f"Failed to fetch bio. Status code: {res.status_code}"
    except Exception as e:
        return f"Error occurred: {e}"

def check_ban(uid):
    try:
        url = f"https://mg24-ban-check.vercel.app/ban?uid={uid}"
        res = requests.get(url, timeout=10)

        if res.status_code != 200:
            return "[B][C][FF0000]❌ API ERROR"

        data = res.json()

        name = data.get("nickname", "Unknown")
        account_id = data.get("account_id", uid)
        region = data.get("region", "N/A")
        status = data.get("ban_status", "Unknown")
        period = data.get("ban_period") or "No Ban"

        status_lower = status.lower()

        # ✅ SIMPLE + SAFE RULE
        if "not" in status_lower:
            status_color = "66FF00"
            period_color = "66FF00"
        else:
            status_color = "FF4444"
            period_color = "FF4444"

        return f"""
[C][B][5DA9FF]━━━━━━━━━━━━━
[C][B][FF6EC7]BAN STATUS CHECK
[C][5DA9FF]━━━━━━━━━━━━━
[C][E6E6FA]Name    : [9AD0FF]{name}
[C][E6E6FA]UID     : [9AD0FF]{xMsGFixinG(account_id)}
[C][E6E6FA]Region  : [9AD0FF]{region}
[C][E6E6FA]Status  : [{status_color}]{status}
[C][E6E6FA]Period  : [{period_color}]{period}
[C][B][5DA9FF]━━━━━━━━━━━━━
"""

    except Exception as e:
        return f"[B][C][FF0000]❌ Error: {e}"

async def send_full_player_info(data, chat_type, uid, chat_id, key, iv):

    acc = data.get("AccountInfo", {})
    guild = data.get("GuildInfo", {})
    social = data.get("socialinfo", {})
    captain = data.get("captainBasicInfo", {})

    # ────────── MESSAGE 1 : COMMON ACCOUNT INFO ──────────
    msg1 = f"""
[C][B][FFAA00]━━━━━━━━━━━━━
[C][B][FFFFFF]COMMON ACCOUNT INFO
[C][FFAA00]━━━━━━━━━━━━━
[C][FFFFFF]Name      : [66FF00]{acc.get('AccountName', 'N/A')}
[C][FFFFFF]UID       : [66FF00]{ff_num(captain.get('accountId'))}
[C][FFFFFF]Level     : [66FF00]{acc.get('AccountLevel', 'N/A')}
[C][FFFFFF]EXP       : [66FF00]{ff_num(acc.get('AccountEXP'))}
[C][FFFFFF]Likes     : [66FF00]{ff_num(acc.get('AccountLikes'))}
[C][FFFFFF]Region    : [66FF00]{acc.get('AccountRegion', 'N/A')}
[C][FFFFFF]BP Badge  : [66FF00]{ff_num(acc.get('AccountBPID'))}
[C][FFFFFF]Version   : [66FF00]{acc.get('ReleaseVersion', 'N/A')}
"""

    await safe_send_message(chat_type, msg1, uid, chat_id, key, iv)
    await asyncio.sleep(0.5)

    # ────────── MESSAGE 2 : DATE + RANK INFO ──────────
    lang = social.get("language", "N/A")
    if "_" in lang:
        lang = lang.split("_")[-1]   # ARABIC, ENGLISH
    msg2 = f"""
[C][B][FFAA00]━━━━━━━━━━━━━
[C][B][FFFFFF]ACCOUNT DETAILS
[C][FFAA00]━━━━━━━━━━━━━
[C][FFFFFF]Create Date : [66FF00]{human_time(acc.get('AccountCreateTime'))[:16]}
[C][FFFFFF]Last Login  : [66FF00]{human_time(acc.get('AccountLastLogin'))[:16]}
[C][FFFFFF]BR Max Rank     : [66FF00]{ff_num(acc.get('BrMaxRank'))}
[C][FFFFFF]BR Points   : [66FF00]{ff_num(acc.get('BrRankPoint'))}
[C][FFFFFF]CS Max Rank     : [66FF00]{ff_num(acc.get('CsMaxRank'))}
[C][FFFFFF]CS Points   : [66FF00]{ff_num(acc.get('CsRankPoint'))}
[C][FFFFFF]Language    : [66FF00]{lang}
"""

    await safe_send_message(chat_type, msg2, uid, chat_id, key, iv)
    await asyncio.sleep(0.5)

    # ────────── MESSAGE 3 : FULL GUILD INFO ──────────
    msg3 = f"""
[C][B][FFAA00]━━━━━━━━━━━━━
[C][B][FFFFFF]GUILD INFORMATION
[C][FFAA00]━━━━━━━━━━━━━
[C][FFFFFF]Guild Name   : [66FF00]{guild.get('GuildName', 'No Guild')}
[C][FFFFFF]Guild ID     : [66FF00]{ff_num(guild.get('GuildID'))}
[C][FFFFFF]Owner UID    : [66FF00]{ff_num(guild.get('GuildOwner'))}
[C][FFFFFF]Guild Level  : [66FF00]{guild.get('GuildLevel', 'N/A')}
[C][FFFFFF]Members      : [66FF00]{guild.get('GuildMember', '0')}/{guild.get('GuildCapacity', '0')}
"""

    await safe_send_message(chat_type, msg3, uid, chat_id, key, iv)
	
#ADDING-100-LIKES-IN-24H
def send_likes(uid):
    try:
        likes_api_response = requests.get(
             f"https://yourlikeapi/like?uid={uid}&server_name={server2}&x-vercel-set-bypass-cookie=true&x-vercel-protection-bypass={BYPASS_TOKEN}",
             timeout=15
             )
      
      
        if likes_api_response.status_code != 200:
            return f"""
[C][B][FF0000]━━━━━
[FFFFFF]Like API Error!
Status Code: {likes_api_response.status_code}
Please check if the uid is correct.
━━━━━
"""

        api_json_response = likes_api_response.json()

        player_name = api_json_response.get('PlayerNickname', 'Unknown')
        likes_before = api_json_response.get('LikesbeforeCommand', 0)
        likes_after = api_json_response.get('LikesafterCommand', 0)
        likes_added = api_json_response.get('LikesGivenByAPI', 0)
        status = api_json_response.get('status', 0)

        if status == 1 and likes_added > 0:
            # ✅ Success
            return f"""
[C][B][11EAFD]‎━━━━━━━━━━━━
[FFFFFF]Likes Status:

[00FF00]Likes Sent Successfully!

[FFFFFF]Player Name : [00FF00]{player_name}  
[FFFFFF]Likes Added : [00FF00]{likes_added}  
[FFFFFF]Likes Before : [00FF00]{likes_before}  
[FFFFFF]Likes After : [00FF00]{likes_after}  
[C][B][11EAFD]‎━━━━━━━━━━━━
[C][B][FFB300]Subscribe: [FFFFFF]SPIDEERIO YT [00FF00]!!
"""
        elif status == 2 or likes_before == likes_after:
            # 🚫 Already claimed / Maxed
            return f"""
[C][B][FF0000]━━━━━━━━━━━━

[FFFFFF]No Likes Sent!

[FF0000]You have already taken likes with this UID.
Try again after 24 hours.

[FFFFFF]Player Name : [FF0000]{player_name}  
[FFFFFF]Likes Before : [FF0000]{likes_before}  
[FFFFFF]Likes After : [FF0000]{likes_after}  
[C][B][FF0000]━━━━━━━━━━━━
"""
        else:
            # ❓ Unexpected case
            return f"""
[C][B][FF0000]━━━━━━━━━━━━
[FFFFFF]Unexpected Response!
Something went wrong.

Please try again or contact support.
━━━━━━━━━━━━
"""

    except requests.exceptions.RequestException:
        return """
[C][B][FF0000]━━━━━
[FFFFFF]Like API Connection Failed!
Is the API server (app.py) running?
━━━━━
"""
    except Exception as e:
        return f"""
[C][B][FF0000]━━━━━
[FFFFFF]An unexpected error occurred:
[FF0000]{str(e)}
━━━━━
"""

#CHECK ACCOUNT IS BANNED

Hr = {
    'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'Content-Type': "application/x-www-form-urlencoded",
    'Expect': "100-continue",
    'X-Unity-Version': "2018.4.11f1",
    'X-GA': "v1 1",
    'ReleaseVersion': "OB52"}

# ---- Random Colores ----
def get_random_color():
    colors = [
        "[FF0000]", "[00FF00]", "[0000FF]", "[FFFF00]", "[FF00FF]", "[00FFFF]", "[FFFFFF]", "[FFA500]",
        "[A52A2A]", "[800080]", "[000000]", "[808080]", "[C0C0C0]", "[FFC0CB]", "[FFD700]", "[ADD8E6]",
        "[90EE90]", "[D2691E]", "[DC143C]", "[00CED1]", "[9400D3]", "[F08080]", "[20B2AA]", "[FF1493]",
        "[7CFC00]", "[B22222]", "[FF4500]", "[DAA520]", "[00BFFF]", "[00FF7F]", "[4682B4]", "[6495ED]",
        "[5F9EA0]", "[DDA0DD]", "[E6E6FA]", "[B0C4DE]", "[556B2F]", "[8FBC8F]", "[2E8B57]", "[3CB371]",
        "[6B8E23]", "[808000]", "[B8860B]", "[CD5C5C]", "[8B0000]", "[FF6347]", "[FF8C00]", "[BDB76B]",
        "[9932CC]", "[8A2BE2]", "[4B0082]", "[6A5ACD]", "[7B68EE]", "[4169E1]", "[1E90FF]", "[191970]",
        "[00008B]", "[000080]", "[008080]", "[008B8B]", "[B0E0E6]", "[AFEEEE]", "[E0FFFF]", "[F5F5DC]",
        "[FAEBD7]"
    ]
    return random.choice(colors)

print(get_random_color())
    
# ---- Random Avatar ----
async def get_random_avatar():
    await asyncio.sleep(0)  # makes it async but instant
    avatar_list = [
        '902042010', '902037031', '902042010', '902037031', '902042010',
        '902037031', '902042010', '902037031', '902042010', '902037031'
    ]
    return random.choice(avatar_list)

async def ultra_quick_emote_attack(team_code, emote_id, target_uid, key, iv, region):
    """Join team, authenticate chat, perform emote, and leave automatically"""
    try:
        # Step 1: Join the team
        join_packet = await GenJoinSquadsPacket(team_code, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
        print(f"🤖 Joined team: {team_code}")
        
        # Wait for team data and chat authentication
        await asyncio.sleep(1.5)  # Increased to ensure proper connection
        
        # Step 2: The bot needs to be detected in the team and authenticate chat
        # This happens automatically in TcPOnLine, but we need to wait for it
        
        # Step 3: Perform emote to target UID
        emote_packet = await Emote_k(int(target_uid), int(emote_id), key, iv, region)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', emote_packet)
        print(f"🎭 Performed emote {emote_id} to UID {target_uid}")
        
        # Wait for emote to register
        await asyncio.sleep(0.01)
        
        # Step 4: Leave the team
        leave_packet = await ExiT(None, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave_packet)
        print(f"🚪 Left team: {team_code}")
        
        return True, f"Quick emote attack completed! Sent emote to UID {target_uid}"
        
    except Exception as e:
        return False, f"Quick emote attack failed: {str(e)}"
        
        
async def encrypted_proto(encoded_hex):
    key = b'Yg&tc%DEuh6%Zc^8'
    iv = b'6oyZDr22E3ychjM%'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(encoded_hex, AES.block_size)
    encrypted_payload = cipher.encrypt(padded_message)
    return encrypted_payload
    
async def GeNeRaTeAccEss(uid , password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": (await Ua()),
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"}
    data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=Hr, data=data) as response:
            if response.status != 200: return "Failed to get access token"
            data = await response.json()
            open_id = data.get("open_id")
            access_token = data.get("access_token")
            return (open_id, access_token) if open_id and access_token else (None, None)

async def EncRypTMajoRLoGin(open_id, access_token):
    major_login = MajoRLoGinrEq_pb2.MajorLogin()
    major_login.event_time = str(datetime.now())[:-7]
    major_login.game_name = "free fire"
    major_login.platform_id = 1
    major_login.client_version = "1.120.2"
    major_login.system_software = "Android OS 9 / API-28 (PQ3B.190801.10101846/G9650ZHU2ARC6)"
    major_login.system_hardware = "Handheld"
    major_login.telecom_operator = "Verizon"
    major_login.network_type = "WIFI"
    major_login.screen_width = 1920
    major_login.screen_height = 1080
    major_login.screen_dpi = "280"
    major_login.processor_details = "ARM64 FP ASIMD AES VMH | 2865 | 4"
    major_login.memory = 3003
    major_login.gpu_renderer = "Adreno (TM) 640"
    major_login.gpu_version = "OpenGL ES 3.1 v1.46"
    major_login.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
    major_login.client_ip = "223.191.51.89"
    major_login.language = "en"
    major_login.open_id = open_id
    major_login.open_id_type = "4"
    major_login.device_type = "Handheld"
    memory_available = major_login.memory_available
    memory_available.version = 55
    memory_available.hidden_value = 81
    major_login.access_token = access_token
    major_login.platform_sdk_id = 1
    major_login.network_operator_a = "Verizon"
    major_login.network_type_a = "WIFI"
    major_login.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    major_login.external_storage_total = 36235
    major_login.external_storage_available = 31335
    major_login.internal_storage_total = 2519
    major_login.internal_storage_available = 703
    major_login.game_disk_storage_available = 25010
    major_login.game_disk_storage_total = 26628
    major_login.external_sdcard_avail_storage = 32992
    major_login.external_sdcard_total_storage = 36235
    major_login.login_by = 3
    major_login.library_path = "/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/lib/arm64"
    major_login.reg_avatar = 1
    major_login.library_token = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/base.apk"
    major_login.channel_type = 3
    major_login.cpu_type = 2
    major_login.cpu_architecture = "64"
    major_login.client_version_code = "2019118695"
    major_login.graphics_api = "OpenGLES2"
    major_login.supported_astc_bitset = 16383
    major_login.login_open_id_type = 4
    major_login.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWA0FUgsvA1snWlBaO1kFYg=="
    major_login.loading_time = 13564
    major_login.release_channel = "android"
    major_login.extra_info = "KqsHTymw5/5GB23YGniUYN2/q47GATrq7eFeRatf0NkwLKEMQ0PK5BKEk72dPflAxUlEBir6Vtey83XqF593qsl8hwY="
    major_login.android_engine_init_flag = 110009
    major_login.if_push = 1
    major_login.is_vpn = 1
    major_login.origin_platform_type = "4"
    major_login.primary_platform_type = "4"
    string = major_login.SerializeToString()
    return  await encrypted_proto(string)

async def MajorLogin(payload):
    url = "https://loginbp.ggblueshark.com/MajorLogin"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200: return await response.read()
            return None

async def GetLoginData(base_url, payload, token):
    url = f"{base_url}/GetLoginData"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    Hr['Authorization']= f"Bearer {token}"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200: return await response.read()
            return None

async def DecRypTMajoRLoGin(MajoRLoGinResPonsE):
    proto = MajoRLoGinrEs_pb2.MajorLoginRes()
    proto.ParseFromString(MajoRLoGinResPonsE)
    return proto

async def DecRypTLoGinDaTa(LoGinDaTa):
    proto = PorTs_pb2.GetLoginData()
    proto.ParseFromString(LoGinDaTa)
    return proto

async def DecodeWhisperMessage(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = DEcwHisPErMsG_pb2.DecodeWhisper()
    proto.ParseFromString(packet)
    return proto
    
async def decode_team_packet(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = sQ_pb2.recieved_chat()
    proto.ParseFromString(packet)
    return proto
    
async def xAuThSTarTuP(TarGeT, token, timestamp, key, iv):
    uid_hex = hex(TarGeT)[2:]
    uid_length = len(uid_hex)
    encrypted_timestamp = await DecodE_HeX(timestamp)
    encrypted_account_token = token.encode().hex()
    encrypted_packet = await EnC_PacKeT(encrypted_account_token, key, iv)
    encrypted_packet_length = hex(len(encrypted_packet) // 2)[2:]
    if uid_length == 9: headers = '0000000'
    elif uid_length == 8: headers = '00000000'
    elif uid_length == 10: headers = '000000'
    elif uid_length == 7: headers = '000000000'
    else: print('Unexpected length') ; headers = '0000000'
    return f"0115{headers}{uid_hex}{encrypted_timestamp}00000{encrypted_packet_length}{encrypted_packet}"
     
async def cHTypE(H):
    if not H: return 'Squid'
    elif H == 1: return 'CLan'
    elif H == 2: return 'PrivaTe'
    
async def SEndMsG(H , message , Uid , chat_id , key , iv):
    TypE = await cHTypE(H)
    if TypE == 'Squid': msg_packet = await xSEndMsgsQ(message , chat_id , key , iv)
    elif TypE == 'CLan': msg_packet = await xSEndMsg(message , 1 , chat_id , chat_id , key , iv)
    elif TypE == 'PrivaTe': msg_packet = await xSEndMsg(message , 2 , Uid , Uid , key , iv)
    return msg_packet

async def SEndPacKeT(OnLinE , ChaT , TypE , PacKeT):
    try:
        global whisper_writer, online_writer
        if TypE == 'ChaT':
            if whisper_writer is not None:
                whisper_writer.write(PacKeT)
                await whisper_writer.drain()
            else:
                print("⚠️ চ্যাট কানেকশন নেই, মেসেজ পাঠানো যায়নি!")
        elif TypE == 'OnLine':
            if online_writer is not None:
                online_writer.write(PacKeT)
                await online_writer.drain()
    except Exception as e:
        print(f"Packet Send Error: {e}") 

async def safe_send_message(chat_type, message, target_uid, chat_id, key, iv, max_retries=3):
    """Safely send message with retry mechanism"""
    for attempt in range(max_retries):
        try:
            P = await SEndMsG(chat_type, message, target_uid, chat_id, key, iv)
            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
            print(f"Message sent successfully on attempt {attempt + 1}")
            return True
        except Exception as e:
            print(f"Failed to send message (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(0.5)  # Wait before retry
    return False

async def fast_emote_spam(uids, emote_id, key, iv, region):
    """Fast emote spam function that sends emotes rapidly"""
    global fast_spam_running
    count = 0
    max_count = 25  # Spam 25 times
    
    while fast_spam_running and count < max_count:
        for uid in uids:
            try:
                uid_int = int(uid)
                H = await Emote_k(uid_int, int(emote_id), key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
            except Exception as e:
                print(f"Error in fast_emote_spam for uid {uid}: {e}")
        
        count += 1
        await asyncio.sleep(0.1)  # 0.1 seconds interval between spam cycles

# NEW FUNCTION: Custom emote spam with specified times
async def custom_emote_spam(uid, emote_id, times, key, iv, region):
    """Custom emote spam function that sends emotes specified number of times"""
    global custom_spam_running
    count = 0
    
    while custom_spam_running and count < times:
        try:
            uid_int = int(uid)
            H = await Emote_k(uid_int, int(emote_id), key, iv, region)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
            count += 1
            await asyncio.sleep(0.1)  # 0.1 seconds interval between emotes
        except Exception as e:
            print(f"Error in custom_emote_spam for uid {uid}: {e}")
            break

# NEW FUNCTION: Faster spam request loop - Sends exactly 30 requests quickly
async def spam_request_loop_with_cosmetics(target_uid, key, iv, region):
    """Spam request function with cosmetics - using your same structure"""
    global spam_request_running
    
    count = 0
    max_requests = 30
    
    # Different badge values to rotate through
    badge_rotation = [1048576, 32768, 2048, 64, 4094, 11233, 262144]
    
    while spam_request_running and count < max_requests:
        try:
            # Rotate through different badges
            current_badge = badge_rotation[count % len(badge_rotation)]
            
            # Create squad (same as before)
            PAc = await OpEnSq(key, iv, region)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', PAc)
            await asyncio.sleep(0.2)
            
            # Change squad size (same as before)
            C = await cHSq(5, int(target_uid), key, iv, region)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', C)
            await asyncio.sleep(0.2)
            
            # Send invite WITH COSMETICS (enhanced version)
            V = await SEnd_InV_With_Cosmetics(5, int(target_uid), key, iv, region, current_badge)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', V)
            
            # Leave squad (same as before)
            E = await ExiT(None, key, iv)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', E)
            
            count += 1
            print(f"✅ Sent cosmetic invite #{count} to {target_uid} with badge {current_badge}")
            
            # Short delay
            await asyncio.sleep(0.5)
            
        except Exception as e:
            print(f"Error in cosmetic spam: {e}")
            await asyncio.sleep(0.5)
    
    return count
            


# NEW FUNCTION: Evolution emote spam with mapping
async def evo_emote_spam(uids, number, key, iv, region):
    """Send evolution emotes based on number mapping"""
    try:
        emote_id = GENERAL_EMOTES_MAP.get(int(number))
        if not emote_id:
            return False, f"Invalid number! Use 1-21 only."
        
        success_count = 0
        for uid in uids:
            try:
                uid_int = int(uid)
                H = await Emote_k(uid_int, emote_id, key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                success_count += 1
                await asyncio.sleep(0.1)
            except Exception as e:
                print(f"Error sending evo emote to {uid}: {e}")
        
        return True, f"Sent evolution emote {number} (ID: {emote_id}) to {success_count} player(s)"
    
    except Exception as e:
        return False, f"Error in evo_emote_spam: {str(e)}"

# NEW FUNCTION: Fast evolution emote spam
async def evo_fast_emote_spam(uids, number, key, iv, region):
    """Fast evolution emote spam function"""
    global evo_fast_spam_running
    count = 0
    max_count = 25  # Spam 25 times
    
    emote_id = GENERAL_EMOTES_MAP.get(int(number))
    if not emote_id:
        return False, f"Invalid number! Use 1-21 only."
    
    while evo_fast_spam_running and count < max_count:
        for uid in uids:
            try:
                uid_int = int(uid)
                H = await Emote_k(uid_int, emote_id, key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
            except Exception as e:
                print(f"Error in evo_fast_emote_spam for uid {uid}: {e}")
        
        count += 1
        await asyncio.sleep(0.1)  # CHANGED: 0.5 seconds to 0.1 seconds
    
    return True, f"Completed fast evolution emote spam {count} times"

# NEW FUNCTION: Custom evolution emote spam with specified times
async def evo_custom_emote_spam(uids, number, times, key, iv, region):
    """Custom evolution emote spam with specified repeat times"""
    global evo_custom_spam_running
    count = 0
    
    emote_id = GENERAL_EMOTES_MAP.get(int(number))
    if not emote_id:
        return False, f"Invalid number! Use 1-21 only."
    
    while evo_custom_spam_running and count < times:
        for uid in uids:
            try:
                uid_int = int(uid)
                H = await Emote_k(uid_int, emote_id, key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
            except Exception as e:
                print(f"Error in evo_custom_emote_spam for uid {uid}: {e}")
        
        count += 1
        await asyncio.sleep(0.1)  # CHANGED: 0.5 seconds to 0.1 seconds
    
    return True, f"Completed custom evolution emote spam {count} times"

async def RejectMSGtaxt(squad_owner, uid, key, iv, region="BD"):
    random_banner = """
.
.
.
.
.










[00FF00]ＷＥＬＣＯＭＥ ＴＯ[FF0000] _ _ _ M A H I R _ _ _ _   [00FF00]ＢＯＴ
[FF0000]━[00FF00]━[0000FF]━[FFFF00]━[FF00FF]━[00FFFF]━[FFA500]━[FF1493]━[00FF7F]━[FFD700]━[00CED1]━[9400D3]━[FF6347]━[32CD32]━[7B68EE]━[FF4500]━[1E90FF]━[ADFF2F]━[FF69B4]━[8A2BE2]━[DC143C]━[FF8C00]━[BA55D3]━[7CFC00]━[FFC0CB]
[1E90FF]ＤＥＶ   [FF0000]_ _ _ M A H I R _ _ _ _
[FF0000]━[00FF00]━[0000FF]━[FFFF00]━[FF00FF]━[00FFFF]━[FFA500]━[FF1493]━[00FF7F]━[FFD700]━[00CED1]━[9400D3]━[FF6347]━[32CD32]━[7B68EE]━[FF4500]━[1E90FF]━[ADFF2F]━[FF69B4]━[8A2BE2]━[DC143C]━[FF8C00]━[BA55D3]━[7CFC00]━[FFC0CB]
[FF0000]_ _ _ M A H I R _ _ _ _
[FF0000]━[00FF00]━[0000FF]━[FFFF00]━[FF00FF]━[00FFFF]━[FFA500]━[FF1493]━[00FF7F]━[FFD700]━[00CED1]━[9400D3]━[FF6347]━[32CD32]━[7B68EE]━[FF4500]━[1E90FF]━[ADFF2F]━[FF69B4]━[8A2BE2]━[DC143C]━[FF8C00]━[BA55D3]━[7CFC00]━[FFC0CB]
[9400D3]M A D E B Y [FF0000]M A H I R
[FF0000]━[00FF00]━[0000FF]━[FFFF00]━[FF00FF]━[00FFFF]━[FFA500]━[FF1493]━[00FF7F]━[FFD700]━[00CED1]━[9400D3]━[FF6347]━[32CD32]━[7B68EE]━[FF4500]━[1E90FF]━[ADFF2F]━[FF69B4]━[8A2BE2]━[DC143C]━[FF8C00]━[BA55D3]━[7CFC00]━[FFC0CB]
[FFD700] ＦＯＬＬＯＷ    ＭＥ   ＩＮ   [87CEEB]TELEGRAM: [FF0000]@ARIYAN0208
[FF0000]━[00FF00]━[0000FF]━[FFFF00]━[FF00FF]━[00FFFF]━[FFA500]━[FF1493]━[00FF7F]━[FFD700]━[00CED1]━[9400D3]━[FF6347]━[32CD32]━[7B68EE]━[FF4500]━[1E90FF]━[ADFF2F]━[FF69B4]━[8A2BE2]━[DC143C]━[FF8C00]━[BA55D3]━[7CFC00]━[FFC0CB]"""
    
    fields = {
        1: 5,
        2: {
            1: int(squad_owner),
            2: 1,
            3: int(uid),
            4: random_banner
        }
    }
    # Choose packet type based on region
    if region.lower() == "bd":
        packet_type = "0519"
    elif region.lower() == "ind":
        packet_type = "0514"
    else:
        packet_type = "0515"
    
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet_type, key, iv)

async def send_keep_alive(key, iv, region):
    """Send keep-alive packet to maintain connection"""
    try:
        fields = {
            1: 99,  # Keep-alive packet type
            2: {
                1: int(time.time()),
                2: 1,  # Keep-alive flag
            }
        }
        
        if region.lower() == "ind":
            packet_type = '0514'
        elif region.lower() == "bd":
            packet_type = "0519"
        else:
            packet_type = "0515"
            
        packet = await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet_type, key, iv)
        return packet
    except Exception as e:
        print(f"❌ Keep-alive error: {e}")
        return None

async def ArohiAccepted(bot_uid, squad_owner, code, key, iv, region="BD"):
    fields = {
        1: 4,  # Accept invite
        2: {
            1: int(squad_owner),
            3: int(bot_uid),
            8: 1,
            9: {
                2: 161,
                4: "y[WW",
                6: 11,
                8: "1.114.18",  # Your bot's version
                9: 3,
                10: 1
            },
            10: str(code),  # Invite Code
        }
    }
    # BD Server usually uses 0519
    packet_type = "0519" if region.lower() == "bd" else "0515"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet_type, key, iv)


async def TcPOnLine(ip, port, key, iv, AutHToKen, region="BD", reconnect_delay=1):
    import asyncio, json, random, time, traceback

    global online_writer, whisper_writer, insquad, joining_team, senthi

    bot_uid = 14716877021
    BOT_OWNER_UID = bot_uid  

    # স্টেট ইনিশিয়াল
    insquad = False
    joining_team = False
    senthi = False
    last_join_time = 0  # 🔥 ডাবল ইনভাইট বন্ধ করার ম্যাজিক টাইমার
    last_emote_time = 0 # 🔥 [NEW] ইনফিনিটি ইমোট লুপ ঠেকানোর জন্য টাইমার
    last_vbadge_req_time = 0
    last_bundle_anim_time = 0

    while True:
        try:
            print(f"📡 সার্ভারে কানেক্ট হচ্ছে... {ip}:{port}")
            reader, writer = await asyncio.open_connection(ip, int(port))
            online_writer = writer

            # ================= AUTHENTICATION =================
            writer.write(bytes.fromhex(AutHToKen))
            await writer.drain()
            print("✅ বট অনলাইন! ইনভাইট চেক করছে...")

            while True:
                data = await reader.read(4096)
                if not data:
                    print("⚠️ কানেকশন লস্ট!")
                    break

                data_hex = data.hex()
                packets = data_hex.split("0500")

                for p in packets:
                    if len(p) < 10:
                        continue

                    try:
                        decoded_str = await DeCode_PackEt(p[6:])
                        if not decoded_str:
                            continue

                        packet_json = json.loads(decoded_str)
                        packet_id = packet_json.get('1')

                        # ================= KICK/LEAVE =================
                        if packet_id in [6,7,8,9,11,12,13,14]:
                            print(f"🚪 কিক/লিভ ডিটেক্ট (ID: {packet_id}) → স্টেট রিসেট")
                            insquad = False
                            joining_team = False
                            senthi = False
                            continue

                        # ================= 🔥 AUTO COPY EMOTE (MIRROR) 🔥 =================
                        # ফ্রি ফায়ারে স্কোয়াড ইমোট প্যাকেট আইডি সাধারণত 21 বা 26 হয়
                        if insquad and packet_id in [21, 26]:
                            current_time = time.time()
                            
                            try:
                                sender_uid = None
                                emote_id = None
                                
                                # Packet ID 21 (Standard Emote Packet) থেকে ডেটা বের করা
                                if packet_id == 21:
                                    try:
                                        nested = packet_json['2']['data']['5']['data']
                                        sender_uid = nested.get('1', {}).get('data')
                                        emote_id = nested.get('3', {}).get('data')
                                    except: pass
                                    
                                # Packet ID 26 (Direct Emote Packet) থেকে ডেটা বের করা
                                elif packet_id == 26:
                                    try:
                                        nested = packet_json['2']['data']
                                        sender_uid = nested.get('1', {}).get('data')
                                        emote_id = nested.get('2', {}).get('data')
                                    except: pass

                                # যদি ইমোট আইডি এবং কে দিয়েছে তা পাওয়া যায়
                                if sender_uid and emote_id:
                                    # শর্ত: বট যেন নিজের ইমোট নিজে কপি না করে
                                    if str(sender_uid) != str(bot_uid):
                                        # ১ সেকেন্ডের কুলডাউন 
                                        if current_time - last_emote_time > 1.0:
                                            print(f"👀 প্লেয়ার {sender_uid} ইমোট দিয়েছে: {emote_id}! বট কপি করছে...")
                                            last_emote_time = current_time # টাইমার আপডেট
                                            
                                            # বট সাথে সাথে ওই সেম ইমোটটি দিবে
                                            mirror_emote_packet = await Emote_k(bot_uid, int(emote_id), key, iv, region)
                                            if mirror_emote_packet:
                                                writer.write(mirror_emote_packet)
                                                await writer.drain()
                                                print("✅ ইমোট কপি সাকসেসফুল!")
                            except Exception as emote_err:
                                print(f"Emote Mirror Error: {emote_err}")

                        # ================= INVITE =================
                        if '5' in packet_json and isinstance(packet_json['5'], dict) and 'data' in packet_json['5']:
                            invite_data = packet_json['5']['data']
                            
                            # 🔥 [FIX 1] চেক করে নিচ্ছি invite_data আদতে ডিকশনারি (dict) কিনা
                            if isinstance(invite_data, dict):
                                squad_owner_raw = invite_data.get('1', {})
                                invite_code_raw = invite_data.get('8', {})
                                
                                squad_owner = squad_owner_raw.get('data') if isinstance(squad_owner_raw, dict) else None
                                invite_code = invite_code_raw.get('data') if isinstance(invite_code_raw, dict) else None

                                if squad_owner and invite_code:
                                    # 🔥 [FIX] ২ সেকেন্ডের মধ্যে আসা ডাবল/ফেক ইনভাইট ইগনোর করবে
                                    if time.time() - last_join_time < 2:
                                        continue
                                    last_join_time = time.time()

                                    print(f"📩 ইনভাইট পাওয়া গেছে! Owner: {squad_owner}")

                                    # 🌟 [NEW & FIXED] Premium V-Badge Auto Request (5 Seconds Cooldown) 🌟
                                    current_req_time = time.time()
                                    if current_req_time - last_vbadge_req_time >= 5.0:
                                        try:
                                            v_badge_value = 262144  
                                            v_badge_packet = await request_join_with_badge(
                                                squad_owner, v_badge_value, key, iv, region
                                            )
                                            writer.write(v_badge_packet)
                                            await writer.drain()
                                            print("🌟 V-Badge Auto-Request sent to Owner!")
                                            
                                            last_vbadge_req_time = current_req_time # টাইমার আপডেট করা হলো
                                            await asyncio.sleep(0.7) 
                                        except Exception as e:
                                            print(f"Error sending auto V-Badge request: {e}")
                                    else:
                                        print("⏳ V-Badge Request Skipped (5s Cooldown Active)")

                                    # জয়েন রিকোয়েস্ট (V-Badge যাক বা না যাক, বট গ্রুপে ঠিকই জয়েন করবে)
                                    accept_packet = await ArohiAccepted(
                                        bot_uid,
                                        squad_owner,
                                        invite_code,
                                        key,
                                        iv
                                    )
                                    writer.write(accept_packet)
                                    await writer.drain()

                                    insquad = True
                                    joining_team = True
                                    senthi = False
                                    print("🚀 জয়েন রিকোয়েস্ট পাঠানো হয়েছে!")                                    

                        # ================= AFTER JOIN =================
                        if insquad and (joining_team or senthi):
                            sq_data = await GeTSQDaTa(packet_json)
                            if sq_data:
                                owner_uid, chat_code, squad_code = sq_data

                                if joining_team:
                                    print(f"🔑 চ্যাট অথেন্টিকেশন: {owner_uid}")
                                    join_chat_packet = await AutH_Chat(
                                        3,
                                        owner_uid,
                                        chat_code,
                                        key,
                                        iv
                                    )
                                    await SEndPacKeT(
                                        whisper_writer,
                                        online_writer,
                                        'ChaT',
                                        join_chat_packet
                                    )

                                    # ================= WELCOME =================
                                    welcome_msg = (
                                        "[B][C][FB0364]╭[D21A92]─[BC26AB]╮[00BFFF]╔═══════╗\n[B][C][FF7244]│[FE4250]▶[C81F9C]֯│[FFFF00]║[FFFFFF] WLC ARIYAN BOT [FFFF00]║\n[B][C][FDC92B]╰[FF7640]─[F5066B]╯[00BFFF]╚═══════╝"
                                    )
                                    p_msg = await SEndMsG(
                                        0,
                                        welcome_msg,
                                        owner_uid,
                                        owner_uid,
                                        key,
                                        iv
                                    )
                                    await SEndPacKeT(
                                        whisper_writer,
                                        online_writer,
                                        'ChaT',
                                        p_msg
                                    )

                                    await asyncio.sleep(0.8)
                                    
                                    # ================= 3 SECOND ANIMATION + BUNDLE =================
                                    current_anim_time = time.time()
                                    
                                    if current_anim_time - last_bundle_anim_time >= 5.0:
                                        last_bundle_anim_time = current_anim_time # টাইমার আপডেট করা হলো

                                        # ব্যাকগ্রাউন্ড টাস্ক (যাতে ৩ সেকেন্ড অপেক্ষার সময় বট আটকে না যায়)
                                        async def play_anim_and_bundle(w_writer, o_writer, k, v, reg):
                                            try:
                                                bundle_ids = {
                                                    1: 914000002, 2: 914000003, 3: 914038001,
                                                    4: 914039001, 5: 914042001, 6: 914044001,
                                                    7: 914047001, 8: 914047002, 9: 914048001,
                                                    10: 914050001, 11: 914051001
                                                }
                                                
                                                # যেকোনো একটি র‍্যান্ডম বান্ডিল সিলেক্ট করবে
                                                bundle_index = random.randint(1, 11)
                                                real_bundle_id = bundle_ids[bundle_index]

                                                # ১. প্রথমে অ্যানিমেশন প্যাকেট সেন্ড করবে
                                                anim_packet = await animation_packet(real_bundle_id, k, v)
                                                if anim_packet and o_writer:
                                                    await SEndPacKeT(w_writer, o_writer, 'OnLine', anim_packet)
                                                    print(f"✨ ৩ সেকেন্ডের অ্যানিমেশন শুরু: {bundle_index}")

                                                # ২. ঠিক ৩ সেকেন্ড অপেক্ষা করবে
                                                await asyncio.sleep(3.0)

                                                # ৩. ৩ সেকেন্ড পর ড্রেস চেঞ্জ করবে
                                                dress_packet = await bundle_packet_async(real_bundle_id, k, v, reg)
                                                if dress_packet and o_writer:
                                                    await SEndPacKeT(w_writer, o_writer, 'OnLine', dress_packet)
                                                    print(f"📦 ড্রেস চেঞ্জ করা হয়েছে: {bundle_index}")

                                            except Exception as e:
                                                print(f"Animation + Bundle Error: {e}")

                                        # টাস্কটি চালু করে দেওয়া হলো
                                        asyncio.create_task(play_anim_and_bundle(whisper_writer, online_writer, key, iv, region))
                                    else:
                                        print("⏳ Bundle Animation Skipped (5s Cooldown Active)")

                                    # ================= DUAL EMOTE =================
                                    await auto_rings_emote_dual(
                                        owner_uid,
                                        key,
                                        iv,
                                        region
                                    )
                                    print("🎉 ইমোট পাঠানো হয়েছে!")

                                    joining_team = False

                    except Exception as e:
                        print(f"⚠ Packet Error: {e}")
                        traceback.print_exc()
                        continue

                # ================= TEAM CONFIRM =================
                if "0600" in data_hex[:10]:
                    insquad = True
                    senthi = True

        except Exception as e:
            print(f"❌ কানেকশন এরর: {e}")
            traceback.print_exc()
            # স্টেট রিসেট
            insquad = False
            joining_team = False
            senthi = False

        # রিকনেক্ট ডিলে
        await asyncio.sleep(reconnect_delay)
        
                    

                            
async def TcPChaT(ip, port, AutHToKen, key, iv, LoGinDaTaUncRypTinG, ready_event, region , reconnect_delay=0.5):
    print(region, 'TCP CHAT')

    global spam_room , whisper_writer , spammer_uid , spam_chat_id , spam_uid , online_writer , chat_id , XX , uid , Spy,data2, Chat_Leave, fast_spam_running, fast_spam_task, custom_spam_running, custom_spam_task, spam_request_running, spam_request_task, evo_fast_spam_running, evo_fast_spam_task, evo_custom_spam_running, evo_custom_spam_task, lag_running, lag_task, evo_cycle_running, evo_cycle_task, reject_spam_running, reject_spam_task
    while True:
        try:
            reader , writer = await asyncio.open_connection(ip, int(port))
            whisper_writer = writer
            bytes_payload = bytes.fromhex(AutHToKen)
            whisper_writer.write(bytes_payload)
            await whisper_writer.drain()
            ready_event.set()
            if LoGinDaTaUncRypTinG.Clan_ID:
                clan_id = LoGinDaTaUncRypTinG.Clan_ID
                clan_compiled_data = LoGinDaTaUncRypTinG.Clan_Compiled_Data
                print('\n - TarGeT BoT in CLan ! ')
                print(f' - Clan Uid > {clan_id}')
                print(f' - BoT ConnEcTed WiTh CLan ChaT SuccEssFuLy ! ')
                pK = await AuthClan(clan_id , clan_compiled_data , key , iv)
                if whisper_writer: whisper_writer.write(pK) ; await whisper_writer.drain()
            while True:
                data = await reader.read(9999)
                if not data: break
                
                if data.hex().startswith("120000"):

                    msg = await DeCode_PackEt(data.hex()[10:])
                    chatdata = json.loads(msg)
                    try:
                        response = await DecodeWhisperMessage(data.hex()[10:])
                        uid = response.Data.uid
                        chat_id = response.Data.Chat_ID
                        XX = response.Data.chat_type
                        inPuTMsG = response.Data.msg.lower()
                        
                        # Debug print to see what we're receiving
                        print(f"Received message: {inPuTMsG} from UID: {uid} in chat type: {XX}")

                        # --- AUTO FOR EVERYONE ---
                        msg2 = inPuTMsG.strip().lower()

                        if msg2.isdigit():
                            level = int(msg2)

                        elif msg2 in WORD_TO_LEVEL:
                            level = WORD_TO_LEVEL[msg2]

                        else:
                            level = None

                        if level is not None and 0 <= level <= 408:
                            inPuTMsG = f"/c {uid} {level}"
                        
                    except:
                        response = None


                    if response:
                        # ALL COMMANDS NOW WORK IN ALL CHAT TYPES (SQUAD, GUILD, PRIVATE)
                        
                        # --- AUTO FOR EVERYONE ---                    
                        try:
                            parts = inPuTMsG.strip().split()

                            # যদি ইউজার 2টা সংখ্যা লিখে: emote_number + times
                            if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                                emote_number = parts[0]
                                times = int(parts[1])

                                if emote_number in EMOTE_MAP and 0 < times <= 100:
                                    emote_id = EMOTE_MAP[emote_number]

                                    # Auto convert to /p command
                                    inPuTMsG = f"/p {uid} {emote_id} {times}"

                        except Exception as e:
                            print("Error in auto /p conversion:", e)                        
# ================== FINAL AUTO SYSTEM ==================
                        try:
                            msg = inPuTMsG.strip().lower()

                            # 🔒 ONLY SLASH COMMAND ALLOWED
                            if not msg.startswith("@"):
                                raise Exception("Not a slash command")

                            # remove /
                            msg = msg[1:]
                            parts = msg.split()

                            level = None

                            # ---------- AUTO LEVEL (/number or /name) ----------
                            if len(parts) == 1:
                                if parts[0].isdigit():
                                    level = int(parts[0])

                                elif parts[0] in WORD_TO_LEVEL:
                                    level = WORD_TO_LEVEL[parts[0]]

                                if level is not None and 0 <= level <= 408:
                                    inPuTMsG = f"/c {uid} 13793280064 {level}"

                            # ---------- AUTO EMOTE (/number times) ----------
                            elif len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                                emote_number = parts[0]
                                times = int(parts[1])

                                if emote_number in EMOTE_MAP and 0 < times <= 100:
                                    emote_id = EMOTE_MAP[emote_number]
                                    inPuTMsG = f"/p 13793280064 {emote_id} {times}"

                        except Exception:
                            pass
                        # ======================================================

                        # 🔥 FAKE VIP LIKES COMMAND - /like
                        if inPuTMsG.strip().startswith(('/like ', '/likes ')):
                            print('Processing VIP Fake Likes Command')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /like <uid>\nExample: /like 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                
                                # ১. প্রথমে একটি প্রসেসিং মেসেজ দিবে (Format Fixed)
                                wait_msg = (
                                    f"[B][C][00FFFF]╔════════════════════╗\n"
                                    f"[B][C][00FFFF]║   [FFFF00]🌟 VIP LIKE SERVER 🌟   [00FFFF]║\n"
                                    f"[B][C][00FFFF]╚════════════════════╝\n"
                                    f"[FFFFFF]⏳ Searching ID: [00FF00]{target_uid}\n"
                                    f"[FFFFFF]🔄 Connecting to Garena Server..."
                                )
                                await safe_send_message(response.Data.chat_type, wait_msg, uid, chat_id, key, iv)
                                
                                # একটু রিয়েল ফিল দেওয়ার জন্য ফেক ডিলে (Delay)
                                await asyncio.sleep(2)

                                # ফেক ডাটা তৈরি
                                fake_before = random.randint(1500, 4500)
                                fake_added = random.randint(3100, 3999) # 3000+ লাইক
                                fake_after = fake_before + fake_added
                                
                                # ২. ফাইনাল সাকসেস মেসেজ (Format Fixed)
                                success_msg = (
                                    f"[B][C][00FF00]✅ LIKES DELIVERED SUCCESSFULLY!\n\n"
                                    f"[B][C][FF00FF]👑 RAHATVIP LIKES PANEL 👑\n"
                                    f"[FFFFFF]━━━━━━━━━━━━━━━━━━\n"
                                    f"[00FFFF]👤 Target UID  : [FFFFFF]{target_uid}\n"
                                    f"[FFFF00]📈 Likes Before: [FFFFFF]{fake_before}\n"
                                    f"[00FF00]🔥 Likes Added : [FFFFFF]+{fake_added}\n"
                                    f"[FF00FF]🏆 Total Likes : [FFFFFF]{fake_after}\n"
                                    f"[FFFFFF]━━━━━━━━━━━━━━━━━━\n"
                                    f"[FFFF00]⚡ Powered By: [FFFFFF]RAHATBOT\n"
                                    f"[00FF00]💬 Status: [FFFFFF]Completed Instantly!"
                                )
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                
                                #TEAM SPAM MESSAGE COMMAND
                        if inPuTMsG.strip().startswith('/ms '):
                            print('Processing /ms command')

                            try:
                                parts = inPuTMsG.strip().split(maxsplit=1)

                                if len(parts) < 2:
                                    error_msg = (
                                        "[B][C][FF0000]❌ ERROR! Usage:\n"
                                        "/ms <message>\n"
                                        "Example: /ms ARIYAN"
                                    )
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    user_message = parts[1].strip()

                                    for _ in range(30):
                                        color = get_random_color()  # random color from your list
                                        colored_message = f"[B][C]{color} {user_message}"  # correct format
                                        await safe_send_message(response.Data.chat_type, colored_message, uid, chat_id, key, iv)
                                        await asyncio.sleep(0.5)

                            except Exception as e:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Something went wrong:\n{str(e)}"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                
              
                        # /gali কমান্ড হ্যান্ডলার (যেখানে inPuTMsG থেকে কমান্ড চেক করছেন)
                        if inPuTMsG.strip().startswith('/gali '):
                            print('Processing /gali command')
                            try:
                                parts = inPuTMsG.strip().split(maxsplit=1)

                                if len(parts) < 2:
                                    error_msg = (
                                        "[B][C][FF0000]❌ ERROR! Usage:\n"
                                        "/gali <name>\n"
                                        "Example: /gali hater"
                                    )
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    name = parts[1].strip()

                                    # নাম নরমালাইজ করুন: শুধু অক্ষর রাখুন, ছোট হাতের করুন
                                    normalized_name = re.sub(r'[^a-zA-Z]', '', name).lower()

                                    # ব্লক করা নামগুলোর তালিকা নরমালাইজ করে চেক করুন (সাবস্ট্রিং হিসেবে)
                                    blocked = False
                                    for blocked_name in BLOCKED_NAMES:
                                        normalized_blocked = re.sub(r'[^a-zA-Z]', '', blocked_name).lower()
                                        if normalized_blocked in normalized_name:
                                            blocked = True
                                            break

                                    if blocked:
                                        error_msg = (
                                            f"[B][C][FF0000]⚠️শা🤣লা মাদা🤐রচো🥴দ\n"
                                            f"[FFFFFF]তর এই বা🤣পে🤣র নামে গা🥴লি দিতে চাস\n"
                                            f"[FF0000]শা🤣লা মাদা🤣রচো😁দ"
                                        )
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        # এখানে ব্লক হয়ে গেলে পরবর্তী অংশ (মেসেজ পাঠানো) এক্সিকিউট হবে না
                                    else:
                                        # মূল মেসেজ পাঠানোর কোড
                                        messages = [
                    "{Name} আমি তোমার সেক্সি বোনের বোডায় আমার মেশিন ঢুকিয়ে সারা রাত ধরে তাকে জোরে জোরে চো-দব",
                    "{Name} তর মাকে তোর ওপরে ফেলে চো-দব",
                    "{Name} খান🤫কির ছেলে !!",
                    "{Name} মাদার চো🤫দ, তোর মা🤫কে চু🤫দি !!",
                    "{Name} মাদার চো🤫দ, তোর মা🤫কে 5G স্পিডে চু🤫দি !!",
                    "{Name} বোকাচো🤫দা, তোর মা🤫কে কন🤫ডম লাগিয়ে চু🤫দি !!",
                    "{Name} বোকাচো🤫দা, তোর মা🤫কে প্রতিদিন ১০,০০০ টাকার সার্ভিস দেই !!",
                    "F🤫U🤫C🤫K {Name} !!",
                    "{Name} মাদার চো??দ, পো🤫দ মে🤫রে দিবো !!",
                    "{Name} মাদার চো🤫দ !!",
                    "{Name} খান🤫কি, আমি তোর বা🤫প !!",
                    "{Name} তোর মা🤫কে আমি চু🤫ই🤫দা তোরে জন্মায় ছি !!",
                    "{Name} বোকাচো🤫দা, খান🤫কির ছেলে !!",
                    "{Name} মাদার চো🤫দ, তোর মা🤫কে ১৮০ কি.মি. স্পিডে চু🤫দি !!",
                    "{Name} খা🤫ন🤫কির ছেলে বট, নুব🤫রা প্লেয়ার !!",
                    "বাংলাদেশের NO-1 বট PLAYER {Name}",
                    "{Name} জুতা চোর !!",
                    "{Name} মাদারচো🤫দ, ফ্রি ফায়ার খেলা বাদ দিয়ে লুডু খেল যা !!",
                    "{Name} যাই করিস, আমি তোর অব্বা এইডা কখনো ভুলিস না !!"
                                        ]

                                        # প্রতিটি মেসেজ পাঠান
                                        for msg in messages:
                                            colored_message = f"[B][C][00FFFF] {msg.replace('{Name}', name.upper())}"
                                            await safe_send_message(response.Data.chat_type, colored_message, uid, chat_id, key, iv)
                                            await asyncio.sleep(2)

                            except Exception as e:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Something went wrong:\n{str(e)}"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                # ==================== GALI & TROLL COMMAND (ARIYAN PROTECTED + DUAL EMOTE + AUTO KICK) ====================
                        if inPuTMsG.strip().startswith('/gali2'):
                            print('Processing /gali2 command')
                            try:
                                parts = inPuTMsG.strip().split(maxsplit=2)

                                if len(parts) < 2:
                                    error_msg = (
                                        "[B][C][FF0000]❌ ERROR! ব্যবহারের নিয়ম:\n"
                                        "/gali <নাম> [ইউআইডি]\n"
                                        "উদাহরণ ১: /gali2 bot\n"
                                        "উদাহরণ ২: /gali2 bot 123456789"
                                    )
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    name = parts[1].strip()
                                    target_uid = parts[2].strip() if len(parts) > 2 else None
                                    sender_uid = uid  # যে কমান্ডটি লিখেছে তার ইউআইডি

                                    # নাম নরমালাইজ করুন
                                    normalized_name = re.sub(r'[^a-zA-Z]', '', name).lower()

                                    # 🔥 'Ariyan' চেক
                                    if "ariyan" in normalized_name or "arian" in normalized_name or "aryan" in normalized_name:
                                        error_msg = (
                                            f"[B][C][FFD700]⚠️ সাবধান!\n"
                                            f"[FFFFFF]ARIYAN তো এই বটের বস! বসের সাথে বেয়াদবি করা সম্পূর্ণ নিষেধ! 🤫👑"
                                        )
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    else:
                                        messages = [
                                            "{Name} বান্দির পোলা ",
                                            "উনারা জা {Name} মাংগির পোলা 🤣",
                                            "{Name} রাত করে ফাজলামি চুদা ও তোর মারে চু🤫দি",
                                            "তোর সাওয়া দিয়ে {Name} বাঁশ দিমু মাদারচোদ",
                                            "{Name} বাদামি করতে আসবি না",
                                            "{Name}, সব সময় বস বস বলে ডাকবি",
                                            "{Name} চুপচাপ মাফ চেয়ে ভাগ",
                                            "সালা {Name} টুকাই",
                                            "{Name} ভেন্ডিং খোর",
                                            "{Name} ভাগ এনতে"
                                        ]

                                        # ফাস্ট ইমোট স্প্যামের জন্য ব্যাকগ্রাউন্ড টাস্ক
                                        async def spam_gali_emote(s_uid, t_uid, key, iv, region, stop_event):
                                            
                                            # 👇 ১. যে কমান্ড দিয়েছে সে এই ইমোটটি দিবে (909000033 হলো Lol ইমোট)
                                            SENDER_EMOTE_ID = 909000002 
                                            
                                            # 👇 ২. টার্গেট আইডি এই ইমোটটি পাবে (এখানে আপনি আপনার পছন্দমতো আইডি বসিয়ে নিবেন)
                                            TARGET_EMOTE_ID = 909052011 # <--- এই আইডিটা আপনি চেঞ্জ করে নিবেন
                                            
                                            while not stop_event.is_set():
                                                try:
                                                    # সেন্ডারকে (যে লিখেছে তাকে) লল ইমোট দেওয়া
                                                    sender_emote = await Emote_k(int(s_uid), SENDER_EMOTE_ID, key, iv, region)
                                                    if online_writer and sender_emote:
                                                        online_writer.write(sender_emote)
                                                    
                                                    # যদি টার্গেট ইউআইডি থাকে, তবে তাকেও ইমোট দেওয়া
                                                    if t_uid and t_uid.isdigit():
                                                        target_emote = await Emote_k(int(t_uid), TARGET_EMOTE_ID, key, iv, region)
                                                        if online_writer and target_emote:
                                                            online_writer.write(target_emote)
                                                    
                                                    if online_writer:
                                                        await online_writer.drain()
                                                        
                                                except Exception:
                                                    pass
                                                await asyncio.sleep(0.2) # ইমোট স্প্যামের স্পিড

                                        # টাস্ক চালু করা হলো
                                        stop_emote = asyncio.Event()
                                        emote_task = asyncio.create_task(spam_gali_emote(sender_uid, target_uid, key, iv, region, stop_emote))

                                        # মেসেজ পাঠানোর মেইন লুপ
                                        for msg in messages:
                                            colored_message = f"[B][C][00FFFF] {msg.replace('{Name}', name.upper())}"
                                            await safe_send_message(response.Data.chat_type, colored_message, uid, chat_id, key, iv)
                                            await asyncio.sleep(2) # ২ সেকেন্ড পর পর মেসেজ

                                        # সব মেসেজ দেওয়া শেষ হলে ইমোট স্প্যাম স্টপ
                                        stop_emote.set()

                                        # 🔥 [নতুন আপডেট] গালি দেওয়া শেষ হলে অটোমেটিক কিক (Kick) করে দিবে 🔥
                                        if target_uid and target_uid.isdigit():
                                            try:
                                                kick_packet = await KickTarget(target_uid, key, iv)
                                                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', kick_packet)
                                                
                                                kick_msg = f"[B][C][FF0000]💥 {name.upper()} কে কিক মেরে গ্রুপ থেকে বের করে দেওয়া হলো! লবিতে যা বট! 💥"
                                                await safe_send_message(response.Data.chat_type, kick_msg, uid, chat_id, key, iv)
                                            except Exception as kick_err:
                                                print(f"Error kicking in gali2: {kick_err}")

                            except Exception as e:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Something went wrong:\n{str(e)}"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
# ==================== EXTERNAL API SPAM COMMAND (/spam2) ====================
                        if inPuTMsG.strip().startswith('/spam2 '):
                            print('Processing /spam2 external API command')
                            parts = inPuTMsG.strip().split()
                            
                            if len(parts) < 3:
                                error_msg = (
                                    "[B][C][FF0000]❌ ব্যবহার বিধি ভুল!\n"
                                    "[FFFFFF]সঠিক নিয়ম: /spam2 <uid> <মিনিট>\n"
                                    "উদাহরণ: /spam2 123456789 5"
                                )
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                duration_str = parts[2]
                                
                                # চেক করা হচ্ছে সময় ১ থেকে ৫ মিনিটের মধ্যে আছে কিনা
                                if not duration_str.isdigit() or not (1 <= int(duration_str) <= 5):
                                    error_msg = "[B][C][FF0000]❌ সময় অবশ্যই ১ থেকে ৫ মিনিটের মধ্যে হতে হবে!"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    duration = int(duration_str)
                                    wait_msg = f"[B][C][FFFF00]⏳ API এর সাথে কানেক্ট করা হচ্ছে..."
                                    await safe_send_message(response.Data.chat_type, wait_msg, uid, chat_id, key, iv)
                                    
                                    # ব্যাকগ্রাউন্ড টাস্ক যাতে মূল বট আটকে না যায়
                                    async def handle_api_spam(t_uid, dur, c_type, sender_uid, c_id, k, v):
                                        base_url = "https://47eea110-db88-49f9-8301-0ac10a62e1f4-00-2r2axu9x93sz6.pike.replit.dev"
                                        
                                        try:
                                            # ১. API তে স্টার্ট রিকোয়েস্ট পাঠানো
                                            start_url = f"{base_url}/spam?user_id={t_uid}&duration={dur}"
                                            async with aiohttp.ClientSession() as session:
                                                async with session.get(start_url) as res:
                                                    if res.status == 200:
                                                        start_msg = f"""[B][C][00FF00]✅ EXTERNAL SPAM STARTED!
[FFFFFF]──────────────────────
[B][00FFFF]🎯 টার্গেট: [FFFFFF]{t_uid}
[B][FFD700]⏱️ সময়: [FFFFFF]{dur} মিনিট
[FFFFFF]──────────────────────
[B][C][FF00FF]⚡ ঠিক {dur} মিনিট পর অটোমেটিক বন্ধ হয়ে যাবে!"""
                                                        await safe_send_message(c_type, start_msg, sender_uid, c_id, k, v)
                                                    else:
                                                        err_msg = f"[B][C][FF0000]❌ API Error! স্ট্যাটাস কোড: {res.status}"
                                                        await safe_send_message(c_type, err_msg, sender_uid, c_id, k, v)
                                                        return # API ফেইল করলে এখানেই থেমে যাবে
                                            
                                            # ২. ব্যাকগ্রাউন্ডে অপেক্ষা করা (মিনিট কে সেকেন্ডে রূপান্তর করে)
                                            # উদাহরণ: ৫ মিনিট = ৫ * ৬০ = ৩00 সেকেন্ড
                                            await asyncio.sleep(dur * 60)
                                            
                                            # ৩. সময় শেষ হলে অটোমেটিক স্টপ রিকোয়েস্ট পাঠানো
                                            stop_url = f"{base_url}/stop?user_id={t_uid}"
                                            async with aiohttp.ClientSession() as session:
                                                async with session.get(stop_url) as res:
                                                    stop_msg = f"""[B][C][00FFFF]🛑 AUTO STOP EXECUTED!
[FFFFFF]──────────────────────
[B][FFD700]🎯 টার্গেট: [FFFFFF]{t_uid}
[B][00FF00]✅ সময় শেষ! স্প্যাম সফলভাবে বন্ধ করা হয়েছে।
[FFFFFF]──────────────────────"""
                                                    await safe_send_message(c_type, stop_msg, sender_uid, c_id, k, v)
                                                    
                                        except Exception as e:
                                            err_msg = f"[B][C][FF0000]❌ API Connection Failed:\n{str(e)[:50]}"
                                            await safe_send_message(c_type, err_msg, sender_uid, c_id, k, v)

                                    # টাস্কটি চালু করে দেওয়া হলো
                                    asyncio.create_task(handle_api_spam(target_uid, duration, response.Data.chat_type, uid, chat_id, key, iv))
# ==================== API GHOST COMMAND ====================
                        if inPuTMsG.strip().startswith('/ghost '):
                            print('Processing API Ghost command')
                            
                            # maxsplit=2 দেওয়া হয়েছে যাতে নামের মাঝে স্পেস থাকলেও সমস্যা না হয়
                            parts = inPuTMsG.strip().split(maxsplit=2)
                            
                            if len(parts) < 3:
                                error_msg = (
                                    "[B][C][FF0000]❌ ব্যবহার বিধি ভুল!\n"
                                    "[FFFFFF]সঠিক নিয়ম: /ghost <TeamCode> <Name>\n"
                                    "উদাহরণ: /ghost ABC123 ARIYAN"
                                )
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                t_code = parts[1]
                                u_name_raw = parts[2].strip()
                                
                                # নামের মাঝে স্পেস থাকলে সেটাকে URL ফরম্যাটে (%20) কনভার্ট করার জন্য
                                import urllib.parse
                                u_name = urllib.parse.quote(u_name_raw)
                                
                                wait_msg = f"[B][C][FFFF00]⏳ API এর সাথে কানেক্ট করা হচ্ছে...\n[FFFFFF]Team: {t_code}\nName: {u_name_raw}"
                                await safe_send_message(response.Data.chat_type, wait_msg, uid, chat_id, key, iv)
                                
                                # ব্যাকগ্রাউন্ড টাস্ক যাতে মূল বট আটকে না যায়
                                async def handle_api_ghost(team_code, user_name, raw_name, c_type, sender_uid, c_id, k, v):
                                    api_url = f"https://rizerxghostbd.onrender.com/x/{team_code}/{user_name}"
                                    
                                    try:
                                        async with aiohttp.ClientSession() as session:
                                            async with session.get(api_url, timeout=15) as res:
                                                if res.status == 200:
                                                    success_msg = f"""[B][C][00FF00]✅ GHOST JOIN SUCCESSFUL!
[FFFFFF]──────────────────────
[B][00FFFF]🎯 Team Code: [FFFFFF]{team_code}
[B][FFD700]👤 Name: [FFFFFF]{raw_name}
[FFFFFF]──────────────────────
[B][C][FF00FF]⚡ API Request Completed!"""
                                                    await safe_send_message(c_type, success_msg, sender_uid, c_id, k, v)
                                                else:
                                                    err_msg = f"[B][C][FF0000]❌ API Error! স্ট্যাটাস কোড: {res.status}"
                                                    await safe_send_message(c_type, err_msg, sender_uid, c_id, k, v)
                                                    
                                    except Exception as e:
                                        err_msg = f"[B][C][FF0000]❌ API Connection Failed:\n{str(e)[:50]}"
                                        await safe_send_message(c_type, err_msg, sender_uid, c_id, k, v)

                                # টাস্কটি চালু করে দেওয়া হলো
                                asyncio.create_task(handle_api_ghost(t_code, u_name, u_name_raw, response.Data.chat_type, uid, chat_id, key, iv))

                        # ==================== LUCK METER COMMAND (BENGALI) ====================
                        if inPuTMsG.strip().lower() in ['/luk', '/luck']:
                            print('Processing /luk command')
                            
                            import random
                            
                            # ফ্রি ফায়ার থিম কালার কোড সহ লাক ডায়ালগ (সম্পূর্ণ বাংলায়, কোনো ইমোজি নেই)
                            luck_messages = [
                                "[00FF00]আজকে তোমার লাক ১০০% ! টানা ৩টা বুইয়া কনফার্ম !",
                                "[00FFFF]আজ এনিমি তোমার সামনে আসলেই ভয় পাবে ! তুমি হবা MVP !",
                                "[FFD700]তোমার ভাগ্য আজ দারুণ ! গ্র্যান্ডমাস্টার পুশ দেওয়ার সেরা দিন আজ !",
                                "[FF0000]সাবধান ! আজ ল্যান্ড করার আগেই লবিতে যাওয়ার চান্স আছে !",
                                "[FF4500]ভাই আজ গেম খেলিস না, বট এসেও তোকে মেরে চলে যাবে !",
                                "[FF1493]আজ তোমার ইন্টারনেট পিং ৯৯৯+ হওয়ার সম্ভাবনা অনেক বেশি !",
                                "[FFA500]আজকের দিনটা মোটামুটি, টিমমেটদের সাথে থাকলে বেঁচে যাবা, একা গেলে মরবা !",
                                "[00FFFF]পিছন থেকে থার্ড পার্টি খাওয়ার চান্স আছে, একটু সাবধানে খেলো !",
                                "[00FF00]আজকে তোমার হেডশট রেট হবে ৯৯% ! হ্যাকার লেভেলের গেমপ্লে হবে !",
                                "[FF0000]আজকে তোমার ভাগ্য অনেক খারাপ, ল্যান্ডমাইন ফুটে মরার চান্স আছে !",
                                "[FFD700]আজ তুমি এয়ারড্রপ লুট করতে গিয়ে AWM পাবা !",
                                "[00FF00]আজকে তোমার স্কোয়াডের সবচেয়ে বেশি কিল তোমারই হবে ! প্রো প্লেয়ার !"
                            ]
                            
                            todays_luck = random.choice(luck_messages)
                            
                            # প্রিমিয়াম ডিজাইন মেসেজ ফরমেট (বক্স স্টাইল, ইমোজি ছাড়া)
                            msg = (
                                "[B][C][00FFFF]╔════════════════════════╗\n"
                                "[B][C][FFD700]   ভাগ্য পরীক্ষা কেন্দ্র   \n"
                                "[B][C][00FFFF]╚════════════════════════╝\n"
                                f"[B][C]{todays_luck}\n"
                                "[B][C][FFFFFF]━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                                "[B][C][FF00FF]⚡ RAHATVIP BOT ⚡"
                            )

                            await safe_send_message(response.Data.chat_type, msg, uid, chat_id, key, iv)
                                # ==================== WINGMAN LOVE COMMAND (INSTANT EMOTE + INLINE COLORS) ====================
                        if inPuTMsG.strip().startswith('/love '):
                            print('Processing /love wingman command')
                            parts = inPuTMsG.strip().split(maxsplit=1)
                            
                            if len(parts) < 2:
                                error_msg = "[B][C][FF0000]>> ব্যবহার: /love <নাম> <<"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_name = parts[1].strip()
                                
                                # প্রথম মেসেজ (বট ইউজারের হয়ে বলছে) সাথে সাথেই দিয়ে দিবে
                                init_msg = f"[B][C][00FFFF]দোস্ত তুই শরমে পারছিস না, [FFFFFF]তোর হয়ে [FFFF00]আমিই বলে দিচ্ছি! ♡"
                                await safe_send_message(response.Data.chat_type, init_msg, uid, chat_id, key, iv)
                                
                                # ব্যাকগ্রাউন্ড টাস্ক
                                async def love_wingman_sequence(target_name, sender_uid, chat_id, chat_type, key, iv, region):
                                    
                                    # প্রথম ইন্ট্রো মেসেজটি দেওয়ার পর ঠিক ২ সেকেন্ড অপেক্ষা করবে
                                    await asyncio.sleep(2.0)
                                    
                                    # ৮টি মেসেজ (মাঝখানে মাঝখানে কালার দিয়ে সাজানো এবং শুধু হালকা লাভ ♡)
                                    quotes = [
                                        f"[B][C][FFFFFF]♡ [FF1493]{target_name} [FFFFFF]তুই আমার [00FFFF]সেফ জোন [FFFFFF]♡",
                                        f"[B][C][FFFFFF]♡ [00FF00]লবিতে [FFFFFF]শুধু [FFD700]তোকেই খুঁজি [FFFFFF]♡",
                                        
                                        f"[B][C][FFFFFF]♡ [00FFFF]এয়ারড্রপের [FFFFFF]চেয়েও [FF1493]তুই দামি [FFFFFF]♡",
                                        f"[B][C][FFFFFF]♡ [FFD700]তোর হাসিতে [FFFFFF]আমার [00FF00]HP বাড়ে [FFFFFF]♡",
                                        
                                        f"[B][C][FFFFFF]♡ [FF00FF]তুই ছাড়া [FFFFFF]গেম খেলা [00FFFF]পুরোই বৃথা [FFFFFF]♡",
                                        f"[B][C][FFFFFF]♡ [FFA500]স্নাইপারের [FFFFFF]একমাত্র [FF1493]লক্ষ্য তুই [FFFFFF]♡",
                                        
                                        f"[B][C][FFFFFF]♡ [32CD32]তুই আমার [FFFFFF]গ্লু-ওয়ালের [FFD700]কভার [FFFFFF]♡",
                                        f"[B][C][FFFFFF]♡ [FF0000]চল দুজনে [FFFFFF]মিলে [00FFFF]বুইয়া নিই [FFFFFF]♡"
                                    ]
                                    
                                    # আপনার দেওয়া ৪টি স্পেশাল ইমোট
                                    emotes = [
                                        909000010, # রোজ (Rose)
                                        909000045, # হার্ট (Heart)
                                        909038004, # আই লাভ ইউ (I Love You)
                                        909047007  # প্রপোজ/রোজ ২ (Propose)
                                    ]
                                    
                                    # মোট ৮ বার লুপ চলবে (প্রতিটি মেসেজের জন্য একবার করে)
                                    for i in range(8):
                                        # ১. প্রথমে মেসেজ সেন্ড করবে
                                        await safe_send_message(chat_type, quotes[i], sender_uid, chat_id, key, iv)
                                        
                                        # ২. মেসেজের সাথে সাথেই ইমোট মারবে (৪টি ইমোট রিপিট হবে i % 4 এর মাধ্যমে)
                                        try:
                                            current_emote = emotes[i % 4]
                                            emote_packet = await Emote_k(int(sender_uid), current_emote, key, iv, region)
                                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', emote_packet)
                                        except Exception as e:
                                            print(f"Error sending love emote: {e}")
                                            
                                        # ৩. পরবর্তী মেসেজ ও ইমোট দেওয়ার আগে ঠিক ৩ সেকেন্ড অপেক্ষা
                                        await asyncio.sleep(3.0)
                                        
                                # টাস্ক চালু করা হলো
                                asyncio.create_task(love_wingman_sequence(target_name, uid, chat_id, response.Data.chat_type, key, iv, region))
# ==================== V DANCE COMMAND ====================
                        global v_dance_task
                        
                        cmd_parts = inPuTMsG.strip().split()
                        
                        if len(cmd_parts) > 0 and cmd_parts[0].lower() == '/dance':
                            print('Processing /a dance command')
                            
                            # ১. অটোমেটিক যে কমান্ড দিয়েছে তার UID অ্যাড হয়ে যাবে
                            target_uids = [str(uid)]
                            
                            # ২. যদি স্পেস দিয়ে অন্য ইউজারদের UID দেয়, সেগুলো অ্যাড হবে (সর্বোচ্চ ৪ জন এক্সট্রা)
                            for p in cmd_parts[1:5]:
                                if p.isdigit():
                                    target_uids.append(p)
                            
                            # আগের ডান্স চললে সেটা বন্ধ করে দিবে
                            if v_dance_task and not v_dance_task.done():
                                v_dance_task.cancel()
                                
                            # প্রথম মেসেজ
                            init_msg = f"[B][C][00FFFF]🔥 ＶＩＰ ＤＡＮＣＥ ＳＴＡＲＴＥＤ 🔥\n[FFFFFF]প্লেয়ার: {len(target_uids)} জন\nইমোট: ৮টি (৮ সেকেন্ড পর পর)\n[FF0000]থামাতে লিখুন: /as"
                            await safe_send_message(response.Data.chat_type, init_msg, uid, chat_id, key, iv)
                            
                            # ব্যাকগ্রাউন্ড টাস্ক
                            async def v_dance_sequence(uids_list, sender_uid, chat_id, chat_type, key, iv, region):
                                try:
                                    # কমান্ড দেওয়ার সাথে সাথেই ইমোট শুরু হবে (ডিলে বাদ দেওয়া হয়েছে)
                                    
                                    # ⬇️ এখানে আপনার পছন্দের ৮টি ইমোট আইডি বসিয়ে নিবেন ⬇️
                                    emotes = [
                                        909000137, # 1. Emote
                                        909041014, # 2. Emote
                                        909038004, # 3. Emote
                                        909037009, # 4. Emote
                                        909035006, # 5. Emote
                                        909000135, # 6. Emote
                                        909042001, # 7. Emote
                                        909040005  # 8. Emote
                                    ]
                                    
                                    # ৮টি ইমোটের জন্য লুপ
                                    for i in range(8):
                                        current_emote = emotes[i]
                                        
                                        # লিস্টে থাকা সব প্লেয়ারকে (নিজের সহ) একসাথে ইমোট মারবে
                                        for t_uid in uids_list:
                                            try:
                                                emote_packet = await Emote_k(int(t_uid), current_emote, key, iv, region)
                                                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', emote_packet)
                                            except Exception as e:
                                                print(f"Error sending V-Dance emote to {t_uid}: {e}")
                                        
                                        # ৮ নাম্বার ইমোটের পর আর ওয়েট করার দরকার নেই
                                        if i < 7:
                                            await asyncio.sleep(8.0) # ঠিক ৮ সেকেন্ড অপেক্ষা করবে
                                            
                                    # সব শেষ হলে মেসেজ
                                    finish_msg = "[B][C][00FF00]✅ VIP DANCE COMPLETED! 🕺"
                                    await safe_send_message(chat_type, finish_msg, sender_uid, chat_id, key, iv)
                                    
                                except asyncio.CancelledError:
                                    # স্টপ করা হলে এই মেসেজ দিবে
                                    stop_msg = "[B][C][FF0000]🛑 VIP DANCE মাঝপথে থামানো হয়েছে!"
                                    await safe_send_message(chat_type, stop_msg, sender_uid, chat_id, key, iv)
                                    
                            # টাস্ক চালু করা হলো এবং ভেরিয়েবলে সেভ করা হলো
                            v_dance_task = asyncio.create_task(v_dance_sequence(target_uids, uid, chat_id, response.Data.chat_type, key, iv, region))

                        # ==================== V DANCE STOP COMMAND ====================
                        if inPuTMsG.strip().lower() == '/as':
                            if v_dance_task and not v_dance_task.done():
                                v_dance_task.cancel()  # টাস্ক ক্যানসেল করবে
                            else:
                                error_msg = "[B][C][FF0000]❌ কোনো V-Dance চালু নেই!"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
# ==================== SQUAD ROLE COMMAND ====================
                        if inPuTMsG.strip().startswith('/role '):
                            print('Processing /role command')
                            parts = inPuTMsG.strip().split(maxsplit=1)
                            
                            if len(parts) < 2:
                                error_msg = "[B][C][FF0000]❌ ব্যবহার: /role <নাম>\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_name = parts[1].strip()
                                import random
                                
                                roles = [
                                    {"title": "[FF0000]🔥 The Rusher", "desc": "এনিমি দেখলেই সবার আগে দৌড় দেয়, আর সবার আগে মরে ব্যাক করে!"},
                                    {"title": "[00FFFF]🦅 The Sniper King", "desc": "১৫০ মিটার দূর থেকে AWM দিয়ে হেডশট মারে, রিয়েল প্রো!"},
                                    {"title": "[32CD32]🩹 The Medic / Reviver", "desc": "সারাজীবন শুধু টিমমেটদের রিভাইভ দেয় আর মেডিকেট বিলায়!"},
                                    {"title": "[FFFF00]🏃 The Loot Stealer", "desc": "এনিমি মারবে অন্য কেউ, কিন্তু সবার আগে বক্সে গিয়ে লুট করবে সে!"},
                                    {"title": "[FFA500]⛺ The Camper", "desc": "লুকিয়ে লুকিয়ে র‍্যাংক পুশ দেওয়াই যার জীবনের মূল লক্ষ্য!"},
                                    {"title": "[FF00FF]🛡️ The Gloo-Wall Master", "desc": "গুলি করার চেয়ে গ্লু-ওয়াল বেশি মারে! কভার দিতে ওস্তাদ!"}
                                ]
                                
                                selected_role = random.choice(roles)
                                
                                role_msg = (
                                    f"[B][C][00BFFF]🎮 S Q U A D   R O L E 🎮\n"
                                    f"──────────────────────\n"
                                    f"[FFFFFF]👤 Player: [00FF00]{target_name}\n"
                                    f"[FFFFFF]🎖️ Role: {selected_role['title']}\n"
                                    f"[FFFFFF]📝 Bio: [FFFF00]{selected_role['desc']}\n"
                                    f"[B][C][00BFFF]──────────────────────"
                                )
                                await safe_send_message(response.Data.chat_type, role_msg, uid, chat_id, key, iv)
# ==================== DHADHA (RIDDLE) COMMAND ====================
                        if inPuTMsG.strip() == '/dhadha':
                            print('Processing /dhadha command')
                            
                            import random
                            riddles = [
                                {"q": "গেমে ঢোকার আগে সবাই আমাকে খোঁজে, কিন্তু এনিমি সামনে আসলে সবাই আমাকে গালি দেয়! আমি কে?", "a": "পিং বা ইন্টারনেট কানেকশন! 📶"},
                                {"q": "কখনো আমি লাল, কখনো আমি নীল, আমার ভেতরে গেলেই তোমার শরীর হবে ঢিল! আমি কে?", "a": "সেফ জোন (Zone)! 🔴"},
                                {"q": "দেখতে আমি ছোট, কিন্তু আমার পেটে অনেক লুট! আমাকে দেখলে সবাই দৌড়ে আসে। আমি কে?", "a": "এয়ারড্রপ (Airdrop)! 🎁"},
                                {"q": "সবাই আমাকে মারতে চায়, কিন্তু আমি মরে গেলে সবাই খুশি হয়। আমি কে?", "a": "লবির এনিমি বা বট! 🤖"},
                                {"q": "আমার চোখ নেই কিন্তু আমি দেখি, আমার পা নেই কিন্তু আমি ঘুরি। আমার কাজ শুধু তোমার ভুল ধরা! আমি কে?", "a": "অবজারভারে থাকা টিমমেট! 👁️"},
                                {"q": "হাত নেই, পা নেই, তবুও সে গ্রেনেড ছুড়তে পারে। বলতো সে কে?", "a": "ফ্রি ফায়ারের হ্যাকার! 💀"}
                            ]
                            
                            chosen_riddle = random.choice(riddles)
                            
                            # প্রথমে ধাঁধা জিজ্ঞেস করবে
                            q_msg = (
                                f"[B][C][00FFFF]🤔 ম জ দি মা গ  ধাঁ ধা 🤔\n"
                                f"[FFFFFF]────────────────────\n"
                                f"[FFFF00]প্রশ্ন: [FFFFFF]{chosen_riddle['q']}\n"
                                f"[FFFFFF]────────────────────\n"
                                f"[B][C][FF4500]⏳ ৫ সেকেন্ড পর উত্তর আসছে... সবাই ভাবো!"
                            )
                            await safe_send_message(response.Data.chat_type, q_msg, uid, chat_id, key, iv)
                            
                            # ৫ সেকেন্ড পর উত্তর দেওয়ার ব্যাকগ্রাউন্ড টাস্ক
                            async def send_answer(c_type, ans, t_uid, c_id, k, v):
                                await asyncio.sleep(5) # ৫ সেকেন্ড অপেক্ষা
                                a_msg = (
                                    f"[B][C][32CD32]💡 ধাঁধার উত্তর! 💡\n"
                                    f"[FFFFFF]────────────────────\n"
                                    f"[00FF00]উত্তর: [FFFFFF]{ans}\n"
                                    f"[FFFFFF]────────────────────\n"
                                    f"[B][C][00FFFF]কয়জন পেরেছো সত্যি করে বলো! 🤣"
                                )
                                await safe_send_message(c_type, a_msg, t_uid, c_id, k, v)
                                
                            # টাস্কটি চালু করে দেওয়া হলো
                            asyncio.create_task(send_answer(response.Data.chat_type, chosen_riddle['a'], uid, chat_id, key, iv))
# ==================== FF JOKES COMMAND ====================
                        if inPuTMsG.strip() == '/joke':
                            print('Processing /joke command')
                            
                            import random
                            jokes = [
                                "[FF0000]শিক্ষক:[FFFFFF] বলতো, পৃথিবীর সবচেয়ে দ্রুতগামী জিনিস কী?\n[00FFFF]ছাত্র:[FFFFFF] স্যার, ফ্রি ফায়ারে এনিমির হাতে মাইর খাওয়ার পর টিমমেটদের লুট বক্স চুরি করার স্পিড! 🏃‍♂️💨",
                                "[FF0000]প্রেমিকা:[FFFFFF] তুমি আমাকে কতটা ভালোবাসো?\n[00FFFF]প্রেমিক:[FFFFFF] কাস্টম খেলার সময় তোমাকে জেতানোর জন্য আমি ইচ্ছা করে হেরে যাই!\n[FF0000]প্রেমিকা:[FFFFFF] ওলে বাবা! তাই?\n[00FFFF]প্রেমিক:[FFFFFF] আরে ধুর! আমি তো আসলে বট, এমনিতেই হেরে যাই! 🤡",
                                "[FF0000]এক নুব প্রো প্লেয়ারকে বলছে:[FFFFFF] ভাই, আমাকে একটু খেলা শেখাবি?\n[00FFFF]প্রো প্লেয়ার:[FFFFFF] আগে বল, এনিমি দেখলে তুই কী করিস?\n[FF0000]নুব:[FFFFFF] আমি তো গ্লু-ওয়াল ভেবে নেট অফ করে দিই! 🤣",
                                "[FF0000]ডাক্তার:[FFFFFF] আপনার ছেলের তো পালস পাওয়া যাচ্ছে না!\n[00FFFF]বাবা:[FFFFFF] ওর পালস চেক করে লাভ নেই ডাক্তার সাহেব, ওর পিং (Ping) চেক করুন, নির্ঘাত ৯৯৯+ হয়ে আছে! 📡",
                                "[00FF00]জীবনে এমন কাউকে ভালোবাসো...[FFFFFF]\nযে রিভাইভ দেওয়ার সময় নিজের লাস্ট গ্লু-ওয়ালটাও তোমাকে দিয়ে দেবে! 🥲\n(যদিও ফ্রি ফায়ারে এমন মানুষ শুধু রূপকথায় পাওয়া যায়!)",
                                "[FF0000]বাবা:[FFFFFF] কিরে সারাদিন মোবাইল টিপিস, একটু বই পড়!\n[00FFFF]ছেলে:[FFFFFF] বাবা আমি তো বই-ই পড়ি।\n[FF0000]বাবা:[FFFFFF] কী বই?\n[00FFFF]ছেলে:[FFFFFF] 'কীভাবে গ্র্যান্ডমাস্টার যাওয়া যায়' গাইড বই! 📘🤣"
                            ]
                            
                            joke_msg = (
                                f"[B][C][FFD700]😂 জোকস অফ দ্য ডে 😂\n"
                                f"[FFFFFF]────────────────────\n"
                                f"{random.choice(jokes)}\n"
                                f"[FFFFFF]────────────────────\n"
                                f"[B][C][FF00FF]হাসতে হাসতে পেট ব্যথা গ্যারান্টি! 🤣"
                            )
                            await safe_send_message(response.Data.chat_type, joke_msg, uid, chat_id, key, iv)
# ==================== MATCH / LOVE CALCULATOR ====================
                        if inPuTMsG.strip().startswith('/match '):
                            print('Processing /match command')
                            parts = inPuTMsG.strip().split(maxsplit=2)
                            
                            if len(parts) < 3:
                                error_msg = (
                                    "[B][C][FF0000]❌ ERROR! ব্যবহারের নিয়ম:\n"
                                    "[FFFFFF]/match <প্রথম_নাম> <দ্বিতীয়_নাম>\n"
                                    "উদাহরণ: /match RAHATBot\n"
                                )
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                name1 = parts[1].upper()
                                name2 = parts[2].upper()
                                
                                import random
                                percent = random.randint(0, 100)
                                
                                if percent <= 20:
                                    status = "[FF0000]কট্টর শত্রু! 💣"
                                    comment = "তোরা ভাই গেমে একসাথে নামলে একে অপরকে গ্রেনেড মারবি কনফার্ম! দূরে থাক!"
                                elif percent <= 40:
                                    status = "[FFA500]ফেক ফ্রেন্ড! 🐍"
                                    comment = "সামনে ভাই ভাই, পিছনে এনিমি! সুযোগ পেলেই তোর লুট চুরি করে পালাবে!"
                                elif percent <= 70:
                                    status = "[FFFF00]বেস্ট ফ্রেন্ড! 🤝"
                                    comment = "তোদের বন্ধুত্ব অস্থির! একসাথে রাশ দিলে পুরো স্কোয়াড শেষ করে দিবি!"
                                elif percent <= 90:
                                    status = "[00FFFF]গভীর প্রেম! 👩‍❤️‍👨"
                                    comment = "ভাই তোদের তো বিয়ে দেওয়া উচিত! গেমে এসে শুধু রোমান্স চলে!"
                                else:
                                    status = "[00FF00]লাইলা-মজনু! ❤️"
                                    comment = "স্বর্গে তৈরি হওয়া জুটি! রিভাইভ দিতে গিয়ে জোন ড্যামেজে মরে যাবে তাও সাথ ছাড়বে না!"

                                match_msg = f"""[B][C][FF1493]💖 ＲＥＬＡＴＩＯＮ  ＴＥＳＴ 💖
[FFFFFF]──────────────────────
[B][00FFFF] {name1} [FFFFFF]✖️ [00FFFF]{name2}
[FFFFFF]──────────────────────
[B][FFD700]মিল পাওয়া গেছে: [FFFFFF]{percent}%
[B][FFD700]সম্পর্ক: {status}
[FFFFFF]──────────────────────
[B][C][FFFFFF]{comment}
"""
                                await safe_send_message(response.Data.chat_type, match_msg, uid, chat_id, key, iv)

                        # ==================== LUCKY SPIN COMMAND ====================
                        if inPuTMsG.strip().startswith('/spin'):
                            print('Processing /spin command')
                            
                            wait_msg = "[B][C][00FFFF]🎰 ভাগ্য চাকা ঘুরছে... দয়া করে অপেক্ষা করুন! 🌪️\n"
                            await safe_send_message(response.Data.chat_type, wait_msg, uid, chat_id, key, iv)
                            
                            # ব্যাকগ্রাউন্ড টাস্ক ফাংশন (যাতে বট ফ্রিজ না হয়)
                            async def send_spin_result(c_type, t_uid, c_id, k, v):
                                await asyncio.sleep(2) # ২ সেকেন্ড ওয়েট করবে
                                
                                spin_outcomes = [
                                    "[00FF00]🎁 ১০,০০০ ডায়মন্ড! [FFFFFF](তবে স্বপ্নে পেয়েছিস, ঘুম ভাঙলে আর নাই!) 🤣",
                                    "[FF0000]💩 ১টা গোল্ড কয়েন! [FFFFFF]গরিবের কপাল এমনই হয়! 🪙",
                                    "[00FFFF]🔥 ইভো গান ম্যাক্স! [FFFFFF](আজকের ম্যাচে তুই হ্যাকার লেভেলের প্রো!) 🔫",
                                    "[FF4500]💀 আইডি ব্যান! [FFFFFF](বেশি হ্যাক ইউজ করলে এমনই হয়, গেম থেকে বিদায়!) 🚫",
                                    "[FFFF00]🤡 আদম ক্যারেক্টার! [FFFFFF](তোর আসল রূপ এটাই ভাই, মেনে নে!) 🧍‍♂️",
                                    "[FFD700]👑 ভি-ব্যাজ (V-Badge)! [FFFFFF](গ্যারিনা ভুলে তোকে ইউটিউবার ভেবে দিয়ে দিছে!) ✅",
                                    "[FF1493]💔 ছ্যাঁকা! [FFFFFF](গেমে স্পিন না করে সিঙ্গেল জীবনে ফোকাস কর ভাই!) 😭",
                                    "[32CD32]🎒 আনলিমিটেড গ্লু-ওয়াল! [FFFFFF](আজ শুধু প্যাক করে বসে থাকবি, রাশ করবি না!) 🛡️",
                                    "[FFA500]🍗 ফ্রি বুইয়া! [FFFFFF](লবিতে এনিমি সব বট পড়ছে, আজ তোরই দিন!) 🏆"
                                ]
                                
                                import random
                                result = random.choice(spin_outcomes)
                                
                                spin_msg = f"""[B][C][FFD700]🎰 ＬＵＣＫＹ  ＳＰＩＮ 🎰
[FFFFFF]──────────────────────
[B][C][FFFFFF]তোর ভাগ্যে যা উঠলো:
[B][C]{result}
[FFFFFF]──────────────────────
[B][C][00FFFF]⚡ Powered by RAHATVIP
"""
                                await safe_send_message(c_type, spin_msg, t_uid, c_id, k, v)

                            # টাস্কটি ব্যাকগ্রাউন্ডে রান করিয়ে দেওয়া হলো
                            asyncio.create_task(send_spin_result(response.Data.chat_type, uid, chat_id, key, iv))
                            #bio
                        if inPuTMsG.strip().startswith('/bio '):
                            print('Processing bio command in any chat type')

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /bio <uid>\nExample: /bio 4368569733\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                initial_message = f"[B][C]{get_random_color()}\nFetching the player bio...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)

                                # Use ThreadPoolExecutor to avoid blocking the async loop
                                loop = asyncio.get_event_loop()
                                with ThreadPoolExecutor() as executor:
                                    bio_result = await loop.run_in_executor(executor, get_player_bio, target_uid)

                                await safe_send_message(response.Data.chat_type, f"[B][C]{get_random_color()}\n{bio_result}", uid, chat_id, key, iv)

                        # QUICK EMOTE ATTACK COMMAND - /quick [team_code] [emote_id] [target_uid?]
                        if inPuTMsG.strip().startswith('/quick'):
                            print('Processing quick emote attack command')
    
                            parts = inPuTMsG.strip().split()
    
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /quick (team_code) [emote_id] [target_uid]\n\n[FFFFFF]Examples:\n[00FF00]/quick ABC123[FFFFFF] - Join, send Rings emote, leave\n[00FF00]/ghostquick ABC123[FFFFFF] - Ghost join, send emote, leave\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                team_code = parts[1]
        
                                # Set default values
                                emote_id = parts[0]
                                target_uid = str(response.Data.uid)  # Default: Sender's UID
        
                                # Parse optional parameters
                                if len(parts) >= 3:
                                    emote_id = parts[2]
                                if len(parts) >= 4:
                                    target_uid = parts[3]
        
                                # Determine target name for message
                                if target_uid == str(response.Data.uid):
                                    target_name = "Yourself"
                                else:
                                    target_name = f"UID {target_uid}"
        
                                initial_message = f"[B][C][FFFF00]⚡ QUICK EMOTE ATTACK!\n\n[FFFFFF]🎯 Team: [00FF00]{team_code}\n[FFFFFF]🎭 Emote: [00FF00]{emote_id}\n[FFFFFF]👤 Target: [00FF00]{target_name}\n[FFFFFF]⏱️ Estimated: [00FF00]2 seconds\n\n[FFFF00]Executing sequence...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
        
                                try:
                                    # Try regular method first
                                    success, result = await ultra_quick_emote_attack(team_code, emote_id, target_uid, key, iv, region)
            
                                    if success:
                                        success_message = f"[B][C][00FF00]✅ QUICK ATTACK SUCCESS!\n\n[FFFFFF]🏷️ Team: [00FF00]{team_code}\n[FFFFFF]🎭 Emote: [00FF00]{emote_id}\n[FFFFFF]👤 Target: [00FF00]{target_name}\n\n[00FF00]Bot joined → emoted → left! ✅\n"
                                    else:
                                        success_message = f"[B][C][FF0000]❌ Regular attack failed: {result}\n"
                                    
                                    await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
            
                                except Exception as e:
                                    print("failed")
            
            
                        # Invite Command - /inv (creates 5-player group and sends request)
                        if inPuTMsG.strip().startswith('/inv '):
                            print('Processing invite command in any chat type')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /inv (uid)\nExample: /inv 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                initial_message = f"[B][C]{get_random_color()}\nCreating 5-Player Group and sending request to {target_uid}...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                                
                                try:
                                    # Fast squad creation and invite for 5 players
                                    PAc = await OpEnSq(key, iv, region)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', PAc)
                                    await asyncio.sleep(0.3)
                                    
                                    C = await cHSq(5, int(target_uid), key, iv, region)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', C)
                                    await asyncio.sleep(0.3)
                                    
                                    V = await SEnd_InV(5, int(target_uid), key, iv, region)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', V)
                                    await asyncio.sleep(0.3)
                                    
                                    E = await ExiT(None, key, iv)
                                    await asyncio.sleep(2)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', E)
                                    
                                    # SUCCESS MESSAGE
                                    success_message = f"[B][C][00FF00]✅ SUCCESS! 5-Player Group invitation sent successfully to {target_uid}!\n"
                                    await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
                                    
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ ERROR sending invite: {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        if inPuTMsG.startswith(("/6")):
                            # Process /6 command - Create 4 player group
                            initial_message = f"[B][C]{get_random_color()}\n\nCreating 6-Player Group...\n\n"
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                            
                            # Fast squad creation and invite for 4 players
                            PAc = await OpEnSq(key, iv, region)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', PAc)
                            
                            C = await cHSq(6, uid, key, iv, region)
                            await asyncio.sleep(0.3)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', C)
                            
                            V = await SEnd_InV(6, uid, key, iv, region)
                            await asyncio.sleep(0.3)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', V)
                            
                            E = await ExiT(None, key, iv)
                            await asyncio.sleep(3.5)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', E)
                            
                            # SUCCESS MESSAGE
                            success_message = f"[B][C][00FF00]✅ SUCCESS! 6-Player Group invitation sent successfully to {uid}!\n"
                            await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)

                        if inPuTMsG.startswith(("/3")):
                            # Process /3 command - Create 3 player group
                            initial_message = f"[B][C]{get_random_color()}\n\nCreating 3-Player Group...\n\n"
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                            
                            # Fast squad creation and invite for 6 players
                            PAc = await OpEnSq(key, iv, region)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', PAc)
                            
                            C = await cHSq(3, uid, key, iv, region)
                            await asyncio.sleep(0.3)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', C)
                            
                            V = await SEnd_InV(3, uid, key, iv, region)
                            await asyncio.sleep(0.3)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', V)
                            
                            E = await ExiT(None, key, iv)
                            await asyncio.sleep(3.5)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', E)
                            
                            # SUCCESS MESSAGE
                            success_message = f"[B][C][00FF00]✅ SUCCESS! 6-Player Group invitation sent successfully to {uid}!\n"
                            await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)

#GET PLAYER INFO
                        if inPuTMsG.strip().startswith('/info'):
                            print('Processing bio command in any chat type')

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /info <uid>\nExample: /info 436🤫856🤫97🤫33\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                initial_message = f"[B][C]{get_random_color()}\nGetting Player Info...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)

                                info_data = get_player_info(target_uid)

                                await send_full_player_info(info_data, response.Data.chat_type, uid, chat_id, key, iv)

                        if inPuTMsG.strip().startswith('/roommsg'):
                            print('Processing room message command')
    
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]❌ Usage: /roommsg (room_id) (message)\nExample: /roommsg 489775386 Hello room!\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                room_id = parts[1]
                                message = " ".join(parts[2:])
        
                                initial_msg = f"[B][C][00FF00]📢 Sending to room {room_id}: {message}\n"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
        
                                try:
                                    # Get bot UID
                                    bot_uid = LoGinDaTaUncRypTinG.AccountUID if hasattr(LoGinDaTaUncRypTinG, 'AccountUID') else 13793280064
            
                                    # Send room chat using leaked packet structure
                                    room_chat_packet = await send_room_chat_enhanced(message, room_id, key, iv, region)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', room_chat_packet)
            
                                    success_msg = f"[B][C][00FF00]✅ Message sent to room {room_id}!\n"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                    print(f"✅ Room message sent to {room_id}: {message}")
            
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ Failed: {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        # Replace the existing title handler with this
                        # Use the FINAL version
                        if inPuTMsG.strip().startswith('/kick'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /kick (uid)\nExample: /kick 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                initial_message = f"[B][C]{get_random_color()}\nkicking {xMsGFixinG(target_uid)}...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                                
                                try:
                                    # Fast squad creation and invite for 5 players
                                    PAc = await KickTarget(target_uid, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', PAc)
                                    await asyncio.sleep(0.3)
                                except Exception as e:
                                    print(e)

                        if inPuTMsG.strip().startswith(('/add ', '/remove ', '/friends')):

                            parts = inPuTMsG.strip().split()

                            if not Uid or not Pw:
                                await safe_send_message(
                                    response.Data.chat_type,
                                    "❌ Error: Bot UID/Pass not loaded!",
                                    uid,
                                    chat_id,
                                    key,
                                    iv
                                )
                                continue

                            cmd = parts[0].lower()

                            # ==========================
                            # /friends (no uid needed)
                            # ==========================
                            if cmd == "/friends":

                                wait_msg = (
                                    "[C][B][5DA9FF]━━━━━━━━━━━━━\n"
                                    "[C][FF6EC7]FRIEND MANAGER\n"
                                    "[C][E6E6FA]Fetching friend list...\n"
                                    "[C][5DA9FF]━━━━━━━━━━━━━"
                                )

                                await safe_send_message(
                                    response.Data.chat_type,
                                    wait_msg,
                                    uid,
                                    chat_id,
                                    key,
                                    iv
                                )

                                # Game-style friend list
                                result = get_friends_list_game_style(Uid, Pw)

                                await safe_send_message(
                                    response.Data.chat_type,
                                    result,
                                    uid,
                                    chat_id,
                                    key,
                                    iv
                                )

                            # ==========================
                            # /add & /remove
                            # ==========================
                            else:

                                if len(parts) < 2:
                                    error_msg = (
                                        "[C][B][FF5C8A]USAGE ERROR\n"
                                        "[C][E6E6FA]/add <uid>\n"
                                        "[C][E6E6FA]/remove <uid>\n"
                                        "[C][E6E6FA]/friends"
                                    )
                                    await safe_send_message(
                                        response.Data.chat_type,
                                        error_msg,
                                        uid,
                                        chat_id,
                                        key,
                                        iv
                                    )
                                    return

                                target_uid = parts[1]

                                wait_msg = (
                                    "[C][B][5DA9FF]━━━━━━━━━━━━━\n"
                                    "[C][FF6EC7]FRIEND MANAGER\n"
                                    "[C][E6E6FA]Processing request...\n"
                                    "[C][5DA9FF]━━━━━━━━━━━━━"
                                )

                                await safe_send_message(
                                    response.Data.chat_type,
                                    wait_msg,
                                    uid,
                                    chat_id,
                                    key,
                                    iv
                                )

                                if cmd == "/add":
                                    result = add_friend(Uid, Pw, target_uid)

                                elif cmd == "/remove":
                                    result = remove_friend(Uid, Pw, target_uid)

                                else:
                                    result = "[C][B][FF5C8A]UNKNOWN COMMAND"

                                await safe_send_message(
                                    response.Data.chat_type,
                                    result,
                                    uid,
                                    chat_id,
                                    key,
                                    iv
                                )

                        if inPuTMsG.startswith(("/5")):
                            # Process /5 command in any chat type
                            initial_message = f"[B][C]{get_random_color()}\n\nSending Group Invitation...\n\n"
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                            
                            # Fast squad creation and invite
                            PAc = await OpEnSq(key, iv, region)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', PAc)
                            
                            C = await cHSq(5, uid, key, iv, region)
                            await asyncio.sleep(0.3)  # Reduced delay
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', C)
                            
                            V = await SEnd_InV(5, uid, key, iv, region)
                            await asyncio.sleep(0.3)  # Reduced delay
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', V)
                            
                            E = await ExiT(None, key, iv)
                            await asyncio.sleep(3.5)  # Reduced from 3 seconds
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', E)
                            
                            # SUCCESS MESSAGE
                            success_message = f"[B][C][00FF00]✅ SUCCESS! Group invitation sent successfully to {uid}!\n"
                            await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)

                        if inPuTMsG.strip() == "/admin":
                            # Process /admin command in any chat type
                            admin_message = """
[C][B][FF0000]╔══════════╗
[FFFFFF]✨ folow on tiktok   
[FFFFFF]          ⚡ RAHAT❤️  
[FFFFFF]                   thank for support 
[FF0000]╠══════════╣
[FFD700]⚡ OWNER : [FFFFFF]RAHAT   
[FFD700]✨ Name on tiktok : [FFFFFF] ARIYAN__222 ❤️  
[FF0000]╚══════════╝
[FFD700]✨ Developer —͟͞͞ </> RAHAT❄️  ⚡
"""
                            await safe_send_message(response.Data.chat_type, admin_message, uid, chat_id, key, iv)

                        # Add this with your other command handlers in the TcPChaT function
                        if inPuTMsG.strip().startswith('/multijoin'):
                            print('Processing multi-account join request')
    
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ Usage: /multijoin (target_uid)\nExample: /multijoin 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
        
                                if not target_uid.isdigit():
                                    error_msg = f"[B][C][FF0000]❌ Please write a valid player ID!\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    return
        
                                initial_msg = f"[B][C][00FF00]🚀 Starting multi-join attack on {target_uid}...\n"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
        
                                try:
                                    # Try the fake multi-account method (more reliable)
                                    success_count, total_attempts = await real_multi_account_join(target_uid, key, iv, region)
            
                                    if success_count > 0:
                                        result_msg = f"""
[B][C][00FF00]✅ MULTI-JOIN ATTACK COMPLETED!

🎯 Target: {target_uid}
✅ Successful Requests: {success_count}
📊 Total Attempts: {total_attempts}
⚡ Different squad variations sent!

💡 Check your game for join requests!
"""
                                    else:
                                        result_msg = f"[B][C][FF0000]❌ All join requests failed! Check bot connection.\n"
            
                                    await safe_send_message(response.Data.chat_type, result_msg, uid, chat_id, key, iv)
            
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ Multi-join error: {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

           
                        if inPuTMsG.strip().startswith('/fastmultijoin'):
                            print('Processing fast multi-account join spam')
    
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /fastmultijoin (uid)\nExample: /fastmultijoin 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
        
                                # Load accounts
                                accounts_data = load_accounts()
                                if not accounts_data:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! No accounts found!\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    return
                                
                                initial_msg = f"[B][C][00FF00]⚡ FAST MULTI-ACCOUNT JOIN SPAM!\n🎯 Target: {target_uid}\n👥 Accounts: {len(accounts_data)}\n"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
        
                                try:
                                    join_count = 0
                                    # Send join requests rapidly from all accounts
                                    for uid, password in accounts_data.items():
                                        try:
                                            # Use your existing join request function
                                            join_packet = await SEnd_InV(5, int(target_uid), key, iv, region)
                                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
                                            join_count += 1
                                            print(f"✅ Fast join from account {uid}")
                    
                                            # Very short delay
                                            await asyncio.sleep(0.1)
                    
                                        except Exception as e:
                                            print(f"❌ Fast join failed for {uid}: {e}")
                                            continue
            
                                    success_msg = f"[B][C][00FF00]✅ FAST MULTI-JOIN COMPLETED!\n🎯 Target: {target_uid}\n✅ Successful: {join_count}/{len(accounts_data)}\n⚡ Speed: Ultra fast\n"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
            
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ ERROR in fast multi-join: {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
           

                        # Update the command handler
                        if inPuTMsG.strip().startswith('/reject'):
                            print('Processing reject spam command in any chat type')
    
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /reject (target_uid)\nExample: /reject 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
        
                                # Stop any existing reject spam
                                if reject_spam_task and not reject_spam_task.done():
                                    reject_spam_running = False
                                    reject_spam_task.cancel()
                                    await asyncio.sleep(0.5)
        
                                # Send start message
                                start_msg = f"[B][C][1E90FF]🌀 Started Reject Spam on: {target_uid}\n🌀 Packets: 150 each type\n🌀 Interval: 0.2 seconds\n"
                                await safe_send_message(response.Data.chat_type, start_msg, uid, chat_id, key, iv)
        
                                # Start reject spam in background
                                reject_spam_running = True
                                reject_spam_task = asyncio.create_task(reject_spam_loop(target_uid, key, iv))
        
                                # Wait for completion in background and send completion message
                                asyncio.create_task(handle_reject_completion(reject_spam_task, target_uid, uid, chat_id, response.Data.chat_type, key, iv))


                        if inPuTMsG.strip() == '/reject_stop':
                            if reject_spam_task and not reject_spam_task.done():
                                reject_spam_running = False
                                reject_spam_task.cancel()
                                stop_msg = f"[B][C][00FF00]✅ Reject spam stopped successfully!\n"
                                await safe_send_message(response.Data.chat_type, stop_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]❌ No active reject spam to stop!\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                
                                                    
                                                                        
                        # In your command handler where you call Room_Spam:
                        if inPuTMsG.strip().startswith('/room'):
                            print('Processing advanced room spam command')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /room (uid)\nExample: /room 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                room_id = parts[2]
        
                                if not target_uid.isdigit():
                                    error_msg = f"[B][C][FF0000]❌ ERROR! Please write a valid player ID!\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    return
        
                                # Send initial message
                                initial_msg = f"[B][C][00FF00]🔍 Working on room spam for {target_uid}...\n"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
                                
                                try:
                                    # Method 1: Try to get room ID from recent packets
                                
                                    

                                    room_msg = f"[B][C][00FF00]🎯 Detected player in room {room_id}\n"
                                    await safe_send_message(response.Data.chat_type, room_msg, uid, chat_id, key, iv)
            
                                    # Create spam packet
                                    spam_packet = await Room_Spam(target_uid, room_id, "ARIYAN", key, iv)
            
                                    # Send 99 spam packets rapidly (like your other TCP)
                                    spam_count = 500
                                    
                                    start_msg = f"[B][C][00FF00]🚀 Starting spam: {spam_count} packets to room {room_id}\n"
                                    await safe_send_message(response.Data.chat_type, start_msg, uid, chat_id, key, iv)
            
                                    for i in range(spam_count):
                                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', spam_packet)
                
                                        # Progress updates
                                        if (i + 1) % 25 == 0:
                                            progress_msg = f"[B][C][00FF00]📦 Progress: {i+1}/{spam_count} packets sent\n"
                                            await safe_send_message(response.Data.chat_type, progress_msg, uid, chat_id, key, iv)
                                            print(f"Room spam progress: {i+1}/{spam_count} to UID: {target_uid}")
                
                                        # Very short delay (0.05 seconds = 50ms)
                                        await asyncio.sleep(0.05)
            
                                    # Final success message
                                    success_msg = f"[B][C][00FF00]✅ ROOM SPAM COMPLETED!\n🎯 Target: {target_uid}\n📦 Packets: {spam_count}\n🏠 Room: {room_id}\n⚡ Speed: Ultra fast\n"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                    print(f"Room spam completed for UID: {target_uid}")
            
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ ERROR in room spam: {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    print(f"Room spam error: {e}")          
                                    
                                    
                        # Individual command handlers for /s1 to /s5
                        if inPuTMsG.strip().startswith('/s1'):
                            await handle_badge_command('s1', inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)
    
                        if inPuTMsG.strip().startswith('/s2'):
                            await handle_badge_command('s2', inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)

                        if inPuTMsG.strip().startswith('/s3'):
                            await handle_badge_command('s3', inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)

                        if inPuTMsG.strip().startswith('/s4'):
                            await handle_badge_command('s4', inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)
                            
                          #ALL BADGE SPAM REQUEST 
                        if inPuTMsG.strip().startswith('/vspam'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = "[B][C][FF0000]❌ Usage: /spam <uid>\nExample: /spam 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                import time
                                target_uid = parts[1]
                                sequence = ['s1', 's2', 's3', 's4', 's5']  # all badge commands

                                # Send initial consolidated message
                                initial_msg = f"[B][C][1E90FF]🌀 Request received! Preparing to spam {target_uid} with all badges...\n"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)

                                start_time = time.time()
                                count = 0

                                # Run spam for 1 minute
                                while time.time() - start_time < 60:
                                    for cmd in sequence:
                                        fake_command = f"/{cmd} {target_uid}"
                                        await handle_badge_command(cmd, fake_command, uid, chat_id, key, iv, region, response.Data.chat_type)
                                        count += 1
                                        if time.time() - start_time >= 60:
                                            break

                                # Success message after all requests
                                success_msg = f"[B][C][00FF00]✅ Successfully sent {count} Join Requests!\n🎯 Target: {target_uid}\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)

                                    
                                                                                             #JOIN ROOM       
                        if inPuTMsG.strip().startswith('/joinroom'):
                            print('Processing custom room join command')
    
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]❌ Usage: /joinroom (room_id) (password)\nExample: /joinroom 123456 0000\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                room_id = parts[1]
                                room_password = parts[2]
        
                                initial_msg = f"[B][C][00FF00]🚀 Joining custom room...\n🏠 Room: {room_id}\n🔑 Password: {room_password}\n"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
        
                                try:
                                    # Join the custom room
                                    join_packet = await join_custom_room(room_id, room_password, key, iv, region)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
            
                                    success_msg = f"[B][C][00FF00]✅ Joined custom room {room_id}!\n🤖 Bot is now in room chat!\n"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
            
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ Failed to join room: {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        msg = inPuTMsG.strip()

                        if msg.lower().startswith("/e"):
                            try:
                                parts = msg.split(maxsplit=1)
                                if len(parts) != 2:
                                    raise ValueError

                                cmd, team_code = parts
                                emote_part = cmd[2:]   # 🔥 /e12 → "12"

                                if not emote_part.isdigit():
                                    raise ValueError

                                emote_number = int(emote_part)

                                asyncio.create_task(
                                    emote_to_user_once(
                                        team_code=team_code,
                                        emote_number=emote_number,
                                        target_uid=uid,   # 🔥 AUTO YOUR UID
                                        key=key,
                                        iv=iv,
                                        region=region
                                    )
                                )

                                await safe_send_message(
                                    response.Data.chat_type,
                                    f"[B][C][00FF00]✅ Emote sent\nEmote: {emote_number}",
                                    uid, chat_id, key, iv
                                )

                            except:
                                await safe_send_message(
                                    response.Data.chat_type,
                                    "[B][C][FF0000]❌ Usage: /e<number> TEAMCODE\nExample: /e12 ABC123",
                                    uid, chat_id, key, iv
                                )

                        if inPuTMsG.strip().startswith('/createroom'):
                            print('Processing custom room creation')
    
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]❌ Usage: /createroom (room_name) (password) [players=4]\nExample: /createroom BOTROOM 0000 4\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                room_name = parts[1]
                                room_password = parts[2]
                                max_players = parts[3] if len(parts) > 3 else "4"
        
                                initial_msg = f"[B][C][00FF00]🏠 Creating custom room...\n📛 Name: {room_name}\n🔑 Password: {room_password}\n👥 Max Players: {max_players}\n"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
        
                                try:
                                    # Create custom room
                                    create_packet = await create_custom_room(room_name, room_password, int(max_players), key, iv, region)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', create_packet)
            
                                    success_msg = f"[B][C][00FF00]✅ Custom room created!\n🏠 Room: {room_name}\n🔑 Password: {room_password}\n👥 Max: {max_players}\n🤖 Bot is now hosting!\n"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
            
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ Failed to create room: {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)                                                                                                                                                                                                               
                                                
                                              
                                                                                          # FIXED JOIN COMMAND
                        if inPuTMsG.startswith('m'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: m (team_code)\nExample: m ABC123\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                CodE = parts[1]
                                sender_uid = response.Data.uid  # যে ইউজার m কমান্ড দিয়েছে তার UID

                                # ----------------------------
                                # প্রথমে /s2 কমান্ড auto চালানো
                                # ----------------------------
                                s2_command = f"/s2 {sender_uid}"
                                await handle_badge_command('s2', s2_command, uid, chat_id, key, iv, region, response.Data.chat_type)

                                # ----------------------------------
                                # এরপর মূল m join প্রক্রিয়া চলবে
                                # ----------------------------------
                                initial_message = f"[B][C]{get_random_color()}\nJoining squad with code: {CodE}...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)

                                try:
                                    # Regular join
                                    EM = await GenJoinSquadsPacket(CodE, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', EM)
                                    await asyncio.sleep(0.1)

                                    # Dual rings emote
                                    try:
                                        await auto_rings_emote_dual(sender_uid, key, iv, region)
                                    except Exception as emote_error:
                                        print(f"Dual emote failed but join succeeded: {emote_error}")

                                    success_message = f"[B][C][00FF00]✅ SUCCESS! Joined squad: {CodE}!\n💍 Dual Rings emote activated!\n🤖 Bot + You = 💕\n"
                                    await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)

                                except Exception as e:
                                    print(f"Regular join failed, trying ghost join: {e}")
                                    try:
                                        bot_uid = LoGinDaTaUncRypTinG.AccountUID if hasattr(LoGinDaTaUncRypTinG, 'AccountUID') else TarGeT
                                        ghost_packet = await ghost_join_packet(bot_uid, CodE, key, iv)
                                        if ghost_packet:
                                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', ghost_packet)
                                            await asyncio.sleep(0.1)
                                            try:
                                                await auto_rings_emote_dual(sender_uid, key, iv, region)
                                            except Exception as emote_error:
                                                print(f"Dual emote failed but ghost join succeeded: {emote_error}")

                                            success_message = f"[B][C][00FF00]✅ SUCCESS! Ghost joined squad: {CodE}!\n💍 Dual Rings emote activated!\n🤖 Bot + You = 💕\n"
                                            await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
                                        else:
                                            error_msg = f"[B][C][FF0000]❌ ERROR! Failed to create ghost join packet.\n"
                                            await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    except Exception as ghost_error:
                                        print(f"Ghost join also failed: {ghost_error}")
                                        error_msg = f"[B][C][FF0000]❌ ERROR! Failed to join squad: {str(ghost_error)}\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                
                
                        

                        # NEW LAG COMMAND
                        if inPuTMsG.strip().startswith('/llllllllll '):
                            print('Processing lag command in any chat type')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /lag (team_code)\nExample: /lag ABC123\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                team_code = parts[1]
                                
                                # Stop any existing lag task
                                if lag_task and not lag_task.done():
                                    lag_running = False
                                    lag_task.cancel()
                                    await asyncio.sleep(0.1)
                                
                                # Start new lag task
                                lag_running = True
                                lag_task = asyncio.create_task(lag_team_loop(team_code, key, iv, region))
                                
                                # SUCCESS MESSAGE
                                success_msg = f"[B][C][00FF00]✅ SUCCESS! Lag attack started!\nTeam: {team_code}\nAction: Rapid join/leave\nSpeed: Ultra fast (milliseconds)\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)

                        # STOP LAG COMMAND
                        if inPuTMsG.strip() == '/fffff':
                            if lag_task and not lag_task.done():
                                lag_running = False
                                lag_task.cancel()
                                success_msg = f"[B][C][00FF00]✅ SUCCESS! Lag attack stopped successfully!\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]❌ ERROR! No active lag attack to stop!\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        if inPuTMsG.startswith('/exit'):
                            # Process /exit command in any chat type
                            initial_message = f"[B][C]{get_random_color()}\nLeaving current squad...\n"
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                            
                            leave = await ExiT(uid,key,iv)
                            await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , leave)
                            
                            # SUCCESS MESSAGE
                            success_message = f"[B][C][00FF00]✅ SUCCESS! Left the squad successfully!\n"
                            await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)

                        if inPuTMsG.strip().startswith('/start'):
                            # Process /start command in any chat type
                            initial_message = f"[B][C]{get_random_color()}\nStarting match...\n"
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                            
                            EM = await FS(key , iv)
                            await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , EM)
                            
                            # SUCCESS MESSAGE
                            success_message = f"[B][C][00FF00]✅ SUCCESS! Match starting command sent!\n"
                            await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)

# NEW GENERAL EMOTE COMMAND - /c
                        if inPuTMsG.strip().startswith('/c '):
                            print('Processing general emote command in any chat type')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /c uid1 [uid2] [uid3] [uid4] number(1-{len(GENERAL_EMOTES_MAP)})\nExample: /c 123456789 1\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                # Parse uids and number
                                uids = []
                                number = None
                                
                                for part in parts[1:]:
                                    if part.isdigit():
                                        if len(part) <= 3:  # Number should be 1-409 (1-3 digits)
                                            number = part
                                        else:
                                            uids.append(part)
                                    else:
                                        break
                                
                                if not number and parts[-1].isdigit() and len(parts[-1]) <= 3:
                                    number = parts[-1]
                                
                                if not uids or not number:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! Invalid format! Usage: /c uid1 [uid2] [uid3] [uid4] number(1-{len(GENERAL_EMOTES_MAP)})\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    try:
                                        number_str = str(number)
                                        if number_str not in GENERAL_EMOTES_MAP:
                                            error_msg = f"[B][C][FF0000]❌ ERROR! Number must be between 1-{len(GENERAL_EMOTES_MAP)} only!\n"
                                            await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        else:
                                            initial_message = f"[B][C]{get_random_color()}\nSending emote {number_str}...\n"
                                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                                            
                                            success, result_msg = await general_emote_spam(uids, number_str, key, iv, region)
                                            
                                            if success:
                                                emote_id = GENERAL_EMOTES_MAP[number_str]
                                                success_msg = f"[B][C][00FF00]✅ SUCCESS! {result_msg}\n"
                                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                            else:
                                                error_msg = f"[B][C][FF0000]❌ ERROR! {result_msg}\n"
                                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                            
                                    except ValueError:
                                        error_msg = f"[B][C][FF0000]❌ ERROR! Invalid number format! Use 1-{len(GENERAL_EMOTES_MAP)} only.\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        # ===============================
                        # COMMAND DETECT
                        # ===============================

                        if inPuTMsG.strip().lower() == "elist":
                            asyncio.create_task(
                                send_elist(
                                    response.Data.chat_type,
                                    uid,
                                    chat_id,
                                    key,
                                    iv,
                                    whisper_writer,
                                    online_writer
                                )
                            )

                        if inPuTMsG.strip().startswith('/title'):
                            # Process /title command in any chat type
                            parts = inPuTMsG.strip().split()
    
                            # Check if bot is in a team
              
                            initial_message = f"[B][C]{get_random_color()}\nSending title to current team...\n"
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
    
                            try:
                                # Send title packet
                                title_packet = await send_title_msg(chat_id, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', title_packet)
        
                                # SUCCESS MESSAGE
                                success_message = f"[B][C][00FF00]✅ SUCCESS! Title sent to current team!\n"
                                await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
        
                            except Exception as e:
                                print(f"Title send failed: {e}")
                                error_msg = f"[B][C][FF0000]❌ ERROR! Failed to send title: {str(e)}\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        # Emote command - works in all chat types
                        if inPuTMsG.strip().startswith('/e'):
                            print(f'Processing emote command in chat type: {response.Data.chat_type}')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /e (uid) (emote_id)\nExample: /e 123456789 909000001\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                continue
                                
                            initial_message = f'[B][C]{get_random_color()}\nSending emote to target...\n'
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)

                            uid2 = uid3 = uid4 = uid5 = None
                            s = False
                            target_uids = []

                            try:
                                target_uid = int(parts[1])
                                target_uids.append(target_uid)
                                uid2 = int(parts[2]) if len(parts) > 2 else None
                                if uid2: target_uids.append(uid2)
                                uid3 = int(parts[3]) if len(parts) > 3 else None
                                if uid3: target_uids.append(uid3)
                                uid4 = int(parts[4]) if len(parts) > 4 else None
                                if uid4: target_uids.append(uid4)
                                uid5 = int(parts[5]) if len(parts) > 5 else None
                                if uid5: target_uids.append(uid5)
                                idT = int(parts[-1])  # Last part is emote ID

                            except ValueError as ve:
                                print("ValueError:", ve)
                                s = True
                            except Exception as e:
                                print(f"Error parsing emote command: {e}")
                                s = True

                            if not s:
                                try:
                                    for target in target_uids:
                                        H = await Emote_k(target, idT, key, iv, region)
                                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                                        await asyncio.sleep(0.1)
                                    
                                    # SUCCESS MESSAGE
                                    success_msg = f"[B][C][00FF00]✅ SUCCESS! Emote {idT} sent to {len(target_uids)} player(s)!\nTargets: {', '.join(map(str, target_uids))}\n"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)

                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ ERROR sending emote: {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Invalid UID format. Usage: /e (uid) (emote_id)\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                

                        # EVO CYCLE START COMMAND - @
                        if inPuTMsG.strip().startswith('@'):
                            print('Processing evo cycle start command in any chat type')
    
                            parts = inPuTMsG.strip().split()
                            uids = []
    
                            # Always use the sender's UID (the person who typed @)
                            sender_uid = str(response.Data.uid)
                            uids.append(sender_uid)
                            print(f"Using sender's UID: {sender_uid}")
    
                            # Optional: Also allow specifying additional UIDs
                            if len(parts) > 1:
                                for part in parts[1:]:  # Skip the first part which is "@"
                                    if part.isdigit() and len(part) >= 9 and part != sender_uid:  # UIDs are usually 7+ digits
                                        uids.append(part)
                                        print(f"Added additional UID: {part}")

                            # Stop any existing evo cycle
                            if evo_cycle_task and not evo_cycle_task.done():
                                evo_cycle_running = False
                                evo_cycle_task.cancel()
                                await asyncio.sleep(0.5)
    
                            # Start new evo cycle
                            evo_cycle_running = True
                            evo_cycle_task = asyncio.create_task(evo_cycle_spam(uids, key, iv, region))
    
                            # SUCCESS MESSAGE
                            if len(uids) == 1:
                                success_msg = f"[B][C][00FF00]✅ SUCCESS! Evolution emote cycle started!\n🎯 Target: Yourself\n🎭 Emotes: All 18 evolution emotes\n⏰ Delay: 5 seconds between emotes\n🔄 Cycle: Continuous loop until /stop\n"
                            else:
                                success_msg = f"[B][C][00FF00]✅ SUCCESS! Evolution emote cycle started!\n?? Targets: Yourself + {len(uids)-1} other players\n🎭 Emotes: All 18 evolution emotes\n⏰ Delay: 5 seconds between emotes\n🔄 Cycle: Continuous loop until /stop\n"
    
                            await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                            print(f"Started evolution emote cycle for UIDs: {uids}")
                        
                        # EVO CYCLE STOP COMMAND - /s
                        if inPuTMsG.strip() == '/stop':
                            if evo_cycle_task and not evo_cycle_task.done():
                                evo_cycle_running = False
                                evo_cycle_task.cancel()
                                success_msg = f"[B][C][00FF00]✅ SUCCESS! Evolution emote cycle stopped successfully!\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                print("Evolution emote cycle stopped by command")
                            else:
                                error_msg = f"[B][C][FF0000]❌ ERROR! No active evolution emote cycle to stop!\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        
                        # ================= BOT AUTO EMOTE LOOP COMMANDS =================

                        cmd = inPuTMsG.strip().lower()

                        # ---------- /admin ----------
                        if cmd == '/admin':
                            print('Processing /admin auto emote loop')

                            if BOT_STATE["running"]:
                                await safe_send_message(
                                    response.Data.chat_type,
                                    "[B][C][FFFF00]⚠️ Bot already running!",
                                    uid, chat_id, key, iv
                                )
                            else:
                                BOT_STATE["uid"] = ADMIN_BOT_UID
                                BOT_STATE["running"] = True
                                BOT_STATE["task"] = asyncio.create_task(
                                    bot_emote_loop(key, iv, region, delay=6)
                                )
                                await safe_send_message(
                                    response.Data.chat_type,
                                    "[B][C][00FF00]👑 ADMIN BOT STARTED\n🛑 Stop: /s",
                                    uid, chat_id, key, iv
                                )

                        # ---------- /bot ----------
                        elif cmd == '/bot':
                            print('Processing /bot auto emote loop')

                            if BOT_STATE["running"]:
                                await safe_send_message(
                                    response.Data.chat_type,
                                    "[B][C][FFFF00]⚠️ Bot already running!",
                                    uid, chat_id, key, iv
                                )
                            else:
                                BOT_STATE["uid"] = DEFAULT_BOT_UID
                                BOT_STATE["running"] = True
                                BOT_STATE["task"] = asyncio.create_task(
                                    bot_emote_loop(key, iv, region, delay=6)
                                )
                                await safe_send_message(
                                    response.Data.chat_type,
                                    "[B][C][00FF00]🤖 BOT STARTED\n🛑 Stop: /stop",
                                    uid, chat_id, key, iv
                                )

                        if inPuTMsG.strip().lower() == '/stop':
                            print('Processing /s')

                            if not BOT_STATE["running"]:
                                await safe_send_message(
                                    response.Data.chat_type,
                                    "[B][C][FF0000]❌ Bot is not running!",
                                    uid, chat_id, key, iv
                                )
                            else:
                                BOT_STATE["running"] = False
                                if BOT_STATE["task"]:
                                    BOT_STATE["task"].cancel()
                                    BOT_STATE["task"] = None

                                await safe_send_message(
                                    response.Data.chat_type,
                                    "[B][C][00FF00]🛑 BOT STOPPED",
                                    uid, chat_id, key, iv
                                )

# ================================================================

                        # Fast emote spam command - works in all chat types
                        if inPuTMsG.strip().startswith('/fast'):
                            print('Processing fast emote spam in any chat type')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /fast uid1 [uid2] [uid3] [uid4] emoteid\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                # Parse uids and emoteid
                                uids = []
                                emote_id = None
                                
                                for part in parts[1:]:
                                    if part.isdigit():
                                        if len(part) > 3:  # Assuming UIDs are longer than 3 digits
                                            uids.append(part)
                                        else:
                                            emote_id = part
                                    else:
                                        break
                                
                                if not emote_id and parts[-1].isdigit():
                                    emote_id = parts[-1]
                                
                                if not uids or not emote_id:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! Invalid format! Usage: /fast uid1 [uid2] [uid3] [uid4] emoteid\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    # Stop any existing fast spam
                                    if fast_spam_task and not fast_spam_task.done():
                                        fast_spam_running = False
                                        fast_spam_task.cancel()
                                    
                                    # Start new fast spam
                                    fast_spam_running = True
                                    fast_spam_task = asyncio.create_task(fast_emote_spam(uids, emote_id, key, iv, region))
                                    
                                    # SUCCESS MESSAGE
                                    success_msg = f"[B][C][00FF00]✅ SUCCESS! Fast emote spam started!\nTargets: {len(uids)} players\nEmote: {emote_id}\nSpam count: 25 times\n"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)

                        # Custom emote spam command - works in all chat types
                        if inPuTMsG.strip().startswith('/p'):
                            print('Processing custom emote spam in any chat type')

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 4:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /p (uid) (emote_id) (times)\nExample: /p 123456789 909000001 10\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                try:
                                    target_uid = parts[1]
                                    emote_id = parts[2]
                                    times = int(parts[3])
            
                                    if times <= 0:
                                        error_msg = f"[B][C][FF0000]❌ ERROR! Times must be greater than 0!\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    elif times > 100:
                                        error_msg = f"[B][C][FF0000]❌ ERROR! Maximum 100 times allowed for safety!\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    else:
                                        # Stop any existing custom spam
                                        if custom_spam_task and not custom_spam_task.done():
                                            custom_spam_running = False
                                            custom_spam_task.cancel()
                                            await asyncio.sleep(0.5)
                
                                        # Start new custom spam
                                        custom_spam_running = True
                                        custom_spam_task = asyncio.create_task(custom_emote_spam(target_uid, emote_id, times, key, iv, region))
                
                                        # SUCCESS MESSAGE
                                        success_msg = f"[B][C][00FF00]✅ SUCCESS! Custom emote spam started!\nTarget: {target_uid}\nEmote: {emote_id}\nTimes: {times}\n"
                                        await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                
                                except ValueError:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! Invalid number format! Usage: /p (uid) (emote_id) (times)\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        # Spam request command - works in all chat types
                        if inPuTMsG.strip().startswith('/spm_inv'):
                            print('Processing spam invite with cosmetics')
    
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ Usage: /spm_inv (uid)\nExample: /spm_inv 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
        
                                # Stop any existing spam request
                                if spam_request_task and not spam_request_task.done():
                                    spam_request_running = False
                                    spam_request_task.cancel()
                                    await asyncio.sleep(0.5)
        
                                # Start new spam request WITH COSMETICS
                                spam_request_running = True
                                spam_request_task = asyncio.create_task(spam_request_loop_with_cosmetics(target_uid, key, iv, region))
        
                                # SUCCESS MESSAGE
                                success_msg = f"[B][C][00FF00]✅ COSMETIC SPAM STARTED!\n🎯 Target: {target_uid}\n📦 Requests: 30\n🎭 Features: V-Badges + Cosmetics\n⚡ Each invite has different cosmetics!\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)

                        # Stop spam request command - works in all chat types
                        if inPuTMsG.strip() == '/stop spm_inv':
                            if spam_request_task and not spam_request_task.done():
                                spam_request_running = False
                                spam_request_task.cancel()
                                success_msg = f"[B][C][00FF00]✅ SUCCESS! Spam request stopped successfully!\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]❌ ERROR! No active spam request to stop!\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        # NEW EVO COMMANDS
                        if inPuTMsG.strip().startswith('/mr '):
                            print('Processing emote command via JSON map')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /mr uid1 [uid2] [uid3] [uid4] number(1-21)\nExample: /mr 123456789 1\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                # Parse uids and number
                                uids = []
                                number = None
                                
                                for part in parts[1:]:
                                    if part.isdigit():
                                        if len(part) <= 2:  # Number should be 1-21 (1 or 2 digits)
                                            number = part
                                        else:
                                            uids.append(part)
                                    else:
                                        break
                                
                                if not number and parts[-1].isdigit() and len(parts[-1]) <= 2:
                                    number = parts[-1]
                                
                                if not uids or not number:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! Invalid format! Usage: /mr uid1 [uid2] [uid3] [uid4] number(1-21)\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    try:
                                        number_int = int(number)
                                        if number_int not in GENERAL_EMOTES_MAP:
                                            error_msg = f"[B][C][FF0000]❌ ERROR! Number must be between 1-21 only!\n"
                                            await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        else:
                                            initial_message = f"[B][C]{get_random_color()}\nSending evolution emote {number_int}...\n"
                                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                                            
                                            success, result_msg = await evo_emote_spam(uids, number_int, key, iv, region)
                                            
                                            if success:
                                                success_msg = f"[B][C][00FF00]✅ SUCCESS! {result_msg}\n"
                                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                            else:
                                                error_msg = f"[B][C][FF0000]❌ ERROR! {result_msg}\n"
                                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                            
                                    except ValueError:
                                        error_msg = f"[B][C][FF0000]❌ ERROR! Invalid number format! Use 1-21 only.\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        if inPuTMsG.strip().startswith('/evo_fast '):
                            print('Processing evo_fast command in any chat type')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /evo_fast uid1 [uid2] [uid3] [uid4] number(1-21)\nExample: /evo_fast 123456789 1\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                # Parse uids and number
                                uids = []
                                number = None
                                
                                for part in parts[1:]:
                                    if part.isdigit():
                                        if len(part) <= 2:  # Number should be 1-21 (1 or 2 digits)
                                            number = part
                                        else:
                                            uids.append(part)
                                    else:
                                        break
                                
                                if not number and parts[-1].isdigit() and len(parts[-1]) <= 2:
                                    number = parts[-1]
                                
                                if not uids or not number:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! Invalid format! Usage: /evo_fast uid1 [uid2] [uid3] [uid4] number(1-21)\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    try:
                                        number_int = int(number)
                                        if number_int not in GENERAL_EMOTES_MAP:
                                            error_msg = f"[B][C][FF0000]❌ ERROR! Number must be between 1-21 only!\n"
                                            await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        else:
                                            # Stop any existing evo_fast spam
                                            if evo_fast_spam_task and not evo_fast_spam_task.done():
                                                evo_fast_spam_running = False
                                                evo_fast_spam_task.cancel()
                                                await asyncio.sleep(0.5)
                                            
                                            # Start new evo_fast spam
                                            evo_fast_spam_running = True
                                            evo_fast_spam_task = asyncio.create_task(evo_fast_emote_spam(uids, number_int, key, iv, region))
                                            
                                            # SUCCESS MESSAGE
                                            emote_id = GENERAL_EMOTES_MAP[number_int]
                                            success_msg = f"[B][C][00FF00]✅ SUCCESS! Fast evolution emote spam started!\nTargets: {len(uids)} players\nEmote: {number_int} (ID: {emote_id})\nSpam count: 25 times\nInterval: 0.1 seconds\n"
                                            await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                            
                                    except ValueError:
                                        error_msg = f"[B][C][FF0000]❌ ERROR! Invalid number format! Use 1-21 only.\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        if inPuTMsG.strip().lower().startswith("/magic"):
                            parts = inPuTMsG.strip().split()

                            if len(parts) < 2:
                                await safe_send_message(
                                    response.Data.chat_type,
                                    "[B][C][FF0000]❌ Usage: /Magic (team_code)",
                                    uid,
                                    chat_id,
                                    key,
                                    iv
                                )
                            else:
                                team_code = parts[1]

                                await safe_send_message(
                                    response.Data.chat_type,
                                    "[B][C][1E90FF]🌀 Magic bundle started...",
                                    uid,
                                    chat_id,
                                    key,
                                    iv
                                )

                                asyncio.create_task(
                                    magic_bundle_sequence(
                                        team_code,
                                        response.Data.chat_type,
                                        chat_id,
                                        uid,
                                        key,
                                        iv,
                                        region
                                    )
                                )

                        if inPuTMsG.strip().startswith('/animation'):
                            print("Processing animation command")

                            parts = inPuTMsG.strip().split()

                            # যদি কোন আইডি না দেয়
                            if len(parts) < 2:
                                animation_list = """[B][C][FFFFFF]• 1-rampage 
[FFFFFF]• 2-cannibal 
[FFFFFF]• 3-devil 
[FFFFFF]• 4-scorpio 
[FFFFFF]• 5-frostfire
[FFFFFF]• 6-paradox 
[FFFFFF]• 7-naruto 
[FFFFFF]• 8-aurora 
[FFFFFF]• 9-midnight 
[FFFFFF]• 10-itachi 
[FFFFFF]• 11-dreamspace
"""
                                await safe_send_message(response.Data.chat_type, animation_list, uid, chat_id, key, iv)
                                return

                            animation_key = parts[1].lower()

                            # Animation ID Mapping
                            animation_ids = {
                                    "1":      914000002,
                                    "2":      914000003,
                                    "3":      914038001,
                                    "4":      914039001,
                                    "5":      914042001,
                                    "6":      914044001,
                                    "7":      914047001,
                                    "8":      914047002,
                                    "9":      914048001,
                                    "10":     914050001,
                                    "11":     914051001
                                }

                            # যদি ভুল দেয়
                            if animation_key not in animation_ids:
                                await safe_send_message(
                                    response.Data.chat_type,
                                    f"[B][C][FF0000]❌ Animation '{animation_key}' not found!\nUse: /animation [number]",
                                    uid, chat_id, key, iv
                                )
                                return

                            animation_id = animation_ids[animation_key]

                            # Sending message
                            await safe_send_message(
                                response.Data.chat_type,
                                f"[B][C][00FF00]✨ Sending Animation...\n🆔 ID: {animation_id}",
                                uid, chat_id, key, iv
                            )

                            try:
                                # তোমার নতুন ফাংশন কল
                                packet = await animation_packet(animation_id, key, iv)

                                if packet and online_writer:
                                    await SEndPacKeT(whisper_writer, online_writer, "OnLine", packet)

                                    success_msg = f"""[B][C][00FF00]✅ ANIMATION SENT SUCCESSFULLY!
✨ Name: {animation_key}
🆔 ID: {animation_id}
👤 Target: {uid}
"""
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)

                                else:
                                    await safe_send_message(
                                        response.Data.chat_type,
                                        "[B][C][FF0000]❌ Failed to create animation packet!",
                                        uid, chat_id, key, iv
                                    )

                            except Exception as e:
                                await safe_send_message(
                                    response.Data.chat_type,
                                    f"[B][C][FF0000]❌ Error sending animation:\n{str(e)[:80]}",
                                    uid, chat_id, key, iv
                                )

                        if inPuTMsG.strip().startswith('/bundle'):
                            print('Processing bundle command')

                            parts = inPuTMsG.strip().split()

                            if len(parts) < 2:
                                await safe_send_message(
                                    response.Data.chat_type,
                                    "[B][C][FF0000]❌ Use: /bundle [number]",
                                    uid, chat_id, key, iv
                                )
                                return

                            bundle_key = parts[1].lower()

                            bundle_ids = {
                                "1": 914000002,
                                "2": 914000003,
                                "3": 914038001,
                                "4": 914039001,
                                "5": 914042001,
                                "6": 914044001,
                                "7": 914047001,
                                "8": 914047002,
                                "9": 914048001,
                                "10": 914050001,
                                "11": 914051001
                            }

                            # 🔥 Custom Delay Mapping
                            delay_map = {
                                "1": 5.1,
                                "2": 3.0,
                                "3": 3.0,
                                "4": 5.0,
                                "5": 3.3,
                                "6": 3.5,
                                "7": 2.6,
                                "8": 3.7,
                                "9": 4.4,
                                "10": 3.0,
                                "11": 4.2
                            }

                            if bundle_key not in bundle_ids:
                                await safe_send_message(
                                    response.Data.chat_type,
                                    f"[B][C][FF0000]❌ Bundle '{bundle_key}' not found!",
                                    uid, chat_id, key, iv
                                )
                                return

                            bundle_id = bundle_ids[bundle_key]
                            delay_time = delay_map.get(bundle_key, 3)

                            # =========================
                            # 1️⃣ SEND ANIMATION FIRST
                            # =========================
                            await safe_send_message(
                                response.Data.chat_type,
                                f"[B][C][00FF00]✨ Sending Animation First...\n🆔 {bundle_id}",
                                uid, chat_id, key, iv
                            )

                            try:
                                animation_pkt = await animation_packet(bundle_id, key, iv)

                                if animation_pkt and online_writer:
                                    await SEndPacKeT(whisper_writer, online_writer, "OnLine", animation_pkt)
                                else:
                                    await safe_send_message(
                                        response.Data.chat_type,
                                        "[B][C][FF0000]❌ Animation failed!",
                                        uid, chat_id, key, iv
                                    )
                                    return

                            except Exception as e:
                                await safe_send_message(
                                    response.Data.chat_type,
                                    f"[B][C][FF0000]❌ Animation Error:\n{str(e)[:80]}",
                                    uid, chat_id, key, iv
                                )
                                return

                            # =========================
                            # 2️⃣ WAIT CUSTOM DELAY
                            # =========================
                            await safe_send_message(
                                response.Data.chat_type,
                                f"[B][C][FFFF00]⏳ Waiting {delay_time}s before bundle...",
                                uid, chat_id, key, iv
                            )

                            await asyncio.sleep(delay_time)

                            # =========================
                            # 3️⃣ SEND BUNDLE
                            # =========================
                            await safe_send_message(
                                response.Data.chat_type,
                                f"[B][C][00FF00]🎁 Sending Bundle...\n🆔 {bundle_id}",
                                uid, chat_id, key, iv
                            )

                            try:
                                bundle_pkt = await bundle_packet_async(bundle_id, key, iv)

                                if bundle_pkt and online_writer:
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', bundle_pkt)

                                    await safe_send_message(
                                        response.Data.chat_type,
                                        f"[B][C][00FF00]✅ DONE!\n✨ Animation + Bundle Sent\n🆔 {bundle_id}",
                                        uid, chat_id, key, iv
                                    )
                                else:
                                    await safe_send_message(
                                        response.Data.chat_type,
                                        "[B][C][FF0000]❌ Bundle packet failed!",
                                        uid, chat_id, key, iv
                                    )

                            except Exception as e:
                                await safe_send_message(
                                    response.Data.chat_type,
                                    f"[B][C][FF0000]❌ Bundle Error:\n{str(e)[:80]}",
                                    uid, chat_id, key, iv
                                )

                        elif inPuTMsG.strip().startswith('/b'):
    
                            parts = inPuTMsG.strip().split()
                            
                            if len(parts) < 2:
                             
                                bundle_list = """[B][C][FFFFFF]• 1-rampage 
[FFFFFF]• 2-cannibal 
[FFFFFF]• 3-devil 
[FFFFFF]• 4-scorpio 
[FFFFFF]• 5-frostfire
[FFFFFF]• 6-paradox 
[FFFFFF]• 7-naruto 
[FFFFFF]• 8-aurora 
[FFFFFF]• 9-midnight 
[FFFFFF]• 10-itachi 
[FFFFFF]• 11-dreamspace
"""
                                await safe_send_message(response.Data.chat_type, bundle_list, uid, chat_id, key, iv)
                            else:
                                bundle_name = parts[1].lower()
                          
      
                                # Bundle IDs mapping
                                bundle_ids = {
                                    "1":     914000002,
                                    "2":      914000003,
                                    "3":      914038001,
                                    "4":      914039001,
                                    "5":      914042001,
                                    "6":      914044001,
                                    "7":      914047001,
                                    "8":      914047002,
                                    "9":      914048001,
                                    "10":      914050001,
                                    "11":      914051001
                                }
                                
                             
                                if bundle_name not in bundle_ids:
                                    error_msg = f"""[B][C][FF0000]❌ Bundle '{bundle_name}' not found!

[00FF00]Available bundles:
[FFFFFF]• rampage • cannibal • devil
[FFFFFF]• scorpio • frostfire • paradox
[FFFFFF]• naruto • aurora • midnight
[FFFFFF]• itachi • dreamspace

[00FF00]Use: /bundle [name]"""
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    return
                                    
                                bundle_id = bundle_ids[bundle_name]

                                initial_msg = f"[B][C][00FF00]🎁 Sending bundle...\nID: {bundle_id}\n"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
        
                                try:
                                
                                    bundle_packet = await bundle_packet_async(bundle_id, key, iv)
            
                                    if bundle_packet and online_writer:
                                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', bundle_packet)
                                        success_msg = f"[B][C][00FF00]✅ BUNDLE SENT SUCCESSFULLY!\n🎁 Name: {bundle_name}\n🆔 ID: {bundle_id}\n👤 Target: {uid}"
                                        await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                    else:
                                        error_msg = f"[B][C][FF0000]❌ Failed to create bundle packet!\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ Error sending bundle: {str(e)[:50]}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)


                        # FREEZE COMMAND - /freeze [uid]
                        parts = inPuTMsG.strip().split()
                        
                        # যদি ফাঁকা মেসেজ আসে, তবে ক্র্যাশ না করে ইগনোর করবে
                        if not parts:
                            continue
                            
                        cmd = parts[0].lower()

                        if cmd == "/f" or cmd == "/freeze":
                            print('Processing freeze command')
    
                            parts = inPuTMsG.strip().split()
    
                            if len(parts) < 2:
                                error_msg = f"""[B][C][00FFFF]❄️ FREEZE COMMAND

❌ Usage: /freeze (uid)
        
📝 Examples:
/freeze me - Freeze yourself
/freeze 123456789 - Freeze specific UID

🎯 What it does:
• Sends 3 ice/freeze emotes in sequence
• 1-second cycles for 10 seconds total
• Emotes: 909052008 → 909052008 → 909052008
• Creates a "freeze" effect!

💡 Use /stop_freeze to stop early
"""
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                
                                # Handle "me" or "self"
                                if target_uid.lower() in ['me', 'self', 'myself']:
                                    target_uid = str(response.Data.uid)
                                    target_name = "Yourself"
                                else:
                                    target_name = f"UID {target_uid}"
                                
                                # Stop any existing freeze task
                                global freeze_running, freeze_task
                                if freeze_task and not freeze_task.done():
                                    freeze_running = False
                                    freeze_task.cancel()
                                    await asyncio.sleep(0.5)
        
                                # Send initial message
                                initial_msg = f"""[B][C][00FFFF]❄️ FREEZE COMMAND STARTING!

🎯 Target: {target_name}
⏱️ Duration: {FREEZE_DURATION} seconds
🔄 Cycle: 1 second (3 emotes each)
🎭 Sequence: 
  1. 909052008 (Ice)
  2. 909052008 (Frozen) 
  3. 909052008 (Freeze)

⏳ Starting freeze sequence...
"""
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
        
                                # Start freeze task
                                freeze_running = True
                                freeze_task = asyncio.create_task(
                                    freeze_emote_spam(target_uid, key, iv, region, response.Data.chat_type, chat_id, uid)
                                )
        
                                # Handle completion
                                asyncio.create_task(
                                    handle_freeze_completion(freeze_task, target_uid, uid, chat_id, response.Data.chat_type, key, iv)
                                )                      
                    
                        # NEW EVO_CUSTOM COMMAND
                        if inPuTMsG.strip().startswith('/evo_c '):
                            print('Processing evo_c command in any chat type')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /evo_c uid1 [uid2] [uid3] [uid4] number(1-21) time(1-100)\nExample: /evo_c 123456789 1 10\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                # Parse uids, number, and time
                                uids = []
                                number = None
                                time_val = None
                                
                                for part in parts[1:]:
                                    if part.isdigit():
                                        if len(part) <= 2:  # Number or time should be 1-100 (1, 2, or 3 digits)
                                            if number is None:
                                                number = part
                                            elif time_val is None:
                                                time_val = part
                                            else:
                                                uids.append(part)
                                        else:
                                            uids.append(part)
                                    else:
                                        break
                                
                                # If we still don't have time_val, try to get it from the last part
                                if not time_val and len(parts) >= 3:
                                    last_part = parts[-1]
                                    if last_part.isdigit() and len(last_part) <= 3:
                                        time_val = last_part
                                        # Remove time_val from uids if it was added by mistake
                                        if time_val in uids:
                                            uids.remove(time_val)
                                
                                if not uids or not number or not time_val:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! Invalid format! Usage: /evo_c uid1 [uid2] [uid3] [uid4] number(1-21) time(1-100)\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    try:
                                        number_int = int(number)
                                        time_int = int(time_val)
                                        
                                        if number_int not in GENERAL_EMOTES_MAP:
                                            error_msg = f"[B][C][FF0000]❌ ERROR! Number must be between 1-21 only!\n"
                                            await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        elif time_int < 1 or time_int > 100:
                                            error_msg = f"[B][C][FF0000]❌ ERROR! Time must be between 1-100 only!\n"
                                            await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        else:
                                            # Stop any existing evo_custom spam
                                            if evo_custom_spam_task and not evo_custom_spam_task.done():
                                                evo_custom_spam_running = False
                                                evo_custom_spam_task.cancel()
                                                await asyncio.sleep(0.5)
                                            
                                            # Start new evo_custom spam
                                            evo_custom_spam_running = True
                                            evo_custom_spam_task = asyncio.create_task(evo_custom_emote_spam(uids, number_int, time_int, key, iv, region))
                                            
                                            # SUCCESS MESSAGE
                                            emote_id = GENERAL_EMOTES_MAP[number_int]
                                            success_msg = f"[B][C][00FF00]✅ SUCCESS! Custom evolution emote spam started!\nTargets: {len(uids)} players\nEmote: {number_int} (ID: {emote_id})\nRepeat: {time_int} times\nInterval: 0.1 seconds\n"
                                            await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                            
                                    except ValueError:
                                        error_msg = f"[B][C][FF0000]❌ ERROR! Invalid number/time format! Use numbers only.\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        # Stop evo_fast spam command
                        if inPuTMsG.strip() == '/stop evo_fast':
                            if evo_fast_spam_task and not evo_fast_spam_task.done():
                                evo_fast_spam_running = False
                                evo_fast_spam_task.cancel()
                                success_msg = f"[B][C][00FF00]✅ SUCCESS! Evolution fast spam stopped successfully!\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]❌ ERROR! No active evolution fast spam to stop!\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        # Stop evo_custom spam command
                        if inPuTMsG.strip() == '/stop evo_c':
                            if evo_custom_spam_task and not evo_custom_spam_task.done():
                                evo_custom_spam_running = False
                                evo_custom_spam_task.cancel()
                                success_msg = f"[B][C][00FF00]✅ SUCCESS! Evolution custom spam stopped successfully!\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]❌ ERROR! No active evolution custom spam to stop!\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

# =================================================================
                        # EXACT MATCH FULL COMMANDS VIP HELP MENU 🚀 (UNIVERSAL FOR ALL CHAT TYPES)
                        # =================================================================
                        if inPuTMsG.strip().lower() in ("help", "hi", "/help", "hello", "commands"):
                            print(f"Help command detected from UID: {uid} in chat type: {response.Data.chat_type}")
                            
                            # সবার জন্য একই হেডার (Welcome Text)
                            header = f"[B][32CD32]👋 Hey User Welcome To ARIYAN BOT"
                            await safe_send_message(response.Data.chat_type, header, uid, chat_id, key, iv)
                            await asyncio.sleep(0.6)

                            # ───── Box 1: ACCOUNT & INFO ─────
                            account_commands = """[B][00FFFF]■ V bage spam■
[B][00FFFF]──────────────────
[B][FFD700] V bage spam
[B][00FFFF]├─[00FF00]/s1 [FFFFFF][uid]
[B][00FFFF]├─[00FF00]/s2 [FFFFFF][uid]
[B][00FFFF]├─[00FF00]/s3 [FFFFFF][uid]
[B][00FFFF]└─[00FF00]/s4 [FFFFFF][uid]
[B][00FFFF]──────────────────
[B][FFD700]ultra power 
[B][00FFFF]├─[00FF00]/vspam [FFFFFF][uid]
[B][00FFFF]├─[00FF00]/room [FFFFFF][uid] [rmid]
[B][00FFFF]└─[00FF00]/spam2 [FFFFFF][all]
[B][00FFFF]──────────────────"""
                            await safe_send_message(response.Data.chat_type, account_commands, uid, chat_id, key, iv)
                            await asyncio.sleep(0.6)

                            # ───── Box 2: TEAM & MATCH ─────  
                            team_commands = """[B][FFA500]■ TEAM & MATCH ■
[B][FFA500]──────────────────
[B][FFD700]TEAM CREATION
[B][FFA500]├─[00FF00]/3 [FFFFFF](3 Player Grp)
[B][FFA500]├─[00FF00]/5 [FFFFFF](5 Player Grp)
[B][FFA500]├─[00FF00]/6 [FFFFFF](6 Player Grp)
[B][FFA500]└─[00FF00]/inv [FFFFFF][uid]
[B][FFA500]──────────────────
[B][FFD700]MATCH CONTROL
[B][FFA500]├─[00FF00]m [FFFFFF][code] (Join)
[B][FFA500]├─[00FF00]/exit
[B][FFA500]├─[00FF00]/start
[B][FFA500]└─[00FF00]/kick [FFFFFF][uid]
[B][FFA500]──────────────────"""
                            await safe_send_message(response.Data.chat_type, team_commands, uid, chat_id, key, iv)
                            await asyncio.sleep(0.6)

                            # ───── Box 3: ROOM SPAM & BADGE ─────  
                            room_commands = """[B][FF00FF]■ ROOM & BADGE ■
[B][FF00FF]──────────────────
[B][FFD700]CUSTOM ROOM
[B][FF00FF]├─[00FF00]/createroom [FFFFFF][name] [pass]
[B][FF00FF]├─[00FF00]/joinroom [FFFFFF][id] [pass]
[B][FF00FF]├─[00FF00]/roommsg [FFFFFF][id] [msg]
[B][FF00FF]└─[00FF00]/room [FFFFFF][uid] [room_id]
[B][FF00FF]──────────────────
[B][FFD700]BADGE REQUESTS
[B][FF00FF]├─[00FF00]/s1 [FFFFFF]to [00FF00]/s5 [FFFFFF][uid]
[B][FF00FF]└─[00FF00]/spa🤫m [FFFFFF][uid] (All Badges)
[B][FF00FF]──────────────────"""
                            await safe_send_message(response.Data.chat_type, room_commands, uid, chat_id, key, iv)
                            await asyncio.sleep(0.6)

                            # ───── Box 4: FUN & ENTERTAINMENT ─────  
                            fun_commands = """[B][8A2BE2]■ FUN & ENTERTAINMENT ■
[B][8A2BE2]──────────────────
[B][FFD700]GAMES & JOKES
[B][8A2BE2]├─[00FF7F]/dhadha [FFFFFF](মজার ধাঁধা)
[B][8A2BE2]├─[00FF7F]/joke [FFFFFF](এফএফ জোকস)
[B][8A2BE2]└─[00FF7F]/luk [FFFFFF](Luck Meter)
[B][8A2BE2]──────────────────
[B][FFD700]FUN TEXTS
[B][8A2BE2]├─[00FF7F]/love [FFFFFF][নাম] (ভালোবাসা)
[B][8A2BE2]├─[00FF7F]/role [FFFFFF][নাম] (স্কোয়াড রোল)
[B][8A2BE2]├─[00FF7F]/Ga🤫li [FFFFFF][নাম] (বকা দেওয়া)
[B][8A2BE2]└─[00FF7F]/Gali2 [FFFFFF][নাম] (ইউ আইডি)
[B][8A2BE2]──────────────────"""
                            await safe_send_message(response.Data.chat_type, fun_commands, uid, chat_id, key, iv)
                            await asyncio.sleep(0.6)

                            # ───── Box 5: ATTACK & CRASH ─────  
                            attack_commands = """[B][FF0000]■ SPAM & ATTACK ■
[B][FF0000]──────────────────
[B][FFD700]TEAM ATTACK
[B][FF0000]├─[00FF00]/ghost [FFFFFF][code]
[B][FF0000]├─[00FF00]/multijoin [FFFFFF][uid]
[B][FF0000]├─[00FF00]/sp🤫m_inv [FFFFFF][uid]
[B][FF0000]└─[00FF00]/stop
[B][FF0000]──────────────────
[B][FFD700]PLAYER ATTACK
[B][FF0000]├─[00FF00]/reject [FFFFFF][uid]
[B][FF0000]├─[00FF00]/reject_stop
[B][FF0000]├─[00FF00]/freeze [FFFFFF]or [00FF00]/f [FFFFFF][uid]
[B][FF0000]└─[00FF00]/quick [FFFFFF][code] [emote_id]
[B][FF0000]──────────────────"""
                            await safe_send_message(response.Data.chat_type, attack_commands, uid, chat_id, key, iv)
                            await asyncio.sleep(0.6)

                            # ───── Box 6: EMOTE PANEL ─────  
                            emote_commands = """[B][FF1493]■ MX EMOTE  ■
[B][FF1493]──────────────────
[B][FFD700]BASIC
[B][FF1493]├─[00FF00]elist [FFFFFF] [Emotes]
[B][FF1493]└─[00FF00][Only Number]
[B][FF1493]──────────────────
[B][FFD700]CUSTOM & FAST
[B][FF1493]├─[00FF00]/fast [FFFFFF][uids] [id]
[B][FF1493]└─[00FF00]/e [nm] [FFFFFF][code]
[B][FF1493]──────────────────
[B][FFD700]AUTO BOT
[B][FF1493]├─[00FF00]/bot [FFFFFF] [Default Loop]
[B][FF1493]├─[00FF00]/spin [FFFFFF] lak
[B][FF1493]└─[00FF00]/stop
[B][FF1493]──────────────────"""
                            await safe_send_message(response.Data.chat_type, emote_commands, uid, chat_id, key, iv)
                            await asyncio.sleep(0.6)

                            # ───── Box 7: EVO & BUNDLE ─────  
                            evo_commands = """[B][00BFFF]■ EVO & BUNDLE ■
[B][00BFFF]──────────────────
[B][FFD700]EVO SYSTEM
[B][00BFFF]├─[00FF00]/mr [FFFFFF][uids] [num 1-21]
[B][00BFFF]├─[00FF00]/evo_fast [FFFFFF][uids] [num]
[B][00BFFF]├─[00FF00]/dance [FFFFFF][uids] [all] [dacn]
[B][00BFFF]├─[00FF00]@ [FFFFFF][uid] [Evo Cycle]
[B][00BFFF]└─[00FF00]/stop [FFFFFF](Stop Cycle)
[B][00BFFF]──────────────────
[B][FFD700]ANIMATION & MAGIC
[B][00BFFF]├─[00FF00]/animation [FFFFFF][num]
[B][00BFFF]├─[00FF00]/bundle [FFFFFF][num]
[B][00BFFF]├─[00FF00]/b [FFFFFF][name]
[B][00BFFF]├─[00FF00]/magic [FFFFFF][code]
[B][00BFFF]└─[00FF00]/match [FFFFFF] nam name 
[B][00BFFF]──────────────────"""
                            await safe_send_message(response.Data.chat_type, evo_commands, uid, chat_id, key, iv)
                            await asyncio.sleep(0.6)

                            # সবার জন্য একই ফুটার (Developer Info)
                            footer = """[B][4169E1]■ BOT SYSTEM ■
[B][4169E1]──────────────────
[B][FFD700]DEVELOPER INFO
[B][4169E1]├─[FFFFFF]Owner: [FFD700]ARIYAN
[B][4169E1]└─[FFFFFF]TG: @ff_ariyan_bot
[B][4169E1]──────────────────
[B][FF0000]WARNING
[B][4169E1]├─[FFFFFF]Stop Task: [FF0000]/stop
[B][4169E1]└─[FFFFFF]Status: [00FF00]Premium Active
[B][4169E1]──────────────────"""
                            await safe_send_message(response.Data.chat_type, footer, uid, chat_id, key, iv)
                            
                        # =================================================================
                        # ARIYAN LOGO ANIMATION (5 COLORS, 0.2s DELAY)
                        # =================================================================
                        if inPuTMsG.strip().lower() == "ariyan":
                            print(f"Ariyan animation triggered by UID: {uid}")
                            
                            # ব্যাকগ্রাউন্ড টাস্ক যাতে বট ল্যাগ না করে
                            async def ariyan_logo_sequence(c_type, t_uid, c_id, k, v):
                                # ৫টি ভিন্ন ভিন্ন কালার (Cyan, Yellow, Pink, Green, Red)
                                colors = ["[00FFFF]", "[FFFF00]", "[FF00FF]", "[00FF00]", "[FF0000]"]
                                
                                # বেসিক লোগো স্ট্রাকচার (শুধু কালার প্লেসহোল্ডার {c} রাখা হয়েছে)
                                logo_template = """{c} WLC ARIYAN BOT
░█████╗░██████╗░██╗██╗░░░██╗░█████╗░███╗░░██╗
██╔══██╗██╔══██╗██║╚██╗░██╔╝██╔══██╗████╗░██║
███████║██████╔╝██║░╚████╔╝░███████║██╔██╗██║
██╔══██║██╔══██╗██║░░╚██╔╝░░██╔══██║██║╚████║
██║░░██║██║░░██║██║░░░██║░░░██║░░██║██║░╚███║
╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚══╝"""
                                
                                # ৫ বার লুপ চলবে (প্রতিবার ভিন্ন কালার)
                                for color in colors:
                                    colored_logo = logo_template.format(c=color)
                                    await safe_send_message(c_type, colored_logo, t_uid, c_id, k, v)
                                    await asyncio.sleep(0.7) # ০.২ সেকেন্ড ব্রেক
                                    
                            # টাস্কটি চালু করে দেওয়া হলো
                            asyncio.create_task(ariyan_logo_sequence(response.Data.chat_type, uid, chat_id, key, iv))
                            
                        response = None
                            
            whisper_writer.close() ; await whisper_writer.wait_closed() ; whisper_writer = None
                    
        except Exception as e: print(f"ErroR {ip}:{port} - {e}") ; whisper_writer = None
        await asyncio.sleep(reconnect_delay)

# ==============================================================================
#                  SECURITY FUNCTIONS (KILL-SWITCH)
# ==============================================================================
import urllib.request

def show_update_message():
    """Beautiful Neon Maintenance Screen when bot is OFF"""
    os.system('clear' if os.name == 'posix' else 'cls')
    
    C = "\033[96m"   # Cyan
    R = "\033[91m"   # Red
    G = "\033[92m"   # Green
    Y = "\033[93m"   # Yellow
    M = "\033[95m"   # Magenta
    W = "\033[97m"   # White
    RS = "\033[0m"   # Reset

    print(f"\n{R}   ██████████████████████████████████████████████████████████{RS}")
    print(f"{R}   █{Y}             ⚠️ SYSTEM ACCESS REVOKED ⚠️              {R}█{RS}")
    print(f"{R}   ██████████████████████████████████████████████████████████{RS}\n")

    print(f"   {C}╔════════════════════════════════════════════════════════╗{RS}")
    print(f"   {C}║{RS}  {W}The VIP Premium Bot is currently under maintenance or {C}║{RS}")
    print(f"   {C}║{RS}  {W}your access has been disabled by the Developer.       {C}║{RS}")
    print(f"   {C}╠════════════════════════════════════════════════════════╣{RS}")
    print(f"   {C}║{RS}  {Y}✨ NEXT GENERATION UPDATE IS ARRIVING SOON! ✨        {C}║{RS}")
    print(f"   {C}╠════════════════════════════════════════════════════════╣{RS}")
    print(f"   {C}║{RS}  {M}📞 WhatsApp :{RS} {G}{WHATSAPP_LINK[:37]:<37} {C}║{RS}")
    print(f"   {C}║{RS}  {M}✈️ Telegram  :{RS} {G}@{TELEGRAM_LINK:<36} {C}║{RS}")
    print(f"   {C}║{RS}  {M}📱 Number   :{RS} {G}{PHONE_NUMBER:<37} {C}║{RS}")
    print(f"   {C}╚════════════════════════════════════════════════════════╝{RS}\n")
    print(f"   {R}>> EXITED (Error Code: 403 Forbidden) <<{RS}\n")
    os._exit(0)

def check_initial_status():
    """Hacker-style Loading Animation before Checking License"""
    os.system('clear' if os.name == 'posix' else 'cls')
    
    C = "\033[96m"
    G = "\033[92m"
    Y = "\033[93m"
    R = "\033[91m"
    M = "\033[95m"
    RS = "\033[0m"

    print(f"\n  {M}✦{RS} {C}INITIALIZING SECURITY PROTOCOLS...{RS}")

    bar_len = 40
    spinners = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    
    for i in range(101):
        spin = spinners[i % len(spinners)]
        filled = int(bar_len * i / 100)
        bar = '█' * filled + '░' * (bar_len - filled)
        color = R if i < 40 else Y if i < 80 else G

        sys.stdout.write(f"\r  {C}{spin}{RS} Verifying License: {color}[{bar}] {i}%{RS}")
        sys.stdout.flush()
        time.sleep(0.015)

    sys.stdout.write(f"\r  {G}✔ Verifying License: [{'█'*bar_len}] 100%{RS}\n")
    sys.stdout.flush()
    time.sleep(0.5)

    print(f"  {Y}Contacting GITHUB Security Server...{RS}")

    try:
        req = urllib.request.urlopen(GITHUB_STATUS_URL, timeout=10)
        status = req.read().decode('utf-8').strip().lower()

        if status == "off":
            time.sleep(0.8)
            show_update_message()
        elif status == "on":
            print(f"  {G}=================================================={RS}")
            print(f"  {G}✅ ACCESS GRANTED! SERVER IS ONLINE. STARTING...{RS}")
            print(f"  {G}=================================================={RS}")
            time.sleep(1.2)
        else:
            print(f"  {R}✖ Invalid Server Status Response!{RS}")
            os._exit(0)
            
    except Exception as e:
        print(f"\n  {R}✖ CANNOT CONNECT TO SECURITY SERVER: {e}{RS}")
        print(f"  {Y}Please check your internet connection!{RS}\n")
        os._exit(0)

async def background_status_monitor():
    """চলন্ত অবস্থায় ব্যাকগ্রাউন্ডে চেক করবে, এটা সাইলেন্ট থাকবে"""
    while True:
        await asyncio.sleep(STATUS_CHECK_INTERVAL)
        try:
            req = urllib.request.urlopen(GITHUB_STATUS_URL, timeout=10)
            status = req.read().decode('utf-8').strip().lower()
            if status == "off":
                print("\n\n\033[91m[!] ACCESS REVOKED BY ADMIN! SHUTTING DOWN...\033[0m")
                show_update_message()
        except Exception:
            pass


async def MaiiiinE():
    global bot_uid
    
    # Nm.txt se account load karega
    try:
        with open('ARIYAN.txt', 'r') as file:
            data = json.load(file)
            if data:
                # Pehla account uthayega
                Uid = list(data.keys())[0]
                Pw = data[Uid]
                print(f"Loaded Account: {Uid}")
            else:
                print("Error: No account found in ARIYAN.txt")
                return None
    except Exception as e:
        print(f"Error reading ARIYAN.txt: {e}")
        return None
    

    open_id , access_token = await GeNeRaTeAccEss(Uid , Pw)
    if not open_id or not access_token: print("ErroR - InvaLid AccounT") ; return None
    
    PyL = await EncRypTMajoRLoGin(open_id , access_token)
    MajoRLoGinResPonsE = await MajorLogin(PyL)
    if not MajoRLoGinResPonsE: print("TarGeT AccounT => BannEd / NoT ReGisTeReD ! ") ; return None
    
    MajoRLoGinauTh = await DecRypTMajoRLoGin(MajoRLoGinResPonsE)
    UrL = MajoRLoGinauTh.url
    # In the MaiiiinE function, find and comment out these print statements:
    os.system('clear')
    print("🔄 Starting TCP Connections...")
    print("📡 Connecting to Free Fire servers...")
    print("🌐 Server connection established")

    region = MajoRLoGinauTh.region

    ToKen = MajoRLoGinauTh.token
    print("🔐 Authentication successful")
    TarGeT = MajoRLoGinauTh.account_uid
    key = MajoRLoGinauTh.key
    iv = MajoRLoGinauTh.iv
    timestamp = MajoRLoGinauTh.timestamp
    
    LoGinDaTa = await GetLoginData(UrL , PyL , ToKen)
    if not LoGinDaTa: print("ErroR - GeTinG PorTs From LoGin DaTa !") ; return None
    LoGinDaTaUncRypTinG = await DecRypTLoGinDaTa(LoGinDaTa)
    OnLinePorTs = LoGinDaTaUncRypTinG.Online_IP_Port
    ChaTPorTs = LoGinDaTaUncRypTinG.AccountIP_Port
    OnLineiP , OnLineporT = OnLinePorTs.split(":")
    ChaTiP , ChaTporT = ChaTPorTs.split(":")
    acc_name = LoGinDaTaUncRypTinG.AccountName
    #print(acc_name)
    
    equie_emote(ToKen,UrL)
    AutHToKen = await xAuThSTarTuP(int(TarGeT) , ToKen , int(timestamp) , key , iv)
    ready_event = asyncio.Event()
    
    task1 = asyncio.create_task(TcPChaT(ChaTiP, ChaTporT , AutHToKen , key , iv , LoGinDaTaUncRypTinG , ready_event ,region))
    task2 = asyncio.create_task(TcPOnLine(OnLineiP , OnLineporT , key , iv , AutHToKen))  
    task3 = asyncio.create_task(background_status_monitor()) # 🔥 SECURITY MONITORING TASK

    # ==============================================================================
    # 🌟 VIP LIVE DASHBOARD ANIMATION
    # ==============================================================================
    
    # TCP Connection রেডি হওয়ার জন্য অপেক্ষা
    await ready_event.wait()
    await asyncio.sleep(0.5)

    os.system('clear' if os.name == 'posix' else 'cls')

    # 1. Quick Matrix Booting Animation
    C_CYAN = "\033[38;5;51m"
    C_GREEN = "\033[38;5;46m"
    C_YELLOW = "\033[38;5;226m"
    C_MAGENTA = "\033[38;5;213m"
    C_RED = "\033[38;5;196m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    
    boot_texts = [
        "Initializing RAHATNeural Network...",
        "Bypassing Free Fire Security Protocols...",
        "Establishing Secure TCP Socket...",
        "Fetching Account Data & Tokens...",
        "Synchronizing VIP Dashboard..."
    ]
    
    print("\n")
    for text in boot_texts:
        sys.stdout.write(f"\r  {C_CYAN}[{C_MAGENTA}≈{C_CYAN}]{RESET} {C_GREEN}{BOLD}{text}{RESET}")
        sys.stdout.flush()
        await asyncio.sleep(0.4)
        sys.stdout.write("\033[K")
    
    await asyncio.sleep(0.3)
    os.system('clear' if os.name == 'posix' else 'cls')

    # 2. Render Beautiful Logo
    try:
        # If cfonts is installed, use it
        logo = render('ARIYAN', colors=['cyan', 'magenta'], align='center')
        print(logo)
    except Exception:
        # Fallback Neon Logo
        print(f"{C_CYAN}{BOLD}")
        print("       █████╗ ██████╗ ██╗██╗   ██╗█████╗ ███╗   ██╗")
        print("      ██╔══██╗██╔══██╗██║╚██╗ ██╔╝██╔══██╗████╗  ██║")
        print("      ███████║██████╔╝██║ ╚████╔╝ ███████║██╔██╗ ██║")
        print("      ██╔══██║██╔══██╗██║  ╚██╔╝  ██╔══██║██║╚██╗██║")
        print("      ██║  ██║██║  ██║██║   ██║   ██║  ██║██║ ╚████║")
        print("      ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝")
        print(f"{RESET}")

    # 3. Premium Info Box Design
    panel = f"""
    {C_CYAN}╔════════════════════════════════════════════════════════════╗{RESET}
    {C_CYAN}║{RESET}   {BOLD}{C_YELLOW}✨ Ｐ Ｒ Ｅ Ｍ Ｉ Ｕ Ｍ   Ｄ Ａ Ｓ Ｈ Ｂ Ｏ Ａ Ｒ Ｄ ✨{RESET}   {C_CYAN}║{RESET}
    {C_CYAN}╠════════════════════════════════════════════════════════════╣{RESET}
    {C_CYAN}║{RESET}  👤 {BOLD}OWNER/DEV{RESET}  : {C_MAGENTA}𝐀𝐑𝐈𝐘𝐀𝐍 𝐓𝐇𝐄 𝐁𝐎𝐒𝐒{RESET}                      {C_CYAN}║{RESET}
    {C_CYAN}║{RESET}  🆔 {BOLD}BOT UID{RESET}    : {C_GREEN}{str(TarGeT).ljust(41)}{RESET}{C_CYAN}║{RESET}
    {C_CYAN}║{RESET}  📛 {BOLD}BOT NAME{RESET}   : {C_GREEN}{str(acc_name).ljust(41)}{RESET}{C_CYAN}║{RESET}
    {C_CYAN}║{RESET}  🌍 {BOLD}REGION{RESET}     : {C_GREEN}{str(region).upper().ljust(41)}{RESET}{C_CYAN}║{RESET}
    {C_CYAN}║{RESET}  📡 {BOLD}STATUS{RESET}     : {C_GREEN}🟢 ACTIVE & LISTENING{RESET}                    {C_CYAN}║{RESET}
    {C_CYAN}║{RESET}  🔌 {BOLD}CONNECTION{RESET} : {C_GREEN}SECURE TCP SOCKET{RESET}                        {C_CYAN}║{RESET}
    {C_CYAN}╠════════════════════════════════════════════════════════════╣{RESET}
    {C_CYAN}║{RESET}  {BOLD}{C_RED}⚠️  DO NOT CLOSE THIS TERMINAL WHILE BOT IS RUNNING ⚠️{RESET}  {C_CYAN}║{RESET}
    {C_CYAN}╚════════════════════════════════════════════════════════════╝{RESET}
    """
    print(panel)
    print(f"  {BOLD}{C_MAGENTA}✦ System is Live! Waiting for commands in Free Fire... ✦{RESET}\n")

    # 4. Start the infinite tasks
    await asyncio.gather(task1, task2, task3) # 🔥 Task3 (Status monitor) added here


# ==============================================================================
# 🛑 SHUTDOWN & VIP STARTUP ANIMATION ENGINE
# ==============================================================================

def handle_keyboard_interrupt(signum, frame):
    """Clean handling for Ctrl+C"""
    print("\n\n\033[38;5;196m🛑 Bot shutdown requested...\033[0m")
    print("\033[38;5;46m👋 Thanks for using RAHATVIP Engine!\033[0m")
    sys.exit(0)

# Register the signal handler
import signal
signal.signal(signal.SIGINT, handle_keyboard_interrupt)

async def vip_loading_screen():
    """A highly premium dynamic loading screen for startup/retry"""
    C_CYAN = "\033[38;5;51m"
    C_MAGENTA = "\033[38;5;213m"
    C_YELLOW = "\033[38;5;226m"
    C_GREEN = "\033[38;5;46m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"\n{C_CYAN}  ╔════════════════════════════════════════════════════╗{RESET}")
    print(f"{C_CYAN}  ║{RESET}  {BOLD}{C_YELLOW}🚀 ARIYAN'S SUPREME ENGINE IS INITIALIZING...{RESET}     {C_CYAN}║{RESET}")
    print(f"{C_CYAN}  ╚════════════════════════════════════════════════════╝{RESET}\n")
    
    spinners = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    bar_length = 35
    
    # Smooth 0-100% Progress Bar Animation
    for i in range(101):
        spin = spinners[i % len(spinners)]
        filled = '█' * int((i / 100) * bar_length)
        unfilled = '░' * (bar_length - int((i / 100) * bar_length))
        
        sys.stdout.write(f"\r  {C_MAGENTA}{spin}{RESET}  {C_CYAN}{BOLD}LOADING CORE:{RESET} {C_GREEN}[{filled}{unfilled}]{RESET} {C_YELLOW}{i}%{RESET}")
        sys.stdout.flush()
        await asyncio.sleep(0.02) # Ultra-fast smooth loading
        
    print(f"\n\n  {C_GREEN}✔ Core Engine Loaded Successfully!{RESET}")
    print(f"  {C_MAGENTA}✦ Connecting to Data Servers...{RESET}\n")
    await asyncio.sleep(0.8)

async def StarTinG():
    global error_shown
    error_shown = False # Make sure it's initialized
    
    while True:
        try:
            await asyncio.wait_for(MaiiiinE(), timeout=7 * 60 * 60)

        except KeyboardInterrupt:
            print("\n\n\033[38;5;196m🛑 Bot shutdown by user\033[0m")
            print("\033[38;5;46m👋 Thanks for using ARIYAN!\033[0m")
            break

        except asyncio.TimeoutError:
            print("\n\033[38;5;226mToken Expired! Restarting Engine...\033[0m")

        except Exception as e:
            if not error_shown:
                await vip_loading_screen()
                error_shown = True
            else:
                await asyncio.sleep(2)


if __name__ == '__main__':
    # 🔥 Check permission from GitHub first (Kill-Switch)
    check_initial_status()
    
    # 🔥 Start the bot engine
    asyncio.run(StarTinG())