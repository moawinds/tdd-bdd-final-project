Feature: The product service back-end
    As a Product Manager
    I need a RESTful catalog service
    So that I can keep track of all my products

Background:
    Given the following products
        | name       | category   | available |
        | Fedora     | CLOTHS     | True      |
        | MacBook    | ELECTRONICS| True      |
        | Desk       | FURNITURE  | False     |

Scenario: Read a Product
    When I visit the "Home Page"
    And I set the "Name" to "Fedora"
    And I press the "Search" button
    Then I should see "Fedora" in the "Name" field

Scenario: Update a Product
    When I visit the "Home Page"
    And I set the "Name" to "Fedora"
    And I press the "Search" button
    And I change "Name" to "Blue Fedora"
    And I press the "Update" button
    Then I should see the message "Success"

Scenario: Delete a Product
    When I visit the "Home Page"
    And I set the "Name" to "MacBook"
    And I press the "Search" button
    And I press the "Delete" button
    Then I should see the message "Product has been Deleted!"

Scenario: List all Products
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see "Fedora" in the results
    And I should see "MacBook" in the results
    And I should see "Desk" in the results
