Kratsbox
========

A simple lightbox-like jQuery plugin focusing on usability.
What makes kratsbox different from other lightboxes is:

* _Keyboard focus_.  The close, next and prev actions get visible
  focus, and when kratsbox is closed, focus returns to the right link.

* _Only images_.  While not an feature in itself, lack of support for
  embeddly, iframes or ajax does allow the small size of kratsbox.

* _No extra loading_.  The graphics in kratsbox is pure css3, no extra
  images / sprites.


Usage
-----

First, put the kratsbox file in some path on your web server and make
sure you have them (and jQuery) availiable in the page:

    <link rel="stylesheet" type="text/css" href="/somepath/kratsbox.css"/>
    <script type="text/javascript" src="/somepath/jquery.js"></script>
    <script type="text/javascript" src="/somepath/kratsbox.js"></script>

You can (and should) combine and minify them with your other javascript and
css files to minimize impact on page load time.
If you prefer a white box over a gray, you can use _kratsbox.light.css_
instead of _kratsbox.css_.

Basic usage is just to jQuery-select the links you want to use the box
on and call kratsbox, like so:

    $('a.image').kratsbox();

As usual, you need to execute that after the links actually exist.
You also might want to set some options, e.g. for localization.
  
    $(function() {
      $('a.image').kratsbox({
        'next': 'nästa \u2192',
        'prev': 'förra \u2190',
        'close': 'stäng \u00D7'
      });
    });

This assumes you have image links.  I usually do something like:

    <a class="image" href="large-image.jpg"><img src="small-image.jpg"></a>

This makes the small image visible directly in the page, and clicknig it
brings up a box displaying the large image.

Options
-------

* `next` - Text for the link to the next image.
* `prev` - Text for the link to the previous image.
* `close` - Text for the close button.
* `minsize` - If the browser window is less tall or less wide than
   this, kratsbox functionality will be disabled.