import os
import json
import re
import urllib.request

repo = os.environ.get("GITHUB_REPOSITORY")
token = os.environ.get("GITHUB_TOKEN")

if not repo or not token:
    print("❌ 缺少必要的環境變數")
    exit(1)

url = f"https://api.github.com/repos/{repo}/releases?per_page=100"
req = urllib.request.Request(url)
req.add_header("Authorization", f"Bearer {token}")
req.add_header("Accept", "application/vnd.github.v3+json")

print("正在獲取 Release...")
with urllib.request.urlopen(req) as response:
    releases = json.loads(response.read().decode('utf-8'))

history_content = "# 版本更新記錄\n\n"

for rel in releases:
    tag = rel.get("tag_name", "")
    date = rel.get("published_at", "")[:10]
    body = rel.get("body", "") or ""
    
    # 1. 截斷 Magisk 警告及後續內容
    magisk_keyword = "Assets 裡的 zip 格式壓縮包"
    if magisk_keyword in body:
        body = body.split(magisk_keyword)[0]
        
    # 2. 逐行過濾 [!NOTE] / [!WARNING] 等塊
    cleaned_lines = []
    in_alert = False
    for line in body.split('\n'):
        stripped = line.strip()
        
        # 開啟警報遮罩
        if re.match(r'^>\s*\[!(?:NOTE|WARNING|IMPORTANT|TIP|CAUTION)\]', stripped, re.IGNORECASE):
            in_alert = True
            continue
        
        # 如果處於遮罩狀態
        if in_alert:
            if stripped.startswith('>'): 
                continue # 繼續過濾掉警告下面的 > 內容（包括 > ⚠️）
            else:
                in_alert = False # 遇到普通段落，解除遮罩
                
        # 強制過濾單獨的 > ⚠️ 行（防止漏網）
        if stripped.startswith('>') and "⚠️" in stripped:
            continue
            
        # 強制過濾包含網盤網址的整行
        if "http://lxgw.ys168.com" in line:
            continue
            
        # 3. 過濾 Full Changelog 和包含“更新日誌”的行
        if "**Full Changelog**" in line or "更新日誌" in line:
            continue
        if "compare" in line and "https://github.com" in line:
            continue
            
        cleaned_lines.append(line)
        
    body = '\n'.join(cleaned_lines)
    # 4. 清理連續空行
    body = re.sub(r'\n{3,}', '\n\n', body).strip()

    if body: 
        history_content += f"## [{tag}] - {date}\n\n{body}\n\n---\n\n"

# ================= 新增：全域清理 =================
# 5. 合併連續的分隔線（允許中間有空行），統一替換為單個 ---
history_content = re.sub(r'(?m)^\s*---\s*$\s*(?:^---\s*$\s*)+', '---\n\n', history_content)

# 6. 清理因為合併 --- 可能產生的多餘空行
history_content = re.sub(r'\n{3,}', '\n\n', history_content)
# ==================================================

with open("HISTORY.md", "w", encoding="utf-8") as f:
    f.write(history_content)
    
print("✅ HISTORY.md 生成完畢！")
