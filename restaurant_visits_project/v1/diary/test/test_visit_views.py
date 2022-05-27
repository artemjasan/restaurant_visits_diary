import pytest
from datetime import date, timedelta
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient

from .conftest import try_all_authentications_with_codes
from .factories import RestaurantFactory, UserFactory, VisitFactory
from .mock_test_data import BASE_RESTAURANTS_URL, BASE_VISIT_URL


@pytest.mark.django_db
@pytest.mark.parametrize(**try_all_authentications_with_codes(401, 200, 200))
def test_get_visits_list_different_auths_status_code(
    visit_factory: VisitFactory, configured_api_client: APIClient, status_code: int
):
    visit_factory.create_batch(2)
    response = configured_api_client.get(BASE_VISIT_URL)

    assert response.status_code == status_code


@pytest.mark.django_db
def test_get_visits_list_can_see_their_restaurants(
    user_factory: UserFactory,
    visit_factory: VisitFactory,
    api_client: APIClient,
):
    def _check_user_sees_only_their_visits(user: User, visits_number: int):
        api_client.force_authenticate(user=user)
        response = api_client.get(BASE_VISIT_URL)
        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == visits_number

    first_user = user_factory.create()
    second_user = user_factory.create()
    third_user = user_factory.create()
    visit_factory.create_batch(2, creator=first_user)
    visit_factory.create_batch(4, creator=second_user)

    # Check that users see only their own visits
    _check_user_sees_only_their_visits(first_user, 2)
    _check_user_sees_only_their_visits(second_user, 4)
    # Third user has no visits
    _check_user_sees_only_their_visits(third_user, 0)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "is_registered,is_creator,status_code",
    [
        (False, False, 401),  # anonymous
        (True, False, 403),  # registered, not a restaurant creator
        (True, True, 200),  # review creator
    ],
)
def test_user_can_get_their_detail_visits(
    create_user,
    visit_factory: VisitFactory,
    api_client: APIClient,
    is_registered: bool,
    is_creator: bool,
    status_code: int,
):
    user = create_user(is_registered=is_registered, is_staff=False)
    if is_creator:
        visit = visit_factory.create(creator=user)
    else:
        visit = visit_factory.create()

    api_client.force_authenticate(user)
    response = api_client.get(BASE_VISIT_URL + f"{visit.pk}/")
    assert response.status_code == status_code

    if status_code == status.HTTP_200_OK:
        response = api_client.get(BASE_VISIT_URL + f"{visit.pk}/")
        assert response.data["date"] == str(visit.date)
        assert response.data["bill"] == visit.bill
        assert response.data["notes"] == visit.notes
        assert response.data["rating"] == visit.rating


@pytest.mark.django_db
@pytest.mark.parametrize(
    "is_registered,is_creator,status_code",
    [
        (False, False, 401),  # anonymous
        (True, False, 403),  # registered, not a restaurant creator
        (True, True, 200),  # review creator
    ],
)
def test_user_can_update_their_visits(
    create_user,
    visit_factory: VisitFactory,
    api_client: APIClient,
    is_registered: bool,
    is_creator: bool,
    status_code: int,
):
    user = create_user(is_registered=is_registered, is_staff=False)
    if is_creator:
        visit = visit_factory.create(creator=user, bill=1000)
    else:
        visit = visit_factory.create(bill=1000)

    api_client.force_authenticate(user)
    response = api_client.patch(BASE_VISIT_URL + f"{visit.pk}/", data={"bill": 9999})
    assert response.status_code == status_code

    if status_code == status.HTTP_200_OK:
        response = api_client.get(BASE_VISIT_URL + f"{visit.pk}/")
        assert response.data["bill"] == 9999


@pytest.mark.django_db
@pytest.mark.parametrize(
    "is_registered, is_creator,status_code",
    [
        (False, False, 401),  # anonymous
        (True, False, 403),  # registered, not a restaurant creator
        (True, True, 204),  # review creator
    ],
)
def test_user_can_delete_their_visits(
    create_user,
    visit_factory: VisitFactory,
    api_client: APIClient,
    is_registered: bool,
    is_creator: bool,
    status_code: int,
):
    user = create_user(is_registered=is_registered, is_staff=False)
    if is_creator:
        visit = visit_factory.create(creator=user)
    else:
        visit = visit_factory.create()

    api_client.force_authenticate(user)
    response = api_client.delete(BASE_VISIT_URL + f"{visit.pk}/")
    assert response.status_code == status_code


@pytest.mark.django_db
def test_user_can_not_update_wrong_date_to_visit(
    user_factory: UserFactory,
    restaurant_factory: RestaurantFactory,
    visit_factory: VisitFactory,
    api_client: APIClient,
):
    user = user_factory.create()
    restaurant = restaurant_factory.create(creator=user)
    next_day = (date.today() + timedelta(1)).isoformat()

    api_client.force_authenticate(user)

    # Create a new visit to the restaurant
    visit = visit_factory.create(creator=user, restaurant=restaurant)

    response_patch = api_client.patch(BASE_VISIT_URL + f"{visit.pk}/", data={"date": next_day})
    assert response_patch.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_restaurant_avr_rating_changes_on_visit_create(
    user_factory: UserFactory,
    restaurant_factory: RestaurantFactory,
    visit_factory: VisitFactory,
    api_client: APIClient,
):
    user = user_factory.create()
    restaurant = restaurant_factory.create(creator=user)

    api_client.force_authenticate(user=user)
    response = api_client.get(BASE_RESTAURANTS_URL + f"{restaurant.pk}/")
    # Check avr rating
    assert response.status_code == status.HTTP_200_OK
    assert response.data["average_rating"] == 0.0

    # Add 2 visits to the restaurant
    visit_first = visit_factory.create(creator=user, restaurant=restaurant)
    visit_second = visit_factory.create(creator=user, restaurant=restaurant)

    response = api_client.get(BASE_RESTAURANTS_URL + f"{restaurant.pk}/")
    # Check new avr rating
    assert response.status_code == status.HTTP_200_OK
    assert response.data["average_rating"] == round(
        (visit_first.rating + visit_second.rating) / len(response.data["visits"]), 1
    )


@pytest.mark.django_db
def test_restaurant_avr_rating_changes_on_visit_update(
    user_factory: UserFactory,
    restaurant_factory: RestaurantFactory,
    visit_factory: VisitFactory,
    api_client: APIClient,
):
    user = user_factory.create()
    restaurant = restaurant_factory.create(creator=user)
    visit_first = visit_factory.create(creator=user, restaurant=restaurant, rating=5)
    visit_second = visit_factory.create(creator=user, restaurant=restaurant)

    api_client.force_authenticate(user=user)

    # Check avr rating with 2 visits
    response = api_client.get(BASE_RESTAURANTS_URL + f"{restaurant.pk}/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["average_rating"] == round(
        (visit_first.rating + visit_second.rating) / len(response.data["visits"]), 1
    )

    # Change rating for the first visit
    new_rating = 1
    api_client.patch(BASE_VISIT_URL + f"{visit_first.pk}/", data={"rating": new_rating})

    # Check avr rating after visit updating
    response = api_client.get(BASE_RESTAURANTS_URL + f"{restaurant.pk}/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["average_rating"] == round(
        (new_rating + visit_second.rating) / len(response.data["visits"]), 1
    )


@pytest.mark.django_db
def test_restaurant_avr_rating_changes_on_visit_delete(
    user_factory: UserFactory,
    restaurant_factory: RestaurantFactory,
    visit_factory: VisitFactory,
    api_client: APIClient,
):
    user = user_factory.create()
    restaurant = restaurant_factory.create(creator=user)
    visit_first = visit_factory.create(creator=user, restaurant=restaurant)
    visit_second = visit_factory.create(creator=user, restaurant=restaurant)

    api_client.force_authenticate(user=user)

    # Check avr rating with 2 visits
    response = api_client.get(BASE_RESTAURANTS_URL + f"{restaurant.pk}/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["average_rating"] == round(
        (visit_first.rating + visit_second.rating) / len(response.data["visits"]), 1
    )

    # Delete the first visit
    api_client.delete(BASE_VISIT_URL + f"{visit_first.pk}/")

    # Check avr rating after visit deletion
    response = api_client.get(BASE_RESTAURANTS_URL + f"{restaurant.pk}/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["average_rating"] == round(visit_second.rating / len(response.data["visits"]), 1)
