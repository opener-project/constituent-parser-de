require_relative '../../lib/opener/constituent_parsers/de'
require 'rspec/expectations'
require 'tempfile'

def kernel_root
  File.expand_path("../../../", __FILE__)
end

def kernel
  return Opener::ConstituentParsers::DE.new
end
