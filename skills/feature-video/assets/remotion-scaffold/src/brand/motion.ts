import { interpolate } from "remotion";
import { brandEase } from "./tokens";

export type Key = { f: number; v: number };

export function keyframes(frame: number, keys: Key[]): number {
  if (keys.length === 0) return 0;
  if (frame <= keys[0].f) return keys[0].v;
  for (let i = 0; i < keys.length - 1; i++) {
    const a = keys[i];
    const b = keys[i + 1];
    if (frame <= b.f) {
      return interpolate(frame, [a.f, b.f], [a.v, b.v], {
        easing: brandEase,
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      });
    }
  }
  return keys[keys.length - 1].v;
}

export function enter(frame: number, start: number, duration = 22): number {
  return interpolate(frame, [start, start + duration], [0, 1], {
    easing: brandEase,
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
}