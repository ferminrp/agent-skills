/**
 * Fill this file per project. Components import only from here for brand-specific values.
 */
export const brandConfig = {
  neutral: {
    50: "#fafafa",
    100: "#f4f4f5",
    200: "#e4e4e7",
    300: "#d4d4d8",
    400: "#a1a1aa",
    500: "#71717a",
    600: "#52525b",
    700: "#3f3f46",
    800: "#27272a",
    900: "#18181b",
    950: "#09090b",
  },
  fonts: {
    sansFamily: "system-ui, -apple-system, sans-serif",
    monoFamily: "ui-monospace, 'Cascadia Code', monospace",
    faces: [] as Array<{ family: string; file: string; weight: string }>,
  },
  logos: {
    icon: {
      lightInk: "brand/logo-icon-light.svg",
      darkInk: "brand/logo-icon-dark.svg",
    },
    lockup: {
      lightInk: "brand/logo-lockup-light.svg",
      darkInk: "brand/logo-lockup-dark.svg",
    },
  },
  motion: {
    easeBezier: [0.22, 1, 0.36, 1] as [number, number, number, number],
  },
  product: {
    name: "Example product",
    defaultAppHost: "app.example.com",
    closingLine: "Built for teams who ship.",
    websiteUrl: "https://example.com",
  },
  copy: {
    locale: "en-US",
    toneRules: [
      "Lead with outcomes, not button labels.",
      "One short body sentence per scene.",
      "No hype adjectives unless brand docs allow them.",
    ],
    demoDataPrefix: "video-demo-",
  },
} as const;

export type BrandConfig = typeof brandConfig;