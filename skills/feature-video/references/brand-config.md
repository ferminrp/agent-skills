# Brand config reference

`brand.config.ts` is the only place project-specific brand values should live. Components under `src/brand/` read from it; do not hard-code palette names, font families, or URLs in compositions.

## Discovering values

1. Search the product repo for design tokens (CSS variables, Tailwind theme, Figma tokens export).
2. Read brand or marketing docs for tagline, tone, and approved claims.
3. Locate logo SVGs (marketing site, `public/`, or design repo) and note light vs dark background usage.
4. If something is missing, ask the user once with a short checklist (colors, fonts, logos, URLs, copy rules).

## Fields

| Area | Purpose |
| --- | --- |
| `neutral` | Background and text scale (50–950). Used by `BrandBackground`, frames, captions. |
| `fonts.sansFamily` / `monoFamily` | CSS `font-family` stacks after local fonts load. |
| `fonts.faces` | `{ family, file, weight }` under `public/` for `FontFace` loading. |
| `logos` | Paths to SVG icon and lockup, `lightInk` on dark scenes, `darkInk` on light scenes. |
| `motion.easeBezier` | Cubic bezier for `brandEase` (default matches common product motion). |
| `product` | `name`, `defaultAppHost` (browser chrome), `closingLine`, `websiteUrl`. |
| `copy.locale` | BCP 47 tag for Playwright (`en-US`, `es-AR`, …). |
| `copy.toneRules` | Bullet rules the agent must follow in titles and body copy. |
| `copy.demoDataPrefix` | Prefix for seeded ids (`video-demo-`). |

## Tone and demo data

- Match the product’s voice (formal, casual, regional second person, etc.) using `toneRules`.
- Demo personas should look believable for `copy.locale` (names, phone formats, currency) without using real people.

## Login hook

`scripts/lib/login.mjs` must export `loginAuthenticated` for your stack. The stub throws with instructions; replace with magic-link seeding, fixture cookies, or a test account flow documented in the app repo.