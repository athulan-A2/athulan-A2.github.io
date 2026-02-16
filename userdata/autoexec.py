import xbmc

# Vent til Kodi er ferdig lastet (viktig på macOS)
xbmc.sleep(8000)

# Spill introvideoen
xbmc.executebuiltin('PlayMedia("/Users/Athu/Documents/A2zone_intro.mp4")')
