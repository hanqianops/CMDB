from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect

from asset import models

class BaseAdmin(object):
    """自定义admin类"""

    choice_fields = []
    fk_fields = []
    dynamic_fk = None
    dynamic_list_display = []
    dynamic_choice_fields = []
    m2m_fields = []

# admin.TabularInline  定义内联对象
class ServerAdmin(admin.TabularInline):
    model = models.Server
    exclude = ('memo',)
    readonly_fields = ['create_date',]

class MemAdmin(admin.TabularInline):
    model = models.Mem
    exclude = ('memo',)
    readonly_fields = ['create_date']

class CpuAdmin(admin.TabularInline):
    model = models.Cpu
    exclude = ('memo',)
    readonly_fields = ['create_date']

class NicAdmin(admin.TabularInline):
    model = models.Nic
    exclude = ('memo',)
    readonly_fields = ['create_date']

class DiskAdmin(admin.TabularInline):
    model = models.Disk
    exclude = ('memo',)
    readonly_fields = ['create_date']

# class AssetAdmin(admin.ModelAdmin):
#     list_display = ('sn','name','asset_type','status','id','device_type','idc','business_unit','trade_date')
#     inlines = [ServerAdmin,MemAdmin,CpuAdmin,NicAdmin,DiskAdmin]   # 内联字段
#     search_fields = ['sn',]   # 搜索控件
#     #list_filter = ['idc','manufactory','business_unit','asset_type']
#     choice_fields = ('asset_type','status')
#     #fk_fields = ('manufactory','idc','business_unit','admin')
#     list_per_page = 10   # 分页， 每页10条数据
#     list_filter = ('asset_type','status','device_type','idc','business_unit','trade_date')
#     dynamic_fk = 'asset_type'
#     dynamic_list_display = ('model','sub_asset_type','os_type','os_distribution')
#     dynamic_choice_fields = ('sub_asset_type',)
#     m2m_fields = ('tags',)  # 多对多

class IDCAdmin(admin.ModelAdmin):
    model = models.IDC

class NetworkDeviceAdmin(admin.ModelAdmin):
    model = models.NetworkDevice

class ManufactoryAdmin(admin.ModelAdmin):
    model = models.Manufactory

class BusinessUnitAdmin(admin.ModelAdmin):
    model = models.BusinessUnit

class TagAdmin(admin.ModelAdmin):
    model = models.Tag
class EventLogAdmin(admin.ModelAdmin,BaseAdmin):
    list_display = ('name','colored_event_type','component','detail','date')
    list_filter = ('event_type','component','date')

class NewAssetApprovalZoneAdmin(admin.ModelAdmin):
    list_display = ('sn','asset_type','manufactory','model','cpu_model','cpu_count','cpu_core_count','mem_size','os_release','date','approved','approved_date')
    actions = ['approve_selected_objects']
    def approve_selected_objects(modeladmin, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        ct = ContentType.objects.get_for_model(queryset.model)
        return HttpResponseRedirect("/asset/new_/static/approval/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))
    approve_selected_objects.short_description = "批准入库"

admin.site.register(models.IDC, IDCAdmin)
# admin.site.register(models.Asset,AssetAdmin)
admin.site.register(models.Server)
admin.site.register(models.Device_Status)
admin.site.register(models.Cpu)
admin.site.register(models.Disk)
admin.site.register(models.Nic)
admin.site.register(models.Mem)
admin.site.register(models.Asset)
admin.site.register(models.BusinessUnit,BusinessUnitAdmin)
admin.site.register(models.NetworkDevice, NetworkDeviceAdmin)
admin.site.register(models.Manufactory, ManufactoryAdmin)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.EventLog,EventLogAdmin)
admin.site.register(models.NewAssetApprovalZone,NewAssetApprovalZoneAdmin)