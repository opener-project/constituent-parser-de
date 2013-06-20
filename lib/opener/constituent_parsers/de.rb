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
        return "python -E -O #{kernel} #{args.join(' ')}"
      end

      ##
      # Runs the command and returns the output of STDOUT, STDERR and the
      # process information.
      #
      # @param [String] input The input to process.
      # @return [Array]
      #
      def run(input)
        unless File.file?(kernel)
          raise "The Python kernel (#{kernel}) does not exist"
        end

        return Open3.capture3(command, :stdin_data => input)
      end

      ##
      # Runs the command and takes care of error handling/aborting based on the
      # output.
      #
      # @see #run
      #
      def run!(input)
        stdout, stderr, process = run(input)

        if process.success?
          puts stdout

          STDERR.puts(stderr) unless stderr.empty?
        else
          abort stderr
        end
      end

      protected

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
