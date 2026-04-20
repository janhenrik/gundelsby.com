# Emits a .md companion next to every markdown-sourced page so a Bunny
# CDN Edge Rule can serve it when the request has Accept: text/markdown.

module Jekyll
  module MarkdownForAgents
    MARKDOWN_EXTS = %w[.md .markdown].freeze
    FRONT_MATTER = /\A---\s*\n.*?\n---\s*\n/m

    Hooks.register :pages, :post_init do |page|
      next unless MARKDOWN_EXTS.include?(File.extname(page.path))
      source_path = File.join(page.site.source, page.relative_path)
      raw = File.read(source_path, encoding: "UTF-8")
      raw = raw.sub(FRONT_MATTER, "") if raw.match?(FRONT_MATTER)
      page.data["_markdown_source"] = raw
    end

    Hooks.register :site, :post_write do |site|
      liquid_config = site.config["liquid"] || {}

      site.pages.each do |page|
        source = page.data["_markdown_source"]
        next unless source
        dest = page.destination(site.dest)
        next unless dest.end_with?(".html")

        info = {
          registers: { site: site, page: page.to_liquid },
          filters: [Jekyll::Filters],
          strict_filters: liquid_config["strict_filters"],
          strict_variables: liquid_config["strict_variables"]
        }

        template = site.liquid_renderer.file(page.relative_path).parse(source)
        rendered = template.render!(site.site_payload, info).strip + "\n"

        md_dest = dest.sub(/\.html\z/, ".md")
        File.write(md_dest, rendered)
      end
    end
  end
end
