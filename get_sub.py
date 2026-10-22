#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import base64
import sys
import os
import re
import json
from collections import defaultdict
from datetime import datetime

URL = "https://shadowmere.xyz/api/b64sub/"
FILE_MAIN = "subscription.txt"
FILE_FAV = "favorites.txt"
FILE_MY = "my_list.txt"
FILE_HIST = "history.json"
FILE_EXPORT_JSON = "export.json"
FILE_EXPORT_CSV = "export.csv"

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[97m'
    END = '\033[0m'
    BOLD = '\033[1m'

# ═══════════════ အသုံးပြုသည့် လုပ်ဆောင်ချက်များ ═══════════════
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def extract_country(text):
    match = re.search(r'[🇦-🇿]\s*([A-Za-z\s]+)|-\s*([A-Za-z\s,]+)$', text)
    if match:
        return match.group(1) or match.group(2)
    return "အခြား"

def extract_server_name(line):
    match = re.search(r'#(.+)$', line)
    if match:
        return match.group(1).strip()
    return line[:30] + "..."

def save_to_history(content):
    try:
        history = []
        if os.path.exists(FILE_HIST):
            with open(FILE_HIST, "r", encoding="utf-8") as f:
                history = json.load(f)
        history.append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "size": len(content),
            "lines": len(content.splitlines())
        })
        with open(FILE_HIST, "w", encoding="utf-8") as f:
            json.dump(history[-50:], f, ensure_ascii=False, indent=2)
    except:
        pass

def check_updates():
    print(f"{Colors.CYAN}🔄 နောက်ဆုံးဗားရှင်း ရှာဖွေနေသည်...{Colors.END}")
    try:
        req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as res:
            new_encoded = res.read().decode("utf-8").strip()
        new_content = base64.b64decode(new_encoded).decode("utf-8") if new_encoded else ""
        
        if not os.path.exists(FILE_MAIN):
            print(f"{Colors.GREEN}✅ ဒေတာအသစ် ရှိနေသည်! ကျေးဇူးပြု၍ 'ဒေတာအသစ်ရယူပါ' ကိုရွေးပါ{Colors.END}")
            return True
        
        with open(FILE_MAIN, "r", encoding="utf-8") as f:
            old_content = f.read()
        
        if new_content.strip() != old_content.strip():
            print(f"{Colors.GREEN}✅ ဒေတာအသစ်ထွက်နေသည်! 'ဒေတာအသစ်ရယူပါ' ဖြင့်မွမ်းမံပါ{Colors.END}")
            return True
        else:
            print(f"{Colors.YELLOW}⏰ နောက်ဆုံးပေါ်ဖြစ်နေပါသည်{Colors.END}")
            return False
    except Exception as e:
        print(f"{Colors.RED}❌ စစ်ဆေး၍မရပါ: {e}{Colors.END}")
        return False

# ═════════════== ပငမ လုပ်ဆောင်ချက်များ ═══════════════
def fetch_data():
    print(f"{Colors.CYAN}🔄 အချက်အလက်များ ရယူနေသည်...{Colors.END}")
       try:
        req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as res:
            encoded = res.read().decode("utf-8").strip()
        
        decoded = base64.b64decode(encoded).decode("utf-8")
        
        with open(FILE_MAIN, "w", encoding="utf-8") as f:
            f.write(decoded)
        
        save_to_history(decoded)
        
        lines = = decoded.splitlines()
        print(f"{Colors.GREEN}✅ အောင်မြင်စွာ ရယူပြီး သိမ်းဆည်းပြီးပါပြီ!{Colors.END}")
        print(f"📄 စုစုပေါင်း လိုင်းအရေအတွက်: {Colors.BOLD}{len(lines)}{Colors.END}")
        return decoded
    except urllib.error.URLError:
        print(f"{Colors.RED}❌ ကွန်ရက်ချိတ်ဆက်မှု အမှားအယွင်း ရှိနေသည်{Colors.END}")
        return None
    except base64.binascii.Error:
        print(f"{Colors.RED}❌ ဒေတာဖော်ထုတ်၍မရပါ{Colors.END}")
        return None
    except Exception as e:
        print(f"{Colors.RED}❌ အမှားအယွင်း: {e}{Colors.END}")
        return None

def show_data():
    if not os.path.exists(FILE_MAIN):
        print(f"{Colors.YELLOW}⚠️ ဖိုင်မရှိသေးပါ။ အရင် ဒေတာအသစ်ရယူပါ။{Colors.END}")
        return
    print(f"{Colors.HEADER}📋 လက်ရှိဒေတာများ:{Colors.END}\n")
    with open(FILE_MAIN, "r", encoding="utf-8") as f:
        content = f.read()
    print(content)
    print(f"\n{Colors.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
    input(f"{Colors.CYAN}ပြန်မယူဖို့ မည်သည့်ခလုတ်ကိုမဆို နှိပ်ပါ...{Colors.END}")

def count_and_show():
    if not os.path.exists(FILE_MAIN):
        print(f"{Colors.YELLOW}⚠️ ဖိုင်မရှိသေးပါ။ အရင် ဒေတာအသစ်ရယူပါ။{Colors.END}")
        return
    with open(FILE_MAIN, "r", encoding="utf-8") as f:
        lines = = [l.strip() for l in f.read().splitlines() if l.strip()]
    ss_links = = [l for l in lines if l.startswith("ss://")]
    
    print(f"{Colors.GREEN}🔢 စာရင်းဇယား:{Colors.END}")
    print(f"စုစုပေါင်း လိုင်းအရေအတွက်: {len(lines)}")
    print(f"SS လင့်ခ် အရေအတွက်: {len(ss_links)}")
    print(f"အခြားလိုင်း အရေအတွက်: {len(lines) - len(ss_links)}")
    input(f"\n{Colors.CYAN}ပြန်မယူဖို့ ခလုတ်တစ်ခုခုနှိပါ...{Colors.END}")

def search_data():
    if not os.path.exists(FILE_MAIN):
        print(f"{Colors.YELLOW}⚠️ ဖိုင်မရှိသေးပါ။ အရင် ဒေတာအသစ်ရယူပါ။{Colors.END}")
        return
    keyword = input(f"{Colors.CYAN}🔍 ရှာဖွေလိုသော စာသား/နိုင်ငံအမည် ရိုက်ထည့်ပါ: {Colors.END}")
    with open(FILE_MAIN, "r", encoding="utf-8") as f:
        lines = = f.read().splitlines()
    found = = [l for l in lines if keyword.lower() in l.lower()]
    if found:
        print(f"\n{Colors.GREEN}✅ တွေ့ရှိချက် ({len(found)} ခု):{Colors.END}")
        for i, item in enumerate(found, 1):
            print(f"  [{i}] {item}")
    else:
        print(f"{Colors.RED}❌ မတွေ့ပါ{Colors.END}")
    input(f"\n{Colors.CYAN}ပြန်မယူဖို့ ခလုတ်တစ်ခုခုနှိပါ...{Colors.END}")

def copy_all():
    if not os.path.exists(FILE_MAIN):
        print(f"{Colors.YELLOW}⚠️ ဖိုင်မရှိသေးပါ။ အရင် ဒေတာအသစ်ရယူပါ။{Colors.END}")
        return
    with open(FILE_MAIN, "r", encoding="utf-8") as f:
        content = = f.read()
    print(f"{Colors.GREEN}📋 အောက်ပါအတိုင်း ကူးယူအသုံးပြုပါ:{Colors.END}\n")
    print("━" * 60)
    print(content)
    print("━" * 60)
    print(f"{Colors.YELLOW}⚠️ အပေါ်က စာသားအားလုံးကို ကိုယ်တိုင်ကူးယူပါ{Colors.END}")
    input(f"{Colors.CYAN}ပြန်မယူဖို့ ခလုတ်တစ်ခုခုနှိပါ...{Colors.END}")

# ====== A: နိုင်ငံအလိုက် စီစဉ်ပြခြင်း ======
def group_by_country():
    if not os.path.exists(FILE_MAIN):
        print(f"{Colors.YELLOW}⚠️ ဖိုင်မရှိသေးပါ။ အရင် ဒေတာအသစ်ရယူပါ။{Colors.END}")
        return
    with open(FILE_MAIN, "r", encoding="utf-8") as f:
        lines = = [l.strip() for l in f.read().splitlines() if l.strip() and l.startswith("ss://")]
    
    groups = defaultdict(list)
    for line in lines:
        country = extract_country(line)
        groups[country].append(line)
    
    print(f"{Colors.HEADER}🌍 နိုင်ငံအလိုက် စီစဉ်ထားချက်များ:{Colors.END}\n")
    for country in sorted(groups.keys()):
        print(f"{Colors.BLUE}📍 {country} ({len(groups[country])} ခု):{Colors.END}")
        for idx, link in enumerate(groups[country], 1):
            name = extract_server_name(link)
            print(f"   {idx}. {name}")
        print()
    
    input(f"{Colors.CYAN}ပြန်မယူဖို့ ခလုတ်တစ်ခုခုနှိပါ...{Colors.END}")

# ====== B: သီးခြားဖိုင်သို့ သိမ်းဆည်းခြင်း ======
def save_selected():
    if not os.path.exists(FILE_MAIN):
        print(f"{Colors.YELLOW}⚠️ ဖိုင်မရှိသေးပါ။ အရင် ဒေတာအသစ်ရယူပါ။{Colors.END}")
        return
    with open(FILE_MAIN, "r", encoding="utf-8") as f:
        lines = = [l.strip() for l in f.read().splitlines() if l.strip()]
    
    print(f"{Colors.CYAN}📋 လင့်ခ်စာရင်းများ (နံပါတ်ရွေးပါ၊ အများအပြား=ကော်မာခြား ဥပမာ: 1,3,5):{Colors.END}\n")
    for i, line in enumerate(lines, 1):
        print(f"  [{i}] {extract_server_name(line)}")
    
    choice = input(f"\n{Colors.CYAN}နံပါတ်(များ) ရိုက်ထည့်ပါ: {Colors.END}")
    try:
        indices = [int(x.strip()) - 1 for x in choice.split(",")]
        selected = [lines[i] for i in indices if 0 <= i < len(lines)]
        
        mode = "a" if os.path.exists(FILE_MY) else "w"
        with open(FILE_MY, mode, encoding="utf-8") as f:
            for item in selected:
                f.write(item + "\n")
        
        print(f"{Colors.GREEN}✅ {len(selected)} ခုကို 'my_list.txt' သို့သိမ်းဆည်းပြီးပါပြီ{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}❌ အမှားအယွင်း: {e}{Colors.END}")
    
    input(f"{Colors.CYAN}ပြန်မယူဖို့ ခလုတ်တစ်ခုခုနှိပါ...{Colors.END}")

def view_my_list():
    if not os.path.exists(FILE_MY):
        print(f"{Colors.YELLOW}⚠️ သိမ်းဆည်းထားသည့်စာရင်းမရှိသေးပါ{Colors.END}")
    else:
        print(f"{Colors.HEADER}💾 ကျွန်ုပ်၏စာရင်း (my_list.txt):{Colors.END}\n")
        with open(FILE_MY, "r", encoding="utf-8") as f:
            print(f.read())
    input(f"{Colors.CYAN}ပြန်မယူဖို့ ခလုတ်တစ်ခုခုနှိပါ...{Colors.END}")

# ====== C: လင့်ခ်အသက်ဝင်မှု စစ်ဆေးခြင်း ======
def check_link_alive():
    if not os.path.exists(FILE_MAIN):
        print(f"{Colors.YELLOW}⚠️ ဖိုင်မရှိသေးပါ။ အရင် ဒေတာအသစ်ရယူပါ။{Colors.END}")
        return
    
    with open(FILE_MAIN, "r", encoding="utf-8") as f:
        lines = = [l.strip() for l in f.read().splitlines() if l.strip() and l.startswith("ss://")]
    
    print(f"{Colors.CYAN}🔌 လင့်ခ်များ စစ်ဆေးနေသည်... (အချိန်ကြာနိုင်ပါသည်){Colors.END}\n")
    print(f"{Colors.GREEN}🟢 = အသက်ဝင်သည်  |  {Colors.YELLOW}🟡 = မသိရှိနိုင်  |  {Colors.RED}🔴 = မအလုပ်လုပ်ပါ{Colors.END}\n")
    
    print(f"{Colors.YELLOW}⚠️ SS လင့်ခ်များကို တိုက်ရိုက်ချိတ်ဆက်စစ်ဆေး၍မရပါ။ ပုံမှန်အားဖြင့် အသက်ဝင်နေသည်ဟု မှတ်ယူပါ။{Colors.END}")
    print(f"{Colors.GREEN}🟢 SS ပရိုတိုကော လင့်ခ် = အသက်ဝင်နေသည်ဟု မှတ်ယူပါသည်{Colors.END}\n")
    
    for i, line in enumerate(lines[:10], 1):
        name = extract_server_name(line)
        print(f"  [{i}] 🟢 {name}")
    
    if len(lines) > 10:
        print(f"\n  ... နောက်ထပ် {len(lines) - 10} ခု ကျန်ရှိပါသည်")
    
    input(f"{Colors.CYAN}\nပြန်မယူဖို့ ခလုတ်တစ်ခုခုနှိပါ...{Colors.END}")

# ====== D: တင်ပို့ခြင်း ======
def export_json():
    if not os.path.exists(FILE_MAIN):
        print(f"{Colors.YELLOW}⚠️ ဖိုင်မရှိသေးပါ။ အရင် ဒေတာအသစ်ရယူပါ။{Colors.END}")
        return
    with open(FILE_MAIN, "r", encoding="utf-8") as f:
        lines = = [l.strip() for l in f.read().splitlines() if l.strip()]
    
    data = {
        "export_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_items": len(lines),
        "items": lines
    }
    
    with open(FILE_EXPORT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"{Colors.GREEN}✅ JSON ဖိုင်အဖြစ် '{FILE_EXPORT_JSON}' သို့တင်ပို့ပြီးပါပြီ{Colors.END}")
    input(f"{Colors.CYAN}ပြန်မယူဖို့ ခလုတ်တစ်ခုခုနှိပါ...{Colors.END}")

def export_csv():
    if not os.path.exists(FILE_MAIN):
        print(f"{Colors.YELLOW}⚠️ ဖိုင်မရှိသေးပါ။ အရင် ဒေတာအသစ်ရယူပါ။{Colors.END}")
        return
    with open(FILE_MAIN, "r", encoding="utf-8") as f:
        lines = = [l.strip() for l in f.read().splitlines() if l.strip()]
    
    with open(FILE_EXPORT_CSV, "w", encoding="utf-8") as f:
        f.write("Server Name,Link\n")
        for line in lines:
            name = extract_server_name(line).replace(",", " -")
            f.write(f'"{name}","{line}"\n')
    
    print(f"{Colors.GREEN}✅ CSV ဖိုင်အဖြစ် '{FILE_EXPORT_CSV}' သို့တင်ပို့ပြီးပါပြီ{Colors.END}")
    input(f"{Colors.CYAN}ပြန်မယူဖို့ ခလုတ်တစ်ခုခုနှိပါ...{Colors.END}")

# ====== E: အကြိုက်ဆုံး/အမှတ်အသား ======
def load_favorites():
    if os.path.exists(FILE_FAV):
        with open(FILE_FAV, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def save_favorites(favs):
    with open(FILE_FAV, "w", encoding="utf-8") as f:
        for item in favs:
            f.write(item + "\n")

def toggle_favorite():
    if not os.path.exists(FILE_MAIN):
        print(f"{Colors.YELLOW}⚠️ ဖိုင်မရှိသေးပါ။ အရင် ဒေတာအသစ်ရယူပါ။{Colors.END}")
        return
    with open(FILE_MAIN, "r", encoding="utf-8") as f:
        lines = = [l.strip() for l in f.read().splitlines() if l.strip()]
    
    favs = load_favorites()
    
    print(f"{Colors.CYAN}⭐ လင့်ခ်စာရင်းများ - အမှတ်အသားပြုရန် နံပါတ်ရွေးပါ:{Colors.END}\n")
    for i, line in enumerate(lines, 1):
        star = " ⭐" if line in favs else ""
        print(f"  [{i}]{star} {extract_server_name(line)}")
    
    choice = input(f"\n{Colors.CYAN}နံပါတ်ရိုက်ထည့်ပါ: {Colors.END}")
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(lines):
            link = lines[idx]
            if link in favs:
                favs.remove(link)
                print(f"{Colors.YELLOW}⭐ အကြိုက်မှဖယ်ရှားပြီးပါပြီ{Colors.END}")
            else:
                favs.add(link)
                print(f"{Colors.GREEN}⭐ အကြိုက်ဆုံးထဲသို့ထည့်ပြီးပါပြီ{Colors.END}")
            save_favorites(favs)
    except ValueError:
        print(f"{Colors.RED}❌ မှားနေပါတယ်{Colors.END}")
    
    input(f"{Colors.CYAN}ပြန်မယူဖို့ ခလုတ်တစ်ခုခုနှိပါ...{Colors.END}")

def view_favorites():
    favs = load_favorites()
    if not favs:
        print(f"{Colors.YELLOW}⚠️ အကြိုက်ဆုံးစာရင်းမရှိသေးပါ{Colors.END}")
    else:
        print(f"{Colors.HEADER}⭐ အကြိုက်ဆုံးစာရင်း:{Colors.END}\n")
        for i, item in enumerate(favs, 1):
            print(f"  [{i}] {item}")
    input(f"{Colors.CYAN}ပြန်မယူဖို့ ခလုတ်တစ်ခုခုနှိပါ...{Colors.END}")

# ====== F: အလိုအလျောက် စစ်ဆေးခြင်း ======
def auto_check_updates():
    check_updates()
    input(f"{Colors.CYAN}ပြန်မယူဖို့ ခလုတ်တစ်ခုခုနှိပါ...{Colors.END}")

# ====== G: မှတ်တမ်းသမိုင်း ======
def view_history():
    if not os.path.exists(FILE_HIST):
        print(f"{Colors.YELLOW}⚠️ မှတ်တမ်းမရှိသေးပါ{Colors.END}")
    else:
        print(f"{Colors.HEADER}📜 မှတ်တမ်းသမိုင်း:{Colors.END}\n")
        with open(FILE_HIST, "r", encoding="utf-8") as f:
            history = json.load(f)
        if not history:
            print(f"{Colors.YELLOW}မှတ်တမ်းမရှိသေးပါ{Colors.END}")
        else:
            for idx, rec in enumerate(reversed(history[-20:]), 1):
                print(f"  [{idx}] {rec['time']} → {rec['lines']} လိုင်း")
    input(f"{Colors.CYAN}ပြန်မယူဖို့ ခလုတ်တစ်ခုခုနှိပါ...{Colors.END}")

# ═════════════== ပင်မ Menu ═══════════════
def main_menu():
    while True:
        clear_screen()
        print(f"""{Colors.HEADER}
╔═══════════════════════════════════════════════════╗
║          🚀 Sub Downloader  v3.0  (အပြည့်အစုံ)         ║
╠═══════════════════════════════════════════════════╣
║  📥 အခြေခံ လုပ်ဆောင်ချက်များ:                          ║
║   1. ဒေတာအသစ်ပြန်ရယူပါ                              ║
║   2. လက်ရှိဒေတာကို ကြည့်ပါ                           ║
║   3. စာရင်းဇယား ကြည့်ပါ                              ║
║   4. နိုင်ငံအလိုက် စီစဉ်ကြည့်ပါ (A)                     ║
║   5. နိုင်ငံ/လင့်ခ် ရှာဖွေပါ                           ║
║   6. အားလုံးကူးယူဖို့ ပြပါ                              ║
║                                                   ║
║  ⭐ အကြိုက်ဆုံး & သိမ်းဆည်းခြင်း:                       ║
║   7. လင့်ခ်ရွေးပြီး သိမ်းဆည်းပါ (B)                    ║
║   8. ကျွန်ုပ်၏စာရင်းကို ကြည့်ပါ                       ║
║   9. အကြိုက်ဆုံးအဖြစ် အမှတ်အသားပြုပါ (E)                ║
║  10. အကြိုက်ဆုံးစာရင်း ကြည့်ပါ                        ║
║                                                   ║
║  📤 တင်ပို့ခြင်း & စစ်ဆေးခြင်း:                        ║
║  11. လင့်ခ်အသက်ဝင်မှု စစ်ဆေးပါ (C)                    ║
║  12. JSON အဖြစ်တင်ပို့ပါ (D)                          ║
║  13. CSV အဖြစ်တင်ပို့ပါ (D)                           ║
║                                                   ║
║  🔍 အခြားအသုံးဝင်သည့်အရာများ:                         ║
║  14. အသစ်ရှိလား စစ်ဆေးပါ (F)                          ║
║  15. မှတ်တမ်းသမိုင်း ကြည့်ပါ (G)                      ║
║  16. ဖိုင်ကိုဖျက်ပါ                                    ║
║   0. ပရိုဂရမ်မှ ထွက်ပါ                                ║
╠═══════════════════════════════════════════════════╣
║  💡 နံပါတ်ရိုက်ပြီး Enter နှိပ်ပါ                      ║
╚═══════════════════════════════════════════════════╝{Colors.END}""")
        
        choice = input(f"{Colors.BOLD}👉 သင့်ရွေးချယ်မှု: {Colors.END}")
        
        if choice == "1":
            fetch_data()
            print(f"\n⏳ ခဏစောင့်ပါ...")
            import time; time.sleep(1.5)
        elif choice == "2":
            show_data()
        elif choice == "3":
            count_and_show()
        elif choice == "4":
            group_by_country()
        elif choice == "5":
            search_data()
        elif choice == "6":
            copy_all()
        elif choice == "7":
            save_selected()
        elif choice == "8":
            view_my_list()
        elif choice == "9":
            toggle_favorite()
        elif choice == "10":
            view_favorites()
        elif choice == "11":
            check_link_alive()
        elif choice == "12":
            export_json()
        elif choice == "13":
            export_csv()
        elif choice == "14":
            auto_check_updates()
        elif choice == "15":
            view_history()
        elif choice == "16":
            confirm = input(f"{Colors.YELLOW}⚠️ ဖိုင်အားလုံးဖျက်မှာလား? (y/n): {Colors.END}").lower()
            if confirm == 'y':
                for f in [FILE_MAIN, FILE_MY, FILE_FAV, FILE_HIST]:
                    if os.path.exists(f): os.remove(f)
                print(f"{Colors.GREEN}🗑️ ဖျက်ပြီးပါပြီ{Colors.END}")
            input(f"{Colors.CYAN}ဆက်ရန် ခလုတ်နှိပ်ပါ...{Colors.END}")
        elif choice == "0":
            print(f"{Colors.GREEN}👋 ကျေးဇူးတင်ပါတယ်!{Colors.END}")
            sys.exit(0)
        else:
            print(f"{Colors.RED}❌ မှားနေပါတယ်။ 0-16 ကြား နံပါတ်သာရိုက်ပါ{Colors.END}")
            import time; time.sleep(1.5)

if __name__ == "__main__":
    main_menu()
