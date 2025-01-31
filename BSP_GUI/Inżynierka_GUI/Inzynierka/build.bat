@echo off
pyinstaller --onefile --windowed --icon=logo.png ^
    --add-data "about_tab.py;." ^
    --add-data "audio_tab.py;." ^
    --add-data "connect_tab.py;." ^
    --add-data "Debuger.py;." ^
    --add-data "half_keys_indexed.json;." ^
    --add-data "localization_tab.py;." ^
    --add-data "logo.png;." ^
    --add-data "loralibery.py;." ^
    --add-data "manual_tab.py;." ^
    --add-data "map.html;." ^
    --add-data "microphone.png;." ^
    --add-data "pause.png;." ^
    --add-data "play.png;." ^
    --add-data "recording.wav;." ^
    --add-data "start_page.py;." ^
    --add-data "text_tab.py;." ^
    --add-data "trash.png;." ^
    --add-data "video.py;." ^
    --add-data "wspolne.jpeg;." ^
    --add-data "ZDJĘCIE.PNG;." ^
    --add-data "ZDJĘCIE1.PNG;." ^
    main_testowy2.py
pause
