class Document:
    data = None
    template = None

    def __init__(self, data):
        self.data = data


class InstallationContractReport(Document):
    template = "installation_contract.html"


class AdvertisingContractReport(Document):
    template = "advertising_contract.html"
