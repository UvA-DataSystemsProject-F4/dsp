# dsp

# Installation
1) Clone Repository
2) Install libraries:
   1) pip install -r requirements.txt 
3) Create Database:
   1) Either download pre-created one or
   2) Make database by running: python manage.py migrate


# Working with the Code

* All UI code should go into the dspui sub folder
  * HTML code needs to be in the templates folder
  * All static files (css, javascript, images, etc) needs to go into the Static folder
  * Things that need to be available globally need to be referenced in Base.html
  * Style sheets are created with SCSS, which is compiled into css automatically