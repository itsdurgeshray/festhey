# FestHey on Next.js

Every FestHey page (landing, listings, fest and event pages, blog, info pages, the organiser
and student dashboards, and the login and registration flows) running as Next.js App Router routes.

## Run it

```bash
npm install
npm run dev     # http://localhost:5212
npm run build && npm start
```

`predev` and `prebuild` copy the shared design system (`../assets`: CSS, JS, images, Lucide icons)
into `public/assets`, so the static site and the Next app always use the same files.

## How it is built

- `app/layout.jsx` holds the fonts, `site.css` (the design system tokens and components) and the grain overlay.
- Each route in `app/<page>/page.jsx` is real JSX: `className`, `htmlFor`, style objects, `defaultValue`
  and `defaultChecked`. Links point at clean routes (`/fest`, `/org-event?tab=regs`).
- Page stylesheets load with `precedence="page"`, so they always come after `site.css`.
- `app/components/ScriptChain.jsx` loads each page's interaction scripts in order after hydration
  (GSAP, Lenis, then `site.js`, `app.js`, `dash.js` and so on).
- Old links such as `/fest.html` redirect to `/fest`.
- Text and spacing are copied exactly, and the converter follows the browser's HTML rules for tags
  that close themselves (`<option>`, `<li>`, `<p>`...), so React hydrates every page without errors
  and the `anim`/`figma` class on `<html>` is never lost.
- To run `next dev` next to a production build, give it its own folder: `NEXT_DIST_DIR=.next-dev npm run dev`.

## Updating pages

The routes are generated from the static pages by `scripts/port.py`. Change a page in
`../assets/src/*.py`, rebuild the static HTML, then run:

```bash
npm run port
```

## Routes

| Area | Routes |
| --- | --- |
| Public | `/`, `/fests`, `/fest`, `/event`, `/team`, `/colleges`, `/college`, `/blog`, `/article`, `/about`, `/help`, `/privacy`, `/refund` |
| Auth | `/login`, `/register` (`?role=organiser`), `/verify`, `/org-verify`, `/forgot`, `/reset` |
| Organiser | `/org`, `/org-gate`, `/org-fests`, `/org-fest`, `/org-event` (`?tab=regs`, `?tab=wallet`), `/org-create-fest`, `/org-create-event`, `/org-college`, `/org-ads`, `/org-ad-new`, `/org-plans` (`?plan=pro`), `/org-upgrade` |
| Student | `/me`, `/me-registrations`, `/me-registration` (`?state=done`), `/me-saved`, `/me-payments` |
| Design system | `/design-system`, `/system` |
| Earlier versions | `/v1`, `/v2`, `/v3`, `/v4` |

Add `?figma` to any route for the static, animation-free version used for Figma import.
