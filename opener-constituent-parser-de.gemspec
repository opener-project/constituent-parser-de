require File.expand_path(
  '../lib/opener/constituent_parsers/de/version',
  __FILE__
)

Gem::Specification.new do |gem|
  gem.name        = 'opener-constituent-parser-de'
  gem.version     = Opener::ConstituentParsers::DE::VERSION
  gem.authors     = ['development@olery.com']
  gem.summary     = 'Constituent parser for the German language'
  gem.description = gem.summary
  gem.has_rdoc    = 'yard'

  gem.required_ruby_version = '>= 1.9.2'

  gem.files = Dir.glob([
    'core/site-packages/pre_build/**/*',
    'core/vendor/**/*',
    'core/*.py',
    'ext/**/*',
    'lib/**/*',
    '*.gemspec',
    '*_requirements.txt',
    'README.md'
  ]).select { |f| File.file?(f) }

  gem.executables = Dir.glob('bin/*').map { |f| File.basename(f) }

  gem.add_dependency 'opener-build-tools', ['>= 0.2.7']

  gem.add_development_dependency 'rspec'
  gem.add_development_dependency 'cucumber'
  gem.add_development_dependency 'rake'
end
