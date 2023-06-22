from gallery.models import AppliedArt, Works, Views


def main():
    print("Starting migrations of 'views' to the 'Views' model")

    works = AppliedArt.objects.all()
    for work in works:
        views_rate = Views.objects.create(is_applied_art=True, applied_art=work)
        views_rate.views = work.views
        views_rate.save()

    works = Works.objects.all()
    for work in works:
        views_rate = Views.objects.create(is_applied_art=False, art_work=work)
        views_rate.views = work.views
        views_rate.save()
    print("Migration finished!")
