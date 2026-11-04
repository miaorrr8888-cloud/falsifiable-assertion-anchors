# 回归测试反证检查

[新手逐步使用指南](USER_GUIDE.md) · [用途与适用人群介绍](INTRODUCTION.md)

`falsifiable-assertion-anchors` · 独立技能仓库 · MIT

适合：希望确认测试确实锁住修复的程序员

## 解决什么问题

在临时副本中撤回一项修复，看测试是否真的会失败，再恢复验证，减少“全绿但没测到问题”。

## 安装

```sh
# 纯标准库
python scripts/check_anchor.py --root examples/demo_project --anchor examples/anchor.json
```

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

## 适用用户

**适合：** 需要确认「这次改动真的修好了问题」的开发者——用回滚对照与指定报错来验证测试有效性，
而不是看测试是不是绿的。

**不适合：** 只想要一个测试覆盖率数字的人；
在没有可回滚基线（未提交代码）的项目上使用。

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

## 许可证

MIT，全文见 [LICENSE](LICENSE)。可商用、可修改、可再分发，保留版权与许可声明即可。

**不提供任何形式的担保。** 本技能输出的是辅助判断，不构成法律、财税或平台合规意见；
回滚对照只证明测试有效性，不证明业务结论正确。

第三方依赖各自遵循其原始许可证，本项目不再分发它们的代码或模型权重，详见 `PROVENANCE.md`（如有）。

## 运行环境

| 项 | 状态 |
|---|---|
| Windows 11 + Python 3.12 / 3.13 | ✅ 实测通过 |
| Linux / macOS | ⚠️ **未实测**。代码用 `pathlib`，无硬编码分隔符，理论上可跑，但测试只在 Windows 跑过，不声称支持 |

诚实标注：没实跑过的平台，不要在对外文案里写「已支持」。
