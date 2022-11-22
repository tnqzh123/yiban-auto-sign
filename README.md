# 易班 易伴云 网薪签到 自动化脚本

![yiban-sign-page](https://s1.ax1x.com/2022/09/15/vzplSH.jpg)

Python 实现的易班易伴云网薪签到自动化脚本。可与 GitHub Actions 或其他 CI/CD 平台配合使用实现每日定时签到，防止断签。

## 使用说明

要求 Python 版本不低于 3.8。

**注意**：首次使用前需要在易班网页端或 App 手动签到一次，以确保授予易伴云相关权限；此外，根据观察，每隔一个月左右，易伴云就会重新要求 OAuth 授权，若未及时授权，将导致签到失败，请注意。

### 本地部署

1. Clone 这个仓库到本地
2. 编辑 `config.json`
   - 将 `phone` 的值修改为你的易班账户绑定的手机号
   - 将 `password` 的值修改为你的易班账户的密码
3. 安装依赖
   - `pip install -r requirements.txt`
4. 运行 `yiban-auto-sign.py`

可与 Crontab 等实用工具配合实现自动化签到。

### 使用 CI/CD 平台实现自动化签到

#### GitHub Actions

> 近期发现 GitHub Actions 构建节点与易伴云服务器之间存在连接性问题，容易连接超时，导致签到失败。如有条件，建议使用其他 CI/CD 平台，或部署至自有环境。

1. [Fork](https://github.com/tnqzh123/yiban-auto-sign/fork) 这个仓库
2. 在仓库的 Settings -> Security -> Secrets -> Actions 中新建两条 repository secret：
   - `YIBAN_PHONE`，值为你的易班账户绑定的手机号
   - `YIBAN_PASSWORD`，值为你的易班账户的密码
3. 启用 GitHub Actions
   - 进入仓库的 Actions 页面，点击绿色的「I understand my workflows, go ahead and enable them」按钮
      - 出于安全考虑，GitHub 会对 Fork 时存在 Workflow 文件的仓库禁用 Actions，需要用户手动确认安全才会启用。
      - 如果仓库没有 Actions 页面，请进入仓库的 Settings -> Code and automation -> Actions -> General -> Actions permissions 检查是否允许运行 Actions。

默认每天早上八点自动触发 Workflow 发起签到（GitHub Actions 高负载时可能延迟）。如需修改为其他时间或条件下签到，可按照 GitHub [文档](https://docs.github.com/cn/actions/using-workflows/triggering-a-workflow)修改 `.github/workflows/sign.yml`。

订阅 GitHub Actions 的 [Workflow 运行通知](https://docs.github.com/cn/actions/monitoring-and-troubleshooting-workflows/notifications-for-workflow-runs)，可在签到失败（Workflow 执行失败）时收到通知提醒。

#### 其他 CI/CD 平台

1. 将这个仓库的代码上传到你想使用的 CI/CD 平台
2. 新建三条环境变量：
   - `GITHUB_ACTIONS`，值为 `true`（大小写敏感，请注意）
   - `YIBAN_PHONE`，值为你的易班账户绑定的手机号（建议设为 Secret）
   - `YIBAN_PASSWORD`，值为你的易班账户的密码（建议设为 Secret）
3. 编写你的 Workflow：
   1. 根据 `requirements.txt` 中的内容安装依赖（建议缓存依赖）
      - `pip install -r requirements.txt`
   2. 运行 `yiban-auto-sign.py`

## License

MIT License.
