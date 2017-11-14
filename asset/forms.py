# # coding: utf-8
# __author__ = "HanQian"
#
from django.forms import ModelForm, TextInput,Select,SelectMultiple,DateTimeInput
from django.utils.translation import ugettext_lazy as _
from asset.models import *

from django.utils.html import escape,format_html
from django.utils.html import escape,format_html
from django.utils.encoding import force_text
from django.forms.utils import flatatt


class DDD(Select):
    def render(self, name, value, attrs=None):
        print(name, value,']]]]]]]]]]]]]]]]]')
        if value is None:
            value = ''
        # self.attrs.update({'class': '%s textinput' % self.attrs.get('class', '')})
        # final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        # if value != '':
        final_attrs={'class': 'form-control'}
        templ = """
        <select name="form-0-asset" class="form-control" id="id_form-0-asset">
  <option value="">---------</option>

  <option value="1">兆维aaaa机房-G-10-1</option>

  <option value="2">兆维机房-G-10-2</option>

  <option value="3">兆维机房-G-10-3</option>

  <option value="4">兆维机房-G-10-4</option>

  <option value="5">兆维机房-G-10-5</option>

  <option value="6">兆维机房-G-10-6</option>

  <option value="7">亦庄机房-B-10-6</option>

  <option value="8">亦庄机房-B-10-5</option>

  <option value="9">亦庄机房-B-10-4</option>

  <option value="10">亦庄机房-B-10-3</option>

  <option value="11">亦庄机房-B-10-2</option>

  <option value="12" selected="">亦庄机房-B-10-1</option>

  <option value="13">亦庄机房-F-20-22</option>

</select>
        """
        html = format_html(templ, flatatt(final_attrs))
        return html

class ServerForm(ModelForm):
    # def __init__(self,*args, **kwargs):
    #     super(ServerForm, self).__init__(*args, **kwargs)
    #     self.fields['name'].required = True
    # def clean_name(self):
    #     """自定义验证方法"""
    #     print("执行顺序2：clean_name")
    #     value = self.cleaned_data['name']
    #     if value == 'root':
    #         return value
    #     else:
    #         raise ValidationError("你不是管理员！")

    class Meta:
        model = Server
        fields = ('__all__')
        labels = {'asset': _('机柜'), }
        widgets = {
            "asset": DDD(attrs={'class': 'form-control'}),
            "name":TextInput(attrs={'class': 'form-control',}),
            "inner_ip":TextInput(attrs={'class': 'form-control',}),
            "management_ip":TextInput(attrs={'class': 'form-control',}),
            "device_status":Select(attrs={'class': 'form-control'}),
            "business_unit":Select(attrs={'class': 'form-control'}),
            "server_type":Select(attrs={'class': 'form-control'}),
            "upper_layer":Select(attrs={'class': 'form-control'}),
            "switch":Select(attrs={'class': 'form-control'}),
            "os_release": TextInput(attrs={'class': 'form-control', }),
            "os_type": TextInput(attrs={'class': 'form-control', }),
            "sn": TextInput(attrs={'class': 'form-control', }),
            "os_type": TextInput(attrs={'class': 'form-control', }),
            "device_type": Select(attrs={'class': 'form-control', }),
            "server_attr": TextInput(attrs={'class': 'form-control', }),
            "trade_date": DateTimeInput(attrs={'type':'date'}),
            "expire_date": DateTimeInput(attrs={'type':'date'}),
            "tags":SelectMultiple(attrs={'class': 'form-control'})
        }
        # help_texts = {'name': _('Some useful help text.'), }
        error_messages = {
            'name': {'required': _("请填写主机名"),'unique':'主机名必须唯一' },
            'sn': {'required': _("请填写SN"),'unique':'SN必须唯一' },
            # 'birth_date': {'required': _("时间不能为空"), },
        }

from django.forms.models import modelformset_factory
EditSeverFormSet = modelformset_factory(
            Server,  # model模型
            fields=('id','name', 'asset', 'device_status', 'server_type', 'upper_layer', 'switch'),
            max_num=1,  # 控制额外表单的显示数量，不会限制已经存在的表单对像的显示
            extra=1,  # 如果 max_num大于存在的关联对像的数量，表单集将添加 extra个额外的空白表单, 但表单总量不会超过 max_num 个
            widgets={
                "name": TextInput(attrs={'class': 'form-control', 'readonly': ''}),
                "asset": Select(attrs={'class': 'form-control'}),
                "device_status": Select(attrs={'class': 'form-control'}),
                "server_type": Select(attrs={'class': 'form-control'}),
                "upper_layer": Select(attrs={'class': 'form-control'}),
                "switch": Select(attrs={'class': 'form-control'}),
                "tags": SelectMultiple(attrs={'class': 'form-control'})
            }
        )