from django.db import models
from django.contrib.auth.models import User

class Skill(models.Model):
    skill_name = models.CharField(max_length = 100)

    def __str__(self):
        return self.skill_name

class Organization(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    org_name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="")
    about_org = models.TextField(max_length = 500)
    org_website = models.CharField(max_length=100)

    def __str__(self):
        return self.user.org_name

class Country(models.Model):
    class Meta:
        verbose_name_plural = "Countries" # name to display in Django Admin interface, which defaults plural to class name + 's'

    country = models.TextField(max_length = 100)
    def __str__(self):
        return self.country

class City(models.Model):
    class Meta:
        verbose_name_plural = "Cities" # name to display in Django Admin interface, which defaults plural to class name + 's'

    city = models.TextField(max_length = 100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.city + ", " + Country.objects.get(city=self).country

class Posting(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    title = models.CharField(max_length = 250)
    description = models.TextField(max_length = 1000)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    posted_on = models.DateField()
    last_updated_on = models.DateField()
    posting_url = models.URLField(max_length=300)
    contact_details = models.CharField(max_length = 250)

    def __str__(self):
        return self.organization.org_name + ' - ' + self.title

    class Meta:
        ordering = ['-last_updated_on'] # sort posting in descending order

class PostingSkills(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    posting = models.ForeignKey(Posting, on_delete=models.CASCADE)
