# Daily BioMed Log

全自动的每日运行日志，也支持自愿补充生物医学数据科学学习笔记。

## 自动运行

- GitHub Actions 每天新加坡 / 中国时间 **09:17** 运行，**21:17** 再检查一次作为补跑。
- 先运行单元测试和 Python 编译检查，再生成 `entries/YYYY/MM/YYYY-MM-DD.md` 并提交到默认分支 `main`。
- 同一天已有记录就跳过，不重复提交，也不覆盖手写内容。
- 自动记录包含实际运行时间和 Actions 来源链接，并明确说明它是自动化运行记录，**不代表本人当天完成了学习或研究**。
- 提交使用仓库所有者的 GitHub ID 型隐私邮箱，关联到所有者账号；不需要额外 token 或 AI 服务。
- 不创建提醒 Issue，不 @用户，不发送每日催填评论。旧的 Daily learning reminder 工作流已移除。

在 Actions 页面选择 **Automatic daily log → Run workflow** 可手动补跑当天；不会补造过去日期的记录。

GitHub 定时任务可能延迟或被跳过，贡献图也可能延迟最多 24 小时更新，因此不能保证永不漏日。账号关联邮箱、独立仓库和默认分支等条件满足时，提交符合贡献统计条件。GitHub 账号已有的 Actions 通知偏好仍由用户自己的 GitHub 设置控制；本项目不主动发消息。

## 自愿补充学习笔记

在 **Daily learning log inbox** Issue 回复：

```text
/log [Python] 今天弄清了列表推导式和普通 for 循环的区别。
```

分类可以省略。机器人会追加手写内容、回复结果链接，并防止重复处理同一评论。自动记录与人工笔记会明确区分。

也可以在本地运行：

```powershell
.\scripts\add-log.ps1 -Category Python -Text "今天学会了用 pandas 选择缺失值。"
```

仓库公开，请勿写入密码、令牌、学号或病人信息。

## 本地验证

```powershell
python -m unittest discover -s tests -v
python -m py_compile scripts/add_entry.py scripts/auto_entry.py
```

## 官方规则

- [GitHub：贡献统计规则](https://docs.github.com/en/account-and-profile/reference/profile-contributions-reference)
- [GitHub：隐私邮箱格式](https://docs.github.com/en/account-and-profile/reference/email-addresses-reference)
- [GitHub：定时工作流及其限制](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)

## License

[MIT](LICENSE)
