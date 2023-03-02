#!usr/bin/env python
# -*- coding utf-8 -*-
"""
Project:    math_work2
File:       arithmetic_link_list.py
author:     Liu Duan-Yang
Email:      liuduanyangwj@qq.om
time:       2023/3/1  14:39
IDE:        PyCharm
"""
from arithmetic_node import ArithmeticNode
from random import randint, choice
op_list = ["+", "-", "*", "/"]


class ArithmeticLinkList:

    def __init__(self, num_op, start_num=0):
        # print(num_op, start_num)
        self.num_op = num_op
        self.op_list = []
        self.end_num = start_num
        self.tail = None
        self.headers = []
        self.build_link_list()

    def build_link_list(self):

        if self.num_op == 1:
            op = choice(op_list)
            self.op_list.append(op)
            a_node = ArithmeticNode(op, start_num=self.end_num)
            self.op_list = a_node.op_list
            self.end_num += 2
            self.tail = a_node
            # self.headers.append(a_node)
            # print(a_node.expr)
            # print(a_node.op)
            # print(a_node.op_list)
            # print(self.op_list)

        if self.num_op >= 2:
            is_binary = randint(0, 1)
            if self.num_op == 2:
                is_binary = 0
            if is_binary == 0:
                is_left = randint(0, 1)
                op = choice(op_list)
                a_tree = ArithmeticLinkList(self.num_op - 1, self.end_num)
                self.end_num = a_tree.end_num
                # self.op_list.extend(a_tree.op_list)
                if is_left:
                    a_node = ArithmeticNode(op, right_ele=a_tree.tail, start_num=self.end_num)
                else:
                    a_node = ArithmeticNode(op, left_ele=a_tree.tail, start_num=self.end_num)
                self.op_list = a_node.op_list
                self.end_num += 1
                self.tail = a_node
                self.headers.extend(a_tree.headers)
                # a_tree.tail.next = a_node
                # print(a_node.expr)
                # print(a_node.op)
                # print(a_node.op_list)
                # print(self.op_list)
            else:
                num_left = randint(1, self.num_op - 2)
                num_right = self.num_op - 1 - num_left
                # print(self.num_op, num_left, num_right)
                left_tree = ArithmeticLinkList(num_left, self.end_num)
                self.end_num = left_tree.end_num
                right_tree = ArithmeticLinkList(num_right, self.end_num)
                self.end_num = right_tree.end_num
                # self.op_list.extend(left_tree.op_list)
                # self.op_list.extend(right_tree.op_list)
                op = choice(op_list)
                # self.op_list.append(op)
                a_node = ArithmeticNode(op, left_tree.tail, right_tree.tail, self.end_num)
                self.op_list = a_node.op_list
                self.tail = a_node
                self.headers.extend(left_tree.headers)
                self.headers.extend(right_tree.headers)
                left_tree.tail.next = a_node
                right_tree.tail.next = a_node
                # print(a_node.expr)
                # print(a_node.op)
                # print(a_node.op_list)
                # print(self.op_list)


if __name__ == "__main__":
    a = ArithmeticLinkList(6)
    print(a.tail.expr)
    print(len(a.headers))
    pass
