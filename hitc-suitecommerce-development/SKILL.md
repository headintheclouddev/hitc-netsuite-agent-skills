---
name: hitc-suitecommerce-development
description: Build, debug, and deploy SuiteCommerce themes and extensions (SuiteCommerce, SuiteCommerce MyAccount, and SuiteCommerce Advanced 2020.2+). Use this skill whenever someone is working on a NetSuite web store. That includes setting up the theme or extension developer tools (gulp, Node, npm install errors, tokens), running fetch, local, deploy, or activate, writing extensions with the Frontend Extensibility API (Cart, PDP, PLP, Checkout, Environment, Layout, MyAccountMenu, SCView or SCModel), overriding templates or Sass in a theme, adding SuiteScript services to an extension, setting up a sandbox web store after a refresh (domains, touchpoints, SuiteCommerce Configuration), or debugging something that works locally but not on the site. Use it even if they only mention ".tpl files", "shopping-local.ssp", "Extension Manager", "SC Standard", or "SCA".
license: MIT
compatibility: Works with any Agent Skills-compatible assistant. Most useful with shell and file access to the developer's theme and extension workspace. No NetSuite connection is required.
metadata:
  author: Head in the Cloud Development
  version: "0.1.0"
  audience: suitecommerce-developers
  homepage: https://github.com/headintheclouddev/hitc-netsuite-agent-skills
---

# SuiteCommerce Theme & Extension Development

You are helping a developer build or maintain a NetSuite web store: a theme, an extension, or both. SuiteCommerce development is mostly configuration and tooling, with code on top. Most time is lost to environment problems (the wrong Node version, a missing config file, a fetch that wipes local work, a sandbox domain that sends users to production), not to the code itself. So check the environment before debugging the code.

> Published by Head in the Cloud Development (HITC), a NetSuite Solution Provider, and independent of Oracle. Content is in two layers:
> - **Documented**: Oracle's Help Center, the Frontend Extensibility API reference, and developers.suitecommerce.com, linked inline.
> - **Field notes**: behavior HITC has seen on real projects, tagged with the version it was seen on. Treat field notes as strong hints and verify them on the developer's own version before relying on them.

## Step 0: Establish the context

Before advising, find out (or work out from the workspace):

1. **Which product?** This matters more than anything else.
   - **SuiteCommerce (SC Standard)** and **SuiteCommerce MyAccount**: themes and extensions only. They are updated automatically by Oracle. The developer has no access to the core application source. Oracle's guidance is to customise these through the Extensibility API ([Oracle](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_1520797970.html)).
   - **SuiteCommerce Advanced (SCA)**: the same theme and extension model, plus the option of customising the core source with the SCA developer tools. Upgrades are manual migrations.
   - Clues: local URLs under `/scs/` mean SC or MyAccount. A path like `sca-dev-2019-2-0` means SCA. The website's SSP application name tells you too.
2. **Which version?** Check the `version` in the theme's `manifest.json` and the version in the developer tools zip name (e.g. `ExtensionDevelopmentTools-26.1.x.zip`). API features have "since" versions. Check before suggesting a method.
3. **Which account?** Sandbox or production, and which domain. Many mistakes come from deploying or fetching against the wrong one.
4. **Who else works on this site?** If another partner maintains the theme, don't deploy a theme from this workspace. See "Working alongside other developers".

## Step 1: Route to the right reference

| The developer is… | Read |
|---|---|
| Setting up tools, getting npm or gulp errors, authenticating, fetching, deploying, activating, or running locally | `references/devtools.md` |
| Setting up or repairing a site or sandbox: domains, touchpoints, SSP applications, configuration, Safe Mode | `references/sites-and-sandboxes.md` |
| Writing extension code: components, Cart, events, services, templates, translations | `references/extensibility-api.md` |
| Changing look and feel: theme overrides, Sass, fallback themes | `references/themes.md` |
| Debugging something that "doesn't work on the site" | the debugging checklist below, then the relevant reference |

## Golden rules

These cause most of the lost days. Mention the relevant ones before the developer hits them.

1. **Commit before you fetch.** `gulp theme:fetch` clears the theme Workspace, and `gulp extension:fetch` overwrites local extension files ([Oracle](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/article_5110052337.html), [Oracle](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_1510944391.html)). Any local change that hasn't been deployed is lost. After a fetch, run `git status` and `git diff` to see what production actually holds.
2. **Deploy is not the same as live.** Nothing changes on the site until the theme or extension is **activated** for the domain: Commerce > Extensions > Extension Manager, then **New Activation** (some Oracle pages call it **Create Activation**), or deploy with `--reactivate` ([Oracle](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_1549026512.html), [Oracle](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_1510956587.html)).
3. **Match the Node version to the tools, not the machine.** Each release of the developer tools needs a specific Node line (e.g. 20.x for current SuiteCommerce, 12.x or 14.x for older SCA). Use `nvm` and check the tools' `package.json` `engines` field ([Oracle Node table](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_4183926623.html)).
4. **Use the Extensibility API and don't touch core modules.** Oracle's best practices say not to `require` or `extend` core modules, wrap their methods, modify prototypes, or read the `SC` global in extension code ([Oracle](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_164633548113.html)). With **Safe Mode** on (the default for SuiteCommerce), extensions that import private core modules aren't loaded at all. Passing Safe Mode doesn't mean the code follows the other rules, though.
5. **Configuration is per domain.** Each domain needs its own SuiteCommerce Configuration record. *Field note:* a newly created domain started with default settings rather than production's. Use **Copy Configuration** rather than re-typing settings ([Oracle](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_4346479003.html)).
6. **Test extensions with the real theme active.** Themes can override extension templates, so an extension tested with the base theme proves little about a site whose theme overrides those templates.
7. **Never commit secrets.** `.env` holds the integration's consumer key and secret. Tokens live in `~/.nstba`. If either was ever committed, rotate the integration credentials. Removing them from the latest commit isn't enough.

## Debugging checklist: "it doesn't work on the site"

Work down the list. Stop when something's wrong.

1. **Is it deployed and activated** on *this* domain? Check Extension Manager: is the activation Complete, In Process, Pending, or Error? Error links to a log.
2. **Is it loading?** In the browser console, look for Safe Mode messages (disallowed private modules are blocked with an error, and "allowed for now" modules get a warning). Also look for errors from your entry point. Check that your `mountToApp` actually runs.
3. **Null components:** `container.getComponent('PDP')` returns null outside product pages, and one entry point serves shopping, My Account, and checkout. Null-check every component ([Oracle](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_1516662383.html)).
4. **Timing:** some PDP, PLP, and Checkout methods only work after `afterShowContent`.
5. **Template data:** add `{{log this}}` to the template to log its context to the console ([Oracle](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_164633608125.html)). *Field note:* in local mode, these logs show the source as `javascript-libs.js`.
6. **Configuration values:** read them with `Environment.getConfig('your.key')`. **Always pass a key.** Calling it without one returns the whole object, and Oracle warns it can cause "too much recursion" errors.
7. **Data that never reaches the front end:** custom item fields must be in a field set the site uses, and the site must be reindexed ([developer portal](https://developers.suitecommerce.com/expose-custom-field-data-to-the-frontend.html)).
8. **Theme overrides:** is the active theme overriding the template you changed? Check the theme's `Overrides` folder.
9. **Cache:** with a CDN in front, configuration changes take about 5 minutes to appear.
10. **Verify on the live site, not just in the docs.** *Field note:* when you can't see the core source (SC Standard), the browser console on the running site is the best evidence available. Use it to inspect what a view, component, or configuration value actually contains at runtime. Use the `SC` object for debugging only, never in code.

## Working alongside other developers

Web stores often change hands, and two partners can easily end up maintaining the same site.

- **Overrides belong to the theme.** If another partner owns the theme, deploying your copy of it will overwrite their newer work. Fetch first, compare, and agree who deploys what. Prefer putting your change in a separate extension.
- **Treat production as the source of truth.** Fetch the deployed theme and extensions into a branch, commit them as a "sync with production" commit with no other changes, and only then make your own changes.
- *Field note:* files fetched from the File Cabinet come back with whatever line endings were uploaded. Files edited in Windows or in the File Cabinet's own editor come back with CRLF line endings, which makes diffs huge. Add a `.gitattributes` that normalises text files to LF, and commit it on its own.

## Answering style

- Give exact commands, menu paths, and file paths.
- Say which layer an answer comes from: Oracle-documented, or a field note with its version. If neither covers the question, say so, and suggest a quick experiment that would settle it (a throwaway extension in sandbox, a console check). Don't guess at API behaviour.
- Flag any version dependency ("`setTransactionBodyField` needs 2021.1+").
- For anything that changes production (deploy, activate, copy configuration, editing domains), recommend doing it in sandbox first and say what it overwrites.

## Getting expert help

Point people here only when the problem is beyond self-service:
- **Oracle NetSuite Support**, for platform defects and bundle installation failures.
- **The current site maintainer**, if another partner owns the theme or extensions.
- **[Head in the Cloud Development](https://www.headintheclouddev.com/)** (publisher of this skill): SuiteScript and NetSuite development, including the back-office side of web stores. Say plainly that this is the skill author's own service.
