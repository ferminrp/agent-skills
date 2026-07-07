---
name: product-shaping
description: Guided process for shaping product ideas, features, and specs by systematically uncovering the user's unknowns before anything gets built. Use this whenever the user wants to shape, spec, define, scope, or think through a product or feature — including phrases like "I have an idea for...", "help me shape...", "let's spec out...", "write a PRD/brief for...", "should we build...", or when they bring a vague product problem (churn, activation, a new market) and need to turn it into a concrete, buildable pitch. Also use when the user asks to brainstorm product directions or wants mockups to react to before committing to a spec.
---

# Product Shaping

Turn a fuzzy product idea into a shaped, pitch-ready spec by finding the user's unknowns *before* they become expensive. The core insight: the gap between what the user tells you (the map) and what the product actually needs (the territory) is made of unknowns. Your job is to surface them cheaply — through research, brainstorming, mockups, and interviews — rather than letting them be discovered in production.

## The unknowns framework

Classify what you learn into four quadrants and keep a running log throughout the session:

- **Known knowns** — what the user explicitly told you. Trust it, but probe if it conflicts with evidence.
- **Known unknowns** — things the user knows they haven't decided. Resolve via the Interview phase.
- **Unknown knowns** — criteria the user will only recognize when they see them ("I'll know it when I see it"). Resolve via Brainstorm + Prototype: show options, let them react.
- **Unknown unknowns** — things the user hasn't considered at all. Resolve via the Blind Spot Pass: research and teach.

Different quadrants need different techniques. Asking interview questions can't surface unknown unknowns (the user can't answer what they can't conceive of), and research can't resolve taste (the user must see options). Match the technique to the quadrant.

## Process

Run these phases in order, but adapt: skip a phase when there's clearly no signal to gain from it, and loop back when a later phase reveals a new unknown. Announce which phase you're in so the user can steer.

### Phase 0 — Starting point

Before anything else, get the user's context. Ask (briefly, in one message):

1. The idea or problem in their own words
2. Who it's for and what they'd do with it
3. Their experience with this domain (expert? first time?) — this calibrates how much teaching the Blind Spot Pass needs
4. Constraints: appetite (how much time/effort this is worth), team, existing product it lives in
5. What they already feel unsure about

From their answers, draft the initial unknowns log (all four quadrants) and share it. This log is the backbone of the session — update it visibly as phases resolve items.

### Phase 1 — Blind Spot Pass (unknown unknowns)

Research what the user doesn't know to ask about. Depending on the problem, this can include: competitor and comparable-product research (use web search), common failure modes for this kind of feature, regulatory/compliance angles, adjacent solutions to the same job-to-be-done, and what "great" looks like in this category.

Then *teach*, don't dump: explain the 3–6 most decision-relevant findings in plain language, each ending with the question it raises for their product. The goal is to upgrade the user's ability to shape, not to show research volume.

Skip or shorten this phase if the user is a domain expert shaping in familiar territory.

### Phase 2 — Brainstorm directions (unknown knowns)

Generate genuinely divergent options for the user to react to. Reactions are how "I'll know it when I see it" criteria get verbalized.

- Propose 3–5 distinct product directions, ordered cheapest → most ambitious. Make them *actually different* — different mechanisms, not the same idea at three sizes.
- For anything with a user-facing surface, offer an HTML prototype: a single self-contained HTML file with fake data showing the different directions side by side (tabs or stacked sections) so the user can compare. See [prototype-guide.md](references/prototype-guide.md) before building it.
- Ask the user to react: what resonates, what's off, what surprised them. Capture *why* — the reasons are the hidden criteria. Add each verbalized criterion to the unknowns log as a new known known.

### Phase 3 — References

Ask if there's a product, feature, or flow they've seen that feels right (or explicitly wrong). References carry detail the user can't articulate. If they name one, analyze what specifically it does — interaction model, information hierarchy, tone — and confirm which properties they want to inherit versus discard.

### Phase 4 — Interview (known unknowns)

Now resolve the remaining open decisions. Interview the user **one question at a time**, prioritizing questions whose answer would change the shape of the product (scope, core mechanism, target user) over ones that only change details. For each question, offer 2–4 concrete options with trade-offs rather than asking open-ended — options are faster to react to and surface criteria as a side effect.

Stop when remaining unknowns wouldn't change the shape — mark those as "deferred to build" in the log rather than forcing decisions the builder is better placed to make.

### Phase 5 — Write the shaping doc

Write the deliverable using the template in [shaping-doc-template.md](references/shaping-doc-template.md). Save it as a markdown file. Key qualities:

- **Shaped, not specified**: define the problem, the solution's core mechanism, and the boundaries — at "fat marker" fidelity. Leave implementation detail to whoever builds it; over-specifying reintroduces the too-rigid failure mode.
- The **unknowns log** goes in the doc: decisions made (with the reasoning), deferred unknowns, and explicit no-gos. This is what makes the doc useful to an agent or teammate who inherits it — they know where they may improvise and where they may not.
- If a prototype was made, reference it from the doc and ship both files together.

### Phase 6 — Gut check

Before closing, verify the shape actually matches the user's head:

- Give a 3–5 question quiz on the decisions in the doc ("What did we decide about X, and why?"). If they miss one, that section of the doc doesn't reflect their thinking — revisit it.
- Ask the killer question: "If this shipped exactly as shaped, what would disappoint you?" Whatever they answer is an unknown that escaped the process — fold it in.

## Working style

- Be a thought partner, not a stenographer. If the research or brainstorm suggests the user is solving the wrong problem, say so early — pivoting during shaping is cheap, pivoting during build is not.
- Keep the unknowns log visible and current; it's the session's shared state.
- Don't run the full process ceremonially on small ideas. A tiny feature might need only Phase 0, three interview questions, and a one-page doc. Match process weight to appetite.
- Deliverables are files, not chat text: `shaping-doc.md` always; `prototype.html` when there's a user-facing surface.

## Additional resources

- [prototype-guide.md](references/prototype-guide.md) — rules for HTML prototypes that trigger reactions
- [shaping-doc-template.md](references/shaping-doc-template.md) — deliverable structure for the shaping doc
