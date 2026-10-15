# 检查测试是否真的覆盖修复

测试全绿，但可能根本没有执行到修复的逻辑；撤回修复后测试仍然通过。

这个开源技能可以帮助你：在临时副本中运行正常测试、撤回指定修复、恢复修复，并检查预期失败信息是否匹配。

**适合谁：**程序员、代码审查者、使用AI生成测试的开发者。

**怎么开始：**下载并解压独立仓库，按USER_GUIDE先跑自带示例，再换成自己的资料。需要电脑和相应运行环境。

**能看到的结果：**status=PASS，baseline=0、rollback=1、restored=0，expected_failure_matched=true。含义是本例反证成立，不是整个项目没有其他问题。

**使用前知道：**测试仍具有本机程序权限，临时副本不限制外部副作用。正则过宽会降低失败原因判断的可靠性。

[项目与下载入口](https://github.com/miaorrr8888-cloud/falsifiable-assertion-anchors) · [逐步使用指南](https://github.com/miaorrr8888-cloud/falsifiable-assertion-anchors/blob/main/USER_GUIDE.md)

说明：示例、演示与实际业务结果分开记录；介绍文案已准备，尚未发布到自媒体平台。
