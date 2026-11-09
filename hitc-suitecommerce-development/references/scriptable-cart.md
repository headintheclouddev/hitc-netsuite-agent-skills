# Scriptable Cart

Contents: When to use it · Enabling it · Deploying a script · SuiteScript versions · Supported events · Web store context and permissions · Performance and recursion · Common patterns · Limits and gotchas · Debugging

Base URL for Oracle links: `https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/`. All content here is **documented** unless it's marked as a field note or unconfirmed.

## When to use it

- **What it is:** Scriptable Cart lets you "use SuiteScript to invoke client scripts on the sales order form used for website orders". The script runs when a sales order is created on the website or in the back-office UI ([article_63082620519](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/article_63082620519.html)).
- **Where it applies:** it started as a Site Builder feature, but works with SuiteCommerce and SuiteCommerce Advanced. Oracle calls it an advanced feature to use "only … when it is not possible to achieve your customization through other means" ([article_164815363102](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/article_164815363102.html)).
  - The website preferences page lists SuiteCommerce, SCA and Site Builder for the Scriptable Cart settings, but not SuiteCommerce MyAccount ([section_N2562624](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_N2562624.html)).
- **When to reach for it:** use it when the change has to happen on the order itself and the Frontend Extensibility API can't do it. Examples are changing an item's rate (Oracle says this "can only be implemented using Scriptable Cart"), adding or removing lines from code, or validating lines as they're added.
  - For changes that are only presentation, use an extension instead.
- **Check for native settings first.** For example, the website record has a native **Minimum Order Amount** field on the **Shopping** subtab ([section_N2462817](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_N2462817.html)). Make sure no setting already does what you need before scripting a rule.

## Enabling it

1. Go to **Setup > Company > Enable Features**.
   - On the **Web Presence** tab, check **Advanced Site Customization**.
   - On the **SuiteCloud** tab, check **Client SuiteScript** ([article_63082620519](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/article_63082620519.html)).
2. Go to **Commerce > Websites > Website List**, click **Edit**, open the **Setup** tab, and under **Preferences** check **Scriptable Cart and Checkout**.
3. Set the two scripting templates ([section_N2549847](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_N2549847.html)):
   - **Scripting Template (Credit Card)**: your customised Sales Order – Cash Sale form.
   - **Scripting Template (Invoice)**: your customised Sales Order – Invoice form.
   - If customers buy on terms, attach the script to **both** forms.
4. Set the role on the script deployment to the **same customer center role** that's selected in **Default Role for New Customers** (Setup > Company > General Preferences).

## Deploying a script

You can attach the script in two ways ([section_N2553295](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_N2553295.html), [article_80082826669](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/article_80082826669.html)):

- **Form level:** add the functions on the custom sales order form's **Custom Code** subtab. Oracle says this "provides the most flexibility for multiple websites".
- **Record level:** this is Oracle's SuiteCommerce/SCA walkthrough.
  1. Create a script record of type **Client** and enter your function name in **Recalc Function**.
  2. On the deployment, set **Applies To** to **Sales Order** and **Status** to **Released**.
  - Oracle says a record-level script "can run on all sales orders in the application and on the web store", back-office ones included. That's why checking the context (below) matters.
- `beforeSubmit`/`afterSubmit` logic must go in a **User Event** script ([section_N2545908](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_N2545908.html)).
- On the **checkout** form, "client scripts attached to the checkout form do not run". Only user event scripts can run there.

## SuiteScript versions

From [section_N2545233](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_N2545233.html):

- "SuiteScript 2.1 client scripts are not currently supported in the Scriptable Cart."
- You can't use SuiteScript 2.0 user event scripts and 2.0 client scripts together for Scriptable Cart. Oracle suggests a **1.0 user event with a 2.0 client script** in most cases. The reverse combination is also supported.
- Oracle's samples are all SuiteScript 1.0. Whether 2.1 **user event** scripts are supported is unconfirmed.

## Supported events

Only a subset of client events is available ([section_N2545233](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_N2545233.html), [section_N2545908](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_N2545908.html), [section_0517085825](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_0517085825.html)):

| Event | Notes |
|---|---|
| pageInit | The type must be `create` |
| fieldChanged | |
| postSourcing | |
| recalc | Fires after the cart changes. One Oracle page says the action can only be `commit` or `remove`. Another lists `commit`, `batchcommit`, `insert`, or `remove`. Handle all four |
| validateLine | Return `true` or `false`. Returning nothing counts as `false` |
| saveRecord | Return `true` or `false` |

Other client events (lineInit, validateField, validateInsert, validateDelete) aren't in Oracle's supported list, so don't rely on them.

## Web store context and permissions

- **Check the context first.** In SuiteScript 1.0, exit unless `nlapiGetContext().getExecutionContext() === 'webstore'`. Back-office orders return `'userinterface'` ([article_1141046782](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/article_1141046782.html), [section_0517032601](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_0517032601.html)).
  - Oracle says this is "not simply a design choice", because permissions differ between the two contexts.
  - In 2.x, `runtime.ContextType.WEBSTORE` exists ([section_4296646855](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_4296646855.html)). Oracle doesn't show it being used in a Scriptable Cart 2.0 client script, so test it before relying on it.
- **Guest shoppers:** an `entity` value of `0` means the shopper isn't logged in. Handle that case ([section_0517032601](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_0517032601.html), [section_N2552581](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_N2552581.html)).
- **Permissions:** Scriptable Cart "runs with either customer center or shopper access", unlike a UI script, which runs with administrator permissions ([article_63082620519](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/article_63082620519.html)).
  - If the script reads a custom record, that record's permissions must allow those roles. Oracle's sample sets Administrator, Customer Center and Shopper to Full ([section_N2552581](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_N2552581.html)). Grant only what the script needs.

## Performance and recursion

- "With Scriptable Cart, functions are called much more frequently, which can negatively impact performance" ([article_63082620519](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/article_63082620519.html)). The order's other events run too ([section_N2545908](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_N2545908.html)). Keep handlers cheap.
- Oracle's best practices ([article_0151255693](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/article_0151255693.html)):
  - Include a custom recalc function.
  - Cache lookups in the session with `getSessionObject`/`setSessionObject` rather than searching on every event.
  - Guard against recursion with a flag that's reset in `finally`. A recalc that changes lines triggers recalc again.
- Oracle's gift wrap sample uses a body field as the recursion flag (`custbodyprocessing`) ([section_N2557809](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_N2557809.html)).

## Common patterns (Oracle samples)

- **Adding a charge line** (gift wrap, [section_N2557809](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_N2557809.html)):
  - In recalc, use `nlapiSelectNewLineItem` and `nlapiCommitLineItem` to add the line, and `nlapiRemoveLineItem` to take it off.
  - Requirements: **per-line-item taxing must be disabled**, and the charge item needs **Display in Web Site** checked.
  - Use this sample as the starting point for a fee or surcharge line. The Extensibility API's Cart can't reliably manage such a line (see the field note in `extensibility-api.md`).
- **Changing a rate** (gift card, [article_1141046782](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/article_1141046782.html)): set the line's `price` to `-1` (custom), then set `rate`.
- **Quantity limits** ([section_N2558716](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_N2558716.html)): validateLine checks quantities as lines are added, and a user event `afterSubmit` records what was bought.
- **Passing data from the front end:** Oracle's pattern is to set a custom transaction body or column field in SuiteCommerce and read it in Scriptable Cart ([article_63082620519](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/article_63082620519.html)).
  - From an extension (2021.1+), `Cart.setTransactionBodyField({ fieldId, type, value })` sets a body field ([release note](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_160571233509.html), [API reference](https://system.netsuite.com/help/helpcenter/en_US/APIs/SuiteCommerce/Extensibility/Frontend/Cart.html)).
  - Oracle doesn't explicitly connect the two, so check that your script sees the value in your version.

When copying Oracle's samples, check them carefully. At least one validateLine sample has `if (type = 'item')`, which assigns rather than compares.

## Limits and gotchas

From the [FAQ](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_N2553295.html) unless noted otherwise:

- **Checkout flow:** you can't use SuiteScript to skip checkout pages or change their order.
- **Registration:** "SuiteScript is not available for use in web store registration" ([chapter_N2545000](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/chapter_N2545000.html)).
- **Fields:** the fields on the custom sales order form depend on the features enabled in the account. Referencing a field that isn't there causes "Invalid Field Reference" errors.
- **Alerts:** Oracle contradicts itself. The [overview](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/article_63082620519.html) says you can't trigger alerts in Scriptable Cart, while some samples use `alert()`. To stop a line, return `false` from validateLine rather than relying on alerts.

## Debugging

From [article_69152608165](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/article_69152608165.html):

- Log with `nlapiLogExecution` and test in a fresh private or incognito session. Oracle notes that changes "are not available in open sessions or browsers".
- Remove debug logging when you're done.
- *HITC advice:* test as a guest, as a logged-in customer, and on a back-office sales order, to make sure the context check works both ways.
