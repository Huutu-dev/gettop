# Created by Houston Le at 12/15/2021
@platform:Windows_10
@browser:Chrome_96.0
@mode:BrowserStack
@emulation:mobileEmulation.json
Feature: Footer content and links
  Test mobile web on task TMTN-11/TMTN-97
  Scenario: Footer shows Best Selling, Latest, Top Rated categories
    Given open Home page
    And foreach footer groups
      | group         |
      | Best Selling |
      | Latest       |
      | Top Rated    |
    Then verify that each group on the footer is shown

#  Scenario: All products in the footer have price, name, star-rating
#    Given open Home page
#    Then Verify that all products on the footer have price, name
#    And Verify that at least one product on the footer has star-rating

  Scenario: Footer has working links to all product categories
    Given open Home page
    And foreach footer categories
      | category    | partial_url          |
      | MAC         | macbook/             |
      | IPHONE      | iphone/              |
      | IPAD        | ipad/                |
      | WATCH       | accessories/watch/   |
      | ACCESSORIES | accessories/airpods/ |
    Then verify that each category on the footer has valid link

  Scenario: Copyright shown in footer
    Given open Home page
    Then verify that copyright contain "Copyright 2021"