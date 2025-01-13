import pandas as pd
import glob
import ImportScreeningConstantsVariables
import re

pd.set_option('display.max_columns', None)  # show all columns in pycharm output


def quality_control_order_file_finder(workingMode):
    if workingMode == 'work':
        files = glob.glob(ImportScreeningConstantsVariables.importFilePattern['work'])
    else:
        files = glob.glob(ImportScreeningConstantsVariables.importFilePattern['test'])
    if files:
        print("DYN file has been found")
        return files[0]
    else:
        print("Please add DYN file first and restart script")


def quality_control_order_file_importer(qualityControlOrderFilePath):
    df = pd.read_excel(qualityControlOrderFilePath, usecols=ImportScreeningConstantsVariables.importedColumns)
    df = df[
        df[ImportScreeningConstantsVariables.importedColumn].isin(
            ImportScreeningConstantsVariables.importedValuesForImportedColumn)]

    df.drop(axis=1, columns=['Grupa testowa'], inplace=True)
    df.columns = ImportScreeningConstantsVariables.importedColumnsNewNames

    df["Data rejestracji"] = (
        df["Data rejestracji"]
        .astype(str).str[:10]
        .str.strip()
    )

    df.sort_values(by='Data rejestracji', inplace=True)

    print(f"Data file imported. Unnecessary columns rejected. File sorted by date.")
    return df


def quality_control_order_file_status_setup(df):
    def concatStatus(row):
        if (row['Stan'] == 'Sukces') and (row['Akceptacja błędu'] == 'Nie'):
            return 'OK'
        else:
            return 'NG'

    df['Status'] = df.apply(concatStatus, axis=1)

    df = df.drop(['Stan', 'Akceptacja błędu'], axis=1)

    print(f"Status of deliveries set up")
    return df


def quality_control_order_file_DCUL_spliter(df):
    df["Uwagi"] = (
        df["Uwagi"]
        .str.replace(r'[^0-9 ]', '', regex=True)
        .str.strip()
    )

    splitDCUL = df['Uwagi'].str.split(' ', expand=True, n=5)
    splitDCUL.columns = [f'DCUL{i + 1}' for i in range(splitDCUL.shape[1])]
    df = pd.concat([df, splitDCUL], axis=1)

    df = df.drop(['Uwagi'], axis=1)

    return df


def quality_control_order_file_DCUL_manager(df):
    def categorize_DC_UL(row):
        DC = []
        UL = []

        for col in ['DCUL1', 'DCUL2', 'DCUL3', 'DCUL4', 'DCUL5', 'DCUL6']:
            value = row[col]
            if pd.notnull(value):
                if re.fullmatch(r'\d{4}', str(value)):
                    DC.append(str(value))
                elif re.fullmatch(r'\d{5,6}', str(value)):
                    UL.append(str(value))

        return " ".join(DC), " ".join(UL)

    df[['DC', 'UL']] = df.apply(categorize_DC_UL, axis=1, result_type="expand")

    df = df.drop(['DCUL1', 'DCUL2', 'DCUL3', 'DCUL4', 'DCUL5', 'DCUL6'], axis=1)
    return df


def quality_control_order_file_saver(df):
    df.to_excel(ImportScreeningConstantsVariables.exportFilePattern, index=False)
    print(f"Data file saved as {ImportScreeningConstantsVariables.exportFilePattern}")


def main(workingMode="work"):
    print(f"WARNING: Working mode: {workingMode}!")
    qualityControlOrderFilePath = quality_control_order_file_finder(workingMode)
    qualityControlOrderFile = quality_control_order_file_importer(qualityControlOrderFilePath)
    qualityControlOrderFile = quality_control_order_file_status_setup(qualityControlOrderFile)
    qualityControlOrderFile = quality_control_order_file_DCUL_spliter(qualityControlOrderFile)
    qualityControlOrderFile = quality_control_order_file_DCUL_manager(qualityControlOrderFile)
    quality_control_order_file_saver(qualityControlOrderFile)


if __name__ == "__main__":
    main()
