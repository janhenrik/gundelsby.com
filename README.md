# gundelsby.com (al-folio experiment)

Source for Jan Henrik Gundelsby's personal website, built with [Jekyll](https://jekyllrb.com/) and the
[al-folio](https://github.com/alshedivat/al-folio) v1.2 starter (runtime layouts come from the `al_folio_core`
and related gems, see `Gemfile`).

## Where the content lives

- `_pages/about.md` – home page (bio bullets, profile photo `assets/img/profile.jpg` with the octocat `assets/img/octocat.png` in front)
- `_data/socials.yml` – social icons on the home page
- `_bibliography/papers.bib` – publications rendered by jekyll-scholar on `/publications/`
- `_data/publications.yml` – the same papers as structured data for the schema.org JSON-LD on `/publications/`
- `_data/talks.yml` – talks rendered on `/talks/`
- `_data/cv.yml` – CV (RenderCV format) rendered on `/cv/` by `al_folio_cv`

## Profile metadata

When the role or focus changes, update all of: `_pages/about.md`, `_data/cv.yml`, `_config.yml`
(`description`, `keywords`, `seo.*`), `llms.txt` (`llms-full.txt` is generated automatically from `_data/*.yml`),
`_includes/schema-person.html`, and the `identity` block in `_data/publications.yml`.

## Local overrides of theme files

`_includes/head.liquid` shadows the gem's head include to add favicons, agent-discovery `<link>`
relations, and the schema.org JSON-LD includes. Check for upstream drift with
`bundle exec al-folio upgrade overrides audit`.

## Local preview with Docker

```sh
docker run -d --name gundelsby-alfolio -p 4000:4000 \
  -v "$PWD":/site -w /site -v gundelsby-alfolio-bundle:/usr/local/bundle ruby:3.3 \
  bash -c 'apt-get update -qq && apt-get install -y -qq nodejs >/dev/null && bundle install -j4 && \
           bundle exec jekyll serve --host 0.0.0.0 --port 4000 --force_polling --destination /tmp/_site'
```

`ruby:3.3` already ships ImageMagick (needed for responsive WebP images); Node.js is needed by
`jekyll-terser`.

## Deployment

Pushing to `main` triggers `.github/workflows/main.yml`, which builds the site and uploads `_site` to Bunny.net.

## License

MIT, see [LICENSE](LICENSE). Theme: al-folio (MIT).
