Feature: Test webhook

  Scenario: Check webhook contains schedulePackage
     Given The webhooks from a bin
      When I get the content of them
      Then I check that in the "data" the key "schedulePackage" is present

  Scenario: Check the package is been delivered without errors
    Given The webhooks from a bin
    When I get the content of them
    Then I check that in schedulePackage success is True
    And I check that in schedulePackage error is None
    And I check that package type in schedulePackage is a dictionary
