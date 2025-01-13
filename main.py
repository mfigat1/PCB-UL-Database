import ULscrapper
import ImportScreening
import ExcelVisualConverter
import Concat

print("---------------------------------------------------------------------------")
print("Import")
print(":")
ImportScreening.main(workingMode='work')  # workingMode= 'work' / 'test'
print("---------------------------------------------------------------------------")
print("Ul base scrap")
print(":")
ULscrapper.main()
print("---------------------------------------------------------------------------")
print("Final Concat")
print(":")
Concat.main()
print("---------------------------------------------------------------------------")
print("---------------------------------------------------------------------------")
print("Excel converter")
print(":")
ExcelVisualConverter.main(workingMode="normal")  # workingMode -> ExcelVisualConverterConstantsVariables
print("---------------------------------------------------------------------------")
