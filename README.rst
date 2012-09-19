What is a catalog ?
-------------------

A catalog contains:

- child catalogs
- forms,
- lists,
- views,
- objects.

For example, if you want to manage books and paintings the catalog hierarchy
can look like:

- Catalog: Artwork
  - forms
    - CommonArtworkForm
    - ...
  - objects
    - une oeuvre pas trop detaillée
    - ...
  - catalogs
    - Book
      - forms
        - BookForm
        - ...
      - lists
        - BookList
        - ...
      - views
        - BookDetail
        - ...
      - objects
        - un livre ancien ..
        - ...
    - Painting
      - forms
        - PaintingForm
        - ...
      - lists
        - PaintingList
        - ...
      - views
        - PaintingDetail
        - ...
      - objects
        - un Picasso ..
        - ...

How to manage permissions ?
---------------------------

If you want users of group "trainees" have a BookForm without the price field
for example, then:

- create a form with:
    - a name like "Book trainee", it doesn't matter
    - catalog Book,
    - using the Book form as base
- click the "Security" tab of the form, and check for the "trainee" group

Then, open the "Security", you will see a table where each row is a group or a
user, and each column is a form. Simply check the cell in column "Group
trainee" and form "Book trainee" to authorize trainees to use the lighter Book
form.

Fields left to do
-----------------

- file upload
- file browse
- cropped image upload
- cropped image browse
- simple relation
- multiple relation
- choice
- multiple choice

FormUpdateView
--------------

Allow several bases ?
