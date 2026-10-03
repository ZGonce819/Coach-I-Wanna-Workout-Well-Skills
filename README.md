# Coach I Wanna Workout Well Skills

一个以知识库为基础的健身教练 skill 系统。

项目负责识别用户目标与意图，检索相关领域知识，并将知识组合成可执行、可调整的训练、饮食、活动度和恢复建议。

## 目录结构

```text
Coach-I-Wanna-Workout-Well-Skills/
├── Coach-I-Wanna-Train-Well-Skill/
│   └── SKILL.md
├── Coach-I-Wanna-Eat-Well-Skill/
│   └── SKILL.md
├── Coach-I-Wanna-Know-Well-Skill/
│   └── SKILL.md
├── Coach-I-Wanna-Flex-Well-Skill/
│   └── SKILL.md
└── Coach-I-Wanna-Recover-Well-Skill/
    └── SKILL.md
```

## 能力边界

- **Train Well**：训练目标、动作选择、训练计划、训练容量、频率、周期化与渐进超负荷。
- **Eat Well**：增肌、减脂、维持体重、热量、宏量营养素与饮食偏好。
- **Know Well**：肌肥大原理、发力机制、运动生理与训练知识解释。
- **Flex Well**：热身、动态拉伸、柔韧性与关节活动度。
- **Recover Well**：疼痛筛查、训练修改、基础康复、恢复安排与返场训练。

顶层总控负责用户画像、意图识别、风险筛查、知识检索、子 skill 路由、结果整合和计划迭代。

## 知识库原则

每个 skill 后续应逐步补充以下内容：

1. 基础知识与适用条件
2. 决策规则与计算方法
3. 可执行的输出模板
4. 异常情况、风险边界和转交条件

`Recover Well` 提供运动相关疼痛的初步筛查与训练调整建议，不替代医生或物理治疗师的诊断和治疗。

## License

本项目采用 MIT License，详见 [LICENSE](LICENSE)。

## 文献与致谢

文献来源、引用信息、开放获取文件、版权说明和安全提示见 [REFERENCES.md](REFERENCES.md)。
