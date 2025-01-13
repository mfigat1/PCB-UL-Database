import pandas as pd
import ULScrapperConstantsVariables

pd.set_option('display.max_columns', None)  # show all columns in pycharm output


def main():
    ULbase = pd.read_html(ULScrapperConstantsVariables.site)[0]
    ULbase.rename(columns=ULScrapperConstantsVariables.columnsNameConversion, inplace=True)
    ULbase = ULbase[ULScrapperConstantsVariables.columnsNames].drop(labels=[0])
    ULbase[ULScrapperConstantsVariables.columnsNames[1]] = (
        ULbase[ULScrapperConstantsVariables.columnsNames[1]].str.replace('E', '', regex=False))
    ULbase.to_excel(ULScrapperConstantsVariables.exportFilePattern, index=False)
    print(f"Ul base scrapped and saved as {ULScrapperConstantsVariables.exportFilePattern}")


if __name__ == "__main__":
    main()
