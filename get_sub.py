#!/usr/bin/env python3
import urllib.request
import base64

URL = "https://shadowmere.xyz/api/b64sub/"

def main():
    print("🔄 အချက်အလက်များ ရယူနေသည်...")
    try:
        with urllib.request.urlopen(URL) as res:
            encoded = res.read().decode("utf-8").strip()
        decoded = base64.b64decode(encoded).decode("utf-8")
        print("\n✅ အောင်မြင်ပါပြီ!\n")
        print(decoded)
        with open("subscription.txt", "w", encoding="utf-8") as f:
            f.write(decoded)
        print("\n💾 သိမ်းဆည်းပြီးပါပြီ → subscription.txt")
    except Exception as e:
        print(f"❌ အမှားအယွင်း: {e}")

if __name__ == "__main__":
    main()
