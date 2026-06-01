from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as file:
    readme = file.read()

setup(
    name="django_base_kit",
    version="0.1.4",
    license="MIT License",
    author="Thiago Azevedo",
    author_email="thiagoarvore@gmail.com",
    description=(
        "A fast initial setup for Django projects, providing a base model"
        "using UUID for the primarykey, active flag and auditlog."
        "As well a custom user model, "
        "authentication forms, and admin configuration."
    ),
    long_description=readme,
    long_description_content_type="text/markdown",
    keywords="django user authentication forms admin audit",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "django_base_kit": [
            "templates/*.html",
            "templates/*/*.html",
            "templates/*/*/*.html",
        ]
    },
    install_requires=["django", "django-widget-tweaks", "django-auditlog"],
)
