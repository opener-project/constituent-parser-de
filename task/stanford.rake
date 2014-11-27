file 'tmp/stanford.zip' do |task|
  sh "wget #{STANFORD_ARCHIVE_URL} -O #{task.name} --no-check-certificate --quiet"
end

directory 'tmp/stanford' => ['tmp/stanford.zip'] do |task|
  orig_dirname = File.basename(STANFORD_ARCHIVE, '.zip')

  sh "unzip #{task.prerequisites[0]}"
  sh "mv #{orig_dirname} #{task.name}"
end

desc 'Installs the Stanford parser'
task :stanford => ['tmp/stanford'] do
  Dir.chdir('tmp/stanford') do
    STANFORD_JAR_NAMES.each do |name|
      dest = File.join(STANFORD_DIRECTORY, name)

      sh "cp -f #{name} #{dest}"
    end
  end
end
