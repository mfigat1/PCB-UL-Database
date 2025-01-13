importFilePattern = {
    'work': 'DYN*.xlsx',
    'test': 't*.xlsx'
}

exportFilePattern = "Quality Control Order File.xlsx"

importedColumns = [
    'Data i godzina utworzenia',
    'Kod pozycji',
    'Grupa testowa',
    'Uwagi Odnośnie Partii',
    'Stan',
    'Akceptacja błędu']

importedColumnsNewNames = [
    'Data rejestracji',
    'Indeks',
    # 'Grupa testowa' - deleted, not necessary
    'Uwagi',
    'Stan',
    'Akceptacja błędu']

importedColumn = 'Grupa testowa'
importedValuesForImportedColumn = ['RAP.DOST.', 'PCB', 'PCB_AS']


