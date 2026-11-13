import urllib.request

RO_URL = "https://" + "iptv-org.github.io" + "/iptv/countries/ro.m3u"
DE_URL = "https://" + "iptv-org.github.io" + "/iptv/countries/de.m3u"

lines = ["#EXTM3U"]

def adauga_canale(url, tara):
    try:
        req = urllib.request.urlopen(url, timeout=15)
        content = req.read().decode("utf-8").splitlines()
        info = ""
        for line in content:
            line = line.strip()
            if line.startswith("#EXTINF"):
                nume = line.split(",")[-1].strip()
                info = f'#EXTINF:-1 group-title="{tara}",{nume}'
            elif line.startswith("#"):
                continue
            elif line.startswith("http") and info:
                lines.append(info)
                lines.append(line)
                info = ""
    except Exception as e:
        print(f"Eroare la {tara}: {e}")

adauga_canale(RO_URL, "Romania TV")
adauga_canale(DE_URL, "Germania TV")

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
