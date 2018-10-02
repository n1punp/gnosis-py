from django_eth.serializers import EthereumAddressField, HexadecimalField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .safe_service import SafeOperation


class SafeMultisigEstimateTxSerializer(serializers.Serializer):
    safe = EthereumAddressField()
    to = EthereumAddressField(default=None, allow_null=True)
    value = serializers.IntegerField(min_value=0)
    data = HexadecimalField(default=None, allow_null=True, allow_blank=True)
    operation = serializers.IntegerField(min_value=0)

    def validate_operation(self, value):
        try:
            SafeOperation(value)
            return value
        except ValueError:
            raise ValidationError('Unknown operation')

    def validate(self, data):
        super().validate(data)

        if not data['to'] and not data['data']:
            raise ValidationError('`data` and `to` cannot both be null')

        if not data['to'] and not data['data']:
            raise ValidationError('`data` and `to` cannot both be null')

        if data['operation'] == SafeOperation.CREATE.value:
            if data['to']:
                raise ValidationError('Operation is Create, but `to` was provided')
            elif not data['data']:
                raise ValidationError('Operation is Create, but not `data` was provided')
        elif not data['to']:
            raise ValidationError('Operation is not Create, but `to` was not provided')

        return data


class SafeMultisigTxSerializer(SafeMultisigEstimateTxSerializer):
    safe_tx_gas = serializers.IntegerField(min_value=0)
    data_gas = serializers.IntegerField(min_value=0)
    gas_price = serializers.IntegerField(min_value=0)
    gas_token = EthereumAddressField(default=None, allow_null=True)
    refund_receiver = EthereumAddressField(default=None, allow_null=True)
    nonce = serializers.IntegerField(min_value=0)

    def validate(self, data):
        super().validate(data)

        if data.get('gas_token'):
            raise ValidationError('Gas Token is still not supported')

        return data
