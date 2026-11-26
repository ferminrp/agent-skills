import { AbsoluteFill, Series, useCurrentFrame } from "remotion";
import { brandConfig } from "../brand.config";
import {
  AppShot,
  BrandBackground,
  BrandLogo,
  Caption,
  MonoLabel,
  ProductLayout,
  Scene,
} from "../brand/components";
import { loadBrandFonts } from "../brand/fonts";
import { enter } from "../brand/motion";
import { font, neutral } from "../brand/tokens";

const img = (name: string) => `example/${name}.jpg`;

export const EXAMPLE_SCENES = {
  intro: 90,
  step: 120,
  outro: 90,
} as const;

export const EXAMPLE_DURATION = Object.values(EXAMPLE_SCENES).reduce((a, b) => a + b, 0);

export function ExampleFeature() {
  loadBrandFonts();
  const s = EXAMPLE_SCENES;
  return (
    <AbsoluteFill style={{ background: neutral[100], fontFamily: font.sans }}>
      <Series>
        <Series.Sequence durationInFrames={s.intro}>
          <Intro />
        </Series.Sequence>
        <Series.Sequence durationInFrames={s.step}>
          <ProductStep />
        </Series.Sequence>
        <Series.Sequence durationInFrames={s.outro}>
          <Outro />
        </Series.Sequence>
      </Series>
    </AbsoluteFill>
  );
}

function Intro() {
  const frame = useCurrentFrame();
  const p = (d: number) => {
    const v = enter(frame, d, 30);
    return { opacity: v, transform: `translateY(${(1 - v) * 24}px)` };
  };
  return (
    <Scene>
      <BrandBackground tone="dark" />
      <AbsoluteFill style={{ padding: 96, justifyContent: "space-between" }}>
        <div style={p(0)}>
          <BrandLogo variant="lockup" ink="light" height={44} />
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: 36 }}>
          <div style={p(8)}>
            <MonoLabel color={neutral[400]}>{brandConfig.product.name} · Feature demo</MonoLabel>
          </div>
          <div
            style={{
              ...p(14),
              color: neutral[50],
              fontWeight: 500,
              fontSize: 96,
              lineHeight: 0.95,
              letterSpacing: "-0.06em",
              maxWidth: 1400,
            }}
          >
            Show what the product actually does.
          </div>
        </div>
      </AbsoluteFill>
    </Scene>
  );
}

function ProductStep() {
  return (
    <Scene>
      <BrandBackground />
      <ProductLayout
        caption={
          <Caption
            step="01 · Publish"
            title="Ship the update in one flow."
            body="Walk through the real UI with demo data—no mocked screens."
          />
        }
      >
        <AppShot
          url={brandConfig.product.defaultAppHost}
          images={[
            { src: img("screen-empty"), from: 0 },
            { src: img("screen-filled"), from: 45, fade: 8 },
          ]}
          cursor={[
            { f: 12, x: 520, y: 380 },
            { f: 44, x: 680, y: 520, click: true },
          ]}
          camera={[
            { f: 0, scale: 1, x: 720, y: 450 },
            { f: 90, scale: 1.25, x: 680, y: 480 },
          ]}
        />
      </ProductLayout>
    </Scene>
  );
}

function Outro() {
  const frame = useCurrentFrame();
  const p = enter(frame, 10, 28);
  return (
    <Scene>
      <BrandBackground tone="dark" />
      <AbsoluteFill
        style={{
          alignItems: "center",
          justifyContent: "center",
          flexDirection: "column",
          gap: 32,
          opacity: p,
        }}
      >
        <BrandLogo variant="lockup" ink="light" height={52} />
        <div style={{ color: neutral[300], fontSize: 28, fontFamily: font.sans }}>{brandConfig.product.closingLine}</div>
        <MonoLabel color={neutral[500]}>{brandConfig.product.websiteUrl.replace(/^https?:\/\//, "")}</MonoLabel>
      </AbsoluteFill>
    </Scene>
  );
}