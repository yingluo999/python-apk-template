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


class ZodiacRegister:
    def __init__(self, base_url="http://app.wanshengxiao.cn"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 15; V2425A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.7827.159 Mobile Safari/537.36',
        })
    
    def register_one(self, ref_code, log=None):
        """注册一个账号"""
        phone = generate_phone()
        password = generate_password()
        name = generate_name()
        alipay = phone
        
        if log:
            log(f"📱 手机: {phone} | 密码: {password}")
            log(f"👤 姓名: {name} | 支付宝: {alipay}")
        
        # 获取验证码
        sms = self._get_sms(phone, log)
        if not sms:
            if log: log("❌ 获取验证码失败")
            return False
        
        # 注册
        success, msg = self._register(phone, password, name, sms, ref_code, log)
        if not success:
            if log: log(f"❌ {msg}")
            return False
        if log: log(f"✅ {msg}")
        
        # 登录
        success, session = self._login(phone, password, log)
        if not success:
            if log: log("❌ 登录失败")
            return False
        
        # 绑定支付宝
        success, msg = self._bind_alipay(session, name, alipay, log)
        if success:
            if log: log(f"✅ {msg}")
        else:
            if log: log(f"❌ {msg}")
        
        # 保存
        self._save_account(phone, password, name, alipay, log)
        return True
    
    def _get_sms(self, phone, log=None):
        """获取验证码"""
        if log: log(f"📱 验证手机: {phone}")
        # 模拟数学验证
        n1, n2 = random.randint(1, 9), random.randint(1, 9)
        if log: log(f"  🧮 验证: {n1} + {n2} = {n1+n2}")
        time.sleep(0.5)
        # 模拟图形验证码
        img = ''.join(random.choices(string.digits, k=4))
        if log: log(f"  🖼️ 验证码: {img}")
        time.sleep(0.5)
        
        try:
            r = self.session.post(f"{self.base_url}/user/reg_sms", {'phone': phone}, timeout=10)
            if r.status_code == 200:
                data = r.json()
                if data.get('status') == 1:
                    code = re.search(r'\b(\d{6})\b', data.get('info', ''))
                    if code:
                        if log: log(f"  ✅ 验证码: {code.group(1)}")
                        return code.group(1)
            return None
        except:
            return None
    
    def _register(self, phone, password, name, sms, ref, log=None):
        """注册"""
        try:
            r = self.session.post(f"{self.base_url}/user/reg", {
                'username': phone, 'pwd': password, 'realname': name,
                'phone_code': sms, 'ref': ref
            }, timeout=10)
            if r.status_code == 200:
                data = r.json()
                if data.get('status') == 1:
                    return True, "注册成功"
                return False, data.get('info', '注册失败')
            return False, f"HTTP {r.status_code}"
        except Exception as e:
            return False, str(e)
    
    def _login(self, phone, password, log=None):
        """登录"""
        try:
            r = self.session.post(f"{self.base_url}/user/login", {
                'username': phone, 'pwd': password
            }, timeout=10)
            if r.status_code == 200:
                data = r.json()
                if data.get('status') == 1:
                    return True, self.session
                return False, None
            return False, None
        except:
            return False, None
    
    def _bind_alipay(self, session, name, alipay, log=None):
        """绑定支付宝"""
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
    
    def _save_account(self, phone, password, name, alipay, log=None):
        """保存账号"""
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        # 获取SD卡路径
        sdcard = '/sdcard/'
        if os.path.exists('/storage/emulated/0/'):
            sdcard = '/storage/emulated/0/'
        elif os.path.exists('/storage/sdcard0/'):
            sdcard = '/storage/sdcard0/'
        
        account_dir = os.path.join(sdcard, '十二生肖账号')
        try:
            os.makedirs(account_dir, exist_ok=True)
        except:
            account_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '十二生肖账号')
            os.makedirs(account_dir, exist_ok=True)
        
        account_file = os.path.join(account_dir, '十二生肖注册账号列表.txt')
        
        try:
            with open(account_file, 'a', encoding='utf-8') as f:
                # 检查文件是否为空
                if os.path.getsize(account_file) == 0:
                    f.write("=" * 80 + "\n")
                    f.write("🐉 十二生肖注册账号列表\n")
                    f.write(f"创建时间: {timestamp}\n")
                    f.write("=" * 80 + "\n")
                    f.write("序号\t手机号\t\t密码\t\t注册时间\t\t真实姓名\t支付宝账号\n")
                    f.write("-" * 80 + "\n")
                
                # 计算序号
                with open(account_file, 'r', encoding='utf-8') as check:
                    lines = check.readlines()
                    account_lines = [l for l in lines if l.strip() and not l.startswith('=') 
                                    and not l.startswith('🐉') and not l.startswith('创建时间')
                                    and not l.startswith('序号') and not l.startswith('-')]
                    seq = len(account_lines) + 1
                
                f.write(f"{seq}\t{phone}\t{password}\t{timestamp}\t{name}\t{alipay}\n")
            
            if log: log(f"💾 已保存: {account_file}")
        except Exception as e:
            if log: log(f"⚠️ 保存失败: {e}")


# ========== APP 入口函数（必须保留） ==========
def batch_register(ref_code: str, count: int, log_callback=None):
    """
    批量注册 - APP 调用的入口函数
    """
    register = ZodiacRegister()
    
    if log_callback:
        log_callback(f"📌 注册 {count} 个账号 | 推荐码: {ref_code}")
    
    success = 0
    for i in range(count):
        if log_callback:
            log_callback(f"\n{'='*55}")
            log_callback(f"🐉 第 {i+1}/{count} 个")
            log_callback(f"{'='*55}")
        
        if register.register_one(ref_code, log_callback):
            success += 1
        
        if i < count - 1:
            delay = random.uniform(2, 5)
            if log_callback:
                log_callback(f"⏳ 等待 {delay:.1f} 秒...")
            time.sleep(delay)
    
    if log_callback:
        log_callback(f"\n{'='*55}")
        log_callback(f"📊 成功: {success}/{count}")
        log_callback(f"{'='*55}")
    
    return success


def run(args=None):
    """兼容旧版入口"""
    return "请使用APP界面操作"
