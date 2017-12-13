from django.db import models


class BaseTimeField(models.Model):
    create_date = models.DateTimeField(verbose_name="创建时间", blank=True, auto_now_add=True)  # 创建时间
    update_date = models.DateTimeField(verbose_name="更新时间", blank=True, auto_now=True)  # 更新时间

    class Meta:
        abstract = True

class IDC(models.Model):
    """机房信息"""
    name = models.CharField(verbose_name=u'机房名称', max_length=64, unique=True)
    address = models.CharField(verbose_name=u'机房地址',max_length=100, blank=True)
    start_date = models.DateField(verbose_name=u'租赁日期',null=True,blank=True,)
    end_date = models.DateField(verbose_name=u'到期日期',null=True,blank=True)
    memo = models.CharField(verbose_name=u'备注', max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'IDC机房'
        verbose_name_plural = "IDC机房"


class Cabinet(BaseTimeField):
    """
    资产信息表
    """
    idc = models.ForeignKey(verbose_name='IDC机房', to='IDC')
    device_type_choices = ((1, '服务器'), (2, '交换机'), (3, '防火墙'),)
    device_type_id = models.IntegerField(verbose_name="设备类型",choices=device_type_choices, default=1)
    cabinet_num = models.CharField('机柜位置', max_length=30, null=True, blank=True)
    memo = models.TextField(verbose_name=u'备注', max_length=128, blank=True, null=True)

    class Meta:
        verbose_name_plural = "机柜信息"

    def __str__(self):
        return "%s-%s" % (self.idc.name, self.cabinet_num)



class Server(BaseTimeField):
    """服务器设备"""
    cabinet = models.OneToOneField(verbose_name=u'机柜位置',to='Cabinet', null=True, blank=True)
    name = models.CharField(verbose_name=u'主机名',max_length=30, unique=True)
    inner_ip = models.GenericIPAddressField(verbose_name=u'内网IP', blank=True, null=True)
    management_ip = models.GenericIPAddressField(verbose_name=u'管理IP', blank=True, null=True)
    business_unit = models.ForeignKey('BusinessUnit', verbose_name='业务线', null=True, blank=True)
    device_status_choices = ((0, '在线'), (1, '已下线'), (2, '未知'), (3, '故障'), (4, '备用'),)
    device_status = models.IntegerField(verbose_name="状态",choices=device_status_choices, default=1)
    server_type_choices = ((0, '物理服务器'), (1, '宿主机'),(2, '虚拟机'),)
    server_type = models.SmallIntegerField(verbose_name="服务器类型", choices=server_type_choices, default=0)
    upper_layer = models.ForeignKey(verbose_name='所属宿主机',to='self', related_name='upperlayer', blank=True, null=True)  # v1/v2/v3
    switch = models.ForeignKey(verbose_name='所属交换机',to='NetworkDevice',blank=True, null=True)
    os_type = models.CharField(verbose_name=u'系统平台', max_length=64, blank=True, null=True) # Linux、Wondows
    os_release = models.CharField(verbose_name=u'系统版本', max_length=64, blank=True, null=True) # Centos6.5、RedHat5

    sn = models.CharField(verbose_name=u'资产SN号', max_length=128, unique=True)
    server_attr = models.CharField(verbose_name=u'设备型号', max_length=128, null=True, blank=True)
    device_type = models.ForeignKey(to='Manufactory', verbose_name=u'设备厂商', null=True, blank=True)
    tags = models.ManyToManyField(to='Tag', blank=True, default=1)  # 可以自定义一些标记

    trade_date = models.DateField(verbose_name=u'购买时间', null=True, blank=True)
    expire_date = models.DateField(verbose_name=u'过保修期', null=True, blank=True)

    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = "服务器"

    def __str__(self):
        return self.name


class NetworkDevice(BaseTimeField):
    """网络设备"""

    cabinet = models.OneToOneField(verbose_name=u'机柜信息', to='Cabinet', null=True, blank=True)
    name = models.CharField(verbose_name="设备名称",max_length=64, unique=True)
    vlan_ip = models.GenericIPAddressField(verbose_name=u'VlanIP', blank=True, null=True)
    intranet_ip = models.GenericIPAddressField(verbose_name=u'管理IP', blank=True, null=True)
    manufactory = models.CharField(verbose_name=u'厂商',max_length=128,null=True, blank=True)
    model = models.CharField(verbose_name=u'型号', max_length=128, null=True, blank=True)
    firmware = models.CharField(verbose_name=u'固件信息', max_length=128,  blank=True, null=True)
    port_num = models.SmallIntegerField(verbose_name=u'端口个数', null=True, blank=True)
    device_detail = models.TextField(verbose_name=u'配置', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '网络设备'
        verbose_name_plural = "网络设备"


class Mem(BaseTimeField):
    """内存组件"""
    server = models.ForeignKey(verbose_name=u'所属服务器', to='Server')
    slot = models.CharField(verbose_name=u'插槽', max_length=64)
    capacity = models.IntegerField(verbose_name=u'内存大小(MB)')
    model = models.CharField(verbose_name=u'内存型号', max_length=128)
    speed = models.CharField(verbose_name=u'速率', max_length=16, null=True, blank=True)
    sn = models.CharField(verbose_name=u'SN号', max_length=128, blank=True, null=True)
    memo = models.CharField(verbose_name=u'备注', max_length=128, blank=True, null=True)

    def __str__(self):
        return '%s:%s:%s' % (self.server.name, self.slot, self.capacity)

    class Meta:
        verbose_name = '内存'
        verbose_name_plural = "内存"


class Cpu(BaseTimeField):
    """CPU组件"""

    server = models.ForeignKey(verbose_name='所属服务器', to='Server')
    count = models.IntegerField(verbose_name='CPU核心')
    model = models.CharField(verbose_name=u'CPU型号', max_length=128, null=True, blank=True)
    speed = models.CharField(verbose_name=u'CPU主频（MHz）', max_length=128, null=True, blank=True)
    memo = models.TextField(verbose_name=u'备注', null=True, blank=True)

    class Meta:
        verbose_name = 'CPU'
        verbose_name_plural = "CPU"

    def __str__(self):
        return '%s:%s'%(self.server.name,self.model)


class Disk(BaseTimeField):
    """硬盘组件"""

    server = models.ForeignKey(to='Server', verbose_name='所属服务器')
    sn = models.CharField(u'SN号', max_length=128, blank=True, null=True)
    slot = models.CharField(u'插槽位', max_length=64)
    model = models.CharField(u'磁盘型号', max_length=128, blank=True, null=True)
    capacity = models.FloatField(u'磁盘容量GB')
    disk_iface_choice = (
        ('SATA', 'SATA'),
        ('SAS', 'SAS'),
        ('SCSI', 'SCSI'),
        ('SSD', 'SSD'),
    )
    iface_type = models.CharField(u'接口类型', max_length=64, choices=disk_iface_choice, default='SAS')
    memo = models.TextField(u'备注', blank=True, null=True)

    # auto_create_fields = ['sn', 'slot', 'manufactory', 'model', 'capacity', 'iface_type']

    class Meta:
        verbose_name = '硬盘'
        verbose_name_plural = "硬盘"

    def __str__(self):
        return '%s-%s-%s' % (self.server.name, self.slot, self.capacity)



class Nic(BaseTimeField):
    """网卡组件"""

    server = models.ForeignKey(to='Server', verbose_name='所属服务器')
    name = models.CharField(u'网卡名', max_length=64, blank=True, null=True)
    ip = models.GenericIPAddressField(u'IP', blank=True, null=True)
    mac = models.CharField(u'MAC', max_length=64, unique=True)
    netmask = models.CharField(max_length=64, blank=True, null=True)
    status = models.BooleanField(default=False)
    model = models.CharField(u'网卡型号', max_length=128, blank=True, null=True)
    sn = models.CharField(u'SN号', max_length=128, blank=True, null=True)
    memo = models.CharField(u'备注', max_length=128, blank=True, null=True)

    def __str__(self):
        return '%s:%s' % (self.server_name, self.name)

    class Meta:
        verbose_name = u'网卡'
        verbose_name_plural = u"网卡"

    # auto_create_fields = ['name', 'sn', 'model', 'macaddress', 'ipaddress', 'netmask', 'bonding']



class Manufactory(models.Model):
    """厂商"""

    manufactory = models.CharField(u'厂商名称', max_length=64, unique=True)
    support_num = models.CharField(u'支持电话', max_length=30, blank=True)
    memo = models.CharField(u'备注', max_length=128, blank=True)

    def __str__(self):
        return self.manufactory

    class Meta:
        verbose_name = '厂商'
        verbose_name_plural = "厂商"


class BusinessUnit(models.Model):
    """业务线"""

    name = models.CharField(u'业务线', max_length=64, unique=True)
    # 上级业务线，可以创建层级关系
    parent_unit = models.ForeignKey(verbose_name='上层模块',to='self', related_name='parent_level', blank=True, null=True)
    # 业务负责人，之后关联用户表
    principal = models.CharField(u"负责人", max_length=64, blank=True, null=True)
    memo = models.CharField(u'备注', max_length=64, blank=True)

    def save(self, *args, **kwargs):
        if self.parent_unit:
            self.name = '-'.join([str(self.parent_unit),str(self.name)])
        return super(BusinessUnit, self).save(*args, **kwargs)


    def __str__(self):
            return self.name

    class Meta:
        ordering = ['name']
        verbose_name = '业务线'
        verbose_name_plural = "业务线"

class Tag(models.Model):
    """资产标签"""
    name = models.CharField('Tag name', max_length=32, unique=True)
    # creator = models.ForeignKey('UserProfile')
    create_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class EventLog(models.Model):
    """事件,记录平台变更信息"""

    name = models.CharField(u'事件名称', max_length=100)
    event_type_choices = (
        (1, u'硬件变更'),
        (2, u'新增配件'),
        (3, u'设备下线'),
        (4, u'设备上线'),
        (5, u'定期维护'),
        (6, u'业务上线\更新\变更'),
        (7, u'其它'),
    )
    event_type = models.SmallIntegerField(u'事件类型', choices=event_type_choices)
    component = models.CharField('事件子项', max_length=255, blank=True, null=True)
    detail = models.TextField(u'事件详情')
    date = models.DateTimeField(u'事件时间', auto_now_add=True)
    # user = models.ForeignKey('UserProfile', verbose_name=u'事件源')
    memo = models.TextField(u'备注', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '审计日志'
        verbose_name_plural = "审计日志"

    def colored_event_type(self):
        if self.event_type == 1:
            cell_html = '<span style="background: orange;">%s</span>'
        elif self.event_type == 2:
            cell_html = '<span style="background: yellowgreen;">%s</span>'
        else:
            cell_html = '<span >%s</span>'
        return cell_html % self.get_event_type_display()

    colored_event_type.allow_tags = True
    colored_event_type.short_description = u'事件类型'


class NewAssetApprovalZone(models.Model):
    """新资产待审批区，审批后存入正式数据库"""

    sn = models.CharField(u'资产SN号', max_length=128, unique=True)
    asset_type_choices = (
        ('server', u'服务器'),
        ('switch', u'交换机'),
        ('router', u'路由器'),
        ('firewall', u'防火墙'),
        ('storage', u'存储设备'),
        ('others', u'其它类'),
    )
    asset_type = models.CharField(choices=asset_type_choices, max_length=64, blank=True, null=True)
    manufactory = models.CharField(max_length=64, blank=True, null=True)
    model = models.CharField(max_length=128, blank=True, null=True)
    mem_size = models.IntegerField(blank=True, null=True)
    cpu_model = models.CharField(max_length=128, blank=True, null=True)
    cpu_count = models.IntegerField(blank=True, null=True)
    cpu_core_count = models.IntegerField(blank=True, null=True)
    os_type = models.CharField(max_length=64, blank=True, null=True)
    os_release = models.CharField(max_length=64, blank=True, null=True)
    data = models.TextField(u'资产数据')
    date = models.DateTimeField(u'汇报日期', auto_now_add=True)
    approved = models.BooleanField(u'已批准', default=False)
    # approved_by = models.ForeignKey('UserProfile', verbose_name=u'批准人', blank=True, null=True)
    approved_date = models.DateTimeField(u'批准日期', blank=True, null=True)

    def __str__(self):
        return self.sn

    class Meta:
        verbose_name = '新上线待批准资产'
        verbose_name_plural = "新上线待批准资产"


