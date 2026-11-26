import { continueRender, delayRender, staticFile } from "remotion";
import { brandConfig } from "../brand.config";

let loaded = false;

export function loadBrandFonts() {
  if (loaded || typeof document === "undefined") return;
  const faces = brandConfig.fonts.faces;
  if (faces.length === 0) {
    loaded = true;
    return;
  }
  loaded = true;
  const handle = delayRender("Loading brand fonts");
  Promise.all(
    faces.map((f) => {
      const face = new FontFace(f.family, `url(${staticFile(f.file)})`, { weight: f.weight });
      return face.load().then((ff) => (document.fonts as unknown as { add: (f: FontFace) => void }).add(ff));
    }),
  )
    .then(() => continueRender(handle))
    .catch((err) => {
      console.error(err);
      continueRender(handle);
    });
}