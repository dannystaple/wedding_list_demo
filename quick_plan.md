* Use Flask + Jquery for the front end.
* Github actions for CI testing.
* Docker compose for desktop environment

Front End:

* index 
    * Shows gift list.
    * Add -> product selection
    * Gift -> Subtract button
    * Gift -> Purchase button 
        * Greyed when bought. - changed to tick.
        * More prominent than remove.
    * Gift Report - should be served up as static (low/no js)  - so it's saveable/printable
        * Purchase section
        * Not Purchased section.

# How It could be improved

* Selenium for front end testing - using a Docker firefox webdriver image.
* Mocha for JS testing

# Known Bugs

* We could definitely handle the "gift added twice" - pass it to the browser, or filter the list of gifts by that.
* Definitely needs an "are you sure" button.

# Addable features

* The models allow filtering by price. Could put a price field and button.
* Filtering by brands - perhaps lookup by brands/filter in the add list.

