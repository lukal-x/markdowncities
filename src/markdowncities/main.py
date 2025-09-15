from markdown import markdown
from markdown.extensions import toc
from types import SimpleNamespace

import os

var = SimpleNamespace(
    start="<!-- KyuWeb Doc Start /-->",
    end="<!-- KyuWeb Doc End /-->",
    meta="<!-- Metadata /-->",
)

with open("sources/template.html", "r") as f:
    template = f.read()

    for md in os.listdir("sources"):
        if not md.endswith(".md"):
            continue

        with open(f"sources/{md}") as mdf:
            content = mdf.read()
            slug = md.rstrip(".md")

            *_, design = slug.split(".")
            has_design = design != slug

            if has_design:
                if os.path.exists(f"sources/template.{design}.html"):
                    with open(f"sources/template.{design}.html", "r") as f:
                        template = f.read()

                slug = slug.replace(f".{design}", "")

            title = slug.replace("-", " ").capitalize()

            result = template

            for k, v in {
                "start": markdown(
                    content, extensions=["attr_list", "fenced_code", toc.TocExtension(permalink=True)]
                ),
                "end": "",
                "meta": f"<title>{title}</title>",
            }.items():
                result = result.replace(getattr(var, k), v)

            newfile = slug + ".html"
            with open(f"docs/{newfile}", "w") as htmf:
                htmf.write(result)
