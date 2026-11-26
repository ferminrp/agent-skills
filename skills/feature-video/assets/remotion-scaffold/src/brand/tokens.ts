import { Easing } from "remotion";
import { brandConfig } from "../brand.config";

export const neutral = brandConfig.neutral;

export const font = {
  sans: brandConfig.fonts.sansFamily,
  mono: brandConfig.fonts.monoFamily,
} as const;

export const brandEase = Easing.bezier(...brandConfig.motion.easeBezier);

export const FPS = 30;
export const sec = (s: number) => Math.round(s * FPS);