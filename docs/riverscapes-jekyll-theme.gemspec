# frozen_string_literal: true

Gem::Specification.new do |spec|
  spec.name          = "riverscapes-jekyll-theme"
  spec.version       = "0.1.0"
  spec.authors       = ["Matt Reimer"]
  spec.email         = ["matt.reimer@gmail.com"]

  spec.summary       = "Write a short summary, because Rubygems requires one."
  spec.homepage      = "http://riverscapes.xyz"
  spec.license       = "MIT"

  spec.files         = `git ls-files -z`.split("\x0").select { |f| f.match(%r!^(assets|_layouts|_includes|_sass|LICENSE|README)!i) }

  spec.add_runtime_dependency "jekyll", ">= 3.8"

  spec.add_development_dependency "bundler"
end
