#include <unistd.h>
#include <math.h>
#include <iostream>

//#define DEBUG

#define FAKEBUTTON 200
#define FAKEBUTTONRETURN 10

#ifndef DEBUG
#include <JetsonGPIO.h>
#endif

//TODO: Créer la fonction de homming + homming automatique

//m_direction = 0 -> sens positif, m_direction = 1 -> sens négatif

/**
 * @brief Basic class to control one step motor
 * 
 */

#define STEPS_FOR_ACCELERATION 100
#define MIN_DELAY 2
#define MAX_DELAY 20
#define COEF_ACCELERATION  pow((float)MAX_DELAY/MIN_DELAY,(float)1/(STEPS_FOR_ACCELERATION+1))

#define PI 3.1415926535897932384626433832795
//Diamètre en mm
#define DIAMETER 12.5
//Périmètre
#define PERIMETER (PI*DIAMETER)
//Pas pour faire un tour
#define STEPS_PER_REVOLUTION 200
#define STEP_PER_DISTANCE STEPS_PER_REVOLUTION/PERIMETER

class CMotorControl{
    private:
        bool m_direction;
        bool m_enable;
        int m_pinEnable;
        int m_pinDir;
        int m_pinPul;
        int m_pinButton;
        long m_stepsPosition;
        void pulse();
        void changeEnable(bool state);
        void setDirection(bool direction);
        void shiftWithSteps(unsigned long int steps);
    public:
        CMotorControl();
        void setup(int pinEnable,int pinDir,int pinPul,int pinButton);
        void homming();
        void moveToCoordinate(unsigned long int distance);
        bool isEnabled();

};