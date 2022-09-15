# 易班 易伴云 网薪签到 自动化脚本

![yiban-sign-page](https://s1.ax1x.com/2022/09/15/vzplSH.jpg)

Python 实现的易班易伴云网薪签到自动化脚本。可与 GitHub Actions 配合使用实现每日定时签到，防止断签。

## 使用说明

要求 Python 版本不低于 3.7。

**注意**：首次使用前需要在易班网页端或 App 手动签到一次，以确保授予易伴云相关权限。

### 本地部署

1. Clone 这个仓库到本地
2. 编辑 `config.json`
   - 将 `phone` 的值修改为你的易班账户绑定的手机号
   - 将 `password` 的值修改为你的易班账户的密码
3. 安装依赖
   - `pip install -r requirements.txt`
4. 运行 `yiban-auto-sign.py`

可与 Crontab 等实用工具配合实现自动化签到。

### GitHub Actions 自动化签到

1. [Fork](https://github.com/tnqzh123/yiban-auto-sign/fork) 这个仓库
2. 在仓库的 Settings -> Security -> Secrets -> Actions 中新建两条 repository secret：
   - `YIBAN_PHONE`，值为你的易班账户绑定的手机号
   - `YIBAN_PASSWORD`，值为你的易班账户的密码

默认每天早上八点自动触发 Workflow 发起签到（GitHub Actions 高负载时可能延迟）。如需修改为其他时间或条件下签到，可按照 GitHub [文档](https://docs.github.com/cn/actions/using-workflows/triggering-a-workflow)修改 `.github/workflows/sign.yml`。

订阅 GitHub Actions 的 [Workflow 运行通知](https://docs.github.com/cn/actions/monitoring-and-troubleshooting-workflows/notifications-for-workflow-runs)，可在签到失败（Workflow 执行失败）时收到通知提醒。

## License

MIT License.
