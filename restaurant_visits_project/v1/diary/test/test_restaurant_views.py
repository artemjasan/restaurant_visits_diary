import pytest
from datetime import date, timedelta
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient

from .conftest import try_all_authentications_with_codes
from .factories import RestaurantFactory, UserFactory, VisitFactory
from .mock_test_data import BASE_RESTAURANTS_URL, RESTAURANT_DATA_BASE


@pytest.mark.django_db
@pytest.mark.parametrize(**try_all_authentications_with_codes(401, 200, 200))
def test_get_restaurant_list_different_auths_status_code(
    restaurant_factory: RestaurantFactory, configured_api_client: APIClient, status_code: int
):
    restaurant_factory.create_batch(2)
    response = configured_api_client.get(BASE_RESTAURANTS_URL)

    assert response.status_code == status_code


@pytest.mark.django_db
def test_get_restaurant_list_can_see_their_restaurants(
    user_factory: UserFactory,
    restaurant_factory: RestaurantFactory,
    api_client: APIClient,
):
    def _check_user_sees_only_their_restaurants(user: User, restaurants_number: int):
        api_client.force_authenticate(user=user)
        response = api_client.get(BASE_RESTAURANTS_URL)
        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == restaurants_number

    first_user = user_factory.create()
    second_user = user_factory.create()
    third_user = user_factory.create()
    restaurant_factory.create_batch(2, creator=first_user)
    restaurant_factory.create_batch(4, creator=second_user)

    # Check that users see only their own restaurants
    _check_user_sees_only_their_restaurants(first_user, 2)
    _check_user_sees_only_their_restaurants(second_user, 4)
    # Third user has no restaurants
    _check_user_sees_only_their_restaurants(third_user, 0)


@pytest.mark.django_db
@pytest.mark.parametrize(**try_all_authentications_with_codes(401, 201, 201))
def test_user_can_create_restaurant(
    configured_api_client: APIClient,
    status_code: int,
):
    response = configured_api_client.post(BASE_RESTAURANTS_URL, data=RESTAURANT_DATA_BASE, format="json")
    assert response.status_code == status_code


@pytest.mark.django_db
def test_fields_when_user_creates_restaurant(
    user_factory: UserFactory,
    api_client: APIClient,
):
    user = user_factory.create()
    api_client.force_authenticate(user=user)
    response = api_client.post(BASE_RESTAURANTS_URL, data=RESTAURANT_DATA_BASE, format="json")
    assert response.status_code == status.HTTP_201_CREATED

    assert response.data["name"] == RESTAURANT_DATA_BASE["name"]
    assert response.data["city"] == RESTAURANT_DATA_BASE["city"]
    assert response.data["cuisine"] == RESTAURANT_DATA_BASE["cuisine"]
    assert response.data["average_rating"] == 0.0
    assert response.data["visits"] == []


@pytest.mark.django_db
@pytest.mark.parametrize(
    "is_registered,is_creator,status_code",
    [
        (False, False, 401),  # anonymous
        (True, False, 403),  # registered, not a restaurant creator
        (True, True, 200),  # review creator
    ],
)
def test_user_can_get_their_detail_restaurants(
    create_user,
    restaurant_factory: RestaurantFactory,
    api_client: APIClient,
    is_registered: bool,
    is_creator: bool,
    status_code: int,
):
    user = create_user(is_registered=is_registered, is_staff=False)
    if is_creator:
        restaurant = restaurant_factory.create(creator=user)
    else:
        restaurant = restaurant_factory.create()

    api_client.force_authenticate(user)
    response = api_client.get(BASE_RESTAURANTS_URL + f"{restaurant.id}/")
    assert response.status_code == status_code

    if status_code == status.HTTP_200_OK:
        response = api_client.get(BASE_RESTAURANTS_URL + f"{restaurant.id}/")
        assert response.data["name"] == restaurant.name
        assert response.data["city"] == restaurant.city
        assert response.data["cuisine"] == restaurant.cuisine
        assert response.data["average_rating"] == 0.0
        assert response.data["visits"] == []


@pytest.mark.django_db
@pytest.mark.parametrize(
    "is_registered,is_creator,status_code",
    [
        (False, False, 401),  # anonymous
        (True, False, 403),  # registered, not a restaurant creator
        (True, True, 200),  # review creator
    ],
)
def test_user_can_update_their_restaurants(
    create_user,
    restaurant_factory: RestaurantFactory,
    api_client: APIClient,
    is_registered: bool,
    is_creator: bool,
    status_code: int,
):
    user = create_user(is_registered=is_registered, is_staff=False)
    if is_creator:
        restaurant = restaurant_factory.create(creator=user, name="Kozlovna")
    else:
        restaurant = restaurant_factory.create(name="Kozlovna")

    api_client.force_authenticate(user)
    response = api_client.patch(BASE_RESTAURANTS_URL + f"{restaurant.id}/", data={"name": "Vytopna"})
    assert response.status_code == status_code

    if status_code == status.HTTP_200_OK:
        response = api_client.get(BASE_RESTAURANTS_URL + f"{restaurant.id}/")
        assert response.data["name"] == "Vytopna"


@pytest.mark.django_db
@pytest.mark.parametrize(
    "is_registered, is_creator,status_code",
    [
        (False, False, 401),  # anonymous
        (True, False, 403),  # registered, not a restaurant creator
        (True, True, 204),  # review creator
    ],
)
def test_user_can_delete_their_restaurants(
    create_user,
    restaurant_factory: RestaurantFactory,
    api_client: APIClient,
    is_registered: bool,
    is_creator: bool,
    status_code: int,
):
    user = create_user(is_registered=is_registered, is_staff=False)
    if is_creator:
        restaurant = restaurant_factory.create(creator=user)
    else:
        restaurant = restaurant_factory.create()

    api_client.force_authenticate(user)
    response = api_client.delete(BASE_RESTAURANTS_URL + f"{restaurant.id}/")
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "is_registered,is_creator,status_code",
    [
        (False, False, 401),  # anonymous
        (True, False, 403),  # registered, not a restaurant creator
        (True, True, 201),  # review creator
    ],
)
def test_user_can_create_visit_for_their_restaurants(
    create_user,
    restaurant_factory: RestaurantFactory,
    api_client: APIClient,
    is_registered: bool,
    is_creator: bool,
    status_code: int,
):
    user = create_user(is_registered=is_registered, is_staff=False)
    if is_creator:
        restaurant = restaurant_factory.create(creator=user)
    else:
        restaurant = restaurant_factory.create()

    api_client.force_authenticate(user)
    response = api_client.post(
        BASE_RESTAURANTS_URL + f"{restaurant.id}/add_visit/",
        data={"date": "2022-05-20", "bill": 1000, "notes": "some text", "rating": 5},
    )
    assert response.status_code == status_code

    if status_code == status.HTTP_201_CREATED:
        assert response.data == f"A new visit to {restaurant.name} restaurant was added."


@pytest.mark.django_db
def test_user_can_not_set_wrong_date_to_visit(
    user_factory: UserFactory,
    restaurant_factory: RestaurantFactory,
    api_client: APIClient,
):
    user = user_factory.create()
    restaurant = restaurant_factory.create(creator=user)
    next_day = (date.today() + timedelta(1)).isoformat()

    api_client.force_authenticate(user)

    response = api_client.post(
        BASE_RESTAURANTS_URL + f"{restaurant.id}/add_visit/",
        data={"date": next_day, "bill": 1000, "notes": "some text", "rating": 5},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_fields_when_user_creates_restaurant_and_visit(
    user_factory: UserFactory,
    restaurant_factory: RestaurantFactory,
    visit_factory: VisitFactory,
    api_client: APIClient,
):
    user = user_factory.create()
    restaurant = restaurant_factory.create(creator=user)
    visit = visit_factory.create(creator=user, restaurant=restaurant)

    api_client.force_authenticate(user=user)
    response = api_client.get(BASE_RESTAURANTS_URL + f"{restaurant.pk}/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == restaurant.name
    assert response.data["city"] == restaurant.city
    assert response.data["cuisine"] == restaurant.cuisine
    assert response.data["average_rating"] == visit.rating  # We have only 1 visit

    visit_to_restaurant = response.data["visits"][0]  # We have only 1 visit

    assert visit_to_restaurant["date"] == str(visit.date)  # Need to convert to str format
    assert visit_to_restaurant["bill"] == visit.bill
    assert visit_to_restaurant["notes"] == visit.notes
    assert visit_to_restaurant["rating"] == visit.rating
    assert visit_to_restaurant["restaurant"] == restaurant.pk
