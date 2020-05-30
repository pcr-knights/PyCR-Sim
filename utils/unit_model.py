

class Unit:
    """
    基本的角色交互逻辑，保存角色的属性、Buff剩余持续时间和在动作循环中的位置
    """
    def __init__(self, data_path = "../data/redive_cn.db"):
        # TODO:根据uid利用data_loader读取角色信息，并根据装备、星数、rank、好感度计算属性值
        # data = DataBaseReader(data_path=data_path)
        self.unit_id = 1
        self.unique_id = 12     # Hash生成的独特id
        self.hp = 11767         # 生命值
        self.tp = 0             # 技能值
        self.atk_type = 1       # 攻击形式，1为物理，2为魔法
        self.atk_1 = 2703       # 物理攻击力
        self.atk_2 = 0          # 魔法攻击力
        self.def_1 = 124        # 物理抗性
        self.def_2 = 54         # 魔法抗性
        self.crit_1 = 53        # 物理暴击
        self.crit_2 = 0         # 魔法暴击
        self.hp_self_rec = 900  # 生命值自动回复
        self.tp_self_trec = 105 # 生命值自动回复
        self.life_steal = 0     # HP吸收
        self.hp_up = 10         # 回复量上升
        self.tp_up = 19         # TP回复量上升
        self.tp_reduce = 0      # TP消耗减轻
