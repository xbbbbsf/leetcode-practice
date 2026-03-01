import random
import re

class Minesweeper:
    def __init__(self, height=9, width=9, num_bombs=10):
        self.height = height
        self.width = width
        # 地雷数量
        self.num_bombs = num_bombs 
        # 初始化棋盘
        self.board = self.make_new_board()
        self.dug = set() # 记录已经翻开的格子，例如 (0, 0)
        self.flags = set() # 记录标记的旗帜

    def make_new_board(self):
        # 1. 创建一个全是空值的棋盘
        board = [[None for _ in range(self.width)] for _ in range(self.height)]

        # 2. 随机布置地雷
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.height * self.width - 1)
            row = loc // self.width
            col = loc % self.width

            # 确保不要重复埋雷
            if board[row][col] == '*':
                continue

            board[row][col] = '*' # '*' 代表地雷
            bombs_planted += 1

        # 3. 计算每个格子周围的地雷数
        for r in range(self.height):
            for c in range(self.width):
                if board[r][c] == '*':
                    continue
                # get_num_neighboring_bombs 会计算 (r, c) 周围的雷数
                board[r][c] = str(self.get_num_neighboring_bombs(r, c))

        return board

    def get_num_neighboring_bombs(self, row, col):
        num_neighboring_bombs = 0
        # 检查周围 8 个格子
        #这个居然是最优的遍历方法
        for r in range(max(0, row-1), min(self.height-1, row+1)+1):
            for c in range(max(0, col-1), min(self.width-1, col+1)+1):
                if r == row and c == col:
                    continue
                if self.board[r][c] == '*':
                    num_neighboring_bombs += 1
        return num_neighboring_bombs

    def reveal(self, row, col):
        # 翻开格子
        self.dug.add((row, col))

        # 如果是地雷，返回 False (游戏结束)
        if self.board[row][col] == '*':
            return False
        # 如果周围有雷，只翻开这一个格子
        elif self.board[row][col] != '0':
            return True

        # 如果是 '0'，自动翻开周围所有格子 (递归)
        for r in range(max(0, row-1), min(self.height-1, row+1)+1):
            for c in range(max(0, col-1), min(self.width-1, col+1)+1):
                if (r, c) in self.dug:
                    continue
                self.reveal(r, c)
        return True

    def display(self, show_all=False):
        # 打印棋盘
        # 打印列号
        print('  ', ' '.join([str(i) for i in range(self.width)]))
        
        for r in range(self.height):
            row_str = f"{r}|"
            for c in range(self.width):
                if (r, c) in self.dug or show_all:
                    # 如果已经翻开或者要求显示全部，显示真实内容
                    row_str += str(self.board[r][c]) + "|"
                elif (r, c) in self.flags:
                    # 如果标记了旗帜
                    row_str += "F|"
                else:
                    # 否则显示为隐藏格子
                    row_str += " |"
            print(row_str)
        print('')

    def play(self):
        print("扫雷游戏开始！输入 'q' 退出，输入 'f' 标记旗帜。")
        print("输入格式：行 列 [操作] (例如: 0 0 或 0 0 f)")

        while len(self.dug) < self.height * self.width - self.num_bombs:
            self.display()

            # 获取用户输入
            user_input = input("请输入位置: ").split()
            if user_input[0].lower() == 'q':
                print("游戏退出。")
                return

            # 解析输入
            try:
                row = int(user_input[0])
                col = int(user_input[1])
                
                # 检查坐标是否越界
                if row < 0 or row >= self.height or col < 0 or col >= self.width:
                    print("坐标超出范围！")
                    continue

                # 处理标记旗帜
                if len(user_input) >= 3 and user_input[2].lower() == 'f':
                    if (row, col) in self.flags:
                        self.flags.remove((row, col))
                        print(f"已移除 ({row}, {col}) 的旗帜")
                    else:
                        self.flags.add((row, col))
                        print(f"已标记 ({row}, {col}) 为旗帜")
                    continue

                # 如果该位置已经有旗帜，不允许翻开
                if (row, col) in self.flags:
                    print("该位置已有旗帜，请先移除旗帜。")
                    continue

                # 如果该位置已经翻开，跳过
                if (row, col) in self.dug:
                    continue

                # 翻开格子
                safe = self.reveal(row, col)
                if not safe:
                    # 踩雷了
                    self.display(show_all=True)
                    print("你踩到地雷了！游戏结束。")
                    return

            except ValueError:
                print("输入格式错误，请输入数字。")
            except IndexError:
                print("请输入完整的行和列。")

        # 赢得游戏
        self.display(show_all=True)
        print("恭喜你，扫雷成功！")

# --- 主程序 ---
if __name__ == '__main__':
    # 可以修改参数：高度、宽度、地雷数
    game = Minesweeper(height=9, width=9, num_bombs=10)
    game.play()