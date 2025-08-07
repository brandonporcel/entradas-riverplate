from colorama import Fore, Style, init
init()

def log_info(message):
    print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} {message}")

def log_success(message):
    print(f"{Fore.GREEN}[✔]{Style.RESET_ALL} {message}")

def log_warning(message):
    print(f"{Fore.YELLOW}[!]{Style.RESET_ALL} {message}")

def log_error(message):
    print(f"{Fore.RED}[✖]{Style.RESET_ALL} {message}")
