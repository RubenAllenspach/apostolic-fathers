#!/usr/bin/env python3

import re

from lxml import etree

NS = {"TEI": "http://www.tei-c.org/ns/1.0"}

with open("raw-ogl-lake/tlg1622.tlg001.1st1K-grc1.xml") as f:
    tree = etree.parse(f)
    for part in tree.xpath("TEI:text/TEI:body/TEI:div[@type='edition']/TEI:div[@type='textpart']", namespaces=NS):
        assert part.attrib["subtype"] == "chapter"
        chapter = part.attrib["n"]
        if chapter == "preface" or chapter == "praef":
            chapter = 0
        else:
            chapter = int(chapter)
        for child in part:
            if child.tag == "{http://www.tei-c.org/ns/1.0}p":
                verse = 0
                text = re.sub("\s+", " ", child.xpath("string()").strip())
                print(f"{chapter}.{verse} {text}")
            elif child.tag == "{http://www.tei-c.org/ns/1.0}div":
                assert child.attrib["subtype"] == "section"
                verse = int(child.attrib["n"])
                print(f"{chapter}.{verse}", end="")
                for gchild in child:
                    if gchild.tag == "{http://www.tei-c.org/ns/1.0}p":
                        print("", re.sub("\s+", " ", gchild.text).strip(), end="")
                        for ggchild in gchild:
                            print("", re.sub("\s+", " ", ggchild.tail).strip(), end="")
                    else:
                        assert False
                print()
            else:
                assert False