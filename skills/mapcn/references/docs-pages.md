# mapcn Docs Pages Index

## Introduction

URL: `https://www.mapcn.dev/docs`

- High-level overview of mapcn and its design intent.
- Positions mapcn as a practical map component layer for React + shadcn workflows.
- Clarifies mapcn sits on top of MapLibre.

Use this page when:

- You need to explain what mapcn is.
- You need to frame whether mapcn fits a project.

## Installation

URL: `https://www.mapcn.dev/docs/installation`

- Canonical setup command:
  - `npx shadcn@latest add @mapcn/map`
- Prerequisites include Tailwind CSS and shadcn/ui.
- Expected import path pattern starts from `@/components/ui/map`.

Use this page when:

- User asks how to install mapcn.
- Agent needs to bootstrap a new mapcn integration.

## API Reference

URL: `https://www.mapcn.dev/docs/api-reference`

- Lists available components, hooks, and exposed API surface.
- Documents key props and expected callback patterns.
- Useful as a lookup table when implementing feature-specific behavior.

Use this page when:

- You need prop names and signatures.
- You need to verify behavior for component options.

## Map

URL: `https://www.mapcn.dev/docs/basic-map`

- Minimal map rendering patterns.
- Initial camera/view configuration.
- Baseline component composition.

Use this page when:

- Building first runnable map view.
- Debugging why map does not render in a simple case.

## Controls

URL: `https://www.mapcn.dev/docs/controls`

- Control toggles and placement options.
- Typical utility controls for navigation and location.

Use this page when:

- User requests zoom/compass/locate/fullscreen controls.
- You need to adjust controls position.

## Markers

URL: `https://www.mapcn.dev/docs/markers`

- Marker rendering patterns and marker composition primitives.
- Marker content, labels, tooltips, and marker-attached popups.

Use this page when:

- User requests custom marker UI.
- You need point annotations with interactive content.

## Popups

URL: `https://www.mapcn.dev/docs/popups`

- Popup behavior and content patterns.
- Marker-attached vs standalone popup workflows.

Use this page when:

- User asks for click-driven details UI on map.
- You need floating info cards anchored to map coordinates.

## Routes

URL: `https://www.mapcn.dev/docs/routes`

- Route/path overlay patterns.
- Polyline rendering and interaction hooks.

Use this page when:

- User asks to draw routes or navigation-like lines.
- You need path overlays in mapcn.

## Clusters

URL: `https://www.mapcn.dev/docs/clusters`

- Point clustering with GeoJSON-backed datasets.
- Scale-friendly rendering for larger marker sets.

Use this page when:

- Data volume is too large for many DOM markers.
- User needs clustered point visualization.

## Advanced Usage

URL: `https://www.mapcn.dev/docs/advanced-usage`

- Imperative control patterns through `MapRef`.
- Context/hook access via `useMap`.
- Event wiring and low-level customization.

Use this page when:

- User asks for advanced MapLibre-level behavior.
- You need custom interaction/event lifecycles.
