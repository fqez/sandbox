class PID:

    def __init__(self, reference=0, P=0, D=0, I=0, I_LEN=0):
        self.reference = reference
 
        self.P = P
        self.D = D
        self.I = I

        self.I_LEN = I_LEN
        self._error_history = []

        self.last_value = 0
        self.historical_error = 0
        self.alpha = 0.1

        self._feedback = 0
        
        self._error_P = 0
        self._error_D = 0
        self._error_I = 0

    def feedback(self, value=None):

        if value is None:
            return self._feedback

        self._error_P = value - self.reference
        self._error_D = self._error_P - self.last_value

        if self.I_LEN > 0:
            self._error_history += [self._error_P]
            n = len(self._error_history)
            if n > self.I_LEN:
                self._error_history = self._error_history[n-self.I_LEN:n]
            self._error_I = sum(self._error_history)
        else:
            self._error_I = self.alpha*self._error_P + (1-self.alpha)*self.historical_error   #media ponderada
        
        self.last_value = value
        self.historical_error = self._error_I

        self._feedback = self.P * self._error_P + self.D * self._error_D + self.I * self._error_I
        return self._feedback



        