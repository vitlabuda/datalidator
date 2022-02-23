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


# 6. Object Blueprint

[`ObjectBlueprint`](../datalidator/blueprints/impl/ObjectBlueprint.py) is possibly the most important blueprint for 
using this library is a practical manner. It allows one to use a subclass of 
[`ObjectModel`](../datalidator/blueprints/extras/ObjectModel.py) populated with class variables to declare a "model"
for a "heterogeneous" dictionary. Each variable's name is used as a key to find a value in an input dictionary (or 
another object convertible to a dictionary) which is then parsed by the blueprint assigned to the class variable. The 
model class can then be passed to `ObjectBlueprint`'s initializer and when the blueprint is used, the model gets 
instantiated and the data parsed according to it are passed to its initializer using `kwargs` (`ObjectModel` is a 
subclass of `types.SimpleNamespace`, so it is not necessary for you to define your own initializer function).

By default, all the dictionary keys (= names of class variables) are considered mandatory which means that if a key
is not present in the input dictionary, `ObjectBlueprint` raises an exception. To make a key optional, wrap its 
blueprint into an instance of [`OptionalItem`](../datalidator/blueprints/extras/OptionalItem.py) (or, to be exact, into 
an instance of any class implementing [`OptionalItemIface`](../datalidator/blueprints/extras/OptionalItemIface.py)) 
whose method for getting a default value will be called if the key is not found in the input dictionary. All in all, 
this blueprint addresses the practical shortcomings of `DictionaryBlueprint` described in the 
[previous chapter](005_Lists-and-Dictionaries.md) of this tutorial.

The way of declaring an `ObjectModel` looks similar to the way of declaring tables of 
[SQLAlchemy](https://docs.sqlalchemy.org/en/14/orm/tutorial.html#declare-a-mapping) or 
the forms of [WTForms](https://wtforms.readthedocs.io/en/2.3.x/crash_course/#getting-started).

The following example shows how to parse values from an *over-simplified* registration form:
```python
from datalidator.blueprints.impl.ObjectBlueprint import ObjectBlueprint
from datalidator.blueprints.impl.StringBlueprint import StringBlueprint
from datalidator.blueprints.impl.IntegerBlueprint import IntegerBlueprint
from datalidator.blueprints.impl.BooleanBlueprint import BooleanBlueprint
from datalidator.blueprints.extras.ObjectModel import ObjectModel
from datalidator.blueprints.extras.OptionalItem import OptionalItem

class RegistrationFormModel(ObjectModel):
    username = StringBlueprint()
    password = StringBlueprint()
    age = IntegerBlueprint()
    tos_accepted = OptionalItem(wrapped_blueprint=BooleanBlueprint(), default_value=False)  # "tos" = Terms of Service

blueprint = ObjectBlueprint(object_model=RegistrationFormModel)

blueprint.use({"username": "joe123", "password": "MyPassword", "age": "18\n", "tos_accepted": True})  # == RegistrationFormModel(username='joe123', password='MyPassword', age=18, tos_accepted=True)
blueprint.use({"username": "joe123", "password": "MyPassword", "age": "18\n", "tos_accepted": "FALSE"})  # == RegistrationFormModel(username='joe123', password='MyPassword', age=18, tos_accepted=False)
blueprint.use({"username": "joe123", "password": "MyPassword", "age": "18\n"})  # == RegistrationFormModel(username='joe123', password='MyPassword', age=18, tos_accepted=False)
blueprint.use([["username", "joe123"], ["password", "MyPassword"], ["age", "18\n"]])  # == RegistrationFormModel(username='joe123', password='MyPassword', age=18, tos_accepted=False)

blueprint.use({"username": tuple(), "password": "MyPassword", "age": "18\n", "tos_accepted": True})  # raises InputDataTypeNotInAllowlistExc (= a subclass of DatalidatorExc)
blueprint.use({"username": "joe123", "password": "MyPassword", "age": "hello", "tos_accepted": True})  # raises InputDataNotConvertibleExc (= a subclass of DatalidatorExc)
blueprint.use({"username": "joe123", "password": "MyPassword", "age": "18\n", "tos_accepted": "invalid"})  # raises InputDataValueNotAllowedForDataTypeExc (= a subclass of DatalidatorExc)
blueprint.use({"username": "joe123", "age": "18\n", "tos_accepted": True})  # raises InvalidInputDataExc (= a subclass of DatalidatorExc)
blueprint.use({"username": "joe123", "password": "MyPassword", "tos_accepted": True})  # raises InvalidInputDataExc (= a subclass of DatalidatorExc)
blueprint.use(1)  # raises InputDataNotConvertibleExc (= a subclass of DatalidatorExc)
blueprint.use(None)  # raises InputDataNotConvertibleExc (= a subclass of DatalidatorExc)
```


## Predefined Dictionary Blueprint
`ObjectBlueprint` contains little logic and is mostly just a lightweight wrapper class of 
[`PredefinedDictionaryBlueprint`](../datalidator/blueprints/impl/PredefinedDictionaryBlueprint.py). This blueprint 
accepts a "dictionary specification" instead of an object model class and returns a dictionary instead of an instance
of the object model. Therefore, with the use of `PredefinedDictionaryBlueprint`, it is, for example, possible to use 
keys other than strings or keys whose names are Python keywords (such as "class" or "return").

The above example of an *over-simplified* registration words can be easily rewritten to make use of 
`PredefinedDictionaryBlueprint` instead of `ObjectBlueprint`:
```python
from datalidator.blueprints.impl.PredefinedDictionaryBlueprint import PredefinedDictionaryBlueprint
from datalidator.blueprints.impl.StringBlueprint import StringBlueprint
from datalidator.blueprints.impl.IntegerBlueprint import IntegerBlueprint
from datalidator.blueprints.impl.BooleanBlueprint import BooleanBlueprint
from datalidator.blueprints.extras.OptionalItem import OptionalItem

blueprint = PredefinedDictionaryBlueprint(dict_specification={
    "username": StringBlueprint(),
    "password": StringBlueprint(),
    "age": IntegerBlueprint(),
    "tos_accepted": OptionalItem(wrapped_blueprint=BooleanBlueprint(), default_value=False)  # "tos" = Terms of Service
})

blueprint.use({"username": "joe123", "password": "MyPassword", "age": "18\n", "tos_accepted": True})  # == {'username': 'joe123', 'password': 'MyPassword', 'age': 18, 'tos_accepted': True}
blueprint.use({"username": "joe123", "password": "MyPassword", "age": "18\n", "tos_accepted": "FALSE"})  # == {'username': 'joe123', 'password': 'MyPassword', 'age': 18, 'tos_accepted': False}
blueprint.use({"username": "joe123", "password": "MyPassword", "age": "18\n"})  # == {'username': 'joe123', 'password': 'MyPassword', 'age': 18, 'tos_accepted': False}
blueprint.use([["username", "joe123"], ["password", "MyPassword"], ["age", "18\n"]])  # == {'username': 'joe123', 'password': 'MyPassword', 'age': 18, 'tos_accepted': False}

blueprint.use({"username": tuple(), "password": "MyPassword", "age": "18\n", "tos_accepted": True})  # raises InputDataTypeNotInAllowlistExc (= a subclass of DatalidatorExc)
blueprint.use({"username": "joe123", "password": "MyPassword", "age": "hello", "tos_accepted": True})  # raises InputDataNotConvertibleExc (= a subclass of DatalidatorExc)
blueprint.use({"username": "joe123", "password": "MyPassword", "age": "18\n", "tos_accepted": "invalid"})  # raises InputDataValueNotAllowedForDataTypeExc (= a subclass of DatalidatorExc)
blueprint.use({"username": "joe123", "age": "18\n", "tos_accepted": True})  # raises InvalidInputDataExc (= a subclass of DatalidatorExc)
blueprint.use({"username": "joe123", "password": "MyPassword", "tos_accepted": True})  # raises InvalidInputDataExc (= a subclass of DatalidatorExc)
blueprint.use(1)  # raises InputDataNotConvertibleExc (= a subclass of DatalidatorExc)
blueprint.use(None)  # raises InputDataNotConvertibleExc (= a subclass of DatalidatorExc)
```

---

* Next chapter: [7. Special Blueprints](007_Special-Blueprints.md)
* Previous chapter: [5. Lists and Dictionaries](005_Lists-and-Dictionaries.md)
