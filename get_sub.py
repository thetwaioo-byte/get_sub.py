#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import base64
import sys
import os
import re
import json
import time
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
    BLACK = '\033[30m'
    WHITE = '\033[97m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    GRAY = '\033[90m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    REVERSE = '\033[7m'
    END = '\033[0m'

class Styles:
    LINE_TOP = "╔" + "═" * 38 + "╗"
    LINE_MID = "╠" + "═" * 38 + "╣"
    LINE_BOT = "╚" + "═" * 38 + "╝"
    PIPE = "║"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    print(f"\n{Colors.MAGENTA}{Styles.LINE_TOP}{Colors.END}")
    print(f"{Colors.MAGENTA}{Styles.PIPE}{Colors.BOLD}{Colors.CYAN}  ✨ {title.ljust(34)}{Colors.END}{Colors.MAGENTA}{Styles.PIPE}{Colors.END}")
    print(f"{Colors.MAGENTA}{Styles.LINE_MID}{Colors.END}")

def print_footer():
    print(f"{Colors.MAGENTA}{Styles.LINE_BOT}{Colors.END}\n")

def extract_country(text):
    match = re.search(r'#([A-Za-z\s,]+)$', text)
    if match:
        return match.group(1).strip()
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
    except Exception:
        pass

def check_updates():
    print_header("အသစ်ရှိမှု စစ်ဆေးခြင်း")
    print(f"{Styles.PIPE}  {Colors.CYAN}🔄 နောက်ဆုံးဗားရှင်း ရှာဖွေနေသည်...{Colors.END}".ljust(40) + Styles.PIPE)
    try:
        req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as res:
            new_encoded = res.read().decode("utf-8").strip()
        new_content = base64.b64decode(new_encoded).decode("utf-8") if new_encoded else ""
        
        if not os.path.exists(FILE_MAIN):
            print(f"{Styles.PIPE}  {Colors.GREEN}✅ ဒေတာအသစ် ရှိနေသည်! 'ဒေတာအသစ်ရယူပါ' ကိုရွေးပါ{Colors.END}".ljust(40) + Styles.PIPE)
            print_footer()
            return True
        
        with open(FILE_MAIN, "r", encoding="utf-8") as f:
            old_content = f.read()
        
        if new_content.strip() != old_content.strip():
            print(f"{Styles.PIPE}  {Colors.GREEN}✨ ဒေတာအသစ်ထွက်နေသည်! မွမ်းမံပါ{Colors.END}".ljust(40) + Styles.PIPE)
        else:
            print(f"{Styles.PIPE}  {Colors.YELLOW}⏰ နောက်ဆုံးပေါ်ဖြစ်နေပါသည်{Colors.END}".ljust(40) + Styles.PIPE)
    except Exception as e:
        print(f"{Styles.PIPE}  {Colors.RED}❌ စစ်ဆေး၍မရပါ: {e}{Colors.END}".ljust(40) + Styles.PIPE)
    print_footer()

def fetch_data():
    print_header("ဒေတာ ရယူခြင်း")
    print(f"{Styles.PIPE}  {Colors.CYAN}🔄 အချက်အလက်များ ရယူနေသည်...{Colors.END}".ljust(40) + Styles.PIPE)
    try:
        req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as res:
            encoded = res.read().decode("utf-8").strip()
        
        decoded = base64.b64decode(encoded).decode("utf-8")
        
        with open(FILE_MAIN, "w", encoding="utf-8") as f:
            f.write(decoded)
        
        save_to_history(decoded)
        
        lines = decoded.splitlines()
        print(f"{Styles.PIPE}  {Colors.GREEN}✅ အောင်မြင်စွာ ရယူပြီးပါပြီ!{Colors.END}".ljust(40) + Styles.PIPE)
        print(f"{Styles.PIPE}  {Colors.CYAN}📄 စုစုပေါင်း လိုင်းအရေအတွက်: {Colors.BOLD}{len(lines)}{Colors.END}".ljust(40) + Styles.PIPE)
    except urllib.error.URLError:
        print(f"{Styles.PIPE}  {Colors.RED}❌ ကွန်ရက်ချိတ်ဆက်မှု အမှားအယွင်း{Colors.END}".ljust(40) + Styles.PIPE)
    except base64.binascii.Error:
        print(f"{Styles.PIPE}  {Colors.RED}❌ ဒေတာဖော်ထုတ်၍မရပါ{Colors.END}".ljust(40) + Styles.PIPE)
    except Exception as e:
        print(f"{Styles.PIPE}  {Colors.RED}❌ အမှားအယွင်း: {e}{Colors.END}".ljust(40) + Styles.PIPE)
    print_footer()

def show_data():
    print_header("လက်ရှိဒေတာများ")
    if not os.path.exists(FILE_MAIN):
        print(f"{Styles.PIPE}  {Colors.YELLOW}⚠️ ဖိုင်မရှိသေးပါ။ အရင် ဒေတာအသစ်ရယူပါ။{Colors.END}".ljust(40) + Styles.PIPE)
    else:
        print(f"{Styles.PIPE}  {Colors.WHITE}အောက်တွင် ဒေတာများကို ကြည့်ရှုနိုင်ပါသည်-{Colors.END}".ljust(40) + Styles.PIPE)
        print(f"{Styles.LINE_MID}")
        with open(FILE_MAIN, "r", encoding="utf-8") as f:
            content = f.read()
        print(content)
    print_footer()
    input(f"{Colors.CYAN}⏎ ပြန်မယူဖို့ မည်သည့်ခလုတ်ကိုမဆို နှိပ်ပါ...{Colors.END}")

def count_and_show():
    print_header("စာရင်းဇယား")
    if not os.path.exists(FILE_MAIN):
        print(f"{Styles.PIPE}  {Colors.YELLOW}⚠️ ဖိုင်မရှိသေးပါ။ အရင် ဒေတာအသစ်ရယူပါ။{Colors.END}".ljust(40) + Styles.PIPE)
    else:
        with open(FILE_MAIN, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f.read().splitlines() if l.strip()]
        ss_links = [l for l in lines if l.startswith("ss://")]
        
        print(f"{Styles.PIPE}  {Colors.CYAN}📊 စုစုပေါင်း လိုင်းအရေအတွက်: {Colors.BOLD}{len(lines)}{Colors.END}".ljust(40) + Styles.PIPE)
        print(f"{Styles.PIPE}  {Colors.GREEN}🔗 SS လင့်ခ် အရေအတွက်:   {Colors.BOLD}{len(ss_links)}{Colors.END}".ljust(40) + Styles.PIPE)
        print(f"{Styles.PIPE}  {Colors.BLUE}📝 အခြားလိုင်း အရေအတွက်:   {Colors.BOLD}{len(lines) - len(ss_links)}{Colors.END}".ljust(40) + Styles.PIPE)
    print_footer()
    input(f"{Colors.CYAN}⏎ ပြန်မယူဖို့ ခလုတ်တစ်ခုခုနှိပါ...{Colors.END}")

def search_data():
    print_header("ရှာဖွေခြင်း")
    if not os.path.exists(FILE_MAIN):
        print(f"{Styles.PIPE}  {Colors.YELLOW}⚠️ ဖိုင်မရှိသေးပါ။ အရင် ဒေတာအသစ်ရယူပါ။{Colors.END}".ljust(40) + Styles.PIPE)
        print_footer()
        return
    keyword = input(f"{Styles.PIPE}  {Colors.CYAN}🔍 ရှာဖွေလိုသော စာသား/နိုင်ငံအမည်: {Colors.END}")
    with open(FILE_MAIN, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    found = [l for l in lines if keyword.lower() in l.lower()]
    
    if found:
        print(f"{Styles.PIPE}  {Colors.GREEN}✅ တွေ့ရှိချက် ({len(found)} ခု):{Colors.END}".ljust(40) + Styles.PIPE)
        for i, item in enumerate(found, 1):
            short = item[:35] + "..." if len(item) > 35 else item
            print(f"{Styles.PIPE}     {Colors.WHITE}[{i}] {short}{Colors.END}".ljust(40) + Styles.PIPE)
    else:
        print(f"{Styles.PIPE}  {Colors.RED}❌ မတွေ့ပါ{Colors.END}".ljust(40) + Styles.PIPE)
    print_footer()
    input(f"{Colors.CYAN}⏎ ပြန်မယူဖို့ ခလုတ်တစ်ခုခုနှိပါ...{Colors.END}")

def copy_all():
    print_header("ကူးယူခြင်း")
    if not os.path.exists(FILE_MAIN):
        print(f"{Styles.PIPE}  {Colors.YELLOW}⚠️ ဖိုင်မရှိသေးပါ။ အရင် ဒေတာအသစ်ရယူပါ။{Colors.END}".ljust(40) + Styles.PIPE)
    else:
        print(f"{Styles.PIPE}  {Colors.GREEN}📋 အောက်ပါအတိုင်း ကူးယူအသုံးပြုပါ-{Colors.END}".ljust(40) + Styles.PIPE)
        print(f"{Styles.LINE_MID}")
        with open(FILE_MAIN, "r", encoding="utf-8") as f:
            print(f.read())
        print(f"{Styles.LINE_MID}")
        print(f"{Styles.PIPE}  {Colors.YELLOW}⚠️ ကိုယ်တိုင်ကူးယူပါ{Colors.END}".ljust(40) + Styles.PIPE)
    print_footer()
    input(f"{Colors.CYAN}⏎ ပြန်မယူဖို့ ခလုတ်တစ်ခုခုနှိပါ...{Colors.END}")

def group_by_country():
    print_header("နိုင်ငံအလိုက် စီစဉ်ခြင်း")
    if not os.path.exists(FILE_MAIN):
        print(f"{Styles.PIPE}  {Colors.YELLOW}⚠️ ဖိုင်မရှိသေးပါ။ အရင် ဒေတာအသစ်ရယူပါ။{Colors.END}".ljust(40) + Styles.PIPE)
        print_footer()
        return
    with open(FILE_MAIN, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f.read().splitlines() if l.strip() and l.startswith("ss://")]
    
    groups = defaultdict(list)
    for line in lines:
        country = extract_country(line)
        groups[country].append(line)
    
    for country in sorted(groups.keys()):
        print(f"{Styles.PIPE}  {Colors.BLUE}🌍 {country} ({len(groups[country])} ခု):{Colors.END}".ljust(40) + Styles.PIPE)
        for idx, link in enumerate(groups[country], 1):
            name = extract_server_name(link)
            print(f"{Styles.PIPE}     {Colors.WHITE}{idx}. {name}{Colors.END}".ljust(40) + Styles.PIPE)
    print_footer()
    input(f"{Colors.CYAN}⏎ ပြန်မယူဖို့ ခလုတ်တစ်ခုခုနှိပါ...{Colors.END}")

def save_selected():
    print_header("ရွေးချယ်၍ သိမ်းဆည်းခြင်း")
    if not os.path.exists(FILE_MAIN):
        print(f"{Styles.PIPE}  {Colors.YELLOW}⚠️ ဖိုင်မရှိသေးပါ။ အရင် ဒေတာအသစ်ရယူပါ။{Colors.END}".ljust(40) + Styles.PIPE)
        print_footer()
        return
    with open(FILE_MAIN, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f.read().splitlines() if l.strip()]
    
    print(f"{Styles.PIPE}  {Colors.CYAN}📋 ရရှိနိုင်သောလင့်ခ်များ:{Colors.END}".ljust(40) + Styles.PIPE)
    for i, line in enumerate(lines, 1):
        name = extract_server_name(line)
        print(f"{Styles.PIPE}     {Colors.WHITE}[{i}] {name}{Colors.END}".ljust(40) + Styles.PIPE)
    
    choice = input(f"\n{Styles.PIPE}  {Colors.CYAN}နံပါတ်(များ) ရိုက်ထည့်ပါ (ကော်မာခြား): {Colors.END}")
    try:
        indices = [int(x.strip()) - 1 for x in choice.split(",")]
        selected = [lines[i] for i in indices if 0 <= i < len(lines)]
        
        mode = "a" if os.path.exists(FILE_MY) else "w"
        with open(FILE_MY, mode, encoding="utf-8") as f:
            for item in selected:
                f.write(item + "\n")
        
        print(f"{Styles.PIPE}  {Colors.GREEN}✅ {len(selected)} ခုကို my_list.txt သို့သိမ်းဆည်းပြီးပါပြီ{Colors.END}".ljust(40) + Styles.PIPE)
    except Exception as e:
        print(f"{Styles.PIPE}  {Colors.RED}❌ အမှားအယွင်း: {e}{Colors.END}".ljust(40) + Styles.PIPE)
    print_footer()
    input(f"{Colors.CYAN}⏎ ပြန်မယူဖို့ ခလုတ်တစ်ခုခုနှိပါ...{Colors.END}")

def view_my_list():
    print_header("ကျွန်ုပ်၏စာရင်း")
    if not os.path.exists(FILE_MY):
        print(f"{Styles.PIPE}  {Colors.YELLOW}⚠️ သိမ်းဆည်းထားသည့်စာရင်းမရှိသေးပါ{Colors.END}".ljust(40) + Styles.PIPE)
    else:
        print(f"{Styles.PIPE}  {Colors.GREEN}💾 သိမ်းဆည်းထားသည့်လင့်ခ်များ-{Colors.END}".ljust(40) + Styles.PIPE)
        print(f"{Styles.LINE_MID}")
               with open(FILE_MY, "r", encoding="utf-8") as f:
            print(f.read())
    print_footer()
    input(f"{Colors.CYAN}⏎ ပြန်မယူဖို့ ခလုတ်တစ်ခုခုနှိပါ...{Colors.END}")

def check_link_alive():
    print_header("လင့်ခ် စစ်ဆေးခြင်း")
    if not os.path.exists(FILE_MAIN):
        print(f"{Styles.PIPE}  {Colors.YELLOW}⚠️ ဖိုင်မရှိသေးပါ။ အရင် ဒေတာအသစ်ရယူပါ။{Colors.END}".ljust(40) + Styles.PIPE)
        print_footer()
        return
    
    with open(FILE_MAIN, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f.read().splitlines() if l.strip() and l.startswith("ss://")]
    
    print(f"{Styles.PIPE}  {Colors.GREEN}🟢 အသက်ဝင်သည်  |  {Colors.YELLOW}🟡 မသိရှိနိုင်  |  {Colors.RED}🔴 မအလုပ်လုပ်ပါ{Colors.END}".ljust(40) + Styles.PIPE)
    print(f"{Styles.PIPE}  {Colors.CYAN}ℹ️ SS လင့်ခ်များကို တိုက်ရိုက်မစစ်ဆေးနိုင်ပါ{Colors.END}".ljust(40) + Styles.PIPE)
    
    for i, line in enumerate(lines[:10], 1):
        name = extract_server_name(line)
        print(f"{Styles.PIPE}     {Colors.GREEN}🟢 [{i}] {name}{Colors.END}".ljust(40) + Styles.PIPE)
    
    if len(lines) > 10:
        print(f"{Styles.PIPE}     {Colors.YELLOW}... နောက်ထပ် {len(lines) - 10} ခု ကျန်ရှိ{Colors.END}".ljust(40) + Styles.PIPE)
    print_footer()
    input(f"{Colors.CYAN}⏎ ပြန်မယူဖို့ ခလုတ်တစ်ခုခုနှိပါ...{Colors.END}")

def export_json():
    print_header("JSON ဖိုင်အဖြစ် တင်ပို့ခြင်း")
    if not os.path.exists(FILE_MAIN):
        print(f"{Styles.PIPE}  {Colors.YELLOW}⚠️ ဖိုင်မရှိသေးပါ။ အရင် ဒေတာအသစ်ရယူပါ။{Colors.END}".ljust(40) + Styles.PIPE)
        print_footer()
        return
    with open(FILE_MAIN, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f.read().splitlines() if l.strip()]
    
    data = {
        "export_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_items": len(lines),
        "items": lines
    }
    
    with open(FILE_EXPORT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"{Styles.PIPE}  {Colors.GREEN}✅ JSON ဖိုင်အဖြစ် အောင်မြင်စွာ တင်ပို့ပြီးပါပြီ{Colors.END}".ljust(40) + Styles.PIPE)
    print(f"{Styles.PIPE}  {Colors.CYAN}📁 ဖိုင်အမည်: {FILE_EXPORT_JSON}{Colors.END}".ljust(40) + Styles.PIPE)
    print_footer()
    input(f"{Colors.CYAN}⏎ ပြန်မယူဖို့ ခလုတ်တစ်ခုခုနှိပါ...{Colors.END}")

def export_csv():
    print_header("CSV ဖိုင်အဖြစ် တင်ပို့ခြင်း")
    if not os.path.exists(FILE_MAIN):
        print(f"{Styles.PIPE}  {Colors.YELLOW}⚠️ ဖိုင်မရှိသေးပါ။ အရင် ဒေတာအသစ်ရယူပါ။{Colors.END}".ljust(40) + Styles.PIPE)
        print_footer()
        return
    with open(FILE_MAIN, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f.read().splitlines() if l.strip()]
    
    with open(FILE_EXPORT_CSV, "w", encoding="utf-8") as f:
        f.write("Server Name,Link\n")
        for line in lines:
            name = extract_server_name(line).replace(",", " -")
            f.write(f'"{name}","{line}"\n')
    
    print(f"{Styles.PIPE}  {Colors.GREEN}✅ CSV ဖိုင်အဖြစ် အောင်မြင်စွာ တင်ပို့ပြီးပါပြီ{Colors.END}".ljust(40) + Styles.PIPE)
    print(f"{Styles.PIPE}  {Colors.CYAN}📁 ဖိုင်အမည်: {FILE_EXPORT_CSV}{Colors.END}".ljust(40) + Styles.PIPE)
    print_footer()
    input(f"{Colors.CYAN}⏎ ပြန်မယူဖို့ ခလုတ်တစ်ခုခုနှိပါ...{Colors.END}")

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
    print_header("အကြိုက်ဆုံး အမှတ်အသားပြုခြင်း")
    if not os.path.exists(FILE_MAIN):
        print(f"{Styles.PIPE}  {Colors.YELLOW}⚠️ ဖိုင်မရှိသေးပါ။ အရင် ဒေတာအသစ်ရယူပါ။{Colors.END}".ljust(40) + Styles.PIPE)
        print_footer()
        return
    with open(FILE_MAIN, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f.read().splitlines() if l.strip()]
    
    favs = load_favorites()
    
    print(f"{Styles.PIPE}  {Colors.CYAN}⭐ လင့်ခ်စာရင်းများ - နံပါတ်ရွေးပါ-{Colors.END}".ljust(40) + Styles.PIPE)
    for i, line in enumerate(lines, 1):
        star = " ⭐" if line in favs else ""
        name = extract_server_name(line)
        print(f"{Styles.PIPE}     {Colors.WHITE}[{i}]{star} {name}{Colors.END}".ljust(40) + Styles.PIPE)
    
    choice = input(f"\n{Styles.PIPE}  {Colors.CYAN}နံပါတ်ရိုက်ထည့်ပါ: {Colors.END}")
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(lines):
            link = lines[idx]
            if link in favs:
                favs.remove(link)
                print(f"{Styles.PIPE}  {Colors.YELLOW}⭐ အကြိုက်မှဖယ်ရှားပြီးပါပြီ{Colors.END}".ljust(40) + Styles.PIPE)
            else:
                favs.add(link)
                print(f"{Styles.PIPE}  {Colors.GREEN}⭐ အကြိုက်ဆုံးထဲသို့ထည့်ပြီးပါပြီ{Colors.END}".ljust(40) + Styles.PIPE)
            save_favorites(favs)
    except ValueError:
        print(f"{Styles.PIPE}  {Colors.RED}❌ မှားနေပါတယ်{Colors.END}".ljust(40) + Styles.PIPE)
    print_footer()
    input(f"{Colors.CYAN}⏎ ပြန်မယူဖို့ ခလုတ်တစ်ခုခုနှိပါ...{Colors.END}")

def view_favorites():
    print_header("အကြိုက်ဆုံးစာရင်း")
    favs = load_favorites()
    if not favs:
        print(f"{Styles.PIPE}  {Colors.YELLOW}⚠️ အကြိုက်ဆုံးစာရင်းမရှိသေးပါ{Colors.END}".ljust(40) + Styles.PIPE)
    else:
        print(f"{Styles.PIPE}  {Colors.GREEN}⭐ သိမ်းဆည်းထားသည့်အရာများ-{Colors.END}".ljust(40) + Styles.PIPE)
        for i, item in enumerate(favs, 1):
            name = extract_server_name(item)
            print(f"{Styles.PIPE}     {Colors.WHITE}[{i}] {name}{Colors.END}".ljust(40) + Styles.PIPE)
    print_footer()
    input(f"{Colors.CYAN}⏎ ပြန်မယူဖို့ ခလုတ်တစ်ခုခုနှိပါ...{Colors.END}")

def view_history():
    print_header("မှတ်တမ်းသမိုင်း")
    if not os.path.exists(FILE_HIST):
        print(f"{Styles.PIPE}  {Colors.YELLOW}⚠️ မှတ်တမ်းမရှိသေးပါ{Colors.END}".ljust(40) + Styles.PIPE)
    else:
        print(f"{Styles.PIPE}  {Colors.CYAN}📜 ယခင်ရယူခဲ့သည့်မှတ်တမ်း-{Colors.END}".ljust(40) + Styles.PIPE)
        with open(FILE_HIST, "r", encoding="utf-8") as f:
            history = json.load(f)
        if not history:
            print(f"{Styles.PIPE}  {Colors.YELLOW}မှတ်တမ်းမရှိသေးပါ{Colors.END}".ljust(40) + Styles.PIPE)
        else:
            for idx, rec in enumerate(reversed(history[-15:]), 1):
                print(f"{Styles.PIPE}     {Colors.WHITE}[{idx}] {rec['time']} → {rec['lines']} လိုင်း{Colors.END}".ljust(40) + Styles.PIPE)
    print_footer()
    input(f"{Colors.CYAN}⏎ ပြန်မယူဖို့ ခလုတ်တစ်ခုခုနှိပါ...{Colors.END}")

def main_menu():
    while True:
        clear_screen()
        now = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
        
        print(f"{Colors.MAGENTA}╔═══════════════════════════════════════════╗{Colors.END}")
        print(f"{Colors.MAGENTA}║{Colors.CYAN}{Colors.BOLD}           🚀  SUB DOWNLOADER              {Colors.END}{Colors.MAGENTA}║{Colors.END}")
        print(f"{Colors.MAGENTA}║{Colors.DIM}         Premium Edition  v3.1            {Colors.END}{Colors.MAGENTA}║{Colors.END}")
        print(f"{Colors.MAGENTA}╠═══════════════════════════════════════════╣{Colors.END}")
        print(f"{Colors.MAGENTA}║{Colors.CYAN}  📥 အခြေခံ လုပ်ဆောင်ချက်များ{Colors.END}{' ' * 18}{Colors.MAGENTA}║{Colors.END}")
        print(f"{Colors.MAGENTA}║{Colors.WHITE}   1. ဒေတာအသစ်ပြန်ရယူပါ              {' ' * 11}{Colors.MAGENTA}║{Colors.END}")
        print(f"{Colors.MAGENTA}║{Colors.WHITE}   2. လက်ရှိဒေတာကို ကြည့်ပါ          {' ' * 11}{Colors.MAGENTA}║{Colors.END}")
        print(f"{Colors.MAGENTA}║{Colors.WHITE}   3. စာရင်းဇယား ကြည့်ပါ             {' ' * 11}{Colors.MAGENTA}║{Colors.END}")
        print(f"{Colors.MAGENTA}║{Colors.WHITE}   4. နိုင်ငံအလိုက် စီစဉ်ကြည့်ပါ       {' ' * 11}{Colors.MAGENTA}║{Colors.END}")
        print(f"{Colors.MAGENTA}║{Colors.WHITE}   5. ရှာဖွေပါ                        {' ' * 11}{Colors.MAGENTA}║{Colors.END}")
        print(f"{Colors.MAGENTA}║{Colors.WHITE}   6. အားလုံးကူးယူဖို့ ပြပါ             {' ' * 11}{Colors.MAGENTA}║{Colors.END}")
        print(f"{Colors.MAGENTA}╠═══════════════════════════════════════════╣{Colors.END}")
        print(f"{Colors.MAGENTA}║{Colors.GREEN}  💾 သိမ်းဆည်းခြင်း & အကြိုက်ဆုံး{Colors.END}{' ' * 15}{Colors.MAGENTA}║{Colors.END}")
        print(f"{Colors.MAGENTA}║{Colors.WHITE}   7. လင့်ခ်ရွေးပြီး သိမ်းဆည်းပါ      {' ' * 11}{Colors.MAGENTA}║{Colors.END}")
        print(f"{Colors.MAGENTA}║{Colors.WHITE}   8. ကျွန်ုပ်၏စာရင်းကို ကြည့်ပါ     {' ' * 11}{Colors.MAGENTA}║{Colors.END}")
        print(f"{Colors.MAGENTA}║{Colors.WHITE}   9. အကြိုက်ဆုံးအဖြစ် အမှတ်အသားပြုပါ {' ' * 11}{Colors.MAGENTA}║{Colors.END}")
        print(f"{Colors.MAGENTA}║{Colors.WHITE}  10. အကြိုက်ဆုံးစာရင်း ကြည့်ပါ        {' ' * 11}{Colors.MAGENTA}║{Colors.END}")
        print(f"{Colors.MAGENTA}╠═══════════════════════════════════════════╣{Colors.END}")
        print(f"{Colors.MAGENTA}║{Colors.YELLOW}  📤 တင်ပို့ခြင်း & စစ်ဆေးခြင်း{Colors.END}{' ' * 17}{Colors.MAGENTA}║{Colors.END}")
        print(f"{Colors.MAGENTA}║{Colors.WHITE}  11. လင့်ခ်အသက်ဝင်မှု စစ်ဆေးပါ      {' ' * 11}{Colors.MAGENTA}║{Colors.END}")
        print(f"{Colors.MAGENTA}║{Colors.WHITE}  12. JSON အဖြစ်တင်ပို့ပါ             {' ' * 11}{Colors.MAGENTA}║{Colors.END}")
        print(f"{Colors.MAGENTA}║{Colors.WHITE}  13. CSV အဖြစ်တင်ပို့ပါ              {' ' * 11}{Colors.MAGENTA}║{Colors.END}")
        print(f"{Colors.MAGENTA}╠═══════════════════════════════════════════╣{Colors.END}")
        print(f"{Colors.MAGENTA}║{Colors.CYAN}  🔍 အခြားအသုံးဝင်သည့်အရာများ{Colors.END}{' ' * 18}{Colors.MAGENTA}║{Colors.END}")
        print(f"{Colors.MAGENTA}║{Colors.WHITE}  14. အသစ်ရှိလား စစ်ဆေးပါ            {' ' * 11}{Colors.MAGENTA}║{Colors.END}")
        print(f"{Colors.MAGENTA}║{Colors.WHITE}  15. မှတ်တမ်းသမိုင်း ကြည့်ပါ        {' ' * 11}{Colors.MAGENTA}║{Colors.END}")
        print(f"{Colors.MAGENTA}║{Colors.RED}  16. ဖိုင်အားလုံးကိုဖျက်ပါ              {' ' * 11}{Colors.MAGENTA}║{Colors.END}")
        print(f"{Colors.MAGENTA}║{Colors.WHITE}   0. ပရိုဂရမ်မှ ထွက်ပါ               {' ' * 11}{Colors.MAGENTA}║{Colors.END}")
        print(f"{Colors.MAGENTA}╠═══════════════════════════════════════════╣{Colors.END}")
        print(f"{Colors.MAGENTA}║{Colors.DIM}  🕒 {now}{' ' * 23}{Colors.MAGENTA}║{Colors.END}")
        print(f"{Colors.MAGENTA}╚═══════════════════════════════════════════╝{Colors.END}")
        
        choice = input(f"\n{Colors.BOLD}{Colors.CYAN}  ✅ ရွေးချယ်မှု → {Colors.END}")
        
        if choice == "1":
            fetch_data()
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
            check_updates()
        elif choice == "15":
            view_history()
        elif choice == "16":
            confirm = input(f"\n{Colors.RED}  ⚠️ ဖိုင်အားလုံးဖျက်မှာ သေချာပါသလား? (y/n): {Colors.END}").lower()
            if confirm == 'y':
                for f in [FILE_MAIN, FILE_MY, FILE_FAV, FILE_HIST]:
                    if os.path.exists(f):
                        os.remove(f)
                print(f"\n  {Colors.GREEN}🗑️ ဖိုင်အားလုံးဖျက်ပြီးပါပြီ{Colors.END}")
            time.sleep(1.5)
        elif choice == "0":
            clear_screen()
            print(f"{Colors.MAGENTA}╔════════════════════════════════════════╗{Colors.END}")
            print(f"{Colors.MAGENTA}║{Colors.CYAN}{Colors.BOLD}        👋 ကျေးဇူးတင်ပါတယ်!              {Colors.END}{Colors.MAGENTA}║{Colors.END}")
            print(f"{Colors.MAGENTA}║{Colors.DIM}     ထပ်မံအသုံးပြုရန် ကြိုဆိုပါတယ်         {Colors.END}{Colors.MAGENTA}║{Colors.END}")
            print(f"{Colors.MAGENTA}╚════════════════════════════════════════╝{Colors.END}")
            sys.exit(0)
        else:
            print(f"\n  {Colors.RED}❌ မှားနေပါတယ်။ 0-16 ကြား နံပါတ်သာရိုက်ပါ{Colors.END}")
            time.sleep(1.5)

if __name__ == "__main__":
    main_menu()
