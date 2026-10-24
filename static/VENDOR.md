# Browser dependencies

`web/assets/jquery/jquery.min.js` is the unmodified jQuery 3.7.1 release from
https://code.jquery.com/jquery-3.7.1.min.js (MIT license in the file header).

SHA-256: `fc9a93dd241f6b045cbff0481cf4e1901becd0e12fb45166a8f17f95823f0b1a`

The old Bootstrap 4 alpha JavaScript rejected jQuery 3 and included unused
components. The site only used its menu collapse behavior. `theme/js/navigation.js`
now handles that behavior, including keyboard dismissal and resize. Existing
Bootstrap/Mobirise styles remain; no Bootstrap JavaScript is loaded.
