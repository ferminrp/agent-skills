# Prototype Guide

The prototype exists to trigger reactions, not to demo. Its job is to convert unknown knowns ("I'll know it when I see it") into stated criteria. Optimize for comparison speed, not polish.

## Rules

- **One self-contained HTML file** (`prototype.html`). Inline CSS/JS, no build step, no external dependencies except optionally a CDN font. It must open by double-clicking.
- **Fake data that looks real.** Plausible names, realistic numbers, real-length text. Lorem ipsum hides layout problems and dampens reactions.
- **Genuinely divergent directions.** 3–4 variants that differ in mechanism or mental model, not in color scheme. If a viewer can't say in one sentence how variant B differs from A, they're not different enough.
- **Easy comparison.** Tabs or a switcher at the top, one variant visible at a time, labeled with a short name and a one-line thesis (e.g. "Direction B: the feed IS the product").
- **Interactive only where it changes understanding.** Fake a click-through if the flow is the thing being evaluated; keep it static if layout is the question. Don't wire up anything real.
- **No backend, no state, no localStorage.** It's a sketch.

## Prompting reactions

After delivering, ask three questions and log the answers as criteria:

1. Which direction is closest, and what specifically pulls you to it?
2. What in any variant is actively wrong? (Negative reactions are the sharpest criteria.)
3. What did you expect to see that isn't in any of them?
