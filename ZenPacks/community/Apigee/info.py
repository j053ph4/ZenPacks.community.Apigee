from ZenPacks.community.ConstructionKit.ClassHelper import *

def APIMethodgetEventClassesVocabulary(context):
    return SimpleVocabulary.fromValues(context.listgetEventClasses())

class APIMethodInfo(ClassHelper.APIMethodInfo):
    ''''''


