from django.db import models

class LegacyForeignKey(models.ForeignKey):
    """
    ForeignKey for legacy databases where foreign keys columns
    are non-nullable and using zero values as NULL.

    class Order(models.Model):
        carrier = LegacyForeignKey('Carrier', null=True)
        class Meta:
           managed = False
           db_table = "ps_order"

    order.carrier_id = 0
    order.carrier  # no Carrier.DoesNotExist exception
    """

    def get_local_related_value(self, instance):
        ret = super().get_local_related_value(instance)
        return [None if item == 0 else item for item in ret]