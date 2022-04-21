static const ActionPtr actionPtr[NB_ACTION] = { // TODO: add all the function pointers corresponding to the Action enum in the right order.
        &actionNop,
        &actionExample1FromRunning,
        &actionExample1FromIdle,
        &actionExample2,
        &actionKill
    };


/**
 * @brief State machine of the Example class
 */

static Transition stateMachine[NB_STATE][NB_EVENT] = {
//startMAE
	[S_IDLE][E_EXAMPLE1]    = {S_RUNNING,	A_EXAMPLE1_FROM_IDLE},
    [S_RUNNING][E_EXAMPLE1] = {S_RUNNING, A_EXAMPLE1_FROM_RUNNING},
    [S_RUNNING][E_EXAMPLE2] = {S_IDLE, A_EXAMPLE2}
//endMAE
};


/* ----------------------- ACTIONS FUNCTIONS ----------------------- */

// TODO: Write all the action functions

static void actionExample1FromRunning(Example * this) {
    TRACE("[ActionEx1FromRunning] - %d\n", this->msg.param);