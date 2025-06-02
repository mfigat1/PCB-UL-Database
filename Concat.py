import pandas as pd
import numpy as np
import ImportScreeningConstantsVariables
import ULScrapperConstantsVariables
import ConcatConstantsVariables
import datetime
from datetime import timedelta

pd.set_option('display.max_columns', None)  # show all columns in pycharm output


def UL_base_file_loader():
    ULbase = pd.read_excel(ULScrapperConstantsVariables.exportFilePattern)
    ULbase["UL number"] = ULbase["UL number"].replace(["", "nan", "null"], np.nan)
    ULbase["UL number"] = pd.to_numeric(ULbase["UL number"], errors='coerce').astype("Int64")
    return ULbase


def quality_control_order_file_loader_and_merger(ULbase):
    qualityControlOrderFile = pd.read_excel(ImportScreeningConstantsVariables.exportFilePattern)
    qualityControlOrderFileByLastDelivery = (qualityControlOrderFile
                                             .groupby("Indeks")["Data rejestracji"]
                                             .max()
                                             .reset_index()
                                             .rename(columns={"Data rejestracji": "Last delivery"}))

    qualityControlOrderFileByDC = (qualityControlOrderFile
                                   .groupby("Indeks")
                                   .agg(
        ok_count=("Status", lambda x: (x == "OK").sum()),
        ng_count=("Status", lambda x: (x == "NG").sum()))
                                   .reset_index()
                                   .rename(columns={"ok_count": "OK count",
                                                    "ng_count": "NG count"})
                                   )

    qualityControlOrderFileByUL = (
        qualityControlOrderFile
        .groupby("Indeks")["UL"]
        .agg(lambda x: x.mode().iloc[0] if not x.mode().empty else "")
        .reset_index()
    )

    qualityControlOrderFile = qualityControlOrderFileByLastDelivery.merge(
        qualityControlOrderFileByDC,
        on="Indeks",
        how="inner")

    qualityControlOrderFile = qualityControlOrderFile.merge(
        qualityControlOrderFileByUL,
        on="Indeks",
        how="inner")

    qualityControlOrderFile["UL"] = qualityControlOrderFile["UL"].replace(["", "nan", "null"], np.nan)
    qualityControlOrderFile["UL"] = pd.to_numeric(qualityControlOrderFile["UL"], errors='coerce').astype("Int64")

    ULverificationConditions = [
        qualityControlOrderFile["UL"].isna(),
        (qualityControlOrderFile["UL"] == 198407).fillna(False),
        (qualityControlOrderFile["UL"].isin(ULbase["UL number"])).fillna(False),
        (~qualityControlOrderFile["UL"].isin(ULbase["UL number"])).fillna(False)
    ]

    qualityControlOrderFile["UL status"] = np.select(ULverificationConditions,
                                                     ConcatConstantsVariables.ULverificationChoices,
                                                     default="Unknown Status")

    qualityControlOrderFile = qualityControlOrderFile.sort_values(
        by=ConcatConstantsVariables.qualityControlOrderFileSortedBy, ascending=False)

    qualityControlOrderFile.to_excel(ConcatConstantsVariables.exportFilePattern, index=False)
    return qualityControlOrderFile


def UL_rejected_file_exporter(qualityControlOrderFile):
    time = (datetime.datetime.now() - timedelta(days=ConcatConstantsVariables.ULRejectedHowFarToCheck)).strftime(
        "%Y-%m-%d")
    problematicULStatus = qualityControlOrderFile["UL status"] == ConcatConstantsVariables.ULverificationChoices[3]
    onlyLastTime = qualityControlOrderFile["Last delivery"] >= time

    ULRejectedToCheck = pd.DataFrame(
        qualityControlOrderFile[problematicULStatus & onlyLastTime][['Indeks','UL', "Last delivery"]]).drop_duplicates(
        subset='UL').reset_index(drop=True)
    ULRejectedToCheck.to_excel(ConcatConstantsVariables.ULRejectedToCheckExportFilePattern, index=False)

    print(f"""
    Rejected UL numbers to check:
    
    {ULRejectedToCheck}
    
    Saved as {ConcatConstantsVariables.ULRejectedToCheckExportFilePattern}""")


def main():
    ULbase = UL_base_file_loader()
    qualityControlOrderFile = quality_control_order_file_loader_and_merger(ULbase)
    UL_rejected_file_exporter(qualityControlOrderFile)


if __name__ == "__main__":
    main()
