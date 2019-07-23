from sbol import * # noqa
import os
import sys

TESTSDIR = os.path.dirname(os.path.abspath(__file__))
PARENTDIR = os.path.dirname(TESTSDIR)
SRCDIR = os.path.join(PARENTDIR, 'src')
sys.path.insert(0, SRCDIR)

from componentbuckets import addPlasmidParts, resetModules, setNames, createFunctionalComponents # noqa


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

    return (cd, subCD1, subCD2, subCD3)


def createModules():
    device_test_context = ModuleDefinition('context') # noqa
    device_test = ModuleDefinition('device_test') # noqa
    device = ModuleDefinition('device') # noqa

    device_test_submod = device_test_context.modules.create('device_test')
    device_test_submod.definition = device_test.identity

    device_submod = device_test.modules.create('device')
    device_submod.definition = device.identity

    return (device_test_context, device_test, device)


def test_addingPlasmidParts():
    doc = Document() # noqa
    setHomespace('https://bu.edu/ben') # noqa
    Config.setOption('sbol_compliant_uris', True) # noqa
    Config.setOption('sbol_typed_uris', False) # noqa

    testCD, subCD1, subCD2, subCD3 = createTestCD()
    device_test_context, device_test, device = createModules()
    fc = device.functionalComponents.create('TestCD_sub1')
    fc.definition = subCD1.identity
    fc = device.functionalComponents.create('TestCD_sub2')
    fc.definition = subCD2.identity

    doc.addModuleDefinition(device_test)
    doc.addModuleDefinition(device)

    originalCDs = [testCD]
    plasmidPartDictionary = {}
    addedPlasmidParts = {}

    addPlasmidParts(doc, originalCDs, device_test, device, plasmidPartDictionary, addedPlasmidParts) # noqa

    cd = doc.componentDefinitions[0]
    assert cd.displayId == 'TestCD__sub1__sub2'
    assert len(cd.components) == 2

    componentDisplayIds = [c.displayId for c in cd.components]
    assert 'TestCD_sub1' in componentDisplayIds
    assert 'TestCD_sub2' in componentDisplayIds
    assert 'TestCD_sub3' not in componentDisplayIds

    componentDefinitions = [c.definition for c in cd.components]
    assert subCD1.identity in componentDefinitions
    assert subCD2.identity in componentDefinitions
    assert subCD3.identity not in componentDefinitions


def test_resettingModules():
    testCD, subCD1, subCD2, subCD3 = createTestCD()
    device_test_context, device_test, device = createModules()
    fc = device.functionalComponents.create('TestCD_sub1')
    fc.definition = subCD1.identity
    fc = device.functionalComponents.create('TestCD_sub2')
    fc.definition = subCD2.identity

    resetModules(device_test_context, device_test, device)

    assert len(device_test_context.functionalComponents) == 0
    assert len(device_test.functionalComponents) == 0
    assert len(device.functionalComponents) == 0


def test_settingNames():
    class TestWidget:
        def __init__(self, name):
            self.value = name

    names = [TestWidget('bob'), TestWidget('joe'), TestWidget('john')]
    device_test_context, device_test, device = createModules()

    setNames(device_test_context, device_test, device, names)

    assert device_test_context.name == 'bob'
    assert device_test.name == 'joe'
    assert device.name == 'john'


def test_creatingFunctionalComponents():
    class TestWidget:
        def __init__(self, selectedList):
            self.options = selectedList

    doc = Document() # noqa
    setHomespace('https://bu.edu/ben') # noqa
    Config.setOption('sbol_compliant_uris', True) # noqa
    Config.setOption('sbol_typed_uris', False) # noqa

    testCD, subCD1, subCD2, subCD3 = createTestCD()
    device_test_context, device_test, device = createModules()
    doc.addComponentDefinition(testCD)
    doc.addComponentDefinition(subCD1)
    doc.addComponentDefinition(subCD2)
    doc.addComponentDefinition(subCD3)

    selectedNames = ['TestCD_subCD1', 'TestCD_subCD2', 'TestCD_subCD3']

    dtcSelected = TestWidget([])
    dtSelected = TestWidget([])
    dSelected = TestWidget(selectedNames)

    selectedLists = [dtcSelected, dtSelected, dSelected]
    cdDisplayIDMap = {'TestCD_subCD1': subCD1,
                      'TestCD_subCD2': subCD2,
                      'TestCD_subCD3': subCD3}
    modulesDictionary = {'Device-Test-Context': device_test_context,
                         'Device-Test': device_test,
                         'Device': device}
    moduleNames = ['Device-Test-Context', 'Device-Test', 'Device']
    fcDictionary = {}

    createFunctionalComponents(doc,
                               selectedLists,
                               cdDisplayIDMap,
                               modulesDictionary,
                               moduleNames,
                               fcDictionary)

    assert len(device_test_context.functionalComponents) == 0
    assert len(device_test.functionalComponents) == 0
    assert len(device.functionalComponents) == 3

    for fc in device.functionalComponents:
        assert fc.displayId in selectedNames


if __name__ == '__main__':
    test_addingPlasmidParts()
    test_resettingModules()
    test_settingNames()
    test_creatingFunctionalComponents()
