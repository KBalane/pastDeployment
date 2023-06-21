from __future__ import unicode_literals
from digiinsurance.models.CompanyFAQ import CompanyFAQ

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from digiinsurance.models import *
from digiinsurance.models import TermsAndConditions
from digiinsurance.models.User import *
from digiinsurance.models.Company import *
from digiinsurance.models.Policy import *
from digiinsurance.models.InsureePolicy import *
from digiinsurance.models.Beneficiaries import *
from digiinsurance.models.HealthQuestions import *
from digiinsurance.models.Claims import *
from digiinsurance.models.payout import *
from digiinsurance.models.Transaction import *
from digiinsurance.models.Investment import *
from digiinsurance.models.UserFavourite import *
from digiinsurance.models.TermsAndConditions import *
from digiinsurance.models.UserBankAccount import *
from digiinsurance.models.EmailVerification import *
from digiinsurance.models.HealthQuestionsAnswers import *
from digiinsurance.models.BankAccounts import *
from digiinsurance.models.InsureePolicyDocs import *
from digiinsurance.models.CompanyRequirements import *
from digiinsurance.models.Advertisement import *
from digiinsurance.models.TempBeneficiaries import *

from digiinsurance.models import AuditEntry


class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': (
            'role', 'photo', 'step')}),
        (_('Permissions'), {'fields': ('is_active', 'is_superuser',
                                       'groups', 'user_permissions',
                                       'is_verified', 'info_submitted')}),
    )

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('username', 'email', 'password1', 'mobile_number',
                       'password2', 'role')}),
    )

    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = (
        'username', 'email', 'mobile_number',
        'last_login', 'date_joined', 'role', 'is_active', 'is_verified', )
    list_filter = ('role', 'is_active', 'is_verified', )
    ordering = ('date_joined', )


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'domain', 'created_at', )


# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('key', 'name', 'description', 'created_at')


class InsureeAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'middle_name', 'last_name', 'email', 'gender',
        'mobile_number')
    ordering = ('created_at', )

    search_fields = ('first_name', 'middle_name', 'last_name', 'email')


class InsureePaymentDetailAdmin(admin.ModelAdmin):
    list_display = ('key', 'name', 'description', 'created_at')


class StaffAdmin(admin.ModelAdmin):
    list_display = (
        'staff_first_name', 'staff_middle_name', 'staff_last_name',
        'staff_email', 'staff_mobile_number', )
    ordering = ('created_at', )
    search_fields = (
        'staff_first_name', 'staff_middle_name', 'staff_last_name',
        'staff_email', )

    def staff_first_name(self, obj):
        return obj.user.first_name

    def staff_middle_name(self, obj):
        return obj.user.middle_name

    def staff_last_name(self, obj):
        return obj.user.last_name

    def staff_email(self, obj):
        return obj.user.email

    def staff_mobile_number(self, obj):
        return obj.user.mobile_number

    staff_first_name.short_description = 'First Name'
    staff_first_name.admin_order_field = 'user__first_name'
    staff_middle_name.short_description = 'Middle Name'
    staff_middle_name.admin_order_field = 'user__middle_name'
    staff_last_name.short_description = 'Last Name'
    staff_last_name.admin_order_field = 'user__last_name'
    staff_email.short_description = 'Email'
    staff_email.admin_order_field = 'user__email'
    staff_mobile_number.short_description = 'Mobile Number'
    staff_mobile_number.admin_order_field = 'user__mobile_number'


# class RSVPAdmin(admin.ModelAdmin):
#     list_display = (
#         'student', 'student_email', 'student_company', 'student_course',
#         'event', )
#     list_filter = ('event__title', )
#     ordering = ('date', )

#     def student_email(self, obj):
#         return obj.student.email

#     def student_company(self, obj):
#         return obj.student.company

#     def student_course(self, obj):
#         return obj.student.course

#     student_email.short_description = 'Email'
#     student_email.admin_order_field = 'student__email'
#     student_company.short_description = 'Company'
#     student_company.admin_order_field = 'student__company'
#     student_course.short_description = 'Course'
#     student_course.admin_order_field = 'student__course'


# class EventAdmin(admin.ModelAdmin):
#     list_display = (
#         'title', 'venue', 'companys', 'courses', 'date', )
#     ordering = ('id', )


# class ExamQuestionAdmin(SummernoteModelAdmin):
#     summernote_fields = ('text', )


# class CoursewareAdmin(SummernoteModelAdmin):
#     summernote_fields = ('content', )


# class FeatureAdmin(SummernoteModelAdmin):
#     summernote_fields = ('content', )


# class EnrollmentAdmin(admin.ModelAdmin):
#     list_display = (
#         'student', 'enrolled_object', 'date_enrolled', 'date_completed',
#         'status', )
#     list_filter = ('status', )
#     search_fields = (
#         'student__first_name', 'student__last_name', 'student__email', )


class PaymentDetailAdmin(admin.ModelAdmin):
    list_display = (
        'txn_id', 'enrollment', 'company', 'amount', 'vat', 'fee',
        'completed_at', 'processor', 'processor_type', )
    list_filter = ('processor', 'processor_type', )

    search_fields = (
        'txn_id', 'enrollment__student__first_name',
        'enrollment__student__last_name', 'enrollment__student__email',
        'company__name',
    )


class PayoutAdmin(admin.ModelAdmin):
    list_display = (
        'payment', 'company', 'amount', 'completed_at',)
    search_fields = ('payment__txn_id', 'company__name')

@admin.register(AuditEntry)
class AuditEntryAdmin(admin.ModelAdmin):
    list_display = ['action', 'username', 'ip',]
    list_filter = ['action',]


# admin.site.register(Event, EventAdmin)
# admin.site.register(RSVP, RSVPAdmin)
# admin.site.register(DataCompany)
# admin.site.register(DataCourse)
# admin.site.register(DailyNewUser)
# admin.site.register(DailyActiveUser)
admin.site.register(TempBeneficiaries)
admin.site.register(User, MyUserAdmin)
admin.site.register(Insuree, InsureeAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(UserBankAccount)
admin.site.register(EmailVerification)
admin.site.register(Company, CompanyAdmin)
admin.site.register(CompanyFAQ)
admin.site.register(Beneficiaries)
admin.site.register(HealthQuestions)
admin.site.register(HealthQuestionsAnswers)
admin.site.register(BankAccount)
admin.site.register(Claims)
admin.site.register(Payout)
admin.site.register(Policy)
admin.site.register(InsureePolicy)
admin.site.register(Transaction)
admin.site.register(InsureePolicyDocs)
admin.site.register(CompanyRequirements)
admin.site.register(Advertisement)
admin.site.register(PolicyCalculator)
admin.site.register(PolicyRequirements)
admin.site.register(CompanyInvestmentType)
admin.site.register(UserInvestment)
admin.site.register(Favourites)
admin.site.register(TermsAndCondition)
# admin.site.register(CourseBundle)
# admin.site.register(Grade)
# admin.site.register(Courseware, CoursewareAdmin)
# admin.site.register(Class)
# admin.site.register(ClassBundle)
# admin.site.register(Schedule)
# admin.site.register(Attendance)
# admin.site.register(Feedback)
# admin.site.register(DocumentTemplate)
# admin.site.register(CompanySocials)
# admin.site.register(Product, ProductAdmin)
# admin.site.register(CompanyConfig)

# admin.site.register(PaymentDetail, PaymentDetailAdmin)
# admin.site.register(PayoutDetail)
# admin.site.register(Payout, PayoutAdmin)
# admin.site.register(BatchPayout)
# admin.site.register(Loan)

# admin.site.register(Classroom)
# admin.site.register(ClassroomSchedule)
# admin.site.register(Reservation)
# admin.site.register(CourseCampaign)

# admin.site.register(Enrollment, EnrollmentAdmin)
# admin.site.register(Progress)

# admin.site.register(Exam)
# admin.site.register(ExamQuestion, ExamQuestionAdmin)
# admin.site.register(ExamChoice)
# admin.site.register(ExamSubmission)
# admin.site.register(InsureeExamAnswer)

# admin.site.register(Feature, FeatureAdmin)
