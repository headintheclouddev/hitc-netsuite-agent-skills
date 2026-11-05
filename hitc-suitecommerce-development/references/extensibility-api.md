# Writing Extensions

Contents: Structure · Components · Cart · Environment · Rules for safe extensions · Item types in the web store · Backend services · Templates and translations · Custom field data

Links:
- **API** = `https://system.netsuite.com/help/helpcenter/en_US/APIs/SuiteCommerce/Extensibility/Frontend/` (the Frontend Extensibility API reference)
- **OHC** = `https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/`

The API reference marks when each method was added ("since"). Check it against the site's version before suggesting a method.

## Structure

- **Entry point (documented):** each active extension's entry point exports `mountToApp(container)`. The application calls it once per extension, in activation order ([API ExtensionEntryPoint](https://system.netsuite.com/help/helpcenter/en_US/APIs/SuiteCommerce/Extensibility/Frontend/ExtensionEntryPoint.html)).
- **Components:** get them with `container.getComponent('Cart')`. It **returns null** when the component isn't available, and one entry point runs in shopping, My Account, and checkout. So null-check every time ([OHC section_1516662383](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_1516662383.html)).
- **Modules:** all modules are AMD modules: `define('Vendor.Module.Purpose', [deps], function (...) {...})` ([OHC article_161858972640](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/article_161858972640.html)). SuiteScript 2 service files leave the module name out.
- **manifest.json:** gives the name, vendor, version (`dd.dd.dd`), target (`SCA,SCS`), entry points, templates, Sass, assets, configuration, SuiteScript, and page types ([OHC section_1511302363](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_1511302363.html)). The tools regenerate it on `local` and `deploy` unless you pass `--preserve-manifest`.

## Components

**Documented** ([OHC section_163215257564](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_163215257564.html), [API index](https://system.netsuite.com/help/helpcenter/en_US/APIs/SuiteCommerce/Extensibility/Frontend/index.html)):

| Component | Use it for |
|---|---|
| `Cart` | Lines, summary, promotions, shipping estimates, payment, submit |
| `Checkout` | Checkout steps, step groups, and modules |
| `PDP` / `PLP` | Product detail page (options, quantity, images); product list page (filters, sort, pagination). Each is null on other pages |
| `Environment` | Configuration, site settings, session, translations, trackers |
| `Layout` | Header, footer, home, and other views without their own component (`addChildView`, `registerView`) |
| `MyAccountMenu`, `UserProfile`, `LoginRegisterPage` | My Account menu, the current customer, and login/register events (2019.1+) |
| `PageType`, `CMS` | Page types and layouts for Site Management Tools, and custom content types |
| `SCView`, `SCFormView`, `SCCollectionView`, `SCModel`, `SCCollection` | Base classes you `require` for your own views and models (2020.1 / 2020.2+) |

The Backend Extensibility API is deprecated since 2020.1. Use the frontend API or SuiteScript 2.x services instead.

## Cart

**Methods (documented, [API Cart](https://system.netsuite.com/help/helpcenter/en_US/APIs/SuiteCommerce/Extensibility/Frontend/Cart.html)).** All return a jQuery Deferred. The line methods take **a wrapper object**, not bare values:
- `addLine({ line: { item: { internalid }, quantity } })`. This adds to the quantity if the item is already in the cart.
- `addLines({ lines: [{ item: { internalid }, quantity }] })`
- `updateLine({ line: { internalid, quantity } })`. Setting quantity to 0 removes the line.
- `removeLine({ line_id })`. Line IDs are regenerated when an item is re-added.
- `getLines()`, `getSummary()`, `getPromotions()`, `getShipMethods()` (checkout pages only)
- 2021.1+: `getLatestAddition()`, `setTransactionBodyField({ fieldId, type, value })`, `getPurchaseOrderNumber()`, and `setPurchaseOrderNumber(po[, save_order])`. Note that `setPurchaseOrderNumber` takes **positional** arguments, works only on the checkout page, and needs "Display Purchase Order Field on Payment Info Page" enabled.

*Field note (26.1):* passing a bare line or a bare ID is rejected. The validation error names the property it expected, so read it.

**Events (documented):**
- before/after pairs for AddLine, UpdateLine, RemoveLine, AddPromotion, RemovePromotion, EstimateShipping, SetShipMethod, AddPayment, SetPurchaseOrderNumber, SetTransactionBodyField, and Submit
- `beforeShowContent` and `afterShowContent`

`before*` events can be **cancelled**: register the handler with `cancelableOn` and throw an error, or return a rejected Deferred ([API CancelableEvents](https://system.netsuite.com/help/helpcenter/en_US/APIs/SuiteCommerce/Extensibility/Frontend/CancelableEvents.html)). Oracle's events overview says cancelling also stops the matching `after*` event ([OHC section_1521059818](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_1521059818.html)). Check that a specific event is cancelable in your version before relying on it. Use this to refuse a change (for example, stopping a customer removing a required line) rather than just hiding the button.

*Field note (26.1):* other event names, such as `afterCartUpdate`, `afterAddLines`, and `afterSetLines`, also registered without error. They aren't in the reference, so don't build on them. React to the documented after* events instead.

## Environment

**Documented** ([API Environment](https://system.netsuite.com/help/helpcenter/en_US/APIs/SuiteCommerce/Extensibility/Frontend/Environment.html)):
- `getConfig('dot.path.key')` returns a copy of that configuration value. **Always pass a key.** With no key it returns everything, and Oracle warns this can cause "too much recursion" errors. *Field note:* we've seen a configuration value come back as a whole context object because it was being read from the container rather than the Environment component.
- `getSiteSetting(key)` and `getSession()` (currency, language, price level). `isPageGenerator()` is true while the SEO page generator is rendering.
- `setTranslation(locale, [{ key, value }])`. Prefix your keys so you don't overwrite core strings.
- Read configuration through Environment, **not** `SC.Configuration` or the `SC` global ([OHC section_164633548113](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_164633548113.html)).

## Rules for safe extensions

**Documented**, from Oracle's General Best Practices ([OHC section_164633548113](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_164633548113.html)). In extensions:
- don't `require` or `define` core modules
- don't `extend()` them or `_.wrap()` their methods
- don't modify prototypes
- don't use the `SC` global
- don't extend other extensions

Use `addChildView`, `addToViewContextDefinition`, and the components instead. Oracle says these rules apply to SCA too "if you want to minimize the issues". Safe Mode only enforces the first rule: it blocks imports of private core modules. Code that passes Safe Mode can still break the others.

**What to do when the API can't do it:**
1. Check the reference again, including the version "since" tags and the component's events.
2. Ask whether a different design fits inside the API: a child view, a context variable, a cancelable event, or a server-side SuiteScript backstop.
3. On SCA, the SCA developer tools can customise core source, which is Oracle's documented route for cases the API can't cover. On SuiteCommerce there's no such route, so say so plainly instead of reaching for private modules.
4. *Field note:* the API is less complete than its documentation suggests, and some behaviour isn't documented. Before building on it, prove it with a throwaway extension in sandbox, with the real theme active.

*Field note (26.1):* view helpers such as `showError` and `showConfirmationMessage` exist on views at runtime, but the API only documents `showError` for checkout `WizardModule`. For general messages, use the documented `showMessage()` (2019.2+).

## Item types in the web store

- **Documented:** Discount, Subtotal, Markup, Payment, and **Other Charge** items are "supported, but not visible in Commerce web stores". Other unsupported item types need customisation ([OHC preface_1518477920](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/preface_1518477920.html)).
- *Field note (26.1):* an Other Charge item with **Display in Web Site** ticked could be added with `Cart.addLine()`, and it changed the cart summary. But it never appeared in `getLines()`, and `removeLine()` failed with "line not found". So an extension can add such a line but can't manage it afterwards. Other observations:
  - Other Charge items have no Store Display Name or URL Component, so the cart label comes from the Sales Description.
  - Add-to-cart tracking threw an error about generating a URL, but the add still completed.
  - Without Display in Web Site ticked, `addLine` failed with an "invalid item reference key … for subsidiary" error, which is misleading because the subsidiary was fine.
- If an extension has to add **and later remove or change** a line, test a regular catalog item type first. Prove the full add/update/remove cycle in sandbox before committing to a design. Keep such items out of commerce categories and site search on purpose.
- For charges that must always be right (fees, surcharges), enforce them **server-side** on the sales order as well. Treat the cart as presentation, and the server as the source of truth.

## Backend services

- **Documented:** extensions can include SuiteScript 1.0 services (`*.ServiceController.js` under `SuiteScript/`) and SuiteScript 2.0 services (`*.Service.ss` under `SuiteScript2/`) ([OHC article_161858972640](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/article_161858972640.html)). Oracle's developer portal says SuiteScript 2.1 is "not **currently** supported" in SuiteCommerce SuiteScript; use 2.x, 2.0, or 1.0 ([Getting Started](https://developers.suitecommerce.com/getting-started.html)).
- **Permissions (documented):** to let a service do more than the shopper's role allows, open the `.ss` file's record in the File Cabinet and go to the **Permissions** subtab. Tick **Enable**, choose an **Execute as Role** (it can't be Administrator), and tick **Run Script Without Login** only if anonymous visitors need it ([OHC section_1529598291](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_1529598291.html)). Use a narrowly scoped custom role ([developer portal](https://developers.suitecommerce.com/elevating-permissions-on-service-files.html)).
- *Field note:* after deploying a new version of an extension, check that the service files kept their permission settings, and re-apply them if not.
- **Security (HITC guidance):** services are reachable by anyone who can load the site. Log full exception details server-side and return generic messages. Raw NetSuite errors can expose field IDs, record types, and internal IDs. Return a proper error status (e.g. 400) rather than `{type: 'error'}` in a 200 response, or Backbone will treat the failure as success.

## Templates and translations

- Templates are Handlebars (`.tpl`).
  - **`{{log this}}`** logs the template's context to the console ([OHC section_164633608125](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_164633608125.html)).
  - Use `{{!-- comments --}}`, which aren't rendered, rather than HTML comments, which are.
  - Oracle documents adding custom helpers with `Handlebars.registerHelper`. Its example `define`s the core `Handlebars` module, which is an exception to the "don't require core modules" rule. Check the current page for the recommended pattern.
- **Translatable text:** use `{{translate 'Text with $(0)' value}}` in templates and `_('…').translate()` in JavaScript ([OHC section_1516657590](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_1516657590.html)).
  - Merchants can override translated strings under Configuration > **Multi-Domain > Translations** ([OHC bridgehead_4688691652](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/bridgehead_4688691652.html)). The configuration record takes precedence over extension and theme translation files ([OHC section_159707109160](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_159707109160.html)).
  - *Field note:* this also works English to English, so a wording change to a translated string can be made in configuration without a code deploy.

## Custom field data

**Documented** ([developer portal](https://developers.suitecommerce.com/expose-custom-field-data-to-the-frontend.html)):
- **Item fields:** add the field to a **field set** the site uses (e.g. `details`) and reindex. Check it with the Item Search API (`/api/items?...&fields=...`), then use it in templates (e.g. `{{model.item.custitem_x}}`).
- **Customer fields:** they need Store Value and must apply to Web Site. They come through `UserProfile`.
- **Transaction body fields:** use `Cart.setTransactionBodyField` (2021.1+), or Oracle's Custom Fields extension.
