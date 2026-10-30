class CreateScenarioError(Exception):
    pass


class MissingApiKeyError(Exception):
    pass


class MissingVectorDbError(Exception):
    pass


class TestRunError(Exception):
    pass


class ListenerBindError(RuntimeError):
    """A custom multiturn Target's ``bind_listener`` raised, ended cancelled,
    ran past its time, or returned something that is not a release: the Run is
    not started. It is the cause of the ``TestRunError`` the caller sees."""
