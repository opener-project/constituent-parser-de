Feature: using a fixture file as input and another file as the output
  In order to perform constituent parsing
  Using a file as an input
  Using a file as an output

  Scenario Outline: perform constituent parsing.
    Given the fixture file "<input_file>"
    And I put them through the kernel
    Then the output should match the fixture "<output_file>"
  Examples:
    | input_file      | output_file        |
    | file.1.in.kaf   | file.1.out.kaf     |
    | file.2.in.kaf   | file.2.out.kaf     |
