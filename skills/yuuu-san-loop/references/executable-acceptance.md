# 执行验收

已有项目验收入口能逐项证明检查确实运行并通过、核对运行环境和最终候选时，复用它的原始报告和校验命令。否则，用 [verify_checks.py](../scripts/verify_checks.py) 运行 Git 候选上的命令，逐项校验原始报告。脚本使用 Python 3.11 及以上版本和 Git。

## 固定清单

以用户目标、项目必验项和原触发条件确定清单。在看到结果前保存清单和摘要到任务记录，保留在运行目录之外。修订时保留原清单、原结果和变更依据，独立复核必要检查仍覆盖验收要求。范围调整、替代验证和人工检查按 [SKILL.md](../SKILL.md) 的完成条件核对。

以下清单中的命令和用例名称按项目实际入口填写。

```json
{
  "checks": [
    {
      "id": "recovery",
      "argv": ["node", "--test", "test/recovery.test.mjs"],
      "report": "node-test",
      "cases": [["relation recovery", "restart resumes"], ["relation recovery", "SIGTERM releases lock"]],
      "os": "Linux",
      "timeout_seconds": 180
    },
    {
      "id": "typecheck",
      "argv": ["node", "node_modules/typescript/bin/tsc", "--noEmit"],
      "report": "exit",
      "timeout_seconds": 180
    }
  ]
}
```

- `node-test` 给 `node --test` 加载随附的 [原始事件报告器](../scripts/node_test_reporter.mjs)，需要提供完整测试汇总的 Node 版本，本机以 Node 22.23.4 验证。按从外到内的套件名和用例名列齐必验项，同名路径可按文件拆分。测试组和文件级记录不计作用例。顶层用例与源文件同名时，用不同的名称或套件路径指认该用例。原进程须退出 0，失败、跳过、取消或 TODO 均判未通过。其他测试框架用项目已有的校验器。
- `exit` 用于退出码本身能证明完成的命令，如类型检查。带跳过或跳选能力的测试使用能逐项验证的报告或项目校验器。
- `os` 为可选的实际运行系统要求。涉及原生信号等行为时，在所需环境执行脚本，并用项目约定的方式核对专库、服务、依赖等条件。命令参数和证据存放在受控位置，使用合成数据，避免把凭据写入清单或日志。

## 运行与核验

`SCRIPT` 指向技能内的 `scripts/verify_checks.py`。从脚本第一次输出取得 `HASH`，其他参数按实际绝对路径填写。使用同一个干净工作树运行与再核验，脚本核对提交和工作树根，并拒绝隐藏改动的 Git 索引标记。证据保存于仓外新目录。同一版本的失败和重跑分别留存。多仓任务每个责任仓使用相应候选和回执。非 Git 或只读任务沿用项目已有的版本绑定和授权边界。

```text
python SCRIPT freeze PLAN
python SCRIPT run PLAN HASH REPO NEW_EVIDENCE_DIRECTORY
python SCRIPT verify PLAN HASH REPO EVIDENCE_DIRECTORY
```

`run` 保存完整标准输出、标准错误和运行记录，随后执行同样的核验。缺少报告、用例漏跑、版本不符或校验失败时返回非零。修复和独立复查完成后，对要交付的版本再运行 `verify`，核对退出码 0 和返回的 `status: passed`。该回执证明固定清单内的可执行检查通过，最终结案还需核对历轮事项和独立复查证据。

脚本依赖可信的清单、命令和证据来源。若项目另有获授权的 Hook、CI 或发布门槛，可以调用它并依据退出码决定是否放行。需要强制拦截时，由受保护的执行入口持有清单摘要和可信运行结果。
