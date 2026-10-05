# 本地长期档案

此工具为本机单一使用者保存精简档案，不是聊天仓库，不是多会员管理系统。没有明确同意时只使用当前对话；为他人咨询时不要写入本人档案。所有命令从总控 skill 目录运行，Python 路径按宿主选择；中文环境推荐 `python -X utf8`。

## 历史信息硬边界

宿主应用可能提供其他会话的摘要或上下文，但它们不等于本 skill 的用户档案，也不能自动视为用户已经报告过的事实。当前对话中的明确陈述，或下面所述在有效同意后成功召回的本地记录，才能作为已确认的跨对话历史。来源不明、冲突或缺少日期的历史只能作为待确认线索；向用户核实后再写入档案，不得用“基于你之前的情况”掩盖不确定性。

跨对话服务不要求每次从零开始。若档案状态为 active，先按当前需求召回必要字段；若状态为 disabled、paused 或 revoked，说明档案不可用，并只询问会改变当前建议的最少信息。不要因为一次未启用档案就声称用户没有任何历史。

## 同意与状态

先运行 `python -X utf8 scripts/memory_store.py status`。未启用时询问是否允许本机保存精简的健身目标、计划和反馈；说明这是未加密的本地数据，同意后按必要变化更新，可随时查看、暂停、撤销和删除。拒绝后本轮不重复询问，服务继续。

只有用户明确同意保存，才运行 `python -X utf8 scripts/memory_store.py enable --confirm`。实现工具本身或要求写 skill 不等于授权保存个人健康资料。

默认目录：Windows 使用本机 `LOCALAPPDATA/CoachI WannaWorkout`，其他系统使用 `~/.local/share/coach-i-wanna-workout`。高级用户可设置绝对路径 `WORKOUT_MEMORY_DIR`；必须是本人私密、非仓库、非公开或同步目录。脚本阻止当前仓库、Git 仓库和常见公开/同步目录；不保证识别所有云盘或代替系统访问权限。不要设置到公共目录或多人共享位置。

## 记录结构与来源

`apply` 接收单个对象或最多 50 条对象的数组，每个对象必须包含以下六个字段：

```json
{
  "scope": "user",
  "field": "goal",
  "value": "希望增肌，每周训练三次",
  "source_type": "user_report",
  "source_ref": "当前对话中用户明确回答",
  "occurred_at": "2026-10-04"
}
```

日期使用事实发生或报告的用户当地日期，示例日期不自动套用。数字保留单位和计量条件，未知不写，估算不能保存成已核实测量。

| scope | 允许的 field | 来源 |
| --- | --- | --- |
| user | goal、age_band、experience、schedule、equipment、preferences、constraints、height_cm、weight_kg、medical_context | 只允许 user_report；稳定事实须用户明确陈述 |
| plan | training、nutrition、mobility、recovery | coach_plan 或 user_report；值中标明这是教练建议还是用户报告的现有计划 |
| event | 稳定英文标识，如 workout_2026-10-04、review_2026-10-11 | user_report 或 measurement；可核对的用户叙述或测量，并附来源 |

不保存原始聊天、照片、完整病历、身份资料或模型诊断。症状、疾病和用药仅保存用户明确提供且影响当前建议的必要摘要，注明“用户报告”，不从模型推断补事实。measurement 的值中注明测量方法和误差，工具结果不能自动改写稳定用户事实。

## 更新与召回

使用结构化工具或 UTF-8 JSON 文件传入，避免把健康内容直接拼进命令行：

```text
python -X utf8 scripts/memory_store.py apply --file /absolute/private/update.json
```

也支持 `--file -` 从标准输入接收 JSON。临时输入文件只能放私密目录，使用后按用户授权清理；不要留在公开仓库。脚本按 scope + field 覆盖，同一事件重复更新原记录。完全相同的内容不重复创建撤销历史。

默认总记录最多 100 条，事件最多 20 条（按发生日期保留最近的），撤销历史最多 20 次。单条用户字段最多约 1000 JSON 字符、计划 6000、事件 600；先压缩低价值内容，不能扩容绕过限制。

跨对话开始，确认状态 active 后按当前需要运行：

```text
python -X utf8 scripts/memory_store.py context --max-chars 4000
python -X utf8 scripts/memory_store.py context --scope plan --max-chars 6000
```

仅加载必要信息；最近事件最多召回 8 条，记录 JSON 总长度受 max-chars 控制。omitted 非零表示部分记录未加载，不把“未召回”当成“不存在”。旧档案带日期，应询问是否仍有效，特别是症状和医疗限制。不要把召回内容作为本轮新事实再次保存。

更新成功后用一句话说明改了什么和如何撤销。脚本失败、无权限或不可用时说明没有保存，提供交接摘要；不得改写工具结果声称成功。暂停或撤回同意时不自动读或写；show 仅用于用户明确要求查看。

## 用户控制

| 用户请求 | 命令与行为 |
| --- | --- |
| 查看档案 | `show`，可加 `--scope user/plan/event`，展示结果中的相关字段 |
| 暂停 / 恢复 | `pause` / `resume`，保留数据；已撤回同意时 resume 不能重新启用 |
| 撤销刚才更新 | `undo`，撤销最近一批 apply，最多保留 20 批；只在 active 时允许 |
| 删除某项 | `forget --scope user --field medical_context --confirm`；先确定准确字段，删除并清除全部撤销历史，避免复原已删除资料 |
| 撤回同意，保留数据 | `revoke --confirm`；停止自动读取和写入，清除撤销历史 |
| 撤回并删除全部 | `revoke --delete --confirm`；清除记录与撤销历史，停用 |
| 清空全部但继续启用 | `clear --confirm`；清除记录与撤销历史，保留当前同意状态 |

`--confirm` 是工具保护参数，不是用户同意的替代；用户明确要求删除或撤回时可直接执行准确范围，不重复询问。普通暂停、撤回和删除保留空数据库或状态，不删除整个用户目录。

SQLite 使用事务和 secure_delete 清除库内记录；此机制无法清除用户另外创建的备份、操作系统快照或同步副本，不声称法证级擦除。档案工具不提供自动提醒；没有宿主调度工具时只能约定复查时间，不能声称会主动唤醒。
