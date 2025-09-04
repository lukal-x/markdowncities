from markdown import markdown
from types import SimpleNamespace

import os

var = SimpleNamespace(
    start="<!-- KyuWeb Doc Start /-->",
    end="<!-- KyuWeb Doc End /-->",
    meta="<!-- Metadata /-->"
)

with open("source/template.html", "r") as f:
    template = f.read()

    for md in os.listdir("source"):
        if not md.endswith(".md"):
            continue

        with open(f"source/{md}") as mdf:
            content = mdf.read()
            title = md.rstrip(".md").replace("-", " ").capitalize()
        
            result = template

            for k, v in {
                "start": markdown(content),
                "end": "",
                "meta": f"<title>{title}</title>"
            }.items():
                result = result.replace(getattr(var, k), v)

            newfile = md.rstrip(".md") + ".html"
            with open(f"build/{newfile}", "w") as htmf:
                htmf.write(result)
