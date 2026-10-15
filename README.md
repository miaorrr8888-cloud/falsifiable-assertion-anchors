# falsifiable-assertion-anchors

Python 3.10+, standard library only.
`python scripts/check_anchor.py --root <project> --anchor <anchor.json>`
Anchor JSON: file, original, rollback, command (an argv array). Run only trusted project tests.
The tool tests baseline, mutation and restoration in a temporary source copy.
A rollback must exit 1; other nonzero codes are not accepted as proof of an assertion failure.

Published by miaorrr8888-cloud with AI-assisted development and cleanup. See PROVENANCE.md and LICENSE.
Validation: run `python -m unittest discover -s tests -v` from this repository root.

## 独立仓库

本仓库只包含 falsifiable-assertion-anchors 一个技能。
源码目录、SKILL.md、许可和相关测试均可独立取得，不依赖其他技能仓库。
工作记录与其他技能入口：[agent-skills-worklog](https://github.com/miaorrr8888-cloud/agent-skills-worklog)。

离线验证：`python -m unittest discover -s tests -v`。
