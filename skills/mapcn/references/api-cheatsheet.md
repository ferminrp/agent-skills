# mapcn API Cheatsheet

This file is a compact operational guide for frequent mapcn integration tasks.

## Good Defaults

- Start with uncontrolled map for quick delivery.
- Add explicit container height (`h-[400px]` or larger).
- Enable basic controls via `MapControls`.
- Move to controlled viewport only when external state sync is needed.
- Use clusters or GeoJSON layers for large datasets.

## Component Reference

## `Map`

Purpose:

- Core map container and camera state owner.

Common props:

- `initialViewState`: initial camera values (`longitude`, `latitude`, `zoom`, optional pitch/bearing).
- `viewport`: controlled view state object.
- `onViewportChange`: controlled mode callback.
- `styles`: optional map style override (MapLibre-compatible).
- `children`: controls, markers, layers, routes, popups.

Typical patterns:

- Uncontrolled quick start:
  - `<Map initialViewState={...}>...</Map>`
- Controlled state:
  - `<Map viewport={viewport} onViewportChange={setViewport}>...</Map>`

## `MapControls`

Purpose:

- Adds standard map UI controls.

Common props:

- `showZoom?: boolean`
- `showCompass?: boolean`
- `showLocate?: boolean`
- `showFullscreen?: boolean`
- `position?: "top-left" | "top-right" | "bottom-left" | "bottom-right"`

## `MapMarker`

Purpose:

- Places a marker at a map coordinate.

Common props (typical):

- coordinate/position values (longitude + latitude)
- interaction handlers (click/open behavior)

Used with:

- `MarkerContent`
- `MarkerPopup`
- `MarkerTooltip`
- `MarkerLabel`

## `MarkerContent`

Purpose:

- Custom JSX content for marker visual body.

Use when:

- You need non-default marker visuals.

## `MarkerPopup`

Purpose:

- Popup content anchored to a marker context.

Use when:

- You want marker-specific detail cards.

## `MarkerTooltip`

Purpose:

- Lightweight hover/focus annotation for markers.

## `MarkerLabel`

Purpose:

- Static text label associated with marker rendering.

## `MapPopup`

Purpose:

- Standalone popup anchored to map coordinates.

Use when:

- Popup lifecycle is independent from marker component tree.

## `MapRoute`

Purpose:

- Draw route/path overlays.

Typical inputs:

- ordered coordinate array
- style or interaction options for route rendering

## `MapClusterLayer`

Purpose:

- Cluster large point sets using GeoJSON source data.

Use when:

- Marker count is high and DOM marker performance degrades.

Typical input:

- GeoJSON `FeatureCollection<Point>`

## `useMap`

Purpose:

- Access map context/instance from child components.

Use cases:

- register map event listeners
- read map state
- invoke map methods through context-safe access

Lifecycle guidance:

- attach listeners in effect hooks
- cleanup listeners on unmount/dependency changes

## `MapRef`

Purpose:

- Imperative map control from parent scope.

Common methods (MapLibre-level):

- `flyTo(...)`
- camera/zoom/bearing methods

Use when:

- user requests imperative transitions or programmatic camera control.

## Callback and Data Shape Notes

Viewport shape (typical):

```ts
{
  longitude: number;
  latitude: number;
  zoom: number;
  pitch?: number;
  bearing?: number;
}
```

Coordinate conventions:

- keep consistent coordinate ordering across app code
- validate expected shape before passing into markers/routes/popups

## Performance Rules of Thumb

- Up to a few hundred points: DOM markers are usually acceptable.
- Beyond that: prefer `MapClusterLayer` or GeoJSON-based rendering.
- Minimize unnecessary re-renders by memoizing heavy marker lists.
