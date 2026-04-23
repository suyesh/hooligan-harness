Article: https://www.anthropic.com/engineering/harness-design-long-running-apps

2 Problems solved by the PGE Architecture:

1. **Context Anxiety** is a real thing: models start wrapping things up if they think they're nearing the limits of their Context. Even if compacted (prev context summarized), still paranoid
2. **Self-evaluation overconfidence**
   1. Outcomes are not defined and verifyable
   2. Agents skew positive when grading their own work even when it is verifyable
