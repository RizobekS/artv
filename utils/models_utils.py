from accounts.models import Craftmanship
from general.models import Sections


def get_valid_craftmanship():
	craftmanships = Craftmanship.objects.all()

	for craftmanship in craftmanships:
		if not craftmanship.authors.exists():
			craftmanship.valid = False
		else:
			craftmanship.valid = True

	return craftmanships


def get_valid_sections():
	sections = Sections.objects.all().order_by("order")

	for section in sections:
		if not section.work_section.exists():
			section.valid = False
		else:
			section.valid = True

	return sections
