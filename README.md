# Pursuit<sup>PM<sup>
**Pursuit<sup>PM** is a project management application written for the [web2py](http://www.web2py.com) framework.

It aims at helping individuals follow up on multiple quantities of items (tasks). An item is defined as a decomposable *to-do* task for which resources are working.

The goal of the application is to provide users with an *at-a-glance* dashboard of the items featuring simple mechanics to follow-up on those.

Out of the dashboard, each item can be detailed further with the help of a log-journal, effectively allowing users to dump information on the item page to reflect its latest status.

Two type of pages are available to the user:
- The dashboard - index page
- An item page (*one for each item*)

### Dashboard - Index
Users are welcomed by the dashboard of the application, on this page users can create new *top-level* items. Top-level items get be attributed children items. The items with children can be collapsed or extended.

For each item users will see:
- The status of the items shown with a color coded pill
  - Red - Not started
  - Yellow - Action needed
  - Green - On track
- The latest log entry of the item
- the time elapsed since a log was entered for this item
- A button to edit the name of the item
- A button to view the item page

On the bottom of the page a list of all the items done is displayed in a light grey color.

## Item page
On the item page, users can set the status of the item (not started, action needed, on track or done), edit the name of item and delete the item. For convenience a navigation pane to browse parent or children items page is provided.

On this page users can add logs entries to the item, the logs support [MARKMIN](http://www.web2py.com/init/static/markmin.html) syntax.

This project is in development and more features should be added on the way based on what I feel necessary on my daily work experience.
