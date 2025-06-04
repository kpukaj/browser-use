import asyncio
import sys

import pytest

from browser_use.agent.tests import action_registry, sample_history
from browser_use.browser import BrowserProfile


@pytest.mark.asyncio
async def test_save_playwright_script(tmp_path):
	pytest.importorskip('playwright.async_api')
	history = sample_history(action_registry())
	script_path = tmp_path / 'workflow.py'
	history.save_as_playwright_script(script_path, browser_profile=BrowserProfile(headless=True))
	assert script_path.exists()

	proc = await asyncio.create_subprocess_exec(
		sys.executable,
		str(script_path),
		stdout=asyncio.subprocess.PIPE,
		stderr=asyncio.subprocess.PIPE,
	)
	await proc.communicate()
	assert proc.returncode == 0
