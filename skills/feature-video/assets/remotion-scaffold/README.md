# Feature video · Remotion scaffold

Minimal Remotion project bundled with the `feature-video` agent skill. Copy this folder into your product repo, rename if needed, then follow `skills/feature-video/SKILL.md`.

## Quick start

```bash
npm install
npm run dev
npm run render:example
npm run qa -- out/example.mp4
```

## Customize

1. Edit `src/brand.config.ts` (colors, fonts, logos, URLs, copy rules).
2. Replace `public/brand/*.svg` with your logo files (keep light/dark ink naming).
3. Implement `scripts/lib/login.mjs` for Playwright capture.
4. Add `src/<feature>/` compositions and JPG captures under `public/<feature>/`.

The `ExampleFeature` composition (~10 s) uses neutral placeholder screenshots to prove the shared components.