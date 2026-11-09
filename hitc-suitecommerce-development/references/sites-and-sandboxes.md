# Sites, Domains & Sandboxes

The base URL for Oracle links is `https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/`.

## How the pieces fit

**Website record** → **domain(s)** → **SSP application** linked to the domain → **theme and extensions activated** per domain → **SuiteCommerce Configuration** record per domain.

If any link in that chain is missing, the site can look broken in ways that seem unrelated to the real cause.

## Domains

**Documented:** domain types ([section_N2484898](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_N2484898.html)):
- **Single Domain for Web Store and Checkout**: shopping and checkout share one HTTPS domain. It is required for SuiteCommerce MyAccount.
- **Web Store Only**, combined with a separate checkout domain (preset or **Checkout Only**).
- Others: Hosted Web Page, Redirect URL, Promotional URL, Email Campaign Domain.

**Rule of thumb:** a sandbox domain should **use the same domain type as production**. Check production's domain type and the live touchpoints first. If shopping and checkout share one host in production, a Web Store Only domain in sandbox can leave checkout unusable, which is often exactly where you need to test.

**Linking the application (documented):**
1. Go to **Commerce > Hosting > SSP Applications**, then **Link to Domain**. Choose "SuiteCommerce" for SC or MyAccount, or "SuiteCommerce Advanced - Dev xxxx" for SCA ([article_1231025705](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/article_1231025705.html)).
2. Deploy the SuiteScript 2 application to the domain or site: "SuiteCommerce SS2", or "SuiteCommerce Advanced - Dev xxxx v2" for 2020.2+ ([article_1231024650](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/article_1231024650.html)).

*Field note (26.1):* if the domain is linked to the wrong SSP application (for example an old development application instead of SuiteCommerce), the site will load without its theme and extensions. Themes and extensions activate against the application. The symptom looks nothing like the cause.

## Touchpoints

- **Documented:** touchpoints on a domain override the website's, but you must still set them on the **website record**. "Domain-only touch point configuration is not supported" ([article_1231025705](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/article_1231025705.html)).
- *Field note (26.1):* after a sandbox refresh, some touchpoints were stored as **absolute URLs** that still pointed at the production host (`home`, `customercenter`, `serversync`). Check every touchpoint, not just the obvious ones. If a sandbox sends shoppers or session syncs to production, the result is confusing and potentially harmful.

## SuiteCommerce Configuration

- **Documented:** Commerce > Websites > Configuration. Choose the website **and domain**. Saving creates a configuration record for that domain, and each domain needs its own ([section_4346479003](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_4346479003.html)).
- **Copy Configuration** copies everything from one website/domain to another and **overwrites the destination**. Oracle recommends copying to a test domain first. Use it to give a new sandbox domain production's settings, rather than re-entering them.
- Tabs for themes and extensions only appear after they've been activated on the domain ([section_4666182345](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_4666182345.html)).
- With a CDN in front, changes take about 5 minutes to appear.
- *Field note:* an extension that "does nothing" on a new domain often just has its feature switched off in that domain's fresh, default configuration.

## Safe Mode

**Documented:** **Extensibility Layer Safe Mode** (`isSafeMode`) is under Configuration > **Advanced > Extensions**. It applies to SuiteCommerce and SCA 2020.2.1+. It is **on by default for SuiteCommerce** and off for SCA ([section_160461219470](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_160461219470.html)).
- When it's on, extensions that import disallowed private core modules aren't loaded, and an error is written to the console.
- Modules that are "allowed for now" load, with a console warning. Treat those warnings as future breakage.
- Turning Safe Mode off to make an extension work hides the problem; it doesn't fix it. Fix the extension to use the Extensibility API instead.

## Features to enable (new sites)

**Documented:** on **Setup > Company > Enable Features** ([section_N2656144](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_N2656144.html)):
- **Web Presence** tab:
  - Web Site
  - Advanced Site Customization
  - Descriptive URLs
  - Site Management Tools
  - one of **SuiteCommerce**, **SuiteCommerce MyAccount** or **SuiteCommerce Advanced**
  - Host HTML Files
  - Online Ordering
- **SuiteCloud** tab:
  - Client SuiteScript
  - Server SuiteScript
  - SuiteScript Server Pages
  - SOAP Web Services

Dependencies ([article_1114075116](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/article_1114075116.html)):
- Site Management Tools needs SuiteCommerce or SuiteCommerce Advanced enabled.
- Descriptive URLs can only be enabled once a domain has been set up.

## Field sets

**Documented** ([section_N2659559](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_N2659559.html), [section_3716578295](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_3716578295.html)):
- Field sets decide which item record fields the site can read through the Item Search API. Set them up on the website record (Commerce > Websites > Website List > Edit) on the **Field Sets** subtab.
- Field set IDs must be lowercase alphanumeric, with no spaces or special characters.
- **Field sets are public.** Anyone on the internet can request the fields you include, so don't expose costs, internal notes, or anything else sensitive.
- SuiteCommerce expects a standard set of field set IDs, including `order` (needed for My Account order history), `search`, `details`, `matrixchilditems`, `matrixchilditems_search`, `correlateditems`, `relateditems`, `typeahead`, `itemssearcher`, `relateditems_details`, and `correlateditems_details`.
- For SC and SCA, Oracle provides a setup script that creates these field sets. Run it in the SuiteScript Debugger as **SuiteScript 1.0**, and delete any existing field sets first. There's no setup script for MyAccount.
- **To expose a custom item field:**
  1. Give at least one item a value.
  2. Add the field to a field set, e.g. `details`.
  3. Rebuild the search index.
  4. Check it with `/api/items?id=<id>&fields=<field_id>`.
  5. Use it in a template ([developer portal](https://developers.suitecommerce.com/expose-custom-field-data-to-the-frontend.html)).

## Search index

**Documented:**
- **Rebuild it manually:** Commerce > Websites > Website List > **Edit** > **Actions > Rebuild Search Index** ([bridgehead_1500035326](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/bridgehead_1500035326.html)).
  - The rebuild can take up to 10 minutes to start, and longer for large catalogues.
  - You can only request it **twice in 24 hours**, so don't spend a request until your field sets and settings are final.
  - It does nothing on an inactive site.
- **Full rebuilds happen automatically** when you change facets, search fields, or sort options on the **Search Index** subtab. Removing a search field only triggers one if you remove all of its match types. They also happen when you add or remove languages or subsidiaries, change site currencies while currency-based fields are facets or sort options, change **Include Out Of Stock Items in Web Store**, or reactivate a site ([bridgehead_1500035290](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/bridgehead_1500035290.html)).
- **Incremental updates** happen automatically when item records change (including through CSV import), and with pricing, availability, and category changes ([bridgehead_1500035310](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/bridgehead_1500035310.html)).
- **Check progress:** Commerce > Websites > Website List, then **View** in the **Search Index Status** column. "Index is live" means the new index is serving searches ([bridgehead_1500035318](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/bridgehead_1500035318.html)).

## Caching

**Documented:**
- **Default CDN cache times** ([section_4411360163](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_4411360163.html), [bridgehead_4170304533](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/bridgehead_4170304533.html)):
  - static files (images, CSS): 7 days
  - session-independent scripts: 2 hours
  - content delivery (`page.ss`) and Item Search API responses: 5 minutes
- **Clear it:** Commerce > Content Management > **Cache Invalidation Requests > New** ([section_1495124477](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_1495124477.html)).
  - Choose the domains and either the whole domain or specific paths.
  - Use it after redeploying, when the site still serves old file cabinet content, scripts, CMS content, or Item Search API output.
  - Oracle notes that CDN invalidation takes about 7 minutes ([bridgehead_4170304533](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/bridgehead_4170304533.html)).
  - It **doesn't** clear visitors' browser caches ([chapter_4169406426](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/chapter_4169406426.html)).
  - Track the status at Commerce > Content Management > Cache Invalidation Requests.
- **Automatic invalidation** happens when a hosted file is modified or overwritten, but **not** when a file is moved, renamed, deleted, or newly uploaded ([section_1496421879](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_1496421879.html)).
- Publishing Site Management Tools content clears that site's caches automatically.

## Sandbox refresh checklist

**Documented:**
- Domains are **not copied** to a sandbox. You must set them up again after every refresh.
- Domain names must be unique across all of an account's sandboxes.
- Hard-coded links aren't rewritten ([section_1516026974](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_1516026974.html)).

Steps:

1. **DNS and certificate.** Point a hostname you control at NetSuite's hosting, as the domain setup page describes.
   - *Field note:* if the same sandbox hostname was used before the refresh, its DNS and certificate may still be valid. Then only the NetSuite domain record needs re-creating.
   - Keep sandbox hostnames on a DNS zone your team controls. A domain registered years ago in an account nobody can log into is a dead end.
2. **Create the domain** (Commerce > Hosting > Domains), using the **same type as production**, and link it to the website.
3. **Link the SSP application** and deploy the SS2 application (see above).
4. **Touchpoints:** set them on the website record, check that **every one** points at the sandbox host, and fix any absolute production URLs.
5. **Configuration:** use **Copy Configuration** from production's domain to the new domain (it overwrites the destination), then change anything that must differ in sandbox.
6. **Activate** the theme and extensions on the new domain, matching production's set. *Field note:* the refreshed sandbox already held the deployed theme and extension files in its File Cabinet, so we could activate them without redeploying.
7. **Developer tools:** create a token for the sandbox (`--to`, and `--account 123456-sb1` if needed). Keep it in a separate tools folder from production, as Oracle recommends.
8. **Verify** in the browser console on the sandbox site:
   - the account is the sandbox
   - the shopping and checkout hosts are the sandbox hosts
   - the expected theme and extension namespaces are loaded
