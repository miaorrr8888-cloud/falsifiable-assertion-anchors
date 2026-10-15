---
name: falsifiable-assertion-anchors
description: 在临时源码副本中回滚指定修复，检查测试能否发现缺陷，适用于验证回归测试是否有效。
license: MIT
---

# 可证伪断言检查

使用 `scripts/check_anchor.py --root <project> --anchor <anchor.json>`。锚点 JSON 包含 file、original、rollback 与 command（参数数组），格式见 README.md。

选择具体修复及对应的可信测试。original 必须精确出现一次，且与 rollback 不同；失配不能算通过。

工具在临时副本中先运行原测试，再替换修复并运行，再恢复并运行。baseline=0、rollback=1、restored=0 是必要条件；提供 expected_failure 时还必须匹配预期失败信息，否则 FAIL。未提供该字段时仅为 EXIT_CODES_ONLY，不能据此认定失败原因。原项目不做回滚写入。安装、语法或网络故障的退出码不能当作断言失败证明；要在隔离目录中核实失败原因。

测试在回滚后仍通过时，检查断言过宽、未执行目标分支或其他变量干扰。不要为了反证而削弱原测试。

仅运行已检查、获准执行的测试命令。临时复制不是安全沙箱，测试程序仍有本机进程权限；本工具不限制网络与任意代码副作用。

## 上手示例与当前限制

先读 [README.md](README.md) 的快速开始、输入输出和未完成项；可运行例子在 examples/，本次修订见 CHANGELOG.md。不要把合成演示或离线检查当成真实平台验证。

## 扩展能力

锚点增加 expected_failure 正则；回滚后除退出码外还检查指定断言信息，失败原因不匹配则 FAIL。 使用前阅读 [README.md](README.md) 的“第二轮”命令和当前限制。不要把本地检查、人工声明或模拟响应解释为实时平台验证。

## 面向使用者的说明

解释用途、适用人群、下载和第一次运行时，读 [USER_GUIDE.md](USER_GUIDE.md)；需要中文对外介绍时参考 [INTRODUCTION.md](INTRODUCTION.md)，不要把介绍稿等同于已发布。
