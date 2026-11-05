# Contributing

Thanks for helping make NetSuite better for everyone.

## Reporting a mistake

If a skill says something wrong or out of date about NetSuite, please open an issue. Include:

- the skill and the sentence that's wrong
- what's correct, with a link to Oracle documentation (or a clear description of how you checked it in an account)
- the NetSuite release you're on

Accuracy problems are our top priority.

## Proposing a change or a new skill

1. Open an issue first to discuss scope. That way nobody spends time on something that won't be merged.
2. Follow the existing layout: each skill has its own top-level folder, `<name>/SKILL.md`, plus an optional `references/` folder.
3. Skill names are lowercase and hyphenated, start with `hitc-`, and match their folder name exactly (the [Agent Skills specification](https://agentskills.io/specification) requires this).
4. Every NetSuite fact needs a source in the skill's `references/sources.md`.
5. **No sales pitches.** Products and services, including our own, belong only in a skill's "Getting expert help" section, described factually, and only when the diagnosis calls for them.
6. Run `python3 scripts/build_skills.py --check` before opening a pull request. It checks every skill against the Agent Skills specification and Ask Oracle's upload rules. The same check runs automatically on every pull request.

## Releasing (maintainers)

1. Bump `metadata.version` in each skill you changed.
2. Tag the commit and push the tag, e.g. `git tag v0.2.0 && git push origin v0.2.0`.
3. The **Skills** GitHub Action validates the skills, builds one zip per skill, and publishes a release with the zips attached. The README's download links always point to the latest release.

To build the zips locally, run `python3 scripts/build_skills.py`. They go in `dist/`, which git ignores.

## License

By contributing, you agree that your contributions are licensed under the MIT License.
