<!--
Copyright (c) 2022 Vít Labuda. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
following conditions are met:
 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
    disclaimer.
 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
    following disclaimer in the documentation and/or other materials provided with the distribution.
 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
    products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
-->


# 1. The Basics

**Datalidator** is a flexible, object-oriented Python library for parsing and validating untrusted input data.

One of its most prominent characteristics is that it is able to parse various kinds of input data: **configuration 
files, user inputs, web API outputs** etc.


## Blueprints, filters & validators
The main building blocks of this library's functionality are the following 3 types of objects:
1. **Blueprints** – The purpose of blueprints is to safely and reliably parse untrusted<sup>[1]</sup> input data to a 
   specific blueprint's output data type and raise an appropriate exception if it is not possible (i.e. blueprints 
   *must* be able to react to input data of any type and value without getting into an unexpected state under regular 
   conditions). If applicable, blueprints should also be capable of running the parsed data through filters and 
   validators. All blueprints must implement [`BlueprintIface`](../datalidator/blueprints/BlueprintIface.py).
2. **Filters** – The purpose of filters is to modify data already parsed by a blueprint (i.e. NOT the untrusted input 
   data!) in some way without changing their data type. Filters are normally not used directly, but instead through a 
   blueprint. All filters must implement [`FilterIface`](../datalidator/filters/FilterIface.py).
3. **Validators** – The purpose of validators is to check whether data already parsed by a blueprint and optionally 
   filtered by "zero or more" filters (i.e. NOT the untrusted input data!) meet certain requirements and if not, raise 
   `DataValidationFailedExc`. Validators are normally not used directly, but instead through a blueprint. All validators 
   must implement [`ValidatorIface`](../datalidator/validators/ValidatorIface.py).

<sup>1</sup> By untrusted data, data that were acquired in a way that does not allow arbitrary code to be put into the 
application are meant (e.g. deserialized JSON document or HTTP POST body). Therefore, for example, if a blueprint is 
used on a malicious *unpickled* object, the malicious code can get executed by the blueprint!

All blueprints, filters and validators also implement [`DatalidatorObjectIface`](../datalidator/DatalidatorObjectIface.py).

See the [class hierarchy document](Appendix-001_Class-Hierarchy.md) to find out what blueprints, filters and validators
come with this library.


## Exceptions & errors
Blueprints, filters and validators may raise subclasses of the following exception and error base classes:
1. [**DatalidatorExc**](../datalidator/exc/DatalidatorExc.py) – A superclass of all **exceptions** raised by Datalidator.
   One should catch exceptions that inherit from this class in the vast majority of cases because they can commonly
   occur even when one is using the library in a completely correct way – for example when invalid input data are
   passed to a blueprint (which is something that will happen if this library is used to handle untrusted user input in 
   any way).
2. [**DatalidatorError**](../datalidator/exc/err/DatalidatorError.py) – A superclass of all **errors** raised by Datalidator.
   One should not catch errors that inherit from this class in most cases because they can occur only when
   the library is used incorrectly, for example when an invalid argument is passed to a blueprint's initializer, and
   not for example as a result of invalid input data passed to a blueprint (this is what `DatalidatorExc` is here for). 
   Therefore, these errors are not mentioned in methods' docstrings.
 
See the [exception hierarchy document](Appendix-002_Exception-Hierarchy.md) to find out what exception and error classes 
come with this library.

---

* Next chapter: [2. Using Blueprints](002_Using-Blueprints.md)
