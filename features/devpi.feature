Feature: Devpi server list our packages

  As a    Developer
  I want  to access the in house package repository
  So that I can install the latest and greatest software

  Scenario Outline: see my index
    Given I access the main devpi page as "<user>"
    Then I can see my "<index>" index
    And I want to "outline" this element
    And I annotate this in the "se" with
       """
       Click the link to your
       personal repository
       """
    And I want a screenshot as "index.png"

     Examples: Developers
       | user      | index |
       | nlaurance | dev   |
