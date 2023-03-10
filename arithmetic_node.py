#!usr/bin/env python
# -*- coding utf-8 -*-
"""
Project:    math_work2
File:       arithmetic_node.py
author:     Liu Duan-Yang
Email:      liuduanyangwj@qq.om
time:       2023/3/1  14:26
IDE:        PyCharm
"""
import fractions


op_dict = {"+": -1,
           "-": -2,
           "*": -3,
           "/": -4}


class ArithmeticNode:
    def __init__(self, op, left_ele=None, right_ele=None, start_num=0):
        self.op = op
        self.op_list = []
        if self.op == "+" or self.op == "-":
            self.type = "1st"
        else:
            self.type = '2nd'
        self.left_ele = left_ele
        self.right_ele = right_ele
        self.start_num = start_num
        self.end_num = 0
        self.idx_list = []
        self.expr = ""
        self.inv_expr = ""
        self.next = None
        self.pre = []
        # 若左侧/右侧是数字, 则self.left_type/self.right_type是数字编号, 否则代表的左侧/右侧最后一步的计算种类
        # -1: 加法; -2: 减法; -3: 乘法, -4: 除法
        self.left_type = 0
        self.right_type = 0

        if isinstance(left_ele, self.__class__):
            self.pre.append(left_ele)
            self.start_num = max(self.start_num, left_ele.end_num)
            self.idx_list.extend(left_ele.idx_list)
            self.left_type = op_dict[left_ele.op]
            self.op_list.extend(left_ele.op_list)
        if isinstance(right_ele, self.__class__):
            self.pre.append(right_ele)
            self.start_num = max(self.start_num, right_ele.end_num)
            self.idx_list.extend(right_ele.idx_list)
            self.right_type = op_dict[right_ele.op]
            self.op_list.extend(right_ele.op_list)
        self.end_num = self.start_num
        self.op_list.append(self.op)

        self.build_express()

    def build_express(self):

        left_str = ""
        right_str = ""
        i_left_str = ""
        i_right_str = ""

        if not isinstance(self.left_ele, self.__class__):
            left_str = f"{{{self.end_num}}}"
            i_left_str = left_str
            self.left_type = self.end_num
            self.end_num += 1

        if not isinstance(self.right_ele, self.__class__):
            right_str = f"{{{self.end_num}}}"
            i_right_str = right_str
            self.right_type = self.end_num
            self.end_num += 1

        if self.op == "+":
            if isinstance(self.left_ele, self.__class__):
                left_str = self.left_ele.expr
                if self.left_ele.type == '1st':
                    i_left_str = self.left_ele.inv_expr
                else:
                    i_left_str = self.left_ele.expr
            if isinstance(self.right_ele, self.__class__):
                right_str = self.right_ele.expr
                if self.right_ele.type == '1st':
                    i_right_str = self.right_ele.inv_expr
                else:
                    i_right_str = self.right_ele.expr
            self.expr = f"{left_str}+{right_str}"
            self.inv_expr = f"{i_left_str}-{i_right_str}"

        elif self.op == "-":
            if isinstance(self.left_ele, self.__class__):
                left_str = self.left_ele.expr
                if self.left_ele.type == '1st':
                    i_left_str = self.left_ele.inv_expr
                else:
                    i_left_str = self.left_ele.expr
            if isinstance(self.right_ele, self.__class__):
                if self.right_ele.type == '1st':
                    right_str = self.right_ele.inv_expr
                    i_right_str = self.right_ele.expr
                else:
                    right_str = self.right_ele.expr
                    i_right_str = self.right_ele.expr
            self.expr = f"{left_str}-{right_str}"
            self.inv_expr = f"{i_left_str}+{i_right_str}"

        elif self.op == "*":
            if isinstance(self.left_ele, self.__class__):
                if self.left_ele.type == '1st':
                    left_str = f"({self.left_ele.expr})"
                    i_left_str = left_str
                else:
                    left_str = self.left_ele.expr
                    i_left_str = self.left_ele.inv_expr
            if isinstance(self.right_ele, self.__class__):
                if self.right_ele.type == '1st':
                    right_str = f"({self.right_ele.expr})"
                    i_right_str = right_str
                else:
                    right_str = self.right_ele.expr
                    i_right_str = self.right_ele.inv_expr
            self.expr = f"{left_str}*{right_str}"
            self.inv_expr = f"{i_left_str}/{i_right_str}"

        elif self.op == "/":
            if isinstance(self.left_ele, self.__class__):
                if self.left_ele.type == '1st':
                    left_str = f"({self.left_ele.expr})"
                    i_left_str = left_str
                else:
                    left_str = self.left_ele.expr
                    i_left_str = self.left_ele.inv_expr
            if isinstance(self.right_ele, self.__class__):
                if self.right_ele.type == '1st':
                    right_str = f"({self.right_ele.expr})"
                    i_right_str = right_str
                else:
                    right_str = self.right_ele.inv_expr
                    i_right_str = self.right_ele.expr
            self.expr = f"{left_str}/{right_str}"
            self.inv_expr = f"{i_left_str}*{i_right_str}"

        self.idx_list.extend(list(range(self.start_num, self.end_num)))

    def get_human_expr(self, num_list):

        if len(num_list) != self.end_num:
            raise ValueError("给出的数字数与字符长度不符")
        expr = self.expr.format(*num_list).replace("*", "×").replace("/", "÷") + "="
        return expr

    def eval(self, num_list, is_all_int=True):

        if len(num_list) < self.end_num:
            raise ValueError("给出的数字数不够代入计算!")
        if is_all_int:
            frac_num_list = []
            for num in num_list:
                frac_num_list.append(fractions.Fraction(num, 1))
            expr = self.expr.format(*frac_num_list)
        else:
            expr = self.expr.format(*num_list)
        val = eval(expr)
        if int(val) == val:
            val = int(val)
        return val
        # print(eval(expr))


if __name__ == "__main__":
    a = ArithmeticNode("+", start_num=0)
    b = ArithmeticNode("-", start_num=2)
    c = ArithmeticNode("*", start_num=4)
    d = ArithmeticNode("/", start_num=6)
    e = ArithmeticNode("*", a, b)
    pass
