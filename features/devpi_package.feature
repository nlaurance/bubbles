Feature: Devpi server list our personal packages

  As a    Developer
  I want  to access the in house package repository
  So that I can install the latest and greatest software

  Scenario: see my personal index
    Given I access the main devpi page as "nlaurance"
    When I click My personal repository
    Then I have permission to upload packages
    And I want to "outline" this element
    And I annotate this in the "ne" with
       """
       Make sure the upload permission
       is set for you
       """
    Then I see my package list
    And I want to "outline" this element
    And I annotate this in the "ne" with
       """
       Link to detailed information
       and direct download of the package
       """
    And I want a screenshot as "annotated.png"
