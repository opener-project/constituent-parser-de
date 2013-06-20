require File.expand_path(
  '../lib/opener/constituent_parsers/de/version',
  __FILE__
)

generated = Dir.glob('core/site-packages/pre_build/**/*')

Gem::Specification.new do |gem|
  gem.name        = 'opener-constituent-parser-de'
  gem.version     = Opener::ConstituentParsers::DE::VERSION
  gem.authors     = ['development@olery.com']
  gem.summary     = 'Constituent parser for the German language'
  gem.description = gem.summary
  gem.has_rdoc    = 'yard'

  gem.required_ruby_version = '>= 1.9.2'

  gem.files       = (`git ls-files`.split("\n") + generated).sort
  gem.executables = gem.files.grep(%r{^bin/}).map{ |f| File.basename(f) }
  gem.test_files  = gem.files.grep(%r{^(test|spec|features)/})

  gem.add_dependency 'opener-build-tools'

  gem.add_development_dependency 'rspec'
  gem.add_development_dependency 'cucumber'
  gem.add_development_dependency 'rake'
end
