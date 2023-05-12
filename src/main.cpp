#include <iostream>
#include <vector>
#include <cstdlib>
#include <iterator>
#include <string>
#include <cstring>
#include "AmeliorationLocale.h"
using namespace std;

/**
 * Fonction utilitaire permettant de lire le fichier contenant les donnees de votes
 * @param nom_fichier : le nom du fichier
 * @param resultats_vote : une matrice qui contiendra le resultat de la lecture
 */
void lire_fichier_votes(string nom_fichier, vector<vector<int>>& resultats_vote){
    resultats_vote.clear();
    ifstream infile(nom_fichier);
    int nb_colonnes, nb_lignes;
    vector<int> ligne;
    int resultat;
    if (infile.is_open()) {
        infile >> nb_colonnes >> nb_lignes;
        for (int i = 0; i < nb_lignes; i++){
            ligne.clear();
            for(int j = 0; j < nb_colonnes; j++){
                infile >> resultat;
                ligne.push_back(resultat);
            }
            resultats_vote.push_back(ligne);
        }
        infile.close();
    }
    else {
        cout << "Impossible d'ouvrir le fichier " << nom_fichier << endl;
        exit(1);
    }
}


/**
 * Fonction principale
 */
int main(int argc, char* argv[]) {
    if (argc < 5){
        cout << "Argument ou parametre manquant lors de l'appel.\n";
        exit(1);
    }
    // Verification de l'argument -e
    if (strncmp(argv[1], "-e", 2) != 0){
        cout << "Argument "<< argv[1] << " inconnu.\n";
        exit(1);
    }
    string nom_fichier = argv[2];

    // Verification de l'argument -c
    if (strncmp(argv[3], "-c", 2) != 0){
        cout << "Argument "<< argv[3] << " inconnu.\n";
        exit(1);
    }
    vector<vector<int>> resultats_vote;
    string nombre_circonscriptions = argv[4];
    lire_fichier_votes(nom_fichier, resultats_vote);
    bool afficher_matrice = false;
    int id = 0;
    int nb_circonscriptions = stoi(nombre_circonscriptions);
    if (argc >= 6){
        if(strncmp(argv[5], "-p", 2) != 0){
            cout << "Argument " << argv[5] << "inconnu.\n";
            exit(0);
        }
        afficher_matrice = true;
    }
    if (argc == 8){
        if(strncmp(argv[6], "-id", 3) != 0){
            cout << "Argument " << argv[6] << "inconnu.\n";
            exit(0);
        }
        std::string id_str = argv[7];
        std::cout << "ID = " << id_str << endl;

        // Trim leading and trailing whitespace characters
        id_str.erase(id_str.begin(), std::find_if(id_str.begin(), id_str.end(), [](int ch) {
            return !std::isspace(ch);
        }));
        id_str.erase(std::find_if(id_str.rbegin(), id_str.rend(), [](int ch) {
            return !std::isspace(ch);
        }).base(), id_str.end());

        id = std::stoi(id_str);
    }
    AmeliorationLocale ameliorationLocale(id);
    ameliorationLocale.truquer_election(nb_circonscriptions, resultats_vote, afficher_matrice);
}
