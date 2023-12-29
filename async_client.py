import aiohttp
from models.common import InfoResponse, ListOperationsRequest, OperationOutput, BackupRequest
from models.modules.ln import LnInvoiceRequest, LnInvoiceResponse, AwaitInvoiceRequest, LnPayRequest, LnPayResponse, AwaitLnPayRequest, Gateway, SwitchGatewayRequest
from models.modules.wallet import DepositAddressRequest, AwaitDepositRequest, WithdrawRequest
from models.modules.mint import ReissueRequest, SpendRequest, ValidateRequest, SplitRequest, CombineRequest

class FedimintClient:
    def __init__(self, base_url: str, password: str):
        self.base_url = f"{base_url}/fedimint/v2"
        self.password = password
        self.session = aiohttp.ClientSession()

    async def _fetch_with_auth(self, endpoint: str, method: str, data=None):
        headers = {'Authorization': f'Bearer {self.password}'}
        if method == 'GET':
            async with self.session.get(f"{self.base_url}{endpoint}", headers=headers) as response:
                if response.status != 200:
                    raise aiohttp.ClientResponseError(response.status, message=f"HTTP error! status: {response.status}")
                return await response.json()
        elif method == 'POST':
            headers['Content-Type'] = 'application/json'
            async with self.session.post(f"{self.base_url}{endpoint}", json=data.model_dump(), headers=headers) as response:
                if response.status != 200:
                    raise aiohttp.ClientResponseError(response.status, message=f"HTTP error! status: {response.status}")
                return await response.json()
        else:
            raise ValueError("Unsupported HTTP method")
        
    async def close(self):
        await self.session.close()

    async def info(self):
        return await self._fetch_with_auth('/admin/info', 'GET')

    async def backup(self, request: BackupRequest):
        return await self._fetch_with_auth('/admin/backup', 'POST', data=request)

    async def discover_version(self):
        return await self._fetch_with_auth('/admin/discover_version', 'GET')

    async def list_operations(self, request: ListOperationsRequest):
        return await self._fetch_with_auth('/admin/list_operations', 'POST', data=request)

    async def config(self):
        return await self._fetch_with_auth('/admin/config', 'GET')

    @property
    def modules(self):
        class Modules:
            def __init__(self, client):
                self.ln = self.LN(client)
                self.wallet = self.Wallet(client)
                self.mint = self.Mint(client)

            class LN:
                def __init__(self, client):
                    self.client = client

                async def create_invoice(self, request: LnInvoiceRequest):
                    return await self.client._fetch_with_auth('/ln/invoice', 'POST', data=request)

                async def await_invoice(self, request: AwaitInvoiceRequest):
                    return await self.client._fetch_with_auth('/ln/await-invoice', 'POST', data=request)

                async def pay(self, request: LnPayRequest):
                    return await self.client._fetch_with_auth('/ln/pay', 'POST', data=request)

                async def await_pay(self, request: AwaitLnPayRequest):
                    return await self.client._fetch_with_auth('/ln/await-pay', 'POST', data=request)

                async def list_gateways(self):
                    return await self.client._fetch_with_auth('/ln/list-gateways', 'GET')

                async def switch_gateway(self, request: SwitchGatewayRequest):
                    return await self.client._fetch_with_auth('/ln/switch-gateway', 'POST', data=request)

            class Wallet:
                def __init__(self, client):
                    self.client = client

                async def create_deposit_address(self, request: DepositAddressRequest):
                    return await self.client._fetch_with_auth('/wallet/deposit-address', 'POST', data=request)

                async def await_deposit(self, request: AwaitDepositRequest):
                    return await self.client._fetch_with_auth('/wallet/await-deposit', 'POST', data=request)

                async def withdraw(self, request: WithdrawRequest):
                    return await self.client._fetch_with_auth('/wallet/withdraw', 'POST', data=request)

            class Mint:
                def __init__(self, client):
                    self.client = client

                async def reissue(self, request: ReissueRequest):
                    return await self.client._fetch_with_auth('/mint/reissue', 'POST', data=request)

                async def spend(self, request: SpendRequest):
                    return await self.client._fetch_with_auth('/mint/spend', 'POST', data=request)

                async def validate(self, request: ValidateRequest):
                    return await self.client._fetch_with_auth('/mint/validate', 'POST', data=request)

                async def split(self, request: SplitRequest):
                    return await self.client._fetch_with_auth('/mint/split', 'POST', data=request)

                async def combine(self, request: CombineRequest):
                    return await self.client._fetch_with_auth('/mint/combine', 'POST', data=request)

        return Modules(self)
