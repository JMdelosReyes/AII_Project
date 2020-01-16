from main.models import Generation, Type
from main.populate.populate_generations import populate_generations
from main.populate.populate_types import populate_types


def delete_data():
    Generation.objects.all().delete()
    Type.objects.all().delete()


def populate_database():
    print("Started database population")
    delete_data()

    populate_generations()
    populate_types()

    print("Finished database population")


if __name__ == '__main__':
    populate_database()
