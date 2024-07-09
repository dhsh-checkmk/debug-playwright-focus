"""Document playwright code to run using pytest."""

import re
from collections.abc import Iterator

import pytest
from playwright.sync_api import (
    BrowserType,
    BrowserContext,
    FrameLocator,
    Page,
    sync_playwright,
)

URL = "http://127.0.0.1:8080/cmk/check_mk/login.py"
PASSWORD = ""  # UPDATE ME! Follow instructions in README.md

@pytest.fixture(name="page")
def _page() -> Iterator[Page]:
    pw = sync_playwright().start()
    chromium: BrowserType = pw.chromium
    browser = chromium.launch(
        headless=False,
    )
    context: BrowserContext = browser.new_context()
    page: Page = context.new_page()
    yield page
    page.close()
    context.close()
    browser.close()


@pytest.fixture(name="setup")
def _setup(page: Page) -> FrameLocator:
    # login
    page.goto(URL, wait_until="load")
    page.locator("#input_user").fill("cmkadmin")
    page.locator("#input_pass").fill(PASSWORD)
    page.locator("#_login").click()
    page.wait_for_url(re.compile("dashboard.py$"), wait_until="load")
    # Navigate to desired page

    page.get_by_role(role="link", name="Help").click()
    page.get_by_role(role="link", name="Change log (Werks)").click()
    page.wait_for_url(re.compile("change_log.py$"), wait_until="load")
    main_area: FrameLocator = page.frame_locator("iframe[name='main']")
    # Apply filters
    main_area.get_by_role(role="link", name="Filter").click()
    main_area.locator("#popup_filters").locator(
        "#wo_grouping"
    ).select_option(label="Day of creation")
    main_area.get_by_role(role="button", name="Apply").click()
    page.wait_for_load_state("load")
    return main_area


def test_focus_click(setup: FrameLocator, page: Page):
    """Reproduce bug.

    Aim is to reproduce the bug, originally filed at
    https://github.com/microsoft/playwright-python/issues/2481

    `focus` and `click` for a partially visible `locator` misbehave.
    """
    _id: int = 17119
    # expectation: scroll and place the locator at the centre of the `viewport`
    # observation: `locator` remains at the edge of the viewport
    setup.get_by_role(role="link", name=f"#{_id}").focus()
    # expectation: navigates to the desired link when the locator is `click`ed
    # observation: no navigation is performed
    setup.get_by_role(role="link", name=f"#{_id}").click()
    page.wait_for_url(re.compile(f"{_id}$"), wait_until="load")
