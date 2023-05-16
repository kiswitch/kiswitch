#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Rafael Silva <perigoso@riseup.net>

import typing


class kiswitch_property:
    def __init__(
        self,
        *,
        base_type: typing.Any = None,
        allowed_list: list[typing.Any] = None,
        list_property: bool = False,
        default: typing.Any = None,
        doc: str = None,
    ):
        assert isinstance(base_type, type) and base_type is not None, "base_type must be a type"
        assert isinstance(list_property, bool), "list_property must be a bool"

        if allowed_list is not None:
            assert isinstance(allowed_list, list), "allowed_list must be a list"
            try:
                new_allowed_list = set()
                for item in allowed_list:
                    new_allowed_list.add(base_type(item))
                allowed_list = list(new_allowed_list)
            except Exception:
                raise TypeError(f"allowed must be a list of {base_type}")

        if default is not None:
            try:
                if list_property:
                    assert isinstance(default, list), "default must be a list"
                    new_default = set()
                    for item in default:
                        new_default.add(base_type(item))
                    default = list(new_default)
                else:
                    default = base_type(default)
            except Exception:
                raise TypeError(f"default must be of type {base_type}")

        self._base_type = base_type
        self._allowed_list = allowed_list
        self._list_property = list_property
        self._default = default
        self._doc = doc

    def __get_default__(self):
        return self._default

    def __set_name__(self, owner, name):
        self._name = "_" + name

    def __get__(self, obj, type):
        if obj is None:
            return self._default
        return getattr(obj, self._name, self._default)

    def __set__(self, obj, value):
        if value is None:
            value = self._default
        else:
            try:
                if self._list_property:
                    assert isinstance(value, list), f"value must be a list"
                    new_value = list()
                    for item in value:
                        new_value_item = self._base_type(item)
                        if self._allowed_list is not None:
                            if new_value_item not in self._allowed_list:
                                raise ValueError(f"Value not allowed: {new_value_item}")
                        new_value.append(new_value_item)
                    value = new_value
                else:
                    value = self._base_type(value)
                    if self._allowed_list is not None:
                        if value not in self._allowed_list:
                            raise ValueError(f"Value not allowed: {value}")
            except Exception:
                raise TypeError(f"Value must be of type {self._base_type}")
        setattr(obj, self._name, value)

    def __doc__(self):
        return self._doc


def get_kiswitch_properties(cls):
    names = dir(cls)

    result = []
    processed = set()

    for name in names:
        if name not in processed:
            if not name.startswith("_"):
                dict_obj = cls.__dict__[name]
                if isinstance(dict_obj, kiswitch_property):
                    result.append(
                        {
                            "name": name,
                            "type": dict_obj._base_type,
                            "default": dict_obj._default,
                            "doc": dict_obj._doc,
                            "allowed": dict_obj._allowed_list,
                        }
                    )
            processed.add(name)

    return result
