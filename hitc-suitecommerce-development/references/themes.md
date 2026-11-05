# Themes

The base URL for Oracle links is `https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/`.

## The model

- A **theme** controls templates, Sass, and assets for a domain. Each domain has **one active theme** and any number of extensions.
- **Published themes** (from Oracle or a vendor) can't be overwritten. When you change one, the tools make you save it as a new **custom theme** ([section_1503696962](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_1503696962.html), [article_5110052337](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/article_5110052337.html)).
- On SuiteCommerce you can't edit the core application, so templates and Sass are changed through the theme, and behaviour through extensions.

## Overriding extension templates and Sass

**Documented** ([section_1498666438](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_1498666438.html)):
1. Find the file under `Workspace/Extras` (the tools put extension sources there).
2. Copy it into the theme's `Overrides` folder, keeping the file name. Follow Oracle's example for the path: the `Extras/Extensions/<ExtensionName>/` prefix is dropped (e.g. `Extras/Extensions/MyExt/Modules/...` becomes `Overrides/Modules/...`). Copying the full path as-is won't work.
3. Edit it, then restart `theme:local` so the new file is picked up ([section_1497015355](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_1497015355.html)).

Overrides belong to the **theme** and change how the extension looks on that domain without changing the extension. You can't override asset files.

**Consequences:**
- A theme that overrides cart or checkout templates decides how an extension's output looks there. **Always test extensions with the production theme active.**
- *Field note:* mature custom themes often override a lot, sometimes every Cart template and dozens of checkout templates. Count the overrides (`Overrides/` and the `override` entries in the manifest) before estimating any change in that area.

## Fallback themes

**Documented** (2023.2+ with the latest Base Theme, [article_3162629949](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/article_3162629949.html), [developer portal](https://developers.suitecommerce.com/fallback-themes-architecture.html)):
- Create one with `gulp theme:create`. The manifest marks it as a fallback subtype. Oracle's pages spell the key both `subtype` and `sub_type`, so copy the one the tools generate.
- It **inherits from the Base Theme**, so re-activating picks up Oracle's Base Theme updates. That means much less upgrade work than a full copy.
- It includes only the files you changed. It **can't add new templates or Sass** (put those in an extension), and the assets folder is all-or-nothing.
- Use it for new themes on current SuiteCommerce unless the design needs more than it allows.

## Sass

**Documented, summarised from** [Oracle's Sass best practices](https://developers.suitecommerce.com/best-practices-for-writing-sass.html) (2020):
- Write mobile-first.
- Name classes for what they do.
- Keep nesting shallow.
- Use variables.
- `@extend` can't reach into media queries.

**Variables exposed to Site Management Tools** (`/*editable(...)*/`): avoid user functions, `@if`, and mixins in them ([section_1500579362](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_1500579362.html)). Changes to skins and SMT variables need a deploy and an activation to show ([section_1497015355](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_1497015355.html)).

## Workflow for a template change

1. Find the text or element. Search the repository, and use the browser's element inspector to find class names to search for.
2. Check whether the file is the theme's own template, an override of an extension template, or core (on SuiteCommerce, core templates are changed by overriding them in the theme).
3. If the change is only wording in a translated string, consider a **translation override** in Configuration instead (see `extensibility-api.md`).
4. `theme:local`, test with `shopping-local.ssp` (or `my_account-local.ssp` / `checkout-local.ssp`), then `theme:deploy`, then activate.
5. Commit with a message that names the template and the reason.
