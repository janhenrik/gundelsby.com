# gundelsby.com

This repository contains the source for Jan Henrik's personal website. The site is built with [Jekyll](https://jekyllrb.com/) using the [cvless](https://github.com/piazzai/cvless) theme.

The site exposes [schema.org](https://schema.org) `Person` metadata to help search engines and chatbots better understand its content.

## Local development with Docker

1. Ensure [Docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/) are installed.
2. Start the development container:

```sh
docker-compose up
```

The site will be available at [http://localhost:4000](http://localhost:4000).

You can also run the container directly on Linux/macOS:

```sh
docker run -p 4000:4000 -v $(pwd):/site bretfisher/jekyll-serve
```

## Running without Docker

If you prefer running Jekyll locally, install Ruby and Bundler, then:

```sh
bundle install
bundle exec jekyll serve
```

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

## Credits

Based on [cvless](https://github.com/piazzai/cvless).
