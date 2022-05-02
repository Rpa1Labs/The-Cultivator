#include "CMotorControl.h"
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <thread>

#define PORT 800
#define QUEUE 20
#define NUMBER_MOTORS 2

/*
CODE DE RETOUR -> 1 byte -> 8 bits -> uint8_t
    0 : OK
    1 : MOTEUR INVALIDE
    2 : MOTEUR DEJA UTILISE
    3 : COMMANDE INVALIDE
*/

/**
 * @brief Manage socket requests
 * 
 * @param sConnection   Client connection id
 * @param motors        Array of step motors (CMotorControl)
 */
void manageRequest(int sConnection, CMotorControl* motors){
    
    unsigned long long int reception;

    //Récupère la requète du client
    recv(sConnection, &reception, 8, 0);

    //Décode la requète du client
    uint16_t          command      = (reception >> 48);
    uint16_t          num_motor    = (reception >> 32);
    unsigned long int distance     = reception & 0x00000000ffffffff;
    
    std::cout << "Command: " << command << std::endl;
    std::cout << "Motor: " << num_motor << std::endl;
    std::cout << "Distance: " << distance << std::endl;

    uint8_t returnCode = 0;

    //Exécute la fonction approprié avec le moteur correspondant
    if(num_motor >=NUMBER_MOTORS){

        std::cout << "Invalid motor number" << std::endl;
        returnCode = 1;

    }else if(motors[num_motor].isEnabled()){

        std::cout << "Motor already used" << std::endl;
        returnCode = 2;

    }else{

        switch (command)
        {
        case 0:
            std::cout << "Homming" << std::endl;
            motors[num_motor].homming();
            break;
        case 1:
            std::cout << "Set position" << std::endl;
            motors[num_motor].moveToCoordinate(distance);
            break;
        default:
            std::cout << "Invalid command number" << std::endl;
            returnCode = 3;
            break;
        }

    }

    //Envoi du code de retour
    send(sConnection, &returnCode, sizeof(uint8_t), 0);

    //Fermeture de la connexion une fois la fonction réalisée
    close(sConnection);
    return;
}

/**
 * @brief Main loop
 * 
 * @return int 
 */
int main()
{
    
    //Initialisation du serveur socket
    int ss = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in server_sockaddr;
    server_sockaddr.sin_family = AF_INET;         //protocole tcp
    server_sockaddr.sin_port = htons(PORT);       //port indiqué dans le define
    server_sockaddr.sin_addr.s_addr = INADDR_ANY; //toutes les sources sont acceptées

    //Vérifie si le serveur socket  est bien initialisé
    if (bind(ss, (struct sockaddr *)&server_sockaddr, sizeof(server_sockaddr)) == -1)
    {
        std::cout << "error bind";
        exit(1);
    }
    if (listen(ss, SOMAXCONN) == -1)
    {
        std::cout << "error listen";
        exit(1);
    }

    //Setup des GPIOs avec la classe CMotorControl
    
    #ifndef DEBUG
    GPIO::cleanup();
    GPIO::setmode(GPIO::BOARD);
    #endif

    CMotorControl* motors = new CMotorControl[NUMBER_MOTORS];
    motors[0].setup(18,22,24,19);
    motors[1].setup(26,38,36,21);

    //Boucle infinie pour ouvrir la connexion socket serveur-client
    while (1)
    {

        struct sockaddr_in client_addr;
        socklen_t length = sizeof(client_addr);

        //accepte la connexion du client
        int conn = accept(ss, (struct sockaddr *)&client_addr, &length);

        //si la connexion est acceptée correctement, on traite la requète dans un thread
        std::thread * t1;
        if( conn > 0 )  t1 = new std::thread(manageRequest,conn,motors);

    }
    close(ss);
    delete[] motors;
    return 0;
}


