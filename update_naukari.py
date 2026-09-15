from pathlib import Path
import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

BASE = Path(__file__).resolve().parent
load_dotenv(BASE / ".env")
SHOTS = BASE / "screenshots"
SHOTS.mkdir(exist_ok=True)
USER_DATA = BASE / "chrome-profile"
PROFILE_URL = "https://www.naukri.com/mnjuser/profile"


def main():
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            user_data_dir=str(USER_DATA),
            headless=False,
            channel="chrome",
            ignore_https_errors=True,
            viewport={"width": 1366, "height": 900},
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto(PROFILE_URL, wait_until="domcontentloaded", timeout=90000)
        page.wait_for_timeout(4000)
        page.screenshot(path=str(SHOTS / "step1.png"))

        card_html = page.evaluate(
            """
            () => {
              const nodes = [...document.querySelectorAll('*')];
              const hit = nodes.find(e => {
                const t = (e.innerText || '').trim();
                return t.startsWith('Resume headline') || t.startsWith('Resume Headline');
              });
              if (!hit) return 'HEADLINE_NOT_FOUND';
              const box = hit.closest('section, article, li, .widget, .card') || hit.parentElement || hit;
              return box.outerHTML.slice(0, 4000);
            }
            """
        )
        (SHOTS / "headline_card.html").write_text(card_html, encoding="utf-8")
        print("Wrote screenshots/headline_card.html")
        print(card_html[:500])

        # Click pencil/edit inside the same card as "Resume headline"
        card = page.locator("section, article, div").filter(has_text="Resume headline").first
        inner = [
            card.get_by_title("Edit"),
            card.locator("[class*='edit' i]"),
            card.locator("em, i, svg, button, span.icon, .icon"),
            card.get_by_text("Edit", exact=False),
        ]
        clicked = False
        for i, loc in enumerate(inner):
            try:
                loc.last.click(timeout=2500)
                print("Clicked inner control", i)
                clicked = True
                break
            except Exception as e:
                print("Inner skip", i, str(e)[:70])

        page.wait_for_timeout(2000)
        page.screenshot(path=str(SHOTS / "step2.png"))

        # Try fill + save if a drawer/modal opened
        filled = False
        for sel in ["textarea", "[contenteditable='true']", "div[role='textbox']"]:
            loc = page.locator(sel).last
            try:
                if loc.is_visible(timeout=1500):
                    cur = ""
                    try:
                        cur = loc.input_value()
                    except Exception:
                        cur = loc.inner_text()
                    print("Found editor:", (cur or "")[:80])
                    new = cur[:-1] if (cur or "").endswith(".") else (cur or "Updated") + "."
                    try:
                        loc.fill(new)
                    except Exception:
                        loc.click()
                        page.keyboard.press("End")
                        page.keyboard.type(".")
                    filled = True
                    break
            except Exception:
                continue

        saved = False
        for sel in ["button:has-text('Save')", "button:has-text('SAVE')", "#saveResumeHeadline"]:
            try:
                page.locator(sel).last.click(timeout=2000)
                print("Clicked Save")
                saved = True
                break
            except Exception:
                continue

        page.wait_for_timeout(2000)
        page.screenshot(path=str(SHOTS / ("success.png" if saved else "save_failed.png")))
        print("CLICKED_PENCIL:", clicked, "FILLED:", filled, "SAVED:", saved)
        ctx.close()


if __name__ == "__main__":
    main()
