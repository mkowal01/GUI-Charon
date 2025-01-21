DEBUG = True
TEXT = True
Audio = True
Localization = True
Connect = True
Main = True

def debug_print(filname, message):
    if DEBUG:
        if filname == "main_testowy2" and Main is True:
            print(f"\033[31m\033[1m[DEBUG]\033[0m\033[32m[{filname}   ] \033[0m {message}")
        if filname == "text_tab" and TEXT is True:
            print(f"\033[31m\033[1m[DEBUG]\033[0m\033[33m[{filname}        ] \033[0m {message}")
        if filname == "audio_tab" and Audio is True:
            print(f"\033[31m\033[1m[DEBUG]\033[0m\033[34m[{filname}       ] \033[0m {message}")
        if filname == "localization_tab" and Localization is True:
            print(f"\033[31m\033[1m[DEBUG]\033[0m\033[35m[{filname}] \033[0m {message}")
        if filname == "connection_tab" and Connect is True:
            print(f"\033[31m\033[1m[DEBUG]\033[0m\033[36m[{filname}  ] \033[0m {message}")