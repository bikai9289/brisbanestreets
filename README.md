# Brisbane Streets Field Guide

Independent English-language fan guide for Brisbane Streets. Static HTML, CSS and JavaScript; no database, sign-in, tracking integration or game files.

The homepage provides an outbound Play entrance and sections for mission-menu help, map basics and practical tips. Play opens the official game in a new tab. These sections are interface-based references, not mission-completion walkthroughs. Existing controls and loading/save guides remain on their original routes.

## Local preview

From the repository root:

```sh
python -m http.server 4311
```

Open http://localhost:4311/.

## Build and deploy

The editable source and generator are in `designs/brisbane-streets/`.

```sh
python3 designs/brisbane-streets/build.py --output dist
```

For Cloudflare Pages, use the command above and set the output directory to `dist`. Build requires Python's standard library only. The export excludes design notes, local screenshots and verification reports. `_redirects` maps former template routes; `404.html` is the missing-page response.

The domain configured in canonical URLs and sitemap is https://brisbanestreets.online/. Deployment, DNS, HTTPS, Search Console and analytics setup are separate operational steps.

## Content and attribution

This is an unofficial guide, not affiliated with or endorsed by the game's developer. Play buttons link to https://brisbane-streets.pages.dev/. No game code or assets are redistributed.

City photograph: [Brisbane City Skyline](https://commons.wikimedia.org/wiki/File:Brisbane_City_Skyline.jpg) by Nickwallen, [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Resized and shown with a dark overlay; photograph adaptations retain that license. This photograph is not game footage. The photo license does not license the entire site's code.

See `designs/brisbane-streets/README.md` for design details and optional local browser verification.
