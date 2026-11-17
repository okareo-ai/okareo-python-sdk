from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.outbound_line_request_api_keys_type_0 import OutboundLineRequestApiKeysType0
    from ..models.outbound_line_request_simulation_params_type_0 import OutboundLineRequestSimulationParamsType0


T = TypeVar("T", bound="OutboundLineRequest")


@_attrs_define
class OutboundLineRequest:
    """Turn an outbound Simulation on. Same ingredients as a simulation run, plus
    the line's own limits.

        Attributes:
            mut_id (UUID): The Target; must receive calls (call_direction agent_calls_okareo)
            scenario_id (UUID):
            driver_id (UUID):
            checks (list[str] | None | Unset):
            name (None | str | Unset):
            api_keys (None | OutboundLineRequestApiKeysType0 | Unset):
            simulation_params (None | OutboundLineRequestSimulationParamsType0 | Unset):
            armed_max_duration_s (int | None | Unset): Turn off automatically after this long (default 2 h, max 8 h)
            idle_timeout_s (int | None | Unset): Turn off after this long with no calls (default 30 min)
            expected_caller_ids (list[str] | Unset): If set, calls from any other number are rejected
    """

    mut_id: UUID
    scenario_id: UUID
    driver_id: UUID
    checks: list[str] | None | Unset = UNSET
    name: None | str | Unset = UNSET
    api_keys: None | OutboundLineRequestApiKeysType0 | Unset = UNSET
    simulation_params: None | OutboundLineRequestSimulationParamsType0 | Unset = UNSET
    armed_max_duration_s: int | None | Unset = UNSET
    idle_timeout_s: int | None | Unset = UNSET
    expected_caller_ids: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.outbound_line_request_api_keys_type_0 import OutboundLineRequestApiKeysType0
        from ..models.outbound_line_request_simulation_params_type_0 import OutboundLineRequestSimulationParamsType0

        mut_id = str(self.mut_id)

        scenario_id = str(self.scenario_id)

        driver_id = str(self.driver_id)

        checks: list[str] | None | Unset
        if isinstance(self.checks, Unset):
            checks = UNSET
        elif isinstance(self.checks, list):
            checks = self.checks

        else:
            checks = self.checks

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        api_keys: dict[str, Any] | None | Unset
        if isinstance(self.api_keys, Unset):
            api_keys = UNSET
        elif isinstance(self.api_keys, OutboundLineRequestApiKeysType0):
            api_keys = self.api_keys.to_dict()
        else:
            api_keys = self.api_keys

        simulation_params: dict[str, Any] | None | Unset
        if isinstance(self.simulation_params, Unset):
            simulation_params = UNSET
        elif isinstance(self.simulation_params, OutboundLineRequestSimulationParamsType0):
            simulation_params = self.simulation_params.to_dict()
        else:
            simulation_params = self.simulation_params

        armed_max_duration_s: int | None | Unset
        if isinstance(self.armed_max_duration_s, Unset):
            armed_max_duration_s = UNSET
        else:
            armed_max_duration_s = self.armed_max_duration_s

        idle_timeout_s: int | None | Unset
        if isinstance(self.idle_timeout_s, Unset):
            idle_timeout_s = UNSET
        else:
            idle_timeout_s = self.idle_timeout_s

        expected_caller_ids: list[str] | Unset = UNSET
        if not isinstance(self.expected_caller_ids, Unset):
            expected_caller_ids = self.expected_caller_ids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "mut_id": mut_id,
                "scenario_id": scenario_id,
                "driver_id": driver_id,
            }
        )
        if checks is not UNSET:
            field_dict["checks"] = checks
        if name is not UNSET:
            field_dict["name"] = name
        if api_keys is not UNSET:
            field_dict["api_keys"] = api_keys
        if simulation_params is not UNSET:
            field_dict["simulation_params"] = simulation_params
        if armed_max_duration_s is not UNSET:
            field_dict["armed_max_duration_s"] = armed_max_duration_s
        if idle_timeout_s is not UNSET:
            field_dict["idle_timeout_s"] = idle_timeout_s
        if expected_caller_ids is not UNSET:
            field_dict["expected_caller_ids"] = expected_caller_ids

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.outbound_line_request_api_keys_type_0 import OutboundLineRequestApiKeysType0
        from ..models.outbound_line_request_simulation_params_type_0 import OutboundLineRequestSimulationParamsType0

        d = dict(src_dict)
        mut_id = UUID(d.pop("mut_id"))

        scenario_id = UUID(d.pop("scenario_id"))

        driver_id = UUID(d.pop("driver_id"))

        def _parse_checks(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                checks_type_0 = cast(list[str], data)

                return checks_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        checks = _parse_checks(d.pop("checks", UNSET))

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_api_keys(data: object) -> None | OutboundLineRequestApiKeysType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                api_keys_type_0 = OutboundLineRequestApiKeysType0.from_dict(data)

                return api_keys_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | OutboundLineRequestApiKeysType0 | Unset, data)

        api_keys = _parse_api_keys(d.pop("api_keys", UNSET))

        def _parse_simulation_params(data: object) -> None | OutboundLineRequestSimulationParamsType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                simulation_params_type_0 = OutboundLineRequestSimulationParamsType0.from_dict(data)

                return simulation_params_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | OutboundLineRequestSimulationParamsType0 | Unset, data)

        simulation_params = _parse_simulation_params(d.pop("simulation_params", UNSET))

        def _parse_armed_max_duration_s(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        armed_max_duration_s = _parse_armed_max_duration_s(d.pop("armed_max_duration_s", UNSET))

        def _parse_idle_timeout_s(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        idle_timeout_s = _parse_idle_timeout_s(d.pop("idle_timeout_s", UNSET))

        expected_caller_ids = cast(list[str], d.pop("expected_caller_ids", UNSET))

        outbound_line_request = cls(
            mut_id=mut_id,
            scenario_id=scenario_id,
            driver_id=driver_id,
            checks=checks,
            name=name,
            api_keys=api_keys,
            simulation_params=simulation_params,
            armed_max_duration_s=armed_max_duration_s,
            idle_timeout_s=idle_timeout_s,
            expected_caller_ids=expected_caller_ids,
        )

        outbound_line_request.additional_properties = d
        return outbound_line_request

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
