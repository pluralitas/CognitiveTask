import nidaqmx, numpy as np

class daq:
    def __init__(self):
        self.daqfound = True
        try:
            with nidaqmx.Task() as consttask: # write 2.5V to ao1 for EMG Amplifiers
                consttask.ao_channels.add_ao_voltage_chan("Dev1/ao1")
                consttask.write(2.5,auto_start=True)
        except:
            self.daqfound = False

    def acqdaq(self,rate,sam):
        if self.daqfound == True:
            with nidaqmx.Task() as task:
                task.ai_channels.add_ai_voltage_chan("Dev1/ai0:3", terminal_config=nidaqmx.constants.TerminalConfiguration.RSE) #ai0:3 = QC Left, HS Left, QC Right, HS Right. Input terminal config=RSE(10083)
                task.timing.cfg_samp_clk_timing(rate=rate, sample_mode=nidaqmx.constants.AcquisitionType.FINITE)
                raw_in = task.read(number_of_samples_per_channel=sam)
            arr_out = np.array(raw_in)*1000
            arr_out = arr_out.astype('uint16').tolist()
    
        else:
            arr_out = [[0]*sam]*4
        return arr_out

if __name__ == "__main__":
    import time
    #Parameters
    samp_rate = 1000 #for DAQ (Hz)
    samples = 10 #per acquisition

    daqq = daq()

    while True:
        tim = time.time()
        arrdaq = daqq.acqdaq(samp_rate,samples)
        print(time.time()-tim)
        
        

