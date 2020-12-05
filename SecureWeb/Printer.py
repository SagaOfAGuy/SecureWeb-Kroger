import os
import subprocess
import platform
def check_os():
    system = platform.platform()
    if ('macOS' in system):
        return "mac" 
    elif ("Linux" in system or "linux" in system):
        return "linux"
    elif ('Windows' in system or "win" in system):
        return 'Windows'
    else:
        return 'Unknown OS'
def run_cmd(command):
    return subprocess.check_output(command, stdin=subprocess.PIPE, shell=True, universal_newlines=True)
def find_printers_nix():
    find_printer_cmd = run_cmd("lpstat -a | cut -d ' ' -f1")
    printers = list(find_printer_cmd.split("\n"))
    if (type(printers) == list):
        return printers[0]
    else:
        return printers
def print_file(filename, printer):
    system_os = check_os()
    if ("mac" in system_os):
        os.system(f"lpr -P {printer} -o landscape -o media=A4 -o fit-to-page {filename}")
        print("Paystub is printing...")
        print("Success!")
    elif ("linux" in system_os):
        os.system(f"lp -d {printer} -o landscape -o fit-to-page -o media=A4 {filename}")
        print("File is printing...")
        print("Success!")
    else:
        pass 
