"""Tests for the additional Homework 1 return-eligibility tool."""

from __future__ import annotations

from agent import tools
from agent.auth import AuthContext


SHOPPER_1 = AuthContext(user_id=1, role="shopper")
SHOPPER_2 = AuthContext(user_id=2, role="shopper")
SUPPORT = AuthContext(user_id=9501, role="support")


def test_check_return_eligibility_for_eligible_order(world: dict) -> None:
    result = tools.check_return_eligibility(SHOPPER_1, 4127)
    assert result["ok"] is True
    assert result["eligible"] is True
    assert result["return_window_days"] == 30


def test_check_return_eligibility_for_ineligible_order(world: dict) -> None:
    result = tools.check_return_eligibility(SHOPPER_1, 3980)
    assert result["ok"] is True
    assert result["eligible"] is False
    assert result["return_window_days"] == 30


def test_check_return_eligibility_respects_scope(world: dict) -> None:
    result = tools.check_return_eligibility(SHOPPER_2, 4127)
    assert result["ok"] is False
    assert result["error"] == "permission_denied"


def test_check_return_eligibility_uses_store_override(world: dict) -> None:
    # Order 38 belongs to Northwind Books, whose policy overrides the
    # platform's 30-day window with a 45-day window.
    result = tools.check_return_eligibility(SUPPORT, 38)
    assert result["ok"] is True
    assert result["return_window_days"] == 45
