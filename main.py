import threading
import os
try:
    from android.permissions import Permission, request_permissions, check_permission
    def request_storage_permission():
        permissions = [Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE]
        if not all(check_permission(p) for p in permissions):
            request_permissions(permissions)
            import time
            time.sleep(0.5)
    request_storage_permission()
except:
    pass

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.core.window import Window
from app.your_code import batch_register

class MainApp(App):
    def build(self):
        Window.size = (360, 640)
        Window.clearcolor = (0.95, 0.95, 0.95, 1)
        root = BoxLayout(orientation='vertical', spacing=10, padding=15)
        title = Label(text="🐉 十二生肖注册机器人", font_size=22, size_hint_y=None, height=50, color=(0.8,0.1,0.2,1), bold=True)
        root.add_widget(title)
        input_box = BoxLayout(orientation='vertical', spacing=8, size_hint_y=None, height=150)
        ref_layout = BoxLayout(orientation='horizontal', spacing=8, size_hint_y=None, height=40)
        ref_label = Label(text="推荐码:", size_hint_x=0.2, font_size=16, color=(0.2,0.2,0.2,1))
        self.ref_input = TextInput(text='125872', multiline=False, font_size=16, size_hint_x=0.8)
        ref_layout.add_widget(ref_label)
        ref_layout.add_widget(self.ref_input)
        input_box.add_widget(ref_layout)
        count_layout = BoxLayout(orientation='horizontal', spacing=8, size_hint_y=None, height=40)
        count_label = Label(text="数量:", size_hint_x=0.2, font_size=16, color=(0.2,0.2,0.2,1))
        self.count_input = TextInput(text='1', multiline=False, font_size=16, size_hint_x=0.3, input_filter='int')
        count_layout.add_widget(count_label)
        count_layout.add_widget(self.count_input)
        count_layout.add_widget(Label(size_hint_x=0.5))
        input_box.add_widget(count_layout)
        root.add_widget(input_box)
        btn_box = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        self.start_btn = Button(text="🚀 开始注册", font_size=18, background_color=(0.8,0.1,0.2,1), color=(1,1,1,1))
        self.start_btn.bind(on_press=self.start_register)
        self.clear_btn = Button(text="清空日志", font_size=16, background_color=(0.5,0.5,0.5,1), color=(1,1,1,1))
        self.clear_btn.bind(on_press=self.clear_log)
        btn_box.add_widget(self.start_btn)
        btn_box.add_widget(self.clear_btn)
        root.add_widget(btn_box)
        self.progress = ProgressBar(value=0, max=100, size_hint_y=None, height=20)
        root.add_widget(self.progress)
        log_box = BoxLayout(orientation='vertical', size_hint_y=1)
        log_label = Label(text="📋 日志输出", font_size=14, size_hint_y=None, height=25, color=(0.3,0.3,0.3,1))
        log_box.add_widget(log_label)
        self.log_output = TextInput(readonly=True, font_size=13, background_color=(0.05,0.05,0.05,1),
                                     foreground_color=(0.8,0.9,0.2,1), multiline=True, scroll_y=0)
        scroll = ScrollView(size_hint_y=1)
        scroll.add_widget(self.log_output)
        log_box.add_widget(scroll)
        root.add_widget(log_box)
        self.status_label = Label(text="✅ 就绪", font_size=12, size_hint_y=None, height=25, color=(0.3,0.6,0.3,1))
        root.add_widget(self.status_label)
        self.log_buffer = []
        self.is_running = False
        try:
            from app.your_code import ZodiacBot
            bot = ZodiacBot()
            self.log(f"📁 存储路径: {bot.account_file}")
        except:
            pass
        return root

    def log(self, text):
        self.log_buffer.append(text)
        if len(self.log_buffer) > 500:
            self.log_buffer = self.log_buffer[-500:]
        Clock.schedule_once(self.update_log, 0)

    def update_log(self, dt):
        if self.log_buffer:
            self.log_output.text = '\n'.join(self.log_buffer[-200:])
            self.log_output.cursor = (0, len(self.log_output.text))
            self.log_output.scroll_y = 0

    def clear_log(self, instance):
        self.log_buffer = []
        self.log_output.text = ''
        self.progress.value = 0
        self.status_label.text = "✅ 已清空"

    def start_register(self, instance):
        if self.is_running:
            self.log("⚠️ 正在运行中，请等待完成")
            return
        try:
            ref_code = self.ref_input.text.strip() or '125872'
            count = int(self.count_input.text.strip() or '1')
            if count <= 0:
                self.log("❌ 数量必须大于0")
                return
            if count > 100:
                self.log("⚠️ 数量过多(>100)，请确认")
                return
        except ValueError:
            self.log("❌ 请输入有效数字")
            return
        self.is_running = True
        self.start_btn.text = "⏳ 运行中..."
        self.start_btn.disabled = True
        self.progress.value = 0
        self.log_buffer = []
        self.log("=" * 55)
        self.log(f"🐉 开始批量注册")
        self.log(f"📌 推荐码: {ref_code}")
        self.log(f"📌 注册数量: {count}")
        self.log("=" * 55)
        thread = threading.Thread(target=self.run_register, args=(ref_code, count))
        thread.daemon = True
        thread.start()

    def run_register(self, ref_code, count):
        def log_callback(text):
            self.log(text)
        try:
            success = batch_register(ref_code, count, log_callback)
            if success == count:
                self.log("\n🎉 全部注册完成!")
                self.status_label.text = "✅ 全部完成"
            else:
                self.log(f"\n⚠️ 完成 {success}/{count}，有 {count-success} 个失败")
                self.status_label.text = f"⚠️ 完成 {success}/{count}"
        except Exception as e:
            self.log(f"\n❌ 发生错误: {str(e)}")
            self.status_label.text = "❌ 发生错误"
        finally:
            self.is_running = False
            Clock.schedule_once(lambda dt: self.reset_ui(), 0)

    def reset_ui(self):
        self.start_btn.text = "🚀 开始注册"
        self.start_btn.disabled = False
        self.progress.value = 100

if __name__ == '__main__':
    MainApp().run()
