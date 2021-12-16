# Created by Houston Le at 12/7/2021

#@browser:Firefox_94.0
#@platform:Windows_10
#@browser:Chrome_96.0
#@mode:headless_EventFiring
#@mode:EventFiring

#@platform:OS&X_Big&Sur
#@browser:Safari_14.1
#@mode:BrowserStack
Feature: Top Cart Menu
  # Task TMTN-5 / TMTN-10

  Scenario: Hovering over empty cart icon shows "No products in the cart." message
    Given open Home page
    Then verify if no products were added
    When hover over Cart icon
    Then verify that message is "No products in the cart."

  Scenario: Clicking on Cart icon opens Empty Cart page if no products were added
    Given open Home page
    Then verify if no products were added
    When click on Cart
    Then verify that Empty Cart page opened

  Scenario Outline: Add product to cart, verify that values in top nav menu is correct
    Given a "<product>" page "<link>"
    Then verify that product is in stock
    When add to cart
    Then verify that amount of price is correct
    And verify that amount of items are correct
    Examples: Multi products
      |product                             |link                                     |
      |AirPods Pro                         |https://gettop.us/product/airpods-pro/
      |AirPods with Wireless Charging Case |https://gettop.us/product/airpods/
      |MacBook Air                         |https://gettop.us/product/macbook-air/
      |MacBook Pro 13-inch                 |https://gettop.us/product/macbook-pro-13/
      |MacBook Pro 16-inch                 |https://gettop.us/product/macbook-pro-16/
      |Watch Series 3                      |https://gettop.us/product/land-tee-jack-jones/
      |iPad                                |https://gettop.us/product/ipad/
      |iPad Air                            |https://gettop.us/product/ipad-air/
      |iPad Pro                            |https://gettop.us/product/ipad-pro/
      |iPad mini                           |https://gettop.us/product/ipad-mini/
      |iPhone 11                           |https://gettop.us/product/iphone-11/
      |iPhone 11 Pro                       |https://gettop.us/product/iphone-11pro/
      |iPhone SE                           |https://gettop.us/product/iphone-se/

  Scenario: Add product to cart, hover over Cart icon, verify correct products and subtotal shown
    Given a "iPhone SE" page "iphone-se/"
    When add to cart
    And hover over Cart icon
    Then verify correct products and subtotal shown

  Scenario: Add products to cart, hover over Cart icon, verify user can click on "View Cart" and is taken to cart page
    Given a "iPhone SE" page "iphone-se/"
    When add to cart
    And hover over Cart icon
    Then verify user can click on "View Cart" and is taken to cart page

  Scenario: Add products to cart, hover over Cart icon, verify user can click on "Checkout" and is taken to checkout page
    Given a "iPhone SE" page "iphone-se/"
    When add to cart
    And hover over Cart icon
    Then verify user can click on "Checkout" and is taken to checkout page

  Scenario: Add a product to cart, hover over Cart icon, verify user can remove a product
    Given a "iPhone SE" page "iphone-se/"
    When add to cart
    And hover over Cart icon
    Then verify user can remove a product
