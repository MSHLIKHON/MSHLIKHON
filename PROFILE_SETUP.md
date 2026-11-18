# Animated profile maintenance

Adapted from [DevVerse](https://github.com/Muhtasim-Masum-Hasnayen/devverse-profile), with its license and visible author attribution preserved.

Edit `config.yml` for identity, theme, skills and social links. Run `npm run build` to preview locally. Custom project and community sections live in `scripts/generate.js`.

The **Refresh animated profile** workflow runs daily at 00:17 Asia/Dhaka and can also be run manually. It generates the README, SVG animations, contribution snake and 3D graph. These use the repository-scoped `GITHUB_TOKEN`; no personal token or additional secret is required.

The activity graph is provided by a third-party public service. Core animated visuals are stored in this repository. Original profile content remains available in Git history.
