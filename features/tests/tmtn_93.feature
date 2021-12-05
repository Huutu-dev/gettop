# Created by Houston Le at 12/4/2021
# Automation-gettop project
# epic TMTN-21 Shop

Feature: Sort by Latest Product
  # Task TMTN-93
  # Working on page https://gettop.us/shop/

  Scenario: User can sort products by Latest
    Given Open Shop page
    When Select "Sort by latest" on Order by drop box
    Then Verify order by date page will open

  Scenario: After user sorts products by Latest, they can then reset to Default Sorting
    Given Open Sort by latest page
    When Select "Default sorting" on Order by drop box
    Then Verify that "Default sorting" will be selected


  Scenario: User can go through product page number 2 after they sorted by Latest
    Given Open Sort by latest on first page
    Then Verify that number 1 to be selected
    When Click on number 2 button
    Then Verify that number 2 to be selected

  Scenario: User can go through next product page after they sorted by Latest
    Given Open Sort by latest on first page
    Then Verify that number 1 to be selected
    When Click on ">" button
    Then Verify that number 2 to be selected


  Scenario: User can go through product page number 1 after they sorted by Latest
    Given Open Sort by latest on second page
    Then Verify that number 2 to be selected
    When Click on number 1 button
    Then Verify that number 1 to be selected

  Scenario: User can go through prev product page after they sorted by Latest
    Given Open Sort by latest on second page
    Then Verify that number 2 to be selected
    When Click on "<" button
    Then Verify that number 1 to be selected