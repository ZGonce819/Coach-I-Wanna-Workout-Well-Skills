# Coach I Wanna Workout Well Skills

一个以循证知识库为基础的健身教练 skill 系统，覆盖训练、饮食、原理解释、热身与恢复。

从用户目标和现实条件出发，按需检索相关知识，交付可执行的方案，并根据实际完成情况、训练表现和恢复反馈持续调整。当前包含一个总控、五个领域 skill、接待与案例模板，以及默认关闭的本地长期档案工具。

## 安装

本技能以目录形式加载：把整个技能包放进豆包的用户技能目录，重启客户端即可使用。

### 1. 获取技能包

```text
git clone git@github.com:ZGonce819/Coach-I-Wanna-Workout-Well-Skills.git
```

没有 Git 时，在仓库页面 Download ZIP 后解压。技能包是 `Coach-I-Wanna-Workout-Well-Skills/` 整个目录；知识库、引用模板和本地工具都在该目录内，不能只复制单个 `SKILL.md`。

### 2. 找到用户技能目录

豆包 Windows 客户端的用户技能目录通常为：

```text
<用户数据目录>\User Data\Default\.doubao\agent_mode\workspace\.user_skills\
```

本机默认路径示例（将 `<用户名>` 替换为实际 Windows 用户名）：

```text
C:\Users\<用户名>\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\.user_skills\
```

### 3. 放入技能包

将 `Coach-I-Wanna-Workout-Well-Skills/` 整个目录复制到上述 `.user_skills\` 下，并重命名为技能名（全小写连字符）：

```text
.user_skills\coach-i-wanna-workout-well\
```

复制后校验目录结构，必须包含以下条目：

```text
coach-i-wanna-workout-well\
|-- SKILL.md                              # 总控
|-- Coach-I-Wanna-Train-Well-Skill\       # 五个领域子 skill
|-- Coach-I-Wanna-Eat-Well-Skill\
|-- Coach-I-Wanna-Know-Well-Skill\
|-- Coach-I-Wanna-Flex-Well-Skill\
|-- Coach-I-Wanna-Recover-Well-Skill\
|-- knowledge-base\                       # 导读索引 + 三十九份主题指南
|-- references\                           # 接待与反馈、案例模板
`-- scripts\memory_store.py               # 本地档案工具（默认关闭）
```

### 4. 重启并验证

重启豆包客户端（或新开对话），然后提问：

- “帮我制定一个增肌训练计划” —— 应进入总控接待与筛查流程
- “深蹲怎么做才是对的？” —— 应从知识库动作技术主题作答

若回答明显未使用知识库，依次检查：目录名是否为 `coach-i-wanna-workout-well`、`SKILL.md` 是否位于技能目录根、`knowledge-base\` 是否完整。

### 更新与卸载

- **更新**：`git pull` 获取最新内容后，用仓库内 `Coach-I-Wanna-Workout-Well-Skills/` 整体覆盖已安装副本，保持技能目录名不变。
- **卸载**：删除 `.user_skills\coach-i-wanna-workout-well\` 目录即可。本地档案数据库（`memory.sqlite3`）存放在技能目录之外的独立位置；曾启用过档案的需要单独清除（见[本地长期档案](#本地长期档案)）。

## 使用入口

综合需求从 [总控 skill](Coach-I-Wanna-Workout-Well-Skills/SKILL.md) 开始，单一需求也可以直接使用对应领域。安装时请复制完整的 `Coach-I-Wanna-Workout-Well-Skills/` 目录；知识库、引用模板和本地工具已经放在这个目录内，不能只复制一个 `SKILL.md`。

可以这样开始：

```text
我是抗阻训练新手，想增肌，每周能练三天，每次五十分钟，
在普通健身房训练。帮我制定首周计划，并告诉我训练后反馈什么。
```

也可以提出局部问题：

- “今天只有三十分钟，原计划怎么精简？”
- “我七十公斤，增肌一天需要多少蛋白？经常外食怎么安排？”
- “练完不酸痛，是不是没效果？”
- “今天练腿举，给我五分钟热身。”
- “最近睡不好，训练表现下降，怎么调整？”

知识问答直接解释，不要求先填完整档案。制定个体计划时，会补问影响决策的目标、年龄段、经验、时间、器械和安全信息；不知道的内容保持未知，不虚构重量、消耗或健康状况。

技能支持跨对话保留用户历史，但历史分为两层：用户明确同意后成功保存并召回的本地档案可以直接复用；其他会话摘要、示例和推测只能作为待确认线索。档案不可用时只补问影响当前方案的关键信息，不把用户当成完全没有历史。

## 五个领域

| 领域 | 主要任务 | 交付内容 |
| --- | --- | --- |
| [Train Well](Coach-I-Wanna-Workout-Well-Skills/Coach-I-Wanna-Train-Well-Skill/SKILL.md) | 训练计划、动作选择、负荷与容量、进阶、漏练与平台期 | 排期、动作表、工作组次、余力、休息、替代动作和调整条件 |
| [Eat Well](Coach-I-Wanna-Workout-Well-Skills/Coach-I-Wanna-Eat-Well-Skill/SKILL.md) | 增肌减脂与维持体重、营养目标、外食和补剂评估 | 估算依据或份量法、蛋白计量口径、餐次安排、替代选择和趋势复盘 |
| [Know Well](Coach-I-Wanna-Workout-Well-Skills/Coach-I-Wanna-Know-Well-Skill/SKILL.md) | 肌肥大与发力原理、误区、证据争议 | 直接结论、关键原因、证据限制和对当前做法的影响 |
| [Flex Well](Coach-I-Wanna-Workout-Well-Skills/Coach-I-Wanna-Flex-Well-Skill/SKILL.md) | 热身、动态拉伸、长期柔韧性与活动度 | 有时间预算的练习顺序、剂量、动作提示、替代和停止条件 |
| [Recover Well](Coach-I-Wanna-Workout-Well-Skills/Coach-I-Wanna-Recover-Well-Skill/SKILL.md) | 疼痛筛查、负荷修改、睡眠恢复和回归训练 | 今天停止或降低什么、可保留什么、观察指标与就医条件 |

总控负责接待、风险筛查、领域选择与整合，按当前需求读取对应指令和知识文件；不依赖五个独立后台代理，也不会每次自动生成五份完整方案。

## 服务与反馈

基本流程：明确需求 → 筛查适用条件 → 补关键问题 → 按需检索 → 给可执行安排 → 根据反馈维持、微调或转介。

第一次训练后，可以这样反馈：

```text
今天完成了计划，用了四十五分钟。
推胸二十公斤，两组分别十次、九次，最后一组大约还能做两次。
没有疼痛；次日有轻微酸痛，不影响日常活动。
下周有一天没时间，怎么调整？
```

每周复盘实际完成率、主要动作表现、训练时长与恢复。涉及体重目标时再补同条件测量的趋势和饮食执行情况；不因一次体重波动、没酸痛或漏练就大幅改计划，也不集中补回漏练容量。

模板与示例：

- [接待与反馈](Coach-I-Wanna-Workout-Well-Skills/references/intake-and-feedback.md)：最小问卷、当前档案、训练后反馈、每周复盘和交接摘要。
- [三天增肌案例](Coach-I-Wanna-Workout-Well-Skills/references/train-worked-example.md)：完整训练交付、组数核算与后续调整。
- [其余领域案例](Coach-I-Wanna-Workout-Well-Skills/references/domain-worked-examples.md)：饮食计算、原理解释、热身预算、恢复修改和综合服务检查。

案例均为虚构条件下的操作示例，不是所有人的默认方案。

## 知识库与证据

[导读与主题索引](knowledge-base/topic-index.md) 将典型问题映射到主题文件。当前知识库包含导读、三十九份主题指南及一份[关键处方原文核验报告](knowledge-base/prescription-source-check.md)，主题分属五个领域。

默认读取一至三份与当前问题直接相关的主题；安全筛查需要时补读。每次结合适用人群、决策规则、剂量、例外与证据限制，不把群体平均、机制推断或经验策略当成个体保证。

主题内引用以导读中的文献编号与名称为准，通过题名、作者、年份、DOI 或公开链接检索来源；不要求具体页码。证据缺口与尚未核实的结论继续明确标注，不编造出处。文献与版权说明另见 [REFERENCES.md](REFERENCES.md)。

2026-10-04 已完成第一轮关键处方核验，检查十五份本地来源的核心条目，并修正 WHO 腰痛推荐、康复等级、训练容量、蛋白剂量与 CKD 透析适用范围。ACSM 两份材料目前为中文译本加英文摘要核对，部分历史临床试验仍待直接核实；全部主题与引用尚未逐条完成原文审校，不能将知识库视为已完成全部证据核验。

2026-10-05 第四轮补齐：新增「运动解剖基础与训练应用」（Know Well）与「执教技术与动作教学」（Train Well）两份主题指南，补齐运动解剖与执教教学文献；书目见 [REFERENCES.md](REFERENCES.md) 表末两组，开放获取 PDF 存于 `references/coaching/`。

2026-10-05 第五轮全补充：按缺口分析补齐 11 个缺失主题——高优先 4（运动前健康筛查与风险分层、有氧与心肺训练处方、女性全生命周期训练、慢病运动处方）、中优先 3（恢复手段证据、活动度渐进改善、运动坚持与行为改变）、低优先 4（居家/自重/弹力带训练、高级抗阻技术、跑步与耐力专项训练、老年防跌倒与平衡训练）；文献编号 [125]–[150] 已入知识库总表，引用式添加、未下载新 PDF。

2026-10-05 第六轮补剂补齐：新增「补剂第二梯队与证据边界」（Eat Well），覆盖 BCAA、碳酸氢钠、硝酸盐/甜菜根、瓜氨酸/精氨酸、HMB、电解质/运动饮料、铁 7 类"场景证据"补剂；文献编号 [151]–[158] 已入总表，核心五补剂（肌酸/β-丙氨酸/咖啡因/维D/鱼油）沿用既有主题，不重复。

2026-10-05 第七轮训练服务闭环：按缺口分析补齐 7 项——核心动作技术与进退阶（Train Well）、训练适应生理机制（Know Well）、增肌期营养实操（Eat Well）、训练监控与调整工作流（Train Well）、初始评估与体测流程（Train Well）、团课/循环/HIIT 课程设计（Train Well）、青少年与素食者营养补遗（Eat Well）；文献编号 [159]–[168] 已入总表，引用式添加、未下载新 PDF。

## 本地长期档案

档案默认关闭，只有使用者明确同意保存后才启用。用于同一使用者跨对话复用必要目标、条件、当前计划和少量反馈，不保存完整聊天、照片或病历，也不管理多个会员。

| 操作 | 行为 |
| --- | --- |
| 查看 | 查看当前档案或指定类别 |
| 暂停 / 恢复 | 暂停自动召回与写入，保留已有数据；恢复仍需有效同意 |
| 撤销 | 撤销最近一批更新，最多保留二十批历史 |
| 删除某项 / 清空 | 删除记录并清除撤销历史，防止通过撤销复原 |
| 撤回同意 | 停止自动读写，可选择保留或删除已有数据 |

工具仅依赖 Python 标准库，数据存于本人本机用户目录，未加密。总记录最多一百条、事件最多二十条，按需召回压缩内容。数据不得存入公开仓库、公共目录或同步目录；当前版本没有自动提醒服务。

在项目根目录检查状态，此操作不会为尚未启用的档案创建数据文件：

```text
python -X utf8 Coach-I-Wanna-Workout-Well-Skills/scripts/memory_store.py status
```

同意流程、字段、完整命令与存储边界见 [本地长期档案](Coach-I-Wanna-Workout-Well-Skills/references/long-term-memory.md)。没有同意、工具不可用或保存失败时，继续使用当前对话，并提供可自行复用的交接摘要；只在实际写入成功后确认保存。

## 目录结构

```text
.
|-- Coach-I-Wanna-Workout-Well-Skills/
| |-- SKILL.md
| |-- Coach-I-Wanna-Train-Well-Skill/SKILL.md
| |-- Coach-I-Wanna-Eat-Well-Skill/SKILL.md
| |-- Coach-I-Wanna-Know-Well-Skill/SKILL.md
| |-- Coach-I-Wanna-Flex-Well-Skill/SKILL.md
| |-- Coach-I-Wanna-Recover-Well-Skill/SKILL.md
| |-- references/
| | |-- intake-and-feedback.md
| | |-- train-worked-example.md
| | |-- domain-worked-examples.md
| |   `-- long-term-memory.md
| |-- scripts/memory_store.py
| |-- tests/test_memory_store.py
|   `-- knowledge-base/
|       |-- topic-index.md
|       |-- Train-Well/
|       |-- Eat-Well/
|       |-- Know-Well/
|       |-- Flex-Well/
|       `-- Recover-Well/
|-- knowledge-base/
|   `-- （仓库根目录副本，供项目文档与编辑使用）
|-- README.md
|-- REFERENCES.md
`-- LICENSE
```

## 验证

在项目根目录运行档案工具测试：

```text
python -X utf8 -m unittest discover -s Coach-I-Wanna-Workout-Well-Skills/tests -v
```

测试使用临时目录与虚构数据，不启用个人档案，覆盖同意状态、持久化与重复更新、暂停、撤销、删除、来源约束、容量上限、压缩召回和 UTF-8 输入。

截至 2026-10-04，已完成六个 skill 的格式校验、十三项工具测试、二百二十四个本地链接检查，以及四个独立虚构场景试用。格式与工具检查不代表真实咨询效果或医疗安全已被验证；案例文件列出持续试用时应观察的行为。

## 安全边界

本项目提供一般健身指导，不替代医生、营养师或物理治疗师的诊断与治疗，不处方或调整药物。儿童、孕产期、相关疾病与损伤人群需按对应知识的适用边界处理。

训练中出现胸痛、晕厥、异常气促、进行性麻木无力等危险信号时，优先停止训练并及时医疗处理；症状恶化不等待周复盘。不承诺固定期限的增肌、减脂、治愈或返场结果。

## License

本项目采用 MIT License，详见 [LICENSE](LICENSE)。

## 文献与致谢

文献来源、引用信息、开放获取文件、版权说明和安全提示见 [REFERENCES.md](REFERENCES.md)。
