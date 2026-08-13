import pytest
from datetime import datetime
import html
BASE_URL = "https://xabeta.com/en"

def test_accessibility(browser):
    page = browser.new_page()
    url = BASE_URL

    page.goto(url, wait_until="networkidle")
    page.wait_for_selector("body")

    page.add_script_tag(
        url="https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.6.3/axe.min.js"
    )

    results = page.evaluate("""
        async () => {
            return await axe.run();
        }
    """)

    violations = results.get("violations", [])

    generate_html_report(violations, url)

    serious = [v for v in violations if v["impact"] in ("serious", "critical")]
    assert len(serious) == 0, f"Found {len(serious)} serious accessibility issues on {url}"


def generate_html_report(violations, url):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Назва файлу залежно від URL
    safe_url = url.replace("://", "_").replace("/", "_")
    report_file = f"axe_report_{safe_url}_{timestamp}.html"

    html_content = f"""
    <html>
    <head>
        <meta charset="UTF-8" />
        <title>Accessibility Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; padding: 20px; }}
            h1 {{ color: #4A90E2; }}
            .violation {{ border: 1px solid #ccc; padding: 10px; margin-bottom: 15px; border-radius: 5px; }}
            .impact-critical {{ background-color: #ffcccc; }}
            .impact-serious {{ background-color: #ffe0cc; }}
            .impact-moderate {{ background-color: #fff0cc; }}
            .impact-minor {{ background-color: #f7f7f7; }}
            code {{
                display: block;
                white-space: pre-wrap;
                word-break: break-all;
                background: #f0f0f0;
                padding: 5px;
                border-radius: 4px;
                margin-bottom: 5px;
            }}
        </style>
    </head>
    <body>
        <h1>Accessibility Report</h1>
        <p><strong>Tested URL:</strong> {url}</p>
        <p><strong>Generated:</strong> {timestamp}</p>
        <h2>Total violations: {len(violations)}</h2>
    """

    for v in violations:
        html_content += f"""
        <div class="violation impact-{v['impact']}">
            <h3>{v['id']} ― <span>{v['impact']}</span></h3>
            <p><strong>Description:</strong> {v['description']}</p>
            <p><strong>Help:</strong> <a href="{v['helpUrl']}">{v['help']}</a></p>
            <h4>Nodes:</h4>
        """
        for node in v["nodes"]:
            pretty_html = html.escape(node['html']).replace("><", ">\n<")
            html_content += f"<code>{pretty_html}</code>"

        html_content += "</div>"

    html_content += "</body></html>"

    with open(report_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"HTML report saved to {report_file}")
