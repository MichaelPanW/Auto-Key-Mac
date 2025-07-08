#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mac環境定時按鍵盤程序（支援設定檔）
使用 pynput 庫來模擬鍵盤輸入
使用 schedule 庫來處理定時任務
"""

import time
import schedule
import threading
from datetime import datetime
from pynput.keyboard import Key, Controller
import sys
import signal
import json
import os

class AutoKeyboard:
    def __init__(self, config_file="config.json"):
        """初始化自動鍵盤控制器"""
        self.keyboard = Controller()
        self.running = False
        self.config_file = config_file
        self.config = self.load_config()
        
    def load_config(self):
        """載入設定檔"""
        default_config = {
            "interval_minutes": 1,
            "key_sequence": ["z", "a"],
            "key_duration": 0.1,
            "key_interval": 0.2,
            "description": "按鍵設定說明",
            "auto_start": False,
            "log_level": "info"
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # 合併預設設定和檔案設定
                    for key, value in default_config.items():
                        if key not in config:
                            config[key] = value
                    print(f"✅ 已載入設定檔: {self.config_file}")
                    return config
            else:
                print(f"⚠️  設定檔 {self.config_file} 不存在，使用預設設定")
                self.save_config(default_config)
                return default_config
        except Exception as e:
            print(f"❌ 載入設定檔失敗: {e}")
            print("使用預設設定")
            return default_config
    
    def save_config(self, config):
        """儲存設定檔"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            print(f"✅ 設定檔已儲存: {self.config_file}")
        except Exception as e:
            print(f"❌ 儲存設定檔失敗: {e}")
    
    def press_key_sequence(self):
        """按設定檔中的按鍵順序"""
        try:
            key_sequence = self.config["key_sequence"]
            key_duration = self.config["key_duration"]
            key_interval = self.config["key_interval"]
            
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 開始執行按鍵順序: {key_sequence}")
            
            for i, key in enumerate(key_sequence):
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 按下 {key} 鍵")
                
                # 處理特殊鍵
                if key.lower() in ['up', 'down', 'left', 'right', 'space', 'enter', 'tab', 'escape', 'backspace', 'delete']:
                    # 使用Key類別處理特殊鍵
                    key_obj = getattr(Key, key.lower())
                    self.keyboard.press(key_obj)
                    time.sleep(key_duration)
                    self.keyboard.release(key_obj)
                else:
                    # 處理普通字符鍵
                    self.keyboard.press(key)
                    time.sleep(key_duration)
                    self.keyboard.release(key)
                
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {key} 鍵已釋放")
                
                # 如果不是最後一個按鍵，則等待間隔時間
                if i < len(key_sequence) - 1:
                    time.sleep(key_interval)
            
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 按鍵順序執行完成")
            
        except Exception as e:
            print(f"按鍵時發生錯誤: {e}")
    
    def start_scheduler(self):
        """開始定時任務"""
        interval = self.config["interval_minutes"]
        print(f"開始定時按鍵，間隔: {interval} 分鐘")
        print(f"按鍵順序: {self.config['key_sequence']}")
        print("按 Ctrl+C 停止程序")
        
        # 設定定時任務
        schedule.every(interval).minutes.do(self.press_key_sequence)
        
        # 立即執行一次
        self.press_key_sequence()
        
        self.running = True
        while self.running:
            schedule.run_pending()
            time.sleep(1)
    
    def stop(self):
        """停止程序"""
        print("\n正在停止程序...")
        self.running = False
        schedule.clear()
    
    def set_interval(self, minutes):
        """設定按鍵間隔"""
        self.config["interval_minutes"] = minutes
        self.save_config(self.config)
        print(f"已設定按鍵間隔為 {minutes} 分鐘")
    
    def set_key_sequence(self, sequence):
        """設定按鍵順序"""
        self.config["key_sequence"] = sequence
        self.save_config(self.config)
        print(f"已設定按鍵順序為: {sequence}")
    
    def show_config(self):
        """顯示當前設定"""
        print("\n=== 當前設定 ===")
        print(f"間隔時間: {self.config['interval_minutes']} 分鐘")
        print(f"按鍵順序: {self.config['key_sequence']}")
        print(f"按鍵持續時間: {self.config['key_duration']} 秒")
        print(f"按鍵間隔: {self.config['key_interval']} 秒")
        print(f"描述: {self.config['description']}")
        print(f"自動開始: {self.config['auto_start']}")
        print(f"日誌等級: {self.config['log_level']}")

def signal_handler(signum, frame):
    """處理Ctrl+C信號"""
    if auto_keyboard:
        auto_keyboard.stop()
    sys.exit(0)

def main():
    """主函數"""
    global auto_keyboard
    
    print("=== Mac環境定時按鍵盤程序（支援設定檔）===")
    print("此程序將根據設定檔定時按鍵")
    print("注意: 請確保您有權限控制鍵盤輸入")
    print()
    
    # 設定信號處理器
    signal.signal(signal.SIGINT, signal_handler)
    
    # 創建自動鍵盤實例
    auto_keyboard = AutoKeyboard()
    
    # 顯示當前設定
    auto_keyboard.show_config()
    
    # 詢問是否要修改設定
    print("\n是否要修改設定？(y/n，預設n): ", end="")
    modify_config = input().strip().lower()
    
    if modify_config == 'y':
        # 修改間隔時間
        try:
            interval_input = input(f"請輸入按鍵間隔時間（分鐘，當前{auto_keyboard.config['interval_minutes']}分鐘）: ").strip()
            if interval_input:
                interval = float(interval_input)
                if interval > 0:
                    auto_keyboard.set_interval(interval)
                else:
                    print("間隔時間必須大於0，保持原設定")
        except ValueError:
            print("輸入無效，保持原設定")
        
        # 修改按鍵順序
        try:
            sequence_input = input(f"請輸入按鍵順序（用逗號分隔，當前{auto_keyboard.config['key_sequence']}）: ").strip()
            if sequence_input:
                sequence = [key.strip() for key in sequence_input.split(',')]
                if sequence:
                    auto_keyboard.set_key_sequence(sequence)
                else:
                    print("按鍵順序不能為空，保持原設定")
        except Exception as e:
            print(f"輸入無效: {e}，保持原設定")
    
    print()
    print("程序開始運行...")
    print("=" * 50)
    
    # 開始定時任務
    auto_keyboard.start_scheduler()

if __name__ == "__main__":
    auto_keyboard = None
    main()
