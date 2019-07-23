# import pytest
from sbol import * # noqa
import os
import sys

TESTSDIR = os.path.dirname(os.path.abspath(__file__))
PARENTDIR = os.path.dirname(TESTSDIR)
SRCDIR = os.path.join(PARENTDIR, 'src')
sys.path.insert(0, SRCDIR)

from componentsingle import addComponent, typesMap, rolesMap # noqa


def test_successfulAdd():
    doc = Document() # noqa
    setHomespace('https://bu.edu/ben') # noqa
    Config.setOption('sbol_compliant_uris', True) # noqa
    Config.setOption('sbol_typed_uris', False) # noqa
    addedCDs = []

    componentName = 'araC'
    componentType = 'Protein'
    componentRole = ''

    addComponent(doc, addedCDs, componentName, componentType, componentRole)

    addedCD = doc.componentDefinitions[0]

    assert addedCD.displayId == componentName
    assert addedCD.types[0] == typesMap[componentType]
    assert len(addedCD.roles) == 0


def test_addSame():
    doc = Document() # noqa
    setHomespace('https://bu.edu/ben') # noqa
    Config.setOption('sbol_compliant_uris', True) # noqa
    Config.setOption('sbol_typed_uris', False) # noqa
    addedCDs = []

    componentName = 'araC'
    componentType = 'Protein'
    componentRole = ''

    addComponent(doc, addedCDs, componentName, componentType, componentRole)
    addComponent(doc, addedCDs, componentName, componentType, componentRole)

    assert len(doc.componentDefinitions) == 1


def test_illegalName():
    doc = Document() # noqa
    setHomespace('https://bu.edu/ben') # noqa
    Config.setOption('sbol_compliant_uris', True) # noqa
    Config.setOption('sbol_typed_uris', False) # noqa
    addedCDs = []

    componentName = '#$%^&*'
    componentType = 'Protein'
    componentRole = ''

    addComponent(doc, addedCDs, componentName, componentType, componentRole)

    assert len(doc.componentDefinitions) == 0
