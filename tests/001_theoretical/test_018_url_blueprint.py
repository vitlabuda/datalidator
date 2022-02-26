#!/bin/false

# Copyright (c) 2022 Vít Labuda. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#  1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
#     disclaimer.
#  2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
#     following disclaimer in the documentation and/or other materials provided with the distribution.
#  3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
#     products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import os
import os.path
import sys
if "DATALIDATOR_TESTS_AUTOPATH" in os.environ:
    __TESTS_DIR = os.path.dirname(os.path.realpath(__file__))
    __MODULE_DIR = os.path.realpath(os.path.join(__TESTS_DIR, "../.."))
    if __TESTS_DIR not in sys.path:
        sys.path.insert(0, __TESTS_DIR)
    if __MODULE_DIR not in sys.path:
        sys.path.insert(0, __MODULE_DIR)

import theoretical_testutils
import pytest
import datetime
import ipaddress
import uuid
import urllib.parse
from urllib.parse import ParseResult
from test_014_string_blueprint import StringableObject, ExceptionRaisingStringableObject
from datalidator.blueprints.impl.URLBlueprint import URLBlueprint
from datalidator.blueprints.exc.InputDataTypeNotInAllowlistExc import InputDataTypeNotInAllowlistExc
from datalidator.blueprints.exc.InputDataNotConvertibleExc import InputDataNotConvertibleExc


# NOTE: Some outputs might not seem "sane" when comparing them to input data.
#  However, the outputs are produced by underlying Python standard library functions which might have some quirks caused by their internal implementation.
#  As testing the standard library is obviously not the objective of this test, it does not matter - the important thing is that the tested blueprints, filters and validators themselves work fine.


__URL_BLUEPRINT_TEST_SUITE = (
    (URLBlueprint(), (
        (
            urllib.parse.urlparse("https://docs.python.org/3/library/urllib.parse.html?highlight=params#url-parsing"),
            ParseResult(scheme="https", netloc="docs.python.org", path="/3/library/urllib.parse.html", params="", query="highlight=params", fragment="url-parsing")  # noqa
        ),
        (
            urllib.parse.urlparse("https://user@pass:www.example.org:8443/hello/world.txt;params=something?abc=def&xyz=123#page-part"),
            ParseResult(scheme="https", netloc="user@pass:www.example.org:8443", path="/hello/world.txt", params="params=something", query="abc=def&xyz=123", fragment="page-part")  # noqa
        ),
        (
            urllib.parse.urlparse("someprotocol://user@pass:www.example.org:8443/hello/world.txt;params=something?abc=def&xyz=123#page-part"),
            ParseResult(scheme="someprotocol", netloc="user@pass:www.example.org:8443", path="/hello/world.txt;params=something", params="", query="abc=def&xyz=123", fragment="page-part")  # noqa
        ),
        (
            urllib.parse.urlparse("https://český.web.cz/Příliš žluťoučký kůň/šložka/soubor.html;parametry=něco?možnost1=🤍&možnost2=Добро пожаловать#část stránky"),
            ParseResult(scheme="https", netloc="český.web.cz", path="/Příliš žluťoučký kůň/šložka/soubor.html", params="parametry=něco", query="možnost1=🤍&možnost2=Добро пожаловать", fragment="část stránky")  # noqa
        ),
        (
            urllib.parse.urlparse("https://xn--esk-noa0f.web.cz/P%C5%99%C3%ADli%C5%A1%20%C5%BElu%C5%A5ou%C4%8Dk%C3%BD%20k%C5%AF%C5%88%2F%C5%A1lo%C5%BEka%2Fsoubor.html;parametry=n%C4%9Bco?mo%C5%BEnost1=%F0%9F%A4%8D&mo%C5%BEnost2=%D0%94%D0%BE%D0%B1%D1%80%D0%BE%20%D0%BF%D0%BE%D0%B6%D0%B0%D0%BB%D0%BE%D0%B2%D0%B0%D1%82%D1%8C#%C4%8D%C3%A1st%20str%C3%A1nky"),
            ParseResult(scheme="https", netloc="xn--esk-noa0f.web.cz", path="/P%C5%99%C3%ADli%C5%A1%20%C5%BElu%C5%A5ou%C4%8Dk%C3%BD%20k%C5%AF%C5%88%2F%C5%A1lo%C5%BEka%2Fsoubor.html", params="parametry=n%C4%9Bco", query="mo%C5%BEnost1=%F0%9F%A4%8D&mo%C5%BEnost2=%D0%94%D0%BE%D0%B1%D1%80%D0%BE%20%D0%BF%D0%BE%D0%B6%D0%B0%D0%BB%D0%BE%D0%B2%D0%B0%D1%82%D1%8C", fragment="%C4%8D%C3%A1st%20str%C3%A1nky")  # noqa
        ),
        (
            urllib.parse.urlparse("řeřicha://český.web.cz/Příliš žluťoučký kůň/šložka/soubor.html;parametry=něco?možnost1=🤍&možnost2=Добро пожаловать#část stránky"),
            ParseResult(scheme="", netloc="", path="řeřicha://český.web.cz/Příliš žluťoučký kůň/šložka/soubor.html", params="parametry=něco", query="možnost1=🤍&možnost2=Добро пожаловать", fragment="část stránky")  # noqa
        ),
        (
            urllib.parse.urlparse("%C5%99e%C5%99icha://xn--esk-noa0f.web.cz/P%C5%99%C3%ADli%C5%A1%20%C5%BElu%C5%A5ou%C4%8Dk%C3%BD%20k%C5%AF%C5%88%2F%C5%A1lo%C5%BEka%2Fsoubor.html;parametry=n%C4%9Bco?mo%C5%BEnost1=%F0%9F%A4%8D&mo%C5%BEnost2=%D0%94%D0%BE%D0%B1%D1%80%D0%BE%20%D0%BF%D0%BE%D0%B6%D0%B0%D0%BB%D0%BE%D0%B2%D0%B0%D1%82%D1%8C#%C4%8D%C3%A1st%20str%C3%A1nky"),
            ParseResult(scheme="", netloc="", path="%C5%99e%C5%99icha://xn--esk-noa0f.web.cz/P%C5%99%C3%ADli%C5%A1%20%C5%BElu%C5%A5ou%C4%8Dk%C3%BD%20k%C5%AF%C5%88%2F%C5%A1lo%C5%BEka%2Fsoubor.html", params="parametry=n%C4%9Bco", query="mo%C5%BEnost1=%F0%9F%A4%8D&mo%C5%BEnost2=%D0%94%D0%BE%D0%B1%D1%80%D0%BE%20%D0%BF%D0%BE%D0%B6%D0%B0%D0%BB%D0%BE%D0%B2%D0%B0%D1%82%D1%8C", fragment="%C4%8D%C3%A1st%20str%C3%A1nky")  # noqa
        ),
        (
            "https://docs.python.org/3/library/urllib.parse.html?highlight=params#url-parsing",
            ParseResult(scheme="https", netloc="docs.python.org", path="/3/library/urllib.parse.html", params="", query="highlight=params", fragment="url-parsing")  # noqa
        ),
        (
            "https://user@pass:www.example.org:8443/hello/world.txt;params=something?abc=def&xyz=123#page-part",
            ParseResult(scheme="https", netloc="user@pass:www.example.org:8443", path="/hello/world.txt", params="params=something", query="abc=def&xyz=123", fragment="page-part")  # noqa
        ),
        (
            "someprotocol://user@pass:www.example.org:8443/hello/world.txt;params=something?abc=def&xyz=123#page-part",
            ParseResult(scheme="someprotocol", netloc="user@pass:www.example.org:8443", path="/hello/world.txt;params=something", params="", query="abc=def&xyz=123", fragment="page-part")  # noqa
        ),
        (
            "https://český.web.cz/Příliš žluťoučký kůň/šložka/soubor.html;parametry=něco?možnost1=🤍&možnost2=Добро пожаловать#část stránky",
            ParseResult(scheme="https", netloc="český.web.cz", path="/Příliš žluťoučký kůň/šložka/soubor.html", params="parametry=něco", query="možnost1=🤍&možnost2=Добро пожаловать", fragment="část stránky")  # noqa
        ),
        (
            "https://uživatel@heslo:český.web.cz:8443/Příliš žluťoučký kůň/šložka/soubor.html;parametry=něco?možnost1=🤍&možnost2=Добро пожаловать#část stránky",
            ParseResult(scheme="https", netloc="uživatel@heslo:český.web.cz:8443", path="/Příliš žluťoučký kůň/šložka/soubor.html", params="parametry=něco", query="možnost1=🤍&možnost2=Добро пожаловать", fragment="část stránky")  # noqa
        ),
        (
            "https://xn--esk-noa0f.web.cz/P%C5%99%C3%ADli%C5%A1%20%C5%BElu%C5%A5ou%C4%8Dk%C3%BD%20k%C5%AF%C5%88%2F%C5%A1lo%C5%BEka%2Fsoubor.html;parametry=n%C4%9Bco?mo%C5%BEnost1=%F0%9F%A4%8D&mo%C5%BEnost2=%D0%94%D0%BE%D0%B1%D1%80%D0%BE%20%D0%BF%D0%BE%D0%B6%D0%B0%D0%BB%D0%BE%D0%B2%D0%B0%D1%82%D1%8C#%C4%8D%C3%A1st%20str%C3%A1nky",
            ParseResult(scheme="https", netloc="xn--esk-noa0f.web.cz", path="/P%C5%99%C3%ADli%C5%A1%20%C5%BElu%C5%A5ou%C4%8Dk%C3%BD%20k%C5%AF%C5%88%2F%C5%A1lo%C5%BEka%2Fsoubor.html", params="parametry=n%C4%9Bco", query="mo%C5%BEnost1=%F0%9F%A4%8D&mo%C5%BEnost2=%D0%94%D0%BE%D0%B1%D1%80%D0%BE%20%D0%BF%D0%BE%D0%B6%D0%B0%D0%BB%D0%BE%D0%B2%D0%B0%D1%82%D1%8C", fragment="%C4%8D%C3%A1st%20str%C3%A1nky")  # noqa
        ),
        (
            "https://u%C5%BEivatel:heslo@xn--esk-noa0f.web.cz:8443/P%C5%99%C3%ADli%C5%A1%20%C5%BElu%C5%A5ou%C4%8Dk%C3%BD%20k%C5%AF%C5%88%2F%C5%A1lo%C5%BEka%2Fsoubor.html;parametry=n%C4%9Bco?mo%C5%BEnost1=%F0%9F%A4%8D&mo%C5%BEnost2=%D0%94%D0%BE%D0%B1%D1%80%D0%BE%20%D0%BF%D0%BE%D0%B6%D0%B0%D0%BB%D0%BE%D0%B2%D0%B0%D1%82%D1%8C#%C4%8D%C3%A1st%20str%C3%A1nky",
            ParseResult(scheme="https", netloc="u%C5%BEivatel:heslo@xn--esk-noa0f.web.cz:8443", path="/P%C5%99%C3%ADli%C5%A1%20%C5%BElu%C5%A5ou%C4%8Dk%C3%BD%20k%C5%AF%C5%88%2F%C5%A1lo%C5%BEka%2Fsoubor.html", params="parametry=n%C4%9Bco", query="mo%C5%BEnost1=%F0%9F%A4%8D&mo%C5%BEnost2=%D0%94%D0%BE%D0%B1%D1%80%D0%BE%20%D0%BF%D0%BE%D0%B6%D0%B0%D0%BB%D0%BE%D0%B2%D0%B0%D1%82%D1%8C", fragment="%C4%8D%C3%A1st%20str%C3%A1nky")  # noqa
        ),
        (
            "řeřicha://český.web.cz/Příliš žluťoučký kůň/šložka/soubor.html;parametry=něco?možnost1=🤍&možnost2=Добро пожаловать#část stránky",
            ParseResult(scheme="", netloc="", path="řeřicha://český.web.cz/Příliš žluťoučký kůň/šložka/soubor.html", params="parametry=něco", query="možnost1=🤍&možnost2=Добро пожаловать", fragment="část stránky")  # noqa
        ),
        (
            "řeřicha://uživatel@heslo:český.web.cz:8443/Příliš žluťoučký kůň/šložka/soubor.html;parametry=něco?možnost1=🤍&možnost2=Добро пожаловать#část stránky",
            ParseResult(scheme="", netloc="", path="řeřicha://uživatel@heslo:český.web.cz:8443/Příliš žluťoučký kůň/šložka/soubor.html", params="parametry=něco", query="možnost1=🤍&možnost2=Добро пожаловать", fragment="část stránky")  # noqa
        ),
        (
            "%C5%99e%C5%99icha://xn--esk-noa0f.web.cz/P%C5%99%C3%ADli%C5%A1%20%C5%BElu%C5%A5ou%C4%8Dk%C3%BD%20k%C5%AF%C5%88%2F%C5%A1lo%C5%BEka%2Fsoubor.html;parametry=n%C4%9Bco?mo%C5%BEnost1=%F0%9F%A4%8D&mo%C5%BEnost2=%D0%94%D0%BE%D0%B1%D1%80%D0%BE%20%D0%BF%D0%BE%D0%B6%D0%B0%D0%BB%D0%BE%D0%B2%D0%B0%D1%82%D1%8C#%C4%8D%C3%A1st%20str%C3%A1nky",
            ParseResult(scheme="", netloc="", path="%C5%99e%C5%99icha://xn--esk-noa0f.web.cz/P%C5%99%C3%ADli%C5%A1%20%C5%BElu%C5%A5ou%C4%8Dk%C3%BD%20k%C5%AF%C5%88%2F%C5%A1lo%C5%BEka%2Fsoubor.html", params="parametry=n%C4%9Bco", query="mo%C5%BEnost1=%F0%9F%A4%8D&mo%C5%BEnost2=%D0%94%D0%BE%D0%B1%D1%80%D0%BE%20%D0%BF%D0%BE%D0%B6%D0%B0%D0%BB%D0%BE%D0%B2%D0%B0%D1%82%D1%8C", fragment="%C4%8D%C3%A1st%20str%C3%A1nky")  # noqa
        ),
        (
            "%C5%99e%C5%99icha://u%C5%BEivatel:heslo@xn--esk-noa0f.web.cz:8443/P%C5%99%C3%ADli%C5%A1%20%C5%BElu%C5%A5ou%C4%8Dk%C3%BD%20k%C5%AF%C5%88%2F%C5%A1lo%C5%BEka%2Fsoubor.html;parametry=n%C4%9Bco?mo%C5%BEnost1=%F0%9F%A4%8D&mo%C5%BEnost2=%D0%94%D0%BE%D0%B1%D1%80%D0%BE%20%D0%BF%D0%BE%D0%B6%D0%B0%D0%BB%D0%BE%D0%B2%D0%B0%D1%82%D1%8C#%C4%8D%C3%A1st%20str%C3%A1nky",
            ParseResult(scheme="", netloc="", path="%C5%99e%C5%99icha://u%C5%BEivatel:heslo@xn--esk-noa0f.web.cz:8443/P%C5%99%C3%ADli%C5%A1%20%C5%BElu%C5%A5ou%C4%8Dk%C3%BD%20k%C5%AF%C5%88%2F%C5%A1lo%C5%BEka%2Fsoubor.html", params="parametry=n%C4%9Bco", query="mo%C5%BEnost1=%F0%9F%A4%8D&mo%C5%BEnost2=%D0%94%D0%BE%D0%B1%D1%80%D0%BE%20%D0%BF%D0%BE%D0%B6%D0%B0%D0%BB%D0%BE%D0%B2%D0%B0%D1%82%D1%8C", fragment="%C4%8D%C3%A1st%20str%C3%A1nky")  # noqa
        ),
        # The following 504 entries are auto-generated (and then checked manually - oh my...) by the following Python code (which was run via Jupyter Notebook):
        #   import urllib.parse
        #   i=0
        #   out=""
        #   for scheme in ("", "https", "invalidproto"):
        #       for netloc in ("", "www.example.org", "user@pass:www.example.org:8443", "uživatel@heslo:příklad.cz:8443", "uživatel@heslo:[2001:db8::1234]:8443"):
        #           for path in ("/", "/Příliš žluťoučký/kůň 🤍.jpg", "/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt"):
        #               for params in ("", "Příliš žluťoučký kůň=🤍"):
        #                   for query in ("", "abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍", "test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test"):
        #                       for fragment in ("", "Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍"):
        #                           if scheme == "invalidproto" and params != "":
        #                               path += (";" + params)
        #                               params = ""
        #                           result=urllib.parse.ParseResult(scheme=scheme, netloc=netloc, path=path, params=params, query=query, fragment=fragment)  # noqa
        #                           url=repr(urllib.parse.urlunparse(result))
        #                           out+="\t\t(\n\t\t\t{url},\n\t\t\t{result}\n\t\t),\n".format(url=url, result=result)
        #                           i+=1
        #   out = out.replace("\t", " " * 4)
        #   with open("/home/development/TEMP/url-testsuite.txt", "w") as f:
        #       f.write(out)
        #   print(i)
        (
            '/',
            ParseResult(scheme='', netloc='', path='/', params='', query='', fragment='')  # noqa
        ),
        (
            '/#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='', path='/', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '/?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='', netloc='', path='/', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            '/?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='', path='/', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '/?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='', netloc='', path='/', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            '/?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='', path='/', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '/;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='', netloc='', path='/', params='Příliš žluťoučký kůň=🤍', query='', fragment='')  # noqa
        ),
        (
            '/;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='', path='/', params='Příliš žluťoučký kůň=🤍', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '/;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='', netloc='', path='/', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            '/;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='', path='/', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '/;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='', netloc='', path='/', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            '/;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='', path='/', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '/Příliš žluťoučký/kůň 🤍.jpg',
            ParseResult(scheme='', netloc='', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='', fragment='')  # noqa
        ),
        (
            '/Příliš žluťoučký/kůň 🤍.jpg#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '/Příliš žluťoučký/kůň 🤍.jpg?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='', netloc='', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            '/Příliš žluťoučký/kůň 🤍.jpg?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '/Příliš žluťoučký/kůň 🤍.jpg?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='', netloc='', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            '/Příliš žluťoučký/kůň 🤍.jpg?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='', netloc='', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='', fragment='')  # noqa
        ),
        (
            '/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='', netloc='', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            '/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='', netloc='', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            '/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt',
            ParseResult(scheme='', netloc='', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='', fragment='')  # noqa
        ),
        (
            '/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='', netloc='', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            '/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='', netloc='', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            '/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='', netloc='', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='', fragment='')  # noqa
        ),
        (
            '/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='', netloc='', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            '/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='', netloc='', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            '/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//www.example.org/',
            ParseResult(scheme='', netloc='www.example.org', path='/', params='', query='', fragment='')  # noqa
        ),
        (
            '//www.example.org/#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='www.example.org', path='/', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//www.example.org/?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='', netloc='www.example.org', path='/', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            '//www.example.org/?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='www.example.org', path='/', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//www.example.org/?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='', netloc='www.example.org', path='/', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            '//www.example.org/?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='www.example.org', path='/', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//www.example.org/;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='', netloc='www.example.org', path='/', params='Příliš žluťoučký kůň=🤍', query='', fragment='')  # noqa
        ),
        (
            '//www.example.org/;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='www.example.org', path='/', params='Příliš žluťoučký kůň=🤍', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//www.example.org/;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='', netloc='www.example.org', path='/', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            '//www.example.org/;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='www.example.org', path='/', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//www.example.org/;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='', netloc='www.example.org', path='/', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            '//www.example.org/;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='www.example.org', path='/', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//www.example.org/Příliš žluťoučký/kůň 🤍.jpg',
            ParseResult(scheme='', netloc='www.example.org', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='', fragment='')  # noqa
        ),
        (
            '//www.example.org/Příliš žluťoučký/kůň 🤍.jpg#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='www.example.org', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//www.example.org/Příliš žluťoučký/kůň 🤍.jpg?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='', netloc='www.example.org', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            '//www.example.org/Příliš žluťoučký/kůň 🤍.jpg?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='www.example.org', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//www.example.org/Příliš žluťoučký/kůň 🤍.jpg?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='', netloc='www.example.org', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            '//www.example.org/Příliš žluťoučký/kůň 🤍.jpg?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='www.example.org', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//www.example.org/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='', netloc='www.example.org', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='', fragment='')  # noqa
        ),
        (
            '//www.example.org/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='www.example.org', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//www.example.org/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='', netloc='www.example.org', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            '//www.example.org/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='www.example.org', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//www.example.org/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='', netloc='www.example.org', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            '//www.example.org/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='www.example.org', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//www.example.org/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt',
            ParseResult(scheme='', netloc='www.example.org', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='', fragment='')  # noqa
        ),
        (
            '//www.example.org/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='www.example.org', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//www.example.org/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='', netloc='www.example.org', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            '//www.example.org/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='www.example.org', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//www.example.org/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='', netloc='www.example.org', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            '//www.example.org/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='www.example.org', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//www.example.org/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='', netloc='www.example.org', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='', fragment='')  # noqa
        ),
        (
            '//www.example.org/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='www.example.org', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//www.example.org/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='', netloc='www.example.org', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            '//www.example.org/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='www.example.org', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//www.example.org/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='', netloc='www.example.org', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            '//www.example.org/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='www.example.org', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//user@pass:www.example.org:8443/',
            ParseResult(scheme='', netloc='user@pass:www.example.org:8443', path='/', params='', query='', fragment='')  # noqa
        ),
        (
            '//user@pass:www.example.org:8443/#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='user@pass:www.example.org:8443', path='/', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//user@pass:www.example.org:8443/?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='', netloc='user@pass:www.example.org:8443', path='/', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            '//user@pass:www.example.org:8443/?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='user@pass:www.example.org:8443', path='/', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//user@pass:www.example.org:8443/?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='', netloc='user@pass:www.example.org:8443', path='/', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            '//user@pass:www.example.org:8443/?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='user@pass:www.example.org:8443', path='/', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//user@pass:www.example.org:8443/;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='', netloc='user@pass:www.example.org:8443', path='/', params='Příliš žluťoučký kůň=🤍', query='', fragment='')  # noqa
        ),
        (
            '//user@pass:www.example.org:8443/;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='user@pass:www.example.org:8443', path='/', params='Příliš žluťoučký kůň=🤍', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//user@pass:www.example.org:8443/;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='', netloc='user@pass:www.example.org:8443', path='/', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            '//user@pass:www.example.org:8443/;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='user@pass:www.example.org:8443', path='/', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//user@pass:www.example.org:8443/;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='', netloc='user@pass:www.example.org:8443', path='/', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            '//user@pass:www.example.org:8443/;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='user@pass:www.example.org:8443', path='/', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//user@pass:www.example.org:8443/Příliš žluťoučký/kůň 🤍.jpg',
            ParseResult(scheme='', netloc='user@pass:www.example.org:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='', fragment='')  # noqa
        ),
        (
            '//user@pass:www.example.org:8443/Příliš žluťoučký/kůň 🤍.jpg#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='user@pass:www.example.org:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//user@pass:www.example.org:8443/Příliš žluťoučký/kůň 🤍.jpg?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='', netloc='user@pass:www.example.org:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            '//user@pass:www.example.org:8443/Příliš žluťoučký/kůň 🤍.jpg?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='user@pass:www.example.org:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//user@pass:www.example.org:8443/Příliš žluťoučký/kůň 🤍.jpg?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='', netloc='user@pass:www.example.org:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            '//user@pass:www.example.org:8443/Příliš žluťoučký/kůň 🤍.jpg?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='user@pass:www.example.org:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//user@pass:www.example.org:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='', netloc='user@pass:www.example.org:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='', fragment='')  # noqa
        ),
        (
            '//user@pass:www.example.org:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='user@pass:www.example.org:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//user@pass:www.example.org:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='', netloc='user@pass:www.example.org:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            '//user@pass:www.example.org:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='user@pass:www.example.org:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//user@pass:www.example.org:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='', netloc='user@pass:www.example.org:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            '//user@pass:www.example.org:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='user@pass:www.example.org:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//user@pass:www.example.org:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt',
            ParseResult(scheme='', netloc='user@pass:www.example.org:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='', fragment='')  # noqa
        ),
        (
            '//user@pass:www.example.org:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='user@pass:www.example.org:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//user@pass:www.example.org:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='', netloc='user@pass:www.example.org:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            '//user@pass:www.example.org:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='user@pass:www.example.org:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//user@pass:www.example.org:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='', netloc='user@pass:www.example.org:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            '//user@pass:www.example.org:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='user@pass:www.example.org:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//user@pass:www.example.org:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='', netloc='user@pass:www.example.org:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='', fragment='')  # noqa
        ),
        (
            '//user@pass:www.example.org:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='user@pass:www.example.org:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//user@pass:www.example.org:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='', netloc='user@pass:www.example.org:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            '//user@pass:www.example.org:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='user@pass:www.example.org:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//user@pass:www.example.org:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='', netloc='user@pass:www.example.org:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            '//user@pass:www.example.org:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='user@pass:www.example.org:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//uživatel@heslo:příklad.cz:8443/',
            ParseResult(scheme='', netloc='uživatel@heslo:příklad.cz:8443', path='/', params='', query='', fragment='')  # noqa
        ),
        (
            '//uživatel@heslo:příklad.cz:8443/#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:příklad.cz:8443', path='/', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//uživatel@heslo:příklad.cz:8443/?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:příklad.cz:8443', path='/', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            '//uživatel@heslo:příklad.cz:8443/?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:příklad.cz:8443', path='/', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//uživatel@heslo:příklad.cz:8443/?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='', netloc='uživatel@heslo:příklad.cz:8443', path='/', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            '//uživatel@heslo:příklad.cz:8443/?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:příklad.cz:8443', path='/', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//uživatel@heslo:příklad.cz:8443/;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:příklad.cz:8443', path='/', params='Příliš žluťoučký kůň=🤍', query='', fragment='')  # noqa
        ),
        (
            '//uživatel@heslo:příklad.cz:8443/;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:příklad.cz:8443', path='/', params='Příliš žluťoučký kůň=🤍', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//uživatel@heslo:příklad.cz:8443/;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:příklad.cz:8443', path='/', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            '//uživatel@heslo:příklad.cz:8443/;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:příklad.cz:8443', path='/', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//uživatel@heslo:příklad.cz:8443/;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='', netloc='uživatel@heslo:příklad.cz:8443', path='/', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            '//uživatel@heslo:příklad.cz:8443/;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:příklad.cz:8443', path='/', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//uživatel@heslo:příklad.cz:8443/Příliš žluťoučký/kůň 🤍.jpg',
            ParseResult(scheme='', netloc='uživatel@heslo:příklad.cz:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='', fragment='')  # noqa
        ),
        (
            '//uživatel@heslo:příklad.cz:8443/Příliš žluťoučký/kůň 🤍.jpg#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:příklad.cz:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//uživatel@heslo:příklad.cz:8443/Příliš žluťoučký/kůň 🤍.jpg?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:příklad.cz:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            '//uživatel@heslo:příklad.cz:8443/Příliš žluťoučký/kůň 🤍.jpg?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:příklad.cz:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//uživatel@heslo:příklad.cz:8443/Příliš žluťoučký/kůň 🤍.jpg?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='', netloc='uživatel@heslo:příklad.cz:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            '//uživatel@heslo:příklad.cz:8443/Příliš žluťoučký/kůň 🤍.jpg?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:příklad.cz:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//uživatel@heslo:příklad.cz:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:příklad.cz:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='', fragment='')  # noqa
        ),
        (
            '//uživatel@heslo:příklad.cz:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:příklad.cz:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//uživatel@heslo:příklad.cz:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:příklad.cz:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            '//uživatel@heslo:příklad.cz:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:příklad.cz:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//uživatel@heslo:příklad.cz:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='', netloc='uživatel@heslo:příklad.cz:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            '//uživatel@heslo:příklad.cz:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:příklad.cz:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//uživatel@heslo:příklad.cz:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt',
            ParseResult(scheme='', netloc='uživatel@heslo:příklad.cz:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='', fragment='')  # noqa
        ),
        (
            '//uživatel@heslo:příklad.cz:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:příklad.cz:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//uživatel@heslo:příklad.cz:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:příklad.cz:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            '//uživatel@heslo:příklad.cz:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:příklad.cz:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//uživatel@heslo:příklad.cz:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='', netloc='uživatel@heslo:příklad.cz:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            '//uživatel@heslo:příklad.cz:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:příklad.cz:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//uživatel@heslo:příklad.cz:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:příklad.cz:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='', fragment='')  # noqa
        ),
        (
            '//uživatel@heslo:příklad.cz:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:příklad.cz:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//uživatel@heslo:příklad.cz:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:příklad.cz:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            '//uživatel@heslo:příklad.cz:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:příklad.cz:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//uživatel@heslo:příklad.cz:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='', netloc='uživatel@heslo:příklad.cz:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            '//uživatel@heslo:příklad.cz:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:příklad.cz:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//uživatel@heslo:[2001:db8::1234]:8443/',
            ParseResult(scheme='', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/', params='', query='', fragment='')  # noqa
        ),
        (
            '//uživatel@heslo:[2001:db8::1234]:8443/#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//uživatel@heslo:[2001:db8::1234]:8443/?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            '//uživatel@heslo:[2001:db8::1234]:8443/?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//uživatel@heslo:[2001:db8::1234]:8443/?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            '//uživatel@heslo:[2001:db8::1234]:8443/?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//uživatel@heslo:[2001:db8::1234]:8443/;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/', params='Příliš žluťoučký kůň=🤍', query='', fragment='')  # noqa
        ),
        (
            '//uživatel@heslo:[2001:db8::1234]:8443/;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/', params='Příliš žluťoučký kůň=🤍', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//uživatel@heslo:[2001:db8::1234]:8443/;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            '//uživatel@heslo:[2001:db8::1234]:8443/;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//uživatel@heslo:[2001:db8::1234]:8443/;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            '//uživatel@heslo:[2001:db8::1234]:8443/;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//uživatel@heslo:[2001:db8::1234]:8443/Příliš žluťoučký/kůň 🤍.jpg',
            ParseResult(scheme='', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='', fragment='')  # noqa
        ),
        (
            '//uživatel@heslo:[2001:db8::1234]:8443/Příliš žluťoučký/kůň 🤍.jpg#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//uživatel@heslo:[2001:db8::1234]:8443/Příliš žluťoučký/kůň 🤍.jpg?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            '//uživatel@heslo:[2001:db8::1234]:8443/Příliš žluťoučký/kůň 🤍.jpg?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//uživatel@heslo:[2001:db8::1234]:8443/Příliš žluťoučký/kůň 🤍.jpg?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            '//uživatel@heslo:[2001:db8::1234]:8443/Příliš žluťoučký/kůň 🤍.jpg?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//uživatel@heslo:[2001:db8::1234]:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='', fragment='')  # noqa
        ),
        (
            '//uživatel@heslo:[2001:db8::1234]:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//uživatel@heslo:[2001:db8::1234]:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            '//uživatel@heslo:[2001:db8::1234]:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//uživatel@heslo:[2001:db8::1234]:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            '//uživatel@heslo:[2001:db8::1234]:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//uživatel@heslo:[2001:db8::1234]:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt',
            ParseResult(scheme='', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='', fragment='')  # noqa
        ),
        (
            '//uživatel@heslo:[2001:db8::1234]:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//uživatel@heslo:[2001:db8::1234]:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            '//uživatel@heslo:[2001:db8::1234]:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//uživatel@heslo:[2001:db8::1234]:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            '//uživatel@heslo:[2001:db8::1234]:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//uživatel@heslo:[2001:db8::1234]:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='', fragment='')  # noqa
        ),
        (
            '//uživatel@heslo:[2001:db8::1234]:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//uživatel@heslo:[2001:db8::1234]:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            '//uživatel@heslo:[2001:db8::1234]:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            '//uživatel@heslo:[2001:db8::1234]:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            '//uživatel@heslo:[2001:db8::1234]:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https:///',
            ParseResult(scheme='https', netloc='', path='/', params='', query='', fragment='')  # noqa
        ),
        (
            'https:///#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='', path='/', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https:///?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='https', netloc='', path='/', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'https:///?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='', path='/', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https:///?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='https', netloc='', path='/', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'https:///?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='', path='/', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https:///;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='https', netloc='', path='/', params='Příliš žluťoučký kůň=🤍', query='', fragment='')  # noqa
        ),
        (
            'https:///;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='', path='/', params='Příliš žluťoučký kůň=🤍', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https:///;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='https', netloc='', path='/', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'https:///;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='', path='/', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https:///;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='https', netloc='', path='/', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'https:///;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='', path='/', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https:///Příliš žluťoučký/kůň 🤍.jpg',
            ParseResult(scheme='https', netloc='', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='', fragment='')  # noqa
        ),
        (
            'https:///Příliš žluťoučký/kůň 🤍.jpg#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https:///Příliš žluťoučký/kůň 🤍.jpg?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='https', netloc='', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'https:///Příliš žluťoučký/kůň 🤍.jpg?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https:///Příliš žluťoučký/kůň 🤍.jpg?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='https', netloc='', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'https:///Příliš žluťoučký/kůň 🤍.jpg?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https:///Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='https', netloc='', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='', fragment='')  # noqa
        ),
        (
            'https:///Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https:///Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='https', netloc='', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'https:///Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https:///Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='https', netloc='', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'https:///Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https:///\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt',
            ParseResult(scheme='https', netloc='', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='', fragment='')  # noqa
        ),
        (
            'https:///\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https:///\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='https', netloc='', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'https:///\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https:///\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='https', netloc='', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'https:///\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https:///\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='https', netloc='', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='', fragment='')  # noqa
        ),
        (
            'https:///\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https:///\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='https', netloc='', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'https:///\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https:///\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='https', netloc='', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'https:///\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://www.example.org/',
            ParseResult(scheme='https', netloc='www.example.org', path='/', params='', query='', fragment='')  # noqa
        ),
        (
            'https://www.example.org/#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='www.example.org', path='/', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://www.example.org/?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='https', netloc='www.example.org', path='/', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'https://www.example.org/?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='www.example.org', path='/', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://www.example.org/?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='https', netloc='www.example.org', path='/', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'https://www.example.org/?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='www.example.org', path='/', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://www.example.org/;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='https', netloc='www.example.org', path='/', params='Příliš žluťoučký kůň=🤍', query='', fragment='')  # noqa
        ),
        (
            'https://www.example.org/;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='www.example.org', path='/', params='Příliš žluťoučký kůň=🤍', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://www.example.org/;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='https', netloc='www.example.org', path='/', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'https://www.example.org/;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='www.example.org', path='/', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://www.example.org/;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='https', netloc='www.example.org', path='/', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'https://www.example.org/;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='www.example.org', path='/', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://www.example.org/Příliš žluťoučký/kůň 🤍.jpg',
            ParseResult(scheme='https', netloc='www.example.org', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='', fragment='')  # noqa
        ),
        (
            'https://www.example.org/Příliš žluťoučký/kůň 🤍.jpg#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='www.example.org', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://www.example.org/Příliš žluťoučký/kůň 🤍.jpg?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='https', netloc='www.example.org', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'https://www.example.org/Příliš žluťoučký/kůň 🤍.jpg?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='www.example.org', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://www.example.org/Příliš žluťoučký/kůň 🤍.jpg?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='https', netloc='www.example.org', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'https://www.example.org/Příliš žluťoučký/kůň 🤍.jpg?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='www.example.org', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://www.example.org/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='https', netloc='www.example.org', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='', fragment='')  # noqa
        ),
        (
            'https://www.example.org/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='www.example.org', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://www.example.org/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='https', netloc='www.example.org', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'https://www.example.org/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='www.example.org', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://www.example.org/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='https', netloc='www.example.org', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'https://www.example.org/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='www.example.org', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://www.example.org/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt',
            ParseResult(scheme='https', netloc='www.example.org', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='', fragment='')  # noqa
        ),
        (
            'https://www.example.org/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='www.example.org', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://www.example.org/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='https', netloc='www.example.org', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'https://www.example.org/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='www.example.org', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://www.example.org/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='https', netloc='www.example.org', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'https://www.example.org/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='www.example.org', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://www.example.org/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='https', netloc='www.example.org', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='', fragment='')  # noqa
        ),
        (
            'https://www.example.org/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='www.example.org', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://www.example.org/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='https', netloc='www.example.org', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'https://www.example.org/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='www.example.org', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://www.example.org/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='https', netloc='www.example.org', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'https://www.example.org/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='www.example.org', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://user@pass:www.example.org:8443/',
            ParseResult(scheme='https', netloc='user@pass:www.example.org:8443', path='/', params='', query='', fragment='')  # noqa
        ),
        (
            'https://user@pass:www.example.org:8443/#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='user@pass:www.example.org:8443', path='/', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://user@pass:www.example.org:8443/?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='https', netloc='user@pass:www.example.org:8443', path='/', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'https://user@pass:www.example.org:8443/?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='user@pass:www.example.org:8443', path='/', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://user@pass:www.example.org:8443/?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='https', netloc='user@pass:www.example.org:8443', path='/', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'https://user@pass:www.example.org:8443/?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='user@pass:www.example.org:8443', path='/', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://user@pass:www.example.org:8443/;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='https', netloc='user@pass:www.example.org:8443', path='/', params='Příliš žluťoučký kůň=🤍', query='', fragment='')  # noqa
        ),
        (
            'https://user@pass:www.example.org:8443/;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='user@pass:www.example.org:8443', path='/', params='Příliš žluťoučký kůň=🤍', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://user@pass:www.example.org:8443/;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='https', netloc='user@pass:www.example.org:8443', path='/', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'https://user@pass:www.example.org:8443/;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='user@pass:www.example.org:8443', path='/', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://user@pass:www.example.org:8443/;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='https', netloc='user@pass:www.example.org:8443', path='/', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'https://user@pass:www.example.org:8443/;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='user@pass:www.example.org:8443', path='/', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://user@pass:www.example.org:8443/Příliš žluťoučký/kůň 🤍.jpg',
            ParseResult(scheme='https', netloc='user@pass:www.example.org:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='', fragment='')  # noqa
        ),
        (
            'https://user@pass:www.example.org:8443/Příliš žluťoučký/kůň 🤍.jpg#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='user@pass:www.example.org:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://user@pass:www.example.org:8443/Příliš žluťoučký/kůň 🤍.jpg?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='https', netloc='user@pass:www.example.org:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'https://user@pass:www.example.org:8443/Příliš žluťoučký/kůň 🤍.jpg?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='user@pass:www.example.org:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://user@pass:www.example.org:8443/Příliš žluťoučký/kůň 🤍.jpg?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='https', netloc='user@pass:www.example.org:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'https://user@pass:www.example.org:8443/Příliš žluťoučký/kůň 🤍.jpg?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='user@pass:www.example.org:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://user@pass:www.example.org:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='https', netloc='user@pass:www.example.org:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='', fragment='')  # noqa
        ),
        (
            'https://user@pass:www.example.org:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='user@pass:www.example.org:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://user@pass:www.example.org:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='https', netloc='user@pass:www.example.org:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'https://user@pass:www.example.org:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='user@pass:www.example.org:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://user@pass:www.example.org:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='https', netloc='user@pass:www.example.org:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'https://user@pass:www.example.org:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='user@pass:www.example.org:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://user@pass:www.example.org:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt',
            ParseResult(scheme='https', netloc='user@pass:www.example.org:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='', fragment='')  # noqa
        ),
        (
            'https://user@pass:www.example.org:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='user@pass:www.example.org:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://user@pass:www.example.org:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='https', netloc='user@pass:www.example.org:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'https://user@pass:www.example.org:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='user@pass:www.example.org:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://user@pass:www.example.org:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='https', netloc='user@pass:www.example.org:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'https://user@pass:www.example.org:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='user@pass:www.example.org:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://user@pass:www.example.org:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='https', netloc='user@pass:www.example.org:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='', fragment='')  # noqa
        ),
        (
            'https://user@pass:www.example.org:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='user@pass:www.example.org:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://user@pass:www.example.org:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='https', netloc='user@pass:www.example.org:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'https://user@pass:www.example.org:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='user@pass:www.example.org:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://user@pass:www.example.org:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='https', netloc='user@pass:www.example.org:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'https://user@pass:www.example.org:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='user@pass:www.example.org:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://uživatel@heslo:příklad.cz:8443/',
            ParseResult(scheme='https', netloc='uživatel@heslo:příklad.cz:8443', path='/', params='', query='', fragment='')  # noqa
        ),
        (
            'https://uživatel@heslo:příklad.cz:8443/#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:příklad.cz:8443', path='/', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://uživatel@heslo:příklad.cz:8443/?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:příklad.cz:8443', path='/', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'https://uživatel@heslo:příklad.cz:8443/?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:příklad.cz:8443', path='/', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://uživatel@heslo:příklad.cz:8443/?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='https', netloc='uživatel@heslo:příklad.cz:8443', path='/', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'https://uživatel@heslo:příklad.cz:8443/?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:příklad.cz:8443', path='/', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://uživatel@heslo:příklad.cz:8443/;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:příklad.cz:8443', path='/', params='Příliš žluťoučký kůň=🤍', query='', fragment='')  # noqa
        ),
        (
            'https://uživatel@heslo:příklad.cz:8443/;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:příklad.cz:8443', path='/', params='Příliš žluťoučký kůň=🤍', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://uživatel@heslo:příklad.cz:8443/;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:příklad.cz:8443', path='/', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'https://uživatel@heslo:příklad.cz:8443/;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:příklad.cz:8443', path='/', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://uživatel@heslo:příklad.cz:8443/;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='https', netloc='uživatel@heslo:příklad.cz:8443', path='/', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'https://uživatel@heslo:příklad.cz:8443/;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:příklad.cz:8443', path='/', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://uživatel@heslo:příklad.cz:8443/Příliš žluťoučký/kůň 🤍.jpg',
            ParseResult(scheme='https', netloc='uživatel@heslo:příklad.cz:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='', fragment='')  # noqa
        ),
        (
            'https://uživatel@heslo:příklad.cz:8443/Příliš žluťoučký/kůň 🤍.jpg#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:příklad.cz:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://uživatel@heslo:příklad.cz:8443/Příliš žluťoučký/kůň 🤍.jpg?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:příklad.cz:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'https://uživatel@heslo:příklad.cz:8443/Příliš žluťoučký/kůň 🤍.jpg?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:příklad.cz:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://uživatel@heslo:příklad.cz:8443/Příliš žluťoučký/kůň 🤍.jpg?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='https', netloc='uživatel@heslo:příklad.cz:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'https://uživatel@heslo:příklad.cz:8443/Příliš žluťoučký/kůň 🤍.jpg?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:příklad.cz:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://uživatel@heslo:příklad.cz:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:příklad.cz:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='', fragment='')  # noqa
        ),
        (
            'https://uživatel@heslo:příklad.cz:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:příklad.cz:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://uživatel@heslo:příklad.cz:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:příklad.cz:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'https://uživatel@heslo:příklad.cz:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:příklad.cz:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://uživatel@heslo:příklad.cz:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='https', netloc='uživatel@heslo:příklad.cz:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'https://uživatel@heslo:příklad.cz:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:příklad.cz:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://uživatel@heslo:příklad.cz:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt',
            ParseResult(scheme='https', netloc='uživatel@heslo:příklad.cz:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='', fragment='')  # noqa
        ),
        (
            'https://uživatel@heslo:příklad.cz:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:příklad.cz:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://uživatel@heslo:příklad.cz:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:příklad.cz:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'https://uživatel@heslo:příklad.cz:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:příklad.cz:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://uživatel@heslo:příklad.cz:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='https', netloc='uživatel@heslo:příklad.cz:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'https://uživatel@heslo:příklad.cz:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:příklad.cz:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://uživatel@heslo:příklad.cz:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:příklad.cz:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='', fragment='')  # noqa
        ),
        (
            'https://uživatel@heslo:příklad.cz:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:příklad.cz:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://uživatel@heslo:příklad.cz:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:příklad.cz:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'https://uživatel@heslo:příklad.cz:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:příklad.cz:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://uživatel@heslo:příklad.cz:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='https', netloc='uživatel@heslo:příklad.cz:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'https://uživatel@heslo:příklad.cz:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:příklad.cz:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://uživatel@heslo:[2001:db8::1234]:8443/',
            ParseResult(scheme='https', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/', params='', query='', fragment='')  # noqa
        ),
        (
            'https://uživatel@heslo:[2001:db8::1234]:8443/#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://uživatel@heslo:[2001:db8::1234]:8443/?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'https://uživatel@heslo:[2001:db8::1234]:8443/?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://uživatel@heslo:[2001:db8::1234]:8443/?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='https', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'https://uživatel@heslo:[2001:db8::1234]:8443/?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://uživatel@heslo:[2001:db8::1234]:8443/;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/', params='Příliš žluťoučký kůň=🤍', query='', fragment='')  # noqa
        ),
        (
            'https://uživatel@heslo:[2001:db8::1234]:8443/;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/', params='Příliš žluťoučký kůň=🤍', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://uživatel@heslo:[2001:db8::1234]:8443/;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'https://uživatel@heslo:[2001:db8::1234]:8443/;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://uživatel@heslo:[2001:db8::1234]:8443/;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='https', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'https://uživatel@heslo:[2001:db8::1234]:8443/;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://uživatel@heslo:[2001:db8::1234]:8443/Příliš žluťoučký/kůň 🤍.jpg',
            ParseResult(scheme='https', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='', fragment='')  # noqa
        ),
        (
            'https://uživatel@heslo:[2001:db8::1234]:8443/Příliš žluťoučký/kůň 🤍.jpg#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://uživatel@heslo:[2001:db8::1234]:8443/Příliš žluťoučký/kůň 🤍.jpg?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'https://uživatel@heslo:[2001:db8::1234]:8443/Příliš žluťoučký/kůň 🤍.jpg?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://uživatel@heslo:[2001:db8::1234]:8443/Příliš žluťoučký/kůň 🤍.jpg?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='https', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'https://uživatel@heslo:[2001:db8::1234]:8443/Příliš žluťoučký/kůň 🤍.jpg?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://uživatel@heslo:[2001:db8::1234]:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='', fragment='')  # noqa
        ),
        (
            'https://uživatel@heslo:[2001:db8::1234]:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://uživatel@heslo:[2001:db8::1234]:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'https://uživatel@heslo:[2001:db8::1234]:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://uživatel@heslo:[2001:db8::1234]:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='https', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'https://uživatel@heslo:[2001:db8::1234]:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://uživatel@heslo:[2001:db8::1234]:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt',
            ParseResult(scheme='https', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='', fragment='')  # noqa
        ),
        (
            'https://uživatel@heslo:[2001:db8::1234]:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://uživatel@heslo:[2001:db8::1234]:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'https://uživatel@heslo:[2001:db8::1234]:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://uživatel@heslo:[2001:db8::1234]:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='https', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'https://uživatel@heslo:[2001:db8::1234]:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://uživatel@heslo:[2001:db8::1234]:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='', fragment='')  # noqa
        ),
        (
            'https://uživatel@heslo:[2001:db8::1234]:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://uživatel@heslo:[2001:db8::1234]:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'https://uživatel@heslo:[2001:db8::1234]:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'https://uživatel@heslo:[2001:db8::1234]:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='https', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'https://uživatel@heslo:[2001:db8::1234]:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='https', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='Příliš žluťoučký kůň=🤍', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto:/',
            ParseResult(scheme='invalidproto', netloc='', path='/', params='', query='', fragment='')  # noqa
        ),
        (
            'invalidproto:/#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='', path='/', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto:/?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='invalidproto', netloc='', path='/', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'invalidproto:/?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='', path='/', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto:/?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='invalidproto', netloc='', path='/', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'invalidproto:/?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='', path='/', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto:/;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='invalidproto', netloc='', path='/;Příliš žluťoučký kůň=🤍', params='', query='', fragment='')  # noqa
        ),
        (
            'invalidproto:/;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='', path='/;Příliš žluťoučký kůň=🤍', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto:/;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='invalidproto', netloc='', path='/;Příliš žluťoučký kůň=🤍', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'invalidproto:/;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='', path='/;Příliš žluťoučký kůň=🤍', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto:/;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='invalidproto', netloc='', path='/;Příliš žluťoučký kůň=🤍', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'invalidproto:/;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='', path='/;Příliš žluťoučký kůň=🤍', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto:/Příliš žluťoučký/kůň 🤍.jpg',
            ParseResult(scheme='invalidproto', netloc='', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='', fragment='')  # noqa
        ),
        (
            'invalidproto:/Příliš žluťoučký/kůň 🤍.jpg#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto:/Příliš žluťoučký/kůň 🤍.jpg?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='invalidproto', netloc='', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'invalidproto:/Příliš žluťoučký/kůň 🤍.jpg?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto:/Příliš žluťoučký/kůň 🤍.jpg?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='invalidproto', netloc='', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'invalidproto:/Příliš žluťoučký/kůň 🤍.jpg?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto:/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='invalidproto', netloc='', path='/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍', params='', query='', fragment='')  # noqa
        ),
        (
            'invalidproto:/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='', path='/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto:/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='invalidproto', netloc='', path='/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'invalidproto:/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='', path='/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto:/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='invalidproto', netloc='', path='/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'invalidproto:/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='', path='/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto:/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt',
            ParseResult(scheme='invalidproto', netloc='', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='', fragment='')  # noqa
        ),
        (
            'invalidproto:/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto:/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='invalidproto', netloc='', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'invalidproto:/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto:/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='invalidproto', netloc='', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'invalidproto:/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto:/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='invalidproto', netloc='', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍', params='', query='', fragment='')  # noqa
        ),
        (
            'invalidproto:/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto:/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='invalidproto', netloc='', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'invalidproto:/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto:/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='invalidproto', netloc='', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'invalidproto:/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://www.example.org/',
            ParseResult(scheme='invalidproto', netloc='www.example.org', path='/', params='', query='', fragment='')  # noqa
        ),
        (
            'invalidproto://www.example.org/#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='www.example.org', path='/', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://www.example.org/?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='invalidproto', netloc='www.example.org', path='/', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'invalidproto://www.example.org/?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='www.example.org', path='/', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://www.example.org/?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='invalidproto', netloc='www.example.org', path='/', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'invalidproto://www.example.org/?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='www.example.org', path='/', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://www.example.org/;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='invalidproto', netloc='www.example.org', path='/;Příliš žluťoučký kůň=🤍', params='', query='', fragment='')  # noqa
        ),
        (
            'invalidproto://www.example.org/;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='www.example.org', path='/;Příliš žluťoučký kůň=🤍', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://www.example.org/;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='invalidproto', netloc='www.example.org', path='/;Příliš žluťoučký kůň=🤍', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'invalidproto://www.example.org/;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='www.example.org', path='/;Příliš žluťoučký kůň=🤍', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://www.example.org/;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='invalidproto', netloc='www.example.org', path='/;Příliš žluťoučký kůň=🤍', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'invalidproto://www.example.org/;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='www.example.org', path='/;Příliš žluťoučký kůň=🤍', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://www.example.org/Příliš žluťoučký/kůň 🤍.jpg',
            ParseResult(scheme='invalidproto', netloc='www.example.org', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='', fragment='')  # noqa
        ),
        (
            'invalidproto://www.example.org/Příliš žluťoučký/kůň 🤍.jpg#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='www.example.org', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://www.example.org/Příliš žluťoučký/kůň 🤍.jpg?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='invalidproto', netloc='www.example.org', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'invalidproto://www.example.org/Příliš žluťoučký/kůň 🤍.jpg?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='www.example.org', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://www.example.org/Příliš žluťoučký/kůň 🤍.jpg?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='invalidproto', netloc='www.example.org', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'invalidproto://www.example.org/Příliš žluťoučký/kůň 🤍.jpg?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='www.example.org', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://www.example.org/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='invalidproto', netloc='www.example.org', path='/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍', params='', query='', fragment='')  # noqa
        ),
        (
            'invalidproto://www.example.org/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='www.example.org', path='/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://www.example.org/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='invalidproto', netloc='www.example.org', path='/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'invalidproto://www.example.org/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='www.example.org', path='/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://www.example.org/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='invalidproto', netloc='www.example.org', path='/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'invalidproto://www.example.org/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='www.example.org', path='/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://www.example.org/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt',
            ParseResult(scheme='invalidproto', netloc='www.example.org', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='', fragment='')  # noqa
        ),
        (
            'invalidproto://www.example.org/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='www.example.org', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://www.example.org/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='invalidproto', netloc='www.example.org', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'invalidproto://www.example.org/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='www.example.org', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://www.example.org/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='invalidproto', netloc='www.example.org', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'invalidproto://www.example.org/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='www.example.org', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://www.example.org/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='invalidproto', netloc='www.example.org', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍', params='', query='', fragment='')  # noqa
        ),
        (
            'invalidproto://www.example.org/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='www.example.org', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://www.example.org/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='invalidproto', netloc='www.example.org', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'invalidproto://www.example.org/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='www.example.org', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://www.example.org/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='invalidproto', netloc='www.example.org', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'invalidproto://www.example.org/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='www.example.org', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://user@pass:www.example.org:8443/',
            ParseResult(scheme='invalidproto', netloc='user@pass:www.example.org:8443', path='/', params='', query='', fragment='')  # noqa
        ),
        (
            'invalidproto://user@pass:www.example.org:8443/#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='user@pass:www.example.org:8443', path='/', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://user@pass:www.example.org:8443/?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='invalidproto', netloc='user@pass:www.example.org:8443', path='/', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'invalidproto://user@pass:www.example.org:8443/?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='user@pass:www.example.org:8443', path='/', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://user@pass:www.example.org:8443/?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='invalidproto', netloc='user@pass:www.example.org:8443', path='/', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'invalidproto://user@pass:www.example.org:8443/?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='user@pass:www.example.org:8443', path='/', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://user@pass:www.example.org:8443/;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='invalidproto', netloc='user@pass:www.example.org:8443', path='/;Příliš žluťoučký kůň=🤍', params='', query='', fragment='')  # noqa
        ),
        (
            'invalidproto://user@pass:www.example.org:8443/;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='user@pass:www.example.org:8443', path='/;Příliš žluťoučký kůň=🤍', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://user@pass:www.example.org:8443/;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='invalidproto', netloc='user@pass:www.example.org:8443', path='/;Příliš žluťoučký kůň=🤍', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'invalidproto://user@pass:www.example.org:8443/;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='user@pass:www.example.org:8443', path='/;Příliš žluťoučký kůň=🤍', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://user@pass:www.example.org:8443/;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='invalidproto', netloc='user@pass:www.example.org:8443', path='/;Příliš žluťoučký kůň=🤍', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'invalidproto://user@pass:www.example.org:8443/;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='user@pass:www.example.org:8443', path='/;Příliš žluťoučký kůň=🤍', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://user@pass:www.example.org:8443/Příliš žluťoučký/kůň 🤍.jpg',
            ParseResult(scheme='invalidproto', netloc='user@pass:www.example.org:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='', fragment='')  # noqa
        ),
        (
            'invalidproto://user@pass:www.example.org:8443/Příliš žluťoučký/kůň 🤍.jpg#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='user@pass:www.example.org:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://user@pass:www.example.org:8443/Příliš žluťoučký/kůň 🤍.jpg?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='invalidproto', netloc='user@pass:www.example.org:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'invalidproto://user@pass:www.example.org:8443/Příliš žluťoučký/kůň 🤍.jpg?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='user@pass:www.example.org:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://user@pass:www.example.org:8443/Příliš žluťoučký/kůň 🤍.jpg?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='invalidproto', netloc='user@pass:www.example.org:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'invalidproto://user@pass:www.example.org:8443/Příliš žluťoučký/kůň 🤍.jpg?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='user@pass:www.example.org:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://user@pass:www.example.org:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='invalidproto', netloc='user@pass:www.example.org:8443', path='/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍', params='', query='', fragment='')  # noqa
        ),
        (
            'invalidproto://user@pass:www.example.org:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='user@pass:www.example.org:8443', path='/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://user@pass:www.example.org:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='invalidproto', netloc='user@pass:www.example.org:8443', path='/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'invalidproto://user@pass:www.example.org:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='user@pass:www.example.org:8443', path='/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://user@pass:www.example.org:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='invalidproto', netloc='user@pass:www.example.org:8443', path='/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'invalidproto://user@pass:www.example.org:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='user@pass:www.example.org:8443', path='/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://user@pass:www.example.org:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt',
            ParseResult(scheme='invalidproto', netloc='user@pass:www.example.org:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='', fragment='')  # noqa
        ),
        (
            'invalidproto://user@pass:www.example.org:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='user@pass:www.example.org:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://user@pass:www.example.org:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='invalidproto', netloc='user@pass:www.example.org:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'invalidproto://user@pass:www.example.org:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='user@pass:www.example.org:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://user@pass:www.example.org:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='invalidproto', netloc='user@pass:www.example.org:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'invalidproto://user@pass:www.example.org:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='user@pass:www.example.org:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://user@pass:www.example.org:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='invalidproto', netloc='user@pass:www.example.org:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍', params='', query='', fragment='')  # noqa
        ),
        (
            'invalidproto://user@pass:www.example.org:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='user@pass:www.example.org:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://user@pass:www.example.org:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='invalidproto', netloc='user@pass:www.example.org:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'invalidproto://user@pass:www.example.org:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='user@pass:www.example.org:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://user@pass:www.example.org:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='invalidproto', netloc='user@pass:www.example.org:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'invalidproto://user@pass:www.example.org:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='user@pass:www.example.org:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:příklad.cz:8443/',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:příklad.cz:8443', path='/', params='', query='', fragment='')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:příklad.cz:8443/#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:příklad.cz:8443', path='/', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:příklad.cz:8443/?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:příklad.cz:8443', path='/', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:příklad.cz:8443/?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:příklad.cz:8443', path='/', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:příklad.cz:8443/?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:příklad.cz:8443', path='/', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:příklad.cz:8443/?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:příklad.cz:8443', path='/', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:příklad.cz:8443/;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:příklad.cz:8443', path='/;Příliš žluťoučký kůň=🤍', params='', query='', fragment='')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:příklad.cz:8443/;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:příklad.cz:8443', path='/;Příliš žluťoučký kůň=🤍', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:příklad.cz:8443/;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:příklad.cz:8443', path='/;Příliš žluťoučký kůň=🤍', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:příklad.cz:8443/;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:příklad.cz:8443', path='/;Příliš žluťoučký kůň=🤍', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:příklad.cz:8443/;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:příklad.cz:8443', path='/;Příliš žluťoučký kůň=🤍', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:příklad.cz:8443/;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:příklad.cz:8443', path='/;Příliš žluťoučký kůň=🤍', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:příklad.cz:8443/Příliš žluťoučký/kůň 🤍.jpg',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:příklad.cz:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='', fragment='')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:příklad.cz:8443/Příliš žluťoučký/kůň 🤍.jpg#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:příklad.cz:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:příklad.cz:8443/Příliš žluťoučký/kůň 🤍.jpg?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:příklad.cz:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:příklad.cz:8443/Příliš žluťoučký/kůň 🤍.jpg?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:příklad.cz:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:příklad.cz:8443/Příliš žluťoučký/kůň 🤍.jpg?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:příklad.cz:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:příklad.cz:8443/Příliš žluťoučký/kůň 🤍.jpg?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:příklad.cz:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:příklad.cz:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:příklad.cz:8443', path='/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍', params='', query='', fragment='')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:příklad.cz:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:příklad.cz:8443', path='/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:příklad.cz:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:příklad.cz:8443', path='/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:příklad.cz:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:příklad.cz:8443', path='/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:příklad.cz:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:příklad.cz:8443', path='/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:příklad.cz:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:příklad.cz:8443', path='/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:příklad.cz:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:příklad.cz:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='', fragment='')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:příklad.cz:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:příklad.cz:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:příklad.cz:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:příklad.cz:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:příklad.cz:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:příklad.cz:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:příklad.cz:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:příklad.cz:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:příklad.cz:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:příklad.cz:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:příklad.cz:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:příklad.cz:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍', params='', query='', fragment='')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:příklad.cz:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:příklad.cz:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:příklad.cz:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:příklad.cz:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:příklad.cz:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:příklad.cz:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:příklad.cz:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:příklad.cz:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:příklad.cz:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:příklad.cz:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:[2001:db8::1234]:8443/',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/', params='', query='', fragment='')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:[2001:db8::1234]:8443/#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:[2001:db8::1234]:8443/?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:[2001:db8::1234]:8443/?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:[2001:db8::1234]:8443/?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:[2001:db8::1234]:8443/?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:[2001:db8::1234]:8443/;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/;Příliš žluťoučký kůň=🤍', params='', query='', fragment='')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:[2001:db8::1234]:8443/;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/;Příliš žluťoučký kůň=🤍', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:[2001:db8::1234]:8443/;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/;Příliš žluťoučký kůň=🤍', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:[2001:db8::1234]:8443/;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/;Příliš žluťoučký kůň=🤍', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:[2001:db8::1234]:8443/;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/;Příliš žluťoučký kůň=🤍', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:[2001:db8::1234]:8443/;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/;Příliš žluťoučký kůň=🤍', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:[2001:db8::1234]:8443/Příliš žluťoučký/kůň 🤍.jpg',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='', fragment='')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:[2001:db8::1234]:8443/Příliš žluťoučký/kůň 🤍.jpg#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:[2001:db8::1234]:8443/Příliš žluťoučký/kůň 🤍.jpg?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:[2001:db8::1234]:8443/Příliš žluťoučký/kůň 🤍.jpg?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:[2001:db8::1234]:8443/Příliš žluťoučký/kůň 🤍.jpg?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:[2001:db8::1234]:8443/Příliš žluťoučký/kůň 🤍.jpg?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/Příliš žluťoučký/kůň 🤍.jpg', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:[2001:db8::1234]:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍', params='', query='', fragment='')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:[2001:db8::1234]:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:[2001:db8::1234]:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:[2001:db8::1234]:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:[2001:db8::1234]:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:[2001:db8::1234]:8443/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/Příliš žluťoučký/kůň 🤍.jpg;Příliš žluťoučký kůň=🤍', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:[2001:db8::1234]:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='', fragment='')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:[2001:db8::1234]:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:[2001:db8::1234]:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:[2001:db8::1234]:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:[2001:db8::1234]:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:[2001:db8::1234]:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:[2001:db8::1234]:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍', params='', query='', fragment='')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:[2001:db8::1234]:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍', params='', query='', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:[2001:db8::1234]:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:[2001:db8::1234]:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍', params='', query='abc=def&možnost=Příliš žluťoučký kůň&další možnost=🤍', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:[2001:db8::1234]:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='')  # noqa
        ),
        (
            'invalidproto://uživatel@heslo:[2001:db8::1234]:8443/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍?test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test#Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍',
            ParseResult(scheme='invalidproto', netloc='uživatel@heslo:[2001:db8::1234]:8443', path='/\ufffftest/somedir\u202f\u2029abc/\r\nsome \x00\t  file.txt;Příliš žluťoučký kůň=🤍', params='', query='test=test\x00abc&speciální=abc\uffff\u2028\r\n\t  \u202f\x01test', fragment='Příliš\r\n\x01\x00 žluťoučký\uffff kůň 🤍')  # noqa
        ),
        # The previous entry is the last auto-generated test case.
        (
            "https://www.example.com/dir/test.txt?abc=def&xyz=123#part",
            ParseResult(scheme="https", netloc="www.example.com", path="/dir/test.txt", params="", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "www.example.com/dir/test.txt?abc=def&xyz=123#parthttps://",
            ParseResult(scheme="", netloc="", path="www.example.com/dir/test.txt", params="", query="abc=def&xyz=123", fragment="parthttps://")  # noqa
        ),
        (
            "/dir/test.txt?abc=def&xyz=123#parthttps://www.example.com",
            ParseResult(scheme="", netloc="", path="/dir/test.txt", params="", query="abc=def&xyz=123", fragment="parthttps://www.example.com")  # noqa
        ),
        (
            "?abc=def&xyz=123#parthttps://www.example.com/dir/test.txt",
            ParseResult(scheme="", netloc="", path="", params="", query="abc=def&xyz=123", fragment="parthttps://www.example.com/dir/test.txt")  # noqa
        ),
        (
            "#parthttps://www.example.com/dir/test.txt?abc=def&xyz=123",
            ParseResult(scheme="", netloc="", path="", params="", query="", fragment="parthttps://www.example.com/dir/test.txt?abc=def&xyz=123")  # noqa
        ),
        (
            "https://www.example.com/dir/test.txt?abc=def&xyz=123#part#",
            ParseResult(scheme="https", netloc="www.example.com", path="/dir/test.txt", params="", query="abc=def&xyz=123", fragment="part#")  # noqa
        ),
        (
            "https://www.example.com/dir/test.txt?abc=def&xyz=123#part#abc",
            ParseResult(scheme="https", netloc="www.example.com", path="/dir/test.txt", params="", query="abc=def&xyz=123", fragment="part#abc")  # noqa
        ),
        (
            "https://www.example.com/dir/test.txt?abc=def?xyz=123#part",
            ParseResult(scheme="https", netloc="www.example.com", path="/dir/test.txt", params="", query="abc=def?xyz=123", fragment="part")  # noqa
        ),
        (
            "https://www.example.com//dir/test.txt?abc=def&xyz=123#part",
            ParseResult(scheme="https", netloc="www.example.com", path="//dir/test.txt", params="", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "https://www.example.com/dir///test.txt?abc=def&xyz=123#part",
            ParseResult(scheme="https", netloc="www.example.com", path="/dir///test.txt", params="", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "https:///www.example.com/dir/test.txt?abc=def&xyz=123#part",
            ParseResult(scheme="https", netloc="", path="/www.example.com/dir/test.txt", params="", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "https:////www.example.com/dir/test.txt?abc=def&xyz=123#part",
            ParseResult(scheme="https", netloc="", path="//www.example.com/dir/test.txt", params="", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "https//www.example.com/dir/test.txt?abc=def&xyz=123#part",
            ParseResult(scheme="", netloc="", path="https//www.example.com/dir/test.txt", params="", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "https://www.example.com/dir/test.txt??abc=def&xyz=123#part",
            ParseResult(scheme="https", netloc="www.example.com", path="/dir/test.txt", params="", query="?abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "https://www.example.com/dir/test.txt?abc=def&xyz=123##part",
            ParseResult(scheme="https", netloc="www.example.com", path="/dir/test.txt", params="", query="abc=def&xyz=123", fragment="#part")  # noqa
        ),
        (
            "https:://www.example.com/dir/test.txt?abc=def&xyz=123#part",
            ParseResult(scheme="https", netloc="", path="://www.example.com/dir/test.txt", params="", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "http\x00s://www.example.com/dir/test.txt?abc=def&xyz=123#part",
            ParseResult(scheme="", netloc="", path="http\x00s://www.example.com/dir/test.txt", params="", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "https://www.e\x00xample.com/dir/test.txt?abc=def&xyz=123#part",
            ParseResult(scheme="https", netloc="www.e\x00xample.com", path="/dir/test.txt", params="", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "https://www.example.com/d\x00ir/test.txt?abc=def&xyz=123#part",
            ParseResult(scheme="https", netloc="www.example.com", path="/d\x00ir/test.txt", params="", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "https://www.example.com/dir/test.txt?abc=de\x00f&xyz=123#part",
            ParseResult(scheme="https", netloc="www.example.com", path="/dir/test.txt", params="", query="abc=de\x00f&xyz=123", fragment="part")  # noqa
        ),
        (
            "https://www.example.com/dir/test.txt?abc=def&xyz=123#pa\x00rt",
            ParseResult(scheme="https", netloc="www.example.com", path="/dir/test.txt", params="", query="abc=def&xyz=123", fragment="pa\x00rt")  # noqa
        ),
        (
            "https://www.example.com/dir/test.txt;key=value?abc=def&xyz=123#part",
            ParseResult(scheme="https", netloc="www.example.com", path="/dir/test.txt", params="key=value", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "https://www.example.com/dir/test.txt;;key=value?abc=def&xyz=123#part",
            ParseResult(scheme="https", netloc="www.example.com", path="/dir/test.txt", params=";key=value", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "https://www.example.com/dir/test.txt;key==value?abc=def&xyz=123#part",
            ParseResult(scheme="https", netloc="www.example.com", path="/dir/test.txt", params="key==value", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "https://www.example.com/dir/test.txt;ke\x00y=value?abc=def&xyz=123#part",
            ParseResult(scheme="https", netloc="www.example.com", path="/dir/test.txt", params="ke\x00y=value", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "https://user@pass:www.example.com:8443/dir/test.txt;key=value?abc=def&xyz=123#part",
            ParseResult(scheme="https", netloc="user@pass:www.example.com:8443", path="/dir/test.txt", params="key=value", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "https://user@@pass:www.example.com:8443/dir/test.txt;key=value?abc=def&xyz=123#part",
            ParseResult(scheme="https", netloc="user@@pass:www.example.com:8443", path="/dir/test.txt", params="key=value", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "https://user@pass::www.example.com:8443/dir/test.txt;key=value?abc=def&xyz=123#part",
            ParseResult(scheme="https", netloc="user@pass::www.example.com:8443", path="/dir/test.txt", params="key=value", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "https://user@pass:www.example.com::8443/dir/test.txt;key=value?abc=def&xyz=123#part",
            ParseResult(scheme="https", netloc="user@pass:www.example.com::8443", path="/dir/test.txt", params="key=value", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "https://user@pass:www.exam:ple.com:8443/dir/test.txt;key=value?abc=def&xyz=123#part",
            ParseResult(scheme="https", netloc="user@pass:www.exam:ple.com:8443", path="/dir/test.txt", params="key=value", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "https://user@pass:www.example.com:88443/dir/test.txt;key=value?abc=def&xyz=123#part",
            ParseResult(scheme="https", netloc="user@pass:www.example.com:88443", path="/dir/test.txt", params="key=value", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "https://user@pass:www.example.com:https/dir/test.txt;key=value?abc=def&xyz=123#part",
            ParseResult(scheme="https", netloc="user@pass:www.example.com:https", path="/dir/test.txt", params="key=value", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "https://user@pass:www.example.com:invalidport/dir/test.txt;key=value?abc=def&xyz=123#part",
            ParseResult(scheme="https", netloc="user@pass:www.example.com:invalidport", path="/dir/test.txt", params="key=value", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "https://user@pa@ss:www.example.com:8443/dir/test.txt;key=value?abc=def&xyz=123#part",
            ParseResult(scheme="https", netloc="user@pa@ss:www.example.com:8443", path="/dir/test.txt", params="key=value", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "https://us\x00er@pass:www.example.com:8443/dir/test.txt;key=value?abc=def&xyz=123#part",
            ParseResult(scheme="https", netloc="us\x00er@pass:www.example.com:8443", path="/dir/test.txt", params="key=value", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "https://user@pa\x00ss:www.example.com:8443/dir/test.txt;key=value?abc=def&xyz=123#part",
            ParseResult(scheme="https", netloc="user@pa\x00ss:www.example.com:8443", path="/dir/test.txt", params="key=value", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "https://user@pass:www.example.com:84\x0043/dir/test.txt;key=value?abc=def&xyz=123#part",
            ParseResult(scheme="https", netloc="user@pass:www.example.com:84\x0043", path="/dir/test.txt", params="key=value", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "https://user\x00pass:www.example.com:8443/dir/test.txt;key=value?abc=def&xyz=123#part",
            ParseResult(scheme="https", netloc="user\x00pass:www.example.com:8443", path="/dir/test.txt", params="key=value", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "https://user@pass\x00www.example.com:8443/dir/test.txt;key=value?abc=def&xyz=123#part",
            ParseResult(scheme="https", netloc="user@pass\x00www.example.com:8443", path="/dir/test.txt", params="key=value", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "https://user@pass:www.example.com\x008443/dir/test.txt;key=value?abc=def&xyz=123#part",
            ParseResult(scheme="https", netloc="user@pass:www.example.com\x008443", path="/dir/test.txt", params="key=value", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "https://user@pass:www.exam\uffffple.com:8443/dir/test.txt;key=value?abc=def&xyz=123#part",
            ParseResult(scheme="https", netloc="user@pass:www.exam\uffffple.com:8443", path="/dir/test.txt", params="key=value", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "https://user@pass:www.ｅｘａｍｐｌｅ.com:8443/dir/test.txt;key=value?abc=def&xyz=123#part",
            ParseResult(scheme="https", netloc="user@pass:www.ｅｘａｍｐｌｅ.com:8443", path="/dir/test.txt", params="key=value", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "https://user@pass:www.éxámple.com:8443/dir/test.txt;key=value?abc=def&xyz=123#part",
            ParseResult(scheme="https", netloc="user@pass:www.éxámple.com:8443", path="/dir/test.txt", params="key=value", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "https://user@pass:www.éxámple.com:8443/dir/test.txt;key=value?abc=def&xyz=123#part",
            ParseResult(scheme="https", netloc="user@pass:www.éxámple.com:8443", path="/dir/test.txt", params="key=value", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "https://user@pass:www.\u30d5\u309a.com:8443/dir/test.txt;key=value?abc=def&xyz=123#part",
            ParseResult(scheme="https", netloc="user@pass:www.\u30d5\u309a.com:8443", path="/dir/test.txt", params="key=value", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "https://user@pass：www.example.com:8443/dir/test.txt;key=value?abc=def&xyz=123#part",
            InputDataNotConvertibleExc
        ),
        (
            "https://user＠pass:www.example.com:8443/dir/test.txt;key=value?abc=def&xyz=123#part",
            InputDataNotConvertibleExc
        ),
        (
            "https://user@pass:[2001:db8::1234]:8443/dir/test.txt;key=value?abc=def&xyz=123#part",
            ParseResult(scheme="https", netloc="user@pass:[2001:db8::1234]:8443", path="/dir/test.txt", params="key=value", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "https://user@pass:[2001:db8\x00::1234]:8443/dir/test.txt;key=value?abc=def&xyz=123#part",
            ParseResult(scheme="https", netloc="user@pass:[2001:db8\x00::1234]:8443", path="/dir/test.txt", params="key=value", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "https://user@pass:[2001:db8š::1234]:8443/dir/test.txt;key=value?abc=def&xyz=123#part",
            ParseResult(scheme="https", netloc="user@pass:[2001:db8š::1234]:8443", path="/dir/test.txt", params="key=value", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "https://user@pass:[2001:db8:1234]:8443/dir/test.txt;key=value?abc=def&xyz=123#part",
            ParseResult(scheme="https", netloc="user@pass:[2001:db8:1234]:8443", path="/dir/test.txt", params="key=value", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "https://user@pass:[2001:db8!::1234]:8443/dir/test.txt;key=value?abc=def&xyz=123#part",
            ParseResult(scheme="https", netloc="user@pass:[2001:db8!::1234]:8443", path="/dir/test.txt", params="key=value", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "https://user@pass:[[2001:db8::1234]:8443/dir/test.txt;key=value?abc=def&xyz=123#part",
            ParseResult(scheme="https", netloc="user@pass:[[2001:db8::1234]:8443", path="/dir/test.txt", params="key=value", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "https://user@pass:[2001:db8::1234]]:8443/dir/test.txt;key=value?abc=def&xyz=123#part",
            ParseResult(scheme="https", netloc="user@pass:[2001:db8::1234]]:8443", path="/dir/test.txt", params="key=value", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "https://user@pass:[[2001:db8::1234]]:8443/dir/test.txt;key=value?abc=def&xyz=123#part",
            ParseResult(scheme="https", netloc="user@pass:[[2001:db8::1234]]:8443", path="/dir/test.txt", params="key=value", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "https://user@pass:[\x002001:db8::1234]:8443/dir/test.txt;key=value?abc=def&xyz=123#part",
            ParseResult(scheme="https", netloc="user@pass:[\x002001:db8::1234]:8443", path="/dir/test.txt", params="key=value", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "https://user@pass:[2001:db8::1234\x00]:8443/dir/test.txt;key=value?abc=def&xyz=123#part",
            ParseResult(scheme="https", netloc="user@pass:[2001:db8::1234\x00]:8443", path="/dir/test.txt", params="key=value", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "https://user@pass:[\x002001:db8::1234\x00]:8443/dir/test.txt;key=value?abc=def&xyz=123#part",
            ParseResult(scheme="https", netloc="user@pass:[\x002001:db8::1234\x00]:8443", path="/dir/test.txt", params="key=value", query="abc=def&xyz=123", fragment="part")  # noqa
        ),
        (
            "https://user@pass:[2001:db8::1234:8443/dir/test.txt;key=value?abc=def&xyz=123#part",
            InputDataNotConvertibleExc
        ),
        (
            "https://user@pass:2001:db8::1234]:8443/dir/test.txt;key=value?abc=def&xyz=123#part",
            InputDataNotConvertibleExc
        ),
        (
            "https://user@pass:[2001:db8::1234\x00:8443/dir/test.txt;key=value?abc=def&xyz=123#part",
            InputDataNotConvertibleExc
        ),
        (
            "https://user@pass:\x002001:db8::1234]:8443/dir/test.txt;key=value?abc=def&xyz=123#part",
            InputDataNotConvertibleExc
        ),
        (
            "",
            ParseResult(scheme="", netloc="", path="", params="", query="", fragment="")  # noqa
        ),
        (
            "\x00",
            ParseResult(scheme="", netloc="", path="\x00", params="", query="", fragment="")  # noqa
        ),
        (
            "hello",
            ParseResult(scheme="", netloc="", path="hello", params="", query="", fragment="")  # noqa
        ),
        (
            "žluťoučký kůň",
            ParseResult(scheme="", netloc="", path="žluťoučký kůň", params="", query="", fragment="")  # noqa
        ),
        (
            "🤍",
            ParseResult(scheme="", netloc="", path="🤍", params="", query="", fragment="")  # noqa
        ),
        (
            "\r\n\t\v\f\x85  \n\r   žlu \n\x01\x02\x1d\x1eťoučký\r \u2028\u2029\u202fkůň 🤍 \u2060\uffff\ufffe\x00\a\b",
            ParseResult(scheme="", netloc="", path="žlu \n\x01\x02\x1d\x1eťoučký\r \u2028\u2029\u202fkůň 🤍 \u2060\uffff\ufffe\x00\a\b", params="", query="", fragment="")  # noqa
        ),
        (
            "\r\n\t\f\v    https://www.example.com/dir/test.html?abc=def&xyz=123#frag  \u2028\u2029\x1c\x1d\x1e      \t  ",
            ParseResult(scheme="https", netloc="www.example.com", path="/dir/test.html", params="", query="abc=def&xyz=123", fragment="frag")  # noqa
        ),
        (
            "\r\n\t\f\v    https://user@pass:www.example.com:8443/dir/test.html?abc=def&xyz=123#frag  \u2028\u2029\x1c\x1d\x1e      \t  ",
            ParseResult(scheme="https", netloc="user@pass:www.example.com:8443", path="/dir/test.html", params="", query="abc=def&xyz=123", fragment="frag")  # noqa
        ),
        (
            "\r\n\t\f\v    https://www.example.com/Příliš žluťoučký kůň/test.html?abc=def&xyz=123#frag  \u2028\u2029\x1c\x1d\x1e      \t  ",
            ParseResult(scheme="https", netloc="www.example.com", path="/Příliš žluťoučký kůň/test.html", params="", query="abc=def&xyz=123", fragment="frag")  # noqa
        ),
        (
            "\r\n\t\f\v    https://user@pass:www.example.com:8443/Příliš žluťoučký kůň/test.html?abc=def&xyz=123#frag  \u2028\u2029\x1c\x1d\x1e      \t  ",
            ParseResult(scheme="https", netloc="user@pass:www.example.com:8443", path="/Příliš žluťoučký kůň/test.html", params="", query="abc=def&xyz=123", fragment="frag")  # noqa
        ),
        (
            " https://user@pass:www.example.com:8443/Příliš žluťoučký kůň/test.html?abc=def&xyz=123#frag\r\n",
            ParseResult(scheme="https", netloc="user@pass:www.example.com:8443", path="/Příliš žluťoučký kůň/test.html", params="", query="abc=def&xyz=123", fragment="frag")  # noqa
        ),
        (
            " https://www.example.com/Příliš žluťoučký kůň/test.html?abc=def&xyz=123#frag\r\n",
            ParseResult(scheme="https", netloc="www.example.com", path="/Příliš žluťoučký kůň/test.html", params="", query="abc=def&xyz=123", fragment="frag")  # noqa
        ),
        (
            ".",
            ParseResult(scheme="", netloc="", path=".", params="", query="", fragment="")  # noqa
        ),
        (
            "..",
            ParseResult(scheme="", netloc="", path="..", params="", query="", fragment="")  # noqa
        ),
        (
            "../",
            ParseResult(scheme="", netloc="", path="../", params="", query="", fragment="")  # noqa
        ),
        (
            "/..",
            ParseResult(scheme="", netloc="", path="/..", params="", query="", fragment="")  # noqa
        ),
        (
            "/../",
            ParseResult(scheme="", netloc="", path="/../", params="", query="", fragment="")  # noqa
        ),
        (
            "\x00/../",
            ParseResult(scheme="", netloc="", path="\x00/../", params="", query="", fragment="")  # noqa
        ),
        (
            urllib.parse.urlparse(b'https://www.google.com/test?abc=def#frag'),
            InputDataTypeNotInAllowlistExc
        ),
        (
            urllib.parse.ParseResultBytes(scheme=b'', netloc=b'', path=b'', params=b'', query=b'', fragment=b''),  # noqa
            InputDataTypeNotInAllowlistExc
        ),
        (
            ("https", "www.google.com", "/test", "", "abc=def", "frag"),
            InputDataTypeNotInAllowlistExc
        ),
        (None, InputDataTypeNotInAllowlistExc),
        (True, InputDataTypeNotInAllowlistExc),
        (False, InputDataTypeNotInAllowlistExc),
        (-1, InputDataTypeNotInAllowlistExc),
        (0, InputDataTypeNotInAllowlistExc),
        (1, InputDataTypeNotInAllowlistExc),
        (-1.5, InputDataTypeNotInAllowlistExc),
        (-1.0, InputDataTypeNotInAllowlistExc),
        (-0.0, InputDataTypeNotInAllowlistExc),
        (0.0, InputDataTypeNotInAllowlistExc),
        (1.0, InputDataTypeNotInAllowlistExc),
        (1.5, InputDataTypeNotInAllowlistExc),
        (float("inf"), InputDataTypeNotInAllowlistExc),
        (float("nan"), InputDataTypeNotInAllowlistExc),
        (1+2j, InputDataTypeNotInAllowlistExc),
        (b'', InputDataTypeNotInAllowlistExc),
        (b'https://www.google.com/test?abc=def#frag', InputDataTypeNotInAllowlistExc),
        (bytearray(b''), InputDataTypeNotInAllowlistExc),
        (bytearray(b'https://www.google.com/test?abc=def#frag'), InputDataTypeNotInAllowlistExc),
        ([], InputDataTypeNotInAllowlistExc),
        (["https://www.google.com/test?abc=def#frag"], InputDataTypeNotInAllowlistExc),
        ({}, InputDataTypeNotInAllowlistExc),
        ({"https://www.google.com/test?abc=def#frag": "https://www.google.com/test?abc=def#frag"}, InputDataTypeNotInAllowlistExc),
        (str, InputDataTypeNotInAllowlistExc),
        (theoretical_testutils.EmptyObject, InputDataTypeNotInAllowlistExc),
        (datetime.datetime.now(), InputDataTypeNotInAllowlistExc),
        (datetime.datetime.now().date(), InputDataTypeNotInAllowlistExc),
        (datetime.datetime.now().time(), InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_address("127.7.8.9"), InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_address("::1"), InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_network("127.0.0.0/8"), InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_network("2001:db8::/64"), InputDataTypeNotInAllowlistExc),
        (uuid.UUID('{12345678-1234-5678-1234-567812345678}'), InputDataTypeNotInAllowlistExc),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc),
        (theoretical_testutils.TestException(), InputDataTypeNotInAllowlistExc),
        (object(), InputDataTypeNotInAllowlistExc),
        (StringableObject(""), InputDataTypeNotInAllowlistExc),
        (StringableObject("https://www.google.com/test?abc=def#frag"), InputDataTypeNotInAllowlistExc),
        (StringableObject(None), InputDataTypeNotInAllowlistExc),
        (StringableObject(theoretical_testutils.EmptyObject()), InputDataTypeNotInAllowlistExc),
        (ExceptionRaisingStringableObject(), InputDataTypeNotInAllowlistExc),
    )),
)


@pytest.mark.parametrize(("blueprint", "input_", "output"), theoretical_testutils.test_function_parameter_generator(__URL_BLUEPRINT_TEST_SUITE))
def test_url_blueprint(blueprint, input_, output):
    theoretical_testutils.perform_test(blueprint, input_, output)
