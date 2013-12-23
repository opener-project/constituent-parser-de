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

namespace :clean do
  desc 'Removes Stanford parser related files'
  task :stanford do
    Dir.glob(File.join(TMP_DIRECTORY, '*')).each do |path|
      sh "rm -rf #{path}"
    end

    Dir.glob(File.join(STANFORD_DIRECTORY, '*.jar')).each do |path|
      sh "rm #{path}"
    end
  end
end

desc 'Cleans up the repository'
task :clean => [
  'python:clean:bytecode',
  'python:clean:packages',
  'clean:tmp',
  'clean:gems',
  'clean:stanford'
]

desc 'Installs the Stanford parser JAR archives'
task :stanford do
  zipname   = File.join(TMP_DIRECTORY, STANFORD_ARCHIVE)
  directory = File.join(TMP_DIRECTORY, File.basename(STANFORD_ARCHIVE, '.zip'))

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

    sh "cp -f #{directory}/stanford-parser.jar #{STANFORD_DIRECTORY}"
    sh "cp -f #{directory}/stanford-parser-2.0.5-models.jar #{STANFORD_DIRECTORY}"
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
