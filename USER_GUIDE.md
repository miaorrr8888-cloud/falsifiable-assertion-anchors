# 检查测试是否真的覆盖修复：用户使用指南

## 它能帮你做什么

在临时副本中运行正常测试、撤回指定修复、恢复修复，并检查预期失败信息是否匹配。

## 适合谁

程序员、代码审查者、使用AI生成测试的开发者。

## 具体解决什么问题

测试全绿，但可能根本没有执行到修复的逻辑；撤回修复后测试仍然通过。

**不适合这些目标：**不懂项目时运行陌生代码、自动理解任意缺陷，或把临时目录当安全沙箱。

## 下载与准备

- [打开独立仓库](https://github.com/miaorrr8888-cloud/falsifiable-assertion-anchors)
- [直接下载源码ZIP](https://github.com/miaorrr8888-cloud/falsifiable-assertion-anchors/archive/refs/heads/main.zip)

也可在仓库页面点 Code → Download ZIP。解压后打开包含 SKILL.md、README.md、USER_GUIDE.md 的那层文件夹。不要停在外层目录或只复制一个脚本。

建议使用Windows电脑和Python 3.12；这是本次验证环境。先在该文件夹打开PowerShell，再执行：

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\python.exe --version
```

这里直接使用虚拟环境里的Python，不需要运行激活脚本或修改系统执行策略。安装步骤及其他系统说明见[通用安装说明](https://github.com/miaorrr8888-cloud/agent-skills-worklog/blob/main/INSTALLATION.md)。

本指南的基础示例只用Python标准库，无需安装第三方Python包。

## 第一次使用：先跑自带示例

示例VALUE=2时通过，临时改成VALUE=1后出现指定断言，恢复后再次通过；原项目不被回滚写入。

```powershell
.\.venv\Scripts\python.exe scripts/check_anchor.py --root examples/demo_project --anchor examples/anchor.json
```

## 结果怎么看

status=PASS，baseline=0、rollback=1、restored=0，expected_failure_matched=true。含义是本例反证成立，不是整个项目没有其他问题。

## 换成自己的资料

anchor.json 指定文件、原字符串、回滚字符串、测试命令参数数组和 expected_failure。原字符串必须恰好匹配一次。

先选一项已知修复和对应的可信测试，写一个小锚点；预期失败信息尽量具体。不要整批回滚未知代码，也不要把缺依赖的失败当作断言失败。

## 不想手动敲命令：给AI助手的任务

以下任务适用于能读取所选目录、执行本地命令的助手。WorkBuddy需要先确认当前版本的权限与技能启用状态；本项目未完成WorkBuddy实际导入验收。

```text
请先读取我选定文件夹中的 SKILL.md 和 USER_GUIDE.md，只在该项目范围内处理。
只运行examples/demo_project里的反证示例，解释三次退出码和预期断言的含义。不要运行任何未检查的外部项目命令。之后告诉我怎样为自己的一项小修复建立锚点。
缺少依赖时先说明用途，优先放进本项目虚拟环境；不要读取其他目录中的密码、密钥或浏览器登录数据。
```

## 常见问题

**anchor must match exactly once**

检查文件版本和原字符串，匹配零次或多次都应停下修正。

**baseline failed**

先修复原本测试或环境问题，再验证反证；不能把这个失败计为有效回归测试。

**找不到文件或脚本**

确认终端当前目录就是包含SKILL.md的技能根目录；路径含空格时加双引号。输出目录已存在时换新名字，不覆盖已有结果。

## 当前能力边界

测试仍具有本机程序权限，临时副本不限制外部副作用。正则过宽会降低失败原因判断的可靠性。

## 验证范围

本指南示例已在Windows独立副本中运行复核，见[命令复核结果](https://github.com/miaorrr8888-cloud/agent-skills-worklog/blob/main/USER_GUIDES_VERIFICATION.md)。已有回归测试只覆盖被测试行为，不证明真实业务结果。WorkBuddy实际运行、手机端使用和所有系统版本均不在本次已验证范围内。

许可证和素材来源分别见 [LICENSE](LICENSE)、[PROVENANCE.md](PROVENANCE.md)。
