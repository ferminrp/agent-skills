// Shared Playwright helpers for real UI capture (see feature-video skill).
import { chromium, devices } from "playwright";
import { execFileSync } from "node:child_process";
import { mkdirSync, readdirSync, unlinkSync } from "node:fs";
import { join } from "node:path";
import { loginAuthenticated } from "./login.mjs";

export const DESKTOP = { viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 };
export const MOBILE = devices["iPhone 14"];

/** Authenticated app session — implement `login.mjs` for your product. */
export async function openAuthenticated(ctxOpts = {}) {
  return loginAuthenticated({ ...DESKTOP, colorScheme: "light", permissions: ["clipboard-read", "clipboard-write"], ...ctxOpts });
}

/** Browser without a session (public forms, marketing pages). */
export async function openPublic(opts = DESKTOP, locale = "en-US") {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ colorScheme: "light", locale, ...opts });
  return { browser, ctx, page: await ctx.newPage() };
}

export function scrollTo(loc, offset = 24) {
  return loc.first().evaluate((el, off) => {
    let p = el.parentElement;
    while (p && !(p.scrollHeight > p.clientHeight + 4 && /(auto|scroll)/.test(getComputedStyle(p).overflowY))) p = p.parentElement;
    const elTop = el.getBoundingClientRect().top;
    if (!p) {
      const root = document.scrollingElement ?? document.documentElement;
      root.scrollTop += elTop - off;
      return;
    }
    const containerTop = p.getBoundingClientRect().top;
    p.scrollTop = elTop - containerTop + p.scrollTop - off;
  }, offset);
}

export async function box(loc) {
  const b = await loc
    .first()
    .boundingBox({ timeout: 5000 })
    .catch(() => null);
  return (
    b && {
      x: Math.round(b.x),
      y: Math.round(b.y),
      w: Math.round(b.width),
      h: Math.round(b.height),
      cx: Math.round(b.x + b.width / 2),
      cy: Math.round(b.y + b.height / 2),
    }
  );
}

export function ensureDir(dir) {
  mkdirSync(dir, { recursive: true });
  return dir;
}

export function pngsToJpg(srcDir, destDir) {
  ensureDir(destDir);
  for (const f of readdirSync(srcDir).filter((n) => n.endsWith(".png"))) {
    const dest = join(destDir, f.replace(/\.png$/, ".jpg"));
    execFileSync("ffmpeg", ["-loglevel", "error", "-y", "-i", join(srcDir, f), "-q:v", "2", "-pix_fmt", "yuvj444p", dest]);
  }
}

export function cleanPngs(dir) {
  for (const f of readdirSync(dir).filter((n) => n.endsWith(".png"))) unlinkSync(join(dir, f));
}