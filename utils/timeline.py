from utils.unit_model import Unit

# TODO:
class TimeLine:
    def __init__(self, ally_unit:list[Unit], enemy_unit:list[Unit], union_burst):
        self.time_frame_list = []
        self.time_frame_list.append(TimeLineFrame(ally_unit, enemy_unit, union_burst))

    def getTimeFrame(self, time):
        return self.time_frame_list[time]

    def get_last_frame(self):
        return self.time_frame_list[-1]

    def update(self):
        self.time_frame_list.append(self.get_last_frame().update())

    def