from gallery.models import AppliedArt, Works


def main():
    faulty_works = ''
    print("-----------------Начинается нанесение логотипа-----------------")

    works = Works.objects.all()
    for work in works:
        try:
            work.save()
            print(f"{work.name} -- Done!")
        except Exception as e:
            faulty_works += f"->{work.name} Создан: {work.pub_date} Ошибка: {e}\n"
            print(f"{e}-- Возникла ошибка пропускаю картину -- {work.name}")

    applied_arts = AppliedArt.objects.all()
    for applied_art in applied_arts:
        try:
            applied_art.save()
            print(f"{applied_art.name} -- Done!")
        except Exception as e:
            faulty_works += f"->{applied_art.name} Создан: {applied_art.pub_date} Ошибка: {e}\n"
            print(f"{e}-- Возникла ошибка пропускаю картину -- {applied_art.name}")

    report_txt = open("logo_report.txt", "w")
    report_txt.write(faulty_works)
    report_txt.close()
    print("-----------------Завершено нанесение логотипа-----------------")
