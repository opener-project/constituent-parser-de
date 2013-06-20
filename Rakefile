require 'bundler/gem_tasks'
require 'opener/build-tools/tasks/python'
require 'opener/build-tools/tasks/clean'

require_relative 'ext/hack/support'

desc 'Lists all the files of the Gemspec'
task :files do
  gemspec = Gem::Specification.load('opener-constituent-parser-de.gemspec')

  puts gemspec.files.sort
end

desc 'Verifies the requirements'
task :requirements do
  verify_requirements

  require_executable('curl')
  require_executable('unzip')
end

desc 'Cleans up the repository'
task :clean => [
  'python:clean:bytecode',
  'python:clean:packages',
  'clean:tmp',
  'clean:gems'
]

desc 'Installs the Stanford parser JAR archives'
task :stanford do
  zipname   = File.join(TMP_DIRECTORY, STANFORD_ARCHIVE)
  directory = File.join(TMP_DIRECTORY, File.basename(STANFORD_ARCHIVE, '.zip'))

  vendor_directory = File.expand_path(
    '../core/vendor/stanford-parser',
    __FILE__
  )

  Dir.chdir(TMP_DIRECTORY) do
    unless File.file?(zipname)
      puts 'Downloading the Stanford parser...'

      sh "curl -O #{STANFORD_ARCHIVE_URL}"
    end

    unless File.directory?(directory)
      puts 'Unpacking the Stanford parser...'

      sh "unzip #{STANFORD_ARCHIVE}"
    end

    puts 'Moving JAR archives into place...'

    sh "cp -f #{directory}/*.jar #{vendor_directory}"
  end
end

desc 'Alias for python:compile'
task :compile => ['stanford', 'python:compile']

desc 'Runs the tests'
task :test => :compile do
  sh('cucumber features')
end

desc 'Performs preparations for building the Gem'
task :before_build => [:requirements, 'python:clean:bytecode'] do
  path = File.join(PYTHON_SITE_PACKAGES, 'pre_build')

  install_python_packages(PRE_BUILD_REQUIREMENTS, path)
end

task :build   => :before_build
task :default => :test
