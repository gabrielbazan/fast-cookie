

run_unit_tests:
	./scripts/run_unit_tests.sh


{% if cookiecutter.add_database == 'Yes' %}
alembic_migration:
	./scripts/generate_alembic_migration.sh "${MESSAGE}"
{% endif -%}
