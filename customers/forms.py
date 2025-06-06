from django import forms
from customers.models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            "name", "phone_encrypted", "birth_encrypted", "gender",
            "attribute", "grade", "propensity", "intimacy", "priority",
            "is_target_customer", "is_active_touching","has_report", "memo"
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "w-full p-2 border rounded"}),
            "phone_encrypted": forms.TextInput(attrs={"class": "w-full p-2 border rounded"}),
            "birth_encrypted": forms.TextInput(attrs={
                "class": "w-full p-2 border rounded",
                "placeholder": "예: 19910802"
            }),
            "gender": forms.Select(attrs={"class": "w-full p-2 border rounded"}),
            "attribute": forms.Select(attrs={"class": "w-full p-2 border rounded"}),
            "grade": forms.Select(attrs={"class": "w-full p-2 border rounded"}),
            "propensity": forms.Select(attrs={"class": "w-full p-2 border rounded"}),
            "intimacy": forms.Select(attrs={"class": "w-full p-2 border rounded"}),
            "priority": forms.Select(attrs={"class": "w-full p-2 border rounded"}),
            "is_target_customer": forms.CheckboxInput(attrs={"class": "h-5 w-5"}),
            "is_active_touching": forms.CheckboxInput(attrs={"class": "h-5 w-5"}),
            "has_report": forms.CheckboxInput(attrs={"class": "h-5 w-5"}),
            "memo": forms.Textarea(attrs={"class": "w-full p-2 border rounded", "rows": 4}),
        }
        labels = {
            "name": "이름",
            "phone_encrypted": "전화번호",
            "birth_encrypted": "생년월일 (8자리)",
            "gender": "성별",
            "attribute": "고객 속성",
            "grade": "고객 등급",
            "propensity": "고객 성향",
            "intimacy": "라포 형성도",
            "priority": "우선 순위",
            "is_target_customer": "타겟 고객 여부",
            "is_active_touching": "터치 진행 여부",
            "has_report": "레포트 등록 여부",
            "memo": "메모",
        }

    def clean_birth_encrypted(self):
        data = self.cleaned_data["birth_encrypted"]
        if not data.isdigit() or len(data) != 8:
            raise forms.ValidationError("생년월일은 숫자 8자리(YYYYMMDD)로 입력하세요.")
        return data

    def clean_phone_encrypted(self):
        data = self.cleaned_data["phone_encrypted"]
        if not data.isdigit() or len(data) != 11:
            raise forms.ValidationError("전화번호는 숫자 11자리(예: 01012345678)로 입력하세요.")
        return data