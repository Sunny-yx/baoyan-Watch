# BaoyanWatch

BaoyanWatch 是一个面向保研学生的通知监控工具。你可以 fork 这个项目，在 `config/schools.yaml` 里填入自己关注的学校和学院官网，GitHub Actions 会每天自动检查是否有新的夏令营、预推免、九推、十推等通知，并在发现新通知时发送邮件提醒。

第一版是个人自用型 MVP：不需要服务器，只需要 GitHub 账号和一个可用于发信的邮箱。

## 它能做什么

- 定时抓取学校 / 学院官网通知页面
- 根据关键词筛选保研相关通知
- 识别新增通知，避免重复提醒
- 发送邮件摘要
- 生成 `docs/latest.md` 汇总文件

默认样例会监控南方科技大学自动化与智能制造学院官网，并匹配：

- 全国优秀大学生
- 暑期
- 营

## 快速开始

### 1. Fork 项目

点击 GitHub 页面右上角的 **Fork**，把项目复制到自己的账号下。

### 2. 修改关注列表

打开 `config/schools.yaml`，按下面格式添加自己关注的学院官网：

```yaml
sources:
  - id: sustech-aim
    school: 南方科技大学
    college: 自动化与智能制造学院
    url: https://aim.sustech.edu.cn/
    enabled: true
    match_mode: all
    keywords:
      - 全国优秀大学生
      - 暑期
      - 营
```

字段说明：

- `id`：每个来源的唯一名称，建议用英文和短横线。
- `school`：学校名称。
- `college`：学院名称。
- `url`：通知页面或学院首页地址。
- `enabled`：是否启用。
- `match_mode`：`any` 表示命中任意关键词即可，`all` 表示必须同时命中全部关键词。
- `keywords`：该来源单独使用的关键词；不填时使用 `config/keywords.yaml` 的全局关键词。

如果某个网站结构比较特殊，可以额外配置 CSS 选择器：

```yaml
selectors:
  item: ".news-list li"
  title: "a"
  link: "a"
  date: ".date"
```

### 3. 设置邮件密钥

进入 GitHub 仓库页面：

`Settings` -> `Secrets and variables` -> `Actions` -> `New repository secret`

添加这些 Secrets：

| 名称 | 含义 |
| --- | --- |
| `SMTP_HOST` | 发件邮箱 SMTP 地址，例如 `smtp.qq.com` |
| `SMTP_PORT` | SMTP 端口，例如 `465` |
| `SMTP_USER` | 发件邮箱账号 |
| `SMTP_PASSWORD` | 发件邮箱授权码或密码 |
| `MAIL_TO` | 收件邮箱，例如 `your-email@example.com` |

QQ 邮箱通常需要在邮箱设置里开启 SMTP，并使用“授权码”作为 `SMTP_PASSWORD`。

> 隐私提示：请不要把真实邮箱、SMTP 授权码、Cookie、Token 或其他个人信息写进仓库文件里。把它们放在 GitHub Actions Secrets 中即可，fork 后每个用户都需要在自己的仓库里单独配置。

### 4. 手动运行一次

进入 GitHub 仓库页面：

`Actions` -> `BaoyanWatch Monitor` -> `Run workflow`

如果有新增通知，会收到邮件；同时项目会更新：

- `data/seen.json`
- `docs/latest.md`

## 本地运行

安装依赖：

```bash
pip install -r requirements.txt
```

执行一次检查但不发送邮件：

```bash
python -m src.main --no-email
```

执行测试：

```bash
pytest
```

## 注意事项

- BaoyanWatch 只做通知提醒，不判断报名资格、截止时间是否变更，也不解释招生政策。
- 请始终点击原始官网链接确认最终信息。
- 建议每天检查 1 次，不要高频抓取学校官网。
- 第一版不支持公众号、小程序、登录后页面、验证码页面和复杂 JS 渲染页面。
