require 'bundler/gem_tasks'
require 'rake/clean'

##
# Stanford Configuration.
#
# These settings are used for downloading a local copy of the Stanford parser.
# This parser is packaged in the Gem upon building it.

# Path to the directory containing the Stanford parser files.
STANFORD_DIRECTORY = File.expand_path(
  '../core/vendor/stanford-parser',
  __FILE__
)

# Name of the Stanford zip archive.
STANFORD_ARCHIVE = 'stanford-parser-2013-04-05.zip'

# URL to the zip archive of the Stanford parser.
STANFORD_ARCHIVE_URL = "https://s3-eu-west-1.amazonaws.com/opener/stanford/#{STANFORD_ARCHIVE}"

# The names of the JAR files to copy over to vendor/core/stanford-parser.
STANFORD_JAR_NAMES = [
  'stanford-parser.jar',
  'stanford-parser-2.0.5-models.jar'
]

CLEAN.include(
  'tmp/*',
  'pkg',
  '**/*.pyo',
  '**/*.pyc',
  File.join(STANFORD_DIRECTORY, '*'),
  'core/site-packages/pre_build',
  'core/site-packages/pre_install'
)

Dir.glob(File.expand_path('../task/*.rake', __FILE__)) do |task|
  import(task)
end

task :default => :test
