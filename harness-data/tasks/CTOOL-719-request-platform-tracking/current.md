# current — current state

> Read this first when resuming in a new session. Keep it to
> "current stage + single next step" only; never pile up history here.
> (State lives in files — the anti-pattern is result.md ballooning to thousands of lines.)

- Task name / ID: CTOOL-719-request-platform-tracking (Jira CTOOL-719, Task, Backlog)
- mode: standard # standard / minimal — minimal must come from an explicit user request (harness-dev §3)
- involved apps: conversations-frontend (single app)
- spec/plan: /Users/yangjun/Desktop/project/conversations-frontend/docs/changes/CTOOL-719-request-platform-tracking/ # project artifacts, committed with the feature branch
- current stage: self-test (GA3 both layouts + GA4 view_item both layouts delivered; UTM scope removed; acceptance pending in a separate session)
- single next step: follow-ups all user-side — GTM Data Layer Variable + GA4 custom dimension registration, Jira AC English note, inform WA/analytics that upgrade traffic now emits GA4 view_item; acceptance session (harness-testing)
- blockers (if any): none — validate ALL GREEN; PR #456 + Jira current; user's local nuxt.config.ts must not be committed
