# Sources

Every NetSuite fact in `SKILL.md` comes from Oracle's documentation, linked below (checked October 2026). Read this file when a user asks where a recommendation comes from, or when you need to double-check a detail before stating it.

Oracle updates its help pages with each release. If a page here conflicts with what the user sees in their account, trust the account and say there's a discrepancy.

## Measuring

- **Performance Details** (double-click the logo; Server/Network/Client breakdown; Total may not apply to reports, dashboards, centers, or saved searches): https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_48151513026.html
- **Network time and the ISP** (the "internet service provider" quote is on the Performance Details page above; the CDN is covered here): https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_0824033849.html
- **Client-side troubleshooting** (RAM, antivirus and firewall, add-ons, the 200-line sales order example): https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_N574405.html
- **Reporting a performance problem to Support**: https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/article_1030024032.html

## APM SuiteApp

- **Overview and official name**: https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/chapter_4283522055.html
- **Installing; prerequisites; bundle 67350 unsupported since March 7, 2023**: https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/bridgehead_4309364558.html
- **APM Setup** (granting access to roles and employees): https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_4553051128.html
- **List of APM tools**: https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_4304060408.html
- **Profiler Details**: https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_1547529505.html
- **FAQ** (30-day data window, 10,000-row CSV limit, Processors Monitor replacing the Script Queue Monitor): https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_4283525918.html

## Scripts, workflows and customization

- **"Customization… is often the main cause of performance challenges"**: https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/chapter_N571805.html
- **User event scripts** (the "ten beforeLoad scripts" example, under 5 seconds, counting bundled scripts): https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/chapter_N3361453.html
- **Script performance** (combining scripts, inactivating deployments, execution context, log level Error or Emergency, running as Administrator, targets, search operators): https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_4460387617.html
- **Logging limits** (100,000 calls per 60 minutes, automatic log-level increase, 30-day purge): https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_N3352137.html
- **Workflow performance**: https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_1540490044.html
- **Forms**: https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/chapter_N2852749.html
- **General account practices** (unique forms and fields, role switching, imports outside business hours): https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_0914011325.html
- **Script Execution Logs**: https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_4375937190.html
- **Scripted Records**: https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/article_1029093731.html and https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/chapter_N2936246.html

## Browsers

- **Supported browsers**: https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_N340018.html
- **Browser troubleshooting**: https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_0825025054.html

## First loads and caching

- **Why first loads are slower** (what clears caches; the Administrator role): https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_0914012159.html
- **Account Warmer FAQ**: https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/article_0209013127.html
- **Account Warmer: custom records not supported**: https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/article_0209010010.html
- **Oracle SuiteApps list** (describes Account Warmer differently from its FAQ): https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/article_3134602194.html
- **Caching for NetSuite** (The Next Digitals): https://thenextdigitals.nl/en/caching-for-netsuite/

## HITC field guidance (not from Oracle)

The code-level causes in Step 4, the network checks (comparing networks, involving IT), and the advice about connector roles come from HITC's own experience. They aren't presented as Oracle guidance.

## Related skills

- **Oracle SuiteCloud Agent Skills**, including `netsuite-sdf-safe-guide` for code-level performance patterns: https://github.com/oracle/netsuite-suitecloud-sdk/tree/master/packages/agent-skills
