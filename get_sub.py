#!/usr/bin/env python3
import urllib.request
import base64
import sys

URL = "https://shadowmere.xyz/api/b64sub/"

def main():
    print("🔄 အချက်အလက်များ ရယူနေသည်...")
    try:
        # HTTP request ပြုလုပ်ခြင်း
        req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as res:
            encoded = res.read().decode("utf-8").strip()
        
        # Base64 ဖြင့် decode လုပ်ခြင်း
        decoded = base64.b64decode(encoded).decode("utf-8")
        
        # ရလဒ်ပြသခြင်း
        print("\n✅ အောင်မြင်စွာ ဖော်ထုတ်ပြီးပါပြီ!\n")
        print(decoded)
        
        # ဖိုင်အဖြစ်သိမ်းဆည်းခြင်း
        with open("subscription.txt", "w", encoding="utf-8") as f:
            f.write(decoded)
        print("\n💾 ဖိုင်အဖြစ် သိမ်းဆည်းပြီးပါပြီ → subscription.txt")
        print("📄 စုစုပေါင်းလိုင်းအရေအတွက်:", len(decoded.splitlines()))
        
    except urllib.error.URLError:
        print("❌ ကွန်ရက်ချိတ်ဆက်မှု အမှားအယွင်း ရှိနေသည်")
        sys.exit(1)
    except base64.binascii.Error:
        print("❌ ဒေတာဖော်ထုတ်၍မရပါ - မမှန်ကန်သောကုဒ်ဖြစ်နေသည်")
        sys.exit(1)
    except Exception as e:
        print(f"❌ အမှားအယွင်း: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
    
