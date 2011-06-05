PySchemaOrg
===========

An experiment in making a Python interface to the [Schema.org](http://schema.org/)
model and other similar models. This might act as a backbone for a
[microdata](http://www.w3.org/TR/microdata/) CMS, as the glue between a document
store and templating system, but it attempts to be as neutral as possible on that
count.

Elements
--------

* **multidict.py**

  The initial implementation was (very lightly) adapted from Andrew Dalke's 
  `UnorderedMultiDict`. It was the simplest, lightest implementation free of
  dependencies I could find on short notice. However, after experimenting with
  and learning from that code, I built a more idiosyncratic `MultiDict` that
  suited the base data model better.
  
* **base.py**

  There is a `Base` class from which many data models could be derived.
  The basic use is for descendent classes to form their own hierarchy, and to
  define a class dict containing properties that the class adds. The value for 
  each property's key in the class dict is a callable or class path that marshals 
  the data into an object.
  
  There are also some supporting functions to aid in automated data conversion.

* **schema.py**

  This is an attempt to replicate the entire schema.org schema in code. It uses
  the same property names, even when the spelling runs counter to Python convention.


License
-------

Copyright (c) 2011 Adam T. Lindsay

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
