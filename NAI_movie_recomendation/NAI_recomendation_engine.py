#Program autorstwa: Kacper Wojtasiński, Piotr Palczewski
'''
Program silnika rekomendacji filmów na podstawie pliku JSON 
z danymi zebranymi od użytkowników składającego się z:
"imie_nazwisko":{
    "tytul_filmu": ocena,
    ...,
    }

Program sprawdza kompatybilność pomiędzy użytkownikami
na podstawie wspólnych filmów i ich ocen obliczając
odległość euklidesową lub Persona (zależnie od wyboru użytkownika)
na wykresie dwuwymiarowanym, wykorzystując klasteryzacje danych.
Wybiera się najbliższą osobę pod względem obejrzanych filmów 
i wybiera 6 filmów (o ile istnieją) których osoba dla której 
szukamy rekomendacji nie oglądała o ocenie powyżej 8 oraz 
6 filmów o ocenie poniżej 3. Jeśli takowe filmy nie istnieją zostają 
wyszukane u kolejnej najbliższej osoby.
'''
import json
import click
import numpy as np


class MoviesRecommendations:
    def __init__(self, data: dict) -> None:
        self._data = data
        self._closest_users = {"euclidean": {}, "pearson": {}}
        self._sort_movies_by_rating()

    @classmethod
    def from_json_file(cls, path: str) -> "MoviesRecommendations":
        with open(path) as _file:
            data = json.load(_file)
            return cls(data)
    """ Pobieranie danych z pliku json oraz zwracanie danych """
    @staticmethod
    def sort_dict_for_user(user: str, _dict: dict) -> dict:
        _dict[user] = {
            key: value
            for key, value in sorted(
                _dict[user].items(), key=lambda i: i[1], reverse=True
            )
        }
    ''' Grupowanie danych w formie par przy użyciu funkcji Dictionary '''

    def validate_users(self, *users):
    
        for user in users:
            if not user in self._data.keys():
                raise ValueError(f"Cannot find {user} in dataset")
    ''' Sprawdzenie czy użytkownik istnieje w pliku z danymi '''
    
    def _sort_movies_by_rating(self):

        for user in self._data.keys():
            self.sort_dict_for_user(user, self._data)
    ''' Sortowanie danych użytkownika po ocenie filmów '''
    
    
    """ Metoda obliczenia korelacji osób metodą Person'a """
    def _pearson_score(self, user1, user2):
        self.validate_users(user1, user2)
    
        # Filmy wspólne dla użytkownika szukającego rekomendacji i pozostałych użytkowników z bazy
        common_movies = {}
        
        # Pętla wyszukiwania wspólnych filmów
        for item in self._data[user1]:
            if item in self._data[user2]:
                common_movies[item] = 1

        num_ratings = len(common_movies)

        # Przy braku wspólnych filmów użytkowników wynikiem korelacji jest 0
        if num_ratings == 0:
            return 0

        # Obliczanie sumy ocen dzielonych filmów
        user1_sum = np.sum([self._data[user1][item] for item in common_movies])
        user2_sum = np.sum([self._data[user2][item] for item in common_movies])

        # Obliczanie sumy kwadratów ocen dzielonych filmów
        user1_squared_sum = np.sum(
            [np.square(self._data[user1][item]) for item in common_movies]
        )
        user2_squared_sum = np.sum(
            [np.square(self._data[user2][item]) for item in common_movies]
        )

        # Obliczanie sumy produków oceny wspólnych filmów
        sum_of_products = np.sum(
            [
                self._data[user1][item] * self._data[user2][item]
                for item in common_movies
            ]
        )

        # Obliczanie współczynnika korelacji Pearsona
        Sxy = sum_of_products - (user1_sum * user2_sum / num_ratings)
        Sxx = user1_squared_sum - np.square(user1_sum) / num_ratings
        Syy = user2_squared_sum - np.square(user2_sum) / num_ratings

        if Sxx * Syy == 0:
            return 0

        return Sxy / np.sqrt(Sxx * Syy)


    ''' Metoda obliczenia korelacji osób metodą euklidesową'''
    def _euclidean_score(self, user1, user2):
        self.validate_users(user1, user2)

        # Filmy wspólne dla użytkownika szukającego rekomendacji i pozostałych użytkowników z bazy
        common_movies = {}
        
        # Pętla wyszukiwania wspólnych filmów
        for item in self._data[user1]:
            if item in self._data[user2]:
                common_movies[item] = 1

        # Przy braku wspólnych filmów użytkowników wynikiem korelacji jest 0
        if len(common_movies) == 0:
            return 0
        
        #Różnica kwadratów odelgłości między punktami
        squared_diff = []
    
        #Pętla licząca różnice kwadratów odelgłości między punktami
        for item in self._data[user1]:
            if item in self._data[user2]:
                squared_diff.append(
                    np.square(self._data[user1][item] - self._data[user2][item])
                )

        return 1 / (1 + np.sqrt(np.sum(squared_diff)))

    ''' Metoda wyszukiwania najbliższego użytkownika na przestrzeni dwuwymiarowej '''
    def find_closest_users(self, name: str, method="euclidean"):
        score_function = (
            self._euclidean_score if method == "euclidean" else self._pearson_score
        )


        if not name in self._closest_users[method]:
            self._closest_users[method][name] = {}

            for user in self._data.keys():
                self._closest_users[method][name][user] = score_function(name, user)

            self.sort_dict_for_user(name, self._closest_users[method])

        return self._closest_users[method][name]

    ''' Metoda wyszukiwania unikalnych filmów użytkownika '''
    def find_unique_movies(self, for_user, from_user) -> dict:
        unique_movies_names = list(
            set(self._data[from_user].keys()) - set(self._data[for_user].keys())
        )

    
        unique_movies = {key: self._data[from_user][key] for key in unique_movies_names}

        return {
            key: value
            for key, value in sorted(
                unique_movies.items(), key=lambda i: i[1], reverse=True
            )
        }
    
    
    ''' Metoda wyszukiwania rekomendowanych filmów dla wybranego użytkownika
        wybraną metodą - euklidesową lub Pearsona'''
    def find_recommendations(
        self, user, method: str, points_for_best, points_for_worst, amount
    ) -> dict:
        best_movies = []
        worst_movies = []
        users = self.find_closest_users(user, method)

        
    # Pętla wyszukiwania najlepszych i najgorszych filmów u użytkownika najbliższego profilowi
        for _user in users:
            unique_movies = self.find_unique_movies(user, _user)
            for movie in unique_movies:
                if (
                    self._data[_user][movie] >= points_for_best
                    and len(best_movies) < amount
                ):
                    best_movies.append(movie)

                if (
                    self._data[_user][movie] <= points_for_worst
                    and len(worst_movies) < amount
                ):
                    worst_movies.append(movie)

                if len(best_movies) == amount and len(worst_movies) == amount:
                    return {"best": list(best_movies), "worst": list(worst_movies)}

        return {"best": list(best_movies), "worst": list(worst_movies)}
        
''' Interfejs wprowadzania danych w wierszu poleceń '''
@click.command()
@click.option("--path", prompt="Give path of JSON file")
@click.option("--method", prompt="Method", type=click.Choice(['euclidean', 'pearson']), default='euclidean')
@click.option("--user", prompt="User")
@click.option("--min_value", prompt="Min value (1, 10)", type=click.IntRange(1, 10), default=3)
@click.option("--max_value", prompt="Max value (1, 10)", type=click.IntRange(1,10), default=8)
@click.option("--amount", prompt="Amount (1, 6)", type=click.IntRange(1, 6), default=6)


def run(path, method, user, min_value, max_value, amount):
    r = MoviesRecommendations.from_json_file(path)
    r.validate_users(user)
    print(r.find_recommendations(user, method, max_value, min_value, amount))
''' Metoda wywoławcza'''

if __name__ == "__main__":
    run()
