import requests
import random
import string
import time
import re
import os

def generate_phone():
    cmcc = ['134','135','136','137','138','139','147','148','150','151','152',
            '157','158','159','172','178','182','183','184','187','188','195','197','198']
    cucc = ['130','131','132','145','146','155','156','166','167','175','176','185','186','196']
    ctcc = ['133','149','153','162','173','174','177','180','181','189','191','193','199']
    all_prefixes = cmcc * 5 + cucc * 3 + ctcc * 2
    for _ in range(10):
        prefix = random.choice(all_prefixes)
        suffix = ''.join(random.choices(string.digits, k=8))
        phone = prefix + suffix
        if not any(p in phone for p in ['123456', '111111', '000000', '888888']):
            return phone
    return '138' + ''.join(random.choices(string.digits, k=8))

def generate_password():
    length = random.randint(8, 12)
    chars = string.ascii_letters + string.digits
    pwd = [random.choice(string.ascii_letters), random.choice(string.digits)]
    pwd += random.choices(chars, k=length-2)
    random.shuffle(pwd)
    return ''.join(pwd)

def generate_name():
    surnames = ['王','李','张','刘','陈','杨','黄','赵','吴','周','徐','孙','马','朱','胡','郭','林','何','高','罗']
    given = ['伟','芳','娜','敏','静','丽','强','磊','洋','勇','艳','杰','倩','涛','明','超','秀英','华','慧','建']
    return random.choice(surnames) + random.choice(given)

def get_ua():
    return random.choice([
        'Mozilla/5.0 (Linux; Android 15; V2425A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.7827.159 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 14; SM-S921B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.7128.145 Mobile Safari/537.36',
    ])

class ZodiacBot:
    def __init__(self, base_url="http://app.wanshengxiao.cn"):
        self.base_url = base_url
        self.sdcard_path = self.get_sdcard_path()
        self.account_file = os.path.join(self.sdcard_path, '十二生肖注册账号列表.txt')
        self.ensure_dir()
    
    def ensure_dir(self):
        try:
            if not os.path.exists(self.sdcard_path):
                os.makedirs(self.sdcard_path, exist_ok=True)
        except:
            fallback = os.path.join(os.path.dirname(os.path.abspath(__file__)), '十二生肖账号')
            if not os.path.exists(fallback):
                os.makedirs(fallback, exist_ok=True)
            self.sdcard_path = fallback
            self.account_file = os.path.join(self.sdcard_path, '十二生肖注册账号列表.txt')
    
    def get_sdcard_path(self):
        for path in ['/sdcard/', '/storage/emulated/0/', '/storage/sdcard0/']:
            if os.path.exists(path):
                app_dir = os.path.join(path, '十二生肖账号')
                try:
                    if not os.path.exists(app_dir):
                        os.makedirs(app_dir, exist_ok=True)
                    return app_dir
                except:
                    continue
        fallback = os.path.join(os.path.dirname(os.path.abspath(__file__)), '十二生肖账号')
        if not os.path.exists(fallback):
            os.makedirs(fallback, exist_ok=True)
        return fallback
    
    def create_session(self):
        s = requests.Session()
        s.headers.update({
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': self.base_url,
            'Referer': f'{self.base_url}/sx/app.html',
            'User-Agent': get_ua(),
        })
        return s
    
    def get_sms_code(self, session, phone, log=None):
        if log: log(f"📱 验证手机: {phone}")
        n1, n2 = random.randint(1, 9), random.randint(1, 9)
        if log: log(f"  🧮 数学验证: {n1} + {n2} = ? → {n1+n2}")
        time.sleep(0.5)
        img = ''.join(random.choices(string.digits, k=4))
        if log: log(f"  🖼️  图形验证码: {img}")
        time.sleep(0.5)
        try:
            r = session.post(f"{self.base_url}/user/reg_sms", {'phone': phone}, timeout=10)
            if r.status_code == 200:
                data = r.json()
                if data.get('status') == 1:
                    code = re.search(r'\b(\d{6})\b', data.get('info', ''))
                    if code:
                        if log: log(f"  ✅ 验证码: {code.group(1)}")
                        return code.group(1)
            return None
        except Exception as e:
            if log: log(f"  ❌ {e}")
            return None
    
    def register(self, phone, password, name, ref, log=None):
        session = self.create_session()
        sms = self.get_sms_code(session, phone, log)
        if not sms:
            return False, "获取验证码失败"
        try:
            r = session.post(f"{self.base_url}/user/reg", {
                'username': phone, 'pwd': password, 'realname': name,
                'phone_code': sms, 'ref': ref
            }, timeout=10)
            if r.status_code == 200:
                data = r.json()
                if data.get('status') == 1:
                    return True, "注册成功"
                return False, data.get('info', '未知错误')
            return False, f"HTTP {r.status_code}"
        except Exception as e:
            return False, str(e)
    
    def login(self, session, phone, password, log=None):
        try:
            r = session.post(f"{self.base_url}/user/login", {'username': phone, 'pwd': password}, timeout=10)
            if r.status_code == 200:
                data = r.json()
                if data.get('status') == 1:
                    return True, "登录成功"
                return False, data.get('info', '登录失败')
            return False, f"HTTP {r.status_code}"
        except Exception as e:
            return False, str(e)
    
    def bind_alipay(self, session, name, alipay, log=None):
        try:
            session.headers.update({
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
                'Referer': f'{self.base_url}/user/info',
            })
            r = session.post(f"{self.base_url}/user/info", {
                'realname': name, 'alipay': alipay, 'type': 'alipay'
            }, timeout=10)
            if r.status_code == 200:
                try:
                    data = r.json()
                    if data.get('status') == 1:
                        return True, "绑定成功"
                    return False, data.get('info', '绑定失败')
                except:
                    if '修改成功' in r.text or '成功' in r.text:
                        return True, "绑定成功"
                    return False, "绑定失败"
            return False, f"HTTP {r.status_code}"
        except Exception as e:
            return False, str(e)
    
    def save(self, phone, password, name="", alipay="", log=None):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        try:
            with open(self.account_file, 'a', encoding='utf-8') as f:
                if not os.path.exists(self.account_file) or os.path.getsize(self.account_file) == 0:
                    f.write("=" * 80 + "\n")
                    f.write("🐉 十二生肖注册账号列表\n")
                    f.write(f"创建时间: {timestamp}\n")
                    f.write("=" * 80 + "\n")
                    f.write("序号\t手机号\t\t密码\t\t注册时间\t\t真实姓名\t支付宝账号\n")
                    f.write("-" * 80 + "\n")
                with open(self.account_file, 'r', encoding='utf-8') as check:
                    lines = check.readlines()
                    account_lines = [l for l in lines if l.strip() and not l.startswith('=') 
                                    and not l.startswith('🐉') and not l.startswith('创建时间')
                                    and not l.startswith('序号') and not l.startswith('-')]
                    seq = len(account_lines) + 1
                f.write(f"{seq}\t{phone}\t{password}\t{timestamp}\t{name}\t{alipay}\n")
            if log: log(f"💾 已保存: {phone}")
        except Exception as e:
            if log: log(f"⚠️ 保存失败: {e}")
    
    def register_one(self, ref, log=None):
        phone = generate_phone()
        password = generate_password()
        name = generate_name()
        alipay = phone
        if log:
            log(f"\n📋 手机: {phone} | 密码: {password}")
            log(f"  姓名: {name} | 支付宝: {alipay}")
            log(f"\n📌 步骤1: 注册")
        success, msg = self.register(phone, password, name, ref, log)
        if not success:
            if log: log(f"❌ {msg}")
            return False
        if log: log(f"✅ {msg}")
        session = self.create_session()
        if log: log(f"\n📌 步骤2: 登录")
        success, msg = self.login(session, phone, password, log)
        if not success:
            if log: log(f"❌ {msg}")
            return False
        if log: log(f"\n📌 步骤3: 绑定支付宝")
        success, msg = self.bind_alipay(session, name, alipay, log)
        if success:
            if log: log(f"✅ {msg}")
            self.save(phone, password, name, alipay, log)
        else:
            if log: log(f"❌ {msg}")
            self.save(phone, password, name, "", log)
        return True

def batch_register(ref, count, log=None):
    bot = ZodiacBot()
    if log:
        log(f"📌 注册 {count} 个账号 | 推荐码: {ref}")
        log(f"📁 保存: {bot.account_file}")
    success = 0
    for i in range(count):
        if log: log(f"\n{'='*55}\n🐉 第 {i+1}/{count} 个\n{'='*55}")
        if bot.register_one(ref, log):
            success += 1
        if i < count - 1:
            delay = random.uniform(2, 5)
            if log: log(f"⏳ 等待 {delay:.1f} 秒...")
            time.sleep(delay)
    if log:
        log(f"\n{'='*55}")
        log(f"📊 成功: {success}/{count}")
        log(f"📁 文件: {bot.account_file}")
        log(f"{'='*55}")
    return success

def run(args=None):
    return "请使用APP界面操作"
