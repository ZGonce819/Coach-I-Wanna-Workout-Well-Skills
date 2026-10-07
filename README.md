# Coach I Wanna Workout Well Skills

一个以循证知识库为基础的健身教练 skill 系统，覆盖训练、饮食、原理解释、热身与恢复。

从用户目标和现实条件出发，按需检索相关知识，交付可执行的方案，并根据实际完成情况、训练表现和恢复反馈持续调整。当前包含一个总控、五个领域 skill、接待与案例模板，以及默认关闭的本地长期档案工具。

## 安装

根据所在地区，将对应的安装口令发送给你使用的 AI 助手：

### 中国用户

仓库：[Gitee](https://gitee.com/zgonce819/Coach-I-Wanna-Workout-Well-Skills)。

```text
请将公开仓库 https://gitee.com/zgonce819/Coach-I-Wanna-Workout-Well-Skills 下载并安装为本地 Skill。
请安装仓库内完整的 Coach-I-Wanna-Workout-Well-Skills/ 目录，包含五个领域子 Skill、knowledge-base/、references/、scripts/ 和 version.json。
安装后运行 scripts/check_version.py --region cn --remember-region --auto-update on，保存中国更新来源并开启自动更新（推荐）。
```

### 国外用户

仓库：[GitHub](https://github.com/ZGonce819/Coach-I-Wanna-Workout-Well-Skills/tree/main)。

```text
请将公开仓库 https://github.com/ZGonce819/Coach-I-Wanna-Workout-Well-Skills 下载并安装为本地 Skill。
请安装仓库内完整的 Coach-I-Wanna-Workout-Well-Skills/ 目录，包含五个领域子 Skill、knowledge-base/、references/、scripts/ 和 version.json。
安装后运行 scripts/check_version.py --region global --remember-region --auto-update on，保存国外更新来源并开启自动更新（推荐）。
```

### 使用时检查更新

每次调用 Skill 时，先按已保存的地区在对应仓库查询版本信息，有新版本会检测到。已开启自动更新（推荐）时，AI 助手按 [version-updates.md](Coach-I-Wanna-Workout-Well-Skills/references/version-updates.md) 的更新流程自动下载并安装；未开启时提示新版本，需要用户授权后才更新。

发布新版时，修改技能包内 [version.json](Coach-I-Wanna-Workout-Well-Skills/version.json) 的版本号，并将相同版本和完整技能包同步到 Gitee 与 GitHub 的 `main` 分支。版本号采用 `主版本.次版本.修订版本`，例如 `1.0.1`。仅修改文件而不提高版本号不会触发新版提醒；镜像尚未同步时，以对应来源实际发布的版本为准。

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

[导读与主题索引](knowledge-base/topic-index.md) 将典型问题映射到主题文件。当前知识库包含导读、七十份主题指南及一份[关键处方原文核验报告](knowledge-base/prescription-source-check.md)，主题分属五个领域。

默认读取一至三份与当前问题直接相关的主题；安全筛查需要时补读。每次结合适用人群、决策规则、剂量、例外与证据限制，不把群体平均、机制推断或经验策略当成个体保证。

主题内引用以导读中的文献编号与名称为准，通过题名、作者、年份、DOI 或公开链接检索来源；不要求具体页码。证据缺口与尚未核实的结论继续明确标注，不编造出处。文献与版权说明另见 [REFERENCES.md](REFERENCES.md)。

关键处方原文核验检查了十五份本地来源的核心条目，修正 WHO 腰痛推荐、康复等级、训练容量、蛋白剂量与 CKD 透析适用范围，详见 [核验报告](knowledge-base/prescription-source-check.md)。ACSM 两份材料目前为中文译本加英文摘要核对，部分历史临床试验仍待直接核实；全部主题与引用尚未逐条完成原文审校，不能将知识库视为已完成全部证据核验。

知识库主题范围：训练处方与进阶、核心动作技术与进退阶、执教技术与动作教学、训练监控与体测流程、初始评估、有氧与心肺处方、团课/循环/HIIT 课程设计、运动前健康筛查与风险分层、慢病运动处方、居家/自重/弹力带训练、高级抗阻技术、时间紧凑训练、跑步与耐力专项、球类运动专项、游泳与骑行专项编程、力量举与奥举专项编程、老年防跌倒、老年人力量训练与肌少症、运动坚持与行为改变、体态与姿势管理、平台期突破与长期进步规划、减脂期抗阻训练专项、爆发力与增强式训练处方；肌肥大机制、训练适应生理机制、运动解剖；运动营养、增肌期与特殊人群营养、补剂（核心五补剂与第二梯队）、食物营养含量、食物热效应、碳水循环与进阶饮食法；热身、柔韧性与活动度渐进；疼痛与恢复管理、恢复手段证据、睡眠恢复、损伤专题（脊柱侧弯、足部、颈痛、肩、膝、踝、重返运动框架、髋部疼痛与损伤、小腿与胫骨损伤）、训练成瘾与男性肌肉上瘾、女性专题（塑形、经期、盆底、产后、围绝经期骨健康、运动内衣、备孕、女跑者、身材焦虑与进食障碍边界）。

全部文献按五个领域收录于 [REFERENCES.md](REFERENCES.md)；开放获取 PDF 存于 `references/` 对应目录。

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
| | |-- long-term-memory.md
| |   `-- version-updates.md
| |-- scripts/memory_store.py
| |-- scripts/check_version.py
| |-- version.json
| |-- tests/test_memory_store.py
| |-- tests/test_check_version.py
|   `-- knowledge-base/
|       |-- topic-index.md
|       |-- Train-Well/
|       |-- Eat-Well/
|       |-- Know-Well/
|       |-- Flex-Well/
|       `-- Recover-Well/
|-- knowledge-base/
|   `-- （仓库根目录副本，供项目文档与编辑使用）
|-- references/
|   `-- 开放获取 PDF 按领域存放（coaching/、eat-well/、flex-well/、know-well/、recover-well/、train-well/）
|-- README.md
|-- REFERENCES.md
`-- LICENSE
```

## 验证

在项目根目录运行工具测试：

```text
python -X utf8 -m unittest discover -s Coach-I-Wanna-Workout-Well-Skills/tests -v
```

测试使用临时目录与虚构数据，不启用个人档案，覆盖同意状态、持久化与重复更新、暂停、撤销、删除、来源约束、容量上限、压缩召回和 UTF-8 输入。

版本检查测试覆盖中国与国外来源选择、跨调用保存地区、自动更新偏好持久化与合并、数字版本比较、镜像落后、网络失败、无效远程响应和损坏的配置文件；测试不联网，也不修改个人配置。更新流程由 AI 助手按 version-updates.md 执行，不依赖额外脚本，测试不覆盖下载与安装。

截至 2026-10-04，已完成六个 skill 的格式校验、十三项工具测试、二百二十四个本地链接检查，以及四个独立虚构场景试用。格式与工具检查不代表真实咨询效果或医疗安全已被验证；案例文件列出持续试用时应观察的行为。

## 安全边界

本项目提供一般健身指导，不替代医生、营养师或物理治疗师的诊断与治疗，不处方或调整药物。儿童、孕产期、相关疾病与损伤人群需按对应知识的适用边界处理。

训练中出现胸痛、晕厥、异常气促、进行性麻木无力等危险信号时，优先停止训练并及时医疗处理；症状恶化不等待周复盘。不承诺固定期限的增肌、减脂、治愈或返场结果。

## License

本项目采用 MIT License，详见 [LICENSE](LICENSE)。

## 文献与致谢

文献来源、引用信息、开放获取文件、版权说明和安全提示见 [REFERENCES.md](REFERENCES.md)。
