import math
import numpy as np
from random import choice, randint, sample
from mini_number_theory_lib import decomp_num
from arithmetic_link_list import ArithmeticLinkList


op_list = ["+", "-", "*", "/"]
max_num = 50
max_res = 50
max_try = 100000
recur_rand_time = int(math.log(max_num)) - 1
delta = 10 ** int(math.log10(max_num - 1))
int_list = []
for i in range(max_num // delta + 1):
    sub_list = (list(range(i * delta, min((i * delta + delta), max_num + 1))) * (max_num // delta + 1 - i))
    sub_list.sort()
    int_list.extend(sub_list)
i = 0
idx_2 = int_list.index(2)
int_list = [0, 1] + int_list[idx_2:]


def rand_a_int(inf=None, sup=None):
    if inf is None or inf == 0:
        idx_inf = 0
    else:
        idx_inf = int_list.index(inf)

    if sup is None or sup == max_num:
        idx_sup = -1
    else:
        idx_sup = int_list.index(sup + 1)

    return choice(int_list[idx_inf:idx_sup])


def recur_rand(num_time, inf=0):
    num = max_num
    for idx in range(num_time):
        num = rand_a_int(inf, sup=num)
        print(num)
    return num


def rand_a_node(node, num_list, lv=0, num_try=0):

    print(node.expr + "开始")
    inf = 0
    sup = max_num
    if lv < 0:
        inf = min(50, (max_num // 100) << (- lv * 2))
    elif lv > 0:
        sup = max(20, max_num >> (lv * 2))

    if "*" not in node.op_list and "/" not in node.op_list:
        while True:
            num_try += 1
            if num_try > max_try:
                raise ValueError(f"已经尝试生成超过{max_try}次了!")
            for idx in node.idx_list:
                num_list[idx] = rand_a_int()
            # 即便计算结果不符合范围条件, 仍然有10%的几率通过
            val = node.eval(num_list)
            if val < 0 or val > max_res:
                continue
            if sup >= val >= inf or randint(0, 9) == 0:
                break

    elif node.op == "*":

        if node.left_type >= 0 and node.right_type >= 0:
            while True:
                num_try += 1
                if num_try > max_try:
                    raise ValueError(f"已经尝试生成超过{max_try}次了!")
                # num_list[node.left_type] = recur_rand(recur_rand_time)
                num_list[node.right_type] = recur_rand(recur_rand_time, 0)
                num_list[node.left_type] = rand_a_int(sup=max_res // max(num_list[node.right_type], 1))
                val = node.eval(num_list)
                if val < 0 or val > max_res:
                    continue
                # 即便计算结果不符合范围条件, 仍然有10%的几率通过
                if sup >= val >= max(inf, 1) or randint(0, 9) == 0:
                    break

        elif node.left_type * node.right_type <= 0:
            idx = max(node.left_type, node.right_type)
            pre_node = node.pre[0]
            pre_lv = max(1, lv + 1)
            while True:
                num_try += 1
                if num_try > max_try:
                    raise ValueError(f"已经尝试生成超过{max_try}次了!")
                num_try = rand_a_node(pre_node, num_list, pre_lv, num_try)
                num_list[idx] = rand_a_int(sup=max_res // max(pre_node.eval(num_list), 1))
                val = node.eval(num_list)
                if val < 0 or val > max_res:
                    continue
                # 即便计算结果不符合范围条件, 仍然有10%的几率通过
                if sup >= val >= max(inf, 1) or randint(0, 9) == 0:
                    break

        else:
            pre_lv = max(1, lv + 1)
            while True:
                num_try += 1
                if num_try > max_try:
                    raise ValueError(f"已经尝试生成超过{max_try}次了!")
                num_try = rand_a_node(node.left_ele, num_list, pre_lv, num_try)
                num_try = rand_a_node(node.right_ele, num_list, pre_lv, num_try)
                val = node.eval(num_list)
                if val < 0 or val > max_res:
                    continue
                # 即便计算结果不符合范围条件, 仍然有10%的几率通过
                if sup >= val >= max(inf, 1) or randint(0, 9) == 0:
                    break

    elif node.op == "/":

        if node.left_type >= 0 and node.right_type >= 0:
            while True:
                num_try += 1
                if num_try > max_try:
                    raise ValueError(f"已经尝试生成超过{max_try}次了!")
                num_list[node.right_type] = recur_rand(recur_rand_time, 1)
                res_factor = rand_a_int(sup=max_num // num_list[node.right_type])
                num_list[node.left_type] = num_list[node.right_type] * res_factor
                val = node.eval(num_list)
                if val < 0 or val > max_res:
                    continue
                # 即便计算结果不符合范围条件, 仍然有10%的几率通过
                if sup >= val >= max(inf, 1) or randint(0, 9) == 0:
                    break

        elif node.left_type < 0 <= node.right_type:
            pre_lv = min(-1, lv - 1)
            while True:
                num_try += 1
                if num_try > max_try:
                    raise ValueError(f"已经尝试生成超过{max_try}次了!")
                num_try = rand_a_node(node.left_ele, num_list, pre_lv, num_try)
                if node.left_ele.eval(num_list) < 1:
                    continue
                # print("分解数字:" + str(node.left_ele.eval(num_list)))
                prime_divisors = decomp_num(node.left_ele.eval(num_list))
                if len(prime_divisors) >= 4 - min(lv, 0):
                    break
            while True:
                num_try += 1
                if num_try > max_try:
                    raise ValueError(f"已经尝试生成超过{max_try}次了!")
                # noinspection PyUnboundLocalVariable
                num_factor = randint(0, len(prime_divisors))
                selected_factors = sample(prime_divisors, num_factor)
                num_list[node.right_type] = int(np.product(np.array(selected_factors)))
                val = node.eval(num_list)
                if val < 0 or val > max_res:
                    continue
                if 1 < num_list[node.right_type] < node.left_ele.eval(num_list) or randint(0, 9) == 0:
                    break

        elif node.right_type < 0 <= node.left_type:
            pre_lv = min(-1, lv - 1)
            while True:
                num_try += 1
                if num_try > max_try:
                    raise ValueError(f"已经尝试生成超过{max_try}次了!")
                num_try = rand_a_node(node.right_ele, num_list, pre_lv, num_try)
                if node.right_ele.eval(num_list) == 0:
                    continue
                res_factor = rand_a_int(sup=max_num // max(node.right_ele.eval(num_list), 1))
                num_list[node.left_type] = node.right_ele.eval(num_list) * res_factor
                val = node.eval(num_list)
                if val < 0 or val > max_res:
                    continue
                # 即便计算结果不符合范围条件, 仍然有10%的几率通过
                if sup >= val >= max(inf, 1) or randint(0, 9) == 0:
                    break

        else:
            pre_lv = min(-1, lv - 1)
            while True:
                num_try += 1
                if num_try > max_try:
                    raise ValueError(f"已经尝试生成超过{max_try}次了!")
                num_try = rand_a_node(node.right_ele, num_list, pre_lv, num_try)
                right_val = node.right_ele.eval(num_list)
                if 0 < right_val <= int(max_num ** 0.5):
                    if right_val > 1 or randint(0, 9) == 0:
                        break
            while True:
                num_try += 1
                if num_try > max_try:
                    raise ValueError(f"已经尝试生成超过{max_try}次了!")
                num_try = rand_a_node(node.left_ele, num_list, pre_lv, num_try)
                left_val = node.left_ele.eval(num_list)
                if left_val % right_val == 0:
                    if 1 < left_val // right_val or randint(0, 9) == 0:
                        break
    else:
        while True:
            num_try += 1
            if num_try > max_try:
                raise ValueError(f"已经尝试生成超过{max_try}次了!")
            if node.left_type < 0:
                num_try = rand_a_node(node.left_ele, num_list, lv, num_try)
                # left_val = node.left_ele.eval(num_list)
            else:
                num_list[node.left_type] = rand_a_int()

            if node.right_type < 0:
                num_try = rand_a_node(node.right_ele, num_list, lv, num_try)
                # right_val = node.right_ele.eval(num_list)
            else:
                num_list[node.right_type] = rand_a_int()

            val = node.eval(num_list)
            if val < 0 or val > max_res:
                continue

            if inf < val < sup or randint(0, 9) == 0:
                break
    print(node.expr + "结束")
    return num_try


def gene_express(num_op):
    while True:
        try:
            link_list = ArithmeticLinkList(num_op)
            num_list = list(range(num_op + 1))
            rand_a_node(link_list.tail, num_list)
        except ValueError:
            continue
        break
    # noinspection PyUnboundLocalVariable
    return link_list.tail.get_human_expr(num_list), link_list.tail.eval(num_list)


if __name__ == "__main__":
    print(gene_express(6))
    pass
