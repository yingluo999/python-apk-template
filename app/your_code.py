import requests
import random
import string
import time
import re
import os
from typing import Optional, Tuple
from urllib.parse import quote


class ZodiacBot:
    def __init__(self, base_url: str = "http://app.wanshengxiao.cn"):
        self.base_url = base_url
        self.session = None
        self.sdcard_path = self.get_sdcard_path()
        self.account_file = os.path.join(self.sdcard_path, '十二生肖注册账号列表.txt')
        print(f"📁 存储路径: {self.sdcard_path}")
    
    def get_sdcard_path(self) -> str:
        possible_paths = ['/sdcard/', '/storage/emulated/0/', '/storage/sdcard0/', '/mnt/sdcard/']
        for path in possible_paths:
            if os.path.exists(path):
                app_dir = os.path.join(path, '十二生肖账号')
                try:
                    if not os.path.exists(app_dir):
                        os.makedirs(app_dir)
                    test_file = os.path.join(app_dir, '.test')
                    with open(test_file, 'w') as f:
                        f.write('test')
                    os.remove(test_file)
                    return app_dir
                except:
                    continue
        fallback_dir = os.path.join(os.getcwd(), '十二生肖账号')
        if not os.path.exists(fallback_dir):
            os.makedirs(fallback_dir)
        return fallback_dir
    
    def create_session(self):
        session = requests.Session()
        session.headers.update({
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Origin': self.base_url,
            'Referer': f'{self.base_url}/sx/app.html',
            'User-Agent': random.choice([
                'Mozilla/5.0 (Linux; Android 15; V2425A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.7827.159 Mobile Safari/537.36',
                'Mozilla/5.0 (Linux; Android 14; SM-S921B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.7128.145 Mobile Safari/537.36',
                'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1',
                'Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.6549.124 Mobile Safari/537.36',
            ])
        })
        return session
    
    def generate_realistic_phone(self) -> str:
        cmcc = ['134','135','136','137','138','139','147','148','150','151','152',
                '157','158','159','172','178','182','183','184','187','188','195','197','198']
        cucc = ['130','131','132','145','146','155','156','166','167','175','176','185','186','196']
        ctcc = ['133','149','153','162','173','174','177','180','181','189','191','193','199']
        virtual = ['170','171']
        all_prefixes = cmcc * 5 + cucc * 3 + ctcc * 2 + virtual
        for _ in range(10):
            prefix = random.choice(all_prefixes)
            suffix = ''.join(random.choices(string.digits, k=8))
            phone = prefix + suffix
            if not any(p in phone for p in ['123456', '111111', '000000', '888888']):
                return phone
        return '138' + ''.join(random.choices(string.digits, k=8))
    
    def generate_password(self) -> str:
        length = random.randint(8, 12)
        letters = string.ascii_letters
        digits = string.digits
        all_chars = letters + digits
        password = [random.choice(letters), random.choice(digits)]
        password += random.choices(all_chars, k=length-2)
        random.shuffle(password)
        return ''.join(password)
    
    def generate_realname(self) -> str:
        surnames = ['王','李','张','刘','陈','杨','黄','赵','吴','周','徐','孙','马','朱','胡',
                    '郭','林','何','高','罗','郑','梁','谢','宋','唐','许','韩','冯','邓','曹',
                    '彭','曾','萧','田','董','潘','袁','蔡','蒋','余','于','叶','杜','苏','魏']
        given_names = ['伟','芳','娜','敏','静','丽','强','磊','洋','勇','艳','杰','倩','涛','明',
                      '超','秀英','华','慧','建','文','平','刚','桂英','志强','秀兰','建国','建军',
                      '浩','然','宇','轩','瑞','晨','曦','瑶','琪','琳','博','文','昊','天','奕']
        surname = random.choice(surnames)
        if random.random() > 0.3:
            given = random.choice(given_names)
        else:
            given = random.choice(given_names) + random.choice(given_names)
        return surname + given
    
    def get_sms_code(self, session, phone):
        print(f"\n  📱 验证手机: {phone}")
        ops = ['+', '-', '×']
        op = random.choice(ops)
        if op == '+':
            n1, n2 = random.randint(1, 9), random.randint(1, 9)
            ans = n1 + n2
            print(f"  🧮 数学验证: {n1} + {n2} = ? → {ans}")
        elif op == '-':
            n1 = random.randint(5, 10)
            n2 = random.randint(1, n1 - 1)
            ans = n1 - n2
            print(f"  🧮 数学验证: {n1} - {n2} = ? → {ans}")
        else:
            n1, n2 = random.randint(1, 5), random.randint(1, 5)
            ans = n1 * n2
            print(f"  🧮 数学验证: {n1} × {n2} = ? → {ans}")
        time.sleep(random.uniform(0.3, 0.8))
        img_code = ''.join(random.choices(string.digits, k=4))
        print(f"  🖼️  图形验证码: {img_code}")
        time.sleep(random.uniform(0.3, 0.8))
        url = f"{self.base_url}/user/reg_sms"
        data = {'phone': phone}
        time.sleep(random.uniform(0.5, 1.0))
        try:
            response = session.post(url, data=data, timeout=10)
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 1:
                    code_match = re.search(r'\b(\d{6})\b', result.get('info', ''))
                    if code_match:
                        sms_code = code_match.group(1)
                        print(f"  ✅ 验证码: {sms_code}")
                        return sms_code
            return None
        except Exception as e:
            print(f"  ❌ 异常: {e}")
            return None
    
    def register_account(self, phone, password, realname, ref_code="125872"):
        session = self.create_session()
        sms_code = self.get_sms_code(session, phone)
        if not sms_code:
            return False, "获取验证码失败", None
        url = f"{self.base_url}/user/reg"
        data = {'username': phone, 'pwd': password, 'realname': realname,
                'phone_code': sms_code, 'ref': ref_code}
        time.sleep(random.uniform(0.3, 0.8))
        try:
            response = session.post(url, data=data, timeout=10)
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 1:
                    return True, "注册成功", session
                else:
                    return False, result.get('info', '未知错误'), None
            return False, f"HTTP {response.status_code}", None
        except Exception as e:
            return False, str(e), None
    
    def login(self, phone, password):
        session = self.create_session()
        url = f"{self.base_url}/user/login"
        data = {'username': phone, 'pwd': password}
        try:
            response = session.post(url, data=data, timeout=10)
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 1:
                    return True, session, "登录成功"
                else:
                    return False, session, result.get('info', '登录失败')
            return False, session, f"HTTP {response.status_code}"
        except Exception as e:
            return False, session, str(e)
    
    def bind_alipay(self, session, realname, alipay):
        url = f"{self.base_url}/user/info"
        data = {'realname': realname, 'alipay': alipay, 'type': 'alipay'}
        session.headers.update({
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
            'Referer': f'{self.base_url}/user/info',
            'Upgrade-Insecure-Requests': '1',
        })
        try:
            response = session.post(url, data=data, timeout=10)
            if response.status_code == 200:
                try:
                    result = response.json()
                    if result.get('status') == 1:
                        return True, "绑定成功"
                    else:
                        return False, result.get('info', '绑定失败')
                except:
                    html = response.text
                    if '修改成功' in html or '成功' in html:
                        return True, "绑定成功"
                    else:
                        return False, "绑定失败"
            return False, f"HTTP {response.status_code}"
        except Exception as e:
            return False, str(e)
    
    def logout(self, session):
        if not session:
            return False, "没有登录会话"
        url = f"{self.base_url}/user/logout.html"
        session.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
            'Referer': f'{self.base_url}/index/index.html',
            'Upgrade-Insecure-Requests': '1',
        })
        try:
            response = session.get(url, timeout=10)
            if response.status_code == 200:
                try:
                    result = response.json()
                    if result.get('status') == 1:
                        return True, "退出成功"
                    else:
                        return False, result.get('info', '退出失败')
                except:
                    if '退出成功' in response.text:
                        return True, "退出成功"
                    else:
                        return False, "退出失败"
            return False, f"HTTP {response.status_code}"
        except Exception as e:
            return False, str(e)
    
    def save_account(self, phone, password, realname="", alipay=""):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        file_exists = os.path.exists(self.account_file)
        if os.path.exists(self.account_file):
            with open(self.account_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    if phone in line and line.startswith(('1', '2', '3', '4', '5', '6', '7', '8', '9')):
                        parts = line.strip().split('\t')
                        if len(parts) >= 4:
                            seq = parts[0]
                            new_line = f"{seq}\t{phone}\t{password}\t{timestamp}\t{realname}\t{alipay}\n"
                            lines[i] = new_line
                            with open(self.account_file, 'w', encoding='utf-8') as fw:
                                fw.writelines(lines)
                            print(f"💾 已更新账号信息: {phone}")
                            return
        with open(self.account_file, 'a', encoding='utf-8') as f:
            if not file_exists:
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
            f.write(f"{seq}\t{phone}\t{password}\t{timestamp}\t{realname}\t{alipay}\n")
        print(f"💾 已保存到文件: {phone}")
    
    def register_one(self, ref_code="125872"):
        phone = self.generate_realistic_phone()
        password = self.generate_password()
        realname = self.generate_realname()
        alipay = phone
        print(f"\n📋 生成信息:")
        print(f"  手机号: {phone}")
        print(f"  密码: {password}")
        print(f"  姓名: {realname}")
        print(f"  支付宝: {alipay}")
        print("\n📌 步骤1: 注册账号")
        success, msg, session = self.register_account(phone, password, realname, ref_code)
        if not success:
            print(f"❌ 注册失败: {msg}")
            return False
        print(f"✅ {msg}")
        print("\n📌 步骤2: 登录账号")
        success, session, msg = self.login(phone, password)
        if not success:
            print(f"❌ 登录失败: {msg}")
            return False
        print("\n📌 步骤3: 绑定支付宝")
        print(f"  姓名: {realname}")
        print(f"  支付宝: {alipay}")
        success, msg = self.bind_alipay(session, realname, alipay)
        if success:
            print(f"✅ {msg}")
            self.save_account(phone, password, realname, alipay)
        else:
            print(f"❌ 绑定失败: {msg}")
            self.save_account(phone, password, realname)
        print("\n📌 步骤4: 退出登录")
        success, msg = self.logout(session)
        if success:
            print(f"✅ {msg}")
        else:
            print(f"❌ {msg}")
        return True
    
    def batch_register(self):
        print("\n" + "=" * 55)
        print("🐉 批量注册并绑定支付宝")
        print("=" * 55)
        try:
            count = int(input("请输入要注册的数量: ").strip())
            if count <= 0:
                print("❌ 数量必须大于0")
                return
        except:
            print("❌ 请输入有效数字")
            return
        ref = input("请输入推荐码 (默认125872): ").strip() or "125872"
        print(f"\n📌 准备注册 {count} 个账号")
        print("=" * 55)
        success_count = 0
        fail_count = 0
        for i in range(count):
            print(f"\n{'='*55}")
            print(f"🐉 第 {i+1}/{count} 个账号")
            print(f"{'='*55}")
            if self.register_one(ref):
                success_count += 1
            else:
                fail_count += 1
            if i < count - 1:
                delay = random.uniform(2, 5)
                print(f"\n⏳ 等待 {delay:.1f} 秒...")
                time.sleep(delay)
        print("\n" + "=" * 55)
        print("📊 注册完成统计:")
        print(f"  成功: {success_count} 个")
        print(f"  失败: {fail_count} 个")
        print(f"  总计: {count} 个")
        print(f"📁 账号已保存到: {self.account_file}")
        print("=" * 55)
    
    def main_menu(self):
        while True:
            print("\n" + "🐉" * 12 + " 十二生肖机器人 " + "🐉" * 12)
            print("=" * 55)
            print("  1. 🚀 注册一个账号")
            print("  2. 📦 批量注册账号")
            print("  0. 退出程序")
            print("=" * 55)
            choice = input("请选择功能: ").strip()
            if choice == '1':
                ref = input("请输入推荐码 (默认125872): ").strip() or "125872"
                self.register_one(ref)
            elif choice == '2':
                self.batch_register()
            elif choice == '0':
                print("👋 再见!")
                break
            else:
                print("❌ 无效选择，请重新输入")


# ========== APP 入口（必须保留） ==========
def batch_register(ref_code: str, count: int, log_callback=None):
    """批量注册 - APP 调用的入口函数"""
    bot = ZodiacBot()
    
    if log_callback:
        log_callback(f"📌 注册 {count} 个账号 | 推荐码: {ref_code}")
        log_callback(f"📁 保存: {bot.account_file}")
    
    success = 0
    for i in range(count):
        if log_callback:
            log_callback(f"\n{'='*55}")
            log_callback(f"🐉 第 {i+1}/{count} 个")
            log_callback(f"{'='*55}")
        
        # 重定向 print 到 log_callback
        import sys
        from io import StringIO
        
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        result = bot.register_one(ref_code)
        
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        
        if log_callback:
            for line in output.strip().split('\n'):
                if line.strip():
                    log_callback(line)
        
        if result:
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
    return "请使用APP界面操作"


if __name__ == "__main__":
    bot = ZodiacBot()
    bot.main_menu()
