from typing import TYPE_CHECKING

from mock import call, MagicMock

from grouper.constants import PERMISSION_ADMIN, PERMISSION_CREATE
from grouper.models.permission import Permission

if TYPE_CHECKING:
    from tests.setup import SetupTest


def test_permission_disable(setup):
    # type: (SetupTest) -> None
    setup.grant_permission_to_group(PERMISSION_ADMIN, "", "admins")
    setup.add_user_to_group("gary@a.co", "admins")
    setup.create_permission("some-permission")
    setup.commit()
    mock_ui = MagicMock()
    usecase = setup.usecase_factory.create_disable_permission_usecase("gary@a.co", mock_ui)
    usecase.disable_permission("some-permission")
    assert mock_ui.mock_calls == [call.disabled_permission("some-permission")]
    assert not Permission.get(setup.session, name="some-permission").enabled


def test_permission_disable_denied(setup):
    # type: (SetupTest) -> None
    setup.create_user("zorkian@a.co")
    setup.create_permission("some-permission")
    setup.commit()
    mock_ui = MagicMock()
    usecase = setup.usecase_factory.create_disable_permission_usecase("zorkian@a.co", mock_ui)
    usecase.disable_permission("some-permission")
    assert mock_ui.mock_calls == [
        call.disable_permission_failed_because_permission_denied("some-permission")
    ]
    assert Permission.get(setup.session, name="some-permission").enabled


def test_permission_disable_system(setup):
    # type: (SetupTest) -> None
    setup.grant_permission_to_group(PERMISSION_ADMIN, "", "admins")
    setup.add_user_to_group("gary@a.co", "admins")
    setup.create_permission(PERMISSION_CREATE)
    setup.commit()
    mock_ui = MagicMock()
    usecase = setup.usecase_factory.create_disable_permission_usecase("gary@a.co", mock_ui)
    usecase.disable_permission(PERMISSION_CREATE)
    assert mock_ui.mock_calls == [
        call.disable_permission_failed_because_system_permission(PERMISSION_CREATE)
    ]


def test_permission_not_found(setup):
    # type: (SetupTest) -> None
    setup.grant_permission_to_group(PERMISSION_ADMIN, "", "admins")
    setup.add_user_to_group("gary@a.co", "admins")
    setup.commit()
    mock_ui = MagicMock()
    usecase = setup.usecase_factory.create_disable_permission_usecase("gary@a.co", mock_ui)
    usecase.disable_permission("nonexistent")
    assert mock_ui.mock_calls == [call.disable_permission_failed_because_not_found("nonexistent")]
