# frozen_string_literal: true

require "bibtex"

module Gundelsby
  # Makes the BibTeX bibliography the single source for publication metadata.
  # Identity and profile links remain in _data/publications.yml.
  class PublicationsFromBibtex < Jekyll::Generator
    safe true
    priority :highest

    def generate(site)
      publications = site.data.fetch("publications")
      identity = publications.fetch("identity")
      bibliography_path = site.in_source_dir("_bibliography", "papers.bib")

      bibliography = BibTeX.open(bibliography_path)
      publications["works"] = bibliography.entries.values.map do |entry|
        publication_from(entry, identity)
      end
    rescue KeyError, Errno::ENOENT, BibTeX::ParseError => error
      raise Jekyll::Errors::FatalException, "Unable to build publication metadata: #{error.message}"
    end

    private

    def publication_from(entry, identity)
      {
        "key" => entry.key,
        "entry_type" => entry.type.to_s,
        "year" => entry.fetch(:year).to_s.to_i,
        "title" => entry.fetch(:title).to_s,
        "doi" => entry.fetch(:doi).to_s,
        "venue" => venue_for(entry),
        "pages" => optional_value(entry, :pages),
        "authors" => authors_for(entry, identity)
      }.compact
    end

    def venue_for(entry)
      optional_value(entry, :booktitle) || optional_value(entry, :journal)
    end

    def authors_for(entry, identity)
      entry.fetch(:author).map do |name|
        author = { "name" => name.to_s }
        author["orcid"] = true if profile_author?(name, identity)
        author
      end
    end

    def profile_author?(name, identity)
      normalize(name.first) == normalize(identity.fetch("given_name")) &&
        normalize(name.last) == normalize(identity.fetch("family_name"))
    end

    def optional_value(entry, field)
      entry[field]&.to_s&.then { |value| value unless value.empty? }
    end

    def normalize(value)
      value.to_s.unicode_normalize(:nfkc).downcase.strip
    end
  end
end
