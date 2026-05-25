from compendium.forms import (
    RegisterForm,
    SubscriberForm
)


def test_register_form_valid_data(db):
    form = RegisterForm(data={
        "username": "testuser",
        "email": "test@example.com",
        "password1": "StrongPass123!",
        "password2": "StrongPass123!",
    })
    assert form.is_valid()


def test_register_form_missing_email(db):
    form = RegisterForm(data={
        "username": "testuser",
        "email": "",
        "password1": "StrongPass123!",
        "password2": "StrongPass123!",
    })
    assert "email" in form.errors


def test_register_form_passwords_do_not_match(db):
    form = RegisterForm(data={
        "username": "testuser",
        "email": "test@example.com",
        "password1": "StrongPass123!",
        "password2": "WrongPass123!",
    })
    assert "password2" in form.errors


def test_register_form_all_fields_have_form_control_class(db):
    form = RegisterForm()
    for field in form.fields.values():
        assert field.widget.attrs.get("class") == "form-control"


def test_subscriber_form_valid_email(db):
    form = SubscriberForm(data={"email": "sub@example.com"})
    assert form.is_valid()


def test_subscriber_form_invalid_email(db):
    form = SubscriberForm(data={"email": "not-an-email"})
    assert "email" in form.errors


def test_subscriber_form_missing_email(db):
    form = SubscriberForm(data={"email": ""})
    assert "email" in form.errors