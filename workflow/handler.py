"""
workflow/handler.py
Workflow handling utilities for GSoC-2026-MoganLab.
Fixes #2: Replace generic error messages with descriptive ones.
"""


class WorkflowError(Exception):
    """Base exception for workflow handling errors."""
    pass


def load_workflow(file_path):
    """
    Load a workflow configuration from the given file path.

    Args:
        file_path (str): Path to the workflow config file.

    Returns:
        dict: Parsed workflow configuration.

    Raises:
        WorkflowError: If the file is missing, empty, or invalid.
    """
    if not file_path:
        raise WorkflowError(
            "Workflow loading failed: 'file_path' must not be empty. "
            "Provide a valid path to a workflow configuration file."
        )

    try:
        with open(file_path, "r") as f:
            content = f.read()
    except FileNotFoundError:
        raise WorkflowError(
            f"Workflow loading failed: the file '{file_path}' was not found. "
            f"Check that the path is correct and the file exists."
        )
    except PermissionError:
        raise WorkflowError(
            f"Workflow loading failed: permission denied when reading '{file_path}'. "
            f"Check file permissions and try again."
        )

    if not content.strip():
        raise WorkflowError(
            f"Workflow loading failed: the file '{file_path}' is empty. "
            f"A valid workflow file must contain at least one step definition."
        )

    return {"source": file_path, "content": content}


def validate_workflow(workflow):
    """
    Validate a loaded workflow configuration.

    Args:
        workflow (dict): Workflow config returned by load_workflow().

    Raises:
        WorkflowError: If required fields are missing or invalid.
    """
    if not isinstance(workflow, dict):
        raise WorkflowError(
            f"Workflow validation failed: expected a dict, "
            f"got {type(workflow).__name__}. "
            f"Pass the output of load_workflow() directly."
        )

    if "steps" not in workflow:
        raise WorkflowError(
            "Workflow validation failed: the 'steps' key is missing. "
            "Every workflow must define a list of steps to execute."
        )

    steps = workflow["steps"]

    if not isinstance(steps, list) or len(steps) == 0:
        raise WorkflowError(
            "Workflow validation failed: 'steps' must be a non-empty list. "
            "Add at least one step to the workflow definition."
        )

    for i, step in enumerate(steps):
        if "name" not in step:
            raise WorkflowError(
                f"Workflow validation failed: step at index {i} is missing "
                f"the required 'name' field. Each step must have a unique name."
            )
        if "action" not in step:
            raise WorkflowError(
                f"Workflow validation failed: step '{step.get('name', i)}' "
                f"is missing the required 'action' field. "
                f"Specify what action this step should perform."
            )


def execute_step(step, context):
    """
    Execute a single workflow step.

    Args:
        step (dict): Step definition with 'name' and 'action'.
        context (dict): Shared execution context passed between steps.

    Raises:
        WorkflowError: If the step or context is invalid.
    """
    if not isinstance(step, dict):
        raise WorkflowError(
            f"Step execution failed: expected step to be a dict, "
            f"got {type(step).__name__}."
        )

    if not isinstance(context, dict):
        raise WorkflowError(
            f"Step execution failed: expected context to be a dict, "
            f"got {type(context).__name__}."
        )

    step_name = step.get("name", "<unnamed>")
    action = step.get("action")

    if not callable(action):
        raise WorkflowError(
            f"Step execution failed: the 'action' of step '{step_name}' "
            f"must be a callable (function), but got "
            f"{type(action).__name__}. "
            f"Assign a valid function to the 'action' key."
        )

    try:
        action(context)
    except Exception as exc:
        raise WorkflowError(
            f"Step '{step_name}' raised an unexpected error "
            f"during execution: {exc}. "
            f"Check the step's action function for bugs."
        ) from exc


def run
