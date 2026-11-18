# Likhon's personal GitHub profile

Original artwork and generator created specifically for MD Shyed Hasan Likhon.

## Edit and rebuild

Edit `profile.json` for identity, links and project descriptions. The other biographical
sections and the visual design live in `scripts/build_profile.py`.

```sh
python3 scripts/build_profile.py
```

Python 3.9 or newer is sufficient; no packages, remote fonts, external image services,
or Node.js installation are needed. All artwork and contribution graphics are local
SVG files. The README uses standard GitHub Markdown and HTML.

## Daily updates

The **Refresh personal profile** workflow runs daily at 00:17 Asia/Dhaka (GitHub may
delay scheduled runs), when its configuration changes, or manually from Actions.
It reads public project metadata and the GitHub contribution calendar using the
repository's existing `GITHUB_TOKEN`. It then redraws the activity calendar and
isometric terrain and commits any changes. No personal access token is needed.

To refresh locally, set `GITHUB_TOKEN` in your shell without saving it to a file,
then run `python3 scripts/build_profile.py --refresh`.

Activity counts cover the date range printed on the calendar. The language list
is based on bytes in owned, non-fork public repositories; it is not a skill ranking.
All-time contributions and private repository details are not requested.

## Design

Graphite, warm white, mint and periwinkle; an original ML monogram; four linked
nodes representing learn, build, connect and impact. Project glyphs represent
navigation, a bridge, progress steps and Conway's cellular automaton.

Animations use CSS, contain no scripts or network requests, leave all essential
content readable in the first frame and respect reduced-motion preferences.
Git history preserves the earlier profile versions.
