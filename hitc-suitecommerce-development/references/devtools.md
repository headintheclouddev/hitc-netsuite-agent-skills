# Theme & Extension Developer Tools

Contents: Getting the tools · Node and npm · First-time setup · Authentication · Commands · Local testing · Deploy and activate · Install and runtime errors

The base URL for Oracle links is `https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/`. Pages are linked by file name.

## Getting the tools

- **Documented:** download both kits from the File Cabinet at `SuiteBundles/Bundle 521562/`. They are `ThemeDevelopmentTools-<version>.zip` and `ExtensionDevelopmentTools-<version>.zip`; use the latest minor version for your release. Sites on SCA Aconcagua or 2018.2 must use the `18.2.1` tools ([section_1518824336](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_1518824336.html), [section_1509997459](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_1509997459.html)).
- **Documented:** the **SuiteCommerce Extension Management** SuiteApp (bundle 582380 as of 2026.1) is required before you install any theme or extension bundles. It provides **Commerce > Extensions > Extension Manager** ([section_N2675216](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_N2675216.html), [section_1510954484](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_1510954484.html)). Bundle IDs change between releases, so check the current page.
- *Field note (2026.1):* if the zips aren't in that folder in a given account, look in the Extension Management bundle's own File Cabinet folder.
- Extract each zip into its own folder (many teams use `Theme/` and `Extensions/` in one repository). **Don't move or rename anything inside it.** Oracle also recommends **separate root folders for production and sandbox**.

## Node and npm

- **Documented:** Node versions by product, from [section_4183926623](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_4183926623.html):

  | Implementation | Node.js |
  |---|---|
  | SuiteCommerce, SC MyAccount, SCA 2026.a and 2025.2 | 20.10.0 |
  | SCA 2022.2.1 | 14.19.0 |
  | SCA 2021.1 – 2022.2 | 12.21.x |
  | SCA 2020.2 | 12.16.x |

- *Field note (tools 26.1.30):* the tools' `package.json` pinned **Node ^20.20.2 and npm ^10.8.2**, with `engine-strict` on. That is stricter than the table, so `npm install` fails outright on Node 22. Read the `engines` field in the tools you actually downloaded.
- Use `nvm` to keep several Node versions installed (`nvm install <v>`, `nvm use <v>`) without changing the machine default. Developers who support several sites will need several versions.
- **Documented:** install Gulp globally, version 3.9.1 or higher ([section_4183927828](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_4183927828.html)). *Field note (26.1):* this differs from Oracle's install step. The 26.1 tools shipped a local Gulp 5, and running them needed a global `gulp-cli` 3.x rather than a global `gulp` 3.9.1.
- *Field notes (older tools, Node 12 and 14):*
  - `npm install` often ended with Python or `node-gyp` errors but left a working install. Run `gulp` to check before troubleshooting further. Developers on macOS got past the Python 2 requirement by aliasing `python` and `python2` to `python3`.
  - After switching Node versions, `npm rebuild node-sass` was sometimes needed.
  - On Apple Silicon, some old tool versions only installed under an older Node line, or on an Intel machine.

## First-time setup

1. `cd` into the tools folder and run `npm install`.
2. Run `gulp` on its own. It lists the available tasks, which confirms the install worked.
3. *Field note (seen on every version from 2021 to 26.1):* `gulp/config/config.json` is in `.gitignore`, so it's missing after a fresh clone. Every gulp task then fails immediately, for example with `Cannot read properties of undefined (reading 'application_manifest')`. Copy `gulp/config/config-default.json` to `config.json` in **both** the theme and the extension tools.
4. Put the integration's consumer key and secret in the `.env` file in the tools folder (see Authentication). Keep it out of git.
5. Recommended `.gitignore` entries: `node_modules/`, `.env`, `.nsdeploy`, `gulp/config/config.json`, `LocalDistribution/`, `DeployDistribution/`. *Field note:* the folders the tools generate can hold more than a thousand files. If git suddenly wants to commit them all, it's missing `.gitignore` entries.
6. **Don't edit generated or tool files** ([theme](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_1497018780.html), [extension](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_1510174355.html)). Leave `DeployDistribution/`, `LocalDistribution/`, `gulp/`, `node_modules/`, `gulpfile.js`, `package.json`, and the files under `Workspace/Extras` alone. Oracle says not to manually edit the individual files in the tools' top-level folder. Your work belongs in `Workspace/`.

## Authentication

**Documented:** the tools use token-based authentication ([section_160997054391](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_160997054391.html), [section_161004948870](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_161004948870.html)). The integration settings below are from the setup page ([section_1509997459](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_1509997459.html)).

1. Create an **integration record** with these settings:
   - Token-Based Authentication: checked
   - TBA: Authorization Flow: checked
   - Callback URL: `http://localhost:7777/tba`
   - User Credentials: checked
   - Authorization Code Grant: cleared
2. Copy its consumer key and secret into `.env` in the tools' root folder.
3. On the first fetch or deploy, enter an **authentication ID** (a label such as `client-sb1`). A browser window opens: choose the account and role, then click **Allow**.
4. The token is saved in `.nstba` in your home folder. Run any command with `--to` to choose a different saved token or create a new one, e.g. `gulp extension:fetch --to`.
5. Deploy also writes `.nsdeploy` (the target account and website). `gulp theme:deploy --to` rewrites it, and `gulp clear` deletes it. For accounts with account-specific domains (2021.2.1+), add `--account 123456`, or `--account 123456-sb1` for a sandbox.

The Administrator and SCDeployer roles have the required permissions by default.

*Field notes:*
- A saved token that has stopped working can fail **silently**. Create a fresh one with `--to` before debugging anything else.
- If `.nsdeploy` points at the wrong account or website, delete it and pick again.
- In some accounts, the tools' RESTlet deployments only allowed specific roles. If you get an auth error with the right role selected, check the roles on those RESTlet deployments.
- One integration per developer per account becomes hard to manage. Decide as a team how integrations and tokens are shared, and **never commit them**.

## Commands

**Documented** ([section_1510956587](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_1510956587.html)):

| Task | Theme tools | Extension tools |
|---|---|---|
| Download what's deployed | `gulp theme:fetch` | `gulp extension:fetch` |
| Run locally | `gulp theme:local` | `gulp extension:local` |
| Upload | `gulp theme:deploy` | `gulp extension:deploy` |
| Scaffold | `gulp theme:create` (fallback themes; see [article_3162629949](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/article_3162629949.html)) | `gulp extension:create`, `gulp extension:create-module` |
| Rebuild manifest | `gulp theme:update-manifest` | `gulp extension:update-manifest` |

Useful flags and tasks:
- `--to` creates or chooses a token.
- `--reactivate` activates straight after deploying.
- `--preserve-manifest`: `local` and `deploy` overwrite manual edits to `manifest.json` unless you pass it.
- `--source <type>` deploys only part of the code, e.g. `templates` or `sass`.
- `gulp validate`, `gulp clear`, and `gulp reactivate`.

**Fetch behaviour (documented):**
- `theme:fetch` clears the Workspace before it downloads.
- `extension:fetch` overwrites local extension files.
- Before extension work, the **active theme** has to be fetched. `gulp extension:fetch` does this from the extension tools and puts the theme files in the `Extras` folder ([section_1510944391](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_1510944391.html)).
- Published extensions (installed from a SuiteApp) aren't downloaded. Published themes can be.

## Local testing

- **Documented:** open the local version of a page through the site's own domain ([section_1510870075](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_1510870075.html)):
  - `http://<domain>/c.<account_id>/<SSP_APPLICATION>/shopping-local.ssp`, where SSP_APPLICATION is `scs` for SuiteCommerce or the SCA root for SCA (e.g. `sca-dev-2019-2-0`)
  - *Field note:* on many sites the shorter `/<SSP_APPLICATION>/shopping-local.ssp` on the shopping domain also works. The local assets are served from `localhost:7777`.
  - `my_account-local.ssp` and `checkout-local.ssp` work the same way.
  - Find the application path under **Commerce > Hosting > Domains** if you're unsure.
- **Mixed content (documented):** browsers may block `http://localhost:7777` assets on an HTTPS page. Allow insecure content for that site, or use another documented workaround ([bridgehead_4420063206](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/bridgehead_4420063206.html)).
  - Redirects (to log in, for example) land on the production page, not the local one. Edit the URL back to `-local.ssp` by hand.
- **What runs locally (documented):** SuiteScript services and configuration changes don't work locally until they've been deployed and activated, and manifest changes need the local server restarted ([section_1510870075](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_1510870075.html)).
  - Also restart `local` after adding new files or overrides ([section_1497015355](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_1497015355.html)).
  - Translations can't be tested locally ([section_159707109160](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_159707109160.html)).
- *Field note (26.1):* the extension tools only start an HTTPS local server for SCIS. For web stores, expect HTTP plus the mixed-content setting.

## Deploy and activate

1. `gulp extension:deploy` (or `theme:deploy`) asks which extension to deploy and its version.
2. **Activate (documented):** Commerce > Extensions > Extension Manager > **New Activation** (also called **Create Activation**) > choose the website and domain ([section_1549026512](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_1549026512.html)).
   - Each domain has one theme and any number of extensions.
   - Simultaneous activations are queued. Each shows a status of Complete, In Process, Pending, or Error. Error links to a log ([section_1548960962](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_1548960962.html)).
   - Activating requires the Administrator role unless the installer deployment has been opened to other roles ([section_1561500233](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_1561500233.html)).
3. Re-activating with no changes is the normal way to push a redeployed version of something that's already active.
4. Oracle's developer portal says an activation taking longer than about 15 minutes may mean a problem ([developer portal](https://developers.suitecommerce.com/develop-your-first-extension.html)).

## Install and runtime errors

| Symptom | Likely cause | Fix |
|---|---|---|
| `npm install` refuses to run (engine errors) | Wrong Node or npm version | `nvm use` the version in the tools' `engines` field |
| Every gulp task fails straight away | `gulp/config/config.json` is missing | Copy it from `config-default.json` |
| Auth fails, or the browser never opens | Stale token, wrong integration in `.env`, or role not allowed | Run with `--to` and check `.env` and the role |
| Deploy goes to the wrong account | Stale `.nsdeploy` | Delete it or use `--to` |
| Local work vanished | You ran fetch | Recover it from git, and commit before fetching next time |
| `ENOENT … DeployDistribution` or node-sass errors (old tools) | Node/native module mismatch | Switch to the correct Node, then `npm rebuild node-sass` |
| Extension won't run locally | Active theme hasn't been fetched for extension work | `gulp extension:fetch` (it also brings down the active theme) |
| Deploy fails with `startDeploy Errored: Cannot Read Property 'files' of Undefined` | A RESTlet request ran out of governance units (worse with deeply nested folders) | Lower `chunk_size` (default 80) in `gulp/config/config.json` ([Oracle](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_4404434060.html)) |
| Builds behave strangely or deploy stale files | Leftover build output | `gulp clear` removes `DeployDistribution`, `LocalDistribution`, and `.nsdeploy`. Use it instead of deleting folders by hand, then choose the deploy target again ([Oracle](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_1510956587.html)) |
