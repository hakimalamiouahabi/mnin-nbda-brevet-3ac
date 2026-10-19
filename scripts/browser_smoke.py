#!/usr/bin/env python3
"""Diagnostic autonome du navigateur de développement. Sans accès à WordPress."""
import argparse
import asyncio
import json
import sys
from pathlib import Path

async def run(args):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        options = {"headless": True}
        if args.executable:
            executable = Path(args.executable).expanduser()
            if not executable.is_file():
                raise FileNotFoundError("os error 3 : exécutable introuvable : " + str(executable))
            options["executable_path"] = str(executable)
        elif args.channel:
            options["channel"] = args.channel
        browser = await p.chromium.launch(**options)
        try:
            page = await browser.new_page(viewport={"width": 390, "height": 844})
            await page.set_content('<html lang="fr"><head><title>MNIN</title></head><body><h1>MNIN Browser QA</h1></body></html>')
            assert await page.title() == "MNIN"
            output = Path(".mnin-private")
            output.mkdir(exist_ok=True)
            await page.screenshot(path=str(output/"browser-smoke.png"))
            print(json.dumps({"status":"PASS","browser_version":browser.version,
                "capture":str(output/"browser-smoke.png"),
                "note":"Navigateur indépendant opérationnel ; navigateur interne Codex non testé."}))
        finally:
            await browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--channel", choices=["msedge","chrome"])
    parser.add_argument("--executable")
    opts = parser.parse_args()
    try:
        asyncio.run(run(opts))
    except Exception as error:
        print("BLOQUE — " + str(error), file=sys.stderr)
        print("Vérifier chemin et tenter python -m playwright install chromium ou --channel msedge.",file=sys.stderr)
        sys.exit(3)
