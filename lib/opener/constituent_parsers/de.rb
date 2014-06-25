require 'open3'

require_relative 'de/version'

module Opener
  module ConstituentParsers
    ##
    # Constituent parser kernel for the German language.
    #
    # @!attribute [r] args
    #  @return [Array]
    # @!attribute [r] options
    #  @return [Hash]
    #
    class DE
      attr_reader :args, :options

      ##
      # Hash containing the default options to use.
      #
      # @return [Hash]
      #
      DEFAULT_OPTIONS = {
        :args     => []
      }.freeze

      ##
      # @param [Hash] options
      #
      # @option options [Array] :args The commandline arguments to pass to the
      #  underlying Python code.
      #
      # @see Opener::ConstituentParsers::DEFAULT_OPTIONS
      #
      def initialize(options = {})
        options  = DEFAULT_OPTIONS.merge(options)
        @args    = options.delete(:args) || []
        @options = options
      end

      ##
      # Builds the command used to execute the kernel.
      #
      # @return [String]
      #
      def command
        return "python -E #{kernel} #{args.join(' ')}"
      end

      # Runs the command and returns the output of STDOUT, STDERR and the
      # process information.
      #
      # @param [String] input The input to tag.
      # @return [Array]
      #
      def run(input)
        stdout, stderr, process = capture(input)
        raise stderr unless process.success?
        return stdout, stderr, process
      end

      protected

      ##
      # capture3 method doesn't work properly with Jruby, so
      # this is a workaround
      #
      def capture(input)
        Open3.popen3(*command.split(" ")) {|i, o, e, t|
          out_reader = Thread.new { o.read }
          err_reader = Thread.new { e.read }
          i.write input
          i.close
          [out_reader.value, err_reader.value, t.value]
        }
      end

      ##
      # @return [String]
      #
      def core_dir
        return File.expand_path('../../../../core', __FILE__)
      end

      ##
      # @return [String]
      #
      def kernel
        return File.join(core_dir, 'stanford_parser_de.py')
      end
    end # DE
  end # ConstituentParsers
end # Opener
