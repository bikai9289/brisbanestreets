# Brisbane Streets — design and site

Direction approved in chat: dark city photography with lime wayfinding. Original static template supplied in the project is the structural reference; the new site uses custom local CSS and no UI library.

Body copy is 18px; minimum interface text is 16px. Mobile layouts stack at 700px. FAQ uses native disclosures; control tabs support keyboard navigation. No tracking, external font dependency, game mirror, or unverified code walkthrough.

The preview folder and root deployment files are kept in sync by `python build.py`. Run this from the project folder after editing design source. The generator emits static HTML so content is readable without JavaScript; mobile controls can be selected with the device tabs.

Sources: https://brisbane-streets.pages.dev/ (controls, checked 2026-11-05); https://commons.wikimedia.org/wiki/File:Brisbane_City_Skyline.jpg (Nickwallen, CC BY-SA 4.0). Photo is resized with a CSS dark overlay. Photography adaptations remain CC BY-SA 4.0. UI is independent of the photo license.

Deployment: run `python3 designs/brisbane-streets/build.py --output dist` from the repository root and set Cloudflare Pages output directory to `dist`. Only the generated website belongs in that output, excluding design sources, audit notes and screenshots. Cloudflare Pages reads `_redirects` for former template URLs. 404.html handles missing routes. Submit sitemap.xml only after deployment; no indexing time is promised. A custom domain, DNS, live HTTP status codes, HTTPS, GSC verification and any analytics property still require their actual services; local checks do not verify them.

Local verification: with the preview served at port 4311, run `python designs/brisbane-streets/verify.py`. This checks desktop/mobile layouts, minimum visible font size, keyboard interactions, no-JavaScript fallback, links and the clean export. It requires the locally installed Python Playwright and Edge. Results are in verification.json.

Before publication: review copy and provider-specific privacy wording; add a real contact channel when available. No contact address has been invented. Metro code and map walkthroughs are intentionally not published without verification.
