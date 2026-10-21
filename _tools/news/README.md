# News updates

Edit `_data/news.json` to update both the News page and the homepage.
Each entry has:

- `date`: announcement date in `YYYY-MM-DD` format (quoted string).
- `year`: the same four-digit year, used to group the News page.
- `text`: a short, plain-text announcement.
- `featured`: `true` to consider it for the homepage, or `false` for the News page only.
- `url` (optional): a related paper, project, or activity, using either an absolute HTTPS URL or a site-relative path.

The homepage shows the two most recent featured entries, sorted by date.
It displays a single entry when only one is featured, and hides the whole
Latest News block when none are featured. Entries with the same date retain
the reverse of their source order after sorting; use distinct dates when order matters.
The News page keeps every entry, grouped by year and sorted newest first.

Changes appear after Jekyll rebuilds the site and the updated site is deployed.
No duplicate homepage editing or external news service is needed.
