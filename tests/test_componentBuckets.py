from sbol import * # noqa
import os
import sys

TESTSDIR = os.path.dirname(os.path.abspath(__file__))
PARENTDIR = os.path.dirname(TESTSDIR)
SRCDIR = os.path.join(PARENTDIR, 'src')
sys.path.insert(0, SRCDIR)

from componentsingle import addComponent, typesMap, rolesMap # noqa


def createTestCD():
    setHomespace('https://bu.edu/ben') # noqa
    cd = ComponentDefinition('TestCD', BIOPAX_DNA) # noqa
    subCD1 = ComponentDefinition('SubCD1', BIOPAX_DNA) # noqa
    subCD2 = ComponentDefinition('SubCD2', BIOPAX_DNA) # noqa
    subCD3 = ComponentDefinition('SubCD3', BIOPAX_DNA) # noqa

    sub1 = cd.components.create('sub1')
    sub2 = cd.components.create('sub2')
    sub3 = cd.components.create('sub3')

    sub1.definition = subCD1.identity
    sub2.definition = subCD2.identity
    sub3.definition = subCD3.identity

    return cd


def test_addPlasmidParts():
    return None
