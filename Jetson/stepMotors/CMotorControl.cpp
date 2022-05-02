#include "CMotorControl.h" 


#ifdef DEBUG
unsigned long long pulsations = 0;
#endif


/**
 * @brief Construct a new CMotorControl::CMotorControl object
 * 
 */
CMotorControl::CMotorControl()
:m_direction(0),m_enable(0),m_pinEnable(0),m_pinDir(0),m_pinPul(0),m_pinButton(0),m_stepsPosition(0){

}

/**
 * @brief PIN setup of step motor
 * 
 * @param pinEnable ENA on the motor driver
 * @param pinDir    DIR on the motor driver
 * @param pinPul    PUL on the motor driver
 * @param pinButton PIN of end-of-run switch
 */
void CMotorControl::setup(int pinEnable,int pinDir,int pinPul,int pinButton){
  m_pinEnable = pinEnable;
  m_pinDir    = pinDir;
  m_pinPul    = pinPul;
  m_pinButton = pinButton;
 
  #ifndef DEBUG
  GPIO::setup(m_pinEnable ,GPIO::OUT);
  GPIO::setup(m_pinDir    ,GPIO::OUT);
  GPIO::setup(m_pinPul    ,GPIO::OUT);
  GPIO::setup(m_pinButton ,GPIO::IN);

  GPIO::output(m_pinEnable,0);
  GPIO::output(m_pinDir   ,m_direction);
  GPIO::output(m_pinPul   ,0);
  #endif
}

#ifdef DEBUG
/**
 * @brief Display for debug the number of steps realized
 * 
 */
void displayRealizedSteps(){
  std::cout << "Number of steps realized: " << pulsations << std::endl;
  pulsations = 0;
}
#endif

/**
 * @brief Move to position zero by detect the position with the button
 * 
 */
void CMotorControl::homming(){
  changeEnable(1);
  // Acceleration
  #if STEPS_FOR_ACCELERATION > 0
  double coef =  MAX_DELAY;
  #endif
  #if STEPS_FOR_ACCELERATION <= 0
  double coef =  MIN_DELAY;
  #endif

  setDirection(1);

  for( unsigned long int i=0 ; i<STEPS_FOR_ACCELERATION ; i++){

    #ifndef DEBUG
    if(GPIO::input(m_pinButton)) break;
    #endif

    coef = coef/COEF_ACCELERATION;

    #ifdef DEBUG
    std::cout << "Coef: " << coef << std::endl;
    #endif

    pulse();
    usleep(coef*1000);
    
  }

  // Vitesse cste
  #ifndef DEBUG
  while(!GPIO::input(m_pinButton)){
  #endif
  #ifdef DEBUG
  for(int i = 0; i<FAKEBUTTON;i++){
  #endif
    pulse();
    usleep(coef*1000);
  }

  #ifdef DEBUG
  displayRealizedSteps();
  #endif

  usleep(MAX_DELAY*1000);

  setDirection(0);

  #ifndef DEBUG
  while(GPIO::input(m_pinButton)){
  #endif
  #ifdef DEBUG
  for(int i = 0; i<FAKEBUTTONRETURN;i++){
  #endif
    pulse();
    usleep(MAX_DELAY*1000);
  }
  
  // Met à 0 la position
  m_stepsPosition = 0;

  changeEnable(0);

  #ifdef DEBUG
  displayRealizedSteps();
  #endif


}

/**
 * @brief Shift of 1 step on the step motor
 * 
 */
void CMotorControl::pulse(){
  #ifndef DEBUG
  GPIO::output(m_pinPul,1);
  usleep(100);
  GPIO::output(m_pinPul,0);
  #endif
  #ifdef DEBUG
  pulsations++;
  #endif
}

/**
 * @brief Change the direction of the step motor
 * 
 * @param direction 0 for positive direction and 1 for negative direction
 */
void CMotorControl::setDirection(bool direction){
  m_direction = direction;
  #ifndef DEBUG
  GPIO::output(m_pinDir,m_direction);
  #endif
}

/**
 * @brief Return if the step motor is enabled or not
 * 
 * @return true The step motor is enabled
 * @return false The step motor is disabled
 */
bool CMotorControl::isEnabled(){
  return m_enable;
}

/**
 * @brief Enable or disable the step motor
 * 
 * @param state 0 for disabled and 1 for enabled
 */
void CMotorControl::changeEnable(bool state=0){
  #ifndef DEBUG
  GPIO::output(m_pinEnable,state);
  #endif
  m_enable = state;
}

/**
 * @brief Move position to specific coordinates
 * 
 * @param distance coordinate in mm
 */
void CMotorControl::moveToCoordinate(unsigned long int distance){
  changeEnable(1);
  unsigned long int targetSteps = (unsigned long int) distance*STEP_PER_DISTANCE;
  if( targetSteps > m_stepsPosition){
    setDirection(0);
    shiftWithSteps(targetSteps-m_stepsPosition);
    m_stepsPosition = targetSteps;
  }else if(targetSteps < m_stepsPosition){
    setDirection(1);
    shiftWithSteps(m_stepsPosition-targetSteps);
    m_stepsPosition = targetSteps;
  }
  changeEnable(0);
}

/**
 * @brief Move the step motor by a number of steps
 * 
 * @param steps Number of steps
 */
void CMotorControl::shiftWithSteps(unsigned long int steps){
  std::cout << steps << std::endl;
  unsigned long int stepsForForwardSpeed = steps-(STEPS_FOR_ACCELERATION<<1);
  unsigned long int stepsForAcceleration = STEPS_FOR_ACCELERATION;

  // Si le nombre de pas a faire est inférieur au nombre de pas pour l'acceleration
  if(steps <= (STEPS_FOR_ACCELERATION<<1)){
    stepsForForwardSpeed=0;         // Pas de vitesse cste
    stepsForAcceleration=steps>>1;  // Moitié du temps accélération et moitié du temps déccélération
  }

  // Acceleration
  #if STEPS_FOR_ACCELERATION > 0
  double coef =  MAX_DELAY;
  #endif
  #if STEPS_FOR_ACCELERATION <= 0
  double coef =  MIN_DELAY;
  #endif
  for( unsigned long int i=0 ; i<stepsForAcceleration ; i++){
    coef = coef/COEF_ACCELERATION;
    pulse();
    usleep(coef*1000);

    #ifdef DEBUG
    std::cout << "Coef: " << coef << std::endl;
    #endif
    
  }

  // Vitesse cste
  for(int i=0;i<stepsForForwardSpeed;i++){
    pulse();
    usleep(coef*1000);
  }

  // Décceleration
  for( unsigned long int i=0 ; i<stepsForAcceleration ; i++){
    coef = coef*COEF_ACCELERATION;
    pulse();
    usleep(coef*1000);

    #ifdef DEBUG
    std::cout << "Coef: " << coef << std::endl;
    #endif
    
  }

  #ifdef DEBUG
  displayRealizedSteps();
  #endif

}

