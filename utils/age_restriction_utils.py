from datetime import date

from accounts.models import AuthUsers
from gallery.models import Works, AppliedArt


def get_safe_works(request, obj=None, applied_art=False):
    if obj:
        # for not authenticated users we show don't show 16+ content
        if not request.user.is_authenticated:
            filtered_works = obj.filter(age_restriction=False)
            return filtered_works

        else:
            current_user = AuthUsers.objects.get(email__exact=request.user.email).birth_date
            age_years = (date.today() - current_user).days // 365

            # for users who are under we don't show 16+ content
            if age_years < 16:
                filtered_works = obj.filter(age_restriction=False)
                return filtered_works

            # else we show 16+ content
            else:
                filtered_works = obj
                return filtered_works

    elif applied_art:
        # for not authenticated users we show don't show 16+ content
        if not request.user.is_authenticated:
            filtered_works = AppliedArt.objects.filter(age_restriction=False)
            return filtered_works

        else:
            current_user = AuthUsers.objects.get(email__exact=request.user.email).birth_date
            age_years = (date.today() - current_user).days // 365

            # for users who are under we don't show 16+ content
            if age_years < 16:
                filtered_works = AppliedArt.objects.filter(age_restriction=False)
                return filtered_works

            # else we show 16+ content
            else:
                filtered_works = AppliedArt.objects.all()
                return filtered_works

    else:
        # for not authenticated users we show don't show 16+ content
        if not request.user.is_authenticated:
            filtered_works = Works.objects.filter(age_restriction=False)
            return filtered_works

        else:
            current_user = AuthUsers.objects.get(email__exact=request.user.email).birth_date
            age_years = (date.today() - current_user).days // 365

            # for users who are under we don't show 16+ content
            if age_years < 16:
                filtered_works = Works.objects.filter(age_restriction=False)
                return filtered_works

            # else we show 16+ content
            else:
                filtered_works = Works.objects.all()
                return filtered_works
