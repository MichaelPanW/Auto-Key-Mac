# Mac環境定時按鍵盤程序（支援設定檔）

這是一個在Mac環境中定時按鍵盤的Python程序，支援JSON設定檔來配置按鍵順序和時間間隔。

## 功能特點

- 支援JSON設定檔配置
- 可自定義按鍵順序和時間間隔
- 實時顯示按鍵時間戳
- 支援Ctrl+C優雅停止
- 錯誤處理和異常捕獲
- 內建設定檔編輯器

## 安裝依賴

在運行程序之前，請先安裝所需的Python依賴項：

```bash
pip install -r requirements.txt
```

或者手動安裝：

```bash
pip install pynput==1.7.6 schedule==1.2.0
```

## 使用方法

### 基本使用

1. 運行程序：
   ```bash
   python main.py
   ```

2. 程序會顯示當前設定並詢問是否要修改
   - 選擇 'y' 來修改設定
   - 選擇 'n' 使用當前設定

3. 程序開始運行後會：
   - 立即執行一次按鍵順序
   - 按照設定的間隔時間定時執行按鍵順序
   - 在控制台顯示每次按鍵的時間戳

4. 停止程序：
   - 按 `Ctrl+C` 停止程序

### 設定檔編輯器

使用內建的設定檔編輯器：

```bash
python config_editor.py
```

或者指定特定的設定檔：

```bash
python config_editor.py my_config.json
```

### 預設設定檔範例

程序包含多個預設設定檔範例：

1. **快速打字模式** (`config_examples/quick_typing.json`)
   - 每30秒按zax
   - 快速按鍵模式

2. **遊戲模式** (`config_examples/gaming.json`)
   - 每2分鐘按WASD
   - 適合遊戲使用

3. **保持活躍模式** (`config_examples/keep_alive.json`)
   - 每5分鐘按空格鍵
   - 防止系統休眠

4. **方向鍵模式** (`config_examples/arrow_keys.json`)
   - 每1分鐘按上下左右方向鍵
   - 基本方向鍵操作

5. **順時針方向鍵** (`config_examples/arrow_keys_clockwise.json`)
   - 每2分鐘按上右下左
   - 順時針方向鍵序列

6. **十字方向鍵** (`config_examples/arrow_keys_cross.json`)
   - 每1.5分鐘按上下左右
   - 十字方向鍵模式

使用範例設定檔：

```bash
cp config_examples/arrow_keys.json config.json
python main.py
```

## 設定檔格式

設定檔使用JSON格式，包含以下參數：

```json
{
  "interval_minutes": 1,
  "key_sequence": ["z", "a"],
  "key_duration": 0.1,
  "key_interval": 0.2,
  "description": "按鍵設定說明",
  "auto_start": false,
  "log_level": "info"
}
```

### 參數說明

- `interval_minutes`: 按鍵間隔時間（分鐘）
- `key_sequence`: 按鍵順序陣列
  - 支援普通字符：`["z", "a", "x"]`
  - 支援方向鍵：`["up", "down", "left", "right"]`
  - 支援特殊鍵：`["space", "enter", "tab", "escape"]`
- `key_duration`: 每個按鍵的持續時間（秒）
- `key_interval`: 按鍵之間的間隔時間（秒）
- `description`: 設定描述
- `auto_start`: 是否自動開始（未來功能）
- `log_level`: 日誌等級（debug/info/warning/error）

### 支援的按鍵類型

#### 方向鍵
- `"up"` - 上方向鍵 ↑
- `"down"` - 下方向鍵 ↓
- `"left"` - 左方向鍵 ←
- `"right"` - 右方向鍵 →

#### 功能鍵
- `"space"` - 空格鍵
- `"enter"` - 回車鍵
- `"tab"` - Tab鍵
- `"escape"` - Esc鍵
- `"backspace"` - 退格鍵
- `"delete"` - 刪除鍵

#### 普通字符
- 所有字母：`a-z`, `A-Z`
- 所有數字：`0-9`
- 符號：`!@#$%^&*()_+-=[]{}|;':",./<>?`

## 注意事項

### 權限設定
在Mac上運行此程序需要授予輔助功能權限：

1. 打開「系統偏好設定」>「安全性與隱私」>「隱私」
2. 選擇「輔助功能」
3. 點擊鎖圖標並輸入密碼
4. 添加您的終端機應用程序（Terminal.app 或 iTerm2）
5. 勾選該應用程序

### 安全提醒
- 此程序會模擬鍵盤輸入，請確保在安全的環境中使用
- 建議在測試環境中先試用
- 不要在不安全的應用程序中使用

## 程序結構

- `main.py` - 主程序文件
- `config_editor.py` - 設定檔編輯器
- `config.json` - 主設定檔
- `config_examples/` - 設定檔範例目錄
- `requirements.txt` - Python依賴項列表
- `README.md` - 使用說明

## 自定義修改

如果您想要修改程序功能：

1. 修改按鍵邏輯：編輯 `press_key_sequence()` 方法
2. 添加新的設定參數：在 `load_config()` 方法中添加預設值
3. 修改日誌格式：編輯日誌輸出部分
4. 添加新的定時任務：在 `start_scheduler()` 方法中添加

## 故障排除

### 常見問題

1. **權限錯誤**：確保已授予輔助功能權限
2. **模組未找到**：確保已安裝所有依賴項
3. **設定檔錯誤**：檢查JSON格式是否正確
4. **程序無法停止**：使用 `Ctrl+C` 或強制終止進程

### 日誌輸出
程序會在控制台顯示詳細的運行日誌，包括：
- 程序啟動信息
- 設定檔載入狀態
- 每次按鍵的時間戳
- 錯誤信息（如果有）

## 版本信息

- Python版本：3.6+
- 依賴項：
  - pynput 1.7.6
  - schedule 1.2.0 