import factory
from django.contrib.auth import get_user_model
from factory import fuzzy


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Faker("user_name")
    email = factory.Faker("email")


class RestaurantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "diary.Restaurant"

    name = factory.Sequence(lambda n: f"{n} Restaurant")
    city = factory.Sequence(lambda n: f"{n} City")
    cuisine = factory.Sequence(lambda n: f"{n} cuisine")
    creator = factory.SubFactory(UserFactory)


class VisitFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "diary.Visit"

    date = factory.Faker("date_this_year")
    bill = fuzzy.FuzzyInteger(100, 10000)
    notes = factory.Faker("text")
    rating = factory.Faker("pyint", min_value=1, max_value=5)
    restaurant = factory.SubFactory(RestaurantFactory)
    creator = factory.SubFactory(UserFactory)
