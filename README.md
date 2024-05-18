# Tele-DLL-Forwarding
We want to get a shell after a victim open the notepad, calculator and other Microsoft built-in programs!! 

# About
When attackers get an infected file onto your machine, this file is then executed when the application vulnerable to DLL hijacking is run. DLL hijacking is a cyberattack method that injects an infected file within the search parameters of an application. A user then attempts to load a file from that directory and instead loads the infected DLL file. This infected file takes action when the application is loaded. DLL files are often preloaded into a computer. Many applications with DLL files automatically load during startup, which can then compromise the entire computer, giving hackers access to it whenever the file containing the malicious code loads.

Windows operating systems provide the functionality to allow custom DLL’s to be loaded into the address space of almost all application processes. This can give the opportunity for persistence since an arbitrary DLL can be loaded that will execute code when applications processes are created on the system. Administrator level privileges are required to implement this technique.

Therefore; Microsoft protect Windows users from malware has disabled by default the loading of DLLs’s via AppInit. However, setting the registry key “LoadAppInit_DLLs” to value “1” will enable this functionality. Dropping the arbitrary DLL into the “Program Files” directory and modifying the “AppInit_DLLs” registry key to contain the path of the DLL will load the pentestlab.dll into every Windows application. This is because DLL’s that are specified in the “AppInit_DLLs” registry key are loaded by the user32.dll which is used by almost all applications.

and here we go , this project is going to make your life easy by breaking those security implimented by MicroSOft to make this attack happening Ethically

# DAY 1 : Thinking like hacker
![wow](https://github.com/AuxGrep/Tele-DLL-Forwarding/assets/103135612/f97b27ce-8233-4f8e-9a22-25c65c26092c)

# DAY 2: Building the bot
The Bolt tool will generate shellcode and write a dedicated C program designed to backdoor specific registry keys and their associated values on the target system.

![Screenshot from 2024-05-18 17-07-48](https://github.com/AuxGrep/Tele-DLL-Forwarding/assets/103135612/f80f44f2-21ed-435b-97b3-86cc18a9f6cf)

# DAY 3: Testing the Exploit
The Exploit was testing on Windows 10, Windows 11 23H..
![Screenshot from 2024-05-18 16-45-11](https://github.com/AuxGrep/Tele-DLL-Forwarding/assets/103135612/6580f523-f351-46b6-82b5-e2562e186e78)

![image](https://github.com/AuxGrep/Tele-DLL-Forwarding/assets/103135612/db8ca0ae-531d-4215-a8a8-c3f688f45b29)


# OUTPUT 

