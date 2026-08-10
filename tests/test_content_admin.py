# tests/test_content_admin.py
import pytest
from services.content_manager import save_template, get_template, preview_template

@pytest.mark.asyncio
async def test_template_save_and_preview():
    tpl = await save_template("TEST_TEMPLATE", "Hello {first_name}", 1)
    assert tpl.key == "TEST_TEMPLATE"
    prev = await preview_template(tpl.content, {"first_name": "Alex"})
    assert "Alex" in prev
