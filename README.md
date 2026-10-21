# SEEDS Lab

Website for SEEDS Lab at China University of Petroleum (East China).

Production address: **[yongzanliu.github.io/seeds](https://yongzanliu.github.io/seeds/)**

## Local preview

Use Ruby 3.3 and Bundler, then run:

```sh
bundle install
bundle exec jekyll serve --livereload
```

Open `http://127.0.0.1:4000/`. All website content and media are contained in this
repository; files under `_tools/` document how selected research visuals were made.

## Production build

```sh
JEKYLL_ENV=production bundle exec jekyll build --config _config.yaml,_config.production.yaml
python3 _tools/deployment/verify_site.py --site _site --baseurl /seeds
```

The production configuration applies the `/seeds` project path. The verifier
checks local page, image, script, stylesheet, and anchor references. Template
example people/posts and development files are excluded from published output.
Generated files in `_site/` are not committed.

## GitHub Pages deployment

1. In this repository's **Settings → Pages → Build and deployment**, select
   **GitHub Actions** as the source.
2. Commit the website source and push `main` to `YongzanLiu/seeds`.
3. Follow **Actions → Deploy SEEDS Lab website**. The workflow builds and verifies
   the website, then publishes it to GitHub Pages.
4. Check the homepage, research pages, team, publications, software animations,
   news, and contact links at the production address.

Later pushes to `main` deploy automatically. Pull requests build and validate
without publishing. The workflow can also be run manually.

Publication and team content is maintained in `_data/`. News updates are shared
between the homepage and News page; see [_tools/news/README.md](_tools/news/README.md).
The previous template automation is archived in `_tools/deployment/legacy-workflows/`
and is inactive.

Built with [Lab Website Template](https://github.com/greenelab/lab-website-template).
