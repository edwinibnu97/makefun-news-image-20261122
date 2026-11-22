# makefun-news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/edwinibnu97/makefun-news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/edwinibnu97/makefun-news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

One image that sums up the world's news of Sunday 22 November 2026, drawn
as a newspaper front page for
[news-image-20261122](https://make.fun/bounty/news-image-20261122): NATO
rallies behind Poland after Russian missiles hit its soil, Mexican forces
capture cartel kingpin "El Chapo Isidro" as 11 are killed in the backlash,
the EU and Indonesia sign a mega trade deal after a decade of talks, drones
hit a Russian cargo ship in the Baltic, and Iran strikes spread across the
Gulf — plus COP31, the Japan–India training pact, trilateral peace talks in
Abu Dhabi, and TikTok's deepfake-detection tool.

`generate.py` draws the page with Pillow (no network, no randomness, no
clock), and `main.ts` copies the resulting `entry.png` to `/output/entry.png`.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

To draw the image again from scratch (needs Pillow):

```sh
python3 generate.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=q17yfxs8&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
