
from django.db import models

def get_no():
    a='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return timezone.now().strftime('%Y%m%d%H%M%S')+''.join(random.choice(a) for i in range(8))

class WXOrderModel(models.Model):

    no = models.CharField('�ڲ�΢�Ŷ�����',max_length=300,blank=True)
    transaction_id=models.CharField('΢��֧��������',max_length=300,blank=True)
    time_end=models.CharField('֧�����ʱ��',max_length=300,blank=True)
    total_fee=models.CharField('�ܽ��',max_length=300,blank=True)
    openid=models.CharField('������openid',max_length=300,blank=True)
    trade_type=models.CharField('��������',max_length=300,blank=True)
    result_code=models.CharField('ҵ����',max_length=300,blank=True)
    detail=models.TextField(verbose_name='��ϸ',blank=True)
    create_time=models.DateTimeField(verbose_name='��¼����ʱ��',auto_now_add=True,null=True)
    last_update_time=models.DateTimeField(verbose_name='��¼����޸�ʱ��',auto_now=True,null=True)
    pay=models.CharField('֧�����',max_length=100,blank=True)
    confirmed=models.BooleanField('�Ƿ�ȷ��',default=False)
    
    #org_fee=models.CharField('ԭ��',max_length=100,blank=True)
    #car=models.ForeignKey(UserCarModel,verbose_name='����',blank=True,null=True)
    #order=models.OneToOneField(OrderModel,verbose_name='����',blank=True,null=True)
    #meal=models.ForeignKey(MealModel,verbose_name='�ײ�',blank=True,null=True)
    #coupon=models.ForeignKey('CouponModel',verbose_name='�Ż�ȯ',blank=True,null=True)    

    
    def __init__(self,*args,**kw):
        super(WXOrderModel,self).__init__(*args,**kw)
        if not self.no:
            self.no= 'WX'+get_no()
    
    class Meta:
        abstract=True