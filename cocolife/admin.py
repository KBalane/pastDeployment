from django.contrib import admin


from cocolife.models.Feature import CLFeature
from cocolife.models.Product import *
from cocolife.models.InsureePolicyIssuanceSettings import *
from cocolife.models.Underwriting import *
from cocolife.models.DigiInsuree import *
from cocolife.models.PolicyOwner import *
from cocolife.models.Beneficiary import *
from cocolife.models.AgentAssisted import *
from cocolife.models.ProductInsuree import *

from cocolife.models.AppStat import *

from cocolife.models.CLHealthQuestions import *
from cocolife.models.CLHealthQuestionsAnswers import *
from cocolife.models.CLAdvertisements import *
from cocolife.models.DigiKYC import *
from cocolife.models.DigiTransaction import *
from cocolife.models.CompanyInformation import *


# Register your models here.
admin.site.register(AppStat)

admin.site.register(AgentAssisted)
admin.site.register(CLFeature)

admin.site.register(DigiInsuree)

admin.site.register(Underwriting)

admin.site.register(ProductInsuree)
admin.site.register(PolicyOwner)

admin.site.register(DigiUserID)

admin.site.register(Product)
admin.site.register(Package)
admin.site.register(Variant)
admin.site.register(Benefit)
admin.site.register(Premium)

admin.site.register(CLHealthQuestions)
admin.site.register(CLHealthQuestionsAnswers)

admin.site.register(DigiTransaction)
admin.site.register(CompanyInformation)

admin.site.register(InsureePolicyIssuanceSettings)
admin.site.register(Beneficiary)

admin.site.register(CLAdvertisements)
