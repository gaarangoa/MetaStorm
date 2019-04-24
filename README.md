## Metastorm Admin
go to settings and setup the right url

## Metastorm backend
need to update few things with the URL to work:

* For login, hardcode the url in the ./static/js/login.js file
* Add the url in the configuration file ./static/js/prod.js
* On the apache configuration need to add a proxy:

    ProxyPass /static/ http://localhost:15001/static/

This is not nice, but, works, basically there is a problem with the container and
it cannot access to the static files, therefore, nothing gets loaded, By adding
this proxy we just point to the static to MS automatically.

