# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-31 06:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('asset_type', models.CharField(choices=[('server', '服务器'), ('networkdevice', '网络设备'), ('storagedevice', '存储设备'), ('securitydevice', '安全设备')], default='server', max_length=64, verbose_name='资产类型')),
                ('status', models.SmallIntegerField(choices=[(0, '在线'), (1, '已下线'), (2, '未知'), (3, '故障'), (4, '备用')], default=0, verbose_name='资产状态')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('sn', models.CharField(max_length=128, unique=True, verbose_name='资产SN号')),
                ('trade_date', models.DateField(blank=True, null=True, verbose_name='购买时间')),
                ('expire_date', models.DateField(blank=True, null=True, verbose_name='过保修期')),
                ('server_attr', models.CharField(blank=True, max_length=128, null=True, verbose_name='设备型号')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '资产表',
                'verbose_name_plural': '资产表',
            },
        ),
        migrations.CreateModel(
            name='BusinessUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='业务线')),
                ('principal', models.CharField(blank=True, max_length=64, null=True, verbose_name='负责人')),
                ('memo', models.CharField(blank=True, max_length=64, verbose_name='备注')),
                ('parent_unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent_level', to='asset.BusinessUnit')),
            ],
            options={
                'verbose_name': '业务线',
                'verbose_name_plural': '业务线',
            },
        ),
        migrations.CreateModel(
            name='Cpu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('cpu_count', models.IntegerField(blank=True, null=True, verbose_name='CPU核心')),
                ('cpu_physical_count', models.IntegerField(blank=True, null=True, verbose_name='物理CPU个数')),
                ('cpu_model', models.CharField(blank=True, max_length=128, null=True, verbose_name='CPU型号')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('asset', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='asset.Asset')),
            ],
            options={
                'verbose_name': 'CPU部件',
                'verbose_name_plural': 'CPU部件',
            },
        ),
        migrations.CreateModel(
            name='Disk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('sn', models.CharField(blank=True, max_length=128, null=True, verbose_name='SN号')),
                ('slot', models.CharField(max_length=64, verbose_name='插槽位')),
                ('model', models.CharField(blank=True, max_length=128, null=True, verbose_name='磁盘型号')),
                ('capacity', models.FloatField(verbose_name='磁盘容量GB')),
                ('iface_type', models.CharField(choices=[('SATA', 'SATA'), ('SAS', 'SAS'), ('SCSI', 'SCSI'), ('SSD', 'SSD')], default='SAS', max_length=64, verbose_name='接口类型')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asset.Asset')),
            ],
            options={
                'verbose_name': '硬盘',
                'verbose_name_plural': '硬盘',
            },
        ),
        migrations.CreateModel(
            name='EventLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='事件名称')),
                ('event_type', models.SmallIntegerField(choices=[(1, '硬件变更'), (2, '新增配件'), (3, '设备下线'), (4, '设备上线'), (5, '定期维护'), (6, '业务上线\\更新\\变更'), (7, '其它')], verbose_name='事件类型')),
                ('component', models.CharField(blank=True, max_length=255, null=True, verbose_name='事件子项')),
                ('detail', models.TextField(verbose_name='事件详情')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='事件时间')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asset.Asset')),
            ],
            options={
                'verbose_name': '审计日志',
                'verbose_name_plural': '审计日志',
            },
        ),
        migrations.CreateModel(
            name='IDC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='机房名称')),
                ('memo', models.CharField(blank=True, max_length=128, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '机房',
                'verbose_name_plural': '机房',
            },
        ),
        migrations.CreateModel(
            name='Manufactory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manufactory', models.CharField(max_length=64, unique=True, verbose_name='厂商名称')),
                ('support_num', models.CharField(blank=True, max_length=30, verbose_name='支持电话')),
                ('memo', models.CharField(blank=True, max_length=128, verbose_name='备注')),
            ],
            options={
                'verbose_name': '厂商',
                'verbose_name_plural': '厂商',
            },
        ),
        migrations.CreateModel(
            name='Mem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('slot', models.CharField(max_length=64, verbose_name='插槽')),
                ('capacity', models.IntegerField(verbose_name='内存大小(MB)')),
                ('model', models.CharField(max_length=128, verbose_name='内存型号')),
                ('speed', models.CharField(blank=True, max_length=16, null=True, verbose_name='速率')),
                ('sn', models.CharField(blank=True, max_length=128, null=True, verbose_name='SN号')),
                ('memo', models.CharField(blank=True, max_length=128, null=True, verbose_name='备注')),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asset.Asset')),
            ],
            options={
                'verbose_name': 'RAM',
                'verbose_name_plural': 'RAM',
            },
        ),
        migrations.CreateModel(
            name='NetworkDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('sub_asset_type', models.SmallIntegerField(choices=[(0, '路由器'), (1, '交换机'), (2, '负载均衡'), (4, 'VPN设备')], default=0, verbose_name='服务器类型')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('vlan_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='VlanIP')),
                ('intranet_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='内网IP')),
                ('manufactory', models.CharField(blank=True, max_length=128, null=True, verbose_name='厂商')),
                ('model', models.CharField(blank=True, max_length=128, null=True, verbose_name='型号')),
                ('firmware', models.CharField(blank=True, max_length=128, null=True, verbose_name='固件信息')),
                ('port_num', models.SmallIntegerField(blank=True, null=True, verbose_name='端口个数')),
                ('device_detail', models.TextField(blank=True, null=True, verbose_name='设置详细配置')),
                ('asset', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='asset.Asset')),
            ],
            options={
                'verbose_name': '网络设备',
                'verbose_name_plural': '网络设备',
            },
        ),
        migrations.CreateModel(
            name='NewAssetApprovalZone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sn', models.CharField(max_length=128, unique=True, verbose_name='资产SN号')),
                ('asset_type', models.CharField(blank=True, choices=[('server', '服务器'), ('switch', '交换机'), ('router', '路由器'), ('firewall', '防火墙'), ('storage', '存储设备'), ('others', '其它类')], max_length=64, null=True)),
                ('manufactory', models.CharField(blank=True, max_length=64, null=True)),
                ('model', models.CharField(blank=True, max_length=128, null=True)),
                ('mem_size', models.IntegerField(blank=True, null=True)),
                ('cpu_model', models.CharField(blank=True, max_length=128, null=True)),
                ('cpu_count', models.IntegerField(blank=True, null=True)),
                ('cpu_core_count', models.IntegerField(blank=True, null=True)),
                ('os_type', models.CharField(blank=True, max_length=64, null=True)),
                ('os_release', models.CharField(blank=True, max_length=64, null=True)),
                ('data', models.TextField(verbose_name='资产数据')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='汇报日期')),
                ('approved', models.BooleanField(default=False, verbose_name='已批准')),
                ('approved_date', models.DateTimeField(blank=True, null=True, verbose_name='批准日期')),
            ],
            options={
                'verbose_name': '新上线待批准资产',
                'verbose_name_plural': '新上线待批准资产',
            },
        ),
        migrations.CreateModel(
            name='Nic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=64, null=True, verbose_name='网卡名')),
                ('ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP')),
                ('mac', models.CharField(max_length=64, unique=True, verbose_name='MAC')),
                ('netmask', models.CharField(blank=True, max_length=64, null=True)),
                ('status', models.BooleanField(default=False)),
                ('model', models.CharField(blank=True, max_length=128, null=True, verbose_name='网卡型号')),
                ('sn', models.CharField(blank=True, max_length=128, null=True, verbose_name='SN号')),
                ('memo', models.CharField(blank=True, max_length=128, null=True, verbose_name='备注')),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asset.Asset')),
            ],
            options={
                'verbose_name': '网卡',
                'verbose_name_plural': '网卡',
            },
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='主机名')),
                ('inner_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='内网IP')),
                ('management_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='管理IP')),
                ('server_attr', models.CharField(blank=True, max_length=128, null=True, verbose_name='服务器类型')),
                ('raid_type', models.CharField(blank=True, max_length=512, null=True, verbose_name='raid卡型号')),
                ('os_type', models.CharField(blank=True, max_length=64, null=True, verbose_name='操作系统平台')),
                ('os_release', models.CharField(blank=True, max_length=64, null=True, verbose_name='操作系统版本')),
                ('asset', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='asset.Asset')),
                ('upper_layer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='upperlayer', to='asset.Server', verbose_name='上层设备')),
            ],
            options={
                'verbose_name': '服务器',
                'verbose_name_plural': '服务器',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='Tag name')),
                ('create_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='asset',
            name='business_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='asset.BusinessUnit', verbose_name='所属业务线'),
        ),
        migrations.AddField(
            model_name='asset',
            name='device_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='asset.Manufactory', verbose_name='设备厂商'),
        ),
        migrations.AddField(
            model_name='asset',
            name='idc',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='asset.IDC', verbose_name='IDC机房'),
        ),
        migrations.AddField(
            model_name='asset',
            name='tags',
            field=models.ManyToManyField(blank=True, default=1, to='asset.Tag'),
        ),
        migrations.AlterUniqueTogether(
            name='nic',
            unique_together=set([('asset', 'mac')]),
        ),
        migrations.AlterUniqueTogether(
            name='mem',
            unique_together=set([('asset', 'slot')]),
        ),
        migrations.AlterUniqueTogether(
            name='disk',
            unique_together=set([('asset', 'slot')]),
        ),
    ]
