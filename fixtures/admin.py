from django.contrib import admin

from . import models


# class FxitureGuessInline(admin.TabularInline):
    # model = models.FixtureGuess

admin.site.register(models.Fixture)
admin.site.register(models.Team)
