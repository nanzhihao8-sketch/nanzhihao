# 🚀 如何把这个项目发布到 GitHub

> 跟着做，10 分钟搞定。**看不懂就用网页上传法（方法二），不需要任何命令。**

---

## 第 0 步：先装 Git（用命令行法才需要）

打开 PowerShell，粘贴回车：

```powershell
winget install --id Git.Git -e --source winget
```

装完**关掉所有窗口重新打开**，输入 `git --version` 能出版本号就成功了。

> 只用「方法二（网页上传）」的话，**不用装 Git**。

---

## 第 1 步：在 GitHub 建一个空仓库

1. 打开 <https://github.com/new>
2. 填写：

| 字段 | 填什么 |
|---|---|
| **Repository name** | `thunder-deepseek-wechat-bot`（或你喜欢的名字） |
| **Description** | `用 DeepSeek 驱动的微信自动回复脚本，学会你的说话风格` |
| **Public / Private** | 选 **Public**（开源） |
| **Add a README file** | ⚠️ **不要勾**（我们已经有 README 了） |
| **Add .gitignore** | ⚠️ **不要选**（我们已经有 .gitignore 了） |
| **Choose a license** | ⚠️ **不要选**（我们已经有 LICENSE 了） |

3. 点 **Create repository**

建好后页面会显示一堆命令 —— **别急着复制**，先看下面的方法。

---

## 方法一：命令行上传（推荐，以后更新方便）

打开 PowerShell，`cd` 到桌面那个文件夹：

```powershell
cd "$env:USERPROFILE\Desktop\雷霆DeepSeek微信自动回复脚本"

git init
git add .
git commit -m "feat: 雷霆DeepSeek微信自动回复脚本 v1.0.0"
git branch -M main
git remote add origin https://github.com/你的用户名/你的仓库名.git
git push -u origin main
```

> 第一次推送会弹出登录框，用浏览器登录 GitHub 授权即可。

### ⚠️ 推送前务必确认

```powershell
git status
```

**确认列表里没有这些文件**（有的话立刻停下告诉我）：
```
❌ .env                 （含你的 API Key）
❌ persona.txt          （你的人格画像）
❌ chat_history.json    （你的聊天记录）
❌ bot.log              （运行日志）
```

`.gitignore` 已经帮你排除了，但**自己扫一眼最保险**。

---

## 方法二：网页拖拽上传（不用装 Git）

1. 打开你刚建的仓库页面
2. 点 **uploading an existing file**（或 `Add file` → `Upload files`）
3. 把桌面文件夹里的**所有文件**（连同 `stickers` 文件夹）拖进去
4. 下面填提交信息：`feat: v1.0.0 首版发布`
5. 点 **Commit changes**

> 注意：网页上传**不支持空文件夹**，`stickers` 里有 README.md 所以没问题。

---

## 第 2 步：发布 Release（让别人能下 zip）

1. 仓库页面右侧 → **Releases** → **Create a new release**
2. 填写：

| 字段 | 填什么 |
|---|---|
| **Choose a tag** | 输入 `v1.0.0` → 点 "Create new tag" |
| **Release title** | `v1.0.0 首版发布` |
| **Description** | 把桌面 `发布说明.md` 的**全部内容**粘贴进去 |
| **Attach binaries** | 把桌面 `雷霆DeepSeek微信自动回复脚本.zip` **拖进去上传** |

3. 点 **Publish release**

这样别人在 Releases 页面既能看说明，又能**直接下载 zip**。

---

## 第 3 步：之后怎么更新？

改了代码后：

```powershell
cd "$env:USERPROFILE\Desktop\雷霆DeepSeek微信自动回复脚本"
git add .
git commit -m "fix: 修了某个 bug"
git push
```

新版本发布：再走一遍第 2 步，tag 用 `v1.0.1`。

---

## 📋 给仓库加个好看的描述（可选）

在仓库页面右上角 **⚙️ Settings** → **General** 里可以改：

**Topics**（标签，方便别人搜到）：
```
wechat  deepseek  chatbot  auto-reply  python  wechat-bot  llm  ai
```

**About**（右上角 ✏️ 编辑）：
```
⚡ 用 DeepSeek 驱动的微信自动回复脚本 | 学会你的说话风格 · 图片识别 · 表情包 · 熔断保护
```

---

## ⚠️ 开源前的最后检查

- [ ] 仓库里**没有** `.env`（API Key）
- [ ] 仓库里**没有** `persona.txt`（人格画像，含真名）
- [ ] 仓库里**没有** `chat_history.json`（聊天记录）
- [ ] 仓库里**没有** `bot.log`
- [ ] README 里的联系方式/署名是**你愿意公开的**

**都确认了再点 push。**
