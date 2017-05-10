
from django.db import models

def get_no():
    a='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return timezone.now().strftime('%Y%m%d%H%M%S')+''.join(random.choice(a) for i in range(8))

class WXOrderModel(models.Model):

    no = models.CharField('内部微信订单号',max_length=300,blank=True)
    transaction_id=models.CharField('微信支付订单号',max_length=300,blank=True)
    time_end=models.CharField('支付完成时间',max_length=300,blank=True)
    total_fee=models.CharField('总金额',max_length=300,blank=True)
    openid=models.CharField('付款人openid',max_length=300,blank=True)
    trade_type=models.CharField('交易类型',max_length=300,blank=True)
    result_code=models.CharField('业务结果',max_length=300,blank=True)
    detail=models.TextField(verbose_name='详细',blank=True)
    create_time=models.DateTimeField(verbose_name='记录创建时间',auto_now_add=True,null=True)
    last_update_time=models.DateTimeField(verbose_name='记录最后修改时间',auto_now=True,null=True)
    pay=models.CharField('支付情况',max_length=100,blank=True)
    confirmed=models.BooleanField('是否确认',default=False)
    
    #org_fee=models.CharField('原价',max_length=100,blank=True)
    #car=models.ForeignKey(UserCarModel,verbose_name='汽车',blank=True,null=True)
    #order=models.OneToOneField(OrderModel,verbose_name='订单',blank=True,null=True)
    #meal=models.ForeignKey(MealModel,verbose_name='套餐',blank=True,null=True)
    #coupon=models.ForeignKey('CouponModel',verbose_name='优惠券',blank=True,null=True)    

    
    def __init__(self,*args,**kw):
        super(WXOrderModel,self).__init__(*args,**kw)
        if not self.no:
            self.no= 'WX'+get_no()
    
    class Meta:
        abstract=True