#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
恶魔轮盘赌_v1.6.1
作者：余胜军徒儿
当前最新版本：v1.6.1
原创不易，严禁抄袭！

Ⓒ余胜军团队专属防伪标

等一下，如果您不是开发者的话，你是怎么接收到代码文件的？
"""

import random
import time

# ============ 游戏配置 ============
ITEM_POOL = ['手锯', '放大镜', '手铐', '香烟', '啤酒', '逆转器', '过期药品', '一次性手机']
ITEM_DESC = {
    '手锯': '下次实弹伤害×2',
    '放大镜': '查看弹膛中的子弹',
    '手铐': '跳过对方下回合',
    '香烟': '恢复1点生命值',
    '啤酒': '退掉弹巢中一发随机子弹',
    '逆转器': '反转下一发子弹（实弹变空包弹，空包弹变实弹）',
    '过期药品': '50%恢复2血，50%扣1血',
    '一次性手机': '一个神秘的声音，让你窥探未来',
    '上帝的生死状': '完全恢复所有生命值（仅正常模式可获得）',
}

MAX_INVENTORY = 8
MAX_HP = 5  # 生命值最高上限

# ============ 辅助函数 ============

def show_health(player_lifes, devil_lifes):
    print(f"\n  你的生命: {'♥' * player_lifes}")
    print(f"  恶魔生命: {'♥' * devil_lifes}")

def show_inventory(inventory):
    if not inventory:
        print("  (道具栏为空)")
        return
    counts = {}
    for item in inventory:
        counts[item] = counts.get(item, 0) + 1
    parts = []
    for item in sorted(counts.keys()):
        parts.append(f"{item}×{counts[item]}")
    print(f"  [道具: {', '.join(parts)}]")

def get_items_for_round():
    """获取本回合的初始道具：数量随机2~6个"""
    num_items = random.randint(2, 6)
    items = []
    for _ in range(num_items):
        items.append(random.choice(ITEM_POOL))
    print(f"  [获得道具: {', '.join(items)}]（共{num_items}个）")
    return items

def ensure_chamber(bullet_box, chamber_index, inventory=None, allow_items=True):
    """确保弹巢有弹，如果已空则重新装填。返回 (bullet_box, chamber_index, item)"""
    if not bullet_box or chamber_index >= len(bullet_box):
        bullet_box = ["实弹", "实弹", "实弹", "空包弹", "空包弹", "空包弹"]
        random.shuffle(bullet_box)
        chamber_index = 0
        item = None
        if allow_items and inventory is not None and len(inventory) < MAX_INVENTORY:
            item = random.choice(ITEM_POOL)
            inventory.append(item)
            print(f"  [弹巢已空，重新装填完毕] [获得道具: {item}]")
        else:
            print("  [弹巢已空，重新装填完毕]")
        # 换弹后显示实弹和空包弹数量
        print(f"  [换弹完毕: {bullet_box.count('实弹')}发实弹, {bullet_box.count('空包弹')}发空包弹]")
        return bullet_box, chamber_index, item
    return bullet_box, chamber_index, None

def fire_bullet(bullet_box, chamber_index, reverser_active=False, inventory=None, allow_items=True):
    """按弹膛顺序取出发射，返回 (子弹类型, 新的弹巢, 新的弹膛索引, 道具)"""
    item = None
    if not bullet_box or chamber_index >= len(bullet_box):
        bullet_box = ["实弹", "实弹", "实弹", "空包弹", "空包弹", "空包弹"]
        random.shuffle(bullet_box)
        chamber_index = 0
        if allow_items and inventory is not None and len(inventory) < MAX_INVENTORY:
            item = random.choice(ITEM_POOL)
            inventory.append(item)
            print(f"  [弹巢已空，重新装填] [获得道具: {item}]")
        else:
            print("  [弹巢已空，重新装填...]")
        # 换弹后显示实弹和空包弹数量
        print(f"  [换弹完毕: {bullet_box.count('实弹')}发实弹, {bullet_box.count('空包弹')}发空包弹]")

    bullet = bullet_box[chamber_index]
    chamber_index += 1

    if reverser_active:
        bullet = "空包弹" if bullet == "实弹" else "实弹"

    return bullet, bullet_box, chamber_index, item

def devil_turn(devil_lifes, bullet_box, skip_opponent, reverser_active=False, chamber_index=0, inventory=None, allow_items=True):
    """恶魔的回合，返回 (结果, bullet_box, chamber_index):
    'skipped'=被手铐跳过, 1=玩家扣血, 0=恶魔自残扣血, 'demon_goes_again'=恶魔自射空包弹继续行动
    """
    bullet_box, chamber_index, item = ensure_chamber(bullet_box, chamber_index, inventory, allow_items)
    print("\n--- 恶魔的回合 ---")
    time.sleep(1)

    if skip_opponent:
        print("  手铐效果发动！恶魔的回合被跳过！")
        return 'skipped', bullet_box, chamber_index, item

    action = random.choice(["打玩家", "打自己"])
    if action == "打玩家":
        print("  恶魔选择...打你！")
        time.sleep(0.8)
        bullet, bullet_box, chamber_index, item2 = fire_bullet(bullet_box, chamber_index, reverser_active, inventory, allow_items)
        if reverser_active:
            print("  [逆转器发动！子弹被反转了！]")
            reverser_active = False
        if bullet == "实弹":
            print("  恶魔开枪打中了你！你扣除1点生命值")
            return 1, bullet_box, chamber_index, item2
        else:
            print("  恶魔开枪...是空包弹！虚惊一场，轮到你的回合")
            return 'devil_blank_at_player', bullet_box, chamber_index, item2
    else:
        print("  恶魔选择...打自己！")
        time.sleep(0.8)
        bullet, bullet_box, chamber_index, item2 = fire_bullet(bullet_box, chamber_index, reverser_active, inventory, allow_items)
        if reverser_active:
            print("  [逆转器发动！子弹被反转了！]")
            reverser_active = False
        if bullet == "实弹":
            print("  恶魔对自己开了枪...是实弹！")
            return 0, bullet_box, chamber_index, item2
        else:
            print("  恶魔对自己开了枪...是空包弹！恶魔逃过一劫，再次行动！")
            return 'demon_goes_again', bullet_box, chamber_index, item2

def use_item(item_name, inventory, player_lifes, max_lifes, bullet_box, chamber_index, reverser_active=False, skip_opponent=False):
    """使用道具，返回 (inventory, player_lifes, effect)
    effect: 'double_damage'=手锯buff, 'skip_opponent'=手铐buff, 'reverser_active'=逆转器buff, None=即时生效
    """
    inventory.remove(item_name)

    if item_name == '手锯':
        print("  使用了【手锯】！下次实弹伤害×2")
        return inventory, player_lifes, 'double_damage'
    elif item_name == '放大镜':
        if not bullet_box or chamber_index >= len(bullet_box):
            print("  使用了【放大镜】！弹膛已空，下一发将触发重新装填，无法预览")
        else:
            preview = bullet_box[chamber_index]
            if reverser_active:
                preview = "空包弹" if preview == "实弹" else "实弹"
                print(f"  使用了【放大镜】！弹膛中的子弹是：{preview}（逆转器已生效）")
            else:
                print(f"  使用了【放大镜】！弹膛中的子弹是：{preview}")
        return inventory, player_lifes, None
    elif item_name == '手铐':
        if skip_opponent:
            print("  手铐效果尚未结束，无法再次使用手铐！")
            inventory.append(item_name)  # 放回道具栏
            return inventory, player_lifes, None
        print("  使用了【手铐】！对方下回合将被跳过")
        return inventory, player_lifes, 'skip_opponent'
    elif item_name == '香烟':
        new_lifes = min(player_lifes + 1, max_lifes)
        print(f"  使用了【香烟】！恢复了1点生命值 (当前: {new_lifes}/{max_lifes})")
        return inventory, new_lifes, None
    elif item_name == '啤酒':
        if bullet_box:
            discarded = bullet_box.pop(random.randint(0, len(bullet_box) - 1))
            print(f"  使用了【啤酒】！退掉了弹巢中的一发{discarded} (剩余: {len(bullet_box)}发)")
        else:
            print("  弹巢已空，无法退掉子弹")
            inventory.append(item_name)
        return inventory, player_lifes, None
    elif item_name == '逆转器':
        print("  使用了【逆转器】！下一发子弹将被反转")
        return inventory, player_lifes, 'reverser_active'
    elif item_name == '过期药品':
        if random.random() < 0.5:
            new_lifes = min(player_lifes + 2, max_lifes)
            player_lifes = new_lifes
            print(f"  使用了【过期药品】！运气不错，恢复了2点生命值 (当前: {new_lifes}/{max_lifes})")
        else:
            player_lifes -= 1
            print(f"  使用了【过期药品】！糟糕，是过期了...扣除1点生命值 (当前: {player_lifes}/{max_lifes})")
        return inventory, player_lifes, None
    elif item_name == "一次性手机":
        # 排除当前弹膛，取剩余可窥探的索引
        candidates = [i for i in range(len(bullet_box)) if i != chamber_index]
        if not candidates:
            print("弹巢里没有其他子弹可窥探了，手机没信号。")
            return inventory, player_lifes, None
        peek_idx = random.choice(candidates)
        bullet_type = bullet_box[peek_idx]
        print(f"📱 听筒里传来一个沙哑的声音：")
        print(f"   「第 {peek_idx + 1} 发是……{'实弹' if bullet_type == 1 else '空包弹'}。」")
        print("   随后是一阵电流杂音，手机彻底黑屏了。")
        return inventory, player_lifes, None

    elif item_name == '上帝的生死状':
        player_lifes = max_lifes
        print(f"  使用了【上帝的生死状】！上帝的契约生效，全部生命值已恢复至 {max_lifes}/{max_lifes}！")
        return inventory, player_lifes, None

    return inventory, player_lifes, None

def check_death_and_win(player_lifes, devil_lifes):
    """检查死亡和胜利条件"""
    if player_lifes <= 0:
        print("\n  你的生命值耗尽...")
        return 'player_lose'
    if devil_lifes <= 0:
        print("\n  恭喜！你击败了本回合的恶魔！")
        return 'player_win'
    return None

def play_round(round_num, player_hp, devil_hp, player_name="无名者", infinite_mode=False):
    """进行单个回合的游戏"""
    player_lifes = player_hp
    devil_lifes = devil_hp
    really = random.randint(1, 4)
    fake = random.randint(1, 4)
    bullet_box = ["实弹"] * really + ["空包弹"] * fake
    random.shuffle(bullet_box)
    chamber_index = 0

    # 获取本回合道具
    inventory = []
    if infinite_mode or round_num >= 3:
        # 无限模式或第3回合：正常获得随机道具
        inventory = get_items_for_round()
    elif round_num == 2:
        # 正常模式第2回合：获得彩蛋道具"上帝的生死状"
        inventory.append('上帝的生死状')
        print("  [获得彩蛋道具: 上帝的生死状]（仅正常模式可获得）")
    # 正常模式第1回合：不获得道具

    # 是否允许从弹巢换弹中获得道具
    allow_items = infinite_mode or round_num >= 3
    double_damage = False
    skip_opponent = False
    reverser_active = False

    print(f"\n{'#' * 40}")
    print(f"  >>> 第 {round_num} 回合开始 <<<")
    print(f"  初始弹巢: {bullet_box.count('实弹')}发实弹, {bullet_box.count('空包弹')}发空包弹")
    show_health(player_lifes, devil_lifes)

    turn = 'player'  # 当前回合方: 'player' 或 'demon'

    while player_lifes > 0 and devil_lifes > 0:
        bullet_box, chamber_index, item = ensure_chamber(bullet_box, chamber_index, inventory, allow_items)
        print(f"\n{'=' * 30}")
        show_health(player_lifes, devil_lifes)
        show_inventory(inventory)
        if double_damage:
            print("  [手锯效果激活: 下次实弹伤害×2]")

        if turn == 'player':
            # --- 玩家回合 ---
            print("\n--- 你的回合 ---")

            print("  1. 打恶魔")
            print("  2. 打自己")
            if inventory:
                print("  3. 使用道具")

            choice = input("  请选择行动 [1/2/3]: ").strip()

            if choice == '3' and inventory:
                print("\n  --- 使用道具 ---")
                counts = {}
                for item in inventory:
                    counts[item] = counts.get(item, 0) + 1
                for i, item in enumerate(sorted(counts.keys()), 1):
                    print(f"    {i}. {item} (×{counts[item]}) - {ITEM_DESC[item]}")

                item_choice = input("  选择使用道具 [编号]: ").strip()
                try:
                    item_idx = int(item_choice) - 1
                    selected_item = sorted(counts.keys())[item_idx]
                    inventory, player_lifes, effect = use_item(
                        selected_item, inventory, player_lifes, MAX_HP, bullet_box, chamber_index, reverser_active, skip_opponent
                    )
                    if effect == 'double_damage':
                        double_damage = True
                    elif effect == 'skip_opponent':
                        skip_opponent = True
                    elif effect == 'reverser_active':
                        reverser_active = True
                except (ValueError, IndexError):
                    print("  输入无效，跳过使用道具")
                continue

            elif choice == '1':
                bullet, bullet_box, chamber_index, _ = fire_bullet(bullet_box, chamber_index, reverser_active, inventory, allow_items)
                if reverser_active:
                    print("  [逆转器发动！子弹被反转了！]")
                    reverser_active = False
                if bullet == "实弹":
                    print(f"  {player_name}对着恶魔开了枪...是实弹！")
                    damage = 2 if double_damage else 1
                    devil_lifes -= damage
                    double_damage = False
                    show_health(player_lifes, devil_lifes)
                    result = check_death_and_win(player_lifes, devil_lifes)
                    if result:
                        return result
                    print(f"  {player_name}打中了恶魔...轮到恶魔的回合")
                else:
                    print(f"  {player_name}对着恶魔开了枪...是空包弹！")
                    print("  恶魔获得额外行动机会！")

                # 恶魔回合
                devil_result, bullet_box, chamber_index, _ = devil_turn(devil_lifes, bullet_box, skip_opponent, reverser_active, chamber_index, inventory, allow_items)
                skip_opponent = False
                if devil_result == 'skipped':
                    print("  恶魔回合被跳过，轮到你的下一轮")
                    turn = 'player'
                    continue
                elif devil_result == 'demon_goes_again':
                    turn = 'demon'
                    continue
                elif devil_result == 1:
                    player_lifes -= 1
                elif devil_result == 0:
                    devil_lifes -= 1
                    print("  恶魔扣除1点生命值")
                elif devil_result == 'devil_blank_at_player':
                    print("  恶魔射出空包弹，未造成任何效果")
                show_health(player_lifes, devil_lifes)
                result = check_death_and_win(player_lifes, devil_lifes)
                if result:
                    return result
                turn = 'player'

            elif choice == '2':
                bullet, bullet_box, chamber_index, _ = fire_bullet(bullet_box, chamber_index, reverser_active, inventory, allow_items)
                if reverser_active:
                    print("  [逆转器发动！子弹被反转了！]")
                    reverser_active = False
                if bullet == "实弹":
                    print(f"  {player_name}对着自己开了枪...是实弹！")
                    damage = 2 if double_damage else 1
                    player_lifes -= damage
                    double_damage = False
                    show_health(player_lifes, devil_lifes)
                    result = check_death_and_win(player_lifes, devil_lifes)
                    if result:
                        return result
                    print(f"  {player_name}勉强撑住了...轮到恶魔")

                    # 恶魔回合
                    devil_result, bullet_box, chamber_index, _ = devil_turn(devil_lifes, bullet_box, skip_opponent, reverser_active, chamber_index, inventory, allow_items)
                    skip_opponent = False
                    if devil_result == 'skipped':
                        print("  恶魔回合被跳过，轮到你的下一轮")
                        turn = 'player'
                        continue
                    elif devil_result == 'demon_goes_again':
                        turn = 'demon'
                        continue
                    elif devil_result == 1:
                        player_lifes -= 1
                    elif devil_result == 0:
                        devil_lifes -= 1
                        print("  恶魔扣除1点生命值")
                    elif devil_result == 'devil_blank_at_player':
                        print("  恶魔射出空包弹，未造成任何效果")
                    show_health(player_lifes, devil_lifes)
                    result = check_death_and_win(player_lifes, devil_lifes)
                    if result:
                        return result
                    turn = 'player'
                else:
                    print(f"  {player_name}对着自己开了枪...是空包弹！")
                    print("  运气不错，还是你的回合！")
                    continue
            else:
                print("  输入无效，请重新选择")
                continue

        else:
            # --- 恶魔的回合（连续行动）---
            devil_result, bullet_box, chamber_index, _ = devil_turn(devil_lifes, bullet_box, skip_opponent, reverser_active, chamber_index, inventory, allow_items)
            skip_opponent = False
            if devil_result == 'skipped':
                print("  恶魔回合被跳过，轮到你的下一轮")
                turn = 'player'
                continue
            elif devil_result == 'demon_goes_again':
                turn = 'demon'
                continue
            elif devil_result == 1:
                player_lifes -= 1
            elif devil_result == 0:
                devil_lifes -= 1
                print("  恶魔扣除1点生命值")
            elif devil_result == 'devil_blank_at_player':
                print("  恶魔射出空包弹，未造成任何效果")
            show_health(player_lifes, devil_lifes)
            result = check_death_and_win(player_lifes, devil_lifes)
            if result:
                return result
            turn = 'player'

    if player_lifes <= 0:
        return 'player_lose'
    return 'player_win'

# ============ 游戏主逻辑 ============

def start_game():
    print("=" * 40)
    print(" " * 14, "恶魔轮盘赌")
    print(" " * 11, "作者：余胜君徒儿")
    print("=" * 40)
    print("  规则：分3个回合，每回合血量随机（2~4点）")
    print("  每回合随机获得2~6个道具")
    print("  实弹扣1血，空包弹无事发生且追加一回合")
    print("  生命值归零则游戏立即结束！")
    print("  [道具系统] 每回合开始获得随机道具（仅无限模式）")
    print("    手锯: 下次实弹伤害×2    放大镜: 查看弹膛")
    print("    手铐: 跳过对方回合(效果未结束前不可重复使用)  香烟: 恢复1血    啤酒: 退掉一发子弹")
    print("    逆转器: 反转下一发子弹    过期药品: 50%恢复2血/50%扣1血")
    print("    一次性手机：一个神秘的声音，让你窥探未来")
    print("  子弹打完后重新装填时会额外获得1个道具")
    print("  正常模式中会有彩蛋道具")
    print("  生命值最高上限为5点")
    print("  每回合最多携带8个道具，回合结束后全部收回")
    print("  版本号：v1.6.1")
    print("  当前最新版本：v1.6.1(已更新)")
    print("=" * 40)

    print("\n  [恶魔的声音从黑暗中传来...]")
    time.sleep(1.5)
    print('  "凡人，在我与你对决之前，先签下这份生死状吧。"')
    time.sleep(1)
    print('  "签上你的名字，从此你的命运就与我绑定了..."')
    time.sleep(1.5)
    signed_name = input("\n  请输入你的名字: ").strip()
    if not signed_name:
        signed_name = "无名者"

    print(f"\n  【{signed_name}】，你的名字已被刻在生死状上。")
    time.sleep(1)

    # 询问是否进入无限模式
    infinite_mode = False
    choice = input("\n  是否进入无限模式？(y/n): ").strip().lower()
    if choice in ('y', 'yes', '是'):
        infinite_mode = True
        print("  [已进入无限模式]")
    else:
        print('  [正常模式] 前两个回合无法获得道具，第2回合可获得开发者的彩蛋道具')
    time.sleep(1.5)

    print("  游戏即将开始...祝你好运。")
    time.sleep(2)

    total_money = 0

    while True:
        if total_money > 0:
            print(f"\n  [当前资金: {total_money:,} 块钱]")

        for round_num in range(1, 4):
            # 每回合血量随机生成 2~4，玩家和恶魔血量相等
            p_hp = random.randint(2, 4)
            d_hp = p_hp  # 与玩家血量相等
            result = play_round(round_num, p_hp, d_hp, player_name=signed_name, infinite_mode=infinite_mode)
            if result == 'player_lose':
                print("\n" + "=" * 40)
                print(f"  {signed_name}，你的生命值已耗尽，游戏结束！")
                print("=" * 40)
                if total_money > 0:
                    print("  你输了... 资金被清零")
                    total_money = 0
                break
            elif result == 'player_win':
                if round_num < 3:
                    print(f"\n  你击败了第 {round_num} 回合的恶魔，准备进入下一回合...")
                    time.sleep(1.5)
                else:
                    print("\n" + "=" * 40)
                    print(f"  恭喜！{signed_name}，你通关了所有回合，恶魔被你彻底击败！")
                    print("=" * 40)

                    total_money += random.randint(10000, 100000)
                    print(f"\n  你获得了 {total_money:,} 块钱！")
                    time.sleep(1)

                    while True:
                        choice = input("\n  加倍还是放弃？(y/n): ").strip().lower()
                        if choice in ('y', 'yes', '是'):
                            print(f"\n  带着 {total_money:,} 块钱重新挑战！")
                            time.sleep(1.5)
                            break
                        elif choice in ('n', 'no', '否'):
                            print(f"\n  你带走了 {total_money:,} 块钱，再见！")
                            return
                        else:
                            print("  请输入 y 或 n")

        if total_money == 0:
            pass
        else:
            continue

        replay = input("\n  再来一局吗？(y/n): ").strip().lower()
        if replay not in ('y', 'yes', '是'):
            print("\n  感谢游玩，再见！")
            return
        continue


if __name__ == '__main__':
    start_game()