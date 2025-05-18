from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.generation_tone import GenerationTone
from ..models.scenario_type import ScenarioType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.scenario_data_poin_response import ScenarioDataPoinResponse
    from ..models.scenario_set_generate_checks_item_type_1 import ScenarioSetGenerateChecksItemType1


T = TypeVar("T", bound="ScenarioSetGenerate")


@_attrs_define
class ScenarioSetGenerate:
    """
    Attributes:
        name (str): Name of the generated scenario set
        number_examples (int): Number of examples to be generated for the scenario set
        project_id (Union[None, UUID, Unset]): ID for the project
        source_scenario_id (Union[None, UUID, Unset]): ID for the scenario set that the generated scenario set will use
            as a source. Will throw an exception if 'source_scenario_rows' is also provided.
        source_scenario_rows (Union[None, Unset, list['ScenarioDataPoinResponse']]): Rows for the scenario set that the
            generated scenario set will use as a source. Will throw an exception if 'source_scenario_id' is also provided.
        synonym_sets (Union[None, Unset, list[list[str]]]): 2D list used by the generator to determine synonyms. Used
            with the SYNONYMS generation type.
        save_generated_scenario (Union[Unset, bool]): Whether to save the generated scenarios. Defaults to True.
            Default: True.
        generation_type (Union[Unset, ScenarioType]):
        generation_tone (Union[Unset, GenerationTone]):
        generation_prompt (Union[None, Unset, str]): Prompt for the generator to use when generating scenarios. Only
            supported by CustomGenerator type.
        pre_template (Union[None, Unset, str]): Template for pre-processing scenario before sending it to generator
        post_template (Union[None, Unset, str]): Template for post-processing scenario after generator before it's saved
        lock_result (Union[Unset, bool]): Whether to lock the result of the generated scenario. Used in the Custom
            Generator type. Default: False.
        checks (Union[Unset, list[Union['ScenarioSetGenerateChecksItemType1', str]]]): List of check names or check
            configs to run on the generated scenarios
    """

    name: str
    number_examples: int
    project_id: Union[None, UUID, Unset] = UNSET
    source_scenario_id: Union[None, UUID, Unset] = UNSET
    source_scenario_rows: Union[None, Unset, list["ScenarioDataPoinResponse"]] = UNSET
    synonym_sets: Union[None, Unset, list[list[str]]] = UNSET
    save_generated_scenario: Union[Unset, bool] = True
    generation_type: Union[Unset, ScenarioType] = UNSET
    generation_tone: Union[Unset, GenerationTone] = UNSET
    generation_prompt: Union[None, Unset, str] = UNSET
    pre_template: Union[None, Unset, str] = UNSET
    post_template: Union[None, Unset, str] = UNSET
    lock_result: Union[Unset, bool] = False
    checks: Union[Unset, list[Union["ScenarioSetGenerateChecksItemType1", str]]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.scenario_set_generate_checks_item_type_1 import ScenarioSetGenerateChecksItemType1

        name = self.name

        number_examples = self.number_examples

        project_id: Union[None, Unset, str]
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        elif isinstance(self.project_id, UUID):
            project_id = str(self.project_id)
        else:
            project_id = self.project_id

        source_scenario_id: Union[None, Unset, str]
        if isinstance(self.source_scenario_id, Unset):
            source_scenario_id = UNSET
        elif isinstance(self.source_scenario_id, UUID):
            source_scenario_id = str(self.source_scenario_id)
        else:
            source_scenario_id = self.source_scenario_id

        source_scenario_rows: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.source_scenario_rows, Unset):
            source_scenario_rows = UNSET
        elif isinstance(self.source_scenario_rows, list):
            source_scenario_rows = []
            for source_scenario_rows_type_0_item_data in self.source_scenario_rows:
                source_scenario_rows_type_0_item = source_scenario_rows_type_0_item_data.to_dict()
                source_scenario_rows.append(source_scenario_rows_type_0_item)

        else:
            source_scenario_rows = self.source_scenario_rows

        synonym_sets: Union[None, Unset, list[list[str]]]
        if isinstance(self.synonym_sets, Unset):
            synonym_sets = UNSET
        elif isinstance(self.synonym_sets, list):
            synonym_sets = []
            for synonym_sets_type_0_item_data in self.synonym_sets:
                synonym_sets_type_0_item = synonym_sets_type_0_item_data

                synonym_sets.append(synonym_sets_type_0_item)

        else:
            synonym_sets = self.synonym_sets

        save_generated_scenario = self.save_generated_scenario

        generation_type: Union[Unset, str] = UNSET
        if not isinstance(self.generation_type, Unset):
            generation_type = self.generation_type.value

        generation_tone: Union[Unset, str] = UNSET
        if not isinstance(self.generation_tone, Unset):
            generation_tone = self.generation_tone.value

        generation_prompt: Union[None, Unset, str]
        if isinstance(self.generation_prompt, Unset):
            generation_prompt = UNSET
        else:
            generation_prompt = self.generation_prompt

        pre_template: Union[None, Unset, str]
        if isinstance(self.pre_template, Unset):
            pre_template = UNSET
        else:
            pre_template = self.pre_template

        post_template: Union[None, Unset, str]
        if isinstance(self.post_template, Unset):
            post_template = UNSET
        else:
            post_template = self.post_template

        lock_result = self.lock_result

        checks: Union[Unset, list[Union[dict[str, Any], str]]] = UNSET
        if not isinstance(self.checks, Unset):
            checks = []
            for checks_item_data in self.checks:
                checks_item: Union[dict[str, Any], str]
                if isinstance(checks_item_data, ScenarioSetGenerateChecksItemType1):
                    checks_item = checks_item_data.to_dict()
                else:
                    checks_item = checks_item_data
                checks.append(checks_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "number_examples": number_examples,
            }
        )
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if source_scenario_id is not UNSET:
            field_dict["source_scenario_id"] = source_scenario_id
        if source_scenario_rows is not UNSET:
            field_dict["source_scenario_rows"] = source_scenario_rows
        if synonym_sets is not UNSET:
            field_dict["synonym_sets"] = synonym_sets
        if save_generated_scenario is not UNSET:
            field_dict["save_generated_scenario"] = save_generated_scenario
        if generation_type is not UNSET:
            field_dict["generation_type"] = generation_type
        if generation_tone is not UNSET:
            field_dict["generation_tone"] = generation_tone
        if generation_prompt is not UNSET:
            field_dict["generation_prompt"] = generation_prompt
        if pre_template is not UNSET:
            field_dict["pre_template"] = pre_template
        if post_template is not UNSET:
            field_dict["post_template"] = post_template
        if lock_result is not UNSET:
            field_dict["lock_result"] = lock_result
        if checks is not UNSET:
            field_dict["checks"] = checks

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.scenario_data_poin_response import ScenarioDataPoinResponse
        from ..models.scenario_set_generate_checks_item_type_1 import ScenarioSetGenerateChecksItemType1

        d = dict(src_dict)
        name = d.pop("name")

        number_examples = d.pop("number_examples")

        def _parse_project_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                project_id_type_0 = UUID(data)

                return project_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))

        def _parse_source_scenario_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                source_scenario_id_type_0 = UUID(data)

                return source_scenario_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        source_scenario_id = _parse_source_scenario_id(d.pop("source_scenario_id", UNSET))

        def _parse_source_scenario_rows(data: object) -> Union[None, Unset, list["ScenarioDataPoinResponse"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                source_scenario_rows_type_0 = []
                _source_scenario_rows_type_0 = data
                for source_scenario_rows_type_0_item_data in _source_scenario_rows_type_0:
                    source_scenario_rows_type_0_item = ScenarioDataPoinResponse.from_dict(
                        source_scenario_rows_type_0_item_data
                    )

                    source_scenario_rows_type_0.append(source_scenario_rows_type_0_item)

                return source_scenario_rows_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["ScenarioDataPoinResponse"]], data)

        source_scenario_rows = _parse_source_scenario_rows(d.pop("source_scenario_rows", UNSET))

        def _parse_synonym_sets(data: object) -> Union[None, Unset, list[list[str]]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                synonym_sets_type_0 = []
                _synonym_sets_type_0 = data
                for synonym_sets_type_0_item_data in _synonym_sets_type_0:
                    synonym_sets_type_0_item = cast(list[str], synonym_sets_type_0_item_data)

                    synonym_sets_type_0.append(synonym_sets_type_0_item)

                return synonym_sets_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[list[str]]], data)

        synonym_sets = _parse_synonym_sets(d.pop("synonym_sets", UNSET))

        save_generated_scenario = d.pop("save_generated_scenario", UNSET)

        _generation_type = d.pop("generation_type", UNSET)
        generation_type: Union[Unset, ScenarioType]
        if isinstance(_generation_type, Unset):
            generation_type = UNSET
        else:
            generation_type = ScenarioType(_generation_type)

        _generation_tone = d.pop("generation_tone", UNSET)
        generation_tone: Union[Unset, GenerationTone]
        if isinstance(_generation_tone, Unset):
            generation_tone = UNSET
        else:
            generation_tone = GenerationTone(_generation_tone)

        def _parse_generation_prompt(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        generation_prompt = _parse_generation_prompt(d.pop("generation_prompt", UNSET))

        def _parse_pre_template(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        pre_template = _parse_pre_template(d.pop("pre_template", UNSET))

        def _parse_post_template(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        post_template = _parse_post_template(d.pop("post_template", UNSET))

        lock_result = d.pop("lock_result", UNSET)

        checks = []
        _checks = d.pop("checks", UNSET)
        for checks_item_data in _checks or []:

            def _parse_checks_item(data: object) -> Union["ScenarioSetGenerateChecksItemType1", str]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    checks_item_type_1 = ScenarioSetGenerateChecksItemType1.from_dict(data)

                    return checks_item_type_1
                except:  # noqa: E722
                    pass
                return cast(Union["ScenarioSetGenerateChecksItemType1", str], data)

            checks_item = _parse_checks_item(checks_item_data)

            checks.append(checks_item)

        scenario_set_generate = cls(
            name=name,
            number_examples=number_examples,
            project_id=project_id,
            source_scenario_id=source_scenario_id,
            source_scenario_rows=source_scenario_rows,
            synonym_sets=synonym_sets,
            save_generated_scenario=save_generated_scenario,
            generation_type=generation_type,
            generation_tone=generation_tone,
            generation_prompt=generation_prompt,
            pre_template=pre_template,
            post_template=post_template,
            lock_result=lock_result,
            checks=checks,
        )

        scenario_set_generate.additional_properties = d
        return scenario_set_generate

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
