# 回归测试反证检查

[新手逐步使用指南](USER_GUIDE.md) · [用途与适用人群介绍](INTRODUCTION.md)

`falsifiable-assertion-anchors` · 独立技能仓库 · MIT

适合：希望确认测试确实锁住修复的程序员

## 解决什么问题

在临时副本中撤回一项修复，看测试是否真的会失败，再恢复验证，减少“全绿但没测到问题”。

## 快速开始

Python 3.10+，标准库；只运行自己审核过的测试。

在本仓库根目录运行：

```sh
python scripts/check_anchor.py --root examples/demo_project --anchor examples/anchor.json
```

## 输入与输出

**输入**：anchor.json 指定 file、original、rollback、command 参数数组。{python} 可作为当前解释器占位符。

**输出**：baseline/rollback/restored 退出码与 PASS/FAIL；输入错误或超时不当作修复证明。原项目源码不做回滚写入。

## 本次完善

原有缺口：回滚语法错、字符串命令、超时和符号链接缺少明确边界。

已补：拒绝无效命令和非正超时；先检查 Python 回滚语法；拒绝项目符号链接；提供一个可运行的反证小项目。

## 当前限制

正则仍可过宽，需选择稳定且具体的断言标记。旧格式无 expected_failure 时保留兼容，但 evidence_level 明确为 EXIT_CODES_ONLY；临时副本不是安全沙箱。

## 验证与使用注意

```sh
python -m unittest discover -s tests -v
```

测试覆盖被断言的离线行为，不等于真实平台、生产模型或业务效果验证。

示例数据和图片均为合成演示，不是真实客户、交易、销量或模型成绩。不要提交真实凭据和私有输入。

## 来源与工作记录

由 miaorrr8888-cloud 在 AI 辅助下积累和维护，来源与边界见 [PROVENANCE.md](PROVENANCE.md)，许可见 [LICENSE](LICENSE)。

[全部独立技能与阶段性工作记录](https://github.com/miaorrr8888-cloud/agent-skills-worklog)

## 第二轮：预期失败原因检查

锚点增加 expected_failure 正则；回滚后除退出码外还检查指定断言信息，失败原因不匹配则 FAIL。

在仓库根目录运行：

```sh
python scripts/check_anchor.py --root examples/demo_project --anchor examples/anchor.json
```

新增工具的输入字段见脚本参数与 examples/。快照示例采用固定日期，过期后正常返回 HOLD；需要检查新采集的页面时填写真实带时区的采集时间，不要改日期伪装新证据。
