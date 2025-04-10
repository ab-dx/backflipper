import pandas as pd
import yaml
import os

class FRAME_FROM_CSV:
    def __init__(self):
        self.file = "./output.csv"
        with open('config.yml', 'r') as file:
            self.config = yaml.safe_load(file)

    def get_frame(self, frame):
        frame_ref = 0
        data = pd.read_csv(self.file)
        counter = 0
        frame_tensor = []
        for i in data.values:
            counter+=1
            frame_tensor.append(i[1])
            if(counter%(3*len(self.config['ragdoll']['unique']))==0):
                if(frame == frame_ref):
                    #print("Frame Tensor Length:", len(frame_tensor), "Frame count:", frame_ref)
                    return frame_tensor
                    #print(frame_tensor)
                # Train RNN or generate point map
                frame_tensor = []
                frame_ref += 1

    def get_all_frames(self):
        master_data = []
        # for file in os.listdir(os.fsencode('./data/')):
        #     data = pd.read_csv('./data/'+os.fsdecode(file))
        #     frame_tensor = []
        #     counter = 0
        #     for i in data.values:
        #         counter += 1
        #         frame_tensor.append(i[1])
        #         if (counter%(3*len(self.config['ragdoll']['unique']))==0):
        #             master_data.append(frame_tensor)
        #             frame_tensor = []

        data = pd.read_csv('./centered.csv')
        frame_tensor = []
        counter = 0
        for i in data.values:
            counter += 1
            frame_tensor.append(i[1])
            if (counter%(3*len(self.config['ragdoll']['unique']))==0):
                master_data.append(frame_tensor)
                frame_tensor = []

        print(len(master_data[9]))
        return master_data

# f = FRAME_FROM_CSV()
# f.get_all_frames()
# f.get_frame(1)
#print(data.iloc[:39])
