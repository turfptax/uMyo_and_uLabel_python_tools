
class uLabel:    
    def __init__(self, uid):
        self.last_pack_id = 0
        self.unit_id = uid
        self.packet_type = 0
        self.data_count = 0
        self.batt = 0
        self.version = 0
        self.data_id = 0
        self.prev_data_id = 0
        self.hall_values = [0] * 5
#	sQ Qsg;
#	sQ zeroQ;
        self.Qsg = [0,0,0,0]
        self.zeroQ = [0,0,0,0]
        self.ax = 0
        self.ay = 0
        self.az = 0
        self.dev_yaw = 0
        self.dev_pitch = 0
        self.dev_roll = 0
        self.update_time = 0
    
    

