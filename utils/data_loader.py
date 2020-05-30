import sqlite3
import pandas as pd

class DataBaseReader:
    def __init__(self, data_path='redive_cn.db'):
        self.data_path = data_path
        self.conn = sqlite3.connect(self.data_path)

    # 获取角色基础数据
    def getCharaBase(self):
        charac_base_info = pd.read_sql_query(
            """
                SELECT ud.unit_id
                ,ud.unit_name
                ,ud.kana
                ,ud.prefab_id
                ,ud.move_speed
                ,ud.search_area_width
                ,ud.atk_type
                ,ud.normal_atk_cast_time
                ,ud.guild_id
                ,ud.comment
                ,ud.start_time
                ,up.age
                ,up.guild
                ,up.race
                ,up.height
                ,up.weight
                ,up.birth_month
                ,up.birth_day
                ,up.blood_type
                ,up.favorite
                ,up.voice
                ,up.catch_copy
                ,up.self_text
                ,IFNULL(au.unit_name, ud.unit_name) 'actual_name' 
                FROM unit_data AS ud 
                LEFT JOIN unit_profile AS up ON ud.unit_id = up.unit_id 
                LEFT JOIN actual_unit_background AS au ON substr(ud.unit_id,1,4) = substr(au.unit_id,1,4) 
                WHERE ud.comment <> '' 
            """, self.conn)
        return charac_base_info

    # 获取角色Rank汇总数据
    def getCharaPromotionStatus(self, unit_id:int):
        chara_promotion_status = pd.read_sql_query(
            """
                SELECT * 
                FROM unit_promotion_status 
                WHERE unit_id={uid} 
                ORDER BY promotion_level DESC
            """.format(uid=unit_id), self.conn)
        return chara_promotion_status

    # 获取角色装备数据
    def getCharaPromotion(self, unit_id:int):
        chara_promotion = pd.read_sql_query(
            """
                SELECT * 
                FROM unit_promotion 
                WHERE unit_id=$unitId
                ORDER BY promotion_level DESC 
            """.format(uid=unit_id), self.conn
        )
        return chara_promotion

    # 获取所有装备数据
    def getEquipmentAll(self):
        equipment_all = pd.read_sql_query(
            """
                SELECT 
                a.* 
                ,b.max_equipment_enhance_level 
                ,e.description 'catalog' 
                ,substr(a.equipment_id,3,1) * 10 + substr(a.equipment_id,6,1) 'rarity' 
                FROM equipment_data a, 
                ( SELECT promotion_level, max( equipment_enhance_level ) max_equipment_enhance_level FROM equipment_enhance_data GROUP BY promotion_level ) b 
                JOIN equipment_enhance_rate AS e ON a.equipment_id=e.equipment_id
                WHERE a.promotion_level = b.promotion_level 
                AND a.equipment_id < 113000 
                ORDER BY substr(a.equipment_id,3,1) * 10 + substr(a.equipment_id,6,1) DESC, a.require_level DESC, a.equipment_id ASC 
            """, self.conn
        )
        return equipment_all

    # 获取装备强化数据 param id 装备ids
    def getEquipmentEnhance(self, equipment_id: int):
        equipment_enhance = pd.read_sql_query(
            """
                SELECT * 
                FROM equipment_enhance_rate 
                WHERE equipment_id = {equipmentId}
            """.format(equipmentId=equipment_id), self.conn
        )
        return equipment_enhance

    # 获取所有装备强化数据
    def getEquipmentEnhance(self):
        equipment_enhance = pd.read_sql_query(
            """
                SELECT * 
                FROM equipment_enhance_rate 
            """, self.conn
        )
        return equipment_enhance

    # 获取角色技能数据
    def getUnitSkillData(self, unit_id:int):
        chara_skill = pd.read_sql_query(
            """
                SELECT * 
                FROM unit_skill_data 
                WHERE unit_id={uid}
            """.format(uid=unit_id), self.conn
        )
        return chara_skill

    # 获取技能数据
    def getSkillData(self, skill_id:int):
        skill_data = pd.read_sql_query(
            """
                SELECT * 
                FROM skill_data 
                WHERE skill_id={skillId}
            """.format(skillId=skill_id), self.conn
        )
        return skill_data

    # 获取技能动作数据
    def getSkillAction(self, action_id:int):
        action_data = pd.read_sql_query(
            """
                SELECT * 
                FROM skill_action 
                WHERE action_id={actionId}
            """.format(actionId=action_id), self.conn
        )
        return action_data

    # 获取行动顺序
    def getUnitAttackPattern(self, unit_id:int):
        attack_pattern = pd.read_sql_query(
            """
                SELECT * 
                FROM unit_attack_pattern 
                WHERE unit_id={uid} 
                ORDER BY pattern_id 
            """.format(uid=unit_id), self.conn
        )
        return attack_pattern

    # 获取会战期次
    def getClanBattlePeriod(self):
        cbp = pd.read_sql_query(
            """
                SELECT * 
                FROM clan_battle_period 
                ORDER BY clan_battle_id DESC 
            """, self.conn
        )
        return cbp

    # 获取会战phase
    def getClanBattlePhase(self, clanBattle_id:int):
        cp = pd.read_sql_query(
            """
                SELECT 
                a.difficulty 'phase'
                ,b1.wave_group_id 'wave_group_id_1'
                ,b2.wave_group_id 'wave_group_id_2'
                ,b3.wave_group_id 'wave_group_id_3'
                ,b4.wave_group_id 'wave_group_id_4'
                ,b5.wave_group_id 'wave_group_id_5'
                FROM clan_battle_map_data AS a 
                JOIN clan_battle_boss_group AS b1 ON a.clan_battle_boss_group_id = b1.clan_battle_boss_group_id AND b1.order_num = 1
                JOIN clan_battle_boss_group AS b2 ON a.clan_battle_boss_group_id = b2.clan_battle_boss_group_id AND b2.order_num = 2
                JOIN clan_battle_boss_group AS b3 ON a.clan_battle_boss_group_id = b3.clan_battle_boss_group_id AND b3.order_num = 3
                JOIN clan_battle_boss_group AS b4 ON a.clan_battle_boss_group_id = b4.clan_battle_boss_group_id AND b4.order_num = 4
                JOIN clan_battle_boss_group AS b5 ON a.clan_battle_boss_group_id = b5.clan_battle_boss_group_id AND b5.order_num = 5
                WHERE a.clan_battle_id={clanBattleId}
                ORDER BY a.difficulty DESC 
            """.format(clanBattleId=clanBattle_id), self.conn
        )
        return cp

    # 获取会战phase - wave
    def getWaveGroupData(self, wave_group_list:list):
        wgd = pd.read_sql_query(
            """
                SELECT * 
                FROM wave_group_data 
                WHERE wave_group_id IN ( {waveGroupList} ) 
            """.format(waveGroupList=','.join(wave_group_list)), self.conn
        )
        return wgd

    # 获取enemyList
    def getEnemy(self, enemy_id_list:list):
        el = pd.read_sql_query(
            """
                SELECT 
                a.* 
                ,b.union_burst 
                ,b.union_burst_evolution 
                ,b.main_skill_1 
                ,b.main_skill_evolution_1 
                ,b.main_skill_2 
                ,b.main_skill_evolution_2 
                ,b.ex_skill_1 
                ,b.ex_skill_evolution_1 
                ,b.main_skill_3 
                ,b.main_skill_4 
                ,b.main_skill_5 
                ,b.main_skill_6 
                ,b.main_skill_7 
                ,b.main_skill_8 
                ,b.main_skill_9 
                ,b.main_skill_10 
                ,b.ex_skill_2 
                ,b.ex_skill_evolution_2 
                ,b.ex_skill_3 
                ,b.ex_skill_evolution_3 
                ,b.ex_skill_4 
                ,b.ex_skill_evolution_4 
                ,b.ex_skill_5 
                ,b.sp_skill_1 
                ,b.ex_skill_evolution_5 
                ,b.sp_skill_2 
                ,b.sp_skill_3 
                ,b.sp_skill_4 
                ,b.sp_skill_5 
                ,u.prefab_id 
                ,u.atk_type 
                ,u.normal_atk_cast_time
                ,u.search_area_width
                FROM 
                unit_skill_data b 
                ,enemy_parameter a 
                LEFT JOIN unit_enemy_data u ON a.unit_id = u.unit_id 
                WHERE 
                a.unit_id = b.unit_id 
                AND a.enemy_id in ( {enemy_id_list} )  
            """.format(enemy_id_list=','.join(enemy_id_list)), self.conn)
        return el

    # 获取敌人抗性值
    def getResistData(self, resistStatus_id:int):
        redata = pd.read_sql_query(
            """
                SELECT * 
                FROM resist_data 
                WHERE resist_status_id={resistStatusId} 
            """.format(resistStatusId=resistStatus_id), self.conn
        )
        return redata

    # 获取友方召唤物
    def getUnitMinion(self, minion_id:int):
        unmi = pd.read_sql_query(
            """
                SELECT
                a.*,
                b.union_burst,
                b.union_burst_evolution,
                b.main_skill_1,
                b.main_skill_evolution_1,
                b.main_skill_2,
                b.main_skill_evolution_2,
                b.ex_skill_1,
                b.ex_skill_evolution_1,
                b.main_skill_3,
                b.main_skill_4,
                b.main_skill_5,
                b.main_skill_6,
                b.main_skill_7,
                b.main_skill_8,
                b.main_skill_9,
                b.main_skill_10,
                b.ex_skill_2,
                b.ex_skill_evolution_2,
                b.ex_skill_3,
                b.ex_skill_evolution_3,
                b.ex_skill_4,
                b.ex_skill_evolution_4,
                b.ex_skill_5,
                b.sp_skill_1,
                b.ex_skill_evolution_5,
                b.sp_skill_2,
                b.sp_skill_3,
                b.sp_skill_4,
                b.sp_skill_5
            FROM
                unit_skill_data b,
                unit_data a
            WHERE
                a.unit_id = b.unit_id
                AND a.unit_id = {minionId}
                """.format(minionId=minion_id), self.conn
        )
        return unmi

    # 获取敌方召唤物
    def getEnemyMinion(self, enemy_id:int):
        enmi = pd.read_sql_query(
            """
                            SELECT
                            d.unit_name,
                            d.prefab_id,
                            d.search_area_width,
                            d.atk_type,
                            d.move_speed,
                            a.*,
                            b.*,
                            d.normal_atk_cast_time,
                            c.child_enemy_parameter_1,
                            c.child_enemy_parameter_2,
                            c.child_enemy_parameter_3,
                            c.child_enemy_parameter_4,
                            c.child_enemy_parameter_5
                            FROM
                            enemy_parameter a
                            JOIN unit_skill_data AS b ON a.unit_id = b.unit_id
                            JOIN unit_enemy_data AS d ON a.unit_id = d.unit_id
                            LEFT JOIN enemy_m_parts c ON a.enemy_id = c.enemy_id
                            WHERE a.enemy_id = {enemyId}
                            """.format(enemyId=enemy_id), self.conn
        )
        return enmi

    # 获取会战bossList
    def getDungeons(self):
        dun = pd.read_sql_query(
            """
                SELECT
                a.dungeon_area_id,
                a.dungeon_name,
                a.description,
                b.*
                FROM
                dungeon_area_data AS a 
                JOIN wave_group_data AS b ON a.wave_group_id=b.wave_group_id 
                ORDER BY a.dungeon_area_id DESC 
            """, self.conn
        )
        return dun



if __name__ == "__main__":

    db = DataBaseReader('../data/redive_cn.db')

    df = db.getSkillData(1011001)
    print(df.head(10))
    for col in df.columns:
        print(col, df[col][0])

    df = db.getSkillAction(302100101)
    print(df.head(10))
    for col in df.columns:
        print(col, df[col][0])




