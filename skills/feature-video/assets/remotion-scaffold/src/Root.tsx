import { Composition } from "remotion";
import { EXAMPLE_DURATION, ExampleFeature } from "./example/ExampleFeature";
import { FPS } from "./brand/tokens";

export function RemotionRoot() {
  return (
    <>
      <Composition
        id="ExampleFeature"
        component={ExampleFeature}
        durationInFrames={EXAMPLE_DURATION}
        fps={FPS}
        width={1920}
        height={1080}
      />
    </>
  );
}