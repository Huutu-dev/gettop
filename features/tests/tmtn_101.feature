# Created by Houston Le at 11/27/2021
# Automation-gettop project
# epic TMTN-99 My Account

Feature: Account Login Error Handling
  # Task TMTN-101
  # Working on page https://gettop.us/my-account/

  Scenario: User cannot login with a blank password and blank email then sees a correct error message
    Given Open My Account Gettop
    When Clean email text input
    And Clean password text input
    And Click on LOG IN
    Then Verify the message is "Error: Username is required."


  Scenario: User cannot login with a blank email and sees a correct error message
    Given Open My Account Gettop
    When Clean email text input
    And Input eKFa-wORDpASS into password text input
    And Click on LOG IN
    Then Verify the message is "Error: Username is required."


  Scenario: User cannot login with a blank password and sees a correct error message
    Given Open My Account Gettop
    When Input fake@email.com into username text input
    And Clean password text input
    And Click on LOG IN
    Then Verify the message is "Error: The password field is empty."

  Scenario: User cannot login with invalid credentials
    # test@test.com / test and sees a correct error message
    Given Open My Account Gettop
    When Input test@test.com into username text input
    And Input eKFa-wORDpASS into password text input
    And Click on LOG IN
    Then Verify the message is "Unknown email address. Check again or try your username."

