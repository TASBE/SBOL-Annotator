from sbol import * # noqa
import os
import sys

TESTSDIR = os.path.dirname(os.path.abspath(__file__))
PARENTDIR = os.path.dirname(TESTSDIR)
SRCDIR = os.path.join(PARENTDIR, 'src')
sys.path.insert(0, SRCDIR)

from addinginteractions import findPlasmid, createInteraction, mapInteractions, createMapsTos # noqa


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


def test_findCorrectPlasmid():
    # Using a ComponentDefinition as a Functional Component
    # Plasmid is Test
    cd = ComponentDefinition('Test_fc') # noqa
    fcDictionary = {'Test_fc': 'fc'}

    name = findPlasmid(cd, fcDictionary)
    assert name == 'Test'


def test_createInteractionSuccessful():
    setHomespace('https://bu.edu/ben') # noqa
    Config.setOption('sbol_compliant_uris', True) # noqa
    Config.setOption('sbol_typed_uris', False) # noqa
    testCD, subCD1, subCD2, subCD3 = createTestCD()
    device_test_context, device_test, device = createModules()
    fc = device.functionalComponents.create('TestCD_sub1')
    fc.definition = subCD1.identity
    fc = device.functionalComponents.create('TestCD_sub2')
    fc.definition = subCD2.identity

    customNameDictionary = {'Device-Test-Context': device_test_context,
                            'Device-Test': device_test,
                            'Device': device}

    moduleName = 'Device'
    interactionName = 'TestInteraction'
    interactionType = 'Genetic Production'
    participantDictionary = {}
    selectedFC = ['TestCD_sub1']

    createInteraction(customNameDictionary,
                      moduleName,
                      interactionName,
                      interactionType,
                      participantDictionary,
                      selectedFC)

    assert len(device.interactions) == 1
    assert len(device.interactions[0].types) == 1
    assert len(device.interactions[0].participations) == 1
    assert device.interactions[0].displayId == interactionName
    assert device.interactions[0].types[0] == mapInteractions[interactionType]
    assert device.interactions[0].participations[0].displayId == selectedFC[0]


def test_createMapsTosSuccessful():
    class TestWidget:
        def __init__(self, value, description):
            self.value = value
            self.description = description

    doc = Document() # noqa
    setHomespace('https://bu.edu/ben') # noqa
    Config.setOption('sbol_compliant_uris', True) # noqa
    Config.setOption('sbol_typed_uris', False) # noqa

    testCD, subCD1, subCD2, subCD3 = createTestCD()
    device_test_context, device_test, device = createModules()
    fc1 = device.functionalComponents.create('TestCD_sub1')
    fc1.definition = subCD1.identity
    fc2 = device.functionalComponents.create('TestCD_sub2')
    fc2.definition = subCD2.identity

    plasmidPart = ComponentDefinition('TestCD__sub1') # noqa
    c = plasmidPart.components.create('TestCD_sub1')
    c.definition = subCD1.identity

    fc = device.functionalComponents.create('TestCD__sub1')
    fc.definition = plasmidPart.identity

    doc.addModuleDefinition(device)

    interactionName = 'TestInteraction'
    interactionType = 'Genetic Production'

    interaction = device.interactions.create(interactionName)
    interaction.types = mapInteractions[interactionType]

    participation = interaction.participations.create(fc1.displayId)
    participation.participant = fc1.identity

    participationWidgetsChildren = [TestWidget('<b>TestCD<b>', ''),
                                    TestWidget('Inhibitor', 'sub1')]
    participantDictionary = {fc1.displayId: participation}
    plasmidPartDictionary = {'TestCD_sub1': c}
    addedPlasmidParts = {'TestCD_sub1': fc}

    createMapsTos(doc,
                  participationWidgetsChildren,
                  participantDictionary,
                  plasmidPartDictionary,
                  addedPlasmidParts)

    assert len(device.functionalComponents) == 3
    assert len(device.functionalComponents[2].mapsTos) == 1
    assert device.functionalComponents[2].mapsTos[0].local == fc1.identity
    assert device.functionalComponents[2].mapsTos[0].remote == c.identity


if __name__ == '__main__':
    test_findCorrectPlasmid()
    test_createInteractionSuccessful()
    test_createMapsTosSuccessful()
