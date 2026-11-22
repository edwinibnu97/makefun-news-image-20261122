// News-image entry for make.fun (news-image-20261122). The image is baked into
// this repository as entry.png — rendered by generate.py (Pillow, no network,
// deterministic) — and this program copies it to /output/entry.png.
// Standard library only, no network: the same bytes come out on every run.
//
// Local run:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
copyFileSync(new URL("./entry.png", import.meta.url), join(outDir, "entry.png"));
