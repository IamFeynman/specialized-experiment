class Cal_Core:
    def __init__(self):
        self.stack = []
        self.last_expression = ''

    def cal_by_operation(self, op_str):
        try:
            if op_str == 'clean_stack':
                self.stack.clear()
                return '', None
            if op_str == 'C' or op_str == 'CE':
                self.stack.clear()
                return '', None
            if op_str == '<-':
                self.stack.pop()
                expression = ''.join(self.stack)
                return str(expression), None
            if op_str == '=':
                result = self.calculate()
                expression = ''.join(self.stack)  # 获取当前表达式
                self.last_expression = expression  # 更新最后一次表达式
                self.stack.clear()
                return str(self.last_expression), self.limit_result(result)  # 返回最后一次表达式和结果
            self.stack.append(op_str)
            expression = ''.join(self.stack)
            return str(expression), None  # 返回最后一次表达式和结果
        except Exception as e:
            expression = ''.join(self.stack)
            self.stack.clear()
            return str(expression), "ERROR"

    def calculate(self):
        expression = ''.join(self.stack)
        return eval(expression)

    def limit_result(self, result):
        # 如果结果超过 9 位，则截断为 9 位
        result_str = str(result)
        if len(result_str) > 9:
            if type(result) == float:
                return float(result_str[:9])
            return int(result_str[:9])
        return result

if __name__ == "__main__":
    cal = Cal_Core()
    while True:
        ans = cal.cal_by_operation(input())
        if ans is not None:
            print(ans)
