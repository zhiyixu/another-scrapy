# pipelines.py
class Pipeline:
    def process_item(self, item, spider):
        # 假设这里简单地将数据打印出来，实际上可以存入数据库或文件等
        print("Processing item:", item)
        return item
