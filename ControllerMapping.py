from xml.etree import cElementTree as ElementTree
from collections import defaultdict

def etree_to_dict(t):
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {t.tag: {k: v[0] if len(v) == 1 else v
                     for k, v in dd.items()}}
    if t.attrib:
        d[t.tag].update(('@' + k, v)
                        for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
                d[t.tag]['#text'] = text
        else:
            d[t.tag] = text
    return d


""" Function reads in an xml file containing controller information and returns a python dictionary of key mappings """
def getController(xml_file = "controllerconfig.xml", profile_name = "BDSP"):
    tree = ElementTree.parse(xml_file)
    root = tree.getroot()
    for profile in root.findall('Profile'):
        if profile.attrib['name'] == profile_name:
            return( etree_to_dict(profile)["Profile"] )