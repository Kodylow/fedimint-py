import requests
from models.common import InfoResponse, ListOperationsRequest, OperationOutput, BackupRequest
from models.ln import LnInvoiceRequest, LnInvoiceResponse, AwaitInvoiceRequest, LnPayRequest, LnPayResponse, AwaitLnPayRequest, Gateway, SwitchGatewayRequest
from models.wallet import DepositAddressRequest, AwaitDepositRequest, WithdrawRequest
from models.mint import ReissueRequest, SpendRequest, ValidateRequest, SplitRequest, CombineRequest

class FedimintClient:
    def __init__(self, base_url: str, password: str):
        self.base_url = f"{base_url}/fedimint/v2"
        self.password = password
        self.ln = self.LN(self)
        self.wallet = self.Wallet(self)
        self.mint = self.Mint(self)

    def _fetch_with_auth(self, endpoint: str, method: str, data=None):
        headers = {'Authorization': f'Bearer {self.password}'}
        if method == 'GET':
            response = requests.get(f"{self.base_url}{endpoint}", headers=headers)
        elif method == 'POST':
            headers['Content-Type'] = 'application/json'
            response = requests.post(f"{self.base_url}{endpoint}", json=data.model_dump(), headers=headers)
        else:
            raise ValueError("Unsupported HTTP method")

        if response.status_code != 200:
            raise Exception(f"HTTP error! status: {response.status_code}")

        return response.json()

    def info(self):
        return self._fetch_with_auth('/admin/info', 'GET')

    def backup(self, request: BackupRequest):
        return self._fetch_with_auth('/admin/backup', 'POST', data=request)

    def discover_version():
        return self._fetch_with_auth('/admin/discover_version', 'GET')

    # def restore(self, request: RestoreRequest):
    #     return self._fetch_with_auth('/admin/restore', 'POST', data=request)

    def list_operations(self, request: ListOperationsRequest):
        return self._fetch_with_auth('/admin/list_operations', 'POST', data=request)
    
    # def module(self, name: str):
    #     return self._fetch_with_auth(f'/admin/module', 'POST')

    def config(self):
        return self._fetch_with_auth('/admin/config', 'GET')

    class LN:
        def __init__(self, client):
            self.client = client

        def create_invoice(self, request: LnInvoiceRequest):
            return self.client._fetch_with_auth('/ln/invoice', 'POST', data=request)

        def await_invoice(self, request: AwaitInvoiceRequest):
            return self.client._fetch_with_auth('/ln/await-invoice', 'POST', data=request)

        def pay(self, request: LnPayRequest):
            return self.client._fetch_with_auth('/ln/pay', 'POST', data=request)

        def await_pay(self, request: AwaitLnPayRequest):
            return self.client._fetch_with_auth('/ln/await-pay', 'POST', data=request)

        def list_gateways(self):
            return self.client._fetch_with_auth('/ln/list-gateways', 'GET')

        def switch_gateway(self, request: SwitchGatewayRequest):
            return self.client._fetch_with_auth('/ln/switch-gateway', 'POST', data=request)

    class Wallet:
        def __init__(self, client):
            self.client = client

        def create_deposit_address(self, request: DepositAddressRequest):
            return self.client._fetch_with_auth('/wallet/deposit-address', 'POST', data=request)

        def await_deposit(self, request: AwaitDepositRequest):
            return self.client._fetch_with_auth('/wallet/await-deposit', 'POST', data=request)

        def withdraw(self, request: WithdrawRequest):
            return self.client._fetch_with_auth('/wallet/withdraw', 'POST', data=request)

    class Mint:
        def __init__(self, client):
            self.client = client

        def reissue(self, request: ReissueRequest):
            return self.client._fetch_with_auth('/mint/reissue', 'POST', data=request)

        def spend(self, request: SpendRequest):
            return self.client._fetch_with_auth('/mint/spend', 'POST', data=request)

        def validate(self, request: ValidateRequest):
            return self.client._fetch_with_auth('/mint/validate', 'POST', data=request)

        def split(self, request: SplitRequest):
            return self.client._fetch_with_auth('/mint/split', 'POST', data=request)

        def combine(self, request: CombineRequest):
            return self.client._fetch_with_auth('/mint/combine', 'POST', data=request)
