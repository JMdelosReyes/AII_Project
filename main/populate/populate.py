from main.models import Generation
from main.populate.populate_generations import populate_generations


def delete_data():
    Generation.objects.all().delete()


def populate_database():
    print("Started database population")
    delete_data()

    populate_generations()

    print("Finished database population")


if __name__ == '__main__':
    populate_database()
