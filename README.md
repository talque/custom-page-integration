# Talque Custom Page Integration Example

This is an example app that generates a page that can be embedded as a
talque external page iframe. It receives tamper-proof information
about the talque user that opened the page as a signed Json Web
Token. Given this data, it can display personalized information in a
secure manner.


## Prerequisites

* Python 3.7+


## Build & Run

Run `./serve.sh`

This will install pyjwt in a local virtualenv. If you have that
installed already system-wide you can just run `./minimal_server.py`
