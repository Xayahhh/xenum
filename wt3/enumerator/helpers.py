
class NameGenerator:

    def __init__(self):
        # self.name_counter = 0
        self.prefixes = {}

    def generate_name(self, prefix: str = "") -> str:
        """
        Generates a unique name for a node based on its type and a counter.
        """
        if prefix not in self.prefixes:
            self.prefixes[prefix] = 0
        self.prefixes[prefix] += 1
        return f"{prefix}{self.prefixes[prefix]}"
    
    def copy(self):
        """
        Creates a copy of the NameGenerator with the same state.
        """
        new_gen = NameGenerator()
        for key, value in self.prefixes.items():
            new_gen.prefixes[key] = value
        return new_gen
    

def partition_list(data: list, n: int) -> list[list[list]]:

    results = []

    def backtrack(item_index: int, partitions: list[list]):
        remaining_items = len(data) - item_index
        empty_partitions = sum(1 for p in partitions if not p)
        if remaining_items < empty_partitions:
            return

        if item_index == len(data):
            results.append([list(p) for p in partitions])
            return

        current_item = data[item_index]

        # --- 递归与回溯 ---
        # 遍历所有 n 个分区，尝试将当前元素放入其中
        for i in range(n):
            # 1. 做出选择：将元素放入第 i 个分区
            partitions[i].append(current_item)
            
            # 2. 向下递归：处理下一个元素
            backtrack(item_index + 1, partitions)
            
            # 3. 撤销选择（回溯）
            partitions[i].pop()

            if not partitions[i]:
                break

    initial_partitions = [[] for _ in range(n)]
    backtrack(0, initial_partitions)

    return results

