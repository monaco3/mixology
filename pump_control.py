"""
Here we will control the motors/pumps
Each pump/motor is assigned to a specific chemical, which comes from the selected buffer

Run each motor/pump one by one till the required chemical weight target is reached

"""
import time
from private import *
import time
import logging
import logging.config
from logconfig import LOGGING_CONFIG
from labjack import ljm
#from labjack_pump_conn import mylabjack
#from scale_control import Initialise_Serial_Unit
from make_buffer import export_used_pumps as used_pumps, pump_pins, chemBuff_results, chemical_weights


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__) if __name__ == "__main__" else logging.getLogger()


# Set up logger
#logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Add a handler to print messages on the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
logger.addHandler(console_handler)


######-----Setting Motor High and Low independently maybe wont use it-------
def set_motor_high(pin, value):
    #ljm.eWriteName(mylabjack, pin, value)
    print(f"Set pin {pin} high")
def set_motor_low(pin):
    #ljm.eWriteName(mylabjack, pin, 0)
    print(f"Set pin {pin} low")
######-----Detting Motor High and Low independently maybe wont use it-------


class PumpController:
    def __init__(self,adjusted_weights):
        self.pumptesting = None
        self.adjusted_weights = adjusted_weights
        #self.scale = scale
        # Define flush and dosing parameters here or pass them as arguments to the methods

        self.pumptesting = {
            "Speed": 5.0,
            "Time": 2.0,
            "Mass": 0.1
        }
        self.flush = {
            "flush_speed": 5.0,
            "flush_step_time": 0.25,
            "flush_time": 2.0
        }

        self.dosing = {
            "FullSpeed": 1.0,  #5.0
            "SlowSpeed":0.8,    #2.5  so far the motors are not able to start running at 2.5 setting this to 3 and higher the motors are able to run
            "SlowMass": 0.10,
            "SlowFraction": 0.1,
            "AcceptanceMass": 0.4,
            "AcceptanceFraction": 0.01,
            "StepTime": 0.4,
            "StepPause": 0.8
        }

        self.chem_to_pump = {}
        for result in chemBuff_results:
            chemical_name = result[1]
            pump_no = result[2]
            self.chem_to_pump[chemical_name] = pump_no

    def PUMP(self, pump_no, pump_speed):
        pin = pump_pins[pump_no]
        if pump_speed > 0:
            #ljm.eWriteName(mylabjack, pin, pump_speed)
            print(f"Set pin {pin} high")
        else:
            #ljm.eWriteName(mylabjack, pin, 0)
            print(f"Set pin {pin} low")
        logger.debug('Set: Pump {} to speed: {}'.format(pump_no,pump_speed))

    def STOP(self):
        pump_off_signal = 0.0
        for pump in self.chem_to_pump.values():
            pin = pump_pins[pump]
            self.PUMP(pump, pump_off_signal)
        logger.debug('Pumps Stoped')
    

    def set_motor_pwm(self, pump_no, duty_cycle):
        pin = pump_pins[pump_no]
        #ljm.eWriteName(mylabjack, pin, duty_cycle)
        print(f"Set pin {pin} to duty cycle {duty_cycle}")


    def TARA(self):
        # Implement the TARA function here to tare the scale
        self.scale.tara()
        pass

    def WEIGHT(self):
        # Implement the WEIGHT function here to read the weight from the scale
        return self.scale.stable_weight()
        pass

    def READ_SCALE(self):
        # Implement the READ function here to read the data from the scale
        pass

    # run the pump for a short time
    def SHORT_RUN(self, pump_no):

        self.PUMP(pump_no, self.dosing['SlowSpeed'])
        time.sleep(self.dosing['StepTime'])
        self.STOP()
        time.sleep(self.dosing['StepPause'])
        pass

    #Flush the pumps to be used
    def FLUSH(self, pumps_used):
        for pump in pumps_used:
            self.PUMP(pump, self.flush['flush_speed'])
            time.sleep(self.flush['flush_step_time'])
            print("Flushing")

        time.sleep(self.flush['flush_time'])

        for pump in pumps_used:
            self.PUMP(pump, 0)  # 0 is the pump_off_signal
            time.sleep(self.flush['flush_step_time'])

        self.STOP()
        print("Stopped flushing")
    

    # def DOSE(self, pump_no, mass_target=None):
    #     if mass_target is None:
    #         for chemical, weight in self.adjusted_weights.items():
    #             if self.chem_to_pump[chemical] == pump_no:
    #                 mass_target = weight
    #                 break
    #     slow_buffer = max(self.dosing['SlowMass'], self.dosing['SlowFraction'] * mass_target)
    #     accept_buffer = max(self.dosing['AcceptanceMass'], self.dosing['AcceptanceFraction'] * mass_target)
    #     logger.debug("Slow_buffer: {}, accept_buffer: {}".format(slow_buffer, accept_buffer))
    #
    #     estimated_flow_rate = 1.0  # Set your estimated flow rate (in g/s or any other unit you prefer)
    #
    #     mass_pumped = 0.0
    #     while mass_target > mass_pumped + slow_buffer:
    #         duty_cycle = 1.0
    #         self.set_motor_pwm(pump_no, duty_cycle)
    #         time.sleep(1)  # Run the pump for 1 second at a time (adjust as needed)
    #         mass_pumped += estimated_flow_rate  # Update the mass_pumped based on the estimated flow rate
    #
    #     self.STOP()
    #
    #     pulse_duration = 0.1  # Define the pulse duration (adjust as needed)
    #     pulse_interval = 0.2  # Define the interval between pulses (adjust as needed)
    #
    #     while mass_target > mass_pumped + accept_buffer:
    #         duty_cycle = 1.0
    #         self.set_motor_pwm(pump_no, duty_cycle)
    #         time.sleep(pulse_duration)  # Run the pump for the pulse duration
    #         self.STOP()
    #         time.sleep(pulse_interval)  # Wait for the interval between pulses
    #         mass_pumped += estimated_flow_rate * pulse_duration  # Update the mass_pumped based on the estimated flow rate
    #
    #     self.STOP()
    #
    #     logger.info("Pump {} added: {:.2f} g".format(pump_no, mass_pumped))
    #     return mass_pumped
    #




    def DOSE(self, pump_no, mass_target=None):

        if mass_target is None:
            for chemical, weight in self.adjusted_weights.items():
                if self.chem_to_pump[chemical] == pump_no:
                    mass_target = weight
                    break
        slow_buffer = max(self.dosing['SlowMass'], self.dosing['SlowFraction'] * mass_target)
        accept_buffer = max(self.dosing['AcceptanceMass'], self.dosing['AcceptanceFraction'] * mass_target)
        logger.debug("Slow_buffer: {}, accept_buffer: {}".format(slow_buffer, accept_buffer))

        estimated_flow_rate = 1.0  # Set your estimated flow rate (in g/s or any other unit you prefer)

        mass_pumped = 0.0
        while mass_target > mass_pumped + slow_buffer:
            pump_speed = self.dosing['FullSpeed']
            self.PUMP(pump_no, pump_speed)
            time.sleep(1)  # Run the pump for 1 second at a time (adjust as needed)
            mass_pumped += estimated_flow_rate  # Update the mass_pumped based on the estimated flow rate

        self.STOP()


        #increasing the SlowSpeed value in the dosing dictionary, e.g., to 3.0 or 3.5. Next, adjust the pulse duration and interval to better match your motor's characteristics:

        n_pulses = 10  # Define the number of pulses (adjust as needed)
        pulse_duration = 0.1  # Define the pulse duration (adjust as needed)
        pulse_interval = 0.2  # Define the interval between pulses (adjust as needed)

        while mass_target > mass_pumped + accept_buffer:
            for _ in range(n_pulses):
                self.PUMP(pump_no, self.dosing['SlowSpeed'])  # Add 'SlowSpeed' to your dosing dictionary
                time.sleep(pulse_duration)  # Run the pump for the pulse duration
                self.STOP()
                time.sleep(pulse_interval)  # Wait for the interval between pulses
                mass_pumped += estimated_flow_rate * pulse_duration  # Update the mass_pumped based on the estimated flow rate


        #pulse_duration = 0.1  # Define the pulse duration (adjust as needed)
        #pulse_interval = 0.2  # Define the interval between pulses (adjust as needed)

       # while mass_target > mass_pumped + accept_buffer:
        #    self.PUMP(pump_no, self.dosing['SlowSpeed'])  # Add 'SlowSpeed' to your dosing dictionary
        #    time.sleep(pulse_duration)  # Run the pump for the pulse duration
            self.STOP()
        #    time.sleep(pulse_interval)  # Wait for the interval between pulses
         #   mass_pumped += estimated_flow_rate * pulse_duration  # Update the mass_pumped based on the estimated flow rate

        self.STOP()

        logger.info("Pump {} added: {:.2f} g".format(pump_no, mass_pumped))
        return mass_pumped




    def TEST(self, pump_no):
        estimated_flow_rate = 1.0  # Set your estimated flow rate (in g/s or any other unit you prefer)

        # Start the pump
        self.PUMP(pump_no, self.pumptesting['Speed'])
        time.sleep(self.pumptesting['Time'])
        self.STOP()

        # Calculate the mass increase based on the estimated flow rate and test time
        mass_increase = estimated_flow_rate * self.pumptesting['Time']

        if mass_increase > self.pumptesting['Mass']:
            logger.info('Mass increase by pump {}: {:0.2f}'.format(pump_no, mass_increase))
            return True
        else:
            logger.warning('Low mass increase by pump {}: {:0.2f}g'.format(pump_no, mass_increase))
            return False

# Create an instance of the PumpController class
pump_controller = PumpController(chemical_weights)

pump_controller.FLUSH(used_pumps.get_pumps())

for result in chemBuff_results:
    pump_no = result[2]
    pump_controller.DOSE(pump_no)

# Call the FLUSH method on the instance of the class, passing the list of pumps
#pump_controller.FLUSH(used_pumps.get_pumps())

