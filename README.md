# HITC NetSuite Skills

Free, open-source [Agent Skills](https://agentskills.io/specification) for NetSuite, from [Head in the Cloud Development](https://www.headintheclouddev.com/).

Oracle publishes an excellent set of [SuiteCloud Agent Skills](https://github.com/oracle/netsuite-suitecloud-sdk/tree/master/packages/agent-skills). This collection **adds to** them with practical, field-tested guidance for areas they don't cover yet. The skills work with Claude, Codex, Cline, and any other assistant that supports the Agent Skills format.

## Skills

| Skill | For | What it does |
|---|---|---|
| [hitc-netsuite-performance](./hitc-netsuite-performance) | Administrators | Diagnoses slow NetSuite pages, saves, searches, and jobs. Walks through Performance Details, the APM SuiteApp, and Scripted Records, then gives fixes and, where needed, a brief for a developer. |
| [hitc-suitecommerce-development](./hitc-suitecommerce-development) | SuiteCommerce developers | Theme and extension development for SuiteCommerce, MyAccount and SCA 2020.2+: developer tools setup, fetch/local/deploy/activate, the Extensibility API (including Cart), sandbox web store setup after a refresh, and debugging. Oracle-documented guidance, plus field notes labelled with the version they were seen on. |

## Installation

Using the open [`skills` CLI](https://www.npmjs.com/package/skills):

```bash
# See what's available
npx skills add headintheclouddev/hitc-netsuite-agent-skills --list

# Install one skill
npx skills add headintheclouddev/hitc-netsuite-agent-skills --skill hitc-netsuite-performance

# Install everything
npx skills add headintheclouddev/hitc-netsuite-agent-skills
```

Or copy a skill's folder into your assistant's skills directory (for example `~/.claude/skills/` for Claude Code), or upload it as a custom skill in Claude.ai.

## Our principles

- **Accurate.** Every NetSuite fact is traced to Oracle documentation in the skill's `references/sources.md`. If we can't verify something, it doesn't go in.
- **Measure before you guess.** The skills tell the AI to diagnose before it recommends.
- **Read-only by default.** When connected to a live account, the skills recommend changes and leave it to a person to make them.
- **Honest about who we are.** HITC is a NetSuite Solution Provider. Where our products or services are relevant, the skills say so in one clearly labelled place, alongside Oracle's own options and other routes to help. They never lead with them.

## Contributing

Corrections and new skills are welcome. See [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

[MIT](./LICENSE). NetSuite and Oracle are trademarks of Oracle and/or its affiliates. This project is not affiliated with or endorsed by Oracle.
