from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0004_deliveryzone_order_delivery_fee_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='user_order_no',
            field=models.PositiveIntegerField(default=0, help_text='Sequential number per user'),
        ),
    ]


