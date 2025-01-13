import ImportScreeningConstantsVariables
import ULScrapperConstantsVariables
import ConcatConstantsVariables


exportFiles = [ImportScreeningConstantsVariables.exportFilePattern,
               ULScrapperConstantsVariables.exportFilePattern,
               ConcatConstantsVariables.exportFilePattern,
               ConcatConstantsVariables.ULRejectedToCheckExportFilePattern
               ]

columnsWidth = {
    "narrow": 20,
    "wide": 40
}

rowHeight = 30
horizontalAlignment = "left"
verticalAlignment = "top"
wrapText = True

mode_mapping = {
    "normal": [
        (ImportScreeningConstantsVariables.exportFilePattern, 'narrow'),
        (ULScrapperConstantsVariables.exportFilePattern, 'wide'),
        (ConcatConstantsVariables.exportFilePattern, 'narrow'),
        (ConcatConstantsVariables.ULRejectedToCheckExportFilePattern, 'narrow')
    ],
    "export narrow": [(exportFiles, 'narrow')],
    "export wide": [(exportFiles, 'wide')],
    "all narrow": [("all", 'narrow')],
    "all wide": [("all", 'wide')],
}