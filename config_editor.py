#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
設定檔編輯工具
用於編輯 AutoKeyboard 程序的設定檔
"""

import json
import os
import sys

def load_config(config_file="config.json"):
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
    
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # 合併預設設定
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
                return config
        except Exception as e:
            print(f"載入設定檔失敗: {e}")
            return default_config
    else:
        return default_config

def save_config(config, config_file="config.json"):
    """儲存設定檔"""
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"✅ 設定檔已儲存: {config_file}")
        return True
    except Exception as e:
        print(f"❌ 儲存設定檔失敗: {e}")
        return False

def show_config(config):
    """顯示設定"""
    print("\n=== 當前設定 ===")
    print(f"1. 間隔時間: {config['interval_minutes']} 分鐘")
    print(f"2. 按鍵順序: {config['key_sequence']}")
    print(f"3. 按鍵持續時間: {config['key_duration']} 秒")
    print(f"4. 按鍵間隔: {config['key_interval']} 秒")
    print(f"5. 描述: {config['description']}")
    print(f"6. 自動開始: {config['auto_start']}")
    print(f"7. 日誌等級: {config['log_level']}")
    print("8. 儲存並退出")
    print("0. 退出（不儲存）")

def edit_config(config):
    """編輯設定"""
    while True:
        show_config(config)
        choice = input("\n請選擇要編輯的項目 (0-8): ").strip()
        
        if choice == '0':
            print("退出編輯器")
            return False
        elif choice == '1':
            try:
                value = float(input(f"請輸入新的間隔時間（分鐘，當前{config['interval_minutes']}）: "))
                if value > 0:
                    config['interval_minutes'] = value
                    print("✅ 間隔時間已更新")
                else:
                    print("❌ 間隔時間必須大於0")
            except ValueError:
                print("❌ 輸入無效")
        elif choice == '2':
            try:
                sequence_input = input(f"請輸入新的按鍵順序（用逗號分隔，當前{config['key_sequence']}）: ")
                if sequence_input.strip():
                    sequence = [key.strip() for key in sequence_input.split(',')]
                    if sequence:
                        config['key_sequence'] = sequence
                        print("✅ 按鍵順序已更新")
                    else:
                        print("❌ 按鍵順序不能為空")
                else:
                    print("❌ 輸入不能為空")
            except Exception as e:
                print(f"❌ 輸入無效: {e}")
        elif choice == '3':
            try:
                value = float(input(f"請輸入新的按鍵持續時間（秒，當前{config['key_duration']}）: "))
                if value > 0:
                    config['key_duration'] = value
                    print("✅ 按鍵持續時間已更新")
                else:
                    print("❌ 按鍵持續時間必須大於0")
            except ValueError:
                print("❌ 輸入無效")
        elif choice == '4':
            try:
                value = float(input(f"請輸入新的按鍵間隔（秒，當前{config['key_interval']}）: "))
                if value >= 0:
                    config['key_interval'] = value
                    print("✅ 按鍵間隔已更新")
                else:
                    print("❌ 按鍵間隔不能為負數")
            except ValueError:
                print("❌ 輸入無效")
        elif choice == '5':
            value = input(f"請輸入新的描述（當前{config['description']}）: ")
            if value.strip():
                config['description'] = value.strip()
                print("✅ 描述已更新")
            else:
                print("❌ 描述不能為空")
        elif choice == '6':
            value = input(f"是否自動開始？(y/n，當前{config['auto_start']}): ").strip().lower()
            if value in ['y', 'yes', 'true']:
                config['auto_start'] = True
                print("✅ 自動開始已設為 True")
            elif value in ['n', 'no', 'false']:
                config['auto_start'] = False
                print("✅ 自動開始已設為 False")
            else:
                print("❌ 輸入無效，請輸入 y 或 n")
        elif choice == '7':
            value = input(f"請輸入新的日誌等級（debug/info/warning/error，當前{config['log_level']}）: ").strip().lower()
            if value in ['debug', 'info', 'warning', 'error']:
                config['log_level'] = value
                print("✅ 日誌等級已更新")
            else:
                print("❌ 日誌等級必須是 debug、info、warning 或 error")
        elif choice == '8':
            return True
        else:
            print("❌ 無效的選擇，請輸入 0-8")

def main():
    """主函數"""
    print("=== AutoKeyboard 設定檔編輯器 ===")
    
    config_file = "config.json"
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
    
    print(f"設定檔: {config_file}")
    
    # 載入設定
    config = load_config(config_file)
    
    # 編輯設定
    if edit_config(config):
        # 儲存設定
        save_config(config, config_file)
        print("設定已儲存並退出")
    else:
        print("設定未儲存")

if __name__ == "__main__":
    main() 