// QA: contact sheet (one frame every N seconds) from a rendered MP4.
// Usage: node scripts/contact-sheet.mjs out/example.mp4 [everySeconds=3]
import { execFileSync } from "node:child_process";
const [, , input, every = "3"] = process.argv;
if (!input) {
  console.error("Usage: node scripts/contact-sheet.mjs <video.mp4> [everySeconds]");
  process.exit(1);
}
const output = input.replace(/\.mp4$/, "-contact.png");
execFileSync("ffmpeg", [
  "-loglevel",
  "error",
  "-y",
  "-i",
  input,
  "-vf",
  `fps=1/${every},scale=640:-1,tile=4x6:padding=8:color=white`,
  "-frames:v",
  "1",
  output,
]);
console.log(output);