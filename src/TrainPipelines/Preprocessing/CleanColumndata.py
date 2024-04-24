class Cleaner:
    def __init__(self) -> None:
        pass

    def cleanSyntaxPrefixes(self,df):
        '''Cleaning Account Names'''
        caseReportTable = df.copy()

        def clean_account_name(account_name):
            cleaned_name = re.sub(r'^(?:ZZZ:LOST\s?--?|ZZZ:LOST\s?-\s?|ZZZ: LOST--\s?|ZZZ: Lost - |ZZZ:Lost - |ZZZ:Lost -- |\d{4}-\d{2}-\d{2}-?\s?)', '', account_name)
            return cleaned_name.strip()

        caseReportTable['Account'] = caseReportTable['Account'].apply(clean_account_name)
        caseReportTable['Account'] = caseReportTable['Account'].apply(clean_account_name)
        return caseReportTable