"""
Tests for onchain-related Pydantic models.
"""
import pytest
from pydantic import ValidationError

from taptools_api_mcp.models.onchain import (
    AssetSupplyRequest, AssetSupplyResponse,
    AddressInfoRequest, AddressInfo, AddressInfoResponse,
    AddressUTXOsRequest, UTXO, AddressUTXOsResponse,
    TransactionUTXOsRequest, TransactionUTXOsResponse
)

class TestAssetSupplyModels:
    def test_asset_supply_request_valid(self):
        """Test AssetSupplyRequest with valid data."""
        request = AssetSupplyRequest(unit="test_token")
        assert request.unit == "test_token"

    def test_asset_supply_request_missing_unit(self):
        """Test AssetSupplyRequest fails without required unit."""
        with pytest.raises(ValidationError) as exc:
            AssetSupplyRequest()
        assert "field required" in str(exc.value)
        assert "unit" in str(exc.value)

    def test_asset_supply_response_valid(self):
        """Test AssetSupplyResponse with valid data."""
        response = AssetSupplyResponse(supply=1000000)
        assert response.supply == 1000000

    def test_asset_supply_response_invalid_type(self):
        """Test AssetSupplyResponse with invalid supply type."""
        with pytest.raises(ValidationError) as exc:
            AssetSupplyResponse(supply="invalid")
        assert "value is not a valid integer" in str(exc.value)

class TestAddressInfoModels:
    def test_address_info_request_empty(self):
        """Test AddressInfoRequest with no values (all optional)."""
        request = AddressInfoRequest()
        assert request.address is None
        assert request.payment_cred is None

    def test_address_info_request_with_address(self):
        """Test AddressInfoRequest with address."""
        request = AddressInfoRequest(address="addr1test123")
        assert request.address == "addr1test123"
        assert request.payment_cred is None

    def test_address_info_request_with_payment_cred(self):
        """Test AddressInfoRequest with payment credential."""
        request = AddressInfoRequest(payment_cred="cred123")
        assert request.address is None
        assert request.payment_cred == "cred123"

    def test_address_info_valid(self):
        """Test AddressInfo with valid data."""
        info = AddressInfo(
            address="addr1test123",
            assets=[{"unit": "token1", "quantity": 100}],
            lovelace="1000000",
            payment_cred="cred123",
            stake_address="stake1test123"
        )
        assert info.address == "addr1test123"
        assert len(info.assets) == 1
        assert info.assets[0]["unit"] == "token1"
        assert info.lovelace == "1000000"
        assert info.payment_cred == "cred123"
        assert info.stake_address == "stake1test123"

    def test_address_info_missing_required(self):
        """Test AddressInfo fails without required fields."""
        with pytest.raises(ValidationError) as exc:
            AddressInfo()
        assert "field required" in str(exc.value)

class TestAddressUTXOsModels:
    def test_address_utxos_request_defaults(self):
        """Test AddressUTXOsRequest with default values."""
        request = AddressUTXOsRequest()
        assert request.address is None
        assert request.payment_cred is None
        assert request.page == 1
        assert request.per_page == 100

    def test_address_utxos_request_custom(self):
        """Test AddressUTXOsRequest with custom values."""
        request = AddressUTXOsRequest(
            address="addr1test123",
            payment_cred="cred123",
            page=2,
            per_page=50
        )
        assert request.address == "addr1test123"
        assert request.payment_cred == "cred123"
        assert request.page == 2
        assert request.per_page == 50

    def test_utxo_valid(self):
        """Test UTXO with valid data."""
        utxo = UTXO(
            assets=[{"unit": "token1", "quantity": 100}],
            hash="tx123",
            index=0,
            lovelace="1000000"
        )
        assert len(utxo.assets) == 1
        assert utxo.assets[0]["unit"] == "token1"
        assert utxo.hash == "tx123"
        assert utxo.index == 0
        assert utxo.lovelace == "1000000"

    def test_utxo_invalid_types(self):
        """Test UTXO with invalid data types."""
        with pytest.raises(ValidationError) as exc:
            UTXO(
                assets="invalid",  # Should be list
                hash=123,  # Should be string
                index="invalid",  # Should be integer
                lovelace=1000000  # Should be string
            )
        assert "value is not a valid list" in str(exc.value)
        assert "value is not a valid integer" in str(exc.value)

class TestTransactionUTXOsModels:
    def test_transaction_utxos_request_valid(self):
        """Test TransactionUTXOsRequest with valid data."""
        request = TransactionUTXOsRequest(hash="tx123")
        assert request.hash == "tx123"

    def test_transaction_utxos_request_missing_hash(self):
        """Test TransactionUTXOsRequest fails without required hash."""
        with pytest.raises(ValidationError) as exc:
            TransactionUTXOsRequest()
        assert "field required" in str(exc.value)
        assert "hash" in str(exc.value)

    def test_transaction_utxos_response_valid(self):
        """Test TransactionUTXOsResponse with valid data."""
        response = TransactionUTXOsResponse(
            inputs={
                "addr1": [{"txHash": "tx1", "amount": 100}],
                "addr2": [{"txHash": "tx2", "amount": 200}]
            },
            outputs={
                "addr3": [{"txHash": "tx3", "amount": 150}],
                "addr4": [{"txHash": "tx4", "amount": 150}]
            }
        )
        assert len(response.inputs) == 2
        assert len(response.outputs) == 2
        assert response.inputs["addr1"][0]["amount"] == 100
        assert response.outputs["addr3"][0]["amount"] == 150

    def test_transaction_utxos_response_empty_dicts(self):
        """Test TransactionUTXOsResponse with empty dictionaries."""
        response = TransactionUTXOsResponse(inputs={}, outputs={})
        assert len(response.inputs) == 0
        assert len(response.outputs) == 0

    def test_transaction_utxos_response_invalid_types(self):
        """Test TransactionUTXOsResponse with invalid data types."""
        with pytest.raises(ValidationError) as exc:
            TransactionUTXOsResponse(
                inputs="invalid",  # Should be dict
                outputs="invalid"  # Should be dict
            )
        assert "value is not a valid dict" in str(exc.value)
