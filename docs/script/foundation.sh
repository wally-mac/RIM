#!/bin/sh

set -e

# copy the whole sass package for the css
rm -fr _sass/motion-ui
cp -fr node_modules/motion-ui _sass/motion-ui

rm -fr _sass/foundation-sites
cp -fr node_modules/foundation-sites _sass/foundation-sites

rm -fr _sass/font-awesome
cp -fr node_modules/font-awesome _sass/font-awesome

rm -fr assets/fonts
cp -fr node_modules/font-awesome/fonts assets/fonts


# We only need a few JS files
cp node_modules/foundation-sites/dist/js/foundation.min.js assets/js/foundation.min.js
cp node_modules/foundation-sites/dist/js/foundation.min.js.map assets/js/foundation.min.js.map
cp node_modules/motion-ui/dist/motion-ui.min.js assets/js/motion-ui.min.js
cp node_modules/jquery/dist/jquery.min.* assets/js/