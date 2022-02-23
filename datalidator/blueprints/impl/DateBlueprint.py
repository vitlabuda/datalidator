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


from typing import final, Final, Any, Sequence, Optional, Tuple, Type
import datetime
from datalidator.blueprints.DefaultBlueprintWithStandardFeaturesImplBase import DefaultBlueprintWithStandardFeaturesImplBase
from datalidator.blueprints.impl.DatetimeBlueprint import DatetimeBlueprint
from datalidator.filters.FilterIface import FilterIface
from datalidator.validators.ValidatorIface import ValidatorIface


__all__ = "DateBlueprint",


class DateBlueprint(DefaultBlueprintWithStandardFeaturesImplBase[datetime.date]):
    """
    INPUT:
    - any object accepted by the initializer-provided 'DatetimeBlueprint' instance

    OUTPUT:
    - 'datetime.date' object
    """

    __slots__ = "__datetime_blueprint",

    def __init__(self,
                 datetime_blueprint: DatetimeBlueprint,
                 filters: Sequence[FilterIface[datetime.date]] = (),
                 validators: Sequence[ValidatorIface[datetime.date]] = (),
                 tag: str = ""):
        DefaultBlueprintWithStandardFeaturesImplBase.__init__(self, filters, validators, tag)

        self.__datetime_blueprint: Final[DatetimeBlueprint] = datetime_blueprint

    @final
    def get_datetime_blueprint(self) -> DatetimeBlueprint:
        return self.__datetime_blueprint

    def _get_allowed_output_data_types(self) -> Optional[Tuple[Type, ...]]:
        return datetime.date,

    def _parse(self, input_data: Any) -> datetime.date:
        datetime_object = self.__datetime_blueprint.use(input_data)

        return datetime_object.date()
