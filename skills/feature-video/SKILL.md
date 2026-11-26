---
name: feature-video
description: "Make a short product video (30–60 s, MP4) that shows one feature flow using real UI captures, project brand tokens, and Remotion. Use when a feature ships and someone asks for a demo or launch video, a walkthrough, social clip, or to add or update a video in the collection."
---

# Feature video

Short videos that show **one feature, one flow** for the product’s primary audience. Copy the Remotion scaffold from this skill’s `assets/remotion-scaffold/` into your repo (commonly as `videos/`). Treat `src/example/ExampleFeature.tsx` as the template for a new composition.

The method, in one line: **brief → storyboard → real captures → composition → QA → render → deliver.** Do not skip the storyboard, and never invent UI.

## Brand config (fill per project)

Before capture or composition, create or update `brand.config.ts` at the scaffold root (see `references/brand-config.md` and `assets/remotion-scaffold/src/brand.config.ts`).

Derive values from the project’s design system, tokens, or brand docs when they exist. Ask the user only for what you cannot find:

- **Colors** — neutral scale for backgrounds and type (no hard-coded third-party palette names in code).
- **Fonts** — sans for titles/body, mono for step labels; local font files under `public/fonts/` and entries in `brand.config.ts` (do not rely on live Google Fonts in render).
- **Logos** — SVG paths for icon and lockup, light and dark ink variants.
- **Product URLs** — default host shown in `BrowserFrame`, marketing URL on the closing card, tagline or closing line.
- **Copy** — locale, tone-of-voice rules, and how demo personas should read for the target market (realistic names and emails; no real customer data).

## 1. Brief (ask only what you cannot read in the code)

- Which feature and which flow, from the end user’s point of view. One video = one flow, not a product tour.
- Where it runs: web app, signup form, mobile web, or another repo. Read its README, agent rules, and any `verify-*` or local-dev skill.
- Format: 16:9 1920×1080 by default. 9:16 1080×1920 only if they ask for socials/stories.
- Length: 30–60 s. Roughly 4–8 s per step.

Check the code for what the feature **really** does. If the brief mentions something that does not exist (for example, export to PDF when only Markdown exists), say so and leave it out of the video; do not mock it up.

## 2. Storyboard first

Write a shot list and show it to the user before you write any code:

| # | Step label | Title (benefit) | What you see | Seconds |
| --- | --- | --- | --- | --- |
| 0 | — | Opening line | Dark neutral background, logo lockup | 4 |
| 1 | `01 · Link` | Short benefit headline | App flow: empty → filled → result; zoom on key detail | 11 |
| … | | | | |
| n | — | Closing | Logo + tagline + product URL | 4 |

Caption rules (apply the project’s tone from `brand.config.ts`):

- Title = **benefit or outcome**, not the click (“Responses arrive on their own”, not “Click Leads”).
- Body: one sentence, about 20 words max, readable in the time the scene is on screen.
- Step label in mono: `0N · Name`. No extra eyebrows above titles elsewhere.
- Do not invent claims, numbers, or slogans not approved in brand docs.

## 3. Real captures with demo data

1. Run the app locally per its dev/verify docs. Use **local-only** data stores; never production or remote databases unless the user explicitly requires it.
2. Seed **fictitious, coherent** demo data with a configurable prefix (default `video-demo-` in `brand.config.ts`). Use realistic names and emails for the target market. No real clients. Fix values that would look wrong on screen (implausible numbers, broken date math).
3. Capture with Playwright using `scripts/lib/capture.mjs`:
   - `loginAuthenticated({ ... })` — implement project-specific auth in `scripts/lib/login.mjs` (magic link, test user, or session cookie). The scaffold ships a stub; copy and adapt it.
   - `openPublic(DESKTOP | MOBILE)` for unauthenticated surfaces.
   - Desktop 1440×900 CSS px, DPR 2. Mobile `iPhone 14` or the device the product targets.
   - One screenshot **per UI state** (empty form, filled form, success state, “Copied” toast…). Crossfades between states read as interaction.
   - `box(locator)` gives CSS px for each control. Cursor and camera in Remotion use those coordinates. Save them in `src/<feature>/boxes.json`.
   - `scrollTo(locator, offset)` scrolls the container that actually scrolls (often not `window`). Frame each section so its heading is visible.
4. Convert to JPG with `pngsToJpg(src, "public/<feature>")` and review every capture before using it.

## 4. Composition

In `src/<feature>/<Feature>.tsx`, reuse `src/brand/`:

- `Scene` (fade in/out with brand easing), `BrandBackground` (`light` for product, `dark` for opening/closing), `ProductLayout` + `Caption`.
- `AppShot` / `Screen`: crossfading screenshots + `cursor` keys (`click: true` draws the press) + `camera` keys (`scale`, focus `x`,`y` in CSS px; the frame never shows past the edges).
- `BrowserFrame` with the real URL, `PhoneFrame` for mobile, `BrandLogo` (files from config, correct ink polarity).
- Easing: `brandEase` / `keyframes()` from `src/brand/motion.ts`.

Register the composition in `src/Root.tsx`, add `render:<feature>` to `package.json`, and document the video in the project’s videos README.

```tsx
export const SCENES = { intro: 120, step1: 300, outro: 120 } as const;
export const DURATION = Object.values(SCENES).reduce((a, b) => a + b, 0);

function Step1() {
  return (
    <Scene>
      <BrandBackground />
      <ProductLayout
        caption={
          <Caption
            step="01 · Step"
            title="Benefit in a few words."
            body="One sentence that explains the outcome."
          />
        }
      >
        <AppShot
          url="app.example.com/path"
          images={[
            { src: "feature/state-1.jpg", from: 0 },
            { src: "feature/state-2.jpg", from: 60, fade: 8 },
          ]}
          cursor={[
            { f: 20, x: 700, y: 500 },
            { f: 52, x: 316, y: 189, click: true },
          ]}
          camera={[
            { f: 0, scale: 1, x: 720, y: 450 },
            { f: 90, scale: 1.5, x: 1230, y: 330 },
          ]}
        />
      </ProductLayout>
    </Scene>
  );
}
```

Rules of thumb:

- Change the screenshot 2–4 frames after the click, with `fade: 4–8`. For typing, crossfade empty → filled with `fade: 40–50`.
- Zoom only to read something (a link, a value). 1.2–1.5 for a section, 2–2.2 for one detail. Keep section headings in view.
- Each scene needs ~2.5 s with nothing moving after the caption shows so people can read it.
- Text in files (Markdown, JSON): import as a TS string. `fetch` during render is unreliable.

## 5. QA before you deliver

```bash
cd videos   # or wherever the scaffold lives
npx tsc --noEmit
npm run dev                                  # Studio: scrub every scene
npx remotion render <Composition> out/<feature>.mp4
npm run qa -- out/<feature>.mp4              # contact sheet, one frame every 3 s
```

Review the contact sheet **and** full-size frames at each zoom (`ffmpeg -ss <t> -i out/x.mp4 -frames:v 1 f.png`). Check:

- [ ] Every scene matches its caption: relevant values visible, not a collapsed list or half-cut panel.
- [ ] Headings and key values are not clipped. Cursor lands on the real control.
- [ ] Demo data is coherent across screens. No error toasts or debug chrome left in captures.
- [ ] Brand checklist from `brand.config.ts`: fonts, neutral palette, logo polarity, tone rules.
- [ ] Nothing shown that does not exist in the product.

## 6. Deliver and save

- Send the MP4 (and a poster from `npm run still` if configured). Say what you could not show and why.
- Commit `src`, `public/<feature>`, scripts, and README on a branch. **Do not commit `out/`** (deliverable only).
- Stop only the processes this run started. Leave local dev data as-is unless the user asks to reset.

## Gotchas (generic)

- Modal sheets often close on outside click; use `blur()` or targeted clicks instead of clicking `body`.
- Deep-linked wizard steps may need a debug query or seed state so you can screenshot mid-flow; hide debug UI before capture.
- Prefer stable selectors (`getByRole`, accessible name) over class names that change with refactors.
- Pin Playwright to the version already installed with browsers in the project; avoid redundant `playwright install` unless versions changed.
- If auth uses time-limited tokens, generate them inside the capture script right before `page.goto`.

## Scaffold layout

```
assets/remotion-scaffold/
├── package.json
├── tsconfig.json
├── remotion.config.ts
├── src/
│   ├── brand.config.ts      # ← project-specific
│   ├── brand/               # components, motion, fonts, tokens
│   ├── Root.tsx
│   └── example/             # neutral placeholder composition
├── scripts/
│   ├── contact-sheet.mjs
│   └── lib/
│       ├── capture.mjs
│       └── login.mjs        # ← implement auth for your app
└── public/
    ├── brand/               # logo SVGs
    └── example/             # JPG captures for the sample
```

Copy the tree into the target repo, run `npm install`, then follow the phases above.