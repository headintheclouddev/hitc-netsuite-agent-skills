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
