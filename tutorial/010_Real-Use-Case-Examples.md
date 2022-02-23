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


# 10. Real Use Case Examples

Some automated tests bundled with this library show (and obviously also test) real use cases, such as parsing 
real configuration files and outputs of web APIs, and may be used as examples when learning how to use this library in
"serious" projects. However, keep in mind that these tests are quite complex, so make sure you fully understand the 
"theoretical" examples (which are much simpler) contained within [this tutorial](.), or you might get easily confused!

The aforementioned automated tests are located in the [tests/002_real](../tests/002_real) directory:
1. [Configuration file: A NAT64 translator](../tests/002_real/test_100_config_nat64.py)
2. [Web API: JSONPlaceholder](../tests/002_real/test_001_api_jsonplaceholder.py)
3. [Web API: GitHub](../tests/002_real/test_002_api_github.py)
4. [Web API: Boženka](../tests/002_real/test_003_api_bozenka.py)

---

* Previous chapter: [9. Extending the Functionality](009_Extending-the-Functionality.md)
