require 'opener/build-tools'

include Opener::BuildTools::Requirements
include Opener::BuildTools::Python
include Opener::BuildTools::Files

# Directory where packages will be installed to.
PYTHON_SITE_PACKAGES = File.expand_path(
  '../../../core/site-packages',
  __FILE__
)

# Directory containing the temporary files.
TMP_DIRECTORY = File.expand_path('../../../tmp', __FILE__)

# Path to the pip requirements file used to install requirements before
# packaging the Gem.
PRE_BUILD_REQUIREMENTS = File.expand_path(
  '../../../pre_build_requirements.txt',
  __FILE__
)

# Path to the pip requirements file used to install requirements upon Gem
# installation.
PRE_INSTALL_REQUIREMENTS = File.expand_path(
  '../../../pre_install_requirements.txt',
  __FILE__
)

# Path to the directory containing the Stanford parser files.
STANFORD_DIRECTORY = File.expand_path(
  '../../../core/vendor/stanford-parser',
  __FILE__
)

# Name of the Stanford zip archive.
STANFORD_ARCHIVE = 'stanford-parser-2013-04-05.zip'

# URL to the zip archive of the Stanford parser.
STANFORD_ARCHIVE_URL = "http://nlp.stanford.edu/software/#{STANFORD_ARCHIVE}"

##
# Verifies the requirements to install thi Gem.
#
def verify_requirements
  require_executable('python')
  require_version('python', python_version, '2.7.0')
  require_executable('pip')
  require_version('pip', pip_version, '1.3.1')
end
