"""Function call AST validator check - adapted from server predefined check.

This is a complex check that validates function calls using AST checker logic
from the Berkeley Function Call Leaderboard. Used to test that complex checks
pass validation.
"""

import json
import re

from okareo.checks import CodeBasedCheck


def safe_json_loads(value: str) -> dict | list | str:
    """Safely parse JSON, returning original string on failure."""
    if not isinstance(value, str):
        return value
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return value


class Check(CodeBasedCheck):
    """
    Validates function calls using AST checker from Berkeley Function Call Leaderboard.

    Compares tool calls from model output against expected structure defined in scenario result.
    All validation and error formatting logic is encapsulated in this class.
    """

    # Type mapping constants for validation
    PYTHON_TYPE_MAPPING = {
        "string": str,
        "integer": int,
        "float": float,
        "boolean": bool,
        "array": list,
        "tuple": list,
        "dict": dict,
        "object": dict,
        "any": str,
    }

    PYTHON_NESTED_TYPE_CHECK_LIST = ["array", "tuple"]

    @staticmethod
    def evaluate(
        model_output: str,
        scenario_input: str,
        scenario_result: str,
        metadata: dict,
        model_input: str,
    ) -> bool:
        """
        Evaluate function calls against expected structure.

        Args:
            model_output: Model output (not used directly, tool calls come from metadata)
            scenario_input: JSON string containing function descriptions
            scenario_result: JSON string containing expected function calls
            metadata: Dictionary containing tool_calls from model
            model_input: Model input (not used)

        Returns:
            bool indicating if validation passed
        """
        scenario_input_parsed = safe_json_loads(scenario_input)
        if isinstance(scenario_input_parsed, dict):
            func_descriptions = scenario_input_parsed.get("function", {})
            if (
                not func_descriptions
                or (isinstance(func_descriptions, dict) and len(func_descriptions) == 0)
                or (isinstance(func_descriptions, list) and len(func_descriptions) == 0)
            ):
                return False
        else:
            return False

        tool_calls = metadata.get("tool_calls", [])
        if not isinstance(tool_calls, list) or len(tool_calls) == 0:
            return False

        tool_calls_parsed = []
        for tc in tool_calls:
            tool_call = tc.get("function", {})
            tool_call_parsed = {tool_call.get("name"): tool_call.get("arguments")}
            tool_calls_parsed.append(tool_call_parsed)

        scenario_result_parsed = safe_json_loads(scenario_result)

        strict_function_order = (
            scenario_result_parsed.get("strict_function_order", False)
            if isinstance(scenario_result_parsed, dict)
            else False
        )

        expected_calls_list = None

        if (
            isinstance(scenario_result_parsed, dict)
            and "function_calls" in scenario_result_parsed
        ):
            expected_calls_list = scenario_result_parsed["function_calls"]

        if expected_calls_list is None:
            expected_calls_list = scenario_result_parsed

        if not isinstance(expected_calls_list, list):
            return False

        possible_answers = []
        for sr in expected_calls_list:
            if not isinstance(sr, dict):
                continue

            scenario_result_args = {
                k: v
                for k, v in sr.get("arguments", {}).items()
                if (isinstance(v, str) and len(v) > 0)
                or (not isinstance(v, str) and v is not None)
            }
            possible_answers.append({sr.get("name", ""): scenario_result_args})

        if strict_function_order:
            result = Check.parallel_function_checker_with_order(
                func_descriptions, tool_calls_parsed, possible_answers
            )
        else:
            result = Check.parallel_function_checker_no_order(
                func_descriptions, tool_calls_parsed, possible_answers
            )

        return result["valid"]

    @staticmethod
    def parallel_function_checker_no_order(
        func_descriptions: list,
        model_output: list,
        possible_answers: list,
    ) -> dict:
        """Validate multiple function calls (order-independent)."""
        if len(model_output) != len(possible_answers):
            return {
                "valid": False,
                "error": ["Wrong number of functions."],
                "error_type": "parallel_function_checker_no_order:wrong_count",
            }

        matched_indices = []

        for i in range(len(possible_answers)):
            func_name_expected = list(possible_answers[i].keys())[0]
            func_description = Check.find_description(
                func_descriptions, func_name_expected
            )

            all_errors = []

            for index in range(len(model_output)):
                if index in matched_indices:
                    continue

                result = Check.simple_function_checker(
                    func_description,
                    model_output[index],
                    possible_answers[i],
                )

                if result["valid"]:
                    matched_indices.append(index)
                    break
                else:
                    all_errors.append(
                        {
                            f"Model Result Index {index}": {
                                "sub_error": result["error"],
                                "sub_error_type": result["error_type"],
                                "model_output_item": model_output[index],
                                "possible_answer_item": possible_answers[i],
                            }
                        }
                    )

            if not result["valid"]:
                considered_indices = [
                    i for i in range(len(model_output)) if i not in matched_indices
                ]
                all_errors.insert(
                    0,
                    {
                        "No Matching Function": (
                            {
                                "error_message": f"Could not find a matching function among index {considered_indices} "
                                + f"of model output for index {i} of possible answers.",
                                "possible_answer_item": possible_answers[i],
                            }
                        )
                    },
                )
                return {
                    "valid": False,
                    "error": all_errors,
                    "error_type": "parallel_function_checker_no_order:cannot_find_match",
                }

        return {"valid": True, "error": []}

    @staticmethod
    def parallel_function_checker_with_order(
        func_descriptions: list,
        model_output: list,
        possible_answers: list,
    ) -> dict:
        """Validate multiple function calls (order-aware, position-based matching)."""
        if len(model_output) != len(possible_answers):
            return {
                "valid": False,
                "error": ["Wrong number of functions."],
                "error_type": "parallel_function_checker_with_order:wrong_count",
            }

        all_errors = []
        first_order_violation_index = None

        for i in range(len(possible_answers)):
            func_name_expected = list(possible_answers[i].keys())[0]
            func_description = Check.find_description(
                func_descriptions, func_name_expected
            )

            result = Check.simple_function_checker(
                func_description,
                model_output[i],
                possible_answers[i],
            )

            if not result["valid"]:
                all_errors.append(
                    {
                        f"Model Result Index {i}": {
                            "sub_error": result["error"],
                            "sub_error_type": result["error_type"],
                            "model_output_item": model_output[i],
                            "possible_answer_item": possible_answers[i],
                            "expected_position": i,
                        }
                    }
                )

                if result["error_type"] == "simple_function_checker:wrong_func_name":
                    if first_order_violation_index is None:
                        first_order_violation_index = i

        if all_errors:
            if first_order_violation_index is not None:
                expected_order = [list(pa.keys())[0] for pa in possible_answers]
                actual_order = []
                for mo in model_output:
                    if isinstance(mo, dict) and mo:
                        func_name = list(mo.keys())[0]
                        actual_order.append(func_name)
                    else:
                        actual_order.append("unknown")

                order_error = {
                    "error_message": (
                        f"Function calls are in wrong order. "
                        f"Expected order: {', '.join(expected_order)}. "
                        f"Actual order: {', '.join(actual_order)}. "
                        f"First mismatch at position {first_order_violation_index}."
                    ),
                    "expected_order": expected_order,
                    "actual_order": actual_order,
                    "first_mismatch_position": first_order_violation_index,
                    "detailed_errors": all_errors,
                }

                return {
                    "valid": False,
                    "error": [order_error],
                    "error_type": "parallel_function_checker_with_order:wrong_order",
                }
            else:
                return {
                    "valid": False,
                    "error": all_errors,
                    "error_type": "parallel_function_checker_with_order:validation_error",
                }

        return {"valid": True, "error": []}

    @staticmethod
    def simple_function_checker(
        func_description: dict,
        model_output: dict,
        possible_answer: dict,
    ) -> dict:
        """Validate individual function call (name, parameters, types, values)."""
        possible_answer = list(possible_answer.values())[0]
        func_name = func_description["name"]
        param_details = func_description["parameters"]["properties"]
        required_params = func_description["parameters"]["required"]

        result = {
            "valid": True,
            "error": [],
            "error_type": "simple_function_checker:unclear",
        }

        func_name = Check.convert_func_name(func_name)

        if func_name not in model_output:
            result["valid"] = False
            result["error"].append(
                f"Function name {repr(func_name)} not found in model output."
            )
            result["error_type"] = "simple_function_checker:wrong_func_name"
            return result

        model_params = model_output[func_name]

        for param in required_params:
            if param not in model_params:
                result["valid"] = False
                result["error"].append(f"Missing required parameter: {repr(param)}.")
                result["error_type"] = "simple_function_checker:missing_required"
                return result

        for param, value in model_params.items():
            if param not in param_details or param not in possible_answer:
                result["valid"] = False
                result["error"].append(f"Unexpected parameter: {repr(param)}.")
                result["error_type"] = "simple_function_checker:unexpected_param"
                return result

            full_param_details = param_details[param]
            expected_type_description = full_param_details["type"]
            nested_type_converted = None

            expected_type_converted = Check.PYTHON_TYPE_MAPPING[
                expected_type_description
            ]
            if expected_type_description in Check.PYTHON_NESTED_TYPE_CHECK_LIST:
                nested_type = param_details[param]["items"]["type"]
                nested_type_converted = Check.PYTHON_TYPE_MAPPING[nested_type]

            if expected_type_description == "tuple" and isinstance(value, tuple):
                value = list(value)

            if expected_type_description == "float" and isinstance(value, int):
                value = float(value)

            possible_answer_for_type_check = possible_answer[param]
            if expected_type_converted == list and isinstance(
                possible_answer_for_type_check, list
            ):
                possible_answer_for_type_check = [possible_answer_for_type_check]

            type_check_result = Check.type_checker(
                param,
                value,
                possible_answer_for_type_check,
                expected_type_description,
                expected_type_converted,
                nested_type_converted,
            )
            is_variable = type_check_result["is_variable"]
            if not type_check_result["valid"]:
                return type_check_result

            if expected_type_converted == dict:
                result = Check.exact_object_checker(
                    param, value, possible_answer[param]
                )
                if not result["valid"]:
                    return result
                continue

            if not is_variable:
                if expected_type_converted == list and nested_type_converted == dict:
                    result = Check.listdict_checker(
                        param, value, [possible_answer[param]]
                    )
                    if not result["valid"]:
                        return result
                    continue

                elif expected_type_converted == str:
                    result = Check.string_checker(
                        param, value, [possible_answer[param]]
                    )
                    if not result["valid"]:
                        return result
                    continue

                elif expected_type_converted == list:
                    result = Check.list_checker(param, value, [possible_answer[param]])
                    if not result["valid"]:
                        return result
                    continue

            if value not in possible_answer[param]:
                result["valid"] = False
                result["error"].append(
                    f"Invalid value for parameter {repr(param)}: {repr(value)}. Expected one of {possible_answer[param]}."
                )
                result["error_type"] = "value_error:others"
                return result

        for param in possible_answer:
            if param not in model_params and "" not in possible_answer[param]:
                result["valid"] = False
                result["error"].append(
                    f"Optional parameter {repr(param)} not provided and not marked as optional."
                )
                result["error_type"] = "simple_function_checker:missing_optional"
                return result

        return result

    @staticmethod
    def exact_object_checker(param: str, model_output, expected_output) -> dict:
        """Validate exact structural equality between model_output and expected_output."""
        result = {
            "valid": True,
            "error": [],
            "error_type": "exact_object_checker:unclear",
        }

        def compare_values(actual, expected, path=""):
            current_path = path if path else param

            if actual is None and expected is None:
                return True
            if actual is None or expected is None:
                result["valid"] = False
                result["error"].append(
                    f"Value mismatch at {current_path}: {repr(actual)} vs {repr(expected)}"
                )
                result["error_type"] = "exact_object_checker:value_mismatch"
                return False

            if type(actual) is not type(expected):
                result["valid"] = False
                result["error"].append(
                    f"Type mismatch at {current_path}: {type(actual)} vs {type(expected)}"
                )
                result["error_type"] = "exact_object_checker:type_mismatch"
                return False

            if isinstance(actual, dict):
                for key in actual:
                    if key not in expected:
                        result["valid"] = False
                        result["error"].append(
                            f"Unexpected key '{key}' in {current_path}"
                        )
                        result["error_type"] = "exact_object_checker:unexpected_key"
                        return False

                for key in expected:
                    if key not in actual:
                        result["valid"] = False
                        result["error"].append(f"Missing key '{key}' in {current_path}")
                        result["error_type"] = "exact_object_checker:missing_key"
                        return False

                for key in actual:
                    if not compare_values(
                        actual[key], expected[key], f"{current_path}.{key}"
                    ):
                        return False

                return True

            elif isinstance(actual, list):
                if len(actual) != len(expected):
                    result["valid"] = False
                    result["error"].append(
                        f"List length mismatch at {current_path}: {len(actual)} vs {len(expected)}"
                    )
                    result["error_type"] = "exact_object_checker:length_mismatch"
                    return False

                for i, (a_item, e_item) in enumerate(zip(actual, expected)):
                    if not compare_values(a_item, e_item, f"{current_path}[{i}]"):
                        return False

                return True

            elif isinstance(actual, str):
                if Check.standardize_string(actual) != Check.standardize_string(
                    expected
                ):
                    result["valid"] = False
                    result["error"].append(
                        f"String mismatch at {current_path}: {repr(actual)} vs {repr(expected)}"
                    )
                    result["error_type"] = "exact_object_checker:string_mismatch"
                    return False
                return True

            else:
                if actual != expected:
                    result["valid"] = False
                    result["error"].append(
                        f"Value mismatch at {current_path}: {repr(actual)} vs {repr(expected)}"
                    )
                    result["error_type"] = "exact_object_checker:value_mismatch"
                    return False
                return True

        compare_values(model_output, expected_output)
        return result

    @staticmethod
    def format_function_call_error_message(
        error_type: str | None,
        error: list | dict | None,
    ) -> str:
        """Format error messages into human-readable format."""
        if error_type is None and (
            error is None or (isinstance(error, list) and len(error) == 0)
        ):
            return "Function Call Validation Failed\n\nAST error found, but no details provided."

        if error_type is None:
            error_type = "unknown_error"

        if error is None:
            error = []

        if error_type == "parallel_function_checker_no_order:wrong_count":
            return "Function Call Validation Failed\n\nWrong number of function calls."

        elif error_type == "parallel_function_checker_no_order:cannot_find_match":
            return "Function Call Validation Failed\n\nCould not find matching function call."

        elif error_type == "parallel_function_checker_with_order:wrong_count":
            return "Function Call Validation Failed\n\nWrong number of function calls."

        elif error_type == "parallel_function_checker_with_order:wrong_order":
            return (
                "Function Call Validation Failed\n\nFunction calls are in wrong order."
            )

        elif error_type == "parallel_function_checker_with_order:validation_error":
            return (
                "Function Call Validation Failed\n\nValidation error in function calls."
            )

        else:
            if isinstance(error, list) and len(error) > 0:
                error_str = str(error[0]) if isinstance(error[0], str) else str(error)
            elif isinstance(error, dict):
                error_str = str(error)
            else:
                error_str = str(error)

            return f"Function Call Validation Failed\n\n{error_str}"

    @staticmethod
    def get_possible_answer_type(possible_answer: list):
        """Get the type of the first non-empty answer in the list."""
        for answer in possible_answer:
            if answer != "":
                return type(answer)
        return None

    @staticmethod
    def type_checker(
        param: str,
        value,
        possible_answer: list,
        expected_type_description: str,
        expected_type_converted,
        nested_type_converted,
    ) -> dict:
        """Check if a parameter value matches the expected type."""
        result = {
            "valid": True,
            "error": [],
            "is_variable": False,
            "error_type": "type_error:simple",
        }

        is_variable = False
        possible_answer_type = Check.get_possible_answer_type(possible_answer)
        if possible_answer_type is not None:
            if possible_answer_type != expected_type_converted:
                is_variable = True

        if isinstance(value, expected_type_converted):
            if nested_type_converted is None:
                result["is_variable"] = is_variable
                return result
            else:
                for possible_answer_item in possible_answer:
                    flag = True
                    if isinstance(possible_answer_item, list):
                        for value_item in value:
                            checker_result = Check.type_checker(
                                param,
                                value_item,
                                possible_answer_item,
                                str(nested_type_converted),
                                nested_type_converted,
                                None,
                            )
                            if not checker_result["valid"]:
                                flag = False
                                break

                    if flag:
                        return {"valid": True, "error": [], "is_variable": is_variable}

                result["valid"] = False
                result["error"] = [
                    f"Nested type checking failed for parameter {repr(param)}. Expected outer type "
                    + f"{expected_type_description} with inner type {str(nested_type_converted)}. "
                    + f"Parameter value: {repr(value)}."
                ]
                result["error_type"] = "type_error:nested"

        possible_answer_type = Check.get_possible_answer_type(possible_answer)
        if possible_answer_type is not None:
            if isinstance(value, possible_answer_type):
                result["is_variable"] = True
                return result

        result["valid"] = False
        result["error"].append(
            f"Incorrect type for parameter {repr(param)}. Expected type {expected_type_description}, "
            + f"got {type(value)}. Parameter value: {repr(value)}."
        )
        result["error_type"] = "type_error:simple"
        return result

    @staticmethod
    def standardize_string(input_string: str) -> str:
        """Standardize string by removing spaces, punctuation, and converting to lowercase."""
        regex_string = r"[ \,\.\/\-\_\*\^]"
        return re.sub(regex_string, "", input_string).lower().replace("'", '"')

    @staticmethod
    def dict_checker(param: str, model_output: dict, possible_answers: list) -> dict:
        """Check if a dictionary parameter matches any of the possible answer dictionaries."""
        result = {"valid": False, "error": [], "error_type": "dict_checker:unclear"}
        for i in range(len(possible_answers)):
            if possible_answers[i] == "":
                continue

            result = {"valid": False, "error": [], "error_type": "dict_checker:unclear"}

            flag = True

            possible_answer = possible_answers[i]

            for key, value in model_output.items():
                if key not in possible_answer:
                    result["valid"] = False
                    result["error"].append(f"Unexpected dict key parameter: '{key}'.")
                    result["error_type"] = "value_error:dict_key"
                    flag = False
                    break

                standardize_value = value
                if isinstance(value, str):
                    standardize_value = Check.standardize_string(value)

                standardize_possible_answer = []
                for j in range(len(possible_answer[key])):
                    if isinstance(possible_answer[key][j], str):
                        standardize_possible_answer.append(
                            Check.standardize_string(possible_answer[key][j])
                        )
                    else:
                        standardize_possible_answer.append(possible_answer[key][j])

                if standardize_value not in standardize_possible_answer:
                    result["valid"] = False
                    result["error"].append(
                        f"Invalid value for parameter {repr(key)}: {repr(value)}. "
                        + "Expected one of {standardize_possible_answer}."
                    )
                    result["error_type"] = "value_error:dict_value"
                    flag = False
                    break

            for key, value in possible_answer.items():
                if key not in model_output and "" not in value:
                    result["valid"] = False
                    result["error"].append(f"Missing dict key parameter: '{key}'.")
                    result["error_type"] = "value_error:dict_key"
                    flag = False
                    break

            if flag:
                return {"valid": True, "error": []}

        return result

    @staticmethod
    def listdict_checker(
        param: str, model_output: list, possible_answers: list
    ) -> dict:
        """Check if a list of dictionaries parameter matches any of the possible answer lists."""
        result = {
            "valid": False,
            "error": [],
            "error_type": "listdict_checker:unclear",
        }

        for answer_index in range(len(possible_answers)):
            flag = True

            if len(model_output) != len(possible_answers[answer_index]):
                result["valid"] = False
                result["error"] = ["Wrong number of dictionaries in the list."]
                result["error_type"] = "value_error:list_dict_count"
                flag = False
                continue

            for dict_index in range(len(model_output)):
                result = Check.dict_checker(
                    param,
                    model_output[dict_index],
                    [possible_answers[answer_index][dict_index]],
                )
                if not result["valid"]:
                    flag = False
                    break
            if flag:
                return {"valid": True, "error": []}

        return result

    @staticmethod
    def string_checker(param: str, model_output: str, possible_answer: list) -> dict:
        """Check if a string parameter value matches any of the possible answers."""
        standardize_possible_answer = []
        standardize_model_output = Check.standardize_string(model_output)
        for i in range(len(possible_answer)):
            if isinstance(possible_answer[i], str):
                standardize_possible_answer.append(
                    Check.standardize_string(possible_answer[i])
                )

        if standardize_model_output not in standardize_possible_answer:
            return {
                "valid": False,
                "error": [
                    (
                        f"Invalid value for parameter {repr(param)}: {repr(model_output)}. "
                        + f"Expected one of {possible_answer}. Case insensitive."
                    )
                ],
                "error_type": "value_error:string",
            }

        return {"valid": True, "error": []}

    @staticmethod
    def list_checker(param: str, model_output: list, possible_answer: list) -> dict:
        """Check if a list/tuple parameter value matches any of the possible answers."""
        standardize_model_output = list(model_output)

        for i in range(len(standardize_model_output)):
            if isinstance(standardize_model_output[i], str):
                standardize_model_output[i] = Check.standardize_string(model_output[i])

        standardize_possible_answer = []
        for i in range(len(possible_answer)):
            standardize_possible_answer.append([])
            for j in range(len(possible_answer[i])):
                if isinstance(possible_answer[i][j], str):
                    standardize_possible_answer[i].append(
                        Check.standardize_string(possible_answer[i][j])
                    )
                else:
                    standardize_possible_answer[i].append(possible_answer[i][j])

        if standardize_model_output not in standardize_possible_answer:
            return {
                "valid": False,
                "error": [
                    f"Invalid value for parameter {repr(param)}: {repr(model_output)}. Expected one of {possible_answer}."
                ],
                "error_type": "value_error:list/tuple",
            }

        return {"valid": True, "error": []}

    @staticmethod
    def find_description(func_descriptions, name):
        """Find function description by name."""
        if isinstance(func_descriptions, list):
            for func_description in func_descriptions:
                if func_description["name"] == name:
                    return func_description
            return None
        else:
            return func_descriptions

    @staticmethod
    def convert_func_name(function_name: str) -> str:
        """Convert function name (replace dots with underscores)."""
        if "." in function_name:
            return re.sub(r"\.", "_", function_name)
        return function_name
