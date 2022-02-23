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


# Datalidator Class Hierarchy
This document contains the hierarchy of this library's built-in classes.

---

- **DatalidatorObjectIface** *([datalidator.DatalidatorObjectIface](../datalidator/DatalidatorObjectIface.py))*
    - **BlueprintIface** *([datalidator.blueprints.BlueprintIface](../datalidator/blueprints/BlueprintIface.py))*
        - **DefaultBlueprintImplBase** *([datalidator.blueprints.DefaultBlueprintImplBase](../datalidator/blueprints/DefaultBlueprintImplBase.py))*
            - **BlueprintChainingBlueprint** *([datalidator.blueprints.specialimpl.BlueprintChainingBlueprint](../datalidator/blueprints/specialimpl/BlueprintChainingBlueprint.py))*
            - **DefaultValueNoneHandlingBlueprint** *([datalidator.blueprints.specialimpl.DefaultValueNoneHandlingBlueprint](../datalidator/blueprints/specialimpl/DefaultValueNoneHandlingBlueprint.py))*
            - **ExceptionHandlingBlueprint** *([datalidator.blueprints.specialimpl.ExceptionHandlingBlueprint](../datalidator/blueprints/specialimpl/ExceptionHandlingBlueprint.py))*
            - **NoneHandlingBlueprint** *([datalidator.blueprints.specialimpl.NoneHandlingBlueprint](../datalidator/blueprints/specialimpl/NoneHandlingBlueprint.py))*
            - **DefaultBlueprintWithStandardFeaturesImplBase** *([datalidator.blueprints.DefaultBlueprintWithStandardFeaturesImplBase](../datalidator/blueprints/DefaultBlueprintWithStandardFeaturesImplBase.py))*
                - **DateBlueprint** *([datalidator.blueprints.impl.DateBlueprint](../datalidator/blueprints/impl/DateBlueprint.py))*
                - **DictionaryBlueprint** *([datalidator.blueprints.impl.DictionaryBlueprint](../datalidator/blueprints/impl/DictionaryBlueprint.py))*
                - **GenericBlueprint** *([datalidator.blueprints.impl.GenericBlueprint](../datalidator/blueprints/impl/GenericBlueprint.py))*
                - **ObjectBlueprint** *([datalidator.blueprints.impl.ObjectBlueprint](../datalidator/blueprints/impl/ObjectBlueprint.py))*
                - **PredefinedDictionaryBlueprint** *([datalidator.blueprints.impl.PredefinedDictionaryBlueprint](../datalidator/blueprints/impl/PredefinedDictionaryBlueprint.py))*
                - **TimeBlueprint** *([datalidator.blueprints.impl.TimeBlueprint](../datalidator/blueprints/impl/TimeBlueprint.py))*
                - **TimeIntervalBlueprint** *([datalidator.blueprints.impl.TimeIntervalBlueprint](../datalidator/blueprints/impl/TimeIntervalBlueprint.py))*
                - **UnixFilesystemPathBlueprint** *([datalidator.blueprints.impl.UnixFilesystemPathBlueprint](../datalidator/blueprints/impl/UnixFilesystemPathBlueprint.py))*
                - **URLBlueprint** *([datalidator.blueprints.impl.URLBlueprint](../datalidator/blueprints/impl/URLBlueprint.py))*
                - **UUIDBlueprint** *([datalidator.blueprints.impl.UUIDBlueprint](../datalidator/blueprints/impl/UUIDBlueprint.py))*
                - **JSONBlueprint** *([datalidator.blueprints.specialimpl.JSONBlueprint](../datalidator/blueprints/specialimpl/JSONBlueprint.py))*
                - **DefaultBlueprintWithModeSupportImplBase** *([datalidator.blueprints.DefaultBlueprintWithModeSupportImplBase](../datalidator/blueprints/DefaultBlueprintWithModeSupportImplBase.py))*
                    - **BooleanBlueprint** *([datalidator.blueprints.impl.BooleanBlueprint](../datalidator/blueprints/impl/BooleanBlueprint.py))*
                    - **BytesBlueprint** *([datalidator.blueprints.impl.BytesBlueprint](../datalidator/blueprints/impl/BytesBlueprint.py))*
                    - **DatetimeBlueprint** *([datalidator.blueprints.impl.DatetimeBlueprint](../datalidator/blueprints/impl/DatetimeBlueprint.py))*
                    - **FloatBlueprint** *([datalidator.blueprints.impl.FloatBlueprint](../datalidator/blueprints/impl/FloatBlueprint.py))*
                    - **IntegerBlueprint** *([datalidator.blueprints.impl.IntegerBlueprint](../datalidator/blueprints/impl/IntegerBlueprint.py))*
                    - **IPAddressBlueprint** *([datalidator.blueprints.impl.IPAddressBlueprint](../datalidator/blueprints/impl/IPAddressBlueprint.py))*
                    - **IPNetworkBlueprint** *([datalidator.blueprints.impl.IPNetworkBlueprint](../datalidator/blueprints/impl/IPNetworkBlueprint.py))*
                    - **ListBlueprint** *([datalidator.blueprints.impl.ListBlueprint](../datalidator/blueprints/impl/ListBlueprint.py))*
                    - **StringBlueprint** *([datalidator.blueprints.impl.StringBlueprint](../datalidator/blueprints/impl/StringBlueprint.py))*
    - **FilterIface** *([datalidator.filters.FilterIface](../datalidator/filters/FilterIface.py))*
        - **DefaultFilterImplBase** *([datalidator.filters.DefaultFilterImplBase](../datalidator/filters/DefaultFilterImplBase.py))*
            - **ListDeduplicateItemsFilter** *([datalidator.filters.impl.ListDeduplicateItemsFilter](../datalidator/filters/impl/ListDeduplicateItemsFilter.py))*
            - **StringDeduplicateWhitespaceFilter** *([datalidator.filters.impl.StringDeduplicateWhitespaceFilter](../datalidator/filters/impl/StringDeduplicateWhitespaceFilter.py))*
            - **StringControlAndSeparatorCharacterFilter** *([datalidator.filters.impl.StringControlAndSeparatorCharacterFilter](../datalidator/filters/impl/StringControlAndSeparatorCharacterFilter.py))*
            - **StringCapitalizeFilter** *([datalidator.filters.impl.StringCapitalizeFilter](../datalidator/filters/impl/StringCapitalizeFilter.py))*
            - **StringUppercaseFilter** *([datalidator.filters.impl.StringUppercaseFilter](../datalidator/filters/impl/StringUppercaseFilter.py))*
            - **UnixFilesystemPathAddTrailingSlashFilter** *([datalidator.filters.impl.UnixFilesystemPathAddTrailingSlashFilter](../datalidator/filters/impl/UnixFilesystemPathAddTrailingSlashFilter.py))*
            - **NumberRoundFilter** *([datalidator.filters.impl.NumberRoundFilter](../datalidator/filters/impl/NumberRoundFilter.py))*
            - **StringStripFilter** *([datalidator.filters.impl.StringStripFilter](../datalidator/filters/impl/StringStripFilter.py))*
            - **StringAlwaysEmptyFilter** *([datalidator.filters.impl.StringAlwaysEmptyFilter](../datalidator/filters/impl/StringAlwaysEmptyFilter.py))*
            - **NumberAbsoluteValueFilter** *([datalidator.filters.impl.NumberAbsoluteValueFilter](../datalidator/filters/impl/NumberAbsoluteValueFilter.py))*
            - **StringUnifyNewlinesFilter** *([datalidator.filters.impl.StringUnifyNewlinesFilter](../datalidator/filters/impl/StringUnifyNewlinesFilter.py))*
            - **StringLowercaseFilter** *([datalidator.filters.impl.StringLowercaseFilter](../datalidator/filters/impl/StringLowercaseFilter.py))*
            - **StringRegexReplaceFilter** *([datalidator.filters.impl.StringRegexReplaceFilter](../datalidator/filters/impl/StringRegexReplaceFilter.py))*
            - **NumberMaximumClampFilter** *([datalidator.filters.impl.NumberMaximumClampFilter](../datalidator/filters/impl/NumberMaximumClampFilter.py))*
            - **DatetimeAddTimezoneFilter** *([datalidator.filters.impl.DatetimeAddTimezoneFilter](../datalidator/filters/impl/DatetimeAddTimezoneFilter.py))*
            - **NumberMinimumClampFilter** *([datalidator.filters.impl.NumberMinimumClampFilter](../datalidator/filters/impl/NumberMinimumClampFilter.py))*
            - **StringUnifyWhitespaceFilter** *([datalidator.filters.impl.StringUnifyWhitespaceFilter](../datalidator/filters/impl/StringUnifyWhitespaceFilter.py))*
            - **DatetimeChangeTimezoneFilter** *([datalidator.filters.impl.DatetimeChangeTimezoneFilter](../datalidator/filters/impl/DatetimeChangeTimezoneFilter.py))*
            - **ReplacementMapFilter** *([datalidator.filters.impl.ReplacementMapFilter](../datalidator/filters/impl/ReplacementMapFilter.py))*
            - **StringReplaceFilter** *([datalidator.filters.impl.StringReplaceFilter](../datalidator/filters/impl/StringReplaceFilter.py))*
            - **UnixFilesystemPathStripTrailingSlashesFilter** *([datalidator.filters.impl.UnixFilesystemPathStripTrailingSlashesFilter](../datalidator/filters/impl/UnixFilesystemPathStripTrailingSlashesFilter.py))*
            - **StringUnicodeNormalizeFilter** *([datalidator.filters.impl.StringUnicodeNormalizeFilter](../datalidator/filters/impl/StringUnicodeNormalizeFilter.py))*
            - **ListSortFilter** *([datalidator.filters.impl.ListSortFilter](../datalidator/filters/impl/ListSortFilter.py))*
    - **ValidatorIface** *([datalidator.validators.ValidatorIface](../datalidator/validators/ValidatorIface.py))*
        - **DefaultValidatorImplBase** *([datalidator.validators.DefaultValidatorImplBase](../datalidator/validators/DefaultValidatorImplBase.py))*
            - **DefaultValidatorWithNegationSupportImplBase** *([datalidator.validators.DefaultValidatorWithNegationSupportImplBase](../datalidator/validators/DefaultValidatorWithNegationSupportImplBase.py))*
                - **SequenceContainsItemValidator** *([datalidator.validators.impl.SequenceContainsItemValidator](../datalidator/validators/impl/SequenceContainsItemValidator.py))*
                - **StringContainsSubstringValidator** *([datalidator.validators.impl.StringContainsSubstringValidator](../datalidator/validators/impl/StringContainsSubstringValidator.py))*
                - **IPAddressIsMulticastValidator** *([datalidator.validators.impl.IPAddressIsMulticastValidator](../datalidator/validators/impl/IPAddressIsMulticastValidator.py))*
                - **SequenceIsNotEmptyValidator** *([datalidator.validators.impl.SequenceIsNotEmptyValidator](../datalidator/validators/impl/SequenceIsNotEmptyValidator.py))*
                - **DatetimeIsAwareValidator** *([datalidator.validators.impl.DatetimeIsAwareValidator](../datalidator/validators/impl/DatetimeIsAwareValidator.py))*
                - **IPAddressIsPrivateValidator** *([datalidator.validators.impl.IPAddressIsPrivateValidator](../datalidator/validators/impl/IPAddressIsPrivateValidator.py))*
                - **IPAddressIsInNetworkValidator** *([datalidator.validators.impl.IPAddressIsInNetworkValidator](../datalidator/validators/impl/IPAddressIsInNetworkValidator.py))*
                - **IPAddressIsGlobalValidator** *([datalidator.validators.impl.IPAddressIsGlobalValidator](../datalidator/validators/impl/IPAddressIsGlobalValidator.py))*
                - **IPAddressIsLinkLocalValidator** *([datalidator.validators.impl.IPAddressIsLinkLocalValidator](../datalidator/validators/impl/IPAddressIsLinkLocalValidator.py))*
                - **StringMatchesRegexValidator** *([datalidator.validators.impl.StringMatchesRegexValidator](../datalidator/validators/impl/StringMatchesRegexValidator.py))*
                - **IPAddressIsLoopbackValidator** *([datalidator.validators.impl.IPAddressIsLoopbackValidator](../datalidator/validators/impl/IPAddressIsLoopbackValidator.py))*
            - **SequenceMaximumLengthValidator** *([datalidator.validators.impl.SequenceMaximumLengthValidator](../datalidator/validators/impl/SequenceMaximumLengthValidator.py))*
            - **StringIsOnlySingleCharacterValidator** *([datalidator.validators.impl.StringIsOnlySingleCharacterValidator](../datalidator/validators/impl/StringIsOnlySingleCharacterValidator.py))*
            - **NumberMinimumValueValidator** *([datalidator.validators.impl.NumberMinimumValueValidator](../datalidator/validators/impl/NumberMinimumValueValidator.py))*
            - **DatetimeNotAfterValidator** *([datalidator.validators.impl.DatetimeNotAfterValidator](../datalidator/validators/impl/DatetimeNotAfterValidator.py))*
            - **UnixFilesystemPathIsAbsoluteValidator** *([datalidator.validators.impl.UnixFilesystemPathIsAbsoluteValidator](../datalidator/validators/impl/UnixFilesystemPathIsAbsoluteValidator.py))*
            - **SequenceHasAllItemsUniqueValidator** *([datalidator.validators.impl.SequenceHasAllItemsUniqueValidator](../datalidator/validators/impl/SequenceHasAllItemsUniqueValidator.py))*
            - **StringIsOnlySingleWordValidator** *([datalidator.validators.impl.StringIsOnlySingleWordValidator](../datalidator/validators/impl/StringIsOnlySingleWordValidator.py))*
            - **StringContainsNoControlOrSeparatorCharactersValidator** *([datalidator.validators.impl.StringContainsNoControlOrSeparatorCharactersValidator](../datalidator/validators/impl/StringContainsNoControlOrSeparatorCharactersValidator.py))*
            - **IntegerIsPositiveValidator** *([datalidator.validators.impl.IntegerIsPositiveValidator](../datalidator/validators/impl/IntegerIsPositiveValidator.py))*
            - **AllowlistValidator** *([datalidator.validators.impl.AllowlistValidator](../datalidator/validators/impl/AllowlistValidator.py))*
            - **StringIsOnlySingleLineValidator** *([datalidator.validators.impl.StringIsOnlySingleLineValidator](../datalidator/validators/impl/StringIsOnlySingleLineValidator.py))*
            - **IPAddressIsIPv4Validator** *([datalidator.validators.impl.IPAddressIsIPv4Validator](../datalidator/validators/impl/IPAddressIsIPv4Validator.py))*
            - **DatetimeNotBeforeValidator** *([datalidator.validators.impl.DatetimeNotBeforeValidator](../datalidator/validators/impl/DatetimeNotBeforeValidator.py))*
            - **UnixFilesystemPathContainsOnlyFilenameValidator** *([datalidator.validators.impl.UnixFilesystemPathContainsOnlyFilenameValidator](../datalidator/validators/impl/UnixFilesystemPathContainsOnlyFilenameValidator.py))*
            - **BlocklistValidator** *([datalidator.validators.impl.BlocklistValidator](../datalidator/validators/impl/BlocklistValidator.py))*
            - **IPAddressIsIPv6Validator** *([datalidator.validators.impl.IPAddressIsIPv6Validator](../datalidator/validators/impl/IPAddressIsIPv6Validator.py))*
            - **SequenceMinimumLengthValidator** *([datalidator.validators.impl.SequenceMinimumLengthValidator](../datalidator/validators/impl/SequenceMinimumLengthValidator.py))*
            - **NumberMaximumValueValidator** *([datalidator.validators.impl.NumberMaximumValueValidator](../datalidator/validators/impl/NumberMaximumValueValidator.py))*
            - **UnixFilesystemPathIsRelativeValidator** *([datalidator.validators.impl.UnixFilesystemPathIsRelativeValidator](../datalidator/validators/impl/UnixFilesystemPathIsRelativeValidator.py))*
            - **IntegerIsZeroOrPositiveValidator** *([datalidator.validators.impl.IntegerIsZeroOrPositiveValidator](../datalidator/validators/impl/IntegerIsZeroOrPositiveValidator.py))*
