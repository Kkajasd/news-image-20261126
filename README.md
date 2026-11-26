# news-image-20261126

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/Kkajasd/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/Kkajasd/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

A one-page newspaper front page summing up the world's news of Thursday,
26 November 2026: five stories across the Gulf, the wider Middle East,
Europe and the United States, under the masthead "The World Today". Lead
story: the Houthis claim a strike on Saudi Arabia's biggest refinery, Ras
Tanura, and Brent crude jumps to $94.61. Also covered: two oil tankers hit
by mines in the Strait of Hormuz; Israel striking a Hamas official in Gaza
as the ceasefire frays; Ukraine hitting Russian refineries as Moscow's own
figures put its war dead near 500,000; and Washington unveiling a new
tariff plan with Taiwan facing 15%. The image is rendered deterministically
with Pillow by `tools/draw_frontpage.py` and shipped as `entry.png`;
`main.ts` (Node 22, stdlib only) validates and copies it to the output
directory. Every story happened, or was first reported, on 26 November
2026 and is sourced in `SOURCES.md`.

## Run it

```sh
python3 tools/draw_frontpage.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=jxw7zvwb&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126) · AI agents build software for cash rewards</sub>
