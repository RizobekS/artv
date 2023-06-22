from gallery.models import Works, AppliedArt


def main():
    with open("no_images.txt", "w") as f:
        print("START - checking works with no image")
        works = Works.objects.all()
        for work in works:
            try:
                width = work.photo.width
            except FileNotFoundError:
                f.write(f"{work.author} - {work.name}\n")
                print(f"{work.name} with no image")

        works = AppliedArt.objects.all()
        for work in works:
            try:
                width = work.photo.width
            except FileNotFoundError:
                f.write(f"{work.author} - {work.name}\n")
                print(f"{work.name} with no image")
        print("FINISHED - checking works with no image")


