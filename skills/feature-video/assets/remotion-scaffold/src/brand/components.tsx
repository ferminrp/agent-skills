import type { CSSProperties, ReactNode } from "react";
import { AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { brandConfig } from "../brand.config";
import { enter, keyframes, type Key } from "./motion";
import { font, neutral } from "./tokens";

export function BrandBackground({ tone = "light" }: { tone?: "light" | "dark" }) {
  return (
    <AbsoluteFill style={{ background: tone === "dark" ? neutral[950] : neutral[100] }}>
      <Grain opacity={tone === "dark" ? 0.09 : 0.05} />
    </AbsoluteFill>
  );
}

export function Grain({ opacity = 0.06 }: { opacity?: number }) {
  return (
    <AbsoluteFill style={{ opacity, mixBlendMode: "overlay", pointerEvents: "none" }}>
      <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
        <filter id="brand-grain">
          <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" stitchTiles="stitch" />
          <feColorMatrix type="saturate" values="0" />
        </filter>
        <rect width="100%" height="100%" filter="url(#brand-grain)" />
      </svg>
    </AbsoluteFill>
  );
}

export function Scene({ children, fadeOut = true }: { children: ReactNode; fadeOut?: boolean }) {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const inP = enter(frame, 0, 20);
  const outP = fadeOut
    ? interpolate(frame, [durationInFrames - 14, durationInFrames], [1, 0], {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      })
    : 1;
  return <AbsoluteFill style={{ opacity: inP * outP }}>{children}</AbsoluteFill>;
}

export function MonoLabel({ children, color = neutral[500], style }: { children: ReactNode; color?: string; style?: CSSProperties }) {
  return (
    <div
      style={{
        fontFamily: font.mono,
        fontSize: 18,
        letterSpacing: "0.18em",
        textTransform: "uppercase",
        color,
        ...style,
      }}
    >
      {children}
    </div>
  );
}

export function Caption({
  step,
  title,
  body,
  at = 6,
  width = 440,
}: {
  step: string;
  title: string;
  body?: string;
  at?: number;
  width?: number;
}) {
  const frame = useCurrentFrame();
  const rise = (delay: number) => {
    const p = enter(frame, at + delay, 26);
    return { opacity: p, transform: `translateY(${(1 - p) * 18}px)` };
  };
  return (
    <div style={{ width, display: "flex", flexDirection: "column", gap: 28 }}>
      <div style={rise(0)}>
        <MonoLabel>{step}</MonoLabel>
      </div>
      <div
        style={{
          ...rise(4),
          fontFamily: font.sans,
          fontWeight: 500,
          fontSize: 60,
          lineHeight: 0.98,
          letterSpacing: "-0.055em",
          color: neutral[950],
        }}
      >
        {title}
      </div>
      {body ? (
        <div
          style={{
            ...rise(10),
            fontFamily: font.sans,
            fontSize: 26,
            lineHeight: 1.45,
            color: neutral[600],
            maxWidth: width,
          }}
        >
          {body}
        </div>
      ) : null}
    </div>
  );
}

export function ProductLayout({ caption, children }: { caption: ReactNode; children: ReactNode }) {
  return (
    <AbsoluteFill style={{ flexDirection: "row", alignItems: "center", padding: "0 72px", gap: 64 }}>
      <div style={{ flexShrink: 0 }}>{caption}</div>
      <div style={{ flex: 1, display: "flex", justifyContent: "flex-end", alignItems: "center", height: "100%" }}>
        {children}
      </div>
    </AbsoluteFill>
  );
}

export const BROWSER_BAR = 44;

export function BrowserFrame({ url, width, height, children }: { url: string; width: number; height: number; children: ReactNode }) {
  return (
    <div
      style={{
        width,
        height: height + BROWSER_BAR,
        borderRadius: 14,
        overflow: "hidden",
        background: "#ffffff",
        boxShadow: `0 0 0 1px rgba(9,9,11,0.08), 0 30px 80px -20px rgba(24,24,27,0.28), 0 12px 24px -12px rgba(24,24,27,0.18)`,
        display: "flex",
        flexDirection: "column",
      }}
    >
      <div
        style={{
          height: BROWSER_BAR,
          background: neutral[100],
          borderBottom: `1px solid ${neutral[200]}`,
          display: "flex",
          alignItems: "center",
          padding: "0 16px",
          gap: 8,
          flexShrink: 0,
        }}
      >
        {[0, 1, 2].map((i) => (
          <div key={i} style={{ width: 11, height: 11, borderRadius: 99, background: neutral[300] }} />
        ))}
        <div
          style={{
            margin: "0 auto",
            height: 26,
            minWidth: 360,
            borderRadius: 8,
            background: neutral[50],
            border: `1px solid ${neutral[200]}`,
            fontFamily: font.sans,
            fontSize: 14,
            color: neutral[500],
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            padding: "0 16px",
          }}
        >
          {url}
        </div>
        <div style={{ width: 49 }} />
      </div>
      <div style={{ position: "relative", width, height, overflow: "hidden" }}>{children}</div>
    </div>
  );
}

export function PhoneFrame({ width, height, children }: { width: number; height: number; children: ReactNode }) {
  const bezel = 12;
  return (
    <div
      style={{
        width: width + bezel * 2,
        height: height + bezel * 2,
        borderRadius: 52,
        background: neutral[900],
        padding: bezel,
        boxShadow: `0 30px 80px -20px rgba(24,24,27,0.35), 0 0 0 1px ${neutral[700]} inset`,
      }}
    >
      <div style={{ position: "relative", width, height, borderRadius: 40, overflow: "hidden", background: neutral[50] }}>
        {children}
      </div>
    </div>
  );
}

export type ScreenImage = { src: string; from: number; fade?: number };
export type CursorKey = { f: number; x: number; y: number; click?: boolean };
export type CameraKey = { f: number; scale: number; x: number; y: number };

export function Screen({
  images,
  width,
  baseWidth = 1440,
  baseHeight = 900,
  cursor,
  camera,
  scrollY,
  overlay,
}: {
  images: ScreenImage[];
  width: number;
  baseWidth?: number;
  baseHeight?: number;
  cursor?: CursorKey[];
  camera?: CameraKey[];
  scrollY?: Key[];
  overlay?: (k: number) => ReactNode;
}) {
  const frame = useCurrentFrame();
  const k = width / baseWidth;

  const cam = camera?.length
    ? {
        scale: keyframes(frame, camera.map((c) => ({ f: c.f, v: c.scale }))),
        x: keyframes(frame, camera.map((c) => ({ f: c.f, v: c.x }))),
        y: keyframes(frame, camera.map((c) => ({ f: c.f, v: c.y }))),
      }
    : { scale: 1, x: baseWidth / 2, y: baseHeight / 2 };

  const W = baseWidth * k;
  const H = baseHeight * k;
  const clampX = Math.min(0, Math.max(W * (1 - cam.scale), W / 2 - cam.x * k * cam.scale));
  const clampY = Math.min(0, Math.max(H * (1 - cam.scale), H / 2 - cam.y * k * cam.scale));

  const sy = scrollY ? keyframes(frame, scrollY) : 0;

  return (
    <div style={{ position: "absolute", inset: 0, overflow: "hidden" }}>
      <div
        style={{
          position: "absolute",
          left: 0,
          top: 0,
          width: baseWidth * k,
          height: baseHeight * k,
          transformOrigin: "0 0",
          transform: `translate(${clampX}px, ${clampY}px) scale(${cam.scale})`,
        }}
      >
        <div style={{ position: "absolute", inset: 0, transform: `translateY(${-sy * k}px)` }}>
          {images.map((img, i) => {
            const fade = img.fade ?? 10;
            const opacity =
              i === 0
                ? 1
                : interpolate(frame, [img.from, img.from + fade], [0, 1], {
                    extrapolateLeft: "clamp",
                    extrapolateRight: "clamp",
                  });
            if (frame < img.from && i !== 0) return null;
            return (
              <Img
                key={img.src}
                src={staticFile(img.src)}
                style={{ position: "absolute", left: 0, top: 0, width: baseWidth * k, opacity }}
              />
            );
          })}
        </div>
        {overlay ? overlay(k) : null}
        {cursor?.length ? <Cursor keys={cursor} k={k} /> : null}
      </div>
    </div>
  );
}

export function Cursor({ keys, k }: { keys: CursorKey[]; k: number }) {
  const frame = useCurrentFrame();
  const x = keyframes(frame, keys.map((c) => ({ f: c.f, v: c.x })));
  const y = keyframes(frame, keys.map((c) => ({ f: c.f, v: c.y })));
  const appear = enter(frame, keys[0].f - 8, 10);
  let press = 0;
  let ring = 0;
  for (const c of keys) {
    if (!c.click) continue;
    const d = frame - c.f;
    if (d >= 0 && d < 8) press = Math.max(press, 1 - Math.abs(d - 3) / 4);
    if (d >= 0 && d < 18) ring = Math.max(ring, d / 18);
  }
  const s = 1 - press * 0.14;
  return (
    <div style={{ position: "absolute", left: x * k, top: y * k, opacity: appear, pointerEvents: "none" }}>
      {ring > 0 ? (
        <div
          style={{
            position: "absolute",
            left: -26,
            top: -26,
            width: 52,
            height: 52,
            borderRadius: 99,
            border: `2px solid ${neutral[900]}`,
            opacity: (1 - ring) * 0.5,
            transform: `scale(${0.4 + ring * 0.8})`,
          }}
        />
      ) : null}
      <svg
        width={26}
        height={26}
        viewBox="0 0 24 24"
        style={{
          transform: `translate(-3px,-2px) scale(${s})`,
          transformOrigin: "3px 2px",
          filter: "drop-shadow(0 2px 3px rgba(9,9,11,0.35))",
        }}
      >
        <path
          d="M4 2.5 L4 19.5 L8.6 15.3 L11.6 22 L14.6 20.6 L11.7 14.1 L18 14.1 Z"
          fill={neutral[950]}
          stroke="#ffffff"
          strokeWidth={1.4}
          strokeLinejoin="round"
        />
      </svg>
    </div>
  );
}

export function BrandLogo({
  variant,
  ink,
  height,
}: {
  variant: "icon" | "lockup";
  ink: "light" | "dark";
  height: number;
}) {
  const paths = variant === "icon" ? brandConfig.logos.icon : brandConfig.logos.lockup;
  const src = ink === "light" ? paths.lightInk : paths.darkInk;
  return <Img src={staticFile(src)} style={{ height, width: "auto" }} alt="" />;
}

export const APP_W = 1272;
export const APP_H = Math.round((APP_W * 900) / 1440);

export function AppShot(props: Omit<Parameters<typeof Screen>[0], "width"> & { url?: string; width?: number }) {
  const { url = brandConfig.product.defaultAppHost, width = APP_W, ...rest } = props;
  const height = Math.round((width * (rest.baseHeight ?? 900)) / (rest.baseWidth ?? 1440));
  return (
    <BrowserFrame url={url} width={width} height={height}>
      <Screen {...rest} width={width} />
    </BrowserFrame>
  );
}