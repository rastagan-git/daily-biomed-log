# Daily BioMed Log

一个低摩擦的生物医学数据科学学习日志：每天写下一条真实收获，GitHub Actions 会把它整理成当天的 Markdown 文件并提交到 `main`。

## 最简单的用法

1. 打开仓库中标题为 **Daily learning log inbox** 的固定 Issue。
2. 回复一条命令：

   ```text
   /log [Python] 今天弄清了列表推导式和普通 for 循环的区别。
   ```

3. 等待大约一分钟。机器人会回复当天记录的链接，并给原评论加一个 🎉。

分类是可选的；下面这样也可以：

```text
/log 复习了矩阵乘法的维度规则。
```

每晚北京时间 21:17，如果当天还没有记录，机器人会在固定 Issue 中提醒一次。

## 它如何工作

- 只有仓库所有者发出的 `/log` 评论会被处理。
- 评论内容写入 `entries/YYYY/MM/YYYY-MM-DD.md`。
- 自动生成的 commit 使用评论者的 GitHub ID 型隐私邮箱，因此无需公开真实邮箱。
- commit 直接进入默认分支 `main`，符合 GitHub 的贡献统计条件。
- 同一条评论即使重新运行工作流，也不会重复写入。

GitHub 的贡献图可能需要最多 24 小时才显示新贡献。绿格是学习留下的副产品，不是项目拿空气压出来的草坪贴纸。

## 本地记录

如果更喜欢终端，可以在 PowerShell 中运行：

```powershell
.\scripts\add-log.ps1 -Category Python -Text "今天学会了用 pandas 选择缺失值。"
```

脚本会创建或追加当天文件，然后只提交 `entries` 中对应的记录并推送。

## 记录建议

每天写一条就够了，例如：

- 一个新概念；
- 一段刚调通的代码；
- 一个尚未解决的问题；
- 一篇论文的核心结论；
- 一次实验失败以及原因。

仓库是公开的，请不要写密码、令牌、学号、病人信息或其他敏感数据。

## 本地验证

```powershell
python -m unittest discover -s tests -v
python -m py_compile scripts\add_entry.py
```

## 官方规则

- [GitHub：个人资料贡献统计规则](https://docs.github.com/en/account-and-profile/reference/profile-contributions-reference)
- [GitHub：隐私邮箱格式](https://docs.github.com/en/account-and-profile/reference/email-addresses-reference)
- [GitHub：定时工作流](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)

## License

[MIT](LICENSE)
